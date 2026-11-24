#!/usr/bin/env bash
set -euo pipefail
cd /tmp/af-res-240-evidence
export LD_LIBRARY_PATH=$PWD/icu-prefix/lib
dat=$PWD/icu/source/data/in/icudt76l.dat
mkdir -p "$PWD/extracted"
./icu-prefix/sbin/icupkg -l "$dat" | awk '$0 == "unames.icu" {print; ok++} END {exit ok!=1}'
./icu-prefix/sbin/icupkg -x unames.icu -d "$PWD/extracted" "$dat"
sha256sum "$dat" extracted/unames.icu icu/source/data/out/build/icudt76l/unames.icu \
    icu-prefix/lib/libicudata.so.76.1
cmp extracted/unames.icu icu/source/data/out/build/icudt76l/unames.icu
od -An -tx1 -N32 extracted/unames.icu
nm -D icu-prefix/lib/libicudata.so.76.1 | awk '$3 == "icudt76_dat" {print; ok++} END {exit ok!=1}'
