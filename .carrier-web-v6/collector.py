#!/usr/bin/env python3
import argparse, concurrent.futures, hashlib, ipaddress, json, pathlib, re, socket, time
from urllib.parse import quote_plus, unquote, urlparse, parse_qs
import requests
from bs4 import BeautifulSoup

UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36 CarrierWebV6/0.1'
FILLERS=[
 r'(?i)\b(?:it is important to note that|it should be noted that|in other words|generally speaking|as a matter of fact)\b[,;:]?\s*',
 r'(?i)\b(?:currently,?\s+based on the information available,?|taking all of the above into consideration,?)\s*',
 r'(?:현재\s+확인된\s+바에\s+따르면|종합적으로\s+고려했을\s+때|다시\s+말해서|말씀드리자면)[,，]?\s*',
]
PROTECTED_MARKERS=re.compile(r'(?i)\b(?:not|no|never|only|except|unless|until|before|after|if|when|hold|release|must|shall|may|might|cannot|can\'t|without|scope|authority|approved?|denied?|cancel(?:led)?|supersed(?:e|ed)|deprecated|warning|error|failed?)\b|(?:아니|않|못|없|만|제외|예외|조건|경우|이후|이전|까지|보류|해제|승인|취소|대체|범위|권한|실패)')
NUM_ID=re.compile(r'https?://\S+|\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}:\d{2}\b|\b\d+(?:\.\d+)?\s*(?:%|ms|s|sec|seconds?|minutes?|hours?|days?|MB|GB|KB|tokens?|USD|KRW|원|개|회)?\b|\b[A-Z][A-Z0-9_-]{2,}\b')
WORD=re.compile(r'[A-Za-z0-9가-힣_+-]{2,}')
SENT_SPLIT=re.compile(r'(?<=[.!?。！？])\s+|\n+')

def safe_url(u):
    try:
        p=urlparse(u)
        if p.scheme not in ('http','https') or not p.hostname: return False
        host=p.hostname.lower()
        if host in ('localhost','localhost.localdomain') or host.endswith('.local'): return False
        try:
            for info in socket.getaddrinfo(host, p.port or (443 if p.scheme=='https' else 80), type=socket.SOCK_STREAM):
                ip=ipaddress.ip_address(info[4][0])
                if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved: return False
        except socket.gaierror: return False
        return True
    except Exception: return False

def clean_url(u):
    if not u: return None
    if 'duckduckgo.com/l/' in u:
        q=parse_qs(urlparse(u).query).get('uddg')
        if q: u=unquote(q[0])
    return u.split('#')[0]

def search_ddg(q,n,session):
    r=session.get('https://html.duckduckgo.com/html/?q='+quote_plus(q),timeout=15,headers={'User-Agent':UA})
    r.raise_for_status(); s=BeautifulSoup(r.text,'html.parser'); out=[]
    for a in s.select('a.result__a'):
        href=clean_url(a.get('href')); title=' '.join(a.stripped_strings)
        if href and safe_url(href): out.append({'url':href,'title':title,'engine':'ddg'})
        if len(out)>=n: break
    return out

def search_bing(q,n,session):
    r=session.get('https://www.bing.com/search?q='+quote_plus(q)+f'&count={max(n,10)}',timeout=15,headers={'User-Agent':UA})
    r.raise_for_status(); s=BeautifulSoup(r.text,'html.parser'); out=[]
    for a in s.select('li.b_algo h2 a'):
        href=clean_url(a.get('href')); title=' '.join(a.stripped_strings)
        if href and safe_url(href): out.append({'url':href,'title':title,'engine':'bing'})
        if len(out)>=n: break
    return out

def do_search(q,n):
    s=requests.Session(); errs=[]
    for fn in (search_ddg,search_bing):
        try:
            got=fn(q,n,s)
            if got: return q,got,errs
        except Exception as e: errs.append(f'{fn.__name__}:{type(e).__name__}:{e}')
    return q,[],errs

def visible_text(content,ctype):
    if 'html' not in ctype.lower(): return content.decode('utf-8','replace')
    soup=BeautifulSoup(content,'html.parser')
    for t in soup(['script','style','noscript','svg','canvas','template']): t.decompose()
    for t in soup.select('nav,footer,aside'): t.decompose()
    return '\n'.join(' '.join(x.split()) for x in soup.stripped_strings if x.strip())

def fetch_page(task):
    idx,u,title,q,max_bytes=task; t=time.time(); s=requests.Session(); h={'User-Agent':UA,'Accept':'text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.2'}
    try:
        if not safe_url(u): raise ValueError('unsafe_url')
        r=s.get(u,timeout=(5,20),headers=h,stream=True,allow_redirects=True); r.raise_for_status(); data=bytearray()
        for ch in r.iter_content(65536):
            data.extend(ch)
            if len(data)>=max_bytes: break
        text=visible_text(bytes(data),r.headers.get('content-type',''))
        return {'idx':idx,'url':r.url,'title':title,'query':q,'status':r.status_code,'text':text,'raw_bytes':len(data),'ms':round((time.time()-t)*1000,1)}
    except Exception as e:
        return {'idx':idx,'url':u,'title':title,'query':q,'error':f'{type(e).__name__}:{e}','text':'','raw_bytes':0,'ms':round((time.time()-t)*1000,1)}

