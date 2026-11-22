# AF-RES-029 — reader_1 initial masked reading

## Status and boundaries

This is a separate-context reading by the same model, not independent human adjudication. The assigned design events are Q01, Q04, Q07 and Q10. The twelve opaque packets contain three packets per event; they are not twelve independent design events. The inherited fixed research SHA is `a4894493dbacdc9d93357426f8bd63929074bf30`. It is recorded from the assignment and was not revalidated through branch or commit operations in this reader pass.

The initial judgments are in `judgments.jsonl`, with one record per assigned packet, including both empty packets. There are 16 candidate uses and 123 complete candidate/predicate objects, each evaluated on both evidence surfaces. No judgment has been revised after its initial write. The coordinator should preserve this file before any exposed reconciliation.

Only the following material was read: root `AGENTS.md` for scope; `ADJUDICATION.md`; `reader_1-assignment.json`; selected frozen-question records; the four exact assigned first-text files; all twelve assigned opaque packet files; the 28 unique evidence JSON files they name; and this reader's own output for completeness checks. No route directory, route input, common source file, sources/returns ledger, ranking key, other reader output, later proposal draft, repository search, external lookup, or browser was used. Root workflow directions were applied only insofar as compatible with the explicitly narrowed masked assignment; no broader project context was opened.

All four original texts were read before any packet candidate. The log begins at `2026-11-22T12:50:20.668785+00:00`; the final first-design/predicate recovery read was at `12:50:55.736612+00:00`; the first packet was opened at `12:51:01.750791+00:00`. `read-log.jsonl` records actual file reads, their UTC times, their stages, and whether full bodies or selected records/ranges were displayed. A combined frozen-question output and one combined evidence output were truncated by the tool display. The missing Q07 predicates and the affected PHP-types/SWIG segments were explicitly reread from the same allowed files; no missing text was inferred.

## Counts

| Measure | Opened evidence | Returned exact citations |
|---|---:|---:|
| Supported predicate judgments | 33 | 33 |
| Conflict predicate judgments | 10 | 10 |
| Unverified predicate judgments | 80 | 80 |
| Supported partial candidate uses | 8 | 8 |
| Conflicting partial candidate uses | 0 | 0 |
| Unverified partial candidate uses | 8 | 8 |
| Supported whole candidate uses | 0 | 0 |
| Conflicting whole candidate uses | 10 | 10 |
| Unverified whole candidate uses | 6 | 6 |
| Packets containing a supported partial use | 5 | 5 |
| Packets containing a supported whole use | 0 | 0 |

These are reader-assignment counts, not route scores or the full twelve-event result. At least one assigned packet supports the partial action for Q01, Q04 and Q10. Q07 has no supported partial use. With the original partial/whole request boundary retained, Q01 is the only one of these four design events with any supported candidate for its requested scope. Which packets correspond to which route remains sealed.

## Q01 — extraction semantics and the Go boundary

All six returned PHP/JavaScript uses support both partial predicates on both surfaces. The evidence directly supplies the extraction operation rather than leaving a caller-written extraction loop to an adapter.

The PHP manual, evidence `E489b7d69fc2ceb41`, documents distinct positional variables, ignored elements and missing-key nulls in its returned Array destructuring section, especially L474–502 and L549–555. It also provides a mixed integer/string destructuring example. The selected boundary is a dense zero-based sequence. PHP arrays are general maps, so arbitrary sparse/associative arrays must not be presumed to have sequence semantics. Missing keys produce a diagnostic; the documented null result is not a promise about a custom error handler that converts diagnostics into exceptions. Square-bracket destructuring is identified as PHP 7.1+, and the diagnostic level changes at PHP 8.0. PHP `list` for this retrieval use is explicitly named in the first text, so all PHP uses are `same_named_use`.

The JavaScript manual, evidence `E513900890968df8c`, documents a fixed pattern, ordered values, bounded iteration and defaults. Missing bare bindings produce `undefined` (L391), which is a real counterexample to unconfigured null padding. Each JavaScript use is therefore evaluated with a literal null default on every binding and without a rest binding. Choosing the documented default expression is caller configuration allowed by the rules; it does not add an extraction or padding algorithm. This includes the generic-name JavaScript candidate in P916c66b4c2f1: its stated intended use is null-padded preparation, and its exact citation includes the documented defaults. JavaScript is not named in the first Go text, so this is `new_target`, without any inference about actual human prior knowledge.

