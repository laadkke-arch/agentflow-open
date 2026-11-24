# AF-RES-113 — Route A automatic-reader judgment

**Eligible novelty: 0 of 6 slots.** R1, R2, R3, and R6 have no assigned extra text. The R4 and R5 prefixes add tutorial content but do not newly support a change or discriminating test for their original requested targets.

## Reader and input record

- Start UTC: `2026-11-24T04:14:38.405277+00:00`
- End UTC: `2026-11-24T04:16:17.424177+00:00`
- Packet SHA256: `dec38a96c5a94832f7daf9a369bdcd7dfb981e07ecfb2777caa57f57fa0e3e00`
- Receipt SHA256: `7cc19e35dcef983a9107fdbdd21a87c053b9ea0c38a77d5672cdaf29248b1c53`
- Packet: all 59,924 UTF-8 bytes / 58,867 Unicode codepoints read; hash and character count match the receipt.
- Receipt: all 1,243 bytes read. All issue, common-text, extra-text hashes and extra lengths match.
- Only `packet.json` and `packet-receipt.json` in this Route A directory were read. All six opening bodies, all frozen baseline fields, every common source-text section, all supplied extras, and all envelope fields were inspected.
- The first full-packet tool display was truncated in its middle. R3 and R4 were then printed in full in separate untruncated results. R1, R2, R5, and R6 were fully visible in the initial result. No unread content is being claimed.
- Parent supplied remote seal commit `11287afdf0c3a0d990f125b72c4f75e9af42f38f`; no git operation was performed to verify it. Packet common seal is `96a754e80f9bbeb5f65e544f7e7f81457b245971`.
- `external_opens=0`, `executed=0`, `cross_route_exposure=false`, `figures_seen=0`, `postseal_verification_exposure=false`.
- Python was used only for permitted input reading, integrity checks, in-memory report checks, and report writing. No target project or example was executed.
- This is an automatic document assessment, **not a human experiment or independent developer adoption**. It establishes neither requester learning nor successful implementation.

## Six-slot summary

| Slot | Extra actually seen | Classification for original target | New decision/test | Eligible count |
| --- | --- | --- | --- | ---: |
| R1-A | Vacant (vacant_link) | Unavailable | None | 0 |
| R2-A | Vacant (vacant_start) | Unavailable | None | 0 |
| R3-A | Vacant (vacant_link) | Unavailable | None | 0 |
| R4-A | 3,000 codepoints; no figures | Irrelevant; insufficient for target change | None | 0 |
| R5-A | 3,000 codepoints; no figures | Irrelevant; insufficient for target change | None | 0 |
| R6-A | Vacant (vacant_start) | Unavailable | None | 0 |

Each judgment below distinguishes material already present in the opening request/common API from the assigned extra. Local source labels identify fields of the sealed `packet.json`; URLs contained in those fields were not opened.

## Exact source-text coverage

| Request | Opening body codepoints | Common codepoints | Extra codepoints | Extra boundary |
| --- | ---: | ---: | ---: | --- |
| R1 | 524 | 5172 | 0 | Empty |
| R2 | 1437 | 0 | 0 | Empty |
| R3 | 2259 | 6857 | 0 | Empty |
| R4 | 1493 | 1384 | 3000 | Ends at `The added n` |
| R5 | 1501 | 3407 | 3000 | Ends at `image_m` |
| R6 | 2703 | 0 | 0 | Empty |

The machine-readable judgment records exact input hashes, byte ranges, per-section UTF-8 lengths and codepoint ranges. Common and extra text were read directly, not inferred from baseline summaries.

## R1-A — unavailable; eligible count 0

**Original target.** Make streaming the same filename.mkv work without the reported unknown-format error, while retaining the loop that passes each speech chunk to tokenizer(speech, return_tensors="pt").

**Old approach.** The opening post loads the first ten seconds with librosa.load(..., duration=10, sr=16000), then attempts librosa.stream on the same MKV with block_length=10 and frame_length=hop_length=16000; the latter reports an unknown-format error.

**New unit, order, or responsibility supported by the extra.** None. No new implementation decision and no new discriminating test.

