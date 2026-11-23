# pandas 자연 보고층 조사 메모

## 이 하위 조사에서 확정한 범위

정해진 순서의 30개 현재 공개 본문을 열어 코드·관측·문제·expected 절을 판독했고, 적격 17개 중 처음 세 자리 N-P1=#38928, N-P2=#39398, N-P3=#40336을 고정했다. 세 자리 모두 원저자가 입력과 어떤 출력을 게시했지만, 날짜 출력은 두 자리뿐이다. 나머지 한 자리는 실패 예외이며 다른 호출의 expected 날짜 배열을 실제 결과로 세지 않는다. 실제 로드 자료판과 입력·지역·출력을 같은 과거 프로세스에 연결한 경우는 **관측 0/3**이다. [frame.csv](frame.csv), [receipts.json](receipts.json), [summary.json](summary.json).

| 측정 단위 | 분자 / 분모 또는 수 | 범위와 한계 |
| --- | --- | --- |
| 현재 원보고 URL 추적 | 3/3 | 최초 본문판 복원은 세 자리 모두 미확인 |
| 원저자가 게시한 어떤 출력 | 3/3 | 날짜 두 건, 실패 예외 한 건; 기계 원 stdout이 아님 |
| 원저자가 게시한 날짜·달력 출력 | 2/3 | N-P2는 인쇄값은 있으나 정확 호출 연결에 내부 충돌 |
| 원 run stdout | 관측 0/3 | 붙여넣은 이슈 보고와 분리 |
| 실제 로드 tzdb판 확인 | 관측 0/3 | 모듈판 self-report나 공개 배포판과 구별 |
| 같은 실행의 입력·지역·로드판·날짜 출력 전체 결속 | 관측 0/3 | 출력 확인과 자료판 확인의 교집합도 0/3 |
| 최초 30 이슈 저작 / 그 원저자 | 30 / 28 | 탈락한 13개는 issue_scope_exclusion으로 별도 분류 |
| 선택한 원보고 사건 레코드 / 원저자 | 3 / 3 | 실제 독립 프로세스 수는 미확인 |
| 선택 본문+댓글의 고유 참가자 | 5 | 댓글만의 참가자는 4; 토론을 독립 실행으로 세지 않음 |
| 세 보기 비교 셀 | 9 | 3사례 × V0/V1/V2; 보조 이슈는 분모에서 제외 |

43개 출처 행은 30 이슈 저작과 11 공식 소스 열람, 2 배포 archive 열람을 나타낸다. 여기서 최소 독해 수는 개정·형식·멤버를 묶으면 33 계보이며, 통합 시 root가 읽은 pytz/dateutil 계보와 다시 합쳐야 한다. 모든 30 이슈가 자연 표본의 적격 보고라는 뜻은 아니다. [sources.jsonl](sources.jsonl)의 category/count_minimum/lineage_id를 함께 사용한다.

## 모집 봉인과 수정 이력

봉인 시각은 2026-11-23T05:09:55.123Z이고, 첫 본문 획득은 그 뒤다. 초기 여섯 키워드 검색은 timezone 63, time zone 8, tzdata 7, DST 21, offset 42, daylight 4건을 반환했다. 이 숫자는 합집합 크기가 아니다. 키워드 없는 월별 제목 1,899개를 2021-01~10월까지 대조해, compound/substring 때문에 누락됐던 #38928, #39097, #40367, #40948, #41843, #41847을 **본문 열람 전에** 더했다. 첫 30번째 기준일은 2021-10-22에서 2021-06-10로 앞당겨졌다. 2021~2025 전체 이슈를 전수 조사했다는 주장은 하지 않는다. 먼저 확보한 키워드 목록의 30번째가 10월이어서 그 월까지 제목을 대조한 것이다. [keyword-titles.json](keyword-titles.json), [title-census.json](title-census.json), [frame-seal.json](frame-seal.json).

