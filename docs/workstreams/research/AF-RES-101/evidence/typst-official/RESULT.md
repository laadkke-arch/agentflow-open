# Q5 Typst 공식 동작 대조

**범위:** 단계② 원격 봉인 `4e7539906eb03abd46e6910643ed5317f97ddb45`의 Typst 후보 12자리. 최초 이력·봉인 후보와 30일 타인 제안 projection만 읽었다. OP 후속·자기 답·채택을 읽지 않고 동작을 판정했다. TY-U2의 세 빈 자리에 공식 문서에서 새 후보를 넣지 않았다. CSS 후보 TY-A1-C1은 root의 별도 공식 검증으로 최종 결합한다.

**실행:** 공식 v0.10.0 바이너리 `typst 0.10.0 (70ca0d25)`, 소스 `70ca0d257bb4ba927f63260e20443f244e0bb58c`. 2023-12-04 공개판이므로 2024년 1–2월 질문보다 앞선다. 다만 질문자의 실제 판은 미기재다. 연구자가 이 판에서 합성 입력을 실행한 결과이며 질문자의 실제 실행 증거가 아니다. 원 코드의 이름·소속·이메일은 합성 4명으로 바꿨다. [환경·공식 다운로드 SHA](environment.json)

## 후보별 판정

| 봉인 후보 | 필수 출력과 변경 불가 조건 | 실제 확인 | 판정과 제한 |
| --- | --- | --- | --- |
| TY-A1-C1 CSS | Typst 격자에 각 항목의 선 | 이 분담은 Typst 공식 자료만 담당 | root CSS 검증과 결합. 미확인 placeholder를 CSS 최종판정으로 쓰지 않는다. |
| TY-A1-C2 항목별 box | 4개 항목 둘레 선, 내용·격자 배치 유지 | 초기 배경 stroke 1개 → 항목 stroke 4개. 합성 12줄 내용 동일. 2열·4 row tracks·1cm gutter·silver 1pt dashed 유지 | **지지.** 같은 도구의 다른 처리 위치다. 실제 질문판·원 첨부 렌더는 미확인. |
| TY-A1-C3 outset | 표시할 선과 여백을 올바르게 조절 | 원 제안은 수치·width/height 유지 여부 미명시. 연구자 2pt/2cm 대조 모두 컴파일되지만 2cm에서는 테두리가 페이지 밖으로 나감 | **미확인/조건부.** 임의로 성공 수치를 넣어 원 제안을 완전 유효로 올리지 않는다. B 생존이지만 top2 밖이다. |
| TY-A2-C1 외부 red binding | 수학 모드에서 content·color 두 인자를 유지 | 같은 helper의 plain red 호출은 unknown variable. 외부 `#let red = red`를 더하면 원 수식이 붉게 출력 | **지지.** helper는 이미 알려져 있고 호출 환경이 달라졌다. 같은 helper 텍스트가 같은 효과를 보장하지 않는다. |
| TY-A2-C2 인수 #red | 원 수식·색 인자화 | 최초 댓글의 짧은 예시 성공. 원 수식을 유지하며 인수에만 #를 붙인 별도 적용도 성공; C1과 렌더 PNG SHA 동일 | **지지.** `#`는 code mode 진입이다. 후대 답변의 markup mode라는 명칭은 부정확하나 조작은 작동한다. 최초 예시에서 빠진 위첨자 −를 보존했다고 쓰지 않고 별도 적용으로 구분한다. |
| TY-A2-C3 | 빈 자리 | 구체적 타인 제안 없음 | 미확인/빈 자리. |
| TY-U1-C1 pagebreak | figure 전용 페이지·세로 중앙 | 원 prose의 literal `#pagebreak`는 함수 이름을 출력하고 1page에 남는다. `#pagebreak()`로 호출을 명시하면 3pages, 가운데는 figure·caption만 | **미확인/조건부.** literal과 의도된 함수 호출 해석을 분리. 괄호를 보충한 성공을 원 문자열 그대로의 성공이라고 하지 않는다. |
| TY-U1-C2 page container | figure 전용 페이지·세로 중앙·이미지+caption | 앞본문/그림/뒤본문 3pages. 도형 대조와 실제 합성 PNG 모두 가운데 페이지에 caption과 그림만 존재 | **명시된 수동 페이지 목표 지지.** 자동 float-page 스케줄링 동등성은 미확인. |
| TY-U1-C3 my-fig helper | C2와 같은 목표, 호출 시 placement 분기 | string `p` 분기에서 C2와 같은 가운데 페이지. 실제 PNG도 확인. built-in figure에 `p`를 직접 주면 타입 오류 | **명시된 수동 목표 지지.** 새 helper 이름은 새 floating 기구가 아니다. B는 생존하나 top2 밖. |
| TY-U2-C1/C2/C3 | 빈 세 자리 | 봉인된 30일 타인 후보가 없음 | 공식 자료 검색으로 빈 자리를 채우지 않음. |

기계 결합용 전체 12행은 [assessment.json](assessment.json)에 있다. 여기의 유효성은 공개 인지·실행·신규성을 뜻하지 않는다. 다른 유효 조작 손실의 후보별 근거로는 TY-A1-C2와 TY-A2-C1/C2에서 실제 기존 조작과의 차이를 지지한다. TY-U1은 이전 Typst 시도 자체가 미확인이므로 **출력이 유효하다는 사실과 이전 시도와 다르다는 사실을 구분**해야 한다.

## 실제 실행과 반례

[17행 실행 영수증](run-receipt.json)에 명령·UTC·종료값·입출력 SHA·변경한 입력·PDF 페이지/도형/텍스트 측정이 있다. **15개 컴파일 성공, 2개 의도한 실패 대조**다. 성공 컴파일 안에도 원 목적을 만족하지 않는 literal pagebreak 및 큰 outset 대조가 있으므로 15/17을 성공률로 해석하지 않는다. [요약 측정](metrics.json) [입력](inputs) [출력](outputs)

