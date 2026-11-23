#!/usr/bin/env python3
"""Task-specific evidence checks; never executes author tools or participant code."""
import argparse
import csv
import datetime
import json
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent
REPO = P.parents[3]
OWNED = 'docs/workstreams/research/AF-RES-050/'
BASE = '522ea9092d4d56ef6db0bd4f707bfc90032e179e'
ap=argparse.ArgumentParser(); ap.add_argument('--documents',action='store_true'); args=ap.parse_args()
errors=[]; checks=[]
def verify(name,condition,detail):
    checks.append({'check':name,'passed':bool(condition),'detail':detail})
    if not condition:errors.append(name)
def csvread(name):
    with (P/name).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
sources=[json.loads(l) for l in (P/'sources.jsonl').read_text().splitlines()]
ids={d['source_id'] for d in sources}; studies=csvread('studies.csv'); joins=csvread('joins.csv'); outcomes=csvread('outcomes.csv')
J={d['join_id']:d for d in joins}; O={d['outcome_id']:d for d in outcomes}
verify('unique_source_ids',len(ids)==len(sources),len(sources))
verify('fixed8retained',{d['study_id'] for d in studies}=={'S01','S02','S03','S04','S05','S06','X01','X02'},len(studies))
verify('software_denominator6',sum(d['stratum']=='software-primary' for d in studies)==6,'cross-domain rows excluded from software family denominator')
for tab in [studies,joins,outcomes]:
    for d in tab:
        refs=json.loads(d['source_ids'])
        verify('source_references:'+str(d.get('join_id',d.get('outcome_id',d.get('study_id')))),all(x in ids for x in refs),refs)
for d in sources:
    verify('source_metadata:'+d['source_id'],bool(d['url'] and d['checked_at_utc']!='미확인' and d['locator']!='미확인' and d['question_ids']),d['record_origin'])
    verify('failed_not_counted:'+d['source_id'],d['direct_read'] or not(d['quota_count'] or d['substantive_unique_primary_count']),d['status'])
count=json.loads((P/'evidence/source-counts.json').read_text())
verify('quota_unique_work_dedup',len({d['duplicate_group'] for d in sources if d['substantive_unique_primary_count']})==count['unique_substantive_primary_works_read'],count['unique_substantive_primary_works_read'])
verify('quota_tier_shortfalls_explicit',count['quota']['author_supplement']['shortfall']==4 and count['quota']['task_implementation']['shortfall']==3 and count['filled_quota_slots']==17,count['quota'])
audit=json.loads((P/'streams/ncq-exoa/ncq-row-audit.json').read_text())
for i,a in enumerate(audit['files'],1):
    row=J['J-NA-0'+str(i)]
    verify('NCQfilecount:'+str(i),int(row['input_rows'])==a['data_records'] and int(row['key_unique_count'])==a['distinct_P_T'],a['file'])
    verify('NCQduplicate_basis:'+str(i),int(row['exact_duplicate_records'])==a['exact_duplicate_full_records'] and int(row['key_nonunique_excess'])==a['non_unique_P_T_excess_records'] and row['duplicate_groups']!='0','normal1:N is not exact-row duplication')
    verify('NCQunknown_joint_rows:'+str(i),row['joined_rows']=='미확인' and row['left_unmatched']=='미확인','missing join not rewritten as0')
verify('NCQsame_people',all('same10' in O[x]['denominator'] for x in ['O-NA-01','O-NA-02','O-NA-03']),'same10, not20independent people')
verify('exoa_cap_preserved',all('40minutes whole4-task' in O['O-NA-0'+str(i)]['time_limit'] for i in range(4,9)),'whole-session cap')
verify('exoa_timing_n_not_pass_n','n not given' in O['O-NA-04']['denominator'],'no successful-count substitution')
verify('blueprint_completer_denominator','E9/C8' in O['BC-O02']['denominator'] and 'E10/C10' in O['BC-O02']['denominator'],'finishers versus all assigned')
verify('blueprint_quality_separate',O['BC-O04A']['endpoint']!=O['BC-O04B']['endpoint'] and O['BC-O04B']['treatment']=='94' and O['BC-O04B']['control']=='116','two separate tasks/ranks')
verify('codemend_planned_not_observed','planned E60/C60' in O['BC-O06']['denominator'] and 'actual attempts 미확인' in O['BC-O06']['denominator'],O['BC-O06']['denominator'])
verify('strata_aggregate_only',J['J-US-AGG']['joined_rows']=='6' and 'NOT participant' in J['J-US-AGG']['unit'] and '1:1' in J['J-US-AGG']['cardinality'],'6published condition×task means')
verify('no_numeric_activity_claim',all('미확인' in d['activity_time'] for d in outcomes),'known partial interaction fraction not whole labor')
paths=subprocess.check_output(['git','diff','--name-only',BASE],cwd=REPO,text=True).splitlines()
paths+=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=REPO,text=True).splitlines()
verify('owned_path_only',all(x.startswith(OWNED) for x in paths),{'checked_paths':len(set(paths))})
doc_locations={}
if args.documents:
    required=['RESULT.md','SELF_CHECK.md','evidence/acceptance-evidence.json']
    for f in required:verify('required_document:'+f,(P/f).exists(),f)
    text=(P/'RESULT.md').read_text();lines=text.splitlines()
    h1='| 연구군·층 | 과제·배정 단위 | 링크·설명의 차이 | 배정 인원·시행 | 시간 시작·종료·단위 | 품질 기준 | 원자료 URL·파일·키 | 연결된 행/대상 행 | 미확인 |'
    h2='| 연구·비교 조건 | 비교 가능 단위·분모 | 선택시간 | 총 과제시간 | 활동시간 | 품질·실패·제한시간 | 추정치·불확실성 또는 미산출 이유 | 반증·근거 주소 |'
    h3='| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀌는 조건 |'
    verify('required_table_headers',h1 in lines and h2 in lines and h3 in lines,'exact user headers')
    verify('starts_with_tables',lines[0]==h1 and lines.index(h2)<35,'no preamble before required tables')
    if h3 in lines:
        tail=[l for l in lines[lines.index(h3)+2:] if l.strip()]
        verify('exactly3finalweaknesses',len(tail)==3 and all(l.startswith('|') for l in tail),len(tail))
    verify('questionsQ1toQ7',all('Q'+str(n) in text and 'Q'+str(n) in (P/'SELF_CHECK.md').read_text() for n in range(1,8)),'all addressed')
    verify('partial_quota_visible','17/24' in text and '부분' in text,'not claiming full acceptance')
    doc_locations={k:lines.index(h)+1 for k,h in [('required_table1_line',h1),('required_table2_line',h2),('final_weakness_table_line',h3)] if h in lines}
report={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'documents' if args.documents else 'ledgers','status':'pass' if not errors else 'fail','exit_code':0 if not errors else 1,'errors':errors,'checks':checks,'document_locations':doc_locations,'scope':'structural/semantic consistency of published evidence artifacts; not a replication of study effects'}
out=P/'evidence'/('validation-documents.json' if args.documents else 'validation-ledgers.json');out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':report['status'],'checks':len(checks),'errors':errors,'document_locations':doc_locations,'output':str(out.relative_to(REPO))},ensure_ascii=False))
raise SystemExit(report['exit_code'])
