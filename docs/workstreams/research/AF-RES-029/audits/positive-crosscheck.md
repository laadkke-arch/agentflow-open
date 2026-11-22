# AF-RES-029 — exposed positive crosscheck

This is a separate-context, same-model **exposed reread**, not an independent human adjudication. It reviews Q01, Q04 and Q10 apparent partial positives from reader 1, followed by the coordinator-authorized Q11 citation sensitivity from reader 2. It changes no initial reader file. All three reader 3 hashes match the previously completed files; the JSON records those hashes.

## Results

| Question / audited packet(s) | Full returned evidence | Original first-document sensitivity | Audit decision |
|---|---|---|---|
| Q01: P916c66b4c2f1, P70dfae1f8126, Pf24318507ac9; six JavaScript/PHP candidates | Native-language extraction/defaulting is supported. Practical reuse from the fixed Go caller is unverified. | A single native-language document supports the analogy, not the Go input/output bridge. | Separate native capability from an operational Go reuse claim. |
| Q04: Pa90cc5b68c40; Kfc9303e5ce | Supported. | Unverified using setInt32 alone. | Agree with the full positive; preserve the two-URL conjunction. |
| Q10: Pe542423e34cc; K29fe78f3c6 | Supported. | from_dlpack supports P01/P02, but P03 remains unverified. | Agree with the full positive and the producer-export gap in the first URL. |
| Q11: Pac9cb3093e57; K3d245ae3ce | Supported through the returned strings documentation plus PDF. | Strict P03 reading: unverified using strings HTML alone. | Preserve full positive; remove the HTML-only P03 sufficient set in this exposed sensitivity. |
| Q11: P28947817c6ea; K4f47fffc26 | Unverified, agreeing with the initial returned negative. | Unverified. | The same strict reading also qualifies its initial opened positive. |

Seven packets and ten candidates were reviewed. Nine candidates were initially returned-positive: six receive a Go caller-compatibility qualification; the remaining three retain their full returned positives. One additional Q11 returned-negative candidate was inspected for the requested comparison. No runtime test or new web evidence was used.

## Q01: the language behavior is established; the Go caller boundary is not

The frozen caller is a Go developer processing `opts ...interface{}` in `NewExtParam`, retaining existing type assertions and downstream conversion. The frozen residual adapter may bind already prepared positions to Go variables and integrate syntax. It may not implement extraction or missing-value padding itself. This audit does **not** require new Go syntax for partial completion.

The JavaScript evidence, **E513900890968df8c**, directly supplies positional bindings at L376–387, defaults at L332–348, missing positions at L389–400, ignored trailing values at L437–453 and bounded iteration at L539–551. Selecting literal `null` defaults is configuration of a supplied behavior. Without those defaults, missing values are `undefined`, so the configured use matters. The PHP evidence, **E489b7d69fc2ceb41**, supplies distinct-variable extraction at L474–502, ignored positions at L502–511 and missing-key nulls at L549–555. The diagnostic attached to an absent PHP key is documented, not a silent failure: E_WARNING in PHP 8.0+, E_NOTICE earlier. The frozen partial does not require warning-free operation.

Those statements entail the native-language actions. They do not identify a supplier interface through which the actual Go heterogeneous sequence reaches a JavaScript iterable/PHP array and the result returns with the values and type distinctions needed by the Go caller. “Supply a representation” is not evidence of that bridge. Conversely, this absence is not evidence that a bridge is impossible. Both operational predicates should therefore be **unverified**, not conflict, when evaluating the fixed Go use. The JSON preserves native semantic support separately for every candidate.

The opened SWIG document **Ee9cbe7a0f1e1ccd4** does not close this gap. L14–18 identifies C/C++ varargs; L109–148 describes bounded, often uniform-type replacement; L186–248 explicitly uses Python-dependent argument extraction and custom typemaps. It is not a documented Go-to-JavaScript/PHP composition and was not returned as either candidate. PHP overview indexes likewise add no bridge contract.

A component tally intentionally abstracted from caller compatibility may retain all six positives, but should label them as native-language capabilities or design analogies. They do not establish direct operational reuse by the fixed caller. PHP list was explicitly named for the same use in the first design; the JavaScript supplier is a new target relative to that text. Neither novelty label repairs compatibility.

## Q04: verify the actual shared buffer, and retain the conjunction

**E5583b2882b0890ea**, the returned setInt32 page, really delivers L182 and L203–235. It states the four-byte signed-integer write, caller-selected byte offset, byte-order parameter and bounds condition. That proves the encoding operation, but not which WebAssembly memory the view references.

**Eeade3ea945731b8b**, the separately returned Memory page, really delivers the necessary connection. L174–178 describes instance-accessible memory and recommends DataView for Wasm's little-endian representation. L198–207 identifies the underlying buffer and warns that growth detaches the old buffer. L221–246 actually shows a DataView of imported memory, writes to it, invokes an export consuming the values, and demonstrates access to exported memory's buffer. These are delivered body lines, not an inference from a reported document length: the stored responses contain setInt32 L0–363 and Memory L0–631.

The full partial action is supported. Its returned sufficient set is **{setInt32 URL, Memory URL}**, a conjunction, not two independent alternatives. P2 can use Memory alone, but P1 needs the signed-integer method contract together with the Wasm-memory connection. Restricting the return to the first method URL leaves the complete partial unverified. The uncited DataView overview **Eb838c0c6fc168477**, L187–214 and L325–328, is opened corroboration only.

