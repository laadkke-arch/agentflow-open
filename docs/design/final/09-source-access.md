# 09. 원문 접근: 가져오는 곳과 확인하는 곳을 나눈다

상태: 설계(2026-11-27). 근거 표시는 README와 같다. **(a)** 문서 판독, **(b)** 고정 입력에서 코드로 확인, **(c)** 실제 운영이 있어야 아는 것. 이 문서의 측정은 [access/](access/)에서 다시 돌린다(`bash access/reach.sh`, `python3 -I access/routes.py <catalog-p5 targets.jsonl.gz> out.json 40`). 장부 코드(`ledger/`)는 고치지 않았다.

이 문서가 쓰는 두 사다리는 이름이 비슷해 헷갈리기 쉽다. **확인 단계 L1~L4**는 조사 수집소 catalog의 것이다(L1 병합만, L2 주소 살아 있음, L3 인용이 원문에 있음, L4 교차 확인이 쓸모까지 받침, [08 3절](08-implementation.md#3-조사-수집소-자료읽기만)). **근거 수준 L0~L5**는 장부의 답 자리 것이다([04 3.4](04-architecture.md#34-근거-수준-사다리)). 아래에서 "L3"는 따로 말하지 않으면 확인 단계 L3다.

## 0. 결론

지금 이 클라우드 환경에서 열리는 곳은 GitHub와 패키지 저장소(그리고 GitLab API와 클라우드 SDK 몇 곳)뿐이다. catalog 대상 23,395개 가운데 80.6%(18,860개)는 그 밖의 웹 7,784개 호스트에 있고, 그 호스트의 2/3(5,100개)는 대상이 하나뿐이다. 그래서 허용 목록에 호스트를 더하거나 GitHub 미러를 찾는 방식으로는 꼬리를 덮지 못한다(1.2절). 어딘가 한 곳은 웹 전체를 읽어야 한다. 문제는 그곳을 어디에 두고, 읽은 것을 어떻게 믿느냐다.

고른 구조는 **가져오는 곳과 확인하는 곳을 나누는 것**이다.

1. **확인은 지금처럼 좁은 환경에서 결정적 코드로 한다.** 인용 대조, 판 비교, 장부 쓰기, 시험은 GitHub만 열린 개발 환경에서 돈다. 이 환경은 넓히지 않는다.
2. **가져오기는 경로 사다리를 탄다.** 싼 경로부터 쓴다. (A) 이 환경에서 바로 닿는 GitHub 원문과 패키지 저장소, (B) 문서 사이트를 그 문서를 만드는 저장소로 옮겨 읽는 원천 대응, (C) 따로 둔 **포착 일꾼**, (D) 웹 기록 보관소, (E) 사용자 기기, (F) 모델 판독 순이다(4.2절).
3. **포착 일꾼은 웹을 여는 따로 둔 클라우드 환경의 예약 작업이다.** 결정적 스크립트가 주소 목록을 받아 정중하게(robots.txt, 호스트당 속도, 조건부 요청) 바이트를 받고, 머리·시각·sha256과 함께 GitHub의 포착 저장소(opensource의 `captures` 가지)에 커밋한다. 개발 환경은 그 가지를 git으로 받아 읽는다. opensource는 비공개라 `raw`가 아니라 세션에 붙은 저장소의 git fetch로 읽는다. 웹 내용을 읽는 쪽은 장부와 코드에 쓰지 않고, 장부와 코드를 쓰는 쪽은 웹을 열지 않는다(4.3절).
4. **포착물이 곧 기록 재생 자료다.** 지금의 `fixtures/http/*.json` 형식에 경로·결속·지문 몇 칸을 더한다. 시험은 지금처럼 재생으로 돌고, "실제 실행"은 "새 포착물 재생"이 된다. EVAL-X1은 SUMO를 72시간 위상 무작위로 실제로 포착해 재생한다(4.6·4.8절).
5. **L3는 바이트에 묶일 때만 준다.** 확인 단계에 결속 표시를 붙인다. 직접 바이트(d), 보관소 바이트(a), 원천 대응(s)만 L3가 된다. 모델이 읽어 준 것(m)은 L3로 세지 않고 교차 확인(L4)의 재료로만 쓴다(4.7절).
6. **요청 시계는 기다리지 않는다.** 요청 중에는 A·B와 이미 있는 포착물만 읽는다. 없으면 포착 작업을 걸고(요청판당 4개까지) 자리를 "확인할 후보(원문 가져오는 중)"로 낸다. 포착물이 오면 재확인 작업과 같은 길로 관측이 생기고, 그 후보를 낸 자리에 알림이 간다(4.5절).

설정을 바꾸지 않고도 오늘 할 수 있는 것이 있다. 표본으로 재면 경로 A·B만으로 대상 약 1,290개의 인용을 원문(또는 원천)에서 확인할 수 있다. 지금 L3는 286개다(1.3절). 나머지 꼬리는 포착 일꾼이 필요하고, 그 환경을 만드는 것은 준혁님 승인이 필요한 설정 변경이다(8절).

## 1. 무엇이 막혔고, 얼마나 막혔나

### 1.1 이 환경에서 닿는 곳 (b)

[access/out/reach.tsv](access/out/reach.tsv), 2026-11-27T05:33Z. 이 세션의 환경은 `Default`, 네트워크 수준 Trusted(제품 설정 이름), 추가 허용 호스트 없음이다.

| 묶음 | 결과 | 비고 |
| --- | --- | --- |
| GitHub 원문 `raw.githubusercontent.com` | 열림(200) | 어느 공개 저장소든 태그·가지·커밋으로 읽는다. 지금 구현이 쓰는 길이다 |
| GitHub API `api.github.com` | 검색과 붙은 저장소만 열림 | `search/code`는 200. `repos/python/cpython/...`는 403 "GitHub access to this repository is not enabled for this session". 붙지 않은 저장소의 커밋·이슈·PR은 API로 못 읽는다. 구현 노트가 "열렸다"(I7)와 "막혔다"로 갈린 까닭이 이것이다 |
| `github.com` 화면, `codeload.github.com` 묶음 | 403 | 같은 저장소 범위 규칙([cloud environments](https://code.claude.com/docs/en/cloud-environments) "Repository scope") |
| GitLab API | 열림 | `gitlab.com/api/v4/...`. GitLab 문서 원천을 여기서 읽었다 |
| 패키지 저장소 | 열림 | PyPI JSON, npm, Go 모듈 프록시와 `sum.golang.org`, `index.crates.io`·`static.crates.io`, RubyGems, Maven, NuGet, Packagist |
| 일반 웹 | 막힘(000, 프록시 거절) | `docs.python.org`, `support.mozilla.org`, `blog.mozilla.org`, `www.openarchives.org`, `example.com`, 위키백과 |
| 보관소 | 막힘 | Wayback, Common Crawl 색인과 데이터, archive.today, Software Heritage |
| CDN 미러·대리 읽기 | 막힘 | jsDelivr, unpkg, docs.rs, `r.jina.ai` |
| Claude Code 내장 읽기 도구(WebFetch) | 열림 | 같은 세션에서 `docs.python.org`·`support.mozilla.org`·`commoncrawl.org`를 200으로 읽었다. 셸과 다른 길이다. 돌려주는 것은 바이트가 아니라 작은 모델의 답이다(1.4절) |

제품 문서가 말하는 수준은 넷이다. None, Trusted(패키지 저장소·GitHub·클라우드 SDK), Full(모든 도메인), Custom(직접 쓴 허용 목록, 기본 목록 포함 선택). 환경마다 하나를 고르고, 예약 작업(routine)도 환경을 골라 돈다(a, [cloud environments](https://code.claude.com/docs/en/cloud-environments) "Access levels"). 이 사실이 4.3절의 포착 일꾼을 가능하게 한다.

### 1.2 catalog 23,395개를 원문 경로로 나누면 (b)

opensource `55c51d4`의 catalog 대상([fixtures/catalog-p5](../../../ledger/fixtures/catalog-p5/SOURCES.json), 읽기만)을 주소 꼴로 나눴다(`access/routes.py`의 `classify`).

| 경로 | 대상 | 비율 | 지금 L3·L4 | 무엇인가 |
| --- | --- | --- | --- | --- |
| A1 GitHub 파일·README | 1,159 | 5.0% | L3 229 | `blob` 661, 저장소 첫 화면(README) 491, raw 7 |
| A2 패키지 저장소 | 441 | 1.9% | L3 3, L4 3 | docs.rs 195(crate 묶음), pkg.go.dev 127(Go 모듈 zip), pypi.org 119(JSON 설명) |
| A3 GitHub API만 | 400 | 1.7% | L3 14 | 이슈·PR·토론·위키·릴리스·커밋 화면. 붙지 않은 저장소라 이 환경에서는 못 읽는다 |
| B 원천 대응(쟀음) | 764 | 3.3% | L4 4 | docs.python.org, MDN, docs.github.com, kubernetes.io, GitLab 문서, MS Learn(Azure·.NET). 영어 262, 번역판 502 |
| B 원천 있음(안 쟀음) | 1,771 | 7.6% | L3 2, L4 15 | git-scm, PostgreSQL, PHP, W3C, IETF, Debian, googlesource, MS Learn 나머지 등 |
| C 웹만 | 18,860 | 80.6% | L3 38, L4 66 | 호스트 7,784개 |

C의 모양이 결론을 정한다. 호스트 7,784개 가운데 5,100개는 대상이 하나뿐이고, 대상의 48%(9,067개)가 대상 셋 이하인 호스트에 있다. 상위 20개 호스트(docs.aws.amazon.com 517, docs.cloud.google.com 348, developers.google.com 159, patents.google.com 116 …)를 다 허용해도 C의 11%다. 언어는 영어 8,180, 일본어 2,807, 프랑스어 1,977, 독일어 1,272, 중국어 1,233, 한국어 1,201 순이고, PDF가 1,786개다.

### 1.3 닿는 경로에서 인용이 실제로 맞나 (b)

경로마다 대조할 인용(공백으로 나눈 낱말 6개 이상)이 있는 대상을 40개까지 무작위로 뽑아(씨앗 20261127) 원문이나 원천을 받고, 그 안에서 `claim.evidence`를 찾았다. 대조 규칙은 이 측정용 임시 규칙이다. NFKC·소문자로 바꾸고 rst 역할과 마크다운 기호를 지운 낱말 줄에서, 인용 낱말 줄이 그대로 있으면 exact, 인용 4-gram의 80% 이상이 있으면 near다. 요청 845회(200 545, 404 299, 429 1), 176MB. [access/out/routes40.json](access/out/routes40.json), 원인 나눔은 [post40.json](access/out/post40.json).

| 경로 | 표본 | 일치 | 못 받음 | 놓침: 번역된 인용 | 놓침: 그 밖 | 받은 것 중 일치 |
| --- | --- | --- | --- | --- | --- | --- |
| A1 GitHub `blob` (대조군) | 40 | 26 | 0 | 8 | 6 | 65% |
| A1 README | 40 | 32 | 0 | 4 | 4 | 80% |
| A2 crate 묶음 | 40 | 23 | 0 | 8 | 9 | 58% |
| A2 Go 모듈 zip | 40 | 25 | 0 | 9 | 6 | 63% |
| A2 PyPI 설명 | 40 | 23 | 0 | 7 | 10 | 58% |
| B docs.python.org → `cpython/<판>/Doc/*.rst` | 21 | 16 | 0 | 4 | 1 | 76% |
| B kubernetes.io → `kubernetes/website` | 40 | 30 | 1 | 6 | 3 | 77% |
| B MDN 영어 → `mdn/content` | 28 | 19 | 0 | 4 | 5 | 68% |
| B MDN 번역 → `mdn/translated-content` | 40 | 22 | 11 | 0 | 7 | 76% |
| B GitLab 문서 → `gitlab-org/gitlab/doc` | 40 | 22 | 15 | 1 | 2 | 88% |
| B MS Learn Azure 영어 → `MicrosoftDocs/azure-docs` | 38 | 15 | 19 | 0 | 4 | 79% |
| B MS Learn .NET 영어 → `dotnet/docs` | 30 | 12 | 18 | 0 | 0 | 100% |
| B docs.github.com 영어 → `github/docs` | 19 | 7 | 1 | 1 | 10 | 39% |
| B 번역판(GitHub Docs·MS Learn) → 영어 원천 | 120 | 2 | 53 | 0 | 65 | 3% |

읽기는 넷이다.

1. **원천 대응은 직접 읽기만큼 맞는다.** 같은 바이트를 읽는 대조군(GitHub `blob`)이 65%다. 같은 언어의 원천 대응은 docs.github.com을 빼면 받은 것 중 68~100%가 맞았다. 문서 사이트의 글은 대부분 그 저장소의 원천 글과 같은 문장이다. docs.github.com만 낮은 까닭은 변수 치환(`{% data variables %}`)이 많아서다.
2. **놓친 것의 절반은 접근 문제가 아니다.** A 경로(raw 7개 포함) 놓침 74건 중 37건은 영어 원문에 한국어 등으로 옮긴 인용을 단 기록이다. 어떤 경로로 읽어도 L3가 될 수 없다. p5 지시문("쓸모마다 원문 문장")을 지키지 않은 기록이므로 수집 쪽에서 고친다(8절 단계 0).
3. **못 받음은 대응 규칙의 빈칸이다.** MS Learn·GitLab은 주소와 파일 경로가 일대일이 아니어서 404가 많다. 받은 것은 잘 맞으므로 대응 규칙(목차 파일, 리디렉션 표)을 보강하면 는다.
4. **번역판은 원천이 공개되지 않으면 막힌다.** MDN은 번역 저장소가 공개라 76%가 맞았다. GitHub Docs·MS Learn 번역판은 영어 원천과 대조할 수밖에 없어 3%다. 이런 대상은 포착 일꾼(C)이 필요하다.

표본 일치율을 모집단에 곱하면 경로 A·B로 **약 1,290개**가 L3가 된다(A 약 1,090, B 약 200, 표본이 작아 범위가 넓다). 지금 L3 286개 중 A1이 229개이므로 새로 생기는 몫은 약 1,060개다. 설정 변경 없이 할 수 있다.

### 1.4 모델 판독은 얼마나 믿을 만한가 (b, 작은 표본)

[access/out/model_read_probe.md](access/out/model_read_probe.md). 내장 읽기 도구에 기대값을 주지 않고 앵커만 주어 물었다(눈가림). `docs.python.org`의 `asyncio.Queue` 첫 두 문장은 `cpython/3.13/Doc/library/asyncio-queue.rst`와 2/2 같았다(꾸밈 표시 제외). SUMO `future-of-pocket/history`의 개정 행은 기록 재생 자료와 겹치는 셋(308355, 308427, 313551)이 모두 같았다. 그리고 **기록에 없는 새 개정 둘**을 보였다. 313578(2025-11-12, 링크 문구와 사소한 수정)과 317710(2026-01-08, "See Bug 2008808")이다. EVAL-X1 기록 재생 자료가 실제 이력보다 두 개정 늦다는 뜻이다. 313578은 바뀐 것 없는 개정이라 알림이 가면 안 되는 경우이므로, 실제 포착으로 돌리면 효과 판정(`confirms`)을 처음 시험하게 된다(4.8절).

같은 도구로 Software Heritage 문서를 읽자 본문 대신 봇 차단 화면(Anubis)이 왔다. 봇 차단은 실제로 만나는 실패 종류다(4.9절).

이 경로는 넓게 닿지만 바이트와 지문이 없다. 판을 비교할 수 없고 재생할 수 없다. 그래서 L3로 세지 않는다.

## 2. 다른 곳은 어떻게 푸나 (a)

| 방식 | 하는 일 | 빌릴 것 | 빌리지 않을 것 |
| --- | --- | --- | --- |
| 코딩 에이전트의 망 설정 | Claude Code 클라우드는 None·Trusted·Full·Custom 넷 중 하나를 환경마다 고르고, GitHub는 따로 둔 대리 서버가 붙은 저장소 범위로만 연다([cloud environments](https://code.claude.com/docs/en/cloud-environments)). Codex는 에이전트 단계 인터넷을 기본으로 막고, 허용 목록(없음·흔한 의존성·전부)과 GET·HEAD·OPTIONS 제한을 두며, 위험으로 "Prompt injection from untrusted web content", "Code or secret exfiltration"을 든다([Codex internet access](https://learn.chatgpt.com/docs/cloud/internet-access)). Copilot 에이전트 방화벽은 권장 목록을 기본으로 켜고 "should not be considered a comprehensive security solution"이라고 적는다([Copilot firewall](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-firewall)) | 코드와 비밀을 가진 세션은 좁게 둔다. 넓힐 때는 환경을 따로 만들고 방법을 GET·HEAD로 줄인다 | 개발 세션 자체를 Full로 여는 것 |
| 웹 기록 보관소 | Wayback 가용성 API는 주소와 시각을 받아 가장 가까운 포착을 준다([wayback api](https://archive.org/help/wayback_api.php)). CDX 서버는 포착마다 시각·상태·지문을 준다([CDX README](https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md)). Common Crawl CDXJ 색인은 수집 회차별이고, `filename`·`offset`·`length`로 WARC 레코드 하나를 범위 요청하며, `digest`는 페이로드 SHA-1이다([CDXJ index](https://commoncrawl.org/cdxj-index)). 주소의 35~90%만 보관본이 하나 이상 있고, 짧은 주소(Bitly) 표본은 35%였다([Ainsworth 외](https://arxiv.org/abs/1212.6177)) | 죽은 주소의 판 되찾기, 제3자가 가진 증인 판, 지문으로 판 비교 | 1차 읽기 경로. 꼬리일수록 보관본이 드물다 |
| 시간 축 주소 | Memento(RFC 7089)는 Accept-Datetime으로 그 시각의 판을 고르는 TimeGate와 판 목록 TimeMap을 정한다([RFC 7089](https://datatracker.ietf.org/doc/rfc7089)). Robust Links는 인용 링크에 원래 주소, 보관본 주소, 날짜를 함께 단다([spec](https://mementoweb.org/robustlinks/spec/)). 대법원 판결문 링크의 절반이 원래 자료로 가지 않는다는 조사가 Perma.cc를 낳았다([ABA Journal](https://www.abajournal.com/news/article/link_rot_int_scotus_decisions_documented_half_dont_go_to_original_material), [Harvard Law Review](https://harvardlawreview.org/forum/vol-127/perma-scoping-and-addressing-the-problem-of-link-and-reference-rot-in-legal-citations/)) | 판 없는 웹 페이지의 판을 "포착 시각 + 지문"으로 두는 것, 답의 첫 링크 옆에 포착본을 두는 것 | — |
| 포착 형식 | WACZ는 WARC를 ZIP에 담고 `archive/`, CDXJ `indexes/`, `pages/pages.jsonl`, 자원마다 sha256이 든 `datapackage.json`을 두며 서명도 정의한다([WACZ 1.1.1](https://specs.webrecorder.net/wacz/1.1.1)). Webrecorder 도구(브라우저 확장 ArchiveWeb.page, 크롤러 Browsertrix, 재생기 pywb)가 이 형식을 쓴다 | 포착 기록 칸을 WARC 이름(Target-URI, Date, Payload-Digest)과 맞춰 나중에 WACZ로 내보낼 수 있게 한다 | 지금 WARC 도구를 들이는 것(장부는 표준 라이브러리만 쓴다) |
| 소스 보관과 패키지 저장소 | Go 모듈 프록시는 바뀌지 않는 판을 주고 `.info`에 원 저장소 커밋(`Origin.Hash`)을 적으며, `sum.golang.org`가 지문을 공증한다(이번에 받아 확인). crate 묶음은 `.cargo_vcs_info.json`에 커밋과 경로를 담는다(opensource R0 정찰). Software Heritage는 내용 지문 ID(SWHID)로 소스를 보관한다 | 패키지 판을 판 키로, 원 커밋을 원천 결속으로 | — |
| 시험의 기록·재생 | VCR.py·pytest-recording 같은 도구는 처음 한 번 기록하고 이후 재생하며, CI는 새 요청을 막는 모드로 돈다. Bazel·Nix는 지문을 알고 받는(fixed-output) 내려받기만 허용한다 | 고정물은 출처가 붙은 포착물이다. 시험은 재생만, 새 포착은 일꾼만 | — |
| CI를 가져오기 일꾼으로 | GitHub Actions 약관은 GitHub 호스팅 실행기로 "any other activity unrelated to the production, testing, deployment, or publication of the software project associated with the repository"를 금하고, CDN이나 서버리스 앱의 일부로 쓰지 말라고 적는다([GitHub additional product terms](https://github.com/github/docs/blob/main/content/site-policy/github-terms/github-terms-for-additional-products-and-features.md)). 예약 실행은 기본 가지에서만 돈다 | 이 저장소 시험용 고정물 새로 받기(작은 규모)는 맞는다 | 수집소 2만 대상을 긁는 일, 제품의 원문 서버 |
| 정중한 수집 | robots.txt(RFC 9309), 호스트당 속도, ETag·Last-Modified 조건부 요청(304) | 그대로. 304 비율은 07 R-2(조건부 폴링 비용)의 실제 자료가 된다 | — |
| 모델 제공자의 서버 쪽 읽기 | Claude API의 `web_fetch` 서버 도구는 허용·차단 도메인, `max_uses`, `max_content_tokens`, 인용 표시를 받고 문서 블록을 돌려준다. 대화에 이미 나온 주소만 읽는다(claude-api 참고, `web_fetch_20260209`) | 제품에서 서버 포착이 막힐 때의 보조 읽기(결속 m에 가깝다) | L3 판정기 |
| 제3자 스크레이핑 서비스 | 주소를 보내면 렌더링한 글을 돌려준다 | — | 모든 주소가 제3자에게 간다. 1.8절 "누가 왜 읽었는지 남기지 않는다"와 맞지 않는다 |

## 3. 안 비교

평가 기준은 일곱이다. (1) C 꼬리 도달, (2) 결속(바이트인가), (3) 사람 손(준혁님은 스크립트를 돌리지 않는다), (4) 개발 세션의 주입·유출 면, (5) 약관과 예절, (6) 기록 재생·판과 맞물림, (7) 제품에도 쓰이나.

| 안 | (1) 꼬리 | (2) 결속 | (3) 손 | (4) 보안 | (5) 약관 | (6) 재생 | (7) 제품 | 판정 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O1 개발 환경에 호스트 몇 개 추가(Custom) | ✗ 상위 20개가 11% | d | 0 | △ | ○ | ○ | ✗ | 보조. 포착 일꾼이 서기 전 EVAL-X1만 급할 때 |
| O2 개발 환경을 Full로 | ○ | d | 0 | ✗ 푸시 권한을 가진 세션이 웹 전체를 읽는다 | ○ | ○ | ✗ | 버림 |
| **O3 포착 전용 환경 + 예약 작업** | ○ 봇 차단·로그인 제외 | d | 0 | ○ 읽는 쪽과 쓰는 쪽이 나뉜다 | ○ | ○ | ○ 같은 계약을 서버 포착기로 | **고름(경로 C)** |
| O4 GitHub Actions | ○ | d | 기본 가지 병합 필요 | ○ | 수집 ✗, 시험 고정물 ○ | ○ | ✗ 약관 | 시험 고정물만 대안 |
| O5 사용자 기기(Remote Control·내장 브라우저) | ○ 로그인·JS 포함 | d | 기기 켜짐·승인 | ○ | ○ | ○ | ○ Studio 쪽 포착 | 고름(경로 E, 실패 승급) |
| O6 브라우저 확장 포착 | 한 쪽씩 | d | ✗ 사람이 누른다 | ○ | ○ | ○ | ○ 사용자가 근거를 가져오는 길 | 제품에서만 |
| O7 보관소 | △ 35~90% | a | 0 | ○ | ○ 속도 제한 | ○ 시각 판 | ○ 첫 링크 옆 포착본 | 고름(경로 D, 죽은 주소·증인) |
| O8 원천 대응·패키지 | ✗ 쟀음 3.3% + 있음 7.6% | s·d | 0 | ○ | ○ | ○ | ○ D10과 같은 방향 | 고름(경로 A·B, 오늘) |
| O9 모델 판독(WebFetch·dot·API) | ○ | m | 0 | △ 모델이 웹 글을 읽는다 | ○ | ✗ 바이트 없음 | △ | 교차 확인만(경로 F) |
| O10 제3자 스크레이핑 | ○ | 추출 글 | 0 | ✗ 주소 유출 | △ | △ | ✗ | 버림 |

O3가 이기는 까닭은 하나다. 꼬리를 덮는 안(O2·O3·O9·O10) 가운데 바이트를 주면서 개발 세션을 넓히지 않는 것이 O3뿐이다. O3가 지는 곳은 봇 차단, 로그인, 자바스크립트로만 그리는 페이지다. 이 실패는 경로 E(사용자 기기)로 넘긴다. 데이터센터 주소를 막는 사이트도 같은 길로 간다.

## 4. 고른 구조

### 4.1 한 장 그림

```
         ┌─────────────── 개발 환경(Trusted, 지금 그대로) ───────────────┐
요청 ──▶ │ ④ 확인: 경로 A(GitHub raw·패키지) · B(원천 대응) · 포착 가지 읽기   │──▶ 관측(결속 d·s·a) ──▶ 답
         │        없으면 포착 작업을 건다(요청판당 4개)                    │
         └──────────────┬───────────────────────────────▲───────────────┘
                        │ 포착 대기열(주소·이유만)        │ 포착 색인(채널처럼 폴링)
                        ▼                               │
         ┌──────── 포착 환경(Full, 예약 작업, 결정적 스크립트) ────────┐
         │ robots·호스트당 속도·조건부 GET → 바이트·머리·sha256 커밋      │
         │ 실패: 404·410 → 보관소(D) / 봇 차단·로그인·JS → 기기(E) 대기열 │
         └────────────────────────────────────────────────────────────┘
```

### 4.2 경로 사다리

| 경로 | 어디서 도나 | 덮는 것 | 결속 | 시계·예산 | 실패하면 |
| --- | --- | --- | --- | --- | --- |
| A 직접 | 개발 환경 | GitHub 파일(`raw`), 저장소 README(`HEAD`), 패키지 저장소(PyPI JSON, Go 모듈 zip, crate 묶음 …) | d | 요청 시계 가져오기 1회 | B |
| B 원천 대응 | 개발 환경 | 문서 사이트 → 그 문서를 만드는 저장소의 같은 판 원천(문서 판이 있으면 그 가지·태그) | s | 요청 시계 가져오기 1회 | C |
| C 포착 일꾼 | 포착 환경 | 공개 웹 전체(로그인 없음) | d | 배경 시계. 요청은 작업만 건다 | 404·410 → D, 봇 차단·로그인·JS → E, 일시 실패 → 2회 재시도 |
| D 보관소 | 포착 환경 | Wayback·Common Crawl의 같은 주소 원본 바이트(`id_` 재생, WARC 범위 요청) | a | 배경 시계 | 보관본 없음 → "원문 접근 실패" |
| E 사용자 기기 | 준혁님 기기(Remote Control, 내장 브라우저) | 봇 차단, 로그인, 자바스크립트 렌더링, 사내 문서 | d(쿠키가 있으면 비공개) | 사람 승인이 걸리는 따로 둔 시계 | 남김(사람 판단) |
| F 모델 판독 | 어디서나 | 무엇이든 | m | 교차 확인 표본만 | — |

원천 대응(B)은 표 하나로 둔다. 키는 호스트와 주소 꼴, 값은 저장소·가지 규칙·경로 규칙·꾸밈 제거 규칙이다. 이번에 쓴 규칙 아홉이 `access/routes.py`의 `classify`에 있다. 문서 판이 주소에 있으면(`docs.python.org/3.11/…`) 그 가지를, 없으면 기본 가지를 읽고, 판 키는 `fetch` 종류(가져온 시각, 지문)로 둔다(`edition.kind='fetch'`, 지금 스키마 그대로). 붙지 않은 저장소는 API로 커밋을 못 얻으므로 가지 이름과 지문으로 판을 묶는다.

### 4.3 포착 일꾼

**어디서.** 준혁님 개인 클라우드 환경을 하나 더 만든다. 이름 "원문 포착", 네트워크 Full, 환경 변수와 비밀 없음. 예약 작업에는 opensource 저장소 하나만 붙인다. 예약 작업 "원문 포착"이 이 환경에서 6시간마다(첫 이틀은 매시) 돈다. 지금 "수집소 6시간 정리"와 같은 운영 방식이라 사람이 스크립트를 돌릴 일이 없다.

**무엇을.** 예약 작업은 opensource의 `tools/capture.py run --minutes 25` 하나를 돌리고 결과 숫자만 보고한다. 스크립트가 하는 일은 다음과 같다.

1. 포착 대기열(`captures/queue/*.jsonl`)과 감시 목록(`captures/watch.json`, 주기·위상이 붙은 출처)을 읽는다.
2. 호스트마다 robots.txt를 24시간 캐시로 보고, 금지면 받지 않고 `robots` 결과를 남긴다.
3. GET·HEAD만 쓴다. 쿠키를 쓰지 않고, 로그인 화면을 따라가지 않는다. 호스트당 2초에 1회, 전체 동시 8개, 응답 20초, 크기 5MB 상한. 받을 형식은 HTML·텍스트·JSON·XML·PDF.
4. 지난 포착의 ETag·Last-Modified로 조건부 요청을 보낸다. 304는 포착 기록만 남기고 바이트를 다시 받지 않는다. 이 비율이 07 R-2의 실제 값이 된다.
5. 리디렉션은 5번까지 따라가며 하나하나 적는다. 봇 차단 화면(상태 403·429·503과 알려진 표지)과 로그인 화면을 알아보고 실패로 분류한다.
6. 받은 바이트를 sha256으로 이름 붙여 저장하고, 포착 기록(4.4절)과 색인 줄을 쓴 뒤 `captures` 가지에 커밋·푸시한다. 기본 가지와 dot 가지에는 쓰지 않는다.

**하지 않는 것.** 예약 작업의 Claude는 받은 본문 파일을 열지 않는다. 스크립트는 개수와 상태만 출력한다. 웹 글이 담은 지시가 장부나 코드에 닿을 길을 처음부터 두지 않기 위해서다. 사용자 이름·메일 같은 개인 정보를 User-Agent에 넣지 않는다(일반 이름 `agentflow-capture/0`).

**얼마나.** C 대상 18,860개는 호스트가 넓게 흩어져 있어 호스트당 속도보다 실행 시간이 묶는다. 한 번에 2,000~3,000개면 첫 이틀(매시)에 다 돈다 **[가정 C19]**. 그 뒤로는 감시 목록과 새 대상만 돈다.

**저장.** 포착물은 opensource(비공개)에 둔다. 원문 전체 사본이므로 공개하지 않는다. 인용으로 쓰이지 않은 바이트는 90일 뒤 지우고, 포착 기록(지문·머리·시각)은 남긴다. 공용 장부에는 지금처럼 인용 지문과 짧은 인용만 간다(07 D7). 큰 바이트가 저장소를 키우면 릴리스 자산으로 옮긴다(`release-assets.githubusercontent.com`은 Trusted 목록에 있다).

### 4.4 포착 기록

지금 `adapters/http.py`가 쓰는 기록(`method`, `url`, `request_headers`, `fetched_at`, `status`, `headers`, `body`·`body_b64`, `note`)에 칸을 더한다. 기록 키(방법·주소·키 머리의 sha256 앞 24자)는 그대로다. 그래서 같은 재생기가 포착물도 읽는다.

```json
{
  "capture_v": 1,
  "method": "GET", "url": "https://support.mozilla.org/en-US/kb/future-of-pocket/history",
  "request_headers": {"If-None-Match": "\"…\""},
  "fetched_at": "2026-11-28T03:17:41Z", "status": 200,
  "headers": {"content-type": "text/html; charset=utf-8", "etag": "\"…\"", "last-modified": "…"},
  "final_url": "https://support.mozilla.org/en-US/kb/future-of-pocket/history",
  "redirects": [],
  "route": "C", "binding": "d", "worker": "capture-env/routine@tools/capture.py#<커밋>",
  "robots": "allowed",
  "payload_sha256": "…", "payload_bytes": 20744, "payload_ref": "captures/blob/ab/cd/<sha256>.gz",
  "outcome": "ok",
  "reason": "watch"
}
```

`outcome`은 4.9절의 분류다. `reason`은 `request`·`catalog`·`watch` 셋 중 하나이고 어느 프로젝트의 요청인지 적지 않는다. WARC와는 `url`=WARC-Target-URI, `fetched_at`=WARC-Date, `payload_sha256`=WARC-Payload-Digest(sha256)로 맞춘다. 원천 대응(B)의 기록은 `route: "B"`, `binding: "s"`, `source: {"repo": "python/cpython", "ref": "3.13", "path": "Doc/library/asyncio-queue.rst"}`를 더한다.

### 4.5 장부와 맞물림

- **관측 키는 그대로다.** (page, 판, 위치). 판 번호가 없는 웹 페이지는 지금 스키마의 `edition.kind='fetch'`로 (포착 시각, 지문)을 판 키로 쓴다. 같은 지문이면 같은 판이라 다시 본 기록이 되고, 지문이 바뀌면 새 판이다. 판 사이 위치는 m1(08 I4)이 옮긴다.
- **관측에 두 칸을 더한다.** `binding`(d·a·s·m)과 `capture_ref`(포착 기록 키). 지금 `reader`·`evidence_ref` 칸은 판독 주체와 원장 출처를 그대로 맡는다.
- **가져오기 셈(07 D1)은 뜻을 지킨다.** "(주소, 판)의 원문을 네트워크에서 받은 횟수"다. 경로 A·B의 원문 읽기와 포착 저장소에서 포착물을 읽는 것을 똑같이 1회로 센다. 포착 일꾼이 원 서버에 보낸 요청은 배경 시계의 공용 몫이다(07 D11). 요청 몫을 쓰지 않는다.
- **포착 작업은 외부 시도로 센다.** 요청판 하나가 걸 수 있는 포착 작업은 4개다(`REQUEST_CAPTURE_JOBS = 4`, 07 D1의 가져오기 4회와 같은 크기) **[가정 C20]**. 넘으면 남은 후보는 지금처럼 "예산"으로 접는다.
- **늦게 온 원문은 재확인과 같은 길로 들어온다.** 포착 색인을 채널처럼 폴링한다(외부 ID = 포착 기록 키, 07 D3·04 3.8). 기다리던 주소의 포착이 오면 재확인 작업이 생기고, 작업자가 포착물을 읽어 관측을 쓴다. 앞서 남긴 실패 관측(`outcome='unreachable'`)은 새 관측으로 대체되고, 그 후보를 낸 자리에 "원문 확인" 알림이 간다. 지난 답은 당시 문장 그대로다(04 3.3). 알림 종류를 하나 더하는 것이 엔진 변경의 전부다.
- **공개와 비공개.** 포착 일꾼은 로그인 없이 공개 주소만 받으므로 그 관측은 공용 장부에 둘 수 있다. 대기열에는 주소와 이유만 있고 프로젝트는 없다. 요청과 포착 작업의 연결은 프로젝트 장부의 `call_log`에만 있다. 경로 E에서 쿠키·로그인으로 받은 것은 그 프로젝트 장부에만 둔다. 지금 장부에는 비공개 관측 표가 없다. 경로 E를 켤 때 정한다 **[빈칸]**.
- **포착 글은 데이터다.** 모델 판독기가 포착 글을 읽을 때는 지시가 아닌 자료로 넘긴다. 결정적 대조기는 글을 해석하지 않는다.

### 4.6 기록 재생과 하나로

`Transport`의 세 모드(live·record·replay)에 넷째 원천을 더한다. 재생 디렉터리를 여럿 두고 앞에서부터 찾는다(`fixtures/http/` → 포착 저장소에서 모은 `fixtures/captures/`). 시험은 지금처럼 재생만 하고 네트워크를 쓰지 않는다(`test_replay_used_no_network` 유지). 측정의 `--live`는 경로 A·B만 실제로 읽고, C 몫은 포착 저장소에서 모은 최신 포착물을 읽는다. 결과 파일에 포착 시각을 함께 적어 "몇 시간 전 원문인가"가 보이게 한다. 포착 저장소에서 고정물로 모으는 도구는 지금의 `tools/snapshot_*.py`처럼 읽기만 하고 커밋·경로를 `SOURCES.json`에 남긴다.

### 4.7 catalog 확인 단계와 맞물림

| 단계 | 주는 조건 | 결속 표시 |
| --- | --- | --- |
| L2 주소 살아 있음 | 경로 A·B·C가 200을 받았고 봇 차단·로그인 화면이 아니다. 또는 보관소가 그 주소의 200 포착을 가졌다(그 시각까지만) | 경로 기호를 붙인다(L2-C, L2-D) |
| L3 인용이 원문에 있음 | 결정적 대조기가 결속 d·a·s 원문에서 인용을 찾았다 | L3d, L3a, L3s. 지금의 L3 276개는 대부분 L3d(GitHub)다 |
| L4 교차 확인이 쓸모까지 받침 | 지금처럼 다른 dot의 교차 확인(VR) | 그대로 |
| (표시) 모델만 읽음 | 경로 F의 눈가림 판독만 있다 | `m` 표시. L3로 세지 않는다 |

대조 규칙은 opensource가 이미 L3에 쓰는 규칙을 기준으로 한다. 이 문서의 측정 규칙(4-gram 80%)은 임시다. PDF는 포착 일꾼이 글을 뽑아 함께 저장한다(`pdftotext`가 있으면). 번역된 인용(1.3절 읽기 2)은 L3 대상에서 빼고, 수집 쪽에 원문 문장으로 고쳐 달라는 요청으로 돌린다.

### 4.8 EVAL-X1과 새 검색 직접 갈래

- **EVAL-X1.** 감시 목록에 SUMO 도움말 `future-of-pocket`, 그 개정 이력(`…/history`), 개정마다의 본문 화면(주소 꼴은 첫 포착 때 확인), 공급자 소식 피드(`blog.mozilla.org/en/feed/`)를 넣는다. 주기는 72시간이고 위상은 출처마다 무작위다(06 3.4). `adapters/channel_raw.py`는 포착 색인을 읽고, 채널에 보인 시각은 포착 시각이다. 그러면 단위 2 완료 기준 (1) "게시 뒤 폴링 주기 + 24시간 안에 관측"을 실제 시계로 잴 수 있다. 과거 개정(2025년)은 이력 페이지 포착 하나로 다시 세운다. 개정 번호·시각을 기록 재생 자료와 대조하고(1.4절의 셋은 이미 맞다), 빠진 313578·317710을 더한다. 313578은 바뀐 것 없는 개정이므로 대체 효과가 `confirms`이고 알림이 0이어야 한다. 원장 판독(`reading`)을 옮긴 칸은 포착한 개정 본문 인용으로 바꾼다.
- **새 검색 직접 갈래.** 06 3.1이 기본안으로 둔 `docs.python.org/3.13/searchindex.js`(키 없는 검색 색인)를 감시 목록에 주 1회로 넣는다. 검색 어댑터는 포착물에서 색인을 읽는다. 그러면 I7이 막혀서 GitHub 코드 검색으로 바꾼 갈래를 원래 안으로 되돌려 둘을 비교할 수 있다.

### 4.9 실패 분류와 다음 경로

지금 `fetch_log.outcome`(ok, not_modified, not_found, unreachable, truncated, unsupported)에 다섯을 더한다.

| 결과 | 알아보는 법 | 다음 경로 |
| --- | --- | --- |
| `blocked_policy` | 개발 환경 프록시 거절(연결 실패·403과 프록시 표지) | C에 작업을 건다. 같은 호스트를 다시 직접 시도하지 않는다 |
| `robots` | robots.txt 금지 | 받지 않는다. 보관소에 이미 있는 공개 포착본만 증인(a)으로 쓴다 |
| `challenge` | 403·429·503과 봇 차단 표지(예: Anubis, Cloudflare 확인 화면) | E 대기열 |
| `login` | 로그인 화면으로 리디렉션, 401 | E 대기열(비공개) |
| `gone` | 410, 또는 404가 이틀 넘게 이어짐 | D |

같은 실패가 세 번 이어지면 그 관측을 인용한 자리에 "원문 접근 실패" 알림을 보낸다는 04 6.2의 규칙은 그대로다. 이제 실패마다 다음 경로가 있으므로, 알림은 사다리 끝까지 간 뒤에만 보낸다.

### 4.10 운영 지표

| 지표 | 경보 [가정] | 동작 |
| --- | --- | --- |
| 포착 대기열 최고령 | 72시간 초과 | 예약 작업 주기를 당긴다 |
| 경로별 성공률(C·D) | C 80% 미만 | 실패 분류 표를 보고 호스트별 규칙을 더한다 |
| 봇 차단 비율 | 호스트별 20% 초과 | 그 호스트를 E로 보낸다 |
| 304 비율 | — | 07 R-2 값으로 기록한다. 304가 싸다는 가정(C14)을 잰다 |
| 보관소로 넘긴 비율 | — | 죽은 주소 비율로 본다 |
| L3 결속별 수 | 하루 증가 0이 사흘 | 대기열과 대조기를 점검한다 |

## 5. 제품 배포 뒤에도 같은가

같다. 개발 환경과 포착 환경의 나눔이 제품에서는 "장부를 쓰는 서버"와 "원문 포착기"의 나눔이 된다. 포착기는 같은 포착 기록을 쓰고, 장부는 포착물을 읽어 관측을 쓴다. 경로 E는 Studio가 사용자 기기에서 사내 문서·로그인 문서를 포착하는 길이 되고, 그 관측은 그 프로젝트에만 남는다. 서버 포착이 막힌 사이트에는 모델 제공자의 서버 쪽 읽기(결속 m)를 보조로 쓸 수 있지만 L3로 세지 않는다. 답의 첫 링크 옆에 포착본(보관소나 자체 포착)을 함께 두면 Robust Links처럼 링크가 죽어도 근거가 남는다. 공용 관측이 된 공개 주소에만 그렇게 한다. 어느 경로에도 요청 문장을 보내지 않는다. 경로가 받는 것은 주소뿐이다.

## 6. 하지 않는 것

- 개발 환경을 Full로 열지 않는다. 푸시 권한과 장부를 가진 세션이 웹 글을 바로 읽게 된다(2절 Codex·Copilot이 드는 위험).
- GitHub Actions로 수집소를 긁지 않는다. 약관이 막는다. 이 저장소 시험 고정물을 새로 받는 일에는 쓸 수 있지만, 예약 실행은 기본 가지 병합이 필요해 지금은 쓰지 않는다.
- 제3자 스크레이핑·읽기 서비스(Jina Reader, Firecrawl 등)에 주소를 보내지 않는다.
- 내장 읽기 도구(WebFetch)나 dot 판독을 L3 판정기로 쓰지 않는다. 바이트가 없고 비용이 대상 수에 비례한다.
- 원문 전체 사본을 공용 장부나 공개 저장소에 두지 않는다.

## 7. 결정과 가정

| 번호 | 결정 | 근거 |
| --- | --- | --- |
| D12 | 가져오기와 확인을 나눈다. 확인은 개발 환경의 결정적 코드, 가져오기는 경로 사다리 | 1.2절 꼬리 모양, 2절 에이전트 망 설정 |
| D13 | 경로 순서 A → B → C → D/E, F는 교차 확인만 | 1.3절 일치율, 3절 비교 |
| D14 | 포착 일꾼은 따로 둔 Full 환경의 예약 작업이 도는 결정적 스크립트이고, 본문을 모델이 읽지 않는다 | 3절 O3, 2절 Actions 약관 |
| D15 | 확인 단계 L3는 결속 d·a·s만. m은 표시만 한다 | 1.4절 |
| D16 | 요청 시계는 A·B와 기존 포착물만 읽는다. 포착 작업은 요청판당 4개이고 배경 시계 몫이다 | 07 D1·D11 |
| D17 | 판 없는 웹 페이지의 판은 (포착 시각, 지문). 같은 지문은 다시 본 기록 | 지금 스키마 `edition.kind='fetch'`, Memento |
| D18 | 쿠키·로그인으로 받은 원문(경로 E)은 프로젝트 장부에만 | 04 2.1 데이터 소유 |

| 번호 | 가정 | 재는 법 |
| --- | --- | --- |
| C18 | 정중한 속도와 robots를 지키면 C 대상의 80% 이상을 받는다 | 첫 이틀 포착의 경로별 성공률 |
| C19 | 한 번에 25분, 2,000~3,000개 | 첫 실행의 처리량 |
| C20 | 요청판당 포착 작업 4개면 보류율 5%를 넘지 않는다 | 07 D11처럼 decide_sim에 포착 지연을 넣어 비교 |
| C21 | 원천 대응의 인용 일치는 그 페이지의 직접 대조와 같다 | 포착 일꾼이 생긴 뒤 B 대상 100개를 C로도 받아 L3s와 L3d를 나란히 |
| C22 | 포착물 저장이 opensource를 감당 못 할 만큼 키우지 않는다 | 첫 주 저장소 크기. 넘으면 릴리스 자산 |

## 8. 단계와 완료 기준

**단계 0. 설정 변경 없이(오늘).**

- 수집소 쪽: 경로 A·B로 L3를 다시 매긴다(L3d·L3s 표시). 표본 추정 약 1,290개. 번역된 인용은 L3 대상에서 빼고 dot에 원문 문장으로 고쳐 달라고 요청한다(REQUESTS.md Q번호).
- 구현 쪽: 포착 기록 형식(4.4)을 `adapters/http.py`가 읽고, 재생 디렉터리를 여럿 받게 한다. 관측에 `binding`·`capture_ref`, `fetch_log.outcome`에 4.9절 다섯을 더한다. 원천 대응 표와 결정적 대조기를 장부 쪽 모듈로 둔다. 완료 기준: 지금 시험이 모두 통과하고, `docs.python.org` 서랍 후보(I7의 세마포어)가 B로 `cpython/3.13/Doc/library/asyncio-sync.rst`에서 L3s 관측이 된다.

**단계 1. 포착 환경(준혁님 승인 뒤).**

- 이 스레드가 환경 "원문 포착"(Full)과 예약 작업을 만든다. 둘 다 준혁님 화면에 승인 카드가 뜬다.
- 수집소 쪽에 `tools/capture.py`를 두고 C 대상을 돈다. 완료 기준: 이틀 뒤 C 대상의 경로별 결과 표(C18·C19), L3d 증가, 304 비율.
- 구현 쪽: EVAL-X1을 포착물로 다시 돌린다. 완료 기준: 06 3.4 단위 2 기준 셋이 포착 시각으로 맞고, 313578에서 알림 0.

**단계 2. 실패 승급.** 경로 D(보관소)와 경로 E(사용자 기기)를 켠다. E는 비공개 관측 표가 정해진 뒤다.

구현 세션에 넘길 짧은 지시는 프로젝트 파일 `prompts/source-access-unit.md`에 있다.

## 출처

- 측정: [access/out/reach.tsv](access/out/reach.tsv), [access/out/routes40.json](access/out/routes40.json), [access/out/post40.json](access/out/post40.json), [access/out/model_read_probe.md](access/out/model_read_probe.md)
- Claude Code [cloud environments](https://code.claude.com/docs/en/cloud-environments) (Access levels, GitHub proxy, Default allowed domains, Time limits)
- Codex [agent internet access](https://learn.chatgpt.com/docs/cloud/internet-access)
- GitHub Copilot [customize the agent firewall](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-firewall)
- GitHub [terms for additional products and features](https://github.com/github/docs/blob/main/content/site-policy/github-terms/github-terms-for-additional-products-and-features.md) (Actions)
- Internet Archive [Wayback API](https://archive.org/help/wayback_api.php), [CDX server README](https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md)
- Common Crawl [CDXJ index](https://commoncrawl.org/cdxj-index)
- Ainsworth, AlSum, SalahEldeen, Weigle, Nelson, [How Much of the Web Is Archived?](https://arxiv.org/abs/1212.6177)
- [RFC 7089 Memento](https://datatracker.ietf.org/doc/rfc7089), [Robust Links](https://mementoweb.org/robustlinks/spec/), [RFC 9309 robots](https://datatracker.ietf.org/doc/rfc9309)
- Zittrain 외 Perma 논문([Harvard Law Review Forum](https://harvardlawreview.org/forum/vol-127/perma-scoping-and-addressing-the-problem-of-link-and-reference-rot-in-legal-citations/)), [ABA Journal 기사](https://www.abajournal.com/news/article/link_rot_int_scotus_decisions_documented_half_dont_go_to_original_material)
- Webrecorder [WACZ 1.1.1](https://specs.webrecorder.net/wacz/1.1.1)
