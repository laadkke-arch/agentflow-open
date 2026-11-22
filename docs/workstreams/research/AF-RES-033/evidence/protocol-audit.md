# AF-RES-033 — independent pre-body protocol audit

Date: 2026-11-22. Reviewer: separate `protocol_audit` context. This is a protocol/code review, not independent semantic validation of the study's eventual judgments.

## Decision and access boundary

**Conditional body GO:** seal the mixed-scope and reconstructed-opening-snapshot amendment, the patched collector/retriever, and the complete provider frame remotely before the recipient author opens bodies. The old SCOPE alone does not satisfy the requested mixed-scope composition. A reconstructed opening snapshot must remain explicitly unproven as the original submission.

Read: repository AGENTS.md, RESEARCH_WORKFLOW.md, this task's SCOPE.md, retrieval.py, environment.json, collect_initials.py, and recipient_frame.csv metadata. No donor cache, donor source summaries, recipient originals, S/R queries, target PR pages, or outcomes were read. External lookups were limited to GitHub API documentation. Synthetic tests below used invented metadata and strings, not the study corpus or queries. Remote seals and the actual 18 provider bodies were outside this review's access boundary.

The root authorized a subsequent repair to collect_initials.py. That repair was authored and self-tested by this reviewer; root review of the repair is a distinct step. No commit or branch change was made by this reviewer.

## Concrete findings and disposition

### 1. Earliest commit is not the opening proposal — repaired, residual uncertainty remains

The original collector read only the first surviving PR commit and restored a newly added file there. Counterexample: commit A adds an incomplete draft at 09:00, B completes the contract at 10:00, and the PR opens at 11:00. A is the earliest surviving commit, but B is the content initially presented in the PR. No force-push is required for this mismatch. A new proposal can also be added in B after an unrelated setup commit A; the old structural screen would exclude it.

The patched collector now preserves projected SHAs, author/committer dates, and parents for the surviving PR commit list. It chooses the unique topologically maximal retained commit whose committer date does not exceed PR creation, then examines only its retained ancestry for added Markdown candidates. It tracks pre-opening renames and resolves candidate blobs against the opening candidate's Git tree. It retains the earliest added-path commit separately. Incomparable candidate tips, inconsistent ancestor dates, and a possibly capped commit list fail closed.

The opening SHA is **opening_head_candidate_sha**. The original **initial_commit_sha** remains the first retained commit and must not be passed to restoration merely because its field name says “initial.” Added-design paths are structural candidates; a new README, template, copied proposal, or incidental Markdown file still needs body-based eligibility review before becoming a recipient.

