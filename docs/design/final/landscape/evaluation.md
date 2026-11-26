# 제품 효용 평가와 '작동했다'의 근거 · 지형 조사

✔는 원장을 직접 다시 센 값이다. 나머지는 REVIEW·HANDOFF를 판독한 값이다. 실제 사람 참가는 전 작업에서 0명이다.

## 1. 확정 · 정정 · 열린 것

| 판단 | 작업·핵심 수치 | 상태 |
| --- | --- | --- |
| 미인지→선택 변경→실행 | 022 A 엄격 0/24✔, 기지 제약 교정 2/24(A01·A19), 초기 표적 해법 기지 21/24, 목적표집 B 1/9(B08)✔ [s022]. 236 공식 링크 3/40(엄격 1), 교체 산출물 0/3 [c236]. 225 동일 작성자 직계 수정 1/1·1/2, 외부 URL 0/3 [h225]. 046 0/4, 121 0/6, 153 0/11, 157 0/8, 194 0/4, 203 0/8, 214 0/4, 145 0/16 | **정정**: 전부 U다. 0 효과가 아니다. 공개 기록에는 사전 지식·노출이 없다 |
| 단계 시간과 전체 노동 | 034 NCQ-2 선택 380→57초, 총 849→847초(중앙값, 조건당 10명)✔. 링크만 바꾼 비교 0, 채택 후 재작업 대조 0 [e034]. 237 12행 전부 dev 655, 작성자 자기보고, post 0분 7행, 검수·인수 키 0/12✔ [c237]. 195 배정 24/24·분절 96, 검수 키 0/96. 60초 넘는 공백을 빼면 TUR 첫 문서 PE2/HT 720,511/2,061,853ms가 523,317/517,066ms로 역전 [h195]. 164 98.125/65/115.625, 단위 불명 | **확정**: 단계 절감 ≠ 전체 절감. 총노동 측정 0 |
| 관련성 평정 → 필수조건 | 262 84행·40URL·0점 14✔. 주표 12: 양성·음성·상충 4/4/4. 부가조건 Y3·N4·U3·NA2. 확정 양성 중 Y1·N2·NA1✔. 공동 성공 1–4/12. J1·J2는 높은 평정에도 Unicode 조건 실패 [c262] | 1단계 필터로만 쓴다. 정적 판독이며 S1–S3 원판 0/3 |
| 근거 위치 | 021 근거 회수 A/P/M 6·9·14/23, 오승인 4·3·3/14. 잘못 붙인 대응선은 P보다 나쁨 [h021] | 고정 후보 재생 |
| 같은 예산의 일반 검색 | 013 LLM 웹 16/176(9.1%), 정답 146/176이 내부 대안. 025 새 대상 G·R이 충돌 5·보류 20으로 같음, 열람·인용 완결 0/50 [s025]. 109 질의 15회 같고 개봉 23 대 29, 엄격 쌍 0/6. 209 개선 0·악화 1. 220 자기 제외 첫 해법 개선 0·동률 4, 자기 이슈 1위 5/8 [p220]. 018 BLOCKED | **열림**: 구조화 우위 증거 0 |
| 설명·출처의 부작용 | 058 오권고 거절 82→53/205, 전체 정답 +10.6%p [h058]. 062 출처 3개로 오수락 78.2→68.2%, 클릭 시행 318/1,232, 검색 권유는 오수락 +6.21%p. 066 5개 URL이 정·오 양쪽 근거 | 근거 표시가 오수락을 늘릴 수 있다 |
| 실행한 '작동' | 251 매뉴얼 해석이 8/16회 반전 [r251]. 253 axe 4.7.2 violations→4.8.0 incomplete, 틀린 이름도 passes [u253]. 255 PASS 8/8인데 cut 2도 같은 단언 충족, 폭 +0.015625px에서 줄 [120,120,40]→[80,60,140] [x255]. 186 엔진 간 일치 9/10 | 정확판·고정 입력 한정 |
| 합격 표시의 독립성 | 176 표시 55 = 재렌더 55/55, 같은 조건 독립 실행은 확인 0·미확인 20 [a176]. 184 표시 3 → 로그 1개, 재빌드 연결 0/8 [r184]. 168 0/16→4/16 | 표시 수 ≠ 실행 수 |
| 갤러리 깊이 | 257 D(공개 결과 완결)/R(소스 회수): 깊이 2 0/5·0/5, 3 0/7·0/7, 끝 0/13·1/13(C9, 9위, 집계 accuracy만 공개)✔. API 페이지는 한 번 이동하면 충족, 신규 URL 0 [b257] | '바로 얻는' 링크 0 |
| 유일한 양성 집계 | 054 40분 정확 완료 3/12 대 1/12. 과제 3만 보면 3/12 대 4/12 | 저자 집계 1건 |

