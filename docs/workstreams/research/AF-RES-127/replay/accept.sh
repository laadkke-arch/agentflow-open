#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 || ! "$1" =~ ^[a-f0-9]{40}$ ]]; then
  printf 'usage: bash replay/accept.sh RESULT_SHA NEW_OUTPUT_DIR [full]\n' >&2
  exit 2
fi

af127_sha="$1"
af127_checks="${3:-replay}"
mkdir "$2"
af127_out=$(realpath "$2")
af127_branch=work/research-af-res-127
af127_repo=https://github.com/laadkke-arch/agentflow-open.git
af127_path=docs/workstreams/research/AF-RES-127

function step() {
  local name="$1" code
  shift
  {
    printf 'cd %q\n' "$PWD"
    printf '%q ' "$@"
    printf '\n'
  } >> "$af127_out/commands.log"
  if "$@" > "$af127_out/$name.stdout" 2> "$af127_out/$name.stderr"; then
    code=0
  else
    code=$?
  fi
  printf '%s\n' "$code" > "$af127_out/$name.exit"
  printf '%s %s\n' "$name" "$code"
  return "$code"
}

step clone git clone --no-tags --single-branch --branch "$af127_branch" "$af127_repo" "$af127_out/checkout"
cd "$af127_out/checkout"
step checkout git switch --detach "$af127_sha"
step checkout-sha git rev-parse HEAD
test "$(git rev-parse HEAD)" = "$af127_sha"
step clean-before git status --porcelain
test ! -s "$af127_out/clean-before.stdout"
step runtime bash -c 'date -u +%FT%TZ
uname -srm
cat /etc/os-release
git --version
python -V
node --version
npm --version
chromium --version
sha256sum /usr/bin/chromium /usr/lib/chromium/chromium'
step recount python -B "$af127_path/replay/audit.py" --report "$af127_out/recount.json"
step npm-ci npm --cache "$af127_out/npm-cache" --prefix "$af127_path/fixture" ci --no-audit --no-fund
step browser-main-controls-supplement node "$af127_path/replay/drive.mjs" --mode all --out "$af127_out/run" --chromium /usr/bin/chromium
step browser-pilot node "$af127_path/replay/drive.mjs" --mode pilot --out "$af127_out/run" --chromium /usr/bin/chromium
step compare python -B "$af127_path/replay/compare.py" --reference "$af127_path/evidence" --candidate "$af127_out/run" --commit "$af127_sha" --report "$af127_out/compare.json"

if [[ "$af127_checks" == full ]]; then
  af127_check_code=0
  step session python -B -m workbench.session check "$af127_path/manifest.json" --fetch || af127_check_code=1
  step cloud python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean || af127_check_code=1
  step repository python -B scripts/check.py --require-git || af127_check_code=1
  step clean-after git status --porcelain || af127_check_code=1
  test ! -s "$af127_out/clean-after.stdout" || af127_check_code=1
  exit "$af127_check_code"
fi
step clean-after git status --porcelain
test ! -s "$af127_out/clean-after.stdout"
