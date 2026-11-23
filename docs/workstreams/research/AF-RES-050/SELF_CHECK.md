# AF-RES-050 · SELF_CHECK

**현재 판정: partial(부분 충족).** 실질적으로 직접 읽은 고유1차 저작은25건이지만 지정 배당은 원논문8/8, 별도 연구자료2/6, 독립 과제·채점·구현3/6, 방법/추가자료6/4로 충족 슬롯은 **17/24**이다. 배당 적격 저작19건과 읽은 저작25건을 혼동하지 않는다. 고정8군에서 배정×시간×최종품질 공동 원자료로 비교를 추정할 수 있는 군은 **관측0/8**, 소프트웨어 주표본은 **0/6**이다. 이는 효과0 또는 공개자료가 세상에 없다는 결론이 아니다.

검토 기준은 관측·연결·반례 묶음③ `9cb61b4f5952c3b3b8b32f6be27239d06d55f404`와 현재 통합 원장이다. 원장 ID→논리행/물리줄은 `evidence/line-index.json`을 사용했다. 이 문서는 미완료 증거를 지우지 않고 Q별 답·반대 근거·결손·재개 행동을 점검한다. 작성 UTC: `2026-11-23T00:46:22.674151+00:00`.

## 판정 수와 단위

| 점검 | 확인한 수 | 단위·해석 | 근거 |
| --- | --- | --- | --- |
| 표본 유지 | 8/8; 소프트웨어6, 대조2 | 실험·파일·참가자 수로 연구군을 부풀리지 않음 | studies.csv:2–9 |
| 출처 원장 | 143행, 직접열람 표시97행, 실패/미열람46행 | 여러 판·패키지 구성파일·metadata를 포함한 기록 수 | evidence/source-counts.json |
| 고유 실질 1차 저작 | 25건 | 검색/실패/판복제와 같은 패키지 구성파일 제외 | sources.jsonl; evidence/source-counts.json |
| 지정 배당 | 적격19건, 충족17/24 | 8/8·2/6·3/6·6/4; 방법 초과2건은 다른 층 대체 불가 | evidence/source-counts.json |
| 공동 원자료 비교 가능 군 | 관측0/8; 소프트웨어0/6 | 배정×시간×최종품질의 공유키·행을 확보하여 비교 가능한 군. 효과 추정치 아님 | joins.csv; analysis-procedure.md |
| 참가자 원행 탐색/부분 확보 | 탐색4군; 부분 참가자행 확보1군(NCQ) | 최소2군 기준의 보수적 확보 판정1/2 partial. CodeMend IR·Strata 집계·Unakite schema·DataShop metadata는 확보 수에서 제외 | AC-08; J-NA-01/02; BC-J04; J-US-AGG; J-RT-02/03 |
| 원장 구성 | 8 studies·16 joins·26 outcomes | join 계획/구조 감사와 실제 참가자 join 성공을 구별 | evidence/line-index.json |
| 실제 원장 검사 | 356/356 pass, exit0 | 원장 구조·의미 일관성 검사이며 연구 효과 재현은 아님 | evidence/validation-ledgers.json |

## 질문별 자체 점검

각 Q의 판정은 `answered_with_limits`이다. 근거 또는 구체적 미확인이7/7에 붙었다는 뜻이며, 질문의 모든 실증 항목이 해결됐다는 뜻은 아니다.

### Q1

**답과 판정.** 고정8군의 개입·대조·배정 단위를 구분했다. NCQ는 같은 사람이 다른 과제를 baseline-first로 수행하여 순서와 조건이 얽힌다. eXoaDocs와 Blueprint는 독립군이고, CodeMend와 Unakite 연구2는 사람 내 비교에서 과제·기간을 보존해야 한다. Unakite 연구1 및 Strata는 독립군이다. 링크·문서 후보, 허용 browser, 자동 수집·구조화·문맥·도구 기능이 함께 달라지는 비교를 같은 링크의 설명 한 요소 효과로 환원하지 않았다.

