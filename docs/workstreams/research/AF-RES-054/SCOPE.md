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

### R1a · 검색 문법 적응, 선정 전 명시

시점: 2026-11-23 UTC, 새 여섯 자리 선정 및 원자료/결과 열람 전. Zenodo API의403/정렬400, OSF 제목 필터의 Boolean문자열 리터럴 처리, 웹검색의 domain/date 필터 무시를 관측했다. 실패나 잘못 해석된 질의를 적격0의 근거로 쓰지 않는다. 사전식 자체와 적격 조건·출판일/ID 정렬은 유지하고 다음 **동치 질의 분해**를 허용한다.

- 소프트웨어 원식의 여섯 conjunction을 왼쪽부터 `API example + user study`, `API example + experiment`, `code example + user study`, `code example + experiment`, `documentation + user study`, `documentation + experiment`로 실행한다. 따옴표·site/domain·날짜는 실제 엔진 문법에 맞춰 기록한다.
- 교육/설계는 `worked example + task time`, `worked example + completion`, `design example + task time`, `design example + completion`의 네 conjunction이다. 분야 조건은 원래 분야 슬롯에 맞춰 사용한다.
- native 제공 정렬을 확인하여 유효한 정렬로 재요청할 수 있다. 이것은 결과 부호를 본 후 문턱을 바꾸는 변경이 아니다.
- linked 학회/기관 원논문 metadata에서 author Zenodo/OSF package를 찾는 역방향도 기록한다. 해당 저작이 원식·연도·개입/대조·사람 수행·공개 표기를 만족해야 같은 셀에 들어간다.
- **동일 source×domain 전체에서 최대30 metadata**를 유지한다. atom마다30으로 늘리지 않는다. 원순서·중복·domain 밖/연도 밖·상한 초과를 구분한다. 최종 선택은 여전히 dedup 후 원논문 출판일·영구ID순이다.
- 당시 노출: software 예비 metadata에서 observational learning-resources 및 prompt study 후보를 보았으나 적격/결과는 확정하지 않았다. crossdomain에서는 확대 진단으로 2024 worked-example 논문/OSF 표기를 보았으나 효과 수치는 선정에 쓰지 않았다. 이 진단 후보는 동치 원식을 만족하는지 확인하고 그 유입 경로를 표시해야만 들어갈 수 있다. 완전 무노출 모집이라고 부르지 않는다.
- 전후 결론: 아직 선정 완료0이므로 교체된 연구0. 이전 broken-query 반환만으로는 빈 자리를 확정하지 않았고, 이후에도 결과 좋은 연구로 채우는 선택은 금지한다. 실제 영향은 frame과 selection에 남긴다.

### R1b · 실제 모집틀과 사전 노출의 한계

새 연구의 최종 원격 선정 snapshot 전, 2026-11-23 UTC에 다음 실제 동작을 확인했다.

1. Zenodo는 이 환경의 anonymous API에서 size25가 허용되며 size30은400을 돌려준다. `sort=publication_date` 응답의 실제 날짜는 내림차순이었다. 첫25+다음5 페이지 또는 지원되는 역방향을 확인하고 실제 원순서를 저장한다. 실패/정렬 탐색은 probe이고 최종 후보 목록과 구분한다.
2. OSF는 전역 Boolean 검색을 같은 방식으로 제공하지 않아 제목 substring으로 넓게 얻은 후보에서 원식의 나머지 조건을 저자/논문 metadata와 색인 검색으로 재확인했다. 이는 원식과 동일한 API 전수검색이 아니다. 웹검색의 Methods snippet 자동노출, 정확 term match 미확인 후보를 기록한다. 단순히 `worked example`라는 제목만으로 원식의 시간측 조건이 성립했다고 간주하지 않는다.
3. 소프트웨어에서는 넓은 native 결과가 비소프트웨어 실험 documentation을 많이 포함하여 software/programming/API 저자 keyword 층과 논문→저자 package 경로를 사용했다. keyword 누락 연구를 놓칠 수 있다. 공개 패키지에 닿는 원논문 경로는 frame에 별도 표시하며 native 첫30 전체의 대표 표본이라고 부르지 않는다.
4. source/domain/year 필터 밖의 검색 결과는 원 반환 순서·탈락 이유·집계로 보존한다. 읽은 후보 메타데이터의 공식 retained frame은 source×domain 최대30으로 제한한다. 여러 문법·정렬 probe의 전체 abstract를 재게시하지 않고 request/status/count/hash/date range와 노출 사실을 남긴다. 부적격 후보를 지우고 유리한 결과로 갈아 끼우는 규칙은 없다.
5. 출판일은 DOI 생성일이나 OSF node 생성일로 대체하지 않는다. 저자/발행자의 online 날짜와 journal issue 날짜, 정밀도·충돌을 함께 보존한다. 중첩되는 불완전 날짜 때문에 선후가 확정되지 않으면 operational sort key와 순서 민감도를 명시하고 세계에서 가장 이른 연구라고 주장하지 않는다.
6. 교육 모집 중 Pillai2020를 임시 first-verified 후보로 보았으나 원격 동결 전에 같은 OSF첫30의 dx6qv를 Bichler2019/2020 저작으로 식별했다. 최종 선정은 이 metadata 보정과 날짜 비교 후 확정한다. 이 과정에서 결과 수치·자료 결합 가능성으로 교체하지 않았다. 초기 제안과 보정은 selection history에 남긴다.
7. 별도 방법/복제 조사자가 Bichler2019/2020를 먼저 열었고 root는 해당 논문의 표본수·시간설계·제외 정의를 우연히 먼저 전달받았다. 이 저작이 이후 교육 후보와 겹쳤다. 교육 선정 담당자는 이 시점까지 PDF결과·데이터 내용을 열지 않았고 그에게는 우선 저작 식별 metadata만 전달했다. **전체 팀이 모든 신규 저작에 무노출이었다고 주장하지 않는다.** 선정 snapshot에는 역할별 노출을 기록하며 효과 방향·숫자·결합 가능성은 적격·순서 기준으로 쓰지 않는다.

