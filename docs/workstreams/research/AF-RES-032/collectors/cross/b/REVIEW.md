# AF-RES-032 B01·B04·B06 — 사건부터 찾은 보조 시도

| 사건 | 질의/상한 | 후보 문서 계열/상한 | 실제로 관측한 소비자 | 엄격한 같은 참조의 교체·HTML 배포·날짜 사슬 | 현재 목적 판단 |
|---|---:|---:|---|---|---|
| B01 Yarn Classic 이관 계획, 2020-01-24 | 3/3 | 4/5 | Rails 6.0.2.1·6.0.3의 공식 버전 HTML. `package.json` 설명의 옛 href 유지. | 0/1. 다른 용도의 설치 링크 추가를 기존 배경 링크의 정정으로 세지 않았다. 최초 HTML 공개일과 완전한 중간 배포물 목록 미확인. | 유지: 현재 옛 경로가 Yarn 1 설명으로 301→200 이동한다. |
| B04 Google 도움말 통합 공지, 2020-11-11 | 3/3 | 2/5 | Sphinx Sitemap 2.1.0·2.2.0·2.2.1의 배포 source README, 현재 HTML. 같은 옛 URI 유지. | 0/1. 실제 sdist에 HTML이 없고 과거 HTMLzip도 404. source 배포와 HTML 노출을 합치지 않았다. | 보류: 새 공식 본문은 읽었지만 원 경로의 shell GET은 429, 도구는 redirect 뒤 조회 실패. |
| B06 HashiCorp Developer beta, 2022-06-21 | 3/3 | 3/5 | StarlingX 6.0·7.0·현재 공식 HTML의 Vault API 참조. 옛 href 유지. | 0/1. beta mirror 공개일은 확인되지만 redirect 시행일과 해당 HTML 최초 공개일이 미확인. | 유지: 옛 경로가 현재 API 설명으로 308→308→308→200 이동한다. |
| **합계** | **9/9** | **9/15** | 사건 3회, 최종 소비자 계열 3개 | **0/3**, 계산 적격 지연 0쌍, 우측 검열 0행 | 유지 2, 보류 1. 실제 독자 클릭·실패는 모두 미확인. |

봉인 입력은 `ffbce62e4c01459ebbfb006a5d6c67e425ed7c17`, 원격 blob은 `d31a257bdfcaea85ab7ac2507d146b5704636f61`이다. 소비자 질의를 시작하기 전에 이 입력을 고정했고 사건을 교체하지 않았다. 원장에 원문 25개를 기록했으며 중복·메타데이터·source-only 등에서 보수적으로 제외한 최소수 산입은 7개다. 이 7개는 A의 배포 문서 12개를 대신하지 않는다. 서로 다른 공식 notice 세 개는 루트 B-U01/B-U04/B-U06과 같은 원문이라 여기서 다시 산입하지 않는다.

## B01: 새 설치 링크와 기존 배경 링크는 다른 참조다

