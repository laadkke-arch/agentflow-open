# AF-RES-033 prefix opening-event corroboration

Execution: `prefix-archive-20261122T165431`. Completed: 2026-11-22T16:55:06.842682+00:00.

## Result

**All eleven authorized prior structural exclusions have a unique historical opening event, and all eleven archived opening heads exactly match their previously reconstructed heads. There are zero head discrepancies.** Every corresponding hourly archive was streamed completely and hashed; there were no failed attempts, retries, adjacent-hour searches, or unresolved targets.

The archived base SHAs are now available for the recipient collector's separate opening-diff metadata verification. Matching the head does not, by itself, establish that a structural exclusion is correct: the added/renamed proposal-path check must still use the archived comparison. This audit did not read those proposal bodies or decide semantic eligibility. It also does not decide any outcome-based result or the first-authored-draft question.

| Earlier PR | Archived head prefix | Archived base prefix | Matches reconstruction | Projection line |
|---|---|---|---|---:|
| rust-lang/rfcs #2842 | `be2e05ce9230` | `751cf1141760` | Yes | 1 |
| kubernetes/enhancements #1429 | `501a8dcf2331` | `7598d57720f8` | Yes | 4 |
| kubernetes/enhancements #1430 | `60e4f0c0f8a0` | `f6af521711a2` | Yes | 3 |
| kubernetes/enhancements #1431 | `eee627cabcdf` | `f6af521711a2` | Yes | 2 |
| kubernetes/enhancements #1434 | `fa614a77e0f5` | `98dca0ce7f3f` | Yes | 6 |
| kubernetes/enhancements #1436 | `ca5d42032606` | `98dca0ce7f3f` | Yes | 5 |
| kubernetes/enhancements #1437 | `4b9c4a6cdfac` | `98dca0ce7f3f` | Yes | 7 |
| kubernetes/enhancements #1442 | `82ffcee708bd` | `82f7787d7549` | Yes | 8 |
| kubernetes/enhancements #1443 | `1bad7f33aa17` | `143495252ccf` | Yes | 10 |
| rust-lang/rfcs #2847 | `41a81ea16067` | `81c6debd8e03` | Yes | 9 |
| kubernetes/enhancements #1449 | `4f24da05bb42` | `143495252ccf` | Yes | 11 |

Full immutable SHAs and exact event/archive coordinates are in [prefix-archive-checks.jsonl](prefix-archive-checks.jsonl). Completed projections were made available incrementally to `recipient_inputs` for archived first-diff checks. The separate eight-source object audit remains in [initial-source-binding-audit.md](initial-source-binding-audit.md); its scope and bytes were not changed by this task.

## Method and evidence

The exact eleven metadata tuples were supplied in `recipient/recipient_prefix_archive_targets.jsonl`, SHA256 `51dbf3856b25a181b67bc3350a86db974c65771b0bf430684be4be58b532fbee`. Before streaming, the wrapper verified every tuple against the frozen frame and its explicitly referenced earlier inspection, including repository, PR number, creation time, reconstructed head, and inspection time. Receipt canonical hashes are preserved in each result.

[prefix-archive-recovery.py](prefix-archive-recovery.py) reuses the previously audited `archive-recovery.py` scanner/projector unchanged and routes its writes to new ledgers. The reused scanner SHA256 is `1cc05ee1c08d14c2c40221f38b481a1992e8c4f312fd3a806722f7c095b6bb58`. The wrapper additionally requires a complete scan and exactly one match for `usable_projection=true` and records `archived_head_matches_reconstruction` separately from both head values. Each matching payload has the exact target repository/number, `PullRequestEvent`/`opened` identity, and matching PR creation time. Event timestamps are retained independently; several are one second later than PR creation.

[Prefix attempts](prefix-archive-attempts.jsonl) preserve the command, target metadata hashes, script hashes, request URLs, HTTP and transfer metadata, start/end times, bounds, complete compressed archive hashes, and execution summary. Eleven hourly streams consumed 440,917,014 compressed bytes in total. Where a Content-Length was declared, consumed bytes equal it. No raw archive or unfiltered event was persisted or displayed. Only allowed identity/time/head/base metadata was projected; no title, source body, comment, current state, query, ranking, or PR outcome was read by the auditor.

The initial four Rust archive files, the earlier twenty-target recovery artifacts, the reused scanner, and both separate final-eight binding artifacts had identical before/after hashes. There were no recipient-file edits and no commits by this auditor.

## Artifact hashes

| Artifact | SHA256 |
|---|---|
| `prefix-archive-checks.jsonl` | `35a32dbbdcce8a1a07d7f759bf6642f39c2a8347c9fa2318863f7266617e7efa` |
| `prefix-archive-attempts.jsonl` | `0104de52e98cfadf23124c8640c33f4caa0d0ce3a4b5980b96ef045c6a664b7f` |
| `prefix-archive-recovery.py` | `1ac3605081b63e2a153e2f3c60be078757678eb95475ded663c2c9b5ad57fc9f` |

This closes the opening-head provenance question for these eleven exclusions. Structural first-diff decisions are separately recorded by the recipient collector, as described below.

## Recipient handoff received after event verification

The recipient collector subsequently recorded `archive_prefix_verification_complete` at 2026-11-22T16:55:52.538948Z, in `recipient/recipient_attempts.jsonl` row 569 (canonical row SHA256 `e4a291436b0debad277ce4e12c33d87849fe3978e312effa80951f46aa7618a6`). That receipt binds the exact prefix projection-file hash, reports 11 matching opening heads, zero new proposal paths, and unchanged selected identities. The collector also reported that all eleven archived comparisons had no added/renamed proposal Markdown and no capped file lists. These are the recipient collector's structural verification results; the present auditor did not reopen bodies or independently reinterpret proposal eligibility. The final eight identities consequently remain unchanged according to that handoff.
