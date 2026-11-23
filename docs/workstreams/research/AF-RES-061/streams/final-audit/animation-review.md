# Animation final audit — AF-RES-061#2

검토자 `/root/animation_audit`. 인수판 `672366cdf4542d4ca9f579963d66c2745f4316ed`. 이 검토는 봉인된 예측과 이미 수행한 실험을 보존하는 사후 검토다. 새 실험·인간 평가·최초 설계자의 행동 변화 측정은 수행하지 않았다. 검토의 시각·파일 해시·메타데이터 정정은 [animation-review.json](animation-review.json)에 있다.

## 결론과 발견한 정정

기존 Android·react-spring 네 주 사례의 숫자 및 변수 대응에서 실질적인 오류는 찾지 않았다. **같은 판·같은 입력의 독립 원출력은 4행 모두 미확인, 현재 확보는 관측 0/4**다. 이번 보조 실행과 상류 시험의 선언된 기대값을 독립 원출력으로 올려서는 안 된다. 무조건적 구현 동작에 관한 사전 A/B 불일치는 **관측 0/4**이므로, 불일치 행에서 원전 추가의 적중률은 **해당 없음**이다.

파일 정합성에서 한 가지 정정이 필요하다. `streams/react/artifact-hashes.json`의 `observations.csv`와 `counterexamples.csv` 해시는 CRLF bytes를 대상으로 했으나 원격 커밋은 LF로 저장했다. 원래의 CRLF를 재구성하면 두 기존 해시가 정확히 맞는다. 따라서 셀 내용 변경을 요구하는 결함은 아니며, **기존 영수증을 보존하고 최종 LF 해시를 함께 기록**한다. 상세 두 해시는 이 검토 JSON의 `hash_corrections`에 있다. 다른 react 실행·출력·영수증 8개, Android 보존 원본 4개, 관련 봉인 예측 파일 5개는 해시가 일치했다. 기존 manifest를 조용히 덮어쓰지 않았다.

## 필수 결과표에 사용할 네 행의 검토된 해석

