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

v1: 표본 열람 전 고정. 건너뛴 후보는 실시간으로 `evidence/screening-*.json`에 누적하고, 최종 이 파일에 총수·이유·경로를 연결한다. v1 고정 때에는 아직 스레드 검색/열람하지 않았다.

### 보완 질의 사전 고정 — 2026-11-20 (정확한 시각은 이 변경의 원격 커밋)

초기 S1–S4/H1–H4 검색에서 태그·목록·설문·Show HN 비중이 높아 원래 질의만으로 층을 채우지 못했다. 아래 보완은 해당 결과를 보기 전에 추가한다. 포함 기준·최소 답 수·완전열람 기준·코딩은 바꾸지 않는다.

- S9–S16: 각각 S1–S8 원문에 `-inurl:tagged -inurl:users -inurl:ask`를 추가, 동일 날짜필터/engine2→동일 engine1 순서. 그 뒤에도 부족하면 원래 검색에 처음 나타난 해당 범위의 태그/질문 목록을 열어 **보이는 정렬·순서 그대로** 질문 링크를 검사한다. 목록 주소/정렬/페이지/행순서를 기록하며 결과에 맞춰 정렬을 바꾸지 않는다. 페이지가 끝나면 다음 페이지를 순서대로 열 수 있다.
- H9: `site:news.ycombinator.com/item "Ask HN" "alternative to" "open source"`
- H10: `site:news.ycombinator.com/item "Ask HN" "recommend" "library"`
- H11: `site:news.ycombinator.com/item "Ask HN" "looking for" "software"`
- H9–H11에도 동일 날짜필터·관련도 순서·engine2→동일 engine1을 적용한다. 원래 H1–H8을 먼저 소진한다.

셸 git push는 인증 부재로 실패했으므로 연결된 GitHub의 tree/commit/ref API로 같은 파일 묶음을 원격 커밋·게시한다. 첫 원격 고정 커밋은 `b1dc4258a6714cfedbc711eb271d022ee21ca71d`이며 실제 표본 조사는 그 뒤 시작했다.

### Reddit 보완 질의 사전 고정 — 2026-11-20 (이 변경 커밋 이후 실행)

R1–R8은 책 추천·홍보·프로필·단순 설문을 다수 반환했고, 개별 적격 후보 중에는 본문 접근 실패도 있었다. 기존 네 Reddit 사례는 보존하고 부족한 whole1/part5를 다음 순서로 선별한다. 기존 검색 결과의 프로필 URL은 개인정보 최소화를 위해 사용자명을 가린 `profile_result_redacted`로 제외 기록한다. 날짜 메타데이터가 검색 결과에 명시되고 본문 상대 날짜와 모순되지 않으면 날짜의 출처를 `search_published_metadata`로 따로 적는다. 본문 읽기 대신 검색 snippet을 쓰는 것은 여전히 금지한다.

1. R9 `site:reddit.com/r/softwarearchitecture/comments/ "recommend" "library" -book -books`
2. R10 `site:reddit.com/r/ExperiencedDevs/comments/ "recommend" "authentication"`
3. R11 `site:reddit.com/r/devops/comments/ "recommend" "queue"`
4. R12 `site:reddit.com/r/selfhosted/comments/ "looking for" "API" -inurl:user -intitle:removed -intitle:weekly`
5. R13 `site:reddit.com/r/selfhosted/comments/ "alternative to" "backup"`
6. R14 `site:reddit.com/r/golang/comments/ "recommend" "library"`
7. R15 `site:reddit.com/r/rust/comments/ "recommend" "library"`

동일 기간·정렬·선별·공개 댓글 완전열람 기준. R9–R15 engine2에서 부족하면 동일 engine1. 새로운 서브레딧을 실제 채택하면 그 규칙도 비스레드 원장에 포함한다. 전체/부분 할당을 채운 뒤 나온 후보는 `quota_filled`로 남긴다.

### GitHub·기타 보완 질의 사전 고정 — 2026-11-20

G1–G4 및 O1–O4에서 저장소 내비게이션·기사·도서관 의미의 library 등 비적격 결과가 많았다. 원래 질의를 먼저 소진한 뒤, 다음을 이 변경 커밋 이후 실행한다. 기간·정렬·최소 실질 답 2개·완전 열람 기준은 같다.

- G5 `site:github.com inurl:discussions "library" "recommend" -inurl:categories -inurl:topics`
- G6 `site:github.com inurl:issues "alternative to" "library" -inurl:topics`
- O5 `site:lobste.rs/s/ "ask" "looking for"`
- O6 `site:news.hada.io/topic "Ask GN" "추천"`
- O7 `site:okky.kr/questions "라이브러리" "추천"`

### GitHub 공개 이슈 검색 보완 사전 고정 — 2026-11-20

