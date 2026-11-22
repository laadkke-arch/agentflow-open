# 경로 R — 봉인 후 실제 배포 HTML 조사

6참조 / 3프로젝트. 실제 CRAN archive 78개(아카이브 목록 75개와 현재 배포 3개)를 열어 문서 상태 156개를 확인했다. knitr 26판, rmarkdown 32판, dplyr 20판이다. 열거된 판 중 접근 실패·미검사판은 0개다. 삭제됐거나 원장에 없는 판까지 완전하다는 주장은 하지 않는다. 원래 봉인된 A-R01–06은 변경하지 않았다.

현재 재사용 판정은 **유지 4/6, 교체 1/6, 보류 1/6**이다. 이 판정의 주체는 동일 연구 수집자이며 실제 독자의 판단/클릭은 관측하지 않았다. **같은 목적의 literal href 수정이 실제 배포 HTML에 나타난 참조는 3/6**이고, 이는 소스 수정 사건 2개에 연결된다. 엄격한 상류 시행→동일 목적 소비자 공개 수정의 날짜쌍은 **적격 0개**다. 조사한 6개 참조 모두 시행일 또는 같은 목적의 연결이 부족하다. 적격 조건부 분모 0은 해당 없음이며, 이를 우측 검열이나 지연 0일로 기록하지 않았다.

## 배포 경계

