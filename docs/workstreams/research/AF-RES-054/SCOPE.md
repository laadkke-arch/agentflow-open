# AF-RES-054 범위·사전 규칙

## 입력판과 권한

- 작업: AF-RES-054#1, 공개 기록 연구. 새 사람 모집·저자 연락·계정 변경·유료 자원·배포·공통 파일 변경은 하지 않는다.
- 저장소: laadkke-arch/agentflow-open; 브랜치: work/research-af-res-054; 허용 경로: docs/workstreams/research/AF-RES-054/.
- 계획 통합판: d7e60daf1b5b2c918502c407982566369b7149e3.
- 실제 시작 통합판: 573a8f1a7cafa90b87bcbb4267e73fee12385bda. GitHub ref와 Git ls-remote에서 확인했다.
- 의존 인계: AF-RES-050@a3e13076e889dd49bfa7b7aa2fad6d149d874452.
- 읽은 결과판: 5797f9a9f1a1f0281d54c1922c6698a53093b67a의 RESULT.md, joins.csv, outcomes.csv, evidence/source-counts.json.
- AGENTS.md, STATE.md, docs/DOT_AUTOMATION.md, docs/RESEARCH_WORKFLOW.md, dot-control.json의 AF-RES-054와 AF-RES-050 항목, 제품 브리프를 GitHub에서 직접 읽었다. 실제 start 영수증은 evidence/session-start.json이다.
- 작업자는 이 대화의 assistant이며 배정 worker_kind는 web-pro다. 별도 웹 Pro UI 모델 선택을 관측했다고 주장하지 않는다. 병렬 보조 조사자는 분리된 하위 경로에만 쓰고 root가 편집·커밋한다.

## R1: 결과 열람 전 모집 규칙

1. 여덟 자리: B01 Blueprint directed, B02 eXoaDocs 네 과제 묶음; S01–S04 새 소프트웨어 네 자리; E01 worked-example 교육 한 자리; D01 CAD·공학 설계 한 자리.
2. 새 여섯 자리는 출판일 2018-01-01~2025-12-31, 사람 대상 수행 과제, 예제/API 문서/선례 링크 도움의 중재와 대조, 저자 공개 연구자료 표기를 모두 요구한다. 자료 공개를 찾아 설계한 표본이지 분야 공개율 표본이 아니다.
3. 자료원×분야는 Zenodo/OSF × software/education/design의 여섯 셀이다. 셀마다 최대 30개 실제 반환 메타데이터를 보존한다. native API가 가능하면 동일 질의로 날짜 오름차순 30개; 실패하면 동일 질의를 site/domain 범위 웹 검색에 보내 반환 순서를 보존한다. 이 경우 검색엔진이 노출한 제한 모집틀이며 native 전체 목록으로 부르지 않는다. 각 실제 API·엔진, query 문자열, UTC, 반환 범위·순서·실패를 남긴다. 채우기 위해 30개를 넘는 별도 숨은 후보 풀을 쓰지 않는다.
4. 소프트웨어 질의: ("API example" OR "code example" OR "documentation") AND ("user study" OR "experiment"). 교육·설계 질의: ("worked example" OR "design example") AND ("task time" OR "completion"). 분야·2018~2025 필터를 명시하고 실제 엔진 문법을 기록한다. 두 source 셀을 합친 뒤 DOI, 저작·코호트로 중복 제거하고 논문 출판일·영구 ID순으로 정렬한다. 날짜가 연도뿐이면 해당 정밀도와 tie 순서를 보존한다. 논문일과 dataset 공개일을 혼동하지 않는다.
5. 파일 목록·제목·초록·공개자료 표기까지만 보고 적격을 판정한다. abstract에 결과가 함께 나오면 노출을 기록하되 결과 부호·수치·결합 가능성은 선정 열에 사용하지 않는다. 각 분야의 첫 적격 4/1/1개를 선택하고 선정 snapshot을 root에 보내 고정한 뒤 Methods·결과·CSV를 읽는다.
6. 050의 기존 연구 NCQ, eXoaDocs, Blueprint, CodeMend, Unakite, Strata, Schwonke worked examples, Chan engineering analogy는 두 기준 자리 외에는 중복 제외한다. 새 공개판 없는 NCQ 코드북·Strata workbook·CodeMend 평가표는 재탐색하지 않는다.
7. 적격 부족이면 빈 자리를 유지한다. 공개자료 표기 후 원자료가 없거나 접근 불가해도 후순위로 교체하지 않는다. 기관 저장소·학회 원논문은 선정 metadata의 저작 식별·원문 및 연결 자료 확인용이며 임의 결과 좋은 연구를 채우는 별도 선정 경로가 아니다.

## R2: 종점·결합·계산

