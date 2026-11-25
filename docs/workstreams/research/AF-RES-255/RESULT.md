| 시험·엔진·반복 | 빌드·폰트 | 원형 판정·픽셀 근거 | 실제 단어별 줄 | 예측·단언 차이 | 원영수증·미확인 |
|---|---|---|---|---|---|
| 002 · Chromium · 1 | 156.0.8078.79 · Ahem 20px · W 399.984 CSS px | PASS, exit 0 · `!=` · Δ 4,800/480,000 px | 123 567 901 / 345 789 123 | cut 3 관측. 공개 단언은 불일치. | [WPT](receipts/primary/chromium-002-r1/summary.json) · [좌표](receipts/geometry/chromium-002-r1/geometry.json) |
| 002 · Chromium · 2 | 156.0.8078.79 · Ahem 20px · W 399.984 CSS px | PASS, exit 0 · `!=` · Δ 4,800/480,000 px | 123 567 901 / 345 789 123 | cut 3 관측. 공개 단언은 불일치. | [WPT](receipts/primary/chromium-002-r2/summary.json) · [좌표](receipts/geometry/chromium-002-r2/geometry.json) |
| 002 · WebKitGTK · 1 | 2.54.3 · Ahem 20px · W 400.000 CSS px | PASS, exit 0 · `!=` · Δ 4,800/480,000 px | 123 567 901 / 345 789 123 | cut 3 관측. 공개 단언은 불일치. | [WPT](receipts/primary/webkitgtk-002-r1/summary.json) · [좌표](receipts/geometry/webkitgtk-002-r1/geometry.json) |
| 002 · WebKitGTK · 2 | 2.54.3 · Ahem 20px · W 400.000 CSS px | PASS, exit 0 · `!=` · Δ 4,800/480,000 px | 123 567 901 / 345 789 123 | cut 3 관측. 공개 단언은 불일치. | [WPT](receipts/primary/webkitgtk-002-r2/summary.json) · [좌표](receipts/geometry/webkitgtk-002-r2/geometry.json) |
| 003 · Chromium · 1 | 156.0.8078.79 · Ahem 15px · W 525.000 CSS px | PASS, exit 0 · `==` · Δ 0/480,000 px | plain·inline 각각 The quickest brown fox / jumped over the lazy dog | cut 4 관측. 기대 줄은 입력에 노출. | [WPT](receipts/primary/chromium-003-r1/summary.json) · [좌표](receipts/geometry/chromium-003-r1/geometry.json) |
| 003 · Chromium · 2 | 156.0.8078.79 · Ahem 15px · W 525.000 CSS px | PASS, exit 0 · `==` · Δ 0/480,000 px | plain·inline 각각 The quickest brown fox / jumped over the lazy dog | cut 4 관측. 기대 줄은 입력에 노출. | [WPT](receipts/primary/chromium-003-r2/summary.json) · [좌표](receipts/geometry/chromium-003-r2/geometry.json) |
| 003 · WebKitGTK · 1 | 2.54.3 · Ahem 15px · W 525.000 CSS px | PASS, exit 0 · `==` · Δ 0/480,000 px | plain·inline 각각 The quickest brown fox / jumped over the lazy dog | cut 4 관측. 기대 줄은 입력에 노출. | [WPT](receipts/primary/webkitgtk-003-r1/summary.json) · [좌표](receipts/geometry/webkitgtk-003-r1/geometry.json) |
| 003 · WebKitGTK · 2 | 2.54.3 · Ahem 15px · W 525.000 CSS px | PASS, exit 0 · `==` · Δ 0/480,000 px | plain·inline 각각 The quickest brown fox / jumped over the lazy dog | cut 4 관측. 기대 줄은 입력에 노출. | [WPT](receipts/primary/webkitgtk-003-r2/summary.json) · [좌표](receipts/geometry/webkitgtk-003-r2/geometry.json) |

표 1의 한 행은 원형 시험 1개×엔진 빌드 1개×신규 프로필 1개다. 계획 8, 원형 판정·PNG 및 별도 기하 각 8, 결측 0. 003 plain과 inline은 한 시험이다. 공개 run은 별도 층에서 미확인이다. 픽셀 분모는 같은 엔진의 800×600 입력·참조를 비교한 값이다.

