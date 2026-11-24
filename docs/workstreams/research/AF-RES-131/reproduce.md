# AF-RES-131 재현

GitHub에서 고정 결과 SHA를 가진 `work/research-af-res-131`을 받아 저장소의 과제 폴더에서 실행한다. 측정에 사용한 Python 3.12.14, Node 24.22.1, npm 11.9.0, Chromium 156.0.8078.79와 설치 모듈·bundle 지문을 [브라우저 환경](evidence/browser/environment-main.json)에 남겼다. Chromium은 Unix socket 경로 제한 때문에 표준 짧은 임시 경로를 쓴다. 영구 출력과 npm cache는 과제 폴더 아래에 둔다.

## 지정한 npm 판과 브라우저 입력

```sh
mkdir -p .scratch
af131_run=$(mktemp -d "$PWD/.scratch/replay.XXXXXX")
npm --cache "$af131_run/npm-cache" --prefix fixture ci --no-audit --no-fund --registry https://registry.npmjs.org/
env -u TMPDIR node replay/drive.mjs --mode all --out "$af131_run/raw" --chromium /usr/bin/chromium
python -B replay/summarize.py --evidence "$af131_run/raw" --output "$af131_run/runs.jsonl"
python -B replay/compare.py --reference evidence/browser --candidate "$af131_run/raw" --report "$af131_run/compare.json"
python -B replay/audit.py --report "$af131_run/recount.json"
```

`--mode all`은 본 48, 배경·클릭 16, 보충 12, 래퍼 없는 정착 8을 새 컨텍스트에 보낸다. `main`, `controls`, `supplement`, `bare`도 지원한다. 실제 pointer 입력과 결과를 각 JSON에 쓰므로 출력 폴더는 새 위치로 지정한다. `compare.py`는 raw 이벤트, 좌표·호출·반환·순서, 초기 화면 SHA, 실제 bundle·환경의 지문을 비교한다. 시각은 리플레이 비교에서 따로 유지하고 browser 경고 수도 별도로 센다. [입력](fixture/input.json) · [실행 순서](fixture/cases.json) · [버전 핀](fixture/versions.json)

## 깨끗한 두 checkout 및 저장소 검사

이 과제 폴더에서 `AF131_RESULT_SHA`를 [수용 영수증](evidence/acceptance/RECEIPT.md)의 40자리 결과 SHA로 설정한다. 두 경로는 각각 별도 Git 저장소와 cache를 준비한다. A는 과제 브랜치 clone 뒤 detach, B는 빈 저장소에서 결과 SHA 한 개만 shallow fetch 한다. A가 고정 SHA에서 명시 세션과 공통 검사를 실행한다.

```sh
af131_verify=$(mktemp -d "$PWD/.scratch/verify.XXXXXX")
bash replay/accept.sh "$AF131_RESULT_SHA" "$af131_verify/route-a" clone
bash replay/accept.sh "$AF131_RESULT_SHA" "$af131_verify/route-b" fetch-sha
python -B replay/compare.py --reference "$af131_verify/route-a/run" --candidate "$af131_verify/route-b/run" \
  --reference-commit "$AF131_RESULT_SHA" --commit "$AF131_RESULT_SHA" --report "$af131_verify/cross.json"
```

공통 검사를 따로 실행할 때는 받은 결과 SHA로 checkout한 **저장소 루트**를 쓴다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-131/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

Git에서 읽은 날짜와 명령의 stdout·stderr·exit는 확인할 SHA가 같은지 먼저 대조한다.

## 공개판 모집, 소스 분기 비교

