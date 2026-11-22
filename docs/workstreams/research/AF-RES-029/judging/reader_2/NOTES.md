# AF-RES-029 — masked reader 2 notes

## Status and scope

These are the initial judgments of a fresh, separate context of the same model. They are **not independent human adjudication**. The assigned inherited research SHA was `a4894493dbacdc9d93357426f8bd63929074bf30`; no git operation was used to change or verify it. No branches or commits were made.

The assigned subset contains four design events, Q02, Q05, Q08, and Q11, represented by twelve opaque packets. All twelve packets are preserved, including both empty Q02 packets. The output contains sixteen candidate uses and 168 frozen predicates: 48 partial and 120 whole predicates, each assessed on two evidence surfaces. The twelve packets are not twelve independent design events. These counts must not replace the study's event denominator.

`judgments.jsonl` was created as a new file and remained unmodified during verification. Every candidate has a separate assessment, version boundary, novelty classification, caller compatibility, remaining-work boundary, and predicate-level reasons. No candidate is completed by pooling unrelated candidates' features. The two empty packets are observed retrieval/return failures, not evidence that no component exists.

## Read order and allowed material

The actual read log records these opening steps in UTC on 2026-11-22:

| Step | Time | Material |
|---|---|---|
| Scope | 12:50:29.871 | Root `AGENTS.md` |
| Protocol | 12:50:36.463 | `ADJUDICATION.md` and `reader_2-assignment.json` |
| Frozen requirements | 12:50:42.621 onward | Only Q02/Q05/Q08/Q11 records were displayed from `frozen-questions.jsonl`; truncated views were reread |
| Actual first texts | 12:51:05.928–12:51:09.862 | Q08 first PEP 778 text, Q02 initial issue body, Q05 first PEP 667 text, Q11 first NEP 55 text |
| First opaque packets | 12:51:16.371 onward | Packet candidates and their sealed citations |

All four actual first texts were read before any packet candidates. Their exact paths were:

- `docs/workstreams/research/AF-RES-029/streams/go/bodies/43744-initial.md`
- `docs/workstreams/research/AF-RES-029/streams/python/originals/pep-0667-b06bbdf9c6ac.rst`
- `docs/workstreams/research/AF-RES-029/streams/python/originals/pep-0778-78c4086b041d.rst`
- `docs/workstreams/research/AF-RES-029/streams/numpy/first_texts/NEP-55.rst`

Twenty-six distinct evidence files named by the assigned packets were read. Delivered bodies were substantively inspected, including chunked rereads after large tool outputs were truncated. No route directories, route inputs, common source files, source/return ledgers, ranking key, another reader's output, later proposal drafts, external search, web pages, personal-context search, or supplementary implementation files were read. Reading the shared frozen JSONL parses the file but displays only the four assigned records; this distinction is recorded in the log.

The read log records file reads, timestamps, and exposed ranges or filtering where relevant. Three metadata-only key inspections after context compaction were logged immediately afterward with an explicit note rather than an invented earlier timestamp. Programmatic validation reads of already read inputs and the initial output are also logged. Local UTF-8 byte counts describe saved files, not network transfer volume; no HTTP/token instrumentation was available or inferred.

## Counts

### Candidate completion verdicts

| Scope and surface | Supported | Conflict | Unverified | Candidate total |
|---|---:|---:|---:|---:|
| Partial, opened | 4 | 3 | 9 | 16 |
| Partial, exact returned citations | 1 | 3 | 12 | 16 |
| Whole, opened | 0 | 4 | 12 | 16 |
| Whole, exact returned citations | 0 | 4 | 12 | 16 |

### Predicate verdicts

| Surface | Supported | Conflict | Unverified | Predicate total |
|---|---:|---:|---:|---:|
| Opened | 34 | 11 | 123 | 168 |
| Exact returned citations | 24 | 11 | 133 | 168 |

There is a supported partial candidate in three opened-evidence packets and one returned-citation packet, all for Q11. No whole candidate is supported. The empty packets remain present but contain no fabricated candidate or predicate objects.

