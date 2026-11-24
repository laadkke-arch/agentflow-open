# 공개 회수 영수증

2026-11-24 UTC 초 단위 기록을 [페이지 영수증](public-pages.jsonl)에 보존했다. GitHub connector의 REST JSON을 25개씩 요청하고, 각 비어 있지 않은 마지막 페이지 다음의 `[]`를 받았다. 빈 첫 페이지인 #9588·#7579 일반 대화는 같은 PR의 REST 메타데이터 `comments=0`과 일치한다. REST 응답 본문은 언어·페이지 순서대로 검토할 수 있도록 일시 보존하고, 저장소에는 [ID, 부모 ID, SHA 및 본문 해시](public-index.jsonl)만 남겼다. GitHub endpoint별 [요약](../coverage.csv)은 총 64행이다.

| 집계 단위 | 고유 개수 | 설명 |
|---|---:|---|
| PR 메타데이터 | 8 | 본문 8개, current activity timestamp |
| 이슈 대화 | 99 | 9개 updated_at 차이 |
| 제출 리뷰 행 | 173 | 현재 본문 있음 22개 |
| 인라인 첫 발언·답글 | 172·139 | REST pulls/comments 311개, 부모 ID 미매치 0 |
| PR 커밋 | 241 | 최대 한 PR 165개, PR 메타데이터 8/8 일치 |
| 공개 타임라인 | 611 | 일반 대화·리뷰·커밋의 ID 394개 재표시, 독립 이벤트 217개 |
| GraphQL 스레드 | 172 | 8/8에서 311개 REST ID 집합과 일치, 최대 중첩 응답 7개 |

[GitHub REST 문서](https://docs.github.com/en/rest/pulls/pulls#list-commits-on-a-pull-request)의 250개 상한에 도달한 PR은 0개다. [리뷰 코멘트 REST](https://docs.github.com/en/rest/pulls/comments#list-review-comments-on-a-pull-request)는 루트와 답글을 함께 반환한다. GraphQL wrapper는 #9618에서 130개 스레드와 모든 REST 인라인 ID를 반환했다. GraphQL 연결의 `pageInfo` 및 스레드별 reply cursor와 커넥터 REST의 원본 HTTP Link는 노출되지 않았다. `gh api --include 'repos/pydata/xarray/pulls/9618/comments?per_page=1&page=1'`은 이 환경에서 종료 1, api.github.com Forbidden. 끝 확인은 원래 endpoint의 빈 다음 페이지, PR 메타데이터와 REST↔GraphQL ID 대조에 근거한다.

현재의 created_at과 updated_at 차이는 이슈 대화 9개, 인라인 221개다. 인라인 배치 발행 자체로도 차이가 생긴다. 리뷰 REST 응답에는 submitted_at만 있고, PR 메타데이터 updated_at은 본문 외 작업도 반영한다. #9580 및 #9618의 현재 GitHub HTML에서 PR 본문의 공개 편집 표시와 편집 로그 fragment 주소를 확인했다. #9580 [해당 fragment](https://github.com/user_content_edits/show_edit_history_log/PR_kwDOAMm_X859nbzR)의 비인증 요청은 HTTP 404였다. 현재 공개 회수 결과에서 과거 본문 또는 삭제된 발언을 전부 복원할 수 없다.

작업 브랜치 최초 기준은 원격 조회의 `588e642b99e695e710573b9418b60364d7f3880b`다. start의 fetch 사이 통합 head가 `b6255317d161b5d1742bdd7cf1b80a2136cdc786`으로 이동해 manifest의 integration.commit은 후자를 고정했다. 두 판 사이 변경은 dot-control.json만이며 작업 계약·자기 배정과 AF-RES-133 인계 SHA는 같다. 사전 고정 커밋 `db16e146f3550d630d9b8eb1ad0bab9d14ad7e78`의 [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/db16e146f3550d630d9b8eb1ad0bab9d14ad7e78/docs/workstreams/research/AF-RES-137/SCOPE.md)를 그 exact ref에서 재열람했다.
