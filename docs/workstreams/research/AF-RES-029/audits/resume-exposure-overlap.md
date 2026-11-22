# AF-RES-029 — exposed exposure and prior-sample overlap audit

Recorded 2026-11-22T13:12:38.253080+00:00. This is an explicitly unmasked, saved-receipt audit by the same-model reader after its initial masked work. It is not another masked judgment, an independent human assessment, or a rescore. The inherited research SHA is `a4894493dbacdc9d93357426f8bd63929074bf30`; the prior-study inventory is fixed to `cf27e148b96bf3c5a3dc8a2a926db4abcf63f146`.

## Findings and denominators

The conservative **sampling outcome/later-recovery exposure set is Q05–Q12 (8 events)**, leaving Q01–Q04 (4). The **strict set covering any recorded current-status/followup exposure, including related proposals, contains all 12 events**. Its retained denominator is zero and any success rate is **N/A**. The **recorded opposite-route input exposure set is empty**, so that exclusion alone retains all 12; this is a receipt-based finding, not proof of cognitive independence.

Among **44 candidate uses in 36 original returns**, compared with **66 prior candidates**, no exact concrete component match was identified and no returned document URL matched the prior inventory. The **broader upstream-project overlap is Q02, Q03 and Q08**: Go and Bazel, involving five candidate appearances. Those are different components and operations. They must not be called the same prior sample.

| Exclusion rule | Excluded events | Retained event denominator | Interpretation |
|---|---|---:|---|
| Sampling outcome or later recovery draft | Q05–Q12 | 4 | Q01–Q04 remain; not a perfectly status-blind sample claim |
| Strict any recorded current-status/followup, related proposals included | Q01–Q12 | 0 | N/A, not 0% effectiveness |
| Positive recorded opposite-route input/result exposure | None | 12 | Same-route memory is reported separately |
| Sampling plus opposite-route exclusion | Q05–Q12 | 4 | Opposite-route rule adds no recorded cases |
| Strict exposure plus opposite-route exclusion | Q01–Q12 | 0 | N/A |
| Exact prior-025 concrete component overlap | None identified | 12 | Bounded by the supplied inventory |
| Optional broader provider-family exclusion | Q02, Q03, Q08 | 9 | Deliberately broader than exact-component repetition |

Sources for these sets are the per-question records below, the 36 rows of `returns.jsonl`, and all 66 entries of `evidence/excluded-025-candidates.json`. The JSON companion supplies row-level references, candidate-level comparisons, exact URL lists and hashes for the saved inputs. Candidate appearances, mirrored documents and URLs are not additional design events.

## Definitions that make the sets auditable

**Sampling exposure** includes explicitly recorded later status/outcome/implementation metadata and substantive later drafts encountered while recovering first versions. The distinction matters: Q05, Q06 and Q07 have later-body exposure but a null `later_status_exposure`; the audit does not invent an acceptance label for them. Q08 has an explicit Deferred header. Q09–Q12 have explicit later-status metadata flags. Thus the narrower explicit-status subset has five events (Q08–Q12), while three more (Q05–Q07) have substantive later-draft exposure. The eight-event union is the conservative sampling sensitivity. Current titles, dates, downloaded-but-unshown status fields and an initial Draft header do not alone trigger it. See `streams/python/questions.jsonl` rows 1–4, `streams/python/SAMPLING.md` lines 40–50, `streams/numpy/questions.jsonl` rows 1–4, and `streams/numpy/exposures.jsonl` rows 1–3.

**Strict exposure** is broader and stage-aware: it includes relevant current proposal, predecessor, companion or followup snippets; explicit current implementation/release changes; and later bodies in sampling, common search or either route. A snippet can count as exposure even though it was never opened or admitted as evidence. A current page date, unrelated catalog name, stored unshown payload or generic link label does not by itself qualify. This rule does not imply that the sampled proposal succeeded. Q01 is included because the saved Route A receipt exposes a related Incan RFC under `closed/implemented`; Q02 is included because it exposes the current sampled issue and its benchmark-format predecessor. Consequently a rule considering only common-search followup flags would miss two recorded Route A cases. See `routes/A/Q01/exposures.jsonl` rows 3–6 and `routes/A/Q02/exposures.jsonl` rows 2–6.

