# Final evidence-ledger consistency review

Recorded UTC: **2026-11-24T03:06:53.242410Z**. Resolution verified UTC: **2026-11-24T03:08:15.637666Z**. Snapshot began 2026-11-24T03:06:53.178260Z.

## Conclusion

**The integrated ledgers reconcile. Three narrative findings were identified and then corrected by the parent: two source-link targets, a Chromium date reconciliation, and one exact column name. The corrections were independently verified; no material finding remains open.** They do not change the numeric findings or repair the strict-comparison denominator. No new semantic contradiction was found among candidate decisions, choice counts, cost counts, source-family allocation or aftermath rows.

This independent AI consistency review used only AF-RES-109 files. It did not conduct new external research, repeat technical source adjudication, execute candidate tests, run `recalculate.py`, run git or modify inputs. The search seal remains `628e33709b0be7a19486f1bfeaef93f42e129394`. The parent reported result commit `ada47907ac8ee68b5e12e02e246d37cdab0930fd`; this review identifies its actual local inputs by hashes and does not claim an independent git verification of that commit.

Reviewed `RESULT.md` SHA256: `ea060de3c73724741dce08b75ff09608b3f0a904722a9d6772e05cc2c5b14be8`. Reviewed `result-analysis.md` SHA256: `4eb9985cbaf34faeec2b0ef841eb2587a28862a99e6d6e771441d1c8aa9b9896`. Complete coverage and hashes for all28 inputs, plus preservation hashes for the48 raw arm files, are in [the JSON review](final-ledger-review.json). Inputs were rechecked unchanged while this report was built.

## Findings and verified corrections

The findings below describe the initially observed result snapshot (`56c173f986df64d96ee849f1af4f5f92cdc5c11d827f2caf2a2675b4496665ef`). The parent applied the corrections, and this reviewer read the corrected table, narrative and root reconciliation fields before marking all three resolved. Raw blind judgments were preserved.

