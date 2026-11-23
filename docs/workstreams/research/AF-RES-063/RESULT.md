| 사례·층·원기록 URL | 실행자·실행시각 | 입력 UTC·지역·호출 | 선언·설치·로드 판 | 같은 실행 연결키 | 당시 출력·원위치 | 양립하는 판·미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| N-P1 · 자연 · [pandas #38928](https://github.com/pandas-dev/pandas/issues/38928) | nabelekt; 게시 2021-01-03; 실행 UTC **미확인** | `2020-10-19 18:58:20 EDT` 등 → `pd.to_datetime`; UTC·IANA 지역 미확인 | pandas1.2.0/Python3.7.3 선언; 설치 미확인; 같은 보고 warning의 dateutil 경로만 있음 | body의 test.py/Running block; PID 없음 | naive `2020-10-19 18:58:20` 등과 UnknownTimezoneWarning; body Running 절; O-R | tzdb 조회 자체 미확인. dateutil stock 세 판 중 warning 행1218은2.8.1과 맞으나 패치판·다른 환경 배제 못 함. [R-N-P1-body](receipts.csv), [후보](candidate-editions.csv) |
| N-P2 · 자연 · [pandas #39398](https://github.com/pandas-dev/pandas/issues/39398) | rwijtvliet; 게시 2021-01-25; 실행 UTC **미확인** | Berlin 2020-03-27부터4일; `i+i.freq`; 첫 입력은 표시 offset 기준03-26 23Z라는 산술 | pandas1.2.0, show_versions의 pytz2020.5/dateutil2.8.1; 공식 pytz2020.5는2020e; 실제 설치·로드판 미확인 | 동일 body지만 i/i2와 환경표는 별도 블록; 첫 날짜 불일치 | `2020-03-30 01:00+02:00`을 게시. 첫 i는27일인데 첫 i2는29일이라 명시한 +1 Day와 결속 충돌; O-R | Berlin 멤버는 pytz2020.1/2020a와2020.5/2020e에서 동일. 전체판·정확 호출 귀속 미확인. [R-N-P2-body](receipts.csv) |
| N-P3 · 자연 · [pandas #40336](https://github.com/pandas-dev/pandas/issues/40336) | teddyward; 게시 2021-03-09; 실행 UTC **미확인** | `date_range` endpoint `2020-03-09 00:00-07`→2021-03-09 00:00-08, 별도 LA zone; UTC07Z/08Z 산술 | pandas1.2.3, pytz2020.1/dateutil2.8.1 환경표; 공식2020a 대응만 확인; 실제 로드 미확인 | body의 실패 호출과 오류; expected와11월 댓글은 별개 | `TypeError: Start and end cannot both be tz-aware with different timezones`; 날짜 성공 출력 아님 | 오류는 두 endpoint tzinfo 차이와 양립; 특정 자료판을 고르지 못함. expected는 `freq='H'`까지 바뀐 다른 호출. [R-N-P3-body](receipts.csv) |
| N-M1 · 자연 · [Moment #922](https://github.com/moment/moment-timezone/issues/922) | lucapu88; 게시 2021-01-08; 실행 UTC **미확인** | `2021-1-8 08:00`, Rome, `moment.tz(...).format()`; offset/format 없는 입력 | 패키지·설치·dataVersion 모두 미확인 | body의 입력/출력; 원 parser 내부 순간 미확인 | `2021-01-08T09:00:00+01:00`; 08:00+01은 expected; O-R | 출력 해석08Z와 의도한 현지07Z를 구별. 공식2020a/d Rome 멤버 동일; 유일판 아님. [R-N-M1](receipts.csv) |
| N-M2 · 자연 · [Moment #925](https://github.com/moment/moment-timezone/issues/925) | skang; 게시 2021-01-23; 실행 UTC **미확인** | `2021-01-23 0:02`/`00:02`를 `guess()` 지역에 전달; 실제 지역·UTC 미확인 | 0.5.32 선언; 공식 기본판2020d; 설치·실제 dataVersion 미확인 | 같은 body의 두 문자열·두 결과; 실행 ID 없음 | 첫 입력→전날19:02, 두 번째→당일00:02; body; O-R | 한 자리 hour의 parser 경로 차이와 양립. 0.5.32 선언을2020d 실제 로드로 승격하지 않음. [R-N-M2](receipts.csv) |
| N-M3 · 자연 · [Moment #926](https://github.com/moment/moment-timezone/issues/926) | joemarieandres; 게시 2021-02-05; 실행 UTC **미확인** | `format('z')`만 있음; 지역·날짜·UTC 미기재 | 0.5.32 표기; 설치·로드 미확인 | body의 정성 보고; 완전 호출 없음 | 이름 대신 offset 표시라는 관측. 정확 숫자·문자열 미확인; PST는 expected | 날짜·지역이 없어 관측값 조건부 후보집합 미정의. 더 풍부한 #929로 교체하지 않음. [R-N-M3](receipts.csv) |
| E-P1 · 실행물 우선 · **빈자리** · [고정15 run](evidence/artifacts/frozen-pandas-runs.json) | 배정 없음; 후보의 원 run 시각은2025-12-22~23 | 같은 run 입력·지역·호출 미확인 | 고정 workflow/environment는 선언; 설치·로드 미확인 | 후보15개 run ID/attempt는 있음; 날짜 출력으로 선정된 run 없음 | 로그13×410, skipped2×404; artifacts15/15 빈 목록 | 출력 조건을 충족한 첫 사례 미확보. 후보 첫 run을 이 자리의 성공 사례로 대입하지 않음. [조회 영수증](evidence/artifacts/pandas-log-attempts.json) |
| E-P2 · 실행물 우선 · **빈자리** · [동일 고정 후보군](evidence/artifacts/frame.csv) | 배정 없음 | 미확인 | 미확인 | 첫15 후보 안에서 두 번째 보존 날짜 출력 미확보 | 당시 날짜 출력 미확인 | 뒤의 다른 성공 CI/노트북으로 교체하지 않음. 후보 모집단15와 본자리2를 구별. [R-E-P2](receipts.csv) |
| E-M1 · 실행물 우선 · **빈자리** · [공식 경로·대체 아카이브](evidence/artifacts/fallback-http.json) | 배정 없음; 역사 실행 총수 미확인 | 미확인 | 미확인 | Actions60개월 조회0; Travis 원 경로/API/Wayback에서도 run ID 미확보 | 보존 날짜 출력 미확인; 예제 주석은 제외 | 조회 가능한 원기록 관측0은 과거 실행 부재를 뜻하지 않음. [R-E-M1](receipts.csv) |
| E-M2 · 실행물 우선 · **빈자리** · [고정 문서 탐색](evidence/artifacts/document-reads.json) | 배정 없음 | 미확인 | 미확인 | 지정 공식 진입문서에서 적격 저자 실행 노트북 목록 미확보 | 미확인 | 원목록·순번·당시 출력이 먼저 필요. 인터넷 전체에서 없다는 주장은 하지 않음. [R-E-M2](receipts.csv) |

| 사례·핵심 주장 | V0 판단 | V1 판단 | V2 판단 | 반증·충돌 출처 URL | 추가 열람 비용 | 사용자에게 허용되는 문장·다음 관측 |
| --- | --- | --- | --- | --- | --- | --- |
| N-P1 · EDT 입력에 특정 tzdb가 적용됐는가 | pandas1.2.0 표기만 있음 | 공개 dateutil 코드 비교는 가능; 원 설치 없음 | 같은 보고 경로·경고는 있으나 region/UTC와 tzdb lookup이 미확인 | [원 warning](https://github.com/pandas-dev/pandas/issues/38928); [loader/행 비교](evidence/pandas/official-evidence.json) | V0/V1/V2 개별 요청1/0/4, 성공4·실패1; 공통 읽기 별도 | “작성자는 naive 출력과 경고를 보고했다.” 다음: 당시 같은 run의 parser판·입력 의미·tzinfo. 조회가 없었다면 tzdb판은 해당 없음 |
| N-P2 · pytz2020.5가 이 출력의 원인인가 | 환경표의 판 자기 보고 | 공식2020.5→2020e는 확인; 원 설치는 없음 | 첫 i/i2 날짜 충돌과 열린 Berlin 바이트 미확인 | [원 본문](https://github.com/pandas-dev/pandas/issues/39398); [서로 다른 전체판의 같은 멤버](evidence/pandas/candidate-member-evidence.json) | 1/0/5, 성공5·실패1; 공식 두 wheel은 공유 비용 | “Berlin 01:00 출력을 게시했으나 같은 호출·로드판은 확정할 수 없다.” 다음: 원 셀 순서·입력 상태·전체 배포 또는 구별 멤버 지문 |
| N-P3 · expected 날짜 배열을 실제 결과로 쓸 수 있는가 | pandas/pytz 환경표 | 공식2020a 대응만 확인 | 실패 출력만 확인; expected는 입력과 freq가 다른 호출 | [Code Sample/Expected Output](https://github.com/pandas-dev/pandas/issues/40336) | 1/0/4, 성공4·실패1 | “작성자는 서로 다른 고정 offset endpoint에서 오류를 보고했다.” 다음: 성공을 주장할 호출 자체의 보관 출력 |
| N-M1 · 한 시간 차이가 자료판 차이인가 | 판 표기 없음 | 2020a/d 공식 후보의 Rome 멤버 동일 | parser 해석·원 UTC 미확인; 해결 댓글은 입력·지역도 달라짐 | [다른 후속 호출](https://github.com/moment/moment-timezone/issues/922#issuecomment-756704179) | 1/0/3; HTML220,626B만 실측 | “작성자는 Rome 입력08:00에09:00+01을 보고했다.” 다음: 같은 입력의 explicit format·epoch·dataVersion |
| N-M2 · 0.5.32→2020d 실제 실행인가 | 패키지 자기 신고 | 기본 pack의2020d 라벨은 확인 | guess 지역·core판·로드판 미확인; format 변경은 판 변경과 다름 | [hour 정정](https://github.com/moment/moment-timezone/issues/925#issuecomment-766717317) | 1/0/3; HTML246,127B만 실측 | “입력의 hour 자릿수에 따라 다른 결과를 보고했다.” 다음: guess 결과, 두 epoch, 명시 format, 실제 로더 라벨 |
| N-M3 · 이름 대신 offset이면 과거 계산 오류인가 | 0.5.32 정성 보고 | 공식판 기본 라벨만 확인 | 실제 지역·순간·문자열 없음; 숫자 약칭이 가능한 규칙도 있음 | [유지보수자 답](https://github.com/moment/moment-timezone/issues/926#issuecomment-780154079) | 1/0/3; HTML222,356B만 실측 | “작성자는 offset 표시를 보고했다.” 다음: 원 zone·UTC·정확 z/Z 출력; PST를 지역 ID로 임의 대체하지 않음 |
| E-P1 · CI 성공이면 날짜 출력·자료판이 확인되는가 | 원 run metadata만 확인 | 고정 workflow/env의 하한만 확인 | 원 run jobs/artifacts/logs를 찾았으나 날짜 stdout 없음 | [최초 run](https://github.com/pandas-dev/pandas/actions/runs/20441074943); [410/404](evidence/artifacts/pandas-log-attempts.json) | 공유 E-AUDIT: 아래 비용 원장; 빈자리마다 중복 합산 안 함 | “이 run은 존재하지만 날짜 출력·실제 로드판은 미확인이다.” 다음: 이 고정 run의 당시 stdout/환경 artifact |
| E-P2 · 빈 출력을 다른 성공 자료로 채워도 되는가 | 빈자리 | 공개 소스는 설치 영수증 아님 | 동일15에서 두 번째 적격 출력 없음 | [고정 후보·순서](evidence/artifacts/frozen-pandas-runs.json) | E-P1과 공유 | “보강 두 번째 사례를 확보하지 못했다.” 다음: 원15 안의 보관 출력; 순서 밖 성공례는 보조로만 추가 |
| E-M1 · 목록0이면 당시 실행도0인가 | 조회 가능한 목록0 | 역사 README는 Travis→Actions 경로를 제공 | 원 API/아카이브에도 run ID를 못 찾음; 역사 전체 미확인 | [원 경로 시도](evidence/artifacts/fallback-http.json) | 공유 E-AUDIT;60월+공식 대체 경로 | “조사한 공식 목록에서 적격 원기록을 확보하지 못했다.” 다음: 날짜·ID가 있는 원 작성자 실행목록 |
| E-M2 · 공식 사이트 예제를 원 stdout으로 쓸 수 있는가 | 설명 예제만 있음 | 번들·custom data 경로는 확인 | 출력·환경이 같은 과거 실행에 연결되지 않음 | [고정 문서 원전](evidence/artifacts/document-reads.json) | E-M1과 공유 | “예제는 원 실행 출력의 증거가 아니다.” 다음: 저자 보관 노트북의 저장 output과 run 계보 |

# AF-RES-063 결과 — 부분 인계

**공개 링크의 버전 표기만으로 “그날 그 SDK가 그 시간대 자료판을 사용해 이 날짜를 냈다”를 제품의 확정 사실로 붙일 수 없다.** 다만 공개 기록의 종류와 같은 실행의 연결 정도를 밝히면, 저자가 보고한 값, 보존된 셀 출력, 공급자가 스스로 표시한 자료판을 서로 다른 강도로 반환할 수 있다. 보조 사례에서는 입력·지역·출력·dataVersion이 같은 REPL에 이어지는 실제 공개 보고를 찾았다. 그러므로 “공개 기록으로는 언제나 불가능하다”도 이 조사와 맞지 않는다. [자연 영수증](receipts.csv) · [보조 REPL](https://github.com/moment/moment-timezone/issues/967#issuecomment-1019463236)

위 표의 ‘당시 출력’은 작성자가 과거 실행의 결과라고 게시한 현재 공개 본문의 값이라는 뜻이다. 최초 본문판을 독립 복원하거나 원 stdout을 확보했다는 뜻이 아니다. 여섯 자연 보고 모두 정확한 실행시각은 **미확인**이다. 이 제한 때문에 무조건적인 과거 사실 문장 대신 보고 주체와 기록의 한계를 포함한 문장을 채택한다. [본문·편집 확인](evidence/pandas/edit-history-attempts.json) · [Moment 확인](evidence/moment/issue-html-edits.json)

## 두 층의 분모와 수용 상태

| 층·단위 | 추적 가능 | 과거 날짜·offset literal 출력 | 실제 사용 자료판 L 라벨 | 같은 실행의 입력·지역·판·출력 | 실제 로드 바이트 H |
| --- | --- | --- | --- | --- | --- |
| 자연 선정 6보고 | 6/6 | 4/6 O-R; 예외 포함 어떤 관측은6/6 | 관측0/6 | 관측0/6 | 관측0/6 |
| 보강 출력 배정 4자리 | 0/4 채움; 모두 빈자리 | 관측0/4 확보 | 관측0/4 확보 | 관측0/4 확보 | 관측0/4 확보 |
| 위 보강의 pandas 원 후보 15run | 15/15 metadata | 관측0/15 확보 | 관측0/15 확보 | 관측0/15 확보 | 관측0/15 확보 |
| 위 보강의 Moment 발견 원 후보 | 관측0개; 역사 총수 미확인 | 비율 해당 없음 | 비율 해당 없음 | 비율 해당 없음 | 비율 해당 없음 |
| 별도 보조 A-M967-M 1보고 | 1/1 | 1/1 O-R | 1/1 자기 보고2021e | 1/1 보고된 REPL 문맥 수준; 외부 실행시각·바이트는 미확인 | 관측0/1 |

보강의0/4는 네 실행이 실제로 없었다는 비율이 아니라 배정 자리를 채운 수다. pandas15는 현재 조회되는 적격 후보의 첫15이며, 삭제·접근 결손 이전의 역사 전체 첫15를 복원했다고 하지 않는다. Moment는 0/0을 성공률로 계산하지 않는다. 보조의1을 자연0/6이나 보강0/4에 더하지 않았다. [집계](evidence/integrated-counts.json) · [실행물 판정](evidence/artifacts/acceptance-artifacts.json)

직접 독해 원장은 **110행, 보수적 중복 제거 후51개 독립 계보**다. 이 중 출력 차이를 다룬 이슈 계보38개(17+21), 공식 원전8개, 저자 노트북2개, 다른 분야2개와 별도 보조 복제자료1개를 최소수에 산입했다. 직접 읽었지만 출력 적격이 아닌22본문과 stdout 없는15 CI는 이51개에서 제외했다. 같은 이슈 댓글, 같은 코드의 다른 판, 같은 패키지 멤버, 같은 노트북의 여러 셀을 독립 저작으로 늘리지 않았다. [출처 원장](sources.jsonl) · [계수](evidence/integrated-counts.json)

실행·결과 계열의 최소4건은 A-PW1/A-PW2의 저장 출력 노트북과 X-D1의 저자 발행 월별 숫자 자료, X-Z1의 저자 발행 원 시뮬레이션 결과라는 **서로 다른 네 저작의 합집합**으로 충족한다. X-D1을 실행 로그로 분류하지 않는다. 이4건에서 실행시각·실제 입력 해시·로드·출판 출력까지 완전 연결한 수는 관측0/4다. A-PW2 출력은2020판에도 존재하므로2021–2025 신규 실행으로 세지 않는다. 별도 보조 A-XG9의 원 Stata 로그도2008 실행과2023 발행을 구별한다. [다른 분야 독해](evidence/crossfield/READING.md) · [독립 검토](evidence/peer-review.json)

## 모집을 어떻게 고정했는가

자연층은2021-01-01~2025-12-31 UTC 생성 이슈, PR 제외, 제목의 timezone/time zone/tzdata/DST/offset/daylight를 대상으로 했다. 키워드 검색 후 제목 census를 대조하고 생성시각·번호로 첫30본문씩을 읽었다. pandas 제목 census1,899개에서 키워드 검색이 놓친6개를 **본문 전에** 복원했다. 첫30 경계가2021-10-22에서2021-06-10으로 바뀌었다. Moment는 전기간142개 중 제목적합80개이며 첫30은2021-01-08~2022-11-10이다. 후보의 나중 버전·로그 충실도를 보고 선정하지 않았다. [SCOPE](SCOPE.md) · [pandas 사전 봉인](evidence/pandas/frame-seal.json) · [Moment 사전 봉인](evidence/moment/title-frame-seal.json)

Moment #1158은 생성시각2021년이지만2026-09-14 이관됐다. 현재 저장소의 생성시각순 목록에서는5번째로 유지했고 적격이 아니어서 선정3에는 영향이 없다. 현재 제목·본문을 기준으로 한 후향적 목록과 당시 저장소의 목록은 다르다. 원 제목의 변경과 최초 본문의 복원 실패도 결과의 한계다. [이관 원 기록](https://api.github.com/repos/moment/moment-timezone/issues/1158/timeline)

보강층은 결과를 보기 전에 workflow 이름·경로 필터와 Actions→다른 공식 CI→공식 연결 저자 노트북의 순서를 고정했다. 두 저장소60개월씩 조회했다. pandas2025-12의1,150개 응답은 상한 때문에 구간분할했고, 먼저 찾은 적격60개에서 첫15를 고정했다. 페이지의 총수178→177 변동은 한 페이지40개 좁은 구간으로 첫15가 같음을 확인했다. 성공11·실패1·취소1·skipped2를 그대로 유지했다. 15run,13commit,8triggering account,68job은 서로 다른 단위다. [봉인](evidence/artifacts/frozen-pandas-runs.json) · [재대조](evidence/artifacts/run-details-and-check.json)

## Q1 — 실제 출력이라고 읽을 수 있는 것은 무엇인가

N-P1/N-P2/N-M1/N-M2에는 작성자가 실제 결과라고 제시한 날짜 문자열이 있다. N-P3은 오류만, N-M3은 표시 형식에 대한 정성 관측만 있다. expected를 실제 output으로 바꾸거나 코드만 있는 예제를 실행 로그로 세지 않았다. N-P3의 hourly 배열은 실패 코드와 입력·freq가 다르다. N-M1의08:00+01은 요구값이고09:00+01이 보고값이다. [원 이슈 #40336](https://github.com/pandas-dev/pandas/issues/40336) · [#922](https://github.com/moment/moment-timezone/issues/922)

보조 A-PW1과 A-PW2는 원 저자 notebook의 JSON `outputs`와 `execution_count`를 직접 읽었다. 그 필드는 저장 결과의 증거지만 실행시각·kernel UUID를 보장하지 않는다. X-Z1은24노트북 모두 출력이 비었고, 실제 숫자는 별도 raw-result 파일에 있다. CI15는 원 run/job metadata가 있지만 날짜 stdout을 받지 못했다. 도구의 성공 상태, green check, 사이트 주석은 관측값으로 대체하지 않았다. [노트북1](evidence/artifacts/notebook-supplement.json) · [노트북2](evidence/artifacts/notebook-second-author.json) · [ZIP 전수 output 검사](evidence/crossfield/zenodo-package-inspection.json)

이슈의 최초 생성일, 댓글 생성일, 파일 commit일, 원 실행시각, 현재 열람 UTC는 각기 별도 열이다. 원본 편집 이력은 HTML/timeline 및 edit 경로까지 시도했으나 최초 body의 독립 사본은 미확보다. 따라서 “2021년에 생성된 이슈의 현재 본문은 …라고 보고한다”가 더 정확한 반환 문장이다. [원 위치·시각·해시](sources.jsonl)

## Q2 — 동일한 순간·지역·호출인가

N-P1의 EDT는 지역 ID도 명시 숫자 offset도 아니다. 경고 뒤 naive 값이 나왔다고 해서 UTC−04 또는 America/New_York를 자동 부여하지 않는다. N-M1의 모양이 느슨한 문자열은 명시 format이 없고, 출력09:00+01에서 계산한08Z와 의도한 local08:00의07Z는 다른 순간이다. N-M2는 `guess()` 반환을 남기지 않았다. -05 지역/UTC 파싱 설명은 가능한 경로일 뿐 관측 사실이 아니다. [세부 입력](receipts.csv)

N-P2는 더 강한 내부 반례다. `i+i.freq`가 첫 날짜를27→28일로 한 번 이동시키는 명시 호출인데 게시된 i2는29일부터 시작한다. 보이지 않는 중간 연산을 만들어 붙이지 않는다. DST를 가로지르는24시간 Tick과 달력 하루의 차이를 설명하는 유지보수자 답은 유용하지만, 불일치하는 원 출력의 실행 순번을 복원하지 못한다. [본문과 답](https://github.com/pandas-dev/pandas/issues/39398)

선정 밖 #989는 초를 받는 `unix()` 값을 ms를 받는 `Zone.utcOffset()`에 넣은 사례다. API의 −60은 UTC 서쪽 분이고 Moment 객체의 offset 부호는 동쪽 분이다. 단위·양의 방향을 통일하지 않으면 서로 다른 순간과 부호를 자료판 변화로 오독한다. [원 입력과 유지보수자 재현](https://github.com/moment/moment-timezone/issues/989#issuecomment-1152829460) · [공식 ms 명시 정정](https://github.com/moment/momentjs.com/commit/d0dc7f13dfbb08de1774ab01fdb4590293f558e4)

fold/gap에서는 지역과 현지 시각만으로 순간이 하나가 아닐 수 있다. 공식 PEP495의 fold=0/1 및 gap 규칙을 대조했지만, 선정 사례의 누락된 fold를 추정해 채우지 않았다. 출력에서 UTC를 역산한 값은 ‘연구자 산술’, 원 작성자가 게시한 입력은 ‘저자 보고’로 분리했다. 날짜만 표시된 A-PW1에는 UTC/지역이 해당 없음이며, 날짜 모양의 출력이 언제나 tzdb 사용을 뜻하지 않는다. [공식 규칙 독해 S-L04](sources.jsonl) · [A-PW1](evidence/artifacts/notebook-supplement.json)

## Q3 — 선언·고정 배포·설치·실제 로드는 무엇이 다른가

이 연구는 D(선언), K(공개 고정 배포·잠금), I(해당 실행의 설치), L(로드 공급자의 경로·라벨 자기 보고), H(실제 열린 바이트 지문)를 분리한다. O-R은 작성자 보고, O-M은 보존 기계 출력/노트북, E는 expected, R은 현재 연구자 재실행이다. 어느 사례에서도 현재 받은 공식 파일을 과거 프로세스의 H로 바꾸지 않았다. [판정 계약](SCOPE.md)

공식 CPython3.9.1의 ZoneInfo는 TZPATH에서 먼저 찾고 없으면 tzdata를 사용한다. dateutil2.8.1은 system path·Windows registry·bundled zoneinfo·POSIX 경로가 있다. pytz2020.5는 `PYTZ_TZDATADIR`로 자료 위치가 바뀔 수 있다. Moment0.5.32는 기본 index가 packed data를 읽지만 `tz.load()`와 `tz.add()`가 공개되고, `guess()`는 Intl/host 경로와 캐시를 쓴다. 따라서 설치된 패키지 목록과 실제 선택한 공급자는 같은 명제가 아니다. [S-L01~03](sources.jsonl) · [고정 Moment loader](https://github.com/moment/moment-timezone/blob/3128dda269e4c08e11fc42e3dfbaeed1f7e33542/moment-timezone.js)

반대로 **A-M967-M**은 같은 Node REPL에 `TZ=America/Sao_Paulo`, Date 입력, format과 offset, `tz.version=0.5.34`, `dataVersion=2021e`가 함께 있다. 보고된 Date 문자열의 UTC 산술은2022-01-23 11:05:14Z이며 출력은08:05:14−03:00이다. “이 유지보수자의 공개 REPL은2021e라고 표시한 공급자로 이 값을 출력했다고 보고한다”는 L+O-R 문장은 허용한다. 외부 타임스탬프나 실제 로드 파일 해시가 없으므로 공식 바이트의 실행을 H로 확정하지 않는다. [원 REPL](https://github.com/moment/moment-timezone/issues/967#issuecomment-1019463236)

**A-M938**은 정반대다. utils import 후 `dataVersion=2021a` 표기는 있으나 날짜 입력·출력이 없다. 이것을 어떤 시각의 계산 결과로 확장할 수 없다. 그리고 #967의 원저자−02, 다른 참가자의 host/tz 불일치, 유지보수자의−03은 서로 다른 세 사건이다. 버전 한 줄을 다른 참가자 출력에 붙이지 않았다. [라벨만 있는 보고](https://github.com/moment/moment-timezone/issues/938) · [다른 참가자의 사건](https://github.com/moment/moment-timezone/issues/967#issuecomment-1004746405)

## Q4 — 한 관측이 후보를 얼마나 제거하는가

후보집합은 조건부이고 완전 열거가 아니다. 다음 비교는 보고 당시 이용 가능했던 특정 공개 공급자들 사이의 최소 하한을 만든다. 사용자 설치·커스텀 bundle·patch·다른 공급자를 전부 열거하지 않았으므로 유일판 판정은 보류한다. [30행 후보 원장](candidate-editions.csv)

| 비교 | 정확 라벨·배포가 제거하는 것 | 지역 멤버 지문이 제거하는 것 | 관측값이 제거하는 것·한계 |
| --- | --- | --- | --- |
| pytz2020.1/2020a ↔2020.5/2020e, Berlin | 공식 package/OLSON_VERSION 대응은 두 전체판을 구별 | 두 Berlin 멤버는2,298B, SHA256 `5ee475f71a0fc1a32faeb849f8c39c6e7aa66d6d41ec742b97b3a7436b3b0701`로 같아 둘 다 남음 | Berlin offset 구성 요소에는 최소 두 판이 남음. 명시 호출과 전체 i2는 내부 충돌이 있어 완전한 입력·출력 쌍의 양립 판집합은 미확인. [실제 wheel 비교](evidence/pandas/candidate-member-evidence.json) |
| Moment0.5.31/2020a ↔0.5.32/2020d, Rome | 0.5.32라는 정확 공식 pack은2020d; 원 설치 연결은 별개 | Rome1,011B, SHA256 `ebc19f8feb975df485f2a1aabece72f31d9cfdcf80309008af76b103556a3c50` 동일 | N-M1의+01과 한 시간 차이로 두 자료판을 가를 수 없음. [고정 멤버](evidence/moment/candidate-edition-files.json) |
| Moment Athens, 2020a/d/2021a; A-M929 | 원저자0.5.33 선언만으로 로드판 확정 불가 | Athens 멤버가 같아 최소 세 판이 남음 | UTC2020-05-18T00Z→03:00+03은 정확히 보고돼도 판은 복수. [원 보고](https://github.com/moment/moment-timezone/issues/929) |
| N-P1 dateutil2.7.5/2.8.0/2.8.1 | 같은 경고 문구만으로는 제거 못 함 | 원 파일 전체 hash는 없음. 무수정 source의 경고 행은1204/1206/1218 | 원 stderr1218은 제한된 stock 후보 중2.8.1을 지지하지만 패치판/줄 이동을 배제 못 함; tzdb판 증명도 아님. [공식 source 비교](evidence/pandas/official-evidence.json) |
| Dataverse XAMFQK V1/V2 | 전체 dataset version/manifest는5파일과61파일을 구별 | U_Data.xlsx ID/MD5가 동일해 두 판이 남음 | 같은 월 숫자 하나로 전체 vintage판을 구별 못 함. [고정 V1/V2](evidence/crossfield/dataverse-version-inspection.json) |

다른 공급자가 같은 값을 내는 직접 보고도 있다. pandas #41834의 유지보수자는 Australia/Broken_Hill의2000년 입력에 pytz와zoneinfo가 모두+10:30을 주고1900년에는9:26/9:30으로 다름을 게시했다. 현대 offset 하나는 공급자도 판도 식별하지 못하며,1800년 비교에서는 분 단위 반올림과 초 정밀도도 구별해야 한다. 이 값의 역사적 정답을 별도로 재검증했다고 주장하지 않는다. [두 공급자 원 비교](https://github.com/pandas-dev/pandas/issues/41834#issuecomment-861501342) · [초 정밀도 비교](https://github.com/pandas-dev/pandas/issues/41834#issuecomment-861518279)

새 구별 관측이 필요할 때는 근거를 먼저 읽었다. pytz의 고정2020a/e `tz/europe`에서 Volgograd 말단이 +04 유지와2020-12-27 02:00s의+04→+03으로 갈린다. 따라서 같은 공급자·같은 실행에서2021-01-01T00Z를 처리한 기록이 있다면 이 **두 후보**를 가르는 데 도움 된다. +04/+03은 원 전환행에서 수동 도출한 후보값이며, 이번 조사에서 현재나 과거에 실행해 얻은 값이 아니다. 두 판보다 큰 집합을 유일하게 나눈다는 주장도 하지 않는다. [S-P-L10/L11의 두 전환행](evidence/pandas/official-evidence.json)

Moment0.5.33은2021-02-06에 npm에 발행돼 자연 세 건의 최초 생성시각보다 뒤다. 이 npm판은 그 시점의 해당 공급자 후보에서 제외되지만, 상류2021a를 받은 커스텀 bundle까지 배제하지 않는다. 원 body의 최초 버전을 복원하지 못했으므로 이 시간 절단 역시 ‘본문이 당시 입력을 보존한다’는 조건을 붙인다. [발행 원전](evidence/moment/package-metadata.json)

## Q5 — “그 사이 과거판이 바뀌었다”에 필요한 두 사건

최소한 같은 시스템 계보·같은 입력의 첫/마지막 관측과 각 시점의 로더 판 또는 열린 바이트, 이를 연결하는 설치·재배포 영수증이 필요하다. 두 관측이 있으면 변경은 그 사이 구간에 있었다고 제한할 수 있다. 하나면 그 한 관측점만 말할 수 있다. 자료가 공개된 시간은 프로그램이 받은 시간이나 장기 실행 프로세스가 다시 로드한 시간과 다르다. [ZoneInfo cache/pickle 규칙 S-L01](sources.jsonl)

선정6보고와 pandas15후보에서 이러한 변경 사슬은 관측0이다. #925의 explicit format 해결은 입력 해석의 변경이고, #922 후속은 다른 변수·지역을 사용한다. #967의 여러 날짜 출력은 참가자도 다르다. pandas #40915의2021과2025 댓글도 별도 실행으로 남겼다. 이들을 전후 한 쌍으로 합치지 않았다. [pandas 보조 사건](evidence/pandas/auxiliary-cases.json) · [Moment 영수증](evidence/moment/receipts.json)

A-PW2에서는2024 notebook이 Python3.9.20 metadata와 pandas2.2.3 requirements를 갖지만2020판의 모든 저장 output과 같다. 2024 patch는 경로·메타데이터·형식을 바꾼다. 이는2024 새 환경으로 실행했다는 추정을 반박하며, 반대로 재실행하지 않았다는 확정 증거도 아니다. 출력만 같아서는 실행 또는 환경 변경 사건의 유무를 가릴 수 없다. [2020/2024 직접 대조](evidence/artifacts/notebook-second-author.json)

## Q6 — 다른 분야의 대응 증거

선정은 Dataverse/Zenodo 원 저자 metadata에서 시작했고 날짜·영구 ID로 읽을 순서를 고정했다. Dataverse의 최초 기간 내 native 원저작 XAMFQK와 Zenodo의 고정 검색창 내 첫 적격6532252를 읽었다. Zenodo API의 oldest가 전역 발행일 정렬은 아니므로 수집30개 안에서만 순서를 보장한다. 검색에서 먼저 보인 G9QZOU는 더 풍부하더라도 보조로만 두었다. [검색 프레임](evidence/crossfield/frame-metadata.json) · [시도·수신 원장](evidence/root-access.jsonl)

| 별도 사례 | 관측월·저장판/해시·실행·출판 출력 | 시간대 문제의 대응 | 빠진 열 |
| --- | --- | --- | --- |
| X-D1 · [러시아 경제 불확실성 복제자료](https://doi.org/10.7910/DVN/XAMFQK) | Sheet1의199210·숫자값, V1/V2, 받은 XLSX MD5 일치. VINTAGE=0/1은 날짜가 아니라 사전 종류 | 관측월↔지역/순간; dataset판↔tzdb전체판; 파일hash↔지역멤버hash | 61파일에 code/notebook/log 없음. 실제 분석이 이 파일을 읽었는지와 실행시각 미확인 |
| X-Z1 · [스케줄링 실험 결과](https://zenodo.org/records/6532252) | 78,304,329B ZIP MD5 일치; scenario와200행 raw output; 코드의 정확 상대경로;24노트북의 저장output0, CSV/PDF0 | scenario/seed↔정확 입력; raw result↔관측값; ZIPhash↔배포 바이트 | 논문 표를 만든 동일 실행의 read digest·실행 셀 결과·시각 미확인; 관측월은 해당 없음 |

A-XG9의2023 복제패키지는1998/2004/2018 변수로 분석하는 코드와2008 Stata 원로그를 함께 보관한다. 원로그에는N694, 계수.5780659와 실제 호출이 있지만2023의 다른 vintage 데이터를 읽은 실행은 아니다. 공표된 원모형 숫자와 닮았다는 이유로 다른 데이터판을 실제 사용했다고 판단하면 틀린다. 동일 아카이브·같은 논문 주제는 동일 run 키를 대신하지 않는다. [원 저자 패키지](https://doi.org/10.7910/DVN/G9QZOU) · [읽은 행443~460의 요약](evidence/crossfield/READING.md)

## Q7 — 최소 기록과 제품 문장, 비용

V0/V1/V2는 실제 확보한 자료를 순차 노출하는 비교다. 최초 이슈 GET에 이미 출력이 들어 있었더라도 V0에서는 날짜·판 표기만 드러내고 V2에서 입력·출력 문맥을 함께 본다. 세 번의 독립 실행이나 맹검 실험을 했다는 뜻이 아니다. 같은 자료를 되읽은 비용과 새 URL 취득을 구별했다. [30개 비교 셀](views.csv)

| 관점 | N-P2에 V0만 적용 | V1에서 더 말할 수 있는 것 | V2를 거친 허용 문장 |
| --- | --- | --- | --- |
| 사용자 | pytz2020.5라는 환경 표기가 있음 | 그 공식판의 자료 라벨은2020e | “작성자가 Berlin01:00 결과를 보고했으나 명시 호출과 첫 날짜가 어긋난다.” |
| 유지보수자 | bug 재현 환경의 단서 | 공식 코드의 Tick·timezone 경로를 조건부 비교 | “24시간/달력일 차이가 설명 후보지만 이 붙여넣기만으로 같은 호출의 원인을 확정하지 못한다.” |
| 배포 담당자 | 선언판만 보임 | 두 공식 wheel과 멤버hash는 확인 가능 | “이 배포물의 Berlin 멤버는 다른 전체판과 같다. 과거 run의 설치·로드 영수증은 없다.” |
| 과거 결과 감사 설계자 | 버전문자열을 색인할 수 있음 | 배포 후보를 고정할 수 있음 | “원 셀 순서·입력hash·열린 공급자/전체pack·출력을 같은 run 키로 묶어야 승인할 수 있다.” |

자연6에 배정한 개별 열람은 **28요청=25성공+3실패**다. V0는6개 issue GET, V1은 새 개별 URL0(공통 공식 원전 사용), V2는22개 댓글/timeline/HTML/edit 시도다. V1의0은 연구 비용0이 아니다. Moment HTML 세 응답의689,109B만 실제 부분 비용으로 확인했다. connector 응답문자수를 HTTP byte로 환산하지 않았으며 전체 다운로드 bytes는 미확인이다. 최종 감사의 N-P2 원본문 재열람1회는 보기 비교 밖에 따로 기록했으므로, 이 감사까지 포함한 선택 사례 요청은29회(성공26·실패3)다. 원 후보 비교와 root의78MB ZIP 등은 공유 조사 비용으로 따로 남겼다. [비용 집계](evidence/view-costs.json) · [개별 보기](views.csv) · [root 취득](evidence/root-access.jsonl)

보강의120월 조회,15run/job/artifact/log 검사, 추가 job log4건 및 공식 대체 아카이브는 E-AUDIT 공유 비용이다. 이를 네 빈자리의 비용으로 네 번 더하지 않았다. 본10자리에서 실제 사용판 귀속이 강화된 사례는 관측0/10, 같은 실행의 판·값을 확보한 V2 셀도 관측0/10이다. 자료를 더 읽은 효과는 오류를 확정한 척하는 것이 아니라 미확인의 원인과 첫 추가 원자료를 구체화한 데 있다. [원 검색 원장](evidence/artifacts/search-log.jsonl)

보조에서는 제한적 상승이 있다. A-M938은 D에서 L의 공급자 라벨 보고까지, A-M967-M은 D에서 L+O-R의 같은 REPL 보고까지 올라간다. 각각 원 이슈의 댓글·import 문맥을 추가로 읽은 결과이며 전체 배포 바이트 H까지 오르지는 않는다. 자연 비율에 합치지 않는다. 실사용판이 다수여도 출력은 보고된 A-M929, 공급자판은 표시됐어도 해당 날짜 출력은 없는 A-M938를 함께 보여 주어 제품 문장의 두 축을 유지한다. [보조 카드](cards.md)

## 반증·감도·인수 범위

‘버전만으로 부족하다’는 첫 결론을 깨려고 dataVersion·동일 REPL·보존 notebook·실행 환경 artifact를 적극 찾았다. 그 결과 A-M967-M의 L 수준 연결은 인정했고, 절대 불가능이라는 결론을 버렸다. 반대로 지역hash면 충분하다는 대안은 Berlin/Rome/Athens의 실제 동일 멤버가 반박했다. 최신 파일의 환경표기면 저장output에 적용할 수 있다는 대안은 A-PW2가 반박했다. [Q별 자기검토](SELF_CHECK.md)

N-P1을 경고만 묻는 사례로 좁게 제외하면 첫3은#39398/#40336/#40817이고, N-M3의 정성 관측을 제외하면#929가 세 번째다. 이것은 사후 민감도이며 본 선정을 교체하지 않았다. 두 변화 모두 실제 로드판의 원 영수증을 추가하지 않는다. “literal 숫자 출력이 얼마나 자주 있나”는 선정 해석에 민감하므로 일반 사용자 비율로 외삽하지 않는다. [pandas 감도](evidence/pandas/summary.json) · [Moment 감도](evidence/moment/notes.md)

AF-RES-059의14파일·72행, Beirut 대조, Grafana/pandas 소비자0/2는 고정 결과를 인수했을 뿐 재조사하지 않았다. 이번 신규 비교는2020a/e Berlin과Volgograd, Moment0.5.31~0.5.34 등 이번 원보고에 필요한 경로에 한정했다. 기존 Grafana 이미지 재추출, pandas 릴리스 재열거, BLS/ALFRED 재다운로드, 새 사용자 연락, 현재 서비스 점검은 하지 않았다. 신규 날짜변환 재실행과 저자 코드 실행은 **미실시**이며, 새 실행을 과거 증거로 사용하지 않았다. [인수](evidence/intake.json) · [묶음 이력](WORK_LOG.md)

## 마지막 불일치·약점

| 불일치·약점 | 영향받는 주장 | 직접 근거 URL·위치 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 원 stdout·최초 body·역사 목록 결손:15 CI 로그13×410/2×404, Moment 목록0, 현재본문/이관 목록 사용 | 과거 실행의 정확 시각·입력·자료판·출력, 역사 첫 후보 순서 및 보강4자리 완전 수용 | [원 run](https://github.com/pandas-dev/pandas/actions/runs/20441074943), [만료시도](evidence/artifacts/pandas-log-attempts.json), [이관](https://api.github.com/repos/moment/moment-timezone/issues/1158/timeline), [본문편집](evidence/pandas/edit-history-attempts.json) | 고정15 run 중 하나의 당시 stdout/환경 artifact 또는 원 저자 공개 archive와 최초본문 사본을 찾기 | 원기록이 같은 run/attempt·입력·로드·출력을 연결하고 기존 후보순서와 편집시각을 검증할 때 |
| 판 후보는 제한된 하한이며 지역hash/출력은 여러 전체판과 같음; N-P2 호출·출력 날짜도 충돌 | “유일 자료판”과 “그 판이 이 차이를 만들었다”는 주장 | [Berlin 실제hash](evidence/pandas/candidate-member-evidence.json), [Moment 동일 멤버](evidence/moment/candidate-edition-files.json), [N-P2 원본문](https://github.com/pandas-dev/pandas/issues/39398) | 원 셀 순서와 같은 run의 전체pack/로드path 지문; 필요하면 읽어둔 Volgograd 전환을 가르는 보관 두 번째 입력 | 해당 시점 모든 관련 후보를 열거하고 실제 로드 영수증이 유일 후보 및 정확 호출을 지지할 때 |
| 다른 분야 검색의 전역 발행순 불완전, 보관 바이트·노트북 metadata·출판 숫자와 실제 분석run이 끊김 | 최소 독해를 완전 실행증명으로 바꾸는 주장; 파일 개정일=재실행일 | [Zenodo 원판](https://zenodo.org/records/6532252), [Dataverse V1/V2](https://doi.org/10.7910/DVN/XAMFQK), [2020/2024 동일output](evidence/artifacts/notebook-second-author.json) | 날짜·PID 정렬의 완전 목록과 이미 공개된 원 분석log·입력digest·셀/run 키를 확보 | 모집 선행순서가 복원되고 원 입력digest와 실제 실행·출판output이 같은 사건으로 이어질 때 |
