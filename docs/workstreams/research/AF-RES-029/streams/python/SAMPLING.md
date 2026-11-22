# Python sample — AF-RES-029, sampling only

The packet selects **four independent PEP design events: two whole and two partial**, with one of each in each requested period. It stops before common search. No supplier search, provider page, experimental route, or proposal reply was read by this worker.

## Frame and frozen traversal

The official `https://peps.python.org/api/peps.json` response contained 749 metadata rows. Filtering its `Created` field to 2021–2024 produced the preserved preliminary frame of 124 rows: 55 early and 69 late. The raw response is retained; its status/outcome fields were not printed or used for selection. The first-addition audit of the official Git history found PEP 650, whose `Created` field says 2020 but whose public PR and official Post-History say January 2021. That metadata-only supplement produces the final **125-row finite frame: 56 early, 69 late**. PEP 650 sorts at early rank 45, so it cannot alter the selected prefix. The preliminary frame is preserved separately, not overwritten without an audit trail.

Every final row preserves the canonical ID, title, metadata date, period, literal hash input, SHA-256, traversal rank, and decision. Canonical IDs are `pep-####`. Ordering is the ascending SHA-256 of UTF-8 `AF-RES-029|v1|python|<period>|<canonical-id>`, with canonical ID as the tie-break. Full hashes are in `metadata-frame.jsonl`; the actual traversed prefix is in `traversal.jsonl`.

| Period | Rank | Event | Decision | Operational boundary |
|---|---:|---|---|---|
| 2021–2022 | 1 | PEP 667 | Q05, whole | Live namespace views plus execution-context consistency and C interfaces |
| 2021–2022 | 2 | PEP 686 | Q06, partial | Default-codec behavior within existing Python text I/O |
| 2023–2024 | 1 | PEP 727 | Q07, partial | A documentation-metadata constructor and Annotated component |
| 2023–2024 | 2 | PEP 2026 | Excluded | Administrative release-numbering/lifecycle policy, Type Process |
| 2023–2024 | 3 | PEP 778 | Q08, whole | Wheel-format, backend, validation, installation, and removal protocol |

The whole/partial definition was clarified prospectively by the integration worker before any route execution: whole means a multi-operation subsystem or complete protocol including integration; partial means a bounded operation/component in a larger system. A whole document does not by itself make a whole-system request. Classification reasons and partial utility are preserved in every question record. No acceptance or supplier outcome selected these events. Five candidates were traversed; the administrative exclusion did not consume a sample slot.

This is a **finite metadata sampling frame, not a claim of an exhaustive historical universe or a probability sample**. Untraversed rows do not all have independently recovered first-public dates or first-purpose text. The current Created header is a discovery field, not automatically a public date. All four selected events have fixed recovered originals and public-date evidence. Boundary metadata additionally establishes that PEP 702's PR opened on 2022-12-31 and PEPs 764/769 opened in 2024 despite later main copies. PEP 705's index records 2022 initial discussions despite a 2023 PR. Those rows are beyond the chosen prefix. Earlier pre-PEP/private drafts not present in the recovered official history remain unobserved.

## Genuine earliest originals

An unauthenticated GitHub history request failed with HTTP 403 because the shared API core quota was exhausted. Its error and attempts are preserved. Recovery continued through an official bare partial Git clone, outside the authored checkout, and authenticated public PR metadata. The clone is an intermediate and is not a gitlink or deliverable.

The first main-branch added file was **not assumed to be the initial draft**. Each selected PR's branch history was examined for predecessor filenames and renames. The first public date below is the opening of the official public PR; an earlier authoring timestamp is not asserted to be public. The original is the earliest authored blob recoverable in that initial PR history, not a later current page or an assertion that the PR's opening head had that exact older content.

| ID | Canonical event | First public PR date | Frozen earliest commit | Actual original path |
|---|---|---|---|---|
| Q05 | PEP 667 | 2021-08-20, PR 2053 | `b06bbdf9c6ace7ac4b2bcd81c5d60637351ce08a` | `pep-06xx.rst` |
| Q06 | PEP 686 | 2022-03-18, PR 2443 | `72f4666aca21e695fb21a2aaea3b6df81c567a3d` | `pep-0686.rst` |
| Q07 | PEP 727 | 2023-08-28, PR 3310 | `03f6d6ebd28296b82dd50dae3e88678a51442604` | `pep-0755.rst` |
| Q08 | PEP 778 | 2024-05-20, PR 3786 | `78c4086b041db07a2d560884d658e7b3990b5a6d` | `peps/pep-0778.rst` |

