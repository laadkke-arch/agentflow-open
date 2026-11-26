#!/bin/sh
# PR #9 첫 커밋(f1698015)의 엔진으로 시뮬레이션을 돌려 out/sim_v1.json을 쓴다.
# 엔진 세 파일만 임시 디렉터리로 꺼내고, 사례 자료(db/cases.py, fixtures, receipts)는 현재 것을 쓴다.
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
PIN=${PIN:-f1698015}
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
for f in ledger.py schema.sql project_schema.sql; do
  git -C "$HERE" show "$PIN:docs/design/final/db/$f" > "$TMP/$f"
done
python3 -I "$HERE/ops_sim.py" --engine "$TMP" --out "$HERE/out/sim_v1.json" --perf "$HERE/out/perf_v1.txt"
