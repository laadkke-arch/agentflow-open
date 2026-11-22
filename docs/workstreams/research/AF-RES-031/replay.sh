#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  printf 'Usage: bash replay.sh CACHE_ROOT NEW_EMPTY_DIRECTORY\n' >&2
  exit 2
fi
workstream=$(cd "$(dirname "$0")" && pwd)
probes="$workstream/probes"
cache=$(realpath "$1")
mkdir "$2"
out=$(realpath "$2")
mkdir "$out"/{original,py20,py21,java,classes,rust,ipyk26,ipyk27}

run() {
  python -B "$probes/record.py" --out "$out" "$@"
}

run --id py21-original --cwd "$out/original" --target ee4d09ebef61c663c1efbfa4c18e518a03b798be \
  --input "$probes/q01_pyarrow21_probe.py" -- \
  "$cache/venv/py21/bin/python" -B "$probes/q01_pyarrow21_probe.py" --output-dir fixtures
for version in 20 21; do
  if [ "$version" = 20 ]; then
    sha=3ad0370a04ccdae638755b94c3c31c8760a11193
  else
    sha=ee4d09ebef61c663c1efbfa4c18e518a03b798be
  fi
  run --id "py$version" --cwd "$out/py$version" --target "$sha" \
    --input "$probes/parquet_types.py" --input "$probes/inputs.json" -- \
    "$cache/venv/py$version/bin/python" -B "$probes/parquet_types.py" \
    "$probes/inputs.json" fixtures --version "$version.0.0"
done

jvm="$cache/tools/jdk"
native="$cache/java-dist/lib/arrow_cdata_jni/x86_64"
java_sha=7a581880a85358315d05da08296cf570b3643924
java_src="$cache/source/arrow-java"
test_file="$java_src/c/src/test/java/org/apache/arrow/c/RoundtripTest.java"
test_class=org.apache.arrow.c.RoundtripTest
test_cp=$(cat "$cache/setup/java/java.cp")
console="$cache/setup/java/junit-platform-console-standalone-6.1.3.jar"
test "$(git -C "$java_src" rev-parse HEAD)" = "$java_sha"
test "$(git -C "$java_src" hash-object "$test_file")" = 4d2acbb091af4e563e2a08fc2ae319a57f797f14
run --id java-upstream --cwd "$out/java" --target "$java_sha" \
  --input "$test_file" --input "$console" --input "$native/libarrow_cdata_jni.so" -- \
  "$jvm/bin/java" --add-opens=java.base/java.nio=ALL-UNNAMED "-Darrow.cdata.library.path=$native" \
  -cp "$console:$test_cp" org.junit.platform.console.ConsoleLauncher execute --disable-ansi-colors \
  --details=flat --fail-if-no-tests --reports-dir "$out/java/official-reports" \
  "--select-method=$test_class#testLargeVarBinaryVector" "--select-method=$test_class#testLargeListVector"

classpath="$out/classes:$test_cp"
printf '%s\n' "$classpath" > "$out/java/bridge.cp"
run --id arrow-consumer-compile --cwd "$out/java" --target "$java_sha" \
  --input "$probes/ArrowConsumer.java" -- \
  "$jvm/bin/javac" -cp "$classpath" -d "$out/classes" "$probes/ArrowConsumer.java"

java_read() {
  run --id "$1" --cwd "$out/java" --target "$java_sha" --input "$2" --input "$probes/ArrowConsumer.java" -- \
    "$jvm/bin/java" --add-opens=java.base/java.nio=ALL-UNNAMED -cp "$classpath" ArrowConsumer "$2" "$3"
}
bridge() {
  local id=$1
  local input=$2
  shift 2
  run --id "$id" --cwd "$out/java" --target "$java_sha" --input "$input" \
    --input "$probes/cdata_bridge.py" --input "$native/libarrow_cdata_jni.so" -- \
    "$cache/venv/py21/bin/python" -B "$probes/cdata_bridge.py" \
    --jvm "$jvm/lib/server/libjvm.so" --jni-library-dir "$native" \
    --classpath-file "$out/java/bridge.cp" "$@"
}
for mode in large stored; do
  if [ "$mode" = large ]; then
    input="$out/py21/fixtures/no_stored_schema.arrow-stream"
  else
    input="$out/py21/fixtures/stored_schema.arrow-stream"
  fi
  java_read "ipc-$mode" "$input" "$mode"
  bridge "cd-$mode" "$input" --ipc "$input" --type "$mode"
done
if java_read ipc-reject-small-as-large "$out/py21/fixtures/stored_schema.arrow-stream" large; then
  printf 'A small vector unexpectedly passed the large-only check.\n' >&2
  exit 1
fi
grep -F 'binary vector: VarBinaryVector' "$out/ipc-reject-small-as-large.stderr" > /dev/null
bridge cd-2g "$probes/inputs.json" --threshold-fixture "$probes/inputs.json"

rust_sha=4b7cdcb9220b6d94b251aef32c21ef9b4097ecfa
rust_src="$cache/source/arrow-2021"
rust_lock="$rust_src/rust/Cargo.lock"
test "$(git -C "$rust_src" rev-parse HEAD)" = "$rust_sha"
cmp "$workstream/evidence/locks/rust-4b7cdcb-Cargo.lock" "$rust_lock"
rust_bin() {
  local prefix=$1
  local candidate
  local matches=()
  for candidate in "$cache/cache/rust149/debug/deps/$prefix"-*; do
    if [ -f "$candidate" ] && [ -x "$candidate" ]; then
      matches+=("$candidate")
    fi
  done
  test "${#matches[@]}" = 1
  printf '%s\n' "${matches[0]}"
}
original_bin=$(rust_bin af_res025_scalar_probe)
boundaries_bin=$(rust_bin scalar_boundaries)
provider_bin=$(rust_bin datafusion)
run --id rust025 --cwd "$out/rust" --target "$rust_sha" --input "$original_bin" --input "$rust_lock" \
  --input "$probes/af_res025_scalar_probe.rs" -- "$original_bin" common_accessor_boolean_utf8_list --exact --nocapture
run --id rust-boundaries --cwd "$out/rust" --target "$rust_sha" --input "$boundaries_bin" --input "$rust_lock" \
  --input "$probes/scalar_boundaries.rs" -- "$boundaries_bin" --nocapture --test-threads=1
run --id rust-upstream --cwd "$out/rust" --target "$rust_sha" --input "$provider_bin" --input "$rust_lock" \
  --input "$rust_src/rust/datafusion/src/scalar.rs" -- "$provider_bin" scalar::tests::scalar_list_ --nocapture --test-threads=1

for version in 26 27; do
  run --id "ipyk$version" --cwd "$out/ipyk$version" --target "ipykernel v6.$version.0; jupyter_client v8.6.0" \
    --input "$probes/jupyter_wire.py" --input "$probes/inputs.json" --timeout 130 -- \
    env "IPYTHONDIR=$out/ipyk$version/ipython" "JUPYTER_RUNTIME_DIR=$out/ipyk$version/runtime" \
    "JUPYTER_CONFIG_DIR=$out/ipyk$version/config" "$cache/venv/ipyk$version/bin/python" -B \
    "$probes/jupyter_wire.py" --version "6.$version.0" --fixture "$probes/inputs.json"
done
