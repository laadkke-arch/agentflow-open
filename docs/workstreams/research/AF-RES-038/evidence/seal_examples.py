"""Freeze authored examples and blind reading input BEFORE separate-context grading.
Do not rerun after grading without preserving the prior seal and explaining the change.
"""
from pathlib import Path
import csv, json, hashlib, random
from datetime import datetime, timezone

B = Path(__file__).resolve().parents[1]
if (B/'evidence/blind-observed.json').exists():
    raise SystemExit('An observed grade exists; do not overwrite pre-grade inputs.')
pc = json.loads((B/'streams/pandas/cases.json').read_text())['cases']
nc = json.loads((B/'streams/numpy/cases.json').read_text())
src = {s['source_id']:s for s in [json.loads(x) for x in (B/'sources.jsonl').read_text().splitlines() if x.strip()]}
def urls(ids):
    return [src[i]['pinned_url_or_version'] for i in ids]
def jwrite(path,x):
    path.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def masked(s):
    replacements={'C/C++/Cython':'native','CPython':'언어 구현','Python':'호스트 언어','setup.py':'통합 빌드 스크립트','setup 스크립트':'통합 빌드 스크립트','numpy':'배열 라이브러리','NumPy':'배열 라이브러리','pandas':'테이블 라이브러리','CMake':'빌드 도구','Meson':'빌드 도구','setuptools':'패키징 도구','PEP517':'표준 frontend/backend','Series':'컨테이너'}
    for old,new in replacements.items():s=s.replace(old,new)
    return s

rubric=[]
examples=[]
for c in pc:
    for r in c['requirements']:
        rubric.append({'case_id':c['case_id'],'case_kind':c['kind'],'requirement_id':r['id'],
          'original_requirement':r['original_requirement'],'original_url':c['initial_url'],
          'original_locator':r['original_locator'],'original_created_or_event':c['historical_frame']['formal_proposal'],
          'origin_kind':r['origin_kind'],'t0_prompt':r['t0_prompt'],'t1_probe':r['t1_probe'],
          'pass':r['pass'],'partial':r['partial'],'fail':r['fail'],'fatal_violation':r['fatal'],
          'allowed_alternatives':' | '.join(a['name_for_grader'] for a in c['allowed_alternatives']),
          'alternative_urls':json.dumps([u for a in c['allowed_alternatives'] for u in a['evidence_urls']],ensure_ascii=False),
          'criterion_urls':json.dumps(urls(r['criterion_sources']),ensure_ascii=False),
          'criterion_locators':' | '.join(src[i]['locator'] for i in r['criterion_sources']),
          'same_original_requirement_t1':True,'new_requirement_excluded':json.dumps(c['new_requirement_excluded'],ensure_ascii=False),
          'independence_limit':c['criterion_independence']})
    for e in c['examples']:
        alternative=next((a for a in c['allowed_alternatives'] if a['id']==e['alternative']),None)
        examples.append({'record_kind':'AUTHOR_CREATED_TWO_PHASE_EXAMPLE_NOT_A_PERSON',
          'case_id':c['case_id'],'submission_id':e['id'],'alternative_id':e['alternative'],
          't0_decision':masked(e['blinded_submission']).split('재검')[0] if c['case_id']=='P04' else masked(e['blinded_submission']),
          'joint_t0_t1_evidence_text':masked(e['blinded_submission']),
          'phase_note':'한 설명 안의 최초 설계와 명시된 재검 응답을 함께 판독한다. 이는 실제 시간순 참가자 로그가 아니라 사전에 작성한 두 시점 증거 vignette다.',
          'first_declaration_utc':None,'t0_active_seconds':None,'t1_active_seconds':None,'repair_seconds':None,
          'expected_before_grade':{'overall':e['expected'],'requirements':e['expected_requirements'],'major_error':e['expected']=='fail','t1_action':e['t1_expected_action']},
          'source_urls':alternative['evidence_urls'] if alternative else [c['initial_url']],
          'counterexample_role':e['counterexample_role'],
          'author_self_read':{'reader':'root','overall':e['expected'],'requirements':e['expected_requirements'],'basis':'공통 원요구와 제출의 동작을 직접 대조; 역사적 software 실행 아님'},
          'separate_context_observed':None,'adjudication':None,'external_human_validated':False})

