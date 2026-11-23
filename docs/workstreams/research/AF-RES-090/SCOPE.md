# AF-RES-090 — 현재 독자의 두 번 열람 계약

- 실제 시작 통합 SHA: `c2709abf8d25163eed75a7553ebcbde966105b55` (2026-11-23 UTC에 원격 조회 후 clone). 계획 SHA `62a80b9f111c695527a8ca87bcb867796d2e96bb`와 구별한다.
- 작업 브랜치: `work/research-af-res-090`; 유일 쓰기 범위: `docs/workstreams/research/AF-RES-090/`.
- 유일 선행: `work/research-af-res-086@6907534462af729f409c52ce08d3331de22c96e6`의 HANDOFF. 결과 입력은 `e6a79c3ac05b84ea1c7db313233df1717cade756`의 RESULT, cards, comparison, routes, claims다. 선행의 현재/역사 구분을 인수하며 역사적 제공·빌드·복구·동시 제공을 재조사하지 않는다.
- AGENTS, STATE, START_HERE, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF와 시작판의 dot-control 자기 행을 직접 읽었다. 자기 행은 RUNNING, 의존 086은 DONE이며 result_commit은 위 값이다. 중앙 진행표는 수정하지 않는다.
- manifest는 지정된 `python -B -m workbench.session start … --fetch` 명령으로 생성했으며 계약 v2와 실제 시작판·의존 SHA를 고정한다.

## 모집과 사전 선택 규칙

고정 네 자리 × 두 목적 × A/B = 16판독; 목적별 대응쌍은 8쌍이다. P1의 404도 교체하지 않는다. 아래 목적은 연구자가 부여한 판 확인 과제다. 발행자가 약속한 내용·대상 독자는 별도 원문으로 확인한다.

| 목적 ID | 지정판과 읽을 것 | A | B | 후속 선정 규칙 |
|---|---|---|---|---|
| P3-body | cibuildwheel 3.3.0 enable | https://cibuildwheel.pypa.io/en/stable/options/#enable | https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable | 본문에서 끝냄 |
| P3-next | 안내된 1.x 지원 Python 표 | 위 A | 위 B | 발행자가 명시한 1.x 표. 3.3.0과 동일한 판이라는 뜻이 아니라 발행자가 연결한 구계열 판 식별 |
| P1-body | bandersnatch 7.0.1 발행자 사용 설명의 첫 설정 예제 | https://bandersnatch.readthedocs.io/en/latest/ | https://bandersnatch.readthedocs.io/en/7.0.1/ | 고정 소스의 사용 설명에서 첫 설정 예제를 선정 |
| P1-next | 그 예제의 첫 동작 관련 참조/설정 문서 | 위 A | 위 B | 예제 안의 DOM/소스 순서 첫 후보, 없으면 본문 내 명시 경로 없음 |
| R1-body | archive 1.1.12 archive_read Usage/Examples | https://archive.r-lib.org/reference/archive_read.html | https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html | 본문에서 끝냄 |
| R1-next | 고정 예제의 첫 동작 관련 참조 | 위 A | 위 B | Examples 안의 DOM 순서 첫 동작 관련 href/URI, 없으면 본문 내 명시 경로 없음 |
| R2-body | asciicast 2.3.1 init_knitr_engine, Using SVG files | https://asciicast.r-lib.org/articles/asciicast-demo.html | https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html | 본문에서 끝냄 |
| R2-next | 해당 예제의 첫 SVG/재생 자원 또는 인라인 payload | 위 A | 위 B | Using SVG files의 첫 src/href/data. 인라인이면 추가 열람 0 |

후속 주소·anchor·DOM 순서·href/src·내장 데이터·원 URI·base를 읽고 **목적지를 요청하기 전에** 2차 커밋으로 봉인한다. 기준이 바뀌면 원 값·이유·UTC를 후속 커밋에 남긴다. 인기 있는 다른 예제로 교체하지 않는다.

## 열람·채점 정의

1. 독자 판독은 입구를 포함해 최대 두 문서/자원 열람이다. 각 판독의 실제 URL 순서, 리다이렉트, UTC, HTTP 상태, MIME, 응답 바이트와 SHA256을 남긴다. 같은 페이지 안 anchor 이동과 인라인 payload는 추가 문서 열람 0이다. HTTP redirect 내부 hop과 페이지의 자동 하위 요청은 문서 열람 횟수와 별도다.
2. 생성 HTML 원본·고정 소스·Git tree/API의 보조 대조는 독자 경로 밖이다. 보조 요청으로 발견한 파일을 독자가 두 번 안에 읽었다고 승격하지 않는다. GitHub 파일 보기는 HTML 소스 표시이며 Raw는 두 번째 열람을 소비한다. 상대 URI를 수동 조립하면 그 사실을 별도 표시한다.
3. `target_body`, `followup_resource`, `same_version`은 독립 축이다. 값은 `confirmed`, `refuted`, `unconfirmed`, `inaccessible`, `no_explicit_path`, `not_applicable`를 사용한다. HTTP200 자체는 성공이 아니다. 판 반박·경로 없음·접근 실패·판 근거 미확인을 합치지 않는다.
4. P3-next는 발행자가 지정한 1.x **목적판** 확인과 그 안내 연결을 평가한다. 1.x가 3.3.0과 같은 릴리스라는 잘못된 점수를 만들지 않는다. R 자원은 같은 생성 commit 파일인지와 현 서비스 응답 일치 여부를 나눈다.
5. 정적 본문/자원 확인은 JavaScript 실행·R/Python 예제 실행 성공과 다르다. 사람 독해 시간은 측정하지 않는다. 브라우저 관측과 HTTP/DOM 대조도 구분한다.
6. 일부 원자료가 막히면 공개 고정 트리/배포판을 한 번 보조 대조하고 실제 독자 경로는 도달한 곳에서 끝낸다. proxy 오류를 원 서비스 영구 장애로 단정하지 않는다.

