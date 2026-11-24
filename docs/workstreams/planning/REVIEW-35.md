# REVIEW-35 · 링크가 실제로 바꾼 것과 아직 물어야 할 것

사용자는 설계 중인 소프트웨어의 전부 또는 일부와 목적을 주고, 가져다 쓸 기능·부품·다른 분야의 원리를 원문 링크로 찾고 싶어 한다. 이번 네 작업에서 가장 분명한 사례는 xarray 작성자가 링크에 있는 네 타입 중 세 개를 빌려 자기 코드의 주석을 고친 일이다. 반면 한국어 요청에서 ‘가중치를’로 찾아낸 기능은 저장된 모델을 쓰려는 사람에게 표본 인덱스를 돌려주는 기능이었다. **무슨 자료를 발견했는지, 그중 어느 부분이 들어맞았는지, 사용자가 실제 무엇을 바꿨는지를 각각 기록해야 한다.** 기능 링크로 원저자가 재작업이나 사람 시간을 줄였는지는 여전히 미확인이다. [제품 목표][goal] · [타입 제안과 응답][typeans] · [한국어 첫 요청][weight]

## 검토한 범위

2026-11-24 UTC. 계획 브랜치 `9cfc033`의 최신 REVIEW-34를 먼저 읽었다. 그 검토가 사용한 통합판 `1d65b0b`와 이번 통합판 `d950356`의 진행표를 작업 ID로 맞춰 모든 필드를 비교했다. 기존 134행은 같고 137~140 네 행이 추가돼 모두 DONE이다. 전체 138행은 **DONE 136, BLOCKED 2**다. 연구만 세면 136건 중 DONE 134, BLOCKED 2(018·035)이고, 별도 연결 시험 두 건이 DONE이다. 중앙 DONE 136행의 `acceptance_evidence`는 모두 비어 있다. 네 작업자가 인계서에 기록한 상태는 모두 **PARTIAL**이다. [직전 검토][prev] · [직전 진행표][old] · [이번 진행표][reg]

| 새 DONE | 작업 브랜치에서 확인한 인계판 | 별도로 검사한 결과 본문판 | 원장에서 다시 센 단위 |
| --- | --- | --- | --- |
| 137 · 리뷰 링크의 귀속 | [48475ac · 인계][h137] | [ae8b00d · 결과][r137] | 고정 PR 8, 사건 61, 공개 목록 범위 64행, 출처 85행 중 산입 고유 저작 37 |
| 138 · 한국어 조사와 표시 | [198e743 · 인계][h138] | [5313f08 · 결과][r138] | 저자 5, 질문×카드 80쌍, 정책별 320행·이동 480행, 출처 129행 중 고유 저작 37 |
| 139 · 판별 재검사 비용 | [c06598b · 인계][h139] | [1aabc75 · 결과][r139] | 배포 30판, 발표순 인접 29쌍, 비용 요약 42행, 출처 164행 중 고유 저작 34 |
| 140 · 기술 자료와 원저자 질문 | [e9ee53c · 인계][h140] | [a43dad1 · 결과][r140] | 모집 60행, 채택 8사건, 후속 댓글 24행, 출처 63행 중 고유 저작 27 |

네 브랜치의 조회 head는 각각 중앙의 `result_commit`과 같았다. 네 RESULT.md의 내용과 Git blob도 위의 별도 결과 본문판과 일치했다. 이번 검토에서는 해당 인계·결과와 근거 원장을 열어 집계했다. 실행값은 작업자가 저장한 영수증 범위에서 인용한다. 137~139에는 해당 결과판 checkout 검사가 있고, 140은 원격 파일·커밋 검산만 있어 CLI 종료값이 없다. 이전 작업의 결론과 정정은 REVIEW-34에서 이어받았다. [137 검사][chk137] · [138 검사][chk138] · [139 검사][chk139] · [140 검산][chk140]

## 처음부터 지금까지의 설계 판단

