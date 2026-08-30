#!/usr/bin/env python3
import base64, re
from urllib.parse import parse_qs, quote_plus, unquote, urlparse
import requests
from bs4 import BeautifulSoup
import collector


def clean_url_v2(u):
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
    return u.split('#')[0]


def search_google(q, n, session):
    r = session.get(
        'https://www.google.com/search',
        params={'q': q, 'num': max(n + 4, 10), 'hl': 'en', 'filter': '0'},
        timeout=15,
        headers={'User-Agent': collector.UA},
    )
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    out, seen = [], set()
    for a in soup.select('a'):
        href = a.get('href') or ''
        title = ' '.join(a.stripped_strings)
        target = None
        if href.startswith('/url?'):
            target = parse_qs(urlparse(href).query).get('q', [None])[0]
        elif href.startswith(('http://', 'https://')):
            target = href
        target = clean_url_v2(target)
        if not target:
            continue
        host = (urlparse(target).hostname or '').lower()
        if host.endswith('google.com') or host.endswith('googleusercontent.com'):
            continue
        if target not in seen and collector.safe_url(target):
            seen.add(target)
            out.append({'url': target, 'title': title[:240], 'engine': 'google'})
        if len(out) >= n:
            break
    return out


def site_domains(q):
    return [x.lower().rstrip('.') for x in re.findall(r'(?i)\bsite:([A-Za-z0-9._-]+)', q)]


def domain_ok(u, domains):
    if not domains:
        return True
    host = (urlparse(u).hostname or '').lower()
    return any(host == d or host.endswith('.' + d) for d in domains)


def do_search_v2(q, n):
    domains = site_domains(q)
    variants = [q]
    if domains:
        plain = re.sub(r'(?i)\bsite:[A-Za-z0-9._-]+\s*', '', q).strip()
        if plain and plain != q:
            variants.append(plain)
    session = requests.Session()
    errors, out, seen = [], [], set()
    for variant in variants:
        for fn in (search_google, collector.search_ddg, collector.search_bing):
            try:
                rows = fn(variant, max(n * 2, 8), session)
            except Exception as e:
                errors.append(f'{fn.__name__}:{type(e).__name__}:{e}')
                continue
            for row in rows:
                u = clean_url_v2(row.get('url'))
                if not u or u in seen or not collector.safe_url(u) or not domain_ok(u, domains):
                    continue
                seen.add(u)
                out.append({**row, 'url': u})
                if len(out) >= n:
                    return q, out, errors
    return q, out, errors


collector.clean_url = clean_url_v2
collector.do_search = do_search_v2
collector.main()
