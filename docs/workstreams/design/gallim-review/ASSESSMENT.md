# 기존 갈림안 검증 · 무엇이 실제로 작동하고 어디서 깨지는가

대상은 `work/design-gallim` 고정판 [`fc68f0d1`][g]이다. 이 문서는 전체 설계서가 아니다. 최종 설계서를 통합하는 쪽이 그대로 가져갈 것, 고쳐 쓸 것, 버릴 것을 근거와 함께 고르도록 돕는다.

## 결론

1. **판단을 기록하는 뼈대는 그대로 가져갈 만하다.** 요청 판 고정과 원문 범위 검증, 요청 판에 묶인 판단, 비유를 지지 근거로 세지 않는 보수적 판정기, 지난 답의 정확한 재생과 "지금은 낡음" 표시는 고정 입력에서 문서가 약속한 대로 동작했다. 테스트 40건도 모두 통과했다.
2. **후보를 찾는 단계는 다시 설계해야 한다.** 관계 추론은 정규식 세 개뿐이라 영어나 다른 표현의 같은 요구에서 0건이다. 어휘 단계는 겹친 단어 수로 순위를 매기는데, 기능어와 숫자도 한 단어로 센다. Toyota가 영어 URL 조건에서 4위에 오른 근거는 `and` 하나였다. 공통 요청 R1에서는 관계 0건, 판독 0건, 답 0건이었다.
3. **시간과 동일성이 없다.** 스키마에 관측·발행·효력 시각이 없어 "그날 알 수 있던 것"을 물을 수 없다. 동일성은 URL 문자열 하나뿐이고 합치기·나누기·철회가 없다. 수집·유지 정책도 없다. 152·147·150의 결과가 각각 필요한 형태를 이미 보여 준다.
4. **단순화할 곳이 있다.** 2단계 전문 색인을 통째로 빼도 다섯 사례의 답이 같았다. 258과 257에서는 대상 분야의 1차 문서가 이미 답을 담고 있었다. 타 분야 연결의 추가 가치는 아직 입증되지 않았다.
5. **실제 사용자 효과는 아무도 재지 않았다.** 249는 설계만 있고 참가자가 0명이다. 267은 채점기만 재현했다.

## 1. 무엇을 어떻게 확인했나

| 항목 | 값 |
| --- | --- |
| 기존안 고정판 | [`fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c`][g]의 `docs/workstreams/design/gallim/` 전부(문서 9개, 코드 8개, 테스트 6개) |
| 함께 읽은 연구 결과 | 012 [`cb602858`][r012], 147 [`30afd115`][r147], 150 [`ff2c1fc8`][r150], 152 [`ba038a0a`][r152], 257 [`ff1eb5da`][r257], 258 [`8106a22f`][r258], 249 [`a61cee2b`][r249], 267 [`c9c39336`][r267], 49차 검토 `work/planning` `c8f4b5f1` |
| 실행 환경 | Linux, Python 3.13, SQLite 내장판, Node 22, three 0.170.0 (npm) |
| 기존 테스트 | `pytest` 40건, 하위 시험 19건 통과 |
| 재현 | [`probes/run.sh`](probes/run.sh) 한 번이면 고정판을 `git archive`로 꺼내 탐침 10개를 다시 돌리고 [`probes/out/`](probes/out/)에 쓴다 |
| 하지 않은 것 | 실제 사용자 관찰, 새 온라인 원문 취득, 다른 스레드의 새 구상 읽기 |

아래에서 **확인**은 고정 코드를 고정 입력으로 돌려 본 결과이고, **약속**은 문서에만 있는 동작이며, **미확인**은 사람이나 운영 자료가 있어야 알 수 있는 것이다.

## 2. 약속과 실제 동작

