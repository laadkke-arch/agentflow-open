# Gold evidence reproduction

All commands run from repository root. Public URLs are explicit and fixed; the downloader does not discover or crawl links. No dependency installation is needed beyond Python standard library and an already available Godot executable.

```sh
python -B docs/workstreams/research/AF-RES-112/gold-work/fetch_examples.py
godot --version
python -B docs/workstreams/research/AF-RES-112/gold-work/run_original_current_engine.py
python -B docs/workstreams/research/AF-RES-112/gold-work/run_gold_checks.py
```

The recorded installation was `4.7.2.stable.official.ed1daf0bf`. New runs record the actual installed version; changing it is a different execution, not replication of historical 3.4.2 / 4.0-dev.20220118. Original records are `run-current-engine.json` and `run-controlled-current-engine.json`; new replay logs go under ignored `examples/` and do not overwrite them.

The extraction keeps only project configuration and textual script/scene/resource files from the original ZIP. Icons and editor caches are deliberately not executed or supplied. This is an extraction difference from the full original archive, recorded here; relevant source/config bytes are preserved. Original archive size/hash and full member list are in `original-artifact-receipts.json`. Current-engine imports generate fresh caches. The relevant project scripts have been read before execution and contain only local object/scene operations.

G2 original uses its own assertion. OS exit zero is not proof that the assertion passed: inspect stderr and the printed result. All-ones is a researcher-constructed input from the frozen request. Removing UID attributes is a supplemental counterexample that preserves the Number/Sum types and stored values; it is not asserted to be the original author's resave operation. G3 current-engine run uses the author's later Godot4 port, which has a different local flag than the original Godot3 ZIP. The one-flag variant and constructed G1 lifecycle checks are supplemental, not main reader trials.

## Historical tests not executed

After obtaining the user's permitted, already available exact binaries, run the original Godot3 project with `timeout --signal=TERM 10s godot-3.4.2 --no-window --path docs/workstreams/research/AF-RES-112/gold-work/examples/G3/test res://main.tscn`. Here `godot-3.4.2` must resolve to the exact 3.4.2 binary; it is an unmet prerequisite, not an installed command in this session. Timeout exit124 means the process remained running after observations and must not be called a passed test. The original project contains breakpoint/stop metadata but may remain running afterwards. For G1, use the fixed original repository at `1a5942e87c2510e6f9fb281ba27f6a257258eb35`, retain each `.tscn` flag, change only the load/preload call in two separately copied projects, record references and process one frame before re-instantiation. For G2 use the exact `4.0-dev.20220118` build after resolving its commit identity, with fresh cache and the hash-checked original ZIP. Capture each item's UID/path/instance ID/value as well as total and assertion stderr.

No historical binary was installed or executed during this task. The source-supported grade and the unverified historical numeric outcome have separate fields in gold.csv.

## File and originality accounting

The original requests are counted only in recruitment. Attached programs count as distinct authored artifacts but retain the same request/author lineage; they are not independent corroborations. All Godot manual chapters/versions count once and all engine implementation files/patches count once. Irrelevant issue79944 and the dead demo4.0-dev URL are recorded without increasing the primary-original denominator. The source count file is an accounting aid, not an acceptance claim for the overall24-source allocation.
