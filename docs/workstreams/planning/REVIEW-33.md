# REVIEW-33 · 기존 기능의 링크가 실제 선택을 바꾼 범위

선택한 지도 피처를 끌 때 **어느 판에서 피처가 움직이고 어느 판에서 지도 중심이 움직이는지**는 배포 파일과 입력 로그로 확인됐다. 반면 기능을 몰랐던 최초 작성자가 링크를 받아 재작업을 줄인 사건은 이번에도 입증되지 않았다. 링크를 본 뒤 답이 달라진 관측은 한 건 있다. 독자는 추가 도구를 써도 될 때의 선택지를 하나 더 냈고, 원 작성자는 그 도구를 추가하길 원치 않았다. 이 결과를 설계에 쓰려면 링크가 가리키는 동작, 독자가 바꾼 답, 작성자가 받아들인 선택을 각각 기록해야 한다. [지도 실행 원장][runs] · [교체 귀속 원장][dec] · [독자의 원래 답][answers] · [작성자의 후속 발언][jq]

## 이번 검토의 범위

2026-11-24 UTC에 `work/planning@52a75d5`에서 최신 REVIEW-32를 먼저 읽었다. 32차가 사용한 통합판 `f5279ca`와 이번 `42260ca`의 진행표를 ID별로 비교했다. 기존 126행은 모든 필드가 같고 AF-RES-129~132 네 행이 새 DONE이다. 현재 총 130행 중 DONE 128, BLOCKED 2다. 연구 128건 중 DONE은 126건이고 018·035가 BLOCKED다. 나머지 DONE 2건은 연결 시험이다. 중앙 DONE 128행의 `acceptance_evidence`는 모두 빈 배열이다. [32차 누적 검토][prev] · [이전 진행표][oldreg] · [이번 진행표][reg]

| 새 DONE | 등록된 인계판 · 작업자 판정 | 대조한 결과판 | 원장에서 다시 확인한 범위 |
| --- | --- | --- | --- |
| 129 · 기존 순회 기능으로 교체 | [86369e7 · PARTIAL][h129] | [f288c8a][r129] | 지정 모듈 24행, 전환 후보·공석·대조 16행, 결정 14행. 원전 89행, 적격 고유 37저작(같은 구현 계보를 더 합치면 36) |
| 130 · 한국어 조사 결합 별칭 | [56e82ef · PARTIAL][h130] | [2c901ef][r130] | 모집 96행 중 실제 포럼 첫 글 열람 1건. 출처 76행 중 열람 성공 8건, 최소량에 산입할 저작 7개 |
| 131 · 지도 옵션의 판 경계 | [5cf6899 · DONE][h131] | [de62ead][r131] | 안정판 64개, 브라우저 본 48·대조 16·보충 12·정착 상태만 비교한 8행. 적격 고유 37저작 |
| 132 · 둘째 원문을 본 독자 | [510e9db · PARTIAL][h132] | [99be7be][r132] | 한 독자의 6사건×3답, 열람 과정 46행, 본시험 주장 21행과 타 분야 6행. 적격 원전 29행·고유 24저작 |

검토 시 네 작업 브랜치의 head가 각각 등록 SHA와 일치했고 각 head의 RESULT.md는 표의 결과판과 같은 Git blob이었다. 아래 새 수치는 고정 원장을 재집계한 값이다. 브라우저와 두 checkout에서의 재생은 131 작업자가 수행했다. 129·130은 당시 checkout/DNS 문제, 132는 웹 전용 환경으로 지정 세션 검사를 실행하지 못했다. 129의 이력 결측, 130의 모집 실패, 132의 독립 채점 부재는 각각 다른 한계다. [129 자기검사][check129] · [130 접근·검산][check130] · [131 실행 영수증][check131] · [132 원격 재집계][check132]

## 1~32차에서 이어 온 설계 판단