**근거 ID·파일행.** NA-001 (`sources.jsonl`:57); NA-002 (`sources.jsonl`:58); BC-01 (`sources.jsonl`:18); BC-02 (`sources.jsonl`:19); US-01 (`sources.jsonl`:123); US-02 (`sources.jsonl`:124); RT-P01 (`sources.jsonl`:111); RT-P02 (`sources.jsonl`:112)

**반대 증거.** 공통 원페이지/기본 표가 있는 Unakite·Strata도 표시 구조와 기능 묶음이 다르다. eXoaDocs 대조 문서에도 수작업 예제가 있고, Blueprint는 실험군 browser 사용이 제한된다. NCQ의 baseline-first 순서와 S05 연구1의 훈련 시점 차이는 링크 설명 단독 귀속에 반대 근거다. 관련 반례: C-04, C-06, C-08, C-12 (`counterexamples.md`).

**남은 결손.** 개인별 실제 배정·period 표; 도구 소개·연습의 실제 시간; 각 시행의 후보/링크/설명 노출량.

**재개 행동.** 연구별 배정표와 조건 지침을 같은 task/version에 연결하고, 노출 로그를 배정과 분리한다. 설명만 달라진 arm이 실제 있는지 확인하기 전 단일 요소 효과를 계산하지 않는다.

### Q2

**답과 판정.** 8군 모두 논문에서 공개자료 또는 구체적 실패·결손 위치까지 추적했다. NCQ 두 CSV는142/156 snippet행과 각20개의 P×T 그룹까지 확인했지만 조건 코드북·시각·최종검사 키가 없다. CodeMend361행은 IR질의이며 사람 lab 기록이 아니다. Strata는 조건×과제 집계6행을 TeX와 연결했지만 외부 workbook은 포함되지 않았다. DataShop 후보77/78의 metadata를 고정 X02 코호트나 참가자 행으로 인정하지 않았다. 최소2군 이상의 참가자 원행 탐색을 수행한 것과 실제 대장 확보는 다르다. 구체적인 탐색4군 중 가명 참가자에 연결된 부분 행동행을 직접 확보한 군은 NCQ1군뿐이므로 최소2군 확보에 대한 보수적 판정은1/2 partial이다. IR표·출판 집계·정적 스키마·카탈로그는 이 확보 수에서 제외한다.

**근거 ID·파일행.** J-NA-01 (`joins.csv`:2); J-NA-02 (`joins.csv`:3); J-NA-04 (`joins.csv`:5); BC-J01 (`joins.csv`:6); BC-J03 (`joins.csv`:8); BC-J04 (`joins.csv`:9); J-US-01 (`joins.csv`:10); J-US-02 (`joins.csv`:11); J-US-03 (`joins.csv`:12); J-US-AGG (`joins.csv`:14); J-RT-01 (`joins.csv`:15); J-RT-02 (`joins.csv`:16); J-RT-03 (`joins.csv`:17); US-11 (`sources.jsonl`:140)

**반대 증거.** 같은 P×T가 반복되는 것은 정상1:N snippet 관계일 수 있다. 파일명에 evaluation 또는 user-study가 있거나 웹 화면에 Students/Transactions가 표시된다는 사실만으로 배정×시간×채점 대장을 확보했다고 할 수 없다. Strata6/6은 발표용 평균 계보의 join이다. 관련 반례: C-03, C-07, C-09 (`counterexamples.md`).

**남은 결손.** 획득하지 못한 표의 실제 행수·고유키·null·unmatched; NCQ T값과 조건/문제/period의 코드북; Strata CSCW 2020 Participants Tracking.xlsx의 공개 비식별판; X02 데이터셋↔코호트↔사후검사 ID 연결.

**재개 행동.** 첫 행동은 NCQ codebook 및 배정·시각·최종검사 export의 공개판을 확인하는 것이다. 이어 Strata의 정확한 workbook명과 DataShop 코호트 crosswalk를 확인한다. 원행이 없는 join의 수를0으로 대치하지 않는다.