for i,r in enumerate(nc['requirements']):
    rubric.append({'case_id':'N08','case_kind':'whole_bounded_workflow','requirement_id':r['id'],
      'original_requirement':r['requirement'],'original_url':r['source_url'],'original_locator':r['locator'],
      'original_created_or_event':'formal document2010-04-27; git2010-04-29; prior discussion2010-04-10',
      'origin_kind':r.get('inference_note',r.get('operationalization','원판 use-case 요구')),
      't0_prompt':r['t0'],'t1_probe':r['t1'],'pass':r['acceptance'],
      'partial':'요구 일부만 실현되거나 근거가 불충분한 경우. 구체적 위반은 fail. 같은 원인의 파급은 사건수 중복하지 않는다.',
      'fail':r['fatal_violation'],'fatal_violation':True,
      'allowed_alternatives':'동일 순열로 키/값 정렬+그룹 감소 | 고유키 역색인+원행 선택+그룹 감소',
      'alternative_urls':json.dumps(urls(['N-S02','N-S03','N-S04']),ensure_ascii=False),
      'criterion_urls':json.dumps(r['criterion_urls'],ensure_ascii=False),'criterion_locators':'원문 URL의 행 앵커; 구성요소 시험과 산술 참조',
      'same_original_requirement_t1':True,'new_requirement_excluded':'빈 그룹·NA·연도경계·성능·새 ufunc/API 정책',
      'independence_limit':'기준은 다른 NumPy 파일/공개 시험이나 같은 프로젝트. 구매행과 기대 숫자는 작성자 구성; 별도 사람 실행 없음.'})
for e in nc['examples']:
    expected=e['expected']
    self_req=dict(expected['requirements'])
    if e['submission_id']=='N08-E3':self_req['N08-R2']='fail'
    examples.append({'record_kind':'AUTHOR_CREATED_TWO_PHASE_EXAMPLE_NOT_A_PERSON','case_id':'N08','submission_id':e['submission_id'],
      'alternative_id':e['alternative_id'],'t0_decision':e['blind_text'],'joint_t0_t1_evidence_text':e['blind_text'],
      't0_outputs':e.get('t0_computed_outputs',nc['references']['t0_expected']),
      't1_outputs':e.get('t1_computed_outputs',nc['references']['t1_expected']),
      'phase_note':'같은 고정 의사코드의 t0/t1 출력; 입력행만 재배열. 원판의 구매 데이터나 실제 참가자 제출이 아니라 작성자 산술 예시.',
      'first_declaration_utc':None,'t0_active_seconds':None,'t1_active_seconds':None,'repair_seconds':None,
      'expected_before_grade':{**expected,'t1_action':e['expected_t1']},'source_urls':urls(e['reference_sources']),
      'counterexample_role':e['unmasked_label'],'author_self_read':{'reader':'root','overall':expected['overall'],'requirements':self_req,
        'basis':'의사코드와 그룹 숫자 대조. N08-E3 R2는 실제 완성 출력이 틀렸으므로 self fail; 원 작성자 expected partial을 덮어쓰지 않음.'},
      'separate_context_observed':None,'adjudication':None,'external_human_validated':False})

