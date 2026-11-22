# PLAN 11 · 원문 링크가 설계 판단을 바꾸었다고 말할 수 있는 범위

만들고 있는 소프트웨어의 전체나 일부와 그 목적을 주면, 설계자가 참고할 완성품·부품·다른 분야의 원리를 찾아 원문 링크로 돌려주는 것이 이 연구의 목적이다. 이번에 가장 분명해진 사실은 **링크의 가치는 독자가 확인하려는 것에 따라 달라진다**는 점이다. 정정된 자료의 옛 수치를 찾을 때는 날짜가 붙은 발행 주소가 유용했다. 같은 프로젝트의 링크를 합치면 한 요구에서는 다른 구현이 보였고, 다른 요구에서는 꼭 필요한 설명이 사라졌다. 지정한 pandas 판에서는 잘못된 답을 실제 출력으로 가려냈다. 이 관측에서 설계자의 작업시간이나 재작업 절감량을 도출할 근거는 아직 없다. [제품 브리프][product] · [043 짝 비교][43pairs] · [044 요구별 차이][44changes] · [042 실행 원장][42probe]

**H1**은 요구와 근거 절을 연결한 링크가 후보 판단을 돕는다는 가설이다. **H2**는 추천한 이유를 남기고 다시 확인하면 오래된 판단을 바로잡을 수 있다는 가설이다. 필요할 때 새로 검색하는 방법(C0), 주소·판·용도를 보관하는 방법(C1), 발췌·판정 이력까지 보관하는 방법(C2)은 목적에 따라 조합할 수 있다. 아직 입력 형식, 검색 엔진, 저장 구조, 상시 수집 주기 중 확정한 것은 없다. [누적 검토 10][r10] · [운영 규칙][workflow]

## 검토 범위와 인수 상태

2026-11-22 UTC에 `work/planning@e7bf988`에서 최신 REVIEW-10을 먼저 읽었다. 그 검토의 진행표는 등록 38·DONE 36·BLOCKED 2였다. 이번 통합 브랜치 `1f722bf`에서는 **등록 42·DONE 40·BLOCKED 2**다. 새 DONE은 041~044뿐이다. 이전 36건의 과학적·기술적 판단은 REVIEW-10의 누적 기록을 이어받았다. 새 네 건은 해당 브랜치의 소유 경로에서 HANDOFF, RESULT, 자체 점검, 수용 원장과 판정·실행 자료를 읽었다. 진행표의 결과 SHA는 네 브랜치 끝과 각각 일치했다. 각 인계서가 지정한 본문 SHA에서도 RESULT와 수용 원장을 다시 읽어 브랜치 끝과 같은 내용임을 확인했다. 아래의 원장 재집계는 보관된 관측에 대한 검산이다. 당시 외부 원문 열람·소프트웨어 실행은 작업자가 저장한 기록에 근거한다. [REVIEW-10][r10] · [이번 진행표][control]

| 새 DONE | 인계가 있는 브랜치 끝 / 결과 본문 | 작업자가 직접 읽은 고유 원문 | 수용 원장을 다시 센 결과 |
| --- | --- | ---: | --- |
| 041 · 인쇄와 악보에서 가져온 원리 | [3a4ef6d][41h] / [d610d7b][41r] | 29저작 | 관측 조건 34/49. 정확한 원판·저자 연결 등 15개 미충족. 결과 고정 후 절차 4개는 별도 인계 기록이다. [수용 원장][41a] |
| 042 · pandas 두 판의 실제 동작 | [11c6812][42h] / [b0675fc][42r] | 31개 | 내용 조건 15/15. 날짜 18행·정수 25행을 최초와 빈 환경에서 관측했다. [수용 원장][42a] |
| 043 · 판 주소와 옛 인용문 | [3e0b143][43h] / [69060e2][43r] | 발행자 원문 하한 28개 | 31/40. 고유 총수는 충족했지만 지정 배당은 23/24. 실제 과거 사용판·표집 순서·중립성 등의 조건이 남았다. [수용 원장][43a] |
| 044 · 세 자리에서 대안이 보이는 조건 | [6c8c025][44h] / [176e2ee][44r] | 84개, 이 중 핵심 53개 | 27/33. 자연 원순서, 규칙 준수, 관측된 보기 수와 보강 양성 수 등 6개 미충족. [수용 원장][44a] |

