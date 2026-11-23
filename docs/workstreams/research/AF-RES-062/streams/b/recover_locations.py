from pathlib import Path
import json,urllib.request,urllib.parse,datetime,concurrent.futures
p=Path(__file__).parent
j=json.loads((p/'candidate-freeze.json').read_text())
keys={'DIG42','DIG35','DIG36','DIG32','SEARCH11','DIG22','DIG31','DIG33','DIG28','SEARCH6','SEARCH7','DIG21'}
rows=[r for r in j['method_order'] if r['discovery_key'] in keys]
def one(r):
 u='https://api.openalex.org/works/https://doi.org/'+r['doi'];out={'discovery_key':r['discovery_key'],'doi':r['doi'],'query_url':u,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  q=urllib.request.urlopen(u,timeout=20);s=json.load(q);out.update(status=q.status,open_access=s.get('open_access'),best_oa_location=s.get('best_oa_location'),locations=s.get('locations'))
 except Exception as e:out.update(status='failed',error=str(e))
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e: out=list(e.map(one,rows))
(p/'openalex-recovery.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
for x in out: print(x['discovery_key'],x['status'],json.dumps(x.get('open_access')),[(z.get('landing_page_url'),z.get('pdf_url')) for z in x.get('locations') or []])
