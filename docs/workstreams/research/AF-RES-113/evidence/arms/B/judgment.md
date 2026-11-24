# AF-RES-113 — Route B sealed-packet judgment

**Result: 0 eligible novelty findings across 6 slots.** Five extra-text slots are unavailable. R3 supplies an article preview whose network-fusion topic does not support the requested scalar empty-neighbor repair while preserving pairwise errors.

## Audit and evidence boundary

- Reader: fresh automatic document reader; not a human experiment or independent developer-adoption observation.
- Start UTC: `2026-11-24T04:14:58.945727+00:00`
- End UTC: `2026-11-24T04:20:20.709923+00:00`
- Packet SHA256: `3e79f554a5bb84cb6ec9eafe551cc164978af7b287124cd8fc8236d0450fc03b`
- Receipt SHA256: `833cc707bb222942fb794319991d93b88ee559bcd77c4c99820d97e81461bb42`
- Packet digest, all nonempty source-text digests, per-slot extra lengths, and receipt values match.
- External opens: **0**. Target projects/tests/experiments executed: **0**. Cross-route exposure: **false**. Git operations: **0**.
- Only Python JSON/hash/read/write processing was performed. No citations, build logs, comments, methods, figures, target project files, other routes, or postseal verification material were opened.
- Packet seal commit was reported by the parent as `11287afdf0c3a0d990f125b72c4f75e9af42f38f`; no Git verification was performed. The packet embeds common seal `96a754e80f9bbeb5f65e544f7e7f81457b245971`.

Files read, in full:

- `/workspace/scratch/7e9d1ab33296/agentflow-open/docs/workstreams/research/AF-RES-113/evidence/arms/B/packet.json`
- `/workspace/scratch/7e9d1ab33296/agentflow-open/docs/workstreams/research/AF-RES-113/evidence/arms/B/packet-receipt.json`

Python read packet bytes `[0, 56191)` (55136 Unicode codepoints) and receipt bytes `[0, 1178)`. The full receipt text, all packet metadata, and every parsed field of all six requests were displayed and read without output truncation. This included every original opening body, full common API text, full extra text or explicit vacancy, and the full frozen baseline. The original packet's insignificant JSON whitespace was not separately displayed. No source-text judgment relies solely on a baseline summary.

### Source-text exposure

| Slot | Opening body codepoints | Common text codepoints | Extra text codepoints | Extra status | Images seen |
|---|---:|---:|---:|---|---:|
| R1-B | 524 | 5172 | 0 | vacant_link | 0 |
| R2-B | 1437 | 0 | 0 | vacant_start | 0 |
| R3-B | 2259 | 6857 | 3000 | abstract_only | 0 |
| R4-B | 1493 | 1384 | 0 | vacant_link | 0 |
| R5-B | 1501 | 3407 | 0 | vacant_link | 0 |
| R6-B | 2703 | 0 | 0 | vacant_start | 0 |

All listed source-text sections were read completely; zero-length sections were inspected as vacancies. The JSON judgment records each section's UTF-8 length and SHA256.

## Six-slot decision table

| Slot | Extra classification | New relevant implementation | New relevant discriminating test | Eligible count |
|---|---|---|---|---:|
| R1-B | Unavailable: vacant link | None | None | 0 |
| R2-B | Unavailable: vacant start | None | None | 0 |
| R3-B | Insufficient for target; new fusion topic is irrelevant; citation/formulas already common | None | None | 0 |
| R4-B | Unavailable: vacant link | None | None | 0 |
| R5-B | Unavailable: vacant link | None | None | 0 |
| R6-B | Unavailable: vacant start | None | None | 0 |

A useful comparison reproduced below remains opening/common evidence. It does not fill an unavailable extra slot and does not receive novelty credit. Predictions are conditional and unexecuted; source reports are labeled separately.

## R1-B — unavailable; novelty 0

**Original target.** Stream the same filename.mkv with block_length=10, frame_length=16000, hop_length=16000 without the reported unknown-format error, preserving iteration into tokenizer(speech, return_tensors="pt").

