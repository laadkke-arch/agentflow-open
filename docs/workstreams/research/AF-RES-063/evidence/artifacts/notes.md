# 실행물 우선 보강층 — 부분 인계

## 고정 프레임과 핵심 결과

`SCOPE.md`의 판정 규칙을 적용한 뒤 실제 날짜변환 출력으로 배정할 본자리 E-P1, E-P2, E-M1, E-M2는 **0/4**다. 이는 네 실행이 없었다는 결론이 아니라 출력 조건을 만족한 원기록을 확보하지 못했다는 결과다. pandas의 실제 원 CI 15건은 추적 가능하지만 당시 날짜 출력·로드한 자료판·둘의 동시 확보는 각각 관측 0/15다. Moment는 조회 가능한 원 실행 메타데이터가 관측 0이며 역사 전체 실행 수는 미확인이다.

먼저 2021–2025의 두 저장소 Actions를 월별로 조회했다. pandas는 59개월 0, 2025-12월만 1,150건이었고 Moment는 60개월 모두 0이었다. 월별 원질의와 열람 시각은 `actions-2021.json`, `actions-2022-2023.json`, `actions-2024-2025.json`에 있다. GitHub의 1,000건 페이지 상한을 넘는 12월은 **로그 열람 전에** 구간을 나눴다. 2025-12-01..15는 0, 16..23은 처음 응답178, 두 번째 페이지 응답177이었다. 확인 가능한177건 중 이름/경로 필터 적격60건을 날짜·run ID로 정렬해 최초15개를 먼저 고정했다. 이 작은 목록의 총수 변동 원인은 미확인이며 삭제나 특정 보존기간이라고 단정하지 않는다. 이후 12-23 07:00Z까지의 한 페이지40건에서 같은 최초15개가 다시 나왔다. 선정은 바꾸지 않았다. [봉인](frozen-pandas-runs.json) · [작은 구간 재대조](run-details-and-check.json)

15건은 2025-12-22 18:51:03Z부터 12-23 06:57:27Z까지이며 문서 빌드12건, wheel 빌드3건이다. 성공11, 실패1, 취소1, skipped2를 모두 유지했다. 원run15, commit13, triggering account8, job68을 구별한다. wheel run20450788866은 wrapper 첫 페이지30 jobs에서 멈추지 않고 per_page100으로50 jobs를 확인했다. 성공·실패 여부를 보고 선택하지 않았다. [프레임](frame.csv) · [run 세부사항](run-details-and-check.json)

## 원문·입력·로드·출력의 연결 상태

각 run의 원 metadata, jobs, artifacts, 전체 로그 archive URL을 직접 열었다. 13개 archive는 HTTP410, skipped2개는404였다. artifacts는15/15 빈 목록이다. 최초4건은 job별 로그도 별도로 열었으나 모두410이었다. HTTP410은 해당 URL에서 원 로그를 받을 수 없다는 직접 증거다. 정확히 언제, 누가, 어떤 보존 정책으로 삭제했는지는 그 응답만으로 알 수 없다. skipped404는 실행 로그가 만들어지지 않은 가능성과 만료를 혼동하지 않는다. [실패 영수증](pandas-log-attempts.json) · [job별 재시도](run-details-and-check.json)

첫 run의 head SHA `554f9c61deef5d32dd07b6274bac9838d0f308c8`에 있는 문서 workflow는 `doc/make.py` 실행과 website artifact의 retention-days14를 선언한다. 같은 트리 environment.yml은 Python3.11, pytz>=2024.2, pip tzdata>=2023.3, python-dateutil을 선언한다. 이는 정확한 해석 환경의 설치 영수증도, 실제 선택한 공급자도 아니다. 성공한 문서 빌드에서 날짜별 예제가 실행됐을 가능성은 있어도 stdout/환경 artifact 없이 한 입력·자료판·출력을 결합하지 않았다. release 파일이나 현행 HTML의 숫자를 과거 CI 출력으로 채우지 않았다.