All six whole uses conflict at Q01-W1 because the delivered operations are PHP or JavaScript syntax, not a Go-level assignment. The other whole semantic predicates are individually supported in the supplier environment; that does not erase the Go conflict. Practical usefulness is a semantic reference or a preparation step in a supplied foreign runtime. No packet establishes a bridge preserving arbitrary Go `interface{}` values. A hypothetical Go implementation of the extraction logic is explicitly left as core work, not residual integration.

## Q04 — actual memory preparation versus a representation reference

Pa90cc5b68c40's DataView candidate supports the two partial predicates on both surfaces. `E5583b2882b0890ea` supplies the signed int32 writer, offset, endianness parameter and bounds contract. `Eeade3ea945731b8b` connects a DataView to the actual `WebAssembly.Memory.buffer`, writes it, and has an exported function consume it. The same document shows obtaining exported memory. The caller may choose an ABI-correct offset and supply an already known export; those are explicitly allowed integration choices. The operation still requires `littleEndian=true`, the real module buffer, and a refreshed view after growth detaches an old buffer.

Q04-P1's returned sufficient set is the conjunction of the setInt32 and Memory URLs. On the opened surface, the additional general DataView URL can replace the Memory URL for the writer's WebAssembly context when paired with the setInt32 contract. Q04-P2 has the Memory URL as an independently sufficient source for the shared-buffer mutation boundary. The precise sections and support sets are retained in JSON, so later URL restriction does not treat a conjunction as independent alternatives.

No whole Go-export predicate is counted as supported for this candidate. The generic WebAssembly memory examples do not establish a selected Go function, its export table, the Go stack ABI or the observed Go argument value. The Go `master` compiler document was opened, but its delivered body stops at L1239 in the line-directive discussion; the reported source length does not supply a later export section. This is a source-completeness gap, not evidence that current Go lacks an export facility. DataView and `setInt32(sp + 8, id, true)` already occur in the initial text for the same purpose, so novelty is `same_named_use`.

The two export-section/linear-memory candidates in Pd2a4b8dc1ffd and Pac572e5bed71 are unverified for every frozen predicate. Their delivered draft specifies byte vectors, named export descriptors and binary encoding, but provides neither a host int32 writer nor a Go exporting implementation. The representation is useful background; implementing the operational core from it cannot be called residual wiring. Their novelty is limited to `new_component_in_named_family`: a specific binary representation contract within the already named WebAssembly family. This does not count as a new provider family or a completed operation. The source identifies Draft 2024-12-09 with GC/function-reference/tail-call extensions and a one-memory boundary; no later edition was merged into its contract.

## Q07 — empty returns and incomplete carrier evidence

P68d72d248ba9 and P6ff49030111e remain empty, with `candidates: []`. They were not dropped and no candidate was fabricated from an opened API clue.

The first empty packet contains a useful actual Annotated excerpt in `E2dd4909b3620f031`: it describes metadata storage, `get_type_hints(..., include_extras=True)` and `__metadata__`. This proves generic association/retrieval primitives, but it does not provide the single-string documentation object demanded by Q07-P1. Its no-match DocInfo response is not a universal absence proof. The other empty packet supplies generic annotation-access and qualifier documentation, again without a supplied documentation carrier.

The sole returned Q07 candidate, the CPython typing overview in Pe07ec062cdda, is unverified on all nine predicates. `Ec014f8983c210791` contains the overview through L543; its returned section identifies the overview/callable-annotation material at L1–145. Neither contains the needed carrier. `E2fee27ee68bcbd0b` delivers GitHub metadata and line-number controls, not the source body. The actual Annotated excerpt from a different packet is not credited to this candidate. The displayed `/3/` manual title is Python 3.15.2, but the URL is unpinned and no historical claim is made. Novelty remains `unverified` because no concrete carrier component is identified; membership in the already named Python typing family alone is insufficient to identify a new use.

The remaining adapter would have to supply the carrier itself, which is prohibited core repair for partial completion. Static documentation consumption, multiline cleaning and the outer nested-annotation requirement are also unverified. Absence in these excerpts is not a claim about every Python package.

## Q10 — concrete DLPack and unfulfilled whole integration

