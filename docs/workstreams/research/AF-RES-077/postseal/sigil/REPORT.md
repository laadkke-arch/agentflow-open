# AF-RES-077 — Sigil post-seal evidence

**The frozen SG-E operation is not expressible through Sigil 0.9.17's supported native split/rename workflow.** Its requested destination, `Text/parts/ch1_tail.xhtml`, requires a nested text folder. This version places HTML resources in a fixed `OEBPS/Text` folder, rejects slashes in native filenames, and normalizes imported content into fixed category folders. The frozen input has been preserved; no flatter destination was substituted.

**The historical bug also differs from SG-E's split placement.** Later investigation of #450 found the failure when the reference and target moved together into the same split-off chapter while the href retained the old filename. Splitting between the reference and target was reported to work. These findings constrain applicability; they are not an executed score for any proposal.

Evidence was released after seal commit **`7bc2d1f84c04b47711d72e7c110b8f927d97f4ad`**. This investigator read `SG-common.json` and prior recruitment notes, **not A/B proposal choices**. The working common packet was verified byte-for-byte against its sealed version. All source analysis is pinned to **Sigil 0.9.17, `30419827123d533d10ad482b1634dcec05ff0e1b`**, unless explicitly labeled as the later repair.

## 1. Historical outcome and what it establishes

