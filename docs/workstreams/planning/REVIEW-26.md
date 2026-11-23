# REVIEW-26 · 이미 써 본 방법, 지금 열리는 예제, 다시 편집할 수 있는 부분

같은 도구를 이미 쓴 개발자에게도 같은 도구의 다른 절을 줄 이유가 있었다. Typst에서는 페이지 배경에 선을 한 번 긋는 대신 각 항목에 테두리를 적용하자 내용 12줄을 보존하면서 선이 하나에서 넷으로 늘었다. 반대로 같은 그림 파일을 가리키는 링크도 독자의 목적에 따라 갈렸다. ggplot2에서는 두 예제의 PNG가 바이트까지 같았지만 `coord_flip()`을 다시 쓰려는 독자가 찾아야 할 코드는 두 번째 블록에 있었다. 이번 증거로 확인할 수 있는 것은 **어떤 조작·절·출력이 목적을 충족하는가**까지다. 그 차이를 사용자가 처음 알았는지, 덕분에 재작업을 줄였는지는 여전히 열린 질문이다. [Typst 후보와 동작][a101] · [두 코드 블록 비교][r102] · [작성자 후속][f101]

## 검토 기준과 새 DONE

2026-11-23 UTC. `work/planning`의 최신 누적 검토는 `896cf10`의 REVIEW-25였다. 그 검토가 사용한 진행표 `ace1a06`과 이번 통합판 `49f603a`의 tasks를 ID로 맞췄다. 등록은 **98→102**, DONE은 **96→100**, BLOCKED는 **2→2**다. 기존 98개 항목은 모든 필드가 같았고 새 DONE은 AF-RES-101~104다. AF-RES-018(범용 LLM 웹 검색과 동예산 비교)과 035(Go 추출·DLPack 호출 경계)는 계속 BLOCKED다. 이번 DONE 100행의 중앙 `acceptance_evidence`는 모두 빈 배열이다. 이전 결과의 판단은 REVIEW-25에서 계승했고, 새 네 작업은 각 소유 경로의 인계·결과와 원장까지 열었다. [직전 누적 검토][prev] · [전회 진행표][old] · [이번 진행표][reg]

| 작업 · 담당 | 중앙 등록 커밋과 브랜치 끝의 HANDOFF | 실제 검사 대상의 RESULT | 이번에 대조한 관측 단위 |
| --- | --- | --- | --- |
| 101 · web-pro | [b29c25f][h101] | [392ff3d][r101] | 후보 24자리와 요청 8건의 후속에서 실제 반환, 기존 사용과의 차이, 인지·실행을 구분했다. |
| 102 · web-pro | [c1c0c86][h102] | [092f4c5][r102] | 예제 12쌍 자리와 판 24자리에서 결원·수록·사용·생성을 대조했다. 검사 뒤 [8552d73][check102]에 영수증을 저장했다. |
| 103 · codex-cloud | [09503ac][h103] | [41f5fbb][r103] | 주 실행 30개, 보조 14개, 반복 15쌍을 구별하고 출력마다 약속한 속성을 확인했다. |
| 104 · codex-cloud | [ce82834][h104] | [f38c0af][r104] | 두 축 각각 16대응쌍의 결측과 전용 완결을 세고, 같은 질문이 몇 번 들어갔는지 대조했다. |

네 원격 끝은 모두 중앙 등록 인계와 일치했다. 검토자가 101 후보 CSV의 양쪽 제외·반환 위치, 102 예측·판별 CSV의 실제·결원, 103 실행 종류와 성공·실패, 104 대응 CSV의 축별 결과를 다시 집계했다. 각 인계에는 명시한 manifest 검사의 종료값 0과 공통 검사의 자동 세션 수 0이 함께 남아 있다. 중앙의 `last_progress_at`은 21:49~21:50 UTC, 실제 인계 커밋은 22:27~22:50 UTC여서 두 시각을 구별했다. 도구 실행·화면·당시 작성자 행동은 아래에 인용한 연구 영수증이나 공개 기록에 귀속된다. [101 후보][c101] · [102 판별][l102] · [103 실행][run103] · [104 대응][p104] · [중앙 기록][reg]

