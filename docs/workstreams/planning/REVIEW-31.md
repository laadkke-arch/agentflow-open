# REVIEW-31 · 링크가 실제로 바꾼 것

부분 설계와 목적을 받아 이미 있는 제품·기능·부품·다른 분야의 원리를 찾아 주는 탐색기의 목표는 늦은 발견 때문에 생기는 재작업을 줄이는 것이다. 120이 읽을 수 있는 경로로만 남겼던 여섯 질문에 대해 **한 AI 독자가 추가 시험 링크 세 개를 모두 열었고, 한 사건에서 세미콜론 구분자의 동작 근거를 더 얻었다**. 여섯 사건에서 핵심 처방을 고친 사례는 없었다. 설계자가 링크를 받고 예정했던 구현을 바꿨는지, 사람이 시간을 아꼈는지는 여전히 미확인이다. [제품 목표][goal] · [독자가 본 구간][trail] · [시점별 채점][score]

## 검토 범위

2026-11-24 UTC에 `work/planning`의 최신 [REVIEW-30][prev]을 먼저 읽었다. 그 검토의 통합 진행표와 이번 진행표를 ID로 결합했다. 기존 118행은 내용까지 같았고, AF-RES-121~124 네 행이 새 DONE이다. 전체 122행은 DONE 120·BLOCKED 2다. 연구 120건 중 DONE 118·BLOCKED 2(018·035)이고, AF-DOT 연결 시험 두 건은 DONE이다. DONE 120행 모두 중앙 `acceptance_evidence`가 비어 있어, 아래 수용 범위는 작업별 결과와 원장에서 확인했다. [이전 진행표][old] · [검토 시점 진행표][reg] · [연구 운영 규칙][rules]

| 새 DONE | 등록판의 인계 | 작업자가 검사한 결과판 | 이 검토에서 대조한 단위 |
| --- | --- | --- | --- |
| 121 · 선례와 설계 변경 | [fe74c5e][h121] | [97e6900][r121] | 5사건, 목표 연결 6개, 주장 17행, 연표 58행 |
| 122 · 한국어 질문의 기능 검색 | [1fe2997][h122] | [e69a3f8][r122] | 공개 질문 진단 10건·구성 9건의 304쌍, 모집 경계와 네 조회의 표시 분모 |
| 123 · 차트에서 드래그한 대상 | [7554304][h123] | [0a4acb5][r123] | 본 시도 48행과 대조 36행, 원형 SVG의 막대·바탕 기록, 기능 절 선택 48행 |
| 124 · 추가 링크를 받은 독자 | [0c1b573][h124] | [7dd19f7][r124] | 실제 읽기·중단을 담은 18자리, 세 시점의 18답, 사후 실행 출력 |

네 인계의 연구 상태는 모두 **PARTIAL**이다. 확인 시 네 작업 브랜치의 head가 등록 SHA와 일치했다. 네 마지막 커밋은 각각 `HANDOFF.md` 하나만 추가했고, 각 등록판의 `RESULT.md`는 표에 적힌 검사판과 본문이 같았다. 각 인계가 보고한 고유 1차 저작은 순서대로 31·55·41·27개다. 이 검토에서는 원장 행과 관측값을 다시 읽고 집계했다. 브라우저 조작·CPU 실행·당시 독자 열람은 해당 작업자의 관측이다. 122·123에는 고정 checkout에서의 세션 검사 기록이 있다. 121·124는 GitHub 원격 자료를 재검산했고, DNS 문제로 정식 workbench 계약 검사는 미실시였다. [122 검사 기록][ev122] · [123 검사 기록][ev123] · [121 인계][h121] · [124 재검산][check124]

## 30회까지의 결론을 이은 설계 판단

