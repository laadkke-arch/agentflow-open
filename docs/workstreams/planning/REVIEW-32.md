# REVIEW-32 · 기존 기능을 권할 수 있는 조건

기존 기능을 더 일찍 알려 주면 설계를 고치는 비용이 줄어드는가. 이번 네 작업에서 가장 분명한 관측은 **같은 지도 화면을 끌어도 처리 순서에 따라 피처만 움직이거나 지도 중심까지 함께 움직인다**는 것이다. 반면 소비자가 이미 쓸 수 있던 연산을 뒤늦게 발견해 자체 구현을 지운 본 사례는 이번 모집에서 확보하지 못했다. 한국어 별칭의 표시 이득은 구성문에서 나왔고, 둘째 원문이 새 독자의 답을 바꾸는지는 아직 측정되지 않았다. 이 차이가 어떤 링크를 누구에게 어떤 조건으로 권할 수 있는지를 결정한다. [제품 목표][goal] · [지도 실측][runs] · [교체 표본][changes] · [별칭별 손익][effects] · [둘째 원문 비교][bundles]

## 이번에 열린 작업과 검사의 범위

2026-11-24 UTC에 `work/planning@23bf07e`의 최신 [REVIEW-31][prev]을 먼저 읽었다. 그 검토가 쓴 통합판 `4a92e22`과 이번 통합판 `f5279ca`의 진행표를 ID로 결합했다. 기존 122행의 모든 필드가 같았고 AF-RES-125~128 네 행이 새 DONE이다. 현재 126행 중 DONE 124, BLOCKED 2다. 연구 124건 중 122건이 DONE이고 018·035는 BLOCKED다. 연결 시험 두 건은 DONE이다. 중앙 DONE 124행의 `acceptance_evidence`는 모두 빈 배열이다. 이전 작업의 결론은 31차 누적 검토에서 이어받았고, 이번에 원장을 다시 펼친 연구는 아래 네 건이다. [이전 진행표][old] · [이번 진행표][reg] · [운영 규칙][rules]

| 새 DONE | 등록 SHA의 인계 상태 | 작업자가 검사한 결과판 | 이번 검토에서 맞춰 본 단위 |
| --- | --- | --- | --- |
| 125 · 자체 구현 교체 | [3b3e37f · PARTIAL][h125] | [475723b][r125] | 모집 96행, 부모 대비 변경 48건, 결정 9행. 출처 원장 고유 저작 58개 중 발췌 4건 제외 시 54개 |
| 126 · 한국어 별칭의 경계 | [d2bfe8c · DONE][h126] | [abcdda4][r126] | 요청 31건의 원문·가림, 별칭 구간 48행, 새 대조의 기능 판정 192쌍. 고유 저작 38개 |
| 127 · 지도에서 실제 움직인 대상 | [50eb2d5 · DONE][h127] | [cee582b][r127] | 본 16·대조 12·보충 10행과 별도 파일럿 3회. 본 8개 조건의 예측과 반환 절. 고유 저작 37개 |
| 128 · 둘째 원문의 증명 범위 | [cdf5522 · PARTIAL][h128] | [3c8a3cf][r128] | 기존 답 18·주장 72·본문 조합 18개, 별도 대조 4개. 고유 저작 24개 |

검토 시 네 작업 브랜치의 head가 각 등록 SHA와 일치했고, 각 `RESULT.md`의 본문은 표의 검사판과 같았다. 이 검토의 수치는 GitHub에 보존된 원장에서 다시 셌다. CPU·브라우저의 실제 실행은 126·127 작업자가 했고 두 작업 모두 고정판의 명시 세션 검사를 기록했다. 125·128은 원격 자료 재검산을 마쳤으나 당시 checkout DNS 실패로 정식 세션 검사를 수행하지 못했다. [125 재검산][check125] · [126 실행 영수증][check126] · [127 실행 영수증][check127] · [128 재검산][check128]

## 1~31회에서 이어지는 설계 판단