**Old approach.** The opening post reports that load(filename.mkv, duration=10, sr=16000) succeeds, while stream(filename.mkv, ...) fails with an unknown-format error.

**Preserved conditions.** The original MKV remains the input. The generator is consumed as audio chunks by the original tokenizer loop.

**Changed unit, order, or responsibility.** No change is newly supported by extra text. The frozen common baseline separates decoder/container acceptance from chunk geometry, target sample rate, frame padding, and generator cleanup. The common API limits accepted codecs to soundfile support. No extra evidence supplies a decoder change for the same MKV.

**Extra evidence.** Status `vacant_link`; 0 Unicode codepoints; 0 images.
No additional source observation is available.

**Smallest concrete input available from the opening/frozen baseline.** The original filename.mkv with the exact stream parameters and tokenizer loop. A smaller concrete failing file is not established. The frozen supported-reference-file control is already common evidence, not a new Route B test. Origin: Opening body; the actual file bytes and codec are not supplied.

**Two-output distinction.** The opening supplies the load-success/stream-error report, but no extra supplies an alternative decoder path whose output for the same MKV can be predicted. Success on a different soundfile-readable input would not show repair of the original input.
No justified old-versus-repaired output pair is supplied; no alternative numerical result is filled in.

**Source-supported observations, distinct from reader predictions:**

- The author reports load success and an unknown-format error on the stream path. Source: `issue_current_body`.
- The inspected API text documents soundfile-supported codecs, generator blocks, optional resampling with an integer compatibility condition, center=False for frame analysis, and explicit close on early termination. These are all common exposure. Source: `common_text`.

**Reader prediction status.** No additional implementation-output prediction is made.

**Counterexample or limitation:**

- A sample-rate, centering, or block-size adjustment need not change decoder acceptance, so it cannot be credited as the missing MKV repair.
- The MKV codec/native rate, tokenizer requirements, and actual current-version runtime behavior remain unknown.

**Eligibility.** additional_text is empty (vacant_link). There is no extra-source implementation decision or discriminating test to count.

**Frozen-baseline assessment.** No substantive disagreement; the frozen decoder-evidence hold remains warranted.

**Evidence locations:** `packet.json#/requests/0/issue_current_body`, `packet.json#/requests/0/baseline`, `packet.json#/requests/0/common_text`, `packet.json#/requests/0/additional_text`.

## R2-B — unavailable; novelty 0

**Original target.** Provide pitch-contour sonification in librosa with graceful unvoiced NaN handling and an sr/hop_length sampling grid, avoiding onset/offset scoops associated with the reported nan_to_num workaround.

**Old approach.** The author uses mir_eval pitch_contour, explicit time measurements, and nan_to_num(f0), and reports onset/offset scoops.

**Preserved conditions.** Retain sonification of the supplied f0 contour. Handle voiced/unvoiced transitions without the reported scoops. Support the requested frame-based grid.

**Changed unit, order, or responsibility.** No change is newly supported by extra text. Replacing cumsum by nancumsum and accepting frame parameters are proposals in the opening body itself. Neither is a discovery from an extra source; exact interpolation, gap amplitude, and phase behavior are not specified.

**Extra evidence.** Status `vacant_start`; 0 Unicode codepoints; 0 images.
No additional source observation is available.

**Smallest concrete input available from the opening/frozen baseline.** Constructed f0=[220, NaN, 220] on the same frame grid. A small conceptual voiced/unvoiced/voiced contour, not a complete executable or empirically minimized reproducer; sr and hop_length values are unspecified. Origin: Frozen baseline example derived from the original request.

**Two-output distinction.** Scoops are reported for the existing workaround; the opening only hypothesizes nancumsum. No supplied source establishes the exact alternative waveform or two contrasting predicted waveform outputs.
No justified old-versus-repaired output pair is supplied; no alternative numerical result is filled in.

**Source-supported observations, distinct from reader predictions:**

