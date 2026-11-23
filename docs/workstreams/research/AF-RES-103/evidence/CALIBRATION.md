# 환경과 기준 렌더

[환경 지문](../environment.json)에서 Pandoc 3.6, pdfTeX 1.40.26, pdf2svg 0.2.4-1, MuPDF 1.25.1 및 Chromium 156.0.8078.79의 실행 파일 지문이 099와 일치한다. 실제 LaTeX 로드는 2024-11-01 patch level 2, standalone 1.5a, xcolor 3.02, PGF 3.1.10, PGFPlots 1.18.1이다. 099의 fmtutil-user 생성본과 이번 시스템 pdflatex.fmt 지문은 다르며 LaTeX 버전 문자열은 같다. K는 099 Lua의 pdflatex 인자를 사용한다. M/P와 독립 기준에는 recorder 및 no-shell-escape가 추가된다. 읽힌 Computer Modern 파일과 브라우저 글꼴 후보의 지문은 환경 원장에 있다.

| 대조 | 실제 표시와 종료 | 직접 증거 |
| --- | --- | --- |
| 독립 원문 기준 T0/T1 | 각 0, PDF 1쪽, 각 q₁–q₄와 방향 전이 8. T1 q₁ 외곽 청색·전체 채움 옅은 청색 | [T0 화면](reference/T0/pdf-page-01.png) · [T1 화면](reference/T1/pdf-page-01.png) · [좌표 판독](REFERENCE_SEAL.json) |
| 독립 원문 기준 T2 | 0, PDF 14쪽, 27개의 각도별 청색 선과 확대된 축/틱. 0·90도 경우도 보존 | [PDF](reference/T2/input.pdf) · [첫 쪽](reference/T2/pdf-page-01.png) · [최종 투영](reference/T2/pdf-page-14.png) · [방향과 좌표](REFERENCE_SEAL.json) |
| 독립 원문 기준 T3/T4 | 각 0, PDF 1쪽, 그림 각각 두 개. T3 E2 청→적, T4 적→청, 두 번째 E2는 q₂→q₁와 r | [T3](reference/T3/pdf-page-01.png) · [T4](reference/T4/pdf-page-01.png) |
| K 양성 T0 | reader 0, pdflatex 0, pdf2svg 0, Pandoc 0. 402×112 이미지와 앞뒤 문장 선택. 새 폴더 HTML 단독 이동으로 이미지 유지 | [실행](calibration/CAL-T0-K/receipt.json) · [DOM](calibration/CAL-T0-K/browser.json) · [화면](calibration/CAL-T0-K/browser.png) |
| K 음성 T1 | 기준 원문 성공. 격리 pdflatex 1, xcolor AFControl 미정의. Pandoc 83 | [전달 TeX](calibration/CAL-T1-K/children/01-pdflatex/diagram.tex) · [로그](calibration/CAL-T1-K/children/01-pdflatex/stdout) · [099 대응 실행](https://github.com/laadkke-arch/agentflow-open/blob/01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7/docs/workstreams/research/AF-RES-099/evidence/matrix/B-CUSTOM-PREAMBLE/pandoc.stderr.txt) |
| M 범위 T4 | 각 pdflatex와 변환 0, writer 0. 두 그림과 문장 셋. 첫째·둘째 원 목록 및 발색을 따로 기록 | [선택한 원 행](calibration/CAL-T4-M/selected-lines.json) · [DOM](calibration/CAL-T4-M/browser.json) · [화면](calibration/CAL-T4-M/browser.png) |
| P 양성 T0 | pdfLaTeX 0, MuPDF 0, 595×842 페이지 이미지. 그림과 문장은 화면에 보이지만 호스트 DOM 선택은 0/2 | [페이지 SVG](calibration/CAL-T0-P/out1.svg) · [DOM](calibration/CAL-T0-P/browser.json) · [화면](calibration/CAL-T0-P/browser.png) |

Chromium의 실제 file URL 이동은 관리 정책에서 차단됐다. 최초 교정은 오류 페이지의 비동기 전환과 겹쳐 같은 탭의 루프백 이동도 중단됐다. 새 탭으로 바꿔 재실행하니 Playwright 오프라인 컨텍스트의 로컬 바이트 공급이 작동했다. 이동 시험은 sibling SVG가 없는 폴더에서 독립 컨텍스트를 열어 검사한다. 본 30자리는 이 교정 후 시작한다. [첫 오류](calibration-recovery/first-browser.json) · [교정 후](calibration/CAL-T0-K/browser.json) · [오프라인 재열기](calibration/CAL-T0-K/moved.json)