## 설계자가 이어받을 누적 판단

제품의 입력은 만들고 있는 소프트웨어의 전체 또는 일부 구조와 그 목적이다. 반환 후보에는 완성품 외에도 한 기능, 재사용할 부품, 다른 분야에서 빌려올 원리가 들어간다. 아래는 나중에 채택·교체·조합할 판단 단위다. 필수 입력 JSON이나 저장 필드, 검색 엔진, 크롤링 주기, UI는 설계자가 비교할 선택지로 남아 있다. [제품 연구 브리프][goal] · [연구·정리 규칙][rules]

| 설계 질문 | 100까지 남은 근거 | 101~104를 반영한 판단 |
| --- | --- | --- |
| 부분 요청에 무엇을 더 물을까 | 020은 주장 72/73을 전달했지만 충돌 해소는 2/16이었다. 070 자연 요청에는 되물은 답 때문에 정오가 바뀌었다고 셀 독립 분모가 없었다. 074의 구성 대조는 조건 하나로 8/8이 좁혀졌고 093-P2의 RGBA 요구는 이미 최초 본문에 있었다. [이전 근거][prev] | 101의 TY-A2 작성자는 이미 색상 helper를 알았다. 같은 수식에서도 바인딩이나 인수 표기가 달라지면 결과가 달라졌다. 기존 시도의 정확한 입력·적용 단계를 먼저 활용할 수 있다. 전체 후보의 사전 인지는 18개 모두 미확인이다. [후속][f101] · [분모][n101] |
| 다른 분야 선례가 어떤 선택을 가를까 | 010은 분야 단서로 원리군 7개를 얻었다. 033의 무단서 144쌍은 넓은 지지 1, 당시판 지지 0이었다. 069·073은 접수와 실제 적용, 이전과 유지 책임을 갈랐다. 077 보조 세 건에서 핵심 구현 변경은 0이었다. 089에서는 같은 두 음에 편집 표시가 달라졌고 091에서는 위치 보존만으로 원 Point 행 선택을 복구하지 못했다. [이전 근거][prev] | 103의 SVG에서는 같은 그림의 색이 삽입 방식에 따라, DOT에서는 간선의 촉이 정의 위치에 따라 달라졌다. 이런 선례는 실패 시험을 제안할 근거다. 원 개발자가 그 선례를 보아 선택을 바꿨는지는 미확인이다. [교차 분야 원 시험·대조][r103] |
| 같은 기능·주소를 언제 병합할까 | 032는 배포 참조 12개에서 유지 9·교체 2·보류 1이었다. 055는 옛 답 4/4를 복원했지만 다음 판 답은 0/4였다. 071·075는 조건·양성의 존재를 22/22·15/15 복원해도 1위 판정은 양쪽 16/16 유보했다. 097의 Pillow 원 입력 두 건·세 판에서는 두 호출 모두 맞은 경우와 한 호출만 맞은 경우가 각각 3/6이었고 검정 픽셀 199개의 투명도가 갈렸다. [이전 근거][prev] | 도구 이름을 기준으로 빼면 101의 유효한 다른 조작 셋도 빠진다. 반대로 조작을 구분해 더 보여 준 일곱 개에는 셸·래퍼 오류가 있는 제안도 있다. 102의 수평 상자그림은 저장된 PNG와 구체적 작성 방법을 다른 단위로 묶어야 하는 예다. [후보][c101] · [구체적 방법과 반환 절][r102] |
| 어느 판과 어느 절을 보존할까 | 086은 당시 제공 주 관측창을 확인한 경우가 0/9였고 090의 후속 자원 엄격 충족은 0/8이었다. 094에서는 새 트리에 남은 옛 SVG 두 개가 해당 절에서 빠졌다. 098에서는 옛 정적 그림을 현재 절이 계속 썼고 두 판 12자리 모두 당시 빌드의 신규 생성은 미확인이었다. [이전 근거][prev] | 102에서는 확인한 16판 자리 모두 수록·본문 사용이 맞았지만 그 빌드에서 생성됐다는 증거는 없었다. HBox 예제에서는 목적이 유지된 뒤 제목 앵커만 깨졌다. 독자에게 줄 새 위치, 역사 인용 주소, 생성 귀속은 각각 검증할 수 있다. [판별 원장][l102] · [반환 절][ret102] |
| 주 도구 옆의 부품이나 두 번째 링크가 필요한가 | 076의 자연 요구 6×20후보에서 직접 양성 0, 080 범위 확장의 비교 가능 양성 전환은 자연 1/5·교정 3/5였다. 078은 각각 성공한 두 기능도 연결하면 실패함을 보였다. 088의 비교 가능 26쌍에는 수정 전후 변화가 없었다. 092는 순위 안 인접 원문 노출 0, 096은 경계 6/6에 노출돼도 단독 완결 0/6, 전체 8쌍은 양쪽 완결 5·미완결 3이었다. 100 전체 파일 7쌍에서 인접만 완결 1은 기존 helper 교체를 허용해야 했고, 첫 발췌에서는 양쪽 미완결 7이었다. [이전 근거][prev] | 104에서는 같은 파일과 같은 실제 문자 예산에서도 구간 선택이 J1의 진단 근거를 살렸다. 도구 파일 정책 A/B만 바꾼 비교 가능 14쌍에는 한쪽만 완결된 경우가 없었다. 어디서 찾았는지, 어떤 조건을 보였는지, 실제 조합이 실행됐는지를 따로 세야 한다. [대응표][p104] |
| 설명을 얼마나 주고 무엇을 비용으로 셀까 | 021의 두 절 열람에서 공식 근거 회수는 주소만 6/23, 절 목록 9/23, 조건에 맞춘 절 14/23, 잘못 맞춘 절 8/23이었다. 066에서는 반대 권고에 같은 링크가 붙었다. 022의 미인지→결정 변경→실행 확인은 0/24, 034의 부분 시간은 380→57초였으나 전체는 849→847초였다. 093은 4,268→7,449바이트, 094는 엄격한 목적 충족 4/24였고 12대응쌍에서 양쪽 두 번째 주소가 실제 달랐던 쌍은 0이었다. [이전 근거][prev] | 104의 발췌는 같은 74,400자여도 시험과 예외를 다르게 남겼고 101은 실제 배움의 분모를 구하지 못했다. 표시한 문자, 준비 계산, 독자 시간, 설계 재작업은 각각 관측해야 한다. [104 비용과 예외][n104] · [101 작성자 근거][f101] |
| 재사용할 부분이 주변에 미치는 영향은 무엇인가 | 095에서는 PDF 12/12·셀값 144/144가 나왔는데도 두 표에 같은 매크로를 적용한 4/4에서 뒤 표의 선이 사라졌다. 096-P4의 준비 실패 뒤 099는 한 원 TeX에서 그림·검색 가능한 본문·외부 파일을 구별했고 전역 색 정의가 별도 컴파일을 깨뜨리는 반례를 냈다. [이전 근거][prev] | 103에서는 위치별 정의를 전달하면 두 그림을 맞출 수 있었지만, 닫힌 그룹을 다음 그림까지 넘기면 올바른 HTML 안에 잘못된 색이 남았다. 자연 문서 T2는 27개 투영을 표시했다. 한 투영만 편집하면서 나머지를 보존하는 방법은 아직 시험하지 않았다. [원소별 판독과 대조][el103] |

