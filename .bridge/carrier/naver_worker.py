import json, os, pathlib, re, sys, time, traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import carrier_core as c

def visible(e):
    try:return e.is_displayed() and e.size.get('width',0)>3 and e.size.get('height',0)>3
    except:return False
def text(e):
    try:return (e.text or e.get_attribute('aria-label') or e.get_attribute('title') or '').strip()
    except:return ''
def qr(d):
    d.get('https://nid.naver.com/nidlogin.login'); c.ready(d); time.sleep(1)
    for e in d.find_elements(By.XPATH,"//*[self::a or self::button or @role='button' or @role='tab']"):
        if visible(e) and re.search(r'QR\s*(코드|로그인|sign-in)?',text(e),re.I):
            try:d.execute_script('arguments[0].click()',e);break
            except:pass
    else:d.get('https://nid.naver.com/nidlogin.login?mode=qrcode')
    c.ready(d); time.sleep(2); target=None
    for sel in ["img[id*='qr' i]","img[class*='qr' i]","[id*='qr' i] img","[class*='qr' i] img"]:
        xs=[e for e in d.find_elements(By.CSS_SELECTOR,sel) if visible(e) and e.size.get('width',0)>=100]
        if xs: target=xs[0]; break
    (target or d.find_element(By.TAG_NAME,'body')).screenshot(str(c.OUT/'login.png'))
def auth(d):
    try:
        d.get('https://mail.naver.com'); c.ready(d); time.sleep(1); u=d.current_url.lower()
        if 'nidlogin' in u:return False
        names={x.get('name') for x in d.get_cookies()}
        if 'NID_AUT' in names or 'NID_SES' in names:return True
        return bool(re.search(r'메일\s*쓰기|받은메일함|메일함',d.find_element(By.TAG_NAME,'body').text))
    except:return False
def wait_login(d,n=600):
    end=time.time()+n
    while time.time()<end:
        try:
            names={x.get('name') for x in d.get_cookies()}
            if ('NID_AUT' in names or 'NID_SES' in names) and auth(d):return True
            if 'nidlogin' not in d.current_url.lower() and auth(d):return True
        except:pass
        time.sleep(2)
    return False

def subject(d):
    for s in ["input[placeholder*='제목']","input[aria-label*='제목']","input[name*='subject' i]","input[id*='subject' i]","input[id*='title' i]"]:
        xs=[e for e in d.find_elements(By.CSS_SELECTOR,s) if visible(e)]
        if xs:return xs[0]
    return None
def send(d,cmd):
    to=str(cmd['to']).strip(); sub=str(cmd.get('subject') or ''); bodytxt=str(cmd.get('body') or '')
    if '@' not in to:raise ValueError('invalid recipient')
    d.get('https://mail.naver.com/v2/new'); c.ready(d); time.sleep(2)
    if 'nidlogin' in d.current_url.lower():raise RuntimeError('session lost')
    rec=d.find_elements(By.ID,'recipient_input_element'); rec=rec[0] if rec and visible(rec[0]) else None; sj=subject(d)
    if rec is None or sj is None:raise RuntimeError('compose header not found')
    d.execute_script("const e=arguments[0],v=arguments[1],s=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;s.call(e,'');e.dispatchEvent(new Event('input',{bubbles:true}));s.call(e,v);e.dispatchEvent(new Event('input',{bubbles:true}));e.focus()",rec,to); time.sleep(.5); sj.click(); sj.clear(); sj.send_keys(sub)
    ed=None
    for s in ["[contenteditable='true'][role='textbox']","div[contenteditable='true']","textarea[placeholder*='내용']"]:
        xs=[e for e in d.find_elements(By.CSS_SELECTOR,s) if visible(e)]
        if xs:ed=xs[0];break
    if ed is None:
        for fr in d.find_elements(By.CSS_SELECTOR,'iframe'):
            try:
                d.switch_to.frame(fr); xs=[e for e in d.find_elements(By.CSS_SELECTOR,"body[contenteditable='true'],[contenteditable='true'],textarea") if visible(e)]
                if xs:ed=xs[0];break
                d.switch_to.default_content()
            except:d.switch_to.default_content()
    if ed is None:raise RuntimeError('body editor not found')
    ed.click(); ed.send_keys(bodytxt); d.switch_to.default_content(); time.sleep(.5)
    page=d.find_element(By.TAG_NAME,'body').text
    if to not in page:raise RuntimeError('recipient readback failed')
    btn=None
    for e in d.find_elements(By.XPATH,"//*[self::button or self::a or @role='button']"):
        if visible(e) and text(e) in ('보내기','메일 보내기','Send'):btn=e;break
    if btn is None:raise RuntimeError('send button not found')
    d.execute_script('arguments[0].click()',btn); time.sleep(3)
    for dialog in d.find_elements(By.CSS_SELECTOR,"[role='dialog'],.layer,.modal"):
        if not visible(dialog):continue
        for e in dialog.find_elements(By.XPATH,".//*[self::button or self::a or @role='button']"):
            if visible(e) and text(e) in ('확인','보내기','Send'):d.execute_script('arguments[0].click()',e);time.sleep(2);break
    ok='/done' in d.current_url.lower() or re.search(r'메일을\s*보냈|발송.*완료|보내기\s*완료',d.find_element(By.TAG_NAME,'body').text,re.I)
    if not ok:raise RuntimeError('send success not detected')
    return d.current_url