중앙 진행표에는 DONE 40건 모두 `acceptance_evidence=[]`이고 이번 네 건의 `source_commit`과 `actual_model`도 비어 있다. 위 충족 수는 **각 작업의 고정 수용 파일**에서 왔다. 작업마다 조건·분모가 다르므로 합산 점수로 쓰지 않는다. 018은 세 번째 시도에서 대화 길이 한도, 035는 첫 시도에서 사이버 보안 위험 가능성 표시로 종료됐고 둘 다 공식 인계·결과 SHA가 없다. [등록·차단 기록][control]

## REVIEW-10까지 무엇이 쌓였는가

| 연구 축과 작업 | 근거가 있는 관측 | 아직 설계자가 전제로 삼기 어려운 주장 |
| --- | --- | --- |
| 작업 전달, 입력, 식별 · DOT-001·002, RES-001~004·016·020 | 전달과 복원 경로는 시험됐다. 합성 입력 6건에서 부정 조건이 빠졌고, 2문제·17질의에서는 동명 후보와 부품이 섞였다. 003·004는 같은 주소/대상/목적의 구분을 제안하고 합성 18행을 판독했다. 020은 주장 73개 중 72개의 전달을 확인했다. | 실제 사용자가 준 입력을 항상 보존한다는 근거는 없다. 016의 내부 판독 일치는 후보 형태 78.3%, 기여 70.8%였다. 020의 충돌 16개 중 완전 해소는 2개였다. [이전 근거][r10] |
| 탐색·부분 요구 · 009~014·025·029·033 | 비교 시스템 35개에 겹치는 기능이 있었다. 분야 단서를 준 010은 24원문에서 원리 7군을 식별했다. 011의 실제 61스레드·635답에서 부분 질문 33개 중 10개가 진전했다. 013의 역사적 선례 176개 중 웹 검색은 16개, 목록은 5개를 회수했다. 029의 부분 요구 인용 완결은 공통 검색·추가 웹 검색·제공자 내부 탐색으로 각각 2/12·4/12·3/12였다. | 011의 전이 답 14개에는 질문자 반응이 없었다. 012의 합성 질의에서 늘어난 근접 오답은 014의 485자료에서 재현되지 않았다. 025는 72칸 중 지지 2·충돌 14·보류 53·빈칸 3, 029의 전체 요구 완결은 모두 0/12였다. 033은 8설계×18후보의 엄격 지지가 넓은 기준 1/144, 당시판 0이었고 두 검색 모두 실제 상위 세 자리 완결 0/8이었다. [누적 검토][r10] · [실제 반환창][33win] |
| 뒤늦은 발견과 분야 간 인과 · 017·022·037 | 017은 40건 중 두 날짜를 연결한 사례가 18건이었다. 022의 결정 우선 24건에서 이미 알던 대안의 조건을 바로잡고 시행한 경우가 2건 있었다. 037은 같은 목적의 후속 명세·코드·시험을 결정 우선 7/8, 출처가 드러난 표본 3/4에서 확인했다. | 017은 당시 검색 가능성을 입증한 사건 0건. 022의 미인지→당시 가용→변경→시행은 주표본 0/24, 발견 진술 우선층 1/9, 노동 절감은 33건 모두 미확인. 037의 최초안 변경 인과는 0/8·0/4이고, GDAL 1건은 기준을 기존 코드로 옮기고 표준을 제공 분야로 인정한 감도에서만 성립했다. [누적 검토][r10] · [037 사건별 기준선][37j] |
| 근거 설명과 사람의 일 · 021·026·030·034·038 | 같은 후보에서 두 절만 연 021의 완결은 주소만 6/23, 절 목록 9/23, 요구와 절 연결 13/23이었다. 030의 같은 변수 질문에 직접 답한 수는 최초 표본 3/24, 질문을 보고 고른 보강 6/8이었다. 038은 pandas·NumPy 네 과제에 같은 링크를 통제한 과제지와 루브릭을 만들었다. B/C 11개 링크의 URL·판·순서가 같았고 첫 별도 AI 문맥의 요구별 채점은 35/36 일치했다. | 잘못 연결한 021은 8/23. 026에서 질문을 실제 전송한 횟수는 0이고 030에서 같은 답변자의 권고 변경과 요청자의 신규 시행까지 이어진 사례는 0/3·0/6이었다. 사람 연구 22군·26실험을 검토한 034에서 NCQ의 선택 시간은 380→57초, 전체 시간은 849→847초(중앙값)였다. 038의 사람 참가자는 0명이고 N08의 절대 최초 공개판은 미확인이다. [누적 검토][r10] · [034 사람 연구의 종점][34effects] · [038 측정 범위][38measure] |
| 추천의 붕괴와 재확인 비용 · 015·019·024·028 | 015의 500추천 중 현재 판정 가능한 195개에서 붕괴 14개, 과거 복원 83개에서는 후발 붕괴 5·최초 오류 4였다. 024의 64이유×16분기에서 유지 897·무효 95·최초 오류 16·보류 16이었다. 분기 20회 방문에서는 무효 이유 11개를 정기 확인이 모두, 신호 뒤 확인이 8개 찾았다. | 019의 사건/대조 7쌍에서 경보는 양쪽 3건씩이었다. 024의 10회 예산에서는 7/11 대 0/11, 40회에서는 모두 11/11이었다. 028의 실행 검증이 덮은 유지층은 32셀로 다른 865셀의 동작은 미확인이다. 모든 링크에 맞는 갱신 주기를 정할 근거는 없다. [누적 검토][r10] |
| 보관된 이력과 목적지 · 023·027·032·036·039 | 023에서 목적지를 고른 수는 18사건 중 주소·이유 3, 식별자·판·근거 추가 5, 변경 관계·시점 추가 15였다. 032의 실제 HTML 12참조는 모두 HTTP 200이었지만 교체가 필요한 것이 있었다. 같은 현재 내용을 준 036은 이력 유무 모두 유지 11·교체 1이었다. 039의 현재 판단도 양쪽 모두 유지 1·보류 11이었고 저장한 옛 발췌는 12/12 다시 표시됐다. | 023에 사후 정정이 섞였고 자동 복원은 0/18. 027·032에서 상류 시행과 소비자 배포를 엄격한 두 날짜로 연결한 수는 0/12·0/6이었다. 036의 29→17 GET은 목적지를 아는 모의값이다. 039 실측에서 현재·과거의 정확한 두 발췌를 함께 복원한 것은 C1 0/12·C2 1/12, 논리 요청 실패 88/94 중 80회는 CONNECT 단계였다. 발행처 소멸과 보관 손익분기는 미확인이다. [누적 검토][r10] · [039 짝 원장][39pairs] |
| 실제 동작과 링크 묶음 · 031·040 | 031은 알려진 추천 3개를 계약 입력 36개(양성 11·대조 21·경계 4)로 재생했다. 040은 8요구·48후보 칸에서 처음 입증된 필수조건 8개가 URL·상류·부품별 표시에서 8·6·8개 남는 것을 보였다. 상류별 표시에서 서로 보완하는 문서가 필요한 요구 2/8이 부분 근거를 잃었다. | 031은 기대 정정 6행, 대용량 종단 전달과 실제 프런트엔드 자동 전달은 미확인이었다. 040은 원풀 완전 대안 0/8이고 이름만 묻는 사례도 없었다. 부품별 표시가 완전 대안을 더 살리는지는 그 표본에서 판정할 수 없었다. [누적 검토][r10] · [040 손실 원장][40loss] |