## 네 작업에서 확인한 근거와 결론이 달라지는 조건

### 101 · 더 많이 반환한 일곱 후보 중 다른 유효 조작은 두 요청의 세 후보였다

ImageMagick 60건과 Typst 27건의 모집틀에서 최초 요청 8건을 선정하고, 각 요청의 첫 세 후보 자리와 두 자리 반환 한도를 고정했다. 24자리 중 실재 18·결원 6이다. 사용한 제품이 같으면 빼는 A는 실재 9개를 제외하고 7개를 반환했다. 기존 호출과 같다는 증거가 있어야 빼는 B는 제외 0개·반환 14개였다. 살아남았어도 순위 밖인 후보는 양쪽 모두 반환으로 세지 않았다. 연구판에서 목적을 지지하고 실제 시도와도 다른 후보는 TY-A1-C2와 TY-A2-C1/C2뿐이었다. A가 셋을 모두 제외했고 B는 모두 반환했다. 짧은 예문에 빠진 위첨자까지 그대로 요구하면 분모는 2다. [후보별 원순서와 반환][c101] · [분모·민감도][n101]

B에만 남은 나머지 네 후보에는 래퍼 API와 셸 구문·인자에 관한 반대 근거가 있다. Typst에서도 괄호 없는 `#pagebreak`는 종료값 0이면서 함수 이름이 찍힌 한 페이지를 만들었다. 작성자가 수정한 IM-A1-C1의 실패는 질문 수정과 댓글에 남은 **한 사건**이다. 실재 18개 모두 제안 전체를 미리 알았는지, 새로 배웠는지, 원판·원입력으로 그대로 실행했는지는 미확인이다. 35개 고유 1차 자료와 합성 실행은 어떤 제안이 구체적으로 다르고 어디서 실패하는지를 지지한다. 재추천 제거율이나 이용자의 학습률에는 독립 분모가 없다. [실행과 반례][r101] · [작성자 시점별 기록][f101]

