import base64, json, os, pathlib, re, sys, time
import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from selenium import webdriver
from selenium.webdriver.common.by import By

ROOT = pathlib.Path(os.environ.get('LOCALAPPDATA', str(pathlib.Path.home()))) / 'NaverMailBridge'
ROOT.mkdir(parents=True, exist_ok=True)
PRIVATE = pathlib.Path(os.environ.get('NMB_PRIVATE_KEY', str(ROOT / 'private.pem')))
PUBLIC = ROOT / 'public.pem'
DEBUGGER = os.environ.get('NMB_DEBUGGER', '127.0.0.1:9222')
REPO = os.environ.get('REPOSITORY', 'Valon-Jang/Root-Engineering')
BRANCH = os.environ.get('COMMAND_BRANCH', 'naver-local-persistent-20260830')
TOKEN = os.environ.get('GH_TOKEN', '')
STATUS_PATH = '.bridge/local/status.json'
LAST_PATH = ROOT / 'last-command.json'


def now():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def visible(e):
    try:
        return e.is_displayed() and e.size.get('width', 0) > 3 and e.size.get('height', 0) > 3
    except Exception:
        return False


def label(e):
    try:
        return (e.text or e.get_attribute('aria-label') or e.get_attribute('title') or '').strip()
    except Exception:
        return ''


