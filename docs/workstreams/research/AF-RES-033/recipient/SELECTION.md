# AF-RES-033 recipient selection and source record

The final sample contains four Rust RFC proposals and four Kubernetes enhancement proposals. Each is an initial submitted design restored at the exact historical pull-request opening head. The archived head identifies the submitted snapshot; it does not establish the first privately authored draft or first authored commit.

## Selection

The complete annual metadata frame contains 3,415 unique PRs: 638 from rust-lang/rfcs and 2,777 from kubernetes/enhancements, covering 2020–2024. Annual searches were complete and ordered by creation time, with PR number breaking ties. Titles, bodies, closure/merge fields, comments and outcomes were suppressed before metadata inspection.

Per repository, the chronological first four eligible proposals contain both whole and partial designs. No scope-quota replacement was needed. The final method first four and final selected four are identical.

| ID | Repository | PR | Created at UTC | Scope |
|---|---|---:|---|---|
| R01 | rust-lang/rfcs | 2843 | 2020-01-04T13:02:21Z | partial_design |
| R02 | rust-lang/rfcs | 2845 | 2020-01-06T17:22:44Z | partial_design |
| R03 | rust-lang/rfcs | 2850 | 2020-01-13T13:29:48Z | whole_design |
| R04 | rust-lang/rfcs | 2856 | 2020-01-22T14:29:45Z | whole_design |
| R05 | kubernetes/enhancements | 1438 | 2020-01-08T20:43:16Z | partial_design |
| R06 | kubernetes/enhancements | 1439 | 2020-01-08T21:44:36Z | whole_design |
| R07 | kubernetes/enhancements | 1444 | 2020-01-10T12:56:37Z | partial_design |
| R08 | kubernetes/enhancements | 1450 | 2020-01-14T17:06:09Z | partial_design |

The necessary chronological prefix comprises six Rust PRs and seventeen Kubernetes PRs. Fifteen earlier entries contain no added or renamed proposal Markdown in their archived opening base-to-head diff. All fifteen exclusions and all eight selected opening heads are now backed by unique archived opened events. None of the comparison file lists reached the API cap guard.

## Preserved earlier screening

Before archive recovery became available, current-history restoration failures led to additional chronological screening. The ledger preserves 158 distinct inspected PRs, 14 full original reads, and one snapshot restored without reading its body (#1614). The frame has eight selected, 150 excluded from the final sample, and 3,257 not screened. An excluded-from-sample row may still be eligible or unresolved; the separate eligibility column distinguishes these cases.

Rust #2859 and Kubernetes #1478 and #1566 remain eligible provisional reads, but earlier archive-recovered designs placed them beyond the final chronological cutoff. These are archival-recovery displacements, not scope-quota exclusions. Source-based exclusions remain distinct: Rust #2857 is a nonspecific roadmap, Kubernetes #1460 is an unfilled template, and #1543 is a migration/restatement of a pre-existing 2017 design. All are retained with counted_minimum=false.

Current-history-only restoration failures beyond the final cutoff remain unresolved where their initial document was not inspected. A transport failure was never itself treated as design ineligibility. The before-prefix annotated frame and selection record are retained separately.

## Initial conditions and queries

Each of the eight frozen condition packets retains the requested behavior, whole-design conditions, mandatory/preferred/unnecessary predicates, named prior solutions stated in the original, explicit uncertainties, and a fixed partial target whose mandatory predicates must all hold. Predicates include original line spans and exact snapshot hashes.

Only one repository-relative image was referenced by the final eight: the project-group workflow PNG for Rust #2856. It was restored at the exact opening head and visually inspected. Its re-entry arrow differs from the prose step reference; the packet retains that discrepancy without inventing an extra approval gate. Other original ambiguities, including the RFC/team-consensus inconsistency and the instance-configuration draft-year discrepancy, are retained. Mutable external prior-art links were not followed.

A fresh query-author context read only the final eight full originals, that PNG and the frozen source/condition packet. It did not see excluded/provisional sources, selection history, archive history, provider material, outcomes or rankings. The sixteen English S/R queries use the same maximum-80 [a-z0-9]+ token rule. Every S token is present in its own original. R fidelity is documented by source-located input/state/action/output/invariant checks. Integration preserved all authored query strings and hashes unchanged.

## Durable references and timing

`recipient_sources.jsonl` records one row per restored proposal, including the unread snapshot, with immutable opening commit/path URLs, Git blob identity, raw and canonical-LF hashes, retrieval UTC, reading locations, eligibility, count status and limitations. Local original bytes are retained but ignored by Git; immutable source URLs and content hashes are the durable references. Five retrospective read receipts bound the full reading between source retrieval and target freeze rather than inventing an exact first-display timestamp.

`recipient_attempts.jsonl` is append-only and preserves metadata pagination, failures, transport projections, original and archived inspections, restores, full reads, image handling and integrity checks. `recipient_final_opening_bindings.jsonl` binds the eight selected sources to exact lines and row hashes in the projected archive ledgers.

No later PR comments, closure/merge outcomes, rankings or provider material were read during this recipient work. Inputs are held for the root’s remote seal; later outcome work requires a separate authorization.
