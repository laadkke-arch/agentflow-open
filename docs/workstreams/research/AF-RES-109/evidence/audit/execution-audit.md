# AF-RES-109 execution-log audit

Recorded UTC: **2026-11-24T02:29:03.232475Z**. Auditor: isolated `execution_audit` collaboration agent.

## Finding and coverage

All **12 arms / 6 pairs** were complete at this audit snapshot. The 30 individual queries, 52 explicit page actions, 33 final links and 3 explicit final vacancies reconcile internally. Every arm stays within **3 queries / 6 explicit opens / 3 final links**. All recorded input hashes match the corrected experimental-input digests, and every pair follows the assigned order with the first arm ending before the second starts.

One material chronology ambiguity affects common-consumption candidate identity: **R3-B** records concurrent opens in an index order that disagrees with their UTC start order. Both prefixes are preserved below. Later same-request material was automatically exposed in **R2-A** and **R6-B**. No source quality, historical availability, novelty, condition-fit, or success judgment is made here. This audit **does not establish a valid strict A/B comparison**.

The audit read only `SCOPE.md`, `requests.jsonl`, `baseline.csv`, `evidence/start/*`, and the four permitted files for each completed search arm. It performed no web retrieval, git operation, source-page adjudication, or raw-prompt read. Only `execution-audit.md` and `execution-audit.json` were written. Covered inputs were rehashed unchanged before writing.

## Counts and bookkeeping

| Arm | Queries | Explicit opens | Final links | Vacant final ranks | Failed actions | Repeat-work actions | Hash / counts / source refs |
| --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| R1-A | 2 | 4 | 2 | 3 | 1 | 0 | agree |
| R1-B | 3 | 3 | 2 | 3 | 0 | 0 | agree |
| R2-A | 3 | 3 | 3 | — | 0 | 0 | agree |
| R2-B | 3 | 6 | 3 | — | 0 | 3 | agree |
| R3-A | 2 | 2 | 2 | 3 | 0 | 0 | agree |
| R3-B | 2 | 4 | 3 | — | 0 | 1 | agree |
| R4-A | 3 | 6 | 3 | — | 0 | 3 | agree |
| R4-B | 2 | 6 | 3 | — | 0 | 3 | agree |
| R5-A | 2 | 5 | 3 | — | 0 | 0 | agree |
| R5-B | 3 | 4 | 3 | — | 1 | 0 | agree |
| R6-A | 3 | 3 | 3 | — | 0 | 0 | agree |
| R6-B | 2 | 6 | 3 | — | 1 | 2 | agree |

There are **523 logged search-result rows** across 30 queries. All top-five positions are either present once or explicitly vacant. The sole short result set is **R2-B event5**: rank1 present and ranks2–5 vacant. Result arrays keep their logged displayed-rank order, and required rank/title/URL/ref/seen-content fields are present. This establishes internal logging completeness; original engine renderings were not independently rechecked.

All 12 event-index sequences are contiguous from zero. Query/open UTC intervals and elapsed values agree to 1 ms. Overlapping intervals are retained as concurrent calls, not mislabeled as sequential execution failures. The only retrieval-start inversion is R3-B. Each of the 52 explicit actions has a matching source row/ref, including failures, clicks, finds and reopens. Final candidates plus vacancies account for all 36 prescribed slots.

## Observed pair order

| Pair | Assigned and observed order | First arm end UTC | Second arm start UTC | Gap seconds |
| --- | --- | --- | --- | ---: |
| R1 | A→B | 2026-11-24T01:53:57.962Z | 2026-11-24T01:57:33.978Z | 216.016000 |
| R2 | B→A | 2026-11-24T01:59:13.294Z | 2026-11-24T02:00:30.393540349Z | 77.099540 |
| R3 | A→B | 2026-11-24T01:57:26.388280Z | 2026-11-24T01:58:30.416321Z | 64.028041 |
| R4 | B→A | 2026-11-24T02:10:27.531Z | 2026-11-24T02:12:20.176Z | 112.645000 |
| R5 | A→B | 2026-11-24T02:12:05.900Z | 2026-11-24T02:13:41.684Z | 95.784000 |
| R6 | B→A | 2026-11-24T02:15:16.584Z | 2026-11-24T02:16:45.454Z | 88.870000 |

