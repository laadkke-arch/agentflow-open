# R4-B — controlled search arm

## Input and baseline

The supplied post, dated 2024-01-01T08:21:31Z, asks for a restricted node-selection area analogous to a drag handle. Overlapping nodes should allow clicks through some regions. The author's existing implementation sets selectable to false and uses a drag handle, preserving dragging but reportedly losing deletion because selection is required. That implementation is the baseline, not a discovery by this arm. The supplied current opening post is not verified as its original edition.

Assignment input SHA-256: 58e5a6870b870326fb391c173f025aba11d74708a0549ac8dfbfe32e1c09be1d. This is the supplied identifier; it was not independently recomputed.

## Method B decomposition

- **Target part:** the hit area that causes a front node to be selected.
- **Preserved conditions:** clicks outside the active area reach an overlapping node; the front node remains draggable from its existing handle; selection remains possible so the author's deletion workflow can operate.
- **Relation:** pointer location determines a hit target; the application's event handling changes selected state; deletion uses that state. Drag initiation is a related, separately controlled input path.

The post does not require a new keyboard workflow, a separate drag and selection region, multiselection changes, a particular browser, or a particular node component. None was made a requirement. The tests use ordinary clicks, dragging, and the configured deletion action.

## Actual search strategy

1. Same-domain query: `site:reactflow.dev custom node pointerEvents selectable dragHandle selection`.
2. Relational query: `click through overlapping elements except child interactive area pointer events`.

Both were English system2 queries. The second names neither a donor field nor React Flow. It surfaced a W3C standard alongside product documentation and unrelated discussions. A third query was unnecessary.

All 12 results from query 1 and all 24 from query 2 are logged in displayed order. The first five remain the first five; useful lower-ranked results were not promoted into those logs. The second query displayed search12 before search10 and search11; that order is preserved.

Six counted page actions followed: three initial opens, a same-document click, a reopen, and a find. The W3C anchor click returned the opening segment again, so it consumed a slot without verifying the target section. The final find directly exposed section 6.2. The component-reference reopen directly exposed the relevant interaction and keyboard properties. Raw responses were held only in orchestration memory; no third-party pages were copied into the output.

## Candidates and proposed tests

The three actual discovered links and their evidence are in returns.json. The candidates add an underlying hit-testing mechanism, a negative control for selection suppression, and drag/stacking discriminators. They do not establish that a selectHandle implementation already works.

| Test | Proposed discriminator | Status |
| --- | --- | --- |
| T1 | Exclude the front node's actual outer hit box while enabling one child; compare clicks outside/inside that child, handle dragging, and deletion after selection. | Proposed only |
| T2 | Compare a nodrag child with hit-test exclusion; log the receiving target and selected IDs to distinguish suppression from passing through. | Proposed only |
| T3 | Compare drag-induced selection settings and repeat the overlap click after selection can change stacking order. | Proposed only |

Expected results in returns.json are proposed acceptance conditions or narrowly attributed documented behavior. There were **zero executed tests**. The CSS mechanism is a component of the same web interaction domain; this arm does not claim a cross-domain transfer.

## Unfilled requirements and unknowns

The author's exact React Flow version, rendered wrapper hierarchy, CSS precedence, event handlers, and deletion configuration are unknown. No reproduction or implementation was built. Styling an inner body instead of the actual wrapper may leave a hit target in front; that is a proposed failure test, not an observed defect.

The directly read W3C edition is from 2026, and the React Flow pages are current live documentation. Their availability and exact behavior on the post's January 2024 date are unknown. Earlier W3C editions were linked but not read. No claim of historical novelty or absence is supported.

Q3, Q4, Q5, and Q6 were required as source-record identifiers without their question text. They are preserved without invented definitions.

## Unintended exposure and exclusions

The relational query automatically exposed unrelated Stack Overflow answers/comments, Reddit discussions, secondary documentation, academic security material, and later-dated SVG standards. These were recorded as search exposure and not opened or used as technical evidence. Preview-site React Flow documentation appeared in query 1 but was not opened. The W3C find also returned unrelated sections and change-appendix context; no issue discussion was followed.

No original source-issue URL, source-issue comment/status, linked PR, release, or later resolution was retrieved. No sibling or other repository file was read, no delegation occurred, and no git operation was performed.

## Timing and cost limits

Every web action has actual UTC start and return timestamps and elapsed seconds. The preliminary local prompt read was before the timed session and was not separately timed. The stop event closes the research interval before artifact serialization. Automatic engine reads, token use, immutable backend version, and monetary cost were not exposed and remain null/unknown. Only the parent-displayed model label, GPT-6 Astra Pro, is known.