- The author explicitly proposes nancumsum and an sr/hop_length grid, and reports the nan_to_num workaround and scoops. Source: `issue_current_body`.
- Both are empty; the public target/start was not mapped in this packet. Source: `common_text / additional_text`.

**Reader prediction status.** No additional implementation-output prediction is made.

**Counterexample or limitation:**

- Replacing a cumulative-sum operation alone does not, on the supplied evidence, specify the interpolation or phase/amplitude behavior at a NaN gap.
- No unseen mir_eval documentation or source implementation was read.

**Eligibility.** additional_text is empty (vacant_start); repeating the opening proposal would be a restatement, not eligible novelty.

**Frozen-baseline assessment.** No substantive disagreement; the already-known proposal remains untested and underspecified.

**Evidence locations:** `packet.json#/requests/1/issue_current_body`, `packet.json#/requests/1/baseline`, `packet.json#/requests/1/common_text`, `packet.json#/requests/1/additional_text`.

## R3-B — insufficient; novelty 0

**Original target.** Permit empty-neighbor rows in global/scalar affinity-bandwidth estimation by using missing-value-friendly scalar aggregation, while retaining empty-neighbor errors for individual/pairwise estimation such as mean_k and gmean_k.

**Old approach.** The opening reports a regression from an earlier scalar nanmedian path to constructing all kth-neighbor distances first and raising at an empty neighbor set before later bandwidth estimation.

**Preserved conditions.** The original recurrence graph and temporal-neighbor conditions are not changed to hide the empty row. Individual/pairwise bandwidth paths retain their no-neighbor errors. A scalar fix must address an empty row rather than substituting an unrelated multi-network task.

**Changed unit, order, or responsibility.** No change is newly supported by extra text. The relevant responsibility change is to select the scalar-versus-local bandwidth branch before treating missing neighbor distances as fatal: ignore missing values for a usable global scalar estimate, retain errors for local/pairwise estimates. The opening body already proposes that distinction.

**New topic outside the target.** The abstract adds a high-level per-data-type-network-then-fuse workflow. That changes the problem unit to multiple sample networks and supplies no rule for missing kth-neighbor distances, scalar aggregation, or preserved pairwise errors.

**Extra evidence.** Status `abstract_only`; 3000 Unicode codepoints; 0 images.

- The preview describes building a sample-similarity network for each available data type and then fusing these into a single network, illustrated with multiple genomic data types. Source: `additional_text, abstract`.
- The 3,000-character excerpt includes article metadata, an abstract, access information, figure titles, related-content text, and a truncated references section. It does not include a method, equations, figure images, or an empty-neighbor example. Source: `additional_text, visible preview boundaries`.
- The Wang paper title/citation and association with average local distances and pair distance were already present in the common API text. Source: `common_text, bandwidth bibliography`.

**Smallest concrete input available from the opening/frozen baseline.** Frozen candidate data=[[0., 0.1, 100.]], k=1, sym=True, width=1, mode="affinity"; first establish that its effective graph contains the 0.1-distance mutual pair and one isolated row. Three samples suffice for the proposed mutual pair plus isolated sample. This public-API graph is conditional and unexecuted; it is not asserted to be the implementation result. Origin: Frozen R3-ISSUE-EMPTY test; no extra-derived input.

**Two-output distinction.** This is a useful original-target distinction, but it was fully frozen before Route B. The article preview does not introduce or strengthen it.

1. **Unconditional empty-neighbor failure before estimator selection:** An exception at the isolated row, including on the scalar branch. Prediction conditional on the candidate graph, consistent with the opening regression report.
2. **The opening-proposed scalar NaN-ignore branch, with pairwise failure preserved:** For kth distances [0.1, 0.1, NaN], scalar bandwidth 0.1 yields exp(-1) on the connected pair and leaves the isolated row unlinked; mean_k/gmean_k still reject the empty-neighbor row. Arithmetic and behavioral prediction from the original proposal plus common affinity formula; not an observed execution.

**Source-supported observations, distinct from reader predictions:**