| 설계 질문 | 앞선 연구에서 확보한 근거 | 31회까지 설계자가 쓸 수 있는 판단과 남은 공백 |
| --- | --- | --- |
| 선례가 새 선택을 만드는가 | 010은 분야 단서가 있을 때 원리 7군을 찾았다. 단서 없는 033은 144쌍 중 넓은 지지 1쌍, 당시판 지지 0쌍이었다. 022에서 미인지→변경→시행이 모두 이어진 사건은 0/24였다. 109의 12개 선택·27개 시험 제안은 원 프로젝트에서 실행되지 않았다. 117 잠정 8건에서도 직접 귀속을 확정하지 못했다. | 121은 구체적인 문안 수정과 API를 유보한 순서를 복원했다. 목표 선례의 직접 귀속은 0/6이다. 작성자가 시도해 본 기능의 쓸모, 당시 몰랐다는 진술, 실제 구현 변경, 비용은 각각 다른 증거를 요구한다. |
| 부분 입력에 어느 문맥이 필요한가 | 020은 주장 72/73을 전달해도 충돌 완전 해소 2/16, 074는 구성 입력에서 추가 값으로 8/8을 구별했다. 111은 동의어 변경 뒤 두 방식 모두 기준 정합 0/6이었다. 119의 자연 도표 6건은 원요구만으로 자동 정확 0/6, 인접 레코드와 직접 참조는 각각 3/6이었다. | 123의 같은 x좌표에서 막대와 바탕이 다른 범주를 골랐다. 시작 시 선택 상태와 실제로 눌린 객체는 입력 후보가 된다. 이를 사용자에게 되묻는 것이 전체 작업에 드는 비용과 효용은 미측정이다. |
| 직접 답과 쓸 만한 부품이 어디서 사라지는가 | 076의 자연 6요구×20후보는 직접 적격 0, 080은 자료집 확장으로 자연 1/5·교정 3/5가 양성으로 바뀌었다. 118은 활성 32개 요청–언어의 직접 10쌍 중 9쌍을 조사했다. 세 자리를 채우는 정책은 직접 9·일부 7·명시 충돌 15였고 조작·대상 근거를 요구하면 직접 8·일부 0·충돌 0이었다. 영어 Filter Mask는 표시에서, 같은 기능의 한국어 진단은 조사 단계에서 빠졌다. | 122의 실제 한국어 질문 진단에는 자료집만으로 전체 요구를 채우는 기능이 없었다. 원문 API 이름으로 찾은 세 하위 조작, 한국어 별칭이 되찾은 구성 답, 별칭 때문에 밀려난 구성 답을 따로 볼 수 있다. |
| 판·주소·인용을 어디까지 보존하는가 | 055는 예전 판단 4/4, 다음 판 판단 0/4였다. 071은 조각과 설정으로 옛 자료 22/22를 복원했고 075는 후보 전체가 없어 유일성·공동 1위를 각각 16/16 보류했다. 106에서는 살아 있는 주소가 옛 집단 점수의 용도를 잃었다. 120에는 직접 절보다 앞에 있어 놓친 월 번호 규칙이 있었다. | 121에서 인용 때 공개된 판을 복원해도 저자가 읽은 정확한 판은 6/6 미확인이다. 124에서 읽은 면 13개를 고정 원전과 맞출 수 있었지만, 사후에 다른 판으로 얻은 실행 결과는 당시 독자의 근거에 더할 수 없다. |
| 한 줄 설명이나 둘째 링크가 판단을 돕는가 | 021의 같은 두 절 예산에서 충분한 근거는 주소만 6/23, 절 목록 9/23, 조건에 맞춘 절 14/23, 잘못 붙인 절 8/23이었다. 116의 새 목차 단서는 2/6에서 경로를 바꿨다. 120의 자연 6건은 직접 절에서 인접 정의에 도달할 수 있었지만 완전 근거는 6건 모두 미확인이었고 실제 독자 비교는 0건이었다. | 124에서 이 여섯 건에 한 독자의 열람과 답을 연결했다. 핵심 처방은 원답에 이미 있었고, 읽은 자료가 특정 하위 주장만 보강했다. 034에서 부분 시간은 380→57초, 전체 시간은 849→847초였듯, 열어 본 수와 전체 작업시간도 따로 관측해야 한다. |
| 어떤 기능을 연결하거나 고치면 무엇을 보존하는가 | 078은 따로 쓸 수 있는 기능을 연결했을 때의 실패를 보였다. 103은 외관 10/10 보존과 8자리의 텍스트 선택 소실을 함께 기록했다. 107은 한 발생만 편집할 때 공유 정의 0/6·위치 지정 6/6이었고 119의 차트는 로컬 설정과 공유 설정이 같은 정지 화면에서 다른 조작 결과를 냈다. | 123은 같은 초기 화면에서 선택 폭·범주·색을 각각 재측정했다. 지도 피처와 화면 중심, 오디오 클립과 시간 선택도 비슷한 판단 대상이다. 지도와 오디오에서 차트 단서가 추가로 얼마나 예측하는지는 실행할 문제로 남았다. |

