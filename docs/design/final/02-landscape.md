# 02. 연구 지형과 다섯 판단 문제

근거 표시는 1장과 같다. (a) 문서 판독, (b) 고정 입력에서 코드로 확인, (c) 실제 사용자나 운영이 있어야 아는 것.

## 1. 무엇을 어디까지 읽었나

| 읽은 것 | 고정판 | 이 설계가 가져온 사실 |
| --- | --- | --- |
| 제품 브리프 | [`933a0f7d` RESEARCH_BRIEF.md][brief] | 사용자는 설계 전체나 한 부분과 그 목적을 준다. 가치는 비슷한 완제품, 적용할 부품, 빌려올 원리, 이미 있는 대안을 원문에 잇는 데 있다 |
| 통합 진행표 | [`933a0f7d`][dot0]·[`45896ef1`][dot1] `dot-control.json` | 253행. 요청 시점에 DONE 245·RUNNING 2·BLOCKED 6, 마감에 DONE 247·BLOCKED 6(018, 035, 149, 151, 242, 254). 247행 모두 `acceptance_evidence`가 빈 배열이라, 완료 여부와 독립 확인 수준은 각 인계에서 읽어야 한다(a). 장면 2의 ii-svn-log 근거는 BLOCKED(PARTIAL)인 149의 출처 원장 한 줄이다. 그래서 이 설계는 그 줄을 (a)로만 쓴다 |
| 49차 검토 | [`c8f4b5f1` REVIEW-49][r49] | 설계자가 정할 일 다섯(무엇을 한 번 더 물을까, 무엇을 새 적격 링크로 셀까, 타 분야 원리가 무엇을 더 예측했나, 하나·대안·필수 조합 중 무엇을 줄까, 어디까지 저장하면 과거와 현재를 복원할까)과 각 질문의 원장 수치 |
| AF-RES-256~267 | 진행표 밖의 결과 브랜치. 각 고정판은 [landscape/](landscape/)에 있다 | 256 판 조건과 묻기 이득, 257 읽기 깊이, 258 온도 조절기→LOD, 259 소속 라벨, 260 같은 경로의 다른 원본, 261 층별 재확인, 262 정적 판정, 263 BagIt 충돌, 264 판에 묶인 기능, 265 GLB 단독 표시, 266 파일 단위 철회, 267 고정 벡터 채점 |
| 원장 아래까지 | 147·150·152·012는 원 CSV와 재생 스크립트까지 다시 돌렸다(b). 나머지는 인계와 결과 판독(a) | 아래 2절의 수치 |
| 기존 설계 | [`fc68f0d1` gallim][g] 문서 9, 코드 8, 시험 6 | 3절 |
| 병행 설계 | PR #6 [`8f674773`][pr6], PR #7 [`8fbc885d`][pr7], PR #8 [`72e8aee2`][pr8] | [03-concepts.md](03-concepts.md) |

### 1.1 부문별 지형

다섯 부문 정리가 [landscape/](landscape/)에 있다. 각 문서는 확정·정정·열린 것, 근거 수준, 설계 함의, 뒤집거나 단순화하는 근거, 다른 부문에 주는 사실 순이다. 여기서는 설계를 움직인 것만 적는다.

| 부문 | 설계를 움직인 확정 사실 | 아직 열린 것 |
| --- | --- | --- |
| [요청과 답변](landscape/request.md) | 부분 질문이 흔하다. 011의 공개 질문 61건 중 33건(a). 목표를 좁힌 입력이 전체 입력보다 나았다. 012 K02.1 nDCG .365 대 .268(b). 물을 값이 이미 요청판에 있던 경우가 026에서 8/24였다(a) | 실제 사용자가 해석 줄을 읽고 고치는지(c, 0건) |
| [발견과 타 분야 원리](landscape/discovery.md) | 무힌트 타 분야 쌍의 지지는 033에서 144쌍 중 부분 1·전체 0(a). 258과 257은 대상 1차 문서가 이미 답을 담았다(a·b). 한국어 질의로 영어 설명을 찾으면 R@10이 .234에서 .124로 떨어졌다(b) | 타 분야 원리가 사람의 선택을 바꾸는지(c) |
| [식별·저장·판본](landscape/identity.md) | 147의 판 단위 관측과 전달 기록, 150의 범위 붙은 같음 15/16과 단일 주소 32/32(b) | 별칭을 누가 붙이고 얼마나 틀리는지(c) |
| [관리·운영](landscape/operations.md) | 152에서 기본 정책 하나가 모든 공급자를 이기지 못했다. 표시일 창이 늦은 편입을 놓쳤다(b) | 304 조건부 요청 비율, 헛된 재확인 비율(c) |
| [제품 효용 평가](landscape/evaluation.md) | 249는 설계만 있고 참가자 0명, 267은 채점기 재현만 있다(a·b) | P가 S보다 나은지 자체(c) |