def prepare():
    c.ensure_keys(); c.put_bytes(f'{c.RUNTIME}/public.pem',c.pub_bytes(),f'Carrier {c.GEN}: handoff key')
    if c.MODE=='bootstrap':
        c.status('bootstrap_qr_ready'); c.start_browser('https://nid.naver.com/nidlogin.login'); d=c.attach()
        try:qr(d)
        finally:d.quit()
        return
    c.status('waiting_handoff',predecessor=c.PRED); path=f'{c.RUNTIME}/handoff.enc'; end=time.time()+900; env=None
    while time.time()<end:
        raw=c.get_bytes(path)
        if raw:
            try:
                x=json.loads(raw.decode())
                if x.get('generation')==c.GEN:env=x;break
            except:pass
        time.sleep(2)
    if env is None:raise TimeoutError('handoff not received')
    state=c.decrypt(env); c.start_browser(); d=c.attach()
    try:
        c.restore_state(d,state)
        if auth(d):c.status('handoff_restored',ok=True)
        else:qr(d); (c.ROOT/'needs-login').write_text('1'); c.status('relogin_required',ok=False)
    finally:d.quit()
    try:c.delete(path,f'Carrier {c.GEN}: consume handoff')
    except:pass

def run():
    d=c.attach()
    try:
        if c.MODE=='bootstrap' or (c.ROOT/'needs-login').exists():
            if not wait_login(d):raise TimeoutError('login timeout')
        elif not auth(d):qr(d); c.status('relogin_required',ok=False)
        if not auth(d) and not wait_login(d):raise TimeoutError('relogin timeout')
        c.publish_current(); started=time.time(); last_keep=0; last_id=None; rotate=False
        rotate_after=int(os.environ.get('ROTATE_AFTER_SECONDS','16200')); hard=int(os.environ.get('HARD_STOP_AFTER_SECONDS','20100')); poll=float(os.environ.get('COMMAND_POLL_SECONDS','5')); keep=int(os.environ.get('KEEPALIVE_SECONDS','900'))
        while time.time()-started<hard:
            age=time.time()-started
            if rotate or age>=rotate_after:
                if c.relay(d):return
                rotate=False; started=time.time()-(rotate_after-900)
            raw=c.get_bytes(c.COMMAND)
            if raw and raw.strip()!=b'PENDING':
                try:
                    env=json.loads(raw.decode())
                    if env.get('generation')==c.GEN:
                        cmd=c.decrypt(env); cid=str(cmd.get('id') or ''); act=str(cmd.get('action') or '')
                        if cid and cid!=last_id:
                            last_id=cid
                            if act=='send_mail':
                                c.cmd_status(cid,act,'sending')
                                try:c.cmd_status(cid,act,'sent',ok=True,url=send(d,cmd))
                                except Exception as e:c.cmd_status(cid,act,'failed',ok=False,error=f'{type(e).__name__}: {e}')
                            elif act=='rotate_now':c.cmd_status(cid,act,'accepted',ok=True);rotate=True
                            elif act=='ping':ok=auth(d);c.cmd_status(cid,act,'pong',ok=ok,authenticated=ok)
                except:pass
            if time.time()-last_keep>=keep:
                if not auth(d):c.status('session_lost',ok=False);qr(d);c.status('relogin_required',ok=False);wait_login(d)
                last_keep=time.time()
            time.sleep(poll)
        raise RuntimeError('hard stop without handoff')
    finally:
        try:d.quit()
        except:pass

def main():
    try:
        (prepare if sys.argv[1]=='prepare' else run)()
    except Exception as e:
        try:c.status('fatal',ok=False,error=f'{type(e).__name__}: {e}',traceback=traceback.format_exc()[-1000:])
        except:pass
        raise
if __name__=='__main__':main()
