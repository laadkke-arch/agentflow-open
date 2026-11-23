## 3. 판정과 적용 범위

**출처가 있는 기능명을 넣으면 발견되는 후보는 늘었지만, 두 번 이하의 문서 열람으로 공동 조건을 확인한 구현은 늘지 않았다.** 이번 고정 입력에서 완결 후보는 네 조합 모두 0이다. 이것은 구현의 실제 능력이 없다는 판정이 아니다. 28개 요구×공급자 쌍을 조사했으나 전체 요구의 진위가 확인된 분모는 0이며, 1쌍은 독립 조건 하나의 조건부 부분 근거, 27쌍은 미확인이다. 84경로에서는 부분3·미확인81이다. 부분3은 같은 Ajv 첫 창을 공유하므로 세 번의 독립 성공이 아니다. [원장](../paths.csv), [집계](comparison-summary.json), [부분 근거](paths-schema/findings.md).

첫 표의 판·주소는 실제 읽은 공급자 문서의 판을 가리킨다. 주소가 있다는 사실을 해당 요구가 확인되었다는 뜻으로 읽으면 안 된다. P1은 첫 창, P2는 첫 창+첫 정보 링크, P3는 첫 창+둘째 정보 링크다. 첫 표는 가장 나은 **경로 전체**의 상태를 보여주며, 세 경로의 각 문서·C1·C2·환경·판 일치 여부와 실패는 paths.csv에 있다. 두 경로의 성공 절을 조합한 완결은 없다. 표의 C1/C2는 요약이고, 금지 행동·guard·원문/코드 유래·양성/근접음성은 requirements.json을 따른다.

| 층·분모 | L×F0 후보 있는 요구 / 채운 슬롯 | V×F0 | L×F1 | V×F1 |
| --- | --- | --- | --- | --- |
| 기존8, 각24슬롯 | 0/8 · 0/24 | 1/8 · 1/24 | 3/8 · 5/24 | 4/8 · 7/24 |
| 새4, 각12슬롯 | 0/4 · 0/12 | 1/4 · 1/12 | 0/4 · 0/12 | 2/4 · 4/12 |
| 전체12, 각36슬롯 | 0/12 · 0/36 | 2/12 · 2/36 | 3/12 · 5/36 | 6/12 · 11/36 |

48비교의 전체 매치 발생은43, 고유 요구×공급자 쌍은28, 게시행은20이다. 144슬롯 중18이 채워졌고, 111은 실제 무매치, 15는 후보 풀 소진이다. 새 요구 네 자리는 모두 확보하여 미실시 비교는0이다. 현재 LD 모집틀의 20자리 중5자리가 없다는 것과 선정 요구가 비었다는 것은 다르다. 슬롯의 부분1/미확인17과 진위확정 분모0을 공개하며 정확도·오탐률은 산출하지 않는다. 확정오답0은 **조사한28쌍에 붙은 상태의 개수**이지 0% 오답률이 아니다. [matches.csv](../matches.csv), [slots.csv](../slots.csv), [holdout.csv](../holdout.csv).

**연구 상태는 `partial_handoff`다.** 62행 편집, 48비교, 144슬롯, 28쌍의 경로 및 최소 외부 저작 배당은 수행했다. 그러나 다음 결손을 완전 충족으로 덮을 수 없다. 새 경로 두 개에서611/500단어가 노출되었고, 인수 경로 하나는 제목 없는 JSON 경계가 미확인이다. 편집 해석 정정 때 추가로 읽은1,411단어가 있으며, metadata 요청 총수는 보존 영수증의 하한이다. 정확한 F0 당일 응답이나 일부 구성요소의 정식판도 입증하지 못했다. 파일 저장·계약 검사·내용 연구의 충족 여부를 별도 평가한다. [수용 원장](acceptance-evidence.json), [예산 초과](paths-ld/preview-exposure.json), [편집 봉인](feature-freeze.json).

## 4. Q1 — 무엇을 보존해야 유용한 권고인가

기존8요구는 AF-RES-056 연구자가 이미 본 자료이며 현재 작업도 그 결과를 먼저 인수했다. **튜닝층**으로만 해석한다. 이전80본문 선별·62행 원순 복원·LD 역사적 태그 덤프·SC-032/PyLD의 예산 밖 실행은 다시 하지 않았다. 인수한9핵심 파일은 원 Git blob과 바이트까지 맞췄고, 기존16 L/V×F0 비교는 전체 매치·순위·용어가16/16 동일하다. [입력 감사](input-byte-audit.json), [기준 재생](baseline-replay.json), [별도 재생 감사](review/stage3-audit.md).