### 102 · 여덟 번 맞은 경로 규칙이 다루지 못한 두 가지 오류

ggplot2 3.4.0→3.5.0과 Matplotlib 3.6.3→3.7.0의 이전 판에서 프로젝트별 첫 적격 40개를 모집했다. 각 프로젝트의 일반층 2쌍과 경로 유지·소스 변경층 2쌍이 채워졌다. 옛 파일 경로가 사라진 층은 각 2쌍씩 결원이었다. 실제 8쌍의 경로 예측은 전부 ‘새 절에서 사용’이었고 모두 맞았다. 16판 자리 모두 파일 수록과 정확한 절의 사용은 확인, 실제 역사적 빌드의 신규 생성은 미확인이다. 채워진 네 프로젝트·층의 거짓음성은 각각 0/2였지만 실제 음성은 0개라 거짓양성률·특이도는 산출할 수 없다. 첫 40 안의 추가 20개씩을 봤어도 경로가 남고 절이 버린 사례, 경로가 사라지고 후계가 살아난 사례의 주 표본은 늘지 않았다. [사전 예측][p102] · [실제 판별][l102] · [층별 분모][n102]

주 8쌍의 PNG는 모두 바이트가 달라도 원래 설명 목적이 유지됐다. MP-C1의 같은 높이 HBox는 새 절에도 있었으나 옛 `#hboxdivider-demo`는 새 DOM에 없었다. 보조 ggplot2의 같은 PNG 두 개는 x/y 매핑 교환과 `coord_flip()`이라는 다른 코드를 가리켰다. 조사 시점에 제공된 Matplotlib HTML 네 개는 최초 발행본과 바이트가 모두 달랐지만 해당 절의 텍스트·그림 속성은 4/4, 1x·2x PNG는 8/8 일치했다. ggplot2의 실행 기록 조회 14건과 Matplotlib의 22건은 모두 HTTP 200에 보이는 실행 0이었다. 확인한 고유 자료 111개 중 어느 것도 선택한 바이트와 당시 생성 실행을 이어 주지 못했다. 지금 줄 절을 고르는 데는 이런 빌드 귀속이 없어도 되는 경우가 있다. [목적별 반환][ret102] · [발행·실행 조회와 반례][r102]