| 동작 | 문서의 약속 | 고정 입력에서 확인한 것 | 사용자·운영에서 남은 것 |
| --- | --- | --- | --- |
| 요청 고정 | 원문·선택·접점·조건을 한 번에 쓰고, 범위가 어긋나면 거절 ([ARCH L46][g-arch-46]) | 확인. 같은 판의 다른 내용 재전송 거절, 조건 원문 범위 검증 (테스트) | 입력 제공자가 실제로 원문 범위를 붙여 줄 수 있는지 |
| 판단 범위 | 판단은 요청 판에 묶이고 다른 프로젝트로 새지 않음 ([ARCH L24][g-arch-24]) | 확인. `claim`·`candidate_context`가 요청 판을 외래 키로 가짐 ([schema L47–56][g-schema-claim]) | 없음 |
| 판정 | 직접 근거만 지지·반증, 비유·제안은 제외, 미확인·상충 구분 ([ARCH L49][g-arch-49]) | 확인. 비직접 근거는 이유를 남기고 무시 ([demo L29–31][g-demo-rej]), 반증 필수조건이면 배제 ([demo L77–83][g-demo-eval]) | 보류가 많을 때 사용자가 다음 확인을 실제로 하는지 |
| 지난 답 재생 | "지난번 무슨 근거로 답했나"에 답함 ([ARCH L25][g-arch-25]) | 확인. 같은 키로 다시 부르면 바이트 단위로 같은 답, 출처 새 판이 생기면 `stale`과 후속 판 표시 ([p1](probes/out/p1_jobs.txt)) | 없음 |
| 재검토 작업 | 새 출처판이 생기면 관련 판단에 재검토 작업 ([ARCH L51][g-arch-51]) | 일부. 작업은 생기지만 새 판단을 내도 해결되지 않음. `publish_answer`가 `resolve_jobs`를 넘기지 않는다 ([roundtrip L136][g-rt-136], [p1](probes/out/p1_jobs.txt)) | 대기 작업을 누가 언제 처리하는가 |
| 다른 이름으로 재발견 | 관계로 찾으면 분야명이 달라도 후보가 됨 ([ARCH L27][g-arch-27]) | 일부. 정규식이 맞는 한국어 표현에서는 ML 증강 요청이 NARA 보존 마스터를 관계 경로로 찾음. 영어 같은 뜻 요청은 0건 ([p2](probes/out/p2_other.txt)) | 관계 문장을 누가 붙이는가 |
| 관계의 방향 | "어떤 동작이 어떤 성질을 보존/위반하는지" ([ARCH L23][g-arch-23]) | 아님. `catalog_relation`에 극성·판·설정 칸이 없다 ([catalog L17–20][g-cat-rel]). 원본을 지우는 Paperless도 "원본 보존" 관계로 ML 증강 요청에 올라옴 ([p2](probes/out/p2_other.txt)) | 없음 |
| 관측과 판단 분리 | 관측 종류·적용판·판단 시각을 따로 둠 ([SEARCH L26][g-search-26]) | 아님. 한 `claim` 행이 근거 조각과 요청별 판단을 함께 가진다 ([schema L47–56][g-schema-claim]). 다른 요청은 같은 원문을 다시 판독해야 함 | 없음 |
| 그날 알던 것 | 당시 알 수 있던 것과 나중에 복원한 것을 구분 ([EVAL L13][g-eval-13]) | 아님. 시각 칸은 `decision_run.created_at` 하나 ([schema L64][g-schema-run]) | 발행 시각을 모르는 원문의 비율 |
| 동일성 | fragment·판·배포본을 한 사실로 접지 않고, 병합 별칭을 바로 사실로 쓰지 않음 ([ARCH L22][g-arch-22], [L59][g-arch-59]) | 접지 않는 쪽만 확인. 정규화는 스킴·호스트·포트뿐이라 같은 문서 변형 7개가 6항목이 됨. 합치기·나누기·철회·제목 정정 없음 ([p3](probes/out/p3_catalog.txt)) | 없음 |
| HTTP와 유효한 이유 | 상태 코드와 "이유가 아직 맞는가"를 분리 ([ARCH L57][g-arch-57]) | 아님. 수집 코드가 없다 | 152가 본 Pocket처럼 200인 채 기능이 사라지는 비율 |
| 읽기 예산과 중단 | URL 6개·문서당 500단어·1 MiB 같은 읽기 예산과 중단 사유 ([SEARCH L76–80][g-search-76]) | 아님. 코드의 예산은 화면에 보일 후보 수다 ([retrieval L173][g-ret-173]) | 기본 예산 |
| 판독 | 후보의 판·설정·위치를 확인해 조건 판정 | 고정 URL 두 개만. 요구 원문이 정확히 한 문장, 부품 이름이 정확히 "파일 수집"일 때만 근거를 만든다 ([roundtrip L172–182][g-rt-172]). 제안 문장은 URL별로 박혀 있다 ([L156][g-rt-156]) | 없음 |
| 기권 문구 | 원문을 못 읽은 후보가 어디서 탈락했는지 복구 ([SEARCH L28][g-search-28]) | 아님. 관계 0건이든 판독 불가든 "표시 예산 안에서 후보 없음" 한 문장 ([roundtrip L166][g-rt-166]) | 없음 |

## 3. 고정 입력 탐침 결과

| 탐침 | 무엇을 했나 | 본 것 |
| --- | --- | --- |
| [p0](probes/out/p0_roundtrip.json) | 기존 왕복 실행 그대로 | 공개 문서 기반 Paperless는 `keep_source` 반증으로 배제, NARA는 비유라 보류. 주석 철회 뒤 Paperless는 보류로 돌아감(보수적) |
| [p1](probes/out/p1_jobs.txt) | 재검토 작업과 재생 | 지난 답 동일 재생, `stale` 표시. 작업 1건은 두 번째 판단 뒤에도 미해결 |
| [p2](probes/out/p2_other.txt) | 같은 관계, 다른 표현 세 개 | 한국어 바꿔 쓰기와 ML 증강은 관계 경로로 찾음. 영어 "Files dropped into the inbox must stay where the user put them"은 관계 0, 후보 0 |
| [p3](probes/out/p3_catalog.txt) | 카탈로그 단독 | "throttle writes to slow disk and refill buffer"에 Toyota가 `and` 하나로 나옴. 같은 Paperless 문서 변형 7개가 6항목. 제목 정정 거절 |
| [p4](probes/out/p4_toyota.txt) | Toyota 순위 분해 | §5.1 |
| [p5](probes/out/p5_ablate.txt) | 기능어를 뺀 BM25 재계산 | §5.1 |
| [p6](probes/out/p6_crowd.txt) | 요청 문장을 제목에 그대로 적은 가짜 북마크 2개 추가 | 관계가 맞은 후보가 앞에 남음. 예산 3에서 가짜 하나가 미판독 목록에 오름 |
| [p7](probes/out/p7_delete_stage2.txt) | 2단계 색인 삭제 | §6 |
| [p8](probes/out/p8_r1.txt) | 공통 요청 R1 | §4 |
| [p9](probes/out/p9_evalx1.txt) | 봉인 사례 EVAL-X1의 T0·T3 요청 | 두 요청 모두 관계 0, 답 0. 012 자료집을 넣으면 `수`, `한다`, `공개` 같은 말로 GitHub Code Search, OCRmyPDF가 상위에 옴 |
| [lod](probes/lod/lod_runtime.json) | three r170 `LOD.update` 실제 실행 | §5.2 |

