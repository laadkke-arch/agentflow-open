# REVIEW-36 · 어떤 링크를 저장하고, 어느 요청에 다시 써도 되는가

이 제품은 설계 중인 소프트웨어의 전체 또는 일부와 목적을 받아, 가까운 오픈소스·서비스·기능과 다른 분야에서 빌릴 수 있는 원리를 원문 링크로 건넨다. 36차에서 가장 강한 근거는 **같은 링크의 쓸모가 요청의 세부 조건에 따라 달라진다**는 것이다. 날짜 정제 명령은 성공했어도 열 전체가 텍스트로 남을 수 있었고, 숫자 함수의 지정 문서 절이 그대로여도 한 배포판은 공개 진입점에서 열리지 않았다. 반면 새로운 원리를 발견한 사람이 실제 설계 결정을 바꾸고 총노동을 줄였는지는 미확인이다. 다음 네 작업은 이 차이를 검색, 저장, 요청 전달, 설계 결정에서 각각 검사한다. [제품 연구 목표][goal] · [실행 후의 추천 분기][dec144] · [배포판 비교][pairs143]

## 어떤 작업을 새로 검토했나

계획 브랜치에서 번호가 가장 큰 REVIEW-35를 먼저 읽었다. 거기서 사용한 통합판 `d950356`과 2026-11-24의 `9ad2ffc`에서 진행표의 모든 작업을 ID로 대조했다. 기존 138행은 모든 필드가 같았고, 새로 추가된 141~144 네 행이 모두 DONE이었다. 현재 전체 142행 중 DONE 140, BLOCKED 2다. 연구만 세면 140건 중 인계 138, 차단 2(018의 범용 웹 검색 동예산 비교, 035의 호출 경계 값·타입 보존)이고 나머지 DONE 두 건은 연결 시험이다. 중앙 DONE 140행의 `acceptance_evidence`는 모두 빈 배열이다. 새 네 작업의 자체 수용 판정은 모두 **PARTIAL**이다. [직전 누적 검토][prev] · [직전 진행표][oldreg] · [이번 진행표][reg]

| 새 인계 | 등록된 인계판 | 결과 본문판 | 해당 작업의 고정 원장에서 다시 센 단위 |
| --- | --- | --- | --- |
| 141 · 실제로 빌린 연산 | [db0e26a · PARTIAL][h141] | [764e893][r141] | 모집 64자리, 반환 PR 52, 심층 8개 PR의 조작 11개, 대응 18행, 출처 132행 중 산입 고유 33저작 |
| 142 · 후보 목록과 한국어 요청 구절 | [1fa9555 · PARTIAL][h142] | [6c379fe][r142] | 11요청×22후보 242쌍, 순위 836행, 조사·표시 484자리 중 표시 132자리, 출처 82행 중 고유 23저작 |
| 143 · 배포판 재확인과 실제 비용 | [61823fd · PARTIAL][h143] | [b6519bd][r143] | 배포 24판, 인접 경계 22, 셀쌍 5,696, 비용 1,080질의, 출처 109행 중 고유 34저작 |
| 144 · 원저자 조건과 정확판 실행 | [9283340 · PARTIAL][h144] | [ad394b7][r144] | 사례 5, 입력 24, 실행 137행·CLI 호출 149개, 댓글 21, 출처 116행 중 고유 30저작 |

네 작업 브랜치의 조회 head와 등록 인계 SHA가 일치했고, 각 인계판의 RESULT.md는 표의 본문판과 같은 Git blob이었다. 141의 사건·대응표에는 결과 본문 뒤에 추가한 재확인 열이 있어 인계판에서 읽었다. 141·142는 작업자가 고정 파일을 원격 검산했고 지정 checkout 검사는 미실시다. 143·144는 각각 결과판의 재생 영수증이 있다. 이 검토에서는 원장 행·범주·짝·분모를 재계산했다. 패키지와 CLI 실측은 해당 작업자의 기록을 인용한다. 이전 연구의 수치는 REVIEW-35에서 이어받았고, 새 비교에 필요한 시제품의 검색 한도와 판독 경로만 코드에서 별도로 확인했다. [141 사건][events141] · [142 재집계][check142] · [143 검사][check143] · [144 재생][check144] · [시제품 호출 경로][prototype]

