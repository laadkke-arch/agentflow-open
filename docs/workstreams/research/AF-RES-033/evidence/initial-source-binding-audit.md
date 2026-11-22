# AF-RES-033 initial-source binding audit

Audit completed: 2026-11-22T16:53:26.655882Z. Auditor: `protocol_audit`.

## Decision and scope

**All eight specified text snapshots and the R04 attached image pass the metadata and byte-binding audit. No opening-head, path, blob, or local-byte mismatch was found.** This accepts these exact objects as snapshots at the head recorded by each archived opening event. It does not certify semantic interpretation, selection-prefix completeness, or first-authored-draft status. The subsequently requested prefix closure remains a separate task.

The requested set is Rust RFC PRs 2843, 2845, 2850, 2856 and Kubernetes enhancement PRs 1438, 1439, 1444, 1450. The auditor read collection code, frame/inspection/restoration metadata, projected archive records, and immutable Git metadata. Local source bytes were consumed only by hashing code. No proposal body, title, image content, query, ranking, or outcome was displayed to or interpreted by the auditor. No recipient files or earlier sealed evidence were edited by the auditor, and no commits were made.

## Exact source checks

| Source | Archived opening head prefix | Verified blob prefix | Raw bytes | Result |
|---|---|---|---:|---|
| rust-lang/rfcs #2843 | `d5fe87812fc9` | `07421f19c9c4` | 3,143 | Pass |
| rust-lang/rfcs #2845 | `6fb5bd5a6132` | `4da40976887a` | 18,688 | Pass |
| rust-lang/rfcs #2850 | `5559913ccacb` | `4489ee9aa89b` | 42,931 | Pass |
| rust-lang/rfcs #2856 | `c80e28415d8a` | `0a4146ed6f7b` | 16,868 | Pass |
| kubernetes/enhancements #1438 | `6d97b64e5985` | `f8fcdd406b7a` | 21,513 | Pass |
| kubernetes/enhancements #1439 | `50f8b89cb8f0` | `1228c1feb8f5` | 18,582 | Pass |
| kubernetes/enhancements #1444 | `63f35ac4f5d3` | `ffce7d79fc03` | 13,878 | Pass |
| kubernetes/enhancements #1450 | `2cef2aacc292` | `8aff1a2d878a` | 3,133 | Pass |

Full commit, base, tree, path, blob, and SHA256 values are in [initial-source-binding-checks.json](initial-source-binding-checks.json). Each source record pins its opening-event projection row and canonical hash, the **inspection preceding restoration**, the restoration row, tree/path trace, and raw-byte results. Selected receipt rows have canonical hashes independent of later ledger appends.

The three legacy Rust restorations (2843, 2845, 2850) used retained-history opening-head candidates. Their snapshot commit SHAs exactly match the historical opening events in [opening-archive-checks.jsonl](opening-archive-checks.jsonl). The event evidence corroborates these particular reconstructed heads; this does not validate the reconstruction rule for every PR. The other five use [archive-recovery-checks.jsonl](archive-recovery-checks.jsonl). Every source has one matching `PullRequestEvent` with `action=opened`, matching repository/number and PR creation time, and a completely streamed and hashed hourly archive.

For every source, the audit checked the immutable head against Git commit metadata, resolved the full repository path through nonrecursive trees, independently reconstructed each Git tree object hash, and recomputed the local raw blob hash with `SHA1("blob " + decimal_byte_length + NUL + raw_bytes)`. All eight raw SHA256 values, byte lengths, and separately recorded LF-canonical hashes match their restoration receipts; all eight have zero CRLF sequences. Git commit objects themselves were **not** reconstructed and rehashed because commit messages were deliberately omitted. Head-to-tree association relies on the immutable GitHub metadata response and its recorded identity; tree and blob hashes were independently verified.

