# AF-RES-097 재현

GitHub 원본에 접근할 수 있는 Linux x86_64, Git, Python 3.12+, `uv`, `curl`, `unzip`, `sha256sum`으로 실행한다. 분석 프로세스와 Pillow child의 Python을 분리한다. 단계별 산출물은 별도 임시 디렉터리에 쓴다. 설치 URL·공식/실측 SHA-256·정확한 파일 경로는 [environment.json](environment.json), 각 실험 입력은 [inputs.json](inputs.json)에 있다.

```sh
set -eu
af097_dir=docs/workstreams/research/AF-RES-097
af097_root=$(mktemp -d /tmp/af-res-097-replay.XXXXXX)
export UV_CACHE_DIR="$af097_root/uv-cache"
export UV_PYTHON_INSTALL_DIR="$af097_root/uv-python"
uv python install 3.9.23 --no-bin
af097_python=$(uv python find --managed-python 3.9.23)
python -B - "$af097_dir" "$af097_root" "$af097_python" <<'PY'
import hashlib, json, pathlib, subprocess, sys, urllib.request

where, scratch = map(pathlib.Path, sys.argv[1:3])
config = json.loads((where / 'environment.json').read_text())
for version, row in config['versions'].items():
    wheel = row['wheel']
    data = urllib.request.urlopen(wheel['url'], timeout=60).read()
    assert len(data) == wheel['bytes']
    assert hashlib.sha256(data).hexdigest() == wheel['sha256_expected']
    path = scratch / wheel['filename']
    path.write_bytes(data)
    env = scratch / 'env' / version
    subprocess.run(['uv', 'venv', '--python', sys.argv[3], env], check=True)
    subprocess.run(['uv', 'pip', 'install', '--python', env / 'bin/python', '--no-index', '--no-deps', path], check=True)
PY
af097_gist=7389968dec0ac74f493d28ccd0f5f7b00e7ca8de
af097_gist_id=d98a4b54fb409bc8f745d169df0196fc
curl -fsSL "https://codeload.github.com/gist/$af097_gist_id/zip/$af097_gist" -o "$af097_root/issue5593.zip"
unzip -p "$af097_root/issue5593.zip" "$af097_gist_id-$af097_gist/indexed_with_transparency.png" > "$af097_root/indexed_with_transparency.png"
printf '%s  %s\n' 'a4fa91aa20ae6115d4c5520d11fc8e2f1a52a4d3df53860175a51eaa94ce12be' "$af097_root/indexed_with_transparency.png" | sha256sum -c
curl -fsSL 'https://raw.githubusercontent.com/python-pillow/Pillow/fdfa9e8521a0b9436a6324f652c323a2e3a0b21e/Tests/images/hopper.ppm' -o "$af097_root/hopper.ppm"
printf '%s  %s\n' '4c5f7cecc9d468eb37c886840d8f7e7824267e7e315d08751318efddb09a5efb' "$af097_root/hopper.ppm" | sha256sum -c
python -B "$af097_dir/run.py" inspect "$af097_root/indexed_with_transparency.png"
python -B "$af097_dir/run.py" execute calibration --env-dir "$af097_root/env" --output "$af097_root/calibration"
python -B "$af097_dir/run.py" execute experiment --env-dir "$af097_root/env" --input "$af097_root/indexed_with_transparency.png" --hopper "$af097_root/hopper.ppm" --output "$af097_root/experiment"
```

교정은 본 실험의 세 판과 보조 8.4.0에 대해 양성·음성 2종마다 PNG를 쓰고 새로 연다. `ledger.jsonl`의 8자리 모두 `exit_code=0`, `stage=observed`를 기대한다. 실험 원장 `kind=main`은 24자리다. 실험 명령의 종료 0은 원장 생성 성공이다. 각 실행의 오류·관측 여부는 `stage`, `exit_code`, `process`, 원 stdout/stderr로 판단한다. `rejected`의 `unsupported_call` 종료 2는 고의 대조다. 원 PNG와 Hopper는 각 child가 기대 바이트 SHA-256을 검증한다. 원본을 못 가져온 경우 `--input`을 빼면 본 실험 #5593의 12자리 및 그 추가 대조가 `not_run_input`으로 남고 다른 호출을 계속 실행한다. 원 PNG를 구성 입력으로 덮어쓸 경로는 없다.

`run.py`는 #5593 변환 대상과 입력 판독용 객체를 같은 bytes에서 별도로 연다. 변환 대상은 `Image.open`의 헤더를 읽은 상태로 유지한 후 바로 원 호출을 적용한다. 변환 전 인덱스의 실제 읽기는 판독용 객체에서 실행한다. #5595의 저장·재열기 행은 새 리스트와 새 이미지를 사용한 별도 프로세스다. 같은 객체의 순차 실행만 `sequential`로 표시한다. 각 프로세스는 `-I -B`에서 명시 경로의 Python으로 실행한다. 버전·코어·prefix가 맞지 않으면 호출 전에 멈춘다. 서로 다른 PID·시각·디렉터리는 동등한 픽셀 결과의 반복 비교에서 제외한다.

고정 테스트는 Pillow 소스 트리에서 실행한 pytest와 별개다. `hopper` 행은 고정 PPM과 helper의 경로를 써서 `P → implicit RGB` 두 번, `info['transparency']=0 → implicit` 순서를 연구 코드로 다시 실행한다. 8.4.0의 파일은 공식 배포판이며 #5594 커밋 자체를 빌드한 바이너리는 아니다. PNG 크기·바이트 해시는 인코더와 zlib가 같을 때 비교할 수 있다. mode·RGB·인덱스·alpha를 우선 확인한다. 원 배포판·GIF/Arrow/GDAL 테스트의 추가 실행 방법과 경계는 결과의 해당 절에 있다.

저장소 결과 커밋에서 별도로 실행하는 검사 명령은 다음과 같다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-097/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

원장과 관측을 비교하는 명령이다. 저장소 경로에 출력을 덮어쓰지 않는다. [새 환경에서 재생한 비교](evidence/replay.json)

```sh
python -B "$af097_dir/audit.py"
python -B "$af097_dir/audit.py" --replay-dir "$af097_root"
```