## 2. 다섯 판단 문제의 답

다섯 문제 모두에서 판단을 뒤집거나 단순하게 만드는 근거를 먼저 찾았다. 결과는 이렇다. 둘은 단순해졌다(258, 257). 하나는 뒤집혔다(Toyota). 둘은 규칙 하나로 정리됐다(150·147, 152).

### 2.1 Toyota 4위는 우연인가 기제인가

**답: 우연이다. 영어 URL만의 4위와 설명을 붙인 조건의 1위 모두 그렇다.** v1은 이 우연을 구조 규칙으로 막고, 원리 후보는 다른 길로 들인다.

- **근거.** 012 고정판으로 다시 계산했다(b, [sections/rj/p03_rank.py](sections/rj/p03_rank.py)). 영어 URL만의 4위는 `and` 하나로 맞았다. URL+한 줄과 URL+한 줄+용도의 1위는 and·by·in·is·it·the·time·when으로 맞았다. 기능어를 빼면 Toyota는 8위·23위(`time`만 남음)로 내려가고, Queue가 1·2위로 오른다. 남은 `time`은 요청의 관용구 "at a time", "ahead of time"에만 있다. Toyota의 작동 설명(인출·보충)과 요청의 필요(대기·용량 회복)는 내용어를 하나도 공유하지 않는다([sections/retrieval_judgment.md 3.1절](sections/retrieval_judgment.md)). PR #7도 같은 결론이다. 영어 URL 조건의 상위 10위 256쌍 중 167쌍이 기능어만 겹쳤다([ASSESSMENT 5.1절][pr7a]).
- **뒤집힌 것.** "URL만으로 다른 분야 원리를 찾는다"는 해석은 성립하지 않는다. 기능어를 빼면 영어 URL만의 원리 R@10은 .174에서 .027로 떨어진다(b). 원리를 찾던 재현율의 대부분이 우연이었다.
- **v1 규칙.** 기능어와 숫자만 겹친 적중은 우연 적중으로 표시하고 후보 근거로 세지 않는다. 서랍 후보는 서로 다른 내용어 둘 이상과 두 칸 이상이 맞아야 한다. 기능어를 질의에서 지우지는 않는다. 36질의 재현율이 지우면 오르기도 내리기도 했다(.204→.178, .270→.344, b). v1의 서랍에서 Toyota는 기능어를 셀 때 3위, 내용어만 셀 때 `time` 하나로 22위이고 자격이 없다(b, [db/out/cases.json](db/out/cases.json) `drawer_audit_toyota`, `drawer_content_toyota`).
- **분야명을 모르는 사람의 길.** 낱말 일치로는 닿지 않는다. v1은 두 길을 둔다. ① 새 검색의 "분야 이름 없는 관계 문장" 갈래와 "분야 추정" 갈래. R1에서 Toyota와 Reactive Streams는 분야 추정 갈래에서만 나왔다(b, `path_log`). ② 서랍의 한 단계 위 꼬리표와 접수가 같은 높이로 쓴 필요 문장을 칸끼리 맞추는 길. 두 길 모두 후보는 원리 관문에만 오른다. R1에서는 관문이 닫힌다(2.5절). 그래서 이 길이 막혀도 R1은 잃는 것이 없다. 회수율은 측정되지 않았다(c).

### 2.2 258 온도 조절기: 무엇을 빌리고 무엇을 대상에서 정하나

**답: 빌리는 것은 모양뿐이다. 임계 둘, 직전 상태 1비트, 사이 구간에서 직전 상태를 유지하는 성질이다. 등호와 단위와 초기 상태는 대상에서 정한다. 그리고 대상 1차 문서를 먼저 본다.**

