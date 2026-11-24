# R5-A isolated search notes

## Input and baseline

The supplied opening post asks for examples or references for multiple edges on the same node(s), with automatic spacing. It supplies no code, package version, layout algorithm, or existing implementation. There is therefore no author-mentioned implementation to rebrand as a new contribution. The returned choices are absent from the supplied text; this does not establish that the author did not know them.

The post's image URL was supplied but its pixels were not inspected. Whether the intended arrangement is parallel edges between one pair of nodes, general fan-out, separate ports, or another geometry remains unresolved. No gap size, direction, collision rule, or acceptable change to node placement was inferred as a requirement. The source-post date is 2024-01-01T19:31:01Z; the current opening-post edition is not established. The assigned input hash is recorded without claiming an independent historical reconstruction.

## Actual search strategy

1. Search React Flow's official site for multiple edges, nodes, spacing, and handles. This exposed handle configuration and a duplicate-insertion rule. Open the handle guide and addEdge utility reference.
2. Search ELK's official site for multiple edges, spacing, ports, and routing. This exposed configurable automatic port spacing and limited-space behavior. Open the spacing guide, Layered algorithm reference, and node-size options.

The exact English queries, rankings, timestamps, URLs, output references, and summaries are in events.jsonl. Both search calls returned 18 displayed results. All 36 are logged in their displayed order, including results outside the requested site filter. No top-five rank was missing. The first query's rank 13 contained a long excerpt in its displayed title; that metadata was preserved.

The final candidate order is an assessment of usefulness, not a revised search ranking. The three returned links are all directly read official sources. Five separate official documentation pages were opened; different anchors were not counted as additional works.

## Choices and proposed tests

**R5-A-T1 — named, count-positioned handles.** Use a stable handle identity for each connection endpoint and derive endpoint positions from the incident-edge count. The equal-spacing formula in returns.json is this arm's proposal, supported by the guide's positioning and geometry-update mechanisms. The guide does not itself supply that formula. A three-to-four-edge transition distinguishes working dynamic spacing from several handles that remain centered. This tests endpoint separation only.

**R5-A-T2 — ELK uniform gaps and crowded-node policy.** The node-size reference distinguishes equalizing gaps affected by unequal labels from deciding what happens when a node is too small. A supporting layout configuration can compare uniform spacing and overhang options. The other opened ELK pages establish that ports and multiple edges are supported and that endpoint gaps differ from route gaps. Node layout may also change; acceptance of that behavior is not established by the request.

**R5-A-T3 — edge insertion before geometry.** Add a second edge with a different ID but identical endpoint and handle IDs, then compare with a valid different handle. The official utility note predicts duplicate suppression in the first case. This distinguishes missing data from overlapping paths and adds no claim of automatic route separation.

Every test above is **proposed only**. None was executed. Expected outputs are documentation-based predictions or explicitly identified design calculations, not observed software results.

## Unfilled requirements and limitations

The exact intended image, parallel-versus-fan-out interpretation, stable ordering policy, node resize behavior, removal behavior, installed library version, and required full-path clearance remain unknown. The ELK adapter code, port coordinate transfer into React Flow, and exact executable layout configuration were not investigated. No prototype, screenshot comparison, benchmark, regression test, or historical source checkout was produced.

Current documentation cannot establish what was available at the post's 2024 date. The handle guide reports an October 8, 2026 update; the remaining inspected pages lack a verified publication date or immutable edition. Q3-Q6 were named by the required source schema but not defined in the assignment; they are retained as labels without invented question meanings.

## Unintended exposure

The first query automatically exposed a different xyflow discussion, number 2692, with comments from November 2023 and later comments from June 2024 and April 2025. It mentioned overlapping floating edges, examples, and later suggestions. That thread was not opened or treated as verified evidence. The original request, number 3758, was never opened, and no exposure specifically identified as its comments, status, linked PR, release, or resolution was observed.

Other automatically exposed material included third-party tutorials, wrapper documentation, PDFs, videos, current ELK source snippets, and theses. Those were not opened. A thesis snippet mentioned a possible routing failure with equal port positions, but this was not promoted to a verified technical claim. Documentation navigation and embedded-image links were visible; those links and images were not followed.

## Budget and audit

Completed two query items and five explicit opens. There were no clicks, finds, reopens, failed internet opens, shell network calls, or GitHub API requests. One query slot and one open slot were intentionally left unused. Every network action records before/after UTC times and elapsed duration; concurrent events use invocation order. In-memory parsing and reading stored response text incurred no new retrievals.

Automatic engine reads, token usage, monetary cost, and exact immutable backend version are unknown, not zero. The inherited model's displayed parent label is GPT-6 Astra Pro. Raw third-party responses were kept only in transient functions store; no full pages were copied into these deliverables. There are no unfilled candidate ranks. No git commands or commits were performed.

