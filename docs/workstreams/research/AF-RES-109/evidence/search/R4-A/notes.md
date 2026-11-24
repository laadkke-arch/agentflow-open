# R4-A: selection-handle search arm

## Input and baseline

The supplied request, posted 2024-01-01T08:21:31Z, asks for a selection region analogous to a drag handle so that overlapping node bodies can be clicked through while nodes remain deletable. The opening post's original edition is not established. Its assigned input hash is `58e5a6870b870326fb391c173f025aba11d74708a0549ac8dfbfe32e1c09be1d`; this hash was supplied, not independently recomputed.

The author already reports a working click-through and dragging combination using `selectable=false` with a drag handle, but reports losing deletion through selection. That implementation is the baseline, not a new finding. An alternative absent from this text is not proved unknown to the author.

Only the assigned prompt was read locally. No other request, repository instructions, HANDOFF, sibling result, original issue page, issue comments, status, linked PR, or identified later resolution was inspected. No delegation or git operation occurred.

## Actual strategy

Method A used three adaptive English searches, all through `system2_search_query`:

1. `React Flow node pointerEvents node.style NodeWrapper` — look for the implementation boundary between node selection and pointer targeting.
2. `site:w3.org/TR/css-ui-4 pointer-events none auto descendants hit-testing` — verify the browser-level targeting and propagation rule in its primary specification.
3. `site:reactflow.dev/api-reference deleteElements nodes selected deletable` — test whether selection-dependent keyboard deletion is the only documented deletion path.

The six explicit reads were three opens followed by three finds. Finds and revisits counted against the same limit. They covered three distinct works: a W3C draft, the official DeleteElements reference, and a versioned xyflow package artifact hosted by UNPKG. Repeated sections of the same artifact do not count as new primary works.

All 49 search results appear in `events.jsonl` in displayed order: 20, 17 and 12 results respectively. Each top five is preserved without re-ranking, and none has a missing rank. Result titles, URLs and references are exact returned metadata; seen-content descriptions are paraphrases. One malformed multiline search title is preserved literally as metadata.

## Returned choices and proposed tests

| Test | Evidence and decision | Minimal discriminating check | Status |
|---|---|---|---|
| R4-A-T1 | [CSS pointer-events](https://www.w3.org/TR/css-ui-4/) supports a pointer-transparent outer box with an active descendant handle. Keep selection eligibility available. | Overlap A above B; set A's wrapper to none and handle to auto. Body clicks should target B; handle clicks should target the descendant and traverse A's handlers. | Proposed; not executed |
| R4-A-T2 | [DeleteElements](https://reactflow.dev/api-reference/types/delete-elements) offers explicit deletion using IDs, addressing the deletion obstacle while retaining the reported baseline. | Delete unselected, nonselectable, deletable A by ID, with child C and edge A–B. With deletion permitted, inspect removal of A, C and the incident edge, preservation of B, and asynchronous results. | Proposed; not executed |
| R4-A-T3 | [NodeWrapper in @xyflow/react 12.4.2](https://app.unpkg.com/@xyflow/react@12.4.2/files/dist/esm/index.mjs) supplies a version-specific failure check for relying on selection eligibility alone. | Compare draggable, nonselectable A with no override, inner-content pointer exclusion, and wrapper-level node.style exclusion. Inspect the wrapper's actual pointerEvents and event targets. | Proposed; not executed |

The first and third links support a related design/test chain rather than independent fixes. The implementation shows that a draggable node can retain wrapper pointer events even when selection is disabled, and that node.style overrides the default wrapper value. This is evidence about version 12.4.2, not a finding that the author's reported baseline was wrong.

The deletion reference directly documents ID-bearing payloads and related-element cleanup. The package caller passes those payloads into an imported helper, emits removal changes, and returns matching results. The helper itself was not read, so no claim is made that all filtering or veto conditions were verified.

## Version, source and timing limits

The CSS page identifies a 2026-01-20 Working Draft. Earlier versions were linked but not opened; the exact relevant text or browser support on 2024-01-01 remains unknown. The live DeleteElements page did not establish an exact revision or publication date. The package URL fixes version 12.4.2 but its release date, integrity and source commit were not verified. UNPKG is a distribution mirror of authored package code, and the search tool described its extraction as a rewritten summary.

Every web action has actual UTC start/end timestamps and elapsed seconds. Independent opens/finds were batched; event indexes record launch order. Initial prompt loading, local inspection of already-returned session data, and report writing are outside retrieval timing. The parent model label supplied to this arm was GPT-6 Astra Pro; an immutable backend identifier was not exposed. Automatic engine reads, tokens and monetary costs are unknown, never assumed zero.

## Unintended exposure

The first search automatically exposed secondary analysis, two product-news snippets and a version-13 migration snippet. The third automatically exposed product-news/release snippets, a version-12 migration snippet, and an unrelated change number 4957. None of those pages was opened.

The W3C query exposed an unrelated CSSWG issue archive about iframe hit testing. A returned code window exposed an unrelated xyflow issue 4779 about batching. Neither issue was opened. Documentation navigation and surrounding returned sections were also automatically visible. No identified source-issue comment, status, linked PR or later resolution was encountered.

## Unfilled requirements and what was not tested

The input does not specify dependency or browser versions, the full node DOM/CSS, whether deletion must use the existing keyboard shortcut, or the intended interaction with keyboard focus and multi-selection. These remain unknown rather than added requirements.

No React Flow instance, browser interaction, drag, keyboard deletion, selection event, touch input, stacking change or accessibility behavior was executed. The CSS specification's qualifications about focus navigation, text selection and unspecified hit-test corners remain relevant. Neither software installation nor implementation changes were made. Only report structure and assigned research counts are checked locally.

All source summaries are paraphrased. No third-party page bodies are copied into the deliverables; raw responses remain only in session storage. Q3–Q6 are retained as requested question labels because the assignment supplied no definitions.
