#!/usr/bin/env bash
set -euo pipefail

AF078_SCRIPTS=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
AF078_OUTPUT=${1:?pass a new output directory}
if [[ -f "${AF078_OUTPUT}/runs.jsonl" || -f "${AF078_OUTPUT}/evidence/diagnostics.jsonl" ]]; then
    printf '%s\n' 'Choose a new output directory for an independent replay.' >&2
    exit 2
fi
mkdir -p -- "${AF078_OUTPUT}"
for AF078_PHASE in versions solo main edge diag; do
    python -B "${AF078_SCRIPTS}/trial.py" --phase "${AF078_PHASE}" --out "${AF078_OUTPUT}"
done
python -B "${AF078_SCRIPTS}/verify.py" --replay-dir "${AF078_OUTPUT}"
