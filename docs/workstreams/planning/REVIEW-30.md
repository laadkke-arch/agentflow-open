# REVIEW-30 · 근거를 읽은 뒤 무엇이 달라졌는가

부분 설계와 목적을 받은 탐색기는 유용한 기능을 찾아 링크를 줄 수 있어야 한다. 이번 네 작업에서 설계자가 가져갈 수 있는 가장 구체적인 결과는 **어느 단계에서 쓸 만한 정보가 사라지는지**다. 예를 들어 영어로 찾은 Filter Mask는 첫 후보였지만 표시 기준을 엄격히 하자 숨겨졌다. 차트에서 로컬 색 설정과 선택 범위 이동 설정은 같은 정지 그림을 만들면서도 다른 상태를 바꿨다. 독자가 이 차이를 읽고 실제로 설계를 고쳤는지, 그 결과 재작업이 줄었는지는 아직 미확인이다. [표시 원장][slots] · [도표 검산][v119] · [독자 원장][trails]

## 검토 기준과 새로 인수한 작업

2026-11-24 UTC에 `work/planning`의 최신 [REVIEW-29][prev]를 먼저 읽었다. 그 파일이 인용한 [이전 진행표][old]와 [이번 통합 진행표][reg]의 작업 행을 ID와 내용으로 대조했다. 기존 114행은 모두 같고 AF-RES-117~120 네 행이 새 DONE이다. 현재 전체 118행은 DONE 116·BLOCKED 2다. 연구만 세면 116건 중 DONE 114·BLOCKED 2(018·035)이고 나머지 DONE 두 건은 AF-DOT 연결 시험이다. DONE 116행의 중앙 `acceptance_evidence`는 모두 빈 배열이다. 네 연구의 실제 수용 범위는 각 인계와 근거 원장에 있다. [연구 운영 규칙][rules]

| 새 DONE·연구 상태 | 등록 SHA의 인계 | 작업자가 검사한 결과판 | 이번 검토에서 다시 센 대상 |
| --- | --- | --- | --- |
| AF-RES-117 · PARTIAL | [87081e4][h117] | [63d6852][r117] | 잠정 8사건·51개 사건 행, 귀속 등급과 모집 경계 |
| AF-RES-118 · PARTIAL | [077258d][h118] | [7186eb4][r118] | 24기능의 기준 판독, 실측 288자리와 미모집 108자리, 세 표시 정책의 이득·손실 |
| AF-RES-119 · PARTIAL | [be7d6e3][h119] | [038ac86][r119] | 보기별 반환, 렌더러·환경별 출력 수, 동일 도형의 좌표 |
| AF-RES-120 · PARTIAL | [d85c855][h120] | [de99023][r120] | 111보기의 경로 수, 자연 6건의 문서 표지, 99개 예정 단계의 실제 수신 여부 |

읽을 때 네 작업 브랜치의 head는 각각 등록된 인계 SHA였다. 각 마지막 커밋의 변경은 `HANDOFF.md` 하나였고, 등록판과 작업자가 검사한 판의 `RESULT.md` 내용도 네 쌍 모두 같았다. 아래 재생·시험은 연구자가 남긴 실행 기록이다. 이번 검토에서 다시 한 일은 고정 원장의 행·분모 대조와 원 관측값 확인이다. 앞선 116번까지의 결과는 직전 누적 검토에서 인수했다. [이전 누적 검토][prev]

## 이전 회차부터 이어지는 제품 판단

사용자는 전체 또는 일부 구조와 목적을 준다. 반환 후보에는 완성품·서비스뿐 아니라 기능 하나, 연결 가능한 부품, 다른 분야의 원리가 들어간다. 제품이 줄이려는 비용은 이미 있던 해법을 늦게 발견해 설계를 다시 하는 비용이다. 저장할 원문 범위, 되물을 조건, 검색·AI 전처리 방식, 상시 수집 여부, Studio의 입력 계약은 여전히 설계 대안이다. [제품 연구 브리프][goal]

