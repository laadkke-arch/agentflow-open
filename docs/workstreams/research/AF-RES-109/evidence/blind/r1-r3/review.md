# Blinded technical adjudication: R1–R3

## Scope and evidence boundary

This automated adjudication covers all 15 variants in 12 packet groups. Those groups contain 11 distinct candidate URLs because D01 and D04 use the same Node-RED guide. The search outputs were remotely sealed at `628e33709b0be7a19486f1bfeaef93f42e129394`. The blinded packet was generated from those sealed outputs afterward and is intended for inclusion in the adjudication bundle. Only that blinded packet and its three explicitly supplied natural-input caches were read locally. Method names, ranks, candidate tables, search logs, mappings, task/PLAN files, issue discussions and aftermath were not read. No git operations were performed.

The creation dates supplied separately from sealed metadata are R1 **2024-01-01 10:50:08 UTC**, R2 **2024-01-01 21:23:17 UTC**, and R3 **2024-01-03 12:47:55 UTC**. The original request-body editions remain unverified. Newness here means absent from those supplied bodies. It makes no claim about what the original authors knew.

Candidate sources were directly reopened between **2026-11-24 02:27:28 and 02:32:00 UTC**. Ten distinct candidate URLs yielded relevant bodies. The Function-node page yielded repository identity only; target-section reads and finds repeatedly returned HTTP 503, while raw/tagged views were restricted or disabled. Earlier source-reading claims were never accepted as substitute evidence. Every success, failed acquisition, edition, timestamp and relevant section is recorded in `sources.jsonl`; incidental search excerpts are labelled separately and are not direct-page confirmations. Timestamp values are tool-call or immediately post-response clock observations, not invented publication timestamps.

No proposed test was executed. No Node-RED or donor application/source program, credential store, browser DOM inspection, or API mutation was run. Only artifact-construction and structural-check scripts ran. Source code appearing in the Auxx article is an unexecuted excerpt; the Node-RED comparator’s operative body was not read. This is an automated review, with no human-review claim. All source records have `counts_as_unique_primary: false` and `count_category: post_search_verification`.

## Decision rubric and counts

A condition marked **yes** is covered by the proposed change’s stated contract; it is not proof that a fix works. **Partial** denotes a diagnostic or conditional/incomplete contribution, **no** a bypass or missing condition, and **unknown** an evidentiary gap. Repair fit, newness, and availability in 2024 are separate assessments.

| Request | Variants | New implementation flags | Distinct current choice keys | New test flags | Distinct accepted tests |
|---|---:|---:|---:|---:|---:|
| R1 | 4 | 0 | 0 | 4 | 3 |
| R2 | 6 | 0 | 0 | 5 | 4 |
| R3 | 5 | 4 | 3 | 5 | 5 |
| Total | 15 | 4 | 3 | 14 | 12 |

Flags are per-variant eligibility judgments and must not be summed as unique discoveries. D01-V1/V2 share one test; D04-V1/V2 share one test; D09/D10 share one preserving-update choice. D06 receives no accepted count because its source-derived comparator remains unverified. These are current, conditional technical counts, not blanket claims of historical availability. All three R3 choice families still require target-specific validation.

## R1: label meaning and localization

