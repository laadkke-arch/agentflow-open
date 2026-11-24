# AF-RES-216 | PyPI 철회 배너와 파일 메타데이터

| 판·파일 | HTML 배너 | JSON 원 플래그·사유 | Simple 원 플래그·사유 | 지문·주소 | 차이·미확인 |
| --- | --- | --- | --- | --- | --- |
| matplotlib 3.9.0 / 29 | 현재판 없음 | `false` / `null` ×29 | `false` ×29 | `77c04c3c` [H01 현재판 L5773](https://pypi.org/project/matplotlib/3.9.0/) · [V01 `/urls/0..28`](https://pypi.org/pypi/matplotlib/3.9.0/json) `25285edc` · [I01 `/files/1881..1909`](https://pypi.org/simple/matplotlib/) `39beadba` | 의미 일치. 이력 카드에 3.9.1 철회 표시가 따로 있다. |
| matplotlib 3.9.1 / 24 | Yanked, Key dates `2024-08-05T01:44:21+0000` | `true` / [원 문자열 M ×24](files.csv#L54) | [원 문자열 M ×24](files.csv#L54) | `d5720b8e` [H02 배너 L346–355·Key dates L578](https://pypi.org/project/matplotlib/3.9.1/) · [V02 `/urls/0..23`](https://pypi.org/pypi/matplotlib/3.9.1/json) `25033013` · [I01 `/files/1910..1933`](https://pypi.org/simple/matplotlib/) `39beadba` | 표시는 전체 일치. Windows wheel 0, 실제 고장 조건은 당시 원기록 참조. |
| matplotlib 3.9.1.post1 / 29 | 현재판 없음 | `false` / `null` ×29 | `false` ×29 | `55049cfb` [H03 현재판 L5725](https://pypi.org/project/matplotlib/3.9.1.post1/) · [V03 `/urls/0..28`](https://pypi.org/pypi/matplotlib/3.9.1.post1/json) `f21cee1c` · [I01 `/files/1934..1962`](https://pypi.org/simple/matplotlib/) `39beadba` | 의미 일치. Windows wheel 5, 환경별 수정 범위는 당시 시험 참조. |
| pytest 8.0.2 / 2 | 현재판 없음 | `false` / `null` ×2 | `false` ×2 | `ae57c53f` [H04 현재판 L2185](https://pypi.org/project/pytest/8.0.2/) · [V04 `/urls/0..1`](https://pypi.org/pypi/pytest/8.0.2/json) `6221b3d5` · [I02 `/files/309..310`](https://pypi.org/simple/pytest/) `9f95351f` | 의미 일치. 이력 카드에 8.1.0 철회 표시가 따로 있다. |
| pytest 8.1.0 / 2 | Yanked, Key dates `2024-03-04T15:13:02+0000` | `true` / [원 문자열 P ×2](files.csv#L86) | [원 문자열 P ×2](files.csv#L86) | `7125b026` [H05 배너 L346–355·Key dates L633](https://pypi.org/project/pytest/8.1.0/) · [V05 `/urls/0..1`](https://pypi.org/pypi/pytest/8.1.0/json) `ac505502` · [I02 `/files/311..312`](https://pypi.org/simple/pytest/) `9f95351f` | 두 사유 문자열이 정확히 같다. |
| pytest 8.1.1 / 2 | 현재판 없음 | `false` / `null` ×2 | `false` ×2 | `cf53a4d0` [H06 현재판 L2122](https://pypi.org/project/pytest/8.1.1/) · [V06 `/urls/0..1`](https://pypi.org/pypi/pytest/8.1.1/json) `02fbc945` · [I02 `/files/313..314`](https://pypi.org/simple/pytest/) `9f95351f` | 의미 일치. 플러그인별 결과는 별도 근거가 필요하다. |
| matplotlib 3.9.1 / 삭제 집단 1 | 배너 사유에 Windows wheel 삭제 | 현재 해당 객체 부재 | 현재 해당 객체 부재 | [H02 배너 L346–355](https://pypi.org/project/matplotlib/3.9.1/) · [M01 삭제 목록 L441–468](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1) | 과거 삭제 5개는 현재 88개 분모 밖이다. 개별 삭제 이벤트 시각과 당시 API 플래그는 미확인. |

| 판·분모 | 양쪽 일치 | 한쪽만·신규·삭제 | 업로드 대 조회시각 | 역사적 근거 |
| --- | --- | --- | --- | --- |
| matplotlib 3.9.0 / 29 | 29 | 0·0·0 | 2024-05-15 23:37:04.927481–23:38:15.591949Z / [V01 `/urls/*/upload_time_iso_8601`](https://pypi.org/pypi/matplotlib/3.9.0/json) 2026-11-24 21:32 UTC | [M01 본문 L144–180](https://github.com/matplotlib/matplotlib/issues/28551) 비교 시험 |
| matplotlib 3.9.1 / 24 | 24 | 0·0·0 현존, 별도 집단 1 | 2024-07-04 07:15:25.890006–07:16:41.501768Z / [V02 `/urls/*/upload_time_iso_8601`](https://pypi.org/pypi/matplotlib/3.9.1/json) 2026-11-24 21:32 UTC | [M01 삭제·결정 L441–468, L702–721](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1) |
| matplotlib 3.9.1.post1 / 29 | 29 | 0·0·0 | 2024-08-06 22:00:11.114595–22:01:24.863361Z / [V03 `/urls/*/upload_time_iso_8601`](https://pypi.org/pypi/matplotlib/3.9.1.post1/json) 2026-11-24 21:32 UTC | [M03 tag L184–189](https://github.com/matplotlib/matplotlib/releases/tag/v3.9.1.post1) · [M01 시험 L1018–1073](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1) |
| pytest 8.0.2 / 2 | 2 | 0·0·0 | 2024-02-24 22:21:27.561174–22:21:30.762987Z / [V04 `/urls/*/upload_time_iso_8601`](https://pypi.org/pypi/pytest/8.0.2/json) 2026-11-24 21:32 UTC | [M04 8.0.2 L82–89](https://docs.pytest.org/en/8.1.x/changelog.html#pytest-8-0-2-2024-02-24) |
| pytest 8.1.0 / 2 | 2 | 0·0·0 | 2024-03-03 21:23:38.040582–21:23:43.502406Z / [V05 `/urls/*/upload_time_iso_8601`](https://pypi.org/pypi/pytest/8.1.0/json) 2026-11-24 21:32 UTC | [M02 결정·캐시 로그 L227–267, L349–401](https://github.com/pytest-dev/pytest/issues/12069) · [C01 환경 L455–475](https://github.com/pytest-dev/pytest/issues/12061) |
| pytest 8.1.1 / 2 | 2 | 0·0·0 | 2024-03-09 11:51:04.858193–11:51:08.012236Z / [V06 `/urls/*/upload_time_iso_8601`](https://pypi.org/pypi/pytest/8.1.1/json) 2026-11-24 21:32 UTC | [M04 문서 일자 03-08·복원 2항목 L11–15, L66–80](https://docs.pytest.org/en/8.1.x/changelog.html#pytest-8-1-1-2024-03-08) |
| 합계 / 기존 88, 현재 88 | 88 | 0·0·0, 역사 집단 1 | UTC API 21:32:16–18, HTML 21:32:40–43 | 첫 파일별 플래그 노출 시각 미확인 |

| 사용자 목적 | 유지·경고·대체·보류 | 직접 지지하는 파일 | 경쟁 설명·반례 |
| --- | --- | --- | --- |
| matplotlib 정확 재현 | 유지+경고, Windows wheel 필요 시 보류 | [`matplotlib-3.9.1.tar.gz`](files.csv#L54)와 macOS·Linux 등 24개 [V02 `/urls/0..23`](https://pypi.org/pypi/matplotlib/3.9.1/json) | 5개 삭제와 소스 대체 경로는 [M01 L441–552](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1) |
| matplotlib 신규 범위 | 태그·Python·범위 허용 시 대체 후보, 문제 조합은 보류 | [`matplotlib-3.9.1.post1-cp312-cp312-win_amd64.whl`](files.csv#L72) 등 5개 [V03 `/urls/17` 등](https://pypi.org/pypi/matplotlib/3.9.1.post1/json) | [M01 L1032–1073](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1)의 조건부 실패 |
| matplotlib 기설치 설명 | 당시 링크 유지, 날짜 있는 경고 | [`matplotlib-3.9.1.tar.gz`](files.csv#L54) [V02 `/urls/23`](https://pypi.org/pypi/matplotlib/3.9.1/json) · [M01 삭제 해시 5개](history-deleted.csv) | [M01 L215–227](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1) conda-forge 별도 계보 |
| pytest 정확 재현 | 유지+경고, 변경 시 명시적 핀 | [`pytest-8.1.0-py3-none-any.whl`](files.csv#L86) · [`pytest-8.1.0.tar.gz`](files.csv#L87) [V05 `/urls/0..1`](https://pypi.org/pypi/pytest/8.1.0/json) | [M02 L349–401](https://github.com/pytest-dev/pytest/issues/12069) 캐시 wheel 성공과 [C01 L455–475](https://github.com/pytest-dev/pytest/issues/12061) hook 실패 |
| pytest 신규 범위 | 호환 시 대체 후보, 좁은 범위는 보류 | [`pytest-8.1.1-py3-none-any.whl`](files.csv#L88) · [`pytest-8.1.1.tar.gz`](files.csv#L89) [V06 `/urls/0..1`](https://pypi.org/pypi/pytest/8.1.1/json) | [M02 L447–478](https://github.com/pytest-dev/pytest/issues/12069) 내부 API 의존 |
| pytest 기설치 설명 | 당시 링크와 플러그인 조건 유지 | [`pytest-8.1.0-py3-none-any.whl`](files.csv#L86) · [`pytest-8.1.0.tar.gz`](files.csv#L87) [V05 `/urls/0..1`](https://pypi.org/pypi/pytest/8.1.0/json) | [M02 L349–401](https://github.com/pytest-dev/pytest/issues/12069) 설치 성공과 런타임의 별개 관측 |

위 지문은 응답 SHA-256 접두사다. 원문 M·P는 각 대상 파일의 `json_reason_raw`와 `simple_yanked_raw`에서 문자열 그대로 확인할 수 있다. HTML 비교는 고정판의 상단 배너와 현재 카드 구간을 사용했다. [files.csv](files.csv) · [API HTTP 기록](receipts/api/http.json) · [HTML HTTP 기록](receipts/html/http.json) · [1차 집계](receipts/reconciliation.json)

## Q1. 수신 범위와 고정 입력

2026-11-24 UTC 21:32:16.672877–21:32:18.135115에 PyPI의 여섯 version JSON과 두 Simple JSON을 한 번씩 수신했다. 전부 HTTP 200이며 요청과 최종 HTTPS 주소가 동일하다. version JSON은 `application/json`, Simple은 요청값 `application/vnd.pypi.simple.v1+json`과 동일했다. HTML 6개도 21:32:40.874486–21:32:43.602070에 HTTP 200이었다. 각 응답의 전체 바이트는 gzip으로 보존했다. 지문과 크기는 압축을 풀어 나온 HTTP 본문 기준이다. [V01–V06·I01/I02 상태·시간·주소·SHA-256](receipts/api/http.json) · [H01–H06 상태·시간·주소·SHA-256](receipts/html/http.json)

Simple의 API 버전은 1.4다. 같은 프로젝트에서 양쪽 API의 `X-PyPI-Last-Serial`과 본문 serial이 일치했다. matplotlib은 40979980, pytest는 42838779였다. 조회 사이의 인덱스 갱신 가능성을 검토할 때 쓸 값이며 이 수집의 원자성이나 개별 이벤트의 UTC는 미확인이다. [V01–V06·I01/I02 HTTP serial과 원본문 위치](receipts/api/http.json) · [R05 프로젝트 직렬 번호 L194–201](https://docs.pypi.org/api/index-api/#get-distributions-for-project)

## Q2. 릴리스 문맥과 원파일 필드

version JSON의 `info`에서 판 이름·버전·`yanked`·`yanked_reason`을 별도로 읽었다. 조인의 파일 값은 `urls[]` 안에 있는 `yanked` boolean과 `yanked_reason`이다. Simple의 `files[]`는 같은 파일에 대해 사유가 있으면 `yanked`를 비어 있지 않은 문자열로 반환했다. 대상 26개에 대해 JSON 사유와 Simple 문자열은 공백을 포함해 정확히 같다. 인접 62개의 원값은 JSON `false`와 `null`, Simple `false`이고 Simple에 분리된 사유 키는 없다. 실제 표본에는 키 누락, 빈 이유, Simple 무사유 `true` 사례가 없었다. [V02 `/urls/23`](https://pypi.org/pypi/matplotlib/3.9.1/json) · [I01 `/files/1933`](https://pypi.org/simple/matplotlib/) · [R01 info/urls L416–500](https://docs.pypi.org/api/json/#get-a-release) · [R02 JSON Project Detail L388–423](https://packaging.python.org/en/latest/specifications/simple-repository-api/#project-detail)

PyPI의 관리 문서는 릴리스 전체를 철회하는 UI를 설명한다. 규격은 파일 링크별 상태 표현, 철회 해제·재철회, 상태 보존이나 필터링을 하는 미러를 허용한다. 관측 6판의 전파가 파일 단위의 표현을 확인해 주므로, 다른 인덱스에서 혼합 사례가 들어오면 현재 파일 값을 판정의 근거로 둔다. 결측과 명시적 false를 구별하고, JSON의 빈 `yanked` 문자열은 형 이상으로 보류한다. HTML Simple의 빈 `data-yanked` 속성은 상태가 존재한다는 규칙을 따른다. [R02 HTML L238–251, JSON L407–411](https://packaging.python.org/en/latest/specifications/simple-repository-api/) · [R03 철회 및 미러 L95–117](https://packaging.python.org/en/latest/specifications/file-yanking/) · [R04 관리 문서 L104–134](https://docs.pypi.org/project-management/yanking/)

## Q3. 정확 키와 해시

B01 기존 88키, version JSON 88키, Simple에서 고정 6판에 속한 88키가 같다. JSON만 0, Simple만 0, 신규 0, 기존 키 양쪽 부재 0, 중복 0, SHA-256 차이 0이다. `files.csv`는 모든 파일의 0부터 시작하는 JSON Pointer, 양쪽 해시·파일 URL·정확한 이름 및 태그를 담는다. 태그 검산은 파일명과 양쪽 URL basename, version JSON의 `packagetype`/`python_version`, B01 전사를 대조했다. 플랫폼 설치 시험은 미실시다. 새 프로세스 교차 검사에서 HTML 파일별 상세표의 SHA-256도 88/88 같았다. [B01 고정 입력](https://github.com/laadkke-arch/agentflow-open/blob/1ae3b56d3f445188109c343b00a1b67516f683ce/docs/workstreams/research/AF-RES-200/releases.csv) · [전수 파일표](files.csv) · [HTML 상세표 교차 검사](receipts/crosscheck.json)

I01 원응답의 2,733개 중 82개를 채택했다. 범위 밖으로 해석한 2,641개와 1.4.3 레거시 Windows `.exe` 10개는 제외했다. I02 355개 중 6개를 채택하고 다른 판 349개를 제외했다. 3.9.1과 3.9.1.post1은 별도 키다. 잘못된 판 라우트에 동일 filename이 들어온 합성 사례에서 출처 충돌과 원래 판의 누락을 둘 다 표기했다. [I01 `/files/76..85` 및 `/files/1881..1962`](https://pypi.org/simple/matplotlib/) · [I02 `/files/309..314`](https://pypi.org/simple/pytest/) · [통제 C14–C15](receipts/controls-result.json)

## Q4. 대상 26개, 대조 62개와 삭제 집단

대상 26/26의 release 배너·양쪽 flag 의미·사유가 일치했다. 인접 62/62에서 현재판 배너가 없고 양쪽에 false가 있다. 양쪽 업로드 UTC와 Python 제약도 88/88 같다. matplotlib 표본은 `>=3.9`, pytest 표본은 `>=3.8`이다. matplotlib 3.9.1의 남은 24개에는 sdist 1개와 Windows 이외 wheel 23개가 있다. 앞판과 뒤판에는 Windows wheel이 5개씩이다. pytest 8.1.0의 wheel은 `py3-none-any`이고 sdist도 함께 철회 표시다. 범용 태그와 실제 플러그인 호환성은 별도 근거를 사용한다. [V02 `/urls/0..23`](https://pypi.org/pypi/matplotlib/3.9.1/json) · [V05 `/urls/0..1`](https://pypi.org/pypi/pytest/8.1.0/json) · [판별 집계](receipts/reconciliation.json)

M01에서 유지자가 2024-08-04T00:55:14Z 이전에 이미 삭제를 마쳤다고 보고했고 01:05:41Z에 CPython 3.9~3.12 및 PyPy 3.9의 Windows x86-64 파일 5개와 SHA-256을 열거했다. C03의 7월 8일 CI 기록에는 CPython 3.12 이름 한 개의 다운로드 및 당시 설치 성공이 있다. 현재 V02/I01/H02에는 다섯 이름이 없다. 각 파일의 정확 삭제 이벤트와 당시 플래그는 미확인이다. 과거 파일 상세 5개는 B01의 집단 1자리를 구체화하며 현재 88개 분모 밖이다. [M01 삭제 보고](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1#issuecomment-2267223102) · [M01 이름·해시 L461–468](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1#issuecomment-2267225291) · [C03 로그 L385–418](https://github.com/PyO3/maturin/issues/2141) · [삭제 파일·증거 상한](history-deleted.csv)

## Q5. 현재 표시와 당시 증거

- matplotlib 3.9.1 파일은 2024-07-04 업로드였다. 유지자 철회 결정 댓글은 2024-08-05T01:43:21Z이며 H02 Key dates의 현재 표시값은 01:44:21Z다. OS·DLL·의존 wheel이 다른 환경에서도 같은 고장이 발생하는지는 미확인이다. 8월 6일 post1 태그는 Windows wheel 오류를 고칠 목적을 명시한다. 고정 태그의 소스 diff는 Zenodo 인용·캐시 관련 3경로였다. 8월 7일 post1+nightly ContourPy wheel 수동 시험 성공과 자체 빌드 ContourPy·별도 프로그램에서의 실패가 같이 보고됐다. DLL 버전·이름·탐색 순서 가설은 경쟁 설명이다. 원 빌드와 후속 CI 로그는 F02–F04의 404로 미확인이다. [M01 결정 UTC](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1#issuecomment-2268018494) · [H02 L578](https://pypi.org/project/matplotlib/3.9.1/) · [M03 태그 L184–189](https://github.com/matplotlib/matplotlib/releases/tag/v3.9.1.post1) · [M05 태그 diff L1,43,57](https://github.com/matplotlib/matplotlib/compare/44be14cc3a866e28a9ad22f36abfe8c0623cc6ac...9c9792a66900de7740fa6428f7fe59edb5083c60.diff) · [M01 후속 시험 L1032–1073](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1#issuecomment-2273144251) · [M06 L163–191](https://github.com/adang1345/delvewheel/issues/52)
- pytest 8.1.0 파일은 2024-03-03 업로드였고, 03-04T15:12:02Z 철회 발언과 당일 15:13:02Z의 H05 Key dates가 있다. 03-09T21:51:30Z에 올라온 별도 로그는 캐시된 정확 핀 wheel에서 경고와 설치 성공을 보여 준다. 그 로그의 게시 UTC와 설치의 실제 시작 UTC는 별개다. 8.1.1 문서 날짜 03-08과 PyPI 파일 업로드 03-09도 별개다. 사용자 hook 실패 및 8.1.1에서 남은 private API 의존을 기록했다. [H05 L633](https://pypi.org/project/pytest/8.1.0/) · [M02 결정](https://github.com/pytest-dev/pytest/issues/12069#issuecomment-1976808605) · [M02 캐시 로그](https://github.com/pytest-dev/pytest/issues/12069#issuecomment-1986989847) · [C01 L455–475](https://github.com/pytest-dev/pytest/issues/12061) · [M04 L11–15, L66–80](https://docs.pytest.org/en/8.1.x/changelog.html#pytest-8-1-1-2024-03-08)

두 HTML의 Key dates 시각은 보존된 판 수준의 날짜 필드다. 최초 파일별 철회 전파와 첫 실제 경고는 당시의 인덱스 직렬 이벤트 또는 시간 표기 원응답이 있어야 확정할 수 있다. 현재 API 플래그를 과거 시점에 복사해 만든 판정은 0개다. [H02·H05 원응답](receipts/html/http.json) · [날짜 정정과 증거 범위](COUNTEREXAMPLES.md)

## Q6. 주소가 살아 있는 출판 정정

PLOS ONE 원문은 19(4) e0291840, 2024-04-03 공개다. 현재 원문에서 19(11) e0313792 정정 공고가 보이며 공고는 2024-11-08 공개다. 공고의 Reference 1이 원문을 지목한다. 편집 범위는 S1 File과 Fig 8, 관련 Results·Discussion이다. 발행 매체에서 원문과 정정 대상 부분을 함께 찾는 설계를 비교할 수 있다. 적용 목적과 날짜 기준은 편집 기록에 따르며 과학적 내용은 평가 범위 밖이다. [X01 원문 L221–234, L267–271](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0291840) · [X02 공고 L123–145, L157–165](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0313792)

## Q7. 통제와 링크 문구

20개 대조의 기대값과 실제가 일치했다. 파일 키 결측·false·true·null·비어 있지 않은 사유와 빈 문자열, 사유·digest·태그 충돌, API 한쪽 부재·신규·삭제 후보·중복과 잘못된 판의 동일 filename을 구분했다. 고정 원응답 재생과 합성 재생은 각자 새 프로세스에서 실행해 1차 결과와 바이트 단위로 대조했다. [기대·실제](receipts/controls-result.json) · [API 재생](receipts/reconcile-replay.json) · [합성 재생](receipts/controls-replay.json)

기존 잠금과 정확 핀은 원본 링크 및 해당 파일의 기록을 유지하고 철회 사유·관측일을 덧붙인다. 읽는 목적이 새 범위 설치면 범위·해시·Python·태그를 다시 적용한다. `==3.9.1`과 `==3.9.1.*`는 뒤판 수용 여부가 다르다. `==8.1.0.*`는 8.1.1을 담지 않는다. pip 24.0의 인덱스 후보 경로는 모두 철회된 적용 후보이며 핀인 경우에 그 후보를 남긴다. 기존 로컬 환경의 설명은 당시 출처와 실제 플러그인·빌드 증거를 우선한다. 독자가 사용 중인 클라이언트나 미러의 지원과 설치 성공은 별도 조건이다. [R07 exact/prefix L546–562](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-matching) · [R06 pip 24.0 L299–339](https://github.com/pypa/pip/blob/24.0/src/pip/_internal/resolution/resolvelib/factory.py#L299-L339) · [목적별 문구와 변경 근거](advice.csv)

## 관점별 적용 조건과 비용

| 관점 | 우선 연결 | 비용과 결손 | 경쟁 설명이 판정을 바꾸는 조건 |
| --- | --- | --- | --- |
| 발행자 | PyPI 관리 조치와 유지자의 실제 장애 조건을 함께 연결 | 사유 원문과 영향 플랫폼의 맥락을 보존해야 한다. H02의 포괄 경고만 보여 주면 정상 조합도 실패로 읽힐 수 있다. | 파일별 혼합 철회가 관측되면 해시 단위에 경고를 붙인다. [R04 L104–134](https://docs.pypi.org/project-management/yanking/) · [M01 비교 L215–227](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1) |
| 인덱스 운영자 | 두 API의 파일별 원값과 지문을 연결 | 프로젝트 전체 Simple 본문 수집과 누락·캐시 충돌 처리가 필요하다. 동일 PyPI 계보에서 읽은 값이다. | 미러가 철회 파일을 숨기거나 직렬 번호가 달라지면 한쪽 부재의 의미를 보류한다. [I01 `/meta`, `/files`](https://pypi.org/simple/matplotlib/) · [R03 Mirrors L109–117](https://packaging.python.org/en/latest/specifications/file-yanking/) |
| 정확판 재현 사용자 | 이름·버전·해시 고정 원본을 유지하고 상태 표시 추가 | 삭제된 Windows wheel이나 철회 파일을 거부하는 인덱스는 재현을 막을 수 있다. | 당시 신뢰 가능한 파일과 일치 해시를 확보하면 삭제 파일의 재현 보류를 다시 판단한다. [M01 삭제 목록 L461–468](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1#issuecomment-2267225291) · [M02 캐시 로그 L349–401](https://github.com/pytest-dev/pytest/issues/12069) |
| 새 범위 설치 사용자 | 제약을 만족하는 비철회 후보와 예외 기록을 연결 | 버전 조건 외 태그·의존 환경을 검사해야 한다. 배너가 제안한 3.11.2와 9.2.0은 예시 범위를 벗어난다. | 소비자의 Windows 조합에서 post1 실패가 해당되면 대체를 보류하고, pytest 내부 API가 필요하면 8.1.1 안내에 영향 범위를 명시한다. [H02/H05 배너](receipts/html/http.json) · [M01 L1032–1073](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1) · [M02 L447–478](https://github.com/pytest-dev/pytest/issues/12069) |
| 학술 편집자 | 원문 DOI와 영향 부분을 지목한 정정 공고를 연결 | 같은 자료에 두 출판 날짜와 정정 범위를 유지한다. | 공고가 전체 원문을 취소하거나 대체 DOI를 명시하면 범위와 우선 링크를 다시 판단한다. [X01 Correction L232–234](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0291840) · [X02 Reference 1](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0313792) |

주소 접근은 release HTML 6/6과 파일 URL 88개 노출로 관측했다. 파일 URL에 대한 현행 본문 다운로드는 미확인이다. 후보 선택은 규격과 지정 구현의 판단이고, 실제 고장·회복은 당시 플랫폼과 플러그인 로그의 범위에 한정했다. 가벼운 배너 경로는 링크 설명에는 쓸 수 있다. 파일별 결정을 할 때는 두 API의 키·상태를 확인하고, 시간 또는 설치 결과를 말할 때는 별도 당시 증거를 붙인다. [H01–H06](receipts/html/http.json) · [88파일 조인](files.csv) · [반례](COUNTEREXAMPLES.md)

| 불일치·약점 | 영향을 받는 결론 | 다음에 열 원자료·조사 | 판정을 바꿀 관측 |
| --- | --- | --- | --- |
| 두 API와 HTML은 같은 PyPI 계보의 비동시 스냅샷이다. 파일별 첫 경고 또는 개별 삭제 이벤트 UTC 미확인 | 철회 경고를 과거 재현 결과에 붙일 수 있는 시점 | [H02 Key dates](https://pypi.org/project/matplotlib/3.9.1/) · [H05 Key dates](https://pypi.org/project/pytest/8.1.0/)에 대응하는 당시 serial/인덱스 스냅샷과 실제 클라이언트 경고 UTC | 동일 filename의 최초 양성 응답 또는 이전 음성 응답의 저장 시각 |
| post1 일부 조합이 실패하고 원 빌드·후속 CI 로그가 404다 | Windows post1 대체와 특정 DLL 원인의 범위 | [M01 후속 시험](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1#issuecomment-2273144251) · [M06 답변 L163–191](https://github.com/adang1345/delvewheel/issues/52)이 가리키는 파일 해시 및 보존 CI 로그 | 같은 Python·태그·의존 패키지 조건에서 비교한 정상·실패 wheel의 DLL 및 시험 결과 |
| 현재 파일 본문과 사용자별 resolver·플러그인 조합 미확인 | 정확 핀 재현과 실제 런타임 대체 | [M02 캐시 원로그](https://github.com/pytest-dev/pytest/issues/12069#issuecomment-1986989847)와 동일 파일 해시·인덱스·잠금·플러그인 환경의 원실행 기록 | 캐시 없는 같은 해시 다운로드와 해당 hook 또는 Windows 로컬 시험 결과 |