G5–G6도 웹 검색이 URL 필터를 무시하고 저장소·토픽 목록을 반환하여 부족하면, GitHub 공개 이슈 검색으로 전환한다. 이 변경 커밋 이후 G7 `is:issue is:public "alternative" "library" created:2014-01-01..2026-11-20 comments:2..80`, 이어 G8 `is:issue is:public "recommend" "library" created:2014-01-01..2026-11-20 comments:2..80`을 best-match 정렬, 처음20개씩 반환 순서로 검사한다. 댓글 수 필터는 실질 답 2개를 보장하지 않으므로 원래 포함 기준을 본문에서 다시 검사한다.

### 한국어 부분 질문 보완 사전 고정 — 2026-11-20

O1–O7을 소진한 뒤 기타 part2가 부족하면 O8 `site:news.hada.io/topic "Ask GN" "라이브러리"`를 이 변경 커밋 이후 실행한다. 기존 기간·engine2→engine1·관련도 반환순서·원문 및 2실질답 기준을 유지한다.

### Reddit 잔여 부분 질문 사전 고정 — 2026-11-20

R9–R15에서 댓글 전체 열람을 확인할 수 없는 후보를 제외하고 part 할당이 부족하면 R16 `site:reddit.com/r/golang/comments/ "looking for" "library" -book -books -resources`, R17 `site:reddit.com/r/rust/comments/ "alternative to" -book -books`, R18 `site:reddit.com/r/softwarearchitecture/comments/ "recommend" "database"`를 이 변경 커밋 이후 순서대로 실행한다. 동일 기간·engine2→동일engine1·관련도·최소2실질답·80이하 및 완전열람 기준이다.

Reddit의 R2에서 반환된 여러 앱용 VPS 질문은 완성 앱이 아닌 실행 기반(part)으로 분류했다. 원래 '부족 층의 다음 질의 적격 사례' 조항에 따라 Reddit 목표를 whole4/part6으로 기록하며, 전체60의 whole27/part33은 각각20 이상을 유지한다. 성공·거절 결과로 선택을 바꾼 것이 아니며 해당 후보는 R2 반환순번5다. 검색 호출을 병렬 묶음으로 실행한 경우 개별 질의의 가상 순위를 만들지 않고 반환 묶음의 순위를 기록한다. R3–R4는 누락을 발견해 후속 수행했고 후보의 최초 제외·재확인 이력을 보존한다.

### 공개 댓글 열람 기준의 일관성 정정 — 2026-11-20, 최종 표본 확정 이전

진행 중 지시에서 Reddit 헤더의 총 댓글 수와 도구가 노출한 댓글 노드 수가 정확히 같아야 한다는 추가 조건을 잘못 적용했다. 이는 최초 고정한 공개 본문·댓글 열람 기준에 없었으며, 삭제된 내용을 복원하지 않는 원칙과도 별개다. T045는 공개47노드(확장한 봇 하위 응답 포함)/헤더52였고, 다른 담당은 같은 유형의 차이로 후보를 제외해 일관성 문제가 드러났다.

이 변경 이후 **모든 기존 후보에 같은 기준을 재적용**한다. 현재 공개 본문을 끝까지 읽고, 남은 공개 더보기/continue가 없으면 포함할 수 있으며 헤더 수 차이는 `coverage.header_count_gap`에 보존한다. 숫자 차이의 원인을 삭제라고 단정하지 않는다. 미해결 더보기·반복 링크 때문에 공개 범위가 불명하면 기존대로 제외한다. 숫자 차이만으로 제외했던 후보는 최초 반환 순서에서 다시 판정하고, 나중에 본 후보보다 우선한다. 실질 응답80개 초과 제외는 유지한다. 이는 특정 채택·거절 결과를 보고 구제하는 예외가 아니라, 사전 절차에 없던 추가 조건의 일괄 정정이다. 분석에서는 헤더 차이 사례를 뺀 민감도 결과도 낸다.

R1/R5 최초 묶음 순번15 MediaManager는 잘린 URL로 첫 접근이 실패했던 오류를 감사에서 발견했다. 실제 반환 URL로 질문·현재 공개 댓글을 다시 확보하여 T061로 추가한다. 기존 사례를 교체하지 않고 총 표본61개(whole28/part33 예정)로 남기며, T061 제외 민감도도 낸다. 원문은 첫 관측73댓글, 재관측72댓글로 달라졌고 최종 판본을 코딩했다.

### 표본 확정과 코딩 단위 점검 — 2026-11-20 05:55:57 UTC

본표본은 **61개**다: SR30, HN10, Reddit11, GitHub5, 기타5. 전체28·부분33이다. T045는 앱 배치의 하위 인프라를 고르는 부분 질문이며, 원래 반환 URL을 잘못 줄여 제외했던 MediaManager 질문을 같은 기준으로 다시 열어 T061 전체 질문을 추가했다. 결과를 보고 기존 사례를 교체하지 않았다. 최종 선택 로그는 `evidence/screening-se.json`, `screening-hgo.json`, `screening-reddit-root.json`, `screening-reddit-part.json`에 있고 보완 반례 질의는 `evidence/counter-searches.json`에 있다. 보완·부분 열람 사례는 본표본에서 제외한다.

무작위 재코딩은 61개 전체에서 원래 seed1101로15개를 뽑았다. 목록은 `evidence/reliability-selection.json`, 비교 전 원코딩은 `evidence/reliability-original.json`에 고정했다. 새 검토자는 코드북과 URL/ID만 받았고 기존 코딩·분석은 읽지 않는다.

