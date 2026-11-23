#!/usr/bin/env bash
# Build in a fresh checkout of the first parent and a separate empty folder.
set -euo pipefail

if [[ $# != 3 ]]; then
    echo 'usage: build_variants.sh PINNED_CHECKOUT BUILD_DIR BINARY_OUTPUT_DIR' >&2
    exit 2
fi
source_dir=$(realpath "$1")
build_dir=$(realpath -m "$2")
binary_dir=$(realpath -m "$3")
packet=$(cd "$(dirname "$0")/.." && pwd)
expected=f4fcf53ff65c56f0efb616a3af209d3faba9b342
[[ $(git -C "$source_dir" rev-parse HEAD) == "$expected" ]]
[[ -z $(git -C "$source_dir" status --porcelain) ]]
mkdir "$build_dir" "$binary_dir"
mkdir -p "$build_dir/install/share/mscore-3.1" "$binary_dir/logs"
cp -a "$source_dir/share/styles" "$build_dir/install/share/mscore-3.1/"

git -C "$source_dir" apply "$packet/patches/common-gcc14.patch"
git -C "$source_dir" apply "$packet/patches/common-probe.patch"
cmake -S "$source_dir" -B "$build_dir" -G 'Unix Makefiles' \
    -DCMAKE_BUILD_TYPE=Debug '-DCMAKE_CXX_FLAGS=-w -gsplit-dwarf' \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_WEBENGINE=OFF -DBUILD_JACK=OFF \
    -DBUILD_PULSEAUDIO=OFF -DBUILD_ALSA=OFF -DBUILD_PORTAUDIO=OFF -DBUILD_PORTMIDI=OFF \
    -DBUILD_LAME=OFF -DDOWNLOAD_SOUNDFONT=OFF -DUSE_SYSTEM_FREETYPE=OFF \
    -DCMAKE_INSTALL_PREFIX="$build_dir/install" > "$binary_dir/logs/configure.log" 2>&1
# The original suite targets here retain the U model behavior.
cmake --build "$build_dir" --parallel "${AF081_JOBS:-4}" \
    --target tst_parts tst_links tst_element tst_exchangevoices tst_readwriteundoreset \
    tst_implodeExplode tst_copypaste > "$binary_dir/logs/build-original.log" 2>&1

active_patch=
restore_variant() {
    if [[ -n "$active_patch" ]]; then
        git -C "$source_dir" apply --reverse "$active_patch"
    fi
}
trap restore_variant EXIT
for variant in U G L; do
    case "$variant" in
        G) active_patch="$packet/patches/G-global-selection.patch" ;;
        L) active_patch="$packet/patches/L-excerpt-selection.patch" ;;
    esac
    if [[ -n "$active_patch" ]]; then
        git -C "$source_dir" apply --check "$active_patch"
        git -C "$source_dir" apply "$active_patch"
    fi
    cmake --build "$build_dir" --parallel "${AF081_JOBS:-4}" --target af_res_081 \
        > "$binary_dir/logs/build-$variant.log" 2>&1
    cp "$build_dir/mtest/af_res_081/af_res_081" "$binary_dir/af_res_081-$variant"
    mkdir "$binary_dir/smoke-$variant"
    (
        cd "$binary_dir/smoke-$variant"
        export QT_QPA_PLATFORM=offscreen XDG_CONFIG_HOME="$PWD/config"
        export XDG_DATA_HOME="$PWD/data" XDG_CACHE_HOME="$PWD/cache"
        "$binary_dir/af_res_081-$variant" --smoke "$packet/fixtures/two-parts.mscx" \
            > stdout.jsonl 2> stderr.txt
    )
    restore_variant
    active_patch=
done

sha256sum "$binary_dir"/af_res_081-{U,G,L} > "$binary_dir/binaries.sha256"
