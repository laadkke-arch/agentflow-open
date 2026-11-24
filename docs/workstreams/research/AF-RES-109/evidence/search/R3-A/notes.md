# R3-A — controlled search arm

## Input and baseline

The supplied opening post reports Node-RED 3.1.3 global credential values becoming `__PWRD__` after adding a plaintext global variable and updating an Inject flow. The values initially work. The author already references an earlier flow-level problem and its stated fix; those are baseline information, not discoveries from this arm. Node.js v16.20.2, npm 8.19.4, Docker, Linux, and Firefox 121.0 are supplied environment details, not independently verified facts.

The post includes two edits before the failure check: a global-variable edit and a test-flow edit. It does not show the network request, secret persistence state, implementation, or original historical opening-post edition. A masked runtime result does not itself identify where the value changed.

The supplied input hash is recorded verbatim. The prompt supplies no canonical byte-boundary specification for independently reproducing that hash.

## Actual strategy and acquisition

1. Query the official Node-RED documentation for node-password handling. Search returned 13 displayed results. Open the credential guide, rank 1, directly.
2. Adapt to the editor/runtime asymmetry by searching HashiCorp's documentation for partial secret updates. Search returned 12 displayed results. Open the KV patch command guide, rank 2, directly.
3. Stop after two queries and two explicit opens. One query and four open slots remain unused. No additional query was issued to fill a quota.

Each query/open is timed in UTC in events.jsonl. Result ranks are preserved. Every additional result beyond rank 5 is also listed; no top-five rank is missing. Open responses report the same original and final URLs; no redirects or failures occurred. Search snippets and directly read pages are distinguished.

## Useful returns

**R3-A-S1 — Node-RED credential guide.** The directly read page distinguishes runtime values from the editor's indication that a password exists. This suggests inspecting the conversion from an unchanged editor field into a credential update. It documents per-node credentials; applying the distinction to global variables is an inference.

**R3-A-S2 — Vault KV patch command.** The directly read page supplies a concrete comparison between updating only supplied fields and reconstructing a complete secret-bearing record. This suggests checking preservation when credential entries are omitted from an unrelated update. It does not establish any Node-RED endpoint's behavior.

Candidate rank 3 is vacant. Adjacent documentation was mostly redundant and was not opened merely to produce another return.

## Proposed tests and what they discriminate

**T1 — proposed, not executed.** Separate the plaintext settings edit from the Inject-flow edit, keep the original secret-reader unchanged in the first case, and trace presence metadata, outbound secret fields, stored values, and runtime output. Use a deliberate secret replacement as a control. This can locate a mask-to-value conversion and avoid assuming either edit is the sole trigger.

**T2 — proposed, not executed.** Seed a secret plus a plaintext entry, submit only a new plaintext entry to the candidate save boundary, and compare that with the full editor payload. Then submit an intentional secret replacement. This distinguishes omission-preserving semantics from full replacement and checks that preservation does not prevent intentional changes.

Neither test is a result, fix, or guarantee. No Node-RED or Vault instance was run, and no requests were replayed.

## Unfilled requirements and limitations

The exact global-variable data model, save contract, credential identifiers, deletion behavior, persistence format, root cause, and implementation costs remain unknown. Whether loss is durable, recoverable, browser-specific, deployment-mode-specific, or limited to one editor session was not tested. No requirement for concurrency, a replacement secrets manager, a new HTTP API, or versioning is inferred from the post.

Historical availability at 2024-01-03 is unestablished for both live pages. Vault's current version selector and example timestamps do not resolve this. The opening post's original edition is also unestablished. The author's prior knowledge of either mechanism is unknown.

The instruction asks for question identifiers Q3–Q6 but gives no question wording. The source rows retain those literal identifiers without inventing definitions.

## Exposure and exclusions

No original issue URL, issue comments, status, linked PR, release, or later same-issue resolution was opened or returned in search. Supplied forum URLs were not opened. Generic Node-RED navigation, a Twitter-node example link, HashiCorp navigation, current version links, and a HashiConf 2025 banner were displayed. The first search also returned a forum-hosted PDF of unverified relevance; it was not opened or used as evidence.

No other request, arm, repository, HANDOFF, or sibling file was read. No delegation, git operation, central-ledger edit, shell network retrieval, or alternative internet tool was used. Raw responses were held in session store only; full third-party pages were not copied into these output files.

## Accounting

- Individual queries: 2 of 3 maximum.
- Explicit opens: 2 of 6 maximum.
- Directly read independent primary works: 2.
- Returned candidate links: 2; vacant ranks: 3.
- Actual tests executed: 0.
- Automatic engine reads, token use, exact immutable model version, and monetary cost: unknown.
- Inherited model's displayed parent label: GPT-6 Astra Pro. No more specific identity was exposed.
