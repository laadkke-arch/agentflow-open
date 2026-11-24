# Post-seal clarification: timestamp provenance and G2 execution receipts

This addendum clarifies metadata only. No sealed gold value, grade, criterion, packet, or receiver response was changed. The gold actor has not inspected receiver files.

## Timestamp precision correction

`gold.csv` records `read_start_utc=2026-11-24T01:52:00Z`. This was a **retrospectively assigned, minute-rounded estimate of the reading session start**, not a timestamp instrumented at the first read. It must not be presented as an exact event or used to prove minute-level ordering of preregistration and reading. There was no per-tool-call start-time logger for those initial gold reads.

The common `sources.jsonl` interval `2026-11-24T01:52:00Z/2026-11-24T02:00:02Z` also needs this qualification: its lower endpoint is the same estimate; the upper endpoint came from an actual clock-tool observation. It is an approximate session label, **not a demonstrated bound for every source row**. Some follow-up reading, including further issue-comment inspection, continued after that clock observation. The existing `bounded observed session interval` wording overstates its precision. Source-specific exact reading instants cannot be reconstructed from that field alone.

`gold.csv`'s `read_end_utc` was obtained with Python's current UTC clock while assembling the gold ledger. It precisely timestamps that metadata assignment, not the instant when the model finished reading the final source. Archive receipts use UTC captured after downloading the bytes; those timestamps measure retrieval completion, not completion of model interpretation. Execution receipt UTC values were captured immediately before the corresponding subprocess call.

For formal ordering, use actual tool-event ordering, file hashes, and the remote commit/receipt chronology. The input remote-seal timing deviation already recorded in gold-method.md remains a deviation; this addendum does not repair it retroactively.

## G2 current-engine execution semantics

All three observations below used the installed `4.7.2.stable.official.ed1daf0bf`. They do not verify the originally reported `4.0-dev.20220118` runtime. These are previously recorded executions, not new runs during this clarification.

| Receipt / execution | Captured subprocess-start UTC | Numeric stdout | Stderr | OS exit code | Meaning |
| --- | --- | ---: | --- | ---: | --- |
| `run-current-engine.json` / `G2-run` | 2026-11-24T01:56:31.372078+00:00 | 8 | GDScript `Assertion failed` at test.gd:9 | 0 | The example's expected-sum assertion failed despite normal process termination. This is not a passed correctness check. |
| `run-controlled-current-engine.json` / `G2_all_ones_same_uid_run` | 2026-11-24T01:58:27.573432+00:00 | 4 | Empty | 0 | Researcher-constructed all-ones input; its expected assertion was changed to 1+1+1+1. It cannot expose identity collapse when every value is equal. |
| `run-controlled-current-engine.json` / `G2_distinct_paths_no_uid_run` | 2026-11-24T01:58:31.643811+00:00 | 7 | Empty | 0 | Supplemental treatment removed UID attributes from the resource files/references while retaining Number/Sum classes and values. It is not claimed to reproduce the author's historical resave operation. |

`G2-run` followed a current-engine editor import of the extracted source/config files. Original editor cache and icon assets were excluded from extraction. The import itself reported duplicate UID warnings and script-class initialization errors; its exit code was also zero. These environment/input qualifications are preserved in the original logs and REPRODUCE-GOLD.md.
