# JSON Schema 모집 순서 경계 검토 · 목적지 노출 전

검토자: `/root/authority_records`. 같은 과제 안의 별도 하위 에이전트이며, 독립 외부 검토·다른 모델 평가가 아니다. 부모가 제안한 선정안과 그 사유를 전달받았으므로 선정안 블라인드 검토도 아니다. 구현 목록·공급자 문서·정답 시험·L/V 순위는 보지 않았다. 읽은 것은 `evidence/schema-pre/metadata.json`으로 생성일·ID 정렬한 **1~9위의 최초 body revision만**이다. 답·댓글·추천 수를 선정 근거로 사용하지 않았다.

검토 입력은 `metadata.json`의 2026-11-23T01:26:09.113806+00:00 API 관측과 `revisions-p1.json`의 2026-11-23T01:26:34.429082+00:00 관측이다. 후자의 응답 SHA-256은 `e4bf03863ae78dcf48ef77174a616c826914092cc39c4e6bfa8220ff856f1c3c`다. 아래 표는 이 파일의 원문을 판독한 검토이지 새로운 사용자 질문 표본을 추가한 것이 아니다.

## 권고

**첫 네 적격 요구를 원순위 5·7·8·9로 잡는 안은 허용 가능하다.** 다만 분야 경계를 먼저 명시해야 한다. “JSON Schema의 validation·annotation을 수행하는 구현”을 이번 자료군으로 삼고, 폼 생성·제출 구조 변환·언어 모델 생성은 제외한다. 원순위 2·4는 독립 조건이 없어서가 아니라 이 분야 경계 때문에 제외된다고 기록해야 한다. 코드에 선언된 제약을 필수조건으로 채택하는지 여부도 일관되게 명시한다.

