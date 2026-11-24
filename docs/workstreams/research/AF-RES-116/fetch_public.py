"""Bounded public-source capture with observed transport receipts."""
from pathlib import Path
from datetime import datetime, timezone
import urllib.request, urllib.error, hashlib, json, time
BASE=Path(__file__).resolve().parent
def now():return datetime.now(timezone.utc).isoformat()
def fetch(url,relative_path,*,limit=25000000):
    p=BASE/relative_path
    p.parent.mkdir(parents=True,exist_ok=True)
    start=now(); tic=time.monotonic()
    receipt={'original_url':url,'started_utc':start,'output':relative_path,'status':None}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-116-public-research','Accept':'*/*'})
        with urllib.request.urlopen(req,timeout=45) as r:
            raw=r.read(limit+1)
            if len(raw)>limit:raise ValueError('bounded source exceeds limit')
            receipt.update(arrived_url=r.url,status=r.status,content_type=r.headers.get('Content-Type'),last_modified=r.headers.get('Last-Modified'),etag=r.headers.get('ETag'),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        p.write_bytes(raw)
    except Exception as e:
        receipt.update(error=type(e).__name__+': '+str(e),arrived_url=getattr(e,'url',None),status=getattr(e,'code',None))
        raw=None
    receipt.update(finished_utc=now(),wall_seconds=round(time.monotonic()-tic,6))
    p.with_name(p.name+'.receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    return raw,receipt
