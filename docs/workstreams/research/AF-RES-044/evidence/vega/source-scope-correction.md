# V 출처 원장 범위 정정 v2

정정 시각: 2026-11-22T20:53:04.890675+00:00. 발견자는 Pandoc 담당 내부 검토자이며, 정정자는 원래 V 자료를 작성한 같은 Vega 담당 에이전트다. 사람의 독립·맹검 검증으로 표현하지 않는다.

## 정정 이유

`sources-V.jsonl`의 V-D 행은 locator가 특정 fragment의 strict 창인데 verified_fact에는 문서 전체의 요약이 반복되어 있었다. 대표 오류는 V-D-V2-2다. 실제 `#documentation-overview`는8어절의 목차뿐인데, 그 행의 설명은 다른 절인 Projection Types의 identity/reflectY 지원을 제시했다. Text와 Aggregate의 Overview, 각 configuration/encoding/transform 절에도 같은 종류의 범위 혼합이 있었다.

`coding-V.json`의 strict_fact 자체도 같은 문서별 요약을 복제하고 있어, 그것을 그대로 출처 원장으로 복사하면 오류가 해소되지 않는다. 반면 strict_atom_verdicts와 subcondition_facts는 V2-1/V2-4의 하위조건과 Overview의 무입증을 구분하고 있었다. 따라서 원 coding을 보존하고 실제 도착절을 다시 읽어 문구 override를 만들었다. 완전 지원 원자·완전 대안·후보 순서·group key는 바꾸지 않았다.

## 보존 파일과 적용 파일

| 파일 | 역할 | SHA256 |
| --- | --- | --- |
| sources-V-v1.jsonl | 정정 전29행의 바이트 그대로 보존. 활성 원장에 다시 합치지 않는 이력 파일 | `e383ef71c190e4ba86e63b9fada3e5bbdabb4e446e80c80d24b6aa6668e5fc93` |
| sources-V.jsonl | 활성 원장34행. 원래 V-D17행 정정, W5행 추가 | `65c1c1d66a054b135c75946c11fadfede76257c5c60c106ce390e7a3d18239fd` |
| scope-fact-overrides.json | candidate ID를 키로 한17개 객체. strict_fact, limitation, locator 및 관측 해시를 제공 | `ded3b8f32bdd54ac13be4b4cfe91fcb3e289aa4441b5e0e484438d3554d5a541` |

`coding-V.json`은 수정하지 않았다. 루트 통합에서는 override의 strict_fact를 해당 후보의 범위 설명에, limitation과 locator를 같은 후보 필드에 적용할 수 있다. supports/full_document_supports, 원 atom, 정렬, 표시 metadata를 바꾸는 파일이 아니다. 과거 `code_evidence.py`로 원장을 다시 생성하면 넓은 문구가 돌아올 수 있으므로, 재현 시 이 정정 버전과 override를 함께 적용해야 한다.

## 직접 재대조한 범위

공식 `spec.html`, `projection.html`, `text.html`, `transform.html`, `aggregate.html`을 다시 HTTP로 읽었다. 새 응답 SHA256은 기존 candidate-fetch-receipts의5개 문서 해시와 모두 같았다. 기존 `window_metadata.py`와 같은 DOM·토큰 경계로17개 strict 창을 추출했으며, 새 strict_text_sha256도 `windows-V.json`의17개 값과 모두 같았다. 문서가 바뀌어서 생긴 차이가 아니라 기록 문구의 범위 오류였음을 확인했다. 전체 HTML 사본을 새 파일로 저장하지 않았다.

