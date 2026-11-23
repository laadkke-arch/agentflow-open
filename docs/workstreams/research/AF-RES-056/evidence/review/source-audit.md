# 원문 집계 감사

## 판정과 고정 범위

**최종 269행 스냅샷에서 집계 계산은 재현되며, 필수 24저작의 배당을 늘리는 자체 실행·미러·같은 매뉴얼 중복은 발견하지 않았다.** 다만 목록 데이터 계약과 제출 양식을 별도 저작으로 정의한다는 조건을 밝혀야 한다. 위치 표기 1건의 작은 정정도 반영됐으며, 전체 109개 work_id를 모두 원문 전체 재열람으로 검증했다는 주장은 이 감사 범위를 넘는다.

감사자는 `/root/catalogs`이다. 집계 작성자인 root와 별도로 계산과 표본 근거를 대조했으나, 같은 협업 세션에서 `catalog-pre`와 `schema-diagnostics` 원장 작성에도 참여했다. **외부 또는 맹검 독립 검토가 아니다.** 자신의 원장을 포함한 집계 검산과 교차 검토이다.

`source-audit-receipt.json`은 2026-11-23T02:11:41.007727+00:00에 완료한 입력 해시와 715개 구조·조인 검사 결과를 보존한다. 최초265행 receipt는 `source-audit-receipt-265.json`에 별도로 보존했다. root의 집계 스크립트를 실행하거나 root 파일을 수정하지 않고, 별도 `source_audit.py`로 재계산했다.

| 파일 | 감사 입력 SHA256 |
| --- | --- |
| aggregate_sources.py | `0bb866435c718f4a2138c1d664790293c17cf99945a3fb09b809f46517d3688f` |
| sources.jsonl | `12ea916ece316d0740e46e059c83607e21baf1f95d69634d4505b0bf9a8e6ce4` |
| evidence/source-counts.json | `2df326c00d6e00e41114d3100267dbf2f8b0c497693af996baaa5ce0c923c6e6` |
| evidence/primary-works.csv | `cdf889720f1f41339bfabbbfb38b90937fe847c3a05ee1df4194b13d0050ea1e` |

## 1. 산술·원장 결합·배당

| 검사항목 | 독립 재계산 | 판정 |
| --- | --- | --- |
| 열람 원장 전체 | 269행 | 12개 하위 원장 합계와 일치 |
| 직접 1차 자료 행 | 190 | 표시된 분류와 일치 |
| 실패 | 40 | 실패 경로를 고유 원문으로 산입하지 않음 |
| metadata·허가문 | 18 | 고유 원문 최소 수 제외 |
| 미러·재수록 | 2 | LOC 연간 PDF와 동봉 suite enum 파일 제외 |
| 내부 입력·자체 실행 | 19 | 내부 입력·선행16 + 자체 실행3 제외 |
| 직접 1차 고유 work_id | 109 | CSV의 109행과 정확 일치; 질문80 + 그 밖29 |
| 필수 배당 고유 work_id | 24 | 24개 서로 다른 ID, 실제 직접 열람 분류 확인 |

`sources.jsonl`은 원래 하위 원장의 모든 필드를 보존하면서 work_id 정규화, origin_ledger/origin_line, 분류, 배당을 더한 결과와 **행별 완전 일치**한다. `primary-works.csv`의 대표 URL/source_id, sources_lines, source_ids도 모든 묶음에서 일치했다. 실패·metadata와 복제 행이 같은 work_id를 가져도 직접 자료 집합에 들어가지 않는다.

| 필수 묶음 | 배당 | 실제 선택 ID | 검토 결과 |
| --- | --- | --- | --- |
| 사용자 질문 | 8/8 | SCH-Q05/07/08/09; LDQ-01/03/05/07 | 서로 다른 질문 ID, 최초 revision 식별자·본문 해시 연결 |
| 공식 목록·별도 편집 규칙 | 4/4 | CAT002/006/007/010 | 2목록+데이터 계약+제출 양식이라는 저작 경계에서 충족 |
| 표준·공개 시험 | 4/4 | SCH-STD-VALID07; SD001; LD-STD-API; LD-TEST-01 | validation 표준, Schema suite, LD API 표준, LD API suite 각각 별도 저작 |
| 공급자 | 4/4 | SD009; SD014; LD-SUP-JS-DOC; LD-SUP-PY-DOC | 4개 문서·구현 저작. 독립 개발 계보/독립 실행4개라는 뜻은 아님 |
| 전거 개념 | 4/4 | AUTH-LC1/LC2/AAT1/AAT2 | LOC 개념2와 Getty AAT 개념2를 URI로 구분 |

