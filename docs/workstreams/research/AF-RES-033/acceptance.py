"""Write condition-level acceptance evidence without hiding protocol deviations.

The pre-seal version truthfully leaves fixed-result verification pending. A
later version may mark it met only from actual fixed-commit execution/read
receipts. The final HANDOFF verifies the resulting acceptance commit again.
"""
import argparse
import datetime
import json
from hashlib import sha256
from pathlib import Path

P=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--verified-result');args=parser.parse_args()
def jl(name):return [json.loads(x) for x in (P/name).read_text().splitlines() if x.strip()]
def ev(name,scope=None):
    path=P/name
    return {'file':name,'lines':[1,len(path.read_text().splitlines())] if path.exists() else None,
        'scope':scope or 'Whole named evidence file; see IDs and exact source positions inside.'}
def condition(cid,title,met,files,scope,next_step,disposition=None):
    return {'condition_id':cid,'condition':title,'met':bool(met),'evidence':[ev(f) for f in files],
        'fulfilled_scope_or_unmet_reason':scope,'next_minimum_verification':next_step,
        'disposition':disposition or ('met_in_stated_scope' if met else 'pending')}

summary=json.loads((P/'evidence/recount.json').read_text())
sources=jl('sources.jsonl');minimum=[s for s in sources if s['counted_minimum']]
prepath=P/'evidence/pre-result-validation.json'
pre=json.loads(prepath.read_text()) if prepath.exists() else None
pre_ok=bool(pre and all(r['exit_code']==0 for r in pre['commands']))
session=json.loads((P/'evidence/session-check.json').read_text())
session_ok=session['exit_code']==0 and session['stdout']['status']=='passed'
verified=False;candidate=None;remote=None
if args.verified_result:
    candidate=json.loads((P/'evidence/result-candidate-verification.json').read_text())
    remote=json.loads((P/'evidence/result-candidate-remote-read.json').read_text())
    assert candidate['checked_commit']==args.verified_result
    assert remote['commit']==args.verified_result and remote['all_requested_files_matched']
    assert all(r['exit_code']==0 for r in candidate['commands'])
    assert candidate['session_check_exit_code']==0
    verified=True

C=[]
add=lambda *a,**kw:C.append(condition(*a,**kw))
add('A01','기존 작업 브랜치/커밋을 보존해 재개',True,['evidence/resume-033-2.json','PROGRESS.md','manifest.json'],
    '8358b5e에서 fast-forward만 수행; 최초 base와 재개 통합 SHA를 구분했다.','최종 원격 ref가 결과 커밋의 후손인지 확인.')
add('A02','지시된 지침·배정·의존 결과를 먼저 읽음',True,['evidence/resume-033-2.json','SCOPE.md'],
    'AGENTS/STATE/DOT_AUTOMATION/RESEARCH_WORKFLOW와 dot-control AF033, 고정 AF010/029 HANDOFF를 확인했다.','의존 SHA를 바꾸는 경우 별도 재검. 현재 변경하지 않음.')
add('A03','소유 경로와 의존 SHA 계약',session_ok,['manifest.json','evidence/session-check.json'],
    '889c5e 작업트리에서 --fetch 통과; outside_paths=[], unmerged_paths=[], errors=[]. 이 검사는 의미적 타당성 인증이 아니다.',
    '고정 결과 SHA에서 동일 --fetch 명령을 다시 실행.')
add('A04','수신 두 원장의 최초 생성 목록과 결정적 선정',True,['frame.csv','recipient/recipient_frame.csv','SCOPE.md','evidence/resume-input-audit.md'],
    '2020–2024 메타데이터3415건; 생성순 첫 적격4+4. 접두부23=선정8+제외15. 2020에서 충족해 연도 이동 없음.','초기판 오류 발견 시 해당 선택 접두부와 후속 순번을 함께 재검.')
