# 새 요구 선정·용어 고정

## 실제 분모와 순서

단계2 원격 고정 SHA `412192e28356bee13e4c11f20511ab5ec590662c`를 루트가 확인한 뒤에만 신규 제목·metadata·본문 수집을 시작했다. `stage2-gate.json`의 기록 시각은 2026-11-23T03:39:42.323534+00:00이다. 이 문맥은 F1 필드 파일, 새 후보 순위, 답, 댓글, Stack Overflow 점수·채택 여부를 읽지 않았다. 056의 기존8 요구와 용어 및 F0 재생에는 앞서 노출되었다. SCOPE의 사전 추출 해석 예시도 읽었다. 같은 모델 계열의 별도 문맥 분업이며 독립 모델이나 사람이 한 검토라고 주장하지 않는다.

현재 canonical `jsonschema`·`json-ld` 태그, 생성 UTC 2023-07-01~12-31, creation_date→question_id 순서를 사용했다. JSON Schema 20건, JSON-LD 15건의 최초 revision1 본문을 **35/35 직접 읽었다**. 예정 모집틀은 40자리이며 LD16~20은 **현재 모집풀 소진 5자리**다. API의 `has_more=false`와 15건 결과가 근거다. 취득 실패한 최초본문은 0/35, 선정은 4/4다. 삭제·과거 retag까지 복원한 2023년 모집단이라고 말하지 않는다.

`holdout.csv`는 40행이다. 35개의 실제 source/work와 5개의 자료가 없는 예정 자리를 분리한다. 최초 태그와 현재 태그 모두 보존했다. 예컨대 LD13의 최초 태그는 jsonschema였지만 현재 json-ld 모집틀에 들어왔다. 같은 질문이 두 태그에 있으면 모집 행을 모두 보존하도록 수집기를 사전 교정했으며, 이번 실측 중복 질문은 0이다. metadata 한 페이지 100건을 받을 수 있으나 경계 동률 확인 뒤 첫20만 표시·저장했다. answer_count/score/accepted_answer_id/owner는 allowlist에서 제외했다. LD15 본문에 들어 있는 Google API `resultScore`는 요청자가 제시한 문제 데이터이며 SO 평점이 아니다.

## 최종 첫 적격 두 건씩

