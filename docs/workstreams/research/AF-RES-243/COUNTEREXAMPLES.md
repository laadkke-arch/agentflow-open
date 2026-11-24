# 반례와 정정 (봉인 이후)
사전 판정 파일 95d6946fc000f32312b92015dfd4dd506c7074e8는 변경하지 않는다. 여기서 바뀐 것은 **첫 절의 상세화**와 근거의 신뢰도이지 원글에 후속 증거를 소급 주입하는 것이 아니다.

- R1 인쇄 없이 탐색: [X639855](https://tex.stackexchange.com/questions/639855/add-table-of-content-to-pdfs-bookmarks-but-suppress-printing-the-actual-page-w) 및 [X529058](https://tex.stackexchange.com/questions/529058/generate-a-table-of-contents-to-have-pdf-outlines-but-dont-show-it) 원요구는 종이 목차를 원하지 않는다. --toc 일괄 권고는 산출물을 바꿔 버린다. 반대 방향 X194720은 인쇄 TOC의 Intro 링크를 원함(탐색 금지까지는 명시되지 않음). 엄격한 인쇄-only·outline 금지 원요구는 미확인. bookmarks=false인 합성 대조는 실험 예정이지 관측 아님.
- R2 공유 깊이: [H18](https://ftp.math.utah.edu/pub/texlive/Contents/live/texmf-dist/doc/latex/hyperref/manual.html) 2018-09 §5.23 기본 tocdepth, 별도 숫자/이름; §9.1.38 titlesec 비호환 경고. Hcur §7.24/11.1.33과 방향 양립. 1999 HP99도 tocdepth 연결. 서로 다른 층이 반드시 서로 독립 옵션이라는 결론은 틀림. 동일 깊이 요청에는 하나의 toc-depth 안내가 충분할 수 있으나 옵션이 실제 전달되는 template/engine 확인. 반대로 부모 관계가 잘못된 #4519에서 깊이 변경은 결함을 숨길 수 있다.
- R3 #449 초안의 hyperref bookmark 첫 링크는 출력 층으로 옳지만 **당시 수정 위치는 Pandoc PDF 반복 실행 코드** P449. pdflatex 1회/2회 대조 필요. Bpkg 및 H18은 bookmark 패키지 1회 가능성을 제시하여 모든 판에 '두 번 필수'라고 말할 수 없다.
- R4 #3555 hyperref PDF strings만 보더라도 Pandoc이 대체 문자열을 새로 만든다는 W119+SH119 경로를 빠뜨리면 raw TeX 우회가 왜 다른지 설명 못 한다. 순수 LaTeX \texorpdfstring 설명과 Markdown parse/AST/LaTeX writer는 별개. C3555 일반 수식은 수용, 로고는 실패 보고.
- R5 #4519 [유지보수자](https://github.com/jgm/pandoc/issues/4519#issuecomment-377969323)의 custom template 조언은 hyperref 뒤의 header-includes가 titlesec를 늦게 로드하는 조합에 한함. 원작성자는 bookmark 추가로 해결했다고 보고함. template 전체 변경을 일반 처방하지 않음. G119에서 1.19.2.1 submodule 경로 확인; gitlink SHA 미확인, 2.1.3은 원작성자의 별도 재현 버전이므로 구판 템플릿 대체물로 소급 사용 금지.
- R6 #4856 toc-title은 2.2.3.2 비교 템플릿에는 없고 2.3에 들어감. 사용자 custom template가 해당 조건을 구현하지 않으면 최신 옵션 설명만으로는 해결 안 됨. PR의 contentsname 수정이 자동으로 outline Title까지 바꾼다는 보장 없음. 클래스가 TOC를 북마크로 등록할 경우 반례 가능, 미실행.
- R7 [X7731](https://api.github.com/repos/jgm/pandoc/issues/7731) pdfroff, Evince, apostrophe [cq] 보고. --toc 없는 명령과 TOC라는 표현만으로 탐색/종이 판별하지 않음. 스크린샷 Z7731 실패. 따라서 첫 링크로 엔진 선택 절을 줄 수 있으며 LaTeX macro는 해당 없음.
- R8 EPUB [E33](https://www.w3.org/TR/2026/REC-epub-33-20260113/#sec-spine-elem) §5.7.2 명시: 필수 nav가 spine에 있을 필요는 없다. CC nav는 spine에 있고 Page Blanche nav는 없음; SVG extra도 없음. PDF의 페이지/outline을 EPUB의 nav/spine과 동일 구조로 취급하지 말 것. Page Blanche의 다른 content page에 별도 시각 목차가 그려졌는지는 미확인.

원자료 count 수정: 51 ledger rows(45+6), 30 포함 work IDs(29+G119), 20 lineage IDs, named 4, other 7, Pandoc 7, PDF 5, EPUB 7. H18 및 E33S는 직접 읽었으나 기존 work로 중복 산입 안 함. §5.7.2 spine 규정의 원문 위치 추가. 실패 3건 추가. 자료 개수와 인과 재현은 별개.
