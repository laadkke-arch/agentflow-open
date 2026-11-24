# AF-RES-110 재생

검사할 결과 SHA를 [HANDOFF.md](HANDOFF.md)에서 고른다. 기록된 DB·순위의 실행 환경은 Python 3.12.14, SQLite 3.53.1 (JSON 및 dbstat 지원)이다. 다른 SQLite 빌드에 다르게 배치된 b-tree의 바이트 지문은 같은 연구 논리의 입력이더라도 달라질 수 있다. 실행은 저장소 루트에서 한다.

```sh
git fetch --no-tags origin refs/heads/work/research-af-res-110:refs/remotes/origin/work/research-af-res-110
git fetch --no-tags origin refs/heads/work/design-gallim:refs/remotes/origin/work/design-gallim
git fetch --no-tags origin refs/heads/work/research-af-res-106:refs/remotes/origin/work/research-af-res-106
git switch --detach RESULT_SHA
python -B docs/workstreams/research/AF-RES-110/tools/prototype.py
python -B docs/workstreams/research/AF-RES-110/tools/replay.py --output /tmp/af110-replay
python -B docs/workstreams/research/AF-RES-110/tools/summarize.py --output /tmp/af110-rebuilt-tables
python -B docs/workstreams/research/AF-RES-110/tools/verify.py --fresh /tmp/af110-replay
python -B -m workbench.session check docs/workstreams/research/AF-RES-110/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
python -B scripts/check.py --require-git
```

`RESULT_SHA`는 설명용 자리다. 결과 SHA가 아니라 최종 HANDOFF SHA를 넣으면 검증판이 달라진다. 교정 코드에 필요한 원형은 `fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c`다. Git blob을 읽고 실행에 필요한 형제 모듈과 SQL은 임시 디렉터리에 푼다. 원형 파일은 수정하지 않는다. 원격 브랜치가 결과판 이후 영수증과 HANDOFF로 전진하기 전에 아래 재열람을 수행했다. 나중에는 명시 결과 SHA 확인 후 브랜치 끝 대신 해당 조상 여부를 대조해 같은 raw URL을 읽을 수 있다.

```sh
python -B docs/workstreams/research/AF-RES-110/tools/readback.py --commit RESULT_SHA --output /tmp/af110-readback.json
```

자연 실험 입력은 `catalog.jsonl`의 48판과 `queries.jsonl` 여섯 쌍이다. 재생 도중 `truth.csv`를 읽지 않는다. 재정렬기의 입력은 카드 `applicability`와 검색문에서 추출한 기술 판·형식·플랫폼 필드다. 검산기는 원 순위 산술을 토큰과 집합으로 별도 계산하고 정답·표·결손을 조합한다. `evidence/replacement-input.json`의 두 검색문은 자연 집계 밖에서 한 카드의 판 교체를 확인한다. 과거/현재 data set 전체 출시를 재구성하는 시험 대신 23개 현행 카드를 그대로 두고 SP-X1만 교체한다.

재생은 임시 DB에서 page_size 4096, cache_size -2048, journal DELETE, synchronous FULL, temp_store MEMORY, auto_vacuum NONE을 쓴다. 한 DB 재생 내부의 순서는 A와 B 생성, en 전체, ko 전체, 각 요청 A→B→C, 동점 별도 조회다. SQL trace는 호출 수만 센다. `ranks.csv`와 교체 결과는 재생판 사이 바이트가 같다. `runs.jsonl`의 경과 시간은 당일 관측이다. 비용 표는 커밋된 관측을 원장에서 다시 생성한다.

요구 모집의 재검사는 `issue-frame.csv`의 프로젝트/시각/번호와 `queries.jsonl`의 원문 위치를 사용한다. GH Archive 파일 이름은 UTC 생성 시각의 `YYYY-MM-DD-H`다. 이번 환경의 직접 API와 아카이브 endpoint가 접근 차단됐다. 다음 검증판에서 최초 본문의 차이를 확인할 정확한 입력은 고정된 여섯 선발 번호와 그 앞의 3083/3084다. GitHub GraphQL 사용은 공개 이슈의 첫 게시물 편집 이력을 읽는 범위다.

```sh
gh api graphql -f query='{ repository(owner:"mkdocs",name:"mkdocs") { a:issue(number:3083){createdAt lastEditedAt includesCreatedEdit userContentEdits(first:20){nodes{editedAt deletedAt diff}}} b:issue(number:3084){createdAt lastEditedAt includesCreatedEdit userContentEdits(first:20){nodes{editedAt deletedAt diff}}} c:issue(number:3085){createdAt lastEditedAt includesCreatedEdit userContentEdits(first:20){nodes{editedAt deletedAt diff}}} } }'
```

편집 이력에서 최초 revision이 보이지 않으면 `https://data.gharchive.org/2023-01-02-12.json.gz` 등 생성 시간의 압축 JSONL에서 `type=IssuesEvent`, `payload.action=opened`, 저장소와 번호를 맞춰 첫 본문을 비교한다. 외부 공개 페이지의 실제 UI 동작은 이 SQLite 재생 범위 밖이다.
