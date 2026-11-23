# AF-RES-103 작업 계약과 사전 판정

목적은 전체 페이지, 그림 한 조각, 검색 가능한 본문을 각기 전달할 때 필요한 입력과 반환 링크를 고르는 것이다. 제품 코드나 중앙 진행표는 작업 경로 밖에 있다. 공통 [manifest](manifest.json)의 base는 GitHub 시작 시점의 `ac7abc85e12b3a5b5f87b694d00e9511332fe272`다. 계획판 `ace1a06a13ea435f5cb6a3e340ad24f03f68ecae` 이후 변경은 `docs/automation/dot-control.json` 하나였다. 읽은 운영 규칙·연구 브리프·AGENTS·STATE·Dot 안내의 blob은 [입력 원장](inputs.json)에 있다. [공통 계약](https://github.com/laadkke-arch/agentflow-open/blob/ac7abc85e12b3a5b5f87b694d00e9511332fe272/docs/collaboration/contract.json) · [계획판 비교](https://github.com/laadkke-arch/agentflow-open/compare/ace1a06a13ea435f5cb6a3e340ad24f03f68ecae...ac7abc85e12b3a5b5f87b694d00e9511332fe272)

운영 의존은 등록 인계판 `8426e3511114fd36a00fc57bc270cfe3f5d573c8`이다. 시작 시 원격 끝을 GitHub에서 확인했다. 연구 입력은 099 결과 `01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7` 및 096 Lua `1d399f630930d2763459e16509c5224b0cded9a0`에 고정한다. 099 결과에서 등록 인계까지 HANDOFF.md 한 파일이 추가됐다. 전체 비교 및 사용 blob은 [입력 원장](inputs.json)에 있다. [099 인계](https://github.com/laadkke-arch/agentflow-open/blob/8426e3511114fd36a00fc57bc270cfe3f5d573c8/docs/workstreams/research/AF-RES-099/HANDOFF.md) · [099 결과](https://github.com/laadkke-arch/agentflow-open/blob/01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7/docs/workstreams/research/AF-RES-099/RESULT.md)

## T2 선정 순서

2025-01-01 UTC 이전 안정 릴리스의 고정 트리에서 examples/test 계열의 소스 경로를 바이트 순서로 읽었다. 확장자와 파일 역할로 원 소스, 실행 설정, 부속물 및 기대 로그를 구별했다. 완전한 LaTeX 문서와 외부 사용자 정의의 실제 그림 참조가 모두 필요하다. 처리기별 전체 문서는 별도 기록했다. 표준 패키지 로드와 버전 호환 키만 있는 입력은 이 조건을 충족하지 않는다. 그림을 매크로로 생성한 경우에도 실호출에 전달된 그림 밖 값이 그림의 배치를 결정하면 적격이다. 성공 여부나 M 지원 여부는 선정에 사용하지 않았다. 소스 전체와 부속 파일 검토, 탈락 사유는 [T2 선정 영수증](evidence/T2_SELECTION.md)에 있다.

PGF 3.1.10 공식 시험에서 독립 문서 조건을 충족하지 못해 PGFPlots 1.18.1로 넘어갔다. 첫 적격은 `unittest_3d_0.tex`다. 전체 문서 69행, 원시 TikZ 그림 틀 하나, 루프 매개변수와 여섯 명시 호출로 출력 그림 27개다. 원문의 섹션 제목과 틱 라벨은 관측한다. 앞뒤 산문 문장은 해당 없음이다. [원 소스](https://github.com/pgf-tikz/pgfplots/blob/d8e70d407d4f40a02cfdcc4783e7ff3028d8c5c6/source/latex/pgfplots/pgfplotstest/regressiontests/unittest_3d_0.tex#L16-L69)

## 실행 및 채점

| 경로 | 전달과 산출물 | 성공의 분모 |
| --- | --- | --- |
| K | T0–T4 원 TeX와 Pandoc `latex+raw_tex`, 099 고정 Lua 및 `--embed-resources`. PATH 계측은 자식의 실제 argv, stdin·stdout·stderr, 임시 TeX/PDF/SVG 지문을 보존한다. | 약속은 **그림별** 이미지와 호스트 본문. 모든 그림·대응 라벨, 원 스타일, 본문 및 순서, HTML만 이동 후 이미지가 일치해야 함 |
| M | 같은 Pandoc reader와 HTML writer. 선택된 RawBlock을 그림별 새 standalone TeX로 컴파일하고 선택된 정의 원 행을 프리앰블/본문 순서를 보존해 넘긴다. 이미지 노드 치환과 `pdf2svg`는 연구자 구현이다. | K와 같은 기준. 원 그림 ID를 안전하게 연결할 수 없는 동적 입력은 구조화된 미지원 실패 |
| P | 전체 입력을 독립적으로 pdfLaTeX, 공개 답의 `mutool draw -oout.svg`로 페이지 SVG를 만든다. 연구자가 페이지 번호 순으로 data URL img를 넣는다. | 약속은 페이지 외관 및 오프라인 페이지 이미지. 그림별 분리와 호스트 본문은 별도 열로 채점 |

그림은 PDF 원소의 위치, 선 시작과 끝, 화살촉, 색과 텍스트를 원 소스와 연결한다. T0/T1은 상태 4, 방향과 라벨을 묶은 간선 8, 초기 화살표, 수락 이중원 2, 문장 둘이다. T3/T4는 두 그림 각각 같은 분모와 E2의 판별 차이, 문장 셋이다. T2는 27개 투영의 위치, 청색 선 경로·촉·축과 틱을 판독한다. 원문 추출·화면의 읽기 순서를 함께 기록한다. PDF의 페인트 순서와 화면상의 텍스트 위치는 T0/T1에서 다를 수 있다. AST·SVG 구조 개수·프로세스 종료값은 보조 지표다. 판별 실패로 뒷단을 볼 수 없으면 미확인으로 둔다. [독립 기준 PDF의 사전 판독](evidence/REFERENCE_SEAL.json)

성공은 경로의 약속 기준을 전부 만족한 자리의 수다. 색·방향·라벨·호스트 본문 검색 가능성·alt 속성·단일 파일 이동성은 서로 다른 관측이다. Chromium에서 호스트 텍스트 노드를 실선택하고 찾기 쿼리를 실행한다. 이동은 새 폴더 내 HTML 한 파일과 새 오프라인 컨텍스트를 사용한다. 로컬 file URL 차단 시 차단 증거를 남기고 로컬 파일 바이트만 공급한 루프백 컨텍스트를 사용한다. 스크린 리더는 별도 확인이 필요하다. 반복은 관측 의미와 주 출력 바이트를 별도로 비교한다. 두 실패에 같은 산출물 부재가 반복돼도 바이트 일치 쌍으로 세지 않는다. [30자리 계획](evidence/plan.json)

## M 선언·범위 규칙

연구자가 원 소스에서 그림별 행 번호를 직접 골라 [M 선언 원장](evidence/definitions.json)에 표기했다. 운영에서 사용자가 제공하거나 문서에 명시할 동일한 입력을 모사한다. 선언 전부를 정적 분석하거나 임의의 TeX를 복원하는 처리기는 이 연구에 포함되지 않는다.

- 지원하는 선언은 한 물리 행의 리터럴 `\definecolor{이름}{RGB}{정수,정수,정수}` 또는 소수 모델 `rgb`, 리터럴 TikZ 설정/`/.style`을 담은 `\tikzset`, 인자와 기본값이 없는 리터럴 본문의 `\newcommand{\이름}{값}`이다. 원문의 주석 제외, 균형 중괄호, 구체적인 값만 허용한다. 계산·훅·조건문·포인터나 간접 키 생성은 범위 밖이다.
- 명시적인 `\begingroup`/ `\endgroup`으로만 연구자가 범위 스택을 대조했다. 현재 위치까지 진입한 그룹에서 아직 유효한 선언을 바깥 선언부터 원래 행 순서로 전달한다. 그룹을 닫으면 그 안의 행이 밖의 그림 목록에서 빠진다. 같은 스타일을 다시 정의한 행은 이전 행과 함께 유지하며 TeX가 마지막 유효 정의를 적용한다. 중복 `\newcommand`는 정상 재정의로 해석하지 않는다.
- 지원 그림은 중첩되지 않은 명시적 `\begin{tikzpicture}…\end{tikzpicture}` 한 블록과 같은 RawBlock 매치의 일대일 대응이 있어야 한다. 선언이 호스트의 정의/반복/조건문 안에서 그림을 만들거나 매개변수·간접 제어명·외부 입력에 의존하면 동적 의존으로 판정하고 해당 원 행을 기록한다. T2의 `\def\testplot#1#2` 및 `\foreach`가 이 기준에 걸린다. 추가 입력 후보는 완전히 펼친 그림 한 개, 그 위치의 구체적 정의, 원 PDF 페이지이다.
- M에는 K의 고정 문서 클래스, xcolor·TikZ 및 세 라이브러리, 투명 배경 초기화만 기본 제공한다. T0의 원본 `\tikzset`도 M에는 명시적으로 넘긴다. 원본과 동일한 생략을 가진 K, 순서를 잃은 M, 필요한 전역 선언을 뺀 M을 각각 비교할 수 있다.

별도 대조는 T1 색/설정 제거, T3 둘째의 재정의/색 제거 및 역순, T4 첫째 역순/그룹 누출, 무관 선언 추가, 그림 제거, 동일 라벨의 두 색과 방향, 외부 SVG 없는 이동 및 SVG/Graphviz의 범위 예다. [대조 계획](evidence/plan.json)
