# AF-RES-077 — MuseScore bounded recruitment

## Decision

**Primary slot: vacant. Auxiliary background: MuseScore PR [#4590](https://github.com/musescore/MuseScore/pull/4590), “fix #281441 unset selected flag in clones.”** None of the ten required current issue/PR bodies establishes the complete combination of master-score/linked-part editing, an undo or reopen boundary, version evidence, and a distinguishing effect on out-of-scope voices or parts. This is a finding about the fixed recruitment frame, not evidence that no qualifying report exists elsewhere.

PR #4590 supports a narrower part-creation problem. Its author, **ericfont** (GitHub user ID `6502474`, current association `CONTRIBUTOR`), describes source elements selected before creating a part remaining blue in the generated part even though that part has no actual selection. The body proposes that cloning should not retain the selection flag. The current description is the author-goal source; **its first revision is unverified**. Contributor association does not establish a maintainer request. The original tracker author and affected release are unverified: the attempted official tracker page `/en/node/281441` returned HTTP 403.

There is **no verified author demand about undo, reopening a file, or unaffected other voices/parts** in this auxiliary. Any probe adding those boundaries is research-authored. No runtime result, successful fix, or later PR conclusion is asserted here.

## Fixed searches and order

Both exact public REST requests used `sort=created`, `order=asc`, `per_page=10`, `page=1`:

| Query | Total indexed matches | First ten in original returned order |
|---|---:|---|
| `repo:musescore/MuseScore part created:2019-01-01..2025-12-31` | 3,173 | 4525, 4529, 4534, 4535, 4541, 4553, 4565, 4590, 4603, 4614 |
| `repo:musescore/MuseScore undo created:2019-01-01..2025-12-31` | 695 | 4541, 4542, 4570, 4621, 4622, 4627, 4652, 4669, 4730, 4752 |

The authoritative receipts are `public_part_query.json` and `public_undo_query.json`. Both returned HTTP 200 and `incomplete_results=false`. Their union contains 19 distinct repository numbers. Deduplication followed by ascending `(created_at, number)` gives the directly read first ten below. Search matches can originate beyond the current body, so a matching keyword is not itself body evidence.

| Union rank | PR | Created UTC | Current-body assessment |
|---:|---|---|---|
| 1 | [4525](https://github.com/musescore/MuseScore/pull/4525) | 2019-01-02 07:20:45 | MSVC build-configuration failure; outside target behavior. |
| 2 | [4529](https://github.com/musescore/MuseScore/pull/4529) | 2019-01-03 09:49:30 | Main score and created-part layout performance; no qualifying undo/reopen boundary or affected release. |
| 3 | [4534](https://github.com/musescore/MuseScore/pull/4534) | 2019-01-04 11:39:10 | Rest/slur crash in a higher voice; no linked-part boundary, version, or out-of-scope comparison. |
| 4 | [4535](https://github.com/musescore/MuseScore/pull/4535) | 2019-01-04 15:55:35 | Soundfont preset ordering; outside target behavior. |
| 5 | [4541](https://github.com/musescore/MuseScore/pull/4541) | 2019-01-06 21:50:22 | Single-note dynamics feature; no relevant linked-part undo/reopen demand. |
| 6 | [4542](https://github.com/musescore/MuseScore/pull/4542) | 2019-01-06 22:23:34 | Timeline refactor and selection artifacts; no linked-part undo/reopen demand. |
| 7 | [4553](https://github.com/musescore/MuseScore/pull/4553) | 2019-01-09 12:22:51 | Repeated lyric-line reset updates and freeze; no linked-part boundary or exact version. |
| 8 | [4565](https://github.com/musescore/MuseScore/pull/4565) | 2019-01-11 20:04:48 | Compilation compatibility; outside target behavior. |
| 9 | [4570](https://github.com/musescore/MuseScore/pull/4570) | 2019-01-12 16:16:01 | Undoing deletion of instrument names crashes; no linked-part or out-of-scope evidence and no exact release. |
| 10 | [4590](https://github.com/musescore/MuseScore/pull/4590) | 2019-01-16 04:54:28 | Part creation leaks selection appearance; auxiliary only for the missing boundaries above. |

`search-order.json` preserves both original orders, query membership/ranks, and the complete sorted union. `candidates.json` records author, timestamps, body location, rejection reason, and first-revision uncertainty for every direct read.

The initial connector issue-search action excluded PRs and supplied null timestamps. Its generic search endpoint rejected the exact untyped queries with 422. These are retained as nonauthoritative attempts. Separate `is:issue`/`is:pr` queries succeeded and are also retained; their PR order agrees with the canonical exact public results. The public requests resolved the access discrepancy without changing the recruitment frame.

## Confirmed source version

The contextual pre-change baseline is [**v3.0.1**](https://github.com/musescore/MuseScore/releases/tag/v3.0.1), whose [tag ref](https://api.github.com/repos/musescore/MuseScore/git/ref/tags/v3.0.1) resolves directly to commit **`06a66a2206fc5f3c2c33d7ee4123badf496bc4dd`**. The [Git commit metadata](https://api.github.com/repos/musescore/MuseScore/git/commits/06a66a2206fc5f3c2c33d7ee4123badf496bc4dd) dates it to `2019-01-15T09:20:49Z`; release publication is `2019-01-15T10:00:18Z`. Both precede #4590 creation by about a day.

This establishes a contemporary source revision, **not the reporter's exact affected version or the PR's base/head**. The code at this pin still copies `_flags` in `Element`'s copy constructor, consistent with the author's described mechanism. No selected PR patch was used to identify this path. Initial guesses of a `v3.0.0` release/ref returned 404 and are preserved as failures, not silently replaced by a version claim.

## Two preservation conditions

### P1 — Author-supported: selection belongs to the part's actual selection

Creating a part from selected source elements should not make its clones appear selected when the part's selection does not contain them. This is supported by #4590's current body, paragraphs 1–2. At the pinned revision, `Selection` owns a `Score*` and an element list; `add/update` set flags for listed elements and `clear/remove` clear them. `Element::curColor` renders a selected element with a selection color. These source paths explain why copying the selection flag can create a visible mismatch; no execution result is claimed.

### P2 — Analyst-supplied: preserve musical links and the excerpt's scope

A change limited to selection inheritance should preserve linked musical identity and the excerpt's track mapping, including the existing system-element exceptions. Musical data outside the intended part/voice scope should remain unchanged. This is a **research preservation condition**, not a request or verified outcome attributed to ericfont. It is informed by `Excerpt::createExcerpt`/`cloneStaves`, the linked-clone path, and the link membership and XML representation described below. Undo/reopen checks and comparisons against unaffected voices or parts would extend this condition and remain research-authored.

## Pre-change interfaces and writes

All locations below refer to the pinned SHA, with exact source copies and fetch receipts retained under this directory. They constitute one MuseScore work, not independent evidence units per file or release.

| Source and symbol | Interface or storage effect relevant to the auxiliary |
|---|---|
| [`element.h`](https://github.com/musescore/MuseScore/blob/06a66a2206fc5f3c2c33d7ee4123badf496bc4dd/libmscore/element.h), `ElementFlag::SELECTED`, `selected`, `setSelected` | Defines selection as bit `0x00000040` in per-element `_flags`; setter changes that bit. Lines 57–65, 151–192. |
| [`element.cpp`](https://github.com/musescore/MuseScore/blob/06a66a2206fc5f3c2c33d7ee4123badf496bc4dd/libmscore/element.cpp), `Element(const Element&)` | Copies `_flags = e._flags`, along with track, parent, position, color and other fields. Lines 167–180. This is the narrow candidate write boundary. |
| Same file, `Element::linkedClone` | Calls polymorphic `clone()`, sets autoplace, and submits `Link(e, this)` through the source score's undo interface. Lines 196–201. This identifies a command interface, not proof of undo correctness. |
| Same file, `Element::curColor` | Uses `selected()` or a note's marked state to choose a voice-specific selection color. Lines 287–319. |
| [`select.h`](https://github.com/musescore/MuseScore/blob/06a66a2206fc5f3c2c33d7ee4123badf496bc4dd/libmscore/select.h) and [`select.cpp`](https://github.com/musescore/MuseScore/blob/06a66a2206fc5f3c2c33d7ee4123badf496bc4dd/libmscore/select.cpp), `Selection` | Stores `_score`, `_state`, `_el`; `add/update` append and set selected flags; `clear/remove` remove entries and clear flags. Header 123–152; implementation 296–337, 604–608. |
| [`excerpt.cpp`](https://github.com/musescore/MuseScore/blob/06a66a2206fc5f3c2c33d7ee4123badf496bc4dd/libmscore/excerpt.cpp), `Excerpt::createExcerpt` | Creates and links staffs, appends parts, constructs a source/destination voice-track map, calls `cloneStaves`. Lines 129–192. |
| Same file, `Excerpt::cloneStaves` | Skips unmapped source tracks (506–508), links included clones and changes destination track/score (558–566). Measure-attached system elements have an explicit unmapped-track exception (697–719). New elements and measures enter destination containers. |
| [`scoreElement.cpp`](https://github.com/musescore/MuseScore/blob/06a66a2206fc5f3c2c33d7ee4123badf496bc4dd/libmscore/scoreElement.cpp), copy constructor, `linkTo`, `unlink` | Copy clears `_links`; `linkTo` shares/creates a `LinkedElements` list and appends members, while `unlink` removes a member and clears or disposes lists. Lines 141–151, 507–544. |
| [`undo.cpp`](https://github.com/musescore/MuseScore/blob/06a66a2206fc5f3c2c33d7ee4123badf496bc4dd/libmscore/undo.cpp), `LinkUnlink::link/unlink`, `Link` | Mutates linked-list membership and element link pointers. Lines 2243–2280. No command was executed. |
| `element.cpp`, `Element::writeProperties/readProperties` | The XML writer emits `linkedMain` or relative `linked`/`indexDiff` information outside clipboard mode; the reader reconstructs link membership by location and type. Lines 460–504, 550–605. This identifies persistence machinery, not observed reopen preservation. |

## Provenance, exposure and limitations

Collection took place on 2026-11-23 UTC; each receipt records its exact retrieval time. `sources.json` contains source IDs, public author lineage, URLs, pinned version, section/symbol, confirmed facts, unverified claims, access failures and request costs. All ten descriptions are current bodies, not verified first revisions. Several candidate bodies themselves contain proposed-fix summaries, compile-test claims or timing results. The initial underscoped issue-search output also exposed release checklists. `exposure-log.json` records these unavoidable or accidental body-level exposures; they were not used as verified outcomes.

No donor fields, experimental-design materials, selected PR patches, comments, reviews, downstream tests or later PR conclusion pages were read. Raw issue API receipts retain ordinary status metadata, but only identity/date/title/body extracts were displayed during mandatory direct reads. No runtime test or UI reproduction was performed. Original issue access failed with 403; a single official-domain search did not find a matching report. No further recruitment expansion was performed.

The work used 34 external request attempts, created no paid resources, changed no account or application state, and sent no external messages. Output was confined to `docs/workstreams/research/AF-RES-077/recruitment/musescore/`; no git commit was created.
