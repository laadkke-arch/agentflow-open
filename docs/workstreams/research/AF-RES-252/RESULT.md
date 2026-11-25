| 기계 후보·순번 | 원질문 판·질의 토큰 | A 원위치·부분수열 | B 원배열 첫 ID | 선택 답·실제 영수증 | 정상 공석·미확인 |
|---|---|---|---|---|---|
| 모집 실패로 미배정, 상한 12 | 최초·현행판, 후보 제목과 질의 미확인 | 미실시, raw top5·AND 최초 5 미확인 | 미실시, 배열·첫 ID 미확인 | 선택 미실시. 모집 선행 영수증 F01·F02 | 실제 후보 수·정상 공석 수 미확인 |

표 1의 정상 한 행은 시간순 기계 후보 한 건과 두 경로다. 모집 상한은 120 질문과 기계 후보 12건이다. 확인된 모집 API 페이지 0개, 실제 모집·후보 분모 미확인, 본표에 배정한 행 0개다. 표의 한 줄은 결측 상태다. 254의 의미 판독 목표는 최초 적격 4건과 8경로이며 현재 관측 0, 미배정 4, 미실시 8이다.

| 파일·판독 순서 | 의도한 차단 필드 | 실제 행 수·SHA-256 | 재파싱 대조 | 누출·판독 가능 조건 |
|---|---|---|---|---|
| 0. [packet-manifest.json](packet-manifest.json) | 후보 ID, 답, 경로, seed | 파일 명세 3개, 각 실제 레코드 수와 SHA는 null. manifest 자체 SHA `d41899ceaebd7c49a6f7ad3de42d05d57b8411eb6c9e6a7839f5024ea52cb6d2` | JSON 파싱 및 차단 상태 확인 | `blocked`. 254 개방 보류 |
| 1. `reader/origins.jsonl` | 출처 ID, 링크, 경로·답·SQL 직접 단서 | 미생성, 실제 행 수와 SHA 미확인 | 공개 원응답 필요 | 원문 데이터·문체·해법 언급이 남을 수 있음 |
| 2. `reader/destinations.jsonl` | A/B, 후보 대응, 공개 ID·답 채택/득표 | 미생성, 실제 행 수와 SHA 미확인 | 공개 원응답 필요 | 답 SQL은 판독 근거. 익명 라벨과 도착 순서가 필요 |
| 3. `mapping.json` | 1·2를 판독하는 동안 모든 연결 | 미생성, 실제 행 수와 SHA 미확인 | 공개 원응답 및 봉인된 질의 필요 | 판독 기록을 고정한 뒤 열 파일 |

표 2의 한 행은 파일 한 개다. 판독 파일 3개 중 원응답으로 생성한 파일 0개다. `mapping.json` 레코드 수는 생성 시 origins·routes·destinations 세 배열의 행 수 합이다.

## Q1. 실제 필터와 모집창