소스 수 충족은 역사적 태그 모집 복원이나 두 동작 안의 구현 완결까지 보장하지 않는다. 추가 질문72개가 있어 전체 109가 커져도, 비어 있는 필수 분야를 다른 분야 자료로 대체할 수 없다.

## 2. 자체 실행·복제·같은 매뉴얼의 처리

**정상 제외.** `EXEC-SC032`, `LD-SUP-EXEC-LOCAL`, `LD-SUP-EXEC-NEST-CAUSE`는 `internal_or_execution`이며 109 또는 24를 늘리지 않는다. 연구자가 쓴 입력의 결과를 외부 독립 시험 보고서로 계산하지 않았다. `INPUT-*`와 `DEP052-*`도 원문 최소 수에서 제외됐다.

**혼합 관측 한 행의 경계.** `LD-SUP-PY-CHECKOUT`은 고정 외부 소스 열람과 로컬 import 실패를 한 행에 담고 있어 `direct_primary`로 분류된다. 고정 소스를 실제 읽은 근거는 있지만, 로컬 import 부분은 외부 1차 저작이 아니다. 이미 `SUP-PYLD`에 합쳐져 있어 이 행을 내부/metadata로 옮겨도 고유109·배당24는 변하지 않는다. 새 공급자 저작이나 성공 실행으로 읽지 않는 현재 제한을 유지하면 수량 결론에 영향이 없다. 분류를 더 엄격하게 하려면 고정 소스 문장과 자체 환경 관측을 분리할 수 있다.

**동일 저작 병합.**

- draft-04/07 core는 `json-schema-core`, draft-07/2020-12 validation과 사후 재확인은 `json-schema-validation`으로 각각 합쳤다.
- JSON Schema suite의 README·운영규칙·enum/ref/default/format 파일은 1저작이다. SC032에 복사된 구판 enum은 별도 미러 행이고 추가 저작이 아니다.
- W3C JSON-LD API suite의 입력·출력·manifest 및 PyLD가 고정한 다른 suite SHA의 동일 fixture는 모두 `w3c-jsonld-api-conformance-suite` 하나다.
- Ajv·python-jsonschema·jsonld.js·PyLD의 README/FAQ/소스/runner/release는 구현별 하나로 묶였다.
- Getty editorial guidelines의 여러 절은 1저작이다. AAT2 note의 재확인은 기존 개념 URI에 합쳤고 인용된 Grove/Oxford 등의 원저를 열람한 것으로 세지 않았다.

## 3. 목록·편집 규칙 4저작의 방어 가능성과 민감도

[CAT002의 목록 데이터](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/data/tooling-data.yaml)와 그 renderer는 한 저작으로 합쳐져 있다. [CAT010의 JSON-LD 목록](https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/index.yaml)도 HTML·template·data를 반복 산입하지 않는다.

남은 두 항목은 다른 목적의 독립 파일이다.

| 항목 | 별도 저작으로 볼 근거 | 한계 |
| --- | --- | --- |
| [CAT006 tooling-data.schema.json](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/data/tooling-data.schema.json) | 게시 데이터의 자료형·허용 속성·필수 속성을 정한 기계 판정 계약. L291은 name/toolingTypes 필수, L292는 추가 속성 금지이다. | 목록과 같은 편집 시스템이며 구현 기능 검증 기준이나 독립 기관의 평가가 아니다. |
| [CAT007 adding-your-tooling.yml](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/.github/ISSUE_TEMPLATE/adding-your-tooling.yml) | 사람이 도구 추가/수정을 신청하는 절차·입력 규칙. Action Type, 설명, source/license 요구 등은 데이터 계약의 단순 문자열 복제가 아니다. | 공통 필드가 많고 같은 발행자가 관리한다. 제출 정보가 사실인지 검증하는 별도 절차를 이 양식이 보증하지 않는다. |

두 파일은 완전히 같은 내용의 미러나 한 매뉴얼의 다른 절이 아니므로, 사용자 요구의 **“공식 목록·별도 편집 규칙”**을 독립 저작 단위로 읽으면 4개 산입은 방어 가능하다. 다만 4개의 독립 목록, 4개의 독립 편집기관 또는 4개의 독립 기능 검증 근거라는 표현은 잘못이다. 계약과 양식의 category 선택지에도 차이가 있으므로 이 둘이 자동으로 동기화된 같은 표현이라고 단정하지 않는다.

