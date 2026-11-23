# JSON Schema 사용자 경로 결과:17쌍·51경로

**완결0, 부분3, 확정오답0, 미확인48경로**다. 부분3은 JS6::SC005 한 후보의 세 경로가 같은 P1 근거를 공유한 것이다. 고유 요구×공급자 기준으로 부분1/17, 미확인16/17이다. 일부 키워드·원시 동작을 보았다는 사실과 원래 두 조건을 함께 지원한다는 증거를 구분했다.

주판정은 observations.json SHA256 `4610a78575698a34ea52307a260a97a1fd8b55a5e73cdcb407353f9eba15b747`로 2026-11-23T04:11:30.765827+00:00에 고정했다. 이후 루트도 별도 공급자 실행 진단을 수행하지 않았다. 공급자 설치·실행·원문 사용자 성공은 관측하지 않았다.

## 경로별 결과

| 요구 | 공급자 | P1 | P2 | P3 | 남은 핵심 확인 |
|---|---|---|---|---|---|
| JS-1 | SC-004 | 미확인 | 미확인 | 미확인 | 동일판에서 가변 n의 비마지막 위치를 제한하는 schema 예와 위 양성/근접음성의 기대결과를 확인해야 한다. object optionality만으로 대체하지 않는다. |
| JS-3 | SC-027 | 미확인 | 미확인 | 미확인 | 원래 types.json/Person 예와 실제 Ajv 판을 유지한 참조·required·email guard 확인이 필요하다. 다른 엔진 비교를 원질문 완결로 보고하지 않는다. |
| JS-4 | SC-001 | 미확인 | 미확인 | 미확인 | 동일판의 동적 인스턴스 이름 집합 제약과 nested enum fixture 및 Python 통합 조건을 확인한다. |
| JS-4 | SC-006 | 미확인 | 미확인 | 미확인 | CLI dependency 판과 실제 schema·옵션을 고정하고 원문 instance의 동적 이름 대조 및 enum 검사를 수행해야 한다. |
| JS-4 | SC-016 | 미확인 | 미확인 | 미확인 | Everit 자체 고정판에서 두 제약의 사례·부정 입력을 확인하고 Python 대체/호출 조건을 별도 결정한다. |
| JS-4 | SC-021 | 미확인 | 미확인 | 미확인 | 같은 Go판의 동적 데이터 제약과 enum 예, Python 연계 방식을 확인해야 한다. |
| JS-4 | SC-022 | 미확인 | 미확인 | 미확인 | 동일판 callback 예 또는 native keyword로 원래 두 제약을 구현한 양성·근접음성을 추가 예산에서 확인한다. |
| JS-4 | SC-024 | 미확인 | 미확인 | 미확인 | 동일판 동적 관계 및 enum 사례와 원환경 연결을 별도 검토한다. |
| JS-4 | SC-005 | 미확인 | 미확인 | 미확인 | 실제 columns 구조와 동일판 $data/custom keyword의 가능 범위를 고정하고 원자료의 양성·음성을 확인한다. |
| JS-4 | SC-008 | 미확인 | 미확인 | 미확인 | 같은0.0.3의 실제 nested columns schema와 pii 관계 fixture를 원환경 연결 여부와 함께 확인한다. |
| JS-4 | SC-009 | 미확인 | 미확인 | 미확인 | boon 동일판의 실제 enum/instance 관계 사례를 확인한다. Bowtie UI를 읽어도 그 집계만으로 원요구 성공을 대신하지 않는다. |
| JS-4 | SC-023 | 미확인 | 미확인 | 미확인 | 동일판 headless validation의 실제 input/output과 nested enum 및 동적관계 제약을 확인한다. |
| JS-5 | SC-004 | 미확인 | 미확인 | 미확인 | 원문 casing/array-required/trailing comma를 보존한 진단과 별도의 연구자 schema probe를 구별하고 같은판 draft07/conditional 적용을 확인한다. |
| JS-6 | SC-005 | 부분(조건부 전이) | 부분(조건부 전이) | 부분(조건부 전이) | 같은 Ajv판에서 원본 schema와 대비해 properties.type가 데이터 속성으로 처리되는지, id 숫자를 거부하면서 데이터를 바꾸지 않는지 확인한다. |
| JS-6 | SC-008 | 미확인 | 미확인 | 미확인 | 원래 Ajv환경을 유지하거나 교체를 명시한 뒤 같은판 object property 조합의 양성·근접음성을 확인한다. |
| JS-6 | SC-009 | 미확인 | 미확인 | 미확인 | 같은판 object.properties.type/id schema와 Ajv 대체/연결 조건을 직접 확인한다. |
| JS-6 | SC-023 | 미확인 | 미확인 | 미확인 | 고정판 headless 검증 API가 원자료의 type/id를 그대로 받아 numeric id를 거부하는 짧은 예와 원환경 대체 조건을 확인한다. |

