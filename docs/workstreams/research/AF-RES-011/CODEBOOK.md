# AF-RES-011 — 코드북 v1.3 (원 v1은 표본 열람 전 고정)

고정 시각2026-11-20 05:10 UTC. 출발점은 AF-RES-001 `4d6208c08f6f2657865ba000d6768f6537e832b6` RESEARCH §5–7/CASES 정보명과 AF-RES-004 `2b798c7d2b7355b649691c18de196104ceabb0f0` PROTOCOL v1.1/RESEARCH §6–7이다. 선행8항목과4축을 재설계하지 않고 공개 대화에서 관측할 변수를 아래처럼 정의한다. 예시는 정의를 설명하는 합성이며 관측 사례로 세지 않는다.

## 1. 단위와 누락

단위는 스레드, 질문의 현재 보이는 판본, 각 구별되는 실질 답, 되묻기 사건이다. 최초 질문 판본을 열지 못하면 현재 편집본과 최초 입력을 혼동하지 않는다(`question_version=current_visible`). 각 코드에는 해당 문장·댓글 순서를 찾을 수 있는 짧은 요약 또는 answer/comment permalink를 evidence로 남긴다. 사용자 이름은 저장하지 않는다. `absent`=열람 범위에 없음, `unknown`=본문 미노출/시점 불명, `explicit_unknown`=질문자가 모른다고 말함, `undecided`=미정이라고 말함, `not_applicable`=이 종류 정보의 대상이 아님. 부재를 무제약으로 바꾸지 않는다.

### 1.1. 전체·부분 질문의 정의 — v1.2 명료화

이 정의는 최초 SAMPLING §1에 있었으나 v1 코드북에 빠져 있었다. 독립 재코딩 입력을 코드북으로만 제한했으므로 원래 전체·부분 일치율 6/15를 유효한 불일치로 보존한다. 아래는 새 분류 설계가 아니라 처음 표집에 쓴 정의를 그대로 전달하는 보완이다.

- `whole`: 그 목적을 끝까지 수행하는 앱·서비스·운영 도구를 찾는다.
- `part`: 기존 또는 계획한 시스템에 넣을 라이브러리·API·프로토콜·알고리즘·하위 기능·방법을 찾는다.

판정 대상은 질문의 선택 범위다. 긴 전체 앱 설명이 있어도 고를 대상이 프레임워크·DB 계층·이미지 검증 부품이면 part다. 짧은 한 문장이라도 완성 뉴스 서비스·영상 편집기·금융 관리 앱을 찾으면 whole이다. `answers[].role`은 각 답이 내놓는 대상이므로 질문의 whole_or_part와 다를 수 있다. 실제 인물이 개발자인지 추론하지 않는다.

## 2. 질문 정보8개

`info_codes`는 I1–I8 키와 `present/absent/explicit_unknown/undecided/not_applicable/unknown` 값을 가진 객체다. I1에는 `captured`도 허용한다. 세부 원문 근거는 `info_evidence` 객체에 짧게 적는다.

