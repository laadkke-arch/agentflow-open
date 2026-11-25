# 재현 절차와 대조

## 실행 환경과 입력 고정

주관측은 Linux x64 6.18.57, Node 24.22.1, Playwright Core 1.51.1, Chromium 156.0.8078.79 headless, CDP 1.3, parse5 7.3.0에서 실행했다. 1,280×800 px, en-US, UTC, 매 호출에 새 browser context와 새 document를 썼다. 브라우저 런처·바이너리·드라이버·입력 SHA-256은 [주환경](receipts/runs/environment.json)과 [재생 환경](receipts/replay/axe/environment.json)에 있다.

[inputs.json](inputs.json)과 [fixtures](fixtures/)의 4개 주 입력은 235의 HTML과 세 옵션을 고정한다. 235의 wrapper 제목 `AF235`도 보존했다. 상대 경로 이미지 `x`, `y`는 about:blank 새 문서에서 사용했다. 각 `.case.json`은 주입 전 DOM, 실제 옵션, `axe.version`, 대상 rule 목록, 콘솔, UTC와 파일 지문을 보존한다. 대응 `.json`은 API가 반환한 객체 전체를 JSON으로 직렬화한 것이다.

4.7.2와 4.8.0의 공식 npm tarball을 다시 받아 registry SHA-1, lock 및 registry SRI SHA-512, Git 태그와 registry `gitHead`, tar member와 설치된 `axe.min.js`의 바이트 동등성을 확인했다. 실행 파일 SHA-256은 [배포물 검증](receipts/builds/builds.json)에 있다. 설치는 도구 캐시 권한 오류(ENOENT) 후 쓰기 가능한 /tmp 캐시에서 성공했다. npm install 스크립트는 껐다. [라이브러리 메타데이터·버전·해시](receipts/builds/)와 [고정 lock](deps/package-lock.json)이 재현 입력이다. 소스에서 새로 빌드한 바이너리의 동등성은 미실시다.

## 공개 원자료에서 재생

저장소 root에서 실행한다. 아래 명령은 새 scratch에 출력을 둔다. 현재 저장소의 보고 원자료를 다시 쓸 때는 해당 scratch를 그대로 보관해 비교한다.

```bash
o=docs/workstreams/research/AF-RES-253
sandbox=$(mktemp -d)
mkdir -p "$sandbox/deps"
cp "$o/deps/package.json" "$o/deps/package-lock.json" "$sandbox/deps/"
export AF253_DEPS="$sandbox/deps"
export AF253_BUILD_RECEIPT="$sandbox/builds.json"
npm ci --prefix "$AF253_DEPS" --cache "$sandbox/npm-cache" --ignore-scripts --no-audit --no-fund --no-update-notifier
python "$o/verify-builds.py" "$AF253_DEPS" > "$AF253_BUILD_RECEIPT"
git ls-remote https://github.com/dequelabs/axe-core.git 'refs/tags/v4.7.2*' 'refs/tags/v4.8.0*'

record() {
  local out=$1
  shift
  mkdir -p "$out"
  "$@" > "$out/run.stdout" 2> "$out/run.stderr"
  local code=$?
  printf '%s\n' "$code" > "$out/run.exit"
  return "$code"
}
record "$sandbox/axe" node "$o/run.mjs" main "$sandbox/axe"
record "$sandbox/aria-controls" node "$o/run.mjs" aria-controls "$sandbox/aria-controls"
```

기본 Chromium은 `/usr/bin/chromium`이다. 설치 경로가 다르면 `AF253_CHROMIUM`, wrapper와 실제 바이너리 경로가 다르면 `AF253_CHROMIUM_BINARY`를 지정한다. 실제 24호출은 `node "$o/run.mjs" main "$o/receipts/runs"`의 [exit/stdout/stderr](receipts/runs/)에 보존했다. `aria-controls`는 원문, span 순서 반전, 첫 span의 ID 변경, 둘째 span의 ID 변경을 판·모드별로 실행한다. 총 24회 중 원문과 요청 통제 18회, 둘째 span ID 변경 반례 6회다. 각 통제의 CDP AX 원값은 해당 [통제 영수증](receipts/runs/aria-controls/)의 `accessibility.axNodes`에 있다.

