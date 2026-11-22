# AF-RES-045 · Audacity 재개 입력과 미실행 명령

이 문서는 **실행하지 않은 재현 계획**이다. 역사 프로그램의 빌드·실행·pipe 통신을 수행한 기록이 아니다. 세 요구의 봉인본은 `0d998cb3503e8a7f0faf2bf2f8e62dd046a662b1`의 requests.csv/predictions.csv이며, 아래 계획으로 원예측을 대체하지 않는다.

## 1. 고정 소스와 실행물의 구분

| 용도 | 소스 SHA | 확인된 위치 |
| --- | --- | --- |
| AUD01·AUD02 당대 기준 | `008d8d8c8cb6f6fac9c95f72513f6b0bc98af1dc` | Audacity2.3.3; Nyquist START/END, SetClip Color0..3 |
| AUD03 당대 기준 | `16d52f63a4183bba77ef7305d14622958dc0d1d5` | Audacity2.4.2; NoiseReduction.cpp L75–77의 지역 undef |
| AUD01 후속 구현 C | `0ffa73b9f44acc339e12a350edadd96590dc4b17` | PR6165; GetInfoCommand.cpp L634–645 |
| AUD01 후속 Nyquist wrapper | `ae0ab087588d5c54c1231ecdf42f4eead5aa11be` | PR6347; nyquist/init.lsp L54–78 |
| AUD03 후속 컴파일 조건 정리 | `e7d17d1bcedcb1fe75d78eb522de3b46476c94b7` | PR6201 구성 변경; NoiseReduction.cpp L75–77 |

아래 `AF045_AUDACITY_REPO`에는 위 객체를 이미 확보한 **Audacity 저장소**의 절대 경로를 지정한다. AgentFlow 결과 저장소의 경로가 아니다. `git show`의 소스 SHA와 실제 실행 바이너리의 관계는 별도로 확인해야 한다. 체크아웃 이름이나 About 창 버전만으로 동일 바이너리를 인증하지 않는다.

```sh
AF045_AUDACITY_REPO=/absolute/path/to/audacity
git -C "$AF045_AUDACITY_REPO" cat-file -e 16d52f63a4183bba77ef7305d14622958dc0d1d5^{commit}
git -C "$AF045_AUDACITY_REPO" cat-file -e 0ffa73b9f44acc339e12a350edadd96590dc4b17^{commit}
git -C "$AF045_AUDACITY_REPO" cat-file -e e7d17d1bcedcb1fe75d78eb522de3b46476c94b7^{commit}
```

이 명령들은 미실행이다. 실행할 때 UTC, 실제 저장소 HEAD, 명령별 종료 코드와 stdout/stderr를 보존한다. 객체가 없으면 이 계획의 소스 검사는 미실시로 남는다. 여기에는 저장소 취득·빌드·패키지 설치 명령을 포함하지 않았다.

## 2. AUD01 · 같은 시각을 pipe로 반환하는 후속 C

### 2.1 판별 대상

봉인 A는 새 전용 `GetTime`이고, 봉인 B는 **기존 NyquistPrompt의 선택 속성 읽기**다. 이후 채택된 `GetInfo: Type=Selection`은 C다. C에 봉인된 두 입력을 적용하면 후속 구현의 범위를 확인할 수 있으나, **원래 두 donor 후보가 다른 결과를 예측했다고 바꾸거나 A/B의 판별 성공으로 셀 수 없다.**

명령 구문의 근거는 다음 고정 소스다.