| Packet | Question | Candidates | Partial opened | Partial returned | Whole outcome |
|---|---|---:|---|---|---|
| P28947817c6ea | Q11 | 1 | Supported | Unverified | Unverified |
| P143dfc1244f6 | Q08 | 2 | Both conflict | Both conflict | Both conflict |
| P415f8f3436b9 | Q08 | 2 | Both unverified | Both unverified | Both unverified |
| P8658a4105080 | Q11 | 2 | Both supported | Both unverified | Both unverified |
| Pe82a7bfdf306 | Q05 | 1 | Unverified | Unverified | Unverified |
| P409353b80998 | Q05 | 1 | Unverified | Unverified | Conflict |
| Pefb6d94150a0 | Q08 | 2 | Both unverified | Both unverified | Both unverified |
| Pac9cb3093e57 | Q11 | 1 | Supported | Supported | Unverified |
| P020519ecc00e | Q02 | 0 | Empty | Empty | Empty |
| P3f93ca18f41e | Q02 | 0 | Empty | Empty | Empty |
| P2441d63a934f | Q02 | 2 | One unverified, one conflict | One unverified, one conflict | One unverified, one conflict |
| Pc7e96787b261 | Q05 | 2 | Both unverified | Both unverified | Both unverified |

## Consequential judgments and interpretive boundaries

### Q02 — benchmark unit properties

The benchfmt component supplies an incremental parser, unit/key/value records, a metadata map, and direction/assumption accessors. Its package documentation and `reader.go` independently support P1. The statistical-assumption contract supports W5. benchstat also directly documents the requested default/nonparametric/exact treatment in its own Units section.

The delivered parser positively contradicts the frozen cross-key merge counterexample. In `E59b5b9a6f5964c9b`, `parseUnitLine` L349–377 keys the map by the literal property key and checks conflicting values only for the same `(unit,key)`. `higher=better` and `lower=better` become two different keys and both are stored. That is a conflict for P3/W2, rather than an inference from silence. This implementation is not automatically attributed to benchstat without a documented dependency in the allowed evidence.

The alternate documented syntax `better={higher,lower}` is not itself rejected: the first issue does not require exclusive punctuation. However, a complete normalization of all four frozen formulations was not shown. Incremental access to accumulated metadata also does not establish the complete consumer-side application of properties to every following result. A unit-property CLI path is not shown. Adding these core missing semantics cannot be called residual parser integration.

Version boundary: pkg.go.dev displays the shortened version `v0.0.0-...-4febdb0`, published November 17, 2026. The source URL is HEAD with an observed blob, not a pinned repository commit. The documentation and HEAD implementation are not asserted to be exactly the same revision. benchstat is a same-named use; the distinct benchfmt Reader/UnitMetadataMap is a new component within the explicitly named Go benchmark family.

### Q05 — live namespace views

The current datamodel supplies explicit write-through behavior for `frame.f_locals`, supporting P1. Its exact section does not explicitly describe freshness of the same retained view or the entire thread/generator/coroutine boundary, so those remain unverified in that packet. The frame-member tables alone, for either Python 3.11 or the current manual, do not establish mutation behavior. No remembered CPython behavior is used to convert the older table's omissions into a conflict.

The Python 3.13 C frame API gives stronger evidence: it explicitly makes the proxy always up to date with the live frame locals, supporting P1/P2. A coherent C composition—`PyEval_GetFrame`, repeated `PyFrame_GetBack`, then `PyFrame_GetLocals`—supports selected-depth and explicit-frame access. Selecting/traversing the requested depth and managing references is permitted interface wiring; it does not implement live namespace behavior.

The same packet positively contradicts the frozen whole design. `E00ec94f48c396a33` L10–17 and L38–42 says optimized-scope `locals()` is an independent snapshot and the old `PyEval_GetLocals()` continues returning a borrowed cached mapping. These conflict with W1, the class/function portion of W2, and W5. Deprecation is not the required always-raises behavior.