## 4. 공통 요청 R1을 기존안에 넣으면

R1은 [AF-RES-012 P03.w 한국어 원문][r012-q]이다. 선택 부분은 "작업 투입·완료 신호", 필수조건은 H1(대기 8·처리 중 4), H2(무제한 버퍼 금지), H3(완료·용량 회복으로 재개)이다. 카탈로그는 네 상태로 넣어 봤다. 기존 시드 3개만, 012 자료집 156개 URL만, URL+한 줄 제목, URL+제목+용도 설명이다. 전체 출력은 [p8](probes/out/p8_r1.txt)에 있다.

| 질문 | 고정 코드로 확인한 동작 | 문서만 약속한 동작 |
| --- | --- | --- |
| 무엇을 미리 알아 두었나 | 시드 링크 3개(Paperless 고정판 사용 문서, NARA 보존 마스터, 관계 없는 북마크 1개)와 관계 2개. 관계 사전은 "원본 보존", "실패 뒤 성공 유지", "중복 방지" 세 정규식이다 ([retrieval L86–104][g-ret-86]). 투입 제어·역압과 맞는 관계는 없다. 012 자료집을 넣어도 관계는 0개다. 용도 설명은 `note`로 저장되지만 색인되지 않는다 ([catalog L141–142][g-cat-add]). | 반복해 찾은 링크에 "어떤 동작이 어떤 성질을 보존/위반하는지"를 붙여 다른 분야에서도 찾는다 ([ARCH L23][g-arch-23]) |
| 요청이 온 뒤 무엇을 새로 했나 | 요청 판과 조건 3개를 원문 범위와 함께 저장했다. 관계 추론 결과는 `[]`이다. 어휘 일치만으로 상위 10개를 골랐는데, URL만 넣었을 때 1위 asyncio-semaphore, 2위 asyncio-queue가 맞은 말은 `13`, `3`, `python`뿐이다. 한국어 원문의 "asyncio의"가 조사째 한 단어로 잘려 `asyncio`와 맞지 않았다. 제목을 더하면 asyncio-queue가 7위로 밀리고 taskiq, huey, arq가 `작업`, `큐`로 올라온다. 용도 설명을 더해도 순위가 같다. 원리 후보 Toyota·Reactive Streams는 어느 상태에서도 10위 안에 없다. 판독기는 고정 URL 두 개만 읽으므로 판독 0건, 답 0건, 미판독 3건이다. 기권 문구는 "표시 예산 안에서 후보 없음"이라 원인을 잘못 말한다. | 관계 질의를 여러 용어로 만들고 공개 목록·표준·전문 사이트를 따로 탐색한다 ([ARCH L40][g-arch-40]). 읽기 예산 안에서 원문을 열고 멈춘 이유를 적는다 ([SEARCH L76–80][g-search-76]) |
| 무엇을 기억했기에 다음 요청이 달라지나 | `flow_answer` 1행(빈 답, 미판독 목록, 다음 확인 없음)만 남는다. `candidate_context` 0, `decision_run` 0이고 카탈로그는 그대로다. 같은 요청을 다시 보내면 같은 빈 답을 재생할 뿐이고, 다른 사람이 비슷한 요청을 보내도 달라지는 것이 없다. | 여러 요청에서 반복해 찾은 링크에 관계를 붙인다. 이 일은 사람(큐레이터) 몫으로 남아 있다 |

R1에서 기존안이 잘한 점도 있다. 근거 없이 "검증됨"을 내지 않았고, 미판독 후보를 숨기지 않았으며, 검색 이유를 그대로 보여 줬다. 사용자는 `13, 3, python`이라는 이유를 보고 우연한 일치임을 알아챌 수 있다.

## 5. 다섯 판단 문제

### 5.1 Toyota 4위 (012)

**원장 근거.** [LINK_STUDY L43][g-ls-43]은 Toyota가 영어 URL만으로 P03.w 4위였고 겹친 말이 `and` 하나였다고 적었다. 012 원자료로 다시 계산하면 ([p4](probes/out/p4_toyota.txt)) 다음과 같다.