| 제품 질문 | 이전에 확보한 증거 | 33차에 남는 판단 |
| --- | --- | --- |
| 선례가 실제 선택을 바꾸는가 | 010은 분야 단서로 원리 7군을 찾았다. 단서가 없는 033은 144쌍 중 넓은 지지 1, 당시판 지지 0이었다. 022의 미인지→변경→시행은 0/24였다. 109의 시험 제안 27건은 현장 실행까지 이어지지 않았고 117·121도 원저자의 직접 귀속을 확보하지 못했다. 125가 패치를 읽은 48건에는 적격 런타임 교체가 없었다. | 129는 실제 일부 교체와 후기 리뷰어의 인지를 확인했다. 최초 작성자에게 그때 같은 기능이 가능했는지, 링크 덕분에 얼마나 덜 일했는지는 미확인이다. |
| 부분 설계에서 무엇을 더 물어야 하는가 | 020은 주장 72/73을 전달해도 충돌을 온전히 푼 사례가 2/16이었다. 074의 구성 입력은 추가값으로 8/8 구별했으나 111의 동의어 변경 뒤 정합은 두 방식 모두 0/6이었다. 119의 자연 도표는 원요구만으로 정확 0/6, 인접 레코드와 직접 참조가 각 3/6이었다. 123은 같은 x에서 1px를 끌어도 막대와 배경에서 다른 달이 선택되는 것을 측정했다. | 조작할 대상·유지할 값에 더해 설치판과 이미 준비된 선택 목록이 답을 가를 수 있다. 실제 프로젝트마다 확인 질문 한 번이 절약하는 노력은 미측정이다. |
| 후보를 찾은 것과 화면에 보여 준 것 사이에 무엇이 빠지는가 | 076의 자연 6요구×20후보에서는 직접 적격 0, 자료집을 넓힌 080은 자연 1/5·교정 3/5에서 적격을 얻었다. 118에서 조작·대상 근거를 요구하자 표시된 직접·일부·충돌이 9·7·15에서 8·0·0이 됐다. 122의 한국어 진단 10건은 16기능 내 완전 답이 없었다. 126의 공개 10건은 별칭 적중 0, 새 구성문은 조사 허용으로 각 뷰에 직접 3개와 충돌 1개가 함께 유입됐다. | 130에서 새 공개 질문의 적격 여부 자체를 판정하지 못했다. 구성문 손익, 원문에서 근거를 갖춘 후보 수, 화면에서 밀려난 후보 수에는 각각의 분모가 필요하다. |
| 링크와 판 정보로 무엇을 재현할 수 있는가 | 055는 옛 판단 4/4를 복구했고 다음 판 판단은 0/4였다. 071은 원문 구간과 설정으로 옛 자료 22/22를 복원했다. 075는 전체 후보가 없어 유일성과 공동 1위를 각각 16/16 보류했다. 106은 주소가 살아도 옛 점수의 쓰임이 사라질 수 있음을 보였다. 121에서는 인용 시점 공개판을 알더라도 저자가 실제 읽은 판은 6/6 미확인이었다. | 131은 같은 이름의 옵션에서 행동이 바뀐 정확한 안정판을 찾았다. 어떤 변경 신호를 확인해야 링크의 판단을 갱신할 수 있는지와 그 비용은 별도 질문이다. |
| 짧은 설명과 추가 원문이 답이나 시간을 바꾸는가 | 021의 두 절 예산에서 충분한 근거는 주소만 6/23, 절 목록 9/23, 목적에 맞춘 절 14/23, 잘못 붙인 절 8/23이었다. 034의 부분 시간은 380→57초, 전체는 849→847초였다. 116·120은 탐색 경로·인접 정의를 찾았고, 124의 AI 독자 1명은 추가 시험 3개를 열어도 핵심 처방 수정이 0/6이었다. 128의 기존 답 18개 재판독은 이전 주분류와 9/18 일치했다. | 132에서 실제 추가 열람과 조건부 답 변화가 같은 독서 기록에 연결됐다. 여섯 사건 모두 핵심은 유보됐다. 사람의 채택·시간, 자료를 더 보여 줘서 생긴 평균 효과는 미확인이다. |
| 기능을 합치거나 일부만 편집할 때 무엇이 남는가 | 078은 따로 쓰던 기능의 결합 실패를 보였다. 103은 외관 10/10 보존과 8자리 텍스트 선택 소실을 함께 기록했다. 107의 한 발생 편집은 공유 정의 0/6·위치 지정 6/6이었다. 119·123은 차트의 로컬·공유 설정을 나눠 관측했고 127은 처리 순서에 따라 피처 좌표와 지도 중심이 함께 움직임을 관측했다. | 131은 순서를 고정하고 판에 따라 어느 값이 보존되는지를 분리했다. 여러 피처를 한꺼번에 편집하는 경우와 원 작성자의 앱에서의 결과는 미확인이다. |

