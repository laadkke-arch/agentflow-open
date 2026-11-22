# Go sampling provenance

Sampling-only worker. Actual shell reads of `AGENTS.md` and the prospectively committed `SCOPE.md` on branch `work/research-af-res-029`, observed HEAD `182cca417b2a4ccb2dc96d78dfe10ac3fbb043f5`, on 2026-11-22 UTC. No branch change or commit by this worker.

The finite frame is the official `golang/go` issue ledger, current `Proposal` label, created in 2021–2024. GitHub REST search API is accessed through the GitHub connector, not via local network. Annual queries are paginated at 100 results, creation ascending. Selection is subsequently ordered by the prescribed SHA-256 key. Current label membership is an ascertainment limitation: historical removed labels are not reconstructed.

API responses include fields beyond sampling metadata. The worker programmatically extracts only title, creation timestamp, canonical issue identifier and URL for the frame before traversal. Saved raw responses, if present, are explicitly uninspected and must not be interpreted as first-version evidence. Acceptance labels, status and later comments are not displayed or used for selection.

No supplier search, common-start search, route execution or outcome reading is authorized for this worker. Initial-version recoverability is an eligibility condition, with excluded attempts retained. Current issue body alone cannot establish its unedited initial version.

## Completed sample and stopping points

The frozen frame has 2,841 distinct issues: 509 in 2021, 694 in 2022, 861 in 2023 and 777 in 2024. All 30 REST pages reported `incomplete_results=false`; no annual query reached GitHub's 1,000-result cap. The two sampling cells therefore contain 1,203 and 1,638 events. `frame.csv` retains every row, query page/order, canonical ID, seed, SHA-256 key and within-period order. `frame-metadata.json.gz` is the original pre-coding metadata snapshot, with its uncompressed hash in `metadata-snapshot-manifest.json`.

The ascending SHA-256 order uses exact UTF-8 `AF-RES-029|v1|go|2021-2022|golang/go#NUMBER` or `AF-RES-029|v1|go|2023-2024|golang/go#NUMBER`; canonical-ID lexical order is the tie-breaker. There were no duplicate canonical IDs. Titles never enter the hash.

The early cell stops at rank 7: Q01 is #56094 (partial destructuring assignment, rank 1); Q02 is #43744 (whole benchmark metadata protocol, rank 7). The late cell stops at rank 18: Q03 is #70887 (partial concurrent-map-write failure handling, rank 3); Q04 is #58584 (whole Go/WebAssembly export/call bridge, rank 18). `traversal.jsonl` records every intervening event, original title where recovered, boundary rationale and decision. A filled partial stratum is not reopened to prefer a later event. No acceptance, supplier search result or later implementation was used.

Whole is coded as a multi-operation subsystem or complete protocol with integration. Q02 spans producer representations, parser/merge validation, propagation, and comparison semantics. Q04 spans compiler declaration, linker/export publication, host argument preparation, shared memory/stack, and invocation. A single language operator is partial even if its proposal is long. The integration worker's boundary clarification was based on these initial operations, not on acceptance outcomes.

## Actual initial-version recovery

The GitHub connector and shell were both used. Connector REST search responses supplied the frame; direct shell HTTPS GETs of GitHub HTML succeeded. GitHub's embedded initial Issue node had `bodyVersion` but omitted `lastEditedAt`. The `lastEditedAt` fields initially observed belonged to comment nodes. That probe did **not** establish an unedited initial issue body, and no sampled first text is justified by it. A brief schema debug exposed comment edit timestamps/keys but no comment body or outcome values.

GHArchive HEAD requests returned HTTP 403. A public ranged GET succeeded with HTTP 206, and the worker streamed/decompressed hourly archives using actual shell Python. Only exact `repo.name == golang/go`, `type == IssuesEvent`, `payload.action == opened`, matching issue number were accepted. All four selected events have `event.created_at == issue.created_at == issue.updated_at` in that original opening payload. Their exact body bytes and SHA-256 hashes, opening event IDs, hourly archive URLs, object generation/ETag and captured original event are retained. Current issue text was not substituted.

GHArchive is a **third-party capture of official GitHub author content**. Native GitHub edit history was not recovered. The local fixed body hash/opening-event ID establish the analyzed version; they do not turn the archive into an official Golang Git blob. Counts treat the GitHub URL, GHArchive capture and local file as one original-content group. Four sampled initial designs are counted, with this capture limitation explicit; other recovered first texts are excluded from the sample count.

For #70897, #58678, #61897 and #59205, the creation-hour and adjacent-hour archives had no matching opened event. A further metadata-only scan required `event.created_at == issue.created_at == issue.updated_at` and an opening/initial label/assignment/milestone action; it also found no qualifying snapshot. No later snapshot was accepted. #61897's initial-event metadata was additionally checked for transfer/conversion, with none displayed. These are recovery failures, not claims that no initial text exists anywhere. Current body links were inspected only as potential first-design provenance; no supplier body was followed.

## Exposure and batch recovery

`exposures.jsonl` distinguishes planned current-title metadata, uninspected broad API fields, schema-probe metadata, official proposal-tree filenames, researcher coding clarification, and extra first-text reads. Batch recovery ran ahead while whole-boundary coding or prior-candidate recovery was unresolved. Early ranks 8–23 and late ranks 19–22 were consequently recovered/read beyond the eventual stopping points. Those 20 extra first-text exposures are preserved and have no sampling weight. They did not replace the rank-7/rank-18 whole events. No target-event outcomes or substantive later comments were read.

`nonselected-initial-captures.jsonl` consolidates exact nonselected first bodies, event IDs and body hashes. Some long nonselected bodies (#51259, #56283) were captured in full but only their first 5,000 decoded characters were displayed. Selected originals were fully displayed/read. `recovery-receipts.jsonl` retains success/failure attempts and original receipt names; nonselected individual capture paths in old receipts were consolidated into the JSONL file. `frame-response-hashes.jsonl` preserves original connector response hashes and public restoration URLs without unrelated full issue collection bodies or account selectors.

## Predicate and query freeze

`questions.jsonl` contains the four caller/input/output/limit records, mandatory whole and partial predicates, section/line references, one falsifying input per predicate, explicit named families/components, independent partial action and residual adapter, same-name/wrong-output distractor, one neutral query and two literal prospective A queries. Syntax preferences and unresolved assumptions are separated from mandatory requirements. Q04's partial action is the concrete native-integer memory-write step, not an unsupported assertion that a memory writer completes the Go-export bridge. Q03 requires the actual detector-to-catchable-signal path; a generic recover helper leaving fatal unchanged fails.

No common-start search, A/B route, supplier evidence body, experiment, acceptance judgment or repository commit was performed by this sampling worker. The root worker owns the input seal and subsequent stages.
