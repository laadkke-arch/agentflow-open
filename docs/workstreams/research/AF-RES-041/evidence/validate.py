"""Required evidence/format gates; not a test of historical causality."""
from collections import Counter
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
REPO=next(parent for parent in ROOT.parents if (parent/'.git').exists())
OWNED='docs/workstreams/research/AF-RES-041/'
EXPECTED_BASE='333e83c9a46b0c005d22efcccbb5a055b27e904e'
REQUIRED='source_id original_url pinned_url_or_version publisher event_or_publication_date checked_utc locator source_kind verified_fact limitation question_ids case_ids duplicate_group counted'.split()
checks=[]
def check(name,passed,detail):checks.append(dict(check=name,passed=bool(passed),detail=detail))
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO,text=True).strip()
rows=[json.loads(line) for line in (ROOT/'sources.jsonl').read_text().splitlines() if line.strip()]
ids=[r['source_id'] for r in rows]
counted=[r for r in rows if r['counted']]
groups=[r['duplicate_group'] for r in counted]
cats=Counter(r['quota_category'] for r in counted)
missing=[(r['source_id'],key) for r in rows for key in REQUIRED if key not in r]
check('required_source_fields',not missing,missing)
check('unique_source_ids',len(ids)==len(set(ids)),len(ids))
check('one_count_per_work',len(groups)==len(set(groups)),dict(Counter(groups)))
check('minimum_22_unique_works',len(counted)>=22,len(counted))
for category,required in [('printing_background',4),('music_background',4),('recipient',8),('bibliography',3),('counter',3)]:
    check('quota_'+category,cats[category]>=required,dict(observed=cats[category],required=required))
recipient={case:sum(r['quota_category']=='recipient' and case in r['case_ids'] for r in counted) for case in ['B01','B03']}
check('each_project_at_least_three',all(n>=3 for n in recipient.values()),recipient)
check('counted_primary_not_failed',not [r['source_id'] for r in counted if any(t in r['source_kind'] for t in ['access_failure','discovery_index','self_recheck'])], 'failed/repeated/navigation ranges excluded')

table_data=json.loads((ROOT/'evidence/table-data.json').read_text())
csv_counts={}
for name,expected in table_data.items():
    actual=list(csv.DictReader((ROOT/(name+'.csv')).open()))
    csv_counts[name]=len(actual)
    check('csv_exact_'+name,actual==expected,dict(rows=len(actual),columns=len(actual[0]) if actual else 0))
    unresolved=[]
    for row in actual:
        for source_id in row.get('source_ids','').split(';'):
            if source_id not in ['','미확인','해당 없음'] and source_id not in ids:unresolved.append(source_id)
    check('source_refs_'+name,not unresolved,unresolved)
judgments=list(csv.DictReader((ROOT/'judgments.csv').open()))
check('four_pre_registered_judgments',{r['judgment_id'] for r in judgments}=={'B01-I','B01-C','B03-I','B03-C'} and len(judgments)==4,[r['judgment_id'] for r in judgments])
contacts=['exact_donor','available_then','author_link','change_same_baseline','same_purpose_reflection']
check('twenty_contact_states',all(r[c] in ['참','거짓','미확인'] for r in judgments for c in contacts),Counter(r[c] for r in judgments for c in contacts))
counts={suffix:dict(numerator=sum(r['complete_count']=='1' for r in judgments if r['judgment_id'].endswith(suffix)),denominator=sum(r['judgment_id'].endswith(suffix) for r in judgments)) for suffix in ['I','C']}
check('paired_denominators',counts['I']=={'numerator':0,'denominator':2} and counts['C']=={'numerator':0,'denominator':2},counts)
check('deletion_and_sensitivity_recorded',all(r['deleted_contact']==('author_link' if r['case_id']=='B01' else 'exact_donor') and r['deletion_complete_count']=='0' and r['retrospective_allowed_grade'] and r['code_baseline_sensitivity'] for r in judgments),'same-task self-check')

result=(ROOT/'RESULT.md').read_text();lines=result.splitlines()
blocks=[];active=[]
for line_number,line in enumerate(lines,1):
    if line.startswith('|'):active.append((line_number,line))
    elif active:blocks.append(active);active=[]
