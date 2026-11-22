> **F02 정정 — 2026-11-22 재개 감사:** 아래 이전 초안의 “GTFS/예정 운행 비교”라는 F02 설명은 철회됐다. 고정 SHA256 `b3e6689d94b496817a35f072d175b5b4be9149429a87d8adcaf7c8ff5e904bcc` PDF와 동일 바이트 재다운로드·로컬 렌더에는 “MTA Real Time data”가 있다. 웹 스크린샷의 다른 문구는 동일 고정 바이트의 증거가 아니다. 현재 판정은 `field/resume-field-audit.md`, `field/resume-field-correction.json`, `field/field_sources.jsonl` F02를 따른다. 실제 운행 원로그와 집계 코드를 재실행한 것은 아니다. 이 문서의 아래 과거 문장은 감사 변경 이력으로만 보존한다.

# AF-RES-033 — donor and field-source provenance audit

Date: 2026-11-22. Reviewer: separate `protocol_audit` context. Requested donor seal: `aba0565e5d992dc358c9c7913b2ad7868248db8d`.

## Finding

**The identity/read-evidence count supports 18 distinct selected provider works plus four distinct field works, for 22 qualifying non-recipient originals.** The provider split is six library, six transport, and six statistics works; the field split is two transport and two statistics works. No selected provider is duplicated by a field work.

The broader donor ledger has **36 source-ID rows but 35 work identities**, because `TX14` is an earlier edition of `T06`. The selected 18-document corpus is already unaffected by that alias. A final one-original-per-row source ledger should merge that alias into T06's edition history while preserving the sealed discovery ledger as historical evidence. The two field metadata errors identified below were repaired by root before the first remote field commit; I verified the revised values and repair receipt.

This audit establishes source identity, capture provenance, and counting boundaries. It does not independently validate every donor's semantic eligibility, every extracted section boundary, or any recipient relation judgment. The full minimum of 30 originals remains conditional on eight independently validated recipient proposals; none were inspected here.

## Access and checks

Read [donor_sources.jsonl](../donor/donor_sources.jsonl), the metadata of [corpus.jsonl](../corpus.jsonl), [field_sources.jsonl](../field/field_sources.jsonl), capture/attempt receipts, [capture_validation.json](../donor/capture_validation.json), and [corpus-seal.json](corpus-seal.json). Feature vectors were not inspected. No recipient bodies, inputs, S/R queries, rankings, or subsequent recipient outcomes were opened.

I rehashed cached files without displaying their contents: all **18 selected body hashes**, all **18 selected raw-representation hashes**, and all **eight field capture hashes** matched their ledgers. Provider metadata IDs, source URLs, and selected-body hashes agreed between the donor ledger and canonical corpus. The donor ledger and corpus bytes also matched the files at the specified seal in the local Git object database. This was not a second network reread of the remote branch.

Two concrete uncertainties justified narrow original checks: the correction/version labels in cached F03 HTML, and the date label in cached F04's dataset index. Only those relevant metadata and correction passages were examined. No new source was added and no sealed source, corpus, or recipient file was edited by this reviewer.

## Exact duplicate and edition mapping

Only the first row below is an alias between two existing donor **source IDs**. The other rows concern capture identifiers or URL representations; they must not be promoted into extra source IDs merely to increase counts.

| Existing alias or representation | Canonical source ID | Evidence and counting action |
| --- | --- | --- |
| **TX14 → T06** | **T06** | SFMTA FY 2017–FY 2030 SRTP (`/media/9314/download?inline`) is recorded as a superseded edition of the selected FY 2022–23 SRTP (`/media/33758/download?inline`). TX14 has `same_work_selected_source_id=T06` and `counted_minimum=false`. It was substantively inspected, but adds no work. Merge into T06's edition/alias record in any one-original-per-row synthesis. |
| SFMTA FY 2019–FY 2030 landing/representations | T06 work family | Edition-chain metadata explicitly says the title/date/links were discovered and the body was **not opened**. It adds neither a directly read original nor another work. No separate source ID exists to merge. |
| ABS capture **STAT-03-C4** (2020–21 edition), selected **STAT-03** (Edition 8), whole-chapter/print-section views | **S03** | The earlier Revisions section was substantively read and is already nested under `observed_prior_editions` with `counted_as_separate_document=false`. Edition 8 and the chapter/section representations belong to one National Accounts technical manual. No new source-ID merge is needed; preserve the existing nesting. |
| TransLink capture **TRANSIT-TL-03**, primary capture **TRANSIT-TL-02** | **TX05** | The short URL and long canonical Managing the Transit Network URL have different raw HTML hashes but the same extracted-body hash, `6f55ddb24f331afd2dfeb742bf3b3695b0129f5c957635aabbf956ef86401175`. The alternate is already nested in `duplicate_representations`; both belong to one excluded hub page. |
| **F03-current**, **F03-v1**, **F03-v2** | **F03** | Three captured versions of the same ONS reconciliation article. Count one field original, not three. Version chronology is detailed below. |
| **F04-index**, **F04-v1**, **F04-v2** | **F04** | Dataset index and two workbook versions describe the same ONS mid-2022/2023-geography dataset release family. Count one field original, not three. |

