# 고정 매뉴얼·후보 계약 근거

이 파일의 최초 후보 계약과 MAN-01~09는 Stack Overflow 표본의 R0/R1·답을 전혀 열지 않은 문서 담당자가 작성했다. 그 뒤 별도 배정으로 jq 30개의 R0와 수정 존재 메타데이터만 읽었다(`frame_jq_review.json`). 후보 범위는 늘리지 않았다. 실행은 하지 않았으며, 기록한 것은 고정판 문서·상류 시험 행·변경 diff의 직접 독해다. 다른 회차 연구 결과, R1, 답은 읽지 않았다.

## 고정판

| 도구 | 지정 태그 | git ls-remote로 얻은 태그 대상 SHA | 고정 매뉴얼 blob SHA |
| --- | --- | --- | --- |
| jq | jq-1.7.1 | 71c2ab509a8628dbbad4bc7b3f98a64aa90d3297 | 11e59e1bfa85594923b0b918da9d6d531c11e325 |
| Pandoc | 3.1.11 | c3038dcd54152c4e18e49db31676b79ee7cc29b2 | 83aa443e9b17d296e2a236c515f5c46d90e1dcf2 |

`git ls-remote`의 태그와 `^{}`를 함께 요청했고 추가 peel 행은 없었다. 두 SHA에 대한 GitHub commit 응답도 확인했다. jq 대상 커밋의 UTC는 2023-12-13T19:20:22Z, Pandoc 대상 커밋의 UTC는 2023-12-16T02:56:27Z다. 이는 참조판 식별이지 표본 질문자의 설치판 확인이 아니다. Pandoc 매뉴얼 표시 날짜와 changelog의 3.1.11 표시는 2023-12-15여서 커밋 UTC와 달라도 혼동하지 않는다.

## 8후보의 계약

완전한 기계 판독 행은 `../candidates.csv`에 있다. 판정은 C1·C2 각각에 연결해야 한다. 한 조건을 맞추거나 구체적 사용자 코드가 있어야 맞는 후보를 전체 정답으로 바꾸지 않는다.

| 후보 | 문서가 직접 제공하는 동작 | 입력→출력 | 핵심 실패 경계 |
| --- | --- | --- | --- |
| select | predicate를 만족하는 값 통과 | 값→동일 값 또는 없음 | 필드 변경·집계·정렬 기능이 아님 |
| map | 각 값에 f 적용 후 결과 수집 | 배열 또는 객체 값→배열 | 객체 키 보존은 map_values와 구별; map 자체가 전체 집계가 아님 |
| sort_by | f의 키 결과로 배열 재배치 | 배열→같은 원소의 정렬 배열 | 필터링·값 변경·locale 정렬을 제공하지 않음 |
| group_by | 같은 키 원소를 묶고 키순 정렬 | 배열→하위 배열들의 배열 | 합계나 키→값 객체를 만들지 않음; 원래 그룹 등장순 유지 아님 |
| --metadata | 문서 metadata 설정/덮어쓰기 | 문서와 KEY/VAL→metadata가 바뀐 문서 | 출력 writer/template에서 사용하지 않는 키는 보이는 효과 미확인 |
| --template | 지정 template의 틀·변수 배치 | 지원 writer의 본문/metadata→독립 문서 | docx와 pptx에는 template이 없음; 임의 AST 변경과 구별 |
| --lua-filter | Lua handler가 AST를 수정 | AST+SCRIPT→수정 AST→writer | 사용자 코드 필요; reader 단계에서 소실된 원정보 복원 보장 없음 |
| --standalone | 기본 template의 header/footer 추가 | 문서→완전 문서 | 임의 본문 의미/스타일 변경과 다름; 자동 활성화 형식에서는 중복 flag |

jq의 기본 필드 접근, JSON 리터럴, 산술·비교·불리언, 필요한 배열 순회·포장은 허용한다. `map`의 f에는 기본 객체/배열 생성도 허용하지만 `map(select(...))`처럼 다른 고정 후보를 추가하면 단일 후보 충족으로 세지 않는다. 추가 named 함수·정의 함수·재귀·reduce·외부 프로그램은 이 단일 후보 계약 밖이다. 매뉴얼은 f에 더 일반적인 jq 식을 허용하지만, 연구에서는 후보 하나의 기여를 식별하도록 이 경계를 먼저 고정했다.

Pandoc 공통 배경은 기본 reader/writer와 `-f/-t/-o`, 원래 입력에 있는 metadata다. `--template`의 자체 template 문법과 암묵적 standalone은 허용한다. `--lua-filter`의 사용자 Lua는 옵션 필수 매개물로 허용하되 코드 필요 여부를 반드시 드러내며, 단지 작성 가능하다는 이유로 특정 변환의 충족을 단정하지 않는다. 다른 후보를 명시적으로 추가하거나 별도 전/후처리 프로그램을 붙이는 것은 단일 후보 계약 밖이다.

## 직접 확인한 반례·교차 확인

