#!/usr/bin/env bash
set -euo pipefail

if [[ $# != 3 || ! "$1" =~ ^[a-f0-9]{40}$ || ! "$3" =~ ^(clone|fetch-sha)$ ]]; then
  printf 'usage: bash replay/accept.sh RESULT_SHA NEW_OUTPUT_DIR clone|fetch-sha\n' >&2
  exit 2
fi

af131_sha="$1"
af131_route="$3"
mkdir "$2"
af131_out=$(realpath "$2")
af131_branch=work/research-af-res-131
af131_repo=https://github.com/laadkke-arch/agentflow-open.git
af131_path=docs/workstreams/research/AF-RES-131

function step() {
  local name="$1" code
  shift
  {
    printf 'cd %q\n' "$PWD"
    printf '%q ' "$@"
    printf '\n'
  } >> "$af131_out/commands.log"
  if "$@" > "$af131_out/$name.stdout" 2> "$af131_out/$name.stderr"; then
    code=0
  else
    code=$?
  fi
  printf '%s\n' "$code" > "$af131_out/$name.exit"
  printf '%s %s\n' "$name" "$code"
  return "$code"
}

if [[ "$af131_route" == clone ]]; then
  step clone git clone --no-tags --single-branch --branch "$af131_branch" "$af131_repo" "$af131_out/checkout"
  cd "$af131_out/checkout"
else
  step init git init "$af131_out/checkout"
  cd "$af131_out/checkout"
  step add-remote git remote add origin "$af131_repo"
  step fetch-result git fetch --no-tags --depth=1 origin "$af131_sha"
fi

step checkout git switch --detach "$af131_sha"
step checkout-sha git rev-parse HEAD
test "$(cat "$af131_out/checkout-sha.stdout")" = "$af131_sha"
step clean-before git status --porcelain
test ! -s "$af131_out/clean-before.stdout"
step runtime bash -c 'date -u +%FT%TZ
uname -srm
git --version
python --version
node --version
npm --version
chromium --version
sha256sum /usr/bin/chromium /usr/lib/chromium/chromium'
step audit python -B "$af131_path/replay/audit.py" --report "$af131_out/recount.json"
step npm-ci npm --cache "$af131_out/npm-cache" --prefix "$af131_path/fixture" ci --no-audit --no-fund --registry https://registry.npmjs.org/
step browser env -u TMPDIR node "$af131_path/replay/drive.mjs" --mode all --out "$af131_out/run" --chromium /usr/bin/chromium
step summarize python -B "$af131_path/replay/summarize.py" --evidence "$af131_out/run" --output "$af131_out/runs.jsonl"
step compare python -B "$af131_path/replay/compare.py" --reference "$af131_path/evidence/browser" --candidate "$af131_out/run" --commit "$af131_sha" --report "$af131_out/compare.json"

af131_check_code=0
if [[ "$af131_route" == clone ]]; then
  step session python -B -m workbench.session check "$af131_path/manifest.json" --fetch || af131_check_code=1
  step cloud python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean || af131_check_code=1
fi
step clean-after git status --porcelain || af131_check_code=1
test ! -s "$af131_out/clean-after.stdout" || af131_check_code=1
exit "$af131_check_code"
