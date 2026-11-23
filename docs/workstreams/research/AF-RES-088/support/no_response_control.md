# AF-RES-088 별도 목적 대조: 공개 답·댓글 부재

**Pandoc 원순번23 질문 78566705**는 `2026-11-23T15:19:29.505640+00:00` 조회에서 공개 답변0·질문댓글0이었다. 질문 이력도 본문판1개뿐이다. 선정8자리·32쌍에는 추가하거나 대체하지 않았다.

## 탐색 분모와 첫 후보의 음성 결과

고정 frame60의 ID를 그대로 다시 조회했다. 질문60/60 응답, has_more=false. 현재 answer_count=0인 질문6개를 사전 태그순 jq→pandoc, 각 태그 원순번으로 나열했다. 여섯 질문의 댓글을 한 batch로 조회하여28행·has_more=false를 확인했다. 첫 답0 후보에서 댓글이 발견된 결과를 보존한 뒤, 전체6건 중 답0·공개댓글0인 원순서 첫 사례를 대조로 정했다. 자연층의 발생률이나 원8자리의 분모에 합치지 않는다.

| 태그·원순번 | 질문ID | 현재 답 | 현재 공개댓글 | 생성 후30일 안의 현재 보존댓글 | 30일 별도본문수정 | 답·댓글부재 조건 |
| --- | --- | --- | --- | --- | --- | --- |
| jq 16 | 78342087 | 0 | 8 | 8 | 1 | 미충족 |
| pandoc 10 | 78391068 | 0 | 1 | 1 | 0 | 미충족 |
| pandoc 16 | 78509090 | 0 | 5 | 5 | 0 | 미충족 |
| pandoc 23 | 78566705 | 0 | 0 | 0 | 0 | 충족 |
| pandoc 27 | 78580879 | 0 | 4 | 4 | 0 | 미충족 |
| pandoc 29 | 78624199 | 0 | 10 | 8 | 4 | 미충족 |

탐색 후보6개 중 현재 공개 답·댓글부재를 확인한 것은1개다. 첫 후보 jq16/78342087은 답은0이지만 공개댓글8개가 모두30일 안에 존재한다. 질문자의 후속 질문과 답변자의 기능 링크 안내가 댓글에 있으므로 이 사례를 무응답으로 부르면 틀린다. 이 음성 결과를 삭제하지 않았다.

## 선택한 대조의 원문과 판

- 질문 URL: https://stackoverflow.com/questions/78566705
- 보존 첫판 URL: https://stackoverflow.com/revisions/78566705/1
- GUID: `A91BB051-2F83-4B94-8EA8-400E6AA43697`
- 질문 생성·본문판 UTC: `2024-06-02T14:21:58Z`
- 30일 관측창 끝(포함): `2024-07-02T14:21:58Z`
- 작성자: Pedro Palazzo / user_id1195665
- API HTML SHA256: `2d7923d98d7b7125ec965abaed4a106627ccce358078490ad2fc8c2a6cbb704e`

첫 본문을 직접 읽었다. 작성자는 Eleventy2.0.1의 Markdown 처리를 node-pandoc으로 바꾼 공개 코드를 제시하고, 경미한 오류 뒤에도 처리를 이어가면서 어떤 파일이 어떤 오류를 냈는지 반환받고 싶다고 말한다. 본문판이나 실제 실행결과를 이 과제의8후보 적합 판정으로 재평가하지 않았다.

## 현재와 과거 관측의 구분

| 지표 | 확인 | 한계 |
| --- | --- | --- |
| 현재 answer_count | 0; 개별 answers API도0행·has_more=false | 삭제된 답이 과거에도 없었다는 증명은 아님 |
| 현재 공개 질문댓글 | 0; 개별 comments API도0행·has_more=false | 삭제된 댓글·외부 응답·비공개 대화는 알 수 없음 |
| 현재 보존 자료 중30일 내 답·댓글 | 0·0 | 당시 실시간 캡처가 없어 역사적 절대무응답으로 확정할 수 없음 |
| 별도 본문수정 | 전체 이력1행·has_more=false; 30일 수정0 | grace 기간 안의 합쳐진 수정 및 삭제/수정되지 않는 기록의 결손 가능성 |
| 최초 게시 바이트 | 미확인 | creation_date=revision1 시각만으로 원바이트 보존을 증명하지 않음 |
| 사용 포기·해법 부재·실패·시간 손실 | 미측정 | 공개 응답 부재를 사용자의 실제 결과로 바꾸지 않음 |

## 재열람 가능한 원자료

- [selected_revisions](https://api.stackexchange.com/2.3/posts/78566705/revisions?site=stackoverflow&pagesize=100&filter=%216X_1Q338%29I5q6Nn_): 1행, has_more=False, 직접 읽은 UTC `2026-11-23T15:19:29.467169+00:00`. 저장본 `support/raw/no_response_control_selected_revisions.json`; 응답지문은 인접 receipt에 있다.
- [selected_answers](https://api.stackexchange.com/2.3/questions/78566705/answers?site=stackoverflow&pagesize=100&filter=withbody&order=asc&sort=creation): 0행, has_more=False, 직접 읽은 UTC `2026-11-23T15:19:29.446036+00:00`. 저장본 `support/raw/no_response_control_selected_answers.json`; 응답지문은 인접 receipt에 있다.
- [selected_comments](https://api.stackexchange.com/2.3/posts/78566705/comments?site=stackoverflow&pagesize=100&filter=withbody&order=asc&sort=creation): 0행, has_more=False, 직접 읽은 UTC `2026-11-23T15:19:29.505640+00:00`. 저장본 `support/raw/no_response_control_selected_comments.json`; 응답지문은 인접 receipt에 있다.

60질문 조회·6후보 댓글 batch·최초 후보 개별 조회·최종 후보 개별 조회를 모두 `support/raw/no_response_control*`에 보존했다. 실제 새로운 API 호출의 UTC와 HTTP상태·원URL·SHA256은 각 receipt에 기록했다. 원래8자리와32쌍의 채택·판정 분모는 바뀌지 않는다.
