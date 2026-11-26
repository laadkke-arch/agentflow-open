# 발견·검색·타 분야 원리 — 연구 지형

수준: **a** 문서 판독 · **b** 고정 입력에서 코드·원장으로 이번에 재현 · **c** 사용자 미확인. 링크는 모두 해당 SHA에서 확인.

## 1. 확정 · 정정 · 열린 것

**우연 적중**
- 012/LINK_STUDY: 영어 URL만으로 Toyota JIT 4위. 겹친 단어는 URL 경로 `vision-and-philosophy`의 `and` 하나, TreeDB 9위는 `can` 하나. 한국어 URL만은 무응답 28/36, 원리 R@10 .010→한 줄+용도(+184.7B/건) .125. 한국어에서 Toyota·Bazel·TreeDB는 설명을 붙여도 0점 **b**(link_study.py 재실행 일치) [ls]
- 기존안 코드 **b**: gallim `retrieval.py`는 모든 토큰을 OR로 묶는다(L125). 데모 색인에 `render tiles while scrolling`을 넣자 `while`만 겹친 박물관 원리가 적중했고, 출력에 일치 단어가 없어 Toyota형 사고를 가릴 수 없다. SEARCH.md L59는 “다른 동작·검증이 있을 때만 원리 자리”라 하지만 코드 L146은 가설 후보가 있으면 늘 한 자리를 채운다. 기제 추출은 정규식 3개 [ret] [se]

**타 분야 원리의 기여 — 분모**
- 033: 단서 없이 8설계×18후보=144쌍, 지지1·충돌9·부분50·미확인84 **b**(maps.csv 재집계). 반환창 엄격 인용 완결 S·R 0/8. 유일 지지 X01(접수와 공급 결정의 권한 분리)은 S10·R12위로 미반환, 수신 원문에 이미 있던 관계의 보완 설명. 당시판 적격 0, 채택은 8건 모두 미확인 [m33] [r33]
- 013: 실제 설계문서 31건의 선례 176개 중 같은 분야 146·부품 17·다른 생태계 12·**다른 분야 원리 1(0.57%)**, 외부 타 분야 인용 0 **a** [r13]
- 037: 최초안 선택을 바꾼 완결 인과 A 0/8·B 0/4 [j37]. 145: 두 검색 비교 유효 분모 0/8, 독립 초안 0/16, 타 분야 원전 4개는 봉인 뒤 대조 **a** [h145]
- 추가 예측을 결과로 가를 **적격 분모 0**인 7과제. 예측 동일: 053 5/5 [c53] · 057 6/6 [c57] · 077 핵심 선택 변화 0/3 [v77]. 예측은 갈렸으나 결과 없음: 045 다름 3/6·적격 0 [o45] · 183 세 입력에서 수령자 갈림, 공개 실행 0/16 [c183]. 노출로 무효: 174 0/12 [o174] · 166 48셀 0 [h166]. **b**(053·057), 나머지 **a**
- 258(온도 조절기→three.js r170 LOD, 손추적, 실행 0/8): h=.1 이력 모델 B 적중 3/4·오류1(P4, 90에서 하한 등호), 단일 임계 C 1/4. B−A +3/−1, B−C +2/0. LOD API 문서가 이미 hysteresis·깜빡임 회피를 적어 동종 문서만 본 A+도 같은 가설 가능(순증분 미확인). 원분야 안에서도 ESPHome thermostat(≥/≤)과 bang_bang(>/<)의 등호가 다름 **a** [r258] [t258]
- 245: 끝점 선형식 50ms 이내 R1 2/7·R2 7/7, 최대 잔차 185.3/46.5ms **b**(재계산). “대역 축소→비용 상승” 예측 틀림, 실제 DTW 경로 0/2 [b245]
- 긍정 신호는 시험 관점뿐: 069 관계 검색이 “요청 접수와 말단 적용을 따로 확인”, 073 대상·역할 복원 질의가 ‘그룹 이동→기하 이동’ 오독을 피함, 실행 0 **a** [j69] [r73]

