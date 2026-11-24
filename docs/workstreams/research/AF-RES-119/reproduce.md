# AF-RES-119 재현

저장소 루트에서 실행한다. [모집 봉인](SCOPE.md), [전체 사양 기준](REFERENCE.md), [입력 변경의 사전 고정값](fixtures/operations.json)을 같이 읽는다. 파일 끝의 CRLF를 유지한다. `fixtures/original`의 지문은 `cases.jsonl`의 UTF-8 반열림 구간과 맞아야 한다.

## 모집과 보기 재생

공개 REST 목록의 실제 URL·페이지 범위·수집시각은 [페이지 영수증](evidence/frame-pages.jsonl), 40/41과 탈락 원장은 [frame.csv](frame.csv)에 있다. GitHub 커넥터에서 `state=all&sort=created&direction=asc&per_page=100&page=…`을 열고 `pull_request`와 `body`를 분리했다. 이 환경에서 셸의 `api.github.com` 요청은 터널 403이었다. 깨끗한 환경의 실시간 비교라면 등록한 URL 및 `cases.jsonl`의 이슈별 API를 연다. 변경된 현재 본문과 오래된 opening 최초 revision은 각기 다르게 기록한다.

이미 저장된 40/41 경계를 같은 코드로 복원하는 명령이다.

```sh
af119_repo="$PWD/docs/workstreams/research/AF-RES-119"
af119_tmp=$(mktemp -d /tmp/af119-replay.XXXXXX)
mkdir -p "$af119_tmp/pages"
python -B - "$af119_repo" "$af119_tmp/pages" <<'PY'
import json
from pathlib import Path
import sys
root, scratch = map(Path, sys.argv[1:])
rows = (root / 'evidence/opening-frame.jsonl').read_text().splitlines()
for project in ('V','M'):
    selected = [row for row in rows if json.loads(row)['project'] == project]
    (scratch / f'{project}-frozen.jsonl').write_text('\n'.join(selected) + '\n')
PY
python -B "$af119_repo/collect.py" "$af119_tmp/pages"
python -B "$af119_repo/replay_views.py" "$af119_tmp/views"
```

`collect.py --write`와 `materialize.py`는 같은 저장 위치의 원장·보기·fixture를 다시 쓴다. 후보 메뉴와 요청, 완결 레코드만 subprocess에 넘긴다. 동일 코드 작성자가 전체 사양을 먼저 보았으므로 이 재생의 출력은 기술 진단이다. 판독자 독립성은 미실시다.

## CLI와 데이터 고정

