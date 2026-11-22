from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import ast, base64, hashlib, json
P=Path(__file__).resolve().parent
R=P.parents[1]
loadl=lambda p:[json.loads(x)for x in p.read_text().splitlines()if x]
sources=json.loads((P/'sources.json').read_text())
history=loadl(P/'candidate-history.jsonl')
decisions=loadl(P/'decisions.jsonl')
returns=loadl(R/'streams/arrow/returns.jsonl')
receipts=[json.loads(x.read_text())for x in sorted((P/'receipts').glob('*.json'))]
checks=[]
def ck(name,ok,detail=''):
 checks.append(dict(check=name,passed=bool(ok),detail=detail))
 if not ok: raise AssertionError(name+': '+detail)
sids={x['source_id']for x in sources}
ck('one history row for each unique returned candidate',len(history)==19 and {x['candidate_id']for x in history}=={x['candidate_id']for x in returns if x.get('candidate_id')})
ck('one decision per first question',len(decisions)==4 and {x['question_id']for x in decisions}=={'Q01','Q02','Q03','Q04'})
ck('source identifiers unique',len(sources)==len(sids)==93)
required={'source_id','title','source_url','version','published_or_revised','checked_utc','sections_read','verified_content','limitations','producer','lineage_id','count_in_minimum','count_reason','related_questions','source_role'}
for s in sources:
 ck('source schema '+s['source_id'],required<=s.keys() and s['source_role']in{'followup_decision','historical_provider'} and isinstance(s['count_in_minimum'],bool))
 ck('source after primary seal '+s['source_id'],datetime.fromisoformat(s['checked_utc'].replace('Z','+00:00'))>=datetime(2026,11,22,5,50,22,tzinfo=timezone.utc))
for h in history:
 ck('history status '+h['candidate_id'],h['historical_availability']in{'supported','not_available','unknown'} and bool(h['feature_evidence']) and bool(h['next_minimum_check']))
 ck('history references '+h['candidate_id'],set(h['source_ids'])<=sids and all(set(e['source_ids'])<=sids for e in h['feature_evidence']))
 ck('frozen citations retained '+h['candidate_id'],h['original_return_citations_unchanged'] and h['cannot_rescue_original_citations'])
for d in decisions:
 ck('decision references '+d['question_id'],set(d['source_ids'])<=sids and d['frozen_returns_changed']is False)
 ck('decision annotations cover returns '+d['question_id'],{x['candidate_id']for x in d['candidate_stage_annotations']}=={x['candidate_id']for x in history if x['question_id']==d['question_id']})
http=[x for x in receipts if 'request_id'in x]
web=[x for x in receipts if str(x.get('id','')).startswith('HS-')]
ck('receipt denominators',len(http)==93 and len(web)==4)
ck('success/failure denominator',sum(bool(x.get('success'))for x in http)==90 and sum(not x.get('success',False)for x in http)==3)
for x in http:
 if x.get('success'):
  path=P/x['cache_path']
  ck('retrieved hash '+x['request_id'],path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==x['body_sha256'])
 else: ck('failed source excluded '+x['request_id'],not next(s for s in sources if s['request_id']==x['request_id'])['count_in_minimum'])
cost=json.loads((P/'cost-summary.json').read_text())
ck('cost split',cost['http_get_requests']==93 and cost['web_search_requests']==4 and cost['execution_tests_run']==0 and cost['tokens']is None and cost['human_hours']is None)
for f in ['fetch.py','build_followups.py','verification-inputs/q01_pyarrow21_probe.py']:
 ast.parse((P/f).read_text());ck('python syntax only '+f,True,'Parsing only; no provider/runtime verification executed.')
blob=json.loads((P/'cache/H-JAVA-011.raw').read_text());body=base64.b64decode(blob['content'])
ck('Java cited blob matches body',hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()=='4d2acbb091af4e563e2a08fc2ae319a57f797f14')
ck('all four Qs have multiple subsequent original sources',all(sum(s['count_in_minimum'] and s['source_role']=='followup_decision' and d['question_id']in s['related_questions']for s in sources)>=2 for d in decisions))
result=dict(checked_utc=datetime.now(timezone.utc).isoformat(),all_passed=all(x['passed']for x in checks),count=len(checks),checks=checks,unique_returned_candidates=len(history),availability=dict(Counter(x['historical_availability']for x in history)),decisions=4,source_records=len(sources),local_minimum_count_flags=sum(x['count_in_minimum']for x in sources),global_original_dedup='Root final source registry remains authoritative; historical snapshots excluded locally.',runtime_tests_executed=0)
(P/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k]for k in ['all_passed','count','unique_returned_candidates','availability','decisions','source_records','local_minimum_count_flags','runtime_tests_executed']}))
