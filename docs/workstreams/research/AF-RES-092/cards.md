# 여섯 질문의 독자 카드

**사전 반환**은 `a04fbb20ca1a415235f69a1018a93e07e7adc926`에서 봉인한 A/B 판단이다. **사후 편집 카드**는 공개 답과 후속 기록을 읽은 뒤 독자에게 줄 안내다. 사후에 알게 된 해법으로 사전 점수를 바꾸지 않는다. 아래 명령·예상값은 문서로 구성한 예이며 이번 조사에서 바이너리를 실행한 결과가 아니다. 카드마다 열 링크는 최대 두 개다.

## J1 · 78264525 — 중첩 JSON의 모든 food 객체 수정

**입력 → 원하는 출력:** `lunch`, `snacks[]`, `dinner` 안의 `food` 객체가 있는 JSON → 각 `food`에 `extra_cheese: true`를 추가하고 기존 값과 중첩 구조를 유지한 JSON.

**사전 반환:** A 완결 / B 완결. 원문이 별도 앞뒤 도구를 지목하지 않아 두 경로의 허용 범위는 같았다. 객체인 `food`를 골라 재귀적으로 갱신하는 식을 반환했다.

**사후 편집 카드 — 유지:** 모든 하위 값을 방문하는 `walk`와 경로 대입을 연결한다. 공개 후속에서 보조 설명의 생략 표기를 그대로 실행한 실패가 있었으므로, 실행할 식은 완전하게 적는다.

```sh
jq 'walk(if type == "object" and has("food") and (.food | type == "object") then .food.extra_cheese = true else . end)' input.json
```

- [jq 1.7.1의 walk](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L1952-L1976) — 중첩 객체와 배열의 내부까지 방문한다.
- [같은 판의 경로 대입](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L3410-L3448) — 선택한 `food.extra_cheese`만 바꾸는 근거다.

**한 가지 확인:** `food`의 값은 **객체만** 있습니까, **null·배열 등 다른 타입도** 있습니까? 위 식은 비객체를 건너뛴다. 그 처리까지 바꾸려는 요구는 별도로 정해야 한다. 원 질문자의 주해법 성공 출력과 정확한 jq판은 미확인이다.

## J2 · 78265746 — tasks의 project/path 조회·갱신

**입력 → 원하는 출력:** `settings.tasks[].notebook_task.base_parameters`를 포함하지만 문자열 중간에서 끝난 JSON 조각 → 각 작업의 `project`/`path` 조회값, 또는 지정한 값으로 갱신한 전체 JSON.

**사전 반환:** A 부분 / B 부분. 배열 순회와 갱신 연산은 확인했지만 완전한 JSON, 새 값, 바꿀 원소가 없었다. 독립된 두 번째 원문 제약은 공석이다.

**사후 편집 카드 — 부분 유지:** 완전한 JSON을 받으면 다음 식으로 작업별 조회값을 낼 수 있다. 출력은 객체들의 스트림이며, 원 입력 전체를 수정해서 내는 명령과는 다르다.

```sh
jq '.settings.tasks[].notebook_task.base_parameters | {project, path}' input.json
```

- [jq 1.7.1의 배열 값 순회](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L520-L552) — `tasks[]`의 각 원소를 조회한다.
- [같은 판의 갱신 대입](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L3450-L3505) — 선택한 경로를 갱신할 때 볼 절이다.

**한 가지 확인:** **모든 tasks 원소**를 같은 새 값으로 바꿉니까, **선택한 원소만** 바꿉니까? 완전한 입력과 실제 새 값도 필요하다. 공개 답의 `app2`는 답변자가 택한 예시이며 원 요구의 새 값으로 채우지 않는다. 질문자의 실행·출력은 미확인이다.

## J3 · 78304807 — 인수로 받은 키의 값만 42로 갱신

**입력 → 원하는 출력:** `{"a":1,"b":2,"c":3}`와 문자열 인수 `key=b` → `{"a":1,"b":42,"c":3}`.

**사전 반환:** A 완결 / B 완결. 문자열을 만들어 필터처럼 실행하는 대신 `.[$key]`로 속성을 선택하고 40을 더한다.

**사후 편집 카드 — 유지:** 공개 답의 다른 곱셈 예에 있는 숫자를 옮기지 않고, 원 질문의 기대값 42를 유지한다.

```sh
printf '%s\n' '{"a":1,"b":2,"c":3}' | jq --arg key b '.[$key] += 40'
```

- [jq 1.7.1의 객체 인덱스](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L461-L466) — 문자열 변수로 키를 지정하는 근거다.
- [같은 판의 경로 대입](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L3410-L3448) — 다른 속성을 보존하며 지정한 경로만 갱신한다.

**한 가지 확인:** 전달하는 값은 **최상위의 리터럴 키 이름**입니까, **중첩 경로**입니까? 위 식에서 `a.b`는 점을 포함한 하나의 키 이름이며 중첩 경로로 자동 해석되지 않는다. 원 질문자의 정확판과 실제 출력은 미확인이다.

## P1 · 78273711 — R Markdown의 누락 글리프와 PDF/HTML 출력

**입력 → 원하는 출력:** XeLaTeX·Eisvogel·NotoSans 경로를 지정한 R Markdown → 이모지·특수문자가 보이는 PDF. 원 헤더의 HTML 출력도 유지해야 한다.

