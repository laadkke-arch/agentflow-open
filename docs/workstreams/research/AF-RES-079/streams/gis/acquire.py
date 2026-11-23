"""Read public primary sources; record current HTTP chains, never historical inference."""
import urllib.request,urllib.error,datetime,hashlib,json,concurrent.futures
from pathlib import Path
BASE=Path(__file__).parent
class TraceRedirect(urllib.request.HTTPRedirectHandler):
 def __init__(self): self.chain=[]
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  self.chain.append({'url':req.full_url,'status':code,'location':headers.get('Location'),'next_url':newurl})
  return super().redirect_request(req,fp,code,msg,headers,newurl)
def get(item):
 key,url=item;tr=TraceRedirect();o=urllib.request.build_opener(tr);now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=o.open(urllib.request.Request(url,headers={'User-Agent':'AF-RES-079-research'}),timeout=35);b=r.read();s=b.decode('utf-8','replace');(BASE/'cache'/f'{key}.txt').write_text(s)
  return {'key':key,'requested_url':url,'checked_utc':now,'status':r.status,'arrived_url':r.url,'redirect_chain':tr.chain,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'cache_file':f'cache/{key}.txt','access':'read_success'}
 except urllib.error.HTTPError as e:return {'key':key,'requested_url':url,'checked_utc':now,'status':e.code,'arrived_url':e.url,'redirect_chain':tr.chain,'access':'http_error','error':str(e)}
 except Exception as e:return {'key':key,'requested_url':url,'checked_utc':now,'status':None,'arrived_url':None,'redirect_chain':tr.chain,'access':'network_error','error':str(e)}
if __name__=='__main__':
 import sys
 items=json.loads(Path(sys.argv[1]).read_text());rs=list(concurrent.futures.ThreadPoolExecutor(7).map(get,items))
 with (BASE/'http-acquisition.jsonl').open('a') as f:
  for x in rs:f.write(json.dumps(x,ensure_ascii=False)+'\n')
 print(json.dumps(rs,ensure_ascii=False,indent=2))