이전 수치와 정정의 출처는 32차 누적 검토에 있다. 114의 ‘충돌’ 138/144는 118의 명시 반박 기준으로 충돌 7·미확인 131이며 나머지 6은 일부다. 119의 M3994 원형 MG 좌표 y는 두 로그의 11.71875를 쓴다. 공유 변경 뒤 y=275라는 판단은 같다. 연구 원장의 열 이름은 결과를 추적하기 위한 약속이다. 제품의 최소 저장량, 상시 수집 여부, AI 전처리, AgentFlow Studio 입력 계약은 여전히 설계자가 선택할 문제다. [32차 근거와 정정][prev] · [제품 연구 브리프][goal] · [운영 규칙][workflow]

## 새 DONE 네 건의 증거와 불일치

### 129 · 교체는 일어났고 처음 몰랐던 시점은 입증되지 않았다

more-itertools와 NetworkX의 pairwise·batched 네 조합에서 6개 연말판씩 지정 모듈을 읽었다. 인접 연말 상태는 20구간 중 6곳에서 달랐다(2·3·1·0). 사전 8자리 중 이름을 붙일 수 있었던 후보는 5, 공석은 3이다. 추가 후보 6행과 이전 음성 대조 2행을 합친 것이 전환 원장 16행이다. 12개 배포물과 태그의 바이트 동일성, 20구간의 모든 경로·중간 변경, NetworkX의 다른 경로에 있는 batched는 미확인이다. 실제로 more-itertools에서 연말 사이에 이름과 계약이 바뀐 사례가 있었다. 연말에 같은 상태였다고 중간에 교체가 없었다고 셀 수 없다. [연말 모집][snap] · [전환과 공석][changes] · [판독 구간][read129]

NetworkX #8201은 비순환 경로를 표준 pairwise로 바꾸고 순환 경로를 남겼다. 원래 구현은 표준 안정판이 나오기 전에 이미 있었다. 나중에 다른 사람에게 이 기능을 배웠다고 말한 사람은 리뷰어였고, 변경 작성자는 성능을 들었다. 호출부 전체를 바꾸자는 제안도 병합본에서 빠졌다. 제시된 벤치마크는 반복자를 **생성**하는 시간만 쟀다. more-itertools #784는 strict 옵션 때문에 Python 3.12에서 다시 자체 구현을 택했다. 10.0.0 통합 시점의 최소판 선언(≥3.7)과 배포 메타데이터(≥3.8)도 달랐다. 공개 함수의 존재, 구판에서도 유지되는 동작, 최초 작성자의 미인지, 실제 순회 시간과 사람의 노동시간에 각각 별도 근거가 필요하다. 자료집의 직접 귀속 양성은 없고 전체 발생률은 산출할 수 없다. [당사자·시점 원장][dec] · [NetworkX 변경][nx] · [리뷰어 발언][actor] · [strict 대체 경로][strict]

### 130 · 모집에 실패해 별칭의 손익을 판단할 표본이 없다

ID 6001~6064 중 열람한 첫 글은 6027 하나였고 제품 홍보여서 제외됐다. 나머지 63개는 원문의 존재와 적격 모두 미확인이다. 네 별칭에 대한 사이트 검색은 응답을 얻지 못했다. 원장의 B층 32행은 질의 4개×예정 순위 8개의 자리다. 96개 행은 96개 질문을 읽었다는 근거가 되지 않는다. 76개 출처 기록은 직접 열람 성공 8(홍보 1, 고정 PyTorch API·시험 7), 실패 67, 검색 조각 1이었다. 요구한 고유 원전 24개 중 7개가 적격이고 새 질문의 전수 판독·승격·순위 및 철도·도서관 대조는 미실시다. [모집 원장][frame] · [출처 원장][s130] · [사전 규칙][scope130]

7개 파일에서 확인한 것은 인덱스의 묶음과 샘플의 묶음, 형태 변환 성공과 저장공간 공유처럼 같은 말이 숨기는 출력 차이다. 어느 한국어 질문에서 해당 카드가 필요했는지, 조사 허용이 표시를 개선했는지, 유용한 후보가 밀렸는지는 계산할 수 없다. 여기서 필요한 보완은 같은 모집창의 실제 응답 확보와 독립 공개 표본의 판독이다. 접근 실패를 ‘적중 0’으로 바꾸면 126의 자연 질문 결과가 거짓으로 반복된다. [API 구간과 빠진 산출물][r130] · [재개 및 결측 판정][check130]