- 영어 URL 조건에서 Toyota는 36개 질의 중 21개의 상위 10위에 든다. URL 주소의 `vision-and-philosophy`가 원인이다.
- P03.w의 4위(URL)는 `and` 하나로, 1위(URL+한 줄, URL+한 줄+용도)는 `the`, `time`, `is`, `and`, `when`, `by`, `it`, `in`으로 만들어졌다.
- 영어 URL 조건의 상위 10위 256쌍 중 167쌍은 기능어만 겹쳤다. 그중 관련 판정은 13쌍이고 90쌍은 판정이 없다. 내용어가 겹친 89쌍에서는 34쌍이 관련이었다.
- 결과를 보기 전에 고정한 영어 닫힌 기능어를 빼고 다시 계산하면 ([p5](probes/out/p5_ablate.txt)) Toyota는 P03.w에서 21위로 내려가고(`time`까지 빼면 사라진다), 영어 URL+한 줄+용도의 R@10은 0.306에서 0.350으로, 원리 R@10은 0.226에서 0.250으로 오른다. 반대로 영어 URL만의 원리 R@10은 0.174에서 0.027로 떨어진다.

**기존안의 답.** `discover`는 겹친 서로 다른 단어 수로 순위를 매기고 기능어·숫자를 막지 않는다 ([catalog L179–200][g-cat-disc]). 같은 실패를 그대로 갖는다([p3](probes/out/p3_catalog.txt)). 대신 "왜"에 겹친 말을 그대로 보여 주므로 우연을 숨기지는 않는다.

**뒤집는 것.** "URL만으로도 다른 분야 원리를 찾는다"는 해석은 성립하지 않는다. 영어 URL 조건의 원리 재현율 대부분이 기능어 우연이었다. 용도 설명의 이득은 진짜다. 내용어가 겹친 상위 쌍이 290개, 그중 관련 93개였다. 그런데 기존안은 용도 설명을 색인하지 않는다. Toyota의 메커니즘 설명(인출·보충)과 P03의 요구(대기·용량 회복)는 내용어를 하나도 공유하지 않는다. 그러니 이 원리를 찾으려면 어휘가 아니라 관계 번역이 필요하다.

**권고.** 기능어·숫자만 겹친 일치는 후보 근거로 세지 않고, "왜"가 그것뿐이면 "우연 일치"로 표시한다. 용도 설명을 색인한다. 한국어 조사를 떼어 영어 용어와 맞춘다. 원리 후보는 관계 경로로만 올린다.

### 5.2 258 상태 의존 전이 (three.js LOD ↔ 온도 제어)

**원장 근거.** 258은 4경로×3설명을 사전 봉인하고 손으로 r170 소스를 추적했다 ([RESULT L6–22][r258-res]). 다만 r170 실제 실행은 확보하지 못했다고 인계에 적었다 ([HANDOFF][r258-h]). 이번에 three 0.170.0을 실제로 실행했다 ([lod_runtime.json](probes/lod/lod_runtime.json)).

| 경로 | h=0.1 실행 | h=0 실행 | 258 손추적 |
| --- | --- | --- | --- |
| P1 80→95 | N, N | N, N | 동일 |
| P2 120→95 | F, F | F, N | 동일 |
| P3 80→100→95 | N, F, F | N, F, N | 동일 |
| P4 120→90→95 | **F, F, F** | F, N, N | 동일 |
| 통제 x=95 초기 N/F, x=100, F에서 90, F에서 89.999 | N, F, F, F, N | | 동일 |
| 줌 1, .9, 1, 1.1, 1 (거리 95) | N, F, F, N, N | | 동일 |

온도 제어를 참조한 설명 B는 P4를 F→N→N으로 예측했고, 실행 결과는 F→F→F다. 손추적이 맞았고 B의 P4 오류는 실제다. 원인은 하한 등호다. 온도 조절기 [T05][esphome-t05]는 `>=`·`<=`, 같은 분야의 bang_bang [T06][esphome-t06]는 `>`·`<`를 쓴다 ([RESULT L19, L22, L47][r258-res]). 공여 분야 안에서도 등호 규칙이 갈린다.

**기존안의 답.** 판정기가 비유를 지지 근거로 쓰지 않으므로 B의 오류가 "검증됨"으로 나가지는 않는다. 관계 행에 `invariant`·`breaks_at` 칸이 있어 "빌릴 구조"와 "깨지는 곳"을 적을 자리도 있다. 하지만 전이 제안 문장은 URL별로 박혀 있고 ([roundtrip L21, L156][g-rt-156]), 대상에서 다시 확인할 경계를 구조로 남기지 않는다.

**단순화.** 전이할 것은 "상태에 따라 임계가 둘로 갈린다"는 구조뿐이고, 등호 규칙은 전이 대상이 아니다. 더 큰 단순화도 있다. three.js의 [LOD API 문서 L60–80][three-api]이 이미 `hysteresis`를 "경계에서 깜박임을 막는 임계"로 명시한다. 대상 분야 1차 문서를 먼저 보면 타 분야 연결 없이 답이 나온다. 258도 A+ 대안 대비 타 분야 링크의 독립적 추가 가치는 미확인으로 남겼다 ([RESULT L58][r258-res]).

**권고.** 원리 후보는 먼저 대상의 1차 문서에서 같은 관계를 찾고, 없을 때만 타 분야 후보를 "새 선택"으로 센다. 타 분야 후보에는 빌릴 구조, 대상에서 다시 확인할 경계, 공여 분야 안에서도 갈리는 규칙(전이 제외)을 따로 적는다.

