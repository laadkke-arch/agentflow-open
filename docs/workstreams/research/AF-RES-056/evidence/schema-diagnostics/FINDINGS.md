# JSON Schema 예산 밖 진단

## 지위·판·주체

이 파일의 읽기와 실행은 `b765a189aa2a1f5982a4994fc0476273abbf7127`에서 본표의 목록·순위를 고정한 뒤 수행했다. 용어표 고정판은 `1f63f0129207904a91ae9e01bb3e48c86415a644`이다. 모든 진단은 **두 동작 본표 밖**이며 후보 목록의 제목·별칭·기능 필드, 순위 또는 완결 판정에 역으로 넣지 않는다. 조사·실행 주체는 같은 ChatGPT 협업 세션의 catalog/schema-diagnostics 담당이다. 외부 독립 검토가 아니며, 공식 suite와 공급자 문서는 출처가 다른 근거지만 이 로컬 실행기는 본 연구자가 작성했다.

| 자료 | 고정판 | 판의 용도 |
| --- | --- | --- |
| JSON-Schema-Test-Suite | `e2a68a15cd490750fd6b95e604e4054d7d978d1f`, 2026-11-16 | 현재 공개 기대 입력·출력. 질문 작성 당시 suite 복원이 아니다. |
| Ajv | v8.17.1, `9050ba1359fb87cd7c143f3c79513ea7624ea443` | 2024년 공급자 문서·소스 독해. Ajv 실행은 미실시. |
| python-jsonschema | v4.23.0, `cfe8a4071672b9652c8f083faed1c4ffa7d67705` | 2024년 공급자 FAQ·키워드 소스 독해. 이 판 실행은 미실시. |
| ajv-cli | v5.0.0, `aa7c5062a2d6a8413fcb1274a8d3bd1a3fda4b54` | 고정 manifest·엔진 import. 실제 설치된 Ajv minor는 미확인. |
| 로컬 Python 실행 | jsonschema **4.26.0**, referencing 0.37.0, jsonschema-specifications 2025.9.1 | 2026-11-23 실행의 정확한 환경. v4.23.0 증거로 합치지 않는다. |

## 1. 양성·근접 음성: 기대값과 실제 실행을 구분

`selected-cases.json`은 공식 원본의 schema·data·expected valid를 그대로 보존하고 JSON Pointer로 위치를 기록한다. `run_diagnostics.py`는 이 작은 입력집합만 실행하며, 전체 suite 실행기 또는 적합성 인증이 아니다. 이 실행은 후보 구현의 사용자 요구 두 조건을 함께 시험하지 않는다.

| 진단 ID | 고정 스키마/입력쌍 | 공식 기대값 | 로컬 4.26.0 관측 | 번역의 경계 |
| --- | --- | --- | --- | --- |
| SD-E-1/2 | `enum:[1,2,3]`; 입력 1 / 4 | true / false | Draft7: true / false | enum은 명시된 집합의 멤버십이다. 인스턴스의 다른 배열에서 값 추출까지 뜻하지 않는다. |
| SD-R-1/2 | `bar:{$ref:"#/properties/foo"}`, foo는 integer; bar=3 / true | true / false | Draft7: true / false | $ref는 스키마 위치를 참조한다. 외부 스키마 등록이나 인스턴스 데이터 참조와 구분한다. |
| SD-LIT-1/2/3 | enum에 `{"$ref":"#/$defs/a_string"}` 한 객체; 문자열 / `{"type":"string"}` / enum의 정확 객체 | false / false / true | Draft202012: false / false / true | 같은 철자라도 enum 데이터 안의 $ref를 스키마 참조처럼 실행하면 오답이다. |
| SD-D-1/2/3 | alpha: number, maximum 3, default 5; `{alpha:1}` / `{alpha:5}` / `{}` | true / false / true | Draft202012: true / false / true; 모든 입력 유지 | default를 자동 값 삽입으로 대응하면 누락 {}를 잘못 해석한다. |
| SD-F-ON-1/2 | format=date; `2020-01-31` / `2020-01-32`; FormatChecker 있음 | assertion 태그에서 true / false | Draft202012: true / false | 형식 assertion을 실행하는 조건을 명시해야 한다. |
| SD-F-OFF-1/2 | 같은 날짜쌍, FormatChecker 없음 | assertion 기대값 적용 대상에서 제외한 통제 | Draft202012: true / true | 초안·스키마가 같아도 옵션 없이 무효 날짜가 거절되지 않는다. |