add('A05','최초 제출 본문·첫 diff·실패/제외 보존',True,['evidence/opening-archive-checks.jsonl','evidence/archive-recovery.md','inputs.jsonl','frame.csv'],
    '8개 모두 공개 opened event의 head/base와 tree/path/blob를 검증. 사적 최초 집필 초안은 미확인. 복원 실패와 잠정 선택을 지우지 않음.','GitHub 생성 이벤트와 pinned blob이 달라지는 반증을 제시하면 재복원.')
add('A06','전체/부분 설계와 초기 조건 고정',True,['inputs.jsonl','recipient/recipient_targets.jsonl'],
    '전체3(R03/R04/R06), 부분5. 요청·필수/선호/불필요·기존 해결책과 부분목표를 검색 전에 봉인.','R04 권고 강도 결함은 A07과 별도 민감도에서 평가.')
add('A07','모든 원 고정 필수조건의 요구 강도가 원문과 일치',False,['evidence/resume-input-audit.md','evidence/sensitivity-plan.md','judgments/library-notes.md','judgments/transport-notes.md','judgments/statistics-notes.md'],
    'R04-M07의 회고 산출물/과정 설명은 원문에서 권고적이다. 원 입력을 소급 수정하지 않았다. 해당 하위절만 선호로 낮춘18행과 R04제외를 별도 계산해 strict결과 변화0.',
    '새 재현에서는 최초 R04 L123–144/L343–351의 modal 강도를 독립 작성자가 먼저 다시 부호화. 이 원실험의 결함을 삭제하지 말 것.','disclosed_protocol_deviation')
add('A08','제공 분야·발행처·목록·정렬을 수신 본문 전에 봉인',True,['SCOPE.md','evidence/corpus-seal.json','evidence/resume-donor-audit.md','donor/donor_frame.csv'],
    '3분야 고정 발행처/기간/유한 발견 목록/동률 규칙; 수신별 정답을 제공 수집자에게 주지 않음. 목록은 웹 전수가 아님.','외부 원문을 추가하는 연구는 별도 corpus와 봉인 필요.')
add('A09','고유 제공 원문18·분야별6·판/절/해시 고정',len([s for s in minimum if s['minimum_category']=='candidate'])==18,['corpus.jsonl','sources.jsonl','evidence/resume-donor-audit.md'],
    '도서관6/교통6/통계6. 전문/번역/미러/판을 별도 수로 세지 않음. 18본문·원자료 해시와190창 특징량 확인.','현재 URL 재획득 시 고정 SHA를 먼저 확인; 변화하면 새 판으로 분리.')
add('A10','검색본문에서 문서 표제를 전부 제외',False,['evidence/resume-donor-audit.md','evidence/sensitivity-plan.md','sensitivities/T02-title-excluded-receipt.json'],
    'T02 첫1행 표제가 원본문에 남았다. 첫 검색 전에 위반과 제거 민감도를 봉인. 별도16회에서 순위/상위집합 변화0이나 반환창3슬롯 해시가 변함.',
    '다음 사전 연구는 추출 결과를 독립 검사 후 봉인. 원순위는 유지하고 이 대체판을 원실험으로 덮어쓰지 말 것.','disclosed_protocol_deviation')
add('A11','동일 언어·상한·검색 규칙의 S/R16질의 봉인',True,['inputs.jsonl','recipient/queries_sealed.jsonl','evidence/input-seal.json','retrieval.py'],
    '영어·각80원토큰 상한. 동일 tokenizer/stopword/BM25/동률/창 규칙. 원토큰합각560, 유효고유토큰309/348로 실제 예산 차이를 명시.',
    '동일 유효 토큰 수 비교는 별도 사전 계획에서 실행.')
add('A12','질의 작성자의 제공 원문/제목 노출 방지와 누출 기록',True,['recipient/query_author_checks.json','evidence/resume-input-audit.md','SCOPE.md','judgments/critical-review-notes.md'],
    '질의 작성자는 최초 수신만 읽은 별도 문맥; 기록상 제공 노출0. 통합자의 사후 노출과 평가자의 corpus빈도/메타데이터 출력 노출은 별도 기록. 모델 사전학습 무노출은 입증하지 않음.',
    '새 작성자/새 수신의 누출 로그로 독립 인간 또는 모델 재현.')