### 5.3 150·147 동일성과 저장

**원장 근거.**
- 147: 세 저장안 A(URL과 정확판 재취득), B(정확판 관측), C(B와 전달 기록)는 현재 답에서 모두 맞았다. URL의 마지막 값을 이월한 A-url은 밀집 현재 96건 중 40건을 잘못 승인했다. 과거 답 112건은 C만 재생했고 A·B는 보류했다. B는 A보다 원문 읽기 바이트가 37,163,112에서 12,387,704로 줄었다 ([HANDOFF][r147-h], [RESULT L35, L57][r147-res]).
- 150: 판단과 근거까지 맞은 것은 URL별 A 7/16(오분리 6), 공통 작업 키 B 9/16(오병합 6), 범위가 있는 방향 관계 C 15/16이었다. 한 고정 절을 한 목적으로 읽는 경우에는 주소 하나로 32/32를 유지했다 ([RESULT L43, L51][r150-res]).

**기존안의 답.** 카탈로그의 동일성은 정규화한 URL이다 ([catalog L38][g-cat-canon]). 변형을 함부로 합치지 않는 점은 150의 경고와 맞는다. 그러나 합칠 방법도 없다. 요청 판에 묶인 판단과 `flow_answer`의 정확한 재생은 147의 C와 같은 성질을 이미 갖는다. 반면 판 단위 공개 관측(147의 B)이 없어서, 다른 요청은 같은 원문을 다시 판독해야 한다.

**단순화와 수정.** 북마크처럼 한 절을 한 목적으로 읽을 때는 URL 하나로 충분하다(150의 32/32). 그러니 URL만으로 등록하는 입구는 그대로 둔다. 동일성이 답을 바꾸는 경우에만 범위와 방향이 있는 관계 행을 둔다. URL의 마지막 값은 절대 재사용하지 않는다. 저장은 둘로 나눈다. 공개 관측(URL, 판, 위치, 관측 시각, 값 또는 실패 종류)은 프로젝트 사이에서 공유하고, 전달 기록(요청 판, 프로젝트, 고른 관측, 앞선 답)은 비공개로 둔다. 이 분리가 요청서의 "공개 자료 공유와 비공개 프로젝트 맥락" 경계와도 맞는다. 147에 따르면 현재 답에는 B만으로 충분하고, C의 전달 기록은 과거 답 재생에만 필요하다.

### 5.4 152 수집·유지 운영

**원장 근거.** 유보 기간 재생에서 새 항목 15건 중 S(신호)와 F(희소 순번)는 14건, P(주기)는 13건, O(요청 때만)는 10–14건을 찾았다. 높은 예산 주류의 발견 중앙값은 P 27시간, S 57시간이었다. 같은 비용으로 전체 보관 목록을 읽을 수 있는 구성에서는 O가 364회 중 350회를 맞혔다 ([HANDOFF L5][r152-h]). 희소층을 빼면 낮은 예산 주류의 낡은 추천 시간 순서가 뒤집혔다(기본 P 136시간·S 70시간, 제거 뒤 P 22시간·S 109시간) ([RESULT L135][r152-res]). Pocket 도움말은 기능이 없어진 뒤에도 200이었다 ([RESULT L102][r152-res]).

**기존안의 답.** 없다. 수집 코드가 없고, 재검토 작업은 누군가 새 판을 넣을 때만 생기며 해결 기록도 남지 않는다.

**뒤집는 것.** 하나의 기본 정책은 없다. 순위가 공급자와 이용층에 따라 바뀐다. F는 S와 발견 수가 같고 시간도 같은 범위라, 희소 순번만의 추가 이득은 이 자료에서 보이지 않는다.

**권고.** 공급자가 무엇을 제공하는지로 정책을 고른다. 이어읽기와 삭제 기록이 있는 변경 피드가 있으면 S, 작은 전체 목록이나 과거판 직접 조회가 있으면 O, 둘 다 없으면 예산을 정한 P다. HTTP 상태와 "이유가 아직 유효한가"를 다른 칸에 둔다. 재검토 작업은 후속 판단이 해결 기록을 남기게 하고, 대기 작업 수를 운영 지표로 본다.

### 5.5 257 읽기 깊이

**원장 근거.** 거리+행 인덱스 요구(N)와 새 표본 레이블 요구(C)는 API 페이지 자체에 정확한 예제가 있었고, 같은 절에 닿는 데 추가 URL이 0개였다 ([HANDOFF L21][r257-h], [RESULT L26–28][r257-res]). 갤러리를 더 읽은 효과는 작았다. C는 깊이 2와 3에서 D(공개 결과가 링크에서 보임)·R(소스에서 방법을 복원 가능)이 0이었고, 끝까지 읽어도 깊이 2 대비 D +0, R +1, 링크 +7이었다. 9위 텍스트 분류 예제는 `pred = clf.predict(X_test)`가 있어 R은 되지만, 공개된 것은 정확도 0.752와 시간뿐이라 D는 아니다 ([RESULT L9, L16–21][r257-res]). 257은 스스로 "API 먼저, 정확한 절이 해결하면 멈춤"과 D/R/V를 색인 키로 제안했다 ([RESULT L67, L73][r257-res]).

