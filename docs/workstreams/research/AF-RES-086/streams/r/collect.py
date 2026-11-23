import concurrent.futures, datetime, hashlib, json, pathlib, sys, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent
def get(item):
    sid, url = item
    at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-086-public-evidence/1.0','Accept':'application/vnd.github+json' if 'api.github.com' in url else '*/*'})
    try:
        r=urllib.request.urlopen(req,timeout=40)
    except urllib.error.HTTPError as e:
        r=e
    except Exception as e:
        out={'id':sid,'url':url,'read_utc':at,'status':None,'error':str(e),'bytes':0}
        (ROOT/'evidence'/f'{sid}.receipt.json').write_text(json.dumps(out,indent=2)+'\n')
        return out
    body=r.read(); headers=dict(r.headers.items())
    out={'id':sid,'url':url,'read_utc':at,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':r.code,'final_url':r.geturl(),'headers':headers,'bytes':len(body),'direct_sha256':hashlib.sha256(body).hexdigest(),'publisher_hash':None}
    (ROOT/'.workbench'/f'{sid}.body').write_bytes(body)
    (ROOT/'evidence'/f'{sid}.receipt.json').write_text(json.dumps(out,indent=2)+'\n')
    return out

if __name__=='__main__':
    items=json.loads(pathlib.Path(sys.argv[1]).read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for out in pool.map(get,items):
            print(json.dumps(out,ensure_ascii=False),flush=True)
