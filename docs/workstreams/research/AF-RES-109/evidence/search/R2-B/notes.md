# R2 — Method B search arm

## Input and baseline

The supplied report says double clicking a flow opens an editing pane, but the Properties section is missing and the author cannot rename the flow. That already-working activation route is the baseline. An unmentioned menu route is absent from this account; it is not proved unknown to its author.

Preserved environment: Node-RED version string **3.13**, Node.js **18.16.1**, npm **8.3.0**, Windows and Chrome. The version string was not silently normalized to 3.1.3. The exact browser build, viewport, editor configuration, installed extensions and stored UI state are unknown. The example-flow block is a placeholder. The screenshot URL was supplied but not opened or interpreted. The supplied current opening-post edition is not established as the original edition.

Input SHA-256 from the assignment: `5f983c942a9ccf4273bb3d3309ecc81617439d0ed0574dd32f183b3f3efcdf87`. This identifier was supplied, not independently recomputed.

Before searching, the target part was decomposed as the flow-edit pane's Properties selector/name control. The operative relationship was: **double-click activation → outer pane opens → expected Properties/name controls are absent**. Opening the outer pane therefore does not by itself establish that the inner editing controls initialized correctly. No new user requirement was added.

## Actual search strategy

1. Same-domain query: `Node-RED flow properties dialog rename flow tab official documentation`. It returned 23 ranked results. The official guide supplied an alternative menu entry route for a controlled comparison with the baseline.
2. Relational query: `tabbed dialog selected tab panel hidden keyboard navigation`. It named neither a target product nor a donor field. It returned 19 ranked results. The dated W3C working draft was selected to inspect the relationship between selection and visible panel. This is generic web UI component guidance, not evidence of a novel cross-domain transfer.
3. Same-domain component query: `"Node-RED" "RED.tabs" "scrollable"`. It returned one ranked result; ranks 2–5 are explicitly missing. The unrelated forum result exposed an official core Function editor source link. The word scrollable was an exploratory candidate mechanism, not an inferred requirement or diagnosed cause.

The arm used exactly **3 query items and 6 explicit opens**, with every click/find counted. Initial W3C reading did not reach the desired passage; the contents-link click repeated the initial excerpt, and a subsequent find exposed section 2.31. The official Function file first returned metadata/line numbers; a find exposed the tab setup implementation. The requested master URL redirected to main. No raw fallback, API, shell networking or other search engine was used.

Search-event result arrays preserve every ranked result in its displayed order; reference suffixes were never used to reorder ranks. Embedded links from the last result are identified separately without invented rankings. Raw responses were retained in functions store during this arm and were not copied into these outputs.

## Returned choices and proposed tests

- **T1 — entry-route comparison.** The official flow guide supplies a rename menu entry point absent from the report. Compare it with double click on the same flow. A difference supports investigating route-dependent state/dispatch; failure through both weakens a double-click-only account. Source: [official flow guide](https://nodered.org/docs/user-guide/editor/workspace/flows), direct-read event 3.
- **T2 — selection and visibility.** The W3C tab pattern supplies a way to distinguish an absent selector from a present selector whose corresponding panel does not become visible. Inspect those states in the failing pane before choosing a repair. Its keyboard conventions are not asserted to be implemented in the reported Node-RED build. Source: [dated W3C draft](https://www.w3.org/TR/2015/WD-wai-aria-practices-1.1-20150514/), direct-read event 7.
- **T3 — registration and activation checkpoints.** Current core Function editor code gives a concrete comparator: tabs are registered, a starting selection is made, and the selected identifier determines displayed content. Instrument the actual flow-pane opening to distinguish absent registration from failed selection/content lookup. The Function component is not claimed to be the flow component. Source: [official Function editor source](https://github.com/node-red/node-red/blob/main/packages/node_modules/@node-red/nodes/core/function/10-function.html), direct-read event 9.

**All three tests are only proposed. None was executed.** T2 and T3 overlap conceptually; T3 adds concrete implementation checkpoints. No root cause, successful workaround, repair or reproduction is claimed. No candidate is described as an invention.

## Evidence limits and unfilled needs

The official guide and current source do not establish behavior in the reported build. Their historical availability in the inspected form is unknown. The W3C edition has a 2015 dated official URL, preceding the issue, but it is explicitly a working draft, and its tab section says review was pending after incorporation from APG 1.0. It is not a Node-RED implementation specification.

The flow editor source itself, immutable historical revisions, the actual registration/selection state, whether the tab control or only its content is missing, and a runnable example remain unverified. No DOM, accessibility tree, console output, browser storage, network request, installed-node list, viewport variation, browser comparison or operating-system comparison was inspected. No flow was edited, renamed or deployed. Source-issue comments, status, linked PRs, releases and later resolution were not inspected.

## Unintended and incidental exposure

The first query exposed unrelated community discussions and derivative guides. The second exposed contemporary tab guidance and source copies of some pages. The third exposed an unrelated December 2024 Node-RED forum discussion, later than the supplied January 2024 report, including source links and examples. Those forum claims are discovery material, not primary technical support.

Opening the official GitHub file exposed generic repository navigation, issue/PR counts and links. No particular source-issue status, source-issue comments, same-issue PR or resolution appeared or was followed. The page explicitly reported a master-to-main redirect and a rewritten-summary representation. These limitations are retained in the event/source records.

## Accounting

Every web action has actual UTC start/end timestamps from the functions.exec runtime clock, measured elapsed seconds, query or requested URL, returned refs and exposure notes. The initial assigned-prompt read precedes the timed search interval. The stop record closes research/output preparation immediately before writing these files; retrieval-end time is separately recorded.

Three unique primary works were directly read. Six source rows retain every explicit open, including duplicate and partial reads. Repeated reads and fragments are not counted as independent works. No prose quotations are included; source titles, section names and code identifiers are metadata.

Automatic backend reads, token usage, monetary cost and an exact immutable backend model/tool version are **unknown**, represented by null rather than zero. Only the inherited displayed parent label **GPT-6 Astra Pro** is exposed. Q3/Q4/Q5/Q6 are retained as the supplied question labels; their definitions were not provided, so none was invented.
