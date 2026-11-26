#!/bin/sh
# 기존 갈림안(work/design-gallim@fc68f0d1)을 고정 입력으로 다시 돌린다.
# 사용: sh docs/workstreams/design/gallim-review/probes/run.sh
# 필요: python3 3.11+, git. LOD 탐침은 node 18+와 npm 네트워크 접근이 추가로 필요하다.
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(git -C "$HERE" rev-parse --show-toplevel)
PIN=fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
git -C "$REPO" fetch -q origin work/design-gallim 2>/dev/null || true
git -C "$REPO" archive "$PIN" docs/workstreams/design/gallim | tar -x -C "$TMP"
G="$TMP/docs/workstreams/design/gallim"
OUT="$HERE/out"
mkdir -p "$OUT"
python3 -I -B -c "import sys; sys.path.insert(0, sys.argv[1]); import roundtrip; roundtrip.main()" "$G/db" > "$OUT/p0_roundtrip.json"
python3 -I -B "$HERE/p1_jobs.py" "$G/db" > "$OUT/p1_jobs.txt"
python3 -I -B "$HERE/p2_other.py" "$G/db" > "$OUT/p2_other.txt"
python3 -I -B "$HERE/p3_catalog.py" "$G/db" > "$OUT/p3_catalog.txt"
python3 -I -B "$HERE/p4_toyota.py" "$G" "$REPO" > "$OUT/p4_toyota.txt"
python3 -I -B "$HERE/p5_ablate.py" "$G" "$REPO" > "$OUT/p5_ablate.txt"
python3 -I -B "$HERE/p6_crowd.py" "$G/db" > "$OUT/p6_crowd.txt"
python3 -I -B "$HERE/p7_delete_stage2.py" "$G/db" "$HERE" > "$OUT/p7_delete_stage2.txt"
python3 -I -B "$HERE/p8_r1.py" "$G/db" "$REPO" > "$OUT/p8_r1.txt"
python3 -I -B "$HERE/p9_evalx1.py" "$G/db" "$REPO" > "$OUT/p9_evalx1.txt"
if command -v npm >/dev/null 2>&1; then
  L="$TMP/lod"; mkdir -p "$L"; cp "$HERE/lod/package.json" "$HERE/lod/run_lod.mjs" "$L/"
  (cd "$L" && npm install -s --no-audit --no-fund >/dev/null && node run_lod.mjs) > "$HERE/lod/lod_runtime.json"
fi
echo "outputs in $OUT"