## 2. 근거 수준

- **(a) 문서 판독**: 022·034(공개 집계), 236·225·046·117·121·194·203·214, 058·062·066, 176·184, 013·025 판정, 244·257(태그 소스), 262(정적), 249(설계).
- **(b) 고정 입력에서 실행**: 267(태그로 빌드한 CPython 3.12.0, 채점기·참조판 각 41회·309벡터), 251·253·255·186·042, 195(ZIP 재파싱), 021(재생). 237은 회귀 미실행.
- **(c) 사용자 미확인**: 사전 지식, 노출, 이해, 동일인 변경, 검수 시간, 인수, 스크린리더, 가독성, 실제 사용자 파일.

## 3. 249와 267의 범위

**249** [p249][d249]: 구별 *설계*는 완성됐다. 6분 봉인 기저선, 즉시(E)·12분 지연(L) 공개, t0/t12−/t24 스냅샷, K/N/R/F 코딩, 65필드 사전으로 이뤄진다. 합성 4사례·12스냅샷뿐이고 실제 0명이다(24명×2 = 48배정은 계획). 약점: B의 두 후보가 같은 페이지에 있어 노출을 귀속할 수 없다. 버전 검사는 (3,12)뿐이다. 합성 71 person-min/3은 인용 불가다.

**267**✔ [v267][c267]: 회차마다 86/90이고 실패는 F t24의 B2·B3·B6·B7뿐이다(1/0/2/1 대 기대 3/3/4/3). 참조판 종점 일치는 129/129, r1/r2 24쌍은 동일하다. 통제 39벡터: left 4/8, global 4/7, bool 4/8(값은 같고 타입 실패), restore 8/8 통과(호출 중 쓰기 8/8 관측), raise 7/8. 값·타입·예외 실패가 모두 exit 1이다.

**오채점 반례**

| 조건 | 오채점 |
| --- | --- |
| 반환 시점 계약 | 0건 |
| 호출 중 불변 계약 | 8건(restore) |
| 값만 비교하는 채점기 | 4건(bool) |
| 동률 없는 벡터만 사용 | 틀린 방향 4/4 통과 |
| 연속 키만 사용 | 전역 묶음 오류가 드러나지 않음 |

같은 바이트가 서로 다른 행위자에게 있다(N t0 = F t0). 해시는 작성자를 증명하지 않는다. → 267은 고정 벡터로 코드 후보의 적용 가능성을 자동 판정할 수 있다는 것만 답한다(계약·fixture 조건부). 발견·결정·노동은 0이다.

## 4. 설계 함의

**비교 설계**

| 팔 | 구성 |
| --- | --- |
| G | 평소의 LLM+웹 검색 |
| S | 링크와 짧은 설명 카탈로그 + 전문 검색 + 절 위치·판 영수증(021 이득의 대부분) |
| P | 제품 |

- 같은 요청 원문과 봉인된 필수조건(부가조건 포함)을 쓴다.
- 예산은 질의 수가 아니라 개봉 수·전송량·모델 호출·시간으로 맞춘다(109).
- 요청 단위로 짝을 짓고, 팔을 가린 판정자 2명이 본다.
- 사용자 자신의 이슈·저장소는 발견에서 뺀다(220).
- 정답은 봉인 적격집합과 세 팔의 합집합이다. 미판정은 0이 아니라 U다(262).
- 갈림안의 '신규 질문 사건' 단위, 무결성 중단 조건, 분모 분리는 유지한다 [eg].