| 제품 질문 | 앞서 확인한 결과 | 32회까지 쓸 수 있는 판단과 열린 조건 |
| --- | --- | --- |
| 선례가 실제 선택을 바꾸었나 | 분야 단서가 있는 010은 원리 7군을 찾았다. 단서 없는 033의 144쌍 중 넓은 지지 1, 당시판 지지 0이었다. 022의 미인지→변경→시행은 0/24였고, 109의 12개 선택과 27개 시험 제안은 원 프로젝트에서 실행되지 않았다. 117의 잠정 8건에 이어 121의 목표 연결 6개에도 직접 귀속이 없었다. | 121은 실제 명세 문구 수정과 API 유보 시점을 확인했다. 125는 공급 연산을 아는 것, 해당 지원판에서 쓸 수 있는 것, 런타임 교체가 병합되는 것이 서로 다른 사건임을 보였다. 설계자가 새 링크 때문에 구현을 바꾼 빈도와 절감 시간은 미확인이다. |
| 부분 설계에서 무엇을 더 물어야 하나 | 020은 주장 72/73을 전달했어도 충돌을 온전히 푼 것은 2/16이었다. 074의 구성 입력은 추가 값으로 8/8을 구분했다. 111의 동의어 변경 후 정합은 두 방식 모두 0/6이었다. 119의 자연 도표 6건은 원요구만으로 정확 0/6, 인접 레코드·직접 참조 각 3/6이었다. | 123은 같은 x에서 막대를 누르면 1월, 바탕을 누르면 6월이 잡히는 1px 드래그를 기록했다. 127에서는 지도 위 피처 ID를 알더라도 선택 목록과 이벤트 순서에 따라 보존값이 달라졌다. 어떤 질문 하나가 사용자의 총 작업을 줄이는지는 미측정이다. |
| 쓸 만한 부품은 조회와 표시 중 어디서 빠지나 | 076의 자연 6요구×20후보에 직접 적격은 0이었다. 080은 자료집을 넓혀 자연 1/5·교정 3/5에서 양성을 얻었다. 118의 세 자리 채우기는 직접 9·일부 7·충돌 15, 조작·대상 근거를 요구하면 8·0·0이었다. 영어 Filter Mask는 표시에서, 같은 기능의 한국어 진단은 조사에서 빠졌다. | 122의 한국어 진단 10건에는 16기능 중 완전 답이 없었다. 126은 같은 원문에서 조사 붙은 별칭까지 검사했다. 구성문에서 찾을 기회와 엉뚱한 링크를 표시할 위험을 동시에 확인했다. 공개 원문 집단에서의 직접 회수율은 여전히 분모가 없다. |
| 주소와 판 정보는 무엇을 보존하나 | 055는 옛 판단 4/4를 재현했지만 다음 판 판단은 0/4였다. 071은 조각과 설정으로 옛 자료 22/22를 복원했다. 075는 후보 전체가 없어 유일성·공동 1위를 각각 16/16 보류했다. 106에서는 주소가 살아 있어도 옛 집단 점수의 용도가 사라졌다. | 121의 인용 시점 공개판을 알아도 저자가 읽은 판은 6/6 미확인이었다. 127의 같은 이름 옵션은 두 판에서 적용 조건이 달랐다. 원문 주소에는 어떤 판·입력·목적에서 그 절이 성립하는지 함께 남길 필요가 있다. |
| 한 줄 설명과 둘째 링크가 답 또는 시간을 바꾸나 | 021의 같은 두 절 예산에서 충분한 근거는 주소만 6/23, 절 목록 9/23, 목적에 맞춘 절 14/23, 잘못 붙인 절 8/23이었다. 116은 목차 단서로 2/6의 경로가 바뀌었다. 120의 자연 6건에서는 인접 정의까지 갈 수 있었고 완전 근거는 미확인이었다. 124의 AI 독자 한 명은 제시된 추가 시험 3개를 모두 열었고, 한 사건의 세미콜론 매핑 근거를 더 얻었다. 핵심 처방 수정은 0/6이었다. | 128은 작게 확인된 주장과 핵심 예외의 유보가 한 답에 공존함을 보였다. 034의 부분 시간 380→57초, 전체 849→847초와 마찬가지로 열람 횟수·답 수정·전체 시간을 따로 측정해야 한다. |
| 기능을 조합하거나 편집할 때 무엇이 남나 | 078은 따로 쓰던 기능의 결합 실패를 보였다. 103은 외관 10/10 유지와 8자리 텍스트 선택 소실을 함께 기록했다. 107의 한 발생 편집은 공유 정의 0/6·위치 지정 6/6이었다. 119·123은 차트 로컬·공유 설정에서 화면과 조작 결과가 달라짐을 기록했다. | 127은 지도에서 피처 좌표와 뷰 중심을 따로 재서 둘이 동시에 변하는 경우를 찾았다. 부분 입력에 맞춰 바꿀 대상·보존할 대상·판별 가능한 조작을 연결하는 안이 남는다. 실제 이용자가 이 링크를 선택한 기록은 미확인이다. |