앞선 표본의 정의와 출처는 [REVIEW-30][prev]에 있다. 114의 같은 144쌍에서 ‘충돌’ 138은 118의 명시적 반박 기준으로 충돌 7·미확인 131로 갈렸다. 나머지 6쌍은 두 기준에서 모두 일부였다. 119의 자연 대조 M3994 원형 MG 좌표는 두 브라우저 로그의 **y=11.71875**를 이어 쓴다. 결과 요약에는 11.65625로 적혔지만 국소 변경에서 좌표가 유지되고 공유 변경에서 y=275가 된 판정은 같았다. 이 정의와 정정을 유지해야 후속 비교의 분모가 맞는다. 저장할 원문의 양, AI 전처리, 상시 수집, Studio 입력 계약은 아직 열려 있다. [이전 검토의 원장 대조][prev] · [제품 브리프][goal]

## 새 DONE의 근거와 서로 어긋나는 판정

### 121 · 공개된 선례의 기능과 그것을 읽고 내린 결정

원저작 31개를 읽은 연구다. 근접 3사건과 대조 2사건의 주장 17행을 다시 세면 D1 11·D2 5·탐색 중 나온 경쟁 설명 D2+ 1이다. 당사자가 특정 선례를 이유로 지목하고, 같은 선택의 전후 변경과 당시 적용 가능한 원전을 함께 확인한 D3는 목표 6개에서 0이다. 두 사건의 문구 수정, 세 사건의 초안 결정 변화 여섯 건, 두 사건의 후속 시험 정의는 확인됐다. 실행 영수증과 실제 노동시간은 확보한 건수가 각각 0이다. 선별한 근접·대조 사건만으로 영향의 빈도를 계산할 수 없다. [주장별 등급과 반증][claims] · [당시판 6행][versions] · [분모와 역할별 반환][r121]

117에서 남았던 당대 crate 세 건은 io-mux 1.4.0, bytemuck의 Pod 1.12.3, enum_dispatch 0.3.9까지 좁혀졌다. Rust #3362의 출력 API 폐기 유보는 1월 13일이고, io-mux 인용과 순서 보장 표현 완화는 1월 19일이다. Rust #3367에서 enum_dispatch 최초 공개 언급은 종전에 잡은 1월 8일보다 이른 **1월 6일 02:12:25 UTC**다. wrapper 반례는 그 언급 뒤이면서 Pod 인용 전이고, 나중의 TODO와 종료 기록만으로 선택의 원인을 가를 수 없다. [최초 언급 원문][rust] · [사건 순서][hist]

PEP #2997에서는 명세를 수정한 커밋 시각이 mypy 예시 인용보다 **314초 먼저**다. 공개 push 시각은 미확인이다. 9월의 전환에는 작성자가 별도 사용례 부족과 피드백을 들었고, 10월 축소에는 별도 PEP와 Pyright의 narrowing 변경이라는 설명이 남는다. 설계자에게는 이런 선례도 특정 보존 조건이나 시험을 찾는 링크로 줄 수 있다. 최초 발견·도입·비용 절감에 대한 증거는 여전히 비어 있다. [수정 커밋][p4commit] · [인용 댓글][p4quote] · [역할별 반환 근거][roles]

### 122 · 한국어 질문에 대한 별칭 효과를 어디까지 셌는가

정규 모집 8자리는 2025·2024 생성 UTC 창의 경계를 확인하지 못해 모두 공석이다. 활동순 목록은 생성순이 아니고 일부 페이지가 빠졌다. 별도 경로로 직접 읽은 포럼 원글 13건 중 10건을 진단했다. 16기능과의 160쌍은 직접 0·일부 17·명시 충돌 14·미확인 129다. 공식 시험을 바탕으로 만든 9문장의 144쌍은 직접 12·일부 5·충돌 19·미확인 108이다. 76조회와 두 재생은 이 고정 자료에서의 순위를 설명한다. 실제 질문 집단의 직접 회수율은 분모가 없다. [모집 원장][frame] · [전수 판정][truth] · [네 조건 집계][counts]

| 조건 변화 | 실제 한국어 질문 진단 10건 | 시험 기반 구성 9건 |
| --- | --- | --- |
| 원문을 유지하고 별칭 OFF→ON | 표시 일부 5→5. 12개 활성 별칭의 완전 어절 일치가 없었다. | 직접 12쌍 중 조사 4→9, 표시 3→8 |
| 영어 심벌을 가리고 별칭 OFF→ON | 표시 일부 2→2. O5952의 reshape·view·clone을 가리면 앞의 둘은 조사 4·5위, clone은 조사 밖으로 갔다. | 직접 12쌍 중 조사 3→9, 표시 3→8. C09는 ‘전치’로 복구했지만 C01은 BatchSampler가 표시 3위에서 조사 4위로 밀렸다. |

