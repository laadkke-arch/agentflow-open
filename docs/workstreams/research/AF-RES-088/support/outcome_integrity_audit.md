# AF-RES-088 사후 응답 메타데이터·표현 무결성 감사

판정 **PASS**, 검사 UTC `2026-11-23T15:43:42.623232Z`. 기준으로 전달받은 R1 커밋 `f048885abfbfcca1ffd8840899bf2911cd35da60`.

원본 공개 API의 저장 응답을 별도로 계산했다. 질문 의미·후보 판정은 평가하지 않았고 주파일·Git을 변경하지 않았다. 새로운 원격 API 재취득이나 독립 이중 코딩이 아니다.

## 분모와 무결성

| 항목 | 수/판정 |
| --- | --- |
| 질문 | 8 |
| 답변 | 11 |
| 답변 리비전 | 13 |
| 댓글 | 17 |
| 페이지 종료 | 4/4 has_more=false |
| 현재 채택 | 3 |
| 최초답판 시각=답생성시각 | 11/11 |
| 답 last_body 연결 | 2/2 |
| 확인된 오류 | 0 |

## 질문별 관측 창

| 사례 | 현재 답수 | 30일 답수 | 30일 질문댓글/답댓글 | 최초 답 UTC | 현재 채택 답ID | 30일 질문본문수정: 답전/답후 |
| --- | --- | --- | --- | --- | --- | --- |
| JN1 | 1 | 1 | 4/0 | 2024-04-03T07:46:44Z | None | 2/0 |
| JN2 | 1 | 1 | 4/0 | 2024-04-03T07:39:17Z | 78266023 | 0/0 |
| JE1 | 1 | 1 | 0/0 | 2024-04-09T15:20:06Z | None | 1/0 |
| JE2 | 1 | 1 | 0/0 | 2024-04-10T16:57:05Z | None | 0/1 |
| PN1 | 2 | 2 | 0/1 | 2024-04-02T11:27:35Z | 78260959 | 0/0 |
| PN2 | 1 | 1 | 1/2 | 2024-04-03T16:26:05Z | None | 0/0 |
| PE1 | 1 | 1 | 0/0 | 2024-04-10T06:03:26Z | 78302381 | 2/1 |
| PE2 | 3 | 0 | 1/0 | 2024-08-09T18:49:42Z | None | 1/0 |

PE2는30일 내 **답변0·질문댓글1**이다. 질문댓글138328053은2024-05-11T04:50:59Z에 존재한다. 따라서 댓글을 포함한 무응답으로 보고할 수 없다. 현재는 답변3개가 보이고 첫답78854242가2024-08-09T18:49:42Z에 생성됐다. 삭제된 응답까지 없는 것으로 증명하지 않는다.

## 답 최초판 식별

| 사례·답ID | 첫 GUID | 첫 UTC | 본문판수 | 현재채택 | 현재본문 비교 |
| --- | --- | --- | --- | --- | --- |
| JN1 / 78266070 | 0146B247-C6AC-473E-8951-58A97603F7B3 | 2024-04-03T07:46:44Z | 1 | False | current_equals_first_preserved_body |
| PN1 / 78260959 | 73187E4B-2EE7-4F23-AFD7-04ACAC2FD72D | 2024-04-02T11:27:35Z | 1 | True | pre_class_attribute_only_difference_no_explicit_later_revision |
| PN1 / 78261053 | 7986F26B-4B07-44F8-B575-C42E578E25B7 | 2024-04-02T11:44:37Z | 1 | False | current_equals_first_preserved_body |
| JN2 / 78266023 | 065949B3-EA93-4119-B4DC-BF02839847C5 | 2024-04-03T07:39:17Z | 1 | True | current_equals_first_preserved_body |
| PN2 / 78269109 | 241886B6-90B9-4A8F-927E-FDFEC2094AFD | 2024-04-03T16:26:05Z | 1 | False | current_equals_first_preserved_body |
| JE1 / 78299501 | 1A2183FA-65F2-4D46-953C-DF98E9A237D4 | 2024-04-09T15:20:06Z | 1 | False | current_equals_first_preserved_body |
| PE1 / 78302381 | 4DCC101E-12FB-492E-AC59-62A02672D20B | 2024-04-10T06:03:26Z | 1 | True | current_equals_first_preserved_body |
| JE2 / 78305953 | 0340F2CA-A35F-446C-AC2E-1E2DD59A16CE | 2024-04-10T16:57:05Z | 1 | False | current_equals_first_preserved_body |
| PE2 / 78854242 | 393910E3-846F-407C-AEE7-3B2986E85D40 | 2024-08-09T18:49:42Z | 2 | False | explicit_later_body_revision_current_matches_latest |
| PE2 / 79918495 | F2379943-BAAD-4254-9DB4-2EB9CD00B5D6 | 2026-04-01T15:30:40Z | 1 | False | current_equals_first_preserved_body |
| PE2 / 79918498 | DF7BB9C6-61CF-424A-BFE6-394A6348B64A | 2026-04-01T15:34:51Z | 2 | False | explicit_later_body_revision_current_matches_latest |

