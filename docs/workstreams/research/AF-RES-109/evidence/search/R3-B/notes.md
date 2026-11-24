# R3 — Arm B

## Input and baseline

The supplied opening post reports Node-RED 3.1.3 global environment credentials initially resolving correctly, then resolving to the display marker `__PWRD__` after an additional plaintext global variable is saved. Its existing global-variable implementation and referenced earlier flow-variable fix are baseline context, not discoveries of this arm. Neither linked discussion nor any issue resolution was opened.

The target is the global credential value across an unrelated configuration edit. The preserved condition is that existing credentials remain usable after adding the plaintext entry. The operative relationship is: existing secret plus a collection edit → serialization, update, and subsequent read → original secret remains the runtime value. A possible display-marker/persistence boundary failure is a hypothesis, not an established cause.

## Actual search strategy

1. Same-domain query: `Node-RED creating nodes credentials password has_password unchanged`.
2. Relational query: `configuration update masked secret placeholder preserve existing value unchanged fields`.

The second query names neither Node-RED nor a donor field or product. Its relationship came from the supplied reproduction: changing one configuration entry should preserve another stored value. No third query was needed.

All 24 results from query 1 and all 18 results from query 2 are in `events.jsonl`, retaining their displayed order. Both top-five lists were complete. Four explicit opens covered three independent works; the fourth was a Vendure reopen because its initial page window showed only navigation. No click, find, networking fallback, or other internet retrieval was used.

## Returned candidates and proposed tests

The returned links are ranked for diagnostic usefulness, separately from the untouched search rankings. Detailed source facts and limitations are recorded in `sources.jsonl`; exact candidate fields are in `returns.json`.

- **T1 — persistence boundary, proposed only.** Use two existing credentials and add one plaintext variable. Inspect the filtered update and persisted state separately. This distinguishes failed marker filtering from a later write that drops omitted stored values. The logical fixture is not a claimed Node-RED wire format.
- **T2 — existence boundary, proposed only.** Compare an unchanged placeholder for a stored credential with the same placeholder for a credential that has never been stored. The source's rejection rule for creation is a possible design choice; the natural request does not specify creation behavior.
- **T3 — same-domain control, proposed only.** Compare an ordinary node credential with a global credential across the reported edit, checking editor presence state and runtime values separately. This does not claim that global variables expose the same metadata fields.

These tests were not executed. The input already supplies an end-to-end reproduction; the added value here is intermediate observation and contrasting cases, not rediscovering that reproduction.

## Unfilled requirements and limits

No implementation was inspected or modified. There is no demonstrated root cause, verified patch, passing regression test, or guarantee of compatibility with Node-RED 3.1.3. Global storage shape, credential identity matching, save/deploy boundaries, and deletion semantics remain unknown.

The natural request does not specify whether empty input should retain or clear a credential. The returned sources use different policies, so neither is silently imposed. Ordinary node credential handling is an existing component; using it as a global-variable diagnostic control is an inference.

Auxx's article is dated 2026-08-18, after the 2024-01-03 request. The Vendure current page displays v3.8.2 and an edit date of 2026-07-31; its original availability is unknown. The Node-RED page is undated. These acquisitions therefore do not establish that all candidate evidence was available at the report's date.

## Exposure and what was not tested

Search exposed other Node-RED forum snippets, a third-party wiki mirror, vendor documents, videos, and Reddit results. They were logged but not used for technical claims. No visible result exposed the source issue's comments, status, linked PR, release, or later resolution.

Direct pages necessarily exposed navigation and related links. Auxx's page also discussed OAuth refresh, which was not adopted as a requirement or candidate test. The Vendure page exposed encryption and API-access behavior beyond the chosen edit boundary; those topics were not independently tested.

No Node-RED container, browser workflow, source code, API, or donor implementation was run. No immutable historical edition was retrieved. The counts concern explicit retrieval actions; automatic engine reads, exact backend model version, token usage, and monetary cost remain unknown.

## Audit scope

Only the assigned prompt and this arm's output files were read locally. No sibling or central research file was inspected, and no Git action was taken. UTC bounds surround each web tool action. Concurrent first opens have separate bounds; event order identifies operations and is not a claim about their completion order. The assignment supplied the input hash; local validation records any independently reproducible match. No full third-party page is stored in this output directory.