add('A13','원 입력/질의/검색결과를 후속 열람 전에 원격 봉인',True,['PROGRESS.md','evidence/input-seal.json','evidence/retrieval-execution.json','evidence/observation-seal.json'],
    '입력e139959 → 사전편차35a01fd → 원검색a2ce15d → 후속열람/관측889c5e 순서. 원질의 문자열 수정 없음.','고정 커밋의 입력/순위 해시를 재검.')
add('A14','16원검색·전체288순위·48반환·빈결과 보존',summary['original_searches']==16 and summary['scored_document_rows']==288 and summary['returned_slots']==48,['rankings.csv','returns.jsonl','evidence/retrieval-receipt.json'],
    '0점 문서8행, 빈 검색0/16. 미반환 문서의 최고창은 rankings에만 있고 returns의 상위3으로 소급하지 않음.','retrieval.py --check로 원 특징량에서 replay.')
add('A15','8×18 전수144대응과 조건504의 양측 근거',summary['pair_count']==144 and summary['mandatory_evidence_count']==504,['maps.csv','judgments/library.jsonl','judgments/transport.jsonl','judgments/statistics.jsonl'],
    '고유Cartesian144; 각 행에 입력/상태/출력/역할/예외·접합/새핵심·깨짐·신규성·시점. support는 모든 필수 match와 새핵심 없음.',
    'validate_results.py --require-cache로 ID·조건·위치·해시 조인 재검.')
add('A16','문서 전수 판독과 실제 반환창 인용 완결을 구분',True,['evidence/returned-window-audit.jsonl','maps.csv','RESULT.md'],
    '원48슬롯/37문서창을 정확 char interval로 읽음. 전수 지지1은R05-L06 S10/R12 미반환. 양쪽 top1/top3 엄격0/8.',
    '원창 밖 근거를 포함하려면 별도 복수절 절차로 평가.')
add('A17','필수조건 없는 적합은 미확인/부분으로 낮춤',True,['maps.csv','judgments/critical-review.jsonl','cases.md'],
    '지지1·충돌9·부분50·미확인84. 양측 근거 없는 엄격 support 없음. R05-L03 초안 conflict는 범주 재검 후partial.',
    '단어 부재를 충돌로 바꾸지 말고 누락 핵심의 실제 원문을 확인.')
add('A18','반환하지 않은 후보·근접오답·표현이 다른 대응 검사',True,['RESULT.md','cases.md','maps.csv'],
    'X01 양쪽놓침1/1; 다른7질문은 엄격 적격0이므로 회수 분모 해당없음. register/archival/일반우선순위 등 근접오답 보존.',
    '현재 full-list positive가 삭제되면 조건부 분모도0으로 바꿔야 함.')
add('A19','사전 제외·상위1/3·넓음/엄격·제목/요구강도 민감도',True,['evidence/sensitivity-plan.md','evidence/recount.json','SELF_CHECK.md'],
    'R01/R03/R04/R08 각각제외0/7; 노출제외8유지; R04권고완화18행불변; T02순위불변/창3변화. 넓은 문서 top3 S5/R5와 엄격0을 구분.',
    'X01의 함의를 거부하면support0·partial51·엄격 회수분모0, 원검색0/8은 유지.')
add('A20','현재 전이와 당시 이용 가능성을 분리',True,['corpus.jsonl','maps.csv','evidence/recount.json'],
    '18판중 T04만당시가용1, 후발10, 미상7. 관계8/80/56. 당시가용 stricteligible0이라조건부회수해당없음.',
    '2020년 이전 VPL해당규정판과복합자료접수규칙이역사적주장을바꿀첫자료.')
add('A21','직접 읽은 고유 외부 원문 최소30',len(minimum)>=30,['sources.jsonl','field/field_sources.jsonl','evidence/observation-seal.json'],
    '최소30=수신8+제공18+현장4. 61행에는제외/보조31이있고후속독립7도최소수미산입. duplicate_group30개고유.',
    'sources.counted_minimum와원문동일성그룹으로재계수.')
