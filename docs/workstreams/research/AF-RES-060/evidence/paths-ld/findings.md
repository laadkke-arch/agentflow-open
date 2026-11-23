# 사용자 경로 관측: 7공급자·9요구쌍·27경로

**27경로 모두 미확인이다.** 완결0·부분0·확정오답0은 해당 입력에 대해 구현 성공이나 실패를 입증한 수가0이라는 뜻이다. 진위 판정 가능한 후보 분모가0이므로 정확도는 산출할 수 없다. 또한 SC036의 P3 두 경로는 실제611/500단어 초과 노출 때문에 엄격한 프로토콜을 충족하지 못했다. 이 한계와 조건 미확인이라는 판단은 별도로 기록한다.

## 봉인·범위

- F1 고정판: `412192e28356bee13e4c11f20511ab5ec590662c`. 단계3 요구·순위·경로 배정: `5d01a6208edd9f8a20be7b31f7b545cef2200597`.
- 담당 배정9쌍 전체를 조사했다. JS3/SC040과 LD3/LD008은 해당 조건의 top3 후보다. JS4의5쌍과 JS6의2쌍은 낮은 순위 진단이다. 낮은 순위의 자료를 top3 결과로 끌어올리지 않았다.
- 조건은 봉인된 requirements.json에서 인수했고 원질문을 재선별하지 않았다. 같은 응답을 재사용하지만 각 요구쌍·경로의 논리적 읽기 비용을 따로 센다.
- P1은 첫 제목부터500단어, P2/P3는 같은 첫창에 첫째/둘째 정보링크를 각각 하나만 더한 독립 경로다. F1 기능절 창과 사용자 첫창을 구분했다. 공급자 코드는 실행하지 않았다.

## 요구쌍별 실제 도착 경로

