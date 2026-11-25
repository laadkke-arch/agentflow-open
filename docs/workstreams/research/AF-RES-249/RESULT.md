| 과제·조건 | 링크 공개 전 산출물 | 공개·사용·교체 근거 | 독립 품질·인수 기준 | 분모·결측 | 설계 근거 URL |
|---|---|---|---|---|---|
| A-E | 중립 자유회상, runs 설계/코드, t0 seal | 0분 A1/A2, viewport/open/explain/try/same actor diff, t12−·t24 | A0–A6, 원본 불변, 독립 검수·인수 hash | 예정 12, 1기6; 실제0; 결측 아직 적용 전 | https://docs.python.org/3.12/library/itertools.html#itertools.groupby ; https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf |
| A-L | 동일 요구·seal | 12분 직전 동결 후 동일 카드; 자력 검색·스니펫 별도; 동일 actor diff | 동일 A 벡터/인수 | 예정12, 1기6; 실제0 | https://docs.python.org/3.12/library/collections.html#collections.Counter ; https://pmc.ncbi.nlm.nih.gov/articles/PMC6667942/ |
| B-E | 중립 회상, insertion_index 설계/코드 t0 seal | 0분 B1/B2 제공; 동일 페이지에서 두 후보 보일 수 있음; t12−·t24 | B0–B7, 동률 뒤, 빈 입력, no mutation; 독립 인수 | 예정12, 1기6; 실제0 | https://docs.python.org/3.12/library/bisect.html ; https://web.cs.ucla.edu/~miryung/Publications/icse2019-examplestack.pdf |
| B-L | 동일 | 12분 직전 freeze, 카드 제공; 오염/자력 검색 유지 | 동일 B 벡터/인수 | 예정12, 1기6; 실제0 | https://github.com/python/cpython/blob/v3.12.0/Lib/test/test_bisect.py ; https://pmc.ncbi.nlm.nih.gov/articles/PMC2844943/ |

표 1: 한 행=과제×정책 조건, 총 4행. 예정 48 배정, 24명(1기 24, 각 cell 6). 배정 전이라 예정 좌석 미배정, 실제 로그 0. 실제 결측률은 정의 불가. 두 과제의 결과를 합친 후보 행 수가 사람 분모가 아니다.

| 행동기록 사례 | 사전 인지 근거 | 관측 행동·대안 설명 | 허용할 주장 | 뒤집는 추가 증거 |
|---|---|---|---|---|
| K (합성) A1 | 자유회상에서 이전 사용 명시, 같은 groupby 코드 seal | 0 제공, 1 open; 같은 hash; 상기 가능 | 알려진 방법 유지; 인수는 합성 통과, 교체 N | actor provenance 누락이면 사용 귀속 보류 |
| N (합성) B1 | <=x 수동 구현, 명시 API 모름; 효과는 이미 앎 | 0 제공, 2 open, 5 저장, count→right; 다른 경로 미관측 | 특정 API 첫 접함과 일치, 구현 교체 Y, 합성 품질 통과; 개인 인과/새 개념 확정 아님 | 이전 right 코드·자력 선행 노출→known/독립; 타인 수정→교체 U |
| R (합성) A2 | 수동 방식, Counter 사전 지식 U | 12 제공, 13 열람, 비연속 반례 이유로 거절; 동일 hash | 열람·거절, 교체 N; 기존 코드 합성 인수 | 새 Counter 보조 도입 저장 증거→변경 재판정 |
| F (합성) B2 | 수동 count, 명시 API 낯섦; 적합 조건 U | 12 제공, 13 열람, 16 left로 교체; no-tie 예시만 테스트; B2/B3/B6/B7 실패 | 교체 Y, 이름 발견과 일치, 이해 불충분, 인수 N | 이후 right로 수정→별도 버전; rollback→최종 비채택 |

