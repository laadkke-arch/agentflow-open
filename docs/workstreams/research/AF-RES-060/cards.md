# AF-RES-060 반환 카드

반환 등급은 전체 구현 0 / 조건부 보완 1 / 재질문·보류 11이다. 조건부 보완도 원 요청의 성공 보증이 아니다. 아래 구현 링크는 F0 원게시 URL이며 편집용 고정판 URL을 새 클릭 지름길로 제공하지 않는다. 증거 판·경로는 paths.csv와 RESULT 첫 표에서 감사한다.

## JS-1 — 재질문·보류

재질문·보류: [SC-004 @imhonglu/json-schema](https://github.com/imhonglu/new-wheels/tree/main/libs/json-schema); 지원 확정 링크 아님

보존할 요구: C1 가변 배열의 마지막 이전은 number; C2 마지막 string은 선택 사항; 환경 언어·판 미명시.

optional은 객체 필드 추론으로 발견됐다. 가변 마지막 위치와 중간 string 거부를 같은 판에서 보이는 예가 필요하다.

원 요청: [65660787](https://stackoverflow.com/questions/65660787/how-to-set-one-schema-for-n-1-elements-and-another-for-the-nth-element). 원문 위치·prose/code 구분·양성/근접음성은 requirements.json의 JS-1.

## JS-2 — 재질문·보류

[원 요청](https://stackoverflow.com/questions/65699699/validate-json-schema-with-another-json-schema)으로 재질문·보류; 반환할 구현 없음

보존할 요구: C1 schema 인스턴스의 root type=object; C2 property schema type은 네 primitive만; 환경 draft-07; 언어 미명시.

meta-schema라는 정의 기반 질의에도 후보가 없다. schema-as-instance의 두 위치 제약을 보이는 구현·판이 필요하다.

원 요청: [65699699](https://stackoverflow.com/questions/65699699/validate-json-schema-with-another-json-schema). 원문 위치·prose/code 구분·양성/근접음성은 requirements.json의 JS-2.

## JS-3 — 재질문·보류

재질문·보류: [SC-027 jschon](https://github.com/marksparkza/jschon), [SC-040 json-schema-utils](https://github.com/zx80/json-schema-utils); 지원 확정 링크 아님

보존할 요구: C1 외부 gender $ref 해소와 enum 적용; C2 Person 필수 네 필드 보존; 환경 Node/TypeScript·Ajv; draft04/$id 혼용.

SC-027의 $ref 및 SC-040의 인라인은 하위 기능 근거다. Ajv에서 외부 enum 적용과 Person required 보존이 연결된 예가 없다. draft04/$id와 email guard도 남는다.

원 요청: [65726164](https://stackoverflow.com/questions/65726164/how-to-use-ajv-with-dependent-json-schemas). 원문 위치·prose/code 구분·양성/근접음성은 requirements.json의 JS-3.

## JS-4 — 재질문·보류

재질문·보류: [SC-001 @cfworker/json-schema](https://github.com/cfworker/cfworker/blob/master/packages/json-schema/README.md), [SC-005 ajv](https://github.com/ajv-validator/ajv), [SC-006 ajv-cli](https://github.com/ajv-validator/ajv-cli); 지원 확정 링크 아님

보존할 요구: C1 pii 이름은 현재 columns에 존재; C2 column_datatype∈integer/string/object; 환경 Python3; 값 존재의 의미 미명시.

동적 instance 이름 집합과 정적 enum을 나눠 확인해야 한다. 일반 validate/준수 주장 및 다른 런타임은 원 Python 요구의 공동 성공 근거가 아니다.

원 요청: [65731152](https://stackoverflow.com/questions/65731152/jsonschema-validate). 원문 위치·prose/code 구분·양성/근접음성은 requirements.json의 JS-4.

## LD-1 — 재질문·보류

[원 요청](https://stackoverflow.com/questions/65565025/how-to-generate-breadcrumb-schema-dynamically-using-javascript)으로 재질문·보류; 반환할 구현 없음

보존할 요구: C1 breadcrumb 순번·이름·계층 URL 보존; C2 ld+json script를 head에 부착; 환경 JavaScript/JSP/JSTL.

JSON-LD 표현 변환은 breadcrumb 유도와 DOM head 부착을 대신하지 않는다. 원 JSP/JS 입력과 생성·부착 코드가 필요하다.

원 요청: [65565025](https://stackoverflow.com/questions/65565025/how-to-generate-breadcrumb-schema-dynamically-using-javascript). 원문 위치·prose/code 구분·양성/근접음성은 requirements.json의 LD-1.

## LD-2 — 재질문·보류

[원 요청](https://stackoverflow.com/questions/65835110/in-aem-i-want-to-add-sly-sly-tags-inside-a-script-script-tag-multifiel)으로 재질문·보류; 반환할 구현 없음

보존할 요구: C1 AEM 입력이 있을 때만 FAQ script; C2 여러 Question/Answer 값 보존; 환경 AEM/HTL; 제품판 미명시.

framing을 AEM 존재 조건/HTL 반복 출력으로 확장하지 않는다. 빈 입력과 복수 Q/A의 실제 template 출력이 필요하다.

원 요청: [65835110](https://stackoverflow.com/questions/65835110/in-aem-i-want-to-add-sly-sly-tags-inside-a-script-script-tag-multifiel). 원문 위치·prose/code 구분·양성/근접음성은 requirements.json의 LD-2.

## LD-3 — 재질문·보류

재질문·보류: [LD-008 JSON-LD for RDF.rb](https://github.com/ruby-rdf/json-ld/); 지원 확정 링크 아님

보존할 요구: C1 values에서 a=1 객체 선택; C2 선택 객체 b/c와 나머지 credential 보존; 환경 jsonld.js; 판·processingMode 미명시.

Ruby의 framing 이름은 발견했지만 원 jsonld.js에서 a=1 선택과 b/c·나머지 문서 보존은 미확인이다. 별도 경로의 성공 절을 합치지 않는다.

원 요청: [65917156](https://stackoverflow.com/questions/65917156/how-to-filter-json-ld-object-array-with-json-ld-frames). 원문 위치·prose/code 구분·양성/근접음성은 requirements.json의 LD-3.

## LD-4 — 재질문·보류

[원 요청](https://stackoverflow.com/questions/66023851/calling-a-json-file-with-php-but-cant-echo-in-a-way-i-would-like-to)으로 재질문·보류; 반환할 구현 없음

보존할 요구: C1 ALGYO/ACSEL 항목 선택; C2 종목과 26.14/22.9 가격 대응 보존; 환경 PHP; 판 미명시.

선택과 PHP 출력은 graph 재구조화의 동의어가 아니다. 두 종목/가격 경로의 원 환경 예가 필요하다.

원 요청: [66023851](https://stackoverflow.com/questions/66023851/calling-a-json-file-with-php-but-cant-echo-in-a-way-i-would-like-to). 원문 위치·prose/code 구분·양성/근접음성은 requirements.json의 LD-4.

## JS-5 — 재질문·보류

재질문·보류: [SC-004 @imhonglu/json-schema](https://github.com/imhonglu/new-wheels/tree/main/libs/json-schema); 지원 확정 링크 아님

보존할 요구: C1 root employee이면 각 user에 batchId 요구; C2 firstName/lastName 필수 문자열 유지; 환경 draft-07; 런타임 미명시.

required를 포함한 필드 추론명이 검색됐지만 root 값 조건과 nested item required의 공동 지원은 미확인이다. userType/usertype 혼용과 원 코드 오류를 먼저 구분한다.

원 요청: [76598757](https://stackoverflow.com/questions/76598757/json-schema-if-then-else-validation-for-array). 원문 위치·prose/code 구분·양성/근접음성은 requirements.json의 JS-5.

## JS-6 — 조건부 보완

조건부 보완: [SC-005 ajv](https://github.com/ajv-validator/ajv); C2 이름 전이만

보존할 요구: C1 데이터 속성 type=article 허용; C2 기존 id:string 제약 유지; 환경 Ajv 판 미명시·Drupal10.

Ajv README의 properties.bar.type=string 및 compile(schema)를 id로 이름만 바꾸는 조건부 보완이다. type라는 데이터 이름의 처리와 id 숫자 거부·데이터 불변성은 미실행이며, 원 Ajv판/Drupal 통합도 미확인이다.

원 요청: [76601421](https://stackoverflow.com/questions/76601421/json-schema-for-jsonapi-how-to-add-type-keyword-for-jsonapi-type). 원문 위치·prose/code 구분·양성/근접음성은 requirements.json의 JS-6.

## LD-5 — 재질문·보류

[원 요청](https://stackoverflow.com/questions/76620107/why-is-conversion-from-json-ld-to-turtle-in-rdflib-not-working)으로 재질문·보류; 반환할 구현 없음

보존할 요구: C1 Windows 로컬 JSON-LD→Turtle; C2 context를 쓰는 Turtle→JSON-LD; 환경 Python3.11/RDFLib6.3.2.

표준 RDF dataset 입출력은 Turtle text parser/serializer 및 Windows 경로 처리를 포함하지 않는다. 원 RDFLib6.3.2의 로컬 파일과 양방향 fixture가 필요하다.

원 요청: [76620107](https://stackoverflow.com/questions/76620107/why-is-conversion-from-json-ld-to-turtle-in-rdflib-not-working). 원문 위치·prose/code 구분·양성/근접음성은 requirements.json의 LD-5.

## LD-6 — 재질문·보류

[원 요청](https://stackoverflow.com/questions/76653659/error-parse-error-trailing-garbage-how-do-i-get-content-of-script-type-a)으로 재질문·보류; 반환할 구현 없음

보존할 요구: C1 R에서 ld+json script 내용 추출; C2 복수 본문 파싱·가격/설명 보존; 환경 rvest/xml2/jsonlite/dplyr 판 미명시.

HTML script 추출과 복수 JSON 텍스트 파싱은 각각 확인해야 한다. 단일 JSON-LD expansion/framing 이름으로 R 처리 흐름을 대체하지 않는다.

원 요청: [76653659](https://stackoverflow.com/questions/76653659/error-parse-error-trailing-garbage-how-do-i-get-content-of-script-type-a). 원문 위치·prose/code 구분·양성/근접음성은 requirements.json의 LD-6.

## 사용·중단 조건

한 경로·같은 구현판에서 C1/C2와 환경·guard가 직접 확인되면 전체 구현으로 올릴 수 있다. 지금은 그러한 후보가 없다. JS-6의 이름 매개변수 전이를 허용하지 않는 사용처에서는 조건부 카드도 보류한다. 기능명만 보고 설치·런타임 교체·데이터 변형을 승인하지 않는다. 후속 명령은 evidence/next-checks/README.md에 있으며 모두 미실행 계획으로 표시했다.
