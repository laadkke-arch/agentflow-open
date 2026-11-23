from pathlib import Path
import json,urllib.request,datetime,hashlib,concurrent.futures,sys
sys.path.insert(0,str(Path(__file__).parent))
from render_windows import window
P=Path(__file__).parent
JOBS=[
 ('API14',['LD-001','LD-009','LD-011','LD-013'],'http://www.w3.org/TR/2014/REC-json-ld-api-20140116/','external-standard','JSON-LD 1.0 API Recommendation; not supplier support'),
 ('NODESTREAM',['LD-002','LD-003'],'https://nodejs.org/api/stream.html#stream_class_stream_transform','external-runtime','Node stream API; inherited stream interface, not own JSON-LD behavior'),
 ('API11',['LD-007'],'https://www.w3.org/TR/json-ld11-api/','external-standard','JSON-LD 1.1 API Recommendation'),
 ('API11REMOTE',['LD-010'],'https://www.w3.org/TR/json-ld11-api/#remote-document-and-context-retrieval','external-standard','First actual API section link; earlier tests/feature status links not API docs'),
 ('DOTNETAPI',['LD-012'],'https://dotnetrdf.org/docs/latest/api/','provider-api-unbound-version','latest API documentation; same-version binding must be checked'),
 ('APICURRENT',['LD-018'],'http://www.w3.org/TR/json-ld-api/','external-standard','JSON-LD API link from current pinned README'),
 ('SOPHIAAPI',['LD-020'],'https://docs.rs/sophia/','provider-api','First API documentation link; sophia_api earlier is another crate listing, not API document')
]
def f(job):
 id,rows,url,role,reason=job;utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
 out={'id':id,'catalog_ids':rows,'requested_url':url,'role':role,'selection_reason':reason,'acquired_utc':utc}
 try:
  req=urllib.request.Request(url.split('#')[0],headers={'User-Agent':'AF-RES-060-public-research'})
  with urllib.request.urlopen(req,timeout=25) as r:b=r.read();out.update(status=r.status,final_url=r.url,length=len(b),sha256=hashlib.sha256(b).hexdigest())
  path=P/'raw'/f'{id}.html';path.write_bytes(b)
  w=window(b.decode('utf-8'),'.html',url.split('#')[1] if '#' in url else None)
  out.update({k:v for k,v in w.items() if k!='text'});out['raw_file']=str(path);out['window_file']='windows/'+id+'.txt';out['window_sha256']=hashlib.sha256(w['text'].encode()).hexdigest()
  (P/out['window_file']).write_text(w['text']+'\n');out['fetch_status']='success'
 except Exception as e:out.update(fetch_status='failed',error=type(e).__name__+': '+str(e),rendered_words=0)
 print(json.dumps({k:out.get(k) for k in ['id','fetch_status','heading','rendered_words','error']}),flush=True)
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:res=list(ex.map(f,JOBS))
(P/'followups.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')