## 1~35차에서 이어 온 판단

| 설계자가 결정할 질문 | 지금까지 남은 근거 | 적용할 때 남는 조건 |
| --- | --- | --- |
| 원래 몰랐을 다른 분야 원리가 발견되는가 | 010은 분야 단서를 받고 원리 7군을 찾았다. 단서 없이 고정 자료를 본 033은 144쌍 중 넓게 인정한 지지 1, 당시판 지지 0이었다. 022의 미인지→변경→시행은 0/24였다. 109는 시험 27개를 제안했다. 117·121·125·129의 이력에서는 최초 작성자의 늦은 발견과 노동까지 잇지 못했다. | **검색으로 찾은 것, 독자가 처음 안 것, 실제 바꾼 결정**은 별도 사건이다. 137의 xarray #9618은 링크에 있는 네 타입 중 세 개가 같은 작성자의 주석·배포판에 남았으나 실행 비교식은 그대로였다. 141은 일부 차용과 선행 인지의 다른 사례를 더했다. |
| 선택한 부분과 함께 얼마만큼의 문맥이 필요한가 | 020은 주장 72/73을 전달했으나 충돌을 모두 해결한 것이 2/16이었다. 074의 구성 사례는 추가값으로 8/8 갈렸고, 111의 동의어 변경은 두 방식 모두 완전 정합 0/6이었다. 실제 도표 6건을 본 119에서 원요구만으로 정확 0, 이웃이나 직접 참조를 주면 각각 3이었다. 123은 같은 x의 1px 이동도 시작 대상에 따라 다른 달을 선택했다. | 원문·선택 위치·바꿀 동작·보존값·직접 이웃 중 어느 것이 답을 바꿨는지 기록해야 한다. 전체 프로젝트 입력이나 고정된 Studio 전달 형식의 필요성은 미확인이다. |
| 검색한 후보 중 무엇을 답에 올리는가 | 076은 자연 6요구×20후보에서 직접 적격 0, 목록을 넓힌 080은 자연 1/5·교정 3/5였다. 118에서는 표시 직접·일부·충돌이 9·7·15에서 8·0·0으로 줄었다. 126의 실제 10요구는 활성 별칭 적중 0, 구성 예에서는 직접 3과 충돌 1이 같이 들어왔다. 134의 엄격 표시에서는 조건부로 가능한 직접 후보까지 사라져 18자리가 비었다. 138의 실제 별칭 ‘가중치를’는 저장된 모델, 찾아낸 기능은 표본 인덱스를 가리켰다. | 목록에 없음, 이름이 달라 0점, 조사 순위 밖, 원문 판독 후 보류는 다음 행동이 다르다. 최종 표시 개수와 안에서 검토할 개수도 따로 비교할 수 있다. |
| 무엇을 저장하면 과거 답을 복원하고 현재판에도 쓸 수 있는가 | 055는 옛 판단 4/4와 다음 판 판단 0/4, 071은 원문 절·설정으로 옛 사례 22/22를 복원했다. 075는 전체 후보가 없어 단독·공동 1위 주장을 각각 16/16 보류했다. 106은 주소가 살아도 옛 예제의 용도가 사라지는 경우를 찾았다. 135의 d3-scale 3.2.3→3.2.4에서 같은 README 아래 기본 null 출력이 0에서 undefined로 바뀌었다. 139는 같은 경계에서도 스칼라와 사후 벡터 입력의 관측이 달랐다. | URL은 가벼운 등록 단위로 쓸 수 있다. 이전에 전달한 설명, 요청한 판에서의 동작, 당시의 전체 순위를 다시 판단하는 데 필요한 기록은 다르다. 최소 저장 필드와 재확인 시점은 시험할 선택지다. |
| 링크나 기술 원문 하나를 더 주면 무엇이 개선되는가 | 021의 두 절 예산에서 근거 충분은 주소만 6/23, 절 목록 9/23, 맞춘 절 14/23, 잘못 맞춘 절 8/23이었다. 034의 부분 시간은 380→57초, 전체는 849→847초였다. 124의 추가 시험 후 핵심 처방 수정은 0/6이었다. 132의 독자 한 명은 조건부 대안을 하나 얻었지만 136 재판독에서 도구 제약·후반 선노출이 드러났다. 140의 CSV·YAML에서 열린 둘째 절 7개는 보강·유지 5, 판 후보 축소 1, 조건부 후보 추가 1, 새 핵심 해결 0이었다. | 더 직접적인 원문, 더 구체적인 검사, 실제 적용, 사람의 총 시간에는 별도 근거가 필요하다. 원저자가 이미 결정한 조건과 공개 규약을 찾아 풀 수 있는 조건도 나눠야 한다. |
| 부품 하나의 근거를 조합 전체에 쓸 수 있는가 | 078은 개별 기능을 합쳤을 때의 실패, 103은 외관 10/10 보존과 텍스트 선택 소실, 107은 단일 발생 편집에서 공유 정의 0/6·위치 지정 6/6을 보였다. 127의 지도에서는 처리 순서에 따라 피처와 중심이 같이 움직였고 131에서는 같은 설정도 6.6.1→6.7.0에 동작이 갈렸다. 137의 두 희소 반환형은 같은 마스크에서 곱의 뜻이 달랐다. | 링크를 추천한 근거는 입력·반환값·다음 연산·편집 범위 중 확인한 지점까지만 승계한다. 실제 독자가 가져다 쓴 지점과 대상 환경의 보존 조건은 별도로 남긴다. |