| 제품 질문 | 이어진 관측 | 설계에 쓸 수 있는 범위와 열린 선택 |
| --- | --- | --- |
| 다른 분야 선례가 선택을 바꾸는가 | 010은 분야 단서를 받고 원리 7군을 찾았다. 단서를 뺀 033의 144쌍에서는 넓은 지지 1건, 당시판 지지 0건이었다. 022의 미인지→변경→시행은 0/24였다. 109의 시험 제안 27건과 117·121·125·129도 원저자의 늦은 발견과 노동을 잇지 못했다. 129의 NetworkX #8201에서는 비순환 경로만 바뀌고 나중에 배웠다고 밝힌 사람은 리뷰어였다. 133·137에서 이름 제안과 링크의 부분 차용을 구별할 증거가 늘었다. | 참고할 원리, 실제 바뀐 조작, 제공자와 수신자, 기존 사용 흔적을 각각 알려줄 수 있다. 분야를 넘는 발견률이나 절약한 시간은 미확인이다. |
| 부분 요청의 문맥은 얼마나 필요한가 | 020은 주장 72/73을 전달했지만 충돌을 모두 푼 것은 2/16이었다. 074에서 구성한 입력은 추가값으로 8/8 갈렸고, 111에서는 동의어 변경 뒤 두 방식 모두 0/6 정합이었다. 119의 자연 도표 6건은 원요구만으로 정확 0, 인접 기록과 직접 참조로 각각 3이었다. 123에서는 같은 x에서 1px 끌어도 시작 대상에 따라 선택한 달이 달랐다. 140에서는 작성자의 출력 문자 의무와 판에 따른 소프트웨어 동작이 갈렸다. | 객체·반환값·보존할 것을 먼저 적었을 때, 기술 자료로 답할 조건과 원저자가 결정할 조건을 따로 남긴다. 질문 한 번의 실측 편익은 없다. |
| 어떤 기능 링크를 보여 줄 것인가 | 076의 자연 6요구×20후보에는 직접 적격 0, 자료 범위를 넓힌 080은 자연 1/5·교정 3/5였다. 118에서 표시 직접·일부·충돌이 9·7·15→8·0·0이 됐다. 122의 자연 10요구에는 16카드로 완전한 답이 없었다. 126의 공개 10건에서 별칭 적중 0, 구성한 표현에서는 직접 3과 충돌 1이 함께 유입됐다. 130은 포럼 적격 원문 확보가 부족했고 134의 새 GitHub 6건에는 활성 별칭이 없었다. 138의 실제 적중 1개는 이미 시도한 조작이었다. | 검색에서 조사할 후보, 실제 표시, 목록 자체에 적격 기능이 있는지를 분리한다. 134의 엄격 표시에서는 직접 후보도 빠졌고, 138에는 처음부터 직접 후보가 없었다. |
| 옛 추천을 어떻게 복원하고 언제 재확인할까 | 055는 옛 판단 4/4와 다음 판 판단 0/4, 071은 절·설정으로 옛 사례 22/22를 복원했다. 075는 전체 후보가 없어 단독·공동 1위를 각각 16/16 보류했다. 106은 살아 있는 주소에서 옛 예제의 쓰임 소실, 121은 실제 읽은 판 6/6 미확인, 131은 지도 옵션의 판 경계를 기록했다. 135에서 d3-scale의 문서 절 신호는 출력 전환 둘 중 하나를 놓쳤고 넓은 구현 신호는 26쌍 중 불필요 경보 23이었다. 139에서는 같은 발표 경계도 스칼라와 벡터 질의의 정답이 달랐다. | 이전 답의 근거, 지금 판·입력에서의 실행, 모든 후보에 대한 우선순위에는 서로 다른 자료가 필요하다. 요청할 때 열기와 매번 검사하기의 비용은 질의 분포에 달려 있다. |
| 원문을 하나 더 주면 답이 나아지는가 | 021의 두 절 예산에서 근거 충분은 주소만 6/23, 절 목록 9/23, 맞춘 절 14/23, 잘못 붙인 절 8/23이었다. 034의 부분 시간은 380→57초, 전체는 849→847초였다. 116·120은 후속 정의로 가는 경로를 보였고 124의 추가 시험 후 핵심 처방 수정은 0/6이었다. 128은 주분류 일치 9/18, 132는 한 독자의 조건부 후보 추가 1건이었다. 136 재판독에서는 도구 제약과 후반 선노출이 드러났다. 140은 새 사례에서 둘째 절과 원저자의 실제 발언을 분리했다. | 더 구체적인 근거, 새 조건부 대안, 문제 해결, 당사자 수락은 따로 센다. 첫 답이 충분한 때, 원문이 필요한 때, 한 질문이 남는 때를 비교할 수 있으나 평균 효과는 미측정이다. |
| 개별 기능을 결합·편집해도 같은 것이 보존되는가 | 078은 단독 기능의 결합 실패, 103은 외관 10/10 보존과 8자리 텍스트 선택 소실, 107은 단일 발생 편집에서 공유 정의 0/6·위치 지정 6/6을 보였다. 119·123은 차트의 로컬·공유 상태를 나눴다. 127은 처리 순서가 바뀌자 피처와 지도 중심이 함께 움직였고, 131은 같은 순서에서 6.6.1→6.7.0 사이 이동 대상이 바뀜을 확인했다. 135의 지도 실측은 같은 네 판이었다. 137의 희소 행렬도 값이 같아 보이는 두 반환형에서 후속 곱의 의미가 갈렸다. | 보존할 위치·객체·반환형·후속 연산까지 링크 설명의 후보로 둔다. 다른 렌더러와 원저자 앱에 대한 적합성은 해당 입력으로 확인해야 한다. |