The existence of generator/coroutine frame accessors does not by itself establish edit preservation on resume in the required threaded setting. P3 remains unverified even for the stronger proxy packet. Repeated-view equality, arbitrary extra-key retention, and the first draft's dynamic name assertion are not silently inferred. The malformed `nonlocal` example and ambiguous pseudocode were preserved; no corrected example was treated as verified.

Version boundaries remain separate: the C documentation is 3.13.18, current `/3` documents identify 3.15.2, and the older inspect table is 3.11.18. The proxy change beginning in 3.13 is not backported to 3.11. These are same-named uses because the original draft already names `f_locals`, the debugger operation, and the relevant C frame access.

### Q08 — wheel links

The PyPA wheel and RECORD sources provide useful surrounding installation/version/inventory contracts. Their actual frozen link predicates remain unverified. A major-version rejection rule does not require a generated LINKS wheel to declare version 2.0. Unpack/spread does not entail target preflight. An installed-file removal inventory does not specify no-follow deletion. The wheel 1.0 example is not treated as positive evidence that a LINKS wheel declares 1.0. These are same-named baseline uses.

The pinned Bazel Fileset source is a conceptual algorithm reference with a real finite traversal guard and cycle detection. It is not credited as an operational wheel graph validator. It treats nonrelative link targets as strings in an in-memory Fileset and expressly tolerates out-of-fileset links. Cycle/long-chain branches warn and omit offending entries while processing the rest; full resolution catches dangling/cyclic errors and logs them. Its output is a pruned manifest, not rejection of the invalid graph. This produces conflict judgments for P1/W3 and P3/W4 against the frozen complete-plan validation purpose.

The cycle interpretation is exposed rather than hidden: if “reject” were read as merely omitting a cyclic edge while accepting the rest, the P3 fragment could be read differently. This reader retained the independent purpose of validating the complete LINKS graph before creation and W4's explicit graph-rejection language. The source is not claimed to traverse indefinitely or emit the cyclic edge. A port that adds wheel roots, actual-tree existence checks, and graph failure would implement core validation work.

Goomba supplies actual package operations. It documents symlink recreation and explicitly states that Unlink removes symlinks without following them. W7/W9 receive support for these operational fragments within its Conda record API. Ordinary-file copy/hardlink fallbacks are not misread as a policy to copy symlink targets. However, its destination boundary is an environment prefix, and it explicitly permits links between different packages. This conflicts with the frozen same-wheel containment requirement. Missing-target and bounded-cycle validation remain unverified. A wheel caller would need Go/Conda metadata adaptation, while adding the missing graph checks is core work. Unlink must not run concurrently with Link in the same prefix.

Both Bazel and Goomba are new targets relative to the first wheel draft, but neither completes the independent partial action. No whole result is manufactured by combining their fragments with PyPA contracts. The first draft's source/target orientation disagreement remains unresolved.

### Q11 — variable-width NumPy strings

The strings manual directly supports variable-width UTF-8 `np.array` construction without a maximum parameter, same-pass strict rejection via `coerce=False`, and the sentinel categories. The earlier L46–50 contract explicitly associates StringDType with NumPy indexing/broadcasting and arrays of Python strings. Together with its ordinary inference example, this supports the complete partial use and W01 on the opened surface.

The narrow returned sections in P28947817c6ea and P8658a4105080 omit that Python-string/indexing contract and ordinary inference example. A one-dimensional array's printed quotation marks are not treated as proof of Python `str` scalar behavior. The generic ndarray PDF return supplies shape/dtype/indexing but no strict variable-width StringDType construction. Those returned partial uses remain unverified.

The generic ndarray candidate's opened assessment uses the explicit configuration `np.array(..., dtype=StringDType(coerce=False))` documented in the same packet. This is one coherent provider/API configuration, and selecting the supplied dtype is expressly permitted by the frozen adapter rule. It does not combine unrelated tools. If candidate identity were restricted to default ndarray construction only, that opened partial would instead be unverified; the ambiguity is recorded in the candidate and retained in this initial judgment.