| 변경 조건 | 실측 폭·줄수 | 가능한 규칙 | 규칙을 가르는 결과 | 적용 범위 |
|---|---|---|---|---|
| C1 auto → balance, 두 엔진 | W 159.984/160 CSS px. 3→3줄, advance [160,120,40]→[80,140,100] CSS px | 최대 접두사 또는 최소 분산 | 모두 cut 2;4→1;3, Δ 2,400 px | 줄수와 공백을 고정한 C1 |
| C1 word 2 뒤 br, Chromium forced auto → forced balance | W 159.984 CSS px. 3→3줄, [160,120,40] 유지 | 오른쪽 chunk 재균형 또는 유지 | cut 2;4 유지, Δ 0 px. unforced balance에 br을 넣으면 Δ 2,400 px | 강제 경계가 있는 Chromium C1 |
| C1 word 2 뒤 br, WebKitGTK forced auto → forced balance | W 160 CSS px. 3→3줄, [160,120,40]→[160,60,100] | 오른쪽 chunk 재균형 또는 유지 | cut 2;4→2;3, Δ 1,600 px. unforced balance에 br을 넣으면 Δ 2,400 px | 강제 경계가 있는 WebKitGTK C1 |
| W7 Chromium auto → balance | W 139.984 CSS px. 3→3줄, [120,120,40]→[80,60,140] | 최대 줄 길이 최소 또는 최소 분산 | cut 2;4→1;3, Δ 3,200 px. word 2 뒤 br 대조에서는 cut 2;4로 돌아감 | 같은 단어폭과 기본 7ch |
| W7 WebKitGTK auto → balance | W 140 CSS px. 3→3줄, [120,120,40] 유지 | 최대 줄 길이 최소, exact-fit 후보 탈락, 일반 auto와 동일 출력 | cut 2;4 유지, Δ 0 px. cut 1;3을 직접 강제하면 [80,60,140]의 3줄이 실제로 들어감 | W7 정확히 맞는 폭 |
| W7 WebKitGTK, W+1/64 또는 W+1 CSS px | W 140.015625 또는 141 CSS px. 모두 3→3줄 | 폭 경계에 따른 후보 허용 또는 순수 최대 줄 길이 최소 | 두 폭 모두 auto cut 2;4, balance cut 1;3, Δ 3,200 px. Chromium은 두 증가폭에서도 balance cut 1;3 | W7의 분수 폭과 1px 감도 |
| 002 별도 사본에 br을 word 2 또는 3 뒤에 둠 | W 399.984/400 CSS px. 각각 2줄, [140,300]과 [220,220] | 약한 불일치 조건 또는 cut 3을 요구하는 조건 | 두 엔진에서 같은 외부 참조에 대해 각각 7,200/4,800 px 차이 | 원형과 분리한 불일치 대조 |
| Chromium 002 Ahem 404 | W 200 CSS px. 2줄, [100,100] | 폰트 성공 확인 또는 픽셀 관계만 확인 | cut 3과 불일치 관계 유지, Δ 1,089 px. face `error` | 별도 포트의 fallback |
| Chromium 003 Ahem 404 | W 262.5 CSS px. 초록 각 2줄 | 동일 픽셀에서 Ahem을 추정 또는 로드 검증 | cut 4, 참조 대비 Δ 0 px. face `error` | 별도 포트의 fallback |
| WebKitGTK 002 Ahem 404 | W 260 CSS px. 시험·참조 각 1줄 | 현 폰트 및 폭으로 다시 계산 | 관계 반전, 참조 대비 Δ 0 px. face `error` | 별도 포트의 fallback |
| WebKitGTK 003 Ahem 404 | W 350 CSS px. 초록 각 1줄, 파란 블록 및 참조 각 2줄 | 현 폰트의 soft wrap과 명시된 br | 관계 반전, 참조 대비 Δ 8,629 px. face `error` | 별도 포트의 fallback |
| Sintel cue 3의 DOM 폭 42ch → 20ch | 504→240 CSS px. 2→4줄 | cue 원텍스트 내부 개행·추가 soft wrap·cue 시간 | 두 엔진의 native cue 3은 29.000–32.450초와 raw 2행을 유지 | 문장·시간 분리 통제, overlay 범위 밖 |
| Sintel cue 4의 DOM 폭 42ch → 20ch | 504→240 CSS px. 1→3줄 | cue 원텍스트 내부 개행·추가 soft wrap·cue 시간 | native cue 4는 32.750–35.800초와 raw 1행을 유지. cue 간 간격 0.300초 | 문장·시간 분리 통제, overlay 범위 밖 |

