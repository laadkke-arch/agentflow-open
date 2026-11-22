# Observation assembly

`assemble_observations.py` is an offline provenance/counter assembler. It assigns no semantic success, selects no candidate, and changes no original source, receipt, route record, return, or seal.

Run `python -B docs/workstreams/research/AF-RES-029/assemble_observations.py --allow-incomplete` for an in-memory schema check. This mode always writes **no global ledgers**, even when all packets happen to exist. The default run requires all twelve common packets, twenty-four A/B packets, their route/source files, and verified input/common/route seals; every return must belong to its appropriate seal. `--check-only` applies the complete default gates without writing. A repeated run is byte-identical for identical inputs. A differing existing generated output is rejected unless `--replace-generated` is explicitly supplied.

## Outputs

| File | Rows and preservation rule |
| --- | --- |
| `sources.jsonl` | Directly read substantive originals, including uncounted duplicate editions and reused frozen first texts. Every row retains `original_record`, the original count flags, original duplicate group, source-file line/hash, and receipt references. |
| `attempts.jsonl` | Every remaining original source row: snippets, failures, metadata, provenance/recovery, navigation-only indices, locators, and ambiguous readings. Ambiguous direct reading is `미확인`; no row is silently discarded or promoted. |
| `routes.jsonl` | Exactly 36 observations: twelve common-only C and twenty-four A/B. Frozen input/selection provenance, original route records, actual receipt counters, declared counters, caps, and original return-file hashes. |
| `visits.jsonl` | One row per actual recorded experimental web operation. An operation with both navigation and body debits remains one row. Search/index/body attempts, exact retries, failures, and charged within-page finds remain visible. Local cache reads/common reuse add no requests. |
| `returns.jsonl` | Exact parsed copies of all 36 originally gated packets, adding only `source_file` and `source_sha256`. No clipping, reordering, reranking, replacement, or reserialization-gate alteration. Original file hashes preserve byte provenance. |
| `evidence/observation-assembly.json` | Input/output hashes, row counts, twelve independent events versus 36 observations, actual caps, source category minima, all duplicate groups, citation/source-URL associations, missing metadata, warnings, and cost sensitivity. |

## Normalization and counting

Source rows expose standard fields for identity/type/publisher, original URL, version, date, UTC, actually read sections, finding, limitations, linked question/route/stage, receipts, and eligibility. Missing values are `미확인`. The full unmodified input row is preserved under `original_record`, so alias normalization never destroys a field. The common odd/even and A/B variants are supported: `url`/`original_url`; `kind`/`type`; `verified`/`finding`/`verified_finding`; `read_sections`/`directly_read_sections`; all recorded receipt aliases; and boolean or object eligibility fields.

Two identities deliberately serve different purposes. Citation membership uses sealed source IDs or edition-preserving document URLs, removing only fragments/tracking and normalizing exact GitHub raw/blob copies. Conservative source counts additionally collapse NumPy edition aliases/source-rendered paths, Python manual editions/source-rendered chapters, and official Go runtime HACKING mirrors. Distinct API or manual paths stay distinct. Original URLs, versions, groups, and normalization notes remain available. Grouping never authorizes combining incompatible versions as semantic evidence.

The initial twelve exact `counted=true` aggregate flags are kept separate. Reused first texts add no first-design or supplier count. The primary supplier minimum requires a directly read original, an explicit original eligible flag, and actual A/B returned citation membership. False or absent eligibility flags are never promoted, including duplicate rows; another qualifying row can represent the same document group. Each qualifying document group counts once. C-only suppliers are a separate sensitivity. Post-seal cross-field/supplementary sources are outside this assembler and cannot add original route wins.

`actual_returned_line_ranges` is calculated only from line markers literally present in saved responses, never from reported total line counts. Server transfer bytes and token costs are `미계측`; saved UTF-8 text/JSON/file byte sizes are recorded separately. Source records can preserve worker-provided section claims, but the returned ranges remain the independently reproducible delivery boundary.

The cost sensitivity leaves original debits and packets intact and reports `nav_if_find_is_navigation`: declared operation navigation debits plus one for each within-page find that had a zero navigation debit. A/B routes exceeding two under that alternative are flagged separately from the main recorded budget.

## Limits

The assembler verifies provenance and explicit counters, not supplier behavior, citation sufficiency, historical availability, novelty, runtime behavior, selector independence, or semantic verdicts. It requires per-operation receipts with one web command each; a batched receipt without operation-specific debits is rejected rather than divided by assumption. It reports consumed files absent from the three seal maps. It does not create substitute source summaries or count search metadata as supplier originals.
