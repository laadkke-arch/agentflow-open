# REVIEW-16 · 추천 근거가 설계자의 질문에 답하는 범위

원전 링크로 설명할 수 있는 원리, 그 판의 구현이 실제로 한 일, 링크를 본 사람이 내린 결정에는 각각 다른 증거가 필요하다. 이번에 가장 분명한 사례는 **같은 URL이 같은 문항의 정답 권고와 오답 권고 양쪽에 붙었다**는 점이다. 또 고정한 11개 요구–후보 쌍에서 첫 주소를 특정 절로 옮기면 읽는 분량은 줄었지만, 두 조건을 모두 확인한 쌍은 늘지 않았다. 제품의 반환 단위로는 ‘이 부분의 이 조건을 이 판의 이 절에서 확인했다’는 문장을 검토할 수 있다. 그것이 실제 설계자의 오판이나 재작업을 얼마나 줄이는지는 미확인이다. [자극의 링크 원장][stim62] · [도착 경로][rt64] · [조건별 판정][jud64]

## 검토 범위와 증거의 출처

2026-11-23 UTC. `work/planning@55d64c4`의 최신 REVIEW-15를 먼저 읽고, 그 기준인 통합판 `aa1dc65`와 현재 `chore/workspace-foundation@028d16f`의 작업 ID·상태·결과 SHA를 대조했다. 등록 **58→62**, DONE **56→60**, BLOCKED **2→2**다. 이미 등록된 작업의 상태나 결과 SHA 변경은 없었다. 이번에 원본 인계·결과를 연 작업은 새 DONE **AF-RES-061~064**다. 060까지의 결론은 직전 검토에서 인수했다. 018은 세 번째 시도에서 대화 길이 한도에 도달했고 035는 첫 시도에서 사이버 보안 위험 가능성이 표시됐다. 두 행 모두 중앙 결과 SHA가 비어 있다. [직전 검토][prev] · [직전 진행표][oldreg] · [이번 진행표][reg]

| 새 DONE | 인계 커밋 / 결과 본문 고정판 | 실제로 인계된 분모와 상태 |
| --- | --- | --- |
| 061 · 물리 원리와 구현 | [bf9f27e][h61] / [1ea7312][r61] | 부분 인계. 외부 원저작 31개, 4개 구현에 정상·경계 8행. 두 자료 보기를 실제로 비교할 수 있는 행은 6개. [수용 원장][a61] |
| 062 · 출처 제공과 판단 | [36e5040][h62] / [bb3c627][r62] | 부분 인계. 외부 원저작 47개. 주 표본 6자리 중 3자리 선정, 최초 순위 확정은 1자리. 양 군의 정오별 수락 원개수는 관측 표본 한 코호트에서 4셀 회수. [수용 원장][a62] |
| 063 · 과거 실행의 자료판 | [8e348bb][h63] / [86403f9][r63] | 인계문은 **BLOCKED / 부분 인계**로 표기. 외부 독립 계보 51개. 자연 보고 6건과 보강 4자리를 조사했고 보강에 배정할 원출력은 0건. [수용 원장][a63] |
| 064 · 후보의 첫 주소 | [c522e01][h64] / [6341dce][r64] | 부분 인계. 산입 자료 32개·31계보. 12요구, 36슬롯, 실제 후보 11쌍. 두 보기 22경로 가운데 실제 노출 한도를 지킨 경로는 20개. [갱신 수용 원장][a64] |

네 인계 SHA는 각각 작업 브랜치 끝과 일치했다. 마지막 커밋은 각자 HANDOFF.md 한 파일을 변경했고, 인계판의 RESULT.md는 표의 본문판과 같은 Git blob이었다. 중앙 DONE 60건의 `acceptance_evidence`는 모두 빈 배열이고 새 네 행의 `source_commit`과 `actual_model`은 null이다. 이번 검토에서는 저장소의 예측·관측 행, 연구 조건별 원개수, 보고·실행물 영수증, 슬롯·판정·실행 원장을 대조했다. 외부 원문 판독과 프로그램 실행은 해당 연구자의 기록에 근거한다. [예측][pr61] · [정오별 수락][out62] · [실행 영수증][rc63] · [슬롯][sl64] · [실행 원장][run64]