Pac9cb3093e57 returns the broader string manual sections and the PDF's release statement that StringDType implements a NumPy array of Python strings. It completes the partial action on both surfaces. The string manual alone is an independent sufficient URL for its supported partial predicates; the PDF is an independent alternative for P03 when the returned generic-array and StringDType release sections are used together.

The NumPy 2.1 C API supplies an explicit allocator-mutex protocol and copy-pack replacement of an entry with a new string of caller-supplied size. P28947817c6ea receives W05 support within that documented protocol: retain the allocator lock for string access/replacement, do not mutate readonly unpacked buffers, release once, and obey its GIL restriction. This does not assert safety for arbitrary unlocked ndarray writes or resizing. The C record does not explicitly document a string-memory freeing/lifetime operation sufficient to complete W04; releasing the allocator mutex is not conflated with freeing strings.

The later packet's general thread-safety advice is neither a StringDType growth/lifetime guarantee nor a positive contradiction of safe access under a supported locked contract. Full casts/ufunc coverage, unequal-parameter rejection, safe `allow_pickle=False` npy/npz round trips, and complete advanced-indexing/Python/C integration remain unverified. No serialization conclusion is imported from model memory.

Versions are kept explicit. The strings manual is 2.6.dev0, the stable PDF identifies 2.5.0, and the C API is 2.1. The 2.5 PDF requires a width for fixed-width casts while the development manual permits width inference; they also differ on possible inline short-string storage. These are not merged into a single representation/cast contract. The 2.5 None-sentinel example omits `dtype=dt`; support for the category relies on its explicit prose, not a repaired example. All NumPy candidates are same-named uses: the first NEP already proposed StringDType and this input-boundary operation.

## Delivered-text limits and unusable material

A reported total line count was never treated as delivered evidence. Material examples include:

- The initial stable PDF response delivered L0–414 rather than its reported 24,727 lines. Later records delivered discontinuous ranges that were read as such.
- The first datamodel response ended at L321, before its frame section; a separate allowed response delivered the relevant L644–658 text.
- The Python builtins response ended at L358, before the actual `locals()` entry. Snapshot evidence came from the reflection API, not an imagined later part of that page.
- The Goomba response ended at L478 although it reported a longer page. Undelivered Options/PlannedPaths bodies were not credited.
- `Ee2a121395e54cfaf`, the GitHub installer.ts page, delivered navigation/file metadata and a rendered line-number column through 620, not the implementation. Its remaining 1,194 physical lines were blank or numeric-only after the initial header range. All nontrivial text was inspected, and this record supplies no installer code support.

## Masking, memory, and independence

No route or rank key was read. However, masking is not perfect. Pac9cb3093e57's sealed citation labels literally retain “common response” and original response IDs. This reveals likely common-origin material. Repeated PyPA and frame-member citations across the assigned packets also suggest overlap, without identifying route/rank labels. These are exposure caveats, not proof of any route assignment.

Familiar APIs may activate model memory, and current supplier documents necessarily expose later implementations. Such familiarity was not used as predicate evidence. In particular, no remembered Python 3.11 failure or NumPy serialization implementation was credited or treated as a conflict. Later PEP links appearing inside documentation were not followed. The reader had no access to another reader's judgments and made no independent-human claim.

## Sufficient-source sets and verification

For every supported predicate, `opened_support_sets` and `returned_support_sets` explicitly identify sufficient URL sets. Separate singleton sets mean independently sufficient alternatives; one multi-URL set means a required conjunction. Unsupported/conflicting predicates have empty support sets, even when their evidence arrays contain a useful fragment or a contradiction. In particular, Q05 W4 requires the frame and reflection API URLs jointly; it must not be counted from just one. No first-URL ranking key or top-one scoring was read or performed.

Structural verification checked all twelve packet IDs, candidate identities, every frozen predicate ID exactly once per candidate, evidence IDs and URLs within each packet/candidate's permitted surface, nonempty sufficient sets exactly for supported statuses, and scope verdicts as conjunctions with conflict precedence. Exact returned section boundaries were checked while assigning each source. Verification did not mutate the initial judgment file or fetch additional evidence. The initial verdicts are preserved for the coordinator's later hash seal and separate reconciliation.