**Opposite-route exposure** requires a positive record that an executing selector saw the other route’s specific input, selection, return or judgment before its own return. Authorized common baselines, same-route batch preloads, prior questions in the same worker and completion-only scheduling messages are separate. All A return contexts state their separation from B; all B contexts explicitly set `opposite_route_read=false`. Q11’s fresh-worker handoff is corroborated by `evidence/route-coordination.jsonl` row 1. No positive case was found; absence of a positive record is not an independent verification of every internal cognitive boundary.

## Event-level exposure evidence

Rows refer to JSONL rows, starting at 1. The frozen question row and `questions.jsonl` row equal the numeric Q suffix. Every event retains its original C/A/B return rows; no empty return is removed.

| Event and design | Sampling exclusion | Strict exposure: sufficient saved record | Original return rows C/A/B |
|---|---|---|---|
| Q01: golang/go#56094 | No positive later-outcome/draft record | Related implemented Incan RFC and other proposal snippets. `routes/A/Q01/exposures.jsonl` rows 3, 4, 5, 6 | 1/2/3 |
| Q02: golang/go#43744 | No positive later-outcome/draft record | Current #43744 and benchmark-format predecessor snippets. `routes/A/Q02/exposures.jsonl` rows 2, 3, 4, 5, 6 | 4/5/6 |
| Q03: golang/go#70887 | No positive later-outcome/draft record | Current runtime fatal/recover behavior; common followups also flagged. `routes/A/Q03/exposures.jsonl` rows 2 | 7/8/9 |
| Q04: golang/go#58584 | No positive later-outcome/draft record | Current #58584 and derivative Go 1.24+ wasmexport claim. `common/Q04/exposures.jsonl` rows 3, 4 | 10/11/12 |
| Q05: pep-0667 | Yes: later recovery draft | Current PEP 667/558 and 3.13 frame implementation references. `routes/A/Q05/exposures.jsonl` rows 2, 3, 4, 5, 6, 7 | 13/14/15 |
| Q06: pep-0686 | Yes: later recovery draft | Current Final/3.15 status, related discussions and default-change notes. `common/Q06/exposures.jsonl` rows 3, 4, 5, 6, 7, 8, 9 | 16/17/18 |
| Q07: pep-0727 | Yes: later recovery draft | Current PEP 727 later naming/status snippet. `routes/A/Q07/exposures.jsonl` rows 2, 3 | 19/20/21 |
| Q08: pep-0778 | Yes: explicit later status/metadata | Current Deferred PEP 778, companion and predecessor proposals. `common/Q08/exposures.jsonl` rows 3, 4, 5, 6, 7 | 22/23/24 |
| Q09: NEP-50 | Yes: explicit later status/metadata | Current NEP 50/47 and implementation-change references. `routes/A/Q09/exposures.jsonl` rows 2, 3, 4, 5, 6, 7, 8, 9 | 25/26/27 |
| Q10: NEP-47 | Yes: explicit later status/metadata | Later NEP 47 mirror plus related RFC links in context. `common/Q10/exposures.jsonl` rows 3, 4, 5 | 28/29/30 |
| Q11: NEP-55 | Yes: explicit later status/metadata | Later StringDType implementation/release outcomes, including fresh B. `routes/B/Q11/exposures.jsonl` rows 1, 3, 4, 5, 6 | 31/32/33 |
| Q12: NEP-53 | Yes: explicit later status/metadata | Current NEP 53 and incidental adopted NEP 50 reference. `common/Q12/exposures.jsonl` rows 3, 4 | 34/35/36 |

### Sampling provenance and remaining unknowns

For Q01–Q04, `streams/go/exposures.jsonl` rows 1–7 records current-title enumeration, reduced API payloads, schema probes, recovery navigation, proposal-tree metadata, coding clarification and initial-body batch overshoot. These records explicitly deny outcome/later-comment reading. Titles may have changed; the audit therefore says “no positive recorded later outcome/draft exposure,” not “no modern information seen.” The frozen issue identities are #56094, #43744, #70887 and #58584 (`questions.jsonl` rows 1–4).

