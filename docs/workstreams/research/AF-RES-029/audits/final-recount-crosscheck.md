# AF-RES-029 — independent exposed recount crosscheck

Completed 2026-11-22T13:23:28.328167+00:00. This is a same-model exposed verification, not independent human adjudication. The calculation did not read, import or invoke `recount.py`, make web requests, or modify existing data or initial reader judgments. Exact input hashes are preserved in the JSON.

## Verdict

All **2,427 arithmetic comparisons** matched the audited `pairs.csv` and `evidence/report-facts.json` snapshot. Direct predicate aggregation also agrees with every recorded candidate verdict. A separate response-classification problem remains: twelve visit classifications should change when substantive supplier text is distinguished from metadata/navigation. Those proposals are detailed below and do not alter semantic success, requests, debits, failures, URL limits or unique-source eligibility.

## Event and predicate totals

| Surface | C | A | B |
|---|---:|---:|---:|
| Partial, opened | 3 | 5 | 3 |
| Partial, returned, up to three URLs | 2 | 4 | 3 |
| Whole, opened | 0 | 0 | 0 |
| Whole, returned | 0 | 0 | 0 |
| Partial, first URL, initial reader interpretation | 2 | 2 | 3 |
| Partial, first URL, R01 strict interpretation | 2 | 2 | 2 |
| Whole, first URL | 0 | 0 | 0 |

The denominator is **12 independent design events**, with **36 C/A/B observations, 44 candidates, 381 predicate rows and 762 opened/returned surface judgments**. Seven observations are empty: C/Q02; A/Q03, Q06, Q07; and B/Q02, Q03, Q07. Unknown and empty observations remain in the event denominator.

The maximum-three returned successes are C: Q01/Q09; A: Q01/Q04/Q09/Q10; B: Q01/Q09/Q11. All three routes additionally support Q11 on the opened surface. Therefore **Q11-C and Q11-A lose success through their exact returned citations**: two route observations of one event, not two independent events.

R01 changes only Q11-B first-URL sufficiency for P03. The initial result remains **C2/A2/B3**, the strict first-URL result is **C2/A2/B2**, and full returned support remains **C2/A4/B3**. First documents were reconstructed from raw candidates sorted by original rank and from their citation order, then checked against the key. Shuffled packet order was not used, and the best available URL was not substituted.

| Candidate verdicts | Supported | Unverified | Conflict |
|---|---:|---:|---:|
| Partial, opened | 17 | 20 | 7 |
| Partial, returned | 14 | 23 | 7 |
| Whole, opened | 0 | 26 | 18 |
| Whole, returned | 0 | 26 | 18 |

The opened predicate surface contains 114 supported, 232 unverified and 35 conflict judgments. The returned surface contains 102 supported, 244 unverified and 35 conflict judgments. Each sums to 381. Novelty labels across the 44 candidates comprise 5 new targets, 5 new components in named families, 33 same named uses and 1 unverified. Novelty does not itself establish completion.

## Source and row headlines

| Count | Independently recomputed |
|---|---:|---:|
| First-design groups | 12 |
| Returned A/B supplier groups | 32 |
| Cross-field groups / cases | 5 / 2 |
| Required union of these groups | 49 |
| All qualified direct document groups | 59 |
| Groups with a raw direct-read flag | 64 |
| Source rows | 134 |
| Attempt rows | 661 |
| Experimental web operations | 116 |

The returned A/B minimum was independently computed by matching actual raw-return source IDs to explicitly eligible source records and deduplicating conservative document groups. It yields 32 and agrees with the published counted flags. The required union comprises 12 first-design groups, 32 supplier groups and 5 cross-field groups, without overlap in that union. All twelve per-question source-count rows match. The JSON identifies the five groups excluded from the raw direct-flag count.

The 661 attempt rows include discovery hits, excluded/provenance entries and post-seal attempts. They do not represent 661 distinct originals or web calls. Source-minimum eligibility is a separate decision from response-body classification: a substantive paragraph may be excluded from the required returned-source minimum, while repeated responses never create new document groups. The two post-seal cross-field cases do not enlarge the twelve-event denominator.

## Raw request and budget verification

| Metric | C | A | B |
|---|---:|---:|---:|
| Web operations | 34 | 52 | 30 |
| Declared navigation debits | 12 | 24 | 18 |
| Body-open debits | 22 | 28 | 29 |
| Dual-debit operations | 0 | 0 | 17 |
| Within-document find operations | 0 | 1 | 5 |
| Failed fetches | 1 | 0 | 4 |
| Invocation-time sum, ms | 17,362 | 21,353 | 13,128 |

All 24 A/B observations satisfy the originally declared navigation/body limits and the three-document URL cap. Treating each find as navigation leaves **20 compliant A/B observations** and four violations: **Q06-B, Q07-B, Q09-A and Q11-B**. Q05-B uses a find but remains within the stricter limit.

The eight compliant A/B pairs are **Q01, Q02, Q03, Q04, Q05, Q08, Q10 and Q12**. Their maximum-three returned partial totals are C1/A3/B1. Every raw request receipt was matched to its visit record. Debits and fetch failures match. A failed find still consumes its recorded operation/debit; cached common reuse adds no new request. Invocation-time sums are not wall-clock labor, and saved serialization sizes do not measure network transfer or token cost.

## Proposed visit-classification overlay

