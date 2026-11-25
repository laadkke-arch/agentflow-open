# 같은 입력으로 재실행

## 릴리스와 화면 준비

GitHub에서 `work/research-af-res-251`의 결과를 체크아웃하고 아래를 실행한다. Debian 13.6 x86-64의 시험에서는 다운로드한 AppImage 두 개를 사용자 쓰기 경로에서 풀고 각 `AppRun`을 실행했다. AppImage, ELF, 내장 SHA와 매뉴얼의 지문은 [3.4.2](receipts/release-3.4.2.json)와 [3.5.0](receipts/release-3.5.0.json)에 있다.

```bash
owned="$(git rev-parse --show-toplevel)/docs/workstreams/research/AF-RES-251"
trial="$(mktemp -d /workspace/scratch/af-res-251-replay.XXXXXX)"
for version in 3.4.2 3.5.0; do
    install_dir="$trial/$version"
    mkdir -p "$install_dir"
    (
        set -eu
        cd "$install_dir"
        filename="audacity-linux-$version-x64.AppImage"
        release="https://github.com/audacity/audacity/releases/download/Audacity-$version"
        curl -fSL "$release/CHECKSUMS.txt" -o CHECKSUMS.txt
        curl -fSL "$release/$filename" -o "$filename"
        tr -d '\r' < CHECKSUMS.txt |
            awk -v file="$filename" '$1 == file {print $3 "  " $1}' |
            sha256sum -c -
        sha256sum "$filename"
        chmod +x "$filename"
        ./"$filename" --appimage-extract >extract.stdout 2>extract.stderr
        sha256sum squashfs-root/bin/audacity
    ) || break
done
```

