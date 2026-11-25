# AF-RES-252 범위와 사전 규칙

## 착수 기준

- 2026-11-24 UTC 착수. GitHub의 `chore/workspace-foundation` HEAD `d1353701530ffd4c68587276c15d988d2cc92972`에서 `work/research-af-res-252`를 새로 만들었다. `session.json`은 `workbench.session start --fetch`의 출력이다. 계약 v2, 단일 허용 경로 `docs/workstreams/research/AF-RES-252/`, 의존 브랜치와 SHA를 고정했다.
- 계획판 `7369707441e2eb70e84004ca6cb3bfeefc8b4061`과 착수판의 diff는 `docs/automation/dot-control.json` 한 파일이다. 두 contents 본문이 비어 blob `f6587b49dccac907b5e2dd1e67bf3e36c1590ccd`, `41cefbc22f8d86795d0aff7204c9cbefb69577fa`에서 읽었다. 작업 240→253개, 계획판에는 252가 없고 착수판에 252 RUNNING/attempt 1/depends_on AF-RES-231이 있다. 231의 항목과 SHA가 동일하다. 진행표에는 쓰지 않는다.
- 착수판의 AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, CLOUD_WORKFLOW, START_HERE, 제품 브리프를 읽었다. [AF-RES-231 고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/e55fd8c9df7fdd45259346aeb8884a7d3586594b/docs/workstreams/research/AF-RES-231/HANDOFF.md), 같은 판의 RESULT, SCOPE, receipts/INDEX.json, control_predictions.csv를 읽었다. 중앙 DONE, 자체 PARTIAL, 4개 예정 사건·8개 경로 모두 미관측, 제목식 질의의 이전 대응값 없음. 이번 제목식 질의는 새 비교 조건이다. 238–242의 입력·결과를 사용하지 않는다.

## 모집과 입력판

1. Stack Exchange API v2.3, site=dba, `fromdate=1325376000`, `todate=1735689599` (2012-01-01~2024-12-31 UTC, 끝점 포함). `/questions`의 `tagged=postgresql;greatest-n-per-group` AND, `sort=creation&order=asc&pagesize=100`. 원페이지 배열·UTC·HTTP·quota·backoff·has_more·SHA-256을 보존한다. 원위치는 페이지·페이지 내 1기준과 누적 1기준을 함께 쓴다. 120번째의 생성 초가 끊기는 곳 또는 종료 응답까지 확인한다. 같은 초는 질문 ID 오름차순으로 정렬해 최초 120개를 표시한다. 페이지 간 생성시각 역전·중복 ID는 경계 유효성 실패로 남긴다.
2. 처음 120개에서 `closed_reason`을 공백 제거·소문자화해 정확히 `duplicate`인 상태를 찾는다. 그 순서의 첫 12개를 기계 후보로 삼는다. 12개를 넘은 수와 정상 부족을 따로 집계한다. 모집 단계의 응답 필터에서 답과 중복 대상은 요청하지 않는다. 254가 이 후보군에서 그룹별 최신 원행을 요구한 처음 4건을 의미 판독한다. 보정 #138641은 별도 라벨을 붙인다. 모집과 겹치면 원영수증을 재사용한다.
3. 원질문의 현행 질문과 `/posts/{ids}/revisions`를 따로 보존한다. 게시 시각과 일치하는 공개 최초 `revision_number=1`에 title/body가 함께 있으면 원본 판을 선택한다. 정상 종료된 revision 열에서 해당 전문을 확인할 수 없으면 현행 판을 사용하고 빠진 근거를 남긴다. 네트워크·필터·페이지 실패로 원본의 존재 자체를 가를 수 없으면 그 질의를 미확인으로 둔다. 보이는 가장 오래된 revision과 선택판을 구분한다.
4. A는 고른 title을 HTML entity 해제·소문자화하고 정규식 `[a-z][a-z0-9_]*`로 토큰화한다. `a an the how can i to of in for from with postgresql postgres sql`만 삭제한다. 앞 토큰 4개(반복 유지), 2개 미만이면 A 공석이다. `queries.csv`에 원제목·전체 토큰·이유(불용어·4개 한도)·선택 토큰·질의·입력판·해법어 표식을 남긴다. 명시 해법어 표식은 `DISTINCT ON`, `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LATERAL`, `GROUP BY`, 윈도 함수 표시의 고정 어휘로 붙인다. 이 표식의 누락 가능성이 있으며 질의에서 추가 삭제하지 않는다. 표제/토큰과 증거를 Git에 커밋한 뒤에만 후보의 A 검색과 B 원배열을 개방한다.