| 코드 | AF-RES-001 후보 | present 기준과 예시 |
|---|---|---|
| I1 | 원문 또는 다시 찾을 고정 위치 | 스레드 URL을 보존했다면 `captured`. 질문자가 추가 설계·기존 질문을 연결했으면 present. 연구자의 수집 성공을 질문의 충실성으로 세지 않는다. |
| I2 | 바라는 결과/불편 | 하려는 작업/문제/결과가 명시됨. 단순 제품명 나열만은 absent. 예: 서버 없이 노트를 동기화하고 싶음. |
| I3 | 선택 범위와 변경하지 않을 곳 | 바꾸거나 도입할 대상(노트 앱, 인증 라이브러리 등)이 명시됨. 비목표가 없어도 대상 범위가 분명하면 present; 비목표 유무는 별도 scope_fixed 기록. |
| I4 | 명시 조건의 대상·부정·강제성·이유 | 적어도 하나의 요구/선호/금지 명시. constraints 배열에 target/polarity/force/reason을 각각 기록. force=must/prefer/unclear, 미상 이유 발명 금지. |
| I5 | 직접 주변 입출력·공유 경계 | 입력/출력 자료·상대 시스템·호출 주체·공유 자원이 명시됨. 단순 OS명만으로 present를 주지 않음. 예: 기존 PostgreSQL과 REST로 연결. |
| I6 | 시점·현재/계획/예시/보고 지위 | 현재 쓰는 것, 만들 계획, 써봤다는 보고, 예시 지위를 분명히 구별. 게시일 자체는 해당하지 않음. |
| I7 | 제품 버전·실제 설정·자료형 | OS/언어/런타임·버전·구성·입력 포맷 중 적용에 구체적인 것. '오픈소스'만은 I4이지 I7 아님. 버전이 없으면 있는 설정만 근거로 기록. |
| I8 | 해석·제안과 원문 사이 관계 | 질문이 원문 인용·이전 요구·재해석/가정을 구별하거나 어떤 요청을 다시 표현했는지 연결. 그러한 변환이 없는 독립 질문은 not_applicable. 보편 필수 입력으로 평가하지 않음. 답의 요구 연결은 아래 FIT에서 별도 코딩. |

## 3. 되묻기

실질적으로 추가 정보를 요구하는 문장만 코딩한다. 수사적 반박·단순 도구 추천을 질문 형태로 말한 것은 제외한다. 코드: C_GOAL(결과/왜), C_SCOPE(어느 부분/대체 범위), C_CONSTRAINT(가격/라이선스/금지/강제성), C_IO(입출력·연동·규모), C_CONTEXT(언어/OS/버전/설정), C_TIME(현재/계획·시점), C_TRIED(이미 시도한 것/실패 이유), C_TERM(용어 의미), C_PRIORITY(조건 간 우선순위), C_CONFIRM(이해한 요청 확인). 복수면 가장 직접적인 코드 하나를 primary로 기록하고 secondary에 나머지를 둔다.

`changed_answer=yes`: 되묻기에 질문자가 답한 후 후보/설명/질문 수정이 뒤따랐다는 순서와 내용을 실제 확인. `no`: 질문자 응답이 있고 그 뒤 같은 추천 유지/필요없음을 명시적으로 확인. `unknown`: 무응답·관측 창 이후·순서 불명·수정 이력 없음. 무응답을 no 또는 이탈의 인과 증거로 세지 않는다. `decision_changed`에는 답에 따라 달라질 판단 한 문장을 적고, 단지 보완 설명인지 후보 선택 변경인지 `change_kind`로 구별한다.

## 4. 답의 형태·역할·반응

- form: `comparison_table`(실제 표), `experience`(직접 사용 근거가 주 설명), `link_explanation`(링크+기능/조건 설명), `link_only`(URL/이름+권유만), `text_only`(원리·절차 설명이나 링크 없는 설명). 표→경험→설명→링크 순으로 primary 하나를 부여하고 필요하면 secondary_forms에 추가한다.
- role: `product`(전체 목적 수행 앱/서비스), `component`(삽입할 부분), `principle`(재사용 원리·방법), `mixed`(분리하기 어려운 복수 역할). 추천 도구가 library라도 전체 질문의 목적을 끝내는 앱을 추천한 답은 product다.
- codes: `FIT`(질문의 특정 조건/부분과 명시 대응), `TRADEOFF`(한계/대가), `PERSONAL_USE`(사용 경험), `CROSS_DOMAIN`(다른 종류 제품/분야의 관계를 대상 문제로 옮김). 단순히 다른 브랜드나 언어는 CROSS_DOMAIN 아님.
- outcome 객체: `accepted`(true/false/null), `top_voted`(true/false/null), `asker_response`(`adopt/reject/try/thanks/none/unknown`), `observed_reason` 요약. 체크표/점수/질문자 발언을 구별한다. 감사는 채택 아님, 채택은 실제 통합 성공 아님, 추천점수는 질문자 채택 아님. null=표식이 보이지 않음.
- `rejection_codes`는 실제 질문자/댓글 작성자가 거절·비판한 경우만 부여. 연구자의 기능 의심은 notes.hypothesis에 둔다. 질문자가 이미 시도하고 배제한 후보는 `preexisting_rejections`에 별도 기록해 답 거절과 혼합하지 않는다.

