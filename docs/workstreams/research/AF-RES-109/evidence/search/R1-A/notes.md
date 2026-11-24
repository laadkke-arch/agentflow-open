# R1-A controlled search notes

## Input and baseline

The supplied request reports Node-RED 3.1.0 and a mismatch between the flow menu's rename wording and its broader editing dialog. The author already found flow-level environment-variable editing in that dialog and requests a broader edit caption plus translation updates. Existing dialog behavior is the baseline. No discovered technique is represented as unknown to the author.

The source opening post was supplied as current text, with original edition unestablished. Its URL was not opened. The supplied input SHA-256 is 8751afc5b5f681615cdc533f7489a93e79c017fa915de023d339fa1f4e505eae; the hash is recorded as supplied.

## Actual search strategy

Method A used two English system2 queries:
1. `site.nodered.org docs flow properties edit environment variables menu`
2. `site.nodered.org internationalisation editor translation keys i18n`

The first located official flow documentation and a documented alternate route. The second sought official localization mechanics and incidentally returned i18next documentation. All search results were preserved in the displayed order: 20 for query 1 and 16 for query 2, with the first five explicitly ranked. Search previews were exposures rather than direct reads.

Four explicit opens were made: the flow guide, Node-RED node-authoring internationalisation guide, i18next translation-resolution URL, and a project wiki URL discovered in a result preview. The i18next URL redirected to its fallback page; the tool labeled its returned text a rewritten summary. The wiki fetch failed with DisabledError. No third query, click, find, reopen, shell networking, GitHub API, or alternate retrieval was used.

## Returned contributions

- **R1-A-T1 — proposed only:** preserve the documented existing flow edit action and compare menu access with tab double-click. Edit a variable while retaining the flow name, then reopen through the other route. This can reveal incorrect binding/targeting that checking the new caption alone would miss. The guide also identifies a documentation reference that may need to follow the UI wording.
- **R1-A-T2 — proposed only, conditional transfer:** omit one selected-locale entry while keeping the English caption in an isolated translation fixture. A translation-completeness check should fail even if configured fallback renders readable English. Node-RED's exact fallback mechanism is unverified, so this is a transferred failure-test principle.
- **Rank 3 vacant:** the node-authoring localization guide is useful background but does not establish the core menu binding. Its overlap with the second contribution does not warrant a third claim.

Current documentation editions are not treated as historical snapshots. Their availability in the exact retrieved form on 2024-01-01 is unknown.

## Unintended exposure and fidelity limits

Search automatically exposed pre-request Node-RED release previews from 2015, 2019, and 2021. None was opened. It also exposed replies in an unrelated December 2024 localization forum thread. That later thread was not opened or used as historical evidence. Other previews included community documentation, examples, PDFs, forums, Reddit, and video results; none was promoted as primary technical evidence.

No source-issue comments, status, linked PR, later same-issue release, or resolution were exposed. The original issue and its later solution were not inspected.

The i18next search preview and opened summary differ about the final fallback-array key. The proposed test avoids that detail and all unverified defaults. This discrepancy is recorded rather than silently reconciled. The failed wiki open left direct Node-RED/i18next integration unknown.

## Unfilled requirements and work not performed

The exact core menu translation key, catalog paths, locale inventory, menu attributes, dependency version, and runtime behavior remain unknown. There is no basis here for specifying translation strings in each language or an implementation patch. Q3–Q6 labels were requested by the evidence schema without question wording; they are retained as identifiers without invented answers.

No implementation, UI test, translation fixture, usability study, or regression test was executed. Both new tests are proposals. No claim is made that any fix shipped, that the current UI has the old label, or that these sources establish the author's prior knowledge.

Only the assigned prompt was read locally before writing this output. No sibling, central ledger, repository implementation, parent research, or additional request file was inspected. No git command or commit was run.

## Accounting

Queries: 2 of 3. Explicit opens: 4 of 6, including one failed open. Three successful unique primary-document opens are recorded; only two final candidate links are returned. The node-authoring guide is background evidence.

Search session UTC: 2026-11-24T01:52:01.773Z to 2026-11-24T01:53:57.962Z; 116.189 seconds. The initial prompt read preceded the controlled-search start and its logging instructions; its timestamps were not invented. Query/open timing is captured around each actual tool invocation. The three independent initial opens were dispatched concurrently and logged in dispatch order.

Displayed model identity: inherited parent label GPT-6 Astra Pro. Exact backend version, automatic engine reads, token use, and monetary cost are unknown. No raw third-party page copies are retained in these output files; summaries are paraphrased and short. Source titles, section identifiers, and necessary API identifiers are metadata rather than body quotations.