| 활성 원장 행·source ID | 창의 어절 수 | 정정 후 관측 요지 |
| --- | --- | --- |
| 5 · V-D-V1-1 | 293 | View Configuration의 뷰 크기·배경 기본값. 이 창에는 title/subtitle이 없음 |
| 6 · V-D-V2-1 | 800 | 첫800 안에 identity와 reflectY 행이 실제 포함됨. 복합 graticule 요구 전체는 미입증 |
| 7 · V-D-V2-2 | 8 | Projection Properties/Types/Configuration 목차3개. identity/reflectY 본문 근거 없음 |
| 8 · V-D-V2-3 | 484 | type/center/clip 등 속성 표. identity/reflectY 지원 행은 다른 절 |
| 9 · V-D-V2-4 | 180 | Projection Types의 identity/reflectX/reflectY 하위조건만 확인 |
| 10 · V-D-V2-5 | 58 | config.projection 기본 속성 및 다른 property 절 참조. 개별 identity/labels 계약은 없음 |
| 11 · V-D-V3-1 | 706 | text mark 정의·속성·예제·설정. word-cloud 배치 근거 없음 |
| 12 · V-D-V3-2 | 17 | Text 관련 목차만 있음 |
| 13 · V-D-V3-3 | 502 | text mark의 angle/align/baseline 등 표현 속성 |
| 14 · V-D-V3-4 | 113 | 표·히트맵 라벨·텍스트 산점도·지리 텍스트 예제 |
| 15 · V-D-V3-5 | 46 | config.text 기본값과 encoding에 의한 덮어쓰기 |
| 16 · V-D-V4-1 | 147 | view-level/encoding 실행 순서와 지원 변환 목록 |
| 17 · V-D-V4-2 | 76 | view-level 배열 순서와 지원 목록. 앞 문단의 encoding 순서는 이 창에 포함하지 않음 |
| 18 · V-D-V4-3 | 800 | encoding/transform 집계의 두 경로와 속성 설명이 실제 첫800에 있음 |
| 19 · V-D-V4-4 | 26 | Aggregate 관련 목차만 있음 |
| 20 · V-D-V4-5 | 198 | encoding aggregate와 group-by/detail 계약 |
| 21 · V-D-V4-6 | 208 | transform aggregate/groupby 및 op/field/as 계약 |

## W 판독의 별도 기록

활성 원장30–34행을 `V-W-spec`, `V-W-projection`, `V-W-text`, `V-W-transform`, `V-W-aggregate`로 추가했다. 각 행은 같은 원문 안에서 이미 별도로 확인한 관련 절의 W 판독이며 전부 counted=false다. locator를 문서별 실제 절로 좁혔고, 관련 strict source ID를 연결했다. 첫29행의 source ID와 counted 플래그는 유지했다.

예를 들어 spec의 Common Properties에 있는 title 행은 이제 V-W-spec에만 기록하며 #config strict 행에 섞지 않는다. Projection Types의 identity 행을 Overview에서 읽은 것으로 처리하지 않고, W-projection 또는 실제 해당 strict창 V2-1/V2-4에만 둔다. ‘전체 문서 허용’은 그 문서의 모든 문장을 완독했다고 주장하는 표현이 아니며, 따로 확인한 관련 절의 근거를 허용하는 범위다.

## 검산과 영향

- 활성 원장 행 수는29→34지만 counted=true는 **13→13**, counted 원문의 duplicate_group 고유 수도 **13→13**이다.
- V-D17행의 URL·pinned HTML hash·original checked time·source ID·duplicate_group·counted는 유지했다. scope_reviewed_utc를 별도로 추가했다.
- 17개 override와 정정 V-D행의 verified_fact/locator가 각각 일치한다. subcondition_facts는 원 coding에서 그대로 복사했다.
- strict/full 지원 atom과 완전 대안 판정은 바꾸지 않았다. V3의 `text` 토큰 이탈도 그대로 유지한다.
- 루트 candidate/results/group 파일은 이 작업에서 수정하지 않았다. 문구 override 통합 뒤 루트가 정정 사실을 출처 원장과 함께 연결한다.

이 정정은 “Overview에서도 identity 근거를 제공했다”는 잘못된 설명을 철회한다. 현재 계산의 완전 대안 수가 변하지 않는다는 이유로 그 설명 오류를 유지하지 않는다.
