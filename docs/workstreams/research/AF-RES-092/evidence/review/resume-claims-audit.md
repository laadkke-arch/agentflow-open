# AF-RES-092 재개 기술 주장 감사

검토 대상: `b40b4dfeb8b7079f6568e511105117b02f477d14`. 검토 종료 관측 UTC: 2026-11-23T17:13:41Z. 별도 협업자가 커밋된 결과와 고정 1차 원문을 대조했다. 이는 새로운 독립 맹검 탐색이나 원 사용자 재현이 아니다. 최초 12경로·봉인 후보·판정을 다시 실행하거나 수정하지 않았다. 신규 외부자료 최소량 기여는 0이다.

## 결론

**PARTIAL 유지가 타당하다.** J1/J3의 두 경로 완결은 명시한 원 예제 범위의 문서 적합 판정으로 지지된다. P2는 고정 Pandoc 생성 코드의 가능한 해법과 원 Quarto 실행 연결을 구별해야 한다. P3는 공개 해법과 reader 코드가 원인 후보를 강하게 지지하나, 정확한 원 입력·명령·판의 AST/최종 출력은 검증되지 않았다.

## 직접 다시 연 근거

|검토|원문과 위치|직접 확인·결론|한계|
|---|---|---|---|
|J1 재귀 보존|[jq builtin.jq 235–263](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.jq#L235-L263), [대입 문서](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L3370-L3520)|walk는 객체 값/배열 항목을 재귀 방문한 뒤 f를 적용한다. 객체 food만 수정하는 가드와 경로 대입은 나머지 구조 보존을 지지한다.|모든 food가 객체라는 원 예제 범위. 비객체를 건너뛰는 것을 실제 사용자 요구라고 일반화하지 않는다. 바이너리 미실행.|
|J3 동적 키와 산술 갱신|[객체 인덱스](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L450-L470), [갱신 대입](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L3410-L3452)|문자열 변수의 객체 인덱스와 +=40은 b=2→42 및 a/c 보존을 문서로 지지한다. 카드는 답변자의 곱셈 출력 대신 원 목표를 유지했다.|문자열 a.b는 하나의 키다. 원 사용판·실제 실행 확인은 아니다.|
|P2 빈 머리글과 선|[Table.hs 45–125](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/src/Text/Pandoc/Writers/LaTeX/Table.hs#L45-L125)|빈 머리글 분기에서도 top rule을 내고 bottom rule을 별도 생성한다. 빈 헤더 자체가 선 제거 해법이라는 추론은 반박된다. rule 뒤의 noalign과 빈 그룹까지 함께 확인했다.|Quarto의 실제 template/생성 tex 및 원 PDF는 이 정적 코드와 동일하다고 확인하지 않았다. {}와 [2]{} 재정의는 인수 소비가 다르다.|
|P2 include 전달|[Quarto schema 1–85](https://github.com/quarto-dev/quarto-cli/blob/466d959674507930685b2c977e878495932152ba/src/resources/schema/document-includes.yml#L1-L85)|include-in-header 문자열은 파일명, text 객체는 본문이다. 별도 header-includes는 literal content를 받는다. 잘못된 전달 형식은 조합을 깨뜨릴 수 있다.|이 스키마만으로 실제 패키지 로드 순서·후속 재정의 부재를 증명하지 못한다.|
|P3 reader 분기|[Markdown.hs 813–840](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/src/Text/Pandoc/Readers/Markdown.hs#L813-L840), [948–962](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/src/Text/Pandoc/Readers/Markdown.hs#L948-L962), [2192–2234](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/src/Text/Pandoc/Readers/Markdown.hs#L2192-L2234), [Lists.hs 112–170](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/src/Text/Pandoc/Parsing/Lists.hs#L112-L170)|@label+period 표식 및 뒤 공백/개행이 목록 문맥에서 Example로 읽힐 수 있고 example_lists guard가 있다. 등록된 example label은 citation 대신 숫자로 처리될 수 있다. reader 단계 설명을 지지한다.|전체 원문·판·명령이 없으므로 실제 R0 AST를 직접 관측한 것은 아니다. 문단 중간·대괄호 인용을 일괄 example 목록이라고 하면 틀린다.|

## 필요한 최소 문구 수정 1건

`RESULT.md`의 조합 반례 문단에는 **“반대로 P3에서는 reader가 이미 다른 구조로 해석했으므로 … 실제 원인에 닿지 않았다”**라는 단정이 있다. 주변 절과 SELF_CHECK는 미확인을 충분히 적었으나 이 한 문장은 정확한 원 AST를 관측한 것처럼 읽힐 수 있다.

권고 대체문:

> P3의 공개 답·해결 보고와 고정 reader 코드는 example_lists 충돌을 지지하지만, 원 입력의 실제 AST는 미확인이다. 사전 두 경로는 주 도구 내부의 이 reader 후보를 반환하지 않았다.

봉인 판단·수치·카드의 조건은 바꿀 필요가 없다. 이 수정은 사후 설명의 증거 수준을 맞춘다.

추가로 공개답의 [2]{}가 “두 토큰”을 소비한다는 표현은 “두 필수 인수(고정 writer에서는 noalign 명령과 빈 그룹)”라고 쓰면 더 정확하다. 이 표현 차이는 현 PARTIAL 판정을 바꾸지 않는다.

## 접근·재현 한계

Stack Overflow 질문/답 웹 주소 2개를 재열람했으나 DisabledError여서 새 내용 확인은 실패했다. 공개 답·질문자 댓글 부분은 커밋된 원 영수증의 검토까지만 했다. 직접 다시 연 GitHub 고정판의 URL·범위·blob SHA·관측 시점·한계는 [receipts.json](resume-claims/receipts.json)에 있다. 모든 항목은 이미 조사한 계보의 재열람이거나 실패이며 신규 원자료 최소량과 경로 비용에 합산하지 않는다.

