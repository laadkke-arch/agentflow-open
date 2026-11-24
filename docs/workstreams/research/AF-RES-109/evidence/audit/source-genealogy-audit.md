# Post-blind source genealogy and counting audit

## Conclusion

**The proposed count of 17 is defensible as a conservative count of primary-source work/function families.** It should be labelled that way. It is neither an exact bibliography nor a count of independent implementations, mechanisms, successful repairs, or sources proven available in January 2024. Each of the 17 selected anchors is a distinct substantive primary work acquired during the original search; several families intentionally merge other qualifying documents/functions, which reduces the count rather than padding it.

This audit uses the [candidate returns](../../candidates.csv), [sealed acquisition ledger](../search-sources-unadjudicated.jsonl), and both [R1–R3 source/review ledgers](../blind/r1-r3/review.md) and [R4–R6 source/review ledgers](../blind/r4-r6/review.md). Source IDs below identify exact original acquisition rows. The JSON companion supplies a disposition for all 52 rows and the precise post-search corroboration IDs. No new web research, tool-log replay, application test, git operation, or modification to the original/blind ledgers was performed. This is an automated post-blind audit; method and rank identities were allowed.

Search outputs were remotely sealed at `628e33709b0be7a19486f1bfeaef93f42e129394`. The blinded packets, adjudication outputs, and this audit were produced later. The seal is not claimed to contain those later files.

## Count reconciliation

| Quantity | Count |
|---|---:|
| Candidate slots / returned / vacant | 36 / 33 / 3 |
| Distinct returned URLs | 26 |
| Original acquisition rows | 52 |
| Raw true primary-count flags | 37 |
| Raw true flags retained as global carriers | 14 |
| Later substantive original-search rows promoted from false | 3 |
| Raw true flags removed or folded | 23 |
| Recommended conservative global credits | **17** |
| New post-search discovery credits / executed candidate tests | **0 / 0** |

The three promoted rows are `R2-B-S4`, `R3-B-S4`, and `R4-B-S1-R2`. They were already substantive acquisitions inside the original searches. Promoting the correct row of an already encountered work is not a post-search discovery or a second credit. The original flags remain unchanged; these are recommendations for a derived counted view.

## Exact source IDs recommended for credit

One row per family receives one global credit. The carrier is normally the earliest substantive original-search read used by a returned candidate. This timestamp rule is bookkeeping, not evidence that an arm deserves an exclusive discovery win. Per-arm comparisons must retain their own acquisition records and apply a separate declared deduplication policy.

| Family | Count-credit source ID | Why one credit is appropriate |
|---|---|---|
| F01: Node-RED flow editing | `R2-B-S1` | Four acquisitions repeat the same UI guide; PUT flow is a separate document and configuration path, conservatively folded into the same flow-editing family. |
| F02: Microsoft menu naming guidance | `R1-B-S2` | First-party Windows design guidance contains the operative task-label and object-property convention. |
| F03: Chrome CSS diagnostics | `R2-A-S3` | First-party documentation describes its own resolved-style diagnostic facility. |
| F04: W3C 2015 tab-panel guidance | `R2-B-S4` | The original substantive section read is S4. S2 exposes status/contents only and S3 repeats an incomplete opening segment. |
| F05: Node-RED credential representation | `R3-A-S1` | Both arms read the same official editor/runtime credential contract despite different original_work_id strings. |
| F06: Vault partial secret update | `R3-A-S2` | Official documentation describes Vault own partial-update and read-modify-write behavior. |
| F07: Auxx secret lifecycle implementation | `R3-B-S3` | A first-party engineering account describes its own mask filtering and nested preserving merge; this is not a generic tutorial paraphrasing another protocol. |
| F08: Vendure secret-field contract | `R3-B-S4` | Original S2 read only identity/version; S4 read create/update placeholder semantics and must carry the one credit. |
| F09: CSS UI pointer-events guidance | `R4-B-S1-R2` | Both arms eventually read section 6.2; earlier metadata/anchor acquisitions do not substantiate hit-testing. The earliest qualifying original body read is R4-B-S1-R2. |
| F10: React Flow interaction APIs and classes | `R4-B-S2` | Selection/deletion controls, utility classes and component interaction props are intentionally merged into one broad product-function family; the unpkg mirror is excluded. |
| F11: React Flow connection handles and insertion | `R5-A-S1` | Repeated handles guide and separate addEdge insertion validation are folded into one connection family. Failed hook-detail fetch contributes zero. |
| F12: ELK port sizing and spacing | `R5-A-S5` | The returned candidate rests on node-size options. Spacing and layered-algorithm pages are substantive nonfinal support, folded in without extra count. |
| F13: yFiles parallel-edge router | `R5-B-S2` | The vendor API and first-party source demo describe the same router. Trigger/scope behavior in the demo adds detail, not a second router. |
| F14: Chromium touchpad encoder | `R6-B-S5` | Two revisions share the same file/function genealogy. The first qualifying original read is R6-B-S5; commit metadata is supporting and the failed change fetch is uncredited. |
| F15: D3 zoom component | `R6-A-S2` | Official component reference gives filter-versus-listener-removal and wheel scaling behavior. |
| F16: Chrome passive-wheel intervention | `R6-A-S3` | First-party browser policy article documents Chrome own root-listener passivity change. |
| F17: Chromium PDF gesture adapter | `R6-B-S3` | Official source implements a separate consumer-side adapter with scaling, accumulation and gesture lifecycle. |