## Common-consumption prefixes

For each pair, set `q = min(qA, qB)` and `o = min(oA, oB)`. Traverse the ordered retrieval actions and stop **before the first action exceeding either cap**. Later actions are not cherry-picked back into the prefix. Query hits and initial navigation windows do not credit a final candidate whose substantive acquisition/read occurs later. “Eligible” below means only that its recorded acquisition is included; it is not a success judgment.

| Pair | Common q/o cap | A prefix: actions; consumed q/o | A eligible final ranks | B prefix: actions; consumed q/o | B eligible final ranks |
| --- | --- | --- | --- | --- | --- |
| R1 | 2/3 | 1, 2, 3, 4, 5; 2/3 | 1, 2 | 1, 2, 3, 4; 2/2 | 1, 2 |
| R2 | 3/3 | 1, 2, 3, 4, 5, 6; 3/3 | 1, 2, 3 | 1, 2, 3, 4, 5, 6; 3/3 | 1 |
| R3 | 2/2 | 1, 2, 3, 4; 2/2 | 1, 2 | 1, 2, 3, 4; 2/2 | index: 3; UTC: 1; identity indeterminate |
| R4 | 2/6 | 1, 2; 2/0 | none | 1, 2, 3, 4, 5, 6, 7, 8; 2/6 | 1, 2, 3 |
| R5 | 2/4 | 1, 2, 3, 4, 5, 6; 2/4 | 1, 3 | 1, 2; 2/0 | none |
| R6 | 2/3 | 1, 2, 3, 4; 2/2 | 1, 2 | 1, 2, 3, 4, 5; 2/3 | 2 |

First excluded actions are R1-A event6 (fourth open), R1-B event5 (third query), R2-B event7 (fourth open), R3-B event5 by index or event3 by UTC (third open), R4-A event3 (third query), R5-A event7 (fifth open), R5-B event3 (third query), R6-A event5 (third query), and R6-B event6 (fourth open). R2-A, R3-A and R4-B retain all retrieval actions.

### R3-B: identity remains indeterminate

| Event | Recorded start UTC | Role |
| ---: | --- | --- |
| 4 | 2026-11-24T02:00:14.109792Z | Vendure initial navigation window; substantive read requires event6 |
| 5 | 2026-11-24T02:00:14.113018Z | Auxx direct read; final candidate rank1 |
| 3 | 2026-11-24T02:00:14.119597Z | Node-RED credentials direct read; final candidate rank3 |

The index prefix is `[1,2,3,4]`, admitting final rank3. The UTC-start prefix is `[1,2,4,5]`, admitting final rank1. Each admits one candidate, but no individual B candidate is eligible under both recorded orders. Any common-consumption assessment of a specific new choice or test must therefore mark these two identities **indeterminate**, rather than choose whichever order favors a positive result. Rank2 remains excluded under both because its substantive read is event6. Original records are unchanged.

### Acquisition schemas checked

The audit recognizes scalar acquisition events and the different object keys for open/read/section events, including arrays of reads and supporting reads. It does not use the first integer found in an object. R2-B rank2 requires direct-read event7; its initial W3C open4 and duplicate click6 do not qualify it. R2-B rank3 requires read9. R6-B rank3 requires reads3 and6, so it is excluded even though its initial API open3 fits the cap. R4-A and R5-B reach their third query before any direct read and therefore have no eligible final links at the common prefix.

Concurrent actions are atomic counting units for this descriptive truncation. Exact UTC ties retain the logged event index. Responses may finish after other calls have already launched; these prefixes are not actual reduced-budget reruns, nor proof that a final proposal had already been formulated at the cutoff.

## Input hashes and unknown costs

