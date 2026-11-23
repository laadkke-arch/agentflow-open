# AF-RES-081 재현

## 핀과 준비

실험 코어는 MuseScore PR #4590 첫 부모 `f4fcf53ff65c56f0efb616a3af209d3faba9b342`다. `G-global-selection.patch`는 실제 병합과 첫 부모의 element.cpp diff다. `L-excerpt-selection.patch`는 연구용이다. 세 native 타깃은 같은 계측과 같은 GCC 호환 변경을 적용한다. 빌드에 쓴 정확한 명령, 라이브러리 경로, 플래그, 바이너리와 패치 지문, 기동 stdout/stderr는 [build-info](evidence/build/build-info.json)에 있다.

빌드에 Debian 13.6 amd64, GCC/G++ 14.2, CMake 3.31.6, Qt 5.15.15, Unix Makefiles, 네 병렬 작업을 썼다. GCC 14가 거절한 DTL의 미호출 `enableTrivial()`의 `const`를 공통으로 제거했다. Qt 개발 패키지는 private prefix에 풀고 호스트의 같은 Qt 5.15.15 런타임과 data/plugins를 참조했다. Ninja의 `all.h`/AUTOMOC 순환 및 private prefix의 Qt 플러그인 경로를 복구한 로그도 보존했다. 스타일 데이터는 pin의 `share/styles`다. [빌드와 실패·복구 원 로그](evidence/build/)

`AF081_BASE`는 이 GitHub 저장소의 루트다. Debian 13 Cloud 이미지에서 이미 설치된 GCC, make, Git, Qt runtime과 Python 3.12 이상을 사용한다. `bootstrap_debian.sh`는 이 이미지용이다. 다른 OS에서는 Qt5 개발 모듈과 audio/compression 헤더, CMake, GCC를 OS의 패키지 관리자로 제공할 수 있다.

```bash
set -euo pipefail
AF081_BASE="$PWD"
AF081_PACKET="$AF081_BASE/docs/workstreams/research/AF-RES-081"
AF081_TMP=$(mktemp -d -t af-res-081-replay.XXXXXXXX)
git init "$AF081_TMP/upstream"
git -C "$AF081_TMP/upstream" remote add origin https://github.com/musescore/MuseScore.git
git -C "$AF081_TMP/upstream" fetch --depth=2 --no-tags origin \
  16851045c9e50eafb016c5cf4f2733f974e841bf \
  06a66a2206fc5f3c2c33d7ee4123badf496bc4dd \
  refs/tags/v3.0:refs/tags/v3.0 refs/tags/v2.3.2:refs/tags/v2.3.2
git -C "$AF081_TMP/upstream" switch --detach f4fcf53ff65c56f0efb616a3af209d3faba9b342
git -C "$AF081_TMP/upstream" diff 16851045c9e50eafb016c5cf4f2733f974e841bf^1 \
  16851045c9e50eafb016c5cf4f2733f974e841bf -- libmscore/element.cpp \
  | cmp - "$AF081_PACKET/patches/G-global-selection.patch"
"$AF081_PACKET/tools/bootstrap_debian.sh" "$AF081_TMP/deps"
source "$AF081_TMP/deps/env.sh"
"$AF081_PACKET/tools/build_variants.sh" "$AF081_TMP/upstream" "$AF081_TMP/build" "$AF081_TMP/bin"
```

`build_variants.sh`가 시작할 때 source는 clean이고 두 출력 경로는 새로 만든다. 동일 build 디렉터리에서 U를 컴파일한 뒤 G용 element.cpp와 L용 excerpt.cpp를 각기 다시 컴파일하고 relink했다. G/L 패치를 동시에 적용하지 않았다. 재현 시 absolute path 또는 toolchain package revision이 바뀌면 binary의 SHA가 달라질 수 있다. 정확한 패치 입력과 모델 관측의 동등성을 검산할 때 기록된 원 바이너리 SHA도 함께 읽는다. [소스 revision](evidence/upstream-revisions.txt) · [호스트 패키지](evidence/build/host-package-versions.tsv) · [다운로드 패키지](evidence/build/downloaded-debs.tsv)

## 여섯 조작과 표

```bash
python -B "$AF081_PACKET/tools/run_matrix.py" --binaries "$AF081_TMP/bin" --out "$AF081_TMP/matrix"
python -B "$AF081_PACKET/tools/compare.py" --root "$AF081_TMP/matrix" --format markdown
python -B "$AF081_PACKET/tools/compare.py" --root "$AF081_PACKET" --format json > "$AF081_TMP/recorded-states.json"
python -B "$AF081_PACKET/tools/compare.py" --root "$AF081_PACKET" --format markdown
python -B "$AF081_PACKET/tools/verify.py" --replay "$AF081_TMP/matrix"
```

`run_matrix.py`는 셀 순서 01–18, 반복 1·2에 대해 시작 시 비어 있는 cwd와 독립 Qt/XDG 환경으로 실행한다. `runs.jsonl` 각 행에 argv, 입력 SHA, binary SHA, exit, stdout/stderr 및 저장 악보 경로·크기·SHA가 있다. 생성 직후는 `createExcerpt`나 `cloneVoice`가 반환하고 `endCmd`가 호출되기 전이다. 별도 endCmd 행도 남겼다. E04는 P2 편집→P1 편집→한 번 undo, E05는 비링크 성부 복사, E06은 직접 mark setter의 통제다. 전용 계측의 observation은 읽기 전용이고 조작·fixture 준비는 그 앞의 별도 test driver 호출이다.