### 103 · 페이지를 볼 수 있다는 보증과 조각을 편집할 수 있다는 보증

다섯 입력에서 세 경로를 두 번씩 실행했다. K는 고립된 그림 조각, M은 사람이 위치별로 고른 선언과 조각, P는 전체 문서의 페이지를 SVG 이미지로 넣은 HTML이다. 각 경로가 약속한 출력의 충족은 K 2/10, M 8/10, P 10/10이다. 30자리 20성공·10실패에서 ‘성공’의 정의는 경로에 따라 다르다. K/M의 성공 HTML 10개는 호스트 본문을 검색할 수 있었다. P는 문장이 있던 8자리 모두 선택이 안 됐고 자연 T2에서 따로 검사한 제목도 0/8이었다. P의 외관 성공률을 편집 또는 접근성의 순위로 쓸 수 없다. [실행 원장][run103] · [브라우저·페이지·DOM][el103]

T2는 독립적인 공개 원본 한 건으로 같은 틀에서 27개 투영을 14쪽에 만든다. P 두 번에서 모두 표시됐다. K는 첫 그림의 `axis`가 미정의라 실패했고 M은 반복·매개변수 처리 범위를 벗어나 자식 컴파일 전에 멈췄다. 구성 T3·T4에서는 재정의 순서나 그룹 범위를 틀리게 전달해도 종료값 0에 둘째 그림만 틀린 색이 남았다. 의미상 반복은 15/15쌍, 산출물이 생긴 10쌍의 HTML·SVG 바이트 일치는 10/10, PDF는 0/10이다. 연구자가 고른 선언의 효과를 자동 추출 능력으로 일반화하기 어렵고 자연 문서 수는 하나다. 원 TeX의 PITCH 반복은 고도 0을 처음과 끝에 넣는다. 12번째와 21번째 투영은 둘 다 (−30, 0)이므로 각도만으로는 편집할 한 곳을 고를 수 없다. 두 곳 중 하나만 바꿨을 때의 실제 출력과 스크린 리더 경험은 미확인이다. [원 반복문][tex103] [자연 원본과 단위][i103] · [대조·반복][n103] · [103 인계][h103]

### 104 · 같은 분량에서도 새 시험은 들어오고 원래의 예외는 빠졌다

100의 jq·Pandoc 요청 8건, 파일 정책 A/B와 공석을 고정했다. W1은 첫 일치 한 구간, W2는 두 질의의 토큰을 고르게 담는 두 구간이다. 각각 64파일 자리, 원문 코드포인트 74,400자, 추가 이동 0이었다. W1은 100의 짧은 발췌 실재 62자리 모두를 재현했다. W1/W2 16쌍 중 P3-B 공석으로 1쌍을 제외해 W2만 완결 2·양쪽 미완결 13이다. A/B 비교는 14쌍에서 양쪽 완결 1·미완결 13, 2쌍 비교 불가다. 회복된 2/9자리는 **동일 J1의 A·B**다. 중간 값을 관측하는 진단이 목표면 지지되고 최종 JOIN 성공까지 요구하면 W2 전용은 0/15가 된다. 독립된 두 질문의 발견으로 세기 어렵다. [대응쌍][p104] · [민감도와 비용][n104]

