# 설계자 반환 카드

전체 구현으로 확인되어 반환하는 카드는0개다. 보완 링크와 보류를 구분하며, 아래 추가 공급자 링크는 본표의 두 행동 성공이나 순위로 세지 않는다. 각 카드의 원문 조건은 requirements.json에 고정되어 있다.

## JS-1

- 원문: [65660787](https://stackoverflow.com/questions/65660787/how-to-set-one-schema-for-n-1-elements-and-another-for-the-nth-element)
- 계약: ① 마지막 이전은 숫자만; ② 마지막 문자열은 허용하되 선택적
- 환경/guard: 명시 없음; 가변 n; 빈 배열의 기대는 명시되지 않음
- 반환 결정: 보류. [§6.4.1/6.4.6 정의](https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01.html)는 구현 링크가 아님
- 확인한 경계: 표준 items/contains/default의 범위 차이; 단일 구현의 두 조건 시험 없음
- 반증/누락: 번역 보류; 표제만 충분한 사례 관측0
- 전체 구현으로 올릴 최소 자료: 가변 길이·선택적 마지막 문자열의 같은 구현/판 양성·중간 문자열 음성

## JS-2

- 원문: [65699699](https://stackoverflow.com/questions/65699699/validate-json-schema-with-another-json-schema)
- 계약: ① 대상 schema root type=object; ② property type명은 string/number/integer/boolean만
- 환경/guard: 언어 미명시; 원문 $schema draft-07; null/array/object를 property type에 허용하지 않음; arbitrary latest draft를 추가하지 않음
- 반환 결정: 보완. [§4.3.2](https://json-schema.org/draft-07/draft-handrews-json-schema-01.html); 구현 추천 보류
- 확인한 경계: meta-schema 정의와 enum/type의 차이; 사용자 custom meta-schema 실행 없음
- 반증/누락: 표준명 meta-schema가 고정 게시필드에 없음; 특정 구현 누락은 미입증
- 전체 구현으로 올릴 최소 자료: draft07 custom meta-schema의 root/property 제한을 함께 시험한 고정 구현

## JS-3

- 원문: [65726164](https://stackoverflow.com/questions/65726164/how-to-use-ajv-with-dependent-json-schemas)
- 계약: ① 외부 gender $ref 해결·enum 적용; ② Person 필수 속성 유지·예제 검증
- 환경/guard: Node.js / TypeScript; email format도 source schema에 있음. 형식 assertion 통과는 별도 미확인 guard; literal draft04/$id 혼용을 자동교정하지 않음
- 반환 결정: 보완. [Ajv 고정 참조 문서](https://github.com/ajv-validator/ajv/blob/9050ba1359fb87cd7c143f3c79513ea7624ea443/docs/guide/combining-schemas.md); 당시 Ajv판/URI등록 확인 필요
- 확인한 경계: Ajv v8.17.1의 $ref/등록 설명; 공식 local-ref fixture의 별도 Python3.12.14 / python-jsonschema4.26.0 실행
- 반증/누락: schema references/dereferencing 매치0; 원문 draft04와 $id 혼용을 자동교정 안 함
- 전체 구현으로 올릴 최소 자료: 원 package lock·draft04 처리/기준URI·같은 Person 예제의 외부ref/required/format

## JS-4

- 원문: [65731152](https://stackoverflow.com/questions/65731152/jsonschema-validate)
- 계약: ① pii ⊆ 같은 instance의 동적 columns 키; ② datatype명은 integer/string/object만
- 환경/guard: Python 3.x; 이름·description·datatype에 값이 있어야 한다는 추가 문의를 보존한다. 빈 문자열/null/공백 기준은 미명시이므로 minLength1로 자동번역하지 않는다. 전체 요구를 반환하려면 이 guard도 별도 확인해야 한다.
- 반환 결정: 보완. [SC-032 enum 코드](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/src/json-validator.cpp)는 C2만; 전체 구현 반환 보류
- 확인한 경계: SC-032 build2.4.1의 enum 코드와 C++ C2-only 실제3입력; C1음성은 수락
- 반증/누락: validation 관계의 의미 오류는 미입증; 미확인1을 오탐1로 바꾸지 않음
- 전체 구현으로 올릴 최소 자료: Python환경·동적 columns 제약·값 존재 guard·같은 입력의 두 조건 동시 입증

## LD-1

- 원문: [65565025](https://stackoverflow.com/questions/65565025/how-to-generate-breadcrumb-schema-dynamically-using-javascript)
- 계약: ① 경로 순번·이름·계층 URL을 BreadcrumbList에 보존; ② 생성 script를 head에 부착
- 환경/guard: Javascript 명시; JSP/JSTL 입력 코드와 jQuery ready 호출 노출; C2의 목적 위치 head는 원문 code에서 읽음. 끝 prose는 대상 tag 이름이 비어 있으므로 prose 명시라고 하지 않음. C1은 원하는 출력 예시의 비교 조건이다.
- 반환 결정: 보류. [원문 입력/출력](https://stackoverflow.com/questions/65565025/how-to-generate-breadcrumb-schema-dynamically-using-javascript)을 다음 구현 탐색의 계약으로 반환
- 확인한 경계: Context 정의와 변환 알고리즘; DOM 동적 생성/부착 구현은 미판별
- 반증/누락: 일반 JSON-LD 처리와 DOM 삽입은 동의 아님; 누락 구현 미입증
- 전체 구현으로 올릴 최소 자료: JSP/JS 데이터→ListItem 생성과 head 부착을 함께 보인 구현판

## LD-2

- 원문: [65835110](https://stackoverflow.com/questions/65835110/in-aem-i-want-to-add-sly-sly-tags-inside-a-script-script-tag-multifiel)
- 계약: ① 값이 채워졌을 때만 FAQ script 출력; ② 모든 작성 Q/A 쌍을 반복 보존
- 환경/guard: AEM HTL/Sightly 명시; 단순 script 배치만이 아니라 조건부 데이터 생성과 반복 데이터 보존이 명시되어 모집. Google 검색 노출은 새 필수조건으로 추가하지 않음.
- 반환 결정: 보류. [원문 Q/A 구조](https://stackoverflow.com/questions/65835110/in-aem-i-want-to-add-sly-sly-tags-inside-a-script-script-tag-multifiel); AEM판과 작성값 조건 유지
- 확인한 경계: JSON-LD 문서 생성과 AEM HTL 조건/반복은 다른 층; 공급자 완결 근거 없음
- 반증/누락: 공식 처리기 기능명으로 HTL 조건/반복을 치환하지 않음
- 전체 구현으로 올릴 최소 자료: 사용 AEM판·HTL escaping/조건·반복 산출물의 같은 시행

## LD-3

- 원문: [65917156](https://stackoverflow.com/questions/65917156/how-to-filter-json-ld-object-array-with-json-ld-frames)
- 계약: ① values에서 a=1 객체만 선택; ② 그 b/c와 나머지 credential 필드 보존
- 환경/guard: jsonld package 링크가 digitalbazaar/jsonld.js를 가리킴; 선정 시 링크만 노출, 목적지 미열람; 이후 예산 밖 고정판 진단은 RESULT Q5/Q6; 원 context @version=1.1, 패키지판 미명시, jsonld.js를 PyLD로 교체할 의사 미명시; 같은 값 목록과 같은 객체 식별은 다르다. @nest가 객체 경계를 보존한다고 가정하지 않는다. 최신 패키지 버전을 요구에 추가하지 않는다.
- 반환 결정: 보완. [JS frame](https://github.com/digitalbazaar/jsonld.js/blob/27a2b812267fef702c0ac5260a7555d35c3af005/lib/jsonld.js) / [PyLD frame](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/docs/reference/frame.md); context/옵션/언어조건 포함
- 확인한 경계: jsonld.js9/PyLD3.3 frame 소스; 축소·변경한 연구 fixture에서 a=1 선택과 b/c/issuer 보존 확인; 원 credential 공동시험 미실시. @nest fixture는 예외(exit1)
- 반증/누락: framing은 실제 있으나 LD목록 기능필드가 없어 안 들어옴; 원 입력 완결은 미확인
- 전체 구현으로 올릴 최소 자료: 원 credential remote context 고정판·원 package lock·객체 경계·필드 보존 공동시험

## LD-4

- 원문: [66023851](https://stackoverflow.com/questions/66023851/calling-a-json-file-with-php-but-cant-echo-in-a-way-i-would-like-to)
- 계약: ① 지정 종목만 선택; ② 각 종목과 해당 가격을 PHP 행/표에 짝지음
- 환경/guard: PHP 코드 명시; 문서에서 데이터 추출→출력 요구는 포함한다. graph framing과 PHP 출력이 동의라는 가정은 하지 않는다.
- 반환 결정: 보류. [원 종목·가격 예제](https://stackoverflow.com/questions/66023851/calling-a-json-file-with-php-but-cant-echo-in-a-way-i-would-like-to); PHP출력 구현 추천은 미확인
- 확인한 경계: 프레임 정의와 PHP 선택/행 출력 목적의 차이; 해당 PHP 구현은 미판별
- 반증/누락: 값 선택이라는 관련성만으로 framing 동의어를 추가하지 않음
- 전체 구현으로 올릴 최소 자료: 지정종목 필터와 중첩가격 대응을 같이 검증하는 PHP판/예제
