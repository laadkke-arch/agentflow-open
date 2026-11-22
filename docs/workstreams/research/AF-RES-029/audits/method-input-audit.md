# AF-RES-029 — independent static input-method audit

## Finding and scope

**The fixed sample, predicates, and common retrieval receipts pass the structural checks below. A fully status-blind, fully prospective sampling-and-selection claim does not pass.** Keep the actual frozen comparison and report its limitations; do not repair these gaps by rewriting inputs or recasting later recovery as the original experiment.

This is a separate fresh **same-model GPT-6 Astra Pro agent context**, not an independent human review. The reviewer received the audit assignment and input scope, without the sampling/common workers' conversation transcripts. No `routes/*` or `route-inputs/*` file content was opened. The common seal's 24 route-input entries were explicitly skipped. There were no external requests, software implementation tests, branch changes, or commits by this reviewer. The two files in `audits/` are the only authored outputs.

**Fixed audit target:** `5543465bd18542d3994280ebaab3487ae04a1e04` (common-start bundle). The input bundle is `3475576d56b4307bd75964b9a27dc2a60093efbf`. HEAD was the common bundle when inspection began; concurrent parent work advanced it to `dd5dd2296fc5480c5d8e4b1fe7ba86b643e38430` by the recorded machine check. Every checked sealed file was compared both with the working bytes and with its blob at the fixed audit target. This audit does not extend to the concurrent later work.

Acceptance references below use the assignment's Q1–Q8 and its direct-reading/completion requirements, as recorded in `docs/automation/dot-control.json` for AF-RES-029. Evidence paths are relative to the AF-RES-029 directory unless stated otherwise.

## What the shell actually verified

The reproducible Python program, exact interpreter arguments, UTC interval, output digest, stdout-derived results, and actual exit code are in `method-input-checks.json` under `execution`. It ran with `-B` at **2026-11-22 08:07:46 UTC**, exit **0**, empty stderr. It reads an explicit input/common allowlist and rejects route paths. Its checks are artifact checks, not evidence that the proposed features execute.

| Check | Observed result | Practical limit |
| --- | --- | --- |
| Seal integrity at the fixed target and in the working copy | 24 input files and 82 common files match; 0 mismatches | 24 route-input files were deliberately unexamined |
| Sample shape | 12 unique design-event IDs; 4 each for Go, Python, NumPy; one whole and one partial in each ledger-period cell | Quota balance is not random sampling or population coverage |
| Finite frame | 2,976 unique rows; all order hashes and within-cell ranks recompute | Discovery completeness and first-date validity for every untraversed row are separate questions |
| Traversal | Go prefixes 1–7 and 1–18; Python prefixes 1–2 and 1–3; NumPy selected ranks 1–2 in each period | These verify the saved traversal, not a predetermined recovery-effort budget |
| Predicate structure | 68 whole + 33 partial predicates; 101 unique IDs; all falsifiers/inheritance references present; 144 position ranges valid; 41 stored literal excerpts match | A valid line reference does not establish that its interpretation or practical reuse is correct |
| Prospective question freeze | Purpose, adapter, distractor, one common query and two A queries present for all 12; input seal 07:36:36; input commit 07:42:34; first common search 07:44:50 UTC | Does not establish that the sampling reader had no earlier status exposure |
| Common retrieval | 12 exact frozen single-query requests; 280 supplied results; first 120 rows match raw provided order; 22 body attempts; first two pages selected according to the stored eligibility coding | Provided order is not global search rank; eligibility judgments need substantive review |
| Common coverage | 11/12 events have at least one recorded original-body read; 20 original-read records, conservatively 15 document groups | Q02 is empty; Q04 has a fetch failure; Q07 has a metadata-only second open; an excerpt is not a full-document read |
| First-design count | 81 source rows contain 12 counted distinct initial-content groups | Four are GHArchive captures of official author content, with the hosting/provenance caveat below |

The recorded Git commands also exited 0: `git rev-parse HEAD` and `git show -s --format=%H\ %cI` for each fixed bundle. Each sealed-file comparison executed `git show <target>:<path>` and checked its exit and SHA-256. The JSON preserves the complete replay program; no project checker that might traverse A/B artifacts was run.

## Substantive risks and affected acceptance conditions

### M1 — The strict preselection exposure condition is false

