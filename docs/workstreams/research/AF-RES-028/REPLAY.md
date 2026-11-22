# AF-RES-028 재현 명령과 고정 입력

GitHub에서 AF-RES-028의 작업 브랜치를 내려받고 024를 별도 ref로 가져온다. 이 경로는 Linux x86-64에 CPython 빌드 도구, curl, Git, X11 검사 도구 `xwininfo`, `dpkg-deb`, OpenSSL 개발 헤더·동적 라이브러리 및 Tcl/Tk 8.6 런타임 개발 링크가 있는 Debian 13 계열을 사용했다. 별도 Python 패키지와 운영 서비스를 쓰지 않는다. 두 공식 복제본과 제한된 임시 포트·TTY·가상 X 세션이 필요하다. 터미널과 디스플레이를 대신하는 플래그는 실행 환경으로 남는다.

```sh
git clone --no-tags --single-branch --branch work/research-af-res-028 \
  https://github.com/laadkke-arch/agentflow-open.git
cd agentflow-open
git fetch --no-tags origin \
  refs/heads/chore/workspace-foundation:refs/remotes/origin/chore/workspace-foundation \
  refs/heads/work/research-af-res-024:refs/remotes/origin/work/research-af-res-024
p=docs/workstreams/research/AF-RES-028
lab=$(mktemp -d)
umask 077
design=e41cc32aa07011b904d0fb665849622b80381d07
sealed=97d4774fe6ca7a94441096ed640ab4d54b83db52

python -B "$p/draw.py" --out "$lab/draw" --answer "$lab/answer.jsonl" --design-commit "$design"
cmp "$p/packets.jsonl" "$lab/draw/packets.jsonl"
cmp "$p/scope-lock.json" "$lab/draw/scope-lock.json"
python -B "$p/compare.py" --answer "$lab/answer.jsonl" --sealed-commit "$sealed" --out "$lab/join"
cmp "$p/comparison.csv" "$lab/join/comparison.csv"
cmp "$p/tabulations.json" "$lab/join/tabulations.json"
python -B -m workbench.session check "$p/manifest.json" --fetch
python -B "$p/verify.py"
```

`draw.py`는 점수가 없는 큐와 키를 파일로 쓰고 표준 출력에는 두 해시를 보낸다. 답 파일은 작업 checkout 밖의 임시 경로에 생성한다. 이후 `compare.py`가 고정 [가림 관측 커밋](https://github.com/laadkke-arch/agentflow-open/blob/97d4774fe6ca7a94441096ed640ab4d54b83db52/docs/workstreams/research/AF-RES-028/observation-seal.json)과 대조한다. 정책은 새로 방문하지 않고 024의 `visits.csv`를 고정 입력으로 읽는다.

## 태그 실행

깨끗한 관측 재생은 위 `lab`과 별도의 실행 캐시를 구분한다. 2026-11-22의 추가 재생에서는 24개 캐시를 재사용했다. 아래 획득은 캐시가 없는 환경에서 실행하는 명령이다. CPython은 `configure --with-ensurepip=no`, `make`, `make install TESTSUBDIRS=`로 태그 소스를 직접 빌드한다. 초기 빌드에서 개발 헤더가 부족했던 3.10.1과 3.10.4의 _tkinter는 같은 태그의 소스로 따로 빌드한다.

```sh
python -B "$p/prepare.py" --fixtures "$lab/fixtures" --system "$lab/system"
python -B "$p/acquire.py" --packets "$p/packets.jsonl" --cache "$lab/cache" \
  --system "$lab/system" --out "$lab/runtimes.json" --jobs 2 --build-workers 2
python -B - "$p/artifacts.csv" "$lab/runtimes.json" <<'PY'
import csv
import json
import sys
from pathlib import Path
with open(sys.argv[1]) as f:
    reference = {(r["ecosystem"], r["tag"]): r for r in csv.DictReader(f)}
actual = json.loads(Path(sys.argv[2]).read_text())
assert len(actual) == len(reference) == 24
for row in actual:
    fixed = reference[row["ecosystem"], row["tag"]]
    assert row["status"] == "ready" and row["tag_verified"], row
    for key in ("archive_url", "commit", "sha256"):
        assert row[key] == fixed[key], (row["tag"], key, row[key], fixed[key])
PY
python -B "$p/repair_tk.py" --cache "$lab/cache" --system "$lab/system" --out "$lab/tk"
python -B "$p/run.py" --cache "$lab/cache" --fixtures "$lab/fixtures" \
  --system "$lab/system" --out "$lab/run"
python -B "$p/seal.py" --run "$lab/run" --out "$lab/seal"
python -B "$p/official_runs.py" --cache "$lab/cache" --out "$lab/official-current.jsonl"
python -B "$p/pydoc_check.py" --cache "$lab/cache" --out "$lab/pydoc.jsonl"
```

공식 바이너리·소스 URL과 SHA-256은 [배포물 원장](artifacts.csv)에 있다. CPython 아카이브 포장이 원래 관측 이후 바뀌어 SHA가 다르면 같은 커밋과 달라진 포장을 구별해 저장한다. 배포 당시 Linux 바이너리나 공급자의 서명과 같다고 추론하지 않는다. 새 설치의 접두 경로·빌드 시각·라이브러리에 따라 바이너리 해시가 달라질 수 있다. 새 빌드의 동작 재현은 `canonical_judgment_sha256`으로 비교하고 해당 환경과 변경된 input 해시를 함께 남긴다. 정확히 보존된 캐시를 사용하면 두 해시가 모두 일치해야 한다.

한 실행의 T0와 목표판 원 로그는 `run/raw.jsonl`, 종료 코드는 각 행의 `rc`, 예상값은 [계약](contracts.jsonl), 중복하지 않은 실제 런타임 출력은 `run/versions.jsonl`에 있다. 원 로그에는 임시 경로·PID·벽시간 등이 있어 SHA가 달라질 수 있다. 비교·판정의 로그 장식과 경로를 제외한 입력 및 실측값은 고정 해시로 대조한다. RSA-3072 공개 재현 fixture의 인증서 기한은 2028년 8월이다. 이후 같은 방법에 맞는 새 공개 테스트 인증서를 선택하고 fixture 선택과 SHA 변경을 버전으로 기록해야 한다. [원래 입력 버전](probes/fixtures.json) · [준비 후 보조 버전](receipts/python-aux-runtime.json)

`costs.py --with-replay --out "$lab/costs"`는 보관된 영수증에서 [비용 원장](costs.csv)과 합계를 재생한다. `cloud_check.py --environment codex-cloud --fetch-contract --require-clean`은 검사할 checkout을 고정하고 수행한다.
