#!/usr/bin/env python3
"""Audit AF-RES-030 committed inputs, traceability and table invariants.

Does not run Matplotlib/xarray/DuckDB products, fetch the web or change any
ledger. --receipt saves only this check's result under the owned path.
"""
from pathlib import Path
from datetime import datetime,timedelta,timezone
from collections import Counter
import argparse,csv,hashlib,json,re,subprocess,sys
P=Path(__file__).resolve().parent
ROOT=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
OWN=str(P.relative_to(ROOT))+'/'
BASE='172c6bc37bdf91b91c86b9b3be29cb5b44fa4971'
SEAL='9de54923257d613359348c8ccee2ff8225c8a0d8'
def canonical(p):return p.read_bytes().replace(b'\r\n',b'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def jl(p):return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
checks=[]
def ck(name,ok,evidence):checks.append({'condition':name,'met':bool(ok),'evidence':evidence})
ap=argparse.ArgumentParser();ap.add_argument('--receipt',default='evidence/validation.json');ap.add_argument('--handoff',action='store_true');args=ap.parse_args()
target=(P/args.receipt).resolve();assert P in target.parents,'receipt outside owned path'
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()

changed=subprocess.check_output(['git','diff','--name-only',BASE,'HEAD'],text=True).splitlines()
working=[]
for row in subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],text=True).splitlines():working.append(row[3:])
ck('all committed and working changes stay inside owned_path',all(x.startswith(OWN) for x in changed+working),{'committed_paths':len(changed),'working_paths':working})
dc=subprocess.run(['git','diff','--quiet',BASE,'--','docs/automation/dot-control.json']).returncode
ck('dot-control.json unmodified',dc==0,'git diff --quiet BASE -- docs/automation/dot-control.json')
manifest=json.loads((P/'manifest.json').read_text())
ck('manifest pins actual start and dependency',manifest['base_commit']==BASE and manifest['dependencies']==[{'branch':'work/research-af-res-026','commit':'c6eff012a74451e9882d8d43b6a6e510b4d15225'}] and manifest['allowed_paths']==[OWN], 'manifest.json')
seal=json.loads((P/'evidence/t0-seal.json').read_text())['sha256'];mismatch=[]
for path,expected in seal.items():
 if sha(canonical(ROOT/path))!=expected:mismatch.append(path)
ck('all134 pre-outcome canonical hashes remain sealed',len(seal)==134 and not mismatch,{'count':len(seal),'mismatch':mismatch,'basis':'Git LF canonical text'})

initial=jl(P/'initial.jsonl');A=[r for r in initial if r['sample']=='A'];B=[r for r in initial if r['sample'].startswith('B')];sel=[r for r in B if r['b_selected']]
ck('A24 B80 and selectedB8 distinct roots',len(A)==24 and len(B)==80 and len(sel)==8 and len({r['root_url'] for r in A+B})==104,{'A':len(A),'B_screened':len(B),'B_selected':len(sel)})
strata=Counter((r['project'],r['quarter'].removeprefix('A')) for r in A)
ck('fixed6 strata each4 A roots',len(strata)==6 and set(strata.values())=={4} and {r['quarter'].removeprefix('A') for r in A}=={'2023Q1','2024Q3'},str(dict(strata)))
frame=list(csv.DictReader((P/'frame.csv').open()))
selection_fail=[]
for project,quarter in strata:
 chosen=sorted([r for r in A if r['project']==project and r['quarter'].removeprefix('A')==quarter],key=lambda x:x['created_utc'])
 lo='2023-01-01' if quarter=='2023Q1' else '2024-07-01';hi='2023-04-01' if quarter=='2023Q1' else '2024-10-01'
 eligible={r['root_url']:r for r in frame if r['project']==project and lo<=r['created_utc'][:10]<hi and r['root_eligible'] in ('True','included_A')}
 ordered=sorted(eligible.values(),key=lambda x:x['created_utc'])[:4]
 if [r['root_url'] for r in ordered]!=[r['root_url'] for r in chosen]:selection_fail.append((project,quarter))
