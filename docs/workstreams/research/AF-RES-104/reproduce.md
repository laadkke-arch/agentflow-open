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
