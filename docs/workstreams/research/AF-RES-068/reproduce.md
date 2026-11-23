# 재현

Python 3.12.14에서 Markdown-It 3.0.0, mdurl 0.1.2, Docutils 0.21.2를 사용했다. 사용자가 보는 GitHub 브라우저의 픽셀이 아니라 pinned raw의 코드·텍스트 투영이다. 선택에는 공급자 트리·manifest·제목·공개 선언의 [구조화 목록](evidence/selector-metadata.json)과 [가린 입력](selector-cases.json), [심볼 표기](mentions.jsonl)만 사용한다.

저장소 루트에서 실행한다. 결과 작업 폴더의 변경 없이 모든 재생 출력을 임시 디렉터리에 저장한다.

```sh
study="$PWD/docs/workstreams/research/AF-RES-068"
scratch=$(mktemp -d)
python -m venv "$scratch/render"
"$scratch/render/bin/pip" install markdown-it-py==3.0.0 mdurl==0.1.2 docutils==0.21.2
render="$scratch/render/bin/python"
"$render" -B "$study/replay.py" --boundary --output "$scratch/boundary"
cmp "$study/evidence/boundary.json" "$scratch/boundary/boundary.json"
"$render" -B "$study/replay.py" --case A01 --pair AC --cache "$scratch/pair-cache" --output "$scratch/pair"
"$render" -B "$study/replay.py" --cache "$scratch/cache-1" --output "$scratch/all-1"
"$render" -B "$study/replay.py" --cache "$scratch/cache-2" --output "$scratch/all-2"
for n in 1 2; do
  cmp "$study/routes.csv" "$scratch/all-$n/routes.csv"
  cmp "$study/windows.jsonl" "$scratch/all-$n/windows.jsonl"
  cmp "$study/evidence/route-actions.jsonl" "$scratch/all-$n/actions.jsonl"
done
```

`--case L01`처럼 한 요구에 세 경로를 볼 수 있다. **추가 실제 노출**로 기록할 때만 `--emit-text`를 붙인다. 창의 가명과 표시문이 해당 디렉터리에 나온다. 첫 읽기를 재판독하면 그 사실을 원래 실제 엄격 집계와 별도로 남긴다. 499/500/501단어, Markdown/RST code와 원행, 숨긴 이미지와 수식, 긴 한 토큰·구두점 많은 코드와 깨진 앵커는 [경계 기록](evidence/boundary.json)에 있다. 적격 링크가 없었던 실제 경로와 링크가 깨진 합성 경로를 구별한다. `source_index`의 각 행은 raw 시작·끝 줄, 블록 종류, 표시 토큰 번호 범위다. 여러 줄 단락에서 잘린 위치는 표시 줄바꿈으로 경계를 보수적으로 기록한다.

입수 시각과 재사용 여부는 [retrieval.jsonl](evidence/retrieval.jsonl)에 있다. 이를 제외하고 raw SHA와 크기, URL, 창 해시·행·경로 행동을 두 cold cache에서 비교했다. [비교 영수증](evidence/replay-comparison.json)

메타데이터도 같은 커밋으로 재생한다.

```sh
mkdir "$scratch/providers" "$scratch/index"
git clone --bare --filter=blob:none --no-tags https://github.com/ajv-validator/ajv.git "$scratch/providers/ajv.git"
git -C "$scratch/providers/ajv.git" fetch --no-tags origin refs/tags/v8.8.2:refs/tags/v8.8.2 refs/tags/v8.9.0:refs/tags/v8.9.0
git clone --bare --single-branch --branch v5.2.0 --no-tags https://github.com/digitalbazaar/jsonld.js.git "$scratch/providers/jsonld.git"
"$render" -B "$study/select_routes.py" --repos "$scratch/providers" --output "$scratch/index"
cmp "$study/evidence/selector-metadata.json" "$scratch/index/selector-metadata.json"
```
