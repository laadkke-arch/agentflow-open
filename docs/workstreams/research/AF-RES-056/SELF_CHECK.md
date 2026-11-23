# AF-RES-056 자체 검토

## 검토 결론과 주체

**현재 공개 태그 코호트의 고정 8요구·16비교에서는 V가 후보 1개를 추가했지만, 허용 창의 같은 시행에서 두 조건을 확인한 완결 구현이나 한 조건을 확인한 부분 구현은 늘지 않았다.** 새 후보는 미확인이며, 이를 번역 오탐 1개나 구현 미지원 1개로 바꾸지 않는다. 이 결론은 현재 모집·게시 필드·사전 용어·원문 두 동작이라는 제한 아래의 관측이다. 역사적 모집 전체나 용어 연결의 일반 효용을 판단한 결론은 아니다.

작성·집계 교차 검토: `/root/catalogs`. 이 담당자는 공식 목록 복원과 Schema 예산 밖 진단을 작성했고, root의 최종 출처 집계를 별도 코드로 다시 계산했다. 따라서 자신의 자료를 포함한 팀내 자체 검토이다. `/root/authority_records`는 전거 조사와 일부 Schema 선정 경계 검토, 별도 순위·창 계산 감사를 수행했다. root는 요구 계약 통합·본표·SC032 경로와 C++ 진단을, JSON-LD 담당은 해당 모집·표준·공급자 및 PyLD 진단을 수행했다. **외부·인간·맹검 독립 검토가 아니다.** Git 선후와 역할 분리는 기록했지만 인지적 비노출 전체를 증명하지 않는다. 감사자가 공급자 실행을 독립적으로 재실행한 것으로도 표시하지 않는다.

이 문서는 원장, 두 필수 표, 하위 결과, 실제 검사·실행 영수증을 대조한 자체 검토이다. 문서 작성 때의 집계는 `evidence/review/source-audit-receipt.json`에 고정된 269행판이다. 최종 결과 커밋의 원격 재열람과 session check는 별도의 최종 발행 검증으로 확인해야 하며, 여기서 미리 성공했다고 표시하지 않는다.

## 1. 예정 분모·실측 단위·표와 원장의 대응

| 검토 대상 | 예정 또는 해석 단위 | 확인한 값과 근거 | 제한 |
| --- | --- | --- | --- |
| 질문 모집 | 각 태그 생성일·ID순 최대40 | `frame.csv` 80행: JSON Schema40 + JSON-LD40 | 현재 canonical tag에서 복원한 모집이다. 삭제·태그 제거·과거 별칭까지 포함한 당시 전체 모집은 미확인 |
| 선정 요구 | 두 필수조건을 가진 분야별 첫4 | 8개: Schema 원순위5/7/8/9, LD 원순위1/3/5/7; `requirements.json` | 최초 본문80/80 직접 열람 기록과 역사적 전체 모집80건 확보는 다름 |
| L/V 비교 | 8요구×2방법 | `matches.csv` 16행; RESULT 첫 표16행, 둘째 표8행 | 추가어가 실제 생긴 요구는4/8. 8개 모두 동일 강도의 개입이 아님 |
| 게시 목록 | 분야별 첫40까지 | `catalog.csv` 62행: Schema40, LD22에서 소진 | 전체 생태계나 독립 상류 엔진62개를 뜻하지 않음 |
| 사전 용어 | 원문 기능구·허용/보류 관계 | `vocabulary.csv` 37행: literal20, V 허용7, 보류10; 중복을 뺀 추가 질의6 | 표준어의 존재를 원 요구 두 조건의 구현 성공으로 올리지 않음 |
| 결과 자리 | 16비교×3 | `slots.csv` 48행: 채움1, 실제 무매치45, 매치풀 소진2 | 무매치45와 풀 소진2를 접근 실패나47개 구현 실패로 세지 않음 |
| 주 경로 | 대표 하나 / 대표→첫 정보 링크 / 대표→둘째 정보 링크 | JS-4-V-P1/P2/P3의 **3경로**, 행동수1/2/2 | 같은 README를 재사용한 대안 경로이다. 독립 독자3명이나 독립 반복실험3회가 아님 |
| 창 원장 | 빈자리 행 + 경로별 행동 행 | `windows.csv` **52행 = 빈자리47 + 논리적 행동5** | 한 시행에서5번 열람하거나52번 원문을 연 것이 아님 |
| 판정 원장 | 빈 비교·주 경로·진단 분리 | `judgments.csv` **19행 = 빈 비교15 + 주 경로3 + 예산 밖 진단1** | 본표 판정은18행. 추가 진단1을 본표 부분 성공으로 넣지 않음 |
| 본표 관측 | 같은 시행·같은 구현/판의 C1/C2 | 완결 관측0, 부분 관측0; 후보1개는 세 경로 모두 미확인 | 미확인을 확정 오답으로 바꾸지 않음. 정확도·오탐률은 산출 근거 부족 |
| 출처 전체 | 열람 행·고유 저작·필수 배당 분리 | **269행 / 고유 직접 1차 저작109 / 필수 배당24** | 109개 저작의 모든 본문을 감사자가 새로 재열람했다는 뜻은 아님 |

RESULT 첫 표의 비교 키는 `case_id`+`method`이며 `matches.csv` 16개 비교 및 `slots.csv`의 세 자리와 연결된다. 둘째 표는 같은 8개 `case_id`로 연결된다. 유일한 후보 SC-032의 게시 원순번32는 원데이터 순번6과 다르며, 반환에는 게시 순번을 썼다. 해당 세 경로의 판단은 `J-JS-4-V-P1/P2/P3`, 예산 밖 C2 진단은 `J-JS4-DIAG-C2`이다. 나머지15개 빈 비교는 `J-<비교ID>-EMPTY`이며 가상 공급자나 가상 열람 근거가 없다.

