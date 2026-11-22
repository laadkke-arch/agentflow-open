"""Build T1 research annotations from immutable, publicly fetched metadata.

Does not fetch or save source bodies; does not modify any T0 sealed file.
All Korean summaries below are researcher annotations, not source quotations.
"""
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path

P = Path(__file__).parent
SEAL = '68fc97fadceb46f9945a71fcc53730e29f6c62bf'
NOW = dt.datetime.now(dt.timezone.utc).isoformat()
initial = [json.loads(x) for x in (P/'initial.jsonl').read_text().splitlines()]
frozen = [json.loads(x) for x in (P/'frozen-responses.jsonl').read_text().splitlines()]
threads = json.loads((P/'thread-metadata.json').read_text())
metadata = json.loads((P/'followup-metadata.json').read_text())
byid = {r['artifact_id']: r for r in metadata}
bycase = {r['case_id']:r for r in initial}
thread = {r['case_id']:r for r in threads}
sources0 = json.loads((P/'sources.json').read_text())
source = {r['id']:r for r in sources0}
notnull_source=dict(id='S-TD02',related_q=['Q5','Q6','Q8'],case_ids=['S08'],
    url='https://github.com/sqlite/sqlite/blob/57acbb1380e3b51476aa8c71d1a881821f8ad5ff/test/notnull.test',
    published_or_revised='2021-12-30T15:30:28Z (version commit)',
    fixed_version='SQLite 3.37.1 / 57acbb1380e3b51476aa8c71d1a881821f8ad5ff',checked_utc=NOW,
    read_locations='L25–51 notnull-1.0–1.2b; L75–81 notnull-1.6',
    observed='NOT NULL이며 default가 없는 열을 INSERT 열 목록에서 빼면 제약 오류. DEFAULT가 있는 열의 생략은 별도 성공 사례.',
    limitations='T1에서 추가로 연 같은 비교판 테스트. 동결 메시지의 입력 원문으로 소급하지 않음. 이 세션에서 테스트 자체를 실행하지 않았고 실제 Node package 판은 미상.',
    producer='SQLite maintainers',lineage='SQLite official regression tests; distinct test file',
    count_in_minimum=True,count_reason='독립적으로 읽은 당시 고정판 공식 회귀 테스트 원문; 댓글/개정 증식 아님.',kind='provider_test',
    evidence_opened_stage='T1',part_of_frozen_message_input=False)
source['S-TD02']=notnull_source

def stamp(s):
    return dt.datetime.fromisoformat(s.replace('Z','+00:00')).replace(tzinfo=dt.timezone.utc)

