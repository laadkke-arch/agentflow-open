# AF-RES-057 사전 범위와 판정 규칙

작성 UTC: 2026-11-23T03:17:37.426759+00:00. 이 파일은 모집 본문·선정 시험 assertion 열람 전에 고정한다. 실제 수행자는 ChatGPT 클라우드 세션 / 지시상 GPT-6 Astra Pro와 같은 모델의 보조 조사자다. web-pro 배정은 UI에서 독립 검증하지 않았다.

## 계약과 인수

시작: 3f4d43b19cd76d56983e6f500eebe7010eb3fa51. 계획판: 8036b862a0f921196dca57e8532df606bf6f1de6. 의존 인계: AF-RES-053@94231403b7ce6debd1ee7bb1a34e86e3956c7920. 결과/예측/관측/계수는 87a375d72c269f921589e98b27265e344a70000d. 사용자 지정 규칙·제품 브리프·CLOUD_WORKFLOW·협업 안내를 읽었다. 053의 I/D 동일 예측 5/5와 실제 동일판 공개 출력 0/20 논리셀, 창밖 노출 경계를 인수한다. 이전 도표·자막·지도 라벨 조사자료를 새 표본으로 사용하지 않는다.

허용 경로: docs/workstreams/research/AF-RES-057/ 뿐이다. dot-control.json은 읽기 전용. root가 커밋/원격 업로드를 맡고 보조자는 자기 streams 하위에만 쓴다. 동일 checkout의 다른 작업자를 독립 사람 검토자로 부르지 않는다.

## ① 모집·판·목록·차폐를 결과보다 먼저 고정

- 자연층: yjs/yjs와 ProseMirror/prosemirror. UTC [2019-01-01T00:00:00Z, 2026-01-01T00:00:00Z). is:issue로 PR 제외, open/closed 모두. 제목 대소문자 무시 substring undo 또는 redo 또는 history. 각 단어 질의를 created asc로 각각 취득하고 합집합을 created_at,number 오름차순 정렬한 첫 30개. 결과 부족은 빈 분모로 남기고 기간/저장소를 바꾸지 않는다.
- 현재 API에서 회복 가능한 최초 본문을 읽는다. 최초 작성본의 revision 복원이 불가능하면 현재 복원 본문과 edited/update 노출을 표시한다. 목표, 둘 이상의 편집 주체 또는 사건 경계, 보존 대상이 본문에 함께 있는 첫 2개를 채운다. 단순 API 질문/추상 undo 불만/두 조작 모두의 답을 이미 노출한 본문은 이유를 기록한다. 원요구의 정상 대조가 없으면 연구자 변형임을 표시한다.
- 자연판: 본문의 명시 버전 우선. 없으면 이슈 created_at보다 늦지 않은 마지막 정식 tag를 사건 당시 공개 기준판으로 쓴다. 실제 작성자 설치판은 미확인. 진단판: UTC 2025-12-31 말 이전 마지막 정식 tag(semver prerelease 제외). tag 시각은 release published_at, 없으면 연결 commit 시각을 보조하여 한계를 표시. 모집 본문 전에 실제 선택 tag/SHA와 시험 경로 목록을 각 stream의 metadata 파일로 고정한다.
- Yjs 진단 파일 후보는 tests/undo-redo.tests.js, ProseMirror history 후보는 test/test-history.ts, test/test-history.js. 지정 tag의 tree에서 존재하는 경로를 사전 목록으로 확정하고 사전 후보가 모두 없으면 test 또는 tests 아래 history/undo 이름을 경로순으로 열거한 구조적 대체를 본문 열람 전에 기록한다.
- 진단 시험 선택: 경로순/선언순으로 첫 시험군 중 undo/redo를 실제 호출하고, 식별 가능한 2회 이상 편집 사건과 문서 상태 assertion을 가진 군. actor 구분 또는 연속 사건 구분이 가능해야 한다. 결과 내용으로 선택하지 않는다. 다중 단계 시험군은 가장 이른 적격 접두사(첫 undo와 첫 redo까지)를 기본 입력으로 한다. 추가 뒤 순서는 반례로 분리한다.
- 차폐: raw 시험 파일은 .cache 아래 자동 취득 후 사람이 직접 출력하지 않는다. assertion 호출(t.compare*, t.assert*, ist, eq, deepEqual, strictEqual, assert*, expect와 연결된 matcher) 전체와 expected/snapshot 변수·결과 설명 주석을 문장 단위로 제거한 입력 창을 기계적으로 만든다. 제거 위치/원문 해시를 기록하고 assertion RHS/스냅샷 파일은 ② 원격 커밋 이후에만 연다. multiline은 괄호 균형으로 제거한다. 완전 차폐가 불확실하거나 제목·이슈 본문에 답이 보이면 공개 독해 진단으로 표시하고 신규 적중에서 제외한다. 프로그래밍적으로 raw를 읽은 것과 모델에게 표시된 내용은 분리 기록한다.

## ② 조작·카드·예측

자리: YN1, YN2, YT1, PN1, PN2, PT1. 각 보기 A(공통 API), E(A+같은 분야 예제), D(A+타 분야 원전) 18행. 조작은 opA/opB로 구별하여 보기 A와 혼동하지 않는다. 각 op는 제품판에서 실제 API 호출 가능한 한 설정/범위 차이로 만들고, 불가능한 개념 전체 롤백은 실행 가능 미확인으로 남긴다. 초기 상태, 작성자, 원점, 시각/그룹 경계, 삽입/삭제/원격 전달, undo/redo 순서를 입력으로 고정한다. 원래 요구와 연구자 정상·역순·단독 연속 변형을 분리한다.

