# AndroidX DynamicAnimation 1.1.0 — 봉인 뒤의 대조

예측 봉인: `02359364000057f69b00594d8b43571ac72df298`. 이 파일의 구현 독해·보조 실행·이슈 본문은 그 뒤에 수행했다. `baseline.json`과 `a-predictions.json`은 수정하지 않았다. 주 사례는 AN-N·AN-B 두 개이며, 실행 출력 행과 보조 변형을 별도 사례나 독립 원출력으로 세지 않는다.

## 확인 범위

공식 Maven `dynamicanimation-1.1.0-sources.jar` SHA-256 `d730234d4276722a13721feea2630a5aaa189d5dc11681aacc7cfe94527d7b94`의 SpringForce·SpringAnimation·DynamicAnimation·AnimationHandler 네 파일이 공식 release-log 끝점 `d5923c378c00b537f3421786eb3a50e6f6868386`의 대응 파일과 각각 바이트 일치했다. [대조 영수증](evidence/source-match.json). minSdk21·minCompileSdk34·minAGP8.1.1은 배포 AAR 메타데이터에서 읽었다. 현재 안내의 maintenance-mode 문구를 2025년 정책으로 소급하지 않는다.

JVM 보조 실행은 배포 소스의 여덟 클래스 본문을 변경하지 않고 컴파일했다. Android View·Choreographer·Looper·ValueAnimator 등은 명시적인 연구자 스텁이고, frame timestamp는 수동 입력이다. 실제 Android 단말·에뮬레이터·시스템 설정·화면 렌더링을 실행했다고 부르지 않는다. `javac` 실행 파일은 없었으나 기존 JDK21의 `jdk.compiler` 모듈로 컴파일했다. 설치는 하지 않았다. [명령과 범위](reproduce.md), [컴파일·실행 영수증](evidence/probe-receipt.json), [전체 작은 출력](evidence/probe-output.csv).

## Q1. 사용 목적과 요청자의 목적

API는 픽셀·스케일·회전 같은 속성의 시작값·시작속도·목표·강성·감쇠와 종료 가시성을 설정한다. A 창은 공식 안내의 첫 구성 절이며 239단어로 고정했다. 이 창은 앱을 갑자기 떠나거나 뷰가 보이지 않으면 취소할 수 있다는 제품 수명주기 요구를 추가하지만 수치 해법이나 종료 임계값을 주지 않는다. [A011](sources.jsonl), [창 메타데이터](a-window.json).

사전 모집 기간은 2024-04-09~2026-04-09다. 공식 tracker 목록은 웹 독해에서 로그인 링크만 반환했고, 직접 공개 HTML의 날짜 질의에서도 정렬된 후보 프레임을 확보하지 못했다. 따라서 **그 기간의 첫 적격 사용 이슈는 미확인**이다. 검색 결과가 없다는 것을 관측 0건으로 바꾸지 않는다. [모집 원장](issue-recruitment.json), [후속 접근 원장](search-log.jsonl).