| 설계자가 판단할 문제 | 29회까지 확보한 근거 | 이번 회차를 반영한 판단 |
| --- | --- | --- |
| 선례를 발견하면 결정이 바뀌는가 | 분야 단서를 준 010은 원리 7군을 찾았고, 단서 없는 033은 144쌍 중 넓은 지지 1쌍·당시판 지지 0쌍이었다. 022의 미인지→변경→시행은 0/24였다. 105의 ‘처음 알았다’ 두 발언은 특정 조작에 관한 것이었다. 109의 12선택·27시험 제안은 원 프로젝트에서 실행되지 않았고 113은 예제·출전을 모두 읽은 쌍이 0/6이었다. | 117은 링크가 들어간 문구 변경과 구체적인 반대 논거를 찾아냈다. 특정 선례에 대한 작성자의 명시적 귀속과 확인된 옵션 변경을 함께 충족한 사례는 찾지 못했다. 버려진 대안도 적용 한계나 시험 입력을 알려줄 수 있지만 당시 채택·비용은 별도 근거가 필요하다. [117 주장][claims] |
| 어떤 정보가 부분 입력의 원뜻을 지키는가 | 020은 주장 72/73을 전달해도 충돌 완전 해소가 2/16이었다. 070의 자연 요청에는 되묻기 효과 분모가 없었고, 074의 구성 입력은 추가 값으로 8/8을 구별했다. 111은 동의어 변경 후 두 방식 모두 기준 정합 0/6이었다. 115의 본 자연 1/6에서 시작 사각형 ID는 있었고 아직 생성하지 않은 텍스트의 ID는 없었다. | 119는 작성자가 본문에 쓴 도표 6/6을 확보했다. 같은 분량에서 인접 레코드와 직접 참조를 주자 두 방식의 자동 정확 판정이 각 3/6이었다. #3981에는 작성자가 제안한 두 끝점이 처음부터 있었다. 무엇을 이미 알고 있었고 어떤 발생·다른 객체를 함께 지키려는지 구분할 근거가 생겼다. [선택과 근거][choices] |
| 쓸 수 있는 기능이 목록과 화면에 있는가 | 076의 자연 6요구×20후보에는 직접 적격이 없었다. 080의 자료집 확장에서 자연 1/5·교정 3/5가 양성으로 바뀌었다. 096은 인접 자료를 6/6 노출해도 단독 완결 0/6이었다. 110의 직접 1쌍은 영어로만 찾았고, 114의 한국어 구성 대조에서 별칭은 표시된 직접 적격을 1/2→2/2, 확인된 충돌을 2→6으로 늘렸다. | 118의 32개 활성 요청–언어에서 자료집 직접 적격 10쌍 중 9쌍이 조사에 들어왔다. 그대로 채우면 9, 조작·대상 근거를 요구하면 8쌍을 표시했다. 검색 누락·표시 누락·하위 기능의 가치는 다른 단계에서 생긴다. 실제 한국어 작성자의 회수는 미확인이다. [표시 집계][sum118] |
| 주소와 인용으로 과거·현재 판단을 복원하는가 | 055는 과거 판단 4/4, 다음 판 판단 0/4였다. 071은 저장한 조각·설정으로 과거 자료 22/22를 복원했지만 075에서는 전체 집합이 필요한 유일성·공동 1위 주장을 각각 16/16 보류했다. 086은 당시 제공 관측창이 0/9였고 106의 같은 주소는 옛 집단 점수라는 용도를 잃었다. 113은 같은 예제의 첫 3,000자 밖에서 실패 사례를 찾았다. | 117의 당대 crate 세 판본과 119의 최초 게시 리비전 6건은 미확인이다. 120에서 직접 절 뒤쪽에서 시작하니 오히려 앞쪽의 월 번호 규칙을 놓친 후보가 있었다. 판·문서 구간·입력·반환 이유를 보존할 필요는 주장마다 다르다. [117 결과][r117] · [120 경로][routes] |
| 링크 옆 한 줄이나 둘째 링크가 독자를 돕는가 | 021에서 두 절 예산으로 충분한 판단은 주소만 6/23, 절 목록 9/23, 조건에 맞춘 절 14/23, 잘못 붙인 절 8/23이었다. 108의 같은 1,200자에선 키워드 4/16·예외 우선 2/16이었다. 112의 반복 설명과 116의 반복 문구(A/B)는 길을 바꾸지 않았고, 새 목차 단서는 116의 2/6에서 길을 바꿨다. 그 자연 6건의 완전 답 기회는 도달 불가 4·기준 미확인 2였다. | 120의 직접 절이 자연 6/6에서 인접 정의를 노출하는 경로가 있었고, 둘째 시험이 완전 근거를 더한 예는 구성 문제에서 확인됐다. 실제 수신자가 답한 건수는 0이다. 034의 부분 시간 380→57초·전체 시간 849→847초처럼 열람 비용과 사용자 전체 작업시간도 각자 측정해야 한다. [경로와 비교 분모][pairs] |
| 일부를 고치면 다른 무엇이 바뀌는가 | 078은 단독 기능을 연결할 때의 실패를, 089·091은 선택색·위치와 실제 편집 대상·행의 차이를 보였다. 095의 옆 표 경계선, 103의 외관 10/10 보존과 8자리 텍스트 선택 소실, 107의 단일 발생 편집에서 공유 정의 0/6·위치 지정 6/6이 보존 조건을 드러냈다. 115의 악보 변동 1바이트는 주석이었고 재생 기대열은 이미 맞았다. | 119에서 한 자식의 정렬은 공유 도메인과 충돌해 같은 그림이 남았고 공통 정렬은 막대와 주석을 함께 옮겼다. 차트의 정지 화면, 편집된 사양 값, 이후 입력의 결과를 각각 확인해야 어느 기능 절을 권할지 정할 수 있다. [저장 변경·렌더 결과][r119] |

