# F1 편집: SC-033–040 / LD-001–022

최종 취합 2026-11-23T03:36:18.179459+00:00. 작업자 `features_ld`; 2023 새 질문·후보 순위·조건 판정 미노출. 부모 검토도 새 질문·순위 전 추출 규칙·위치만 검토했다. 30행 전수 시도, 29행 원문 창 직접 독해, 27행에 기능 표기 77개를 추가했다. 이 수는 요구를 만족하는 구현 수가 아니다.

## 분모와 직접 비용

| 항목 | 실제 | 단위·한계 |
|---|---:|---|
| 편집 시도 | 30 | 게시행; SC 8 + LD 22 |
| 읽은 공급자 원문 | 29 | 고유 README/공식 crate 소개; LD022 본문 미확보 |
| 추가 필드가 생긴 행 | 27 | 빈3행은 아래 사유 |
| 저장한 원표기 | 77 | 행별 최대3; 원표기만 검색 필드에 투입 |
| 메타데이터 요청 | 84 | release/commit/redirect/crate 조회; HTTP redirect hop 수가 아님 |
| 실제 본문 요청 | 37 | 공급자29 + 후속8; 후속404 하나 포함 |
| 성공 원문 응답 | 36 | docs.rs redirect shell도 응답 성공이며 적격 본문으로는 제외 |
| 행별 논리적 문서 행동 | 42 | 공급자29 + 후속13; 공유 API/Node 문서 재사용 포함, 각행≤2 |
| 공급자 첫창 | 12467 | 표시단어; 각창≤500 |
| 공유 문서를 행마다 읽는 비용 | 17890 | 공급자 첫창 + 행별 후속창; 미리 알아도 행별 비용이 사라지는 것으로 처리하지 않음 |
| 캐시창 하나씩 센 읽기량 | 15890 | 파일별 창; 동일 저작 복수 URL/절은 독립 저작이 아님 |
| 정정 이전 추가 표시 노출 | 1411 | 아래 정정표; 겹친 단어도 추가 표시 비용이며 새 외부 원문 수와 다름 |
| 출처 원장 | 39 | 공급자30(실패1 포함) + 후속9(실패1·redirect shell1 포함) |

29개 공급자 저작 중 jsonld.js, PyLD, jsonld-cli 3개는 AF-RES-056 재사용이다. 나머지 26개가 이번 직접 읽은 공급자 저작이며, wrapper/원엔진·suite 패키지는 `engine_lineage`로 별도 묶는다. 이 수를 26개의 서로 독립적인 실행 엔진이라고 해석하면 안 된다. JSON-LD 1.0/1.1 API와 그 절/현재 URL은 같은 API 저작의 판·복수 응답 계보로 묶었고 신규 저작 수를 늘리지 않는다. Sophia/SC039 후속 API도 원래 공급자 저작과 동일하다.

## 30행 최종 표기와 빈칸