공식 `/questions`의 AND와 creation 정렬 계약(L3–19)에 맞춰 모집 필터의 wrapper·질문 필드를 지정했다. F01은 `/filters/create`의 CONNECT 403으로 curl 56, 원제공자 HTTP 및 본문 미수신, filter/included_fields/quota/backoff/has_more는 미확인이다. F02는 `filter=default`로 보낸 같은 창의 연결 진단이며 CONNECT 403이다. 이 진단은 맞춤 필터가 확인된 모집에서 제외한다. 모집 120번째 생성 초와 동률 전체를 확인하지 못했다. [S01 /questions](https://api.stackexchange.com/docs/questions) · [S15 filter](https://api.stackexchange.com/docs/types/filter) · [F01](receipts/filter-frame.1.meta.json) · [F02](receipts/frame-default-diagnostic.1.meta.json)

## Q2. 기계 후보와 최초 공개판

실제 기계 후보는 배정할 수 없었다. 검증된 모집에서 두 태그·생성 초·ID와 현재 duplicate 상태를 읽은 뒤 첫 12건을 정한다. 공개 최초 revision의 번호·게시 초·전문을 확인하고, 정상 이력 종료 후 전문이 빠졌을 때의 현행판 사용과 이력 미수신을 가른다. 보정 #138641의 현행 HTML에는 두 태그, duplicate 배너, 이후 UPDATE의 SQL·링크가 표시된다. 수정 이력은 웹 접근 실패다. 이 보정 사건의 실제 모집 위치, 최초 전문, 공식 B 배열은 미확인이다. [S05 revisions](https://api.stackexchange.com/docs/revisions-by-ids) · [S10 revision type](https://api.stackexchange.com/docs/types/revision) · [K01 #138641](https://dba.stackexchange.com/questions/138641/efficiently-get-records-with-latest-timestamp-per-group?noredirect=1)

## Q3. 제목식 질의

토큰화·불용어·보존 및 제외 위치를 코드로 고정했다. 231은 작업자 생성 2–4단어를 커밋하지 못했고, 이번 제목식 A는 새 비교 조건이다. 실제 `queries.csv`는 후보 원문 미확인으로 아직 봉인하지 못했다. DBA 보조 D03의 TITLE에 `DENSE_RANK`가 있고 문서 P02에서 함수 의미를 확인했다. 제목에서 기법 표현은 검색 토큰으로 보존될 수 있으며 가림 판독에는 별도 마스킹을 적용한다. [H01 231 인계](https://github.com/laadkke-arch/agentflow-open/blob/e55fd8c9df7fdd45259346aeb8884a7d3586594b/docs/workstreams/research/AF-RES-231/HANDOFF.md) · [D03](https://dba.stackexchange.com/questions/287606/dense-rank-not-working-as-expected) · [P02](https://www.postgresql.org/docs/16/functions-window.html)

## Q4. A/B 도착 배열

A의 현재 순서는 제공자 OR 검색에서만 가져온다. raw 상위 5개와 두 태그 AND 부분수열의 최초 5개, 첫 비자기 후보를 각각 기록한다. 5개 확보까지 추가 페이지가 필요할 수 있고, 익명 page 25에서 잘리면 미확인으로 기록한다. B는 `original_questions` 원배열의 첫 ID를 쓴다. 정상 응답의 자기 첫 요소, 질문 미반환, `closed_details` 생략, 배열 필드 생략, 빈 배열을 별도 공석으로 표시한다. 선봉인 입력이 없어 두 배열을 요청하지 않았다. 합성 A에서 자기 제외 후 raw 위치 6의 후보를 복원했고, B에서 첫 요소가 자기여도 다음 요소로 이동하지 않는 동작을 확인했다. [S02 /search/advanced](https://api.stackexchange.com/docs/advanced-search) · [S04 closed_details](https://api.stackexchange.com/docs/types/closed-details) · [S13 익명 한도](https://api.stackexchange.com/docs) · [재생](replay.md)

## Q5. 질문당 한 답과 예산

질문이 반환한 채택 답 ID로 본문 하나를 읽고, ID가 없으면 모든 답 메타를 얻어 score 내림·creation_date와 answer_id 오름으로 배열한 후 첫 본문 하나를 읽도록 구현했다. 실제 도착 질문·답·메타 GET은 0건 실행했다. 질문/답 본문을 물리적으로 재사용해도 보존한 각 경로의 논리적 1+1 열람량을 따로 잰다. 실제 수렴, 정상 빈 도착, 채택 상태는 미확인이다. D07의 게시자는 한 날짜의 답을 읽고 질문에 있던 복수 기준일을 다시 명시했다. 이는 순위나 채택 필드와 원요구가 따로 기록되어야 하는 보조 사례다. [S11 답 목록](https://api.stackexchange.com/docs/answers-on-questions) · [S16 answer](https://api.stackexchange.com/docs/types/answer) · [D07](https://dba.stackexchange.com/questions/214865/mysql-5-6-27-how-to-get-latest-pairs-for-different-points-in-time-in-a-single-q/214879)

## Q6. 판독 가능성

실제 패킷은 차단 상태다. 코드의 판독판은 질문·답·저작권 귀속의 메타데이터를 별도 대응표로 옮기고 duplicate 배너와 게시물 링크를 제거한다. 원질문의 SQL 코드 단서와 제목의 명시 해법어를 마스킹한다. 요구를 재구성해야 하므로 일반 표현·예시 데이터·표의 구조는 남는다. 본문·그림을 통해 알아본 출처, 문체로 추정한 저자, 남은 해결 접근은 가림 한계다. #138641의 UPDATE·답 링크는 원본과 판독판의 노출 차이를 보여 준다. 이 작업자는 보정 HTML을 열어 배너를 보았다. 합성 판독판 4·2·14 레코드의 재파싱, 해시, 링크 제거와 표 열 보존을 확인했다. 254는 실제 봉인과 파일 해시 검산이 끝나면 지정 순서로 연다. [K01 #138641](https://dba.stackexchange.com/questions/138641/efficiently-get-records-with-latest-timestamp-per-group?noredirect=1) · [S19 각 revision 라이선스](https://stackoverflow.com/help/licensing) · [재생](replay.md)

## Q7. Crossref와 페이지 분류

서지 실험은 Shannon 제목의 relevance와 Kuhn 제목에 1900-01-01 단일 날짜를 적용한 조건이다. 둘 모두 첫 cursor GET이 CONNECT 403이었다. 원응답·DOI 순서·next-cursor와 정상 0 여부는 미확인이다. 공식 문서는 cursor 시작 `*`, 이후 `next-cursor`, `len(items)<rows` 정지를 정의한다. `rows=0`의 빈 items는 total-results와 별도로 확인해야 한다. Wiley에서 같은 Shannon 제목·저자의 서로 다른 두 DOI를, Chicago Press에서 Kuhn 초판 1962년과 4판 2012년을 직접 열었다. 제목만으로 두 DOI를 하나로 합치면 서로 다른 권호를 잃는다. 합성 입력은 정상 0, 다음 커서가 있어도 끝나는 페이지, 중복 DOI, 레코드 순서 변조를 검출했다. [C02 Crossref tips](https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-the-crossref-rest-api/) · [F03](receipts/crossref-shannon-p1.1.meta.json) · [F04](receipts/crossref-kuhn-1900-p1.1.meta.json) · [C07 Shannon 7월](https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1948.tb01338.x) · [C08 Shannon 10월](https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1948.tb00917.x) · [C09 Kuhn](https://press.uchicago.edu/ucp/books/book/chicago/S/bo13179781) · [재생](replay.md)

## 비용과 대안

- `collect.py` Cloud GET 시도 4건에서 제공자 본문을 받은 연결은 0건이다. 제공자 호출 차감 수는 미확인이다. 착수 시 단순 연결 시도 F05·F06은 별도로 집계했다. 정상 frame은 페이지와 경계에서 비용이 들고 A는 후보당 최대 25 metadata 페이지가 필요할 수 있다. 실제 답 본문 예산과 메타데이터 비용은 별개다. [Cloud 실행 기록](receipts/live-execution.json)
- 열람 원장은 75행, 산입 고유 원자료 41건, 그 계보 20개다. 공식 SE 자료 18, DBA 보조 10과 보정 1, 제작자 규격·선행 인계·라이선스 4, Crossref 공식·저자 사례 6, 출판사 제목 계보 2를 산입했다. DBA 직접 열람 11건 가운데 본표 0, 보정 1, 보조 10이다. Crossref 실시간 실험 관측 0/2와 결측 2는 따로 센다. [sources.jsonl](sources.jsonl)
- Crossref 두 연구에서 동일한 제목이나 가장 높은 검색 순위만으로 서지 동일성을 고정하기 어렵다. Grobid는 응답을 TEI로 재구성하고, Tkaczyk는 후보 검증을 검색 점수와 따로 비교했다. 254의 의미 판독을 위한 대응표를 분리하는 이유를 보여 주되 해당 일치 알고리즘을 이 실험의 순위 대용으로 쓰지 않았다. [C05 연구](https://www.crossref.org/blog/what-if-i-told-you-that-bibliographic-references-can-be-structured/) · [C06 Grobid](https://www.crossref.org/blog/how-grobid-uses-crossref-metadata-to-enrich-bibliographic-information/)
- 결과는 PARTIAL이다. 같은 공개 API URL에서 필터 토큰을 받은 뒤 모집과 판독 패킷을 이어갈 수 있다. GitHub에는 직접 열람 자료, 연결 실패 영수증, 독립 폴더에서 실행한 자체 재생과 합성 검사 12개를 저장했다. 별도 독립 검토는 미실시다. [재생 실행 기록](receipts/replay-execution.json) · [자체 점검](SELF_CHECK.md)

| 중요한 불일치 또는 약점 | 영향을 받는 판단 | 다음에 볼 구체적 원자료·검사 | 판정이 바뀌는 관측 |
|---|---|---|---|
| CONNECT 403으로 filter·frame 미수신 | Q1–Q4, Q6, 실제 후보 분모와 254 개방 | 허용된 네트워크에서 F01 성공 후 두 태그 AND 실제 `/questions` 페이지 및 120 경계 확인 | 토큰·필드와 정상 페이지 수신, cutoff에서 다른 ID 또는 정상 0까지 검증 |
| 공개 최초 내용의 누락·후편집 해법·자기/공유 후보의 가능성 | Q2–Q6, 질의의 입력판, 공석과 한 건 예산 | 후보별 revision·봉인 질의·raw A/B 배열·선택 답 GET을 다시 파싱 | 실제 제목 토큰이 바뀌거나, 정상 빈/자기 첫 요소/공유 답이 크로스체크됨 |
| Crossref 두 REST cursor가 미수신되고 출판사 제목과 DOI는 다대일 가능 | Q7 실제 순서·0·중복, 오프라인 검산 일반화 | F03/F04의 첫 정상 JSON, Shannon의 다음 cursor, Kuhn 총수와 items | 정상 0이거나 데이터 결함·다른 저작이 매치됨. 같은 제목의 두 DOI가 다른 행이면 별도 유지 |
