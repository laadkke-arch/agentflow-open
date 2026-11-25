# 반례 판정과 중지 규칙

## 판정 층을 분리한다
244의 고정 SCOPE L6: C는 새 질의 predict 레이블을 출력 또는 명확한 후속 연산으로 연결; 학습 y/확률/score만으로 대체하지 않는다. 이번 사전 SCOPE는 개별 레이블 소비·가시성의 엄격 기준을 유지한다. 모호성이 실제로 C9에서 나타났다. 소스에서 해당 estimator의 새 표본별 레이블 배열을 명시적으로 회수하여 후속 연산에 넘기는 조작(R), 공개 결과에서 개별 새 표본에 귀속되는 레이블 값을 보여 주는 엄격 완결(D), 합성 grid의 클래스 표면(V)을 따로 기록한다. R은 244의 "명확한 후속 연산"에 해당할 수 있으나, 집계만 공개된 경우 D가 아니다. 사전 H0(모두 조건부)는 D에서 유지, H1(꼬리에 직접 회수)은 R에서 지지, H2(G3 distance 추가)는 기각. 판정 기준을 바꾸어 baseline을 유리하게 재분류하지 않는다.

| 경쟁 판정 | 실제 반례와 위치 | 올바른 결과 |
|---|---|---|
| VotingClassifier의 final prediction을 KNN의 label이라 본다 | C3-T L47–69; I7 L421–477 soft voting argmax(weighted probabilities), decoder | ensemble 결과는 다른 receiver. 그러나 C3의 clf2 own panel은 별도로 존재. 전체를 ensemble-only로 기각하는 것도 오판. |
| predict라는 토큰과 test 변수를 발견하면 test row label이라고 본다 | C7-T L63–75, I1 L346–375: X_test의 min/max로 X_grid 생성, response_method predict; L387–416 label encode/reshape/display; I9 L201–214 | test set의 각 행을 예측한 것이 아님. disp.response, xx0, xx1에 좌표별 정수 class encoding은 있다. 합성 질의가 목적이면 V 적격, 첫 rank3(C3). C7은 저장된 display를 활용 가능하나 원문에 개별 배열을 꺼내는 줄 없음. |
| 실제 predict가 없으므로 KNN이 실행되지 않았다고 본다 | C5-T L69–82, C6-T L86–89; I2 L787–794,1195–1209; I8 L546–572 | score internally calls predict; pipeline final estimator가 KNN이면 귀속 가능. 그러나 내부 label array만으로 개별 소비를 충족했다고 주장할 수 없다. C5/C6는 실제 held-out score, C8 KNN은 전체 2-feature 데이터 fit; C8의 이후 분류 성능 수치는 다른 모델. |
| 명시 predict가 있는 C9의 confusion matrix를 KNN 결과로 본다 | C9-T L149–167,281–291 Ridge; L320–347 benchmark; L365–390 KNN k100 | Ridge confusion 두 개는 오탐. KNN benchmark의 pred는 X_test별로 회수되어 accuracy_score(y_test,pred)로 전달(I10 L227–241 비교 후 평균). R 직접 최초 rank9, D 조건부; 함수 반환은 description, score, time뿐. 공개 kNN accuracy .752, train .00104s/test .0726s(C9-H L1513–1525)로 개별 label을 복원할 수 없음. |
| distance라는 단어가 있으면 G의 distance mode라 본다 | G3-T L55–61,88–106; C4-T L39–40 KNeighborsTransformer distance, C7-T L62 weights=distance | Ward linkage는 거리 기반 군집이지만 kneighbors_graph call mode default connectivity(I4 L58–67,146–147). KNN weights / 다른 transformer는 다른 조작. G3 adds connectivity only; CSR shape 1500x1500, k10, self=False, I5 L1023–1048. |
| 아무 숫자도 공개하지 않는 그래프는 무조건 조건부 | G3 graph -> fit -> labels scatter, G1/G2 같은 pattern | connectivity subgoal direct: 명시 graph consumer. 둘 다 필요한 full goal은 조건부. I6 시험 소스는 양 mode의 정확 배열 소비를 한 번에 제공하지만 기존 author test 기대이며 이 turn 실행 관측은 아니다. |

## CPython 3.13.1, 순서 비교 아님
고정 tag commit 067145177975eadd61a0c907d0d177f7b6a5a3de (2024-12-03). P1 공식 RST L808–836은 recipes를 교육 및 후보 발굴 목적으로 설명한다. 이 문서의 배열 순서는 sklearn 원래 href 순위와 비교할 수 없다.