`www.w3.org`, `www.rfc-editor.org`에 정상적인 원격 요청이 가능한 실행 환경에서 아래를 이어서 실행한다. 첫 호출은 5 URL의 redirect 단계, Content-Type, UTC, 길이, SHA-256을 기록한다. 두 번째 호출은 WCAG 6개 및 RFC 2개 fragment의 직접 탐색을 검사하며, origin GET 바이트가 있으면 parse5와 Chromium 같은 바이트 비교를 추가한다. replay 경로에서는 문서 하위 리소스 요청을 차단한다. 도착한 문서의 발행일·절 제목·상태와 브라우저의 해시·위치를 함께 본다.

```bash
record "$sandbox/http" node "$o/fetch-pages.mjs" "$sandbox/page-bytes" "$sandbox/http"
record "$sandbox/origins" node "$o/run.mjs" anchors "$sandbox/origins" "$sandbox/page-bytes" "$sandbox/http"
```

이번 초기 5 GET는 [페이지 HTTP 영수증](receipts/pages/)으로 남겼다. 명령은 종료 1, 개별 curl 종료 56이었다. 이어서 [Chromium 원격 탐색](receipts/pages/browser/) 8회를 실행해 종료 1과 각 터널 오류를 기록했다. 제공된 Cloud의 제한 정책에서 두 호스트는 허용 목록에 없었다. 재생 준비 때 [정책](receipts/replay/network.json)을 다시 확인했고 같은 제한이 적용됐다. 원 게시 HTML과 origin target의 관측은 미확인이다.

## 별도 폴더 재생

주관측 SHA `e8e29011c0270d09cc2c67508e3bb52e677703d4`의 소유 경로를 `git archive`로 별도 폴더에 풀었다. `npm ci`와 배포물 검증을 독립 cache에서 실행했다. 해당 폴더에서 `node run.mjs default OUT`을 실행하면 기본 모드 8개를 새 프로필로 반복한다. 수신이 허용된 환경에서는 같은 폴더에 별도 HTTP/바이트 디렉터리를 주어 `fetch-pages.mjs`와 `run.mjs anchors`도 반복한다.

```bash
replay_checkout="$sandbox/replay-checkout"
mkdir -p "$replay_checkout"
git archive HEAD "$o" | tar -x -C "$replay_checkout"
npm ci --prefix "$replay_checkout/$o/deps" --cache "$sandbox/replay-cache" --ignore-scripts --no-audit --no-fund --no-update-notifier
python "$replay_checkout/$o/verify-builds.py" "$replay_checkout/$o/deps" > "$sandbox/replay-builds.json"
AF253_DEPS="$replay_checkout/$o/deps" AF253_BUILD_RECEIPT="$sandbox/replay-builds.json" \
  record "$sandbox/default-replay" node "$replay_checkout/$o/run.mjs" default "$sandbox/default-replay"
```

[비교 JSON](receipts/replay/comparison.json)은 두 원 dump의 SHA-256, top-level 차이, 입력·환경과 정규화 결과를 모두 기록한다. `python "$o/compare.py"`로 저장된 두 폴더의 비교를 재계산한다. 정규화에서 제거한 필드는 각 호출의 최상단 `timestamp` 하나다. 객체 키는 정렬해 변환하고 배열·노드·selector 순서는 보존한다.

## 앵커 검사기의 반례

합성 HTML을 처음과 별도 폴더에서 실행했다. `anchor-controls`는 실제 날짜판 탐색과 별도의 입력군이다. [입력](fixtures/anchor-controls.html)과 [원 관측](receipts/pages/controls/), [재생](receipts/replay/anchor-controls/)을 보존했다.