1. **TY-A1의 처리 위치:** 원 배경 stroke는 문서 body 뒤의 별도 content다. 항목마다 box를 만드는 조작은 map 결과 각각에 stroke를 붙인다. 현재 linked box reference와 고정 `container.rs`는 outset이 layout 크기를 바꾸지 않고 그리는 외곽을 늘린다고 설명한다. 실제 큰 outset에서 text 위치는 유지되고 테두리만 페이지 경계를 넘었다. 이는 같은 box 옵션이라는 이유로 모든 값이 원 목적을 충족한다고 할 수 없다는 반례다. [TY-D01](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/crates/typst/src/layout/container.rs) [TY-D05](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/crates/typst/src/layout/page.rs)

2. **TY-A2의 helper 동일성과 입력 환경:** `get`과 `get_in_math`는 모두 사용자 scope를 찾지만 기본 라이브러리 fallback이 각각 global과 math다. 그래서 helper가 같아도 outer red binding의 유무·값과 code escape에 따라 실패/붉은 출력/푸른 출력이 달라졌다. C1과 C2의 원 수식 적용은 PNG SHA `a00e81c47f5660490b01db50bd33475c7e0bd5e686d30c35bd7b16dafa51a030`으로 일치했다. 이것은 해당 입력·판에서의 효과 동등성이고 두 제안의 공개 출처·호출 방법을 같은 이력으로 합치는 이유가 아니다. [TY-D02](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/crates/typst/src/eval/math.rs) [TY-D03](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/crates/typst/src/foundations/scope.rs) [TY-D04](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/docs/reference/syntax.md)

3. **TY-U1의 이름·호출·처리 기구:** prose의 함수 이름은 호출과 다르다. literal은 오류 없이 `pagebreak`라는 글자를 출력했으므로 종료값 0만으로 페이지 분리를 통과시키면 안 된다. 실제 함수 호출·page container·helper의 p 분기는 이 입력에서 같은 고립 페이지를 만든다. 하지만 built-in figure는 `none/auto/top/bottom` 계열의 placement를 가지며, helper의 string p는 직접적인 내장 옵션이 아니다. 자동 float-page 선택·재배치는 테스트하거나 확정하지 않았다. [TY-D05](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/crates/typst/src/layout/page.rs) [TY-D06](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/crates/typst/src/layout/align.rs) [TY-D07](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/crates/typst/src/model/figure.rs)

직접 렌더한 대표 페이지와 상류 expected PNG 세 개를 눈으로 확인했다. [합성 출력 비교](outputs/visual-contact.png)에 1개/4개 테두리, 큰 outset의 잘림, 붉은/푸른 수식, literal pagebreak와 호출 성공의 차이가 보인다. 실제 PNG 입력의 결과는 [page container](outputs/u1-c2-image-page2.png), [helper](outputs/u1-c3-image-page2.png)에서 확인했다. PyMuPDF의 standalone red-only 문서 색 metadata가 흰색으로 추출되는 경우가 있어 색 판정은 그 필드에 단독 의존하지 않았고 실제 렌더를 대조했다.

## 근거 수와 실제 읽기

[자료 원장](sources.jsonl)은 **고정 문서/구현 7개 + 상류 입력/예상 출력 묶음 3개 = 고유 10개**를 산입한다. 현재 typst.app reference 3페이지는 같은 계보의 비교용으로만 기록하고 하한에 더하지 않았다. container/math-content/align의 원 `.typ`와 고정 expected `.png`를 각각 직접 읽고 봤다. expected 이미지 한 개를 독립 사건으로 늘리지 않았다. Page/grid overflow 보조 입력과 상류 시험 실행 설명은 읽었지만 최소량에는 추가하지 않는다.

상류 전체 test harness는 실행하지 않았다. 직접 실행한 것은 공식 동일판 바이너리에 넣은 이 보고서의 후보별 합성 입력이다. 이것과 원 upstream test 파일을 읽었다는 사실을 분리한다. [바이트·URL 수신 영수증](source-receipts.json)

입력 projection을 읽는 과정에서 답변자 작성의 30일 내 후대 revision도 노출됐다(TY-U1 revision3, TY-A2 revision2). 봉인된 첫 후보의 code를 그 후대 변형으로 교체하지 않았다. 특히 helper의 최초 string p와 후대 page-value selector를 섞지 않았다. OP 후속은 노출되지 않았다.

## 판단을 바꿀 최소 확인

| 현재 제한 | 다음 직접 확인 | 판정 변경 조건 |
| --- | --- | --- |
| 원 질문의 실제 Typst 판·렌더 이미지 미확인, author 데이터는 합성 | 질문자가 쓴 정확한 판에서 최초 코드와 per-author box를 같은 입력으로 실행 | 같은 연구판에서 지원된 필수 출력이 실제 판·입력에서 실패하면 그 후보를 조건부로 낮춘다. |
| outset 수치와 pagebreak prose의 호출 괄호 미명시 | 당시 수신한 구체적인 함수 호출·outset 값 확인 | 값이 페이지 밖으로 나가거나 literal 함수값 전달이 의도였으면 반박, 완전한 안전 호출이 확인되면 그 범위로 지지. |
| manual figure-page와 LaTeX 자동 floating은 다른 요구일 수 있음 | 본문 흐름을 끊지 않는 재배치·복수 figure·초과 크기의 입력과 허용 조건 | 자동 재배치가 필수이고 manual container가 이를 깨면 C2/C3의 요구 전체 충족을 낮춘다. |
