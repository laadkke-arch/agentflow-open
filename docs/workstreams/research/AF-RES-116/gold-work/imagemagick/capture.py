"""Bounded, public-only snapshots in this gold reader's owned directory."""
from pathlib import Path
from datetime import datetime, timezone
import urllib.request, urllib.error, urllib.parse, hashlib, json, time
BASE = Path(__file__).resolve().parent
def now(): return datetime.now(timezone.utc).isoformat()
def redacted_url(url):
    if not url: return url, None
    p = urllib.parse.urlsplit(url)
    keys = [k for k,v in urllib.parse.parse_qsl(p.query, keep_blank_values=True)]
    if p.query and (any(k.lower().startswith(('x-amz-', 'x-goog-')) or k.lower() in {'sig','signature','token','jwt','se','sp','sv','skoid','sktid','skt','ske','sks','skv'} for k in keys)):
        return urllib.parse.urlunsplit((p.scheme,p.netloc,p.path,'','')), {'query_redacted': True, 'removed_query_keys': keys, 'qualification': 'Observed arrival origin/path only; signing query removed. This is NOT an observed canonical URL.'}
    return url, None
def fetch(url, name, limit=25000000):
    path=BASE/name; path.parent.mkdir(parents=True,exist_ok=True)
    assert BASE in path.resolve().parents
    receipt={'original_url':url,'started_utc':now(),'output':name,'status':None,'download_is_direct_read':False}
    tic=time.monotonic(); raw=None
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-116-independent-gold-reader','Accept':'*/*'})
        with urllib.request.urlopen(req,timeout=40) as r:
            arrived,redaction=redacted_url(r.url)
            receipt.update(arrived_url=arrived,arrived_url_redaction=redaction,status=r.status,content_type=r.headers.get('Content-Type'),last_modified=r.headers.get('Last-Modified'),etag=r.headers.get('ETag'),declared_bytes=r.headers.get('Content-Length'))
            if r.headers.get('Content-Length') and int(r.headers['Content-Length'])>limit: raise ValueError('declared size exceeds bounded fetch limit '+str(limit))
            raw=r.read(limit+1)
            if len(raw)>limit: raw=None; raise ValueError('body exceeds bounded fetch limit '+str(limit))
        path.write_bytes(raw)
        receipt.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    except Exception as e:
        if isinstance(e,urllib.error.HTTPError): receipt.update(status=e.code)
        receipt.update(error=type(e).__name__+': '+str(e))
    receipt.update(finished_utc=now(),wall_seconds=round(time.monotonic()-tic,6))
    path.with_name(path.name+'.receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    return receipt
def record_read(source,sections,utc=None,**kw):
    row={'source':source,'read_utc':utc or now(),'read_sections':sections,**kw}
    with (BASE/'read-events.jsonl').open('a') as f: f.write(json.dumps(row,ensure_ascii=False)+'\n')
    return row
if __name__=='__main__':
    import sys
    print(json.dumps(fetch(sys.argv[1],sys.argv[2]),ensure_ascii=False))
