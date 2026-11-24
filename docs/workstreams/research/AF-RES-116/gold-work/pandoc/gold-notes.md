# AF-RES-116 Pandoc 독립 기준 판독

## 판독 범위와 결론

이 기준은 P1–P3의 요청과 원문, 고정 공식 문서, 공식 구현 및 원 저작자의 공개 반례를 읽어 만들었다. 꾸러미, B/C 문구, 제작 기록, 수신 판독, 실험 답, 다른 gold 작성물은 읽지 않았다. 처음 `cases.json`을 표시할 때 전체 객체가 출력되어 I1–I3의 요청문도 보였다는 우발 노출은 `gold.json`에 기록했다. 그 내용은 Pandoc 근거 선정이나 판단에 사용하지 않았다.

세 사건의 기준 결론은 다음과 같다.

| 사건 | 조작 O | 보존 P | 기준 판단 |
| --- | --- | --- | --- |
| P1 / 2.19.2 | self-contained HTML과 TOC 생성 | 같은 native fenced Div 안의 동급 B1/B2를 모두 TOC에 유지 | 원 입력을 기본 writer에 그대로 주면 충족하지 않는다. 구조를 판별하는 구현이 결정적이며 일반 TOC 깊이·Div 문법 설명만으로 해결을 보장할 수 없다. |
| P2 / 판 미상 → 연구 고정 3.8.3 | 설명·주석을 가진 단일 원본을 약어 파일로 직접 읽음 | 원본 self-documentation과 기존 고유 약어 key 집합의 인식 | stock loader에는 첫 공백/탭 이후 무시나 YAML key 추출이 없다. 문서 계약에 근거한 제한된 부정과 실제 행 처리 구현을 확인한 부정을 구별한다. |
| P3 / 2.14.0.3 | 표·그림·복수 문단을 페이지로 렌더링 | 표와 실제 다음 페이지 float를 유지한 채 하단 여백 보존 | exact command/engine/template/TeX package 판이 빠져 있으므로 성공 보장은 보류한다. 첨부와 후속으로 PDF/Quarto 및 LaTeX longtable 조사 경로는 확인되지만 해결 실행값은 없다. |

이 작업자는 Pandoc나 TeX를 실행하지 않았다. 웹 수신, JSON 추출, 해시 확인, 문서 offset 산출은 연구 도구 실행이다. 저장된 upstream test의 기대 출력을 읽은 것도 독립 실행이 아니다. 비교용 longtable 4.16 source는 2021년 고정 판이며 원 사용자의 실제 설치판을 알아냈다는 뜻이 아니다.

## 고정 판과 실제 읽기

