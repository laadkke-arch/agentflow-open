"""Preserve first blind observations; reconcile the documented N08 criterion ambiguity."""
from pathlib import Path
import json, csv, hashlib
from datetime import datetime, timezone
B=Path(__file__).resolve().parents[1]
def readj(p):return json.loads((B/p).read_text())
def writej(p,x):(B/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
seal=readj('evidence/grade-seal.json')
assert hashlib.sha256((B/'evidence/blind-input.json').read_bytes()).hexdigest()==seal['input_hashes']['evidence/blind-input.json']
observed=readj('evidence/blind-observed.json')
assert observed['reviewer_scope']['input_sha256']==seal['input_hashes']['evidence/blind-input.json']
mapping=readj('evidence/blind-key.json')['mapping']
by_anon={g['submission_key']:g for g in observed['grades']}
by_original={m['submission_id']:by_anon[m['submission_key']] for m in mapping}
examples=[json.loads(s) for s in (B/'examples.jsonl').read_text().splitlines() if s]
original_rubric=B/'evidence/rubric-before-adjudication.csv'
if not original_rubric.exists():original_rubric.write_bytes((B/'rubric.csv').read_bytes())
with original_rubric.open(newline='') as f:reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
new_pass='각 원 키에 실제 속한 원행의 number를 대상으로 min/max/sum과 산술평균의 완성 출력이 맞아야 한다. 잘못 선택한 다른 원행 slice의 산술만 맞으면 통과가 아니다. 정수 절삭 불허; 분수 표기 허용.'
for row in rows:
    if row['requirement_id']=='P04-R3':
        row['t1_probe']='explicit/inferred 모두 각 batch에서 실제 확정한 format_used에 두 공통 probe를 적용한다. DMY이면 01-13의 month13, MDY이면 13-01의 month13에서 raise가 올바르다. inferred 모드는 batch마다 같은 추론 알고리즘으로 한 번 확정한다.'
    if row['requirement_id']=='N08-R2':
        row['pass']=new_pass
        row['partial']='네 필수 통계는 모두 제시했으나 일부 근거/검산 증거가 불충분해 완전 확인이 안 됨. 필수 통계 자체 누락이나 원키 기준 오출력은 fail.'
        row['fail']='원키별 완성 통계가 틀림; 빈도를 수량 합으로 대체; 통계 누락; 정수 평균 절삭. 소속 오류의 파급으로 틀린 숫자도 이 셀에서는 fail, 원인 사건수는 R3과 중복하지 않음.'
with (B/'rubric.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)

changed=[];cell_match=0;overall_match=0
for e in examples:
    g=by_original[e['submission_id']]
    actual={e['case_id']+'-'+k:v for k,v in g['requirements'].items()}
    e['separate_context_observed']={'stage':'first_blind_read','submission_key':g['submission_key'],'overall':g['overall'],
      'requirements':actual,'major_error':g['major_error'],'evidence':g['evidence'],'t1_action':g['t1_action'],'uncertainty':g['uncertainty'],
      'source_file':'evidence/blind-observed.json','human':False,'historical_software_execution':False}
    expected=e['expected_before_grade']
    overall_match+=g['overall']==expected['overall']
    final=dict(actual)
    for rid,v in expected['requirements'].items():
        cell_match+=v==actual[rid]
        if v!=actual[rid]:changed.append({'submission_id':e['submission_id'],'requirement_id':rid,'expected':v,'author_self_read':e['author_self_read']['requirements'][rid],'first_blind_observed':actual[rid]})
    if e['submission_id']=='N08-E3':
        final['N08-R2']='fail'
        e['adjudication']={'actor':'root author, source-based criterion clarification','requirements':final,'overall':'fail',
          'reason':'최초 formal 구매 use-case는 원키별 통계를 요구한다. selected values의 산술로 좁힐 수 있던 pass 문구를 원키별 완성 출력으로 명확화. partial/pass/fail 세 기존 판독을 보존.',
          'source_url':'https://github.com/numpy/numpy/blob/bceb9c20700514db5667831ce2878f1660fb071f/doc/neps/groupby_additions.rst#L23-L38',
          'primary_error_count':1,'secondary_failed_cells':['N08-R2'],'primary_failed_requirement':'N08-R3','external_human_agreement':False}
    else:e['adjudication']={'actor':'root author comparison, no change','requirements':final,'overall':g['overall'],'reason':'기대와 최초 별도 판독 일치','external_human_agreement':False}

(B/'examples.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in examples))
comparison={'kind':'AUTHORED_FIXTURE_COMPARISON_NOT_HUMAN_RELIABILITY','checked_utc':datetime.now(timezone.utc).isoformat(),
 'sealed_commit':'a9589eb1ed899da83230e5c6a3ffa30123b7d5f2','first_input_hash':seal['input_hashes']['evidence/blind-input.json'],
 'examples':len(examples),'expected_valid':8,'expected_invalid':4,'overall_matches':overall_match,'overall_denominator':12,
 'first_requirement_matches':cell_match,'requirement_denominator':36,
 'valid_false_rejections':sum(e['expected_before_grade']['overall']=='pass' and e['separate_context_observed']['overall']!='pass' for e in examples),
 'invalid_false_acceptances':sum(e['expected_before_grade']['overall']=='fail' and e['separate_context_observed']['overall']=='pass' for e in examples),
 'disagreements':changed,'first_blind_human_count':0,'initial_self_vs_blind_agreement_is_not_human_agreement':True,
 'adjudication_status':'author criterion clarified; same AI reviewer targeted reread requested; not a fresh independent replication',
 'post_clarification_review':None,
 'limits':['authored examples selected to exercise boundaries; no error-rate or population inference','no group assignment or treatment effect','P04 inferred-strict alternative is permitted but is not a fourth sealed sample','same model family and instruction-based access separation']}
writej('evidence/grading-comparison.json',comparison)
payload=readj('evidence/blind-input.json')
case=next(c for c in payload['cases'] if c['case_key']=='V4')
case['requirements'][1]['pass_condition']=new_pass
review={'kind':'TARGETED_CLARIFICATION_REREAD_NOT_FRESH_BLIND_REPLICATION','instruction':'한 요구의 통과 문구를 원키별 완성 출력으로 명확히 했다. 기대 판정과 원 사례명은 제공하지 않는다. 같은 세 제출을 새 기준으로 다시 판독하고 이전과 달라진 셀/이유를 보존하라. 이전 입력을 이미 보았으므로 새 독립검사라고 부르지 않는다. 실제 수정 수행은 여전히 미확인이다.',
 'cases':[case],'submissions':[s for s in payload['submissions'] if s['case_key']=='V4'],
 'requested_output':'JSON with scope, input_sha256, grades[submission_key,requirements,overall,major_error,evidence,t1_action], changed_interpretation, human_validation=false'}
writej('evidence/blind-clarification-input.json',review)
writej('evidence/clarification-seal.json',{'created_utc':datetime.now(timezone.utc).isoformat(),'input_sha256':hashlib.sha256((B/'evidence/blind-clarification-input.json').read_bytes()).hexdigest(),
 'prior_input_unchanged':True,'prior_rubric_sha256':hashlib.sha256(original_rubric.read_bytes()).hexdigest(),
 'new_rubric_sha256':hashlib.sha256((B/'rubric.csv').read_bytes()).hexdigest(),'expected_before_grading_unchanged':True})
print(json.dumps({k:comparison[k] for k in ['examples','overall_matches','first_requirement_matches','valid_false_rejections','invalid_false_acceptances','disagreements']},ensure_ascii=False))
