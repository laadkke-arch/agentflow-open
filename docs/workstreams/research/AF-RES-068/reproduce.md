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

## 고정 배포 실행

최초 실행 `dd41f04279f50cc083c6a442fef5bb32803a49fb`의 probe를 쓰면 Node v24.22.1/npm 11.9.0에서 생긴 원 실행을 재현할 수 있다. JSON-LD 두 시리즈는 이 조합에서 `esm` 로더 TypeError로 메서드 진입 전 종료 1이었다. 현재 probe의 JSON 복사와 예외 단계 분리는 이 실패 이후 변경이며, 초기 실행 stdout의 stage 이름을 검산할 때 초기 커밋을 사용한다. 두 시리즈에 같은 fixture bytes와 npm lock을 사용한 Node v14.18.3 재시도는 별도로 저장했다. [최초 출력](evidence/runtime) · [재시도와 Node 배포 해시](evidence/runtime-recovery) · [검증군·시도 원장](runs.jsonl)

```sh
python -B "$study/run_fixtures.py" --locks "$study/evidence/runtime" --scratch "$scratch/node24" --output "$scratch/node24-out"
mkdir "$scratch/node14-release"
cd "$scratch/node14-release"
curl -fsSLO https://nodejs.org/dist/v14.18.3/SHASUMS256.txt
curl -fsSLO https://nodejs.org/dist/v14.18.3/node-v14.18.3-linux-x64.tar.xz
rg '  node-v14.18.3-linux-x64.tar.xz$' SHASUMS256.txt | sha256sum -c
tar -xJf node-v14.18.3-linux-x64.tar.xz node-v14.18.3-linux-x64/bin/node
python -B "$study/run_fixtures.py" --case L01 --case L02 \
  --node "$scratch/node14-release/node-v14.18.3-linux-x64/bin/node" \
  --locks "$study/evidence/runtime" --scratch "$scratch/node14" --output "$scratch/node14-out"
```

L01은 저자가 보고한 출력 포맷 비교를 위해 N-Quads 문자열과 RDFJS dataset 반환을 같은 inline 입력·옵션에서 각각 읽는다. 두 출력의 JSON-encoded 구조 해시와 `termType`/값을 본다. L02는 alias 및 해당 값·자료형을 따로 확인한다. npm 설치와 Node 평가의 런타임은 별도이며 14.18.3 재시도의 npm은 24.22.1 엔진으로 실행했다. URL 호출이 발생하면 loader가 즉시 오류를 반환하게 했다.

## 검산과 작업 계약

```sh
python -B "$study/audit.py" --report --replayed "$scratch/all-1" --replayed "$scratch/all-2"
python -B -m workbench.session check docs/workstreams/research/AF-RES-068/manifest.json --fetch
```

검산은 모집·경로 순서와 연결, 창의 원문 위치·SHA, 자료 계보, 문서 판정의 경로 내 위치, 실행의 입력·출력 byte/값 및 표 행 수를 비교한다. 원작성자 당시 런타임과 사람이 본 화면의 동일성은 이 검사에서 미확인이다.