**Preserved condition.** Same MKV source and chunk-by-chunk tokenizer consumption. Decoder acceptance must be established; chunk geometry or frame alignment cannot by itself establish support for the container/codec.

**What the sources actually show.**

- REQ-R1 opening body reports successful load and failed stream; those are historical reports contained in the packet.
- R1 common_text permits codecs supported by soundfile, describes sr conversion constraints, left-aligned frame analysis, and explicit generator close. Its STFT and mel examples are already common exposure.
- R1 additional_text is empty.

**Smallest concrete input.** No route-extra-derived input. Existing evidence: The original filename.mkv and exact stream arguments above. The actual file bytes are absent, so this is an identified source input, not a self-contained fixture.

**Distinct outputs.** There is no extra text or source-supported decoder replacement. The packet does not justify a second outcome for the same MKV.

- Existing/old outcome: Unknown-format error is reported by the issue author, not predicted or reproduced by this reader.
- Candidate alternative: Unavailable; no second outcome is filled in.

**Reader prediction.** No new outcome prediction. Any supported-reference-file comparison or explicit sr=16000 choice is already frozen common evidence, and neither establishes successful streaming of the original MKV.

**Counterexample or limitation.** Changing center=False or the sample rate leaves the codec-acceptance question unresolved. Native rate, codec, actual MKV bytes, and tokenizer tail requirements are unavailable.

**Novelty decision.** An empty assigned slot cannot supply a new preserving implementation decision or discriminating test.

**Frozen-baseline comparison.** Agree. Decoder capability is separate from downstream geometry; common STFT examples and sample-rate reasoning are not extra-route discoveries.

**Sources.** `packet.json:requests[R1].issue_current_body`; `packet.json:requests[R1].baseline`; `packet.json:requests[R1].common_text`; `packet.json:requests[R1].additional_status`.

## R2-A — unavailable; eligible count 0

**Original target.** Provide pitch-contour sonification in librosa, handle NaN unvoiced regions without onset/offset scoops, and allow a frame grid specified by sr and hop_length.

**Old approach.** The author uses mir_eval pitch_contour for documentation and nan_to_num(f0) for unvoiced regions; the author reports resulting scoops and already suggests nancumsum plus an sr/hop_length grid.

**New unit, order, or responsibility supported by the extra.** None. No new implementation decision and no new discriminating test.

**Preserved condition.** Retain contour sonification while avoiding the reported transition artifacts; frame-grid support is part of the original target, not a newly inferred requirement.

**What the sources actually show.**

- REQ-R2 explicitly proposes replacing cumsum with nancumsum and accepting sr/hop_length.
- R2 common_text and additional_text are empty; the author URL appears only as text and was not opened.

**Smallest concrete input.** No route-extra-derived input. Existing evidence: Frozen baseline proposes f0=[220, NaN, 220] on a fixed frame grid. It is a constructed baseline transition fixture, not an observed waveform or a Route A discovery.

**Distinct outputs.** Neither common API text nor extra text is available. The proposed nancumsum implementation and its exact interpolation/phase behavior are not shown.

- Existing/old outcome: The issue reports scoops with its existing nan_to_num workaround; it supplies no exact output for the constructed three-frame fixture.
- Candidate alternative: Unavailable; no second outcome is filled in.

**Reader prediction.** No new waveform prediction. A statement that nancumsum necessarily eliminates the scoops would exceed the shown evidence.

**Counterexample or limitation.** The packet does not specify how frequency interpolation crosses an unvoiced gap, whether phase should persist or reset, or how a candidate synthesis implementation behaves at voiced boundaries.

**Novelty decision.** The only candidate change is already in the original request; a vacant route cannot make that proposal new.

**Frozen-baseline comparison.** Agree. nancumsum and the frame grid are original proposals, with exact waveform behavior unresolved.

**Sources.** `packet.json:requests[R2].issue_current_body`; `packet.json:requests[R2].baseline`; `packet.json:requests[R2].common_text`; `packet.json:requests[R2].additional_status`.

## R3-A — unavailable; eligible count 0

**Original target.** Allow empty-neighbor rows when estimating a global/scalar affinity bandwidth by using NaN-friendly estimation, while preserving errors for individual/pairwise bandwidth estimates that require those local distances.