| 관찰 | 단위 · 분모 | 성공 판정 | 필요한 로그 |
| --- | --- | --- | --- |
| 새 자료 | (요청, 후보). 봉인 요청. 공석·미수신은 별도 | G·S 결과, 사전 목록, 요청 전 카탈로그 어디에도 없던 적격 후보 1개 이상 | 후보 출처(카탈로그·요청 시·상시 수집), first_seen_at, 팔별 결과, 사전 목록 해시 |
| 적용 가능 대안 | (요청, 후보, 조건). 적격집합이 있는 요청 | 조건별 Y/N/U/NA, 사다리 L2 이상. 오승인은 따로 | 조건 판, 스냅샷 해시·절, 정확판 시험 영수증, 판정자 2명 |
| 결정 변화 | 배정(사람×과제) 전원, ITT | 제공→보임→열람→이해→시도→동일인 교체→유지→인수를 단계별 Y/N/U로. K/N/R/F와 '기지 대안의 조건 교정'은 따로 | 249 사전: seal, delivery, visible, open, parent/child 해시+행위자, test, review, accept |
| 전체 노동 | 배정당 작성자+검수자+인수자 person-min. 실패를 포함한 전원, 인수당 비용(인수 0이면 NA) | 단계 시간으로 총량을 대신하지 않는다(034). 대기는 노동이 아니다 | actor_role, mono 구간, active_seconds, artifact_hash에 묶인 review·acceptance |

**제품 DB 필수 기록**
- 결과를 보여 주기 전: 회상과 설계 스냅샷을 봉인한다.
- 추천 슬롯: 순위, 팔, 주장, 근거, 사다리 단계, 영수증 ID. 근거는 URL이 아니라 (추천, 주장, 스냅샷, 절) 단위로 둔다(066).
- 노출: 보임·열람·절.
- 사용자 표지: 알던 것, 새것, 거절과 이유.
- 후속: 전후 해시·행위자, 검수, 인수, 활동 구간.
- missing_code(OBS_ZERO/U/NA/VACANT)는 0으로 바꾸지 않는다. 정정은 덧붙인다.

**근거 사다리**

| 단계 | 근거 | 쓸 수 있는 말 |
| --- | --- | --- |
| L0 | 목록 등재 | "목록에 있다" |
| L1 | 호출·언급(244: 언급은 NearestNeighbors, 실제는 TSNE) | 경고 필요 |
| L2 | 태그 소스에서 요청한 값을 만들고 소비하는 줄(257 R). 태그 SHA와 줄 범위가 필요 | **"방법을 배울 수 있다"** |
| L3 | 공개 산출물에 그 값이 보임(257 D 0/13) | **"바로 얻는다"** |
| L4 | 정확판·고정 입력 실행 영수증 | "이 판에서 이 값". 판이 바뀌면 다시 확인 |
| L5 | 사용자 맥락 | 미확인. 확인 질문으로 넘긴다 |

- 독립 확인 수는 (계보, 시험 SHA, 옵션, 로그 ID) 고유 조합으로 센다.
- **더 읽을 가치**: 정본 API·시험을 먼저 본다. 목록은 목표가 L2이고 아직 미충족일 때만 더 읽는다. 링크 하나에 소스·태그 2파일 대조가 든다. 깊이·공석·첫 충족 순위를 기록한다.

## 5. 뒤집거나 단순화하는 근거

- 025·109·209·220에서 구조 질의는 일반 검색을 이기지 못했다. 재현된 이득은 021의 절 대응뿐이다. 따라서 **S가 v1의 진짜 경쟁안**이다(추론).
- 결정 변화 0/N은 공개 기록의 구조적 결손 탓이다. 공개 사례를 더 캐지 말고 제품이 직접 기록해야 한다.
- 관측된 가치는 주로 기지 대안의 조건 교정과 근거 있는 거절이다(022 기지 21/24, 194). 갈림 EVALUATION은 '당사자가 뜻밖이라고 확인'한 대안을 세지만 사후 자기보고에 기댄다(249 Q2). 사전 봉인 회상과 대조하고, '반영할 수 있음'은 실제 동일인 변경으로 바꾸고, 노동에 검수자·인수자를 넣어야 한다 [eg].
- 근거 표시는 오수락을 늘릴 수 있다. 채택과 오승인을 항상 같이 보고한다.

## 6. 다른 담당에 주는 사실

