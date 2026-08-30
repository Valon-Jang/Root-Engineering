#!/usr/bin/env python3
import base64
from urllib.parse import parse_qs, unquote, urlparse
import collector

_original_clean_url = collector.clean_url

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

collector.clean_url = clean_url_v2
collector.main()
