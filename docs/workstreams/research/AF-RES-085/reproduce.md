# AF-RES-085 재현

## 역사판과 세 빌드

Debian 13 amd64에서 Python, Git, GCC 14, Make를 사용했다. Qt 5.15.15 모듈, CMake, Xvfb, xdotool은 081의 private package prefix 절차를 사용한다. 빌드 벤더의 네트워크 주소는 GitHub와 Debian archive다. `/tmp`의 짧고 서로 다른 경로는 QtSingleApplication의 Unix socket 이름 길이를 제한한다. 앱의 실행 파일은 share 자료 아래 상대 레이아웃과 compile-time install prefix를 참조한다. [세 빌드 지문](evidence/build/build-info.json)

연구 저장소 루트에서 다음을 실행한다.

```bash
set -euo pipefail
AF085_PACKET="$PWD/docs/workstreams/research/AF-RES-085"
AF085_TMP=$(mktemp -d /tmp/af085-repro.XXXX)
AF085_PIN=60d0c8a1c1ea20b4d5f9cf47ae9a24a627012cfc
git fetch origin "$AF085_PIN"
mkdir "$AF085_TMP/081"
git archive "$AF085_PIN:docs/workstreams/research/AF-RES-081" | tar -x -C "$AF085_TMP/081"
git init "$AF085_TMP/upstream"
git -C "$AF085_TMP/upstream" remote add origin https://github.com/musescore/MuseScore.git
git -C "$AF085_TMP/upstream" fetch --depth=2 --no-tags origin 16851045c9e50eafb016c5cf4f2733f974e841bf
git -C "$AF085_TMP/upstream" switch --detach f4fcf53ff65c56f0efb616a3af209d3faba9b342
"$AF085_TMP/081/tools/bootstrap_debian.sh" "$AF085_TMP/deps"
source "$AF085_TMP/deps/env.sh"
"$AF085_PACKET/fixtures/build_variants.sh" "$AF085_TMP/upstream" "$AF085_TMP/081" "$AF085_TMP/build" "$AF085_TMP/bin"
```

실측 빌드는 같은 cache에서 공통 호환 수정으로 먼저 U 타깃을 컴파일한 뒤 계측 소스를 적용했다. 이후 두 변형은 차이 파일을 각각 다시 컴파일하고 relink했다. G와 L은 같은 실행 파일에 함께 들어가지 않는다. probe는 `AF085_TRACE`에서 stdout에 JSON을 기록한다. 계측용 QTimer는 요청 파일을 읽고 모델과 현재 위젯의 좌표를 기록한다. 사용자 조작은 Qt action 호출용 API 없이 xdotool의 X11 키·좌표 입력으로 수행한다. `Note::scanElements` probe는 기존 tag 조건과 callback의 전후만 기록한다. [정확한 계측 위치](fixtures/probe/inject.py) · [모델 원장](fixtures/probe/model.h) · [화면 영역 수집기](fixtures/probe/ui.h)

## 기동과 메뉴

```bash
mkdir "$AF085_TMP/smoke"
for variant in U G L; do
  python -B "$AF085_PACKET/fixtures/replay.py" --binary "$AF085_TMP/bin/mscore-$variant" \
    --fixture "$AF085_PACKET/fixtures/x1.mscx" --case smoke --out "$AF085_TMP/smoke/$variant"
done
```

각 기동은 해당 fixture를 열고 초기 모델·화면을 읽는다. Startup Wizard와 Tour의 새 프로필 안내는 X11 클릭으로 닫는다. 측정 입력의 원 파일은 복사하여 사용한다. XDG 경로와 TMPDIR을 프로세스마다 격리하고 별도 Xvfb 1280×900에서 실행한다. X1/X2는 음+Shift 클릭으로 인접 두 보표를 선택한다. X3/X4에서만 역사판의 `-e`를 켠다. X3에서는 layer 상태 막대에서 hidden과 shown을 선택한다. `V`와 `6`은 원래 단축키다. 다음 절차의 좌표, 명령, 시각, 프로세스별 정상 종료 여부는 `steps.jsonl`과 `result.json`에 남는다.

```bash
mkdir "$AF085_TMP/runs"
for case in X1 X2 X3 X4; do
  case "$case" in
    X1) fixture=x1.mscx ;;
    X2) fixture=x2.mscx ;;
    X3|X4) fixture=layer.mscx ;;
  esac
  for variant in U G L; do
    for repeat in 1 2; do
      python -B "$AF085_PACKET/fixtures/replay.py" --binary "$AF085_TMP/bin/mscore-$variant" \
        --fixture "$AF085_PACKET/fixtures/$fixture" --case "$case" --out "$AF085_TMP/runs/$case-$variant-$repeat"
    done
  done
done
```

창의 요소가 보이는 방식은 원 화면 `*-shown.png`와 재생 단계별 캡처로 대조한다. 보라색, 파란색, 기본색 판정에는 view transform을 거친 `objects_on_screen`의 rect와 화면 픽셀을 함께 사용한다. 포인터 값은 해당 앱 프로세스 안에서만 따라가고 재열기 시 tick/track, pitch, 부모, 링크를 다시 대조한다. 뷰 재클릭이 추가된 단계는 접미사 `-R`이며, 주 실행의 별도 양성 대조다. `Ctrl+Z`는 해당 편집이 undo index를 올린 경우에만 입력한다. 저장 뒤 원 앱을 닫고 다른 프로세스로 같은 저장 bytes를 읽는다.