The complete current [issue #450 discussion](https://github.com/Sigil-Ebook/Sigil/issues/450) contains 49 comments. Early simple cases placed a split between the reference and target; maintainers and the author could not reproduce the reported failure with that arrangement. The author later explained that the practical task was reducing abnormally large chapters to roughly 200 KB before reading on macOS, using multiple split markers. A commercial sample was shared through a now-deleted Dropbox link; it was not recovered.

The important later evidence is:

| Evidence | Finding | Evidence level |
|---|---|---|
| [520240119](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520240119), Kevin Hendricks | Supplies a readable single-marker source example with the link before the split and the target after it; reports that this worked. | Test source plus maintainer report; no independent execution receipt. |
| [520254553](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520254553), Kevin Hendricks | Identifies a commercial-book link and target after every split marker; both ended in `part0008_0005.xhtml`, but the href retained `part0008.xhtml`. | Maintainer investigation report with specific locations. |
| [520258201](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520258201), Doug Massay | Explicitly distinguishes splitting between link and target, which worked, from moving the href into a split-created file. | Maintainer report. |
| [520259623](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520259623), Kevin Hendricks | Pastes debug lines with `file_id == resource_filename == Section0001_0001.xhtml`, explaining why the original updater left the stale href alone. | Posted debug artifact; not a retrieved CI log or a run performed here. |
| [520649931](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520649931), gennaios | Reports examining about 150 EPUBs, finding ten with this style of link, and seeing no split issues with the test build; reports separate NCX merge problems. | Request-author tester assertion. |
| [520947721](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520947721), Kevin Hendricks | Closes the issue as fixed in master on 2019-08-13T18:15:52Z. | Maintainer closure assertion. |

The source branch and fixture layout support this explanation, but this investigation did not build or run Sigil. The discussion's claims about own-filename links being outside a specification are retained as historical statements and are **not** adopted as requirements or normative findings.

The original author's numeric version and exact build remain unknown. A later maintainer fixture carries 0.9.17 metadata, which does not establish the original reporter's installed build. The current issue body is not established as its initial revision; no actual edit history was recovered. The recruitment vacancy therefore remains.

## 2. Exact public fixture, including its limitation

The public reduced fixture attached by Kevin Hendricks is [test_split2.epub.zip](https://github.com/Sigil-Ebook/Sigil/files/3490396/test_split2.epub.zip), linked in [comment 520256671](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520256671). It was downloaded without modification.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Outer ZIP | 1,884 | `32555ab1fea6b756ed47546397334939dc1660a9edfba00358fcc827fadb0ea6` |
| Inner EPUB | 2,060 | `244dc0107a2cb1ad17ef2bf80c858e90e3b7396a63bb78869ae024206d6aa7df` |
| `OEBPS/Text/Section0001.xhtml` | 500 | `f4dad5d427f054bd5573dad7ceb6b93b7fd43d6cd0be66d179453c9e4bb91695` |

The fixture contains a real `hr` split marker **before both** the reference and the `here` target. Its OPF has a Sigil version value of 0.9.17 and an EPUB 3 package. No golden output EPUB is included.

The present attachment also contains a significant limitation: its href is literally **`../Section0001.xhtml#here`** inside **`OEBPS/Text/Section0001.xhtml`**. Normal path resolution targets **`OEBPS/Section0001.xhtml`**, which is absent from the archive. The exact fixture is preserved; this path was not corrected to make the example cleaner.

That inspection was actually executed using read-only ZIP/XML/path parsing. It is **not execution of Sigil**. `fixture-inspection-receipt.json` records the checks and `originals/fixture-inspection.json` preserves all readable archive members. A contemporary checksum was not available, so historical byte identity with the 2019 download is unverified.

The pinned import code does not supply a hidden justification for claiming this original path was valid: `GumboInterface::update_attribute_value` resolves an attribute against the current directory and rewrites it only if the resulting path is in its source-update map. Here it computes the absent `OEBPS/Section0001.xhtml`, whereas the actual manifest maps the member under `OEBPS/Text`. The undefined-fragment warning uses `QUrl::fileName()` and ID presence, so that warning alone is not proof of full-path validity. Sources: [GumboInterface.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/Misc/GumboInterface.cpp) and [Book.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/BookManipulation/Book.cpp).

The **source-derived**, unexecuted repaired output would put both nodes in `Section0001_0001.xhtml`, change the reference to `#here`, and resolve it to the text **target of link**.

## 3. Original updater and later repair

At the operational pin, `AnchorUpdates::GetIDLocations` produces a fragment-ID-to-filename hash over the supplied files. `Book::CreateNewSections` supplies the original section followed by its new sections. The updater looks up the fragment and changes an href when the located target filename differs from the current resource filename. When the target is in the same newly split resource, the original code does nothing—even if the href still names the old resource. See [AnchorUpdates.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/SourceUpdates/AnchorUpdates.cpp).

A bounded file-history query identified repair commit [ae60e3e63a2f9343b40d316f179b9dfbcb6d838b](https://github.com/Sigil-Ebook/Sigil/commit/ae60e3e63a2f9343b40d316f179b9dfbcb6d838b), authored by Kevin Hendricks at **2019-08-11T21:12:00Z**. Its parent is `ed8fbc0823910e5d0bd49c0b41b8a5ffcf69ffe4`. The issue timeline did not directly cross-link a PR; identification rests on the matching file, date, message, and change.

The commit changes only `AnchorUpdates.cpp`. Besides debug statements, it adds a branch for:

`file_id == resource_filename && !base_href.contains(file_id)`

That branch replaces the href with `#fragment`. It is a narrow same-file/stale-base repair. It does not add nested-folder operations, duplicate-ID ambiguity handling, or an automated regression test. Its substring test is not evidence of a general document-identity resolver. The complete patch is retained in `postseal-receipts.json`.

## 4. Frozen SG-N / SG-E / SG-X applicability

The packet's `<!--SPLIT-->` delimiter is not an automatic Sigil split marker. `XhtmlDoc::BREAK_TAG_SEARCH` recognizes `hr` elements with `sigil_split_marker` or `sigilChapterBreak` classes. A manual cursor split at the comment's position is a possible harness interpretation, but the packet does not state that interpretation. It also supplies content fragments rather than complete EPUB archives. These are recorded limitations; no frozen bytes were changed. Source: [XhtmlDoc.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/BookManipulation/XhtmlDoc.cpp).

| Frozen case | What the source supports | What remains unexecuted or inapplicable |
|---|---|---|
| **SG-N** | With an explicitly performed split between the unique reference and target, the pre-existing different-file branch points the link toward the tail. The generated name is normally `ch1_0001.xhtml`; an ordinary basename rename can produce the packet's requested `ch1_1.xhtml`. | The exact marker/harness and archive wrapper are not specified. No save/reopen run was performed. This is not the historical repaired branch. |
| **SG-E** | Before its requested move, a valid imported split between reference and target uses the existing different-file branch. `ch2` is outside the split-derived ID map. External chapter links, once normalized during import, are gated by the originating filename. | **The nested-folder move is unsupported as frozen.** No flatter rename or externally edited archive was substituted. Literal in-memory toc hrefs without import normalization also do not necessarily match the external updater's `../Text/ch1.xhtml` predicate. No pass/fail execution result is assigned. |
| **SG-X** | The ID hash overwrites earlier entries with later same-ID entries; the supplied section order places split-off sections after the original. The undefined-fragment gate checks whether an ID is present, not whether it is unique. No ambiguity/refusal branch appears in the inspected updater. | Reaching the updater with duplicate IDs can silently select the later section; that is a static prediction, not an observed run. The source's uniqueness assumption is violated. No trusted original target is established, and unchanged bytes/digests alone cannot supply missing target intent. |

The SG-E blocker is direct source evidence, not merely absence of a menu search:

- [FolderKeeper.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/BookManipulation/FolderKeeper.cpp), `AddContentFileToFolder`, places HTML under `m_FullPathToTextFolder + "/" + filename`; the filename is taken from the basename.
- [OPFModel.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/MainUI/OPFModel.cpp) has fixed, noneditable category folders, enables text reordering, and explicitly rejects both `/` and backslash in native renames.
- [ImportEPUB.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/Importers/ImportEPUB.cpp), `LoadOneFile`, uses that fixed-folder placement on reopen. An out-of-band ZIP rearrangement would be a different operation and would be normalized on import.

## 5. Save/reopen timing

The prior recruitment finding about `SetText` remains: it updates a document or worker cache, separately from persistence. The post-seal export source now adds the final sequence. `ExportEPUB::WriteBook` updates metadata, calls `SaveAllResourcesToDisk`, copies the working book into a temporary publication directory, and creates a temporary EPUB. It then opens the actual destination with `WriteOnly | Truncate` and copies bytes from the temporary archive. The shown path does not perform an atomic final rename. Source: [ExportEPUB.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/Exporters/ExportEPUB.cpp).

Reopening goes through folder normalization and source updates. A successful setter or correct in-memory href therefore does not by itself establish the frozen save/reopen observations. No final archive, interrupted-save behavior, or GUI result was generated here.

## 6. Tests, CI, and exact documented build commands

The untruncated pinned tree, principal CMake files, and CI configurations were inspected. No first-party automated anchor test or matching `add_test`, `enable_testing`, or `ctest` registration was found in that bounded scope. The existing `docs/testplugin_v014.zip` and build-document menu steps test the Python plugin framework, not anchor preservation. Dependency test suites were not counted as Sigil tests.

[.travis.yml](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/.travis.yml) contains macOS build/packaging commands. [appveyor.yml](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/appveyor.yml) configures Ninja, builds, and makes an installer. These source files are not receipts of executed behavioral tests.

For both the release pin and repair commit, current GitHub combined-status responses have **zero statuses**, and check-run responses have **zero check runs**. The combined status value of `pending` with an empty list is not interpreted as a historical pending build. The linked AppVeyor artifact page returned only the present application shell through public HTTP. One guessed GET route returned 405; the documented project-history route returned 404. No historical build result, job log, or anchor-test receipt was obtained. These retrieval failures do not prove that historical builds or tests never ran.

The [pinned Linux build document](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/docs/Building_on_Linux.md) requires a C++11 toolchain, CMake 3.0+, Qt 5.9.4+ with QtWebEngine and the listed modules, and Python 3.4+ components. After dependencies are already available, its configure/build commands are:

```sh
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release ../sigil-src
make -j4
```

A reproducibility setup would additionally clone the repository, detach `sigil-src` at `30419827123d533d10ad482b1634dcec05ff0e1b`, and create a sibling `sigil-build` directory. Those pinning steps are supplied by this investigation; the configure/build commands above are from the source. **None were run. No dependencies were installed. No source-supported automated anchor-test command was found, so none is invented.**

## 7. Integrity, lineage, cost, and files

All **21 newly retrieved source files** match the Git blob SHAs in the pinned tree. `integrity.json` records their SHA-256 values and the unchanged common-packet hash. The linked fixture archives and individual members have separate hashes.

All Sigil code, official guide, maintainer fixture, and repair are same-work material. The root investigator's already-read 2019-06-25 guide at `d101fa2b...` remains that same work and is not counted as independent corroboration. Requester statements retain gennaios authorship.

Post-seal acquisition used **30 GitHub read requests, two web reads, and four top-level public HTTP requests through the shell**. Three lookup failures are preserved: inaccessible AppVeyor web-tool result, unsupported API GET 405, and documented history lookup 404. No paid calls, external mutations, git commits, installed dependencies, target builds/tests, or GUI executions occurred. Local executed work was limited to archive parsing, path checks, source hash verification, and sealed-packet byte comparison.

The requested deliverables are `report.json` and this `REPORT.md`. Supporting originals and receipts include:

- `issue450-comments.json`: all 49 current comments with author and UTC dates.
- `originals/test_split2.epub.zip`, `originals/test_split2.epub`, and `originals/fixture-inspection.json`.
- `fixture-inspection-receipt.json`: executed artifact checks and explicitly unexecuted expected output.
- `pinned-originals.json` and `pinned-originals-part2.json`: exact source bodies, URLs, refs, and blob SHAs.
- `postseal-receipts.json`: timeline, repair patch, current status/check responses.
- `ci-fetch-receipts.json` and `ci-history-fetch-receipt.json`: bounded CI attempts and failures.
- `test-source-inventory.json`, `integrity.json`, and `manifest.json`.

The remaining unknowns are the initial request revision, original reporter's exact build, historical attachment byte identity, actual frozen-case runtime behavior, and independently retrievable historical execution receipts.

