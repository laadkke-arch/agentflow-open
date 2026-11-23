# RS — 구현판에서 확인한 설명·차용·행동의 범위

최종 예측 봉인 `02359364000057f69b00594d8b43571ac72df298` 뒤에만 아래 코드·시험·이슈 결과를 읽고 실행했다. baseline/A 파일은 수정하지 않았다. 증거 종류는 **고정 소스 사실 / 저자 보고 / 이번 보조 실행 / 연구자 추론**으로 구분한다. [`sources.jsonl`](sources.jsonl), [`observations.json`](observations.json), [`transfer-notes.json`](transfer-notes.json), [`execution.md`](execution.md)가 상세 원장이다.

## Q1 — 어떤 문제를 해결하려는가

공식 목적은 React의 단일 값과 화면 속성을 움직이는 것이다. 고정 README는 opacity와 y, 선언형·명령형 사용 및 여러 렌더링 target을 제시한다. 주 비교의 0→1은 연구자가 정한 무차원 진단이며, 실제 사용자 화면의 물리적 길이 또는 질량이 아니다. `advance(dt)`의 단위는 ms다. [R013/R033, 고정 README](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/README.md)

사전 제목·날짜 frame의 9개 결과에서 DNS 문제 #2370을 제외한 첫 적격 본문은 **#2377**이다. terrymun은 서로 다른 Button/Toggle의 ratio가 각자의 입력에 따라 움직이기를 원했다. 본문에는 `api.stop().start`, 임의 ratio, 소수점 셋째 자리 표시가 있다. 정확한 instance 수·픽셀 좌표·프레임 간격은 **미확인**이다. 사용판은 10.0.1이며, 10.0.0 비교와 후속 10.0.2 workaround 보고가 있다. 이것을 고정 10.0.3의 RS-N/B 원시험으로 쓰지 않는다. 최초성은 지정한 제목 여섯 단어와 release±365일 검색 frame 안에서만 성립한다. [R041/R042, 요청과 후속 보고](https://github.com/pmndrs/react-spring/issues/2377)

독립 작성자 m10의 #2381은 100ms마다 상태를 갱신하는 three 장면에서 scale 0.1→hover 1.5→leave 1을 원했으나 초기값으로 되돌아감을 보고한다. 이 입력은 보존하되 유지보수자가 같은 stale-update 사건으로 연결했으므로 저작·사건 수를 늘리지 않았다. 2026년의 10.0.4 해결 설명은 후대의 증언이다. [R043/R044, #2381](https://github.com/pmndrs/react-spring/issues/2381)

반증 탐색은 자연스럽게 보이는 감쇠 궤적이 화면의 목적을 충족한다는 가정을 겨냥했다. instance 소유권과 부모 재렌더의 초기화 문제는 올바른 진동 방정식으로 해결되지 않는다. 이 판단을 바꾸려면 같은 사용판·React 생명주기를 포함한 원 재현에서 물리 계수 변경만으로 instance 간 간섭이 해결되는 독립 출력이 필요하다.

## Q2 — 명시 차용 기록은 어디까지인가

