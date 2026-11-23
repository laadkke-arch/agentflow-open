# JSON Schema SC-001–032 기능 편집 인계

로컬 필드 봉인: 2026-11-23T03:36:00.973981+00:00. 원격 stage2 커밋은 통합 연구자가 수행한다. 이 편집 문맥은 신규 요청 본문·F1 후보 순위를 읽지 않았다. 기존056 공급자 고정판과 목록은 읽었다. 역할은 기능명 취득·편집이며 요구 충족·실행 판정이 아니다.

## 완료 분모

32/32 게시행을 같은 절·500단어·두 문서 한도로 시도했다. 27행에 원표기 77개를 추가했고 5행은 빈 필드다. 첫 문서 32개와 허용 후속 문서 3개를 요청하여 34개를 읽었다. SC-025 후속은 HTTP503으로 읽지 못했다. 첫 창은 12,512단어, 성공한 후속 두 창은 541단어, 합계 13,053표시단어다. 62행 전체 분모는 이 파일 단독에서 주장하지 않는다.

판/경로 메타데이터의 보존된 요청은 106개, 그중 실패·미해소 응답은 13개다. 초기 SC001/002/004/010/013의 진단 재시도가 요청별로 전부 보존되지 않아 메타데이터 총량은 하한이다. 원문/창/단어의 분모는 정확하며, 시간·총 HTTP 요청비용은 측정했다고 주장하지 않는다. acquisition-ledger.jsonl은 보존 영수증의 단위로 세었다.

## 행별 편집 결과

| 행 | 추가 원표기(최대3) | 읽은 원문/단어 | 빈 사유·역할 경계 |
|---|---|---:|---|
| SC-001 | Validator; validate; Add schemas | 1 / 275 | own implementation; comparison to Ajv is not delegation |
| SC-002 | Converts schemas to self-contained JavaScript files; Integrates nicely with bundlers; requireValidation | 1 / 500 | own schemasafe implementation |
| SC-003 | registerSchema; unregisterSchema; getAllRegisteredSchemaUris | 1 / 500 | Hyperjump implementation |
| SC-004 | TypeScript static type checking support for schema definitions; Smart type inference; Required/optional field inference | 1 / 500 | own implementation; conformance limitations stated |
| SC-005 | all validation keywords; discriminator; nullable | 1 / 389 | Ajv |
| SC-006 | Help command; help; Validate data | 2 / 1000 | Ajv delegation stated in introduction |
| SC-007 | compiles JSON Schema into a lower-level intermediate language; custom vocabularies; custom resolution of external schemas | 1 / 305 | Blaze |
| SC-008 | Native C++ validation; Memory safety; Detailed error reporting | 1 / 500 | native C++ backend; specific engine identity not independently verified in editing window |
| SC-009 | detect infinite loop traps; $schema cycle; validation cycle | 1 / 230 | boon |
| SC-010 | Source Generation; OpenAPI; AsyncAPI | 1 / 500 | Corvus.Text.Json / Corvus.JsonSchema family |
| SC-011 | validateSchema; Detailed Error View in the Console | 1 / 500 | Ajv errors explicitly supplied by Ajv; separate Cypress APIs are not this plugin |
| SC-012 | djv; addFormat; setErrorHandler | 1 / 500 | djv |
| SC-013 | 빈 필드 | 1 / 500 | no_eligible_heading_list_or_api_name_in_window |
| SC-014 | json_schema; valid?; errors | 1 / 500 | ActiveModel validations stated; schema output is its own DSL |
| SC-015 | JsonParser; parse; SchemaLoader | 1 / 500 | json-sKema |
| SC-016 | load; validate | 2 / 541 | everit implementation; org.json is upstream data representation |
| SC-017 | function_from_string | 1 / 288 | Exonerate |
| SC-018 | 빈 필드 | 1 / 500 | implementation_edition_unconfirmed_dynamic_page |
| SC-019 | allOf; anyOf; oneOf | 1 / 431 | built on fost-base JSON implementation |
| SC-020 | 빈 필드 | 1 / 7 | no_eligible_name_and_no_api_features_link |
| SC-021 | NewReferenceLoader; Validate; Valid | 1 / 500 | gojsonschema; URI and pointer helper dependencies named separately |
| SC-022 | getReader; read; validate | 1 / 241 | Jaronuinga; JSONP is data representation dependency |
| SC-023 | renders a complete form; instant client-side validation; Standalone client-side forms without server validation | 1 / 500 | Jedison; other server validators are optional alternatives |
| SC-024 | Schema; deref; validate | 1 / 177 | jema.js |
| SC-025 | Command-Line Interface; --json; internal in-memory storage | 1 / 500 | jesse; JSON parsing delegated to caller or callback |
| SC-026 | Create a schema; schema; Create a schema (short-hand) | 1 / 400 | jinx; comparisons to Java libraries/Ajv are not delegation |
| SC-027 | Schema compilation; indexing; $ref loading | 1 / 189 | jschon |
| SC-028 | 빈 필드 | 1 / 7 | development_site_identity_only_no_function_names |
| SC-029 | new_schema; jsi_schema_module; new_schema_module | 1 / 500 | JSI; native Hash/Array delegated methods remain separate |
| SC-030 | Loading JSON from; Writing JSON to; Encoding support | 1 / 500 | JSON Essentials; implementation internals not verified |
| SC-031 | 빈 필드 | 1 / 73 | development_instructions_only_no_application_feature_names |
| SC-032 | basic_error_handler; Thread-safety; validate | 1 / 500 | pboettch validator atop nlohmann JSON data library |

