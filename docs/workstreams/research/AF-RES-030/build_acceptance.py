#!/usr/bin/env python3
"""Build explicit acceptance judgments from observed evidence, retaining gaps."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
v=json.loads((P/'evidence/validation.json').read_text())
s=json.loads((P/'evidence/source-counts.json').read_text())
session=json.loads((P/'evidence/session-check.json').read_text())
out=[]
def add(condition,met,evidence,note):out.append(dict(condition=condition,met=bool(met),evidence=evidence,note=note))
add('최신 배정 통합의 지시·상태·자동화·연구 규칙·AF-RES-030와 의존026 결과를 직접 읽고 manifest 고정',True,['SCOPE.md','manifest.json','evidence/execution-context.json'],'시작172c6bc, 계획478c539 구분. 의존c6eff012. 실제 session start --fetch 수행. 표시모델 지침명과 확인 불가 UI설정을 구분.')
add('작업브랜치와 자기 소유경로만 변경하고 dot-control 미수정',all(x['met'] for x in v['checks'] if x['condition'] in ['all committed and working changes stay inside owned_path','dot-control.json unmodified']),['manifest.json','evidence/validation.json'],'work/research-af-res-030; docs/workstreams/research/AF-RES-030/. 공통 색인은 제안만 인계.')
add('두 비연속 분기·원장·정렬·대체 순서를 결과 열람 전에 고정',True,['SCOPE.md','ANALYSIS_RULES.md','evidence/bundle-commits.json'],'2023Q1/2024Q3. 원장실패 대체와 다음기간 순서 사전고정. 닫힘·답수·인기·수락을 선정키로 쓰지 않음.')
add('A를3원장×2분기×최초4건 총24건으로 재현',s['counts']['A_threads']==24,['frame.csv','initial.jsonl','evidence/validation.json'],'metadata670행은 직접원문670개가 아님. 앞선 제외·삭제/접근시도와 상한뒤 미심사 구분.')
add('A와 별도 B8을 같은 원장의 다른달·상한80에서 첫질문만으로 선정',s['counts']['B_selected_threads']==8 and s['counts']['all_B_eligible_screened_threads']==80,['evidence/b-selection.csv','evidence/t0-summary.json','initial.jsonl'],'M27/X27/D26 interleave80. 첫질문적격14중처음8. XB06늦은첫답도 선정유지, root30분모에서만 제외.')
add('모든 B시도80개에서 최초목적·첫답·후속창 연결',s['counts']['B_nonselected_screening_threads']==72,['streams/matplotlib/screening-followups.jsonl','streams/xarray/screening-followups.jsonl','streams/duckdb/screening-followups.jsonl','chains.jsonl','evidence/validation.json'],'선정B8+비선정72. 제외28/상한뒤21는 다른범주; 양성으로A표본 보충 안 함.')
add('원판 복원/편집·인용·첨부 확인을 시도하고 호환등급과 미래노출을 보존',True,['initial.jsonl','streams/matplotlib/evidence/edit-history-attempts.json','streams/xarray/edit-history-attempts.json','streams/duckdb/evidence/edit-and-attachment-attempts.json'],'O0, Q부분A2/B2. 전체복원 실패를U/Q로 낮췄고 후속값을 최초값으로 넣지 않음. 노출A4/B2.')
add('모든 선정사례의 첫 응답 전 최초본문 전체와 값 공개시점을 복원',False,['initial.jsonl','ADJUDICATIONS.md#사후-판정과-정정','https://github.com/duckdb/duckdb/issues/6943#event-8932902142'],'0/32. 공개 revision/원 알림 미확보. 첫 재개자료 M01 최초 알림/공개편집판; 미복원시 U등급 유지.')
add('목적·시도·판/설정/입력·출력·선호/필수/금지를 원문 절에 연결',True,['initial.jsonl','streams/matplotlib/initial.jsonl','streams/duckdb/initial.jsonl','streams/xarray/initial-field-audit.jsonl'],'모든32건에 원문위치/목적/현재값과 추가 필드매핑 연결. 부재와미확인 구분, 전체원판 보장 아님.')
add('모든 필드별 매핑을 후속내용 및 미래정보에 노출되지 않은 상태로 사전 완성',False,['streams/xarray/initial-field-audit.jsonl','initial.jsonl','ADJUDICATIONS.md'],'xarray13의 보강 필드audit는 봉인cache hash일치하지만 후속판독후 작성. 효과적미래노출6/32. 첫재개: 원판메일로 노출없는새코더 판독; 이번코딩을 맹검으로 바꾸지 않음.')
add('첫 응답 전략·실제 질문 변수·두 예상분기를 작성자 후속 열람 전에 봉인',True,['questions.csv','evidence/t0-seal.json','evidence/bundle-commits.json'],'9de5492에서134canonicalhash봉인. broad candidate-fit M03과 strict정보분모 구분. X02 후발질문 예상은 사전봉인이라 주장하지 않음.')
add('최초즉답 뒤 첫 명확화·새설계·실행요청·역방향질문을 별도 단계 보존',True,['question-audit.csv','streams/*/later-questions.csv','chains.jsonl'],'X02후발 오류, D02/XB13실행요청, X05/X08새설계, X07역방향. X02traceback답후편집시점 미확인.')
add('30일 대화와90일 같은사건 후속을 별도 마감하고 늦은후속/무응답/관측불능 분리',True,['chains.jsonl','wait-audit.csv','streams/xarray/chains.jsonl#XB06,XB08'],'공개창 모두종료. XB06first16개월뒤, XB08실행root153일뒤 별도. 미표시삭제 부재는 미확인.')
add('작성자·변수·판·대상 동일성, 직접/부분/재진술/제3자/새실행/새선호를 분리',True,['chains.jsonl','ADJUDICATIONS.md','evidence/root-rechecks.jsonl'],'A3/B6엄격직접답. X04확장답, M08부분입력, D05지원자추정, XB13다른파일성공, XB03후발선호 구분.')
add('복합질문의 변수를 나누되 왕복 중복 합산하지 않음',True,['question-audit.csv','evidence/denominators.json','evidence/independent-review.json'],'A3변수/3왕복/3사례, B8변수/7왕복/6사례. XB14한episode두발화, XB13한답두변수.')
add('같은지원자의 전후후보·명시연결·첫제안·설명변화를 구별',True,['chains.jsonl','ADJUDICATIONS.md','https://github.com/duckdb/duckdb/issues/5818#issuecomment-1374567686'],'D02 no_prior_proposal 유지. 엄격변경0은 양성부족실패가 아니라 관측결과. 첫제안과설명진전도 별도기록.')
add('기술지지·당사자수락·새실행·공급자새기능을 분리하고 감사/종료로 실행승인하지 않음',True,['chains.jsonl','sources.jsonl','RESULT.md'],'A한정성공4/전체2/실패1; B성공1/실패1. 공급자PR·정적기대시험은 원작성자실행아님.')
add('기술적 적합을 주장하는 행마다 당시 공급자 URL 또는 미확인 이유 연결',True,['sources.jsonl','RESULT.md#판정의-의미와-핵심-결론','PENDING_EXECUTIONS.md'],'공식판의 제한명제만 주장. XD05판차이·M07setter·D07변환계약 등 미확인 유지. PR본문만읽은DP08/09 범위표시.')
add('역사판·원입력·요청자 환경의 제품 실행을 독립 재현',False,['PENDING_EXECUTIONS.md','evidence/execution-environment.json'],'현재Python3.12/NumPy2.3.5/Matplotlib3.10.8이며 xarray/DuckDB없음; 원데이터·macOSGUI없음. 미실시, 연구집계 검사의 실패는 아님. 첫 재개 X04실데이터/metadata/판 및 M07합성검사 명령.')
add('A내 대조를 결과와 무관한 규칙으로 봉인하고 미성립과 목적차이를 보존',True,['comparisons.csv','comparison-results.csv','evidence/t0-seal.json'],'5짝/3미성립. X02후발질문은 사전짝없음. 성공D08로 D05대조를 교체하지 않음.')
add('무응답·확정중복·질문없는실행·같은후보설명변화·도움가능사례를 반증 탐색',True,['RESULT.md#3-실제-반례대조','DESIGN_RULES.md','streams/*/screening-followups.jsonl'],'M07/D05, MB21, M04/D08/MB09, X04, MB07/XB25. 비선정반례를A/B율에산입 안 함.')
add('비용은 실제왕복·대기와 미확인 클릭/읽기/대신할 노동을 분리',True,['wait-audit.csv','evidence/denominators.json','ADJUDICATIONS.md'],'답편집D02/XB13/XB14의 생성~수정범위; XB14재표현89초와최초11.7547h 구분. 순증지연/노동효과미확인.')
for c in s['conditions']:
 add(c['condition'],c['met'],['evidence/source-counts.json',c['evidence']],'canonical original과 counting group을 구별. 동일스레드댓글/판mirror/검색실패로최소수부풀리지 않음.')
add('RESULT의3필수표순서·전표본32행·분자분모·판정주체·미확인을 유지',True,['RESULT.md','evidence/validation.json','evidence/result-review.json'],'표1이제목직후. 표현수정4건 반영 후 결과표 재생성; 수치변화없음.')
add('SELF_CHECK Q1~Q8별 근거·뒤집을조건·실제반증경로·미확인 완성',True,['SELF_CHECK.md','INDEPENDENT_REVIEW.md'],'단순체크박스가 아니라 실제 반례/실패영수증/다음자료 연결.')
add('A전체·실제질문·직접답·같은목적실행·B 및 역할/노출/중복발신자 민감도 구분',True,['evidence/denominators.json','sensitivity.csv','ADJUDICATIONS.md'],'원판O0는해당없음. 미확인양끝은 비증거 시나리오로만 보존. 전수맹검·인과효과 주장 안 함.')
add('실제 로컬 무결성 검사 통과와 실패검사 영수증 보존',v['exit_code']==0,['evidence/validation.json','evidence/validation-first.json'],'최초검사기는B_screen범주와분기접두사해석이틀려95/99, 수정후99/99 exit0. 데이터판정 수정없이검사기교정. 원장은LFcanonical로검산.')
add('실제 workbench.session check --fetch 통과',session['exit_code']==0,['evidence/session-check.json','manifest.json'],'최신통합f1d420d를읽어계약/범위/의존검사 통과. 시작manifest172c6bc는변경하지않음. 최종결과SHA 재검 영수증은별도마지막인계에추가.')
add('모든 주장·한계·미실시의 근거와 첫 재개 자료를 남김',True,['RESULT.md','SELF_CHECK.md','PENDING_EXECUTIONS.md','sources.jsonl','chains.jsonl'],'미확인에 이유·마지막확인위치·다음자료. RESULT끝 약점정확3행; HANDOFF에도 같은형식으로최종작성.')
(P/'evidence/acceptance-evidence.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
summary={'status':'REVIEW_READY_WITH_GAPS','conditions':len(out),'met':sum(x['met'] for x in out),'not_met':sum(not x['met'] for x in out),'gaps':[x['condition'] for x in out if not x['met']], 'validation_input_receipt':'evidence/validation.json','session_input_receipt':'evidence/session-check.json','positive_count_is_not_a_completion_gate':True}
(P/'evidence/acceptance-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