## 새 결과에서 확인한 것과 약했던 지점

### 041 · 출처가 명시된 때와 설계가 바뀐 때

두 사건을 최초안과 기존 코드 두 기준으로 읽은 판정 4행을 대조했다. **저자의 포괄적 출처 명명과 같은 기능의 반영은 2/2, 정확한 원판·당대 가용·저자 연결·같은 선택 변경·같은 용도 반영을 모두 갖춘 인과는 최초안 0/2, 기존 코드 0/2**였다. 037과 겹치는 두 사례의 깊이를 높인 것이므로 사건 네 건을 새로 더한 것으로 셀 수 없다. [041 판정 원장][41j] · [037 원 판정][37j]

pdfTeX의 1996년 제안 p.248에 이미 자폭 축과 문단 줄바꿈을 결합하는 생각이 있다. 2000년 저자의 hz 영감 진술과 구현 세부를 몰랐다는 진술은 함께 성립한다. 번역판과 원저작의 관계는 좁혔지만 영어 원책자와 Zapf 원논문 본문, 처음 읽은 날짜, 그 전후의 같은 선택은 미확인이다. LilyPond 0.1.22→0.1.23에서는 flat의 본보기 주석이 Schubert에서 Müller로 바뀌고 같은 기호의 함수·매개변수도 달라졌다. 이 버전 차이만으로 어떤 악보의 어느 쪽을 읽고 수정했는지는 알 수 없다. 현재 견본·후대 저장 출력·재구성된 배포본의 범위, 당시 프로그램 재실행 0건을 카드에 보존해야 한다. 추천 가능한 것은 해당 조작을 비교할 원문과 적용 조건이다. [041 본문과 원전 위치][41r] · [반환 카드][41cards]