### Q3

**답과 판정.** 선택·첫 붙여넣기·부분과제·문서 전환 추정·설명 문턱·전체 경과시간을 별도 종점으로 남겼다. NCQ 선택과 총시간, Blueprint first paste와 completion, CodeMend subtask는 서로 대체하지 않는다. eXoaDocs의 다음 관련 문서30초 초과 체류로 추정한 누적시간은 제출 시각이 아니다. Unakite 연구1의 interaction/total 분율과 연구2의 세 번째 정당한 설명, Strata의 적합성 설명 종료도 구별했다.

**근거 ID·파일행.** O-NA-01 (`outcomes.csv`:2); O-NA-02 (`outcomes.csv`:3); O-NA-04 (`outcomes.csv`:5); O-NA-05 (`outcomes.csv`:6); BC-O01 (`outcomes.csv`:12); BC-O02 (`outcomes.csv`:13); BC-O05 (`outcomes.csv`:17); O-US-01 (`outcomes.csv`:20); O-US-02 (`outcomes.csv`:21); O-US-03 (`outcomes.csv`:22); O-RT-01 (`outcomes.csv`:25); O-RT-02 (`outcomes.csv`:26); RT-M01 (`sources.jsonl`:114)

**반대 증거.** NCQ 선택 중앙값380→57초와 총849→847초는 공존한다. 웹 체류·이벤트 간격·DataShop duration 및 Unakite focus/타이머 함수는 활동 노동의 증명이 아니다. Chan2011의30분은 고정 프로토콜이며 관측된 가변 완료시간이 아니다. 관련 반례: C-01, C-07, C-08, C-10 (`counterexamples.md`).

**남은 결손.** 정확한 원점·중단·대기·idle 처리와 시간 단위 코드북; 교육·작성자·검증·추적 구간의 개인 시간; 계획시간과 실제 강제 상한의 구별에 필요한 이벤트.

**재개 행동.** 원 이벤트의 start/selection/submit/timeout/wait를 같은 시행키로 연결하고 각 종점을 먼저 고정한다. 활성/idle 판정 규칙이 실제 계측되어 있을 때만 활동시간을 산출한다.

### Q4

**답과 판정.** 완료·기능 충족·이유 유효성·순위·독창성·사후 정답을 원 척도별로 분리했다. eXoaDocs 전체40분 내 전과제 통과3/12와1/12는 저자 집계이며 시간표 포함자와 연결되지 않는다. Blueprint 완료자9/8과 배정자10/10, CodeMend 예정60기회와 실제 도달/시도, Strata 종료 선언과 이유별 정오는 별개다. 유의하지 않은 점수 차이를 동등 품질로 선언하지 않았다.

**근거 ID·파일행.** O-NA-07 (`outcomes.csv`:8); O-NA-08 (`outcomes.csv`:9); BC-O02 (`outcomes.csv`:13); BC-O03 (`outcomes.csv`:14); BC-O04A (`outcomes.csv`:15); BC-O04B (`outcomes.csv`:16); BC-O06 (`outcomes.csv`:18); O-US-02 (`outcomes.csv`:21); O-US-03 (`outcomes.csv`:22); O-US-05 (`outcomes.csv`:24); O-RT-01 (`outcomes.csv`:25); O-RT-02 (`outcomes.csv`:26); RT-M03 (`sources.jsonl`:116)

**반대 증거.** eXoaDocs Task3 통과 수는 전체 통과 수와 방향이 다르다. Blueprint의 first paste 뒤 미완료3명, Strata의 생략된 무효 이유, Chan의1321→1066 개념 필터는 실패나 제외를 완료/품질과 혼동할 수 없게 한다. Strata precision 표/그림 및 recall 관계 불일치도 해결하지 못했다. 관련 반례: C-04, C-05, C-06, C-07, C-09, C-10, C-11 (`counterexamples.md`).