## Transfer credit away from incomplete first reads

| Initial acquisition | Later substantive original-search read | Treatment |
|---|---|---|
| `R2-B-S2` | `R2-B-S4` | Metadata/status to tab-panel body. Receives the global family credit. |
| `R3-B-S2` | `R3-B-S4` | Header/version to secret update/create body. Receives the global family credit. |
| `R4-A-S01` | `R4-A-S04` | CSS metadata to section 6.2 body. Retains substantive evidence; global credit remains with `R4-B-S1-R2`. |
| `R4-B-S1` | `R4-B-S1-R2` | CSS metadata and unsuccessful anchor to section 6.2 body. Receives the global family credit. |
| `R4-B-S3` | `R4-B-S3-R1` | Incomplete target range to interaction/keyboard rows. Retains substantive evidence; global credit remains with `R4-B-S2`. |
| `R6-B-S1` | `R6-B-S4` | Incomplete target range to interaction/keyboard rows. Retains substantive evidence; global credit remains with `R4-B-S2`. |

`R2-B-S3` and `R4-B-S1-R1` also repeated incomplete opening segments. They do not independently substantiate the requested operative section. `R4-B-S3` did read a drag threshold, so it is not empty metadata; it still did not substantiate its final interaction/keyboard claim until the later read. The same qualification applies to the initial R6 component-page window.

Two potential transfers remain blocked. `R2-B-S5` was a Function-node source identity/line-listing read; `R2-B-S6` claims a subsequent operative section, but the blinded independent body verification failed. Both receive zero under this deliberately conservative gate. This is uncertainty, not a finding that the original read never happened. For the unpkg artifact, `R4-A-S03` is the initial mirrored, tool-rewritten acquisition; later `R4-A-S05/S06` expose useful code excerpts but do not repair the original provenance or add independent source origins.

## Duplicates, exclusions, and support-only rows

| Original source IDs | Recommended treatment |
|---|---|---|
| `R1-A-S3` | Exclude: original i18next acquisition explicitly labelled a tool-rewritten summary. Later clean direct verification cannot backfill original primary-discovery status. |
| `R1-A-S2`, `R1-B-S3` | Nonfinal Node-RED node-authoring i18n background. Substantive first-party documentation, but no additional allotted count and no verified core-menu linkage. |
| `R1-A-S4` | Failed wiki fetch; no direct body. |
| `R2-B-S5`, `R2-B-S6` | Hold the Function-node comparator because independent operative verification failed; no count from source identity alone. |
| `R4-A-S03`, `R4-A-S05`, `R4-A-S06` | Same unpkg distribution, excluded under this audit’s provenance gate; recorded rewritten extraction, integrity and source commit not established. This is not a universal claim that every mirror is nonprimary. |
| `R5-A-S3`, `R5-A-S4` | Substantive nonfinal ELK support pages; fold into the returned `R5-A-S5` option family. |
| `R5-B-S3` | Hook detail returned HTTP 404; zero. |
| `R6-B-S2` | Change-body fetch timed out; zero. |
| `R6-B-S6` | Dates an already counted encoder tree; metadata support only. |
| Every blinded `S*` and `PV-R4R6-*` row | Zero original-search credit, including later successful rereads, historical follow-ups, release notices, failures, input caches and the integrity exception. |

The [JSON disposition list](source-genealogy-audit.json) covers all remaining duplicates explicitly. In particular: the flow UI guide repeats across R1/R2 and both arms; the credential page repeats across R3 arms; CSS draft reads repeat across arms and section acquisitions; React Flow’s component API repeats across R4/R6; the handles guide repeats across R5 arms; the yFiles API and demo share a router; and the two Chromium touchpad source revisions share one encoder. Different `original_work_id` strings or revision hashes do not create extra source origins.

## Why the proposed families are not URL padding

The broadest consolidations must remain visible. Node-RED’s UI guide and PUT API are separate documents and paths; React Flow’s interaction grouping combines utility classes, component props and explicit deletion; its connection grouping combines handle placement with addEdge insertion validation; yFiles combines an API reference and a source demo. These are not exact single-document identities. Counting one per family is a conservative policy, and should not be described as proof that the grouped functions are identical.