## 060까지 이어받은 연구 흐름

목표는 전체 또는 일부 소프트웨어 설계와 목적을 받아 완성품·부품·타 분야의 원리를 찾고, 어디에 왜 적용할 수 있는지 링크로 알려 주는 것이다. 연구 묶음을 받아 조립할 설계자에게 입력 형식, 저장량, 검색 방법, 갱신 방식은 열린 선택으로 남아 있다. 아래 수치는 각각의 표본과 열람 예산에 속한다. [제품 브리프][product] · [연구 운영 규칙][rule] · [누적 검토와 근거 위치][prev]

| 설계 질문 | 앞선 작업에서 확인한 것 | 남은 제약과 반례 |
| --- | --- | --- |
| 부분 요청의 목적과 금지 조건을 어떻게 보존하는가 | DOT-001·002는 세션을 바꿔 인계를 복원했다. RES-001~004에서는 합성 입력 6건에서 부정 조건이 누락됐고 2문제·17질의에서 동명 제품과 부분 기능이 섞였다. 020은 주장 72/73을 전달했다. | 016의 내부 판독 일치는 후보 형태 78.3%, 기여 70.8%였다. 020의 충돌 16건 중 완전 해소는 2건. 026의 실제 추가 질문 발송은 0건, 030의 직접 답변 3건에서 권고 변경과 요청자의 후속 실행이 함께 연결된 경우는 0/3이었다. [누적 검토][prev] |
| 분야나 제품명을 모를 때 다른 원리를 찾는가 | 009의 35개 대상에는 기능 중복이 있었다. 010은 분야 단서와 원전 24개에서 원리 7군을 찾았다. 011은 61스레드·635답에서 부분 질문의 진전 10/33을 확인했다. | 타 분야 답 14개에는 요청자 반응이 없었다. 012의 합성 근접 오답 증가는 014의 실제 자료 485개에서 재현되지 않았다. 013의 당시 선례 회수는 웹 16/176·목록 5/176. 025의 72칸 중 지지 2, 029의 세 경로는 각 완결 0/12, 033의 분야 단서 없는 144쌍은 넓은 엄격 지지 1쌍·당시판 지지 0쌍이었다. [누적 검토][prev] |
| 원전을 알면 구현 선택이나 재작업이 달라지는가 | 022의 결정 우선 2/24에서 이미 알던 대안의 조건을 고쳐 시행했다. 037은 같은 목적의 반영을 결정 우선 7/8·노출 우선 3/4에서, 046은 링크 우선층에서 같은 작성자·목적 수정 2/4를 찾았다. 049는 Matplotlib 3.0.2의 좌표 선택에 따른 출력·예외 차이를 재생했다. | 미인지부터 변경·시행까지 이은 022 사례는 결정 우선 0/24, 발견 진술 우선 1/9였다. 046의 첫 링크를 수정 이유로 명시하고 시험까지 이은 보강 사례는 0/4. 053의 채운 5자리와 057의 공동 편집 6자리 모두 동종 근거와 타 분야 근거의 예측이 같았다. 057의 Yjs 13.6.28에서 undo 그룹 경계의 효과는 확인됐지만 당시판·입력·두 조작·redo의 완전 공개 쌍은 0/6이었다. [누적 검토][prev] |
| 설명이나 예제로 사람의 판단과 시간이 개선되는가 | 021의 두 번 열람에서 요구 완결은 주소만 6/23, 절 목록 9/23, 요구–절 대응 13/23, 잘못 대응한 보기 8/23이었다. 054의 eXoaDocs 실험에서 40분 내 네 과제 정확 완료는 예제 제공 3/12 대 기존 문서 1/12였다. | 038의 실제 참가자는 0명. 034의 패키지 선택 중앙값 380→57초에 비해 전체 과제는 849→847초였다. 050의 시간·최종 품질 원행 신규 결합은 0/8. 054의 단일 과제는 3/12 대 4/12로 방향이 바뀌었다. 058의 진단층에서 단어 강조 후 전체 정답 990/1,600→1,160/1,600과 오수락 123/205→152/205가 함께 늘었고, 주 선정층의 정오별 수락 원개수는 0셀 회수였다. [누적 검토][prev] |
| 추천 이유는 언제 다시 확인해야 하는가 | 015의 현재 판정 가능 이유 195개 중 붕괴 14개. 과거 83개 중 뒤늦은 붕괴 5개와 최초 오류 4개. 032의 12참조는 모두 HTTP 200이어도 교체할 이유가 있었다. 055·059는 베이루트 특정 순간의 현지 날짜가 중간 시간대 판에서만 달라짐을 좁혔다. | 019의 사건·대조 7쌍에서 경보는 각 3건. 024의 분기 예산 10/20/40회에서 정기 대 신호 후 발견은 각각 7 대 0, 11 대 8, 11 대 11(분모 11)이었다. 059에서 배포 파일 14/14의 해시와 정·역순 실행 72행을 확인했지만 두 소비 프로젝트 모두에서 과거 사용자 프로세스의 로드를 확인할 수 없었다(확인 0/2). 같은 패키지를 설치해도 호스트 자료 우선 여부에 따라 값이 갈렸다. [누적 검토][prev] |
| 어떤 기록으로 과거 주장과 실제 사용판을 복원하는가 | 023에서 주소·이유, 판·근거 추가, 변경 관계·시점 추가의 복원은 3/18→5/18→15/18이었다. 039는 옛 발췌 12/12를 다시 표시했다. 051 통제에서 경로·필드·변환은 64/64 판정과 일치했다. 055의 과거 답 복원은 주소·이유 0/4, 옛 판·해시 2/4, 사용 행까지 4/4였다. | 027·032의 상류 변경과 소비 배포일 연결은 0/12·0/6, 043의 자연 사용판은 0/4, 047의 소비 우선층 외부 입력 연결은 0/6이었다. 051에서는 불완전한 목록을 완전하다고 두자 거짓 음성 3건이 생겼다. 055의 세 보기 모두 다음 판 판정은 0/4였다. [누적 검토][prev] |
| 상위 링크에 대안과 필요한 근거가 같이 남는가 | 040의 URL·상류·부품별 표시는 필수조건 8·6·8개를 보존했다. 044 보강층의 완전 대안은 2·11·1·0개로 갈렸다. 052는 묶음을 바꾸면 5번 후보가 드러나도 미러의 보완 관계일 수 있음을 보였다. 056은 목록 62행에 정의 기반 용어를 넣어 후보 있는 요구를 0/8→1/8로 늘렸다. | 060에서 원문 질의·게시 필드부터 확장 질의·추가 기능 필드까지 넓히자 후보 있는 요구는 기존층 0/8→4/8, 새 층 0/4→2/4였다. 후보가 밀린 사례도 있었다. 고유 28쌍에서 공동 조건 완결 0, 이름 전이를 허용한 부분 근거 1, 미확인 27. 열람 예산은 81/84 경로에서 확인됐다. [누적 검토][prev] |

