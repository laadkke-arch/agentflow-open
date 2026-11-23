# AF-RES-107 · 공유 정의와 구체적 사용의 편집 범위

## 시작판과 소유 범위

`work/research-af-res-107`는 최초 원격 확인에서 비어 있었다. 2026-11-23 UTC에 최신 `e601fa1aed009106be983ae9b24e4778e793276f`에서 만들었다. 계획판 `49f603a98188fbf2009c4c490b0539f32d124e38`과의 차이는 `docs/automation/dot-control.json` 92줄 추가 하나다. 계약 fetch 중 원격 통합판 `32b6bb32989730df78d521c29a50dbebd3289b46`이 확인됐다. 추가 차이가 동일 진행표의 다른 작업 상태 6줄 교체였으므로, 작업 파일 커밋 전 fast-forward하고 `workbench.session start`를 그 판에서 다시 실행했다. 정책·제품 브리프·작업 계약 blob은 모두 같았다. 허용 경로는 `docs/workstreams/research/AF-RES-107/` 하나다. [계획판→계약판](https://github.com/laadkke-arch/agentflow-open/compare/49f603a98188fbf2009c4c490b0539f32d124e38...32b6bb32989730df78d521c29a50dbebd3289b46) · [읽은 blob과 배정](inputs.json) · [manifest](manifest.json)

등록 AF-RES-103은 DONE이며 결과가 `09503ac5452bbfb329aa0d5ff4bad9499924f277`이다. 의존 브랜치 실제 끝도 같다. 연구 입력은 검사된 `41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd`에 고정한다. 두 판 사이 추가는 `HANDOFF.md` 하나이며 이용한 결과·입력·TeX·좌표·다른 분야·재현 파일의 Git blob은 일치한다. 103의 30자리, 099 변환, P의 페이지·호스트 본문·날짜 지문은 인수한다. 이번에는 원본의 새 기준 렌더와 색 편집을 실행한다. [103 인계](https://github.com/laadkke-arch/agentflow-open/blob/09503ac5452bbfb329aa0d5ff4bad9499924f277/docs/workstreams/research/AF-RES-103/HANDOFF.md) · [103 결과](https://github.com/laadkke-arch/agentflow-open/blob/41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd/docs/workstreams/research/AF-RES-103/RESULT.md)

## 원본 모집

T는 원 TeX와 선행 판의 SHA-256과 바이트를 대조했다. 접힌 macro 입력의 문자열이나 매개변수 쌍으로 발생을 합치지 않는다. YAW 11회 뒤 PITCH 처음과 마지막인 g12·g21에 같은 (-30,0)이 들어간다. 동일 투영의 장·회차·문서 순서를 각각 식별한다. [T 원본 L21–69](https://github.com/pgf-tikz/pgfplots/blob/d8e70d407d4f40a02cfdcc4783e7ff3028d8c5c6/source/latex/pgfplots/pgfplotstest/regressiontests/unittest_3d_0.tex#L21-L69)

S와 D는 고정 Git tree의 파일 경로를 UTF-8 바이트순으로 나열해 각 처음 100 blob을 읽었다. 파일 형식이 다르면 열어 지원 파일로 기록했다. S는 표시 가능한 두 발생이 같은 정의를 참조하는 SVG 원 fixture와 그 기대 동작을 찾는다. 한 도형의 서로 다른 위치인 marker-start/end도 두 SVG 마커 발생으로 본다. SMIL 대상 지정만 반복되면 표시 발생의 수에 넣지 않는다. D는 변경할 색이나 촉의 **명시적 원본 기본 선언**을 상속한 식별 가능한 간선 최소 두 개가 있어야 한다. 그래프가 무향이면 색을 선택할 수 있다. AF-RES-103 `currentcolor-fill-stroke-repaint.html`과 `clusters.gv`는 공개 신규 원본에서 제외한다. [S 100개와 판단](evidence/selection/S.jsonl) · [D 100개와 판단](evidence/selection/D.jsonl)

S는 SVG 트리 2,654개 중 1–100번을 읽었고 40번 원본을 고른다. 첫 100개에 리터럴 `<use>`가 없었으며 두 `url(#marker)` 발생을 선택했다. 이 선택은 마커 paint의 자연 사례를 주 실험에 둔다. SVG `<use>` 상속·독립 복제는 별도 상류 근거 및 구성 대조에서 확인한다. WPT에는 시간별 공식 assertion과 고정 보조 스크립트가 있다. 2초 시점의 정적 상류 색 화면은 미확인이다. D는 `tests/graphs/` 265개 중 1–100번을 읽었고 4번 Heawood를 고른다. 앞선 폰트·ER 사례는 명시적 공유 간선색/촉 선언이 없다. Heawood의 연쇄는 14개의 간선을 만들고 단일 문장 일곱 개도 같은 기본값을 받는다. 원 예상 DOT와 PS를 로컬 `dot` 기준과 나란히 둔다. [S 공식 시간 기대](https://github.com/web-platform-tests/wpt/blob/03d41fe0fe3338c66cb56644b8a1705fe2e7247b/svg/animations/animate-marker-orient-from-angle-to-angle.html#L67-L102) · [D 원본](https://gitlab.com/graphviz/graphviz/-/blob/00d9fb4479c21b021e510dfb2633f1058d695db7/tests/graphs/Heawood.gv) · [D 예상 DOT](https://gitlab.com/graphviz/graphviz/-/blob/00d9fb4479c21b021e510dfb2633f1058d695db7/tests/share/Heawood.gv)

## 판정과 순서

A는 정의에서 편집한다. 정의가 원래 읽는 인자를 써도 된다. B는 실제 사용과 호출에서 편집한다. 사용을 분리하거나 그 위치의 지역 분기·지역 덮어쓰기를 쓸 수 있다. 각 목적의 기준은 고정된 값·ID 집합으로 판정한다. 도구가 종료 0을 돌려주면 출력이 판독 가능한지 확인하고, 변경 집합과 보존 항목은 따로 채점한다. 조건부 정의로 하나만 좁힐 수 있는 경우와 사용 한 줄이 여러 인스턴스를 바꾸는 경우를 별도 입력에서 찾는다. [기대 6행](EXPECTATIONS.md) · [판정과 실행 ID](protocol.json)

기준 3원본 × 2회, 주 3원본 × 2목적 × 2방식 × 2회다. TeX는 설치 pdfLaTeX/PGFPlots와 PyMuPDF 벡터·화면, SVG는 오프라인 Chromium의 고정 WPT 스크립트·computed style·화면, DOT는 `dot -Tsvg` 및 같은 Chromium의 SVG 재렌더를 쓴다. 실제 버전·폰트·실행은 묶음 ②부터 영수증으로 남긴다. 서로 다른 도구의 색·좌표 판단을 같은 파싱 규칙으로 간주하지 않는다. 날짜를 포함한 PDF 해시와 그림 의미·화면의 일치를 구분한다.

① 선정·기대·측정법의 원격 봉인 뒤 수정 없는 기준을 만들고 편집 diff를 준비한다. ② 두 방식을 원격 봉인한 뒤 주 실행과 대조를 수행한다. ③ 실행과 관측을 커밋한 뒤 결과표와 자가점검을 작성한다. ④ clean 결과 SHA에서 필수 두 검사와 자체 검산을 하고 GitHub의 고정판을 재열람한다. 마지막 인계는 별도 커밋이다.
