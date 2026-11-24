# R6 / Method B search notes

## Input and baseline

The supplied opening post is dated 2024-01-02T06:25:26Z; its original edition is not established. It reports pinch scrolling instead of zooming on Windows with React Flow's `panOnScroll=true`, using the existing Figma-like configuration. Windows 11 and Chrome/Edge are mentioned, with Chrome 120 reported. Mac behavior is reported working. `zoomOnPinch=true` is already the default and has already been tried, so repeating that setting is baseline.

The input does not identify the physical pinch device or provide an event trace. Touchpad-generated wheel input is one hypothesis explored here, not an added requirement or an established diagnosis. The author's statement about affected users is a report, not a verified population result.

## Decomposition before searching

Target part: gesture classification and viewport transformation.

Preserved conditions: Windows, the reported browsers, scroll-panning enabled, and pinch-zoom enabled.

Operative relationship: physical pinch → browser input representation → handler classification → viewport scale or translation. Useful evidence can distinguish failure at the browser-event boundary from failure in routing or default-action handling.

## Actual search strategy

1. `React Flow Windows pinch panOnScroll ctrlKey wheel zoomOnPinch source`
2. `browser pinch gesture wheel event modifier key distinguish scrolling zooming Windows`

Both were English `system2_search_query` queries. The second is relational and names neither the target product nor a donor field. Query 1 exposed 18 results and query 2 exposed 25; all are logged in displayed order, including the exact top five and all additional exposures.

There were six explicit-open actions: a React Flow API open, a failed Chromium historical-diff open, a Chromium PDF source open, an API reopen, a Chromium pinch-queue source open, and a click to the pinch-queue tree revision's metadata. One query slot remained unused. Search stopped because three directly read candidate links were available, not to fill the remaining quota.

## Candidate decisions and proposed tests

- **R6-B-T1 — event classification:** use the Chromium pinch-queue source to motivate a marked/unmarked wheel comparison while preserving the target configuration. Capture real input separately. The historical tree is dated 2018-10-12, before the supplied request. It does not prove behavior in Chrome 120 or on the reporter's hardware.
- **R6-B-T2 — gesture normalization:** the Chromium PDF viewer provides an explicit wheel-to-pinch lifecycle adapter. Its timer, scale clamp, and cancellation behavior support a small sequence test. They are implementation examples, not newly invented user requirements.
- **R6-B-T3 — keyboard activation ablation:** compare React Flow's documented activation shortcut default with `null` while leaving the supplied pan and pinch properties fixed. This is a conditional diagnostic, not a promised fix.

Every test is **proposed, not executed**. All three actual links and detailed discriminators are in returns.json. No candidate is asserted to be unknown to the original author. The two Chromium links are different components within one project, not evidence of a cross-domain discovery.

## Unintended exposure

Query 1 displayed the original issue at rank 6, including later-comment material about Windows/Wacom Control-wheel behavior and slow zoom. The issue was not explicitly opened, but the search arm is not uncontaminated: that later material was visible. It is logged and was not used as supporting evidence.

The same query exposed a later separate Windows pinch issue and a 2026 release snippet. They were not opened or used. Query 2 exposed a later MDN issue and historical Chromium review metadata. The final tree-metadata click displayed an unrelated service-worker revert subject; it was used only to date the already-read tree.

No original issue page, later same-issue PR, source-issue comments, status, release, or resolution was deliberately inspected. No sibling output or other research file was read. The assigned prompt was reread only to verify its supplied input hash.

## Unfilled requirements and what was not tested

The original source edition, React Flow dependency version, physical device, driver settings, and actual emitted input events remain unknown. Current API documentation is not a verified January 2024 edition. The exact PDF code revision date remains unknown; its copyright year is not a publication date. The dated Chromium snapshot establishes historical existence, not browser release availability.

No Windows/browser reproduction, virtual-machine test, actual event capture, patched application, adapter execution, sensitivity benchmark, or regression test was performed. No root cause or working fix is claimed. Device differences and overlapping physical-Control versus synthesized-Control wheel semantics remain discriminating uncertainties.

The supplied digest matches the natural-input body with its trailing newline removed. The initial prompt read occurred before instrumentation, so exact timestamps for that bootstrap action were not captured. Every subsequent web acquisition has actual UTC start/end timing. Automatic engine reads, token usage, money cost, and exact immutable model backend are unknown. The only model label exposed by the assignment is the inherited parent label GPT-6 Astra Pro. Q3–Q6 are preserved as labels because their question text was not supplied.

No full third-party page or raw tool response is written into these deliverables.