## 새 자료에서 확인한 것과 판단이 끊기는 곳

### 061 · 같은 원리를 설명해도 제품의 경계 동작까지 결정되지는 않는다

D3 문서는 Barnes–Hut를 명시한다. 고정판의 공간 집계와 힘의 크기는 따로 비교할 수 있다. d3-force 3.0.0의 해당 코드에서 힘의 크기는 거리의 역수에 비례했고, 음수 세기와 거리 제한이 있었다. Graphviz sfdp가 직접 지목한 Hu는 그래프 분야 논문이고 그 논문이 Barnes–Hut를 인용한다. Android와 react-spring에 대응시킨 물리 교재는 연구자가 골랐다. 구현자가 그 교재를 읽고 선택했다는 기록은 미확인이다. Android 보조 실행에서는 16ms 내부 계산이 목표 100을 넘어 100.0375였어도 외부 속성은 100·속도 0으로 종료됐다. react-spring의 1ms 관측에서는 clamp를 켜도 242ms에 1.00266이 보였고 다음 표본은 1이었다. [차용·변수 대응][tr61] · [판별 입력과 관측][ob61] · [결과][r61]

8행 중 Graphviz 2행에는 동종 예제 보기가 없고, 공개 한 단계 입력과 원출력도 확보하지 못했다. 두 보기를 제공한 6행에서 구현 동작에 대한 사전 예측 차이는 0/6이다. **원전이 다른 예측을 새로 맞힌 비율은 분모가 0이라 계산할 수 없다.** 같은 판·같은 입력의 독립 원출력은 0/8, 연구자 보조 실행은 6/8이다. 단말 화면, 실제 React 앱, 사용자 선택은 이 실행 범위 밖이다. 053·057과 함께 보면 원전이 무엇을 설명하는지는 보이지만, 다른 설계자가 원전을 받으면 구현 선택이 달라지는지는 여전히 열려 있다. [사전 비교 규칙][rule61] · [예측 행][pr61] · [관측 행][ob61]

