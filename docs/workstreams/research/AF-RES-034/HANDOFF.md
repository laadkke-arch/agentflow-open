# AF-RES-034 · 최종 인계

**상태: REVIEW_READY_WITH_GAPS.** 짧은 사람 과제에서 실제 시간과 품질을 함께 관측한 비교는 확인했다. 그러나 **선례를 일찍 제공해 첫 채택 뒤의 재작업 노동을 줄였다는 인과 절감량은 이번 핵심22연구군에서 확인하지 못했다.** 절감량0분이라는 결론이 아니라 미확인이다. 문헌·산출물 최소수는 봉인한 독립 내용 기준으로 충족했으며, 검색 포괄성과 일부 원판·시간 원자료의 제한은 미충족으로 남긴다.

## 고정 결과와 실행 환경

| 항목 | 실제 확인값 |
| --- | --- |
| task_id / 담당 | AF-RES-034 / 배정 worker_kind web-pro |
| 저장소 / 작업 브랜치 | laadkke-arch/agentflow-open / work/research-af-res-034 |
| owned_path | docs/workstreams/research/AF-RES-034/ |
| **result_commit** | **0fe0ae4510e0052031919c748972dcf4bd4a7cbc** |
| 고정 결과 | [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/0fe0ae4510e0052031919c748972dcf4bd4a7cbc/docs/workstreams/research/AF-RES-034/RESULT.md) |
| 고정 수용 판정 | [acceptance-evidence.json](https://github.com/laadkke-arch/agentflow-open/blob/0fe0ae4510e0052031919c748972dcf4bd4a7cbc/docs/workstreams/research/AF-RES-034/evidence/acceptance-evidence.json) + 이 인계 커밋의 evidence/acceptance-finalization.json |
| 계획 기준 통합 SHA | d3fbd08d44fd0e2915d1f766721a81845bacc213 |
| 실제 시작 통합 SHA | 9668632e915d508e93ddfdc5e8fe4b88bcbfec56 |
| 종료 전 검사에서 확인한 최신 통합 SHA | 97bf71e483826692aa351559c3dda23f7a92ae70 |
| 고정 의존 결과 | AF-RES-022 df80ec2406042a73c2114e316894173f66309cda / AF-RES-030 3f77073d6294b739bb340b23e3c4c10640c5b08c |
| 실제 작업환경·모델 | ChatGPT Linux cloud shell, 공개 웹·기관/저자 원문, GitHub 연결. 세션 지침 명칭 GPT-6 Astra Pro. UI 표시 모델/선택값·추론 강도는 관측되지 않아 미확인 |
| 기간 | 발행2005–2025 고정, 검색 종료일2026-11-23 KST. 검색 종료 기록 UTC는 evidence/search-closure.json. 일부 검색의 정확 실행시각은 미보존이며 기록시각으로 대체하지 않음 |

처음에 통합 브랜치의 AGENTS.md, STATE.md, DOT_AUTOMATION, RESEARCH_WORKFLOW, dot-control의 배정 및 의존 HANDOFF를 읽었다. 실제 세션 시작 명령과 manifest는 첫 커밋에 있다. AF-RES-022의33사건,026의 문구,030의 A24/B8을 새 사람 표본으로 세지 않았고, 웹·빌드·재생·PR 경과일·수정 줄 수를 사람 노동으로 바꾸지 않았다. 새 모집·연락·사용자 시험은 실행하지 않았다.

## 확인한 범위와 핵심 판정

| 층위 | 결과 | 적용 범위 |
| --- | --- | --- |
| 적격 고유 외부 원문 | **30 = 소프트웨어15 + 산업·제품 디자인3 + 학습과학4 + 별도 원산출물8** | source 원장48행 중 적격30만 산입. 부분/발견·동반·인접·제외 행은 별도 |
| 핵심 가족 / 독립 실험 | **22 / 26** | 같은 논문의 별도 코호트와 동일 실험 중복 출판을 구별 |
| 설계상 직접 / 간접·불명 / 대조 부재 | **16 / 4 / 2 가족** | 실험 등급 R19/Q3/U2/O2. R도 제품 링크 단독 인과효과를 뜻하지 않음 |
| 링크만 바뀐 제품 직접 비교 | **0** | UI·코퍼스·교육·실행기능·완성 풀이가 함께 바뀐 효과를 분리하지 못함 |
| 채택 후 재작업 노동의 대조 관측 | **0** | 조건부 절감 산식은 해당 없음; 전체 문헌에 존재하지 않는다는 증명 아님 |
| 원장과 심사 규모 | sources48행 / studies74군행 / effects53행 / attempts203행 / screening1066행·고유URL901 | 검색행·과제·코드 snippet을 사람 또는 독립 연구 수로 세지 않음 |

가장 가까운 양성 근거는 Unakite2의 **정답설명3개에 도달하는 시간114.63 대332.56초**(새16명, 양 조건 전원 달성)와 Strata의 **적합성 판단292.1 대432.7초·유효 이유7.9 대4.5개**(20명)다. 좁은 이해·판단 과제의 도구 묶음 결과이며 실제 구현 전체 품질·장기 수정 노동으로 외삽하지 않는다(Rt-S01/Er-01, Rt-S03/Er-04).

주요 반례는 NCQ2에서 package 선택 중앙시간이380→57초였지만 **총 중앙시간은849→847초**였다는 점, ExampleOverflow의 고정45분 품질 평균1/4 대2/4라는 반대방향 점추정, Acar에서 기능성공과 조건부 보안이 다른 방향이지만 전체 분석시행의 안전한 기능완성이18/52씩 같았다는 점이다. NCQ는 baseline 선행, EO는5명씩의 넓은 불확실성, Acar는 배정 서술 충돌을 보존했다. 효과 없음·불확실성·동등성은 구별한다.

다른 분야에서는 먼 유추의 참신성 방향이 Chan/Fu에서 달랐지만 거리척도와 자극이 같지 않았으며, Reisslein의 지식×순서 교차는 근접전이에 한정됐다. 학습시간 단축과 공통 후검사가 있어도 품질 동등성은 입증되지 않았다. 시간·품질·고착·후검사·실제 수정 노동의 경계는 measures.md에, Q별 반례와 틀릴 조건은 SELF_CHECK.md에 있다.

## 산출물과 검증 범위

SCOPE.md와 initial-selection.json은 사전 규칙·초기 기대를, screening.csv는 후보·선정·제외·미심사·접근 실패를, studies.csv/effects.csv는 군별 설계와 원값·계산·누락을 보존한다. sources.jsonl/attempts.jsonl에는 URL·판·UTC/시각 한계·위치·확인 내용·반대 해석을 남겼다. claims.jsonl와 DATA_DICTIONARY.md는 ID·분모·JSON 열의 연결을 설명한다. REVISIONS.md와 분담 final-review는 원장 고정 뒤 바뀐 행·판단을 추적한다.

RESULT는 제목 다음에 지정한 세 표를22/16/5행으로 두고 Q1~Q8·관점·전이 한계를 설명한 뒤 정확3행 약점표로 끝난다. future-study.md는 **미시행** 자유검색 대 목적·근거 링크의 병렬 무작위 비교를 구체화했다. 같은 과제·예산·사전 지식·맹검 품질·실제 사람활동·첫채택 SHA·다음 재검을 연결하며, 고정 상한의 행정적 검열과 조기 포기/실패를 구분한다. 제안90/60분·7일·10분 사업차이·−5%p 품질 경계·표본 가정은 관측 결과가 아니다.

원산출물8개는 두 연구군의 독립 내용 자료다. **실험 전용 자료만 인정하여 NCQ 일반 조작 지시문을 제외하면7개**, 그리고 **사람별 시작·종료·중단 시간 raw는0개**다. CodeMend IR 자료3개는20명 lab 시간자료가 아니고, 준비 notebook의 hatch/shadow·10후보쌍/실제5쌍은 실제 제공판 동일성이 미확인이다. 같은 파일의 여러 그림이나 원고의 여러 쪽을 쪼개 산입하지 않았다.

분담 작성자들의 직접 판독과 자체 산술 검사, 다른 AI 에이전트의 원산출물 추가 재독을 구별했다. 독립 인간 두 명의 맹검 이중 코딩이나 새 사람 시험 재현으로 부르지 않는다.

## 실제 검사 영수증

| 검사 | 대상·실제 결과 | 영수증 |
| --- | --- | --- |
| 통합 ID·카운트·산식·구조 | 91검사,64수치 재계산 및 별도 비시간3대비/EO CI 확인, exit0. source/study/effect/claim/attempt 조인 누락0 | evidence/validation.json |
| 고정판 원격 재독 | 결과 SHA0fe0ae4…의 RESULT·acceptance·validation을 GitHub에서 재열람. 실제 내용·blob SHA·bytes 일치. 검증 입력16파일의 커밋 SHA256도 모두 일치 | evidence/remote-reread.json |
| 요청된 session check | **2026-11-22T16:36:51.903069+00:00, exit0, status=passed, freshness=remote_checked**. checked_out_commit=0fe0ae4510e0052031919c748972dcf4bd4a7cbc. outside_paths=[], unmerged_paths=[], errors=[] | evidence/session-check.json |
| 계약·기준 | task_base/scope_base=9668632e915d508e93ddfdc5e8fe4b88bcbfec56, integration=97bf71e483826692aa351559c3dda23f7a92ae70, contract SHA256=19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc | manifest.json 및 session-check.json |

실제 실행한 필수 명령은 다음과 같다. 저장소 계약 검사이며 제품/사용자 시험 통과를 뜻하지 않는다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-034/manifest.json --fetch
```

고정 수용 파일은 결과를 출판하기 직전의 내용 검증판이다. 그 판을 원격 재독한 사실을 보존하기 위해 덮어쓰지 않았다. 당시 pending이었던 출판·검사·인계 단계의 실제 완료는 이 인계와 evidence/acceptance-finalization.json이 보완한다. 실질적 검색 한계4개와 자료 민감도 진단3개는 해소한 것으로 바꾸지 않는다.

## 묶음별 원격 커밋

| 묶음 | 원격 SHA |
| --- | --- |
| ① 범위·manifest | 9a7d461ed8fd3fe57c2b4d29d8249b7c64e93eae |
| ② 초기 입력·기대/선정 봉인 | 5873c4b42d4a0fb362f024b3d1d76eb4a2ba5b1a |
| ③ 실제 관측·직접 판독·탈락·반례 | f31b498c56dc9f06f76a163d0601280df0704f7a |
| ④ 재집계·RESULT·SELF_CHECK·수용 | 634a27a34e7445c19f8a880c0c35d328bb34b391 |
| ④ 원격 재독 보정·최종 결과 | **0fe0ae4510e0052031919c748972dcf4bd4a7cbc** |
| ⑤ 최종 인계 | 이 HANDOFF와 실제 재독·검사 영수증을 포함하는 마지막 커밋. 부모는 위 최종 결과 SHA이며 자기 커밋 SHA를 파일 안에서 순환 참조하지 않음 |

셸 push는 자격 증명이 없어 exit128이었고, 승인된 GitHub 연결로 커밋 객체와 ref를 갱신한 뒤 공개 fetch로 확인했다. dot-control.json을 수정하지 않았고 통합 브랜치에 병합하지 않았다. 모든 결과·영수증·수정은 owned_path 아래다.

## 미충족과 막힌 지점

네이티브 ACM DL/IEEE 정렬 첫30개와 완전한1단계 cited-by 목록을 확보하지 못해 일반 웹·venue/site 검색·기관/저자본으로 대체했다. 이 검색을 네이티브 전수검색으로 부르지 않는다. 초기 보조7질의의 순위와 후기2전방검색의 정확 질의·실행 UTC도 남지 않았다. 후자의 반환16/10개는 보존했으나 잃은 인자를 추정해 채우지 않았다. 이 네 검색/추적 조건은 수용 A06/A07/A08/A10에서 미충족이다.

산출물 엄격 하위집합7, 실제 제공판 불확실성, 사람 시간 raw0은 A15/A16/A17의 진단이다. 이는 새로 추가한 사용자 최소조건이 아니며 독립 내용 기준8개라는 판정과 함께 읽어야 한다. 일부 원판·원자료에 접근할 수 없으므로 전체 배정자 CI나 장기 재작업 절감량을 더 계산하지 않았다.

**재개할 첫 자료:** [NCQ 고정 조작 지시문](https://github.com/Brittany-Reid/node_code_query/blob/ce14f193f7014c120f04619826cb251818d99b0e/docs/instructions.md)과 논문 §7.1.5의 참가자 화면 문서를 나란히 두고 실험 제공판을 식별할 커밋/문서 증거를 먼저 확인한다. 확인되면 산출물 판 동일성의 불확실성을 좁힐 수 있지만 사람 시간 raw 부재는 그대로다. 검색 수용을 마무리할 첫 입력은 SCOPE의 동일 일반/반대 질의에 대한 ACM DL/IEEE의2005–2025 관련도 첫30개 export이며, 기존 screening의 DOI/제목/URL과 중복 대조해야 한다. 과거 순위는 새 실행으로 소급 복원했다고 쓰지 않는다.

## 직접 실행하지 않은 원 분석과 필요한 입력

자체 집계·검산은 실행했다. 다음은 저자 분석의 향후 재생 경로이며 이 작업에서 실행한 것으로 표시하지 않는다. 이를 재생해도 참가자 시간 원자료가 생기지는 않는다.

| 원 분석 | 실행할 명령·작업 위치 | 먼저 필요한 고정 입력·한계 |
| --- | --- | --- |
| NCQ snippet lint | 고정 저장소 루트에서 `node data/scripts/user-study-snippets` | ce14f193f7014c120f04619826cb251818d99b0e, Node14.17.0 및 해당 lockfile, codesnippets1.csv/2.csv. 기본 main은 첫 파일이며 두 번째는 원 주석 선택을 명시해 별도 실행. 출력순서와 CSV레코드 매핑 필요. Fig20 사람 총시간은 재계산 불가 |
| CodeMend IR 평가 | 고정 저장소의 codemend/models에서 `python2 eval2.py` | 445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d, Python2.7 호환 의존성, eval-gt-2.csv361행, before1~5.py, vectors-so-text-python-lemma.bin, bi2-0410-d.model, elem_pyplot_counts_0404 등 코드가 요구하는 모델/캐시. MRR/top-k 채점 재생이며20명lab 시간 재현이 아님 |
| 실제 사람 시간 재계산 | 입력 확보 뒤 사람×과제×조건별 시작·종료·중단을 조인하고 paired/층화 설계에 맞춰 계산 | 공개8산출물에는 해당 입력이 없다. 군별 집계평균에 임의 참가자 행을 만들지 않음. 필요한 원표 필드는 future-study.md의 activity/submission/quality/rework를 참조 |

## 색인에 넣을 한 줄

AF-RES-034 — 원문30개·22연구군/26실험에서 짧은 사람 과제의 시간·품질 비교를 확인했으나, 링크 단독효과와 첫 채택 뒤 재작업 노동 절감량은 미확인; 검색·선택 단축이 총시간으로 이어지지 않는 반례와 산출물8/엄격7·시간raw0의 한계를 고정함. 결과0fe0ae4510e0052031919c748972dcf4bd4a7cbc.

## 가장 중요한 약점 세 건과 다음 조사

| 가장 중요한 불일치 또는 약점 | 근거 자료 주소 | 영향을 받는 결론 | 다음 조사 제안과 첫 자료 |
| --- | --- | --- | --- |
| 첫 채택 뒤 되돌린 결정·실제 수정 노동의 대조 관측0 | [Unakite pp9–10](https://lxieyang.github.io/assets/files/pubs/unakite-uist-2019/unakite-uist-2019.pdf), [NCQ §10](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf) | 제품의 장기 재작업 절감량은 미확인 | future-study.md의 첫채택SHA–후속재검 연결표와 동일요구 품질루브릭을 먼저 고정. 자유검색 대 근거카드의 두군·두시점 비교에서 최초+수정 노동과 전원 최종품질을 함께 판별. 이 시험은 아직 시행하지 않음 |
| 완료자 선택·넓은 품질 구간·원판 분모/표 불일치 | [eXoaDocs TablesX–XII](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf), [McLaren 열람 조판본](https://www.cs.cmu.edu/~bmclaren/pubs/McLarenVanGogEtAl-Efficiency%20of%20WE-CHB016.pdf), [Strata Table2](https://lxieyang.github.io/assets/files/pubs/strata-cscw-2021/strata-cscw-2021.pdf) | 전체 배정자의 동등품질 시간차와 해당 CI | 먼저 McLaren 최종 출판판/정오표의 ErrEx·TPS n을 열람판과 대조. eXoaDocs 사람별 문서로그–테스트결과 조인과 Strata Deep 개인별 채점열이 확보되면 보류한 분모·품질판정을 갱신 |
| 원산출물의 정확 제공판과 검색 포괄성 미확인; 엄격 자료7·시간raw0 | [NCQ instructions 고정판](https://github.com/Brittany-Reid/node_code_query/blob/ce14f193f7014c120f04619826cb251818d99b0e/docs/instructions.md), [CodeMend lab 준비본](https://github.com/ronxin/codemend/blob/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d/codemend/models/user-study-prepare-0405.ipynb) | 자료 최소수의 좁은 해석·실험 재현·문헌 부재 주장의 범위 | NCQ 실제 제공문서 commit과 CodeMend 최종bar/실제5쌍 매핑을 먼저 확인. 검색은 SCOPE의 고정 질의·연도·정렬 첫30 export를 확보해 기존1066심사행과 대조하며, 이는 검색범위 판정만 갱신하고 기존 사람 표본을 늘리지 않음 |