Python's sampling worker read later main bodies for Q05/Q06/Q07 before recovering earlier ancestry, plus Q08's later Deferred header. The Q05 later text materially differs from the frozen first draft: snapshot `locals()` versus live `locals()`. NumPy's discovery exposed NEP 47 status and later implementation facts; title/event metadata exposed further acceptance/status words. Go's worker read 20 extra initial texts beyond its eventual stopping points while recovery and boundary coding were unresolved. These are different exposures and should not be collapsed into one unspecified clean/unclean flag. (`streams/python/SAMPLING.md`, `streams/python/freeze-receipt.json`, `streams/numpy/exposures.jsonl`, `streams/go/PROVENANCE.md`, `streams/go/exposures.jsonl`.)

The saved hashes and prefixes provide evidence against outcome-based substitution. They do **not** prove that exposure had no cognitive effect on classification, eligibility, or predicate wording. Mark the literal Q1 condition of selecting before candidate/status exposure **false**; report the narrower deterministic-traversal condition as met. For Q5/Q8, distinguish sampling exposure, common-result followup snippets, and possible cross-route exposure. Route isolation itself is outside this audit. Do not call an exposure-excluded rate valid until its exclusion definition and surviving denominator are explicit.

### M2 — Ranking is reproducible; the historical frame and recovery boundary are narrower

The Go frame uses current Proposal-label membership, so removed labels are not reconstructed. Python's 125-row frame starts from current Created metadata plus one documented supplement; first-public dates and first-purpose text were not recovered for every untraversed row. NumPy combines its current directory with a title query and explicitly misses unnumbered proposals whose title omits NEP. These are finite discovery frames, not an exhaustive first-public-design universe. (`streams/go/PROVENANCE.md`, both `SAMPLING.md` files.)

Recoverability also matters: four Go exclusions include rank-14 #61897, whose current title suggests a potentially whole request before selected Q04 at rank 18. The records preserve honest failed recovery attempts, but SCOPE does not freeze a per-event recovery effort/endpoint stopping budget. A future discovery of that earlier first text could change the whole-event sample without changing a single order hash. The four selected Go bodies are third-party captures with matching opened-event timestamps, not native GitHub edit-history recoveries. Python distinguishes earliest authored PR-ancestry blobs from a proven exact opening-head snapshot. NumPy scopes dates to verified numbered-NEP PRs and acknowledges earlier related discussion/meeting limits.

For Q1, quota/rank/preserved-exclusion conditions pass; exhaustive historical coverage, exact earliest-public completeness, and official-host first-version recovery for all 12 must remain **unverified or false if claimed universally**. Count 12 original-content groups with the stated provenance limits. Do not turn them into 12 independently hosted immutable official originals.

### M3 — One preselection raw receipt is absent

`streams/numpy/exposures.jsonl#NUMPY-E01` explicitly says the first discovery response was not saved locally. A summary of seen status/implementation facts is present, and conversation reference IDs are retained, but they are not the response itself. Complete locally replayable exposure provenance is **false** for that discovery operation. This affects Q1/Q5 and the audit-trail completion condition, not the integrity of the later common search receipts, which are present. The next recovery material is the actual original conversation tool response if accessible; a new search cannot recreate the historical observation.

### M4 — Common-start diversity and the mirror rule limit strategy comparisons

Q03/Q05/Q06/Q07/Q09/Q12 use both common body attempts on the same conservatively grouped manual family. Q07's second attempt is only GitHub metadata; Q04 spends its first attempt on failure and its second on a sparsely returned PDF whose only explicit external URL is outside the allowed provider. These are real budget outcomes. They make B's reachable information depend on page rendering, edition duplication, and visible links as well as on the strategy. (`common/Q*/start.json`, `common/Q*/sources.jsonl`.)

The detailed alias/mirror rule is recorded in `evidence/common-rule-clarification.json` at **07:56:23 UTC**, after the latest common-call end of **07:50:20 UTC**. Its note says it was communicated during collection; this file timestamp is not proof of an earlier freeze. Thus an assertion that *all* common selection details were frozen before common results is **false/unsubstantiated**. This does not show A/B received different common packets, and it does not justify retroactively replacing a mirror with a better page.

For Q3/Q7/Q8, keep both 12-event and 11-event original-body subdenominators. Explain empty or unnavigable starts and same-family pairs when attributing wins/failures. For Q4/Q6 and source minima, use actual returned passages and duplicate groups; 22 opens are not 22 originals. The 15 common source groups are not automatically 15 qualifying *returned* supplier documents, nor proof that the required 28-source category minimum is met. That final requirement is outside this input audit.

### M5 — Q02's empty start is a bounded eligibility judgment