add('A22','별도 현장4원문·둘 이상 제공 분야',True,['field/field_sources.jsonl','field/resume-field-audit.md','analysis/field-and-followup.md','cases.md'],
    '교통2/통계2, 총3사건. MTA/DCP는같은사건·공유자료이며독립운영실험2회가아님. 후발다른기관봉인지침의인과적용도미확인.',
    'F02 보존feed/DCP집계코드, F04 MYE3전후원본을연결해실행범위를넓힐것.')
add('A23','현장 반증과 잘못 읽은 근거의 정정 이력',True,['field/resume-field-correction.json','field/ons-correction-comparison.json','evidence/source-audit.md','evidence/method-notes.md'],
    'F02 고정PDF의Real Time을채택하고GTFS해석철회. F04 357키/39변경행/78H·I셀,J/O불변;전체모형미재현.',
    'F02 원시feed/집계코드와F04전체워크북모형은필요시별도검사.')
add('A24','후속 승인·구현·직접인용·실제채택을 별도 판정',True,['recipient/outcome-observations.jsonl','recipient/outcome-supplements.jsonl','recipient/outcome-doc-sources.jsonl','evidence/followup-citation-screen.json'],
    '최초PR5병합/3미병합종료, 대체PR과부분구현확인. 도메인18문자열0/913비빈본문+현재PR8. 간접인용/사적지식/실제채택8건미확인.',
    '공개설계결정기록에서제공원문을읽고선택을바꿨다는시점/인용을확인해야채택판정변경.')
add('A25','Q7 세 관점·성공가능/충돌/보류·판독 교란',True,['cases.md','analysis/q7-role-walkthroughs.jsonl','judgments/critical-review.jsonl'],
    'X01/CE01/CE03 각각수신설계자·운영자·반례검토자9행. 한줄/절/옮길단계/깨질조건·원순위/사후설명구분. 용어만/역할뒤집기/절삭제는재검색아닌판독교란.',
    '실제사용자세역할의행동시험은별도승인된연구에서실시;현재인터뷰했다고주장하지않음.')
add('A26','독립 문맥 판독과 작성자 자체 재검을 구분',True,['judgments/library-notes.md','judgments/transport-notes.md','judgments/statistics-notes.md','judgments/critical-review-notes.md','SELF_CHECK.md'],
    '세분야서로다른문맥144판독, 별도5행검토주분류5/5일치. 모두동일모델이고선택한5행이라인간합의율/전체신뢰도추정불가.',
    '새인간판독자는조건강도·객체동일성·새핵심을각각독립평가.')
add('A27','sources/attempts/frame의 발견·열람·확인·실패·중복 구분',True,['sources.jsonl','attempts.jsonl','frame.csv','compile_ledgers.py'],
    '행마다원URL·고정판/해시·확인UTC·읽은위치·관측·한계·산입여부. 실패/대체경로와판/미러를보존. 사건행수는네트워크호출수아님.',
    '새시도는rawledger에append하고compile_ledgers.py로조인;기존판정/해시를덮지않을것.')
add('A28','RESULT의 처음3표·질문별 답·마지막3행',True,['RESULT.md','compose_result.py'],
    '제목직후지정열의표3개. 첫표38(원반환합집합37+전수전용1), 둘째8+합계, 셋째5반례. Q1–Q7/관점/버릴가정/선택지이후마지막약점표정확3행.',
    'validate_results.py --require-report로표순서·열/분모·마지막행검사.')
add('A29','SELF_CHECK Q1–Q7별 근거·틀릴조건·실제반례·미확인',True,['SELF_CHECK.md'],
    '7질문표및계수·중복·분모·노출·수정·남은미확인을기록. 아직수행전인최종게이트는수행한것처럼쓰지않음.',
    '고정결과검증영수증이생기면작성시점상태를추가하고최종HANDOFF에실제SHA/종료코드기록.')