**남은 결손.** 제출물·검사 코드·gold 목록과 이유별 점수의 공유키; wrong/no-submit/timeout/unreached 구분; 제외·누락의 원 배정 분모; 동등성 허용 차이와 해당 CI.

**재개 행동.** 배정표에 제출·검사표를 left join하고 분모와 탈락 이유를 보존한다. 기존 aggregate 통과 수를 시간표의 n으로 대입하지 않으며, Strata는 원 workbook 공식·gold 분모로 불일치를 확인한다.

### Q5

**답과 판정.** 새로 실행한 계산은 공개 파일의 구조·기수·flag 기술통계와 집계 계보 감사다. NCQ snippet행, CodeMend IR행, Blueprint 그래프 위치, Strata 평균6행을 참가자 효과의 공통 분모로 합치지 않았다. 고정8군에서 배정×시간×최종품질 공동 원자료로 비교를 추정할 수 있는 군은 관측0/8, 소프트웨어 주표본은0/6이다. 이는 효과가0이라는 추정이 아니며 새 참가자 효과·paired CI는 산출하지 않았다.

**근거 ID·파일행.** J-NA-01 (`joins.csv`:2); J-NA-02 (`joins.csv`:3); BC-J02 (`joins.csv`:7); BC-J04 (`joins.csv`:9); J-US-AGG (`joins.csv`:14); O-NA-SNIPPET1 (`outcomes.csv`:10); O-NA-SNIPPET2 (`outcomes.csv`:11); O-US-04 (`outcomes.csv`:23); J-RT-02 (`joins.csv`:16); RT-M02 (`sources.jsonl`:115); RT-M05 (`sources.jsonl`:76)

**반대 증거.** 성공자 평균, 집단 통과 수, marginal median과 SD만으로 동일 품질 시간의 공동분포나 짝의 공분산을 복원할 수 없다. 교차설계라도 다른 과제·period를 버리면 비교가 바뀌며, NCQ 순서 교란은 원행이 생겨도 자동 해소되지 않는다. 관련 반례: C-01, C-02, C-06, C-07, C-08 (`counterexamples.md`).

**남은 결손.** 독립군의 군별 n/분산과 반복과제 cluster; 교차설계의 실제 사람·과제·기간 배정표 및 공분산; 전체 배정 분모의 시간·정답 공동 관측.

**재개 행동.** analysis-procedure.md의 배정→이벤트 요약→제출/채점 left join 순서를 실행한다. 실제 입력의 기수·누락을 기록한 뒤 동일 종점 안에서만 독립군 또는 교차 비교를 산출한다.

### Q6

**답과 판정.** 여덟 군 모두에 반대 근거 또는 구체적인 미확인 조건을 연결했다. NCQ Used/Runs 불일치와 Blueprint 붙여넣기 후 미완료는 실제 공개 자료의 경계 사례이고, eXoaDocs Task3은 집계 품질 방향이 다르다. Unakite 수집/저장/표 삽입은 서로 다른 사건이며, 소비자 시간 이득에 작성·교육 비용을 더한 실제 역전은 미확인이다. Strata 표/그림 불일치는 임의 수정하지 않았다.

**근거 ID·파일행.** O-NA-SNIPPET1 (`outcomes.csv`:10); O-NA-SNIPPET2 (`outcomes.csv`:11); O-NA-08 (`outcomes.csv`:9); BC-J02 (`joins.csv`:7); BC-O06 (`outcomes.csv`:18); O-US-01 (`outcomes.csv`:20); O-US-05 (`outcomes.csv`:24); US-12 (`sources.jsonl`:141); O-RT-01 (`outcomes.csv`:25); RT-A01 (`sources.jsonl`:113)

**반대 증거.** 개인별로 더 오래 걸렸으나 정답인 시행, 설명을 실제 읽고 거부한 시행, 실패자를 포함했을 때 시간 이득이 역전되는 빈도는 미확인이다. flags나 event 이름은 이해·최종 정답을 뜻하지 않는다. 초보/숙련별 새 효과도 행 연결 없이 계산하지 않았다. 관련 반례: C-01, C-02, C-03, C-04, C-05, C-06, C-07, C-08, C-09, C-10, C-11, C-12 (`counterexamples.md`).