앞선 수치의 표본과 정의는 [31차 누적 검토][prev]에 연결되어 있다. 114의 ‘충돌’ 138/144는 118의 명시 반박 기준으로 충돌 7·미확인 131이었고, 나머지 6은 두 기준 모두 일부였다. 119의 M3994 원형 MG 좌표는 두 브라우저 로그의 y=11.71875를 적용한다. 요약의 11.65625와 달라도 공유 변경에서 y=275가 된 판정은 유지된다. 연구용 원장 형식과 미래 제품 DB는 별개다. 최소 저장량, 상시 수집 여부, AI 전처리, AgentFlow Studio 입력 계약은 계속 열린 설계 질문이다. [이전 정정과 근거][prev] · [제품 브리프][goal]

## 새 DONE에서 확인된 것과 증거가 끊기는 곳

### 125 · 교체 패치와 늦은 발견의 분모

제목으로 모집한 scikit-learn·Matplotlib의 고유 후보는 각각 47·41개였다. 각 24개를 읽은 변경 원장은 일반 패치 판독으로 기록된 43건, 발췌 4건, 병합 부모 대비 파일 변화가 없는 1건으로 나뉜다. 관측된 런타임 자체 계산→새 NumPy/SciPy 연산 교체는 0건으로, 본 사례 6자리가 전부 비었다. 대조는 명칭 변경과 OO 예제 정리 각 1건이었다. 전체 후보 88건 중 나머지 40건과 잘린 네 패치에는 부재 판정을 내릴 수 없다. 직접 귀속률의 분모는 0이다. [모집 순번][frame] · [변경 범위][changes]

scikit-learn #18930에서는 작성자가 시험 인자를 알게 된 발언과 시험 변경을 연결할 수 있다. CPython 최소 SciPy 0.19.1에는 새 가중치 인자가 없고, 공급 수식상 거리 3·가중치 4에서 p=1일 때 12로 같지만 p=2이면 옛 방식 12·새 방식 6이다. 수식 대조까지 했고 당시판 실행 로그는 없다. Matplotlib #19500은 기존 네 NumPy 호출을 유지하며 경고 억제 코드를 지웠다. 설치 최소판 선언과 런타임 검사가 어긋나던 흔적도 있다. 줄 수와 PR 경과일은 있으나 노동시간 자료는 없다. 인계를 따라 재검산할 때 주의할 점도 있다. 인계의 첫 diff 예시는 #19237의 명칭 변경이다. 가중치 사건은 #18930의 부모 `6b4f824`와 병합 `b7a48a0`를 사용해야 한다. [사건별 판정][decisions] · [가중치 병합][weight] · [경고 억제 제거][warning] · [인계의 명령][h125]

### 126 · 한국어 표면형을 찾은 뒤 무엇이 표시됐나

