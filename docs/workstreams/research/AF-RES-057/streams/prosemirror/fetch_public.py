from pathlib import Path
from datetime import datetime,timezone
import urllib.request,json,hashlib
ROOT=Path(__file__).resolve().parent
CACHE=ROOT.parents[1]/'.cache'/'prosemirror'
CACHE.mkdir(parents=True,exist_ok=True)
def fetch(url,key):
    start=datetime.now(timezone.utc).isoformat()
    req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-057-public-research'})
    try:
        with urllib.request.urlopen(req,timeout=45) as r:
            data=r.read();status=r.status;ctype=r.headers.get('Content-Type')
        (CACHE/(key+'.raw')).write_bytes(data)
        receipt={'url':url,'key':key,'started_UTC':start,'finished_UTC':datetime.now(timezone.utc).isoformat(),'status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'content_type':ctype,'model_displayed':False}
    except Exception as e:
        receipt={'url':url,'key':key,'started_UTC':start,'finished_UTC':datetime.now(timezone.utc).isoformat(),'error':str(e),'model_displayed':False}
        with (ROOT/'fetch-log.jsonl').open('a') as f:f.write(json.dumps(receipt)+'\n')
        raise
    with (ROOT/'fetch-log.jsonl').open('a') as f:f.write(json.dumps(receipt)+'\n')
    return data
def jfetch(url,key):return json.loads(fetch(url,key))