- 1차 종점은 배정 단위가 원래 제한시간 안 제출하고 원래 최종 품질 기준을 통과한 교집합이다. 원래 없던 통과선·cap을 만들지 않는다. 선택/검색/붙여넣기, 총 수행, 검사, 훈련, 추적 재작업을 분리한다.
- 배정 cohort×person×task×condition×period를 왼쪽 원장으로 삼는다. event는 키·시간종점별 집계 후 결합한다. 키 유일성·원행/집계행/결합행·중복/미연결/철회 분모를 기록한다. 정렬된 그림 순위, 익명 query ID는 참가자 키가 아니다.
- 같은 N에 정확한 t(시간 내 제출), q(품질 통과)가 있으면 L=max(0,q+t-N), U=min(q,t). 2×2 순서는 [both=x, quality_only=q-x, time_only=t-x, neither=N-q-t+x]. 각 극단의 비음수 정수·행열 합을 검산한다.
- 설계가 품질 통과⊆시간 내 제출 등 포함 관계를 명시하면 그 제약을 먼저 적용한다. 저자가 동일 교집합을 명시하면 author aggregate로 기록하고 raw direct join과 구별한다.
- t 또는 q를 모르면 알려진 정확한 주변 개수에서만 경계를 얻는다. 둘 다 모르면 N이 알려진 경우 count [0,N]/rate [0,1]은 논리적 무정보 범위다. N도 모르면 count/rate 추정의 입력 자체가 미확인이다. 구조적 포함만 있고 정확한 q가 없다면 그 제약만 보존한다.
- 통과자에게만 있는 시간분모, 중앙값, p값, 모집 계획 상한에서 전체 t를 역산하지 않는다. 등가 품질은 독립 기준 없이는 주장하지 않는다.
- 같은 과제·문턱·분모 조건하에 treatment-control 식별범위는 [L_T/N_T-U_C/N_C, U_T/N_T-L_C/N_C]. 식별범위와 표본추출/배정 불확실성을 분리하며 이를 CI라고 부르지 않는다. 교차 설계에서 개인·period 대응 없이는 개인별 효과를 계산하지 않는다.
- 결측은 실패로 덮지 않는다. 원래 규칙으로 미제출이 실패이면 그 규칙을 적용하고, 관측 안 된 칸은 별도로 민감도와 미확인으로 남긴다.
- 모든 수치에 facts/author aggregate/calculated bound/illustrative counterexample/proposal을 구별한다. constructed table은 가능한 예이며 관측 행이 아니다.

## R3: 근거·완결성

- sources.jsonl은 요청된 15필드를 지킨다. source_id는 열람, work_id는 고유 저작이다. 성공/부분/실패, URL·최종 URL·UTC·판·쪽/절·확인 내용·한계·계보를 한 행에 남긴다.
- 최소 고유 1차 저작 22: 새 원논문6, 기준2, 별도 author dataset4, 별도 개입/과제/루브릭4, 원 방법4, 별도 사전등록/직접복제2. 한 package의 CSV/README/동일 논문 판·번역·mirror는 하나다. 한 저작을 복수 quota에 중복 배정하지 않는다. 추가 자료는 초과층으로 표시하고 다른 층 미달을 숨기지 않는다.
- RESULT는 표1(8자리)·표2(조건·대비·결측)부터 시작하고 Q1~Q7, 대안 조건, 허용 문장, 약점3건 순이다. SELF_CHECK는 질문별 주장·직접 근거·반례 범위·틀릴 조건·최소 재개 자료를 쓴다.
- 묶음별 원격 커밋: (1) 이 규칙·계약 (2) 선정8자리·원자료/분모 (3) 결합·경계·반례 (4) 필수표·검토. 결과 고정 SHA 재열람과 session check 후 HANDOFF만 마지막 단독 커밋한다.

## 사전 노출 및 변경 이력

- 사용자 brief와 AF-RES-050 고정 인계·결과에는 기준 연구 및 기존 여덟 연구 수치가 이미 있다. 새 여섯 자리 선정과 독립이며 숨긴 블라인드로 부르지 않는다.
- 규칙 원격 커밋 전 도구 가용성 확인 과정에서 한 건의 software Zenodo site query를 실행했다. system2가 domain 밖 결과도 반환했다. 검색 결과의 제목/일부 초록이 노출됐고 원논문이나 dataset을 열어 선정하지 않았다. evidence/pilot-query.json에 원결과를 보존한다. 이 검색은 공식 30개 모집틀에 포함하지 않으며 공식 모집은 본 규칙 커밋 뒤 재실행한다. 이 노출 때문에 완전한 사전 무노출이라고 주장하지 않는다.
- 향후 변경은 UTC, 이전/이후 규칙, 당시 노출자료, 영향 행과 양쪽 결론을 이 절에 추가한다. 결과를 보고 불리한 자리를 교체하지 않는다.
