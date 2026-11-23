# AF-RES-058 HANDOFF

- `task_id`: AF-RES-058
- `status`: **PARTIAL — 연구 조건 전체 충족으로 수용하지 않음**
- `worker`: web-pro; 실제 실행·통합 주체는 이 세션의 root AI, 보조 조사는 software_ir/adjacent/diagnostics AI
- `repository`: laadkke-arch/agentflow-open
- `branch`: work/research-af-res-058
- `owned_path`: docs/workstreams/research/AF-RES-058/
- `result_commit`: **4265e446b0e1a22022d68a6f989ebc1d504f3e84**
- `verification_commit`: **93f2a738c87390b73f48daa79097e5f2e8a7f126**
- `handoff_written_utc`: 2026-11-23T04:25Z 이후, 고정판 재열람·실제 session check 통과 뒤 작성
- 이 파일만 마지막 단독 커밋으로 게시한다. 자체 commit SHA·정확한 시각은 이 파일을 포함한 Git commit metadata를 따른다.

## 1. 먼저 열 파일과 두 필수 표

고정 결과는 [RESULT.md@4265e44](https://github.com/laadkke-arch/agentflow-open/blob/4265e446b0e1a22022d68a6f989ebc1d504f3e84/docs/workstreams/research/AF-RES-058/RESULT.md)다. 파일 맨 앞의 **「표 1. 여덟 고정 연구 자리」**가 첫 표, 바로 다음 **「표 2. 조건별 정오층·대비·결측 원장」**이 둘째 표다. 첫 표8자리, 둘째 표98행(조건별 정오44·대비32·결측/미실시22)이다. 그 뒤 판정·Q1–Q7·설계 대안·추가 분석이 이어지고 마지막 약점 표는 정확히3행이다.

조건별 계획/실제 분자·분모·단위·원위치·결손·다음 확인은 [acceptance-evidence.json@4265e44](https://github.com/laadkke-arch/agentflow-open/blob/4265e446b0e1a22022d68a6f989ebc1d504f3e84/docs/workstreams/research/AF-RES-058/evidence/acceptance-evidence.json)에 있다. 이 파일은 결과 고정 전 생성했으므로 최종 계약 검사는 pending으로 기록되어 있다. 뒤에 실제 수행한 검사를 미리 통과 처리하지 않았으며 그 완료 근거는 [final-verification.json@93f2a73](https://github.com/laadkke-arch/agentflow-open/blob/93f2a738c87390b73f48daa79097e5f2e8a7f126/docs/workstreams/research/AF-RES-058/evidence/final-verification.json)다. 검사 통과 뒤에도 연구의 PARTIAL은 유지된다.

상세 재현·손검산은 [reproduce.md](reproduce.md), Q별 근거·반대 자료·뒤집힐 조건은 [SELF_CHECK.md](SELF_CHECK.md), 원순번·탈락/코호트는 [frame.csv](frame.csv), 원 자극·동시 개입은 [stimuli.csv](stimuli.csv), 응답/차이는 [outcomes.csv](outcomes.csv)·[contrasts.csv](contrasts.csv), 자료별 열람·판·한계는 [sources.jsonl](sources.jsonl)이다.

## 2. 조사 결과와 수용 판정

**고유 심층 외부 1차 저작28개를 직접 읽었고 출처 기록109개를 남겼다.** 선별 방법만 읽은 자료까지 포함한49개 계보와 구별한다. 같은 논문의 부록/미러/개정, 같은 패키지의 README/CSV/노트북, 같은 코호트의 재분석을 중복 합산하지 않았다. 내부 인수 파일·검색·접근 실패·자가 생성 진단은 최소20개 수에서 제외했다.

| 요건 | 실제 확보·상태 |
| --- | --- |
| 여덟 자리 | 표에는8자리 보존. 실제 선정 A2/B4=6, A03/A04 미충원 |
| 선정 정식 사람 실험 원논문8 | 직접 읽은 정식 논문5. A02는 저자 poster만 읽었으며 원논문403; 독립 논문으로 승격하지 않음 |
| 별도 실험 자극/도구/프로토콜4 | 엄격한 독립 프로토콜 계보2. DrXAI/BIOS/MIMIC 도구3은 원천/모델 지원으로 별도 기록 |
| 저자 데이터/분석 패키지4 | A01, D01, D03, D04의4개 |
| 독립 반대/다른 분야 사람 실험4 | 진단 D01–D07의7논문 계보. 같은 논문 내 연구·재사용 참가자는 더하지 않음 |
| 정답 원천 지원 | Ott2011/2013+공식 데이터, BIOS 논문, MIMIC-NLE 논문, Cranfield의6개 |
| 선정 연구의 정오별 수락 원개수 | 식별한 셀0. 미확인·원종점 부재·설계상 오권고 부재이지 참여자0/효과0이 아님 |
| 진단층 원개수 | D01/D04 같은 원행에서 연결. 66개의 수락 셀·52대비에는 다른 조건/분석집합이 포함되므로 독립 연구 수가 아님 |
| 자체·동료 검토 | 소유 stream 작성자 재검토, 별도 AI의 통합 원장 감사/B03 재독, root의 D04 별도 재계산. 외부 인간 심사·참가자 복제 아님 |

28개라는 합계는 정식 선정5+poster1+프로토콜2+패키지4+진단논문7+정답지원6+모델도구3이다. 최소20개는 충족했지만 여덟 실제 연구·자료군 배당·주 결과 식별성을 충족하지 못해 PARTIAL로 인계한다.

### 원개수로 확인한 핵심 반례

진단 D04의 공개 분석 파일에서 `machine`과 `machine_and_heatmap`은 각각80개 익명 사람 키×20=1,600행이다. 두 조건 모두 정권고1,395·오권고205다.

| 종점 | machine | machine_and_heatmap | 기술 차이 |
| --- | ---: | ---: | ---: |
| 맞는 권고 수락 | 908/1,395 | 1,107/1,395 | +14.2652pp |
| 틀린 권고 수락 | 123/205 | 152/205 | +14.1463pp |
| 전체 최종 정답 | 990/1,600 | 1,160/1,600 | +10.6250pp |

따라서 전체 정확도가61.875%→72.5%로 높은 조건에서 오권고 거절률은40%→25.8537%로 낮았다. 원개수·분모를 다시 세어 저자 Fig3/4의 반올림 값과 대조했다. 무작위화 절차·원배정 전체 명단·초기 자기 답·실제 읽음은 미확인이라 **조건 간 기술 비교**로 남겼다. J1은 행연결 등급이며 인과 효과 등급이 아니다. 별도 무권고 `heatmap` 조건과 혼동하지 않도록 원키를 썼다. [고정 데이터](https://github.com/vivlai/deception-machine-in-the-loop/tree/7c5ae6bb4b7dcd5613e620e4731b9c3c67ed8285), [별도 검산](streams/root/independent-calculation.json).

정권고 수락도 늘었으므로 모든 식별 지표가 나빠졌다는 주장은 하지 않는다. D01 Amazon에서는 오수락이 감소하는 조건 차이가 있었고, D06 미로의 검증 가능한 경로 강조는 어려운 문제의 과잉 수락 감소를 보고했다. D07은 부분적 설명이 정권고 수락도 낮추는 비용을 보였다. 효과 방향을 설명 존재 하나로 일반화하지 않는다.

**사용할 제품 문장:** 전체 정확도·신뢰도만으로 오류 선별 개선을 판단하지 말고, 같은 후보·판·참값 규약에서 정권고 수락·오권고 수락·최종 정답·결측을 나눠 보아야 한다.

**보류할 문장:** 원문 링크를 실제로 읽게 하면 같은 소프트웨어 후보의 잘못된 권고를 더 잘 거른다. 확보 자료에는 실제 외부 원문 열람만 배정한 해당 비교가 없고 A층 및 원행 연결이 부족하다. 설치·총 노동시간·후속 재작업 효과도 추산하지 않았다.

## 3. 막힌 이유와 시도한 경로

| 남은 결손 | 실제 시도·확인 | 최소 추가 입력 |
| --- | --- | --- |
| A03/A04와 A02 정식 본문 | 정확 질의/페이지 한도/R0→R1을 결과 전 고정. A547 고유 DOI→관련32→날짜·DOI순30, ACM/ACL native와 사전 fallback. 후속 원문2개 회수 후에도 원순번7/8/9/22/26 방법과15 main-paper proxy 한계 잔존. A02 저자 poster만 성공 | 고정 순번 원문의 방법 전문, A02 정식 본문·배정·key. 다른 분야로 자리를 메우지 않음 |
| A01 권고 수락 D/A | 저자 고정 repo5batch·코드·별도 branch 목록·Brown 보고서·Cranfield를 직접 읽음. 559/459/67행과67 ID 연결, qrel25행·142/143 유일 제목 대응까지 확인 | 배포 SHA와 T/TA/TAB 조건표, 전체 impression/docID/rank, relevance 이진 규칙,150완료자 대응·최종 선택/철회 |
| B02 부분분모와 정정판 | KIT arXiv v3·Table3·Ott원천/공식 데이터 확인. publisher 정정 VoR 전문403·다른 미러404. no missing은 SEM 맥락, confidence 서술/표 방향 불일치 보존 | 정정 VoR와 초기 답/권고/참값/최종 답 공동표, 제외·배정명단 |
| B03 정14 대 그림50% | v5 Table1·§3.3·각주7·Fig3/5·AppendixC를 두 AI가 다시 판독. 정8/오6인데 정권고 수락+거절 몫50%;12개 포함을 입증하는 규칙 미확인 | Fig3/5 포함 마스크·가중 규칙·군별 정수 교차표 또는 공개 정오표 |
| B04 원개수·실제 노출 | 공식 ACL 본문/부록·화면·모형그림·BH·전문가 규약 확인. 연결 GitHub 고정판은14byte README1개, OSF shell/API 실패 기록. MIMIC-NLE package는 원응답이 아님 | 사람×영상×finding×조건×기간 배정과 전문가 정답·최종 답·결측, 정확한 분석 포함 규칙 |
| 외부 링크 읽기와 부품 선택 이전 | 제공 텍스트·강조·내부 corpus보기·자발 클릭·OnDemand/Wait/Update를 구별. 공개 참가자 실험 외에는 확장하지 않음 | 같은 후보·순위·판에서 설명/배정열람/실제노출을 구별하고 최종 응답을 잇는 기존 공개 자료 |

실패·탐색·취득과 읽음의 차이는 source/search/retrieval 로그에 있다. 접근 실패를 자료 없음의 증명으로 쓰지 않았고 비공개 원자료를 요청하거나 사람을 새로 모집하지 않았다. AF054의 eXoaDocs 집계/결합 실패와 AF038의 사람0명은 인수 사실이며 제외한 시계·개인 코드·6,200조합 재조사를 하지 않았다.

## 4. 재개 첫 행동과 필요한 입력·명령

**첫 행동:** B03 [AD-M26 원문 v5](https://arxiv.org/pdf/2209.11812v5) 및 논문의 공개 저자자료/정오표 경로에서 **Fig3/Fig5의 포함 마스크·가중 규칙·정수 교차표**가 제공됐는지 먼저 확인한다. 현재 원문을 다시 읽어12라는 분모를 추정하는 것은 진전이 아니다. 새 자료가 없다면 그 실패 경로·시각을 남기고 아래 A층의 기존 접근 제한 원문으로 이동한다. 저자에게 메시지를 보내라는 인계가 아니다.

원응답이 공개된 경우 필요한 입력 단위는 `participant_key, item_id, condition, period, AI_label, truth_label, final_label, inclusion/exclusion, skip/withdrawal`이다. B03은 선택14개 key와 Fig3/5 포함 규칙까지 필요하다. 이는 **필요한 스키마**이며 존재하는 파일의 열 이름이라고 꾸민 것이 아니다. 원 자료의 실제 codebook과 공유키를 먼저 대조하고 공개 개인행은 저장소에 재게시하지 않는다. 교차 집계만 나오면 정오층별 배정/판정가능/결측 D와 수락 A·최종정답 C가 직접 명시돼야 한다. 그 뒤 해당 stream 원장에 관측값을 기록하고 다음 기존 명령으로 통합·검산한다.

```bash
python -B docs/workstreams/research/AF-RES-058/assemble_ledgers.py
python -B docs/workstreams/research/AF-RES-058/assemble_outcomes.py
python -B docs/workstreams/research/AF-RES-058/build_tables.py
python -B docs/workstreams/research/AF-RES-058/build_acceptance.py
python -B docs/workstreams/research/AF-RES-058/validate_artifacts.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-058/manifest.json --fetch
```

새 자료로 행 수가 달라지면 `validate_artifacts.py`의 현재 수량 기대값은 증거와 함께 명시적으로 수정해야 한다. 실패를 없애기 위해 임의로 기대값을 바꾸거나 원 모집 결과를 소급 교체하지 않는다. 현재 셀을 다시 생성하는 명령은 없는 B03/B04 원행을 만들어 주지 않는다.

현재 확보한 진단 수치를 재현하려면 입력은 고정 Bansal/Lai SHA의 공개 CSV/GZIP이며, 전체 URL/해시/키/산식은 [reproduce.md](reproduce.md)와 `streams/diagnostics/input-receipt.json`에 있다.

```bash
python -B docs/workstreams/research/AF-RES-058/streams/diagnostics/reproduce_diagnostics.py --download
python -B docs/workstreams/research/AF-RES-058/streams/diagnostics/sensitivity_prefilter.py
python -B docs/workstreams/research/AF-RES-058/streams/root/verify_lai_and_bounds.py
```

위 집계는 이번 세션에서 같은 해시의 캐시로 실제 실행했다. 캐시 없는 환경에서만 `--download`가 필요하다. A01 패키지/Cranfield 감사의 정확한 명령·입력은 `streams/software/reproduce.md`에 있다. 재실행하면 집계 시각이 바뀌므로 수치·입력 해시로 고정판과 비교한다. 원 저자 앱 배포·R 추론모형 재적합·새 사람 실험·비공개 임상 재생은 미실시이며 이들로 누락된 정오별 원개수를 대신하지 않았다.

## 5. 실제 검증 결과

- 지정 `session start` 실제 실행: 2026-11-23T03:17:13.383527Z–03:17:19.656926Z, exit0. [session-start.json](evidence/session-start.json).
- 통합 불변식 검사: `validate_artifacts.py` 실제 exit0,228개 검사 PASS. 출처 계보,60선별/20자극/246결과/84대비,44주 결과/32주 대비/22주 결측,52개 원개수 차이, 모형/계획 분리, 끝 약점3행 등을 확인. [artifact-validation.json@4265e44](https://github.com/laadkke-arch/agentflow-open/blob/4265e446b0e1a22022d68a6f989ebc1d504f3e84/docs/workstreams/research/AF-RES-058/evidence/artifact-validation.json).
- GitHub 고정판 재열람: 2026-11-23T04:23:06Z, RESULT87,239bytes와 acceptance334,610bytes의 전체 내용을 읽고 신규 fetch의 Git blob 및 workspace와 일치 확인. RESULT SHA256 `ccb06745827ac4f3c336f6b7df0e80f6ed3a7c8a46e9626bbfdba0d6268b068d`; acceptance SHA256 `c98b45575b1c10c538a177fdf41bb056c3adba6a8dcfb85c595a01435be26b72`.
- 요청한 최종 명령 실제 실행: `python -B -m workbench.session check docs/workstreams/research/AF-RES-058/manifest.json --fetch`, 2026-11-23T04:23:06.847508Z–04:23:15.681702Z, **exit0 / status passed / freshness remote_checked**.
- 검사한 checkout은 결과 SHA `4265e446b0e1a22022d68a6f989ebc1d504f3e84`, 검사 시 최신 통합판은 `c0d55315c19dba047937969fdf9bc404d21cc33a`. 시작판을 최신 통합판으로 소급 바꾸지 않았다. 계약 SHA256 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc` 유지, `outside_paths`, `unmerged_paths`, `errors`는 모두 빈 목록이다.
- 검사 주체는 root의 제공된 cloud workspace 실제 CLI다. 연결된 다른 CI가 실행했다고 주장하지 않는다. 검사 경계는 Git 계약/소유 경로이며 제품 효과 검증이 아니다. 이 인계 파일 자체는 위 검사 이후 추가되므로 그 검사에 포함됐다고 말하지 않는다. 마지막 커밋의 단일파일 변경과 원격/로컬 HEAD는 게시 뒤 별도 Git 확인한다.

## 6. 시작·의존·원격 커밋

실제 시작판은 `chore/workspace-foundation@3f4d43b19cd76d56983e6f500eebe7010eb3fa51`이고 계획 입력 `8036b862a0f921196dca57e8532df606bf6f1de6`와 구별했다. 지정 AGENTS/STATE/DOT_AUTOMATION/RESEARCH_WORKFLOW/dot-control의 AF-RES-058 항목을 직접 읽었다. 의존 AF054 인계는 `425f64dda404b4e275acf4eae5ff9244eab36d37`, RESULT/endpoints/joins/bounds는 `377facae73f5e49677cb5719a05fdac457d8357b`에서 직접 인수했다. 증거는 [manifest.json](manifest.json), [inherited-inputs.json](evidence/inherited-inputs.json)에 있다.

| 묶음 | 원격 SHA | 실제 commit UTC |
| --- | --- | --- |
| ① 모집·채점 R0 | e87ebdce358541d8180e20bc0077706cae41ea70 | 2026-11-23T03:19:10Z |
| 결과 전 발견정렬 R1 | c47d8429ccad9885e7093771fe89ec09d8cc47ac | 2026-11-23T03:21:18Z |
| 결과 전 발견 목록 | 02dbcaa1cd8dad27b113e9a225ab1fc95b913a9a | 2026-11-23T03:24:45Z |
| 방법 선정·빈자리 고정 | 1ff924dc53dee8ff4b07fa1f1c25e7f601d72d95 | 2026-11-23T03:32:07Z |
| ② 조건·원 자극·참값 | 11ecea10235c018bebd2f5d4d36557f967d11843 | 2026-11-23T03:46:06Z |
| ③ 응답·교차 집계·반증 | f7c9b344aa2f5e8f2755828ba3e0849739d542b2 | 2026-11-23T04:03:50Z |
| ④ 필수 표·자체 검토·수용 원장 | 4265e446b0e1a22022d68a6f989ebc1d504f3e84 | 2026-11-23T04:21:31Z |
| 고정판 재열람·실제 검사 영수증 | 93f2a738c87390b73f48daa79097e5f2e8a7f126 | 2026-11-23T04:23:55Z |

셸 push는 최초에 자격증명 부재로 실패했고, 이후 연결된 GitHub API의 blob/tree/commit 및 expected-head ref update로 해당 작업 브랜치에 게시했다. 모든 원격 커밋을 fetch해 실제 SHA·시각을 확인했다. 공통 파일·dot-control.json·다른 workstream·통합 브랜치는 수정하지 않았다. 이 인계 이후 추가 산출물을 커밋하지 않는 것을 마지막 단독 HANDOFF 커밋의 경계로 삼는다.
