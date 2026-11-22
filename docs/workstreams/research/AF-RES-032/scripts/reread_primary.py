from pathlib import Path
import json,urllib.request,tarfile,io,hashlib,concurrent.futures,subprocess
from datetime import datetime,timezone
from lxml import html
P=Path(__file__).resolve().parents[1];refs={r['reference_id']:r for r in map(json.loads,(P/'evidence/a-sealed.jsonl').read_text().splitlines())};py=json.loads((P/'collectors/python/followup/archives.json').read_text());jobs=[]
for version in ['3.8.14','3.8.15']:
 r=next(x for x in py if x['version']==version);m=next(x for x in r['documents'] if x['name']=='bugs.html');jobs.append({'reference_id':'A-D02','purpose':'positive boundary reread','url':r['url'],'member':m['member'],'expected_archive_sha256':r['archive_sha256'],'expected_member_sha256':m['member_sha256'],'expected_href':m['anchors'][0]['href']})
r=refs['A-R04'];jobs.append({'reference_id':'A-R04','purpose':'hold original conditional recommendation reread','url':r.get('artifact_url',r.get('archive_url')),'member':r.get('member',r.get('member_path')),'expected_archive_sha256':r.get('artifact_sha256',r.get('archive_sha256')),'expected_member_sha256':r['member_sha256'],'expected_href':r['raw_href']})
jobs.append({'reference_id':'A-D01','purpose':'negative correction-needed hypothesis reread','url':refs['A-D01']['raw_href'],'member':None})
def run(j):
 o=dict(j,observed_at_utc=datetime.now(timezone.utc).isoformat())
 try:
  r=urllib.request.urlopen(j['url'],timeout=40);b=r.read();o.update(status=r.status,final_url=r.url,sha256=hashlib.sha256(b).hexdigest())
  if j['member']:
   t=tarfile.open(fileobj=io.BytesIO(b));raw=t.extractfile(j['member']).read();d=html.fromstring(raw);o['member_sha256']=hashlib.sha256(raw).hexdigest();o['href_present']=j['expected_href'] in d.xpath('//a/@href');o['archive_hash_matches']=o['sha256']==j['expected_archive_sha256'];o['member_hash_matches']=o['member_sha256']==j['expected_member_sha256'];o['pass']=o['href_present'] and o['archive_hash_matches'] and o['member_hash_matches'];o['finding']='Exact original archive/member bytes and relevant href match independently fetched bytes.'
   if j['reference_id']=='A-R04':o['pandoc_1_12_3_text_present']='1.12.3' in d.text_content();o['finding']='Original conditional Pandoc recommendation exists; this does not supply current IDE payload/version proof.'
  else:
   d=html.fromstring(b);o['pass']=r.status==200 and 'reStructuredText' in d.text_content();o['finding']='Original URL still reaches reStructuredText background description; current purpose check only.'
 except Exception as e:o['error']=repr(e);o['pass']=False
 return o
rows=list(concurrent.futures.ThreadPoolExecutor(4).map(run,jobs));out={'target_repository_head':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'working_tree_data_sha256':hashlib.sha256((P/'sources.jsonl').read_bytes()).hexdigest(),'command':'python docs/workstreams/research/AF-RES-032/scripts/reread_primary.py','read_mode':'fresh public urllib GET, tar member extraction; not cached-only or user interaction','checks':rows,'all_pass':all(r['pass'] for r in rows),'exit_code':0 if all(r['pass'] for r in rows) else 1,'completed_at_utc':datetime.now(timezone.utc).isoformat()};(P/'evidence/primary-reread.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({'checks':len(rows),'all_pass':out['all_pass'],'exit_code':out['exit_code']},indent=2));raise SystemExit(out['exit_code'])