The initial pass found missing transport-cache copies for the legacy Rust commit/tree chains and image resources subtree. These were evidence-cache gaps, not unequal bytes. Ten successful immutable public Git metadata requests resolved them: three commit objects, six legacy Rust tree objects, and one resources tree. The checks file preserves URLs, timestamps, HTTP status, response hashes, allowed projections, and original gap records. An initial SHA/tree connectivity probe is disclosed separately. Unfiltered responses were neither persisted nor displayed. Recipient caches were not changed.

## Archived comparison and collector guards

| Archive-restored source | Changed files | Comparison commits | Complete commit metadata |
|---|---:|---:|---|
| rust-lang/rfcs #2856 | 2 | 1 | Yes |
| kubernetes/enhancements #1438 | 1 | 13 | Yes |
| kubernetes/enhancements #1439 | 1 | 1 | Yes |
| kubernetes/enhancements #1444 | 1 | 1 | Yes |
| kubernetes/enhancements #1450 | 1 | 1 | Yes |

Each immutable GitHub `base...head` comparison has the archived event base, its last returned commit equals the event head, and its selected path/blob agrees with the verified head tree. All five commit lists are complete and every selected proposal path is recorded as added. No selected comparison approaches the 300-file cap. The collector fails structural eligibility at 300 or more files. GitHub documents that paginated comparison files occur on the first page and are limited to 300: [official compare-commits documentation](https://docs.github.com/en/rest/commits/commits#compare-two-commits).

The final reviewed `archive_collect.py` SHA256 is `8f7bc728f5d08221ac17b3a36fd5153f9bedda008ad4c0ae65037fbaa0c90e66`. Its binding guard verifies the unique copied event, repository/PR/creation identity, immutable head/base syntax, expected evidence ledger, canonical projection-row hash, one complete matching event, and copied versus projected head/base/archive identity. Inspection resolves added or renamed proposal paths at the archived head. Restoration requires the archived head and a prior inspected path/blob, recomputes the raw Git blob hash, and refuses unequal existing bytes. Each selected inspection predates restoration and embeds the exact same archive binding as its restoration and current copied binding.

**Resolved guard gap:** the first reviewed version matched a prior inspection on repository/PR/head/path/blob/flags without requiring its embedded archive binding to equal the current binding. A stale inspection with the same head/path/blob but another base/projection could qualify. The parent added explicit `entry.get("archive_binding") == event` during this audit; the final code was rechecked and both version hashes are recorded. All five actual prior inspections and restorations already had exact binding equality, so source recollection was unnecessary. This review does not imply that the final code version executed every earlier restoration.

## R04 attached image

`resources/project-group-workflow.png` is bound to opening head `c80e28415d8a7f94448661badb963d3d6fc9efb2`. Its archived comparison entry, root/resources tree path, and local bytes agree:

- Git blob: `746510e3400034ec447957e183d513a340f20948`.
- Raw SHA256: `89e85208a67739bb872da3d1be76d1a41a3255de7b7591d0ce5c3593ef25dee1`.
- Size: 93,361 bytes.

The image was not displayed or visually interpreted. The audit verifies this specified image object, without deciding its semantic role or completeness of all possible linked attachments.

## Evidentiary limits

| Claim | Audit disposition |
|---|---|
| Selected SHA equals the archived opening-event head | Established for all eight within the GH Archive event record's provenance. |
| Exact path/blob belongs to that head tree | Established for all eight text snapshots and R04 image. |
| Local raw bytes equal the expected Git blob and restoration SHA256 | Established for all eight text snapshots and R04 image. |
| Copied archive binding equals the independently projected event | Established for all five archive restorations; legacy Rust3 are separately joined to matching archived heads. |
| Full-source semantic interpretation, eligibility, or whole/partial scope | Not audited. |
| Earliest eligible sampling prefix is complete | Not decided by this source-object audit. |
| Snapshot is the first draft ever authored; first comparison commit first introduced the proposal | Not proved. An opening head can contain multiple pre-opening commits. |
| Subsequent revisions, reception, adoption, merger, or closure | Outside scope and not read. |
