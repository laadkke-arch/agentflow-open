# 사전 봉인 뒤의 별도 상류 동작 검증

기준: 사전 판단 원격 커밋 `a04fbb20ca1a415235f69a1018a93e07e7adc926` 뒤에 수행한 검증이다. 아래 자료는 신규 12경로가 사용한 검색·열람 예산에 소급해서 넣지 않는다. `TEST-JQ-PATHS`와 `TEST-PD-CITE`는 재산입하지 않는다. 원문은 고정 SHA의 raw 파일로 다시 가져와 로컬 캐시와 바이트가 같은지 확인했다. **상류의 입력·기대출력 fixture 및 원 사용 보고를 읽었으며, jq/Pandoc 바이너리나 PDF/DOCX 변환을 실행하지 않았다.**

## 신규 upstream_behavior 산입 자료

| ID | 고정 원문·직접 읽은 위치 | 입력·기대출력 또는 원 관측 | 지지하는 경계와 반례 | 한계 |
| --- | --- | --- | --- | --- |
| UP-01 | [jq 1.7.1 tests/shtest](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/tests/shtest#L288-L307) | `--arg foo 1 --argjson bar 2`에 기대하는 첫 출력은 `{"foo":"1","bar":2}`이며 뒤에는 `$ARGS.named`와 같다는 `true`가 온다. 이어진 `--slurpfile`/`--rawfile` 시험은 같은 JSON 파일을 각각 배열 안의 객체와 문자열로 받는다. | shell 인수→jq 값의 자료형 경계가 명시된다. 문자열 `1`과 JSON 숫자 `1`을 같은 입력으로 간주하면 후속 비교·조합을 잘못 판정할 수 있다. | 기대출력과 `cmp` assertion을 읽은 것이다. 이 환경에서 통과했다고 말하지 않는다. 특정 질문자의 shell·인용·변수 값 성공은 미확인이다. |
| UP-02 | [Pandoc 3.1.11 test/command/emoji.md](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/test/command/emoji.md) | 동일 `:smile:` 입력에서 `markdown+emoji` 출력은 별칭을 보존하고 `markdown-emoji` 출력은 `😄`이다. GFM 출력의 emoji 확장 on/off에도 대응하는 차이가 적혀 있다. | 문서 파서·작성기의 문자열/AST 변환과 최종 PDF 소비자의 glyph 렌더링을 분리해야 한다. 이 시험은 ‘Unicode 문자를 생성했다’까지 지지한다. | 폰트 파일·LaTeX 엔진·PDF의 가시 glyph를 시험하지 않는다. 이 fixture를 근거로 색상 emoji 렌더링 성공을 선언하면 과장이다. |
| UP-03 | [Pandoc 3.1.11 delimited locator fixture](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/test/command/pandoc-citeproc-locators-delimited.md#L14-L127) | `--citeproc -t markdown-citations`와 테스트 CSL을 사용한다. 빈 `{}`는 locator를 비워 뒤 숫자를 suffix로 유지한다. 범위 `35-89`는 기대출력에서 `35--89`로 바뀌며, 불균형 `{`·`}`는 locator 파싱을 바꾸는 반례가 있다. | 인용 본문 문자열→locator/suffix 해석→CSL 렌더링은 서로 다른 계약이다. 표시된 문자가 같다고 파서 의미까지 같지는 않다. | 일반 저널 스타일이 아니라 `command/locators.csl`이라는 시험 전용 스타일이다. 원 질문의 CSL·서지 레코드·실사용 결과로 일반화하지 않는다. 기존 Chicago fixture와 다른 파일·다른 시험이지만 같은 Pandoc 시험 저작 계보로 묶는다. |
| UP-04 | [Pandoc 3.1.11 pipe table 입력](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/test/pipe-tables.txt#L28-L34) 및 [native 기대출력](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/test/pipe-tables.native#L369-L455) | 빈 셀로 된 헤더 줄·정렬 줄·본문 3행의 입력이 있고 대응 native fixture에는 `TableHead ( "" , [] , [] ) []`가 있다. 본문 값 12·123·1과 정렬은 보존된다. | 주 도구 안에서 입력 표현을 해석하여 headerless AST를 만들 수 있다. ‘빈 헤더 셀 행’과 ‘행 없는 TableHead’는 같은 구조가 아니다. | 입력·출력 파일을 한 시험 묶음 한 건으로 센다. 이 native fixture만으로 모든 writer·PDF/DOCX 소비자의 동작을 보증하지 않는다. |
| UP-05 | [Pandoc #7343 원 사용 보고](https://github.com/jgm/pandoc/issues/7343), 2021-06-01T22:18:40Z | 보고자는 2.11.3→2.11.4 갱신 후 `pandoc test/pipe-tables.txt -o test/pipe-tables.pdf -f markdown`에서 headerless 사례의 PDF에 빈 헤더가 생겼다고 적었다. 프로젝트 시험 입력을 재현 경로로 명시했다. | 같은 입력·같은 도구 이름이어도 판이 바뀌면 소비 결과가 달라진 실제 회귀 보고다. 주 도구 내부 수정이 필요한 사례를 불필요한 새 인접 도구로 우회할 수 있다는 반례다. | 최초 보고 본문을 직접 읽었다. 관련 commit의 전체 diff·PDF 출력·수정판 바이너리는 확인하지 않았다. 보고자의 원인 commit 지목을 독립 검증한 것으로 취급하지 않는다. |
| UP-06 | [Pandoc #7369 원 사용 보고](https://github.com/jgm/pandoc/issues/7369), 2021-06-09T22:35:53Z | 보고자는 Lua `SimpleTable`의 `headers = {}`로 만든 표가 Pandoc 2.14 DOCX에서 invalid가 되고 2.13은 정상이라고 기록했다. 빈 `<w:tr>`와 `tblHeader` XML을 제거하면 정상이라는 관측 및 빈 셀 두 개로 바꿨을 때의 우회 결과를 제시했다. | AST·writer·최종 Office 소비자의 구조 경계를 보여준다. 빈 헤더의 두 표현을 등가로 취급하면 실제 파일 유효성이 달라질 수 있다. | 본문에 재현 명령·입력 Lua·출력 XML·첨부 링크가 있다. 첨부 DOCX 자체는 열지 않았고 해당 사용자 환경을 재현하지 않았다. ‘보고된 성공/실패’ 수준을 유지한다. |

## 직접 자료 수와 독립성

새로 산입한 `upstream_behavior`는 **UP-01–UP-06 여섯 건**이다. 이 중 네 건은 서로 다른 상류 시험 묶음, 두 건은 서로 다른 원 사용자 회귀 보고다. UP-04의 입력·출력 두 파일은 한 시험 묶음으로 셌다. 보수적으로 jq 시험 저작 1, Pandoc 시험 저작 1, 이슈 #7343 사건 1, 이슈 #7369 사건 1의 **독립 저작/사건 네 그룹**으로 보고한다. 상류 시험 파일 수가 독립 인간 실험 수라는 주장은 하지 않는다.

UP-X01은 locator fixture가 직접 가리킨 [pandoc-citeproc PR #362](https://github.com/jgm/pandoc-citeproc/pull/362)의 본문이다. balanced bracket locator와 suffix 분리에 관한 변경 목적 및 기존 시험 기대값 변화의 불확실성을 직접 읽었다. 주 동작 자료 여섯 건에는 더하지 않는다. UP-X02의 시험 CSL은 UP-03 해석 전제를 확인하는 보조 파일이다. 최초 작성시각을 확인하지 못한 시험 파일은 판 포함 시각을 상한으로만 남기며 파일의 최초 공개시각을 꾸며 쓰지 않는다.

## 사전 판단을 바꿀 수 있는 범위

이 자료는 사전 결과를 소급 수정하지 않고 조건을 덧붙이는 데 사용한다. UP-01은 jq 앞단 shell 변수를 JSON 문자열/숫자로 넘기는 계약, UP-02는 문자 생성과 glyph 렌더링의 구분, UP-03은 citation text와 CSL 처리 경계, UP-04–06은 표 구조와 consumer 결과의 차이를 검증한다. 특정 신규 질문의 완결성 승패를 바꾸려면 그 질문의 정확 입력·금지 조건·사용판이 이 상류 fixture와 대응한다는 추가 근거가 있어야 한다.

다음 최소 관측은 각 사례의 R0 입력에 대한 고정판의 실제 산출물 하나다. 현재 상태에서는 상류 fixture 존재와 공개 회귀 보고까지 확인했고, 연구자의 실행 성공·질문자 실제 채택·정확판 재현은 별도 미확인이다.

## P3 사후 해법과 example_lists 충돌: 추가 확인

부모 조사자가 사후 답에서 확인한 `--from=markdown-example_lists` 해법을 전달한 뒤 읽은 근거다. 기존 A/B 경로의 결과를 이 자료를 이용해 다시 성공으로 분류하지 않는다. 이 단락의 입력 예시는 파서 분기를 설명하기 위한 최소형이며 원 질문의 전체 입력을 복제한 것이 아니다.

- **UP-P3-READ:** [고정 Markdown reader](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/src/Text/Pandoc/Readers/Markdown.hs#L948-L962)는 `Example` 목록 스타일에 `guardEnabled Ext_example_lists`를 요구한다. [813–840행](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/src/Text/Pandoc/Readers/Markdown.hs#L813-L840)은 marker 다음에 공백 또는 줄바꿈을 요구한다. [2192–2234행](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/src/Text/Pandoc/Readers/Markdown.hs#L2192-L2234)은 이미 등록된 example label을 citation으로 다루지 않고 뒤늦게 확인된 label도 숫자 참조로 만드는 분기를 명시한다.
- **UP-P3-LIST:** [고정 list parser](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/src/Text/Pandoc/Parsing/Lists.hs#L112-L170)는 `@` 다음 영숫자 label을 읽고 `Example`을 반환한다. 일반 marker 생성은 이 parser를 마침표 delimiter와도 조합한다. 따라서 **블록 시작의 `@achelis1897. text`**에서 `@achelis1897.`가 example marker가 될 수 있다는 구조적 근거가 있다. `@achelis1897`만 있는 문자열, 대괄호 인용 `[@achelis1897]`, 문단 중간의 문자열까지 무조건 같은 분기로 간다고 확대하지 않는다.
- **UP-P3-TEST:** [별도 회귀 fixture 6836.md](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/test/command/6836.md)는 `(@foo)`를 `OrderedList ... Example ...`로, `See @foo.`를 숫자 1 참조로 기대한다. 앞뒤의 `[@buchanan]`은 각각 `Cite`이며 noteNum 1·2를 유지한다. 이것은 example 참조와 citation 해석이 같은 reader 상태를 공유한다는 기대출력 근거다. `achelis1897`이라는 정확키·마침표 목록 입력의 실행 시험은 아니다.

**정정의 의미:** 주 도구의 parser 확장 선택만으로 문제를 풀 수 있는 실제 후보가 사후에 드러났다. 입력 reader에서 이미 citation과 다른 구조로 읽혔다면 BBT 출력이나 CSL 표시 규칙의 변경은 원인보다 뒤의 단계를 건드린다. 이는 ‘도구 이름 밖 인접 단계를 허용하면 반드시 더 완결해진다’는 주장의 반례 후보다. 판정을 확정하는 최소 관측은 같은 전체 입력에 대해 `-f markdown -t native`와 `-f markdown-example_lists -t native`가 각각 `OrderedList Example`과 의도한 `Cite`를 만드는지 비교하는 것이다. 현재는 코드·fixture 독해만 했으므로 정확 입력에서의 그 출력은 미확인이다.

추가 P3 코드 두 파일과 fixture 한 파일은 원장에 별도로 기록하되 앞의 **새 upstream_behavior 여섯 건**에 더하지 않았다. 동일 소스가 다른 원장 항목에서 이미 세어졌을 가능성을 남겨 전체 합산은 canonical URL/SHA로 중복 제거해야 한다.