- [SelectCommand.cpp L53–77·L104–148](https://github.com/audacity/audacity/blob/0ffa73b9f44acc339e12a350edadd96590dc4b17/src/commands/SelectCommand.cpp#L53-L148): Select Time, Start, End, RelativeTo 및 ProjectStart 기준.
- [GetInfoCommand.cpp L634–645](https://github.com/audacity/audacity/blob/0ffa73b9f44acc339e12a350edadd96590dc4b17/src/commands/GetInfoCommand.cpp#L634-L645): 선택의 t0/t1를 Start/End로 반환.
- [pipeclient.py L14–36·L262–302](https://github.com/audacity/audacity/blob/0ffa73b9f44acc339e12a350edadd96590dc4b17/scripts/piped-work/pipeclient.py#L14-L36): 입력 줄을 명령으로 보내는 CLI, 응답 시간 제한, Q 종료.
- [pipe_test.py L10–11·L21–30·L50–65](https://github.com/audacity/audacity/blob/0ffa73b9f44acc339e12a350edadd96590dc4b17/scripts/piped-work/pipe_test.py#L10-L65): Audacity와 mod-script-pipe가 이미 동작해야 함, 플랫폼별 pipe와 응답 구분.

### 2.2 입력 환경과 준비 조건

실행자는 C가 포함된 고정 빌드와 출처·빌드 설정·바이너리 해시를 먼저 확보한다. 이미 실행 중인 해당 빌드에서 mod-script-pipe가 활성화되어 있어야 한다. 다른 동시 pipe 작성자가 없는 상태를 기록하고, 3초 이상 길이의 한 mono track을 담은 새 시험 프로젝트를 사용한다. 샘플레이트와 입력 오디오 파일 SHA256도 기록한다. 시각 조회 자체는 파형 내용에 의존하지 않지만 프로젝트·선택 입력을 특정하기 위한 조건이다.

`AF045_OUTPUT_DIR`은 AgentFlow 저장소에서 이 과제의 소유 경로 아래에 마련한 **기존 출력 디렉터리**다. 다음 명령은 fixed source의 공식 CLI를 복사해 사용하므로 출처와 라이선스 머리말을 유지한다. 새 보조 시험 코드의 정확성을 역사 구현의 보증으로 사용하지 않는다.

```sh
AF045_OUTPUT_DIR=/absolute/path/to/agentflow-open/docs/workstreams/research/AF-RES-045/evidence/reproduction
git -C "$AF045_AUDACITY_REPO" show 0ffa73b9f44acc339e12a350edadd96590dc4b17:scripts/piped-work/pipeclient.py > "$AF045_OUTPUT_DIR/pipeclient-0ffa73b9.py"
python3 "$AF045_OUTPUT_DIR/pipeclient-0ffa73b9.py" -t 10 -s False <<'AUDACITY_COMMANDS'
Help: Command="SelectTime"
Help: Command="GetInfo"
SelectTime: Start=1.25 End=2.50 RelativeTo=ProjectStart
GetInfo: Type=Selection Format=JSON
SelectTime: Start=1.25 End=1.25 RelativeTo=ProjectStart
GetInfo: Type=Selection Format=JSON
Q
AUDACITY_COMMANDS
```

**미실행**이다. Help 응답은 실행 빌드의 실제 명령 목록과 인자 확인에 사용한다. 지원되지 않는 명령, pipe 오류, timeout 또는 setter 실패가 있으면 이후 getter 결과를 성공으로 해석하지 않는다. 공식 CLI의 timeout 문구는 검사 결과에 포함하며, 프로세스의 종료 코드만으로 각 명령 성공을 판정하지 않는다.

| 입력 | C에 대해 확인할 값 | 지금의 상태 |
| --- | --- | --- |
| 선택 [1.25, 2.50]초 | JSON 숫자 Start=1.25, End=2.50 | 미실행·미확인 |
| 점 선택 [1.25, 1.25]초 | JSON 숫자 Start=1.25, End=1.25; 길이0 | 미실행·미확인 |

원 응답 전체를 명령별로 보존한 뒤 숫자로 비교한다. 이 수치는 이진수로 정확히 표현 가능한 값이지만, 출력 문자열의 공백·자리수 차이는 별도다. 숫자 비교를 허용 오차로 할 경우 연구자가 사전에 정한 `abs(observed-expected) <= 1e-6 seconds`를 명시하고, 원 JSON을 남긴다. 이 문서는 실행한 자동 비교 결과를 제공하지 않는다.

**봉인 B의 정확한 pipe 구문은 아직 검증되지 않았다.** 당대 소스가 Nyquist에 START/END 속성을 제공한다는 사실과 그 값을 NyquistPrompt 명령으로 pipe 밖에 전달할 수 있다는 사실은 다르다. 미확인 인자·따옴표·응답 경로를 갖는 NyquistPrompt 명령을 만들어 여기에 실행 가능 명령처럼 넣지 않았다. 재개 시 같은 공식 CLI로 `Help: Command="NyquistPrompt"`를 조회하고, 당대 NyquistPrompt의 명령 정의·응답 직렬화 경로를 먼저 읽어야 한다. C 또는 이후 `aud-get-info` wrapper의 성공을 B의 성공으로 대체하지 않는다.

### 2.3 판단을 바꿀 최소 증거

A와 B의 각각의 고정 구현, 동일 프로젝트의 두 선택 상태, 실제 보낸 바이트·응답, 버전·바이너리 해시가 연결되어야 한다. C의 추가 시험은 해당 C가 이 두 시각을 반환한다는 범위를 강화할 뿐이다. A/B 모두 같은 두 값을 반환한다면 donor 간 판별성은 여전히 없으며, 서로 다른 명령 이름을 다른 수치 결과로 세지 않는다.

## 3. AUD02 · 현재 네 색 API로 임의 RGB를 시험할 수 없음

[2.3.3 SetClipCommand.cpp](https://github.com/audacity/audacity/blob/008d8d8c8cb6f6fac9c95f72513f6b0bc98af1dc/src/commands/SetClipCommand.cpp#L31-L55)의 Color0..3 enum과 clip별 color-index 설정은 **임의 RGB 전경/배경 인터페이스가 아니다.** 아래는 그 한계를 다시 읽기 위한 미실행 명령이다.

```sh
git -C "$AF045_AUDACITY_REPO" show 008d8d8c8cb6f6fac9c95f72513f6b0bc98af1dc:src/commands/SetClipCommand.cpp | rg -n -C 3 'enum kColours|Color0|Color1|Color2|Color3|DefineEnum|SetColourIndex'
```

`SetClip: Color=#777777` 같은 미확인 구문을 제시하지 않는다. 알려진 인터페이스가 표현하지 못하는 입력의 거부를 donor A/B의 실패로 세어도 안 된다.

실제 A/B 시험을 만들려면 먼저 [Audacity4에서 고쳤다는 발언](https://github.com/audacity/audacity/issues/511#issuecomment-2445034377)에 대응하는 코드 SHA와 사용자색·배경색 인터페이스를 특정해야 한다. 그다음 아래 입력을 서로 구분하여 기록한다.

| 입력 | A: 임의 RGB 값 보존 | B: 읽을 수 있게 자동 보정 |
| --- | --- | --- |
| foreground #000000, background #FFFFFF | 두 값 보존 | 요구 대비가 충분하면 두 값 보존 가능 |
| foreground #777777, background #777777 | 두 값 보존, waveform 대비비1:1 | foreground 또는 대체 표시를 변경하여 대비 확보; 원색 보존 요구와 충돌할 수 있음 |

필수 새 자료는 실제 적용한 UI/명령 입력, 저장된 전경·배경 RGB, 렌더된 결과, 테마·선택/hover 상태, 사용자 override 가능 여부다. 별도 테두리를 추가하는 구현은 A/B 어느 쪽에도 억지로 넣지 말고 제3안으로 기록한다. 기존 팔레트의 이름·preview 개선이나 복사/분할 후 color-index 보존은 이 exact-RGB 시험을 대체하지 않는다.

## 4. AUD03 · 비활성 contract 확인과 toy 입력의 경계

### 4.1 먼저 확인할 고정 소스

```sh
git -C "$AF045_AUDACITY_REPO" show 16d52f63a4183bba77ef7305d14622958dc0d1d5:src/effects/NoiseReduction.cpp | rg -n -C 3 'SPECTRAL_SELECTION|#undef EXPERIMENTAL_SPECTRAL_EDITING|#ifdef EXPERIMENTAL_SPECTRAL_EDITING'
git -C "$AF045_AUDACITY_REPO" show e7d17d1bcedcb1fe75d78eb522de3b46476c94b7:src/effects/NoiseReduction.cpp | rg -n -C 3 'SPECTRAL_SELECTION|#undef SPECTRAL_EDIT_NOISE_REDUCTION|#ifdef SPECTRAL_EDIT_NOISE_REDUCTION'
git -C "$AF045_AUDACITY_REPO" show e7d17d1bcedcb1fe75d78eb522de3b46476c94b7 -- src/effects/NoiseReduction.cpp
```

모두 미실행 명령이다. 읽을 핵심은 두 판 모두 **L75–77의 지역 undef**를 갖는다는 점이다. 전역 flag 정의와 조건부 코드의 존재만으로 활성 기능이라고 판정하지 않는다. 첫 판은 EXPERIMENTAL_SPECTRAL_EDITING, 후속 판은 SPECTRAL_EDIT_NOISE_REDUCTION이라는 이름으로 NoiseReduction의 예외를 유지한다. 이 지침은 설정을 바꾸거나 빌드 우회를 수행하지 않는다.

지역 undef를 제거하거나 다른 컴파일 옵션으로 뒤집으면 원래 API와 다른 구현이 된다. 그러한 변경의 결과를 원판 실행 또는 이번 봉인 예측의 기존 구현 검증으로 보고할 수 없다. 새 연구에서 변경 구현을 다룬다면 별도 SHA·조건·관측 ID가 필요하다.

### 4.2 봉인된 계산 입력

| 항목 | 고정값 | 의미 |
| --- | --- | --- |
| Fs | 48,000Hz | 연구자 toy 입력 |
| N | 2,048 | 연구자 toy 변환 길이; 실제 NoiseReduction window 설정으로 확인한 값 아님 |
| bin 간격 | 23.4375Hz | Fs/N |
| 선택 Hz 범위 | [1,000, 2,000] | low bin42, exclusive high bin86로 대응 |
| 정상 bin | 64 = 1,500Hz | 두 toy 연산의 내부 |
| 경계 bin | 86 = 2,015.625Hz | hard-mask의 첫 외부 bin |
| A | bin42..85에 −6dB, 나머지0dB | 봉인된 가상 gain 연산 |
| B | A의 log-gain을 중심5bin 등가중 평균 | 선형 gain의 기하평균과 같은 toy kernel |

따라서 toy 계산상 정상 bin64는 A/B 모두 −6dB이고, 외부 bin86은 A=0dB, B=−2.4dB다. 이것은 신호·noise profile·window·overlap-add를 거친 역사 NoiseReduction의 실제 출력이 아니다. 실제 window가 N=2,048이고 실제 평활화가 이 5bin kernel이라고 추정하지 않는다. 현 수신 API에서 그 효과가 선택 주파수대를 실제로 소비하는지부터 확인해야 한다.

### 4.3 판단을 바꿀 최소 증거

필요한 최소 묶음은 다음과 같다.

1. 해당 효과에 주파수 경계를 전달하는 **명시적으로 정의된 구현**과 고정 SHA, 활성/비활성 설정.
2. 실제 sample rate, 분석 window 길이·종류, FFT 배치, overlap, noise profile 입력과 hash, sensitivity·감쇠·주파수 smoothing 등 모든 영향 설정.
3. 동일 입력에서 bin64와 bin86을 포함한 처리 전후 주파수 성분의 측정값, 처리 범위, 선택 외부 변화 및 시간영역 부작용.
4. 실제 알고리즘이 봉인 toy A/B와 같은 조작인지 확인하는 대응표.

현재 자료로는 이 묶음을 실행할 정확한 동일-API 명령이 없다. 임의로 활성화한 conditional branch나 일반 감쇠 필터를 NoiseReduction의 후속 시험으로 바꾸지 않는다.

## 5. 수용 원장에 연결할 기록

- 역사 실행0건, 새 실제 pipe 시험0건이다.
- 이 문서의 명령은 **재개 입력**이며 성공한 검사로 산입하지 않는다.
- Audacity3.6.0 릴리스(AUD-O360)는 PR6165와 같은 기능의 발표를 확인한다. 보수적 최소수 집계에서는 `minimum_count=false`, `duplicate_of=AUD-O6165`로 처리하고 원문·날짜·역할은 보존하는 편이 맞다. 해당 기능의 독립 실행 증거가 늘어난 것은 아니다. 이 문서는 canonical sources.jsonl을 수정하지 않았다.
- 앞선 outcome 원장 제안의 후속5저작은 이 보수 규칙에서4저작이다. 독립 비교 PR5653은 별도1저작이며, 채점·지원율은 변하지 않는다.
- 본 추가 작업에서 직접 연3개 고정 소스는 아래와 같다. 모두 재현 구문 확인용이며 최소 원문 수를 늘리지 않는다.

| 자료 ID | 원 주소·최종 주소 | 발행자·종류·판 | 확인 UTC·변경일 | 확인 위치·내용 | 한계·연결·산입 |
| --- | --- | --- | --- | --- | --- |
| AUD-RR01 | [요청 raw](https://raw.githubusercontent.com/audacity/audacity/0ffa73b9f44acc339e12a350edadd96590dc4b17/scripts/piped-work/pipe_test.py) · [최종 blob](https://github.com/audacity/audacity/blob/0ffa73b9f44acc339e12a350edadd96590dc4b17/scripts/piped-work/pipe_test.py) | Audacity, 실행 예제 소스, 0ffa73b9 | 2026-11-22T22:30:36.134Z; 도구 보고 변경일2020-09-29T15:34:14Z; 최초 발행일 미확인 | L10–11,21–30,50–65: 전제·pipe 이름·송수신 경계 | 프로그램 미실행. Q5/Q7·AUD01. 이미 읽은 수신 판의 보조 파일, minimum_count=false |
| AUD-RR02 | [요청 raw](https://raw.githubusercontent.com/audacity/audacity/0ffa73b9f44acc339e12a350edadd96590dc4b17/scripts/piped-work/pipeclient.py) · [최종 blob](https://github.com/audacity/audacity/blob/0ffa73b9f44acc339e12a350edadd96590dc4b17/scripts/piped-work/pipeclient.py) | Audacity, pipe CLI 소스, 0ffa73b9 | 2026-11-22T22:30:36.134Z; 도구 보고 변경일2022-06-21T08:31:47Z; 최초 발행일 미확인 | L14–36,262–302: stdin 명령·timeout·Q 종료 | 실제 바이너리 호환·실행 확인 아님. Q5/Q7·AUD01. minimum_count=false |
| AUD-RR03 | [요청 raw](https://raw.githubusercontent.com/audacity/audacity/0ffa73b9f44acc339e12a350edadd96590dc4b17/src/commands/SelectCommand.cpp) · [최종 blob](https://github.com/audacity/audacity/blob/0ffa73b9f44acc339e12a350edadd96590dc4b17/src/commands/SelectCommand.cpp) | Audacity, 선택 명령 소스, 0ffa73b9 | 2026-11-22T22:30:36.134Z; 도구 보고 변경일2023-11-17T11:43:14Z; 최초 발행일 미확인 | L53–77,104–140: Start/End/ProjectStart 인자와 시각 설정 | static source, 실행 아님. Q2/Q5/Q7·AUD01. minimum_count=false |

기존 판정·수량의 근거는 audacity-outcomes.json, audacity-outcome-sources.jsonl 및 audacity-outcome-notes.md와 함께 읽는다. 후속 실제 실행이 생기면 날짜·입력·판을 새 관측으로 덧붙여야 한다.
