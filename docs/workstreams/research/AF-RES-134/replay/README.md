# AF-RES-134 재생과 원문 확인

Python 3.12 표준 라이브러리와 Git을 사용한다. AF-RES-122 고정판에서 16개 카드·별칭·심벌 투영·점수와 정렬을, AF-RES-126 고정판에서 NFC 후 한국어 어절 보존·한 조사 검출·B/C를 사용한다. 이 워크스트림의 코드는 공개 첫 본문 수집, 저장용 투영, Gate의 표시 3 적용, 분모와 원장 검증을 담당한다. 이전 요청/구성문 투영 파일 두 개는 AF-RES-122의 공용 입력 로더가 읽으며 이번 요청 순위를 내는 루프에는 들어가지 않는다. 카드나 알고리즘 복사본을 저장하지 않았다.

## 고정 결과 재생

브랜치 checkout 루트에서 실행한다. `--out`은 비어 있는 임시 디렉터리로 지정한다.

```sh
af134=docs/workstreams/research/AF-RES-134
af122=docs/workstreams/research/AF-RES-122
af126=docs/workstreams/research/AF-RES-126
pin122=e69a3f837d400ba8a4820edb5bcd91223dc5f9cc
pin126=abcdda426e2a2d19f0732752c221ea4d494458c4
git fetch --no-tags origin "$pin122" "$pin126"
scratch134=$(mktemp -d)
mkdir -p "$scratch134/af122" "$scratch134/af126"
git archive "$pin122" "$af122/aliases.csv" "$af122/catalog.csv" "$af122/prepare.py" \
  "$af122/replay.py" "$af122/evidence/query-inputs.jsonl" "$af122/evidence/controls-query-inputs.jsonl" |
  tar -x -C "$scratch134/af122" --strip-components=4
git archive "$pin126" "$af126/capture.py" "$af126/replay.py" |
  tar -x -C "$scratch134/af126" --strip-components=4
for af134_seed in 0 37; do
  PYTHONHASHSEED="$af134_seed" python -B "$af134/replay/run.py" \
    --af122 "$scratch134/af122" --af126 "$scratch134/af126" --out "$scratch134/run-$af134_seed"
done
diff -rq "$scratch134/run-0" "$scratch134/run-37"
cmp "$af134/ranks.csv" "$scratch134/run-0/ranks.csv"
for af134_name in slots.csv transitions.csv editor-cost.csv metrics.csv alias-audit.csv; do
  cmp "$af134/evidence/$af134_name" "$scratch134/run-0/$af134_name"
done
python -B "$af134/replay/recount.py"
```

[실제 별도 프로세스 영수증](../evidence/replay-validation.json)에서는 순위 묶음 SHA의 작업 경로와 선행 코드를 두 디렉터리로 각각 Git archive했다. 첫 게시물을 두 번 다시 받았으며 두 프로세스 모두 초판 관측 본문 지문·구절·투영과 일치했다. 두 번의 B/C/Gate 결과 6개 CSV가 커밋본과 일치했다.

## 원문을 재취득하는 명령

원문 첫 본문은 임시 UTF-8 JSONL로 사용한다. 접근 가능한 GitHub 공개 페이지에서 locator를 다시 확인한 후 아래 입력을 만들 수 있다.

```sh
python -B - "$af134/requests.jsonl" > "$scratch134/selected.jsonl" <<'PY'
import json
import sys
from pathlib import Path
for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    row = json.loads(line)
    print(json.dumps({key: row[key] for key in ("repository", "issue_number", "created_at", "position")}))
PY
python -B "$af134/replay/acquire.py" openings --window "$scratch134/selected.jsonl" \
  --out "$scratch134/openings.jsonl"
python -B "$af134/replay/project.py" --requests "$af134/requests.jsonl" \
  --opening "$scratch134/openings.jsonl" --af122 "$scratch134/af122" \
  --af126 "$scratch134/af126" --out "$scratch134/current-inputs.jsonl"
cmp "$scratch134/current-inputs.jsonl" "$af134/replay/inputs.jsonl"
```

본문 편집이나 응답판 변경으로 지문이 달라졌다면 새판으로 구별해 판독과 기준을 다시 봉인한다. 공백·CRLF는 응답의 Markdown에서 보존하고 NFC에서만 정상화한다. 구절 좌표는 NFC 코드포인트이며 바이트 위치가 아니다.

포럼 접근 가능한 환경에서는 아래 JSON 회수를 먼저 실행하고 정상 HTML의 같은 topic과 post_number=1을 대조한다.

```sh
curl -sS -D - --max-time 30 'https://discuss.pytorch.kr/t/6001.json' -o "$scratch134/topic-6001.json"
curl -sS -D - --max-time 30 --get --data-urlencode 'q=가중치' \
  'https://discuss.pytorch.kr/search.json' -o "$scratch134/search-weights.json"
python -B "$af134/replay/acquire.py" forum --receipt "$scratch134/forum-http.jsonl" \
  --out "$scratch134/forum-openings.jsonl"
```

`forum` 모드는 A의 원문 후보와 B 검색 배열을 저장한다. B 응답의 첫 8 ID가 확인되면 질의별 순서대로 같은 공개 JSON/HTML에서 첫 글을 연다. 새 관측 시각을 쓰고 원래의 미접근 기록을 보존한다. GitHub 검색은 `window --layer G1` 또는 `G2-how` 및 `G2-want`를 지정한다. 구문과 페이지 상한은 [수집 코드](acquire.py)와 [모집 확인](../evidence/intake.md)에 있다.