직전 34차에서 세운 경계도 중요하다. 133의 #7579는 같은 작성자가 의존성 **이름** 제안을 받아들인 사건이었다. 134의 6질문×16카드는 직접 1·일부 1·충돌 3·미확인 91이었고 표시 18자리가 모두 비었다. 유일한 직접 후보 D01도 작성자가 단일 프로세스를 허용하는지에 따라 등급이 달랐다. 135의 d3-scale 3.2.3→3.2.4에서는 README 바이트가 같은데 기본 `null` 출력이 0→`undefined`로 바뀌었다. 136의 6사건×3답은 핵심 해결 6건 모두 유보였고, J2에 추가된 fq는 저자가 나중에 밝힌 도구 제약과 부딪혔다. 판독자가 알아본 12/18답을 빼면 단계쌍을 비교할 수 없었다. [34차 검토와 원장 위치][prev]

기존 정정도 유지한다. 114의 ‘충돌’ 138/144는 118의 명시 반박 기준에서 충돌 7·미확인 131이고, 나머지 6은 일부다. 119의 M3994 원형 MG 좌표 y는 11.71875, 공유 변경 뒤는 275다. 136의 ‘고유 8면’은 본문 해시 기준 9면이다. 10회 열람과 답·면 연결 16쌍은 단위가 다르다. 제품의 최소 저장 필드·AI 전처리·상시 수집·AgentFlow 연동 계약은 계속 비교할 설계 선택이다. [이전 근거와 정정][prev] · [연구 결과의 용도][wf]

## 새 증거에서 확인된 것과 끊긴 곳

### 137 · 부분 차용의 귀속은 타입 주석까지 확인됐다

133은 xarray #9618의 앞쪽 비어 있지 않은 댓글 18개를 읽었다. 137은 이 PR 본문 있는 대화 항목 276개를 포함해 8개 PR에서 440개를 판독했다. 두 크기로 회수한 40개 REST 목록의 ID와 빈 다음 페이지가 일치했다. 인라인 311개에 원래 Git blob이 있었고 그중 36개는 최종 head 조상 밖이었다. 삭제되거나 공개되지 않은 대화, 원시 HTTP Link·중첩 GraphQL 마지막 커서는 미확인이다. 고정 8건의 61개 조작은 채택률을 추정할 무작위 표본이 아니다. [회수 원장][coverage] · [사건 원장][events] · [집계][agg137]