보조 이슈 [182190872](https://issuetracker.google.com/issues/182190872)는 2021-03-09의 공개 요청이다. 원 요청자는 시작→목표 변경→다음 프레임 전 즉시 취소→새 목표 변경 뒤 새 목표가 사용되기를 요구하지만 이전 pending target이 사용된다고 보고했다. 픽셀 수치·배포 버전·원 실행 trace는 없다. 이번 연구의 0→100과 99.9→100 입력은 연구자가 정한 진단이다. 같은 메커니즘의 [2019년 취소 수정](https://android-review.googlesource.com/c/platform/frameworks/support/+/978170)과 보수적으로 한 계보로 묶었으며, 동일 사용자의 같은 사건이라는 인과관계는 주장하지 않는다.

독립 설계 기록 [13d32f91](https://github.com/androidx/androidx/commit/13d32f91c54e21d074bc84416eecf9e6aa59d78a)는 Remove animations 설정에 대응하기 위해 duration scale을 소비하도록 바꿨다고 명시한다. 이는 실제 라이브러리 유지보수자의 제품 결정이며, 이번 링크 노출 때문에 설계자의 행동이 바뀌었다는 관측은 아니다.

반증 탐색은 기간 제한 tracker, 공식 코드 이력, 공개 이슈 본문, 수정의 원시험으로 진행했다. 첫 적격 요청자의 목표·성공을 바꿀 최소 입력은 해당 기간의 완전한 정렬 후보 목록과 첫 적격 이슈의 공개 본문·사용판이다.

## Q2–Q3. 원전 차용과 수식 대응

네 고정 Java 파일 전체와 공통 API Javadoc에서 특정 진동 논문·저자·교재로 이어지는 명시 인용은 찾지 못했다. 보이는 외부 주소는 라이선스이고, `analytical approach`라는 설명은 논문 채택 기록이 아니다. 이 범위의 직접 인용은 **관측 0**, 다른 설계 문서·구두 학습에서의 실제 차용은 **미확인**이다. 이번 진동 교재 링크는 연구자 대응이며 `same_equation_only`로 기록한다.

| 원리·변수 | 고정 구현 위치 | 실제 대응과 달라진 가정 |
|---|---|---|
| 변위 y=x−target | [SpringForce.java L215–221, L272–278](https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/main/java/androidx/dynamicanimation/animation/SpringForce.java#215) | 절대 화면 좌표를 최종 위치에 대한 상대 변위로 바꾼다. |
| 자연진동수 ωₙ | 같은 파일 L135–140 | `sqrt(stiffness)`를 저장한다. 별도 질량 API가 없으므로 정규화 질량1 모델과 대응할 수 있지만 kg·N/m의 물리 단위를 제품이 보장하지 않는다. |
| 감쇠계수 c | 같은 파일 L218–221 | `2*ωₙ*dampingRatio`; 반환 가속도는 `−ωₙ²*y−c*v`. 공개 속도 단위는 속성/초다. |
| 연속해와 시간 | 같은 파일 L239–313 | 과감쇠·임계감쇠·저감쇠의 해석해를 선택한다. 입력 long ms를 /1000하여 초로 쓰며 결과는 float로 축소한다. Euler 업데이트라고 설명하면 틀린다. |
| 초기조건 | 같은 파일 L280–308 | 매 호출의 직전 위치와 속도가 계수를 결정한다. 임계감쇠라도 목표 쪽으로 충분한 초기속도가 있으면 한 번 목표를 통과할 수 있다. |
| 종료 허용량 | [DynamicAnimation.java L295,L738–739](https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/main/java/androidx/dynamicanimation/animation/DynamicAnimation.java#738), SpringForce L77–80,L229–234,L326–328 | 가시 변화량×0.75와 그것의62.5배 속도를 **둘 다 엄격히 미만**일 때 평형으로 취급한다. 1px이면0.75px·46.875px/s다. 원 진동 방정식의 필연적 정지점이 아니다. |
| 관측값과 종료 | [SpringAnimation.java L259–302](https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/main/java/androidx/dynamicanimation/animation/SpringAnimation.java#259) | 먼저 적분, 범위 제한, 평형 검사를 한 뒤 target·0속도로 바꾸고 종료한다. 따라서 내부 연속해의 overshoot가 화면 속성에 나타나지 않을 수 있다. |
| 프레임과 설정 | DynamicAnimation L671–692; [AnimationHandler L123–132,L257–273](https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/main/java/androidx/dynamicanimation/animation/AnimationHandler.java#123) | 첫 pulse는 시작값만 복사한다. SDK33 이상에서만 시스템 duration scale 초기값·변경 통지를 이 경로로 읽는다. 0이면 큰 시간 간격으로 대체한다. |

불변 목표를 가정하는 교재 해와 달리 retarget는 한 프레임의 절반을 이전 목표, 절반을 새 목표로 계산하는 근사를 쓴다. 취소·가시성·사용자 설정·float 양자화도 원 해석해 밖의 제품 결정이다. 특정 원전 채택이라고 판정을 바꿀 자료는 유지보수자의 명시적 설계 인용과 해당 코드판을 연결하는 기록이다.

## Q4–Q5. 봉인 예측과 관측의 층

공통 API와 A 창은 저감쇠의 overshoot 경향을 설명하지만 지정 시간의 좌표·정지 순간을 정하지 않았다. B는 원식에 대한 조건부 수치를 주며, 라이브러리의 질량·시간·정지 설정 대응을 조건으로 남겼다. 사후의 코드 대응과 보조 실행을 이용해 이를 사전 라이브러리 예측으로 바꾸지 않는다.

| 사례 | 정확한 배포 소스의 JVM 보조 결과 | 원출력·검증 경계 |
|---|---|---|
| AN-N | SpringForce 직접 호출16ms: x=1.21181833744px, v=147.226440430px/s. 250ms: x=102.335960388, v=274.109893799. 정수 ms 중 처음100 초과는242ms. | 연구자 보조 출력이다. 같은 입력·판의 독립 보관 원출력은 미확인. |
| AN-N 프레임16ms | 첫 시간기준 pulse에서는x=0만 복사. 이후 첫100초과 표본256ms, 처음 종료912ms에서x=100/v=0. | 첫 초과 표본은 연속해의 정확한 교차 시각이 아니다. 수동 timestamp이고 실제 UI프레임 보장은 없다. |
| AN-B | 실제 API float99.9f는99.9000015258789. SpringForce16ms의x=100.037498474, v=7.29434871674. | double99.9 입력일 때x=100.037490845로 차이가 난다. 입력 정밀도를 숨기지 않는다. |
| AN-B 종료 | 초기 pulse는99.9000015259/v10. 첫16ms 업데이트에서x=100/v=0으로 snap하고 종료. | 이 수동 프레임 실행에서는 내부 해가 목표를 지났어도 공개 속성에는 overshoot가 나타나지 않는다. 최소변화량1px 임계값이 원인이다. |

같은 SHA의 원시험은 `SpringTests.java`에 존재한다. [고정 원문](https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/androidTest/java/androidx/dynamicanimation/tests/SpringTests.java). 정상 비교는 시작800·감쇠1/1.5/2·고강성, 저감쇠 비교는 시작360·감쇠0.3/0.5/1·기본강성이다. AN-N/AN-B와 같은 입력이 아니므로 참고 기대값이다. 취소 원시험 L169–190은 이전목표200→취소→새목표−200→skipToEnd에서 취소 이벤트0과 정상 종료−200을 선언한다. 보관된 실제 출력·동일판 CI artifact는 확보하지 않았다.

원시험 독해에서 세 가지 반대 증거를 확인했다. 첫째, `testScaleMinChange` L622는 `@Test`가 없고 목표1 뒤 종료 기대값0을 갖는다. 둘째, `testDurationScaleChangeListener` L880은 `@Ignore`이며 SDK34 실패 주석이 있다. 셋째, 저감쇠 비교 L302–307은 `velocity2=velocity` 직후 두 값이 반대 부호라는 조건을 검사하므로 그 bounce-count 분기는 실행될 수 없다. 이들 선언을 통과한 원 관측으로 사용할 수 없다. 전체 테스트가 실패한다고 확대하지도 않는다.

## Q6. 원전을 그대로 권하면 틀리는 조건

1. **연속 통과와 화면 관측은 다르다.** AN-B 수동 프레임 실행은 내부 해가100을 넘지만 첫 공개 속성 업데이트가100으로 종료된다. 실기기 화면은 미실시다. 정지 임계값 없이 원전만 읽고 UI overshoot를 보장할 수 없다.
2. **프레임을 길게 건너뛰면 경로를 보지 못한다.** AN-N에3000ms 한 pulse만 주면100/v0으로 종료하여 중간 overshoot가 보이지 않는다. 같은 해석해의 수치 안정성과 화면이 보여준 경로는 별개다.
3. **감쇠를 키우면 빠르게 정착한다는 무조건 명제는 틀린다.** 같은 입력에서감쇠2의16ms cadence 종료는1856ms, 감쇠0.5는912ms다. 지정 threshold와 초기조건에서의 보조 결과이며 임의 감쇠의 순위가 아니다.
4. **취소는 평형 도달이 아니다.** 16ms에서 취소한 경우x=1.21181833744, v=147.226440430을 남기고 running=false가 된다. pending target은 새 spring target에 반영되며 이후 명시적 retarget가 다시 덮어쓴다. 원전의 에너지 소멸로 설명할 수 없다.
5. **설정 소비와 모든 운동 억제는 다르다.** SDK33 스텁 경로의 durationScale0은 기본 감쇠에서 첫 업데이트를 종료시켰지만, 감쇠0의 추가 변형은x=171.281753540, v=701.349548340으로 계속 running이다. 이 반례는 소스에 값이 전달된 사실을 부정하지 않는다. 실기기에서의 재현은 미실시다. SDK32 스텁에서는 이 코드 경로가 설정을 읽지 않아scale1로 움직였다.

추가 변형은 예측 봉인 이후의 반증 행이다. 처음 실행 결과는 `probe-output-v1.csv`와 `probe-receipt-v1.json`에 보존했고, durationScale0의 무조건 종료 주장을 확인하기 위해 감쇠0 한 변형을 추가한 후 두 번째 실행을 기록했다.

## Q7. 반환 카드와 이해관계자의 선택

**첫 반환 링크:** [1.1.0 SpringAnimation의 업데이트·종료 분기](https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/main/java/androidx/dynamicanimation/animation/SpringAnimation.java#259). 설계자가 보는 값이 왜 원 연속해와 다른지를 가장 직접적으로 확인할 수 있기 때문이다. 임계값은 이어지는 `DynamicAnimation.getValueThreshold`와 `SpringForce.isAtEquilibrium`를 읽는다.

| 읽는 사람·목적 | 우선 위치 | 선택을 바꿀 최소 자료 |
|---|---|---|
| 진동 원전 저자·해석 모델 검토자 | SpringForce.updateValues의 변수·단위와 원 교재의 초기조건 절 | 실제 질량·물리 단위를 시뮬레이션해야 한다는 요구가 나오면 원전 먼저; 화면 장식이라면 제품 분기 먼저 |
| 라이브러리 유지보수자 | 고정 source와 같은 SHA의 cancellation test·ignored test 위치 | 같은 입력의 공개 CI trace와 테스트 활성 여부 |
| UI 개발자 | SpringAnimation.updateValueAndVelocity와 cancel | 목표 통과를 꼭 보여야 하는지, 아니면 즉시 종료해야 하는지에 대한 구체적인 화면 요구·프레임 예산 |
| 움직임·읽기 부담에 민감한 사용자 | 우선순위 재질문 후 Remove animations 설계와 실제 옵션 소비 경로 | 실제 기기 SDK·사용자 설정·감쇠0 사용 여부·효과 억제 요구; 일반 접근성 권고만으로 해당판 동작을 확정하지 않음 |

정확한 연속 운동을 보존하려는 목표는 UI를 지연 없이 취소하거나 움직임을 억제하려는 목표와 충돌할 수 있다. 2022년 Remove animations 설계와 2019/2021 취소 계보는 그 제품 요구가 실제로 제기됐음을 보여 준다. 이번 연구에서 링크를 받은 실제 설계자의 행동 변화는 **미실시**이며, 카드 선택은 근거를 사용한 연구자의 반환 제안이다.

## 남은 결손과 첫 재개 행동

- 첫 적격 사용 이슈: 완전한 기간별 tracker 후보 목록을 얻어 동일 모집 규칙으로 정렬한다. 오래된 보조 이슈로 빈 자리를 메우지 않는다.
- 같은 판·같은 두 입력의 독립 원출력: 현재 **미확인 2/2**. 자체 JVM 출력으로 바꾸지 않는다. 실제 Android instrumented fixture와 로그가 필요하다.
- 차용의 기록: 지정 공개 source/API 범위에서 특정 원전 인용은 관측0. 저자의 설계 기록 또는 원전 명시 인용이 있어야 실제 차용 판정이 바뀐다.