def init_key():
    if not PRIVATE.exists():
        k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        PRIVATE.write_bytes(k.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
        PUBLIC.write_bytes(k.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
    elif not PUBLIC.exists():
        k = serialization.load_pem_private_key(PRIVATE.read_bytes(), password=None)
        PUBLIC.write_bytes(k.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
    print(str(PUBLIC))


def decrypt_envelope(raw: bytes):
    env = json.loads(raw.decode('utf-8'))
    keyobj = serialization.load_pem_private_key(PRIVATE.read_bytes(), password=None)
    aes_key = keyobj.decrypt(
        base64.b64decode(env['wrapped_key']),
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    plain = AESGCM(aes_key).decrypt(base64.b64decode(env['nonce']), base64.b64decode(env['ciphertext']), None)
    return json.loads(plain.decode('utf-8'))


def api_headers():
    return {
        'Authorization': f'Bearer {TOKEN}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }


def write_status(obj):
    obj = dict(obj)
    obj['updated_at'] = now()
    text = json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '\n'
    (ROOT / 'status.json').write_text(text, encoding='utf-8')
    if not TOKEN:
        return
    api = f'https://api.github.com/repos/{REPO}/contents/{STATUS_PATH}'
    sha = None
    r = requests.get(api, headers=api_headers(), params={'ref': BRANCH}, timeout=30)
    if r.status_code == 200:
        sha = r.json().get('sha')
    elif r.status_code != 404:
        r.raise_for_status()
    body = {
        'message': f"Naver local mail status: {obj.get('status', 'update')}",
        'content': base64.b64encode(text.encode()).decode(),
        'branch': BRANCH,
    }
    if sha:
        body['sha'] = sha
    r = requests.put(api, headers=api_headers(), json=body, timeout=30)
    r.raise_for_status()


def attach():
    opts = webdriver.ChromeOptions()
    opts.debugger_address = DEBUGGER
    return webdriver.Chrome(options=opts)


def detach(driver):
    try:
        driver.service.stop()
    except Exception:
        pass


def accept_alert_if_any(driver):
    try:
        alert = driver.switch_to.alert
        txt = alert.text
        alert.accept()
        return txt
    except Exception:
        return None


def authenticated(driver):
    try:
        driver.get('https://mail.naver.com')
        time.sleep(1.5)
        alert = accept_alert_if_any(driver)
        if alert:
            return False, alert
        if 'nidlogin' in driver.current_url.lower():
            return False, 'redirected to login'
        names = {x.get('name') for x in driver.get_cookies()}
        if 'NID_AUT' in names or 'NID_SES' in names:
            return True, 'cookie'
        body = driver.find_element(By.TAG_NAME, 'body').text
        return bool(re.search(r'메일\s*쓰기|받은메일함|메일함', body)), 'page'
    except Exception as e:
        return False, f'{type(e).__name__}: {e}'


def find_subject(driver):
    for s in [
        "input[placeholder*='제목']",
        "input[aria-label*='제목']",
        "input[name*='subject' i]",
        "input[id*='subject' i]",
        "input[id*='title' i]",
    ]:
        xs = [e for e in driver.find_elements(By.CSS_SELECTOR, s) if visible(e)]
        if xs:
            return xs[0]
    return None


def send_mail(driver, cmd):
    to = str(cmd['to']).strip()
    subject = str(cmd.get('subject') or '')
    bodytxt = str(cmd.get('body') or '')
    if '@' not in to:
        raise ValueError('invalid recipient')

    driver.get('https://mail.naver.com/v2/new')
    time.sleep(2)
    alert = accept_alert_if_any(driver)
    if alert:
        raise RuntimeError(f'naver alert: {alert}')
    if 'nidlogin' in driver.current_url.lower():
        raise RuntimeError('session lost')

    recs = driver.find_elements(By.ID, 'recipient_input_element')
    rec = recs[0] if recs and visible(recs[0]) else None
    sj = find_subject(driver)
    if rec is None or sj is None:
        raise RuntimeError('compose header not found')

    driver.execute_script(
        "const e=arguments[0],v=arguments[1],s=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;"
        "s.call(e,'');e.dispatchEvent(new Event('input',{bubbles:true}));"
        "s.call(e,v);e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));e.focus();",
        rec, to,
    )
    time.sleep(0.7)
    sj.click(); sj.clear(); sj.send_keys(subject)

    editor = None
    for s in ["[contenteditable='true'][role='textbox']", "div[contenteditable='true']", "textarea[placeholder*='내용']"]:
        xs = [e for e in driver.find_elements(By.CSS_SELECTOR, s) if visible(e)]
        if xs:
            editor = xs[0]
            break
    if editor is None:
        for frame in driver.find_elements(By.CSS_SELECTOR, 'iframe'):
            try:
                driver.switch_to.frame(frame)
                xs = [e for e in driver.find_elements(By.CSS_SELECTOR, "body[contenteditable='true'],[contenteditable='true'],textarea") if visible(e)]
                if xs:
                    editor = xs[0]
                    break
                driver.switch_to.default_content()
            except Exception:
                driver.switch_to.default_content()
    if editor is None:
        raise RuntimeError('body editor not found')

    editor.click(); editor.send_keys(bodytxt)
    driver.switch_to.default_content()
    time.sleep(0.7)

    page = driver.find_element(By.TAG_NAME, 'body').text
    if to not in page:
        raise RuntimeError('recipient readback failed')

    send_btn = None
    for e in driver.find_elements(By.XPATH, "//*[self::button or self::a or @role='button']"):
        if visible(e) and label(e) in ('보내기', '메일 보내기', 'Send'):
            send_btn = e
            break
    if send_btn is None:
        raise RuntimeError('send button not found')

    driver.execute_script('arguments[0].click()', send_btn)
    time.sleep(3)
    for dialog in driver.find_elements(By.CSS_SELECTOR, "[role='dialog'],.layer,.modal"):
        if not visible(dialog):
            continue
        for e in dialog.find_elements(By.XPATH, ".//*[self::button or self::a or @role='button']"):
            if visible(e) and label(e) in ('확인', '보내기', 'Send'):
                driver.execute_script('arguments[0].click()', e)
                time.sleep(2)
                break

    ok = '/done' in driver.current_url.lower()
    if not ok:
        body = driver.find_element(By.TAG_NAME, 'body').text
        ok = bool(re.search(r'메일을\s*보냈|발송.*완료|보내기\s*완료', body, re.I))
    if not ok:
        raise RuntimeError('send success not detected')
    return driver.current_url


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == '--init-key':
        init_key(); return
    if len(sys.argv) < 2:
        raise SystemExit('usage: send_mail.py <encrypted-command-file>')
    if not PRIVATE.exists():
        raise RuntimeError(f'private key missing: {PRIVATE}')

    command_file = pathlib.Path(sys.argv[1])
    cmd = decrypt_envelope(command_file.read_bytes())
    cid = str(cmd.get('id') or '')
    action = str(cmd.get('action') or '')
    if not cid:
        raise ValueError('command id missing')

    if LAST_PATH.exists():
        try:
            last = json.loads(LAST_PATH.read_text(encoding='utf-8'))
            if last.get('command_id') == cid and last.get('status') == 'sent':
                write_status(last)
                return
        except Exception:
            pass

    driver = attach()
    try:
        if action == 'ping':
            ok, detail = authenticated(driver)
            result = {'command_id': cid, 'action': action, 'status': 'pong', 'ok': ok, 'authenticated': ok, 'detail': detail}
        elif action == 'send_mail':
            ok, detail = authenticated(driver)
            if not ok:
                raise RuntimeError(f'not authenticated: {detail}')
            write_status({'command_id': cid, 'action': action, 'status': 'sending', 'ok': True})
            url = send_mail(driver, cmd)
            result = {'command_id': cid, 'action': action, 'status': 'sent', 'ok': True, 'url': url}
        else:
            raise ValueError(f'unsupported action: {action}')
        LAST_PATH.write_text(json.dumps(result, ensure_ascii=False), encoding='utf-8')
        write_status(result)
    except Exception as e:
        result = {'command_id': cid, 'action': action, 'status': 'failed', 'ok': False, 'error': f'{type(e).__name__}: {e}'}
        LAST_PATH.write_text(json.dumps(result, ensure_ascii=False), encoding='utf-8')
        write_status(result)
        raise
    finally:
        detach(driver)


if __name__ == '__main__':
    main()
