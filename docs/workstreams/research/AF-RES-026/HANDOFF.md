# AF-RES-026 · 부분 설계에서 먼저 물을 조건 — 인계

**상태: REVIEW_READY_WITH_GAPS**

인계 작성 UTC: 2026-11-22T06:12:06.890825+00:00

요청한 공개 원장 조사·봉인·후속 대조·반증·결과 표·검산을 완료했다. 수용 조건18개 중17개가 충족됐고, **S01에서 봉인 전 검색 답 문장에 노출된1건** 때문에 전24건의 완전한 사전 미노출 조건은 `met=false`다. 이를 다른 사례로 교체하거나 사후에 노출이 없었던 것으로 만들지 않았다. 전체24와 엄격 미노출23의 집계를 함께 인계한다. 새 Q 정보에 따른 변화가0이라는 결과 자체는 미충족 조건이 아니다.

최종 검증 보강본의 SELF_CHECK·acceptance-evidence·verification-summary를 아래 고정 SHA에서 GitHub로 다시 읽은 **뒤에** 이 HANDOFF를 작성했다. 인계는 별도 마지막 커밋이다. 공통 진행표·계약·색인·dot-control은 변경하지 않았다.

## 고정 참조와 실행 위치

| 항목 | 고정 값 |
| --- | --- |
| 저장소·브랜치 | laadkke-arch/agentflow-open · `work/research-af-res-026` |
| 소유 경로 | `docs/workstreams/research/AF-RES-026/` |
| **인계할 고정 결과 커밋** | **`25c7345d8673bc763b2fc7d442a35a803621b656`** — 결과·데이터·최종 수용 근거·검사 영수증을 포함 |
| 결과 본문·실제 검사 대상 | `ed14e806a5a7bf4e6195fd12024c482d31768449` — RESULT 본문은 이후 변경 없음; 이후 커밋은 검증 영수증·수용/자체점검 보강 |
| 전체 T0 봉인 | `68fc97fadceb46f9945a71fcc53730e29f6c62bf` — 24건·72문구; 봉인9파일 불변 |
| 표집·판정 사전 규칙 | `cecbfb981b9a7ccfd59f7bc40a23445a19d020fa` |
| 계획 기준 / 배정 통합 기준 | `e2d0917ccd0e0010e14627a2f919265c332cec53` / `b420fb7e1e01f4a366512fa71c0f507051aa6a19` |
| 최종 계약 확인 때 통합 SHA | `21c517691e8d8882f0e66ef262b32fe3ad39b630` — 고정 계약과 같음; 새 연구 입력으로 사용한 것이 아님 |
| 고정 의존 입력 | AF-RES-021@`29049a5f15b6ef7cd7431f59a059598db6f5d857`, AF-RES-022@`df80ec2406042a73c2114e316894173f66309cda` |
| 실행 환경·표시 모델 | ChatGPT Linux cloud workspace `/workspace/scratch/f7aa0910b8d1`, Python3.12.14; 세션 표기 GPT-6 Astra Pro. UI 모델 선택·별도 계정 연결은 미관측 |
| 조사 창 | 2026-11-22 UTC 단일 실행. 배정 확인04:46:58Z; 공통 보강 검사 종료06:06:25.615Z; 인계 작성은 최종 검증 커밋의 원격 확인 뒤. 개별 직접 열람 UTC는 sources/영수증에 있음 |

보고서: [RESULT.md](RESULT.md). 원문별 위치·관측·한계: [sources.json](sources.json). Q별 주장·반증: [SELF_CHECK.md](SELF_CHECK.md). 최종 조건: [acceptance-evidence.json](evidence/acceptance-evidence.json). 모든 묶음 SHA와 이전 행동: [PROGRESS.md](PROGRESS.md), [bundle-commits.json](evidence/bundle-commits.json).

## 검산한 분모와 결과

