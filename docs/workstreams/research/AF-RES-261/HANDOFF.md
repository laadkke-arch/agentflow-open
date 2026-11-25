# AF-RES-261 HANDOFF

**자체 상태 PARTIAL** (중앙 status는 수정하지 않음). 고정 결과·자기 점검 커밋 **7b785cc63133c096ae2fac9251a31ed7c31f3cb1**. 작업 브랜치 work/research-af-res-261; 착수 integration 95c94f58adcb5579ee3d28ead7d58503f4dbb9b5. [결과 고정판](https://github.com/laadkke-arch/agentflow-open/blob/7b785cc63133c096ae2fac9251a31ed7c31f3cb1/docs/workstreams/research/AF-RES-261/RESULT.md) · [자기 점검](https://github.com/laadkke-arch/agentflow-open/blob/7b785cc63133c096ae2fac9251a31ed7c31f3cb1/docs/workstreams/research/AF-RES-261/SELF_CHECK.md) · [범위](https://github.com/laadkke-arch/agentflow-open/blob/7b785cc63133c096ae2fac9251a31ed7c31f3cb1/docs/workstreams/research/AF-RES-261/SCOPE.md) · [9셀](https://github.com/laadkke-arch/agentflow-open/blob/7b785cc63133c096ae2fac9251a31ed7c31f3cb1/docs/workstreams/research/AF-RES-261/features.csv) · [소비자](https://github.com/laadkke-arch/agentflow-open/blob/7b785cc63133c096ae2fac9251a31ed7c31f3cb1/docs/workstreams/research/AF-RES-261/consumers.csv) · [갱신/반례](https://github.com/laadkke-arch/agentflow-open/blob/7b785cc63133c096ae2fac9251a31ed7c31f3cb1/docs/workstreams/research/AF-RES-261/refresh.md) · [원자료 원장](https://github.com/laadkke-arch/agentflow-open/blob/7b785cc63133c096ae2fac9251a31ed7c31f3cb1/docs/workstreams/research/AF-RES-261/sources.jsonl). 이 인계 파일의 자체 SHA는 마지막 커밋 후 확인해야 하므로 본문에 순환 참조하지 않는다.

## 완료 / 미달

- 의존 AF-RES-248 중앙 DONE, 자체 PARTIAL, [HANDOFF fixed] (https://github.com/laadkke-arch/agentflow-open/blob/4a690fc68182b8b2792c15d921ed3baeeaa7220e/docs/workstreams/research/AF-RES-248/HANDOFF.md), RESULT b55e3a7a283076085b09e70fbb4eacbdc3ae92fd. Own path, current control row and dependency confirmed; SCOPE precommit caefb9459ef24bafc70b9144a486aad6aa6607ac. Source bundles 1c26459589f25830e0a46da8e268e1eac6bfd158, 648793f0629e50a3bcc977f2de55c81a2d85f04d, 54d1a333f079da5009b5401d12f6c344a52e9bce. Cell commit 7f4774087b559b06cd9046df9be6b9c7663e028e, consumers 284a9ade88609d283f870da6e04fbc3880b25a4c, refresh 200ca1311d1f092923c579333755b7c1c6dd94eb, RESULT f68f949200d109521493869b69a1a0a10f41c09b, SELF_CHECK 7b785cc63133c096ae2fac9251a31ed7c31f3cb1.
- docs.rs original Linux build #1342362: actual --all-features and cfg docsrs,tokio_unstable,tokio_taskdump; distinct from consumer default/full and local runtime. Three canonical rendered function pages not retrievable in this session; source definitions and root/log verified, exact per-function HTML 0/3 (misreceipts not proof absence). 
- Tokio exact 1.40.0 isolated Linux 9/9 static feature gate comparisons: 3 excluded by source, 6 included by source, compile 0/9, run 0/9. Minimum export feature vs runtime feature separate. full with default Builder IO/timer off counterexample source-backed, not executed.
- Two fixed workspaces Vector v0.41.1 and cargo-binstall v1.10.5: 2/2 manifests, pinned locks with 1.40.0 and actual timeout call sites; graph witness 0/2, version-only real caller 0/2. No isolated/default-only claim from lock. Actual Windows/non-Unix ctrl_c source calls not Linux receipts. Additional batch attempt exceeded tool limit, no result. Exact version-only witness remains core missing.
- Two change positions confirmed source diff: 1.41.0 cfg_fs WASI condition removed but stable wasm global compile_error remains; Iroh #3993 signal/process removal and relay server signal forwarding (different unresolved Tokio version). No changed build/runtime receipt. GDAL GTiff/netCDF 2/2 config and example sources, actual selected distribution binary 0/2. 
- JSONL: 99 rows (94 access yes, 5 no), 50 counted unique lineages; classes 14/6/14/8/8 meet 7/4/5/3/3, no failed row counted. Individual access timestamp unrecorded (UTC date only). Format checks directly parsed 9×19 features and 4×18 consumer traces in fixed RESULT snapshot; no independent review. Workbench local session/check not performed (connector-only). No paid API, no merge/deploy, no actual cargo build/signal/service/GDAL operation. No dot-control modification.
- Index proposal: evidence_type=source+original-docs-build; object=crate API; qualifiers=crate version/source SHA/target/docs build ID+flags/direct requested features/effective graph/runtime driver/input; statuses=rendered page, public gate, consumer compile, run separately. Mark api_display=unknown for 3 failed HTML fetches, graph/compile/run=unobserved; not unsupported merely from missing receipt. Attach RESULT tables and sources IDs. Refresh on package/target, doc build, manifest/lock/graph selection, runtime/input changes. Keep older claims immutable.

## 다음 첫 행동 (web worker)

Directly reopen exact rendered target pages, save HTTP status, body/title, availability badge and anchor, target/version/time:
- https://docs.rs/tokio/1.40.0/tokio/fs/fn.read.html
- https://docs.rs/tokio/1.40.0/tokio/time/fn.timeout.html
- https://docs.rs/tokio/1.40.0/tokio/signal/fn.ctrl_c.html
- target-specific prefix https://docs.rs/tokio/1.40.0/x86_64-unknown-linux-gnu/tokio/ (same paths after prefix)
- actual build https://docs.rs/crate/tokio/1.40.0/builds/1342362/x86_64-unknown-linux-gnu.txt ; compare adjacent https://docs.rs/crate/tokio/1.41.0/builds .
If access fails, record actual failure and verified pinned source fallback; do not transform failure into absent page. Search additional real version-only consumers using small manifest batches of 3–6, pin release SHA, record normal dependency edge + Cargo.lock same identity + actual API call source, compare selected graph witness. Begin with exact 1.40.0 lock candidates already screened (Zed v0.154.3, SurrealDB v2.0.1, cargo-binstall v1.10.7; not selected as completed samples). No relaxed version substitutions.

## Codex 검산 인계 — 실행하지 않은 명령·입력·예상

Use fresh isolated scratch directory (not production or shared service); only save receipts in authorized follow-up owned_path, not original integration. Check compiler version and target, same crate pin. Resolve lock once per cell then use locked commands; transitive dependency versions not already pinned, record each generated lock and package source/checksum. Capture stdout/stderr, exit code and UTC start/end, command, toolchain, manifest and source SHA/hash, target, selected features, lock hash, sample input hash. Use exact 1.40.0; if no registry cache/network or target toolchain, report blocked. No bypass, new install/account changes, or arbitrary live signals. 

Shell inputs for 9 isolated compile gates (proposal, not run):
```sh
rustc -Vv
cargo -Vv
# in a temporary sandbox, separate directories per cell, e.g. mktemp -d
# each Cargo.toml: package name = "afres261_f1" (change per cell), version = "0.0.0", edition = "2021"
# [dependencies] as exactly one of:
# tokio = "=1.40.0"
# tokio = { version = "=1.40.0", default-features = false, features = ["fs"] }
# tokio = { version = "=1.40.0", default-features = false, features = ["time"] }
# tokio = { version = "=1.40.0", default-features = false, features = ["signal"] }
# tokio = { version = "=1.40.0", features = ["full"] }
# F1-3 fs: src/main.rs = fn main() { let _ = tokio::fs::read("fixture.txt"); }
# F4-6 time: fn main() { let _ = tokio::time::timeout(std::time::Duration::from_millis(50), std::future::ready(7)); }
# F7-9 signal: fn main() { let _ = tokio::signal::ctrl_c(); }
# create each corresponding declaration in features.csv; no extra Tokio dependency edges
cargo generate-lockfile
cargo tree --locked --target x86_64-unknown-linux-gnu -e features -i tokio@1.40.0
cargo metadata --locked --format-version 1 --filter-platform x86_64-unknown-linux-gnu
cargo check --locked --target x86_64-unknown-linux-gnu
```
Expected gate failures F1/F4/F7, gate-included predictions F2/F3/F5/F6/F8/F9; compare actual errors (unresolved module vs unrelated dependency/toolchain error). Do not run these compile-only snippets (timeout constructing outside runtime is intentionally not a runtime test). Reverse: compile succeeds on isolated default or feature absent in graph despite minimum request, or another error invalidates attribution; recheck lock/target/graph. Record failed command too. Build selection examples:
```sh
# read-only clones/worktrees, fixed SHAs
# vector 745babdc7dfa183feaab26ce915c15b10cd5bb6b
# from Vector root, selected root package:
cargo tree --locked --target x86_64-unknown-linux-gnu -p vector -e features -i tokio@1.40.0
cargo metadata --locked --format-version 1 --filter-platform x86_64-unknown-linux-gnu
# cargo-binstall f9144d57df0014c2e0975517e582dbaaa2b597af
cargo tree --locked --target x86_64-unknown-linux-gnu -p cargo-binstall -e features -i tokio@1.40.0
cargo tree --locked --target x86_64-unknown-linux-gnu -p binstalk -e features -i tokio@1.40.0
cargo metadata --locked --format-version 1 --filter-platform x86_64-unknown-linux-gnu
```
If package names/feature selections differ, read manifests and record changed selector, not silent substitution. Do not build entire product or operate service; graph first. Compare selected package vs workspace flags only with explicit selection. Need a controlled two-member synthetic counterexample too: workspace resolver="2"; app depends on tokio = "=1.40.0" and normal path dep helper; helper declares tokio = {version="=1.40.0",features=["time"]}, helper lib exports e.g. pub fn marker() {}. app main calls helper::marker(); let _ = tokio::time::timeout(Duration::from_millis(50),std::future::ready(7)); check app with helper present then separate identical app with helper edge removed and marker call removed. Record both locks/tree/check receipts; expect success with normal unified time, failure without. Repeat inactive target or dev-only edge as separate case if needed (resolver2). This fixture proves mechanism only, not actual public workspace witness.

Runtime follow-up only in isolated Codex fixture: separate manifest variants features=["fs","rt"], ["time","rt"], ["signal","rt"] and ["full"], default-features=false for minimal; use manually configured runtime (no macros required). 
- fs: write ordinary scratch fixture.txt containing bytes "hello" (no newline), input hash; src/main.rs main creates tokio::runtime::Builder::new_current_thread().build().unwrap(); rt.block_on(async { assert_eq!(tokio::fs::read("fixture.txt").await.unwrap(), b"hello"); }); then missing file variant expected Err. No special pipe/large file.
- time: same builder with .enable_time().build(), inside rt.block_on(async { assert_eq!(tokio::time::timeout(std::time::Duration::from_millis(50), std::future::ready(7)).await.unwrap(),7); assert!(tokio::time::timeout(std::time::Duration::from_millis(20),std::future::pending::<()>()).await.is_err()); }); repeat full without enable_time/enable_all: expect runtime panic; with enable_time expect success. Keep error text and exit status; time duration is fixture input, not latency guarantee.
- signal: full without IO driver expected missing signal driver panic on first poll. Positive separate child uses Builder::new_current_thread().enable_io().build() with signal+rt or full; in async block pin tokio::signal::ctrl_c future and poll once to Pending (import std::future::Future and std::task::Poll; poll_fn maps Pending to Ready(()), unexpected Ready is error); print and flush READY after registration; await future, print RECEIVED, exit. Only if authorized in Codex, test supervisor launches that one fixture child, observes READY, checks PID belongs to its own child, sends SIGINT only to that PID, collects RECEIVED, waits; no terminal/process group/live external service signal. If no controlled child isolation or timeout, mark unexecuted. No action in this web session. 
```sh
# in each explicit runtime fixture after lock/tree metadata
cargo run --locked --target x86_64-unknown-linux-gnu
```
Reverse criteria: enabled driver case still fails with matched graph/input, or disabled driver succeeds under verified same Builder; inspect hidden runtime/setup. No runtime claim until matched original receipt. For gdAL, if separately approved binary fixture on installed release, capture gdalinfo --version, gdalinfo --formats, gdalinfo -checksum byte.tif (expected test-source checksum 4672), gdalinfo sst.nc and gdalinfo 'NETCDF:sst.nc:tos' with exact fixture hashes and plugin paths; docs example not input availability guarantee. No new GDAL test this turn.

## Workbench contract checks (not executed)

Connector branch compare confirmed only owned files; no local checkout so cannot run workbench.session. At source 95c94f5, docs/CLOUD_WORKFLOW.md L69–81 and workbench/session.py L299–313 specify start/check flags. If existing original session manifest exists, read it and run python -m workbench.session check <original-manifest> --fetch; do not overwrite. This task began without a local manifest. For authorized follow-up create a new session contract (not retroactive proof) at fresh integration baseline, with actual result dependency and approved owned path. Example for reconstruction of original required inputs, if allowed in a separate session with original branch and no overwrite:
```sh
git fetch origin
git checkout work/research-af-res-261
git diff --name-only 95c94f58adcb5579ee3d28ead7d58503f4dbb9b5..HEAD
# original required start invocation, not actually performed; use new filename if follow-up:
python -m workbench.session start af-res-261 --allow docs/workstreams/research/AF-RES-261/ --dependency work/research-af-res-248=4a690fc68182b8b2792c15d921ed3baeeaa7220e --output docs/workstreams/research/AF-RES-261/session.json --fetch
python -m workbench.session check docs/workstreams/research/AF-RES-261/session.json --fetch
```
Run only with authorized follow-up write; do not add session file after this final HANDOFF in this worker. If integration moved, treat start as new baseline, not prior success; note dependency/contract changes. No independent verifier receipt. Final worker response should report this HANDOFF commit SHA and fixed results; integration owner decides next scheduling.