| fragment | 파서의 적격 요소 수 | Chromium :target과 위치 |
| --- | --- | --- |
| legacy | 1 · a[name] | a[name=legacy], Legacy anchor section · 968 px |
| duplicate | 2 · id | 첫 section#duplicate, First duplicate · 1,821 px |
| priority | 2 · a[name] 하나와 id 하나 | 뒤에 나오는 section#priority, ID wins · 3,621 px |
| missing | 0 | :target 없음 · 0 px |
| other-name | 0 · input[name] 문자열 일치 1개 | :target 없음 · 0 px |

W3C Git의 `WCAG22-20231005` 태그가 가리키는 개발 커밋은 `732353ba0ce6193afc262d432d5dfba50c0eff59` (2024-02-01)이다. 작성 원파일 두 개는 각각 section ID 1개이고 같은 Chromium에서 해당 :target에 도착했다. `parsing`의 H4는 제거 표지, `non-text-content`는 존속 절이다. 전체 페이지는 ReSpec include를 쓰므로 원 게시 HTML·페이지 위치는 미확인이다. [작성 Parsing](https://github.com/w3c/wcag/blob/732353ba0ce6193afc262d432d5dfba50c0eff59/guidelines/sc/20/parsing.html) · [작성 Non-text Content](https://github.com/w3c/wcag/blob/732353ba0ce6193afc262d432d5dfba50c0eff59/guidelines/sc/20/non-text-content.html) · [작성 index](https://github.com/w3c/wcag/blob/732353ba0ce6193afc262d432d5dfba50c0eff59/guidelines/index.html)

```bash
git init "$sandbox/w3c"
git -C "$sandbox/w3c" fetch --depth=1 https://github.com/w3c/wcag.git refs/tags/WCAG22-20231005:refs/tags/WCAG22-20231005
mkdir -p "$sandbox/w3c-fragments"
for fragment in parsing non-text-content; do
  git -C "$sandbox/w3c" show "732353ba0ce6193afc262d432d5dfba50c0eff59:guidelines/sc/20/$fragment.html" \
    > "$sandbox/w3c-fragments/$fragment.html"
done
record "$sandbox/anchor-controls" node "$o/run.mjs" anchor-controls "$sandbox/anchor-controls" "$sandbox/w3c-fragments"
```

## RFC 공식 HTML 대조

| 자료 | 후보 fragment | 원 본문 | 파서 및 Chromium |
| --- | --- | --- | --- |
| [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html#section-1) | section-1 | §1은 MUST 계열의 요구 수준을 정의 | 원바이트 미확인 · [HTTP](receipts/pages/RFC2119.http.json) · [Chromium](receipts/pages/browser/RFC2119--section-1.json) |
| [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html#section-2) | section-2 | 헤더와 §1에 Updates 2119. §2는 대문자 적용 범위와 두 RFC를 함께 참조하는 문구 | 원바이트 미확인 · [HTTP](receipts/pages/RFC8174.http.json) · [Chromium](receipts/pages/browser/RFC8174--section-2.json) |

RFC Editor의 [BCP 14 원장](https://www.rfc-editor.org/info/bcp14/)에는 두 RFC가 모두 있고, [RFC 7322 §4.1.4](https://www.rfc-editor.org/rfc/rfc7322.html#section-4.1.4)는 Updates와 Obsoletes를 원발행 헤더에 표시하는 방식을 기록한다. 실제 fragment 접근 성공 여부와 명제·관계 종류는 별도 값이다. 같은 Obsoletes 표기의 범위도 본문과 함께 읽는다. RFC 7230 일부에 대해 공통 의미는 9110, HTTP/1.1 메시지 구문과 처리 범위는 9112로 나뉜 사례가 있다. [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) · [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.html)
