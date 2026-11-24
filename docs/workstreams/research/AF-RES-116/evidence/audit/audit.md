# AF-RES-116 source, recruitment, and chronology audit

## Decision and scope

**The sealed source allocation is supported: 6 natural requests + 9 definition/example/implementation works + 6 separate regression/counter-input works + 13 cross-domain works = 34 required-class works; adding 3 screening-only works gives 37.** The 195 sealed source rows are not 195 works or 195 reader opens. The first-50 recruitment frames, selected original-body hashes, and fixed document-version mapping pass independent reconstruction.

This is a source/protocol audit, not a judgment of A/B/C answers or effects. It does not establish overall DONE. The exact original JP2 for I3 remains unavailable, and the records establish consistent commit/read ordering more strongly than they establish independently timestamped remote ref-update ordering. Those qualifications must survive final status reporting. No quota deficit or demonstrated natural-case replacement was found.

- Auditor: `/root/source_protocol_audit`, separate AI audit actor supplied the parent audit task. This audit has no retained spawn receipt independently certifying context isolation; it is not a human reviewer or independent historical software execution.
- Primary audited input: remote source seal `8b57d241d88cb6c5ddf3454d2b28fa3fb46fd473`.
- Checks performed: 2026-11-24 UTC. Exact rerun time and numerical receipts are in `checks.json`; audit source reopen times are in `source-reads.jsonl`.
- Allowed writes: `evidence/audit/` only. No commits, external messages, paid APIs, or accounts.
- Not inspected: recipient event logs, trails, answers, evaluator judgments, hint text, or packet treatment text. A programmatic projection of `case_id`, `document_version`, and `start_doc_id` from the sealed packets was used solely to verify version mapping. A filename-only Git diff checked packet/authoring immutability.

## Independently checked evidence

`python -B evidence/audit/check_sources.py` independently reconstructs the recruitment frame from the saved compressed search payloads, compares the counted source inventory to its five source ledgers, checks input fingerprints, checks phase-sealed files, verifies document-version metadata, and validates archived reference bytes. It writes only its audit receipt. The existing `analysis/build_sources.py --check` also passed before the integration worker added later non-counting reopen rows. The existing `analogies/verify_analogies.py` passed after cache restoration; it was invoked without `--write-evidence` even though that script prints a fixed command string containing that option.

| Check | Observed result | Evidence |
| --- | --- | --- |
| Search payload hashes and order | Four saved searches match their receipts; each is sorted by `(created_at, number)` and reports `incomplete_results=false`. | `recruitment/receipts.json`; four `search-*.json.gz` files |
| Body-only word filter and deduplication | Reapplied the exact case-insensitive word-boundary expressions to complete saved bodies, excluded PRs, deduplicated issue numbers, and rebuilt both first-50 lists. All 100 rows and body hashes match. | `recruit.py`; `frame.csv`; `recruitment/*/first50.json`; audit checker |
| Individual original-body snapshots | All six individual issue API bodies hash to the selected-case SHA-256 and to the corresponding search body. | `cases.json`; six `recruitment/*/issue-*.json` snapshots |
| Source totals | 195 rows; 37 uniquely credited work IDs; 34 in required classes. All listed ledger input hashes match the sealed bytes. | `sources.jsonl`; `analysis/source-counts.json`; `analysis/source-inventory.csv` at `8b57d241` |
| Reference storage | 12 reference archives and all 258 archive members match their indexed lengths and SHA-256. All 14 counted representative Pandoc/ImageMagick source snapshots match their source-ledger hashes, including the TIFF mirror before normalization. | `evidence/reference-cache/index.json`; counted rows in both reference source ledgers |
| Frozen selection and authorship | Scope and recruitment files are unchanged from their own earlier seals. The later `recruitment/sealed-sources.jsonl` is byte-identical to `sources.jsonl` at the original-request seal. No authoring/packet/input filename differs between the packet and gold seals. | `7a76c8cc`, `878f2e1b`, `762fe1fc`, `8b57d241`; `checks.json` |
| Version mapping | Each case's three packets have the same prescribed version/start document; the corpus catalog maps it to the recorded upstream commit. | Sealed version metadata projection; `documents/catalog.jsonl` and `documents/metadata/*-commit.json` in the document cache |

### Recruitment and eligibility

Pandoc's reconstructed frame runs from #8518 to #8809, with the fiftieth issue created at `2023-04-26T13:57:47Z`. Its 100-result `table` search extends to `2024-02-23T10:51:18Z`, and its 100-result `image` search extends to `2023-11-18T11:39:37Z`. Both extend beyond the cutoff row, so the saved first pages are sufficient for the prescribed merge.

