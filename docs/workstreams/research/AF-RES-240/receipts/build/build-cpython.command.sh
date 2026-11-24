#!/usr/bin/env bash
set -euo pipefail
umask 022
unset PYTHONPATH PYTHONHOME CFLAGS CPPFLAGS LDFLAGS LD_LIBRARY_PATH CONFIG_SITE
export LC_ALL=C TZ=UTC
sha=60403a5409ff2c3f3b07dd2ca91a7a3e096839c7
archive=cpython-$sha.tar.gz
url=https://codeload.github.com/python/cpython/tar.gz/$sha
printf 'ref=v3.13.0\nsource_commit=%s\narchive_url=%s\nstart_utc=%s\n' "$sha" "$url" "$(date -u +%FT%TZ)"
git ls-remote https://github.com/python/cpython.git 'refs/tags/v3.13.0' 'refs/tags/v3.13.0^{}'
curl --fail --location --silent --show-error --retry 2 --max-time 240 --dump-header "$archive.headers" --output "$archive" "$url"
sha256sum "$archive"
tar -xf "$archive"
cd "cpython-$sha"
./configure --without-ensurepip
make -j2
./python -I -c 'import sys, unicodedata as u; print(sys.version); print(u.unidata_version); assert sys.version_info[:3] == (3, 13, 0) and u.unidata_version == "15.1.0"'
printf 'end_utc=%s\n' "$(date -u +%FT%TZ)"