| 원순위·최초판 | 원문에서 읽은 목적·조건 | 선정 판단 권고 | 결과가 달라질 경계 |
| --- | --- | --- | --- |
| 1 · [65574254](https://stackoverflow.com/questions/65574254/folder-reference-for-json-schema), rev1 F271A70D-85E8-422B-B8D8-B2798E3BAAF8 | 폴더를 `$ref`로 가리켜 여러 schema 파일을 참조하려는 목적이다. “optional”은 서술되어 있지만 어떤 입력이 허용·거절되거나 어떤 출력이 생기는지를 별도로 정의하지 않았다. | 제외 가능: 폴더 참조 요청 외에 독립 판정 가능한 두 번째 계약을 확정할 수 없음. | optional을 검토자가 임의로 “필드 누락을 허용” 또는 “파일이 없을 때 성공”으로 번역하면 표본을 인위적으로 채우게 된다. 저자의 추가 정의가 생기면 재판정 가능. |
| 2 · [65597922](https://stackoverflow.com/questions/65597922/how-to-create-a-typical-country-province-or-state-dependency-dropdowns-with-re), rev1 4C219659-5813-490E-8E83-7D711C94A12A | country 선택에 맞춰 province 목록이 변해야 한다. 유효한 선택의 오류가 없어야 하고, 제출값은 중첩 래퍼 없이 개별 값이어야 한다. react-jsonschema-form 안에서 구현하려는 제약이 있다. | **분야 밖으로 제외**: 주된 산출물이 폼 UI·submission 구조이다. 독립 조건이 없다는 제외 사유는 틀림. | JSON Schema를 쓰는 모든 소프트웨어를 모집한다면 이 질문이 먼저 들어와야 한다. 현재 과제는 유효성 검사·주석 처리 자료군이라는 경계를 사용해야 함. |
| 3 · [65635741](https://stackoverflow.com/questions/65635741/json-schema-validator-compatibility), rev1 F3FBBA94-4789-40B8-A711-4FDD3C28ECD3 | 사용자 정의 prohibited와 required·oneOf를 포함한 한 schema가 서로 다른 validator에서 어떻게 해석되는지 묻는다. 두 환경의 예측은 저자가 정답 여부를 질문하는 가설이다. | 제외 가능: 같은 구현·환경에서 함께 성립해야 할 두 목표가 아니라, 다른 환경의 동작을 설명해 달라는 비교 질문이다. | 두 예측을 동시에 요구되는 계약으로 만들면 질문 목적을 바꾼다. “모든 입력 거절”이라는 저자의 추측을 정답 조건으로 고정해서도 안 됨. |
| 4 · [65638877](https://stackoverflow.com/questions/65638877/create-pydantic-model-for-json-schema-having-oneof-reference), rev1 DDB2A5C1-D6CF-480A-9DD6-FA3299D120E5 | 중첩 Pets/Cat·Pets/Dog 참조 구조를 유지하면서 schema를 pydantic 모델로 변환하려 한다. 변환 및 구조 유지라는 목적은 판정 가능하다. | **분야 밖으로 제외**: 코드·모델 생성이지 이번 validation·annotation 구현 요구가 아님. | 변환 요구까지 Schema 자료군에 포함하도록 경계를 넓히면 이 항목도 먼저 선택될 수 있다. JSON-LD 자료군의 변환을 이유로 Schema 자료군 범위를 사후 확장하지 않음. |
| 5 · [65660787](https://stackoverflow.com/questions/65660787/how-to-set-one-schema-for-n-1-elements-and-another-for-the-nth-element), rev1 FF299B83-E209-42FB-BEE4-A732446B5F5B | 가변 길이의 숫자 배열에 마지막 문자열이 선택적으로 올 수 있다. 문자열이 중간에 오는 입력은 거절해야 한다. 양성·음성 배열 예가 모두 있다. | 포함: 두 조건이 저자의 직접 서술과 입출력 예에서 분리된다. | 빈 배열 허용, 최소 숫자 개수, 스키마 초안은 저자가 확정하지 않았다. 임의의 최소 길이를 추가하지 말 것. |
| 6 · [65672597](https://stackoverflow.com/questions/65672597/do-i-have-one-schema-or-two), rev1 AA1484C6-F0C4-42F1-A9E2-DA250189ECE7 | JSON Schema와 Protocol Buffers를 두 schema라고 부를지 두 포맷이라고 부를지 묻는다. | 제외: 용어 구분 질문으로 소프트웨어 입력→출력·허용→거절의 동시 두 목표가 없다. | 실제 변환 기능을 원하는 것으로 재해석하지 않음. |
| 7 · [65699699](https://stackoverflow.com/questions/65699699/validate-json-schema-with-another-json-schema), rev1 9172C932-54A3-4E80-A903-46F7329EFE56 | schema를 입력으로 검증할 때 루트의 type은 object이고, properties 내부 type은 저자가 나열한 string/number/integer/boolean이어야 한다. draft-07 표기가 있다. | 포함: 위치에 따라 다른 type 제약이 직접 명시되어 있다. | 저자가 나열하지 않은 null을 “원시 타입”이라는 넓은 말에서 자동으로 추가하거나, 인스턴스 데이터를 검증하는 질문으로 바꾸지 않음. |
| 8 · [65726164](https://stackoverflow.com/questions/65726164/how-to-use-ajv-with-dependent-json-schemas), rev1 88B51B29-6318-430E-A01F-75D88DB74236 | Node/Ajv에서 두 schema의 외부 참조를 해석하고 Person을 검증하려 한다. 제출 schema는 sex가 외부 gender enum을 따르며 name/surname/sex/email을 required로 선언한다. | 포함 가능: **제출한 schema의 명시 제약도 조건 근거로 인정한다는 규칙** 아래 C1 외부 enum 참조, C2 Person 필수 멤버를 채택한다. prose-only 조건이라고 쓰면 안 됨. | `$schema` draft-04와 `$id`, schema 조각을 꺼내 addSchema/compile하는 원 코드, 미지정 Ajv판을 보존한다. `$id`를 id로 자동 수정하거나 현재 Ajv 기본판을 당시 환경으로 확정하면 틀림. email format 등 다른 제출 제약도 지우지 않음. |
| 9 · [65731152](https://stackoverflow.com/questions/65731152/jsonschema-validate), rev1 C76C0362-B96B-4309-A7D6-38C3BD1F2D62 | pii 값은 동적으로 변하는 columns의 키 안에 있어야 한다. 메타데이터에 값이 있는지 검사하고 datatype을 integer/string/object로 제한하려 한다. | 포함. **C2는 명확히 나열된 datatype enum을 권고**한다. “has a value”는 추가 조건으로 그대로 보존하고 비어 있음의 정의를 미확인으로 두면 해석 위험이 줄어든다. | “has a value”를 자동으로 minLength=1·공백 금지·null 금지 전부로 강화하면 저자 의도를 앞서간다. C1 동적 키 비교와 datatype enum 두 조건은 명시적이다. |

## 일관성 점검

후보가 많이 매치될 것 같은지를 기준으로 위 경계를 정하지 않았다. 범위 사유와 조건 수 사유를 분리하면 폼·모델 생성 요구가 두 조건을 갖고도 제외된 이유를 재현할 수 있다. 원문 코드의 제약을 인정한다는 동일 원칙은 원순위 8에만 특별 적용하면 안 된다. 2·4는 코드 조건을 인정해도 분야 경계로 제외되고, 3은 저자가 묻는 서로 다른 환경의 가설을 하나의 목표로 합치지 않으므로 제외된다.

이 검토의 반대 관점은 넓은 입력→출력 정의를 사용하면 2와 4도 적격이라는 것이다. 그런 경계는 유용한 대안이지만 이번 Schema 자료군의 사전 범위와 다르므로 본표에 섞지 않는다. 경계를 바꾸려면 바뀐 모집 순서와 그로 인해 밀리는 행을 SCOPE의 별도 변경 이력 또는 감도로 남겨야 한다.

이 검토는 원순위 10~40 및 최초판 전체 복원·태그 alias 이력까지 확인한 것이 아니다. API 페이지에서 body가 포함된 최초 revision을 읽었고, 질문 자체의 원래 태그 여부·누락 revision은 부모의 frame 점검 범위다. 직접 원문 검토 수에 9개 질문을 다시 더하지 않는다.
