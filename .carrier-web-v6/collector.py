#!/usr/bin/env python3
import argparse, concurrent.futures, ipaddress, json, math, pathlib, re, socket, time
from urllib.parse import quote_plus, unquote, urlparse, parse_qs
import requests
from bs4 import BeautifulSoup

UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36 CarrierWebV6/0.2'

# Conservative prose-only deletions. These are framing/filler expressions, not evidence selection rules.
FILLERS=[
 r'(?i)\b(?:it is important to note that|it should be noted that|in other words|generally speaking|as a matter of fact)\b[,;:]?\s*',
 r'(?i)\b(?:currently,?\s+based on the information available,?|taking all of the above into consideration,?)\s*',
 r'(?:현재\s+확인된\s+바에\s+따르면|종합적으로\s+고려했을\s+때|다시\s+말해서|말씀드리자면)[,，]?\s*',
]
PROTECTED_MARKERS=re.compile(r'(?i)\b(?:not|no|never|only|except|unless|until|before|after|if|when|hold|release|must|shall|may|might|cannot|can\'t|without|scope|authority|approved?|denied?|cancel(?:led)?|supersed(?:e|ed)|deprecated|warning|error|failed?)\b|(?:아니|않|못|없|만|제외|예외|조건|경우|이후|이전|까지|보류|해제|승인|취소|대체|범위|권한|실패)')
NUM_ID=re.compile(r'https?://\S+|\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}:\d{2}\b|\b\d+(?:\.\d+)?\s*(?:%|ms|s|sec|seconds?|minutes?|hours?|days?|MB|GB|KB|tokens?|USD|KRW|원|개|회)?\b|\b[A-Z][A-Z0-9_-]{2,}\b')


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
    """Remove non-content web chrome before the compression baseline is measured."""
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


def compact_line(line):
    """Delete only conservative filler while protecting decision-bearing spans."""
    orig=' '.join(line.split())
    if not orig: return orig
    protected=NUM_ID.findall(orig); marker_count=len(PROTECTED_MARKERS.findall(orig)); x=orig
    for pat in FILLERS: x=re.sub(pat,'',x)
    x=re.sub(r'\s+',' ',x).strip(' ,;')
    if not x: return orig
    if any(p not in x for p in protected): return orig
    if len(PROTECTED_MARKERS.findall(x)) < marker_count: return orig
    return x


def conservative_compress(text,min_retention=0.70):
    """Never remove more than (1-min_retention) of visible body text.

    No sentence ranking, summarization, relevance filtering, or semantic deletion is performed.
    If lexical trimming would cross the retention floor, changed lines are restored until the
    hard floor is satisfied.
    """
    if not text: return text,1.0
    min_retention=max(0.70,min(float(min_retention),1.0))
    raw_lines=text.splitlines()
    rows=[]
    for line in raw_lines:
        orig=' '.join(line.split())
        comp=compact_line(orig)
        rows.append([orig,comp,max(0,len(orig)-len(comp))])
    compressed='\n'.join(r[1] for r in rows)
    floor=math.ceil(len(text)*min_retention)
    if len(compressed) < floor:
        # Restore the most aggressively shortened lines first until >=70% is retained.
        changed=sorted((i for i,r in enumerate(rows) if r[2]>0), key=lambda i: rows[i][2], reverse=True)
        for i in changed:
            rows[i][1]=rows[i][0]
            compressed='\n'.join(r[1] for r in rows)
            if len(compressed) >= floor: break
    if len(compressed) < floor:
        compressed=text
    retention=len(compressed)/max(1,len(text))
    return compressed,retention


def chunk_text(text,max_chars=2600):
    """Chunk without dropping or reordering any compressed text."""
    if not text: return []
    out=[]; buf=''
    for line in text.splitlines():
        piece=line if not buf else '\n'+line
        if len(buf)+len(piece) <= max_chars:
            buf+=piece
            continue
        if buf: out.append(buf); buf=''
        while len(line)>max_chars:
            out.append(line[:max_chars]); line=line[max_chars:]
        buf=line
    if buf: out.append(buf)
    return out


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--request',required=True); ap.add_argument('--out',required=True); ap.add_argument('--raw-dir',required=True); a=ap.parse_args()
    started=time.time(); req=json.load(open(a.request,encoding='utf-8')); rid=req.get('request_id') or pathlib.Path(a.request).stem
    queries=[str(x).strip() for x in req.get('queries',[]) if str(x).strip()][:50]; seeds=[str(x).strip() for x in req.get('urls',[]) if str(x).strip()][:100]
    perq=max(1,min(int(req.get('max_results_per_query',5)),10)); max_pages=max(1,min(int(req.get('max_pages',40)),100)); max_bytes=max(100000,min(int(req.get('max_bytes_per_page',1500000)),3000000))
    min_retention=max(0.70,min(float(req.get('min_text_retention',0.70)),1.0))
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
    sources=[]; evidence=[]; raw_chars=compressed_chars=ok=0
    for p in pages:
        handle=f's{len(sources)}'
        if p.get('text'):
            ok+=1; raw=p['text']; raw_chars+=len(raw); (rawdir/f'{handle}.txt').write_text(raw,encoding='utf-8',errors='replace')
            compact,retention=conservative_compress(raw,min_retention=min_retention); compressed_chars+=len(compact)
            sources.append({'h':handle,'url':p['url'],'title':p.get('title','')[:240],'query':p['query'],'status':p.get('status'),'raw_chars':len(raw),'compressed_chars':len(compact),'retention':round(retention,4),'fetch_ms':p['ms']})
            for part,chunk in enumerate(chunk_text(compact)):
                evidence.append({'s':handle,'part':part,'text':chunk})
        else:
            sources.append({'h':handle,'url':p['url'],'title':p.get('title','')[:240],'query':p['query'],'error':p.get('error'),'fetch_ms':p['ms']})
    retention=(compressed_chars/max(1,raw_chars)) if raw_chars else 1.0
    result={
        'schema':'carrier-web-v6/0.2-conservative',
        'request_id':rid,
        'generated_at':time.time(),
        'compression_policy':{'mode':'filler-only','min_text_retention':min_retention,'max_text_reduction':round(1-min_retention,4),'semantic_selection':False,'summarization':False},
        'metrics':{
            'queries':len(queries),'search_hits':len(found),'unique_urls':len(unique),'pages_ok':ok,'pages_failed':len(pages)-ok,
            'raw_chars':raw_chars,'evidence_chars':compressed_chars,'text_retention':round(retention,4),'text_reduction_pct':round((1-retention)*100,2),
            'evidence_items':len(evidence),'elapsed_ms':round((time.time()-started)*1000,1),'workers':5,'search_error_count':len(search_errors)
        },
        'sources':sources,
        'evidence':evidence,
        'note':'Visible page body is preserved in order. Only conservative filler is removed; at least 70% of each page body is retained. No Top-N evidence selection or summarization.'
    }
    pathlib.Path(a.out).parent.mkdir(parents=True,exist_ok=True); pathlib.Path(a.out).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(result['metrics'],ensure_ascii=False))

if __name__=='__main__': main()
