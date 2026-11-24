# AF-RES-143 재생 명령

루트는 깨끗한 결과 커밋의 Git 체크아웃이다. Python 3.12, Node v24.22.1, npm 11.9.0, Linux, TZ UTC, C.UTF-8을 사용한다. 단일 명령에서 읽는 두 실행 경로는 서로 다른 디렉터리 및 npm 캐시를 갖는다.

```sh
task=docs/workstreams/research/AF-RES-143
scratch=$(mktemp -d /tmp/af143-replay.XXXXXX)
python -B "$task/replay/prepare.py" --scratch "$scratch/static" --out "$scratch/frozen"
python -B "$task/replay/run.py" --label A --scratch "$scratch/A" --out "$scratch/A.jsonl"
python -B "$task/replay/run.py" --label B --scratch "$scratch/B" --out "$scratch/B.jsonl"
python -B "$task/replay/compare.py" --first "$scratch/A.jsonl" --second "$scratch/B.jsonl" --out "$scratch/compare"
python -B "$task/replay/run.py" --label CAL --calibration --scratch "$scratch/cal" --out "$scratch/calibration.jsonl"
python -B "$task/replay/join.py" --out "$scratch/joined"
python -B "$task/replay/measure.py" --scratch "$scratch/cost" --out "$scratch/measure"
python -B "$task/replay/audit.py" --rebuilt "$scratch/compare" --fresh-run "$scratch/A.jsonl" --fresh-run "$scratch/B.jsonl"
python -B -m workbench.session check "$task/manifest.json" --fetch
```

첫 명령은 현재 공지의 편집 시각이 달라지거나 태그가 이동했는지 드러내는 정적 재수집이다. 예측 평가는 봉인한 predictions.csv를 사용한다. 새 실행 경로는 저장한 lock, 입력, 실제 타르 URL과 무결성을 사용하고 출력 전용 비교에 예측표를 주지 않는다. 대형 인수의 반복 전후는 지문과 고정 생성 입력으로 보존한다.
비용은 각 정책에 빈 로컬 캐시와 직후 보존 캐시를 주고 세 번 반복한다. 정적 Acorn 설치는 공통 준비이며 실제 요청 비용은 HTTP 본문과 잠금 오프라인 npm/Node에서 계측한다. 측정값이 달라져도 이전 영수증을 새 값으로 덮어쓰지 않는다.