고정한 cutoff는 2026-11-24T10:04:35Z다. 아래 packument는 재실행 시점의 응답이며 살아 있는 버전과 시각을 다시 확인하는 입력이다. 원 관측 당시의 고정 목록은 [첫 커밋의 releases.csv](https://github.com/laadkke-arch/agentflow-open/blob/6c5dd2b08dfec7fd0888d3b73bce856739e17a6c/docs/workstreams/research/AF-RES-131/releases.csv)다. 최신 응답의 지문이 최초 관측과 다르면 [모집 영수증](evidence/roster.json)의 날짜와 함께 남긴다.

```sh
af131_sources=$(mktemp -d "$PWD/.scratch/source.XXXXXX")
curl -fsSL --compressed https://registry.npmjs.org/ol -o "$af131_sources/ol.json"
git clone --filter=blob:none --no-checkout https://github.com/openlayers/openlayers.git "$af131_sources/openlayers"
python -B replay/roster.py "$af131_sources/ol.json" --cutoff 2026-11-24T10:04:35Z \
  --output "$af131_sources/roster.csv" --prereleases "$af131_sources/prereleases.csv"
python -B replay/release_artifacts.py "$af131_sources/roster.csv" --upstream "$af131_sources/openlayers" \
  --cache "$af131_sources/tarballs" --output "$af131_sources/artifacts.csv"
python -B replay/release_rules.py "$af131_sources/artifacts.csv" --upstream "$af131_sources/openlayers" \
  --cache "$af131_sources/tarballs" --output "$af131_sources/releases.csv" --receipt "$af131_sources/rules.json"
python -B replay/lineage_probes.py "$af131_sources/ol.json" --cache "$af131_sources/tarballs" > "$af131_sources/lineage.json"
diff -u releases.csv "$af131_sources/releases.csv"
```

동일한 소스 구조를 판정하는 보조 정규식은 commit과 tarball의 constructor 및 hit 함수 구조를 재집계한다. 다른 구조는 미판독으로 바꾸고 해당 줄을 직접 읽는다. [독립 배포·Git 시간과 반증](evidence/release-history.md)

## QGIS와 Audacity 별도 재현

측정한 디스플레이는 Debian Xvfb 21.1.16과 1200×780×24다. 같은 출력에서 [QGIS](evidence/cross-domain/qgis.stdout.log)는 memory 레이어만 다루고 [Audacity](evidence/cross-domain/audacity.stdout.log)는 합성 음원만 사용한다. 가상 디스플레이의 `-displayfd` 출력으로 `AF131_DISPLAY`를 설정한다. 적격 바이너리와 입력 지문은 [분야 환경](evidence/cross-domain/environment.json)에 있다.

```sh
mkdir -p .scratch/desktop
Xvfb -displayfd 1 -screen 0 1200x780x24 -nolisten tcp -ac > .scratch/desktop/display
```

Xvfb를 실행한 상태에서 다른 셸의 과제 폴더에서 QGIS를 실행한다. 검사항목은 script가 만든 두 memory layer의 활성 상태, 선택, 편집 가능 여부, Move Feature의 두 클릭 후 좌표다.

```sh
AF131_DISPLAY=:$(cat .scratch/desktop/display)
mkdir -p .scratch/desktop/qgis .scratch/desktop/qgis-cache
install -d -m 700 .scratch/desktop/qgis-runtime
DISPLAY="$AF131_DISPLAY" XDG_CACHE_HOME="$PWD/.scratch/desktop/qgis-cache" \
  XDG_RUNTIME_DIR="$PWD/.scratch/desktop/qgis-runtime" qgis --nologo --noplugins --noversioncheck \
  --profiles-path "$PWD/.scratch/desktop/qgis" --profile af131 --code "$PWD/replay/qgis_move.py"
```

Audacity는 [공식 3.7.5 Linux asset](https://github.com/audacity/audacity/releases/expanded_assets/Audacity-3.7.5)과 script-pipe 모듈을 쓴다. 새 전용 설정에서 시작 화면을 닫고 Modules의 mod-script-pipe를 Enabled로 바꾼 뒤 재시작한다. 이 테스트는 합성 파일을 새 프로그램에서 열며, 독립된 Audacity script pipe를 사용한다. 추출한 AppRun을 사용하면 시스템 설치를 생략할 수 있다.

```sh
af131_audio="$PWD/.scratch/desktop/audio"
AF131_DISPLAY=:$(cat .scratch/desktop/display)
mkdir -p "$af131_audio/config" "$af131_audio/cache" "$af131_audio/data" "$af131_audio/tmp"
install -d -m 700 "$af131_audio/runtime"
curl -fsSL 'https://github.com/audacity/audacity/releases/download/Audacity-3.7.5/audacity-linux-3.7.5-x64-22.04.AppImage' \
  -o "$af131_audio/audacity.AppImage"
printf '%s  %s\n' aa092571e6447b3e82d8cf6b9e31ee4907581e4925b791f49c8563e1cfa93716 "$af131_audio/audacity.AppImage" | sha256sum -c
chmod +x "$af131_audio/audacity.AppImage"
(cd "$af131_audio" && ./audacity.AppImage --appimage-extract)
python -B replay/audacity_pointer.py --tone "$af131_audio/af131-tone.wav"
env -u APPIMAGE DISPLAY="$AF131_DISPLAY" XDG_CONFIG_HOME="$af131_audio/config" \
  XDG_CACHE_HOME="$af131_audio/cache" XDG_DATA_HOME="$af131_audio/data" \
  XDG_RUNTIME_DIR="$af131_audio/runtime" TMPDIR="$af131_audio/tmp" \
  "$af131_audio/squashfs-root/AppRun" "$af131_audio/af131-tone.wav"
```

또 다른 셸에서 같은 위치와 디스플레이를 설정하고 `--calibrate` 이미지를 열어 동일한 포인터 위치를 확인한다. 실제 XTest 드래그를 보낸 뒤 GetInfo JSON과 Selection Toolbar 이미지를 읽는다. clip 위치는 1ms 오차로 비교한다. 디스플레이 크기나 GTK 테마가 다르면 calibrate 이미지에서 핸들과 파형 y를 맞춘다.

```sh
af131_audio="$PWD/.scratch/desktop/audio"
AF131_DISPLAY=:$(cat .scratch/desktop/display)
DISPLAY="$AF131_DISPLAY" python -B replay/audacity_pointer.py --calibrate "$af131_audio/calibrate.png"
DISPLAY="$AF131_DISPLAY" python -B replay/audacity_pointer.py --output "$af131_audio/observations" \
  --x 380 --end-x 600 --handle-y 221 --waveform-y 274
```

[분야의 원전, 동작과 적용 한계](evidence/cross-domain/README.md)