### 042 · 정답표가 실행 결과를 얼마나 구별하는가

CPython 3.10.6에서 pandas 1.4.4의 날짜 과제와 1.5.2의 정수 과제를 각각 최초 환경과 새 환경에서 실행했다. **typed 관측은 18+25=43행이고 두 번의 결과가 43/43 일치했다.** 원장에서 봉인한 예상 동작과 맞은 행은 43개이고, 요구 의미와 맞지 않은 의도적 오답은 그 안에 5개다. 구형 infer는 한 batch 안에서 12월 1일과 1월 13일을 섞었고, 고정 MDY는 둘째 입력의 월 13을 올바르게 거부했다. 정수 쪽은 기본 Series의 승격 2행, NumPy 대입과 명시적 int 변환의 1.5→1 절삭 2행이 차이를 드러냈다. 같은 값 2.0을 다시 넣는 시험에 3.0을 별도로 넣자 실제 변경 여부도 구분됐다. [실행 43행][42probe] · [042 본문][42r]

`expectedFailure`는 무관한 오류를 넣어도 계수됐다. 지정 입력·값·타입·오류 후 상태를 보며 판정해야 하는 이유다. 038의 해당 예시 6개·요구 셀 18개의 분류는 유지됐고, 오류 발생 위치와 실질적인 값 변경에 대한 평가자 주석 두 곳이 제안됐다. 선택한 환경의 재현은 성립했지만 원 저자의 OS·의존 잠금, 나머지 두 NumPy 과제의 실행, 독립 사람의 품질·작업시간·후속 재작업은 이 증거 밖에 있다. 042의 15/15를 H1의 노동 절감 검증으로 확대할 수 없다. [루브릭 대응][42rubric] · [환경·재현 범위와 인계][42h]

### 043 · 발행판 확인과 실제 사용판 확인

B는 기본 주소와 목적, L은 판/절로 가는 추가 주소, X는 저장한 옛 발췌다. 8참조×4구성×2과업의 판독 64행과 짝 64행을 층별로 다시 셌다. **정정 우선 4건**에서 과거 발행판 대조는 B·BL·BX·BLX 순서로 **2/4·4/4·2/4·4/4**, 현재 목적의 근거 있는 판정은 **3/4·4/4·2/4·3/4**였다. **자연층**은 현재 기준이 있는 세 건에서 모든 구성 3/3, 과거 실제 소비판 기준은 0/4여서 해당 판의 성공률을 계산할 수 없다. 연구자가 재구성한 판의 도달 0/3·2/3·0/3·2/3은 따로 읽어야 한다. [043 판독 원장][43j] · [사례 내 짝 비교][43pairs]

T01의 날짜 주소는 두 번 안에 당일의 1.6% 최초 발표로 데려갔다. T02는 기본 주소 자체가 이미 판을 가리켰다. J02에서 달라진 것에는 DOI 접근 실패와 직접 HTML 성공도 있다. X가 있는 과거 판독 14/14에서 발췌를 재표시했고 그중 6회는 저장 문구만 볼 수 있었다. X를 더해 발행판 대조가 늘어난 짝은 없었다. J01의 옛 수치는 원문과 일치하지만 현재 재사용에는 정정이 필요했다. X 때문에 잘못된 수치를 확언한 사건은 관측되지 않았다. [043 결과][43r] · [과업별 짝][43pairs]