- **요청**: 노출 전에 "이미 고려한 것"을 봉인하지 않으면 결정 변화를 셀 수 없다. 자기 이슈에는 표지를 붙인다(220 5/8).
- **DB**: 근거 단위는 (추천, 주장, 스냅샷, 절)이다. 해시를 작성자로 쓰지 않는다. 영수증에 정확한 런타임 튜플을 남긴다(267).
- **수집**: first_seen_at이 없으면 '새 자료'를 판정할 수 없다. 합격 표시는 실행 계보로 중복을 제거한다.
- **검색**: 예산은 개봉 수로 잰다. 깊이·공석을 기록한다.
- **운영**: 판이 바뀌면 그 판정만 다시 실행한다(253 4.7.2→4.8.0). 경계 조건(255 폭)도 함께 저장한다.

[s022]: https://github.com/laadkke-arch/agentflow-open/blob/df80ec2406042a73c2114e316894173f66309cda/docs/workstreams/research/AF-RES-022/evidence/statistics.json
[c236]: https://github.com/laadkke-arch/agentflow-open/blob/538cb1f04c83ae2dbf79be7d4fc91b27f818baef/docs/workstreams/research/AF-RES-236/chain.csv
[h225]: https://github.com/laadkke-arch/agentflow-open/blob/d1d8595dd72dcfc809c1045e20d44366bbe30ae5/docs/workstreams/research/AF-RES-225/HANDOFF.md
[e034]: https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/effects.csv
[c237]: https://github.com/laadkke-arch/agentflow-open/blob/0cd0389a47514c81d95ed2b2cd7e42e1efe84ba5/docs/workstreams/research/AF-RES-237/cohort.csv
[h195]: https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/HANDOFF.md
[c262]: https://github.com/laadkke-arch/agentflow-open/blob/ed4e0b1b331c6da5b532130bb6fa9f68b18b2292/docs/workstreams/research/AF-RES-262/conditions.csv
[h021]: https://github.com/laadkke-arch/agentflow-open/blob/29049a5f15b6ef7cd7431f59a059598db6f5d857/docs/workstreams/research/AF-RES-021/HANDOFF.md
[s025]: https://github.com/laadkke-arch/agentflow-open/blob/cf27e148b96bf3c5a3dc8a2a926db4abcf63f146/docs/workstreams/research/AF-RES-025/evidence/scored-slots.jsonl
[p220]: https://github.com/laadkke-arch/agentflow-open/blob/5df1c4816f3401629d6a247d8f0ed8bb7c0cad37/docs/workstreams/research/AF-RES-220/pairs.csv
[h058]: https://github.com/laadkke-arch/agentflow-open/blob/fefeb2146c7f63e49d0578f78989be49acd63291/docs/workstreams/research/AF-RES-058/HANDOFF.md
[r251]: https://github.com/laadkke-arch/agentflow-open/blob/676545d3443eed407f7aa7e7d5b10024bdf0273c/docs/workstreams/research/AF-RES-251/runs.csv
[u253]: https://github.com/laadkke-arch/agentflow-open/blob/520ba50d86e4aad2e67b207cff5dcb1f5d5e3edd/docs/workstreams/research/AF-RES-253/rules.csv
[x255]: https://github.com/laadkke-arch/agentflow-open/blob/060a8587df4c7d58ec12c5f07d4e9f35e627ed61/docs/workstreams/research/AF-RES-255/COUNTEREXAMPLES.md
[a176]: https://github.com/laadkke-arch/agentflow-open/blob/a347a373cdd46910f2cd2cf53419849ba48ee03a/docs/workstreams/research/AF-RES-176/assertions.csv
[r184]: https://github.com/laadkke-arch/agentflow-open/blob/2b83f0fa4f86e97b9643eafaeecc6596cd245561/docs/workstreams/research/AF-RES-184/runs.csv
[b257]: https://github.com/laadkke-arch/agentflow-open/blob/ff1eb5dad4294f27ec368698f544f03519d7fb12/docs/workstreams/research/AF-RES-257/budget.csv
[p249]: https://github.com/laadkke-arch/agentflow-open/blob/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/protocol.md
[d249]: https://github.com/laadkke-arch/agentflow-open/blob/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/event-dictionary.csv
[v267]: https://github.com/laadkke-arch/agentflow-open/blob/c9c39336764b557c1c8f4c154d5ae444c007043d/docs/workstreams/research/AF-RES-267/vectors.csv
[c267]: https://github.com/laadkke-arch/agentflow-open/blob/c9c39336764b557c1c8f4c154d5ae444c007043d/docs/workstreams/research/AF-RES-267/receipts/controls/vectors.csv
[eg]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/EVALUATION.md