| 관측 단위 | 수와 의미 |
| --- | --- |
| 모집 원장 | 149행 = root 심사40(선정24/제외16) + 답장 metadata87 + 상한 뒤 미심사22 |
| 주 질문 | SQLite8 + PostgreSQL8 + curl8 =24. 2022–2024를 시작 범위로 정했으나 모두2022년1월에 상한 도달 |
| 최초판 증거 | 공개 보존 전문·artifact/Message-ID·응답 순서 연결24; 추가 교차근거18; 미노출23; 보강과 미노출의 교집합17 |
| 원형 증거의 한계 | PostgreSQL RFC822 Received 확보0/8. P04/P05 첫 답 인용 대조2건은 보강이며 P04는 실질 질문 전문만 일치. 서로 다른 증거 수준을 동일한 암호학적 원본으로 부르지 않음 |
| 봉인 출력 | I즉답/C조건부/Q한문장질문 24×3=72. 각300자 이하, 후보45개·사례최대2. 실제 발송0 |
| 후속·조건 행 | followups137 = 실제 공개 발화114 + 개정4 + 검열 요약11 + 미연결 인접8. judgments294는 같은 후보·판의 T0/T1 및 기술/행동 판정원 |
| 고유 외부 원문 | 61 =24대화 + 당시 제공자 문서/테스트32 + 타 분야5. 날짜 불명 X-S1을 빼도60/타 분야4. sources159행과 고유 원문 수는 다름 |
| 독립성 한계 | 서로 다른 최초 요청24건이 관측 단위. 공개 발신자 표기는19개이며 독립 사람24명·독립 채택24회가 아님. 공급자이기도 한 C06/C07 제외 분모22 |
| T0 사실 충분 | 원래 질문의 선언된 판정 범위에서6/24; P05의 명시적14.1 비교판 음성 구문 답까지 포함하면7/24. 설치 환경의 모든 사실을 확인한 수는 아님 |
| Q 정보 | 이미 T0에 값이 있음8/24. 명확한 작성자의 기존 사실로 새로 채운 값0/24. 같은 변수의 실제 질문→직접 답 하위분모0이므로 비율은 해당 없음. 나머지16은 엄격 값 미확정 |
| Q 민감도 | P03 지시대상·S04 상충 주장·C05 부분 선호를 모두 넓게 인정하면 새 값0–3. 통계적 구간 아님 |
| 제한된 문구의 기술 지지 | I13/24·C14/24. 보류 I11/C9. C 근거부족1(P04). 확인된 기술 오승인0은 근거부족0 또는 전체 정답을 뜻하지 않음 |
| 전체 사용 승인 | I4/C2; 미노출23에서는 I3/C1. S08 C의 NOT NULL 누락과 S03 C의 미확정 분기/참조 확인을 제외. S03의 가능한 A 경로까지 세는 넓은 C3은 별도 정의 민감도 |
| 새 사실에 따른 변화 | 엄격 후보 변화0/24, 변화와 작성자 진전 동반0/24. P03의 local을 실제 원천으로 넓게 읽는 경우에만 변화1 |
| 실제 진전 | S01 새 자가 실행 성공1, C05 결정 수용·기존 workflow1, C06 공급자 신규 개발1. 사용자 채택3으로 합치지 않음. 미노출 외부 사용자 새 실행 성공0/23 |
| 실제 비용 | 주 대화 추가 질문7쌍(기술 입력만6) + 별도 구현1쌍 = 중복 없는8. 구현쌍도30일 안. 주 쌍 대기0.076522–16.222305시간이며 겹치는 구간을 합산하지 않음 |
| 가상 대리 비용 | I/C 문구 발송에 추가 왕복0, Q는 답이 오면 최소1. 문구 링크 I23/C35/Q0. 실제 사용자 클릭·전략별 달력시간·인과 절감은 미확인 |

전체24/원판24/미노출23/직접답0/비공급자22/추가 보강18은 [strategy-summary.csv](strategy-summary.csv)에서 따로 계산한다. 원판 미확인0의 성립/불성립 양극단은 아카이브 식별 기준 아래서 같다. raw 서버 시각 불확실성까지0이라는 뜻은 아니다.

## 설계자에게 넘길 판단

1. **먼저 원문 전체를 다시 읽는다.** C01의 브라우저 요청 주체, S08의 JS 값처럼 이미 적힌 조건을 묻는 것은 새 정보의 편익이 아니다. S03 OFF가 필수인지도 명시되지 않았으며, 최초 변수 요약의 반대 방향 오류는 원본을 보존한 채 표시만 바로잡았다.
2. **작은 판정이 완결되면 즉답과 근거 링크를 준다.** C03의 시간 경계 설명과 P01의 조회 방향은 주변 프로젝트 전체를 알지 않아도 답할 수 있다. 설명의 성립과 작성자 실행 성공은 별개다.
3. **안전하게 설명할 수 있는 갈림은 조건부로 반환한다.** C04의 CR/LF 분기는 두 공식 절, S05의 mutex 계약은 한 공식 문서로 안내할 수 있다. S05의 다중호출 순서·pointer 수명·성능까지 승인하면 범위를 넘는다.
4. **원문에 없고 판정 또는 다음 행동을 바꾸는 한 변수만 질문한다.** 답이 와도 다른 조건이 남는 P02/P06, 입력 경계를 잘못 고른 P04, 후보가 없는 C08을 보류로 유지한다. 공개 기록의 신규 값0은 질문이 쓸모없다는 인과 결론이 아니다.
5. **늦게 나온 요구는 발생 시점부터 따로 기록한다.** P08의 순서/pop나 C06의 이후 설계선택을 숨은 T0 필수조건으로 바꾸지 않는다. 도서관 Mexico는 후보가 유지돼도 검색 숙련도 정보의 가치가 있을 수 있음을, Census는 probe 자체가 해석·회상을 흔들 수 있음을 보여준다. 목적 자체의 신규 생성은 직접 확인하지 못했다.

