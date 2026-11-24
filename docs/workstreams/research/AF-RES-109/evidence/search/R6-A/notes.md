# R6 / Arm A — controlled search notes

## Input and baseline

The supplied current opening post reports pinch producing viewport scrolling on Windows 11 in Chrome 120 and Edge when `panOnScroll=true`; Mac works. Setting `zoomOnPinch=true` had already been tried and is described as the default. These settings and the existing React Flow example are the baseline, not newly invented proposals. The supplied post gives no dependency version, event trace, listener registration, source code, hardware model, or distinction between a touchscreen and trackpad. The search emphasized trackpad wheel input as a hypothesis, not an established device classification.

The assigned input hash is `12887f1a139112b86eb8d21f2ecaab2e6ca4c7d61e71328fb06fb5bb037b0244`. It was supplied by the assignment rather than independently recomputed. The opening-post date was supplied as 2024-01-02T06:25:26Z; its original edition was not established. The source issue itself and supplied example links were not opened.

## Actual strategy

Method A used three English system2 queries. The first sought Windows pinch and wheel-event semantics, yielding primary Chromium code. The second targeted D3 event filters and wheel scaling. The third investigated a separate cancellation failure through Chrome's passive-listener guidance. One explicit page was opened after each query: three opens total, with no clicks, finds, reopens, failed opens, other retrieval, or shell networking.

All 41 search results are logged in their original displayed order: 17, 12, and 12. Each query returned at least five results, so no top-five ranks are missing. Search responses sometimes included extensive page text; it remained search exposure until a separate explicit open. Full third-party pages are not written into these deliverables. Raw responses were held in functions store only.

The three returned candidates identify event classification, selective admission to zoom, and cancellation as different diagnostic points. Suggested choices are inferences applied to the supplied request, not established fixes. Unmentioned approaches are only absent from the supplied post; the author's knowledge is unknown.

## Candidate evidence and proposed tests

- **S1 / T1:** Chromium code supplies the Control-modified wheel discriminator. Compare events differing only in that modifier, then check whether a native Windows pinch actually matches. The proposed oracle separates zoom scaling from ordinary panning without forbidding translation needed to preserve a zoom anchor.
- **S2 / T2:** D3 documents preserving a filtered wheel route. A tiny harness distinguishes removing all wheel handling from accepting a Control-modified event. Its predicted scale is arithmetic from the documented default, not a measured React Flow result.
- **S3 / T3:** Chrome documents a root-listener cancellation failure. Compare default listener options against explicit non-passive handling and observe `defaultPrevented`. This is conditional on the listener actually being affected.

Every test is **proposed, not executed**. No browser, physical device, simulation, reproduction application, or test harness was run.

## Unintended exposure

The first query automatically exposed an unrelated recent Flutter commit containing a proposed/resolved behavior change and reported tests, and an unrelated WebKit issue's status and later changes. Neither was opened or used as verified evidence. The original xyflow issue's comments, status, linked PRs, releases, and later resolution were not exposed in returned results and were not inspected.

The third query exposed a Lighthouse 13 audit-removal notice and current two-dimensional-panning documentation. English and Spanish panning excerpts differed in their modifier guard; this was not investigated. Four translated copies of the Chrome wheel article appeared in the search results and are recorded as exposures, not additional independent works.

## Unfilled requirements and limits

The cause of the reported bug remains unknown. No actual Windows event stream, device/driver behavior, React Flow routing, dependency edition, listener target, passive option, scale bounds, or browser default action was verified. Native event provenance and synthetic event behavior may differ. Touchscreen and trackpad paths were not compared. Physical Control-plus-wheel can resemble pinch and its desired product behavior is unspecified. Browser zoom versus viewport zoom must be observed separately.

The pinned Chromium revision date is unknown; its copyright year does not prove historical availability. D3 is live documentation with a displayed D3 version label, not an established January 2024 edition. Chrome's article displays a February 2019 update date, but no archived edition was read. Availability of any proposal to the reporter at the time is not inferred beyond these observations.

Question labels Q3–Q6 were required by the prompt, but their definitions were not provided. The sources retain those labels without inventing definitions.

## Measurement and isolation

Web-call UTC timestamps were captured immediately before and after each search-tool action using the execution runtime's clock. Elapsed values measure observed tool-call wall time. The start event begins controlled research after reading the assigned prompt; prompt-read duration is not included. The stop event closes evidence preparation before final persistence.

Only the assigned prompt was read locally; no other repository, request, arm, HANDOFF, or sibling output was read. All persistent writes are confined to this arm's assigned directory. No delegation, git commands, commits, central-ledger writes, or extra research occurred.

The inherited parent display label is GPT-6 Astra Pro. An immutable backend model/version was not exposed. Automatic engine reads, token usage, and monetary cost are unknown, represented by null values rather than zero.
