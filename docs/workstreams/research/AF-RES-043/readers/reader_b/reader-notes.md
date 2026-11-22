# Reader B notes

Reader: same-family fresh-context model reader; this is document reading, not a human study.
Assigned cases: N-S-01, T01, J01. Frozen input commit supplied: b3aa200fce66f0635e74aa39c4cb008cafd86eff (no git operation performed).
Key exposure: none. Protocol read before cards. Only assigned rows are selected for display, one card at a time, by presentation_index; tasks follow task_order. Each task starts independently, while previous exposure is explicitly retained in the record.

## reader_b-N-S-01-BX-C
- Local X displayed separately; no publisher verification or edition identification is inferred from this display.
- C: 보류 (normative_time_intent), 1 publisher open. Current landing page showed return-history revisions and CIZ transition; stopped because the unresolved temporal purpose is decisive. Tool rendering may be cached; no network timing claim.
## reader_b-N-S-01-BX-H
- Independent H start. Earlier exposure: same card C and its live landing-page response; those observations are not reused as H evidence. Local X displayed.
- H first open: current landing page; follow its actually rendered Historical Archives link 10 at L133.
- H: local_redisplay, 2 publisher opens. Archive index is not the historical record itself. Raw href spelling was not exposed by the web renderer; the actual link ID and resolved target are recorded. Consumer edition remains unconfirmed.
## reader_b-N-S-01-BL-C
- Independent C start; prior exposure: N-S-01-BX C/H (including current landing page and archive index). Only current card URLs and new responses will serve as evidence. No X in this card.
- C: 보류 (normative_time_intent), 1 publisher open; no second open needed for the unresolved decision criterion.
## reader_b-N-S-01-BL-H
- Independent H start; earlier exposure: N-S-01-BX C/H and this card C. The current card's additional archive URL is chosen as the first URL. Direct public HTTP is selected initially for the ZIP.
- H: publisher_edition_match for the card-added 2022 archive, 1 publisher open plus same-ZIP member inspection at budget 0. The 192607 Mkt-RF value matches the consumer example. Consumer's actual edition is not confirmed; the added archive cannot establish the full through-2023-03 output provenance. No network round-trip timing is claimed.
## reader_b-N-S-01-B-C
- Independent C start. Prior cards BX and BL (both tasks), including BL's 2022 archive, remain in memory; only this card's first URL is used and new evidence is recorded. No X.
- C: 보류 (normative_time_intent), 1 publisher open; initial response prefix displayed. Earlier archive knowledge was not used to choose a nonvisible URL.
## reader_b-N-S-01-B-H
- Independent H start with prior BX/BL tasks and this card C exposure acknowledged. Current-card original URL opened anew; no X.
- H first open and budget-0 window of the same response for the card's Fama-French factors. Actual archive link 10 is visible at L133; follow that link as the second open.
- H: unverified, 2 publisher opens. The archive index exposes further file links but the budget is exhausted. Previous-card archive content is not reused as evidence.
## reader_b-N-S-01-BLX-C
- Independent C start; prior BX/BL/B cards and all completed tasks remain known, without importing their evidence. Local X displayed.
- C: 보류 (normative_time_intent), 1 publisher open and separate X display.
## reader_b-N-S-01-BLX-H
- Independent H start; all earlier N-S-01 tasks acknowledged. Local X displayed. Card-visible 2022 ZIP is requested anew by direct public HTTP; prior downloaded files are not reused.
- H: publisher_edition_match for the additional 2022 archive; consumer_edition_confirmed=false. 1 publisher open, 1 local X display, and 1 same-document extraction (budget 0).

### Case N-S-01 completed
- 4 cards / 8 independent task readings recorded; no key exposure and no self-grading.
## reader_b-T01-B-C
- Independent C start. Prior exposure: all 8 N-S-01 tasks; no prior T01 card. Target is the current GDP product reference, distinct from endorsing 1.6 as current. No X.
- C: 유지, 1 publisher open. Decision applies to the functioning current-statistics reference; it does not approve 1.6 as the latest GDP value.
## reader_b-T01-B-H
- Independent H start; prior N-S-01 tasks and same-card C exposure acknowledged. Original product URL is opened anew; no X.
- H first open: current product page; follow actual News Release Archive link 32 at L61.
- H: unverified, 2 publisher opens. Archive filtering would require another document request; the original estimate text was not reached.
## reader_b-T01-BLX-C
- Independent C start; all prior N-S-01 and T01-B tasks acknowledged. Local X displayed. Target remains the original current-statistics reference.
- C: 유지 for the current product reference, 1 publisher open plus separate X display.
## reader_b-T01-BLX-H
- Independent H start, previous cards/tasks acknowledged. X displayed locally; choose the edition-specific URL visible in this card as first publisher open.
- H: publisher_edition_match, 1 publisher open. Date/title and first GDP paragraph match the explicitly named consumer edition; supersession is kept separate from historical wording.
## reader_b-T01-BL-C
- Independent C start; prior N-S-01 and T01-B/BLX tasks acknowledged. No X. Only current card original GDP URL is used for current-reference judgment.
- C: 유지 for the product reference, 1 publisher open. Historical number not treated as current.
## reader_b-T01-BL-H
- Independent H start; earlier cards and same-card C remain known. No X. The edition-specific URL is visible in this card and is freshly opened.
- H: publisher_edition_match, 1 publisher open; specified consumer edition confirmed against date/title/paragraph.
## reader_b-T01-BX-C
- Independent C start. Prior cards include T01 original-release access in BLX/BL; remembered URLs are not imported. Local X displayed. Current card original product URL is chosen.
- C: 유지, 1 publisher open; current-reference decision kept distinct from historical number.
## reader_b-T01-BX-H
- Independent H start. Earlier explicit-edition cards and this card C exposure remain acknowledged, but their URLs/evidence are not reused. Local X displayed; current-card product URL opened first.
- H first open recorded. Follow actual News Release Archive link 32 at L61; no remembered edition URL is requested.
- H: local_redisplay, 2 publisher opens. The earlier explicit-edition document is not imported into this task.