누적 정정도 유지한다. 114의 ‘충돌’ 138/144는 118의 명시 반박 기준에서 충돌 7·미확인 131이며 나머지 6은 일부다. 119의 M3994 원형 MG 좌표 y는 11.71875, 공유 변경 뒤는 275다. 136의 고유 면 수는 본문 해시 기준 9이며, 10회 열람·답과 면의 연결 16쌍과 단위가 다르다. 연구 파일의 열을 미래 제품 DB에 그대로 옮길지, AI 전처리나 상시 수집을 둘지는 아직 열린 결정이다. [35차 근거와 정정][prev] · [연구 자료의 용도][wf]

## 새 결과의 근거와 한계

### 141 · 출전 링크의 어느 부분이 실제로 쓰였나

Matplotlib #24976 작성자는 직접 링크를 받기 전에 외부 타입 스텁을 알았다고 답했다. 저장소의 최초 공개 코드와 v3.8.0 태그에서 zorder의 float가 유지됐다. 한편 #24891의 문서 제목과 이전 주소 연결은 링크 없는 리뷰 제안 뒤 수정됐고, 사건 원장의 후속 확인에서 v3.7.0 소스까지 연결됐다. 보충 사례 #26278은 원전 예제 두 개에서 일부 표현을 결합했고 마스크·레벨 등은 옮기지 않았다. Pillow #6926의 래퍼 복사 자인은 해당 PR 브랜치까지다. 이를 ‘외부 기능 전체를 처음 배워 배포했다’고 기록하면 주체·시점·연산이 모두 달라진다. [제안에 대한 작성자 답][stubs] · [사건별 후속 확인][events141] · [연산별 대응][transfer141]

52개 PR 중 33개는 검색 목록만 확인했고 19개에서 본문이나 대화·diff를 읽었다. 그중 12개도 세 대화 목록의 첫 페이지 수준이고 7개는 부분 판독이었다. 8개 심층 PR의 최초 적격 순서, 전체 채택률, 최초 배포 설치물, 노동시간은 미확인이다. 서체 원자료에서는 같은 글리프의 두 마스터 좌표를 보았지만 단위와 fork 기준판이 달라 실제 인쇄 모양까지 확정할 수 없다. 출처 33저작과 독립 검토·사용자 효능은 별개의 수치다. [모집 깊이][frame141] · [작업자 자체점검][self141]

### 142 · 정답표에 있는 후보가 표시되지 않은 이유