실제 읽은 [Rails 6.0.2.1 Getting Started](https://guides.rubyonrails.org/v6.0.2.1/getting_started.html)의 §3.2 표는 `package.json`에 필요한 npm 의존성을 적고 Yarn이 사용하는 파일이라고 설명하며 `https://yarnpkg.com/lang/en/`으로 연결한다. [6.0.3의 같은 표](https://guides.rubyonrails.org/v6.0.3/getting_started.html)에서도 이 href는 그대로다. 이 판에는 §3.1.3 설치 문단이 있고 그 문단의 다른 링크는 `https://classic.yarnpkg.com/en/docs/install`로 연결된다. 설치 예시의 기대 출력은 Yarn 1.22.0이다.

따라서 두 링크의 도메인이 다르다는 사실만 보고 “배경 링크를 Classic으로 정정했다”고 쓰면 같은 용도 연결이 끊어진다. 이 사례에서 관측한 것은 **기존 배경 링크 유지와 다른 설치 링크의 공존**이다. 두 공식 버전 페이지의 실제 HTML과 해시는 확보했지만, 그 HTML의 최초 배포 시각은 독립적인 build·출판 영수증으로 확인하지 못했다. HTTP `Last-Modified`는 각각 2019-12-18과 2020-05-06을 반환했으나 이를 최초 출판일로 사용하지 않는다.

현재 [옛 배경 링크](https://yarnpkg.com/lang/en/)는 실제 GET에서 `https://classic.yarnpkg.com/en/`로 301 이동한 뒤 200을 반환했다. 도착 본문은 Yarn 1 문서라는 표기와 의존성 관리 설명을 포함한다. [현재 Classic 설치 문서](https://classic.yarnpkg.com/en/docs/install)도 직접 읽었다. 이 관측은 현재 배경 읽기 목적을 지지한다. 2020년 이후 모든 날의 접근 가능성, 실제 설치 성공, Yarn 이관 시행 시각을 증명하지는 않는다.

대체 후보도 실패를 남겼다. CRAN `packer_0.0.6.tar.gz`의 HTML들은 UI 템플릿이며 빌드된 도움말이 아니었다. `rhino_0.6.4.tar.gz`는 실제 vignette HTML 두 개를 포함하지만 Yarn href가 없었고, 다음 `rhino_1.0.0.tar.gz`는 HTML 멤버가 없었다. JupyterLab의 추정 버전 1.2.6/1.2.x/2.0.x HTMLzip 경로는 모두 404였다. 마지막 경우는 **시도한 경로의 실패**이며 JupyterLab 전체에 역사 도움말이 없다는 결론은 아니다.

다음 최소 자료는 Rails 6.0.x의 날짜 있는 HTML build artifact 또는 전체 공식 HTML 배포 원장 한 개다. 현재까지는 어느 판이 “최초 교체판”인지 말하지 않는다.

## B04: 날짜 있는 source 배포가 있어도 HTML 판은 미확인이다

첫 후보 Django 3.0의 [실제 오프라인 ZIP](https://media.djangoproject.com/docs/django-docs-3.0-en.zip)을 열고 `ref/contrib/sitemaps.html`을 확인했다. Google ping URL과 News publisher 도움말은 있었지만 봉인 사건의 `support.google.com/webmasters` href는 없었다. 같은 Google 도메인이라는 이유로 다른 노출을 이 사건의 소비자로 채택하지 않았다.

다음 후보 [Sphinx Sitemap의 현재 Advanced Configuration](https://sphinx-sitemap.readthedocs.io/en/latest/advanced-configuration.html)은 여러 문서 판·언어의 sitemap을 하나의 index에 모으는 문맥에서 다음 실제 href를 사용한다.

`https://support.google.com/webmasters/answer/75712?hl=en`

공식 PyPI 원장을 직접 열어 2020–2024 source 배포 목록과 UTC를 확인했고, 세 tarball 안의 `README.rst`를 읽었다.

| source 배포 | PyPI 업로드 UTC | README의 목적/주소 | 빌드 HTML 멤버 |
|---|---|---|---:|
| 2.1.0 | 2020-02-23 01:19:10.837816Z | 여러 판·언어의 sitemap을 index에 모으기 / 위 old URI | 0 |
| 2.2.0 | 2020-08-06 02:13:55.526488Z | 같은 old URI | 0 |
| 2.2.1 | 2022-11-12 03:41:08.913002Z | 같은 old URI | 0 |

공식 PyPI 원장에서 2.2.0은 공지 전 마지막 sdist이고 2.2.1은 공지 후 첫 sdist다. 그 사이 추가 sdist는 0개다. 이는 **sdist 원장에 대한 진술**이며 최초 HTML 출판판이라는 진술이 아니다. 과거 2.1.0/v2.1.0/2.2.0 페이지와 HTMLzip 경로를 시도했으나 404였다. 현재 HTML만으로 2020년의 렌더링 결과를 재구성하지 않았다. `PKG-INFO`에 반복되는 README는 별도 원문으로 세지 않았다.

현재 원 경로는 두 관측 경로가 달랐다. 검색 서비스 직접 열기는 `developers.google.com/search/docs/advanced/sitemaps/large-sitemaps`로 이동하는 것을 관측했지만 뒤의 조회가 실패했다. 독립 shell GET은 Google의 429를 받았다. 이 실패를 모든 독자에게 발생한 404로 일반화하지 않았다. 관측된 공개 새 URI를 별도로 열었을 때 [현재 sitemap index 안내](https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps)는 200이었고, 여러 sitemap을 index에 모으는 설명·XML 예·필수 태그를 실제 읽을 수 있었다. **새 대상 200과 옛 경로의 전체 전달 200을 합치지 않았다.**

다음 최소 자료는 Sphinx Sitemap 2.2.0 또는 2.2.1의 날짜 있는 렌더링 HTML artifact 한 개다. 이 자료가 오면 source-only였던 고리를 배포 HTML과 연결할 수 있다. 실제 Google 개별 URI의 이관 시행 시각은 여전히 별도 근거가 필요하다.

## B06: 새 mirror가 생겼다는 공지는 옛 링크 실패의 시작이 아니다

[HashiCorp의 2022-06-21 공지](https://www.hashicorp.com/en/blog/new-hashicorp-developer-site-is-now-in-public-beta)는 Vault와 Waypoint 자료를 새 사이트에 mirror로 제공한다고 말한다. Learn과 제품별 사이트가 그날 중단됐다고 말하지 않는다. 이 beta 공개일을 redirect 시행일이나 독자 실패일로 사용하지 않는다.

첫 후보 `vaultr`의 실제 CRAN 1.1.0·1.1.1 tarball에는 `vaultr/inst/doc/vaultr.html`과 `packages.html`이 들어 있었다. 그 HTML을 열어 본 결과 참고 주소는 `vaultproject.io`의 KV/auth/dev-server 문서였고, 봉인한 Learn/Developer 주소는 없었다. DESCRIPTION의 출판 시각은 2021-06-09 14:00:02Z와 2022-08-22 11:30:02Z지만 이 날짜쌍을 다른 URI 사건의 지연 계산에 사용하지 않았다. 뒤의 `hvac` 후보도 v0.11.2 HTMLzip을 실제 열었다. ZIP 멤버는 89개였고 HTML의 href를 모두 검사했으나 Learn/Developer 주소가 없었다. 이는 프로그램으로 수행한 배제 검사이며 그 모든 페이지를 독립 원문 최소수로 세지 않았다.

검색으로 발견한 StarlingX에서는 [6.0](https://docs.starlingx.io/r/stx.6.0/usertasks/kubernetes/vault-aware.html), [7.0](https://docs.starlingx.io/r/stx.7.0/usertasks/kubernetes/vault-aware.html), [현재판](https://docs.starlingx.io/usertasks/kubernetes/vault-aware.html)의 실제 HTML을 읽었다. 모두 애플리케이션이 Vault REST API를 통해 secrets를 읽거나 쓰는 맥락에서 `https://learn.hashicorp.com/vault/getting-started/apis`를 참고 링크로 제공한다. 같은 본문은 하나의 중복 그룹으로 묶었다.

공식 [Documentation Archive](https://docs.starlingx.io/archive/index-documentation-archive-900988dce206.html)의 현재 HTML에서는 Release 6/7/8/9라는 서로 다른 라벨이 모두 같은 6.0 주소를 가리켰다. 라벨 수를 서로 다른 보존판 수로 세지 않고 7.0의 실제 URI를 따로 열었다. 현재 받은 6.0·7.0 파일의 HTTP 수정 시각은 2026년이며, 그 날짜를 2022년의 출판 시각으로 대체하지 않았다.

현재 old Learn href를 직접 GET했을 때 308 이동 세 번을 거쳐 [Vault HTTP API 학습 문서](https://developer.hashicorp.com/vault/tutorials/get-started/learn-http-api)에 200으로 도착했다. 현재 본문에는 HTTP API·토큰 헤더·인증 방법 설명이 있다. 이것은 API 설명을 찾아 읽는 목적을 지지한다. 본문의 현재 예제를 옛 StarlingX 환경에서 실행하거나 그 호환성을 검증한 것은 아니다.

다음 최소 자료는 StarlingX 6.0 또는 7.0의 해당 HTML을 날짜와 함께 고정한 build·공개 출판 영수증 한 개다. exact redirect 시행일은 beta 공지와 별도 자료로 입증해야 한다.

## 검산과 비용의 범위

`sources.jsonl`은 원문 URL·판·읽은 절·확인 UTC·해시·한계를, `references.jsonl`은 실제 HTML의 href·링크 텍스트·기준 URL·바이트 위치와 한국어 목적 요약을 보존한다. `attempts.jsonl`은 9개 질의, 9개 후보 계열, 42회의 공개 GET 및 실패를 기록한다. GET 수와 고유 원문 수는 다르다. 검색 질의의 정확한 실행 초는 따로 저장하지 못했으므로 사후 원장 작성 UTC를 실행 UTC로 위장하지 않았다. 각 shell GET의 시작·완료 UTC는 직접 기록했다.

검산은 같은 작업자의 재독이다. 실제 배포물 안의 HTML 존재 여부, raw href, source release 날짜와 HTTP 수정일의 구분, 계산 적격 0쌍, 원문 중복 산입을 다시 확인했다. 프로그램이나 설치 지침은 실행하지 않았다. 어떤 사례도 시작 시각이 불명확한 상태에서 우측 검열로 바꾸지 않았다.

Q8 가림 판독에서는 추가 오염 한 건이 있다. A L1/L2 봉인 후, 허용된 B 봉인 파일을 통째로 읽는 과정에서 B05의 IETF 2022 전환 계획 요약과 A-D04 중복 가능성 문구에 노출됐다. 즉시 루트에 알렸고 A-D04의 L3에 표시하도록 기록했다. L1/L2에는 이 노출이 없었다. B01/B04/B06 조사 중 다른 A의 최종 결과는 읽지 않았다.