추가 주소 8개 중 판·발표 주소는 5개, 직접 저작 주소는 2개, 이관 위치는 1개였다. 두 번째 방문 9건 중 원 HTML의 href 철자를 보존한 것은 2건이었다. 한 자연 카드에는 판독을 유도할 해설이 들어갔고 UCLA의 당대판·X, 일부 검색의 원순위, BMJ 발행자 소비 원문의 배당이 비었다. 이 자료로 주소의 일반 효과나 사람의 재방문 비용까지 추정하기는 어렵다. [기준·표집 감사][43audit] · [043 수용 조건][43a]

### 044 · 세 자리 합계가 같아도 사라지는 대안은 달랐다

자연층 8건에서 Pandoc 4건은 원응답 HTML 결측, Vega-Lite 4건의 관측 풀은 완전 대안 0개였다. Vega V3는 원요구의 명사 대신 `text`를 써서 원규칙 준수 여부까지 갖춘 자연 요구는 **3/8**이다. 결측 Pandoc의 나중 브라우저 DOM은 당시의 전송 바이트와 순서를 복원하지 못했다. 전체 보기 36개 중 실제 입력이 관측된 보기는 24개다. [원풀 판정][44gold] · [044 본문][44r]

보강 4건의 완전 대안 ID 수는 **2·11·1·0**이다. A(정확 URL)·B(상류)·C(부품/용도/판/역할을 포함한 키)는 모두 세 대표에서 직접 12/14, 대안별로 한 번의 두 클릭 경로가 존재한 수는 13/14였다. 그런데 C1에서 B는 가려졌던 Requests를 올려 직접 ID가 1→2, C2에서 B는 Matplotlib 직접 근거를 가려 11→10이지만 두 클릭으로 11을 회복했다. C3에서 B는 필요한 보완 절을 밀어내 두 클릭 완결 1→0이었다. 같은 PEP 전체까지 읽는 감도에서는 이 손실이 사라졌다. C1-B의 두 ID는 서로 다른 시행에서 확인됐고 한 시행의 최대는 1이었다. 따라서 13/14는 한 독자가 두 번 눌러 본 대안의 수가 아니다. [요구별 손익][44changes] · [시행별·보기별 재집계][44views]

원래 목표였던 별개 대안 복원 양성과 보완 문서 양성은 각각 1/2였다. C4는 원풀에서 두 조건을 함께 입증하지 못했다. 관측된 8풀 모두 C와 A의 분할이 같아서, 세밀한 키가 실제로 서로 다른 URL을 합쳤을 때의 장단점은 미확인이다. 1,927개 통제 시행과 84개 원문은 풍부한 도달 기록이지만 실제 사람이 고른 링크·채택·작업시간은 측정하지 않았다. [수용 조건 33개][44a] · [044 인계][44h]

## 불일치가 가리키는 다음 네 작업

