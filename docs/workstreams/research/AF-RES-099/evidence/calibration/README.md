# 실행환경 교정

| 입력 | 실제 경계 | 열어 본 증거 |
| --- | --- | --- |
| FIRST-B, 원 TeX 그대로 | Pandoc 83. 시스템 format으로 pdflatex 0. PATH에서 pdf2svg execve가 모두 ENOENT이며 실행기 127. SVG·HTML 없음. 임시 PDF 바이트를 복사하지 않은 시도 | [오류](FIRST-B/pandoc.stderr.txt) · [strace](FIRST-B/trace.txt) · [종료값](FIRST-B/exit.txt) |
| 포맷 준비 | 작업 경로의 pdflatex·xelatex format을 fmtutil-user로 생성. 두 명령 0. format을 찾는 kpsewhich에는 엔진을 지정 | [명령](format-runs.jsonl) · [format 조회](Q2-POS/found-format.stdout.txt) |
| Q2-POS | 작은 standalone TeX에서 PDF, pdf2svg SVG, MuPDF SVG, 외부 SVG를 읽은 HTML을 각각 생성. 3개 실제 변환 모두 0. 브라우저에서 218×51, CAL 이중원, 초기 화살표, yes를 가진 우향 전이, OK가 보임 | [compile log](Q2-POS/calibration.log) · [PDF](Q2-POS/calibration.pdf) · [SVG](Q2-POS/calibration.svg) · [HTML](Q2-POS/calibration.html) · [브라우저](Q2-POS/calibration-browser.png) |
| Q2-NOFMT | 교정된 파일 경로에서 TEXFORMATS만 빈 디렉터리로 바꾸고 MKTEXFMT=0. kpsewhich 1, pdflatex 1, Pandoc 83. converter 호출 0, SVG·HTML 없음 | [child](Q2-NOFMT/events/00-pdflatex.json) · [오류](Q2-NOFMT/pandoc.stderr.txt) |
| Q3-OTHER | 연구 Markdown의 .tikz CodeBlock 하나. pdflatex 0 → Inkscape 0 → Pandoc 0. 관측 복사본에서 CodeBlock 콜백 1회. 77×20 파란 OTHER 화살표가 보이고 원 그래프 0/4·0/8 | [입력](Q3-OTHER/other.md) · [관측](Q3-OTHER/observed.stderr.txt) · [HTML](Q3-OTHER/other.html) · [브라우저](Q3-OTHER/browser.png) |
| Q3-UPSTREAM | 지정 diagram의 원 test/input-tikz.md. xelatex와 Inkscape 각 2회 모두 0, Pandoc 0. figure/일반 img 2개와 열리는 SVG 2개. upstream runner 전체는 미실시 | [실행 HTML](Q3-UPSTREAM/actual.html) · [두 이미지의 브라우저 관측](Q3-UPSTREAM/browser.json) · [고정 upstream fixture](https://github.com/pandoc-ext/diagram/blob/023b31752cb5b63cd8bab828b268fa60ebd16d0c/test/input-tikz.md#L1-L62) |

file URL 첫 브라우저 시도는 관리 정책으로 막혔다. 각 로컬 결과 디렉터리만 제공하는 Playwright 라우팅으로 바꾸어 Chromium의 오프라인 컨텍스트에서 다시 열었다. 초기 계측기 인자 위치를 고친 뒤, 자체 CodeBlock 초안의 `stealth'`에는 필요한 arrows 라이브러리가 없음을 TeX 로그로 확인했다. 작은 양성 CodeBlock에서는 기본 화살촉을 사용했다. 원 연구 TeX·봉인 Lua는 이 교정과 별개다. [file 오류](pilot/file-scheme-blocked.json) · [TeX 오류](pilot/legacy-arrow-tex-error.txt) · [Pandoc 오류](pilot/legacy-arrow-pandoc.stderr.txt)

[원장](runs.jsonl)의 artifact 지문은 각 실행 시점의 목록이다. xelatex/inkscape 관측의 하위 프로세스는 같은 원장에 있으며, 임시 출력은 Q2의 핵심 양성 파일 및 Q3의 HTML/SVG로 표본을 골라 보존했다. FIRST-B는 래퍼를 쓰기 전의 실제 실패이며 096에서 관측한 format 실패와 단계가 다르다.
