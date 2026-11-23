| 요구 ID·원문 주소 | 필수조건 1·2 | 방법·허용 용어와 근거 절 | 목록 판·검색 필드 | 총 매치·상위 3개 원순번 | 두 번 열어 함께 확인한 구현·판 | 오답·미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| [JS-1](https://stackoverflow.com/questions/65660787/how-to-set-one-schema-for-n-1-elements-and-another-for-the-nth-element) | ① 마지막 이전은 숫자만; ② 마지막 문자열은 허용하되 선택적 | L · `list of numbers`; `last element`; `optional` | Schema `1a415f9d…` · 제목+Validator 기능 표제 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [JS-1](https://stackoverflow.com/questions/65660787/how-to-set-one-schema-for-n-1-elements-and-another-for-the-nth-element) | ① 마지막 이전은 숫자만; ② 마지막 문자열은 허용하되 선택적 | V · L + 추가 없음(정의 동등 관계 보류) | Schema `1a415f9d…` · 제목+Validator 기능 표제 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [JS-2](https://stackoverflow.com/questions/65699699/validate-json-schema-with-another-json-schema) | ① 대상 schema root type=object; ② property type명은 string/number/integer/boolean만 | L · `validate JSON Schema`; `primitive type` | Schema `1a415f9d…` · 제목+Validator 기능 표제 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [JS-2](https://stackoverflow.com/questions/65699699/validate-json-schema-with-another-json-schema) | ① 대상 schema root type=object; ② property type명은 string/number/integer/boolean만 | V · L + [meta-schema](https://json-schema.org/draft-07/draft-handrews-json-schema-01#rfc.section.4.3.2) §4.3.2 | Schema `1a415f9d…` · 제목+Validator 기능 표제 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [JS-3](https://stackoverflow.com/questions/65726164/how-to-use-ajv-with-dependent-json-schemas) | ① 외부 gender $ref 해결·enum 적용; ② Person 필수 속성 유지·예제 검증 | L · `dependent json-schemas`; `$ref` | Schema `1a415f9d…` · 제목+Validator 기능 표제 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [JS-3](https://stackoverflow.com/questions/65726164/how-to-use-ajv-with-dependent-json-schemas) | ① 외부 gender $ref 해결·enum 적용; ② Person 필수 속성 유지·예제 검증 | V · L + [schema references](https://json-schema.org/draft-04/json-schema-core#rfc.section.7.1) §7.1; [dereferencing](https://json-schema.org/draft-04/json-schema-core#rfc.section.7.2.3) §7.2.3 | Schema `1a415f9d…` · 제목+Validator 기능 표제 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [JS-4](https://stackoverflow.com/questions/65731152/jsonschema-validate) | ① pii ⊆ 같은 instance의 동적 columns 키; ② datatype명은 integer/string/object만 | L · `schema check`; `validate`; `restrict column data type` | Schema `1a415f9d…` · 제목+Validator 기능 표제 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [JS-4](https://stackoverflow.com/questions/65731152/jsonschema-validate) | ① pii ⊆ 같은 instance의 동적 columns 키; ② datatype명은 integer/string/object만 | V · L + [validation](https://json-schema.org/draft-07/draft-handrews-json-schema-01#rfc.section.3.1) §3.1; [enum](https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01#rfc.section.6.1.2) §6.1.2 | Schema `1a415f9d…` · 제목+Validator 기능 표제 | 1 · SC-032(원32), —, —; 풀 소진2 | SC-032@d5199551…; P1/P2/P3 모두 미확인; 완결 관측0 | 확정 근접오답0, 미확인 후보1; C++/Python 차이·JSON창 경계 유의 |
| [LD-1](https://stackoverflow.com/questions/65565025/how-to-generate-breadcrumb-schema-dynamically-using-javascript) | ① 경로 순번·이름·계층 URL을 BreadcrumbList에 보존; ② 생성 script를 head에 부착 | L · `generate the schema dynamically`; `Breadcrumb Schema`; `getting appended` | LD `f9e9288d…` · 제목만; 언어/CLI는 소속 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [LD-1](https://stackoverflow.com/questions/65565025/how-to-generate-breadcrumb-schema-dynamically-using-javascript) | ① 경로 순번·이름·계층 URL을 BreadcrumbList에 보존; ② 생성 script를 head에 부착 | V · L + 추가 없음(정의 동등 관계 보류) | LD `f9e9288d…` · 제목만; 언어/CLI는 소속 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [LD-2](https://stackoverflow.com/questions/65835110/in-aem-i-want-to-add-sly-sly-tags-inside-a-script-script-tag-multifiel) | ① 값이 채워졌을 때만 FAQ script 출력; ② 모든 작성 Q/A 쌍을 반복 보존 | L · `show this script only`; `add more Question and Answers values` | LD `f9e9288d…` · 제목만; 언어/CLI는 소속 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [LD-2](https://stackoverflow.com/questions/65835110/in-aem-i-want-to-add-sly-sly-tags-inside-a-script-script-tag-multifiel) | ① 값이 채워졌을 때만 FAQ script 출력; ② 모든 작성 Q/A 쌍을 반복 보존 | V · L + 추가 없음(정의 동등 관계 보류) | LD `f9e9288d…` · 제목만; 언어/CLI는 소속 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [LD-3](https://stackoverflow.com/questions/65917156/how-to-filter-json-ld-object-array-with-json-ld-frames) | ① values에서 a=1 객체만 선택; ② 그 b/c와 나머지 credential 필드 보존 | L · `JSON-LD frame`; `filter only the element`; `values field filtered` | LD `f9e9288d…` · 제목만; 언어/CLI는 소속 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [LD-3](https://stackoverflow.com/questions/65917156/how-to-filter-json-ld-object-array-with-json-ld-frames) | ① values에서 a=1 객체만 선택; ② 그 b/c와 나머지 credential 필드 보존 | V · L + [framing](https://www.w3.org/TR/2020/REC-json-ld11-framing-20200716/#framing) §2.1/2.1.1·4.2·4.3 | LD `f9e9288d…` · 제목만; 언어/CLI는 소속 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [LD-4](https://stackoverflow.com/questions/66023851/calling-a-json-file-with-php-but-cant-echo-in-a-way-i-would-like-to) | ① 지정 종목만 선택; ② 각 종목과 해당 가격을 PHP 행/표에 짝지음 | L · `only call some certain elements`; `currency ALGYO, and its price` | LD `f9e9288d…` · 제목만; 언어/CLI는 소속 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |
| [LD-4](https://stackoverflow.com/questions/66023851/calling-a-json-file-with-php-but-cant-echo-in-a-way-i-would-like-to) | ① 지정 종목만 선택; ② 각 종목과 해당 가격을 PHP 행/표에 짝지음 | V · L + 추가 없음(정의 동등 관계 보류) | LD `f9e9288d…` · 제목만; 언어/CLI는 소속 | 0 · —, —, —; 무매치로 빈슬롯3 | 완결 반환 관측0; 후보0으로 시행 해당 없음 | 오답/미확인 후보 판정 해당 없음(후보0) |

| 요구 ID | L→V 신규·탈락 구현 | 같은 시행의 완결·부분 증감 | 실제 예산 밖에서만 확인한 근거 | 번역 오탐·목록 누락 | 설계자에게 반환할 URL·조건 | 미확인·다음 판별 자료 |
| --- | --- | --- | --- | --- | --- | --- |
| JS-1 | 신규 관측0; 탈락 해당 없음(L항목0) | 반환 완결0→0·부분0→0; 조건 시험은 해당 없음 | 표준 items/contains/default의 범위 차이; 단일 구현의 두 조건 시험 없음 | 번역 보류; 표제만 충분한 사례 관측0 | 보류. [§6.4.1/6.4.6 정의](https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01.html)는 구현 링크가 아님 | 가변 길이·선택적 마지막 문자열의 같은 구현/판 양성·중간 문자열 음성 |
| JS-2 | 신규 관측0; 탈락 해당 없음(L항목0) | 반환 완결0→0·부분0→0; 조건 시험은 해당 없음 | meta-schema 정의와 enum/type의 차이; 사용자 custom meta-schema 실행 없음 | 표준명 meta-schema가 고정 게시필드에 없음; 특정 구현 누락은 미입증 | 보완. [§4.3.2](https://json-schema.org/draft-07/draft-handrews-json-schema-01.html); 구현 추천 보류 | draft07 custom meta-schema의 root/property 제한을 함께 시험한 고정 구현 |
| JS-3 | 신규 관측0; 탈락 해당 없음(L항목0) | 반환 완결0→0·부분0→0; 조건 시험은 해당 없음 | Ajv v8.17.1의 $ref/등록 설명; 공식 local-ref fixture의 별도 Python3.12.14 / python-jsonschema4.26.0 실행 | schema references/dereferencing 매치0; 원문 draft04와 $id 혼용을 자동교정 안 함 | 보완. [Ajv 고정 참조 문서](https://github.com/ajv-validator/ajv/blob/9050ba1359fb87cd7c143f3c79513ea7624ea443/docs/guide/combining-schemas.md); 당시 Ajv판/URI등록 확인 필요 | 원 package lock·draft04 처리/기준URI·같은 Person 예제의 외부ref/required/format |
| JS-4 | SC-032 1개 신규; 탈락 해당 없음(L항목0) | 반환 완결0→0·부분0→0; 후보 미확인0→1 | SC-032 build2.4.1의 enum 코드와 C++ C2-only 실제3입력; C1음성은 수락 | validation 관계의 의미 오류는 미입증; 미확인1을 오탐1로 바꾸지 않음 | 보완. [SC-032 enum 코드](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/src/json-validator.cpp)는 C2만; 전체 구현 반환 보류 | Python환경·동적 columns 제약·값 존재 guard·같은 입력의 두 조건 동시 입증 |
| LD-1 | 신규 관측0; 탈락 해당 없음(L항목0) | 반환 완결0→0·부분0→0; 조건 시험은 해당 없음 | Context 정의와 변환 알고리즘; DOM 동적 생성/부착 구현은 미판별 | 일반 JSON-LD 처리와 DOM 삽입은 동의 아님; 누락 구현 미입증 | 보류. [원문 입력/출력](https://stackoverflow.com/questions/65565025/how-to-generate-breadcrumb-schema-dynamically-using-javascript)을 다음 구현 탐색의 계약으로 반환 | JSP/JS 데이터→ListItem 생성과 head 부착을 함께 보인 구현판 |
| LD-2 | 신규 관측0; 탈락 해당 없음(L항목0) | 반환 완결0→0·부분0→0; 조건 시험은 해당 없음 | JSON-LD 문서 생성과 AEM HTL 조건/반복은 다른 층; 공급자 완결 근거 없음 | 공식 처리기 기능명으로 HTL 조건/반복을 치환하지 않음 | 보류. [원문 Q/A 구조](https://stackoverflow.com/questions/65835110/in-aem-i-want-to-add-sly-sly-tags-inside-a-script-script-tag-multifiel); AEM판과 작성값 조건 유지 | 사용 AEM판·HTL escaping/조건·반복 산출물의 같은 시행 |
| LD-3 | 신규 관측0; 탈락 해당 없음(L항목0) | 반환 완결0→0·부분0→0; 조건 시험은 해당 없음 | jsonld.js9/PyLD3.3 frame 소스; 축소·변경한 연구 fixture에서 a=1 선택과 b/c/issuer 보존 확인; 원 credential 공동시험 미실시. @nest fixture는 예외(exit1) | framing은 실제 있으나 LD목록 기능필드가 없어 안 들어옴; 원 입력 완결은 미확인 | 보완. [JS frame](https://github.com/digitalbazaar/jsonld.js/blob/27a2b812267fef702c0ac5260a7555d35c3af005/lib/jsonld.js) / [PyLD frame](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/docs/reference/frame.md); context/옵션/언어조건 포함 | 원 credential remote context 고정판·원 package lock·객체 경계·필드 보존 공동시험 |
| LD-4 | 신규 관측0; 탈락 해당 없음(L항목0) | 반환 완결0→0·부분0→0; 조건 시험은 해당 없음 | 프레임 정의와 PHP 선택/행 출력 목적의 차이; 해당 PHP 구현은 미판별 | 값 선택이라는 관련성만으로 framing 동의어를 추가하지 않음 | 보류. [원 종목·가격 예제](https://stackoverflow.com/questions/66023851/calling-a-json-file-with-php-but-cant-echo-in-a-way-i-would-like-to); PHP출력 구현 추천은 미확인 | 지정종목 필터와 중첩가격 대응을 같이 검증하는 PHP판/예제 |

## 1. Q1 — 원문 요구, 최초판, 환경

**현재 공개 코호트의16비교에서는 정의 연결이 후보1개를 추가했지만, 두 조건을 한 시행에서 확인한 구현은 늘지 않았다.** 후보가 생긴 JS-4도 미확인이므로 실제 기능 정확도나 번역 오탐률을0으로 추정하지 않는다. 원문 배당과 현재 입력의 비교는 완료했으나 역사적 모집단·별칭 복원 및 원 환경의 구현 완결 판정이 남아 **부분 인계**한다.

[frame.csv](frame.csv)는 생성일 범위2021-01-01~2024-12-31 UTC, 각 현재 canonical tag에서 생성일·ID순40건씩80건을 보존한다. 최초 revision1 본문80/80을 직접 읽었고, 질문의 목적/독립적으로 판정 가능한 두 조건만으로 Schema5·7·8·9위와 LD1·3·5·7위를 골랐다. 여덟 질문은 모두2021년1~2월에 생성됐다. 답변·댓글 내용과 추천 수는 선정 기준으로 사용하지 않았다. 초기 LD metadata 응답의 score/answer_count 일부 노출, Schema 비선정 질문의 후속판 일부 노출은 SCOPE에 공개하고 최초판으로 다시 확인했다. 이를 완전한 맹검 선정이라고 부르지 않는다.

| 요구 | 원문에서 읽은 의미·입출력 | 명시한 환경·판과 추가 보존 조건 |
| --- | --- | --- |
| JS-1 | 모든 마지막 이전 요소는 number이며 중간 string은 거부한다. 마지막 string은 허용하지만 필수는 아니다: 전부 number인 배열도 허용한다. | 언어/제품판 명시 없음; draft07은 정의 비교용이며 요청판으로 가정하지 않음; 가변 n; 빈 배열의 기대는 명시되지 않음 |
| JS-2 | 검증 대상 schema의 root type은 object이다. 그 properties 내 각 property schema의 type 값은 string/number/integer/boolean만 허용한다. | 명시 없음; 원문 $schema draft-07; null/array/object를 property type에 허용하지 않음; arbitrary latest draft를 추가하지 않음 |
| JS-3 | person.sex가 참조하는 외부 types.json#/properties/gender를 같은 검증 체인에서 해결하고 enum 제약을 적용한다. Person의 name/surname/sex/email 필수 속성을 유지하여 example Person 검증을 수행한다. | Node.js / TypeScript; 두 문서가 draft-04를 선언하지만 $id/JSONSchemaType 사용; 불일치 자체 보존; email format도 source schema에 있음. 형식 assertion 통과는 별도 미확인 guard; literal draft04/$id 혼용을 자동교정하지 않음 |
| JS-4 | pii의 값은 해당 instance columns에 실제 존재하는 column 이름으로만 제한한다. column_datatype 값을 integer/string/object 중 하나로 제한한다. | Python 3.x; 명시 없음; 이름·description·datatype에 값이 있어야 한다는 추가 문의를 보존한다. 빈 문자열/null/공백 기준은 미명시이므로 minLength1로 자동번역하지 않는다. 전체 요구를 반환하려면 이 guard도 별도 확인해야 한다. |
| LD-1 | 예시와 같이 각 경로를 position/name/item이 있는 ListItem으로 만들며 순번·이름·계층 URL을 보존한다. 생성한 application/ld+json script를 head에 부착한다. | Javascript 명시; JSP/JSTL 입력 코드와 jQuery ready 호출 노출; 제품판/JSON-LD processingMode 미명시; C2의 목적 위치 head는 원문 code에서 읽음. 끝 prose는 대상 tag 이름이 비어 있으므로 prose 명시라고 하지 않음. C1은 원하는 출력 예시의 비교 조건이다. |
| LD-2 | 값이 채워진 경우에만 FAQ JSON-LD script를 출력한다. 작성자가 추가한 여러 Question/Answer 쌍을 원하는 mainEntity 반복 구조로 보존한다. | AEM HTL/Sightly 명시; AEM 제품판과 JSON-LD 판 미명시; 단순 script 배치만이 아니라 조건부 데이터 생성과 반복 데이터 보존이 명시되어 모집. Google 검색 노출은 새 필수조건으로 추가하지 않음. |
| LD-3 | values에 a=1인 첫 객체만 남기고 두 번째 객체는 제거한다. 선택 객체의 b,c와 문서의 나머지 credential 필드를 보존한다. | jsonld package 링크가 digitalbazaar/jsonld.js를 가리킴; 선정 시 링크만 노출, 목적지 미열람; 이후 별도 고정판 진단은 Q5/Q6; package version 미명시; 사용자 context의 @version=1.1 명시; 같은 값 목록과 같은 객체 식별은 다르다. @nest가 객체 경계를 보존한다고 가정하지 않는다. 최신 패키지 버전을 요구에 추가하지 않는다. |
| LD-4 | 요청한 ALGYO, ACSEL 등 지정 종목만 골라 목록 전체 출력은 제외한다. 선택 종목의 해당 가격(ALGYO 26.14, ACSEL 22.9)을 각 표/행에 짝지어 출력한다. | PHP 코드 명시; PHP/JSON-LD 제품판 미명시; 문서에서 데이터 추출→출력 요구는 포함한다. graph framing과 PHP 출력이 동의라는 가정은 하지 않는다. |

각 질문의 짧은 원문 기능구·URI·정규화는 [vocabulary.csv](vocabulary.csv), 최초 수정 GUID·body hash·태그는 [frame.csv](frame.csv), 원문별 두 조건의 코드/본문 위치는 [Schema 원문 계약](evidence/schema-pre/requirements.json)과 [LD 원문 계약](evidence/ld-pre/requirements.json)에 있다. JS-3의 조건 일부와 LD-1의 head 목적지는 코드에서 읽었으며 모두 저자의 prose 문장이라고 표시하지 않았다. JS-4의 모호한 값 존재 문의를 임의의 minLength=1 또는 자동 보정 요청으로 바꾸지 않았다.

현재 태그 모집은 당시 전체 모집단 복원과 다르다. LD-1/LD-2는 최초판에 json-ld가 없었고 각각2021-01-05와2021-01-21에 추가됐다. 두 글이 기간 중 태그를 가졌다는 기록과 생성 순간 태그를 가졌다는 기록은 구분한다. 현재의 두 tag-synonyms API는 빈 목록이지만 과거 별칭의 부재를 입증하지 않는다. 삭제·태그 제거까지 포함한 당시 유니버스는 미확인이다. 원 본문이 모두 복원되어 동일ID dump fallback은 필요하지 않았지만, 역사 유니버스용 dump 확보는 완료되지 않았다. [PostHistory/TagSynonyms 구조 설명](https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede/2678)은 필요한 필드를 안내하며, 실제2024cutoff 자료를 대신하지 않는다(META-HISTORY-01/02).

범위도 제한한다. LD-1/2는 기존 웹 작성 데이터에서 JSON-LD를 생성하고, LD-4는 JSON-LD에서 값을 추출한다. 세 경우를 JSON-LD 핵심 graph 처리 알고리즘을 요청한 것으로 다시 쓰지 않았다. `expand/compact/flatten`만을 대상으로 한 더 좁은 모집은 별도 사전 표본 설계가 필요하며 이8자리를 사후 교체하지 않는다.

## 2. Q2 — 허용한 정의 관계와 거절한 확장

용어표는 원격 `1f63f0129207904a91ae9e01bb3e48c86415a644`에서 후보 순위 전에 고정했다. 총37행은 literal20·V 허용7·보류10이며 `validation` 중복을 빼면 추가 질의는6개, 질의가 실제 바뀐 요구는4/8이다. L은 casefold·공백·하이픈만 정규화하고 연속 기능구를 단어 경계로 일치시켰다. 검색은 기능구 간 OR이지만 완결 판정은 두 조건과 환경을 함께 요구한다.

| 요구 | V에서 추가한 의미·직접 정의 | 보류한 관계와 이유 |
| --- | --- | --- |
| JS-1 | 추가 없음; 원문 literal 유지 | items는 배열 요소/고정 tuple, contains는 어느 위치 하나의 존재이다. 가변 마지막 위치·선택적 문자열과 동등하지 않다. optional을 default 삽입으로 바꾸지 않는다. |
| JS-2 | [meta-schema](https://json-schema.org/draft-07/draft-handrews-json-schema-01#rfc.section.4.3.2) §4.3.2 | 표준 type 전체에는 array/null/object도 있어 저자의 property type 허용4값보다 넓다. |
| JS-3 | [schema references](https://json-schema.org/draft-04/json-schema-core#rfc.section.7.1) §7.1; [dereferencing](https://json-schema.org/draft-04/json-schema-core#rfc.section.7.2.3) §7.2.3 | properties의 dependencies와 외부 schema URI 참조는 다른 관계다. draft04의 id와 원문의 $id 혼용을 감추지 않는다. |
| JS-4 | [validation](https://json-schema.org/draft-07/draft-handrews-json-schema-01#rfc.section.3.1) §3.1; [enum](https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01#rfc.section.6.1.2) §6.1.2 | datatype는 데이터 자체의 type이 아니라 허용하는 이름 문자열3개다. enum은 C2에만 대응하며 동적 C1은 해결하지 않는다. dependentRequired는 고정 property 의존이므로 보류. |
| LD-1 | 추가 없음; 원문 literal 유지 | 동적 DOM 생성·script 삽입을 expand/compact와 동의라고 정의할 근거 없음. |
| LD-2 | 추가 없음; 원문 literal 유지 | AEM template 조건부 생성/반복은 JSON-LD graph 처리의 동일 기능이 아님. |
| LD-3 | [framing](https://www.w3.org/TR/2020/REC-json-ld11-framing-20200716/#framing) §2.1/2.1.1·4.2·4.3 | framing은 matching/shaping을 가리키지만 값 선택·객체 경계·필드 보존을 보장하는 증거는 별도다. expand/compact/flatten을 대신 쓰지 않음. |
| LD-4 | 추가 없음; 원문 literal 유지 | 특정 값을 골라 PHP 행으로 출력하는 목적과 framing은 관련되더라도 의미 동일성이 입증되지 않음. |

JSON Schema `default`는 주석과 값 삽입을 구분해야 한다. draft07 Validation §10.2를 읽었고, 공급자 확장과 실제 mutation은 Q6에서 따로 대조했다. JSON-LD API §2.1–2.4/§8.1/§8.4의 expansion·compaction은 방향이 반대이며, framing은 별도 Recommendation의 matching/shaping이다. 표준에 이름이 있다는 사실을 공급자 기능 지원 또는 원문 두 조건의 동시 통과로 올리지 않았다.

표준 원장 SCH-STD-VALID20의 초기 위치란은 본문에서 확인한 §7.2.1–2보다 넓게 적혀 있었다. §6.5.4/§9.2를 초기 본문 확인으로 세지 않도록 정정하고 dependentRequired 본문은 사후 SCH-STD-VALID20-RECHECK로 기록했다. 그 용어는 처음부터 보류였으며, 허용 V·질의·후보·판정은 전후 동일하다. 사후에 새 동의어를 추가한 것은 아니다.

## 3. Q3 — 게시된 필드와 편집 단위

두 방법은 같은 [catalog.csv](catalog.csv)의 Schema40행과 LD22행을 사용한다. 목록의 실제 기능 열 부재를 공급자 페이지에서 찾은 기능으로 보충하지 않았다. 공식 목록 둘을 복원할 수 있어 Bowtie/W3C 구현 보고서 대체판은 사용하지 않았다. 목록 담당자는 숨은 설명·지원판을 볼 수 있었지만 공급자 목적지나 외부 시험 성적은 읽지 않은 단계에서 목록을 고정했다. 원문·코드 위치와 화면 대조는 [목록 복원 기록](evidence/catalog-pre/NOTES.md), [대조 영수증](evidence/catalog-pre/live-source-comparison.json)에 있다.

| 항목 | JSON Schema | JSON-LD |
| --- | --- | --- |
| 고정 발행판 | [website@1a415f9d36c34fe0eae271c05f86a459746ed00b](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/data/tooling-data.yaml) | [json-ld.org@f9e9288d7c41db5643386effff1ff2a3fe820237](https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/index.yaml) |
| 순서 | 기본 obsolete 제외, toolingTypes 그룹, 이름 오름차순; Load More를 펼친 앞40 | 언어/CLI 카드 순서, 카드 내부 원배열; 전체22에서 소진 |
| 검색 필드 | 이름·명시 별칭·보이는 기능 분류/기능 필드; 실제 앞40의 기능 표제는 모두 Validator, 명시 별칭0 | 이름·명시 별칭·보이는 기능 필드; 실제 명시 별칭/기능 필드0이므로 이름만 |
| 별도 보존하되 기능구 매칭에서 제외 | 언어·지원 draft·라이선스, modal의 notes/description/compliance/upstream | 언어·CLI 소속, JSON-LD 규격판·WIP; 규격판을 제품 release로 읽지 않음 |
| 대표 목적지 | Source 우선, 없으면 Homepage; 정확 URL만 중복 처리 | 각 게시 항목의 repo href; 정확 URL만 중복 처리 |
| 직접 화면과 소스 대조 | 초기 표시89행의 순서·표시필드89/89 일치; 펼친40은 소스 재현 | 게시22행의 순서·표시필드22/22 일치 |

Schema 원자료282도구 중 기본 obsolete 제외211도구가 분류 중복을 유지한258게시행을 만든다. 이 전체 크기와 앞40의 후보 분모는 다르다. [변환 코드 L49–61, L242–358](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/pages/tools/hooks/useToolsTransform.tsx#L49-L61)의 기본값·정렬·그룹을 복원했고, 실제 브라우저에서 Load More와 modal을 클릭한 것은 **미실시**다. [행 렌더러](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/pages/tools/components/ToolingTable.tsx#L159-L167)와 [modal 링크 순서](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/pages/tools/components/ToolingDetailModal.tsx#L90-L118)를 읽어 목적지를 고정했다. 두 행동은 이 URL 목록을 준비한 뒤의 원문 열람 예산이다. 실제 사용자의 목록 펼치기·modal 열기까지 포함하는 클릭 비용이나 탐색 시간을 측정한 것이 아니다.

LD의 [카드 순서](https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/index.liquid#L80-L90), [소속 규칙](https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/_includes/implementation-card.liquid), [항목 렌더러](https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/_includes/implementation-item.liquid)는 이름·규격판 등을 표시한다. 따라서 `framing`이 실제 구현에 있어도 이름에 없으면 이번 V가 검색할 위치가 없다. 언어 카드 아래 있다는 사실을 기능 동의어로 확장하지 않았다. 제목/분류만으로 각 항목이 명세인지 엔진인지 wrapper인지 확정하지 않고, 원장에 게시 역할과 알려진 상류를 분리했다. 사후 `ajv-cli`·`jsonld-cli`는 다른 엔진을 감싼 인터페이스라는 소스 근거를 Q5에 기록한다.

편집 저작 배당은 두 목록 외에 [Schema 데이터 계약](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/data/tooling-data.schema.json#L291-L295)과 [Add/Modify Tooling 제출 양식](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/.github/ISSUE_TEMPLATE/adding-your-tooling.yml)을 별도 규칙 저작으로 센다. 같은 목록의 YAML·HTML·컴포넌트는 하나로 묶었다. 계약과 양식은 다른 artifact/기능을 가지지만 같은 편집 시스템이므로 독립 편집기관4개라는 주장은 하지 않는다. 더 엄격하게 편집 시스템 단위로 묶으면 이 배당은2/4, 전체 필수 배당은22/24가 된다. 이 경계 민감도와 CAT006 위치 L291 정정은 [원문 감사](evidence/review/source-audit.md)에 공개했다.

## 4. Q4 — 신규 반환, 빈 자리, 밀림과 감도

[matches.csv](matches.csv)는 전체16비교의 모든 매치와 질의를, [slots.csv](slots.csv)는 각 상위3자리를 보존한다. 대소문자·공백·하이픈 정규화 및 구 경계 매칭을 두 방법에 똑같이 적용했다. 정렬을 관련도 점수로 바꾸지 않았고 정확 URL 중복 제거 뒤 발행 순서를 유지했다. 독립적으로 다시 구현한 [순위 감사](evidence/review/ranking-audit.md)의35검사는 통과했다. 감사자는 같은 협업 세션의 별도 문맥이며 외부·인간·맹검 검토자는 아니다.

| 측정 단위 | L | V | 해석 |
| --- | ---: | ---: | --- |
| 비교한 요구 | 8 | 8 | 같은 질문·목록·필드·판·도착 규칙 |
| 비어 있지 않은 반환 요구 | 0/8 | 1/8 | JS-4에서 SC-032가 새로 들어옴; 절대 변화1요구 |
| 비어 있는 반환 요구 | 8/8 | 7/8 | 전체15/16비교가 실제 무매치 |
| 상위3의 채운 자리 | 0/24 | 1/24 | 전체1/48; V의 남은2자리는 매치풀 소진 |
| 확인된 완결 반환 요구 | 0/8 | 0/8 | 관측 변화0; 구현 부재의 증명 아님 |
| 확인된 한 조건 반환 요구 | 0/8 | 0/8 | 예산 밖 C2 시험을 주표에 더하지 않음 |
| 판정할 실제 후보 | 0 | 1 | L의 후보 정확도·오답 판정은 해당 없음 |
| 완결/부분/확정 근접오답/미확인 후보 | 해당 없음 | 0 / 0 / 0 / 1 | 미확인을 확정 오탐으로 바꾸지 않음 |
| 두 방법의 빈 반환 동률 | 7/8쌍 | 7/8쌍 | 동일한7쌍을 중복 합산하지 않음 |
| L 기존 후보가 V 상위3 밖으로 밀림 | 해당 없음 | 해당 없음 | 조건부 분모가 L 후보0; 밀림이 없다는 일반 법칙을 검증하지 못함 |

전체48슬롯은 `observed_no_match`45, `matched_pool_exhausted`2, `filled`1이다. [windows.csv](windows.csv)는 빈 슬롯47행과 실제 행동5행, 합계52행이다. 실제 행동은 독립 시행 P1=1회, P2=2회, P3=2회의 합이며 한 시행에5회를 허용한 것이 아니다. [judgments.csv](judgments.csv)는 빈 비교15행, 본표 시행3행, 예산 밖 C2 진단1행으로19행이다. 같은 시행에서 확보하지 않은 조건을 합친 완결은0이다.

도구 단위로 주표에 들어온 것은 SC-032 하나이고, 검증 엔진도 하나다. 그 의존성인 nlohmann/json을 두 번째 검증 엔진으로 세지 않았다. 도착 응답은 README·공식 소개·meta-schema 세 개이며, 경계가 확정된500단어 창은 두 개다. 두 필수조건 또는 한 조건을 입증한 **예산 안 기여 문서는0**이다. 관련 구현 설명문서1을 기능 입증문서1로 올리지 않는다. 구현 지원을 판단하는 전체 독립 상류의 수를 목록 이름만으로 추정하지 않았다.

사전 지정한 민감도는 `LD-3-V1`의 **framing 제거**와 **상위3→4**다. 각각 원래16비교와 함께 재계산했으며 신규·탈락·완결·부분 변화는 모두 관측0이다. 단, framing은 원래 매치0이고 최대 매치풀도1이므로 이 무변화는 강한 안정성 근거가 아니다. 결과를 본 뒤 `validator`를 허용하면 모든 Validator 표제가 영향을 받을 수 있지만, 어형/역할의 정의 근거와 사전 조건을 새로 고정해야 할 별도 실험이다. 이번 V·순위에는 넣지 않았다. 원문 제목/공식 이름만으로 충분한 요구를80건 모집과8선정 안에서 적극 찾았으나, 선택된8건의 L에서는 관측0이었다. 풀 밖 사례를 끌어와 이 분모를 바꾸지 않았다.

## 5. Q5 — 같은 구현·같은 판·같은 창의 두 조건

SC-032의 대표 URL은 [pboettch/json-schema-validator](https://github.com/pboettch/json-schema-validator)이고 읽은 README 고정판은 [`d5199551f758ba067612979ae32ec35693640ccf`](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/README.md)다. 다음 표의 경로들은 서로 독립된 시행이다. 첫 창의 첫 두 정보 링크를 그대로 사용했고, 더 유리한 세 번째 nlohmann/json 링크로 바꾸지 않았다.

| 시행 | 두 행동의 실제 도착과 판독 창 | C1/C2·같은 판 판정 |
| --- | --- | --- |
| JS-4-V-P1 | 동작1 README 렌더500단어, L3–106 첫 단어까지; 동작2 없음 | C++·draft7·version2·빌드 안내. 동적 columns/pii 제한과 datatype enum 둘 다 미확인 |
| JS-4-V-P2 | 같은 README → 첫 정보 링크 `http://json-schema.org/` → [현재 소개](https://json-schema.org/), web L6–105 렌더500단어 | 일반 소개/커뮤니티 자료. 특정 공급자판의 C1/C2 증거가 아님 |
| JS-4-V-P3 | 같은 README → 둘째 정보 링크 `http://json-schema.org/schema` → [draft2020-12 meta-schema](https://json-schema.org/draft/2020-12/schema) | 동작2회 충족. 제목 없는 JSON의 사전 창 경계 미확인; README의 draft7 표기와 현재 도착판도 다름 |

본문500단어 추출에는 실제 결함이 있었다. v1은 raw Markdown의 제목 기호·fence까지 세어 README/소개가 표시487/479단어에 그쳤다. 같은 고정 응답을 pandoc3.1.11.1 GFM→HTML text node로 다시 계산한 v2는 각각 표시500단어다. 추가13/21단어는 빌드 안내와 행사 정보이며 첫 두 링크·C1/C2·순위·완결0을 바꾸지 않았다. 감사자의 최초 감도-only 권고와 root가 원래 렌더 규칙의 기계적 정정으로 최종 원장에 v2를 적용한 결정을 함께 보존했다. 정정 시점에는 공급자 전체 진단이 이미 노출됐으므로 사전 관측처럼 숨기지 않는다. [v1/v2·해시·위치·31개 검사](evidence/review/window-audit.md)와 [변경 시점](SCOPE.md)을 참조한다. JSON 응답168단어 전체를 허용하는 사후 감도에서도 구현판의 두 조건 근거는 없지만 그 감도를 본표에 소급하지 않았다.

추가 독해에서 [CMakeLists.txt L14](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/CMakeLists.txt#L14)의 build판2.4.1, [enum 구현 L551–560](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/src/json-validator.cpp#L551-L560)을 확인했다. 이 판 정보와 C2 근거는 두 행동 밖이므로 주표 부분 판정으로 올리지 않았다. 공급자 [시험 설명](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/README.md#L271-L280)과 같은 소스의 [known-failures](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/test/JSON-Schema-Test-Suite/known-failures.json)를 함께 확인했다. 포괄적 설명, 하네스의 기대값, 이 판의 실제 실행 성공은 서로 다른 증거다.

예산 밖에서 이름을 구별한 소프트웨어 인터페이스는 SC-032, Ajv, python-jsonschema, jsonld.js, PyLD, ajv-cli, jsonld-cli의7개다. 앞의5개는 별도 실행 코드베이스이고 뒤의2개는 다음과 같이 위임한다. 이것이 서로 독립적으로 개발된 알고리즘5개라는 뜻은 아니다.

| 상류/시험 계보 | 직접 근거와 결론 | 남는 한계 |
| --- | --- | --- |
| ajv-cli → Ajv | [package 의존 범위](https://github.com/ajv-validator/ajv-cli/blob/aa7c5062a2d6a8413fcb1274a8d3bd1a3fda4b54/package.json#L36-L44), [getAjv 코드](https://github.com/ajv-validator/ajv-cli/blob/aa7c5062a2d6a8413fcb1274a8d3bd1a3fda4b54/src/commands/ajv.ts#L24-L42): CLI를 별도 검증 엔진으로 세지 않음 | `^8.0.0`만 확인; 당시 정확 minor·lock 없음 |
| jsonld-cli → jsonld.js | [개발판2.0.1-0 package](https://github.com/digitalbazaar/jsonld-cli/blob/ab35bc8b00dedcd119904f56a8904721188094b1/package.json), [frame 위임 L363–383](https://github.com/digitalbazaar/jsonld-cli/blob/ab35bc8b00dedcd119904f56a8904721188094b1/bin/jsonld.js#L363-L383): processor를 재사용 | `jsonld ^8.3.2`를 조사한 jsonld.js9.0.0 고정 소스판과 합치지 않음 |
| PyLD와 jsonld.js | [PyLD 고정 소스 머리말](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/lib/pyld/jsonld.py): JavaScript 구현에서 이식한 계보. 별도 Python 코드베이스이며 단순 JS wrapper는 아님 | 공급자 저작2개를 독립 알고리즘 계보2개로 오인하지 않음 |
| 여러 구현과 공식 suite | [SC-032 vendored 시험 안내](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/test/JSON-Schema-Test-Suite/README.md), [PyLD 시험 계보](evidence/ld-suppliers/versions.json) | 같은 입력을 재사용한 하네스·목록·보고서의 수를 독립 성공 횟수로 합산하지 않음 |

LD의 jsonld.js9.0.0/PyLD3.3.0에는 frame API가 실제 있지만, 목록의 이름에는 framing이 없어 둘 다 반환되지 않았다. 이는 **기능 필드 누락 진단**이며 원 LD-3를 해결하는 완결 구현 두 개를 발견했다는 뜻은 아니다. 이번 현재 재탐색에서 고정한 판을2021년 질문 당시 설치판으로 소급하지 않는다. Python3를 명시한 JS-4에 C++ 후보가 반환된 환경 차이도 보존한다. 사용자의 교체 허용이 명시되지 않아 완결 추천을 하지 않지만, 언어 차이만으로 `validation` 정의 관계 자체가 틀렸다고 판정하지 않는다.

## 6. Q6 — 처음의 번역과 예상이 틀리는 경우

표준 정의, 공개 시험의 기대 출력, 실제 공급자판 실행을 세 층으로 구분했다. 아래의 공식 양성/근접 음성은 분야별 배당을 채우며 본표 밖 진단이다. 공급자별 모든 suite를 실행했다는 뜻은 아니다.

| 분야·반례 | 직접 읽은 입력·기대값 | 실제 실행과 범위 |
| --- | --- | --- |
| Schema enum | [고정 suite enum L5–21](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/enum.json#L5-L21): enum [1,2,3]에서1 허용/4 거절 | python-jsonschema4.26.0 Draft7에서 해당 쌍 일치. 동적 instance의 키 추출은 시험하지 않음 |
| Schema $ref의 위치 | [local $ref L38–57](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/ref.json#L38-L57): bar=3 허용/true 거절; [enum 속 $ref L231–258](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/ref.json#L231-L258)는 리터럴 데이터 | 작은 local fixture는 실제 일치. JS-3 외부 URI·원 Ajv판·required/email 전체를 시험하지 않음 |
| Schema default | [고정 suite L52–81](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/default.json#L52-L81): maximum3/default5에서 alpha1 허용, alpha5 거절, 누락{} 허용 | jsonschema4.26.0에서 모두 기대와 일치, {} 유지. 주석을 값 삽입과 동의라고 하면 틀림 |
| Schema format | [date 입력쌍 L44–86](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/format-date.json#L44-L86): 2020-01-31/2020-01-32 | 같은4.26.0과schema도 FormatChecker 있으면 true/false, 없으면 true/true. draft 이름만으로 필수 assertion을 판정할 수 없음 |
| LD @nest 양성/근접 음성 | [n006 입력](https://github.com/w3c/json-ld-api/blob/fd4f7eb41f679fb73a54923143c473c3a1d06093/tests/expand/n006-in.jsonld)과 [기대 출력](https://github.com/w3c/json-ld-api/blob/fd4f7eb41f679fb73a54923143c473c3a1d06093/tests/expand/n006-out.jsonld)은 속성 병합; [en01 문자열 입력](https://github.com/w3c/json-ld-api/blob/fd4f7eb41f679fb73a54923143c473c3a1d06093/tests/expand/en01-in.jsonld)은 invalid @nest value 기대 | 공식 fixture 실행 미실시. [n007](https://github.com/w3c/json-ld-api/blob/fd4f7eb41f679fb73a54923143c473c3a1d06093/tests/expand/n007-in.jsonld)의 여러 객체도 한 노드에 합쳐지는 기대 출력은 원래 객체 조합 보존과 다름 |
| LD 방향 반전 | [expand/0002 입력](https://github.com/w3c/json-ld-api/blob/fd4f7eb41f679fb73a54923143c473c3a1d06093/tests/expand/0002-in.jsonld)·[출력](https://github.com/w3c/json-ld-api/blob/fd4f7eb41f679fb73a54923143c473c3a1d06093/tests/expand/0002-out.jsonld), [compact/0002](https://github.com/w3c/json-ld-api/blob/fd4f7eb41f679fb73a54923143c473c3a1d06093/tests/compact/0002-out.jsonld) | 공식 기대값 직접 독해, 실행 미실시. 특정 쌍의 compact 출력=expand 입력 blob은 모든 입력에서 byte 역함수라는 증명이 아님 |

Schema의 실제 소규모 실행14회는 공식 기대값 적용12/12 일치, FormatChecker 없는 통제2회는 모두 true, 입력 mutation 관측0/14다. 실행 환경은 jsonschema4.26.0/referencing0.37.0/jsonschema-specifications2025.9.1이며 [runtime-receipt.json](evidence/schema-diagnostics/runtime-receipt.json)에 입력·해시·출력·시각·종료 코드가 있다. 읽은 FAQ판4.23.0을 실행판4.26.0으로 바꾸어 쓰지 않았다. [Ajv8.17.1 useDefaults](https://github.com/ajv-validator/ajv/blob/9050ba1359fb87cd7c143f3c79513ea7624ea443/docs/guide/modifying-data.md#L155-L217)는 옵션으로 삽입을 할 수 있는 반대 가능성이고, [python-jsonschema4.23 FAQ](https://github.com/python-jsonschema/jsonschema/blob/cfe8a4071672b9652c8f083faed1c4ffa7d67705/docs/faq.rst#L100-L209)는 기본 비변이와 확장을 설명한다. 두 문서의 가능성을 두 실행 성공으로 세지 않았다. [Ajv format 플러그인](https://github.com/ajv-validator/ajv/blob/9050ba1359fb87cd7c143f3c79513ea7624ea443/docs/guide/formats.md#L3-L31), [선택 format-assertion 어휘 시험](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/optional/format-assertion.json)은 초안·어휘·등록·옵션을 분리해야 하는 추가 근거다. 후자의 custom meta-schema 실행은 미실시다.

SC-032@d5199551…와 nlohmann/json3.12.0@55f93686…를 g++14.2.0으로 직접 빌드한 [C++ 진단](evidence/windows/sc032-execution.json)은 C2-only schema의 세 입력을 실행했다. datatype=string은 수락하고 array는 거절했지만, pii=missing_column도 수락했다. 이는 **연구자가 만든 그 schema의 C1 누락**을 보여 주며 라이브러리 전체로 C1을 구현할 수 없다는 증명이 아니다. 원문 columns 배열 각 객체의 열 이름 집합과 pii의 포함관계, Python 환경, 값 존재 guard를 함께 입증하지 못했다. fixture의 원래 키 `desired_full_contract_accept`는 모든 guard가 아니라 분석한 C1/C2만의 oracle였으므로 [해석 정정](evidence/windows/fixture-scope-correction.json)을 남기고 원 입력·출력을 소급 수정하지 않았다.

LD의 실제 실행은 [고정 PyLD3.3.0](https://github.com/digitalbazaar/pyld/tree/3ac1987d9be3648c09b7c7e34865ce82d637e742)와 [연구자 최소 입력2개](evidence/ld-suppliers/minimal-fixtures.json)다. Python3.12.14, lxml6.1.1, cachetools8.0.2, frozendict2.5.1을 기록했고 외부 context 요청은0회였다. 다음 실패를 포함해 관측을 보존한다.

| 실행 | 실제 관측 | 뒤집힌 예상·허용되는 결론 |
| --- | --- | --- |
| PLAN-LD-POS | 별도 노드로 모델링한 values에서 a1/b2/c3 객체 하나와 issuer-A를 함께 반환 | 이 작은 연구자 입력의 C1/C2는 참. 원 credential 전체나 원 jsonld.js 환경의 완결은 아님 |
| PLAN-LD-NEST | 입력·프레임 context의 values 매핑을 @nest로 바꾸자 frame 확장 단계에서 FrameError, 출력 없음 | 단순 C1=false/C2=false 출력이라는 사전 예상이 틀림. 최초 runner exit1을 그대로 유지 |
| DIAG-LD-NEST-CAUSE | expand는 a=[1,4], b=[2,5], c=[3,6]으로 한 노드에 합침. frame 내부 원인은 @requireAll의 colliding keywords | 특정 프레임 표현의 키 충돌과 이 입력의 객체 경계 소실을 구분. 모든 @nest 프레임이 불법이라는 결론은 아님. 후속 exit0은 원인 기록 완료이며 앞 시험의 통과가 아님 |

두 최초 frame 호출과 후속 expand1회/frame 재호출1회는 [최초 실행 출력](evidence/ld-suppliers/execution-attempts/offline-frame.stdout.json), [원인 진단](evidence/ld-suppliers/execution-attempts/nest-cause.stdout.json)에 있다. 원 credential remote context·jsonld.js 실행·W3C 전체 suite·공급자 자체 회귀시험의 실제 통과는 미실시다. 또한 같은 jsonld.js9.0.0의 [JSDoc 기본값 L403–406](https://github.com/digitalbazaar/jsonld.js/blob/27a2b812267fef702c0ac5260a7555d35c3af005/lib/jsonld.js#L403-L406)과 [코드 기본값 L420–425](https://github.com/digitalbazaar/jsonld.js/blob/27a2b812267fef702c0ac5260a7555d35c3af005/lib/jsonld.js#L420-L425)은 embed/requireAll에서 다르다. 이 문서·코드 불일치도 문서 이름만으로 옵션을 확정할 수 없다는 반례이며 JS 실행으로 확인한 것은 아니다.

## 7. Q7 — 전거에서 옮길 수 있는 관계와 옮길 수 없는 보증

도서관2·미술2 실제 개념 레코드를 직접 읽었다. 전거의 선호어/이형어·상하위·연관·역관계·범위 주석은 소프트웨어 용어의 출처와 방향을 관리하는 데 참고할 수 있다. 전거에 이름이 실렸다는 사실은 소프트웨어 구현의 두 조건 통과를 증명하지 않는다. 세부 발췌·응답 hash·접근 실패·편집 매뉴얼 위치는 [authority-records.json](evidence/authority/authority-records.json)과 [Q7 조사](evidence/authority/findings.md)에 있다.

| 개념 URI·직접 연 레코드 | 같은 개념의 다른 표현 | 분리해야 할 관계·반례 |
| --- | --- | --- |
| [LOC Engraving / sh85043995](https://id.loc.gov/authorities/subjects/sh85043995.json) | 선호 Engraving, 이형 Engravings·Line-engraving 등 | 상위 Graphic arts/Prints, 하위 Bamboo engraving 등, 관련 Etching. related를 동의어로 읽으면 안 됨 |
| [LOC Etching / sh85045046](https://id.loc.gov/authorities/subjects/sh85045046.json) | 선호 Etching, 이형 Etchings | 상위 Art/Prints, 하위 Aquatint, 관련 Engraving. 같은 철자의 [sh00005643](https://id.loc.gov/authorities/subjects/sh00005643.json)은 재료 아래 쓰는 주제 세목으로 URI/사용 범위가 다름 |
| [AAT paintings (visual works) / 300033618](https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&subjectid=300033618) | 같은 레코드의 단수 painting (visual work) | Objects 계층의 작품. 제작 행위300054216과 produced by 관계이며 동의어 아님 |
| [AAT painting (image-making) / 300054216](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300054216) | 같은 레코드의 painted (image-making) | Activities 계층의 제작. 작품을 produces하며 coating300161986과 distinguished from; 같은 어근으로 합치면 목적이 달라짐 |

Getty canonical URI는 `http://vocab.getty.edu/aat/300033618`와 `http://vocab.getty.edu/aat/300054216`이다. semantic view의403 뒤 같은 공식 기관의 Full Record Display를 읽었고, 그 HTML을 다른 개념으로 중복 세지 않았다. 레코드가 인용한 Grove/Oxford 등의 원 저작은 직접 열지 않아 추가 배당하지 않는다. [Getty 계층 규칙 §3.1](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.1/), [용어·출처 §3.3](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.3/), [연관 관계 §3.5](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.5/)는 같은 매뉴얼 한 저작으로 묶었다. 가이드 표제 아래의 소속을 동일 개념으로 보는 오류는 Schema의 Validator 표제를 개별 두 조건의 보증으로 보는 오류와 유사하다. 이 유추는 제안이며 L/V 실측 효과가 아니다.

옮길 조건은 개념 URI·정의 절·판·관계 종류·방향·입출력 범위를 함께 남기는 것이다. 동일 개념의 접근점과 넓은말/좁은말/관련어를 분리하고, 소프트웨어에서는 추가로 양성/근접 음성 및 같은 구현판·옵션을 요구해야 한다. 작품/제작 행위, schema/instance, 주석/변이, expand/compact를 관계가 있다는 이유만으로 치환하지 않는다.

## 8. 대안별 적용 조건과 반환 결정

관측은 **이번 게시 필드·40/22행·현재 공개8요구·두 행동 창에서 V가 신규 후보 하나를 만들었지만 사용자가 바로 확인할 완결 증거를 늘리지 못했다**는 범위에 한정된다. 모든 자연 요구나 모든 용어 사전의 효과가 없다는 결론은 아니다. [cards.md](cards.md)는 전체 구현0, 조건부 보완4(JS-2/3/4·LD-3), 보류4(JS-1·LD-1/2/4)로 반환 결정을 분리한다. 보완 링크도 본표 성공으로 세지 않는다.

| 대안 | 적용할 조건 | 이번 자료가 지지하는 것·추가 실험 |
| --- | --- | --- |
| 현재 L 유지 | 허용 기능구가 실제 게시명에 있고 최소 비용이 우선일 때 | 이번8건에서는 빈 반환8건. 다른 풀에서 제목으로 충분한 사례가 나오는지는 미측정 |
| 정의 기반 V를 보조로 사용 | 방향·부정·판·범위가 보존되고 해당 명칭이 게시 필드에 있을 때 | JS-4 후보1증가. validation이라는 넓은 연산명만으로 동적 조건까지 해결한다고 반환하면 안 됨 |
| 목록에 출처 있는 기능 필드/명시 별칭을 편집 | 발행자가 URI·판·관계 방향·소스 링크를 관리할 수 있을 때 | framing이 구현에 있지만 제목만 있는 누락 진단. 필드 자체를 바꾸는 새 요인이므로 별도 사전 고정 비교 필요 |
| 응용층 요구를 나누어 탐색 | DOM/AEM/PHP 출력 등 processor 바깥 조건을 함께 보존할 때 | LD1/2/4에 처리기 명칭을 강제로 대응하지 않고 별도 계층의 구현 근거를 찾을 수 있음. 이번8자리를 대체하지 않음 |
| 조건별 보완 링크 반환 | 전체 구현과 구별하고 충족 조건·미확인 guard·버전을 카드에 명시할 때 | SC-032의 C2, LD-3의 frame/객체 경계, JS-3의 참조 등록 문서처럼 설계자가 검토할 출발점을 제공. 실제 채택/효용은 미측정 |

관점별 증거 링크도 다르다. 요구자는 [자기 원문과 조건 원장](requirements.json) 및 [반환 카드](cards.md)에서 부정 입력·미확인 조건을 확인해야 한다. 목록 편집자는 [고정 게시 필드](catalog.csv), [데이터 계약](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/data/tooling-data.schema.json), [Getty 용어 출처 규칙](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.3/)으로 별칭의 출처와 역할을 관리할 수 있다. 구현 유지보수자는 [조건별 판정](judgments.csv), [C++ 입력/출력](evidence/windows/sc032-execution.json), [PyLD 예측 불일치](evidence/ld-suppliers/execution-attempts/offline-frame.stdout.json)를 통해 동일 입력·판·옵션의 공동시험이 무엇인지 확인할 수 있다. 전거 편집자에게 필요한 것은 [같은 철자·다른 URI 대조](evidence/authority/findings.md)다.

## 9. 원문 배당, 상태와 재현 범위

[sources.jsonl](sources.jsonl)은 실제 열람269행이다. 직접1차190, 접근 실패40, metadata/허가문18, 미러/재수록2, 내부 입력/자체 실행19로 구분했다. 외부 고유 직접1차저작은109개이고, 같은 매뉴얼의 절·공식 suite의 여러 파일·같은 질문의 개정/미러·같은 개념의 RDF/HTML은 중복 계보로 합쳤다. 자체 실행은 외부 원문 저작 수에 넣지 않는다. 숫자와 각 대표 source_id의 원장 행은 [source-counts.json](evidence/source-counts.json), [primary-works.csv](evidence/primary-works.csv), [715개 원장 감사](evidence/review/source-audit-receipt.json)에 있다.

| 필수 배당 | 예정/확보 고유 저작 | 대표 원장 ID·경계 |
| --- | --- | --- |
| 공개 요구 | 8/8 | SCH-Q05/07/08/09, LDQ-01/03/05/07; 추가 모집72질문은 별도 저작이지만 필수8을 대체하지 않음 |
| 목록·별도 편집 규칙 | 4/4 | CAT002·CAT006·CAT007·CAT010; 두 편집 생태계, 같은 시스템으로 묶는 민감도2/4 |
| 표준·공개 적합성 시험 | 4/4 | SCH-STD-VALID07·SD001·LD-STD-API·LD-TEST-01; 표준과 suite는 다르나 시험 파일 여러 개는 한 suite |
| 공급자 판별 자료 | 4/4 | SD009·SD014·LD-SUP-JS-DOC·LD-SUP-PY-DOC; PyLD port 계보 공개, 독립 알고리즘4개 주장 아님 |
| 도서관·미술 개념 전거 | 4/4 | AUTH-LC1/LC2·AUTH-AAT1/AAT2; 각각2개, 추가 LOC세목은 진단 |
| 합계 | 24/24 | 별도 artifact 저작 경계 적용; 편집 시스템 경계 민감도22/24 |

원문 배당의 충족과 과제 전체의 완전 충족은 다르다. 현재 모집80/80 최초판 읽기·선정8/8·비교16/16·슬롯48/48은 관측/계산 완료지만, 당시 tag/alias·삭제 모집단 복원은 미확인이다. 총 목록 상한80에 대해 실제62행은 Schema40+LD의전체22이며 LD18행을 접근 실패로 만들지 않았다. 실제 후보의 미확인1과 빈 비교15를 구별했다. 실행하지 않은 공급자 전체 suite와 원 사용자 환경은 미실시이며, 실행한 최소 입력의 결과를 확대하지 않았다. 실제 독자의 클릭·채택·만족은 미측정이다.

작업 입력판은 계획 기준 `d7e60daf1b5b2c918502c407982566369b7149e3`, 실제 시작 `573a8f1a7cafa90b87bcbb4267e73fee12385bda`, AF-RES-052 HANDOFF `6e6818e345ff8ab9beffd0ea0e1cee9fd6f4ae01`, 읽은 결과판 `3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9`다. [manifest.json](manifest.json)·[SCOPE.md](SCOPE.md)에 고정했다. 이전052/048의 후보 묶음과 Python/remark 문제를 재생해 분모에 더하지 않았다. 이번 python-jsonschema 진단은 새 공식 시험 입력·공급자판의 범위를 밝힌 별도 반례다.

원격 단계는 사전계약 [`628c3309`](https://github.com/laadkke-arch/agentflow-open/commit/628c330941babcb43b636d0a37ecb073b2c9d107) → 모집/용어 [`1f63f012`](https://github.com/laadkke-arch/agentflow-open/commit/1f63f0129207904a91ae9e01bb3e48c86415a644) → 목적지 전 목록/순위 [`b765a189`](https://github.com/laadkke-arch/agentflow-open/commit/b765a189aa2a1f5982a4994fc0476273abbf7127) → 창/판/반례/감사 [`d9fbc7c9`](https://github.com/laadkke-arch/agentflow-open/commit/d9fbc7c9a8a1ee7c4febb1b2f3f3d29c286b8bac)다. 최종 결과판·원격 재열람·session check 실제 출력은 이후 [HANDOFF.md](HANDOFF.md)와 [수용 원장](evidence/acceptance-evidence.json)에서 고정 SHA로 연결한다. 보고서 작성 시점의 미실시 gate를 실행한 것으로 선기록하지 않는다.

재현의 핵심 입력은 frozen frame/vocabulary/catalog/matches/slots, windows/judgments와 각 실행 receipt다. [SELF_CHECK.md](SELF_CHECK.md)는 Q1–Q7별 직접 근거·반례·뒤집힐 조건을 채운다. 같은 팀의 순위/창/원문 교차 검산은 수행했지만 외부 독립 재현이나 인간 검토는 없었다. LD40질문의 최초 본문 해시는 metadata 조인으로 재검증했고 Schema40은 저장된 본문으로 해시를 재계산했으므로,80본문 전체를 감사자가 다시 열어 독립 검증했다는 표현은 쓰지 않는다.

## 10. 가장 중요한 불일치·약점 3건

| 불일치·약점 | 영향받는 주장 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| 현재 canonical-tag 모집과 당시 tag/alias·삭제 유니버스가 다름;8질문 모두2021초, LD3/4건은 응용층 생성/추출 | 역사 모집단의 첫4건·일반적인 문서 변환 요구에서의 효과라는 일반화 | [frame.csv](frame.csv) 80행, [LD tag 이력](evidence/ld-pre/requirements.json), [역사 스키마 설명](https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede/2678); sources META-HISTORY-01/02/F01/F02 | 2024cutoff의 Posts/PostHistory·당시 TagSynonyms 원본/덤프와 삭제·retagged 범위를 확보, 같은 ID 규칙으로 frame 대조 | 원순서/적격 첫4가 달라지면 역사 모집단 결론은 수정. 현재 고정 코호트16비교는 별도로 보존 |
| 용어와 게시 필드의 접점이 좁음; Validator≠validation, LD 기능 열 없음; L후보0·최대풀1 | 용어 연결의 일반 효과·오탐률·밀림·slot4 안정성 | [catalog.csv](catalog.csv) SC001–040/LD001–022, [matches.csv](matches.csv)16행, [순위 감사](evidence/review/ranking-audit.md); CAT002/010·LD-SUP-JS-DOC/PY-DOC | 기능 필드/출처 있는 별칭과 어형/역할 관계를 사전 정의한 별도 대조; 본표 사후 확대 금지 | 같은 의미의 게시명으로 후보와 양조건 증거가 늘거나, 새 근접오답/기존후보 밀림이 관측되면 효과·비용 판단이 바뀜 |
| 본표 구현 미확인·환경/판/guard 결손과 창 추출 정정; P3는 제목 없는 JSON; 최소 fixture가 원 요구 전체를 대신하지 못함 | 동일 구현·판·두 행동 안의 완결 및 정확도 | [windows.csv](windows.csv) P1/P2/P3, [judgments.csv](judgments.csv), [창 감사](evidence/review/window-audit.md), [C++ receipt](evidence/windows/sc032-execution.json), [PyLD exit1](evidence/ld-suppliers/execution-attempts/offline-frame-attempt.json) | 원 Python/jsonld 환경·고정 context/lock·모호한 guard 의미를 확보하고 동일 입력 양성/근접음성을 같은 판·옵션에서 실행; 두 조건 근거가 들어오는 사전 창 필요 | 실제 동일판 두 조건·guard 증거가 허용 창에서 함께 확인되면 완결로 승격. v1/v2 현재 결론은 둘 다0이며 사후 추가 창만으로 승격하지 않음 |