All start-event and return digests agree with `requests.jsonl.experiment_input_sha256` for all 12 arms. Each legacy `full_input_sha256`, assignment digest and baseline digest agrees with the raw-source digest in the newline reconciliation. The reconciliation records CRLF/CR→LF normalization during prompt generation and no change to words, punctuation, values or conditions. The audit did not re-open out-of-scope raw bodies or prompts, so it verifies these ledger relationships rather than independently reconstructing raw-byte equivalence. Some arms independently rehashed their supplied input; others explicitly recorded the supplied hash. That distinction remains in the JSON.

| Request | Experimental input SHA-256 (both arms) |
| --- | --- |
| R1 | `8751afc5b5f681615cdc533f7489a93e79c017fa915de023d339fa1f4e505eae` |
| R2 | `5f983c942a9ccf4273bb3d3309ecc81617439d0ed0574dd32f183b3f3efcdf87` |
| R3 | `b73e0ba4608fe658b80c8f43f833fe824bfa87ce6d58c8c5c4cc3cd19d6ac98a` |
| R4 | `58e5a6870b870326fb391c173f025aba11d74708a0549ac8dfbfe32e1c09be1d` |
| R5 | `a3c757a2728256ddccc4dd823f8b297e1c5ba199a9937e4e23b01438c3a30c88` |
| R6 | `12887f1a139112b86eb8d21f2ecaab2e6ca4c7d61e71328fb06fb5bb037b0244` |

All arms record the inherited display label **GPT-6 Astra Pro**. Immutable backend identity/seed is unverified. Every acquisition action retains `automatic_reads: null` and `monetary_cost: null`; return records likewise mark token use, automatic reads, backend identity and money unknown. No null is converted to zero. The current opening-post edition, original-edition gap and engine-internal exposure gap remain outside what these logs can establish.

## Reopens, failures and limited reads

| Arm / event | Recorded operation or issue | Accounting |
| --- | --- | --- |
| R1-A / 6 | failed_disabled_error | one explicit-open slot; unique-primary flag false |
| R5-B / 6 | failure_http_404 | one explicit-open slot; unique-primary flag false |
| R6-B / 4 | failed_timeout | one explicit-open slot; unique-primary flag false |
| R2-B / 6,7,9 | W3C click/find and Function-source find | three repeat-work rows; all flags false |
| R3-B / 6 | Vendure substantive reopen after navigation-only first response | repeat-work row; flag false |
| R4-A / 7,8,9 | CSS section find and two package-code finds | three repeat-work rows; all flags false |
| R4-B / 6,7,8 | Same-document click, API reopen, CSS find | three repeat-work rows; all flags false |
| R6-B / 6,8 | API reopen and tree metadata for the already read code work | two repeat-work rows; all flags false |

The three failures are the R1-A disabled wiki fetch, R5-B HTTP404 hook click, and R6-B timed-out Chromium diff open. A successful envelope is not assumed to imply a successful page: the R5-B 404 remains a failure. The 12 repeat-work actions include one metadata click rather than a literal page reopen; no repeat row increases the within-arm unique-work flag count. Cross-arm lineage deduplication, source authenticity and whether an initial partial view is sufficient primary reading are reserved for source adjudication.

Redirect/canonicalization records are preserved, including R1-A translation-resolution→fallback, R2-B master→main, the R1-A failed wiki URL normalization, and the R4-A encoded package URL. No redirect is silently treated as a separately acquired primary work.

## Actual later-outcome exposure

| Observer | Recorded exposure | Consequence |
| --- | --- | --- |
| R2-A, query event1 rank2 | Same-title Node-RED forum later replies and a January2 report of recovery after a Node.js change; author uncertain about the cause | Outcome blindness contaminated; thread not explicitly opened or used as candidate evidence |
| R6-B, query event1 rank6 | Original issue3759 snippet containing later Windows Desktop/Wacom ctrlKey wheel and slow-zoom comment material | Same-issue follow-up exposure; no verified final resolution inferred; issue not explicitly opened |
| Root, before search, R4 | Start records acknowledge a later updateNode selected:false example while inspecting issue HTML | Root is not a clean R4 searcher/blinded reader; records say content was not passed to isolated arms |

