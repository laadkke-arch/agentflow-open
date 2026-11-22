import csv,pathlib,urllib.request,urllib.parse,concurrent.futures,hashlib,json,datetime,re
from lxml import html
P=pathlib.Path(__file__).parent
rows=list(csv.DictReader((P/'pool-V.csv').open()))
urls=list(dict.fromkeys(urllib.parse.urldefrag(r['url'])[0] for r in rows if r['url']))
def fetch(u):
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(u,timeout=30) as res:b=res.read();final=res.geturl();status=res.status
  name=urllib.parse.urlsplit(u).path.rsplit('/',1)[-1];(P/(name+'.tmp')).write_bytes(b)
  return {'url':u,'checked_utc':now,'http_status':status,'final_url':final,'sha256':hashlib.sha256(b).hexdigest(),'local_temporary_filename':name+'.tmp'}
 except Exception as e:return {'url':u,'checked_utc':now,'status':'failure','error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:receipts=list(ex.map(fetch,urls))
(P/'candidate-fetch-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
for rec in receipts:
 if rec.get('http_status')!=200:print(rec);continue
 root=html.fromstring((P/rec['local_temporary_filename']).read_bytes());h=root.xpath('//h1')[0]
 print('DOC',rec['url'],'H1',h.text_content(),'PARENT',h.getparent().tag,h.getparent().attrib)