## 무엇을 확인했고 무엇을 확인하지 않았는가

- F0 게시 표기와 공급자의 실제 기능 표기를 분리했다. SC001의 `Validator`/`validate`, SC006의 `Help command`/`help`처럼 같은 개념일 수 있는 별명은 문자열 정규화만으로 같아지지 않으면 별도로 남겼다. 요구별 유리한 이름으로 대체하거나 validation 같은 표준어로 바꾸지 않았다. 첫3 제한 때문에 SC007의 뒤쪽 Annotations, SC010의 뒤쪽 Schema Validation, SC030의 뒤쪽 instance validation은 추가 필드에 들어가지 않는다. 이 사실은 매치·완결 증가 여부의 결론이 아니다.
- SC005·006·032는 056의 정확한 SHA를 재사용했다. 다른 GitHub 공급자는 릴리스/시각 규칙으로 고른30개 고정SHA가 있으며, 무릴리스 공급자의 정식판은 미확인으로 남겼다. SC001/004의 monorepo 릴리스는 다른 패키지 이름이다. 하위 README의 고정SHA는 확보했지만 해당 컴포넌트의 독자적 정식판을 발명하지 않았다.
- SC010은 첫200 릴리스의 게시시각을 대조한 범위에서 5.8.12가 선택된다. 그보다 오래된 페이지는 소진하지 않았으므로 전역 마지막 게시판의 완전성은 미확인이다. 고정SHA 자체와 그 README의 실제 표기는 확인됐다. 통합 연구자 요청에 따라 추가 메타데이터 조회를 중단했다.
- SC015는 선택판 v0.32.0인데 README 설치 예가0.25.0이고, SC016은 v1.14.5인데 설치 예가1.14.4다. 고정 소스와 설치 명령의 결과를 동일 판으로 합치면 안 된다. SC030은 페이지의1.2.1 및 HTTP Last-Modified를 확인했지만 정확한 F0 시각의 배포 응답은 복원하지 않았다.
- SC018은 기능 표제가 실제로 있지만 구현판을 확인할 수 없어 빈 F1이다. SC013은 장문의 공급자 설명이 있으나 허용한 표제/기능목록/API 기호의 적격 원표기를 창에서 찾지 못했다. SC020·028은 각7단어의 소개, SC031은 개발 설치/시험 안내만 읽혔다. 빈 필드는 구현에 기능이 없다는 판정이 아니다.
- Ajv, ajv-cli, Cypress 플러그인, ExtendsClass는 서로 다른 게시행/저작이지만 Ajv 계보를 공유한다. jschon.dev와 jschon도 관계를 기록했다. Blaze4J는 C++ native backend를 선언하지만 편집창에서 특정 엔진 동일성을 직접 확정하지 못해 Blaze와 자동 합치지 않았다. nlohmann JSON·JSONP·org.json 같은 데이터 표현 의존성과 스키마 검증 엔진도 구분했다.
- SC006의 첫 API 링크는 Node 모듈 해석 문서로 간다. SC016은 org.json의 프레임 랜딩으로 간다. 외부 런타임/API의 기능을 원공급자의 기능으로 귀속하지 않았고, 다음 좋은 링크로 대체하지 않았다. SC025는 API 문서 링크가503을 반환해 그 실패를 보존했다.
- SC014의 valid?/errors는 EasyTalk::Model 조건이 있고 SC027의 원격 $ref에는 선택 requests 의존 조건이 있다. SC025는 JSON 파싱이 없고 호출자/콜백이 파싱한다. SC026은 alpha 상태와 미구현 목록을 선언한다. SC032는 검증의 thread-safe와 생성의 thread-unsafe를 분리한다. 이름 하나만 저장하면 이러한 조건이 손실될 수 있다. 각 notes와 원문 창에 이를 남겼다.