No other same-request later-outcome exposure is identified in the permitted arm logs. This is bounded to recorded evidence, not proof of unseen cognitive or engine exposure absence. Unrelated discussions, later release/news snippets, current code/docs, translations and navigation exposures remain in each arm’s notes; they are not recast as the target request’s resolution. Removing an exposed thread from citations does not restore blindness.

## Other exact timing caveats

R6-B event11 is a whole-run stop interval whose `started_utc` equals the run start. Use its `ended_utc` when placing the stop summary; do not move it to the beginning of the acquisition chronology. This does not change any budget count.

returns.retrieval_end_utc is 2026-11-24T01:54:20.646116527Z; the final recorded retrieval is event4 ending 2026-11-24T01:53:57.135437577Z, a difference of 23.510679 seconds. The action rows determine acquisition timing; the later auxiliary field is not evidence of an extra open.

## Covered files and SHA-256

Snapshot read began 2026-11-24T02:29:03.192700Z and ended 2026-11-24T02:29:03.232475Z. All **60** files below were byte-hashed and confirmed unchanged before the outputs were written. Paths are relative to `docs/workstreams/research/AF-RES-109/`. The JSON companion contains per-event ranking checks, both prefix variants, candidate gates, exposure records, and the same inventory.

| Covered file | Bytes | SHA-256 |
| --- | ---: | --- |
| `SCOPE.md` | 9701 | `0846e992ee2ec76ea07d16fa6465a786b3b0916cf85492556c24880a92513dfc` |
| `requests.jsonl` | 9396 | `1fccc3acdf04647f014d38b0b5c015615bf98d1ed7672a350a5c5ea90e750e6f` |
| `baseline.csv` | 7769 | `adc646d34fe9ba1d8900b6ee286843fedb5ee643c539212a0c3e1196d280bdf4` |
| `evidence/start/assignment.json` | 1427 | `3d211d67b0aa754e4e3ebe0b9f566452230914ba07f56c4829aef6d245fed5d2` |
| `evidence/start/baseline-representation-addition.json` | 922 | `868107c0ed15f31cc64655270ba192e4f1e88a8aeb947f93af6c8b9ea989684d` |
| `evidence/start/contract-read.json` | 14359 | `11eb6bfd7a9f2ff5fd0bd84054ca3502ed7be9a2c85ef2935cbebb0854a17102` |
| `evidence/start/frame-query-receipt.json` | 1177 | `f548362c5660ffc2633429a2d16358b8222c1cbb88ce90c9b580395bde075bde` |
| `evidence/start/inherited-reconciliation.json` | 914 | `b8b4de7da78c0d01c923b1416d62ffb7d71ddb65979152dec8a144670a3ce13d` |
| `evidence/start/input-newline-reconciliation.json` | 3532 | `74fabb966831d4006670487dd4cfb8dc517b5e95ca4a6c70a71f82cf65853700` |
| `evidence/start/prompt-fingerprints.json` | 3667 | `f1ed093b0384781f2deeda0e1ad17919a6daacf66f0e2880035de075fbdc8c70` |
| `evidence/start/recruitment-review.md` | 6526 | `0f63fb6ff38e9a3bfbc906edd4d6d1c6f03d1efeabb28a27631237820383f209` |
| `evidence/start/search-instructions.md` | 5705 | `83541efe4bf7dc4970199b1343c5d815e1801d3a23dcb0f039f403f6b1ab3c9e` |
| `evidence/search/R1-A/events.jsonl` | 18547 | `d69a3f4a818fc2b411b9cbd3beff8d3e70c390c97168a9c06dbe64f173168966` |
| `evidence/search/R1-A/returns.json` | 8380 | `9f4bb40f765cc982ff2f8fefc763fb32ac035fbb091abf3da2d6172dafb353e7` |
| `evidence/search/R1-A/sources.jsonl` | 7039 | `ce788607aadeeab72b5777ef1b8fdb295c352b803ed9f2a2c1a55f9ce6fa2051` |
| `evidence/search/R1-A/notes.md` | 5642 | `3e1fde9142d49843457bd41b4c246af67cc9b205ad06a55b5685f09e4eabcb3e` |
| `evidence/search/R1-B/events.jsonl` | 30219 | `af63176d48674e64c0c75d55233814e06895dd8cfec8f31a1abfcac41598247a` |
| `evidence/search/R1-B/returns.json` | 6056 | `3a48f9c66105287f6e3b6279059e58f947cafecbdc06e270a478d2e4ca7d43af` |
| `evidence/search/R1-B/sources.jsonl` | 5024 | `ba928739afa2e7df5bfcdb0c421ec9f248d4f43907d383da3ae753b21085b135` |
| `evidence/search/R1-B/notes.md` | 5434 | `9156db584a0421e861d21c3aa33097c43c1155d00a6c5bae031989dc14a087bd` |
| `evidence/search/R2-A/events.jsonl` | 23765 | `38f147a902321d82b521dae9493b05988e4e346d392a0360d5efec1538c1bbca` |
| `evidence/search/R2-A/returns.json` | 8695 | `cec3519ad2c0cb31f1a9645cad08293d031878eaa8cf4f1fe2fef8c12f192f6b` |
| `evidence/search/R2-A/sources.jsonl` | 7551 | `02b07490b1e52c4e06bd5a5e35742b781109ad7dd9b71e294293dde0a39fd17e` |
| `evidence/search/R2-A/notes.md` | 6549 | `364543b88434ca4150b63d01ae65210785c50ddc0909cdeb5c463d2625237d81` |
| `evidence/search/R2-B/events.jsonl` | 30315 | `83209f88f736ba453175ba25556049bdc6fcd27210d668a44188a846954c5613` |
| `evidence/search/R2-B/returns.json` | 9934 | `7f33a1a75d32c65da9dd84947b0bdc3be95f88788bbbbc220344c7d7932d54a2` |
| `evidence/search/R2-B/sources.jsonl` | 8673 | `3591e996fcaa7ea00ccc43fd2249bfe6766336339d6008c5998a98472ec64680` |
| `evidence/search/R2-B/notes.md` | 7644 | `66feecf31f05152d4c7223f52ba814aa0d6f22c3229a5e46d2e269b5c8d229a9` |
| `evidence/search/R3-A/events.jsonl` | 14128 | `89d090bb76ff0e4590dc01382a1190f97e94720768a65f4baef41a5c419c0867` |
| `evidence/search/R3-A/returns.json` | 8925 | `10b201a6b92a36342e8ecfbcbb42793dfc069fab3100b0fdfc2552b1294930f8` |
| `evidence/search/R3-A/sources.jsonl` | 3402 | `c3066ada5f1ece59dfcbcbe04c7124c88a36618ebd1b50bd8fa306db083dd91e` |
| `evidence/search/R3-A/notes.md` | 5635 | `d770de0f73d89ded6e1bbfe895e3a2f46e7500e7a8255180661accf01f3ff216` |
| `evidence/search/R3-B/events.jsonl` | 24414 | `34ee4db8faea13b1b690c6e26e86b87967c7c56fe06b0c7bd897d61849324ab7` |
| `evidence/search/R3-B/returns.json` | 8029 | `bc0debb4044b1a2221b27f66b4a8522ef4bd179c2ad96ee101f3a51951f9187b` |
| `evidence/search/R3-B/sources.jsonl` | 6896 | `5ba86598a408140ff2e790621676fdd4485cdc68f0b467326760b7969089ffec` |
| `evidence/search/R3-B/notes.md` | 5433 | `4d644a11f881fc377fbfcda2b202715d1fd7f42a8518e6c65e0f9a57366b6498` |
| `evidence/search/R4-A/events.jsonl` | 30606 | `25bfc091b8c24254e6e14a96c8dd19fc13f277dc27307105e6777a276886e1c5` |
| `evidence/search/R4-A/returns.json` | 8269 | `d5666cd099f9a369b76d5ea613cc056d96fc6d99a8539f6f55e7ba12cf2c7c3b` |
| `evidence/search/R4-A/sources.jsonl` | 9285 | `681424b95b544bf161f176129f6f19b141bcd84e0cd1e5f1686487397eeb7f66` |
| `evidence/search/R4-A/notes.md` | 6981 | `aa99991b5d68708e4d0ede9f608ba42e044e8b96bbc3f02774856c5d094de9b8` |
| `evidence/search/R4-B/events.jsonl` | 20474 | `3ce7f322b0fe57fe1035ca776e86dc85f950d78d6efc24c598fb53d0a52ba87d` |
| `evidence/search/R4-B/returns.json` | 10512 | `de7820351a359034009da587932e23a5a6774f965a3d17fca62d875cae7df8db` |
| `evidence/search/R4-B/sources.jsonl` | 9877 | `e0f6ddb72d71f3a7dfb06e26ca3039ce004156fa5d1e2312214a1681b2441cd4` |
| `evidence/search/R4-B/notes.md` | 5808 | `7e9dcf9a5135a4a4b0fb49b02fd420cad2b1f6debe25b5aa3e32df3e4bcdacb9` |
| `evidence/search/R5-A/events.jsonl` | 22357 | `8f64cfbf754282da3ec4461edf01f408390a646a2cd5580ebb637516ec9e9875` |
| `evidence/search/R5-A/returns.json` | 9386 | `4fc33e4f77e15c40a845a59ae8738ff0c13706428d16808ef9c1cfff5e5706c9` |
| `evidence/search/R5-A/sources.jsonl` | 6675 | `45ea9744fb8ccb24a97aa4dd33e346b98de43f4697826ffecda3f700ee6fb5b2` |
| `evidence/search/R5-A/notes.md` | 6253 | `1349502fdf29c2c1d5450e054601bd6033846e20101bfcfa84485e8c47785772` |
| `evidence/search/R5-B/events.jsonl` | 34744 | `228c3e19469d0b45e4dddb946f3e37b29d22f627a9b8c955a0f1cbc58a73385d` |
| `evidence/search/R5-B/returns.json` | 8665 | `eabfad5fac7920c797c9276e482c53e36ba39e8249d9b44f4ef9ed20da27249c` |
| `evidence/search/R5-B/sources.jsonl` | 7710 | `571648e022f4a8039793caf9393c8c246fcc59cd376c216a8fac485b6399ada4` |
| `evidence/search/R5-B/notes.md` | 8026 | `5380f292a4a3d545beca0e65dd96f6d134e0bf2bf6deea33d9e783ba69ec0079` |
| `evidence/search/R6-A/events.jsonl` | 25181 | `548e0d29ab94bdda0958efc62ada54a603639dac91e3431d918f3a9c5185ca6c` |
| `evidence/search/R6-A/returns.json` | 8820 | `45702d462f2ed590680169ab12c0a99091b7f0b4121a34e45aebeb7e45e71392` |
| `evidence/search/R6-A/sources.jsonl` | 7178 | `8a4b574178bcec9d75ca34fbe655680f2569b502412deff391947c797305d097` |
| `evidence/search/R6-A/notes.md` | 5936 | `4adf285b369d23c48d3e79b3e299838ecb5c60b979e367459adab54ac1cc43da` |
| `evidence/search/R6-B/events.jsonl` | 27672 | `03c662218ff9b6ae48c81edd08e7e4b5d18fb35b5de97ec389d872647d3c6695` |
| `evidence/search/R6-B/returns.json` | 13041 | `9b75f64cd71f90a617c1070d474e81f76ec19e6afac65ccbe7208730a6f3b0dd` |
| `evidence/search/R6-B/sources.jsonl` | 9127 | `d9661d31349436f9507c9bf50ca08522c4e8daf54c0c15f3a4d861e548a0c3b7` |
| `evidence/search/R6-B/notes.md` | 5610 | `74c2414b359dbaba4acdb9c1dc6e35da661fa2c06d53732348201c98841e61d9` |

## Audit limit

Internal execution bookkeeping is reconciled except for the stated timing ambiguity and ancillary timing/schema caveats. The audit supplies no strict-comparison winner, no causal claim, and no independent source adjudication. Original-edition, immutable-model, automatic-read and contamination limitations remain in force.
