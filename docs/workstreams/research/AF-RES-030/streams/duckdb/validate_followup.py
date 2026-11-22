"""Recount evidence rows and verify foreign keys/time windows; not a DuckDB product test."""
from pathlib import Path
import datetime as dt, hashlib, json, subprocess
P=Path(__file__).resolve().parent
repo=next(x for x in P.parents if (x/'.git').exists())
seal='9de54923257d613359348c8ccee2ff8225c8a0d8'
load=lambda name:[json.loads(x) for x in (P/name).read_text().splitlines()]
parse=lambda s:dt.datetime.fromisoformat(s.replace('Z','+00:00'))
frozen=['initial.jsonl','questions.csv','frame.csv','pairs-frozen.csv','source-ledger.jsonl','T0_NOTES.md']
frozen_results={}
for name in frozen:
 path=(P/name).relative_to(repo).as_posix()
 old=subprocess.check_output(['git','show',seal+':'+path],cwd=repo)
 current=(P/name).read_bytes()
 sealed_blob=subprocess.check_output(['git','rev-parse',seal+':'+path],cwd=repo,text=True).strip()
 working_blob=subprocess.check_output(['git','hash-object','--path='+path,path],cwd=repo,text=True).strip()
 frozen_results[name]={'raw_bytes_identical':old==current,'canonical_git_blob_unchanged':sealed_blob==working_blob,'sealed_blob':sealed_blob,'working_blob':working_blob}
 assert sealed_blob==working_blob, 'Frozen Git blob changed: '+name
chains=load('chains.jsonl');initial={x['case_id']:x for x in load('initial.jsonl')};providers=load('providers.jsonl');audit=load('screening-followups.jsonl')
assert len(chains)==10 and len({x['case_id'] for x in chains})==10
assert {x['case_id'] for x in chains if x['sample']=='A'}=={f'D{i:02}' for i in range(1,9)}
assert {x['case_id'] for x in chains if x['sample']=='B'}=={'DB04','DB07'}
assert len(audit)==30 and sum(x['eligible_root'] for x in audit)==26 and sum(x['selected_global_B'] for x in audit)==2
provider_ids={x['source_id'] for x in providers};assert len(provider_ids)==len(providers)
allkeys=[];question_count=0;direct_answers=0
for x in chains:
 assert x['first_response_url']==initial[x['case_id']]['first_response_url']
 assert set(x['provider_source_ids'])<=provider_ids
 root=parse(x['root_created_utc']);qs={q['question_id']:q for q in x['questions']}
 question_count+=sum(q['kind']=='information_request' for q in qs.values())
 for a in x['answers']:
  if not a.get('same_variable'):continue
  q=qs[a['question_id']];when=parse(a['created_utc']);asked=parse(q['created_utc'])
  assert a['actor']==x['root_author'];assert asked<=when
  assert a['answer_within_root30']==(when<=root+dt.timedelta(days=30))
  assert a['answer_within_root90']==(when<=root+dt.timedelta(days=90))
  assert a['answer_within_question30']==(when<=asked+dt.timedelta(days=30))
  assert abs(a['wait_hours']-(when-asked).total_seconds()/3600)<1e-8
  assert a['url'].startswith(x['root_url']+'#issuecomment-')
  allkeys.append(a['roundtrip_key']);direct_answers+=1
 if x['chain_success']:
  assert x['same_variable_answer'] and x['linked_recommendation_change'] and x['new_execution_success']
 assert x['windows']['root30_comment_count']<=x['windows']['root90_comment_count']<=x['windows']['current_all_comment_count']
assert len(allkeys)==len(set(allkeys))==3
assert question_count==5 and direct_answers==3
assert sum(x['linked_recommendation_change'] for x in chains)==0
assert sum(x['new_execution_success'] for x in chains)==1
assert next(x for x in chains if x['new_execution_success'])['case_id']=='D08'
assert next(x for x in chains if x['case_id']=='DB04')['exposure_effective'] is True
assert next(x for x in chains if x['case_id']=='D02')['no_prior_proposal'] is True

counts={}
for group in ['A','B']:
 z=[x for x in chains if x['sample']==group]
 counts[group]={'cases':len(z),'first_question_cases':sum(x['first_question'] for x in z),
 'any_information_question_root30_cases':sum(x['any_question_root30'] for x in z),
 'same_variable_direct_answer_cases':sum(x['same_variable_answer'] for x in z),
 'restatement_already_present_cases':sum(x['restatement_already_present'] for x in z),
 'strict_linked_recommendation_change_cases':sum(x['linked_recommendation_change'] for x in z),
 'bundle_linked_explanation_revision_cases':sum(x.get('bundle_linked_explanation_revision',False) for x in z),
 'new_execution_success_cases':sum(x['new_execution_success'] for x in z),'new_execution_failure_cases':sum(x['new_execution_failure'] for x in z),
 'chain_success_cases':sum(x['chain_success'] for x in z),
 'original_full_verified_cases':sum(x['original_grade']=='O' for x in z),
 'unexposed_cases':sum(not x['exposure_effective'] for x in z),
 'non_supplier_requester_cases':sum(not x['supplier_also_requester'] for x in z)}
inputs=['chains.jsonl','later-questions.csv','corrections.jsonl','providers.jsonl','screening-followups.jsonl','reading-updates.jsonl','contrasts.csv','prediction-audit.jsonl','followup-notes.md']+frozen
record={'check':'DuckDB data recount, foreign keys, clock windows, frozen canonical Git blob comparison',
 'execution':'actual local Python shell; no remote CI receipt and no DuckDB binary/test execution',
 'target_git_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),
 'sealed_input_sha':seal,'input_state':'listed working-tree artifacts hashed; not asserting all are yet committed',
 'input_sha256':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in inputs},
 'command':'python docs/workstreams/research/AF-RES-030/streams/duckdb/validate_followup.py',
 'checked_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':0,'counts':counts,
 'frozen_unchanged':frozen_results,'actual_information_question_utterances':question_count,'unique_direct_answer_roundtrips':len(allkeys),
 'B_audit_roots':30,'B_eligible_screened':26,'B_root_exclusions':4,
 'provider_read_records':len(providers),'provider_distinct_groups':len({x['duplicate_group'] for x in providers}),
 'provider_minimum_count':sum(x['count_minimum'] for x in providers),
 'minimum_A_thread_count':8,'not_an_independent_reader':True,
 'limitations':['Coding judgments are human/model judgments, not proved by schema checks','Original root versions unrecovered','No product execution; source expectations only']}
(P/'evidence/followup-validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record['counts'],ensure_ascii=False));print('frozen_git_blobs_unchanged=6/6; question_utterances=5; unique_answer_roundtrips=3; provider_minimum=9; exit_code=0')