### 131 · 같은 위치에서 끌어도 설치판이 바뀌면 움직이는 대상이 달랐다

6.0.0~10.11.0 안정판 64개의 배포 모듈에서 목록과 두 옵션을 함께 적용한 판은 15, 목록을 우선한 판은 49였다. 경계는 6.6.1→6.7.0이고 공개시각순·버전순 63인접쌍에 이 계약의 되돌림은 없었다. 네 판에서만 브라우저 실측을 했다. 단일 Canvas 피처·같은 마우스 경로에서 선택 목록에 hit 피처를 넣고 filter를 거부로 둔 6.6.1에서는 피처 변화 (0,0), 중심 (−64,+36)이었다. 6.7.0에서는 지정한 두 콜백의 호출이 0회였고 피처 (+72,−40), 중심 (0,0)이었다. layers를 거부로 둔 셀에도 같은 경계가 있었고, 빈 목록에서는 네 판 모두 피처가 움직이지 않았다. [안정판 원장][rels] · [변경 커밋][changeol] · [6.6.1의 입력 로그][raw661] · [6.7.0의 입력 로그][raw670]

본 48행은 피처만 이동 16, 중심만 이동 32다. 127에서 둘 다 움직였던 경우는 처리 순서가 달랐고 131은 순서를 고정했다. 두 결과는 서로 다른 입력에 답한다. 두 checkout에서 일치한 84행 중 76은 이벤트·콜백, 8은 정착 상태만 비교했다. 다중 피처, 다른 렌더러, #9625 당사자의 실제 설치판·목록에는 직접 적용할 수 없다. 9개 링크 반환 시나리오에서 사용자 채택은 모두 미확인이다. 별도 분야 실행에서는 QGIS 활성 레이어의 편집 상태에 따라 도구 활성 여부가 달랐고, Audacity에서는 파형 안을 끌 때 시간 선택이, 핸들을 끌 때 클립 위치가 바뀌었다. 실제 누른 대상과 보존할 값을 함께 물어볼 근거다. [실행 원장][runs] · [재생 영수증][check131] · [반환 시나리오][returns] · [타 분야 실행][domain] · [원 작성자 발언][origol]

### 132 · 둘째 원문이 보탠 근거와 실제 작성자가 받아들일 수 있는 답이 갈렸다

새 대화의 AI 독자 한 명이 여섯 사건에서 요청만 본 답, 첫 면 뒤 답, 최종 답을 각각 봉인했다. 여섯 번 모두 둘째 면을 원했고, 제시한 4개를 모두 열었다. 첫 면 뒤 처방 수정은 0/6, 그 뒤에는 추가 열람 4건 중 조건부 후보 추가 1·근거만 보강 3이었다. 첫 면만 받은 대조에서도 2건 중 하나는 검사 방법이 구체화됐다. jq의 내부 YAML 사례에서 독자가 새로 제시한 fq 후보는 다른 실행기를 써도 좋다는 조건이 붙었다. 후속 발언에서 작성자는 추가 도구를 원치 않았다. 여섯 사건 모두 핵심 처방의 해결은 유보됐다. 새로운 아이디어, 좁게 지지된 주장, 실제 제약을 만족한 채택을 같은 성공으로 세면 이 차이가 사라진다. [봉인 답][answers] · [실제 열람][reading] · [주장별 근거][claims] · [요구를 밝힌 발언][jq]

실제 10면의 누적 분량은 11,958자였고 같은 본문을 한 번만 세면 9면·10,458자다. 첫 면만 받은 두 사건은 모두 Python, 새로 고른 둘째 면을 받은 두 사건은 모두 jq였다. 조건당 두 건, 한 독자의 자기채점이며 면 길이도 다르다. 실행 시각·도구 대기는 계측되지 않았다. 설명이 나아졌다는 자기평가나 열람 4/4는 사람의 선택·시간 또는 특정 둘째 면의 인과효과를 뒷받침하지 않는다. 사후 분야 대조는 1813년판 소설의 인쇄 1쪽과 스캔 8쪽, 같은 편곡의 총보·파트에서 제7마디 진입을 맞췄다. 이 여섯 주장도 독서 시험의 21개 주장과 분모를 따로 둔다. [배정과 면][assign] · [해제 뒤 근거][r132] · [원격 검산][check132]

