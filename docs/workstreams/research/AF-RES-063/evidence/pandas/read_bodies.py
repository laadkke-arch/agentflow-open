import json,pathlib,concurrent.futures,urllib.request,datetime,hashlib
P=pathlib.Path(__file__).parent
frame=json.loads((P/'frame-seal.json').read_text())
def one(x):
 u=f"https://api.github.com/repos/pandas-dev/pandas/issues/{x['number']}"
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'Accept':'application/vnd.github+json','User-Agent':'AF-RES-063-public-research'}),timeout=45);b=r.read();j=json.loads(b)
  return {'number':x['number'],'title':j['title'],'created_at':j['created_at'],'updated_at':j['updated_at'],'author':j['user']['login'],'author_association':j.get('author_association'),'body':j['body'],'comments':j['comments'],'html_url':j['html_url'],'url':u,'opened_utc':start,'status':r.status,'response_bytes':len(b),'response_sha256':hashlib.sha256(b).hexdigest(),'body_sha256':hashlib.sha256((j['body'] or '').encode()).hexdigest()}
 except Exception as e:return {'number':x['number'],'url':u,'opened_utc':start,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: rows=list(ex.map(one,frame['first30']))
(P/'body-snapshots.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
(P/'body-acquisition.json').write_text(json.dumps([{k:v for k,v in x.items() if k!='body'} for x in rows],ensure_ascii=False,indent=2))
print([(x['number'],len(x.get('body') or ''),x.get('error')) for x in rows])