새 모집은 현재 public 태그를 API creation 오름차순으로 정렬한 UTC2023-07-01~12-31 질문이다. JSON Schema20, JSON-LD15개의 revision1 본문을 직접 읽었다. 없는 LD5자리는 pool_exhausted로 보존했다. 이는2023년 당시 태그 모집단 복원이 아니다. 답·댓글·점수·평판·공급자 F1은 선정 입력에서 제외했다. 최초 본문 revision은 수정 유예시간의 모든 키 입력을 복원하는 자료가 아니다. [모집 봉인](holdout/freeze.json), [선정 원장](../holdout.csv), [API 정의](https://api.stackexchange.com/docs/revisions-by-ids).

| 새 자리 | 현재 태그 모집 순번·원 요청 | 분리한 조건의 출처 | 대비 입력과 반례 |
| --- | --- | --- | --- |
| JS-5 | Schema1 · [76598757](https://stackoverflow.com/questions/76598757/) | employee이면 batchId는 prose; firstName/lastName required:string은 기존 코드의 보존 조건 | 두 개의 정상 user 예; batchId만 누락한 예와 lastName만 누락한 예를 분리. userType/usertype 혼용·required 위치·trailing comma를 원문 성공으로 자동 교정하지 않음 |
| JS-6 | Schema2 · [76601421](https://stackoverflow.com/questions/76601421/) | 데이터 property type 허용은 prose; id:string은 기존 코드의 보존 조건 | type=article/id="1" 및 id="2"; type를 유지하고 id=1인 근접음성. required·article-only enum·UUID format은 추가하지 않음 |
| LD-5 | LD1 · [76620107](https://stackoverflow.com/questions/76620107/) | JSON-LD→Turtle 및 역방향 모두 prose/code에서 읽음; Windows/Python3.11/RDFLib6.3.2 명시 | 언어표시 literal 한 개/두 개의 그래프 보존; 한 방향만 되는 구현, Windows 경로를 URL scheme c로 잘못 읽는 동작을 분리 |
| LD-6 | LD3 · [76653659](https://stackoverflow.com/questions/76653659/) | script 추출 및 복수 결과 파싱·가격/설명 보존; R package 코드는 직접 명시 | script1개/2개; 추출은 되지만 두 JSON을 이어붙여 parser 오류, 또는 price를 버리는 근접음성. 원문에 없는 area/location 값을 만들지 않음 |

Schema 잠정 선정1·3을1·2로 정정했다. 처음에는 rank2의 코드 보존 조건을 제외하면서 다른 사례의 코드 조건을 받아들여 일관되지 않았다. 정정은 **새 순위와 목적지 판정 전**이며 사유·전후 값을 보존했다. 기대 후보수로 바꾼 것이 아니다. 그럼에도 선정자 판단의 재현성 한계는 남는다. [정정 기록](holdout/selection-correction.json). 양성/근접음성 fixture는 원문에서 직접 가져온 것과 연구자가 구성한 미실행 입력을 분리했다. 원 사용자의 성공은 관측하지 않았다.

반증할 수 있는 결론은 “기능 하나의 성공으로 나머지 필드·금지 행동이 보존되는 것은 아니다”다. 예를 들어 외부 schema 참조가 해결돼도 Person required를 지우면 JS-3 C2는 실패한다. LD-6에서 추출에 성공해도 가격을 버리면 C2는 실패한다. 이런 반례는 논리적 대비 입력이며 이번 실제 실행에서 관측한 실패로 세지 않았다. 같은 판의 입력·출력으로 두 조건과 guard를 함께 확인하면 해당 보류 판정을 뒤집을 수 있다.

## 5. Q2 — 어떤 공급자 정보를 기능 필드로 저장할 수 있는가

62게시행 전체에 같은 추출 규칙을 적용했다. 54행에 총154개 원표기를 넣었다. 기존 F0와 정확히 중복되는2표기를 제외하면 새 문자열은152개다. 빈8행은 SC-013/018/020/028/031/033, LD-001/022다. **기능 필드가 비어 있음**과 **그 구현에 기능이 없음**은 features.csv의 서로 다른 칸이다. 62행 모두 구현 능력 부재를 판정하지 않았다. [features.csv](../features.csv), [규칙](../SCOPE.md), [편집 봉인](feature-freeze.json).

자기 기능의 표제·명시 목록·공개 API 기호만 원문 순서로 최대3개 저장했다. 비교 상대 이름, 언어, 준수 규격, 설치 명령의 dependency, 선택적 플러그인은 자기 구현의 지원 기능으로 복사하지 않았다. 기능절 제목의 whitelist, 첫 API/Features 링크, 코드/JSON의 whitespace 단어 경계는 사전 규칙을 따랐다. 표준 URI로 연결할 직접 관계가 없으면 concept_uri를 비워 두었다. F1 검색 문자열에 표준 명칭을 임의 복제하지 않았다.

| 직접 관측 | 편집·판정에서 보존한 경계 | 근거 |
| --- | --- | --- |
| SC-004의 Required/optional field inference | required/optional 문자열은 검색되지만 대상은 객체 필드의 추론이다. JS-1의 가변 마지막 배열 위치나 JS-5의 root 조건부 요구를 보증하지 않는다 | F-SC-004; PS-SC-004-P1; features-schema 및 paths-schema 창 |
| LD-008의 expansion/compaction/framing | framing이 F1에서 LD-3 후보를 만든다. Ruby 구현3.3.2의 기능명과 원 jsonld.js 요구의 공동 조건은 별도다 | F-LD-008; P-LD-008-D1; [고정 README](https://github.com/ruby-rdf/json-ld/blob/652730747e70f44f71ab7331f111c4308fe25b5c/README.md) |
| LD-001의 표준 준수 목록 | JSON-LD/Framing 규격 이름을 자사 기능 목록으로 변환하지 않아 F1이 빈다. 기능이 없다는 결론은 아니다 | F-LD-001 및 첫 표준 링크, features-ld 원장 |
| SC-008은 Blaze의 Java wrapper | 사용자 첫 창에서 직접 확인했다. 단계2 F1은 바꾸지 않고 엔진 계보에 추가한다. SC-007/008을 독립 엔진 두 개로 세지 않는다 | PS-SC-008-P1 소개; [경로 결과](paths-schema/findings.md) |
| SC-006은 Ajv를 부르는 CLI; LD-014는 jsonld.js를 사용 | wrapper README 두 개가 같은 엔진에 대한 독립 실행 성공 두 개가 되지 않는다. 실제 dependency 판 연결도 확인해야 한다 | PS-SC-006-P1/P2; F-LD-014 |
| LD-020의 Term/Graph/Dataset과 선택 jsonld module | core 타입 이름을 모든 JSON-LD 동작의 지원 보증으로 읽지 않는다 | F-LD-020/F-LINK-SOPHIAAPI; features-ld 원장 |

SC-001/004의 선택된 저장소 릴리스명은 다른 monorepo package의 이름이다. 고정 commit은 확보했지만 해당 구성요소 자체의 마지막 정식판은 미확인이다. SC-010은 처음200릴리스 범위만 조사해 전역 최후 정식판을 단정하지 않는다. SC-015/016의 설치 예시판과 repository 고정판도 다르다. SC-018은 판/역할 확인 부족, LD-022는 접근 실패를 빈 칸으로 남겼다. 당일 이전 commit을 고정하는 것은 F0 시각의 실제 HTTP 응답을 회수했다는 뜻이 아니다. [행별 version_and_role_limits_json](../features.csv).

추출 해석 감사에서는 허용 제목과 비슷한 제목, 쉼표/and로 이어진 여러 기능명, 코드 locator를 정정했다. 새 본문과 F1 순위 이전의 정정이지만 추가 노출1,411단어를 비용에서 지우지 않았다. 세 기능을 나누는 의미 단위 자체가 편집자 판단을 요구한다. 같은 규칙의 다른 편집자가 다른3개를 고르면 발견 이득도 달라질 수 있다. 이 경우 원표/정정표를 함께 비교해야 하며 유리한 행만 고쳐 주결과를 다시 쓰면 안 된다.

## 6. Q3 — 사용자 용어 확장과 공급자 용어 저장을 분리한 결과

질의 V는 L에 **같은 개념·방향·입출력 범위로 확인한** 표준어만 OR로 더한다. F1은 공급자가 실제 쓴 원표기다. 질의의 정의 관계를 공급자의 구현 지원 증거로 대신하지 않았다. 기존37용어행에 새22행을 더해59행을 고정했고, 새22행은 L9·허용 V5·보류8이다. 새 본문을 읽기 전 F1을 원격412192e로 봉인했고, 새 용어·48순위·경로 계획을5d01a620으로 봉인한 후 목적지 조건을 판정했다. [vocabulary.csv](../vocabulary.csv), [시간·노출](../SCOPE.md), [원격 기록](publication-log.json).

| 구분 | 허용하거나 보류한 이유 | 반대 사례·고정 정의 |
| --- | --- | --- |
| validation / Validator | operation명과 파생된 도구 유형명을 자동 어간 매치하지 않음 | Validator를 추가하면 F0 Schema40행 모두 검색된다. 원 두 조건의 지원 증거가40개 생긴 것은 아님. [core07 §3.1](https://json-schema.org/draft-07/draft-handrews-json-schema-01#rfc.section.3.1) |
| enum / 데이터 값 삽입 | schema가 나열한 값의 일치 제약이지 다른 instance columns에서 이름 집합을 만들어 넣는 동작이 아님 | 현재 columns에 없는 pii를 정적 enum으로 허용하면 JS-4 C1 실패. [validation07 §6.1.2](https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01#rfc.section.6.1.2) |
| contains / 가변 마지막만 | 어느 위치에서든 만족하는 값의 존재는 마지막 위치 제한과 다름 | [3,"x",4]의 string 위치; [§6.4.6](https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01#rfc.section.6.4.6) |
| 데이터 property type / schema keyword type | 같은 철자라도 역할이 다름; JS-6에는 properties와 validation만 정의 근거로 확장 | keyword type을 데이터 값 article로 바꾸면 schema의 역할이 달라짐; [§6.5.4](https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01#rfc.section.6.5.4) |
| framing / DOM 생성·PHP/R 처리 | frame의 graph matching/재구조화 정의는 script 부착·HTML 추출·표 출력을 정의하지 않음 | JS breadcrumb와 AEM 반복출력은 입력·출력 방향부터 다름; [2020 framing §§2.1,2.3](https://www.w3.org/TR/2020/REC-json-ld11-framing-20200716/) |
| RDF dataset 변환 / Turtle text 양방향 | 중간 dataset과 최종 Turtle text의 입출력 범위가 다름 | LD-5에는 별도 Turtle parser/serializer와 Windows path 처리가 필요; [2020 API §§2.4,8.1,8.4](https://www.w3.org/TR/2020/REC-json-ld11-api-20200716/) |

LD-5의 두 중간 pipeline 명칭은 잠정 V에서 **새 순위 전** 보류로 옮겼다. Graph.parse가 중간 RDF 변환을 암시해도 전체 원문 기능구의 동의어가 되지 않는다는 이유다. 이전 freeze와 수정 근거를 남겼다. [vocabulary-amendment.json](holdout/vocabulary-amendment.json). 이 판단이 지나치게 엄격할 가능성은 있다. 사용자가 중간 구성요소를 찾는 작업으로 범위를 바꾸면 관계어 확장이 유용할 수 있다. 다만 그 별도 질문을 이번 원문과 같은 요구로 취급하지 않는다.

## 7. Q4 — 무엇이 새로 들어오고 밀려났는가

L을 고정하고 F0→F1로 바꾸면 기존층에서 JS-1/3/4 세 요구가 새로 비지 않게 된다. 새층에서는 L 그대로인 경우 모두0이다. V를 고정한 F0→F1은 기존층1→4, 새층1→2이다. F1에서 L→V는 전체3→6이며 LD-3의 framing, JS-5의 required, JS-6의 validation/properties 등이 영향을 준다. 두 변경을 모두 해야만 생긴 후보는14개의 고유 요구×행 쌍이다. 전체 풀은 OR 확대이므로 탈락0이지만, top3는 원게시순 때문에 기존 후보가 밀린다. [changes.csv](../changes.csv), [독립 순위 감사](review/stage3-audit.json).

| 변경 | 밀린 게시행 | 이전→이후 후보순위 | 의미 |
| --- | --- | --- | --- |
| JS-4, V고정 F0→F1 | SC-032 | 1→11 | 기존 유일 후보가 top3 밖으로 이동. 이전에도 두 조건 미확인이므로 완결 후보의 손실이라고 할 수 없음 |
| JS-6, V고정 F0→F1 | SC-032 | 1→5 | 새 Ajv 부분 근거와 미확인 후보들이 앞에 들어옴. SC-032 진위는 여전히 미확인 |
| JS-4, F1고정 L→V | SC-016 | 3→6 | 질의 확장도 top3를 바꿈. 같은 엔진/다른 엔진·판을 혼합하지 않음 |

정확 URL 중복 규칙은 게시 순위의 동일성 규칙이다. 같은 엔진을 별도로 합쳐 순위를 바꾸지 않았다. 다만 SC-005/006의 Ajv 계보, SC-007/008의 Blaze 계보, LD wrapper들은 보고서의 독립성 해석에서 분리한다. 게시행20은 독립 엔진20이라는 뜻이 아니다. 버전·정의문서·구현문서의 구분도 순위 변경의 구실로 쓰지 않았다.

반대 증거는 **검색되지 않았어도 쓸 수 있는 원시 메커니즘이 있을 수 있다**는 것이다. JS-4용으로 읽은 SC-035 같은 창에는 properties.name의 string 제약과 검증 호출이 있지만 JS-6의 봉인된 질의에는 검색되지 않았다. 이름만 id로 바꾸는 가능성을 사후 진단으로 남겼으나, Kotlin을 원 Ajv 환경으로 바꿀 근거도 없고 JS-6 후보 분모에 추가하지 않았다. Product 예제의 id:number·추가 required를 원 요구에 복사하지 않는다. [사후 반대 자료와 실제 행 위치](paths-ld/posthoc-nonretrieved-diagnostic.json).

## 8. Q5 — 두 행동 안에서 공동 조건이 확인되었는가

모든 전체 매치의 고유28쌍을 세 경로씩 읽었다. 낮은 순위에서도 좋은 근거가 있으면 보존하지만 top3 성과로 올리지 않는다. 새 공급자 첫 문서는 F1 취득 때의 같은 고정 응답을 재사용하되, **편집 기능절 창과 사용자 첫500단어 창을 따로 만들었다.** F1 창 밖 지식은 사용자 판정 근거가 아니다. 경로별 실제 문서·SHA·창 파일·위치·조건 근거는 paths.csv와 세 observations.json에 있다.

주목한 네 경계는 다음과 같다.

- **JS-6/SC-005 Ajv:** 고정9050ba…의 첫 창에서 object.properties.bar.type=string과 compile(schema)를 직접 읽었다. bar→id라는 일반 속성명 매개변수 변경만 조건부 전이하여 C2 부분 지원으로 기록했다. type라는 데이터 이름과 schema keyword의 공존은 C1 미확인이다. 원문 Ajv판·Dr​​upal 통합, id 숫자 거부, 데이터 불변성, 실제 원 사용자 성공은 관측하지 않았다. P2의 live draft04 안내나 P3의 RFC8927 접근 실패를 이 부분 근거에 합치지 않았다. [PS-SC-005-P1, 창289–304행](paths-schema/stage3-5d01a6208edd9f8a20be7b31f7b545cef2200597/SC-005-P1.txt).
- **JS-3/SC-040:** README의 참조 인라인은 문서화되어 있다. 그러나 원 Ajv 체인의 외부 gender enum 적용과 Person required 보존은 같은 경로에서 연결되지 않는다. 다른 simplify 명령의 키워드 제거를 inline의 실패라고 바꾸어 읽지 않았다. [P-SC-040-D1](paths-ld/first-windows/SC-040.txt).
- **LD-3/LD-008:** framing 인터페이스 이름과 구현 주장은 있지만 a=1 선택 및 b/c·나머지 credential 보존의 입력·출력이 없다. streaming writer의 노드 배치를 framing의 필드 손실 반례로 사용하지 않았다. 다음 링크는 규격 앞부분과 RDF gem metadata여서 간극을 채우지 못한다. [P-LD-008-D1](paths-ld/first-windows/LD-008.txt).
- **JS-4/JS-6/SC-008·036:** root scalar enum/string 예와 nested object property의 제약은 다르다. SC-036의 object.properties.a는 integer이며, a→id 이름 변경과 integer→string 검증 타입 변경은 구별했다. 단순 이름이 없다는 이유가 아니라 요청된 string 제약의 직접 메커니즘이 이 창에 없어서 C2 미확인이다. [별도12경로 검토](paths-ld/review-evidence.json), [Schema 부분 판정 검토](paths-schema/scope-review.md).

원래 정보 링크를 따라가면 SC-004는 같은 README와 번역, SC-008은 내부 절, SC-006은 Ajv 저장소와 과거 benchmark, SC-016은 다른 엔진 json-sKema로 도착한다. SC-022/024는 후속 정보 링크가 없고 SC-038은 하나뿐이다. old latest core의404, RFC8927의403, Bowtie 정적 shell의 본문0을 후순위의 더 유리한 문서로 교체하지 않았다. [Schema 도착 결과](paths-schema/findings.md), [LD 도착 결과](paths-ld/findings.md).

SC-032의 JS-4 세 경로는056 판정을 그대로 인수했다. JS-6에서는 같은 README와 새로 회수한 homepage/메타스키마 창을 읽었다. draft7이라고 연결된 일반 schema URL은 실제2020-12 meta-schema로 도착했다. 규범 문서의 최신 draft를 고정 C++ 구현의 공동 조건 지원 증거로 합칠 수 없다. 새168단어 JSON 계수를 기존056 경계 미확인에 소급 적용하지 않았다. [root-paths](root-paths/findings.md).

## 9. Q6 — 검색 증가가 선택을 나쁘게 만들 가능성

상위3의 새 진입과 탈락을 모두 판정했고, 전체 낮은 순위도 포함해28쌍을 읽었다. 관측 완결0·확정오답0·조건부 부분1·미확인27이다. **완결 후보가4위 이하로 밀린 관측은0개지만, 완결 여부를 아는 후보 자체가0개다.** 그러므로 안전하게 “선택이 나빠지지 않았다”고 결론내릴 수 없다. unknown을 실패로 간주하면 평가자에게 문서가 적게 도착한 도구를 부당하게 벌주고, 성공으로 간주하면 이름만 있는 도구를 추천하게 된다.

동음이의·범위 차이의 직접 반대 자료는 optional의 객체/배열 역할, schema $ref와 instance 동적 값, keyword/data type의 역할, framing/DOM의 연산 차이다. 구현의 실제 오답 사례와 이런 의미상 위험을 별도 칸에 남겼다. 같은 positive를 통과하고 근접 negative에서 실패하는 **이번 실행 결과는 미실시**다. 공급자 코드의 기대 boolean이나 표준 suite 입력은 실제 이 요구·이 판 실행의 대체물이 아니다. benchmark가 고급 기능을 평가하지 않는다고 명시한 점도 일반 준수에서 모든 설계 요구를 추론하는 데 반대 근거다. [paths-schema/findings.md](paths-schema/findings.md), [SELF_CHECK.md](../SELF_CHECK.md).

### 주표 뒤의 감도

| 감도 | 실제 재생 결과 | 해석 한계 |
| --- | --- | --- |
| top4 | 채운 슬롯18→21. 추가3은 JS-4 L/F1 SC-021, JS-4 V/F1 SC-008, JS-6 V/F1 SC-023. 모두 미확인; 완결0 유지 | 이미 조사한 전체 풀의 경로를 재사용. top4 사용자 행동을 새로 측정한 것이 아님 |
| 기능명1개만 | 채운 슬롯18→10; F1 L의 후보 있는 요구3→1, F1 V는6→3. 조건부 부분1·완결0 유지 | 먼저 읽힌 첫 이름만 남긴 순위 감도. 실제 편집 읽기 비용이 줄었다는 실험은 아님 |
| literal 예제만 인정 | JS-6 Ajv 부분1쌍→미확인; 부분3경로→미확인. 완결0 유지 | 원시 메커니즘의 이름 매개변수 전이 허용 여부에 민감함. 원 데이터의 실행 실패가 새로 관측된 것은 아님 |
| validation→Validator | JS-4/JS-6 각각 F0·F1의 Schema 후보40행, top3=SC-001/002/003 | 파생형 때문에 도구 유형 그룹 전체가 적중. 새 범위 밖 쌍의 진위는 미실시이므로 오탐률 산출 불가 |
| 보류 관계를 모두 동의어처럼 사용 | 24셀의 별도 재생을 보존; runtime/IO/넓은말 반례를 함께 기록 | 정의 위반 후보 증가의 진단이며 주 용어표 수정 아님. 미조사 후보를 확정오답으로 세지 않음 |
| 편집 출처로 바로 이동 | **미실시**; 원게시 URL과 첫째/둘째 정보 링크를 주실험에서 유지 | 편집용 창을 이용자 지름길로 바꾸면 색인 축과 클릭 경로 축이 섞임. 이득을 이번 F1 성과로 주장하지 않음 |

전체 수치와 비교ID는 [sensitivity-summary.json](sensitivity-summary.json)에 있다. 주표의 순위 입력은 이 감도 뒤에도 바뀌지 않았다. 예산 초과 두 경로는 top3나 top4에는 없지만 전체 경로 분모84에 남긴다. 제외하면 엄격히 예산이 확인된 경로는81개이며 모두 완결0, 부분3이다. 인수 경계 미확인1과 초과2를 삭제해 성공적인 실험으로 다시 이름 붙이지 않는다.

## 10. Q7 — 편집 비용, 전거의 역할, 중단 조건

### 직접 센 비용

| 비용 단위 | 관측값 | 포함·제외 |
| --- | --- | --- |
| F1 편집 시도/추가행 | 62 / 54행 | 빈8행도 조사·비용에서 보존 |
| 공급자 본문 물리 요청 | 72회 | Schema32행35 + 나머지30행37; metadata와 별도. 성공응답70에는 redirect shell 포함 |
| 행별 논리 편집 행동/읽힌 창 | 78 / 75 | 같은 응답의 행별 재사용·fragment를 구분; 실제 고유 저작 수 아님 |
| 편집 논리 표시단어 | 30,943 | 모든 행의 지정 창 합계; 고유 저장 창 합계28,943과 다른 단위 |
| 정정 중 추가 표시량 | 1,411단어 | 새 본문·순위 이전 노출이지만 비용·프로토콜 한계에서 제외하지 않음 |
| 보존 metadata 요청 | 최소190회 | 일부 초기 redirect/tag retry 영수증이 없어 정확 총수 미확인 |
| 신규 사용자 경로의 논리 문서 시도 | 130회 | Schema81+LD44+root 신규5; 인수 JS-4 세 경로의5행동은 별도 |
| 신규 사용자 경로 지정 창 합계 | 51,095단어 | 31,325+17,602+2,168. 초과 preview를 경로별 반영하면51,317; 같은 실제 초과111이 두 경로에 영향을 줌 |
| 인수 사용자 경로 읽기량 | 알려진2,000단어+미확인 JSON창1 | 이번 신규 독해량에 합치지 않음 |
| 신규 경로용 본문/metadata 요청 | 29 / 6회 | Schema본문12+LD15+root2; Schema metadata4+LD2. F1 응답 재사용과 공유 homepage를 중복 네트워크 청구하지 않음 |

F0 원게시 필드의 **역사적 구축 비용은 이번에 재실측하지 않았다.** 9고정 입력과62행을 인수해 순위만 재생했으므로 F0 원래 비용이0이었다는 비교는 성립하지 않는다. 사용자 경로의 논리 행동 합계도 실제 사람의 시간·클릭·만족·채택 비용이 아니다. 고유 창은 겹친 문장을 제거한 독립 읽기량이 아니며, 같은 창의 교차 검토 횟수·토큰 청구·벽시계 시간·금액은 계측하지 않았다. [편집 비용](feature-freeze.json), [Schema 경로 비용](paths-schema/summary.json), [LD 경로 비용](paths-ld/summary.json), [root 비용](root-paths/summary.json).

갱신 시 최소한54개 채워진 행의154개 원표기, 각 판과 역할/위임, 창 위치, 링크 생존, 정의 연결을 재확인해야 한다. 빈8행도 접근 복구·판 확인·규칙 변경이 있을 때 재시도 대상이다. 특정 기능을 찾는12요구를 위해 이62행 비용을12번 청구하지 않는다. 미래 질의가 몇 번 재사용할지·갱신 빈도·실제 절약 행동을 측정하지 않았으므로 투자 수익이나 최적 갱신 주기는 계산하지 않는다.

### 다른 분야의 실제 전거 네 개

AF056의 Engraving/Etching/painting 대신 **Lithography / Offset printing, offset printing / offset lithography**를 직접 읽었다. LOC JSON과 MARCXML은 같은 레코드의 표현이며 둘로 세지 않는다. Getty 범위 주석과 관계를 실제 레코드에서 읽었고 검색 스니펫으로 대체하지 않았다. [상세 원장](authority/record-observations.json), [출처·한계](authority/findings.md).

| 실제 레코드 | 직접 읽은 필드·관계 | 소프트웨어에 주는 반례 |
| --- | --- | --- |
| [LOC Lithography sh85077598](https://id.loc.gov/authorities/subjects/sh85077598.marcxml.xml) | 150 Lithography; 450 Lithographs의 $w=nne; 550 Prints의 $w=g | 이전 채택형 접근점의 이력을 빼고 행위와 산물이 모든 문맥에서 동의어라고 처리하면 범위를 잃음 |
| [LOC Offset printing sh85094211](https://id.loc.gov/authorities/subjects/sh85094211.marcxml.xml) | 450 Lithoprinting/Printing, Offset; Lithography 상위 관계와 Direct의 별도 연관 | 다른 접근점, 상위, 관련 개념을 같은 OR 문자열로 평탄화하면 의미 방향이 사라짐 |
| [Getty AAT300053279](https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=work&page=1&subjectid=300053279) | 중간 표면을 거치는 전사; 다른 레코드와 distinguished from | 중간 전사라는 공통 과정만으로 더 좁은 원이미지 조건을 생략할 수 없음 |
| [Getty AAT300192900](https://www.getty.edu/vow/AATFullDisplay?find=&logic=null&note=&page=1&subjectid=300192900) | lithographic 원이미지 조건; 산물·장비와 방향 있는 관계 | 관련 장비/출력의 이름은 자기 개념의 동의어나 기능 지원 보증이 아님 |

MARC [4XX](https://www.loc.gov/marc/authority/ad4xx.html), [5XX](https://www.loc.gov/marc/authority/ad5xx.html), [tracing $w](https://www.loc.gov/marc/authority/adtracing.html)는 한 편집 형식 저작이다. Getty [용어](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.3/), [범위 주석](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.4/), [연관 관계](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.5/)도 한 매뉴얼의 절이다. 두 매뉴얼은 기존 저작 재사용, 네 실제 개념은 신규 저작이다. 중간 전사를 쓰지만 원이미지가 lithographic 방식이 아닌 사례는 넓은 조건만 맞는 논리적 근접음성이다. 실제 인쇄 실행을 했다는 뜻은 아니다.

| 관점 | 보존해야 할 정보 | 사용·중단 조건 |
| --- | --- | --- |
| 공급자 유지보수자 | 자기 기능의 원표기·입출력·판·직접 지원/위임·옵션 | 일반 준수/유형 이름을 특정 두 조건의 성공으로 올리기 전에 같은 판의 예·반례를 제공 |
| 목록 편집자 | 원표기, 개념ID, 관계 종류/방향, 출처 창, 판, 갱신 대상 | 기능명 적중과 조건 지원을 나눠 저장. 역할/판이 불명확하면 빈 칸과 사유 |
| 부분 설계 질문자 | C1/C2, 환경, 금지 행동, 남길 필드, 독립 경로 | 전체 구현0; JS-6만 조건부 보완; 나머지11은 재질문·보류. 필요한 다음 입력을 카드에 명시 |
| 표준 작성자 | 연산 정의·입출력 범위·규범/예시 구분 | 관련 개념 기록은 검색 설명에 사용하되 개별 구현의 실행/지원 보증으로 쓰지 않음 |

이 자료가 지지하는 선택은 작은 필드 추가만으로 완결 권고를 약속하는 것이 아니라, **찾아낸 기능의 의미와 실제 조건 증거를 분리하는 카드**다. 사용자가 중간 구성요소를 원하고 추가 연결 작업을 받아들이면 조건부 보완이 유용할 수 있다. 한 경로에서 공동 조건·환경이 확인될 때만 전체 구현으로 올린다. 비용을 계속 쓰고도 판/역할/필수 guard가 확인되지 않으면 보류한다. [12개 반환 카드](../cards.md).

## 11. 출처 배당·반증·자체 검토

출처 원장은 {{SOURCE_EVENTS}}개 취득/열람 사건을 보존한다. 그중 실질 본문을 직접 읽은 적격 사건 {{QUAL_SOURCE_EVENTS}}개를 계보로 합치면 **{{SOURCE_WORKS}}개 외부 원저작**, 기존056에 없던 저작은 **{{NEW_WORKS}}개**다. 기존 저작의 재열람은 신규 수에서 제외한다. 요청35개를 포함하므로 단순62공급자 수와 같은 분모가 아니다. 내려받기 중복, 같은 README fragment/번역, 같은 suite의 여러 행, 같은 레코드 RDF/HTML, metadata/목차만 읽은 원문은 최소 수를 부풀리지 않는다. {{SOURCE_WORKS}}저작을 독립 엔진이나 독립 실험 {{SOURCE_WORKS}}개로 읽으면 안 된다. [sources.jsonl](../sources.jsonl), [정규화·집계](source-counts.json), [계보 감사](review/final-audit.md).

| 자료군 | 사전 목표 | 실제 적격 최소 증거 | 재사용·한계 |
| --- | --- | --- | --- |
| 새 선정 요청 | 4 | H-SO-S01/S02/L01/L03 4저작; 모집 검토는35저작 | revision1·현재태그이며 당시 모집단 아님 |
| 서로 다른 공급자 직접 설명 | 8 | F-SC-001/004/008/009/016/021/022 및 F-LD-008 등 최소8개 공급자 원저작; 목록 공급자57+도착 utility2=59저작 | 기존6·신규53저작. 59개 독립 공급자/엔진이라는 뜻은 아님; wrapper/monorepo 계보 공개 |
| 공식 표준/시험 | 4 | 사전 지정 STD-SC-CORE07, STD-SC-VALID07, STD-LD-API11, STD-LD-FRAME11 4저작 모두 재열람; 전체 적격7저작 | 전체 기존6·신규RFC6901 1. suite/이전판·같은 meta-schema 개정은 계보를 합침 |
| 고정 목록/공식 편집 규약 | 2 | CAT-SCHEMA-CONTRACT, CAT-LD-INDEX 2저작 | F0 원순 재구성 아님; 기존 저작의 직접 재열람 |
| 실제 전거 | 4 | LOC2+Getty2 신규 실제 개념 레코드 | 같은 레코드 JSON/XML 재취득을 중복 집계하지 않음 |

최소22라는 합계뿐 아니라 위 배당을 확인했다. 공급자 설명의 취득 자체와 사용자 경로에서 조건을 증명하는 것은 서로 다른 적격성이다. 조회 실패·front matter·패키지 판/저자 metadata만 본 기록은 탐색/비용에 남기고 substantive quota에서 제외했다. 611단어를 읽은 공식 원문은 읽은 사실은 보존하되 경로 예산 충족이라고 하지 않는다.

자체 종합 주체는 `/root`다. 두 공급자 분담자가 전수 편집과 사용자 경로를 기록했고, `/root/authority`가 F0 및 네 조합의 순위를 별도 구현으로 재생하고 모집·계보·분모를 검토했다. 추가 경로 검토자는 LD분담4쌍·12경로의 허용 창10개를 직접 읽었으며 Schema 분담에서는 Ajv/Blaze의 지정6창과 C1/C2 독립성 해석을 검토했다. 같은 모델 계열·일부 상위 문맥을 공유한 검토이므로 외부 사람의 눈가림 재현으로 표현하지 않는다. 최종 감사가 직접 본 파일·범위와 미검토 범위는 [final-audit](review/final-audit.md), [SELF_CHECK](../SELF_CHECK.md)에 적었다.

가능한 독립 조사·반대 탐색을 마친 상태에서 남은 결손은 원전 부족, 판·역할 범위, 예산 오염, 실제 공동 입력·출력의 부재다. 실행이 필요한 대비 fixture와 명령은 [다음 확인](next-checks/README.md)에 있으며 미실행이라고 표시했다. 기존 금지 범위의 SC-032/PyLD 시험을 다시 요청하지 않는다. 원격 결과 재열람과 계약 검사 영수증은 evidence/verification에 저장하고, 마지막 HANDOFF 단독 커밋에서 실제 고정 결과 SHA·검사 결과·재개 첫 행동을 연결한다.

## 12. 남은 불일치·약점 — 세 항목

| 불일치·약점 | 영향받는 주장 | 근거 주소·위치 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| 경로611/500 초과2개, 인수 JSON 경계 미확인1개, 편집 정정 추가1,411단어 | 모든 조사가 엄격히 정해진 읽기 예산을 지켰다는 주장 | [preview-exposure](paths-ld/preview-exposure.json); [root 관측](root-paths/observations.json); [feature-freeze](feature-freeze.json) | 초과 노출을 보지 않은 별도 독자가 stage3의 같은 판·링크·정확500단어 창으로 해당 경로만 새 복제 조사; 인수 경계 원자료 확보 | 새 복제의 실제 노출 영수증과 동일 조건 판정이 확보되면 복제의 예산 충족 판정 가능. 현재 기록의 초과를 소급 삭제하지 않음 |
| 마지막 정식판/당일 응답과 metadata 정확 총수 미확인; 현재 LD틀15/20 | 특정 시점의 목록·판·편집 비용을 정확한 전체로 일반화하는 주장 | [features.csv 판/비용 칸](../features.csv); [holdout.csv 결손5행](../holdout.csv); [feature-freeze](feature-freeze.json) | component release provenance 및 누락 취득 영수증을 확보; 현재 모집틀 부족은 그대로 유지 | 원래 시각의 판/요청 기록이 나오면 범위·비용을 정정. 새 태그 결과로 기존 틀을 몰래 보충하지 않음 |
| 공동 조건 직접 근거0, JS-6 부분은 bar→id 전이, 새 요구 C2 두 개가 코드 보존 조건 | 기능 필드가 실제 사용 가능한 완결 권고를 늘렸다는 주장과 부분1의 강도 | [Ajv P1](paths-schema/stage3-5d01a6208edd9f8a20be7b31f7b545cef2200597/SC-005-P1.txt) 289–304행; [요구·기원](../requirements.json); [scope-review](paths-schema/scope-review.md) | 같은 Ajv판의 두 양성+numeric-id 근접음성 및 데이터 불변성, 원 환경판/옵션을 별도 예산에서 확인 | 같은 경로·같은 판의 직접 공동 근거가 나오면 그 후보 완결로 변경 가능. literal-only 기준이면 현재 부분은 미확인; 추가 실행만으로 기존 두 행동 실험을 소급 성공 처리하지 않음 |
