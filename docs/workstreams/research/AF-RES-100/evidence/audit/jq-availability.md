# AF-RES-100: J1–J4 pre-outcome evidence availability audit

## Result

All 16 packet decisions retain their initial completeness and condition statuses. Six packets establish every frozen condition: A/F and B/F for J1, J2 and J4. All eight S packets remain incomplete after every exact fixed window was displayed. J3 A/F and B/F establish C1 but leave C2 partial; their failure classification is **unclear**, because the bounded full-file audit did not find the necessary shell-boundary proof and does not claim an exhaustive read of all four files. There are **zero `missed_but_available` completeness flips**.

| Case | Packet | Route | Initial complete | Availability complete | Conditions | Classification |
|---|---|---|---|---|---|---|
| J1 | cc86f215a28e | A/F | true | true | C1 supported | confirmed_available |
| J1 | 28483f232965 | A/S | false | false | C1 unknown | evidence_absent_in_permitted_window |
| J1 | 2f20d4696820 | B/F | true | true | C1 supported | confirmed_available |
| J1 | 90c5d90f8abc | B/S | false | false | C1 unknown | evidence_absent_in_permitted_window |
| J2 | b6aad97ea044 | A/F | true | true | C1 supported; C2 supported | confirmed_available |
| J2 | 3ea1130ebcab | A/S | false | false | C1 partial; C2 partial | evidence_absent_in_permitted_window |
| J2 | 14f044b30814 | B/F | true | true | C1 supported; C2 supported | confirmed_available |
| J2 | 2d1378170a3d | B/S | false | false | C1 partial; C2 partial | evidence_absent_in_permitted_window |
| J3 | a13997d37fef | A/F | false | false | C1 supported; C2 partial | unclear |
| J3 | 8591724781d4 | A/S | false | false | C1 unknown; C2 unknown | evidence_absent_in_permitted_window |
| J3 | 0be2a4830a4c | B/F | false | false | C1 supported; C2 partial | unclear |
| J3 | a76ec0d77f82 | B/S | false | false | C1 unknown; C2 unknown | evidence_absent_in_permitted_window |
| J4 | a0007d0fb17a | A/F | true | true | C1 supported; C2 supported | confirmed_available |
| J4 | d018c8051020 | A/S | false | false | C1 unknown; C2 unknown | evidence_absent_in_permitted_window |
| J4 | 837da1ed6706 | B/F | true | true | C1 supported; C2 supported | confirmed_available |
| J4 | a032f9aa185e | B/S | false | false | C1 partial; C2 unknown | evidence_absent_in_permitted_window |

## Scope and independence

This is a separate **machine availability audit**, not a human review or an independent initial discovery measurement. It was allowed to see A/B routes and all four initial judgments for each case. It read the preserved first-revision requests and the frozen protocol, then used only `audit_availability.py` to display registered source text. It fetched no external material, read no answers/comments/current question pages, ran no original-user or synthetic solution commands, and sent no judgments to active readers. Original-user runtime success remains unknown.

The protocol/packet seal supplied for this audit is `e0cb8eaec3cbd9a7e5d40291a5a883f33473ec2f`. Initial judgments stay in `evidence/readers/R1..R4/judgments.jsonl`; audit decisions do not overwrite them. Audit display receipts are separate in `evidence/audit/availability-access.jsonl`. The initial reader access wrapper and budget logs were not used or changed by this auditor.

For S, the four original 1200-codepoint intervals were read exactly, totaling 4800 codepoints per packet, without navigation. For F, positive conclusions use packet-contained constructive proof; the J3 negative conclusion is bounded by the targeted navigation described below. The same source file appearing in another case or route never widens a packet boundary.

`confirmed_available` means the initial supported result was corroborated. `evidence_absent_in_permitted_window` means the complete fixed S windows do not contain sufficient proof. `unclear` means a full-file packet remained unproved after bounded searching; it does not assert universal absence. `audit_added: true` on every citation identifies the separate audit record and display receipt; it does not mean that the original reader missed that fact.

## Counterexample checks

**J3 main manual and shell boundary.** The manual does contain Unix-shell quoting advice for the jq program, `--argjson`, and `@sh`. None of those displayed passages establishes the Bash expansion of `json_content` and `json_file` as the needed arguments and variable output target. A additionally contains the exact `argv[i+2]` JSON parser boundary. B adds a Terminal proposal's literal `> foo.txt` redirection discussion and JSON quoting warning. These are partial context, not a supported correction of the frozen variable-based automation. Substituting Bash documentation, a literal-only call, or a slurpfile-only alternative would change the boundary or requirement. C1 stays supported; C2 stays partial.