영어 이름을 가리면 작성자가 이미 비교한 방법도 함께 사라진다. C06에서는 거절한 ‘복사본’이 충돌하는 clone을 1위로 올렸다. 그리고 기존 전처리는 한글 연속 어절이 사전에 **정확히** 있을 때만 저장한다. 따라서 공개 질문의 ‘일치 0’만으로 조사가 붙은 표현까지 없었다고 단정할 수 없다. O5952의 원 환경은 torch 2.2.2·Core ML이고 공식 CPU 2.5.1 검산은 그 변환의 추론 일치를 검사하지 않았다. [변화별 원장][effects] · [전처리 규칙][prep] · [저자 입력 범위][reqs]

### 123 · 같은 화면에서 1픽셀을 움직인 두 결과

본 48행에서 첫 이동의 예상 선택 범위와 관측 범위 차이는 32행에서 0, 16행에서 101 CSS px였다. 16행은 빈 선택에서 막대를 누른 12행과, 기존 선택을 접은 뒤 막대가 드러난 공유 설정 4행이다. 같은 x=110에서 1픽셀 오른쪽으로 움직였을 때 원형 SVG의 막대 위에서는 범위 [9,10]에 1월, 바탕 위에서는 [110,111]에 6월이 잡혔다. 두 경우 모두 실제 범위를 범주로 바꾼 계산은 맞았다. 101은 손이 움직인 거리와 구별되는 좌표 차이다. 본 48행·대조 36행은 한 Chromium과 같은 입력 조건의 반복이다. [막대 원기록][mark] · [바탕 원기록][plot] · [본·대조 원장][runs]

로컬 색 설정은 원형과 비교한 16/16에서 이동과 최종 범주를 유지했다. 기존 선택에서 공유 설정의 이동을 끄면 8/8의 궤적이 달라졌다. 119의 정지 화면과 신호 주입 시험에 실제 포인터 경로가 추가된 셈이다. 기능 절의 1순위가 바뀐 32/48은 작업자가 정한 전후 규칙의 결과다. 원 GIF, 저자의 초기 선택과 런타임·데이터, 어느 변경을 원했는지와 실제 채택은 미확인이다. OpenLayers의 피처 이동과 지도 중심 이동도 이 단계에서는 공식 예제·소스에서 도출한 예측이다. [기능 절 선택 원장][decision] · [타 분야 근거][cross] · [환경과 한계][r123]

### 124 · 자료에 도달한 뒤 어떤 주장이 바뀌었는가

한 AI 독자의 여섯 자연 요청에서 18번의 열람 기회 중 첫 절 열기 6·추가 시험 열기 3·기존 절 계속 읽기 4·조기 중단 5를 원장에서 다시 셌다. 실제 읽은 면은 13개, 18,897자다. 추가 시험이 제시된 세 사건은 모두 열었다. 자기 채점은 첫 절 직후와 최종 모두 부분 3·정당 보류 3이었다. 핵심 처방 수정·완전 근거·위험한 확정은 각각 0/6이다. P2의 추가 시험은 명시 구분자와 명시 필드명을 쓴 매핑까지 지지한다. 첫 줄 `SEP=;`를 메타데이터로 볼 조건은 남는다. P1에서는 첫 절을 계속 읽기만 해도 dialect 설명이 늘었고, 실제 파일의 끝은 확인되지 않았다. J2는 JSON 파서의 계약을 확인하면서도 YAML 요구 전체는 ‘정당 보류’, P1은 파일 끝을 확인하지 못한 채 ‘부분’이었다. 전체 등급만으로는 어느 하위 주장이 입증됐는지 알 수 없다. [열람 원장][trail] · [시점별 채점][score] · [원전과 읽은 면 대조][faces]