표 안의 과거 수치와 표본 정의는 [REVIEW-29][prev]에 연결돼 있다. 다음은 이번에 직접 읽은 네 작업의 증거와 사용 한계다.

## 새 DONE에서 확인한 것과 근거가 끊긴 곳

### 117 · 링크가 주장을 바꾼 기록과 선택을 바꾼 기록

Python PEP와 Rust RFC의 첫 검색 결과 각 100건에서 초안·부모 차이를 읽은 잠정 사례는 각 4건이었다. 고유 1차 저작 24개를 읽었으나, 두 저장소 모두 적격 30번째와 다음 31번째의 경계를 확정하지 못했다. 8개 주장에는 G2 후보 4·G1 1·G0 3이 있다. 특정 선례 때문에 옵션 또는 시험이 달라졌다고 명시한 작성자 발언과 실제 차이가 동시에 확인된 G3는 0건이다. 모집단 빈도나 영향이 없다는 결론을 낼 분모는 없다. [모집 상태][frame117] · [사건 51행][events] · [주장 등급][claims]

Rust #3362에서는 io-mux가 인용된 날 같은 링크를 넣으며 스트림 순서에 관한 표현이 완화됐다. API 폐기 유보는 그보다 이른 1월 13일 기록에 있다. #3367에서는 Pod·enum_dispatch 인용 뒤 TODO와 작성자의 한계 인정이 있지만 이미 1월 6일 별도 반례가 있었고 종료 이유에 가용시간과 재작성도 있다. PEP #2997에서는 mypy 예제와 TypedMapping→ReadOnly 범위 축소를 각각 찾았지만 두 사건을 잇는 최초 변경과 이유는 비어 있다. 당대 외부 crate 원문 세 건, 원 프로젝트의 시험 실행과 실제 절감시간도 미확인이다. 초안 병합·철회·안정화 시각을 발견 효과로 해석하기엔 이 연결이 빠져 있다. [문안·반응·경쟁 설명][r117]

### 118 · 잘못 붙인 링크를 줄인 비용

32개 활성 요청–언어마다 정책별 세 자리, 즉 96자리씩을 비교했다. 아래 합계는 활성 288자리에서 다시 센 값이다. 396행 원장에 함께 보존된 미모집 자연층의 예정 108자리는 제외했다. [표시 원장][slots] · [층별 집계][sum118]

| 같은 후보의 표시 규칙 | 직접 적격 | 일부 근거 | 원절과 명시 충돌 | 미확인 표시 | 공석 |
| --- | ---: | ---: | ---: | ---: | ---: |
| A · 기존 순서로 채움 | 9 | 7 | 15 | 38 | 27 |
| B · 명시 충돌만 건너뜀 | 9 | 7 | 0 | 46 | 34 |
| C · 조작·대상의 근거 요구 | 8 | 0 | 0 | 0 | 88 |