이 변화의 영향은 반환 범위/순서의 제한과 metadata 불확실성이다. 원래 계획한2018~2025·중재/대조·사람 수행·공개자료 표기·8자리, 공동 종점·통과선 금지 규칙은 바꾸지 않았다. 부분 모집틀의 공백은 공개자료가 세상에 없다는 판정이 아니다. 최종 수용 원장은 엄격한 원식·완전한 사전 무노출과 달라진 부분을 `부분`으로 표시한다.

### R2a · 동결 후 전문 판독과 원장 통합

2026-11-23 UTC, 선정 동결 뒤 전문·실험 패키지를 읽었다. 교육 동결은 `9cacf328e1ce325e15f1ab6cdd6da396216ea825`, 소프트웨어 동결은 `c3c4eb6a7ccf2815202cc67c2a2cf25c94353e7c`이다. 문턱·정렬·후보를 결과 방향에 따라 바꾸지 않았다.

- S02 DesignPatternDoc은 실제 T22/T32 구현 과제를 확인하여 유지했다. S03 Casdoc은 전문에서13명이 모두 같은 복합 문서를 보고 형식을 자유롭게 고르는 연구임을 확인했다. 별도 배정 대조군 요건은 충족하지 못하지만 원래 선정 자리에 범위 이탈로 남겼다. S04/D01은 미충원 상태를 유지한다.
- Newton의25분 저자 완료6/4는 보조 종점이다. 최종 제출이 무엇인지와 기능적 완료 판정식을 공개판에서 확인하지 못했으므로 요청한 제출×최종품질 종점으로 승격하지 않는다. 독립 채점자 자체를 새 필수 요건으로 만든 것은 아니다. 원래 기능 판정식과 저자 집계의 대응이 확인되면 독립 채점자가 없어도 판정을 갱신할 수 있다.
- Blueprint 원래 이진 품질선 없음, eXoaDocs의 명시된40분 공동 집계3/1, E01의 연습45분/별도 검사 약35분은 서로 다른 증거 수준으로 유지한다. 원래 사건이 정의되지 않은 경우에는 무정보 수치범위를 만들어 원 종점처럼 보고하지 않는다.
- AF-RES-050에서 인수한 Blueprint 그림 연결 주장은 재검토 후 채택하지 않는다. 지정 CHI PDF에는 Fig4 참조만 있고, 직접 본 dissertation Fig5.4의 네 독립 순위는 공통 사람키가 아니다. 이것은 증거 정정이며 모집·계산 규칙 변경이 아니다.
- `streams/crossdomain/search-audit.json`은 초기 보조 웹 검색 중 일부 질의 문자열/초 단위 시각을 보존하지 못한 한계를 명시한다. native API 질의/반환범위·순서와 최종 선정 snapshot은 남았다. 전체 검색을 완전 재연 가능하다고 주장하지 않는다.
- 고유 저작 계산은 패키지 파일을 중복 산입하지 않는다. BM-P01 저자 계획 DOCX는 실질적 열람이지만 보수적 최소 수에는 추가하지 않았다. 별도 에이전트는 추가1저작으로 셀 수 있다고 판단했으나, 어느 관례에서도 개입 자료4개 배당 미달과 실험판 대응 한계는 달라지지 않는다. 독립 도구 DesignPatternDoc 저장소는1저작으로 세며21명 실험 바이너리와 동일성은 미확인이다.
- 별도 에이전트 교차검토의 세 정정(Casdoc 복합 instruction 코드, Blueprint 그림 위치, eXoaDocs 실패사유 미확인 표현)을 반영했다. 검토는 외부 사람의 독립 심사나 독립 복제 연구가 아니다.

전·후 결론: 사전 규칙은 이진 통과선 발명과 결과를 본 뒤 후보 교체를 금지했다. 전문 판독 후에도 규칙은 동일하다. 새 이름 있는4자리 중 실제 배정 비교는3자리이며, 전체8자리의 부족분을 진단용 연구로 메우지 않았다. 선정 연구에 대한 단독 설명 효과나 주효과 입증은 판정하지 않는다.
