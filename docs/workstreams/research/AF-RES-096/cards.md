# AF-RES-096 · 조건부 반환 카드

각 요청의 링크는 최대 두 개다. 사후 링크를 포함한 편집안이며 봉인된 A/B 반환·승패를 변경하지 않는다. '완결'은 고정판의 문서 적합을 뜻하고 원 사용자의 실행 성공과 다르다.

## J1 · 79322478

1. [배열/변수 binding 및 string interpolation 명세](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml)
2. [짧은 join 기반 대안](https://stackoverflow.com/a/79322532)

**질문자에게:** 부모 값과 각 자식의 대응을 같은 filter에서 유지한다. 잘린 입력을 그대로 실행한 성공은 주장하지 않는다.

**유지관리자에게:** 부모 binding을 보존한 채 자식 하나를 현재 입력으로 둔다. 소수점 자릿수 보존은 이번에 새 요구로 추가하지 않았다.

**검색 결과 편집자에게:** 한 매뉴얼이 입력·반복·출력을 모두 설명한다. 두 번째 링크를 쓸 때는 짧은 공개 join 대안임을 표시한다.

**되물을 한 가지:** 잘린 JSON의 닫힘을 포함한 최소 완전 입력을 줄 수 있는가?

**귀속·한계:** 현재 채택 첫답은 배열을 더한 뒤 join. 30일 내 질문자 후속 없음. 원 JSON 조각 exit5, 닫힘만 수리한 입력에서는 봉인 filter 3행 일치. 위 처리 설명과 추천은 연구자의 적용 추론이며, 원문 사실과 사후 실행의 자세한 귀속은 outcomes.csv 및 각 sources 원장에 있다.

## J2 · 79388729

1. [객체 생성 시 input 문맥과 missing key=null 명세](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml)
2. [INDEX 대안과 null offset을 숨기지 않은 구체 출력](https://stackoverflow.com/a/79389173)

**질문자에게:** 두 최상위 필드를 묶는 구조는 제공할 수 있다. 주어진 숫자까지 맞는 완결 예제로 제시하려면 실제 offset 입력이 필요하다.

**유지관리자에게:** 배열 전체를 유지해 title과 tracks를 같은 객체에서 만든다. 없는 offset의 null과 입력 title/artist 대응을 분리해서 확인한다.

**검색 결과 편집자에게:** cat의 전달 계약은 맞지만 누락 입력을 채우지 못한다. 반환 우선순위는 jq의 객체·스코프 설명과 짧은 공개 해법이다.

**되물을 한 가지:** offset 수치와 title/artist 정규화 규칙을 포함한 완전 입력을 줄 수 있는가?

**귀속·한계:** 현재 채택 답에 질문자의 긍정 댓글이 있음. 비채택 INDEX 답의 실제 제시 출력은 offset=null. 원 숫자·title/artist 대응의 완결은 여전히 미확인. 위 처리 설명과 추천은 연구자의 적용 추론이며, 원문 사실과 사후 실행의 자세한 귀속은 outcomes.csv 및 각 sources 원장에 있다.

## J3 · 79389414

1. [공식 range/index/+ 및 while/slice 명세](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml)
2. [짧은 _nwise 대안과 문서화된 while 대안이 함께 있는 고정 수정판](https://stackoverflow.com/revisions/8B5D568A-8370-4DA2-8612-FF08869D3144/view-source)

**질문자에게:** 연속 두 항목을 위치로 묶는다. 실제 JSON envelope와 홀수 개 입력 정책은 원 질문에서 확정되지 않았다.

**유지관리자에게:** 공개 API인 range/인덱싱/더하기로 같은 쌍 묶기를 구성할 수 있다. _nwise는 공개 답이 undocumented라고 명시한다.

**검색 결과 편집자에게:** Overpass 쪽 질의를 바꾸면 'jq만' 조건을 깨뜨릴 수 있다. 생산자 이름 등장 자체를 외부 해법의 필요성으로 읽지 않는다.

**되물을 한 가지:** 실제 객체의 merge 전 변형과 중복 key 충돌 규칙을 보여줄 수 있는가?

**귀속·한계:** 현재 채택 첫답은 undocumented _nwise(2)+add. 질문자는 더 복잡한 실제 사례에도 접근이 작동한다고 후속. 원 Overpass 입력·판은 없음. 위 처리 설명과 추천은 연구자의 적용 추론이며, 원문 사실과 사후 실행의 자세한 귀속은 outcomes.csv 및 각 sources 원장에 있다.

## J4 · 79410149

1. [grep의 -P/-o 지원 조건과 출력 경계](https://git.savannah.gnu.org/cgit/grep.git/tree/doc/grep.in.1?h=v3.11)
2. [재귀 PCRE의 짧은 명령과 별도 시험 입력/출력](https://stackoverflow.com/a/79426171)

**질문자에게:** 한 줄의 literal balanced brackets, 빈 값과 반복 발생을 처리한다. 문자열 안의 ]를 escape/quote 문법으로 해석하는 요구까지 확장하면 봉인 filter는 실패한다.

**유지관리자에게:** 로그는 raw input으로 받아 문자별 대괄호 깊이를 센다. jq regex 기능에는 Oniguruma가 필요하고 grep 대안에는 -P 지원이 필요하다.

**검색 결과 편집자에게:** 짧은 grep 답은 사후 대안으로 추가할 수 있다. B가 밀어낸 jq 구현의 'Oniguruma 없는 build' 경고는 완결점수 밖 설명 손실이다.

**되물을 한 가지:** 모든 대괄호가 균형을 이루고 escape/quoted bracket이 없다는 점과 grep -P 지원을 확인할 수 있는가?

**귀속·한계:** 비채택 첫답은 recursive PCRE grep 명령+입출력. 질문자 성공 후속 없음. 봉인 jq filter 범위내8/8 일치; JSON quoting 확장반례는 조기절단. 위 처리 설명과 추천은 연구자의 적용 추론이며, 원문 사실과 사후 실행의 자세한 귀속은 outcomes.csv 및 각 sources 원장에 있다.

## P1 · 79332660

1. [질문자의 실제 후속 코드와 적용 대상 확인.](https://stackoverflow.com/revisions/6F659201-6815-46E2-BB6F-5C2C61CC5090/view-source)
2. [Div/Span 및 custom-style 계약 확인.](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt#L7349-L7376)

**질문자에게:** 자동 role 전달이 끊긴다는 진단을 준다. 공개 우회 코드는 원 문단별 custom role을 자동으로 복원한 해법이 아니다.

**유지관리자에게:** Asciidoctor 원 시험은 role 방출을 지지하고 Pandoc reader의 simpara 분기는 role을 custom-style로 보존하지 않는다. 소실 위치와 우회 성공을 구분한다.

**검색 결과 편집자에게:** 공식 custom-style 계약과 실제 후속 코드를 연결하되 '모든 굵은 요소를 test 문자 스타일로'라는 조건을 함께 보여 준다.

**되물을 한 가지:** 원 role 값과 목표 DOCX 스타일의 이름·문단/문자 유형을 어떻게 일대일 연결해야 하나요?

**귀속·한계:** 질문자 self-answer는 Strong→Span(custom-style=test) 우회 성공. 원 DocBook 문단 role 보존과 다른 입력·목표이며 생성 DOCX는 없음. 위 처리 설명과 추천은 연구자의 적용 추론이며, 원문 사실과 사후 실행의 자세한 귀속은 outcomes.csv 및 각 sources 원장에 있다.

## P2 · 79369213

1. [기대 계약과 문단/문자 스타일 구분.](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt#L7349-L7376)
2. [질문자가 보고한 실제 XML 중복 반례.](https://stackoverflow.com/questions/79369213#comment139974623_79369213)

**질문자에게:** 기존 VE와 새 스타일이 왜 다르게 취급되는지 판단하려면 정의와 최소 입력이 필요하다. 현재 자료만으로 재사용 성공을 보장하지 않는다.

**유지관리자에게:** custom-style의 Div/Span과 DOCX paragraph/character style 유형을 확인한다. 같은 표시 이름만으로 같은 styleId/type을 보장하지 않는다.

**검색 결과 편집자에게:** 인접 도구를 발명하지 않는 A=B 대조다. 공식 스타일 계약 한 링크로 시작하고 실제 참조 파일을 받아야 진단을 좁힐 수 있다.

**되물을 한 가지:** 원본과 생성 DOCX의 word/styles.xml에서 두 VE 항목의 w:type·w:name·w:styleId를 제공할 수 있나요?

**귀속·한계:** 공개 답 없음. 질문자가 30일 내 styles.xml의 style name/id를 조사했으나 실제 reference.docx 및 해결 결과는 없음. 위 처리 설명과 추천은 연구자의 적용 추론이며, 원문 사실과 사후 실행의 자세한 귀속은 outcomes.csv 및 각 sources 원장에 있다.

## P3 · 79375162

1. [HTML 블록의 Markdown 해석 확장에 관한 정확한 주 도구 설명.](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt#L5282-L5318)
2. [Rmarkdown에서 그 옵션을 전달하는 공개 예와 답변자 결과 이미지.](https://stackoverflow.com/revisions/DF73AC92-8281-499B-963C-D995EEE0FB91/view-source)

**질문자에게:** 이 카드의 사후 옵션은 Rmarkdown의 pandoc_args로 markdown_in_html_blocks를 비활성화하는 예다. 원 문자열에 raw 표지를 더한 사전안과 적용 위치가 다르다. 두 방식은 고정3.6 중간 입력에서 같은 표를 냈지만 R 전체와 원 사용자판은 미검증이다.

**유지관리자에게:** YAML scalar의 Markdown 파싱과 RawInline HTML 경계를 구별한다. 사전 raw wrapper와 사후 reader 확장 비활성화는 서로 다른 주 도구 내부 해법이다.

**검색 결과 편집자에게:** 기본 링크는 원문 매뉴얼, 두 번째는 Rmarkdown YAML까지 연결한 채택 답으로 제시한다. 사후 발견을 B의 사전 승리로 올리지 않는다.

**되물을 한 가지:** 실제 Rmarkdown 렌더가 사용하는 전체 --from 형식과 R/rmarkdown 버전을 확인할 수 있나요?

**귀속·한계:** 현재 채택 답은 주 도구 markdown_in_html_blocks 비활성화. 답변자 화면은 R4.4.2/rmarkdown2.29/Pandoc3.1.11.1. 연구자3.6 중간입력: br38→0, R 전체 미실행. 원문은 옵션을 묻지만 사전 C1은 출력 목표로 고정; 옵션만 허용하는 사후 민감도는 양쪽 부분. 원문에 이전 주 질문의 repost라는 자술도 있음. 위 처리 설명과 추천은 연구자의 적용 추론이며, 원문 사실과 사후 실행의 자세한 귀속은 outcomes.csv 및 각 sources 원장에 있다.

## P4 · 79393445

1. [원 LaTeX reader에 맞는 RawBlock 변환의 공식 예.](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/lua-filters.md#L777-L874)
2. [생성 SVG를 HTML 산출물에 포함시키는 경계.](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt#L1015-L1037)

**질문자에게:** 원 그림의 preamble과 명령을 보존한 재현안은 있으나 이 환경에서 그림 생성은 실패했다. 단순히 HTML 파일이 생기는 것은 목표 그림을 보존했다는 증거가 아니다.

**유지관리자에게:** diagram filter는 CodeBlock을 처리하지만 원 LaTeX는 RawBlock이다. 공식 RawBlock Lua 예제에 원 TikZ preamble을 공급하고 SVG를 HTML에 포함하는 경로를 문서로 연결했다.

**검색 결과 편집자에게:** 공식 RawBlock 변환과 SVG 포함 문서를 한 쌍으로 반환한다. TeX·pdf2svg가 없는 환경에서는 문서 완결과 실행 가능을 같은 표지로 표시하지 않는다.

**되물을 한 가지:** pdflatex 포맷·원 TikZ 라이브러리와 pdf2svg를 갖춘 환경에서 같은 입력을 실행할 수 있나요?

**귀속·한계:** 공개 답은 PDF→MuPDF SVG와 출력 이미지, 질문자 후속 없음. 원 TeX는 RawBlock2개/TikZ1개로 읽힘. 봉인 filter 전체 실행은 exit83, pdflatex.fmt 부재. 위 처리 설명과 추천은 연구자의 적용 추론이며, 원문 사실과 사후 실행의 자세한 귀속은 outcomes.csv 및 각 sources 원장에 있다.