ImageMagick's frame runs from #5987 to #7693, with the fiftieth issue created at `2024-10-15T00:33:38Z`. The `profile` and `alpha` searches returned all 35 and 62 results respectively, and both extend past the fiftieth frame row. This verifies the specified search-frame procedure; it does not claim exhaustive recall of every public issue independently of GitHub search indexing or reconstruction of the bodies before historical edits.

I read the full original bodies of all nine screened rows, including the three exclusions. My eligibility assessment agrees with the stored selection, with the narrow interpretations below preserved.

| Project/rank | Issue | Audit assessment of the two-condition rule |
| --- | --- | --- |
| Pandoc 1 | #8518 / P1 | Eligible: Markdown-to-HTML/TOC conversion and preservation of the subordinate headings in the TOC. The keyword `image` is in a screenshot alt label; this is not itself an image-conversion case. |
| Pandoc 2 | #8522 / P2 | Eligible under the protocol's input-to-representation interpretation: consume an annotated abbreviation source while retaining its usable abbreviation set and the annotations in that single source. The request does not ask Pandoc to reproduce comments in its output, and does not establish current support. |
| Pandoc 3 | #8526 / P3 | Eligible: page rendering with figures/tables and preservation of the following text's bottom-margin flow. Original body does not specify the actual engine or command. |
| ImageMagick 1 | #5987 | Exclusion defensible: opacity classification accuracy is the requested diagnostic itself; no separate image transformation plus preserved property is stated. |
| ImageMagick 2 | #6079 | Exclusion defensible: proposes a contrast transfer function without a separate preserved property. Its embedded implementation formula is already in the original body, not an opened answer. |
| ImageMagick 3 | #6159 / I1 | Eligible: add a grayscale meta channel while preserving RGB appearance/channel semantics. The reporter's question does not establish a confirmed alpha bug. |
| ImageMagick 4 | #6187 / I2 | Eligible under the stated representation-conversion interpretation: extract the channel into an image while preserving its spatial signal. The desired preservation is close to extraction correctness; retain that limitation rather than claim an independently manipulated second variable. |
| ImageMagick 5 | #6190 | Exclusion defensible: build/delegate regression; no separately specified image-property preservation across conversion. |
| ImageMagick 6 | #6237 / I3 | Eligible as decoding into an image/channel representation while preserving its actual color/channel meaning. The author explicitly expresses uncertainty about RGBA and grayscale. Do not turn the reporter's belief into a known reference color. |

Thus the first eligible three are Pandoc ranks 1/2/3 and ImageMagick ranks 3/4/6. These are purposive semantic coding decisions within a frozen chronological frame, not a measured inter-rater reliability result. The prior recruitment reviewer inherited parent deliberations, as `recruitment/audit/screening.json.context_exposure` already discloses. Incidental later-body exposure is also disclosed and does not appear to have replaced a selected case.

### Work units and direct-read evidence

The nine definition works are the Pandoc manual; three distinct implementation families for section/TOC construction, abbreviation input, and LaTeX table generation; the ImageMagick manual; PNG 2003; JPEG 2000 T.800; TIFF 6; and Adobe's Photoshop file-format specification. I checked the three counted Pandoc implementation excerpts in the archived fixed-version source files: they implement different behavior, and the associated code/test/template files are grouped within their respective family. The count should be described as these operational work units, not nine independently authored publications.

The six regression/counter-input works are Pandoc #8741, Pandoc #7124, the conservatively merged LaTeX tools/3512–#137–#158 lineage, ImageMagick discussion #6299, discussion #7848, and issue #8022. I read the three counted Pandoc/LaTeX issue bodies in the saved primary snapshots and reopened discussion #6299 at its publisher URL. These are distinct reports/inputs. #6299 is another input in the same extra-sample mechanism as I2; it is not another independently observed fix. Issue bodies, replies, attachments, mirrors, and repeat reads receive no additional credit.

The Pandoc manual's three versions count once. All ImageMagick manual pages and three versions count once. The TIFF specification's ITU copy is explicitly debited and its Adobe-hosted copy credited once. The Eisenhower reading copy and press release count as one speech work, although they are different archival records; its index and finding guide count as one finding work. Yale's publisher item record counts as cataloging, while the unread original letter does not count as a directly read manuscript.

Direct-read support is not inferred from download success. The Pandoc representative rows resolve to actual display events, including substantive intervals at `read-log.jsonl` rows 33, 36, 46, 51–53, and 57. The ImageMagick ledger retains truncated displays and subsequent narrow rereads; its counted representatives have non-truncated substantive reads. Cross-domain entries identify read method, tool reference, section, status, and timestamp meaning. The reference-cache hashes establish which saved bytes are available, not that a person read every cached byte.

