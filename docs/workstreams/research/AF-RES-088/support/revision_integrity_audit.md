# AF-RES-088 리비전 메타데이터·본문 연결 무결성 감사

판정: **PASS**. 검사시각 `2026-11-23T15:05:57.980267Z`. 부모가 제공한 원격 R0 봉인 커밋 `42e46d5788278efa8d5b8ab0272ace48830fb477` 이후에 수행했다.

공개 API를 새로 호출한 재확인이 아니라, 고정 압축 원본의 별도 계산이다. 본문 의미·후보 판정은 평가하지 않았고 judgments.csv는 읽거나 변경하지 않았다. 독립 이중 판독으로 세지 않는다.

## 집계

- 목록 60행, 서로 다른 질문 60개, 선택 8자리.
- jq 72개 이력·30질문, Pandoc 57개 이력·30질문. 양 API 응답 has_more=false, 원목록 ID 전부 포함.
- last_body 연결 51개 검사, 51개 일치. 오류 0개.
- 같은 HTML 바이트를 다시 기록한 별도 본문 revision 0개. 따라서 이 스냅샷의 body 존재 기반 편집수와 실제 본문 바이트 변경수는 일치한다.
- 최초 본문판은60질문 모두 판1이며 질문 생성시각과 같다. 비본문 Staging Ground 생성 사건이 같은 시각에 붙은 질문 [78596229, 78652004]은 그 사건을 본문판으로 세지 않았다.
- 선택자리의 R0=R1 3개, 별도 본문판 5개. R1 미작성 상태에서 비교한 자리 0개.

## 독립 재계산한 8자리

| 사례 | 원순번 | R0 GUID·UTC | R1 GUID·UTC | R1 작성 주체·종류 | 30일 내 별도 본문판 |
| --- | --- | --- | --- | --- | --- |
| JN1 | jq 1 | F262790D-B04B-4660-94B3-054090091E09 / 2024-04-01T00:14:19Z | 5FC9B85A-FDF3-4DD8-840F-5395C864C492 / 2024-04-01T11:34:30Z | user7939871 (id=None; unverified_deleted_or_missing_account_id) / body | 2 |
| JN2 | jq 2 | AB2C2CBD-E08C-49C2-8E26-AD90779C3B66 / 2024-04-02T14:43:42Z | AB2C2CBD-E08C-49C2-8E26-AD90779C3B66 / 2024-04-02T14:43:42Z | Starbucks Admin (id=14820140; question_author) / initial_body | 0 |
| JE1 | jq 5 | 92DE1FA7-F276-4799-8A25-3E363A57CFC3 / 2024-04-09T05:58:37Z | 62F8A2CB-8249-4015-AD16-50F716581C23 / 2024-04-09T06:07:46Z | Arun (id=8253518; other_editor) / body | 1 |
| JE2 | jq 7 | 7C90E82D-FE85-4B1C-B522-5E7DB5F71D07 / 2024-04-10T16:50:23Z | 71471D22-27D3-4030-B7D0-4FA5E8B6AFA7 / 2024-04-11T04:26:50Z | oguz ismail (id=10248678; other_editor) / body+tags | 1 |
| PN1 | pandoc 1 | 9838C9A3-FAC3-4C2C-9163-67B00B6065C2 / 2024-04-01T23:12:49Z | 9838C9A3-FAC3-4C2C-9163-67B00B6065C2 / 2024-04-01T23:12:49Z | Robert Dodier (id=871096; question_author) / initial_body | 0 |
| PN2 | pandoc 2 | 5FF30549-BD38-4348-81D9-A746AA52FF69 / 2024-04-03T12:00:23Z | 5FF30549-BD38-4348-81D9-A746AA52FF69 / 2024-04-03T12:00:23Z | Alexey Bogdanov (id=19893853; question_author) / initial_body | 0 |
| PE1 | pandoc 4 | DAD692BA-D95F-4262-8B83-C762CF15C4A9 / 2024-04-09T18:50:27Z | 06E686FC-FB2D-4E3B-836C-7CA2CF31DB4E / 2024-04-10T06:04:11Z | tarleb (id=2425163; other_editor) / body | 3 |
| PE2 | pandoc 12 | 9D423177-6C8D-4691-B857-ABBF6BCDCBF3 / 2024-05-10T18:35:18Z | E1BF2992-76D3-4E9A-8678-A17B00F06672 / 2024-05-11T04:48:15Z | Shafee (id=10858321; other_editor) / body | 1 |

## 판별 절차와 한계

1. snapshot_archives.json의 압축·해제 SHA256을 다시 계산했다. API wrapper has_more=false와 요청30개의 post_id 집합을 맞췄다. 동일 GUID, 누락 판 번호, 시각 정렬과 숫자 판 정렬의 불일치를 검사했다.
2. 각 질문에서 body가 실제 포함된 판만 본문판으로 분리했다. 최초 본문판을 R0, creation_date부터30일(2,592,000초) 이하의 마지막 본문판을 R1으로 계산했다. title/tag-only와 비내용 이벤트는 별도 분류했다.
3. 각 다음 본문판 last_body가 바로 앞 body와 정확히 같은 UTF-8 문자열인지 확인했다. 바이트 동일 여부를 의미 동일 판정으로 사용하지 않았다. 표현만 달라진 경우는 부모의 별도 의미판독 대상이다.
4. frame의 적격 판정을 입력으로 삼아 각 태그의 첫 자연층2개, 이후 별도 본문수정이 있는 첫 편집층2개를 재선택했다. 적격 자체의 의미 판독은 감사하지 않았다.
5. 질문자/타인 구분은 안정적인 user_id가 양쪽에 있을 때만 확정했다. 삭제된 계정의 user_id가 없으면 표시명이 달라도 안정적 식별 근거 미확인으로 남겼다.
6. 모든 R0가 판1 및 질문 생성시각과 일치하는지 검사는 최초 게시 바이트 보존 증명이 아니다. grace 병합·삭제된 역사·조회시점 태그가 만드는 한계는 유지된다.

## 재실행

```sh
python docs/workstreams/research/AF-RES-088/support/audit_revision_integrity.py
```

출력 JSON의 input_sha256은 실제 검사한 파일을 고정한다. revisions.jsonl에 R1을 추가한 뒤 다시 실행하면 해당 작성본과 GUID를 비교한다. 프로그램은 실패 발견 시 종료1, 발견하지 않으면 종료0이다. JSON의 all_question_checks에60질문의 개별 이력 분류가 들어 있다.

## 검출 오류

```json
[]
```
