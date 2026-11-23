# jq J1–J4 사후 공개 근거와 고정판 실행

## 시간 경계와 귀속

사전 두 경로 원장·판정의 원격 봉인은 `d03ca37daf0c43688c68bc39417d84a9b84803e9`이다. 이 묶음은 그 뒤에 읽은 공개 자료와 연구자가 수행한 실행만 기록한다. 사전 경로 파일·판정은 수정하지 않았다. 최초 사후 자료 열람 시각은 **2026-11-23T18:28:34.641413+00:00**이며 `first-public-read.json`과 `public-read-log.jsonl`에서 재확인할 수 있다.

공개 최초답 5개, 댓글 14개, 질문 본문 revision 7개를 직접 읽었다. 추가 답 수정본 3개도 읽어 최초답과 분리했다. 같은 답의 수정·같은 질문의 댓글을 새로운 독립 사건으로 세지 않는다. 독립 질문 사건은 4개이다. 공개 후속은 외부 1차자료 하한에 추가 산입하지 않는다. 아래 실행은 사전 방식의 검색2회/본문4회 밖에서 이루어진 보조 검증이다.

## 공개 행동과 엄격 판정

| 요청 | 현재 채택 | 30일 이내 질문자 행동 | 정확한 질문자 실행 확인 | 사전판정과 관계 |
|---|---|---|---|---|
| J1 | 79322532 | 생성 후 댓글·본문수정 없음 | 미확인 | 주 도구 안의 다른 배열/join 조합으로 같은 구조를 해결하는 답. 채택만으로 실행 입증하지 않음 |
| J2 | 79388975 | 두 댓글 중 하나에서 수정되는 듯하다고 보고하고 설명 요청 | 미확인 | 객체결합에 대한 긍정과 모든 출력조건 완결은 다름. offset 결손 때문에 A/B 부분 유지 |
| J3 | 79389420 | 실제 사례는 merge 전 변형이 더 필요하지만 같은 접근이 작동한다고 보고 | 미확인 | 주 도구 안의 undocumented 함수·후속 while 대안. A/B 완결 방향과 일치 |
| J4 | 없음 | 실패 지적, 괄호문법 추정, 실제형 예시 추가와 본문수정 두 차례 | 미확인 | 인접 grep의 짧은 공개 답이 있지만 질문자 성공 후속 없음. 사전 B 승리로 소급하지 않음 |

현재 채택 3/4, 질문자의 명시적 또는 약한 긍정 후속 2/4, 생성 후 공개 행동 관측 3/4, **입력·명령·판·성공출력을 함께 확인한 질문자 실행 0/4**이다. 분모를 바꾸거나 긍정 댓글을 exact execution으로 승격하지 않는다. 현재 채택의 실제 시각은 API에서 확인되지 않는다. J4의 30일 뒤 댓글 하나는 제3자의 사교적 대화여서 성과자료에서 제외했다.

## 답의 최초판과 수정 시각

| 요청/답 | 생성 UTC | 마지막 수정 UTC | 읽은 본문 revision UTC |
|---|---|---|---|
| J1/79322532 | 2025-01-02T00:04:07+00:00 | 없음 | r1: 2025-01-02T00:04:07+00:00 |
| J2/79388975 | 2025-01-26T17:28:55+00:00 | 2025-01-26T18:51:21+00:00 | r1: 2025-01-26T17:28:55+00:00<br>r2: 2025-01-26T18:51:21+00:00 |
| J2/79389173 | 2025-01-26T19:32:22+00:00 | 없음 | r1: 2025-01-26T19:32:22+00:00 |
| J3/79389420 | 2025-01-26T22:36:55+00:00 | 2025-01-26T22:49:05+00:00 | r1: 2025-01-26T22:36:55+00:00<br>r2: 2025-01-26T22:43:47+00:00<br>r3: 2025-01-26T22:49:05+00:00 |
| J4/79426171 | 2025-02-10T05:53:50+00:00 | 없음 | r1: 2025-02-10T05:53:50+00:00 |

## 요청별 사후 해석

### J1: 같은 주 도구의 다른 조합

