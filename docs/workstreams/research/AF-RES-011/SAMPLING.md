# AF-RES-011 — 사전 고정 표본 절차 v1

고정 시각: 2026-11-20 05:10 UTC. 실제 스레드 본문·검색 결과를 보기 전에 이 파일과 CODEBOOK.md를 커밋한다. source_commit: `020c8d002cf782079053441368ed3e4a95b3289f`. 지정 의존 SHA는 manifest.json에 있다. 지침·고정 입력은 GitHub에서 직접 읽었다. 모집단의 무작위 표본이 아닌 **검색 결과 순서에 따른 층화 연속 편의표본**이다. 비율은 이 표본의 기술통계만 뜻한다.

## 1. 범위와 순서

- 기간: 2014-01-01부터 2026-11-20 UTC까지 게시된 공개 질문. 오래된 답의 관측 때문에 2019년보다 넓게 시작한다. 게시일 미확인은 본표본에서 제외한다.
- 포함: 구체 소프트웨어 목적·설계·부품·도구·방법을 찾는 질문이며, 추천/설명을 하는 답변이 2개 이상 본문으로 열람 가능. GitHub/HN/Reddit/기타에서는 서로 구별되는 실질적 응답 2개를 뜻한다. 단순 감사/봇/중복은 답 수에 넣지 않는다.
- 제외: 출시 홍보/Show HN/설문만, 단순 오류 해결만, 비공개/로그인 필요, 원문 질문 삭제, 답이 2개 미만, 2014 이전, 질문·답·댓글 본문을 확인할 수 없음, 한 스레드의 중복 URL. 실질 응답이 80개를 넘거나 전체 댓글을 도구에서 더 읽을 수 없으면 `coverage_limit`로 별도 기록하고 본표본에서 제외한다.
- 전체(whole): 그 목적을 끝까지 수행하는 앱/서비스/운영 도구를 찾음. 부분(part): 기존 또는 계획한 시스템에 넣을 라이브러리·API·프로토콜·알고리즘·하위 기능/방법을 찾음. 한 문장만으로 묻는 것도 허용한다. 개발자라는 신원은 추론하지 않는다.
- 스레드 ID: T001–T030 SR SE(전체15/부분15), T031–T040 Ask HN(전체5/부분5), T041–T050 Reddit(전체5/부분5), T051–T055 GitHub(부분5), T056–T060 기타(전체3/부분2). 기타에는 한국어 개발 커뮤니티 최소1개, 서로 다른 사이트 최소2개를 포함한다. 이 목표는 28 whole/32 part다. 어떤 층의 정해진 범위가 부족하면 그 플랫폼에서 다음 쿼리의 적격 사례를 순서대로 추가하며 전체/부분 최소20씩을 보존한다. 플랫폼 최소개수는 다른 사이트로 대체하지 않는다.

## 2. 검색 질의와 정렬

기본은 web search의 system2 엔진, 관련도 순서다. 반환된 순위 그대로 후보를 조사하고, 순위·URL·포함/제외 이유를 `evidence/screening-*.json`에 남긴다. 첫 질의에서 해당 범위 할당량을 채우면 다음 질의로 이동하지 않는다. 0개/부족/본문 접근 실패면 다음 질의를 순서대로 수행한다. system2에서 부족하면 **동일 질의**를 system1으로 확인하고 엔진 변경을 기록한다. 검색 시 아래 각 문자열 뒤에 `after:2014-01-01 before:2026-11-21`을 붙인다. 검색엔진의 날짜 필터를 믿지 않고 본문 게시일을 확인한다.

