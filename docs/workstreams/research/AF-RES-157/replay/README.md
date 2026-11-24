# AF-RES-157 읽기 전용 재생

Python 3.12 표준 라이브러리로 공개 파일럿 입력 및 집계를 판독한다. 작업 저장소 밖 임시 경로를 만들고 각 출력은 stdout으로 받는다. 사용자·기기·그림 본문은 저장소에 반출하지 않는다.

```sh
AF157_DIR=docs/workstreams/research/AF-RES-157
AF157_TMP="$(mktemp -d)"
AF157_CSV=https://raw.githubusercontent.com/brownhci/sketchy-1.0/f01bb57fbc7f5f14b6bd057b01221f5c3618f69e/data/pilot_data/sketchy_dec6_dec13_peeks_updated.csv
curl -fLsS --max-time 45 "$AF157_CSV" --output "$AF157_TMP/pilot.csv"
sha256sum "$AF157_TMP/pilot.csv"
python -B "$AF157_DIR/replay/pilot.py" "$AF157_TMP/pilot.csv" > "$AF157_TMP/metadata.json"
python -B "$AF157_DIR/replay/pilot.py" "$AF157_TMP/pilot.csv" --selection > "$AF157_TMP/selection.csv"
python -B "$AF157_DIR/replay/observed.py" "$AF157_TMP/pilot.csv" > "$AF157_TMP/snapshots.json"
python -B "$AF157_DIR/replay/observed.py" "$AF157_TMP/pilot.csv" --events > "$AF157_TMP/events.csv"
cmp "$AF157_TMP/metadata.json" "$AF157_DIR/evidence/pilot-metadata.json"
cmp "$AF157_TMP/selection.csv" "$AF157_DIR/selection.csv"
cmp "$AF157_TMP/snapshots.json" "$AF157_DIR/evidence/pilot-snapshots.json"
cmp "$AF157_TMP/events.csv" "$AF157_DIR/events.csv"
python -B "$AF157_DIR/replay/check_ledgers.py"
```

고정 입력은 15,062,721바이트 및 `aec34f174ac350448b62a2223a859303ae496f99ba526775e027e914a4a1afbc`다. 파일럿 196행, 진단 4자리, 엄격쌍 0이 재생된다. `pilot.py`가 입력 지문과 열 구성을 확인한다. `--selection`에는 이번 모집창에서 키가 확인되지 않은 계획 자리도 둔다.

정규화된 입력은 `location,participant,task,document,kind,tick,stimulus,version,snapshot,verified` 열을 요구한다. `tick`은 수집자 확인을 거친 공통 정수시계, `verified=1`은 동작과 버전을 별도 근거로 확인했다는 뜻이다. 저장 `snapshot`은 내용 판별에 쓴 지문이며 실제 공개 작품을 검증하는 시점에 계산해야 한다. 원자료 취득 전 코드가 원시 CSV의 열 이름으로 의미를 추정하지 않는다.

```sh
python -B "$AF157_DIR/replay/strict_join.py" "$AF157_DIR/replay/synthetic.csv" --expected "$AF157_DIR/replay/synthetic-expected.json"
python -B "$AF157_DIR/replay/strict_join.py" "$AF157_DIR/replay/synthetic.csv" --include-multi-stimulus
python -B "$AF157_DIR/replay/strict_join.py" "$AF157_DIR/replay/synthetic.csv" --gap 2 --include-multi-stimulus
```

첫 입력은 모두 인공 27행이다. 위 세 집계의 전체 적격은 2/3/2다. 사람 원자료 출력에는 합산하지 않는다. 다른 공개 아카이브의 입력 검증 절차는 [ACQUISITION](../evidence/ACQUISITION.md)에서 시작한다. 별도 제작판 스크립트는 Blender 로드 시 자동 실행을 끄고 호출한다. 입력 커밋·LFS 해시·명령은 [COMPARISONS](../evidence/COMPARISONS.md)에 있다.
