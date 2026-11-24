# AF-RES-109 public aftermath review

Prepared UTC: **2026-11-24T02:49:08.120Z**. Direct retrieval window: **2026-11-24T02:33:40.367Z to 2026-11-24T02:37:51.539Z**.

The parent reported the complete search stage sealed at `628e33709b0be7a19486f1bfeaef93f42e129394` before authorizing these follow-up reads. This review records public actors and actions after the six January 2024 requests. The 2026 search recommendations did not precede those historical actions, and no causal attribution to this research is made.

## Six-request outcome ledger

| Request | Public issue | Observed follow-up | Original requester execution/confirmation |
| --- | --- | --- | --- |
| R1 | [Node-RED #4505](https://github.com/node-red/node-red/issues/4505) | PR #4506 merged January 5; listed in release 3.1.4 published February 6 | Not observed; issue has no comments |
| R2 | [Node-RED #4507](https://github.com/node-red/node-red/issues/4507) | Requester reports recovery after a Node.js upgrade and closes January 2 | **Explicit recovery statement**, with causal doubt |
| R3 | [Node-RED #4508](https://github.com/node-red/node-red/issues/4508) | Contributor diagnosis; PR #4526 merged January 16; listed in release 3.1.4 | Not observed; diagnosis is by another actor |
| R4 | [xyflow #3757](https://github.com/xyflow/xyflow/issues/3757) | Maintainer suggests a helper-based custom-node click handler and closes August 26 | Not observed |
| R5 | [xyflow #3758](https://github.com/xyflow/xyflow/issues/3758) | Maintainer suggests custom-edge paths and links an example; closes January 3 | Not observed |
| R6 | [xyflow #3759](https://github.com/xyflow/xyflow/issues/3759) | Maintainer tests, two merged fix PRs and release 11.11.3; later users report slow zoom | Original author has no post-fix confirmation in the returned thread |

All six issues are currently marked closed/completed. The issue state is distinct from verified requester adoption. There is **one explicit original-requester recovery account among six requests**, and **three requests with directly verified merged patches plus release listings**. Those are historical observations, not successful executions of this research's recommendations.

## Coverage and source handling

The review directly fetched the current issue object, comments, and timeline for each request through the GitHub connector's public REST GET capability. All six comment totals reconcile with the issue metadata: **24 comments** across the six requests. The timelines contain **76 events**. Every requested collection had fewer than its 100-row page limit; no second page was needed from the observed response lengths. Relevant fix commits, PR metadata and diffs, discussions/reviews, and release metadata were then read. A narrow January 1–6 commit listing located R1's merge because its issue timeline did not expose a PR reference.

There are **46 retrieval records** in `sources.jsonl`: **42 successful responses**, including **9 explicitly empty collections**, and **4 failures**. Empty comment/review arrays are successful observations. The file records actual URLs, UTC, actors, versions, exact sections/anchors, limitations and failures. Full third-party posts, comments and pages are not republished.

Every aftermath source row has `unique_primary_count: 0`. The original requests were already counted during recruitment, and comments, patches and releases in the same issue episodes do not create extra independent primary works for the research quota. A metadata fetch, repeated episode evidence, and an independent original work are different units.

The reader previously audited the execution logs, including their recorded unintended exposure. This is a separately documented post-search follow-up read, not a claim of outcome-blind discovery or independent source-fit adjudication.

## R1 — menu label and translations

The opening post already asks for the label and translation change. GogoVega opened [PR #4506](https://github.com/node-red/node-red/pull/4506) at **2024-01-01T14:37:31Z**. It explicitly references issue #4505. knolleary merged it at **2024-01-05T21:00:29Z**, and the issue closed one second later. The ten-file diff changes the menu lookup to `menu.label.edit` while retaining `core:edit-flow`, and removes the old rename key from nine locale catalogs. [PR diff](https://github.com/node-red/node-red/pull/4506/files)

The PR author checked a statement that `npm run test` passed. The added-tests checkbox is unchecked, and the changed-file list contains no test file. That is a contributor's reported test execution; no CI run was independently inspected and it is not a requester confirmation. The issue has zero comments, and the PR comment/review collections read here are empty. [PR checklist](https://github.com/node-red/node-red/pull/4506)

[Node-RED 3.1.4](https://github.com/node-red/node-red/releases/tag/3.1.4), published **2024-02-06T17:00:27Z**, lists this PR. Patch and release evidence establish a public change matching the requested label direction. They do not establish that camueller installed or tested it.

**Remaining observation:** a dated requester report identifying the installed version and observed menu/dialog behavior. CI artifacts for head `7f24de442f997e376b512b79258f083c6010a12e` would independently check the contributor's unit-test statement.

## R2 — recovery reported, cause uncertain

knolleary requested browser-console errors at **2024-01-02T10:11:34Z** and linked the parallel forum discussion. [Maintainer comment](https://github.com/node-red/node-red/issues/4507#issuecomment-1873829715)

At **2024-01-02T14:05:05Z**, goldriver2 explicitly reported upgrading Node.js and that the environment then worked, while doubting the upgrade as the explanation. The requester closed the issue at that timestamp. This is sufficient for a **reported requester action and recovery**, but not for a controlled causal diagnosis. [Requester confirmation](https://github.com/node-red/node-red/issues/4507#issuecomment-1874067118)

The version literals remain distinct: the opening post lists **18.16.1**; the GitHub follow-up says **18.6** to **20.10**. They are not silently reconciled. The linked [forum URL](https://discourse.nodered.org/t/flow-properties-tab-missing-3-13-cant-rename-a-flow/84186/2) failed through the web-open tool, so its exact body was not obtained during this pass. No linked patch or release appears in the retrieved issue timeline.

**Remaining observation:** access the forum post and dated console/environment details before assigning the recovery to a particular runtime change. The unambiguous positive is the author's recovery statement, not proof of why it recovered.

## R3 — diagnosed loss and merged credential handling

GogoVega's comment, created **2024-01-03T14:54:22Z** and updated **14:56:08Z**, describes a mismatch between changed-only global credential payloads and processing that expects a complete map. It includes editor/runtime observations and a pinned code location. This is another contributor's diagnosis, not a retest by requester kanunnikau. [Diagnostic comment](https://github.com/node-red/node-red/issues/4508#issuecomment-1875500460)

knolleary's [fix commit](https://github.com/node-red/node-red/commit/58e2fcbeee66f3f9096e9e434d4b69d975ddaac3), authored **2024-01-15T16:44:43Z**, changes the editor credential map and runtime handling of existing keys and masked unchanged values. [PR #4526](https://github.com/node-red/node-red/pull/4526) explicitly references issue #4508 and was merged by knolleary at **2024-01-16T11:58:20Z**; the issue closed one second later.

The two changed files are `env-var.js` and `credentials.js`. There is no added test file in that diff and no execution result in the read PR comments/reviews. [PR diff](https://github.com/node-red/node-red/pull/4526/files) The same [3.1.4 release](https://github.com/node-red/node-red/releases/tag/3.1.4), published February 6, explicitly includes PR #4526.

**Remaining observation:** a dated kanunnikau replay of the original add-plaintext-variable sequence on a named fixed version, and any CI/regression artifacts for head `58e2fcbeee66f3f9096e9e434d4b69d975ddaac3`. Merge, fixed label, and release inclusion do not substitute for that requester retest.

## R4 — suggestion and closure without requester confirmation

moklick posted a helper-based suggestion and closed the issue at **2024-08-26T15:24:13Z**. The comment proposes using `updateNode` from a button or other custom-node area. Its actual snippet sets **`selected: false`**. That value is preserved; this review does not repair it to `true` or claim the snippet demonstrates successful selection/deletion. [Maintainer comment](https://github.com/xyflow/xyflow/issues/3757#issuecomment-2310479396)

The thread has one comment and no original-requester reply. No linked patch, release or test result appears in the retrieved timeline. The public observation is a maintainer-provided option followed by closure.

**Remaining observation:** a dated 0p3r4t0r reply or public implementation showing the reported click-through, dragging, selection and deletion interactions, with the relevant helper version.

## R5 — custom-edge reference and recoverable title edit

At **2024-01-03T11:56:39Z**, moklick recommended a custom edge whose path changes when another edge is present, linked a bi-directional-edge example, and closed the issue. There is no later comment by vseverestek. [Maintainer comment](https://github.com/xyflow/xyflow/issues/3758#issuecomment-1875259548)

The linked [Custom Edges page](https://reactflow.dev/examples/edges/custom-edges) was directly read in its current edition. It includes a bi-directional example and imports `BiDirectionalEdge`; the imported component body and a January 2024 snapshot were not obtained. No example runtime was executed. Current page content establishes what is available at retrieval, not what the requester tried or the exact historical example.

The [timeline rename event](https://api.github.com/repos/xyflow/xyflow/issues/events/11365940209) records a title change by vseverestek at **2024-01-01T19:31:27Z**, **26 seconds after creation**. The prior ending was **“auto spacing node.”** and the replacement ending **“auto spacing between edges.”** This is actual title-edit provenance. It does not recover the opening-post body or prove the complete current title/body was the first edition.

**Remaining observation:** historical body-edit evidence or an archive contemporaneous with **2024-01-01T19:31:01Z**, the January 2024 example source, and an explicit requester implementation/test report before crediting adoption or working automatic spacing.

## R6 — fixes, corrected test reports and residual slow zoom

The original author aleib's only follow-up clarifies use of a MacBook touchpad with Windows simulated through Browserstack/Parallels, alongside reports from Windows-laptop users. It is pre-fix reproduction context. [Requester clarification](https://github.com/xyflow/xyflow/issues/3759#issuecomment-1877253792)

| UTC date | Actor and observation | Evidence |
| --- | --- | --- |
| 2024-01-31 | peterkogo describes event-classification investigation and links a wheel checker | [Comment](https://github.com/xyflow/xyflow/issues/3759#issuecomment-1919014613) |
| 2024-02-08 04:44:39 | tubarao312 says the checker distinguishes pinch/scroll and initially describes the Figma example as working slowly | [Initial report](https://github.com/xyflow/xyflow/issues/3759#issuecomment-1933356224) |
| 2024-02-08 15:35:09 | tubarao312 retracts that positive example statement, specifying Windows 11/Lenovo touchpad and no pinch zoom | [Correction](https://github.com/xyflow/xyflow/issues/3759#issuecomment-1934384383) |
| 2024-03-28 | moklick reports that removing the macOS-only guard works in a Windows 11/Parallels/MacBook setup, then asks for real-Windows checking | [Limited test](https://github.com/xyflow/xyflow/issues/3759#issuecomment-2024826540) |
| 2024-04-30 | moklick announces fixed versions and closes the issue; the current comment was subsequently edited May 2 | [Fixed-version claim](https://github.com/xyflow/xyflow/issues/3759#issuecomment-2085825155) |
| 2024-06-28 | vitaliimelnikov reports Windows pinch works but is slow | [Residual problem](https://github.com/xyflow/xyflow/issues/3759#issuecomment-2196546763) |
| 2024-07-02 | ChaitraK01 reports very slow Windows pinch | [Residual problem](https://github.com/xyflow/xyflow/issues/3759#issuecomment-2202581188) |

The directly read [system commit](https://github.com/xyflow/xyflow/commit/d1b50707ff7a5428963a1c303d79eb0b0ba3a627) and [core commit](https://github.com/xyflow/xyflow/commit/9eef7048f52c1117c5e2841300fb470cbb9bc89f) remove the macOS-only guard from the Control-modified pinch path. [PR #4229](https://github.com/xyflow/xyflow/pull/4229) was merged into `next` at **2024-04-30T15:47:30Z**; [PR #4230](https://github.com/xyflow/xyflow/pull/4230) into `next-v11` at **15:57:17Z**. Both were authored and merged by moklick.

[Release 11.11.3](https://github.com/xyflow/xyflow/releases/tag/11.11.3), published **2024-04-30T16:11:31Z**, explicitly references PR #4230 and issue #3759. Version **12.0.0-next.17** remains a maintainer statement in the current edited comment: its unscoped release lookup returned 404, and the encoded scoped-tag lookup was rejected by the connector with 400. Those failures do not prove the package/version was absent.

The linked [wheel checker](https://codesandbox.io/p/sandbox/wheel-checker-4y5m8l) could not be opened. Its reported results are therefore attributed to the commenters, not to an independently read or executed test. The PR #4230 file list contains a changeset and implementation code, without an added test file. No CI run or hardware/browser reproduction was executed by this reviewer.

No post-fix confirmation by **aleib** appears among the 19 comments. Other participants' tests are not relabeled as the original requester's execution. Later slow-zoom reports prevent an unqualified full-resolution statement. Downstream dependency-upgrade cross-references in the timeline were not treated as requester adoption.

The issue object's `closed_at` is **16:13:48Z** while the closure timeline event is **16:13:49Z** on April 30. Both timestamps are retained. The one-second metadata difference is not treated as a different outcome.

**Remaining observation:** recover the checker source, inspect a dated next.17 package/tag artifact, locate an existing aleib retest account, and collect distinct device/browser/event traces for residual slow zoom. These are next reads or observations, not messages sent or tests performed.

## Original-edition and causal limits

No full original opening-post edition was recovered for any of the six requests. The R5 title rename is positive evidence of an edit, but does not fill the missing original-body requirement. REST `updated_at`, a current body, a closed state, or a body-version marker alone is not first-edition proof. Several comments also have later update timestamps; their current wording is not assumed to be their first wording.

The merged patches and public statements occurred in **2024**. Search discovery occurred in **2026**. No public actor is shown receiving or executing these research recommendations. Historical implementation, requester recovery, contributor testing, and a recommendation's causal effect remain separate fields in the ledger.

## Retrieval gaps and exact next steps

| Missing read | Observed failure | Next exact read/action |
| --- | --- | --- |
| R2 linked forum post | Web-open tool reports inaccessible URL | Read the same public post through an accessible renderer; preserve its version literals and authorship |
| R6 event-checker source | Web-open tool reports inaccessible CodeSandbox URL | Inspect the linked public sandbox's source without claiming a browser/device result unless actually observed |
| R6 next.17 release metadata | GitHub 404 for unscoped tag; connector 400 for scoped path | Inspect the exact published package/tag metadata for `12.0.0-next.17`; keep the existing maintainer statement separately |
| All six original bodies | REST responses provide current bodies and event metadata | Obtain a public edit-history version or contemporaneous archive with a verifiable title/body boundary |

## Output validation

`aftermath.csv` has exactly **six unique request rows** and 31 named columns. Embedded JSON fields parse; original UTC source strings are preserved, including the R6 closure discrepancy. Spreadsheet-cell date conversions were checked against their source instants before CSV serialization. All source IDs referenced by request rows are defined in the 46-row source ledger. Dates, actors and patch/release links are recorded separately from tests and requester confirmations.

Only the requested files under `evidence/aftermath/` were written. No external message, account change, paid API, source-code mutation, central-ledger edit, git command or commit was performed.