#9618에서는 내부 정의 링크 → 같은 작성자의 부분 차용 응답 → 첫 수정 `eaf3c731` → 2025.1.2 배포까지 연결됐다. 네 후보 타입 가운데 세 개를 썼고 날짜 비교식은 그대로였다. #9589는 133에서 비었던 첫 파서 수정 `a9a940e8`이 복원됐으나 전달 매체는 함수 이름이었다. #7576은 원 PR 작성자와 보호 패치 작성자가 달랐고, #7579의 약 9→6분은 제안 전에 보고된 빌드 시간이다. 확인한 사건에서 기존 공개 실행 기능 링크·동일 작성자의 최초 인지·같은 런타임 수정이 함께 입증된 것은 0건이고 실제 사람 노동 시간은 61건 모두 미확인이다. 실행 기록에서는 SciPy 1.11.2에서 기본 matrix와 opt-in array의 같은 마스크에 `*`를 적용한 합이 10과 6, `@`의 최대차가 0이었다. 추천 설명에 보존할 연산을 붙일 실제 근거다. [링크 제안][typeprop] · [작성자 답][typeans] · [첫 수정][typechange] · [파서 답][parser] · [반환 계약 실행][comp]

통계 정정에서도 같은 구분이 필요했다. ONS G7G6의 같은 2022년 2분기 값은 v28과 후판에서 480→479(천 명)였지만 즉시 대체판 셀과 제보자는 미확인이다. RFC 정오표에는 제보·검토·승인과 반영된 인라인 값까지 남은 사례, 제보자 이름이 있어도 반려된 사례가 함께 있었다. 사건 기록과 그 조작이 반영된 판을 각각 확인할 필요가 있다. [정정 원장][cross137]

### 138 · 조사 결합형을 찾았지만 가리킨 대상이 달랐다

6개 질의의 예정 120칸에서 반환 창 43슬롯, 중복 제거 후 첫 본문 41개를 열었다. 목적층 1명과 중립층 4명이 적격으로, 계획한 목적층 4명·전체 8명에 못 미쳤다. 5질문×16카드의 전수 기준은 직접 0·일부 3·충돌 3·미확인 74였다. 유일한 활성 별칭 ‘가중치를’는 이미 저장한 모델 파라미터였다. 끝조사 하나를 허용하자 표본 인덱스를 내는 D08이 조사 4위로 들어오고 D02가 8위 밖으로 밀렸지만 표시 상위 3장은 그대로였다. ‘리뷰’ 안의 ‘뷰’ 두 곳은 점수에 들어가지 않았다. [모집표][frame138] · [전수 판정][truth] · [별칭 위치][alias] · [정책 순위][rank]

원문에서 요구 출력과 맞는지 확인하는 표시 규칙(Gate)은 화면의 일부 2·미확인 9를 보류해 공석을 4/15→15/15로 늘렸다. 원래 표시된 충돌도 직접도 0이어서, 이 표본으로 직접 회복률이나 표시 충돌 제거의 이득을 추정할 수 없다. 추가 원절 33개를 읽었고, 같은 절에서 한 조건만 빠졌는지 23쌍을 더 판독해도 조건부 표시는 0이었다. P1-07의 후속 답은 모델을 직접 호출하는 경로여서 기존 로더를 쓰는 단계가 정말 필요한지조차 달라진다. 동일 작업자가 표시·정답표를 만들었고 실제 클릭과 PyTorch 회귀 실행은 미측정이다. MBTA에서는 같은 Park Street와 방향으로도 종점이 갈렸고, 서지에서는 한 편곡 목록과 악보 원책임표시까지 확인한 범위가 달랐다. [편집 비용][cost138] · [후속 답][forward] · [타 분야 원장][other138]

### 139 · 같은 배포 경계에서 입력 형태가 경보의 정답을 바꿨다

