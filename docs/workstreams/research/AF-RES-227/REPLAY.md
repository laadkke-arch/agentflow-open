# 재생

작업 커밋을 체크아웃한 저장소 루트에서 실행한다. 표와 원영수증은 [RESULT.md](RESULT.md)에서 연결한다. 아래 명령은 실험용 파일과 빌드를 임시 디렉터리에 쓴다. 전용 코드의 원본 확인과 2개의 소스 빌드에 네트워크, C 컴파일러, GNU make, Git 빌드 의존성 및 Python 3.12가 필요하다.

~~~sh
set -eu
af227_owned="$(git rev-parse --show-toplevel)/docs/workstreams/research/AF-RES-227"
af227_tmp="$(mktemp -d)"
af227_out="$af227_tmp/output"
git clone --depth 1 --branch v2.43.0 https://github.com/git/git.git "$af227_tmp/stock"
git clone --depth 1 --branch v2.43.0 https://github.com/git/git.git "$af227_tmp/diagnostic"
git clone --depth 1 --branch v0.2.13 https://github.com/breezy-team/patiencediff.git "$af227_tmp/breezy"
git -C "$af227_tmp/diagnostic" apply --check "$af227_owned/git-trace.patch"
git -C "$af227_tmp/diagnostic" apply "$af227_owned/git-trace.patch"
LC_ALL=C LANG=C TZ=UTC make -C "$af227_tmp/stock" -j4 NO_GETTEXT=YesPlease NO_TCLTK=YesPlease all
LC_ALL=C LANG=C TZ=UTC make -C "$af227_tmp/diagnostic" -j4 NO_GETTEXT=YesPlease NO_TCLTK=YesPlease all

for af227_phase in stock challenges diagnostic; do
    case "$af227_phase" in
        diagnostic) af227_git="$af227_tmp/diagnostic" ;;
        *) af227_git="$af227_tmp/stock" ;;
    esac
    python -B "$af227_owned/run.py" --phase "$af227_phase" \
        --git-source "$af227_git" --breezy-source "$af227_tmp/breezy" \
        --out "$af227_out/receipts" --scratch "$af227_tmp/runs/$af227_phase"
done

af227_dp="$af227_tmp/lis_dp_source.py"
curl --fail --silent --show-error --location \
    'https://raw.githubusercontent.com/TheAlgorithms/Python/30507bbe41397065728167fb09aa820f9fce8dc7/dynamic_programming/longest_increasing_subsequence_iterative.py' \
    -o "$af227_dp"
AF227_DP="$af227_dp" AF227_OUT="$af227_out" PYTHONPATH="$af227_owned" python -B - <<'PY'
import os
from pathlib import Path
import run
import sys
import tempfile

out = Path(os.environ['AF227_OUT'])
with tempfile.TemporaryDirectory(prefix='af227-lis-replay-') as tmp:
    cwd = Path(tmp)
    result = run.capture([sys.executable, '-B', '-S', run.HERE/'lis_check.py', os.environ['AF227_DP']],
                         cwd, run.clean_environment(cwd))
    run.save_json(out/'receipts/lis.json', result)
    if result['exit_code'] != 0:
        raise SystemExit(result['stderr'])
PY

python -B "$af227_owned/analyze.py" --final --git-source "$af227_tmp/stock" \
    --receipts "$af227_out/receipts" --output "$af227_out" > "$af227_out/primary-table.md"
python -B "$af227_owned/observe.py" --receipts "$af227_out/receipts" --output "$af227_out"
python -B "$af227_owned/verify_replay.py" --replay "$af227_out/receipts" \
    --replay-checkout "$(git rev-parse HEAD)" --output "$af227_out/replay-summary.json"
~~~

원영수증의 stdout/stderr는 JSON 문자열을 UTF-8로 돌리면 원바이트가 된다. 바이트가 UTF-8로 해석되지 않을 때는 Python의 `surrogateescape` 규칙을 쓰고 각 스트림의 SHA-256을 검증한다. 예를 들어 `jq -jr 'select(.ordinal==21).stdout' receipts/base.jsonl`은 C2 Git patience stdout을 꺼낸다. `stderr`를 선택하면 계측 영수증의 trace도 같은 방식으로 읽힌다. 반복의 cwd·시각·실행 경로와 unittest 경과 시간은 재생 때 달라질 수 있다. 입력 파일명 `a`, `b`는 각 새 임시 디렉터리 안에서 동일하다.

간단히 저장된 재생 대조만 검산하려면 `python -B "$af227_owned/verify_replay.py" --replay "$af227_owned/receipts/replay" --replay-checkout 8377dbb --output /tmp/af227-verify.json`을 실행할 수 있다. 이 명령은 기존 두 경로의 기록을 대조한다.