- grouper(P1 L950–964): 이름 등장보다 alias가 핵심. [iter(iterable)] * n은 같은 iterator를 n회 참조. fill 반환 zip_longest, strict 반환 zip(strict=True), ignore 반환 zip. caller가 list/next로 소비할 때 tuple이 관측된다. 동일 RST의 숨은 doctest L1561–1576: abcdefg, n3 fill x → abc,def,gxx; strict 두 tuple 후 세 번째 next에서 ValueError; ignore abc,def. 단순 호출자 이름 색인이 아니라 mode와 laziness/예외 시점까지 표시. P3 L4496–4565 구현은 활성 iterator가 남는 동안 fillvalue를 넣음. P4 L2878–2965 zip의 short/long strict 검사. P2 L1100–1125 zip_longest 기본 None 및 unequal length, P5 L1892–1909 strict mismatch와 부분 소비(다른 iterator의 next 값이 다름)를 저자 표준 시험으로 연결. recipe별 직접 doctest와 primitive test는 별개이며 실행되지 않음.
- roundrobin(P1 L966–973): map(iter, iterables) → cycle(islice(iterators,num_active)) → yield from map(next,iterators). cycle 출력 자체는 iterator 객체들의 순환; caller가 받는 것은 원소들. P1 L1609–1620 direct doctest 'abc','d','ef'→a,d,e,b,f,c, Counter equality(중복/누락 검사지만 순서 보장 자체는 아님), lazy prefix 'aeglmbfhnc' 후 입력에 'dijkopqr' 잔존. P2 L755–760 cycle의 유한 prefix/empty, L1476–1510 islice의 prefix 소비 및 잔존 검사; P3 L1288–1314,1796–1831 구현. 이름 등장만으로 cycle의 직접 반환을 받는다고 할 수 없고, 호출자를 위한 interleaving은 정확히 보인다. 본문에서 helper 사용법만 필요하면 레시피+doctest에서 멈추고, 내부 소비/예외 필요 시 primitive 구현·시험으로 이동한다.

## 선택지와 철회 조건
A. API-first: 동일 URL 내부의 exact Examples를 먼저 찾는다. N/C는 추가 URL 0, G는 partial. 목적이 배포된 현장 문맥이라면 단순 API만으로 부족하다.
B. budgeted sequential gallery: API 예제에 없고, 링크의 operation/receiver/return/mode 메타데이터가 없을 때만 next. 현재 N stop at 1; G stop on exhausted 3 (distance 미충족), C는 R이 필요하고 API 예제가 없다면 rank9까지 발견 가능. 깊이2 또는3 고정 컷은 C9 R을 놓치고, end 전수는 8개의 추가 페이지에 strict gain 0. 이 작은 목록을 전체 제품의 정밀도/효용으로 외삽 금지.
C. operation-aware re-ranking: source-backed label '직접 새 표본별 predict 배열 회수; 공개는 accuracy/time' (C9), 'KNN own grid + soft voter 별개' (C3), 'connectivity CSR to Ward only' (G3). 원순위는 보존하되 별도의 purpose-specific recommendation. source version/hash/receiver/argument/query scope/result chain/counterevidence 저장. dynamic aliases와 runtime route 불확실 시 unknown 처리; strict API contract와 observed example result를 혼합하면 철회.
D. test-backed supplementary answer: G3를 더 읽는 대신 I6를 1회 열면 두 mode fixture의 expected arrays 제공. 사용자가 실행 보증/현장 성능을 원하면 정확판 별도 실행 후 원 receipt가 필요하다. 테스트 기대를 관측으로 바꾸지 않는다.

## 제안 라벨
- C9: 1.6.1 · KNN k100 · held-out 문서별 pred 회수→정확도 · 공개는 0.752/시간, 개별 값 미공개.
- C7: 1.6.1 · k11 scaler pipeline · predict grid, uniform vs distance weight · test 범위/합성 좌표, row label 아님.
- G3: 1.6.1 · sample CSR 연결 k10/self 제외 · Ward 군집 · distance mode 없음.
- Python grouper: 3.13.1 · same iterator alias → tuple chunks · fill/strict/ignore + consumption-time exception. roundrobin: cycle/islice 내부 → caller element interleaving; lazy prefix test.