Targeted F searches used `Bash|quot|word spl|redirect|shell|argjson` in the manual (`context=160`, `limit=80`); `bash|word.?spl|parameter.expansion|double.quot|single.quot|redirect|argjson|shell` in the other files (`context=120`, `limit=30`; main.c used `context=220`); and `quot|expan|variable` in the Terminal snippets proposal (`context=180`, `limit=30`). Candidate results and the positive append/assignment passages were displayed. No whole-file exhaustive absence claim follows from these searches.

**J4 AWS evidence.** The complete AWS example file demonstrates all four sibling fields and later shows `--query "Volumes[*].{ID:VolumeId,Tag:Tags}"`, preserving each volume's ID and Tags together. It is useful corroboration, but does not by itself select `Value` where `Key=VolName`. The contained jq manual already establishes the full transformation in A/F and B/F. B/S permits only `[0,1200)`, which ends before Size in the first example and before all Tags/query material; the full-file counterexample cannot be credited to B/S.

**Original input limitations.** J1 asks for a next debugging action, so the absent full two-file data do not invalidate the documented procedure; a unique cause or final successful JOIN remains unproved. J2 permits missing content to remain null and requires the event path to be qualified because the full envelope is absent. J4 permits absent Iops to remain null and fixes the tag key as VolName. No numeric Iops, TRUE semantics, or corrected original runtime output was synthesized.

## Per-packet findings and exact audit citations

All ranges below are zero-based half-open Unicode codepoint and UTF-8 byte intervals in the frozen raw source. Every listed citation has `audit_added: true`; the JSONL contains source/segment hashes and the exact audit access timestamp. Sources displayed only as limiting context are labeled accordingly.

### J1 A/F — cc86f215a28e

Initial: **true** (R1); availability: **true**; classification: `confirmed_available`. No condition-status or completeness change.

**C1 — supported.** The contained manual and builtin definitions support inserting debug into the original input stage and before JOIN's add stage, while retaining the value passed onward. Filename/line observers can identify the last consumed input. This is sufficient for the frozen next-diagnostic-action requirement; full original data are not needed to establish documentary availability.

Documentary construction (not executed):

`For a diagnostic step, replace the original JOIN fourth argument add with (debug | add), and instrument the original input subexpression with value-preserving debug/filename-line probes. Compare the displayed INDEX overloads. This proposes observations, not a unique cause or a repaired final JOIN.`