- **근거.** 온도 제어를 참조한 설명 B는 P4(120→90→95)를 F→N→N으로 예측했다. three r170 실행 결과는 F→F→F다(b, [PR #7 lod_runtime.json][pr7lod]). 원인은 하한 등호다. 원분야 안에서도 ESPHome thermostat는 `>=`·`<=`, bang_bang은 `>`·`<`를 쓴다([258 RESULT][r258]). 공여 분야 안에서도 갈리는 규칙은 옮기지 않는다.
- **단순화.** three.js LOD API 문서가 이미 `hysteresis`를 경계에서 깜박임을 막는 임계로 적는다([LOD.html L60–80][lodapi]). 258도 대상 문서 대비 타 분야 링크의 독립 추가 가치를 미확인으로 남겼다. 그래서 v1의 관문은 대상 1차 문서가 같은 관계를 이미 말하면 닫힌다.
- **v1 규칙.** `Ledger.gate`가 ① 역할 대응, ② 원문 절에서 인용한 지킬 성질, ③ 동종 기준선과 예측이 갈리는 깨지는 입력을 요구한다. 대상 문서가 이미 말하면 `target_doc_says_it=True`로 닫는다(b, `test_gate_closes_when_target_doc_already_says_it`). 원리 자리는 빌릴 것, 대상에서 다시 확인할 것, 깨지는 입력, 보류 조건을 따로 적는다. 258이라면 첫 링크는 `LOD.js`의 판정 줄이고, 온도 조절기 원문은 "같은 모양의 선례, 등호는 원분야 안에서도 갈림"으로 둘째 자리에 간다.

### 2.3 150·147 같음: 언제 합치고 무엇을 저장하나

**답: 전역 병합은 하지 않는다. 관측의 키는 (주소 원문 문자열, 판, 위치)이고, 별칭과 그 취소만 둔다. 저장은 공개 관측과 비공개 전달 기록으로 나눈다. 범위 붙은 같음 그래프는 v1에서 뺀다.**

- **근거.** 150에서 판단과 근거까지 맞은 것은 URL별 A 7/16(오분리 6), 공통 작업 키 B 9/16(오병합 6), 범위 붙은 방향 관계 C 15/16이었다. 한 고정 절을 한 목적으로 읽을 때는 주소 하나로 32/32를 유지했다([150 RESULT L43·L51][r150], b). 147에서 판 단위 관측(B)과 전달 기록(C)은 현재 답을 모두 맞혔다. URL의 마지막 값을 이어 쓴 A-url은 96건 중 40건을 잘못 승인했다. 과거 답 112건은 C만 재생했다. 원문 읽기는 B가 37,163,112 B에서 12,387,704 B로 줄였다([147 RESULT L35][r147], b).
- **단순화.** 150 C의 15/16은 작업자가 손으로 판독한 결과다. 두 사례 추적(R1, EVAL-X1)과 장면 2에서 범위 붙은 같음이 답을 바꾼 일이 없었다. 그래서 v1은 그 그래프 대신 다음 셋으로 충분하다고 판단했다. ① 판이 다르면 다른 관측이다. ② 주소 이동은 증거 관측을 단 별칭이다. ③ 잘못 붙인 별칭은 취소 행으로 끊는다(`test_cancelled_alias_is_not_followed`).
- **다시 넣는 조건.** 같은 대상을 가리키는 두 관측이 같은 답의 서로 다른 자리에 나오는 일이 운영에서 분기 1건 이상 생기면 그래프를 넣는다([04-architecture.md 6.3절](04-architecture.md#63-오병합과-분리)).
- **147이 정한 저장 경계.** 현재 답에는 B(공개 관측)만으로 충분하다. C의 전달 기록은 과거 답 재생에만 필요하다. v1에서 B는 `observation`이고, C는 프로젝트의 `answer_run`·`slot`·`usage`다. 이 경계가 그대로 공개와 비공개의 경계가 된다(1장 1.8절).

### 2.4 152 신선도, 희귀 발견, 요청 지연

**답: 세 목표를 한 정책으로 사지 않는다. 시계 셋이 각자 하나씩 산다. 희귀 발견은 배경 시계의 ID 차분이, 신선도는 후속 시계의 채널 항목과 공지 기한이, 요청 지연은 재사용 관문이 산다.**

- **근거.** 152 유보 기간에 새 항목 15건 중 S·F는 14건, P는 13건, O는 10~14건을 찾았다. 높은 예산 주류의 발견 중앙값은 P 27시간, S 57시간이었다. 낮은 예산 희소에서는 P 92.1시간, S 27시간으로 뒤집혔다. P가 놓친 CF-2026-01은 표시일이 1월 1일이고 편입이 1월 30일이라 30일 표시일 창에서 빠졌다([152 RESULT L112–116][r152], b). 같은 예산에서 늘 요청 때 읽는 O는 보류 때문에 높은 예산 336·309/364를, 캐시와 채널을 쓴 S는 340·343/364를 맞혔다(b).
- **뒤집힌 것.** "기본 정책 하나"는 없다. 순위가 공급자와 수요층에 따라 바뀐다. F의 희소 전용 자리는 S와 발견 수가 같아 이득이 보이지 않는다. v1은 F를 채택하지 않는다.
- **v1 규칙.** 공급자가 무엇을 주는지로 정한다. 변경 피드가 있으면 그 ID 집합의 차분을 읽는다(표시일로 거르지 않는다). 작은 전체 목록이나 과거판 직접 조회가 있으면 요청 때 읽는다. 둘 다 없으면 예산을 정한 순환이다. 관측마다 감시 키(같은 주소 / 공급자 두 층)와 공지 기한을 단다. 기한 24시간 전과 기한 시각에 직접 읽고, 기한이 지났다는 것만으로 무효로 하지 않는다. 기한이 지나면 캐시에서 빼는 152 규칙은 Pocket 기한 연장 때 잘못된 제외를 S 27시간, P 279시간 냈다(b, [sections/discovery_ops.md 6절](sections/discovery_ops.md)). 감시가 건전하다는 조건이 모두 참이면 재사용 관측을 다시 열지 않는다(`Ledger.reuse_gate`). 보증은 "장부가 받은 변화 뒤에는 재사용하지 않는다"이고, 받기 전 지연은 채널 주기로 묶인다(구현 노트 I39·I40, 감시 범위 조건 (4') 추가).
- **남은 것.** 시계별 예산 비율은 152 S의 잰 배분(요청 횟수로 배경 66%·후속 3%·요청 31%)에서 시작하지만, 제품 요청 분포에서는 재지 않았다(c).

### 2.5 257 L2와 L3: 얼마나 깊이 읽나

**답: 목표 근거 수준을 먼저 정하고, 그 수준에 맞는 곳만 읽는다. 목표가 "결과 값을 본다"(L3)이면 예제 목록을 읽지 않는다. API 절을 보고, 없으면 작게 실행해 L4로 간다.**

- **근거.** 세 목표를 합친 갤러리 링크는 깊이 2·3·끝에서 5·7·13개였다. 공개 결과에서 요청한 값이 보인 링크(L3)는 0/5·0/7·0/13이었다. 소스에서 그 값을 만들고 쓰는 줄(L2)은 끝까지 가서 1/13이었다. API 페이지의 Examples 절은 새 주소 없이 두 반환값을 바로 보였다([257 RESULT L46][r257], a·b).
- **단순화.** 갤러리 끝까지 읽어도 깊이 2보다 L3이 +0, L2가 +1이었다. 깊이를 키우는 것보다 목표 수준을 정하는 것이 더 많이 줄인다.
- **v1 규칙.** 근거 수준 사다리를 고정 문장 여섯 단계로 둔다(L0 목록에 있음, L1 소개·언급, L2 이 판의 원문 줄에서 방법, L3 공개 산출물에서 값, L4 이 판에서 실행해 값, L5 사용자 맥락에서 확인해야 함). 각 자리에 그 문장을 그대로 붙이고 설명으로 부풀리지 않는다. 058에서 설명을 덧붙이자 맞는 권고와 함께 틀린 권고의 수락도 123/205에서 152/205로 늘었다(a, [058][r058]). 목표가 L2인데 API 절로 채워지지 않을 때만 목록을 깊이 2까지 읽는다. 그 너머는 목록 순서가 아니라 그 값을 받아 쓰는 줄을 따라간다. 멈추면 도달 깊이와 첫 충족 순위를 적는다. 못 찾았으면 "깊이 k까지 없음"을 적는다.
- **1번 자리의 하한.** 1번 자리는 모든 필수 조건을 L2 이상으로 채워야 한다. R1의 직접 자리는 L4다(입력 40개로 실행, 영수증 [db/receipts/](db/receipts/)).

## 3. 기존 설계: 약속, 확인, 미확인

기존 설계 [`fc68f0d1`][g]를 세 겹으로 나눴다. PR #7이 고정판을 꺼내 탐침 10개를 돌렸다([ASSESSMENT 2·3절][pr7a]). 이 설계는 그 결과를 원장과 다시 대조했다.

| 동작 | 문서가 약속한 것 | 코드가 고정 입력에서 확인한 것 | 실제 사용자·운영이 있어야 아는 것 |
| --- | --- | --- | --- |
| 요청 고정 | 원문·선택·조건을 한 번에 쓰고 범위가 어긋나면 거절 ([ARCH L46][g-arch-46]) | 확인. 같은 판의 다른 내용 재전송을 거절한다 | 입력 쪽이 원문 범위를 실제로 붙여 주는지 |
| 판단 범위 | 판단은 요청판에 묶이고 다른 프로젝트로 새지 않는다 ([ARCH L24][g-arch-24]) | 확인. 판단 행이 요청판을 외래 키로 가진다 | 없음 |
| 판정 | 직접 근거만 지지·반증, 비유는 제외 ([ARCH L49][g-arch-49]) | 확인. 비직접 근거는 이유를 남기고 무시한다 | 보류가 많을 때 사용자가 다음 확인을 하는지 |
| 지난 답 재생 | "지난번 무슨 근거로 답했나" ([ARCH L25][g-arch-25]) | 확인. 바이트 단위로 같고 새 판이 생기면 낡음을 표시한다 | 없음 |
| 재검토 작업 | 새 판이 생기면 관련 판단에 작업 ([ARCH L51][g-arch-51]) | 일부. 작업은 생기지만 새 판단을 내도 닫히지 않는다 ([roundtrip L136][g-rt-136]) | 누가 언제 처리하나 |
| 다른 이름으로 재발견 | 관계로 찾으면 분야명이 달라도 후보 ([ARCH L27][g-arch-27]) | 일부. 정규식이 맞는 한국어 표현에서만. 같은 뜻 영어 요청은 0건 | 관계 문장을 누가 붙이나 |
| 관측과 판단 분리 | 관측 종류·적용판·판단 시각을 따로 ([SEARCH L26][g-search-26]) | 아님. 한 행이 근거 조각과 요청별 판단을 함께 가진다 ([schema L47–56][g-schema-claim]) | 없음 |
| 그날 알던 것 | 당시 알 수 있던 것과 나중에 복원한 것을 구분 ([EVAL L13][g-eval-13]) | 아님. 시각 칸은 하나 ([schema L59–65][g-schema-run]) | 발행 시각을 모르는 원문의 비율 |
| 동일성 | 함부로 접지 않고 병합 별칭을 사실로 쓰지 않음 ([ARCH L22][g-arch-22]) | 접지 않는 쪽만 확인. 합치기·나누기·철회가 없다 | 없음 |
| HTTP와 유효한 이유 | 분리 ([ARCH L57][g-arch-57]) | 아님. 수집 코드가 없다 | 200인 채 기능이 사라지는 비율 |
| 읽기 예산 | URL 6개·문서당 500단어·1 MiB ([SEARCH L76–80][g-search-76]) | 아님. 코드의 예산은 화면에 보일 후보 수 ([retrieval L171–173][g-ret-173]) | 기본 예산 |
| 기권 문구 | 어디서 탈락했는지 복구 ([SEARCH L28][g-search-28]) | 아님. 언제나 "표시 예산 안에서 후보 없음" 한 문장 ([roundtrip L166][g-rt-166]) | 없음 |
| R1 | 관계 질의를 여러 용어로 만든다 ([ARCH L40][g-arch-40]) | 관계 0, 판독 0, 답 0. URL 조건 1·2위가 `13`·`3`·`python`으로 맞음 ([p8][p8]) | 없음 |

## 4. 무엇을 가져오고 무엇을 버렸나

PR #7의 20행 후보표([ASSESSMENT 7절][pr7a])에 최종 판정을 붙였다. "다른 곳에서 달라지는 동작"은 이 결정 때문에 다른 부문의 동작이 어떻게 바뀌는지 하나씩 적은 것이다.

| # | 요소 | 판정 | 근거 | 다른 곳에서 달라지는 동작 |
| --- | --- | --- | --- | --- |
| 1 | 요청판 고정과 원문 범위 검증 | 채택 | 테스트, [ARCH L46][g-arch-46] | 지난 답 재생과 사실 변경 비교가 판 단위로 이뤄진다. R1 3.12 전환은 요청판 2다 |
| 2 | 판단을 요청판에 묶기 | 채택(확장: 비공개 쪽지로 이동) | [schema L47–56][g-schema-claim] | 다른 프로젝트는 판단을 물려받지 않는다. EVAL-X1 T3의 물려받은 판단 0건 |
| 3 | 보수적 판정기 | 채택 | [demo L29–83][g-demo-rej] | 원리는 결코 "검증됨"이 되지 않으므로 답에 "시험할 원리" 자리가 따로 있다 |
| 4 | 지난 답 정확 재생과 낡음 표시 | 채택 | PR #7 p1, 147 C 112/112 | 현재 답 조회와 과거 답 재생이 다른 호출이다(`Ledger.replay`) |
| 5 | URL만으로 등록 | 채택 | [catalog L117–118][g-cat-add0], 150 단일 주소 32/32 | 등록은 작게 유지되고 꼬리표는 처음 원문을 읽을 때 붙는다 |
| 6 | 관계 키로 재발견 | 수정. 칸 꼬리표와 대비로 교체 | PR #7 p2, [catalog L17–20][g-cat-rel] | 극성이 없던 관계 대신 `breaks_when` 칸과 대비 행이 있어, 반대로 작동하는 후보가 지지가 아니라 대조로 나온다 |
| 7 | 정규식 관계 추론 셋 | 폐기 | [retrieval L86–104][g-ret-86], [p8][p8] | 접수가 칸별 필요 문장을 만들고 해석 줄로 사용자에게 보인다. 사용자가 잘못 읽은 해석을 고칠 수 있다 |
| 8 | 겹친 단어 수 순위 | 수정 | [catalog L179–200][g-cat-disc], 2.1절 | 기능어·숫자만 겹친 적중은 우연으로 표시되고, 원리 후보는 관문으로만 오른다 |
| 9 | 용도 설명을 색인하지 않음 | 수정(꼬리표를 색인) | [catalog L141–142][g-cat-add] | 꼬리표가 검색에 들어가므로 원문 쪽 말만 쓰고 요청 문장은 거절한다(`PrivacyError`) |
| 10 | 2단계 전문 색인 | 폐기 | [p7][p7] | 경로 기록(서랍 / 새 검색)을 1단계에서 남긴다(`path_log`) |
| 11 | URL 문자열이 곧 동일성 | 수정 | 150 C 15/16, 147 A-url 40/96 | 관측 키에 판과 위치가 들어간다. 별칭은 증거 관측과 취소를 가진다 |
| 12 | 관측과 판단이 한 행 | 수정(분리) | 147 B | 다른 요청이 같은 판·위치를 다시 판독하지 않는다. 사례 A 프로젝트 C의 전체 원문 열람 0회 |
| 13 | 시간 칸 없음 | 수정(넷으로) | [schema L59–65][g-schema-run] | "10월 9일에 알던 기한"을 물을 수 있다(`Ledger.known_on`) |
| 14 | 재검토 작업 | 수정 | [roundtrip L136][g-rt-136] | 후속 판단이 작업을 닫고, 같은 관측의 새 원인은 열린 작업에 합쳐진다 |
| 15 | 수집·유지 정책 없음 | 추가 | 152 | 공급자마다 채널 종류와 주기를 기록한다 |
| 16 | 고정 URL 둘 판독기와 박힌 제안 문장 | 폐기 | [roundtrip L156·L172–185][g-rt-172] | 판독기가 위치를 못 내면 그 후보는 L0·L1의 "확인할 후보"로만 나온다 |
| 17 | 한 문장 기권 | 수정 | [roundtrip L166][g-rt-166] | 답 상태 여섯 가지(complete, partial, none_verified, budget_exhausted, source_unreachable, none_in_scope)와 다음 행동 한 문장 |
| 18 | 표시 개수 예산 | 수정 | [retrieval L171–173][g-ret-173], 257 | 예산이 원문 열람 횟수와 바이트로 바뀌어 읽기 깊이 규칙을 집행할 수 있다 |
| 19 | 근거 종류 셋 | 수정(사다리 여섯) | 257, 058 | 1번 자리 하한(L2)과 원리 자리 상한(L2)을 같은 사다리로 적는다 |
| 20 | 대상 1차 문서 우선 | 추가 | 258 LOD API, 257 API 절 | 타 분야 후보는 대상 문서에 같은 관계가 없을 때만 자리를 얻는다 |

[brief]: https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d/docs/product/RESEARCH_BRIEF.md
[dot0]: https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d/docs/automation/dot-control.json
[dot1]: https://github.com/laadkke-arch/agentflow-open/blob/45896ef1/docs/automation/dot-control.json
[r49]: https://github.com/laadkke-arch/agentflow-open/blob/c8f4b5f1/docs/workstreams/planning/REVIEW-49.md
[g]: https://github.com/laadkke-arch/agentflow-open/tree/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim
[pr6]: https://github.com/laadkke-arch/agentflow-open/blob/8f674773863f56141bb82bafe364397b6f1d82f0/docs/design-threads/independent.md
[pr7]: https://github.com/laadkke-arch/agentflow-open/tree/8fbc885d6a52cd43949c1caf633a39182de2613d/docs/workstreams/design/gallim-review
[pr7a]: https://github.com/laadkke-arch/agentflow-open/blob/8fbc885d6a52cd43949c1caf633a39182de2613d/docs/workstreams/design/gallim-review/ASSESSMENT.md
[pr7lod]: https://github.com/laadkke-arch/agentflow-open/blob/8fbc885d6a52cd43949c1caf633a39182de2613d/docs/workstreams/design/gallim-review/probes/lod/lod_runtime.json
[pr8]: https://github.com/laadkke-arch/agentflow-open/blob/72e8aee231313f84c5f148a4b6694401d8371b50/docs/workstreams/design/alt-starts/README.md
[p7]: https://github.com/laadkke-arch/agentflow-open/blob/8fbc885d6a52cd43949c1caf633a39182de2613d/docs/workstreams/design/gallim-review/probes/out/p7_delete_stage2.txt
[p8]: https://github.com/laadkke-arch/agentflow-open/blob/8fbc885d6a52cd43949c1caf633a39182de2613d/docs/workstreams/design/gallim-review/probes/out/p8_r1.txt
[r147]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/RESULT.md#L35
[r150]: https://github.com/laadkke-arch/agentflow-open/blob/ff2c1fc8786ba70a1432f1089f8f81288e43a61d/docs/workstreams/research/AF-RES-150/RESULT.md#L43
[r152]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/RESULT.md#L112-L116
[r257]: https://github.com/laadkke-arch/agentflow-open/blob/ff1eb5dad4294f27ec368698f544f03519d7fb12/docs/workstreams/research/AF-RES-257/RESULT.md#L46
[r258]: https://github.com/laadkke-arch/agentflow-open/blob/8106a22f4122c798edb52ed9825b06e1040a7ffc/docs/workstreams/research/AF-RES-258/RESULT.md
[r058]: https://github.com/laadkke-arch/agentflow-open/blob/fefeb2146c7f63e49d0578f78989be49acd63291/docs/workstreams/research/AF-RES-058/HANDOFF.md#L40-L48
[lodapi]: https://github.com/mrdoob/three.js/blob/beab9e845f9e5ae11d648f55b24a0e910b56a85a/docs/api/en/objects/LOD.html#L60-L80
[g-arch-22]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L22
[g-arch-24]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L24
[g-arch-25]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L25
[g-arch-27]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L27
[g-arch-40]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L40
[g-arch-46]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L46
[g-arch-49]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L49
[g-arch-51]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L51
[g-arch-57]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L57
[g-search-26]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/SEARCH.md#L26
[g-search-28]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/SEARCH.md#L28
[g-search-76]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/SEARCH.md#L76-L80
[g-eval-13]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/EVALUATION.md#L13
[g-schema-claim]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/schema.sql#L47-L56
[g-schema-run]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/schema.sql#L59-L65
[g-demo-rej]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/demo.py#L29-L83
[g-cat-rel]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/catalog.py#L17-L20
[g-cat-add0]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/catalog.py#L117-L118
[g-cat-add]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/catalog.py#L141-L142
[g-cat-disc]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/catalog.py#L179-L200
[g-ret-86]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/retrieval.py#L86-L104
[g-ret-173]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/retrieval.py#L171-L173
[g-rt-136]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/roundtrip.py#L136
[g-rt-166]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/roundtrip.py#L166
[g-rt-172]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/roundtrip.py#L156-L185
