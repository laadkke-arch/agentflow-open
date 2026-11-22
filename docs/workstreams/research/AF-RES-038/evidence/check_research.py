"""Verify bounded artifact integrity, not source truth or human effects."""
from pathlib import Path
import ast,csv,hashlib,json,re,subprocess
from datetime import datetime,timezone
B=Path(__file__).resolve().parents[1]
REPO=B.parents[3]
def j(p):return json.loads((B/p).read_text())
def sha(p):return hashlib.sha256((B/p).read_bytes()).hexdigest()
checks={}
syntax=[]
for p in B.rglob('*.py'):
    ast.parse(p.read_text(),filename=str(p));syntax.append(str(p.relative_to(B)))
for p in B.rglob('*.json'):json.loads(p.read_text())
for p in B.rglob('*.jsonl'):
    for line in p.read_text().splitlines():
        if line.strip():json.loads(line)
checks['structured_files_parse']=True
sources=[json.loads(x) for x in (B/'sources.jsonl').read_text().splitlines() if x]
required={'source_id','original_url','pinned_url_or_version','publisher','published_or_event_date','checked_utc','locator','source_kind','verified_fact','limitation','question_ids','case_ids','duplicate_group','counted'}
checks['source_schema']=all(required.issubset(r) for r in sources)
checks['source_ids_unique']=len({r['source_id'] for r in sources})==len(sources)
counted=[r for r in sources if r['counted']]
checks['counted_groups_unique']=len({r['duplicate_group'] for r in counted})==len(counted)
checks['source_minimum']=len(counted)>=24
summary=j('evidence/source-summary.json')
checks['canonical_count_agrees']=len(counted)==summary['counted_unique_original_groups'] and len(sources)==summary['ledger_rows']
counted_ids={r['source_id'] for r in counted}
role_ids=[i for r in summary['roles'].values() for i in r['source_ids']]
checks['disjoint_role_assignment']=len(role_ids)==len(set(role_ids))==len(counted_ids) and set(role_ids)==counted_ids
witness=summary['core_24_disjoint_witness']['by_role']
wids=[i for v in witness.values() for i in v]
checks['core_24_disjoint_and_counted']=len(wids)==len(set(wids))==24 and set(wids).issubset(counted_ids)
frames=list(csv.DictReader((B/'frame.csv').open()))
checks['frame_40_and_selected_4']=len(frames)==40 and sum(r['eligibility']=='selected_document_task_conditional' for r in frames)==4
checks['participant_files_20']=len(list((B/'packets').glob('*/*.md')))==20
checks['bc_identity']=all(r['same_urls_order_versions'] and r['only_explanation_paragraphs_differ'] and r['max_three'] for r in j('evidence/material-check.json')['case_checks'])
checks['card_urls_anonymous_access']=j('evidence/public-access.json')['opened']==j('evidence/public-access.json')['denominator']==11
rr=list(csv.DictReader((B/'rubric.csv').open()))
checks['rubric_12_unique_requirements']=len(rr)==len({r['requirement_id'] for r in rr})==12
checks['all_t1_same_requirement']=all(r['same_original_requirement_t1']=='True' for r in rr)
seal=j('evidence/grade-seal.json')
checks['original_blind_json_unchanged']=sha('evidence/blind-input.json')==seal['input_hashes']['evidence/blind-input.json']
checks['original_expected_json_unchanged']=sha('evidence/expected-before-grading.json')==seal['input_hashes']['evidence/expected-before-grading.json']
transport=j('evidence/transport-normalization.json')
checks['original_csv_transport_explained']=transport['difference_only_crlf_to_lf'] and transport['parsed_rows_equal'] and transport['sealed_local_crlf_sha256']==seal['input_hashes']['rubric.csv']
checks['clarification_archive_hash']=sha('evidence/rubric-at-clarification.csv')==j('evidence/clarification-seal.json')['new_rubric_sha256']
checks['final_rubric_hash']=sha('rubric.csv')==j('evidence/post-review-rubric-change.json')['after_sha256']
checks['clarification_input_unchanged']=sha('evidence/blind-clarification-input.json')==j('evidence/clarification-seal.json')['input_sha256']==j('evidence/blind-clarification-observed.json')['input_sha256']
ex=[json.loads(x) for x in (B/'examples.jsonl').read_text().splitlines() if x]
checks['examples_12']=len(ex)==len({e['submission_id'] for e in ex})==12
checks['examples_have_three_judgment_stages']=all(e['expected_before_grade'] and e['author_self_read'] and e['separate_context_observed'] and e['adjudication'] for e in ex)
checks['no_example_human_durations']=all(all(e[k] is None for k in ['first_declaration_utc','t0_active_seconds','t1_active_seconds','repair_seconds']) and not e['external_human_validated'] for e in ex)
grades=j('evidence/grading-comparison.json')
checks['first_grades_preserved']=grades['overall_matches']==12 and grades['first_requirement_matches']==35 and len(grades['disagreements'])==1
checks['no_valid_rejected_or_bad_accepted']=grades['valid_false_rejections']==grades['invalid_false_acceptances']==0
fix=[json.loads(x) for x in (B/'evidence/measurement-fixtures.jsonl').read_text().splitlines() if x]
checks['state_fixtures_12_without_human_times']=len(fix)==12 and all(all(r[k] is None for k in ['active_seconds','repair_active_seconds','provider_active_seconds','first_acceptance_utc']) for r in fix)
checks['state_rule_and_semantic_checks']=j('evidence/measurement-check.json')['matching']==12 and j('evidence/measurement-comparison.json')['matches']==12
checks['blank_forms_11']=len(list((B/'forms').glob('*.csv')))==11 and all(len(list(csv.reader(p.open())))==1 for p in (B/'forms').glob('*.csv'))
checks['run_config_not_run']=j('forms/run-config.json')['actual_human_participants']==0 and j('forms/run-config.json')['status']=='NOT_LOCKED_NOT_RUN'
lines=(B/'RESULT.md').read_text().splitlines()
tables=[];current=[]
for n,line in enumerate(lines,1):
    if line.startswith('| '):current.append((n,line))
    elif current:tables.append(current);current=[]
