"""Compile post-seal DuckDB coding. Never writes T0 files; raw caches are ignored."""
from pathlib import Path
import csv, datetime as dt, hashlib, json

P = Path(__file__).resolve().parent
C = P / 'evidence/unread_cache'
NOW = dt.datetime.now(dt.timezone.utc).isoformat()
SEAL = '9de54923257d613359348c8ccee2ff8225c8a0d8'
initial = {r['case_id']: r for r in map(json.loads, (P/'initial.jsonl').read_text().splitlines())}
selected = ['D01','D02','D03','D04','D05','D06','D07','D08','DB04','DB07']
parse = lambda s: dt.datetime.fromisoformat(s.replace('Z','+00:00'))
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
def writejl(name, rows):
    (P/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
def cm(case):
    return json.loads((C/f"comments-{initial[case]['issue_number']}.json").read_text())
def event(case, cid, summary, **more):
    x=next(x for x in cm(case) if x['id']==cid)
    return dict(comment_id=cid,url=x['html_url'],created_utc=x['created_at'],updated_utc=x['updated_at'],
                actor=x['user']['login'],public_association=x['author_association'],body_sha256=sha(x['body']),
                summary=summary,**more)
def q(case,cid,qid,var,summary,kind='information_request',presealed=False):
    return event(case,cid,summary,question_id=qid,variable=var,kind=kind,presealed=presealed,
                 within_root30=parse(next(x for x in cm(case) if x['id']==cid)['created_at'])<=parse(initial[case]['root_created_utc'])+dt.timedelta(days=30))
def answer(case,cid,qrow,summary,classification,**more):
    z=event(case,cid,summary,question_id=qrow['question_id'],classification=classification,**more)
    root=parse(initial[case]['root_created_utc']); when=parse(z['created_utc']); asked=parse(qrow['created_utc'])
    z.update(same_original_requester=z['actor']==initial[case]['root_author'],same_variable=True,
      answer_within_root30=when<=root+dt.timedelta(days=30),answer_within_root90=when<=root+dt.timedelta(days=90),
      answer_within_question30=when<=asked+dt.timedelta(days=30),wait_hours=(when-asked).total_seconds()/3600,
      roundtrip_key=f"{case}:{qrow['comment_id']}:{cid}")
    return z

chains={}
timeline={r['case_id']:r for r in json.loads((P/'evidence/timeline-observation.json').read_text())}
for case in selected:
    s=initial[case]; r=parse(s['root_created_utc']); comments=cm(case)
    in30=[x for x in comments if parse(x['created_at'])<=r+dt.timedelta(days=30)]
    in90=[x for x in comments if parse(x['created_at'])<=r+dt.timedelta(days=90)]
    receipt=json.loads((P/f"evidence/first-{s['issue_number']}.json").read_text())
    chains[case]={k:s[k] for k in ['case_id','root_url','root_created_utc','root_author','request_type','information_score','original_grade','first_strategy','first_response_url','first_responder','supplier_also_requester']}
    chains[case].update(sample='A' if case.startswith('D0') else 'B',seal_sha=SEAL,checked_utc=NOW,
      exposure_frozen=s['exposure'],exposure_effective=s['exposure'] or case=='DB04',
      first_question=s['has_information_question'],any_question_root30=s['has_information_question'],
      questions=[],answers=[],recommendations=[],executions=[],supplier_implementations=[],
      same_variable_answer=False,restatement_already_present=False,linked_recommendation_change=False,
      bundle_linked_change=False,change_linked_to_asked_variable='not_observed',
      new_execution_success=False,new_execution_failure=False,chain_success=False,
      windows={'root30_end':(r+dt.timedelta(days=30)).isoformat(),'root90_end':(r+dt.timedelta(days=90)).isoformat(),
       'root30_comment_count':len(in30),'root90_comment_count':len(in90),'current_all_comment_count':len(comments),
       'conversation_status':'observed_closed_window','deleted_comments':'no_deleted_placeholder_observed; undetectable deletion not provable',
       'pagination':{'api_per_page':100,'api_has_next_page':receipt.get('has_next_page'),
           'html_timeline':timeline[case]['timeline_page_info'],'html_back_timeline':timeline[case]['back_timeline_page_info']},
       'last_endpoint':s['root_url'],'last_api_endpoint':receipt.get('url'),'checked_utc':NOW,
       'last_observed_comment_utc':comments[-1]['created_at'] if comments else None,
       'comment_versions':'current public bodies; created/updated timestamps and hashes retained; edit originals unavailable'},
      provider_source_ids=[],unknowns=[],costs={'roundtrip_keys':[],'answered_wait_hours':[],
       'reader_time':'미확인: 클릭/읽기 시간 로그 없음','counterfactual_work_saved':'미확인: 대안 전략을 시행하지 않음'})

d=chains['D01']
d['recommendations']=[event('D01',1375783093,'다른 lambda 오류도 함께 고칠 계획을 알림',kind='supplier_plan'),
 event('D01',1422727980,'근본 지원은 미루고 명시적 미지원 예외와 향후 작업 표시로 제한함',kind='supplier_scope_reduction',within_root30=False,within_root90=True)]
d['executions']=[event('D01',1369666494,'첫 외부답 이전 작성자가 수정한 binder 코드 때문에 원래와 다른 오류가 나왔음을 정정',kind='pre_response_self_correction',new_execution_after_advice=False)]
d['supplier_implementations']=[{'url':'https://github.com/duckdb/duckdb/commit/88e217dc5a4ec937cea98779559b6684c150a526','utc':'2023-02-09T11:30:18Z','source_id':'DP06','status':'source_read_not_executed','summary':'CHECK와 generated column에서 lambda 미지원 예외를 던지는 코드와 오류 기대 테스트. 원목표 기능 구현 성공과 다름','within_root30':False,'within_root90':True}]
d['provider_source_ids']=['DP06'];d['unknowns']=[{'claim':'원 작성자의 후속 새 실행 성공','reason':'지원자 계획/예외 추가 후 requester 실행 보고 없음','last_confirmed':d['root_url'],'next_source':'https://github.com/duckdb/duckdb/commit/88e217dc5a4ec937cea98779559b6684c150a526 에 대한 작성자 실행 로그'}]

d=chains['D02']; qq=q('D02',1373853388,'D02-Q1','observed_workload_vs_theoretical','실제 문제가 발생했는지 이론 분석만인지 질문',presealed=True);d['questions']=[qq]
d['answers']=[answer('D02',1374537619,qq,'예기치 않은 메모리 오류를 실제 겪었다고 답하고 별개 쿼리의 동시 실행이라는 추가 논거를 함께 제시','direct_existing_new_disclosure',same_target_version='same reported BufferManager issue; exact run log unavailable',new_execution_after_question=False)]
d['recommendations']=[event('D02',1373853388,'같은 쿼리 전체 중단이면 스레드 중복 실패가 시스템 동작을 바꾸지 않는다고 설명',kind='before_explanation',candidate='local allocation fix not yet justified'),
 event('D02',1374567686,'서로 다른 쿼리의 동시 실행이면 문제가 될 수 있음을 인정하고 쿼리 단위 중단·자원 반환 대기를 포함하는 설계를 처음 제시',kind='explanation_revision_and_first_concrete_proposal',candidate='query-aware memory handling',same_supporter=True,explicit_answer_connection=True,connection_basis='작성자가 추가한 동시 다중 query 논거를 직접 인용; 실제 OOM 경험 여부만 인용한 것이 아님',bundle_linked_change=True,before_concrete_proposal_exists=False,no_prior_proposal=True,change_linked_to_asked_variable='미확인: 답에 추가 다중-query 논거가 함께 존재'),
 event('D02',1375479682,'작성자가 이전 예시 패치 적용을 철회하고 전체 재설계와 이번 신고 범위를 구분',kind='requester_scope_boundary',execution=False)]
d['questions'].append(q('D02',1374567686,'D02-ACTION1','proposed_patch_test_result','예시 변경이 실제 OOM을 해결하는지 시험했는지 확인 요청',kind='patch_verification_action_request',presealed=False))
d.update(same_variable_answer=True,linked_recommendation_change=False,bundle_linked_change=True,bundle_linked_explanation_revision=True,before_concrete_proposal_exists=False,before_explanation_exists=True,no_prior_proposal=True,change_linked_to_asked_variable='unconfirmed')
d['executions']=[event('D02',1374537619,'실제 장애 경험을 새로 공개했지만 질문 후 새로 실행한 결과는 아님',kind='retrospective_existing_execution',new_execution_after_advice=False)]
d['provider_source_ids']=['DP05'];d['unknowns']=[{'claim':'실제 물은 경험 여부 한 값이 설명/권고 변경을 유발함','reason':'동일 답글의 다중-query 논거가 명시 연결의 대상이라 단일 변수의 기여 분리 불가','last_confirmed':'https://github.com/duckdb/duckdb/issues/5818#issuecomment-1374567686','next_source':'Mytherin이 두 정보 중 무엇으로 판단을 수정했는지 명시한 공개 결정 기록'}, {'claim':'새 구현의 성공','reason':'작성자 예시 적용 철회, 시험 결과 없음','last_confirmed':'https://github.com/duckdb/duckdb/issues/5818#issuecomment-1375479682','next_source':'같은 workload·판으로 실행한 공개 회귀시험 기록'}]

d=chains['D03'];d['supplier_implementations']=[{'url':'https://github.com/duckdb/duckdb/pull/6039','utc':'2023-02-06T11:29:53Z','source_id':'DP07','status':'source_and_patch_read_not_executed','summary':'table function 안 lambda parameter 바인딩 수정 및 해당 사례 경로를 로컬 parquet로 대체한 회귀시험','within_root30':False,'within_root90':True}];d['provider_source_ids']=['DP07'];d['unknowns']=[{'claim':'작성자 실행/수락','reason':'30/90일 댓글 0; 공급자 PR만 있음','last_confirmed':d['root_url'],'next_source':'https://github.com/duckdb/duckdb/pull/6039 적용판에서 원 작성자의 remote URL 입력 실행 로그'}]
d=chains['D04'];d['supplier_implementations']=[{'url':'https://github.com/duckdb/duckdb/pull/5869','utc':'2023-01-12T11:39:52Z','source_id':'DP08','status':'decision_body_read_not_executed','summary':'ICU 역방향 필드 연산 패치, subtraction hack 제거 및 테스트 갱신이라고 명시','within_root30':True,'within_root90':True}];d['provider_source_ids']=['DP08'];d['unknowns']=[{'claim':'원 작성자 사용 성공','reason':'maintainer가 원 요청자이며 root에 수정 제안 존재, 댓글 0; PR 병합은 사용자 실행이 아님','last_confirmed':d['root_url'],'next_source':'https://github.com/duckdb/duckdb/pull/5869/files 의 당시 테스트를 지정 환경에서 실행한 결과'}]

d=chains['D05'];d['questions']=[q('D05',2200636928,'D05-Q1','connection_time_zone','연결 시간대 이름을 요청',presealed=True)]
d['answers']=[event('D05',2200829808,'같은 지원자가 UTC 오프셋으로 여러 시간대 후보를 나열하고 Kolkata를 추정함',classification='third_party_inference',same_original_requester=False,same_variable_answer=False)]
d['supplier_implementations']=[{'url':'https://github.com/duckdb/duckdb/pull/12794','utc':'2024-07-02T09:04:23Z','source_id':'DP02','status':'patch_and_tests_read_not_executed','summary':'months를 days보다 먼저 더하는 순서로 수정. 테스트에 Kolkata 설정. 작성자 답으로 확인한 설정은 아님','within_root30':True,'within_root90':True}]
d['provider_source_ids']=['DP02'];d['unknowns']=[{'claim':'작성자 실제 연결 시간대','reason':'작성자 답 없음; +05:30는 여러 zone과 대응','last_confirmed':'https://github.com/duckdb/duckdb/issues/12784#issuecomment-2200829808','next_source':'원 작성자의 current_setting(timezone) 출력 또는 당시 연결 설정'}, {'claim':'작성자 수정판 실행 성공','reason':'공급자 코드/기대 테스트만 확인','last_confirmed':'https://github.com/duckdb/duckdb/pull/12794','next_source':'원 작성자의 수정판 재현 결과'}]

d=chains['D06'];d['supplier_implementations']=[{'url':'https://github.com/duckdb/duckdb/pull/12859','utc':'2024-07-07T11:55:01Z','source_id':'DP09','status':'decision_body_read_not_executed','summary':'list_zip의 fixed array 입력을 지원하도록 수정한다는 PR 명시','within_root30':True,'within_root90':True}];d['provider_source_ids']=['DP09'];d['unknowns']=[{'claim':'원 요청자의 수정판 실행','reason':'댓글 0; 공급자 변경만 확인','last_confirmed':d['root_url'],'next_source':'https://github.com/duckdb/duckdb/pull/12859/files 의 관련 회귀시험/요청자 재실행 결과'}]

d=chains['D07'];d['recommendations']=[event('D07',2202144244,'pandas 경유 결측값 처리와 다른 API의 결과를 설명함; 작성자 후속 답/새 실행은 없음',kind='directive_explanation')];d['unknowns']=[{'claim':'NumPy masked 결과가 사용자가 원하는 전체 출력에 적합함','reason':'공급자 첫 댓글 설명은 있지만 작성자 수락/후속 실행 및 당시 공식 변환 계약을 별도 확인하지 못함','last_confirmed':'https://github.com/duckdb/duckdb/issues/12796#issuecomment-2202144244','next_source':'DuckDB v1.0.0 Python numpy_result_conversion.cpp의 null mask/fill_value 처리와 작성자 후속'}]

d=chains['D08'];d['recommendations']=[event('D08',2203075138,'프레임 경계를 설명하고 함수 교체를 권함. 함수와 alias 구분의 일부 설명은 이후 본인이 정정',kind='directive_before'),event('D08',2203186542,'작성자의 구체적인 실행 보고 후 value 함수도 frame 경계를 따름을 인정하고 전체 frame 조정을 권고',kind='unsolicited_feedback_revision',same_supporter=True,explicit_answer_connection=False,info_question_before=False)]
d['executions']=[event('D08',2203153988,'작성자가 last_value와 전체 partition을 포함하는 frame으로 바꿔 기대 동작을 얻었다고 구체적으로 보고',kind='new_execution_success',same_goal=True,success_extent='reported expected behavior for original query',evidence_grade='requester specifies operation and outcome; no full output attachment',after_clarification_answer=False)]
d.update(new_execution_success=True,change_linked_to_asked_variable='not_applicable_no_information_question')
d['supplier_implementations']=[{'url':'https://github.com/duckdb/duckdb-web/pull/3223','utc':'2024-07-02T12:56:13Z','source_id':'DP10','status':'documentation_diff_read','summary':'공급자가 first/last alias 설명을 문서에서 제거했지만 뒤의 지원자 정정과 상충. 문서 병합 그 자체를 기술적 정답으로 세지 않음','within_root30':True,'within_root90':True}]
d['provider_source_ids']=['DP01','DP10'];d['unknowns']=[{'claim':'어느 링크/문장만으로 성공했는가','reason':'첫답에 공식 링크 2개와 잘못된 설명 및 유용한 frame 설명이 함께 존재; 클릭 로그 없음','last_confirmed':'https://github.com/duckdb/duckdb/issues/12804#issuecomment-2203153988','next_source':'작성자가 실제 사용한 안내 요소를 특정한 공개 후속 설명'}]

d=chains['DB04'];qq=q('DB04',1493265260,'DB04-Q1','actual_csv_null_is_quoted','제시 예제로는 재현되지 않아 실제 파일 null 토큰의 인용 여부를 요청',presealed=True);d['questions']=[qq];d['answers']=[answer('DB04',1493302942,qq,'실제 CSV에서는 null 토큰이 따옴표 안에 있다고 답하고 수정 예시를 제시','direct_existing_new_disclosure',new_requirement=False,first_version_value_evidence='first responder quoted unquoted example; title was renamed after answer')];d.update(same_variable_answer=True,change_linked_to_asked_variable='unconfirmed_no_supporter_followup')
d['supplier_implementations']=[{'url':'https://github.com/duckdb/duckdb/pull/7379','utc':'2023-05-08T14:22:39Z','source_id':'DP03','status':'patch_and_tests_read_not_executed','summary':'quoted null fixture와 parallel true/false의 nullstr 결과를 회귀시험에 추가. 후속 권고/작성자 사용은 아님','within_root30':False,'within_root90':True}]
d['provider_source_ids']=['DP03'];d['unknowns']=[{'claim':'답 후 동일지원자의 권고 변경','reason':'작성자 답 뒤 30/90일 댓글 없음; 제목 수정은 권고 아님','last_confirmed':'https://github.com/duckdb/duckdb/issues/6943#issuecomment-1493302942','next_source':'Mytherin의 답을 인용한 후속 권고 기록'}, {'claim':'원판 제목에 quoted 값이 있었다','reason':'후발 rename event로 반증; T0는 미래 제목에 노출됨','last_confirmed':'https://github.com/duckdb/duckdb/issues/6943#event-8932902142','next_source':'원 본문 편집 이력 또는 최초 알림 메일'}]

d=chains['DB07'];qq=q('DB07',1493424295,'DB07-Q1','desired_result_order_contract','원래 입력 순서라는 뜻과 적용 범위를 질문',presealed=True);d['questions']=[qq,q('DB07',1494488354,'DB07-LQ1','row_number_placement','같은 projection에 서로 다른 window로 row number를 붙이고 나중에 정렬하려는 것인지 질문',presealed=False)]
d['answers']=[answer('DB07',1493849083,qq,'dplyr 예제로 입력 행 순서 유지 목표를 다시 보여주고 native 미지원 답도 수용 가능하다고 말함','restatement_already_present',new_information='native 지원이 없어도 괜찮다는 수용 범위는 새 공개, 기존 선호인지 질문으로 형성됐는지 미확인'),event('DB07',1494446827,'입력은 임의 relational operation일 수도 있으며 ROW_NUMBER를 붙였다 제거하는 안을 설명',classification='unsolicited_method_or_scope_expansion',same_original_requester=True,new_execution_success=False)]
d['recommendations']=[event('DB07',1494416484,'data frame의 index에 대한 최종 정렬을 처음 구체적으로 제안',kind='no_prior_proposal',same_supporter=True,explicit_answer_connection=False),event('DB07',1494488354,'streaming row number가 다른 window 뒤에 평가된다는 이유로 입력 data frame에 미리 순서열을 넣고 최종 정렬하라고 수정 제안',kind='method_refinement_after_unsolicited_detail',same_supporter=True,explicit_answer_connection=True,linked_to_direct_answer_to_own_question=False)]
d['executions']=[event('DB07',1494163402,'client에서 구현하겠다는 계획',kind='intention_not_execution'),event('DB07',1494446827,'row number를 붙였다 제거하고 있다는 방법 설명, 완료된 출력/성공 보고 없음',kind='implementation_in_progress_no_result')]
d.update(same_variable_answer=True,restatement_already_present=True,change_linked_to_asked_variable='unconfirmed_no_prior_concrete_proposal_and_later_question_unanswered')
d['provider_source_ids']=['DP04'];d['unknowns']=[{'claim':'최초 질문의 답이 하나의 기존 제안을 변경함','reason':'구체적 index 사용 제안은 답 이후 처음 등장; 마지막 방법 수정은 자발적으로 밝힌 임의 relation/row-number 안을 받음','last_confirmed':'https://github.com/duckdb/duckdb/issues/6947#issuecomment-1494488354','next_source':'최초 목표 답과 후보 선택을 명시 연결한 지원자 결정 기록'}, {'claim':'같은목표 실행 성공','reason':'계획/작업중 설명은 있지만 새 코드 출력이나 성공 보고 없음','last_confirmed':'https://github.com/duckdb/duckdb/issues/6947#issuecomment-1494446827','next_source':'해당 client 변경 커밋과 동일 dplyr 예제 재현 출력'}]

for d in chains.values():
    r=parse(d['root_created_utc'])
    direct=[a for a in d['answers'] if a.get('same_original_requester') and a.get('same_variable')]
    d['costs']['roundtrip_keys']=sorted(set(a['roundtrip_key'] for a in direct))
    d['costs']['answered_wait_hours']=[a['wait_hours'] for a in direct]
    for qq in d['questions']:
        matching=[a for a in direct if a['question_id']==qq['question_id']]
        qq['question30_end']=(parse(qq['created_utc'])+dt.timedelta(days=30)).isoformat()
        qq['answer_status']='same_variable_direct_answer' if matching else 'no_answer_in_observed_window'
        qq['censored_at_root30_hours']=min(720,max(0,((r+dt.timedelta(days=30))-parse(qq['created_utc'])).total_seconds()/3600)) if not matching else None
        qq['question30_observed']=True
        qq['unanswered_followup_censor_hours']=720 if not matching else None
    d['any_question_root30']=any(x['kind']=='information_request' and x['within_root30'] for x in d['questions'])
    d['unique_roundtrip_count']=len(d['costs']['roundtrip_keys'])
    d['answer_no_response_primary']=any(x['kind']=='information_request' and x['within_root30'] and x['answer_status']=='no_answer_in_observed_window' for x in d['questions'])
    d['observability']='current_public_conversation_complete_original_edits_unconfirmed'
writejl('chains.jsonl',list(chains.values()))

later=[]
for case in selected:
    for x in chains[case]['questions']:
        if x['presealed']:continue
        later.append({'case_id':case,'question_id':x['question_id'],'url':x['url'],'created_utc':x['created_utc'],'actor':x['actor'],'kind':x['kind'],'variable':x['variable'],'summary':x['summary'],'pre_answer_prediction':'none: post-seal retrospective coding','answer_status':x['answer_status'],'count_information_question':x['kind']=='information_request','reason':'patch verification excluded from information-question denominator' if x['kind']!='information_request' else 'implementation detail requested; no later author reply'})
later.append({'case_id':'DB07','question_id':'DB07-ROLE-REVERSAL','url':'https://github.com/duckdb/duckdb/issues/6947#issuecomment-1494422798','created_utc':'2023-04-03T14:22:41Z','actor':'krlmlr','kind':'requester_asks_supporter','variable':'meaning_of_index_column','summary':'requester가 index column의 뜻/접근법을 질문하고 지원자가 다음 댓글에서 답함','pre_answer_prediction':'none: post-seal retrospective coding','answer_status':'supporter answered, not original-requester disclosure','count_information_question':False,'reason':'주체 방향 반대; requester 값 회수 분모 제외'})
later.append({'case_id':'D05','question_id':'D05-GUESS','url':'https://github.com/duckdb/duckdb/issues/12784#issuecomment-2200829808','created_utc':'2024-07-01T19:07:06Z','actor':'hawkfish','kind':'supporter_guess_possible_confirmation','variable':'connection_time_zone','summary':'지원자가 Kolkata를 추정; 원 작성자 값/직접답 아님','pre_answer_prediction':'none: post-seal retrospective coding','answer_status':'no author reply','count_information_question':False,'reason':'엄격 직접 요청으로 추가 세지 않고 확인을 기대한 추정 가능성 기록'})
with (P/'later-questions.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(later[0]));w.writeheader();w.writerows(later)

corrections=[{'correction_id':'D-C01','case_id':'DB04','checked_utc':NOW,'frozen_sha':SEAL,'affected_files':['initial.jsonl','questions.csv','source-ledger.jsonl'],'claim_at_T0':'current title의 quoted NULL 정보와 원판 위치가 불확실; exposure=false','new_evidence':'2023-04-05T09:19:04Z Mytherin의 제목 변경: 원 제목은 Mac v0.7.1 현상, 후 제목은 quoted NULL 조건. 작성자 답은 4월2일.','url':'https://github.com/duckdb/duckdb/issues/6943#event-8932902142','effective_exposure':True,'value_in_initial_title':'absent','original_body_grade':'Q for first-response quoted example only; full original U','action':'frozen files left intact; use exposure_effective in chains for sensitivity','impact':'unexposed B subset excludes DB04; current title cannot count as already-provided value'},
{'correction_id':'D-C02','case_id':'D02','checked_utc':NOW,'frozen_sha':SEAL,'affected_files':['questions.csv'],'claim_at_T0':'actual workload vs theoretical branch predicted to influence next work','new_evidence':'同 지원자 변경은 답글에 함께 추가된 concurrent multi-query 논거를 직접 인용함','url':'https://github.com/duckdb/duckdb/issues/5818#issuecomment-1374567686','action':'record bundle_linked_change=true and asked-single-variable attribution unconfirmed','impact':'actual asked variable one-value effect cannot be inferred'},
{'correction_id':'D-C03','case_id':'DB07','checked_utc':NOW,'frozen_sha':SEAL,'affected_files':['questions.csv'],'claim_at_T0':'physical-order value would predict order key/final ordering','new_evidence':'예상 종류의 제안은 나왔지만 답 전 구체적 제안 없음; 후속 방법 변경은 추가 자발적 입력과 연결, 새 실행 없음','url':'https://github.com/duckdb/duckdb/issues/6947#issuecomment-1494488354','action':'no_prior_proposal for first recommendation; refinement not strict asked-variable chain','impact':'predicted branch fit is not evidence of recommendation change caused by question'},
{'correction_id':'D-C04','case_id':'D02','checked_utc':NOW,'frozen_sha':SEAL,'affected_files':['post-seal chains coding only'],'earlier_postseal_code':'linked_recommendation_change=true under broad explanation revision interpretation','new_evidence':'root 독립 재독의 이의: 첫 Mytherin 답은 기술 영향 평가와 시험 난점 설명이며 구체 권고가 없다. 작성자 CAS 예시는 동일지원자가 추천한 후보가 아니다. 후속 재설계는 첫 구체 제안이다.','url':'https://github.com/duckdb/duckdb/issues/5818#issuecomment-1373853388','action':'linked_recommendation_change=false; before_concrete_proposal_exists=false; no_prior_proposal=true; bundle_linked_explanation_revision=true','impact':'strict 권고변경은 DuckDB 주표본0건; 설명수정1건은 별도 지표','review_type':'root separately re-read exact thread; not blind independent full recoding'}]
writejl('corrections.jsonl',corrections)

# Reduce publishable timeline metadata; complete cached payload remains ignored.
t=json.loads((P/'evidence/timeline-observation.json').read_text())
for case in t:
    for e in case['events']:
        if 'previousTitle' in e:
            e['previous_title_sha256']=sha(e.pop('previousTitle'))
            e['current_title_sha256']=sha(e.pop('currentTitle'))
            e['title_change_summary']='초기 Mac판 제목에서 quoted-null 조건 제목으로 후발 변경' if case['case_id']=='DB04' else 'lambda 관련 제목의 범위를 nested로 구체화'
(P/'evidence/timeline-observation.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n')

print(json.dumps({'cases':len(chains),'A':8,'B':2,'roundtrips':sum(x['unique_roundtrip_count'] for x in chains.values()),'first_questions':sum(x['first_question'] for x in chains.values()),'direct_answer_cases':sum(x['same_variable_answer'] for x in chains.values()),'bundle_changes':sum(x['bundle_linked_change'] for x in chains.values()),'single_variable_supported_changes':0,'new_execution_successes':sum(x['new_execution_success'] for x in chains.values()),'chain_successes':0},ensure_ascii=False))
