# AF-RES-029 — reader 3 masked adjudication notes

## Scope and provenance

This is a fresh separate-context reading by the same model as the coordinator. It is not independent human adjudication. The inherited research SHA supplied with the assignment is `a4894493dbacdc9d93357426f8bd63929074bf30`; no Git operation was performed to change or reverify it.

The reader evaluated Q03, Q06, Q09 and Q12 in all twelve assigned opaque packets. The outputs contain twelve packet records, three empty packets, twelve returned candidates and ninety frozen predicate rows. Each predicate has an opened-evidence status and a returned-exact-citation status, for 180 surface-level judgments. Every supported predicate has explicit sufficient URL sets. A singleton set is sufficient by itself; different sets are alternatives. Evidence items preserve exact URLs, delivered line ranges, evidence IDs and rationales. Unsupported predicates have empty support sets.

Only AGENTS.md, ADJUDICATION.md, the reader assignment, the four selected frozen-question records, the exact initial-text files they identify, the twelve assigned packets, their 26 distinct evidence files and this reader's own output files were read. No key, route directory, route input, common source/search file, sources.jsonl, returns.jsonl, other reader output, later proposal draft, supplementary research, external browser or web search was used. This reader wrote only files in `judging/reader_3/`.

## Reading order and delivery discipline

The assigned frozen questions were first read at 2026-11-22 12:50:47 UTC. The four exact initial texts were then read in full, before any packet:

| Question | Exact initial text read time (UTC) |
|---|---|
| Q03 | 12:50:55.306 |
| Q06 | 12:50:55.306 |
| Q09 | 12:50:59.672 |
| Q12 | 12:51:03.659 |

The first packet was read at 12:51:09.745 UTC. The machine check of the read log confirms that every exact initial-text read preceded it. The first combined frozen-question display and two early multi-file evidence displays were truncated by the tool output limit. The exact initial texts and affected substantive evidence were subsequently read in bounded outputs. The log preserves the actual initial file reads and the rereads, rather than rewriting their times. An inventory read is expressly labelled as an inventory, not substantive review.

Evidence scores use actual delivered source text, never a source's advertised total line count. Blank lines and standalone GitHub numeric line-number lists were omitted from some displays; no substantive source sentence was supplied by those lists. Identical overlapping builtins response lines were checked for exact equality and displayed once for the remaining body review. The returned request4 open section is E96073278c8766a25; an earlier response at the same URL stopped at L363 and cannot support open at L693 by itself.

## Candidate outcomes

These are candidate counts, not twelve independent design events. This assignment covers four of the full study's twelve events, with three opaque packets per event. Empty packets remain explicit records and do not become invented candidates.

| Surface and scope | Supported | Conflict | Unverified |
|---|---:|---:|---:|
| Partial, opened evidence | 5 | 4 | 3 |
| Partial, returned exact citations | 5 | 4 | 3 |
| Whole, opened evidence | 0 | 4 | 8 |
| Whole, returned exact citations | 0 | 4 | 8 |

| Packet | Question | Candidates | Partial returned result | Whole returned result |
|---|---|---:|---|---|
| P9a5ef68e2eae | Q06 | 1 | Conflict | Conflict |
| Pfd4c68aa9ed3 | Q12 | 1 | Unverified | Unverified |
| Paf4ebe483963 | Q06 | 0 | Empty; unverified | Empty; unverified |
| Pc56a29cd57c4 | Q03 | 2 | Both conflict | Both conflict |
| Pf332ba0ca4e5 | Q06 | 1 | Conflict | Conflict |
| P0b20ae7bc761 | Q12 | 1 | Unverified | Unverified |
| P4dff49f6c7ef | Q03 | 0 | Empty; unverified | Empty; unverified |
| P72f64351b73a | Q09 | 2 | Both supported | Both unverified |
| P9f7e2bc0ff8a | Q09 | 2 | Both supported | Both unverified |
| Padd9d9784977 | Q12 | 1 | Unverified | Unverified |
| P302680327451 | Q03 | 0 | Empty; unverified | Empty; unverified |
| P219dcfbc5934 | Q09 | 1 | Supported | Unverified |

There are three packets with at least one supported partial returned use, all for the same Q09 design event. No packet has a supported whole returned use. These packet counts must not inflate the independent-event denominator.

## Q03 — detected concurrent map writes