### 062 · 같은 답에 출처를 붙이는 것과 검색을 권하는 것의 결과가 달랐다

Kim의 Study 2는 같은 답 템플릿에 출처 3개를 더했다. 오권고 수락은 설명이 없을 때 78.2%→68.2%, 있을 때 82.8%→76.9%였다. 두 차이는 저자가 보고한 반올림 평균이다. 출처 제공 시행 1,232회 중 적어도 한 링크를 클릭한 시행은 318회였고, 원문 로드·독해·시행별 최종 선택의 결합은 미확인이다. 이번 검토에서 부록 추출표의 72자리(12문항×정오 2×링크 3)를 주소 문자열로 묶었다. **67개 URL 중 5개가 네 문항에서 각각 옳은 권고와 틀린 권고 양쪽에 쓰였다.** 예를 들어 Port Royal 문항의 양쪽 두 번째 링크는 동일하다. 문장과 연결된 정확한 절을 읽어야 어느 쪽을 뒷받침하는지 판정할 수 있다. [정오별 결과][out62] · [클릭 원장][clk62] · [부록의 링크 자리][stim62]

Aslett Study 1은 자유 검색을 권유했다. 관측한 응답에서 오주장 수락은 356/1,188→420/1,161(+6.21%p), 오주장을 정확히 판정한 응답은 387/1,188→367/1,161(−0.97%p)이었다. 정오키가 있는 관측 응답 전체의 정답은 2,224/4,478→2,413/4,366(+5.60%p)이었다. ‘판단 불가’ 응답이 있어 오수락의 여집합 전체를 정답으로 셀 수 없다. 원래 배정된 전체 인원과 미관측 시행을 연결한 코호트는 0개였다. 058과 같은 방향의 반례가 별개 과제에서 나왔지만, 링크 제공·강조·검색 권유의 효과를 합치거나 소프트웨어 부품 선택으로 옮길 근거는 없다. [원개수와 조건][out62] · [재집계][sum62] · [선정과 결측][r62]

### 063 · 보고된 출력과 실제 로드판은 각각 확인해야 한다