**Old approach.** The issue describes constructing all kth-neighbor distances before estimating bandwidth, with an exception at any row without neighbors. The requested scalar-versus-pairwise split is already in the opening body.

**New unit, order, or responsibility supported by the extra.** None. No new implementation decision and no new discriminating test.

**Preserved condition.** Missing neighbors still cause an error for individual/pairwise modes such as mean_k and gmean_k; the requested scalar repair must not silently replace the graph with a full graph or change temporal exclusions.

**What the sources actually show.**

- REQ-R3 reports the no-neighbors exception from the segmentation gallery and already proposes NaN filling plus a NaN-friendly scalar estimator.
- R3 common_text defines med_k_scalar, arithmetic/geometric pairwise scales, sym, width, full, and exp(-distance/bandwidth).
- R3 additional_text is empty. The common bibliography is already common exposure; no linked paper was opened.

**Smallest concrete input.** No route-extra-derived input. Existing evidence: Frozen baseline proposes data=[[0., 0.1, 100.]], k=1, sym=True, width=1, mode="affinity", yielding a candidate mutual-neighbor graph with a distance-0.1 pair and one isolated point. Graph realization must be checked before using it as a public-API fixture.

**Distinct outputs.** No extra text is available. The following distinction is already the original request and frozen baseline.

- Existing/old outcome: Conditional on the candidate graph and the reported unconditional check, scalar and pairwise paths both raise for the isolated point.
- Candidate alternative: Conditional on the proposed scalar-only NaN policy, the scalar bandwidth is 0.1 and the connected-pair affinity is exp(-1); pairwise paths continue to raise.
- Evidence status: Unexecuted mathematical reasoning from the original proposal and common affinity definition, not observed public-API output or Route A novelty.

**Reader prediction.** No new prediction beyond the explicitly conditional frozen-baseline fixture. The packet does not establish the current implementation or original Csync values.

**Counterexample or limitation.** If every row is empty, ignoring NaNs leaves no finite distances from which to estimate a scalar bandwidth. The proposed repair therefore needs an undefined-estimate policy beyond the shown case. full=True also ignores width in the supplied API text and is not a preserving workaround by default.

**Novelty decision.** Scalar/pairwise responsibility, the proposed test, and local-scale formulas were all known before this vacant extra slot.

**Frozen-baseline comparison.** Agree, including its warning that the toy public-API graph and derived affinity are unexecuted and conditional. The all-empty case remains a limitation, not an extra-text finding.

**Sources.** `packet.json:requests[R3].issue_current_body`; `packet.json:requests[R3].baseline`; `packet.json:requests[R3].common_text`; `packet.json:requests[R3].additional_status`.

## R4-A — irrelevant; eligible count 0

**Original target.** Replace the misleading rank.otsu error for an invalid one-dimensional image with an error stating that two- or three-dimensional arrays are accepted, while preserving the valid 2D and 3D dispatch paths.

**Old approach.** The issue reports a one-dimensional input being routed to a path whose error says the image must be 3D. It already supplies np.asanyarray followed by explicit ndim==2 / ndim==3 / else branches.

**New unit, order, or responsibility supported by the extra.** None. No new implementation decision and no new discriminating test.

**Preserved condition.** Both existing 2D and 3D processing branches remain valid, with documented image shape and dtype behavior. Invalid dimensions receive the requested 2-or-3D diagnostic.

**What the sources actually show.**

- The complete assigned 3,000-codepoint extra introduces local gray-level histograms and rank filters, then shows a 2D camera histogram and median noise-removal examples with disk radii 1, 5, and 20.
- The noise-generation code uses random values above 0.99 and below 0.01 to assign 255 and 0. These are shown thresholds and assignments, not measured exact pixel counts or filtering-quality results.
- The excerpt ends at the partial text "The added n". No figure, later section, runtime result, otsu validation code, or dimensional error was supplied.
- The common API already documents both 2D and 3D images and supplies valid examples of both.

**Smallest concrete input.** No route-extra-derived input. Existing evidence: Original reproducer: otsu(np.eye(10).ravel(), disk(3)). Common examples already cover a 2D camera image and a uint8 3D volume with disk/ball footprints. The extra adds no smaller or more discriminating dimensional-validation fixture.