## 부분지원의 범위와 감도

Ajv의 고정 첫 창은 object schema 안에 properties.bar:{type:"string"}를 놓고 compile(schema)에 전달하는 예를 보여준다(PS-SC-005-P1, Getting started;289–297,304줄). 일반 속성명 bar를 id로 바꾸는 이름 매개변수 전이만으로 JS6의 독립 C2에 조건부 부분지원을 인정했다. 직접 본 메커니즘과 연구자의 전이를 분리했으며, id 실제 검증·숫자id 거부·원문 schema 보존 성공·id required를 주장하지 않는다. 데이터 property type의 article 값 보존은 독립 C1이며 미확인이다.

P2의 live draft04 설명과 P3의 RFC8927 접근실패는 이 부분지원의 근거가 아니다. 세 경로 모두 같은 고정 P1을 사용한다. literal id 예만 허용하는 감도에서는 부분3→미확인3으로 바뀌어51경로 전체가 미확인이다. 실제 반대 실행을 발견한 차이가 아니라 문서화된 메커니즘을 전이하는 증거 문턱의 차이다. scope-review.md에 별도 검토의 최초 의견과 조건 독립성 정정을 보존했다.

Blaze4J의 standalone scalar enum과 type:string 예는 더 좁게 판정했다. color enum을 column_datatype에 적용하려면 문서에 없는 object/items 조합이 추가되고, root string을 properties.id로 옮기려면 object/property 구조를 추가해야 한다. 원시 기능 근거는 직접 있지만 두 요구의 해당 조건 전체는 미확인이다. 이름/런타임 차이만으로 확정오답을 만들지 않았다.

## 원래 링크를 따른 결과

- SC004의 첫 링크 English는 같은 README 자기 링크, 둘째는 한국어 번역이다. 자기 링크도 실제 두 번째 행동으로 남겼으며 후순위 API 링크로 바꾸지 않았다. 번역은 같은 저작이고 동일500단어라도 언어별 의미량이 같다고 주장하지 않는다.
- SC008의 Overview/Features 내부 fragment는 같은 SHA의 다른500단어 창이다. 첫 창에서 Blaze의 Java wrapper라는 계보를 직접 확인했다. 단계2 F1은 바꾸지 않고 단계4 계보에만 추가한다.
- SC006의 첫 링크는 Ajv 저장소, 둘째는 legacy benchmark다. 공식 repository id35914020으로 epoberezkin/ajv와 ajv-validator/ajv의 동일성을 확인하고 기존 Ajv 응답을 공유했다. CLI가 쓰는 정확한 Ajv판은 첫 경로에서 확인되지 않았고, benchmark의 Ajv6.12.6 결과를 다른 판의 성공으로 쓰지 않았다.
- SC016의 첫 링크는 대체 엔진 json-sKema다. 다른 엔진의 성공 절을 Everit의 근거에 붙이지 않았다. Everit README의 설치1.14.4와 고정판1.14.5, json-sKema 설치0.25.0와 고정판v0.32.0도 구별했다.
- SC022·024는 첫 창에 클릭 가능한 후속 정보 링크가 없다. 코드 URL이나 malformed fence 안의 Markdown을 링크로 승격하지 않았다. 네 경로는 첫 문서까지만 도달하며 원문2개의 읽기비용을 청구하지 않았다.
- RFC8927은403, old latest core는404였다. Bowtie는 app div와JS/CSS만 있는 정적 응답으로 본문0이었다. 이 세 결손을 다른 좋은 링크로 대체하지 않았다. HOME은 루트가 취득한 동일응답을 공유하여 자체 사전 renderer로 재생·독해했다.

## 비용과 분모

