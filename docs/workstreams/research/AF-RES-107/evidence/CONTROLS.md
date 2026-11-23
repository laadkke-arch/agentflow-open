# 별도 대조와 상류 재생

| 대조 실행 | 실제 관찰과 다른 가정을 시험한 지점 | 근거 |
| --- | --- | --- |
| T-args-B | PITCH 사용 위치에서 `p=0`로 분기하자 g12·g21 모두 빨강. 두 점의 `view`가 같을 때 호출 줄과 인자만으로 발생을 고르면 범위를 잘못 잡는다. | [패치](../patches/T-args-B.diff) · [PDF](controls/T-args-B/input.pdf) · [좌표](controls/T-args-B/observed.json) |
| T-revert | A 단일을 적용한 뒤 같은 사본에서 역패치했다. 입력 SHA가 원본과 같고 27개 청색, 14쪽·그리기·문자·화면이 기준과 같았다. 원시 PDF 날짜·ID는 별도다. | [영수증](controls/T-revert/receipt.json) · [PDF](controls/T-revert/input.pdf) |
| T-local-positive | PITCH 첫 반복을 펼치고 지역 `every axis plot post`를 적용했다. g12만 빨강, g21 청색이다. 일반 B의 `count`와 다른 선택 방법이다. | [패치](../patches/T-local-positive.diff) · [p6](controls/T-local-positive/page-06.png) · [p11](controls/T-local-positive/page-11.png) |
| S-marker-B-shorthand | 사용 위치의 CSS `marker`를 편집했더니 두 끝과 안쪽 꺾임 (50,15)에도 빨간 마커가 그려졌다. 기존 SMIL 테스트는 통과했다. | [원 화면](baseline/S-base-1/screen.png) · [대조 화면](controls/S-marker-B-shorthand/screen.png) · [SVG](controls/S-marker-B-shorthand/rendered.svg) · [SVG 2 marker shorthand](https://www.w3.org/TR/2018/CR-SVG2-20181004/painting.html#MarkerShorthand) |
| S-use 격리·독립 정의·복사 | 평소에는 모양이 같은 파랑 두 개다. 상속 가능한 첫 use 변경, 두 독립 정의 중 첫 정의 변경, 연결 템플릿 변경에서 각 첫 발생만 빨강이다. 복사된 두 번째 직사각형은 청색이다. | [입력 L5–20](control-inputs/use.svg#L5-L20) · [패치](../patches/S-use-controls.diff) · [기준 화면](controls/S-use-base/screen.png) · [관측](controls/S-use-edited/observed.json) |
| S-use 정의에서 선택 | 기존 use들이 `--ink`에 각자 색을 갖고 있다. 공유 정의에 `var(--ink, blue)`를 연결한 한 줄 편집은 첫 발생만 바꿨다. 원본 S의 marker fill은 그런 인자를 쓰지 않는다. | [입력](control-inputs/use.svg#L9-L20) · [편집 화면](controls/S-use-edited/screen.png) |
| S-use 상속이 막힌 경우 | host `use`의 계산 fill은 red였고, 연결된 도형의 명시 fill이 blue라 두 실제 픽셀은 청색이었다. | [상태와 픽셀](controls/S-use-edited/observed.json) · [SVG 2 스타일 상속](https://www.w3.org/TR/2018/CR-SVG2-20181004/struct.html#UseStyleInheritance) |
| D-chain-B | 첫 edge가 적힌 **한 문장** 끝에 `color=red`를 붙이자 e01–e14 전체가 빨강이다. e16 근접 5×5 패치에 교차 간선 픽셀이 잡혀 SVG endpoint와 다른 두 점을 같이 읽었다. | [원 사용](inputs/D.gv#L21-L24) · [대조 화면](controls/D-chain-B/screen.png) · [대조 SVG](controls/D-chain-B/output.svg) |
| D late default / reassign | 기존 검정 default를 뒤에서 빨강으로 바꾸면 앞으로 생성되는 b→c만 빨강이다. 이미 생성된 a→b를 뒤에서 같은 endpoint로 재지정하면 strict의 동일 간선 한 개가 빨강이다. 두 실행은 각각 5간선이다. | [원 입력](control-inputs/history.gv) · [default](controls/D-history-default/output.svg) · [재지정](controls/D-history-reassign/output.svg) · [DOT 규칙](https://gitlab.com/graphviz/graphviz.gitlab.io/-/blob/ea52d54e7570cf6238586a88d11e04f61d76c5d3/content/en/docs/lang.md#L146-179) |
| D 범위로 선택한 A | local default를 수정했을 때 a→d만 빨강이다. 같은 subgraph의 a→c에는 명시 검정이 있고 바깥 간선은 별도 생성을 따른다. | [패치](../patches/D-scope-A.diff) · [화면](controls/D-scope-A/screen.png) |

실행은 11회다. S의 `<use>` 쌍 다섯 개는 기준/편집 SVG 두 번에 같이 두었다. D 역사 비교는 기준 하나와 편집 세 개다. T 각도·원복·펼침은 각각 1회다. 원 SVG 마커 shorthand와 D 원 chain 대조는 각 1회다. 주 24회의 3원본과 별도다. [전체 판독](verification.json)

6개의 별도 상류 회귀도 열어 예상과 연결했다. PGFPlots의 colormap cyclelist와 CSV/ungrouped foreach assert 각각 exit 0이다. WPT use-inheritance와 template의 attr selector 변경은 각각 420×220 전체 화면이 예상과 정확히 같았고 초록 10,000픽셀이었다. Petersen의 색 프로브 3/3과 arrows 촉 위치 프로브 4/4가 기대 DOT와 일치했다. 원 저작을 임의 fixtures로 대체하지 않았으며 두 종류의 추가 실행은 주 지표에 합산하지 않는다. [원본과 기대판 지문](upstream/support-inputs.json) · [직접 재생 영수증](upstream/replays/) · [1차 자료 원장](../sources.jsonl)
