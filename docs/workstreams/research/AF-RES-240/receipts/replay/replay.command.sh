#!/usr/bin/env bash
set -euo pipefail
p=/tmp/af-res-240-evidence
out="$p/replay"
checkout=/tmp/af-res-240-replay
base=11d5e186580c935640e214cac2a921e3176b67c3
git clone --no-tags --single-branch --branch work/research-af-res-240 \
    https://github.com/laadkke-arch/agentflow-open.git "$checkout"
git -C "$checkout" switch --detach "$base"
test -z "$(git -C "$checkout" status --porcelain)"
git -C "$checkout" rev-parse HEAD
owned="$checkout/docs/workstreams/research/AF-RES-240"
cd "$checkout"
py="$p/cpython-60403a5409ff2c3f3b07dd2ca91a7a3e096839c7/python"
for phase in main controls; do
    "$owned/run.sh" "$phase" "$py" "$p/icu-prefix" "$out/$phase"
    for kind in python-1 python-2 icu-1 icu-2; do
        for stream in stdout stderr; do
            cmp "$owned/receipts/$phase/$kind.$stream" "$out/$phase/$kind.$stream"
            sha256sum "$out/$phase/$kind.$stream"
        done
    done
done
"$owned/run.sh" tz "$py" "$p/icu-prefix" "$out/tz" "$p/tzbuild/with-backward"
for kind in python-tz icu-tz; do
    for stream in stdout stderr; do
        cmp "$owned/receipts/tz/$kind.$stream" "$out/tz/$kind.$stream"
        sha256sum "$out/tz/$kind.$stream"
    done
done
env -i PATH=/usr/bin:/bin LC_ALL=C TZ=UTC "$py" -I "$owned/probe.py" tz \
    --tzdir "$p/tzbuild/no-backward" >"$out/no-backward.stdout" 2>"$out/no-backward.stderr"
for stream in stdout stderr; do
    cmp "$owned/receipts/tz/no-backward.$stream" "$out/no-backward.$stream"
    sha256sum "$out/no-backward.$stream"
done
test -z "$(git status --porcelain)"
printf '%s\n' 'PASS: 11 stdout/stderr pairs byte-identical; fresh checkout remained clean.'
