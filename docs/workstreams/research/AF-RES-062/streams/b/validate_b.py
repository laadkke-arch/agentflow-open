"""Required evidence-ledger consistency checks, not a participant analysis."""
from pathlib import Path
import json,csv,collections,datetime,re
p=Path(__file__).parent
checks={};counts={}
for f in p.glob('*.json'):
 json.loads(f.read_text());checks[f.name]='JSON parse PASS'
for f in p.glob('*.jsonl'):
 lines=f.read_text().splitlines()
 for line in lines:json.loads(line)
 counts[f.name]=len(lines);checks[f.name]='JSONL parse PASS'
for f in p.glob('*.csv'):
 with f.open() as h:r=list(csv.DictReader(h))
 assert r and not any(None in x for x in r),f
 counts[f.name]=len(r);checks[f.name]='CSV shape PASS'
sources=list(map(json.loads,(p/'sources.jsonl').read_text().splitlines()));ids={r['source_id'] for r in sources}
assert len(ids)==len(sources)
for file in ['frame.csv','stimuli.csv']:
 with (p/file).open() as h:rs=list(csv.DictReader(h))
 for r in rs:
  for i in r['source_ids'].split('|'):assert not i or i in ids,(file,i)
checks['source_id_links']='PASS'
f=json.loads((p/'corrected-order.json').read_text())
assert f['corrected_first25']==sum(f['method_status_counts'].values())==25
assert sum(f['eligibility_counts'].values())==25
checks['screen_denominators']='PASS'
h=json.loads((p/'hand-checks.json').read_text());assert all(h['tests'].values())
checks['acceptance_partition_and_abstention']='PASS'
with (p/'outcomes.csv').open() as h:outs=list(csv.DictReader(h))
for r in outs:
 if r['stratum']=='main-vacancy':assert r['acceptance_N']=='미확인'
 elif r['acceptance_N'].isdigit():assert 0<=int(r['acceptance_n'])<=int(r['acceptance_N'])
checks['no_false_zero_denominator']='PASS'
text=(p/'B_REPORT.md').read_text();local=[]
for target in re.findall(r'\]\(([^)]+)\)',text):
 if '://' not in target:
  candidate=p/target.split('#')[0];assert candidate.exists(),str(candidate);local.append(target)
checks['report_local_links']='PASS '+str(len(local))+' references'
counts['source_minimum_flags']=sum(x['count_minimum'] for x in sources)
counts['source_count_categories']=dict(collections.Counter(x['count_category'] for x in sources if x['count_minimum']))
receipt={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actor':'frame_b AI assistant','scope':'B stream schema,local references,screen denominators,aggregate arithmetic; not contract checker or human review','checks':checks,'counts':counts,'prior_failed_check':{'observed_utc_date':'2026-11-23','failure':'Aggregate partition checker incorrectly applied false-claim T+FM+CND identity using final_correct to true-claim rows, double-counting true acceptance; assertion failed.','correction':'Restricted that identity toFM and added universal acceptance+notaccepted=D check; source counts and outcome table did not change.','status':'corrected and rerun'},'not_performed':['git commits/push','workbench.session check','independent reexecution of participant joins','recovered fulltext methods for sixblocked publications'],'result':'PASS for listed structural/arithmetic checks; research acceptance remains PARTIAL'}
(p/'validation-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
