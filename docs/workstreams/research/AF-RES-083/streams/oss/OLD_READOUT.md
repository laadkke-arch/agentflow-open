# O02 옛 안내 모집·사전 제안

후속 본문을 열기 전 작성한 보조 판독이다. core 모집은 **0/3, 공석 3/3**이다. 이는 세 프로젝트에 관련 안내가 전혀 없다는 증명이 아니라, 지정 태그·범위·검색식에서 모집된 적격 원 안내가 없다는 뜻이다. 내부 코드에서 역방향으로 연결한 GAM 가이드를 사후에 본표로 승격하지 않는다.

| 저장소·옛 판 | 검색 범위 | 실제 발견 | core 처리 |
|---|---:|---|---|
| statsmodels v0.12.1 @539478470b53bd3e96473b411e1322bb158fd444 |237 파일|docs/examples 이름 검색0. 내부 get_covder2(simps), GEE.qic(trapz) 발견|공석 유지. GAM 안내→BSplines→UnivariateBSplines→get_covder2는 별도 보조 연결|
| Astropy v4.2 @01369fb9d230480220dd81813f3fff906f88d52d|263 파일|15행은 quad/dblquad, Trapezoid 모델·kernel 또는 저자 Simpson. 별도 BlackBody test에는 trapz|O02 대상 아닌 안내와 내부 시험을 구별|
| scikit-learn0.24.0 @45a817933ef51a24f0c5863c1026b4fe664b26fa|455 파일|PR평가 안내2곳의 trapezoidal AUC; backend는 numpy.trapz|SciPy integrate namespace가 아니므로 제외. 두 안내는 같은 PR 평가 계보로 접음|

## 무엇을 고칠 수 있고 무엇은 근거가 비는가

- **GAM 원 안내**는 사용자가 `BSplines`로 두 설명변수의 기저를 만들고 Gaussian/Poisson GAM을 fit하도록 한다. 자동 생성 API 색인이 아니라 실제 실행 예제다. 그러나 사전 검색식에는 나타나지 않았고, SciPy `simps` 자체를 권하거나 적분값을 약속한 문장은 없다. 내부의 `simps(d2[:,:,None]*d2[:,None,:], x, axis=0)`는 동작 의존성이므로 코드·지원판 정정의 후보가 된다. 원문에 없는 `simps` 철자를 안내에서 일괄 치환할 수는 없다. 실제 `df_autos` 예제를 같은 환경에서 실행하지 않았으며, 079의 simps는 소스 별칭 근거뿐이다.
- **GEE fit 안내**는 `qic`를 부르지 않는다. 같은 클래스 내부의 QIC 적분과 원 독자의 fit/summary 목적은 다른 행동이다. `trapz`가 발견되었다는 이유만으로 GEE 안내 전체에 수정 필요를 부여할 수 없다. QIC 내부는10,000개 격자의 회귀기반 qv를 계산하므로079의3점 입력과도 같지 않다.
- **BlackBody 시험**은100K,100,000파장점의 적분을 Stefan–Boltzmann 결과와1%허용오차로 비교한다. 가까운 원 가이드의10,000K/1,000파장점 곡선과 다르다. 본문과 시험을 연결해 보았지만 동일 예제라고 할 수 없다. 시험의 trapz→trapezoid 일괄변경은 보조 A안으로 봉인하고, B안은 SciPy>=1.1 지원범위·명칭 도입판을 나눈다.
- **Astropy integrate kernel 안내**는 실제 최고정밀도 조건을 갖지만 대상이 quad/dblquad다. **Trapezoid1D fitting 안내**는 도형 모형이지 수치적분 함수가 아니다. **sklearn AP/AUC 안내**는 두 평가 정의가 다름을 설명하며 numpy.trapz를 쓴다. 이 세 가지는 이름·namespace·수학적 목적만으로 같은 대상을 만들지 말아야 하는 음성 대조다.

## 설치판·출시판·읽기 수준

소비자 source tag와 의존 선언은 확인했다. Statsmodels는SciPy>=1.2, Astropy optional/all/docs는>=1.1, sklearn CPython은>=0.19.1이다. Astropy tox의oldestdeps는1.1.*이며 CircleCI의upgrade명령은고정판이없다. 이들은 **실제 설치판이나 실행 로그가 아니다**. 당시 HTTP 이동과 당시 generated HTML destination은 미확인이다. 현재 원문은 고정 GitHub source의 판·행·hash로 보존했다.

Astropy의 GitHub Release 목록은4.2 이전을 담지 않아 annotated tag metadata를 보완했다. old4.2의tag date는2020-11-25, 첫후속정식태그는2021-03-26의4.0.5로 다른 maintenance line이다. 이를4.2의후계내용이라고 가정하지 않는다. 각 태그의 선택근거와SHA는 versions.json에 있다.

## 자료 분모와 재현

sources.jsonl의17행은6개하류원저작계보로 묶었다. 설정·의존선언행은독립원저작최소량에가산하지않았다. guide/test/implementation의동일계보를여러건으로늘리지않았다. 이6계보는core6자리충족과별개다. 정오평가core분모는0이며0/0비율은산출불가다. 보조7레코드는 proposals.csv에사전제안이있어도core오류율의분모로바꾸지않는다.

검색목록은각*-old-scope.txt,규칙과실제hit는old-search.json,원행은frame.csv·records.jsonl에있다.후계명trapezoid/simpson/cumulative_trapezoid도회고검색에사용했다.초기rg호출은존재하지않는doc/docs경로도함께넘겨종료2였으나,최종검색은git ls-files기반존재하는파일목록을정확히읽었다.외부wiki와태그밖generated HTML은검색범위에서빠져있다.

원 source checkout은 .workbench에만 두었으며 게시물에는 원문URL·판·행·hash·판독을 남긴다. build_old_ledger.py는원checkout을읽어사전원장을재구성하는보조스크립트다.후속판을읽은뒤이사전원장을다시실행하여사전시각을바꾸지않는다.