11×22의 고유 쌍은 직접 2, 일부 6, 충돌 3, 미확인 231이었다. 직접 두 쌍 모두 요청 전체를 넓게 읽으면 일부로 내려간다. 신규 중립층에서는 네 정책 각각 18자리, 합계 **0/72 표시**였다. N1-07의 데이터셋 가져오기를 좁게 읽으면 D01이 직접이지만 모든 조합에서 점수가 0이었다. 교정층 60자리 중 유일하게 표시된 C-P1-07/S04는 준비된 입력을 분류기에 주는 하위 동작이다. 이미 후속 답을 본 사례이고, 목표 구절만 살리자 점수를 잃었다. 목록 확대의 자연 신규 효과와 어휘 처리의 효과를 이 한 자리로 입증할 수 없다. [전수 등급][truth142] · [표시 전수][slots142] · [정책 간 이동][paired142]

신규 중립 여섯 명 중 두 건은 질의어가 템플릿에 나타나 엄격한 적격 표본이 네 명 이하일 수 있다. 목적층은 예정 20자리에서 반환 0이고 원격 검색의 전체 건수는 미확인이다. 82출처행 중 산입한 고유 저작 23은 작업 하한 24에 한 건 모자랐다. 교통기관의 스키마는 읽었지만 개별 운행 레코드는 확보하지 못했다. 같은 작업자가 표시와 기준을 판독했고 실제 PyTorch 실행·사용자 클릭은 측정하지 않았다. 후속 재생에 쓸 requests.jsonl에는 신규 6행만 있다. 11건의 점수를 재구성하려면 교정 5건의 원문은 142가 인용한 138의 고정판에서 가져와야 한다. [모집 기록][frame142] · [신규 요청 원장][requests142] · [자료 집계][s142]

### 143 · 수치, 실행 가능 여부, 비용에는 각자의 분모가 있다

simple-statistics 8판과 d3-array 16판에서 비교 예정 5,696셀쌍 중 **5,370쌍 불변, 326쌍 미확인**이었다. 비교 가능한 수치·예외·인수 변화 양성은 0이므로 변화 검출률은 산출할 수 없다. 7.8.6은 두 설치에서 지정한 공개 require가 실패했다. 문서 절만 본 정책 C가 이 판에 직전 답을 잘못 이월한 756응답은 같은 실패의 반복(빈 캐시 378, 보존 캐시 378)이다. 한편 공개 진입의 실패·복구 경계는 실제 두 건이다. 다른 로더에서의 성공이나 함수 값 자체의 변화는 미확인이다. [셀별 원장][cells143] · [판쌍 원장][pairs143] · [비용 요약][cost143]

같은 기계의 빈 캐시 d3-array 순차 질의에서 매번 요청판을 실행한 A는 중앙값 30.706초·Node 16회, 함수·위임·공지 등의 신호로 고른 E는 12.752초·2회였다. 두 끝판만 번갈아 찾으면 A 9.743초·166,147바이트, E 11.286초·577,156바이트였고 공개 Node 실행은 각각 6회였다. 어느 정책이 싼지는 요청 분포와 재사용 상태가 가른다. ONS 원표 ZIP을 직접 읽은 수는 0이고 Census 동일 기준일의 개정값은 기관 발표 HTML에서 확인됐다. 계획표와 실제 운행, 발표표와 원자료를 구별해야 한다. [측정 원장][cost143] · [분야별 관측][domains143]

### 144 · 실행으로 알 수 있는 조건과 저자에게 남은 조건

137개 실행행(성공 103·실패 34), CLI 149회, 입력 24개에서 기술적으로 다른 첫 답이 나왔다. csvkit C4에서는 1.0.5에서 유효한 날짜 열이 파이프를 거쳐 Date가 됐다. 존재할 수 없는 날짜 하나를 섞으면 두 명령이 모두 성공 종료해도 열은 Text로 남았다. yq Y2에서는 세 LF가 든 구성 입력으로 4.30.6 실패·4.30.7 성공이 재현됐다. Y3에서 블록 표기를 위해 CRLF를 LF로 바꿔도 되는지는 작성자의 공개 발언에 나오지 않았다. Y4의 공개 배열 순서는 원문 한 절로 충족했고, 주석과 서식까지 보존할 경우에는 두 식의 결과가 갈렸다. 종전 질문 후보 네 개 중 C4·Y2 두 개의 핵심은 기술 원전과 실행으로 좁혀졌다. [사례별 분기][dec144] · [실행 원장][runs144] · [Y3 작성자 보고][y3]

