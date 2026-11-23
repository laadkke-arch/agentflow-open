# AF-RES-089 재현

역사판은 `f4fcf53ff65c56f0efb616a3af209d3faba9b342`, 태그 대신 가져올 병합은 `16851045c9e50eafb016c5cf4f2733f974e841bf`다. Debian 13.6 amd64, c++ 14.2, CMake 3.31.6, Qt 5.15.15에서 빌드했다. 원 실행의 build argv, package 판, 소스 및 바이너리 지문을 확인할 수 있다. [패치·fixture 출처](fixtures/SOURCES.md) · [빌드 원장](evidence/build/build-info.json) · [사전 봉인](https://github.com/laadkke-arch/agentflow-open/commit/a00648339b3bbda1eaac03bc23c7c7eb4e10cd42)

## 빈 폴더에서 G/L 빌드

[인계](HANDOFF.md)에 적힌 **결과 SHA**를 `AF089_RESULT`에 넣고 같은 Bash 세션에서 실행한다. apt 다운로드는 scratch 안에 Debian archive의 검증된 저장소를 사용한다. 별도 사용자 권한 설치는 필요 없다. ImageMagick `import`와 `xdpyinfo`는 당시 환경에 설치되어 있었다.

```bash
set -euo pipefail
AF089_TMP=$(mktemp -d /tmp/af089.XXXX)
AF089_REPO="$AF089_TMP/repo"
AF089_085=9ce697f2552133108861cc5504ed64722dfde427
AF089_081=60d0c8a1c1ea20b4d5f9cf47ae9a24a627012cfc
git clone --no-tags --single-branch --branch work/research-af-res-089 \
  https://github.com/laadkke-arch/agentflow-open.git "$AF089_REPO"
git -C "$AF089_REPO" switch --detach "${AF089_RESULT:?HANDOFF의 결과 SHA를 지정}"
git -C "$AF089_REPO" fetch --no-tags origin "$AF089_085" "$AF089_081"
AF089_PACKET="$AF089_REPO/docs/workstreams/research/AF-RES-089"
mkdir "$AF089_TMP/ref081" "$AF089_TMP/ref085"
git -C "$AF089_REPO" archive "$AF089_081:docs/workstreams/research/AF-RES-081" tools |
  tar -x -C "$AF089_TMP/ref081"
git -C "$AF089_REPO" archive "$AF089_085:docs/workstreams/research/AF-RES-085" fixtures |
  tar -x -C "$AF089_TMP/ref085"

git init "$AF089_TMP/upstream"
git -C "$AF089_TMP/upstream" remote add origin https://github.com/musescore/MuseScore.git
git -C "$AF089_TMP/upstream" fetch --depth=2 --no-tags origin 16851045c9e50eafb016c5cf4f2733f974e841bf
git -C "$AF089_TMP/upstream" switch --detach f4fcf53ff65c56f0efb616a3af209d3faba9b342
"$AF089_TMP/ref081/tools/bootstrap_debian.sh" "$AF089_TMP/deps"
source "$AF089_TMP/deps/env.sh"
"$AF089_PACKET/fixtures/build.sh" "$AF089_TMP/upstream" "$AF089_TMP/ref085" "$AF089_TMP/build" "$AF089_TMP/bin"
sha256sum "$AF089_PACKET/fixtures/"x{1,2}.mscx
```

경로·패키지 빌드 판·debug 정보가 새 바이너리 전체 해시에 영향을 줄 수 있다. 한 재현에서 G/L이 같은 소스판·옵션·키맵·공통 probe를 쓰는지 확인한다. `bin/logs/source-{G,L}.sha256` 사이에서 `element.cpp`와 `excerpt.cpp`만 달라야 한다. 이 둘의 차이는 패치 및 공통 계측 diff와 비교할 수 있다. [원 파일 지문 차이](evidence/build/file-hash-delta.diff)

## 같은 Xvfb 화면에서 4대조와 8메뉴

```bash
Xvfb -displayfd 3 -screen 0 1280x900x24 -dpi 96 -ac -nolisten tcp \
  3>"$AF089_TMP/display.txt" >"$AF089_TMP/xvfb.log" 2>&1 &
AF089_XVFB=$!
trap 'kill "$AF089_XVFB" 2>/dev/null || true' EXIT
for AF089_RETRY in $(seq 1 40); do
  [[ -s "$AF089_TMP/display.txt" ]] && break
  sleep 0.1
done
test -s "$AF089_TMP/display.txt"
AF089_SCREEN=":$(cat "$AF089_TMP/display.txt")"
for AF089_PHASE in controls main; do
  python -B "$AF089_PACKET/fixtures/run.py" --af085 "$AF089_TMP/ref085" \
    --bin "$AF089_TMP/bin" --display "$AF089_SCREEN" --out "$AF089_TMP/runs" --phase "$AF089_PHASE"
done
```

각 실행과 각 재열기는 새 XDG 프로필이다. 메뉴 경로는 첫 C4 클릭, 아래 Oboe 쉼표 Shift 클릭, Tools → Explode 및 해당 창에서 V다. 양성은 같은 수동 범위, 음성은 Esc로 비운 선택을 값의 기준으로 삼는다. `steps.jsonl`의 X11 단계와 `app.jsonl`의 GUI action, 모델 command 진입, 순회 대상 및 undo 경계를 함께 대조한다. V로 실값을 바꾸고 오직 그 macro만 추가됐을 때 `Ctrl+Z`를 한 번 보낸다. 편집 후와 undo 후의 직렬화는 개별 파일로 두고 각각 별도 프로세스로 연다. 복제 전후의 주소는 같은 프로세스 안에서만 쓰고, 재열기에는 master/part·track·tick·종류·pitch·링크 키를 쓴다. [실행 명령과 종료값](runs.jsonl)

## Q6 보조 재현과 검산

동일한 Xvfb 화면에서 F6으로 Selection Filter를 열어 Voice 1 체크박스의 좌표를 확인한다. 원 실행은 [보조 화면](evidence/aux/filter-geometry/filter.png)의 60 664를 썼다. 레이아웃이 다르면 화면에서 맞는 좌표를 읽어 해당 입력값을 바꾼다. F-P/F-X는 X1의 다른 프로필, PEER/VV는 X2의 다른 프로필에서 실행한다.

```bash
python -B "$AF089_PACKET/fixtures/run_aux.py" --af085 "$AF089_TMP/ref085" \
  --bin "$AF089_TMP/bin" --display "$AF089_SCREEN" --out "$AF089_TMP/aux" --voice1 60 664

cd "$AF089_REPO"
python -B "$AF089_PACKET/fixtures/write_runs.py" --out "$AF089_TMP/committed-runs.jsonl"
cmp "$AF089_TMP/committed-runs.jsonl" "$AF089_PACKET/runs.jsonl"
python -B "$AF089_PACKET/fixtures/verify.py" --out "$AF089_TMP/committed-verify.json"
cmp "$AF089_TMP/committed-verify.json" "$AF089_PACKET/evidence/verify.json"
python -B -m workbench.session check "$AF089_PACKET/manifest.json" --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

새 GUI 실행의 시각·주소는 달라진다. 새 실행은 `result.json`과 재열기 `app.jsonl`의 대응 키 및 저장값으로 비교한다. 마지막 명령 묶음은 저장소의 **커밋된 원자료**에서 지문과 정식·보조 판정을 다시 계산한다. 원 실행 재현에서 수집 파일은 `collect.py --raw <새 실행 폴더> --dest <새 출력 경로> --phase controls|main|auxiliary`로 뽑을 수 있다. [검산 코드](fixtures/verify.py)
