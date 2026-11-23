# ggplot2 단계 ①: 이전 판과 두 예제 고정

## 선택

공식 GitHub 릴리스 목록의 `published_at`을 기준으로 2023–2025의 첫 안정 `x.y.0`은 **3.5.0**, 다음 첫 같은 계열 패치는 **3.5.1**이다. 공개일은 각각 **2024-02-23T09:33:36Z**, **2024-04-23T10:21:20Z**다. 3.4.0은 2022년에 공개됐고 2023의 3.4.1–3.4.4는 패치이므로 제외한다. CRAN 날짜는 공식 changelog에서 각각 2024-02-23/2024-04-23으로 교차 확인했다. GitHub/CRAN 공개시각을 같은 사건이라고 합치지 않는다.

- 목록: <https://api.github.com/repos/tidyverse/ggplot2/releases?per_page=100>
- 릴리스: <https://github.com/tidyverse/ggplot2/releases/tag/v3.5.0>, <https://github.com/tidyverse/ggplot2/releases/tag/v3.5.1>
- 이전 소스 태그: `a6f1a7c845bfe056ef952b839d2fd65b888ab5cd`
- 이전 공식 gh-pages 발행판: `392175bbb00b04025aa5d17a0c18b3896adeb40f`, 2024-02-23T09:46:05Z. 배포 커밋 문구가 위 소스 SHA를 지목한다. 이 문구만으로 각 PNG의 새 생성은 증명되지 않는다.
- 이전 `pkgdown.yml`: pkgdown 2.0.7, pandoc 2.19.2, `last_built: 2024-02-23T09:37Z`.

버전 경로 `https://ggplot2.tidyverse.org/3.5.0/reference/index.html`은 이 세션의 사전 탐색에서 HTTP 404였다. 성공한 공식 **발행 트리** 경로를 사용했다. HEAD를 향한 각 페이지의 source 링크를 역사 소스판이라고 사용하지 않는다.

## 모집틀

이전 발행 커밋의 재귀 트리는 `truncated=false`, 항목 3,556개다. 루트 `reference/*.html` **208개**를 대소문자를 유지한 상대 경로의 오름차순으로 고정했다. `/dev/` 중복 사이트·`articles/`는 이번에 명시된 reference 모집틀 밖이다. 모든 후보 경로와 순위는 [frame.csv](frame.csv)에 있다. 첫 두 적격 페이지가 나온 뒤 나머지는 `not_opened_after_first_two`로 남겨, 열지 않은 본문을 배제 판정으로 바꾸지 않았다.

| 순위 | 상대 경로 | 이전 본문에서 읽은 내용 | 판정 |
|---|---|---|---|
| 1 | reference/absoluteGrob.html | Usage와 Details, Examples 없음 | 제외 |
| 2 | reference/add_theme.html | Usage와 Arguments, Examples 없음 | 제외 |
| 3 | reference/aes.html | `h2#ref-examples`; 첫 그림 `img src="aes-1.png"` | **GG1** |
| 4 | reference/aes_.html | Life cycle, Examples 없음. lifecycle 아이콘은 예제 결과 아님 | 제외 |
| 5 | reference/aes_all.html | 텍스트 Examples, 로컬 그림 없음 | 제외 |
| 6 | reference/aes_auto.html | 텍스트 Examples 또는 사용법, 로컬 그림 없음 | 제외 |
| 7 | reference/aes_colour_fill_alpha.html | `h2#ref-examples`; 첫 그림 `img src="aes_colour_fill_alpha-1.png"` | **GG2** |

공통 `../logo.png`, favicon, 외부 Posit 로고, lifecycle 아이콘은 예제 결과가 아니므로 제외했다. 선택된 두 페이지의 실제 예제 구간을 수동으로 읽었다. GG1의 첫 그림은 `mpg` 자료의 `displ`–`hwy` 산점도이며, GG2는 `mtcars`의 실린더 수를 쓰는 기본 막대그래프다. 각 논리 자원은 **그 페이지 Examples의 첫 렌더링 그림**으로 고정한다. old 파일명 전체 목록은 [old-body-excerpts.json](old-body-excerpts.json), 정규화 경로·본문 지문·목적은 [selected.json](selected.json)에 있다.

## 열람 경계와 한계

이 단계에서 다음 판 3.5.1의 본문·PNG·배포 파일 목록·CI 기록은 읽지 않았다. 릴리스 목록/릴리스 노트에 패치 내용이 나온 것은 공개일 선정 자료 노출이다. 정확한 예제의 후속 상태는 미노출이다. 본문 선택에는 이전판 7페이지를 직접 열었다. 그림 자체의 바이트는 아직 내려받지 않았다.

`stage1_collect.py`는 공식 HTML의 `h2#ref-examples`를 찾는다. 처음 로컬 파서가 `examples`만 찾는 결함을 이전판 첫 세 페이지에서 발견해 수정한 뒤 캐시된 동일 바이트를 다시 읽었다. 이 수정은 다음 판 자료를 본 뒤의 선택 변경이 아니다. 1~7번의 순서·예제 본문 판독과 공통 아이콘 제외를 수동 대조했다.

다음 단계의 최소 정보는 후속 발행 트리에서 두 **정확한 상대 경로**의 존재 여부다. 후속 발행 스냅샷을 찾을 때는 날짜·SHA만 투영하고 커밋 메시지·본문·파일 blob을 보여주지 않는 방식이 가능하다. 이 시간 기준 스냅샷을 실제 3.5.1 발행판으로 확정하는 일은 예측 봉인 뒤로 남겨야 한다. 새 판 본문을 확인한 것처럼 목록 예측에 섞지 않는다.
