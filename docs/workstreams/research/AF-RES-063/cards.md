# 사례 카드

원 공개 기록의 현재 열람판을 기준으로 썼다. `publication_utc`는 실행시각이 아니다. 원문·판·시각·역할은 [sources.jsonl](sources.jsonl), 입력·로드·출력 분리는 [receipts.csv](receipts.csv)를 따른다. 연구자의 신규 날짜변환 재실행은 전 사례에서 **미실시**다.

## 자연 6자리

### N-P1

- 원기록: [pandas-38928-body](https://github.com/pandas-dev/pandas/issues/38928); 2021-01-03T19:08:29Z; nabelekt (author report).
- 공개 관측: 2020-10-19 18:58:20; 2020-10-19 16:45:33; UnknownTimezoneWarning (O-R (author reported calendar output + warning)). naive 날짜 두 개와 경고가 실제라고 게시됨. EDT 의미를 특정 지역·UTC로 보정하지 않는다.
- 같은 실행 입력/지역: 2020-10-19 18:58:20 EDT; 2020-10-19 16:45:33 EDT; EDT abbreviation; IANA ID 미확인; `pd.to_datetime(df['datetime']) after pd.read_csv(test.csv, delimiter=';')`. UTC: 미확인; EDT abbreviation without IANA region or explicit numeric offset.
- 로드 연결: dateutil parser path in same reported stderr; 미확인; unknown-zone warning path returns naive and does not establish a tzdb lookup. 설치/lock: 미확인. 연결키: issue38928 body test.py/Running python test.py block; no run ID/PID.
- 보조 재현: 원 댓글·공식 코드의 독립 설명은 해당 원저자 실행과 구별한다. 현재 연구자의 실행은 미실시. 고정 코드·배포파일 읽기는 실행 재현이 아니다.
- 환경 미상일 때 답: 이 작성자가 위 결과를 보고한 사실까지만 말하며 실제 자료판은 미확인이다. 원본문 최초판도 미확인이다.
- 판을 가를 첫 추가 **보관 원자료**: 동일 실행의 dateutil.__version__/module path, time.tzname, 명시적 지역·numeric offset 또는 당시 원 입력의 의미; 원 tzdb lookup이 없었다면 tzdb판 요구는 해당 없음.
- 상세·한계: [evidence/pandas/receipts.json](evidence/pandas/receipts.json); source `S-P38928`.

### N-P2

- 원기록: [pandas-39398-body](https://github.com/pandas-dev/pandas/issues/39398); 2021-01-25T15:18:39Z; rwijtvliet (author report).
- 공개 관측: printed i2 contains 2020-03-30 01:00:00+02:00; first i2 value is 2020-03-29 00:00:00+01:00 while first i is 2020-03-27 00:00:00+01:00 (O-R; printed calendar values exist, exact stated call/output binding fails internal consistency). 인쇄된 값은 존재하지만 명시한 +1 Day와 첫 출력의 +2일 차이가 충돌한다. 전체 호출·출력에 양립하는 판집합은 미확인이다. Berlin offset 구성요소만 여러 판에 공통이다.
- 같은 실행 입력/지역: date_range 2020-03-27, freq D, periods 4, Europe/Berlin; Europe/Berlin; `i=pd.date_range('2020-03-27',freq='D',periods=4,tz='Europe/Berlin'); i2=i+i.freq`. UTC: i first displayed item = 2020-03-26T23:00:00Z; displayed four local midnights map to 03-26T23Z,03-27T23Z,03-28T23Z,03-29T22Z (arithmetic inference from printed offsets).
- 로드 연결: pytz inferred conditionally from declared code; historical actual path 미확인; 2020e is the official pytz 2020.5 label, not confirmed historical loaded edition. 설치/lock: 미확인; public matching source/distribution is not user install receipt. 연결키: issue39398 body, no cell execution counters/PID; show_versions in separate block.
- 보조 재현: 원 댓글·공식 코드의 독립 설명은 해당 원저자 실행과 구별한다. 현재 연구자의 실행은 미실시. 고정 코드·배포파일 읽기는 실행 재현이 아니다.
- 환경 미상일 때 답: 이 작성자가 위 결과를 보고한 사실까지만 말하며 실제 자료판은 미확인이다. 원본문 최초판도 미확인이다.
- 판을 가를 첫 추가 **보관 원자료**: 원 REPL/노트북의 실행 순번·전체 i/i2 상태와 같은 프로세스의 열린 Berlin 멤버·PYTZ_TZDATADIR. Berlin 멤버만으로 2020a/e가 갈리지 않으므로 전체 배포 지문 또는 동일 실행 Volgograd 2021-01-01T00Z 관측도 필요.
- 상세·한계: [evidence/pandas/receipts.json](evidence/pandas/receipts.json); source `S-P39398`.

### N-P3

- 원기록: [pandas-40336-body](https://github.com/pandas-dev/pandas/issues/40336); 2021-03-09T20:48:39Z; teddyward (author report).
- 공개 관측: TypeError: Start and end cannot both be tz-aware with different timezones (O-R exception only; Expected Output is separate successful-looking hourly call with freq H). 실제는 예외. expected hourly 배열은 입력·freq가 다른 호출이다. 11월 traceback도 원 body와 별도 사건이다.
- 같은 실행 입력/지역: 2020-03-09 00:00:00-07:00; 2021-03-09 00:00:00-08:00; America/Los_Angeles passed separately; endpoint parsers carry different fixed offsets; `pd.date_range('2020-03-09 00:00:00-07:00','2021-03-09 00:00:00-08:00',tz='America/Los_Angeles')`. UTC: 2020-03-09T07:00:00Z to 2021-03-09T08:00:00Z (arithmetic from explicit -07/-08).
- 로드 연결: body historical data provider 미확인; later comment fixed-offset parser evidence kept separate; 미확인; official pytz 2020.1 label 2020a is a candidate environment association. 설치/lock: 미확인. 연결키: issue40336 body failing-call block. Expected Output changes both input representation and freq; November comment is new event.
- 보조 재현: 원 댓글·공식 코드의 독립 설명은 해당 원저자 실행과 구별한다. 현재 연구자의 실행은 미실시. 고정 코드·배포파일 읽기는 실행 재현이 아니다.
- 환경 미상일 때 답: 이 작성자가 위 결과를 보고한 사실까지만 말하며 실제 자료판은 미확인이다. 원본문 최초판도 미확인이다.
- 판을 가를 첫 추가 **보관 원자료**: 원 실패 run의 traceback와 endpoint tzinfo 타입/실행 ID. 성공 날짜 값이 필요한 경우 그 호출 자체의 보관 출력이 필요하며, expected 표로 대체할 수 없다.
- 상세·한계: [evidence/pandas/receipts.json](evidence/pandas/receipts.json); source `S-P40336`.

### N-M1

- 원기록: [moment/moment-timezone#922:body](https://github.com/moment/moment-timezone/issues/922); 2021-01-08T08:14:19Z; lucapu88 / original reporter.
- 공개 관측: 2021-01-08T09:00:00+01:00 (O-R). 08:00+01은 기대값이고09:00+01이 보고값. 가능한 UTC07Z/08Z는 각각 의도/출력 해석의 연구자 산술이다.
- 같은 실행 입력/지역: 2021-1-8 08:00; Europe/Rome; `moment.tz(dateStartFormat, "Europe/Rome").format()`. UTC: 출력의 +01:00을 믿으면 2021-01-08T08:00:00Z; 의도한 현지 08:00+01:00이면 07:00Z. 원 파싱 경로는 미확인..
- 로드 연결: Moment Timezone API를 호출했다고 보고; native parser/host와 dataVersion 미확인; 미확인. 설치/lock: 미확인. 연결키: moment/moment-timezone#922:body.
- 보조 재현: 원 댓글·공식 코드의 독립 설명은 해당 원저자 실행과 구별한다. 현재 연구자의 실행은 미실시. 고정 코드·배포파일 읽기는 실행 재현이 아니다.
- 환경 미상일 때 답: 이 작성자가 위 결과를 보고한 사실까지만 말하며 실제 자료판은 미확인이다. 원본문 최초판도 미확인이다.
- 판을 가를 첫 추가 **보관 원자료**: 같은 원 입력의 explicit-format/UTC 해석, moment.version·tz.version·tz.dataVersion·정확 번들 URL/멤버 지문·결과를 동일 셀에 보존
- 상세·한계: [evidence/moment/receipts.json](evidence/moment/receipts.json); source `M-ISSUE-922`.

### N-M2

- 원기록: [moment/moment-timezone#925:body](https://github.com/moment/moment-timezone/issues/925); 2021-01-23T05:46:36Z; skang / original reporter.
- 공개 관측: 첫 입력:2021-01-22 19:02; 둘째:2021-01-23 00:02 (O-R). 한 자리 hour와 두 자리 hour 두 결과는 같은 보고에 있지만 guess 반환·원 UTC가 없다. 명시 format 해결은 자료판 교체 사건이 아니다.
- 같은 실행 입력/지역: 2021-01-23 0:02; 2021-01-23 00:02; 미확인; `moment.tz(input, moment.tz.guess()).format("YYYY-MM-DD HH:mm")`. UTC: -05 지역에서 첫 문자열을 UTC로 읽으면 2021-01-23T00:02Z→전날19:02와 양립. 두 번째를 현지로 읽으면05:02Z 가능. 추정이며 지역/UTC는 미확인..
- 로드 연결: Moment Timezone API라고 보고; guess의 실제 반환과 JS parser 환경 미확인; 미확인. 설치/lock: 미확인. 연결키: moment/moment-timezone#925:body.
- 보조 재현: 원 댓글·공식 코드의 독립 설명은 해당 원저자 실행과 구별한다. 현재 연구자의 실행은 미실시. 고정 코드·배포파일 읽기는 실행 재현이 아니다.
- 환경 미상일 때 답: 이 작성자가 위 결과를 보고한 사실까지만 말하며 실제 자료판은 미확인이다. 원본문 최초판도 미확인이다.
- 판을 가를 첫 추가 **보관 원자료**: guess() 결과, 두 입력의 valueOf/toISOString, 명시 YYYY-MM-DD H:mm, core/tz/dataVersion를 같은 실행에서 기록
- 상세·한계: [evidence/moment/receipts.json](evidence/moment/receipts.json); source `M-ISSUE-925`.

### N-M3

- 원기록: [moment/moment-timezone#926:body](https://github.com/moment/moment-timezone/issues/926); 2021-02-05T08:24:08Z; joemarieandres / original reporter.
- 공개 관측: offset 표기만 나온다는 정성 보고; 실제 offset 숫자 없음 (O-R). format z의 정성 관측으로 사전 기준에 적격. PST는 기대 약칭이며 지역ID나 실제 numeric offset이 아니다.
- 같은 실행 입력/지역: format("z")만 게시; date/zone 미기재; 미확인; `format("z")`. UTC: 미확인.
- 로드 연결: 미확인; moment 생성/zone 부착 호출 없음; 미확인. 설치/lock: 미확인. 연결키: moment/moment-timezone#926:body.
- 보조 재현: 원 댓글·공식 코드의 독립 설명은 해당 원저자 실행과 구별한다. 현재 연구자의 실행은 미실시. 고정 코드·배포파일 읽기는 실행 재현이 아니다.
- 환경 미상일 때 답: 이 작성자가 위 결과를 보고한 사실까지만 말하며 실제 자료판은 미확인이다. 원본문 최초판도 미확인이다.
- 판을 가를 첫 추가 **보관 원자료**: 원 zone ID·UTC/valueOf·정확 z/Z 출력과 provider/dataVersion. PST를 지역 ID로 임의 대체하지 않는다
- 상세·한계: [evidence/moment/receipts.json](evidence/moment/receipts.json); source `M-ISSUE-926`.

## 실행물 우선 4자리

| 자리 | 공개 관측·실행 결손 | 보조 재현·환경 미상 답 | 첫 추가 보관 원자료 |
| --- | --- | --- | --- |
| E-P1 | Fixed15 candidates have no preserved date output | 현재 실행 미실시. 당시 날짜 출력·자료판은 미확인. 다른 노트북은 대체하지 않음 | Recover stdout/artifact for frozen C1..C15; [evidence/artifacts/receipts.json](evidence/artifacts/receipts.json) |
| E-P2 | Fixed15 candidates have no preserved date output | 현재 실행 미실시. 당시 날짜 출력·자료판은 미확인. 다른 노트북은 대체하지 않음 | Recover stdout/artifact for frozen C1..C15; [evidence/artifacts/receipts.json](evidence/artifacts/receipts.json) |
| E-M1 | No qualifying original metadata found within official Actions/Travis/notebook route; unknown historical total | 현재 실행 미실시. 당시 날짜 출력·자료판은 미확인. 다른 노트북은 대체하지 않음 | Find dated original author run/notebook list from the recorded official route; [evidence/artifacts/receipts.json](evidence/artifacts/receipts.json) |
| E-M2 | No qualifying original metadata found within official Actions/Travis/notebook route; unknown historical total | 현재 실행 미실시. 당시 날짜 출력·자료판은 미확인. 다른 노트북은 대체하지 않음 | Find dated original author run/notebook list from the recorded official route; [evidence/artifacts/receipts.json](evidence/artifacts/receipts.json) |

## 통계·학술 사례 — 별도 두 행

| 사례 | 공개 관측·입력/판 증거 | 실행 연결과 환경 미상 답 | 첫 추가 관측·한계 |
| --- | --- | --- | --- |
| X-D1 | [XAMFQK](https://doi.org/10.7910/DVN/XAMFQK)의 월199210와 저자 숫자; 두 XLSX의 deposit MD5 일치; V1/V2의 U_Data 멤버 동일 | 저자가 출판한 숫자 자료는 확인. 실제 논문 분석이 읽은 파일판은 미확인;61파일에 실행 코드/로그 없음 | 원 분석log+실제 입력hash+dataset manifest. VINTAGE는 사전종류이고 날짜 아님. [독해](evidence/crossfield/READING.md) |
| X-Z1 | [Zenodo6532252](https://zenodo.org/records/6532252)의 scenario1/seed1/FIFO/4workers raw200행, 첫 duration9378.21µs; ZIP MD5 일치 | 원저자 발행 계산 결과는 확인.24노트북 output0; 논문 표 계산과 실제 read입력 연결은 미확인 | 같은 분석run의 입력digest·실행셀 결과·timestamp. 관측월 해당 없음; 연구자 재실행 미실시. [독해](evidence/crossfield/READING.md) |

## 보조 반례 — 본분모에 합하지 않음

| 사례 | 실제로 읽은 반례 | 허용 문장과 첫 추가 보관 원자료 |
| --- | --- | --- | --- |
| A-M929 | [UTC/Athens/03:00+03](https://github.com/moment/moment-timezone/issues/929);2020a/d/2021a Athens 멤버 동일 | 출력은 보고됐지만 자료판은 복수. 같은 run의dataVersion와전체pack지문 필요 |
| A-M938 | [import/dataVersion2021a](https://github.com/moment/moment-timezone/issues/938), 날짜 출력 없음 | 공급자 라벨 보고는 확인. 요청UTC·zone·결과를 가진 원동일run이 추가로 필요 |
| A-M967-M | [유지보수자의 단일REPL](https://github.com/moment/moment-timezone/issues/967#issuecomment-1019463236):Date·Sao_Paulo·0.5.34/2021e·08:05:14−03 | L+O-R로 제한한 같은 보고 귀속. 실제 loadedpackhash와외부 실행timestamp는 미확인 |
| A-M967-O/C | [원저자](https://github.com/moment/moment-timezone/issues/967), [다른참가자](https://github.com/moment/moment-timezone/issues/967#issuecomment-1004746405)의−02와host/tz차이 | 유지보수자의2021e를 이 둘에 붙이지 않는다. 각각의 원로더/모듈경로가 필요 |
| A-M989 | [초/ms와 offset 부호](https://github.com/moment/moment-timezone/issues/989#issuecomment-1152829460) | 다른순간·부호의값을 판변화로 읽지 않는다. 같은epoch의unit·API를 먼저 맞춤 |
| A-M1015-M | [Amman 유지보수자0.5.38 출력](https://github.com/moment/moment-timezone/issues/1015#issuecomment-1312456640) | package판/값은 보고됐지만dataVersion는없다. 원저자+02와같은환경으로합치지않음 |
| A-P40915 | [London gap](https://github.com/pandas-dev/pandas/issues/40915),2021저자/유지보수자03:00과2025다른저자02:00 | 동일시스템 변경구간아님. 두사건의process계보와installreceipt필요 |
| A-P41591 | [US/Eastern tzinfo/localize](https://github.com/pandas-dev/pandas/issues/41591)에서자정날짜차이 | 같은판표기도입력구성차이가날짜를바꿀수있음. 원UTC/tzinfo.utcoffset를연결해야함 |
| A-P41834 | [Broken_Hill 두 공급자](https://github.com/pandas-dev/pandas/issues/41834#issuecomment-861501342):2000에는pytz/zoneinfo+10:30동일,1900에는차이 | 같은offset으로공급자식별불가. 정밀초·다른시대입력과실제resource필요 |
| A-PW1 | [원저자워크숍](evidence/artifacts/notebook-supplement.json)의날짜output과별도환경OK | 날짜파싱저장출력은확인;다른notebook환경표를같은kernel로붙이지않음. 셀실행시각/UUID필요 |
| A-PW2 | [2020/2024원본대조](evidence/artifacts/notebook-second-author.json):메타데이터만바뀌어도모든output동일 |2024환경으로새실행했다는증거없음. 재실행하지않았다는확정도불가. 원실행영수증필요 |
| A-XG9 | [2023복제패키지의2008로그](https://doi.org/10.7910/DVN/G9QZOU),N694/party.5780659 | 같은아카이브라도2023vintage코드와2008run은다름.2023실행log와입력해시필요 |

## 새 실행과 원 자료 재취득을 혼동하지 않기

이 카드의 “다음 관측”은 이미 공개된 원 기록에서 찾아야 할 최소 연결 정보를 뜻한다. 새 사용자에게 로그를 요구하지 않았다. 지금 같은코드를 실행해값이일치해도 원프로세스의수신·로드·실행시각을증명하지못한다. 각다운로드/접근실패는 검색원장을 따른다.