## 5. L/E/H/T 대응과 추가 이유

| 코드 | 정의/기준 |
|---|---|
| L | 연결 주소/출처가 없거나 잘못되거나 끊어져 판단할 근거를 못 찾는다는 반박. |
| E | 추천의 구체 사실 주장이 잘못됐다는 반박. 주장의 조건·버전을 분리. 다른 제품문서 확인을 하지 않았다면 '참여자 주장'으로 한정. |
| H | 질문에 명시된 필수 조건을 추천 사용 방식이 위반. 선호 차이만을 H로 올리지 않음. |
| T | 다른 분야의 원리를 옮길 때 대응/연결 작업/실패 조건이 부족하거나 달라 적용 불가라는 반박. 일반 설치 난이도만은 T 아님. |
| M | 유지보수·관리 중단·업데이트·프로젝트 수명. |
| C | 커뮤니티 규모·생태계·지원·성숙도. |
| P | 가격·예산·운영 비용. |
| LIC | 라이선스·공개성·사용권. |
| TRUST | 보안·개인정보·벤더 신뢰·이해상충. |
| UX | 편의·학습/운영 부담·취향·복잡성. |
| EXP | 사용 경험·실측 결과·팀 숙련/기존 투자. |
| OTHER | 위 분류 밖 이유. 반드시 자유문을 남김. |

다중 코딩 허용: 예산이 필수이면 H+P, 단순 가격 선호이면 P. 유지 중단 자체가 처음 명시된 금지이면 H+M, 나중에 드러난 위험평가이면 M. **모든 이유를 사후 H로 흡수하지 않는다.** 추가 이유가 L/E/H/T 밖인 경우와 축의 입력조건으로 뒤늦게 편입된 경우를 분석에서 나눈다. 채택 이유에도 같은 사유 코드를 쓸 수 있으나 긍정/부정 방향을 분리한다.

AF-RES-004 4라벨은 `SURFACE_OR_CONSTRAINT_MISMATCH / INSUFFICIENT / CONDITIONAL_TRANSFER / DIRECT_DOCUMENTED` 그대로다. 이 관측 연구에서는 대화만으로 DIRECT_DOCUMENTED를 자동 부여하지 않는다. 실제 거절된 근접 오답은 핵심 필수 조건과 거절 근거가 둘 다 보일 때만 SURFACE_OR_CONSTRAINT_MISMATCH 대응 사례로 인정한다. 모름/무응답/미채택은 근접 오답이 아니다.

## 6. 링크 관측 및 오래됨

`link_status_now`는 배열: url, observed_at_utc, status(`accessible/redirected/archived/failed/blocked/not_linked`), final_url, evidence. 실제 URL 관측은 level=D3, 문서에 링크가 없는 not_linked는 D1이다. 접근 성공은 유지/기능 보증 아님. 도구가 접근 거절하면 blocked, 원격404/도메인 소실이 명시되면 failed. 리포지터리 배너로 archived를 확인. 옛 댓글의 dead/unmaintained 지적은 `historical_status_claim`으로 저장하고 현재 단회 결과와 섞지 않는다. URL fragment는 같은 문서로 중복 제거한다.

## 7. 저장·분석·재코딩

CASES.json 루트는 `{study_id, codebook_version, cases:[...]}`. 필수 case 필드는 사용자 지정 id/url/platform/date/accessed_at_utc/whole_or_part/question_summary/info_codes/clarifications/answers/link_status_now/notes. 추가 evidence/constraints/selection/coverage 필드를 둔다. platform enum=`softwarerecs/hackernews/reddit/github/other`. 분석은 스레드 분모와 답 분모를 명확히 나누고 결측을 별도 센다. 15개 내부 별도 재코딩은 I2–I8·whole_or_part·되묻기 유무·답 형태/역할·반응/거절·근접오답을 비교한다. I1의 수집성공은 자명한 동의로 일치율을 부풀리지 않는다.