simple-statistics 30판의 공개 진입에서 **판당 합계 126셀**(quantile 108, median 18)을 두 설치 경로에서 각각 3,780셀씩 대조했다. 발표순 29쌍 모두 스칼라 p의 출력·예외·배열 보존이 같았고 미확인 0이었다. semver 순서도 같아서 두 표의 58행은 독립 전환 58개를 뜻하지 않는다. 양성 전환이 없어 검출률은 산출할 수 없다. 사후에 더한 벡터 p에서는 6.1.0→6.1.1에 `[NaN,461.5,484.5]`가 `[461,468.5,484.5]`로 바뀌었다. 문서 절 C는 이 경계를 생략한다. 함수·직접 위임·공지 신호 E는 인접 두 쌍에서 번들·소스 대응이 불분명해 강제 확인했다. 이를 새 변화에 대한 예측 성공으로 세지 않는다. [출력쌍][pairs] · [사후 벡터][vectors] · [판별 신호][signals] · [해당 수정][p334]

매 발표판을 찾는 30회 모형에서는 매번 실행 30회, 넓은 번들 신호 D 24회, E 3회(최초 1+강제 2)였다. 두 끝판만 교대로 여섯 번 묻는 모형에서는 요청판 직접 실행과 E가 모두 두 번 실행했고, 타르 취득은 각각 541,318바이트와 7,743,450바이트였다. 일부 계측을 합산한 시나리오 비용이며 실제 운영 트래픽이나 사람 대기시간은 미확인이다. 관측된 판에는 직접 런타임 의존 변경 기회도 없었다. SWR 같은 열차의 계획표는 Sway 06:15가 유지되고 New Milton 06:20→06:21이었으나 실운행은 미확인이다. ONS 임금 £34,963→£35,004는 공표 표시까지이며 원표 두 ZIP의 동일 셀은 미확인이다. [질의별 비용][cost139] · [두 분야의 셀][cross139]

### 140 · 추가 기술 자료와 작성자의 조건이 서로 다른 답을 줬다

csvkit·yq에서 번호·생성시각 60개를 고정하고 현재 본문 20개를 열어 8명(각 4)의 사건을 골랐다. 최초 게시판이 복원된 것은 0/8이다. 첫 절은 8개 모두 1,200 코드포인트였고 판독은 즉답 1·조건부 5·보류 2였다. 둘째 절은 7개에서 열렸다. 고정 경로 404인 Y1은 분모에 남겼다. 열렸던 7개 중 유지·보강 5, 버전 후보 좁힘 1(C4), 조건부 후보 추가 1(Y3), 새 핵심 해결 0이었다. C1·C2·Y2에서는 지정한 단어가 목록이나 다른 시험 또는 구현 앞부분을 가리켰다. 알맞은 절을 받았을 때의 효과와, 이번 방식으로 고른 절의 결과는 구분해야 한다. [모집][frame140] · [요구][req] · [첫 절][first] · [사전 분기와 둘째 절][branches]

후속 댓글 24개 중 원저자 댓글 8개는 4사건에 집중됐다. C3에서는 저자가 escape 문자 자체를 거절했다. C4에서는 날짜를 먼저 변환하는 파이프를 보고했다. Y2에서 저자가 성공했다고 한 것은 수정 빌드였고, Y3에서는 CRLF와 LF 결과 차이를 보고했으나 정규화 허용 여부는 밝히지 않았다. 가상 질문 8개 중 발송은 0회였다. 한 판독자의 분류, 작업 당시 판본 일부 불일치, 댓글별 생성·수정 시각 24/24 결측, 정확판 CLI 미실행 때문에 질문 응답률·채택·실제 해결 효과는 미확인이다. 신문 원면과 OCR은 기관 가이드 병치 이미지로만 비교했고, 악보 다섯 면은 동일 편곡 한 저작이다. [후속 발언 원장][follow] · [escape 거절][c3] · [수정 빌드 보고][y2] · [개행 비교][y3] · [신문·악보][other140]

## 우선 풀 불일치 세 건