For Q05–Q08, `streams/python/questions.jsonl` rows 1–4 and `streams/python/freeze-receipt.json` `/limitations/3` explicitly record the recovery exposure. Q05’s later copy changes the live `locals()` boundary to snapshots; Q06 retains the original locale exception; Q07 retains initial `doc()`/`DocInfo`; Q08 exposes Deferred in a later header without reading that later substantive body (`streams/python/SAMPLING.md` lines 44–50). These records support exposure flags and explain why later wording must not repair the frozen requirements.

For Q09–Q12, `questions.jsonl` rows 9–12 and `streams/numpy/questions.jsonl` rows 1–4 explicitly mark `later_status_metadata_seen=true`. NumPy exposure rows 1–3 describe broad discovery, a full PR-title census, and recovery summaries containing status or implementation information. These are shared sampling-worker exposures, linked to all four events; the audit does not pretend every item is a separately witnessed outcome for each event. **The first full discovery response is not stored locally** (`streams/numpy/exposures.jsonl` row 1 and `streams/numpy/sampling-integrity.json` `/limitations/0`). The summary is preserved as a summary, without reconstructing missing text.

Common C and route A/B bodies may also describe current supplier implementations. That is compatible with testing current supplier behavior against a frozen first design, but it prevents describing the research process as fully status-blind. The strict sensitivity is deliberately severe and has no eligible events. Exposure says neither that a predicate is supported nor that the exposure changed a selector’s decision.

## Opposite-route separation and same-worker memory

The original return contexts provide the per-event opposite-route checks: A is in `returns.jsonl` rows 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32 and 35; B is in rows 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33 and 36. The JSON companion points to `/context` or `/context_isolation` for each. Common data were intentionally shared, and the later exposed audit does not retroactively contaminate these earlier route-input records.

There is, however, extensive documented **same-worker, same-route cross-question memory**. A used one worker in the order Q01, Q03, Q05, Q07, Q09, Q11, Q02, Q04, Q06, Q08, Q10, Q12. Its six odd input packets were initially read as a batch. B’s shared worker completed Q02, Q04, Q06, Q08, Q10, Q12, Q01, Q03, Q05, Q07, Q09; it preloaded the even inputs and later the odd metadata. Only the completed Q11 B return came from a fresh single-question worker. These sequences are preserved in the per-return contexts and exposure rows.

That gives **23 of 24 route executions with multi-question context**, and **21 of 24 with earlier completed questions in the executing worker**. The first A question Q01 and first B question Q02 still had batch-input exposure, while Q11 B had neither prior completed-question nor other-question-input exposure in its executing worker. Every event has at least one multi-question route, so a hypothetical requirement that both A and B be fresh per question leaves zero pairs: N/A. This is not the same as opposite-route input exposure.

Two saved examples show why the distinction matters. `routes/B/Q05/exposures.jsonl` row 3 records that Q06 B’s builtins receipt had already delivered current `locals()` snapshot semantics and a PEP 667 reference. `routes/B/Q07/exposures.jsonl` row 4 records earlier Q05 inspection text containing `inspect.cleandoc`. The logs say these were not authorized as the later question’s source or used to enlarge its link boundary, but they remain memory exposures. Their causal influence cannot be quantified from receipts.

For Q11, do not attribute the shared B worker’s preloaded Q11 metadata to the worker that actually produced its return. `routes/B/Q09/exposures.jsonl` row 6 says the old worker did not start Q11 originals/common-body/network work; `evidence/route-coordination.jsonl` row 1 records reassignment; `returns.jsonl` row 33 records the new worker’s single-question context. That fresh context still encountered later implementation and release material, as listed in `routes/B/Q11/exposures.jsonl` rows 1, 3–6.

## Prior-025 component and document overlap

The prior inventory is explicitly for exclusion, with dependency SHA and 66 candidate records (`evidence/excluded-025-candidates.json`). Its purpose and worker boundary are corroborated by `evidence/method-inputs.json`: prior work was a method correction/overlap input, not supplied to route workers. The comparison here reviews the returned candidate names, proposed uses and cited sections against that inventory. It does not assign predicate success or infer historical author knowledge.

