# AF-RES-075 · 재생

Python 3.12 표준 라이브러리와 이 경로의 봉인 입력이 필요하다. 측정 환경은 Linux x86_64, Python 3.12.14였다. PG는 2.17.2·2.18.0, TZ는 2024a·2024b의 정확한 등록 파일을 [manifest](inputs/manifest.json)에서 확인한다. 원격 조회 없는 재생에 Pygments 설치나 IANA 데이터 설치가 필요하지 않다. 다음 명령은 이 파일과 같은 커밋을 GitHub에서 받아 저장소 루트에서 실행한다.

```sh
set -eu
p=docs/workstreams/research/AF-RES-075
one=$(mktemp -d)
two=$(mktemp -d)
python -B "$p/experiment/prepare.py" --out "$one"
python -B "$p/experiment/run.py" --out "$one"
python -B "$p/experiment/prepare.py" --out "$two"
python -B "$p/experiment/run.py" --out "$two"
python -B "$p/experiment/audit.py" --replay "$one" --replay "$two" --final
```

prepare는 공식 4개 파일의 SHA-256과 행 수를 검증하고, seed 75075에서 통제 바이트를 재생성해 커밋된 복사본과 맞춘다. `pairs.csv`의 기대 열은 실행 전에 만든 기록이다. `--freeze`는 최초 작성용이며 재생 명령에는 사용하지 않는다. `broker-assets`와 `oracle-assets`는 별개 복사본이다. `blind-cwd`에는 파일을 두지 않는다. 각 reader는 한 요청을 받아 초기/진단 역사 라우트와 현재 라우트의 응답만 요청하고 종료한다. 그 뒤 정답 프로세스가 전체 원본을 읽는다. [선정과 시드](experiment/prepare.py) · [호출과 채점](experiment/run.py) · [전수 정답기](experiment/oracle.py)

각 출력에는 288 주 판독, 18 SWAP01 보조 판독, 16 손실 판독, 34 전수 판독이 있어야 한다. `runs.jsonl`의 실제 요청은 `input`의 필드 중 `projection_*`와 `wire_*`를 제외하고, `evidence/` 아래 `projection_path`의 JSON을 `record`로 조인하면 복원된다. 키를 정렬한 구분자 없는 UTF-8 JSON의 SHA-256과 B를 검증기가 다시 맞춘다. 프로세스의 행 종료 구분자는 이 B에서 뺐다. 원본 응답의 바이트는 해당 영수증의 `source_url` 및 SHA, 사용 원절은 결정의 `witness.line`과 연결된다. A의 보류에는 두 요청 오류가 `notes`에 남는다. 주 실행의 예외 0과 의도한 소실/무결성 오류는 원장이 분리한다. [판독 원장](runs.jsonl) · [투영 색인](evidence/projections.jsonl) · [손실 원장](evidence/losses.jsonl)

검증기는 `pairs.csv`, `runs.jsonl`, `scores.csv`, `costs.csv`, 봉인·정답·투영·입력경계와 손실·SWAP 원장을 커밋본과 두 재생에서 각각 바이트 단위로 대조한다. 투영 파일의 이름과 바이트도 맞춘다. `timings.jsonl`과 UTC 구간은 변동값이다. 첫 두 동일성 실행은 겹쳤고 실제 시간 비교용 재생은 별도 실행했다. GitHub 작업 브랜치 이름이 들어 있는 합성 표의 URL은 고정 결과 SHA의 같은 경로와 `after_sha256`으로 검증한다. [재생 영수증](evidence/replay-run.json) · [비교 SHA](evidence/cross-check.json)

## 별도 네이티브 확인

공식 PyPI 두 sdist를 다시 확보할 경우 아래 이름으로 저장한다. URL과 파일 지문은 inputs/manifest.json에서 읽는다. 네이티브 확인은 원본 파일 해시와 아카이브 지문을 대조한 후 설치 플러그인 0인 `-I -S` 프로세스에서 22회 실행한다. 이는 연구 점수 원장과 별개의 참조 실행이다.

```sh
p=docs/workstreams/research/AF-RES-075
dist=$(mktemp -d)
python -B - "$p/inputs/manifest.json" "$dist" <<'PY'
import json, pathlib, subprocess, sys
for edition in json.loads(pathlib.Path(sys.argv[1]).read_bytes())["editions"]:
    if edition["domain"] == "PG":
        path = pathlib.Path(sys.argv[2], "PG-" + edition["tag"] + ".tar.gz")
        subprocess.run(["curl", "-fsSL", edition["archive_used_url"], "-o", str(path)], check=True)
PY
python -B "$p/experiment/native_probe.py" --archive-dir "$dist" --output "$dist/native.jsonl"
cmp "$p/evidence/native.jsonl" "$dist/native.jsonl"
```

IANA 배포 원문 표는 버전 주소로 열었다. 셸에서 원 배포 tar가 열리는 환경이라면 아래 멤버를 직접 대조한다. 이 병행 경로의 실제 HTTP 비용은 현 원장에 들어 있지 않다.

```sh
p=docs/workstreams/research/AF-RES-075
dist=$(mktemp -d)
for tag in 2024a 2024b; do
  curl -fSL "https://data.iana.org/time-zones/releases/tzdata$tag.tar.gz" -o "$dist/$tag.tar.gz"
  sha256sum "$dist/$tag.tar.gz"
  tar -xOf "$dist/$tag.tar.gz" zone1970.tab > "$dist/$tag.tab"
  cmp "$dist/$tag.tab" "$p/inputs/TZ-$tag/zone1970.tab"
done
```

## 작업 계약

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-075/manifest.json --fetch
```

이 명령은 통합 브랜치의 계약 지문, 071 원격 의존 SHA, 소유 경로를 확인한다. 연구 판독·표의 검사에는 위 재생과 검증을 사용한다.
