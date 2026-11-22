# AF-RES-033 — archive restoration fallback

Authorized by root under remote amendment `8358b5e75ca45fd9bf0e26cab70e2acc1bc39493`, before final input/query sealing or retrieval. Execution: 2026-11-22 16:31:51–16:32:48 UTC.

**Recovered historical opening head and base SHAs for all 20 authorized earlier history-failure rows.** Each has exactly one matching archived `PullRequestEvent`, action `opened`, and an archived PR creation timestamp identical to the frozen frame. All 19 distinct hourly archives were fully scanned and hashed. No target remains unresolved in this batch.

## Covered chronological targets

- Kubernetes, before PR #1478: **1433, 1438, 1439, 1444, 1445, 1447, 1448, 1450, 1452, 1454, 1457, 1458, 1461, 1462, 1463, 1466, 1467, 1473, 1474**.
- Rust, before PR #2859: **2856**.

The target list came exclusively from frame/inspection metadata. Every row had the prior reason `no_unique_precreation_opening_head_candidate`; none was added because of proposal semantics, scope type, provider fit, later outcomes, or retrieval performance. No earlier frame row in these bounds lacked an inspection receipt. Kubernetes #1462 and #1463 share the `2020-01-16-13` archive, which was downloaded once for both.

The first-four-Rust audit files remain byte-for-byte unchanged. Those earlier results concern the then-provisional four IDs. Root subsequently clarified that no final input/query seal or retrieval run had occurred and authorized recovery of earlier restoration failures. This extension preserves the existing chronological eligibility and scope rules; it expands the available historical provenance before final selection.

## Recipient handoff

[archive-recovery-checks.jsonl](archive-recovery-checks.jsonl) is the authoritative set of 20 strictly projected rows. Each usable row has:

- `repository`, `pr_number`, and frame `created_at`;
- the prior failure reason and inspection timestamp;
- `archived_opening_head_sha` and `archived_opening_base_sha`;
- archive URL, complete-scan flag, archive SHA256, matching line number, and matching event/PR timestamps;
- `status=opened_event_head_base_recovered` and `usable_projection=true`.

The projected match contains only repository/PR identity, action, event/PR creation timestamps, head/base SHAs, and archive line number. No `timestamp_eligible` flag was synthesized. The recipient author was notified incrementally after root's archive-body authorization, and received the completed ledger when all 20 checks finished.

For example, Rust **#2856** opened at head `c80e28415d8a7f94448661badb963d3d6fc9efb2` against base `3df38f62c476d074fbb6f117485c3a5034e02424`. Its PR-created timestamp is `2020-01-22T14:29:45Z`; the event timestamp is one second later. Full head/base identifiers for every other target are in the checks ledger.

The next authorized recipient-side operation is to inspect the archived base-to-head first diff and bind any eligible added proposal path to the archived head tree. Archive recovery alone does not establish that a PR introduces a new proposal or satisfies whole/partial composition. Existing template, migration, roadmap, unchanged-file, and other source-based exclusions remain separate decisions. This auditor opened no proposal body or semantic classification.

## Reproduction and verification

Run from the repository root:

```bash
python -B docs/workstreams/research/AF-RES-033/evidence/archive-recovery.py
```

[archive-recovery.py](archive-recovery.py) groups allowlisted targets by hour and writes results incrementally. [archive-recovery-attempts.jsonl](archive-recovery-attempts.jsonl) preserves the exact executed command, script hash, target projections, 19 request-start receipts, and 19 request-result receipts. Per-hour limits were 128 MiB compressed, 2 GiB uncompressed, an 8 MiB event-line limit, and 120 seconds. No limit was reached; no request failed.

The complete streams contained **800,363,594 compressed bytes**, **5,859,093,050 uncompressed bytes**, and **1,604,243 event lines**. Compressed bytes read equaled Content-Length for all 19 archives. Unfiltered events were processed only transiently in memory, never displayed or persisted; no archive files were written. No new credentials, paid service, current PR state, titles, body text, comments, merge/closure fields, query files, or retrieval outcomes were accessed by the auditor.

Synthetic checks verified the 20-target/19-hour grouping and the opened-event projection whitelist. Post-run checks verified 20 unique target identities, one matching event each, matching creation times, complete archive reads, and unchanged hashes for all three prior four-PR audit files. Commands exited 0.

| Artifact | SHA256 |
| --- | --- |
| archive-recovery.py | `1cc05ee1c08d14c2c40221f38b481a1992e8c4f312fd3a806722f7c095b6bb58` |
| archive-recovery-attempts.jsonl | `4542526a70b4e65f6b7b98b654246b3872d8a87d73f3e407c264b89b721b9f3b` |
| archive-recovery-checks.jsonl | `32b89a477d65e90467c9128451af64ba4d79270a1f22eb38ea2657ee88865484` |

No later failure rows through #1621 were requested or checked in this batch. These archive events are restoration evidence and do not add to the study's count of original proposal documents.