실제 C05는 질문 없는 조건부 설명 뒤 수용이 있었지만 첫 답에는 기술 문서 링크가 없었고 새 실행 보고도 없다. 따라서 **조건부 링크 하나만으로 실제 새 구현이 해결된 사례는 이24건에서 확인되지 않았다.** 사용자에게 보낼 수 있는 실제 봉인 문구와 그 한계는 [examples.md](examples.md)에 있다.

## 중요한 판독·인용 교정

- P03의 local은 실제 ID 테이블과 상수 UNION 예제 결과집합 중 무엇을 가리키는지 불명이다. 엄격0/넓은1을 함께 남겼다.
- S04의 committed 주장과 COMMIT 없는 재현·실패 로그는 충돌한다. 이것만으로 작성자가 거짓이라고 판단하거나 성공 COMMIT 값을 채우지 않는다.
- P04는 재접속이 가능해도 기존 dump의 데이터·시점을 새 dump로 대체할 수 있다는 뜻이 아니다. 이는 원판 재독으로 발견한 문구의 근거 부족이다.
- S08의 다른 실제 조언 실패를 미전송 I/C의 실패로 세지 않는다. S03/S08 C의 전체 승인 집계 교정은 사용자가 새 사실을 알려준 성과가 아니다.
- SQLite의 짧은 메시지16개 중6개는 실제 제공자 링크가 필요한 주장 전부를 포함하지 않았다. curl C01/C·C02/I/C에는 기록된 근거보다 넓은 문장이 있었다. 세 curl 문구는 원래 보류다. 인용 완결·기술적 지지·전체 사용 승인·실제 행동은 별도 축이며 서로 다른 감사 기준을 한 완결률로 합산하지 않는다.

[adjudication-overrides.json](adjudication-overrides.json), [통합 교차검토](evidence/integration-review.json), [SQLite 인용 감사](streams/sqlite/citation-coverage.json), [curl 명제 감사](streams/curl/citation-coverage.json)를 원 계열 태그와 함께 읽는다. 계열별 T0/T1은 같은 작성자의 자기 점검이다. P03 표적 검토와 사후 집계/인용 검토는 전체24건의 독립 가림 이중 판독이 아니다.

## 실행 검증과 보존한 실패

| 실제 검사 | 대상·결과 | 범위·한계 |
| --- | --- | --- |
| 자체 verify.py --require-report | ed14e806,18 PASS/0 FAIL/1 SKIP, exit0 | 현재 SCOPE 해시만 의도적으로 SKIP; 봉인9파일은 PASS. 자료 수·참조·조건 쌍·전략·표/수용 형식 검산. 원문 진실·인과효과의 인증 아님 |
| 자기 manifest check --fetch | ed14e806, PASS/remote_checked, outside_paths[]/errors[] | 통합21c5176과 고정 계약 동일. 계약/소유권 검사 |
| 공통 검사1차 | 같은 ed14e806, FAILED exit1 | 부분 복제의 과거 객체 누락으로 Git bundle 생성 실패. 실패 로그 보존 |
| 공통 검사2차 | 필터 없는 공개 clone의 같은 ed14e806, PASSED exit0 | unit test55, lab test/demo, export·재사용, bundle 복원 및 공통5명령 통과. 공통 코드 수정 없음 |
| 공통 check-all 세션 부분 | not-executed/no_active_sessions/count0/not_checked | 프로세스 exit0을 원격 세션 검증으로 확대하지 않음. 별도 자기 manifest --fetch가 실제 원격 계약 확인 근거 |

