"""Check saved CPython evidence; --network reopens exact source/HTML/PNG/ZIP URLs.
Does not run examples or build documentation, and never rewrites sealed predictions.
"""
from pathlib import Path
import argparse,csv,hashlib,io,json,re,struct,sys,zipfile
from urllib.request import urlopen
from urllib.parse import urljoin
p=argparse.ArgumentParser();p.add_argument('--network',action='store_true');args=p.parse_args()
root=Path(__file__).resolve().parent
rows=list(csv.DictReader((root/'lineage.csv').open()));audit=json.loads((root/'audit.json').read_text())
assert len(rows)==4
assert {(r['case_id'],r['version']) for r in rows}=={(c,v) for c in ['PY1','PY2'] for v in ['3.12.0','3.12.1']}
for r,a in zip(rows,audit['rows']):
 assert (r['case_id'],r['version'])==(a['case_id'],a['version'])
 assert r['payload_sha256']==a['payload_sha256']
 assert r['P_included']=='YES' and r['U_section_uses']=='YES' and r['G_this_build_generated']=='UNKNOWN'
 assert all(a[k] for k in ['body_http_equals_zip','payload_http_equals_zip','tag_rst_equals_archive_source','tag_png_equals_payload','prior_3_11_png_equals_payload'])
 assert a['section_tag_counts']['img']==1
 assert all(a['section_tag_counts'][k]==0 for k in ['source','picture','svg','script'])
 assert a['data_uri_count']==0
 assert a['dimensions']==([955,758] if r['case_id']=='PY1' else [500,320])
assert audit['main_predictions']=={'true':2,'false':0,'hold':0,'unknown':0,'denominator':2}
assert all(x['same_main_body_bytes'] for x in audit['main_body_dedup'])
if args.network:
 cache={};observations=[]
 def fetch(u):
  u=u.split('#',1)[0]
  if u not in cache:
   with urlopen(u,timeout=60) as response:
    b=response.read();cache[u]=b;observations.append({'url':u,'final_url':response.url,'status':response.status,'content_type':response.headers.get('Content-Type'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
  return cache[u]
 for r in rows:
  b=fetch(r['body_url']);assert hashlib.sha256(b).hexdigest()==r['body_sha256'];s=b.decode();anchor=r['body_url'].split('#',1)[1]
  section=re.search(r'<section id="'+re.escape(anchor)+r'">.*?</section>',s,re.S).group(0)
  assert 'src="'+r['reference_uri']+'"' in section
  assert urljoin(r['base_uri'],r['reference_uri'])==r['resolved_payload_uri']
  payload=fetch(r['resolved_payload_uri']);assert hashlib.sha256(payload).hexdigest()==r['payload_sha256'];assert len(payload)==int(r['payload_bytes'])
  package=fetch(r['package_url']);assert hashlib.sha256(package).hexdigest()==r['package_sha256']
  assert zipfile.ZipFile(io.BytesIO(package)).read(r['package_member'])==payload
  assert hashlib.sha256(fetch(r['source_url'])).hexdigest()==r['source_sha256']
  assert fetch(r['source_asset_url'])==payload
 print(json.dumps({'mode':'exact-network-readback','requests':len(cache),'observations':observations},indent=2))
print(json.dumps({'status':'passed','mode':'network_and_saved_evidence' if args.network else 'saved_evidence_consistency_only','rows':4,'P_YES':4,'U_YES':4,'G_UNKNOWN':4,'predictions_true':2,'examples_executed':0}))
