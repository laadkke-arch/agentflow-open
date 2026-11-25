#!/usr/bin/env bash
# Replay one fixed checkout in a blank directory without fetching responses.
set -euo pipefail
checkout=${1:?repository path}
revision=${2:?full Git result commit}
owned=docs/workstreams/research/AF-RES-266
commit=$(git -C "$checkout" rev-parse --verify "$revision^{commit}")
clean=$(mktemp -d "${TMPDIR:-/tmp}/af-res-266-replay.XXXXXX")
printf 'checked_commit=%s\narchive_destination=%s\n' "$commit" "$clean"
git -C "$checkout" archive --format=tar "$commit" "$owned" | tar -xf - -C "$clean"
cd "$clean/$owned"
sha256sum -c receipts/replay-inputs.sha256
PYTHONPATH="$PWD/receipts/tools/packaging-26.3-py3-none-any.whl" \
    python -P replay.py --data "$PWD" --output "$clean/output"
for file in files.csv cells.csv release-events.csv; do
    cmp "$file" "$clean/output/$file"
done
for file in inventory.json parsers.json counterexamples.json; do
    cmp "receipts/computed/$file" "$clean/output/$file"
done
(cd "$clean/output" && sha256sum files.csv cells.csv release-events.csv inventory.json parsers.json counterexamples.json)
printf 'byte-for-byte matches=6\n'