화면을 직접 조작할 수 있는 Linux 데스크톱에서도 아래 GUI 순서로 진행한다. 자동 조작은 1360×1020, Xfwm4 최대화, 영어 UI, 스케일 1과 GTK 스타일에서 캡처한 좌표를 쓴다. Xvfb와 xdotool이 없으면 Debian의 `xvfb_21.1.16-1.3+deb13u4_amd64.deb`, `xdotool_3.20160805.1-5.1_amd64.deb`, `libxdo3_3.20160805.1-5.1_amd64.deb`를 내려받아 `dpkg-deb -x 파일 "$trial/toolchain"`로 풀 수 있다. 실제 도구와 호스트 라이브러리의 지문은 [environment.txt](receipts/environment.txt)에 있다. [Debian xvfb 원경로](https://deb.debian.org/debian/pool/main/x/xorg-server/) · [Debian xdotool 원경로](https://deb.debian.org/debian/pool/main/x/xdotool/)

아래는 비어 있는 display 번호 `:71`에서의 Xvfb 예다. `Xvfb`, `xfwm4`, 앱은 각자 실행한 셸에서 유지하고 이후 명령에도 같은 `DISPLAY`와 `XAUTHORITY`를 적용한다. `Xvfb`가 풀린 패키지에 있으면 해당 실행 파일의 절대 경로를 쓴다. `:72` 등 다른 빈 번호는 버전별 격리에 쓸 수 있다.

```bash
export DISPLAY=:71 XAUTHORITY="$trial/xauthority"
touch "$XAUTHORITY"
chmod 600 "$XAUTHORITY"
xauth add "$DISPLAY" . "$(mcookie)"
Xvfb "$DISPLAY" -screen 0 1360x1020x24 -nolisten tcp -noreset -auth "$XAUTHORITY"
# 디스플레이가 열린 후 별도 셸
dbus-run-session xfwm4 --compositor=off
```

`launch_gui.sh`는 실행 환경의 `XDG_*`와 Audacity의 새 임시 파일 디렉터리를 지정하고, 두 디더를 `None`, 프로젝트를 44,100 Hz·16-bit로 초기화한다. 경로는 사용자가 소유한 쓰기 가능한 디렉터리를 쓴다. Debian 13에서 두 원본 ELF를 실행하기 위해 호스트 libmount, libselinux, Pango 라이브러리를 먼저 로드했다. 다른 배포판에서 기본 `AppRun`이 열리면 해당 호환 처리의 필요 여부와 플랫폼을 기록한다.

```bash
version=3.5.0  # 두 번째 셸에서는 3.4.2 및 해당 DISPLAY 선택
bash "$owned/launch_gui.sh" "$trial/$version/squashfs-root" \
    "$trial/profile-$version" "$trial/session-$version"
```

첫 실행에서 Welcome을 닫고 프로젝트를 최대화한다. App updates 안내가 보이면 확인 후 진행한다. `Help → About Audacity → Build Information`에서 릴리스와 커밋 앞 여섯 자리, `Edit → Preferences → Audio Settings`에서 44,100 Hz·16-bit PCM, `Quality`에서 실시간·고품질 Dither None을 확인한다.

## GUI 내보내기와 판독

1. 비어 있는 프로젝트에서 `File → Import → Audio`로 `fixtures/A.wav`, `File → Import → Labels`로 `fixtures/L.txt`, 오디오로 `fixtures/B.wav`, 라벨로 `fixtures/K.txt`를 차례로 연다. 3.5.0에서 Music Import의 프로젝트 템포 제안이 뜨면 **No**로 초 단위를 유지한다.
2. [SCOPE.md](SCOPE.md)의 한 조작만 적용한다. 위치 이동은 B 메뉴의 Move Track Up 한 번이다. 라벨 교환은 K를 두 번, B를 한 번 위로 이동해 `A · K · B · L`로 만든다. `Edit → Labels → Label Editor`의 범위 3개와 `project.png`의 순서, B 버튼, A 선택 및 커서 0을 확인한다. 효과는 빈 새 트랙에 추가한 것이 없고 gain/pan은 슬라이더 중앙이다.
3. 앱에서 `File → Export Audio`로 연다. 3.5.0의 위치 선택이 뜨면 **Export to computer**를 누른다. 새 출력 폴더, WAV (Microsoft), Mono, 44100 Hz, Signed 16-bit PCM, **Multiple Files → Labels**를 선택한다. `Using Label/Track Name`을 선택하고 첫 라벨 전 오디오, overwrite, trim을 끈다. Export를 눌러 완료 창의 경로와 개수를 캡처한다.
4. 프로젝트를 닫고 빈 프로젝트부터 반복한다. 대표 재실행은 별도 새 프로필과 폴더에 `base`를 한 번 더 내보낸다. 무음 대조는 같은 기본 배치에서 B의 WAV 내용만 `fixtures/Silence.wav`로 교체하고 파일명은 B.wav로 두며 mute는 끈다.

다음은 화면 조작 자동화의 실제 진입점이다. 패키지를 풀어 xdotool을 사용하는 경우에는 display와 패키지의 라이브러리 경로를 지정하여 `exec xdotool "$@"` 하는 실행 파일을 만들고 `--xdotool 그_절대_경로`를 준다. 모든 import 순서와 GUI 키·좌표를 JSON에 남긴다. 최종판 driver는 창 크기와 느린 Music Import를 확인한 뒤 다음 UI 입력을 보낸다.

```bash
python "$owned/gui_runs.py" "$version" "$trial/main-$version" \
    base-r1 move-b-r1 mute-b-r1 swap-labels-r1 \
    base-r2 move-b-r2 mute-b-r2 swap-labels-r2
# 새 프로필에서 앱을 다시 열고 별도 저장 경로 사용
python "$owned/gui_runs.py" "$version" "$trial/again-$version" base-r1 silent-b-r1

run="$trial/main-$version/base-r1"
rc=0
python "$owned/verify_wav.py" "$run/wav" >"$run/analysis.json" 2>"$run/analysis.stderr" || rc=$?
printf '%s\n' "$rc" >"$run/analysis.exit"
python "$owned/measure.py" --reference-dir "$owned/fixtures" "$run/wav/L13.wav"
ffprobe -v error -select_streams a:0 -show_streams -of json "$run/wav/L13.wav"
ffmpeg -v error -i "$run/wav/L13.wav" -map 0:a:0 -f s16le "$run/L13.pcm"
wc -c "$run/L13.pcm"
sha256sum "$run/L13.pcm" "$run/wav/L13.wav"
```

Python parser의 샘플 구역과 FFmpeg 디코딩의 해시를 맞춘다. ffprobe의 `duration_ts × time_base × sample_rate` 및 독립 PCM 바이트 수 ÷ `channels × 2`를 프레임 수에 대조한다. 위 예에서 L13.wav는 88,200 frames, 원 PCM의 176,400 bytes로 관측됐다. 파일 전체 지문은 WAV 헤더와 메타데이터도 포함한다. 실제 slice 판정의 창, 임계, 후보와 오차는 [SCOPE.md](SCOPE.md)와 각 `analysis.json`을 함께 본다.

## Inkscape 겹침 대조

```bash
mkdir -p "$trial/svg-config" "$trial/svg-cache"
export XDG_CONFIG_HOME="$trial/svg-config" XDG_CACHE_HOME="$trial/svg-cache"
inkscape --debug-info
inkscape --query-all "$owned/fixtures/overlap.svg"
inkscape "$owned/fixtures/overlap.svg" --export-type=png --export-dpi=96 \
    --export-background-opacity=0 --export-id=target --export-filename="$trial/bbox.png"
inkscape "$owned/fixtures/overlap.svg" --export-type=png --export-dpi=96 \
    --export-background-opacity=0 --export-id=target --export-id-only \
    --export-filename="$trial/isolated.png"
python - "$trial" <<'PY'
import sys
from pathlib import Path
from PIL import Image

root = Path(sys.argv[1])
with Image.open(root / "bbox.png") as raw_a, Image.open(root / "isolated.png") as raw_b:
    a, b = raw_a.convert("RGBA"), raw_b.convert("RGBA")
    assert a.size == b.size == (100, 80)
    for point in ((5, 5), (35, 19), (65, 52), (95, 75)):
        print(point, a.getpixel(point), b.getpixel(point))
    print(sum(a.getpixel((x, y)) != b.getpixel((x, y))
              for y in range(a.height) for x in range(a.width)))
PY
```

원본 두 PNG, stdout/stderr, 종료 코드 및 RGBA 원값은 [receipts/svg/](receipts/svg/)에 있다. 오디오 결과는 [runs.csv](runs.csv)의 GUI 출력 WAV에서 확인한다.
