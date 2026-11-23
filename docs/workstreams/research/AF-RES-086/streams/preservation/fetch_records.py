"""Bounded public GET receipts for AF-RES-086/Q7; no authentication, no retries."""
import concurrent.futures, datetime, hashlib, json, pathlib, sys, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent

def fetch(spec):
    sid, url = spec['id'], spec['url']
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = dict(id=sid, request_url=url, requested_utc=start, method='GET', observer='AF-RES-086 preservation worker')
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'AF-RES-086-public-research/1.0','Accept':'application/json,text/html,*/*'})
        try:
            response = urllib.request.urlopen(req, timeout=35)
        except urllib.error.HTTPError as e:
            response=e
        with response as r:
            body=r.read(2000001)
            result.update(http_status=r.status,final_url=r.url,headers={k:v for k,v in r.headers.items() if k.lower() in ['content-type','content-length','last-modified','etag','date','location']},response_bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),body_complete=len(body)<=2000000)
            ct=r.headers.get('Content-Type','')
            if len(body)<=2000000:
                suffix='json' if 'json' in ct or body.startswith((b'{',b'[')) else 'html'
                p=ROOT/'evidence'/f'{sid}.{suffix}'
                p.write_bytes(body)
                result['body_path']=p.relative_to(ROOT).as_posix()
            else:
                result['error']='response exceeds bounded read; body not retained'
    except Exception as e:
        result.update(error=type(e).__name__+': '+str(e),response_bytes=0)
    result['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (ROOT/'evidence'/f'{sid}.receipt.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result

if __name__=='__main__':
    specs=json.loads(sys.argv[1])
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for r in pool.map(fetch,specs): print(json.dumps(r,ensure_ascii=False),flush=True)