**사전 반환:** A 부분 / B 부분. A는 폰트 지정과 글리프 존재를 구별했고, B는 R Markdown의 인수 전달과 템플릿·fontspec 연결을 추가로 확인했다. 어느 경로도 실제 문자와 설치 폰트의 공석을 채우지 못했다.

**사후 편집 카드 — 후보 보완, 부분 유지:** 공개 답의 **LuaLaTeX + luaotfload fallback + NotoColorEmoji**를 검토할 후보로 추가한다. 해당 답은 PDF 설정 예이며 HTML 동시 출력과 실제 설치·문자 커버리지를 확인한 기록은 없다.

- [Pandoc 3.1.11의 LaTeX 폰트 지정](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/MANUAL.txt#L2922-L2939) — 폰트 이름·옵션과 엔진의 연결을 확인한다.
- [공개 LuaLaTeX fallback 답](https://stackoverflow.com/a/78275798) — 사후에 찾은 소비자 측 설정 후보이며, 원 사용자의 해결 확인은 아니다.

**한 가지 확인:** 실패한 문자의 실제 Unicode 값이 지정한 NotoSans 파일에 **있습니까 / 없습니까**? 이름이 Noto라는 사실이나 Unicode 문자를 생성한 상류 시험만으로 PDF 글리프 표시가 입증되지는 않는다. HTML 요구, 폰트 설치, 정확 사용판 및 실제 출력은 미확인이다.

## P2 · 78311072 — Quarto PDF 표의 위·아래 선 제거

**입력 → 원하는 출력:** 빈 헤더와 Alice/Bob/Charles 행이 있는 Quarto Markdown 2열 표 → 내용은 유지하고 위·아래 가로선이 없는 PDF.

**사전 반환:** A 완결 / B 완결로 봉인했다. 이 판단의 범위는 고정 Pandoc writer가 낸 인수 없는 `toprule`/`bottomrule`, booktabs가 먼저 로드되는 조건, 전역 재정의에 한정된다.

**사후 편집 카드 — 원 Quarto 연결은 부분:** Quarto의 삽입 위치와 실제 생성된 `.tex`의 rule 호출형을 먼저 맞춘다. 공개 답의 `[2]{}` 재정의와 사전의 `{}` 재정의는 문자 그대로 같지 않으므로 실제 호출을 보지 않고 서로 바꿔 쓰지 않는다. **엄격한 같은 예산 비교에서는 P2를 비교불가 1건으로 분리했다.** 사전 라벨을 소급 변경한 것은 아니다.

- [고정 Quarto의 include-in-header 규칙](https://github.com/quarto-dev/quarto-cli/blob/466d959674507930685b2c977e878495932152ba/src/resources/schema/document-includes.yml#L52-L66) — 파일명과 `text` 본문 전달을 구별한다.
- [공개 top/bottom rule 재정의 답](https://stackoverflow.com/a/78314393) — 구체적 후보를 보여주지만 채택 표지는 원 `.tex`/PDF 성공 영수증을 대신하지 않는다.

**한 가지 확인:** 선을 **문서의 모든 표에서** 지울까요, **이 표에서만** 지울까요? 전역 재정의와 한 표 한정은 같은 조건이 아니다. 원 Quarto/Pandoc/TeX판, 생성 `.tex`, 적용 순서와 실제 PDF 출력은 미확인이다.

## P3 · 78358965 — 페이지 번호 없는 인용과 서지 복구

**입력 → 원하는 출력:** Better BibTeX 서지·CSL과 각주의 `@achelis1897` 인용 → 페이지 번호 없이도 해당 인용, 같은 저작의 다른 인용, bibliography가 정상 표시되는 문서.

**사전 반환:** A 부분 / B 부분. 페이지 번호가 선택값이라는 근거는 확보했지만 실제 입력·CSL이 없어 누락 원인을 확정하지 못했다. B의 BBT/CSL 조사도 이 공석을 해소하지 못했다.

**사후 편집 카드 — 반환 변경:** 공개 답과 파서 근거가 가리키는 주 도구 내부의 `example_lists` 충돌을 먼저 확인한다. 기존 명령에서 Markdown 입력 형식에 다음 옵션을 적용하는 후보를 반환한다.

```text
--from=markdown-example_lists
```

- [Pandoc 3.1.11의 example_lists](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/MANUAL.txt#L4272-L4305) — `@` 표기가 번호 예제와 참조가 될 수 있는 근거다. 같은 매뉴얼의 `--from` 절은 `-EXTENSION`으로 확장을 끄는 문법을 설명한다.
- [원 질문자의 해결 보고](https://stackoverflow.com/questions/78358965#comment138159258_78358965) — 답으로 문제가 해결됐다는 공개 보고가 있다. 정확판·전체 명령·해결 후 출력은 제시되지 않았다.

**한 가지 확인:** 같은 전체 입력에서 이 옵션만 바꾸면 인용과 bibliography가 **둘 다 복구됩니까 / 하나 이상 계속 누락됩니까**? 문단 중간의 인용·대괄호 인용까지 모두 example list라고 일반화하지 않는다. 이 사후 카드는 질문자의 해결 보고를 반영하지만 **사전 A/B 부분 판정은 유지**하며 정확 입력의 실행 재현은 미확인이다.
