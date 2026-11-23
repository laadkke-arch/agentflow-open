# 수정 전 기준과 도구 봉인

| 원본 | 독립 기준 1·2와 보존 항목 | 상류 대조·미확인 |
| --- | --- | --- |
| T | 두 번 모두 pdfLaTeX 0, 14쪽·27 shaft와 stealth 색 청색. 선 시작·두 꺾임·마지막 segment 끝과 tip은 계승 좌표에 대해 최대 0.00005pt 차이. g12 p6(s70/71), g21 p11(s35/36). g12 투영 시작 (217.2700,543.4110), tip (217.2700,382.3491). g21 시작 (217.2700,312.2760), tip (217.2700,151.2141). 좌표는 PDF 좌상단 pt. [기준 1](baseline/T-base-1/input.pdf) · [기준 2](baseline/T-base-2/input.pdf) · [두 쪽의 원 픽셀](baseline/T-base-1/g12-g21.png) | 상류 PGFPlots 자체 PDF는 미확인. 계승 좌표 [AF-RES-103](https://github.com/laadkke-arch/agentflow-open/blob/41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd/docs/workstreams/research/AF-RES-103/evidence/REFERENCE_SEAL.json) |
| S | 두 번 모두 WPT in-page test 1개 통과와 운영 단계 0. 2.000s의 두 삼각형 135°. 시작 (0,15), 끝 (50,65). 정확 청색 픽셀 52/169. 녹색 원 stroke와 접합 모양 동일. [기준 1 PNG](baseline/S-base-1/screen.png) · [기준 2 PNG](baseline/S-base-2/screen.png) · [계산값](baseline/S-base-1/observed.json) | Start 마커가 왼쪽 SVG 테두리에서 잘린 모습이 원 화면이다. 상류 정지 픽셀 기대 미확인. 상류 샘플 시간과 각은 [fixture L67–102](https://github.com/web-platform-tests/wpt/blob/03d41fe0fe3338c66cb56644b8a1705fe2e7247b/svg/animations/animate-marker-orient-from-angle-to-angle.html#L67-L102). 전체 wptrunner 미실시. |
| D | 두 번 모두 dot 0, PNG 307×1336. 14개 라벨과 21개 검정 간선. 화살촉 0. 첫 두 소스 간선은 SVG edge1·edge2이나 e15가 그 사이에 먼저 출력된다. Arial 요청은 dot에서 Liberation Sans Regular로 resolve. [기준 1 SVG](baseline/D-base-1/output.svg) · [기준 2 SVG](baseline/D-base-2/output.svg) · [기준 화면](baseline/D-base-1/screen.png) | [상류 DOT 기대](upstream/Heawood.gv) · [상류 PS 기대](upstream/Heawood.ps) · [Ghostscript가 그린 상류 PS](upstream/Heawood.png). 상류 DOT의 21개 endpoint 쌍은 일치하고 viewBox 절대 좌표와 PS 변환은 세대별로 다르다. 상류 전체 Graphviz 회귀 하네스 미실시. |

## 기준 픽셀 교정

D 화면의 SVG 경로는 폭 1이고 DPR 1에서 x·y가 소수 픽셀에 놓인다. ±2 허용으로 단색 검정만 세면 첫 두 간선에서 0이었다. 패치 실행 전에 같은 PNG, SVG, 기존 샘플 좌표로 안티앨리어싱 픽셀도 별도로 셌다. 중성은 채널 폭 ≤2와 최소값 ≤200, 빨강은 R이 G/B보다 ≥25 높고 G/B 차이가 ≤2일 때 잡는다. 각 path 길이의 30/50/70% 좌표에서 5×5 패치를 센다. 정확 픽셀도 보존했고 상대 색과 전체 기하·순서는 별도 검증한다. [교정 기록](baseline/dot-raster-calibration.json)

## 판과 패치

실제 환경은 Debian 13, pdfTeX 1.40.26, PGFPlots 1.18.1, PGF 3.1.10, `compat=1.3`, Graphviz `dot` 2.42.4, Chromium 156.0.8078.79다. T PDF에는 Computer Modern Type 1 글꼴이 포함된다. S의 SVG에는 텍스트 글리프가 없고 원 테스트 `title`만 판독한다. D Chromium의 폰트 대체는 설치 환경에 종속된다. 포맷·바이너리·패키지·폰트 SHA는 [도구 원장](../environment.json)이다. 스크린은 PyMuPDF 1.5배 또는 Chromium DPR 1이며 PDF에 시각 강제를 적용하지 않는다.

패치는 원본 사본에서만 적용하며 [patches](../patches/)에 12개 주 변경과 보조 대조를 둔다. T A 단일의 원 매개변수 비교와 B 단일의 반복 count는 사전 [protocol](../protocol.json)에 있다. S B는 원 marker의 checked animation ID를 유지하고 복제 문서에서 중복 복제 ID만 제거한다. D B는 첫 edge statement 내부에 접혀 있는 실제 첫 edge를 분리한다. 각 패치의 목적 충족 여부는 기준을 봉인한 뒤에 확인한다.
