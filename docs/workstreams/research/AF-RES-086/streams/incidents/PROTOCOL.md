# Q6 incident protocol — frozen before search

Date: 2026-11-23 UTC. Search period: issue creation 2024-01-01 through 2025-12-31 UTC inclusive.
Repositories: jimporter/mike; mkdocs/mkdocs; readthedocs/readthedocs.org; actions/deploy-pages.

Search each repository with `is:issue created:2024-01-01..2025-12-31 (alias OR redirect OR 404 OR "wrong version")`, sorted creation ascending. The repositories are a prespecified four-family frame, not prevalence sampling. Retrieve up to 30 candidate metadata records per repository. Sort admitted issue metadata within each family by created_at then issue number. Read the earliest three unique issue events in each family, then present those twelve in global chronological order (UTC, repository, number). If a search parser rejects the disjunction, perform the four literal-term searches separately and deduplicate their union; preserve that amendment and all query receipts. Empty families stay empty until an explicit recorded supplemental query is made.

Issue metadata alone is not original content evidence: directly fetch body and comments for each selected event. Linked fix PR, actions run, deployment, ref and before/after HTTP evidence belong to the same incident lineage. Search results, inaccessible URLs and repeated mirrors do not add source or lineage counts.

Strong positive requires all of: (1) publisher evidence of successful generation; (2) successful publication; (3) same ref or artifact identity; (4) wrong reader URL content/response; (5) recovered expected content. A report that a CI badge is green, a closed issue, deployment intent/configuration, or a currently working URL alone is insufficient. A report may support a narrower routing defect without meeting the strong chain. Different names with same identified content are a reverse/no-change control, not failure.

Scope selection is independent of the four fixed consumer slots P3/R1/P1/R2. Denominators remain separate. Unresolved and irrelevant first-twelve events are retained with exclusion reasons. Strong counterexample count may remain zero. Source metadata, comments and follow-up evidence record observed UTC and provider versus researcher observer.

## Execution notes (post-search; original rule above unchanged)

- GitHub accepted the disjunction. Search returns12/20/30/6 records for mike/MkDocs/RTD/deploy-pages; RTD is capped at30. These are returned candidate counts, not full event population denominators. Earliest-three selection is unaffected by later capped records.
- Discovery and source transport were batched. Issue metadata/body delivery was concurrent, then the retained first-twelve were coded and presented by creation UTC and issue number. This is chronological coding of a prespecified stratified first12, not a claim that the server requests themselves occurred in chronological sequence or that these are the global earliest12 across all projects.
- Supplemental selection, kept outside the first12 denominator: RTD11531 (same-revision label control), mike229 (alias label control), deploy-pages383 (stale artifact with success), mike248 (trailing-slash loop). All were in the original returned candidate lists; no post-outcome replacement of any first12 slot.
- deploy-pages383 led to typst-community/dev-builds issue1, a publisher reproduction of the same incident family. It is not a seventeenth independent incident. Its source/ref and retained logs are supplementary evidence within383.
- 2026 comments returned by current API retrieval are preserved for provenance but excluded from the2024–2025 incident inference. In particular, the stronger2026 reproductions in383 do not fill this task's recovery evidence gap.
- AF-RES-082 incident NOTES was read at the fixed dependency commit solely as an inherited lead. Its2023 mike188 and2022 deploy-pages76 incidents are outside this protocol's creation window and not added to the sample.