ck('A is first4 known eligible roots by creation in each stratum',not selection_fail,{'failed_strata':selection_fail,'metadata_rows':len(frame)})
ck('no outcome-based selection flag',all(r['selected_by_outcome']=='False' for r in frame),'frame.csv selected_by_outcome')
expected=['XB03','DB04','XB06','DB07','XB08','MB09','XB13','XB14']
eligible=sorted([r for r in B if r['b_question_eligible']],key=lambda x:x['b_global_order'])
actual=sorted(sel,key=lambda x:x['b_selection_rank'])
ck('B selected first8 of14 question-positive roots under fixed80 cap',[r['case_id'] for r in actual]==expected and [r['case_id'] for r in eligible[:8]]==expected and len(eligible)==14,{'selected':expected,'eligible':len(eligible),'screened':len(B)})
coverage=set()
for stream in ('matplotlib','xarray','duckdb'):
 for name in ('chains.jsonl','screening-followups.jsonl'):
  for r in jl(P/'streams'/stream/name):coverage.add(r['case_id'])
missing={r['case_id'] for r in B}-coverage
ck('every B screening attempt has a followup audit',not missing,{'B_covered':len({r['case_id'] for r in B}&coverage),'missing':sorted(missing)})

chains=jl(P/'chains.jsonl');cid={r['case_id']:r for r in chains}
ck('all32 selected roots have exactly one chain',len(chains)==32 and set(cid)=={r['case_id'] for r in A+sel},list(cid))
window_errors=[];answer_errors=[]
for r in chains:
 root=dt(r['created_utc']);qmap={q['question_id']:q for q in r['questions']}
 for d in (30,90):
  if dt(r['windows'][f'root{d}_end'])!=root+timedelta(days=d):window_errors.append(r['case_id'])
 for coll in ('questions','answers','executions'):
  for e in r[coll]:
   if not e.get('url') or not e.get('utc'):window_errors.append((r['case_id'],coll,'missing provenance'));continue
   for d in (30,90):
    if e[f'root{d}']!=(root<=dt(e['utc'])<=root+timedelta(days=d)):window_errors.append((r['case_id'],coll,d))
 for a in r['answers']:
  if a['strict_same_variable_existing_answer']:
   q=qmap.get(a['question_id'])
   if not(q and a['is_original_author'] and q['is_information_request_to_original_author'] and dt(a['utc'])>=dt(q['utc']) and a['roundtrip_key']):answer_errors.append((r['case_id'],a['question_id']))
ck('root30/root90 boundaries and event provenance match timestamps',not window_errors,window_errors)
ck('strict answers preserve original author variable link and ordered roundtrip',not answer_errors,answer_errors)
g=json.loads((P/'evidence/denominators.json').read_text())['groups']
expect={'A':{'n':24,'information_question':8,'same_variable_answer':3,'linked_recommendation_change':0,'new_execution_success':4,'new_execution_failure':1,'full_goal_success':2,'strict_answer_roundtrips':3,'any_author_reply_roundtrips':6,'question_utterances':8,'question_episodes':8,'question_variables':9},'B':{'n':8,'information_question':7,'same_variable_answer':6,'linked_recommendation_change':0,'new_execution_success':1,'new_execution_failure':1,'full_goal_success':1,'strict_answer_roundtrips':7,'any_author_reply_roundtrips':9,'question_utterances':10,'question_episodes':9,'question_variables':11}}
for sample,ex in expect.items():
 diffs={k:[g[sample+'_all'].get(k),v] for k,v in ex.items() if g[sample+'_all'].get(k)!=v}
 ck(sample+' denominators agree with independent stream recount',not diffs,{'expected':ex,'differences':diffs,'independent_evidence':'evidence/independent-review.json'})
 for r in [x for x in chains if x['sample']==sample]:
  for w in ('root30','root90'):
   keys=[x['roundtrip_key'] for x in r['answers'] if x[w] and x['strict_same_variable_existing_answer']]
   ck(r['case_id']+' '+w+' strict roundtrips not variable duplicates',len(set(keys))==r[w]['strict_answer_roundtrips'],list(set(keys)))