`관측 0`은 실제 규칙을 적용한 분모에서 해당 관측이 없음을 뜻한다. L 기존 후보0에서 탈락·밀림을 시험하는 조건부 분모는0이므로 `해당 없음`이다. 근거가 부족한 SC-032의 조건 충족은 `미확인`이고, 원 프로그램·원 credential 전체나 공식 전체 suite를 실행하지 않은 절차는 `미실시`이다.

## 2. 원문 배당과 독립성의 경계

| 필수 자료군 | 최소/확보 | 배당 source_id | 중복 배제 확인 |
| --- | --- | --- | --- |
| 사용자 질문 | 8/8 | SCH-Q05/07/08/09; LDQ-01/03/05/07 | 질문 ID별 저작. batch API 전송 하나를 한 저작으로 합치거나 질문 개정판을 새 저작으로 더하지 않음 |
| 공식 목록·별도 편집 규칙 | 4/4 | CAT002/006/007/010 | 목록 HTML/data/renderer는 각각 한 목록. 별도 데이터 계약과 제출 양식의 목적·같은 편집 계보를 공개 |
| 표준·공개 적합성 시험 | 4/4 | SCH-STD-VALID07; SD001; LD-STD-API; LD-TEST-01 | 같은 표준의 draft 변형, 같은 suite의 여러 입력·출력·미러는 중복 산입하지 않음 |
| 공급자 판별 자료 | 4/4 | SD009; SD014; LD-SUP-JS-DOC; LD-SUP-PY-DOC | 공급자 매뉴얼의 여러 절·소스·릴리스·runner는 해당 구현 저작으로 합침 |
| 전거 개념 레코드 | 4/4 | AUTH-LC1/LC2/AAT1/AAT2 | LOC2·Getty AAT2. 같은 URI의 JSON/HTML/연례 재수록·번역은 한 개념 |

총269행은 직접 1차 자료190, 실패40, metadata·허가문18, 미러2, 내부 입력·자체 실행19로 나뉜다. 자체 실행3행과 내부/선행16행은 고유109·배당24에서 제외했다. 이 네 수를 서로 바꾸어 보고하지 않는다. 자세한 행 위치와 대표 URL은 `evidence/source-counts.json`·`evidence/primary-works.csv`에 있다.

**동일 편집 시스템으로 묶는 민감도:** Schema 목록·데이터 계약·제출 양식을 모두 한 저작으로 합치면 목록/편집 배당은2/4, 전체 배당은 **22/24**, 전체 고유 work_id는107이 된다. 본집계는 두 별도 편집 산출물의 다른 목적과 내용에 근거한 저작 경계를 쓴다. 4개 독립 편집기관이나 적합성 검증 원천이라고 주장하지 않는다. 더 엄격한 경계를 택한다면 해당 결손을 많은 추가 질문으로 채웠다고 할 수 없다.

