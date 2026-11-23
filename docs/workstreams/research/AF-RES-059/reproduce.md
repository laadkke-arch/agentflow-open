# AF-RES-059 취득·실행 재현

이번의 작업 디렉터리는 GitHub에서 생성·복제한 `/workspace/af-res-059-github`였다. 산출물 디렉터리 외의 작업 바이트는 `/tmp/af059-evidence`에 두었다. 공개 자료의 영수증에는 주소·해시·크기를 남겼다. 실행 환경은 Python 3.12.14, packaging 26.3, Node 24.22.1, strace 6.13였다. Moment 2.29.4는 잠근 tar를 로컬에서 해제했다. 테스트에 이용한 호스트 OS의 tzdata.zi는 2026b, Node의 ICU 시간대 자료는 2026e 표기였다. 파일 해시와 실제 로드 주소는 별도다. [공통 의존](evidence/acquisition.json) · [실행 영수증](evidence/run-receipts.json)

## 시작과 고정 파일 재실행

실제 시작 명령은 branch의 최초 커밋에서 실행했고 exit 0이었다. 최초 커밋과 당시 원격 통합 계약은 [manifest.json](manifest.json)에 있다.

```sh
python -B -m workbench.session start af-res-059 \
  --allow docs/workstreams/research/AF-RES-059/ \
  --output docs/workstreams/research/AF-RES-059/manifest.json \
  --dependency work/research-af-res-055=1b86aeb35a2b93ebcd752d903eb66e702748ba66 --fetch
```

GitHub에서 고정 결과 checkout을 열고 아래를 실행한다. 셸 도구와 언어 버전을 위와 같이 준비한다. 현재 registry를 다시 투영하면 바깥 버전이 늘 수 있다. `replay.py`는 커밋된 fixture의 파일 이름과 SHA-256을 대조하고, 달라진 아카이브를 거절한다.

```sh
af059_docs=docs/workstreams/research/AF-RES-059
af059_run=$(mktemp -d /tmp/af059-replay.XXXXXX)
python -B "$af059_docs/catalog.py" "$af059_run/discovery"
python -B "$af059_docs/replay.py" run "$af059_run/discovery/archives" "$af059_run/replay"
python -B "$af059_docs/cost-probe.py" "$af059_run/costs" "$af059_run/discovery/archives"
python -B -m workbench.session check "$af059_docs/manifest.json" --fetch
```

이번 명령의 입력은 `/tmp/af059-evidence/discovery`, `/tmp/af059-evidence/replay-2`, `/tmp/af059-evidence/record-costs-v2`였다. 첫 실행 실패와 재실행 stdout·stderr 해시 및 종료코드는 영수증에 있다. 비용 첫 예비 실행 뒤 저장 레코드를 디스크에서 다시 읽는 측정을 명시했고, 위 v2의 결과를 보존했다. 로더 stdout과 trace의 전체 해시는 시간·절대 경로에 의존한다. 재현 비교에서는 분배 식별자, 파일 SHA, 도시·UNIX 시각, 세 출력, 상대 멤버와 해시를 맞춘다. 같은 휠을 푼 경로에서 Python은 시스템 검색을 거치지 않는 from_file을 사용한다. `replay.py`의 별도 실험에서만 시스템 및 패키지 fallback을 연다. [실제 값](runs.jsonl) · [실패와 경로](evidence/run-receipts.json)

목록과 관계없이 보존판을 직접 받으려면 아래를 쓴다. 입력 파일은 `evidence/acquisition.json` 안의 `files[comparison == full]` + `moment`다. 확인용 sdist는 `files` 전부를 순회한다. 비어 있는 내용이나 달라진 digest는 사용하지 않는다.