**더 엄격한 경계의 민감도:** 동일 편집 시스템 안의 목록·계약·양식을 모두 1저작으로 합치면 이 묶음은 2/4, 배당 전체는 22/24, 전체 work_id는 107이 된다. 이 숫자는 원래 규칙을 바꾼 별도 계산이다. 본표의 L/V 순위·창 결과는 변하지 않는다. 원래 산입 기준과 이 의존성을 보고하면 되며, 많은 추가 질문으로 이 분야의 두 자리를 대체했다고 주장하면 안 된다.

### 위치 오류 1건 — 정정 확인

CAT006의 최초 원장 위치 `L292-295`는 필수 속성이 있는 **L291**을 빠뜨렸다. 직접 고정 스냅샷과 `nl -ba`로 확인해 root에 통보했고, root가 `L291-295`로 고친 뒤 최종269행에서 확인했다. SCOPE에도 위치 정정 이력이 남았다. 사실 내용·목록 필드·동의어·순위·저작 수는 변하지 않았다. 이 감사자는 root 원장을 직접 수정하지 않았다.

## 4. PyLD 이식 계보와 구현 수

고정 [PyLD 소스 머리말 L1–5](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/lib/pyld/jsonld.py#L1-L5)를 직접 다시 열어 JavaScript 구현에서 이식했다고 적힌 것을 확인했다. [PyLD README](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/README.md#L40-L190)와 [jsonld.js README의 API 예제](https://github.com/digitalbazaar/jsonld.js/blob/27a2b812267fef702c0ac5260a7555d35c3af005/README.md#L195-L245)는 서로 다른 언어의 처리 코드·호출 계약을 제공한다.

따라서 다음 단위를 구분해야 한다.

- **저작:** jsonld.js와 PyLD의 고정 문서·소스는 서로 다른 구현 저작2개로 센다. 공급자 배당2개 산입은 타당하다.
- **코드 구현:** JavaScript와 Python의 자체 처리 코드2개다. PyLD를 JavaScript 엔진을 그대로 호출하는 CLI wrapper와 같다고 쓰면 안 된다.
- **개발 계보:** 이식 조상을 공유한다. 독립적으로 설계된 알고리즘 계보2개 또는 서로 독립적인 확인2개라는 표현은 피해야 한다.
- **시험 계보:** 두 구현 문서가 같은 W3C suite를 언급해도 서로 독립된 두 시험 저작이나 두 실제 통과 보고가 아니다. jsonld.js 실제 실행은 미실시이고, PyLD 실행은 본 연구자의 별도 진단이다.
- **CLI:** jsonld-cli는 고정 의존성과 호출 소스가 jsonld로 위임하므로 제품 진입점은 달라도 추가 독립 framing 엔진이 아니다. ajv-cli도 같은 원칙으로 Ajv와 구분해서 센다.

공통 저자/발행자 또는 포팅 계보를 보존한다는 것은 개별 구현 저작 자체를 무조건 한 저작으로 합친다는 뜻은 아니다. 이 과제의 최소 원문 수와 다른 상류 구현 수를 같은 숫자로 보고하지 않는 것이 핵심이다.

## 5. 출처 URL·판·위치 표본 감사

| 표본 | 실제 감사 범위 | 결과·제한 |
| --- | --- | --- |
| Schema 질문40개 | 저장된 최초 revision body를 SHA256으로 재계산하고 URL의 질문 ID·revision GUID와 대조 | 40/40 일치. API batch URL 하나에 담겨 있어도 저자 질문 ID가 다르면 40저작으로 구분 가능하다. |
| LD 질문40개 | revision-audit의 ID/GUID/body hash와 원장 연결 | 40/40 일치. 현재 snapshot에는 최초 body 원문 전체가 저장되지 않아 body hash 자체를 다시 만들지는 못했다. |
| SCH-Q05/09, LDQ-05 | 원문 ID·첫 revision 위치·요구 인용과 frame/requirements 연결 | 관측한 메타데이터 연결은 일치. LD 전체 원문 재심사가 아니다. |
| CAT002/006/007/010 | 고정 목록·계약·양식·LD YAML snapshot | 별도 저작의 실체와 기능을 확인. CAT006의 L291 위치 정정1건을 최종판에서 확인. |
| SD005/SD009/SD014 | 고정 default fixture, Ajv 문서, Python FAQ의 저장된 원문·위치 | 관련 조건과 예산 밖 제한이 일치. 실제 실행과 문서판을 합치지 않음. |
| LD-SUP-PY-DOC/LD-SUP-PY-API/LD-SUP-JS-DOC | 고정 GitHub URL에서 4회 지정 행을 직접 다시 열람 | blob SHA와 해당 내용 일치. port 계보와 aims-to-conform/skip 문구를 확인. |
| AUTH-LC1/LC2 | 원 JSON의 concept URI·추출 필드·receipt | 선호어/이형어/상위/관련 관계와 URI가 일치한다. |
| AUTH-AAT1/AAT2 | 저장된 record 정리·HTTP receipt의 URL·concept ID·응답 해시 | 두 다른 개념 URI의 구분 일치. 이번 감사에서 Getty HTML 전체를 재열람하지는 않았다. |
| SCH-STD-VALID20 | 정정된 원장과 SCOPE 및 SCH-STD-VALID20-RECHECK | 처음 목차에서 본 6.5.4/9.2를 본문 근거로 산입하지 않는 정정이 보존돼 있다. 기존 판에 없었던 사전 직접 열람으로 소급하지 않는다. |

리뷰 중 새로 수행한 제한된 원문 재열람4회는 `source-audit-sources.jsonl`에 사용자 지정 필드로 남겼다. 최초265행 뒤에 생긴 **동일 저작 재확인4행**이며 root가 최종 통합한269행에 포함됐다. 신규 고유 원문/배당 증가는0, direct_primary는186→190이며 고유109·배당24는 그대로다. 또한 중복된 root 라이선스 행을 실제 읽은 리뷰 담당자의 AUD-SC032-LICENSE 한 행으로 바꿔 순증0으로 처리한 것을 확인했다.

## 6. 재현과 수용 범위

```bash
python -B docs/workstreams/research/AF-RES-056/evidence/review/source_audit.py
```

최종 실제 실행의 종료 코드는 **0**이었다. 269행 첫 재실행에서는 새 자료종류의 일반 `라이선스` 표기를 감사 분류기가 아직 인식하지 못해 행별 일치 검사만 실패했다. `source-audit-receipt-269-first.json`에 그 exit1을 보존하고, 허가문 제외 규칙에 한국어/영어 license 표기를 명시해 다시 검사했다. 이는 원문·배당 결론을 바꾼 조정이 아니다. 이 명령은 root의 집계 스크립트를 호출하지 않고 읽기만 하며 review 폴더의 receipt를 갱신한다. root 원장이 다시 바뀌면 실행할 수 있다. 현재 265행 이전판과 269행 첫 검사/최종 검사는 각각 다른 receipt에 보존돼 있다.

현재 수용할 수 있는 결론은 **명시된 저작 경계에서 24배당의 원장·집계 일치**이다. 이 감사는 역사적 모집의 완전성, 모든 원문의 의미 정확성, 독립 적합성 시험 통과, 실제 독자의 채택을 새로 확인하지 않았다.

## 남는 약점 3건

| 불일치·약점 | 영향받는 주장 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| CAT006의 이전 위치가 L291을 누락했음 — 정정 완료 | 필수 데이터 필드의 정확한 인용 위치 | tooling-data.schema.json L291–292; source_id CAT006; SCOPE 위치 정정 이력 | 최종 수용 원장에서 정정된 원장 위치를 사용 | 내용 자체가 다르면 필드 설명을 재판정; 현재는 위치만 정정되어 결론 동일 |
| 목록 계약·제출 양식의 저작 경계가 같은 편집 시스템에 의존 | 공식 목록·편집 규칙4/4 산입 | CAT002/006/007/010 | 결과/수용 원장에 별도 파일의 목적과 공통 계보 및 22/24 민감도를 함께 명시 | 평가 기준이 시스템 단위를 요구하면 해당 배당은2/4로 변경 |
| LD 최초 본문 전체가 감사 snapshot에 없어 40 body hash를 재계산하지 못함 | 80질문 전체에 대한 독립 복원 검증이라는 더 강한 표현 | evidence/ld-pre/revision-audit.json 및 원장 LDQ-01..40 | 필요 시 동일 ID의 보존된 첫 revision body 응답을 제공받아 기존 hash 재계산 | 원문·GUID·hash 불일치가 나오면 해당 질문 복원과 요구 조건 재검토 |