The remaining anchors are genuine first-party origins of the material being used: Microsoft’s own platform convention; W3C’s authored specification/guidance; Chrome’s diagnostic tool and separate browser intervention; Node-RED, Vault, Vendure, React Flow and ELK product contracts; Auxx’s account of its own implementation; yFiles’s own router; and D3/Chromium components. Auxx is distinguishable from a generic tutorial that merely paraphrases someone else’s protocol, although its source-code excerpts were not independently verified against a repository. Microsoft and W3C are primary guidance works, not independent product implementations.

Separate works can share an underlying mechanism. The secret contracts all concern edit intent and state preservation; the graph references concern placement/routing; the wheel-related references share an event representation. D3, the Chromium producer, the PDF consumer, and the Chrome cancellation policy remain different authored components/contracts, but this audit makes no claim that they are independent inventions or distant-domain transfers. React Flow documentation may expose a product interface around existing mechanisms; without verified dependency evidence it should not be called another independent zoom implementation.

## Current count and historical suitability are separate

| Family | Historical qualification |
|---|---|
| F01: Node-RED flow editing | Historical editions unknown; current primary status does not prove January 2024 wording. |
| F02: Microsoft menu naming guidance | Publisher update date 2022-02-08 supports pre-request guidance; no archived snapshot. |
| F03: Chrome CSS diagnostics | Publisher update date 2022-11-15 UTC supports pre-request guidance; exact historical bytes unverified. |
| F04: W3C 2015 tab-panel guidance | Dated 2015 draft predates the request; non-final status and APG 1.0 inheritance remain explicit. |
| F05: Node-RED credential representation | Undated live page; global-environment and incident-version mapping unknown. |
| F06: Vault partial secret update | Post-search v1.15.x copy and 2023 release notice provide qualified dating support; version navigation conflicts and exact historic wording remain unresolved. |
| F07: Auxx secret lifecycle implementation | Article dated 2026-08-18, after R3; prior mechanism availability unknown. |
| F08: Vendure secret-field contract | Inspected revision edited 2026-07-31; original publication and pre-request mechanism availability unknown. |
| F09: CSS UI pointer-events guidance | Current edition dated 2026-01-20; 2021 negative text search does not prove historical browser non-support. |
| F10: React Flow interaction APIs and classes | Live APIs are not historically pinned. Excluded @xyflow/react 12.4.2 artifact cannot establish January 2024 implementation. |
| F11: React Flow connection handles and insertion | Current next/live pages do not establish 2024 behavior. |
| F12: ELK port sizing and spacing | No dated historical edition established. |
| F13: yFiles parallel-edge router | Java versions and a site footer do not establish exact article/API availability at the request date. |
| F14: Chromium touchpad encoder | Original S6 dates one tree in 2018; later verification independently dates the other revision to June 2018. Failed metadata retries do not negate recorded reads or prove target-browser deployment. |
| F15: D3 zoom component | Live page/package edition not historically established. |
| F16: Chrome passive-wheel intervention | Displayed update date 2019-02-07 UTC predates R6; exact historical text and application listener options unknown. |
| F17: Chromium PDF gesture adapter | Pinned code revision but metadata fetch failed; exact pre-request availability unknown. |

Postdated Auxx, Vendure and CSS editions can contribute to a present-day first-party source count, while failing to establish availability of that edition in 2024. A later versioned Vault page and release announcement are qualified dating support only, not new search discoveries. An unsuccessful historical lookup does not establish that a feature was absent; a copyright year does not date a particular revision. No aggregate “17 historically available sources” is supported.

## R6 integrity qualification

The R4–R6 review records unintended original-discussion exposure at **2026-11-24 02:29:49 UTC**. The original search acquisitions were earlier and sealed, and the candidate rereads have earlier timestamps. This does not retroactively invalidate those original first-party acquisition rows for a descriptive source inventory. It also does not rehabilitate final post-exposure R6 judgments for a strict original-discussion-blind comparison. The discussion/integrity row receives no credit, and source counts must not be presented as blind outcome successes.

## Audit limits and preservation

This is an audit of the permitted consolidated records and blinded ledgers, not an independent replay of every raw tool response. The R4–R6 portion received a separate read-only agent cross-check, which agreed on all nine proposed carrier IDs in that subset and the need for incomplete-read transfers. No human review is asserted.

The recommended view contains exactly 17 count carriers and a complete disposition for all 52 original acquisition rows. All original candidate/source files and both blinded source/review ledgers were hash-checked unchanged while writing only `source-genealogy-audit.md` and `source-genealogy-audit.json`. The sealed blinded judgments and their other artifacts were not edited.