| 참조 | 마지막 옛판 | 열거된 CRAN 판 중 첫 새판 | 실제 관측 내용 | 원 추천 재사용 판정 |
| --- | --- | --- | --- | --- |
| A-R01 | knitr 1.29, 2020-06-23 06:20:05 UTC | [1.30](https://cran.r-project.org/src/contrib/Archive/knitr/knitr_1.30.tar.gz), 2020-09-22 16:30:03 UTC | `datatables.html`의 `http://www.datatables.net` → `https://www.datatables.net`, 같은 표 라이브러리 설명. 1.47에는 www 제거. 1.50에는 simple-datatables라는 다른 라이브러리로 예제를 바꿈. | 유지: 원 예제 배경은 DataTables. 후대의 새 라이브러리를 원 추천에 소급하지 않음. |
| A-R02 | knitr 1.29 | [1.30](https://cran.r-project.org/src/contrib/Archive/knitr/knitr_1.30.tar.gz), 2020-09-22 16:30:03 UTC | `docco-classic.html`에서 github.io → `ashkenas.com/docco/`. 실제 생성 소스는 `docco-linear.Rmd`를 읽는 classic generator. 1.46은 소개 링크 문장만 없애고 Docco 스타일 지침은 유지. | 유지: 현재 도착 본문은 해당 스타일/도구 설명. |
| A-R03 | 관측 끝의 rmarkdown 2.32까지 raw href 유지 | 없음 | 32판 모두 원 MDN 속성 URL 유지. 현재 주소는 `/Reference/Properties/page-break-after`로 redirect하며 구 속성 설명·alias가 존재. 원 2.1부터 이미 `break-after` 권장과 구 속성의 호환성 목적을 설명. | 유지: deprecated 표지만 보고 다른 속성 문서로 덮어쓰면 원 코드를 설명하지 못함. |
| A-R04 | rmarkdown 2.3, 2020-06-18 14:50:02 UTC | [2.4](https://cran.r-project.org/src/contrib/Archive/rmarkdown/rmarkdown_2.4.tar.gz), 2020-09-30 18:40:06 UTC | `pandoc.html` 자체가 사라짐. 모든 다른 compiled HTML을 조사했으나 동일 설치 문단·preview 링크 대체는 확인 못함. | 보류: 현 IDE 다운로드와 보존 앵커는 확인했으나 preview 의도와 특정 IDE/Pandoc 배포 충족은 미확인. |
| A-R05 | dplyr 1.0.1, 2020-07-31 07:00:05 UTC | [1.0.2](https://cran.r-project.org/src/contrib/Archive/dplyr/dplyr_1.0.2.tar.gz), 2020-08-18 12:30:02 UTC | `compatibility.html` 패키지 루트 `http://github.com/hadley/dbplyr/` → `https://github.com/tidyverse/dbplyr/`. 1.1.1부터 compatibility 문서는 없음. `in-packages`의 backend-redshift 코드 예제는 다른 목적. | 유지: 현재 dbplyr 패키지 루트가 후계 패키지 설명을 제공. 별도 backend NEWS 절과 혼합하지 않음. |
| A-R06 | dplyr 0.8.5, 2020-03-07 12:20:02 UTC | [1.0.0](https://cran.r-project.org/src/contrib/Archive/dplyr/dplyr_1.0.0.tar.gz), 2020-05-29 15:00:03 UTC | `dplyr.html` 예제가 NYC 2013/BTS에서 Star Wars/SWAPI로 바뀜. 원 항공통계 링크 정정이 아니라 목적 폐기. | 교체: 현재 BTS raw URL은 항공 본문 없이 국경통과 redirect payload로 끝남. 공식 2013 월별 항공자료 카탈로그를 원2013 설명과 함께 병기할 근거 있음. |

모든 경계의 중간 열거판 수와 미검사판 수는 `cases.json`의 boundaries에 남겼다. “첫”은 이 조사에서 전체 내용을 확인한 보존 CRAN 원장의 판에만 적용한다. 서로 다른 배포 채널 전체의 최초 출판이라는 뜻이 아니다. `archive_observations.jsonl`은 실제 archive/member SHA256과 원 href/관련 문장을, `editions.csv`는 156개 문서 관측을, `boundary-direct-reads.json`과 `excerpts/`는 핵심 전후 본문 바이트를 보존한다.

## 두 시계와 반례

| 소스 사건 | 소스 수정 UTC | 실제 배포 UTC | 보조 차이 | 적격 범위 |
| --- | --- | --- | --- | --- |
| [knitr 6c438873](https://github.com/yihui/knitr/commit/6c4388737598d3411abde548bac0107fbf54c790), R01·R02 | 2020-09-22 01:53:23 | 1.30: 2020-09-22 16:30:03 | 52,600초 = 14시간 36분 40초 | 동일 목적 소스→compiled HTML 배포. 2참조지만 독립 소스 사건은 1개. |
| [dplyr a28d4812](https://github.com/tidyverse/dplyr/commit/a28d481259e23f1a7c739e0ebdf873144c446524), R05 | 2020-08-12 14:47:36 | 1.0.2: 2020-08-18 12:30:02 | 510,146초 = 5.904467593일 | 동일 목적 소스→compiled HTML 배포. check_win_devel은 commit 메시지의 설명일 뿐 로그를 실행/열람한 증거가 아님. |
| [rmarkdown ef67a830](https://github.com/rstudio/rmarkdown/commit/ef67a830efb225d2d0a9f4c06a8701bab126e289), R04 | 2020-09-30 03:10:09 | 2.4: 2020-09-30 18:40:06 | 55,797초 | 문서 폐기 보조량. 동일 목적 링크 정정 지연에서 제외. |
| [dplyr fddda09d](https://github.com/tidyverse/dplyr/commit/fddda09de8f3c1c2e13090027c5f6d09684ebf98), R06 | 2020-02-22 22:56:02 | 1.0.0: 2020-05-29 15:00:03 | 8,352,241초 = 96.669456019일 | 예제 교체 보조량. 그 사이 0.8.5는 3월에 출판됐지만 여전히 NYC/BTS였다. 다음 달력순 release가 소스 수정을 포함한다고 가정하면 틀림. |

상류의 실제 시행일을 위 소스 날짜로 대체하지 않았다. Docco CNAME의 [2017년 소스 설정](https://github.com/jashkenas/jashkenas.github.io/commit/1b34ba3fdcda46dd1f6f1f18e888ad8304841ea0)은 DNS/Pages 실제 시행의 증거가 아니다. MDN의 2025-10-30 경로 이동 source-history도 실제 웹 redirect 시행과 구별한다. 소비자 merge·build·당사자 독자 관측은 모두 미확인이다.

현재 결과를 과거로 소급하면 특히 다음 판단이 틀린다.

- R03: 2020 원문이 이미 호환성용 속성과 새 속성을 구별한다. 현재 deprecated 문구는 후발 정정을 원문의 과거 의도에 추가할 근거가 아니다. 2020년 고정 MDN source도 기존 alias 설명을 확인해 준다.
- R04: [Posit 회사명 공지](https://posit.co/blog/rstudio-is-becoming-posit)는 2022년이며 RStudio IDE 이름은 유지한다고 설명한다. 소비자 설치 vignette는 2020년에 폐기됐으므로 이 공지에 대한 전파로 셀 수 없다. 현재 guide의 `rstudio-ide-oss-downloads` id는 실제로 남아 있으며 주석은 구 다운로드 절의 fragment를 보존하려는 목적을 설명한다. 앵커 존재는 특정 preview판/Pandoc 설치 성공과 별개다.
- R06: HTTP 200은 최소 목적 충족을 보장하지 않는다. 실제 2,007바이트 응답은 항공통계 본문이 없고 국경통과 쪽 JS redirect를 가진다. 원문이 지시한 downstream URL은 별도 GET에서 503이었다. 이는 연구자 관측이며 독자 실패 보고가 아니다. [2014 BTS 통계표](https://www.bts.gov/archive/publications/state_transportation_statistics/state_transportation_statistics_2014/index/chapter4/table4-07)는 DB_ID=120을 항공정시성 자료로 인용하지만, `Link=0`을 포함한 원 URL의 당시 HTTP body 캡처는 아니다.

## 원문 수·미확인·재개

`sources.jsonl`에는 177개 직접 열람/보조 상태 레코드를 남겼다. 최소수에는 **상류 원문 12개, 실제 소비자 후속 HTML 4개**만 산입한다. 나머지 전후판·동일 원고·API/HTML 표현·기술적 redirect payload·지원 metadata는 중복/보조로 구별했다. 검색 결과나 접근 실패는 `attempts.jsonl`에만 있고 최소수에 들어가지 않는다. 원 A의 6원문은 `../final/sources.jsonl`에 따로 있으므로 여기서 다시 세지 않는다.

추가 판독 비용은 `costs.csv`에 실제 archive 열람, compiled 문서 상태, 핵심 경계 재열람 수와 빈 시계 필드로 기록했다. 사람 시간이나 경제 비용으로 변환하지 않았다. 수집자는 전체 근거를 봤으므로 이 판정은 가림 실험 결과가 아니다. B 가림 판독을 위해 다른 수집자의 B 원문·결과는 아직 읽지 않았다.

핵심 재개 자료는 각 case의 `unknowns[].next_source`에 있다. 보류 R04는 왜 preview를 링크했는지 알 수 있는 당시 편집자 문장/공개 배포 HTML이 우선이다. R06의 정확 데이터 재현은 2013년 공식 월별 ZIP과 nycflights13 생성 스크립트의 별도 비교가 필요하다. 이번에는 통계 출처·연도 식별까지 확인했으며 개별 ZIP의 다운로드/내용 동일성은 주장하지 않는다.

로컬 `verify_followup.py`는 실제 cache의 archive/member/발행 metadata 해시, 봉인된 원참조 무변경, 출처 조인, 중복 원문 수와 날짜 산술을 확인한다. 검사 영수증 `verification.json`은 실행 시 HEAD와 입력 해시·종료 코드를 포함한다. 이는 동일 작업자의 재검이며 root의 원격 고정 SHA 재독과 전체 세션 `check --fetch`를 대신하지 않는다.
