# 같은 경로의 직접 근거 범위 검토

검토자: `/root/features_schema/path_scope_review`, 같은 모델 계열의 별도 문맥. 새 원문 열람이나 파일 수정은 하지 않았다. 검토자는 고정 JS-4/JS-6 요구와 다음 여섯 사용자 창만 읽었다: SC008-P1, SC005-P1, PS-BLAZE4J-OVERVIEW, PS-BLAZE4J-FEATURES, PS-AJV-DRAFT04 및 Ajv P3의 접근실패 사실. 이는 전체51경로의 독립 재조사가 아니다. 조사자의 잠정 해석과 루트의 판단 기준을 전달했으므로 blind review라고 주장하지 않는다.

## 최초 의견

literal-example-only 기준에서는 두 후보의 세 경로 모두 C1/C2 직접 사례가 없다고 보았다. Blaze의 standalone enum/string 예와 Ajv의 object property 예는 원시/관련 메커니즘이고, 실제 원문 입력 실행·원문 사용자 성공·확정 근접오답은 관측하지 않았다는 점을 확인했다.

## 조건 독립성에 대한 정정

최초 의견 중 JS6 C2를 확인하려면 데이터 property `type`도 공존해야 한다는 표현은 C1을 C2에 끌어오는 과한 요구였다. 조사자와 루트가 독립 C2(id:string) 경계를 재검토했고 검토자도 이를 정정했다.

Ajv P1의 Getting started, SC-005-P1.txt 289–297줄과304줄은 `properties.bar:{type:"string"}`을 포함한 object schema와 `ajv.compile(schema)`를 보여준다. **bar→id라는 일반 속성명 매개변수만 바꾸는 조건부 전이**는 같은 object/property/string 구조를 유지한다. 주판정에서는 JS6 C2의 문서화된 메커니즘에 의한 조건부 부분지원으로 인정한다.

- 직접 본 것은 bar의 메커니즘이며 id 전이는 연구자의 추론이다.
- id 검증 호출/결과, numeric id 거부, 원래 사용자 schema에서의 보존 성공은 보지 않았다.
- 원래 sample의 `required:["foo"]`를 id required로 옮기지 않는다.
- 데이터 property `type`의 article 값 보존은 독립 C1이며 계속 미확인이다.

따라서 JS6::SC005 P1/P2/P3가 같은 P1 증거를 공유한 부분3경로다. literal id 예만 허용하는 stricter sensitivity에서는 셋 모두 미확인이다. 이는 반대 실행 증거가 아니라 증거 전이 문턱의 감도다.

## Blaze와의 구분

Blaze의 `type:string`은 전체 scalar instance에 적용된다. object의 `properties.id`로 바꾸려면 보이지 않은 object/property 구조를 추가해야 한다. 이는 Ajv의 평범한 속성명 변경과 다른 추론량이다. enum colors→column_datatype도 중첩 properties/items 조합이 추가되어야 하므로 주판정에서 원시기능 근거로만 남겼다. 색 이름을 datatype 이름으로 바꾼다는 사실 자체보다 적용 구조가 없는 것이 핵심 한계다.

## 관측하지 않은 것

실제 공급자 실행, 설치, 새 목적지, F1 편집창의 예산 밖 본문, 루트의 사후 실행 진단을 이 검토에 쓰지 않았다. 다른 런타임이라는 이유만으로 confirmed_wrong을 만들지 않았다. comments의 valid/invalid와 example code는 저자의 기대 동작으로 기록했다.
