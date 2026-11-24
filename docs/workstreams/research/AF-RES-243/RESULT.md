| 원요구·판 | 기대 위치·내용 | 처음 고른 근거 절 | 같은 작성자의 후속·주소 | 유지·반전·미확인 |
|---|---|---|---|---|
| [#449](https://api.github.com/repos/jgm/pandoc/issues/449) 2012 현행 본문, 판 미명시 | SumatraPDF sidebar bookmark | hyperref bookmarks; 인쇄 옵션과 분리 | [감사](https://github.com/jgm/pandoc/issues/449#issuecomment-4578454)만; [유지보수자](https://github.com/jgm/pandoc/issues/449#issuecomment-4577387) run-count 진단 | 미확인(목적 양립, 원작성자 재시험 없음) |
| [#3555](https://api.github.com/repos/jgm/pandoc/issues/3555) 2017 현행 본문, 판 미명시 | bookmark 대체 문자열; 본문 정상 | hyperref PDF strings | [원작성자](https://github.com/jgm/pandoc/issues/3555#issuecomment-291189527) 일반 수식은 수용, 로고 문제 잔존 | 유지(경로); 문제 일부 미해결 |
| [#4519](https://api.github.com/repos/jgm/pandoc/issues/4519) 2018 현행 본문 1.19.2.1 | 인쇄 목차 정상, outline 계층 오류 | hyperref bookmark hierarchy + titlesec 호환 | [원작성자](https://github.com/jgm/pandoc/issues/4519#issuecomment-377981012) bookmark를 titlesec 뒤에 로드해 해결 보고 | 유지(경로); 파일 미검사 |
| [#4856](https://api.github.com/repos/jgm/pandoc/issues/4856) 2018 현행 본문, 판 미명시 | 인쇄 목차 제목 변경 강한 추정 | Pandoc LaTeX 변수/템플릿, 조건부 outline | [동일 작성자 PR](https://github.com/jgm/pandoc/pull/4853) 이슈 이전 생성, 이후 병합; 후속 댓글은 [유지보수자](https://github.com/jgm/pandoc/issues/4856#issuecomment-415982505) | 미확인(후속 동일인 없음; PR 양립) |

표 1 단위: 지명 이슈/원작성자 요청 1행, 4/4 현행 본문. 최초 revision 0/4 확인, #4856 PR 존재 선노출, 원작성자 댓글 3/4(감사만 1), 실질 후속 2/4, 유지 2·반전 0·미확인 2. 실제 질문 응답 0/4. 판정은 산출물 층 경로의 양립성이지 실제 PDF 성공이 아니다.

| 한 조건의 두 값 | 첫 링크 A | 첫 링크 B | 질문 비용·줄 수 있는 답 | 판정이 뒤집히는 사례 |
|---|---|---|---|---|
| 종이 페이지에 목차 A vs 뷰어 탐색창 B | [Pandoc General writer options: --toc](https://pandoc.org/MANUAL.html#general-writer-options) | [hyperref §6.1.1 Bookmarks](https://mirrors.ctan.org/macros/latex/contrib/hyperref/doc/hyperref-doc.html) | 명시 시 1링크·0질문; 미명시 시 조건부 2링크·0질문 또는 1질문·1링크(답 후) | #449 B; X639855 B는 종이 목차를 원하지 않음, X194720 A는 종이 TOC의 링크 요청 |
| 인쇄 목차 깊이 A vs outline 깊이 B | [Pandoc --toc-depth](https://pandoc.org/MANUAL.html#general-writer-options) | [hyperref §7.24 bookmarksdepth](https://mirrors.ctan.org/macros/latex/contrib/hyperref/doc/hyperref-doc.html) | 기본이 연결되므로 독립 깊이가 필요한지 묻거나 옵션 두 값을 안내 | #4519 깊이보다 잘못된 부모 관계·패키지 순서; 깊이만 변경하면 실패 가능 |
| 제목 텍스트 A vs bookmark 표시 문자열 B | [Pandoc structural variables toc-title](https://pandoc.org/MANUAL.html#structural-variables), [2.3 template](https://github.com/jgm/pandoc/blob/2.3/data/templates/default.latex) | [hyperref §6.1.2 PDF strings](https://mirrors.ctan.org/macros/latex/contrib/hyperref/doc/hyperref-doc.html), [writer](https://github.com/jgm/pandoc/blob/1.19.2.1/src/Text/Pandoc/Writers/LaTeX.hs#L744-L764) | #4856 A 강한 추정, #3555 B 명시: 즉답 또는 A 우선/B 조건부; 대기 불필요 | #3555 본문 수식 정상이나 북마크 누락; #4856 contentsname 수정과 별개 |

표 2 단위: 독립 산출물/제어 축 3행, 두 링크 목적지의 원근거가 서로 다른 경우만 센다. 비용은 설계상의 링크/질문 수이며 실측 아님.

## 핵심 판정

**'목차'는 페이지 위에 보이는 목록과 탐색창의 outline이라는 서로 다른 산출물, 그리고 그 목록/노드의 문자열과 연결 대상·부모 관계를 가리킬 수 있다.** 요청에서 위치나 잘못된 층이 명시됐으면 즉답한다. 위치가 비어 있고 독립 경로가 둘이면 짧은 조건부 링크 두 개를 먼저 제시한다. 단순히 용어가 모호하다는 이유로 무조건 질문을 기다리지 않는다. 버전/엔진에 따라 실제 수정 위치가 바뀌며 잘못된 수정의 비용이 큰 경우 한 번의 질문이 타당할 수 있으나, 본 표본에서 그 시간 절약은 관측되지 않았다.

## Q1. 기대 위치 및 명시/추정의 분리

사전 입력은 [first-pass.csv 봉인판](https://github.com/laadkke-arch/agentflow-open/blob/95d6946fc000f32312b92015dfd4dd506c7074e8/docs/workstreams/research/AF-RES-243/first-pass.csv). 아래 원글은 최초 이력 복원판이 아니라 현행 title/body. created_at과 updated_at은 원장에 있으나 updated_at으로 수정 여부를 추정하지 않는다.

- I449: PDF, SumatraPDF sidebar, 이전 markdown2pdf와 새 pandoc 변환의 차이 및 탐색 기능은 명시. --toc 추가·종이 목록의 필요성·깊이·노드명·정확 엔진/버전 미기재. LaTeX 가능성은 추정. C449가 후에 pdflatex run-count 문제를 설명하지만 사전 필드로 소급하지 않는다.
- I3555: PDF, Markdown header와 raw TeX 비교, 수식 대체 문자열 The equation E=mc2 기대 및 bookmark에서 The equation만 남는 현상 명시. 본문 정상이라고 보고. TeX 경로는 강한 추정; PDF engine, Pandoc/TeX 버전, viewer, 인쇄 목차 출력/문자열, 깊이 미기재. 본문과 노드 이름의 분리가 핵심이지 목차 전체 삽입이 아니다.
- I4519: Pandoc 1.19.2.1, YAML subparagraph 및 toc, titlesec 포함; # one / ## one.two / # two / ## two.one; printed TOC correct, PDF bookmark tree가 네 항목을 일렬로 잘못 중첩. 정상 기대 부모 one→one.two, two→two.one은 입력 구조로부터 추론. engine 및 viewer와 hyperref/titlesec 버전 미확인. 계층 깊이 숫자와 각 노드의 부모 관계는 별도.
- I4856: toc-title의 LaTeX/PDF 미지원과 default template 변경 PR을 명시. 원하는 TOC 제목 문자열 자체, 화면, viewer, 설치판 및 엔진 미명시. 인쇄 목차 머리말이라는 강한 추정; PR 존재는 동시 노출, 실제 diff는 봉인 후 읽음. #4856을 완전 가림 원작성자 성공률의 분모에 넣지 않는다.

## Q2. 최소 질문과 정확한 첫 목적지

봉인 시 선택은 **즉답 3/4, 조건부 두 경로 1/4, 질문 우선 0/4**. 실제 질문은 보내지 않았다. first-pass의 CTAN package entrance / manual 후보 앵커를 아래 검증된 문서 절로 상세화했다. 봉인판을 다시 쓰지 않았다.

- 449 A(종이): [Pandoc General writer options --toc](https://pandoc.org/MANUAL.html#general-writer-options); B(탐색): [hyperref §6.1.1](https://mirrors.ctan.org/macros/latex/contrib/hyperref/doc/hyperref-doc.html), 역사 [P449](https://github.com/jgm/pandoc/commit/29c8f1554b412a46bee83e224b72e5931f172cb9). B 이미 명시, 재질문 금지. 해당 사건의 직접 수정 위치는 run count로 정정.
- 3555 A(본문의 수식/TeX 또는 인쇄 항목 표현): [Pandoc 1.19.2.1 MANUAL raw_tex extension](https://github.com/jgm/pandoc/blob/1.19.2.1/MANUAL.txt), [sectionHeader writer](https://github.com/jgm/pandoc/blob/1.19.2.1/src/Text/Pandoc/Writers/LaTeX.hs#L744-L764); B(bookmark 문자열): [2018 hyperref §4.1.2](https://ftp.math.utah.edu/pub/texlive/Contents/live/texmf-dist/doc/latex/hyperref/manual.html) 및 writer/plain branch. 인쇄 TOC 항목 문자열을 변경하라는 요청이었다면 raw TeX optional short heading/템플릿도 확인 대상(실제 출력 미확인). B 명시, 질문 불필요.
- 4519 A(인쇄 깊이): [1.19.2.1 manual L583–592](https://github.com/jgm/pandoc/blob/1.19.2.1/MANUAL.txt#L583-L592); B(탐색 계층): [hyperref 2018 §5.23·9.1.38](https://ftp.math.utah.edu/pub/texlive/Contents/live/texmf-dist/doc/latex/hyperref/manual.html), [2.1.3 template L270–272](https://github.com/jgm/pandoc/blob/2.1.3/data/templates/default.latex#L270-L272). A 정상이라고 명시되어 B만 즉답, 깊이 변경으로 부모 결함을 덮지 않음.
- 4856 A(인쇄 목차 제목): [2.2.3.2 MANUAL L1350–1355](https://github.com/jgm/pandoc/blob/2.2.3.2/MANUAL.txt#L1350-L1355), [2.3 template L363–364](https://github.com/jgm/pandoc/blob/2.3/data/templates/default.latex#L363-L364); B(outline 노드 문자열/등록): [hyperref §6.1.1·6.1.2](https://mirrors.ctan.org/macros/latex/contrib/hyperref/doc/hyperref-doc.html). A 강한 추정이므로 먼저 A, B라면 다른 경로임을 짧게 부기. 최신판 기능을 2018년 구판에 소급하지 않는다.

실제 일반 요청이 단지 "PDF에 목차를 넣고 싶다"라면 질문 문구 후보: **"PDF 페이지 안에 인쇄되는 목차인가요, PDF 뷰어의 왼쪽 탐색창(책갈피)인가요?"** 둘 다 원하는 경우 두 제어를 분리해 안내. engine이 pdfroff/HTML 기반이면 hyperref 경로를 바로 실행하지 말고 사용한 변환 명령을 확인. Q2의 A/B는 설명 말투 차이가 아니라 템플릿의 tableofcontents와 PDF outline 생성이라는 실제 제어 위치 차이(ISO/H18/T213). 두 깊이가 같은 값을 공유하는 경우는 별도의 질문 이익으로 세지 않는다.

## Q3. 옵션 전달과 역사적 제약

[formats.csv](formats.csv)에서 source ID별 원문 위치/버전 관계를 재현한다. 
1. [M119](https://github.com/jgm/pandoc/blob/1.19.2.1/MANUAL.txt#L583-L592)에서 --toc, --toc-depth. [W119](https://github.com/jgm/pandoc/blob/1.19.2.1/src/Text/Pandoc/Writers/LaTeX.hs#L165-L169)는 writerTableOfContents 및 깊이를 template context에 전달하며 book이면 깊이 1 감소. [T213](https://github.com/jgm/pandoc/blob/2.1.3/data/templates/default.latex#L364-L366)에서 toc 조건부 경로의 tocdepth counter와 tableofcontents. T213 L128 hyperref, L270–272 header-includes 순서. T213은 원작성자가 후에 재현했다고 한 2.1.3이지 1.19.2.1의 실제 template가 아니다. [G119](https://github.com/jgm/pandoc/blob/1.19.2.1/.gitmodules)에서 당시 template가 submodule임을 확인했지만 gitlink SHA와 해당 원파일은 Z119a–f 결측.
2. [HP99](https://ctan.katoptra.org/macros/latex/contrib/hyperref/doc/paper.pdf) §5.2.1–4의 당대 이전 문서와 [H18](https://ftp.math.utah.edu/pub/texlive/Contents/live/texmf-dist/doc/latex/hyperref/manual.html) 2018-09 §5.23 L1093–1101, [Hcur](https://mirrors.ctan.org/macros/latex/contrib/hyperref/doc/hyperref-doc.html) §7.24: bookmarksdepth 기본이 현재 tocdepth, 숫자 또는 이름 별도 설정 가능. --toc의 유무가 곧 bookmarks on/off가 아님. 동일 tocdepth에 의존하면 한 옵션이 두 층에 영향을 줄 수 있고 명시적 override로 갈라질 수 있다. 2018-09 매뉴얼은 2018 사건과 가까운 비교지만 사건 날짜보다 늦고 실제 설치판 미확인. 1999·현재판은 시점의 양쪽 대조이지 해당 버전 복원이 아니다.
3. [P449](https://github.com/jgm/pandoc/commit/29c8f1554b412a46bee83e224b72e5931f172cb9) tex2pdf' diff는 tableofcontents 문자열 있을 때 3회, 없을 때 1→2회로 변경. 따라서 사건 당시 --toc가 run count를 간접적으로 바꾸는 경로가 있었다. '목차 옵션 켜야만 북마크 생김'으로 일반화하지 않는다. [Bpkg](https://ctan.org/pkg/bookmark) 및 H18 §4.1.1은 별도 bookmark 패키지의 1회 생성 가능성을 설명. 해당 역사 바이너리 실행은 미확인.
4. [ISO 32000-1](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf) §7.7.2 Table 28 catalog /Outlines와 /PageMode, §12.3.3 Tables 152–153 노드 Title, Parent, First/Last, Prev/Next, Dest 또는 A. 페이지 내의 TOC(텍스트와 링크 annotation)와 outline tree는 구조적으로 독립. viewer가 탐색창을 펼쳐 보이는 여부까지 별개이므로 sidebar 안 보인다고 /Outlines 없음이라고 단정하지 않는다. ISO 본문 텍스트 읽음; 22MB screenshot 실패(ZISO); PDF sample 실행은 하지 않음.

## Q4. 제목 표현 세 층

| 사례·입력 | 본문 제목 | 인쇄 목차 항목 또는 제목 | 북마크 표시 |
|---|---|---|---|
| 3555 Markdown heading: The equation + raw texorpdfstring의 수식과 대체 텍스트 | 원작성자 정상 보고 | 실제 TOC 미기재/미확인 | 대체 E=mc2 누락 보고 |
| 3555 raw TeX section에 동일 표현 | 작성자 raw TeX 비교 성공 보고; 본문 별도 검사 없음 | 실제 TOC 미기재 | 원작성자 정상 보고 |
| 3555 일반 Markdown 수식 Equation + math | 실제 파일 미확인 | 미확인 | 원작성자 Equation E=mc^2 수용 |
| 3555 raw LaTeX logo와 대체 macro | 원작성자 정상 보고 | 미확인 | LaTeX 누락 보고; macro로도 해결 못 함 |
| 4856 toc-title 변수 (요청 값 미기재) | 문서 제목을 바꾸는 요청 아님 | 2.2.3.2 비교 템플릿 미지원; 2.3 contentsname 재정의 | outline Title 변경에 대한 명시 코드·출력 없음 |

기전: [W119 L744–764](https://github.com/jgm/pandoc/blob/1.19.2.1/src/Text/Pandoc/Writers/LaTeX.hs#L744-L764)는 렌더된 TeX와 stringify 기반 plain 대체를 각각 계산하고 다르면 texorpdfstring으로 감쌈. [SH119 L566–576](https://github.com/jgm/pandoc/blob/1.19.2.1/src/Text/Pandoc/Shared.hs#L566-L576)은 Math 내용 포함, raw inline 대부분 plain 경로에서 빠짐. [C3555](https://github.com/jgm/pandoc/issues/3555#issuecomment-291189527)는 이와 양립하나 실제 #3555 설치판은 미확인. [H18 §4.1.2](https://ftp.math.utah.edu/pub/texlive/Contents/live/texmf-dist/doc/latex/hyperref/manual.html) 순수 LaTeX 대체 macro를 제공하지만 이미 writer가 plain 텍스트를 잃었다면 TeX 단의 수정만으로 부족할 수 있음.
[P4853](https://github.com/jgm/pandoc/pull/4853) adds contentsname under toc; [M223](https://github.com/jgm/pandoc/blob/2.2.3.2/MANUAL.txt#L1350-L1355)과 [T223](https://github.com/jgm/pandoc/blob/2.2.3.2/data/templates/default.latex)에는 미지원, [T23](https://github.com/jgm/pandoc/blob/2.3/data/templates/default.latex#L363-L364)/[CH23 L186–187](https://github.com/jgm/pandoc/blob/2.3/changelog#L186-L187)에 추가. CH23 L59–60의 LaTeX reader 수정은 Markdown writer의 logo 문제가 고쳐졌다는 증거가 아님. #4856 자체에 특정 PDF/그림이 제공됐다는 증거 없음; 공개 PDF 직접 검사 0건(지명 네 사건). X7731 screenshot 접근 실패. 따라서 본문/목차/outline 세 층 동시 관측 0건, 알려지지 않은 부분을 정상으로 채우지 않았다.

## Q5. 후속 봉인 대조 및 반례

[followup.csv](followup.csv) 17개 관측 행에 행위자, 댓글/patch 주소, day window(정확 UTC null), 단계 기록. C449는 원작성자의 감사만, 유지보수자의 진단과 실제 code patch 있음; retest 없음. C3555는 원작성자가 plain math 만족 및 logo 실패 재현. C4519는 원작성자 2.1.2/2.1.3 재현 및 bookmark 추가 해결 보고, 유지보수자가 titlesec를 hyperref 이전 로드하는 맞춤 template 대안 제안과 위험 언급. H18 §9.1.38 및 Hcur §11.1.33의 호환성 한계와 일치. C4856은 PR 작성일이 이슈 이전, 병합과 종료는 이슈 이후이지만 댓글 작성자는 jgm; original-author post-issue reply 0. 이슈 닫힘과 성공 파일 생성은 다른 상태.
같은 작성자 실질 후속 2/4 유지, 반전 0, 나머지 미확인 2; exact revision 0/4; followup 자료 읽음 4/4, reply evidence 결측 2(감사만 1/없음 1). 실물 출력·컴파일 검증 0. #449의 2017년 pkaramol은 별도 원작성자이며 README 순서와 내부 링크에 대한 새로운 요구; 이를 hickford 후속으로 세지 않는다. 명시한 결과 층과 첫 절 경로의 양립성 평가이지 실제 해결의 성공률 아님.
맞춤 template는 해당 placeholder 미구현, 패키지 순서, documentclass가 목차를 bookmark로 등록하는지에 따라 달라짐. #4519는 원글의 4 headings 조건 자체에 반례(마지막 삭제 시 정상 보고). [X57284](https://tex.stackexchange.com/questions/57284/pdf-contains-incorrect-bookmark-hierarchy)는 유지보수자가 연결한 TeX hierarchy 별도 사건; [X7731](https://api.github.com/repos/jgm/pandoc/issues/7731)는 pdfroff/2.9.2.1에서 apostrophe [cq] 보고. 화면 Z7731 미확인: LaTeX 전용 설명으로 일반화 불가. 자세한 반례 및 사후 정정은 [COUNTEREXAMPLES.md](COUNTEREXAMPLES.md).

## Q6. EPUB 독립 대조

[W3C EPUB 3.3 REC 2026-01-13](https://www.w3.org/TR/2026/REC-epub-33-20260113/) §7.4.2 toc nav, §5.7.1–2 L3134–3217 spine의 ordered itemrefs, nav spine 포함 선택, linear 기본 yes, §7.5 nav를 content로 재사용 가능/hidden이 content flow 표시만 제한. 오래된 예제 EPUB3.0은 아래 OPF/XHTML 직접 판독 결과만 주장하며 최신 규범 준수 판정은 하지 않는다.

| 출판 예제 | nav → 이동 대상 | OPF → 읽기 순서 | nav가 읽기 순서에 있는가 |
|---|---|---|---|
| Creative Commons A Shared Culture (Jesse Dylan; Creative Commons, 2012) | [ECNAV](https://github.com/IDPF/epub3-samples/blob/main/30/cc-shared-culture/EPUB/xhtml/toc.xhtml) toc six links p10–p60; landmark TOC, Begin Reading | [ECOP](https://github.com/IDPF/epub3-samples/blob/main/30/cc-shared-culture/EPUB/package.opf) manifest toc properties=nav; spine cover linear=no, toc, p10–p60 | 예: toc itemref; linear 생략 |
| La Page Blanche (Boulet/Bagieu Pénélope, éditions Delcourt, 2012) | [EPNAV](https://github.com/IDPF/epub3-samples/blob/main/30/page-blanche/EPUB/Navigation/nav.xhtml) Sommaire; toc 2 링크 page002/page005; 별도 page-list 8 | [EPOP](https://github.com/IDPF/epub3-samples/blob/main/30/page-blanche/EPUB/package.opf) manifest nav properties=nav; spine toc=ncx; cover/white/page001–008 | 아니오: nav idref 없음; 다른 본문 페이지의 별도 목차 그림은 미검사 |
| SVG in spine (ePub Sample/Takeshi Kanai; 보강) | [ESNAV](https://github.com/IDPF/epub3-samples/blob/main/30/svg-in-spine/OPS/nav.xhtml) 3 links | [ESOP](https://github.com/IDPF/epub3-samples/blob/main/30/svg-in-spine/OPS/content.opf) six SVG itemrefs | 아니오 |

두 필수 출판 예제의 nav/OPF 직접 확인 2/2, 반대 구조 yes/no 관측; 보강 포함 3쌍. 다만 publisher 표시는 OPF metadata에 근거, IDPF repository 배포 외 원출판사의 제출 경로 미확인; 실제 EPUB 리더 화면 0, EPUBCheck 0. XML 구조가 주는 증거만 산입. EPUB nav는 반드시 존재해야 하지만 인쇄 PDF의 outline object와 달리 XHTML 자체가 읽기 순서의 콘텐츠가 될 수도 있고 spine은 navigation hierarchy가 아니다. 따라서 제품의 링크 데이터에서 display_surface와 navigation target/order를 별도 보관하고 format-specific relation을 추가할 것을 제안.

## Q7. 왕복 비용과 반대 요구

| 정책 | 4개 현행 원글에서 설계상 링크 수 | 추가 질문 수 | 잘못된 층 또는 비용 조건 |
|---|---:|---:|---|
| 전부 한 절 즉답 | 4 | 0 | 3건 B 명시로 적합; #4856 A 강한 추정이 틀리면 잘못된 층; 일반 미명시 요청에는 오해 가능 |
| 모두 조건부 A/B | 8 | 0 | 3건에서 불필요한 A 링크; #4856 및 미명시 요청에 안전; 같은 깊이를 중복 링크로 과대 계산 주의 |
| 전부 위치 한 번 묻기 | 답을 받은 경우 4 (첫 턴 0으로 가정) | 4 | 3건에 명시된 정보를 반복 요구; #4856 답 오기 전 실제 해결 미제공; 버전/engine 오류는 위치 질문만으로 못 풂 |
| 봉인 선택: 3 즉답 + 1 조건부 | 5 | 0 | #4856의 B 부기는 짧게; 첫 링크가 더 구체적인 code 위치로 바뀔 수 있음 |

비용은 '첫 경로 단위 링크'를 셈; 같은 목적지의 추가 근거 URL 수가 아님. 4건 모두 최초 revision 결측, 실제 가설 질문 응답 0이라 **효율 실측 분모 0/4**; 시간·성공률 계산 불가. 원작성자 후속 답변은 위 가설 질문에 대한 실험 답변이 아님. 3/4의 명시는 현행 본문 관측이지 최초 공개 시점 확인 아님.
반대 목적: [X639855](https://tex.stackexchange.com/questions/639855/add-table-of-content-to-pdfs-bookmarks-but-suppress-printing-the-actual-page-w)와 [X529058](https://tex.stackexchange.com/questions/529058/generate-a-table-of-contents-to-have-pdf-outlines-but-dont-show-it)는 **종이 목차 없이 탐색**을 원함. [X194720](https://tex.stackexchange.com/questions/194720/hyperref-in-toc-without-page-number?noredirect=1)은 인쇄 TOC의 introduction 링크를 원하므로 같은 '목차 링크'라도 목표 층 다름(탐색 금지는 미명시). X33696는 section numbering과 bookmark 별개. #4519는 print 정상/outline 실패, #3555는 본문 정상/title 실패. 실제 반대 목적의 독립 사건은 존재하지만 엄격한 '인쇄만, outline 금지' 원요구는 추가 탐색 필요. 합성 반례 bookmarks=false와 tableofcontents는 검증 계획에 넣음.

## 관점·대안·추가 분석

작성자는 문서에 페이지 목록 추가와 변환 옵션/판을 원하고, 인쇄 독자는 목차의 페이지 번호/순서/보이는 텍스트가 핵심이다. 뷰어 사용자는 노드 제목/계층/대상/창 표시 상태가 핵심. 템플릿 유지보수자는 엔진·패키지 로드 순서·판 호환과 기존 workflow 회귀를 먼저 본다. 한 글자라도 title=문서 제목, TOC heading, TOC entry, bookmark Title, metadata title, destination ID가 모두 동일하다고 가정하지 않는다. PDF outline은 문서 내 트리 노드이고 UI의 실제 노출은 viewer 설정이 좌우할 수 있다. EPUB nav는 콘텐츠로도 재사용될 수 있지만 spine의 default reading order와 toc hierarchy는 독립.

추천 데이터 모델 후보: requested_surface={page,outline,both,unknown}, requested_change={presence,heading_label,entry_label,depth,parent,target,viewer_visibility,numbering}, input_format, engine, version, documentclass, template, macro/parse stage, rendered_evidence_type, source_span. first_route는 요청 층→정확 section→engine gate→version constraint→실제 실행 여부. 답변 생성 단계는 명시 필드 재질문 금지, 목적지 같으면 설정값 설명, 다른 목적지에 중요한 불확실성이 있을 때만 1회 질문. 대안으로 '두 링크 즉시'와 '진단 질문 후 하나'를 별도 기록하되 시나리오별 테스트가 필요.

자료 분모: 51 ledger 행 중 성공 41/실패 10, 중복/기존 판본/댓글 11 제외, 포함 고유 원자료 **30**(named 4/4, other 7/4, Pandoc 7/5, PDF 5/4, EPUB 7/4), 포함 lineage ID 20. OPF/XHTML은 서로 다른 원파일이지만 한 EPUB 작품의 같은 lineage이며 EPUB는 규격 1 + 출판 예제 3(작품 단위로 세도 4). 독립 시작 요청 사건: 지명 4 + X7731/X57284/X639855/X529058/X194720/X33696 6 = 10; PR4853은 #4856에 속하고 P449는 #449에 속함. #449의 후발 pkaramol 요청은 별도 1자리(총 11, 본표 분모 밖). 30은 사건 수나 재현 수가 아님. 실패 경로는 source ledger; 시간창을 기록했으며 개별 열람 UTC/발행일 일부 결측 명시. 기준 템플릿 1.19.2.1 gitlink 및 실제 사건판 hyperref 설치판/출력 파일 결측으로 자체 상태 PARTIAL. 독립 검토 및 반복 계측 미실시.

| 중요한 불일치 또는 약점 | 영향을 받는 판단 | 다음에 볼 구체적 원자료·검사 | 판정이 바뀌는 관측 |
|---|---|---|---|
| 최초 revision 0/4; #4856 PR 본문 동시 노출; 동일인 실질 후속 2/4 | 봉인 경로의 적중/질문 효율·유지 수 | 4 issue edit history; original author reply/artifact IDs, #449 retest, #4856 post-issue output | 최초 revision의 목표가 다르거나 동일인이 첫 층과 반대 목적 명시; 실제 응답 확보 시 효율 분모 변경 |
| #4519 원판 1.19.2.1 gitlink/TeX 패키지 판 미복원; #449 run count 및 #3555 stringify는 버전 제한 | template/engine/hierarchy/문자열 인과 | git ls-tree 1.19.2.1 data/templates, exact submodule default.latex; original TeX logs; fixtures A–D in HANDOFF | 로드 순서 또는 2회 실행 변경 후에도 outline 불변, 혹은 당시 template 달라짐; Pandoc AST 대체 보존되면 writer 진단 수정 |
| 지명 PDF 0건 직접 검사; #7731 screenshot 실패; EPUB 두 예제 UI 및 publisher 제출 경로 미검증 | 출력 3층 분리, 엔진 일반화 및 사례 provenance | original public PDF/PNG, pdftotext/mutool outline and destination checks; epubcheck and reader screenshots; original publisher release metadata | 출력 TOC와 outline 동시 변경/실제 target 불일치, epub nav 표시/순서가 예상과 다름; provenance 수정 |