후속 추천·기술 설명을 같은 후보 이름으로 합쳐 세지 않도록 T041–T044와 T047을 마지막 대조했다. T044 끝의 공개 R-HUB·mRemoteNG 답도 읽고 추가했다. 답 수는 후보 종류 수가 아니며, 긴 토론이 답 빈도를 지배하는지 스레드 단위 존재율을 함께 보고한다. 숨은 댓글을 풀지 못한 사례와, 페이지를 끝까지 읽었으나 헤더 수가 다른 사례를 구별한다. T045(표시52/공개47), T049(10/9), T050(65/62)의 제외 민감도와 T061·경계 T057 제외 민감도를 분석한다.

## 7. 최종 선택 로그 요약

아래 단위는 **검색·목록 반환 기록**이다. 같은 URL이 다른 질의에 재등장하면 별도 기록이므로 포함 표시 합계나 전체 반환 수를 서로 다른 스레드 수로 해석하지 않는다. 실제 고유 본표본은 CASES의61개다. 각 행의 링크에 모든 반환순위·주소·건너뛴 이유가 있다. 집계 원본은 [screening-counts.json](evidence/screening-counts.json)이다.

| 로그 | 질의/반환 묶음·목록 | 반환 기록 | 포함 표시 기록 | 나머지 처리 |
|---|---:|---:|---:|---|
| [SR](evidence/screening-se.json) | 26질의+4목록 | 435 | 30 | 제외393, 할당 충족 뒤 미선별12 |
| [HN·GitHub·기타](evidence/screening-hgo.json) | 26묶음 | 364 | 20 | 제외344 |
| [Reddit root](evidence/screening-reddit-root.json) | 9묶음+R8추가기록 | 231 | 11 | 다른 담당 선별2, 그 밖218; 비스레드76·범위밖73·설문35·열람범위11 등 |
| [Reddit part](evidence/screening-reddit-part.json) | 14질의 | 175 | 5 | 제외168, 보완2 |

중복·날짜·원문삭제·홍보·2실질답 미달·도구 차단·미해결 더보기를 각각 구별했다. D0만 본 결과는 본문 근거 수에 들어가지 않는다. R3–R4의 늦은 실행과 R11/R13–R15 묶음 뒤 R12를 확인한 순서 차이도 로그에 보존했다. 순서가 완벽히 사전등록대로 수행됐다고 주장하지 않는다.

최종 답 단위는 블라인드 차이 감사 후635개다. 새 스레드를 결과에 맞춰 골라 넣은 것이 아니라 기존61개 안의 미포함 독립 답26개를 보완한 것이다. [extra-answer-adjudication.json](evidence/extra-answer-adjudication.json)에 추가·제외43행을 모두 남겼다. 원판 답 단위609개와 블라인드15개150/192단위는 신뢰도 비교에 그대로 보존한다.

### 한계

검색 관련도·접근 가능한 공개 댓글·2답 이상·80실질답 이하로 선택했으므로 실패한 질문, 삭제된 질문, 매우 긴 인기 토론이 덜 보인다. 폐쇄·0답·부분열람 자료는 [SR 보완](evidence/screening-se.json)과 [root 보완](evidence/supplementary-root.json)에 별도로 보존하여 반례로 읽었으나 본표본 분모와 합치지 않는다. 현재 댓글 수 변화와 페이지 캐시 때문에 이후 재열람의 수치가 같다고 보장하지 않는다.

### 최종 반례 보강 — 본표본 선정 뒤

‘링크만 답이 채택’의 관측 신호를 더 엄격히 확인하려고 X7a `site:softwarerecs.stackexchange.com "accepted" "link-only"`, X7b `site:softwarerecs.meta.stackexchange.com "link-only" "accepted"`를 추가 실행했다. 이것은 사전 고정 본표본 검색이 아니라 **사후 반증 보강**이다. 반환21기록 중 SXR08은1정식답이라 제외, SXR09는접힘댓글1로 제외하고 보완 사례만 저장했다. 전자는 최소 링크 답의 보너스 지급, 후자는 공동체가 link-only라 부른 짧은 경험 답의 명시 채택 발언을 보여준다. 공식 체크표와 같은 신호로 합치지 않았다. [질의·순서·D0 제외 목록](evidence/minimal-answer-counter-search.json). 본표본61·비 스레드30·주 링크 관측281 분모는 그대로다.

최종 메타데이터 보강(2026-11-20 08:02 UTC 이후): 익명 공개API의32질문 요청(본표본SR30+보완2)이 성공했다. 본표본 정식답85개 수가 API와 일치하며 현재 채택7개를 본문에 대응했다. SXR08의 최소링크답과SXR09의경험답도공식채택으로확인했다. 원판코딩과재코딩을덮어쓰지않고현재결과필드만보완했다. 위단락의 ‘공식체크표와합치지않음’은API확인전관측단계이며,최종분석은새근거를반영했다. 표본재선택은없다.