The initially requested minimum is confirmed: A/Q06 open-1/open-2 and A/Q08 open-3 are scaffolds, and B/Q03 request-1 contains substantive Go specification text. Those four changes alone would give A25 substantive/3 metadata and B11/15. Raw inspection establishes eight additional corrections, so that minimum would leave known classification errors.

The criterion is content actually delivered. A locator/find may return an API contract; a page serving as an index may include normative clauses. Failure to establish the frozen behavior does not turn supplier body text into metadata. Conversely, a generic introduction explaining what linked documents cover, followed only by links, remains navigation.

| Visit ID | Receipt | Proposed class | Actual delivered evidence |
|---|---|---|---|
| V-897ba26342f8e941 | routes/A/Q06/open-1.json | Metadata/unusable | L0–1395, L1370–1395: GitHub chrome and line-number scaffold only; Q06-A-S1 explicitly records no I/O body and counted_eligibility=false. |
| V-273d2b7e42123b74 | routes/A/Q06/open-2.json | Metadata/unusable | L0–1382, L1360–1382: GitHub chrome and line-number scaffold only; Q06-A-S2 explicitly records no locale API body and counted_eligibility=false. |
| V-8379c4ee7201c9d8 | routes/A/Q08/open-3.json | Metadata/unusable | L0–1401, L1380–1401: GitHub chrome and numeric scaffold only; Q08-A-S3 records no installer source body. |
| V-abcccd49f4f24845 | routes/B/Q03/request-1.json | Substantive | L423–434: Official Go specification states variable, static/dynamic type and interface-value contracts. No map-detector evidence is needed to classify this as substantive body. |
| V-aa2c8546681316fc | routes/B/Q05/request-1.json | Substantive | L300–319: Official Python data model supplies a module.__name__/__spec__ example and API contract. Q05-B-S1 records this as an original type-reference receipt. |
| V-0293c83a3117816d | routes/B/Q05/request-2.json | Substantive | L826–842: Official data model supplies reflected-comparison and object.__hash__ contracts, an implementation example and limitations. Repeated-document source counting is separate. |
| V-f39245bdce0407b6 | routes/B/Q06/request-3.json | Substantive | L693–725: The find response actually delivers open() signature, file/text mode, default encoding and explicit encoding=locale. Source exclusion as a locator/repeated document does not make delivered API text metadata. |
| V-4b6bca762b14f0f3 | routes/B/Q07/request-3.json | Substantive | L1047–1063: Official typing documentation supplies get_type_hints(include_extras=True) and runtime __metadata__ retrieval with examples; Q07-B-S3 also records these findings. |
| V-84a331d55d5ecd73 | routes/B/Q09/request-1.json | Substantive | L38–43: The array-object index also supplies a substantive N-D ndarray, homogeneous-item, dtype and indexed-scalar contract. An index role does not erase behavioral paragraphs. |
| V-f1bcbb7616223db1 | routes/B/Q09/request-3.json | Substantive | L210–227, L417–421: The dtype reference supplies conversion, byte-order and structured-type behavior with construction examples; Q09-B-S3 marks original_type_reference and count_eligibility=true. |
| V-ab0156eb646e63e4 | routes/B/Q10/request-2.json | Substantive | L52–65: The API index states normative positional/keyword-only, broadcasting, dtype, promotion and IEEE rules. These are substantive specification clauses. |
| V-3cafc14e5be77f9f | routes/B/Q11/request-1.json | Metadata/unusable | L44–57: Fundamentals page has a generic navigation introduction and links only. Source explicitly excludes navigation/index metadata; original navigation1/body0 debits remain. |

All twelve proposals produce:

| Route | Published substantive / metadata | Proposed substantive / metadata | Fetch failures, unchanged |
|---|---:|---:|---:|
| C | 20 / 1 | 20 / 1 | 1 |
| A | 28 / 0 | 25 / 3 | 0 |
| B | 10 / 16 | 17 / 9 | 4 |

B has eight upgrades and one downgrade, for a net gain of seven substantive responses. A has three downgrades. B/Q11 request-1 retains navigation debit 1 and body-open debit 0; only its received text is reclassified. A navigation call can receive a page body, so response classifications are not automatically equal to body-open debit counts.

The JSON gives every exact visit ID, receipt hash, before/after classification, line evidence and protected navigation/body/failure values. **Only `substantive_original_body_read` and `metadata_or_unusable_body_response` are proposed to change.** Requests, debits, failures, URL caps, source eligibility, duplicate groups, required source counts, initial reader verdicts and R01 remain unchanged. The root may record an append-only overlay; this audit applies none.

## Scope and preservation

The check covers event partial/whole opened/returned results and negative-status labels; strict and initial top-one results; candidate counts, empties and novelty indicators; raw request/debit/time/URL totals; pair outcomes and increments; candidate/predicate/novelty counts; source headlines and per-question counts; strict-find compliance; and the arithmetic of 25 report strata. Known-provider/external-provider labels and the historical membership of exposure/prior-overlap exclusions were not independently re-adjudicated. The stratum arithmetic uses the stated event subsets.

All initial reader hashes match the report inputs. Any subsequent overlay or report regeneration should be identified as later than this audited snapshot. This audit establishes arithmetic agreement and identifies classification corrections; it supplies no runtime result or historical author-knowledge claim.