## 계보·신규 열람 분모

공급자 출판물32개를 직접 읽었으며 3저작(Ajv·ajv-cli·SC032)은 056의 기존 저작 재사용, 29개는 이 조사에서 새로 연 공급자 출판물이다. 이는 독립 구현29개라는 뜻이 아니다. 동일 엔진 wrapper와 아주 짧은 소개/개발 안내를 엄격히 제외한 실질 공급자 설명의 수는 통합 source ledger에서 따로 계산해야 한다. 외부 Node API 후속1개는 별도 신규 저작이며, JSON-java 프레임 랜딩과503은 실질 신규 원문 최소수에 넣지 않는 보수적 계수를 제공했다.

## 재현·파일 분리

features.json은 catalog 순의32행이며 added_features만 검색용이다. feature_provenance는 실제 창의 줄/기호/조건과 근거 주소를 제공한다. sources.jsonl은35개 자료 접근을 기록한다. 모든 API·HTML 전문을 읽었다고 보고하지 않으며, 원문을 내려받은 것과 선택500단어 창을 직접 읽은 것을 구분한다.

render_windows.py는 GitHub README의 동일판 표시창을 재현한다. Markdown은 marked, RST는 pandoc, AsciiDoc은 기록된 최소 문법 변환을 쓴다. HTML은 main/article 우선, 없으면 body에서 선택했다. SC030의 HTTP 원문과 선택 컨테이너 직렬화 hash는 별도다. render-corrections.json은 파서 offset·AsciiDoc·CRLF·API 링크 문맥 분류의 기계 정정을 기록한다. 초기 잘못된 파서/AsciiDoc 창의 독립 hash가 보존되지 않은 감사 한계도 적었다.

build_ledgers.py는 이 디렉터리와 고정 catalog/source-lineage만 읽으며 요구·순위 파일을 읽지 않는다. 명령: `python -B docs/workstreams/research/AF-RES-060/evidence/features-schema/build_ledgers.py`. 행32개, max3, 원표기/앵커의 실제 창 포함, 문서2/창500 한도, 원문 SHA256/Git blob, 056 공급자 SHA를 확인했다. 공급자 설치·실행은 수행하지 않았다.

출판할 최소 집합은 publication-inventory.json의 publish=true다. _raw/는 같은판 이용자 첫 창을 만드는 현재 세션용 취득 캐시로 유지하되 전문을 일괄 업로드하지 않는다. 중복 중간 metadata/documents.json·readme-paths.json·window-summary.json도 최종 출판에서 제외할 수 있다.

## 결론을 바꿀 최소 입력

1. SC018의 구현판과 그 판의 공식 기능 설명이 확보되면 빈 필드 판단을 다시 할 수 있다. 현재 주표의 필드 교체는 하지 말고 사후 감도로 남긴다.
2. SC010의 남은 릴리스 게시기록에서 더 늦게 게시된 적격 릴리스가 발견되면 판 선택을 재검토해야 한다. 고정SHA 창에서 실제로 읽은 표기를 소급 지우지는 않는다.
3. 요청의 두 조건을 같은 구현판·같은 이용자 경로에서 직접 확인해야만 활용 가능한 권고가 된다. 현재 파일은 기능명 편집 증거이므로 그 후속 결과를 대신하지 않는다.
