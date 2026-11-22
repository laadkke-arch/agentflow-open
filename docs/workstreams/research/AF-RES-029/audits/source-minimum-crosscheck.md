# AF-RES-029 — exposed source minimum cross-check

## Result

**The qualified minimum is verified: 12 first-design groups + 32 distinct A/B-cited supplier groups + 5 cross-field groups = 49 groups.** The three sets are disjoint. The 32 supplier groups were independently reconstructed from eligible source rows and the assembly's A/B citation associations, rather than obtained by adding row or citation counts.

The original 121 source rows are intact. Their exact 669,531-byte prefix has SHA-256 `720e7ae68a9159e984e146e38eed9ee2b86c33ea50386e2b42e4e03c978a290c`, matching the original output recorded in `evidence/observation-assembly.json`. The final thirteen rows equal `supplementary/sources.jsonl` byte for byte.

This is a separate exposed provenance audit after reader 2's initial judgments were sealed. It did not change those judgments, original ledgers, or source-count files. It read the four requested files only; no new web research, raw route-return reopening, or other reader judgments were used.

## Qualified counts

| Category | Observed groups | Required minimum | Result |
|---|---:|---:|---|
| First designs | 12 | 12 | Pass |
| Direct supplier groups actually cited by A/B | 32 | 12 | Pass |
| Cross-field official original documents | 5 | 4 | Pass |
| Disjoint qualified union | 49 | 28 | Pass |

Each first design retains its explicit original `counted=true` flag, exact initial eligibility, and recorded direct-read status; the set covers Q01–Q12 once each. The four Go designs retain the disclosed third-party GHArchive capture basis. This audit does not turn those captures into official-hosted immutable pages.

For each of the 32 supplier groups, at least one eligible direct-original row has an A/B citation witness in `observation-assembly.json.source_URL_associations`. The witness names an exact document URL and section, points to the corresponding source row, and carries a return hash matching the assembly's sealed input hash map. The independently derived group set exactly equals the set marked `counted_supplier_AB_minimum`. Citation membership is a provenance fact; it does not establish that the citation satisfies a frozen behavior predicate.

The five cross-field sources are the Met API manual, the Met individual artwork record, the Hammond family catalog, the Hammond individual part page, and its engineering drawing. These are distinct documents with different content/functions. A catalog, item description, and drawing about one product are not automatically mirrors. The recorded differences between their dimensional/fastener statements are not resolved by this count.

## Why 64 should not be reported as a validated direct-original total

`all_direct_document_groups: 64` is mechanically reproducible as the set of `duplicate_group` values on rows labeled `direct_read=true`. The problem is not inflation from repeated rows:

- Fourteen first-design reuse rows fall into the same twelve first-design groups and add **zero** groups.
- Multiple editions, source/rendered copies, and the Go HACKING mirrors are grouped together. Eight groups contain multiple observed URLs and each contributes one group.
- Of eight non-cross-field supplementary rows, seven reuse existing groups and add **zero** groups. Only the tagged `typing_extensions.Doc` source is a new group.
- The prefix has 58 raw groups. Five cross-field documents plus the one new supplementary document bring the raw union to 64.

The problem is that five groups have no true original count-eligibility flag, despite their aggregate `direct_read=true` value:

| Source rows | Group/content | Why the raw direct count needs qualification |
|---|---|---|
| 38 | `Q04-A-S1`, Go compiler `doc.go` | Real compiler documentation was returned, but the requested wasm export contract was absent and the original count flag is false. This is conservative exclusion, not a claim that no text was read. |
| 58 | `Q06-A-S1`, CPython `io.rst` | The ledger explicitly says only page chrome and line-number scaffolding were delivered; no supplier I/O body. |
| 77 | `Q08-A-S3`, Vercel `installer.ts` | The ledger explicitly says only GitHub chrome/line-number scaffolding was delivered; no installer source body. |
| 107, 112 | NumPy `routines.dtypes` index | Type/family index and class name; original count eligibility is false. |
| 111 | NumPy fundamentals index | Explicitly navigation/index metadata only; original count eligibility is false. |

A conservative broader inventory is therefore **59 groups**, defined as: first designs plus pre-seal supplier groups with at least one explicit true original eligibility flag and recorded direct read, unioned with the separately identified supplementary documents. Its decomposition is **12 + 41 + 5 + 1 = 59**; the last term is the new post-seal typing source. Equivalently, it is the 49 qualified groups plus nine eligible but uncited contextual supplier groups and one new supplementary group.

This 59 is a conservative provenance-ledger inventory, not a new independent substantive reread of every body. The preferred main figure remains **49 qualified document groups**. If 64 is retained for an operational inventory, label it “raw distinct group identifiers among rows marked direct_read,” with the exclusions disclosed. Do not call it 64 qualified or independently validated substantive originals.

## Supplementary metadata

All thirteen rows have a URL, observed version or identity, date or explicit unknown, a valid UTC timestamp, nonempty read sections, finding, limitations, question links, group identifier, and boolean eligibility flags. All thirteen explicitly mark the publication/release date as unknown rather than inventing one. All have initial and A/B minimum flags set to false; exactly five cross-field rows have the cross-field minimum flag set to true.

There is one identifier warning: the five cross-field rows use `linked_questions: ["Q7", "Q8"]`, whereas sampled design events use `Q01` through `Q12`. They may refer to task subquestions 7 and 8, but that namespace is not explicit in these records. Clarify the namespace rather than silently padding or rewriting them. Field presence passes; canonical design-event linkage is unresolved for those five rows. The group totals do not depend on that ambiguity.

| Supplementary rows | Source IDs | Count treatment |
|---|---|---|
| 1–5 | X-MET-OPS, X-MET-ITEM, X-HAM-CATALOG, X-HAM-ITEM, X-HAM-DRAWING | Five new cross-field groups |
| 6–8 | X-MDN-DATAVIEW, X-MDN-MEMORY, X-CPY-LOCALE | Existing groups; rereads add no groups |
| 9 | X-TYPING-DOC | One new post-seal group; excluded from original A/B minimum |
| 10–13 | X-NP-FROMDLPACK, X-NP-INTEROP, X-NP-DOWNSTREAM, X-NP-STRINGS | Existing groups; rereads add no groups |

## Per-question coverage caveat

The global supplier union of 32 is correct, but `source-counts.json.by_question` is not consistently a per-question coverage count. Q09 is listed with two groups; it has **three** eligible A/B-cited supplier groups. The NumPy C-array API document group `D-ba20166dd6d1513fd060` is cited for both Q09 and Q12, while its single global counted representative row is assigned to Q12.

All other stored per-question A/B figures match eligible same-question citation membership. Summing actual per-question memberships gives 33; deduplicating the shared group globally gives 32. Either report Q09 as three and explain that per-question totals overlap, or relabel the existing figures as globally allocated representative-group counts. Do not infer that Q09 lacks the shared cited source.

## Audit boundaries and artifacts

The JSON companion records input hashes, all twelve first-design checks, each of the 32 supplier groups with citation witnesses, the five cross-field sources, per-row checks for all thirteen supplements, raw/conservative group calculations, exact append hashes, and the per-question comparison. No source or original ledger was edited. The initial masked judgments remain sealed and separate.

Counts describe documented reading/citation provenance. They do not imply successful candidate behavior, historical availability, original-author ignorance, or saved implementation effort. Edition collapsing is for conservative counting only and does not permit combining incompatible versions into one supported implementation.
