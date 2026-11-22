"""Read public followup/history originals and preserve request/hash receipts.

Usage: python fetch.py requests.json ; raw bodies remain in ignored cache/.
"""
import concurrent.futures
import datetime
import hashlib
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent

def fetch(item):
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tick = time.monotonic()
    out = {'request_id':item['id'],'source_id':item.get('source_id'),
           'request':{'method':'GET','url':item['url'],'timeout_seconds':30},
           'started_utc':started,'cost_phase':'post-primary-seal followup/history',
           'changes_frozen_discovery':False}
    try:
        request=urllib.request.Request(item['url'],headers={'User-Agent':'AF-RES-025 research'})
        with urllib.request.urlopen(request,timeout=30) as response:
            body=response.read()
            out.update(status_code=response.status,final_url=response.url,
                       content_type=response.headers.get('Content-Type'),
                       bytes=len(body),body_sha256=hashlib.sha256(body).hexdigest(),
                       success=response.status==200)
        target=ROOT/'cache'/(item['id']+'.raw')
        target.write_bytes(body)
        out['cache_path']='cache/'+target.name
    except Exception as error:
        out.update(success=False,error=repr(error))
    out.update(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               wall_ms=round((time.monotonic()-tick)*1000))
    (ROOT/'receipts'/(item['id']+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    return out

if __name__=='__main__':
    items=json.loads(pathlib.Path(sys.argv[1]).read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for row in executor.map(fetch,items):
            print(json.dumps(row,ensure_ascii=False),flush=True)
