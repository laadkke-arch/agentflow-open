# AF-RES-243 HANDOFF

상태: **PARTIAL** (자료·설계·커밋 완료, 역사 원판 및 실제 산출물/효율 검증 결측).
고정 결과 SHA: **5f4cc61469f2a7f39d773fe7e1fe0381f39ecb88** (이 HANDOFF 이전 commit).
통합 착수 기준 d1353701530ffd4c68587276c15d988d2cc92972. 계획판 7369707441e2eb70e84004ca6cb3bfeefc8b4061; 최신 진행표에서 배정/의존 일치, 전체 계획판 diff는 미검사. 의존 AF-RES-230: 중앙 DONE, 자체 PARTIAL, result 896b13e51f18738e60d63977e999c0aa25027057. 요청에서 제외한 238–242의 자료/정답 사용 안 함.

## 결과와 커밋
- [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/5f4cc61469f2a7f39d773fe7e1fe0381f39ecb88/docs/workstreams/research/AF-RES-243/RESULT.md): 필수 표 두 개, Q1–7, 비용, 약점 3개.
- [first-pass.csv](https://github.com/laadkke-arch/agentflow-open/blob/95d6946fc000f32312b92015dfd4dd506c7074e8/docs/workstreams/research/AF-RES-243/first-pass.csv): 댓글/PR 열람 이전 봉인, 최초판 미확인 및 #4856 PR 존재 선노출 표기.
- [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/5f4cc61469f2a7f39d773fe7e1fe0381f39ecb88/docs/workstreams/research/AF-RES-243/sources.jsonl): 51행, 성공41·실패10, 30개 고유 포함 원자료, 20 lineage ID. bucket named4/other7/Pandoc7/PDF5/EPUB7. 사건 시작 10, 별도 후발 요청 1. 자료/작품/사건/실험 구별.
- [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/5f4cc61469f2a7f39d773fe7e1fe0381f39ecb88/docs/workstreams/research/AF-RES-243/SELF_CHECK.md), formats.csv, followup.csv, COUNTEREXAMPLES.md, SCOPE.md.
- 단계 ① SCOPE a19452869e226020dbdce15195e04858e2a40d2e → seal 95d6946fc000f32312b92015dfd4dd506c7074e8; ② ledger 2429d3b6760d16d33730f7eb9728b0311d1b418f; ③ formats 9d3fbcc373040602c2ae2646cf439159b8cd3328, followup c3b125df34df7d0b0130e1a4ae0a6868942e476b, RESULT tables 9523326cbd81b8348250ca2c361ef1e81ec58ef3; ④ ledger addendum 607d2a8c9950a3e225bbd93ea190e07039ba70d5, counterexamples c68233c09f833d68fa5118a15434568dc83b6e1a; ⑤ RESULT c341ea66388198653428cf992b0eae41fb4af175, SELF_CHECK 5f4cc61469f2a7f39d773fe7e1fe0381f39ecb88; ⑥ this file standalone commit.
- 실제 고정 SHA 재열람: 8/8 files 성공. first-pass blob f51aef0964ff50018a8d774af7d6327f41322e93 = 봉인 blob 동일. JSONL 51 parse 성공, 포함 work 30/lineage20; Q1..Q7 성공 원장 행 수 5,14,20,17,16,8,15(중복 Q 허용). 필수 표1 4행×5열, 표2 3행×5열, 마지막 표 3행×4열; first-pass 4행×12열, formats 17행×8열, followup 17행×9열(헤더 제외). URL/ID·원행 수동 대조, 모든 외부 링크 재열람/영속성 시험은 아님. compare integration→result ahead10 behind0, changed8/8 owned_path; dot-control 미변경. 독립 검토 0, 바이너리 시험 0, 로컬 workbench/CI 실행 0.

## 결론 및 미달
4/4 현행 원글 선판독: 3 즉답 B, 1 조건부 A-first/B, 질문 우선 0. 동일인 실질 후속2/4(3555,4519) 경로 유지, 반전0, 미확인2(449 감사만; 4856 PR 생성은 이슈 전, 이후 same-author 댓글 없음). 최초 body revision 0/4, 실제 질문 답0, 효율 eligible0. #449 run-count change, #3555 writer stringify, #4519 package order, #4856 contentsname support는 서로 다른 수정 위치. shared tocdepth/override는 H18 근거; EPUB 2 필수+1 보강 nav/OPF 실제 원파일 구조 읽음. 실제 EPUB viewer/PDF file 검사 없음. publisher metadata는 읽었으나 publisher 직접 제출 provenance 미확인. #7731 screenshot 실패. strict print-only with no outline의 실제 반대 사례 미확인, navigation-only와 print-layer 목표는 직접 관측. 1.19.2.1 당시 template gitlink 및 설치 hyperref/titlesec 정확 판 미확인; 현재판과 2018-09 비교 자료를 소급하지 않음.

## 재개 첫 행동 및 실행 인계 (모두 미실행)
먼저 정확 1.19.2.1 template gitlink를 복원한다. 원판의 .gitmodules G119에서 path 확인. 기존 승인 환경에 이미 사용 가능한 git/도구만 사용하고, 새 설치·유료 실행은 별도 승인 전 하지 않는다. 작업자가 자기 허용 경로에서 검증하고 원봉인 파일을 수정하지 말 것.

~~~sh
git clone https://github.com/jgm/pandoc.git /tmp/af243-pandoc
cd /tmp/af243-pandoc
git ls-tree 1.19.2.1 data/templates
git show 1.19.2.1:.gitmodules
git clone https://github.com/jgm/pandoc-templates.git /tmp/af243-templates
# 위 ls-tree의 160000 gitlink SHA를 실제 읽은 값으로 치환
git -C /tmp/af243-templates show <actual-gitlink-sha>:default.latex
git show 29c8f1554b412a46bee83e224b72e5931f172cb9
git show 2.1.3:data/templates/default.latex
git show 2.2.3.2:data/templates/default.latex
git show 2.3:data/templates/default.latex
~~~
1.19.2.1 tag에 연결된 gitlink를 얻지 못하면 추정 template로 실행하지 말고 원판 결측 유지. 2012 #449 설치판은 원작성자 글에 없음; commit 전후 비교 build의 exact SHA와 dependency lock, 실제 --version을 기록. #3555 판 미명시, 1.19.2.1 비교는 원사건 확정 아님. TeX Live 역사 이미지/패키지 버전이 확보돼야 역사 재현이라고 표시. 현행 환경 결과는 별도 레이블.

공통 fixture A (독립 제어/계층), 실제 #4519 body의 headings를 재사용한 최소 입력:
~~~markdown
# one

## one.two

# two

## two.one
~~~
작업 디렉터리마다 별도 깨끗한 aux/output 사용. 아래 명령의 실행은 이 웹 작업에서 미실시.
~~~sh
pandoc --version
pdflatex --version
pandoc -D latex > default.latex
kpsewhich hyperref.sty
kpsewhich titlesec.sty
kpsewhich bookmark.sty
pandoc -s -t latex fixture.md -o no-toc.tex
pandoc -s -t latex --toc --toc-depth=1 fixture.md -o print-depth1.tex
# 각 조합을 별도 fresh dir에서 실행. 아래 예시는 한 조합.
pdflatex -interaction=nonstopmode -halt-on-error no-toc.tex
# pass 1의 PDF, .log, .out, .aux 저장 후 같은 작업폴더에서 반복
pdflatex -interaction=nonstopmode -halt-on-error no-toc.tex
pdftotext -layout no-toc.pdf no-toc.pages.txt
mutool show no-toc.pdf outline > no-toc.outline.txt
mutool show no-toc.pdf trailer/Root/Outlines > no-toc.outline-root.txt
pdfinfo no-toc.pdf
sha256sum no-toc.tex no-toc.pdf
~~~
TeX 소스 앞부분에 \listfiles를 추가해 실제 class/package 파일판 로그 확보. stdout/stderr/exit code와 각 pass 후 PDF 해시, .toc/.out/.aux, PDF outline node title/parent/dest 및 페이지 텍스트·링크 annotations를 원영수증 단위로 보존. mutool syntax는 설치 버전 help로 확인; 출력과 view UI screenshot 별도. 파일 경로/판/해시 및 명령행 포함.

- A1: 기본 template no-toc vs toc. 2/3회 반복 후 page list 없어도 heading outline 기대, toc variant는 printed heading/entries 기대. #449 역사 pre/post P449 code 경로에서 pass 1/2 결과 비교; bookmark package나 기타 엔진의 pass 수는 별도로 통제. Outline 존재해도 viewer 숨김이면 viewer-only 상태로 구분.
- A2: print-depth1.tex에 hyperref 로드 이후 \hypersetup{bookmarksdepth=2} (article class 기준 level 확인). 예상 인쇄 2 section entries, outline 4 nodes; override 없이 tocdepth=1 variant는 outline 2 예상. 차이 없으면 package/class/section level 조사; book에서는 chapter offset W119에 따라 값 다를 수 있다. 별도 A3: 기본 template에서 hyperref 로드 이전 \PassOptionsToPackage{bookmarks=false}{hyperref} 넣고 --toc, printed entries 유지/outline 부재 기대; 실행 전용 임시 template 사용. 엄격한 print-only 합성 통제(실제 사용자 증거 아님).
- B (#3555): 네 개 파일을 동일 설치판에서 비교. B1 Markdown 줄 '## The equation \texorpdfstring{$E=mc^2$}{E=mc2}', B2 raw TeX '\section{The equation \texorpdfstring{$E=mc^2$}{E=mc2}}', B3 '## Equation $E=mc^2$', B4 '## Testing \texorpdfstring{\LaTeX}{LaTeX} logo in header' (plain \LaTeX 로고 variant도 저장). 
~~~sh
pandoc -f markdown -t native B1.md > B1.ast.txt
pandoc -f markdown -s -t latex --toc B1.md -o B1.tex
~~~
B2–B4도 같은 명령; 각 3회 pdflatex 실행 및 페이지/TOC 항목/outline title/dest 추출. B1 대체 텍스트 소실과 B2 보존, B3 math 대체, B4 logo 소실은 원작성자 보고에 따른 기대. AST에 raw 대체 텍스트가 plain branch에 남거나 결과 다르면 writer/stringify 진단 수정. \texorpdfstring이 raw TeX 수준에서 동작해도 Markdown 수준에서 보장하지 않음.
- C (#4519): 원 fixture에 YAML toc: true, subparagraph: true, header-includes: ['\usepackage{titlesec}'] (정확 YAML escaping 확인). Pandoc 1.19.2.1 실제 binary와 2.1.3 (원작성자 후속) 별도. C1 default; C2 titlesec 삭제; C3 titlesec before hyperref (generated TeX/custom template에서 순서만 이동); C4 titlesec 뒤에 \usepackage{bookmark} 추가; C5 마지막 ## two.one 삭제. 각 repeated passes + \listfiles 기록. 기대 정상 두 sibling branches(one→one.two; two→two.one); C1 report처럼 all nested 가능, C3/4는 해결 보고, C5도 정상 보고. C1부터 정상인 경우 historical package/version 차이로 분류. 인쇄 목차 정상과 실제 bookmark target 위치/부모를 모두 검증.
- D (#4856): tag 2.2.3.2와 2.3 비교; fixture A를 사용하고 `pandoc -s -t latex --toc -M toc-title="Custom contents" fixture.md -o D.tex` 실행, generated source diff와 3회 PDF. 예상 old no contentsname override, new override and visible Custom contents. outline Title 자동 변경은 보장 안 됨. 2.3 custom template에서 해당 conditional 삭제 대조. 문서 제목/목차 제목/목차 항목/outline Title 각각 기록. class가 TOC 자체를 bookmark로 올리는 경우 별도 분리.
- E (#7731): public body의 md '# Introduction' / '## The City'\''s Context in My Life' 와 본문을 그대로 사용. Pandoc 2.9.2.1 Debian11.1/pdfroff 설치판 확인; `pandoc --pdf-engine pdfroff defect.md -o defect.pdf`와 --toc 추가 통제, `pandoc -t ms defect.md -o defect.ms` 저장. 실제 화면 attachment 재획득하면 layer 식별. apostrophe [cq]가 page or outline 중 어디 있는지 별도 확인. 새 판 결과로 과거 판을 고쳤다고 결론 내리지 말 것.
- F EPUB: IDPF epub3-samples의 위 3쌍을 원장 blob SHA와 비교. package manifest의 properties=nav href resolve, spine idrefs order/linear, nav toc href 및 page-list를 XML parser로 추출; epubcheck <actual-epub> (기존 승인 환경에 있을 때), reader screenshot과 nav toggle/읽기 순서 테스트. CC nav spine yes/6 toc links, Page Blanche nav spine no/2 toc links+8 page-list, SVG nav spine no/3 toc links 기대. OPF/XHTML static과 actual reader 결과를 구분; 다른 본문 페이지에 TOC 표시 있는지도 조사. 출판사 original publication/release metadata의 provenance 확인.
- 원글 이력 및 실제 후속: 4 issue edit history 원본 revision 확인, #449 retest artifact/동일인, #4856 issue 이후 동일인 검증/출력. #3555 logo 해결 여부, #4519 exact logs/actual PDF. 실제 질문 답은 없으므로 새로운 현장 관측 없이는 효율 수치 금지.

## 색인 제안
AF-RES-243: printed TOC vs PDF outline vs heading/entry/PDF-string, shared depth and separate override, engine/version/template gates; first-pass 4 current bodies, 3 direct/1 conditional, substantive original-author followups2, 30 distinct source objects /20 lineages; EPUB 2 opposing nav/spine structures; PARTIAL (original revisions/output/historical exact template). 운영자만 중앙 색인/진행표 갱신. 이 작업에서는 dot-control 수정 안 함.