자연 보고 6건 중 날짜·오프셋 문자열은 4건에 있었다. 나머지 둘은 예외와 정성 보고였다. 같은 실행의 입력·지역·공급자 자료판·출력까지 연결된 사례는 0/6이었다. pandas #39398은 원 입력이 27일부터인데 하루를 더했다는 결과는 29일부터 시작한다. 게다가 서로 다른 두 pytz 전체판에서 Berlin 지역 파일 바이트가 같았다. 실행 순서와 읽은 파일을 따로 확인해야 한다. 보강 후보인 pandas 원 실행 15건의 로그 요청은 13건이 410, 2건이 404였고 네 보강 자리는 모두 비었다. 실패한 조회 수는 과거 실행이 없었다는 증거로 쓸 수 없다. [보고별 원장][rc63] · [후보판 비교][ed63] · [원 로그 조회][logs63]

반대 방향의 기록도 있다. 별도 보조 사례 Moment #967에서 유지보수자는 같은 REPL 문맥에 São Paulo의 입력, 출력 08:05:14−03:00, 공급자가 표시한 `dataVersion=2021e`를 남겼다. 이는 공급자 라벨 수준에서의 연결이고 실제 열린 파일의 해시는 미확인이다. 다른 분야에서도 Dataverse V1/V2의 전체 파일 수는 5개와 61개인데 같은 통합문서의 파일 지문은 같았다. 059의 배포 가능판과 063의 자연 보고·보조 보고를 합쳐 ‘당시 사용자가 이 판을 썼다’로 일반화할 수 없다. [층별 집계][ct63] · [후보판과 지문][ed63] · [원 REPL 기록](https://github.com/moment/moment-timezone/issues/967#issuecomment-1019463236)

### 064 · 도착 절을 바꿔 아낀 읽기와 확보한 증거를 따로 셀 수 있다

12요구의 상위 36슬롯은 후보 11, 무매치 18, 풀 소진 7이었다. 같은 후보·판·순위에서 시작 주소와 기능 절 주소가 실제로 달랐던 쌍은 6/11이었다. 두 번째 보기에서 논리 열람은 14→12회, 표시 단어는 6,948→5,747로 줄었고 논리적으로 요청한 원문 바이트는 3,377 늘었다. 두 조건과 환경을 같은 경로에서 확인한 결과는 양쪽 모두 **0/11쌍, 0/12요구**였다. jschon의 정정 전 창까지 본 노출을 제외하면 각 보기 10쌍, 합계 20/22경로다. 사람의 시간은 측정하지 않았다. [슬롯][sl64] · [경로][rt64] · [비용][cost64] · [노출 정정][ex64]

문서에서 보류한 후보 중 Ajv 8.17.1은 합성 draft-07 입력 네 군에서 기대와 모두 맞았다. jschon은 원 draft에서 평가 전에 멈췄고 2020-12 재구성에서 4/4였다. Ruby JSON-LD는 원 URL에서 context 로드가 실패했고, 재구성에서는 값 선택 4/4에도 credential 구조의 정확한 보존은 0/4였다. 문서 근거가 없다는 사실, 다른 환경에서 한 재현, 요청자 환경에서의 성공을 하나의 오탐률로 바꿀 수 없다. 060의 조건부 부분 근거 한 건은 064의 정해진 창에서 확인되지 않았고, 사후 Ajv `properties` 창에서는 개명을 전제로 한 부분 근거가 나타났다. 좁은 절을 미리 고르는 규칙이 새 요구에서도 통할지는 별도 검사가 필요하다. [봉인한 판정][jud64] · [세 구현 실행][run64] · [사후의 절][post64]

## 다음에 무엇을 결정할 수 있는가

