#!/usr/bin/env bash
# Rebuild the evidence with a fresh local input directory.
set -euo pipefail

replay_out=${1:?usage: bash replay.sh ABSOLUTE_EMPTY_DIRECTORY [full|representative]}
replay_mode=${2:-representative}
case "$replay_out" in /*) ;; *) exit 2 ;; esac
case "$replay_mode" in full|representative) ;; *) exit 2 ;; esac
tools_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$replay_out"
test -z "$(find "$replay_out" -mindepth 1 -maxdepth 1 -print -quit)"
logdir="$replay_out/commands"
mkdir -p "$logdir" "$replay_out/npm"
cp "$tools_dir"/package{,-lock}.json "$replay_out/npm/"

step() {
    local label=$1 code=0
    shift
    printf '%q ' "$@" > "$logdir/$label.command"
    printf '\n' >> "$logdir/$label.command"
    "$@" > "$logdir/$label.stdout" 2> "$logdir/$label.stderr" || code=$?
    printf '%s\n' "$code" > "$logdir/$label.exit"
    cat "$logdir/$label.stdout"
    if [ "$code" -ne 0 ]; then cat "$logdir/$label.stderr" >&2; fi
    return "$code"
}

step prepare python -B "$tools_dir/prepare.py" "$replay_out"
step deps npm ci --prefix "$replay_out/npm" --cache "$replay_out/npm-cache" --registry https://registry.npmjs.org --ignore-scripts --no-audit --no-fund
step python-static python -B "$tools_dir/read_bytes.py" "$replay_out"
step node-static node "$tools_dir/read_bytes.mjs" "$replay_out"
step compare-static python -B "$tools_dir/compare_static.py" "$replay_out"
step fixtures python -B "$tools_dir/fixtures.py" "$replay_out"
step epub python -B "$tools_dir/read_epub.py" "$replay_out"
step validator node "$tools_dir/validate.mjs" "$replay_out"
if [ "$replay_mode" = full ]; then
    step browser-1 node "$tools_dir/browser.mjs" "$replay_out" 1
    step browser-2 node "$tools_dir/browser.mjs" "$replay_out" 2
    step summarize python -B "$tools_dir/summarize.py" "$replay_out"
    step compare python -B "$tools_dir/check_replay.py" "$tools_dir/.." "$replay_out" 1 2
else
    step browser-2 node "$tools_dir/browser.mjs" "$replay_out" 2 BoxTextured-G,BoxTextured-R,BoxTextured-O,Lamp-G,Lamp-R,Lamp-O,ktx-on,ktx-off,referenced-absent,external-absent,fallback-off
    step compare python -B "$tools_dir/check_replay.py" "$tools_dir/.." "$replay_out" 2
fi