여섯 사건의 핵심 조작은 이미 원답에 있었다. 같은 사건의 독립 B/C 짝은 0이고, 같은 문서 계보의 첫 노출만 남기면 추가 링크군 2·비교군 0이다. 한 번에 여러 사건의 면을 봤고 P2·P3는 첫 본문이 동일했다. 실제 열람은 보관된 문서면을 읽은 것이며 사후 채점자와 독자는 같은 세션이다. 사후 jq 1.7에서는 J3의 원 정규식도 기대값을 냈지만, 질문자가 보고한 1.6 환경의 원인은 미확인이다. P3의 작은 입력에서는 빈 값과 중복 키가 다른 결과를 냈지만 실제 81열 파일은 없었다. 이 증거로 사람의 정답률·전체 소요시간이나 둘째 링크의 평균 효과를 계산할 수 없다. [사후 실행 원값][probes] · [비교 가능한 분모][r124]

## 다음 작업 네 건

| 독립 작업 | 선행 | 이번에 새로 얻을 증거 | 판정을 뒤집을 관측 |
| --- | --- | --- | --- |
| AF-RES-125 · web-pro | 121 | 로컬 구현을 지운 병합 패치에서 역으로 공급 기능의 출시·소비자의 최소 지원판·발견 진술을 추적한다. | 기능이 뒤늦게 출시됐거나 최소판을 올릴 때까지 쓸 수 없었다면 늦은 발견으로 귀속할 수 없다. |
| AF-RES-126 · codex-cloud | 122 | 고정된 한국어 별칭 12개의 완전 어절, 조사 허용, 부분문자열 일치를 같은 원문과 같은 16기능에서 재생한다. | 추가 적중이 거절한 대안이나 다른 단어이고 유용한 부품을 밀어냈다면 표면형 일치의 순위 이득을 다시 센다. |
| AF-RES-127 · codex-cloud | 123 | 차트에서 얻은 ‘실제 대상과 보존할 상태’ 단서로 OpenLayers의 드래그가 피처·지도 중심 중 무엇을 움직일지 예측하고 브라우저로 검증한다. | 같은 픽셀·선택 상태라도 처리 순서에 따라 둘 다 또는 어느 것도 움직이지 않거나, 지도 문서만으로 이미 같은 예측이 나오면 전이의 기여가 달라진다. |
| AF-RES-128 · web-pro | 124 | 독자가 실제 본 면만으로 기존 18답을 새로 판독하고, 빠진 조건을 채울 둘째 원문을 같은 글자 예산에서 찾아 비교한다. | 잘 맞는 제목의 시험이 입력 조건을 빠뜨리거나 첫 면만으로 이미 충분하다면 둘째 링크의 추가 근거는 없다. |

새 작업은 각각 완료된 선행 하나만 사용하며 서로의 결과를 기다리지 않는다. 작업자별 입력판, 필수 표, 원문 수, 반증 절차와 인계 기준은 [NEXT_TASKS-31.json](NEXT_TASKS-31.json)에 있다.