공개 첫 글 10건은 이전 발췌의 원문·영어 이름을 가린 사본 해시가 각각 10/10 일치했다. 별칭 없음(A), 완전 어절(B), 끝 어절에 조사 12형 허용(C), 끝 어절 내부 일치(D)를 적용해도 이 글들에서 별칭 적중은 0이었다. 표시된 일부 기능은 어떤 정책에서나 원문 5/17, 가림 2/17이었다. 122가 남긴 ‘조사가 붙어서 놓쳤을 가능성’은 이 10건과 고정 별칭 12개 안에서 해소됐다. 122의 정규 모집 8자리, 다른 공개 요청, 실제 클릭·이해는 검증되지 않았다. [원문·구간과 결과][r126] · [층별 분모][stats]

기존 구성문 9건에서는 두 뷰 모두 직접 표시가 A 3/12→B 8/12였고 C·D에서 더 늘지 않았다. 새로 만든 12문장의 192쌍은 직접 10·일부 7·명시 충돌 32·미확인 143이다. B→C에서 직접 표시는 원문 5→8, 가림 4→7이면서 각 뷰에 충돌도 하나 유입됐다. C→D에서는 직접 증가 없이 충돌 둘이 공석으로 들어왔다. ‘복사본을 원함’과 ‘복사본은 거절’ 모두 같은 복사 기능을 1위로 올렸고, ‘전치사’·‘뷰어’도 텐서 기능을 불렀다. 기존 C01의 가림에서는 거절한 기능이 올라 직접 후보가 표시 3위→조사 4위가 됐다. 248회 조회와 3,968개 점수는 31개 요청의 반복이다. 2.5.1 CPU의 인덱스/표본 및 공유/복사 시험에서 확인한 계약을 원 질문자의 Core ML 결과로 확장할 수 없다. [적격 원장][truth] · [구간 역할][matches] · [3,968개 점수][ranks] · [유입·탈락][effects] · [CPU 출력][cpu]

### 127 · 같은 지도 피처에서 두 처리기가 모두 받은 드래그

OpenLayers 10.11.0의 고정 Canvas에서 본 16행을 다시 세면 피처 좌표만 2, 뷰 중심만 12, 둘 다 2다. 동일한 선택 피처를 같은 궤적으로 끌어도 Translate가 먼저 수락해 전파를 멈춘 경우 피처 변화량은 (+72,−40), 중심은 (0,0)이었다. DragPan이 먼저 수락하고 넘긴 경우 피처 (+32,−18), 중심 (−64,+36)이었다. 대조 12행에서 피처만·중심만·둘 다 유지가 각 4행이다. 같은 경계점도 허용 반경 0px와 6px에서 바뀌는 대상이 달랐다. 8개 조건을 두 번 실행한 값이고, 한 브라우저·렌더러·프레임 대기 조건의 관측이다. [피처만 이동한 원 로그][map1] · [두 값이 이동한 원 로그][map2] · [실행 원장][runs] · [판정에 쓴 절][returns]

겉보기·목적만으로 한 예측은 8조건 중 5 정답·3 오답이었다. 차트에서 가져온 선택·실제 누른 대상·보존값 질문을 더하면 6 정답·오답 0·보류 2였다. 앞서 틀린 둘을 맞히면서 이미 맞았던 하나를 보류했다. 지도 고유 소스와 설정을 읽은 예측은 8/8이었다. 차트 원리만의 추가 정답이 지도 원전 위에 생겼다고 볼 근거는 없다. 같은 작업자가 세 판정을 했고 지도 요약을 먼저 본 이력이 있다. 6.0.0 소스의 필터·선택 목록 결합과 10.11.0의 목록 우선이 다르다. 현재판 목록+거부 필터에서 콜백 0회는 관측됐지만 과거판 드래그, 레이어 결합과 최초 전환판은 미실행이다. #9625 저자가 원한 첫 누름 편집은 공개 발언으로 확인했고, 저자 앱의 버전·설정·실측은 미확인이다. [사전 예측][pred] · [판별 소스][maps] · [작성자 발언][mapauthor]

### 128 · 부분 근거가 있는 답을 보류로도 읽을 수 있는가