## 다음 작업과 선택 이유

| 독립 작업 · 담당 | 선행 | 이번에 답할 질문 | 결과를 바꿀 관측 |
| --- | --- | --- | --- |
| AF-RES-133 · web-pro | 129 | 공개 리뷰에서 기존 기능 링크 제시 전후의 같은 작성자·코드를 추적하면 실제 채택이나 거절을 귀속할 수 있는가. | 이미 수정된 커밋·먼저 남긴 TODO·명시적 거절이 나오면 나중 링크에 준 공로를 거둔다. |
| AF-RES-134 · codex-cloud | 130 | 고정 포럼 창의 공개 응답을 복구하고 별도 GitHub 표본에서 같은 16카드를 재생하면 한국어 별칭으로 무엇을 얻고 잃는가. | 직접 후보 유입과 함께 충돌·좋은 후보 탈락이 일어나거나 포럼의 분모가 비면 표시 방침과 적용 모집단을 좁힌다. |
| AF-RES-135 · codex-cloud | 131 | 주소·문서 절·구현 변경 중 무엇이 기능 링크의 재검증 시점을 알려 주는가. 알려진 지도 경계와 별도 수치 축척의 실제 출력을 비교한다. | 주소가 유지된 채 출력이 변하거나 문구만 바뀌어 불필요한 검사가 늘면 재검증 기준과 비용을 수정한다. |
| AF-RES-136 · web-pro | 132 | 새 판독자가 18개 답을 단계·종전 점수 없이 판정할 때, 어떤 둘째 면이 핵심 조건을 해결했는가. | 좁은 근거에 동의하면서 핵심 해결에는 이견이 생기거나 제약이 뒤늦게 공개됐다면 종전 처방 변경의 의미를 좁힌다. |

129의 미열람 이력을 전부 채워도 최초 작성자의 인지를 알 수 없어서 133은 리뷰 사건에서 출발한다. 134는 접근 결측을 해결할 수 있는 별도 창을 둔다. 135는 이미 확립한 경계를 재사용해 장기 유지 비용을 묻는다. 136은 같은 독자의 채점에 다른 판독을 보탠다. 네 과제는 각각 이미 등록된 선행 한 건만 요구한다. 필수 표, 원전 최소량과 종류, 반례, 중간 커밋과 완료 판정은 각 작업의 brief 안에 있다. [33차 작업 지시문](NEXT_TASKS-33.json)

