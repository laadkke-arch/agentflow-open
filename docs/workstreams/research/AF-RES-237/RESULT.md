표 1 — 한 행 = 초기 연구 공개 완료 issue 1건; treatment별 숫자순 처음 6건, 표본 12건. 0=AI 불허, 1=AI 허용(실제 사용 여부 아님). 두 시간 모두 같은 작성자 자기보고 분. 0은 관측된 원값.

| 실험·issue_id·조건 | 만든 사람의 첫 작업 시간 | 리뷰 뒤 작성자 시간 | 독립 검수·인수 키 | 원행 주소·단위 | 미확인 |
|---|---:|---:|---|---|---|
| Early·3·0 | 170 | 30 | 미확인 | [E02 L4](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv#L4)·분 | 실제 AI 사용·리뷰어 시간·인수 |
| Early·5·0 | 422 | 0 (관측 0) | 미확인 | [E02 L6](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv#L6)·분 | 실제 AI 사용·리뷰어 시간·인수 |
| Early·8·0 | 52 | 0 (관측 0) | 미확인 | [E02 L9](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv#L9)·분 | 실제 AI 사용·리뷰어 시간·인수 |
| Early·9·0 | 95 | 0 (관측 0) | 미확인 | [E02 L10](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv#L10)·분 | 실제 AI 사용·리뷰어 시간·인수 |
| Early·10·0 | 15 | 0 (관측 0) | 미확인 | [E02 L11](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv#L11)·분 | 실제 AI 사용·리뷰어 시간·인수 |
| Early·12·0 | 95 | 0 (관측 0) | 미확인 | [E02 L13](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv#L13)·분 | 실제 AI 사용·리뷰어 시간·인수 |
| Early·1·1 | 232 | 10 | 미확인 | [E02 L2](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv#L2)·분 | 실제 AI 사용·리뷰어 시간·인수 |
| Early·2·1 | 36 | 0 (관측 0) | 미확인 | [E02 L3](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv#L3)·분 | 실제 AI 사용·리뷰어 시간·인수 |
| Early·4·1 | 420 | 20 | 미확인 | [E02 L5](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv#L5)·분 | 실제 AI 사용·리뷰어 시간·인수 |
| Early·6·1 | 377 | 15 | 미확인 | [E02 L7](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv#L7)·분 | 실제 AI 사용·리뷰어 시간·인수 |
| Early·7·1 | 54 | 5 | 미확인 | [E02 L8](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv#L8)·분 | 실제 AI 사용·리뷰어 시간·인수 |
| Early·11·1 | 191 | 0 (관측 0) | 미확인 | [E02 L12](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv#L12)·분 | 실제 AI 사용·리뷰어 시간·인수 |

표 2 — 한 행 = 주장과 해당 분모; 처치·역할·품질의 서로 다른 추정 대상.

| 주장·분모 | 배정·누락 규칙 | 시간·품질 근거 | 반례·뒤집히는 조건 | 탐색기에서 추가할 측정 |
|---|---|---|---|---|
| Early 공개 완료 246=110/136, 16 dev; 허용 효과 | 이슈 정의와 두 예상시간을 먼저 등록; 무작위 허용; 제외·미완료가 남음 | E01 §2, E02; 완료 후 작성자 두 단계 합; E03 회귀 | 실제 사용별 선택은 랜덤 아님; 미완료 labor 빠짐 | 모든 배정 및 사전 제외, 실제 노출/사용 따로 |
| 12자리 기술량 (각 6), 같은 dev_id 655 | 숫자순 고정, 무작위 표본 아님 | E02 L2–13, 합 879 vs 1360분; 평균 146.50 vs 226.67분 | 같은 사전 예상 120분인 issue8/9/12 vs7의 결과 다름 | 요구 난도와 작업자별 block, 독립 표본 |
| 초기 발표 회귀 246 완료건, 시간비 | 후기 빈칸 그룹 평균 대체; log(total)~treat+log(noAI forecast) | E03/E04 0.188, HC3 CI 0.013~0.394; M04 대안 | arithmetic PPML +24%, unadjusted +33.7%; jackknife CI 0 포함 | 분모별 arithmetic person-min/accepted·geometric·CI |
| 독립 검수 및 동일 품질 인수 0/12 키 연결 | 초기 및 후기 작성자 시간은 12/12 연결, 독립 시간/인수 없음 | E01 G.2.1·C.2.7, E02 header; 연구 표본 품질 ≠ 인수 | 후기 0이라도 reviewer가 approval을 위해 일했을 수 있음 | reviewer_id, artifact revision, rubric, verdict, final acceptance |
| Late 공개 1134 중 완료 828, 유효 827 | complete/started/ditched 분리, 실제 상태 5종; 후기는 zero-fill (모형) | L01–04; incomplete 244, ditched 57, cheating 2, corrupted 3; started 900 | L196 포기인데 400분 보고; started 이상 5건 포함 | 사전 제외/포기/미완료의 비용, 이유와 추적 창 |
| 번역·검수 paired pilot 2+2건 | 교차 역할, AI 허용 RCT가 아님 | T03 Tables17–21; 79.17분 Pass, 66.36분 Fail | 더 빠른 검수라도 품질 악화; 연구 QA≠고객 인수 | 판·역할·재검·판정키, reviewer·acceptor의 실제 시간 |
| 리뷰 단계 경과·인시 구별 | S02~06 각각 독립 사건/원연구, Rigby 일부 재사용 | Google median <4h elapsed, Porter 22 person-hours/KNCSL | 기다리는 시간이 길어도 active labor 작을 수 있음 | 활동 구간의 합집합, 대기/경과 별도, 사람별 분 |
| 링크 추천 평가 목표: 모든 배정, 동일 요구와 기한 | 추천 허용 vs 통제 무작위; ITT, 미사용도 유지; 인수 실패 별도 | M01–03 방법; 설계 가설, 실측 아님 | 추천 오류·검수/재작업이 author 절감 초과 | 검색~최종 인수 비용, 인수율, 실패비용 및 한계 |

## Q1 무엇이 무작위 배정됐나
E01 v2 §2.1–2.4, §E.1 Table5, §E.3, G.2.1; E02 header; E04 Data Spec. 2025 Feb–Jun, 기존 OSS에 익숙한 16 개발자, 실제 246 완료 이슈. 이슈를 먼저 특정하고 예측 두 값(min) 수집 후 AI 허용 여부를 배정(초기 일부 block, 이후 coin); AI 사용을 강제하지 않았다. AI 허용은 여러 도구 선택 가능, AI 불허에서도 일반 검색·비생성 자동완성 가능. 따라서 허용의 정책 효과이지 특정 생성 모델 또는 탐색기 링크 효과가 아니다. E02 issue_id 1..246, dev_id 익명, ai_treatment 0/1; 실제 사용/노출 로그 없음. 화면 기록/부분 불허 위반 조사 E01 C.3.3 등: 실제 사용 가능성과 배정 동일시 금지.
완료 분모만 공개: 110/136; E01 C.3.3의 unfinished 7 불허, 6 허용, 별도 intentional drop 24 (난도/obsolete/타인 완료 등), G.6의 참가자 단위 제외(2명 repo 중단, 1명 cheating). 제외 범주 중첩·모집 전체/배정 전체의 고유 issue_id 공개 대응이 없으므로 246+13+24를 무조건 ITT N이라 하지 않음. 초기 246은 유효 완료 표본. M01: 비순응은 assignment와 receipt를 분리; 실제 사용만 비교하거나 IV 해석을 자동 허용하지 않는다. 보류: 비공개 개발자/저장소 추적 금지. 논문 판/저자 repo 판 모두 고정했으나 누락 규칙 완전 정합은 미확인.

## Q2 두 시간의 측정자·경계
E04 README + E01 G.2.1 PDF pp40–41(E05 화면 확인). 초기 구현시간=개발자 본인이 이슈 이해/문서 탐색/코딩/테스트/리뷰 요청 가능한 PR까지 작업에 실제 소비했다고 보고한 시간(분); review 응답 대기 제외. 후기=첫 review 뒤 같은 작성자가 수정/merge 준비, 충돌해결 등을 실제 작업한 시간(분); 예시 3일 대기/20분 수정이면 20분. 작성자의 노력, 독립 reviewer의 작업시간이 아님. 0은 수정이 없거나 reviewer approval only/no review일 수 있음. 즉 0은 실제 기록값, reviewer labor=0이 아님. 첫 active start timestamp와 정확한 pause/overlap log 및 작업전 탐색 경계 원행 미확인. 예측 시간 두 열은 실제 시간이 아님.
E02 full: 246 초기 관측/0결측/0zero, 후기 230 관측/16빈(7/9)/109zero(53/56); 표본 12/12 두 단계 관측, 후기 7 zero, 0빈. prior/resource 6 blank; raw 값 유지. README external_resource_needs 척도 1=없음 3=많음 vs G.2.1 지침 1=extensive 3=from memory 상반; 방향 적용 보류. 후기 결측은 코드 주석/논문 C.3.4 ~12%/27과 원행 6.50%/16 불일치. M03 aggregate 시간 일치가 activity segmentation 일치가 아님. 추가 시간의 종류/정의/측정자/기기/입력 버전 별도로 기록.

## Q3 작업 완료·제출·병합·인수
E01 §2.2, §C.2.7, G.2.1; E02 공개 header. 연구 지침은 review-ready PR, 이후 수정 시간을 받는다. 일부 PR이 study end 시 미병합일 가능성; 실제 merge status/PR URL 제출의 개별 익명 대응을 공개 데이터에서 확인할 수 없다. 후기는 merge-ready까지 작성자 수정, 승인/병합의 직접 판정 아님. C.2.7은 후기 수정 시간 집계/품질 proxy (대략 9 vs15분, 비유의), 자체 품질보고·부분 화면/코드 검토 등 별도 표본이며 동일한 12개 row의 rubric/verdict 아니다. 유의하지 않음은 품질 동등성 증명이 아님. 공개 12개에 author time 12, reviewer ID/time 0, final hash·merge/acceptance key 0 연결(실제 존재 여부 미확인). S01 별도 검수자 같은 changeset/accepted comment, S05 §5.1 snapshot→comment→rework→LGTM, S06 RTC와 CTR, D01 테스트 통과 조건: 승인 및 자동 테스트·계약 인수 차이를 보여줌. 동일 품질 인수 주장에 rubric_version, first/final artifact hash, review_round and actor, user accept/reject/defer and timestamp 필요. 연구용 평가자는 실제 인수자와 별도.

## Q4 분모·발표 모형·수기 검산
E03 고정 코드, E04 재현 출력, E01 §D.2, M04 Table2. 모델은 두 작성자 단계 합의 로그 ~ 배정 + log(predicted_time_no_ai). 후기 빈칸만 treatment mean impute; 0 유지. 0=1000/103=9.708738,1=1898/127=14.944882분. log positive row 조건 확인(초기 및 noAI forecast 모두 >0). exp(beta)-1은 보정된 로그 시간비의 변환(동일 조건 기하평균비 해석); 산술 평균비는 추가 오차분포 가정 없이는 다름. E04 0.188은 시간 **증가** 18.8%, 'speedup' 문자열을 감소로 뒤집지 않음; CI nonrobust [0.013,0.395], HC3 [0.013,0.394], cluster [0.016,0.390]. E01 v2 §D.2 HC3 설명 vs 코드 docstring paper nonrobust 표현 차이 확인 필요. 12자리 6+6 author mean 146.5 vs226.6667, +54.72% 기술량; noAI forecast 양성, 같은 dev에 몰린 nonrandom selection이라 전체 효과 추정 아님. 원행 전수 단순 계산(모형 실행 아님): 초기 합 9999/16257.5, post mean 대체한 total mean =9999/110+1000/103≈100.61 vs16257.5/136+1898/127≈134.49; 비 약 +33.7%. M04 독립 재분석(preprint) 기하 보정+18.8%, PPML 산술+24.0%, unadjusted +33.7%, cluster small-N jackknife interval [-0.2,41.6]로 0 포함, post n230; 회귀 독립 재실행은 Codex. Author alone, all assigned, all actors, cost per accepted를 별도 분모로. 상세 estimands.md. 
   
## Q5 완료만 남길 때
L01 data.csv 1134행 전체 직접 판독(별개 2025 late cohort); L02 codebook, L03 regression, L04 모집/선택. L02 createdAt=배정 date, lastModified=마지막 수정 date, 두 날짜 간격은 작업 시간 또는 인수시간 아님. pre estimatedTimeWithAI/WithoutAI vs post estimatedTimeOtherTreatment/effort. 초기/후기 active 분 field 동일하지만 완료/미완료/포기 상태에 따라 경계·결측 다름. 
| status | AI-disallowed N·initial blank·post blank | AI-allowed N·initial blank·post blank |
|---|---:|---:|
| complete | 368·0·0 | 460·0·0 |
| incomplete | 124·82·106 | 120·91·117 |
| ditched | 29·26·26 | 28·20·24 |
| cheating | 2·0·0 | 0·0·0 |
| corrupted | 0·0·0 | 3·0·0 |
Raw blank != zero; 전체 1134, 완료 828, 제외/미완료 등 306. 코드 complete-valid 827, started 900 (824 complete+71 incomplete+5 이상 상태; ditched drop), JS 조건 재판독만 수행. README 3 상태·cheating 제거 설명과 데이터 5 상태 불일치. L01 L3 incomplete allowed 24분 + missing post; L196 ditched allowed 200+200 보고(실제 작업 여부/오입력 미확인), 비용 0 가정 금지. L03 post zero-fill은 통계 가정, 관측 0으로 전환 금지; started 회귀도 합산 outcome, invalid status 명시 필터 없음. L04 10 returning +47 new, 보수 $150→$50, AI 없이는 작업 거부하는 사람/과제 사전 선택 및 동시 agent 때문에 시간 측정 어려움; 결과 신뢰 제한. Panel −18% CI −38,+9, new −4% CI −15,+9 (발표), 초기와 합산 금지. M02 항상 관측 stratum bounds 조건은 monotonicity가 필요하므로 추천이 쉬운 과제는 늘리고 어려운 과제는 포기시킬 가능성에서는 자동 사용 불가. D01 완료 70/95만 시간 비교(각35); D02 4867 field trials 완료 task rate의 다른 결과. 포기/미완료의 누적 시간, censoring window, 재시도, 대체 작성자와 이유를 원배정에 연결.

## Q6 두 역할 시간과 품질
T03 Temizöz thesis pp108–112 Tables17–21, 직접 원표 재열람(텍스트 표, 스크린샷 timeout). 교차 작성-검수 pair En1→Tr1 52.96+26.21=79.17 min, QA93.36% Pass; Tr1→En1 44.98+24.73=69.71 min, QA95.02 Pass. En2→Tr2 47.45+18.91=66.36 min, QA66.39 Fail; Tr2→En2 67.53+42.41=109.94 min, QA64.52 Fail. Revision의 85% 기준, PE 75% 기준. En2 revision으로 68.46→66.39 악화. 이는 교차 pilot 2+2건의 연구 품질 판정이며 역할이 붙은 stage-sum을 계산할 수 있음을 보여주지만 evaluator 시간, 고객 인수 및 버전 hash 없음; 동일 산출물에 대한 HT vs PE 무작위 효과 아님.
T01 Terribile §Table5 산업 HT/PE 번역 WPH 330–820 vs530–1440, revision 1200–3870 vs1990–5540 범위; 언어쌍별 반전, CAT 2분 이상 무활동 제외. job별 동일 버전/actor/검수+재작업+납품 키 없음. WPH 평균 역수는 평균 시간 아님. T02 Plitt/Masselot 12 번역자 문장 시간 자동 수집, 검수자 노동·동일 인수 없음; T04 Robert 16 revisers 4 procedures keystroke logs: mono 짧아도 품질 낮음, 개별 원행 미열람. 
S02 Fagan 현장 검사/재작업 노동을 별도 기록, 23% 생산성/20 person-hours per KNCSL 결과는 다른 사건; S03 NASA 203 inspections 시간/결함 밀도와 pace, 품질 동등성 미확인; S04 Porter 88 inspections, median 22 person-hours/KNCSL와 elapsed 별도. S05 Google 9m reviewed changes, median 전체 review latency <4h; S06 AMD17.5h/Android20.8h 등 review interval, 일부 S04 데이터 재사용. 이 시간들은 author labor와 합산할 수 없다. 검수자 활동분, review 대상 hash, rounds, acceptance rubric/판정자, 재작업이 어떤 comment를 해결한 것인지 기록. 타 연구 효과는 탐색기 성능 추정치가 아니라 측정 설계 근거다.

## Q7 탐색기 평가 설계
evaluation.csv는 제안 스키마 및 대조. 같은 requirement/version, 난도 strata, 작업자 block; 모든 eligible 요청 사전 등록→추천 허용/숨김 랜덤화→동일 기존 검색 허용→노출·클릭·검증/채택 단계 기록. 노출 but no use는 원배정 유지. 대조군 자체 발견 링크도 source/time 기록. 결과 판은 독립 검수자가 동일 rubric로 blind 가능 범위 명시, evidence retrieval/review/rework 시간 별도; user/acceptor acceptance timestamp와 승인한 artifact hash 동일성 확인. 리뷰어가 추천을 보았거나 저자가 자체 검수한 경우 independent flag, blind 불가능 사유 기록. final status accepted/rejected/withdrawn/incomplete with horizon, 누락 원인. 같은 사람의 overlapping active intervals 합집합(중복 제거), 다른 사람 동시분은 합산; elapsed 별도. 동일 actor 다른 issue multitasking은 active segment allocation, 미배분은 unknown not duplicate. 비용은 시간분과 실제 모델/API/금전 별도. 
주요 지표: 원배정별 accepted fraction, 평균 누적 all-role active person-min per assigned at fixed horizon, cost/accepted = all assigned costs / accepted counts (실패 노동 포함), acceptance latency censoring, rubric defect/severity 및 escaped defects follow-up. Equal quality는 사전 noninferiority margin와 통계 CI 별도; 사용된 링크만 분리하는 secondary descriptive. 가상 counterexamples.md: author 80→40, reviewer 10→60, rework 10→15, accept5→5, all105→120; 처음 작업만 50% 줄고 총 14.29% 증가. 10 assigned each, 8 accepted×50+2 fail×200 vs10×80 → 800/800 total, per accepted100 vs80; 성공자만 50 vs80 방향 뒤집힘. 이것들은 실험 결과가 아닌 검증용 가상 입력.
추가 측정 비용(설계 예산, 실측 아님): 20 pilot tasks 2min 사전 입력/1min 노출확인/2min 단계 종료 태그/2min 인수 기록=140 person-min, 10% audit 2×10min=20 추가, 총 160min instrumentation overhead. 실제 reviewer work는 비용 결과에 포함하되 연구용 추가 blinded duplicate reviewer 시간은 별도 연구 overhead로 기록, 예산 20×15min=300min 가정; 자동 event instrumentation 개발/데이터보호 검토 미산정. 수동 time diary와 timestamp 보조 검증 선택. 동의, 최소 로그, 익명 키, raw artifact private if needed, 집계만 공개. 
대안: (A) 저비용 author-only + acceptance count, 총노동 주장 금지. (B) role ledger + matched blind reviewer and explicit acceptance, 권장 pilot. (C) 전수 time log 대신 random audit with sampling weights and missing bounds; 측정 반응성/동의 비용. 기존 AI 허용 처리와 링크 추천 처치는 분리. 

## 자료 분모 및 상태
원장 31행 중 23 비중복 원저작/원자료 단위 산입, 8 미산입(실패/중복/시간근거 부적합). 산입 early4/late6/software5/translation4/methods4, 16 고유 lineage_id. 23 중 D02/T04 원저자 초록만 직접(깊이 제한); full artifact/paper 기준 21. 16 lineage는 독립 사건 수의 근사 분류이지 합산 가능한 사건 N 아님: METR early/late 2 사건, Peng 1, Cui 3 field RCT, software 5 연구 lineages (Rigby는 Porter reuse 포함), 번역 4 연구 lineages, 방법 3 독립 lineages + METR 재분석은 동일 사건. 연구 내 복수 과제/프로젝트의 교차중복까지 제거한 독립 사건 수는 미확인. 계획 12/관측12/후기 결측0; 원 완료 246/초기246/후기230/결측16, 독립 검수·인수 키 0/12. 후속 1134 별도. 원장에 검색 결과 스니펫만 산입하지 않았고 PDF screenshot 실패를 성공으로 표시하지 않았다. early 5번째 별도 도구/지시 artifact 미확인(논문 부록 중복 제외), 최소 분류 하한 미충족 → PARTIAL. 핵심 12자리와 배정/시간 정의는 관측, 총노동/동일 품질 인수는 보류. 웹 역할 자체 판독만, 독립 검토/전수 회귀 미실행. 

## 추가 분석과 조건별 대안
Codex: 고정 early+late commit checkout, 원 CSV row count+header+blob SHA 재확인; 회귀 그대로 실행 및 complete-only/started/valid status 분리 민감도. 원본 CSV raw blank 절대 덮어쓰지 않음. E03 README 예상 0.188, cluster CI 0.016–0.390; 불일치면 package/version/std err/data missing audit. E01 v2 C.3.4 27과 16의 차이는 공개 commit history/저자 설명으로만 해소, 역식별 금지. 세 번째 actor/acceptance 없는 데이터로 labor 절감률 출력 금지. 추정량별 ratio 방향·단위·표본 명시. 원장 초록 수준 원자료 및 초기 독립 지침 artifact 보완 후 완료판정 재검토.

| 중요한 불일치 또는 약점 | 영향을 받는 판단 | 다음에 볼 구체적 자료·검사 | 판정이 바뀌는 관측 |
|---|---|---|---|
| E01 C.3.4 후기 결측 27/~12% vs E02 16/246=6.50%; README resource scale 반대 | 대체값·예측 보정·재현의 판 정합 | early repo history 및 author data dictionary/standalone study tool; fixed regression.py | 동일 버전 변환 기록과 척도 방향, 입력/출력 수 일치 |
| 독립 reviewer/acceptor 키 0/12, QA proxy/author rework≠total labor | 총노동 절감 및 동등 품질 인수 불가 | 익명 versioned review event + reviewer duration + acceptance record 또는 새 pilot | 동일 요구·판·역할·끝점의 두 조건 관측, 누락/실패 포함 |
| Late README 3 states vs 5 observed; started 5 invalid, incomplete/ditched 비용/selection | 완료자 비교의 일반화·분모 | L03 filter audit 827/900, preregister all assigned, separate selection bounds; early 독립 artifact 추가 | 유효 상태 규칙/모집·탈락 ledger 확인, 실패 비용/인수율 함께 보고 |