| 아직 갈리는 판단 | 다음 작업이 가져올 판별 자료 | 결론을 낮춰야 하는 경우 |
| --- | --- | --- |
| 010·037·041은 저자가 언급한 외부 원리를 보여 줬으나 033은 실제 반환창에서 엄격한 새 원리를 입증하지 못했다. 역사적 영감, 검색 성공, 이미 제시한 원리의 설계 적합성은 다른 질문이다. | **045 · web-pro.** 새 요구 6건에서 제공 원리 두 개의 정상·경계 예측을 먼저 적고, 나중에 연 결정·시험에서 두 선택이 갈리는지 본다. | 두 원리가 같은 결과를 예측하거나 후속 시험이 다른 입력을 검사하면 해당 카드는 판별 근거가 약하다. |
| 034의 부분 과제 시간과 전체 시간은 달랐고 038·042는 채점 가능성을 높였다. 똑같은 요구를 맡은 사람이 링크 뒤 실제 코드를 고친 근거는 별도로 필요하다. | **046 · web-pro.** 공개 PR에서 링크 전 코드, 실제 작성자의 반응·후속 패치·시험, 직접 기록한 작업시간을 연결한다. 자연 8자리와 링크 우선 4자리를 나눈다. | 수정이 먼저였거나 CI·다른 리뷰가 원인이거나 실제 작업시간과 비교 조건이 없으면 해당 인과·절감은 미확인이다. |
| 039·043의 저장 발췌와 날짜 주소는 과거 문구 재표시·발행판 대조를 각각 도왔다. 자연 소비자가 어느 판을 실제 썼는지는 열려 있다. | **047 · web-pro.** 공개 분석 6건과 실행 기록 우선 2건에서 발행판, 작성자가 명시한 판, 특정 실행의 입력·필드를 한 사례 안에서 맞춘다. | 여러 판의 값이 같거나 입력을 가리키는 실행 기록이 없으면 사용판 증거가 부족하다. |
| 040·044는 상류 묶음의 방향이 요구에 따라 뒤집힘을 보였다. 044의 다섯 필드 키는 관측된 풀에서 정확 URL과 똑같이 동작했다. | **048 · codex-cloud.** 원문이 결측이거나 규칙을 벗어난 P1~P4·V3를 새 획득으로 기록하고, 표시 키가 같은 서로 다른 URL을 가진 문서 4자리를 따로 선정해 두 클릭을 재생한다. | C가 합칠 기회가 없거나 원 HTML을 얻지 못한 풀에서는 효과가 없다고 판정할 수 없다. 이득·손실은 같은 요구의 대안 ID로 검산한다. |

네 작업은 과거의 고정 입력만 읽는다. 045의 결과는 링크에 붙일 설명의 강도, 046은 사람의 실제 수정과 노동을 뒷받침하는 증거, 047은 사용판 이력에 필요한 최소 기록, 048은 링크를 묶어 표시할 조건을 판단하는 데 쓴다. 작업별 표본, 원문 배당, 필수 결과표, 중간 커밋과 인계 조건은 각각의 brief 안에 있다. [후속 작업 네 건](NEXT_TASKS-11.json)