**목록 깊이·첫 링크**
- 257/244: 갤러리 깊이 2·3·끝 개별 공개 결과 D 0/5·0/7·0/13. 소스상 개별 예측 회수 R 1/13(C9, 9위). 깊이2→끝 링크 +7에 R +1·D +0. API 페이지 Examples는 추가 URL 0으로 두 반환값을 직접 보임 **b**(재집계) [t257] [bu257]
- 064: 절 주소가 시작 주소와 다른 쌍 6/11, 열람 14→12, 두 조건 확인 0/11 [rt64]. 029: 부분 요구 인용 완결 공통2·웹4·제공자 내부3/12, 전체 0/12 [p29] **a**
- 146: 검토 폭 3→8에 조건부 표시 1→4, 추가 셋은 한 요청의 5·7·8위 **a** [tr146]

**사전 색인 vs 요청 시 열람**
- 072: 카드 구축 20회·2,087,664B. 요청당 URL 열람 L 28,260B, 카드 I 0B, 카드+원문 H 485,044B. I/L 손익분기 HTTP 5회·바이트 약 74회. 상위3 원거리 전이 L 0/14, I·H 1/14 **b** [c72]. 076: 부분 적격 L4·발행자 한 줄 S5·카드 E4/10, 전이 0·1·0/2 **a** [c76]
- 010: 힌트 준 검색으로 원리 7군. DANE 원리당 40–100시간 → “수요 있는 부분만 깊게” **a** [h10]

**한국어**: 110 영어 1/1 기능, 한국어 세 방식 모두 0/1 [h110]. 114 별칭 켜면 직접 1/2→2/2, 충돌 표시 2→6 [h114]. 126 조사 4정책 실제 글 10건 적중 0 [r126]. 118 조작·대상 근거 요구 시 직접 9→8·충돌 15→0·공석 27→88 **b** [t118]

**정정**: 012의 “한계 문장 인라인→근접 오답 증가”는 014 실제 485자료에서 재현 안 됨 [h14]. 258 B의 ≤90 오류(사후 B′ 4/4 소급 금지). 033 X01을 명시 문장만 인정하면 지지 1→0.

**열린 것(c)**: 사용자 사전지식·채택(249 합성), 신경망 임베딩(403), 열린 웹 새 출처 발견률, 몇 달 뒤 재발견 관측 0.

## 2. 근거 수준
b는 위 표시 항목뿐이고 258은 손추적이라 a다. 링크가 사람의 선택을 바꿨는지(c)는 연구 전체에 분자가 없다.

## 3. 설계 함의
**미리 / 요청 때.** 미리: URL·판·짧은 정체와 **작동 관계 한 줄**(주체–행위–대상, 보존 성질). 원리는 URL 철자로 안 찾힌다. 072 기준 같은 자료집 요청이 HTTP 5회·바이트 74회를 넘으면 카드가 유리(작성 노동 미측정). 요청 때: 역할 대응, 깨지는 입력, 대상 분야 원문 대조. 첫 링크는 API·기능 절(257·064). 목록은 깊이 2에서 멈추고 “구체 반환값”을 찾을 때만 소비 줄을 따라 더 연다.

**원리 후보 최소 조건.** ① 역할 대응: 수신 측 주체·대상·결정권이 공여 측과 짝지어진다(X01은 권한 경계가 맞아 지지, 033 CE01은 동일성 경계가 어긋나 충돌). ② 유지할 성질 하나를 원문 절로 인용. ③ 깨지는 입력 하나, 그리고 **그 입력에서 동종 기준선과 예측이 다르다.** ③이 없으면 “설명 링크”로 낮춘다.

**우연 적중 신호.** 경로별 일치 토큰과 필드(URL 경로·제목·본문)를 저장한다. 기능어·URL 경로 토큰만 겹치면 `lexical_accident`로 표시해 원리 자리에서 뺀다. 역할·조작 어휘를 지운 질의에서도 남는지, 반환창 안에 필수 근거가 있는지(033 원창 감사) 본다.