| 단위 | 실제 | 해석 |
|---|---:|---|
| 고유 요구×공급자 / 경로 | 17 / 51 | 두 조건 판정의 단위 |
| 첫 공급자 응답 | 12 | 모두 stage2 동일캐시 재사용, 새 네트워크0 |
| 고유 source view | 27 | 같은 문서 fragment·실패 포함 |
| 읽을 수 있는 고유 창 | 24 | 실제 직접 독해한 양성본문 |
| 직접 독해 표시단어 | 9,858 | 고유 창을 한 번씩 센 양; 겹친 문장 자체의 중복 제거는 아님 |
| 성공 응답의 고유 해시 | 22 | 하나의 응답에서 여러fragment가 나올 수 있음 |
| 논리 문서 시도 / 읽힌 창 방문 | 81 / 76 | 요구·경로별 동일응답 재사용/자기링크도 별도로 셈 |
| 논리 표시단어 | 31,325 | 각 경로의 노출량; 실제 연구자 고유 독해량과 다름 |
| 후속 링크 없음 | 4경로 | SC022/024의P2/P3 |
| 후속 접근실패 / 정적본문0 | 3 / 2경로 | 고유실패2URL·고유shell1URL을 경로별로 재사용 |
| 이 분담 네트워크 요청 | 16 | 본문HTTP6+GitHub본문4+동일문서텍스트재취득2+metadata4 |
| 루트 HOME 요청 공유 | 1 | 루트 비용에만 청구, 여기 중복네트워크0 |

이 단계가 직접 읽은 저작은 계보를 합쳐17개다. 이 단계에서 새로 추가한 저작은 benchmark와RFC6901 두 개이며, 공급자/번역/fragment/공식 Test Suite/홈페이지 재열람을 신규 저작으로 부풀리지 않았다. Test Suite 고정판은056이 이미 읽은 e2a68a15…와 같다. 공급자 설명·코드·독립표준은 역할이 다르며, 원저작이 있다는 사실은 해당 구현의 실행 성공을 증명하지 않는다.

정확도는 산출하지 않는다. 완결/확정오답의 진위가 확인된 경로 분모는0이며, 부분·미확인을 음성으로 간주하면 안 된다. 관측한 확정오답0/51은 조사경로의 상태 개수로만 보고한다.

## 반례 탐색과 미확인 경계

- SC004의 optional은 객체 필드 추론으로, JS1의 가변 배열 끝 string 선택성과 다르다. 같은 단어의 매치는 구현 불능의 증거도, 두조건 성공의 증거도 아니다.
- $ref는 주로 schema 참조다. JS4의 같은 instance columns 값에서 이름 집합을 얻는 동작과 구분했다. Ajv $data의 일반 기능도 투영/집합구성 예가 없으므로 C1로 승격하지 않았다.
- 시험군·benchmark에는 버전·구성·관측목적이 있다. Suite 소개는 구현자가 언어별 harness를 만들게 하고 benchmark는 고급 기능을 평가하지 않는다고 밝힌다. 이 자료를 일반 준수→모든설계조건 증명의 반대 자료로 읽되, 특정 구현의 case 실패로 꾸미지 않았다.
- Source comments의 valid/invalid, jema의 기대 boolean, Blaze의 enum 예는 실제 이번 실행과 구분했다. 원래 positive를 통과하고 near-negative에서 틀리는 실제 실행은 이 조사에서 관측하지 않았다.
- 환경은 독립 칼럼이다. Python/Node/Java/CLI의 연결·교체 허가가 미확인이면 그 한계를 남기며 언어 이름만으로 confirmed_wrong을 만들지 않는다. JS6에서는 Ajv 엔진 일치와 정확판/Drupal 통합 미확인을 나눴다.

## 검토·재현·남은 한계

자체 판정 주체는 /root/features_schema다. 별도 문맥 검토자는 같은 모델 계열이며 JS4/JS6의 Ajv/Blaze 여섯 창만 보았다. 일반적인 독립 조사 재현이나 전체51경로의 blind review를 했다고 주장하지 않는다. strict-literal 최초의견과 C2조건 독립성 정정을 보존했다.

prepare_paths.py/prepare_followups.py는 동일 원문에서 경계·링크를 재현한다. HTML comment node의 role=None 때문에 생긴 기계 오류를 D2독해 전에 비요소노드만 건너뛰도록 정정했다(renderer-correction-stage4.json). F1과 링크순서는 바뀌지 않았다. HTML은 static response 기준으로 외부CSS/JavaScript를 실행하지 않았으며, Bowtie 결손과 permalink 등 표시 차이의 한계를 남긴다.

관측 JSON의51행/17쌍·문서최대2·창최대500·원문/창 해시·SC032제외를 검산했다. sources.jsonl과summary.json에서 물리취득·고유창·논리경로 분모를 다시 셌으며 observations의봉인해시는 변하지 않았다. next-checks.md의입력·명령은 후속계획이며 실행결과가 아니다.
