# AF-RES-108 인계

**PARTIAL**. 검사한 결과는 [806cdff845acfb965a1b2f2a641010c2e9604498](https://github.com/laadkke-arch/agentflow-open/commit/806cdff845acfb965a1b2f2a641010c2e9604498)다. [결과와 세 필수 표](https://github.com/laadkke-arch/agentflow-open/blob/806cdff845acfb965a1b2f2a641010c2e9604498/docs/workstreams/research/AF-RES-108/RESULT.md) · [자가검산](SELF_CHECK.md) · [재현](reproduce.md)

## 인수할 관측

- 8쌍, 16입력, 사전 답 32자리와 새 DB 또는 새 렌더의 실행 32회가 연결된다. SQLite 3.51.1과 Chromium 156.0.8078.79를 사용했다. 원본 WPT는 픽셀 비교 2개와 하네스 30개를 통과했다. 8개 합성 입력은 한 값 편집이며 원 테스트와 연결된 기대값을 따로 기록했다. [원 기대](evidence/upstream-oracles.json) · [실행](runs.jsonl) · [엔진](evidence/engines.json)
- K/E 각각 1,200자×16, 경계 32, 추가 이동 0. UTF-8은 K 19,376B, E 19,342B다. 확인 답 각 8/16, 확정 중 오답 각 0/8, 유보 각 8. E는 F2 정상에서 정답 1개를 얻고 F4 정상에서 정답 1개를 유보로 바꿨다. S3의 두 값은 맞았고 E에서 정렬 근거를 잃었다. 주 표본의 오답 방지 전환은 0이다. [대응](pairs.csv) · [집계와 비용](metrics.json)
- S3 동점의 두 가능한 순서는 covering index 진단에서 모두 나왔다. 보조 POSIX는 E가 선두 점과 슬래시 조건을 보존했고, glibc는 flags 차이에서 0/1을 반환했다. 두 SVG 구간은 편집 방식과 무관하게 parity와 초기값을 놓쳤으며 별 중앙점은 evenodd=false, nonzero=true였다. [교정](evidence/calibration.md) · [교정 실행](evidence/calibration.json)

## 계약과 원격 봉인

계획판은 `49f603a98188fbf2009c4c490b0539f32d124e38`다. 시작 원격 `e601fa1aed009106be983ae9b24e4778e793276f`와 실제 계약 기동판 `32b6bb32989730df78d521c29a50dbebd3289b46`까지 바뀐 관련 파일은 중앙 진행표 하나다. 선행 운영 의존은 `ce8283488ab46a76f2d5fa081db5c4734f302526`이며 지정 연구 입력 `f38c0af427c66876bf411bfd0a728cfcd60013eb` 이후 HANDOFF 추가만 있다. 사용한 5개 blob은 일치했다. [계약](manifest.json) · [입력 대사](evidence/repository-input.json)

| 묶음 | 원격 SHA | 원격 확인 UTC | 변경 경로 |
| --- | --- | --- | --- |
| 사전 모집 규칙 | [7a66bf91e1d505420a2e97c5b1917588148db359](https://github.com/laadkke-arch/agentflow-open/commit/7a66bf91e1d505420a2e97c5b1917588148db359) | 2026-11-23T23:23:06Z | `SCOPE.md`, `protocol.json`, `manifest.json` |
| ① 입력·기대 분리 | [6bda721f25b2d1a812d9673ba03ece12194efac1](https://github.com/laadkke-arch/agentflow-open/commit/6bda721f25b2d1a812d9673ba03ece12194efac1) | 2026-11-23T23:29:22Z | `frame.csv`, `inputs/`, `stage_inputs.py`, `evidence/input-seal.json` |
| ② 절·32 사전 답 | [58a05b8275a34189c4750a2341443a7dbdcaf3d2](https://github.com/laadkke-arch/agentflow-open/commit/58a05b8275a34189c4750a2341443a7dbdcaf3d2) | 2026-11-23T23:36:58Z | `packets.jsonl`, `predictions.jsonl`, `select_passages.py`, 단위시험과 `evidence/{documents,prediction-seal,preprocess-cost}.json`, `SCOPE.md` |
| ③ 기대·실행·반례 | [a8dae9274b0279c28198ad2520571dda3e6d329b](https://github.com/laadkke-arch/agentflow-open/commit/a8dae9274b0279c28198ad2520571dda3e6d329b) | 2026-11-23T23:50:17Z | `runs.jsonl`, `sources.jsonl`, `frame.csv`, `run_inputs.py`, `calibration.py`, `evidence/`의 기대·좌표 맵·노출·실행·교정 및 10 PNG |
| ④ 대응·결과·자가검산 | [806cdff845acfb965a1b2f2a641010c2e9604498](https://github.com/laadkke-arch/agentflow-open/commit/806cdff845acfb965a1b2f2a641010c2e9604498) | 2026-11-23T23:56:32Z | `RESULT.md`, `SELF_CHECK.md`, `INDEX_PROPOSAL.md`, `pairs.csv`, `metrics.json`, `adjudicate.py`, `render_result.py`, `reproduce.md` |

시험 기대·실행·방법 매핑은 ②의 원격 확인 뒤 열었다. 선정에서 먼저 보인 내용과 같은 작업자의 이전 입력/같은 토막 노출을 남겼다. 독립 판독 0회다. [봉인](evidence/prediction-seal.json) · [공유 노출](evidence/exposure.json)

## 결과 SHA 검사와 GitHub 재열람

GitHub에서 받은 별도의 깨끗한 detached checkout에서 시행했다. 검사 전후 SHA는 `806cdff845acfb965a1b2f2a641010c2e9604498`이며 git 변경은 0이었다. 아래 UTC는 2026-11-23이다.

| 실제 명령 | UTC 시작 → 종료 | 종료 | 확인 범위 |
| --- | --- | --- | --- |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-108/manifest.json --fetch` | 23:57:26.900239 → 23:57:28.970498 | 0 | 명시 세션 1개, 원격 계약·의존, 소유 경로 안 62파일. outside/unmerged 0. |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 23:57:28.970556 → 23:57:36.261918 | 0 | doctor, acceptance, research-case, original-smoke 통과. 세션 자동 발견 0개, `no_active_sessions`. |
| `python -B docs/workstreams/research/AF-RES-108/adjudicate.py --check --cache /tmp/af108/docs` | 23:57:36.262136 → 23:57:36.325832 | 0 | 인용 지문과 순번, 파일/후보/예산 16쌍, 입력·두 출력과 근거, 집계. |
| `python -B docs/workstreams/research/AF-RES-108/render_result.py --check` | 23:57:36.325872 → 23:57:36.381375 | 0 | 첫 표부터 8·32·19행이 원장과 일치. |
| `python -B -m unittest discover -s docs/workstreams/research/AF-RES-108 -p 'test_*.py' -v` | 23:57:36.381407 → 23:57:36.436546 | 0 | 문장·목록·코드·길이 0/1·Unicode 좌표·예외 교체, 6시험. |

23:58:08.531074–23:58:10.801812 UTC에 고정 SHA의 raw GitHub 14개 파일 바이트를 Git blob과 대조했다. RESULT, SELF_CHECK, reproduce, packets, predictions, runs, pairs, metrics, sources, 원 기대, 변이 기대, 보조 교정, F1·F4 PNG가 일치했다. Connector에서도 RESULT, 원 기대, 실행 대표 두 행과 reproduce를 다시 읽었다. 이 인계 커밋은 해당 검사 기록의 후속이다. [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/806cdff845acfb965a1b2f2a641010c2e9604498/docs/workstreams/research/AF-RES-108/RESULT.md) · [고정 실행 원장](https://github.com/laadkke-arch/agentflow-open/blob/806cdff845acfb965a1b2f2a641010c2e9604498/docs/workstreams/research/AF-RES-108/runs.jsonl) · [고정 재현](https://github.com/laadkke-arch/agentflow-open/blob/806cdff845acfb965a1b2f2a641010c2e9604498/docs/workstreams/research/AF-RES-108/reproduce.md)

## 미확인·미실시와 재개

- 고유 1차 직접 열람 전체는 36개다. 필수 24자리 중 SQLite canonical 회귀 4개와 POSIX 원 규격·시험 2개가 비어 18개를 채웠다. GitHub mirror 4개에서 정식 소스의 manifest와 시험 SHA3를 일치시켰다. 해당 canonical 파일과 The Open Group·Savannah 직접 열람은 미확인이다. [출처](sources.jsonl) · [접근 결과](evidence/access-notes.md)
- 공식 SQLite 3.51.1 docsrc 네 쪽은 미확인이다. SQLite 게시자 페이지 캡처를 대신 사용했다. W3C는 당시 CRD를 제공했으나 두 영역 모두 원시 HTML 맵이 미확인이다. Cloud 셸 정책은 해당 원 도메인 HTTP를 거절했고 웹 경로도 일부 조회를 거절했다. [문서 캡처](evidence/documents.json)
- SQLite 원 Tcl suite와 다른 브라우저 엔진, 독립 사람 판독은 미실시다. SQL 원 Tcl 결과와 로컬 CLI 출력을 비교했다. 실행이 필요한 후속 입력은 [재현](reproduce.md)에 있다. 새 엔진의 결과는 현재 Chromium 영수증과 분리한다.

**재개 첫 행동**은 고정 결과 SHA에서 과거 문서 다운로드를 시도하는 것이다. 공식 ZIP과 [docsrc](https://sqlite.org/docsrc)의 당시 파일을 확인한 뒤, 등록된 입력으로 새 자료 수집 회차를 만든다.

```sh
git checkout --detach 806cdff845acfb965a1b2f2a641010c2e9604498
task_cache=/tmp/af108-resume
mkdir -p "$task_cache/docs"
curl -fL https://sqlite.org/2025/sqlite-doc-3510100.zip -o "$task_cache/sqlite-doc-3510100.zip"
curl -fL https://www.w3.org/TR/2025/CRD-css-flexbox-1-20251014/ -o "$task_cache/docs/flexbox.html"
```

색인 제안 — AF-RES-108 · PARTIAL · SQLite 3.51.1/Flexbox 8쌍 · K/E 확정 8/16씩, 오답 0/8씩 · F2 정상 정답 1을 회복하고 F4 정상 정답 1을 잃음 · 고정 SQLite 문서와 canonical/POSIX 직접 열람 결원. [색인 한 줄](INDEX_PROPOSAL.md)

| 가장 중요한 불일치·약점 | 다음 조사 제안·직접 열 자료 또는 실행할 입력 | 어떤 관측이면 판단을 바꿀지 |
| --- | --- | --- |
| E는 F2의 정상 정답 1개를 얻고 F4의 정상 정답 1개를 잃었다. 주 사전 오답은 0이다. | 별도의 판독자에게 각 입력의 한 방식만 배정한다. F2 두 줄 높이와 F4 80px in-flow 아이템을 새 입력으로 봉인한다. | K의 오답이 E에서 유보·정답으로 이동하고 정상 손실보다 자주 일어나면 예외 우선 범위를 넓힌다. |
| SQLite 당시 문서 네 쪽과 두 분야 원시 HTML 맵이 미확인이다. | [SQLite 3.51.1 ZIP](https://sqlite.org/2025/sqlite-doc-3510100.zip), [공식 docsrc](https://sqlite.org/docsrc), [Flexbox CRD](https://www.w3.org/TR/2025/CRD-css-flexbox-1-20251014/)를 받아 동일 selector를 재실행한다. | 판·표현이 바뀌어도 S3 근거 손실과 F2/F4 전환이 유지되면 그 관측의 문서판 의존성을 낮춘다. |
| SVG parity·초기값이 가려졌고 POSIX 원본 직접 열람이 실패했다. | [Open Group](https://pubs.opengroup.org/onlinepubs/9699919799/functions/fnmatch.html), [Savannah fixture](https://git.savannah.gnu.org/cgit/gnulib.git/tree/tests/test-fnmatch.c), [SVG2 §13.4.2](https://www.w3.org/TR/2018/CR-SVG2-20181004/painting.html#FillRuleProperty)를 열어 표 행과 조건절 보존을 비교한다. | 같은 문자 비용에서 실제로 잘린 parity와 FNM_PATHNAME을 회복하고 정상 근거도 유지하면 표지 사전을 바꾼다. |