**남은 결손.** exposure→save/paste/adopt→test의 실제 시행키; 실패자 포함/성공자만, 부분/전체, 숙련도, 교육 포함/제외를 나눌 원행; 동일 후보/링크와 기능 변화의 분리.

**재개 행동.** 가장 먼저 NCQ 반례의 P/T를 조건·최종검사와 연결하고, Blueprint first paste/미완료의 정확한 시간·품질 파일을 확인한다. 나머지는 각 counterexamples.md 행의 최소 입력으로 재개한다.

### Q7

**답과 판정.** 분야 대조2군은 소프트웨어 분모에서 제외했다. Chan2011은 고정30분 아이디어 과제의 독창성·품질·양을 다루며 완성품의 재작업 시간과 다르다. Schwonke2009의 시간은 학습 단계이고 개념/절차 전이 점수는 별도다. E1의 비유의 점수 차이와 훈련이 달라진 E2, 저자 프로젝트의 다른 후속 코호트를 합쳐 품질 동등성·지연 전이를 선언하지 않았다. Unakite의 일주일 뒤 채택 질적 사례도 통제된 재작업 절감은 아니다.

**근거 ID·파일행.** RT-P01 (`sources.jsonl`:111); RT-P02 (`sources.jsonl`:112); RT-A01 (`sources.jsonl`:113); RT-M04 (`sources.jsonl`:117); J-RT-01 (`joins.csv`:15); J-RT-02 (`joins.csv`:16); J-RT-03 (`joins.csv`:17); O-RT-01 (`outcomes.csv`:25); O-RT-02 (`outcomes.csv`:26); O-RT-03 (`outcomes.csv`:27); US-01 (`sources.jsonl`:123)

**반대 증거.** 설계 유추의 novelty 이득과 quantity 비용, worked-example의 코호트별 차이는 ‘빠른 선택→정확한 완료→나중 재작업 절감’의 단계가 자동 연결되지 않음을 보여준다. 추적 파일을 찾지 못한 것을 추적기간0이나 수정0으로 쓰지 않는다. 관련 반례: C-10, C-11, C-12 (`counterexamples.md`).

**남은 결손.** 설계자: 원 후보·채택·구현·검증·재수정의 동일 산출물 ID; 참가자: 교육·열람·중단·대기의 실제 노동 구간; 채점자: 독립 루브릭·원점수·제외·미완료 분모; 같은 코호트의 지연검사 및 관찰 종료일.

**재개 행동.** 자료를 빨리 골랐다는 사건, 제한시간 내 명세를 충족한 제출, 후속 revision을 각각 기록한 뒤 같은 산출물/사람/과제로 연결한다. 지연 추적이 없으면 제품 재작업 절감은 계속 미확인이다.

## 실제 행·분모를 혼동하지 않았는가

| 자료 | 직접 확인한 범위 | 연결하면 안 되는 대상 | 검사 위치 |
| --- | --- | --- | --- |
| NCQ codesnippets1/2 | 142/156행, 각20 P×T 그룹, exact full-row 중복0 | P×T 반복은 정상1:N일 수 있고 두 파일의 같은 P를 같은 사람으로 연결하지 않음. T는 코드북 없이 조건명 아님 | J-NA-01/02; streams/ncq-exoa/ncq-row-audit.json |
| CodeMend eval-gt-2.csv | 361행·고유360·정확한 중복1쌍 | IR query를 lab 참가자·과제시간·채점행으로 쓰지 않음 | BC-J04; streams/blueprint-codemend/artifact-inspection.json |
| Blueprint Figure4 | 사람별 그래프 위치20개, first paste 후 미완료3명 | 그림 정렬순서를 다른 품질 그림의 사람키로 연결하지 않음. digitized0은 시간0 아님 | BC-J02; BC-16/17; figure-observations.json |
| Strata chart XML↔TeX | 조건×과제 평균6/6, 중복/결측/미연결0 | 참가자60시행의 원행·공분산·실패 분모로 대체하지 않음 | J-US-AGG; aggregate-join-audit.json |
| Unakite 구현·DataShop 후보 | 공개 static schema 또는 metadata | 코드 정의나 후보 ID만으로 실제 연구판·이벤트·행 공개를 주장하지 않음 | US-12; J-RT-02/03 |