**재발견 키.** 분야명·제품명이 아니라 언어 중립 **관계 키 + 상태 변수 + 깨지는 입력**. 예(제안): `threshold-depends-on-previous-state`(258), `accept-separately-from-fulfil`(X01), gallim의 실제 키 `preserve-source-at-original-path`. 언어별 표면형은 출처·대상과 함께 붙인다(114의 충돌). 반환되지 않은 후보도 요청과 독립된 **후보–관계 간선**으로 남기고 탈락 사유(무매치/풀 소진/미판독/근거 부족/충돌)를 나눈다. 재발견이 실제로 일어나는지는 미관측(c).

**빌릴 것/재확인할 것.** 카드를 세 칸으로 둔다. 258이면 빌릴 것: 두 임계와 직전 상태 1비트. 대상에서 재확인: 등호 방향·단위(°C vs 거리 비율)·초기 상태, 첫 링크는 대상 코드 줄(LOD.js L173–198). 버릴 것: 최소 작동시간·NaN 시 off. 공여 분야 안에서도 등호가 갈린다는 사실을 같이 보여 “경계는 대상에서 정한다”를 전달한다.

## 4. 뒤집거나 단순화할 근거
- **분모가 작고 동종 자료로 같은 예측이 나왔다.** 설계 변경 관측 037 0/12·145 유효 0·실제 인용 1/176(013). 같은 예측: 258 LOD API 문서, 166 Slurm backfill 조건, 174 도구 자체 규칙, 245 R2 선형식 7/7, 057 Yjs API.
- **더 단순한 설명(가설).** 관측된 타 분야 원문의 쓸모는 선택 변경이 아니라 **경계 시험 관점**이다(069·073·033 CE01/CE03·258의 89.999 반례). 원리 경로를 순위 신호가 아니라 “대상에서 확인할 시험 입력 생성기”로 두고 ③을 통과할 때만 자리를 연다. gallim의 무조건 1자리는 버린다.
- 한국어 별칭·조사는 실제 글에서 효과 0(126)에 충돌만 늘었다(114). 영어 조작어·대상 심벌로 옮기는 편이 단순할 수 있다(추측).

## 5. 다른 담당에 주는 사실
- **요청**: 이미 아는 대안을 받아야 새로움을 센다(145 자기 초안이 optional/sentinel·explicit clear를 이미 앎). 원리를 붙이려면 대상 판(258 r170)과 대상·역할(073)이 필요하다.
- **DB**: 경로별 일치 토큰·반환창 해시, 요청과 독립된 후보–관계 간선, 사유별 공석이 있어야 우연 판별·재발견이 된다.
- **운영**: 카드 20문서 2.09MB, 재요청 5회부터 HTTP 이득(072). 깊은 대응은 수요 뒤에만(010).
- **평가**: 동종 기준선과 타 분야 보기가 **다르게 예측하는 자리를 사전 봉인**하고 대상 실행으로 가르지 않으면 분모가 0이 된다(7과제). 표시 게이트는 충돌 표시 15→0 대신 직접 1개를 잃고 공석이 61개 늘었다(118). 이 교환을 따로 보고한다.

