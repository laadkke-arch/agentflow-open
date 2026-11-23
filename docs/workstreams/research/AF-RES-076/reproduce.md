# AF-RES-076 재현

저장소 루트에서 시작한다. 오프라인 원장 재생은 표준 라이브러리만 쓴다. 당시 HTTP 시도·원문 창·바이트·시간을 `experiment/captures.jsonl`로 읽고, 초기 점수부터 세 열람과 최종 순위를 다시 계산한다. 원문 전체는 외부 고정 SHA에서 접근한다. 원문 파싱과 발행판 지문을 확인하려면 별도 라이브 명령을 실행한다. 재생은 당시의 시간 필드를 보존한다.

## 두 개의 오프라인 원장 대조

```bash
af076="$(realpath docs/workstreams/research/AF-RES-076)"
af076_tmp="$(mktemp -d)"
for run in replay-a replay-b
do
  target="$af076_tmp/$run"
  mkdir -p "$target/packet/input" "$target/output"
  cp "$af076"/experiment/inputs/*.jsonl "$target/packet/input/"
  cp "$af076"/experiment/search.py "$target/packet/search.py"
  cp "$af076"/experiment/captures.jsonl "$target/packet/captures.jsonl"
  (cd "$target/packet" && python -B search.py input "$target/output" --replay captures.jsonl) || exit 1
  python -B "$af076/experiment/costs.py" "$af076" \
    "$target/output/route-costs.csv" "$target/output/costs.csv" || exit 1
  python -B "$af076/experiment/analyze.py" "$af076" "$target/output" || exit 1
done
python -B "$af076/experiment/verify.py" "$af076" \
  "$af076_tmp/replay-a/output" "$af076_tmp/replay-b/output"
```

각 재생의 `ranks.csv`, `fetches.jsonl`, `route-costs.csv`, `costs.csv`, `slots.csv`, `metrics.json`, 어휘 기여와 세 표 MD를 대조했다. 순위·표시 재생은 기대표가 없는 패킷에서 실행했다. 비용 재계산과 기대/관찰의 결합은 그 뒤 단계다. 출력 지문과 바이트는 감사 영수증에 있다. [검산과 두 지문](evidence/audit.json) · [라이브 입력과 출력 지문](evidence/rank-seal.json)

## 같은 판의 기능·채점기

```bash
af076=docs/workstreams/research/AF-RES-076
af076_runtime="$(mktemp -d)"
python -m pip install --target "$af076_runtime" -r "$af076/experiment/requirements.txt"
PYTHONPATH="$af076_runtime" python -B "$af076/experiment/controls.py"
python -B "$af076/experiment/judge.py" "$af076/experiment/grader-fixtures.jsonl"
```

Pillow 12.0.0, DuckDB 1.4.3, CPython 3.12.14 Linux x86_64에서 실행했다. T-01∼T-06은 생성한 픽셀·로컬 CSV·로컬 SQL 입력과 예상 출력을 코드에 포함한다. T-07은 JPEG 2000 코덱이 있는 wheel로 실행한 PDF 신호 비교다. T-08은 외부 네트워크 없이 로컬 파일명 계산을 비교한다. 두 추가 실행은 자연 요구의 원 환경 확인과 별개다. [구현과 입력](experiment/controls.py) · [고정 결과](evidence/controls.json) · [채점 분기](evidence/grader-pretest.json)

Pillow의 원 시험 세 선택자는 태그 커밋에서 `Tests`가 있는 작업폴더로 가져온 후 실행한다. 실제로 선택한 파일과 함수는 receipt에 기록했다. DuckDB의 `csv_rejects_read.test` L9–21은 태그의 `data/csv/error/mismatch/bad.csv`를 읽었고 `test_delete.test` L8–26의 SQL도 실행했다. DuckDB 1.4.3 Python 드라이버에서 대응 블록만 실행했으며 C++ sqllogictest 전체 실행은 별개다. [Pillow 실행](evidence/upstream-pillow.json) · [DuckDB SQL 실행](evidence/upstream-duckdb.json)

```bash
af076_pillow="$(mktemp -d)"
git clone --depth 1 --branch 12.0.0 https://github.com/python-pillow/Pillow.git "$af076_pillow/upstream"
python -m pip install --target "$af076_runtime" pytest==8.3.4
(cd "$af076_pillow/upstream" && PYTHONPATH="$af076_runtime" python -B -m pytest -p no:cacheprovider -q \
  Tests/test_image_thumbnail.py::test_aspect \
  Tests/test_imagecolor.py::test_hash \
  Tests/test_image_crop.py::test_wide_crop)
```

## 라이브 비용과 사후 한 원문 대조

```bash
af076="$(realpath docs/workstreams/research/AF-RES-076)"
af076_live="$(mktemp -d)"
mkdir -p "$af076_live/packet/input"
cp "$af076"/experiment/inputs/*.jsonl "$af076_live/packet/input/"
cp "$af076"/experiment/search.py "$af076_live/packet/search.py"
(cd "$af076_live/packet" && python -B search.py input "$af076_live/output" --live)
python -B "$af076/experiment/costs.py" "$af076" \
  "$af076_live/output/route-costs.csv" "$af076_live/output/costs.csv"
python -B "$af076/experiment/targeted.py" "$af076" "$af076_live/targeted-windows.jsonl"
```

라이브 응답을 고정 SHA-256과 대조한다. 요청당 세 열람, 1 MiB 본문, 750 표시 단어의 예산을 강제한다. 요청마다 빈 원문 캐시를 만들고 같은 요청의 즉시 반복에서만 보유 본문을 사용한다. S/E 제목과 설명, 화면 주소와 판도 표시량에 포함한다. 동률은 ID 오름차순이고 최대 14개 연속 원문 줄, 108단어의 질의 교집합이 같은 창은 먼저 나온 줄을 사용한다. 검색어 정규화와 불용어는 코드에 있다. [검색·표시 코드](experiment/search.py) · [시도별 비용 원장](fetches.jsonl)

표시 패킷을 새로 만들려면 아래 명령을 실행한다. 동일한 창의 개별 판독 여부를 읽을 수 있고, 기대표와의 결합은 후속 단계에서만 한다.

```bash
python -B "$af076/experiment/display.py" "$af076" "$af076_live/for-reader.jsonl"
python -B -m workbench.session check "$af076/manifest.json" --fetch
```