- Vega-Lite/Vega 짝은 5.5.0/5.22.1, 4.17.0/5.17.0, 5.6.0/5.22.1이다. Node v24.22.1 및 npm 11.9.0에서 `vl2svg`와 `vl2vg`를 실행했다. Vega-Embed 6.21.0은 V8625 작성자 환경의 서술에 있다.
- Mermaid 9.3.0 npm 압축 해제의 `dist/mermaid.min.js`와 Puppeteer 19.11.1, Chromium 156.0.8078.79를 사용했다. 공식 mmdc 9.3.0의 초기 요청은 브라우저가 `file://…/dist/index.html`을 차단했다. 이 단계의 36개 영수증은 [mmdc 초기 실패](evidence/initial-mmdc-failures.jsonl)에 있다. 대체 실행은 Node에서 공개 배포본을 읽고 빈 Chromium 문서의 메모리로 주입한다. 도표 실행 중 네트워크 요청을 모두 차단한다. 정상 파일 탐색을 허용하는 검증자 환경에서는 `--mermaid-backend mmdc`로 공식 CLI를 따로 재연할 수 있다.
- 폰트는 DejaVu Sans, timezone UTC, locale C.UTF-8이다. 프로그램과 환경의 실제 버전·배포본 해시·폰트 해시는 [render-matrix.json](evidence/render-matrix.json)에 있다. V8628는 [고정 vega-datasets 2.5.3](https://github.com/vega/vega-datasets/blob/664835b3090a9069d4626ccae36fad75230c8f36/data/seattle-weather.csv)의 복사본이다. 저자 편집기에서 읽던 데이터 판은 미확인이다.

```sh
af119_repo="$PWD/docs/workstreams/research/AF-RES-119"
af119_tmp=$(mktemp -d /tmp/af119-replay.XXXXXX)
export npm_config_cache="$af119_tmp/npm-cache"
for af119_ver in v55 v417 v56 m93; do
    mkdir -p "$af119_tmp/npm/$af119_ver"
    cp "$af119_repo/fixtures/npm/$af119_ver/"package*.json "$af119_tmp/npm/$af119_ver/"
    npm ci --prefix "$af119_tmp/npm/$af119_ver" --ignore-scripts --no-audit --no-fund
done
python -B "$af119_repo/replay.py" --engines "$af119_tmp/npm" \
    --chromium /usr/bin/chromium --out "$af119_tmp/render"
```

기본 명령은 두 신선한 경로에 같은 입력 33개를 복사해서 각각 실행하고, `runs.jsonl`과 `matrix.json`을 scratch에 쓴다. 각 명령·원 stdout/stderr·종료값은 [runs.jsonl](runs.jsonl), 파일은 [render/r1](evidence/render/r1)과 [render/r2](evidence/render/r2)에서 재열람한다. V8628의 추가 dataflow 주입은 좌표 이벤트가 없는 보조 비교다. 원형/두 수정안의 컴파일 후 January x tuple을 `drag_brush_store`에 넣어 `active.svg`를 만든다. 위치·박스·토폴로지 비교에서 `output.svg`의 원값을 보존하고 root ID 및 대응 URL/CSS 접두어만 정규화한다. HTML label의 `<br>`가 XML parser에서 실패하는 M3994는 원 SVG 문자열과 Chromium DOM의 `XMLSerializer` 두 파일을 모두 둔다. 순서·기하·표지 텍스트는 비교에서 유지한다.

## 미확인 단계와 재개

- V8625 원 531바이트와 두 수정안은 strict JSON에서 멈춘다. v5.5.0의 `vl2svg`는 오류를 stderr에 쓰고 상태 0이므로 SVG 파일 존재 여부와 함께 판단한다. 쉼표 제거 진단본 V8625P는 `customFormatter` 미등록에서 멈춘다. 원 [CodePen](https://codepen.io/danielmalaton/pen/rNrLzaj) 프로젝트, 공식 JS 및 embed 경로는 확인 환경에서 열리지 않았다. 다음 입력은 원 저자의 함수 코드와 `vega.expressionFunction` 등록 호출이다. 원본을 덮어쓰지 말고 동일 설정의 Vega/Vega-Lite/Embed에서 각각 원 날짜와 epoch를 넣는다.
- V8627 및 V8628과 Mermaid의 정확 원 host는 [cases.jsonl](cases.jsonl)의 판 정보, 당시 렌더러 옵션 및 브라우저 판이 필요하다. 특히 V8628은 원 pointer의 hit target, x/y, drag start/end, viewport 및 원 dataset revision을 받아야 점프를 재생한다. 그 전에는 5.6.0의 SVG와 컴파일 signal 및 주입 상태만 판독한다.
- M3981의 원본과 root 방향 수정은 대체판에서 `undefined.id` 단계에서 멈춘다. 이 결과에는 원본 화면의 기하 보존 판정이 없다. 당시 live/VS Code 엔진과 브라우저가 제공되면 위 명령의 `--id M3981`을 실행하고 edge endpoint가 유지되는 backend를 먼저 확인한다.
- 액세스 시도·대체 공식 경로·원본이 남은 이유는 [sources.jsonl](sources.jsonl), 최초 게시본 확인의 최대 범위는 [opening-history.json](evidence/opening-history.json)에 있다.

## 고정판 검산

```sh
python -B docs/workstreams/research/AF-RES-119/verify.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-119/manifest.json --fetch
python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
python scripts/check.py --require-git
```
