# AF-RES-108 · 모집과 판정

링크에 붙인 짧은 발췌에서 예외 문장에 자리를 주면, 실행으로 틀렸음을 확인할 수 있는 적용과 근거 부족으로 유보한 적용이 어떻게 바뀌는지 묻는다. SQLite 조회 네 층과 Flexbox 레이아웃 네 층에 각각 한 쌍을 배정한다. 두 구간은 탐색 결과 한 링크의 표시 형식을 비교하는 단위다.

| 저장소 기준 | 고정 내용 |
| --- | --- |
| 계획 통합판 | [49f603a](https://github.com/laadkke-arch/agentflow-open/commit/49f603a98188fbf2009c4c490b0539f32d124e38) |
| 시작 시 원격 관측 | [e601fa1](https://github.com/laadkke-arch/agentflow-open/commit/e601fa1aed009106be983ae9b24e4778e793276f). 계획판과의 파일 차이는 `docs/automation/dot-control.json` 하나다. |
| 계약 직전 원격 관측 및 시작 기준 | [32b6bb3](https://github.com/laadkke-arch/agentflow-open/commit/32b6bb32989730df78d521c29a50dbebd3289b46). 시작 관측판에 비해 같은 진행표만 바뀌었다. manifest 생성 전에 작업 브랜치를 fast-forward했다. |
| 운영 의존 | [등록 인계 ce82834](https://github.com/laadkke-arch/agentflow-open/blob/ce8283488ab46a76f2d5fa081db5c4734f302526/docs/workstreams/research/AF-RES-104/HANDOFF.md). 원격 끝도 동일했다. |
| 연구 입력 | [검사받은 f38c0af](https://github.com/laadkke-arch/agentflow-open/blob/f38c0af427c66876bf411bfd0a728cfcd60013eb/docs/workstreams/research/AF-RES-104/RESULT.md). 이 판에서 운영 끝까지 바뀐 파일은 선행 HANDOFF.md 한 개다. |

시작 때 GitHub에서 AGENTS, STATE, Dot 운영 규칙과 진행표의 AF-RES-108 및 AF-RES-104, 연구 운영 규칙과 제품 브리프를 읽었다. AF-RES-104의 인계와 고정 RESULT, protocol, metrics, feature-visibility, exposure를 읽었다. W2가 회복한 두 자리는 한 고유 J1이다. F 제약 12자리 중 W2가 11자리, W1이 6자리를 놓쳤다. 같은 S에 대한 30개 조건 재판독은 16개가 달랐다. 예전 jq·Pandoc, J1의 최종 JOIN, SQLite 재귀 CTE FIFO, CSS Grid와 보조 WPT는 계승 근거다.

## 모집과 공개 순서

1. 이 파일과 protocol로 판 선택, 시작 페이지, 후보 정렬, 변이 허용 범위 및 판정 형식을 원격에 고정한다.
2. 2025-12-31 UTC 종료를 기준으로 SQLite 정식 배포의 소스 및 문서 계보, WPT 기본 브랜치와 W3C Flexbox 판을 확인한다. 입출력을 자동 분리한다. 모집 화면에는 테스트의 상대 경로, ID, 입력 및 assertion 종류만 내보낸다. 기대값, 참조 파일과 출력은 별도 임시 디렉터리에 두고 해시를 기록한다. 후보에서 노출된 이름이나 입력 힌트를 기록한다.
3. 각 층은 아래 출발 경로 안의 적격 시험을 경로와 test ID의 문자열 오름차순으로 훑는다. 첫 적격 시험을 택한다. 주제당 최대 30후보이며 상류 기대값, 예상 차이, 브라우저 결과는 선정 조건에 없다. 후보가 없으면 결원을 둔다. 같은 파일의 다른 subtest는 자료를 새로 추가하지 않는다.
4. ① 모집·입력·예산을 원격에 고정한 뒤 제공자 문서 본문을 자동 변환하고 익명 화면을 만든다. ② 전체 사전 답을 원격에서 확인한 뒤 원 기대와 실행 결과를 연다. ③ 실행과 반례를 원격에 고정한 뒤 ④ 비교와 자가검산을 고정한다. 검사 및 GitHub 재열람 뒤 HANDOFF를 별도 커밋한다.

| 층 | 상류 출발 경로와 입력 필터 | 최초 적격과 편집 |
| --- | --- | --- |
| S1 NULL 비교 | `test/null.test`. `=, ==, !=, <>` 등 일반 비교의 NULL 피연산자가 될 수 있는 정적 projection 또는 predicate | 비교식의 숫자 리터럴 1개를 NULL로 바꾼다. 숫자가 없으면 앞선 고정 INSERT의 해당 피연산자 열의 첫 숫자를 NULL로 바꾼다. 원래 NULL이면 0으로 바꾼다. 단순 CASE 안 비교를 포함한다. |
| S2 집계 | `test/func.test`, `test/sum.test`. 정적인 단순 `sum` 또는 `total` 호출 | 인수의 첫 데이터 숫자 한 개를 NULL로 바꾼다. 인수가 열이면 앞선 고정 INSERT에서 그 열의 첫 값 1개를 사용한다. 0은 유효한 입력이다. |
| S3 정렬/동점 | `test/select1.test`, `test/sort.test`. 첫 단순 SELECT로 결과에 이름이 있는 단일 ORDER BY 키 및 식별 가능한 둘 이상의 행 | 직접 초기화한 첫 키를 다음 서로 다른 수치 키로 바꿔 동점을 만든다. 동점군 내부 순열은 허용한다. 원래 키들에도 동점이 있을 수 있다. |
| S4 window frame | `test/window1.test`, `test/window2.test`. 고정 입력과 리터럴 ROWS/RANGE/GROUPS 경계 | 처음 등장하는 정수 PRECEDING/FOLLOWING 경계를 0→1 또는 양수→0으로 바꾼다. SQL 오류를 허용하려는 비교는 제외한다. |
| F1 자동 여백 | `css/css-flexbox/`의 HTML 경로명에 `margin`과 `auto` 모두 포함 | flex 항목에서 처음 해당하는 물리·논리 margin 속성의 `auto` 하나를 0으로 바꾼다. 원본 auto는 경계다. 좌표는 해당 항목의 주축 시작 위치, 축이 다른 경우 여백이 적용되는 축이다. |
| F2 wrap | 같은 경로에서 `wrap`이 포함된 파일 | 명시 `flex-wrap` 또는 `flex-flow`의 `wrap↔nowrap`, `wrap-reverse→wrap`. 여러 형제가 있는 동일 컨테이너에서 두 번째 이후의 첫 줄바꿈 가능 항목을 관측한다. |
| F3 정렬 | 같은 경로에서 `align-items`, `align-self` 또는 `justify-content` 포함 | 명시된 첫 키워드에서 `flex-start/start/normal/stretch→center`, 나머지는 `flex-start`로 바꾼다. 적용 대상 첫 항목(align-self면 속성 보유자)의 정렬 축 좌표를 관측한다. |
| F4 축/방향 | 같은 경로에서 `direction` 포함 | 가장 먼저 적격인 선언 `flex-direction` 또는 `flex-flow`의 `row↔row-reverse`, `column↔column-reverse`. 첫 항목의 해당 축 좌표다. |

SQL 적격의 공통 조건은 정적 Tcl `do_test {execsql {...}}` 또는 `do_execsql_test` 페이로드, 닫힌 로컬 스키마 및 값, 대상 SELECT를 식별할 수 있는 입력이다. 필요한 이전 DDL/DML만 포함한다. 외부 파일·런타임 Tcl 변수·SQLite 설정이나 임의의 앞선 SELECT 부작용이 필요하면 탈락이다. 수동 확인은 마스킹한 SQL에서 수행한다. 결과는 SQL 값과 스토리지 타입의 튜플로 기록한다. SELECT에 행 순서 보장이 없으면 중복을 유지하는 행 멀티셋으로 본다. ORDER BY 동점은 해당 키의 동점군에서 순서를 요구하지 않는다.

CSS 적격의 공통 조건은 WPT 기본 harness 또는 reftest 신호, 외부 페이지 이동이 필요 없는 단일 관측 대상, 명시한 속성 값 한 개를 바꿀 수 있는 입력, CSS와 DOM만으로 어느 컨테이너 및 항목 좌표를 관측할지 식별 가능한 시험이다. 제목, assertion 값, 참조 링크 경로, CSS/HTML 주석, 인라인 JS 내용은 마스킹한다. 테스트의 보이는 본문에 출력을 말하는 문장이 남아 있으면 노출을 기록한다. CSS 좌표는 컨테이너 border box를 원점으로 하는 CSS px, 허용 오차 0.5px, 뷰포트 목표 800×600 CSS px, DPR 1이다. 표의 좌표 외에 전체 rect를 수집한다. 글꼴과 viewport는 실행 시 확인한다. 외부 의존성이나 기대값 차이는 모집에 사용하지 않는다.

정상/경계는 동작의 통상값/바꾼 조건 이름이다. S1·S2의 숫자판, S3의 원 케이스, S4의 양수판, F1의 0판, F2의 nowrap판(없으면 원본), F3의 flex-start·start·normal·stretch판(없으면 원본), F4의 역방향이 없는 판을 기본 정상으로 둔다. 원본과 수정판은 표에서 따로 표시한다. 하류의 합성 변이를 자연 요청이나 추가 상류 시험 수로 세지 않는다.

## 제공자 문서 찾기

키워드 점수는 문서 선택 뒤에만 계산한다. 제공자 공식 시작 페이지는 SQLite 릴리스의 SQL Language Expressions, Aggregate Functions, SELECT, Window Functions 페이지를 층 순서대로 각각 고정한다. Flexbox 네 층은 컷오프 시 최신 정식 W3C TR CSS Flexible Box Layout Level 1 하나를 공유한다. 각 시작 페이지의 버전 색인에서 컷오프 이하와 날짜 최신을 우선하고, 같은 날짜일 때 URL 바이트 순 첫 공식판을 택한다. SQLite 문서 HTML은 버전 배포 zip의 해당 파일 첫 경로를 사용하고 같은 시점 docsrc와 연결한다. 파일 내부는 큰 절 하나를 잘라 심는 대신 문서의 본문 전체를 한 번 문자열로 만든다. 네 Flexbox 질문의 시작 페이지가 같으므로 HTML과 변환도 한 번이다. POSIX와 SVG는 본 표본의 답을 봉인하고 나서 같은 규칙으로 교정한다.

## 문서 취득 편차

원격 예측을 봉인하기 전 실제 취득 방식과 편차를 고정했다. Cloud 셸은 sqlite.org·w3.org의 원문 HTTP를 거절했다. SQLite 문서 ZIP과 날짜 고정 docsrc 경로는 web 열람도 실패했다. 그래서 SQLite의 게시자 공개 웹 본문 네 개를 같은 순서로 대체하고 서로 겹쳐 받은 전체 행의 지문을 봉인했다. 3.51.1 당시 문서와의 등가성은 미확인이다. W3C 당시판은 게시자 페이지의 전 행을 받았다. 양쪽 영역에서 반환된 HTML 텍스트 뷰를 공통 변환하고 그 뷰의 행·열로 역매핑했다. 원시 HTML 태그 좌표는 미확인이다. 정확한 원문이 확보되면 새 입력군으로 다시 봉인할 수 있다. 현재 예측 커밋을 바꾸지 않는다.
