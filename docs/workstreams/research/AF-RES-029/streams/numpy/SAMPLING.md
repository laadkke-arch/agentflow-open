# NumPy sampling freeze

Method: AF-RES-029 prospective scope v1, remote method seal `132a0d71f9e82c223378e8df104e646e109c4b39`.

Canonical design-event identifiers are `NEP-<un-padded decimal number>`, e.g. `NEP-49`. A proposal PR and the same numbered NEP are one event. This identifier choice was confirmed by the integrator before computing sampling hashes.

Periods are exactly `2021-2022` and `2023-2024`. Within each period, sort ascending hexadecimal SHA-256 of UTF-8 `AF-RES-029|v1|numpy|<period>|<canonical-id>`; use the canonical ID to break a tie. Read in this order, retain one whole-design request and one partial-design request per period, and preserve exclusions or quota-full traversal. Full request boundaries and independently useful partial operations are determined from first text. Eventual status and implementation do not enter eligibility, order, or classification.

Frame discovery uses the official NumPy NEP source directory plus complete GitHub title metadata for `repo:numpy/numpy is:pr NEP in:title created:2021-01-01..2024-12-31` (101 results; two pages; incomplete_results=false). This second census retains status/editorial/implementation followups as excluded metadata rows and catches proposal PRs that may not have produced a numbered document. The current source directory has numbered NEPs through 58; current body metadata is only a cross-check, never first-public-date proof. NEP 33 and 39 are absent from the observed directory. No claim is made to cover an unnumbered proposal PR whose title omits NEP and has no representation in the directory.

First public dates use first-proposal PR creation, unless an earlier public discussion is actually recovered. Author-created header dates and commit author timestamps alone do not prove public availability. Recover the initial PR commit and immutable blob. A merged or rebased first-on-main version with later commit time is not automatically the first text. Log unresolved force-push history or recovery gaps.

## Exposure before selection

- A discovery-only web search (`site.numpy.org/neps NEP index 2021 2022 2023 2024`, system2, 2026-11-22) returned unrelated educational-panel results, the official Deferred and Superseded NEPs index including NEP 47, and official NumPy news. Its displayed snippets exposed NEP 47 status and NumPy 1.22.0 implementation facts, including array API, CuPy/JAX, DLPack, datatype/ufunc work, and configurable allocator. The full first response was not saved to a file; the conversation tool receipt is the remaining raw record. This is a receipt gap and accidental candidate/status exposure, not an experimental search, provider search, or evidence.
- Complete PR title enumeration necessarily exposed later status titles, e.g. accept/final/accepted/superseded, and implementation-followup titles. Metadata is retained in raw/pr-search-*.json and the exclusion ledger. These words do not affect the hash order or selection.
- Oldest-file commit metadata can contain squash summaries describing review changes or named families. Such summaries are recovery metadata, not frozen question content. Later history messages other than the oldest entry are stored but not presented for model reading.
- Current bodies were downloaded solely to extract title, Created and Type headers programmatically; their remaining bodies and status fields were not used for question predicates. First text will be read separately from immutable selected versions.

No supplier searches, common-start retrievals, or A/B route execution occur in this stream.

## Selected requests and first-text recovery

| ID | Event | Period | Boundary | Immutable initial commit |
| --- | --- | --- | --- | --- |
| Q09 | NEP-50 | 2021-2022 | Partial: value-independent dtype promotion | `ff5e9b79b1f94e0b438c459f630e505610382670` |
| Q10 | NEP-47 | 2021-2022 | Whole: portable standardized array namespace | `0f2b4b235eb580590eaa744bf015d51e2e675afc` |
| Q11 | NEP-55 | 2023-2024 | Whole: variable-width UTF-8 datatype subsystem | `1c013e78112a94e7a2975212df2304606b0d1d1c` |
| Q12 | NEP-53 | 2023-2024 | Partial: compile-time NumPy API target selection | `bf0835ac5d7a7301f05706ae0d5adce191d43ec2` |

The hashes are in `frame-frozen-order.jsonl`; final eligibility/classification is in `frame.jsonl`. Every one of the 101 PR metadata rows and its exclusion is in `pr-enumeration-exclusions.jsonl`. Each period's first two eligible events fill both quotas, so later events are retained as quota-filled, without opening their first bodies for an outcome-based substitution. NEP 48 is administrative.

NEP 50's original head was recovered from the **before** link of its first force-push event, rather than the later rebased first-on-main commit. NEP 55's pre-force-push head history yields the first added commit before PR creation and before the following discussion-link edit. NEP 53 originally had a `.md` filename containing reStructuredText; its later `.rst` history is not the initial version. All four stored first-text bytes match the official Git blob SHA-1.

`initial_date` means the earliest verified public first-numbered-NEP PR event. It is not a claim that no related idea had appeared earlier. NEP 47 links a 2020 discussion of the upstream standard; NEP 53 reports a 2023-04-03 planning meeting without linking an immutable meeting design. NEP 50 and NEP 55 have earlier Created/author timestamps. These limits remain explicit in the question/source records; no unpublished-date inference is used.

## Prospective predicate QA

Before any supplier or experimental search, the integrator identified that some drafted mandatory predicates were architecture choices or illustrative examples. `predicate-revisions.jsonl` preserves each original predicate and the revised outcome/branch distinction. NEP 50 overflow conversion choices, NEP 53 compatibility-package/table and descriptor examples, and NEP 55 arena/locking/sidecar-format branches are retained for separate sensitivity. They do not independently determine universal whole/partial completion. Required operational outcomes remain in `whole_must` and `partial_must`.

## Retention and counting

`sources.jsonl` counts exactly four immutable first designs. Metadata, unsuccessful access attempts, current-header cross-checks and recovery pages are not additional originals. Full connector payloads were retained without duplicate connector wrappers. Force-push HTML retains exact relevant raw excerpts plus the full-response hash, omitting unexamined page comments. Current bodies used solely for header extraction were trimmed to exact header projections and response hashes. The first web discovery response has the explicit local receipt gap described above. No private connector routing identifiers are retained.
