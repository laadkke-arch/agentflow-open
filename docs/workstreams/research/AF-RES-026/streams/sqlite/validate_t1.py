"""Meaningful denominator, seal, lineage, and citation integrity checks."""
import csv,datetime,hashlib,json
from pathlib import Path
P=Path(__file__).parent
def j(name):return json.loads((P/name).read_text())
def jl(name):return [json.loads(s) for s in (P/name).read_text().splitlines()]
def csvrows(name):return list(csv.DictReader((P/name).open()))
def dt(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
initial=jl('initial.jsonl');frozen=jl('frozen-responses.jsonl');analysis=jl('case-analysis.jsonl')
fields=jl('field-locations.jsonl');followups=csvrows('followups.csv');judgments=csvrows('judgments.csv')
metadata=j('followup-metadata.json');receipt=j('t1-receipt.json');t0=j('t0-receipt.json');counts=j('t1-counts.json')
sources=j('sources.json')+j('t1-sources.json');sourceids={s['id'] for s in sources}
byid={r['artifact_id']:r for r in metadata};checks=[]
def check(name,ok,detail):
    checks.append(dict(condition=name,met=bool(ok),evidence=detail))
check('8 cases ×3 frozen messages',len(initial)==8 and len(frozen)==8 and all(all(k in r for k in ['I','C','Q']) for r in frozen),'initial/frozen rows; case IDs '+','.join(r['case_id'] for r in initial))
check('same8 T0/T1/location case IDs',{r['case_id'] for r in initial}=={r['case_id'] for r in analysis}=={r['case_id'] for r in fields},'case-analysis.jsonl; field-locations.jsonl')
check('T0 core files unchanged',all(hashlib.sha256((P/n).read_bytes()).hexdigest()==h for n,h in t0['files_sha256'].items()),'t0-receipt.json files_sha256')
check('T1 follows permission and frozen messages',dt(receipt['first_followup_body_open_utc'])>dt(receipt['permission_received_utc']) and all(dt(r['created_utc'])<dt(receipt['first_followup_body_open_utc']) for r in frozen),'t1-receipt.json; global seal '+receipt['global_seal_commit'])
check('S01 exposure kept out of strict comparison',[r['case_id'] for r in analysis if not r['strict_preoutcome_eligible']]==['S01'],'case-analysis strict_preoutcome_eligible')
check('all53 raw artifacts verified',len(metadata)==53 and all(r.get('id_matches_raw_sha3') for r in metadata),'followup-metadata.json SHA3 matches IDs')
check('45 followup/edit rows match artifacts',len(followups)==45 and all(r['message_id'] in byid for r in followups),'followups.csv; original rows omitted, edit rows retained')
check('reply and edit lineage resolves',all((not r['reply_to'] or r['reply_to'] in byid) and (not r['is_edit_of'] or r['is_edit_of'] in byid) for r in followups),'followups.csv reply_to/is_edit_of')
expected={(r['case_id'],c['id'],q['id'],t) for r in initial for c in r['candidate_uses'] for q in r['requirements'] for t in ['T0','T1']}
actual={(r['case_id'],r['candidate_id'],r['condition_id'],r['timepoint']) for r in judgments}
check('each candidate/initial condition at T0 and T1',expected.issubset(actual) and len(judgments)==110,'102 original-condition rows +8 S05 explicit sub-boundary rows')
check('judgment citations resolve',all(all(x in sourceids for x in r['technical_source_ids'].split(';')) and r['technical_url'] and r['technical_locator'] for r in judgments),'judgments.csv technical source IDs, URLs, locators')
check('six T0 fields mapped without changing values',all(all(f in x['fields'] and x['fields'][f]['sealed_value']==next(r for r in initial if r['case_id']==x['case_id'])[f] and all(v['url'] and v['locator'] for v in x['fields'][f]['locations']) for f in ['goal','inputs','outputs','version','platform','actors']) for x in fields),'field-locations.jsonl')
check('all hypothetical messages <=300 characters',all(len(r[k])<=300 for r in frozen for k in ['I','C','Q']),'frozen-responses.jsonl; max '+str(max(len(r[k]) for r in frozen for k in ['I','C','Q'])))
check('Q never sent and no exact new value falsely counted',all(not r['strategies']['Q']['actual_message_sent'] and not r['q_value_recovered_strict'] for r in analysis),'case-analysis.jsonl; S04 conflict sensitivity separate')
check('author success only S01, source consultation separate',[r['case_id'] for r in analysis if r['actual_author_reports_progress']]==['S01'] and [r['case_id'] for r in analysis if r['actual_author_reports_source_consultation']]==['S07'],'case-analysis.jsonl')
check('no 31–90 day events in selected threads',all(r['within_30_days']=='True' for r in followups) and counts['same_thread_days31to90_messages']==0,'all observed timestamps lie within30; separate implementation remains unknown')
counted={s['id'] for s in sources if s['count_in_minimum']}
check('17 counted unique originals, reused source IDs not duplicated',len(counted)==17 and counts['counted_unique_originals_total']==17,'sources.json + t1-sources.json count true union; 8 conversations +9 provider originals')
check('strategy limited support and hold counts reproduce',all(sum(r['strategies'][k]['technical_status']=='supported_limited' for r in analysis)==5 and sum(r['strategies'][k]['technical_status']=='hold' for r in analysis)==3 for k in ['I','C']),'case-analysis versus t1-counts; holds not approvals')
check('six actual clarification pairs only',sum(len(r['actual_clarification_pairs']) for r in analysis)==6,'S01 three; S04 three; fictitious Q not in pairs')
out=dict(checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=checks,passed=sum(x['met'] for x in checks),total=len(checks),independent_review=False,meaning='data/seal integrity self-check, not re-execution of original users or independent outcome coding')
(P/'t1-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
if not all(c['met'] for c in checks):raise SystemExit(1)