The caller may select the actual current module buffer and correct stack offset, set `littleEndian=true`, and invoke the already known export. The API performs the core encoding/write. This agrees with the frozen residual-adapter rule. It does not establish Go compiler export selection, linking or ABI behavior, and no whole-completion claim is added. DataView.setInt32 was already explicitly named for this use in the initial design.

## Q10: consumer requirements do not establish NumPy producer export

The first document **Eb3ab8a1b74799214** delivers the complete from_dlpack page, L0–148. L99–121 supplies the consumer signature, producer protocol requirements, CPU device constraint, `copy=False` behavior and ndarray return. L133–140 gives a CPU producer-view example. It independently supports P01 and P02. The input's obligation to implement `__dlpack__` and `__dlpack_device__` is not a statement that NumPy itself implements producer export, so P03 is unverified from that document alone.

The second returned document **E644df4baa58a773a** actually delivers L109–115 and L277–338. L111–115 supplies the strided array protocol and device-query methods. L280–294 demonstrates the NumPy view observing a producer mutation. L325–328 passes a NumPy array into `torch.from_dlpack`; L329–338 documents the writable-array restriction and shows `ext_tensor.__dlpack__()` on the export path. This is substantive provider evidence, not an imagined method based on a familiar API name. It supports P03 and, for the documented supported CPU use, all three partial predicates. Thus the interoperability URL is an independent sufficient document for the frozen partial, although explicit selection of `copy=False` additionally uses the first document's parameter contract.

The full partial and whole subpredicate W05 remain supported. W06 remains unverified: protocol device querying and the import function's device parameter do not establish the separate array-device and creation-call contract. No array-api-strict fragment is combined with this candidate. GPU-to-CPU copying, read-only NumPy export and unsupported storage are outside the selected supported CPU exchange. The observed docs are NumPy v2.5; no historical availability claim follows.

The coordinator explicitly supplied the sealed order after this audit initially inferred order from the masked packet array. That initial inference was wrong and was corrected: **Q10-A originally ranks NumPy DLPack first, with from_dlpack as its first document; array-api-strict is rank two.** Masked candidates are shuffled. The auditor did not read the key. The relevant top-one outcome is therefore P01/P02 supported, P03 unverified.

## Q11: preserve the full positive and expose the scalar-output interpretation

The first URL, **Eebead09b3e733d3c**, supplies unequal-length UTF-8 construction at L73–89 and strict rejection at L138–150. Both audited returns cite those sections, so P01/P02 survive first-URL scoring. The positive packet additionally cites L46–50, which assigns NumPy indexing/broadcasting with Python-string arrays to StringDType. L81–88 then constructs a StringDType array.

The initial reader treats that supplier description as a complete ordinary-array/Python-scalar promise. This is a reasonable documentary interpretation, and the audit preserves it as an explicit alternative. Under a stricter direct-entailment reading, however, those lines do not identify the scalar returned by indexing or show an N-D scalar selection. Because the frozen P03 explicitly includes that output, the **HTML-only sufficient set is unverified in this exposed sensitivity**. A familiar NumPy name or a printed one-dimensional array is not substituted for the missing result contract. There is no positive contradiction, so conflict would be inappropriate.

The positive packet's second returned URL supplies stronger evidence under the same PDF identity. **Ec335bc95110c3dd9**, L109–138 and L183–211 (tool pages 8–11), explicitly defines multidimensional ndarray shape, tuple indexing and sequence-of-sequences construction. **E3eb97fccf5ee602a**, L15531–15535 (tool page 422), supplies the StringDType release statement: it implements arrays of Python strings as a drop-in replacement for object arrays of Python strings and sentinels. Together, those returned PDF sections support the ordinary N-D and Python-string scalar contract. P03 retains **{PDF URL}** as its sufficient set; the complete partial needs **{strings HTML URL, PDF URL}** because the HTML supplies strict construction and variable-width behavior.

The distinction between PDF responses matters. **Ed4fc6c44f98fa409** reaches the heading at L15531 but does not deliver the explanatory release statement. **E3eb97fccf5ee602a** actually delivers it. The negative packet P28947817c6ea does not have that latter evidence; its opened PDF quickstart is generic, and its returned C interface **E86579a23a4e56cf0**, L72–145 and L192–224, describes string buffers/allocators rather than Python scalar indexing. This audit retains its returned-negative decision and records the stricter opened interpretation separately.

An official StringDType scalar-type contract or a two-dimensional construction/indexing test with a Python-str assertion could resolve the remaining first-document ambiguity. No new source or runtime result was obtained. The dev HTML identifies v2.6.dev0 and the PDF Release 2.5.0; the cited release statement is about the introduced 2.0 feature, not proof of the first proposal's date.

## Exposure and preservation

Reader 1 judgments were visible before the first three rechecks. Reader 2 access was subsequently authorized for Q11 only. Q11 evidence incidentally displayed NumPy device/export statements relevant to Q10; those are outside the Q10 packet and were not used to improve its scores. No ranking-key file, route directory, external search, later draft or new runtime evidence was read. Initial masked outputs remain immutable; the recommendations here are exposed audit results with interpretation sensitivities retained.
