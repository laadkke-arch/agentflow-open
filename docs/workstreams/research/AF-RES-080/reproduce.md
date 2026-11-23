# AF-RES-080 재현

소유 경로 안의 원장과 스크립트를 결과 커밋에서 읽는다. CPython 3.12.14, Git 및 공개 GitHub/PyPI 접근을 썼다. 입력과 검산 출력의 임시 경로를 분리한다. GitHub 쿼리는 번호와 날짜의 공용 색인 순서를 조회한다.

## 명령

```bash
p=docs/workstreams/research/AF-RES-080
af080_replay="$(mktemp -d)"
python -B "$p/experiment/build_catalogs.py" \
  --versions "$p/evidence/catalog-versions.json" \
  --workspace "$af080_replay/upstream" --output "$af080_replay/catalogs.jsonl"
cmp "$af080_replay/catalogs.jsonl" "$p/catalogs.jsonl"

python -B "$p/experiment/score.py" "$p" "$af080_replay/score" --compare
python -B "$p/experiment/report_tables.py" "$p" --check
python -B "$p/experiment/check_result.py" "$p"

python -B "$p/experiment/verify_public_frame.py" "$p/frames.csv" natural \
  > "$af080_replay/natural-frame-readback.jsonl"
python -B "$p/experiment/verify_public_frame.py" "$p/frames.csv" calibration \
  > "$af080_replay/calibration-frame-readback.jsonl"

python -B "$p/experiment/run_fixtures.py" "$p" "$af080_replay/fixtures" "$af080_replay/runs.jsonl"
python -B -m workbench.session check "$p/manifest.json" --fetch
git diff --check d73c8ec85d375f37451795b575dd7d0e6b2f3594 HEAD
```

`score.py`는 채점 입력 7개에서 네 상태를 시험하고, 목록의 기능 ID 중복과 좁은 목록의 포함 관계를 확인한다. 48셀의 집계는 엄격과 최초 확보본의 두 경우를 갖는다. `report_tables.py`의 세 표는 각각 12·48·8행이다. 직접 열람 출처와 산입 키 중복도 검사한다. 표 1 원문 링크와 SHA가 요청을 복원할 열이며 원 글 전체 텍스트는 공개 저장소에 복제하지 않았다. [시작 범위](SCOPE.md) · [채점 시험](fixtures/scoring-cases.json)

`verify_public_frame.py`는 2022-01-01~2024-12-31의 `is:issue`, `sort:created-asc` 질의를 사용한다. 교정에만 `is:closed`를 더한다. 라이브 rerun에서 백필·삭제·상태 변경이 있으면 live 비교가 달라질 수 있다. 2026-11-23 조회 영수증은 [검색 원장](search-log.jsonl)에 있다. 원판 검증에서 목록과 이슈 번호가 같다는 사실은 본문이 최초 공개판이었다는 근거가 되지 않는다.

실행판·fixture·계측 코드는 [실행 계획](fixtures/execution-plan.json), [보정](evidence/fixture-correction.md), [실행 원장](runs.jsonl)에 있다. 반복의 경과 시간, 런타임 경로, UTC는 달라진다. 첫 실행 입력은 `877aa0c16691ae3827e4902cec72e8850dda6beb`, 보정 입력은 `a2582e9a6112a7ed8283c3ae1237580ec9eeb189`다. 정확 소비판 네 자리의 8계획은 종결 사건에서 정확 배포가 드러나면 다시 시험할 수 있다.

## 최초 게시판 재개

다음 읽기 전용 명령은 이미 허용된 GitHub GraphQL 연결과 API 호스트 접근이 되는 환경을 전제로 한다. 이번 클라우드에서는 GraphQL 요청이 Forbidden으로 종료 1이었다. 기존 계정 설정 변경 없이 먼저 알려진 수정 대조군을 조회한다.

```bash
p=docs/workstreams/research/AF-RES-080
af080_history="$(mktemp -d)"
GH_PROMPT_DISABLED=1 gh api graphql \
  -F owner=python-attrs -F repo=attrs -F number=1060 \
  -F query=@"$p/fixtures/original_body.graphql" > "$af080_history/known-edit-1060.json"
GH_PROMPT_DISABLED=1 gh api graphql \
  -F owner=pallets -F repo=click -F number=2172 \
  -F query=@"$p/fixtures/original_body.graphql" > "$af080_history/first-2172.json"
```

#1060의 공용 이력이 알려진 편집을 보여주는지 먼저 확인한다. GitHub의 `lastEditedAt`, `includesCreatedEdit`, `userContentEdits`는 SSR 표시와 맥락이 다르다. 기록한 두 모집틀에서 선발과 선행 순번을 같은 절차로 확인한다. 편집 데이터의 `diff`가 생성판을 복원할 만큼 충분한지, 사라진 이력이 있는지 대조한다. 지원 표지가 없는 본문은 최초판 불명으로 유지한다. 첫 판과 기존 해시가 다르면 각 역할을 다시 가리고 수정된 모집·판독을 새 단계로 커밋한다. [첫 판 조회 필드](https://docs.github.com/en/graphql/reference/issues#issue) · [실제 수정 대조군](https://github.com/python-attrs/attrs/issues/1060#issuecomment-1329862116)
