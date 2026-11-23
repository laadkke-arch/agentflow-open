# Markdown 요구 모집·사전 판정 기록

- 모집 URL: https://api.github.com/search/issues?q=repo%3Aremarkjs%2Fremark%20is%3Aissue%20created%3A2022-01-01..2024-12-31&sort=created&order=asc&per_page=40&page=1
- 결과: total_count=40, incomplete_results=false. 2022~2024 범위의 전체 공개 issue 40개이며 PR 제외. created_at UTC 오름차순, 동률 번호 오름차순으로 검토. 첫40과 전체40이 일치한다.
- 본문 열람: 40건 모두 개별 GitHub issue API를 직접 열었다. 검색은 발견·모집 경로로만 사용했다. 댓글 본문은 읽지 않았다. 검색/issue 메타데이터에서 라벨·댓글 개수·closed 상태는 노출되었다.
- 최초판: API의 현재 본문이 이번 세션에서 확보한 최초 가용 본문이다. 생성 당시 revision은 복원하지 못했다. updated_at는 댓글·상태 변경도 포함하므로 본문 수정시각으로 쓰지 않는다.
- 본문 line locator: CRLF를 LF로 바꾼 issue body의 1-based line. 공개 저장 파일에는 원문 전문 대신 SHA256·자체 요약·URL·행을 남긴다. 전문은 추적 제외 cache에만 둔다.
- 모집 기준 해석: 이미 고른 도구의 버그/설정 질문도 부품 또는 조합의 적합성을 판단해야 하는 출력·환경 요구이면 포함한다. 단일 릴리스·오타·배포장소 요청은 제외한다. 새 플러그인 이름 추천 문구가 반드시 있어야 한다고 범위를 임의로 좁히지 않는다.
- 조건 독립성: 같은 문장의 긍정/부정 반복으로 둘을 만들지 않는다. 서로 다른 출력문맥에 대한 실패를 별도로 확인할 수 있거나 명시된 입출력·환경 제약을 별도 확인할 수 있으면 구분한다. 단순 버전·OS 나열을 둘째 기능조건으로 만들지 않는다. M-N1의 lang-null fence와 lang-preserving first node, M-N2의 span 및 pre/code에 대한 엔티티 출력이 두 사전 조건이다.
- 자연층: M-N1=#941, M-N2=#955. 최초 두 적격 요청을 선택했다. 이후 요구로 대체하지 않는다.
- 후보 목록과 공급자 문서는 아직 열지 않았다. 후속 보강층에서 요구를 재사용할 때 공통 requirement_id를 유지한다. frame의 eligible_after_two는 사전 요구 풀 후보이며 자연층 교체가 아니다.
- 두 선택 issue의 CodeSandbox 첨부를 web open으로 시도했으나 둘 다 not accessible/Internal Error. 본문 내 입력/출력은 읽었다. 첨부 미열람으로 누락될 수 있는 실행 dependency/config는 미확인이다.
- M-N1 본문의 react-stringify 패키지 철자를 remark-stringify로 고치지 않는다. 실제 대상 식별 미확인은 이후 판단에 계속 붙인다.
- M-N2의 span 및 block에 대해 같은 판·같은 조합 증거가 필요하다. literal greater-than을 HTML 의미상 허용한다는 반론은 사용자 raw-output 조건을 대체하지 않는다.

## 첨부 실패

| ID | URL | 확인 결과 | 판단을 바꿀 최소 자료 |
| --- | --- | --- | --- |
| M-FAIL-941 | https://codesandbox.io/s/beautiful-water-1j3fe?file=/src/App.js:0-1695 | web open: not accessible / Internal Error | 최초 sandbox의 package.json와 App.js 원문; react-stringify 명칭과 실제 호출 확인 |
| M-FAIL-955 | https://codesandbox.io/s/smoosh-grass-db4x2b | web open: not accessible / Internal Error | 최초 sandbox의 입력 Markdown와 전체 pipeline/serializer options |

후속 목록·후보를 읽은 결과로 기능명사나 필수조건을 보태지 않는다.