Both returned HACKING editions explicitly assign racing map writes to unrecoverable errors handled by fatal. Their exact returned error-handling sections are E71bccad1e99709e2 L145–151 and E7c1c747b9fb98739 L40–46. The generic advice to use panic for recoverable errors does not change the documented classification of this trigger. All two partial and three whole predicates conflict for each returned candidate, including the conjunction that would allow a recovering HTTP caller to finish the affected request.

The two empty packets remain empty. One contains only the manuals and a partial Go specification body: Ece739463f81462c0 delivers L0–434 despite advertising 3823 total lines. A later panic/recover section is not available evidence. The other empty packet additionally delivers current map implementations. E830add6c20bc5eeb L1159–1163 and Ebb8662444ac7c3eb L299–301 call fatal on the writing detector; nil-map assignment panics in a separate branch. The current implementation uses Map/m.writing rather than the first text's hmap/hashWriting. That version difference is preserved and does not establish the state of an uninspected historical runtime.

A valid residual adapter could connect an existing recoverable signal to request cleanup and an error response. Changing the detector itself from fatal to a catchable panic is the requested core behavior. A wrapper that does not change that branch cannot complete this partial action. No assertion about post-race map integrity or memory safety was added.

## Q06 — UTF-8 mode with locale-module isolation

Both returned uses provide directly documented implicit UTF-8 file decoding. The richer packet also supplies explicit encoding="locale" decoding at E96073278c8766a25 L718. These facts do not overcome the frozen locale-module requirement: E6857484659b80af5 L243 explicitly makes locale.getpreferredencoding return UTF-8, and the richer packet's E5688b682e65fdb85 L232–236 independently confirms it. The first PEP text specifically asks that this override be removed. locale.getencoding, documented as ignoring UTF-8 mode at L249, is a different API and is not accepted as a repair of that requirement.

The default-on behavior is documented for Python 3.15, in pages labelled Python 3.15.2 and unpinned CPython main. The original draft's Python-Version 3.12 is recorded as a historical boundary; the current manuals do not establish 3.12 availability. The frozen W1 predicate is evaluated for the observed supplier contract, without silently backdating it.

Opened OS text explicitly covers popen pipe contents at E1d457a280b9d1f74 L3438–3449 and E6857484659b80af5 L5581–5615. Together with the UTF-8 mode section, each OS URL independently supports W1 on the opened surface. Those pipe sections were not among the returned exact sections, so W1 remains unverified on the returned surface. This is a concrete citation loss even though the overall partial and whole verdicts remain conflict for another reason.

Neither packet directly establishes every named TextIOWrapper-derived API in W2, especially Path.read_text. The richer returned open section identifies TextIOWrapper but does not fill the remaining API link. EncodingWarning migration is also unverified in both packets. Missing evidence is not reported as absent functionality.

The empty Q06 packet includes GitHub io.rst and locale.rst responses that deliver navigation, metadata and line-number lists without the actual document prose. Their total line counts cannot supply missing compatibility details.

## Q09 — weak-scalar dtype resolution

The four NumPy candidate uses meet all three partial predicates on their own cited promotion manual. The stable edition is labelled NumPy 2.5; the development edition is 2.6.dev0. They are evaluated independently. Current kind-only handling, concrete NumPy precision retention, scalar-instance result_type examples and the explicit note about changed scalar/0-D behavior establish the required properties. The historical note is not treated as sufficient on its own; it is read with the current contract.

The direct operational path is Python-level np.result_type with original Python scalar instances and typed NumPy operands. Converting the Python class int/float/complex to a dtype first changes its strength, as the cited manual explicitly illustrates. The supplementary dtype-construction source is useful for that boundary but is not necessary for the supported predicates. Accordingly, each supported NumPy predicate retains the promotion URL as a sufficient singleton support set.

For the candidate that also names PyArray_ResultType, the delivered C signature accepts arrays and dtype objects and does not independently explain weak Python-scalar provenance. The supported Python-level path is kept explicit. The reader does not silently invent a C adapter that recreates weak promotion.

The JAX candidate also satisfies the bounded partial predicates in its documented numeric-lattice environment. E2db176fdd818b26a L318 identifies the callable jax.numpy.promote_types; L344 gives pairwise type joins, L349/L362 explicitly supply uint16 plus weak int to uint16, and L367/L391–394 distinguish strong NumPy/explicitly typed operands from weak defaults. This is operational supplier documentation for a type resolver, not merely a conceptual numeric-tower analogy.