if active:blocks.append(active)
headers1=['사건·기준선','변경 전 선택·시점','특정 원전·판·쪽 URL','저자의 연결 발언 URL·날짜','달라진 선택·동일 목적 반영 URL','사슬 판정','미확인 접점']
headers2=['사건·독자에게 줄 용도','원전 조작과 구현 조작','찬성 근거 URL·위치','반대 근거 URL·위치','깨지는 조건','반환 카드와 근거 강도']
headers3=['중요한 불일치·약점','영향받는 판단과 근거 URL·행','다음 최소 조사·첫 자료','결과가 달라지는 조건']
def cells(line):return [x.strip() for x in line.strip('|').split('|')]
check('table1_immediately_after_title',len(blocks[0])==6 and cells(blocks[0][0][1])==headers1 and all(not line.strip() for line in lines[1:blocks[0][0][0]-1]),dict(start=blocks[0][0][0],end=blocks[0][-1][0],rows=len(blocks[0])-2))
check('table2_two_cases',len(blocks[1])==4 and cells(blocks[1][0][1])==headers2,dict(start=blocks[1][0][0],end=blocks[1][-1][0],rows=len(blocks[1])-2))
check('ends_with_exactly_three_weaknesses',len(blocks[-1])==5 and cells(blocks[-1][0][1])==headers3 and result.rstrip().endswith(blocks[-1][-1][1]),dict(start=blocks[-1][0][0],end=blocks[-1][-1][0],rows=len(blocks[-1])-2))
cards=(ROOT/'cards.md').read_text();parts=re.split(r'^## ',cards,flags=re.M)[1:]
check('two_cards_two_external_links_each',len(parts)==2 and all(len(re.findall(r'\]\(https?://[^)]+\)',part))==2 for part in parts),[len(re.findall(r'\]\(https?://[^)]+\)',part)) for part in parts])
self_check=(ROOT/'SELF_CHECK.md').read_text()
check('Q1_through_Q7_selfcheck',all('| '+q+' ' in self_check for q in ['Q1','Q2','Q3','Q4','Q5','Q6','Q7']),'each question has source/locator, counterattempt, unknown and reversal condition')
check('unknown_zero_eligible_not_rate','0/0; 비율 **해당 없음**' in result and all(r['first_exposure']=='미확인' and r['current_explorer_retrievability']=='미확인' for r in judgments),'0 eligible exact pairs; no general adoption-rate estimate')

registered=git('show','-s','--format=%cI','2021e2f236d56073125d940fafe158d2e6ea5c70')
first=min(datetime.fromisoformat(r['checked_utc'].replace('Z','+00:00')) for r in counted)
check('registration_before_counted_readings',datetime.fromisoformat(registered)<first,dict(registration=registered,first_counted_reading=first.isoformat()))
scope_blob=git('hash-object',str(ROOT/'SCOPE.md'))
check('scope_v1_unchanged',scope_blob=='d6ad4b3d8a709749c7cf8c3fc862f2923776fc04',scope_blob)
committed=git('diff','--name-only',EXPECTED_BASE,'HEAD').splitlines()
dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=REPO,text=True).splitlines()
outside=[p for p in committed if p and not p.startswith(OWNED)]
outside += [line[3:] for line in dirty if line and not line[3:].startswith(OWNED)]
check('only_owned_paths',not outside,outside)
check('assigned_branch',git('branch','--show-current')=='work/research-af-res-041',git('branch','--show-current'))
receipts=json.loads((ROOT/'evidence/final-recheck-downloads.json').read_text())
check('core_URLs_reopened_after_result_draft',len(receipts)==9 and all(r['access'].startswith('success') for r in receipts),dict(successes=sum(r['access'].startswith('success') for r in receipts),total=len(receipts),first=receipts[0]['checked_utc'],last=receipts[-1]['checked_utc']))
check('root_locator_reread_record',(ROOT/'evidence/root-recheck.md').exists(),'same-task self-review, not independent replication')
check('three_research_bundle_commits',all(git('merge-base','--is-ancestor',sha,'HEAD')=='' for sha in ['2021e2f236d56073125d940fafe158d2e6ea5c70','ec22461ac03b7d7d6cc11a34db0b474dcb23fcd5','45b4aa76809cf023d82a3f286b5eb0041d6c1656']),'bundle4=result commit; final HANDOFF follows fixed-SHA/session checks')
report=dict(checked_utc=datetime.now(timezone.utc).isoformat(),passed=all(c['passed'] for c in checks),scope='record/format/reference/scope checks; no historical causal proof or historical runtime',
 reading_ranges=len(rows),unique_counted_works=len(counted),categories=dict(cats),recipient_by_case=recipient,csv_rows=csv_counts,
 contact_state_counts=dict(Counter(r[c] for r in judgments for c in contacts)),case_counts=counts,
 result_tables=dict(table1=[blocks[0][0][0],blocks[0][-1][0]],table2=[blocks[1][0][0],blocks[1][-1][0]],weaknesses=[blocks[-1][0][0],blocks[-1][-1][0]]),checks=checks)
(ROOT/'evidence/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({key:report[key] for key in ['passed','reading_ranges','unique_counted_works','categories','csv_rows','contact_state_counts','result_tables']},ensure_ascii=False))
if not report['passed']:
    print(json.dumps([c for c in checks if not c['passed']],ensure_ascii=False,indent=2))
    raise SystemExit(1)