```sh
af059_docs=docs/workstreams/research/AF-RES-059
af059_run=$(mktemp -d /tmp/af059-pin.XXXXXX)
PYTHONPATH="$af059_docs" python -B - "$af059_docs/evidence/acquisition.json" "$af059_run" <<'PY'
import json
import sys
from pathlib import Path
from catalog import HttpJournal, digest, verify

manifest = json.loads(Path(sys.argv[1]).read_text())
target = Path(sys.argv[2]) / "archives"
target.mkdir()
http = HttpJournal()
for row in [*manifest["files"], manifest["moment"]]:
    blob = http.get(row["original_url"])
    if blob is None or not verify(blob, row) or digest(blob) != row["observed_sha256"]:
        raise SystemExit(f"Missing or changed: {row['filename']}")
    (target / row["filename"]).write_bytes(blob)
print(target)
PY
python -B "$af059_docs/replay.py" run "$af059_run/archives" "$af059_run/replay"
```

기본 파일의 wheel·sdist·tag 비교는 `unzip -p ARCHIVE tzdata/zoneinfo/Asia/Beirut`, `tar -xOf SDIST MEMBER`, `git -C python-tzdata show TAG:src/tzdata/zoneinfo/Asia/Beirut` 각각을 SHA-256으로 비교했다. 같은 원리로 New York, `tzdata.zi`, `__init__.py`를 읽었다. npm은 `tar -xOf ARCHIVE package/data/packed/latest.json`과 공개 저장소의 두 JSON 경로를 비교했다. 상류 원규칙은 `git -C tz show TAG:asia`와 `TAG:northamerica`의 고정 원문을 읽었다. 이번에 IANA tar를 재구성하거나 빌드하지 않았다. 체크아웃은 공개 저장소 `eggert/tz`, `python/tzdata`, `moment/moment-timezone`의 태그 해제를 사용했다. [태그 SHA·시각](editions.csv) · [비교 해시](evidence/distribution-members.json)

## 소비 증거와 Grafana 이미지

GitHub connector로 두 저장소 `/releases?per_page=30&page=N`의 날짜를 조회했다. 판은 [소비 프레임](evidence/consumer-releases.json)의 `selected`다. `git fetch --depth=1 --filter=blob:none --no-tags origin tag TAG`로 공개 태그를 받았다. `git ls-tree --full-tree -r --name-only SHA`로 잠금 후보를 찾고, `https://raw.githubusercontent.com/REPO/SHA/PATH`에서 핀 파일을 읽었다. PyPI `pandas/VERSION/json`의 고정 CPython 3.11 manylinux x86-64 wheel과 npm `@grafana/data`의 정확한 tar를 검증했다. Grafana GitHub release의 `grafana-spdx.json`을 열어 `packages[]`의 moment-timezone, `sourceInfo`와 `filesAnalyzed`를 확인했다. 날짜창 및 커밋별 공개 Actions GET의 `total_count`를 기록했다. [읽은 파일·행](evidence/consumer-code.json) · [배포물](evidence/consumer-artifacts.json) · [CI](evidence/consumer-ci.json)

9.4.7의 Linux/amd64 OCI 플랫폼 manifest SHA는 `sha256:0f937ad695e3dd2029d111003d29d789c0ee06af3043b18c3010dffaf7db1366`이다. 당시 빌드의 보관 대상을 이렇게 다시 열 수 있다. 공개 Docker Hub pull 토큰을 헤더에만 넣고 GitHub나 터미널에 기록하지 않는다. 이미지 레이어는 정적 데이터로 읽는다.

