import base64, json, os, pathlib, subprocess, time, uuid
from datetime import datetime, timezone
import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

ROOT=pathlib.Path('/tmp/naver-carrier'); OUT=ROOT/'out'; KEYS=ROOT/'keys'; PROFILE=ROOT/'profile'
for p in (ROOT,OUT,KEYS,PROFILE): p.mkdir(parents=True,exist_ok=True)
REPO=os.environ['REPOSITORY']; TOKEN=os.environ['GH_TOKEN']; BRANCH=os.environ.get('CARRIER_REF','naver-persistent-carrier-20260830')
MODE=os.environ.get('CARRIER_MODE','bootstrap'); GEN=os.environ.get('CARRIER_GENERATION') or f'g-{uuid.uuid4().hex[:12]}'
PRED=os.environ.get('CARRIER_PREDECESSOR',''); RUN_ID=os.environ.get('GITHUB_RUN_ID','')
CHROME=os.environ.get('CHROME_BINARY',''); DRIVER=os.environ.get('CHROMEDRIVER','')
API=f'https://api.github.com/repos/{REPO}'; HEAD={'Authorization':f'Bearer {TOKEN}','Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
RUNTIME=f'.bridge/carrier/runtime/{GEN}'; CURRENT='.bridge/carrier/current.json'; CURRENT_KEY='.bridge/carrier/current-public.pem'; COMMAND='.bridge/carrier/mail-command.enc'; COMMAND_STATUS='.bridge/carrier/command-status.json'

def now(): return datetime.now(timezone.utc).isoformat()
def get_obj(path):
    r=requests.get(f'{API}/contents/{path}',headers=HEAD,params={'ref':BRANCH},timeout=30)
    if r.status_code==404:return None
    r.raise_for_status(); return r.json()
def get_bytes(path):
    o=get_obj(path); return base64.b64decode(o['content']) if o else None
def put_bytes(path,data,msg):
    for i in range(5):
        o=get_obj(path); body={'message':msg,'content':base64.b64encode(data).decode(),'branch':BRANCH}
        if o: body['sha']=o['sha']
        r=requests.put(f'{API}/contents/{path}',headers=HEAD,json=body,timeout=30)
        if r.status_code in (409,422) and i<4: time.sleep(1+i/2); continue
        r.raise_for_status(); return
    raise RuntimeError(f'write failed: {path}')
def put_text(path,text,msg): put_bytes(path,text.encode(),msg)
def put_json(path,obj,msg): put_text(path,json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n',msg)
def delete(path,msg):
    o=get_obj(path)
    if not o:return
    r=requests.delete(f'{API}/contents/{path}',headers=HEAD,json={'message':msg,'sha':o['sha'],'branch':BRANCH},timeout=30)
    if r.status_code not in (200,404): r.raise_for_status()
def status(name,**x):
    p={'generation':GEN,'run_id':RUN_ID,'mode':MODE,'status':name,'updated_at':now()}; p.update(x); put_json(f'{RUNTIME}/status.json',p,f'Carrier {GEN}: {name}')
def cmd_status(cid,action,name,**x):
    p={'generation':GEN,'run_id':RUN_ID,'command_id':cid,'action':action,'status':name,'updated_at':now()}; p.update(x); put_json(COMMAND_STATUS,p,f'Carrier command {cid}: {name}')

def ensure_keys():
    priv=KEYS/'private.pem'; pub=KEYS/'public.pem'
    if priv.exists(): return
    k=rsa.generate_private_key(public_exponent=65537,key_size=2048)
    priv.write_bytes(k.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
    pub.write_bytes(k.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo))
def pub_bytes(): return (KEYS/'public.pem').read_bytes()
def priv_key(): return serialization.load_pem_private_key((KEYS/'private.pem').read_bytes(),password=None)
def encrypt(pub,payload,target):
    p=serialization.load_pem_public_key(pub); key=AESGCM.generate_key(bit_length=256); nonce=os.urandom(12)
    raw=json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode(); ct=AESGCM(key).encrypt(nonce,raw,None)
    wk=p.encrypt(key,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return {'v':1,'generation':target,'wrapped_key':base64.b64encode(wk).decode(),'nonce':base64.b64encode(nonce).decode(),'ciphertext':base64.b64encode(ct).decode()}
def decrypt(env):
    key=priv_key().decrypt(base64.b64decode(env['wrapped_key']),padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    raw=AESGCM(key).decrypt(base64.b64decode(env['nonce']),base64.b64decode(env['ciphertext']),None); return json.loads(raw.decode())

def start_browser(url='about:blank'):
    env=os.environ.copy(); env['DISPLAY']=':99'; env['HOME']=str(ROOT/'home'); pathlib.Path(env['HOME']).mkdir(exist_ok=True)
    subprocess.Popen(['Xvfb',':99','-screen','0','1440x900x24','-ac'],stdout=open(ROOT/'xvfb.log','ab'),stderr=subprocess.STDOUT,env=env,start_new_session=True); time.sleep(1)
    args=[CHROME,'--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--no-first-run','--no-default-browser-check','--password-store=basic','--remote-debugging-address=127.0.0.1','--remote-debugging-port=9222',f'--user-data-dir={PROFILE}','--window-size=1440,900',url]
    subprocess.Popen(args,stdout=open(ROOT/'chrome.log','ab'),stderr=subprocess.STDOUT,env=env,start_new_session=True)
    for _ in range(90):
        try: requests.get('http://127.0.0.1:9222/json/version',timeout=1).raise_for_status(); return
        except Exception: time.sleep(1)
    raise RuntimeError('chrome did not start')
def attach():
    o=webdriver.ChromeOptions(); o.debugger_address='127.0.0.1:9222'; return webdriver.Chrome(service=Service(DRIVER),options=o)
def ready(d,n=30): WebDriverWait(d,n).until(lambda x:x.execute_script('return document.readyState') in ('interactive','complete'))

def capture_state(d):
    d.get('https://mail.naver.com'); ready(d); time.sleep(1)
    cookies=d.execute_cdp_cmd('Network.getAllCookies',{}).get('cookies',[]); clean=[]
    for c in cookies:
        if 'naver' not in (c.get('domain') or ''): continue
        x={'name':c['name'],'value':c['value'],'domain':c['domain'],'path':c.get('path','/'),'secure':bool(c.get('secure')),'httpOnly':bool(c.get('httpOnly'))}
        if c.get('expires',-1)>0:x['expires']=c['expires']
        if c.get('sameSite') in ('Strict','Lax','None'):x['sameSite']=c['sameSite']
        clean.append(x)
    storage={}
    try: storage=d.execute_script("const o={};for(let i=0;i<localStorage.length;i++){let k=localStorage.key(i);o[k]=localStorage.getItem(k)}return o")
    except Exception: pass
    return {'v':1,'captured_at':now(),'cookies':clean,'mail_local_storage':storage}
def restore_state(d,s):
    d.execute_cdp_cmd('Network.enable',{}); d.execute_cdp_cmd('Network.setCookies',{'cookies':s.get('cookies',[])})
    d.get('https://mail.naver.com'); ready(d); time.sleep(1)
    try:
        d.execute_script("for(const [k,v] of Object.entries(arguments[0]||{}))localStorage.setItem(k,v)",s.get('mail_local_storage',{})); d.refresh(); ready(d); time.sleep(1)
    except Exception: pass

def publish_current():
    put_bytes(CURRENT_KEY,pub_bytes(),f'Carrier {GEN}: current key'); put_json(CURRENT,{'generation':GEN,'run_id':RUN_ID,'status':'ready','mode':MODE,'carrier_ref':BRANCH,'started_at':now()},f'Carrier {GEN}: ready'); put_text(COMMAND,'PENDING\n',f'Carrier {GEN}: reset command'); status('ready',ok=True)
def dispatch_child(target):
    body={'event_type':'persistent-web-session-handoff','client_payload':{'carrier_ref':BRANCH,'generation':target,'predecessor_run_id':RUN_ID}}
    r=requests.post(f'{API}/dispatches',headers=HEAD,json=body,timeout=30); r.raise_for_status()
def relay(d):
    target=f'g-{uuid.uuid4().hex[:12]}'; status('starting_handoff',target_generation=target); dispatch_child(target)
    pub=None; deadline=time.time()+480
    while time.time()<deadline:
        pub=get_bytes(f'.bridge/carrier/runtime/{target}/public.pem')
        if pub: break
        time.sleep(2)
    if not pub: status('handoff_child_timeout',ok=False,target_generation=target); return False
    put_json(f'.bridge/carrier/runtime/{target}/handoff.enc',encrypt(pub,capture_state(d),target),f'Carrier {GEN}: handoff to {target}'); status('handoff_sent',target_generation=target)
    deadline=time.time()+720
    while time.time()<deadline:
        raw=get_bytes(CURRENT)
        if raw:
            try:
                cur=json.loads(raw.decode())
                if cur.get('generation')==target and cur.get('status')=='ready': status('handed_off',ok=True,target_generation=target); return True
            except Exception: pass
        time.sleep(3)
    status('handoff_not_confirmed',ok=False,target_generation=target); return False