| 독립 과제 | 앞선 공백을 겨냥한 비교 | 설계자가 받을 판단 |
| --- | --- | --- |
| AF-RES-065 · web-pro | 061의 0/6 예측 차이에서 계산할 수 없었던 원전의 역할을, 사진 갤러리와 악보의 줄 나눔 결정 이력에서 조사한다. 요구로 찾은 사건과 인용으로 찾은 사건을 따로 센다. | 타 분야 원전, 실제 구현 절, 남겨 두어야 할 간단한 대안 중 무엇을 어떤 근거로 연결할지. |
| AF-RES-066 · web-pro | 062의 72개 출처 자리 전부에서 정오 권고의 주장과 당시·현재의 도착 절을 대조한다. 같은 주소가 양쪽에 쓰인 5건도 포함한다. | 링크가 어떤 절에서 조건을 지지·반박하는지, 무엇을 직접 확인해야 하는지. |
| AF-RES-067 · web-pro | 063에서 끊긴 사용판 귀속을 Debian 빌드와 천문 보정 산출물의 장기 보관 기록에서 조사한다. 출력 식별자, 환경 선언, 실제 입력을 잇는 증거를 단계별로 비교한다. | 과거 값을 재인용할 때 남길 최소 기록과, 더 찾아야 할 실행 증거. |
| AF-RES-068 · codex-cloud | 064의 사후 좁은 절을 새 요구에 적용한다. 같은 후보·판에서 첫 화면, 넓은 기능 표제, 요청에 실제 쓰인 공개 심볼의 경로를 사전에 고정해 비교한다. | 절 지정이 두 조건의 검증을 늘리거나 적용 전제를 가리는 경우와 그 비용. |

