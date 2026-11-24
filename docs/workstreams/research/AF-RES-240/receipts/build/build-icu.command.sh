#!/usr/bin/env bash
set -euo pipefail
umask 022
unset PYTHONPATH PYTHONHOME ICU_DATA CFLAGS CPPFLAGS LDFLAGS LD_LIBRARY_PATH CONFIG_SITE
export LC_ALL=C TZ=UTC
command="${1:?cpython or icu}"
case "$command" in
cpython)
    archive=Python-3.13.0.tar.xz
    url=https://www.python.org/ftp/python/3.13.0/$archive
    root=Python-3.13.0
    ;;
icu)
    archive=icu4c-76_1-src.tgz
    url=https://github.com/unicode-org/icu/releases/download/release-76-1/$archive
    root=icu
    ;;
*) exit 64 ;;
esac
printf 'module=%s\narchive_url=%s\nstart_utc=%s\n' "$command" "$url" "$(date -u +%FT%TZ)"
curl --fail --location --silent --show-error --retry 2 --max-time 240 --dump-header "$archive.headers" --output "$archive" "$url"
sha256sum "$archive"
tar -xf "$archive"
case "$command" in
cpython)
    cd "$root"
    ./configure --without-ensurepip
    make -j2
    ./python -I -c 'import sys, unicodedata as u; print(sys.version); print(u.unidata_version); assert sys.version_info[:3] == (3, 13, 0) and u.unidata_version == "15.1.0"'
    ;;
icu)
    cd "$root/source"
    ./configure --prefix="$PWD/../../icu-prefix" --disable-tests --disable-samples
    make -j3
    make install
    "$PWD/../../icu-prefix/bin/icuinfo"
    ;;
esac
printf 'end_utc=%s\n' "$(date -u +%FT%TZ)"