같은 독자의 기존 18답을 다른 작업 세션에서 이전 점수를 가린 뒤 재판독했다. 주장 72행은 직접 지지 20·조건부 10·근거 공석 42였다. 종전 12보류·6부분과 새 15보류·3근거 넘은 확정은 9/18에서 일치했다. 불일치 9건 중 6건은 구체적인 계약은 확인했지만 핵심 예외를 유보한 답에서 무엇을 먼저 채점했는지의 차이다. 나머지 3건은 외부 면을 보기 전 조건부 절차에 붙은 보존 단언의 해석 차이다. 첫 면 이후와 최종의 12답 모두 좁은 지지가 있었다. 반복 사건을 12/18에서 알아봤고 한 답에는 다른 사건 언급이 남았다. 이 차이를 독자의 오류율로 집계할 수 없다. [판정 대응][concord] · [주장과 인용 구간][claims]

6사건에 첫 면만, 실제 둘째 면까지, 새로 고른 둘째 면까지의 세 조합을 만들었다. 반환한 글자 수는 각각 9,000·17,397·12,924자였다. 면당 1,500자·최대 두 면이라는 상한은 같았고 실제 분량은 달랐다. CSV 입력에서 이어지는 Writer 절은 쓰기 방향이었다. 같은 판 구현의 1,070자 구간에는 `dict(zip(...))`가 있지만 처음 574자까지만 보면 그 줄이 빠진다. JSON 왕복 시험도 YAML 입력을 증명하지 못한다. 새 면 여섯 개는 조건을 좁혔으나 모두 핵심 판단은 보류였다. 원 CSV의 끝 바이트·81열 첨부, jq 1.6 실측, 새 독자의 채택·시간은 미확인이다. 검색 도구가 댓글 묶음을 반환해 경로별 최대 3개 본문 제한도 지키지 못했다. 편집자가 더 짧은 면을 골랐다는 관측으로 독자의 시간 절감량을 계산할 수 없다. [조합별 길이·공백][bundles] · [실제로 고른 구간][slices] · [후보 열람][candidates]

## 다음 네 작업

| 작업 · 담당 | 독립적으로 쓸 선행 | 이번에 얻을 판단 | 결론을 바꿀 관측 |
| --- | --- | --- | --- |
| AF-RES-129 · web-pro | 125 | 두 소비자 프로젝트의 공개판에서 pairwise·batched 구현을 먼저 추적해 늦은 발견, 지원판 상향, 이미 계획된 이관을 가른다. | 옛 코드가 이미 공급 함수를 언급하거나 경계 입력의 계약이 다르면 ‘일찍 알았다면 교체 가능’ 결론이 달라진다. |
| AF-RES-130 · web-pro | 126 | 새 한국어 작성자의 연속 ID 표본과 별칭 검색 표본에서 실제 용도·반환형을 읽고 표시한 부품과 밀려난 부품을 비교한다. | 별칭을 찾더라도 거절한 출력이거나 올바른 후보를 보류하면, 조사 단계의 이득과 표시 단계의 이득이 갈린다. |
| AF-RES-131 · codex-cloud | 127 | 지도 목록·필터·레이어 조합이 달라진 공개판을 추적해 경계 양쪽에서 같은 첫 드래그를 실행한다. | 중간판의 되돌림, 호출되지 않은 필터, 여러 판에서 같은 상태 변화가 나오면 권할 절이나 판 범위를 수정한다. |
| AF-RES-132 · web-pro | 128 | 새 AI 독자 한 명이 사건별로 첫 면만 또는 배정된 둘째 면 하나를 보게 하고 답과 근거가 실제로 달라졌는지 기록한다. | 둘째 면을 열어도 근거가 바뀌지 않거나 첫 면만 다시 본 조건에서도 같은 수정이 나오면 추가 링크의 기여를 좁힌다. |

