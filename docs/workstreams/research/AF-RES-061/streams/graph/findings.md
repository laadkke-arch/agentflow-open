# Graph stream findings

## Outcome and evidence status

The exact d3-force 3.0.0 source supports the sealed repulsion and finite-cutoff directions. Our own run gives D3-N velocity increments `(-3.6,-4.8),(3.6,4.8)` and D3-B zero increments. It does not establish an independent historical original output. Graphviz 14.1.1's public sfdp path does not preserve the proposed fixed initial positions or expose the requested one-step control in the inspected path. GV-N and GV-B therefore remain **미확인**, with the point of failure identified rather than replaced by final-layout quality.

Evidence: [observations.json](observations.json), [d3-run.json](d3-run.json), [transfer-notes.md](transfer-notes.md), G020/G025/G026 in [sources.jsonl](sources.jsonl). Main rows: 4. Exact-version researcher executions: 2 main plus 10 post-hoc D3 diagnostics. Native Graphviz execution: **미실시**. Same-version/same-input independently archived original outputs found in reviewed material: **관측 0/4**, with existence outside the reviewed scope **미확인**. These four graph rows are not an ecosystem sample or a human A/B experiment.

## Q1 — Why designers use the implementation

**API purpose.** Tagged D3 documentation describes configurable attraction/repulsion of all nodes, with approximation for large populations. Graphviz's sfdp documentation describes a multiscale layout for large undirected graphs. Those are maintainer API intentions, not direct reports of what any one designer needs. G011/G012/G017 preserve the version and live-document qualifications.

**First recruited D3 usage.** The complete preserved release-window search has 24 issue metadata records. #162 is a unit-test request, excluded by the frozen rule. The next issue, [#166](https://github.com/d3/d3-force/issues/166), is JFLopez7's request to show nodes and links for groups above 3 in a production-like dummy graph. Its linked [Plunk](https://embed.plnkr.co/plunk/SawtfmR9iZvlLWue) directly uses `forceManyBody`. The attached input contains 77 nodes and 254 links; the script uses an 800×600 coordinate basis, strength −3000 for graph nodes, and a separate 154-node/77-link label simulation with strength −50. It calls the label simulation's `alphaTarget(.3).restart()` on graph ticks. These counts come from our parsing of the author's input, not a new output prediction. The script loads a mutable D3 major-5 bundle; exact component version is **미확인**, and this does not establish d3-force 3.0.0 behavior. G044/G047/G064.

The requested screen change is filtering. Fil's reply points to existing opacity logic. It does not require the astronomy paper. No subsequent successful user deployment or behavior change was reported in the inspected discussion. This is a concrete case where a product/API answer can be sufficient.