예전 전체 파일 인용 81개를 통째로 담은 것은 W1 7, W2 0이었다. W2는 더 좁은 구현과 새 시험으로 J1을 지지했다. 한편 사후에 식별한 제약 중 전체 파일에 보였던 12자리에서 W1은 6, W2는 11을 잃었다. W1에만 남은 제약 6자리와 W2에만 보인 상류 시험 3자리가 있었다. 같은 S 구간을 다시 읽어도 조건 등급은 16/30이 바뀌었고 완결 여부는 0/16이 바뀌었다. 단일 판독자는 같은 질문의 다른 경로를 함께 봤고 24/32자리에서 다른 질문과 파일 노출이 겹쳤다. 46개 고유 1차 자료 중 새로운 주 질문 표본은 0이었다. 이 결과는 발췌의 위치와 목적 판정에 관한 것이며 독립 독자의 성능이나 원 작성자의 실행·절약 시간은 미확인이다. [가시 제약·시험 원장][v104] · [노출 원장][e104] · [원 판독과 재판독][r104]

## 다음 작업과 인수 경계

| 작업 · 담당 | 지금 풀 질문 | 완료된 입력 | 판단을 바꿀 관측 |
| --- | --- | --- | --- |
| AF-RES-105 · web-pro | 익숙한 도구의 한 단계가 실제로 새 정보였는가 | [101][h101] | Blender·QGIS 새 요청에서 작성자의 사전 지식, 실제로 받은 제안, 이후 변경·거절을 같은 조작에 연결한다. ‘이미 안다’와 ‘처음 알았다’를 찾은 별도 표본은 시간순 표본과 따로 센다. |
| AF-RES-106 · web-pro | 옛 예제 주소의 소실·잔류를 보았을 때 어느 절로 보낼까 | [102][h102] | 두 발행판의 첫 40 밖에서 실제 제거·이동 신호와 일반 대조를 등록하고, 경로와 후계 목적이 어긋나는 두 방향을 정확한 절·소스·그림에서 판독한다. |
| AF-RES-107 · codex-cloud | 같은 정의를 쓴 그림 중 하나만, 또는 전부 고치려면 어느 소스 위치가 필요한가 | [103][h103] | PGFPlots·SVG·DOT의 공유 정의와 개별 사용 위치를 직접 바꿔 목표 요소와 나머지 요소의 보존을 24번의 실행 자리에서 확인한다. |
| AF-RES-108 · codex-cloud | 제한된 발췌에 예외 조건을 남기면 오답과 보류가 어떻게 달라지는가 | [104][h104] | 새 SQLite·CSS Flexbox 시험 8쌍에서 두 방식에 같은 문자를 주고 정상·경계 입력의 사전 답을 실제 값·치수와 대조한다. |

