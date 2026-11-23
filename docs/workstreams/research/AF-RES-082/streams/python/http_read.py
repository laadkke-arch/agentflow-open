import urllib.request,urllib.error,json,datetime,hashlib,pathlib
D=pathlib.Path(__file__).resolve().parent

def fetch(url,key,parse_json=False):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-082-public-research','Accept':'application/vnd.github+json' if 'api.github.com' in url else '*/*'})
  with urllib.request.urlopen(req,timeout=45) as r:
   b=r.read(); txt=b.decode('utf-8'); status=r.status; final=r.geturl(); headers={k:v for k,v in r.headers.items() if k.lower() in ['etag','last-modified','content-type','link','date']}
  record={'key':key,'url':url,'final_url':final,'opened_at_utc':t,'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'http_status':status,'sha256':hashlib.sha256(b).hexdigest(),'byte_length':len(b),'headers':headers,'result':'opened'}
  with (D/'http-receipts.jsonl').open('a') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
  return json.loads(txt) if parse_json else txt,record
 except Exception as e:
  record={'key':key,'url':url,'opened_at_utc':t,'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'access_failed','error':str(e),'http_status':getattr(e,'code',None),'headers':dict(getattr(e,'headers',{}) or {})}
  with (D/'attempts.jsonl').open('a') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
  return None,record