**기존안의 답.** 근거에 위치를 요구하는 점은 맞다. 그러나 근거 종류가 `direct/proposal/analogy`뿐이라 D·R·합성 grid 레이블(V)을 구별하지 못한다. 코드의 예산은 읽기가 아니라 표시 개수다.

**권고.** 관측에 증거 유형 D/R/V를 적고, 요구별로 어떤 유형을 인정하는지 정한다. 예를 들어 "실제 출력을 보여 주는 예제"를 원하면 D만 인정한다. 읽는 순서는 대상 API 문서(추가 URL 0)가 먼저다. 첫 정확 일치에서 멈추고, 요구가 R을 원하는데 D가 없을 때만 꼬리를 읽는다. 예산은 요청 수와 바이트로 센다.

## 6. 부품 삭제 시험

[p7](probes/out/p7_delete_stage2.txt)은 2단계 색인(`rebuild_index`와 FTS5 `search`)을 1단계 짧은 목록을 그대로 넘기는 함수로 바꿨다. 기존 왕복, 철회 뒤 재판정, ML 증강, 영어 inbox, 한국어 바꿔 쓰기 다섯 경우에서 답·조건 상태·다음 확인이 모두 같았다. 잃는 것은 2단계가 남기던 경로 기록(어휘 경로인지 관계 경로인지)뿐이다. 그 기록은 1단계 "왜"에서 바로 남길 수 있다. 지금 규모에서는 2단계를 빼도 된다.

반대로 관계 행과 관계 추론은 빼면 답이 바뀐다. ML 증강 요청에서 NARA는 겹친 말 없이 관계로만 올라왔다([p2](probes/out/p2_other.txt)). 관계가 빠지면 이 재발견이 없어진다. 문제는 관계라는 생각이 아니라, 관계를 고르는 방법이 정규식 세 개라는 점이다.

## 7. 채택·수정·폐기 후보

| # | 요소 | 판정 | 근거 | 이 결정으로 다른 곳에서 달라지는 동작 하나 |
| --- | --- | --- | --- | --- |
| 1 | 요청 판 고정과 원문 범위 검증 | 채택 | [scope_input][g-scope], 테스트, [ARCH L46][g-arch-46] | 요청을 고치면 새 판이 생기므로, 지난 답 재생과 비교가 판 단위로 이뤄진다 |
| 2 | 판단을 요청 판에 묶기 | 채택 | [schema L47–56][g-schema-claim] | 다른 프로젝트는 판단을 물려받지 않고 공개 관측만 재사용한다(봉인 사례 T3-b) |
| 3 | 보수적 판정기 | 채택 | [demo L29–83][g-demo-rej], [p0](probes/out/p0_roundtrip.json) | 타 분야 원리는 절대 "검증됨"이 되지 않으므로, 답 화면에 "시험해 볼 원리" 칸이 따로 있어야 한다 |
| 4 | 지난 답 정확 재생과 낡음 표시 | 채택 | [p1](probes/out/p1_jobs.txt), 147 C 112/112 | 현재 답 조회와 과거 답 재생이 다른 호출이 된다 |
| 5 | URL만으로 등록 | 채택 | [catalog L117–118][g-cat-add0], 150 단일 주소 32/32 | 등록 비용은 그대로 작고, 설명·관계는 나중에 붙는다 |
| 6 | 관계 키로 재발견 | 수정 | [p2](probes/out/p2_other.txt), [catalog L17–20][g-cat-rel] | 관계에 극성(보존/위반)과 대상 판을 붙이면, Paperless는 ML 증강 요청에서 후보가 아니라 반례로 보인다 |
| 7 | 정규식 관계 추론 3개 | 폐기(교체) | [retrieval L86–104][g-ret-86], [p2](probes/out/p2_other.txt), [p8](probes/out/p8_r1.txt) | 관계 문장을 요청 입력 단계에서 만들고 사용자에게 보여 주므로, 사용자가 잘못 뽑힌 관계를 고칠 수 있다 |
| 8 | 단어 수로 순위 매기기 | 수정 | [catalog L179–200][g-cat-disc], [p4](probes/out/p4_toyota.txt), [p5](probes/out/p5_ablate.txt) | 기능어·숫자를 빼면 영어 URL만의 원리 재현율이 0.174에서 0.027로 정직하게 떨어지고, 원리 후보는 관계 경로로만 오른다 |
| 9 | 용도 설명을 색인하지 않음 | 수정(색인) | [catalog L141–142][g-cat-add], [LINK_STUDY L22][g-ls-22] | 용도 설명이 검색에 들어가므로 설명을 쓸 때 출처와 적용 한계가 꼭 필요해진다(이미 `provenance` 필수) |
| 10 | 2단계 FTS5 색인 | 폐기(지금 규모) | [p7](probes/out/p7_delete_stage2.txt) | 경로 기록을 1단계 "왜"에 남겨야 한다 |
| 11 | URL 문자열이 곧 동일성 | 수정 | [p3](probes/out/p3_catalog.txt), 150 C 15/16, 147 A-url 40/96 | 같은 문서의 고정판과 main판이 다른 관측으로 남고, 합치기는 범위가 있는 관계 행으로만 한다 |
| 12 | 관측과 판단이 한 행 | 수정(분리) | [schema L47–56][g-schema-claim], [SEARCH L26][g-search-26], 147 B | 다른 프로젝트 요청에서 원문을 다시 판독하지 않고 판 단위 관측을 재사용한다 |
| 13 | 시간 칸 없음 | 수정(추가) | [schema L64][g-schema-run], [EVAL L13][g-eval-13] | 발행·효력·관측 시각을 따로 두면 "10월 9일에 알던 기한"을 물을 수 있다(봉인 사례 E-a) |
| 14 | 재검토 작업 | 수정 | [roundtrip L136][g-rt-136], [store L204][g-store-204], [p1](probes/out/p1_jobs.txt) | 후속 판단이 작업을 닫으므로, 대기 작업 수가 운영 지표가 된다 |
| 15 | 수집·유지 정책 없음 | 수정(추가) | 152 | 공급자마다 정책이 달라지므로, 공급자 기록에 "변경 피드·전체 목록 제공 여부"가 필요하다 |
| 16 | 고정 URL 2개 판독기와 박힌 제안 문장 | 폐기(데모 한정) | [roundtrip L172–182][g-rt-172], [L156][g-rt-156] | 판독기가 원문 위치를 못 내면 "미판독"으로 남기고, 제안 문장은 관계 행에서 만든다 |
| 17 | 한 문장짜리 기권 | 수정 | [roundtrip L166][g-rt-166], [p8](probes/out/p8_r1.txt) | R1에서 "관계 0, 어휘만 일치 10, 판독 가능한 원문 없음 3"처럼 원인을 나눠 말한다 |
| 18 | 표시 개수 예산 | 수정 | [retrieval L173][g-ret-173], [SEARCH L76–80][g-search-76], 257 | 예산이 읽기(요청 수·바이트)로 바뀌면 257의 중단 기준을 예산으로 집행할 수 있다 |
| 19 | 근거 종류 3개 | 수정(추가) | [schema L50][g-schema-claim], 257 | 증거 유형 D/R/V가 생기면 요구별 인정 유형을 정할 수 있다 |
| 20 | 대상 1차 문서 우선 | 새로 추가 | 258 LOD API, 257 API 페이지 | 타 분야 후보는 대상 문서에 같은 관계가 없을 때만 "새 선택"으로 센다 |

