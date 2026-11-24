# AF-RES-111 재생

Python 3.12와 표준 라이브러리 SQLite, Git을 사용했다. [원형 핀](https://github.com/laadkke-arch/agentflow-open/tree/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db)은 읽기 전용이다. 명령은 Git checkout 최상위에서 실행한다. 인계에 적힌 검사 결과 SHA에 detached checkout한다.

```sh
git clone --branch work/research-af-res-111 --single-branch https://github.com/laadkke-arch/agentflow-open.git
cd agentflow-open
git fetch origin fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c
af_result=$(git log -1 --format=%H --grep='^Report AF-RES-111 results and local verification$')
test -n "$af_result"
git switch --detach "$af_result"
af_path=docs/workstreams/research/AF-RES-111
af_scratch=$(mktemp -d)
python -B "$af_path/tools/run.py" --out "$af_scratch/replay-1"
python -B "$af_path/tools/run.py" --out "$af_scratch/replay-2"
python -B "$af_path/tools/verify.py" --replay "$af_scratch/replay-1" --replay "$af_scratch/replay-2" --summary "$af_scratch/metrics.json"
python -B "$af_path/tools/tables.py" > "$af_scratch/tables.md"
python -B "$af_path/tools/check_captures.py" --out "$af_scratch/source-spans.json"
python -B -m workbench.session check "$af_path/manifest.json" --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

각 재생은 새 출력 디렉터리를 사용한다. `A.sqlite`, `B.sqlite`의 36개 판정과 `original-history.sqlite`의 원형 재시도·수정은 물리 파일에 커밋한다. 교정은 별도 빈 파일 DB 2개를 쓰며, 보조 대조는 각 한 번의 메모리 DB를 쓴다. 실행 종료 후 [원장](runs.jsonl), [간선](links.csv), [수명주기](lifecycle.csv), 교정과 보조 대조의 다섯 출력 지문이 두 재생에서 같은지 확인한다. 앱의 `created_at`과 실행 시간은 별도 관측으로 취급한다.

실행의 세 입력은 `inputs.jsonl`, `facts.jsonl`, `rules.json`이다. opaque 요청 ID와 표의 요청 ID를 잇는 [대조표](evidence/blind-map.jsonl), 작성자 설명과 gold는 독립 검산기에서 읽는다. `links.csv`의 각 행은 조건별로 검토한 출처 절 하나다. `used=True`는 SQLite `run_claim`의 실제 활성 간선에 대응한다. `False`는 거절·미확인 원인과 원 구간을 함께 남긴다. 두 방식의 저장된 후보 컨텍스트는 같은 부분지도와 같은 판을 받는다.

원 요청은 GitHub issue HTML의 embedded raw body 또는 GitLab 공개 issue API의 description/title로 재확인한다. `check_captures.py`는 원 판의 전체 텍스트 지문과 원문 Unicode 반개구간을 함께 대조한다. 이슈가 편집되면 원 링크와 실패 지문을 남기고, 고정된 인용 사본으로 DB 판정만 재생한다. `run.py`에는 외부 이슈를 다시 가져오는 단계가 없다.

[모집 검색 파라미터와 결과 ID](evidence/recruitment.json), [원순번](frame.csv), [원저작·접근 관측](sources.jsonl)을 함께 읽는다. ExifTool 원포럼 비회원 검색 제한과 FreeCAD Mantis 이관시각의 정밀도는 여기에 표시했다. 새 후보를 뽑을 때는 이미 봉인된 표의 지표와 별도 원장을 만든다.

`tools/tables.py` 출력은 [RESULT](RESULT.md)의 첫 세 표에 해당한다. 입력·비교·해석 범위는 [SCOPE](SCOPE.md)와 [SELF_CHECK](SELF_CHECK.md), 검사판과 커밋·명령 영수증은 [HANDOFF](HANDOFF.md)에서 확인한다.
