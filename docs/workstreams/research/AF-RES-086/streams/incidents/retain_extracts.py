"""Retain short documentary extracts and receipts; do not republish full discussions/pages."""
from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;E=P/'evidence'
X={x['url']:x for x in map(json.loads,(P/'extracts.jsonl').read_text().splitlines())}
for f in E.glob('issue-*.json'):
 j=json.loads(f.read_text());d=j['data']
 if 'body' not in d:continue
 body=d['body'] or '';x=X[d['html_url']]
 j['receipt_kind']='short extract from directly retrieved issue; provider HTTP wire bytes unavailable'
 j['received_body_utf8_bytes']=len(body.encode());j['received_body_sha256']=hashlib.sha256(body.encode()).hexdigest()
 keep={k:d.get(k) for k in ['id','number','title','html_url','created_at','updated_at','closed_at','state','comments','author_association']}
 keep.update(author=d.get('user',{}).get('login'),short_original_extract=x['short_quote'],researcher_summary=x['finding'])
 j['data']=keep;f.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
for f in E.glob('comments-*.json'):
 j=json.loads(f.read_text());d=j['data']
 if not isinstance(d,list):continue
 out=[]
 for c in d:
  if 'body' not in c:out.append(c);continue
  body=c['body'] or ''
  out.append({**{k:c.get(k) for k in ['id','html_url','created_at','updated_at','author_association']},'author':c.get('user',{}).get('login'),'received_body_utf8_bytes':len(body.encode()),'received_body_sha256':hashlib.sha256(body.encode()).hexdigest(),'within_historical_window':c.get('created_at','')<'2026-01-01','body_retention':'Full public comment directly retrieved and relevant parts read; summary in NOTES/incident row; no full comment republication.'})
 j['data']=out;j['receipt_kind']='comment identities/timestamps/body digests; same incident lineage';f.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
for f in E.glob('search-*.json'):
 j=json.loads(f.read_text());r=j.get('result',{})
 for d in r.get('issues',[]):
  d.pop('body',None)
 j['receipt_kind']='discovery only; no body evidence counted';f.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
f=E/'supplement-0.json';j=json.loads(f.read_text());d=j['data']
if 'body' in d:
 body=d['body'] or '';j['received_body_utf8_bytes']=len(body.encode());j['received_body_sha256']=hashlib.sha256(body.encode()).hexdigest()
 j['data']={k:d.get(k) for k in ['id','number','title','html_url','created_at','updated_at','comments','author_association']}
 j['data']['author']='YDX-2147483647'
 j['data']['retained_documentary_fields']={'source_sha':'7d14b2f45ed78db82f976e5cd2dec5c7ffac2f9f','build_run_id':19385417200,'artifact_id':4575825543,'artifact_created_at':'2025-11-15T06:00:13Z','artifact_size_bytes':3160,'publisher_artifact_sha256':'d53e4f18bc9a7e8b0c1d5dd6ba9f81ac546136d6f89531100a0f80a826c46b87','publisher_log_event_at':'2025-11-15T06:42:48Z','deployment_id':'7d14b2f45ed78db82f976e5cd2dec5c7ffac2f9f','page_url':'https://typst-community.github.io/dev-builds/','publish_report':'success','node_action_exit_code':0,'request_url':'https://typst-community.github.io/dev-builds/catalog.json','artifact_catalog_names':['typst-main.2025-11-14.0da0165','typst-main.2025-09-19.586b049'],'reader_catalog_names':['typst-main.2025-09-19.586b049'],'recovery_report':'New workflow_dispatch against same commit fixed content; rerun did not.','recovered_catalog_fingerprint':None,'observer':'publisher, retained public record; researcher did not download historic artifact'}
 j['receipt_kind']='short factual extract from publisher retained log/response report';f.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
f=E/'chain-3.json';j=json.loads(f.read_text());d=j['data']
if isinstance(d,dict) and 'structuredContent' in d:
 body=d['structuredContent']['content'];j['received_body_utf8_bytes']=len(body.encode());j['received_body_sha256']=hashlib.sha256(body.encode()).hexdigest()
 j['data']={'source_sha':'7d14b2f45ed78db82f976e5cd2dec5c7ffac2f9f','path':'.github/workflows/gh-pages.yaml','triggers':['push main','workflow_dispatch','release published'],'build_command':'python scripts/build_catalog.py','dynamic_input':'RELEASE_EVENT from github.event.release','upload_action':'actions/upload-pages-artifact@v3','upload_path':'./dist','deploy_needs':'build','deploy_action':'actions/deploy-pages@v4','environment':'github-pages'}
 j['receipt_kind']='factual configuration extract; no execution claim';f.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
# HTTP receipt already contains full downloaded-byte length/hash; retain only identifying content here.
for f in E.glob('*.body'):
 body=f.read_bytes();name=f.stem
 if name=='typst-catalog-current':
  d=json.loads(body);x={'catalog_version':d.get('version'),'typst_names':[a.get('name') for a in d.get('artifacts',{}).get('typst',[])]}
 else:
  s=body.decode(errors='replace');x={'title':re.findall(r'<title>(.*?)</title>',s,re.S)[:1],'revision':re.findall(r'Revision\s*<code>([^<]+)',s),'rtd_version':re.findall(r'property="readthedocs-version-slug" content="([^"]+)"',s),'error_page':'404' if name.startswith('firefly') else None}
 x.update(received_body_sha256=hashlib.sha256(body).hexdigest(),received_body_bytes=len(body),retention='Full response downloaded/read for title,version,revision or catalog names; only extract retained.')
 (E/(name+'.extract.json')).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');f.unlink()