The requested Rename-to-Edit change and translation updates are already the baseline. D01’s documented action and alternate route contribute one regression comparison: preserve the flow identity/name while a variable changes and survives reopening. This is additional testing, not a new implementation decision. The source still displays the older caption, so it cannot establish current software wording or a shipped repair. [S01](https://nodered.org/docs/user-guide/editor/workspace/flows)

D02 adds a genuinely discriminating negative fixture: deliberately omit the selected locale’s entry and verify that a completeness check fails even if fallback produces readable text. That is not equivalent to a nonempty-caption smoke test. It does not supply translations, verify their semantics, or establish Node-RED’s exact fallback configuration. A post-search Node-RED catalog guide strengthens the catalog-level direction but does not identify the core-menu key. No library default or fallback-array ordering is assumed. [S02](https://www.i18next.com/principles/fallback) [S12](https://nodered.org/docs/creating-nodes/i18n)

**Strong near miss:** Microsoft’s Properties convention supplies a useful first-click comparator, but it does not establish that Properties is better than the requested Edit and existing dialog title. D03 gets a test credit only. Its first-party footer is dated 2022-02-08; that supports pre-request guidance, without establishing archived 2024 bytes. [S03](https://learn.microsoft.com/en-us/windows/win32/uxguide/cmd-menus?source=recommendations)

## R2: visible Properties and renaming inside it

D04 adds one alternate-entry comparison. The baseline already says the outer pane opens, so repeating double-click alone is rejected as novelty. Comparing menu and double-click outcomes can distinguish entry-dependent state, but both may reach the same failure, and cancel/reopen order is a confound. Merely finding a name input does not prove a saved rename. [S01](https://nodered.org/docs/user-guide/editor/workspace/flows)

D05 adds a selector/selection/panel state partition from a dated 2015 W3C draft. That source is primary authoring guidance, not an independent Node-RED implementation, and its section explicitly awaits review. D06 claims a concrete same-product realization, but the source-body failure prevents confirmation. Its proposed checkpoints overlap D05 and are held without a second accepted test. The attempted historical flow-editor source was also inaccessible. [S04](https://www.w3.org/TR/2015/WD-wai-aria-practices-1.1-20150514/) [S05](https://github.com/node-red/node-red/blob/main/packages/node_modules/@node-red/nodes/core/function/10-function.html)

D07 adds a separate observation boundary: missing DOM versus an existing control hidden by resolved presentation state, with ancestor/layout checks and declaration provenance. Its first-party page is dated 2022-11-15 UTC. This is a useful diagnostic, not a new UI implementation. [S06](https://developer.chrome.com/docs/devtools/css/issues)

**Strong near miss:** D08’s API rename bypasses both pane-specific conditions. It remains a valid test of configuration persistence, restricted to the proposed disposable empty flow. Empty arrays on a populated flow would not be an equivalent test. The source’s response table and prose disagree about the body, so the oracle must be the independently reloaded label. [S07](https://nodered.org/docs/api/admin/methods/put/flow/)

## R3: secret intent, preserving updates, and existence

The report already establishes an initially working credential read and combines two later interventions: adding global plaintext state and editing the Inject flow. None of the donor sources proves that the saved secret was overwritten. The first needed observation is where a synthetic value first changes: outgoing request, persisted credential, or runtime resolution.

D09 and D10 share a preserving-update choice. D09 couples mask filtering to a merge that retains omitted siblings at the correct nesting depth; its fixture observes both filtered delta and storage. D10 compares omission, complete redacted input, and deliberate replacement. Those are different discriminating tests of related boundaries. A patch that explicitly supplies a mask can still corrupt the value, and a client read-modify-write built from redacted data cannot recover the original. Stable variable identity is an additional target premise. [S08](https://auxx.ai/blog/connections-part-2-secret-lifecycle) [S09](https://developer.hashicorp.com/vault/docs/commands/kv/patch)

D11-V1 proposes the separate presence/edit-intent representation already illustrated by ordinary Node-RED credentials, transferred conditionally to global updates. Its intervention-isolation test is new: change plaintext global state while holding the reading flow constant, then change only the flow, plus deliberate secret replacement. D11-V2 contributes a same-product component control only. Ordinary node credentials may use different storage and serializers, so the control does not prove a global fix. [S10](https://nodered.org/docs/creating-nodes/credentials)

D12 adds existence-sensitive validation: retain-existing intent is meaningful only with a stored value. Its create-versus-update pair is new relative to the baseline, but rejection on create is a proposed donor policy, not a supplied Node-RED requirement. A legitimate secret equal to a marker needs an explicit contract. Vendure clears on empty input, while Auxx retains; those incompatible choices must not be silently merged. [S11](https://docs.vendure.io/current/framework/developer-guide/secret-fields)

**Strong direct control and near misses:** ordinary Node-RED credential metadata is the strongest same-product conceptual comparator; it still is not the global path. Vault patching alone misses explicit mask input. Auxx’s article is dated 2026-08-18, and the inspected Vendure edition was edited 2026-07-31. Their current usefulness cannot become 2024 discovery credit; earlier mechanism availability remains unknown. A publisher-versioned Vault 1.15 page and a first-party 2023-09-28 release announcement provide qualified historical support for D10, but the live version navigation is internally inconsistent and no immutable pre-request command revision was obtained. [S13](https://developer.hashicorp.com/vault/docs/v1.15.x/commands/kv/patch) [S15](https://www.hashicorp.com/es/blog/vault-1-15-brings-ui-updates-pki-enhancements-new-betas-and-more)

## Genealogy and remaining evidence

Different URLs do not imply different mechanisms. The Node-RED chapters share one project authority; D01/D04 are one work. W3C and Microsoft supply primary design guidance, not independent implementations. Chrome supplies a diagnostic facility. Auxx is first-party testimony about its own implementation, while Vault and Vendure document their own product contracts. The credential proposals remain in the same software secret-edit/update domain despite product differences. S09/S13 are editions of one work; the release announcement is dating evidence only. `lineages.json` preserves these relationships and distinct operative subchoices.

The concrete next observations are recorded for every variant in `judgments.jsonl`. None requires believing a source-derived root-cause story first. A pane repair still must demonstrate visibility through double-click and a persisted rename inside that pane; a credential repair still must demonstrate initial and post-update Inject resolution. No source reread, historical follow-up, synthetic test proposal, or repeated chapter increases the sealed original discovery count.