[검증 요약](evidence/verification-summary.json), [자체 영수증](evidence/verification.json), [계약 영수증](evidence/session-check-receipt.json), [공통 두 시도·재현 경로](evidence/required-checks/README.md). 임시 clone/TMPDIR/대형 bundle은 정리했고, 소규모 원본 로그·영수증은 내용과 해시를 보존했다. 이후 검증 보강·인계 문서 커밋을 ed14의 실행에 포함됐다고 주장하지 않는다.

## 고정 결과 커밋을 확인하는 방법

다음은 저장소 root에서 실행한다. 브랜치의 나중 변화와 무관하게 결과 SHA를 직접 읽는다. HANDOFF 자체의 최종 커밋은 해당 경로의 마지막 커밋으로 확인한다.

```bash
git fetch origin work/research-af-res-026
git show 25c7345d8673bc763b2fc7d442a35a803621b656:docs/workstreams/research/AF-RES-026/RESULT.md
git show 25c7345d8673bc763b2fc7d442a35a803621b656:docs/workstreams/research/AF-RES-026/evidence/acceptance-evidence.json
git show 25c7345d8673bc763b2fc7d442a35a803621b656:docs/workstreams/research/AF-RES-026/evidence/verification-summary.json
git diff --exit-code 68fc97fadceb46f9945a71fcc53730e29f6c62bf 25c7345d8673bc763b2fc7d442a35a803621b656 -- docs/workstreams/research/AF-RES-026/initial.jsonl docs/workstreams/research/AF-RES-026/frozen-responses.jsonl docs/workstreams/research/AF-RES-026/frame.csv
git log -1 --format='%H' origin/work/research-af-res-026 -- docs/workstreams/research/AF-RES-026/HANDOFF.md
```

자료를 바꾸지 않는 검산은 `PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-026/verify.py --require-report`다. 원본 영수증을 덮어쓰지 않는다. 공통 검사를 다시 실행하려면 다음 wrapper가 같은 검사 입력 commit의 공개 원격 clone을 소유 경로 안에 만들고 새 시각의 로그를 남긴다.

```bash
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-026/evidence/required-checks/run_cloud_check.py --commit ed14e806a5a7bf4e6195fd12024c482d31768449 --remote-clone
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-026/manifest-cli.json --fetch
```

## 남은 판단·실행 입력과 다음 첫 행동

필수 자료 구조·직접 원문 최소수·분모·보고서·계약 검사는 완료됐다. S01 사전노출은 복구할 수 없고, PG 원형 수신 메일·모호한 작성자 값·실제 가상전략 효과는 공개 자료 범위에서 남는다. 역사판 제공자 테스트는 직접 읽었으나 이 실행에서 해당 제품을 빌드/실행하지 않았다. 연구자의 실행 영수증을 실제 질문자의 재현·사용 보고와 바꾸지 않는다.

다음 첫 행동은 **고정 T0 봉인만 제공받는 별도 판독자가 미노출23건의 변수·제한 주장·사용 승인/보류를 재판독하는 것**이다. P03을 보강하려면 그 뒤 같은 사건의 실제 ID 질의와 foreign server 귀속을 찾는다. 발신자가 같다는 이유만으로 다른 사건의 SQL이나 새 요구를 가져오지 않는다.

| 보강이 필요한 판정 | 반드시 필요한 입력 | 실제 실행/조회할 명령·관측 |
| --- | --- | --- |
| P03 실제 ID 원천의 서버 소속 | 원 작성자의 공개된 실제 ID SELECT, tbl_link 및 ID 관계의 foreign-table 정의, 실제 PostgreSQL 판. 현재 예제 상수 UNION은 대체 입력이 아님 | 같은 읽기 전용 재현 DB에서 `EXPLAIN (VERBOSE, COSTS OFF) <실제 SELECT>;` 및 `SELECT c.oid::regclass, s.srvname FROM pg_foreign_table f JOIN pg_class c ON c.oid=f.ftrelid JOIN pg_foreign_server s ON s.oid=f.ftserver;`. 실제 질의가 공개되지 않으면 실행 불가·미확인 유지 |
| S04 성공 COMMIT과 원앱/재현 동일성 | iOS12.3·SQLite3.37.0의 원래 앱/재현 소스, 동일 데이터·transaction·재시작 시점, FMDB와 직접C API의 관계 | 원 테스트 앱의 동일 연결에서 `sqlite3_libversion()`, `sqlite3_get_autocommit(db)`와 원래 존재하던 COMMIT 호출(예: `sqlite3_exec(db,"COMMIT",...)`)의 반환·`sqlite3_extended_errcode(db)`를 시각과 함께 기록. 새 COMMIT을 추가한 시험은 별도 개입으로 분리. 성공 반환 뒤 행이 durable하다는 주장까지 검증하려면 원본과 같은 종료·저장 조건이 필요. 현재 파일만으로 명령 실행 성공을 만들지 않음 |
| S03 당시 migration의 독립 실행 보강 | SQLite commit `384f5c26f48b92e8bfcb168381d4a8caf3ea59e7`, 원문 SQL·데이터, C compiler/Tcl·make | 해당 고정 소스의 격리 checkout에서 `./configure --disable-shared`, `make testfixture`, `./testfixture test/altertab.test`; 원문 SQL의 view 제거/재생성 전후 schema·data를 대조. 이 테스트 실행은 이번에 하지 않았으며 작성자 채택 증거도 아님 |