직접 근거는 [enum /tests/0](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/enum.json#L5-L21), [상대 참조 양성·음성](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/ref.json#L38-L57), [enum 속 리터럴 $ref](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/ref.json#L231-L258), [default 입력 3개](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/default.json#L52-L81), [date 태그와 입력쌍](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/format-date.json#L44-L86)이다.

**계산:** 실행 14건 중 해당 profile에 공식 기대값을 적용한 12건은 12/12 일치했다. FormatChecker 없는 통제 2건은 둘 다 유효였고, 공식 assertion 시험 실패율 분모에 넣지 않았다. 입력 변이 관측은 0/14이며, 특히 default 누락 입력은 `{}` 그대로였다. 이 수치를 8요구×L/V의 완결/부분 분모에 넣지 않는다. 실제 UTC·stdout·종료 코드·입력과 실행기 해시·각 출력은 `runtime-receipt.json`과 `execution-output.json`에 있다.

## 2. default: 주석과 삽입은 다른 계약

[Ajv의 고정 문서](https://github.com/ajv-validator/ajv/blob/9050ba1359fb87cd7c143f3c79513ea7624ea443/docs/guide/modifying-data.md#L155-L217)는 `useDefaults`를 켜야 누락 properties/items에 값을 넣는다고 설명한다. [같은 문서의 일반 주의](https://github.com/ajv-validator/ajv/blob/9050ba1359fb87cd7c143f3c79513ea7624ea443/docs/guide/modifying-data.md#L5-L29)는 이런 수정이 비표준이고 실행 순서에 영향을 받을 수 있음을 명시한다. [옵션 기본값](https://github.com/ajv-validator/ajv/blob/9050ba1359fb87cd7c143f3c79513ea7624ea443/docs/options.md#L25-L54)은 `useDefaults:false`이다.

[python-jsonschema v4.23.0 FAQ](https://github.com/python-jsonschema/jsonschema/blob/cfe8a4071672b9652c8f083faed1c4ffa7d67705/docs/faq.rst#L100-L209)는 기본 검증이 instance를 바꾸지 않으며, 필요한 사용자는 `properties`를 확장한 validator를 만들도록 예시를 제공한다. 이는 다른 공급자 관점에서 같은 경계를 드러낸다. 단, 두 문서의 설명을 두 개의 실행 성공으로 세지는 않는다.

**반대 가능성:** 실제 요구가 “유효성 검사 후 누락 기본값을 채운 출력”이고 사용자가 Ajv 옵션이나 Python 확장을 허용한다면 추가 기능으로 충족할 수 있다. 따라서 주석→삽입을 일반 동의어로 허용하지 않는 결론은 유지하되, 그러한 환경을 명시한 별도 요구에서는 해당 구현 문서·옵션·변형 출력 시험을 다시 확인해야 한다. 이번 8요구에 자동 보정을 추가하지 않는다.

## 3. format: 초안·어휘·구현 등록·옵션을 각각 확인

[공식 suite의 태그 규칙](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/README.md#L178-L190)은 2019-09/2020-12의 기본 주석 동작과 assertion 동작을 나눈다. 이 README는 미래 v1도 설명하므로 그 문장을 draft-07 또는 2020-12에 소급하지 않는다.

[python-jsonschema FAQ](https://github.com/python-jsonschema/jsonschema/blob/cfe8a4071672b9652c8f083faed1c4ffa7d67705/docs/faq.rst#L5-L71)와 [고정 구현의 format 함수](https://github.com/python-jsonschema/jsonschema/blob/cfe8a4071672b9652c8f083faed1c4ffa7d67705/jsonschema/_keywords.py#L223-L228)는 검사기의 존재가 동작을 갈라놓는다는 근거다. [validator 인스턴스 정의](https://github.com/python-jsonschema/jsonschema/blob/cfe8a4071672b9652c8f083faed1c4ffa7d67705/jsonschema/validators.py#L223-L240)에서 `format_checker` 기본은 None이다. 클래스의 `FORMAT_CHECKER`가 존재한다는 사실을 기본 활성화로 오독하지 않는다.

Ajv는 다른 계약이다. [Ajv v8.17.1의 format 문서](https://github.com/ajv-validator/ajv/blob/9050ba1359fb87cd7c143f3c79513ea7624ea443/docs/guide/formats.md#L3-L31)는 v7부터 표준 format 구현을 ajv-formats 플러그인에서 제공한다고 명시한다. 따라서 `validateFormats:true`라는 옵션이나 지원 초안만 보아 설치·등록된 format과 결과를 확정할 수 없다.

추가 어휘 반례로 [official optional format-assertion 입력](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/optional/format-assertion.json#L1-L81)을 읽었다. `$vocabulary`의 false는 이미 인식한 어휘의 assertion을 끄는 옵션이 아니다. 이 파일의 custom metaschema 입력은 **미실시**이며 로컬 날짜 실행과 합치지 않는다.

## 4. $ref·정적 enum·$data는 구분해야 한다

[Ajv의 schema $ref 설명](https://github.com/ajv-validator/ajv/blob/9050ba1359fb87cd7c143f3c79513ea7624ea443/docs/guide/combining-schemas.md#L5-L53)에서는 스키마 식별자와 등록을 다룬다. 같은 문서의 [별도 $data 절](https://github.com/ajv-validator/ajv/blob/9050ba1359fb87cd7c143f3c79513ea7624ea443/docs/guide/combining-schemas.md#L124-L173)은 검증 중인 데이터값을 enum 등의 키워드값으로 참조하는 확장을 설명한다. [enum 구현](https://github.com/ajv-validator/ajv/blob/9050ba1359fb87cd7c143f3c79513ea7624ea443/lib/vocabularies/validation/enum.ts#L14-L50)도 `$data` 경로를 구분한다.

이 자료는 “기본 enum만으로 인스턴스 사이 값을 참조할 수 없다”는 진단에 대한 보완 사례다. 확장을 허용하면 가능한 비교가 늘어난다. 그러나 JS-4의 columns는 객체들의 배열이므로 열 이름을 추출하는 투영까지 이 문서에서 확인한 것은 아니다. Ajv를 JS-4의 완결 구현으로 반환하지 않으며, 질문의 Python 환경과도 별도다. JS-3 또한 로컬 $ref 쌍을 통과했다고 외부 URI 등록, draft-04와 $id의 혼재, required/email 조건이 함께 해결됐다고 볼 수 없다.

## 5. ajv-cli와 Ajv의 공유 엔진 계보

| 층 | 직접 확인 | 셀 수 있는 단위·한계 |
| --- | --- | --- |
| CLI 제품 | [고정 package.json L1-L4, L36-L44](https://github.com/ajv-validator/ajv-cli/blob/aa7c5062a2d6a8413fcb1274a8d3bd1a3fda4b54/package.json#L36-L44): ajv-cli 5.0.0, Ajv `^8.0.0` | 별도 배포/진입점·공급자 저작이다. 정확 설치 minor는 고정되지 않는다. |
| 엔진 생성 | [src/commands/ajv.ts L1-L7, L24-L42](https://github.com/ajv-validator/ajv-cli/blob/aa7c5062a2d6a8413fcb1274a8d3bd1a3fda4b54/src/commands/ajv.ts#L24-L42): ajv 패키지의 draft별 클래스를 가져와 생성 | Ajv와 같은 상류 검증 엔진으로 묶는다. 이름이 둘이라고 독립 엔진 2개로 세지 않는다. |
| 실행 경로 | [validate.ts L31-L45](https://github.com/ajv-validator/ajv-cli/blob/aa7c5062a2d6a8413fcb1274a8d3bd1a3fda4b54/src/commands/validate.ts#L31-L45): getAjv→compile→validate(data) | CLI와 라이브러리의 조합 관계는 직접 확인. 실행 통과는 미측정. |
| 의존판 결손 | [고정 재귀 tree](https://api.github.com/repos/ajv-validator/ajv-cli/git/trees/aa7c5062a2d6a8413fcb1274a8d3bd1a3fda4b54?recursive=1) `truncated=false`; lock/shrinkwrap 경로 없음 | `^8.0.0`을 특정 8.x 실행판으로 바꾸어 적으면 안 된다. 보존된 설치 환경이나 잠금파일이 필요하다. |

Ajv 문서판 8.17.1이 CLI의 정확 실행 의존판이라는 결론은 **미확인**이다. 새로 설치해 얻는 버전은 당시 해석판의 증명이 아니다.

## 6. 자료 수·접근 한계·최소 재개

`sources.jsonl`은 34행이다: 원문 파일 직접 열람 23행, 고정판 metadata 재확인 5행, 실패 6행. 본 연구의 원문 최소 수에는 보수적으로 공식 suite 1저작, Ajv 문서·소스 1저작, python-jsonschema 문서·소스 1저작을 가산할 수 있다. ajv-cli의 별도 공급자 저작은 추가 1개지만 Ajv와 같은 엔진 계보이고 앞의 독립 공급자 2개를 대신하지 않는다. 매뉴얼의 여러 절·라이선스·재확인 metadata를 추가 저작으로 세지 않는다. 원문 스냅샷에는 직접 확인한 MIT 허가문을 보존했다.

예전 `tests/draft*` 경로 5개가 404였으나, 고정 suite의 현재 `validation/tests/`와 `annotations/tests/` 위치를 복원했다. 이는 기능 부재나 최종 접근 실패가 아니다. CLI package-lock.json 404는 고정 tree 전체 확인으로 좁혔으나, 정확 해석된 Ajv minor의 결손은 남는다.

### 실행·재개 명령과 입력

완료한 로컬 진단의 재현 입력은 `selected-cases.json`과 고정 스냅샷이다. 저장소 루트에서 실행:

```bash
python -B docs/workstreams/research/AF-RES-056/evidence/schema-diagnostics/run_diagnostics.py
```

이 명령은 현재 설치된 패키지를 검사하고 버전을 출력하므로, 원래 receipt를 덮어쓰지 않으려면 별도 checkout에서 수행한다. 정확히 v4.23.0의 실행 근거가 필요해질 때 첫 행동은 보존된 v4.23.0 환경에서 이 입력/실행기를 실행하고 새 receipt를 다른 파일에 저장하는 것이다. 이번 v4.26.0 결과를 바꿔 적지 않는다.

CLI의 정확 의존판 판별에는 **당시 실제 ajv-cli v5.0.0 설치 디렉터리**가 입력으로 필요하다. 그 디렉터리를 작업 디렉터리로 지정한 뒤 아래 명령의 출력과 기존 잠금파일을 보존한다. 이 명령은 현재 환경에 해당 배포가 없어 미실시다.

```bash
npm ls --all --json ajv
node -p "require('ajv/package.json').version"
```

현재 조사에서 필요한 양성·근접 음성의 예산 밖 진단은 확보했다. 남은 미확인은 원 요구의 두 조건이 같은 판·옵션에서 함께 성립하는지와, 본표의 허용 두 동작 안에서 그 근거가 실제 보이는지다. 이 파일의 추가 공급자 독해로 그 결손을 대체하지 않는다.