[runs]: https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/runs.jsonl
[dec]: https://github.com/laadkke-arch/agentflow-open/blob/86369e7091b3cb58bbea1e3277bee67967afeaa6/docs/workstreams/research/AF-RES-129/decisions.jsonl
[answers]: https://github.com/laadkke-arch/agentflow-open/blob/510e9db7742ea2edc09c17d0fd4e3e8fbf48ca49/docs/workstreams/research/AF-RES-132/answers.jsonl
[jq]: https://github.com/jqlang/jq/issues/2530#issuecomment-1411829108
[prev]: https://github.com/laadkke-arch/agentflow-open/blob/52a75d579f18444d5f419413704949fcde4528fc/docs/workstreams/planning/REVIEW-32.md
[oldreg]: https://github.com/laadkke-arch/agentflow-open/blob/f5279cabf578ae93dd2374adb4f6fb525ce06b9d/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/42260ca230e028e1303667be943b861a1d5953e4/docs/automation/dot-control.json
[h129]: https://github.com/laadkke-arch/agentflow-open/blob/86369e7091b3cb58bbea1e3277bee67967afeaa6/docs/workstreams/research/AF-RES-129/HANDOFF.md
[r129]: https://github.com/laadkke-arch/agentflow-open/blob/f288c8a0335be5d972c5782dccf021b5dd71e8af/docs/workstreams/research/AF-RES-129/RESULT.md
[h130]: https://github.com/laadkke-arch/agentflow-open/blob/56e82eff157e558db4db01acb321d2fcc83574a0/docs/workstreams/research/AF-RES-130/HANDOFF.md
[r130]: https://github.com/laadkke-arch/agentflow-open/blob/2c901ef834f23603f849b6a2e740321c7b8bc56f/docs/workstreams/research/AF-RES-130/RESULT.md
[h131]: https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/HANDOFF.md
[r131]: https://github.com/laadkke-arch/agentflow-open/blob/de62ead16f71041f0a1c3cc37c651a0de3d760a5/docs/workstreams/research/AF-RES-131/RESULT.md
[h132]: https://github.com/laadkke-arch/agentflow-open/blob/510e9db7742ea2edc09c17d0fd4e3e8fbf48ca49/docs/workstreams/research/AF-RES-132/HANDOFF.md
[r132]: https://github.com/laadkke-arch/agentflow-open/blob/99be7bebb9561756fea04621120dd020cecf40b3/docs/workstreams/research/AF-RES-132/RESULT.md
[check129]: https://github.com/laadkke-arch/agentflow-open/blob/86369e7091b3cb58bbea1e3277bee67967afeaa6/docs/workstreams/research/AF-RES-129/SELF_CHECK.md
[check130]: https://github.com/laadkke-arch/agentflow-open/blob/56e82eff157e558db4db01acb321d2fcc83574a0/docs/workstreams/research/AF-RES-130/SELF_CHECK.md
[check131]: https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/evidence/acceptance/RECEIPT.md
[check132]: https://github.com/laadkke-arch/agentflow-open/blob/510e9db7742ea2edc09c17d0fd4e3e8fbf48ca49/docs/workstreams/research/AF-RES-132/evidence/remote-check.json
[goal]: https://github.com/laadkke-arch/agentflow-open/blob/42260ca230e028e1303667be943b861a1d5953e4/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/42260ca230e028e1303667be943b861a1d5953e4/docs/RESEARCH_WORKFLOW.md
[snap]: https://github.com/laadkke-arch/agentflow-open/blob/86369e7091b3cb58bbea1e3277bee67967afeaa6/docs/workstreams/research/AF-RES-129/snapshots.csv
[changes]: https://github.com/laadkke-arch/agentflow-open/blob/86369e7091b3cb58bbea1e3277bee67967afeaa6/docs/workstreams/research/AF-RES-129/changes.csv
[read129]: https://github.com/laadkke-arch/agentflow-open/blob/86369e7091b3cb58bbea1e3277bee67967afeaa6/docs/workstreams/research/AF-RES-129/evidence/READ_RECEIPTS.md
[nx]: https://github.com/networkx/networkx/pull/8201
[actor]: https://github.com/networkx/networkx/pull/8201#issuecomment-3234991126
[strict]: https://github.com/more-itertools/more-itertools/pull/784
[frame]: https://github.com/laadkke-arch/agentflow-open/blob/56e82eff157e558db4db01acb321d2fcc83574a0/docs/workstreams/research/AF-RES-130/frame.csv
[s130]: https://github.com/laadkke-arch/agentflow-open/blob/56e82eff157e558db4db01acb321d2fcc83574a0/docs/workstreams/research/AF-RES-130/sources.jsonl
[scope130]: https://github.com/laadkke-arch/agentflow-open/blob/56e82eff157e558db4db01acb321d2fcc83574a0/docs/workstreams/research/AF-RES-130/SCOPE.md
[rels]: https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/releases.csv
[changeol]: https://github.com/openlayers/openlayers/commit/207fc99295cc6a126425dd5fcb3aaec1865bd424
[raw661]: https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/evidence/browser/main/main-6.6.1-04-r1.json
[raw670]: https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/evidence/browser/main/main-6.7.0-04-r1.json
[returns]: https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/returns.csv
[domain]: https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/evidence/cross-domain/README.md
[origol]: https://github.com/openlayers/openlayers/issues/9625#issuecomment-498282656
[reading]: https://github.com/laadkke-arch/agentflow-open/blob/510e9db7742ea2edc09c17d0fd4e3e8fbf48ca49/docs/workstreams/research/AF-RES-132/reading.jsonl
[claims]: https://github.com/laadkke-arch/agentflow-open/blob/510e9db7742ea2edc09c17d0fd4e3e8fbf48ca49/docs/workstreams/research/AF-RES-132/claims.csv
[assign]: https://github.com/laadkke-arch/agentflow-open/blob/510e9db7742ea2edc09c17d0fd4e3e8fbf48ca49/docs/workstreams/research/AF-RES-132/assignments.json