**Distinct outputs.** The excerpt never shows an otsu invalid-dimension call, error message, dimensional dispatcher, or implementation helper.

- Existing/old outcome: ValueError: The parameter `image` must be a 3-dimensional array, as reported in the opening body.
- Candidate alternative: ValueError: The parameter `image` must be a 2- or 3-dimensional array, as requested and proposed in that same body.
- Evidence status: The second outcome is the original desired result and a prediction for the proposed branch change, not an executed observation or an extra-derived distinction.

**Reader prediction.** The median-denoising examples could motivate a separate image-processing exercise, but they do not distinguish correct versus misleading otsu dimensional diagnostics. No new target-relevant output is predicted.

**Counterexample or limitation.** A successful 2D camera/median call would be compatible with both the old and proposed otsu dispatchers. The gallery description of a 2D structuring element cannot override the common otsu contract that permits 3D images. Sharing a histogram concept does not show that the functions share an input-validation helper.

**Tentative idea, not counted.** Consider consistent dimensional diagnostics across rank functions. The opening body already states that the pattern repeats across the module; the excerpt supplies no further dimensional-validation evidence or helper architecture. No relevant new change is supported; it remains unexecuted.

**Novelty decision.** There is additional algorithm/tutorial content, but no supported new unit, order, responsibility, or discriminating test for the original dimensional-error change. Any supplied camera/rank context is non-discriminating or overlaps common exposure.

**Frozen-baseline comparison.** Agree with keeping the original explicit dimensional branches and common 2D/3D tests. The previously unread gallery prefix adds no relevant evidence that changes those choices.

**Sources.** `packet.json:requests[R4].issue_current_body`; `packet.json:requests[R4].baseline`; `packet.json:requests[R4].common_text`; `packet.json:requests[R4].additional_text[0:3000]`.

## R5-A — irrelevant; eligible count 0

**Original target.** Prevent unintended boundary samples from affecting dilation with a noncompact footprint, using neutral constant extension or an exposed user boundary mode, with the corresponding maximum-neutral policy for erosion and attention to dtype limits.

**Old approach.** The original issue describes grey_dilation using reflect extension, which can map out-of-domain footprint positions onto unintended in-domain pixels; it already proposes constant extension with the dtype minimum or user-selectable boundary modes.

**New unit, order, or responsibility supported by the extra.** None. No new implementation decision and no new discriminating test.

**Preserved condition.** Only intended in-domain footprint samples should affect the result; use a neutral value compatible with the dtype, retain applicable compact-footprint behavior, and keep footprint orientation distinct from boundary extension.

**What the sources actually show.**

- The assigned 3,000-codepoint prefix motivates removing fixed dark spots from a corneal image sequence, loads palisades_of_vogt, and contains the printed dataset description shape (60, 1440, 1440), dtype uint16.
- It shows visualization code and then image_med=np.median(image_seq, axis=0), image_var=np.var(image_seq, axis=0), followed by a shape-equality assertion.
- The text says the dirt is stationary while the signal moves, motivating temporal aggregation for later segmentation. This concerns the unit and order of a separate segmentation workflow.
- The excerpt stops mid-print at "image_m". It supplies neither later segmentation/inpainting methods nor any figures or boundary-mode observations.

**Smallest concrete input.** No route-extra-derived input. Existing evidence: Frozen baseline R5-C0: image=[[7]] as uint8, footprint=[[1,0,1]] as uint8. Its center is excluded and both selected neighbors lie outside the one-pixel image.

**Distinct outputs.** The supplied inpainting prefix does not show dilation, erosion, a footprint, boundary mode, cval, or a boundary comparison.

- Existing/old outcome: Reflect extension repeats the pixel and predicts [[7]].
- Candidate alternative: Constant extension with uint8 minimum 0 predicts [[0]].
- Evidence status: Already-frozen mathematical predictions from the original request and common maximum-neighborhood definition. No filter was executed.