표 2의 한 행은 조건 변화에 대한 대조 하나다. 공통 출력은 두 엔진을 같은 행에 적었다. 13개 보고 행은 합성 기본 렌더 16건, 폭 보조 렌더 10건, 002의 명시적 cut·공통 참조 렌더 6건, 폰트 실패의 입력·참조 4쌍 및 native track 2로드의 일부를 조회한다. 모수가 겹치는 대조끼리 실행 수를 합산할 수 없다. 표의 advance는 폰트 잉크의 바깥 모서리가 아닌 Range의 CSS px 재구성이다. [합성·폰트·cue 영수증](receipts/diagnostics/), [반례와 개별 판정](COUNTEREXAMPLES.md).

## Q1. 표본과 실제 트리

WPT `5ad65d6ea6c649696be2d0cf5188dfdb43f8d801`의 `css/css-text` subtree `08b1300e11f6d4eb22f252b13e1ceaaf0e978e51`은 3,183경로다. 232가 지정한 `white-space/text-wrap-balance-002.html`과 `003.html`의 blob은 `cae9d54d…`, `a2eb8bbf…`이고 각각 L3의 `mismatch`, L4의 `match`가 `reference/` 아래 파일을 지정한다. 별도 참조 blob `d8c1834d…`, `318480bb…` 및 네 SHA-256을 모두 일치 확인했다. 002 참조에는 balance나 강제 개행이 없고, 003 참조 L17–19는 두 초록과 한 파란 블록 모두 fourth word `fox` 뒤에 `br`를 둔다. [manifest.json](manifest.json), [W01/002 입력](https://github.com/web-platform-tests/wpt/blob/5ad65d6ea6c649696be2d0cf5188dfdb43f8d801/css/css-text/white-space/text-wrap-balance-002.html), [W02R/003 참조](https://github.com/web-platform-tests/wpt/blob/5ad65d6ea6c649696be2d0cf5188dfdb43f8d801/css/css-text/white-space/reference/text-wrap-balance-003-ref.html#L17-L19).

경로 순서를 `LC_ALL=C`로 고정하고 선언 및 규격 anchor 검색의 39후보를 남겼다. 003 이전 2,638경로를 넓은 문자열 조건으로 검사하고 002 이전 2,637경로에서 HTML 등 1,797개의 `link rel`을 구조적으로 검사했다. 1,182개가 reftest 링크를 선언했고, 482개에 문서나 선언된 로컬 자원에서 Ahem 표지가 있었다. 이 1,182개에서 balance와 text-wrap 표지가 함께 나온 수는 관측한 0이다. 001의 harness는 높이만 비교하고, 앞선 파싱·상속 및 crash 파일과 `reference/` 전용 파일도 렌더링 입력 적격 조건에서 제외했다. 이 고정 탐색에서 앞선 적격 파일을 찾지 못했다. 동적으로 생성되는 속성이나 선언에 보이지 않는 로딩은 미확인이다. [후보 원행](receipts/css-text-candidates.csv), [구조 검사](receipts/css-text-structural-scan.json), [W03/001 높이 단언](https://github.com/web-platform-tests/wpt/blob/5ad65d6ea6c649696be2d0cf5188dfdb43f8d801/css/css-text/white-space/text-wrap-balance-001.html#L23-L30).

## Q2. 실제 바이너리와 폰트

Debian 13.6 amd64, Linux 6.18.57에 Chromium `156.0.8078.79-1~deb13u1`, ChromeDriver `156.0.8078.79`와 WebKitGTK MiniBrowser `2.54.3`, WebKitWebDriver 패키지 `2.54.3-1~deb13u1`을 사용했다. ChromeDriver CLI가 내놓은 SHA는 upstream `a21ce95c…`와 맞는다. WebKit 드라이버는 `--version` 값 대신 `.deb` 버전·실행 파일 SHA와 `New Session`의 `browserVersion=2.54.3`으로 식별했다. Chromium은 headless, GTK는 Xvfb·GTK3다. 추출된 WebKit 보조 프로세스와 번들의 경로만 연결했고 엔진 바이너리 지문은 원 패키지와 같다. 232의 정적 소스는 Blink `92e20e6b…`, WebKit `fcbbc8e8…`였다. 이번 실행판의 대응 upstream은 Blink `a21ce95c…`, WebKit `eb74cd57…`로 소스 파일 지문이 다르다. Debian 옵션까지 동일한 소스 빌드일지는 미확인이다. [env.json](env.json), [B04 Chromium pool](https://deb.debian.org/debian/pool/main/c/chromium/), [B07 WebKitGTK 출시판](https://webkitgtk.org/2026/11/18/webkitgtk2.54.3-released.html).

원형 입력 PNG 8개가 800×600 px이고 별도 기하 8로드의 viewport 800×600 CSS px, devicePixelRatio 1, 문서 clientWidth 800 CSS px가 일치했다. Ahem Regular 1.5의 Git blob은 `4d4785a4…`, SHA-256은 `b719ecb31c5b21fc573c03f6421c74ac63c271a5a3ff841e34f9705fb94b8448`이다. 별도 로드는 입력과 참조 모두 HTTP 200으로 21,768-byte TTF를 받았고 `FontFace`가 `loaded`였다. Chromium input에서 `loadingdone` 4/4를 수신했다. WebKitGTK input에서는 `ResourceTiming.responseEnd`와 decoded bytes, 서버 응답, face 상태, advance까지 관측했다. 페이지 로드 후 listener 및 별도 빠른 listener의 WebKit DOM `loadingdone` 콜백은 수신하지 못했다. 이 콜백 관측의 공석과 실제 font fetch·사용을 각각 기록했다. [실행 원행](runs.csv), [WebKit 폰트 이벤트 시도](receipts/diagnostics/webkitgtk-font-audit/font-audit.json), [W06 Ahem 원자료](https://www.w3.org/Style/CSS/Test/Fonts/Ahem/).

공개 결과는 별도 층이다. 공식 API의 10자 요청과 full SHA 요청, results 경로 및 raw archive prefix를 열었으나 제한 응답에서 exact-SHA run의 id·판·결과를 확보하지 못했다. 확인 가능한 공개 제출은 0개, 제출 존재 여부와 분모는 미확인이다. 232의 공개 미확인도 그대로 남는다. [W08 API 계약](https://github.com/web-platform-tests/wpt.fyi/blob/384838e8970255eab44042167f45ae8dadb36a02/api/README.md#api-runs), [API 영수증](receipts/public-wpt-probe.txt), [아카이브 조회](receipts/setup/public-wpt-bucket.txt).

## Q3. 원형 WPT의 판정

입력 하나씩 새 runner와 새 프로필을 열어 `chrome`과 `webkitgtk_minibrowser` 제품에서 각 시험을 두 번 실행했다. 8/8 모두 runner `test_end=PASS`, `wptreport=PASS`, exit 0이다. 002는 4/4에서 참조 대비 정확히 4,800픽셀 차이였고 003은 4/4에서 0픽셀이었다. timeout 및 FAIL은 이 기본 표본에서 관측한 0이다. localhost 포트·TLS·라이브러리 기동의 사전 실패에는 `test_end`가 없다. 그 시도는 `receipts/setup/`에 별도로 남겼다. 원 runner가 비교한 PNG와 디코딩 후 diff, SHA-256, 명령과 stdout/stderr는 슬롯별 폴더에 있다. [WPT 원영수증](receipts/primary/), [W05 WPT reftests 규약](https://web-platform-tests.org/writing-tests/reftests.html), [W07 runner 관계 판정](https://github.com/web-platform-tests/wpt/blob/5ad65d6ea6c649696be2d0cf5188dfdb43f8d801/tools/wptrunner/wptrunner/executors/base.py#L532-L598).

002의 `mismatch` 작성자가 지정한 관계는 픽셀 불일치다. 실제 cut 3은 Q4에서 측정할 때만 확인된다. cut 2의 별도 사본 또한 불일치한다. 003은 `match`의 전체 viewport 비교이며 참조와 입력 속 파란 블록은 둘 다 cut 4다. 공개 기대가 주는 단언, 이번 엔진의 구조, 정적 후보를 같은 셀로 환산하면 002에서 정보가 늘어난 것처럼 보이므로 표에서 따로 기록했다. [W01R/002 참조](https://github.com/web-platform-tests/wpt/blob/5ad65d6ea6c649696be2d0cf5188dfdb43f8d801/css/css-text/white-space/reference/text-wrap-balance-002-ref.html), [명시 cut 대조](receipts/diagnostics/chromium-controls/controls.json).

## Q4. 별도 로드에서 실제 글자 위치

고정 바이트의 각 페이지를 별도 WebDriver 프로필과 서버에서 열고 `fonts.ready` 뒤 텍스트 노드에 Range를 만들었다. 기존 DOM에서 word index와 각 fragment의 x/y/width/height를 읽고, 같은 block의 y 차가 0.5 CSS px 이내이면 같은 줄로 묶었다. 002는 두 엔진에서 y 8/28, 줄 advance `[220,220]` CSS px, cut 3이었다. 별도 auto 참조는 cut 5, `[380,60]` CSS px였다. 003은 모든 시험 블록에서 cut 4다. Chromium plain 줄 y 50/65와 WebKitGTK 51/66, inline 줄 y 95/110과 96/111을 실제로 기록했다. WebKitGTK plain·inline advance는 각각 `[330,360]`, Chromium은 plain `[330.015625,360.015625]`와 inline `[330.0625,360.0625]` CSS px다. Chromium의 소수점 직사각형 차이에도 003은 원형에서 0픽셀 관계를 유지했다. [S03 Range의 사각형 정의](https://www.w3.org/TR/2025/WD-cssom-view-1-20250916/#dom-range-getclientrects), [단어 원행](words.csv), [계측 코드](measure.js).

같은 엔진·시험의 r1과 r2는 원형 PNG의 양쪽 SHA 및 기하의 단어 fragment 전체가 일치했다. 측정한 범위는 주 시험 fragment 96/96, 내장 파란 비교 36/36, 외부 참조 132/132이다. 한 줄이 여러 단어를 같은 y에 놓는 것을 관측한 값이며, CSSOM의 font ascent/descent는 캡처 내 잉크 모양의 경계와 구별된다. 232의 정적 cut과 일치한 4개 시험×엔진 조건은 이미 공개 기대를 읽은 후에 관측했다. 가림 적중률의 분모는 공석 0이다. [선행 계산 S05](https://github.com/laadkke-arch/agentflow-open/blob/430a1a5ec049f58878d963cb8ca539c9375f93d0/docs/workstreams/research/AF-RES-232/predictions.csv), [별도 로드 원영수증](receipts/geometry/).

## Q5. 합성 통제가 가른 목적과 폭

두 합성 입력에서 glyph와 공백의 advance는 20 CSS px 수준이고 줄 수는 모두 실제 3이다. C1의 최대 접두사 `[8,6,2]` ch와 최소 분산 `[4,7,5]` ch는 고정 줄 수에서 잔여폭 분산 `56/9` 대 `14/9` ch²다. 등폭·고정 k에서 폭 분산과 잔여폭 분산의 순위는 같다. 원 C1 balance는 두 엔진에서 두 번째 후보였다. 단어 2 뒤에 `br`를 두면 오른쪽 chunk의 `[3,5]` ch가 `[6,2]` ch보다 분산이 작다. WebKitGTK가 `[3,5]`로 바뀌었고, Chromium은 `[6,2]`를 그려 강제 뒤 세부 예측이 빗나갔다. [S01 CSS Text 4 §5.4](https://www.w3.org/TR/2026/WD-css-text-4-20260814/#text-wrap-style), [C1 원표 S05B](https://github.com/laadkke-arch/agentflow-open/blob/430a1a5ec049f58878d963cb8ca539c9375f93d0/docs/workstreams/research/AF-RES-232/breaks.csv).

W7은 최장 줄 길이를 최소화할 때 `[6,6,2]` ch, 잔여폭 분산으로 `[4,3,7]` ch를 고른다. 정확히 맞는 7ch에서 Chromium은 후자, WebKitGTK는 전자를 그렸다. WebKitGTK에서 문서 폭만 1/64 CSS px 늘리면 auto는 같고 balance는 후자로 바뀐다. 같은 폭에서 직접 강제한 `[4,3,7]` ch도 들어가므로 폭 경계가 중요하다. B06/B13의 후보폭 `ceil(width + epsilon)`과 고정 줄 수의 폭 컷은 관측과 일치하는 원인 후보로 남긴다. B03의 Blink score 우선과 bisection fallback, B06의 WebKit cubic 및 forced chunk는 단순 목적함수 표의 선택과 일대일로 대응하지 않는다. 분기 추적은 미실시다. [B03 Blink 분기](https://github.com/chromium/chromium/blob/a21ce95c24ce3964416f09ae1862f53f319eb4d0/third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc#L140-L185), [B06 WebKit exact-fit 컷](https://github.com/WebKit/WebKit/blob/eb74cd57254e5b9738fbaa5ad13df320a68a7119/Source/WebCore/layout/formattingContexts/inline/InlineContentConstrainer.cpp#L394-L432), [실측 통제](receipts/diagnostics/webkitgtk-controls/controls.json).

## Q6. 자막에서 움직이는 경계

DCMP의 조동사 분리 예제에서 공백 포함 16/24 문자로 나눈 안보다 조동사와 본동사를 붙인 26/14 문자를 택한다. Netflix UK 지침도 최대 두 줄과 문법 결합을 두며 여러 유효 대안의 시각적 모양에 별도 선호가 있다. 어느 쪽도 이 자료에서 독자 선호를 측정하지 않았다. [V02 DCMP Line Division](https://dcmp.org/learn/597-captioning-key---text), [V04 Netflix I.10](https://partnerhelp.netflixstudios.com/hc/en-us/articles/30806198616339-English-UK-Timed-Text-Style-Guide).

고정된 MDN Sintel English 원본 L17–24에서 cue 3은 `You're a fool for traveling alone,` / `so completely unprepared.`의 두 원행과 29.000–32.450초를 가진다. Cue 4는 `You're lucky your blood's still flowing.` 한 원행과 32.750–35.800초다. 두 실제 WebDriver의 native `<track>`은 readyState 2, 전체 14 cue, 대상 두 cue의 id·text·초값이 원문 파싱과 일치했다. 일반 DOM에 payload를 넣고 폭을 504→240 CSS px로 바꾸자 cue 3은 2→4줄, cue 4는 1→3줄이 됐다. 내부 개행과 두 cue 사이 0.300초는 보존됐다. WebVTT §4.1의 cue block 정합을 확인했고 영상 overlay·음성 정렬·읽기 실험은 범위 밖이다. [V01 WebVTT 구문](https://www.w3.org/TR/2026/CRD-webvtt1-20260520/#file-structure), [V03 게시 VTT L17–24](https://github.com/mdn/shared-assets/blob/f160bcf2db52b60820a7728aa9b3fa88568cfc38/misc/sintel-en.vtt#L17-L24), [Chromium cue](receipts/diagnostics/chromium-captions/captions.json), [WebKitGTK cue](receipts/diagnostics/webkitgtk-captions/captions.json).

## Q7. 공개 기대·정적 후보·재생이 갈리는 곳

사양 편집자 관점에서는 auto 대비 줄수 유지와 폭 분산 개선, 강제 개행 그룹이 기준이다. WPT 작성자 관점에서는 002의 부정 관계와 003의 강제 참조 픽셀이 기준이다. 003은 각 엔진의 외부 참조와 동일한 반면 엔진끼리의 입력 PNG는 5,805픽셀이 달랐다. 002의 엔진 간 PNG 바이트 SHA는 달랐고 decoded RGBA는 같았다. Chromium 폰트를 의도적으로 빼도 003의 0픽셀과 cut 4가 남았다. 제목을 렌더링하는 개발자가 정확한 단어 위치 또는 폰트 정체성을 필요로 한다면, 브라우저와 폰트 핀에서 runner·기하·font trace 세 증거를 연결해야 한다. 자막 편집자가 확인하는 cue 경계와 언어 묶음은 Q6의 별도 값이다. [S02 CSSWG 결의](https://github.com/w3c/csswg-drafts/issues/10186), [엔진 간 픽셀](receipts/cross-engine.json), [반례 원행](COUNTEREXAMPLES.md).

③ `9992dc123f457f97fc462518d18540d23f6dd6fa`의 코드로 별도 checkout과 프로필에서 Chromium 003을 재생했다. exit 0, PASS, Δ 0, 양쪽 PNG SHA `201c02160bbbc76bfc6c85076a997507a4c33166696f509a965889fcf085dd76`, 각 block과 Ahem 요청 SHA가 r1과 일치했다. 같은 checkout의 C1 재생은 2,400픽셀 auto/balance 차이와 forced auto/balance 0픽셀을 다시 냈다. 원형 8회와 구분한 재생이며 다른 기기에서의 독립 검토는 미실시다. [재생 비교 원행](receipts/replay/comparison.json), [재생 명령](replay.md).

## 비용·대안·추가 분석

공개 호환성의 좁은 판단은 원형 runner와 font receipt로 가능하다. 정확한 텍스트 편집·회귀 판독에는 프로필별 DOM Range와 viewport를 추가해야 하며, 그것으로 실제 캡처의 안티앨리어싱이나 안정성 비용을 대체할 수는 없다. 이번 두 엔진의 고정판을 맞추면서 포트·인증서와 GTK 추출 바이너리 경로를 별도로 해결했다. 준비와 브라우저 기동 시간이 섞여 있어 이 로그의 시간은 레이아웃 성능 비교에 부적합하다.

실제 개발에서 한 제목의 줄을 고정하려면 저작자가 의미 단위와 폭 반응을 다시 대조할 수 있다. 짧은 제목의 자동 balance는 폭이 달라질 때 새로 적응하며, 명시 br은 경계를 강제하는 대신 나머지 그룹 선택에도 영향을 준다. Ahem의 동일 advance는 정확한 차이를 재현하기 쉽다. 비례 글꼴의 실제 제목이나 shaping이 필요한 언어에 대한 해석은 별도 입력이 필요하다. 상대 reftest, 기하 검산, 사람의 평가를 각각 얻는 비용이 다르다. [B05 제목 작성자 설명](https://developer.chrome.com/docs/css-ui/css-text-wrap-balance), [B08 Safari 작성 예](https://webkit.org/blog/15383/webkit-features-in-safari-17-5/).

| 중요한 불일치 또는 약점 | 영향을 받는 판단 | 다음에 볼 구체적 원자료·검사 | 판정이 바뀌는 관측 |
|---|---|---|---|
| W7 WebKitGTK exact-fit과 1/64 CSS px에서 줄 분할 반전, Blink의 forced C1은 별도 움직임 | 균형 비용이나 내부 분기를 최종 줄만으로 귀속 | B06 L105–107·L416, B13 L190의 후보폭과 chosen breakpoints를 140 및 140.015625 CSS px에서 기록하는 동일판 추적 | 정밀 후보폭이 한계 값을 넘는지 및 예측한 branch에서 선택했는지 확인되면 경계 원인 판단 강화 |
| Ahem 404인데 Chromium 003도 0픽셀·cut 4 | PASS 또는 동일 y에서 정상 폰트 추정 | Chromium 003의 원 font payload·face 상태와 별도 404 포트의 영수증 비교. 추가 실폰트로 같은 대조 | face 및 advance 확인과 함께 현재 의도한 픽셀 관계가 재현되면 정상 폰트 주장 강화 |
| 고정 SHA의 공개 run은 접근 실패. 이번 표본은 포트별 고정판 한 개 | 과거 공개 배포판 또는 Safari에 대한 재현성 | W08 `/api/runs?sha=5ad65d6ea6`에서 full revision, run ID·브라우저·OS를 확인한 뒤 raw report 두 경로 비교 | 같은 revision에서 관계가 갈리는 확인된 보고서가 있으면 빌드별 차이로 범위를 좁힘 |
