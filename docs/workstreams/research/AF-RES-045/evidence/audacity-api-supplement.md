# Audacity pre-outcome API supplement

Access phase: before parent supplied prediction seal. No issue comments, PRs, timeline or post-request release notes opened.

## Fixed editions

- Audacity 2.3.3: `008d8d8c8cb6f6fac9c95f72513f6b0bc98af1dc`, commit date 2019-11-15T11:14:55Z; before AUD01 and AUD02.
- Audacity 2.4.2: `16d52f63a4183bba77ef7305d14622958dc0d1d5`, commit date 2020-06-19T15:16:47Z; before AUD03, after AUD01/AUD02. Used only as AUD03 baseline.

## Consequences for the draft choices

**AUD01.** 2.3.3 GetInfo enum (L53–77,145–159) does not expose a Selection type, and track start/end are not selected-range bounds (L487–514). However the same edition Nyquist.cpp L764–767 already populates *SELECTION* START and END from mT0/mT1. Revise the provisional B description to **reuse pre-existing Nyquist properties**, rather than imply an already available generic GetInfo Selection record. A dedicated GetTime and B property access can return the same two values; numeric-output predictions therefore do not distinguish them. UI-read timing/serialization is unexecuted.

**AUD02.** SetClipCommand.cpp L31–55,72–97 already permits setting a particular clip's four-valued color index. The author's desired arbitrary own color and clip background still exceed that interface. A/B both need new representation if described as arbitrary RGB. Contrast normalization B conflicts with strong literal preservation of the chosen color. A beautiful external principle alone does not remove this API or requirement conflict.

**AUD03.** NoiseReduction.cpp already passes frequency bounds (L650–656), converts low/high to floor/ceil FFT-bin indices (L783–789), initializes outside-range gains (L1170–1187), and later applies geometric frequency smoothing across bins (L716–744,1237–1240). Experimental.h L136 defines the spectral flag. These are pre-request static facts, not a report that the request was already solved for the author's binary or arbitrary effect. The initial draft's 2001Hz test is not safely outside the included FFT bins. At 44100Hz and window2048, bin spacing is about21.5332Hz; high bound2000Hz rounds to exclusive index93, while2001Hz is within index92. A careful test should use an explicitly specified bin outside the exclusive bound, e.g. bin93, while retaining the same settings and comparing smoothing0 with a specified positive width. That revised fixture is still researcher supplied, not an observed acceptance test.

## Pre-seal amendments (original draft preserved)

1. AUD01 B original: generic selection record accessor. After pre-request code reading: existing Nyquist *SELECTION* START/END accessor. Expected bounds remain identical; no outcome-dependent selection.
2. AUD03 boundary original: 2001Hz just outside [1000,2000]Hz with20Hz feather. Corrected recommendation: explicit FFT-bin index93 at44100Hz/window2048, because current hardmask boundary itself uses outward floor/ceil. Original initial.json remains preserved so its limitation can be audited.

## Cross-case exposure event

While inspecting 2.4.2 Nyquist.cpp for AUD03, L801–804 also exposed *SELECTION* START/END, a source edition later than AUD01. This event occurred before seal and is not hidden. Direct subsequent reading of 2.3.3 Nyquist.cpp L764–767 confirmed the same properties were already present before AUD01. It supplies no observed later decision, but a maximally conservative sensitivity can exclude AUD01 as any post-request-code exposure. The main explicit outcome leak remains AUD02's retrospective checked subtask.

## Limits

The source files are one release work per edition, not individually counted toward the24 required minimum originals. No historic program has been built, no audio or color output executed, no author adoption inferred. The selected requirements remain407/511/644; inconvenient domain mismatch is preserved.