네 과제는 각각 완료된 061·062·063·064 한 건만 인수한다. 065는 차용의 역사, 066은 이미 제시한 증거의 내용, 067은 과거 실행의 귀속, 068은 새 요청의 도착 경로를 답한다. 결과를 조합하면 H1(조건을 근거 절에 연결하는 것이 판단을 돕는가)과 H2(판이 바뀌어도 과거 추천 이유를 재확인할 수 있는가)를 별도로 검토할 수 있다. 필요할 때 새로 검색하는 안, 주소·목적·판을 저장하는 안, 발췌·실행 근거·판정 이력을 더하는 안 사이의 미결정 사항은 **실제 결정 개선량과 유지 비용**이다. [작업별 전체 지시문][next]

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/55d64c493634f6e09af2ac0ae4ec338bef4e0542/docs/workstreams/planning/REVIEW-15.md
[product]: https://github.com/laadkke-arch/agentflow-open/blob/028d16fee1121f5862efd410b78ec1d79d7080f2/docs/product/RESEARCH_BRIEF.md
[rule]: https://github.com/laadkke-arch/agentflow-open/blob/028d16fee1121f5862efd410b78ec1d79d7080f2/docs/RESEARCH_WORKFLOW.md
[oldreg]: https://github.com/laadkke-arch/agentflow-open/blob/aa1dc65e4eefa9df9a8e8ae694ffadda52a12a75/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/028d16fee1121f5862efd410b78ec1d79d7080f2/docs/automation/dot-control.json
[next]: NEXT_TASKS-16.json
[h61]: https://github.com/laadkke-arch/agentflow-open/blob/bf9f27eb67b1f72b243297c1672bea9b2524e4e4/docs/workstreams/research/AF-RES-061/HANDOFF.md
[r61]: https://github.com/laadkke-arch/agentflow-open/blob/1ea731294c57c233ae164e3c31cd69c57b8896aa/docs/workstreams/research/AF-RES-061/RESULT.md
[a61]: https://github.com/laadkke-arch/agentflow-open/blob/1ea731294c57c233ae164e3c31cd69c57b8896aa/docs/workstreams/research/AF-RES-061/evidence/acceptance-evidence.json
[pr61]: https://github.com/laadkke-arch/agentflow-open/blob/1ea731294c57c233ae164e3c31cd69c57b8896aa/docs/workstreams/research/AF-RES-061/predictions.csv
[ob61]: https://github.com/laadkke-arch/agentflow-open/blob/1ea731294c57c233ae164e3c31cd69c57b8896aa/docs/workstreams/research/AF-RES-061/observations.csv
[rule61]: https://github.com/laadkke-arch/agentflow-open/blob/1ea731294c57c233ae164e3c31cd69c57b8896aa/docs/workstreams/research/AF-RES-061/evidence/comparison-rule.json
[tr61]: https://github.com/laadkke-arch/agentflow-open/blob/1ea731294c57c233ae164e3c31cd69c57b8896aa/docs/workstreams/research/AF-RES-061/transfer.csv
[h62]: https://github.com/laadkke-arch/agentflow-open/blob/36e50408139d35022c2fe527ff2f05216f24516c/docs/workstreams/research/AF-RES-062/HANDOFF.md
[r62]: https://github.com/laadkke-arch/agentflow-open/blob/bb3c627bf94f16418e3d71f56b7838b0c60d5e04/docs/workstreams/research/AF-RES-062/RESULT.md
[a62]: https://github.com/laadkke-arch/agentflow-open/blob/bb3c627bf94f16418e3d71f56b7838b0c60d5e04/docs/workstreams/research/AF-RES-062/evidence/acceptance-evidence.json
[out62]: https://github.com/laadkke-arch/agentflow-open/blob/bb3c627bf94f16418e3d71f56b7838b0c60d5e04/docs/workstreams/research/AF-RES-062/outcomes.csv
[sum62]: https://github.com/laadkke-arch/agentflow-open/blob/bb3c627bf94f16418e3d71f56b7838b0c60d5e04/docs/workstreams/research/AF-RES-062/streams/root/independent-calculation.json
[stim62]: https://github.com/laadkke-arch/agentflow-open/blob/bb3c627bf94f16418e3d71f56b7838b0c60d5e04/docs/workstreams/research/AF-RES-062/streams/a/fostering-source-links.csv
[clk62]: https://github.com/laadkke-arch/agentflow-open/blob/bb3c627bf94f16418e3d71f56b7838b0c60d5e04/docs/workstreams/research/AF-RES-062/streams/a/voluntary-clicks.json
[h63]: https://github.com/laadkke-arch/agentflow-open/blob/8e348bb1306d5243b0a5ff8ebae773707d2dcfb4/docs/workstreams/research/AF-RES-063/HANDOFF.md
[r63]: https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/RESULT.md
[a63]: https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/acceptance-evidence.json
[rc63]: https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/receipts.csv
[ed63]: https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/candidate-editions.csv
[logs63]: https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/artifacts/pandas-log-attempts.json
[ct63]: https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/integrated-counts.json
[h64]: https://github.com/laadkke-arch/agentflow-open/blob/c522e0165815b02da25b065b4d781e3aee0fbf25/docs/workstreams/research/AF-RES-064/HANDOFF.md
[r64]: https://github.com/laadkke-arch/agentflow-open/blob/6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f/docs/workstreams/research/AF-RES-064/RESULT.md
[a64]: https://github.com/laadkke-arch/agentflow-open/blob/8f97be50a4071e05e138c5237569e94c512c5abd/docs/workstreams/research/AF-RES-064/evidence/acceptance-evidence.json
[sl64]: https://github.com/laadkke-arch/agentflow-open/blob/6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f/docs/workstreams/research/AF-RES-064/slots.csv
[rt64]: https://github.com/laadkke-arch/agentflow-open/blob/6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f/docs/workstreams/research/AF-RES-064/routes.csv
[jud64]: https://github.com/laadkke-arch/agentflow-open/blob/6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f/docs/workstreams/research/AF-RES-064/judgments.csv
[cost64]: https://github.com/laadkke-arch/agentflow-open/blob/6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f/docs/workstreams/research/AF-RES-064/evidence/costs.json
[ex64]: https://github.com/laadkke-arch/agentflow-open/blob/6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f/docs/workstreams/research/AF-RES-064/evidence/actual-exposure.json
[run64]: https://github.com/laadkke-arch/agentflow-open/blob/6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f/docs/workstreams/research/AF-RES-064/runs.jsonl
[post64]: https://github.com/laadkke-arch/agentflow-open/blob/6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f/docs/workstreams/research/AF-RES-064/evidence/posthoc.json