| 순서 | 층 | 질의 문자열(각 셀 안의 순서) |
|---|---|---|
| S1–S4 | SR whole | `site:softwarerecs.stackexchange.com/questions/ "open source" "alternative"`; `site:softwarerecs.stackexchange.com/questions/ "self hosted"`; `site:softwarerecs.stackexchange.com/questions/ "looking for" "software"`; `site:softwarerecs.stackexchange.com/questions/ "free" "offline"` |
| S5–S8 | SR part | `site:softwarerecs.stackexchange.com/questions/ "library"`; `site:softwarerecs.stackexchange.com/questions/ "API"`; `site:softwarerecs.stackexchange.com/questions/ "framework"`; `site:softwarerecs.stackexchange.com/questions/ "algorithm"` |
| H1–H4 | HN whole | `site:news.ycombinator.com/item "Ask HN" "alternative"`; `site:news.ycombinator.com/item "Ask HN" "self-hosted"`; `site:news.ycombinator.com/item "Ask HN" "recommend" "tool"`; `site:news.ycombinator.com/item "Ask HN" "looking for"` |
| H5–H8 | HN part | `site:news.ycombinator.com/item "Ask HN" "library"`; `site:news.ycombinator.com/item "Ask HN" "framework"`; `site:news.ycombinator.com/item "Ask HN" "API"`; `site:news.ycombinator.com/item "Ask HN" "queue"` |
| R1–R4 | Reddit whole | `site:reddit.com/r/selfhosted/comments/ "alternative"`; `site:reddit.com/r/selfhosted/comments/ "looking for"`; `site:reddit.com/r/devops/comments/ "recommend" "tool"`; `site:reddit.com/r/selfhosted/comments/ "recommend" "offline"` |
| R5–R8 | Reddit part | `site:reddit.com/r/softwarearchitecture/comments/ "recommend"`; `site:reddit.com/r/ExperiencedDevs/comments/ "library"`; `site:reddit.com/r/devops/comments/ "library"`; `site:reddit.com/r/selfhosted/comments/ "API" "looking"` |
| G1–G4 | GitHub part | `site:github.com "discussions" "is there a library"`; `site:github.com "issues" "alternative to" "library"`; `site:github.com "discussions" "recommend" "library"`; `site:github.com "issues" "looking for" "library"` |
| O1–O4 | 기타 | `site:lobste.rs "ask" "alternative"`; `site:lobste.rs "library" "recommend"`; `site:news.hada.io "추천" "도구"`; `site:okky.kr "라이브러리" "추천"` |

동일 질의가 10개 미만의 후보만 반환하면 도구가 반환한 후보 전부를 기록한다. 결과를 보기 전에 부족 층의 보완 질의를 SAMPLING 변경란에 커밋할 수 있다. 특정 성공/실패 결과를 얻기 위한 본표본 재선택은 금지한다.

## 3. 반례 찾기와 0답 질문

본표본 완료 여부와 별도로 다음 질의를 순서대로 쓴다: `site:softwarerecs.stackexchange.com "closed" "requirements"`, `site:softwarerecs.meta.stackexchange.com "too strict"`, `site:softwarerecs.stackexchange.com "does not" "requirement"`, `site:news.ycombinator.com "Ask HN" "thanks" "clarify"`, `site:reddit.com/r/selfhosted "doesn't meet"`, `site:softwarerecs.stackexchange.com "dead link"`. 날짜 범위는 동일하다. 2답 미만/폐쇄/상위80응답 초과 사례는 `supplementary`로 구분하고 본표본 빈도 분모에 넣지 않는다. 근접 오답 10개가 본표본에 없으면 보완 사례로 찾되 본표본 수치와 혼합하지 않는다.

## 4. 열람·링크·개인정보

스레드 질문, 실질 답변, 공개 댓글을 직접 연다. 검색 snippet은 D0이며 포함하지 않는다. 더보기/페이지가 남으면 열거나 coverage 한계를 기록한다. 저장에는 사용자 이름·프로필·개인 연락처를 제외하고 질문자/답변자/댓글 작성자로 부른다. 원문 전재 없이 요약하며 직접 인용은 스레드 전체에서25단어 이하다.

각 코드화한 답에서 후보의 대표 추천 URL을 중복 제거해 직접 연다. 후보 URL이 없으면 `not_linked`로 남긴다. 현재 접근 결과는 D3 단회 도구 관측이며 접속 가능/이동/보관됨/실패/접근차단을 분리한다. 접속 차단은 죽은 링크로 세지 않는다. 제품의 유지 여부는 HTTP 성공으로 추정하지 않는다.

## 5. 내부 별도 재코딩

본표본60개를 고정한 뒤 `random.Random(1101).sample(sorted(case_ids), 15)`로15개를 뽑는다. 기존 코딩·ANALYSIS를 보지 않은 새 문맥의 내부 별도 검토자에게 코드북과 URL/ID만 준다. 새 검토자는 원문을 열어 같은 주요 변수를 코딩한다. 원응답을 먼저 저장하고 이후 차이를 비교한다. 일치율은 AI 내부 코딩 안정성이지 사람 타당성/사용자 효용이 아니다.

## 6. 변경·건너뛴 후보 기록

v1: 표본 열람 전 고정. 건너뛴 후보는 실시간으로 `evidence/screening-*.json`에 누적하고, 최종 이 파일에 총수·이유·경로를 연결한다. 이 시점에는 아직 스레드 검색/열람하지 않았다.
