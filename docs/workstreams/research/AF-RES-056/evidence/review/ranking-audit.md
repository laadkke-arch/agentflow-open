# 동결 입력·순위 감사

**판정: 동결된 규칙의 16개 매치·순위와 48자리 원장은 재현된다.** L의 8건 빈 반환, V의 JS-4 한 후보 추가는 계산 오류가 아니다. 다만 이 결과만으로 용어 연결의 일반적 효용, 역사적 태그 모집의 완전성, 실제 독자의 두 번 클릭 안 완결 구현 발견을 판단할 수 없다. 이 감사는 공급자 목적지를 읽거나 두 조건의 구현 정답을 판정하지 않았다.

감사자: `/root/authority_records`. 같은 모델·같은 연구팀 안에서 다른 계산 구현으로 검산했다. 외부 독립 검토나 맹검이 아니다. 이 감사자는 앞서 Schema 1–9번 질문과 루트의 선정 제안을 읽고 `authority/screening-review.md`를 작성했으며, Q7의 전거 조사를 담당했다. 이번에는 루트의 예상 결과도 전달받았다. 원자료 추출과 주표 작성의 독립성을 과장하지 않는다.

## 1. 감사 입력과 실제 실행

| 입력 | 고정판·위치 | 확인 |
| --- | --- | --- |
| 모집·조건·용어 규칙 | [stage1 SCOPE](https://github.com/laadkke-arch/agentflow-open/blob/1f63f0129207904a91ae9e01bb3e48c86415a644/docs/workstreams/research/AF-RES-056/SCOPE.md), [vocabulary.csv](https://github.com/laadkke-arch/agentflow-open/blob/1f63f0129207904a91ae9e01bb3e48c86415a644/docs/workstreams/research/AF-RES-056/vocabulary.csv), `frame.csv`, `requirements.json` | stage1 `1f63f0129207904a91ae9e01bb3e48c86415a644` |
| 공식 목록·결과 | [stage2 catalog.csv](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/catalog.csv), [matches.csv](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/matches.csv), `slots.csv` | stage2 `b765a189aa2a1f5982a4994fc0476273abbf7127` |
| 판·노출·행동 사전 기록 | [stage2 SCOPE](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/SCOPE.md), `evidence/path-plan.json`, `evidence/catalog-pre/NOTES.md`, `snapshot-provenance.json`, `live-source-comparison.json` | Git 고정 객체를 읽고 확인. SCOPE 2판·용어표·목록·matches는 GitHub connector로 고정 ref 원격 파일을 직접 다시 열었고 blob SHA도 일치 |
| 모집 이력·계수 | `evidence/schema-pre/revision-audit.json`, `evidence/ld-pre/revision-audit.json`, 각 요구 원장·사전 영수증, stage2의 두 출처 원장 | 공급자 목적지나 단계3 결과에 의존하지 않음 |

`ranking_audit.py`는 주 분석의 `match_catalogs.py`를 가져오거나 실행하지 않는다. 고정 Git 객체만 읽고, 공백·ASCII 하이픈·대소문자 정규화를 한 뒤 문자열 위치와 앞뒤 문자로 단어 경계를 검사한다. 그 결과를 저장된 정규표현식 기반 결과와 대조했다. 정렬은 분야별 `posted_rank` 1부터 연속인지 먼저 검사하고 저장 순서를 따른다. URL의 대소문자·프로토콜·query·fragment·끝 slash를 합치지 않는다.

실행 명령:

```bash
python -B docs/workstreams/research/AF-RES-056/evidence/review/ranking_audit.py
```

최종 실제 출력은 `passed: true`, 35개 검사, 실패 0, 종료 코드 0이다. 시각·입력 blob/SHA256·각 검사·16비교는 `ranking-audit-receipt.json`에 있다. 최초 감사 스크립트 실행은 채운 자리의 상태명을 감사자가 `selected`로 잘못 적어 코드 1을 냈다(2026-11-23T01:49:09.325956+00:00). 원장의 실제 명칭 `filled`로 감사 스크립트만 고친 뒤 재실행했다. 원래 입력·매치·슬롯은 수정하지 않았으며 최초 실행에서도 16개 매치 비교 자체는 모두 일치했다.

## 2. 재계산 결과

| 요구 | L 전체 매치·상위3 | V 전체 매치·상위3 | 원순번 | 비교 해석 |
| --- | --- | --- | --- | --- |
| JS-1 | 0·빈 반환 | 0·빈 반환 | 해당 없음 | V에 허용 추가어가 없어 같은 질의 |
| JS-2 | 0·빈 반환 | 0·빈 반환 | 해당 없음 | meta-schema 추가 후에도 매치 없음 |
| JS-3 | 0·빈 반환 | 0·빈 반환 | 해당 없음 | schema references·dereferencing 추가 후에도 매치 없음 |
| JS-4 | 0·빈 반환 | 1·SC-032 | 32 | validation이 제목 필드에 일치. enum은 일치하지 않음 |
| LD-1 | 0·빈 반환 | 0·빈 반환 | 해당 없음 | V에 허용 추가어가 없어 같은 질의 |
| LD-2 | 0·빈 반환 | 0·빈 반환 | 해당 없음 | V에 허용 추가어가 없어 같은 질의 |
| LD-3 | 0·빈 반환 | 0·빈 반환 | 해당 없음 | framing 추가 후에도 표시 필드에 없음 |
| LD-4 | 0·빈 반환 | 0·빈 반환 | 해당 없음 | V에 허용 추가어가 없어 같은 질의 |

계수는 요구 8, 방법 비교 16, 모집 80, 목록 62(JSON Schema 40·JSON-LD 22), 용어표 37행이다. 용어표의 방법 행은 L/V 공통 20, V 추가 허용 7, 보류 10이다. JS-V09와 JS-V10은 같은 사례에서 같은 `validation`으로 정규화되므로 실제 추가 질의는 6개다. 사례별로 합한 고유 질의 수는 L 20·V 26이며, 질의가 바뀌는 요구는 4/8이다. **8건 전체 비교와 실제 추가어가 있는 4건의 비교를 혼동하지 않아야 한다.** stage1의 용어 개수 설명 오류는 stage2에서 정정되었고 CSV 내용은 두 커밋에서 byte 동일하다.

48자리는 `filled` 1, `observed_no_match` 45, `matched_pool_exhausted` 2로 구성된다. 후자의 두 자리는 JS-4 V에서 후보 한 개를 채운 뒤 생긴 빈자리다. 빈 카탈로그나 접근 실패로 계산한 빈 반환은 없다. 두 분야 모두 원래 목록에 행이 있고, JSON-LD는 22행에서 게시 목록이 소진되었다. [근거: stage2 slots.csv 및 matches.csv](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/slots.csv).

정확 목적 URL은 Schema 40개·LD 22개로 각 분야 안에서 중복이 없다. 따라서 이 고정 입력에서 URL 중복 제거가 후보를 밀거나 줄이지 않는다. 이것은 서로 다른 상류 엔진 62개가 있다는 뜻이 아니다. 목록에는 Ajv를 상류로 선언한 여러 행 등이 있고 빈 `upstream_declared`는 미상이다. 검색에 상류 정보나 목적지 기능을 역으로 넣지 않은 점은 재현된다.

## 3. 제목·기능 분류·문자 경계의 실질적 영향

Schema 40행의 검색 필드는 모두 이름과 기능 분류 `Validator`다. LD 22행의 검색 필드는 이름뿐이다. 두 목록 모두 명시 별칭이 없고, LD의 언어·CLI 표제는 소속 표제여서 기능 필드에 넣지 않았다. Schema 숨은 설명, 언어, 지원 초안은 매치에 쓰지 않았다. 따라서 “두 목록 모두 기능 필드가 없었다”는 설명은 틀리고, “L은 항상 제목만 비교했다”는 설명도 틀리다. [근거: catalog.csv의 `search_fields_json`, `function_field`, `explicit_aliases`; 공식 목록 복원 NOTES](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/evidence/catalog-pre/NOTES.md).

독립 검사에서 다음은 모두 불일치다.

- `validation` 대 `Validator`: 다른 단어이며 파생형 정규화는 사전 규칙에 없다.
- `validate` 대 `validation`: 어간 일치 규칙이 없다.
- `validation` 대 `DSJSONSchemaValidation`: 제목 내부의 이어진 문자열이며 단어 경계가 없다.

유일한 일치는 SC-032의 공백으로 분리된 제목 속 `validation`이다. 원순번 32는 데이터 파일 내 순번 6과 다르다. 정렬된 게시 순번을 반환하고 원본 데이터 순번으로 대체하지 않은 계산이 맞다.

이것은 **용어가 뜻을 잘못 옮겼다는 증거와 다르다.** 유효성 검사라는 일반 행동을 옮긴 단어가 매치되어도 JS-4의 동적 열 이름 관계, datatype 열거값, Python 환경과 추가 값 존재 조건까지 자동으로 보장되지 않는다. 목록상 SC-032는 C++이고 요청 원문은 Python 3.x다. 구현 판정 전부터 환경 부합성을 따져야 한다는 신호다. 이후 이 후보가 오답으로 판정되더라도, “retrieval이 조건을 너무 넓게 잡았다”와 “validation이라는 어휘 관계 자체가 거짓이었다”는 별도 주장으로 기록해야 한다.

`validator`를 새 동의어나 형태 변환으로 넣으면 무엇이 달라질지 생각할 수 있지만 이번 고정 V에는 없다. Schema 40행 모두에 이 분류어가 있다는 사실은 사후 필드 진단일 뿐이다. 이를 채택한 결과를 이번 V 결과에 더하거나 사전 감도로 부르면 안 된다. 새 실험에서는 파생어·기능 수행자 이름을 허용할 표준상 근거와 범위를 후보 순위 전에 정해야 한다.

## 4. 감도·신규·밀림에서 실제로 관측한 것

| 점검 | 실제 결과 | 해석의 한계 |
| --- | --- | --- |
| L→V 신규 | JS-4의 SC-032 1건; 나머지 7건 0 | 구현 두 조건 충족 여부는 이 감사에서 판정하지 않음 |
| L 기존 항목의 탈락·밀림 | 조건부 분모 0; 해당 없음 | L에 채운 자리가 없어 “확장해도 기존 정답을 보존한다”는 주장을 시험하지 못함 |
| L/V 같은 반환 | 빈 반환 동률 7/8 | 목적지 두 조건에 대한 동률 성능을 관측한 것이 아님 |
| 상위3→상위4 | 16비교의 반환 후보 집합·순위 변동 0; 64자리 중 1자리만 채움 | 모든 풀 크기가 0 또는 1이라 네 번째 후보가 들어올 기회 자체가 없음 |
| LD-3-V1 제거 | LD-3 V의 질의 수만 4→3; 16비교의 반환 변동 0 | framing이 원래 필드에 없어 제거 효과를 관측할 기회가 없음 |

두 감도의 무변화는 넓은 규칙 안정성이나 통계적 견고함의 증명이 아니다. 이 입력에서 해당 변수가 순위에 작용하지 않았다는 계산 결과다. 행별 결과는 기계 판독 영수증의 `sensitivity`에 있다.

## 5. 모집·원문 이력·고정 시점

`frame.csv`, `requirements.json`, `vocabulary.csv`는 stage1→stage2에서 byte 동일하고 stage1은 stage2의 조상이다. 따라서 이번 순위 결과를 본 뒤 이 세 파일의 표본·조건·용어를 고친 흔적은 없다. 카탈로그 담당자의 수집 시각은 stage1 커밋보다 앞서지만 담당자를 나눴고 그 담당자는 질의·표본을 작성하지 않았다고 기록했다. Git 이력은 파일 선후를 보증하며, 기록 밖 인지적 비노출이나 외부 맹검을 증명하지 않는다. [근거: stage2 SCOPE의 노출 기록과 catalog-pre/NOTES의 담당자 선언](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/SCOPE.md).

두 모집 프레임은 현재 태그를 조회한 각각 40건이며 모두 최초 revision 1을 복원한 것으로 원장에 대응된다. 생성일 범위는 Schema 2021-01-05~2021-02-04, LD 2021-01-04~2021-06-25다. 2021–2024 전체를 대표하는 분포 표본이 아니라 해당 시간 필터에서 현재 태그 순서의 앞부분이다.

LD-1과 LD-2에는 최초 생성판에 `json-ld` 태그가 없었다. 이후 각각 2021-01-05와 2021-01-21에 추가되어 기간 안에서 이 태그가 있었던 것은 원 이력으로 확인된다. 이 사실만으로 두 질문이 당시 기간에 부적격이었다고 단정할 수는 없다. 그러나 현재 태그 API가 과거에 태그가 제거되었거나 삭제된 다른 질문을 모두 되살리는 것도 아니다. 따라서 **최초 본문 복원 80/80과 역사적 모집단 복원 완료는 서로 다른 상태**다. [근거: LD 개정 이력의 첫째·셋째 record](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/evidence/ld-pre/revision-audit.json).

Schema 선정의 경계는 이전 `authority/screening-review.md`에서 점검했다. country/province UI 질문은 두 조건이 없어서가 아니라 검증·주석 처리 범위 밖이어서 제외됐다. 반면 LD는 HTML/JSP·AEM 입력에서 JSON-LD 내용 생성까지 문서 변환에 포함했다. 분야 정의상 설명 가능한 차이지만, 표본의 절반은 추가 표준어가 없고 LD 세 요구가 전형적인 JSON-LD 프로세서 기능을 묻지 않게 된 경계이기도 하다. 최종 결과에서 이 모집 정의를 숨기면 “JSON-LD 표준 기능 연결의 효과”를 과도하게 일반화할 수 있다. JS-3의 두 조건은 코드에서 도출됐고, JS-4의 빈 값 의미는 미정이라는 제한도 보존해야 한다.

답·댓글을 읽지 않았다는 기록과 추천 수·답 수를 전혀 보지 않았다는 기록은 같지 않다. LD 초기 응답 진단에서 첫 질문 score/answer_count가 보였다고 SCOPE에 정정되어 있다. 선정에 사용하지 않았다는 연구자 선언은 가능하지만 비노출로 다시 쓰면 안 된다.

## 6. 출처 수·배당 주장의 경계

stage2 루트 `sources.jsonl`은 93행·93 source ID이고, 별도 catalog-pre 원장은 21행·21 source ID다. 이 둘을 합쳐도 저작 수와 배당 수는 행 수와 다르다. 루트 원장에는 같은 JSON Schema Core의 두 판, 같은 Validation의 두 판이 각각 같은 work ID로 묶여 있다. 한 공식 목록의 HTML/YAML/renderer 여러 파일도 같은 목록 저작으로 묶여 있다. 실패 행은 별도로 제외해야 한다. 후기 저작이 인용한 앞선 저작은 직접 열지 않았다면 추가 저작으로 세지 않는다.

목록 배당 4개 제안은 Schema 목록·별도 데이터 계약·별도 제출 양식과 LD 목록이다. 데이터 계약과 제출 양식은 별도 기능을 가진 편집 산출물이지만 같은 Schema 편집 계보라는 점이 공개되어 있다. 독립된 네 기관이나 네 적합성 시험으로 표현하면 안 된다. 두 CONTRIBUTING 문서까지 배당에 중복 보탤 필요는 없다.

이 시점의 root 원장에는 authority·후속 시험·공급자 원장이 아직 합쳐지지 않았다. 이는 단계2의 중간 상태이므로 최종 최소24·필수8/4/4/4/4 충족을 이 감사에서 승인하지 않는다. 최종 통합 때 성공한 고유 저작, 필수 배당, 전체 열람 행, 실패 행, 같은 저작의 여러 판·미러를 별도 집계해야 한다. 이 감사 문서는 새 외부 1차 저작으로 세지 않는다.

## 7. 고정 영수증의 줄끝 차이

`evidence/path-plan.json`의 vocabulary SHA256는 `414655e77f699c917b6f6d63e2ed95af2ad6e2e31bb004e796d570b3fdf76949`이고 Git 고정 blob의 SHA256는 `259f6945db551ba814d9379b3038ab72c315dc0b6fade271e65558f0fe87ab15`이다. 작업트리 CSV에는 CRLF 38개, Git 저장본에는 CRLF 0개가 있다. Git 저장본의 LF만 CRLF로 바꾸면 앞의 hash가 정확히 재현된다. 내용·행 변경은 없고 frozen plan은 작업트리 byte hash를 기록한 것이다. catalog hash는 Git 저장본과 동일하다.

사전 계획을 소급 수정할 이유는 없다. 이번 receipt에 원격 Git blob SHA1, 저장본 SHA256, CRLF 재현 hash를 나란히 보존했고 루트에 후속 committed-byte 영수증을 덧붙이도록 전달했다. 이 불일치를 원자료 조작이나 순위 후 용어 변경의 증거로 취급하지 않는다.

## 8. 결론을 뒤집을 가장 강한 세 경계

| 불일치·약점 | 영향받는 주장 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| 현재 태그 첫40과 과거 태그 모집의 완전성이 다름; 삭제·태그 제거 이력이 모집 밖에 남음 | “2021–2024 당시 공개 태그의 첫 적격4건에서 효과가 없었다”는 일반화 | [frame.csv](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/frame.csv)의 80행; LD revision-audit의 LD-1·2 tag_revisions | 당시 질문·PostHistory를 함께 가진 공개 snapshot에서 같은 시간·ID 정렬 모집을 복원. 없으면 부분 수용 유지 | 현재 프레임보다 앞서는 제거·삭제 질문이 발견되어 첫 적격4 또는 조건을 바꾸는 경우. 기존 표본을 몰래 교체하지 말고 별도 판으로 다시 동결 |
| 개입은 추가어 6개·요구4개에만 작용하고, 표시 분류의 파생형·LD 기능 열 부재를 해결하지 못함 | “사용자 표현→표준 기능명 연결은 구현을 찾지 못한다”는 일반화 | [vocabulary.csv](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/vocabulary.csv) 행15·17–18·20–22·36; catalog의 Schema40 Validator와 LD22 title-only | 새 실험에서 파생어 관계를 정의·출처와 함께 사전 고정하거나 편집자 기능 필드를 별도 개입으로 추가. 이번 결과와 분리 | 사전에 허용된 정확 관계가 실제 게시 필드와 연결되어 같은 예산에 완결 구현을 추가하는 경우. 단순히 이번 결과 뒤 validator를 더한 수치는 본표 효과가 아님 |
| 후보 풀 최대1·L 기준선0이고 목록 준비는 공급자 두 행동 밖에 놓임 | “기존 정답을 보존하며 실제 두 번 클릭으로 더 나은 구현을 찾는다”는 주장 및 감도 강도 | [path-plan](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/evidence/path-plan.json), matches.csv JS-4-V, catalog NOTES URL·행동 모델 | 단계3에서 같은 경로·창 안 C1/C2·언어·판을 판정. 이후 실제 클릭 모델이 필요하면 Load More/모달/Source 준비를 포함한 별도 예산 사전 고정 | 두 조건이 동일 구현·판·한 경로에서 실제 확인되거나, L에 기존 후보가 있고 V 확장으로 밀리는 새 사전 표본이 생기는 경우. 현재의 빈 분모·무변화 감도로는 증명되지 않음 |
