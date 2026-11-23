# 좌표·SVG·화면·호스트 DOM 대조

## 그래프 원소

원 PDF의 상태 중심을 원점으로 옮겨 PDF 좌표를 대조했다. 각 전이의 선 시작·끝, 촉 위치·색, 라벨 문자열과 경계상자를 기록했다. HTML에서는 PDF와 동일 원소 주변의 화면 픽셀, 실제 SVG XML과 img의 decoded data payload를 대조했다. 기준과 실행 PDF의 대응 허용은 0.02pt다. 화면의 픽셀 비교는 두 방향으로 2픽셀 오차를 허용한다. [사전 PDF 좌표](REFERENCE_SEAL.json) · [30자리 원소별 판독](verification.json)

| 요소 | 원 그래프와 화면의 판별 단서 | 다른 입력의 변화 |
| --- | --- | --- |
| q₁–q₄ | 왼쪽부터 네 원, 아래첨자 1–4. 첫 원과 마지막 원에 이중원 | T1은 q₁ 외곽 RGB(0,94,179), 네 원 옅은 청색. T0/T3/T4는 회색 |
| 초기 | q₁ 왼쪽의 짧은 화살촉. 텍스트 공백 | 원 tikzset을 빼면 T1의 기본 start 글자가 나타남 |
| E1 | q₁↻ q₁, 위쪽 a | 같음 |
| E2 | q₁→q₂, 중앙 높이의 수평 오른쪽 촉, 위 b | T3 g1 청·g2 적, T4 g1 적·g2 청. 두 g2의 촉은 q₁ 방향이고 라벨 r |
| E3 | q₂→q₃, 중앙 수평 오른쪽 촉 및 a | 같음 |
| E4 | q₂→q₄, 아래 교차선의 q₄ 쪽 촉 및 오른쪽 아래 b | 같음 |
| E5 | q₃→q₂, 중앙 위쪽 호의 왼쪽 촉 및 a | 같음 |
| E6 | q₃→q₁, 아래 교차선의 q₁ 쪽 촉 및 왼쪽 아래 b | 같음 |
| E7 | q₄↻ q₄, 위쪽 b | 같음 |
| E8 | q₄→q₃, 오른쪽 끝 수평선의 왼쪽 촉 및 a | 같음 |

| 대표 출력 | 화면의 그림·문자 | 호스트에서 선택·검색 | 대체 텍스트 | 새 폴더 HTML 단독 |
| --- | --- | --- | --- | --- |
| [T0 K](matrix/T0-K-1/browser.png) · [SVG XML](matrix/T0-K-1/svg.json) | 402×112, 4/4·8/8, PDF 좌표와 그림 내부 요소 일치 | [문장 2/2, 앞→img→뒤](matrix/T0-K-1/browser.json) | alt 없음 | [디코드 성공, 추가 요청 0](matrix/T0-K-1/moved.json) |
| [T1 M](matrix/T1-M-1/browser-img01.png) · [SVG XML](matrix/T1-M-1/svg.json) | 406×112, q₁ 청색과 네 원 옅은 청색, 4/4·8/8 | [2/2](matrix/T1-M-1/browser.json) | alt 없음 | [디코드 성공, 추가 요청 0](matrix/T1-M-1/moved.json) |
| [T3 M](matrix/T3-M-1/browser.png) · [T4 M](matrix/T4-M-1/browser.png) | 각각 두 그림. 4/4·8/8 각, E2 반대색·화살촉·라벨 보존. [T3 g2](matrix/T3-M-1/browser-img02.png) · [T4 g2](matrix/T4-M-1/browser-img02.png) | [각 3/3, 그림 사이에 둘째 문장](matrix/T4-M-1/browser.json) | 두 img 모두 alt 없음 | [각 두 이미지 유지](matrix/T4-M-1/moved.json) |
| [T1 P](matrix/T1-P-1/browser-img01.png) · [SVG XML](matrix/T1-P-1/svg.json) | 595×842. 그림, 색과 문장 2개의 외형이 같은 페이지에 있음 | [0/2](matrix/T1-P-1/browser.json) | Page 1 | [1 img, 추가 요청 0](matrix/T1-P-1/moved.json) |
| [T2 P 첫 쪽](matrix/T2-P-1/browser-img01.png) · [마지막 쪽](matrix/T2-P-1/browser-img14.png) · [SVG XML](matrix/T2-P-1/svg.json) | 페이지마다 612×792. 14쪽의 순서 및 청색 촉이 있는 27 투영. 원 제목과 축 틱이 보임 | [산문 항목 해당 없음. 프로브한 제목 0/8](matrix/T2-P-1/browser.json) | Page n | [14 img, 추가 요청 0](matrix/T2-P-1/moved.json) |

