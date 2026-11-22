# A-D03–A-D06 후속 판독 결과

| 범위 | 실측 결과 |
|---|---|
| A 참조 | 4개. 목적지를 열기 전 원격 봉인 `168d90b8519bcb4f673acc659bbaae895f79fca5` 확인 |
| 실제 소비자 href 교체 | 1/4: PostgreSQL psql의 RFC4180 링크 |
| 현재 최소 읽기 목적 | 4/4 유지. 이 수치는 역사 전 기간의 정상 작동이나 실제 독자 클릭을 뜻하지 않음 |
| 엄격한 상류 시행→같은 목적 소비자 공개판 지연 | 적격0/1 연결 사건. 3개는 확정된 변경 사건 자체가 없음 |
| 독자 당사자 실패 | 확인0/4. 편집자의 redirect 관측과 독자 실패를 분리 |
| PostgreSQL 실제 판 | 12.2–12.22 전체21판 × 2문서. 원장에 있는 사이 판 누락0 |
| SQLite 실제 판 | 2020–2024 원장51판 중5판 × 2문서. 미검사46판을 `editions.csv`에 명시 |
| 후속 수집의 최소수 산입 | 상류8 고유 원문, 소비자 후속/독립 출판3 고유 원문. 원 A4는 별도 |

## 어느 배포판에서 바뀌었는가

`A-D04`는 PostgreSQL12.18(2024-02-08)의 실제 archive 속 `app-psql.html`까지 `https://tools.ietf.org/html/rfc4180`이다. PostgreSQL12.19(2024-05-09)의 같은 문단은 `https://datatracker.ietf.org/doc/html/rfc4180`이며, 해당 문단의 전후 차이는 href 하나다. 12.2 이후 12.22까지 모든 minor edition의 실제 HTML을 읽었으므로 **이 12계열 안에서는 12.19가 최초 새 주소 판**이라고 한정한다. 다른 major, 웹 배포 시각, 설치된 독자의 도움말 갱신 시각에는 이 표현을 확대하지 않는다. [마지막 옛 배포물](https://ftp.postgresql.org/pub/source/v12.18/postgresql-12.18.tar.bz2) · [첫 새 배포물](https://ftp.postgresql.org/pub/source/v12.19/postgresql-12.19.tar.bz2)

같은12 branch의 [소스 commit bfed705](https://github.com/postgres/postgres/commit/bfed70500289fae9e14f5535d1a1d237ad45d8fd)은 2024-04-10T11:53:25Z다. [편집자의 설명](https://www.postgresql.org/message-id/3C1CEA99-FCED-447D-9858-5A579B4C6687%40yesql.se)은 추가 network roundtrip을 피하려는 것이었다. build와 별도 merge 시각은 미확인이다. [공식12.19 공개 공지](https://www.postgresql.org/about/news/postgresql-163-157-1412-1315-and-1219-released-2858/)의 날짜는2024-05-09다. 메일 표시13:09:17에도 timezone이 없고 raw GET는 일반 HTML로 돌아왔다. 따라서 날짜 빼기29일만 보조량으로 보존하며 **정확한 UTC 경과시간이나 상류→소비자 지연이라고 부르지 않는다**.

`A-D03`의 ANSI 기관 링크는 확인한 PostgreSQL21판에서 유지됐다. `A-D05`의 Endianness 링크와 `A-D06`의 file(1) 링크는 SQLite3.31.0,3.35.0,3.37.2,3.41.0,3.47.2의5판에서 유지됐다. SQLite 미검사46판에 잠깐 다른 링크가 들어갔다가 돌아온 가능성은 남아 있다.

## 처음 결론을 뒤집는 반례

옛 tools 주소는 현재 [RFC-Editor의 RFC4180 본문](https://tools.ietf.org/html/rfc4180)으로 도달하고 필요한 Section2를 읽을 수 있다. **소비자 주소가 바뀐 사실은 독자 목적이 실패했다는 증거가 아니다.** 현재 원 주소 유지 판정과 배포자의 새 주소 선택은 판단 주체와 목적이 다르므로 함께 기록한다.

[RFC7111](https://www.rfc-editor.org/rfc/rfc7111.txt)은 RFC4180을 updates하지만 CSV의 행·열·셀 fragment를 다룬다. 번호가 새롭다는 이유로 CSV quoting 원문을 대신하면 목적이 달라진다. [RFC4180 errata](https://www.rfc-editor.org/errata/rfc4180)의 보고/검증/held 상태에는 서로 다른 날짜가 있으므로 후대 상태를 A의2020 시점에 넣지 않았다.

[IETF2022 공지](https://www.ietf.org/blog/finalizing-ietf-tools-transition/)는 전환 계획이며 후대2026-10-29 편집 표시도 있다. [2021 고정 README](https://github.com/ietf-tools/tools-transition-plan/blob/9cc29af66b4f7548f05126d08a9fd00d55b08360/README.md),2022 고정 README와 비교해 RFC와 draft 서비스 경로를 분리했다. 개별 RFC4180 redirect 시행 시각은 여전히 미확인이므로 시작 미상을 우측 검열로 바꾸지 않았다.

Wikipedia2개는 소비자가 실제 가리킨 목적지의 현재 내용 관측에만 사용했다. 기술 권위 자료가 아니다. 과거 revision ID·시각은 metadata에서 찾았지만 해당 본문 요청은403이었다. file(1) 홈페이지의1987 표시는 현재 페이지의 발행일이나 HTTPS 전환일이 아니다.

## 파일과 재확인

`cases.json`은4참조의 현재 HTTP 최종 응답, 최종 URL, fragment/필요 절, 목적 판정, 소스/출판/독자 시계와 다음 최소 자료를 분리한다. `sources.jsonl`은 직접 읽은 원문·배포 멤버별 위치, 해시, 날짜 역할, 한계와 중복 산입 여부를 남긴다. `pg-editions.jsonl`·`sqlite-editions.jsonl`은 배포물/멤버/관련 바이트의 SHA256 원장을 보존하고 `excerpts/`에는 전후 바이트를 둔다. 대형 archive와 원격 페이지 cache는 커밋 대상에서 제외되며 공식 URL·해시·멤버로 다시 확인할 수 있다.

`editions.csv`는 실제 읽음과 미시도를 구별한다. `intervals.csv`는 엄격0과 달력날짜29일을 분리한다. `attempts.jsonl`에는403·502·raw redirect 등 실패도 남긴다. `check_followup.py`의 실행 영수증은 자기 수집 결과 재검이며 독립 사람 검토나 전체 저장소 gate가 아니다. Git mutation과 공통 파일 수정은 하지 않았다.

| 중요한 미확인 | 마지막 확인 근거 | 다음 첫 자료 |
|---|---|---|
| RFC4180 개별 redirect 시행 시각 | IETF 고정 계획표·전환 완료 문구·PG 편집자 관측 | 해당 경로의 날짜 있는 배포 설정 또는 운영 영수증 |
| 공개 HTML 최초 시각과 독자의 실제 클릭 | 실제 archive HTML·공식 제품 릴리스 공지 | archive hash가 적힌 공개 시각 영수증; 같은 목적 독자 기록 |
| SQLite46개 사이 판·Wikipedia2020 본문 | 원장51판·확인5판·revision metadata | 첫 미검사 sqlite-doc-3310100.zip; 본문 접근 가능한 해당 oldid |