Pe542423e34cc's NumPy DLPack candidate supports all three partial predicates and Q10-W05 on both surfaces. `Eb3ab8a1b74799214` provides a concrete ndarray consumer and `copy=False` contract. `E644df4baa58a773a` documents the device-aware protocol, a CPU producer-to-NumPy view with observable producer mutations, and NumPy producer export into PyTorch. The interoperability URL alone is sufficient for all three partial predicates in its documented CPU domain; the consumer-reference URL independently supports P01 and P02 but does not establish NumPy producer export. These alternatives are explicitly separated in `*_support_sets`.

The selected configuration is supported strided CPU data, no-copy import, and a supported writable NumPy producer for export. Imported arrays are read-only in the documented example. Default `copy=None` and DLPack v1 cross-device copying are not used as evidence of an unconditional no-copy result. The delivered manuals identify NumPy v2.5, with unpinned stable URLs. This is `same_named_use`: both `from_dlpack` and `ndarray.__dlpack__` are explicitly proposed for this purpose in the first text. Q10-W02 conflicts because the delivered ndarray output has ordinary `copy()` and `sort()` methods. A useful ndarray handoff is not the frozen whole new-array class.

The two SciPy candidates support Q10-W01 for the explicitly documented composition: `array_namespace` selects a compatible input-specific namespace, `xp.asarray` creates compatible arrays, and numerical operations run through that namespace. This does not imply the rest of the strict 2021 contract. Q10-W03 positively conflicts because L128 explicitly preserves list/scalar/arbitrary-object acceptance for the NumPy path. The CPU `np.asarray` conversion note does not establish the frozen DLPack component. The source is a development SciPy v1.18.0 manual with experimental opt-in behavior, private helpers and backend restrictions. Novelty is a new concrete component within the already named SciPy family.

The abstract DLPack design-contract candidate is unverified for all mandatory predicates. It does not supply a NumPy consumer/producer implementation, and its zero-copy-where-possible language is not a concrete no-copy operation. No actual copy was inferred merely from permissive wording.

The array-object/namespace contract candidate is a later specification, not an implementation. Its Q10-W02 conflict is direct: the exact returned Methods section lists ordinary `array.to_device` at L392, while the frozen first text permits no methods other than dunders. The predicate was not repaired to fit the 2024.12 edition. Generic DLPack method names do not establish NumPy producer implementation or ndarray import.

`array-api-strict` is a concrete test implementation, but its broad current-conformance claim does not directly establish every frozen conjunction. Its page says the current standard is 2025.12 and previous versions require a flag whose details were not delivered. The full dunder-only method, promotion, exact function-interface, discovery, named underlying-operation and compatibility requirements remain unverified. Q10-W06 is supported only for the documented CPU/default configuration: `x.device` and creation-device selection are exposed, CPU_DEVICE is accepted, and values outside the listed device objects/None are rejected. The other two device identities are explicitly simulations and are not credited as hardware support. This is an individual interface finding, not whole completion.

The strict package is coded `same_named_use` because its opened relationship section identifies it as the implementation formerly named `numpy.array_api`, already proposed/prototyped in the first text. Its strengthened testing purpose and package rename do not automatically create a new underlying namespace use. The migration section informs novelty only; it is not inserted into returned predicate evidence outside the citation. Its stated NumPy 1.26/2.0–2.4 support range was not joined with the other candidate's v2.5 manual as one validated installation.

## Masking, exposure and reviewability

API names were recognizable from general model knowledge, including the possibility of later implementations. No remembered implementation, release or compatibility fact was promoted into evidence. The reader saw repeated evidence IDs and differently sized permitted packets; those could suggest a common-only baseline or expanded retrieval. No route identity or ranking was assigned or checked. Allowed cross-packet factual exposure did occur, so it is recorded rather than described as isolation: for example, the ordinary method in the 2024.12 contract was not used to mark the strict-package candidate as conflicting because that method-list evidence is absent from its packet.

There is no citation-loss difference in the completed candidate verdicts for this assignment. That does not mean every opened document was returned: the uncited generic Annotated material and DataView overview remain distinct, and an empty return remains empty. Top-one-URL rescoring must use the coordinator's sealed original ordering. This reader has retained sufficient-source alternatives and required conjunctions but has not opened the ranking key or chosen a best URL.

All support is documentary, not runtime verification. No packages were installed and no supplier code was executed. The completion checks verified that every candidate contains exactly its frozen predicate IDs, supported predicates have explicit sufficient URL sets, returned evidence belongs to the candidate's sealed citations, and all evidence IDs belong to the candidate's own packet. Local UTF-8 byte counts in the read log are not network transfer measurements; actual HTTP/token instrumentation remains unmeasured here.
