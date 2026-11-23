# Reproduction and unperformed checks

## Performed D3 diagnostic

Executor: `/root/graph_releases`, shared cloud checkout. Actual run UTC: `2026-11-23T05:33:16.773Z`. Node `v24.22.3`, Linux x64, kernel `6.18.57`. This is a researcher auxiliary execution, not an upstream author's original output. Installation and runner exited 0. No native Graphviz test was run.

From repository root, the actual package installation was:

```sh
npm install --prefix docs/workstreams/research/AF-RES-061/streams/graph/cache/d3-run --cache docs/workstreams/research/AF-RES-061/streams/graph/cache/npm-cache --no-audit --no-fund --ignore-scripts d3-force@3.0.0 d3-quadtree@3.0.1 d3-dispatch@3.0.1 d3-timer@3.0.1
```

The selected tag's source files were independently downloaded from their fixed GitHub SHA. `fetch-pinned.py` packages that already performed retrieval for a new checkout; this convenience wrapper itself was not separately rerun. It checks the recorded content digests before saving.

```sh
python -B docs/workstreams/research/AF-RES-061/streams/graph/fetch-pinned.py
```

The actual execution was:

```sh
node docs/workstreams/research/AF-RES-061/streams/graph/d3-probe.mjs > docs/workstreams/research/AF-RES-061/streams/graph/d3-run.json
```

For a verification rerun, preserve the original output and redirect to the ignored cache instead:

```sh
node docs/workstreams/research/AF-RES-061/streams/graph/d3-probe.mjs > docs/workstreams/research/AF-RES-061/streams/graph/cache/d3-rerun.json
```

The script imports actual tagged-package force code and compares `manyBody.js`, `simulation.js`, `jiggle.js`, and `lcg.js` byte-for-byte with the independent fixed-source downloads. The preserved `d3-run.json` includes source hashes and the script digest. Its O(n²) comparison is our kernel-derived reference. It is not independent physical truth, and coincidence is excluded from that reference. The source's zero-sum aggregate pruning is intentionally retained, exposing why theta0 can still disagree with pairwise signed-strength calculations.

## Exact input inventory

`d3-probe.mjs` is the executable input definition. It runs the two sealed D3 inputs, cutoff equality, clamped/unclamped near pairs, seed1 coincidence, seven-node theta0/.9/2, three-node cutoff exact/approximate, and mixed-sign zero-aggregate cases. `d3-error-analysis.json` is a post-hoc transformation of the preserved outputs, using Euclidean per-node absolute and relative errors. No timed benchmark was performed.

## Graphviz native checks: 미실시

Selected source is `a74b50c20fc624f46f72e24f981b261f6e5edf71` (14.1.1). The reviewed upstream assertions can be rerun in an exact-version checkout/build, with that build's `dot`/`sfdp` on `PATH`:

```sh
python -m pytest tests/test_regression.py -k 'test_2225 or test_2283 or test_2556'
```

Inputs are the exact tag's `tests/2225.dot`, `tests/2283.dot`, and `tests/2556.dot`; URLs and digests are in `source-receipts.json`. `test_2572` is deliberately not included as an sfdp validation because it passes `-Kneato`. Confirm the executable version and GTS build capability before interpreting return codes; the tests themselves account for unavailable triangulation support. This command was not executed, and no pass is claimed.

A public command such as `sfdp -Gmaxiter=1 -Gstart=regular` does not implement the sealed one-step contract in the inspected source. Therefore no public CLI command is offered as though it would validate GV-N/B.

For the private auxiliary hand calculations, the minimum next execution requires a native harness linked against the selected build. It must construct a symmetric 2×2 CSR adjacency matrix with one edge, `dim=2`, and set `random_start=false`, `maxiter=1`, `p=-1`, `K=1`, `step=.1`, `adaptive_cooling=false`, `beautify_leaves=false`, normal quadtree mode. Call `spring_electrical_embedding` directly, once with `x=[0,0,3,4]`, once with `x=[0,0,0,0]`, and print `flag` and all four coordinates before any multilevel/postprocessing call. No such harness was built or run. It would validate the two explicitly private auxiliary rows only, not repair the public main-row contract or supply independent original output.
