# AgentFlow Open 최종 설계서 v1 · 확인 장부 구조

상태: 구현 착수용 설계(2026-11-26). 이 설계서는 연구 원장, 기존 설계 `gallim`(고정판 [`fc68f0d1`][gallim]), 병행 설계 세 갈래(PR #6 [`8f674773`][pr6], PR #7 [`8fbc885d`][pr7], PR #8 [`72e8aee2`][pr8])와 이번에 쓴 부문별 상세 설계 셋을 하나로 묶는다. 근거 표시는 셋이다. **(a)** 문서 판독, **(b)** 고정 입력에서 코드로 확인, **(c)** 실제 사용자나 운영이 있어야 아는 것. 이 설계서가 새로 세운 가정은 본문에서 **[가정]**으로 표시하고 [06-assumptions-handoff.md](06-assumptions-handoff.md)에 따로 모았다.

재검토(2026-11-26): [07-review.md](07-review.md)가 사례 재생의 손을 떼고 실제 시계·작업자·예산·여러 프로젝트를 붙인 운영 시뮬레이션으로 이 설계를 다시 봤다. 뼈대(관측과 판단 분리, 사용 쪽지 전파, 덧붙이기 전용)는 버텼고, 시계·예산·이름·언어·정정 경로에서 빈칸이 나왔다. 엔진 고침 15건을 반영했고, 설계 결정 11개를 확정해 엔진에 넣었다(안이 갈리는 다섯은 후보안을 시뮬레이션으로 비교해 골랐다). 확정 뒤 13장면 중 8장면이 유지다. 남은 다섯 장면을 닫을 우선순위 붙은 조사 14개도 그 문서에 있다. 그 문서의 **(s)**는 시뮬레이션 값이다.

## 읽는 순서

| 문서 | 내용 |
| --- | --- |
| 이 문서 | 1장. 왜 이 구조인가, 가장 강한 경쟁안이 이기는 때, 기존 설계에서 가장 크게 바뀐 것 |
| [02-landscape.md](02-landscape.md) | 연구 지형, 다섯 판단 문제의 답, 기존 설계의 약속·확인·미확인과 채택·폐기 |
| [03-concepts.md](03-concepts.md) | 경쟁 개념 일곱, 세 질문 비교, 전제 뒤집기, 낯선 분야의 운영 원리, 섞을 때의 전제 확인 |
| [04-architecture.md](04-architecture.md) | 구성요소와 데이터 소유, 입출력 계약, 저장·조회 예, 세 시계, 변경·실패·복구, 운영 지표 |
| [05-cases.md](05-cases.md) | 사례 추적 둘(R1 기존안 대 새 구조, 봉인 사례 EVAL-X1), 장면 2(R2), 구성요소 삭제 시험 |
| [06-assumptions-handoff.md](06-assumptions-handoff.md) | 새 가정 목록, 첫 구현 단위, 실제 사용 시험, 열린 질문 |
| [07-review.md](07-review.md) | 재검토. 몇 달 운영 시뮬레이션 13장면의 전후 결과, 부문별 빈칸·모순, 이번에 고친 것, 확정한 설계 결정 11개와 비교 결과, 우선순위 붙은 추가 조사 |
| [08-implementation.md](08-implementation.md) | 구현 노트. 첫 구현 단위([`ledger/`](../../../ledger/README.md))에서 드러난 설계 수정점 I1~I36, 완료 기준 다섯과 첫 측정 둘(A4·B1)의 결과, R-5 결정(다국어 토큰화), R-6(서랍 순위, 보류), 둘째 단위(변경 채널·감시: 채널 커서 I35, 판 사이 위치 I36) |
| [09-source-access.md](09-source-access.md) | 원문 접근. GitHub 밖 원문을 어디서 가져오고 어떻게 믿나: 이 환경에서 닿는 곳, catalog 23,395개의 경로별 측정, 다른 방식 조사·비교, 경로 사다리와 따로 둔 포착 일꾼, 결속 표시(L3d·L3s·L3a), 결정 D12~D18 |
| [sections/](sections/) | 부문별 상세 설계 셋. 요청·답변과 제품 효용, 검색·판단·조합, 발견·수집과 관리·운영. 각 문서 머리에 총괄 판정이 있다 |
| [landscape/](landscape/) | 부문별 연구 지형 정리 다섯(원장 행까지 고정 링크) |
| [db/](db/) | 저장 구조 실행 예제. 스키마, 엔진, 세 사례 재생, 시험 40개, 실행 기록 |
| [sim/](sim/) | 운영 시뮬레이션(`ops_sim.py`, v1 엔진 결과와 고친 엔진 결과)과 결정 비교(`decide_sim.py`, 갈리는 결정의 후보안을 같은 세계에 돌린다) |

## 1장. 왜 이 구조인가

### 1.1 한 문단

사용자가 Studio에서 프로젝트의 한 부분을 가리키며 물으면, 제품은 그때 찾는다. 기억 서랍과 새 검색을 나란히 돌리고, 후보를 **사용자의 판**에서 열어 그 일을 실제로 하는 절이나 줄을 찾거나 작게 실행해 본다. 답은 1~3자리이고 비어도 된다. 자리마다 고정판 첫 링크, 좁은 동사, 이유 한 줄, 근거 수준, 철회 조건이 붙는다. 확인한 것은 둘로 나눠 남긴다. **원문에 대해 말한 것**(어느 주소의 어느 판, 어느 위치에서 무엇을 보았나)은 공개 관측으로 모든 프로젝트가 같이 쓴다. **사용자의 필요에 대해 말한 것**(이 요청의 어느 조건을 무엇이 채웠나)은 그 프로젝트의 비공개 쪽지로 둔다. 비공개 쪽지는 공개 관측을 ID로만 가리키고, 공개 관측은 어떤 프로젝트도 가리키지 않는다. 이름은 **확인 장부 구조**다.

### 1.2 세 질문에 대한 답

| 질문 | 답 |
| --- | --- |
| 무엇을 미리 알아 두었나 | 원문 사본이 아니다. 세 가지다. ① 이미 읽은 원문의 관측과, 그 관측에 원문 쪽 말로 붙인 "무엇을 받아 무엇을 내고, 그것이 없는 누가 쓰며, 무엇을 지키고, 언제 깨지나" 꼬리표. ② 이미 읽고 있던 소식 흐름에서 처음 본 작은 기능을 추가로 읽지 않고 남긴 "청구 없는 관측". ③ 공급자별 변경 채널의 주소와 커서, 관측마다 단 감시 키와 공지 기한 |
| 요청이 온 뒤 무엇을 새로 했나 | 요청판을 원문 그대로 고정하고 Studio에서 판·환경·위치를 받는다. 해석이 갈리면 정해진 순서로 처리한다. 첫 절이 같으면 진행하고, 다른 명시 칸이 정하면 골라서 첫 줄에 밝히고, 두 뜻을 함께 채우는 행동이 있으면 그것을 주고, 그다음이 회수와 실행이며, 되돌릴 수 없을 때만 한 번 묻는다. 서랍과 새 검색(직접, 분야 이름 없는 관계 문장, 분야 추정, 언어의 네 갈래)을 나란히 돌린다. 후보를 사용자의 판에서 열어 확인하고, 원리 후보는 관문 셋을 통과할 때만 자리를 준다. 답을 조합하고 탐색·판정·인용 기록을 한 번에 쓴다 |
| 무엇을 기억했기에 다음 요청이 달라지나 | 같은 판·같은 위치의 관측은 다시 읽지 않고 쓴다(감시가 건전하면 아예 열지 않는다). 판이 바뀌면 그 판의 같은 위치만 다시 연다. 같은 프로젝트의 새 요청판은 지난 쪽지 가운데 요건 사실이 같고 판이 맞는 것만 물려받는다. 변경 채널 항목이 어떤 관측의 뒤집을 위치에 닿으면, 그 관측을 인용한 답 자리에만 알림이 간다. 다른 프로젝트는 판단을 물려받지 않고 공개 관측만 다시 쓴다. 몇 달 뒤 다른 이름의 질문은 이름이 아니라 꼬리표의 칸으로 옛 관측에 닿는다 |

### 1.3 두 장면을 잇는 구조

두 장면은 같은 장부의 두 끝이다.

- **장면 1(오늘 누군가 한 부분을 가리키며 묻는다).** 놀랍지만 쓸모 있는 원문은 "검색이 높게 올린 것"에서 나오지 않는다. R1에서 기존 설계의 어휘 순위 1·2위는 `13`, `3`, `python`만 겹쳤고 답은 0개였다(b, [PR #7 p8][p8]). 새 구조에서 R1의 첫 자리는 서랍에서 다섯 칸이 맞은 `asyncio.Queue` 관측이 차지한다. 사용자의 판(CPython 3.13.18)의 `queues.py` L36–38을 읽고 입력 40개로 실행해 대기 최대 8, 처리 중 최대 4를 확인했다(b, [실행 기록](db/out/cases.json)). 놀라움은 "직접 만들던 투입·완료 신호가 통째로 없어진다"는 데 있다. 쓸모는 그 판의 줄과 영수증이 보증한다.
- **장면 2(오늘 처음 본 외국어 도구가 몇 달 뒤 다른 질문에서 다시 발견된다).** 2026-11-26 수집 흐름은 일본어 소식 다이제스트에서 ii-svn-log 제작자 글을 이미 읽었다. 제품은 추가 열람 없이(열람 0회) 관측 한 행과 꼬리표 다섯 벌을 남긴다. 꼬리표는 이름이 아니라 칸이다. 예를 들어 `user_without` 칸은 "people on a PC without Subversion can view and share the history"이다. 2027-03 다른 사용자가 "AI 작업 기록을 우리 도구를 설치하지 않은 외부 감리자에게 넘기고 싶다"고 물으면, 요청에는 SVN·Excel·이름 중 어느 말도 없다. 그래도 서랍이 `input`·`output`·`user_without` 세 칸에서 tool·exported·file·standalone·pc가 맞아 이 관측을 찾는다. 새 검색은 이 일본어 개인 글을 찾지 못한다고 둔 고정 입력에서, 이 후보는 서랍에서만 나왔다(b, [05-cases.md 4절](05-cases.md#4-장면-2-r2-ii-svn-log)).

두 장면을 잇는 것은 세 가지 기록이다.

1. **관측의 키가 (주소 원문 문자열, 판, 위치)다.** 요청 때 연 원문과 수집 때 본 원문이 같은 장부에 같은 키로 들어간다. 그래서 장면 1에서 열었지만 답에 쓰지 않은 원문도, 장면 2에서 아무도 청구하지 않은 원문도 다음 요청의 후보가 된다.
2. **꼬리표는 원문 쪽 말로, 칸과 두 높이로 쓴다.** 구체 높이("SVN 저장소 주소를 넣고 커밋 이력을 Excel로 내보낸다")와 한 단계 위 높이("도구가 만든 기록을 그 도구가 없는 PC에서 볼 흔한 독립 파일로 내보낸다")를 함께 둔다. 요청도 접수 때 같은 칸으로 나눈다. 서랍은 칸끼리 맞추고, 두 칸 이상과 서로 다른 내용어 둘 이상이 맞을 때만 후보로 올린다. 이 규칙이 장면 2를 가능하게 하고, 동시에 R1의 Toyota처럼 기능어로 오른 우연을 막는다(1.6절, [02-landscape.md 2.1절](02-landscape.md#21-toyota-4위는-우연인가-기제인가)).
3. **판단은 프로젝트에 남고 원문 관측만 흐른다.** EVAL-X1 T3에서 다른 프로젝트가 "서비스가 문을 닫아도 북마크가 우리 서버에 남아야 한다"고 물으면, 서랍은 Pocket이라는 이름이 아니라 OAI-PMH 관측의 `breaks_when`·`input`·`output`·`summary` 칸으로 원리를 다시 찾는다. 새 프로젝트는 앞 프로젝트의 쪽지를 0건 보고, 관문을 자기 맥락에서 다시 통과시킨다(b, [05-cases.md 3.6절](05-cases.md#36-t3-몇-달-뒤-다른-질문)).

### 1.4 두 경우를 사용자에게 열어 보이는 방식

| 경우 | 공통 사례 | 사용자가 보는 "어디서" | "왜" | 원문으로 들어가는 길 |
| --- | --- | --- | --- | --- |
| 기존 도구로 기능 하나를 생략한다 | R1 | "투입·완료 신호를 따로 만들 필요가 없습니다. 크기 상한 8인 대기열에 일꾼 4개를 고정해 붙이고, 입력이 끝나면 대기열을 닫습니다" | 조건 ID마다 이유(대기 8·처리 중 4는 H1, producer가 put에서 기다리고 작업 객체 4개뿐은 H2, get으로 자리가 날 때만 재개는 H3), 근거 수준("이 판에서 실행해 값을 확인했다"), 함께 필요한 것("[필수] 일꾼 작업을 정확히 4개 만든다") | 첫 링크가 사용자 판의 고정 줄이다(`cpython/blob/v3.13.18/Lib/asyncio/queues.py#L36-L38`). 고르지 않은 근접 대안 넷이 갈린 조건과 함께 접힌 목록에 있다 |
| 다른 분야의 실패 복구 방식이 설계를 바꾼다 | EVAL-X1 | "다른 서비스의 기록을 삭제까지 포함해 변경분만 받아 우리 쪽 사본을 늘 맞춰 둔다(학술 기록 수확 규약)" | 빌릴 것(마지막 수확 시각부터 양 끝 포함 증분 수확, 삭제 기록), 대상에서 다시 확인할 것(변경 이후 목록과 삭제 신호, 호출 한도, 이어읽기 표지 만료), 깨지는 입력(종료 공지 뒤 내보내기가 닫힘. 공지 뒤 일괄 내보내기는 그 창 안에 끝나야만 R2가 성립한다) | OAI-PMH 2.0 §2.5.1·§2.7.1. 이 자리는 Pocket 관측을 대조로만 인용하므로, Pocket이 다섯 번 바뀌어도 이 자리에는 알림이 0건이다 |

두 경우 모두 "이 판에서 무엇을 확인했는가"를 근거 수준 여섯 단계 가운데 하나의 고정 문장으로 적는다([04-architecture.md 3.4절](04-architecture.md#34-근거-수준-사다리)). 원리 자리는 결코 "검증됨"이 되지 않는다. 관문 셋(역할 대응, 원문 절에서 인용한 지킬 성질, 동종 기준선과 예측이 갈리는 깨지는 입력)을 넘지 못하면 자리를 받지 못한다. 대상 1차 문서가 이미 같은 관계를 말할 때도 마찬가지다.

### 1.5 가장 강한 경쟁안이 이기는 때

가장 강한 경쟁안은 **S**다. P(이 제품)의 공개 관측에서 주소·판·절 위치·짧은 설명 한 줄만 남긴 목록, 전문 검색, 같은 절·판의 실행 영수증으로 이루어진다. 꼬리표, 대비, 쪽지, 변화 감시, 원리 관문은 없다. 같은 기억을 더 단순하게 둔 안이다. G(모델과 웹 검색만)보다 강하다([sections/request_utility.md 6절](sections/request_utility.md)).

S가 이기거나 비기는 경우는 다음과 같다.

- **요청이 제품·라이브러리 이름을 담고 필요한 것이 그 절 하나일 때.** R1이 그렇다. `Queue maxsize`로 S를 찾으면 같은 절과 같은 판 영수증이 나온다. 연구 기록에서 결정 당시 표적 해법을 이미 안 경우가 21/24였다(a, [022][r022]). 이런 요청은 흔하다.
- **같은 언어·같은 분야의 질의일 때.** 목적·관계 질의는 일반 질의에 주 지표 0승 12무 0패였고(양쪽 모두 새 완결 0), 새 부품 보조 지표에서는 일반 질의가 2승 10무였다(a, [025][r025]).
- **판이 안정적이고 지난 답을 다시 열 일이 없을 때.** 변화 감시와 쪽지는 비용만 남는다. 152에서 안정 인기 자료 159질의는 모든 정책에서 맞았다(b, [152][r152]).
- **EVAL-X1 T0은 비긴다.** 검증된 직접 도구가 없어 둘 다 "확인할 후보"와 다음 확인을 낸다. P는 T1부터 앞선다. 같은 도움말 주소가 200인 동안 개정 300072가 저장 종료를 적었고, P는 그 항목이 T0 자리의 감시 키에 닿아 표시하지만 S는 다음 요청 전까지 모른다.

P가 이길 수 있는 곳은 장면 2 같은 요청이다. 한국어 질의로 영어 설명을 찾으면 R@10이 .234에서 .124로 떨어졌다(b, [012][r012]). 이름 없이 칸으로 찾으려면 두 높이·두 언어 꼬리표가 필요하다. **이 우위는 측정되지 않았다(c).** 그래서 v1은 S를 제품 안의 기준선으로 둔다. 모든 요청에서 서랍만 찾은 후보와 새 검색만 찾은 후보를 따로 기록하고(`path_log`), 서랍만 찾은 적격 후보가 두 분기 연속 0이면 꼬리표·대비 작성을 멈추고 S의 표현으로 줄인다([04-architecture.md 7절](04-architecture.md#7-운영-지표와-줄이는-규칙)).

### 1.6 기존 설계에서 가장 크게 바뀐 것

기존 설계는 판단을 기록하는 뼈대가 옳았다. 요청판 고정과 원문 범위 검증, 요청판에 묶인 판단, 비유를 지지로 세지 않는 판정기, 지난 답의 바이트 단위 재생은 고정 입력에서 약속대로 동작했다(b, [PR #7 ASSESSMENT 2절][pr7a]). 이 뼈대는 그대로 가져왔다. 바뀐 것은 셋이고, 가장 큰 것은 첫째다.

1. **한 행이던 근거와 판단을 둘로 나눴다.** 기존 `claim` 행은 근거 조각과 요청별 판단을 함께 가졌다([schema L47–56][gclaim]). 그래서 다른 요청은 같은 원문을 다시 판독해야 했고, 판단을 다른 프로젝트와 나눌 방법도 없었다. v1은 공개 관측(판, 위치, 관측 시각, 인용 지문, 실패 종류)과 비공개 판정 쪽지(요청판, 조건, 관측 ID, 판정, 근거 수준, 요건 사실)를 나눈다. 147에서 판 단위 관측은 현재 답을 모두 맞혔고, 원문 읽기 바이트가 37,163,112에서 12,387,704로 줄었다. 과거 답 112건은 전달 기록까지 둔 쪽만 재생했다(b, [147][r147]). 이 분리가 공개 자료 공유와 비공개 맥락 경계를 동시에 정한다. 구성요소 삭제 시험에서 판단 분리를 끄면 앞 프로젝트의 판단 1건이 다른 프로젝트로 흘렀다([05-cases.md 5절](05-cases.md#5-구성요소-삭제-시험)).
2. **후보를 찾는 단계를 다시 만들었다.** 기존 관계 추론은 정규식 셋이라 R1과 EVAL-X1에서 모두 0건이었고, 어휘 순위는 기능어와 숫자를 한 단어로 셌다(b, [PR #7 p8·p9][p8]). v1은 칸으로 나눈 꼬리표, 두 칸·서로 다른 내용어 둘의 후보 자격, 네 갈래 새 검색, 서랍만 찾음·새 검색만 찾음의 기록을 둔다. 2단계 전문 색인은 빼도 다섯 사례의 답이 같아서 뺐다(b, [PR #7 p7][p7]).
3. **시간을 넣었다.** 기존 스키마의 시각은 `decision_run.created_at` 하나라 "그날 알 수 있던 것"을 물을 수 없었다. v1은 관측 시각, 발행 시각, 효력 시각, 알게 된 시각을 나눠 두고, 변경 채널을 외부 ID 집합의 차분으로 읽으며, 공지 기한을 감시 값으로 둔다. EVAL-X1에서 "10월 9일에 알던 기한"은 11월 6일, "10월 10일에 알던 기한"은 11월 12일로 답한다(b).

R1 하나로 차이를 보이면 이렇다. 기존안은 관계 0, 판독 0, 답 0이었고 기권 문구는 "표시 예산 안에서 후보 없음"이었다. v1은 해석 줄 하나와 직접 도구 자리 하나를 내고, 접힌 목록 7개(근접 대안 넷, 범위 밖 실패 시험 하나, 관문에서 접힌 원리 둘)를 이유와 함께 남긴다. 배포 런타임이 3.12로 바뀌면 같은 위치를 3.12.3 판에서 다시 열어(새 관측 6개) 끝 신호 부분만 바꾸고, 지난 답은 당시 문장 그대로 두고 알림 한 줄을 붙인다([05-cases.md 2절](05-cases.md#2-사례-a-r1-기존안과-새-구조)).

### 1.7 주소만으로 충분할 때와 쓸모를 잃을 때

판단 규칙은 하나다. **답이 그 주소의 "어느 판, 어느 위치, 어떤 관계"에 기대면 주소 밖의 기록이 필요하다. 그렇지 않으면 주소와 확인 시각만 남긴다.**

| 주소만으로 충분하다 | 주소만 남기면 처음 발견한 쓸모를 잃는다 |
| --- | --- |
| 안정된 고정판 절을 정해진 목적으로 다시 연다. 고정 절 넷의 두 시점·네 조회가 주소 하나로 32/32 보존됐다(b, [150][r150]) | 쓸모가 긴 글 속 한 줄이다. ii-svn-log의 쓸모는 "SVN 없는 PC에서 열람·공유" 한 줄이고 제목은 "ii-svn-log v1.00"뿐이다(a, [149 L56][s149]). 이 줄을 칸 꼬리표로 남기지 않으면 장면 2가 성립하지 않는다 |
| 북마크와 보관. 147의 세 저장안 모두 링크 보관에는 취득이 0이었다(b, [147][r147]) | 기능이 판에 묶인다. `Queue.shutdown`은 3.13에만 있다(b, 이번 영수증). Git 2.23 전에는 restore가 없다(a, [256][r256]) |
| 원문이 스스로 답을 가리킨다. API 페이지 안의 예제는 추가 주소 0개였다(b, [257][r257]) | 한 주소가 여러 판·대상을 대표한다. 마지막 값을 이어 쓰자 96건 중 40건을 잘못 승인했다(b, [147][r147]) |
| | 같은 주소의 본문이 바뀐다. Pocket 도움말은 기능이 사라진 뒤에도 200이었다(b, [152][r152]) |
| | 다른 분야로 옮기는 원리. 주소에는 대응 관계가 없다. R1의 Toyota 설명과 요청은 내용어를 하나도 공유하지 않았다(b, [PR #7 5.1절][pr7a]) |

### 1.8 개인 맥락과 판단을 얼마나 나누나

| 공개(프로젝트 사이 재사용) | 비공개(프로젝트 안) |
| --- | --- |
| 위치, 별칭과 취소, 판, 관측(인용 지문, 실패 종류, 뒤집을 위치), 실행 영수증, 다시 본 기록, 꼬리표(원문 쪽 말만), 대비(같은 판에서 두 관측이 갈리는 조건), 대체, 변경 채널과 항목, 감시 키, 재확인 작업 | 요청판 원문, 선택 위치, 조건 수치(R1의 8과 4. **재검토:** v1 실행 예제는 이 수치를 공개 영수증 입력과 대비 행에 그대로 담았다. 07 M7c·D6), 맥락 사실, 봉인, 칸별 필요 문장, 해석과 질문, 탐색 기록(일치 토큰·탈락 사유), 판정 쪽지, 답 자리와 문장, 사용 쪽지, 알림, 노출 |

나누지 않는 이유는 둘이다. 판단은 요청의 조건과 요건 사실에 기댄다. 같은 원문이라도 다른 프로젝트에서는 맞지 않는다. 그리고 판단을 공용 관측에 붙이면 프로젝트의 의도가 공개 쪽으로 샌다. 147에서 주소로만 근거를 이어 쓴 구성은 다른 키·절 근거 72건 중 24건이 다른 프로젝트가 취득한 것이었다(b, [147][r147]). 엔진은 공개 꼬리표에 그 요청에만 나온 내용어가 둘 이상 들어가면 쓰기를 거절한다(`PrivacyError`, [db/test_ledger.py](db/test_ledger.py)). 요청 때문에 새로 읽은 공개 원문도 관측은 공개로 남기되, 누가 왜 읽었는지는 남기지 않는다.

### 1.9 주요 결정과 근거

| 결정 | 근거(고정 커밋·파일) | 구현 위치 |
| --- | --- | --- |
| 관측과 판단을 나눈다 | 147 B·C [`30afd115` HANDOFF][r147h], 기존 [`claim` 행][gclaim] | `observation`, `{p}.slip` |
| 재사용은 같은 판·같은 위치만, URL의 마지막 값은 쓰지 않는다 | 147 A-url 40/96 [`30afd115`][r147h] | `Ledger.reusable`, `carry_slips` |
| 전역 병합을 하지 않는다. 별칭과 취소만 둔다 | 150 A 7·B 9·C 15/16 [`ff2c1fc8` RESULT][r150], 023 tree-sitter [`a9178ca9`][r023] | `locator_alias`, `locator_alias_cancel`, `Ledger.resolve` |
| 기능어·숫자만 겹친 적중은 우연, 서랍 후보는 두 칸·내용어 둘 | LINK_STUDY L43 [`fc68f0d1`][ls43], 012 재계산 [sections/rj](sections/rj/) | `Ledger.search_drawer` |
| 원리 관문 셋, 대상 1차 문서 우선 | 258 [`8106a22f`][r258], LOD API [`beab9e84`][lodapi], 033 무힌트 144쌍 중 부분 지지 1·전체 설계 지지 0 [`d6ac67ae`][m033] | `Ledger.gate` |
| 범위 밖 실패 시험은 자리에 두지 않는다 | R1 범위 밖 "장애 복구" [012 P03.w][q012] | `cases.case_a` 접힌 목록 |
| 묻기 앞에 요청판 재독과 공통 행동 | 026 물을 값이 이미 요청판에 있음 8/24 [`c6eff012`][r026], 144 C4·Y2 [`92833407`][r144] | `Ledger.decide` |
| 봉인이 노출보다 먼저 | 022 21/24 [`df80ec24`][r022], 249 동결 뒤 질문 [`a61cee2b`][p249] | `Ledger.show` |
| 채널은 ID 집합 차분, 표시일 창 없음 | 152 CF-2026-01 [`ba038a0a` RESULT][r152] | `Ledger.poll` |
| 공지 기한에 직접 읽고 기한 경과만으로 무효로 하지 않는다 | 152 잘못된 제외 S 27시간·P 279시간 [sections/discovery_ops.md 6절](sections/discovery_ops.md) | `Ledger.due` |
| 감시가 건전하면 재사용 관측을 다시 열지 않는다 | 152 O 336·309/364 대 S 340·343/364 [`ba038a0a`][r152] | `Ledger.reuse_gate` |
| 철회는 사용 쪽지를 따라 인용한 자리에만, 대조 인용은 제외 | EVAL-X1 T2-b [`afa3c285`][sealed] | `Ledger.propagate`, `usage.part` |
| 근거 수준은 고정 문장 여섯 단계 | 257 깊이 2에서 결과 0/5 [`ff1eb5da`][r257], 058 설명을 덧붙이자 틀린 권고 수락 123/205→152/205 [`fefeb214`][r058] | `LADDER_TEXT` |
| 2단계 전문 색인을 뺀다 | PR #7 p7 [`8fbc885d`][p7] | 단일 `tag_fts` |
| 범위 붙은 같음 그래프는 v1에서 뺀다 | 두 사례 추적 모두 쓰지 않음, 150 C의 정확도는 작업자 판독 [`ff2c1fc8`][r150] | 추가 조건은 [04-architecture.md 6.3절](04-architecture.md#63-오병합과-분리) |

[gallim]: https://github.com/laadkke-arch/agentflow-open/tree/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim
[pr6]: https://github.com/laadkke-arch/agentflow-open/blob/8f674773863f56141bb82bafe364397b6f1d82f0/docs/design-threads/independent.md
[pr7]: https://github.com/laadkke-arch/agentflow-open/tree/8fbc885d6a52cd43949c1caf633a39182de2613d/docs/workstreams/design/gallim-review
[pr7a]: https://github.com/laadkke-arch/agentflow-open/blob/8fbc885d6a52cd43949c1caf633a39182de2613d/docs/workstreams/design/gallim-review/ASSESSMENT.md
[pr8]: https://github.com/laadkke-arch/agentflow-open/blob/72e8aee231313f84c5f148a4b6694401d8371b50/docs/workstreams/design/alt-starts/README.md
[p8]: https://github.com/laadkke-arch/agentflow-open/blob/8fbc885d6a52cd43949c1caf633a39182de2613d/docs/workstreams/design/gallim-review/probes/out/p8_r1.txt
[p7]: https://github.com/laadkke-arch/agentflow-open/blob/8fbc885d6a52cd43949c1caf633a39182de2613d/docs/workstreams/design/gallim-review/probes/out/p7_delete_stage2.txt
[gclaim]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/schema.sql#L47-L56
[ls43]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/LINK_STUDY.md#L43
[q012]: https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/queries/queries.jsonl#L31
[r012]: https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/RESULTS.md#L74
[r022]: https://github.com/laadkke-arch/agentflow-open/blob/df80ec2406042a73c2114e316894173f66309cda/docs/workstreams/research/AF-RES-022/evidence/statistics.json
[r023]: https://github.com/laadkke-arch/agentflow-open/blob/a9178ca95979564fd8801559d90d15db4ddac91b/docs/workstreams/research/AF-RES-023/HANDOFF.md
[r025]: https://github.com/laadkke-arch/agentflow-open/blob/cf27e148b96bf3c5a3dc8a2a926db4abcf63f146/docs/workstreams/research/AF-RES-025/RESULT.md#L83
[r026]: https://github.com/laadkke-arch/agentflow-open/blob/c6eff012a74451e9882d8d43b6a6e510b4d15225/docs/workstreams/research/AF-RES-026/HANDOFF.md#L42
[m033]: https://github.com/laadkke-arch/agentflow-open/blob/d6ac67ae199b8205772587bcf7d583559aff44b4/docs/workstreams/research/AF-RES-033/maps.csv
[r058]: https://github.com/laadkke-arch/agentflow-open/blob/fefeb2146c7f63e49d0578f78989be49acd63291/docs/workstreams/research/AF-RES-058/HANDOFF.md#L40-L48
[r144]: https://github.com/laadkke-arch/agentflow-open/blob/92833407f665a6e28e4292491c261b7e0725c69c/docs/workstreams/research/AF-RES-144/decisions.csv
[r147]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/RESULT.md
[r147h]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/HANDOFF.md
[s149]: https://github.com/laadkke-arch/agentflow-open/blob/bc19a446b02049b8c7569ca5de9da8afce255461/docs/workstreams/research/AF-RES-149/sources.jsonl#L56
[r150]: https://github.com/laadkke-arch/agentflow-open/blob/ff2c1fc8786ba70a1432f1089f8f81288e43a61d/docs/workstreams/research/AF-RES-150/RESULT.md
[r152]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/RESULT.md
[p249]: https://github.com/laadkke-arch/agentflow-open/blob/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/protocol.md
[r256]: https://github.com/laadkke-arch/agentflow-open/blob/17a7d6f69d6516929005f09239543b1ac54968c1/docs/workstreams/research/AF-RES-256/RESULT.md
[r257]: https://github.com/laadkke-arch/agentflow-open/blob/ff1eb5dad4294f27ec368698f544f03519d7fb12/docs/workstreams/research/AF-RES-257/RESULT.md
[r258]: https://github.com/laadkke-arch/agentflow-open/blob/8106a22f4122c798edb52ed9825b06e1040a7ffc/docs/workstreams/research/AF-RES-258/RESULT.md
[lodapi]: https://github.com/mrdoob/three.js/blob/beab9e845f9e5ae11d648f55b24a0e910b56a85a/docs/api/en/objects/LOD.html#L60-L80
[sealed]: https://github.com/laadkke-arch/agentflow-open/blob/afa3c285c66a1c5227732cda3e79ab579cd9eddf/docs/workstreams/design/gallim-review/SEALED_CASE.md
