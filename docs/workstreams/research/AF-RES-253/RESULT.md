# 표 1

한 행은 W3C 최초 날짜판의 fragment 하나다. 3판×2기준=6행. 셸과 Chromium 원격 탐색을 각각 시도했다. 본문 상태는 공식 원페이지 텍스트에서 읽은 6절의 판정이다.

| 날짜판·fragment | HTTP·파일 지문 | 실제 일치 요소·절 제목 | 브라우저 도착 | 본문 상태 | 영수증·미확인 |
| --- | --- | --- | --- | --- | --- |
| [2.0 · 2008-12-11 #ensure-compat-parses](https://www.w3.org/TR/2008/REC-WCAG20-20081211/#ensure-compat-parses) | CONNECT 403 · origin 상태·지문 미확인 | 요소 미확인 · 본문 Parsing | 미확인 · 터널 단계 실패 | A · 원 요구 4조건 | [W20 HTTP](receipts/pages/W20.http.json) · [Chromium](receipts/pages/browser/W20--ensure-compat-parses.json) |
| [2.0 · 2008-12-11 #text-equiv-all](https://www.w3.org/TR/2008/REC-WCAG20-20081211/#text-equiv-all) | CONNECT 403 · origin 상태·지문 미확인 | 요소 미확인 · 본문 Non-text Content | 미확인 · 터널 단계 실패 | A · 동등 목적 · Controls → Guideline 4.1 | [W20 HTTP](receipts/pages/W20.http.json) · [Chromium](receipts/pages/browser/W20--text-equiv-all.json) |
| [2.1 · 2018-06-05 #parsing](https://www.w3.org/TR/2018/REC-WCAG21-20180605/#parsing) | CONNECT 403 · origin 상태·지문 미확인 | 요소 미확인 · 본문 Success Criterion 4.1.1 Parsing | 미확인 · 터널 단계 실패 | A · 원 요구 4조건 | [W21 HTTP](receipts/pages/W21.http.json) · [Chromium](receipts/pages/browser/W21--parsing.json) |
| [2.1 · 2018-06-05 #non-text-content](https://www.w3.org/TR/2018/REC-WCAG21-20180605/#non-text-content) | CONNECT 403 · origin 상태·지문 미확인 | 요소 미확인 · 본문 Success Criterion 1.1.1 Non-text Content | 미확인 · 터널 단계 실패 | A · 동등 목적 · Controls → SC 4.1.2 | [W21 HTTP](receipts/pages/W21.http.json) · [Chromium](receipts/pages/browser/W21--non-text-content.json) |
| [2.2 · 2023-10-05 #parsing](https://www.w3.org/TR/2023/REC-WCAG22-20231005/#parsing) | CONNECT 403 · origin 상태·지문 미확인 | 요소 미확인 · 본문 Success Criterion 4.1.1 Parsing (Obsolete and removed) | 미확인 · 터널 단계 실패 | 제거 표지와 이유 | [W22 HTTP](receipts/pages/W22.http.json) · [Chromium](receipts/pages/browser/W22--parsing.json) |
| [2.2 · 2023-10-05 #non-text-content](https://www.w3.org/TR/2023/REC-WCAG22-20231005/#non-text-content) | CONNECT 403 · origin 상태·지문 미확인 | 요소 미확인 · 본문 Success Criterion 1.1.1 Non-text Content | 미확인 · 터널 단계 실패 | A · 동등 목적 · Controls → SC 4.1.2 | [W22 HTTP](receipts/pages/W22.http.json) · [Chromium](receipts/pages/browser/W22--non-text-content.json) |

# 표 2

한 행은 한 새 문서의 axe.run 호출이다. 2판×4입력×3모드=24행. V/I/P/NA는 violations/incomplete/passes/inapplicable의 규칙 항목 수 순서다. 대상은 지정 4 ID이며 전체 수에는 그 밖의 규칙이 포함된다. 한 규칙이 다른 노드의 V와 P에 함께 나올 수 있다. NA의 노드 배열은 비어 있고 미보고는 네 배열 모두에 없는 것이다. [rules.csv](rules.csv)는 호출×규칙 96행으로 태그·노드·공석을 기록한다.

| axe 판·입력·모드 | 실제 rule·노드 | 4종 결과 분류 | 동일 조건 재생 | 235 기대와 차이 | 원 JSON |
| --- | --- | --- | --- | --- | --- |
| 4.7.2 · plain · default | V `duplicate-id` → `p:nth-child(1)` | 대상 1/0/0/3 · 미보고 0 · 전체 4/0/5/77 | [정규화 일치](receipts/replay/comparison.json) | 235 violation · wcag411 · 일치 | [JSON](receipts/runs/4.7.2--plain--default.json) · [조건](receipts/runs/4.7.2--plain--default.case.json) |
| 4.7.2 · plain · wcag2a | V `duplicate-id` → `p:nth-child(1)` | 대상 1/0/0/3 · 미보고 0 · 전체 1/0/4/50 | 대표 범위 밖 | 235 violation · wcag411 · 일치 | [JSON](receipts/runs/4.7.2--plain--wcag2a.json) · [조건](receipts/runs/4.7.2--plain--wcag2a.case.json) |
| 4.7.2 · plain · explicit | V `duplicate-id` → `p:nth-child(1)` | 대상 1/0/0/3 · 미보고 0 · 전체 1/0/0/3 | 대표 범위 밖 | 235 violation · wcag411 · 일치 | [JSON](receipts/runs/4.7.2--plain--explicit.json) · [조건](receipts/runs/4.7.2--plain--explicit.case.json) |
| 4.7.2 · active · default | V `duplicate-id-active` → `button:nth-child(1)` | 대상 1/0/0/3 · 미보고 0 · 전체 3/0/8/75 | [정규화 일치](receipts/replay/comparison.json) | 235 violation · wcag411 · 일치 | [JSON](receipts/runs/4.7.2--active--default.json) · [조건](receipts/runs/4.7.2--active--default.case.json) |
| 4.7.2 · active · wcag2a | V `duplicate-id-active` → `button:nth-child(1)` | 대상 1/0/0/3 · 미보고 0 · 전체 1/0/6/48 | 대표 범위 밖 | 235 violation · wcag411 · 일치 | [JSON](receipts/runs/4.7.2--active--wcag2a.json) · [조건](receipts/runs/4.7.2--active--wcag2a.case.json) |
| 4.7.2 · active · explicit | V `duplicate-id-active` → `button:nth-child(1)` | 대상 1/0/0/3 · 미보고 0 · 전체 1/0/0/3 | 대표 범위 밖 | 235 violation · wcag411 · 일치 | [JSON](receipts/runs/4.7.2--active--explicit.json) · [조건](receipts/runs/4.7.2--active--explicit.case.json) |
| 4.7.2 · aria · default | V `duplicate-id-aria` → `span:nth-child(1)` | 대상 1/0/0/3 · 미보고 0 · 전체 4/0/11/72 | [정규화 일치](receipts/replay/comparison.json) | 235 violation · wcag411 · 일치 | [JSON](receipts/runs/4.7.2--aria--default.json) · [조건](receipts/runs/4.7.2--aria--default.case.json) |
| 4.7.2 · aria · wcag2a | V `duplicate-id-aria` → `span:nth-child(1)` | 대상 1/0/0/3 · 미보고 0 · 전체 1/0/9/45 | 대표 범위 밖 | 235 violation · wcag411 · 일치 | [JSON](receipts/runs/4.7.2--aria--wcag2a.json) · [조건](receipts/runs/4.7.2--aria--wcag2a.case.json) |
| 4.7.2 · aria · explicit | V `duplicate-id-aria` → `span:nth-child(1)` | 대상 1/0/0/3 · 미보고 0 · 전체 1/0/0/3 | 대표 범위 밖 | 235 violation · wcag411 · 일치 | [JSON](receipts/runs/4.7.2--aria--explicit.json) · [조건](receipts/runs/4.7.2--aria--explicit.case.json) |
| 4.7.2 · control · default | V `image-alt` → `img[src="x"]` / P `image-alt` → `img[src="y"]` | 대상 1/0/1/3 · 미보고 0 · 전체 4/0/7/76 | [정규화 일치](receipts/replay/comparison.json) | 235 wcag111 · 사전 V/P 가설 · wcag111 일치, 노드별 V/P 추가 관측 | [JSON](receipts/runs/4.7.2--control--default.json) · [조건](receipts/runs/4.7.2--control--default.case.json) |
| 4.7.2 · control · wcag2a | V `image-alt` → `img[src="x"]` / P `image-alt` → `img[src="y"]` | 대상 1/0/1/3 · 미보고 0 · 전체 1/0/6/49 | 대표 범위 밖 | 235 wcag111 · 사전 V/P 가설 · wcag111 일치, 노드별 V/P 추가 관측 | [JSON](receipts/runs/4.7.2--control--wcag2a.json) · [조건](receipts/runs/4.7.2--control--wcag2a.case.json) |
| 4.7.2 · control · explicit | V `image-alt` → `img[src="x"]` / P `image-alt` → `img[src="y"]` | 대상 1/0/1/3 · 미보고 0 · 전체 1/0/1/3 | 대표 범위 밖 | 235 wcag111 · 사전 V/P 가설 · wcag111 일치, 노드별 V/P 추가 관측 | [JSON](receipts/runs/4.7.2--control--explicit.json) · [조건](receipts/runs/4.7.2--control--explicit.case.json) |
| 4.8.0 · plain · default | 대상에서 보고 노드 0 | 대상 0/0/0/2 · 미보고 2 · 전체 3/0/5/80 | [정규화 일치](receipts/replay/comparison.json) | default 미보고 · 일치 | [JSON](receipts/runs/4.8.0--plain--default.json) · [조건](receipts/runs/4.8.0--plain--default.case.json) |
| 4.8.0 · plain · wcag2a | 대상에서 보고 노드 0 | 대상 0/0/0/2 · 미보고 2 · 전체 0/0/4/53 | 대표 범위 밖 | wcag2a 미보고 · 일치 | [JSON](receipts/runs/4.8.0--plain--wcag2a.json) · [조건](receipts/runs/4.8.0--plain--wcag2a.case.json) |
| 4.8.0 · plain · explicit | V `duplicate-id` → `p:nth-child(1)` | 대상 1/0/0/3 · 미보고 0 · 전체 1/0/0/3 | 대표 범위 밖 | 235 violation · wcag411 · 일치 | [JSON](receipts/runs/4.8.0--plain--explicit.json) · [조건](receipts/runs/4.8.0--plain--explicit.case.json) |
| 4.8.0 · active · default | 대상에서 보고 노드 0 | 대상 0/0/0/2 · 미보고 2 · 전체 2/0/8/78 | [정규화 일치](receipts/replay/comparison.json) | default 미보고 · 일치 | [JSON](receipts/runs/4.8.0--active--default.json) · [조건](receipts/runs/4.8.0--active--default.case.json) |
| 4.8.0 · active · wcag2a | 대상에서 보고 노드 0 | 대상 0/0/0/2 · 미보고 2 · 전체 0/0/6/51 | 대표 범위 밖 | wcag2a 미보고 · 일치 | [JSON](receipts/runs/4.8.0--active--wcag2a.json) · [조건](receipts/runs/4.8.0--active--wcag2a.case.json) |
| 4.8.0 · active · explicit | V `duplicate-id-active` → `button:nth-child(1)` | 대상 1/0/0/3 · 미보고 0 · 전체 1/0/0/3 | 대표 범위 밖 | 235 violation · wcag411 · 일치 | [JSON](receipts/runs/4.8.0--active--explicit.json) · [조건](receipts/runs/4.8.0--active--explicit.case.json) |
| 4.8.0 · aria · default | I `duplicate-id-aria` → `span:nth-child(1)` | 대상 0/1/0/1 · 미보고 2 · 전체 3/1/13/72 | [정규화 일치](receipts/replay/comparison.json) | 235 incomplete · wcag412 · 일치 | [JSON](receipts/runs/4.8.0--aria--default.json) · [조건](receipts/runs/4.8.0--aria--default.case.json) |
| 4.8.0 · aria · wcag2a | I `duplicate-id-aria` → `span:nth-child(1)` | 대상 0/1/0/1 · 미보고 2 · 전체 0/1/11/45 | 대표 범위 밖 | 235 incomplete · wcag412 · 일치 | [JSON](receipts/runs/4.8.0--aria--wcag2a.json) · [조건](receipts/runs/4.8.0--aria--wcag2a.case.json) |
| 4.8.0 · aria · explicit | I `duplicate-id-aria` → `span:nth-child(1)` | 대상 0/1/0/3 · 미보고 0 · 전체 0/1/0/3 | 대표 범위 밖 | 235 incomplete · wcag412 · 일치 | [JSON](receipts/runs/4.8.0--aria--explicit.json) · [조건](receipts/runs/4.8.0--aria--explicit.case.json) |
| 4.8.0 · control · default | V `image-alt` → `img[src="x"]` / P `image-alt` → `img[src="y"]` | 대상 1/0/1/1 · 미보고 2 · 전체 4/0/7/78 | [정규화 일치](receipts/replay/comparison.json) | 235 wcag111 · 사전 V/P 가설 · wcag111 일치, 노드별 V/P 추가 관측 | [JSON](receipts/runs/4.8.0--control--default.json) · [조건](receipts/runs/4.8.0--control--default.case.json) |
| 4.8.0 · control · wcag2a | V `image-alt` → `img[src="x"]` / P `image-alt` → `img[src="y"]` | 대상 1/0/1/1 · 미보고 2 · 전체 1/0/6/51 | 대표 범위 밖 | 235 wcag111 · 사전 V/P 가설 · wcag111 일치, 노드별 V/P 추가 관측 | [JSON](receipts/runs/4.8.0--control--wcag2a.json) · [조건](receipts/runs/4.8.0--control--wcag2a.case.json) |
| 4.8.0 · control · explicit | V `image-alt` → `img[src="x"]` / P `image-alt` → `img[src="y"]` | 대상 1/0/1/3 · 미보고 0 · 전체 1/0/1/3 | 대표 범위 밖 | 235 wcag111 · 사전 V/P 가설 · wcag111 일치, 노드별 V/P 추가 관측 | [JSON](receipts/runs/4.8.0--control--explicit.json) · [조건](receipts/runs/4.8.0--control--explicit.case.json) |

# Q1. 날짜판 원페이지 수신

세 W3C 날짜판의 공개 본문을 직접 읽어 판·발행일과 6절의 문구를 확인했다. Cloud 셸에서 같은 3 URL의 원바이트 수신은 0/3이다. 2026-11-24 23:53:46 UTC의 HTTPS CONNECT가 프록시에서 403을 반환했다. `curl`의 종료 코드는 56, `http_code=0`은 origin 응답을 받기 전 종료한 기록이다. 따라서 origin HTTP 코드·최종 응답 URL·redirect·Content-Type·파일 길이·바이트 지문은 미확인이다. 프록시 응답은 별도 레코드다. 요청에 fragment를 넣지 않았으며 fragment 선택은 열린 문서에서 이뤄진다. [HTTP 원영수증](receipts/pages/) · [HTML의 indicated part 알고리즘 D01](https://html.spec.whatwg.org/multipage/browsing-the-web.html#scroll-to-fragid)

반례로 찾은 W3C Git 태그의 날짜 이름은 원 전송 지문을 제공하지 않는다. `WCAG22-20231005`가 가리키는 2024-02-01의 개발 커밋에는 ReSpec include가 있는 소스가 있고, 원 게시물의 제목·배치는 달라질 수 있다. [작성 index G03](https://github.com/w3c/wcag/blob/732353ba0ce6193afc262d432d5dfba50c0eff59/guidelines/index.html) · [태그 영수증](receipts/pages/authoring-tags.stdout)

# Q2. 실제 요소·절·브라우저

Chrome 156의 여섯 공식 URL 탐색이 모두 `ERR_TUNNEL_CONNECTION_FAILED`였다. [anchors.csv](anchors.csv)의 공란은 일치 0개를 의미하는 수치 0과 구분된다. 각 페이지의 본문은 Parsing 두 옛 판의 A 요구, 2.2의 제거 표지, 1.1.1 세 판의 동등 목적과 예외를 보여준다. 2.0의 Controls 참조는 Guideline 4.1이고 2.1/2.2에서는 SC 4.1.2다. [2.0 W20](https://www.w3.org/TR/2008/REC-WCAG20-20081211/) · [2.1 W21](https://www.w3.org/TR/2018/REC-WCAG21-20180605/) · [2.2 W22](https://www.w3.org/TR/2023/REC-WCAG22-20231005/) · [2.0 정오표 W04](https://www.w3.org/WAI/WCAG20/errata/)

2.0 정오표 #13과 2.1 정오표/재발행은 HTML/XML 충족 간주 해석을 기록하고, 2.2 날짜판은 4.1.1을 제거했다. 2.1 2023 재발행에서 A 본문과 두 노트가 공존한다. 현재 Parsing 해설에는 제거 표지와 역사적 원문 인용이 동시에 보인다. 본문의 문자열 존재만 검사하면 이 해설에 남은 역사 인용을 새 요구로 읽을 수 있다. 2.0 #13 개별 최초 공개일과 235의 일부 정정 시점은 미확인 상태를 유지한다. [2.1 정오표 W05](https://www.w3.org/WAI/WCAG21/errata/) · [WG 결의 W06](https://www.w3.org/2023/04/04-ag-minutes#item04) · [제거 PR W07](https://github.com/w3c/wcag/pull/2797) · [재발행 W08](https://www.w3.org/TR/2023/REC-WCAG21-20230921/#parsing) · [해설 W09](https://www.w3.org/WAI/WCAG22/Understanding/parsing.html)

별도 작성 소스를 실제 파서·브라우저에 넣었을 때 `section#parsing.sc` 한 개의 H4가 제거 표지를 보여주고, `section#non-text-content.sc` 한 개는 존속 절에 도착했다. 두 파일은 [Git 작성 소스](receipts/pages/controls/)로 표시했다. 합성 입력에서는 유일한 레거시 `a[name]`이 타깃이 됐고, 중복 `id`는 첫 요소, 같은 값의 앞선 `name`과 뒤의 `id`가 있으면 ID를 선택했다. `input[name]` 문자열 일치 1개와 아예 없는 fragment는 모두 적격 0개 및 `:target` 공석이었다. 따라서 매치 수, 선택 우선순위 및 스크롤을 분리해 기록해야 한다. [합성 입력과 비교표](replay.md#앵커-검사기의-반례) · [HTML 원문 D01](https://html.spec.whatwg.org/multipage/browsing-the-web.html#scroll-to-fragid)

# Q3. 바이너리·DOM·옵션

두 npm 배포물을 실제 내려받아 SHA-1 및 SRI와 맞추고 Git 태그와 registry `gitHead`를 대조했다. 4.7.2의 tarball 478,224 B와 `axe.min.js` 519,419 B, 4.8.0의 tarball 487,455 B와 `axe.min.js` 529,257 B를 검증했다. 24회 모두 묶음의 배포 파일 SHA-256과 `axe.version`·`testEngine.version`이 일치했다. 4.7.2의 2023-05-25 및 4.8.0의 2023-09-06 발행은 2.2 REC 이전이다. 소스에서 새로 빌드한 바이너리의 비교와 실제 사용자의 설치판은 미확인이다. [빌드 영수증](receipts/builds/builds.json) · [npm 4.7.2 N01](https://registry.npmjs.org/axe-core/4.7.2) · [npm 4.8.0 N02](https://registry.npmjs.org/axe-core/4.8.0) · [발행 A09](https://github.com/dequelabs/axe-core/blob/712026eb791ccd6469b4fa8934f819852c9949fc/CHANGELOG.md#L5)

각 호출은 새 Chromium context와 문서에서 235의 그대로인 body와 `AF235` 제목을 사용했다. [inputs.json](inputs.json)은 `{}`, `runOnly`의 단일 `wcag2a` 태그, 4 rule ID 및 각 `enabled:true`를 고정한다. `resultTypes`는 기본값이다. 기존 235가 제시한 예시의 판별 입력과 옵션을 보존하고, 단일 페이지에 세 모드를 연속 호출하는 대신 모드마다 문서를 새로 구성했다. 세 모드의 부수 규칙 수는 다를 수 있으므로 각 원배열과 네 지정 ID를 함께 읽는다. [환경·DOM 영수증](receipts/runs/) · [API D03](https://github.com/dequelabs/axe-core/blob/712026eb791ccd6469b4fa8934f819852c9949fc/doc/API.md)

# Q4. 호출 결과와 AF-RES-235 기대

- **4.7.2.** plain은 `duplicate-id`의 첫 `p`, active는 `duplicate-id-active`의 첫 `button`, aria는 `duplicate-id-aria`의 첫 `span`이 세 모드 모두 violations였다. 세 태그에 `wcag411`이 있었다. 235의 9개 중복 입력·모드 가설과 일치한다. [rules.csv](rules.csv) · [4.7.2 ARIA rule O03](https://github.com/dequelabs/axe-core/blob/b4f78df8fe5393efa0292f621c5dbca28eaa268c/lib/rules/duplicate-id-aria.json)
- **4.8.0.** generic/active 두 ID가 default와 `wcag2a`의 네 배열에서 사라진 경우는 2 ID×4입력×2모드=16셀이다. `axe.getRules()`에는 두 ID 및 `deprecated`·`wcag2a-obsolete`가 있다. explicit에서 plain/active의 첫 노드는 violations로 복원되고, 해당 규칙에 맞는 대상이 없는 곳에는 inapplicable이 나온다. 보고 누락과 rule 삭제, inapplicable과 규칙 비선택은 서로 다른 관측이다. [generic A01](https://github.com/dequelabs/axe-core/blob/712026eb791ccd6469b4fa8934f819852c9949fc/lib/rules/duplicate-id.json) · [active A02](https://github.com/dequelabs/axe-core/blob/712026eb791ccd6469b4fa8934f819852c9949fc/lib/rules/duplicate-id-active.json) · [폐기 결정 P01](https://github.com/dequelabs/axe-core/pull/4071)
- **ARIA 변경.** 4.8.0의 세 모드에서 같은 첫 span이 `duplicate-id-aria`의 incomplete 및 `wcag412`로 기록됐다. default 전체에는 같은 문서의 `landmark-one-main`, `page-has-heading-one`, `region` violations도 있다. 4.8.0 default ARIA에는 4.7.2에 없던 `aria-conditional-attr` 및 `aria-prohibited-attr` passes 두 항목도 관측했다. 이 부수 규칙은 235의 기대 범위 밖이다. [판정 변경 P02](https://github.com/dequelabs/axe-core/pull/4075) · [4.8.0 default ARIA 원 JSON](receipts/runs/4.8.0--aria--default.json) · [4.7.2 default ARIA 원 JSON](receipts/runs/4.7.2--aria--default.json)
- **image-alt 통제.** 여섯 호출 모두 `img[src="x"]`는 violations, `img[src="y"]`는 passes로 같은 `image-alt`의 서로 다른 버킷에 나타났다. `wcag111`은 유지되고 4.8.0에는 EN 태그가 추가됐다. 혼합 V/P의 실제 노드와 태그 차이는 235의 정적 매핑을 보완한다. `alt="A"`가 이미지 목적과 동등한지 판단하려면 출처 이미지와 사용 맥락이 필요하다. [4.8.0 rule A04](https://github.com/dequelabs/axe-core/blob/712026eb791ccd6469b4fa8934f819852c9949fc/lib/rules/image-alt.json) · [대조 원 JSON](receipts/runs/4.8.0--control--explicit.json)

대상 96개 호출×rule 셀에서 V 17, I 3, P 6, NA 60, 미보고 16을 확인했다. V/P를 함께 가진 image-alt 셀이 6개여서 버킷 수와 셀 수의 합이 다르다. 적용 가능성, 기본 활성, 태그 선택, 노드별 결과를 저장하면 같은 버전의 wrapper가 정책을 바꿀 때 다시 해석할 수 있다. 4.10.1 사용자의 태그 누락 제보와 Accessibility Insights의 4.8.4 채택 PR은 소비자별 설정과 도입 시점의 차이를 보여준다. 사용자의 과거 감사 원결과·제품 설치 환경은 이번 검산에서 미확인이다. [원 네 배열 D03](https://github.com/dequelabs/axe-core/blob/712026eb791ccd6469b4fa8934f819852c9949fc/doc/API.md#L638-L675) · [사용자 제보 X01](https://github.com/dequelabs/axe-core/issues/4753) · [제품 채택 X02](https://github.com/microsoft/accessibility-insights-web/pull/7274)

# Q5. DOM 참조·계산된 이름·axe 판정

요청 통제 18회에 유일하지만 의도와 다른 참조를 남기는 통제 6회를 추가했다. 각 변형·판에서 세 모드의 DOM·AX 결과가 일치했다. `aria-labelledby="n"` 토큰과 버튼 글자는 그대로 두었다. DOM의 첫 매치, `ariaLabelledByElements` 반영 대상 및 CDP AX 이름 출처가 아래와 같이 대조됐다.

| 입력 | 참조 span 위치 | Chromium AX 이름 | 4.7.2 duplicate-id-aria | 4.8.0 duplicate-id-aria |
| --- | --- | --- | --- | --- |
| 원문 | 첫째 | Wrong title | V · span:nth-child(1) | I · span:nth-child(1) |
| span 순서 반전 | 첫째, 텍스트 교체 | Intended title | V · span:nth-child(1) | I · span:nth-child(1) |
| 첫 span의 ID만 유일화 | 둘째 | Intended title | P · #n | P · #n |
| 둘째 span의 ID만 유일화 | 첫째 | Wrong title | P · #n | P · #n |

AX source의 backend DOM node ID가 통제에 따라 첫 span 또는 둘째 span ID를 가리켰다. 반전에서 axe의 selector 문자열은 같아도 `nodes[].html`의 span 텍스트가 바뀐다. 이를 selector 동등성만으로 합치면 이름 변화를 잃는다. 유일화는 중복 이슈를 해소했고 rule 자체는 passes에 남았다. 유일화 후에도 의도와 다른 span이 참조될 수 있다. 두 중복 fixture에서 `button-name`은 default에서 passes였으며 explicit의 선택 ID에는 포함되지 않는다. 실제 수정 작업에는 의도한 이름과 관계, 지원 브라우저/보조기술을 함께 검사할 근거가 필요하다. 화면낭독기 발화는 미실시다. [AX·원 JSON](receipts/runs/aria-controls/) · [AccName 1.1 D02](https://www.w3.org/TR/2018/REC-accname-1.1-20181218/#computation-steps) · [CDP 원정의 D04](https://github.com/ChromeDevTools/devtools-protocol/blob/45931384c3850a9abf9b393c4a72dc0c0764d677/pdl/domains/Accessibility.pdl) · [4.1.2 해설 W10](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html) · [H93 form label 반례 W11](https://www.w3.org/WAI/WCAG22/Techniques/html/H93)

# Q6. RFC의 발행 관계와 section

RFC Editor 공식 HTML에서 2119 §1의 요구 수준 정의와 8174 헤더 및 §1의 Updates 2119, §2의 대문자 적용 범위를 직접 읽었다. 8174의 §2에서는 BCP 14 의미가 대문자 표기에 적용되며 그러한 용어 없이도 규범 문장을 쓸 수 있다고 설명한다. BCP 14 원장에는 두 문서가 모두 등재돼 있다. 각각의 section 후보를 Chromium과 같은 파서 경로에 넣었으나 원 origin 접근 0/2로 실제 요소·도착은 미확인이다. [RFC 2119 R01](https://www.rfc-editor.org/rfc/rfc2119.html#section-1) · [RFC 8174 R02](https://www.rfc-editor.org/rfc/rfc8174.html#section-2) · [BCP 14 R03](https://www.rfc-editor.org/info/bcp14/) · [RFC 대조와 영수증](replay.md#rfc-공식-html-대조)

RFC 7322는 Updates와 Obsoletes를 헤더에 명시한다. RFC 9110과 9112는 둘 다 RFC 7230을 헤더에 열거하고, 실제 범위는 공통 HTTP 의미와 HTTP/1.1 구문·파싱으로 나뉜다. 예전 절 주소를 한 최신 문서로 일괄 교체하는 방법의 반례다. 대체 범위와 절 의미는 헤더와 본문으로 연결하고, 물리적 fragment 도착은 별도 검사로 보존한다. [편집 가이드 R04](https://www.rfc-editor.org/rfc/rfc7322.html#section-4.1.4) · [HTTP 의미 R05](https://www.rfc-editor.org/rfc/rfc9110.html) · [HTTP/1.1 R06](https://www.rfc-editor.org/rfc/rfc9112.html)

# Q7. 재생·원차이·정규화

주관측 커밋을 별도 폴더에 풀고 의존성을 새로 설치해 깨끗한 프로필에서 기본 모드 8/8을 재생했다. 8쌍의 원 JSON은 모두 달랐다. top-level 차이는 모두 `timestamp` 하나였으며, 그 값만 제거하면 전체 JSON이 8/8 일치했다. 입력 DOM, 적용 옵션, axe 파일 SHA-256과 환경 지문, 네 결과 배열·태그·노드 순서도 일치했다. 유형·노드를 정규화에서 버리는 방식은 사용 범위상 필요하지 않았다. 다른 브라우저, AT 및 릴리스의 안정성은 별도다. [두 dump와 해시](receipts/replay/comparison.json)

원 게시 WCAG 앵커 6개와 RFC 2개는 최초 차단 후 동일한 시행 정책을 확인했다. 재생 origin은 미실시, 실제 앵커는 8개 모두 미확인이다. 작성 소스 2개와 합성 앵커 5개는 새 프로필에서 7/7 원 dump가 같았다. 두 기존 환경의 결과가 정규화되더라도 원 URL에서 전달하는 판이나 바이트가 변할 여지는 남는다. [재생 정책과 비교](receipts/replay/) · [작성·합성 비교](replay.md#앵커-검사기의-반례)

# 비용·대안·추가 분석

주호출 24개의 첫 fixture 시작부터 마지막 종료까지 6.852초, 24개 API 원 JSON은 495,343 B였다. 별도 기본 재생은 2.514초 및 285,442 B였다. 두 값은 이번 환경의 관측으로 Chromium 기동, 다운로드·설치와 사람의 판독 시간은 공석이다. 변경 감지 비용을 줄이려면 먼저 날짜판·교정 사건과 rule 설정을 비교하고, 변경된 관측만 해당 바이트와 고정 fixture로 다시 확인할 수 있다. [주호출](receipts/runs/) · [재생](receipts/replay/axe/)

| 목적 | 적용 가능한 대안 | 대가와 한계 |
| --- | --- | --- |
| 옛 감사 편집자 | 당시 edition URL·fragment·도구판·raw JSON을 보존하고 정정 링크를 병기 | 이전 위반의 문구와 태그를 읽을 수 있다. 편집자가 적용 날짜와 실제 감사의 규칙 옵션을 검토해야 한다. |
| 새 HTML 개발자 | 영향받는 IDREF와 계산 이름부터 확인하고 현행 4.1.2 또는 관계 안내를 연결 | 순서 반전과 유일화 통제가 의도한 이름을 판별한다. 프로젝트의 목적과 AT 동작에는 별도 확인 비용이 든다. |
| 규칙 유지보수자 | 원본·모드·태그·버전·V/I/P/NA·미보고 상태를 함께 저장하고 explicit을 진단용으로 노출 | 예전 결과 재현과 변경 알림이 가능하다. 소비 제품 기본값과 원결과 버전 검증이 추가된다. |

안내 주석 하나가 충분한 1.1.1 교차 참조와, 원 요구가 제거된 4.1.1은 비용이 다르다. 과거 자료에는 날짜판과 새 안내를 함께 보관하는 방안이 가역적이다. 현행 수정 화면에서 링크 하나만 보여줄 때는 사용자의 목적, 현재판, 실제 관계 결함이 확인된 경우로 좁힐 수 있다. RFC처럼 후계 문서가 분기하면 절별 적용 범위를 함께 저장한다.

| 중요한 불일치 또는 약점 | 영향을 받는 판단 | 다음에 볼 구체적 원자료·검사 | 판정이 바뀌는 관측 |
| --- | --- | --- | --- |
| 고정 WCAG 3판과 RFC 2판의 원바이트 미확인. 작성 소스의 2개 ID만 실제 확인 | 표 1의 요소·제목·도착과 RFC section 도착 | [재현 절차](replay.md#공개-원자료에서-재생)의 두 원 호스트에서 5 GET와 Chromium 8 fragment 검증 | 동일 ID·절·위치이면 검증 완료, 0·복수·다른 절이면 결함 유형별 정정 |
| Chromium 한 판의 AX 이름, 실제 AT 발화·역사 감사 입력 미확인 | 현재 4.1.2 관련 안내와 과거 감사 보고서 연결 | 세 기존 ARIA 입력에서 Firefox/다른 브라우저 엔진과 실제 AT 이름·관계 비교. 날짜·버전·raw JSON이 갖춰진 공개 감사 원자료 확인 | 이름·대상이 엔진별로 바뀌거나 실제 wrapper 판정이 다르면 적용 범위를 조건부로 수정 |
| 유일화 후 의도와 다른 이름에도 `duplicate-id-aria` passes. 이미지 통제에서 목적 동등성 미확인 | 자동 pass를 안내 완료로 해석할지, 어떤 수동 근거가 필요한지 | 두 유일 ID 통제 원 JSON과 AX source, 동일 텍스트를 갖지만 목적이 다른 실제 이미지·버튼의 수동 평가 | 의도·UI 결과 또는 대체 텍스트 의미 불일치가 확인되면 별개 관계 및 목적 이슈를 연결 |