ck('late XB06 kept out of primary/90-day counts',not cid['XB06']['root30']['information_question'] and not cid['XB06']['root90']['information_question'] and cid['XB06']['first_information_question'],'XB06 original and late event timestamps')
ck('no retrospective late execution added to root90',g['A_all']['root90_same_metrics'] and g['B_all']['root90_same_metrics'],'root90 metric flags same; late_history retained separately')
ck('future exposure6 and whole-original0 disclosed',sum(r['exposure_effective'] for r in chains)==6 and all(r['original_grade']!='O' for r in chains),{'exposed':[r['case_id'] for r in chains if r['exposure_effective']],'whole_original':0})

sources=jl(P/'sources.jsonl');sc=json.loads((P/'evidence/source-counts.json').read_text())
ck('source canonical keys unique',len(sources)==201 and len({r['canonical_key'] for r in sources})==201,len(sources))
ck('source ledger digest matches receipt',sha((P/'sources.jsonl').read_bytes())==sc['sources_jsonl_sha256'],sc['sources_jsonl_sha256'])
required_fields=['source_id','type','publisher','url','version','checked_utc','sections','observed','limitations','linked_Q_cases','duplicate_group','count_minimum']
bad_source=[r['source_id'] for r in sources if any(not r.get(k) for k in required_fields if k!='count_minimum') or not isinstance(r.get('count_minimum'),bool)]
ck('all originals have provenance sections findings and limitations',not bad_source,bad_source)
ck('at least36 including A24 official8 and cross2perdomain',sc['counts']['required_minimum_qualified_unique']==46 and sc['counts']['A_threads']==24 and sc['counts']['official_contemporaneous_manual_test_decision_qualified']>=8 and sc['counts']['cross_library_reference']>=2 and sc['counts']['cross_public_statistics']>=2,sc['counts'])
ck('all source compiler acceptance conditions hold',all(x['met'] for x in sc['conditions']),'evidence/source-counts.json conditions')
ck('minimum does not use B screening frame-only failures or searches',all(r['category'] in ('A_thread','official_provider','cross_library_reference','cross_public_statistics') and r['direct_read'] for r in sources if r['count_minimum']),[r['source_id'] for r in sources if r['count_minimum']])
input_bad=[p for p,h in sc['input_sha256'].items() if sha(canonical(P/p))!=h]
ck('source inputs reproduce canonical LF hashes',not input_bad,input_bad)

old=list(csv.DictReader((P/'comparisons.csv').open()));new=list(csv.DictReader((P/'comparison-results.csv').open()))
ck('presealed comparison pairs unchanged and unmatched retained',len(old)==8 and len(new)==8 and sum(x['comparison_case']!='해당 없음' for x in new)==5 and [(x['question_case'],x['comparison_case']) for x in old]==[(x['question_case'],x['comparison_case']) for x in new] and all(x['question_case']!='X02' for x in new),'comparisons.csv vs comparison-results.csv')
wait=list(csv.DictReader((P/'wait-audit.csv').open()))
ck('wait audit separates18 primary and1 late utterance',len(wait)==19 and sum(x['root30_question']=='True' for x in wait)==18,'wait-audit.csv')
ck('edited answers preserve waiting ranges',all(float(next(x for x in wait if x['question_id']==qid)['reply_latest_from_question_creation_hours'])>float(next(x for x in wait if x['question_id']==qid)['reply_wait_creation_hours']) for qid in ['D02-Q1','XB13-input','XB14-backend-and-remote']),'wait-audit.csv D02 XB13 XB14')

