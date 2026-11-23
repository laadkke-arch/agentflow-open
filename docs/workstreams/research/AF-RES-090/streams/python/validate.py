"""Read-only validation of Python-stream structure and optional retained raw bytes."""
import json,hashlib,re,html,sys,datetime,subprocess
from pathlib import Path
R=Path(__file__).parent;E=R/'evidence'
checks=[]
def check(name,value):
 checks.append({'check':name,'passed':bool(value)})
rows=json.loads((R/'traversals.json').read_text());sources=[json.loads(l) for l in (R/'sources.jsonl').read_text().splitlines()]
check('8 distinct reader traversals',len(rows)==len({x['traversal_id'] for x in rows})==8)
check('4 complete A/B pairs',all({r['route'] for r in rows if r['purpose_id']==p}=={'A','B'} for p in ['P3-body','P3-next','P1-body','P1-next']))
check('Every reader path bounded at two',all(1<=r['view_count']==len(r['views'])<=2 for r in rows))
check('13 independent response receipts',len({v['source_id'] for r in rows for v in r['views']})==13)
check('Measured reader byte total',sum(r['response_bytes'] for r in rows)==1206482)
check('Named404 retained twice',all(r['views'][0]['status']==404 and r['view_count']==1 for r in rows if r['case_id']=='P1' and r['route']=='B'))
check('P3 A body final recovery retained',next(r for r in rows if r['traversal_id']=='P3-body-A')['target_body']=='confirmed')
check('P3 exact target not substituted',all(not r['strict_target_reached'] and r['alternative_information_confirmed'] for r in rows if r['purpose_id']=='P3-next'))
check('P1 upstream not inserted into reader budget',all('https://pypi.org' not in [v['requested_url'] for v in r['views']] for r in rows))
check('Source IDs unique',len(sources)==len({x['source_id'] for x in sources}))
check('All eligible receipts HTTP200',all(x['fingerprint']['status']==200 for x in sources if x['eligible']))
check('No eligible duplicate body hashes',len([s for s in sources if s['eligible']])==len({s['fingerprint']['sha256'] for s in sources if s['eligible']}))
raw_available=0
for f in E.glob('*.receipt.json'):
 d=json.loads(f.read_text());p=E/'raw'/(d['source_id']+'.bin')
 if p.exists():
  raw_available+=1;b=p.read_bytes();check('raw '+d['source_id'],len(b)==d['body_bytes'] and hashlib.sha256(b).hexdigest()==d['sha256'])
for a in [json.loads(l) for l in (R/'assets.jsonl').read_text().splitlines()]:
 if a['publisher_git_blob_sha1']:check('publisher Git blob '+a['asset_id'],a['publisher_file_match'] is True)
cmp=json.loads((E/'comparison.json').read_text());check('P1 identical extracted code at different versions',cmp['p1_first_config']['equal_extracted_text'] and cmp['p1_first_config']['source_version']!=cmp['p1_first_config']['served_version']);check('P3 different tables both retained',not cmp['p3_legacy_tables']['same_table'])
if '--require-raw' in sys.argv:check('all30 raw responses available',raw_available==30)
report={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checkout_head':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'worktree_note':'Checks files currently present; parent records committed result SHA separately.','raw_available':raw_available,'checks':checks,'all_passed':all(x['passed'] for x in checks),'limitation':'No JS/example execution or semantic proof beyond listed original payload checks. Raw cache is optional in committed-only mode.'}
print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(0 if report['all_passed'] else 1)