if current:tables.append(current)
checks['result_first_two_and_last_tables']=lines[0].startswith('# ') and lines[2].startswith('| 과제 ID') and len(tables[0])-2==12 and len(tables[1])-2==12 and len(tables[-1])-2==3 and tables[-1][-1][0]==len(lines)-1
selfcheck=(B/'SELF_CHECK.md').read_text()
checks['self_check_all_questions']=all('## Q'+str(i)+' ' in selfcheck for i in range(1,8))
manifest=j('manifest.json')
branch=subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()
changed=subprocess.check_output(['git','diff','--name-only',manifest['base_commit']],cwd=REPO,text=True,stderr=subprocess.PIPE).splitlines()
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=REPO,text=True).splitlines()
prefix='docs/workstreams/research/AF-RES-038/'
checks['branch_and_path_scope']=branch=='work/research-af-res-038' and all(p.startswith(prefix) for p in changed+untracked)
checks['dot_control_not_edited']='docs/automation/dot-control.json' not in changed+untracked
result={'checked_utc':datetime.now(timezone.utc).isoformat(),'kind':'ARTIFACT_INTEGRITY_NOT_HUMAN_STUDY_ACCEPTANCE','checks':checks,
 'passed':sum(bool(v) for v in checks.values()),'denominator':len(checks),'all_passed':all(checks.values()),
 'syntax_only_files':syntax,'software_API_tests_executed':False,'human_participants':0,
 'result_table_locations':{'mandatory_1':{'start_line':tables[0][0][0],'end_line':tables[0][-1][0],'data_rows':len(tables[0])-2},'mandatory_2':{'start_line':tables[1][0][0],'end_line':tables[1][-1][0],'data_rows':len(tables[1])-2},'last_weaknesses':{'start_line':tables[-1][0][0],'end_line':tables[-1][-1][0],'data_rows':len(tables[-1])-2}},
 'known_substantive_unmet':['N08 absolute first-public formal version not confirmed'],'unperformed':['historical software environments','external human scoring','human experiment'],
 'meaning':'구조/해시/원장/예시 비교 검증. 출처의 역사적 완결성·사람 판별력·제품 효과를 자동 검증한 것이 아님.'}
(B/'evidence/verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':result['passed'],'denominator':result['denominator'],'failed':[k for k,v in checks.items() if not v],'tables':result['result_table_locations']},ensure_ascii=False))
if not result['all_passed']:raise SystemExit(1)
