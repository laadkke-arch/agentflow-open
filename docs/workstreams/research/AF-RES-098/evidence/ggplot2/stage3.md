# ggplot2 단계 ③: 두 예제·두 판의 본문, 바이트, 발행 관계

## 네 자리 판정

예측 봉인 커밋 `0df9ea9edbcee995d631eef54b65fd43f73c245f` 이후에 다음 본문·PNG·생성 규칙을 읽었다. 두 목록 예측은 **참 2/2, 오귀속 0/2, 놓친 연결 0/2, 판정 유보 0/2**다. 이는 정확 절에서의 사용 U에 관한 결과이며 신규 생성 G의 통과율이 아니다.

| 예제·판 | 생성 본문과 실제 참조 | PNG 바이트 / SHA-256 | 포함 P / 절 사용 U / 이번 빌드 생성 G |
|---|---|---|---|
| GG1 · 3.5.0 | [aes Examples](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/aes.html#ref-examples), `img src="aes-1.png"` | 58,480 / `1b130e78c890e9e79483a6b365bad0592726da3b4627bcbe7e0299b18c3aa558` | YES / YES / UNKNOWN |
| GG1 · 3.5.1 | [aes Examples](https://raw.githubusercontent.com/tidyverse/ggplot2/3ab6b4a05b3bde422ccc9adbfd1131bbdef64a3c/reference/aes.html#ref-examples), `img src="aes-1.png"` | 58,295 / `a1f76e00ea21684e8239946149afee18e406e1f3d91bc5f1e1f33e205e27e854` | YES / YES / UNKNOWN |
| GG2 · 3.5.0 | [colour/fill/alpha Examples](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/aes_colour_fill_alpha.html#ref-examples), `img src="aes_colour_fill_alpha-1.png"` | 17,646 / `5c79c37e0d2755127c3e63bd435526bac448df2875d7b26db368fd6c2894de84` | YES / YES / UNKNOWN |
| GG2 · 3.5.1 | [colour/fill/alpha Examples](https://raw.githubusercontent.com/tidyverse/ggplot2/3ab6b4a05b3bde422ccc9adbfd1131bbdef64a3c/reference/aes_colour_fill_alpha.html#ref-examples), `img src="aes_colour_fill_alpha-1.png"` | 16,971 / `8dd7c598a0f2405f8b3a303ca004e176e8d1d31da6e7709a3a25d3ac02a70684` | YES / YES / UNKNOWN |

파일별 실제 원주소·소스 URL·본문 지문·세 판정은 [lineage.csv](lineage.csv)에 있다. 모두 HTTP MIME `image/png`, PNG signature, 실제 크기 **1400×866**이다. 표시 속성은 700×433이다. 네 HTTP 응답에 리다이렉트는 없었고, payload에서 계산한 Git blob SHA가 해당 발행 트리의 그 경로와 일치했다. 실제 PNG 네 개를 이미지로 열어 산점도·막대그래프를 직접 확인했다. 예제 실행은 하지 않았다.

## 정확한 판과 절

날짜만으로 선택했던 새 발행 커밋 `3ab6b4a05b3bde422ccc9adbfd1131bbdef64a3c`의 배포 메시지는 v3.5.1 소스 `8fa3974166aa998f1c61ae77e67886bbb94d8065`를 지목했다. 두 새 HTML의 `small[title="Released version"]`은 3.5.1이다. 이전 두 HTML은 3.5.0이다. 다른 곳의 3.5.0 문자열을 현재판 표시로 혼동하지 않았다. 표본 교체는 없었다. [publication-confirmation.json](publication-confirmation.json)

두 판 모두 `base` 요소가 없으므로 절을 담은 HTML 원주소의 디렉터리가 상대 URI 기준이다. `h2#ref-examples`가 속한 section div 전체에서 `img/src`, `srcset`, `picture/source`, href, data, 내장 data URI, inline SVG, script를 확인했다. GG1에는 img 5개, GG2에는 18개가 있고, source/picture/figcaption/inline SVG/script/data URI는 모두 0개였다. img에는 srcset이 없다. 선택된 첫 그림은 문서 순서상 동일 위치이며 파일명도 유지됐다. 본문 anchor와 API 도움말 링크는 그림 자원으로 세지 않았다. **이 네 절에서의 범위**이며 전체 사이트에 JS나 내장 자원이 없다는 주장이 아니다. [audit.json](audit.json)

소스는 두 태그의 `R/aes.R` 45–64행과 `R/aes-colour-fill-alpha.R` 55–61행에서 확인했다. 전자는 `mpg`의 displ/hwy를 그리는 첫 출력, 후자는 `mtcars` factor(cyl)의 기본 막대그래프다. 소스 첫 예제와 생성 본문의 순서가 대응한다. `aes-colour-fill-alpha.R`은 두 소스판에서 **파일 전체 바이트가 동일**하지만, 그 판의 두 PNG는 달랐다. 이름·동일 예제 소스만으로 출력 바이트를 예상할 수 없다는 보조 근거다.

## 같은 이름인데 무엇이 달랐나

GG1·GG2 모두 전체 PNG SHA뿐 아니라 연결된 IDAT SHA와 디코딩 RGBA SHA도 바뀌었다. 동일한 표의 항목과 도표 관계를 보여도 픽셀 단위 차이가 존재한다. 이 조사에서는 그 차이를 특정 폰트·R·ragg 판에 인과 귀속하지 않았다. 단순한 metadata-only 변경이라고 부를 수도 없다. [png-comparison.json](png-comparison.json)

`pkgdown.yml`은 이전판 pkgdown **2.0.7**, pandoc **2.19.2**, last_built **2024-02-23T09:37Z**이며 새판은 pkgdown **2.0.9**, pandoc **3.1.11**, last_built **2024-04-23T10:23Z**다. 이는 문서 생성 환경의 일부 표지다. PNG 생성 실행·정확한 의존성 집합·출력 digest가 담긴 job 기록을 대신하지 않는다.

## 빌드·배포·캐시를 나눠 읽은 결과

두 소스 태그의 [pkgdown workflow](https://raw.githubusercontent.com/tidyverse/ggplot2/8fa3974166aa998f1c61ae77e67886bbb94d8065/.github/workflows/pkgdown.yaml)는 동일한 바이트다. release-published 이벤트를 받고 `build_site_github_pages(new_process=FALSE, install=FALSE)`로 만든 `docs`를 JamesIves deploy action **v4.4.1**으로 gh-pages에 보낸다. 설치 선언 `any::pkgdown` 자체는 도구판 고정이 아니다.

| 조사한 구간 | 실제 규칙 | 이 사례에 허용되는 판단 |
|---|---|---|
| [pkgdown 2.0.7 build-github](https://raw.githubusercontent.com/r-lib/pkgdown/v2.0.7/R/build-github.R), [2.0.9](https://raw.githubusercontent.com/r-lib/pkgdown/v2.0.9/R/build-github.R), 19–33행 | 로컬 빌드 목적지는 기본 `clean=TRUE`; 이후 build_site 호출 | 로컬 생성 폴더 청소와 원격 배포 브랜치 청소는 별개다. |
| [2.0.7 build-reference](https://raw.githubusercontent.com/r-lib/pkgdown/v2.0.7/R/build-reference.R), [2.0.9](https://raw.githubusercontent.com/r-lib/pkgdown/v2.0.9/R/build-reference.R), lazy 인자·out_of_date 분기 | 개별 reference 호출은 lazy 처리 가능; 전체 build_site 기본은 lazy=FALSE | 캐시 기능의 존재만으로 이번 작업이 예제를 캐시에서 재사용했다고 쓰지 않는다. |
| 같은 파일의 copy_figures, 2.0.7 199–205행 / 2.0.9 202–208행 | 소스 `man/figures`를 출력 `reference/figures`로 복사 | 예제처럼 보이는 파일도 소스 정적 자원일 수 있다. |
| workflow 39–44행 및 [deploy action README](https://raw.githubusercontent.com/JamesIves/github-pages-deploy-action/v4.4.1/README.md) 129행 | 배포는 `clean:false`; 소스에서 사라진 목적지 파일을 지우는 옵션을 끔 | 오래된 파일 잔류를 허용한다. 두 주 PNG가 잔류 파일이라는 결론은 아니다. |
| [3.5.0 소스 SHA의 Actions 질의](https://api.github.com/repos/tidyverse/ggplot2/actions/runs?head_sha=a6f1a7c845bfe056ef952b839d2fd65b888ab5cd&per_page=100), [3.5.1 질의](https://api.github.com/repos/tidyverse/ggplot2/actions/runs?head_sha=8fa3974166aa998f1c61ae77e67886bbb94d8065&per_page=100) | 두 응답 모두 HTTP 200, total_count=0 | 현재 이 질의에서 실행 레코드를 얻지 못했다. 실행이 원래 없었다거나 보존기간 때문에 지워졌다고 단정하지 않는다. |

따라서 P와 U는 각 **4/4 확인**, G는 **4/4 미확인**이다. 소스-배포 메시지와 현재 일치 바이트만으로 G를 올리지 않았다. 특정 실행 ID·입력판·출력 digest를 연결하는 공개 artifact/attestation이 발견되면 G를 재검토한다.

## 보조 사례: 과거 정적 PNG의 명시적 현재 사용

두 [홈페이지](https://raw.githubusercontent.com/tidyverse/ggplot2/3ab6b4a05b3bde422ccc9adbfd1131bbdef64a3c/index.html)는 Usage 예제에서 `reference/figures/README-example-1.png`를 참조한다. [3.5.1 README.md](https://raw.githubusercontent.com/tidyverse/ggplot2/8fa3974166aa998f1c61ae77e67886bbb94d8065/README.md) 56행은 입력 자원 `man/figures/README-example-1.png`를 명시한다. 두 소스 태그의 원 PNG와 두 발행판 PNG를 실제로 받았으며 **네 파일 모두 43,951B, SHA-256 `ac88da0d35022c2a0d37a1cc3889e49dd0e08b2364144bd3a27553e197f05cdb`**다.

위 copy_figures 규칙까지 연결하면, 이 파일은 현재 설명이 의도적으로 사용한 소스 정적 자원이라는 판단을 지지한다. 현재판 사용이 확인된 양성이지 새로 렌더링한 PNG의 증거는 아니다. 실제 해당 실행의 copy 로그는 없으므로 run-level G는 계속 UNKNOWN이다. **보조 사례이며 주 여섯 예제 분모 기여는 0**이고, 동일한 네 PNG는 자료 수에서 한 번만 센다. [static-reuse.json](static-reuse.json), [원 영수증](static-reuse-receipts.json)

## 찾지 못한 반례와 탐색 경계

두 완전 발행 트리에서 이전판 비dev 이미지·데이터 확장자 `.png/.svg/.jpg/.gif/.csv` **1,285개 경로**를 비교했다. 새판에서 사라진 이전 경로는 **0개**였다. 사라진 이름과 새 이름의 동일 blob 관계는 **0개**, 이전 blob과 동일한 새 비dev 별칭도 **0개**였다. 따라서 **이 두 트리 범위에서는 이름 변경·같은 내용 사례를 확보하지 못했다**. 두 판에 그대로 남은 reference PNG 122개는 목록 관측일 뿐, 전부 본문 사용이나 의도적 재사용을 확인한 122사례로 세지 않았다. [counterexample-search.json](counterexample-search.json)

이번 네 주 절에서는 삭제·이름 변경·외부 URL 없는 내장 data URI가 없었다. 잔류·참조 소멸의 실제 새 사건도 이 조사에서 확정하지 않았다. `clean:false` 규칙은 그 가능성의 기전이고, 094의 SVG를 새 사례로 재계수하지 않는다.

## 목적별 반환과 한계

개발자에게는 확인한 판의 Examples와 필요한 첫 PNG를 연결할 수 있다. 과거판 독자에게는 태그와 결합한 **고정 발행 HTML 원문** 및 PNG를 제공한다. GitHub raw HTML은 소스 표시이며 역사 사이트 렌더링 URL로 오해하지 않게 적는다. 발행자에게는 같은 두 주소와 source 태그/workflow를 주되, 이번 빌드가 그 PNG를 생성했다는 근거가 미확인임을 밝힌다. 단순 예제 독자에게 빌드 주소를 항상 추가할 필요는 없다.

수집 영수증은 [stage3-receipts.json](stage3-receipts.json), [supplement-receipts.json](supplement-receipts.json), [github-build-receipts.json](github-build-receipts.json)에 있다. 단계 ③의 저장된 본 수집 요청은 15회, 보조 메커니즘·홈페이지 9회, 정적 재사용 6회, build-github 2회다. 초기 탐색·검색뷰 열람은 이 범위의 요청 수에 포함하지 않는다. 그 탐색은 [exploration-log.json](exploration-log.json)에서 따로 구별한다. 사람 조작 시간은 재지 않았다.

출처 원장은 동일 source/file의 동일 바이트를 중복 제외하고, 빈 Actions 검색 결과를 본 자료 하한에 넣지 않았다. 자기 파싱·시각 확인이며 사람 독립 검토가 아니다.