[goal]: https://github.com/laadkke-arch/agentflow-open/blob/4a92e22c5356dc7ea2b715f671077e8ab63b2835/docs/product/RESEARCH_BRIEF.md
[trail]: https://github.com/laadkke-arch/agentflow-open/blob/7dd19f7fdac69b9dad4d6170ea247580b857f9b4/docs/workstreams/research/AF-RES-124/trails.jsonl
[score]: https://github.com/laadkke-arch/agentflow-open/blob/7dd19f7fdac69b9dad4d6170ea247580b857f9b4/docs/workstreams/research/AF-RES-124/scores.csv
[prev]: https://github.com/laadkke-arch/agentflow-open/blob/51f09bc323ff3517464da69fa7486eb18932cc9d/docs/workstreams/planning/REVIEW-30.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/13be736df17a4c697880f57029d16de38db061dd/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/4a92e22c5356dc7ea2b715f671077e8ab63b2835/docs/automation/dot-control.json
[rules]: https://github.com/laadkke-arch/agentflow-open/blob/4a92e22c5356dc7ea2b715f671077e8ab63b2835/docs/RESEARCH_WORKFLOW.md
[h121]: https://github.com/laadkke-arch/agentflow-open/blob/fe74c5eec9b3f2dd833409d59460c0b82f4cfe79/docs/workstreams/research/AF-RES-121/HANDOFF.md
[r121]: https://github.com/laadkke-arch/agentflow-open/blob/97e69009bd64d56a96d12ed5d7e6614e395f0fce/docs/workstreams/research/AF-RES-121/RESULT.md
[h122]: https://github.com/laadkke-arch/agentflow-open/blob/1fe299790d14a6bd93a101c005ba0802368cba50/docs/workstreams/research/AF-RES-122/HANDOFF.md
[r122]: https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/RESULT.md
[h123]: https://github.com/laadkke-arch/agentflow-open/blob/7554304d725082275661cdd011ad4f4472a00438/docs/workstreams/research/AF-RES-123/HANDOFF.md
[r123]: https://github.com/laadkke-arch/agentflow-open/blob/0a4acb5368e2f064e9b3eb21b52d219de262440f/docs/workstreams/research/AF-RES-123/RESULT.md
[h124]: https://github.com/laadkke-arch/agentflow-open/blob/0c1b5733c8ddc76341c6da872e8b405e6ed38963/docs/workstreams/research/AF-RES-124/HANDOFF.md
[r124]: https://github.com/laadkke-arch/agentflow-open/blob/7dd19f7fdac69b9dad4d6170ea247580b857f9b4/docs/workstreams/research/AF-RES-124/RESULT.md
[ev122]: https://github.com/laadkke-arch/agentflow-open/blob/7efbd4ba68e12ca05d9acfd48a7ce3be0541f64f/docs/workstreams/research/AF-RES-122/evidence/acceptance-evidence.json
[ev123]: https://github.com/laadkke-arch/agentflow-open/blob/37e7429e6060e2771c5cbd9c768f125db99f9bd5/docs/workstreams/research/AF-RES-123/evidence/acceptance/RECEIPT.md
[check124]: https://github.com/laadkke-arch/agentflow-open/blob/3ffca81ab76f3096afd923645abd2db255649a38/docs/workstreams/research/AF-RES-124/evidence/result-readback.json
[claims]: https://github.com/laadkke-arch/agentflow-open/blob/97e69009bd64d56a96d12ed5d7e6614e395f0fce/docs/workstreams/research/AF-RES-121/claims.csv
[versions]: https://github.com/laadkke-arch/agentflow-open/blob/97e69009bd64d56a96d12ed5d7e6614e395f0fce/docs/workstreams/research/AF-RES-121/versions.csv
[rust]: https://github.com/rust-lang/rfcs/pull/3367#issuecomment-1373050026
[hist]: https://github.com/laadkke-arch/agentflow-open/blob/97e69009bd64d56a96d12ed5d7e6614e395f0fce/docs/workstreams/research/AF-RES-121/timeline.csv
[p4commit]: https://github.com/python/peps/commit/f425e498e21b49cbfea03f5c1bf2152672d19760
[p4quote]: https://github.com/python/peps/pull/2997#discussion_r1104123131
[roles]: https://github.com/laadkke-arch/agentflow-open/blob/97e69009bd64d56a96d12ed5d7e6614e395f0fce/docs/workstreams/research/AF-RES-121/fields-and-returns.md
[frame]: https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/frame.csv
[truth]: https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/truth.csv
[counts]: https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/table3.csv
[effects]: https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/effects.csv
[prep]: https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/prepare.py
[reqs]: https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/requests.jsonl
[mark]: https://github.com/laadkke-arch/agentflow-open/blob/0a4acb5368e2f064e9b3eb21b52d219de262440f/docs/workstreams/research/AF-RES-123/evidence/main/M-original-svg-empty-mark-1.json
[plot]: https://github.com/laadkke-arch/agentflow-open/blob/0a4acb5368e2f064e9b3eb21b52d219de262440f/docs/workstreams/research/AF-RES-123/evidence/main/M-original-svg-empty-plot-1.json
[runs]: https://github.com/laadkke-arch/agentflow-open/blob/0a4acb5368e2f064e9b3eb21b52d219de262440f/docs/workstreams/research/AF-RES-123/runs.jsonl
[decision]: https://github.com/laadkke-arch/agentflow-open/blob/0a4acb5368e2f064e9b3eb21b52d219de262440f/docs/workstreams/research/AF-RES-123/decisions.csv
[cross]: https://github.com/laadkke-arch/agentflow-open/blob/0a4acb5368e2f064e9b3eb21b52d219de262440f/docs/workstreams/research/AF-RES-123/evidence/cross-domain.md
[faces]: https://github.com/laadkke-arch/agentflow-open/blob/7dd19f7fdac69b9dad4d6170ea247580b857f9b4/docs/workstreams/research/AF-RES-124/evidence/projection-remote-check.json
[probes]: https://github.com/laadkke-arch/agentflow-open/blob/7dd19f7fdac69b9dad4d6170ea247580b857f9b4/docs/workstreams/research/AF-RES-124/evidence/probe-stdout.jsonl