| 사건 | 공식 source commit | 고정 manual |
| --- | --- | --- |
| P1 | `53325aa2e37a976e5a20d8fc2a662070a04e90a9` | [Pandoc 2.19.2 MANUAL.txt](https://raw.githubusercontent.com/jgm/pandoc/53325aa2e37a976e5a20d8fc2a662070a04e90a9/MANUAL.txt) |
| P2 | `568dab14533940ecee16824097400f1eabf13869` | [Pandoc 3.8.3 MANUAL.txt](https://raw.githubusercontent.com/jgm/pandoc/568dab14533940ecee16824097400f1eabf13869/MANUAL.txt) |
| P3 | `227f675cc46a680d4b8f2fd71e0c4cbb92a3fd0b` | [Pandoc 2.14.0.3 MANUAL.txt](https://raw.githubusercontent.com/jgm/pandoc/227f675cc46a680d4b8f2fd71e0c4cbb92a3fd0b/MANUAL.txt) |

허용 corpus는 이 MANUAL.txt들을 설치된 Pandoc 3.1.11.1로 HTML 변환한 뒤 평문으로 만든 것이다. 고정 역사판의 브라우저 화면이나 역사 바이너리 실행 결과로 부르지 않는다. `source_sha`는 corpus의 렌더된 HTML 해시이고, 원 MANUAL.txt의 해시는 각각 기존 `MANUAL.txt.receipt.json`에 있다. `gold.json`은 corpus gzip 바이트의 SHA-256도 보존한다.

실제 본문 표시는 `read-log.jsonl`에 UTC, source, 표시 구간, 표시 문자열 해시로 기록했고 `excerpts/`에 같은 문자열을 남겼다. 초기에 큰 anchor/search 묶음이 도구 출력에서 일부 잘렸다. 그 묶음 전체를 읽었다고 세지 않았으며 모든 결정적 구간은 짧은 범위로 다시 표시한 후 사용했다. 원 최초 body 해시는 2026-11-24 04:31:58 UTC 재표시에서 다시 확인했다. P3 두 원 이미지와 P1 출력 screenshot은 04:31:59–04:32:00 UTC 실제 이미지로 표시했다. 단순 수신이나 byte hash만으로 pixel을 읽었다고 간주하지 않았다.

## P1: grouped headings와 TOC

### 정확한 동작과 예외

[원 이슈 #8518](https://github.com/jgm/pandoc/issues/8518)의 A1/A2는 각각의 Div 안에 있고, B1/B2는 하나의 Div 안에 동급 `##` heading으로 있다. 원 screenshot에서도 B1/B2가 본문에는 있으나 TOC에는 없는 것을 볼 수 있다. 이는 작성자의 보고된 출력이다.

고정 [HTML writer](https://github.com/jgm/pandoc/blob/53325aa2e37a976e5a20d8fc2a662070a04e90a9/src/Text/Pandoc/Writers/HTML.hs)의 283–291행은 문서를 `makeSections`로 변환하고 TOC를 만든 뒤 본문을 출력한다. 510–524행은 shared `toTableOfContents`를 호출한다. 고정 [Shared.hs](https://github.com/jgm/pandoc/blob/53325aa2e37a976e5a20d8fc2a662070a04e90a9/src/Text/Pandoc/Shared.hs)의 574–592행과 [Writers/Shared.hs](https://github.com/jgm/pandoc/blob/53325aa2e37a976e5a20d8fc2a662070a04e90a9/src/Text/Pandoc/Writers/Shared.hs)의 429–456행을 함께 읽어야 원 입력이 왜 빠지는지 설명할 수 있다.

Div가 첫 block으로 Header를 가질 때, 뒤의 **직접 Header**들은 첫 Header보다 더 깊은 수준이어야 section-like Div와 합쳐질 수 있다. `column`, `columns`, `fragment` class도 제외한다. outer Div와 inner section의 ID가 둘 다 존재하면서 서로 다르면 합치지 않는다. 일반 Div 내부에 section들을 만들어도 TOC 순회가 임의 Div 안으로 무조건 들어가는 것은 아니다. `sectionToListItem`은 직접 첫 child가 Header인 Div에 대해서만 항목 및 하위 항목을 만든다.

따라서 같은 수준의 B1/B2는 원 그룹 안에서 각각 section으로 만들어져도 외곽 Div에 가려진다. A1/A2의 경우 외곽 class Div와 각 단일 section을 합칠 수 있다. 이 차이는 TOC 기본 depth 3으로 설명되지 않는다. B1/B2는 이미 level 2다. `--section-divs`는 출력 포장과 ID의 위치를 바꾸는 옵션이며 이 구조 판정의 전환 switch로 문서화되어 있지 않다.

[jgm의 2023-01-04 설명](https://github.com/jgm/pandoc/issues/8518#issuecomment-1370446360)은 고립된 callout 같은 사용을 위해 Div 내부 heading을 원래 배제했고 round-trip에 필요한 section-like 예외를 넣었다는 설계 배경이다. 설명을 요약하면서 “다른 제목이 하나라도 있으면 불가”로 확대하면 실제 구현보다 강한 주장이 된다.

### 초기 가설을 바꾼 반례

처음 검토할 수 있는 단순 가설은 “복수 제목을 가진 fenced Div는 전부 TOC에서 제외된다”였다. 고정 [공식 `toc.md`](https://github.com/jgm/pandoc/blob/53325aa2e37a976e5a20d8fc2a662070a04e90a9/test/command/toc.md)는 이를 반박한다. 한 Div 안의 `# C`, `## cc`, `# D`는 TOC에 없지만 다른 Div 안의 `# E`, `## e`는 포함된다. 이 테스트의 출력 형식은 Markdown이므로 HTML 실행 증거로 바꾸지 않았다. 두 writer가 쓰는 shared section/TOC 구현을 확인하는 상호 근거로 사용했다.

“heading으로 시작하기만 하면 충분하다”는 다음 단순 가설도 [#8741](https://github.com/jgm/pandoc/issues/8741)과 [maintainer의 ID 보존 설명](https://github.com/jgm/pandoc/issues/8741#issuecomment-2067736991)에 의해 제한된다. 이 독립 보고는 Pandoc 3.1.2의 EPUB/file-scope 사례다. 서로 다른 outer Div ID와 inner Header ID가 section 처리에 간섭하며, 어느 anchor도 무조건 버리면 안 되는 이유가 드러난다. 이 후속 버전·다른 출력 형식의 회귀를 P1 2.19.2 HTML의 직접 실행 결과로 취급하지 않는다. 같은 ID 병합 조건은 P1 고정 구현에서 따로 확인했다.

### 가능한 대안의 경계

[2024-12-10 maintainer 댓글](https://github.com/jgm/pandoc/issues/8518#issuecomment-2532368401)은 명시적 raw HTML opening/closing block을 대안으로 제시한다. 이 방식이나 Div를 적절한 raw wrapper로 바꾸는 필터는 **방출 HTML의 grouping**을 유지하는 후보다. 원래 native Div AST를 그대로 두는 것과는 다르다. plain `<div>`를 그냥 넣으면 `native_divs`가 다시 native Div로 읽을 수 있으므로 `{=html}` raw block과 구별해야 한다. `--section-divs`를 추가하거나 복잡한 속성과 ID를 갖는 경우 최종 HTML nesting도 확인해야 한다.

해당 댓글의 사용자는 3.1.11.1을 보고했다. 2.19.2 manual의 raw syntax가 이 대안의 기본 구성요소를 뒷받침하지만, 이 작업에서 2.19.2의 대안 실행을 검증한 것은 아니다. 원 conditional Lua filter도 제공되지 않았다.

### 허용 corpus에서의 판정

`--toc`, `--self-contained`, depth, fenced Div syntax까지 읽었다면 O와 일반 구문은 복원했다. E3의 section 수집 조건은 corpus 밖의 구현이다. 그 상태에서 B1/B2 보존을 확정하면 근거가 부족하다. 원 보고가 있다는 사실과 보고된 동작의 결정적 문서 근거를 읽은 것은 별도다. `corpus-minimum-intervals.json`은 기능 정의 구간과 결정적 P 근거의 부재를 따로 표시한다.

## P2: 한 파일의 설명과 약어 집합

### 정확한 판과 의미

[원 이슈 #8522](https://github.com/jgm/pandoc/issues/8522)는 당시 판을 밝히지 않았다. 여기의 3.8.3은 2025-12-31 기준 최신 안정판을 택한 연구 규칙상의 판이며, 원 작성자의 실행판이라고 할 수 없다. 원본의 comment/expansion을 문서 본문에 출력하라는 요청도 아니다. 이미 사용하던 생성기의 unique keys 결과와 같은 약어 집합을 직접 읽으려는 것이다.

3.8.3 `--abbreviations=FILE` 문단은 한 행 한 약어, 공백 없는 문자열, Markdown reader에서의 용도, 기본 파일 lookup을 설명한다. 고정 [App.hs](https://github.com/jgm/pandoc/blob/568dab14533940ecee16824097400f1eabf13869/src/Text/Pandoc/App.hs) 368–376행은 실제로 지정 파일 또는 기본 data file 하나를 읽고, `T.lines`의 비어 있지 않은 문자열들을 `Set.fromList`에 넣는다. 첫 공백/탭에서 자르거나 YAML의 key를 추출하거나 `#` 이후를 버리는 분기는 없다. 완전히 같은 행의 dedup은 되지만 서로 다른 expansion이 붙은 동일 bare key를 합치는 연산이 아니다.

고정 [Markdown reader](https://github.com/jgm/pandoc/blob/568dab14533940ecee16824097400f1eabf13869/src/Text/Pandoc/Readers/Markdown.hs) 1765–1787행은 alphaNum과 단일 period를 모은 token을 Set에 정확히 비교한다. `abbr. : expansion`이라는 전체 행이나 탭 뒤 설명이 붙은 행은 bare `abbr.` token과 일치하지 않는다. 이 경로는 `smart`가 활성화되어야 약어 다음의 일반 space를 NBSP로 바꾸며, citation/note와 다른 whitespace 형태를 구별한다.

`Extension: abbreviations`는 다른 기능이다. 동일 reader 421–433행과 manual은 PHP Markdown Extra식 `*[HTML]: ...` 키를 문서에서 건너뛴다고 설명한다. 이 extension을 켰다는 이유로 약어 파일의 YAML이나 comment 문법이 지원되는 것은 아니다.

### 반례와 정확한 제한

초기에는 원 문제의 `abbr.` 형태만 보고 period를 필수조건으로 잡을 수 있다. [#7124](https://github.com/jgm/pandoc/issues/7124)와 [2021-03-05 maintainer 댓글](https://github.com/jgm/pandoc/issues/7124#issuecomment-791106646)은 period 필요조건을 완화했지만 space를 포함한 약어는 허용하지 않았다고 기록한다. 고정 3.8.3 parser에도 마지막 period guard가 없다. 따라서 “모든 약어는 마침표로 끝나야 한다”는 기준을 두면 틀린다. 반대로 여러 단어를 한 약어 entry로 넣는 것이 자동 지원된다는 주장도 틀린다.

고정 [md-abbrevs.md](https://github.com/jgm/pandoc/blob/568dab14533940ecee16824097400f1eabf13869/test/command/md-abbrevs.md)는 `Mr. Bob` 뒤 NBSP와 escaped period로 그 효과를 피하는 대조를 기록한다. 이것을 실제 실행한 것은 아니다. [#8520](https://github.com/jgm/pandoc/issues/8520)의 directory/lang lookup 제안은 읽었지만 행 syntax의 현 지원을 증명하지 않아 별도 할당에 넣지 않았다.

원 YAML과 약어 전체 목록이 없기 때문에 임의 YAML을 첫 공백에서 자르기만 하면 모든 key를 정확히 얻는다고 제안할 수 없다. quoted keys, multiline 값, 들여쓰기, 중복 key 정책, 전체 필요한 집합은 확인되지 않았다. source를 유지하면서 기존 생성기를 실행마다 호출해 임시 목록을 공급하는 방식은 관리상 후보일 수 있지만 stock Pandoc의 직접 YAML 지원으로 부르면 안 된다.

### corpus와 완전 판정의 차이

매뉴얼에서 한 행 한 약어와 공백 금지를 읽으면, 제시된 enriched line이 문서화된 계약을 벗어난다는 제한적 부정이나 정당한 보류가 가능하다. 실제 tab stripping 동작, YAML parsing 부재, 중복 처리의 정확한 의미까지 읽었다고 말하려면 구현 근거가 필요하다. manual의 `spaces`만을 읽고 첫 탭 뒤 처리까지 직접 확인했다고 주장하지 않는다. 이 구별은 문서계약에 맞지 않는 입력을 사용하지 말라는 조언과 loader의 정확한 메커니즘을 설명하는 답을 모두 공정하게 평가하기 위한 것이다.

## P3: 하단 여백과 float/table 조합

### 원문·첨부·후속의 층 구분

[원 이슈 #8526](https://github.com/jgm/pandoc/issues/8526)의 현재 최초 body에는 출력 형식·엔진·명령이 없다. 그 상태에서 PDF/LaTeX라고 확정하지 않는 것이 옳다. 이 작업에서 봉인 후 직접 연 [원 Markdown 첨부](https://github.com/jgm/pandoc/files/10353204/layoutissue.md)는 PDF 렌더 지시와 Quarto 언급, `format: html/pdf/docx` YAML을 포함한다. 그 원 첨부는 PDF 의도를 새로 뒷받침하지만 정확한 실행 command나 engine 선택을 복원하지 못한다.

[2023-01-05 maintainer 댓글](https://github.com/jgm/pandoc/issues/8526#issuecomment-1372561431)은 longtable 문제를 의심한다고 했으며, 확정 원인이나 범용 수정을 선언하지 않았다. [2023-01-07 후속 첨부](https://github.com/jgm/pandoc/files/10366881/layoutissue.txt)는 `article`, `graphicx`, `longtable`의 TeX 입력이다. `figure` 다음에 짧은 `longtable`과 많은 문단을 배치한다. 이 역시 같은 자연 이슈 계보이다. 입력 graphic의 두 업로드는 동일 SHA-256를 갖는 같은 바이트였다.

### 고정 구현이 말하는 부분

2.14.0.3 [LaTeX/Table.hs](https://github.com/jgm/pandoc/blob/227f675cc46a680d4b8f2fd71e0c4cbb92a3fd0b/src/Text/Pandoc/Writers/LaTeX/Table.hs) 45–77행은 표를 `longtable`로 내보낸다. [LaTeX.hs](https://github.com/jgm/pandoc/blob/227f675cc46a680d4b8f2fd71e0c4cbb92a3fd0b/src/Text/Pandoc/Writers/LaTeX.hs) 386–403행은 captioned standalone image를 `figure`로 출력하며 minipage/note 안에서는 다른 처리를 한다. [default.latex](https://github.com/jgm/pandoc/blob/227f675cc46a680d4b8f2fd71e0c4cbb92a3fd0b/data/templates/default.latex) 304–340행은 longtable package와 기본 figure placement `htbp`를 설정한다. 이를 통해 조건부 LaTeX 경로를 설명할 수 있지만 특정 페이지에서 margin이 보존됨을 증명할 수는 없다.

비교용으로 고정한 [longtable 4.16 / 2021-05-07 source](https://github.com/latex3/latex2e/blob/7fe2b014582d9a5a6cef8f00ad01a947aa012b4f/required/tools/longtable.dtx)는 다중 페이지 표를 정의하며 표 행 내부가 아닌 행 사이에서 page break한다고 설명한다(174–184, 270–274행). 다중 column 제한(582–583, 1025–1038행), float와 pagegoal/colroom 관련 v4.14 변경(1308–1347, 1413–1437, 2041–2113행)도 직접 읽었다. 원 사용자의 설치판이 4.16이었다는 근거는 없다.

### 범용 수정이라는 가설을 반박하는 독립 반례

[LaTeX #158](https://github.com/latex3/latex2e/issues/158)은 두 figure와 짧은 longtable을 사용하는 독립 최소 입력을 제공한다. [maintainer의 설명](https://github.com/latex3/latex2e/issues/158#issuecomment-528012636)은 첫 figure에 `htbp`를 넣었을 때 해당 대조의 overflow가 사라지는 이유가 실제로 `h`에 배치되어 float에 의한 `colroom` 변화가 없기 때문이라고 한다. 이 성공은 “그림이 다음 페이지로 떠도 보존된다”는 조건을 통과한 성공이 아니다. Pandoc default template에 `htbp`가 이미 있다는 것도 확인했으므로 그 값만 추가하면 항상 해결된다고 제안할 수 없다.

[2021-09-01 maintainer 댓글](https://github.com/latex3/latex2e/issues/158#issuecomment-910883918)은 v4.14 계열 수정으로 일부 float 상호작용이 고쳐졌으나 이 test는 여전히 실패한다고 기록한다. [관련 #137의 2024-10-31 댓글](https://github.com/latex3/latex2e/issues/137#issuecomment-2449450361)은 original MWE가 당시 TeX Live 2024에서 더 이상 spill하지 않는다고 보고한다. 둘을 함께 읽으면 “과거 longtable bug 수정 = 모든 float/table 조합 또는 P3 해결”이라는 가설이 성립하지 않는다. #137/#158/tools3512는 하나의 관련 계보로 묶어 한 회귀 할당만 했다.

표를 regular `table`로 바꾸자는 대안에는 다중 페이지 표가 깨지는 문제가 붙는다. [P3 maintainer 댓글](https://github.com/jgm/pandoc/issues/8526#issuecomment-1374557600), longtable 문서 및 [#1023](https://github.com/jgm/pandoc/issues/1023)의 two-column 반례를 읽었다. #1023의 현재 closed metadata와 검색에 나타난 2026년 새 기능은 2.14.0.3 지원 근거로 쓰지 않았다. [PR #4392](https://github.com/jgm/pandoc/pull/4392)도 제안 본문이지 고정판 기능 증거가 아니다.

### 무엇을 보류하며 무엇을 다음에 확인할 것인가

매뉴얼의 PDF engine 표, `implicit_figures`, pipe table syntax, geometry 옵션은 O와 일부 구성 조건을 제공한다. `implicit_figures`는 figure/caption을 만드는 구문이고 page float 위치와 longtable 뒤 본문의 안전을 보장하지 않는다. geometry가 margin 변수를 덮어쓴다는 규칙도 구성 규칙이다. 여백을 크게 해서 문제를 일으키는 배치를 피하는 것은 원 preservation 조건을 만족한 증거가 아니다. `Variables for wkhtmltopdf`를 읽은 결과를 LaTeX/longtable 증거로 사용해서도 안 된다.

필요한 최소 추가 정보는 실제 렌더 명령, output/engine, Quarto 판, TeX 배포판·longtable 판, template, 생성 .tex 및 log다. 동일 환경에서 원 표+그림 입력, 그림이 같은 페이지에 남는 대조, 표 제거 대조, 표를 다른 그림으로 치환한 대조를 비교해야 한다. 성공 기준에는 원 표 유지와 실제 다음 페이지 float를 명시해야 한다. 이 작업에서는 이를 실행하지 않았으므로 P3 exact 보존 성공/실패와 특정 수정의 성공은 unknown으로 남는다.

## 근거 구간과 판정 사용법

`gold.json`에는 사건별 O/P, 조건부 기대 답, essential/조건부 예외, exact corpus 구간, corpus 밖 최소 구현 위치, 정당한 보류, source exhaustiveness와 known gaps가 있다. `corpus-minimum-intervals.json`의 19구간은 Unicode code point 기준 `[start,end)`다. 각 구간은 실제 corpus substring과 일치하도록 확인했다.

`target-spans.json`은 C를 보지 않은 reference 판단으로 고정하는 **관련 기능 절의 실제 본문 도달 표적**을 담는다. 해당 절의 label만으로 도착했다고 세지 않도록 option/heading과 최소 첫 문장을 포함한다. 결정적 answer source가 밖이면 별도 `exact_answer_target: outside`로 두었다. 가까운 fenced syntax, figure 구문, 이름이 같은 abbreviation extension은 결정적 답 절과 합치지 않는다.

3개봉 graph의 완전 열거와 실제 수신 답 채점은 parent 역할이다. 이 판독자는 경로를 생성하거나 힌트를 제안하지 않았고, `reachable/unreachable`를 자기 판단으로 할당하지 않았다. 단지 full-supported를 위해 corpus 밖에서 필요한 내용과 corpus만으로 정당하게 보류할 수 있는 내용을 구분했다. 원 소프트웨어에서 불가능한 것과 고정 reader budget에서 근거에 닿지 못하는 것은 다르다.

## 출처 배당 대사

정의/공식 구현 **4개**, 별도 회귀/문서변경/반대 입력 **3개**를 배정했다. 원 자연 요청 3개는 이미 parent가 세므로 새로 더하지 않는다.

| 구분 | 고유 work/lineage | 대표 source |
| --- | --- | --- |
| 정의 1 | Pandoc manual 전체 버전·앵커 | `PD-MANUAL-2192` 및 동일 계보의 383/21403 |
| 정의 2 | section 생성과 TOC 수집 구현 | `PD-TOC-SHARED`, 관련 HTML/Writer Shared 묶음 |
| 정의 3 | abbreviation 파일 ingestion과 Markdown token 소비 | `PD-ABBR-APP`, 관련 Markdown reader 묶음 |
| 정의 4 | LaTeX 표·그림 생성과 default template | `PD-LATEX-TABLE`, 관련 writer/template 묶음 |
| 반례 1 | #8741 Div/Header ID 간섭 | `PD-R8741`과 동일 댓글 계보 |
| 반례 2 | #7124 period 완화와 multiword 제한 | `PD-R7124`와 동일 댓글 계보 |
| 반례 3 | tools/3512, LaTeX #137/#158 float/longtable | `LT-R158`; 관련 댓글·#137·구현을 같은 계보로 묶음 |

관련 test 파일을 각각 새 저작으로 세지 않았고, longtable source를 별도 다섯째 정의로 늘리지 않았다. 추가로 읽은 #782/#1023/#8520/PR4392도 allocation에 넣지 않았다. API tree/commit index, 빈 comment 배열, 같은 그림의 두 업로드는 참고 행만 남겼다. `sources-pandoc.jsonl`의 45행에서 `unique_counted`가 true인 것은 위 일곱 대표 source뿐이다.

각 source 행에는 original/arrived URL, work/lineage, 저자, 판/게시시각, 수신 확인 UTC와 실제 읽기 UTC, 읽은 구간, 확인한 주장, 한계/미확인, Q2/Q5/Q6/Q7, linked case, 배당, primary/status가 있다. 주석·후속 attachment가 original body와 같은 계보인 것도 명시한다.

## 재현·전송·보존 메모

`snapshots/`는 원 public source 수신본과 수신 영수증이다. signed attachment redirect의 query는 저장 영수증에서 제거하고 public attachment transport metadata의 redaction이라고 표시했다. credential로 발행한 것이 아니다. `reproduction-inputs/`에는 P1 원 inline 입력, P3 원 Markdown와 후속 TeX, 원 graphic을 복사했다. P2의 실제 완전 파일은 제공되지 않았으므로 schematic/연구자 구성 입력만 따로 명시한다.

`unexecuted-checks.md` 및 `unexecuted-checks.json`은 필요한 최소 입력/명령과 성공 판단 기준이다. historical binary나 engine의 설치·실행을 수행하지 않았다. `build_gold.py`는 저장된 source/read log에서 JSON 원장과 corpus interval을 다시 만든다. 마지막 검사는 code/자료의 문법·참조·substring·count 검사이며 Pandoc 기능 test가 아니다.

지속적인 행위나 외부 연락, 계정 변경, 설치, 유료 API, git 동작은 수행하지 않았다. 수정은 배정받은 `gold-work/pandoc/` 아래에만 있다.