## 8. 이 문서가 새로 둔 가정

근거가 고정 입력 하나나 사례 두 개뿐인 것은 가정으로 따로 적는다.

- **기능어 목록.** p5의 목록은 결과를 보기 전에 고정했지만 영어 하나다. `time`을 넣느냐에 따라 Toyota가 P03.w의 21위와 순위 밖을 오간다. 경계가 민감하다.
- **관계 문장을 요청 단계에서 만들 수 있다.** 모델이나 사람이 관계 문장을 안정적으로 만든다는 근거는 없다. Toyota와 P03에서 내용어가 하나도 겹치지 않는다는 사실은 번역이 필요하다는 것만 보여 준다.
- **대상 1차 문서 우선.** 근거는 258과 257 두 사례다.
- **공급자 기능에 따른 정책 선택.** 152의 공급원 세 곳에서만 관찰했다.
- **공개 관측이 사생활 경계를 지킨다.** 관측 행에 요청 맥락이 새지 않는지는 스키마 시험으로 확인해야 한다.

## 9. 실제 사용자로 확인할 것

249는 평가 절차만 설계했고 참가자는 0명이다 ([HANDOFF][r249-h]). 267은 CPython 3.12.0에서 채점기를 회차마다 86/90으로 재현했다. 다만 입력을 바꿨다가 되돌리는 통제를 원 채점기가 8/8 통과시켜, 호출 중 쓰기를 놓쳤다 ([HANDOFF][r267-h]). 둘 다 사람에게 미치는 효과를 재지 않았다.

- 사용자가 "왜"에 기능어만 있을 때 우연으로 알아보는가.
- "시험해 볼 원리"를 받은 사용자가 실제로 설계를 바꾸는 비율은 얼마인가. 대상 1차 문서만 받은 경우와 비교한다.
- 지난 답 재생과 낡음 표시가 신뢰 판단에 쓰이는가.
- 기본 읽기 예산과 중단 시점이 사용자의 기다림에 맞는가.
- [봉인 사례 EVAL-X1](SEALED_CASE.md)의 T0-c처럼 해석이 갈릴 때, 한 번 되묻는 것을 사용자가 받아들이는가.

## 10. 봉인 사례에서 기존안의 출발점

[p9](probes/out/p9_evalx1.txt)는 [EVAL-X1](SEALED_CASE.md)의 T0과 T3 요청을 기존안에 넣은 기준선이다. 두 요청 모두 관계 추론 0, 답 0이다. 012 자료집을 넣으면 `수`, `한다`, `공개`, `서버에` 같은 말로 GitHub Code Search, OCRmyPDF, Amazon SQS가 상위에 오지만 판독 대상이 아니라 답은 비어 있다. 오승인은 0이라 T0-a는 어기지 않는다. 하지만 T0-b(시험해 볼 원리 제시)와 T3-a(관계로 재발견)는 충족하지 못하고, T1 이후 기준은 시간 칸이 없어 표현할 수 없다. 새 구상은 이 기준선과 비교하면 된다.