JAX support is conditional on preserving explicit concrete dtypes and on 64-bit support when the input dtype requires it. L367 explicitly warns about the disabled-64-bit case. Mapping concrete dtypes and Python scalar kinds is allowed interface adaptation; rebuilding the lattice or inventing shape-strength rules would not be. No claim is made that importing JAX changes NumPy dispatch, that every registered NumPy custom DType is supported, or that JAX's floating/integer promotion reproduces every NumPy rule outside the frozen partial properties.

All five Q09 whole verdicts remain unverified because W06 is not established. The development manual's statement that can_cast rejects Python scalars does not establish the np.int64(100)-to-uint8 behavior. The C-API page has value-aware and legacy helpers, but no delivered statement identifies them as the current Python np.can_cast path; they are not used to manufacture either support or a contradiction for a different actor.

## Q12 — target-version selection, visibility and binary compatibility

All three returned candidates document a compile-time target control. The two reference-only packets describe NPY_FEATURE_VERSION and NPY_TARGET_VERSION but say older-runtime compatibility is possible "in principle." Import-time rejection of incompatible API/ABI combinations does not establish a successful older-baseline binary. Their P03, older-default W01 and cross-major outcomes remain unverified.

The guide-backed packet is stronger. Ebb... (full ID Ebbe59c8388b26aa9) L44–59 directly documents an older default and the NPY_1_22_API_VERSION selection example. L82–123 supplies a working 2.x-built-wheel/1.x-runtime contract and a 1.23.5 baseline example. These support P01, P03, W01, W03, W04 and W05 as documented contracts, not execution receipts. W04 credits the explicit promise that the rebuilt C/Cython extension works on both generations, which entails compatible calls within the supported API; no translation algorithm or separate compatibility-package requirement is invented.

P02 and W02 remain unverified even in that stronger packet. The frozen requirement specifically hides newer struct fields and functions at the selected/default old target. An older-compatible exposed API and a macro that enables new features do not directly establish every required visibility gate: some compatibility can also come from backports. No delivered header guard or negative compile test supplies that missing claim. Requiring the caller to add these guards would assign core behavior to the adapter. The judgment is an evidence gap, not a claim that NumPy lacks the feature.

W06's concrete replacements for changed/removed NumPy 2.0 C-API are not supplied. A link to the migration guide is not its contents. A later DType compatibility slot documented for 2.5 is preserved as context and not substituted for the full 2.0 migration contract. The two failed navigation responses in Padd9d9784977 are exact failed fetches and add no supplier evidence.

The guide's 1.25-to-1.19 default, 1.22 target example and 2.x/1.23.5 cross-major example remain distinct. They do not produce a fabricated guarantee that every possible older baseline works across the major ABI break.

## Novelty, masking and exposure limits

Every returned candidate is classified as same_named_use. The first Go text already names the runtime detector and panic/recover; the first Python text names UTF-8 mode, its text-I/O APIs and compatibility controls; NEP 50 explicitly names NumPy result_type and JAX weak promotion; NEP 53 explicitly names NPY_TARGET_VERSION and its older-baseline build use. Finding a new manual or an ancillary inspection macro does not make the already proposed core use novel. Actual human prior knowledge and saved labor are unverified.

The packet set necessarily exposes provider identity, repeat source IDs, multiple editions and later current supplier contracts. This makes shared/common provenance potentially guessable. The reader did not infer or use a specific route/rank label, and did not access the key. Evidence was credited only within the packet that lists it. No candidate fragments were combined across unrelated uses or across packets. General pretrained familiarity with public APIs remains a possible unmeasured memory exposure; no prior conversation or retrieved memory was used.

## Validation and remaining work

The output was mechanically checked for all twelve packet IDs, preserved empty packets, every frozen predicate per candidate, valid three-way statuses, evidence IDs confined to each packet and returned URLs confined to each candidate's returned citations. Every supported predicate has at least one sufficient support set; all conflict/unverified rows have none. These are output-integrity checks, not implementation or supplier runtime tests.

The coordinator can rescore any first-URL sensitivity using the returned_support_sets without this reader consulting the ranking key. Predicate-level gaps name a next minimum official source capable of changing the judgment. No such supplementary source was opened during this sealed reading.