1. jq manual의 map 예제는 하나의 입력 값에서 복수 결과가 생기면 출력 배열 길이가 늘 수 있음을 보여준다. 따라서 map을 언제나 길이 보존으로 코딩하면 틀린다. 이 행위는 사용자 f의 결과 수에 달렸다. [MAN-01, L989–1049]
2. jq 상류 시험은 `sort_by`의 복수 키와 `group_by`의 조건 키를 별도 기대 출력으로 고정한다. 이 시험 행은 구현 유지보수자가 기대한 결과이며 이 조사에서 실행한 결과가 아니다. [MAN-03, L1400–1406]
3. Pandoc manual은 docx/pptx에 template이 없고 reference document를 쓰라고 한다. `--template`를 모든 문서 스타일 문제의 해법으로 연결하면 직접 반박된다. [MAN-02, L2151–2152]
4. Pandoc Lua 문서에서 inline handler는 inline/list, block handler는 block/list를 반환해야 한다. 반환 타입이 다르면 오류다. 코드의 존재와 정상 변환은 별도다. [MAN-05, L112–128]
5. 고정 HTML5 template은 title/author/date 등의 metadata와 body가 서로 다른 위치에 들어가는 실제 공식 구현을 보인다. 모든 임의 키가 자동으로 출력되지는 않는다. [MAN-06]
6. jq #2949는 큰 정수의 산술 변환 회귀를 수정하고 경계 기대값을 추가했다. 숫자 보존 조건이 있다면 단순 함수 이름과 문서 설명만으로 설치판·정밀도까지 보증할 수 없다. [MAN-07]
7. Pandoc 3.1.11 변경 diff는 3.1.10에서 고정 횟수로 돌리던 PDF 생산이 사용자 template에서 회귀를 일으킬 수 있었으며 로그 기반 추가 실행 판단으로 바뀌었다고 설명한다. 같은 `--template` 링크라도 엔진·판 차이는 별도의 전제다. [MAN-08]

## 자료 수와 독립성

최초 고정 시점의 성공 원자료는 `sources_manuals.jsonl` MAN-01~09의 9행, 독립 사건/저작 ID는 8개다. MAN-04(NEWS)와 MAN-09(태그 대상 commit)는 jq-1.7.1 release 한 사건으로 묶는다. MAN-03은 sort/group 기대값의 시험 저작이며 MAN-07의 큰 정수 회귀 사건과 다른 근거지만, 같은 상류 저장소의 자료이므로 독립 재현으로 부르지 않는다. 파일 수를 독립 실행자 수로 세지 않는다. 더 보수적으로 jq release와 수치 PR을 한 변화 family로 합쳐도 7개다. 두 역사 매뉴얼 외에도 공식 Lua 설명/예제, 실제 HTML5 template, 상류 시험, 두 도구의 변경 사건을 읽었다. 이후 R0 단계의 Pandoc 코드줄 번호 요구를 보강하기 위해 MAN-10~12를 추가했다. 이 3개 파일은 같은 LaTeX highlighting 생성 경로 한 저작으로 묶었으며, 초기 후보 계약에 사후 출처가 있던 것으로 소급하지 않는다.

개별 HTTP 요청마다 wall-clock을 저장하지 못했다. 출처 행의 `direct_read_utc`는 각 선택 절의 독해 완료를 기록한 2026-11-23T14:50:15Z 체크포인트다. 요청별 전송 시각으로 해석하지 않는다. 검색 서비스의 GitHub DisabledError, 잘못 추정한 경로의 404, 크기가 커 빈 본문으로 돌아온 changelog는 최소량에서 제외했고 `manual_failures.jsonl`에 남겼다. changelog의 필요한 release 부분은 고정 commit diff에서 별도로 직접 읽었다.

## 변경 기록

- 후보 첫 작성: 위 SHA·범위·반례를 R0 노출 없이 고정했다.
- 이 파일 이후 후보 계약을 바꾸면 사전 계약 변경임을 명시하고, 원판 판정과 소급해서 섞지 않아야 한다.
- R0 단계 추가 확인: jq Invoking 절 L78–89(기본 입력은 JSON 값 시퀀스), L124–129(-R은 줄 문자열이며 YAML parser가 아님)를 직접 읽었다. 후보 계약은 그대로다.
- R0 단계 추가 확인: MAN-10~12의 고정 LaTeX 생성 경로를 추적했다. `data/templates/default.latex` L249–251은 생성된 `highlighting-macros`의 삽입점이고 L397–399는 `header-includes` 삽입점이다. `src/Text/Pandoc/Writers/LaTeX.hs` L221–227은 highlighting 사용 시 선택 style의 `styleToLaTeX` 결과를 template 변수로 제공한다. `src/Text/Pandoc/Highlighting.hs` L50과 L81–100은 Skylighting를 사용하고 number/numberLines/number-lines 클래스와 startFrom을 formatter에 전달한다. 이 경로는 LaTeX 환경을 사용자 코드로 조절할 수 있는 위치의 증거다. margin 안으로 번호를 옮기는 특정 재정의가 실제로 작동했다는 증거는 없다. Skylighting 실제 의존판·PDF 엔진·컴파일 출력도 미확인이다.