| 새 ID | 현재 태그 순번·질문 | C1 | C2·근거 구분 | 환경 |
|---|---|---|---|---|
| JS-5 | jsonschema 1 · [76598757 revision1](https://stackoverflow.com/revisions/76598757/1) | employee이면 각 사용자 batchId 필요 | firstName·lastName 필수 문자열 유지; **기존 schema 코드** | draft-07 명시; 런타임/제품판 없음 |
| JS-6 | jsonschema 2 · [76601421 revision1](https://stackoverflow.com/revisions/76601421/1) | 데이터 property `type`을 기술하여 예시 article 값 허용 | id:string 유지; **기존 schema 코드에서 읽은 보존 조건**, 별도 prose 요청 아님 | Ajv 웹앱 / Drupal 10 JSON:API; Ajv판·draft 없음 |
| LD-5 | json-ld 1 · [76620107 revision1](https://stackoverflow.com/revisions/76620107/1) | 로컬 JSON-LD→Turtle | Turtle+context→JSON-LD; 두 방향 **prose 명시** | RDFLib 6.3.2 / Python3.11 / Windows |
| LD-6 | json-ld 3 · [76653659 revision1](https://stackoverflow.com/revisions/76653659/1) | R에서 JSON-LD script 내용 추출 | 복수 내용을 JSON 파싱하여 요청 필드 보존; **prose+code/output** | R / rvest+xml2+jsonlite+dplyr; 판 없음 |

후속 적격 질문은 첫 두 자리를 채운 뒤에도 모두 읽어 원장에 남겼다. JSON-LD2의 Google 구매 링크 노출은 사전 UI 외관 범주라 제외했다. 예측되는 답·후보 개수·실행 난이도로 자리를 바꾸지 않았다. 표의 C1/C2는 기능명 매치의 OR와 별개이며 최종 지원 판정에서는 AND다.

### 봉인 전 정정: 코드 조건의 비대칭

03:49 무렵까지 루트에 전한 **임시** Schema 선정은 1·3이었다. 2번의 id:string을 설명 예시라 제외했으나, 1번의 이름 필드와 3번의 unit:string을 C2로 인정한 것과 비대칭이었다. 056 JS-3도 기존 코드의 required 필드 보존을 C2로 사용한다. 새 순위·F1에 미노출이고 용어 봉인 전인 상태에서 이 일관성 오류를 발견해 2번을 적격으로 교정했다. 따라서 **최종 1·2**, 3번은 후순위 적격이다. `selection-correction.json`에 전후와 노출을 남겼다. 이는 결과가 유리하도록 하는 사후 교체가 아니다.

가까운 음성 `{"type":"article","id":1}`은 C1의 type 데이터 속성을 그대로 만족하면서 C2의 기존 string 제약만 위반한다. 두 양성은 id가 `"1"`, `"2"`인 같은 article 데이터다. 어느 fixture도 특정 구현에서 실행했다고 하지 않는다. 만약 검토자가 “별도 prose로 재요청하지 않은 기존 코드 조건은 어떤 경우에도 인정하지 않는다”는 다른 모집규칙을 적용한다면 JS-5·JS-6뿐 아니라 056 코드 보존 사례까지 재검토해야 한다. 본표에는 원래 허용한 code/output 규칙을 유지하고 이 제한을 공개한다.

## 조건·반례를 보존하는 범위

`requirements-new.json`에는 원문 block 위치, C1/C2 origin, 언어·판·미명시, 동적 값, 금지/유지 guard, 보존 필드별 prose/code/연구자 추론 구분, 양성 두 fixture와 가까운 음성 및 검증 필요 상태를 기록했다. `body-locations.json`은 원 API HTML의 Unicode 문자 offset/line과 block hash다. 원문 전체는 독해용 `.cache/`에만 두며 커밋하지 않는다.

JS-5는 원문의 `userType`/`usertype`, array 위치의 required, sample trailing comma를 자동 교정한 성공으로 보고하지 않는다. JS-6은 `description:uuid`를 UUID assertion으로 바꾸거나 `required`를 새로 넣지 않는다. LD-5의 label·언어 태그 보존은 원 sample에서 읽은 guard이며 byte 단위 왕복 요구로 과장하지 않는다. Windows 파일 읽기 실패와 JSON-LD/RDF 변환 자체를 분리한다. LD-6은 요청자가 가격·면적·설명·위치를 말했다는 사실과 제시된 Product 부분에서 실제 확인할 수 있는 price·description을 나누었다. 없는 면적/위치를 생성하지 않는다. 여러 script의 추출 성공만 있고 JSON 파싱이 실패하는 가까운 음성은 C1만 만족한다.

## 새 L/V: 정의와 역할

용어 파일은 기존 `vocabulary.csv`와 같은 12열이다. 최종 원문 L 9행, 허용 V 5행, 보류 8행이며 V에는 L도 포함된다. casefold·ASCII hyphen→space·연속공백만 정규화한다. 동의어 관계는 아래 직접 읽은 고정 정의로 한정했다.

- [draft-07 core §3.1](https://json-schema.org/draft-07/draft-handrews-json-schema-01#rfc.section.3.1): validate/checking 제약 충족을 validation이라는 기능명에 대응시킨다. Validator라는 파생 명칭은 매치에 넣지 않는다.
- [draft-07 validation §6.5.3~6.5.4](https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01#rfc.section.6.5.3): required는 property 존재, properties는 이름에 따른 child schema 적용이다. C1의 일부 원자에 대응하며 전체 구현을 증명하지 않는다. 데이터의 `type` 이름과 schema의 타입 키워드 역할을 분리했다. conditional/dependencies도 같은 말로 보지 않는다.
- [JSON-LD1.1 API §§2.4,8.1,8.4](https://www.w3.org/TR/2020/REC-json-ld11-api-20200716/#rdf-serialization-deserialization): JSON-LD→RDF 및 RDF→JSON-LD 방향을 구분한다. Turtle 예시가 RDF syntax 연결을 제공하지만 원문 최종 I/O인 Turtle text와 표준 중간 I/O인 RDF dataset이 다르므로 **이 두 기능명은 주표 V에서 보류**한다. Turtle reader/writer·Windows 경로·context 옵션도 별도다. §8.6의 숫자 lexical round-trip 손실 가능성은 일반 변환으로 모든 데이터를 그대로 보존한다는 과잉 결론의 반례다.
- [JSON-LD1.1 API §9.5](https://www.w3.org/TR/2020/REC-json-ld11-api-20200716/#html-content-algorithms): HTML script extraction은 선택 기능이다. 기본 첫 script와 extractAllScripts=true의 전체 script 처리가 다르다. §9.5.2는 JSON text의 내부 map/array 변환이므로 단순 텍스트 추출 후 파싱 실패와 구분한다. R 지원·사용자 fields 보존은 이 정의만으로 확인되지 않는다.

이 세 표준은 **056에서 쓰던 저작의 직접 재열람**이다. 절·HTML 재취득을 새 독립 저작으로 불리지 않는다. framing 보류 경계는 056 고정 정의를 재사용했으며 이번 새 직접열람 수에 넣지 않았다. 비선정 Schema3의 FITS 사례도 읽었지만 최종 네 요구의 용어를 만들기 위해 공급자 문서를 탐색하지 않았다.

### 순위 전 정의 감사의 두 번째 정정

03:52:11Z 첫 지역 봉인에는 LD-5의 두 RDF 중간 단계 명칭이 허용 V로 들어갔다. 루트가 선정4건의 원본문/작성본과 I/O 정의를 대조하여 범위 이동을 지적했다. 당시 새 순위를 아직 계산하지 않았다는 메시지를 받았다. 본 문맥도 F1/순위에 미노출인 채 재검토했으며, 원문 Graph.parse/serialize는 단계를 암시해도 전체 함수구와 동일 I/O를 보장하지 않는다고 판단했다. 두 행을 `withhold`로 바꾸고 파이프라인 단계 확장 감도에서만 쓰도록 남겼다. 요구·선정·L은 바꾸지 않았다. 최초 봉인은 `freeze-v1.json`, 수정 전후·범위는 `vocabulary-amendment.json`, 최종 봉인은 `freeze.json`에 보존한다.

## 재생·검토와 남은 제한

`collector.py show-plan`은 네트워크 없이 규칙만 출력한다. 실제 수집은 stage2 gate 뒤 `collect-frame`, 각 태그 `collect-bodies`, `show-bodies` 순서였다. 프레임은 덮어쓰지 않는다. 재생 때 현재 API를 다시 호출하면 현재태그/삭제 상태가 바뀔 수 있으므로 이미 고정한 frame·revision GUID·body SHA를 사용한다. 원문을 다시 받아 해시가 달라지면 새로운 판 차이로 남기고 기존 독해를 조용히 바꾸지 않는다.

`finalize_holdout.py`는 이 문맥이 실제 읽고 수동 판정한 내용을 구조화할 뿐, 적격성을 자동 추론하지 않는다. 다시 실행하면 기록 시각/파일 해시가 달라지므로 봉인 후 무단 재실행하지 않는다. `freeze.json`이 순위 전의 실제 SHA256와 UTC를 보유한다. 의미 검토는 본 문맥의 자가검토와 루트의 선정4본문/용어 I/O 감사다. 루트가 35본문 전체를 읽었다는 주장은 없다.

새본체 독해 35/35와 목표 40/40을 혼동하지 않는다. 모집풀 부족 5자리는 미실시이며, 실제 빈 검색결과 0건과도 다르다. 네 선정 요구는 충원했지만 목표 40본문의 역사적 복원을 수행하지 않았다. 그 부족을 채우기 위해 기간/태그/순서를 바꾸는 일은 사전 모집규칙에 어긋난다.