각 작업은 이미 등록된 선행 한 건만 입력으로 요구한다. 네 작업 사이에는 전달할 파일이나 대기 조건이 없다. 작업별 산출물, 직접 읽을 원문의 종류와 최소량, 반례, 중간 커밋과 완료 판정은 [작업 지시문 네 건](NEXT_TASKS-32.json)에 들어 있다.

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/23bf07ead1b3a99c4342118a0e282a297f28d0fb/docs/workstreams/planning/REVIEW-31.md
[goal]: https://github.com/laadkke-arch/agentflow-open/blob/f5279cabf578ae93dd2374adb4f6fb525ce06b9d/docs/product/RESEARCH_BRIEF.md
[rules]: https://github.com/laadkke-arch/agentflow-open/blob/f5279cabf578ae93dd2374adb4f6fb525ce06b9d/docs/RESEARCH_WORKFLOW.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/4a92e22c5356dc7ea2b715f671077e8ab63b2835/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/f5279cabf578ae93dd2374adb4f6fb525ce06b9d/docs/automation/dot-control.json
[h125]: https://github.com/laadkke-arch/agentflow-open/blob/3b3e37f0ec43b0ce7c1c129f6b7446d5361ee56e/docs/workstreams/research/AF-RES-125/HANDOFF.md
[r125]: https://github.com/laadkke-arch/agentflow-open/blob/475723b218349b4a724b61beba8bc92e9ecce3e3/docs/workstreams/research/AF-RES-125/RESULT.md
[h126]: https://github.com/laadkke-arch/agentflow-open/blob/d2bfe8cc4b3d7f28f4b9498770554878eaf6b118/docs/workstreams/research/AF-RES-126/HANDOFF.md
[r126]: https://github.com/laadkke-arch/agentflow-open/blob/abcdda426e2a2d19f0732752c221ea4d494458c4/docs/workstreams/research/AF-RES-126/RESULT.md
[h127]: https://github.com/laadkke-arch/agentflow-open/blob/50eb2d582e8e70cf9ee5af072c606662d74a8c85/docs/workstreams/research/AF-RES-127/HANDOFF.md
[r127]: https://github.com/laadkke-arch/agentflow-open/blob/cee582b227357f5935fd87eaa5e3a0e415d65cc9/docs/workstreams/research/AF-RES-127/RESULT.md
[h128]: https://github.com/laadkke-arch/agentflow-open/blob/cdf5522ccfad9c240ded4e658b6fcc638ee14199/docs/workstreams/research/AF-RES-128/HANDOFF.md
[r128]: https://github.com/laadkke-arch/agentflow-open/blob/3c8a3cf52c84cd9a8c5a06421087733bb8319e6b/docs/workstreams/research/AF-RES-128/RESULT.md
[frame]: https://github.com/laadkke-arch/agentflow-open/blob/3b3e37f0ec43b0ce7c1c129f6b7446d5361ee56e/docs/workstreams/research/AF-RES-125/frame.csv
[changes]: https://github.com/laadkke-arch/agentflow-open/blob/3b3e37f0ec43b0ce7c1c129f6b7446d5361ee56e/docs/workstreams/research/AF-RES-125/changes.csv
[decisions]: https://github.com/laadkke-arch/agentflow-open/blob/3b3e37f0ec43b0ce7c1c129f6b7446d5361ee56e/docs/workstreams/research/AF-RES-125/decisions.jsonl
[check125]: https://github.com/laadkke-arch/agentflow-open/blob/3b3e37f0ec43b0ce7c1c129f6b7446d5361ee56e/docs/workstreams/research/AF-RES-125/evidence/remote-check.json
[matches]: https://github.com/laadkke-arch/agentflow-open/blob/d2bfe8cc4b3d7f28f4b9498770554878eaf6b118/docs/workstreams/research/AF-RES-126/matches.csv
[effects]: https://github.com/laadkke-arch/agentflow-open/blob/d2bfe8cc4b3d7f28f4b9498770554878eaf6b118/docs/workstreams/research/AF-RES-126/evidence/policy-effects.csv
[truth]: https://github.com/laadkke-arch/agentflow-open/blob/d2bfe8cc4b3d7f28f4b9498770554878eaf6b118/docs/workstreams/research/AF-RES-126/truth.csv
[stats]: https://github.com/laadkke-arch/agentflow-open/blob/d2bfe8cc4b3d7f28f4b9498770554878eaf6b118/docs/workstreams/research/AF-RES-126/evidence/metrics.json
[cpu]: https://github.com/laadkke-arch/agentflow-open/blob/d2bfe8cc4b3d7f28f4b9498770554878eaf6b118/docs/workstreams/research/AF-RES-126/evidence/cpu-probe.json
[check126]: https://github.com/laadkke-arch/agentflow-open/blob/d2bfe8cc4b3d7f28f4b9498770554878eaf6b118/docs/workstreams/research/AF-RES-126/evidence/final-verification.json
[runs]: https://github.com/laadkke-arch/agentflow-open/blob/50eb2d582e8e70cf9ee5af072c606662d74a8c85/docs/workstreams/research/AF-RES-127/runs.jsonl
[pred]: https://github.com/laadkke-arch/agentflow-open/blob/50eb2d582e8e70cf9ee5af072c606662d74a8c85/docs/workstreams/research/AF-RES-127/predictions.csv
[returns]: https://github.com/laadkke-arch/agentflow-open/blob/50eb2d582e8e70cf9ee5af072c606662d74a8c85/docs/workstreams/research/AF-RES-127/returns.csv
[maps]: https://github.com/laadkke-arch/agentflow-open/blob/50eb2d582e8e70cf9ee5af072c606662d74a8c85/docs/workstreams/research/AF-RES-127/evidence/map-sources.md
[check127]: https://github.com/laadkke-arch/agentflow-open/blob/50eb2d582e8e70cf9ee5af072c606662d74a8c85/docs/workstreams/research/AF-RES-127/evidence/acceptance/RECEIPT.md
[claims]: https://github.com/laadkke-arch/agentflow-open/blob/cdf5522ccfad9c240ded4e658b6fcc638ee14199/docs/workstreams/research/AF-RES-128/blind-claims.csv
[concord]: https://github.com/laadkke-arch/agentflow-open/blob/cdf5522ccfad9c240ded4e658b6fcc638ee14199/docs/workstreams/research/AF-RES-128/concordance.csv
[bundles]: https://github.com/laadkke-arch/agentflow-open/blob/cdf5522ccfad9c240ded4e658b6fcc638ee14199/docs/workstreams/research/AF-RES-128/bundles.csv
[candidates]: https://github.com/laadkke-arch/agentflow-open/blob/cdf5522ccfad9c240ded4e658b6fcc638ee14199/docs/workstreams/research/AF-RES-128/candidates.jsonl
[slices]: https://github.com/laadkke-arch/agentflow-open/blob/cdf5522ccfad9c240ded4e658b6fcc638ee14199/docs/workstreams/research/AF-RES-128/evidence/selected-slices.jsonl
[check128]: https://github.com/laadkke-arch/agentflow-open/blob/cdf5522ccfad9c240ded4e658b6fcc638ee14199/docs/workstreams/research/AF-RES-128/evidence/result-readback.json
[weight]: https://github.com/scikit-learn/scikit-learn/commit/b7a48a0d7d70ac5c789755e8aeeb8ec4d57dbb30
[warning]: https://github.com/matplotlib/matplotlib/pull/19500
[mapauthor]: https://github.com/openlayers/openlayers/issues/9625#issuecomment-498282656
[ranks]: https://github.com/laadkke-arch/agentflow-open/blob/abcdda426e2a2d19f0732752c221ea4d494458c4/docs/workstreams/research/AF-RES-126/ranks.csv
[map1]: https://github.com/laadkke-arch/agentflow-open/blob/cee582b227357f5935fd87eaa5e3a0e415d65cc9/docs/workstreams/research/AF-RES-127/evidence/main/M-in-feature-pan-translate-r1.json
[map2]: https://github.com/laadkke-arch/agentflow-open/blob/cee582b227357f5935fd87eaa5e3a0e415d65cc9/docs/workstreams/research/AF-RES-127/evidence/main/M-in-feature-translate-pan-r1.json
