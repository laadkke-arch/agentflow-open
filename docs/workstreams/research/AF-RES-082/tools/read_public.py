"""Read an explicitly supplied public URL; preserve receipt and a local text cache.
No credentials, mutations, retries, or source-count credit. A researcher must read
and annotate a document before adding it to sources.jsonl.
"""
import argparse,datetime,hashlib,json,pathlib,urllib.request,urllib.error
from html.parser import HTMLParser
D=pathlib.Path(__file__).resolve().parents[1]
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.chunks=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style','noscript'):self.skip+=1
  if t in ('p','div','section','h1','h2','h3','h4','li','tr','pre','br'):self.chunks.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style','noscript'):self.skip=max(0,self.skip-1)
  if t in ('p','div','section','h1','h2','h3','h4','li','tr','pre'):self.chunks.append('\n')
 def handle_data(self,s):
  if not self.skip:self.chunks.append(s)
class Redirect(urllib.request.HTTPRedirectHandler):
 def __init__(self): self.hops=[]
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  self.hops.append({'from':req.full_url,'status':code,'to':newurl})
  return super().redirect_request(req,fp,code,msg,headers,newurl)
def read(url,key,phase):
 cache=D/'evidence'/'cache';cache.mkdir(exist_ok=True)
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();red=Redirect();op=urllib.request.build_opener(red)
 receipt={'key':key,'url':url,'opened_at_utc':start,'phase':phase,'top_level_requests':1,'cache_reuse':False}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-082 documentation research','Accept':'text/html,application/json,text/plain;q=0.9,*/*;q=0.1'})
  try: response=op.open(req,timeout=45)
  except urllib.error.HTTPError as e: response=e
  with response as r:
   b=r.read();charset=r.headers.get_content_charset() or 'utf-8';s=b.decode(charset,errors='replace')
   receipt.update(http_status=r.status,final_url=r.geturl(),body_bytes=len(b),body_sha256=hashlib.sha256(b).hexdigest(),content_type=r.headers.get('Content-Type'),etag=r.headers.get('ETag'),last_modified=r.headers.get('Last-Modified'))
  if 'html' in receipt.get('content_type',''):
   parser=Text();parser.feed(s);s='\n'.join(x.strip() for x in ''.join(parser.chunks).splitlines() if x.strip())
  (cache/(key+'.txt')).write_text(s)
  receipt['cache_path']=(cache/(key+'.txt')).relative_to(D).as_posix()
 except Exception as e:receipt.update(error=type(e).__name__+': '+str(e))
 receipt.update(completed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),redirects=red.hops,http_requests_including_redirects=1+len(red.hops))
 with (D/'evidence'/'http-receipts.jsonl').open('a') as f:f.write(json.dumps(receipt,ensure_ascii=False)+'\n')
 print(json.dumps(receipt,ensure_ascii=False))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('key');p.add_argument('--phase',default='postbudget');a=p.parse_args();read(a.url,a.key,a.phase)
