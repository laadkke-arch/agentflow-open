#!/usr/bin/env bash
# E01 supplemental GUI path. Requires Xvfb, xdotool, and ImageMagick import.
set -euo pipefail
if [[ $# != 3 ]]; then
    echo 'usage: replay_desktop.sh MSCORE SYNTHETIC_SCORE NEW_OUTPUT_DIR' >&2
    exit 2
fi
binary=$(realpath "$1")
score=$(realpath "$2")
output=$(realpath -m "$3")
mkdir "$output"
cd "$output"
mkdir -m 700 runtime
export QT_QPA_PLATFORM=xcb LC_ALL=C.UTF-8 XDG_RUNTIME_DIR="$PWD/runtime"
export XDG_CONFIG_HOME="$PWD/config" XDG_DATA_HOME="$PWD/data" XDG_CACHE_HOME="$PWD/cache"

Xvfb -displayfd 3 -screen 0 1280x900x24 -ac -nolisten tcp \
    3>display.txt >xvfb.stdout 2>xvfb.stderr &
display_pid=$!
app_pid=
cleanup() {
    if [[ -n "$app_pid" ]]; then kill "$app_pid" 2>/dev/null || true; fi
    kill "$display_pid" 2>/dev/null || true
}
trap cleanup EXIT
for attempt in {1..60}; do
    if [[ -s display.txt ]]; then break; fi
    sleep 0.1
done
export DISPLAY=":$(cat display.txt)"
printf '%s start %s\n' "$(date -u +%FT%TZ)" "$DISPLAY" > steps.txt
sha256sum "$binary" "$score" > inputs.sha256
"$binary" --no-synthesizer "$score" >stdout.txt 2>stderr.txt &
app_pid=$!

click() {
    printf '%s click %s %s %s\n' "$(date -u +%FT%TZ)" "$1" "$2" "$3" >> steps.txt
    xdotool mousemove "$1" "$2" click 1
}

wait_for_window() {
    local pattern="$1"
    for attempt in {1..100}; do
        if xdotool search --onlyvisible --name "$pattern" >/dev/null 2>&1; then return; fi
        if ! kill -0 "$app_pid" 2>/dev/null; then return 1; fi
        sleep 0.1
    done
    printf 'window not found: %s\n' "$pattern" >&2
    return 1
}

screenshot() {
    xdotool mousemove 615 451
    sleep 0.25
    import -window root "$1"
}

wait_for_window '^Startup Wizard$'
click 826 566 'Cancel startup wizard'
wait_for_window '^Tour$'
click 419 360 'Disable tours'
click 829 397 'Close tour'
wait_for_window 'MuseScore 3 .*two-parts'
click 369 327 'Select master Flute C4'
screenshot master-selected.png
click 70 10 'File'
click 105 365 'Parts'
wait_for_window '^Parts$'
screenshot parts-dialog.png
click 924 175 'New All'
sleep 0.3
click 850 676 'OK'
sleep 0.4
click 333 149 'Open Flute tab without selecting a note'
screenshot flute.png
click 388 149 'Open Oboe tab without selecting a note'
screenshot oboe.png
xdotool key --clearmodifiers ctrl+q
wait_for_window '^MuseScore$'
click 635 384 'Discard changes to the synthetic score'
set +e
wait "$app_pid"
code="$?"
app_pid=
printf '%s exit %s\n' "$(date -u +%FT%TZ)" "$code" >> steps.txt
printf '%s\n' "$code" > exit.txt
exit "$code"