**Do not merge SX01 into S03:** the ABS Government Finance Statistics manual is a different work from the National Accounts manual, despite the shared publisher and similar “concepts, sources and methods” titles. SX01 remains an excluded work. Likewise F03 and F04 are distinct article/dataset works with different correction events; sharing ONS and population-estimate subject matter does not make them duplicate documents.

Repeated manifest/disposition entries for the same SFMTA URL or repeated attempts at an inaccessible URL are log events, not additional original works.

## Exact counts

| Unit | Count | Included IDs or boundary |
| --- | ---: | --- |
| Selected provider works / canonical corpus rows | **18** | L01–L06, S01–S06, T01–T06 |
| Provider split | **6 + 6 + 6** | Library, statistics, transport |
| Donor source-ID rows, including exclusions | **36** | 18 selected + 18 excluded rows |
| Donor work identities after explicit source-ID alias | **35** | 36 minus TX14→T06 |
| Additional excluded work/page identities beyond selected corpus | **17** | 18 excluded rows minus the T06 older-edition alias |
| Field source works | **4** | F01, F02, F03, F04 |
| Field split | **2 + 2** | Transport and statistics |
| Captured field representations | **8** | F01: 1; F02: 1; F03: 3; F04: 3 |
| Qualifying non-recipient minimum | **22** | 18 selected providers + 4 field works |
| All donor/field source-ID rows | **40** | 36 + 4; this is not a qualifying-original count |
| All donor/field ledger work/page identities | **39** | 35 + 4; includes excluded directories, portals, and other ineligible works |

The 497 rows in donor_attempts.jsonl are **log records**, not 497 source reads or 497 API calls. They include 390 finite-candidate disposition records, 46 official-capture records, and other discovery/screening/control events. `capture_validation.json` correctly calls its 18 excluded items a **record count** and warns about older editions; it must not be shortened to “18 additional unique original works.”

## Directly read versus merely discovered

The 18 selected sources carry substantive-read declarations and retained selected bodies. Their raw provenance is **11 native HTTP HTML captures, six native PDF captures, and one official-page web-reader transcript (L04)**. Thus “18 directly read original-source bodies” is consistent with the records; “18 native original files downloaded successfully” is too strong.

For **L04**, direct HTTP returned a 202 challenge with no usable policy body. The selected policy instead comes from the official-page reader transcript. The canonical donor row correctly points to `LIB-04.web.json` with raw hash `c810d698e613fea7990f8176bfcb5da8c2a941cb52b9c1f17eb1c895d958b615`, and selected body hash `70e625e10cc25a25feba77cc34f7feca7de29abc54b962432ca678d402681e44`. The legacy `LIB-04.capture.json` combines the failed HTTP raw-path/status with the replacement text hash and explicitly explains the fallback in its extraction field. Do not treat that receipt as evidence that the policy text was extracted from the HTTP-202 challenge bytes. Preserve the two acquisition paths when summarizing provenance.

The SFMTA 2019 edition was discovered only. TX10 records a read of a report landing page and explicitly says the linked scorecard PDF was **not** opened. Directory results, linked reports, chapters not read, and website search result snippets do not inherit a direct-read claim from their parent page. The four field rows all have successful native capture receipts; F02 additionally has a screenshot-verification log, and F04 has a stored-value comparison receipt. Hash matching establishes captured-byte identity, not independent re-performance of all semantic reading or numeric analysis.

## Field metadata defects and verified repairs

### F03: a predecessor URL was mislabeled as the corrected endpoint — resolved

The original field row set fixed_url to `/previous/v2`, while the claim about removing the older female-age group requires the later corrected capture. Targeted inspection found:

| Capture | Evidenced version role |
| --- | --- |
| F03-v1 | Original predecessor, before the February 28 figure correction; contains the subsequently corrected sentence. |
| F03-v2 | Superseded predecessor after the **2023-02-28 13:45** figure-label correction; still contains the sentence corrected on March 1. |
| F03-current | The `/previous/` request serves the current article; its canonical link is the base article URL. It records both the February 28 figure correction and **2023-03-01 10:10** sentence correction. Its captured body is hashed, but the endpoint is mutable. |

Root changed fixed_url to null, added current_read_url, and explicitly distinguished v1, v2, and the corrected current capture. I verified the revised ledger and [metadata-repairs.json](../field/metadata-repairs.json). The capture hashes and count of one original did not change. Future citations must point to the appropriate version; v2 alone does not support the March 1 corrected sentence.

### F04: correction date was called publication date — resolved

The original row used publication_date `2023-12-19`. The captured index labels **19 December 2023 09:15** as the correction/supersession timestamp. Its current release header instead displays **29 July 2026**, which also does not establish the initial workbook's publication date. Root set publication_date to null, recorded correction_date `2023-12-19`, and left original publication unverified. I verified the repair receipt and revised row. The original/corrected workbook hashes, MYE3 comparison, and source count did not change.

The receipt records a prior field-ledger hash of `87550ec2f8c4c5cedefb6df125eb84b52535de31c353c4806985e09a784071f6` and revised hash `02a0af139dd342516b4ce209a39b85d2efe9188db408bdfc58248ead3fcae64e`; both correspond to the audited before/after files.

## Claims that must remain bounded

- **Four distinct field works are not four independent deployments or four independent operators.** F01 is an MTA service-plan announcement and F02 is a separate NYC planning analysis of the same broad disruption. They are distinct source works, but share an event context. F03 and F04 are separate ONS correction objects. Count four originals across two fields; do not infer four independent operational replications.
- **F01 supports an announced deployment plan; F02 supports published schedule comparisons.** The latter's relevant figure uses GTFS. Neither alone proves actual train dispatch, actual achieved frequency, passenger outcomes, or a violation of the March announcement. Their existing limitations should remain attached in the synthesis.
- **F03 does not establish automatic rollback or downstream notification success. F04's comparison is limited to MYE3 stored cells.** It does not verify the entire workbook, the estimation system, or every downstream user. No numeric result was re-audited here.
- **Current official pointers do not prove unconditional final adoption.** T05's compiled report retains a draft-status ambiguity; T06 contains dated scenarios and proposed appendix guidance. Their ledger qualifications must survive any summary of “official policies.”
- **Latest-edition claims are bounded by the recorded search/link frame.** T06's 2022 edition is the latest found in the frozen family search, not proof that no newer document exists anywhere. Seven selected editions are dated 2025–2026 (S01, S02, S03, S04, S06, T02, T05), and seven are undated (L01–L06, S05). Current transfer plausibility must not be presented as proven availability to a 2020–2024 recipient.

## Seal and fingerprint receipt

| Artifact | Audited SHA256 | Seal relationship |
| --- | --- | --- |
| donor/donor_sources.jsonl | `ae9ae4ba64bf0dfce1385f16e1b2fd9d330f1e291dcfd9ea58f6257ed2e0cb39` | Byte-identical to the specified donor-seal Git object |
| corpus.jsonl | `8fefde80d6177674b14c90818e6c7a95e9a28e232f07edb87ed14d6b44c3df13` | Byte-identical to the specified donor-seal Git object and corpus-seal receipt |
| field/field_sources.jsonl, repaired | `02a0af139dd342516b4ce209a39b85d2efe9188db408bdfc58248ead3fcae64e` | Revised draft verified; not part of the specified donor seal |
| field/field_fetch_attempts.jsonl | `fc2a6fb2865e633b92904eea70abf6e9dfb1a3ca9b326a6c3be73ea1e2f32078` | Eight capture receipts checked against cached bytes |
| field/metadata-repairs.json | `ac38f5c22c92695683da4dc898ff70669b145f652b3d06d953af43a5f9b42227` | Verified old/new field-ledger hash and the two metadata corrections |

No later remote field seal was checked in this audit. The specified donor seal's absence of field_sources.jsonl does not establish that no later field commit exists. The remaining source-accounting action is to carry **TX14→T06** into the final one-original-per-row ledger, preserve all other version/representation nesting and read-status limits, and cite the repaired field version/date metadata.