The primary requirement is a documented next diagnostic action. A unique original cause, successful final JOIN, and actual runtime trace remain unknown.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| cc86f215a28e / 1 / JQ-0001 | [123208,125480) | [123210,125482) | [input; inputs; debug; input_filename; input_line_number](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Value-preserving diagnostic filters, explicit input consumption and filename/line observers. |
| cc86f215a28e / 3 / JQ-0004 | [10173,10903) | [10173,10903) | [debug(msgs); INDEX and JOIN implementations](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.jq) — JOIN passes its pair to join_expr and exposes INDEX/stream stages suitable for probes. |
| cc86f215a28e / 4 / JQ-0002 | [38482,39160) | [38482,39160) | [f_input and f_debug](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.c) — Confirms unchanged debug value and break as an input-failure possibility; does not diagnose the original run. |

### J1 A/S — 28483f232965

Initial: **false** (R2); availability: **false**; classification: `evidence_absent_in_permitted_window`. No condition-status or completeness change.

**C1 — unknown.** All four exact 1200-codepoint windows were inspected. They contain generic filter composition, literal/encoding tests, opening builtin helpers and C type-error formatting. The error(msg) wrapper and generic composition do not document a concrete observation of JOIN/INDEX intermediate values or input consumption. No applicable probe or stage semantics is established inside these windows.

Every permitted source window was displayed in full; no S navigation or broadening was used. Total permitted and uniquely audited source text is 4800 codepoints.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| 28483f232965 / 1 / JQ-0001 | [0,1200) | [0,1200) | [Complete permitted manual excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Full fixed window inspected; only this window may contribute to this packet. |
| 28483f232965 / 2 / JQ-0080 | [0,1200) | [0,1203) | [Complete permitted jq tests excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/tests/jq.test) — Full fixed window inspected; only this window may contribute to this packet. |
| 28483f232965 / 3 / JQ-0004 | [0,1200) | [0,1200) | [Complete permitted builtin definitions excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.jq) — Full fixed window inspected; only this window may contribute to this packet. |
| 28483f232965 / 4 / JQ-0002 | [765,1965) | [765,1965) | [Complete permitted builtin C excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.c) — Full fixed window inspected; only this window may contribute to this packet. |

### J1 B/F — 2f20d4696820

Initial: **true** (R3); availability: **true**; classification: `confirmed_available`. No condition-status or completeness change.

**C1 — supported.** The contained manual and builtin definitions support inserting debug into the original input stage and before JOIN's add stage, while retaining the value passed onward. Filename/line observers can identify the last consumed input. This is sufficient for the frozen next-diagnostic-action requirement; full original data are not needed to establish documentary availability.

Documentary construction (not executed):

`For a diagnostic step, replace the original JOIN fourth argument add with (debug | add), and instrument the original input subexpression with value-preserving debug/filename-line probes. Compare the displayed INDEX overloads. This proposes observations, not a unique cause or a repaired final JOIN.`

The primary requirement is a documented next diagnostic action. A unique original cause, successful final JOIN, and actual runtime trace remain unknown.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| 2f20d4696820 / 1 / JQ-0001 | [123208,125480) | [123210,125482) | [input; inputs; debug; input_filename; input_line_number](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Value-preserving diagnostic filters, explicit input consumption and filename/line observers. |
| 2f20d4696820 / 3 / JQ-0004 | [10173,10903) | [10173,10903) | [debug(msgs); INDEX and JOIN implementations](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.jq) — JOIN passes its pair to join_expr and exposes INDEX/stream stages suitable for probes. |
| 2f20d4696820 / 4 / JQ-0002 | [38482,39160) | [38482,39160) | [f_input and f_debug](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.c) — Confirms unchanged debug value and break as an input-failure possibility; does not diagnose the original run. |

### J1 B/S — 90c5d90f8abc

Initial: **false** (R4); availability: **false**; classification: `evidence_absent_in_permitted_window`. No condition-status or completeness change.

**C1 — unknown.** All four exact 1200-codepoint windows were inspected. They contain generic filter composition, literal/encoding tests, opening builtin helpers and C type-error formatting. The error(msg) wrapper and generic composition do not document a concrete observation of JOIN/INDEX intermediate values or input consumption. No applicable probe or stage semantics is established inside these windows.

Every permitted source window was displayed in full; no S navigation or broadening was used. Total permitted and uniquely audited source text is 4800 codepoints.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| 90c5d90f8abc / 1 / JQ-0001 | [0,1200) | [0,1200) | [Complete permitted manual excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Full fixed window inspected; only this window may contribute to this packet. |
| 90c5d90f8abc / 2 / JQ-0080 | [0,1200) | [0,1203) | [Complete permitted jq tests excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/tests/jq.test) — Full fixed window inspected; only this window may contribute to this packet. |
| 90c5d90f8abc / 3 / JQ-0004 | [0,1200) | [0,1200) | [Complete permitted builtin definitions excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.jq) — Full fixed window inspected; only this window may contribute to this packet. |
| 90c5d90f8abc / 4 / JQ-0002 | [765,1965) | [765,1965) | [Complete permitted builtin C excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.c) — Full fixed window inspected; only this window may contribute to this packet. |

### J2 A/F — b6aad97ea044

Initial: **true** (R4); availability: **true**; classification: `confirmed_available`. No condition-status or completeness change.

**C1 — supported.** Iteration, map, object construction, from_entries and update-assignment jointly establish a separate Name-to-content object for each EventData.Data array. The frozen original .Event[] envelope can be used conditionally; an individual-event input uses the corresponding shorter path.

**C2 — supported.** A missing .content lookup yields the ordinary JSON value null. Supplying it as value in each key/value object allows the documented from_entries conversion to retain null without inventing TRUE or failing because that specific member is absent.

Documentary construction (not executed):

`.Event[].EventData.Data |= (map({key: .Name, value: .content}) | from_entries), conditional on the reported envelope; for individual-event input use .EventData.Data |= (map({key: .Name, value: .content}) | from_entries).`

The original complete outer envelope, raw logs/XML, actual tool versions and runtime outcome remain unknown. TRUE semantics for missing content are not established or required by the frozen primary interpretation.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| b6aad97ea044 / 1 / JQ-0001 | [20022,23700) | [20022,23700) | [Iteration; pipe; parentheses](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Iterates each Event independently and scopes downstream expressions to the current input. |
| b6aad97ea044 / 1 / JQ-0001 | [26075,28900) | [26075,28900) | [Object construction](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — key and value expressions receive the same current Data element. |
| b6aad97ea044 / 1 / JQ-0001 | [37458,38500) | [37458,38500) | [map(f)](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Applies a filter to every array element and collects results. |
| b6aad97ea044 / 1 / JQ-0001 | [43318,44651) | [43318,44651) | [to_entries; from_entries](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Converts a key/value array to an object without requiring the values to be strings. |
| b6aad97ea044 / 1 / JQ-0001 | [129714,131089) | [129716,131091) | [Update assignment](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Applies the RHS to the old value at every selected path. |
| b6aad97ea044 / 1 / JQ-0001 | [16161,17376) | [16161,17376) | [Object identifier-index](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Missing object member returns null; dotted paths compose lookups. |

### J2 A/S — 3ea1130ebcab

Initial: **false** (R1); availability: **false**; classification: `evidence_absent_in_permitted_window`. No condition-status or completeness change.

**C1 — partial.** The manual synopsis and tests support field lookup, array iteration and a map/add example. They do not supply computed Name-to-value object construction, key/value conversion, or an event-scoped update that establishes the complete transformation. The failed original expression is a requirement/attempt, not proof of a working replacement.

**C2 — partial.** The .foo and .foo? missing-key examples yield null, supporting an explicit null policy without inferring TRUE. The same exact packet lacks the complete Name-to-value transformation; it therefore does not establish whole-transformation handling of missing content.

Every permitted source window was displayed in full; no S navigation or broadening was used. Total permitted and uniquely audited source text is 4800 codepoints.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| 3ea1130ebcab / 1 / JQ-0001 | [1268,2468) | [1268,2468) | [Complete permitted manual excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Full fixed window inspected; only this window may contribute to this packet. |
| 3ea1130ebcab / 2 / JQ-0090 | [66,1266) | [66,1266) | [Complete permitted manual tests excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/tests/man.test) — Full fixed window inspected; only this window may contribute to this packet. |
| 3ea1130ebcab / 3 / JQ-0075 | [809,2009) | [809,2009) | [Complete permitted util.c excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/util.c) — Full fixed window inspected; only this window may contribute to this packet. |
| 3ea1130ebcab / 4 / JQ-0080 | [0,1200) | [0,1203) | [Complete permitted jq tests excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/tests/jq.test) — Full fixed window inspected; only this window may contribute to this packet. |

### J2 B/F — 14f044b30814

Initial: **true** (R2); availability: **true**; classification: `confirmed_available`. No condition-status or completeness change.

**C1 — supported.** Iteration, map, object construction, from_entries and update-assignment jointly establish a separate Name-to-content object for each EventData.Data array. The frozen original .Event[] envelope can be used conditionally; an individual-event input uses the corresponding shorter path.

**C2 — supported.** A missing .content lookup yields the ordinary JSON value null. Supplying it as value in each key/value object allows the documented from_entries conversion to retain null without inventing TRUE or failing because that specific member is absent.

Documentary construction (not executed):

`.Event[].EventData.Data |= (map({key: .Name, value: .content}) | from_entries), conditional on the reported envelope; for individual-event input use .EventData.Data |= (map({key: .Name, value: .content}) | from_entries).`

The original complete outer envelope, raw logs/XML, actual tool versions and runtime outcome remain unknown. TRUE semantics for missing content are not established or required by the frozen primary interpretation.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| 14f044b30814 / 1 / JQ-0001 | [20022,23700) | [20022,23700) | [Iteration; pipe; parentheses](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Iterates each Event independently and scopes downstream expressions to the current input. |
| 14f044b30814 / 1 / JQ-0001 | [26075,28900) | [26075,28900) | [Object construction](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — key and value expressions receive the same current Data element. |
| 14f044b30814 / 1 / JQ-0001 | [37458,38500) | [37458,38500) | [map(f)](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Applies a filter to every array element and collects results. |
| 14f044b30814 / 1 / JQ-0001 | [43318,44651) | [43318,44651) | [to_entries; from_entries](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Converts a key/value array to an object without requiring the values to be strings. |
| 14f044b30814 / 1 / JQ-0001 | [129714,131089) | [129716,131091) | [Update assignment](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Applies the RHS to the old value at every selected path. |
| 14f044b30814 / 1 / JQ-0001 | [16161,17376) | [16161,17376) | [Object identifier-index](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Missing object member returns null; dotted paths compose lookups. |

### J2 B/S — 2d1378170a3d

Initial: **false** (R3); availability: **false**; classification: `evidence_absent_in_permitted_window`. No condition-status or completeness change.

**C1 — partial.** The manual synopsis and tests support field lookup, array iteration and a map/add example. They do not supply computed Name-to-value object construction, key/value conversion, or an event-scoped update that establishes the complete transformation. The failed original expression is a requirement/attempt, not proof of a working replacement.

**C2 — partial.** The .foo and .foo? missing-key examples yield null, supporting an explicit null policy without inferring TRUE. The same exact packet lacks the complete Name-to-value transformation; it therefore does not establish whole-transformation handling of missing content.

Every permitted source window was displayed in full; no S navigation or broadening was used. Total permitted and uniquely audited source text is 4800 codepoints.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| 2d1378170a3d / 1 / JQ-0001 | [1268,2468) | [1268,2468) | [Complete permitted manual excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Full fixed window inspected; only this window may contribute to this packet. |
| 2d1378170a3d / 2 / JQ-0090 | [66,1266) | [66,1266) | [Complete permitted manual tests excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/tests/man.test) — Full fixed window inspected; only this window may contribute to this packet. |
| 2d1378170a3d / 3 / SED-0001 | [185,1385) | [185,1385) | [Complete permitted sed manual excerpt](https://git.savannah.gnu.org/cgit/sed.git/tree/doc/sed.texi?h=v4.9) — Full fixed window inspected; only this window may contribute to this packet. |
| 2d1378170a3d / 4 / SED-0022 | [0,1200) | [0,1200) | [Complete permitted sed tests excerpt](https://git.savannah.gnu.org/cgit/sed.git/tree/testsuite/bsd.sh?h=v4.9) — Full fixed window inspected; only this window may contribute to this packet. |

### J3 A/F — a13997d37fef

Initial: **false** (R3); availability: **false**; classification: `unclear`. No condition-status or completeness change.

**C1 — supported.** The manual establishes .schemes += [$content] with a parsed JSON-valued $content: one object is wrapped in an array, concatenated with the existing array and assigned only to the schemes path. Other settings and pre-existing schemes are preserved by those documented operations.

**C2 — partial.** The contained material establishes the jq-program quoting convention and the --argjson JSON-text boundary. Targeted searches of all four permitted full files did not locate the Bash parameter expansion, word splitting, quoted variable/filename, and .new-target rules required to justify the original automation. The @sh output encoder and, for B, a literal-redirection example do not establish the missing variable boundary. A complete corrected script would require uncited shell knowledge.

Documentary construction (not executed):

`The jq-only expression .schemes += [$content] is supported with --argjson; no fully evidenced variable-based Bash script is claimed.`

F permits navigation within four complete files. This audit searched relevant terms and inspected candidate passages, rather than reading every byte of all implementation/proposal files; it therefore does not claim exhaustive universal absence. No positive proof of C2 was found, so complete remains false.

Counterexample check retained: main-manual shell quoting and @sh do not document double-quoted Bash parameter expansion. The adjacent tool stays Windows Terminal as frozen; substituting Bash documentation or slurpfile-only/literal-only automation would relax the requirement.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| a13997d37fef / 1 / JQ-0001 | [9665,10140) | [9665,10140) | [--argjson](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Parses JSON text into a jq variable, rather than supplying a string. |
| a13997d37fef / 1 / JQ-0001 | [24719,25050) | [24719,25050) | [Array construction](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Wraps the supplied JSON value as one array element. |
| a13997d37fef / 1 / JQ-0001 | [30647,31200) | [30647,31200) | [Addition](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Array addition concatenates arrays, preserving existing elements. |
| a13997d37fef / 1 / JQ-0001 | [127474,131776) | [127476,131778) | [Assignment; update assignment; arithmetic update assignment](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Changes only selected paths and defines += as the corresponding update with addition. |
| a13997d37fef / 1 / JQ-0001 | [3335,4651) | [3335,4651) | [Invoking jq: Unix-shell filter quoting](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Recommends quoting the jq program; does not document expansion of json_content or json_file. |
| a13997d37fef / 1 / JQ-0001 | [77123,77448) | [77125,77450) | [@sh](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Describes escaped POSIX-shell command text, not the Bash variable-expansion and output-target rules needed here. |
| a13997d37fef / 3 / JQ-0070 | [17874,18724) | [17874,18724) | [main.c --argjson processing](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/main.c) — Parses exactly argv[i+2] as JSON text; does not explain how Bash constructs that argv item. |
| a13997d37fef / 4 / JQ-0072 | [14948,15287) | [14948,15287) | [Parser diagnostics](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/parser.c) — The shell-quoting error hint is not a rule for repairing Bash variable expansion. |

### J3 A/S — 8591724781d4

Initial: **false** (R4); availability: **false**; classification: `evidence_absent_in_permitted_window`. No condition-status or completeness change.

**C1 — unknown.** The manual window describes generic composition; the decimal-library window is declarations and includes. The other windows are CLI/parser preambles (A) or schema/proposal introductions (B). No window establishes append by array concatenation, update assignment, or preservation of other settings. The original literal-command success report does not supply the missing packet evidence for the variable-based operation.

**C2 — unknown.** No permitted window documents --argjson, Bash parameter/command expansion, preserving JSON text as one argv item, or the variable .new output filename. The original missing closing quote and unquoted expansion are observations, not an evidenced correction.

Every permitted source window was displayed in full; no S navigation or broadening was used. Total permitted and uniquely audited source text is 4800 codepoints.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| 8591724781d4 / 1 / JQ-0001 | [309,1509) | [309,1509) | [Complete permitted manual excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Full fixed window inspected; only this window may contribute to this packet. |
| 8591724781d4 / 2 / JQ-0016 | [11388,12588) | [11388,12588) | [Complete permitted decimal library excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/decNumber/decNumber.c) — Full fixed window inspected; only this window may contribute to this packet. |
| 8591724781d4 / 3 / JQ-0070 | [30,1230) | [30,1230) | [Complete permitted main.c excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/main.c) — Full fixed window inspected; only this window may contribute to this packet. |
| 8591724781d4 / 4 / JQ-0072 | [1797,2997) | [1797,2997) | [Complete permitted parser.c excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/parser.c) — Full fixed window inspected; only this window may contribute to this packet. |

### J3 B/F — 0be2a4830a4c

Initial: **false** (R1); availability: **false**; classification: `unclear`. No condition-status or completeness change.

**C1 — supported.** The manual establishes .schemes += [$content] with a parsed JSON-valued $content: one object is wrapped in an array, concatenated with the existing array and assigned only to the schemes path. Other settings and pre-existing schemes are preserved by those documented operations.

**C2 — partial.** The contained material establishes the jq-program quoting convention and the --argjson JSON-text boundary. Targeted searches of all four permitted full files did not locate the Bash parameter expansion, word splitting, quoted variable/filename, and .new-target rules required to justify the original automation. The @sh output encoder and, for B, a literal-redirection example do not establish the missing variable boundary. A complete corrected script would require uncited shell knowledge.

Documentary construction (not executed):

`The jq-only expression .schemes += [$content] is supported with --argjson; no fully evidenced variable-based Bash script is claimed.`

F permits navigation within four complete files. This audit searched relevant terms and inspected candidate passages, rather than reading every byte of all implementation/proposal files; it therefore does not claim exhaustive universal absence. No positive proof of C2 was found, so complete remains false.

Counterexample check retained: main-manual shell quoting and @sh do not document double-quoted Bash parameter expansion. The adjacent tool stays Windows Terminal as frozen; substituting Bash documentation or slurpfile-only/literal-only automation would relax the requirement.

Additional audit-only partial context: the Terminal snippets proposal explains > redirection for a literal foo.txt. It still does not establish the required variable argv/filename behavior; C2 stays partial.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| 0be2a4830a4c / 1 / JQ-0001 | [9665,10140) | [9665,10140) | [--argjson](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Parses JSON text into a jq variable, rather than supplying a string. |
| 0be2a4830a4c / 1 / JQ-0001 | [24719,25050) | [24719,25050) | [Array construction](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Wraps the supplied JSON value as one array element. |
| 0be2a4830a4c / 1 / JQ-0001 | [30647,31200) | [30647,31200) | [Addition](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Array addition concatenates arrays, preserving existing elements. |
| 0be2a4830a4c / 1 / JQ-0001 | [127474,131776) | [127476,131778) | [Assignment; update assignment; arithmetic update assignment](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Changes only selected paths and defines += as the corresponding update with addition. |
| 0be2a4830a4c / 1 / JQ-0001 | [3335,4651) | [3335,4651) | [Invoking jq: Unix-shell filter quoting](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Recommends quoting the jq program; does not document expansion of json_content or json_file. |
| 0be2a4830a4c / 1 / JQ-0001 | [77123,77448) | [77125,77450) | [@sh](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Describes escaped POSIX-shell command text, not the Bash variable-expansion and output-target rules needed here. |
| 0be2a4830a4c / 4 / WT-0039 | [22957,23294) | [23005,23342) | [Terminal snippets: other potential issues](https://github.com/microsoft/terminal/blob/73948072120beb51d355b3c74b5f774a6526b277/doc/specs/%231595%20-%20Suggestions%20UI/Snippets.md) — The proposal describes shell redirection to a literal filename; it does not specify Bash variable or JSON quoting. |
| 0be2a4830a4c / 4 / WT-0039 | [20405,20898) | [20453,20946) | [Terminal snippets: JSON quoting discussion](https://github.com/microsoft/terminal/blob/73948072120beb51d355b3c74b5f774a6526b277/doc/specs/%231595%20-%20Suggestions%20UI/Snippets.md) — Recognizes escaped JSON and CLI parsing complexity but supplies no Bash quoting correction. |

### J3 B/S — a76ec0d77f82

Initial: **false** (R2); availability: **false**; classification: `evidence_absent_in_permitted_window`. No condition-status or completeness change.

**C1 — unknown.** The manual window describes generic composition; the decimal-library window is declarations and includes. The other windows are CLI/parser preambles (A) or schema/proposal introductions (B). No window establishes append by array concatenation, update assignment, or preservation of other settings. The original literal-command success report does not supply the missing packet evidence for the variable-based operation.

**C2 — unknown.** No permitted window documents --argjson, Bash parameter/command expansion, preserving JSON text as one argv item, or the variable .new output filename. The original missing closing quote and unquoted expansion are observations, not an evidenced correction.

Every permitted source window was displayed in full; no S navigation or broadening was used. Total permitted and uniquely audited source text is 4800 codepoints.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| a76ec0d77f82 / 1 / JQ-0001 | [309,1509) | [309,1509) | [Complete permitted manual excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Full fixed window inspected; only this window may contribute to this packet. |
| a76ec0d77f82 / 2 / JQ-0016 | [11388,12588) | [11388,12588) | [Complete permitted decimal library excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/decNumber/decNumber.c) — Full fixed window inspected; only this window may contribute to this packet. |
| a76ec0d77f82 / 3 / WT-0021 | [0,1200) | [0,1200) | [Complete permitted Terminal schema excerpt](https://github.com/microsoft/terminal/blob/73948072120beb51d355b3c74b5f774a6526b277/doc/cascadia/profiles.schema.json) — Full fixed window inspected; only this window may contribute to this packet. |
| a76ec0d77f82 / 4 / WT-0039 | [0,1200) | [0,1200) | [Complete permitted Terminal snippets proposal excerpt](https://github.com/microsoft/terminal/blob/73948072120beb51d355b3c74b5f774a6526b277/doc/specs/%231595%20-%20Suggestions%20UI/Snippets.md) — Full fixed window inspected; only this window may contribute to this packet. |

### J4 A/F — a0007d0fb17a

Initial: **true** (R2); availability: **true**; classification: `confirmed_available`. No condition-status or completeness change.

**C1 — supported.** Per-volume iteration and object construction preserve VolumeId, VolumeType, Size and Iops together; the outer array collects one result per volume. The documented absent-key behavior retains null for missing original Iops, as the frozen interpretation permits.

**C2 — supported.** Within each current volume's object constructor, a parenthesized Tags subexpression selects Key=VolName and reads Value. Collecting matches and selecting [0] yields one value or null without dropping or mixing volumes. The first-match policy is explicit for unspecified duplicate matching tags.

Documentary construction (not executed):

`[.Volumes[] | {VolumeId, VolumeType, Size, Iops, VolName: ([.Tags[]? | select(.Key == "VolName") | .Value][0])}]`

Original JSON is incomplete and contains no Iops number. No manual example value is substituted; actual original execution remains unknown. VolName follows the frozen requirement rather than the failed expression's Name spelling.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| a0007d0fb17a / 1 / JQ-0001 | [16161,23700) | [16161,23700) | [Lookup; array indexing/iteration; pipe; parentheses](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Missing Iops yields null; each current volume and local tag pipeline can be retained separately. |
| a0007d0fb17a / 1 / JQ-0001 | [24719,28900) | [24719,28900) | [Array and object construction](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Collects one object per volume and evaluates sibling/tag expressions on that volume. |
| a0007d0fb17a / 1 / JQ-0001 | [44666,45400) | [44666,45400) | [select(boolean_expression)](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Supports selecting tags by Key equality and then reading Value. |

### J4 A/S — d018c8051020

Initial: **false** (R3); availability: **false**; classification: `evidence_absent_in_permitted_window`. No condition-status or completeness change.

**C1 — unknown.** The full fixed windows contain output-format switches, compiler matcher construction, thread-local storage and C value declarations. They do not establish jq iteration/projection/collection of all four siblings into one result per volume.

**C2 — unknown.** None of the four windows documents the required scoped Tags iteration, Key equality selection, Value extraction and attachment to the current volume. No out-of-window jq section may fill this gap.

Every permitted source window was displayed in full; no S navigation or broadening was used. Total permitted and uniquely audited source text is 4800 codepoints.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| d018c8051020 / 1 / JQ-0001 | [5933,7133) | [5933,7133) | [Complete permitted manual excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Full fixed window inspected; only this window may contribute to this packet. |
| d018c8051020 / 2 / JQ-0007 | [22375,23575) | [22375,23575) | [Complete permitted compiler excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/compile.c) — Full fixed window inspected; only this window may contribute to this packet. |
| d018c8051020 / 3 / JQ-0045 | [6282,7482) | [6283,7483) | [Complete permitted jv.c excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/jv.c) — Full fixed window inspected; only this window may contribute to this packet. |
| d018c8051020 / 4 / JQ-0046 | [537,1737) | [537,1737) | [Complete permitted jv.h excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/jv.h) — Full fixed window inspected; only this window may contribute to this packet. |

### J4 B/F — 837da1ed6706

Initial: **true** (R4); availability: **true**; classification: `confirmed_available`. No condition-status or completeness change.

**C1 — supported.** Per-volume iteration and object construction preserve VolumeId, VolumeType, Size and Iops together; the outer array collects one result per volume. The documented absent-key behavior retains null for missing original Iops, as the frozen interpretation permits.

**C2 — supported.** Within each current volume's object constructor, a parenthesized Tags subexpression selects Key=VolName and reads Value. Collecting matches and selecting [0] yields one value or null without dropping or mixing volumes. The first-match policy is explicit for unspecified duplicate matching tags.

Documentary construction (not executed):

`[.Volumes[] | {VolumeId, VolumeType, Size, Iops, VolName: ([.Tags[]? | select(.Key == "VolName") | .Value][0])}]`

Original JSON is incomplete and contains no Iops number. No manual example value is substituted; actual original execution remains unknown. VolName follows the frozen requirement rather than the failed expression's Name spelling.

Adversarial AWS check: Example 4 contains --query "Volumes[*].{ID:VolumeId,Tag:Tags}" and demonstrates ID/Tags association. This is stronger contextual evidence than the B/S opening, but the jq manual already supplies all frozen requirements; no completeness change results.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| 837da1ed6706 / 1 / JQ-0001 | [16161,23700) | [16161,23700) | [Lookup; array indexing/iteration; pipe; parentheses](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Missing Iops yields null; each current volume and local tag pipeline can be retained separately. |
| 837da1ed6706 / 1 / JQ-0001 | [24719,28900) | [24719,28900) | [Array and object construction](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Collects one object per volume and evaluates sibling/tag expressions on that volume. |
| 837da1ed6706 / 1 / JQ-0001 | [44666,45400) | [44666,45400) | [select(boolean_expression)](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Supports selecting tags by Key equality and then reading Value. |
| 837da1ed6706 / 3 / AWS-0706 | [0,3698) | [0,3698) | [describe-volumes Examples 1–4](https://github.com/aws/aws-cli/blob/75930d5779a99149020e242c5b834d2f28b3669f/awscli/examples/ec2/describe-volumes.rst) — Shows all four siblings and a later same-volume ID/Tags projection. It is corroborative; it does not alone extract Value for Key=VolName. |

### J4 B/S — a032f9aa185e

Initial: **false** (R1); availability: **false**; classification: `evidence_absent_in_permitted_window`. No condition-status or completeness change.

**C1 — partial.** The AWS first window shows VolumeType, VolumeId and Iops as siblings in an example Volumes element. It cuts off before that element's Size and supplies no projection/collection procedure. The remaining windows add output formatting, compiler scaffolding and EMR help. The required transformation is not established.

**C2 — unknown.** The AWS fixed window ends before Tags or the later --query example. No permitted window supplies same-volume tag selection or attachment of Value for Key=VolName.

Every permitted source window was displayed in full; no S navigation or broadening was used. Total permitted and uniquely audited source text is 4800 codepoints.

Adversarial AWS check: the B/F file contains a later ID/Tags projection, but it lies outside this packet's [0,1200) window. That later content was not used as evidence for B/S.

| Packet / slot / file ID | Characters | UTF-8 bytes | Source and evidential role |
|---|---|---|---|
| a032f9aa185e / 1 / JQ-0001 | [5933,7133) | [5933,7133) | [Complete permitted manual excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) — Full fixed window inspected; only this window may contribute to this packet. |
| a032f9aa185e / 2 / JQ-0007 | [22375,23575) | [22375,23575) | [Complete permitted compiler excerpt](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/compile.c) — Full fixed window inspected; only this window may contribute to this packet. |
| a032f9aa185e / 3 / AWS-0706 | [0,1200) | [0,1200) | [Complete permitted describe-volumes excerpt](https://github.com/aws/aws-cli/blob/75930d5779a99149020e242c5b834d2f28b3669f/awscli/examples/ec2/describe-volumes.rst) — Full fixed window inspected; only this window may contribute to this packet. |
| a032f9aa185e / 4 / AWS-0248 | [2299,3499) | [2299,3499) | [Complete permitted EMR help excerpt](https://github.com/aws/aws-cli/blob/75930d5779a99149020e242c5b834d2f28b3669f/awscli/customizations/emr/helptext.py) — Full fixed window inspected; only this window may contribute to this packet. |

## Access and display notes

One J3 B/F Terminal-proposal search display was truncated by the output cap at 20:14:36 UTC. The same search was redisplayed completely at 20:15:08 UTC, before conclusions were written; no truncated-only source interval supports a claim. Earlier combined metadata displays were narrowed and reread. The final proof records reference displayed audit-helper intervals, not unseen source-cache text.

No independent-reader success rate, human discovery rate, or original-user runtime success is inferred from these availability results.
