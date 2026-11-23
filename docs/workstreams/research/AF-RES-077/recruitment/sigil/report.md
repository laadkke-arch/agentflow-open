# AF-RES-077 — Sigil recruitment report

Evidence recorded: 2026-11-23 UTC. Role: recruitment/source investigation only. No experimental-design documents, donor source, selected repair patch, downstream tests, or later resolution discussion were read.

## Recruitment outcome

**Strict vacancy is preserved for an exact author-version-confirmed case.** The earliest relevant request in the prescribed bounded sample is [Sigil issue #450](https://github.com/Sigil-Ebook/Sigil/issues/450), opened by **gennaios** at **2019-08-10T23:45:39Z**. It describes self-file-qualified links whose targets are not correctly reassigned after splitting a chapter. The author provides concrete footnote and commercial academic EPUB context in early clarifications, but says only “newest version.” The exact installed numeric version is not established in the body and first six comments read.

Issue #450 is therefore retained as the **earliest relevant auxiliary, with an operational contemporary release pin**. [Sigil 0.9.17](https://github.com/Sigil-Ebook/Sigil/releases/tag/0.9.17) was published at **2019-08-10T13:22:55Z**, before the request. Its annotated tag object `add8e4126dd33776e83f2faea66abaaccb29b4a1` points to exact commit **`30419827123d533d10ad482b1634dcec05ff0e1b`**. This is a verified source snapshot, not proof of the author's installed build. No author-provided example with the same anchor name in two chapters was established.

## Bounded recruitment and response receipts

The required original queries were:

1. `repo:Sigil-Ebook/Sigil split created:2019-01-01..2025-12-31`
2. `repo:Sigil-Ebook/Sigil anchor created:2019-01-01..2025-12-31`

Both were requested with created ascending and first ten. The connector's `search_issues` responses omitted author and creation timestamps and returned only issue records. Raw exact-query API requests then failed with HTTP 422, stating that `is:issue` or `is:pull-request` was required. The failure and original responses are preserved in `query-receipts.json`.

Each query was reconstructed by issuing its issue and pull-request variants, taking the first ten from each disjoint population, merging by `created_at` then issue number, and taking the first ten of the union. This preserves the intended top-ten population: no item ranked below tenth in either disjoint population can enter the combined first ten. No timestamp ties affected the returned boundary. Type-specific API responses reported `incomplete_results: false`.

| Query | Original issue response order | Pull-request order | Reconstructed first ten |
|---|---|---|---|
| split | 404, 450, 483, 492, 576, 577, 580, 586, 587, 604 | 472, 582 | 404, 450, 472, 483, 492, 576, 577, 580, 582, 586 |
| anchor | 450, 522, 531, 598, 667, 776, 797 | none | 450, 522, 531, 598, 667, 776, 797 |

The deduplicated merged order is **404, 450, 472, 483, 492, 522, 531, 576, 577, 580, 582, 586, 598, 667, 776, 797**. The first ten were directly fetched through their official issue-record endpoints, including PR #472's request record without its patch.

| Rank | Candidate / author | Direct-read disposition |
|---|---|---|
| 1 | #404 / BeckyDTP | Dictionary language-name issue; no chapter-link purpose. |
| 2 | #450 / gennaios | Closest auxiliary; chapter splitting, valid footnotes, visible target reassignment failure; exact installed version missing. |
| 3 | PR #472 / luzpaz | Typographical cleanup request. |
| 4 | #483 / ghost | Settings-dialog scrolling. |
| 5 | #492 / BeckyDTP | Interface language persistence. |
| 6 | #522 / wlkz | Anchor corruption on XHTML import; no split/move and no numeric version. |
| 7 | #531 / WS64 | Filenames beginning with # disappear after save/reopen; versions given, but no split-target purpose. |
| 8 | #576 / cj0293 | Saved TXT import produces missing NCX, version 1.4.3; different behavior. |
| 9 | #577 / budikesuma | Automatic checking/freezing. |
| 10 | #580 / szymonlopaciuk | Keyboard shortcuts interfere with Polish typing. |

Candidates beyond rank ten remain search-only records; no eligibility or negative finding is inferred from their unread discussions.

## Requester's actual purpose and observed behavior

The [current request body](https://github.com/Sigil-Ebook/Sigil/issues/450) says that links such as `this_file.xhtml#anchor1` may continue pointing to the original filename or first resulting split. This is the author's report, not an independently reproduced result.

In [author comment 520189313](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520189313), created **2019-08-11T00:12:41Z**, the author says all anchors exist, no warning appears, and a chapter may have dozens of correct footnotes at its end. Removing the same-file filename and leaving fragment-only hrefs before splitting reportedly works.

In [author comment 520196406](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520196406), created **2019-08-11T03:07:52Z**, the author confirms the self-file-qualified-link case, describes four or five occurrences in commercial EPUBs, often academic titles, and asks for automatic handling. These comments establish practical use and desired visible behavior. They are one request-author lineage, not independent corroboration of the bug.

## Two source-supported preservation clues

**P1 — Preserve the identity of an existing internal footnote target when splitting between the link and target.** A link initially written with its own filename plus fragment should continue reaching the same content after the target moves to a resulting chapter. The author reports that all targets exist and that the fragment-only workaround behaves as intended. This clue is directly grounded in #450 and the two author comments above. It does not establish behavior for missing targets or malformed books.

**P2 — Preserve the original chapter scope of links when identical fragment IDs can occur in different chapters.** The pre-request code explicitly separates split-derived files from other files and states that IDs cannot be assumed unique in the latter set. `Book::CreateSectionBreakOriginalResource` and `Book::CreateNewSections` pass the originating filename when updating links from other chapters; `AnchorUpdates::UpdateExternalAnchorsInOneFile` filters for that original path before changing an href. See [Book.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/BookManipulation/Book.cpp) and [AnchorUpdates.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/SourceUpdates/AnchorUpdates.cpp).

P2 is a source-code-supported preservation boundary inferred from existing behavior and comments. It is **not** an author-supplied duplicate-anchor reproduction, an assertion that the code handles every such case, or a new maintainer requirement.

## Pre-change interfaces and write timing

All paths below are at the exact 0.9.17 commit. Their contents count as **one codebase lineage**.

| Interface / symbol | Evidence from the pinned source |
|---|---|
| `Book::CreateSectionBreakOriginalResource(content, originating_resource)` | Renames the original resource, creates the other section, sets its text, saves it to the working file, updates spine order, rewrites anchors among split files, then external chapter links and optional NCX entries; marks the book modified. |
| `Book::CreateNewSections(new_sections, original_resource)` | Creates new sections through concurrent workers and waits for completion; gathers split files; updates internal anchors, external links, optional NCX, and spine; marks the book modified. |
| `AnchorUpdates::UpdateAllAnchorsWithIDs(html_resources)` | Builds ID locations over the supplied file set and applies `UpdateAnchorsInOneFile` with a blocking map. |
| `AnchorUpdates::GetIDLocations(html_resources)` | Returns `QHash<QString, QString>` mapping fragment ID to filename; later assignments replace an earlier value for the same key. File scope depends on the supplied set. |
| `AnchorUpdates::UpdateExternalAnchors(html_resources, originating_filename, new_files)` | Builds locations only from the resulting files and passes the originating filename into each other-file update. |
| `UpdateAnchorsInOneFile` / `UpdateExternalAnchorsInOneFile` | Acquire a resource write lock, parse with Gumbo, modify applicable href attributes, and call `SetText` only if changed. They do not themselves call `SaveToDisk`. |
| `HTMLResource::SetText` / `TextResource::SetText` | Changes the resource's document immediately on the GUI thread; on another thread it caches the text and schedules a GUI-thread update. `GetText` returns the cache while in use. |
| `TextResource::SaveToDisk` | Writes the current cache or text to the resource's working filesystem path. This is separate from the setter and does not by itself establish final EPUB archive export timing. |
| `FlowTab::SplitSection` | Checks well-formedness, prevents splitting the navigation resource, calls the existing undefined-fragment warning gate, and emits `OldTabRequest`. |

The single-section split writes the newly created section before anchor reconciliation. The multi-section worker writes a placeholder file and sets the in-memory resource text; subsequent anchor setters also update resource text/cache. This is static ordering evidence only. No runtime execution, persistence failure, transaction guarantee, or final archive write was tested.

## Provenance, exposure, limits, and cost

- The current body of #450 was read. Its initial revision is **not established** without edit history.
- Only the first six comments of #450 were read; the boundary is author comment **520196406**, **2019-08-11T03:07:52Z**. Four early maintainer clarification messages were incidentally read. Their assertions, including HTML-validity discussion, were not adopted as requirements.
- Search and issue-record metadata unavoidably exposed current closed states and dates. No closure explanation or later discussion was read.
- The release collection transported release-note bodies, but those bodies were filtered before display/read; only release metadata was used.
- No selected repair PR, patch, commit diff, downstream test, donor source, or experimental-design material was inspected.
- No external messages, paid APIs, account changes, git commits, or shared-file edits were made.
- Cost: **33 GitHub read requests**, including **2 failed raw exact-query requests**; zero code executions, tests, paid calls, or external mutations. Per-call wall time was not independently instrumented. Capture/recording timestamps are in the evidence files.

## Files

- `query-receipts.json`: original response order, exact-query failures, type-filtered raw receipts, reconstructed order.
- `direct-read-receipts.json`: first-ten current request records.
- `candidates.json`: candidate IDs, author lineages, direct-read flags, version limits, and strict vacancy.
- `request-and-release-evidence.json`: early comment boundary, author text, release metadata, tag-to-commit resolution.
- `source-notes.json`: source IDs, immutable URLs, blob SHAs, symbols/line sections, bounded excerpts, lineage and validation limits.
- `background.md`: compact handoff context.