Q05's predecessor draft says `PEP: 6xx`; its later numeric draft initially mistypes the header as 677. The official PR lineage maps this design to PEP 667. Q07 initially used 755 and was renamed to 727 in the same PR; it is not the independent later proposal currently numbered 755. Q06's first Created header is a placeholder `XX-Mar-2022`; the PR timestamp supplies the date. These originals are saved byte-for-byte with SHA-256 and Git blob IDs in the question records.

Q08 was first added to main only in July 2025, already marked Deferred. Its linked initial discussion and official PR recover the May 2024 design. The opening Discourse post was version 2, so the revision endpoint was checked rather than treating its current body as initial. The previous/current bodies are identical; that edit changed only the category. Only the opening post and its revision were read, not replies. That discussion is same-event provenance, not a fifth independent original.

## Exposure and first-version differences

Recovery produced material exposures that must remain visible in sensitivity reporting:

- Main-addition bodies for Q05, Q06, and Q07 were initially read while locating originals, before the earlier PR ancestry was recovered. Later numbered copies for Q05/Q07 were also read. These are preserved as recovery intermediates, explicitly excluded from original-source counts. A clean first-text-only reader exposure is not claimed for this worker.
- Q05 is the consequential difference: the earliest draft requires **both `locals()` and `frame.f_locals` to be live views** and specifies `PyEval_Locals(int depth)`. The later numbered/main draft makes `locals()` a snapshot and adds other C-interface details. The frozen predicates and queries use the earliest live-view version. PEP 558 appears only in the later recovery copy and is not first-text knowledge for Q05.
- Q06's first text requires UTF-8 mode to leave the `locale` module unchanged. Its first header and text were not silently updated from the main copy.
- Q07's earliest API is `doc(documentation)` returning a `DocInfo` object. The current index title differs from that first title. Existing interested/adopting libraries explicitly named in the first text are recorded as prior explicit knowledge, not newly discovered targets.
- Q08 exposed the later `Deferred` status in the main-copy header. Its substantive main-copy body was not read. Selection remained determined by the hash prefix, earliest purpose, and recoverability. The earliest LINKS example/prose direction ambiguity is retained as an unresolved limitation.

All four therefore have explicit recovery-exposure flags. Fresh experimental workers should receive only the fixed earliest-original/predicate/query packet, not these later bodies or the raw current index. Do not delete these audit flags or infer that later exposure was an independent human reading.

## Predicates and source counts

`questions.jsonl` contains caller, input, output, operating limits, original named families/components, mandatory whole predicates, inherited partial predicates, first-source line positions and excerpts, a falsifying input for every predicate, independently useful partial next actions, remaining integration, same-name/wrong-subject tests, and the three prospective literal English search strings. There are 27 whole predicates and 12 partial predicates. Optional/deferred requirements and draft ambiguities are separate from mandatory claims. Thin configuration or call adapters may be used, but an adapter that implements the requested core action does not make an unrelated provider a partial solution.

`sources.jsonl` counts exactly **four initial designs**. Current index rows, commit/path metadata, PR metadata, failed requests, later recovery copies, the excluded process proposal, and duplicate discussion provenance are not counted as independent originals. There are zero supplier originals at this sampling stage.

The stored line excerpts are copied from the saved earliest text. Validation recomputes original hashes, checks every source-line range/excerpt, checks every ordering hash, verifies unique IDs and two A queries per question, and checks the four-original count. It does not execute draft pseudocode or claim runtime success.

## Restore and handoff

The raw official index, Git path logs, PR metadata/read projections, first-draft recovery records, error receipts, and the selected texts are under this stream. To reproduce provenance, clone `https://github.com/python/peps.git` into a separate scratch directory; fetch `refs/pull/2053/head`, `refs/pull/2443/head`, `refs/pull/3310/head`, and `refs/pull/3786/head`; then use `git show <fixed-commit>:<actual-original-path>` for the four rows above. The local recovery scripts record the exact extraction logic; no software install or paid API was used.

The integration worker owns the sample seal, commit, common-start searches, route execution, and adjudication. This worker made no branch change or commit and stops after producing this packet. The method seal supplied by the integration worker is `132a0d71f9e82c223378e8df104e646e109c4b39`.