`compare.py`는 저장된 raw JSON의 score 및 object pointer로 실제 목록과 link peer를 다시 찾아 위치 키로 바꾼다. MSCX를 별도로 열어 음 높이와 link marker를 재열림 결과와 대조한다. 원본 주소는 증거에 남는다. 비어 있던 값, 읽을 수 없는 값, 실행되지 않은 조작은 구분한다. 원 시험과 화면 결과를 이 분모에 넣지 않는다. 전체 검산은 [SELF_CHECK](SELF_CHECK.md)의 `tools/verify.py`를 사용한다.

## 당시 기존 mtest

당시 [README](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/mtest/README.md)는 debug 빌드/설치 후 mtest 폴더에서 CTest를 호출한다. [등록 규칙](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/mtest/cmake.inc#L83)은 `-xunitxml -o result.xml`을 전달한다. [Travis job](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/build/travis/job1_Tests/run_tests.sh#L10)의 xVfb 명령과 현재의 offscreen 명령을 구분한다. [보존된 과거 CI 조회](evidence/original-ci.json)는 원 job 실행 0건 확보를 뜻한다.

다음은 Unix Makefiles build 디렉터리의 original target을 실행하는 명령이다. 처음에는 U target이 들어 있다. G 또는 L에서는 임시 upstream에 해당 패치만 `git apply`하고 아래 두 명령을 반복한 뒤 같은 패치를 `git apply --reverse`한다. 각 suite의 `result.xml`을 별도 위치에 보존하고 다음 빌드로 넘어간다.

```bash
cmake --build "$AF081_TMP/build" --parallel 4 --target \
  tst_parts tst_links tst_element tst_exchangevoices tst_readwriteundoreset \
  tst_implodeExplode tst_copypaste
QT_QPA_PLATFORM=offscreen LC_ALL=C.UTF-8 ctest --test-dir "$AF081_TMP/build/mtest" \
  --output-on-failure -j2 \
  -R '^(tst_parts|tst_links|tst_element|tst_exchangevoices|tst_readwriteundoreset|tst_implodeExplode|tst_copypaste)$'
```

현재 실측은 7×3 CTest targets, 각 suite의 QTest XML은 [원시험 출력](evidence/original/)에 있다. 파일·시험 소스와 linked edits가 맞물리는 위치는 [출처 원장](sources.jsonl)을 따른다. [v3.0.1 릴리스](https://github.com/musescore/MuseScore/releases/tag/v3.0.1)의 공식 ZIP과 GitHub 생성 source의 revision 차이를 확인했고, ZIP 접근은 실패했다. Git은 정확한 tag와 parent를 내려 주었다. [Debian Bookworm](https://packages.debian.org/bookworm/musescore3)은 3.2.3이므로 독립 패키징 참고로 썼다. 3.0/2.3.2 신고자의 설치물과 대응하는 fingerprint는 확인하지 못했다. [접근 시도](evidence/access-attempts.jsonl)

## 화면 보조 재현

이 층의 fixture SHA는 같다. File → Parts → New All에서 두 파트를 한 번에 만들고 Flute 및 Oboe 탭을 열었다. 모델 매트릭스 E01은 P2를 먼저 만든다. 실제 창의 Inspector와 음표 pixels를 각 증거로 보존했다. 프로그램 모델의 목록·link 판독은 native probe에서 수행했다.

같은 임시 checkout와 build에 [desktop 전용 compatibility patch](patches/common-desktop-qt.patch)를 추가한다. Qt의 새 enum stream overload와 충돌하던 세 설정 enum은 원 int serialization을 유지하는 구체 overload를 쓴다. LAME을 끈 상태에서 정의되지 않은 unused-variable 참조도 고쳤다. 이 수정은 matrix 바이너리 및 original suite 실행과 별도다. 화면에는 Xvfb, xdotool, ImageMagick `import`가 필요하다.

```bash
git -C "$AF081_TMP/upstream" apply "$AF081_PACKET/patches/common-desktop-qt.patch"
mkdir "$AF081_TMP/desktop-bin"
for variant in U G L; do
  variant_patch=''
  case "$variant" in
    G) variant_patch="$AF081_PACKET/patches/G-global-selection.patch" ;;
    L) variant_patch="$AF081_PACKET/patches/L-excerpt-selection.patch" ;;
  esac
  if [[ -n "$variant_patch" ]]; then
    git -C "$AF081_TMP/upstream" apply "$variant_patch"
  fi
  cmake --build "$AF081_TMP/build" --parallel 4 --target mscore workspaces
  cp "$AF081_TMP/build/mscore/mscore" "$AF081_TMP/desktop-bin/mscore-$variant"
  if [[ -n "$variant_patch" ]]; then
    git -C "$AF081_TMP/upstream" apply --reverse "$variant_patch"
  fi
done
for resource in workspaces instruments templates themes tours wallpaper; do
  cp -a "$AF081_TMP/upstream/share/$resource" "$AF081_TMP/build/install/share/mscore-3.1/"
done
cp "$AF081_TMP/build/share/workspaces/"*.workspace "$AF081_TMP/build/install/share/mscore-3.1/workspaces/"
for variant in U G L; do
  for repeat in 1 2; do
    "$AF081_PACKET/tools/replay_desktop.sh" "$AF081_TMP/desktop-bin/mscore-$variant" \
      "$AF081_PACKET/fixtures/two-parts.mscx" "$AF081_TMP/desktop-$variant-$repeat"
  done
done
```

[화면 원 캡처와 입력·명령](evidence/desktop/) · [픽셀 검산](evidence/desktop-pixels.json) · [GUI 실패와 복구](evidence/desktop-prep/). 고정 1280×900 Xvfb에서 window manager 없이 실행했다. `desktop-pixels.json`의 사각형은 글씨와 title frame을 피한 음표 픽셀 영역이다. RGB에서 B>R+55 및 B>G+28을 만족하는 픽셀을 센다. 사람이 이미지의 악기 탭과 Inspector를 대조했다.