Q02's first ten include identifiable original publications and an official GraphPad page. The selector rejects them from their supplied topics because they do not identify the unit-keyed parser/normalization/assumption mechanism. No body was opened. This is an auditable navigation decision, with an expressly recorded uncertainty, not proof that these pages contain no relevant passage or that no supplier exists. (`common/Q02/start.json`, ranks 1–10; `common/Q02/search.json`.)

Keep Q02 in the full denominator, with no common provider for B. A Q7/Q8 explanation must say “none selected from this first-ten window under this coding,” not “no relevant original exists.” The neutral query also lacks the explicitly known `benchstat` name later present in the frozen A query; one query wording cannot isolate a general strategy effect. This limitation should remain visible even if A later succeeds.

## Predicate interpretation: checks that can overturn an easy success claim

These are scoring cautions and prospective-input sensitivities. They do not add new mandatory predicates or alter sealed text.

| Question | Substantive check | Acceptance affected |
| --- | --- | --- |
| Q01 | Frozen partial P1/P2 abstract sequence extraction before Go binding, while the caller/next action remains Go. A PHP semantic match can satisfy the abstract operation without establishing a usable bridge for Go `[]interface{}` values. Preserve the frozen-predicate score separately from **practical utility / adapter feasibility: unverified**. PHP `list` is already explicitly known. | Q2, Q6, Q8 utility/novelty |
| Q04 | The useful partial action is the native-integer write through the module's shared memory, before the export bridge is complete. `DataView`/`setInt32` is already in the first example. Support is possible, but it is known-component utility; it cannot establish a novel target, a correct Go ABI offset, or a complete export protocol. | Q2, Q6, Q8 |
| Q05 and Q08 | Q05's extra-name example has unresolved pseudocode defects; Q08's LINKS source/target direction is ambiguous. A validator or later manual must not silently fix either first draft. Hold an interpretation-dependent predicate **unverified** unless the exact adopted interpretation is separately disclosed. | Q2, Q6 |
| Q06 | Current UTF-8-mode/default documentation must still be compared with frozen P2's locale-module isolation requirement. Evidence for UTF-8 decoding alone cannot satisfy this partial conjunction. | Q6 |
| Q09 and Q10 | A different array system's “weak scalar” must preserve explicit NumPy scalar/0-D strength for Q09. Q10 requires actual NumPy ndarray producer/consumer interchange and no exchange-time data copy; a generic protocol description or a different edition's standard is insufficient. An adapter implementing the missing algorithm is core work. | Q2, Q6, Q7 |
| Q11 and Q12 | Q11 combines strict variable-width construction with ndarray indexing/scalar output; general ndarray pages alone do not demonstrate the dtype-specific guarantee, especially across stable/development editions. Q12's macro mention alone does not prove default-old targeting, hiding newer APIs, and older-runtime compatibility. All required passages must be in the actual returned packet. | Q6, Q8 |

The NumPy pre-seal revisions correctly separate several architecture alternatives from universal predicates. Reinstating those alternatives after seeing results would create a different experiment. (`streams/numpy/predicate-revisions.jsonl`.)

## Acceptance disposition for integration

| Condition | Input-audit disposition |
| --- | --- |
| 12-event ledger/period/whole-partial quotas; saved hash traversal | **Met** within the stated finite frames |
| Predicates, partial purposes, falsifiers, and literal queries sealed before common searches | **Met structurally**; practical-boundary cautions above remain |
| Sampling without prior candidate/outcome exposure | **False** under the literal strict condition |
| Every historical frame row has verified first-public timestamp and purpose | **False**; explicitly incomplete for untraversed rows |
| Complete locally stored preselection exposure receipts | **False** for the NumPy discovery response |
| Detailed common mirror/eligibility policy fully frozen before common results | **Not established**; do not mark unconditionally fulfilled |
| Twelve exact common queries; first-ten retention; common two-open ceiling | **Met** against saved receipts and stored eligibility coding |
| All 12 have a usable common original | **False**; 11/12 have recorded original-body reads, with additional navigation limitations |
| A/B actual isolation, alternation, budgets, original returns, masked adjudication, gains, and final source minima | **Unassessed here**; no route artifacts were accessed |
| Historical search effectiveness, author ignorance, real labor saving, runtime success, independent human reading | **Unverified**; independent human reading and runtime testing were not performed |

If the strict unmet conditions remain requirements in the final acceptance ledger, preserve them as false and use the prescribed completion-with-gaps status. Passing the static check does not upgrade them. A useful conclusion can still be made about the exact preserved current-web comparison, provided its denominators, exposures, version limits, and adapter uncertainties remain attached.