**First recruited Graphviz usage.** The preserved `search=sfdp` release-window roster contains seven records. Earlier matches use neato, dot, gvpr, or concern building. The first eligible sfdp record is [#2852](https://gitlab.com/graphviz/graphviz/-/issues/2852), a relay of [gertburger's forum report](https://forum.graphviz.org/t/sfdp-crash-regression-in-15-1-1/3392). The original input is a 24-node/23-edge graph. The user expects SVG output and reports an allocator abort in 15.1.1; the tracker relay reports PNG failure on a 15.1.1 development build under Ubuntu 24.04.4. The forum says 15.1.0 worked and the fix landed in 16.1.0. All are author reports; none tests selected 14.1.1. G053/G062.

Firstness is limited to the saved query and criteria. The Graphviz planned window ends 2026-12-13, after our 2026-11-23 read date, so it is right censored. A newly discovered earlier eligible issue, archived removed issue, or alternate wording could revise firstness. The selected issue remains useful as a purpose report but cannot validate the main version.

## Q2 and Q3 — Attribution and what crossed the boundary

[transfer-notes.md](transfer-notes.md) gives the executable mapping and exact locations. D3 explicitly attributes the Barnes–Hut algorithm through its name and a secondary link; the reviewed tagged records do not directly cite the primary paper. Graphviz directly links Hu, who cites Barnes & Hut. Neither observation by itself identifies the library author's historical reading process.

D3 transfers tree aggregation and an opening test while using a velocity-increment kernel with magnitude 1/r, signed strength, alpha cooling, finite range, minimum-distance capping, and seeded jitter. Graphviz transfers multiscale force-layout ideas and tree aggregation, but normalizes the net vector into a per-vertex displacement, updates vertices sequentially, randomizes initial coordinates, and applies presentation postprocessing. Primary-source physics is a way to identify assumptions to check. It does not replace those receiver contracts.

Counterevidence sought: code paths that would preserve fixed positions, make `maxiter=1` public, use a gravitational inverse-square magnitude, or prove theta zero exact. `getPos` initially appeared to support the first possibility; tracing its caller and later random overwrite disproved that inference for the ordinary path. D3's signed aggregate early return disproved unconditional theta-zero exactness. The source comment and operative Graphviz force coefficients are separately recorded, avoiding equation-by-comment equivalence.

## Q4 — What additional documents changed

The graph helper's baseline and A remain sealed in their original files. D3 A supplies a composition example combining many-body, link, and centering forces. It does not add an exact direct-force kernel or a different prediction for the selected D3 normal/boundary pair. Graphviz A could not be recruited under the first-related-section rule; the missing treatment is retained rather than filled with a test assertion or final image. Root owns the separately sealed B predictions and determines differing-view denominators.

The post-seal source findings here must not be counted as changes made by the 250-word A or B window. The helper did not read donor B before sealing A. General model knowledge and incidental API/search exposures are recorded in [exposure.md](exposure.md). There was no independent participant sample or measurement of designer behavior.

## Q5 — What the observed version supports

The D3 runner imports the installed package's actual source, not a reimplementation. Four relevant source files are byte-identical to the independently fetched selected commit. Dependencies match the tag's lockfile. [d3-run.json](d3-run.json) preserves the runtime, all inputs, outputs, source hashes, and script digest. [reproduce.md](reproduce.md) has exact commands.

All five suites in the selected D3 `test/` directory were read. They cover center, collide, find, simulation, and x/y forces. There is no many-body test file or matching main-input assertion in that directory. `forceCollide`'s equal-and-opposite coincidence assertion is not transferred to manyBody; our manyBody jitter diagnostic actually lacks that symmetry. G031–G037, [test-inventory.json](test-inventory.json).

For Graphviz, the selected tag's regression file contains four functions mentioning sfdp, with fixtures for curved splines, beautify spacing, GTS assertions, and isolated nodes. These are executable expectations, not archived successful runs. The isolated-node test invokes `-Kneato` despite its sfdp wording. No reviewed fixture records the two main fixed-coordinate one-step cases. The review covers the named files and a partial tree listing, not every repository artifact. G038–G043.

Two historical author outputs were directly inspected: #2283's image shows N1/N6 overlapping in the same leaf position; #2560's actual DOT screenshot has all four nodes at `(36,36)` whereas its expected screenshot separates them. The report's internal-zeroing diagnosis and final translated coordinates are distinguished. These are independent user-reported events but different inputs/versions, so they cannot fill GV-N/B. G055/G056/G059–G061. #2572's image URLs failed with 404 on the correct public path; its body is direct evidence only of the author's report.

## Q6 — Counterexamples and sensitivity

| Diagnostic | Exact result or evidence type | What it defeats |
|---|---|---|
| D3 distanceMax equality | Own run: separation 5, max 5, zero increments | Interpreting maximum radius as an inclusive boundary. Source uses a strict comparison. |
| D3 minimum distance | Own run: pair separation .05 gives speed 30 at minimum1, speed600 at minimum0 | Extending an uncapped singular kernel into product coincidence handling. |
| D3 coincidence | Own run: finite seeded increments; summed velocity `(26.254215790996636,-16.66231297314544)` | Assuming physical pairwise momentum conservation from N-body vocabulary. |
| D3 opening-angle sensitivity | Seven-node corpus, theta0/.9/2: maximum vector errors about `2.84e−14 / 2.77128 / 33.0790` against our exact-pairwise reference | Treating theta as a universal accuracy guarantee; mean/median alone hides uneven node error. |
| D3 cutoff plus aggregation | Receiver at0, source(9.9,.1) inside10, source(10.1,.2) outside10: theta0 gives receiver `(-3.02999,-.030606)`; theta.9 gives zero | Treating an approximate aggregate cutoff as an exact pairwise geometric fence. |
| D3 mixed signs | theta0 with source strengths+30 and−30 and receiver0 gives all-zero implementation output; reference is nonzero | Assuming disabling far-field acceptance guarantees exact summation even when zero-sum aggregate pruning remains. |
| Graphviz scale postprocessor | #2560, version11.0.0: four final positions all36,36; author identifies no-overlap scaling bug | Assuming a successful force model guarantees final readable geometry. |
| Graphviz beautify | #2283: six expected spokes become five distinct visible positions with two labels overlapping | Treating presentation heuristics as consequences of physical equilibrium. |
| Graphviz fixed coincident input | Public main row **미확인**; private-control arithmetic predicts zero motion | Confusing a privately forced initial condition with the public random-start path. |

The full D3 error distribution is in [d3-error-analysis.json](d3-error-analysis.json). At theta .9, mean relative vector error is 0.00398485 and maximum 0.0264791; at theta2 these are 0.162555 and 0.431830. There are seven deliberately selected nodes, not seven independent trials. These values are local diagnostics, not transplanted astronomy error bounds. Runtime/cost benchmarking was **미실시**; the reference enumerates pairs, but no speedup claim is made.

The independent design issue [#186](https://github.com/d3/d3-force/issues/186) supplies an actual mismatch between user expectation and aggregation. A user wants fixed polygon-fence nodes to repel locally while free nodes interact over longer ranges. The maintainer explains the receiving-node field and suggests layering forces or a wall alternative. A later contributor's per-node-cutoff patch fails on an internal quad without `data`; the maintainer explains that descending to every point defeats the intended pruning. This is a documented implementation tradeoff, not our hypothetical user story. G046/G049.

Searches used explicit `sfdp overlap`, `sfdp pos`, `sfdp maxiter` and the release-window rosters. Rejected candidates and access failures are in [issue-search-rosters.json](issue-search-rosters.json) and [search-log.jsonl](search-log.jsonl). Failure to find a same-input original output is scoped to these materials. The minimum new evidence would be an archived same-version manyBody output fixture or an upstream instrumented Graphviz one-step trace that specifies actual initialization and private/public interface.

## Q7 — First return links and changes of decision

| Card | First return link and current reason | Stakeholder conditions | Smallest evidence that changes the choice |
|---|---|---|---|
| D3 many-body | [Tagged many-body API](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/README.md#many-body-forces), followed by exact `apply` source. It states the options the designer can actually select. | A numerical-method author needs the original aggregation/error assumptions plus receiver kernel. A maintainer needs signed weights, cutoff and zero-cell behavior. A UI developer needs compositional forces and drawing/tick behavior. A motion-sensitive reader may need a static representation or a stop interaction, a product preference not answered by BH. | A real task demanding measured approximation error rather than basic separation would move the donor method/error source first. A stated fencing/filtering or motion requirement instead moves the goal-specific API/example first. A linked donor-induced successful design change would be needed to claim behavior benefit. |
| Graphviz sfdp | [Pinned tuneControl and layout path](https://gitlab.com/graphviz/graphviz/-/blob/a74b50c20fc624f46f72e24f981b261f6e5edf71/lib/sfdpgen/sfdpinit.c#L200-224), with the question whether the task needs final readable layout or controlled internal forces. The main input cannot currently be expressed as a documented one-step contract. | A donor author can explain multilevel/long-range tradeoffs. A maintainer needs initialization, build features, overlap and packing. A UI developer needs the exact graph, labels, desired separation and failure environment. A reader burdened by clutter needs evidence about overlap/readability, not force magnitude alone. | An official fixed-position/one-step trace would make the implementation comparison directly testable. A real graph with confirmed no-overlap and readability priorities would move official usage/overlap guidance first. An approximation-cost question with matched coordinate definitions would move Hu's algorithm first. |

General reduced-motion guidance is not evidence that these numerical libraries read a preference. The reviewed fixed D3 manyBody/simulation source provides calculations and event scheduling; rendering and preference policy belong to the surrounding application. No experiment measured motion-sensitive readers, comprehension, or changed design decisions in this stream. The first-link recommendations are researcher judgments based on the documented contract and missing user priorities.

## Three material remaining weaknesses

| Weakness | Affected claim | Next minimal evidence |
|---|---|---|
| No main-input independent archived output in reviewed exact versions | Any claim that donor B newly predicted a correct unseen result | Locate an upstream same-input output/fixture, keep its original provenance, and compare only after the existing prediction seal. |
| GV one-step/fixed-input request does not map to the reviewed public sfdp path; A is missing | Numerical main-row comparison and A↔B material-effect denominator | Obtain an official instrumented trace or declare a separately preregistered private API experiment; do not backfill the existing public row. |
| Purpose reports have older/newer or unspecified versions and no observed donor-induced behavior change | Q1 exact-version user intent and Q7 actual design-action benefit | Ask/read a version-pinned reproduction and a documented before/after choice; current links support explanation and conditional recommendations only. |