| 행 | 저장한 F1 원표기 | 직접 판·근거 |
|---|---|---|
| SC-033 | 빈칸: 링크만 있는 11단어 README; API/Features 문서로 명시된 링크 없음. 일반 Documentation 링크를 검색하여 확장하지 않음. | [4.0.2](https://github.com/JamesNK/Newtonsoft.Json.Schema/blob/5456c4bffe9a0b18ecd70ee056fc43f8a19ebf7a/README.md) · `F-SC-033` |
| SC-034 | Generation of schemas from .Net types · JSON Schema validation for ASP.Net APIs · Schema generation support for System.ComponentModel.DataAnnotations. | [formal-version-unconfirmed](https://github.com/json-everything/json-everything/blob/d7ef3bd10a15b4093690fd6773930b156c3037c5/README.md) · `F-SC-034` |
| SC-035 | parseFile · validate · validateBasic | [formal-version-unconfirmed](https://github.com/pwall567/json-kotlin-schema/blob/c87e75207da6de1ea4dd65777742020f2d97995b/README.md) · `F-SC-035` |
| SC-036 | Validation · validate · validate! | [v6.2.1](https://github.com/voxpupuli/json-schema/blob/eeb9aa7f1fe0581ace654a9f3f4bb02192b05bac/README.md) · `F-SC-036` |
| SC-037 | custom keywords · internationalization of error messages · annotation collection | [1.9.1](https://github.com/harrel56/json-schema/blob/00c2cd073e58b820f6b8ffa2f67fde92b743b694/README.md) · `F-SC-037` |
| SC-038 | json-schema:validate · Validating a simple type · json-schema.parse:parse | [formal-version-unconfirmed](https://github.com/fisxoj/json-schema/blob/ede034a25f72ba50d22e139bafe154cf877d8a6f/README.rst) · `F-SC-038` |
| SC-039 | compileSchema · SchemaNode · validate | [v11.6.16](https://github.com/sagold/json-schema-library/blob/bfc101953f038e2c9ec627f19b64a7aa41d62bd1/README.md) · `F-SC-039` |
| SC-040 | Inline Schema References · inline · Simplify Schema | [formal-version-unconfirmed](https://github.com/zx80/json-schema-utils/blob/1347b46aec09eb8cc387c4cfa243b6681aef227c/README.md) · `F-SC-040` |
| LD-001 | 빈칸: JSON-LD/Framing 이름은 준수 대상 표준목록에만 있음. 첫 API 링크는 W3C 표준이고 자사 기능 증거 아님. | [9.0.0](https://github.com/digitalbazaar/jsonld.js/blob/27a2b812267fef702c0ac5260a7555d35c3af005/README.md) · `F-LD-001` |
| LD-002 | JsonLdParser · Print all parsed triples from a file to the console · Manually write strings to the parser | [formal-version-unconfirmed](https://github.com/rubensworks/jsonld-streaming-parser.js/blob/0b62b7e6731135aa9590db207f4407e22bff4a20/README.md) · `F-LD-002` |
| LD-003 | JsonLdSerializer · Pretty-print given triples to the console · Pipe a stream of triples | [formal-version-unconfirmed](https://github.com/rubensworks/jsonld-streaming-serializer.js/blob/10d7a3d648ee03eab8406aee65e165b7965b7257/README.md) · `F-LD-003` |
| LD-004 | rdfParser · Parsing by content type · parse | [formal-version-unconfirmed](https://github.com/rubensworks/rdf-parse.js/blob/7f1283213a9f1cc7e8a2717f2fc3dab8469ea670/README.md) · `F-LD-004` |
| LD-005 | IdentifierIssuer · compact | [3.3.0](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/README.md) · `F-LD-005` |
| LD-006 | Graph · Store | [7.6.0](https://github.com/RDFLib/rdflib/blob/8b32146a0f9cb748c2068662e50d02b42fc86dfd/README.md) · `F-LD-006` |
| LD-007 | Transpiling Linked Data Algorithms · Transcribing Linked Data · Serializing JSON-LD as Turtle or TriG | [formal-version-unconfirmed](https://github.com/niklasl/trld/blob/e82bc73a3bec2c0625baf378767c2c26c7376b95/README.md) · `F-LD-007` |
| LD-008 | expansion · compaction · framing | [3.3.2](https://github.com/ruby-rdf/json-ld/blob/652730747e70f44f71ab7331f111c4308fe25b5c/README.md) · `F-LD-008` |
| LD-009 | Expansion · Compaction · RDF Serialization | [v0.9.1](https://github.com/piprate/json-gold/blob/f43b7e3497eb98d7372854273a13803358b59c36/README.md) · `F-LD-009` |
| LD-010 | Expansion · Compaction · Flattening | [v1.7.0](https://github.com/filip26/titanium-json-ld/blob/553fc68526f804028b0c3836163b772d94edaec8/README.md) · `F-LD-010` |
| LD-011 | fromInputStream · JsonLdOptions · compact | [formal-version-unconfirmed](https://github.com/jsonld-java/jsonld-java/blob/4a7305f26af38b47336fe28ba506a5f2ce0aae43/README.md) · `F-LD-011` |
| LD-012 | reading · writing RDF · managing | [v3.5.2](https://github.com/dotnetrdf/dotnetrdf/blob/67142d12e67fb68b37d009c3579ddebaeb4ff2c1/README.md) · `F-LD-012` |
| LD-013 | Expand | [1.0.7](https://github.com/linked-data-dotnet/json-ld.net/blob/fde0281cf8d87f04bcf75700cdf2a7dcc84dac58/README.md) · `F-LD-013` |
| LD-014 | Check JSON-LD for various problematic data. · compact · expanded | [056-fixed-SHA](https://github.com/digitalbazaar/jsonld-cli/blob/ab35bc8b00dedcd119904f56a8904721188094b1/README.md) · `F-LD-014` |
| LD-015 | expand · compact · flatten | [v1.0.3](https://github.com/filip26/ld-cli/blob/3b57ad3732703dab629be6e83ed281cc9c5fb3a1/README.md) · `F-LD-015` |
| LD-016 | JSON-LD reader · writer · customizable HTTP client for remote document loading | [formal-version-unconfirmed](https://github.com/rdf-elixir/jsonld-ex/blob/e0574a4ce236040353937e377fb69f13a6da6f08/README.md) · `F-LD-016` |
| LD-017 | jsonld_compact · jsonld_expand · jsonld_flatten | [formal-version-unconfirmed](https://github.com/digitalbazaar/php-json-ld/blob/fe18c3f2ce47f30ace904ef58e7416f933be25e1/README.md) · `F-LD-017` |
| LD-018 | value matching · deep-filtering · aggressive re-embedding | [formal-version-unconfirmed](https://github.com/lanthaler/JsonLD/blob/6c18b54c6ef912a6ef38f92a9c90df7ab288ed70/README.md) · `F-LD-018` |
| LD-019 | JsonLdProcessor · context processing · expansion | [formal-version-unconfirmed](https://github.com/timothee-haudebourg/json-ld/blob/211effb10bf21ec80b7b03d9d1efab3d57cdf5b3/README.md) · `F-LD-019` |
| LD-020 | Term · Graph · Dataset | [0.10.0](https://crates.io/api/v1/crates/sophia/0.10.0/readme) · `F-LD-020` |
| LD-021 | JsonLdParser · JsonLdSerializer · regular JSON-LD parsing | [0.2.7](https://crates.io/api/v1/crates/oxjsonld/0.2.7/readme) · `F-LD-021` |
| LD-022 | 빈칸: 대표 저장소와 releases API 모두404. 판·자기구현역할·본문 미확인. 기능부재 판단 아님. | [판 미확인](https://github.com/mattrglobal/jsonld-lint) · `F-LD-022` |

## 규칙 경계와 반대 근거

- `Features & conformance`, `✨ Features`는 exact whitelist 표제가 아니다. LD005/LD015는 첫 제목부터 창을 사용한다. 공급자가 링크한 준수 표준 제목은 자기 API명이 아니므로 LD001의 Framing을 저장하지 않았다. 빈 필드가 구현 기능 부재를 뜻하지 않는다. 근거: F-LD001, F-LD005 및 interpretation-correction.json.
- LD008은 “API interfaces”로 직접 명명된 expansion/compaction/framing을 저장했다. 앞의 parses/serializes는 일반 설명 동사라 제외했다. LD018의 supports 문장 괄호 안 value matching/deep-filtering/aggressive re-embedding과 LD019의 algorithms 괄호 목록은 명시 기능 목록으로 처리했다. 이 구문 경계가 기능 추출을 바꿀 수 있으며 임의 동의어 추가를 허용한 것은 아니다. 근거: F-LD008, F-LD018, F-LD019.
- 한 bullet·표제에 독립 연산명이 여러 개면 좌→우로 세 이름 한도를 쓴다. LD014의 Check 다음 compact, expanded에서 닫으며 flattened/canonized와 다음 RDFa 기능을 넣지 않는다. LD012는 reading, writing RDF, managing; LD009의 세 번째는 RDF Serialization; LD016은 JSON-LD reader, writer, customizable HTTP client…이다. 공유 수식어나 목적어를 뒤 항목에 새로 붙이지 않았다. Turtle/TriG처럼 같은 serialization 동작의 데이터 형식명 선택은 별도 연산명으로 보지 않는다. 일반적인 짧은 이름이 늘어날 수 있다는 추출 약점도 보존한다.
- SC034는 F0부터 json-everything suite다. 자사 패키지 기능 표는 적격이지만 Generation/API/DataAnnotations는 서로 다른 패키지이며 selected package not guaranteed다. LD012도 RDFsuite Core·AspNet 구분, LD020은 meta-crate의 jsonld 선택 feature를 구분한다. 그룹 전체 기능을 단일 엔진·기본 설치 기능으로 합칠 수 없다. 근거: F-SC034, F-LD012, F-LD020.
- LD004 rdf-parse의 JSON-LD 처리는 LD002 parser에 위임된다. LD014 CLI는 jsonld.js/jsonld-request wrapper다. 같은 엔진을 감싼 게시행을 독립 실행 검증으로 세지 않는다. 근거: F-LD004, F-LD014.
- LD009은 JSON-LD1.1 Framing 미지원과 HTML processing 미지원이라고 명시한다. LD016은 Framing을 TODO로 둔다. 표준 이름이나 계획 표제를 기능으로 넣으면 오인된다. 근거: F-LD009, F-LD016.
- LD003의 리스트/compound-literal/메모리 관련 제한과 LD007의 advanced compaction→Turtle 전사 제한은 공급자의 일반 기능 설명을 모든 입력 지원으로 읽을 수 없다는 반대 근거다. 이 설명은 사용자 조건 판정이 아니며 그때 허용된 같은 경로에서 다시 확인해야 한다. 근거: F-LD003, F-LD007.
- LD005의 CLI는 optional extra이며 명령 compact를 기본 라이브러리 위치 증거로 쓰지 않는다. 최종 locator는 jsonld.compact 호출이다. SC035 validate·SC039 validate·LD004 parse·LD011 compact도 일반문·주석의 첫 부분문자열이 아니라 공개 API occurrence를 가리킨다. 근거: feature_evidence.eligible_needle와 final-extraction-corrections.json.

## 실제 후속·실패·정정 노출

후속은 API14(4행 공유), NODESTREAM(2행 공유), API11, API11REMOTE, DOTNETAPI, APICURRENT, SOPHIAAPI, RUSTAPI, SC039METHODS다. SC039는 같은 README 응답의 다른 fragment 창이며 물리적 신규 원문 요청은 0이다. DOTNETAPI는404, RUSTAPI는 HTTP200 redirect shell만 읽었고 세 번째 문서인 실제 trait 목적지는 열지 않았다. 기능 출처 URL은 편집 감사용이며 이용자 경로를 바꾸지 않는다.

| 정정 | 실제 추가 노출 | 주 F1 처리 |
|---|---:|---|
| LD005 복합 Features&conformance를 잘못 적격으로 읽음 | 500단어 | 같은 README 첫500으로 교정; 이전 창 기능은 주필드에서 제외 |
| LD010 복합 제목 해석 | 0 신규 단어 | 교정 전후 첫500 동일; 선택 링크는 API 시험행 대신 실제 API 절 |
| LD015 emoji Features를 허용표제로 잘못 처리 | 411 재표시 단어 | 첫제목부터473 단어 창; 이전411은 겹치지만 비용 기록 |
| SC038 제한 RST renderer 교정 | 500 재표시 단어 | 같은 원문500 재렌더링; 코드/표제 경계 교정 |

OpenApi 사이트, te075/tli12 시험 링크, sophia_api crate 목록을 자동 substring 탐지기가 후속 후보로 제시했으나 이 URL들의 본문은 취득·독해하지 않았다. 실제 API/Features 역할의 첫 링크를 사람 검토로 확정했다. window-metadata의 heuristic_api_link_candidate와 최종 first_api_features_link를 분리한다. 문서 수 한도 초과는 없고 위의 표시창 추가 노출은 삭제하지 않았다. 재표시 전체 횟수는 별도로 계측하지 않아 1,411은 등록된 경계 교정 노출량이며 모든 UI 재출력 비용의 완전 계측은 아니다.

## 재현·판·출판

27개 GitHub README 캐시의 Git blob SHA를 전부 원격 blob과 대조해 일치했다. 네 파일의 UTF-16 문자 수/추가 EOF LF 때문에 발생한 차이는 끝 LF만 제거하여 수정했다. 두 crate 소개는 고정 버전 URL의 SHA256을 기록했다. 정식 release가 없는 행은 cutoff 이전 마지막 commit으로 고정하고 formal-release-unconfirmed로 표시한다. 실제 F0 당일판과의 완전한 연계는 별도 입증하지 않았으며 same_day_version_confirmed=false다.

render_windows.py는 marked GFM→lxml 가시 텍스트, RST 한 문서는 제한적 역할/제목/코드 변환을 적용한다. 창 단어 수는 whitespace split, 표 셀은 문서순, 코드 문자 그대로다. RST 전체 문법을 구현한 renderer가 아니라는 한계가 있으나 저장한 세 기호의 원문/창 위치를 직접 확인했다. 읽기 UTC는 독해 후 기록한 완료시각이며 개별 화면의 정확한 순간시각을 따로 수집한 것은 아니다.

출판에 필요한 파일은 features.json, sources.jsonl, findings.md, summary.json, windows/, version-metadata.json, acquisition.json, 두 crate metadata, followups.json, window-metadata.json, manual-selections.json, interpretation-correction.json, interpretation-v0/, final-extraction-corrections.json 및 renderer/취합 스크립트다. raw/는 후속 이용자 경로를 동일 응답으로 재현하기 위한 임시 캐시이므로 현재 유지하되 본문 전문을 원격 출판할 필요가 없다. publication-files.json이 구분을 기록한다. 기능·원문 확인 완료와 전체 연구 수용 완료는 별개이며 조건 판정·48비교·144슬롯은 부모 단계의 후속 작업이다.