## 자료 부족과 다음 첫 행동

AC-08은 독립 검토에 따라 탐색 실행4/2의 pass를 자료 확보까지 충족한 것으로 읽을 위험을 정정했다. 탐색 실행은 별도 지표로 보존하고, 실제 부분 참가자행 확보는 NCQ1군으로 한정하여1/2 partial로 기록한다. 두 NCQ CSV를 두 연구군으로 세지 않으며 공동 원자료 추정 가능 군0/8은 바뀌지 않는다.

지정 배당 중 저자 별도 연구자료는4건, 독립 과제·채점·구현은3건 부족하다. 실패URL, 같은 논문 저자판/학회판/TeX, 같은 저장소의 여러 CSV를 나눠 채우지 않았다. 별도 보강은 사전 두 검색 질의의 반환기록34건 안에서 확인된 적격/선택0군이다. 이34는 고유 저작34가 아니며 metadata만으로 미해결인 항목도 있다. 연구군을 다른 공개성 좋은 연구로 대체하지 않았다.

다음 첫 행동은 **NCQ의 공개 코드북·배정/시각/최종검사 export를 확인하여 `(cohort,P,T)`를 실제 조건·문제·period에 대응**시키는 것이다. 이어 Strata 외부 workbook `CSCW 2020 Participants Tracking.xlsx`의 공개 비식별판과 이유별 gold/validity 키, X02의 DataShop 코호트↔사후검사 crosswalk가 필요하다. 확보 전에는 참가자 효과·paired CI·활동노동·추적 재작업을 산출하지 않는다. 실행 입력과 자연키 계약은 `analysis-procedure.md`, 군별 최소 파일은 `joins.csv`에 있다.

## 실행·검사와 아직 남은 종료 게이트

공개 파일 감사4개 모드(NCQ, CodeMend, Strata, Unakite)와 통합 원장 생성/검사는 실제 실행 기록이 있다. 실행 명령·입력판·출력은 `analysis-procedure.md`와 `evidence/validation-ledgers.json` 및 각 stream 실행 영수증에 있다. 참가자 코드·원저자 서비스·채점기·새 사람 실험을 실행한 것으로 서술하지 않았다.

| 게이트 | 현재 상태 | 다음 실행/입력 |
| --- | --- | --- |
| 최종 문서 검사 | pass;364검사·exit0 | `python -B docs/workstreams/research/AF-RES-050/verify_ledgers.py --documents`; evidence/validation-documents.json에 실제 출력/종료코드 기록 |
| 고정 결과 원격 재열람 | pending | 고정 결과 SHA의 RESULT 표1·표2와 evidence/acceptance-evidence.json을 각각 원격으로 읽고 일치 확인 |
| session check | pending | `python -B -m workbench.session check docs/workstreams/research/AF-RES-050/manifest.json --fetch`; stdout/stderr·exit code 보존 |
| HANDOFF 마지막 단독 커밋 | pending | 앞 검사가 끝난 뒤 결과 SHA·표 위치·자료수·실행/미실행·부분 요건·다음 행동을 기록하고 단독 커밋 |

현재 pending은 성공으로 선기록하지 않았다. root가 실제 수행한 결과로 이 게이트와 수용 원장을 갱신해야 한다. 이후 원격 확인이 성공해도 자료 배당 미달과 공동 원자료 결손은 남으므로 최종 연구 판정은 partial을 유지한다.
