# AF-RES-070 인수·실행 경계

시작 통합판 [76b8c1d](https://github.com/laadkke-arch/agentflow-open/commit/76b8c1d15812fbf91b879f8444fd188ae7445802)에서 AGENTS.md, STATE.md, docs/DOT_AUTOMATION.md, docs/RESEARCH_WORKFLOW.md, RESEARCH_BRIEF.md와 중앙 AF-RES-070 항목을 직접 읽었다. 중앙 항목은 RUNNING, worker_kind web-pro, owned_path와 의존 AF-RES-066이 사용자 지시와 일치했다. 대형 원장은 fetch_file이 빈 content를 반환했으나 GitHub contents URL에서 원문을 받아 해당 항목을 대조했다.

[REVIEW-16](https://github.com/laadkke-arch/agentflow-open/blob/e4c6a79/docs/workstreams/planning/REVIEW-16.md)을 읽고 [AF-RES-066 인계](https://github.com/laadkke-arch/agentflow-open/blob/367f29c6eb8f3da36c7728eb133f1cca9078efbf/docs/workstreams/research/AF-RES-066/HANDOFF.md) 및 RESULT.md를 인수했다. 완전 검증 관측0/24를 실제 지지0으로 해석하지 않는다. 원URL 67개와 72자리, 서로 반대 권고에 쓰인5URL은 이번 새 이슈 모집의 효과분모가 아니다. 026·030은 인수문이 밝힌 경계로만 사용하고 재조사하지 않았다.

작업은 제공된 클라우드 실행공간과 GitHub connector에서 수행했다. 실제 환경 표시에서 특정 웹 Pro UI 모델을 독립 확인한 것은 아니므로 worker_kind 배정값을 실제모델 확인으로 쓰지 않는다. 새 유료 API·계정변경·외부 댓글·사람 연락·제품 실행은 없다. 연구 수집·원장 검사와 지정 workbench 계약만 실행한다.

## 생성 당시 본문 복구

GitHub SSR HTML의 issue 객체에는 bodyVersion이 있지만 lastEditedAt가 없었다. 댓글 객체의 동명 필드를 최초 글에 귀속하지 않는다. 편집 표시 div가 빈 실제 편집글이 발견되어 SSR 빈 표시만으로 무편집을 승인하지 않았다. 공개 GH Archive hourly gzip을 읽어 type=IssuesEvent, action=opened, repository numeric ID, issue number로 생성 원문을 찾았다. body SHA-256·event ID·JSONL행·접근UTC를 남겼다. 이는 원 이슈의 같은 계보이며 별도 원저작에 산입하지 않는다.

jq의 2021 저장소는 stedolan/jq, 현재는 jqlang/jq다. repository ID 5101141로 연결했다. 작성자 계정명 변경도 numeric user ID로 확인한다. 아카이브 최초판과 현재본문이 다른 경우 원본문을 A로 사용하지만, 현재판에서 이미 읽은 추가 정보는 잊을 수 없으므로 별도 reconstructed_exposed 층으로 표시한다. 모집 슬롯을 그 뒤의 더 유리한 사례로 교체하지 않는다.

GitHub 공식 [편집 이력 안내](https://docs.github.com/en/communities/moderating-comments-and-conversations/tracking-changes-in-a-comment)와 [issue 설명 편집](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/editing-an-issue)도 직접 열었다. 이 안내는 렌더된 UI의 편집 표시 의미이며 빈 SSR div의 완전성을 보증하지 않는다. 두 문서는 방법론 보조로만 사용하고 OSS 판별 원저작8개에 산입하지 않는다.

## 노출 경계

원문 모집32개와 슬롯12개를 유지한다. ripgrep 최초판 확인이 끝나기 전에 다음8개를 연 사실은 진단/확장 조회로 보존하며 주슬롯을 바꾸지 않는다. pandoc7003의 HTML 광역탐색 중 댓글2구절 노출, 편집본문 선노출, 지정절 밖 노출은 각 pre.json에 적었다. 이러한 행을 엄격한 가림·예산효과분모로 승격하지 않는다. B는 원격 A 커밋 뒤에만 공개한다.