표 2: 한 행=합성 candidate×동일 artifact 계보, 4행, 실제 관측·실험 분모 0. 원행 worked-traces.csv K/N/R/F; trace-artifacts.jsonl 각 3 checkpoint. 시간/인수는 가정. 독립 검토 실제 미실시.

## 결론의 범위
**설계로는 구별 가능, 개인의 내적 미인지와 링크의 개별 인과는 확정 불가.** 동일 사건 안에서 봉인된 사전 지식·실제 URL 노출·동일 작성자 실제 구현 교체·독립 품질과 인수의 네 종류를 이어야 한다. '처음 접한 특정 API와 일치', '기존에 알던 방법', '조건을 새로 이해', '근거 미확인'을 차원별로 출력. 실제 표본은 0명, 배정 0, 실제 행동 사건 0, 실제 품질 실행/독립 검수 0; 예정 24명/48 배정은 관측 분모가 아니다. 네 합성 사건은 가정된 시각·검수·인수에 대한 한 작업자의 손 판독. 두 단위의 지연 공개 절차, 시험·빈 양식, 동일 기능 단위 원자료와 역전 조건을 완성했으나 실제 효능·노동 절감은 측정하지 않았다.

## Q1. 사건 인정 기준: 제공 ≠ 이해 ≠ 교체
236의 M1, M2, M3 chain 및 S1 supplementary를 비교. [chain.csv 고정](https://github.com/laadkke-arch/agentflow-open/blob/538cb1f04c83ae2dbf79be7d4fc91b27f818baef/docs/workstreams/research/AF-RES-236/chain.csv) M1~M3, S1; [rivals.csv](https://github.com/laadkke-arch/agentflow-open/blob/538cb1f04c83ae2dbf79be7d4fc91b27f818baef/docs/workstreams/research/AF-RES-236/rivals.csv) 첫 M1~M3, S1, R7. M1 링크 뒤 유용성 언급에도 triangle strip 필요 남음, close는 링크 이전. M2는 버튼 이미 사용, 설명을 읽고 오해 수정하나 구현 교체 없음. M3 다른 follow-up 요구에 맞는 미래 기대, 타인 종료. S1은 이미 문서 읽음, 실제 시도 실패, 권고자의 zip은 원작성자 산출물이 아님. 본층 3 URL(40 중), 직접 저자 성공 교체 관측 0/3은 사건 관측 부족이지 실제 무사용 3명 아님. 225는 236 인계 및 이번 brief의 같은 사람 변경/추천 URL 결손만 활용, 별도 새로운 원조사 없음. 세 선행 작업의 빈 칸을 서로 이어 한 완전 사건처럼 제시하지 않는다.

[D01 Blueprint](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf) 연구 화면/평가 pp.517–518, 예제 origin 유지와 paste까지 시간은 유용하나 붙여넣기는 정상 작동/인수 아님. [D05 Assieme](https://raphaelhoffmann.com/publications/282-hoffmann.pdf) L198–235, 73/90 tool tasks 외부 페이지 방문 없이 완료, preview는 실제 보임과 incidental hover 섞임. [D11 Holmes et al.](https://www.cs.ubc.ca/~rtholmes/papers/icsm_2009_holmes.pdf) §3.1–3.2, 40 inspected /14 attempted integration, 탐색·선택·통합 실패 분리. [D03 SnipMatch](https://joelbrandt.com/publications/wightman_uist2012_snipmatch.pdf) 평가의 snippet 선택·삽입을 재사용/상기/취소와 분리.

| 단계 | 최소 관측 | 누락·반례 |
|---|---|---|
| 제공 | candidate_id, recommendation_id, URL, 발송 actor, 수신 assignment, time | 제공만; 아직 화면 안 보일 수 있음 |
| 보임/열람 | first_content_visible(제목/스니펫/hover/본문), 실제 section, open/close, resolved URL, content hash/판 | click 없이도 보임; hover는 읽음 아님; 동일 B 페이지의 두 anchor 간 우연 노출 |
| 이해 | 정답 동결 후 요구 조건과 반전 사례 설명 또는 적용 증거 | 용어 인지뿐/자기보고 오류; F 동률 오해 |
| 시도 | 편집·시도/테스트 원행, actor, 후보와 의도 | 코드 복사/실패/취소도 시도 가능 |
| 실제 교체 | same actor+assignment+session+artifact_id, parent/child bytes SHA256, 기능 diff, 저장 시간 | 초기 계획만→첫 구현; 리팩터; 타인 수정; 링크 전 변경 |
| retained | t12−, t24, terminal hash와 변경 형태 | 중간 교체 뒤 되돌림은 최종 비채택 |
| 품질/인수 | blind alias, test receipts, 독립 reviewer+acceptor/정확 hash+기준 | 테스트 통과와 별도 운영 인수; 승인 문구만/다른 버전은 U |

'링크 후 처음 알게 된 특정 방법과 합치하며 실제 구현이 바뀜'은 사전 해당 지식 부재를 지지하는 증거, 노출의 시간 선후, 본인의 설명, 실제 변경과 대안 경로 검토가 합쳐진 경우에만. 실제 관측의 직접 연결이 하나라도 비면 그 주장을 보류. 개인에게 노출이 없었다면 바꾸지 않았을 반사실은 관측할 수 없음. 배정 효과와 개인 원인 주장 분리([M01 AIR §2](https://users.nber.org/~rdehejia/%21%40%24AEM/Topic%2004%20IV/readings/angrist_imbens_rubin_JASA_1996.pdf)).

## Q2. 첫 지식 측정
[D02 Examplore](https://glassmanlab.seas.harvard.edu/papers/examplore_chi18.pdf) Table1/2, 사전 API familiarity와 과제 API를 미리 알려주는 훈련. 16명, Map 비슷한 구조 경험 12명, SQLite 6명, findViewById 3명; 즉 결과는 이미 특정 API를 알려준 탐색/이해, 이름의 첫 발견 아님. [D07 Web use](https://hci.stanford.edu/publications/2009/webUseStudy/brandt_chi09_webuse.pdf) 관측에서 학습·확인·기억 환기를 구별. [D10 Find Unique Usages](https://arxiv.org/pdf/2005.11474) §III training에서 4명 중 3명이 tool 몰랐다고 보고했으나 훈련 이후 사용, 탐색 조건의 효과와 처음 발견 다른 질문. [P01 METR README](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/README.md#L29-L40)의 1–5 task exposure는 과제 유형 친숙도이지 방법명/적합 조건 지식 아님.
대안 비교:
- 사전 후보명 yes/no는 인식 측정에는 편하나 후보가 힌트가 됨. 본 실험 제외. 자유회상은 누락·표현차·검색 힌트 효과 가능; 무응답은 U. 봉인된 비유도 답변+기존 설계/코드는 적극적 prior 증거. 동일 효과를 수동으로 구현하는 사람은 원리를 알 수 있어도 API 이름/실제 사용을 모를 수 있음.
- 사후 자기보고는 기억 재구성·요구 특성·성공 후 합리화 가능. 동결 이후 짧은 질문과 반전 입력으로 조건 이해 확인; 사전 지식의 양성 evidence가 있으면 사후 부정과 충돌 기록, K 또는 U.
- prior dimension별 K(양성), NAME_ONLY/CONCEPT_ONLY, N_CONSISTENT(구체적인 미인지 진술+봉인·사후 정합), U(회상 없음/충돌/불완전). N 사례는 이름/표준 API 사용의 새 학습과 일치, upper-bound 효과는 사전 알고 있음. R은 Counter 자체 prior U. F의 이름 새 접함과 fit 오해 동시 가능. 기존 방식인 K라도 새 조건만 배우는 반례를 별도로 인정.
- baseline 질문도 전략 생성/주의 변경을 유발할 수 있어 두 조건 동일, 기록. 별도 연구에서 질문 없음/자유회상/이름 질문 요인 실험으로 반응성 추정(본 pilot에서는 추가하지 않음). [F01 Leahy](https://dalyresearch.engin.umich.edu/wp-content/uploads/sites/237/2020/12/Leahy_Daly_McKilligan_Seifert-Design-Fixation-From-Initial-Examples-Provided-Versus-Self-Generated-Ideas.pdf) 방법의 자체 초기 아이디어 조건은 후보를 보여주지 않아도 고착 가능성. 내적 지식의 부재를 보증하지 않음.

## Q3. 지연 공개와 통제
protocol.md §2–3 및 forms.md. 등록 시 task 순서와 timing sequence를 은폐 할당, first task만 알려줌. baseline 6분 중립 요구/회상/설계·코드 봉인 뒤 t0 정책 공개(E); t12− 동일 snapshot 직후 L에도 공개; t24 동일 freeze. 두 카드 동일 외형·순서 무작위, E/L 동일 자유 검색·시간·편집기. 검색 자체 발견과 snippet first exposure/오염은 기록하고 배정 유지. 같은 시간 창의 비교를 1차(24 배정, 4 cell 각6)로 사전 지정. 후반은 E/L 모두 추천 제공됨: 노출 유무가 아닌 timing history. 2기 24는 순서와 carryover, 사후 질문의 학습, 반대 타이밍 추론, 특정 API 선행 학습이 있을 수 있으므로 별도 탐색. 차단된 자원 policy 및 사용자 실험 이탈 기록. 
[D05 Assieme](https://raphaelhoffmann.com/publications/282-hoffmann.pdf) L206–212 Latin square order effect; [D06 ExampleStack](https://web.cs.ucla.edu/~miryung/Publications/icse2019-examplestack.pdf) §VI within-person 2개 task/15분, control 자유 검색, 4 task×order 균형. [M02 Dwan crossover](https://pmc.ncbi.nlm.nih.gov/articles/PMC6667942/) first-period post hoc 선택 지양, 상관/period 명시; [M04 Moher CONSORT 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2844943/) items 9–11 은폐 배정과 assessor masking 별개. 2025 판 직접 열람 실패(대체 2010 원문; 최신 기준 주장 아님). 
설계 대안: 1인 1과제 독립 4 cell 본실험이 carryover 감소, 같은 사람 비교 손실 및 모집 증가. 24명 pilot은 사건 capture feasibility/판독 신뢰도 평가, 유효성 검정력 산정 아님. 참가자간 확산을 실험 환경에서 제한하나 외부 학습 추적 한계. 시간과 사전 질문 모두 통제되더라도 카드 시점이 동기/주의·대체 후보 고착에 영향을 줄 수 있음. 개별 click의 인과효과를 IV로 추정하지 않음(M01 exclusion/monotonicity 미확인).

## Q4. 동일 품질, 규격과 반전
[T01 groupby](https://docs.python.org/3.12/library/itertools.html#itertools.groupby) key change와 공유 iterator, 정렬하는 문서 예시는 A 순서를 바꾸므로 이 과제에는 부적합; [T03 tests](https://github.com/python/cpython/blob/v3.12.0/Lib/test/test_itertools.py#L812-L830) empty/flattened sequence. [T05 Counter](https://docs.python.org/3.12/library/collections.html#collections.Counter) global tally, A2 적합 실패; 첫 등장 순서 보존은 떨어진 run 보존과 다름. [T02 bisect](https://docs.python.org/3.12/library/bisect.html) left/right split, x에는 key 미적용; [T04 tests](https://github.com/python/cpython/blob/v3.12.0/Lib/test/test_bisect.py#L35-L119) empty/repeated ties; [T06 pure Python](https://github.com/python/cpython/blob/v3.12.0/Lib/bisect.py#L21-L100) 비교 차이, 실제 C 구현 미실행. 
A A2 [('a',1),('a',2),('b',3),('a',4)]→[('a',[1,2]),('b',[3]),('a',[4])], 빈 [], 교대 키·0·중복 payload. B [1,2,2,4], x2 right=3/left=1; 빈 0, all equal right len/left0; no-tie 두 API 같은 값이므로 단일 정상 예시로 적합성 판정 금지. 두 함수의 입력 불변, 반환 type/내용·순서. 정답 수작업; 별도 코드 실행 담당 verify_vectors.py로 7+8 고정 벡터 실행. A 수동 루프/적합 groupby, B 선형 count/이진탐색/bisect_right 모두 허용. 시간제약을 알고리즘 우열이나 API 사용 여부로 채점하지 않음. 숨은 반전 입력/기준을 배정 전 고정하고 참가자에게 보여주지 않는다. 실제 API 문서 3.12.16과 테스트 태그 v3.12.0은 같은 minor 다른 patch; 동일 계약이라 설계했으나 실제 runtime/판 대조 미확인. B의 두 링크 같은 문서라는 약점은 노출 provenance로 별도 보류. [D04 Buse & Weimer](https://web.eecs.umich.edu/~weimerw/p/apidoc-icse12-final.pdf) §VII 154 raters, 35 paired examples rating은 preference/utility 평가이지 요구 통과 아님.

## Q5. 동일 개발자의 동일 기능 산출물 + 연구들이 실제 남긴 키
기존 연구 원자료의 관측 단위를 혼동하지 않기 위한 대조:
| 출처 및 위치 | 실제로 있는 공개/보고 키 | 이번에 여전히 필요한 키 |
|---|---|---|
| D01 Blueprint pp517–518 | 예제 origin/붙여넣기/과제와 시간, 실험·대조 | 사전 지식의 4차원 및 원본의 실제 전후 hash·독립 인수 |
| D02 Examplore Table1/2, P06 [기본 자극](https://github.com/UCLA-SEAL/Examplore/blob/be93aa2520b640412a41fbde57c09a6fb53c0fe4/code/meteor_app/private/findViewById.json) 100 records, ID0 | 연구 참가자 응답/조건/순서, stimulus dataset/exampleID/url/rawCode/focalAPI·guard/check/offset | 자극은 사람 행동 아님. 실제 code replacement join, doc exposure receipt, reviewer time |
| D03 SnipMatch 평가 | 검색/선택/삽입/시간 및 사용 세션 | 초기 기능 hash, prior·retained·인수 |
| D04 paired rating | example pair와 선호/평가 | 작성자 전후 산출물 없음 |
| D05 Assieme §study | ParticipantID, task order, query/time, page/preview | actual code compile/replacement 없음, prior/acceptance |
| D06 ExampleStack Table II, [P03 protocol](https://github.com/tianyi-zhang/ExampleStack-ICSE-Artifact/blob/1252ce53bce9d20b36fe9c60a434e23d3e880974/Datasets/README.txt) §2 | P5-A 등 task order/유형별 adaptation/time, clone URL/timestamps/whole file; 629 explicit-reference groups, 14124 variation groups | clone coincidence 가능; adaptation corpus timestamps 없음; same actor prior/edit/acceptance sequence 아님 |
| D08 [Sadowski logs](https://storage.googleapis.com/gweb-research2023-media/pubtools/pdf/43835.pdf) §3.1 | 사용자/타임스탬프/query/click/file/tab 등 집계·session; 27 participants/394 surveys | session segmentation≠stable artifact, prior/integration/acceptance join 없음 |
| D10 Find Unique Usages §III/V | P1..P4, C1..C6/E1..E6, training/feature/elapsed, independent tool discovery 사례 | 링크/해시/전후 저자·독립 검수 로그 없음 |
| P01/P02 [METR CSV](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv) header, lines2–27 | dev_id,issue_id,ai_treatment, prior exposure, initial/post review author min | assignment→추천→전후 artifact→reviewer→acceptor 키 없음 |

P06의 데이터 자체(100 JSON records, ID0 exact keys)를 열고 P07 code/README와 P08 server loader를 대조. ActionLog collection 선언은 실제 사람이 남긴 로그라는 증거가 아님. 공개 자극의 당시 실험 exact version 일치 미확인. D06의 raw multiGB adaptation archives는 열지 않았고 데이터 구축/파일 layout 원문만 확인. [P03] timestamp filtering은 우연 clone의 가능성을 줄이지 없애지 못함. 동일인 237 cohort 및 URL이 있는 236 chain도 독립 사건이다.
필수 join: event_id·actor_id(role)·participant_id·assignment_id·session_id·task_id·candidate/rec ID·resolved URL/판 hash·stable artifact_id·pre/post raw SHA256·parent hash·semantic diff 및 actor-authenticated save receipt·ordered UTC/mono uncertainty·prior evidence IDs·post reason·alternative path·test receipt·reviewer/acceptor IDs, same hash/rubric. 서로 다른 사람의 코드를 결과로 연결 금지. 같은 bytes면 같은 내용이지 동일 저자라는 증명 아님. 이름이나 감사/종료/병합만으로 인수 추론 금지. 
필수 키별 결손 문구: URL 없음 → 추천 출처 미확인; 제공만 → 열람/이해 미확인; prior 없음 → 사전 미인지 미확인; pre hash/actor/diff 누락 → 동일 작성자의 교체 미확인; final hash 누락 → 최종 유지 미확인; reviewer id/rubric/result 없음 → 독립 품질 미확인; acceptor 없거나 버전 다름 → 해당 산출물 인수 미확인. 
forms.md 및 65-field dictionary, worked-events.jsonl, worked-traces.csv, trace-artifacts.jsonl 및 trace-source-fixtures.jsonl에 4 사례의 mock raw bytes·content hashes·가상 시간과 사건 ID/역할 연결. mock source hash는 원문 캡처가 아님. 실제 문서 판은 future runner가 별도로 캡처. 실제 인증/채점/인수 시행 없음.

## Q6. 제작자·외부 검수·경과 비용과 분모
[237 cohort](https://github.com/laadkke-arch/agentflow-open/blob/0cd0389a47514c81d95ed2b2cd7e42e1efe84ba5/docs/workstreams/research/AF-RES-237/cohort.csv) 12 rows, dev_id655 전부; 6/6, post author 0분 관측7, reviewer_acceptance_key UNKNOWN 12. 예 issue3 initial170 post30 author min; issue5 422/0; issue1 232/10. [237 evaluation.csv](https://github.com/laadkke-arch/agentflow-open/blob/0cd0389a47514c81d95ed2b2cd7e42e1efe84ba5/docs/workstreams/research/AF-RES-237/evaluation.csv) review, rework, acceptance, effort_ledger, termination을 분리. METR regression 재계산하지 않음. [P01 README](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/README.md#L29-L40) 정의는 둘 다 작성자 시간. 작성자 POST=0은 외부 검수 비용 0이 아님. 
전체 표: primary window all-assigned N; condition별 완료·미시작·포기·오염·미열람·known·replacement Y/N/U·quality pass/fail/U·인수·비용 observed/U. 성공자 조건부 표는 별도, 인수율과 함께 제시. 미제출 cutoff에서 인수 실패, 교체 U; 실제 로그로 확인한 0만 0. 보류/pending과 unknown 구분. 배정 전 VACANT; no experimental observation, 0/0 undefined. 
제작자 pre/search/impl/test/rework, reviewer/acceptor active interval별 초→분. 동일 actor overlap union, 다른 actor 동시작업은 합산; 대기 wall elapsed는 사람시간 아님. 검수 2인/판독 연구 overhead와 실제 운영 검수 부담 분리. 후기 48h 공통 cutoff, 최대 15분 author rework와 reviewer 10min/version 2round 계획. 역할·stage별 누락 관측; 비용합 unknown이면 총 노동 절감 보류. 성공자 조건부 평균과 all-assigned 평균/합·cost per accepted(accepted=0일 때 NA). [M03 Lee](https://www.princeton.edu/~davidlee/wp/trimbounds.pdf) 항상 관측층 monotone selection 가정 안 맞을 수 있으므로 간단한 binary worst/best bounds와 조건부 별도 보고. 
네 합성의 가정 노동 K15,N20,R17,F19 person-min, 성공3, 총71/3≈23.67 min/accepted; 성공자만52/3≈17.33. 이는 계산 예시, 이른 제공 효과도 실제 시간도 아님. 작성자 4분 절감하고 reviewer 9분 증가하는 역전 사례를 revisions.md에 남겼다. 관측된 0·NA·누락을 조작하지 않는다.

## Q7. 네 합성 사건 및 다른 분야의 경쟁 설명
F01 초기 제공 vs 자체 생성, binary similarity, 2 coder; [F02 Smith et al.](https://people.it.tamu.edu/~stevesmith/SmithCreativity/SmithWardSchumacher1993.pdf) 원자극/특징 coding, 예시 특성 사용은 경고나 지연으로 사라지지 않을 수 있음; [F03 Chrysikou & Weisberg](https://www.researchgate.net/publication/7517400_Following_the_Wrong_Footsteps_Fixation_Effects_of_Pictorial_Examples_in_a_Design_Problem-Solving_Task) Table1 physical similarity/reproductive features, warning 조건 효과; [F04 Jansson & Smith](https://student.cs.uwaterloo.ca/~cs449/w18/Jansson%26Smith1991.pdf) experiment2 fig3/table2 원도면과 결함 채점. 31명 control15/fixation16; overflow 없는 디자인 비율 17%/54%, 높은 유사성 7%/50%. 분모는 디자인이지 사람의 첫 인지 확률 아님. 산업 디자인의 물리적·시각 자극과 코드 문서 이해는 다른 construct; 서로 반대 결과가 가능한 경고의 효과도 software로 일반화 금지. [D10](https://arxiv.org/pdf/2005.11474) §V.B 첫 결과에 집중, 양 군 자력 inline 사용 발견(각1명, 17/13분). 
관점별: 처음 보는 개발자에겐 용어/적합 조건을 이해해야 발견 의미 있음; 이미 알던 개발자는 확인/상기만으로도 도움 받을 수 있음; blind 채점자는 API 대신 동일 명세/입력/산출물만; 검수 비용 담당자는 실패/재작업/후기 인수 시간까지. 새 URL이 무조건 좋은 방법이나 유효성은 아니다. 
손 적용 K: 동일 사전 groupby code→그대로, 사전 알고 있음. N: manual upper-bound→bisect_right, 특정 API novelty-compatible/implementation mechanism changed, baseline도 정확하여 품질 개선 주장은 거절. R: Counter 열었으나 실제 요구 불일치 알고 거절, 기존 코드 정확. F: manual→bisect_left, no-tie 테스트만; 네 반전 실패, 변경됐으나 품질/인수 실패. 네 사례 코드 원문/해시와 78 synthetic event rows(가상 UTC 2000 날짜), 서로 다른 reviewer/acceptor, 명시 가상 labor. 실제 테스트 결과 대신 hand expected. 
C1–C8 및 N'/N''/N'''/R'/F'/F''/K'/missing 반전은 revisions.md. prior artifact에 방법 있으면 N 철회, self-search 선행이면 출처 뒤집힘, 다른 actor면 author replacement 보류, rollback이면 최종 미채택, wrong tie면 품질 실패. 최초 규칙 SCOPE와 최초 판정 OBSERVATIONS를 덮어쓰지 않고 수정 commit. 별도 독립 코더 미시행.

## 비용·대안·추가 분석
기본 24명 × 두 과제는 48 assignment; 과제당 baseline6+work24=30분, 참가자 연구시간 최대 60분+5분 휴식+사후 질문/동의, 후기 작성자 수정 최대 15분/assignment(실제로 0명). 검수 10분/version 최대2round 계획, 독립 QA 재판독 추가 비용 별도. 일정과 비용은 예산 제안이며 계측 아님. 1인1과제로 본실험 하려면 사전 pilot 판독 성공·분산·attrition을 확인하고 검정력/설계 비용 추정. 어느 분야에도 현재 제품 도입 효과를 이전하지 않는다. 사전 지정 1기 all-assigned rate/bounds, task strata 및 2기 exploratory; 사람이 링크를 미열람했거나 K여도 배정 유지. 
개발자/리뷰어는 같은 산출물의 활동 로그를 실제로 기록해야 함. 실험 실시 승인 후 동의/기록 범위를 결정하고 공식 Python URL의 응답 캡처/hash를 fix. 예상 비율, synthetic success counts를 실제 통계에 넣지 말 것. 
자료 수: sources.jsonl 41행; 산입 원자료 24 distinct work/file, lineage17, 종류 개발 검색/예제 7·프로토콜/데이터4·고착4·방법4·Python5. 보수적 D04 (example rating만) 및 P01(데이터 사전) 제외해도 22(6/3/4/4/5) 직접 원자료: P02 실제 anonymized data, P03 별도 construction protocol, P06 실제 stimulus data(3 distinct lineage의 공개 artifact). Python 5는 세 규격과 두 시험 파일, 같은 CPython lineage임. P06/D02, P03/D06, P01/P02 동계보, 논문과 자료를 별도 artifact로 세되 독립 실험처럼 세지 않음. 별도 source_id 41, 산입 외17(원문 보강/중복/실패), 실패 기록/화면 실패는 원장에 명시. 근거 수와 실험 사건 수를 합산하지 않는다. 직접 본 구간만 지원; 전체 파일/원본판·데이터셋 일치 보장 없음. 
결과 파일 재개: protocol.md, stimuli.md, verify_vectors.py, forms.md, event-dictionary.csv, worked-traces.csv, worked-events.jsonl, trace-artifacts.jsonl, trace-source-fixtures.jsonl, revisions.md. 실행/독립 리뷰는 미실시, 자체 재판독만. 

| 중요한 불일치 또는 약점 | 영향을 받는 판단 | 다음에 볼 구체적 원자료·검사 | 판정이 바뀌는 관측 |
|---|---|---|---|
| 사전 무응답/후기 미인지 진술은 실제 미인지 아님. N은 같은 upper-bound 원리 앎; 미리보기·자력 발견·과제 간 학습 혼합 | 최초 API/원리 발견과 링크 귀속, E/L 차이 | t0 free recall·원본 설계/코드와 source snapshot+first_visible+search receipts; 1인 1과제 병행 pilot; D10 inline 자력 사례 비교 | 동일 API 사전 사용/먼저 자력 노출 확인→K 또는 독립; 타이밍·로그 충돌→U; 반응성/전이 없음 관측 시 설계 신뢰도 증가 |
| 원문 3.12.16 vs fixed test v3.12.0; no tie 예시 동치, 두 B anchor 같은 페이지; Python 코드/runner 실제 동작 미확인 | 실제 구현 변경과 독립 품질/인수, 특정 API에 귀속 | CPython3.12.0 isolated runner verify_vectors.py, 원문 hash·visible section, 같은 artifact actor+diff receipts; 두 blind coder, rollback/third-party trace | A2/A5 또는 B2/B3/B6/B7 실패→불합격; both visible/actor missing→귀속 보류; 모든 벡터 및 해당 hash 독립 수락→인수 가능 |
| 237 후기 작성자 시간과 reviewer/acceptor active time 불결합, 성공자만 조건부 평균; 실제 pilot 미실시 | 전체 노동 절감, 실패비용, 운영 인수율 | forms.md 전체 배정 로그·actor interval·review/acceptance receipts 및 미열람/중단 포함; M03 selection assumptions 검토 | 검수 증가·실패비용 추가 시 maker savings가 역전; 독립 actor의 비용/인수 완결 및 all-assigned bounds로 방향 유지할 때만 노동 주장 |