원장에는 저자 본문 예 3, 제3자 재구성 3, 연구자가 만든 대조 18입력이 있다. 주 쟁점 4개 중 당시 판의 저자 공개 예를 재현한 것은 C3·C4 두 건, Y2·Y3은 제3자/구성 자료였다. 원저자 제공 원파일과 최초 게시 본문은 모두 0/5다. 후속 댓글 21개의 공개·수정 시각과 현재 본문 해시를 맞췄어도 편집 전 요구와 동일했는지는 알 수 없다. 신문의 raw OCR·PDF 추출문은 읽었지만 원면의 글자 픽셀과 ALTO 좌표는 대응시키지 못했다. 가상 질문 발송 0회이므로 질문 응답률과 실제 채택도 미확인이다. [입력의 출처][fixtures144] · [공개 시각 원장][timeline144] · [타 분야 대조][domains144]

## 남은 불일치와 다음 배정

| 어느 결론이 충돌하는가 | 이번에 구별한 원인 | 다음에 답을 바꿀 관측 |
| --- | --- | --- |
| 출전을 인용한 변경은 있지만 처음 몰랐던 타 분야 원리가 선택을 바꿨는지는 남는다. | 일부 차용·기존 인지·문서나 시험의 수정·런타임 도입은 같은 사건에서도 갈린다. 사후 PR만으로는 링크를 보기 전 지식을 복원하기 어렵다. | **145**에서 검색 전 독자의 초안을 봉인하고, 일반 검색과 분야 단서 없는 관계 검색 뒤 실제로 달라진 선택·시험을 비교한다. |
| 카드를 늘려도 빈자리가 유지되고, 문맥을 더 주어도 도움이 된다고 보장할 수 없다. | 142는 0점·목록 공백·원문을 읽은 뒤의 보류가 다르고, 144는 사용자 선호처럼 보였던 두 쟁점을 실행으로 풀었다. 시제품은 첫 검색의 폭과 최종 표시 한도가 묶여 있다. | **146**에서 표시 세 자리를 고정하고 검토 폭과 비용을 바꾼다. **148**은 새 문서 사례에서 선택 위치에 실제 이웃 예 하나를 더한 효과를 무관한 형제 예와 비교한다. |
| 변경 신호는 반복 실행을 줄였지만 드문 조회에서는 더 무겁고, 안정된 숫자와 사용할 수 없는 판이 함께 관찰된다. | 자료의 판, 구체 입력, 공개 진입점, 관측 시점, 요청자가 유지할 값이 서로 다르다. 실패를 얼마나 오래 캐시하는지도 재조회 비용에 관여한다. | **147**에서 같은 링크를 다른 요청이 재사용할 때 세 저장안의 잘못된 이월·불필요한 보류·복원 가능성과 필드별 비용을 재생한다. |

| 작업·담당 | 시작할 때 필요한 고정 연구 | 단독으로 납품할 결과 |
| --- | --- | --- |
| 145 · web-pro | 141 | 공개 설계 8건의 검색 전·후 초안과 근거. 실제 독자의 설계 변경, 이미 알던 안, 사후에 얻은 비유를 구분한다. |
| 146 · codex-cloud | 142와 읽기 전용 시제품 고정판 | 같은 표시 세 자리에서 안쪽 검토 폭을 3→8로 바꾼 전환 원장. 되찾은 기능·원리, 추가 비용, 새 오탐을 함께 센다. |
| 147 · codex-cloud | 143 | 가벼운 주소 기록부터 요청별 근거 연결까지 세 저장안의 재생. 과거 답과 현재 답을 구분할 최소 필드를 제시한다. |
| 148 · web-pro | 144 | 새 공개 문서 사건 6건의 3면 가림 비교. 선택 부분, 이웃 참조, 아직 저자만 정할 조건을 전달하는 입력 계약 두 안을 낸다. |

