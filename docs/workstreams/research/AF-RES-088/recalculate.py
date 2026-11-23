"""Offline denominator/integrity checks for AF-RES-088. No semantic classifier."""
import argparse
from collections import Counter
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess

P=Path(__file__).resolve().parent
REPO=P.parents[3]
PREFIX='docs/workstreams/research/AF-RES-088/'
BASE='9dcae48a47b05d7ba2a1320444be28f5d0fcd739'
CONTRACT='9f8a8f5c0d4ac9f8659374d99e71f3d7a1013712'
R0='42e46d5788278efa8d5b8ab0272ace48830fb477'
R1='f048885abfbfcca1ffd8840899bf2911cd35da60'
STATES={'충족','명시 반박','범위 밖','미확인'}

def jl(name):return [json.loads(x) for x in (P/name).read_text().splitlines() if x.strip()]
def table(name):
    with (P/name).open() as f:return list(csv.DictReader(f))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def rate(n,d):return dict(numerator=n,denominator=d,value=n/d if d else None,status='calculated' if d else '산출 불가')
def ts(s):return datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
def truth(x):return x is True or x=='true'
def run_git(*args):return subprocess.check_output(['git',*args],cwd=REPO,text=True)

def calculate():
    f=table('frame.csv');c=table('candidates.csv');j=table('judgments.csv');p=table('pairs.csv');r=jl('revisions.jsonl');o=jl('outcomes.jsonl');s=jl('sources.jsonl')
    assert len(f)==60 and len({x['question_id'] for x in f})==60
    assert len(c)==8 and len(j)==64 and len(p)==32 and len(r)==8 and len(o)==8
    assert {x['case_id'] for x in r}=={'JN1','JN2','JE1','JE2','PN1','PN2','PE1','PE2'}
    assert len({(x['case_id'],x['revision'],x['candidate_id']) for x in j})==64
    assert len({x['pair_id'] for x in p})==32
    assert all(x['assessment'] in STATES and x['failure_rule'] and x['manual_source_ids'] for x in j)
    assert all(x['manual_url'] and x['reference_sha'] in x['manual_url'] for x in j)
    old=list(csv.DictReader(run_git('show',R0+':'+PREFIX+'judgments.csv').splitlines()))
    assert [x for x in j if x['revision']=='R0']==old,'R0 seal modified'
    assert run_git('show',CONTRACT+':'+PREFIX+'candidates.csv').replace('\r\n','\n')==(P/'candidates.csv').read_text().replace('\r\n','\n'),'candidate contract changed'
    for x in r:
        assert x['history_complete'] is True
        assert ts(x['r1']['revision_utc'])<=ts(x['question_created_utc'])+30*86400
        for rev in ['r0','r1']:
            a=x[rev];assert sha(P/a['body_path'])==a['raw_sha256']
        assert x['body_bytes_changed']==(x['r0']['raw_sha256']!=x['r1']['raw_sha256'])
        assert 'text_requirement_change' in x['semantic_comparison']
        if x['case_id']=='PE1':
            assert x['semantic_comparison']['full_input_information_change']=='unknown'
            assert x['semantic_comparison']['visual_equivalence']=='unknown'
    for x in p:
        a=next(y for y in j if y['case_id']==x['case_id'] and y['candidate_id']==x['candidate_id'] and y['revision']=='R0')
        b=next(y for y in j if y['case_id']==x['case_id'] and y['candidate_id']==x['candidate_id'] and y['revision']=='R1')
        known=a['assessment']!='미확인' and b['assessment']!='미확인'
        assert truth(x['documentary_comparable'])==known
        assert x['assessment_changed']==(str(a['assessment']!=b['assessment']).lower() if known else 'unknown')
        assert x['manual_sha']==a['reference_sha']==b['reference_sha']
    for x in o:
        assert x['read_after_pair_commit']==R1
        assert x['answer_records']==len(x['answers'])==x['current_answer_count']
        for a in x['answers']:assert sha(P/a['first_body_path'])==a['first_body_sha256']
        assert x['answers_within_30d']==sum(a['within_30d'] for a in x['answers'])
        if x['current_accepted_answer_id']:
            assert next(a for a in x['answers'] if a['answer_id']==x['current_accepted_answer_id'])['current_is_accepted']
    assert len({x['source_id'] for x in s})==len(s)
    primary=[x for x in s if x['count_primary']]
    assert all(x['direct_read'] and x['original_url'] and x['limitations'] and x['confirmed_content'] for x in s)
    assert len({x['primary_unit'] for x in primary})==len(primary)
    source_ids={x['source_id'] for x in s}
    assert all(set(x['manual_source_ids'].split(';'))<=source_ids for x in j)
    frames={}
    for tag in ['jq','pandoc']:
        ff=[x for x in f if x['tag']==tag]
        assert [int(x['original_rank']) for x in ff]==list(range(1,31))
        assert [(ts(x['creation_utc']),int(x['question_id'])) for x in ff]==sorted((ts(x['creation_utc']),int(x['question_id'])) for x in ff)
        natural=[x for x in ff if truth(x['eligible'])][:2]
        edited=[x for x in ff if truth(x['eligible']) and x not in natural and int(x['body_edits_30d_metadata'])>0][:2]
        assert {x['question_id'] for x in natural+edited}=={x['question_id'] for x in ff if x['selection']=='included'}
        frames[tag]=dict(raw=len(ff),eligible=sum(truth(x['eligible']) for x in ff),natural_selected=len(natural),edited_eligible_after_natural=sum(truth(x['eligible']) and x not in natural and int(x['body_edits_30d_metadata'])>0 for x in ff),edited_selected=len(edited),eligible_unselected=sum(x['selection']=='eligible_not_selected' for x in ff),vacant_slots=4-len(natural+edited),tag_basis='current at query; historical tags separately preserved',first_question=int(ff[0]['question_id']),last_question=int(ff[-1]['question_id']))
    strata={}
    for layer in ['natural','edited']:
        rr=[x for x in r if x['stratum']==layer];pp=[x for x in p if x['stratum']==layer];jj=[x for x in j if x['stratum']==layer];oo=[x for x in o if x['stratum']==layer]
        comparable=[x for x in pp if truth(x['documentary_comparable'])]
        accepted=[x for x in oo if x['current_accepted_answer_id']]
        strata[layer]=dict(cases=len(rr),planned_cases=4,planned_pairs=16,body_pairs_available=len(pp),judgment_rows=len(jj),body_bytes_changed=rate(sum(x['body_bytes_changed'] for x in rr),len(rr)),text_requirement_changed=rate(sum(x['semantic_comparison']['text_requirement_change'] for x in rr),len(rr)),text_input_information_changed=rate(sum(x['semantic_comparison']['text_input_information_change'] for x in rr),len(rr)),full_input_change_unknown=sum(x['semantic_comparison']['full_input_information_change']=='unknown' for x in rr),documentary_comparable_pairs=len(comparable),judgment_unknown_pairs=len(pp)-len(comparable),assessment_change=rate(sum(truth(x['assessment_changed']) for x in comparable),len(comparable)),next_question_change=rate(sum(truth(x['condition_or_next_question_changed']) for x in pp),len(pp)),r0_assessments=dict(Counter(x['assessment'] for x in jj if x['revision']=='R0')),r1_assessments=dict(Counter(x['assessment'] for x in jj if x['revision']=='R1')),body_edit_after_first_answer_cases=rate(sum(bool(x['question_body_edits_after_first_answer']) for x in oo),len(oo)),author_edit_after_first_answer_cases=rate(sum(x['author_body_edits_after_first_answer']>0 for x in oo),len(oo)),author_solution_insertion_after_answer_cases=rate(sum(x['author_solution_insertion_after_answer']>0 for x in oo),len(oo)),no_answer_within_30d_cases=rate(sum(x['answers_within_30d']==0 for x in oo),len(oo)),no_answer_or_comment_within_30d_cases=rate(sum(x['answers_within_30d']==0 and x['comments_within_30d']==0 for x in oo),len(oo)),current_no_answer_cases=rate(sum(x['answer_records']==0 for x in oo),len(oo)),current_accepted_cases=rate(len(accepted),len(oo)),accepted_primary_outside_pool=rate(sum(x['accepted_primary_solution_outside_pool'] is True for x in accepted),len(accepted)),questioner_followup_attempt=rate(sum(x['questioner_followup_attempt_reported'] for x in oo),len(oo)),questioner_complete_success_report=rate(sum(x['questioner_complete_success_reported'] for x in oo),len(oo)),strict_initial_bytes=rate(sum(x['initial_bytes_verified'] for x in rr),len(rr)),questioner_exact_version_report=rate(sum(x['questioner_exact_tool_version_reported'] for x in oo),len(oo)),questioner_success_exact_runtime_verified=rate(sum(x['questioner_success_with_exact_runtime_verified'] for x in oo),len(oo)))
    by_ledger={}
    for ledger in sorted({x['ledger_path'] for x in s}):
        ss=[x for x in s if x['ledger_path']==ledger];ss1=[x for x in ss if x['count_primary']]
        by_ledger[ledger]=dict(records=len(ss),primary_units=len(ss1),independent_events=len({x['independent_event_id'] for x in ss1}))
    changed_paths=run_git('diff','--name-only',BASE,'HEAD').splitlines()+run_git('diff','--name-only').splitlines()+run_git('ls-files','--others','--exclude-standard').splitlines()
    assert all(x.startswith(PREFIX) for x in changed_paths),'outside owned_path write'
    # A read-only review can check rendered table row counts after author_result.py.
    if (P/'RESULT.md').exists():
        result=(P/'RESULT.md').read_text();sections=['## 표 1','## 표 2','## 표 3','## 분모','## 판정']
        offsets=[result.index(x) for x in sections];assert offsets==sorted(offsets)
        for n,expected in [(0,8),(1,32),(2,24)]:
            lines=[x for x in result[offsets[n]:offsets[n+1]].splitlines() if x.startswith('|')]
            assert len(lines)-2==expected,(n,len(lines)-2)
        assert result.count('### 약점 ')==3
    comparable=[x for x in p if truth(x['documentary_comparable'])]
    metrics=dict(schema=1,task='AF-RES-088',research_status='PARTIAL',comparison_scope='explicit text requirements against frozen documentary candidate contract; not original first-post bytes or observed search quality',planned=dict(cases=8,pairs=32,judgment_rows=64),frame=frames,strata=strata,total=dict(cases=len(r),body_pairs_available=len(p),judgment_rows=len(j),documentary_comparable_pairs=len(comparable),unknown_pairs=len(p)-len(comparable),assessment_change=rate(sum(truth(x['assessment_changed']) for x in comparable),len(comparable)),next_question_change=rate(sum(truth(x['condition_or_next_question_changed']) for x in p),len(p)),positive_comparable_pairs=sum(x['r0_assessment']=='충족' for x in comparable),negative_comparable_pairs=sum(x['r0_assessment'] in ('범위 밖','명시 반박') for x in comparable),strict_initial_candidate_change=rate(0,0),causal_help_effect=rate(0,0),answer_records=sum(len(x['answers']) for x in o),answer_first_bodies=sum(len(x['answers']) for x in o),answerer_textual_result_reports=sum(x['answerer_textual_result_count'] for x in o),answerer_concrete_output_text_reports=sum(x['answerer_concrete_output_text_count'] for x in o),answerer_prose_result_reports_only=sum(x['answerer_prose_result_report_only_count'] for x in o),answerer_any_result_reports=sum(x['answerer_result_report_count'] for x in o),answerer_result_definition='concrete output text OR explicit observed-result prose in first preserved answer; excludes expectations and uninspected external demos',public_comment_records=sum(sum(y['kind']=='public_comment' for y in x['timeline']) for x in o),questioner_comment_records=sum(x['author_followup_comments'] for x in o),questioner_comment_cases=sum(x['author_followup_comments']>0 for x in o)),sources=dict(records=len(s),primary_units=len(primary),independent_events=len({x['independent_event_id'] for x in primary}),minimum_primary=24,minimum_independent=20,minimum_met=len(primary)>=24 and len({x['independent_event_id'] for x in primary})>=20,by_ledger=by_ledger),gaps=['PE1 old image content/visual equivalence missing','six Pandoc candidate implementations or reader/writer assumptions not verified'],not_measured=['population edit effect','independent semantic inter-rater agreement','questioner exact-version success','causal help or time saved'],input_sha256={name:sha(P/name) for name in ['frame.csv','candidates.csv','judgments.csv','pairs.csv','revisions.jsonl','outcomes.jsonl','sources.jsonl']})
    return metrics

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');a=ap.parse_args()
    metrics=calculate()
    if a.write:(P/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
    if a.check:assert metrics==json.loads((P/'metrics.json').read_text()),'metrics drift'
    print(json.dumps(dict(validation='PASS',research_status=metrics['research_status'],cases=metrics['total']['cases'],judgments=metrics['total']['judgment_rows'],pairs=metrics['total']['body_pairs_available'],comparable=metrics['total']['documentary_comparable_pairs'],changed=metrics['total']['assessment_change'],unknown=metrics['total']['unknown_pairs'],sources=metrics['sources']['primary_units'],independent_events=metrics['sources']['independent_events'],R0_seal_unchanged=True,candidate_contract_unchanged=True,owned_path_only=True),ensure_ascii=False))

if __name__=='__main__':main()
