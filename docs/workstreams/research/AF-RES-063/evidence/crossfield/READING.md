# 다른 분야의 원저작 독해와 연결 실패

선정 목록은 `frame-metadata.json`에 2026-11-23 05:11:18 UTC 고정했다. 검색은 SCOPE의 쿼리 순서를 적용했다. Dataverse의 공백 쿼리가 OR로 해석된 것을 확인하고 인용부호와 AND로 수정한 뒤 원 실행물을 열었다. Zenodo의 익명 API 상한은 25여서 25+5개를 보존했다. `sort=oldest`는 공개일 전역 정렬을 보장하지 않으므로 수집한 30개 안에서 발행일·영구 ID로 정렬했다. 전 세계 최초 적격 저작이라는 주장은 보류한다. 검색 결과만 본 항목은 직접 독해 수에서 제외한다.

## X-D1 — 러시아 경제 불확실성 복제 자료

- 원본: https://doi.org/10.7910/DVN/XAMFQK ; 고정판 V1/V2는 `dataverse-version-inspection.json`의 파일 ID·체크섬과 대응한다.
- Dataverse V1은 2022-03-16 21:26:58Z, V2는 2022-03-18 11:58:48Z. 파일 수는 5→61이지만 `U_Data.xlsx`의 ID 6100481과 MD5 `7091b83b2a4af7abcc5cac6acd7a4f80`은 같다. 현재 받은 바이트도 그 MD5와 일치했다. 이 파일 하나를 열었다는 기록으로 전체 V1/V2를 구분할 수 없다.
- `U_Data.xlsx` Sheet1 A1:J10에서 월 식별자와 저자가 출판한 숫자를 직접 읽었다. A2/B2는 Oct.92/199210, C2는 96.71812781026418이다. `RU_0_0_0_0.xlsx`의 `1.U` B4:F4는 1992-10-01과 신문별 월별 빈도다. 이는 당시 수집 시각이나 분석 실행 시각이 아니다.
- 설명의 `RU_s_LDA_VINTAGE_LEXICON`에서 VINTAGE=0/1은 축소/확장 설명어 사전의 종류다. 문자열에 vintage가 있다고 자료를 내려받은 역사적 시점을 부여하면 틀린다.
- V2의 61개 파일 목록에는 실행 코드·노트북·로그가 없다. 두 XLSX는 실제로 열었고 모든 시트 이름·크기 및 첫 시트의 앞 10행을 기록했다. 61파일 전부의 셀을 읽었다고 주장하지 않는다. 저장 숫자와 논문 분석 실행을 잇는 입력 해시·호출·런 키는 미확인이다.
- 시간대 대응: 관측월→UTC 입력/현지 날짜, 파일 ID·MD5→배포 멤버 해시, 데이터셋 V1/V2→전체 tzdb판, 실행 입력 해시→실제로 로드한 지역 파일. 동일 멤버는 전체판을 유일하게 식별하지 않는다.

## X-Z1 — 게임 엔진 스케줄링 실험의 원 결과