- 예측 필드: A만/B만/둘 다/둘 다 실패/판별 불가; opA와 opB 후의 정확 텍스트 또는 식별 가능한 보존 속성; 다른 주체 편집, 그룹, redo 후 상태; 근거 절; prior exposure; actor/sequence variant.
- E와 D는 각 한 연속 절에서 같은 표시 단어 수, 각 <=160. 공백 단위 토큰을 단어로 세고 코드도 센다. 공통 A는 예산 비교에서 제외한다. 도판 수는 두 창 모두 0. 코드 행 수와 절단 위치는 별도 기록한다. 가능한 범위에서 24단어의 짧은 창을 우선하며 짧은 단어수가 정보밀도나 읽는 시간 동등성을 뜻하지 않는다. 정확 창을 공유 원장에 한 번 기록하고 반복 사용은 window_id로 연결할 수 있다.
- E 선택 순서: 해당 고정판의 저자 공식 문서 중 undo/history API 바로 뒤 최초 사용 예제; 없으면 저자 공식 가이드의 해당 절; 없으면 별개 테스트의 입력과 이미 공개된 설명(선정 진단 assertion 제외). 목표 API의 그룹/원점/상대 편집 보존을 실제 다루는 첫 적격 절. 검색어, 실패, 첫 선택 근거를 기록한다.
- D 배정 고정: YN1=지도, YN2=회계, YT1=회계; PN1=지도, PN2=회계, PT1=지도. 후보순: 지도 OpenStreetMap Wiki revert/changeset 가이드 → 공식 OSM community/DWG의 실제 revert 기록; 회계 GnuCash manual reverse transaction/void transaction → 공식 예제 원장 또는 bug 보고. 검색어는 [site:wiki.openstreetmap.org revert subsequent edits], [site:openstreetmap.org changeset revert later edits], [site:gnucash.org reverse transaction void transaction], [site:wiki.gnucash.org reversing transaction]. 후보군 내 원기록/후속 변경/정정 이후 상태를 말하는 첫 적격 절을 사용한다. 새 검색은 이 규칙 안 자료 부족을 메우는 탐색으로 기록하고 예측 차이를 보고 donor를 교체하지 않는다.
- 한 모델이 공통 문서와 여러 창을 볼 수 있으므로 무작위 실험/독립 사람 판정/창만의 인과효과를 주장하지 않는다. 카드별 근거와 창밖 지식을 따로 적는다. E와 D가 같은 결론이면 그대로 보존한다.
- ② 원격 SHA가 확인될 때까지 issue 댓글, 연결 수정 diff, 선정 시험 assertion, CI 출력 및 제품 재생 실행을 열지 않는다. source body에 이미 있는 실패 결과는 노출로 기록한다. 예측을 변경할 수 있는 마지막 시점은 봉인 직전이며 이후에는 사후 감도만 허용한다.

## ③ 관측과 근거 등급

원래 assertion/fixture → 관련 패치 → 동일판/시험 실행 CI → 요청자 실행 순으로 읽는다. test 선언, CI 성공, 저자 실행, 연구자 재생을 서로 다른 evidence_kind로 둔다. 입력/판/actor/op/output 중 하나라도 다르면 exact-match 신규 적중 미확인. 자연 원요구와 합성 변형, 진단을 합산하지 않는다. 빈 자리에는 3보기 모두 미확인과 미실시 사유를 유지한다. text 동등과 identity/undo-stack/redo 순서 동등도 구별한다.

목표 외부 원저작 >=20; 배당 요청4, 제품 API·예제·설계4, 독립 시험/수정 계보6, 지도/회계 직접 사례4(각2), 원연구/실패2. 후보 제외 이슈도 직접 읽은 저작수에 포함할 수 있으나 선정 요청 배당을 대신하지 않는다. 시험 코드/CI/PR이 같은 사건이면 한 work_id. 내부 인수·검색 스니펫·실패·metadata·자가 생성은 최소수에서 제외한다. 자료 수와 6자리 검증수를 별개로 센다.

## ④ 판정·반증·검사

6자리 모두에 E/D 선택과 속성 예측 동일 여부를 센다. 서로 다른 사전 예측의 분모가 0이면 조건부 새 정답률 해당 없음. 미확인 출력은 동률 정답으로 세지 않는다. E보류→D정답, E오답→D정답, D새오답을 분리한다. 보존 목적이 달라지는 반례, actor/원점 혼합, 동일 텍스트·다른 이력 순서를 탐색한다.

RESULT 앞 표 18행+6행, Q1~Q7, 사례별 반환 카드, 마지막 정확히 3행 약점 표를 작성한다. frame/events/cards/predictions/observations/sources의 ID를 대조하고 수용 원장에 실제 분자/분모를 기록한다. 봉인 hash, 원격 readback과 session check 실제 로그를 저장한다. 검사 뒤 HANDOFF 단독 마지막 커밋. 완전충족 여부는 저장 성공과 분리한다.

## 변경·노출 원장

현재 모집/결과 미열람. 추가 변경은 이 절에 UTC, 변경 전후, 이유, 이미 본 결과, 주분석/감도 구분을 추가한다.