[ls]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/LINK_STUDY.md
[ret]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/retrieval.py#L86-L163
[se]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/SEARCH.md
[m33]: https://github.com/laadkke-arch/agentflow-open/blob/d6ac67ae199b8205772587bcf7d583559aff44b4/docs/workstreams/research/AF-RES-033/maps.csv
[r33]: https://github.com/laadkke-arch/agentflow-open/blob/d6ac67ae199b8205772587bcf7d583559aff44b4/docs/workstreams/research/AF-RES-033/RESULT.md
[r13]: https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md#L97-L118
[j37]: https://github.com/laadkke-arch/agentflow-open/blob/68c45d2fb4482850d6a3c29826c43a45ea1dc407/docs/workstreams/research/AF-RES-037/judgments.csv
[h145]: https://github.com/laadkke-arch/agentflow-open/blob/116eae3d2e252cfc1ee4da7017228db24fad42f0/docs/workstreams/research/AF-RES-145/HANDOFF.md
[o45]: https://github.com/laadkke-arch/agentflow-open/blob/29c5da579b7a29118f31541092e6a51f3d77219d/docs/workstreams/research/AF-RES-045/outcomes.csv
[c53]: https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/evidence/comparison-counts.json
[c57]: https://github.com/laadkke-arch/agentflow-open/blob/5c5b5299ec57eefde78029a23a62cfb48f508469/docs/workstreams/research/AF-RES-057/evidence/comparison-counts.json
[v77]: https://github.com/laadkke-arch/agentflow-open/blob/5170e3e07d2278800480e1d71cc2f2a2ce9ab01a/docs/workstreams/research/AF-RES-077/VIEWS.csv
[o174]: https://github.com/laadkke-arch/agentflow-open/blob/347f0c96944d074605320027fe8653b0b83a41ad/docs/workstreams/research/AF-RES-174/outcomes.csv
[c183]: https://github.com/laadkke-arch/agentflow-open/blob/ed7c7278be22a5ad6eb8e87255c7d7064d12c9fb/docs/workstreams/research/AF-RES-183/comparisons.csv
[h166]: https://github.com/laadkke-arch/agentflow-open/blob/8fc8b7706840b670aa258f5f8e32c2a6864c0370/docs/workstreams/research/AF-RES-166/HANDOFF.md
[r258]: https://github.com/laadkke-arch/agentflow-open/blob/a6581c8f2bd2d004990ac62a09c8017bb0781370/docs/workstreams/research/AF-RES-258/RESULT.md
[t258]: https://github.com/laadkke-arch/agentflow-open/blob/a6581c8f2bd2d004990ac62a09c8017bb0781370/docs/workstreams/research/AF-RES-258/transfer.md
[b245]: https://github.com/laadkke-arch/agentflow-open/blob/7c0e46d4ec78948ae1109377898c3ee69f2430c4/docs/workstreams/research/AF-RES-245/beats.csv
[j69]: https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/judgments.csv
[r73]: https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/RESULT.md
[t257]: https://github.com/laadkke-arch/agentflow-open/blob/0b5f83fda3bb7420809ec6c48a095e42818fa839/docs/workstreams/research/AF-RES-257/tail.csv
[bu257]: https://github.com/laadkke-arch/agentflow-open/blob/0b5f83fda3bb7420809ec6c48a095e42818fa839/docs/workstreams/research/AF-RES-257/budget.csv
[rt64]: https://github.com/laadkke-arch/agentflow-open/blob/6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f/docs/workstreams/research/AF-RES-064/routes.csv
[p29]: https://github.com/laadkke-arch/agentflow-open/blob/03e074bbba8db44b2f751dbd84042f07960a23e7/docs/workstreams/research/AF-RES-029/pairs.csv
[tr146]: https://github.com/laadkke-arch/agentflow-open/blob/9bf267b71a0000aae5f098e82eab3f84c0dd7714/docs/workstreams/research/AF-RES-146/transitions.csv
[c72]: https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/costs.csv
[c76]: https://github.com/laadkke-arch/agentflow-open/blob/abe6a4ff0ded1f7076e0f11381ac3da5d3984983/docs/workstreams/research/AF-RES-076/costs.csv
[h10]: https://github.com/laadkke-arch/agentflow-open/blob/0603f0d2990c7a501dbdfc45fbbba79155f505fc/docs/workstreams/research/AF-RES-010/HANDOFF.md
[h110]: https://github.com/laadkke-arch/agentflow-open/blob/281b661f9b17e07483f20834859fa157b4846c75/docs/workstreams/research/AF-RES-110/HANDOFF.md
[h114]: https://github.com/laadkke-arch/agentflow-open/blob/9695479c8e9e3c36488f3d0376f197733e05ef3e/docs/workstreams/research/AF-RES-114/HANDOFF.md
[r126]: https://github.com/laadkke-arch/agentflow-open/blob/abcdda426e2a2d19f0732752c221ea4d494458c4/docs/workstreams/research/AF-RES-126/RESULT.md
[t118]: https://github.com/laadkke-arch/agentflow-open/blob/7186eb4bf27cc9f6a3e6b7a1d6ebc2530abfbf0a/docs/workstreams/research/AF-RES-118/evidence/table3.csv
[h14]: https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/HANDOFF.md