[g]: https://github.com/laadkke-arch/agentflow-open/tree/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim
[g-arch-22]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L22
[g-arch-23]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L23
[g-arch-24]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L24
[g-arch-25]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L25
[g-arch-27]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L27
[g-arch-40]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L40
[g-arch-46]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L46
[g-arch-49]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L49
[g-arch-51]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L51
[g-arch-57]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L57
[g-arch-59]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/ARCHITECTURE.md#L59
[g-search-26]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/SEARCH.md#L26
[g-search-28]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/SEARCH.md#L28
[g-search-76]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/SEARCH.md#L76-L80
[g-eval-13]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/EVALUATION.md#L13
[g-ls-22]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/LINK_STUDY.md#L22
[g-ls-43]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/LINK_STUDY.md#L43
[g-schema-claim]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/schema.sql#L47-L56
[g-schema-run]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/schema.sql#L59-L65
[g-demo-rej]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/demo.py#L29-L43
[g-demo-eval]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/demo.py#L47-L83
[g-cat-canon]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/catalog.py#L38-L66
[g-cat-rel]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/catalog.py#L17-L20
[g-cat-add0]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/catalog.py#L117-L118
[g-cat-add]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/catalog.py#L141-L142
[g-cat-disc]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/catalog.py#L179-L200
[g-ret-86]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/retrieval.py#L86-L104
[g-ret-173]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/retrieval.py#L171-L173
[g-rt-136]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/roundtrip.py#L136
[g-rt-156]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/roundtrip.py#L156
[g-rt-166]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/roundtrip.py#L166
[g-rt-172]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/roundtrip.py#L172-L185
[g-store-204]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/store.py#L204
[g-scope]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/scope_input.py
[r012]: https://github.com/laadkke-arch/agentflow-open/tree/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012
[r012-q]: https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/queries/queries.jsonl
[r147]: https://github.com/laadkke-arch/agentflow-open/tree/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147
[r147-h]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/HANDOFF.md
[r147-res]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/RESULT.md
[r150]: https://github.com/laadkke-arch/agentflow-open/tree/ff2c1fc8786ba70a1432f1089f8f81288e43a61d/docs/workstreams/research/AF-RES-150
[r150-res]: https://github.com/laadkke-arch/agentflow-open/blob/ff2c1fc8786ba70a1432f1089f8f81288e43a61d/docs/workstreams/research/AF-RES-150/RESULT.md
[r152]: https://github.com/laadkke-arch/agentflow-open/tree/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152
[r152-h]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/HANDOFF.md
[r152-res]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/RESULT.md
[r257]: https://github.com/laadkke-arch/agentflow-open/tree/ff1eb5dad4294f27ec368698f544f03519d7fb12/docs/workstreams/research/AF-RES-257
[r257-res]: https://github.com/laadkke-arch/agentflow-open/blob/ff1eb5dad4294f27ec368698f544f03519d7fb12/docs/workstreams/research/AF-RES-257/RESULT.md
[r257-h]: https://github.com/laadkke-arch/agentflow-open/blob/ff1eb5dad4294f27ec368698f544f03519d7fb12/docs/workstreams/research/AF-RES-257/HANDOFF.md
[r258]: https://github.com/laadkke-arch/agentflow-open/tree/8106a22f4122c798edb52ed9825b06e1040a7ffc/docs/workstreams/research/AF-RES-258
[r258-h]: https://github.com/laadkke-arch/agentflow-open/blob/8106a22f4122c798edb52ed9825b06e1040a7ffc/docs/workstreams/research/AF-RES-258/HANDOFF.md
[r258-res]: https://github.com/laadkke-arch/agentflow-open/blob/8106a22f4122c798edb52ed9825b06e1040a7ffc/docs/workstreams/research/AF-RES-258/RESULT.md
[r249]: https://github.com/laadkke-arch/agentflow-open/tree/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249
[r249-h]: https://github.com/laadkke-arch/agentflow-open/blob/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/HANDOFF.md
[r267]: https://github.com/laadkke-arch/agentflow-open/tree/c9c39336764b557c1c8f4c154d5ae444c007043d/docs/workstreams/research/AF-RES-267
[r267-h]: https://github.com/laadkke-arch/agentflow-open/blob/c9c39336764b557c1c8f4c154d5ae444c007043d/docs/workstreams/research/AF-RES-267/HANDOFF.md
[three-api]: https://github.com/mrdoob/three.js/blob/beab9e845f9e5ae11d648f55b24a0e910b56a85a/docs/api/en/objects/LOD.html#L60-L80
[esphome-t05]: https://github.com/esphome/esphome/blob/2026.11.0/esphome/components/thermostat/thermostat_climate.cpp#L1045-L1095
[esphome-t06]: https://github.com/esphome/esphome/blob/2026.11.0/esphome/components/bang_bang/bang_bang_climate.cpp#L97-L138