## 진행 담당에게 넘길 색인 반영 제안

공통 파일은 직접 수정하지 않았다. 진행 담당은 AF-RES-026의 상태를 `REVIEW_READY_WITH_GAPS`, 결과 커밋을 `25c7345d8673bc763b2fc7d442a35a803621b656`, 결과 경로를 이 디렉터리로 반영할 수 있다. 인계 커밋은 위 `git log`로 구한 HANDOFF 커밋을 사용한다. 요약은 “24건/72문구·61원문; 이미 적힌 Q값8, 엄격 신규값0, 제한응답I13/C14, 전체승인I4/C2; 사전노출1건과 판독/인과 한계 보존”이다. 검토 전 `REVIEW_READY`나 통합 완료로 승격하지 않는다. 이후 통합·추가 조사는 이 인계의 제안이며 이번 실행에서 수행한 것으로 표시하지 않는다.

## 중요한 약점과 각각의 후속 조사 — 영향순

| 중요한 불일치·약점 | 근거 ID·URL | 영향을 받는 결정 | 다음 조사 질문·찾을 자료·최소 확인 |
| --- | --- | --- | --- |
| P03 local 지시대상이 모호해 새 정보에 따른 후보 변화0/1이 갈림 | [P-S03](https://www.postgresql.org/message-id/DB9PR07MB7180EDC1ACD3222532399E1CCB499%40DB9PR07MB7180.eurprd07.prod.outlook.com), [작성자 local](https://www.postgresql.org/message-id/DB9PR07MB718015C40BC021957A7165F5CB4C9%40DB9PR07MB7180.eurprd07.prod.outlook.com), [표적 검토](streams/curl/p03-cross-review.json) | Q값 회수·후보 변경의 엄격0을 넓은1로 바꿀 수 있음. 실제 진전은 여전히 별도 | 실제 ID 질의의 물리 원천은 어느 서버였나? 같은 사건의 공개 SQL FROM 관계·foreign server 정의/EXPLAIN VERBOSE 한 묶음에서 실제 질의임을 확인 |
| S01 사전노출·PG raw 부재와 같은 작성자의 순차 판독 | [S-S01](https://sqlite.org/forum/artifact/d5ac4dc7975d6480c8d946c11d3e92c6a22e2534c95c080eabd23fc27500e0d3), [노출](evidence/T0-review.md), [raw 시도](streams/postgres/initial-raw-attempts.json) | 전24건 미노출 비교 불가; 유일 외부사용자 새 성공은 엄격집합에서 제외. 원판 증거의 동등성 미확인 | 답을 가린 별도 판독자는 같은 T0에서 어떻게 판정하나? 봉인 SHA만 제공한 독립 재판독1회에서 변수·문구범위·승인/보류·원판등급을 대조하고 원본 부재를 그대로 표시 |
| 직접답 분모0·단일월/반복발신자·미전송전략으로 인과효과와 목적생성을 알 수 없음 | [X-L2](https://ils.unc.edu/MSpapers/2957.pdf), [X-S2](https://www2.census.gov/library/working-papers/2025/adrm/cbsm/rsm2025-03.pdf), [여섯 분모](strategy-summary.csv) | 질문을 줄이는 일반 정책·조건부 링크 단독 해결·시간 절감·새 목적 발생을 확정할 수 없음 | 다음 사전고정 원장에서 같은 변수 질문→기존사실 답→동일판 행동이 이어지는가? 응답 결과와 무관하게 정한 다음 월 공개대화1계열에서 실제 계보와 요구 발생시점 표현을 확인 |
