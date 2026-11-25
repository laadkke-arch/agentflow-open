#!/usr/bin/env bash
set -eu

appdir=$1
profile=$2
receipt_dir=$3
mkdir -p "$profile"/{config/audacity,cache,share,state,runtime,temp} "$receipt_dir"
chmod 700 "$profile"/{runtime,temp}
if [ ! -e "$profile/config/audacity/audacity.cfg" ]; then
    cat > "$profile/config/audacity/audacity.cfg" <<CFG
[Directories]
TempDir=$profile/temp
[Quality]
DitherAlgorithmChoice=None
HQDitherAlgorithmChoice=None
[SamplingRate]
DefaultProjectSampleRate=44100
DefaultProjectSampleFormatChoice=Format16Bit
[GUI]
ShowSplashScreen=0
[Update]
UpdateNoticeShown=1
DefaultUpdatesChecking=0
CFG
fi

export LC_ALL=C.UTF-8
export XDG_CONFIG_HOME="$profile/config" XDG_CACHE_HOME="$profile/cache"
export XDG_DATA_HOME="$profile/share" XDG_STATE_HOME="$profile/state" XDG_RUNTIME_DIR="$profile/runtime"
export FONTCONFIG_FILE=/etc/fonts/fonts.conf FONTCONFIG_PATH=/etc/fonts
export LD_PRELOAD=/lib/x86_64-linux-gnu/libmount.so.1:/lib/x86_64-linux-gnu/libselinux.so.1:/lib/x86_64-linux-gnu/libpango-1.0.so.0:/lib/x86_64-linux-gnu/libpangocairo-1.0.so.0:/lib/x86_64-linux-gnu/libpangoft2-1.0.so.0

set +e
dbus-run-session "$appdir/AppRun" > "$receipt_dir/app.stdout" 2> "$receipt_dir/app.stderr"
code=$?
printf '%s\n' "$code" > "$receipt_dir/app.exit"
exit "$code"