**114와 118의 충돌 수에는 정의 차이가 있다.** 같은 탐색 144쌍에서 114의 충돌 138은 118의 ‘원절로 반박 가능’ 규칙으로는 명시 충돌 7·미확인 131이다. 나머지 6쌍은 두 판정에서 모두 일부다. B는 충돌을 지운 뒤 근거 미확인 링크를 더 보여 줬고 C는 쓸 만한 하위 부품까지 숨겼다. 영어 Filter Mask는 C에서 필요한 동사 근거가 카드에 없어 탈락했고, 같은 기능은 한국어 진단 요청에서 조사 후보에 들어오지 못했다. 35개 고유 저작과 반복 재생으로 고정 카드의 동작은 검산할 수 있다. 언어쌍은 한 작업자가 만들었다. 선행 작성자 원글은 5/6을 직접 열었고, 신규 시험은 단언 6/6과 입력 본체 5/6을 확인했다. 남은 EXR 한 건은 포인터만 열렸다. 실제 한국어 독자의 이해와 앱에서 실행한 결과는 미확인이다. [판정 대응][jud118] · [필터 및 보류 원인][r118]

### 119 · 정지 화면과 다음 조작

두 트래커에서 각각 본문에 도표가 있는 첫 40건과 41번째 경계를 고정해 자연 입력 6/6을 확보했다. 최초 게시본은 0/6 확인, 정확한 저자 전체 환경에서의 유효 SVG는 예정 36자리 중 0이었다. 저자가 명시한 core CLI 시도 6회는 문법 파싱에서 실패했다. 다른 다섯 자연 사건의 대체판은 30회 중 유효 26회, 원형과 두 수정안이 모두 비교 가능한 사건은 4/5였다. 기술 규칙의 정확은 원요구만 0/6·인접 레코드 3/6·직접 참조 3/6, 분량을 맞춘 두 보기 역시 각 3/6이었다. 가림 독자 판독은 0/18이다. [실행 환경과 반복 검산][v119] · [보기별 선택][choices]

#8628의 정지 SVG는 두 수정 모두 원형과 같았다. January 선택값을 주입했을 때 로컬 설정은 막대 49개의 fallback 색을 바꿨고, 공유 설정은 이동 신호 두 개를 제거했다. 실제 포인터를 어디서 누를 때 점프하는지는 이 시험에서 재현하지 않았다. #3987에서는 원 숫자 하나를 줄여 합을 100으로 만들자 세 부채꼴 비율이 바뀌었다. `showData`는 범례에 원값을 넣고 합 101은 그대로 뒀다. 합 100, 같은 값의 같은 표시, 원값 보존 사이의 선택은 작성자 요구로 확인할 문제다. [관측값과 실제 원글의 구별][r119]

**표의 수치 하나는 원 로그와 어긋난다.** 별도 자연 대조 M3994의 RESULT 표 3은 원형 MG의 y를 11.65625로 적었다. 두 반복의 브라우저가 기록한 MG 경계 상자 y는 모두 **11.71875**이고, 국소 변경도 같은 값, 공유 변경은 275다. 이 검토에서 좌표를 인용할 때는 원 관측값을 사용한다. 국소 설정은 원형과 같고 공유 설정은 양쪽 군집을 재배치했다는 판정은 두 기록에서 일치한다. [결과 표][r119] · [원형 1회][mg1] · [원형 2회][mg2] · [세 조건 검산][v119]

### 120 · 읽을 수 있는 위치와 실제 독자의 답

제한 뷰어에서 최대 3회·회당 1,500자로 조사한 111보기의 경로는 892개다. 자연 6건에서 일반 시작점 A는 1/6, 직접 절 B는 6/6에 관련 또는 인접 정의 표지가 있었다. C는 B와 같은 첫 절에 인접 시험을 더했고 두 표지에 닿는 경로가 6/6이었다. JSON 왕복 시험은 YAML을 포함한 입력을 검증하지 않았고 CSV의 빈 행 시험은 특정 81열 입력의 빈 필드 보존을 입증하지 않았다. 자연 6건의 완전한 근거 경로는 **모두 미확인**이다. 엄격한 기회 표본 두 자리는 jq 후보 28건·CPython 다음 창 0건에서 공석이었다. [경로 원장][routes] · [정답 기준][gold120]