| 표면상 어긋나는 결론 | 무엇이 달라 판정이 갈렸는가 | 다음에 답을 바꿀 관측 |
| --- | --- | --- |
| 링크를 빌린 사실은 있는데 새 기능을 발견해 실행을 바꿨다는 사례는 없다 | 137의 수신자는 타입 집합 일부를 차용했다. 이름 제안으로 바뀐 파서, 다른 유지보수자의 런타임 코드, 작성자의 최초 인지에는 각각 별도 기록이 있다. | 141에서 새로운 소비자 둘의 사전 코드·제안·답·첫 diff·배포를 같은 조작에 묶고, 차용된 부분과 배제된 조건을 함께 찾는다. |
| 표시를 엄격하게 하면 공석이 늘고, 원문을 더 줘도 답이 남는다 | 134는 직접 후보까지 숨겼지만 138의 16카드에는 직접 후보가 하나도 없었다. 140 C3의 출력 의무는 작성자에게 있고 Y2의 결함은 기술 쪽에 있었다. 공석의 원인에 따라 자료 추가와 질문의 가치가 달라진다. | 142는 후보 목록 안팎과 요청 구절의 역할을 고정 질문에서 비교한다. 144는 당사자 버전에서 선택지의 실제 출력을 대조한다. |
| 좁은 신호는 실행을 크게 줄이지만 직접 검사보다 더 읽을 수 있다 | 135에는 사전 입력의 변화가 있었고 139의 스칼라 표본에는 변화가 없었다. 139의 벡터 결과는 사후 확인이고, 두 끝판 질의에서는 실행 수가 같아도 취득량이 달랐다. | 143에서 알려진 전환을 교정용으로 남기고, 미열람 판·입력의 경보를 사전에 고정해 실제 요청별 오류와 차가운·재사용 캐시의 비용을 함께 잰다. |

## 다음 배정

| 독립 작업 | 확정 입력 | 담당 | 설계자가 받을 판단 |
| --- | --- | --- | --- |
| AF-RES-141 · 링크에서 빌린 부분의 귀속 | 137의 공개 리뷰·사건 원장 | web-pro | 원출전 전체를 권할지, 빌린 조작과 빠진 조건만 연결할지, 동기를 유보할지 결정할 근거 |
| AF-RES-142 · 한국어 요청에서 후보 자료의 공백 | 138의 16카드·다섯 원요청 | web-pro | 자료집 확장과 저자 목표 구절을 읽는 방법이 각각 되찾거나 밀어내는 직접·일부 링크와 표시 공석 |
| AF-RES-143 · 입력 형태와 재검사 비용 | 139의 스칼라 결과·사후 벡터·비용 원장 | codex-cloud | 미열람 경계에서 잘못 이월한 값과, 정확판을 직접 열 때와 비교한 실제 전송·대기 비용 |
| AF-RES-144 · 작성자 사례의 정확판 실행 | 140의 사전 분기·원저자 후속 발언 | codex-cloud | CSV·YAML의 값·표현을 보존하는지 실행으로 밝힐 조건, 여전히 원저자만 정할 조건 |

