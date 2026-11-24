# Blinded technical adjudication: R4–R6

## Status and limits

**All 18 proposed variants in the 16 packet groups have been adjudicated, and all candidate URLs were reopened. No candidate code, browser interaction, hardware gesture or application test was executed.** The resulting expectations are documentation- or source-derived predictions. This is an AI technical review, not human review.

**Integrity exception:** at **2026-11-24T02:29:49Z**, a post-search query intended to locate official source code unexpectedly returned the original R6 issue discussion, including repair information. The issue page was not opened, but the search-result exposure compromised original-discussion blindness. All final judgments were serialized at 2026-11-24T02:39:39Z, after that exposure; no final R6 adjudication is claimed to predate it. R6 candidate-source observations were made before exposure. Method and rank identities remained masked throughout. R4/R5 original-discussion blindness remained intact. See `PV-R4R6-26`; it is excluded from every judgment’s support list. R6 rows are provisional and explicitly ineligible for a strict original-discussion-blind comparison.

The only pre-existing local files read were the permitted packet and its three natural-input caches. Search outputs were remotely sealed at `628e33709b0be7a19486f1bfeaef93f42e129394`. The blinded packet was generated afterward from those sealed outputs; this SHA is not a claim that the packet existed at the seal. Issue creation times were supplied by the parent from sealed records: R4 2024-01-01T08:21:31Z; R5 2024-01-01T19:31:01Z; R6 2024-01-02T06:25:26Z. These dates do not authenticate the original body editions.

## Decision semantics

- **yes** means the cited mechanism supports that condition within the explicitly stated scope. It is not a runtime-success claim. For R5, a valid external reference can meet the request even without a React Flow adapter.
- **partial** means a relevant operative mechanism exists, with a missing integration step, conditional premise or narrower scope. **no** means the proposed mechanism does not provide that condition; **unknown** means the available evidence cannot determine it.
- Implementation/test flags identify new choices relative to the supplied baseline. They do not measure author ignorance, novelty to the field or experimental success. A concrete near-miss alternative can receive an implementation flag while still failing part of the request.
- Test credit requires an intervention, contrast or observed variable beyond the original reproduction. Repeating Windows pinch with `zoomOnPinch=true`, repeating the reported drag handle, or merely asking whether edges overlap earns no credit by itself.
- Deduplicate by `choice_key` and `test_key`. Raw flags are not distinct-source or distinct-mechanism counts. Every source row has `counts_as_unique_primary:false` and `count_category:post_search_verification`.

## Variant decisions

| Variant | Operative decision or discriminator | Condition 1 | Condition 2 | New implementation | New test |
|---|---|---|---|---:|---:|
| D13-V1 | Drag/selection and stacking diagnostic | no | partial | 0 | 1 |
| D14-V1 | Spatial wrapper/child targeting | yes | partial | 1 | 1 |
| D14-V2 | Same spatial targeting, handle variant | yes | partial | 1 | 1 |
| D15-V1 | Explicit deletion; selection absent | yes | partial | 1 | 1 |
| D16-V1 | Wrapper-versus-inner failure check | partial | no | 0 | 1 |
| D17-V1 | Suppression is not click-through | no | no | 0 | 1 |
| D18-V1 | Missing data versus overlapping geometry | partial | no | 0 | 1 |
| D19-V1 | ELK endpoint-gap/crowding policy | partial | partial | 1 | 1 |
| D20-V1 | Reroute the affected peer group | yes | yes | 1 | 1 |
| D21-V1 | Master path and adaptive/fixed gaps | yes | yes | 1 | 1 |
| D22-V1 | Count-based attachment coordinates | yes | partial | 1 | 1 |
| D22-V2 | Same attachment policy, fan-out fixture | yes | partial | 1 | 1 |
| D23-V1 † | Keep listener, filter events | partial | partial | 1 | 1 |
| D24-V1 † | Modifier routing and first update | partial | partial | 1 | 1 |
| D25-V1 † | Activation shortcut ablation | unknown | yes | 0 | 1 |
| D26-V1 † | Wheel-to-pinch lifecycle adapter | partial | partial | 1 | 1 |
| D27-V1 † | Same encoder/routing family | partial | partial | 1 | 1 |
| D28-V1 † | Cancellation-premise diagnostic | partial | partial | 0 | 1 |

† R6 rows are excluded from strict original-discussion-blind comparisons. All tests in the table are proposed and unexecuted.

## R4: spatial selection versus suppression