원기록 URL 예: [최초 run20441074943](https://github.com/pandas-dev/pandas/actions/runs/20441074943), [첫 실패 run20445440404](https://github.com/pandas-dev/pandas/actions/runs/20445440404), [wheel run20450788866](https://github.com/pandas-dev/pandas/actions/runs/20450788866). 원 실행 키는 repository/run_id/attempt1이며 publication created_at, run_started_at, updated_at을 분리했다. updated_at은 2026년이므로 원 계산시각으로 사용하지 않는다.

## Moment의 별도 원자료·아카이브 시도

2021 고정 README `feaf90069c469822b2cee35d9d0cd37560d351ef`는 Travis를 가리켰고, 2025 고정 README `0efed482fe458bb96695bf2856ed7862e4fe50cd`는 GitHub Actions를 가리킨다. 원 Travis주소는 앱 주소로 이동해 HTML shell만 반환했다. 옛 API는404, 이전된 공개 API는 count0/is_last=true, 원 build URL에 대한 2021–2025 Wayback CDX 목록도0이었다. 원페이지 shell에서 build ID가 발견되지 않았다. 각각 원주소·시각·HTTP·수신바이트·SHA가 있다. 이는 과거에 실행이 없었다는 증거가 아니다. [다른 원자료 조회](fallback-http.json)

공식 README의 Documentation→공식 문서 source 고정판 `c133e6339ba7c929e718d38845458b64438ef3fe`에서 site home/index, 사용 진입·Node·guide intro·bundle loading을 읽었다. 이 정해진 진입문서와 공개 tree에서 보관 실행 노트북의 저자 목록을 찾지 못했다. 전체 인터넷 또는 과거 모든 개정의 링크가 없다고 주장하지 않는다. README와 site home의 날짜값은 코드의 설명용 주석이며 원run stdout으로 산입하지 않았다. Node 문서는 기본 모듈 외에 축소 bundle·데이터 없는 core·customData 경로가 있음을 확인해 준다. 따라서 패키지판 표기만으로 로드 자료판을 결정할 수 없다. [읽은 문서 위치](document-reads.json)

## 보조 반례 A-PW1 — 저장 output이 있어도 공급자는 별개

고정 pandas community tutorials가 직접 링크한 Stefanie Molin의 pandas-workshop 원저작을 열었다. 저자는2021 첫 워크숍 발표를 명시하며 section1 최초 commit은2021-05-20이다. 본문은2025-11-01 고정 SHA `cbe8e758d22a6bbf0278fd5c99e96ad5dfdfe35d`에서 읽었다. 이것은 만료된 최초15개를 대체하지 않는 **보조 행**이다. [원 저자 notebook](https://github.com/stefmolin/pandas-workshop/blob/cbe8e758d22a6bbf0278fd5c99e96ad5dfdfe35d/notebooks/2-data_wrangling.ipynb)

`2-data_wrangling.ipynb`의 zero-based cells14/45/58/69에는 각각 execution_count6/20/25/30과 저장 execute_result가 있다. 날짜 문자열의 dtype 변환, CSV 날짜 파싱, year와 월·일 조합의 변환,2019 공휴일 날짜의 출력이 실제 파일의 outputs 배열에 남아 있다. cell58은2019-09-12,2020-03-05 등 달력 날짜를 반환한다. UTC순간이나 지역 ID는 없으며 timezone-naive 날짜 변환이다. 날짜 모양의 출력이라고 언제나 시간대 DB를 사용하는 것은 아니다.

environment.yml/requirements.txt에는 pandas2.3.0이 명시돼 있고 notebook language_info는 Python3.13.3이다. 별도 `0-check_your_env.ipynb`는 package별 OK stdout을 보존한다. `check_env.py`는 import한 모듈의 `__version__`을 환경 제약과 비교하지만 성공 때 실제판을 출력하지 않는다. 더구나 검사 notebook과 변환 notebook을 같은 kernel/session으로 묶는 UUID·시각·로드 경로가 없다. 현 고정판의 코드/환경만으로 과거 저장 셀의 실행환경을 재구성했다고 하지 않는다. [보조 증거](notebook-supplement.json)

## Q별 해석과 세 보기

- **Q1:** 원run metadata는 빌드 사건의 증거이며 날짜 stdout과 구별한다. notebook의 outputs 배열은 보존된 셀 출력이지만 서명된 실행 영수증은 아니다. README 주석은 expected/example이다.
- **Q2:** 본 보강 사례는 원 입력이 없으므로 UTC/지역/단위를 미확인으로 둔다. A-PW1은 timezone-naive로서 UTC·offset 귀속은 해당 없음이다.
- **Q3:** first-run environment constraints와 notebook 요구판은 선언(D)이다. 동일 run 설치(I)·로더(L)·멤버(H)가 없다. 별도 환경 검사의 OK를 다른 notebook에 붙이지 않는다.
- **Q4:** 원 입력·출력이 없는 자리에서 후보판 전체를 새로 나열하는 것은 판별 정보를 늘리지 않는다. 후보집합은 미확인/해당 없음으로 남겼다. A-PW1은 tzdb가 실제로 호출됐는지조차 해당 셀에서 확인되지 않는다.
- **Q5:** run metadata의 updated_at이 실행시각보다 늦어도 설치판 변경의 두 관측이 아니다. 동일 시스템·동일 입력의 전후 출력과 설치 연결 영수증이 없다.
- **Q7:** V0의 run 시간·commit, V1의 고정 workflow/environment, V2의 원 jobs/artifacts/log 시도를 더해도 본자리4개는 확정 귀속으로 승격하지 않는다. A-PW1에서는 V2에서 보존 날짜 출력만 확인되며 로드판은 미확인이다. [세 보기](views.csv) · [후보판 경계](candidate-editions.json)

검색 비용은 공개 API 응답/도구 열람 건수 원장과 직접 HTTP 수신바이트를 구별한다. 커넥터 반환문자수를 HTTP bytes로 바꾸지 않았다. `search-log.jsonl`은 조회를 공유그룹 E-AUDIT로 기록하므로 빈자리마다 같은120월 질의를 반복 산입하지 않는다. V0/V1/V2는 실제 확보한 증거를 순차적으로 노출하는 보기이며 새 증거를 가상으로 채우지 않았다.

## 수용과 남은 검사

직접 읽은15개 CI의 원metadata는 사건 수로 보존하되, 엄격한 원stdout/저장 output 최소수에는 산입하지 않았다. 보존 출력이 있는 독립 저자 저작은 A-PW1·A-PW2 두 건이다. A-PW1은 **기간 내 공개 저작에 보존된 날짜 출력1건**이며 셀의 실제 실행시각은 **미확인**이다. A-PW2의 출력은2020판에도 존재한다. 따라서 두 자료의 실제2021–2025 실행 확정 수는 **미확인**으로 두고, 기존의 엄격 하위분모 **1/4** 표현은 철회한다. 다른 에이전트의 독립 자료와 계보를 대조해 저작 독해 수를 합산할 수 있으나 실행시각 확인 수와 같게 취급하거나 같은 워크숍의 여러 notebook을 여러 저작으로 세면 안 된다. `sources.jsonl`의 count_minimum=true는 공식 원전3계보+저자 보존 출력2계보이며 run metadata15는false다. 본 보강 출력 자리0/4와 같은 실행의 사용판·출력 동시 확보0/4는 변하지 않는다. [수용 수치](acceptance-artifacts.json)

현재 셀프체크 주체는 execution_artifacts 조사 에이전트다. 새 CI 실행·날짜변환 재실행·로그 재생은 미실시이며, 이 부재가 역사 출력 부재를 의미하지 않는다. 다음 첫 행동은 `pandas-log-attempts.json`의 최초15 run 중 하나의 당시 stdout/환경 artifact를 저자의 공개 보관 위치에서 찾는 것이다. Moment는 `fallback-http.json`에 고정한 공식 원목록의 날짜·runID가 먼저 필요하다. 작업자는 소유 디렉터리 밖을 쓰거나 Git 커밋/공통 상태를 변경하지 않았다.


## 추가 보조 A-PW2 — 파일의 환경 표기 변경과 보존 출력은 다른 사건

통합 담당의 독립 실행 저작 추가 확인 요청에 따라, 공식 pandas tutorials의 다른 저자 원순서 첫 Julia Evans cookbook을 열었다. 원목차에서 filename에 time/date가 있는 첫 notebook(Chapter8)을 output 읽기 전에 고정했다. 최초 저작은2013, 조회한 고정판은2024-10-24 `69d3389e4d9fee6dcf8e59e4c91397e81da79163`, 해당 notebook의 마지막 수정은2024-10-22 `81ae6fbbbb0e7f86a88f40b26a37422e778e22b7`다. [사전 보조 선정](auxiliary-author-selection.json) · [직접 비교](notebook-second-author.json)

cell5의 저장 정수 입력1387295797, cell9의 unit=s 변환, cell13의 저장 날짜2013-12-17 15:56:37이 같은 notebook에 있다. requirements는 pandas2.2.3이고 kernel metadata는 Python3.9.20이다. 그러나2020 고정판 `5a9a21c5a34edb1c50465f1b4cbb9d922722198b`도 직접 열어 비교하니 **모든 저장 output이 동일**하다.2024 patch는 상대 데이터 경로와 kernel metadata(Python3.8.5→3.9.20), notebook 형식만 바꾼다. 이 데이터로2024에 pandas2.2.3을 로드해 새로 실행했다고 귀속할 수 없다. 같은 출력이 반복된다는 이유로 환경 변경이 없었다거나 있었다고 확정할 수도 없다.

A-PW2는 독립 저자의 보존 출력 원자료이자 Q5의 적극적 반례다.2021–2025 신규 실행의 입증 수나 본15개 후보·4개 빈자리에 합하지 않는다. 다음 최소 관측은 이 notebook 실행 때 실제 로드한 pandas/provider/입력digest와 kernel UUID를 출력과 함께 기록한 원 영수증이다.