## 현재본문과 최초판이 다른 세 건

- PN1 답78260959: 보존 리비전은1개뿐이다. 차이는 `<pre class="lang-md prettyprint-override">`와 `<pre>`의class 속성이다. 그 속성만 제거하면 HTML이 같고, 표시텍스트·링크 대상·code텍스트도 같다. 명시 후속본문개정으로 세지 않는다. 렌더링/캐시/정제 중 어떤 원인인지는 이 패킷으로 확인하지 못했다.
- PE2 답78854242: 실제 판2 GUID B3C475B4-F9D3-48D0-AEC5-B93EE659BE33이 존재하며 현재본문이 판2와 같다. 최초판의 외부 이미지 링크를 설명과 코드 예제로 바꾼 기록이다. 최초답 시각에 현재의 상세 예제가 있었다고 소급하면 안 된다.
- PE2 답79918498: 실제 판2 GUID E2520566-9CCE-4271-A258-0C580688F2BA가 존재하며 현재본문이 판2와 같다. 최초판 뒤에 다른 extension 링크를 추가했다.

## 질문본문수정과 답 선후관계

30일 내 별도 질문본문수정8건 중 답전6건, 답후2건이다. 작성 주체 집계는 `{"question_author": 3, "unverified_deleted_or_missing_account_id": 1, "other_editor": 4}`다.

| 사례 | 판/GUID | 질문편집 UTC | 첫답 이후 초 | 편집자 | 첫답 작성자와 동일ID |
| --- | --- | --- | --- | --- | --- |
| JE2 | 2 / 71471D22-27D3-4030-B7D0-4FA5E8B6AFA7 | 2024-04-11T04:26:50Z | 41385 | oguz ismail / 10248678 / other_editor | True |
| PE1 | 4 / 06E686FC-FB2D-4E3B-836C-7CA2CF31DB4E | 2024-04-10T06:04:11Z | 45 | tarleb / 2425163 / other_editor | True |

두 답후 편집은 모두 질문자 이외의 안정user_id다. 질문자가 답을 본 뒤 해법명을 본문에 추가한 사건으로 바꿔 부르면 안 된다. 선후관계만으로 답이 편집을 유발했다고 주장하지 않는다. JN1의 삭제계정 편집자는stableID가 없어 작성자/타인 확정을 보류했다.

댓글 edited=true 표지는 0/17이다. 현재 댓글문구를 생성시각의 최초 문구로 소급하지 않는다. 채택시각과 실제 실행 프로그램판은 이 API 메타데이터에 없으며 만들지 않았다.

## 재실행

```sh
python docs/workstreams/research/AF-RES-088/support/audit_outcome_integrity.py
```

JSON의 input_sha256에 실제 검사 입력을 고정했다. 오류 발견시 종료1, 없으면 종료0. 답11개의 GUID·시각·revision chain과댓글17개의 질문/답 부모 매핑은 JSON에 모두 들어 있다.

## 검출 오류

```json
[]
```
