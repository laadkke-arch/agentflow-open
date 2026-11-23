import urllib.request,urllib.error,json,datetime,hashlib,pathlib,sys
D=pathlib.Path(__file__).resolve().parent

def fetch(url,key=None):
 key=key or hashlib.sha256(url.encode()).hexdigest()[:16]
 p=D/'raw'/f'{key}.json'
 if p.exists(): return json.load(open(p))
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-082-public-research','Accept':'application/vnd.github+json'})
  with urllib.request.urlopen(req,timeout=40) as r:
   b=r.read(); data=b.decode('utf-8'); meta={'url':url,'final_url':r.geturl(),'opened_at_utc':now,'status':r.status,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'rate_remaining':r.headers.get('X-RateLimit-Remaining'),'data':data}
 except Exception as e: meta={'url':url,'opened_at_utc':now,'status':'failed','error':str(e)}
 p.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
 return meta
if __name__=='__main__':
 for repo in sys.argv[1:]:
  v=fetch(f'https://api.github.com/repos/r-lib/{repo}/releases?per_page=100',f'{repo}-releases')
  if v['status']==200:
   rels=json.loads(v['data']); print(repo,v['rate_remaining'],[(x['tag_name'],x['published_at'],x['prerelease'],x['draft']) for x in rels])
  else: print(repo,v)
