# Graphviz와 Jupyter에서 같은 경계 확인

| 경우 | 실제 입력과 출력 | 관측 |
| --- | --- | --- |
| Graphviz 공식 SVG 예 | `digraph { a->b }`를 Debian dot 2.42.4에서 `dot -Tsvg` | 문서 예에서처럼 edge title, path, 화살촉 polygon 1개. 문서 예의 버전은 2.47.1. [공식 예](https://graphviz.org/docs/outputs/svg/#example-simple-graph-rendered-with--tsvg) |
| Graphviz 공식 유한상태 예 | GitLab 고정판의 `graphs/directed/fsm.gv`를 직접 실행 | 저장소 판의 라벨·방향·화살촉 14/14. 갤러리 웹판의 상태명은 0/1, 실행판은 LR_0/LR_1이다. [갤러리](https://graphviz.org/Gallery/directed/fsm.html) · [실행 입력](https://gitlab.com/graphviz/graphviz/-/blob/00d9fb4479c21b021e510dfb2633f1058d695db7/graphs/directed/fsm.gv) |
| Graphviz 링크 원 시험 | 고정 `tests/graphs/url.gv`를 `dot -Tsvg`로 실행하고 linux.x86 기대 SVG와 비교 | href 19개 순서, edge title/label/화살촉 6개 내용이 같은지 원장의 두 배열에서 비교했다. 실제 회귀 하네스는 미실시. [원 입력](https://gitlab.com/graphviz/graphviz/-/blob/00d9fb4479c21b021e510dfb2633f1058d695db7/tests/graphs/url.gv) · [기대 SVG](https://gitlab.com/graphviz/graphviz/-/blob/00d9fb4479c21b021e510dfb2633f1058d695db7/tests/linux.x86/url_dot.svg) |
| Graphviz 연구 대조 | go/back 두 전이. 기본 SVG, `dir=none`, Cairo 및 img/inline | `dir=none`은 같은 title/label 2개에서 화살촉 2→0. Cairo에서도 화면 글자가 보이지만 `text`와 링크 0. 기본 SVG를 직접 열거나 inline으로 배치하면 DOM에 링크 4개, `img`로 읽으면 그림은 보이고 호스트 DOM 링크 0. 목적지 탐색은 미실시. [그림](graphviz/) |
| Jupyter 원 회귀 | nbconvert 7.16.6의 이미지 포함 on/off CLI 2건과 classic PNG metadata 1건 | pytest 2/2 및 1/1 통과. 시작 시 flaky 누락으로 CLI 수집 실패·IPython lexer 부재로 PNG 시험 실패. 두 의존을 시험 venv에 설치해 재실행. CLI 원 fixture는 Markdown 상대 JPEG 3개, PNG 시험은 display_data가 있는 독립 fixture. [로그](upstream-tests/) |
| Jupyter 연구 MIME bundle | nbformat 5.10.4의 작은 노트북, image/png와 text/plain을 같은 display_data에 저장. 별도 Markdown img도 있음 | lab 기본 HTML만 옮기니 display PNG는 data URL 90×34, Markdown PNG는 상대 경로 404. embed-images에서 두 PNG 모두 표시. exclude_output을 함께 쓰면 저장된 display PNG가 HTML에서 빠지고 Markdown PNG만 표시. [입력·화면](jupyter/) |

[실행 원장](cross-results.json)의 Graphviz 기대값과 실행값은 href 19/19가 순서까지 일치한다. [Graphviz SVG 출력 문서](https://graphviz.org/docs/outputs/svg/)가 명시한 Cairo의 XML 차이는 연구 대조에서 관측했다. 링크가 실제 화면의 작동 요소인지 판단할 때는 SVG 자체의 링크와 소비자 페이지의 포함 방식을 같이 확인한다. [URL 문서](https://graphviz.org/docs/attrs/URL/) · [SVG 2 처리 모드](https://www.w3.org/TR/SVG2/conform.html#processing-modes-for-svg-sub-resource-documents)

Jupyter에서 HTML 3종의 exporter는 각각 종료값 0이다. 기본/내장 HTML 모두 lab 템플릿의 RequireJS·MathJax CDN 요청이 오프라인 계측기에서 차단됐다. 두 이미지가 표시된 내장 경우에도 노트북의 모든 동적 기능이 독립 파일에서 제공된다는 일반화에는 별도 실행이 필요하다. 미확인 MIME·widget 재생은 이번에 실행하지 않았다. [nbformat display_data](https://github.com/jupyter/nbformat/blob/60b6151fedcbdc9f137fb2d223eeb10c935a8378/docs/format_description.rst) · [lab의 data_png](https://github.com/jupyter/nbconvert/blob/2ba58585f649c1a2024aadd58007ec138457cc58/share/templates/lab/base.html.j2#L205-L233)
