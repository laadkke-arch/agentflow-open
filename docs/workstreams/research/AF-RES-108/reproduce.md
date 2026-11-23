# AF-RES-108 재현

## 봉인 원장의 계산

작업 브랜치에서 검사 받은 결과 SHA를 detached checkout한다. 이 디렉터리의 `HANDOFF.md`에 검사 결과 SHA와 원격에서 확인한 시각이 있다. 결과에 쓰지 않는 검산은 체크아웃 루트에서 실행한다.

```sh
task_path=docs/workstreams/research/AF-RES-108
python -B -m unittest discover -s "$task_path" -p 'test_*.py' -v
python -B "$task_path/adjudicate.py" --check
python -B "$task_path/render_result.py" --check
python -B -m workbench.session check "$task_path/manifest.json" --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

`adjudicate.py`는 각 입력과 예측 봉인을 지문으로 비교한다. 값·typeof·허용된 순열과 픽셀 오차를 비교하고, 실제 인용이 각 구간 안에 있는지 확인한다. 스냅샷 캐시를 `--cache`로 넘기면 원 인용 내용의 SHA와 익명 화면 SHA도 비교한다. `render_result.py`는 8·32·19행의 세 필수 표를 같은 원장에서 만든다. 중앙 진행표에는 쓸 필요가 없다.

## 차단됐던 원문 확보

[문서 취득 기록](evidence/documents.json)의 각 URL을 번호 붙은 HTML 텍스트 보기로 열고 `line_views.calls`의 범위로 0부터 마지막까지 겹쳐 읽는다. 중복 라인은 일치해야 한다. 문서 값이나 기대를 예측자에게 일찍 표시하지 않는다. 각 줄에서 공통 `L번호:`와 바로 뒤의 표시용 공백 1개를 떼고 LF로 연결한 다음 끝에 LF를 하나 붙인다. 사용자에게 보이는 원문은 게시자 URL에서 읽을 수 있다. Git의 압축 맵에는 텍스트 대신 오프셋·줄·열과 변환 종류가 있다.

| 파일 이름 | 원문 |
| --- | --- |
| `lang_expr.view`, `lang_aggfunc.view`, `lang_select.view`, `windowfunctions.view` | SQLite 공식 게시자 페이지 4개. 이 캡처의 실제 날짜와 SHA는 [문서 원장](evidence/documents.json). |
| `flexbox.view` | [2025-10-14 W3C CRD](https://www.w3.org/TR/2025/CRD-css-flexbox-1-20251014/)의 3,663줄 텍스트 보기 |
| `posix_view.view` | [man7 POSIX.1-2017 재게시](https://man7.org/linux/man-pages/man3/fnmatch.3p.html)의 146줄 |
| `svg_view.view` | [SVG 2 2018 CR painting](https://www.w3.org/TR/2018/CR-SVG2-20181004/painting.html)의 1,194줄 |

SQLite 공식 [3.51.1 문서 ZIP](https://sqlite.org/2025/sqlite-doc-3510100.zip), [공식 docsrc](https://sqlite.org/docsrc), W3C의 raw 페이지를 새 환경에서 먼저 직접 열어 고정한다. 원문 취득은 이 실험에서 막혔다. 원시 HTML로 재실행할 때는 파일을 `docs/` 아래의 `lang_expr.html` 등 같은 stem의 `.html` 이름으로 둔다. selector가 HTMLBody-v1을 자동 사용한다. 과거 Docsrc와 공개 웹 보기 사이 SHA 또는 위치 변경은 새 비교로 기록한다. 기존 `predictions.jsonl`은 원격 봉인에서 가져온다.

같은 번호 뷰가 확보된 경우에 과거 패킷을 재생한다. 캐시 파일 이름이 같아도 `evidence/documents.json`의 SHA-256을 대사해야 한다. 현재 게시자 텍스트가 바뀌면 과거 화면 재생이 불가능할 수 있다.

```sh
task_path=docs/workstreams/research/AF-RES-108
task_cache=/tmp/af108
mkdir -p "$task_cache"/{docs,replay}
cp -a "$task_path/inputs" "$task_cache/replay/"
mkdir -p "$task_cache/replay/evidence"
python -B "$task_path/select_passages.py" "$task_cache/docs" --root "$task_cache/replay"
cmp "$task_path/packets.jsonl" "$task_cache/replay/packets.jsonl"
python -B "$task_path/adjudicate.py" --check --cache "$task_cache/docs"
python -B "$task_path/select_passages.py" "$task_cache/docs" --view 1 1
```

실제 소스 문자열의 UTF-8 SHA, 변환 버전, 커서 변수, 좌표 맵의 지문은 [문서 로그](evidence/documents.json)에 있다. `document-map.json.gz`의 스팬은 생성 스트림과 페이지 보기 사이의 사상이다. display가 가르는 위치와 소스 순서 배치는 selector 단위시험에 있다. 벽시계는 공통 변환·K/E 결합 선택의 실측이다. K는 전체 후보 점수, E는 추가로 표지어 문장 스캔과 후보별 포함 여부를 검사한다. [비용 원장](evidence/preprocess-cost.json) · [각 후보·예외 적격 수](packets.jsonl)

## 16입력 두 번씩 실행

실행을 다시 할 때는 결과 파일을 덮어쓸 수 있는 별도 disposable checkout을 쓴다. 논문 표의 영수증은 체크된 SHA에서 읽는다. 컴파일러·Tcl 8.6 계열·Python 3.12·Playwright·Pillow·Chromium이 이미 있는 환경을 썼다. 정확한 엔진·빌드 구성은 [엔진 원장](evidence/engines.json)을 확인한다.

```sh
task_cache=/tmp/af108
task_path=docs/workstreams/research/AF-RES-108
mkdir -p "$task_cache/upstream/sqlite"
curl -fLsS https://codeload.github.com/sqlite/sqlite/tar.gz/a1de06a4c639a5d741b2b424e5dfea45eaa30e70   -o "$task_cache/sqlite-3.51.1.tar.gz"
tar -xzf "$task_cache/sqlite-3.51.1.tar.gz" --strip-components=1 -C "$task_cache/upstream/sqlite"
(cd "$task_cache/upstream/sqlite" && ./configure --disable-shared && make -j4 sqlite3)
python -B "$task_path/run_inputs.py" "$task_cache" --chromium /usr/bin/chromium
python -B "$task_path/adjudicate.py" --check
```

코드는 WPT 고정 SHA의 필요한 HTML·referer와 하네스·Ahem을 받는다. 공식 SQLite의 로컬 빌드 소스 ID와 manifest를 검증하고 각 쿼리 뒤에 같은 입력의 `typeof()` 관측을 더한다. 각 실행은 `:memory:` DB 또는 800×600 CSS px, DPR 1의 새 Chromium context다. launcher 옵션, stdout·stderr와 종료값, 타입, 상대 rect, 원 assertion과 스크린샷이 남는다. SQL 전체 Tcl 스위트는 미실시다.

원 기대와 다른 값이 보이면 [입력 해시 및 한 값 변경](inputs/selection.json), [기대 근거](evidence/expected.json), 변이 여부, 엔진 조건을 함께 검증한다. `check-layout-th`의 offset과 CSSOM View rect의 기준은 따로 확인한다. 다른 엔진에서 얻은 값은 새 영수증으로 기록한다.

## 보조 교정

앞 표의 POSIX와 SVG 웹 보기 두 개가 `docs/`에 있어야 한다. 같은 fixture를 직접 열어 비교한다. `painting-fill-03-t-manual.svg`의 두 경로를 한 테스트 안의 변형으로 사용한다. POSIX 원본이 접근 가능하면 본문과 실제로 읽은 재게시 지문을 다시 대조한다.

```sh
task_cache=/tmp/af108
task_path=docs/workstreams/research/AF-RES-108
mkdir -p "$task_cache/upstream"
curl -fLsS https://raw.githubusercontent.com/coreutils/gnulib/adbe61f5ee7462a6e479f21d75ce51be919b7550/tests/test-fnmatch.c   -o "$task_cache/upstream/gnulib-fnmatch"
curl -fLsS https://raw.githubusercontent.com/web-platform-tests/wpt/f1edffe3511493e684402fdfed42433e79374d55/svg/import/painting-fill-03-t-manual.svg   -o "$task_cache/upstream/painting-fill-03-t-manual.svg"
python -B "$task_path/calibration.py" "$task_cache"
```

로컬 검산에는 글롭 플래그 결과 다섯 값, SVG 내부 판정 두 값, SQLite 동일 ORDER BY 입력의 인덱스 전후 출력이 있다. [실행·발췌 위치](evidence/calibration.json)
