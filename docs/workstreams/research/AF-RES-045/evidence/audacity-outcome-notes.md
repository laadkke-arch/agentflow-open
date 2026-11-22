# Audacity post-seal outcome notes

## Seal and actual reveal order

- Parent-authorized remote prediction seal: `0d998cb3503e8a7f0faf2bf2f8e62dd046a662b1`, committed **2026-11-22T22:19:23Z**, fetched identical at22:19:27Z.
- First outcomes/labels/comments/timelines opened **22:20:00.421Z**.
- No sealed request, prediction, frame or pre-seal API file was edited by this outcome investigation.
- Full case records: `audacity-outcomes.json`. All post-seal reads/revisits/searches: `audacity-outcome-sources.jsonl`.

## What changed after reveal

### AUD01: the delivered command is a third choice

[PR6165](https://github.com/audacity/audacity/pull/6165) adds **GetInfo:Type=Selection**, merged `0ffa73b9f44acc339e12a350edadd96590dc4b17`. [Fixed source L634–645](https://github.com/audacity/audacity/blob/0ffa73b9f44acc339e12a350edadd96590dc4b17/src/commands/GetInfoCommand.cpp#L634-L645) sends the selected region's two time values. It is neither sealed A's dedicated GetTime nor sealed B's existing Nyquist-property read. The earlier unsealed generic-accessor draft must not be used as if it were the frozen B.

[The contributor's public test report](https://github.com/audacity/audacity/issues/407#issuecomment-2076865041) has a directly viewed attachment showing **Start2.62385, End5.29415**. It does not show the input-selection UI, buildSHA or pipe call. It is not the original requester, not the sealed1.25/2.50 input, and not a zero-length boundary trial. Screenshot SHA256 is `38b57bc4236cab0d629683b046661bd2e02f2cfcbf2b6325057800c5264a0bdf`; image bytes were not committed. A timestamped second direct read confirmed the same image at22:27:44–22:27:54Z.

[PR6347](https://github.com/audacity/audacity/pull/6347) later adds Selection to the Nyquist wrapper; its generic test-completed comment lacks inputs/outputs. [3.6.0 release notes](https://github.com/audacity/audacity/releases/tag/Audacity-3.6.0), Other changes, explicitly announce the command. Neither supplies the frozen input pair. The two donor candidates already made identical numeric predictions, so this cannot be a discriminatory success even with broader endpoint support.

A useful contrary observation is the [postmerge selection-scope dispute](https://github.com/audacity/audacity/pull/6165#issuecomment-2077257269): a complete audio selection may include tracks as well as time. The [maintainer's external-sync use case](https://github.com/audacity/audacity/pull/6165#issuecomment-2077354485) accepts a narrower result. Purpose changes the adequacy of the same output.

### AUD02: checkbox and closed state are not implementation evidence

[Issue511's closing comment](https://github.com/audacity/audacity/issues/511#issuecomment-2445034377) asserts that Audacity4 fixes it, without a specific patch or RGB test. The already-exposed checked subtask2713 has an opposite implication to an apparent completion badge: [its closing comment](https://github.com/audacity/audacity/issues/2713#issuecomment-1150354103) defers the work until post4.x and closes it meanwhile. Its actual debate is color names versus previews, not the frozen same-foreground/background input.

The revealed rename event also shows that511's original title lacked the selection token. The frozen frame is therefore a **current-title query over historically created issues**, not an authenticated reconstruction of titles as they existed in2020. Keep the slot; disclose this sampling limit.

Independent [PR5653](https://github.com/audacity/audacity/pull/5653) supplies an actual different constraint: clip colors must persist through drag/copy/split/save and version interchange. The contributor's [regression report](https://github.com/audacity/audacity/pull/5653#issuecomment-1829887542) and [recording-versus-generation difference](https://github.com/audacity/audacity/pull/5653#issuecomment-1829945652) show why a color is sometimes user state rather than only a contrast variable. This is a comparison case, not same-input support for511.

### AUD03: explicit correction of our missed local preprocessor override

**Error retained:** before sealing, the researcher inspected the global define and conditional frequency-bound code, but missed this file's own local undef. This is our reading weakness; it must not be hidden as merely unavailable public evidence.

The [2024 cleanup diff](https://github.com/audacity/audacity/commit/e7d17d1bcedcb1fe75d78eb522de3b46476c94b7) was first opened22:22:25.972Z. It prompted reinspection of the cached pre-request source at22:22:34.620Z and fresh direct reopening of both fixed sources at22:23:44.433Z:

| Fixed edition | Exact location | Actual contract |
|---|---|---|
| [2.4.2 at16d52f63](https://github.com/audacity/audacity/blob/16d52f63a4183bba77ef7305d14622958dc0d1d5/src/effects/NoiseReduction.cpp#L75-L77) | L75–77 | Local `#undef EXPERIMENTAL_SPECTRAL_EDITING`; comment says spectral selection should not affect this effect because there might be no indication. |
| [e7d17d1b after cleanup](https://github.com/audacity/audacity/blob/e7d17d1bcedcb1fe75d78eb522de3b46476c94b7/src/effects/NoiseReduction.cpp#L75-L77) | L75–77 | Local `#undef SPECTRAL_EDIT_NOISE_REDUCTION`; exception remains disabled while the global experimental flag is retired. |

[PR6201](https://github.com/audacity/audacity/pull/6201) is a relevant subsequent code work, but a compile-flag cleanup is not adoption or execution of either frozen toy operator. The disabled branch still contains useful algorithmic information; it does not prove an active user feature.

[Issue644](https://github.com/audacity/audacity/issues/644) is open. The two comments are a volunteer inquiry and a discussion invitation. No same Fs48000/N2048/bin64/bin86 public test was found in the observed thread or bounded follow-up paths. Both model predictions therefore remain **미확인** for actual receiver behavior. Their arithmetic0dB/-2.4dB divergence is preserved; no replacement prediction was written after observing the override.

## Counts and interpretation boundaries

There are3 Audacity requests and6 frozen predictions:1 same-output pair,1 underdetermined pair,1 different-model pair. **Same-operation/input/purpose public followup:0; different-prediction cases with such followup:0; unique support:0; both rejected:0; conditional rate:해당 없음.** Exact output reporting is weaker than matched-input validation.

The outcome ledger contains42 reads/searches. Its primary-work allocation proposes5 receiver followups (PR6165,PR6347,issue2713,3.6.0release,PR6201) plus1 independent comparison(PR5653). Comments/diff/fixed-source repeats do not add works. If the3.6.0release is conservatively merged with its6165change, receiver followup count becomes4; all substantive judgments stay unchanged.

Explicit original-body outcome exposure excludesAUD02. A stricter sensitivity excluding any later-than-request source encounter also excludesAUD01 because the2.4.2 Nyquist property was first seen while working onAUD03, even though2.3.3 subsequently proved it existed beforeAUD01. No sensitivity creates a successful matched-input case.

## Smallest evidence that could change the judgment

- AUD01: exact frozen inputs on A/B plus pipe end-to-end response and fixedbuild. Both donor predictions may remain equal, so more support alone does not create discrimination.
- AUD02: the Audacity4 patch behind the closure assertion and a fixed arbitraryRGB/background test including the same-color boundary, user override and preservation semantics.
- AUD03: an explicitly enabled frequency-selection NR path with a fixed signal/noiseprofile/window/overlap/settings and actual bin64/bin86 output. The five-bin toy kernel must be compared with the real algorithm before carrying its numerical result over.

This was a delegated same-model source investigation and self-correction, not external independent human validation.
