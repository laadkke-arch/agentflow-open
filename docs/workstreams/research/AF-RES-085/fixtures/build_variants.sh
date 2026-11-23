#!/usr/bin/env bash
# Start with an empty pinned MuseScore checkout, after sourcing AF-RES-081's private dependency env.sh.
set -euo pipefail
if [[ $# != 4 ]]; then
    echo 'usage: build_variants.sh UPSTREAM AF081_PACKET NEW_BUILD_DIR NEW_BINARY_DIR' >&2
    exit 2
fi
source_dir=$(realpath "$1")
previous=$(realpath "$2")
build_dir=$(realpath -m "$3")
output=$(realpath -m "$4")
here=$(cd -- "$(dirname -- "$0")" && pwd)
expected=f4fcf53ff65c56f0efb616a3af209d3faba9b342
merge=16851045c9e50eafb016c5cf4f2733f974e841bf
git -C "$source_dir" diff "$merge^1" "$merge" -- libmscore/element.cpp | cmp - "$previous/patches/G-global-selection.patch"
[[ $(git -C "$source_dir" rev-parse HEAD) == "$expected" ]]
[[ -z $(git -C "$source_dir" status --porcelain) ]]
mkdir "$build_dir" "$output"
mkdir "$output/logs"
git -C "$source_dir" apply "$previous/patches/common-gcc14.patch" "$previous/patches/common-desktop-qt.patch"
python -B "$here/probe/inject.py" "$source_dir"
cmake -S "$source_dir" -B "$build_dir" -G 'Unix Makefiles' \
    -DCMAKE_BUILD_TYPE=Debug '-DCMAKE_CXX_FLAGS=-w -gsplit-dwarf' \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_WEBENGINE=OFF -DBUILD_JACK=OFF \
    -DBUILD_PULSEAUDIO=OFF -DBUILD_ALSA=OFF -DBUILD_PORTAUDIO=OFF -DBUILD_PORTMIDI=OFF \
    -DBUILD_LAME=OFF -DDOWNLOAD_SOUNDFONT=OFF -DUSE_SYSTEM_FREETYPE=OFF \
    -DCMAKE_INSTALL_PREFIX="$build_dir/install" > "$output/logs/configure.log" 2>&1

for variant in U G L; do
    if [[ "$variant" == G ]]; then
        git -C "$source_dir" apply "$previous/patches/G-global-selection.patch"
    elif [[ "$variant" == L ]]; then
        git -C "$source_dir" apply --reverse "$previous/patches/G-global-selection.patch"
        git -C "$source_dir" show HEAD:libmscore/excerpt.cpp > "$source_dir/libmscore/excerpt.cpp"
        git -C "$source_dir" apply "$previous/patches/L-excerpt-selection.patch"
        python -B "$here/probe/inject.py" "$source_dir" --excerpt-only
    fi
    git -C "$source_dir" diff --binary | sha256sum > "$output/logs/source-diff-$variant.sha256"
    cmake --build "$build_dir" --parallel "${AF085_JOBS:-4}" --target mscore workspaces > "$output/logs/build-$variant.log" 2>&1
    cp "$build_dir/mscore/mscore" "$output/mscore-$variant"
done

resources="$build_dir/install/share/mscore-3.1"
mkdir -p "$resources"
for resource in workspaces instruments templates themes tours wallpaper styles; do
    cp -a "$source_dir/share/$resource" "$resources/"
done
cp "$build_dir/share/workspaces/"*.workspace "$resources/workspaces/"
sha256sum "$output"/mscore-{U,G,L} > "$output/binaries.sha256"