T2는 빈 산문을 채우지 않았다. pgfplots 축·틱은 문자 모양이 화면에 있다. 기준 PDF에서 두 장 제목과 27개 하위 제목이 읽히며, 그림마다 청색 선의 시작·중간 꼭짓점·마지막 촉 좌표를 쌍으로 기록했다. g01은 (0,50), g12는 (-30,0), g27은 (90,90)이다. 27개 투영 및 촉의 화면과 좌표 대응을 2회 검산했다. [소스 값](inputs/T2.tex#L21-L69) · [원 그림 전체 목록](REFERENCE_SEAL.json) · [Chrome 원본 이미지 14개](matrix/T2-P-1/)

T2의 숫자 주변 픽셀 257개 상자 중 256개가 두 반복의 양방향 임계값을 넘었다. g23의 숫자 1은 한 방향에서 0.5789였다. 인접 선과 글자를 확대해 양쪽 원 화면에서 1을 읽었다. [기준 확대](T2-g23-tick-reference.png) · [Chromium 확대](T2-g23-tick-browser.png)

MuPDF SVG는 glyph를 path/use 구조 및 data-text 속성으로 보존한다. 이 값은 호스트 HTML에서 s1/s2를 선택한 결과와 개별 지표다. 스크린 리더의 실제 읽기 경험은 미확인이다. [MuPDF SVG 장치 소스](https://github.com/ArtifexSoftware/mupdf/blob/5d61c9df9c5d72520335898ce53046aa53a4e8a7/source/fitz/svg-device.c#L535-L577) · [HTML img](https://html.spec.whatwg.org/multipage/embedded-content.html#the-img-element)

## 원 정의 제거와 범위 대조

| 대조 | 예상에 반하는 관측 | 원 관측 |
| --- | --- | --- |
| T1 M에서 L4 제거 | 같은 그림 조각과 설정을 넘겼으나 xcolor 미정의, g1 pdflatex 1 | [선택](controls/T1-M-no-color/selected-lines.json) · [로그](controls/T1-M-no-color/g1-pdflatex.stdout) |
| T1 M에서 L6 제거 | 0으로 종료하고 q₁ 테두리는 청색. 모든 원의 채움 및 원 전이 촉이 사라지고 초기 start 글자가 생김 | [화면](controls/T1-M-no-tikzset/browser-img01.png) · [PDF 판독](controls/T1-M-no-tikzset/g1.observed.json) |
| T3 M 둘째 L28 제거 또는 L8/L28 교환 | 첫 그림 맞음. 둘째 좌향 r은 살아 있고 청색으로 잘못 물려받음. 출력 생성·DOM 성공 | [제거 화면](controls/T3-M-no-new-style/browser-img02.png) · [역순 화면](controls/T3-M-reverse-styles/browser-img02.png) |
| T3 M 둘째 L5 제거 | g1 SVG가 실제로 생김. g2 pdflatex 1로 HTML 쓰기 전에 실패 | [첫 그림 부분 미리보기](controls/T3-M-no-red/partial.png) · [실행](controls/T3-M-no-red/receipt.json) |
| T4 M 첫째 L12 제거 또는 역순 | 원 첫째 적색 촉이 청색으로 바뀜. 다음 그림은 바깥 청색 유지 | [삭제](controls/T4-M-no-inner/browser.png) · [역순](controls/T4-M-reverse-styles/browser.png) |
| T4 M의 닫힌 그룹을 g2에 전달 | 첫째 적색 맞음. 둘째도 적색으로 남고 최종 HTML이 열림 | [두 그림](controls/T4-M-leak-inner/browser.png) · [전달 행](controls/T4-M-leak-inner/selected-lines.json) |
| T3 M 무관 선언 추가 | g1과 g2 SVG가 주 실행과 각각 바이트 동일. 이 선언은 양쪽에 전달됨 | [추가 행과 SVG 영수증](controls/T3-M-unused/receipt.json) |
| T3 M 같은 b | 그림 2개, E2 둘 다 b. g1 오른쪽 청색과 g2 왼쪽 적색은 남음 | [화면](controls/T3-M-same-label/browser.png) · [g2 PDF 좌표](controls/T3-M-same-label/g2.observed.json) |
| T0 그림 블록 제거 K/M/P | K/M 이미지 0이고 문장 2/2. P는 그림 없이도 지면 이미지 1, 호스트 문장 0/2 | [K](controls/T0-K-no-figure/browser.json) · [M](controls/T0-M-no-figure/browser.json) · [P](controls/T0-P-no-figure/browser.png) |
| T0 P 상대 경로 | SVG 동반 시 그림 1. HTML만 옮기면 out1.svg 404 및 자연 크기 0×0 | [동반](controls/T0-P-external/browser.json) · [이동](controls/T0-P-external/moved.json) |

사용한 문맥 하나를 지웠을 때만 관측이 바뀐 결론은 해당 입력과 목록 순서에 한정한다. 색과 스타일을 그림 안에 다시 쓰거나 그림을 매개변수 없이 펼치는 방법까지 같은 분모에서 검증한 것은 아니다. [14개 보조 실험의 원장](../runs.jsonl) · [수치 검산](verification.json)