105는 작성자의 지식과 행동, 106은 발행판 사이에서 살아남은 설명, 107은 편집 가능한 소스 위치, 108은 짧은 설명에서 정확한 판정을 내릴 조건을 맡는다. 네 작업 모두 인계된 입력 하나에서 시작해 서로 다른 경로에서 끝낼 수 있다. 역사적 빌드의 파일별 생성, 화면 보조기술 사용자의 경험, 사람의 전체 작업시간 절감은 별도의 증거가 필요한 질문으로 남긴다. [작업별 모집 규칙·필수 표·인계 조건][next]

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/896cf100277c7da197f7a74cae7c70ec75a3a0b9/docs/workstreams/planning/REVIEW-25.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/ace1a06a13ea435f5cb6a3e340ad24f03f68ecae/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/49f603a98188fbf2009c4c490b0539f32d124e38/docs/automation/dot-control.json
[goal]: https://github.com/laadkke-arch/agentflow-open/blob/49f603a98188fbf2009c4c490b0539f32d124e38/docs/product/RESEARCH_BRIEF.md
[rules]: https://github.com/laadkke-arch/agentflow-open/blob/49f603a98188fbf2009c4c490b0539f32d124e38/docs/RESEARCH_WORKFLOW.md
[next]: NEXT_TASKS-26.json
[h101]: https://github.com/laadkke-arch/agentflow-open/blob/b29c25fe6d7375dc28c4c700da2240c1a205093d/docs/workstreams/research/AF-RES-101/HANDOFF.md
[r101]: https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/RESULT.md
[h102]: https://github.com/laadkke-arch/agentflow-open/blob/c1c0c863e1c349895533d5c66ac63ba6b4fc6176/docs/workstreams/research/AF-RES-102/HANDOFF.md
[r102]: https://github.com/laadkke-arch/agentflow-open/blob/092f4c5c56451bceb53e632f4bddf33db6cda168/docs/workstreams/research/AF-RES-102/RESULT.md
[h103]: https://github.com/laadkke-arch/agentflow-open/blob/09503ac5452bbfb329aa0d5ff4bad9499924f277/docs/workstreams/research/AF-RES-103/HANDOFF.md
[r103]: https://github.com/laadkke-arch/agentflow-open/blob/41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd/docs/workstreams/research/AF-RES-103/RESULT.md
[h104]: https://github.com/laadkke-arch/agentflow-open/blob/ce8283488ab46a76f2d5fa081db5c4734f302526/docs/workstreams/research/AF-RES-104/HANDOFF.md
[r104]: https://github.com/laadkke-arch/agentflow-open/blob/f38c0af427c66876bf411bfd0a728cfcd60013eb/docs/workstreams/research/AF-RES-104/RESULT.md
[c101]: https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/candidates.csv
[f101]: https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/followup.csv
[n101]: https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/evidence/reconciliation.json
[a101]: https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/evidence/assessment.json
[p102]: https://github.com/laadkke-arch/agentflow-open/blob/092f4c5c56451bceb53e632f4bddf33db6cda168/docs/workstreams/research/AF-RES-102/predictions.csv
[l102]: https://github.com/laadkke-arch/agentflow-open/blob/092f4c5c56451bceb53e632f4bddf33db6cda168/docs/workstreams/research/AF-RES-102/lineage.csv
[n102]: https://github.com/laadkke-arch/agentflow-open/blob/092f4c5c56451bceb53e632f4bddf33db6cda168/docs/workstreams/research/AF-RES-102/counts.json
[ret102]: https://github.com/laadkke-arch/agentflow-open/blob/092f4c5c56451bceb53e632f4bddf33db6cda168/docs/workstreams/research/AF-RES-102/evidence/returns.json
[i103]: https://github.com/laadkke-arch/agentflow-open/blob/41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd/docs/workstreams/research/AF-RES-103/inputs.json
[run103]: https://github.com/laadkke-arch/agentflow-open/blob/41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd/docs/workstreams/research/AF-RES-103/runs.jsonl
[el103]: https://github.com/laadkke-arch/agentflow-open/blob/41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd/docs/workstreams/research/AF-RES-103/evidence/ELEMENTS.md
[n103]: https://github.com/laadkke-arch/agentflow-open/blob/41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd/docs/workstreams/research/AF-RES-103/evidence/verification.json
[p104]: https://github.com/laadkke-arch/agentflow-open/blob/f38c0af427c66876bf411bfd0a728cfcd60013eb/docs/workstreams/research/AF-RES-104/pairs.csv
[n104]: https://github.com/laadkke-arch/agentflow-open/blob/f38c0af427c66876bf411bfd0a728cfcd60013eb/docs/workstreams/research/AF-RES-104/metrics.json
[v104]: https://github.com/laadkke-arch/agentflow-open/blob/f38c0af427c66876bf411bfd0a728cfcd60013eb/docs/workstreams/research/AF-RES-104/evidence/feature-visibility.jsonl
[e104]: https://github.com/laadkke-arch/agentflow-open/blob/f38c0af427c66876bf411bfd0a728cfcd60013eb/docs/workstreams/research/AF-RES-104/evidence/exposure.json
[check102]: https://github.com/laadkke-arch/agentflow-open/blob/8552d736cb8fb1d1ca7a5de9206a0165dac20602/docs/workstreams/research/AF-RES-102/VALIDATION.md
[tex103]: https://github.com/laadkke-arch/agentflow-open/blob/41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd/docs/workstreams/research/AF-RES-103/evidence/inputs/T2.tex#L45-L49