10.0.3 README, 구성 API, SpringValue/AnimationConfig의 관련 구현과 주석에서 특정 기계진동 원논문·MIT 교재의 채택 기록은 찾지 못했다. 이것은 읽은 파일 안의 제한된 부재이며 개발자가 원전을 읽지 않았다는 증거가 아니다. 현행 구성 문서는 Andy Matuschak의 상호작용 설계 발언을 이름으로 인용한다. [R024/R025/R038, Why Springs](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/docs/app/routes/docs.advanced.config.mdx#L205-L212)

태그 이력을 따라간 **v8.0.27@caec34387ffc28c289265f55280a5163a8fe2b8c**의 readme는 Christopher Chedeau의 **animated**와 Cheng Lou의 **react-motion**을 직접 연결하고, interpolation/performance와 ease of use라는 구체적인 영감을 밝힌다. 같은 판에서 Andy의 원 tweet과 동영상도 연결한다. tweet/video 직접 열기는 실패하여 직접 독해 수에서 제외했다. Rebound 차용은 관측하지 않았으므로 적지 않는다. [R049/R050, 역사적 명시 문장](https://github.com/pmndrs/react-spring/blob/caec34387ffc28c289265f55280a5163a8fe2b8c/readme.md)

연결된 react-motion v0.5.2의 `stepper.js`를 읽으면 초 단위 속도 갱신, 고정 질량 생략, 정지 시 속도 0이 확인된다. 두 코드의 식이 닮았다는 사실을 특정 함수 복사의 입증으로 확대하지 않는다. 수신자가 밝힌 것은 사용성 등의 영감이다. [R051, 원 소프트웨어 stepper](https://github.com/chenglou/react-motion/blob/8bd4f7223a8d79535586220f7173f078d4604e07/src/stepper.js)

따라서 **소프트웨어 영감은 직접 인용**, **MIT 진동식 연결은 연구자 선택·같은 식 확인**, **특정 물리 원저작 채택은 미확인**이다. 이를 뒤집을 최소 자료는 해당 물리 출처를 지목하면서 코드 선택을 설명한 당시 설계 문서·커밋·저자 발언이다.

## Q3 — 실제 변수와 바뀐 가정

`position-goal`을 변위, mass/tension/friction을 각각 m/k/b로 놓고 시간을 초로 바꾸면 연속식 `m q″ + b q′ + k(q−goal)=0`과 대응한다. 실제 함수는 pt/ms 속도를 저장하며 spring 항에 10⁻⁶, damping 항에 10⁻³을 곱한다. 이 대응은 **봉인 후 소스에서 검증**했으며 용어만으로 사전 채택한 전제가 아니다. 여기의 pt는 API에서 사용하는 값 단위다. opacity 같은 값이 실제 미터나 질량 단위가 되지는 않는다. [R024, advance](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/core/src/SpringValue.ts#L278-L325)

수신 구현은 정확한 연속해 대신 1ms의 속도 선행 Euler 갱신을 `ceil(dt)`번 수행한다. 정수 간격이 아닌 16.1ms와 16.9ms는 둘 다 17번 갱신하여 동일한 값을 냈다. 일반 RAF 경로의 첫 간격은 16.667ms, 이후 간격 상한은 64ms다. raw `advance(250)`은 250ms를 직접 처리한다. [R032, RAF 시간 정책](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/rafz/src/index.ts#L150-L168)

원식에는 없는 제품 정책은 근접·속도 임계값, 목표 snap, clamp 순서, cancel, live retarget 및 skipped animation이다. 단위·계수 대응이 맞아도 이 정책까지 원전으로 설명했다는 주장은 성립하지 않는다. 동일 입력의 독립 upstream trace에서 위 단계식과 다른 결과가 나오면 실행 경로·배포 mapping부터 재검해야 한다.

## Q4 — 두 추가 보기에서 새로 안 것

A는 API 문서에서 첫 해당 setup 절 `Basic Usage`를 63개 표시 whitespace 단어, 코드 17행으로 읽었다. mass/friction/tension 설정은 있으나 목표 변경이나 출력은 없다. 더 풍부한 예제로 건너뛰지 않았다. B는 별도 독자가 진동 교재의 제한된 창을 읽어 조건부 연속식을 계산했다. A와 B 모두 실제 고정판의 시간별 수치와 3초 안 통과는 미확인으로 두었다. [`a-window.json`](a-window.json), [봉인 B 원장](../donor-reader/b-predictions.json)

따라서 이 두 사례의 **서로 다른 무조건적 구현 예측은 관측 0/2**다. B가 새로 준 것은 계수·시간 대응이 맞을 때 계산 가능한 물리 모델과, 정지·clamp가 추가 정책이라는 설명이다. API와 원전의 창 길이가 다르고, 같은 단어 수를 같은 정보량으로 보지 않는다. A 독자는 2026 release 제목에 선노출되었고 일반 학습 지식도 제거되지 않았다. 독립 인간 A/B 효과나 설계자의 행동 변화는 측정하지 않았다.

이 결론을 뒤집으려면 A/B가 실제 서로 다른 선택·예측을 사전에 기록하고, 동일 판·입력의 독립 출력에서 한 보기가 추가로 맞는 사례가 필요하다. 이후 소스를 읽고 얻은 더 나은 답은 사후 분석으로 남긴다.

## Q5 — 봉인 후 관측과 원출력의 구분

공식 npm 10.0.3의 gitHead를 source SHA와 맞추고 tarball/실행 파일 bytes를 검증한 후 다음 값을 얻었다. 전부 **이번 연구자 보조 실행**이다. [실행·해시](execution.md), [원 출력](raw-outputs.json)

| 고정 입력·관측 | RS-N clamp=false | RS-B clamp=true |
| --- | --- | --- |
| 새 인스턴스에 advance(16) 1회 | 0.012914278196155734 | 0.012914278196155734 |
| 새 인스턴스에 advance(250) 1회 | 1.0253099081131323, 움직이는 중 | 1, idle |
| 1ms frame에서 첫 출력 >1 | 242ms, 1.0026630631890683 | 242ms, 1.0026630631890683 |
| 1ms frame에서 처음 idle | 955ms | 244ms |
| 60Hz frame에서 목표 초과 출력 | 250ms frame에서 있음 | 기록 trace에서 관측 0 |

B의 조건부 정확 연속해 250ms 값 1.0233595799는 구현의 1.0253099081과 다르다. 이는 조건부 모델을 실제 구현 출력이라고 주장한 적중 또는 실패로 세지 않는다. 실제 차이는 고정 step과 제품 경계에서 확인했다.

고정 `SpringValue.test.ts`에는 damping, precision, cancel, skipAnimation의 **선언된 기대값**이 있다. underdamping 표제 시험은 `xit`이며 입력도 damping 1이어서 활성 증거가 될 수 없다. 저장된 0.100002…1 숫자 snapshot은 duration 시험이다. 이것을 spring 입력의 원출력으로 바꾸지 않았다. [R028, 해당 시험](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/core/src/SpringValue.test.ts#L434-L523), [R052, duration snapshot](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/core/src/__snapshots__/SpringValue.test.ts.snap#L3-L16)

검색한 상류 시험·snapshot 범위에서 **주 입력과 맞는 독립 원출력은 확보 0/2**이며 존재 일반은 미확인이다. 서로 다른 사전 A/B 예측 분모가 0이므로 그 조건부 정확률은 **해당 없음**이다. 동일 판과 같은 숫자의 상류 fixture·저자 보관 trace가 최소 재개 입력이다.

## Q6 — 원전을 그대로 권하면 틀리는 경계

1. **clamp가 모든 출력의 초과를 막는다는 해석:** 각 내부 step 시작에 경계를 검사하여 1ms schedule에서는 242ms에 한 번 초과값을 내고 다음 step에 목표로 돌린다. 후속 진동이 없다는 API 기대와 매 샘플 절대 초과 금지는 서로 다르다.
2. **정지면 속도도 0이라는 해석:** 기본 입력은 955ms에 q=1로 snap하고 idle가 되지만 velocity는 약 0.000087516 pt/ms로 남는다. 이것을 정지 뒤 실제 화면 이동이라고 읽어서도 안 된다.
3. **감쇠를 키우면 항상 안전하다는 해석:** friction=3000의 연속계는 강한 감쇠지만 1ms 고정 단계의 수치계는 16ms에 q≈−1.45658을 냈다. 이는 사후의 극단적 보조 입력이며 일반 추천 범위의 실패율로 쓰지 않는다.
4. **큰 browser frame 공백=같은 경과시간의 물리해라는 해석:** RAF 250ms 공백은 64ms만 전달했다. raw advance의 결과를 화면 시계 결과로 내세우면 틀린다.
5. **cancel은 목표까지 수렴한다는 해석:** stop(true)는 16ms의 현재값을 새 목표로 삼고 `cancelled=true, finished=false`로 끝났다. 초기 onRest 연결을 바로잡은 교정 probe만 callback 판정에 사용한다.
6. **prefers-reduced-motion을 설정하면 모든 기존 spring이 자동 중단된다는 해석:** hook을 호출해야 preference를 읽는다. global은 `_resume`에서 확인되며, 이미 움직이는 raw SpringValue에 global만 바꾼 뒤의 frame은 계속 진행했다. 새 시작은 목표로 즉시 갔다. 실제 mounted React/OS 조합은 미실시다. [R026/R031/R037, hook](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/shared/src/hooks/useReducedMotion.ts)

API만으로 충분했던 반례도 있다. #813의 opacity animation crash는 clamp를 config 밖에 넣은 입력 문제였고 요청자가 위치 변경의 해결을 보고했다. 진동 원전은 이 선택을 설명하지 않는다. [R047/R048, 원 stack과 수정 보고](https://github.com/pmndrs/react-spring/issues/813#issuecomment-538005400)

같은 판 문서도 전부 정확한 것은 아니다. 공개 API 표는 precision 기본 0.01과 restVelocity의 precision fallback을 제시하지만 실제 기본은 거리 비례 precision, 속도 threshold는 precision/10이다. 0→1의 기본 정지 955ms는 explicit precision .001과 같았고 .01은 586ms였다. **제품 API를 우선 반환한다는 판단에도 판별 구현 절을 연결해야 한다.**

## Q7 — 반환 링크와 실제 행동 변화

이 고정판의 scalar spring 경계 질문에는 [SpringValue.advance의 근접·clamp·step 절](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/core/src/SpringValue.ts#L220-L325)을 첫 줄로 둔다. 문서 default와 실제 코드의 불일치, transient 초과, 시간 단위를 여기서 구분할 수 있다. 원전 링크는 연속 모델의 설명이 필요할 때 함께 준다.

| 이해관계자 | 지금 필요한 첫 근거 | 첫 링크 선택을 바꿀 최소 자료 |
| --- | --- | --- |
| 원전 저자·수리 모델 검토자 | 물리 모델 원절과 변수 mapping | 어떤 식·단위·오차를 검증할 것인지와 원저작을 지목한 채택 기록 |
| 라이브러리 유지보수자 | 고정 advance + rafz 경계 코드 | 같은 배포·frame schedule·config의 실패 trace와 desired API 의미 |
| UI 개발자 | 해당 구현 절; 단순 취소 사용법이면 stop API | target 타입, cancel의 기대값, 실제 frame schedule과 event 요구 |
| 움직임·읽기 부담에 민감한 사용자 | 원하는 최종 상태/즉시 전환의 허용 여부를 먼저 확인하고 useReducedMotion 근거 | 실제 앱의 hook 장착·OS preference 전환 기록과 사용자가 허용하는 움직임 |

실제 행동 변화에 대한 독립 저자 보고는 #1389에 있다. 초기 '해결됨'이라는 유지보수자의 시각 판단을 요청자가 반박했고, 이후 precision 변경은 요청자가 효과를 확인했다. 기본값 변경을 breaking change로 볼지 문서에 제안할지 논의했다. 이는 제품 사용법 발견의 사례이며 다른 분야 원전 링크의 효과가 아니다. [R045/R046, precision 논의](https://github.com/pmndrs/react-spring/issues/1389#issuecomment-996624083)

## 한계와 재개 순서

- **원출력 결손:** 상류 같은 10.0.3/입력/schedule trace를 먼저 확보한다. 지금의 정량값은 보조 실행이다.
- **차용 계보 결손:** 실제 physics 논문·저자 공개판을 지목하는 설계 기록을 찾는다. 현 자료는 소프트웨어 영감과 식 대응까지만 뒷받침한다.
- **행동·접근성 결손:** 요청자의 실제 앱에서 preference 전환과 cancel·retarget 기대를 확보한다. 원전의 정착 조건을 사용자의 편안함이나 목표 달성으로 대체하지 않는다.
