"""Check research denominators, evidence joins, local links, and owned-path scope.

No original author's code, timezone conversion, network source, or service is executed.
Use --read-only after the final handoff commit to avoid producing new artifacts.
"""
import csv
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from collections import Counter

ROOT=Path(__file__).resolve().parent.parent
REPO=ROOT.parents[3]
READ_ONLY='--read-only' in sys.argv
checks=[]
def check(name, condition, detail=None):
    checks.append({'name':name,'passed':bool(condition),'detail':detail})
def read_json(p):return json.loads(p.read_text())
def rows(n):return list(csv.DictReader((ROOT/n).open()))
def yes(v):return str(v).lower()=='true'

required=['SCOPE.md','frame.csv','receipts.csv','candidate-editions.csv','views.csv','cards.md','sources.jsonl','SELF_CHECK.md','RESULT.md','manifest.json','WORK_LOG.md','evidence/acceptance-evidence.json']
check('all required pre-handoff deliverables exist',all((ROOT/n).is_file() for n in required),required)
parse_fail=[];json_count=0
for f in ROOT.rglob('*'):
    if not f.is_file() or '.cache' in f.parts or '__pycache__' in f.parts:continue
    try:
        if f.suffix=='.json':read_json(f);json_count+=1
        elif f.suffix=='.jsonl':
            for l in f.read_text().splitlines():json.loads(l)
            json_count+=1
    except Exception as exc:parse_fail.append([str(f.relative_to(ROOT)),str(exc)])
check('JSON and JSONL syntax',not parse_fail,{'files':json_count,'failures':parse_fail})
sources=[json.loads(l) for l in (ROOT/'sources.jsonl').read_text().splitlines()]
keys=['source_id','lineage_id','kind','author','original_url','fixed_url','version_or_date','opened_utc','locator','findings','limits','questions','case_ids','count_minimum','category']
check('source ledger required fields',all(all(k in r and r[k] not in ['',None,[]] for k in keys) for r in sources))
check('110 distinct source read rows',len(sources)==110 and len({r['source_id'] for r in sources})==110)
counted=[r for r in sources if r['count_minimum']]
check('51 independent works without counted lineage duplication',len(counted)==51 and len({r['lineage_id'] for r in counted})==51)
check('at least8 eligible report works from both projects',sum(r['category'] in ['issue_report','reported_issue'] for r in counted)==38 and all(any(repo in r['original_url'] for r in counted) for repo in ['pandas-dev/pandas','moment/moment-timezone']))
official=[r for r in counted if 'official' in r['category'] and r['source_id']!='S-L04']
check('seven version-pinned official works excluding mutable PEP snapshot',len(official)==7)
result_ids={'E-NB-PW','E-NB-JV','S-XD1','S-XZ1'}
check('four distinct union-defined execution/result-family works',result_ids.issubset({r['source_id'] for r in counted}) and len({r['lineage_id'] for r in counted if r['source_id'] in result_ids})==4)
check('two selected cross-field works',sum(r['category']=='cross_field' for r in counted)==2)

fr=rows('frame.csv');receipts=rows('receipts.csv');views=rows('views.csv');cand=rows('candidate-editions.csv')
for name,rs in [('frame',fr),('receipts',receipts),('views',views),('candidates',cand)]:
    check(name+' well-formed CSV fields',all(None not in r and all(v is not None for v in r.values()) for r in rs))
natural=[r for r in fr if r['layer']=='natural'];ci=[r for r in fr if r['layer']=='execution-first-candidate']
check('frame94 = natural60 + candidate30 + output slots4',len(fr)==94 and len(natural)==60 and len(ci)==30 and sum(r['layer']=='execution-first-output-slot' for r in fr)==4)
expected={'pandas-dev/pandas':['38928','39398','40336'],'moment/moment-timezone':['922','925','926']}
for repo,ids in expected.items():
    rr=[r for r in natural if r['repository']==repo]
    check(repo+' first30 chronological body frame',len(rr)==30 and [int(r['original_rank']) for r in rr]==list(range(1,31)) and [(r['created_utc'],int(r['record_id'])) for r in rr]==sorted((r['created_utc'],int(r['record_id'])) for r in rr))
    check(repo+' first3 eligible selected without outcome replacement',[r['record_id'] for r in rr if yes(r['eligible'])][:3]==ids==[r['record_id'] for r in rr if yes(r['selected'])])
check('execution candidates15 observed,15 empty Moment positions',sum(yes(r['observed_exists']) for r in ci)==15 and all(r['repository']=='pandas-dev/pandas' for r in ci if yes(r['observed_exists'])))
main=['N-P1','N-P2','N-P3','N-M1','N-M2','N-M3','E-P1','E-P2','E-M1','E-M2']
rc={r['case_id']:r for r in receipts}
check('37 unique receipt rows',len(receipts)==37 and len(rc)==37)
check('six natural reports, four literal date outputs',len([r for r in receipts if r['layer']=='natural'])==6 and {r['case_id'] for r in receipts if r['layer']=='natural' and yes(r['date_output_published'])}=={'N-P1','N-P2','N-M1','N-M2'})
check('no natural loaded edition/byte/same-run overattribution',all(not yes(r[k]) for r in receipts if r['layer']=='natural' for k in ['provider_label_confirmed','loaded_bytes_confirmed','same_run_label_output','same_run_full_bytes']))
check('four output slots remain empty',all(not yes(rc[c]['traceable']) and not yes(rc[c]['date_output_published']) for c in main[6:]))
check('positive auxiliary limited to L+O-R and excluded from cohort',yes(rc['A-M967-M']['same_run_label_output']) and not yes(rc['A-M967-M']['loaded_bytes_confirmed']) and rc['A-M967-M']['layer']=='auxiliary')
check('receipt source joins',all(r['source_id'] in {s['source_id'] for s in sources}|{'E-AUDIT'} for r in receipts),[r['source_id'] for r in receipts if r['source_id'] not in {s['source_id'] for s in sources}|{'E-AUDIT'}])
check('30 view cells = same10 x3',len(views)==30 and set(r['case_id'] for r in views)==set(main) and all({r['view'] for r in views if r['case_id']==c}=={'V0','V1','V2'} for c in main))
check('no main view falsely confirms edition',all(not yes(r['loaded_edition_confirmed']) and not yes(r['same_run_label_output']) for r in views))
check('30 candidate rows with all10 cases covered',len(cand)==30 and set(main).issubset({r['case_id'] for r in cand}))
check('bounded candidates not presented as unique historical edition',all(r['unique_edition']=='미확인' if r['case_id'] in main else '미확인' in r['unique_edition'] for r in cand))

