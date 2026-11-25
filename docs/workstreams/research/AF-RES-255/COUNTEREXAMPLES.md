# AF-RES-255 반례와 정정

## 002의 이미지 차이는 cut 3보다 약하다

같은 Ahem과 20ch에서 단어 2 또는 3 뒤에 `br`를 둔 두 별도 입력을 만들었다. 두 엔진에서 cut 2는 폭 `[140,300]` CSS px, cut 3은 `[220,220]` CSS px였다. 원 auto 참조는 cut 5, `[380,60]` CSS px였다. 800×600 픽셀 비교에서 cut 2는 7,200픽셀, cut 3은 4,800픽셀이 달랐다. 두 서로 다른 출력이 `mismatch` 관계를 충족했다. 원형 8회에 이 변형을 추가하지 않았다. [Chromium 통제](receipts/diagnostics/chromium-controls/controls.json), [WebKitGTK 통제](receipts/diagnostics/webkitgtk-controls/controls.json), [002 입력의 선언](https://github.com/web-platform-tests/wpt/blob/5ad65d6ea6c649696be2d0cf5188dfdb43f8d801/css/css-text/white-space/text-wrap-balance-002.html#L3).

## W7의 1/64 CSS px 경계

W7에 공백 20px, 단어 advance `[80,20,20,80,40]` CSS px, 3줄을 고정하면 `[120,120,40]`은 최대 줄 길이가 더 짧고 `[80,60,140]`은 잔여폭 분산이 더 작다. 이상 단위 `ch²`의 분산은 각각 32/9와 26/9다. Chromium은 7ch에서 `[80,60,140]`을 관측했고 WebKitGTK는 `[120,120,40]`을 관측했다. 후자의 출력은 최대 줄 길이 최소와 외형이 같아서 출력 하나만으로 내부 목적함수를 귀속할 수 있었다는 가설을 점검했다.

WebKitGTK에서 `br` 두 개로 cut 1;3을 직접 두면 W 140 CSS px에 `[80,60,140]`을 그렸다. 강제 개행 없이 폭을 140.015625 또는 141 CSS px로 높이면 auto는 계속 `[120,120,40]`이고 balance는 `[80,60,140]`으로 바뀌었다. 두 폭에서 auto 대비 3,200픽셀 차이였다. 각 조건의 실제 줄 수는 3이다. 140px 결과가 보이는 최대 줄 길이 최소의 취급은 이 미세 폭 변화에서 유지되지 않는다.

WebKitGTK 출시판 `computeLineWidthFromSlidingWidth`는 candidate에 `LayoutUnit::epsilon()`을 더해 ceil하고, fixed-count 탐색에서 해당 폭을 최대폭과 비교해 자른다. `epsilon=1/64`이고 관측 전환점과 맞는다. 이는 소스와 입출력으로 지지된 경계 가설이다. 실행 중 분기, `SlidingWidth`의 각 중간값, 분기 원인의 독립 추적은 미확인이다. [B06 L105–107, L400–431](https://github.com/WebKit/WebKit/blob/eb74cd57254e5b9738fbaa5ad13df320a68a7119/Source/WebCore/layout/formattingContexts/inline/InlineContentConstrainer.cpp#L400-L431), [B13 L190](https://github.com/WebKit/WebKit/blob/eb74cd57254e5b9738fbaa5ad13df320a68a7119/Source/WebCore/platform/LayoutUnit.h#L190).

## 강제 개행으로 C1의 원후보가 달라진다

강제 개행 없이는 두 엔진 모두 C1에서 auto `[160,120,40]`과 balance `[80,140,100]`을 관측했다. 두 번째 단어 뒤에 `br`를 두면 balance의 첫 줄이 160 CSS px로 고정된다. Chromium은 `[160,120,40]`이어서 강제 auto와 0픽셀 차이였고, WebKitGTK는 `[160,60,100]`이어서 강제 auto와 1,600픽셀 차이였다. 두 엔진 모두 3줄이다. Chromium에 대해 동결했던 오른쪽 chunk의 최소 분산 조건 `2;3`은 빗나갔고 WebKitGTK에서는 맞았다. 강제 개행에 대한 Blink bisection의 제약과 WebKit의 chunk 처리는 두 출력이 갈릴 수 있는 코드 근거다. 실행 중 어느 Blink 경로가 사용됐는지는 미확인이다. [Blink B01 L67–77](https://github.com/chromium/chromium/blob/a21ce95c24ce3964416f09ae1862f53f319eb4d0/third_party/blink/renderer/core/layout/inline/paragraph_line_breaker.cc#L67-L77), [WebKit B06 L316–344](https://github.com/WebKit/WebKit/blob/eb74cd57254e5b9738fbaa5ad13df320a68a7119/Source/WebCore/layout/formattingContexts/inline/InlineContentConstrainer.cpp#L316-L344).

## 같은 페이지 관계가 폰트 실패를 감추는 경우

같은 두 WPT 입력과 참조를 별도의 포트에 두고 Ahem TTF만 404로 응답했다. Chromium 002는 폭 200 CSS px에서 두 줄·cut 3, 참조와 1,089픽셀 차이였다. Chromium 003은 폭 262.5 CSS px에서 두 줄·cut 4이며 참조와 0픽셀이었다. 둘 다 정상 폰트 조건과 같은 이미지 관계를 보였다. WebKitGTK 002는 W 260 CSS px의 한 줄이어서 참조와 0픽셀, 003 시험 블록들은 W 350 CSS px의 한 줄이어서 blue/외부 참조의 강제 두 줄과 갈려 8,629픽셀 차이였다. 네 조건 모두 `FontFace.status=error`였다. 003의 0픽셀과 같은 cut이 자산 정체성을 보장한다는 주장은 Chromium 대조에서 뒤집혔다. [네 폰트 실패 영수증](receipts/diagnostics/), [CSS Font Loading §3](https://www.w3.org/TR/2023/WD-css-font-loading-3-20230406/#font-face-set-ready).

## 003의 일치와 cue 경계

각 엔진의 003 초록 두 블록은 강제 br을 사용하는 외부 참조와 일치했다. 해당 두 엔진의 입력 PNG를 서로 비교하면 5,805픽셀이 달랐다. 원형의 `match`는 엔진별 상대 비교다. 002는 브라우저 간 PNG 바이트 SHA가 달라도 디코딩한 입력 RGBA 픽셀은 0개 차이였다. [엔진 간 비교](receipts/cross-engine.json).

고정 Sintel WebVTT의 cue 3·4에는 각각 2·1 raw line이 있다. 두 엔진에서 이 payload를 504→240 CSS px로 바꾸자 표시 줄은 각각 2→4, 1→3이 됐다. native track의 두 cue 시간과 사이 0.300초는 그대로다. DCMP의 조동사 보존 예시는 문자폭 균형을 양보하는 별도 편집 기준을 제공한다. 시각 밀도, 음성 시간과 언어 단위의 출력이 각각 움직일 수 있다. [고정 cue 바이트](https://github.com/mdn/shared-assets/blob/f160bcf2db52b60820a7728aa9b3fa88568cfc38/misc/sintel-en.vtt#L17-L24), [DCMP Line Division](https://dcmp.org/learn/597-captioning-key---text).