| 사례·판 | 고정 입력·목적 | 원리·바뀐 가정 | 기존 보조 관측과 판정 | 원문·기록 |
|---|---|---|---|---|
| AN-N / DynamicAnimation 1.1.0 | 0→100px, v0, stiffness100, ζ0.5; 16/250ms와 목표 통과 | `y=x−target`, ω=√stiffness, c=2ζω. 해석해는 초, 입력 시간은 ms, 결과는 float. UI에는 종료 임계값·frame cadence가 추가된다. | 배포 소스 JVM 실행: 16ms x=1.21181833744, 250ms x=102.335960388. 16ms cadence의 첫 초과 표본은256ms, 종료912ms. 실제 단말·렌더링 결과는 미실시. API/A는 저감쇠 통과 경향만, B는 대응 조건부 연속모델을 설명했다. 사후 수치를 사전 구현 예측으로 바꾸지 않는다. | [SpringForce L215–313](https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/main/java/androidx/dynamicanimation/animation/SpringForce.java#215), [보조 출력](../android/evidence/probe-output.csv), [입력·범위](../android/reproduce.md) |
| AN-B / 동일판 | 99.9f→100px, v10px/s, stiffness100, ζ1, minimumVisibleChange1px | 원식은 초기속도 때문에 한 번 목표를 통과할 수 있다. 제품은 변위<0.75px와 속도<46.875px/s를 동시에 만족하면 target·속도0으로 snap한다. 둘 다 엄격한 `<`다. | 내부16ms x=100.037498474지만 첫 계산 pulse에서 공개 속성은100/v0으로 종료. 시작 pulse와 첫 계산 pulse를 구별한다. 원식 통과와 화면 관측 통과의 차이를 보여주는 보조 반례다. | [평형 검사 L229–234](https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/main/java/androidx/dynamicanimation/animation/SpringForce.java#229), [업데이트·snap L262–302](https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/main/java/androidx/dynamicanimation/animation/SpringAnimation.java#262), [관측](../../observations.csv) AN-B |
| RS-N / @react-spring/core10.0.3 | 0→1, mass1/tension100/friction10, velocity0, clampfalse | 연속식과 변수는 대응하지만 실제 구현은 1ms 속도 선행 Euler를 ceil(dt)회 수행한다. 속도는 값단위/ms. raw advance와 RAF64ms 상한은 서로 다른 경로다. | 새 인스턴스 advance16=0.012914278196155734, advance250=1.0253099081131323. 1ms schedule 첫 초과242ms, idle955ms이며 잔류 속도는 약8.7516×10⁻⁵ 값단위/ms. idle은 계속 움직인다는 뜻이 아니다. | [advance L220–325](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/core/src/SpringValue.ts#L220-L325), [rafz L150–168](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/rafz/src/index.ts#L150-L168), [출력](../react/raw-outputs.json) RS-N |
| RS-B / 동일판 | 같은 입력, clamptrue | clamp 검사가 각 내부 step 시작에 있고, 정지 검사는 그 앞에 있다. 따라서 샘플·frame schedule이 목표 초과 관측을 바꾼다. | 1ms schedule에서242ms 값1.0026630631890683을 한 번 출력,243ms target,244ms idle. 60Hz 수동 schedule에서는 초과 출력 관측0. advance250은 target1/idle. clamp를 모든 공개 샘플의 절대 초과 금지라고 단정하면 틀린다. | [clamp·step 순서](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/core/src/SpringValue.ts#L283-L325), [출력](../react/raw-outputs.json) RS-B, [보조 반례](../react/counterexamples.csv) |

## 차용 근거의 경계

AndroidX의 검토된 소스·API 범위에는 특정 기계진동 원저작을 지목하는 인용이 없다. 이 범위의 직접 인용 **관측 0**과 실제 개발자의 차용 과정 **미확인**을 분리한다. MIT 18.03SC의 진동식은 연구자가 고른 원교재이며 코드와 식의 대응을 검토하는 데 쓰였다.

react-spring은 [v8.0.27 README](https://github.com/pmndrs/react-spring/blob/caec34387ffc28c289265f55280a5163a8fe2b8c/readme.md)에서 animated와 react-motion을 소프트웨어 영감으로 지목한다. [10.0.3 Why Springs](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/docs/app/routes/docs.advanced.config.mdx#L205-L212)는 Andy Matuschak의 상호작용 설계 발언을 지목한다. 이 기록은 특정 진동 논문·MIT 교재·Rebound 채택의 증거가 아니다. `same_equation_only`와 명시적 소프트웨어 영감을 별도 열에 두는 기존 분류가 맞다.

## 출력·시험·실행 범위의 검토

Android 배포 sources.jar와 네 고정 Java 파일의 바이트 일치 기록은 보존돼 있다. 이번 검토에서 공식 SpringForce를 다시 가져와 SHA-256 `713a7683c0d5ad94ac5f451610893e6e52338eadb2d3533a7b5a001c6f78aca3`을 확인했다. Google 공식 release-log 끝점은 GitHub androidx 미러에서 404이므로 미러의 다른 SHA로 바꾸면 안 된다. 공식 googlesource에서는 읽혔다. [실제 재열람 원장](animation-sources.jsonl), [실패·대체 경로](animation-search-log.jsonl).

Android [SpringTests](https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/androidTest/java/androidx/dynamicanimation/tests/SpringTests.java)의 입력은 주 사례와 다르고, 일부는 `@Test` 없음 또는 `@Ignore`다. react-spring의 [SpringValue.test.ts](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/core/src/SpringValue.test.ts#L434-L523)에는 비활성 `xit`가 있으며 숫자 snapshot은 duration 입력이다. 활성 시험의 선언과 저장된 실행 출력도 구별해야 한다. 기존 보고가 이 경계를 지킨다.

React probe의 처음 null onRest는 listener를 후속 no-op start에 부착한 연구자 설정 문제다. 취소 결과에는 [stop-correction.json](../react/stop-correction.json)을 적용한다. `stop(true)`는 현재값을 유지하면서 cancelled=true/finished=false로 종료했으며, 처음의 null을 상류 결함으로 쓰지 않는다.

## 반환 카드와 결정을 바꾸는 최소 자료

| 카드 | 첫 링크와 이유 | 다른 첫 링크로 바뀌는 조건 |
|---|---|---|
| Android UI 종료·취소 질문 | [SpringAnimation.updateValueAndVelocity](https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/main/java/androidx/dynamicanimation/animation/SpringAnimation.java#262). 화면 값과 연속해의 차이를 결정하는 snap·retarget 분기를 직접 보여준다. | 물리 단위·해석해 오차 검증이 목적이면 원교재와 SpringForce mapping을 먼저. 움직임 억제가 우선이면 실제 SDK·설정·기존 애니메이션 처리 요구를 먼저 확인하고 AnimationHandler를 반환한다. |
| react-spring 목표 통과·clamp 질문 | [SpringValue.advance](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/core/src/SpringValue.ts#L220-L325). default precision/restVelocity의 문서 차이와 clamp 순서를 직접 구별한다. | 단순 사용 오류이면 제품 config·stop 안내가 먼저. 실제 기계진동 모형이 목적이면 원교재/단위 확인 먼저. 접근성 우선이면 앱이 useReducedMotion을 장착했는지와 preference 변경 시 이미 실행 중인 spring의 처리 요구가 먼저다. |

라이브러리 유지보수자에게는 같은 판·입력·frame schedule의 원 trace가 가장 작은 판별 자료다. 원전 저자에게는 물리량·단위·오차 기준이, UI 개발자에게는 목표 초과의 허용 여부·취소 반환값이, 움직임에 민감한 사용자에게는 최종 상태와 즉시 전환 허용 여부가 우선한다. 기존 이슈의 사용법 변경 보고를 이번 원전 링크의 행동 효과로 쓰지 않는다.

## 남겨야 할 세 가지 부족한 입력

1. **주 입력의 독립 원출력:** Android 실제 instrumented trace, react-spring 원저자 보관 trace가 필요하다. 지금의 보조 실행을 다시 돌리는 것만으로 결손이 사라지지 않는다.
2. **채택의 기록과 사람의 행동:** 물리 원저작을 지목한 당시 설계 기록과, 원전 링크로 실제 선택이 바뀌는 별도 관측이 필요하다. 수식 대응으로 대체할 수 없다.
3. **사용판·접근성 수명주기:** Android 기간별 첫 적격 이슈 목록과 실제 SDK 설정 trace, react-spring 앱의 hook 장착·기존 운동 처리 기록이 필요하다. 일반 접근성 지침은 해당 제품판의 소비 경로가 아니다.
