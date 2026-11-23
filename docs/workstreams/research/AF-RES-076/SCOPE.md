# AF-RES-076 사전 등록

## 계약과 출발점

계획 SHA는 `39cadb6ecdf62d0b21c0cce67834f2aef3bf6853`다. 배정 시 GitHub 통합 HEAD는 `3ac1f42628930ead89dfcb1bd38f3a8e74c9c192`였고 그 SHA에서 원격 `work/research-af-res-076`을 만들었다. 계약 생성의 원격 갱신에서 `817ee771ebfa63d4a177ee12f46b9818a6335308`을 읽었다. 그 사이 변경은 다른 과제의 배정 원장이며 076의 범위·072 결과 핀은 같았다. 문서는 `AGENTS.md`, `STATE.md`, `docs/DOT_AUTOMATION.md`, `docs/RESEARCH_WORKFLOW.md`, `docs/product/RESEARCH_BRIEF.md`, `docs/automation/dot-control.json`의 076·072 행을 확인했다. 실행은 별도 Codex Cloud checkout에서 수행한다. [배정 시 통합판](https://github.com/laadkke-arch/agentflow-open/tree/3ac1f42628930ead89dfcb1bd38f3a8e74c9c192) · [시작 계약](manifest.json)

선행 연구의 유일한 결과 핀은 `f77d2d68b3361df5a0fd70d5ea10df79b08b0f09`다. 072의 보류 120쌍에는 직접 적격이 없었고 I/H의 두 회수는 같은 쌍, P의 원거리 회수는 다른 쌍이었다. 첫 URL은 6건 모두 A07이었다. 결과 Q2–Q7, qrels, route-reading과 report.py를 연결하면 개별 관찰은 6/54이며 report.py는 반박 이외를 기권으로 매핑했다. 076에서 표 자리, 실제 노출, 개별 판독, 기권, 오채택을 각각 추적한다. 072의 보류·번역·X01은 076 입력·성적에 포함하지 않는다. [072 인계](https://github.com/laadkke-arch/agentflow-open/blob/f77d2d68b3361df5a0fd70d5ea10df79b08b0f09/docs/workstreams/research/AF-RES-072/HANDOFF.md) · [072 결과 Q2–Q7](https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/RESULT.md#q2-회수와-첫-적격-순위) · [072 개별 관찰](https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/evidence/route-reading.json) · [072 보고 코드](https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/report.py#L102-L118)

## 후보 모집틀

- UTC 2025-12-31 이전 PyPI의 비회수 공개 안정판 중 가장 최근 업로드된 세 정수 버전을 고른다. Pillow 12.0.0의 최초 업로드는 2025-10-15T18:21:27.791040Z, 다음 12.1.0은 2026-01-02T09:10:24.953078Z다. DuckDB 1.4.3은 2025-12-09T10:57:46.847367Z, 다음 1.4.4는 2026-01-26T11:48:41.591164Z다. 태그 실체는 각각 `693df7b42c666f88c719f9973be0ad71607328e0`, `d1dc88f950d456d72493df452dabdcd13aa413dd`다. [Pillow 배포 원장](https://pypi.org/pypi/pillow/json) · [DuckDB 배포 원장](https://pypi.org/pypi/duckdb/json) · [Pillow 릴리스](https://github.com/python-pillow/Pillow/releases/tag/12.0.0) · [DuckDB 릴리스](https://github.com/duckdb/duckdb/releases/tag/v1.4.3)
- Pillow는 릴리스 Reference toctree의 첫 8개 모듈 페이지를 순서대로 선택한다. TOC 줄 8–15가 P01–P08이다. 한 페이지가 검색 단위이며 해당 페이지가 선언한 autodoc 함수·클래스는 오프라인 적격 판독의 보조 원절이다. 요청 경로에서 내려받는 원문은 고정 RST 페이지 한 편이다. [Reference 목록](https://github.com/python-pillow/Pillow/blob/693df7b42c666f88c719f9973be0ad71607328e0/docs/reference/index.rst#L4-L39)
- DuckDB는 웹 저장소 기본 브랜치 첫부모 중 같은 마감 전에 마지막인 `a9b46353200eb713d5211684a6234d701d34e4bd`의 안정판 내비게이션을 사용한다. CSV의 메뉴 4편과 Query Syntax의 앞 4편을 표시 순서로 선택한다. 1.4.3 배포일 스냅샷 `79b126c3c72de63028ae5ae4eecf17d9ce53b022`과 선정 경로 및 메뉴에 변경이 없었다. 기능으로 인정하려면 v1.4.3 문서와 코드·시험판에서 성립해야 한다. 후속 수정은 후보에 넣지 않는다. [내비게이션](https://github.com/duckdb/duckdb-web/blob/a9b46353200eb713d5211684a6234d701d34e4bd/_data/menu_docs_stable.json#L37-L62) · [SQL 메뉴](https://github.com/duckdb/duckdb-web/blob/a9b46353200eb713d5211684a6234d701d34e4bd/_data/menu_docs_stable.json#L618-L689) · [당시 배포 이력](https://github.com/duckdb/duckdb-web/blob/a9b46353200eb713d5211684a6234d701d34e4bd/_data/past_releases.csv)
- 다른 분야는 네 개념의 사전 지정 일대일 대조다. X01은 이미지 크기/잘라내기 → 브라우저 CSS Images L3, X02는 표시/상자 → 브라우저 CSS Display L3, X03은 열/출력 → 웹 발행 W3C CSVW Metadata Recommendation, X04는 필터/가시성 → 지도 렌더러 MapLibre v8 스타일 사양이다. 각 독립 사양의 전체 소스 문서가 검색 단위다. X01/02는 CSSWG 기본 브랜치에서 마감 전 해당 파일의 마지막 수정, X03은 2015-12-17 REC 발행 스냅샷, X04는 MapLibre 기본 브랜치 첫부모 마감 이전 마지막의 v8 JSON이다. 후속 발행판·요약·렌더러 구현은 이 네 자리를 늘리지 않는다. [X01 편집 원문](https://github.com/w3c/csswg-drafts/blob/ea83cc06d6454f39cbc75e0da90a4ef276a5fb15/css-images-3/Overview.bs) · [X02 편집 원문](https://github.com/w3c/csswg-drafts/blob/ccb66ec19e37a98ac26c16f5474f1011c93cb05b/css-display-3/Overview.bs) · [X03 공식 발행](https://www.w3.org/TR/2015/REC-tabular-metadata-20151217/) · [X04 렌더러 사양 원본](https://github.com/maplibre/maplibre-style-spec/blob/d7f15a9e5430730d2cc6aaba9337a3dbb14885f9/src/reference/v8.json)
- 세 방식 모두 같은 GitHub 고정 파일 주소를 링크로, 같은 raw 대응 주소를 전송 대상으로 쓴다. 전체 소스 파일 범위는 바꾸지 않는다. 출처 수를 셀 때 Pillow 가이드의 절과 DuckDB 가이드의 여러 페이지는 각 하나의 저작으로 묶는다. 직접 읽은 별도의 PR·시험 설계·릴리스·요청은 사건을 중복하지 않는 경우에만 센다. [선정과 탈락 전수](frames.csv)

## 자연 요청 모집

API 식은 GitHub Search Issues의 `sort=created&order=asc`와 아래 q 문자열이다. 생성 시각 UTC 오름차순, 시각 동률은 이슈 번호 오름차순이다. 범위는 2023-01-01부터 2025-12-31까지 양 끝 날짜 포함이다. 첫 페이지 최대 30개부터 보며 3개를 채우면 멈춘다. 30 내 세 자리가 비면 같은 조건과 페이지 경계를 유지한다. 직접 REST 연결이 안 되면 같은 검색을 GitHub 커넥터에 전달한다. 이 경로가 응답하지 않으면 GitHub 공개 이슈 목록의 동일 q·정렬로 대조하고 어떤 경계가 달라졌는지 표시한다.

```
repo:python-pillow/Pillow is:issue in:body "Pillow versions" created:2023-01-01..2025-12-31 -label:security
repo:duckdb/duckdb is:issue in:body "DuckDB Version" created:2023-01-01..2025-12-31 -label:security
```

두 문구는 같은 프로젝트 릴리스의 입력 양식에 있다. 제목과 최초 작성자의 본문으로만 부분·목적·구별 가능한 C1/C2·환경을 기록한다. 관찰 재현에서 C1과 C2가 각각 독립적으로 틀릴 수 있어야 한다. 이후 댓글·링크된 해법·라벨의 해결 상태·PR 구현은 모집에서 읽거나 쓰지 않는다. 같은 최초 보고나 입력과 기대가 같은 명시적 중복은 앞 사건만 유지한다. 범위 밖 일반 문의·환경 또는 조건이 빈 항목·보안 취약점·최초 본문을 확보할 수 없는 편집 항목은 사유와 순번을 남긴다. 관찰된 최신 본문을 최초 본문으로 보는 근거는 GitHub의 원글 수정 표지가 없다는 것까지이며 수정 이력 누락 가능성은 남는다. 개인 연락처·실명 양식은 저장하지 않는다. [Pillow 양식](https://github.com/python-pillow/Pillow/blob/693df7b42c666f88c719f9973be0ad71607328e0/.github/ISSUE_TEMPLATE/ISSUE_REPORT.md) · [DuckDB 양식](https://github.com/duckdb/duckdb/blob/d1dc88f950d456d72493df452dabdcd13aa413dd/.github/ISSUE_TEMPLATE/bug_report.yml)

## 카드, 기대 판정, 경로

1. 사전 등록 후 20개 원문만 사용해 S와 E를 고정한다. S는 문서의 첫 설명 문장을 문서 마크업 제거 후 가져온다. E는 작성자가 문서에서 확인한 목적·동작·경계를 한 카드로 쓴다. 두 경우 이름과 설명을 합쳐 공백 단어 40개 이내다. 제목 이후 본문을 쓰며, 한 문장이 한도를 넘으면 길이 기록과 함께 어절 경계에서 줄인다. L은 주소만 저장한다.
2. 자연 요청은 카드 봉인 뒤 모집한다. 교정은 고정 자료 안에서 분야별 시험으로 입증 가능한 양성 2건과 적용 층이 다른 반례 1건을 미리 선언한다. 교정과 자연의 최초 사건을 중복시키지 않는다. 기대표의 판독자는 전체 후보·요구를 읽되 세 방식의 카드·순위·표시 창을 보지 않는 파일 경계를 쓴다. 한 작성자의 기억은 차단하기 어려우므로 독립 인력 관찰은 별도로 표시한다.
3. 질의는 요청의 부분·목적·C1·C2·환경 그대로 잇는다. 대소문자·CamelCase·구두점을 정규화한 고유 단어 교집합 수로 초기 점수를 매기고 ID 오름차순으로 동률을 푼다. URL 특징은 blob 뒤의 파일 경로에서 얻고 해시 및 원격 호스트는 점수에서 제외한다. S/E는 각 카드의 이름과 텍스트가 추가된다. 세 방식 모두 동일 20편, 점수, 동률, 최대 원문 3회, 표시 750단어, HTTP 응답 본문 1 MiB를 쓴다. 탐색은 현재 최상위 미열람 후보이며, 읽은 창의 질의어 근거는 순위를 가산한다. 네트워크 또는 예산 실패는 상태를 남기고 다음 열람으로 진행한다. 한도 내 재시도만 허용하며 본 경로의 기본 재시도는 0회다.
4. 원문 표시 위치는 정규화한 연속 소스 창에서 요청 단어가 가장 많이 교차하는 구간이며 줄 번호로 동률을 푼다. 메인 경로는 세 열람을 모두 실행해 첫, 둘째, 셋째 이후 순위를 분리한다. 같은 카드·주소는 요청 중 한 번씩만 표시 비용에 센다. 실제 정답표와는 별개의 창 단위 관찰을 남기고, 무자료·노출 창 없음·개별 판독 누락·판독 후 보류·명시 반박·공동 충족을 구분한다. 채점기 검사는 참, 반박, 범위/판 오채택, 불충분, 미판독, 표시 없음을 입력으로 실험 전 실행한다.
5. 원문 없는 캐시로 각 요청을 실행한 뒤 즉시 재사용 가능한 캐시로 같은 요청들을 실행한다. 순위용 카드/URL 저장과 원문 캐시는 비용상 별도다. HTTP 본문, 원문/카드 디스크 표현, 기계 스캔 및 독자 표시를 따로 센다. 표시 단어는 실제로 제공한 텍스트 분량이며 사람의 읽기 속도·이해를 계측하지 않는다. 연구 재생에는 원문 전체 대신 표시 범위, 네트워크 계수, 고정 원문의 지문을 보관한다.