result=(P/'RESULT.md').read_text();lines=result.splitlines()
headers=[ '| 사례 ID·A/B·시각 | 최초 목적·이미 있는 값과 URL | 실제 질문·변수·URL | 작성자 값·시각·URL | 이전/이후 후보·용도·근거 | 당사자 행동·미확인 |', '| 표본·제외 기준 | 분모 단위·수 | 이미 있던 값 | 같은 변수 직접 답 | 연결된 권고 변경 | 새 실행 성공/실패 | 무응답·관측 불능 | 왕복·대기 범위 |', '| 짝 ID·선정 기준 | 묻기/즉답/조건부 원문 | 판·목적·정보량의 차이 | 공식 지지 | 실제 후속 | 결론이 깨지는 조건·미확인 |']
ck('RESULT starts immediately with required table and preserves order',lines[2]==headers[0] and all(x in result for x in headers) and result.index(headers[0])<result.index(headers[1])<result.index(headers[2]),headers)
firstrows=[]
for line in lines[4:]:
 if not line.startswith('|'):break
 firstrows.append(line)
ck('first required table contains all32 cases once',len(firstrows)==32 and {line.split('|')[1].strip().split(' · ')[0] for line in firstrows}==set(cid),{'rows':len(firstrows)})
weak='| 가장 중요한 불일치 또는 약점 | 근거 URL | 영향을 받는 판단 | 다음 조사 제안·첫 자료 |'
docs=['RESULT.md']+(['HANDOFF.md'] if args.handoff else [])
for name in docs:
 txt=(P/name).read_text();tail=txt[txt.rfind(weak):].strip().splitlines() if weak in txt else []
 ck(name+' ends with exactly3 weakness rows',len(tail)==5 and all(x.startswith('|') for x in tail),{'tail_line_count':len(tail)})
ck('SELF_CHECK has Q1-Q8 five-column audit rows',all('| Q'+str(i)+'.' in (P/'SELF_CHECK.md').read_text() for i in range(1,9)),'SELF_CHECK.md Q별 주장·반증 원장')
links=re.findall(r'\]\(([^)]+)\)',result);broken=[]
for link in links:
 if not re.match(r'^(https?:|#)',link):
  if not (P/link.split('#')[0]).exists():broken.append(link)
ck('RESULT local evidence links exist',not broken,broken)
review=json.loads((P/'evidence/result-review.json').read_text())
ck('separate report review retained',bool(review),'evidence/result-review.json; resolutions recorded separately')
required=['SCOPE.md','manifest.json','frame.csv','initial.jsonl','questions.csv','chains.jsonl','comparisons.csv','sources.jsonl','RESULT.md','SELF_CHECK.md','PROGRESS.md','PENDING_EXECUTIONS.md']
ck('required working deliverables exist',all((P/x).exists() for x in required),required)

inputs={}
for f in required+['build_analysis.py','build_sources.py','build_result.py','verify.py','analysis.csv','question-audit.csv','wait-audit.csv','comparison-results.csv','sensitivity.csv','evidence/denominators.json','evidence/source-counts.json','evidence/t0-seal.json','evidence/independent-review.json','evidence/result-review.json']:
 inputs[f]=sha(canonical(P/f))
if args.handoff:inputs['HANDOFF.md']=sha(canonical(P/'HANDOFF.md'))
passed=all(x['met'] for x in checks)
receipt={'schema':'AF-RES-030-validation-v1','checked_utc':datetime.now(timezone.utc).isoformat(),'target_head':head,
 'target_kind':'HEAD plus explicitly hashed working input files','base_sha':BASE,'t0_seal_sha':SEAL,
 'command':'PYTHONDONTWRITEBYTECODE=1 python '+OWN+'verify.py '+ ' '.join(sys.argv[1:]),
 'input_hash_basis':'UTF-8 text with CRLF normalized to LF, matching repository gitattributes','input_sha256':inputs,
 'checks':checks,'checks_passed':sum(x['met'] for x in checks),'checks_total':len(checks),'exit_code':0 if passed else 1,
 'technical_product_execution':False,'network_used_by_this_script':False}
target.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'target_head':head,'passed':receipt['checks_passed'],'total':len(checks),'exit_code':receipt['exit_code'],'failed':[x for x in checks if not x['met']]},ensure_ascii=False))
sys.exit(receipt['exit_code'])
