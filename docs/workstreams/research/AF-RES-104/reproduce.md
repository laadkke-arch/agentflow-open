# AF-RES-104 재현

Python 3.12와 Git을 사용한다. 저장소 루트에서 실행한다. AF-RES-100 실행 파일은 고정판에서 별도 임시 경로로 꺼낸다. 장문 원문·판독용 원문은 임시 경로에만 둔다.

```sh
AF104=$(mktemp -d /tmp/af-res-104.XXXXXX)
OWNED=docs/workstreams/research/AF-RES-104
PRIOR=docs/workstreams/research/AF-RES-100
FIXED=b3f3694b54bb7a85dc7a21e2731841679fc6753c
git fetch origin work/research-af-res-100
git archive "$FIXED" "$PRIOR"/{protocol.json,packets.jsonl,corpus-plan.json,corpus-files.jsonl.gz,restore_corpus.py,packet_builder.py,evidence/packet-descriptors,evidence/corpus-build-receipts.json,evidence/corpus-manifest.json,evidence/compressed-ledgers.json,evidence/ranking} |
  tar -x -C "$AF104"
CACHE="$AF104/$PRIOR"
python -B "$CACHE/restore_corpus.py" --restore > "$AF104/restore.json"
```

기업 프록시에서 고정 API/FTP 호스트가 403이라면 아래처럼 동일 압축 바이트를 넣고 원 복원기에서 SHA, tar 등록 경로 및 본문 SHA를 다시 검증한다. Debian은 GNU sed의 원 배포 압축 파일을 담은 운송 경로다.

```sh
python -B "$OWNED/stage_archives.py" "$CACHE" > "$AF104/staged.json"
python -B "$CACHE/restore_corpus.py" --restore > "$AF104/restore.json"
python -B "$CACHE/restore_corpus.py" --offline > "$AF104/offline.json"
python -B "$OWNED/stage_archives.py" "$CACHE" --original-ranking-inputs
python -B "$CACHE/packet_builder.py" --verify > "$AF104/prior-ranking.json"
python -B -m unittest discover -s "$OWNED" -p 'test_*.py' -v
python -B "$OWNED/select_passages.py" --cache "$CACHE" --output "$AF104/run-1"
python -B "$OWNED/select_passages.py" --cache "$CACHE" --output "$AF104/run-2"
cmp "$AF104/run-1/packets.jsonl" "$AF104/run-2/packets.jsonl"
cmp "$AF104/run-1/packet-costs.json" "$AF104/run-2/packet-costs.json"
cmp "$AF104/run-1/packets.jsonl" "$OWNED/packets.jsonl"
cmp "$AF104/run-1/packet-costs.json" "$OWNED/evidence/packet-costs.json"
```

UTC·실행시간은 비결정 영수증에만 기록한다. 파일 지문과 비용 원장은 반복 일치 대상이다. 줄 번호는 LF를 세며 원문 문자는 CRLF를 포함해 그대로 둔다. UTF-8와 Unicode 좌표는 각각 0부터 시작하는 반열림 구간이다.

## 판독·감사·교차 분야

첫 판독과 사후 감사를 다시 할 때 우선 고정 결과 커밋의 `protocol.json`, `packets.jsonl`과 원 corpus만 제공한다. 제목·R0 주소·사전 조건·불투명 패킷의 판독용 행 단서는 아래 명령으로 복원된다. 정확한 원문 바이트는 같은 도구의 `--raw-segment PACKET SLOT SEGMENT`로 얻는다. 원문을 추적 파일에 저장하지 않는다.

```sh
python -B "$OWNED/reader_input.py" --cache "$CACHE" --case J1
python -B "$OWNED/reader_input.py" --cache "$CACHE" --raw-segment 4e872c3d225e5a26 3 2 | sha256sum
```

주관 판독을 끝내 봉인한 뒤 이전 원장과 상세 실행 접근 파일을 꺼낸다. 뒤늦게 합류한 선행 결과의 브랜치 끝을 파일 위치 기준으로 바꾸지 않는다.

```sh
git archive "$FIXED" "$PRIOR" | tar -x -C "$AF104"
python -B "$CACHE/recompute.py" --check
python -B "$OWNED/audit.py" --cache "$CACHE" --check
python -B "$OWNED/render_tables.py" --check
python -B "$OWNED/crossdomain.py" "$AF104/cross" --download > "$AF104/crossdomain-windows.json"
cmp "$AF104/crossdomain-windows.json" "$OWNED/evidence/crossdomain-windows.json"
python -B "$OWNED/crossdomain.py" "$AF104/cross" --sqlite-runtime
python -B "$OWNED/wpt_probe.py" "$AF104/cross"
```

WPT는 Chromium과 고정 WPT harness 세 파일을 사용하며 주소가 localhost인 임시 서버에서 축 길이 4개를 검사한다. 현 머신에서 launch 오류 및 timeout이 기록됐다. J1 합성의 두 파일과 전체 명령·결과는 [실행 영수증](evidence/j1-synthetic.json)에 있다. Chromium vis reftest를 필요로 하면 고정 WPT ref 파일과 함께 정상 브라우저 환경에서 `./wpt run chrome css/css-grid/grid-items/grid-minimum-size-grid-items-012.html css/css-grid/grid-items/grid-minimum-size-grid-items-018.html`를 실행한다.

```sh
python -B -m workbench.session check "$OWNED/manifest.json" --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```
