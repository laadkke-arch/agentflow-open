# Graph transfer mapping after prediction seal

All implementation and output inspection below occurred after `02359364000057f69b00594d8b43571ac72df298`. These are explanation and falsification records. They do not amend `baseline.json` or `a-predictions.json`.

## Citation chain

| Receiver | Explicit record | Classification | What is not established |
|---|---|---|---|
| d3-force 3.0.0 manyBody | [Tagged README, many-body](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/README.md#many-body-forces) names Barnes–Hut and links its Wikipedia article; [manyBody.js 63](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/src/manyBody.js#L63) names the approximation. G011/G020. | Explicit algorithm attribution; secondary link. The connection to the 1986 paper is a mediated provenance route, not a directly cited primary paper in these receiver records. | Who read the paper, when, and which primary-paper section motivated this implementation are **미확인**. Physical terminology does not prove adoption of Newton's force law. |
| Graphviz 14.1.1 sfdp | [Official sfdp page](https://graphviz.org/docs/layouts/sfdp/) names Yifan Hu and *Efficient, High-Quality Force-Directed Graph Drawing*, 2005; root's donor ledger reads that paper's sections 3–4 and bibliography [2] Barnes & Hut. G012, root D013. | Direct receiver-to-Hu citation; mediated Hu-to-Barnes–Hut citation. [Source](https://gitlab.com/graphviz/graphviz/-/blob/a74b50c20fc624f46f72e24f981b261f6e5edf71/lib/sfdpgen/spring_electrical.c#L41-43) also names Barnes–Hutt. | Current landing-page citation alone does not date the historical adoption. The 2005 paper's exact settings and termination rules cannot be assumed to survive in 14.1.1. |

## D3 variables and executable kernel

Read [manyBody.js](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/src/manyBody.js) at the pinned commit, G020. For a noncoincident direct pair outside the minimum clamp and inside the maximum cutoff, let `delta=(x_j-x_i,y_j-y_i)`, `r=||delta||`, `s_j=strengths[j]`, `alpha` the force-call argument. The code adds

`Δv_i = alpha * s_j * delta / r²`.

The vector magnitude is `|alpha*s_j|/r`, **not** an inverse-square magnitude. Negative strengths repel. This is a coordinate-unit velocity increment per abstract force call; the code supplies no gravitational constant, physical mass units, or seconds for this API call. Barnes–Hut's cell hierarchy and far-field aggregation can be transferred while the interaction kernel changes.

| Donor/algorithm concept | Receiver symbol and location | Changed assumption or boundary |
|---|---|---|
| Particle positions and source weights | `nodes[].x/y`, `strengths[node.index]`; initialize 22–27 | Strength may be negative, positive, or mixed. A physical positive-mass model is not an adequate signed-strength contract. |
| Cell aggregate and center | `accumulate`, 29–53; signed `quad.value`; center weighted by `abs(child.value)` | Center uses absolute child aggregate weights; cancellation can erase internal cells. `if (!quad.value) return true` at 56 prunes a zero-sum aggregate even with `theta(0)`. |
| Opening criterion | `w*w/theta2 < l`, 65, where `w=x2-x1`, `l=distance²` | Strict comparison, full square width and aggregate center. It is not a certified relative-error bound. A theta scalar alone is not comparable with Graphviz's half-width/geometric-center criterion. |
| Close-distance singularity | 67–69 and 82–84; `l=sqrt(distanceMin2*l)` | For `r<distanceMin`, denominator becomes `distanceMin*r`, capping magnitude at `|alpha*s_j|/distanceMin`. Jitter modifies zero coordinate differences. |
| Finite range | `l<distanceMax2` at 66; `l>=distanceMax2` at 77 | Equality is excluded. When an aggregate is accepted, cutoff is checked at its center, so a source inside the radius may be omitted. |
| Coincidence | [jiggle.js](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/src/jiggle.js), [lcg.js](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/src/lcg.js) | Seeded pseudorandom perturbation gives a direction. Separate receiver evaluations need not have equal-and-opposite jitter. |
| Time advancement | [simulation.js 39–59](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/src/simulation.js#L39-L59) | `simulation.tick` cools alpha, invokes forces, multiplies velocity by default 0.6, then advances positions. Main D3 cases call the force directly and therefore do none of those additional operations. |

Main hand calculation for `(0,0),(3,4)`, `s=-30`, `alpha=1`: `r²=25`, so increments are `(-3.6,-4.8)` and `(3.6,4.8)`. The exact tagged source produced those values in the researcher's run. `distanceMax=4` excludes both contributions. This confirmation is an auxiliary execution, not an upstream original output.

## Graphviz initialization and public boundary

The relevant exact source is [sfdpinit.c](https://gitlab.com/graphviz/graphviz/-/blob/a74b50c20fc624f46f72e24f981b261f6e5edf71/lib/sfdpgen/sfdpinit.c), G025, and [spring_electrical.c](https://gitlab.com/graphviz/graphviz/-/blob/a74b50c20fc624f46f72e24f981b261f6e5edf71/lib/sfdpgen/spring_electrical.c), G026.

1. `getPos` at 64–82 can copy input positions, and `sfdpLayout` passes the array at 102–104. Reading this function alone would suggest fixed positions could be preserved.
2. `spring_electrical_control_new` at 51–71 sets `random_start=true`, `maxiter=500`, `step=0.1`.
3. Public `tuneControl` at 200–224 warns that only `start=random` is supported. It maps `K`, `repulsiveforce`, `levels`, `quadtree`, and presentation controls; it does not map the graph's `maxiter` attribute to `ctrl.maxiter`.
4. Normal embedding at 567–569 seeds the C random generator and overwrites every initial coordinate when `random_start` is true. Multilevel processing may operate on a coarsened graph first; subsequent prolongation is another change of the proposed input.
5. `spring_electrical_embedding` updates until `step<=0.001` or `iter>=maxiter`, 659–660. Later smoothing, rotation, overlap removal, component packing, spline generation, and final translation alter the delivered coordinates further.

Thus GV-N/B's requested fixed-coordinate one-step measurement has a precise missing public contract. It is not repaired by submitting `pos="0,0"` and `maxiter=1` and calling the final image a one-step observation. The claim is scoped to the reviewed ordinary sfdp path; private instrumentation is possible.

## Graphviz force, movement, approximation, and stopping

For the normal internal path, G026 575–648, define `delta=x_i-x_j`, `r=||delta||`, `C=0.2`, `p` the negative repulsion exponent, and `K` the desired length scale. The executable coefficients are:

`KP = K^(1-p)` and `CRK = C^((2-p)/3)/K`.

Each adjacent edge contributes `-CRK*delta*r`; each source contributes `KP*delta/r^(1-p)` with cropped distance. The net force is normalized if nonzero, then `x_i += step*f_i`. Vertices are updated sequentially, so later vertices see earlier moves. These are graph-drawing displacements, not a Newtonian time integrator. The introductory comment at source line 35 is not used as a substitute for this executable mapping.

| Mechanism | Exact receiver | Qualification against Hu/astronomy |
|---|---|---|
| Repulsive exponent | Automatic `p=-1`, or `-1.8` when `power_law_graph` selects it; multilevel 1134–1138 | Geometry/graph-dependent heuristic, not fixed inverse-square gravitational acceleration. |
| Approximation enabled | Normal path `n>=45`, 550; `bh=0.6`, 41–43 | The two-node main input would not use the tree if privately injected. Large-graph behavior is a separate auxiliary question. |
| Cell selection | [QuadTree.c 73–82](https://gitlab.com/graphviz/graphviz/-/blob/a74b50c20fc624f46f72e24f981b261f6e5edf71/lib/sparse/QuadTree.c#L73-82) | Stored half-width is compared to distance from geometric cell center. Force uses the average point and total weight. Hu's printed condition is `<=theta`; this receiver is strict `<`. |
| Cell construction | QuadTree.c 337–347: bounding width at least `1e-5`, multiplied by `0.52`, unit insertion weight | `bh=.6`, D3 theta `.9`, and Hu theta `1.2` have different definitions and tested contexts. No accuracy ranking follows from their ordering. |
| Minimum distance | [general.h 75](https://gitlab.com/graphviz/graphviz/-/blob/a74b50c20fc624f46f72e24f981b261f6e5edf71/lib/sparse/general.h#L75), [general.c 116–118](https://gitlab.com/graphviz/graphviz/-/blob/a74b50c20fc624f46f72e24f981b261f6e5edf71/lib/sparse/general.c#L116-118) | `MINDIST=1e-15`. A zero numerator remains zero in a privately supplied coincident pair. Public initialization normally removes that specified coincidence by randomization. |
| Adaptive cooling | spring_electrical.c 171–184 | If net-force norm increases or stays equal: step×0.9; if decreased less than 5%: unchanged; otherwise step×1.1. There is no five-success counter in this function. |
| Termination | Normal loop 659–660 | It tests step and iteration count, not the header comment's configuration difference directly. Hu's paper's success counter and `tol*K` do not describe this exact implementation. |

### Private normal-path hand calculation, not executed

With a symmetric two-node adjacency matrix, `dim=2`, `random_start=false`, `maxiter=1`, `p=-1`, `K=1`, `step=.1`, and coordinates `(0,0),(3,4)`, the first node's force is `(2.88,3.84)`. Normalization gives `(.6,.8)`, so it moves to `(.06,.08)`. The second node then evaluates the already updated geometry and moves to `(2.94,3.92)`. This is `GV-AUX-PRIVATE-N`, a post-seal hand calculation. It is not the observed public GV-N result.

Under the same private controls with both positions zero, numerator vectors are zero while denominators are cropped; force and movement remain zero. This is `GV-AUX-PRIVATE-COINCIDENT`, also unexecuted. A compiled internal harness is needed to promote either to a researcher execution; an independent upstream same-input output would still be needed for the task's original-output requirement.