네 작업은 각각 이미 저장된 한 선행 작업에서 시작한다. 결과를 서로 기다릴 필요가 없다. 질문·원전 하한·필수 표·반증과 인계 조건은 각 작업자가 받아 볼 지시문 안에 전부 넣었다. [35차 작업 지시문](NEXT_TASKS-35.json)

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/9cfc0339f9ddc840eec6cbec7333f5e4535366f5/docs/workstreams/planning/REVIEW-34.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/1d65b0b7aaef85350df8842dfc05a6be69148b38/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/d950356cdfae3edf799870cdeb90b93b5bd4ffd3/docs/automation/dot-control.json
[goal]: https://github.com/laadkke-arch/agentflow-open/blob/d950356cdfae3edf799870cdeb90b93b5bd4ffd3/docs/product/RESEARCH_BRIEF.md
[wf]: https://github.com/laadkke-arch/agentflow-open/blob/d950356cdfae3edf799870cdeb90b93b5bd4ffd3/docs/RESEARCH_WORKFLOW.md
[h137]: https://github.com/laadkke-arch/agentflow-open/blob/48475acf84dd9e9e49c6fc24958ad50b7aee1440/docs/workstreams/research/AF-RES-137/HANDOFF.md
[r137]: https://github.com/laadkke-arch/agentflow-open/blob/ae8b00dad97ba242d7f274a539964cc66c1f1070/docs/workstreams/research/AF-RES-137/RESULT.md
[h138]: https://github.com/laadkke-arch/agentflow-open/blob/198e74358fe2d124c31e16f8bbb93dbbf7ee561d/docs/workstreams/research/AF-RES-138/HANDOFF.md
[r138]: https://github.com/laadkke-arch/agentflow-open/blob/5313f08e5aa2b45ff3477a963697d1f059059f05/docs/workstreams/research/AF-RES-138/RESULT.md
[h139]: https://github.com/laadkke-arch/agentflow-open/blob/c06598bada3039eae441a9ba49fd28837108873a/docs/workstreams/research/AF-RES-139/HANDOFF.md
[r139]: https://github.com/laadkke-arch/agentflow-open/blob/1aabc75823d6f919ac74ca9e06cfc8d1b614f2ec/docs/workstreams/research/AF-RES-139/RESULT.md
[h140]: https://github.com/laadkke-arch/agentflow-open/blob/e9ee53c53188449c289d4a7ea563e836eded1468/docs/workstreams/research/AF-RES-140/HANDOFF.md
[r140]: https://github.com/laadkke-arch/agentflow-open/blob/a43dad1ece967452a996985541773396ea4363a5/docs/workstreams/research/AF-RES-140/RESULT.md
[events]: https://github.com/laadkke-arch/agentflow-open/blob/48475acf84dd9e9e49c6fc24958ad50b7aee1440/docs/workstreams/research/AF-RES-137/events.jsonl
[coverage]: https://github.com/laadkke-arch/agentflow-open/blob/48475acf84dd9e9e49c6fc24958ad50b7aee1440/docs/workstreams/research/AF-RES-137/coverage.csv
[comp]: https://github.com/laadkke-arch/agentflow-open/blob/48475acf84dd9e9e49c6fc24958ad50b7aee1440/docs/workstreams/research/AF-RES-137/compatibility.csv
[agg137]: https://github.com/laadkke-arch/agentflow-open/blob/48475acf84dd9e9e49c6fc24958ad50b7aee1440/docs/workstreams/research/AF-RES-137/evidence/reaggregation.json
[chk137]: https://github.com/laadkke-arch/agentflow-open/blob/48475acf84dd9e9e49c6fc24958ad50b7aee1440/docs/workstreams/research/AF-RES-137/evidence/workbench-check.json
[cross137]: https://github.com/laadkke-arch/agentflow-open/blob/48475acf84dd9e9e49c6fc24958ad50b7aee1440/docs/workstreams/research/AF-RES-137/corrections.csv
[frame138]: https://github.com/laadkke-arch/agentflow-open/blob/198e74358fe2d124c31e16f8bbb93dbbf7ee561d/docs/workstreams/research/AF-RES-138/frame.csv
[truth]: https://github.com/laadkke-arch/agentflow-open/blob/198e74358fe2d124c31e16f8bbb93dbbf7ee561d/docs/workstreams/research/AF-RES-138/truth.csv
[rank]: https://github.com/laadkke-arch/agentflow-open/blob/198e74358fe2d124c31e16f8bbb93dbbf7ee561d/docs/workstreams/research/AF-RES-138/ranks.csv
[alias]: https://github.com/laadkke-arch/agentflow-open/blob/198e74358fe2d124c31e16f8bbb93dbbf7ee561d/docs/workstreams/research/AF-RES-138/evidence/alias-audit.csv
[cost138]: https://github.com/laadkke-arch/agentflow-open/blob/198e74358fe2d124c31e16f8bbb93dbbf7ee561d/docs/workstreams/research/AF-RES-138/evidence/editor-cost.csv
[chk138]: https://github.com/laadkke-arch/agentflow-open/blob/198e74358fe2d124c31e16f8bbb93dbbf7ee561d/docs/workstreams/research/AF-RES-138/evidence/session-check.json
[other138]: https://github.com/laadkke-arch/agentflow-open/blob/198e74358fe2d124c31e16f8bbb93dbbf7ee561d/docs/workstreams/research/AF-RES-138/domains.csv
[pairs]: https://github.com/laadkke-arch/agentflow-open/blob/c06598bada3039eae441a9ba49fd28837108873a/docs/workstreams/research/AF-RES-139/evidence/output-pairs.csv
[vectors]: https://github.com/laadkke-arch/agentflow-open/blob/c06598bada3039eae441a9ba49fd28837108873a/docs/workstreams/research/AF-RES-139/evidence/posthoc-array-p.json
[signals]: https://github.com/laadkke-arch/agentflow-open/blob/c06598bada3039eae441a9ba49fd28837108873a/docs/workstreams/research/AF-RES-139/signals.csv
[cost139]: https://github.com/laadkke-arch/agentflow-open/blob/c06598bada3039eae441a9ba49fd28837108873a/docs/workstreams/research/AF-RES-139/evidence/cost-summary.csv
[cross139]: https://github.com/laadkke-arch/agentflow-open/blob/c06598bada3039eae441a9ba49fd28837108873a/docs/workstreams/research/AF-RES-139/domain-cells.csv
[chk139]: https://github.com/laadkke-arch/agentflow-open/blob/c06598bada3039eae441a9ba49fd28837108873a/docs/workstreams/research/AF-RES-139/evidence/acceptance.json
[frame140]: https://github.com/laadkke-arch/agentflow-open/blob/e9ee53c53188449c289d4a7ea563e836eded1468/docs/workstreams/research/AF-RES-140/frame.csv
[req]: https://github.com/laadkke-arch/agentflow-open/blob/e9ee53c53188449c289d4a7ea563e836eded1468/docs/workstreams/research/AF-RES-140/requirements.csv
[first]: https://github.com/laadkke-arch/agentflow-open/blob/e9ee53c53188449c289d4a7ea563e836eded1468/docs/workstreams/research/AF-RES-140/first-links.csv
[branches]: https://github.com/laadkke-arch/agentflow-open/blob/e9ee53c53188449c289d4a7ea563e836eded1468/docs/workstreams/research/AF-RES-140/branches.csv
[follow]: https://github.com/laadkke-arch/agentflow-open/blob/e9ee53c53188449c289d4a7ea563e836eded1468/docs/workstreams/research/AF-RES-140/followup.csv
[other140]: https://github.com/laadkke-arch/agentflow-open/blob/e9ee53c53188449c289d4a7ea563e836eded1468/docs/workstreams/research/AF-RES-140/domains.csv
[chk140]: https://github.com/laadkke-arch/agentflow-open/blob/e9ee53c53188449c289d4a7ea563e836eded1468/docs/workstreams/research/AF-RES-140/evidence/remote-recheck.json
[typeprop]: https://github.com/pydata/xarray/pull/9618#discussion_r1911138165
[typeans]: https://github.com/pydata/xarray/pull/9618#discussion_r1912819641
[typechange]: https://github.com/pydata/xarray/commit/eaf3c731cb8b69b329fe677241544a1337290014
[parser]: https://github.com/pydata/xarray/pull/9589#discussion_r1795004788
[weight]: https://github.com/Beomi/KcELECTRA/issues/5
[forward]: https://github.com/Beomi/KcELECTRA/issues/5#issuecomment-977563439
[p334]: https://github.com/simple-statistics/simple-statistics/pull/334
[c3]: https://github.com/wireservice/csvkit/issues/1194#issuecomment-1456759485
[y2]: https://github.com/mikefarah/yq/issues/1501#issuecomment-1378332372
[y3]: https://github.com/mikefarah/yq/issues/1506#issuecomment-1376667839