cost=read_json(ROOT/'evidence/view-costs.json')
check('view costs28=25+3 and extra final audit1',cost['natural_case_request_attempts']==28==cost['natural_case_successful_reads']+cost['natural_case_failed_reads'] and cost['selected_case_requests_including_final_audit']==29)
zen=read_json(ROOT/'evidence/crossfield/zenodo-package-inspection.json')
check('Zenodo archive checksum and24 empty notebook outputs',zen['archive_md5']==zen['archive_md5_expected'] and len(zen['notebook_census'])==24 and all(x['cells_with_outputs']==0 and x['non_null_execution_count']==0 for x in zen['notebook_census']))
dv=read_json(ROOT/'evidence/crossfield/dataverse-version-inspection.json')['versions']
u=[next(f for f in v['file_manifest'] if f['name']=='U_Data.xlsx') for v in dv]
check('Dataverse V1/V2 different manifests same U_Data member',[v['file_count'] for v in dv]==[5,61] and u[0]['id']==u[1]['id'] and u[0]['checksum']==u[1]['checksum'])

text=(ROOT/'RESULT.md').read_text();lines=text.splitlines();tables=[];current=[]
for line in lines:
    if line.startswith('|'):current.append(line)
    elif current:tables.append(current);current=[]
if current:tables.append(current)
check('RESULT starts with required first table',lines[0].startswith('| 사례·층·원기록 URL'))
for i in [0,1]:
    check('required table'+str(i+1)+' exactly ten rows in fixed order',len(tables[i])==12 and [l.split('|')[1].strip().split(' ')[0] for l in tables[i][2:]]==main)
check('last RESULT table exactly3 weaknesses and no trailing prose',len(tables[-1])==5 and tables[-1][0].startswith('| 불일치·약점') and text.rstrip().endswith(tables[-1][-1]))
check('Q1-Q7 each has own result and self-check coverage',all('## Q'+str(n) in text and '| Q'+str(n) in (ROOT/'SELF_CHECK.md').read_text() for n in range(1,8)))
check('RESULT numeric claims match canonical counts','110행' in text and '51개 독립 계보' in text and '4/6 O-R' in text and '28요청=25성공+3실패' in text)

broken=[];links=0
for f in ROOT.rglob('*.md'):
    if '.cache' in f.parts:continue
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',f.read_text()):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'):continue
        target=target.split('#')[0].split('?')[0]
        if not target:continue
        links+=1
        if not (f.parent/target).exists():broken.append({'file':str(f.relative_to(ROOT)),'target':target})
check('all relative Markdown links resolve locally',not broken,{'links':links,'broken':broken})
base='1e741fd0def88ef56b1060a478d81f1985a4e760'
paths=[]
for args in [['git','diff','--name-only',base,'HEAD'],['git','diff','--name-only','HEAD'],['git','ls-files','--others','--exclude-standard']]:
    r=subprocess.run(args,cwd=REPO,capture_output=True,text=True)
    check('scope command '+' '.join(args[:3]),r.returncode==0,r.stderr[:500]);paths+=r.stdout.splitlines()
prefix='docs/workstreams/research/AF-RES-063/'
check('every committed/working/untracked changed path is owned',all(x.startswith(prefix) for x in paths),sorted(set(x for x in paths if not x.startswith(prefix))))
check('dot-control and common instructions not changed',all(not x.endswith('dot-control.json') and x!='AGENTS.md' for x in paths))

passed=all(c['passed'] for c in checks)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
if not READ_ONLY and passed:
    a=read_json(ROOT/'evidence/acceptance-evidence.json')
    for r in a['requirements']:
        if r['id']=='A15':
            r['actual']['numerator']=1;r['status']='실제 통합검사 통과';r['checked_head_sha']=sha;r['checked_utc']=now;r['check_actor']='web-pro/root';r['minimum_resume_action']='Recheck only after concrete evidence changes or for final immutable-commit gate'
    (ROOT/'evidence/acceptance-evidence.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
report={'status':'passed' if passed else 'failed','actor':'web-pro/root','executed_utc':now,'head_sha_at_validation':sha,'working_deliverables_validated':True,'checks_passed':sum(c['passed'] for c in checks),'checks_total':len(checks),'checks':checks,'input_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in required},'not_tested':['historical process authenticity','original timezone conversion execution','remote URL current availability','whole repository implementation tests','workbench session contract (separate command)']}
if not READ_ONLY:(ROOT/'evidence/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':report['status'],'passed':report['checks_passed'],'total':len(checks),'failures':[c for c in checks if not c['passed']]},ensure_ascii=False))
sys.exit(0 if passed else 1)
