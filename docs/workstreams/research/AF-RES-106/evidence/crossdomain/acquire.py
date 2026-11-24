#!/usr/bin/env python3
"""Public primary-source retrieval for Q7. Does not execute external content."""
import concurrent.futures,datetime,hashlib,json,pathlib,sys,urllib.request,urllib.error,urllib.parse
ROOT=pathlib.Path(__file__).parent
REQUESTS={
'IIIF-SPEC':('https://iiif.io/api/presentation/3.0/','iiif-presentation-3.html'),
'JATS-FIG':('https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/fig.html','jats-1.3-fig.html'),
'JATS-XREF':('https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/xref.html','jats-1.3-xref.html'),
'RIJKS-TUTORIAL':('https://data.rijksmuseum.nl/tutorials/iiif/','rijksmuseum-tutorial.html'),
'RIJKS-MANIFEST':('https://iiif.micr.io/PJEZO/manifest','rijksmuseum-manifest.json'),
'FITZ-MANIFEST':('https://miniatures-iiif.fitzmuseum.cam.ac.uk/AGOID.29376/manifest.json','fitzwilliam-manifest.json'),
'PLOS-XML':('https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0319031&type=manuscript','plos-spark.xml'),
'PLOS-HTML':('https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031','plos-spark.html'),
}
if (ROOT/'followup-requests.json').exists():
 REQUESTS.update(json.loads((ROOT/'followup-requests.json').read_text()))
def sanitize(u):
 p=urllib.parse.urlsplit(u)
 if 'X-Amz' in p.query:return urllib.parse.urlunsplit((p.scheme,p.netloc,p.path,'',''))
 return u
def get(sid):
 url,file=REQUESTS[sid];now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 rec={'source_id':sid,'requested_url':url,'requested_utc':now,'method':'stdlib urllib GET; no browser rendering'}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-106 public-source research'})
  with urllib.request.urlopen(req,timeout=30) as res:
   b=res.read();rec.update(http_status=res.status,final_url=sanitize(res.url),content_type=res.headers.get('Content-Type'),size_bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),file=file)
  (ROOT/file).write_bytes(b)
 except urllib.error.HTTPError as e:
  b=e.read();rec.update(http_status=e.code,error='HTTPError',error_body_preview=b[:400].decode(errors='replace'),response_headers={k:v for k,v in e.headers.items() if k.lower() in ['content-type','x-mitmproxy-blocked-reason','server']})
 except Exception as e:rec.update(error=type(e).__name__,error_message=str(e))
 rec['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 (ROOT/(sid.lower()+'-receipt.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
 return rec
if __name__=='__main__':
 ids=sys.argv[1:] or list(REQUESTS)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
  for r in ex.map(get,ids):print(json.dumps(r,ensure_ascii=False),flush=True)
