import urllib.request,json,pathlib,datetime,hashlib,concurrent.futures
from html.parser import HTMLParser
P=pathlib.Path(__file__).parent
selected_ids=[79692729,79701174,79703916,79714790]
rows=json.loads(P.joinpath('r0-metadata.json').read_text())
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(x):
 guid=x['earliest_body_revision']['revision_guid'];url='https://stackoverflow.com/revisions/'+guid+'/view-source';start=now()
 try:
  r=urllib.request.urlopen(url,timeout=45);raw=r.read();txt=raw.decode();out={'question_id':x['question_id'],'url':url,'started_utc':start,'finished_utc':now(),'status':r.status,'sha256':hashlib.sha256(raw).hexdigest(),'response_bytes':len(raw)}
  P.joinpath('_cache',str(x['question_id'])+'-view-source.html').write_text(txt)
  class Parser(HTMLParser):
   def __init__(self):super().__init__();self.data=[];self.inpre=False
   def handle_starttag(self,t,a):
    if t=='pre':self.inpre=True
   def handle_endtag(self,t):
    if t=='pre':self.inpre=False
   def handle_data(self,d):
    if self.inpre:self.data.append(d)
  parser=Parser();parser.feed(txt);body=''.join(parser.data)
  if body:
   P.joinpath('_cache',str(x['question_id'])+'.md').write_text(body);out.update(source_chars=len(body),source_bytes=len(body.encode()),source_sha256=hashlib.sha256(body.encode()).hexdigest())
  return out
 except Exception as e:return {'question_id':x['question_id'],'url':url,'started_utc':start,'finished_utc':now(),'error':repr(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:res=list(ex.map(read,[x for x in rows if x['question_id'] in selected_ids]))
P.joinpath('view-source-receipts.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