```sh
af059_oci=https://registry-1.docker.io/v2/grafana/grafana
af059_token=$(curl -fsS 'https://auth.docker.io/token?service=registry.docker.io&scope=repository%3Agrafana%2Fgrafana%3Apull' | python -c 'import json,sys;print(json.load(sys.stdin)["token"])')
af059_digest=sha256:0f937ad695e3dd2029d111003d29d789c0ee06af3043b18c3010dffaf7db1366
af059_layer=sha256:73f9505ae0ff9dfd5594b9253b15acb1e497dc9ba03c6f602788d1de383563e8
curl -fsS -H "Authorization: Bearer $af059_token" \
  -H 'Accept: application/vnd.docker.distribution.manifest.v2+json' \
  "$af059_oci/manifests/$af059_digest" -o "$af059_run/grafana-manifest.json"
curl -fsSL -H "Authorization: Bearer $af059_token" \
  "$af059_oci/blobs/$af059_layer" -o "$af059_run/grafana-public.tgz"
unset af059_token
sha256sum "$af059_run/grafana-manifest.json" "$af059_run/grafana-public.tgz"
tar -xOf "$af059_run/grafana-public.tgz" usr/share/grafana/public/build/app.93e19703a531ea03eb9d.js > "$af059_run/grafana-frontend.js"
python -B - "$af059_run/grafana-frontend.js" <<'PY'
import hashlib
import json
import pathlib
import sys

js = pathlib.Path(sys.argv[1]).read_bytes()
content, length = json.JSONDecoder().raw_decode(js[93605:].decode())
canonical = json.dumps(content, sort_keys=True, separators=(",", ":")).encode()
assert content["version"] == "2022e"
assert hashlib.sha256(canonical).hexdigest() == "ffcd75013ca57410ad97303f9e708116d088e295ec8d469c7b6ef722e1134d63"
print(content["version"], len(content["zones"]), length, hashlib.sha256(js).hexdigest())
PY
```

같은 digest 계산은 하류 npm 0.5.38 tar의 `package/data/packed/latest.json`에서도 맞는다. 직접 재생에는 위 JS에서 뽑은 JSON 바이트를 0.5.38 해제본의 `node_modules/moment-timezone/data/packed/latest.json` 위치에 놓고 `read-packed.cjs JOB`을 실행했다. JOB의 네 입력과 실행 해시, 이미지/레이어/JS/JSON 각각의 해시는 [이미지 영수증](evidence/grafana-image.json)에 있다. 공식 Linux standalone tar는 CONNECT 403이었다. 셸 접근이 가능한 환경에서 `https://dl.grafana.com/oss/release/grafana-9.4.7.linux-amd64.tar.gz`와 공개 SHA `1e22abd627abd77c5496bc2c26bc68eb4c30aa688f7336b6a0e2c87cc80559cd`를 비교하면 두 배포 형식 사이의 근거가 추가된다. [유지보수자 파일 목록](https://grafana.com/grafana/download/9.4.7?edition=oss)

## 미확인 통계 입력

다음은 실제 접근이 실패한 명령 입력이다. 셸이 CONNECT 403, 웹에서는 해당 CSV 접속 실패, Cloud Chrome에서는 URL 요구조건 읽기 실패였다. ALFRED가 보이는 환경에서 먼저 공식 다운로드 페이지에서 두 빈티지 날짜를 확인한다. 동일 계열 ID를 날짜마다 반복해 열 이름과 관측월을 검사한다.

```sh
af059_jolts=$(mktemp -d /tmp/af059-jolts.XXXXXX)
curl -fLsS --max-time 45 'https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=JTSJOL,JTSJOL&vintage_date=2024-03-06,2024-04-02&cosd=2024-01-01&coed=2024-01-01' \
  -D "$af059_jolts/headers" -o "$af059_jolts/jtsjol.csv"
sha256sum "$af059_jolts/jtsjol.csv"
python -B - "$af059_jolts/jtsjol.csv" <<'PY'
import csv
import sys
with open(sys.argv[1], encoding="utf-8-sig") as source:
    reader = csv.DictReader(source)
    expected = ["observation_date", "JTSJOL_20240306", "JTSJOL_20240402"]
    assert reader.fieldnames == expected, reader.fieldnames
    result = next(row for row in reader if row["observation_date"] == "2024-01-01")
    assert all(result[c] for c in expected), result
    print(result)
PY
```

날짜가 확인되면 `evidence/jolts.json`에 원본/최종 주소, 당시 빈티지 날짜, 발행기관 원표 행, 열 이름·관측행·해시를 각각 추가한다. [두 BLS 판과 ALFRED 결손](evidence/jolts.json) · [ALFRED 날짜 선택](https://alfred.stlouisfed.org/series/downloaddata?seid=JTSJOL)
