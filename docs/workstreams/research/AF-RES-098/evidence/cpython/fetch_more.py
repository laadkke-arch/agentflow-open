"""Download named primary evidence after the prediction seal; never run it."""
import concurrent.futures,datetime,hashlib,json
from pathlib import Path
from urllib.request import build_opener,HTTPRedirectHandler
P=Path('/tmp/af098-cpython');OUT=Path(__file__).resolve().parent
TAGS={'3.12.0':'0fb18b02c8ad56299d6a2910be0bab8ad601ef24','3.12.1':'2305ca51448552542b2414186252123a8dc87db7','3.11.0':'deaf509e8fc6e0363bd6f26d52ad42f976ec42f2'}
URLS=[]
for v,sha in TAGS.items():
 for path in ['Doc/howto/logging_flow.png','Doc/library/hashlib-blake2-tree.png']+(['Doc/howto/logging.rst','Doc/library/hashlib.rst','Doc/Makefile'] if v!='3.11.0' else []):
  URLS.append((v+'-'+path.replace('/','_'),'https://raw.githubusercontent.com/python/cpython/'+sha+'/'+path))
URLS += [('sphinx45-html.py','https://raw.githubusercontent.com/sphinx-doc/sphinx/v4.5.0/sphinx/builders/html/__init__.py'),('docsbuild-old-commits.json','https://api.github.com/repos/python/docsbuild-scripts/commits?until=2023-12-07T20:47:00Z&per_page=1'),('logging-history.json','https://api.github.com/repos/python/cpython/commits?path=Doc/howto/logging_flow.png&sha=v3.12.1&per_page=20'),('hashlib-history.json','https://api.github.com/repos/python/cpython/commits?path=Doc/library/hashlib-blake2-tree.png&sha=v3.12.1&per_page=20')]
def fetch(t):
 key,url=t;record={'key':key,'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'redirects':[]}
 class R(HTTPRedirectHandler):
  def redirect_request(self,req,fp,code,msg,headers,newurl):
   record['redirects'].append({'from':req.full_url,'status':code,'to':newurl});return super().redirect_request(req,fp,code,msg,headers,newurl)
 try:
  with build_opener(R()).open(url,timeout=40) as r:b=r.read();(P/key).write_bytes(b);record.update({'status':r.status,'final_url':r.url,'content_type':r.headers.get('Content-Type'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 except Exception as e:record.update({'error':repr(e),'status':'failed'})
 return record
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:out=list(ex.map(fetch,URLS))
 (P/'more-receipts.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