The 66 prior records contain **82 distinct cited URLs**, and the 44 current candidate appearances contain **41 distinct returned URLs**. Their intersection is empty after fragment removal and scheme/host case normalization; it remains empty with query strings removed. The additional URL-only scan of **36 common/A/B source ledgers** (690 URL fields, including `original_url`) likewise found no exact prior citation URL. This cross-check concerns URL identity. The source ledgers include initial texts, discovery snippets and failed attempts as well as supplier bodies; it does not claim that every inventory row delivered usable text or was returned as a candidate. Different editions, mirrors and filenames are not silently merged.

| Current event / return / candidate | Prior family record | Relationship and boundary |
|---|---|---|
| Q02 A: benchfmt Reader/UnitMetadataMap and benchstat (`returns.jsonl` row 5, candidates 1–2) | CG-K031, prior candidate 43, JSON pointer `/candidates/42` | Same Go upstream family. Benchmark metadata parsing/statistics differs from old-to-new API forwarding with preserved defaults. |
| Q03 C: runtime error handling and current mirror (`returns.jsonl` row 7, candidates 1–2) | CG-K031, prior candidate 43, JSON pointer `/candidates/42` | Same Go family. Runtime fatal/panic guidance is a different operation; mirrored runtime guidance is one component. |
| Q08 A: Bazel FilesetOutputTree (`returns.jsonl` row 23, candidate 2) | CG-K005, prior candidate 22 (`/candidates/21`); CG-K003, prior candidate 25 (`/candidates/24`) | Same Bazel family. Relative-symlink traversal differs from Bzlmod local_path_override and local_repository. |

Those are **five candidate appearances across three events and two upstream families**, representing four distinct current component/use names when the Q03 mirror is consolidated. They are not five repeated prior candidates. The exact-component exclusion removes none; the optional project-family sensitivity removes Q02/Q03/Q08 and leaves nine events. Report those as different sensitivity definitions.

Several easy false matches were rejected. Q08 Goomba and prior Precinct are separate third-party Go packages hosted by `pkg.go.dev`. Q01 MDN JavaScript destructuring and prior Node.js `listen(0)`/child IPC share a language ecosystem but not the supplier component or operation. Q04 WebAssembly exports/memory and prior WebSub subscription verification are different standards. CPython, PyPA, NumPy and JAX are not the prior Jupyter/ipykernel, Arrow or Blosc suppliers merely because they share Python or array-related topics. The frozen designs also name background families present in prior025—Go in Q01–Q04, Go/Rust/Node.js in Q06, and pyarrow in Q08—but a background name is not a returned matching component (`judging/frozen-questions.jsonl` rows 1–8).

The supplied exclusion file does **not** contain the full identities of the 12 prior design events. Therefore an empty candidate/document match does not independently prove that every new design event differs from every old event, nor does it establish literature novelty. Unlisted mirrors, aliases, archived editions or unspecified prior documents remain unknown. No different component was relabeled the same prior sample.

## Preservation and reproducibility

Only this Markdown file and `audits/resume-exposure-overlap.json` were written for the exposed task. No web requests, git operations, ranking-key reads, supplementary evidence expansion or reader_2/reader_3 judgment reads were used. The three original reader_1 files were checked by hash before and after creation and left unchanged:

- `judging/reader_1/judgments.jsonl` — `ecdc6aa51e9a15cfed9bc2d45b86a47abc48b31dd7488c7e7c2d85d91368556f`
- `judging/reader_1/NOTES.md` — `b83f52ddb7ea40c28556ef24c4ed8e7c329c30a7cb10474c9196152377c1afc6`
- `judging/reader_1/read-log.jsonl` — `b8dd4d293cc4a3799b41fa14767a9cdbb506a0c386e0ea3e47e81c1ec175fcc9`

The JSON companion preserves the event sets, definitions, per-Q source rows, all 44 candidate-use comparisons, prior candidate pointers, exact document intersections, source hashes, and explicit unknowns. Its evidence inventory is a reproducibility list of saved inputs used or inspected; it is not an assertion that every byte was substantively displayed to the model. Large exploratory projections were sometimes truncated, and the relevant exposure records and comparison fields were reread in compact form. The frozen masked read log remains a record of the earlier masked task only.