구성 K1은 직접 절 한 번으로 충분했다. K2는 EOF와 strict 조건에 맞는 시험을 추가한 C에서만 두 번(3,000자)에 근거가 모였고, 같은 제목의 writer 시험을 붙인 음성 대조는 실패했다. 반대 방향의 실제 문서 사례도 있다. 후보 O42는 A가 세 번 열어 월 번호 규칙을 찾는데 B의 시작점은 그 문장보다 뒤다. 이는 문서상의 계약까지 확인한 사례다. 실제 적용판의 행동은 미확인이다. 99단계 가운데 81행은 새 독자가 없어 미실시, 18행은 기회 표본 공석이었다. 독자 비교 0건으로 정답률·추가 링크의 오확정률·사람 시간 이득을 계산할 수 없다. [구성·자연·기회 비교][pairs] · [실제 수신 기록][trails] · [결과와 한계][r120]

117과 120은 GitHub로 자료를 판독하고 검사 기록을 남겼으나 정식 workbench 세션 검사는 미실시였다. 118과 119는 고정 checkout에서 재생·명시 세션 검사를 했고 다른 사람이 의미를 가려 판독한 기록은 없다. 같은 사람이 파일을 다시 읽는 검산, 프로그램의 실행, 이용자가 읽고 내린 판단은 수용 근거가 다르다. [117 인계][h117] · [118 인계][h118] · [119 인계][h119] · [120 인계][h120]

## 다음 네 작업

| 작업·담당 | 완료된 선행 | 새로 관찰할 것 | 판정을 바꾸는 반례 |
| --- | --- | --- | --- |
| AF-RES-121 · web-pro | 117 | R1·R3·P4의 당대 선례 기능, 저자가 밝힌 이유, 전후 변경을 맞추고 R2·R4에도 같은 기준을 적용한다. | 링크보다 이른 선택, 같은 변경을 설명하는 다른 이유, 문구만 바뀐 hunk라면 직접 귀속을 보류한다. |
| AF-RES-122 · codex-cloud | 118 | 한국어 작성자의 실제 질문에서 영문 심벌 및 출전이 있는 한국어 별칭의 기여를 16기능과 네 조회로 측정한다. | 원문에 이미 있던 영문 심벌이 적중을 설명하거나 별칭이 반대 역할을 상위로 올리면 그 손실도 센다. |
| AF-RES-123 · codex-cloud | 119 | #8628의 고정 대체 환경에서 브라우저 드래그 48자리의 실제 hit와 선택 경계를 기록해 색·이동·투영 중 어떤 절을 안내할지 판별한다. | 선택 오버레이가 좌표를 가로채거나 범주 경계가 정상적으로 바뀐 경우에는 점프의 원인 판정을 달리한다. |
| AF-RES-124 · web-pro | 120 | 새 웹 Pro 독자가 선행의 봉인된 요청 여섯 건을 직접 읽는다. 첫 절 전후 답을 저장한 뒤 추가 시험 제시 세 건과 같은 절 계속 읽기 세 건의 실제 선택·수정을 관찰한다. | 둘째 링크를 안 열거나 다른 입력의 시험을 읽고 단정한 경우를 그대로 센다. 한 독자와 서로 다른 사건으로 사람의 평균 효과를 추정하지 않는다. |

