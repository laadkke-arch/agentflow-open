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
