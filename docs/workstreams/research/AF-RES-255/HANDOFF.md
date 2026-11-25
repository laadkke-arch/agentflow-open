# AF-RES-255 인수인계

**상태 `REVIEW_READY`.** 두 고정 엔진의 원형 reftest 8/8, 별도 단어 기하 8/8, 반전 대조의 새 프로필 재현과 직접 원자료 하한을 충족했다. 이중 검산은 동일 작업자의 자체 점검이다. 별도 독립 검토는 미실시다.

- 작업 `AF-RES-255` 1회차 · Codex Cloud · `laadkke-arch/agentflow-open`의 `work/research-af-res-255`.
- 소유 경로 `docs/workstreams/research/AF-RES-255/`. 통합 착수 `d1353701530ffd4c68587276c15d988d2cc92972`, 계획 `7369707441e2eb70e84004ca6cb3bfeefc8b4061`. 선행 AF-RES-232 `430a1a5ec049f58878d963cb8ca539c9375f93d0`은 중앙 DONE, 자체 PARTIAL이다.
- 인계 직전 검증 결과 SHA **`d90b7b745046af026fa9d53866fef01fecd327f2`**. 착수와 결과 사이 변경은 소유 경로에 한정된다. 마지막 실제 재생·확인 시간창은 2026-11-25 00:40–00:42 UTC다. [고정 결과 트리](https://github.com/laadkke-arch/agentflow-open/tree/d90b7b745046af026fa9d53866fef01fecd327f2/docs/workstreams/research/AF-RES-255).

## 판단과 저장 지점

WPT `5ad65d6ea6c649696be2d0cf5188dfdb43f8d801`에서 Chromium 156.0.8078.79와 WebKitGTK 2.54.3의 원형 002·003 모두 PASS였다. 002는 원 참조와 4,800픽셀 차이, 실제 cut 3이며 cut 2의 사본도 mismatch를 충족했다. 003은 0픽셀 차이, plain·inline 모두 cut 4였다. Chromium 003은 Ahem이 HTTP 404여도 별도 대조에서 같은 관계와 cut이 발생했다. 원형과 기하용 Chromium 003 캡처 사이에 설명 문단의 3,086픽셀 차이도 확인해 분리 기록했다. [결과](RESULT.md), [실행 목록](runs.csv), [단어 좌표](words.csv), [교차 경로 픽셀](receipts/cross-layer.json).

WebKitGTK W7은 140 CSS px에서 `[120,120,40]`, 140.015625 CSS px에서 `[80,60,140]`을 그렸다. auto와 세 줄은 같은 상태였다. 이 전환은 max-line 최소 해석의 일반화를 뒤집었으며, 고정 구현의 후보폭 `epsilon` 경계와 일치한다. 분기 추적은 미실시다. C1 강제 개행의 3줄은 두 엔진에서 다르게 놓였다. 게시 Sintel cue 3·4의 표시 줄은 2→4, 1→3으로 바뀌었고 원텍스트 행과 cue 사이 0.300초는 보존됐다. [반례](COUNTEREXAMPLES.md), [실험 원영수증](receipts/diagnostics/).

직접 원저작 27개(9/9/5/4), 원천 계보 12개, 목록 43행이다. 각 원형 `command.json`, `wptreport.json`, `raw.jsonl.gz`, stdout/stderr, 두 PNG와 diff는 `receipts/primary/{run_id}`에 있다. 별도 기하 JSON은 `receipts/geometry/`에 있다. [표집·입력판](manifest.json), [환경·지문](env.json), [근거 원장](sources.jsonl), [자체 점검](SELF_CHECK.md), [재생](replay.md).

커밋은 ① `9ecbf783` 표집·예상 봉인, ② `dddf3f2a` 원문·원장, ③ `9992dc12` 주관측·두 표, ④ `87e3321a` 반례 및 재생, ⑤ `02823809` 결과·자체 점검과 `d90b7b74` 캡처 경로 정정 순이다. 232에서 알려진 기대와 003의 입력 내 참조는 가림 성적에서 제외했다. ⑥은 이 파일만 저장한다.

## 결과 SHA에서 시행한 검사

| 실제 검사 | 종료 및 실제 범위 |
|---|---|
| `python -m workbench.session start af-res-255 --allow docs/workstreams/research/AF-RES-255/ --dependency work/research-af-res-232=430a1a5ec049f58878d963cb8ca539c9375f93d0 --output docs/workstreams/research/AF-RES-255/session.json --fetch` | 착수판에서 exit 0. 허용 경로, 기준 SHA, 공통 계약 2와 의존 SHA 고정. [session.json](session.json) |
| `python -m workbench.session check docs/workstreams/research/AF-RES-255/session.json --fetch` | `d90b7b74…`에서 2026-11-25T00:40:42Z, exit 0, `passed`, `remote_checked`. 원격 통합 `b28a67f6d02ab7ce4d050acabbd1b30c64eba97c`, 변경 358경로, 범위 위반·오류 0, stderr 0 bytes. |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 같은 SHA의 깨끗한 checkout에서 exit 0. doctor, acceptance(공통 55·lab 7·9개와 export/백업 검산), research-case, original-smoke가 통과했다. 기본 위치의 check-all은 `no_active_sessions`였다. 소유 경로의 핀은 바로 위 개별 검사에서 확인했다. stderr 0 bytes. |
| 결과 파일과 영수증 재열기 | 고정 SHA에서 핵심 18파일과 추적 영수증 341파일을 읽었다. 8 raw `test_end`·report·Base64 PNG·픽셀을 검산하고 264 Range 원행을 대조했다. 합성/명시적 대조 문서 32, 폰트 404 4쌍, 두 native VTT, 8 cue 폭, 27 원저작, Q1–Q7 및 세 표 8×6·13×5·3×4의 열과 링크를 확인했다. CSV 재생성 diff 0, `node --check measure.js`, shell·Python 구문 확인 및 소유 경로 검산 exit 0. |

## 고정 결과판의 새 프로필 재생

`d90b7b74…`의 별도 `/tmp/af255-pinned-d90` checkout에서 동일 WPT SHA와 `env.json`의 MiniBrowser·WebKitWebDriver를 사용했다. `replay.md`의 환경을 적용하고 `reftest.py --engine webkitgtk --test 003 --repeat 3`을 새 runner·프로필에서 실행했다. 이어 `geometry.py --engine webkitgtk --mode original --test 003 --repeat 3`과 별도 `--mode controls`를 실행했다. 세 프로세스와 비교 검사 모두 exit 0이다. `reftest.py` stdout은 `webkitgtk-003-r3 PASS 0 0`이다. runner stderr는 비대상 Firefox용 `mozrunner`와 `mozleak` 누락 경고 두 줄이었다. 기하 및 통제 stderr는 각각 0 bytes였다.

원형 WebKitGTK 003 재생과 r1의 입력·참조 PNG SHA-256은 모두 `d4678952df863de97a6f37088d30a36c306855d33718ce333fc20417e87c20db`였다. 반복 3의 두 개별 기하 `blocks`와 두 TTF 응답 지문도 r1과 일치했다. WebKitGTK W7 auto 대비 balance 차이는 140 CSS px의 0에서 140.015625 CSS px의 3,200으로 재현됐다. C1 forced auto/balance 차이는 1,600픽셀로 재현됐다. [동일 PNG 원본](receipts/primary/webkitgtk-003-r1/input.png), [r1 기하](receipts/geometry/webkitgtk-003-r1/geometry.json), [기준 W7·C1 원행](receipts/diagnostics/webkitgtk-controls/controls.json).

고정 결과판 재생의 원출력 지문은 report `932a801832f259b803347a533f745729b0192a9a957ec05c5494def026e4294b`, raw (압축 전) `3bf3abadb8cc4497a6a8449b3f4ee3c64799be8906b8498c3214d004f54741a6`, 기하 `ee1bccd46fc8164a05387ed38a661925b35775ec7f8720139bce852467357a8c`, 통제 `9c0f4a36558faced3f46b1bed1f80456c1cd439b7b9ac06081cb5ee416ed28d8`이다. 재생 shim은 `16a3a5d9a98fbc5166f5958a391c84a94aa3f21f5a018947650c173cf0793d88`로 `env.json`과 일치했다. 별도로 ③에서 수행한 Chromium 003 및 C1의 원보고서·화면·좌표는 [저장된 재생 묶음](receipts/replay/)에서 읽을 수 있다.

<details>
<summary>고정 결과판 WebKitGTK 003 재생의 wptreport.json</summary>

```json
{"run_info": {"os": "linux", "processor": "x86_64", "version": "Debian Gnu/Linux 13", "os_version": "13", "bits": 64, "has_sandbox": true, "display": "x11", "automation": false, "linux_distro": "Debian Gnu/Linux", "apple_silicon": false, "apple_catalina": false, "win10_2004": false, "win10_2009": false, "win11_2009": false, "revision": "5ad65d6ea6c649696be2d0cf5188dfdb43f8d801", "python_version": 3, "product": "webkitgtk_minibrowser", "debug": false, "browser_version": "2.54.3", "verify": false, "wasm": false, "webkit_port": "gtk", "headless": false}, "time_start": 1795567243841, "results": [{"test": "/css/css-text/white-space/text-wrap-balance-003.html", "subsuite": "", "subtests": [], "status": "PASS", "message": null, "duration": 201, "known_intermittent": [], "screenshots": {"/css/css-text/white-space/text-wrap-balance-003.html": "sha1:5f1a8f7908c5850ba670987ccbef128007560a7d", "/css/css-text/white-space/reference/text-wrap-balance-003-ref.html": "sha1:5f1a8f7908c5850ba670987ccbef128007560a7d"}}], "subsuites": {"": {"subsuite": ""}}, "time_end": 1795567263853}
```

</details>

## 미확인과 재개 첫 행동

공개 exact-SHA run의 원응답은 API와 raw archive 모두 연결 제한으로 확보하지 못했다. 제출 존재·버전·run id는 미확인이다. WebKitGTK의 별도 DOM `loadingdone` 콜백은 미수신이었으며, 실제 200 응답·폰트 bytes·ResourceTiming·`FontFace.loaded`·폭은 각 로드에서 확인했다. Firefox/Safari 타 포트, 런타임 내부 분기, 실사용 제목에 대한 일반화, 사람의 가독성은 이번 관측 범위 밖이다. [공개 조회 영수증](receipts/public-wpt-probe.txt), [웹킷 이벤트 영수증](receipts/diagnostics/webkitgtk-font-audit/font-audit.json).

재개할 때 먼저 원격 브랜치의 이 인계와 결과 SHA를 대조한다. 공개 run을 보완할 수 있는 환경이면 다음 요청을 하고 full revision과 두 시험의 결과 행을 확인한다. `browser_name`, version, OS와 run ID를 로컬 관측 표에서 구별한다.

```bash
curl -fSL 'https://wpt.fyi/api/runs?sha=5ad65d6ea6' -o af255-public-runs.json
jq '.[] | select(.revision == "5ad65d6ea6c649696be2d0cf5188dfdb43f8d801") | {id,revision,browser_name,browser_version,os_name,raw_results_url}' af255-public-runs.json
```

색인 제안은 `AF-RES-255 — 두 WPT의 픽셀 관계와 실제 단어 줄, WebKitGTK W7 정확폭 경계`를 고정 결과 SHA·Ahem 핀·AF-RES-232 의존성과 연결하는 것이다. 상태는 자체 실행 검증 완료·독립 검토 미실시로 표현하고, 002의 mismatch와 003의 font-failure 대조를 함께 링크한다.