connector 페이지 URL을 조립할 때 최초 `page=1` 치환이 `per_page=100` 부분에 걸려 중복 첫 페이지를 받은 오류가 있었다. 중복을 버리고 `&page=`만 수정하여 누락 페이지를 다시 받았으며, 월별 total_count와 고유 행을 대조했다. 오류와 수정 요청 URL은 frame-seal의 checks/corrections에 보존했다. 결과 본문을 보고 표본을 교체한 일이 아니다.

#38928은 직접 입력 EDT가 출력에서 naive로 바뀐 사실과 경고를 함께 보고했으므로 사전 기준상 적격으로 보았다. 이를 “경고만의 질문”으로 엄격히 제외하는 민감도에서는 첫 세 자리가 #39398/#40336/#40817이 된다. 이 대안은 별도 보존하며 본 표본을 바꾸지 않는다. 원래 제목도 #38928은 BUG:, #39398은 짧은 freq 제목에서 바뀐 기록이 있어, 현재 제목 프레임을 최초 제목 프레임으로 부르지 않는다. [timeline-evidence.json](timeline-evidence.json).

## N-P1 — 약어를 잃은 출력은 자료판을 가리키지 않는다

원 URL은 [pandas #38928](https://github.com/pandas-dev/pandas/issues/38928)이며 nabelekt가 2021-01-03T19:08:29Z에 생성했다. 실행 UTC는 미확인이다. 본문은 2020-10-19의 18:58:20 EDT와 16:45:33 EDT 문자열을 CSV에서 읽어 `pd.to_datetime(df['datetime'])`으로 변환하고, 같은 벽시계 시각의 naive 출력을 게시한다. 경고의 모듈 경로는 dateutil/parser/_parser.py:1218이다. 선언 환경은 pandas 1.2.0/Python 3.7.3이며 dateutil 판은 없다. [receipts.json](receipts.json)의 R-N-P1-body.

이 기록의 “EDT”를 America/New_York와 UTC−04로 보정해서는 안 된다. IANA 지역을 특정하지 못하며, 출력에는 offset이 없다. 공식 dateutil 2.8.1의 `_build_tzaware`는 tzinfos, time.tzname에 있는 로컬 이름, 수치 offset, 알 수 없는 약어를 각각 나누고, 마지막 경우에 경고와 naive 반환을 한다. 따라서 여기서는 특정 tzdb 파일을 조회했는지도 입증되지 않는다. 같은 약어가 다른 호스트의 time.tzname에 들어 있다면 다른 경로가 가능하다는 것이 코드에서 나온 반증이다. [고정 parser 1183–1221행](https://github.com/dateutil/dateutil/blob/fc9b1625ebc729f01e449879b6b140abd12ae621/dateutil/parser/_parser.py#L1183-L1221), [official-evidence.json](official-evidence.json) S-P-L07.

관측 출력만 보면 직접 읽은 dateutil 2.7.5/2.8.0/2.8.1 모두 같은 경고+naive 반환과 양립한다. 원 스택의 1218행은 읽은 세 정식 소스 중 2.8.1과 맞고 나머지는 1204/1206행이지만, 이 제한 집합이나 행 번호는 수정된 소스를 포함한 정확판의 유일 지문이 아니다. PyPI 최초 공개일은 세 후보 모두 보고 이전임을 확인했다. [candidate-editions.csv](candidate-editions.csv), [dateutil-publication-evidence.json](dateutil-publication-evidence.json).

유지보수자 mroeschke의 [댓글 753711091](https://github.com/pandas-dev/pandas/issues/38928#issuecomment-753711091)은 dateutil 경로를 설명하며 별도 실제 재현 출력은 없다. 다음 필요한 공개 보관 입력은 당시 같은 실행의 dateutil 버전·파일 경로·time.tzname과 원 EDT의 의미다. 실제로 지역 자료를 조회하지 않았던 실행이라면 “사용 tzdb판” 분모 자체가 해당 없음으로 바뀔 수 있다.

허용 문장: **“2021-01-03 생성 이슈의 현재 공개 본문은 EDT 문자열을 naive 날짜로 출력하고 dateutil 경고를 냈다고 보고한다. 그 실행의 지역·UTC 순간·시간대 자료판은 미확인이다.”**

## N-P2 — 모듈판도 있고 날짜 출력도 있으나 정확 호출이 이어지지 않는다

원 URL은 [pandas #39398](https://github.com/pandas-dev/pandas/issues/39398), rwijtvliet, 2021-01-25T15:18:39Z다. 입력은 Europe/Berlin의 2020-03-27부터 네 개 현지 자정, freq D이고, 게시 호출은 `i2=i+i.freq`다. show_versions에는 pandas 1.2.0/commit 3e89b4c4b1580aa890023fc550774e63d499da25, Python 3.8.5 Windows, pytz 2020.5, dateutil 2.8.1이 있다. 명시된 offset의 양의 방향은 UTC 동쪽이다. 인쇄된 i의 첫 원소는 03-27 00:00+01, 네 번째는 03-30 00:00+02이다. [receipts.json](receipts.json)의 R-N-P2-body.

게시된 i2에는 03-30 01:00+02가 있어 달력 출력 존재 자체는 확인한다. 그러나 i2의 첫 원소가 **03-29 00:00+01**이다. 첫 i의 03-27에 한 Day를 더한 결과라면 한 날짜만 진행해야 하는데 두 날짜가 진행했다. 숨은 셀 상태·복사 오류를 임의 보정하지 않는다. phofl과 mroeschke가 설명한 24시간 경과량과 DST의 차이는 이 첫 날짜 불일치까지 해소하는 원 실행 로그가 아니다. [댓글 766944304](https://github.com/pandas-dev/pandas/issues/39398#issuecomment-766944304), [댓글 767041834](https://github.com/pandas-dev/pandas/issues/39398#issuecomment-767041834).

show_versions를 단순 의존 선언으로 낮춰 읽는 것도 부정확하다. matching source는 importlib로 모듈을 가져와 __version__을 읽는다. 따라서 해당 환경 점검의 모듈 self-report라는 의미는 있지만, 날짜 계산과 같은 프로세스인지, 열어 쓴 멤버가 무엇인지는 여전히 없다. 일반 지역 문자열이 pytz.timezone으로 전달되는 코드도 원 사용자의 실제 로드 관측이 아닌 조건부 추론이다. [show_versions](https://github.com/pandas-dev/pandas/blob/3e89b4c4b1580aa890023fc550774e63d499da25/pandas/util/_print_versions.py#L79-L87), [optional import](https://github.com/pandas-dev/pandas/blob/3e89b4c4b1580aa890023fc550774e63d499da25/pandas/compat/_optional.py#L49-L57), [loader 분기](https://github.com/pandas-dev/pandas/blob/3e89b4c4b1580aa890023fc550774e63d499da25/pandas/_libs/tslibs/timezones.pyx#L91-L123).

### 같은 지역 파일은 전체 판 지문이 아닐 수 있다

관련 새 후보 pytz 2020.1/2020.5의 저자 공개 wheel을 내려받아 PyPI SHA256과 맞췄고, 변환을 실행하지 않고 archive의 Berlin 멤버 바이트만 비교했다. 이 둘은 059의 고정 14파일을 재검사한 것이 아니다. 전체 archive는 다르지만 두 Berlin 멤버는 모두 **2,298 bytes, SHA256 5ee475f71a0fc1a32faeb849f8c39c6e7aa66d6d41ec742b97b3a7436b3b0701**로 동일하다. 각 공식 전체 자료판 label은 2020a/2020e다. 두 공개일 모두 원 보고 이전이다. [candidate-member-evidence.json](candidate-member-evidence.json).

이 결과는 “원 사용자 Berlin 해시가 있었다면 전체 판도 정해진다”는 첫 가설을 깨뜨린다. 현재 영수증에는 그 역사 해시마저 없다. 후보표의 2020a/e 양립은 **Berlin offset 구성 요소에 대한 제한 하한 두 판**이며, 모순된 완전 호출/출력 쌍을 두 판이 모두 재현한다는 뜻이 아니다. 후자는 숨은 실행 상태 때문에 미확인이다. pytz 2020.5라는 모듈 label만으로도 PYTZ_TZDATADIR가 다른 자료를 가리킬 수 있고, 캐시된 객체와 실제 열린 자료판은 별개다. [pytz open_resource](https://github.com/stub42/pytz/blob/76ed1585bd17a981f295336cb88233deea8cafdc/src/pytz/__init__.py#L78-L108). 공개 후보 pytz 2021.1 wheel은 2021-02-01 업로드라서 이 1월 보고의 당시 공개 집합에서 제외했다. 이는 offset 충돌이 아닌 이용 가능 시점의 배제다. [future-candidate.json](future-candidate.json).

새 분별 관측을 제안하기 전에 두 후보가 vendoring한 전환표를 직접 읽었다. 2020a Europe/Volgograd의 마지막 era는 +04로 끝이 열려 있고, 2020e는 +04가 2020-12-27 02:00s에 끝나 +03로 바뀐다. 따라서 **동일 원 실행의 2021-01-01T00:00Z/Europe/Volgograd 보관 관측**이 있다면 이 두 후보를 +04/+03로 가를 수 있다는 규칙상의 예측이다. 이번에 이 변환을 실행하지 않았고 원 사용자 출력으로도 세지 않는다. 이 관측 하나가 전체 공개판에서 유일판을 보장하지도 않는다. [2020a 2810–2811행](https://github.com/stub42/pytz/blob/164d6af6dc335c0adf6f7fa97800b6fa6d17cc9f/tz/europe#L2810-L2811), [2020e 2916–2918행](https://github.com/stub42/pytz/blob/76ed1585bd17a981f295336cb88233deea8cafdc/tz/europe#L2916-L2918), official-evidence S-P-L10/L11.

먼저 원 REPL/노트북의 전체 i/i2 상태와 실행 순번을 복원해야 한다. 그 뒤 같은 프로세스의 실제 열린 자원과 공급자 판을 조인한다. Berlin 관측을 더 모으는 것만으로는 이 동일 멤버 두 판이 갈리지 않으므로 전체 배포 지문 또는 다른 지역의 보관 관측이 필요하다.

허용 문장: **“보고에는 Berlin의 01:00+02:00 인쇄값과 pytz 2020.5 환경표가 있다. 코드와 첫 출력 날짜가 어긋나며 실제 로드 자료판도 없어, 그 판으로 그 호출을 실행한 결과라고 확정할 수 없다.”**

## N-P3 — expected 배열과 실제 예외는 다른 실행이다

[teddyward의 #40336](https://github.com/pandas-dev/pandas/issues/40336)은 2021-03-09T20:48:39Z에 생성됐다. 실패 호출의 endpoints는 2020-03-09 00:00−07과 2021-03-09 00:00−08이며 tz 인자는 America/Los_Angeles다. 수치 오프셋에서 산술적으로 얻는 UTC는 각각 2020-03-09T07:00Z와 2021-03-09T08:00Z다. 실패 호출에는 freq가 없다. 실제 게시한 결과는 TypeError이며, expected 절의 8,762개 시간별 배열은 오프셋 없는 다른 입력과 freq H를 사용한다. [receipts.json](receipts.json)의 R-N-P3-body.

환경표의 pytz 2020.1은 공개 패키지 2020a label과 연결할 수 있지만, 이 예외는 성공한 지역 변환의 지문이 아니다. 11월 같은 저자의 [댓글 958181780](https://github.com/pandas-dev/pandas/issues/40336#issuecomment-958181780)은 다른 11월 날짜와 pytz.FixedOffset(-480)/(-420)의 비교 실패를 보여 준다. 3월 환경·출력과 합치거나 같은 시스템의 변경 구간으로 묶지 않는다. [고정 infer_tzinfo](https://github.com/pandas-dev/pandas/blob/f2c8480af2f25efdbd803218b9d87980f416563e/pandas/_libs/tslibs/timezones.pyx#L304-L316)는 두 endpoint tzinfo가 다르면 거절하는 경로를 확인할 뿐, 그날 특정 지역 자료를 열었다고 증명하지 않는다.

허용 문장: **“작성자는 두 수치 오프셋 endpoint의 date_range가 예외로 끝났다고 보고했다. 아래 시간별 배열은 다른 호출의 expected 절이라서 이 실패 실행의 실제 날짜 출력으로 인용할 수 없다.”** 첫 추가 보관 입력은 원 실패 run의 traceback·endpoint tzinfo 타입·실행 키다. 성공값을 주장하려면 성공 호출 자체의 원 출력이 필요하다.

## 반례 탐색 — 선택 세 자리 밖에서 무엇을 더 읽었는가

최초 30 안의 아래 보고와 원저자/유지보수자 댓글을 열었다. 좋은 사례를 자연 분모에 편입하지 않았다. 전체 댓글 원문을 재게시하지 않고 [comment-observations.json](comment-observations.json)에 저자·게시/편집 UTC·hash·역할·확인 내용을 보존했다.

| 보조 사례 | 직접 읽은 반대 자료 | 깨지는 귀속 | 남는 한계 |
| --- | --- | --- | --- |
| A-P40915 London gap | [2021 유지보수자 03:00 재현](https://github.com/pandas-dev/pandas/issues/40915#issuecomment-818427467), [내부 hour 2→3 추적](https://github.com/pandas-dev/pandas/issues/40915#issuecomment-818460553), [2025 다른 저자 02:00 보고](https://github.com/pandas-dev/pandas/issues/40915#issuecomment-3198219419) | 같은 입력의 출력 차이가 있어도 같은 시스템의 자료판 변경 기간이라는 결론은 안 됨 | 저자·프로세스·라이브러리판이 달라 설치/재배포 영수증 필요 |
| A-P41591 자정 날짜 변경 | [원 보고](https://github.com/pandas-dev/pandas/issues/41591), [localize를 쓴 유지보수자 출력](https://github.com/pandas-dev/pandas/issues/41591#issuecomment-845452719) | 같은 표기 pytz판에서도 tzinfo 직접 대입과 localize가 서로 다른 순간을 만들 수 있어 날짜 차이만으로 자료판 변경을 말할 수 없음 | 원 프로세스의 UTC 값과 utcoffset를 먼저 연결해야 함 |
| A-P41834 공급자 차이 | [1900/2000 비교](https://github.com/pandas-dev/pandas/issues/41834#issuecomment-861501342), [1800 초 단위 비교](https://github.com/pandas-dev/pandas/issues/41834#issuecomment-861518279) | 현대 2000년의 동일 +10:30 결과로 pytz/zoneinfo 공급자도 고를 수 없음 | 다른 시대의 9:26/9:30/9:25:48 차이는 원 저자 보고; 역사 정답·정확 공급판은 별도 상류 증거 없음 |

추가로 [#41865](https://github.com/pandas-dev/pandas/issues/41865)의 +HHMM/colon 차이를 읽었다. +0930이 +09:00으로, +0545가 +05:05로 해석됐다는 원 보고는 규칙 판이 아니라 형식 파싱을 먼저 확인해야 하는 반례다. 후속 댓글은 2026년이라 모집 기간의 실행 증거로 쓰지 않았다. [#39097](https://github.com/pandas-dev/pandas/issues/39097)은 날짜는 같고 freq 메타데이터만 바뀌어 표본에서 제외했다. [#40817](https://github.com/pandas-dev/pandas/issues/40817)은 dateutil의 Santiago 파일 경로와 fold/epoch 내부 값의 불일치를 다루며 N-P1 선정 해석의 민감도 대안으로만 보존했다. 이런 반례 탐색 범위는 최초 30 이슈 및 위 7 이슈의 댓글까지이며, pandas 전체에서 모든 반례를 찾았다고 주장하지 않는다.

## Q1–Q5·Q7의 현재 답과 뒤집힐 조건

**Q1.** 세 선택 본문은 원저자 보고 O-R이다. 기계 원 stdout은 관측 0이다. N-P3 expected를 제외하고 N-P2 인쇄값 존재와 호출 결속 실패를 동시에 보존한다. 공개 HTML 세 건과 timeline 세 건을 열었지만 최초 본문 내용은 복원하지 못했다. 추정 edits 경로 세 건은 404였다. HTTP 200 HTML의 bodyVersion과 수신 hash는 현재 판 지문이지 과거 최초판의 증거가 아니다. [edit-history-attempts.json](edit-history-attempts.json), [issue-html-edit-check.json](issue-html-edit-check.json), [timeline-evidence.json](timeline-evidence.json). 판정이 바뀌려면 원 body edit diff/보관 snapshot 또는 원 run 로그가 있어야 한다.

**Q2.** N-P1은 절대 순간·지역 미확인, N-P2는 출력의 offset으로 순간을 읽을 수 있으나 코드/첫 날짜가 충돌, N-P3은 실패 endpoints의 UTC는 산술적으로 연결되지만 날짜 출력은 없다. 과거 날짜를 보이게 만드는 코드 블록이 항상 한 실제 호출의 영수증은 아니다. 단순 source 버전 탐색보다 먼저 원 셀 실행 순서·입력 표현·offset 방향을 확인해야 한다. 원 셀 전체를 확보하면 N-P2 충돌이 풀릴 수 있다.

**Q3.** 선언, 모듈 self-report, 배포 label, actual loaded member를 나눴다. N-P2/3 show_versions는 실제 모듈 버전 속성을 조회하도록 구현돼 있지만 같은 날짜 셀 프로세스의 근거는 없다. pytz 환경변수 override와 캐시 분기는 배포판 label만으로 사용판을 확정할 수 없다는 직접 반대 원전이다. 같은 run의 열린 파일 경로/내용과 입력·출력이 조인되면 판정이 강해진다.

**Q4.** N-P2의 Berlin 구성 요소만으로는 직접 읽은 전체 자료판 최소 두 개가 남고, 해당 지역 멤버 hash도 둘을 제거하지 못한다. 전체 판 후보의 완전 열거는 미실시이므로 유일판 선언을 보류한다. N-P1의 parser 행 번호는 후보를 좁히지만 tzdb판을 주지 않는다. N-P3 예외는 지역 규칙 판별 관측이 아니다. 판별력이 있는 다른 지역/순간은 후보 전환행을 먼저 읽고 제안했다.

**Q5.** 선택 세 자리에서 동일 시스템·동일 입력·변경 영수증을 갖춘 before/after는 관측 0/3이다. #40915에서 2021/2025 서로 다른 결과는 확인했지만 다른 참가자의 프로세스다. “2021~2025 사이 이 사용자 시스템의 자료판이 바뀌었다”는 문장은 허용하지 않는다. 공개 업로드 시각은 다운로드 가능성만 주며 수신/설치 영수증과 다르다. 같은 시스템의 이전 마지막값과 이후 첫값, 그 사이 설치/재배포를 잇는 기록이 나와야 변경 구간을 좁힐 수 있다.

**Q7.** V0→V1에서 N-P2/3 두 건은 공개 패키지 label의 2020e/2020a 대응이 추가되지만 역사 로드판 귀속은 0→0이다. V2에서는 날짜 출력 두 건과 실패 출력 한 건의 성격을 분리하고, N-P2 과잉 연결을 거절한다. 과거 전체 실행 귀속은 계속 0이다. 사용자는 “저자가 이렇게 보고했다”, 유지보수자는 “이 호출/분기가 관련될 수 있다”, 배포 담당자는 “이 공개 파일은 이 자료판 label을 갖는다”, 감사 설계자는 “같은 실행 join이 없어서 사용판은 미확인”을 각각 말할 수 있다. 네 관점이 같은 모듈 label에 다른 증거 강도를 요구한다. [views.csv](views.csv).

## 추가 열람 비용의 분리

세 보기는 표본 선정 후의 정보 공개 단계 비교다. 첫 30본문은 적격 여부를 판정하려 이미 읽었으므로, V0/V1에서 입력·출력 칸을 가린다고 그 본문을 실제로 나중에 처음 읽은 것이 되지는 않는다. V0에는 선택 본문 요청 3회, V1에는 사례 전용 새 URL 0회, V2에는 댓글·timeline·HTML·실패 edits 12회와 #39398 댓글 도구 중복 열람 1회가 기록되어 있다. 합계는 16회 요청, 성공 13회, 실패 3회다. URL 고유 수는 15이며 V2의 의미는 추가 원문 및 이미 받은 본문의 재검토다. 단계별 숫자를 일반적인 사용자의 탐색 비용으로 외삽하지 않는다. [views.json](views.json). 최종 감사에서 N-P2 원 본문을 한 번 더 열어 코드 한 Day와 두 날짜 진행의 충돌을 재확인했다. 이는 새 저작이나 새 URL이 아니며 보기 비교 밖의 검증 비용 1회다. 따라서 이 최종 재열람까지 포함한 선택 사례 요청은 17회(성공 14, 실패 3)다. [final-recheck.json](final-recheck.json).

공통 조사에서는 공식 코드 11회, tag/ref/commit metadata 12회, GitHub compiled member 실패 2회, 두 새 wheel+그 metadata 4회, 미래 pytz metadata 1회, dateutil 공개일 metadata 3회가 원장으로 고정돼 있다. 합계 **기록된 33회**이고 V1의 사례별 0과 별개다. 이는 기록된 공통 원자료 요청의 수이며 최초 탐색 overhead 전부의 정확 총량을 주장하지 않는다. connector 반환 문자열 길이를 HTTP bytes로 바꾸지 않았다. 직접 HTTP wheel 요청의 bytes/hash만 실제 수신값이다. [official-evidence.json](official-evidence.json), [candidate-member-evidence.json](candidate-member-evidence.json), [dateutil-publication-evidence.json](dateutil-publication-evidence.json).

## 검사·재개와 이 하위 결과의 한계

이 하위 조사자는 새 날짜 변환을 실행하지 않았다. 직접 실행한 것은 HTTP 획득, hash 대조, archive 멤버 추출/바이트 비교와 JSON/CSV 원장 일관성 검사다. 이는 역사 사용판의 재현 검사가 아니다. 통합 session check/Git commit은 root의 역할이다. 원문 전체 임시 body/comment 캐시는 최소 관측·메타데이터·hash 원장으로 축약 후 삭제했고, 커밋 산출물은 report-context/comment-observations/receipts를 사용한다.

실제 검사 명령은 `python -B docs/workstreams/research/AF-RES-063/evidence/pandas/validate.py`이며 제공된 Linux Python에서 19/19 항목, exit code 0이었다. 검사 시각·입력 파일 SHA256·미실시 범위는 [validation.json](validation.json)에 남겼다. 이 영수증을 원격 고정 커밋 재열람이나 전체 session check의 대체로 사용하지 않는다.

재개자는 [receipts.json](receipts.json)과 [official-evidence.json](official-evidence.json)을 먼저 연다. 새 원고에 단순 제품 문장만 필요하다면 각 case의 allowed_sentence를 사용한다. exact loaded edition이나 변경 기간을 더 강하게 말하려면 아래 원 자료 결손을 먼저 채워야 한다.

| 가장 중요한 약점 | 영향받는 주장 | 직접 근거·위치 | 다음 최소 조사 / 판정 변경 조건 |
| --- | --- | --- | --- |
| 최초 본문판과 실제 실행 UTC를 복원하지 못함 | “그 공개일에 정확히 이 출력이 실행됐다” | issue-html-edit-check / timeline-evidence / selected receipts | 원 body edit diff·당시 archive 또는 원 run timestamp 확보 |
| N-P2 코드와 첫 날짜 출력 충돌, 모든 사례의 실행·로드 join 없음 | “이 호출을 그 자료판으로 실행했다” | #39398 body i/i2, receipts N-P1..3 | 원 셀 실행순서·프로세스 키·열린 자원 영수증 확보; 세 요소가 같은 실행이면 귀속 재평가 |
| Berlin 멤버가 여러 전체 판과 동일하고 공개판 열거가 제한됨 | “멤버 해시/한 offset이면 전체 자료판이 유일하다” | candidate-member-evidence, tz/europe Volgograd 두 고정판 | 같은 원 실행의 전체 배포 지문 또는 판별 지역/순간 보관 출력, 이후 후보 전수 범위 확장 |