- The author reports the empty-neighbor traceback and explicitly distinguishes acceptable scalar handling from necessary individual/pairwise errors. Source: `issue_current_body`.
- The API defines exp(-distance/bandwidth), global median and pairwise bandwidth alternatives, mutual-neighbor filtering, and the width/full behavior. Source: `common_text`.
- The abstract supports only the high-level network-fusion topic relevant to its own genomic integration task; no source-visible empty-neighbor treatment is provided. Source: `additional_text`.

**Reader prediction status.** Only the explicitly conditional opening/common predictions above are retained; none was executed or newly supported by Route B.

**Counterexample or limitation:**

- If every row is empty, ignoring NaNs supplies no valid scalar estimate; neither the opening proposal nor this preview specifies that case.
- A fusion algorithm can build or combine networks without permitting an isolated row in the requested scalar recurrence routine, so the abstract workflow does not imply the desired repair.
- Switching to full=True would ignore width according to the already-common API; it cannot be credited as a preserving repair from this excerpt.
- Figure titles are not figure content. No hidden method, normalization, diffusion rule, convergence result, or numerical performance result is inferred.

**Eligibility.** The extra contains a new general topic but no original-target-preserving implementation decision or discriminating test. Relevant scalar-versus-pairwise responsibility and local-scale formulas are already in the opening/common baseline.

**Frozen-baseline assessment.** No substantive disagreement. The frozen question about whether the first 3,000 characters add relevant support is resolved negatively for this supplied preview. That resolution is an assessment outcome, not a novel implementation result.

**Evidence locations:** `packet.json#/requests/2/issue_current_body`, `packet.json#/requests/2/baseline`, `packet.json#/requests/2/common_text`, `packet.json#/requests/2/additional_text`.

## R4-B — unavailable; novelty 0

**Original target.** Make invalid 1D input to rank.otsu report that 2D or 3D arrays are supported, while preserving its existing valid 2D and 3D processing branches.

**Old approach.** The opening reports that otsu(np.eye(10).ravel(), disk(3)) raises an error implying that only 3D arrays are supported.

**Preserved conditions.** Keep the 2D _apply_scalar_per_pixel path. Keep the 3D _apply_scalar_per_pixel_3D path. Continue rejecting invalid dimensions; change the misleading diagnostic.

**Changed unit, order, or responsibility.** No change is newly supported by extra text. The opening already supplies np.asanyarray followed by ndim==2, elif ndim==3, else a clear ValueError. Responsibility for an invalid dimension moves to explicit dispatch rather than an inappropriate 3D-only error; this is the requester's proposal.

**Extra evidence.** Status `vacant_link`; 0 Unicode codepoints; 0 images.
No additional source observation is available.

**Smallest concrete input available from the opening/frozen baseline.** otsu(np.eye(10).ravel(), disk(3)). This is the smallest fully specified failing reproducer supplied, not a claim that its 100 elements are necessary. Origin: Exact opening-body reproducer and frozen R4-C0.

**Two-output distinction.** The opening gives both messages and the code proposal. This is baseline evidence, not extra-source novelty.

1. **Reported current behavior in the opening:** ValueError: The parameter `image` must be a 3-dimensional array Author-reported output, not a fresh current-version observation.
2. **Original proposed explicit 2D/3D/else dispatch:** ValueError: The parameter `image` must be a 2- or 3-dimensional array Requested output and direct prediction of the supplied proposed branch; not executed.

**Source-supported observations, distinct from reader predictions:**

- The reproducer, reported and desired diagnostic, and explicit dimensional dispatch are supplied by the requester. Source: `issue_current_body`.
- The API documents 2D/3D uint8 or uint16 input and output of the same dtype and shape, and gives valid 2D/3D examples. It does not show a fresh invalid-1D execution. Source: `common_text`.

**Reader prediction status.** Only the explicitly conditional opening/common predictions above are retained; none was executed or newly supported by Route B.

**Counterexample or limitation:**

