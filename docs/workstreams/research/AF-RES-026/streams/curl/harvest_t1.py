"""Read only selected official mail artifacts; persist metadata/hashes, not prose.

Invocation lists URLs/relative January filenames explicitly. Outputs mail body
for direct reading. Network cost and dates are recorded in t1-message-metadata.
"""
from pathlib import Path
import urllib.request, re, html, hashlib, datetime, json, sys, concurrent.futures, time

P=Path(__file__).resolve().parent
DEST=P/'t1-message-metadata.json'
BASE='https://curl.se/mail/archive-2022-01/'
urls=[x if x.startswith('https://') else BASE+x+'.html' for x in sys.argv[1:]]

def clean(s):
    s=re.sub(r'<br\s*/?>','\n',s,flags=re.I)
    return html.unescape(re.sub('<[^>]+>','',s)).strip()

def read(u):
    started=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic()
    try:
        raw=urllib.request.urlopen(u,timeout=30).read(); s=raw.decode()
        b=s.split('<!-- body="start" -->')[1].split('<!-- body="end" -->')[0]
        def field(k):
            m=re.search('<!-- '+k+r'="(.*?)" -->',s,re.S)
            return html.unescape(m.group(1)) if m else None
        meta={k:field(k) for k in ['id','name','subject','sent','isosent','received','isoreceived','charset']}
        meta.update({'url':u,'checked_utc':started,'elapsed_seconds':round(time.monotonic()-t,3),
                     'body_sha256':hashlib.sha256(b.encode()).hexdigest(),'html_sha256':hashlib.sha256(raw).hexdigest(),
                     'bytes_received':len(raw),'status':'read',
                     'reply_hrefs':re.findall(r'<dfn>Reply</dfn>: <a href="([^"]+)"',s),
                     'parent_hrefs':re.findall(r'<dfn>In reply to</dfn>: <a href="([^"]+)"',s)})
        body=clean(b)
        return meta,body
    except Exception as e:return {'url':u,'checked_utc':started,'status':'failed','error':str(e)},''

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: results=list(ex.map(read,urls))
old=json.loads(DEST.read_text()) if DEST.exists() else []
by={x['url']:x for x in old}
for meta,b in results:
    by[meta['url']]=meta
    print(json.dumps({k:meta.get(k) for k in ['url','id','name','isosent','isoreceived','status','reply_hrefs','parent_hrefs']},ensure_ascii=False))
    print('\n'.join(x.strip() for x in b.splitlines() if x.strip() and not x.strip().startswith('>')))
DEST.write_text(json.dumps(list(by.values()),ensure_ascii=False,indent=2)+'\n')
