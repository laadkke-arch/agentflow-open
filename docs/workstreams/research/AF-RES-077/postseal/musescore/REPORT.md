# AF-RES-077 — MuseScore post-seal evidence

## Findings and status

**Primary count remains 0.** PR [#4590](https://github.com/musescore/MuseScore/pull/4590) remains an auxiliary part-creation report. The original tracker still returns **HTTP 403**; its author, body, attachments and affected release remain unknown. The baseline is the contextual release **v3.0.1, `06a66a2206fc5f3c2c33d7ee4123badf496bc4dd`**, not a verified reporter build.

The post-seal evidence establishes an adopted code change and relevant original regression-test source. It does **not** establish a passing historical test run or a new MuseScore run. **MS-N/MS-E/MS-X: 0 of 3 executed; pass and fail counts unknown.**

## What actually merged

The PR API and timeline record merge on `2019-03-07T09:53:22Z`, by `anatoly-os`, at merge commit `16851045c9e50eafb016c5cf4f2733f974e841bf`. The PR head is `3cfc174c665b01e57ef374fbb990c8f36910019a`, parent `a504e3905fdee1345981cdd5c98a9e1dd0716b4a`.

The [changed-file receipt](https://api.github.com/repos/musescore/MuseScore/pulls/4590/files) contains exactly one file and one added line in `Element::Element(const Element&)`:

```cpp
_flags = e._flags;
setFlag(ElementFlag::SELECTED, false);
```

This clears selection in the global element copy constructor. It is not confined to part creation. The patch preserves the surrounding track, position, color and other copy operations and does not modify link, undo or serialization code. **It adds or changes no tests.** Adoption is a historical fact; it does not prove the change satisfies every preservation condition.

Three [discussion comments](https://api.github.com/repos/musescore/MuseScore/issues/4590/comments) were returned. The author links the original issue and asks about side effects. `dmitrio95` supports avoiding selection inheritance and observes that callers already clear selection explicitly; the author agrees. Both displayed associations are `CONTRIBUTOR`. These are design opinions, not reports of an executed test. No review submissions or inline review comments were returned.

## Historical execution evidence

| Evidence category | Retrieved evidence | What can be concluded |
|---|---|---|
| Original regression source | Pinned test C++, CMake, docs and ten actual `.mscx` input/reference files | Expected checks and test coverage can be inspected; no pass follows from source. |
| Contributor discussion | Three comments, no commands/logs or pass claim | Intent and concern about side effects are documented. |
| Actual historical execution receipt | Head and merge status lists empty; head checks and Actions counts 0; public checks page reports no jobs; Travis lookup 404 | No historical result was retrievable from these bounded endpoints. This does not prove no historical test ran. |
| New researcher MuseScore execution | None | No build, GUI, original suite or common-case result is claimed. |
| New researcher static inspection | Blob verification, XML parsing and source-reference comparisons | Findings concern the stored files, not application execution. |

The status API's aggregate `pending` value accompanies `total_count=0`; it is not evidence of a running or failed CI job. The pinned CI configuration is retained as configuration source, not as an execution receipt.

## Original tests and real fixtures

All source below is pinned to the baseline SHA. `source-manifest.json` records exact URLs, UTC retrieval times, Git blob hashes, SHA-256 hashes and receipt paths. There are 35 source files, including ten `.mscx` files; 22 blob hashes were independently matched to GitHub directory metadata. These are one `MS-CODEBASE` lineage, not additional independent works.

| Original test | Actual inspected inputs/reference outputs | Relevant assertion |
|---|---|---|
| `TestParts::createPart1` / `testPartCreation` | `parts/part-empty.mscx` → `part-empty-parts.mscx` | Creates Alto and Tenor parts and compares the saved whole score. |
| `TestParts::voicesExcerpt` | `parts/voices.mscx` → `voices-ref.mscx` | Maps Piano tracks `1→0`, `2→1`, `4→4`; maps Trombone `11→0`; compares serialized reference. |
| `TestParts::addBreath` / `undoAddBreath` | `part-empty-parts.mscx` → `part-breath-add.mscx`; undo → `part-breath-uadd.mscx` | Uses `startCmd/endCmd`, then undo and a whole-score reference comparison. |
| `TestLinks` linked-staff/part cases | Programmatically constructed scores | Checks staff/excerpt counts and linked-element cardinalities through delete/add and undo/redo. |
| `TestExchangevoices::undoChangeVoice` | `exchangevoices/undoChangeVoice.mscx` → `undoChangeVoice01-ref.mscx`; undo → `undoChangeVoice02-ref.mscx` | Moves selected bottom notes to another voice in a score with a linked Piano part, then compares the undo reference. |
| `TestReadWrite::barlines` / `undoreset` | `readwriteundoreset/barlines.mscx` serves as input and expected undo output | Resets positions, undoes, saves and compares. |
| `TestElement::testIds` | Elements constructed in memory | Compares element type after write/read; it does not assert clone selection behavior. |

These paths are under `mtest/libmscore/`. Full original test files are retained, and `report.json` gives function/line locations. Relevant limits are visible in the source: `styleScoreReload` is inside `#if 0`; `measureProperties` is an empty slot; the post-insert reference assertion in `insertMeasure` is commented out. A test name alone is not evidence that a behavior is tested.

### What the expected files show

The breath-add reference differs from its input by two breath elements: one in the master and one in Alto. The Tenor score subtree is identical. The breath-undo reference is **byte-identical** to the input. These are concrete expected scope and restoration relationships.

The voice-undo reference restores the input's pitch/voice sequences in both master and linked Piano part, but is **not byte-identical** to the input. It also contains eight tuplet-style tags and two beam-geometry blocks. Thus an assertion about musical restoration is distinguishable from a demand for raw original-file identity. The exact source-file diffs are retained.

`MTest::saveCompareScore` saves the entire score and runs `diff -u --strip-trailing-cr` against the reference. This is a whole-score **test oracle**; it does not show that undo uses whole-score snapshots. None of the ten inspected fixtures contains a `selected` or `undo` tag. Serialized snapshots therefore do not directly test transient selection lists/colors or in-memory object identity.

## Undo, selection and preservation

The pinned code collects low-level commands between `Score::startCmd/endCmd`. `UndoCommand` undoes children in reverse order. `ChangePitch` retains a `Note*` and pitch/tonal-pitch-class values and swaps old/current values on `flip`; `LinkUnlink` changes link membership. `UndoStack` starts at index zero and performs no undo at zero. The existing loader constructs a new `MasterScore`, loads the file and lays out its scores.

The baseline copy constructor inherits `_flags`, while `Selection` maintains a score-owned list and `Element::curColor` consults the selected flag. The historical patch targets that transient mismatch. Linked excerpt creation independently maps tracks and registers links; ordinary property writing emits link locations and durable properties but omits `SELECTED`. The relevant original code excerpts, exact source hashes and line ranges are in `baseline-code-excerpts.json`.

Whole-state restoration and scoped commands have different risks around object identity, unrelated changes and transient state. The current common cases do not introduce an intervening unrelated edit or stale snapshot. A correctly captured whole-state restoration and a correctly scoped command can therefore agree on all stated musical outputs. The historical snapshot files demonstrate useful expected-state coverage, not a mechanism comparison.

## Do the frozen cases discriminate implementations?

| Frozen case | Discriminating potential | Limitation |
|---|---|---|
| **MS-N** | General linked-edit/undo/reload preservation checks once implemented | Copying and clearing an initially false selected bit agree. It does not distinguish whole-state versus scoped undo. |
| **MS-E** | An **immediate in-memory observation after part creation** can distinguish inherited selection from cleared selection | The packet does not bind the observation to that checkpoint. A final-only check after undo/reopen may lose the transient distinguishing state. No executable harness exists. |
| **MS-X** | Can reject fabrication of a former pitch when neither file nor undo history contains it | Both mechanisms can correctly refuse/no-op when history is absent. It does not identify a preferred storage mechanism. |

Concrete fixtures, symbolic-ID mapping, pitch-command semantics, checkpoints and assertions remain unspecified. These are conditional test-design observations, **not measured outcomes**. The common-case assessment was sent before a later root message disclosed A/B preference; A/B choice artifacts were not opened, and this report is not an additional independent experimental row.

## Revision history, runtime and handoff

The current opening description matches the PR head commit message after its title. That commit is dated `2019-01-16T04:57:06Z`, providing same-author dated corroboration of the current wording. It does not establish the first PR description. The REST timeline supplies no body revision snapshots; the fetched public HTML exposes no edit-history link or edited marker. **First revision remains unverified**, and no access bypass was attempted. The original tracker remains unknown after a fresh 403 response.

The environment lacks CMake, CTest, Xvfb and MuseScore executables; Qt5 package checks and the qmake launcher fail. Nothing was installed. [RUNBOOK.md](RUNBOOK.md) provides the pinned build requirements, original command sources, a private-prefix build/test command sequence, and the remaining work to make the frozen cases executable. Existing copied code is evidence data.

Structured results are in `report.json`. Collection used **58 external GET attempts**: 54 GitHub connector reads and four public HTTP reads. The original tracker failed with 403 and the Travis lookup with 404. No paid resource, account change, external message, application test, GUI operation or git commit occurred. All writes are confined to the assigned post-seal MuseScore directory.
