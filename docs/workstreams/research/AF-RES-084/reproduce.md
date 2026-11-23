# AF-RES-084 재현

명령은 저장소의 `work/research-af-res-084`에서 실행한다. Linux x86_64, CPython 3.12.14, Git, curl, uv 0.13.6을 사용했다. 공개 저장소에는 원문 전문과 압축 원시 자료를 두지 않는다.

## 16셀과 근거 재생

```bash
p=docs/workstreams/research/AF-RES-084
git fetch origin refs/heads/work/research-af-res-080
git cat-file -e 152f5261ab9a35ab675ab003931ac4dc89966b55^{commit}
python -B "$p/verify_events.py" --self-test
python -B "$p/recalculate.py" --check
python -B "$p/verify_result.py"
python -B -m workbench.session check "$p/manifest.json" --fetch
```

`recalculate.py`는 지정된 080 커밋에서 봉인 해시, 모집, 요구, 목록, 정답 및 이전 16판정의 입력을 받는다. 최신·확보 SHA와 개설 여부를 대조한다. 후보를 카탈로그 ID·별칭·절에 연결해 `cells.csv`, 세 종류의 쌍인 `pairs.csv`, `metrics.json`을 재생한다. `--out`으로 임시 경로에 쓸 수 있다. 카탈로그를 다시 생성하지 않으며 080의 다른 32셀을 채점하지 않는다. 파일·절 지문을 공급 원문의 바이트에서도 대조하려면 다음 명령을 추가한다.

```bash
p=docs/workstreams/research/AF-RES-084
replay_084="$(mktemp -d)"
git init -q "$replay_084/click-git"
git -C "$replay_084/click-git" fetch --no-tags --depth=1 https://github.com/pallets/click.git \
  refs/tags/8.0.3:refs/tags/8.0.3 refs/tags/8.5.1:refs/tags/8.5.1
git init -q "$replay_084/attrs-git"
git -C "$replay_084/attrs-git" fetch --no-tags --depth=1 https://github.com/python-attrs/attrs.git \
  refs/tags/26.1.0:refs/tags/26.1.0
python -B "$p/recalculate.py" --check --upstream "$replay_084"
```

## 이번에 실행한 입력

새 실행 10개를 [사전 계획](fixtures/plan.json)에서 읽고, [고정 wheel URL·SHA-256](fixtures/wheels.json)을 검증해 격리된 venv에서 실행한다. 080 참조 네 행은 영수증 데이터만 읽는다. 기존 프로세스를 실행하지 않는다. 네 건의 저자 보고와 교정의 후속 진술 두 건, 미실행 정확판 여섯 행이 함께 기록된다.

```bash
p=docs/workstreams/research/AF-RES-084
replay_084="$(mktemp -d)"
UV_CACHE_DIR="$replay_084/cache" UV_PYTHON_INSTALL_DIR="$replay_084/python" \
  uv python install --no-bin 3.8.12 3.10.3
python -B "$p/run_probes.py" \
  --python "3.8.12=$replay_084/python/cpython-3.8.12-linux-x86_64-gnu/bin/python3.8" \
  --python "3.10.3=$replay_084/python/cpython-3.10.3-linux-x86_64-gnu/bin/python3.10" \
  --work "$replay_084/envs" --out "$replay_084/runs.jsonl"
```

같은 버전과 조건의 `observed`, 내부 CLI 종료, `process_exit`를 비교한다. UTC와 임시 경로는 달라진다. 휴대용 빌드와 인터프리터 SHA는 실행마다 확인한다. CN01의 사전 실행에서 Click 8.0.3 CliRunner는 표준입력 EOF가 전달되지 않아 시간 초과였다. 실제 파이프로 옮긴 뒤 동일 입력과 기대를 다시 사용했다. [계측 보정](evidence/fixture-correction.md)

## 아직 수행하지 못한 원본 확인

공개 GH Archive 시간 파일을 읽을 수 있는 작업공간에서 EDIT1060으로 먼저 검사를 시작한다. 아래 전체 시간 파일은 임시 작업공간에 두고 검증된 한 본문만 가린 판독에 사용한다.