[최초 답](https://stackoverflow.com/revisions/13C6400D-B8AD-4285-9F6A-0099B190B016/view-source)은 부모 startTime 배열과 자식 tuple을 더하고 join한다. 사전 filter는 부모 값을 변수로 보관한 뒤 자식을 순회한다. 둘 다 부모 문맥을 유지하지만 같은 코드는 아니다. 공개 본문에는 완전한 입력, jq판, 실행 stdout이 없고 후속 댓글도 없다. 현재 채택은 “질문자가 이 답을 채택했다”는 관측까지만 지지한다.

### J2: “고쳐졌다”는 후속과 누락 출력값의 불일치

[채택 첫답](https://stackoverflow.com/revisions/4DB44BBE-C949-4542-BB30-1A1951A2B774/view-source)은 .modules.data 전체를 객체 생성의 입력으로 유지한다. 두 하위 값이 각자 배열을 순회하므로 사용자가 겪은 empty 출력은 설명된다. [질문자 댓글](https://stackoverflow.com/questions/79388729#comment140003480_79388975)은 이 변경이 수정되는 듯하다고 말하며 동작 이유를 묻는다. 그러나 offset이 들어 있는 전체 입력이나 3645/3820을 실제로 출력한 결과는 없다.

[별도 INDEX 답](https://stackoverflow.com/a/79389173)은 start/end가 null인 출력을 직접 보여준다. 이는 사전 결손 판정을 지지한다. 원 입력의 title/artist와 원하는 값의 뒤바뀜·문자열 생략도 여전히 남는다. 엄격 완결 기준이 사용자의 실제 핵심 관심보다 좁거나 넓을 수 있다는 불일치가 드러난다. 이 연구에서는 사전 명시 조건을 보존하므로 A/B 부분을 유지한다. 제품 카드는 핵심 객체결합을 설명하면서 offset 원자료를 한 번 더 물어야 한다.

### J3: 채택 답이 검색자가 쓴 절과 다르다

[첫 답](https://stackoverflow.com/revisions/5D70FEFA-D7F3-4AC3-AB07-3FFFAA3DB427/view-source)은 undocumented `_nwise`로 두 항목씩 묶고 add한다. [수정판](https://stackoverflow.com/revisions/8B5D568A-8370-4DA2-8612-FF08869D3144/view-source)은 문서화된 while/slicing 조합도 제공한다. 사전 range/index 조합은 이 둘과 다르다. [질문자 후속](https://stackoverflow.com/questions/79389414#comment140005591_79389420)은 실제 사례는 더 복잡하지만 같은 접근이 작동한다고 말한다. 실제 객체 변형 코드·전체 Overpass 입력·판·실행 출력은 없어서 exact execution은 미확인이다. Overpass 입력이 언급되어도 최종 처리가 jq 안에서 끝나는 반례이며, 인접 도구가 꼭 필요했다고 결론 내릴 수 없다.

### J4: 짧은 인접 도구 답과 긴 합성 해법의 차이

[공개 답](https://stackoverflow.com/a/79426171)은 PCRE를 지원하는 grep의 재귀 capture group으로 균형 괄호를 처리한다. 답변자 test.txt와 세 줄 출력이 함께 있다. 이는 본 연구의 긴 jq 상태형 filter보다 짧은 사후 대안이지만, 그 재귀 문법을 사전 B의 grep 매뉴얼 원문에서 실제 찾았던 것은 아니다. B가 인접 파일을 읽었다는 사실을 “인접 완성해법을 발견했다”로 바꿀 수 없다.

[질문자 후속](https://stackoverflow.com/questions/79410149#comment140049230_79410149)은 괄호가 맞고 escape되지 않는 것으로 생각한다고 표현한다. 다른 참여자는 그 문법을 확정해야 한다고 지적했다. 질문 수정판은 쉼표 포함 예시를 추가했고 뒤에는 일부 중첩 예시를 삭제했다. 삭제된 현재 본문에 맞춰 R0의 중첩 조건을 사후 제거하지 않는다. 공개 해법의 성공 확인은 답변자 예시에 한정되고 질문자 성공·채택은 없다.

## 정확한 비교판에서 실행한 결과

공식 [jq 1.7.1 릴리스](https://github.com/jqlang/jq/releases/tag/jq-1.7.1)의 Linux amd64 자산을 소유 경로의 ignored cache에만 다운로드했다. [공식 checksum](https://github.com/jqlang/jq/releases/download/jq-1.7.1/sha256sum.txt)의 해당 행과 계산 SHA-256이 일치했다. 실행파일은 `jq-1.7.1`과 `--with-oniguruma=builtin`을 보고했다. 기본 설치된 `/usr/bin/jq`의 jq-1.7은 사용하지 않았다.

- 실행파일 SHA-256: `5942c9b0934e510ee61eb3e30273f1b3fe2590df93933a93d7c58b81d19c8ff5`
- J4 봉인 filter SHA-256(A/B 동일): `04bb18fed48eafaa334f8a307ae2b2fee2388b2ea34cf4ef836cc75540de7a1d`
- 실행환경: Linux x86_64, glibc 2.41, Python 3.12.14. 세부 build configuration은 `runtime-environment.json`에 있다.
- 입력·필터·출력·stderr·명령·종료값·실행시각·해시는 `validation/`, `validation-inputs.json`, `validation-filters.json`, `runtime-results.json`에 보존했다.

| 검사 | 입력 귀속 | 실행 수 | 관측 |
|---|---|---:|---|
| J4 원문 로그 한 줄·빈값 | R0의 짧은 code block 그대로 | A/B 각2 = 4 | 전부 exit0, 기대출력 일치 |
| J4 중첩+반복+이웃필드 / marker 없는 줄 | 연구자 제작, 원 요구 범위의 반례 | A/B 각2 = 4 | 전부 exit0, 기대출력 일치 |
| J1 잘린 원 입력 | R0 조각 그대로 | 1 | exit5, Unfinished JSON term; 알려진 입력결손 재현 |
| J1 문법 최소 수리 | 말미 comma 제거와 배열/객체 닫힘만 추가 | 1 | 봉인 filter로 정확히 3줄, 부모·자식 대응 유지 |
| J3 단순 원 배열 | R0의 a/b/c/d 배열; .elements만 제거한 사후 filter 변형 | 1 | ab/cd 출력 일치 |
| J3 elements envelope | 원 단순값을 연구자가 .elements에 감쌈; 봉인 filter 그대로 | 1 | ab/cd 출력 일치 |
| J4 quoted bracket 경계 | 연구자가 JSON quoting 의미를 추가한 범위 밖 입력 | 1 | exit0이지만 조기절단; 추가 기대출력 불일치 |

총 13실행이다. 기본 12실행은 11개 유효입력 성공과 1개 알려진 잘린입력 실패로 분리된다. J4의 원 요구 범위 검사 8/8 성공과 다음 범위 밖 반례 0/1을 합쳐 하나의 “정확도”로 보고하지 않는다. J2는 없는 offset을 실행으로 생성할 수 없으므로 추가 실행하지 않았다.

### 실제로 관측한 적용범위 밖 실패

추가 입력은 연구자가 JSON-style 문자열 quoting을 가정한 것이다.

```text
specificword=["]"] status=ok
```

그 추가 문법 아래 기대한 결과는 `specificword=["]"]`이다. 봉인 filter는 `specificword=["]`까지만 출력하고 exit0으로 종료했다. 따옴표 안 `]`를 구조 괄호와 구분하지 못하기 때문이다. 원 R0에는 따옴표·escape 문법이 명시되지 않았으므로 사전 승패를 바꾸지 않지만, 합성 filter가 임의 JSON 문자열 문법에도 적용된다는 확장은 틀렸다. escape에 대해서는 별도 실행하지 않았으며 미확인으로 남긴다. 이 한 가지 경계 관측 후 추가 테스트를 중단했다.

## 사용자·유지관리자·편집자에게 줄 두 링크

### J1

- [배열/변수 binding 및 string interpolation 명세](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml)
- [짧은 join 기반 대안](https://stackoverflow.com/a/79322532)

편집 판단: 기본 공식 manual 링크를 유지하고, 긴 원 시험 링크 대신 짧은 공개 대안 링크를 두 번째에 제시할 수 있다. 사후 링크이며 사전 근거를 대체하지 않는다.

한 가지 확인: 잘린 JSON의 닫힘을 포함한 최소 완전 입력을 줄 수 있는가?

### J2

- [객체 생성 시 input 문맥과 missing key=null 명세](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml)
- [INDEX 대안과 null offset을 숨기지 않은 구체 출력](https://stackoverflow.com/a/79389173)

편집 판단: cat 링크는 완결값을 보충하지 못하므로 사용자용 두 링크에서는 공식 jq 설명+INDEX 출력 대안으로 바꾼다. 채택답/질문자 반응은 outcomes 근거로 보존하되 제품 카드는 offset 결손을 설명한다.

한 가지 확인: offset 수치와 title/artist 정규화 규칙을 포함한 완전 입력을 줄 수 있는가?

### J3

- [공식 range/index/+ 및 while/slice 명세](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml)
- [짧은 _nwise 대안과 문서화된 while 대안이 함께 있는 고정 수정판](https://stackoverflow.com/revisions/8B5D568A-8370-4DA2-8612-FF08869D3144/view-source)

편집 판단: 공식 manual 유지; 두 번째 링크는 수정판 답으로 교체하면 유지관리자가 private 함수 의존과 documented 대안의 차이를 판단할 수 있다. _nwise가 안정 API인 것처럼 단독 추천하지 않는다.

한 가지 확인: 실제 객체의 merge 전 변형과 중복 key 충돌 규칙을 보여줄 수 있는가?

### J4

- [grep의 -P/-o 지원 조건과 출력 경계](https://git.savannah.gnu.org/cgit/grep.git/tree/doc/grep.in.1?h=v3.11)
- [재귀 PCRE의 짧은 명령과 별도 시험 입력/출력](https://stackoverflow.com/a/79426171)

편집 판단: PCRE 지원 및 bracket 문법을 확인할 수 있으면 사용자 카드에는 훨씬 짧은 grep 대안을 제시할 수 있다. 미확인 환경에는 검증된 jq 합성 filter와 공식 manual을 대안으로 남긴다. 사전 B 문서가 재귀 구문 자체를 입증했다고 주장하지 않는다.

한 가지 확인: 모든 대괄호가 균형을 이루고 escape/quoted bracket이 없다는 점과 grep -P 지원을 확인할 수 있는가?

## 재현과 남은 한계

새 checkout에서도 아래 두 명령은 이미 커밋할 짧은 입력 파일과 고정 filter를 사용한다. 전체 Stack Overflow 원문 캐시가 없어도 실행할 수 있다. 다운로드는 시스템 설치 없이 `_cache/` 안에만 저장하며 위 고정 SHA-256을 요구한다.

```bash
python -B docs/workstreams/research/AF-RES-096/evidence/post-jq/prepare_runtime.py
python -B docs/workstreams/research/AF-RES-096/evidence/post-jq/reproduce_runtime.py
```

실제로 실행한 것은 `run_frozen_filters.py`의 12개 기본 검사와 `run_boundary_counterexample.py`의 1개 경계 검사이다. 재현용 두 wrapper는 구문검사만 했으며 동일 시험을 불필요하게 반복하지 않았다. 재현 wrapper는 원 관측과 동일한 결과를 기대한다. 따라서 알려진 잘린 입력의 exit5와 quoted-bracket의 잘못된 조기절단도 관측 일치 대상이다. 원 관측을 덮어쓰지 않고 별도 `reproduction-results.json`에 기록한다.

이 묶음은 사용자 실제 환경에서의 성공, PCRE grep 대안의 연구자 실행, quote/escape/multiline의 모든 조합을 검증하지 않았다. 자료가 지지하는 범위는 공개된 행동, 고정판에서의 연구자 실행, 그리고 그 둘 사이의 구분이다. 특히 문서의 여러 기능을 조합해 완결 코드를 만드는 능력과 검색 노출만으로 완성된 짧은 해법을 찾는 능력은 다른 측정 대상이다. J4의 성공한 합성 filter와 사후 발견한 짧은 grep 답을 함께 남겨 이 차이를 확인할 수 있게 했다.