def compact_sentence(s):
    orig=' '.join(s.split())
    if not orig: return orig
    protected=NUM_ID.findall(orig); markers=PROTECTED_MARKERS.findall(orig); x=orig
    for pat in FILLERS: x=re.sub(pat,'',x)
    x=re.sub(r'\s+',' ',x).strip(' ,;')
    if not x or any(p not in x for p in protected) or len(PROTECTED_MARKERS.findall(x))<len(markers): return orig
    return x

def query_terms(q):
    stop={'the','and','for','with','from','into','that','this','what','when','where','how','why','official','docs','documentation'}
    return {w.lower() for w in WORD.findall(q) if len(w)>2 and w.lower() not in stop}

def snippets(text,q,limit):
    terms=query_terms(q); cand=[]
    for s in SENT_SPLIT.split(text):
        s=' '.join(s.split())
        if len(s)<35 or len(s)>1000: continue
        low=s.lower(); overlap=sum(1 for t in terms if t in low); nums=len(NUM_ID.findall(s)); markers=len(PROTECTED_MARKERS.findall(s))
        score=overlap*5+min(nums,4)*1.5+min(markers,3)*1.2+min(len(s),300)/300
        if overlap or nums or markers: cand.append((score,s))
    cand.sort(key=lambda x:x[0],reverse=True); out=[]; seen=set()
    for _,s in cand:
        c=compact_sentence(s); k=re.sub(r'\W+','',c.lower())[:240]
        if k and k not in seen: seen.add(k); out.append(c)
        if len(out)>=limit: break
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--request',required=True); ap.add_argument('--out',required=True); ap.add_argument('--raw-dir',required=True); a=ap.parse_args()
    started=time.time(); req=json.load(open(a.request,encoding='utf-8')); rid=req.get('request_id') or pathlib.Path(a.request).stem
    queries=[str(x).strip() for x in req.get('queries',[]) if str(x).strip()][:50]; seeds=[str(x).strip() for x in req.get('urls',[]) if str(x).strip()][:100]
    perq=max(1,min(int(req.get('max_results_per_query',5)),10)); max_pages=max(1,min(int(req.get('max_pages',40)),100)); max_bytes=max(100000,min(int(req.get('max_bytes_per_page',1500000)),3000000)); snip=max(1,min(int(req.get('max_snippets_per_page',5)),12))
    if not queries and not seeds: raise SystemExit('request needs queries or urls')
    search_errors=[]; found=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5,thread_name_prefix='interceptor-search') as ex:
        for f in concurrent.futures.as_completed([ex.submit(do_search,q,perq) for q in queries]):
            q,rows,errs=f.result(); search_errors.extend({'query':q,'error':e} for e in errs); found.extend({**r,'query':q} for r in rows)
    found.extend({'url':u,'title':'seed','engine':'seed','query':queries[0] if queries else ''} for u in seeds if safe_url(u))
    unique=[]; seen=set()
    for r in found:
        u=clean_url(r['url'])
        if u and u not in seen and safe_url(u): seen.add(u); unique.append({**r,'url':u})
        if len(unique)>=max_pages: break
    tasks=[(i,r['url'],r.get('title',''),r.get('query',''),max_bytes) for i,r in enumerate(unique)]; pages=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5,thread_name_prefix='interceptor-fetch') as ex:
        for f in concurrent.futures.as_completed([ex.submit(fetch_page,t) for t in tasks]): pages.append(f.result())
    pages.sort(key=lambda x:x['idx']); rawdir=pathlib.Path(a.raw_dir); rawdir.mkdir(parents=True,exist_ok=True)
    sources=[]; evidence=[]; evseen=set(); raw_chars=compressed_chars=ok=0
    for p in pages:
        handle=f's{len(sources)}'
        if p.get('text'):
            ok+=1; raw_chars+=len(p['text']); (rawdir/f'{handle}.txt').write_text(p['text'],encoding='utf-8',errors='replace'); ss=snippets(p['text'],p['query'],snip); compressed_chars+=len('\n'.join(ss))
            sources.append({'h':handle,'url':p['url'],'title':p.get('title','')[:240],'query':p['query'],'status':p.get('status'),'raw_chars':len(p['text']),'fetch_ms':p['ms']})
            for s in ss:
                k=hashlib.sha256(re.sub(r'\W+','',s.lower()).encode()).hexdigest()
                if k not in evseen: evseen.add(k); evidence.append({'s':handle,'text':s})
        else: sources.append({'h':handle,'url':p['url'],'title':p.get('title','')[:240],'query':p['query'],'error':p.get('error'),'fetch_ms':p['ms']})
    result={'schema':'carrier-web-v6/0.1','request_id':rid,'generated_at':time.time(),'metrics':{'queries':len(queries),'search_hits':len(found),'unique_urls':len(unique),'pages_ok':ok,'pages_failed':len(pages)-ok,'raw_chars':raw_chars,'evidence_chars':compressed_chars,'evidence_items':len(evidence),'elapsed_ms':round((time.time()-started)*1000,1),'workers':5},'search_errors':search_errors[:20],'sources':sources,'evidence':evidence,'note':'Raw page bodies stayed runner-side. Only compact evidence and provenance handles are committed.'}
    pathlib.Path(a.out).parent.mkdir(parents=True,exist_ok=True); pathlib.Path(a.out).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(result['metrics'],ensure_ascii=False))
if __name__=='__main__': main()