add('A30','현재 결과의 재집계·해시·ID조인 실제 실행',pre_ok,['evidence/pre-result-validation.json','validate_results.py','evidence/validation-review.md'],
    '네검사와작업트리검산의실제종료코드가모두0일때만met. 의미판정전수인간인증으로확대하지않음.' if pre_ok else '사전결과검사영수증미작성;아직완료로표시하지않음.',
    'validate_inputs / retrieval --check / aggregate --check / validate_results --require-report --require-cache를실행.')
add('A31','고정 결과 SHA에서 session check --fetch 및 집계 재실행',verified,['evidence/result-candidate-verification.json','evidence/result-candidate-session-check.json'] if verified else ['evidence/session-check.json'],
    ('고정후보 '+args.verified_result+'에서전체명령과session검사종료0. 수용파일갱신커밋은HANDOFF전다시검사한다.') if verified else '현재작업트리계약검사는통과했으나고정결과커밋검사는아직수행전이다.',
    '최종수용파일커밋에서같은명령을재실행하고evidence/final-verification.json에실제SHA를남김.')
add('A32','고정 RESULT·수용 파일을 원격에서 직접 다시 읽음',verified,['evidence/result-candidate-remote-read.json'] if verified else ['PROGRESS.md'],
    ('고정후보 '+args.verified_result+'의RESULT/SELF_CHECK/acceptance를GitHub연결로재독하고blob/바이트해시일치확인. 수정된수용파일도다시재독예정.') if verified else '결과초안은현재작업트리이며아직고정원격재독전이다.',
    '최종결과커밋의RESULT와acceptance를GitHub에서읽고evidence/remote-result-read.json과HANDOFF에기록.')
add('A33','종료는 양성 건수가 아니라 필요한 관측·검증으로 결정',True,['RESULT.md','SELF_CHECK.md','evidence/recount.json'],
    '8수신/18제공/4현장/16검색/144대응/504조건/Q1–Q7·반례충족. 양성0인검색을바꾸기위한새질의없음. 방법편차2건과채택/자유웹미확인을남김.',
    '미충족데이터분모를발견하면그행부터재개;양성을늘리려는표본교체금지.')
result={'task_id':'AF-RES-033','schema_version':1,
    'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status':'observations_complete_with_disclosed_deviations' if verified else 'result_candidate_awaiting_fixed_commit_verification',
    'verified_result_candidate_commit':args.verified_result,
    'scope':'Current fixed closed-corpus retrieval, source-based transfer reading, bounded followups; no open-web recall or real user adoption claim.',
    'counts':{'minimum_originals':30,'recipient':8,'candidate':18,'field':4,'searches':16,'rankings':288,'returned_slots':48,'pairs':144,'mandatory_evidence':504,**summary['counts']},
    'frozen_sha256':{f:sha256((P/f).read_bytes()).hexdigest() for f in ['inputs.jsonl','corpus.jsonl','rankings.csv','maps.csv','RESULT.md','sources.jsonl']},
    'conditions':C,'met_count':sum(x['met'] for x in C),'condition_count':len(C),
    'disclosed_protocol_deviations':[x['condition_id'] for x in C if x['disposition']=='disclosed_protocol_deviation'],
    'pending_conditions':[x['condition_id'] for x in C if not x['met'] and x['disposition']=='pending'],
    'unestablished_claims':['Actual designer prior unawareness','Actual adoption caused by retrieved donor material','Open-web discovery or recall','Historical availability of L06 fixed clauses in January 2020','Full recipient implementation and field execution of every invariant'],
    'final_delivery_rule':'After the updated acceptance is committed, reread that fixed RESULT and acceptance and execute the session check again; write HANDOFF only after those observations. Final receipts live with HANDOFF, avoiding self-referential commit claims.'}
(P/'evidence/acceptance-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'conditions':len(C),'met':result['met_count'],'deviations':result['disclosed_protocol_deviations'],'pending':result['pending_conditions']},ensure_ascii=False))