- 원본/고정판: https://zenodo.org/records/6532252 ; DOI 10.5281/zenodo.6532252, 1.0, 2022-05-09. 발행일은 실행일의 증명이 아니다.
- 저자 `simulation_data.zip` 78,304,329 bytes를 받아 MD5 `89a72a3ccfa50540b71ac27ecc21593f` 일치를 확인했다. 33,135 ZIP 엔트리의 목록과 노트북 24개를 조사했다. 원 코드 실행은 미실시이다.
- `input_scenario_1.txt`에는 200 frames, workers 4..20, seed 시작1/끝51, Random, FIFO 등 알고리즘이 적혀 있다. 입력 SHA256은 `e133e467b07f75052e7d9c2cf53b9c3bf1280620debe52fffea33e0a20b7c0bc`이다.
- 실제 저장 출력 `Result_1/FIFO/4/200/TXT/FIFO_NonSorted_Random_1_200_4.txt`는 200행, SHA256 `b2716d901747918b13255e5667e819c92395d9a1977501d145332596e94a9285`. 첫 행은 frame 0, duration 9378.21 microseconds, critical-path estimate 0, load 0이다. 이것은 작성자가 발행한 계산 결과이며 새 연구자 재실행이 아니다.
- `Scenario 1 - Article - Tables and plots.ipynb`의 0기준 cell4–7은 상대경로 `../Result_1/`와 알고리즘/worker/seed를 조합해 `pd.read_csv`하고 논문 표용 CSV를 만들도록 적혀 있다. 그러나 24/24 노트북의 저장 output 수는 관측 0, 모든 code execution_count는 null이다. ZIP의 생성 CSV와 PDF도 각각 관측 0이다. 따라서 논문 표의 당시 실행까지 연결됐다는 초기 기대를 철회했다.
- `requirements.txt`는 `pandas >= 1.3.2` 같은 하한이며 설치 영수증이 아니다. 기록의 Python3.8.10·pytz2019.3 표기는 선언에 해당한다. kernel 메타데이터·환경 설명을 같은 실행의 실제 import 지문으로 격상하지 않는다.
- 시간대 대응: scenario/frame/seed→정확 입력·지역·순간, raw result→당시 출력, ZIP 체크섬→보관 자료판, 코드의 read_csv→가능한 로드 경로. 누락된 것은 실제 프로세스의 입력 해시/실행 키/실행 시각이다. 관측월은 시뮬레이션 자료에서 해당 없음이다.

## A-XG9 — 같은 아카이브에 있는 서로 다른 시대의 실행

- https://doi.org/10.7910/DVN/G9QZOU 는 Iasmin Goes의 2023-03-19 복제 패키지다. 검색 중 먼저 노출됐으므로 X-D1 대신 선정하지 않고 별도 보조 사례로 남긴다.
- https://dataverse.harvard.edu/api/access/datafile/6983644 의 `replication.do` 4/13/17/21/25행은 원 데이터와 1998/2004/2018 자료를 쓰는 회귀식이다. 단순 suffix는 실제 데이터 수신 영수증이 아니다.
- https://dataverse.harvard.edu/api/access/datafile/6983627 의 `Vreeland_2008_IO.log` 4행은 2008-04-18 23:05:09 개시를 명시한다(시간대 미상). 7행은 `C:\PATH\Vreeland_2008_IO.dta`를 읽는다. 443–460행에는 원 ologit, N=694, log pseudolikelihood=-893.5787, party coefficient=.5780659가 보존돼 있다.
- 로그의 숫자와 2023 논문의 원모형 숫자가 닮아도 2023의 다른 vintage 입력을 이 2008 프로세스가 읽었다고 말할 수 없다. 2023 스크립트와 2008 로그를 이어 붙이지 않는다. 2008 실행은 본 연구의 2021–2025 시간대 표본 분모에서 제외한다.
- 최소 추가 원자료는 2023 분석의 실제 log와 입력 .dta 해시, 그 log가 고정된 코드/데이터에 대응함을 보여 주는 run 키다. 현재 서비스를 점검하거나 새 사용자에게 자료를 요구하지 않는다.

## 독해의 범위와 비용

다운로드 원장 `../root-access.jsonl`에는 URL, UTC, 응답 바이트와 SHA256을 기록했다. 단일 ZIP의 24개 노트북은 독립 저작 24개가 아니라 한 계보다. XLSX의 여러 시트도 한 저작이다. 데이터 패키지 2건과 보조 복제 패키지 1건을 독립 계보로 센다. ZIP 전체 바이트를 받았다는 사실을 모든 33,135개 멤버의 내용 독해로 세지 않는다. 저자 코드의 현재 재실행은 과거 실제 사용을 대신하지 않으므로 수행하지 않았다.
