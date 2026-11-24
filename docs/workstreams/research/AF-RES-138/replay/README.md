# AF-RES-138 재생

Git과 Python 3.12 표준 라이브러리가 필요하다. AF-RES-134의 첫 글 분리·투영·점수·동점·Gate와 AF-RES-122/126의 카드·경계 처리를 고정 SHA에서 불러온다. AF-RES-138은 모집 창의 동점 처리, 네 번째 표시 정책, 원장 검산을 구현한다. 첫 본문의 전체 Markdown과 답글은 임시 폴더에서 열고 필요한 최소 구절과 지문을 보관한다.

저장소 루트에서 아래 블록을 실행한다.

```sh
af138=docs/workstreams/research/AF-RES-138
af122=docs/workstreams/research/AF-RES-122
af126=docs/workstreams/research/AF-RES-126
af134=docs/workstreams/research/AF-RES-134
pin122=e69a3f837d400ba8a4820edb5bcd91223dc5f9cc
pin126=abcdda426e2a2d19f0732752c221ea4d494458c4
pin134=a21414017323dbd7a090b1e7b62f070d4fa1a1ab
scratch138=$(mktemp -d)
git fetch --no-tags origin "$pin122" "$pin126" "$pin134"
mkdir -p "$scratch138/af122" "$scratch138/af126" "$scratch138/af134"
git archive "$pin122" "$af122/catalog.csv" "$af122/aliases.csv" "$af122/prepare.py" \
  "$af122/replay.py" "$af122/evidence/query-inputs.jsonl" "$af122/evidence/controls-query-inputs.jsonl" |
  tar -x -C "$scratch138/af122" --strip-components=4
git archive "$pin126" "$af126/capture.py" "$af126/replay.py" |
  tar -x -C "$scratch138/af126" --strip-components=4
git archive "$pin134" "$af134/replay/acquire.py" "$af134/replay/project.py" "$af134/replay/run.py" |
  tar -x -C "$scratch138/af134" --strip-components=5

for seed138 in 0 37; do
  PYTHONHASHSEED="$seed138" python -B "$af138/replay/run.py" \
    --af122 "$scratch138/af122" --af126 "$scratch138/af126" --af134 "$scratch138/af134" \
    --out "$scratch138/run-$seed138" > "$scratch138/replay-$seed138.json"
  python -B "$af138/replay/verify.py" --replay "$scratch138/run-$seed138" \
    > "$scratch138/recount-$seed138.json"
done
diff -rq "$scratch138/run-0" "$scratch138/run-37"
cmp "$scratch138/replay-0.json" "$scratch138/replay-37.json"
cmp "$scratch138/recount-0.json" "$scratch138/recount-37.json"
```

## 첫 본문 재취득

고정 창을 확인할 때는 커밋된 창을 입력한다. 새 검색 응답은 새 시점의 관측으로 저장한다.

```sh
python -B "$af138/replay/collect.py" search --af134 "$scratch138/af134" --out "$scratch138/new-search"
python -B "$af138/replay/collect.py" openings --af134 "$scratch138/af134" \
  --window "$af138/evidence/window.jsonl" --out "$scratch138/openings"
python -B "$scratch138/af134/project.py" --requests "$af138/requests.jsonl" \
  --opening "$scratch138/openings/openings.jsonl" --af122 "$scratch138/af122" \
  --af126 "$scratch138/af126" --out "$scratch138/fresh-inputs.jsonl"
cmp "$scratch138/fresh-inputs.jsonl" "$af138/replay/inputs.jsonl"
```

본문이 편집됐거나 첫 구절이 달라지면 투영기가 지문 검사에서 멈춘다. 이후 새 본문 판독은 모집·표시·기준·순위 순서로 남긴다. 저장된 다섯 원문에는 존재하는 조사형만 보존한다. 발행·편집 이력 전체와 실제 클릭 비용은 별개 관측이다.

`verify.py`는 카드 점수와 판정표를 받아 양수·정렬·게이트·자리 순서를 독립적으로 다시 계산한다. 정책 간 집합 차이, 원문 및 출처 연결, 층별 분모와 공석을 검산한다. 독립 판독자의 적합성 평가는 이 검산의 범위 밖이다.
