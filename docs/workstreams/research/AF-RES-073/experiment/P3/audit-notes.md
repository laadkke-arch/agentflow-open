# P3 original-experiment audit notes

Checked UTC: 2026-11-23 10:28:45 UTC. Worker: /root/recruit_mep, same model with inherited task context; not an independent human or blinded participant. No Git mutation or post-search historical retrieval was performed by this worker.

## Frozen evidence and derived counts

The raw files are frozen at the parent's request. This note reports corrections without rewriting them.

| Arm | Searches | Document operations | Total cost | Ranked slots | Directly read URLs | Conservatively counted original works | Deferred proposal slots | Unread slots | Jointly eligible | Target execution |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| C | 2 | 6 | 8 | 10 | 6 | 5 | 2 | 2 | 0 | Not performed |
| A | 2 | 6 | 8 | 10 | 6 | 2 | 3 | 0 | 0 | Not performed |
| B | 2 | 6 | 8 | 10 | 5 | 4 | 0 | 4 | 0 | Not performed |

Total: 30 ranked slots, 6 searches, 18 document operations, 18 source-attempt rows, 17 direct-read URL receipts, 11 conservatively counted independent originals, 25 automatically exposed results beyond first five. A has one exact duplicate ranked URL linked to its earlier open. B has one rewritten-summary-only access limitation. There were no HTTP failure responses and no retries. Every arm has the same total cost of 8, so no observed eligible benefit disappears when truncated to equal total cost: all three counts remain zero. Zero eligible results is observed; target application is unmeasured.

### Corrections for central normalization

1. C uses `unread_budget_exhausted` for Q1R5 and Q2R5; B uses `unread_budget`. These describe the same unread state. C/checkpoint.json accidentally counted only the latter spelling and reports unread=0; the correct C value is 2. The P3/summary.json total unread=6 is correct.
2. In C's judgments, unread rows retain search-return cumulative cost 1/2, while B's unread judgments use arm-end cost 8. The rank receipt's `cumulative_cost` records retrieval time; an unopened candidate has no read cost. Normalize central judgment reporting to `read_cost=null; arm_end_cost=8`, retaining the original fields for provenance. All actual operations already have the exact sequence 1..8.
3. C-O5's 2026-11-23 last-updated value is only the observed revision time. No first-publication history was retrieved; availability at the 2023 proposal is unknown. The frozen sources already contain this distinction.
4. C-O3 publisher attribution is only JSON Schema project; named individual authors were removed because their names were not shown in the returned section. The frozen sources reflect the correction.
5. The COPIM DOI open explicitly said `rewritten summary` and reported a redirected landing URL. B-O5 is not a directly read original and does not count toward the minimum or technical candidate evidence. Its single operation still costs 1.
6. B-O6 is directly read but explicitly fictional educational cases plus secondary standards explanation. It does not count as a real operational case or original technical source. No technical assertion is adopted from its W3C summary.

## Interpretation available before any post-seal outcomes

A returned the existing nbformat implementation and Jupyter schema registry. These are two conservative implementation lineages, despite six opened URLs. A-O2's raw v4.5 schema rejects an added root property under direct strict schema evaluation. That is a static counterexample to automatic validation compatibility, not an executed old-reader result. The existing nbbase pair-to-file map is a more immediate baseline than a new analogy.

C restored document, writer, validator and legacy-client types and returned explicit schema/publication/migration rules. OMI's two locale URLs are one work. No C source establishes both retained nbformat fields for an old notebook reader and an immutable one-to-one canonical URI map for the same notebook configuration. The stronger wording improves the type of returned documents here; it does not demonstrate an eligible design gain.

B moved readers toward people and labels toward concepts/citations. Its VTML original design supplies a concrete legacy-client projection mechanism; Ariadne supplies maintained alias equivalence and identity-versus-retrieval distinctions. These are useful comparison mechanisms, but neither proves the notebook conditions. B therefore also contains useful principle evidence; object restoration should not be described as universally superior.

The original design paper VTML incidentally states that a minimal parser was available (B-O3, returned L231). No linked implementation test, release, subsequent decision or historical query was opened. This incidental statement is recorded but is not a measured adoption outcome.

The B returns do not replace the assignment's separate post-seal reads of two independent nonsoftware operational cases. No such post-seal read was done by this worker.

## Reproducible local verification

Executed by /root/recruit_mep with `python -B -` against only the P3 frozen files; exit code 0. Checks: 30 unique rank IDs, 30 matching judgment IDs, 22 judgment columns, 54 unique run event IDs, 18 unique source IDs, every open connected to a source, each arm exactly 2 searches and 6 opens with cost sequence 1..8. Original works deduplicate to 11 under the conservative work IDs. This was ledger checking, not a target notebook test.

The next external investigation should be done only after the parent's raw seal: historical old-reader/validator configuration and original publication/maintainer records. Preserve these original ranks and numerator values.