**Reader prediction.** Temporal aggregation might help distinguish fixed spots from moving tissue in that tutorial, but it supplies no prediction for noncompact-footprint boundary extension. The already-frozen [[7]] versus [[0]] comparison remains the relevant candidate test.

**Counterexample or limitation.** The same temporal median/variance prefix could precede either reflect-based or neutral-constant morphology, so it cannot select between the two. A uint16 dataset description does not establish 64-bit behavior. The common dilation text says maximum for min/ignore despite a maximum-over-neighborhood definition; this pre-existing contradiction is not resolved by the extra.

**Tentative idea, not counted.** Aggregate a stationary-defect movie over time before segmentation. The excerpt supports this tutorial step, but the original requested change is morphological image-boundary handling, not temporal defect segmentation. It would change the problem being solved. No relevant new change is supported; it remains unexecuted.

**Novelty decision.** A new workflow step in a different application is not a preserving change to the original boundary-extension target. No new target-specific implementation decision or discriminating test is present.

**Frozen-baseline comparison.** Agree with explicit neutral constant extension as the original candidate and with retaining the unresolved min/ignore wording contradiction. The gallery prefix adds no resolution.

**Sources.** `packet.json:requests[R5].issue_current_body`; `packet.json:requests[R5].baseline`; `packet.json:requests[R5].common_text`; `packet.json:requests[R5].additional_text[0:3000]`.

## R6-A — unavailable; eligible count 0

**Original target.** Restore Lab-to-LCh-to-Lab round-trip accuracy for float16/float32 on the reported S390x big-endian setup while retaining supported output dtype and the original numerical assertions.

**Old approach.** The opening body provides the colorwheel -> img_as_float -> astype(dtype) -> rgb2lab -> lch2lab(lab2lch(lab)) test, asserts _supported_float_type(dtype), and reports round-trip failures for float16 and float32 on S390x.

**New unit, order, or responsibility supported by the extra.** None. No new implementation decision and no new discriminating test.

**Preserved condition.** Keep the dtype assertion, decimal=4 for float32 supported output and decimal=7 otherwise, and account for the reported platform/version conditions without relaxing the original success criterion.

**What the sources actually show.**

- REQ-R6 supplies the test and a failing float16 traceback, states the same failure for float32, and names the historical package versions.
- The traceback is a source-reported failure, not this reader's runtime observation.
- R6 common_text and additional_text are empty. The external build-log link was not opened.

**Smallest concrete input.** No route-extra-derived input. Existing evidence: The original colorwheel-based parametrized regression test on the stated S390x big-endian environment. No failing pixel values or minimized array are present in the supplied opening body.

**Distinct outputs.** No API or additional text, candidate fix, or root-cause evidence is supplied. A passing repaired output cannot be predicted from this route.

- Existing/old outcome: The issue reports float16/float32 failures on S390x with numpy 1.24.1 and successful other little-endian builds; numpy 1.23 is reported to work.
- Candidate alternative: Unavailable; no second outcome is filled in.

**Reader prediction.** No new prediction and no attribution of the cause to numpy or skimage. The original test remains an existing regression input, not extra-route novelty.

**Counterexample or limitation.** The displayed arrays elide the failing values, so a smallest numerical reproducer cannot be recovered. The source itself leaves numpy regression versus skimage defect unresolved; passing a different platform would not establish repair of the original S390x case.

**Novelty decision.** A vacant start/extra provides no supported repair or newly discriminating test. Existing regression assertions cannot be counted again.

**Frozen-baseline comparison.** Agree. The target symbol and cause remain unresolved in this assigned packet, and no repair is inferred.

**Sources.** `packet.json:requests[R6].issue_current_body`; `packet.json:requests[R6].baseline`; `packet.json:requests[R6].common_text`; `packet.json:requests[R6].additional_status`.

## Key disagreements against the frozen baseline

**No material disagreements.** The original issue bodies and common source texts support the frozen distinctions. R4’s gallery prefix does not change the dimensional-validation decision or add a new invalid-input test. R5’s prefix does not decide boundary extension or resolve the common min/ignore wording contradiction. R3’s constructed graph and affinity outcomes remain conditional predictions, and no historical report has been promoted to a reader-observed runtime result. All six Route A novelty counts remain zero.