```bash
p=docs/workstreams/research/AF-RES-084
archive_084="$(mktemp -d)"
for h in 0 1; do
  curl -fSL --max-time 180 "https://data.gharchive.org/2022-11-28-$h.json.gz" \
    -o "$archive_084/2022-11-28-$h.json.gz"
done
python -B "$p/verify_events.py" --case EDIT1060 \
  --body-output "$archive_084/EDIT1060-opened.md" "$archive_084/"*.json.gz
```

검증기가 이슈 1465633178, 저장소 29918975, 시각 2022-11-28 00:29:53Z, 작성자 mrolle45에 해당하는 유일한 `IssuesEvent / opened`를 찾으면 raw와 LF 해시를 낸다. 원본의 `evolve` 구간 유무를 읽는다. 네 본 사례의 시간 파일은 [이벤트 원장](events.jsonl)의 `archive_urls`에 있다. 시간이 확인돼도 이벤트 본문이 없거나 서로 다른 원본 행이 경합하면 미확인 상태로 둔다.

생성 리비전을 제공하는 인증 읽기 환경에서는 아래 대안을 쓴다. 이 Cloud의 POST는 네 사례와 #1060 모두 403이었다. 테스트 쿼리에는 공개된 읽기 필드만 들어 있다.

```bash
GH_PROMPT_DISABLED=1 gh api graphql \
  -F owner=python-attrs -F repo=attrs -F number=1060 \
  -F query=@"$p/fixtures/original_body.graphql" > "$archive_084/1060.history.json"
```

저장소와 이슈 ID, 번호, 작성자, `includesCreatedEdit`, 완전한 페이지, 삭제 여부와 최초 리비전 내용을 확인한다. 제한된 시간이나 삭제된 편집은 기록한다. 첫 리비전 시각이 겹친 공개 예처럼 정렬만으로 생성 리비전을 대입할 수 없다. 재판독 때는 확보본/개설 본문 투영만 사용하고 해당 단계 SHA를 먼저 봉인한다. 새로운 최초판을 확인해도 080의 전체 선발을 바꾸려면 먼저 해당 층의 선행 순위도 복원해야 한다. [공개 예](https://github.com/orgs/community/discussions/33551)

## 정확 소비판 재개

각 셀의 결손은 [cells.csv](cells.csv)의 `minimal_missing`에 있다. AN01은 원 질문의 정확 Python·attrs, CC01과 AC01은 성공 출력이나 키 조회 결과와 같은 실행의 버전이 필요하다. 그 실행판의 공식 wheel 해시와 상류 태그를 고정한다. 080의 목록 생성기에 확인한 버전 하나를 넣고 두 범위를 추출한다. 입력은 `package`, `version`, `tag`, `commit`만 담는다. [080 생성기](https://github.com/laadkke-arch/agentflow-open/blob/152f5261ab9a35ab675ab003931ac4dc89966b55/docs/workstreams/research/AF-RES-080/experiment/build_catalogs.py) · [버전 입력 형식](https://github.com/laadkke-arch/agentflow-open/blob/152f5261ab9a35ab675ab003931ac4dc89966b55/docs/workstreams/research/AF-RES-080/evidence/catalog-versions.json)

```bash
dep_084=152f5261ab9a35ab675ab003931ac4dc89966b55
root_080=docs/workstreams/research/AF-RES-080
git show "$dep_084:$root_080/experiment/build_catalogs.py" > "$replay_084/build_catalogs.py"
python -B "$replay_084/build_catalogs.py" --versions "$replay_084/confirmed-version.json" \
  --workspace "$replay_084/confirmed-upstream" --output "$replay_084/catalogs-exact.jsonl"
for mode in positive boundary; do
  "$replay_084/confirmed-env/bin/python" -I "$p/fixtures/probe.py" "$case_084" "$mode"
done
```

`case_084`에는 AN01, CC01, AC01 중 확인된 ID를 넣는다. CC01은 위치 인수 등록과 실제 -V 출력, AC01은 두 키 각각의 최종 클래스 동일성을 읽는다. AC01 전용 훅을 지원하는 배포라면 080의 고정 프로브에서 AC01 양성·경계를 별도 대안으로 실행한다. 원 작성자의 실제 출력과 이번 동일판 실행을 각각 기록한다. [080 고정 프로브](https://github.com/laadkke-arch/agentflow-open/blob/152f5261ab9a35ab675ab003931ac4dc89966b55/docs/workstreams/research/AF-RES-080/fixtures/probe.py)
