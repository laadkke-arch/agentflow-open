# 미실행 확인 입력과 명령

아래는 현재 두 문서 주경로의 근거를 대신하지 않는 **후속 계획**이다. 설치·공급자 실행은 수행하지 않았다. 원래 질문의 잘못된 fragment/casing/trailing comma를 자동 교정한 성공으로 보고하지 않는다.

## JS6 Ajv: 조건부 전이와 실제 입력 확인의 경계

주판정에서 확인한 것은 고정판 README의 object.properties.bar 문자열 제약을 id라는 일반 속성명으로 옮기는 메커니즘이다. 다음 최소 입력으로 직접 id 동작을 별도 진단할 수 있다.

```json
{
  "label": "researcher_constructed_C2_only_not_original_user_schema",
  "schema": {
    "type": "object",
    "properties": {"id": {"type": "string"}}
  },
  "positive": {"id": "abc"},
  "near_negative": {"id": 42},
  "expected": [true, false],
  "unspecified": ["id is not made required", "no UUID assertion added"]
}
```

독립 C1의 데이터 이름 보존을 확인할 때는 위 C2 입력과 혼합했다고 말하지 말고 다음 별도 joint probe를 명시한다.

```json
{
  "label": "researcher_constructed_joint_probe_unrun",
  "schema": {
    "type": "object",
    "properties": {
      "type": {"type": "string"},
      "id": {"type": "string"}
    }
  },
  "positive": {"type": "article", "id": "abc"},
  "near_negative": {"type": "article", "id": 42},
  "expected": [true, false],
  "preservation_check": "input before/after deep equality; do not rename/remove type or coerce id",
  "not_added": ["required keys", "article-only enum", "UUID format"]
}
```

재개자는 별도의 checkout에서 다음 명령으로 **먼저 판과 현재 위치를 확인**해야 한다. 이 문서 작성자는 명령을 실행하지 않았다. 실제 checkout 경로와 런타임/의존 설치 방법을 결정한 뒤 실행하며, 그 결과는 현재51경로 밖 진단이다.

```sh
git -C /ABSOLUTE/PATH/TO/AJV_CHECKOUT rev-parse HEAD
git -C /ABSOLUTE/PATH/TO/AJV_CHECKOUT show 9050ba1359fb87cd7c143f3c79513ea7624ea443:package.json
node --version
```

원하는 판은 `9050ba1359fb87cd7c143f3c79513ea7624ea443`이다. 다른 판·다른 기본 옵션으로 실행한 결과를 고정판 성공으로 쓰지 않는다. 실제 사용할 command/script와 의존 lock·입력·출력을 실행 주체가 함께 보존해야 한다.

## 나머지 미확인 조건의 최소 대비 입력

| 요구 | 양성 | 한 조건만 깨는 가까운 음성 | 아직 필요한 자료 |
|---|---|---|---|
| JS1 | `[3,4,5,"hello"]`, `[3,4,5]` | `[3,"hello",4,5]` | 가변 마지막 위치 제약의 같은판 구현/예; 객체 optionality로 대체 금지 |
| JS3 | 원문 types.json gender enum에 속한 sex 및 Person의 원래 네 required 속성 | 같은 외부 참조를 해결하되 name만 제거 | 원문 Ajv판·draft04/$id 혼용·email guard를 보존한 실행 또는 예 |
| JS4 | 원문 columns에 실제 있는 이름만 pii에 사용하고 datatype 세 값 중 하나 | datatype은허용값string 그대로, pii만 실제 없는 이름으로 변경 | 동적 이름 투영과 nested enum의 같은판 구현; Python 연계/교체 조건 |
| JS5 | 원문 employee 조건에서 firstName/lastName 문자열과 batchId 존재 | 두 이름은문자열인 채 batchId만 제거 | userType/usertype·array required·trailing comma 원본 진단을 먼저 분리; draft07/conditional 지원 |

## 취득·표시 결손

- `https://datatracker.ietf.org/doc/rfc8927/`: 이 조사 HTTP403. 재개 시 같은 원링크가 실제로 열리는지를 확인하고 응답판·500단어 창을 새 진단으로 보존한다. 다른 URL로 교체한 효과는 주경로에 소급하지 않는다.
- `http://json-schema.org/latest/json-schema-core.html`: HTTP404. 최신 표준 링크를 찾아 대체하는 행동은 별도 경로다.
- `https://bowtie-json-schema.github.io/bowtie/`: `https://bowtie.report/`로 이동하지만 취득한 정적 body는0단어였다. 같은 원링크를 렌더하는 환경에서 app 데이터가 표시되는지 추가 확인해야 한다. 현재 기록은 표를 읽었다는 주장과 구분한다.

SC032와 PyLD의 기존 예산 밖 시험은 이 계획에 포함하지 않는다.
