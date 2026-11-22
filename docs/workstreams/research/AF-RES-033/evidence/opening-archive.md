# AF-RES-033 — historical opening-head corroboration

Checked 2026-11-22, 16:25:46–16:25:50 UTC. Supplementary provenance audit after the frozen recipient selection; no selection or recipient-file changes.

**All four selected Rust PRs have a matching historical `PullRequestEvent` with `action=opened`, and each archived head SHA exactly matches the reconstructed opening-head candidate. No discrepancy was found.** Each complete creation-hour archive contained one matching event. The archived PR creation timestamp also matches the frozen metadata frame for all four.

| Rust PR | Frozen/archived PR creation time, UTC | Archived opening head = reconstructed candidate | Archive |
| --- | --- | --- | --- |
| #2843 | 2020-01-04 13:02:21 | `d5fe87812fc95f2699e770993848179b6c071f2c` | [2020-01-04-13](https://data.gharchive.org/2020-01-04-13.json.gz) |
| #2845 | 2020-01-06 17:22:44 | `6fb5bd5a6132b15bfe2d9dade6a48d7a77eb2b24` | [2020-01-06-17](https://data.gharchive.org/2020-01-06-17.json.gz) |
| #2850 | 2020-01-13 13:29:48 | `5559913ccacbe1e6c6c5d26d33a08f9b09641c5e` | [2020-01-13-13](https://data.gharchive.org/2020-01-13-13.json.gz) |
| #2859 | 2020-01-23 17:42:33 | `6f967443b27c4277a8589ff94bb156179e4b33ae` | [2020-01-23-17](https://data.gharchive.org/2020-01-23-17.json.gz) |

The event timestamp is one second after the PR creation timestamp for #2843 and #2845, and identical for #2850 and #2859. This is an event/PR timestamp distinction, not a head-SHA mismatch. Projected base SHAs and matching archive line numbers are retained in [opening-archive-checks.jsonl](opening-archive-checks.jsonl).

## Method and preserved evidence

[GH Archive's own documentation](https://www.gharchive.org/) specifies public hourly compressed JSON archives; archives from 2015 onward record GitHub Events API data. The four hours were derived exclusively from the frozen recipient metadata frame. Reconstructed SHAs came only from projected inspect/restore metadata for the four allowlisted repository/PR pairs.

Four HEAD requests and four streaming GET requests succeeded. All four gzip archives were consumed to EOF without a gzip integrity error. Their compressed byte counts matched Content-Length: 21,974,432; 47,757,168; 59,584,106; and 48,398,312 bytes, respectively in table order. Total compressed transfer was **177,714,018 bytes**. Each stream was hashed; archive SHA256 values, HTTP headers, scan counts, timing, and exact executed commands are retained in [opening-archive-attempts.jsonl](opening-archive-attempts.jsonl). There were no retrieval errors or budget-limit stops.

The parser retained only matching repository/PR identity, `action=opened`, event/PR timestamps, head SHA, base SHA, and archive line number. Unfiltered event lines existed only transiently in process memory: none were displayed, saved, or supplied to a model. No archive files were written. No recipient snapshots, titles, query strings, current PR state, merge/closure fields, comments, or recipient outcomes were inspected. No credentials, new accounts, paid query service, or recipient-writer communication were used.

## Interpretation and integration boundary

The evidence supports the label **historical opening head corroborated by a GH Archive opened-event capture** for these four Rust PRs. This supplies historical head-pointer evidence beyond the earlier reconstruction from current surviving ancestry and timestamps. It does not retroactively change what was known when inputs were frozen; root should preserve the earlier uncertainty flags and attach this later corroboration with its audit time, or explicitly version any derived strict-initiality classification.

This check concerns opening-head identity. It does not independently verify proposal-file eligibility, extraction completeness, query blinding, transfer judgments, or any KEP's opening head. The archive events are supplementary provenance records and do not add four original design documents to the study's source minimum. The frozen selection and all recipient files remain unchanged.
