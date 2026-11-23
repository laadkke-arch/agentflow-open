# Sigil background — bounded recruitment handoff

## Status

No exact author-version-confirmed qualifying request was found in the prescribed first-ten merged direct-read population. Keep that strict vacancy. The earliest relevant auxiliary is [Sigil #450](https://github.com/Sigil-Ebook/Sigil/issues/450), opened by **gennaios** on **2019-08-10T23:45:39Z**.

The author's practical task is splitting commercial academic EPUB chapters that contain footnotes. The reported failure is that valid self-file-qualified hrefs, such as `this_file.xhtml#anchor1`, retain the wrong chapter target after splitting. In [comment 520189313](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520189313), the author says all anchors exist, no warning appears, and pre-converting to fragment-only hrefs works. [Comment 520196406](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520196406) confirms the commercial/academic context and asks for automatic handling.

The author says “newest version,” not a numeric installed version. The operational source pin is **0.9.17**, published before the report on **2019-08-10T13:22:55Z**, commit **`30419827123d533d10ad482b1634dcec05ff0e1b`**. This pin must not be represented as proof of the author's environment. The current request body is not established as its original revision.

## Preservation clues

1. After a split separates an existing internal link and its footnote target, the link should continue reaching that same content. This is grounded in the author's request and early comments.
2. Link updates from other chapters must retain filename scope when fragment names can be reused across chapters. This is grounded in pre-request code comments and update boundaries, not in an author-supplied duplicate-anchor reproduction.

No same-anchor-name-in-two-chapters author case was established in this bounded sample. These are recruitment clues for evaluation, not maintainer instructions.

## Pre-request implementation context

At the operational pin, `Book::CreateSectionBreakOriginalResource` and `Book::CreateNewSections` collect the split-derived files, call `AnchorUpdates::UpdateAllAnchorsWithIDs` for that set, and separately call `UpdateExternalAnchors` for other chapters with the originating filename. The latter distinction is explained in code by IDs not being assumed unique across chapters.

`GetIDLocations` builds a `QHash<QString, QString>` from fragment ID to filename over the supplied set. Per-file updates parse resource text, modify href attributes, and call `SetText` when changed. They do not themselves call `SaveToDisk`. The setter updates a GUI document or a worker-thread cache; `SaveToDisk` writes the working resource file separately. The single-section path saves its new section before anchor reconciliation. No transaction or final EPUB export property is established.

Immutable primary source: [Book.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/BookManipulation/Book.cpp), [AnchorUpdates.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/SourceUpdates/AnchorUpdates.cpp), [TextResource.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/ResourceObjects/TextResource.cpp). All code files are one lineage.

## Read boundary

Direct request records: #404, #450, PR #472, #483, #492, #522, #531, #576, #577, #580. For #450, only its body and first six comments were read, ending at author comment 520196406. No later conclusion, selected repair patch, downstream tests, donor source, or experiment-design documents were inspected. Exact-query API failure and the issue/PR union reconstruction are fully recorded in `query-receipts.json`.

This handoff supplies recruitment evidence and static code context only. No reproduction or performance result is claimed.

