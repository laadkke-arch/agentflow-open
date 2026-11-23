#!/usr/bin/env bash
# Configure once and rebuild only the changed source files when switching G to L.
set -euo pipefail
if [[ $# != 4 ]]; then
    echo 'usage: build.sh UPSTREAM AF085_PACKET NEW_BUILD_DIR NEW_BINARY_DIR' >&2
    exit 2
fi
src=$(realpath "$1")
ref085=$(realpath "$2")
build=$(realpath -m "$3")
out=$(realpath -m "$4")
here=$(cd -- "$(dirname -- "$0")" && pwd)
patches="$here/patches"
base=f4fcf53ff65c56f0efb616a3af209d3faba9b342
merge=16851045c9e50eafb016c5cf4f2733f974e841bf
[[ $(git -C "$src" rev-parse HEAD) == "$base" ]]
[[ -z $(git -C "$src" status --porcelain) ]]
git -C "$src" diff "$merge^1" "$merge" -- libmscore/element.cpp | cmp - "$patches/G-global-selection.patch"
mkdir "$build" "$out"
mkdir "$out/logs"
git -C "$src" apply "$patches/common-gcc14.patch" "$patches/common-desktop-qt.patch"
python -B "$ref085/fixtures/probe/inject.py" "$src"
python -B "$here/extend_probe.py" "$src"
git -C "$src" diff --binary > "$out/logs/common.diff"
sha256sum "$src"/libmscore/af085_model.h "$src"/mscore/af085_ui.h > "$out/logs/probe.sha256"
cmake -S "$src" -B "$build" -G 'Unix Makefiles' \
    -DCMAKE_BUILD_TYPE=Debug '-DCMAKE_CXX_FLAGS=-w -gsplit-dwarf' \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_WEBENGINE=OFF -DBUILD_JACK=OFF \
    -DBUILD_PULSEAUDIO=OFF -DBUILD_ALSA=OFF -DBUILD_PORTAUDIO=OFF -DBUILD_PORTMIDI=OFF \
    -DBUILD_LAME=OFF -DDOWNLOAD_SOUNDFONT=OFF -DUSE_SYSTEM_FREETYPE=OFF \
    -DCMAKE_INSTALL_PREFIX="$build/install" > "$out/logs/configure.log" 2>&1
for variant in G L; do
    if [[ "$variant" == G ]]; then
        git -C "$src" apply "$patches/G-global-selection.patch"
    else
        git -C "$src" apply --reverse "$patches/G-global-selection.patch"
        git -C "$src" show HEAD:libmscore/excerpt.cpp > "$src/libmscore/excerpt.cpp"
        git -C "$src" apply "$patches/L-excerpt-selection.patch"
        python -B "$ref085/fixtures/probe/inject.py" "$src" --excerpt-only
    fi
    git -C "$src" diff --binary > "$out/logs/source-$variant.diff"
    (
        cd "$src"
        git ls-files -z --cached --others --exclude-standard | sort -z |
            while IFS= read -r -d '' name; do
                if [[ -f "$name" ]]; then printf '%s\0' "$name"; fi
            done | xargs -0 sha256sum
    ) > "$out/logs/source-$variant.sha256"
    git -C "$src" ls-files --stage | awk '$1 == "160000"' > "$out/logs/submodules-$variant.txt"
    date -u +%FT%TZ > "$out/logs/build-$variant.start"
    status=0
    cmake --build "$build" --parallel "${AF089_JOBS:-4}" --target mscore workspaces > "$out/logs/build-$variant.log" 2>&1 || status=$?
    date -u +%FT%TZ > "$out/logs/build-$variant.end"
    printf '%s\n' "$status" > "$out/logs/build-$variant.exit"
    [[ "$status" == 0 ]]
    cp "$build/mscore/mscore" "$out/mscore-$variant"
done
resources="$build/install/share/mscore-3.1"
mkdir -p "$resources"
for subdir in workspaces instruments templates themes tours wallpaper styles; do
    cp -a "$src/share/$subdir" "$resources/"
done
cp "$build/share/workspaces/"*.workspace "$resources/workspaces/"
sha256sum "$out"/mscore-{G,L} > "$out/binaries.sha256"