For independent spot checks I reopened the Adobe specification's TIFF table and the Prusa maintenance article's applicability/axes sections, plus ImageMagick discussion #6299. These match the narrow source-ledger claims. Raw Pandoc source and GitHub blob/release URLs returned `DisabledError` through this audit's web route; the fixed source excerpt and saved official release API payload were checked locally instead. All audit reopens receive zero new unique-work credit. Full addresses, returned addresses, UTC bounds, sections, failed attempts, and limits are in `source-reads.jsonl`.

## Fixed versions

| Case | Prescribed version | Upstream commit | Basis |
| --- | --- | --- | --- |
| P1 | 2.19.2 | `53325aa2e37a976e5a20d8fc2a662070a04e90a9` | Explicit original version |
| P2 | 3.8.3 | `568dab14533940ecee16824097400f1eabf13869` | No original version; maximum stable published release at or before the cutoff in the saved 100-release API payload |
| P3 | 2.14.0.3 | `227f675cc46a680d4b8f2fd71e0c4cbb92a3fd0b` | Explicit original version, retaining the original `andoc` typo separately |
| I1 | 7.1.1-3 | `c5d5e7117fb07096158bcad05e1086f0c2fff172` | Original `7.1.1.3` normalized to official tag syntax |
| I2 | 7.1.1-4 | `10ad43dc3e5113fa1969a55583a080c5a6a23f65` | Explicit failing version; older reported versions remain comparison reports |
| I3 | 7.1.1-6 | `b2dd67b1681e23d0e0b9769d81bed23f05129e2a` | Original `7.1.1.6` normalized to official tag syntax |

The pinned manual source version is not the installed rendering/runtime version. Pandoc's historical MANUAL.txt files were rendered with installed Pandoc 3.1.11.1 and then converted into a local text view. This is already explicit in `viewer/corpus-build.json`; the audit does not elevate it to a historical browser or historical binary reconstruction.

## Chronology

| Phase | Recorded evidence | Assessment |
| --- | --- | --- |
| Cross-domain supplement begins | First direct read `2026-11-24T03:57:08Z`; `analogies/metrics-analogies.json` window ends 04:11:37Z | Exploratory supplemental reading begins before the main protocol commit. It is separately scoped and not a natural A/B/C trial. |
| Protocol commit | `7a76c8cc`, Git author/committer time 03:59:40Z | Predates saved search captures and first original-body read; scope bytes remain unchanged. |
| Recruitment | Search starts 04:00:11Z; first complete-body display 04:01:57Z; request seal `878f2e1b` commit time 04:05:57Z | Stored sequence is consistent with protocol-first natural recruitment. |
| Author exposure | Requests 04:10:19Z; TOC-only attempts 04:13:02Z/04:13:40Z; own output frozen 04:19:40Z | Exact size of the first truncated TOC display is unknown and already corrected; no manual-body/gold exposure is recorded for the author. |
| Corpus and packet commits | `27bdf61a` at 04:19:12Z; `762fe1fc` at 04:22:19Z | Fixed packets precede the first logged natural-reference reading and do not change before the gold seal. |
| Reference work | Pandoc request read 04:24:21Z; ImageMagick request read 04:24:44Z; substantive document reads follow | Consistent with packet-before-gold reading. These readers are separate actors with procedural, not OS, isolation. |
| Gold/source commit | `8b57d241` at 04:54:50Z | Immutable audit baseline. Its later resume inventory entry is explicitly not the original verification timestamp. |

The `seals.jsonl` protocol record was written at 04:04:25Z, after the first capture/read. Its commit identifies earlier content, but it is not itself an independently sampled timestamp of the original remote ref update. Likewise packet/corpus seal notes were recorded at 04:25:09Z. The file-based audit can verify the consistent stored ordering, commit ancestry, unchanged bytes, and the actors' declared exposures; it cannot independently reconstruct unavailable original tool transcripts or certify the second at which an earlier remote ref was updated. No contradictory natural-source exposure was found.

## Findings and minimum resolution

### A01 — Same-work identifiers were split across non-counting rows

**Severity: low; metadata consistency; no quota change.** At the audited seal, counted natural request rows 1–6 in `sources.jsonl` use GitHub issue URLs as work IDs, while their repeated body/comment/attachment records use `natural-pandoc-8518/8522/8526` and `im-issue-6159/6187/6237`. Row 170 (`ROOT-AN-02`) uses `eisenhower_guide` after normalization, while the counted finding work at row 152 is `eisenhower_finding`. All repeats have `unique_counted=false`, so these splits do not inflate the 37/34 totals.