## 변경 이력

- v1: 공개 사례 검색/열람 전 고정. 이후 새 코드가 필요하면 이유·시점·영향 ID를 남기고 기존 사례도 같은 규칙으로 재검토한다. 원판 코딩과 재코딩 원응답을 덮어쓰지 않는다.
- v1.1 (2026-11-20, 첫20개 묶음 이후·내부 재코딩 이전): 실제 댓글에는 원질문자에게 정보를 묻는 사건 외에 질문자가 추천 기능을 되묻거나 다른 독자가 답변자를 반문하는 사건이 있었다. `target`(`question/recommendation/side_discussion`)과 `respondent`(`original_asker/answerer_not_original_asker/other_commenter/none/unknown`)를 추가한다. v1의 `changed_answer=yes` 기준은 완화하지 않는다. 원질문자의 응답 뒤 변경 순서가 없는 다른 독자의 설명 정정은 `changed_answer=unknown`, 별도 `changed_explanation=yes`로 구별한다. 영향: T043·T045의 비원질문자 반문을 교정하고 모든 후속 사례에 같은 구별을 적용한다. 주 Q2의 빈도는 원질문자에 대한 되묻기이고, 추천 설명·곁가지 반문은 별도 표로 보고한다.
- v1.1의 형식 명료화: 이름/도메인+권유만은 링크 유무와 무관하게 `link_only`(최소 후보 제시)다. 기능이나 사용 조건 설명이 있지만 실제 URL이 없으면 `text_only`다. 실제 웹 링크만을 좁혀 센 결과를 별도로 보고해 명칭만 제시와 URL만 제시를 혼합하지 않는다. 원래 v1의 URL/이름 정의를 유지한 명료화이며 T044의 URL 없는 설명 2개를 교정한다.

- v1.2 (2026-11-20, 블라인드 원응답 수령 후): whole/part 정의 누락을 발견해 최초 SAMPLING §1의 정의를 §1.1로 옮겼다. 원코딩·블라인드 원응답은 수정하지 않는다. 정보 항목·되묻기·형식·L/E/H/T 정의는 바꾸지 않는다. 15개 범위만 원판 코드를 주지 않고 추가 재코딩해 입력 정의의 영향을 따로 보고하며 최초 40% 일치율을 대체하지 않는다.

- v1.3 (2026-11-20, 원판 재코딩 비교 뒤): 명백한 정보·형식 오류와 누락 답 단위를 보정하고 `evidence/adjudications.json`에 old/new·이유를 남겼다. 실제 하이퍼링크 부재(not_linked)는 D1, URL 열람은 D3로 구별한다. 같은 후보 이름이라도 독립된 사용 조건·구현·경험을 더하는 후속 답은 보존하고, 이미 부모 답의 반박 요약에 든 내용은 중복 추가하지 않는다. 추가43단위 중26을 포함하고17을 제외한 전수 판정은 `extra-answer-adjudication.json`에 있다. 원판15개의 코딩·블라인드 응답은 불변이다.
- v1.3의 축 적용 명료화: 링크가 이미 있는 답에 설명·예제를 요구하는 것은 OTHER, 실제 주소/출처 부재·오류는 L이다. 타분야 위험의 비유나 같은 제품군 대안은 CROSS_DOMAIN으로 세지 않는다. 다른 제품 기능을 문제에 사용하는 명시 관계(DB→큐 등)는 포함하고 다른 학문분야 전이와 구별한다. 기능·지원 조건의 반박은 실제 선택 철회와 다를 수 있다.
- v1.3의 반응 명료화: `adopt`의 identified/plan/in_progress/reported_use/integration 단계를 별도 기록한다. `try`도 read_or_consider_or_plan과 actual_trial을 구별한다. 2015년에 추가된 조건이 2017년 답보다 앞설 수 있으므로, 근접 오답의 시간 기준은 ‘최초 질문판’이 아니라 **해당 추천 시점에 알려진 조건**이다. 다른 독자가 그 뒤 새로 밝힌 필수조건은 별도 보완 사례다.
