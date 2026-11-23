# AF-RES-060 F0 기준선 독립 계산 감사

시각 UTC: 2026-11-23T03:22:46.013654+00:00; 검토자 `/root/authority`. 고정 AF056 결과판 `2f8ec01e6b52bef4fc3cd003b1690383b6496526`의 인수 파일을 사용했다.

**결과: 16/16 비교가 후보 ID·원순번·전체 적중·질의 목록까지 동일하다.** 구조 검사 15/15와 비교 내부 144/144 대조가 통과했다. 새 기능 F1과 2023 질문은 읽지 않았다. 이전 결과를 알고 한 계산 검산이며 블라인드 효과 검증은 아니다.

## 1. 고정 목록과 검색 경계

- JSON Schema 40 + JSON-LD 22 = 62 게시행. 가족별 원순번 1–40/1–22와 고유 ID를 확인했다. 원래 웹 목록 순서를 재조사한 것은 아니다.
- 정확 URL 중복 그룹은 0개였다. 후보에서는 정확 문자열 URL만 첫 적중을 남기는 규칙을 적용했다. query/fragment와 trailing slash를 삭제하지 않았다.
- 검색은 search_fields_json만 사용했다. JSON Schema의 Validator는 validation과 일치하지 않으며 숨은 설명/규격/언어/상류를 검색하지 않았다.
- 37 용어행은 literal 20, V 허용 7, 보류 10이다. validation의 두 매핑은 첫 원장 순서의 JS-V09만 같은 질의어로 남는다.
- casefold, ASCII hyphen→공백, 공백축약 후 연속구의 단어 경계로 OR 적중을 계산했다. 구현 조건은 AND라는 의미 경계를 유지했다.

## 2. 16개 비교 재생

| 비교 | 재생 질의 | 전체 후보·원순번 | 빈 슬롯·사유 | 원장 대조 |
| --- | --- | --- | --- | --- |
| JS-1-L | list of numbers; last element; optional | 관측 0 | 3 · observed_no_match | 동일 |
| JS-1-V | list of numbers; last element; optional | 관측 0 | 3 · observed_no_match | 동일 |
| JS-2-L | validate JSON Schema; primitive type | 관측 0 | 3 · observed_no_match | 동일 |
| JS-2-V | validate JSON Schema; primitive type; meta-schema | 관측 0 | 3 · observed_no_match | 동일 |
| JS-3-L | dependent json-schemas; $ref | 관측 0 | 3 · observed_no_match | 동일 |
| JS-3-V | dependent json-schemas; $ref; schema references; dereferencing | 관측 0 | 3 · observed_no_match | 동일 |
| JS-4-L | schema check; validate; restrict column data type | 관측 0 | 3 · observed_no_match | 동일 |
| JS-4-V | schema check; validate; restrict column data type; validation; enum | SC-032(32) | 2 · matched_pool_exhausted | 동일 |
| LD-1-L | generate the schema dynamically; Breadcrumb Schema; getting appended | 관측 0 | 3 · observed_no_match | 동일 |
| LD-1-V | generate the schema dynamically; Breadcrumb Schema; getting appended | 관측 0 | 3 · observed_no_match | 동일 |
| LD-2-L | show this script only; add more Question and Answers values | 관측 0 | 3 · observed_no_match | 동일 |
| LD-2-V | show this script only; add more Question and Answers values | 관측 0 | 3 · observed_no_match | 동일 |
| LD-3-L | JSON-LD frame; filter only the element; values field filtered | 관측 0 | 3 · observed_no_match | 동일 |
| LD-3-V | JSON-LD frame; filter only the element; values field filtered; framing | 관측 0 | 3 · observed_no_match | 동일 |
| LD-4-L | only call some certain elements; currency ALGYO, and its price | 관측 0 | 3 · observed_no_match | 동일 |
| LD-4-V | only call some certain elements; currency ALGYO, and its price | 관측 0 | 3 · observed_no_match | 동일 |

