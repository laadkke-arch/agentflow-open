# AF-RES-123 재생 및 검산

Bash, Git, Python 3.12, Node 24/npm 11, Chromium과 DejaVu Sans를 사용한다. 실측 브라우저는 Chromium 156.0.8078.79, 런타임 환경은 [본행 영수증](evidence/main/environment.json), [대조 영수증](evidence/controls/environment.json)에 있다. Playwright Core는 설치된 headless Chromium을 구동한다. chart의 브라우저 context는 offline이고 CSV는 요청한 원 상대 주소에 fixture bytes로 응답한다. 외부 서버, 선택 tuple 초기 주입, 사용자 데이터 업로드가 필요 없다.

## 깨끗한 경로에서 전체 실행

```sh
af123_tmp=$(mktemp -d /tmp/af123-replay.XXXXXX)
git clone --no-tags --single-branch --branch work/research-af-res-123 \
  https://github.com/laadkke-arch/agentflow-open.git "$af123_tmp/checkout"
cd "$af123_tmp/checkout"
git status --short --branch
git rev-parse HEAD
af123_scope=docs/workstreams/research/AF-RES-123
mkdir "$af123_tmp/npm"
cp "$af123_scope"/fixture/npm/package{,-lock}.json "$af123_tmp/npm/"
npm ci --prefix "$af123_tmp/npm" --cache "$af123_tmp/npm-cache" \
  --ignore-scripts --no-audit --no-fund
TZ=UTC node "$af123_scope/replay/drive.cjs" --mode matrix \
  --engine "$af123_tmp/npm" --out "$af123_tmp/main"
TZ=UTC node "$af123_scope/replay/drive.cjs" --mode controls \
  --engine "$af123_tmp/npm" --out "$af123_tmp/controls"
python -B "$af123_scope/replay/analyze.py" --main "$af123_tmp/main" \
  --controls "$af123_tmp/controls" --out "$af123_tmp/analysis"
python -B "$af123_scope/replay/audit.py" --replay "$af123_tmp" \
  --out "$af123_tmp/verification.json"
python -B -m workbench.session check "$af123_scope/manifest.json" --fetch
```

정확한 고정 결과의 Git checkout과 결과 영수증은 `HANDOFF.md`의 결과 SHA에서 찾는다. 다른 SHA를 명시적으로 재생하려면 위 clone의 branch head와 고정 SHA를 확인한 뒤 `git checkout --detach SHA`로 이동한다. 표준 경로에 없는 Chromium이나 글꼴은 driver `--chromium /실제/경로`와 `--font /실제/DejaVuSans.ttf`를 지정한다. driver는 압축 배포 번들·lock·CSV·spec·글꼴 지문과 배율·origin을 실행 때 검사한다. preview 화면이나 다른 OS의 결과를 비교하려면 동일한 SHA와 좌표 보정값, 새 환경 로그를 같이 남긴다. [입력 지문](fixture/fingerprints.json) · [봉인 계획](plan.json)

`--mode pilot`은 새 output dir에 좌표 후보를 계산하고 initial drag와 hover까지 확인한다. `matrix`와 `controls`는 저장된 봉인 계획을 사용한다. 초기 조건을 만들기 위한 drag는 `initialize` phase이고 본 동작은 `test` phase다. 원파일의 `trajectory`는 명령, `events`는 두 관측 채널의 수신값, `snapshots.first`는 행동마다 첫 rAF에서 읽은 값이다. `nextChanges`는 직후 rAF에서 달라진 값이다. event 원장에서 `state_after_step`은 그 이벤트가 속하는 driver step 후의 rAF 값이다. 같은 event가 여러 handler에 들어가면 `nativeId`로 연결한다. times는 `chart.timeOrigin`과 상대 값이며 다른 브라우저 호출 사이에는 비교하지 않는다. [본 이벤트 예](evidence/main/M-original-svg-empty-mark-1.json) · [관측자 해제 입력](evidence/controls/C09-observers-off-canvas-1.json)

## 실패 후 재개

- 설치가 실패하면 `npm ci`의 stderr와 Node/npm 판을 먼저 본다. registry 가능 환경에서 같은 lock과 새 설치 prefix로 다시 실행한다. 브라우저가 시작하지 않으면 `chromium --version`과 글꼴 SHA를 확인하고 브라우저·글꼴 옵션을 지정한다.
- driver는 충돌을 피하도록 새 output dir만 만든다. 실패한 output의 `environment.json`과 원행 `error`/stderr를 보존한 뒤 같은 mode와 별도 새 디렉터리로 재실행한다. app 결과가 나오지 않았거나 seed가 틀리면 다른 모드로 바꾸기 전에 renderer, CSS 원점, seed 입력과 hit를 먼저 대조한다.
- GIF를 읽을 수 있는 환경에서는 공개 첨부의 bytes를 받아 SHA-256과 실제 프레임 자료를 기록한다. 시점·저자 포인터·빌드를 영상에서 실제 판독할 수 있는 범위까지 업데이트한다. [GitHub 첨부](https://github.com/user-attachments/assets/f9e3cffb-5998-4607-b71e-7e090fa71521) · [접근 시도](evidence/issue-8628.json)