with (B/'rubric.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rubric[0]),lineterminator='\n');w.writeheader();w.writerows(rubric)
(B/'examples.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in examples))

case_alias={'P02':'K7','P04':'M2','P06':'R9','N08':'V4'}
blind_cases=[]
for cid in case_alias:
    rr=[r for r in rubric if r['case_id']==cid]
    req=[{'id':f'R{i+1}','requirement':masked(r['original_requirement']),'pass_condition':masked(r['pass']),
          'scope':'원 요구의 설계/행동 합치성을 판독. 실행하지 않은 성공을 가정하지 않되 이 문서 과제의 pass를 실제 실행 성공 증명과 동일시하지 않음.'} for i,r in enumerate(rr)]
    context={'case_key':case_alias[cid],'requirements':req}
    if cid=='P02':context['context']='컴파일 대상·의존·생성 규칙을 graph 또는 동등 구조로 분리하고 metadata/배포 책임을 연결한다. 파일 이름/개수와 특정 제품은 기준 아님. 개발 및 unpacked source archive 경로가 병렬 컴파일과 표준 wheel/source archive 계약에 도달하는지 추적. 새 실제 target 구현 불필요. 설계와 검증 계획만 평가.'
    elif cid=='P04':context.update(context='batch마다 explicit 또는 첫 nonmissing 행에서 확정한 한 형식을 유지하고 raise 정책을 적용. 고정 MDY가 13-01에서 정당하게 오류를 내도 허용. 결과 컨테이너/속도는 기준 아님.',t0_inputs=['01-01-2000 00:00:00','02-01-2000 00:00:00'],t1_inputs=[['12-01-2000 00:00:00','13-01-2000 00:00:00'],['12-01-2000 00:00:00','01-13-2000 00:00:00']])
    elif cid=='P06':context.update(context='생성 때 native 또는 nullable 64-bit 정수 schema를 선택해 명시 가능. 그 이후에는 선언 dtype을 유지. 작은 scalar 정수/whole float/fractional float/text만 범위. NA/overflow/bool/vector 제외. 매 probe는 [1,2,3]에서 독립 시작.',t0_probes=['index0=4 (integer)','index1=2.0 (float)'],t1_probes=['index1=3.0 (float)','index1=1.5 (float)',"index1='potage' (text)"])
    else:context.update(context='단일년의 관측된 비어있지 않은 그룹. 월 또는 연월 키 둘 다 허용. 원행-키 소속과 네 집계의 완성 출력 평가. 행순서 외 새 조건 없음.',t0_inputs=nc['t0']['records'],t1_inputs=nc['t1']['records'])
    blind_cases.append(context)

rng=random.Random('AF-RES-038-BLIND-SEAL-V1')
ordered=list(examples);rng.shuffle(ordered)
blind_samples=[];mapping=[]
for idx,e in enumerate(ordered):
    anon=f'S{(idx+1)*7+103}'
    row={'submission_key':anon,'case_key':case_alias[e['case_id']],
         'evidence':e['joint_t0_t1_evidence_text'],'phase_note':e['phase_note']}
    if e['case_id']=='N08':
        # Remove row-assignment helper annotations; leave only submitted grouped numbers.
        def public_output(groups):
            return [{'grouping':g['grouping'],'key_field':g['key_field'],'groups':[{k:v for k,v in item.items() if k not in ('row_ids','row_ids_actually_used')} for item in g['groups']]} for g in groups]
        row['t0_submitted_outputs']=public_output(e['t0_outputs'])
        row['t1_submitted_outputs']=public_output(e['t1_outputs'])
    blind_samples.append(row);mapping.append({'submission_key':anon,'submission_id':e['submission_id'],'case_key':case_alias[e['case_id']],'case_id':e['case_id']})

payload={'kind':'BLIND_DOCUMENT_READING_NOT_HUMAN_EXPERIMENT','rater_instruction':'도구/군명·기대 정답은 제공하지 않는다. 요구와 제출 행동만 판독한다. 각 R1~R3를 pass/partial/fail/unverified로 기록하고 근거 문구 또는 계산을 붙인다. pass는 모두 충족, partial은 일부만 실현/확인, fail은 구체적 위반, unverified는 근거 없음. 전체 pass는 필수 모두 pass. 중대 위반 및 t1 같은 원요구 수정/수정불필요/미확인을 별도로 기록. 같은 원인의 다중 요구 파급을 독립 수정사건으로 중복 계수하지 않는다. 외부 원문 직접 재검이나 software 실행은 이 입력만으로 주장하지 않는다. 답안의 이름이나 속도 추측을 기준으로 삼지 않는다.',
         'cases':blind_cases,'submissions':blind_samples,
         'requested_output':'JSON object: reviewer_scope, outside_files_read, human_validation=false, grades[submission_key,case_key,requirements{R1:...,R2:...,R3:...},overall,major_error,evidence{R1:...,R2:...,R3:...},t1_action,uncertainty,arm_guess], cross_case_observations'}
jwrite(B/'evidence/blind-input.json',payload)
jwrite(B/'evidence/blind-key.json',{'audience':'AUTHOR_ONLY_NOT_FOR_BLIND_READER','mapping':mapping})
keys=[{'submission_id':e['submission_id'],'expected_before_grade':e['expected_before_grade']} for e in examples]
jwrite(B/'evidence/expected-before-grading.json',keys)
inputs=['evidence/blind-input.json','evidence/blind-key.json','evidence/expected-before-grading.json','rubric.csv','examples.jsonl']
hashes={p:hashlib.sha256((B/p).read_bytes()).hexdigest() for p in inputs}
jwrite(B/'evidence/grade-seal.json',{'sealed_utc':datetime.now(timezone.utc).isoformat(),'method':'authored before separate-context reading','input_hashes':hashes,'case_count':4,'example_count':12,'required_cells':36,'human_count':0,'reader_prior_context':'only measurement protocol v1 and run-config v1; no case/source/example files','access_rule':'reader may read blind-input.json and its own output only; instruction separation, not OS file permissions','preexisting_author_disagreement':'N08-E3 R2 expected partial; root self-read fail. Preserved before independent result.'})
print(json.dumps({'rubric_rows':len(rubric),'examples':len(examples),'blind_samples':len(blind_samples),'seal':hashes['evidence/blind-input.json']},ensure_ascii=False))