**공급자 저작과 엔진 계보:** Ajv·python-jsonschema·jsonld.js·PyLD는 배당4개 저작이다. PyLD는 JavaScript 구현을 Python으로 이식했다는 [고정 소스 L1–5](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/lib/pyld/jsonld.py#L1-L5)를 확인했다. 별도 처리 코드/저작2개와 독립적으로 개발한 계보2개를 혼동하지 않는다. jsonld-cli와 ajv-cli는 각각 기존 processor를 호출하는 제품 진입점이므로 별도 독립 엔진으로 더하지 않는다.

**최초 본문 감사의 실제 범위:** Schema40개는 보존된 revision1 body에서 SHA256을 다시 계산했다. LD40개는 질문 ID·revision GUID·body hash를 원장과 revision-audit 사이에서 대조했지만, 감사 스냅샷에 최초 body 전체가 없어 해시 자체를 재계산하지 못했다. **“80질문 전부를 독립 재해시했다” 또는 “80개 원문을 독립 맹검 재검토했다”라고 쓰지 않는다.** 담당자의 최초80개 직접 열람 기록은 이 후속 감사와 별개다.

## 3. Q1 — 입력과 반드시 함께 성립할 두 조건

### 직접 원문과 판정 위치

아래는 각 질문의 최초 revision1 본문을 읽은 위치이다. 실제 복원 전송 URL·GUID·body hash는 source_id와 `frame.csv`의 같은 ID를 따른다. 원문 링크의 현재 본문을 최초판으로 가정하지 않는다.

| 요구·출처 | 최초판의 정확한 판정 위치 | 보존한 C1/C2와 환경 경계 |
| --- | --- | --- |
| [JS-1 / SCH-Q05](https://stackoverflow.com/questions/65660787/how-to-set-one-schema-for-n-1-elements-and-another-for-the-nth-element) | array schema, 허용 `[3,4,5,"hello"]`·거부 `[3,"hello",4,5]`, 마지막 선택성 설명 | 마지막 이전 숫자 / 마지막 문자열 선택적 허용. 빈 배열의 기대·구현판은 미명시 |
| [JS-2 / SCH-Q07](https://stackoverflow.com/questions/65699699/validate-json-schema-with-another-json-schema) | 첫 요구 문단, sample JSON, simpleTypes enum 수정의 실패 설명 | schema root=object / property type명은 string·number·integer·boolean. draft07 명시 |
| [JS-3 / SCH-Q08](https://stackoverflow.com/questions/65726164/how-to-use-ajv-with-dependent-json-schemas) | types.json의 gender enum과 Person.sex의 `$ref`, Person required, isPerson 호출 | 외부 참조·enum 적용 / 필수 속성 유지. Node.js/TypeScript·Ajv 이름 노출; 판 미명시, draft04/$id 혼재와 email guard 보존 |
| [JS-4 / SCH-Q09](https://stackoverflow.com/questions/65731152/jsonschema-validate) | 첫 세 요구 문단, columns/pii 예제 | pii는 동적 열 이름 집합 안 / datatype명은 integer·string·object. Python3; 값 존재 문의를 빈 문자열 금지로 자동 구체화하지 않음 |
| [LD-1 / LDQ-01](https://stackoverflow.com/questions/65565025/how-to-generate-breadcrumb-schema-dynamically-using-javascript) | breadcrumb 입력, 원하는 ListItem 출력, head.appendChild 코드 | 순번·이름·계층 URL 보존 / 생성 script의 head 부착. JSP/JSTL·JavaScript/jQuery 노출; head는 코드 근거 |
| [LD-2 / LDQ-03](https://stackoverflow.com/questions/65835110/in-aem-i-want-to-add-sly-sly-tags-inside-a-script-script-tag-multifiel) | 조건부 script 설명, HTL 입력, 원하는 mainEntity의 여러 Q/A 출력 | 값이 있을 때만 출력 / 여러 작성 Q/A 쌍 보존. AEM/HTL 명시, 제품판 미명시 |
| [LD-3 / LDQ-05](https://stackoverflow.com/questions/65917156/how-to-filter-json-ld-object-array-with-json-ld-frames) | 원 credential/context, values의 두 객체, a=1 필터와 나머지 유지 설명 | a=1 객체만 선택 / 그 b,c 및 다른 credential 필드 보존. jsonld.js 링크 노출, 설치판 미명시, context @version1.1 |
| [LD-4 / LDQ-07](https://stackoverflow.com/questions/66023851/calling-a-json-file-with-php-but-cant-echo-in-a-way-i-would-like-to) | ALGYO/ACSEL 지정, 종목/가격 예제, PHP 출력 코드 | 지정 종목만 선택 / 각 종목과 해당 가격을 행에 짝지음. PHP판 미명시 |

| 검토 항목 | 자체 검토 |
| --- | --- |
| 주장 | 현재 공개 태그의 시간 필터 첫40씩에서 원문 목적과 두 조건으로 4개씩 골랐다. 조건은 원문 prose뿐 아니라 명시 예제·코드에서 추출했으며 최신판·자동 보정·언어 교체를 덧붙이지 않았다. |
| 직접 근거 URL·정확 위치 | 위 8개 원문·revision1 위치, `evidence/schema-pre/requirements.json` 및 `evidence/ld-pre/requirements.json`의 C1/C2·guard·인용 위치, `frame.csv`의 원순위·GUID·제외 사유. 고정 [stage1 요구 계약](https://github.com/laadkke-arch/agentflow-open/blob/1f63f0129207904a91ae9e01bb3e48c86415a644/docs/workstreams/research/AF-RES-056/requirements.json)은 후보 순위보다 앞선 판이다. |
| 반대 증거 또는 반례 탐색 범위 | Schema 앞선1–9번의 제외 경계를 팀내 재검토했다. 국가/지역 UI 요구는 두 조건이 없어서가 아니라 validation/annotation 범위 밖으로 제외했다. 반대로 LD는 웹 작성 데이터→JSON-LD 생성·추출을 포함하여 LD1/2/4가 processor 핵심 알고리즘 요구와 다르다. LD1/2의 최초판에 json-ld 태그가 없었고 후일 추가된 사실, 초기 LD score/answer_count 일부 노출, Schema 일부 후속판 노출도 기록했다. |
| 결론이 틀릴 조건 | 현재 프레임보다 앞서는 당시 적격 질문이 삭제·태그 제거·별칭 때문에 누락됐거나, 최초판 두 조건을 잘못 읽어 첫 적격4가 달라지는 경우. LD를 expand/compact/flatten만으로 좁힐 경우에는 별도 표본 설계가 필요하다. |
| 미확인과 최소 재개 자료 | 2021–2024의 당시 질문·태그·삭제/이동·별칭 상태를 복원할 날짜가 명확한 공개 스냅샷과 PostHistory/TagSynonyms, 동일 ID의 최초 본문 응답. 2024 cutoff 자료 한 벌만으로 더 일찍 삭제된 질문까지 복원됐다고 가정하지 않는다. 원 프레임은 유지하고 새 모집판을 별도로 동결해 앞선 적격 질문이 있는지 먼저 비교한다. |

## 4. Q2 — 표준 기능명으로 옮길 수 있는 관계

| 검토 항목 | 자체 검토 |
| --- | --- |
| 주장 | V는 L에 근거 있는 정의 관계만 더했다. JS-2 meta-schema, JS-3 schema references/dereferencing, JS-4 validation/enum, LD-3 framing이 허용됐다. enum은 JS-4의 C2에만 대응하며 C1까지 해결한다는 뜻이 아니다. 넓은 말·관련어·반대 방향은 보류했다. |
| 직접 근거 URL·정확 위치 | [draft07 Core §3.1·§4.3.2](https://json-schema.org/draft-07/draft-handrews-json-schema-01), [draft04 Core §7.1·§7.2.2·§7.2.3](https://json-schema.org/draft-04/json-schema-core), [draft07 Validation §6.1.1/2·§6.4.1/6·§6.5.3/7·§10.2](https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01), [2020-12 Validation §7.2.1–2](https://json-schema.org/draft/2020-12/json-schema-validation), [JSON-LD API §2.1–2.4·§8.1·§8.4](https://www.w3.org/TR/2020/REC-json-ld11-api-20200716/), [Framing §2.1.1·§4.2](https://www.w3.org/TR/2020/REC-json-ld11-framing-20200716/#frame-matching). `vocabulary.csv` 37행의 관계·방향·보류 사유와 source_id SCH-STD-*, LD-STD-*가 연결된다. |
| 반대 증거 또는 반례 탐색 범위 | contains는 어느 위치의 존재이지 선택적 마지막 요소가 아니며, primitive type을 표준 type 전체로 옮기면 허용 집합을 넓힌다. properties의 의존과 외부 schema 참조를 나눴다. default 주석을 값 삽입으로, compact를 expand로, DOM/AEM 조건·PHP 행 출력을 graph framing으로 바꾸는 대응을 보류했다. `validate`→`validation`은 정의 근거로 사전 허용했지만, `validation`→`Validator`의 행위/행위자 파생형 연결은 허용하지 않았다. |
| 결론이 틀릴 조건 | 허용된 대응이 원문의 입출력 방향·부정·판 조건을 바꾸거나, 표준 정의의 적용 범위를 잘못 읽은 경우. 반대로 보류어가 두 조건을 보존한다는 정확한 정의가 추가 확보되면 새 사전 규칙의 비교는 달라질 수 있다. 결과를 본 뒤 단어를 늘린 수치를 기존 V 효과로 합칠 수 없다. |
| 미확인과 최소 재개 자료 | 새 후보어의 정확한 표준판·URI·정의 절, 방향을 가르는 양성/근접 음성 입력이 필요하다. 최초 SCH-STD-VALID20 위치에 목차6.5.4/9.2를 본문처럼 적었던 과장은 §7.2.1–2로 정정했고 dependentRequired 본문은 사후 RECHECK로 분리했다. JS-V12는 전후 모두 보류라 허용어·순위는 변하지 않았다. 다음 연구에서도 구현 결과를 보기 전에 새 용어표를 봉인한다. |

원격 순서는 사전 범위 `628c330941babcb43b636d0a37ecb073b2c9d107` → 모집/용어 `1f63f0129207904a91ae9e01bb3e48c86415a644` → 목록/순위 `b765a189aa2a1f5982a4994fc0476273abbf7127`이다. stage1→stage2의 요구·프레임·용어표 내용은 같다는 검산이 있다. CSV의 작업트리 CRLF와 Git LF 해시 차이도 동일 내용의 줄끝 변환으로 재현됐으며, 새 용어 추가로 해석하지 않았다.

## 5. Q3 — 실제 검색 필드와 목록판

| 검토 항목 | 자체 검토 |
| --- | --- |
| 주장 | Schema 첫40은 제목과 표시 기능 분류 Validator를 검색하고, LD22는 제목만 검색한다. 두 목록의 명시 별칭은 없다. LD 언어/CLI 표제는 소속이며 기능으로 승격하지 않았다. 목적지에서 알게 된 기능·시험 성적을 목록에 역으로 채우지 않았다. |
| 직접 근거 URL·정확 위치 | Schema [고정 데이터](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/data/tooling-data.yaml), [정렬·그룹 변환 L49–61·L186–231·L242–358](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/pages/tools/hooks/useToolsTransform.tsx), [표시·Load More L45–98·L178–353](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/pages/tools/components/ToolingTable.tsx), [모달 L81–159·L327–346](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/pages/tools/components/ToolingDetailModal.tsx). LD [index.yaml L1–115](https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/index.yaml), [그룹 L66–106](https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/index.liquid), [item L1–12](https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/_includes/implementation-item.liquid), [card L1–33](https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/_includes/implementation-card.liquid). |
| 반대 증거 또는 반례 탐색 범위 | Schema 초기에 그룹별5개만 보이는 행을 첫40으로 취하는 해석을 폐기하고, Load More로 전부 펼친 게시 순서의 첫40으로 목적지 판정 전에 고쳤다. 초기 표시89행과 LD22행의 이름·소속·환경 필드를 live 파싱 결과와 대조했다. 실제 기능은 모달 설명·공급자 소스에 있지만 고정 표시 필드에 없는 경우를 LD-3에서 찾았다. 목록이 비어 있거나 접근 실패한 경우와 기능 열 부재는 다르다. |
| 결론이 틀릴 조건 | 소스의 default 정렬/obsolete 제외/그룹 순서가 실제 발행 화면과 다르거나, 원래 보이는 alias/기능 필드를 누락했거나, 첫40을 잘못 잘랐을 경우. Schema 사이트 자체의 Fuse 이름 검색을 L/V의 정확 기능구 일치와 같은 검색이라고 주장할 경우에도 설명이 틀린다. |
| 미확인과 최소 재개 자료 | 실제 배포 전체와 고정 Git SHA가 완전히 동일하다는 배포 증명 및 브라우저 클릭 실측은 없다. 부분 화면·소스 순서 일치로 한정했다. 배포된 데이터/렌더러 commit 또는 당시 전체 화면 응답이 최소 자료다. 목록 Load More·모달·Source 링크 준비는 이미 주어진 목록으로 모델링했고 공급자2동작에 넣지 않았으므로, 실제 UI 클릭 연구는 별도 예산으로 사전 설계해야 한다. |

CAT006의 데이터 계약은 `/items/required`, L291–292가 정확하다. 원장 L292–295를 L291–295로 정정한 이력은 SCOPE에 남았고 목록·매치 결과는 같았다. Bowtie 동적 API를 호출하는 코드가 있다는 것은 보았지만, 그 성적을 이번 후보 선택 필드로 읽어 채우지 않았다. 원 목록이 복원돼 사전 대체 목록은 쓰지 않았다.

## 6. Q4 — 같은 예산의 신규·탈락·동률

| 검토 항목 | 자체 검토 |
| --- | --- |
| 주장 | L은8/8 빈 반환, V는JS-4에서만 SC-032 원32를 추가했다. 다른7요구는 빈 반환 동률이다. L 기존 항목이0이어서 탈락·밀림은 해당 없음이다. 한 후보에 대한3경로를 나누고 같은 시행의 근거만 판정했다. |
| 직접 근거 URL·정확 위치 | [stage2 matches.csv의16개 comparison_id](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/matches.csv), [slots.csv의48개 slot_id](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/slots.csv), [catalog.csv의 SC-032·posted_rank32](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/catalog.csv). 원 링크 순서는 [README L8·L9·L14–15](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/README.md#L8-L15); 첫 두 링크만 주경로에 썼다. |
| 반대 증거 또는 반례 탐색 범위 | 별도 순위 계산기는 전체16비교·48자리를 다시 계산했다. validation은 Validator와 다른 단어이며 이어 붙인 DSJSONSchemaValidation 내부 문자열도 단어 경계 때문에 매치하지 않았다. 정확 URL만 중복 제거했다. 사전 framing 제거와 슬롯3→4 감도는 후보 집합 변동0이었다. 셋째 정보 링크를 더 유리하다는 이유로 선택하지 않았다. |
| 결론이 틀릴 조건 | 허용 용어·검색 필드·정렬·정확 URL 중복·단어 경계 중 하나가 실제 사전 규칙과 다르거나, 새로운 고정 목록/요구에서 L 기존 항목이 있고 V가 그 항목을 밀거나 완결 구현을 추가하는 경우. 현재 무변화 감도는 풀 최대1이라 변화 기회가 없는 결과다. |
| 미확인과 최소 재개 자료 | 기존 정답 보존이나 순위4의 효과를 시험할 조건부 표본이 없다. 다음 비교에는 L이 이미 후보를 반환하는 사전 표본과 더 큰 매치풀이 필요하다. 이번자료에서 제목/공식 표기가 이미 충분한 요구는 관측0이며, 그것이 생태계 전체에 없다는 결론은 아니다. 실제 클릭·채택·읽기 시간은 미측정이다. |

본표 단위는 후보 도구1, 주경로3, 고유 도착 문서3이며 **조건 입증에 기여한 허용 창 문서0**이다. 소개 문서와 메타스키마를 추가 구현으로 세지 않는다. 목록 전체의 이름62개·정확 목적 URL과 상류 구현의 독립성도 같은 수가 아니다. 공유 엔진 확인은 별도 진단이다.

## 7. Q5 — 같은 구현·판에서 두 조건이 함께 있는가

| 검토 항목 | 자체 검토 |
| --- | --- |
| 주장 | SC-032의 세 주경로 모두 C1/C2 미확인이다. 첫 창의 일반 validation·C++·draft7/version2 설명만으로 원 Python 요구의 동적 pii와 datatype 세 값 제약을 함께 확인하지 못했다. 예산 밖 C2 시험을 본표의 부분 성공으로 올리지 않았다. |
| 직접 근거 URL·정확 위치 | [SC-032 README@d5199551… L3–106의 렌더500단어](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/README.md), [동일 시점에 캡처한 소개 페이지](https://json-schema.org/)의 web L6–105 렌더500단어, [두 번째 링크의 도착 JSON](https://json-schema.org/draft/2020-12/schema)의 `$schema/$id/$vocabulary/title`. source_id WIN-01-V2/02-V2/03과 `windows.csv`의 P1/P2/P3가 연결된다. 예산 밖은 [CMake L14](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/CMakeLists.txt#L14), [enum L551–560](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/src/json-validator.cpp#L551-L560), `sc032-execution.json`이다. |
| 반대 증거 또는 반례 탐색 범위 | draft7이라고 붙인 `/schema` 링크가 현재2020-12로 이동하는 판 불일치가 있었다. JSON 전송은 복구했으나 제목 기준 창은 사전 미정이다. README의 포괄 성적 설명 L271–280과 같은 SHA의 [known-failures.json](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/test/JSON-Schema-Test-Suite/known-failures.json)도 대조했다. 표준 정의, harness의 기대값, 구현 실제 통과는 구분했다. |
| 결론이 틀릴 조건 | 같은 고정 응답의 허용500단어·허용된 정확 절·한 경로 안에 원 환경과 옵션에 맞는 C1/C2 공동 근거가 실제 존재한다면 미확인 판정을 바꾼다. 반대로 창에 안 보인다는 이유만으로 라이브러리 전체의 불가능을 결론내리면 이 연구가 틀린다. 언어 교체를 허용하는지 모르는 상태에서 C++/Python 차이를 의미 번역 오류로 확정해도 안 된다. |
| 미확인과 최소 재개 자료 | JS-4 원 Python 패키지/판·schema·동적 columns 처리·값 존재 guard의 정확한 뜻과 동일 입력의 양성/근접 음성 출력이 필요하다. SC032의 build2.4.1은 CMake에서 예산 밖으로 확인했으며 최초 창에 소급하지 않는다. LD-3도 원 credential·remote context 판·원 jsonld lock·명시 frame 옵션의 공동시험이 필요하다. 현재 공급자 소스 링크는 보완 역할이며 완결 대안 반환은 보류한다. |

창 추출의 실제 결함을 보존했다. 최초 v1은 raw Markdown500을 세어 렌더링하면 README487·홈페이지479단어였다. 동일 응답을 렌더링500 기준으로 정정한 v2에서 첫 두 링크·C1/C2 판정은 같았다. 검토자의 최초 권고는 사후 감도로만 보존하는 것이었고 root는 원래 렌더500 규칙의 기계 구현 정정으로 최종 채택했다. 당시 이미 추가 본문·진단을 읽은 뒤였다는 노출과 이 판단 차이를 숨기지 않았다. v2를 비노출 상태의 최초 관측이라고 부르지 않는다. 제목 없는 JSON 전체를 사후 허용하는 감도에서도 구현 공동 근거는 생기지 않지만, 이를 사전 규칙으로 바꾸지 않았다.

## 8. Q6 — 번역이 틀리는 입력과 실제 반증

| 검토 항목 | 자체 검토 |
| --- | --- |
| 주장 | 표준 기능 이름이 맞아도 입력 방향·주석/수정·format 옵션·객체 경계·구현 계보를 잘못 옮기면 요구를 놓친다. 분야별 공식 양성/근접 음성 자료를 직접 읽었고, 별도의 작은 로컬 진단을 실행했다. 실제 실행의 예상 불일치도 유지했다. |
| 직접 근거 URL·정확 위치 | Schema suite 고정판의 [enum /tests/0, L5–21](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/enum.json#L5-L21), [ref L38–57·L231–258](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/ref.json#L231-L258), [default /tests/2, L52–81](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/default.json#L52-L81), [date L44–86](https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/e2a68a15cd490750fd6b95e604e4054d7d978d1f/validation/tests/format-date.json#L44-L86). LD suite [expand-manifest의 tn006/tn007/ten01](https://github.com/w3c/json-ld-api/blob/fd4f7eb41f679fb73a54923143c473c3a1d06093/tests/expand-manifest.jsonld), [n006 입력](https://github.com/w3c/json-ld-api/blob/fd4f7eb41f679fb73a54923143c473c3a1d06093/tests/expand/n006-in.jsonld)·[기대 출력](https://github.com/w3c/json-ld-api/blob/fd4f7eb41f679fb73a54923143c473c3a1d06093/tests/expand/n006-out.jsonld), [en01 문자열 @nest 음성](https://github.com/w3c/json-ld-api/blob/fd4f7eb41f679fb73a54923143c473c3a1d06093/tests/expand/en01-in.jsonld), expand/compact 0002 입력·context·출력을 각 전체 JSON으로 읽었다. |
| 반대 증거 또는 반례 탐색 범위 | enum 내부의 `$ref` 객체는 참조 실행이 아닌 리터럴 비교라는 반례, maximum3/default5의 누락 `{}`와 명시5, 같은 날짜쌍의 format checker on/off, C2-only schema가 잘못된 pii를 수락하는 예를 확인했다. LD의 @nest는 노드 속성들을 합치며 원 객체 조합을 보존한다고 가정하면 안 된다. PyLD 근접 음성의 예상은 C1/C2=false였으나 실제 frame 예외가 발생했다. jsonld.js의 JSDoc 기본값과 코드 기본값 불일치, CLI의 processor 위임, PyLD 이식 계보도 조사했다. |
| 결론이 틀릴 조건 | 원본 두 조건과 환경을 보존한 동일판 실행이 반례를 구분하지 않거나, 명시적으로 허용한 확장·전처리·옵션이 두 조건을 함께 충족하면 해당 진단의 적용 범위를 바꿔야 한다. 연구자 최소 입력의 성공을 원 credential/프로그램 전체 성공으로 읽거나 작은 실패를 라이브러리 전체 한계로 일반화하면 결론이 틀린다. |
| 미확인과 최소 재개 자료 | 공식 전체 suite·공급자 회귀시험의 이 판 실행/EARL 보고는 미확보 또는 미실시다. Ajv8.17.1과 python-jsonschema4.23.0 문서가 그대로 실제 실행됐다는 증거도 없다. CLI의 정확 의존 minor를 판정하려면 당시 잠금파일/설치환경의 npm ls가 필요하다. 원 요구 공동시험에는 원 입력·고정 context·패키지 lock·옵션·출력을 함께 고정해야 한다. 아래 실제 실행표와 하위 replay 문서가 정확한 재개 입력이다. |

### 실제 실행과 문서 독해를 혼합하지 않았는가

| 항목 | 실제 시행·관측 | 합치지 않은 주장 |
| --- | --- | --- |
| Schema 공식 fixture 일부 | 설치 python-jsonschema4.26.0에서14건: 해당 profile 공식 기대값12/12 일치, format OFF 통제2는 모두 유효. 입력 변이0/14. `evidence/schema-diagnostics/runtime-receipt.json`·`execution-output.json` exit0 | v4.23.0 문서판의 실행, 전체 suite 통과, 원 요구8개의 공동 충족 아님 |
| SC032 C2-only 연구 fixture | 같은 d5199551… 소스와 nlohmann3.12.0@55f93686…·g++14.2.0. string 수락·array 거절·없는 pii 수락. `evidence/windows/sc032-execution.json` build/run exit0 | 원 Python 환경·동적 C1·값 존재 guard의 완결 아님. `desired_full_contract_accept`는 두 분석조건의 연구자 oracle이라는 명명 정정 보존 |
| PyLD3.3 최소 양성/음성 | 원 질문 전체가 아닌 로컬 문맥의 입력2개. 별도 노드 양성은 이 작은 입력의 a=1 선택과 b/c/issuer를 보존. @nest 음성은 예상한 false/false 대신 FrameError여서 최초 runner exit1 유지 | 원 credential 성공, 모든 @nest frame 불법, 공식 suite 통과 아님 |
| PyLD 원인 진단 | 새 DIAG-LD-NEST-CAUSE: expand가 a/b/c 값을 단일 노드에 합침. frame 충돌 keyword는 @requireAll. 원인 기록 exit0 | 새 진단 exit0을 최초 음성 예측의 통과로 합치지 않음. 고유 입력2·최초frame2·추가expand1/frame1 구분 |
| 공식 LD suite·자체 회귀 코드 | 고정 입력·기대 출력·manifest·assert를 직접 읽음 | 해당 공식 runner·회귀시험을 실제 통과했다고 쓰지 않음 |

[Ajv useDefaults 문서 L155–217](https://github.com/ajv-validator/ajv/blob/9050ba1359fb87cd7c143f3c79513ea7624ea443/docs/guide/modifying-data.md#L155-L217)와 [Python FAQ L100–209](https://github.com/python-jsonschema/jsonschema/blob/cfe8a4071672b9652c8f083faed1c4ffa7d67705/docs/faq.rst#L100-L209)는 삽입이 각각 옵션 또는 사용자 확장임을 보여준다. [Ajv formats L3–31](https://github.com/ajv-validator/ajv/blob/9050ba1359fb87cd7c143f3c79513ea7624ea443/docs/guide/formats.md#L3-L31)와 [Python format 함수 L223–228](https://github.com/python-jsonschema/jsonschema/blob/cfe8a4071672b9652c8f083faed1c4ffa7d67705/jsonschema/_keywords.py#L223-L228)는 초안명만으로 assertion 활성화를 추정하지 못하게 한다. 이것은 서로 다른 공급자 관점의 문서 근거이며 두 번의 독립 실행 성공이 아니다.

## 9. Q7 — 분야 밖의 전거 관계를 어디까지 옮길 수 있는가

| 검토 항목 | 자체 검토 |
| --- | --- |
| 주장 | 같은 개념 URI 안의 이형어와, 상하위·연관·산출물/행위 관계를 구분하는 원칙은 소프트웨어 용어 관리에 참고할 수 있다. 전거의 검색 접근점이 곧 알고리즘·입출력·옵션의 엄격한 동등성을 보증하는 것은 아니다. 이번 전거 사례가 L/V의 완결률 향상을 실증했다고 주장하지 않는다. |
| 직접 근거 URL·정확 위치 | [LOC Engraving sh85043995](https://id.loc.gov/authorities/subjects/sh85043995.json)의 해당 @id 노드 skos:prefLabel/altLabel/broader/narrower/related, [LOC Etching sh85045046](https://id.loc.gov/authorities/subjects/sh85045046.json)의 같은 필드. [AAT paintings 300033618](https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&subjectid=300033618)의 Full Record Terms·Note·Objects hierarchy·produced by, [painting 300054216](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300054216)의 Terms·Note·Activities hierarchy·produces/distinguished from. [Getty §3.1.1](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.1/), [§3.3.1/3/4/15](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.3/), [§3.5.1](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.5/)의 동일 매뉴얼 관계 규칙. |
| 반대 증거 또는 반례 탐색 범위 | Engraving↔Etching은 related이지 동의어가 아니다. paintings 작품과 painting 행위는 다른 URI와 scope를 가진다. 같은 Etching 철자의 [sh00005643](https://id.loc.gov/authorities/subjects/sh00005643.json)은 재료 아래 붙는 주제 세목이라 독립 표목 sh85045046과 범위가 다르다. AAT coating 구분도 확인했다. 연결된 사전·모든 상하위 레코드를 읽은 것으로 더하지 않았다. |
| 결론이 틀릴 조건 | 해당 URI의 범위·관계를 잘못 해석했거나 병합/폐기된 레코드가 드러나면 개별 사례를 재판정한다. 같은 표현이더라도 소프트웨어의 실제 방향·필수조건·판을 보존하지 못하면 V로 옮길 수 없다. 전거 규칙을 적용해 실제 검색 효과가 개선된다는 주장은 별도 비교에서 입증돼야 한다. |
| 미확인과 최소 재개 자료 | 전거 편집 원칙의 소프트웨어 적용은 제한된 설계 제안이다. 사용자에게는 원 질문/양성·음성 입출력, 편집자에게는 별칭의 표준 URI·정의·표시 필드와 판, 유지보수자에게는 같은 구현판·옵션·시험 입력/출력 링크가 필요하다. 다음 단계는 이 근거를 갖춘 새 기능 필드/동의어 개입을 결과 전에 동결해 비교하는 것이다. |

전거의 JSON·HTML·번역은 같은 개념이고 Getty의 여러 editorial 절도 한 저작이다. 미열람 Grove/Oxford 원저를 추가 산입하지 않았다. Full Record에 직접 하위어가 보이지 않는다고 하위어가 없다고 단정하지 않았다. software 분야 전이의 허용 조건과 독자별 링크는 `evidence/authority/findings.md`에 분리돼 있다.

## 10. 검사 범위와 남은 최소 재개

| 검사·행위 | 실제 상태 | 보존 근거 |
| --- | --- | --- |
| 사전 요구·용어·목록·16순위·48슬롯 재계산 | 실시; 별도 구현35검사, 최종 exit0 | `evidence/review/ranking-audit-receipt.json`; 최초 상태명 오기 실행exit1도 감사 설명에 보존 |
| 경로·창·판정·v1/v2 경계와 fixture 기록 감사 | 실시;31검사, 최종 exit0. 공급자 runtime 재실행은 하지 않음 | `evidence/review/window-audit-receipt.json`·`window-audit.md` |
| 원장 결합·고유/배당·원문 ID/위치 감사 | 실시;269행에서715검사, 최종 exit0 | `evidence/review/source-audit-receipt.json`;265행 및269첫검사도 별도 보존 |
| 두 필수 표·원장 ID 대응 | 이 SELF_CHECK 작성 시점의16행/8행·8 ID·16비교와 연결 확인 | RESULT 첫 두 표, matches/slots/windows/judgments |
| 원 요구 전체·공식 전체 suite·인간 독자 실험 | 미실시 또는 미측정 | 위 Q5/Q6의 구체 범위와 하위 진단 receipt |
| 최종 결과 고정SHA의 원격 RESULT·수용 원장 재열람 및 session check | 이 문서 작성 시점 미실시인 별도 최종 gate; 성공을 선기록하지 않음 | root가 최종 결과 커밋 뒤 보존할 명령 출력·종료 코드·UTC·원격 판 확인 기록으로만 완료 판단 |

이미 수행한 감사의 재생 명령은 다음과 같다. 새 증거를 얻는 명령과 같은 입력을 다시 계산하는 명령을 구분한다.

```bash
python -B docs/workstreams/research/AF-RES-056/evidence/review/ranking_audit.py
python -B docs/workstreams/research/AF-RES-056/evidence/review/window_audit.py
python -B docs/workstreams/research/AF-RES-056/evidence/review/source_audit.py
```

각 감사가 입력으로 쓰는 고정 Git 객체·창 receipt·원장 파일이 필요하다. source_audit.py의 Schema40 재해시에는 공개 저장하지 않은 최초 body 캐시도 필요하며, [재생 입력 안내](evidence/REPLAY.md)의 동일 ID·GUID·hash 검증으로 복구해야 한다. 캐시 없이 그 감사가 즉시 재생된다고 주장하지 않는다. 원래 홈페이지 응답이 없으면 나중의 live 홈페이지로 교체해 같은 창 검증이라고 할 수 없다. 공급자 재생은 `evidence/windows/FINDINGS.md`, `evidence/schema-diagnostics/FINDINGS.md`, `evidence/ld-suppliers/REPLAY_PLAN.md`의 정확한 SHA·입력·환경과 별도 출력 파일을 따른다. 해당 재생이 원 요구 전체를 검증하는 것은 아니다.

최종 결과가 커밋된 뒤 root가 실행할 고정 명령은 아래와 같다. 이 문서 자체는 그 실행의 receipt가 아니다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-056/manifest.json --fetch
```

source 배당과 현재 비교를 충족했다는 이유로 전체 수용을 완전 충족으로 올리지 않는다. 역사적 모집과 원 환경의 공동 구현 근거가 남은 경우, 관측한 분모·확보 실패·정확한 다음 입력을 가진 부분 인계를 유지한다.

## 11. 가장 중요한 불일치·약점 3건

| 불일치·약점 | 영향받는 주장 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| 현재 tag 첫40과 당시 전체 공개 모집의 완전성은 다름. LD1/2의 후속 태그 부착·과거 삭제/제거·별칭 결손이 남음 | “2021–2024 당시 첫 적격4씩에서 일반적으로 효과가 없었다”는 주장 | [고정 frame 80행](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/frame.csv), LD revision-audit의65565025/65835110 tag_revisions, sources SCH-TAG-ALIASES | 당시 날짜별 공개 Posts·PostHistory·TagSynonyms/삭제 전 스냅샷을 확보해 같은 생성일/ID 정렬 모집을 비교; LD 최초 body 전체 응답도 제공받아 hash 재계산 | 앞선 적격 질문·다른 최초 조건이 발견돼 첫4 또는 허용어가 바뀌면 별도 판을 사전 동결해 비교. 기존8자리를 사후 교체하지 않음 |
| 개입은 요구4/8·추가 질의6개에만 작용하고, Schema 파생형 불일치와 LD 기능 필드 부재를 해결하지 못함. catalog4 저작도 같은 편집 시스템 경계에 의존 | 표준 기능명 연결의 일반 효용·누락 감소·출처 완전성에 대한 과도한 결론 | [vocabulary.csv 37행](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/vocabulary.csv), catalog Schema40 Validator/LD22 title-only, CAT002/006/007/010 | 새 차수에서 파생형 관계 또는 표시 기능 필드를 별도 개입으로 고정. 출처 경계는2목록+2편집 산출물과22/24 민감도를 함께 보고 | 사전 근거가 있는 이름이 실제 게시 필드와 연결되어 같은 예산의 공동 근거를 추가하면 효용 판단 변경. 시스템 단위 저작만 인정하면 목록 배당2/4로 변경 |
| 같은 시행의 완결 증거가 없고, 창 v1→v2 정정은 추가본문 노출 뒤 수행됐으며 JSON 창 경계·원 환경·전체 guard는 미확인 | “두 번 열어 실제 사용할 완결 구현을 찾았다” 또는 “이 구현/번역은 오답이다”라는 주장 | [SC032 README L3–106·첫 링크 L8–9](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/README.md), `windows.csv` P1/P2/P3, `judgments.csv` 본표18/진단1, window-audit §4·§6 | 원 Python/schema 또는 원 credential/context/lock/옵션과 양성·근접 음성을 확보해 두 조건·guard를 같은 판에서 시험. 새 실험에서 제목 없는 문서 경계와 목록 준비 행동을 사전 정의 | 허용된 한 경로/한 판에서 두 조건·환경이 함께 입증되면 완결로 변경. 예산 밖 최소 fixture만으로 본표나 원문 전체 성공을 바꾸지 않음 |
