# AF-RES-099 · 원 TeX의 그림을 HTML에서 읽을 수 있는가

## 1. 입력과 약속

| 경로 | 원 요청·공개 답·연구 단계 | 고정 입력과 도구 | 그림과 추가 보존 조건 | 미확인 |
| --- | --- | --- | --- | --- |
| A | 질문자의 LaTeX→HTML 명령을 같은 입력으로 실행 | TeX SHA-256 `12b9969b2a0556c2a43933046a4a0b914a3911c7a97c22bb18425f4eb1aec9bc`, Pandoc 3.6 공식 바이너리 `7f1ac56064cdc02cdf8bd913f9ea45ba07fbb74419e755328c4571e4470769b2`, [diagram 023b31752cb5b63cd8bab828b268fa60ebd16d0c](https://github.com/pandoc-ext/diagram/blob/023b31752cb5b63cd8bab828b268fa60ebd16d0c/_extensions/diagram/diagram.lua#L609-L621) | C1은 HTML에서 원 그림 읽기. q₁–q₄, 방향·라벨 전이 8개, 자기 루프 2개, 수락 이중원 2개와 초기 화살표 | 질문 당시 main SHA와 도구판. [원 요청](https://stackoverflow.com/revisions/79393445/1) |
| B | AF-RES-096의 봉인 Lua를 `latex+raw_tex` 및 `--embed-resources`로 실행 | 같은 TeX·Pandoc. [봉인 Lua](https://github.com/laadkke-arch/agentflow-open/blob/1d399f630930d2763459e16509c5224b0cded9a0/docs/workstreams/research/AF-RES-096/evidence/pandoc/p4-raw-tikz.lua#L23-L43) SHA-256 `a63d10a7ee391a518ddf6f646a5714ebb902b00a3d4f608333d1c1f25581176c`; pdfLaTeX 및 [pdf2svg 0.2.4](https://github.com/dawbarton/pdf2svg/blob/v0.2.4/pdf2svg.c#L61-L124) | C1과 별도로 문장→그림→문장 및 HTML 한 파일을 측정 | 다른 preamble·다중 그림·다른 브라우저의 결과. [환경 지문](environment.json) |
| C | 공개 답의 PDF→페이지 SVG 명령. C+부터 연구자 HTML | 같은 TeX로 독립 컴파일한 PDF, 두 답 revision의 같은 `mutool draw -oout.svg` 인자. 관측판 MuPDF 1.25.1 바이너리 `b9588916750d90219b1511cf329776439c68e9a1ae1e6f92dc6532e21dd96df7` | C의 그림은 독립 SVG에서, C+의 그림은 HTML에서 채점. 검색 가능한 본문·오프라인 단일 파일은 부가 보존 조건 | 답변자 PDF와 프로그램판, 실제 통합 HTML, 답 첨부 화면의 이번 직접 접근. [최초 답](https://stackoverflow.com/revisions/04B193AD-FEB3-4D6A-9618-B08ADC4315FF/view-source) · [수정판](https://stackoverflow.com/revisions/073D223B-CBA7-45F6-AEB4-9A59CA3BC841/view-source) |

## 2. 실행 6자리

| 경로·반복·TeX SHA | 실제 프로세스·종료값·첫 실패 | AST·PDF·SVG·HTML 산출물 | 상태·방향 전이·라벨 | HTML 글·자원 | C+ 연구자 관측 | 증거·미실시 |
| --- | --- | --- | --- | --- | --- | --- |
| A1 · `12b9969b…` | Pandoc HTML 0, AST 0. reader의 TikZ 생략으로 엔진·변환기 호출 0 | [AST](evidence/matrix/A1/reader.json) · [HTML](evidence/matrix/A1/example.html) | 0/4·0/8·0/8 | 본문 2/2, img 0, 외부 참조 0 | — | [화면](evidence/matrix/A1/browser.png) · [경고](evidence/matrix/A1/example.stderr.txt) |
| A2 · `12b9969b…` | Pandoc HTML 0, AST 0. 같은 reader 결과 | [AST](evidence/matrix/A2/reader.json) · [HTML](evidence/matrix/A2/example.html) | 0/4·0/8·0/8 | 본문 2/2, img 0, 외부 참조 0 | — | [화면](evidence/matrix/A2/browser.png) · [별도 실제 콜백 관측](evidence/matrix/A-OBSERVED/observed.stderr.txt) |
| B1 · `12b9969b…` | 최초 환경 FIRST-B는 Pandoc 83, pdflatex 0, pdf2svg 실행 파일 부재. 준비 후 pdflatex 0→pdf2svg 0→Pandoc 0; AST 0 | [AST](evidence/matrix/B1/reader.json) · [임시 원 PDF](evidence/matrix/B1/events/0-diagram.pdf) · [원 SVG](evidence/matrix/B1/af096-tikz-3498ebd886bdcba16dc920ccec9d66eb2fbc6831.svg) · [HTML](evidence/matrix/B1/example.html) | 4/4·8/8·8/8, 초기·수락·루프 보존 | 본문 2/2, 중간 img 1, data URL, 외부 참조 0 | — | [화면](evidence/matrix/B1/browser.png) · [변환 호출](evidence/matrix/B1/events/01-pdf2svg.json) |
| B2 · `12b9969b…` | 새 캐시에서 pdflatex 0→pdf2svg 0→Pandoc 0; AST 0 | [AST](evidence/matrix/B2/reader.json) · [임시 원 PDF](evidence/matrix/B2/events/0-diagram.pdf) · [원 SVG](evidence/matrix/B2/af096-tikz-3498ebd886bdcba16dc920ccec9d66eb2fbc6831.svg) · [HTML](evidence/matrix/B2/example.html) | 4/4·8/8·8/8, 초기·수락·루프 보존 | 본문 2/2, 중간 img 1, data URL, 외부 참조 0 | — | [화면](evidence/matrix/B2/browser.png) · [변환 호출](evidence/matrix/B2/events/01-pdf2svg.json) |
| C1 · `12b9969b…` | pdfLaTeX 0→mutool draw 0. 1쪽 `out1.svg` | [원문 PDF](evidence/matrix/C1/aff2748b-266e-48f5-b2f7-7547936bb6aa.pdf) · [페이지 SVG](evidence/matrix/C1/out1.svg); Pandoc AST·HTML 단계 없음 | 독립 SVG 4/4·8/8·8/8 및 두 문장의 모양 보존 | 자체 산출물은 페이지 SVG | 외부·내장 모두 그림 표시 및 DOM 문장 0/2. 외부 SVG 제거 시 404 | [SVG 화면](evidence/matrix/C1/browser.png) · [C+ 외부](evidence/matrix/CPLUS-EXTERNAL-1/browser.json) · [누락](evidence/matrix/CPLUS-MISSING-1/browser.json) |
| C2 · `12b9969b…` | 새 캐시에서 pdfLaTeX 0→mutool draw 0. 1쪽 `out1.svg` | [원문 PDF](evidence/matrix/C2/aff2748b-266e-48f5-b2f7-7547936bb6aa.pdf) · [페이지 SVG](evidence/matrix/C2/out1.svg); Pandoc AST·HTML 단계 없음 | 독립 SVG 4/4·8/8·8/8 및 두 문장의 모양 보존 | 자체 산출물은 페이지 SVG | 외부·내장 모두 그림 표시 및 DOM 문장 0/2 | [SVG 화면](evidence/matrix/C2/browser.png) · [C+ 내장](evidence/matrix/CPLUS-EMBED-2/browser.json) |

## 3. 사용자 목적별 반환

| 사용자 목적 | 줄 링크와 볼 절 | 필요한 프로그램·파일·조건 | 관측 결과·부수 효과 | 반례·한 번 물을 조건 |
| --- | --- | --- | --- | --- |
| 문서 작성자가 원 TeX의 그림과 본문을 HTML에서 유지 | [Pandoc 공식 TikZ RawBlock 예](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/lua-filters.md#L777-L874) · [실행한 봉인 Lua](https://github.com/laadkke-arch/agentflow-open/blob/1d399f630930d2763459e16509c5224b0cded9a0/docs/workstreams/research/AF-RES-096/evidence/pandoc/p4-raw-tikz.lua#L9-L43) | Pandoc 3.6·`latex+raw_tex`, 봉인 Lua, 동작하는 pdflatex·standalone·TikZ 라이브러리·pdf2svg | B 2/2에서 원 그림만 이미지, 문장 2/2가 검색 가능한 글. 그림의 대체 텍스트 별도 필요 시 보강 대상 | 색 정의가 문서 preamble에만 있으면 [재현된 실패](evidence/matrix/B-CUSTOM-PREAMBLE/pandoc.stderr.txt). 그림이 문서 전역 정의를 쓰나요? |
| 필터 유지관리자가 입력 경계나 무출력을 진단 | [LaTeX reader의 TikZ 분기](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/src/Text/Pandoc/Readers/LaTeX.hs#L1112-L1124) · [diagram callback과 클래스 선택](https://github.com/pandoc-ext/diagram/blob/023b31752cb5b63cd8bab828b268fa60ebd16d0c/_extensions/diagram/diagram.lua#L523-L535) | reader AST와 고정 필터를 먼저 대조. 지원 입력 양성 예에는 TeX와 Inkscape 필요 | A 기본 reader는 그림 블록 0. raw_tex를 켠 RawBlock 1개에도 CodeBlock 호출 0. .tikz CodeBlock 대조는 그림 표시 | [다른 그림만 나타난 결과](evidence/calibration/Q3-OTHER/browser.png). 실제 reader 형식과 AST의 그림 노드 타입·클래스는 무엇인가요? |
| 이미 만든 PDF의 페이지를 벡터 그림으로 전달 | [공개 답 명령](https://stackoverflow.com/revisions/04B193AD-FEB3-4D6A-9618-B08ADC4315FF/view-source) · [MuPDF SVG 출력](https://github.com/ArtifexSoftware/mupdf/blob/1.25.1/docs/src/mutool-draw.rst#L25-L48) | 컴파일된 PDF와 MuPDF. 독립 SVG를 읽을 브라우저. 그림 옆의 글까지 페이지 외관에 포함된다는 조건 | C 2/2에서 1쪽 SVG로 원 그림·문장 모양 보존. C+에는 SVG 배치 markup이 추가됨 | [C+에서 본문 DOM 0/2](evidence/matrix/CPLUS-EMBED-1/browser.json). 페이지 그대로 보면 충분한가요, 본문을 검색해야 하나요? |
| 수신자가 오프라인에서 HTML 파일 하나로 보기 | [Pandoc의 embed-resources](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt#L1015-L1037) · [B의 단독 파일 관측](evidence/matrix/B-ONLY-HTML/browser.json) | 작성자가 이미 내장한 HTML과 수신자의 브라우저. 생성 도구는 작성자 쪽 준비 항목 | B HTML만 옮겨도 그림과 검색 가능한 두 문장 표시. C+ 내장도 그림이 보이며 문장은 그림 안에 있음 | 상대 SVG만 넣은 HTML을 보내면 [그림 404](evidence/matrix/CPLUS-MISSING-1/browser.json). 수신자는 글 검색이나 텍스트 대체도 요구하나요? |

## 반복과 근거

**세 경로의 의미 판정은 3/3쌍에서 반복됐다.** 직접 HTML을 생성한 A·B 네 자리 중 C1은 B의 **2/4**에서 충족됐다. A는 그림 0/2, B는 그림 2/2다. C의 자체 산출물인 독립 SVG는 **2/2**, C+는 SVG를 동반한 외부 2/2와 내장 2/2에서 원 그림이 보였다. C+의 본문은 4개 HTML 모두 DOM 0/2다. 이동한 B HTML은 준비된 SVG 원본을 옆에 두지 않아도 보였다. [요소별 대조](evidence/ELEMENTS.md) · [원장](runs.jsonl)

주 산출물 바이트 일치는 **3/3쌍**으로 A HTML, B HTML, C SVG가 각각 같다. 같은 viewport의 경로별 캡처도 **3/3쌍** 같다. B의 임시 PDF와 C의 보고서 PDF는 **0/2쌍**이 바이트 단위로 같았고 생성 시각이 달랐다. 네 PDF의 상태 원과 전이선을 포함한 드로잉 연산 24개는 원점을 맞춘 후 같은 위치에 놓였다. 차이의 전체 PDF 객체 귀속은 미확인이다. [반복 해시·PDF 좌표](evidence/verification.json)

A의 지정 filter 파일은 root symlink의 대상이다. 기본 reader 결과는 두 Para와 RawBlock/CodeBlock 각각 0이며, 별도 관측 Lua에서 document 콜백만 로깅됐다. 같은 입력을 raw_tex로 바꾸면 RawBlock 2개 중 TikZ 1개가 남지만 diagram의 CodeBlock 콜백은 여전히 0이고 HTML은 A와 바이트가 같았다. 양성 .tikz Markdown에서는 첫 클래스가 tikz인 콜백 1회, 기본 pdfLaTeX와 Inkscape 0 및 렌더된 다른 그림을 확인했다. 업스트림 예제는 xelatex·Inkscape 두 쌍으로 읽히는 SVG 두 개를 생성했다. [A 관측](evidence/matrix/A-OBSERVED/) · [양성 대조](evidence/calibration/README.md)

B에서는 외부 래퍼가 임시 삭제 전 **실제로 사용된** PDF를 복사했으며 두 번 모두 기존 봉인 Lua를 그대로 실행했다. 각 페이지 SVG는 19,761 bytes, SHA-256 `1cd5f27dc0274fea74a6cb371d52da22fa1e7921556b243380b72af2679a4791`다. HTML에서 추출한 base64 payload가 두 번 모두 바이트 일치했다. B의 그림 라벨은 16개 로컬 글리프 참조로 그려졌고, C는 67개 참조에 `data-text` 속성을 싣는다. C의 글리프 속성은 본문 DOM 글자와 별개다. [B 원 호출](evidence/matrix/B1/events/) · [B 디코딩](evidence/matrix/B1/decoded.svg) · [C XML 판독](evidence/matrix/C1/svg.json)

## 부록 · C+와 실패 교정

C의 공개 답 수정은 다른 HTML에서도 쓸 수 있음을 추가했다. 이 실험의 C+는 해당 SVG를 상대 `img src=out1.svg`와 base64 data URL로 각각 사용한다. 같은 그림과 페이지 글자 모양을 보존하면서 HTML에서 문장을 검색하려면 별도의 텍스트 층이 필요하다. 외부 SVG 제거 대조와 달리 B의 단독 HTML은 자체 SVG가 내장돼 있다. [외부 C+](evidence/matrix/CPLUS-EXTERNAL-1/page.html) · [내장 C+](evidence/matrix/CPLUS-EMBED-1/page.html) · [누락 응답](evidence/matrix/CPLUS-MISSING-1/browser.json)

최초 B는 이 환경에서 시스템 format을 읽어 pdfLaTeX 0까지 갔으며 다음 실행 파일 pdf2svg를 찾지 못했다. 096의 format 결손은 빈 TEXFORMATS 대조에서 다시 구분했다. 설치한 로컬 converter와 새 format을 사용한 후 B가 성공했다. 별도 원문 파생에 전역 색 `AFControl`을 정의하니 전체 문서 PDF는 생성됐지만 B의 고립 컴파일은 xcolor 오류 1, Pandoc 83이었다. Chromium의 file URL은 환경 정책에 의해 차단돼 로컬 파일만 응답하는 오프라인 계측 origin을 사용했다. [환경](environment.json) · [초기와 대조](evidence/calibration/README.md) · [전역 색 반례](evidence/matrix/B-CUSTOM-PREAMBLE/)

## 부록 · 다른 분야와 자료

Graphviz의 고정 유한상태 입력은 전이와 화살촉 14/14를 유지했다. 반면 `dir=none`은 SVG에 같은 방향쌍 제목과 레이블을 남기면서 해당 화살촉을 0개로 줄였다. 링크 4개, img와 inline에서의 호스트 DOM 링크 0과 4의 차이도 관측했다. Jupyter에서는 같은 노트북의 display_data PNG와 Markdown 상대 PNG의 내장 조건이 달랐다. 출력 제외 시 원 bundle이 있어도 PNG가 HTML에서 사라졌다. upstream nbconvert의 해당 회귀 3건은 실제 실행했다. WPT의 원 기대값은 직접 읽었다. [교차 분야 실행·로그](evidence/cross-domain/README.md)

자료 원장 60행 중 **39개**를 고유 1차 자료로 산입했다. 질문·답 2, Pandoc·diagram 9, TeX·변환기 13, 웹 규격·WPT 5, Graphviz 5, Jupyter 5다. 수정판, 동일 규격 장, 실패 접근, 내부 고정 결과는 분모에서 제외했다. [자료 원장](sources.jsonl) · [Q1–Q7 자가 검토](SELF_CHECK.md) · [재생 절차](reproduce.md)

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
| --- | --- | --- |
| A의 연구 SHA와 질문자의 당시 main·환경 사이에 간격이 있다 | 질문 당시 diagram SHA·Pandoc 버전·원 생성 HTML을 확보해 같은 TeX와 원 명령 실행 | 당시 판의 실제 콜백이 TikZ를 받고 읽히는 원 그림 4/4·8/8을 표시 |
| B 성공은 봉인 preamble의 원 단일 그림에 한정된다 | `B-CUSTOM-PREAMBLE` 입력과 다중 그림·서로 다른 전역 스타일을 가진 TeX를 같은 B로 실행 | 봉인 필터 본문과 입력 문맥 전달 방식을 유지한 채 사용자 스타일·방향·라벨 모두 표시 |
| C의 SVG→HTML 그림 표시와 검색 가능한 본문 사이에 간격이 있다 | 답변자가 실제로 사용한 통합 HTML 또는 C+ 두 방식에 별도 본문 태그를 붙인 입력에서 DOM·자원 시험 | 한 파일에서 원 그림과 검색 가능한 두 문장이 함께 보이며 네트워크 없이 로드 |