GitHub documents that the PR-commits endpoint returns at most 250 commits; the collector therefore does not certify completeness when 250 or more are returned. [GitHub PR endpoint documentation](https://docs.github.com/en/rest/pulls/pulls#list-commits-on-a-pull-request).

### 2. Immutable blob verification did not bind provenance — repaired

The original restore function accepted independently supplied commit SHA, path, and blob SHA. It verified the blob's bytes, but could attach them to a different claimed immutable URL. A genuine blob hash alone cannot establish that a blob exists at a claimed commit/path or belongs to the inspected PR.

Restoration now requires the repository, PR number, opening-head candidate SHA, path, and blob SHA to match an eligible logged inspection before any blob request occurs. The opening tree provides the commit/path/blob binding. A valid blob from an unrelated commit or path is rejected. Old first-commit-only inspection records do not authorize the revised restoration and must be regenerated with the patched collector.

### 3. Mixed scope was not assured — amendment needed before bodies

SCOPE section 3 originally chose the first four recoverable eligible proposals per repository and allowed a whole/partial composition deficit. That does not ensure the user's requested inclusion of both scopes. A pre-body, per-repository quota amendment can repair the mismatch without using search performance or provider-fit outcomes. It must be described as an amendment to chronological sampling, not as the unchanged “first four” rule.

The proposed algorithm is acceptable under the precise rubric below. Preserve the excluded fourth proposal as an eligible quota exclusion, not as retrospectively “ineligible.” Retain all intervening candidates and reasons. Do not use provider fit, likely positive relations, easy citation windows, or subsequent acceptance to resolve a scope label.

### 4. Returned-window labels and Unicode coordinates — repaired by root

The original retriever populated returned_window_id even for zero-score and non-top-three rows. Although return flags were correct, a later join could mistake a hypothetical best window for an actual return. The revised retriever separates best_window_id from returned_window_id and leaves the latter empty unless returned_top3 is true. Strict citation joins must still use the return flag and the corresponding sealed window identity.

Character offsets were originally named as if they referred to NFC-normalized original-case text, while they were computed after lowercasing. Counterexample: `İ` followed by 201 repetitions of ` alpha` has NFC length 1207 but lowercase length 1208; the original recorded end offset was 1208. Root made the lowercase-normalized coordinate space and its text hash explicit. Extraction must use that coordinate space or map it to original-case text; the field rename alone does not create such a mapping. This example did not alter scores or line numbers.

### 5. Required experiment dimensions were not enforced — repaired by root

The original rank function would silently score a different corpus or recipient count. Root added checks for 18 unique candidate/source IDs, six documents per field, eight unique recipient IDs, and four recipients per repository. The final synthetic rerun verified the dimensions and duplicate rejection. Run with ordinary Python assertion handling, not optimization flags that disable these checks.

Those guards do not establish semantic eligibility, English query quality, source-word fidelity of S, or donor-blind authorship of R. They also do not validate the later 144 relation rows. The later acceptance check must establish one row for every unique recipient×candidate pair, matching sealed IDs, and verify eight denominators rather than treating 144 pairs or 16 searches as independent designs.

## Scope rubric and deterministic quota

The classification unit is the proposal's **focal capability**, not the whole Rust language or Kubernetes product.

- **Whole:** the principal proposal introduces a new independently usable construct, API, resource, workflow, or feature and specifies its input/entry, behavior, and output/error contract. Depending on existing infrastructure does not itself make a new feature partial.
- **Partial:** the principal proposal changes a bounded rule, case, limit, default, compatibility condition, or state transition of an already-defined capability. A new option or flag whose purpose is to alter an existing operation is partial unless it establishes an independently usable capability under the preceding definition.
- **Ambiguous:** coequal changes support both readings or the body does not identify a focal capability. Record the ambiguity and resolve it through a donor-blind application of the fixed rubric before query drafting. An unresolved label cannot satisfy the opposite-scope quota. If unambiguous composition cannot be established, report the quota unmet rather than relabeling to fill it.

For **each repository separately**, take the first four eligible proposals in the frozen creation-time, PR-number, then proposal-path order. If the four include both definite scope classes, retain them. If all four belong to the same class, retain the earliest three and select the first later eligible proposal of the opposite class. Log the original fourth, every intervening rejection, scope evidence locations, and the selection position. If no opposite class exists by the end of 2024, report the unmet requirement. One recipient should represent one selected proposal/PR; multiple added files must not quietly create extra sampling opportunities.

Complete scope screening and selection before the selected recipients' narrow transfer targets and S/R strings are frozen. A donor-blind recipient author should perform the screening. The integrator must not revise scope or target labels using knowledge of donor contents. Publish the original first-four identities alongside the amended selected panel so the quota's effect is visible.

## Limitations that a pre-body patch cannot eliminate

1. **Historical initiality remains unproven.** Commit dates and current ancestry are evidence about retained objects, not a historical PR-opening reference. Rebases, deleted history, altered timestamps, and changes in which commits are unique to the PR can defeat reconstruction. Empty retained force-push events do not prove original content. All such rows remain outside the strict exact-original subset; an empty strict subset must be reported as such. Historical opening-head evidence would be needed to strengthen the claim. GitHub GraphQL documents beforeCommit/afterCommit for retained force-push events, which may help a later provenance investigation but does not itself prove the opening snapshot. [GitHub GraphQL pull-request reference](https://docs.github.com/en/graphql/reference/pulls#headrefforcepushedevent).
2. **The panel is purposive and may concentrate in 2020.** Eligibility spanning 2020–2024 does not mean all years are represented. Chronological recovery, scope quotas, and survival of history can select distinctive designs. This is not a population estimate for all RFCs/KEPs in the period.
3. **R remains lexical retrieval.** BM25 discards word order and the frozen stopword list removes “not.” For example, “must not share state” and “must share state” produce the same retained token set. The study can compare two query-writing routes under this BM25 procedure; it cannot establish the performance of a retriever that understands relations, roles, or negation.
4. **Equal caps do not equalize query information.** The common 80-token maximum is satisfied by the implementation, but S/R may differ in actual length, unique-token count, and generic vocabulary. Report the existing query-length fields so a route advantage is not automatically attributed to relational abstraction alone.
5. **The window rule constrains success.** A valid procedure can cross a fixed 200-token boundary. Failure of strict citation completion then concerns the specified returned-window procedure, not necessarily the absence of a transferable relation in the full source. Keep the full-document 144-pair judgment separate.
6. **Temporal availability and independence remain limited.** Current provider policies can postdate recipients. Separate present-day transfer plausibility from availability when proposed. Separate contexts also do not establish independent human judgment or absence of model pretraining exposure.

## Verification receipt

All commands in this review used synthetic fixtures or allowed metadata and exited **0**. No real retrieval experiment was executed.

Collector checks passed:

- Multi-commit draft→completed opening candidate, including a proposal introduced after a setup commit.
- Post-opening commit exclusion and pre-opening rename resolution through tree metadata.
- Correct restoration tuple accepted; wrong commit, path, blob, repository, and PR rejected. Wrong restoration was rejected before the mocked network function could execute.
- Incomparable pre-creation tips, inconsistent ancestor dates, and the possible 250-commit endpoint cap left structural eligibility false.

Final retriever checks passed:

- Eight synthetic recipients × two routes × 18 documents produced **16 searches and 288 score rows**.
- Exact-score ties followed candidate ID order; repeating a query token did not alter scores.
- Only positive top-three rows exposed returned_window_id; all-zero runs remained empty.
- Incorrect corpus/recipient counts and duplicate identities were rejected.
- The Unicode expansion example used explicitly lowercase-normalized coordinates.

The metadata frame contains **3,415 rows**, with no duplicate repository/PR pair and ascending creation-time/PR order within each repository. Counts are Rust 638 and Kubernetes 2,777. Date range observed: 2020-01-01 through 2024-12-31. These checks concern the saved frame; API search total_count/incomplete_results receipts and remote frame identity were not independently revalidated here.

Reviewed fingerprints after repairs:

| File | SHA256 |
| --- | --- |
| SCOPE.md before the proposed amendment | `2c8fa6b277a5d41178763bd493341784b2575bfc640d66a942faf7da62b56b9d` |
| retrieval.py | `dffe067092fbb3a98547c69d6b159249bc8bebac10c0a7d7a2f7e623c8a76b5c` |
| recipient/collect_initials.py | `0b87631b632782234e8a76097aed89d65f4e3d3d5f28bfa8059df6c7d3f3058e` |
| recipient/recipient_frame.csv | `1434da7d4b3d4198aa65d018b89774a6039b3520c4a99287ab2e6f309d14e3e7` |

Before body GO, the integrator should record the remote commit containing the amendment, reviewed code, and complete provider frame, then release only the recipient-side instructions and metadata. After input/query sealing, preserve all 16 full rankings and actual returned windows before outcome inspection. These are stage gates still to be evidenced, not achievements established by this pre-body audit.