## 선택과 판독 개방

- A는 `/search/advanced?site=dba&tagged=postgresql%3Bgreatest-n-per-group&sort=relevance&order=desc&pagesize=5`에 봉인 질의를 더한다. 검색에는 모집 날짜를 적용하지 않는다. 제공자의 OR raw top5와 제공자 전순서에서 AND를 충족한 부분수열의 최초 5를 기록한다. 이 부분수열에서 자기 ID를 뺀 첫 요소를 선택한다. 출력 순위를 재정렬하지 않는다. 5개 확보, has_more=false, 익명 API 페이지 한도(25), 실패 중 먼저 만난 종료 상태와 추가 비용을 남긴다.
- B는 `closed_details.original_questions` 원순서의 첫 ID다. 자기 경로를 사용 가능한 외부 도착으로 세지 않는다. 검증된 필터와 정상 wrapper에서 원글·`closed_details`·`original_questions`의 생략과 빈 배열을 각각 구분한다. 필드가 생략된 경우는 제공된 외부 도착의 공석으로 기록하며 실제 중복 관계는 미확인이다. 전송·필터 결측과 자료형 오류는 별개다.
- 도착 질문당 1회 본문, 채택 답 ID 우선(채택 ID GET이 비면 대체하지 않음). 채택 ID가 없으면 전체 답 메타를 score 내림차순·creation_date·answer_id 오름차순으로 정렬한다. 고른 한 답만 본문을 가져온다. 공유 질문·답의 물리적 GET을 재사용하고 논리적 경로 예산을 따로 기록한다. 공개 출처·귀속은 대응표에 두고 판독판에는 배치하지 않는다.
- 254의 개방 순서는 manifest → origins → destinations → mapping이다. origins는 후보 순번과 익명 라벨·가림 본문으로 구성한다. destinations는 무작위 순서·불투명 라벨을 사용한다. 중복 뱃지·글 링크를 지우고, origin에서 해법의 직접 단서가 되는 SQL 코드 블록을 마스킹한다. 도착 답의 SQL은 남긴다. 키워드·표현·데이터에서 원글 또는 해법을 역추정할 수 있는 한계를 기록한다. 원문과 연결표는 별도 보존한다.
- 누락된 first-window를 정상 빈 표로 만들지 않는다. 미수신·부분 전송·스키마 또는 transport 오류, 검증된 빈 배열, 사전 공석, 적용 대상 밖을 각각 기록한다. 정상 0 모집의 경우 실제 수신한 영수증으로 0을 증명해야 한다. 필수 배열과 입력이 확정되기 전에는 254를 열지 않는다.

## 원자료·사전 반증 조건

- 공식 문서의 AND/OR 차이가 있기 때문에 raw top5와 AND 부분수열 선택이 달라질 수 있다. 같은 초의 마지막 페이지를 건너뛰면 다른 ID가 120번째가 되는 사례를 검사한다.
- 원판에 해법어·링크가 있거나 후편집에 추가될 수 있다. 마스킹은 단서 저감이며 누출까지 검사한다. 첫 B가 자기인 배열, A/B가 동일 질문·답인 배열, 빈 배열과 미수신, 채택 답 누락, 동점 점수 역순을 대조한다. 가설은 아직 실제 모집의 관측이 아니다.
- Crossref 두 서지 비교의 예측은 검색된 레코드의 내보낸 DOI 열과 서버 cursor 순서가 일치하며, 정상 빈 결과·카운트만 있는 정상 응답·HTTP 미수신을 구별할 수 있다는 것이다. Stack Exchange와 별개 표로 다룬다. DBA 외부 보조와 PostgreSQL 규격은 근거 원장에 별도로 표시한다.
- 언제든 원질문 요구, 동률 의도, 답 적합도, A/B 우열은 254가 판독한다. 여기서는 정해진 모집·수신·선택·익명화만 검사한다.
