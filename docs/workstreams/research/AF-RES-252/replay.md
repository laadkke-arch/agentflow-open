# 원응답 재생과 반례

## 현재 공개 영수증 재생

`filter-frame.1`, `frame-default-diagnostic.1`, `crossref-shannon-p1.1`, `crossref-kuhn-1900-p1.1`은 각 정확한 URL, 수신 구간, curl exit 56, CONNECT 403, 제공자 HTTP 코드 000, 본문과 SHA null을 남긴다. 이 아카이브에서는 네 JSON 메타데이터만 읽힌다. 요청 정책과 오류를 원인·단계별로 구분해서 기록한다.

```bash
P=docs/workstreams/research/AF-RES-252
python -B "$P/collect.py" audit
python -B "$P/collect.py" replay-crossref
python -B "$P/collect.py" replay --seal 980ab5c07176b486350a10d3f2cbb7416480e0b9
python -B "$P/test_replay.py"
```

원본 archive의 audit는 네 건을 `proxy_connect_failed`로 재분류해 exit 0이다. replay-crossref는 같은 결측 요약을 재파싱하고 실측 미완료 exit 2를 반환한다. replay는 최초 필터에서 exit 2로 중단한다. 위 SHA는 사전 범위판이다. 실제 제목 봉인판이 확인되면 그 SHA로 바꾼다. 별도 폴더 실행의 입력 SHA, 정상 stdout/stderr, exit와 소요 구간은 [replay-execution.json](receipts/replay-execution.json)에 있다.

## 검산이 다루는 반례

| 통제 | 관측한 원자료 또는 합성 입력 | 확인된 검사 결과와 한계 |
|---|---|---|
| 페이지 경계와 중복 | DBA D01에서 ID 99 재등장 보고. 유일 정렬을 써도 삽입·삭제가 페이지를 움직인다는 다른 답. D08은 NULL 순서에서 ID 2 재등장을 보고 | 합성 202행·3페이지에서 raw 201번째의 작은 ID가 정규화 120번째가 됐다. 후보 상한 12와 초과 1, 태그 누출 검출. 실제 API 전체가 한 시각의 스냅샷인지 확인은 별개 |
| 후보의 제목 단서·입력판 | D03의 공개 제목과 분할/정렬 혼동, K01의 현행 UPDATE와 중복 링크 | 합성 #1 원본 우선, 초기 전문 없는 현행판, 2개 미만 공석, 해법어 보존, 봉인 이후 원제목 변경 검출. 실제 처음 판과 가림 잔여 단서는 후보별 검증 필요 |
| 자기·공유·정상 공석 | A 자기+OR 4건 다음의 raw 6번째 AND, B의 자기 우선과 다음 외부 ID, B 배열 없음과 빈 배열 | A/B 같은 답 1쌍, 실제 본문 호출을 흉내 낸 고유 질문·답 각 2건과 논리 열람 각 3건. B에서 두 번째를 택하지 않았다. 두 태그 부분수열과 원위치가 유지됐다 |
| 답 선택 규칙 | 동일 score 3건 중 생성 초·ID 역순. 다른 도착지는 별도 채택 답 | 합성 no-accepted에서 9199, accepted에서 9750 선택. 9750의 목록 미수집과 답 본문 하나 확인. PostgreSQL·DBA 보조 글의 답 적합도는 범위 밖 |
| 빈 응답·쿼터·재개 | 합성 정상 빈 wrapper, 429, API 오류 객체, DNS/CONNECT, 전송 중단, quota=0 및 메서드별 backoff | 실제 결측/손상과 정상 0을 구분했다. 합성 archive 재시작 뒤 quota=0에서 모든 SE 새 호출 중지, 메서드 backoff와 다른 메서드의 허용 간격 분리 |
| 가림과 한 레코드 손실 | 양성 가림 패킷 4 origin·2 destination·대응표 논리 행 14. A OR 페이지에서 한 행 삭제, B 배열만 뒤집고 매번 원영수증 SHA 재계산 | 삭제와 재배열 모두 보존된 패킷의 재생에서 거부됐다. 배너·답 링크·origin SQL 단서를 가렸고 예제 표의 열 구분과 destination SQL은 보존했다. 문장·테이블 값으로 원글 역검색 가능 |
| Crossref 서지 순서와 키 | 두 합성 GET의 next-cursor, 두 번째 페이지의 대소문자 DOI 반복, 0건에서 next-cursor 존재, 첫 페이지 빈 items와 양수 total | cursor 전달, 원순서, 케이스폴딩 키 중복, 진짜 0의 중단, 양수 total과의 구별을 검산했다. 첫 페이지를 뒤집고 새 해시를 넣어도 보존한 서지 재생이 다른 배열을 검출했다 |