네 작업은 각각 완료된 선행 하나에만 의존한다. 121의 결정 기록, 122의 한국어 검색, 123의 실제 조작, 124의 독자 답은 서로의 산출물이 없어도 얻을 수 있다. 각 작업자가 바로 시작할 입력판·세부 질문·필수 표·원문 수·반증 및 인계 기준은 [NEXT_TASKS-30.json](NEXT_TASKS-30.json)에 있다.

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/821df6f76fb6bc35e25ae0a0d71e032c3261deb4/docs/workstreams/planning/REVIEW-29.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/101426a5e76154bb89b642dd9bd3c52fc1229c30/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/13be736df17a4c697880f57029d16de38db061dd/docs/automation/dot-control.json
[rules]: https://github.com/laadkke-arch/agentflow-open/blob/13be736df17a4c697880f57029d16de38db061dd/docs/RESEARCH_WORKFLOW.md
[goal]: https://github.com/laadkke-arch/agentflow-open/blob/13be736df17a4c697880f57029d16de38db061dd/docs/product/RESEARCH_BRIEF.md
[h117]: https://github.com/laadkke-arch/agentflow-open/blob/87081e48fd51ed74dd038070b1c46c7f3a7a8da2/docs/workstreams/research/AF-RES-117/HANDOFF.md
[r117]: https://github.com/laadkke-arch/agentflow-open/blob/63d6852aa4693902bfafa420c319144e93d741a7/docs/workstreams/research/AF-RES-117/RESULT.md
[h118]: https://github.com/laadkke-arch/agentflow-open/blob/077258def07e3d7d103ecbd3183d60a2e35f9d48/docs/workstreams/research/AF-RES-118/HANDOFF.md
[r118]: https://github.com/laadkke-arch/agentflow-open/blob/7186eb4bf27cc9f6a3e6b7a1d6ebc2530abfbf0a/docs/workstreams/research/AF-RES-118/RESULT.md
[h119]: https://github.com/laadkke-arch/agentflow-open/blob/be7d6e3365e090ca674b4f0baaf570a27f8e51cf/docs/workstreams/research/AF-RES-119/HANDOFF.md
[r119]: https://github.com/laadkke-arch/agentflow-open/blob/038ac865c8d2cada84e32989bdd5eb174f4bb7d8/docs/workstreams/research/AF-RES-119/RESULT.md
[h120]: https://github.com/laadkke-arch/agentflow-open/blob/d85c8556c85583a900f097c3bcdab76bd6324655/docs/workstreams/research/AF-RES-120/HANDOFF.md
[r120]: https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/RESULT.md
[claims]: https://github.com/laadkke-arch/agentflow-open/blob/63d6852aa4693902bfafa420c319144e93d741a7/docs/workstreams/research/AF-RES-117/claims.csv
[frame117]: https://github.com/laadkke-arch/agentflow-open/blob/63d6852aa4693902bfafa420c319144e93d741a7/docs/workstreams/research/AF-RES-117/FRAME_STATUS.md
[events]: https://github.com/laadkke-arch/agentflow-open/blob/63d6852aa4693902bfafa420c319144e93d741a7/docs/workstreams/research/AF-RES-117/events.jsonl
[slots]: https://github.com/laadkke-arch/agentflow-open/blob/7186eb4bf27cc9f6a3e6b7a1d6ebc2530abfbf0a/docs/workstreams/research/AF-RES-118/slots.csv
[sum118]: https://github.com/laadkke-arch/agentflow-open/blob/7186eb4bf27cc9f6a3e6b7a1d6ebc2530abfbf0a/docs/workstreams/research/AF-RES-118/evidence/table3.csv
[jud118]: https://github.com/laadkke-arch/agentflow-open/blob/7186eb4bf27cc9f6a3e6b7a1d6ebc2530abfbf0a/docs/workstreams/research/AF-RES-118/judgments.csv
[v119]: https://github.com/laadkke-arch/agentflow-open/blob/038ac865c8d2cada84e32989bdd5eb174f4bb7d8/docs/workstreams/research/AF-RES-119/evidence/verification.json
[choices]: https://github.com/laadkke-arch/agentflow-open/blob/038ac865c8d2cada84e32989bdd5eb174f4bb7d8/docs/workstreams/research/AF-RES-119/choices.jsonl
[mg1]: https://github.com/laadkke-arch/agentflow-open/blob/038ac865c8d2cada84e32989bdd5eb174f4bb7d8/docs/workstreams/research/AF-RES-119/evidence/render/r1/M3994-base/browser-observations.json
[mg2]: https://github.com/laadkke-arch/agentflow-open/blob/038ac865c8d2cada84e32989bdd5eb174f4bb7d8/docs/workstreams/research/AF-RES-119/evidence/render/r2/M3994-base/browser-observations.json
[pairs]: https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/pairs.csv
[trails]: https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/trails.jsonl
[routes]: https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/routes.jsonl
[gold120]: https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/gold.csv