[product]: https://github.com/laadkke-arch/agentflow-open/blob/1f722bfb7360ff9c8d221284d7b1b6484c6fa692/docs/product/RESEARCH_BRIEF.md
[43pairs]: https://github.com/laadkke-arch/agentflow-open/blob/69060e2d1c3cf7f4502abe508679386a95bfa34e/docs/workstreams/research/AF-RES-043/pairs.csv
[44changes]: https://github.com/laadkke-arch/agentflow-open/blob/176e2eee3c00257d7dcc64665c74b12bf4399913/docs/workstreams/research/AF-RES-044/changes.csv
[42probe]: https://github.com/laadkke-arch/agentflow-open/blob/b0675fce25d8889df12f34953c885e61bd1232c9/docs/workstreams/research/AF-RES-042/probe-results.csv
[r10]: https://github.com/laadkke-arch/agentflow-open/blob/e7bf988fadee4d98956b5bdf8294adc8b446ae82/docs/workstreams/planning/REVIEW-10.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/1f722bfb7360ff9c8d221284d7b1b6484c6fa692/docs/RESEARCH_WORKFLOW.md
[control]: https://github.com/laadkke-arch/agentflow-open/blob/1f722bfb7360ff9c8d221284d7b1b6484c6fa692/docs/automation/dot-control.json
[41h]: https://github.com/laadkke-arch/agentflow-open/blob/3a4ef6dd8e556d52e78153afd78a32398bd95b40/docs/workstreams/research/AF-RES-041/HANDOFF.md
[41r]: https://github.com/laadkke-arch/agentflow-open/blob/d610d7b16836c2cadff60edcd46cd394dc220ed6/docs/workstreams/research/AF-RES-041/RESULT.md
[41a]: https://github.com/laadkke-arch/agentflow-open/blob/d610d7b16836c2cadff60edcd46cd394dc220ed6/docs/workstreams/research/AF-RES-041/evidence/acceptance-evidence.json
[42h]: https://github.com/laadkke-arch/agentflow-open/blob/11c6812bac6a0399a4ad6ab495a84bcec97e666d/docs/workstreams/research/AF-RES-042/HANDOFF.md
[42r]: https://github.com/laadkke-arch/agentflow-open/blob/b0675fce25d8889df12f34953c885e61bd1232c9/docs/workstreams/research/AF-RES-042/RESULT.md
[42a]: https://github.com/laadkke-arch/agentflow-open/blob/b0675fce25d8889df12f34953c885e61bd1232c9/docs/workstreams/research/AF-RES-042/evidence/acceptance-evidence.json
[43h]: https://github.com/laadkke-arch/agentflow-open/blob/3e0b1433e95cf8fdd5a930db97afa3ae8e3ab1f3/docs/workstreams/research/AF-RES-043/HANDOFF.md
[43r]: https://github.com/laadkke-arch/agentflow-open/blob/69060e2d1c3cf7f4502abe508679386a95bfa34e/docs/workstreams/research/AF-RES-043/RESULT.md
[43a]: https://github.com/laadkke-arch/agentflow-open/blob/69060e2d1c3cf7f4502abe508679386a95bfa34e/docs/workstreams/research/AF-RES-043/evidence/acceptance-evidence.json
[44h]: https://github.com/laadkke-arch/agentflow-open/blob/6c8c025284215c7749921619cb09c89643886276/docs/workstreams/research/AF-RES-044/HANDOFF.md
[44r]: https://github.com/laadkke-arch/agentflow-open/blob/176e2eee3c00257d7dcc64665c74b12bf4399913/docs/workstreams/research/AF-RES-044/RESULT.md
[44a]: https://github.com/laadkke-arch/agentflow-open/blob/176e2eee3c00257d7dcc64665c74b12bf4399913/docs/workstreams/research/AF-RES-044/evidence/acceptance-evidence.json
[33win]: https://github.com/laadkke-arch/agentflow-open/blob/03ff2eb1264b85016266de1f36ddebe45f5fface/docs/workstreams/research/AF-RES-033/evidence/returned-window-audit.jsonl
[37j]: https://github.com/laadkke-arch/agentflow-open/blob/68c45d2fb4482850d6a3c29826c43a45ea1dc407/docs/workstreams/research/AF-RES-037/judgments.csv
[34effects]: https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/effects.csv
[38measure]: https://github.com/laadkke-arch/agentflow-open/blob/5a1699b24679cd7c58242cb98c40fa9fc9c6851a/docs/workstreams/research/AF-RES-038/measurement.md
[39pairs]: https://github.com/laadkke-arch/agentflow-open/blob/cf3e62ef72b4272824873f07de3d2fe952dfb2e6/docs/workstreams/research/AF-RES-039/pairs.csv
[40loss]: https://github.com/laadkke-arch/agentflow-open/blob/9bff55706d5b1a939e39185bda9cf6f22bea246b/docs/workstreams/research/AF-RES-040/losses.csv
[41j]: https://github.com/laadkke-arch/agentflow-open/blob/d610d7b16836c2cadff60edcd46cd394dc220ed6/docs/workstreams/research/AF-RES-041/judgments.csv
[41cards]: https://github.com/laadkke-arch/agentflow-open/blob/d610d7b16836c2cadff60edcd46cd394dc220ed6/docs/workstreams/research/AF-RES-041/cards.md
[42rubric]: https://github.com/laadkke-arch/agentflow-open/blob/b0675fce25d8889df12f34953c885e61bd1232c9/docs/workstreams/research/AF-RES-042/rubric-delta.csv
[43j]: https://github.com/laadkke-arch/agentflow-open/blob/69060e2d1c3cf7f4502abe508679386a95bfa34e/docs/workstreams/research/AF-RES-043/judgments.csv
[43audit]: https://github.com/laadkke-arch/agentflow-open/blob/69060e2d1c3cf7f4502abe508679386a95bfa34e/docs/workstreams/research/AF-RES-043/evidence/acceptance-audit-notes.md
[44gold]: https://github.com/laadkke-arch/agentflow-open/blob/176e2eee3c00257d7dcc64665c74b12bf4399913/docs/workstreams/research/AF-RES-044/evidence/pool-gold-summary.json
[44views]: https://github.com/laadkke-arch/agentflow-open/blob/176e2eee3c00257d7dcc64665c74b12bf4399913/docs/workstreams/research/AF-RES-044/evidence/results-data.json
