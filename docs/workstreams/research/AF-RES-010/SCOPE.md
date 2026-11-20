# AF-RES-010 — 사전 고정 범위와 재탐색 절차

- 작업: AF-RES-010#1. 작성일: 2026-11-20 (KST/UTC).
- 저장소: laadkke-arch/agentflow-open. 작업 브랜치: work/research-af-res-010.
- source_commit: `1eca580bf9ddc153f7c9691e30bd727eb7d0ce06`. 시작 시 원격 foundation 최신 SHA였고, 작업 브랜치 부재를 확인한 뒤 이 SHA에서 만들었다. dot-control의 null source_commit은 수정하지 않는다.
- owned_path: `docs/workstreams/research/AF-RES-010/`. 이 경로 밖 기존 파일은 쓰지 않는다.
- 고정 의존: AF-RES-002 `62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1`; AF-RES-004 `2b798c7d2b7355b649691c18de196104ceabb0f0`.
- 두 의존의 HANDOFF, 002의 PROTOCOL §2/3·RESEARCH §3/5·METHODS·evidence/*의 queries, 004의 PROTOCOL·RESEARCH §5·EXPECTED R11/R12/R17을 직접 읽었다.
- 시작 규칙: foundation AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF, START_HERE 및 cloud workflow를 읽었다. 미배정 문구는 과거 설명이며 이번 명시 배정이 우선한다.

## 1. 질문과 판정 대상

다른 분야의 원리를 소프트웨어의 **선택한 부분과 필수 조건**에 연결하려면 문제·후보를 어떻게 표현해야 하는가? Q1 표현 체계, Q2 실제 시스템, Q3 실증과 역효과, Q4 원저자가 밝힌 실제 소프트웨어 전이, Q5 재탐색, Q6 표현별 관측 차이, Q7 판정에 필요한 설명, Q8 비용을 각각 답한다. 최종 제품 DB/API/검색 스택이나 제품 채택을 확정하지 않는다.

후보 판정은 AF-RES-004의 **문제 × 후보 × 제안한 사용 방식 × 명시된 설정 × 제공 근거** 단위를 유지한다. 같은 원리를 좁은 참고로 쓸 때와 전체 해결책으로 쓸 때는 별도 판정이다. 소프트웨어 기존 기법의 새 이름을 원거리 발견으로 세지 않는다.

## 2. 고정 P1 원문과 조건 — 변경 없이 복사

출처: AF-RES-002 PROTOCOL §2, `62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1`.

> 사용자가 폴더의 PDF·이미지 문서를 한꺼번에 넣으면 각 문서를 변환하고 검색 가능한 결과를 저장하는 도구를 만들고 싶다. 손상된 파일 하나 때문에 다른 성공 결과가 사라지면 안 된다. 작업이 중단되어 다시 시작해도 같은 입력의 결과가 중복으로 공개되지 않아야 하며, 실패 항목을 알아보고 다시 처리할 수 있어야 한다. 자체 운영할 수 있어야 한다. 전체 제품을 쓰거나 필요한 처리 부분만 참고하는 두 선택을 열어 둔다.

- 고정 필수 조건: 항목별 실패 격리, 성공 결과 보존, 중단 후 재시도, 같은 입력의 중복 공개 방지, 실패 확인, 자체 운영 가능성.
- 아직 정하지 않음: 프로그래밍 언어, DB, 큐, OCR 정확도 목표, 문서량, 클라우드, 외부 알림, 완전한 exactly-once 실행.
- 금지된 축약: `retry 지원`을 `중복 부작용 없음`으로, `OCR 가능`을 전체 내구성 요구 충족으로 바꾸지 않는다.


## 3. 고정 P2 원문과 조건 — 변경 없이 복사

출처: AF-RES-002 PROTOCOL §3, 같은 SHA.

> 현장 팀이 연결이 끊겨도 공유 기록을 읽고 각자 수정하는 도구를 만들고 싶다. 연결이 돌아왔을 때 수정이 소리 없이 사라지면 안 되고, 같은 기록의 상충하는 수정은 확인하고 해결할 수 있어야 한다. 사용자가 내용을 자기 파일로 내보낼 수 있어야 한다. 자체 운영을 선호하지만 필수로 고정하지 않는다. 완성된 앱을 쓰거나 동기화 부분만 재사용할 수 있다.

- 고정 필수 조건: 오프라인 읽기·쓰기, 복구 후 병합/충돌 보존, 상충 수정 확인·해결, 사용자 데이터 내보내기.
- 아직 정하지 않음: 단일/다중 기기 수, 중앙 서버 유무, 실시간 동시 타이핑, 암호화 방식, 업무 권한·서명·재고 같은 불변식.
- 금지된 축약: `오프라인`을 `동시 수정 안전`으로, `수렴`을 `사용자 의도 보존`으로 바꾸지 않는다.


## 4. 네 표현의 작성 규칙

원문은 언제나 위에 남고, 변환된 질의는 대체 명세가 아니다. 후보가 직접 해결하는 조건과 범위 밖 조건을 따로 적는다. 질의 번역/절 선택 때문에 빠진 조건도 로그에 적는다.

| 표현 | 작성 규칙 | P1 예시 | P2 예시 |
| --- | --- | --- | --- |
| R0 원 자유문 | 원문 전체 한 질의와 **원문 그대로의 연속 문장/구절** 7개. 어휘를 번역·요약·도메인 명사로 교체하지 않는다. 첫 질의만 전체 원문이고 나머지는 정확한 부분 인용임을 표시한다. | `손상된 파일 하나 때문에 다른 성공 결과가 사라지면 안 된다.` | `사용자가 내용을 자기 파일로 내보낼 수 있어야 한다.` |
| R1 기능 기반 | Functional Basis식 동사와 흐름(정보/신호)을 사용한다. input→transform→store/release, separate/identify/control 등의 관계를 적고 불변식을 덧붙인다. 동사만 나열한 넓은 질의도 반례로 1개 보존한다. | `separate failed input preserve successful output retry transform information prevent duplicate release` | `store local information combine divergent changes preserve conflicting information signal conflict export` |
| R2 모순 기반 | 개선할 속성과 악화되는 속성을 함께 적는다. TRIZ의 명칭·번호 자체를 정답으로 쓰지 않고, 모순이 목표 요구와 어떻게 연결되는지 기록한다. | `increase reliability by repeating interrupted work without duplicating released results` | `allow independent disconnected modification without losing conflicting changes during reconciliation` |
| R3 분야 간 어휘 | 같은 관계를 생물·물류/제조·의학·금융·항공 중 최소 2개, 전체로는 최소4개 분야의 말로 옮긴다. 분야별 의미 차이와 빠진 조건을 명시한다. | `manufacturing quarantine defective batch retain released units restart traceability prevent duplicate release` | `medication reconciliation conflicting medication lists preserve sources resolve discrepancies` |

R0에서 8개 모두 같은 전체 문장을 반복하는 것은 독립 질의 증가로 세지 않는다. 원문 전체/정확한 부분 인용의 차이도 통제되지 않았으므로 표현 우위 실험으로 부르지 않는다. 영어를 사용하는 R1/R2/R3와 한국어 R0의 언어 차이는 비교의 교란 요인이다.

## 5. 사전 고정 검색·기록 절차

1. 문제당 R0~R3 각각 서로 다른 문자열 8개, 총 **64개 고유 질의**를 일반 웹 검색에서 실행한다. 최초 질의에는 후보 제품명을 넣지 않는다. 재시도·원문 확인용 이름 질의는 별도 supplemental로 분리한다.
2. 각 문제/표현에서 사전 지정한 첫째와 다섯째 질의를 공개 분야 검색에도 제출한다(추가16회). 우선 AskNature 공개 검색, 실패하면 Google Patents 또는 Semantic Scholar 공개 검색을 사용한다. 검색 시작 전 접속 점검에서 Google Patents xhr=503, Semantic Scholar API=429, 공개 Scholar/Patents 검색 URL의 web 열람 실패를 관측했다. 우회 인증·계정 생성은 하지 않는다. 실패는 성공한 두 번째 시스템으로 세지 않는다.
3. 공개 일반 웹의 system2를 기본으로 쓰되 반환 부족/1차자료 확인에는 system1을 사용하고 engine을 구분한다. 여러 질의가 섞인 반환은 질의별 호출로 재확인하며 각각의 도구 반환 앞 최대3개 제목·URL을 기록한다. 이것은 엔진 전체 순위가 아닌 관측 창이다.
4. 반환 후보 중 원리 후보 또는 반례로 볼 것이 있으면 원문을 열고 확인한 위치·시각·근거 단계·판정을 기록한다. 제목/snippet은 D0이며 원문 자료수에 넣지 않는다. 후보를 열지 못한 경우 pending/excluded이며 오탐으로 단정하지 않는다.
5. **후보 자료는 Q1~4/8의 32개 자료와 별도 집계**한다. 같은 논문 미러, 같은 URL 재열람, 프래그먼트 차이로 수를 늘리지 않는다. 원리 family를 묶고 같은 family의 여러 출처/검색 경로를 유지한다. 원문 전체나 저작권 자료의 대량 복제는 저장하지 않는다.
6. 날짜/시각은 실제 실행 도구의 UTC를 기록한다. 해석·가설에는 H를 붙이고 문헌 확인(D1)에서 실제 목표 적용(D4)으로 승격하지 않는다. 검색 반환 관측은 D3-search이며 후보 구현 실행을 뜻하지 않는다.

필수 SEARCH_LOG 필드: id, problem, representation, query, verbatim_or_transformed, preserved_constraints, lost_or_unqueried_constraints, requested_at_utc, system, results(title/url), opened(source_id/url/outcome), judgments(candidate_id/T/label/count_bucket), execution_status. 보조 필드로 검색 ref, 후속 원문 확인, 동명/중복 정보를 둔다.

## 6. T축 및 후보 집계 — 기존 기준 그대로

T 값: `not_needed / mapped / analogy_only / unknown`. 질문: 출발 분야의 어떤 요소·관계·불변조건을 대상에 옮기는가? 필요한 연결 작업·실패 조건·반증 관측이 있는가? 원리마다 mapping / bridge / excluded / counterexample / minimum_next_check를 쓴다. 별도 전체 판정은 기존 `DIRECT_DOCUMENTED / CONDITIONAL_TRANSFER / SURFACE_OR_CONSTRAINT_MISMATCH / INSUFFICIENT`를 유지한다. 결정적 위반 우선, 자료 부족을 위반으로 취급하지 않는다. T축 자체를 고치지 않고 빠진 규모·시간·사람 가정은 Q7에 별도 메모한다.

| Q6 집계 | 세는 단위와 조건 |
| --- | --- |
| (a) 새 원리 후보 | AF-RES-002의 기존 후보에 없고, 열린 원문에서 구체 관계·연결·실패를 쓸 수 있어 `mapped + CONDITIONAL_TRANSFER`인 고유 원리 family. 목표의 좁은 부분에 한정한 참고이며 채택 성공 수가 아니다. |
| (b) 표면 오탐 | 원문을 열어 핵심 관계가 다름을 확인한 고유 후보 family. 단지 이름이 비슷함/너무 넓은 동사가 맞음. `analogy_only + SURFACE_OR_CONSTRAINT_MISMATCH`. |
| (c) 근접 오답 | 관계는 대응하지만 **제안된 사용 방식**이 원문의 필수 조건을 위반하는 후보 family. T=mapped여도 제약 위반을 덮지 않는다. |
| 별도 | 기존 재발견, 근거 부족, 열람 실패, 단순 제품/부품은 위 세 범주에 억지로 넣지 않는다. |

표현별 집계에서는 같은 family를 한 번만 세고 표현 사이 중복 발견은 각각 나타낼 수 있다. 따라서 표현별 합은 전체 고유 원리 수가 아니다. 표본이 작고 수작업 질의·언어·문장 길이·검토 예산이 달라 비율·정확도·통계적 우위·전체 recall을 일반화하지 않는다. 기존 7 전이와 SOLVENT/focused abstraction은 새 사례·새 근거 수에서 제외한다.

## 7. 자료와 반증의 완료 기준

- Q1~4/8 직접 본문 자료 32개 이상; 동료심사 논문 12개 이상(방법·결과 절까지; 실험 없는 논문은 그 성격 표시), 표현/시스템 1차자료6개 이상, 소프트웨어 전이 원저자 출처8개 이상.
- 최소6개 표현 체계 비교, 각 체계 P1/P2 조건을 실제 부호화. Q3 표본/조건/측정/수치/재현 경계. 개발자 정보탐색 실증1개 이상.
- 먼 유추 유리 조건과 먼 유추 역효과 실험을 모두 찾고, 설계 고착·너무 넓은 추상화·핵심 속성 손실·실패한 비유를 기록한다. 결과가 없으면 없다고 남긴다.
- Q7은 재탐색에서 나온 원거리 후보6개 이상을 실제 결과 옆 설명 형태로 제시한다. 대응표·연결/실패 조건·원분야 입증수준을 포함한다.
- sources.json 공통 필드 및 excluded 목록, 질의/자료별 근거 연결. 각 본문의 한계는 말미에 모은다.

## 8. 분담·커밋·종료

내부 병렬 조사: 표현/시스템/비용, 실증/개발자 탐색, 원저자 전이의 세 갈래. 주 작성자는 P1/P2 재탐색·집계·원문 재확인·통합을 맡는다. 내부 별도 검토를 사람/독립 모델군/새 웹 세션 시험으로 부르지 않는다. 다른 새 작업 AF-RES-009/011/012 결과를 읽거나 기다리지 않는다.

커밋 묶음: (1)이 SCOPE와 작업 manifest → (2)Q1/Q2·REPRESENTATIONS → (3)EVIDENCE → (4)TRANSFER_CASES → (5)P1 로그·판정 → (6)P2 로그·판정 → (7)RETRIAL·COST → (8)SELF_CHECK → (9)HANDOFF 단독. 각 묶음을 곧바로 원격에 저장하고, 최종 HANDOFF의 원격 본문과 로컬 bytes를 대조한다. Git HTTPS push 인증이 없으면 승인된 GitHub tree/commit/ref 도구의 fast-forward로 같은 묶음을 저장한다.

SELF_CHECK의 Q1~Q8 각 행에 답/자료ID·종류수/반증 질의·결과/불확실성을 적는다. 조건 미달 행을 먼저 보강한다. 검색 시스템의 접근 제한 등 해결할 수 없는 차단이 남으면 완료로 포장하지 않고, 마지막 저장 SHA·재개할 첫 행동·입력/명령을 남긴다.