- A threshold-quality or image-gallery example would not by itself distinguish the requested invalid-dimension error.
- The exact invalid-input message of version 0.26 is not established by these sources.

**Eligibility.** additional_text is empty (vacant_link). The complete known repair and comparison already occur in the opening/common baseline.

**Frozen-baseline assessment.** No substantive disagreement; no new gallery result or current runtime diagnostic is claimed.

**Evidence locations:** `packet.json#/requests/3/issue_current_body`, `packet.json#/requests/3/baseline`, `packet.json#/requests/3/common_text`, `packet.json#/requests/3/additional_text`.

## R5-B — unavailable; novelty 0

**Original target.** Prevent out-of-domain reflected values from affecting dilation with a noncompact footprint, through neutral dtype-boundary constants or selectable boundary handling; the analogous erosion constant is the dtype maximum.

**Old approach.** The opening reports a reflect boundary default that can introduce unintended samples for a noncompact footprint, including one that excludes its center.

**Preserved conditions.** Use the intended footprint samples within the image. Use boundary values that are neutral for the morphological operation and respect the dtype range. Preserve the existing compact-footprint behavior where the opening says reflection only duplicates sampled pixels.

**Changed unit, order, or responsibility.** No change is newly supported by extra text. The opening already proposes constant padding with np.iinfo(image.dtype).min for dilation or allowing a user-selected mode. The common API already exposes mode/cval and discusses footprint orientation/decomposition. No extra establishes a new boundary policy or implementation semantic.

**Extra evidence.** Status `vacant_link`; 0 Unicode codepoints; 0 images.
No additional source observation is available.

**Smallest concrete input available from the opening/frozen baseline.** image=np.array([[7]], dtype=np.uint8); footprint=np.array([[1,0,1]], dtype=np.uint8). One image pixel is enough for this conceptual off-domain-only footprint distinction; the symmetric footprint avoids a separate orientation issue. Not executed. Origin: Frozen R5-C0, constructed from the opening boundary concern and common maximum-neighborhood definition.

**Two-output distinction.** The common maximum operation and original constant-minimum proposal support this conditional comparison. It was already frozen and does not count as new.

1. **reflect with the frozen single-pixel input:** [[7]] Frozen mathematical prediction: reflected off-domain samples reuse the sole value 7; no runtime observation.
2. **constant padding with uint8 minimum 0:** [[0]] Frozen mathematical prediction: both selected footprint locations are outside the image and contribute 0; no runtime observation.

**Source-supported observations, distinct from reader predictions:**

- The author proposes constant dtype-minimum padding and explicitly leaves 64-bit integer behavior to be tested. Source: `issue_current_body`.
- The API defines dilation as a neighborhood maximum, exposes mode/cval, and says min/ignore assumes the dtype maximum while also saying the outside values do not influence the result. Those statements are internally in tension for a maximum operation. Source: `common_text`.
- The bright-center example supplies a 3x3 block of ones in a 5x5 result. It does not distinguish the requested boundary policies. Source: `common_text, inline example`.

**Reader prediction status.** Only the explicitly conditional opening/common predictions above are retained; none was executed or newly supported by Route B.

**Counterexample or limitation:**

- A compact footprint containing the center, such as the common interior example, need not expose the unwanted boundary sampling.
- The source-visible min/ignore sentence would imply a non-neutral maximum value on this toy input if read literally. With no extra source or execution, the actual min/ignore implementation cannot be resolved.
- Nothing newly supports 64-bit integer numerical behavior, floating-point neutral constants, or a historical fix/adoption.

**Eligibility.** additional_text is empty (vacant_link). The boundary comparison and documentation contradiction were already frozen.

**Frozen-baseline assessment.** No substantive disagreement; retain the frozen hold on actual min/ignore semantics and 64-bit behavior.

**Evidence locations:** `packet.json#/requests/4/issue_current_body`, `packet.json#/requests/4/baseline`, `packet.json#/requests/4/common_text`, `packet.json#/requests/4/additional_text`.

