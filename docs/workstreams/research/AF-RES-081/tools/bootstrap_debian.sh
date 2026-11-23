#!/usr/bin/env bash
# Prepare a private dependency prefix on the Debian 13 x86-64 Cloud image.
set -euo pipefail
if [[ $# != 1 ]]; then
    echo 'usage: bootstrap_debian.sh NEW_DIRECTORY' >&2
    exit 2
fi
destination=$(realpath -m "$1")
mkdir "$destination"
mkdir -p "$destination/lists/partial" "$destination/cache/archives/partial" \
    "$destination/empty" "$destination/prefix"
printf '%s\n' 'deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie main' \
    > "$destination/sources.list"
apt_local=(
    /usr/bin/apt-get -o "Dir::Etc::sourcelist=$destination/sources.list"
    -o "Dir::Etc::sourceparts=$destination/empty" -o "Dir::Etc::Parts=$destination/empty"
    -o "Dir::State::lists=$destination/lists" -o "Dir::Cache=$destination/cache"
    -o "Dir::Cache::archives=$destination/cache/archives" -o Debug::NoLocking=true
    -o Acquire::Languages=none
)
"${apt_local[@]}" update
"${apt_local[@]}" --no-install-recommends --download-only -y install \
    cmake ninja-build qtbase5-dev qtdeclarative5-dev libqt5xmlpatterns5-dev \
    libqt5svg5-dev qttools5-dev libqt5opengl5-dev libsndfile1-dev libvorbis-dev \
    zlib1g-dev xvfb xauth xdotool
for package in "$destination"/cache/archives/*.deb; do
    dpkg-deb -x "$package" "$destination/prefix"
done
prefix="$destination/prefix"
for directory in /usr/lib/x86_64-linux-gnu /usr/lib/qt5/bin; do
    if [[ "$directory" == */x86_64-linux-gnu ]]; then
        files=("$directory"/lib*.so*)
    else
        files=("$directory"/*)
    fi
    for file in "${files[@]}"; do
        target="$prefix$file"
        if [[ ! -e "$target" && ! -L "$target" ]]; then ln -s "$file" "$target"; fi
    done
done
for directory in /usr/lib/x86_64-linux-gnu/qt5/{plugins,qml}; do
    if [[ ! -d "$directory" ]]; then continue; fi
    while IFS= read -r -d '' file; do
        target="$prefix$file"
        mkdir -p "${target%/*}"
        if [[ ! -e "$target" && ! -L "$target" ]]; then ln -s "$file" "$target"; fi
    done < <(find "$directory" \( -type f -o -type l \) -print0)
done
{
    printf 'AF081_DEPS=%q\n' "$prefix"
    cat <<'ENV'
af081_multi="$AF081_DEPS/usr/lib/x86_64-linux-gnu"
export PATH="$AF081_DEPS/usr/lib/qt5/bin:$AF081_DEPS/usr/bin:$PATH"
export CMAKE_PREFIX_PATH="$AF081_DEPS/usr"
export LD_LIBRARY_PATH="$af081_multi${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LIBRARY_PATH="$af081_multi${LIBRARY_PATH:+:$LIBRARY_PATH}"
export CPLUS_INCLUDE_PATH="$AF081_DEPS/usr/include${CPLUS_INCLUDE_PATH:+:$CPLUS_INCLUDE_PATH}"
export PKG_CONFIG_PATH="$af081_multi/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
ENV
} > "$destination/env.sh"
