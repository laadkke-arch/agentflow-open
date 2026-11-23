# AF-RES-061 반환 카드 — 원리와 구현의 경계를 함께 반환

이 카드는 구현을 선택하거나 원문을 더 읽을 설계자에게 주는 조건부 반환안이다. 실제 사용자에게 보여 주어 선택 변화·읽기 시간·만족을 측정한 결과가 아니다. 네 구현과 판은 [frame.csv](frame.csv), 차용은 [transfer.csv](transfer.csv), 수치와 실행 주체는 [observations.csv](observations.csv)를 따른다. `미확인`을 이미 작동한 기능으로 읽지 않는다.

## D3 · d3-force 3.0.0 many-body

**첫 링크 — [고정 Many-Body API: strength·theta·거리 제한](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/README.md#many-body)**

노드 사이에 전역 인력/척력을 추가하려는 경우 이 절부터 읽는다. 예를 들어 동일한 두 점이 distanceMax 안에서는 멀어지고 밖에서는 영향받지 않아야 한다면 API가 이미 선택을 가른다. 화면 필터가 목적이라면 [#166](https://github.com/d3/d3-force/issues/166)의 opacity 경로처럼 표시 로직을 먼저 확인한다. [G011/G044/G047](sources.jsonl).

**옮길 원리:** 멀리 있는 다수 점을 공간 셀로 집계하여 계산량을 줄이는 방식. 이름과 중간 링크를 통한 Barnes–Hut 귀속은 명시되어 있지만, 개발자가 특정1986 원논문을 읽고 채택한 사건은 미확인이다. 원1986본문 접근 결손 때문에 조사 B창은 [Demmel의 해당 강의 절](https://people.eecs.berkeley.edu/~demmel/cs267/lecture26/lecture26.html)을 썼다. 이를 직접 채택 기록으로 바꾸지 않는다.

**옮길 조건:** 실제 strength 부호·분포, 근사 허용량, 단위가 있는 좌표/속도, direct force와 simulation tick의 차이를 명시한다. [apply](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/src/manyBody.js#L55-L91)의 Δ/r² kernel과 alpha·distanceMin/Max를 함께 확인한다. 중력의 Δ/r³을 그대로 쓰지 않는다.

**중단 조건:** 정확한 점별 울타리, 부호 상쇄에도 정확한 pairwise 합, 동일 위치의 대칭 운동량 보존을 보장해야 한다면 이 원리 이름만으로 추천을 확정하지 않는다. 주 보조 실행의 cutoff 정상 결과는 모든 집계 경계의 보장이 아니다. [#186](https://github.com/d3/d3-force/issues/186)과 [혼합부호·거리 raw 반례](streams/graph/d3-run.json)는 pruning 비용과 점별 요구가 충돌함을 보여준다.

| 관점·우선순위 | 먼저 확인할 것 | 첫 링크를 바꿀 최소 추가 자료 |
| --- | --- | --- |
| 천체 근사 원전 저자 / 오차·보존량 | 힘 kernel, 양의 질량과 signed strength의 차이, 개방 규칙과 오차 꼬리 | 실제 노드분포와 절대/상대 오차 budget가 제시되면 [Salmon/Warren](https://lss.fnal.gov/archive/other/ccsf-28-92.pdf) 같은 원 오차 연구를 앞에 두고 수신 mapping을 필수로 덧붙임 |
| 유지보수자 / API·비용 | 0합 셀 pruning, theta와 cutoff가 상호작용하는 입력 | 정확한 판·seed·strength·최소 재현이 있으면 apply와 관련 issue 우선 |
| UI 개발자 / 선택 가능한 화면 | filter인가, separation인가, 지속 motion인가; 다른 force와 tick | 실제 그래프·화면 목표가 오면 해당 표시 예제 또는 force 조합 절 우선 |
| 움직임·읽기 부담이 큰 사용자 / 정보 유지 | 정적 배치나 일시정지가 가능한지, 꼭 보여야 할 관계 | 사용자가 허용하는 움직임과 대체 표현을 먼저 확인. 해당 앱의 render/stop/preference 처리 증거가 없으면 계산 라이브러리가 자동으로 설정을 소비한다고 주장하지 않음 |

**이 카드로 확인된 것/아직 없는 것:** D3-N/B의 보조 출력2행이 API 방향을 지지한다. A/B의 새 운영 예측 차이는0/2이고 독립 원출력은 미확인이다. 원전 때문에 실제 설계자가 더 나은 선택을 했다는 자료는 없다.

## GV · Graphviz 14.1.1의 sfdp

**첫 링크 — [고정 sfdp 초기화·tuneControl](https://gitlab.com/graphviz/graphviz/-/blob/a74b50c20fc624f46f72e24f981b261f6e5edf71/lib/sfdpgen/sfdpinit.c#L200-224)**

먼저 필요한 출력이 최종 읽을 수 있는 그래프인지, 고정 좌표에서의 한 단계 힘/이동인지 확인한다. 첫 목적에는 [공식 sfdp 안내](https://graphviz.org/docs/layouts/sfdp/)가 유용하다. 두 번째 목적은 이번에 살핀 공개 경로에서 초기 좌표·maxiter 계약이 연결되지 않아 **미확인**이다. 최종 SVG가 나온 사실을 한 단계 힘 정답으로 쓰지 않는다.

**옮길 원리:** [Hu 저자 원고 §3–4](https://yifanhu.net/PUB/graph_draw_small.pdf)의 다단계 배치, 힘 방향의 정규화 이동, 공간 집계. sfdp가 Hu를 직접 지목하고 Hu가 Barnes–Hut를 지목한다. Hu는 동종 그래프 연구이며 천체 원전과 구별한다. [D001/D013/G025–G030](sources.jsonl).

**옮길 조건:** K/C/거리의 대응, 실제 executable 계수, 초기화, node update 순서, step과 종료, overlap/packing을 모두 맞춘다. 두 노드 direct 경로는 앞 노드가 이동한 좌표를 뒤 노드가 볼 수 있다. 이를 모든 quadtree 집계가 매 노드 이동마다 다시 계산된다는 뜻으로 확대하지 않는다.

**중단 조건:** r=0의 원 특이식, 공개되지 않은 private control, postprocess 전 좌표, 구판 screenshot만으로 선정14.1.1의 최종 가독성을 판정해야 한다면 보류한다. 같은 theta나 원논문 수치만으로 현재 binary의 오차/비용을 보증하지 않는다. [#2560](https://gitlab.com/graphviz/graphviz/-/issues/2560)과 [#2283](https://gitlab.com/graphviz/graphviz/-/issues/2283)은 후처리/beautify가 별도 실패점을 만든 구판 사건이다.

| 관점·우선순위 | 먼저 확인할 것 | 첫 링크를 바꿀 최소 추가 자료 |
| --- | --- | --- |
| 원전 저자 / 계산량·근사 | Hu의 목적함수, 입력 분포, 셀 폭과 개방 규칙 | 정확한 approximation budget와 단위가 오면 Hu §4·§6을 앞세움. 현대 성능 측정 없이 당시 시간을 옮기지 않음 |
| 유지보수자 / 초기화·회귀 | 공식 tag, build option, control 전달과 회귀 fixture | upstream의 실제 초기값·단계별 vector trace가 생기면 공개 one-step 비교를 재개 |
| UI 개발자 / 큰 그래프의 최종 화면 | 실제 node/edge/label·겹침·군집·출력 형식 | graph와 허용 겹침이 오면 공식 overlap/pack 사용 안내를 먼저 반환 |
| 읽기 부담이 큰 사용자 / 관계 식별 | 모든 노드를 펼칠 필요가 있는지, 숨겨도 되는 세부·필수 관계 | 사용자의 읽기 과제와 실제 화면 평가를 먼저 확보. 힘의 크기나 예쁜 예시 그림만으로 읽기 개선을 주장하지 않음 |

**이 카드로 확인된 것/아직 없는 것:** 문서 차용 경로와 고정 소스 대응은 확인했다. GV-N/B의 A보기·공개 한 단계 입력·원출력은 결손이며 native 실행은 미실시다. 더 늦은 예제를 찾아 기존 A를 소급 채우지 않는다.

## AN · AndroidX DynamicAnimation 1.1.0 SpringForce

**첫 링크 — [고정 SpringAnimation의 업데이트·정지·snap 분기](https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/main/java/androidx/dynamicanimation/animation/SpringAnimation.java#262)**

목표를 통과해야 하는지, 부드럽게 도달하면 되는지, 즉시 취소해야 하는지에 따라 읽을 분기가 다르다. AN-B 보조 실행은 내부 연속 상태가100.0375px인데 공개 속성은100px·속도0으로 종료한다. 이 차이를 먼저 설명할 수 있어 위 구현 절을 첫 줄로 택했다. 연속 모델 자체가 목적이면 [SpringForce.updateValues](https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/main/java/androidx/dynamicanimation/animation/SpringForce.java#272)를 앞세운다.

**옮길 원리:** 변위와 초기속도를 가진 선형 감쇠 진동의 해석해. [MIT p1](https://www.ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/911bc225e5913ba15517dbd70528c27a_MIT18_03SCF11_s13_1text.pdf)은 연구자 선택 설명 자료다. 해당 라이브러리가 이 교재나 특정 원논문을 채택했다는 기록은 검토 범위에서 미확인이다.

**옮길 조건:** 속성 단위/초, ms→초, 정규화 질량, ζ와ω, float 초기값을 맞춘다. 초기속도가 충분하면 임계감쇠도 한 번 목표를 통과할 수 있다. pixel threshold1은 위치 .75와 속도46.875의 **동시 엄격 미만** 판정을 만든다. 해석해와 이 종료 규칙을 분리한다. [A012–A016](sources.jsonl).

**중단 조건:** 큰 frame gap에서도 모든 경로를 사용자가 볼 것, cancel이 평형/속도0일 것, durationScale0이 모든 damping에서 항상 정지할 것이라고 요구하면 추가 검증이 필요하다. SDK33 미만과 이상에서 설정 소비 경로가 다르다. 현재 증거는 JVM 플랫폼 스텁이며 실제 기기의 관측이 아니다. [보조 실행 범위](streams/android/reproduce.md).

| 관점·우선순위 | 먼저 확인할 것 | 첫 링크를 바꿀 최소 추가 자료 |
| --- | --- | --- |
| 진동 원전 저자 / 물리 초기조건 | 실제 속성 단위와 정규화 질량, y₀/v₀, 해석해 | 물리적인 질량·단위·에너지 보존 요구가 오면 교재와 SpringForce를 우선하고 UI snap을 모델 밖으로 표시 |
| 유지보수자 / 회귀·호환 | 같은 SHA 시험의 입력과 활성 여부, cancel·pending target | 같은판 instrumented test와 보관 로그가 있으면 그 fixture를 우선. ignored/선언된 assertion만으로 통과를 주장하지 않음 |
| UI 개발자 / 보여 줄 동작 | 목표 통과를 보여야 하는가, cancel 후 어디에 남아야 하는가, frame cadence | 실제 화면·SDK·minVisibleChange·timestamp가 오면 SpringAnimation 또는 cancel 사용 안내 중 선택 |
| 움직임·읽기 부담이 큰 사용자 / 억제·대체 | Remove animations 설정과 보존할 정보, 즉시 상태 전환 허용 | 실제 기기 설정 소비 trace·앱의 damping0 사용 여부를 확인. [설계 패치](https://github.com/androidx/androidx/commit/13d32f91c54e21d074bc84416eecf9e6aa59d78a)만으로 모든 움직임 억제를 확정하지 않음 |

**이 카드로 확인된 것/아직 없는 것:** 배포 네 핵심 Java 파일이 release endpoint와 일치한다. 보조 주2행이 구현 설명을 지지한다. 첫 적격 사용 이슈·기기 원출력·실제 원전 채택·카드 효과는 각각 미확인/미실시다.

## RS · @react-spring/core 10.0.3

**첫 링크 — [고정 SpringValue.advance의 precision·clamp·단계 계산](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/core/src/SpringValue.ts#L220-L325)**

정확한 종료/초과 경계를 묻는다면 문서 기본값만 읽지 말고 이 분기를 함께 확인한다. 같은판 문서의 precision .01 안내와 코드의 거리 기반 기본값이 다르다. RS-B는 clamp=true여도1ms cadence에서 한 번 초과값을 내므로, API의 후속 진동 중단과 모든 샘플 절대 무초과를 구분해야 한다. [R024/R028](sources.jsonl), [보조 raw](streams/react/raw-outputs.json).

**옮길 원리:** m·k·b로 쓸 수 있는 감쇠 모델과 해당 변수 해석. [역사적 README](https://github.com/pmndrs/react-spring/blob/caec34387ffc28c289265f55280a5163a8fe2b8c/readme.md)는 animated/react-motion의 소프트웨어 영감을 명시하지만, MIT 같은 물리 원저작 채택을 입증하지 않는다. [react-motion stepper](https://github.com/chenglou/react-motion/blob/8bd4f7223a8d79535586220f7173f078d4604e07/src/stepper.js)의 유사성도 구체적인 코드 복사 사건으로 확대하지 않는다.

**옮길 조건:** 값/ms의 velocity, 1ms 속도 선행 Euler, ceil(dt), rawadvance와 [rafz의64ms cap](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/rafz/src/index.ts#L150-L168), precision/restVelocity와 stop/cancel을 명시한다. 물리 m/k/b와 제품 숫자 단위가 일치하는 범위만 설명한다.

**중단 조건:** 브라우저가250ms 쉬었으니 정확히250ms 물리해가 표시될 것, 강한 감쇠가 어떤 step에서도 안정할 것, idle이면 내부 velocity0일 것, hook 없이 OS preference가 자동 적용될 것이라는 요구는 보류한다. 실제 React 생명주기와 여러 instance 간 간섭은 원 ODE로 해결되지 않는다. [#2377](https://github.com/pmndrs/react-spring/issues/2377), [반례](streams/react/counterexamples.csv).

| 관점·우선순위 | 먼저 확인할 것 | 첫 링크를 바꿀 최소 추가 자료 |
| --- | --- | --- |
| 원전 저자 / 안정성·물리 모델 | 단위 변환, step, 원연속해와 수치해 오차 | 허용 오차·실제 시간표와 물리 재현 목적이 오면 원전/수치 분석을 먼저 반환 |
| 유지보수자 / API 의미·호환 | advance·rafz·rest 정책·실패 입력 | 같은 배포·schedule·config trace가 있으면 그 분기/시험 우선. 과거 snapshot을 현재 주입력 출력으로 바꾸지 않음 |
| UI 개발자 / 취소·목표 변경 | 원하는 final value, onRest 의미, 목표 타입·instance 소유 | 단순 사용법이면 stop/config 안내를 먼저 반환. [#813](https://github.com/pmndrs/react-spring/issues/813#issuecomment-538005400)처럼 config 위치 문제에는 물리 원전 불필요 |
| 움직임·읽기 부담이 큰 사용자 / 즉시 상태·정보 유지 | 앱의 useReducedMotion 장착과 실행 중 선호 변경 처리 | [실제 hook](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/shared/src/hooks/useReducedMotion.ts)·OS 이벤트·mountedUI trace가 오면 접근성 통합 경로 우선. 현재 raw SpringValue 실험만으로 앱 경험을 보장하지 않음 |

**이 카드로 확인된 것/아직 없는 것:** 고정 package provenance와 보조 주2행은 확인했다. stop 콜백은 [정정 probe](streams/react/stop-correction.json)를 따른다. A/B 추가 적중 분모는0이며 독립 원출력은 미확인이고 원전 링크 행동효과 검사는 미실시다. [#1389](https://github.com/pmndrs/react-spring/issues/1389#issuecomment-996624083)의 설정 발견은 실제 작성자 보고이지만 원전 링크 효과는 아니다.

## 카드를 뒤집는 공통 최소 증거

차용을 확정하려면 원문을 지목하는 수신 저자의 설계 기록이 필요하다. 원전의 새로운 적중을 주장하려면 다른 사전 예측, 같은판·같은입력의 독립 원출력, 그 차이를 설명한 원전 절이 함께 필요하다. 반환 링크가 행동을 개선한다고 주장하려면 실제 독자의 전후 선택과 목표 달성 기록이 필요하다. 지금 자료가 주는 것은 이 세 층을 구별해 원문을 선택하는 조건이다.
