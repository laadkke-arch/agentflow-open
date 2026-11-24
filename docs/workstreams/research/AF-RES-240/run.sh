#!/usr/bin/env bash
# Record probe arguments, stdin, version fingerprints, streams and exit values.
set -euo pipefail

if (( $# < 4 || $# > 5 )); then
    echo "Usage: $0 main|controls|tz CPYTHON ICU_PREFIX OUTPUT [TZDIR]" >&2
    exit 64
fi
phase=$1
cpython=$(realpath "$2")
icu=$(realpath "$3")
out=$(realpath -m "$4")
tzdir=${5:-}
here=$(cd -- "$(dirname -- "$0")" && pwd)
if [[ -e "$out" ]]; then
    echo "Choose a new output directory: $out" >&2
    exit 64
fi
mkdir -p -- "$out"
clean=(env -i PATH=/usr/bin:/bin LC_ALL=C TZ=UTC)
icu_env=("${clean[@]}" "LD_LIBRARY_PATH=$icu/lib")
icu_pkg=("${clean[@]}" "PKG_CONFIG_LIBDIR=$icu/lib/pkgconfig")

record() {
    local name=$1 input=$2 rc=0
    shift 2
    {
        printf 'cwd=%q\nstdin=%q\nargv=' "$PWD" "$input"
        printf ' %q' "$@"
        printf '\nstart_utc=%s\n' "$(date -u +%FT%TZ)"
    } > "$out/$name.receipt"
    "$@" < "$input" > "$out/$name.stdout" 2> "$out/$name.stderr" || rc=$?
    printf 'end_utc=%s\nexit=%s\n' "$(date -u +%FT%TZ)" "$rc" >> "$out/$name.receipt"
    return "$rc"
}

record compiler /dev/null "${clean[@]}" cc --version
record icu-pkg /dev/null "${icu_pkg[@]}" pkg-config --modversion icu-uc icu-i18n
record compile /dev/null "${clean[@]}" cc -std=c11 -Wall -Wextra -Werror -O2 \
    -I"$icu/include" "$here/probe.c" -o "$out/probe" \
    -L"$icu/lib" -licui18n -licuuc -licudata
record ldd /dev/null "${icu_env[@]}" ldd "$out/probe"
record ldd-python /dev/null "${clean[@]}" ldd "$cpython"
record python-module /dev/null "${clean[@]}" "$cpython" -I -c \
    'import unicodedata; print(unicodedata.__file__)'
IFS= read -r module < "$out/python-module.stdout"
record ldd-python-module /dev/null "${clean[@]}" ldd "$module"
record hashes /dev/null "${clean[@]}" sha256sum "$cpython" "$module" \
    "$icu/lib/libicuuc.so.76.1" "$icu/lib/libicui18n.so.76.1" \
    "$icu/lib/libicudata.so.76.1" "$out/probe" \
    "$here/probe.c" "$here/probe.py" "$here/inputs.csv" "$here/controls.csv" "$here/run.sh"

if [[ "$phase" == tz ]]; then
    record python-tz /dev/null "${clean[@]}" "$cpython" -I "$here/probe.py" tz --tzdir "$tzdir"
    record icu-tz /dev/null "${icu_env[@]}" "$out/probe" tz
else
    record cases /dev/null "${clean[@]}" "$cpython" -I "$here/probe.py" "$phase" --emit-icu
    for repetition in 1 2; do
        record "python-$repetition" /dev/null "${clean[@]}" \
            "$cpython" -I "$here/probe.py" "$phase" --repeat "$repetition"
        record "icu-$repetition" "$out/cases.stdout" "${icu_env[@]}" "$out/probe" "$repetition"
    done
fi
