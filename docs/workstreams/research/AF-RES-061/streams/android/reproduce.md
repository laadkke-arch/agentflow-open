# Android 보조 실행과 미실시 검사

## 이번 실제 수행

```sh
python -B docs/workstreams/research/AF-RES-061/streams/android/run_probe.py
```

기존 OpenJDK21.0.13의 `java -m jdk.compiler/com.sun.tools.javac.Main`을 사용했다. 컴파일 exit0, 실행 exit0, stderr 없음. `javac` 명령의 최초 조회는127이었으나 compiler 모듈이 있어 설치 없이 해결했다. 소스·스텁·Probe 생성 디렉터리는 `evidence/probe-build/`이며 git에서 제외한다. 재생 스크립트, upstream의 작은 구현 파일, 원장·digest·stdout·receipt는 보존한다.

Google Maven 공식1.1.0 source archive SHA-256을 먼저 검사한다. SpringForce, SpringAnimation, DynamicAnimation, AnimationHandler, Force, FloatPropertyCompat, FloatValueHolder, FrameCallbackScheduler 여덟 원본 클래스의 바이트를 그대로 컴파일한다. Android 서비스를 대신한 스텁과 연구자 Probe는 스크립트에 명시했다. annotation/collection/view/clock/Choreographer/Looper/ValueAnimator를 스텁으로 제공한다. Property값은 실제 upstream FloatValueHolder를 통해 갱신한다.

주 입력은 AN-N=(x0=0px,target100px,v0=0px/s,kAPI100,ζ0.5), AN-B=(x0=99.9f,target100px,v0=10px/s,kAPI100,ζ1,minVisibleChange1px). 실제 float99.9f와 double99.9의 직접 force 호출을 모두 남긴다. 직접 force 시간16ms·250ms는 시작 상태에서 각각 독립적으로 호출한다. UI orchestration의 기준 timestamp는1000ms이며 첫 pulse가 기준이다. 이후16ms cadence 또는250ms cadence와3000ms 한 프레임을 구분한다. first-crossing은 표본값>100의 최초 표본이다.

추가 입력은 ζ2, 취소 직전 retarget200/취소 뒤 retarget300, stubSDK32/33×scale0, SDK33 listener로scale1→0, 그리고 scale0+ζ0다. 실행 첫 판과 두 번째 판의 차이는 마지막 감쇠0 변형 한 개다. 이것은 사후 반증이며 사전 예측이나 새 독립 원자료로 산입하지 않는다.

## 실제 Android에서 다음에 실행할 명령 — 이번 미실시

동일 AndroidX checkout을 준비하고 SHA를 먼저 확인한다. Android SDK·의존성 checkout·JDK 및 API33 기기가 필요하다. 이 환경에는 Android 에뮬레이터·연결 기기가 없었으므로 다음 명령을 실행하지 않았다.

```sh
git rev-parse HEAD
./gradlew :dynamicanimation:dynamicanimation:connectedDebugAndroidTest --info --no-daemon '-Pandroid.testInstrumentationRunnerArguments.class=androidx.dynamicanimation.tests.SpringTests#testCancelAfterAnimateToFinalPosition'
./gradlew :dynamicanimation:dynamicanimation:connectedDebugAndroidTest --info --no-daemon '-Pandroid.testInstrumentationRunnerArguments.class=androidx.dynamicanimation.tests.SpringTests#testDampingRatioOverAndCriticallyDamped'
./gradlew :dynamicanimation:dynamicanimation:connectedDebugAndroidTest --info --no-daemon '-Pandroid.testInstrumentationRunnerArguments.class=androidx.dynamicanimation.tests.SpringTests#testDampingRatioUnderDamped'
./gradlew :dynamicanimation:dynamicanimation:connectedDebugAndroidTest --info --no-daemon '-Pandroid.testInstrumentationRunnerArguments.class=androidx.dynamicanimation.tests.SpringTests#testUndampedSpring'
```

필수 HEAD는 `d5923c378c00b537f3421786eb3a50e6f6868386`다. 명령의 태스크 형태는 [원 저자의 2022년 명령](https://github.com/androidx/androidx/commit/13d32f91c54e21d074bc84416eecf9e6aa59d78a)과 일치하지만, 이번 checkout에서 Gradle task 존재·SDK 구성을 실제 실행해 확인하지 않았으므로 실행 계획이다.

이 기존 시험은 지정 AN-N·AN-B와 입력이 다르다. 같은 판/입력 검증에는 별도 연구자 instrumented fixture가 필요하다. 위 주 입력 그대로 FloatValueHolder·SpringAnimation을 설정하고 실제 onAnimationUpdate에 timestamp,value,velocity를 수집한다. 실제 프레임은 정확히16/250ms에 도달한다고 가정하지 말고, 직접 force16/250ms와 실제 frame timestamp를 별도 기록한다. AN-B는 첫 기준 pulse와 첫 계산 pulse를 구분한다. 시스템 설정 검사는 SDK32와33 이상을 구분하고 기존 animation scale 값을 기록·복원하는 별도 기기 절차가 필요하다.

`testScaleMinChange`에는 `@Test`가 없고 `testDurationScaleChangeListener`에는 `@Ignore`가 있다. 이 이름을 runner에 전달했다는 사실만으로 검사 완료가 되지 않는다. upstream 파일을 조용히 바꾸거나 ignored 검사를 활성화한 결과를 원판의 원시험 통과라고 부르지 않는다. 필요한 경우 별도 연구자 fixture를 명시적으로 만들고 그 입력·수정·출력을 보조 결과로 보고한다.

실제 화면에서 움직임이 억제되는지, 사용자 설정이 플랫폼에 반영됐는지, SDK34 이후 ignored 문제의 재현·해소는 모두 **미실시**다.