The strongest spatial design is D14: preserve eligibility and restrict browser targeting to an enabled child. Its two variants are one choice. D16 adds direct placement evidence from a published wrapper implementation, but its standalone exclusion fixture lacks an enabled handle and still disables selection; it receives test-only credit. The concrete failure is exclusion on the wrong DOM layer or inheritance into the required control. [CSS section 6.2](https://www.w3.org/TR/css-ui-4/#pointer-events-control), `PV-R4R6-02`; [NodeWrapper artifact](https://app.unpkg.com/@xyflow/react@12.4.2/files/dist/esm/index.mjs), `PV-R4R6-04`.

D15 is a useful purpose-level alternative: delete by identity while retaining the reported configuration. It does not provide the requested selection handle. D17 is a strong near miss as a solution: suppressing a front-node action does not demonstrate that the rear node received the event. D13 contributes a causal diagnostic for drag selection and later overlap order, with selectability made explicit. The minimal next observation is actual target/selected-ID/movement data from one integrated overlap fixture.

## R5: endpoint placement versus entire-path routing

The original image could not be retrieved (`DisabledError`, `PV-R4R6-22`). Therefore general fan-out and repeated same-pair edges remain separate interpretations. D22 provides the most direct React Flow endpoint recipe, but its count arithmetic is application policy; its two variants share one choice and test family. D19 supplies a different port-layout policy with a crowding tradeoff. Neither establishes non-overlap along complete curves. [Handles guide](https://next.reactflow.dev/learn/customization/handles), `PV-R4R6-10`; [ELK options](https://eclipse.dev/elk/reference/options/org-eclipse-elk-nodeSize-options.html), `PV-R4R6-07`.

D20 and D21 concern one yFiles router, with distinct choices about recomputation scope and geometric constraints. They meet the same-pair interpretation as references; they do not establish arbitrary fan-out or a React Flow integration. D18 is the strong near miss: successful insertion is necessary for rendering but does not create spacing. The first useful observation is whether the data contains every intended edge, followed by measured endpoint coordinates or peer-path gaps for the relevant topology. [Router API](https://docs.yworks.com/yfiles/doc/api/y/layout/ParallelEdgeLayouter.html), `PV-R4R6-09`; [demo](https://kb.yworks.com/article/313/Routing-multiple-edges-between-two-nodes-in-a-parallel-fashion), `PV-R4R6-08`.

## R6: input evidence, routing and cancellation remain distinct

The provisional source-based proposals distinguish selective listener retention (D23), event routing (D24/D27), and lifecycle normalization (D26). D24/D27 are revisions of the same encoder, not independent mechanisms. The PDF adapter and D3 consumer are separate components operating on a related representation. Neither representation nor modifier value uniquely proves the physical input. All Windows/application transfer remains unexecuted.

D25 and D28 are useful ablations but weak repair claims. Changing the shortcut may leave behavior unchanged. Cancelling a browser default does not itself repair application panning. D28 is the strongest near miss: its actual listener/passivity premise has not been established. The minimal next observation is the first physical event, its modifiers/key history/cancelability, and resulting scale plus translation with ordinary panning retained. No original-discussion hint is credited as a repair or success. [D3 reference](https://d3js.org/d3-zoom), `PV-R4R6-11`; [Chrome cancellation guidance](https://developer.chrome.com/blog/scrolling-intervention-2/), `PV-R4R6-15`.

## Historical availability and retrieval failures

- The cited CSS draft is dated 2026-01-20. An exact `pointer-events` find in the opened 2021 draft returned no match. That limits backdating of the wording; it is not evidence of browser non-support. `PV-R4R6-02/16`.
- The stable React Flow 12 announcement is dated 2024-07-09. The cited 12.4.2 wrapper artifact is not the January 2024 edition. Other live documentation cannot establish historical API behavior. [Official release notice](https://reactflow.dev/whats-new/2024-07-09), `PV-R4R6-17`.
- Chromium revision `297980d7` has official metadata dated June 4, 2018, establishing pre-request source existence. The displayed timezone is absent. Metadata requests for the two other Chromium revisions failed both at the commit root and JSON retry; copyright years were not used as dates. `PV-R4R6-18/19/20`.
- The passive-wheel article displays a 2019-02-07 UTC update date. This supports a pre-request documented policy, while the exact historical text and the reporter application remain unverified. `PV-R4R6-15`.
- The requested next-documentation hook detail returned 404. The parent handles guide still supplies the refresh instruction, but the detailed hook invocation was not verified there. `PV-R4R6-21`.

## Counts and genealogy

16 request-specific URL groups contain 15 distinct candidate URLs and 14 candidate original-work identities under this ledger’s grouping. They reduce to 11 mechanism families. The 12 raw implementation flags reduce to 9 distinct choice keys; 18 raw proposed-test flags reduce to 15 test keys. These counts include the provisional R6 judgments and are descriptive, not valid blind-comparison successes. R4/R5 alone contain 8 raw implementation flags (6 distinct choices) and 12 proposed-test flags (10 distinct tests). Executed candidate experiments and added search discoveries credited by this review are both **zero**.

`lineages.json` preserves product, component, function, source-work and principle relationships. Different vendors or abstraction layers do not establish distant-domain transfer: these candidates remain in web interaction or graph layout. In particular, the same React Flow API URL supports different R4/R6 diagnostics; yFiles documentation and demo share a router; Chromium encoder revisions share a function; CSS targeting and its React Flow wrapper integration are complementary evidence, not two independent principles.

## Deliverable integrity

`judgments.jsonl` contains all 18 variant IDs exactly once. `sources.jsonl` records 26 source/input/failure/integrity entries with UTC observation times, sections, limits and questions; summaries are at most 160 words and no quoted page passages are reproduced. `lineages.json` records deduplication and scope. No git commands or commits were performed. Serialized coverage and field checks were run only on these evidence files; they are not candidate or application tests.
