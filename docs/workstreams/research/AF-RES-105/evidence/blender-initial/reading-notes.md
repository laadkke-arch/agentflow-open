# Blender initial-only reading notes

## Fixed recruitment and actual reading

`site=blender, tagged=geometry-nodes`, current tags, creation ascending, UTC2024-01-01 through2024-06-30, page1/pagesize80. The response contained80 questions and `has_more=true`. These80, sorted by `(creation_date, numeric question_id)`, run from2024-01-01T11:39:17+00:00 through2024-01-22T22:34:36+00:00. This is the first80 of the current-tag frame, not every question in the half-year and not a random/representative sample. Root is responsible for overall source counts.

All80 earliest revision titles and complete bodies were manually read, in four20-record batches. Exact raw API responses remain only in ignored `.cache/blender-initial`; no full source text/images are included in committed evidence. Three API revision pages were mechanically projected by `initial_revisions` to revision_number1 before output. A second mechanical audit found80 distinct initial body records for80 posts,80 distinct initial GUIDs, and zero duplicate/conflicting first body revisions. No inaccessible initial body was encountered.

The frame records70 eligible and10 ineligible initial posts;4 selected and66 eligible posts retained after the selection boundary. The first four eligible are exactly BL-T1=309037, BL-T2=309047, BL-T3=309058, BL-T4=309084 (ranks1–4). Therefore the Jul–Dec extension was not invoked. Tags are preserved separately; later current tag membership can differ from initial tags (for example rank40 and45).

## Boundary audit

One masked same-second query at fromdate=todate1705962876 returned an empty result even though rank80 has that timestamp. This did not verify the boundary. A single narrow masked bracket query with fromdate1705962875/todate1705962877 returned only question310379 at the exact boundary timestamp and has_more=false. No boundary tie crosses the80-record cutoff; the first80 remain unchanged. Both query receipts and fingerprints are retained. No full-frame refetch was made. Acquisition used6 Stack Exchange API calls: frame1, revisions3, same-second check1, bracket check1; the last returned quota field was76 (shared quota snapshot, not a reserved allowance).

## Image reading and eligibility boundaries

Text paragraph numbers in the selected-case locators count prose paragraphs and omit image-only paragraphs; code blocks and numbered figures are located separately. Figure numbering follows initial body order, excluding the blend-exchange download badge.

29 original image URLs embedded in initial revisions were fetched directly, all returned200, and all29 were visually read. The9 images attached to the four selected posts were all read. `image-reading.jsonl` records exact URL, opened UTC, content fingerprint, what was actually visible, and D1 limitations. The other20 figures resolve image-dependent eligibility for ranks6,9,20,21,37,44,58,61,66,68,70,74,79. No node labels or numeric parameters were inferred from filenames or unread images. Unopened images of other frame posts were not required for the textual eligibility reason and were not treated as read. Blend files, external videos, prior question pages and linked tutorials were not opened.

An actual relevant preliminary operation can satisfy the attempt criterion even if the final requested step was not attempted. Thus rank3 qualifies from constructing the named wired node group; its bulk modifier application loop is only a comment skeleton and remains T/O not documented. The same distinction is maintained for creating/subdividing the rank4 polyhedron versus moving its center edges. Rank21 is excluded on insufficient initial current-input trial evidence after its lone disconnected/crossed-out Raycast picture was read. Rank68 is excluded because its picture is a conceptual Boolean matrix, not an actual edited input/observed output. No full equivalence between different operations is inferred solely from a name.

## Masking and source counting

The selector read AGENTS and SCOPE sections1–6; SCOPE section7 was deliberately omitted. It never opened full question pages, answers, comments, author follow-ups, later revision bodies, answer_count, acceptance or score. Full revision responses were fetched into cache but only revision1 was exposed to this reader. No material from the subsequent proposal/follow-up stage was seen, and no first-proposal or outcome conclusion is made here.

Each selected request is one counted primary source in `sources-part.jsonl` (4 total). Figures/revisions belong to that request lineage and do not add sources; the other76 frame records are retained for recruitment auditing without contributing extra required source-count slots. Public numeric owner ID equals the initial revision user ID for each selected request. BL-T1/BL-T2 share the same owner but are distinct request events. All four author software versions are unconfirmed; no2024 release is guessed from date/UI. The revision GUID fixes the initial text reference; retrieved image hashes establish the bytes seen now, not an independent guarantee of historical image bytes.

## Handoff boundary

Ready for root to combine and remotely seal the initial bundle. This reader must wait for the verified remote seal before opening proposal material. It has neither changed branches nor committed/pushed. All its writes are under `evidence/blender-initial/` or `.cache/blender-initial/`.