L 비어 있지 않은 요구 0/8, V 1/8. 채움1+무매치45+풀소진2=48슬롯. 유일한 JS-4-V 후보는 SC-032 원32이고 적중은 게시 제목의 validation이다. 이 검색 재생은 C1/C2 지원이나 Python 환경 대체 가능성을 확인한 것이 아니다.

## 3. 8요구의 의미 경계

| 요구 | 보존할 조건·환경 | 허용/보류 의미 경계 | 근접 음성의 예 |
| --- | --- | --- | --- |
| JS-1 | 가변 길이에서 마지막 이전 number, 마지막 string은 선택적; 전부 number 허용 | items/contains/default를 마지막 위치·선택성의 동일개념으로 자동 추가하지 않음 | [1,"middle",2]는 중간 string 때문에 C1 위반; 빈 배열 기대는 미확인 |
| JS-2 | schema root object; property schema type은 string/number/integer/boolean 한정; draft07 | meta-schema는 schema 검증 연산을 명명할 뿐 property type 네 값 지원을 자동 보장하지 않음 | root object, property {type:"array"}는 C1만 만족 |
| JS-3 | 외부 gender 참조+enum 적용 및 Person 필수 필드; Node/TS, draft04/$id 혼용 | dependencies와 외부 schema references는 다름; 원판 혼용·format guard를 교정하지 않음 | 외부 참조를 해결했어도 name이 빠진 입력은 C2 위반 |
| JS-4 | 동적 columns 이름의 pii 포함관계와 datatype의 고정 세 문자열, Python3 환경과 값 존재 guard | validation은 Validator와 어형 동등하지 않음; enum은 C2 atom이며 동적 C1/값삽입 아님; C++ 후보로 원 Python을 덮지 않음 | datatype=string이나 pii=존재하지 않는 이름이면 C2만 만족 |
| LD-1 | ListItem position/name/item 및 head script 부착; JavaScript/JSP/JSTL/jQuery 노출 | DOM/HTML 생성은 기존 JSON-LD expand/compact/fromRDF 변환과 동일하지 않음 | ListItem은 맞으나 head에 부착하지 않음 |
| LD-2 | 값이 있을 때만 FAQ script 출력; 여러 Question/Answer 쌍 유지; AEM HTL | framing/compaction을 조건부 HTL 반복 출력으로 번역하지 않음 | 두 쌍을 보존해도 빈 값에서 script를 출력하면 C1 위반 |
| LD-3 | a=1 객체만 선택하되 b/c와 credential 필드 유지; jsonld.js 지시 링크와 context1.1 | framing은 허용된 연산명; @nest의 객체 경계/원 runtime/옵션 성공은 미확인 | a=1은 선택하되 b/c 또는 issuer류 원 필드가 사라지면 C2 위반 |
| LD-4 | ALGYO/ACSEL 지정 종목만 선택하고 해당 가격을 PHP 행/표에 매핑 | graph shaping만으로 PHP 출력과 값 경로의 동등성을 가정하지 않음 | 종목은 맞으나 두 가격이 바뀌면 C2 위반 |

예시들은 고정 requirements의 조건을 점검하려고 만든 연구자 예다. 원 질문 본문을 다시 읽거나, 예제 프로그램을 실행하거나, 기존 원문 예시라고 주장하지 않았다. 원문 직접문장/코드 유래의 구분은 인수 requirements의 guard를 유지했다.

## 4. 한계와 재현

같은 F0에서 재생 결과가 맞는다는 것은 F1 편집의 정확성, 미래 후보 순위의 정확성, 실제 두 행동 완결, 역사 모집단 복원 또는 실제 이용자 효용을 보증하지 않는다. 이 검토는 같은 연구팀의 별도 문맥 계산 검산이다. 새로운 공급자 기능 필드가 봉인된 뒤에도 이 기준선 입력을 수정해서 맞추면 안 된다.

정확 입력 SHA256·각 비교의 전체 terms/hits/9개 체크·구조검사·원문 보존 경계는 [baseline-audit.json](baseline-audit.json)에 있다. 모든 산출물은 소유경로만 썼으며 git mutation은 수행하지 않았다.