def ident(case,n): return thread[case]['artifact_ids'][n]
def meta(case,n): return byid[ident(case,n)]
def url(case,n): return 'https://sqlite.org/forum/artifact/'+ident(case,n)
def hours(a,b): return round((stamp(b)-stamp(a)).total_seconds()/3600,6)
def writejson(name,value):
    (P/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def writecsv(name, rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

# Indexes are artifact positions in thread-metadata.json, with originals/edits separate.
# classification describes the actual utterance, never an answer to an unsent Q.
annotations = {
'S01': {
1: ('author_existing_fact','root_log_revision','메모리 DB 예제에 맞추어 실행 로그를 수정한 최초 답 이전 개정','body L1–93','root_edit','not_Q'),
2: ('third_party','filesystem_permission','파일 생성 권한을 실제로 질문','body L1','clarification_request','different_variable'),
3: ('direct_answer','filesystem_permission','같은 디렉터리에서 생성할 수 있고 여러 DB 경로도 시도했다고 답함','body L1–3','author_answer','different_variable'),
4: ('third_party','extended_error_code','RC 매크로를 오독하고 확장 오류 코드를 요청','body L1–3','clarification_request','different_variable'),
5: ('direct_answer','extended_error_code','기존 검사 매크로를 설명하고 확장 코드도 14라고 답함; 3.37 사용을 자발 명시','body L1–15','author_answer','different_variable'),
6: ('author_existing_fact','binding_comparison','같은 라이브러리·사용자·디렉터리의 스크립트 바인딩은 성공한다고 보고','body L1–31','author_comparison','different_variable'),
7: ('third_party','buffer_and_quoting','문자열 버퍼와 인용 부호의 영향을 확인하자고 요청','body L1–27','clarification_request','different_variable'),
8: ('direct_answer','buffer_and_quoting','인용 방식과 세미콜론 변형을 이미 시도했고 READWRITE 코드를 다시 제시','body L1–47','author_answer','different_variable'),
9: ('third_party','open_CREATE_flag','CREATE와 READWRITE를 함께 쓰는 수정 제안의 초판','body L1','proposed_fix','Q_goal_already_T0'),
10: ('third_party','open_CREATE_flag','제안의 표현을 두 플래그의 결합으로 수정','body L1','reply_edit','Q_goal_already_T0'),
11: ('third_party','main_initialization','CREATE 플래그 및 main 테이블 생성을 넣은 재현과 초기화 가설','body L1–33','third_party_reproduction','different_variable'),
12: ('third_party','earlier_misreading','앞선 코드 오독을 인정','body L1–3','correction','not_Q'),
13: ('third_party','open_CREATE_flag','ATTACH로 플래그가 전달되는지 아직 확신하지 못한다고 정정','body L1–5','uncertainty_correction','Q_goal_already_T0'),
14: ('author_existing_fact','version_and_existing_database','이미 채워진 DB 및 3.35.5·3.36에서도 같은 실패를 확인','body L1–27','author_reproduction','different_variable'),
15: ('author_existing_fact','open_CREATE_flag','CREATE를 켜면 성공·끄면 실패하며 자기 테스트 앱도 해결됐다고 보고; 모든 open의 자동생성은 원치 않는 선호를 뒤늦게 표명','body L3,L16–18,L35–59','reported_progress;author_late_preference','Q_goal_already_T0'),
16: ('third_party','open_CREATE_flag','자신의 ATTACH에서도 플래그 없는 실패를 재현','body L1–5','third_party_reproduction','not_author_value'),
17: ('author_existing_fact','binding_implicit_flag','기존 스크립트 바인딩이 메모리/빈 경로에 CREATE를 내부 추가함을 확인','body L1–5','author_implementation_explanation','different_variable'),
},
'S02': {
1: ('third_party','command_invoked','DB 파일 대신 프로그램을 실행해야 함을 설명하면서 실제 명령을 다시 질문','body L1–3','clarification_request','same_variable_already_T0'),
2: ('third_party','compiled_executable','로그의 -o mysql을 근거로 ./mysql 실행을 제안','body L1–5','proposed_fix','same_variable_already_T0'),
3: ('unavailable','reply_edit','직전 제3자 답의 빈 삭제 개정; 원래 artifact와 다음 재게시 내용은 열람 가능','W 0; P card','deleted_revision','not_author_value'),
4: ('third_party','compiled_executable','동일한 ./mysql 설명을 root에 직접 재게시','body L1–5','proposed_fix','same_variable_already_T0'),
},
'S03': {
1: ('third_party','migration_order_or_legacy','view를 먼저 지우고 뒤에 재생성하는 순서와 legacy 모드 대안을 함께 설명; 작성자의 제약 답은 없음','body L1–9','conditional_advice','third_party_only'),
},
'S04': {
1: ('third_party','transaction_granularity','행마다 트랜잭션인지 전부 한 트랜잭션인지 질문하고 commit 전 재시작 조건을 설명','body L1–2','clarification_request','related_not_success_return'),
2: ('third_party','commit_explanation','성공 commit 전 상태는 확정 데이터가 아니라고 설명하고 현상을 설명하는지 질문','body L1–3','clarification_request','related_not_success_return'),
3: ('third_party','language_wrapper_restart','언어·wrapper·종료 처리·재시작 방식·시험 목적을 묶어 질문','body L1–5','clarification_request','different_variable'),
4: ('direct_answer','language_wrapper_restart','Objective-C, FMDB, 3370000 amalgamation, 전원+홈 강제 재시작이라고 답함','body L1–10','author_answer','different_variable'),
5: ('direct_answer','transaction_granularity','행마다 별도 트랜잭션이라고 답하고 committed 데이터도 사라진다고 주장; 성공 반환 로그는 없음','body L1–2','author_answer;author_assertion_conflicted','partial_related_claim'),
6: ('third_party','reproduction_details','commit된 데이터가 사라진다면 자세한 재현 정보를 계속 달라고 요청','body L1–5','clarification_request','related_not_success_return'),
7: ('direct_answer','reproduction_details','BEGIN·INSERT·close 재현 코드를 제시하나 COMMIT 없음; 손상·commit 실패 로그와 소실 주장','body L7–23,L28–35','author_reproduction;reported_failure','contradicts_unqualified_yes'),
8: ('direct_answer','reproduction_details','같은 재현의 문장 편집판; COMMIT 없는 코드와 commit 실패 로그 유지','body L7–23,L28–35; P card','reply_edit;author_reproduction','contradicts_unqualified_yes'),
9: ('third_party','missing_COMMIT','코드에 END/COMMIT가 없음을 지적하며 CLI 예제로 미확정 행의 소실을 설명; 손상은 별도라고 구별','body L1–44','third_party_reproduction','not_author_value'),
10: ('third_party','database_corruption','손상 원인 문서 링크를 제시','body L1','reference_link','not_author_value'),
},
'S05': {
1: ('third_party','serialized_mode','serialized mode 또는 db_mutex가 NULL이 아닌 조건을 설명; 실제 mode를 작성자가 밝히지 않음','body L1–3','conditional_advice','third_party_only'),
},
'S06': {
1: ('third_party','custom_header','새 SQLITE_CUSTOM_INCLUDE 관련 이전 대화로 안내','body L1–3','reference_link','third_party_only'),
2: ('author_existing_fact','candidate_reaction','가능할 수도 있다고 반응하고 기존 매크로 문서 수정을 희망; 실행·source 형태·판은 보고하지 않음','body L1','tentative_acceptance','no_variable_value'),
},
'S07': {
1: ('third_party','PG_identity_and_sqlite_mode','PG가 PostgreSQL인지 묻되 그렇게 가정하고 SQLite auto_vacuum 문서 링크 및 조건을 설명','body L1–11','clarification_request;reference_link','different_variable'),
2: ('third_party','cross_database_comparison','대체로 맞다고 승인하며 PG tuple 수명과 SQLite page 관리를 설명; PG 반환 예외는 검토하지 않음','body L1–7','third_party_approval','not_author_value'),
3: ('author_existing_fact','source_consultation','링크 문서가 이전 VACUUM 문서보다 자세하다고 직접 비교; 구현·해결 보고는 없음','body L1','source_consultation','not_variable_value'),
4: ('new_requirement','update_delete_followup','UPDATE/DELETE의 사본·in-place·빈 페이지 차이를 추가로 질문; 최초 비교를 대체했다는 증거는 없음','body L1–4','new_question_scope','new_scope_not_T0_condition'),
5: ('third_party','update_delete_followup','row 공간 변화·VACUUM 비용으로 추가 질문에 답함','body L1–9','answer_to_new_question','not_Q'),
6: ('third_party','update_delete_followup','UPDATE는 삭제 후 삽입이고 빈 페이지 이동은 발생 원인과 무관하다고 답함','body L1–13','answer_to_new_question','not_Q'),
7: ('third_party','row_size_estimate','앞 답의 row 크기 추정을 반박하고 100만 행 실측을 보고','body L1–28','third_party_reproduction','not_author_value'),
8: ('new_requirement','in_place_semantics','서로 다른 답 때문에 in-place가 가능한지 다시 질문; 앞의 추가 질문 범위에 속함','body L1–5','new_question_scope','new_scope_not_T0_condition'),
},
'S08': {
1: ('third_party','SQL_quoting_and_NOT_NULL','인용 부호와 여섯 NOT NULL 입력을 지적; 바인딩은 직접 고치지 않음','body L1–8','proposed_fix','not_new_author_fact'),
2: ('author_existing_fact','schema_change_and_failure','그 조언을 따랐지만 같은 오류라고 보고; duration 대신 cascade_name과 id만 남기도록 스키마를 바꿈','body L1','reported_failure;changed_implementation','Q_value_already_T0'),
}}

followups=[]
for case,ann in annotations.items():
    original=bycase[case]
    for n,values in ann.items():
        r=meta(case,n);c=r['cards']
        classification,variable,value,loc,action,relation=values
        isauthor=c.get('U')==meta(case,0)['cards'].get('U')
        followups.append(dict(case_id=case,message_id=r['artifact_id'],url=url(case,n),
            occurred_utc=c['D']+'Z',actor=c.get('U'),role='question_author' if isauthor else 'other_participant',
            reply_to=c.get('I',''),classification=classification,variable=variable,value=value,
            within_30_days=hours(original['submitted_utc'],c['D'])<=720,action=action,locator=loc,
            censoring='deleted_revision;original_recoverable' if n==3 and case=='S02' else '',
            frozen_variable_relation=relation,is_edit_of=c.get('P',''),body_sha256=r['body_sha256'],
            within_90_days=hours(original['submitted_utc'],c['D'])<=2160,
            source_id='S-'+case,original_artifact=r['artifact_id'],
            researcher_note='Q는 실제 발송되지 않음. classification은 원 대화의 발화 관계임.'))
writecsv('followups.csv',followups)

clar_pairs={
 'S01':[(2,3,'filesystem_permission'),(4,5,'extended_error_code'),(7,8,'buffer_and_quoting')],
 'S04':[(3,4,'language_wrapper_restart'),(1,5,'transaction_granularity'),(6,7,'reproduction_details')]
}
clar_pending={'S02':[1],'S04':[2],'S07':[1]}

specific={
'S01':dict(q_variable_status='already_in_T0',q_variable_qualification='생성 의도는 최초 요청에 이미 있음. CREATE 플래그라는 기술 사실은 Q의 답이 아님.',
  change='selection_maintained;author_progress_report_added',I_scope='새 ATTACH 파일 생성이라는 제시된 코드 문제',C_scope='새 파일/기존 파일의 open 플래그 분기',
  full_goal=True,full_I=True,full_C=True,progress_n=15,failure_n=None,
  limitation='S01은 봉인 전 답 한 문장 노출로 엄격 전향 비교에서 제외. 실제 성공은 작성자 보고이며 연구자의 실행이 아님.',
  alternatives=['즉답+플래그 근거 링크','현재 목적을 명시한 조건부 두 경로'],
  new_requirement='author_late_preference;temporal_status_unknown',
  retro='모든 DB open에서 CREATE 금지라는 필수 조건을 T0에 소급하면 단순 A 승인이 탈락한다. 실제로는 늦게 표현된 선호이며 발생 시점은 미상; 파일 존재 선검사라는 새 절충 제안까지 원 질문에 강제하지 않는다.'),
'S02':dict(q_variable_status='already_in_T0',q_variable_qualification='-o mysql과 ./ex1.db가 원 로그에 있음. 실제 답변도 이 사실만으로 수정 가능.',
  change='selection_maintained;author_outcome_unreported',I_scope='실행 파일/데이터 파일 혼동 해소',C_scope='같은 실행 오류의 두 파일 역할 설명',
  full_goal=False,full_I=False,full_C=False,progress_n=None,failure_n=None,
  limitation='C로 실제 데이터를 조회한다는 넓은 목표에는 SELECT가 빠져 있다. 실행 성공조차 작성자 후속이 없어 미확인.',
  alternatives=['즉답+컴파일러 근거 링크','제시 코드가 연결만 열고 조회는 하지 않음을 명시'],new_requirement='none_observed',retro='후속 요구 없음; 소급 비교 해당 없음.'),
'S03':dict(q_variable_status='no_author_value',q_variable_qualification='OFF 유지가 필수인지 작성자는 답하지 않았다. 이 값을 몰라도 원래 교체할 view의 순서를 바꾸는 A는 유지.',
  change='selection_maintained;safe_primary_not_changed_by_Q',I_scope='제시된 migration의 깨진 view 선제 제거',C_scope='OFF 유지 시 A; legacy 허용이면 추가 검토를 붙인 B',
  full_goal=True,full_I=True,full_C=True,progress_n=None,failure_n=None,
  limitation='공식 3.34.0 테스트·구현으로 경로를 판정했지만 저자의 실제 적용이나 migration 성공은 보고되지 않음.',
  alternatives=['즉답으로 A 제안','C로 legacy 대안과 한계 병기'],new_requirement='none_observed',retro='OFF를 변경 금지로 소급해도 A는 유지되고 B만 제외된다. 예제 설정은 금지 발언이 아니다.'),
'S04':dict(q_variable_status='author_existing_fact',q_variable_qualification='author_assertion_conflicted: committed라고 주장했으나 성공 반환은 명시하지 않았고 후속 코드·로그와 충돌.',
  change='still_unknown;assertion_requires_reconciliation',I_scope='원인·성공 commit 판정 보류',C_scope='미확정 INSERT/성공 commit 뒤 조사라는 설명; 실제 분기는 보류',
  full_goal=False,full_I=False,full_C=False,progress_n=None,failure_n=8,
  limitation='작성자의 committed라는 말, COMMIT 없는 직접 C API 재현, commit 실패 로그를 어느 하나로 덮지 않는다. 앞서 FMDB라고 설명한 원앱과 후속 재현 코드가 동일한 완전 실행인지 미확인이다. 성공 반환 증거 미달이며 주장이 거짓이라고 확정하지 않는다.',
  alternatives=['보류와 성공 반환/재현 로그 한 항목 요청','조건부 설명하되 장치 원인 확정 보류'],new_requirement='new_symptom_corruption;not_new_requirement',
  retro='뒤에 보고된 손상을 T0의 필수 진단으로 소급하면 단순 rollback 설명은 불충분해진다. 그것은 뒤에 추가된 증상이며 T0에 있었음은 미확인.'),
'S05':dict(q_variable_status='third_party_only',q_variable_qualification='제3자가 serialized 조건을 제시했지만 실제 연결 mode 값은 한 번도 제시되지 않음.',
  change='still_unknown;no_author_mode_or_execution',I_scope='threading mode와 성능 판정 보류',C_scope='API mutex 조건 설명만; statement 재사용 순서와 성능은 승인하지 않음',
  full_goal=False,full_I=False,full_C=False,progress_n=None,failure_n=None,
  limitation='serialized는 논리적 다중 호출 작업을 원자화하지 않는다. 같은 statement를 reset 후 column 조회하면 계약상 유효 행 조건이 사라진다. 실제 OP가 이 순서였다는 증거는 없다.',
  alternatives=['한 변수 Q는 mutex 조건만 좁힘','C와 함께 실제 statement 수명·순서 검토는 보류'],new_requirement='none_observed',retro='성능 선호를 필수로 소급하면 A/B 모두 성능 근거가 없어 탈락하나, 원문의 우선순위는 그렇게 확정되지 않는다.'),
'S06':dict(q_variable_status='no_author_value',q_variable_qualification='가능할 수도 있다는 반응은 source 형태나 정확한 버전의 답이 아니다.',
  change='still_unknown;tentative_candidate_interest_only',I_scope='당시 custom include 대안 존재 소개, 실제 원인 보류',C_scope='amalgamation/split source를 나눈 후보 안내, 실제 판과 성공 보류',
  full_goal=False,full_I=False,full_C=False,progress_n=None,failure_n=None,
  limitation='감사·가능성 표현을 사용 성공으로 세지 않는다. 연결된 2021 대화의 다른 사용자의 성공을 이 작성자에게 이전하지 않는다.',
  alternatives=['C로 custom include 조건 안내','Q 한 번과 실제 배포판 확인 필요','설치 원인 판정 보류'],new_requirement='none_observed;documentation_wish_repeated',retro='문서 수정 희망은 처음부터 있던 의문의 연장; 새 필수 요구로 소급할 근거 없음.'),
'S07':dict(q_variable_status='already_in_T0',q_variable_qualification='첫 글에 PG autovacuum daemon이 명시되어 일반 VACUUM/FULL 선택을 다시 물을 필요가 없음.',
  change='selection_maintained;separate_followup_scope_added',I_scope='PG 공간 반환 불가라는 단정의 정정',C_scope='PG 일반/FULL 및 SQLite FULL의 제한된 공간 반환 비교',
  full_goal=True,full_I=False,full_C=True,progress_n=None,failure_n=None,
  limitation='링크가 더 자세하다는 읽기 보고는 있지만 최초 비교의 해결·사용 성공 보고는 없음. 후속은 UPDATE/DELETE 및 in-place 의미로 범위 확장.',
  alternatives=['근거 링크로 PG 예외 즉답','C로 일반 VACUUM/FULL 구별'],new_requirement='new_question_scope;original_goal_not_replaced',
  retro='UPDATE/DELETE의 물리 쓰기를 T0 필수 조건으로 소급하면 기존 A 비교 답이 불충분해진다. 후속 질문을 최초 목표로 바꾸는 오류다.'),
'S08':dict(q_variable_status='already_in_T0',q_variable_qualification='req.body.duration의 JS 값임은 원 코드에 있음. 작성자 후속은 값 확인이 아니라 조언 실행 실패와 스키마 변경.',
  change='selection_maintained;different_real_advice_failed',I_scope='parameter 바인딩 및 필수 열 입력',C_scope='JS 값과 SQL 식별자 구별; NOT NULL 전체 조건은 C에 빠짐',
  full_goal=True,full_I=True,full_C=False,progress_n=None,failure_n=2,
  limitation='실제 답변은 인용 부호와 NOT NULL을 지적했고 작성자는 같은 오류라고 보고. 봉인 I/C는 실제 전송되지 않았으며 그 실패를 I/C의 결과로 세지 않음.',
  alternatives=['I로 바인딩과 NOT NULL을 함께 안내','C에는 원래 필수 열 조건을 보강해야 전체 삽입 조언이 됨'],new_requirement='changed_implementation;not_proven_changed_goal',
  retro='두 열로 줄인 후속 스키마를 T0로 소급하면 여섯 NOT NULL 문제를 놓친다. 원 스키마와 바뀐 재현을 별도 판으로 유지한다.'),
}

analyses=[]
for c in initial:
    case=c['case_id'];d=specific[case];fr=next(x for x in frozen if x['case_id']==case)
    pairs=[]
    for ask,answer,var in clar_pairs.get(case,[]):
        pairs.append(dict(request_id=ident(case,ask),request_url=url(case,ask),answer_id=ident(case,answer),
             answer_url=url(case,answer),variable=var,
             wait_hours=hours(meta(case,ask)['cards']['D'],meta(case,answer)['cards']['D']),same_as_frozen_variable=False))
    authorposts=[r for r in followups if r['case_id']==case and r['role']=='question_author' and r['action']!='root_edit' and not r['is_edit_of']]
    first_author=min([r['occurred_utc'] for r in authorposts],default=None)
    narrow=case in ['S01','S02','S03','S07','S08']
    strategies={}
    for k in ['I','C']:
        strategies[k]=dict(technical_status='supported_limited' if narrow else 'hold',
            supported_claim_scope=d[k+'_scope'],approval_for_entire_goal=d['full_'+k] if narrow else False,
            conditional_claims_supported=True,actual_message_sent=False,
            supplied_links=len(__import__('re').findall(r'https?://',fr[k])),
            author_implementation_of_this_message='not_observed;message_was_not_sent',
            expected_additional_roundtrips_lower_bound=0,
            roundtrip_expectation_status='researcher_counterfactual;hold_does_not_equal_resolution')
    strategies['Q']=dict(technical_status='question_not_approval',actual_message_sent=False,
        already_known=case in ['S01','S02','S07','S08'],value_usable_from_new_author_followup=False,
        known_T0_value_can_fill=case in ['S01','S02','S07','S08'],
        direct_answer_to_same_variable_in_actual_thread=False,
        expected_additional_roundtrips_if_answered=1,
        expected_wait_hours=None,expectation_status='hypothetical_minimum;no_causal_time_saving_estimate',
        new_value_alone_sufficient_for_original_goal=False)
    a=dict(case_id=case,family='SQLite Forum',global_seal_commit=SEAL,
        original_confirmed=True,strict_preoutcome_eligible=case!='S01',
        followup_first_thread_fetch_utc=thread[case]['checked_utc'],
        q_variable=c['missing_variable'],q_variable_status=d['q_variable_status'],
        q_variable_qualification=d['q_variable_qualification'],
        q_value_recovered_strict=False,q_value_claim_available_sensitivity=case=='S04',
        q_value_claim_conflicted=case=='S04',
        q_value_already_available_in_T0=case in ['S01','S02','S07','S08'],
        q_new_usable_author_value_count=0,judgment_change=d['change'],
        proposal_changed_because_of_new_Q_value=False,
        technical_false_approval_observed=False,unsupported_full_goal_approval_made=False,
        T0_facts_sufficient_for_bounded_next_action=narrow,
        T0_facts_sufficient_for_entire_original_goal=d['full_goal'],
        strategies=strategies,
        actual_author_reports_progress=d['progress_n'] is not None,
        actual_author_reports_progress_url=url(case,d['progress_n']) if d['progress_n'] is not None else None,
        actual_progress_kind='own_test_app_resolved_with_code_and_contrast' if d['progress_n'] is not None else 'none_observed',
        actual_author_reports_failure=d['failure_n'] is not None,
        actual_author_reports_failure_url=url(case,d['failure_n']) if d['failure_n'] is not None else None,
        actual_failure_scope='failure_of_other_advice_or_reported_scenario;not_frozen_I_C' if d['failure_n'] is not None else None,
        actual_author_reports_source_consultation=case=='S07',
        source_consultation_url=url(case,3) if case=='S07' else None,
        actual_clarification_roundtrips=len(pairs),
        actual_clarification_definition='실제 응답자의 구체적 정보/재현 요청에 작성자가 reply 관계로 응답한 쌍; 편집·단순 감사·저자의 새 질문은 제외; 한 요청의 여러 질문은 왕복 한 번.',
        actual_clarification_pairs=pairs,
        actual_unanswered_clarification_requests=[url(case,n) for n in clar_pending.get(case,[])],
        actual_author_followup_turns=len(authorposts),
        wait_hours=hours(c['submitted_utc'],first_author) if first_author else None,
        wait_hours_definition='최초 제출부터 첫 작성자 후속까지의 달력 구간; 응답 의무·인지 처리 시간 아님. 작성자 후속 없으면 null 및 30일 검열.',
        wait_first_reply_hours=hours(c['submitted_utc'],c['first_reply_utc']),
        wait_to_progress_hours=hours(c['submitted_utc'],meta(case,d['progress_n'])['cards']['D']) if d['progress_n'] is not None else None,
        total_thread_elapsed_hours=hours(c['submitted_utc'],max(meta(case,n)['cards']['D'] for n in range(len(thread[case]['artifact_ids'])))),
        window30_end=(stamp(c['submitted_utc'])+dt.timedelta(days=30)).isoformat(),
        window90_end=(stamp(c['submitted_utc'])+dt.timedelta(days=90)).isoformat(),
        censoring30='원 대화 전체 읽음; 30일 안 작성자 후속 없음(거절/실패 아님)' if not authorposts else '원 대화 전체 읽음; 보고된 내용만 관측; 미답 변수는 미확인',
        followup_90_days=dict(same_thread_31_to_90_events=0,separate_linked_implementation='미확인',
           author_report_within90='own_test_app_fix_and_reproduction' if case=='S01' else 'reproduction_code_without_resolved_commit_boundary' if case=='S04' else 'reported_schema_change_and_persistent_error' if case=='S08' else 'none_observed',
           author_report_within90_url=url(case,15) if case=='S01' else url(case,8) if case=='S04' else url(case,2) if case=='S08' else None,
           report_period='within_first30;not_additional_days31to90' if case in ['S01','S04','S08'] else 'none_observed',
           searched='원 thread 모든 글/편집과 링크를 검토. S06의 과거 2021 지원 대화는 다른 사건이라 사용 성과에서 제외.',
           limitation='8개 원 thread에는 31–90일 메시지나 작성자 별도 구현으로 이어지는 명시 링크 없음. 계정 전역 검색으로 동일인을 추정하지 않음.'),
        requirement_change_status=d['new_requirement'],new_requirement_retroactive_sensitivity=d['retro'],
        available_alternatives=d['alternatives'],limitations=d['limitation'],
        independent_coder=False,reader='/root/sqlite',self_review_only=True)
    a['actual_conditional_answer_with_author_confirmed_resolution']=False
    a['conditional_resolution_search']='8개 고정 thread의 첫 답·작성자 후속 전체에서 확인. S03/S05 조건부 답은 있으나 성공 보고 없음; S06 가능성 반응은 성공이 아님.'
    a['additional_fact_preserves_both_frozen_candidate_verdicts']=(
        dict(fact='생성 권한/여러 경로가 가능하다는 작성자 답',url=url(case,3),locator='body L1–3',
             A='supported→supported',B='new-file R1 conflict→conflict',
             limit='제한된 봉인 후보 A/B의 판정이 유지됐다는 뜻. 다른 권한 원인 가설 전반에 쓸모없다는 뜻 아님.') if case=='S01' else
        dict(fact='Objective-C/FMDB wrapper와 전원+홈 재시작 방식',url=url(case,4),locator='body L1–10',
             A='unknown→unknown',B='unknown→unknown',
             limit='성공 COMMIT를 확인하지 못하므로 고정 A/B의 갈림은 풀리지 않음. wrapper는 후속 재현 검증에 관련될 수 있음.') if case=='S04' else None)
    a['public_reply_claim_conflict']=(
        dict(reply_url=url(case,2),reply_locator='body L1',technical_source='S-D11',
             technical_locator='maintenance.sgml L156–194',
             scope='작성자의 PG 반환 불가 가설에 대한 제3자의 유보적 동의가 공식 일반 VACUUM 끝 페이지 예외와 충돌; 봉인 I/C의 오승인이 아님.') if case=='S07' else
        dict(reply_url=url(case,1),reply_locator='body L3–4',technical_source='S-TD01',
             technical_locator='parse.y L306–309,L971–977,L1006–1016',
             scope='작은따옴표 열 이름은 불가라는 실제 조언의 명제가 해당 SQLite parser 허용과 충돌; 바인딩 문제·전체 실행 성패와 별개.') if case=='S08' else None)
    analyses.append(a)
(P/'case-analysis.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in analyses))

# Every frozen candidate × every frozen requirement × both timepoints.
# Additional interpretation conditions stay explicit, never silently change T0 requirements.
judgments=[]
for c in initial:
    case=c['case_id']
    for cand in c['candidate_uses']:
        for req in c['requirements']:
            for tp in ['T0','T1']:
                verdict='unknown';ids=[cand['source_id']];note='설치판·실제 실행 또는 이 조건에 대한 근거가 부족해 미확인.'
                if case=='S01':
                    ids=['S-D01','S-D02']
                    if req['id'] in ['R1','R2']:
                        verdict='supported' if cand['id']=='A' or req['id']=='R2' else 'conflict'
                        note='CREATE 허용 A는 새 ATTACH 목적과 맞고, 기존 파일 전용 B는 생성 필수 R1과 충돌.'
                    if req['id']=='R3' and tp=='T1': note='작성자는 3.37과 다른 판 재현을 명시했으나 patch 판/VFS 전체는 미확인.'
                    if req['id']=='R4' and tp=='T1':
                        verdict='supported';note='후속 실제 재현은 :memory: 입력을 명시하며 플래그 유무를 비교. 최초판 로그 불일치를 소급 삭제하지 않음.'
                elif case=='S02':
                    ids=['S-D03','S-D01']
                    if req['id']=='R2': verdict='supported';note='-o의 결과 mysql을 실행하는 것으로 로그의 대상 혼동을 정정; 실제 실행은 미보고.'
                    elif req['id']=='R1': note='C 연결 생성은 부합하지만 데이터 조회 SQL은 없어 넓은 읽기 목표 완료는 미확인.'
                elif case=='S03':
                    ids=['S-D04','S-D05']
                    if req['id'] in ['R1','R2'] and cand['id']=='A':
                        verdict='supported';note='제시 데이터 전달 SQL은 유지하고 교체 예정 view의 제거를 rename 전으로 이동; 공식 broken-view 테스트와 같은 실패 경계.'
                    elif req['id']=='R4': verdict='supported';note='외래키 단계 n/a는 금지 아님; 샘플에 해당하지 않음.'
                    elif req['id']=='R3': note='OFF 유지 필수 여부는 T1에도 없음. A를 제안하는 데 그 답은 필요하지 않음.'
                elif case=='S04':
                    ids=['S-D06','S-D07']
                    if tp=='T1': note='commit 소실 주장과 COMMIT 없는 재현/실패 로그가 충돌하여 실제 손실 원인·분기 미확인.'
                    else: note='rowid는 뒤에 rollback될 수 있음. 성공 COMMIT 여부가 없어 A/B를 실제 원인으로 선택하지 않음.'
                elif case=='S05':
                    ids=['S-D01']
                    note='mode 미상. serialized API mutex와 다중 호출 순서/statement 유효성·성능 보증을 구별.'
                elif case=='S06':
                    ids=['S-D08','S-D09']
                    if req['id']=='R2': verdict='supported';note='A/B 모두 왜 여러 빌드 시스템인지 다시 묻지 않음.'
                    else: note='비교판의 경로는 존재하나 실제 source 형태/설치판을 모름. could work는 사용 성공 아님.'
                elif case=='S07':
                    ids=['S-D10','S-D11']
                    if req['id']=='R1':
                        verdict='supported' if cand['id']=='A' else 'conflict';note='일반 autovacuum 비교 A가 최초 목적. B는 autovacuum이 실행하지 않는 별도 FULL의 비교로 범위를 바꿈.'
                    elif req['id']=='R3': verdict='supported';note='개념 비교에 특정 운영 인스턴스 설정은 불필요. 새 운영 요구가 생겼다는 증거 없음.'
                elif case=='S08':
                    ids=['S-D01','S-D12']
                    if req['id']=='R1':
                        verdict='supported' if cand['id']=='A' else 'conflict';note='JS 값은 parameter 바인딩으로 전달. bare duration은 JS 변수 대체가 아님.'
                    elif req['id']=='R2':
                        ids=['S-TD02']
                        verdict='supported' if cand['id']=='A' else 'unknown';note='A는 나머지 NOT NULL 열도 공급하도록 명시. T1의 축소 스키마를 T0에 소급하지 않음.'
                        note+=' T1 추가 판독한 동일 비교판 회귀 테스트로 원조건을 사후 검증한 것이며, 동결 입력에 있던 테스트로 소급하지 않음.'
                tsources=[source[i] for i in ids]
                action='no_report';actionurl='';actionloc=''
                if case=='S01' and tp=='T1' and (cand['id']=='A' and req['id'] in ['R1','R2'] or cand['id']=='B' and req['id']=='R1'):
                    action='reported_progress' if cand['id']=='A' else 'reported_failure'
                    actionurl=url(case,15);actionloc='body L16–18,L35–59'
                    if cand['id']=='B': note+=' 작성자의 실패는 CREATE 없는 플래그로 새 대상을 생성하려 한 비교 실험이며, 기존 파일 전용 B 사용 자체의 실패를 뜻하지 않음.'
                elif case=='S08' and tp=='T1':
                    note+=' 작성자의 실패는 다른 실제 조언/변경 스키마에 관한 것으로 봉인 A/B 실행 결과가 아님.'
                judgments.append(dict(case_id=case,candidate_id=cand['id'],condition_id=req['id'],condition_kind=req['kind'],
                    timepoint=tp,technical_verdict=verdict,technical_source_ids=';'.join(ids),
                    technical_url=';'.join(s['url'] for s in tsources),
                    technical_locator=';'.join(i+': '+source[i]['read_locations'] for i in ids),
                    action_verdict=action,action_url=actionurl,action_locator=actionloc,note=note,
                    condition_url=req['url'],condition_locator=req['locator'],
                    actual_version_scope=cand['version'],
                    source_and_actor_separate=True))

# Extra counterexample rows preserve the frozen R1 while distinguishing its sub-boundaries.
for candidate in ['A','B']:
    for tp in ['T0','T1']:
        for cond,loc,note in [
            ('R1-multicall-order','L4904–4914; L5050–5054; L5117–5141','원판의 같은 statement인지 미상. step(ROW) 뒤 타 thread reset, 뒤 column 조회라는 순서는 문서 계약을 어기므로 mode 하나로 전체 알고리즘을 승인할 수 없다. 연구자 반례이며 실제 OP 수행/이번 실행 아님.'),
            ('R2-speed','L1761–1789; L7654–7662','mutex는 대기를 포함할 수 있다. 성능 향상 측정은 없음; 성능 선호를 안전성과 동일 조건으로 합치지 않음.')]:
            judgments.append(dict(case_id='S05',candidate_id=candidate,condition_id=cond,
                condition_kind='required' if cond.startswith('R1') else 'preference',timepoint=tp,
                technical_verdict='unknown',technical_source_ids='S-D01',technical_url=source['S-D01']['url'],
                technical_locator=loc,action_verdict='no_report',action_url='',action_locator='',note=note,
                condition_url=bycase['S05']['root_url'],condition_locator='원문 L1–8',actual_version_scope='3.37.1 comparison',source_and_actor_separate=True))
writecsv('judgments.csv',judgments)

# Reuse source IDs; observations do not add a second original to minimum counts.
t1sources=[]
for c in initial:
    case=c['case_id'];old=source['S-'+case];r=dict(old)
    r.update(observation_id='S-'+case+'-T1',related_q=['Q4','Q5','Q6','Q8'],
        url=thread[case]['url'],fixed_version='Fossil artifacts listed in followup-metadata.json; original lineage '+ident(case,0),
        checked_utc=thread[case]['checked_utc'],
        read_locations='원 thread 전체 원글·답·편집; '+', '.join('artifact '+ident(case,n)[:12]+' '+annotations[case][n][3] for n in annotations[case]),
        observed=specific[case]['change']+'; '+specific[case]['q_variable_qualification'],
        limitations=specific[case]['limitation']+' 31–90일 동일 thread 추가 발화 없음; 연결되지 않은 별도 구현은 미확인.',
        count_in_minimum=False,count_reason='이미 T0의 S-'+case+'를 대화 1건으로 셈. 댓글·개정은 고유 원문을 추가하지 않음.',
        kind='conversation_followup_observation',lineage='same conversation as S-'+case)
    t1sources.append(r)
r=dict(source['S-D01']);r.update(observation_id='S-D01-T1',related_q=['Q5','Q6','Q8'],case_ids=['S05'],checked_utc=NOW,
    read_locations='L1761–1789; L4904–4914; L5050–5054; L5117–5141; L7654–7662',
    observed='동일 statement의 reset은 현재 row/결과 pointer 수명을 끝낼 수 있다. serialized API 접근 계약과 재사용 작업 순서·성능의 보증은 다르다.',
    limitations='정적 문서 반례; 실제 작성자 sequence/mode는 여전히 미상. undefined 행동을 실행한 테스트가 아님.',
    count_in_minimum=False,count_reason='동일 S-D01 재독, 원문 추가 0',kind='provider_document_followup_observation')
t1sources.append(r)
r=dict(source['S-D12']);r.update(observation_id='S-D12-T1-location-audit',related_q=['Q2','Q5'],case_ids=['S08'],checked_utc=NOW,
    read_locations='L1; L24–46; L51; L58',
    observed='당시 package README는 비동기 binding과 callback 예제를 명시. v5.0.2의 fallback SQLite는 3.32.3으로 적혀 있다.',
    limitations='OP package 판은 미상이다. 봉인의 별도 SQLite 3.37.1 비교판을 node-sqlite3v5.0.2 실제 bundle판으로 취급하지 않음. 현재 재독은 T0 필드의 위치 감사이며 후속 사실을 T0에 추가하지 않음.',
    count_in_minimum=False,count_reason='동일 S-D12 재독, 원문 추가 0',kind='provider_document_followup_observation')
t1sources.append(r)
t1sources.append(dict(id='S-TD01',related_q=['Q5','Q6'],case_ids=['S08'],
    url='https://github.com/sqlite/sqlite/blob/57acbb1380e3b51476aa8c71d1a881821f8ad5ff/src/parse.y',
    published_or_revised='2021-12-30T15:30:28Z (version commit)',fixed_version='SQLite 3.37.1 / 57acbb1380e3b51476aa8c71d1a881821f8ad5ff',checked_utc=NOW,
    read_locations='L306–309 nm::=STRING; L971–977 INSERT idlist_opt; L1006–1016 idlist::=nm',
    observed='INSERT 열 목록의 nm는 STRING 토큰도 수용. 실제 첫 답의 단일 인용 열 이름 불가라는 무조건 명제는 이 SQLite parser 경로와 일치하지 않음. VALUES의 bare identifier/바인딩은 별도 문제.',
    limitations='정적 parser 판독이며 사용자 정확한 설치판과 NodeJS 동작의 실행 검증은 아님.',producer='SQLite maintainers',lineage='sqlite/sqlite source tree; S-D01 same producer',
    count_in_minimum=False,count_reason='구현 소스로 반증 지원; 공식 문서/테스트 최소수에는 추가하지 않음.',kind='provider_implementation'))
t1sources.append(dict(id='S-TL06',related_q=['Q4','Q5','Q6'],case_ids=['S06'],
    url='https://sqlite.org/forum/forumpost/9f431ed4c1f6e82e7a32ad103cb57229df98b83c26f6420e115f3a2dea9989f5?t=r',
    published_or_revised='2021-12-03 23:59:56–2021-12-04 01:48:06 UTC',
    fixed_version='Fossil root 9f431ed4c1f6e82e7a32ad103cb57229df98b83c26f6420e115f3a2dea9989f5',checked_utc=NOW,
    read_locations='posts 1–4; post2 a47c8e944507b0c92f3cdcf882c2ab590218da783296677c97ba0d367c48723a; post3 c68a8bb935cb2fbc15ad847b99b0e7e843caf70435bb51b4a9adbb678b9b785c',
    observed='S06 실제 답이 연결한 이전 지원 대화. 3.37 custom include 사용을 컴파일 옵션/OPTS로 설명하고 마지막 anonymous가 동작했다고 보고.',
    limitations='24건 표본 밖의 과거 대화. anonymous 발화들의 계정 동일성 불명이며 S06 marcob의 성공 근거가 아님. 별도 채택 사례로 더하지 않음.',
    producer='SQLite Forum participants',lineage='linked by S06 actual reply 61e23ba463b1; different root conversation',
    count_in_minimum=False,count_reason='사전에 고른 24건 밖이며 후속 링크 검토용; 최소수·진전 분자에 추가하지 않음.',kind='linked_conversation_outside_frame'))
t1sources.append(notnull_source)
writejson('t1-sources.json',t1sources)

counts=dict(cases=8,original_confirmed=8,strict_preoutcome_eligible=7,
    artifacts_including_roots_and_edits=len(metadata),non_original_artifact_rows=len(followups),
    raw_id_hash_verified=sum(r.get('id_matches_raw_sha3',False) for r in metadata),
    frozen_messages=24,already_T0_variable_values=4,
    new_direct_same_variable_answers=0,new_usable_author_variable_values=0,
    author_claim_conflicted=1,conditional_claim_sensitivity_upper_new_values=1,
    I_supported_limited=5,I_hold=3,C_supported_limited=5,C_hold=3,
    I_full_original_goal_advice=3,C_full_original_goal_advice=3,
    T0_facts_sufficient_bounded_next_action=5,T0_facts_sufficient_original_goal_advice=4,
    same_candidate_proposal_changes_due_Q=0,actual_false_approvals_frozen=0,
    author_progress_reports=1,strict_eligible_author_progress_reports=0,
    author_failure_reports_other_interventions=2,source_consultation_reports=1,
    completed_actual_clarification_roundtrips=sum(x['actual_clarification_roundtrips'] for x in analyses),
    unresolved_actual_clarification_requests=sum(len(v) for v in clar_pending.values()),
    no_author_followup_cases=['S02','S03','S05'],
    clear_new_requirement_replacing_T0_goal=0,new_followup_question_scope_cases=['S07'],
    actual_conditional_answer_with_author_confirmed_resolution=0,
    additional_fact_both_frozen_verdicts_unchanged_cases=['S01','S04'],
    public_reply_claim_conflict_cases_not_frozen_strategy=['S07','S08'],
    late_preference_temporal_status_unknown_cases=['S01'],
    same_thread_days31to90_messages=0,separate_linked_author_implementation_confirmed=0,
    deleted_revision_with_recoverable_original=1,
    counted_unique_originals_T0=16,new_counted_provider_tests_T1=1,counted_unique_originals_total=17,
    counted_provider_originals_total=9,provider_manual_or_tests_only_sensitivity=7,
    notes='sufficient counts concern the bounded technical advice; not success rates, randomized strategies or causal effects. C/I hold rows are not approvals.')
# Derive full-goal message counts rather than trust prose.
for k in ['I','C']:
    counts[k+'_full_original_goal_advice']=sum(x['strategies'][k]['approval_for_entire_goal'] for x in analyses)
counts['strict_sensitivity']={
    'denominator':7,'I_supported_limited':4,'I_hold':3,'C_supported_limited':4,'C_hold':3,
    'I_full_original_goal_advice':2,'C_full_original_goal_advice':2,
    'T0_facts_sufficient_bounded_next_action':4,'T0_facts_sufficient_original_goal_advice':3,
    'already_T0_variable_values':3,'new_usable_author_values':0,'author_progress_reports':0,
    'author_assertion_conflicted':1,
    'reason':'S01 excluded because reply snippet exposure before freeze; originals remain confirmed 8/8.'}
counts['direct_same_variable_answer_denominator']={'cases':0,'rates':'해당 없음(0/0); 0%로 쓰지 않음'}
counts['unknown_original_extreme_bounds']={'unknown_originals':0,'lower':0,'upper':0,
    'note':'SQLite 원판 미확인 사례는 0; 봉인 전 노출 S01의 별도 민감도와 혼합하지 않음.'}
writejson('t1-counts.json',counts)

cf=[
 dict(case_id='S04',label='author_assertion_is_not_verified_success_return',
      premise='committed라는 작성자의 말을 곧바로 성공 COMMIT 반환값으로 대체',
      possible_wrong_decision='A rollback 경로를 부당 탈락시키고 B 장치·sync 문제를 확정 원인으로 승인',
      actual_frozen_decision='I 보류, C 조건부 설명과 원인 보류; 실제 오승인 관측 아님',
      urls=';'.join([url('S04',5),url('S04',8),url('S04',9)]),
      locations='2070eae6 body L1–2; 8a24d27a L7–23,L28–35; 307beed3 L1–44',
      next_minimum='원앱/재현의 계보가 연결된 완전 트랜잭션 코드와 손실 행 COMMIT 성공 반환 로그'),
 dict(case_id='S05',label='serialized_not_multicall_atomicity',
      premise='serialized mode 한 값만 알면 같은 statement 재사용 전체가 안전하고 더 빠르다고 승인',
      possible_wrong_decision='step(ROW)→다른 thread reset→column 조회의 유효성 위반 가능성을 놓침',
      actual_frozen_decision='I 보류, C는 API mutex 범위에만 성립; 실제 작성자 순서/충돌은 미확인',
      urls=source['S-D01']['url'],locations='L1761–1789,L4904–4914,L5050–5054,L5117–5141',
      next_minimum='같은 statement 여부·호출 소유권/수명·실효 mode를 표시한 최소 trace와 실제 timing'),
 dict(case_id='S01',label='late_preference_retrojected_as_prohibition',
      premise='뒤에 밝힌 모든 open의 자동 CREATE를 원치 않는 선호를 T0 필수 금지로 소급',
      possible_wrong_decision='처음 목적에 맞고 실제 성공한 CREATE 플래그 제안을 부당 탈락',
      actual_frozen_decision='당시 A 유지; 선호의 발생 시점 미확인; 노출 사례라 전향 전략 비교에서 제외',
      urls=url('S01',15),locations='body L57–59',
      next_minimum='이 선호가 처음부터 필수였다는 당시 기록 또는 이후 새로 생긴 제약의 명시'),
 dict(case_id='S07',label='later_question_replaces_original_goal',
      premise='후속 UPDATE/DELETE/in-place 질문을 처음부터 필요했던 필수 조건으로 소급',
      possible_wrong_decision='공간 반환 비교 답을 최초 목표의 불충분한 답으로 재분류',
      actual_frozen_decision='원 비교 A 유지; 추가 질문은 새 범위이며 원 목적 대체 증거 없음',
      urls=';'.join([url('S07',4),url('S07',8)]),locations='99729da1 body L1–4; 213694d4 L1–5',
      next_minimum='작성자가 원래 판단하려던 실제 사용 목적과 추가 질문이 그것에 필수였음을 연결한 말'),
 dict(case_id='S08',label='other_intervention_outcome_not_our_strategy',
      premise='작성자가 실제 타인의 조언 후 실패했으므로 봉인 I/C도 실패했다고 코딩',
      possible_wrong_decision='전송하지 않은 parameter 바인딩 조언에 실패를 귀속',
      actual_frozen_decision='실제 조언은 인용·NOT NULL 중심; I/C는 미전송이며 판정·실행 결과를 분리',
      urls=';'.join([url('S08',1),url('S08',2)]),locations='64a2ccd5 body L1–8; b3d355a0 L1',
      next_minimum='실제로 실행한 변경 SQL·bind 인자·schema와 오류 로그의 동일판 기록')]
writecsv('counterfactual-audit.csv',cf)

receipt=json.loads((P/'t1-receipt.json').read_text())
receipt.update(completed_utc=NOW,status='annotated_T1_self_review',
  artifact_count=len(metadata),artifact_hashes_confirmed=counts['raw_id_hash_verified'],
  unchanged_T0_sha256={name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in ['initial.jsonl','frozen-responses.jsonl','frame.csv','sources.json']},
  raw_503_recovered=[r['artifact_id'] for r in metadata if 'previous_error' in r],
  note='Some first batch outputs were truncated; full S02–S08 thread bodies were re-opened in bounded batches and key raw posts re-read with line numbers. No source full bodies persisted.')
writejson('t1-receipt.json',receipt)
print(json.dumps(counts,ensure_ascii=False,indent=2))
