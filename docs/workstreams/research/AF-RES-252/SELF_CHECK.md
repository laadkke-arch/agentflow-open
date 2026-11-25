# AF-RES-252 자체 점검

## 질문별 근거와 반증

| Q | 원근거와 사용 위치 | 실제 찾은 반례·검사 | 공개 측정에서 남은 확인 |
|---|---|---|---|
| Q1 | S01·S07의 tagged/creation/has_more, S03·S15의 filter, S06·S12·S13, F01·F02의 HTTP·UTC | D01의 같은 ID 재등장과 페이지 사이 변동, D08의 NULL 정렬. 합성 raw 201번째 행이 정규화 120번째를 바꿨고 12 초과 1건과 태그 오류를 검출 | 실제 filter/included_fields/토큰, 첫 120행과 cutoff 동률, 쿼터 미확인 |
| Q2 | S05·S10의 revision 필드와 병합, H01·H03·H04, K01 현행판 L42–98, W05 | K01의 현행 UPDATE·링크와 선행 이력의 판 차이. 합성 #1 전문 우선, 최초 전문이 없는 정상 이력에서만 현행판 사용 | 기계 후보의 수·순번, 최초 공개 revision, #138641의 실제 모집 내 위치 미확인 |
| Q3 | H01의 이전 질의 미봉인, S02의 새 비교 입력, P02의 기법 어휘와 D03 공개 제목 | D03의 DENSE_RANK가 제목에서 남는 실제 구조. 합성 entity·ASCII·반복 위치, 2개 미만, title 변조와 Git 봉인 확인 | 실제 후보 질의 파일과 해법어 포함 후보 수 미확인. 후보의 검색·B 배열을 열기 전 커밋 필요 |
| Q4 | S02의 OR relevance, S04·S09·S14의 raw B 필드 및 optional, S13 익명 page 25 | 합성 첫 raw 5개는 자기와 OR뿐, 6번째가 선택. B 자기 첫 요소 유지. 원글 미반환, details/배열 생략, 빈 배열 상태를 구별하도록 정정. 순서 교란 검출 | 제공자 raw 순서, AND 부분수열, 중복 원배열, 자기/공석 수 미확인 |
| Q5 | S11·S14·S16의 점수·ID·채택 필드, D06·D07·D09·D10, P01 | D07의 질문자는 일자 하나의 답을 보고 복수 일자를 다시 요청했다. 합성에서 가장 오래된 같은 점수 중 작은 answer_id 선택, 채택 ID의 1개 본문, 동일 답의 물리·논리 비용 분리 | 실제 수렴·답 수·채택 상태, 빈 답 또는 선택 본문 미확인. 적합도는 254 판독 |
| Q6 | K01의 현행 배너·inline 링크·UPDATE, S08의 HTML body, S19의 판별 귀속, packet-manifest.json | 합성 origins 4·destinations 2·mapping 행 14가 재파싱 일치. 링크·배너·SQL 마스킹, 표의 열과 도착 SQL 유지, 삭제된 한 행의 해시 재계산도 검출. 보정 글에서 표시 배너를 열람한 사실을 기록 | 실제 세 파일의 행 수·SHA 및 잔여 누출 미확인. `blocked` 상태로 254에 자료를 개방하지 않음 |
| Q7 | C02·C03·C04의 query/filter/cursor, C05·C06의 서로 다른 공개 적용, C07·C08·C09의 서지, F03·F04 | Shannon은 제목·저자가 같아도 두 DOI가 있다. Kuhn의 실제 초판 1962년과 1900 제약을 대조. 두 합성 검색에서 커서, verified 0, 중복 DOI, 빈 items/양수 total과 재배열 검출 | 요청 2건 모두 provider JSON 미수신, 실제 DOI·cursor·정상 0 또는 비공석 미확인 |

## 분모·시점·제외

- 예정 모집 상한 120, 판독 후보 상한 12. 원제공자 JSON 페이지 수신 0, 확인한 실제 모집 수·duplicate 수·후보 수·상한 초과 수 모두 미확인이다. 254의 판독 목표 4건·8경로 중 4 미배정, 8 미실시다. 본표 정상 공석 수 미확인, A/B 답 본문 실측 0개다. #138641은 현행 HTML을 확인한 보정 1건이다. 본표 경로의 일부로 세지 않았다.
- 수집기 정상 진입점에서 공개 GET 시도 4건이며 HTTP CONNECT 403과 curl exit 56을 남겼다. 제공자 HTTP/JSON 미수신, 실제 quota/backoff/has_more 없음. 독립 서지 실험 2건 예정, 수신 0, 결측 2, 정상 0 여부 미확인. F05·F06의 연결 진단은 수집기 네 호출과 별도로 보존했다.
- `sources.jsonl` 75행, 산입 41건/고유 work_id 41/계보 20, 산입 제외 34행. Stack 문서 18, 독립 DBA 보조 10, 보정 1, 방법 근거 4, Crossref 원명세·적용 사례 6, 출판사 원서지 저작 2를 산입했다. Shannon 각 권호는 같은 저작 계보이며 DOI는 두 개다. 231의 구성 파일들은 하나의 선행 저작으로 셌다. 직접 DBA 11건 중 실제 기계 모집은 미확인이다. 공식 실측과 두 서지 REST의 하한이 미달했다.
- 238–242의 입력·출력·정답, 254의 판독 결과는 사용하지 않았다. 선행 231의 질의 작성 단계에는 실제 질의가 없다. 이번 제목식 비교는 별도의 조건이다. source 원장의 UTC 범위 표시는 개별 요청 시간이 보존되지 않은 문서 열람에 한해 사용했다.

## 실행과 구조 대조

- 시작은 `python -m workbench.session start af-res-252 --allow docs/workstreams/research/AF-RES-252/ --dependency work/research-af-res-231=e55fd8c9df7fdd45259346aeb8884a7d3586594b --output docs/workstreams/research/AF-RES-252/session.json --fetch`, exit 0. [고정 manifest](session.json)
- `python -B collect.py frame`, `probe-frame`, `crossref`는 실제 curl 시도 후 각 exit 2. 시점·환경 지문·스크립트 SHA·stdout/stderr 보존. `audit`로 네 건의 curl·CONNECT·provider 결과 필드를 구별했다. 이때의 수집기와 후속 재생 구현을 다른 SHA로 기록했다. [live-execution.json](receipts/live-execution.json)
- 별도 폴더에서 입력을 복사해 실제 실패 아카이브 audit 0, 공개 및 Crossref replay 각 2, 합성 suite 12건 통과를 확인했다. 예상 exit 2와 오류 문구를 함께 대조했고, 그 폴더에 판독 파일이 생기지 않았다. [replay-execution.json](receipts/replay-execution.json)
- 표 1·2는 열 6개·5개와 분모 표기, 마지막 표는 열 4개·약점 3건이다. 254 판독 파일 3개의 수·SHA는 null이다. 한 행짜리 결측 표시를 1건 관측으로 세지 않았다. 공개 원응답을 받은 뒤 실제 개수와 해시로 대조할 파일을 `replay.md`에 명시했다.
- 자체 검토를 수행했다. 별도 독립 검토, 실제 254 판독, SQL 적합성 평가 및 열람 순서의 행동 검증은 미실시다. 고정 결과 커밋에서 다시 읽은 파일과 `workbench.session check --fetch` 및 공통 검사의 실제 범위는 마지막 HANDOFF에 연결한다.