### Case T01 completed
- 4 cards / 8 independent task readings recorded; cumulative 16 judgments. No key exposure and no self-grading.
## reader_b-J01-BX-C
- Independent C start; prior N-S-01 and T01 exposures acknowledged, no previous J01 card. Local X displayed. Target is the original cohort sepsis-classification count, not the consumer's own 3,806 analyzed participants.
- C: 보류/access_failure, 1 failed publisher open retained. Redirect metadata is not treated as a qualifying document href; no retry or tool switch within C.
## reader_b-J01-BX-H
- Independent H start. Prior C DOI failure is acknowledged but remains a completed C observation. Direct public HTTP is chosen initially for H, requesting the same card-visible DOI (not the prior redirect target). No previous request is erased or retried within its task. Local X displayed.
- H local preparation error: optional bs4 import was unavailable before any HTTP request executed. This was not a publisher open and consumes no read budget. Replacing the local parser with Python standard library, with the first publisher request still pending.
- H: publisher_edition_match, 1 independent direct-HTTP publisher open. The 2018 article's abstract/results show the X count. Its visible 2024 correction link is noted, not followed or assumed. This H result does not repair or overwrite the failed C observation.
## reader_b-J01-BL-C
- Independent C start. Prior J01-BX C failure and H article body exposure acknowledged. No X. Choose the article/abstract URL actually visible in this card; no prior correction URL is imported.
- C first open: original article count and dated correction banner. Follow actual View correction link 56 at L152 as second publisher open. Web output labels its rendering as a rewritten summary; no byte-level edition identity is claimed.
- C: 교체, 2 publisher opens. The publisher correction explicitly replaces the original cohort sepsis count 3,716/4,989 with 3,806/4,989; the consumer's own analyzed sample is a separate claim.
## reader_b-J01-BL-H
- Independent H start; prior J01 original and correction exposure acknowledged. The current card's 2018 article URL is freshly opened. No X. Historical wording is the task target.
- H: publisher_edition_match, 1 publisher open plus a budget-0 display window of its Abstract. Historical count is recorded independently of the prior C correction result.
## reader_b-J01-B-C
- Independent C start; prior J01 original/correction exposure acknowledged. No X. Direct public HTTP is chosen initially for the only URL visible on this card, the DOI. No remembered article or correction URL is substituted.
- C first direct-HTTP open successful. Parsed first document actual anchor index 59: View correction, raw href /plosone/article?id=10.1371/journal.pone.0301218. Resolve against the current response URL; follow as publisher open 2 via the web tool.
- C: 교체, 2 publisher opens. Current first-document href was recorded verbatim and resolved; switching to the web tool for that distinct qualifying second document is not a failed-first-open repair.
## reader_b-J01-B-H
- Independent H start; all prior cards and same-card C acknowledged. No X. Direct public HTTP is chosen initially and the current card DOI is freshly requested; prior local source files are not reused.
- H: publisher_edition_match, 1 fresh direct-HTTP publisher open; the original 2018 abstract wording was observed anew.
## reader_b-J01-BLX-C
- Independent C start; prior J01 original/correction and all earlier tasks acknowledged. Local X displayed. Current card's article/abstract URL is freshly opened; prior correction URLs are not substituted.
- C first open recorded. The new response exposes actual View correction link 56 at L152; use it for publisher open 2.
- C: 교체, 2 publisher opens and separate X display. The currently reused original cohort count is corrected; the consumer's own analysis count is outside the modification target.
## reader_b-J01-BLX-H
- Independent H start; all earlier cards and same-card C exposure acknowledged without reusing evidence. Local X displayed. Open the current card's 2018 article/abstract URL anew.
- H: publisher_edition_match, 1 publisher open plus separate local X display.

### Case J01 completed
- 4 cards / 8 independent task readings recorded; cumulative 24 judgments.
- One failed publisher request (J01-BX-C DOI web open) is retained without repair. Direct HTTP in later independent tasks was selected initially and did not overwrite that failure.

## Reading completion
- All 12 assigned cards were handled in presentation_index order, with task_order C then H as shown on each assigned card.
- Same-family fresh-context model reader, not a human participant. Key exposure remained none. Prior exposure was acknowledged and not erased.
- No web searches, credentials, login/account actions, git operations, collection/key/versions/components/sources/report/other-reader reads, or writes outside reader_b were performed.
- Web results may be cached; no network round-trip or human timing claim is made. Some PLOS web renderings are labeled rewritten summary by the tool; those labels are retained in read outcomes. Direct HTTP responses are separately identified.
- The only local preparation exception was a missing bs4 import before any HTTP request; it is noted above, consumed no publisher-open budget, and was corrected using the standard library.
- No judgment was scored against an answer key or overwritten.

## Local record integrity check

{"judgments": 24, "cards": 12, "reads": 47, "publisher_opens": 31, "local_x_displays": 12, "same_document_actions": 4, "failed_publisher_opens": 1, "case_counts": {"N-S-01": 8, "T01": 8, "J01": 8}, "issues": []}

Schema presence, ID uniqueness, record linkage, task order indices, per-task publisher budget, separate X accounting, and key_exposure fields checked. No content correctness or answer-key grading was performed.