D01/D08은 SQL 정렬의 경험적 반례이고 API 호출 결과는 아니다. Q1의 페이지 경계 검사는 최초 120개가 바뀌는 관측에 민감하다. 전체의 가능한 누락은 snapshot 또는 장기 변동을 확인할 정보가 필요하다. PostgreSQL SELECT의 LIMIT과 DISTINCT 기준 및 Crossref의 재색인 경고를 함께 확인했다. [D01](https://dba.stackexchange.com/questions/123737/same-record-shows-up-multiple-times-in-ordered-paginated-query) · [D08](https://dba.stackexchange.com/questions/331837/duplicate-results-in-mysql-query-when-try-to-sort-on-null-field-by-with-limit-an) · [P01](https://www.postgresql.org/docs/16/sql-select.html) · [C02](https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-the-crossref-rest-api/)

Shannon과 Kuhn은 이 호출에서 조회를 시도한 정확한 제목이다. Shannon을 같은 이름의 중복 행으로 지우면 실제 두 권호·DOI를 잃을 수 있다. Kuhn의 1900 조건은 출판사 원서지의 초판 연도보다 이르다. 유사 검색이나 기탁 데이터 오류로 양수 결과가 나오면 DOI·published/issued를 다시 확인한다. cursor가 있어도 두 번째 페이지가 빈 상태일 수 있고, rows=0은 카운트 요청이다. 직접 읽은 C05의 후보 검증 실험과 C06의 TEI 내보내기는 서지 일치의 다른 증거를 보여준다. [C02](https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-the-crossref-rest-api/) · [C05](https://www.crossref.org/blog/what-if-i-told-you-that-bibliographic-references-can-be-structured/) · [C06](https://www.crossref.org/blog/how-grobid-uses-crossref-metadata-to-enrich-bibliographic-information/) · [C09](https://press.uchicago.edu/ucp/books/book/chicago/S/bo13179781)

## 허용된 네트워크에서 다시 실행할 순서

브랜치와 결과판을 먼저 일치시킨다. 다음 명령은 Python 3.12, curl, Git으로 실행한다. 실제 필터를 얻은 뒤에만 같은 토큰으로 정식 frame을 요청한다. 명령은 한 출력 폴더에서 차례대로 실행하며, 성공적으로 받은 URL은 파일을 검증해 재사용한다. 실패 영수증은 덮어쓰지 않는다.

```bash
git clone --single-branch --branch work/research-af-res-252 https://github.com/laadkke-arch/agentflow-open.git agentflow-af252-restart
cd agentflow-af252-restart
git rev-parse HEAD
P=docs/workstreams/research/AF-RES-252
python -B "$P/collect.py" frame --retry-failed
python -B "$P/collect.py" origins --retry-failed
python -B "$P/collect.py" audit
```

`frame` 입력은 site=dba, 두 tagged AND, epoch 1325376000–1735689599, creation asc, pagesize=100이다. 피드에서 받은 filter의 included_fields와 wrapper를 확인한다. `origins`에서 실제 원질문과 이력을 얻으면 frame·queries·영수증을 먼저 커밋하고, 그 전체 SHA를 아래 `SEAL`에 넣는다. 성공 영수증은 원 HTTP entity 그대로 보관하며 curl이 압축을 해제한 뒤의 바이트를 해싱한다. 공개 응답에서 쿠키·프로세스 비밀값·내부 헤더는 수집하지 않는다. 수집한 게시물의 실제 content_license·공개 출처는 대응표에서 확인한다.

```bash
git add -- "$P/frame.csv" "$P/frame-stats.json" "$P/queries.csv" "$P/receipts"
git commit -m 'Seal AF-RES-252 actual origin titles before A and B'
SEAL=$(git rev-parse HEAD)
python -B "$P/collect.py" routes --seal "$SEAL" --retry-failed
python -B "$P/collect.py" replay --seal "$SEAL"
python -B "$P/collect.py" crossref --retry-failed
python -B "$P/collect.py" replay-crossref
```

Crossref 실험은 별개다. 양쪽 `cursor=*`, `rows=2`, `sort=score&order=desc`에서 시작한다. `query.bibliographic`에 `A Mathematical Theory of Communication`과 `The Structure of Scientific Revolutions`를 각각 넣고, 두 번째는 `filter=from-pub-date:1900-01-01,until-pub-date:1900-01-01`을 붙인다. 첫 페이지에 2건이 있으면 응답의 next-cursor를 그대로 두 번째 URL에 쓴 뒤 정지한다. 같은 조건이 오류나 throttle을 내면 영수증의 재개 시각·요청 식별자를 사용한다. Stack Exchange의 quota=0 영수증 이후 코드는 최대 24시간 보수적으로 wait를 표시한다. 이 시간은 코드의 재시도 경계다.

`#138641`은 `python -B "$P/collect.py" calibration-origin --retry-failed`로 따로 준비하고 `calibration-query.csv`와 영수증을 커밋한다. `python -B "$P/collect.py" calibration-routes --seal <보정_봉인_SHA> --retry-failed`의 대응은 `receipts/calibration-routes.json`에만 남긴다. 본표와 겹치는 경우 원영수증을 재사용한다.

`packet-manifest.json`이 ready일 때만 254가 origins → destinations → mapping 순서로 연다. 실제 판에서 표와 원장·manifest를 다시 갱신하고 공개 본문만 해당 라이선스로 보존한다. 현재 blocked 단계에서는 실제 본문, 모집·질의 CSV와 대응표 해시가 미확인이다.