| 요구·후보 | P1 | P2의 두 번째 도착 | P3의 두 번째 도착 | C1/C2·환경·예산 |
|---|---|---|---|---|
| JS-3 / SC-040 | 고정 README500 · 미확인 | [500단어](https://pypi.org/project/json-schema-utils) · directly_read_bounded_window | [500단어](https://github.com/zx80/json-schema-utils) · directly_read_bounded_window | C1/C2/원환경 미확인 |
| JS-4 / SC-035 | 고정 README500 · 미확인 | [500단어](https://github.com/pwall567/jsonutil) · directly_read_bounded_window | [228단어](https://github.com/pwall567/yaml-simple) · directly_read_bounded_window | C1/C2/원환경 미확인 |
| JS-4 / SC-036 | 고정 README500 · 미확인 | [0단어](https://tools.ietf.org/html/draft-wright-json-schema-01) · access_failed | [500단어](http://tools.ietf.org/html/draft-zyp-json-schema-04) · bounded_web_reader_primary_document_excerpt | C1/C2/원환경 미확인; P3 실제611/500 노출 |
| JS-4 / SC-038 | 고정 README500 · 미확인 | [134단어](https://json-schema.org/draft/2019-09/schema) · directly_read_bounded_window | 후속 정보링크 없음 | C1/C2/원환경 미확인 |
| JS-4 / SC-039 | 고정 README500 · 미확인 | [0단어](https://bowtie.report/#/?language=typescript&language=javascript) · no_readable_body_at_selected_destination | [500단어](https://github.com/sagold/json-schema-library/blob/bfc101953f038e2c9ec627f19b64a7aa41d62bd1/README.md#draft-support) · directly_read_bounded_window | C1/C2/원환경 미확인 |
| JS-4 / SC-034 | 고정 README500 · 미확인 | [19단어](https://json-everything.net) · read_html_shell_with_error_placeholder; app_not_executed | [65단어](https://docs.json-everything.net) · directly_read_bounded_window | C1/C2/원환경 미확인 |
| LD-3 / LD-008 | 고정 README500 · 미확인 | [500단어](https://www.w3.org/TR/json-ld11/) · directly_read_bounded_window | [72단어](https://rubygems.org/gems/rdf) · directly_read_package_metadata_only | C1/C2/원환경 미확인 |
| JS-6 / SC-034 | 고정 README500 · 미확인 | [19단어](https://json-everything.net) · read_html_shell_with_error_placeholder; app_not_executed | [65단어](https://docs.json-everything.net) · directly_read_bounded_window | C1/C2/원환경 미확인 |
| JS-6 / SC-036 | 고정 README500 · 미확인 | [0단어](https://tools.ietf.org/html/draft-wright-json-schema-01) · access_failed | [500단어](http://tools.ietf.org/html/draft-zyp-json-schema-04) · bounded_web_reader_primary_document_excerpt | C1/C2/원환경 미확인; P3 실제611/500 노출 |

각 행의 P1/P2/P3는 모두 unconfirmed다. 전체27개 개별 판정·URL·판·hash·직접 위치는 observations.json, 원전 기록20개는 sources.jsonl에 있다. 같은 출처를 반복 사용한 것은 독립 시험 성공으로 세지 않았다.

## 두 조건을 보존했을 때의 해석

### JS3: 외부 gender enum과 Person 필수 필드

SC040의 첫창은 `$ref`를 정의로 치환하는 inline 명령을 설명한다. 그러나 원요구 C1은 외부 참조 해소에 더하여 gender enum이 실제 검증에 적용되어야 하고, C2는 name/surname/sex/email 필수 제약을 유지해야 한다. 같은 창의 check 명령은 jmc/jsonschema/jschon을 사용한다고 적으며 원질문은 Ajv 사용을 직접 묻는다. 전처리 기능의 존재를 원 Ajv 체인의 성공으로 간주하지 않았다. PyPI 두 번째 문서는0.9.24에 같은 소개를 재게시하지만 고정 commit과의 대응도 미확인이다. P3는 원 저장소로 돌아가는 자기링크라 다음 유용한 문서로 건너뛰지 않았다. 근거: P-SC-040-D1/D2/D3.

근접음성은 외부 성별 참조가 해결되어도 required를 제거하여 name 없는 Person을 통과시키는 경우다. 이는 고정 요구의 논리적 시험 제안이며 해당 도구를 실행해 관측한 실패가 아니다. draft04/$id 혼용과 email assertion guard도 자동 교정하지 않았다.

### JS4: 동적 instance 관계와 고정 문자열 enum

이 요구의 C1은 같은 instance에서 columns에 존재하는 이름만 pii에 허용하는 관계다. C2는 column_datatype 값으로 integer/string/object라는 문자열 집합을 허용하는 것이다. 예제에서 JSON 값의 type을 integer/number/string으로 검사하는 일과 C2의 값 집합 제약을 혼동하지 않았다.

SC035는 Product의 number/string/required 검사, SC036은 a=5/빈 객체/a=taco의 저자 기대값, SC038은 숫자와 숫자처럼 보이는 문자열의 구별, SC039는 schema의 원격 `$ref`와 character 길이 예제를 보여준다. SC034의 suite 소개에는 instance/external data 접근 vocabulary가 있지만 실제 동적 조건을 작성·검사하는 예가 없다. 모두 C1·C2의 직접 확인에는 이르지 못했다. 근거: P-SC-034/035/036/038/039-D1과 각 허용 후속.

후속의 역할도 달랐다. SC035는 schema 문서가 아니라 현재 구현에서 이전에 쓰던 jsonutil/yaml-simple로 이동했다. 후자는 유지보수 종료와 YAML 부분 지원을 명시하지만 이를 schema validator의 C1 실패라고 옮기지 않았다. SC038의 meta-schema는 schema 문서를 검사하는 자료여서 application instance의 값 제약 증거가 아니다. SC039의 `$ref`는 schema 주소를 해소하며 instance 내부 값으로 enum을 만드는 것과 다르다. C2를 지키면서 pii가 없는 column을 가리키는 근접음성은 여전히 미실행이다.

Python3.x 연결이 문서에 없다는 사실은 환경 미확인으로 남겼다. Kotlin/Ruby/Lisp/.Net/Node 이름 차이만으로 해당 기능이 영구적으로 불가능하다고 판단하지 않았다. 이름·description·datatype의 값 존재를 어느 빈 값 기준으로 해석할지도 원문에서 명확하지 않아 전체 질문 해결을 선언하지 않는다.

### LD3: framing 명칭과 객체·필드 보존

LD008은 새로 찾은 framing 후보이며 첫 사용자 창에도 그 인터페이스명이 있다. 그러나 첫창의 실제 설명은 streaming과 JSON-LD-star가 중심이다. 첫째 정보링크는 JSON-LD1.1 규격 앞부분, 둘째는 RDF.rb gem 판·Ruby 요구 metadata로 연결된다. a=1인 객체만 남기는 C1과 그 객체의 b/c·credential을 보존하는 C2의 같은 구현판 입력/출력은 없다. 근거: P-LD-008-D1/D2/D3.

streaming writer가 각 statement를 별도 node로 쓴다는 설명을 framing의 필드 손실이라고 단정하지 않았다. 별도 연산에 대한 설명이므로 같은 연산·입력의 반례가 아니다. 고정 요구가 제시한 “a=1 선택은 되지만 b/c 또는 주변 필드는 사라짐”이라는 근접음성을 해당 Ruby 판에서 실행하지 않았다. jsonld.js package 링크가 있던 원환경과 Ruby 대안의 교체 허용도 미확인이다.

### JS6: 데이터 속성 type과 id:string

C1의 데이터 속성명 type 보존과 C2의 id:string 제약을 독립적으로 평가했다. SC034의 창에는 구체적인 object/property string 제약이 없다. SC036은 properties.a.type=integer와 string 입력 거부를 보여준다. a라는 보통 property 이름을 id로 바꾸는 전이와, 문서에서 보지 못한 string 제약으로 integer를 바꾸는 추가 전이는 구분했다. 단지 두조건을 동시에 보여주는 예가 없다는 이유로 부분 판정을 막은 것이 아니다. C2는 원 schema 코드에서 읽은 보존 조건이며 별도 prose 요청이 아니었다. type/id를 required로 만들거나 article을 유일 enum 값으로 제한하거나 uuid description을 format assertion으로 바꾸지 않았다.

근접음성 id=1과 양성 id="1"/"2"는 봉인된 연구자 입력이다. 이 후보들에서 실행하지 않았고 실제 실행 결과로 세지 않았다. Ajv/Drupal10 환경의 연결 여부도 별도 미확인이다. 근거: JS6 요구 원장과 P-SC-034/036 각 경로.

## 접근과 노출 감사

SC034 playground에서 취득한 HTML에는 오류 placeholder가 있지만 앱을 실행해 실제 오류를 관측한 것은 아니다. 문서 landing은 sidebar의 설명·API로 더 들어가라는 안내이며 세 번째 문서를 열지 않았다. Bowtie는 선택된 hash route의 본문을 취득 HTML로 읽지 못했으므로 실제 비교 보고서 결과를 읽었다고 세지 않는다. 이런 제한은 해당 서비스 전체가 고장 났거나 기능이 없다는 주장과 다르다.

SC036 draft6 원URL은 HTTP 취득과 같은 URL 웹리더가 모두 실패했다. draft4는 원 HTTP/HTTPS 및 관측 redirect의 직접 HTTP는403이었지만 같은 원URL 웹리더가 datatracker의 동일 draft를 반환했다. 이때 실제 표시된 preview를 재계수한 결과 본문611단어였다. 지정500을111단어 넘겼으며 초과는 목차에 해당한다. 저장된 주근거를500으로 잘랐다고 실제 예산 준수를 회복한 것으로 처리하지 않는다.

| 영향 경로 | source_id | 실제 노출/한도 | 실제 독해 범위 | 판정·엄격준수 |
|---|---|---:|---|---|
| JS4 / SC036 / P3 | P-SC-036-D3 | 611/500 | 문서 제목·abstract·memo·저작권·목차, 원 reader L27~L98 | unconfirmed 유지; 프로토콜 미충족 |
| JS6 / SC036 / P3 | P-SC-036-D3 | 611/500 | 위와 같은 공유 응답 | unconfirmed 유지; 프로토콜 미충족 |

원 preview는 ietf-retry-receipt.json의 /exposed_excerpts/0에 그대로 남겼다. SHA256 `bee525d0b873bb0f1691d91d35539b212f2c5ecfdfcfb667cc2bfce8b171313b`. audit_preview_exposure.py가 reader line label·링크 marker·heading 문법을 제거하고 whitespace split을 재현한다. preview-exposure.json에 초과111단어 내용·영향 경로·원URL·redirect·단위를 남겼다. 추가 원문 수는0이지만 추가 표시 노출과 창 예산 위반은0이 아니다.

## 비용과 분모

| 측정 | 실제 | 의미 |
|---|---:|---|
| 요구×공급자 | 9 | 배정9쌍 전체 |
| 개별 경로 | 27 | 각쌍 P1/P2/P3 |
| 엄격한 창·문서 예산 준수 경로 | 25 | 두 P3는611/500으로 별도 |
| 논리적 문서 행동 | 44 | missing link는0; 실패·shell 접근은 행동으로 계산 |
| 논리적 지정 창 읽기량 | 17602 | 요구쌍·경로별로 동일 창 반복 비용 포함 |
| 초과 포함 논리적 문서 범위 | 17824 | 두 P3에 각111 초과 추가 |
| 고유 저장 창 읽기량 | 6518 | 같은 파일 self return 중복 제외 |
| 추가 preview 표시 | 611 | 재표시 비용; 이 중111은 지정 창 밖 |
| 새 본문 전송 요청 | 15 | 실패·동일 URL 도구 재시도 포함 |
| 새 metadata 요청 | 2 | 이전 dependency 두 repo의 cutoff commit 해소 |
| 실제 공급자 실행 | 0 | 코드·명령·기대값은 저자 설명으로만 독해 |

원 구현의 진위가 확인된 경로 분모는0이다. 따라서 관측한 확정오답 수0을 오답률0%라고 쓰면 안 된다. 문서 내 조건 확인 완결은0/27경로이며, 조건을 실제로 구현하는 공급자가0개라고 결론 내리지 않는다. 네트워크 요청과 저작 수·창 수·논리적 읽기 비용도 서로 다르다.

## 사후 반대 사례: 비검색은 기능 부재가 아니다

JS4/SC035의 허용 첫창에서 이미 읽은 `P-SC-035-D1`에는 object/properties 구조(29·31행), `name`의 string 제약(36~38행), `JSONSchema.parseFile`과 `schema.validate` 호출(85·88~90행)이 있다. [같은 고정 README](https://github.com/pwall567/json-kotlin-schema/blob/c87e75207da6de1ea4dd65777742020f2d97995b/README.md)의 이 메커니즘에서 보통 property 이름을 id로 바꾸는 것은 JS6 C2를 조건부로 뒷받침할 수 있는 연구자 전이이다. **SC035는 봉인된 JS6 후보에 없으므로 주판정이나 요구쌍 분모에 추가하지 않았다.** 새 문서를 읽거나 F1·질의를 고쳐 얻은 결과도 아니다.

이 반대 사례의 범위는 제한된다. 원래 Product 예제의 id는 number(32~34행)이며 required에도 id/name/price가 들어간다(30행). 따라서 예제 전체가 JS6를 만족한다고 말하거나 그 추가 제약을 복사할 수 없다. id:string 제약으로 새 schema를 작성하는 조건부 전이는 실제 JS6 실행 결과가 아니며, Kotlin 구현을 원 Ajv 웹앱으로 대체할 허용·통합도 확인되지 않았다. 이 기록은 새 권고가 아니라 “검색 결과에 없음 ⇒ 관련 기능도 없음”이라는 잘못된 추론에 대한 반대 자료다. 자세한 경계는 posthoc-nonretrieved-diagnostic.json에 있다.

## 반환 카드와 재개 첫 행동

| 요구 | 현재 카드 | 반환 링크·용도 | 판정을 바꿀 최소 자료 |
|---|---|---|
| JS3 | 재질문·보류 | [원 SC040 저장소](https://github.com/zx80/json-schema-utils)의 전처리 설명은 검토 가능 | 같은 Ajv 체인에서 외부 enum·required·guard를 보존하는 판 고정 예제/결과 |
| JS4 | 재질문·보류 | 후보의 generic validator 소개만으로 동적 관계를 권고하지 않음 | 같은 후보판의 instance 값 비교 API와 datatype enum, Python 연결, 근접음성 결과 |
| LD3 | 재질문·보류 | [원 LD008 저장소](https://github.com/ruby-rdf/json-ld/)에서 framing 이름은 확인 | 동일 frame 실행에서 객체 선택·b/c·credential 보존, 교체 환경 범위 |
| JS6 | 재질문·보류 | .Net/Ruby 대안의 일반 schema 설명만 확인 | type 속성 보존·id:string의 양성/음성, 원 Ajv 환경 연결 |

F1 편집에서 본 다른 창을 주판정에 보태지 않았다. outside-budget-editor-evidence.json은 SC039 Methods 편집창과 LD008 Features 편집창의 경계를 기록한다. 사후 직링크 감도는 이 분담에서 실행하지 않았으며 그 효과를0 또는 성공이라고 꾸미지 않는다.

## 자체 확인과 출판

실제 검토 주체는 같은 세션 분담자 features_ld다. 별도 독립 공급자 실행이나 외부 검토 승인을 주장하지 않는다. 27개 고유(case,catalog,path), 최대2문서, source ID 연결, 저장 창 단어수와 SHA256, 초과영향 두 경로를 재계수했다. 조건별 미확인을 일부 조건의 직접 지원으로 승격하지 않았는지 원문 예시와 다시 대조했다.

출판 대상은 observations.json, sources.jsonl, findings.md, summary.json, document-records.json, prepared-plan.json, first-windows/, second-windows/, preview-exposure.json, ietf-retry-receipt.json, 수집 영수증과 재현 스크립트다. raw/ 전문은 임시 캐시로 유지하되 원격 출판 대상에서 제외한다. 준비 문법 검사가 실제 사용자 경로 준수를 증명한 것은 아니며, 실제 발견한111단어 초과가 최종 상태에 남는다.

## 별도 문맥 검토의 실제 범위

`/root/features_ld/path_evidence_review`가 JS3/SC040, LD3/LD008, JS6/SC034·SC036의4쌍·12경로에서 허용된 비어 있지 않은 창10개를 직접 읽었다. 나머지15경로의 조건을 직접 검토한 것은 아니다. 전체27행의 ID·최대2문서·노출 표시를 별도로 점검했다. 검토자는 네 쌍 모두 C1/C2 미확인 유지에 동의했고, SC036의 속성명 전이와 제약 타입 전이를 구분해야 한다고 확인했다. SC040의 다른 명령과 LD008의 다른 연산에서 본 제한을 해당 조건의 실패로 옮기지 않은 판단도 확인했다.

preview611/500·초과111·SHA256과 영향 두 P3도 재계산해 일치했다. 외부 취득·공급자 실행·파일 변경은 없었다. 상위 문맥을 상속한 같은 세션 분업이므로 눈가림 독립검사라고 부르지 않는다. 상세 범위는 review-evidence.json에 있다.
