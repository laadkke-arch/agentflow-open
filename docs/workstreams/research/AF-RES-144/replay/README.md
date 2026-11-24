# CLI 다시 실행

Linux amd64, Python 3.12, uv, curl, tar, Git, C 컴파일러, make와 CPython용 bz2/lzma 개발 헤더·라이브러리가 필요하다. `C.UTF-8`, `en_US.utf8`를 사용했고 `en_GB.UTF-8`이 구동되지 않는 환경의 오류도 비교에 남겼다. OS 로케일이 달라지는 경우 해당 CLI 행을 환경 차이로 검토한다. [빌드 영수증](../evidence/build-notes.md)

저장소 루트에서 실행한다. 인수 디렉터리는 새 경로이고 설치와 빌드는 저장소 밖 임시 폴더에서 진행한다.

```sh
af_study=docs/workstreams/research/AF-RES-144
af_scratch=$(mktemp -d /tmp/af144.XXXXXX)
python -B "$af_study/replay/bootstrap.py" "$af_scratch/tools"
"$af_scratch/tools/yaml-reader/bin/python" -B "$af_study/replay/run_csv.py" "$af_scratch/tools" "$af_scratch/csv" > "$af_scratch/runs.jsonl"
"$af_scratch/tools/yaml-reader/bin/python" -B "$af_study/replay/run_yaml.py" "$af_scratch/tools" "$af_scratch/yaml" >> "$af_scratch/runs.jsonl"
python -B "$af_study/replay/verify.py" --replay "$af_scratch/runs.jsonl"
python -B -m workbench.session check "$af_study/manifest.json" --fetch
```

같은 명령을 다른 `af_scratch`에서 반복할 수 있다. `bootstrap.py`는 Linux amd64 yq 아카이브 멤버와 CPython 소스 SHA-256을 확인하고 고정 의존으로 venv를 만든다. 개발 헤더가 로컬 scratch에 이미 있다면 `--build-includes <absolute-dir> --build-libraries <absolute-dir>`를 사용할 수 있다. 이 연구에서 시스템 설치 없이 준비한 실제 방법과 패키지 판은 build-notes.md에 있다. 독립 판독은 PyYAML 6.0.2/libyaml을 사용한다. CSV는 별도 CPython 3.12의 csv.reader와 단순 TSV 독자를 사용했다.

fixture 생성만 하려면 `python -B "$af_study/replay/fixtures.py" --to "$af_scratch/input"`을 쓴다. 실행 드라이버는 fixture를 각 명령용 새 폴더에 기록하며 파일 byte 지문과 종료·변경 상태를 JSONL로 출력한다. C4 파이프를 구성하는 두 CLI를 순서대로 실행해 첫 명령의 stdout bytes를 그대로 두 번째 stdin에 전달한다. C3에서 종료 1의 부분 stdout과 C4/Y2의 실패 stdout/stderr를 보존한다.

시계의 공개 HTML과 개별 REST를 재수집할 때 `python -B "$af_study/replay/inspect_issues.py" "$af_scratch/timeline.csv" "$af_scratch/clock.json"`을 실행한다. 이번 최초 shell 경로는 REST 연결이 막혔고 후속의 GitHub 원시 REST 읽기로 그 필드를 보완했다. 당시 bodyVersion, 한계와 연결 방법은 [공개 HTML](../evidence/public-clock.json), [REST](../evidence/github-rest.json)에 남겼다.
