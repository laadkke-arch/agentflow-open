"""Bounded, unauthenticated public HTTP evidence collection; no success inference."""
from pathlib import Path
import argparse, concurrent.futures, datetime, hashlib, json, urllib.request, urllib.error

def capture(item, out):
    key, url = item['id'], item['url']
    begun = datetime.datetime.now(datetime.timezone.utc).isoformat()
    req = urllib.request.Request(url, headers={'User-Agent':'AF-RES-086-public-evidence/1.0', 'Accept':'*/*'})
    row = dict(item, requested_at_utc=begun, observer='researcher direct unauthenticated HTTP GET')
    try:
        try:
            response = urllib.request.urlopen(req, timeout=35)
        except urllib.error.HTTPError as e:
            response = e
        with response:
            data = response.read(4000001)
            row.update(status=response.code, final_url=response.url,
                       headers={k:v for k,v in response.headers.items() if 'cookie' not in k.lower()}, bytes=len(data), truncated=len(data)>4000000,
                       response_sha256=hashlib.sha256(data).hexdigest())
            filename=key+('.json' if 'json' in response.headers.get('content-type','') else '.txt')
            (out/filename).write_bytes(data)
            row['body_file']=filename
    except Exception as e:
        row.update(status=None,error=type(e).__name__+': '+str(e),bytes=0)
    row['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (out/(key+'.receipt.json')).write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
    return row

def main():
    p=argparse.ArgumentParser(); p.add_argument('inputs'); p.add_argument('output'); a=p.parse_args()
    items=json.loads(Path(a.inputs).read_text()); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows=list(pool.map(lambda x:capture(x,out),items))
    for r in rows:
        print(json.dumps({k:r.get(k) for k in ['id','url','status','bytes','final_url','response_sha256','error']},ensure_ascii=False))
    return 0

if __name__=='__main__': raise SystemExit(main())
