from pathlib import Path
import urllib.request,datetime,hashlib,json
BASE=Path(__file__).resolve().parents[2]
def read(key,url):
 c=BASE/'.cache/crossdomain';c.mkdir(parents=True,exist_ok=True)
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 rec={'source_id':key,'url':url,'opened_utc':start}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AF-RES-105 public source comparison'}),timeout=40) as r:
   b=r.read();rec.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
  f=c/(key+'.txt');f.write_bytes(b);rec.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),cache=str(f.relative_to(BASE)))
 except Exception as e:
  rec.update(error_type=type(e).__name__,error=str(e));b=None
 rec['ended_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (BASE/'evidence/crossdomain/acquisition.jsonl').open('a') as f:f.write(json.dumps(rec,ensure_ascii=False)+'\n')
 return b,rec