## 원자료·반례·작업 분담

고유 직접 1차자료 최소24개: 발행자 안내/지정판 HTML·소스8, 실제 후속/패키지 다른 파일6, 생성·호스팅·상대 경로 처리 공식 자료6, IIIF와 EPUB의 규격+실제 저작 각각2. 같은 파일의 GitHub/Raw/미러 및 같은 바이트는 중복 산입하지 않는다. 실패·검색 요약·선행 인용·자체 실행은 제외한다. 계보 ID로 독립 저작 수도 나란히 센다.

Python 두 자리, R 두 자리, IIIF/EPUB는 분리 조사하고 주 작성자가 방법 자료와 통합·검산을 맡는다. 각 조사자는 자기 streams 하위만 작성한다. 커밋은 주 작성자가 순서대로 수행한다. 자기 검토와 다른 조사자의 대조를 구분한다.

사전 예상은 고정 파일이 본문 판 식별에 유리하지만 다음 자원의 접근성을 보장하지 않을 수 있다는 것이다. 반대 방향도 조사한다: 단일 절/인라인만으로 충분한 자리, 현재 서비스가 지정판과 일치하는 자리, 같은 HTML이 다른 자원을 가리키는 자리, 목록은 있으나 자원이 읽히지 않는 자리. 실제 반례가 없으면 탐색 경로와 결원을 보존한다.

## 완료와 제외

필수 표 세 개 → 분모 → 방법/해석 순서를 따른다. 필수 근거가 없으면 PARTIAL. HANDOFF는 마지막 단독 커밋이며 결과 SHA에서 계약·공통 검사와 원격 재열람의 실시 범위를 적는다. main 병합·배포·계정 변경·유료 API·역사적 게시 조사·실행성 주장은 범위 밖이다.

## 실행 뒤 해석과 기록 보완 — 2026-11-23 UTC

원격 묶음 ①은 `973897922e07d0e63a4c68c377422b1a65ce0f27`, ② 후보 봉인은 `c2a3f387cc962abd1ef383e39f750cc23ee5e51a`, ③ 실제 열람·반례·타분야 원장은 `833071b378ab379188c7b62c4a013621a4958bdf`다. 최종 결과/검사/인계 SHA는 HANDOFF에 연결한다.

- R2-next의 이전 broad confirmed는 정적 pre 읽힘만을 뜻했다. 독립 검산 뒤 엄격 SVG/재생 후속축은 `no_explicit_path`, 정적 출력은 `static_output=confirmed`로 분리했다. 원 봉인과 이전 기준은 그대로 두고 `streams/r/evidence/R-coding-adjustment.json` 및 최종 targets.csv의 prior_success_criterion에 이유·UTC·원값을 보존했다. 데이터나 목표 예제로 교체한 것은 아니다.
- P3의 봉인 원URI는 `/en/1.x/`이고 목표는 그 root의 지원 표다. `#what-does-it-do`는 이후 실제 root 대조에서 확인한 anchor다. 주 경로의 `/1.x/options/` 표를 사후 목표로 바꾸지 않았다. same_version의 legacy1.x는3.3.0과 동일 release가 아니라 별도로 의도한 목적 계열이라는 뜻이다.
- 주16행은 봉인 링크를 따른 독립 HTTP 읽기다. UI는 메뉴 클릭성·GitHub source/Raw 표시를 확인한 보조 관측으로 `streams/ui/observations.json`에 보존했다. 주 GitHub503 세 건을 이전/UI200으로 치환하지 않았다.
- 원장 최소량은 적격45자료·18계보다. R의 추가 tree/ref/commit목록5건도 원장에 남겼으나 구성 최소량에서는 제외했다. 선행6파일·실패·미러·재요청도 제외했다.
- 공통 검사는 소유 경로 안의 임시 복제본 및 TMPDIR에서 원래 검사기를 변경하지 않고 실행한다. 공통 검사기의 .workbench/lab 출력이 원래 checkout의 허용 경로 밖에 생기지 않도록 한 실행 위치 선택이며 검사 조건을 완화하지 않는다.
