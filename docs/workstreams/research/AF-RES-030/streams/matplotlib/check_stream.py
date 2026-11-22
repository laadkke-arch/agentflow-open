"""Recount public Matplotlib ledgers without the ignored raw cache."""
from pathlib import Path
from collections import Counter
import csv
import datetime as dt
import hashlib
import json
import subprocess

P=Path(__file__).resolve().parent
REPO=next(p for p in P.parents if (p/'.git').exists())
SEAL='9de54923257d613359348c8ccee2ff8225c8a0d8'
def read(name):return [json.loads(s) for s in (P/name).read_text().splitlines() if s.strip()]
initial=read('initial.jsonl');chains=read('chains.jsonl');screen=read('screening-followups.jsonl')
providers=read('providers.jsonl');sources=read('source-ledger.jsonl')+read('screening-sources.jsonl')+providers
questions=list(csv.DictReader((P/'questions.csv').open()))
assert len(initial)==35 and len(chains)==9 and len(screen)==26
assert len({r['case_id'] for r in chains+screen})==35
assert {r['case_id'] for r in chains+screen}=={r['case_id'] for r in initial}
assert {r['case_id'] for r in chains if r['sample']=='B'}=={'MB09'}
assert all(not r['count_in_A_or_B'] for r in screen)
assert len({r['source_id'] for r in sources})==len(sources)
for r in sources:
    for key in ['source_id','type','publisher','url','version','checked_utc','sections','observed','limitations','linked_Q_cases','duplicate_group','count_minimum']:
        assert key in r,(r['source_id'],key)
for case in {r['case_id'] for r in questions}:
    assert sum(len(r['actual_quote'].split()) for r in questions if r['case_id']==case)<=25,case
for r in chains:
    assert r['same_variable_answer_case']==any(q['same_variable_direct'] for q in r['questions'])
    assert not r['full_goal_success_case'] or r['new_execution_success_case']
    assert not r['linked_recommendation_change_case'] or r['same_variable_answer_case']
    assert all(m['within_root90'] for m in r['messages'])
    assert r['root30_status']=='complete_public_snapshot' and r['root90_status']=='complete_public_snapshot'
    assert r['chain_success_case']==(r['same_variable_answer_case'] and r['linked_recommendation_change_case'] and r['new_execution_success_case'])
sealed=[]
for name in ['initial.jsonl','questions.csv','frame.csv','source-ledger.jsonl']:
    rel=str((P/name).relative_to(REPO))
    old=subprocess.check_output(['git','show',SEAL+':'+rel],cwd=REPO)
    current=(P/name).read_bytes()
    attrs=subprocess.check_output(['git','check-attr','text','eol','--',rel],cwd=REPO,text=True)
    canonical=current.replace(b'\r\n',b'\n') if ': eol: lf' in attrs else current
    assert old==canonical,'T0 sealed content changed after declared Git LF normalization: '+name
    sealed.append({'path':rel,'worktree_sha256':hashlib.sha256(current).hexdigest(),'git_normalized_sha256':hashlib.sha256(canonical).hexdigest(),'git_attributes':attrs.splitlines(),'unchanged_from':SEAL})
def count(rs):
    return {'cases':len(rs),'broad_first_questions':sum(r['broad_first_question'] for r in rs),'strict_first_information_questions':sum(r['strict_first_question'] for r in rs),'any_information_question_root30':sum(r['any_question_root30'] for r in rs),'same_variable_answer_cases':sum(r['same_variable_answer_case'] for r in rs),'current_root_overlapping_variable_cases':sum(any(q['already_in_current_root']=='already_present' for q in r['questions']) for r in rs),'pre_first_response_confirmed_overlap_cases':sum(any(q['already_in_pre_first_root_confirmed'] for q in r['questions']) for r in rs),'strict_linked_change_cases':sum(r['linked_recommendation_change_case'] for r in rs),'new_execution_success_cases':sum(r['new_execution_success_case'] for r in rs),'new_execution_failure_cases':sum(r['new_execution_failure_case'] for r in rs),'full_goal_success_cases':sum(r['full_goal_success_case'] for r in rs),'chain_success_cases':sum(r['chain_success_case'] for r in rs),'no_author_response_after_first_cases':sum(not r['author_response_after_first'] for r in rs),'observation_unavailable_cases':sum(r['observation_unavailable'] for r in rs),'root30_comment_observations':sum(sum(m['within_root30'] for m in r['messages']) for r in rs),'root90_comment_observations':sum(len(r['messages']) for r in rs),'strict_roundtrip_keys':sorted({k for r in rs for k in r['observed_cost']['strict_roundtrip_keys']}),'reply_roundtrip_keys':sorted({k for r in rs for k in r['observed_cost']['reply_roundtrip_keys']})}
counts={'A':count([r for r in chains if r['sample']=='A']),'B':count([r for r in chains if r['sample']=='B']),'A_no_known_exposure':count([r for r in chains if r['sample']=='A' and not r['exposure']]),'A_original_grades':dict(Counter(r['original_grade'] for r in chains if r['sample']=='A')),'screening_not_selected_cases':len(screen),'screening_root30_comments':sum(r['root30_comment_count'] for r in screen),'screening_root90_comments':sum(r['root90_comment_count'] for r in screen),'source_url_rows':len(sources),'source_unique_urls':len({r['url'] for r in sources}),'source_canonical_groups':len({r['duplicate_group'] for r in sources}),'provider_url_rows':len(providers),'provider_canonical_groups':len({r['duplicate_group'] for r in providers}),'provider_minimum_count':sum(r['count_minimum'] for r in providers),'A_thread_minimum_count':8,'B_and_screening_minimum_count':0,'minimum_count_total':sum(r['count_minimum'] for r in sources)}
(P/'counts.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
inputnames=['initial.jsonl','questions.csv','frame.csv','source-ledger.jsonl','chains.jsonl','screening-followups.jsonl','screening-sources.jsonl','providers.jsonl','later-questions.csv','corrections.jsonl']
receipt={'checked_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'command':'python docs/workstreams/research/AF-RES-030/streams/matplotlib/check_stream.py','git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),'input_scope':'working files listed below; git_head alone does not imply these files were committed','inputs':{name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in inputnames},'sealed_t0_files':sealed,'exit_code':0,'checks':['JSON/schema/count units','all35 screened roots linked to follow-up records','A/B selection kept fixed','strict answer/change/execution gates','one question excerpt <=25 English whitespace words per source in questions.csv','T0 four ledgers identical to seal after repository-declared Git LF normalization'],'limitations':['same worker recount, not independent substantive reread','historical GUI/PGF/Cartopy code not executed','copyright quote check applies to canonical questions.csv excerpt cells, not code literal duplicates'],'counts':counts}
(P/'evidence/stream-validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','exit_code':0,**counts},ensure_ascii=False))