## R6-B — unavailable; novelty 0

**Original target.** Restore the Lab-to-LCh-to-Lab roundtrip on S390x for the reported float16/float32 cases while keeping the dtype assertion and numerical tolerance.

**Old approach.** The opening gives data.colorwheel -> img_as_float -> astype(dtype) -> rgb2lab -> lch2lab(lab2lch(lab)) and reports a roundtrip assertion failure on S390x with NumPy 1.24.1, whereas 1.23 works.

**Preserved conditions.** Keep lab.dtype == _supported_float_type(dtype). Keep roundtrip decimal=4 for supported float32 and decimal=7 otherwise. Do not establish a fix by dropping the S390x cases, weakening tolerance, or changing the original dtype expectations; little-endian builds are reported to pass.

**Changed unit, order, or responsibility.** No change is newly supported by extra text. No repair is proposed in the opening. Responsibility remains unresolved between a NumPy regression and an exposed scikit-image issue. An extra-source responsibility reassignment would be invented.

**Extra evidence.** Status `vacant_start`; 0 Unicode codepoints; 0 images.
No additional source observation is available.

**Smallest concrete input available from the opening/frozen baseline.** The original colorwheel conversion test, parametrized by np.float16, np.float32, and np.float64, with both original assertions and the reported S390x environment. No smaller failing pixel or complete numeric input is supplied. The colorwheel resource was not opened and the test was not executed. Origin: Opening traceback and version information; the frozen known_issue already names this test.

**Two-output distinction.** The supplied report distinguishes a failing environment from reported successful builds/NumPy 1.23, but no source-supported repair exists from which to predict a corrected output. Passing the original assertions is the acceptance criterion, not evidence for an alternative implementation.
No justified old-versus-repaired output pair is supplied; no alternative numerical result is filled in.

**Source-supported observations, distinct from reader predictions:**

- The author reports float16 and float32 failures on S390x and provides the traceback, dtype assertion, roundtrip assertion, and version information. Source: `issue_current_body`.
- The supplied float16 failure reports 6 / 411810 mismatched elements, maximum absolute difference 5117.8477, and maximum relative difference 118.42903; the author says float32 has the same output. These are transcribed source observations, not reader measurements. Source: `issue_current_body`.
- Both are empty; there is no mapped public target/start or new technical source in this route. Source: `common_text / additional_text`.

**Reader prediction status.** No additional implementation-output prediction is made.

**Counterexample or limitation:**

- The reported architecture/version association does not establish endianness as the causal mechanism or assign the bug to NumPy.
- Promoting all output to a different dtype or relaxing the tolerance would change the stated acceptance conditions and is not supported as a preserving repair.
- The numeric failing values and build log were not opened; no fresh reproducer or numerical result is claimed.

**Eligibility.** additional_text is empty (vacant_start). There is no extra-supported change, discriminating test, or corrected output.

**Frozen-baseline assessment.** No substantive disagreement. baseline_tests=[] does not erase the regression test visibly supplied in the opening and acknowledged in frozen known_issue; it remains original evidence, not Route B novelty.

**Evidence locations:** `packet.json#/requests/5/issue_current_body`, `packet.json#/requests/5/baseline`, `packet.json#/requests/5/common_text`, `packet.json#/requests/5/additional_text`.

## Key disagreements against the frozen baseline

**No substantive disagreement.** The supplied evidence does not overturn the frozen baseline or support a preserving implementation change beyond it.

- R3: the first 3,000 characters have now been read. They do not supply the missing scalar-versus-pairwise empty-neighbor rule. This closes the frozen relevance question for the supplied preview only; it makes no claim about unseen methods or figures.
- R5: the common documentation's min/ignore wording remains internally inconsistent with neutral maximum filtering. The vacancy supplies no basis to settle implementation behavior.
- R6: an empty `baseline_tests` field does not mean that no original test exists. The opening visibly supplies the regression test, and the frozen `known_issue` acknowledges it. Retaining that original test is a bookkeeping clarification, not a new Route B test.