| ID | Scope | Finding and exact correction |
| --- | --- | --- |
| FLR-01 | Q5 citations in RESULT and result-analysis | Vault links `/api-docs/secret/kv/kv-v2#patch-secret`, while the recorded reads are [the command page](https://developer.hashicorp.com/vault/docs/commands/kv/patch), sources `R3-A-S2`, `BLIND13-S09`, `ROOT-VERIFY-VAULT`. yFiles links `ParallelEdgeRouter.html`, while all relevant reads are [ParallelEdgeLayouter.html](https://docs.yworks.com/yfiles/doc/api/y/layout/ParallelEdgeLayouter.html), sources `R5-B-S2`, `BLIND46-PV-R4R6-09`, `ROOT-VERIFY-YFILES`. Replace the narrative citations with those read URLs and use the matching class label. No new read is necessary. This review does not claim the unrecorded pages are nonexistent. |
| FLR-02 | Table2 R6-B-1 and Q6 | The result says only the older encoding has2018 evidence and treats the other revision date as wholly unknown after a failed lookup. Sealed `R6-B-S6` records the `3b54b6aa` tree date **2018-10-12**, without timezone. Later `BLIND46-PV-R4R6-18` failed to reread that metadata; `BLIND46-PV-R4R6-20` separately dates `297980d7` to **2018-06-04**. Preserve both original success and later independent failure. Exact UTC, first introduction, reporter deployment and original-request edition remain unverified. Retain the raw blind historical judgment and reconcile at the root interpretation/table level. |
| FLR-03 | Q2 | The ledger column named `location` in prose is actually `exact_location` in both baseline.csv and requests.jsonl. Correct the exact field reference. |

All three findings are resolved in the final hashed snapshot. These are traceability and qualification corrections. They do not add sources, recover original request editions, validate a strict A/B comparison, or establish an application success.

## Confirmed reconciliation

| Quantity | Recomputed result | Interpretation |
| --- | ---: | --- |
| Natural requests / verified original editions | 6 / 0 | Current public opening posts; R5 title provenance is not original-body proof. |
| Strict comparison denominator | 0 | All36 candidate strict flags and all33 choice strict flags are false; no winner, tie or success rate is supported. |
| Candidate slots / returned / vacant | 36 / 33 / 3 | Vacancies are R1-A-3, R1-B-3 and R3-A-3. |
| Search runs / queries / explicit page actions | 12 / 30 / 52 | Every cost row matches the prior execution audit; failures and reopens remain charged. |
| Global source rows / credited inventory units | 198 / 33 | Exactly6 request +17 search +6 counter +4 external;17 search units are conservative work/function families. |
| Deduplicated proposed choices / tests | 12 / 27 | R1–R5:9/22. Provisional R6:3/5. Includes conditional alternatives and near misses; not12 full solutions. |
| Executed candidate experiments | 0 | All33 application-result fields remain unknown; proposed fixtures are separate from the6 natural requests. |
| Original requester recovery / patch-and-release episodes | 1/6 / 3/6 | R2 recovery statement; R1/R3/R6 patch and release evidence. No causal adoption of this research. |

The36/33/3 coverage, source foreign keys, all33 neutral-ID mappings, blind decision text, condition judgments, implementation/test flags, deduplication keys and verification-source mappings reconcile without differences. Every verification-source ID resolves. Every global source has the canonical provenance, edition, direct-read time, section, confirmed/limit/counter/unknown, question, experiment and accounting fields; phase-specific alias differences are not evidence gaps. The global aftermath CSV is byte-identical to the independent six-row aftermath deliverable. No double `AFTER-AFTER-` IDs remain, and failed aftermath fetches retain null actual/arrived URLs.

The accounting families cover all52 sealed search acquisition rows exactly once. Their17 carriers exactly match the genealogy audit, including transferring credit to the original substantive reads `R2-B-S4`, `R3-B-S4` and `R4-B-S1-R2`. Raw arm flags and original work IDs remain in the derived rows. All48 raw arm files match the execution-audit hashes. [Source accounting](../source-accounting.json), [genealogy audit](source-genealogy-audit.md), [execution audit](execution-audit.md).

## Descriptive counts and common consumption

| Arm | Full candidate rows | Full choices/tests | Unambiguous common-prefix choices/tests | Queries / explicit actions | Sum of arm elapsed seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 16 | 8 / 16 | 5 / 11 | 15 / 23 | 1934.069433 |
| B | 17 | 8 / 16 | 2 / 7 | 15 / 29 | 2234.938809 |

Counts use the numeric novelty flags **and** distinct choice/test keys. A diagnostic row may have a nonempty choice key with implementation flag0; counting keys without that flag would overstate implementation choices. The15 `new_implementation_decision` classifications are also not interchangeable with16 raw implementation flags or12 deduplicated choices.

Every common cap, eligible rank and indeterminate rank matches the execution audit. R3-B ranks1 and3 remain indeterminate because index order and recorded UTC order admit different candidates; no specific identity receives robust credit. R4-A and R5-B correctly receive no common-prefix candidates because their third query occurs before the necessary reads. Common-prefix counts establish only acquisition eligibility, not that an idea had been formulated at the cutoff or that a shorter-budget rerun would reproduce it. [Costs](../../costs.csv), [choices](../../choices.csv).

The two arm totals are descriptive observations, including provisional R6. They support no comparative efficiency or time-savings claim. Automatic reads, tokens and money remain explicitly unknown. Elapsed sums include model/tool waits and overlapping requests and are not whole-study wall time or developer effort.

## Overclaim safeguards present

**R5 topology:** the only raw yes/yes rows, R5-B-2 and R5-B-3, explicitly say `same_pair_interpretation_only`. Their root interpretation preserves the unknown original image/fan-out issue, and every strict full-solution flag remains false. The result table and prose carry this limitation.

**R6 integrity:** all6 final R6 rows retain `original_discussion_blind=false`, `current_eligibility=provisional_exposed_reader`, and strict eligibility false. Method/rank blindness is separately true. The exposure row `BLIND46-PV-R4R6-26` is absent from every candidate support list. No pre-exposure final judgment or restored blindness is asserted. [R4–R6 review](../blind/r4-r6/review.md).

**Original discovery versus later verification:** successful post-search rereads can support current plausibility without becoming original-search primary credits. In particular, R1-A-S3 remains excluded as an original rewritten acquisition, and the held Function comparator R2-B-S6 still receives no new-test credit. Blinded verification, root rereads and all46 same-episode aftermath rows add zero inventory credits; counter/external sources are counted only in their separate post-search allocation. The33 count is a conservative inventory, not33 independent mechanisms or historically available solutions.

**Q7:** independently recomputed24 comments,76 timeline events,33 successful nonempty responses plus9 successful empty collections, and4 failures. Thus42 successful responses include the9 empties; there are46 retrieval records. R2 alone contains explicit original-requester recovery. R6 retains other-user correction and later slow-zoom counter-observations; merged/released does not become requester confirmation. All6 rows deny recommendation causality, all6 reviewer-execution counts are0, and public2024 actions predate the2026 searches. [Aftermath ledger](../../aftermath.csv), [independent review](../aftermath/review.md).

**Report structure:** the first three result tables contain6/36/6 data rows; the final weaknesses table has exactly3. The result-analysis content is the exact narrative suffix of the reviewed result. Its PARTIAL status, strict0, conditional12/27, source33 qualifications, and noncausal aftermath interpretation agree with the ledgers. The identified citation and metadata qualifications now agree as well.

Editorial note: Q5 uses the broad link label ParallelEdgeRouter while targeting the correct ParallelEdgeLayouter API; this is a remaining nonblocking editorial label, not a source-evidence mismatch.

## Boundary

This audit checks internal evidence accounting and claim consistency. It is not proof of source correctness, original-edition authenticity, model equality, clean automatic exposure, successful application of any candidate, or causal adoption/time savings. Findings apply to the recorded input hashes; later corrections should be verified against their new hashes while preserving this observed snapshot.