각 작업은 전용 브랜치와 경로에서 이미 커밋된 선행 한 건으로 시작한다. 145의 독자 수정은 실제 원저자의 채택이나 사람 노동 절감과 별개로 보고한다. 네 결과를 조합하면 ‘어떤 요청을 받아 어떤 후보를 찾았고, 어느 판에서 무엇을 확인해 링크를 건넸는가’를 하나의 설계 결정까지 추적할 수 있다. [네 작업의 실행 지시문](NEXT_TASKS-36.json)

[goal]: https://github.com/laadkke-arch/agentflow-open/blob/9ad2ffc5974bf3379ce1f3fb947a9cf19bbdf673/docs/product/RESEARCH_BRIEF.md
[wf]: https://github.com/laadkke-arch/agentflow-open/blob/9ad2ffc5974bf3379ce1f3fb947a9cf19bbdf673/docs/RESEARCH_WORKFLOW.md
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/9ad2ffc5974bf3379ce1f3fb947a9cf19bbdf673/docs/automation/dot-control.json
[oldreg]: https://github.com/laadkke-arch/agentflow-open/blob/d950356cdfae3edf799870cdeb90b93b5bd4ffd3/docs/automation/dot-control.json
[prev]: https://github.com/laadkke-arch/agentflow-open/blob/f24907c8d9a8327e3e68a7ca8a102820ccd6782f/docs/workstreams/planning/REVIEW-35.md
[prototype]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/roundtrip.py#L111-L120
[stubs]: https://github.com/matplotlib/matplotlib/pull/24976#issuecomment-1384704595
[y3]: https://github.com/mikefarah/yq/issues/1506#issuecomment-1376667839
[h141]: https://github.com/laadkke-arch/agentflow-open/blob/db0e26aac95f34e77ad3c8bf898879f15558ae5c/docs/workstreams/research/AF-RES-141/HANDOFF.md
[r141]: https://github.com/laadkke-arch/agentflow-open/blob/764e89364f0491d6f27f12347b5bf1b2b4af98e4/docs/workstreams/research/AF-RES-141/RESULT.md
[events141]: https://github.com/laadkke-arch/agentflow-open/blob/db0e26aac95f34e77ad3c8bf898879f15558ae5c/docs/workstreams/research/AF-RES-141/events.jsonl
[frame141]: https://github.com/laadkke-arch/agentflow-open/blob/db0e26aac95f34e77ad3c8bf898879f15558ae5c/docs/workstreams/research/AF-RES-141/frame.csv
[self141]: https://github.com/laadkke-arch/agentflow-open/blob/db0e26aac95f34e77ad3c8bf898879f15558ae5c/docs/workstreams/research/AF-RES-141/SELF_CHECK.md
[transfer141]: https://github.com/laadkke-arch/agentflow-open/blob/db0e26aac95f34e77ad3c8bf898879f15558ae5c/docs/workstreams/research/AF-RES-141/transfer.csv
[h142]: https://github.com/laadkke-arch/agentflow-open/blob/1fa95555b2806f0c5cba492bff67cca6143a7b87/docs/workstreams/research/AF-RES-142/HANDOFF.md
[r142]: https://github.com/laadkke-arch/agentflow-open/blob/6c379fe049e8e8416c4a42df8dcb9f76de36b684/docs/workstreams/research/AF-RES-142/RESULT.md
[truth142]: https://github.com/laadkke-arch/agentflow-open/blob/1fa95555b2806f0c5cba492bff67cca6143a7b87/docs/workstreams/research/AF-RES-142/judgments.csv
[slots142]: https://github.com/laadkke-arch/agentflow-open/blob/1fa95555b2806f0c5cba492bff67cca6143a7b87/docs/workstreams/research/AF-RES-142/slots.csv
[paired142]: https://github.com/laadkke-arch/agentflow-open/blob/1fa95555b2806f0c5cba492bff67cca6143a7b87/docs/workstreams/research/AF-RES-142/paired.csv
[frame142]: https://github.com/laadkke-arch/agentflow-open/blob/1fa95555b2806f0c5cba492bff67cca6143a7b87/docs/workstreams/research/AF-RES-142/frame.csv
[s142]: https://github.com/laadkke-arch/agentflow-open/blob/1fa95555b2806f0c5cba492bff67cca6143a7b87/docs/workstreams/research/AF-RES-142/sources.jsonl
[check142]: https://github.com/laadkke-arch/agentflow-open/blob/1fa95555b2806f0c5cba492bff67cca6143a7b87/docs/workstreams/research/AF-RES-142/evidence/recount.json
[requests142]: https://github.com/laadkke-arch/agentflow-open/blob/1fa95555b2806f0c5cba492bff67cca6143a7b87/docs/workstreams/research/AF-RES-142/requests.jsonl
[h143]: https://github.com/laadkke-arch/agentflow-open/blob/61823fd1c98b52d44833bdada4c89708133b528a/docs/workstreams/research/AF-RES-143/HANDOFF.md
[r143]: https://github.com/laadkke-arch/agentflow-open/blob/b6519bd649411d3485f4a50fb8805d479e181f3b/docs/workstreams/research/AF-RES-143/RESULT.md
[pairs143]: https://github.com/laadkke-arch/agentflow-open/blob/61823fd1c98b52d44833bdada4c89708133b528a/docs/workstreams/research/AF-RES-143/evidence/output-pairs.csv
[cells143]: https://github.com/laadkke-arch/agentflow-open/blob/61823fd1c98b52d44833bdada4c89708133b528a/docs/workstreams/research/AF-RES-143/evidence/output-cells.csv
[cost143]: https://github.com/laadkke-arch/agentflow-open/blob/61823fd1c98b52d44833bdada4c89708133b528a/docs/workstreams/research/AF-RES-143/evidence/cost-summary.csv
[domains143]: https://github.com/laadkke-arch/agentflow-open/blob/61823fd1c98b52d44833bdada4c89708133b528a/docs/workstreams/research/AF-RES-143/domain-cells.csv
[check143]: https://github.com/laadkke-arch/agentflow-open/blob/61823fd1c98b52d44833bdada4c89708133b528a/docs/workstreams/research/AF-RES-143/evidence/acceptance.json
[h144]: https://github.com/laadkke-arch/agentflow-open/blob/92833407f665a6e28e4292491c261b7e0725c69c/docs/workstreams/research/AF-RES-144/HANDOFF.md
[r144]: https://github.com/laadkke-arch/agentflow-open/blob/ad394b702f077bc367b879e4d055fdc76016d0b6/docs/workstreams/research/AF-RES-144/RESULT.md
[dec144]: https://github.com/laadkke-arch/agentflow-open/blob/92833407f665a6e28e4292491c261b7e0725c69c/docs/workstreams/research/AF-RES-144/decisions.csv
[runs144]: https://github.com/laadkke-arch/agentflow-open/blob/92833407f665a6e28e4292491c261b7e0725c69c/docs/workstreams/research/AF-RES-144/runs.jsonl
[timeline144]: https://github.com/laadkke-arch/agentflow-open/blob/92833407f665a6e28e4292491c261b7e0725c69c/docs/workstreams/research/AF-RES-144/timeline.csv
[fixtures144]: https://github.com/laadkke-arch/agentflow-open/blob/92833407f665a6e28e4292491c261b7e0725c69c/docs/workstreams/research/AF-RES-144/fixtures.jsonl
[check144]: https://github.com/laadkke-arch/agentflow-open/blob/92833407f665a6e28e4292491c261b7e0725c69c/docs/workstreams/research/AF-RES-144/evidence/clean-replay.json
[domains144]: https://github.com/laadkke-arch/agentflow-open/blob/92833407f665a6e28e4292491c261b7e0725c69c/docs/workstreams/research/AF-RES-144/evidence/domains.md
