# AF-RES-138 모집 및 표시 정책

계획 기준은 `1d65b0b7aaef85350df8842dfc05a6be69148b38`이다. 최초 원격 조회와 manifest 생성 시 통합 HEAD는 `588e642b99e695e710573b9418b60364d7f3880b`였다. 그 두 통합판의 차이는 중앙 진행표였다. 실제 판의 AGENTS, STATE, DOT_AUTOMATION, START_HERE, RESEARCH_BRIEF, RESEARCH_WORKFLOW 및 AF-RES-138 행을 읽었다. 중앙 행은 RUNNING, 브랜치는 `work/research-af-res-138`, 허용 경로는 이 디렉터리다. [중앙표 blob 5ccb8d657](https://github.com/laadkke-arch/agentflow-open/blob/588e642b99e695e710573b9418b60364d7f3880b/docs/automation/dot-control.json) · [계약 및 입력판](manifest.json)

등록 선행은 AF-RES-134 하나다. 중앙 DONE과 고정 인계의 PARTIAL을 별개로 기록한다. 고정 인계의 SCOPE, replay/README, transitions, alias-audit와 결과판에서 원질문 6/6저자, 활성 별칭 0, B/C 동률, Gate 보류 충돌 1과 단일 프로세스 허용 시 직접 1을 확인했다. 130·134의 미회수 포럼 창은 이번 모집과 실행의 입력에서 제외한다. 과거에 연 첫 본문·URL·계보는 신규 여부 판독에만 쓴다. [등록 인계 a214140](https://github.com/laadkke-arch/agentflow-open/blob/a21414017323dbd7a090b1e7b62f070d4fa1a1ab/docs/workstreams/research/AF-RES-134/HANDOFF.md) · [고정 결과 6a17cf5](https://github.com/laadkke-arch/agentflow-open/blob/6a17cf5265e6f13155407c3785906b048982a12f/docs/workstreams/research/AF-RES-134/RESULT.md) · [전이](https://github.com/laadkke-arch/agentflow-open/blob/a21414017323dbd7a090b1e7b62f070d4fa1a1ab/docs/workstreams/research/AF-RES-134/evidence/transitions.csv) · [별칭](https://github.com/laadkke-arch/agentflow-open/blob/a21414017323dbd7a090b1e7b62f070d4fa1a1ab/docs/workstreams/research/AF-RES-134/evidence/alias-audit.csv)

## Q1–Q2 모집과 판독

GitHub 전체 공개 이슈, 생성 UTC 2019-01-01부터 2025-12-31까지, 상태 무관, 첫 본문 검색이다. 공식 웹 응답은 아래 질의에 `sort:created-asc`와 `type=issues`를 적용한다. 공식 REST 대조는 같은 질의에 `sort=created&order=asc`를 사용한다. 첫 20개와 경계와 같은 생성시각의 이슈가 있으면 그 시간의 동점 묶음 끝까지 확인한 뒤 생성 UTC·저장소 경로(casefold)·이슈 번호 순으로 잘라낸다. 원서버 배열 순서를 함께 보존한다. 각 요청의 URL·페이지·응답 시각·본문 상태·마지막 ID를 남긴다.

| 순환 | 모집층 | 정확한 질의 | 예정 |
| --- | --- | --- | --- |
| P1 | 목적 | `"pytorch" "가중치를" is:issue is:public in:body created:2019-01-01..2025-12-31` | 20 또는 배열 끝 |
| P2 | 목적 | `"pytorch" "복사본을" is:issue is:public in:body created:2019-01-01..2025-12-31` | 20 또는 배열 끝 |
| P3 | 목적 | `"pytorch" "전치를" is:issue is:public in:body created:2019-01-01..2025-12-31` | 20 또는 배열 끝 |
| P4 | 목적 | `"pytorch" "데이터로더를" is:issue is:public in:body created:2019-01-01..2025-12-31` | 20 또는 배열 끝 |
| N1 | 중립 | `"pytorch" "궁금합니다" is:issue is:public in:body created:2019-01-01..2025-12-31` | 20 또는 배열 끝 |
| N2 | 중립 | `"pytorch" "도와주세요" is:issue is:public in:body created:2019-01-01..2025-12-31` | 20 또는 배열 끝 |

검색 조각은 모집에만 쓴다. 첫 이슈 본문의 Markdown만 격리해 P1→P2→P3→P4→N1→N2 순으로 한 자리씩 판독한다. 1번 자리 순환이 끝나면 2번으로 이동한다. 중립 배열에 속한 같은 이슈는 중립에 귀속하고 목적의 위치에는 겹침을 적는다. 각 층에서 최초 발생 슬롯을 유지한다. 계보가 확인된 같은 글은 중복으로 둔다. 저자당 최초 적격 요청 하나, 층별 최대 6명, 전체 최대 12명이다. 적격 본시험의 하한은 두 층 각각 4명 및 총 8명이다. 선정 상한에 도달해도 모집창의 나머지 첫 본문과 제외 이유를 기록한다. 미접근 앞 슬롯은 최초 적격 순서를 확정하는 데 필요한 결측으로 둔다.

목적층은 지정 조사형이 NFC 첫 본문에 실제 있어야 한다. 중립층은 네 지정형의 유무를 결과에 적는다. 적격은 작성자가 한국어로 자기 텐서 조작 또는 데이터 적재·배치 과업의 입력·출력·보존 문제를 설명한 첫 요청이다. 오탈자, 음역과 복합어는 관측 원형으로 유지한다. 번역·FAQ·재게시·이전 122/126/130/134에서 열었던 첫 글과 PR을 제외한다. 설치·모델 정확도·파이프라인 전체 상담은 텐서·적재의 저자 요구를 특정할 수 있을 때만 채택한다. 로그·인용·검색 조각만으로 저자 목표를 만들 수 없다. 요청에서 목표·시도·거절·인용·로그 역할을 표시하고 NFC 코드포인트 반열린 구간·원문 지문·구절 지문을 보존한다. 하위 조건은 관측 구절과 해석으로 나눠 기록한다.

## Q3–Q6 표시·전수 기준·재생

[AF-RES-122 카드·별칭·기존 점수 e69a3f8](https://github.com/laadkke-arch/agentflow-open/tree/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122) · [AF-RES-126 어절 abcdda4](https://github.com/laadkke-arch/agentflow-open/tree/abcdda426e2a2d19f0732752c221ea4d494458c4/docs/workstreams/research/AF-RES-126) · [AF-RES-134 투영·재생 a214140](https://github.com/laadkke-arch/agentflow-open/tree/a21414017323dbd7a090b1e7b62f070d4fa1a1ab/docs/workstreams/research/AF-RES-134/replay) · [고정 PyTorch a8d6afb](https://github.com/pytorch/pytorch/tree/a8d6afb511a69687bbb2b7e88a3cf67917e1697e)

| 정책 | 조사 8과 표시 3 |
| --- | --- |
| B | 134의 완전 어절. NFC·경계·URL/경로·수신 대상 제외 규칙을 그대로 쓴다. 양점만 조사 8, 앞 표시 3. |
| C | B에 말끝 조사 한 개 허용(은·는·이·가·을·를·에·에서·로·으로·와·과). 조사 8·표시 3은 B와 같은 예산이다. |
| Gate | 134의 C 조사 순서와 자리를 유지한다. 조사 8에서 저자 조작 구절과 카드 호환 출력 원절이 있고 필수 보존을 지지하는 카드만 순서대로 최대 3장 표시한다. |
| 조건부안 | Gate 통과 카드의 순위와 자리를 유지한다. 공석이 있을 때 C 조사 8의 보류 카드 중 첫 적격 한 장까지 다음 공석에 추가한다. 저자 목표 조작과 카드 반환이 직접 대응하고, 서로 반대인 값 하나만 미확인이고, 값에 따라 추천·보류가 갈려야 한다. 명시 금지와 양립해야 한다. 로그 단어만 맞거나 미해결 값이 두 개 이상이면 공석을 보존한다. 표시에는 짧은 조건 및 저자 조작과 카드 반환 위치를 붙인다. |

점수는 134의 자연 심벌 12, 고유 활성 별칭 구절당 4, 영어 고유 어절 교집합 수의 합을 쓴다. 동점은 카드 ID순이다. 모양 적중·활성 별칭 적중·실제 기능 자격은 각각 센다. 0점, 양점이지만 조사 8 밖, 조사 안 표시 보류, 표시 3 예산 밖, 표시 공석을 별도로 기록한다. 명시하지 않은 목표·보존을 로그·인용 심벌에서 추정하지 않는다. 기존 점수가 그런 심벌을 받는 경우 역추적할 수 있게 별도 표시한다.

첫 봉인은 모든 요청×16의 `display.csv`다. 카드의 입력/반환, 저자 구절, 호환 출력 및 유일 미확인값의 양쪽을 기록한다. 다음 커밋에서 별도 양식 `truth.csv`로 직접(역할·필수 입출력과 보존 충족), 일부(명시한 하위 조작), 충돌(요청의 반대 출력·보존 위반), 미확인(구체적 적합성 부족)을 판정한다. 사실로 뒷받침되는 복수 해석에는 독립 등급과 확인값을 남긴다. 같은 작업자가 점수·추천 결과와 후속 댓글을 보지 않고 두 번 판독한다. 두 봉인을 원격에서 읽은 뒤 후속 댓글과 재생을 연다.

하나의 초기가설은 C가 목표 어절의 별칭을 회수하면서 조사·표시를 돕는다는 것이다. 시도·거절·인용을 끌어올리거나, 정확한 후보를 8/3 밖으로 밀거나, 영어만으로 동일 후보가 이미 남는 원문이 반례다. 다른 가설은 조건부안의 공석 사용이 직접 링크의 유보를 낮춘다는 것이다. 직접 조작이 불명확하거나 추가 조건이 필요하거나, 한 줄 조건을 붙여도 반대 출력이 되는 쌍이면 반례다. 관측 반례와 동일 규칙의 가능성을 분리한다.

같은 요청과 카드의 B→C, C→Gate, Gate→조건부 변화에서 조사·표시 유입/이탈/순위 하락, 확정·조건부·공석을 센다. 조건부 직접·충돌 범위를 참/거짓 해석으로 따로 계산한다. 원절 열람 수는 134의 정의대로 정책이 검사한 원문 구절과 카드 출력 위치의 요청별 고유 수를 센다. 조건부 추가 검사는 첫 적격까지 또는 조사 8 소진까지 센다. 두 빈 디렉터리에서 입력·출력의 SHA-256을 비교한다. 이 수치는 정책상 판독 비용이며 실제 클릭·시간·이해는 측정하지 않는다.

## Q7 및 하한

MBTA에서 동명·다른 승차 위치, 이형·같은 위치, 동일 역할에 날짜 한 값이 남는 관측을 찾는다. LOC 또는 국립중앙도서관에서 같은 인물의 작곡·편곡을 식별자와 책임표시로 확인하고 편성·판 등의 한 조건을 대조한다. 교통과 서지는 검색 비교 분모 밖이다. 최소 고유 원전 22편과 유형별 8 적격 저자·6 PyTorch·4 규정/용례·2 교통·2 서지를 각각 검사한다. 복제본, 검색 조각, 같은 스레드의 댓글, 미접근은 고유 저작 수에서 제외한다. 모집창이 끝나도 층 또는 자료 유형 하한을 충족하지 못하면 PARTIAL이다.