Minimum resolution: normalize those seven aliases to the existing counted work IDs in the consolidation builder, rebuild, and verify that no unique-count flag changes. Preserve the sealed raw ledgers. **Resolved during integration:** all seven aliases now map to the existing counted IDs. Audit readback confirmed that changes among the original consolidated rows are confined to work-ID normalization and the unique count stays 37. `evidence/audit-resolutions.json` records the correction; the historical baseline remains intact.

### A02 — Pre-protocol cross-domain reading needs an explicit chronology label

**Severity: low; reporting qualification; no natural-sample or quota penalty.** `analogies/sources-analogies.jsonl` rows 3/9/16/18/19/25/32 include reads before the main protocol commit. The separate actor reports no exposure to natural cases, hints, gold, or recipient trails; root repeat verification is later. It would nevertheless overstate the record to call all source collection preregistered or all research reading post-packet.

Minimum resolution: label the cross-domain layer exploratory and separately scoped in the final report/chronology. Do not retroactively alter its real timestamps or treat it as natural-outcome evidence. The existing analogies report already keeps its evidentiary role separate; add the explicit timing qualification where the overall study order is described.

### A03 — Exact pre-read remote-update timing is not independently proved by the saved receipt

**Severity: medium provenance limitation, not a demonstrated order violation.** `evidence/seals.jsonl` row 1 records its protocol note at 04:04:25Z; `recruitment/receipts.json` starts at 04:00:11Z, and original-body read logs start at 04:01:57Z. Git commit metadata places the protocol at 03:59:40Z and the immutable contents agree, but the preserved artifact does not contain the original provider-side update-ref response with an independently observed pre-read timestamp.

Minimum resolution: if the original time-bound connector receipt is retained, preserve/link it; otherwise state that the audit verifies stored commit/read consistency and content immutability, with original remote-upload timing not independently re-proven. Do not fabricate a timestamp or describe this audit as observing the original sealing event. If an independently timestamped remote-before-read receipt is a strict DONE gate, this remains an unverified gate.

### A04 — I3's exact original-input evidence remains missing

**Severity: material source limitation; explicitly unresolved.** The original JP2 HTTP/HTTPS attachment and its original publishing directory returned 404 according to `gold-work/imagemagick/gold.json` I3 original-input retrieval records; `target-spans.json` still names `required_unavailable_input`. The corresponding original body is present and eligible, so this is not an unfilled natural request. What is missing is the file-level evidence for its actual color/component semantics. T.800, the NRW product-family document, and fixed implementation source do not substitute for those exact bytes.

Minimum resolution for a stronger file-specific conclusion: recover an authenticated original/same-file copy, record its hash, inspect its JP2 boxes/codestream and exact tile/band definition, and keep historical execution claims bounded by the actual tested runtime. Until then retain the explicit unknown and distinguish a completed search/reading exercise from complete reconstruction of all original-case facts. Source quotas alone cannot justify calling this gap closed. The audit does not prescribe a replacement case or judge any recipient answer.

Historical binaries, actual human time savings, and original-author adoption are explicitly outside the current observation claim and are not newly imposed completion gates. The unavailable Yale original is also correctly excluded from manuscript credit; a separate Eisenhower original-reading example exists, so that Yale failure does not create a cross-domain quota deficit.

### A05 — P3's original rendering invocation is unspecified

**Severity: material source limitation; explicitly unresolved.** `cases.json` P3 preserves the original body's lack of output format/engine/command. `gold-work/pandoc/gold.json` P3 `known_gaps` also records missing engine/version, template, TeX distribution/longtable version, and which YAML format was actually used. The Pandoc manual version is correctly fixed, but that does not identify the full original rendering environment. The separate 2021 longtable source is explicitly a comparison version, not a verified record of the reporter's installation.

Minimum resolution for a stronger original-case reconstruction: recover the original invocation and relevant renderer/package/template identities, or retain the unresolved branch in the final result. This is distinct from imposing a new requirement to execute every historical binary. The source quota and the six-case recruitment count remain fulfilled.

## Audit boundary for completion reporting

The allocation, chronological search-frame reconstruction, chosen-case linkage, stored exposure order, and fixed-version mapping are supported within the stated limits. The audit supports reporting those concrete checks as complete. Complete reconstruction of all original-case facts remains **PARTIAL** because the I3 file-level evidence and P3 rendering environment are unresolved. It does not support an unqualified claim that every original input was recovered, that the full study was prospectively registered before any supplemental reading, that original remote upload timing was independently observed here, or that A/B/C had any particular effect. The integration worker acknowledged these limits and plans to distinguish the completed recruitment/observation/accounting work from those unresolved original-case facts; this audit has not inspected the observation outcomes.
