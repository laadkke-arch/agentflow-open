# 출처 저작·판·계보 재검토

검토 대상은 고정 F1 커밋 `412192e28356bee13e4c11f20511ab5ec590662c`의 `evidence/features-ld/sources.jsonl`과 인수한 `inputs/af-res-056/source-lineage.json`이다. 기능표·기존 원장을 수정하지 않았다. 이 메모는 동일 저작의 복수 URL·판·절을 새로운 외부 저작으로 세지 않기 위한 집계 근거다.

| 기록 | 묶는 work_id | 재사용·판 판단 |
|---|---|---|
| F-LD-001 | SUP-JSONLDJS | 056의 LD-SUP-JS-DOC, AUD-JSONLDJS-README/USAGE와 같은 공급자 저작; 동일 SHA |
| F-LD-005 | SUP-PYLD | 056의 LD-SUP-PY-DOC, AUD-PYLD-README 등과 같은 저작; 동일 SHA |
| F-LD-014 | jsonld-cli-snapshot | 056의 LD-SUP-CLI-PKG/FRAME와 같은 패키지 저작; README를 새로 읽었어도 신규 저작 아님 |
| F-LINK-API14 / API11 / API11REMOTE / APICURRENT | w3c-jsonld11-api | 2014 1.0판·1.1판·같은 판의 remote-document 절·현재 리다이렉트 URL은 하나의 Processing Algorithms and API 저작 계보. 056 LD-STD-API 재사용 |
| F-LD-020 / F-LINK-SOPHIAAPI | supplier-pchampin-sophia_rs | crate 소개와 API 재게시/관련 절을 하나의 공급자 저작으로 묶음 |
| F-SC-039 / F-LINK-SC039METHODS | supplier-sagold-json-schema-library | 동일 README blob의 다른 fragment; 문서 행동은 두 번이어도 신규 저작은 한 개 |
| F-LD-019 / F-LINK-RUSTAPI | supplier-timothee-haudebourg-json-ld | 같은 crate 계보. 후속은 redirect shell만 독해했으므로 실제 trait API 본문 확보로 세지 않음 |
| F-LD-012 / F-LINK-DOTNETAPI | supplier-dotnetrdf-dotnetrdf | 후속 API404는 탐색 실패; 공급자 README 저작 외 신규 확보 없음 |
| F-LINK-NODESTREAM | nodejs-stream-docs | 두 게시행이 공유한 같은 Node Stream 문서·fragment; 새 배경 저작 한 개. 공급자의 자체 구현 증거로 승격하지 않음 |

`w3c-jsonld11-api`라는 문자열의 `11`은 인수한 식별자를 유지한 것이다. 2014판을 JSON-LD1.1이라고 표시한다는 뜻이 아니다. 각 판은 URL·응답 해시로 구분되며 원저작 수는 합산하지 않는다. 표준 개정 간 차이는 별도의 판 비교에 사용할 수 있지만 신규 표준 저작 할당을 채우는 데 쓰지 않는다.

## 현재 분모

39개 원장 기록 중 접근 실패 두 건(F-LD022, F-LINK-DOTNETAPI)과 API 본문이 없는 redirect shell 한 건(F-LINK-RUSTAPI)을 빼면 적격 직접 독해 기록은36개다. work_id로 묶으면31저작이며, 056에서 읽은 공급자3 + API1 =4저작을 재사용했다. 신규로 읽은 저작은 공급자26 + Node 배경1 =27이다. 이 분담분의 신규 표준 저작은0이다. `lineage-audit.json`에 계산 입력과 집합을 저장했다.

## 엔진·suite와 원저작의 차이

LD004 rdf-parse는 JSON-LD 부분을 LD002 jsonld-streaming-parser에 위임한다. LD014 CLI는 jsonld.js/jsonld-request를 사용한다. 두 README의 저자가 다르거나 내용이 독립이어도 같은 처리 엔진에 대한 시험 성공을 두 번 얻었다고 셀 수 없다. work_id를 다른 값으로 유지하는 경우에도 engine_lineage를 함께 읽어야 한다.

SC034 json-everything과 LD012 dotNetRDF, LD020 Sophia는 여러 패키지·모듈을 포괄한다. 자사 suite 문서를 여러 지원 기능으로 나누었다고 독립 저작 수가 늘지 않는다. 특정 패키지의 기능을 같은 판의 다른 모듈과 이어 붙여 두 조건을 충족했다고 판정할 수 없다.

전체 연구의 외부 저작 수는 다른 분담 원장의 같은 표준·Node·공급자 ID와 다시 합쳐 세어야 한다. 이27을 다른 분담의 신규 수에 그대로 더하면 중복이 생길 수 있다.
