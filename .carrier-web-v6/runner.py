#!/usr/bin/env python3
import base64, re
from collections import deque
from urllib.parse import parse_qs, quote_plus, unquote, urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import collector

# Compatibility shim: conservative compressor v0.2 no longer needs WORD itself,
# but the discovery layer still uses it for sitemap/query scoring.
if not hasattr(collector, 'WORD'):
    collector.WORD = re.compile(r'[A-Za-z0-9가-힣_+-]{2,}')

SEARCH_HOSTS = {'www.google.com','google.com','www.bing.com','bing.com','search.brave.com','www.mojeek.com','mojeek.com'}


def clean_url_v3(u):
    if not u:
        return None
    p = urlparse(u)
    if 'duckduckgo.com/l/' in u:
        q = parse_qs(p.query).get('uddg')
        if q:
            u = unquote(q[0])
    elif p.hostname and p.hostname.endswith('bing.com') and p.path.startswith('/ck/a'):
        enc = parse_qs(p.query).get('u')
        if enc:
            v = enc[0]
            if v.startswith('a1'):
                v = v[2:]
            try:
                v += '=' * ((4 - len(v) % 4) % 4)
                decoded = base64.urlsafe_b64decode(v.encode()).decode('utf-8', 'strict')
                if decoded.startswith(('http://', 'https://')):
                    u = decoded
            except Exception:
                pass
    elif p.hostname and p.hostname.endswith('google.com') and p.path == '/url':
        q = parse_qs(p.query).get('q')
        if q:
            u = q[0]
    return u.split('#')[0]


def site_domains(q):
    return [x.lower().rstrip('.') for x in re.findall(r'(?i)\bsite:([A-Za-z0-9._-]+)', q)]


def domain_ok(u, domains):
    if not domains:
        return True
    host = (urlparse(u).hostname or '').lower()
    return any(host == d or host.endswith('.' + d) for d in domains)


def generic_search(url, params, q, n, session, engine):
    r = session.get(url, params=params, timeout=15, headers={'User-Agent': collector.UA})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    out, seen = [], set()
    for a in soup.find_all('a', href=True):
        href = a.get('href') or ''
        if href.startswith('/'):
            href = urljoin(r.url, href)
        target = clean_url_v3(href)
        if not target or not target.startswith(('http://','https://')):
            continue
        host = (urlparse(target).hostname or '').lower()
        if host in SEARCH_HOSTS or host.endswith('.googleusercontent.com'):
            continue
        if target in seen or not collector.safe_url(target):
            continue
        title = ' '.join(a.stripped_strings).strip()
        if len(title) < 2:
            continue
        seen.add(target)
        out.append({'url': target, 'title': title[:240], 'engine': engine})
        if len(out) >= n:
            break
    return out


def search_google(q,n,s):
    return generic_search('https://www.google.com/search', {'q':q,'num':max(n+6,12),'hl':'en','filter':'0'}, q, n, s, 'google')

def search_brave(q,n,s):
    return generic_search('https://search.brave.com/search', {'q':q,'source':'web'}, q, n, s, 'brave')

def search_mojeek(q,n,s):
    return generic_search('https://www.mojeek.com/search', {'q':q}, q, n, s, 'mojeek')


def sitemap_candidates(domain, q, n, session):
    terms = {w.lower() for w in collector.WORD.findall(re.sub(r'(?i)\bsite:[A-Za-z0-9._-]+','',q)) if len(w)>2}
    todo = deque([f'https://{domain}/sitemap.xml', f'https://{domain}/sitemap_index.xml'])
    try:
        robots = session.get(f'https://{domain}/robots.txt',timeout=8,headers={'User-Agent':collector.UA})
        if robots.ok:
            for line in robots.text.splitlines():
                if line.lower().startswith('sitemap:'):
                    todo.append(line.split(':',1)[1].strip())
    except Exception:
        pass
    seen_maps, urls = set(), []
    while todo and len(seen_maps) < 12 and len(urls) < 6000:
        sm = todo.popleft()
        if sm in seen_maps or not collector.safe_url(sm):
            continue
        seen_maps.add(sm)
        try:
            r=session.get(sm,timeout=12,headers={'User-Agent':collector.UA})
            if not r.ok or len(r.content)>8_000_000:
                continue
            soup=BeautifulSoup(r.content,'xml')
            locs=[x.get_text(strip=True) for x in soup.find_all('loc')]
            if soup.find('sitemapindex'):
                for x in locs[:50]:
                    if domain_ok(x,[domain]): todo.append(x)
            else:
                urls.extend(x for x in locs if domain_ok(x,[domain]))
        except Exception:
            continue
    scored=[]
    for u in urls:
        low=unquote(urlparse(u).path).lower().replace('-',' ').replace('_',' ')
        score=sum(3 for t in terms if t in low)
        if score:
            scored.append((score,u))
    scored.sort(key=lambda x:(x[0],-len(x[1])),reverse=True)
    return [{'url':u,'title':'sitemap candidate','engine':'sitemap'} for _,u in scored[:n]]


def do_search_v3(q, n):
    domains = site_domains(q)
    session = requests.Session()
    errors, out, seen = [], [], set()

    if domains:
        for d in domains:
            for row in sitemap_candidates(d,q,max(n*2,10),session):
                u=clean_url_v3(row['url'])
                if u and u not in seen and domain_ok(u,domains):
                    seen.add(u); out.append(row)
                    if len(out)>=n:
                        return q,out,errors

    variants=[q]
    if domains:
        plain=re.sub(r'(?i)\bsite:[A-Za-z0-9._-]+\s*','',q).strip()
        if plain: variants.append(plain)
    funcs=(search_google,search_brave,search_mojeek,collector.search_ddg,collector.search_bing)
    for variant in variants:
        for fn in funcs:
            try:
                rows=fn(variant,max(n*3,12),session)
            except Exception as e:
                errors.append(f'{fn.__name__}:{type(e).__name__}:{e}')
                continue
            for row in rows:
                u=clean_url_v3(row.get('url'))
                if not u or u in seen or not collector.safe_url(u) or not domain_ok(u,domains):
                    continue
                seen.add(u); out.append({**row,'url':u})
                if len(out)>=n:
                    return q,out,errors
    return q,out,errors

collector.clean_url = clean_url_v3
collector.do_search = do_search_v3
collector.main()
