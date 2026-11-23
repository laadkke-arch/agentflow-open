# AF-RES-100: public followup attribution after seal2

This report covers all eight preregistered cases. It is separate attribution evidence after commit `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673`; it does not change the sealed packet judgments, source rankings, or comparison denominators.

## What the public record establishes

The API returned eight questions, five answers across four questions, 29 revision records, and 18 comments in the specified 30-day windows. Three answers were accepted within those windows. No case supplies a verified execution tying the same original tool versions, complete inputs, and required outputs together. Author reports of failure, partial diagnostics, existing helper use, and a working alternative are recorded separately below.

| Case | Current accepted answer | Questioner followup category | Same version/input/output execution |
| --- | --- | --- | --- |
| [J1](https://stackoverflow.com/questions/79694539) | None | failed_workaround_reported | Not established |
| [J2](https://stackoverflow.com/questions/79699191) | [79700162](https://stackoverflow.com/a/79700162) | mixed_partial_diagnostic_reports | Not established |
| [J3](https://stackoverflow.com/questions/79711268) | None | success_reported_for_alternative_input_method | Not established |
| [J4](https://stackoverflow.com/questions/79727040) | [79727098](https://stackoverflow.com/a/79727098) | none_observed | Not established |
| [P1](https://stackoverflow.com/questions/79692729) | None | existing_helper_use_reported | Not established |
| [P2](https://stackoverflow.com/questions/79701174) | None | none_observed_after_original | Not established |
| [P3](https://stackoverflow.com/questions/79703916) | None | working_dockerfile_claim_without_output | Not established |
| [P4](https://stackoverflow.com/questions/79714790) | [79714812](https://stackoverflow.com/a/79714812) | none_observed | Not established |

Acceptance is a platform event. Thanks or an assertion that a workaround works is a user report. An answerer's example output is not a questioner's execution. The false verification fields in the CSV mean evidence was not established, rather than proving different versions or inputs were used.

## Retrieval and attribution

The window is inclusive from each original question's creation timestamp through exactly 30 days later. Current posts and all returned answer/question revisions are also retained as metadata, with explicit window flags. The earliest body-bearing answer revisions are compared with later revisions and current answers. The source ledger preserves exact API URLs, UTC retrieval times, response hashes, revision IDs, public user roles, and fixed revision URLs where available. The initial blinded revision filter omitted editors; a separate ordinary revision request supplies editor metadata after the seal.

There were 20 API requests, 0 recorded failures, and no returned backoff instructions. Pagination completed for every response. No questioners were contacted; no linked old questions, external demos, or documentation pages were followed. No subject runtime was executed, including no P4 render. Deleted/private posts and deleted comments are outside the API-visible record, and comments have no retrieved edit history.

This was a reused machine-reader context following an interrupted duplicate reading attempt. It is not independent human confirmation. Original full bodies are held only in the ignored cache; the committed deliverables contain metadata, hashes, links, and short paraphrases.

## J1 — [79694539](https://stackoverflow.com/questions/79694539)

Window: 2025-07-08T16:15:58+00:00 through 2025-08-07T16:15:58+00:00. Current answers: 0; comments in window: 3.

No public answer was returned. A commenter suggested replacing input[] with inputs[]; the questioner reported that this removed the error but did not perform the intended JOIN.

Only the original question body revision was returned; the current body hash equals the frozen original.

No answer revision exists in the retrieved public record.

**Attribution and execution.** No positive acknowledgement; explicit negative result for the proposed workaround. The questioner reports trying inputs[] on the two-file task and obtaining normal termination without the intended join. No command transcript, complete inputs, or correct output is supplied.

**Goal and route.** Successful termination was reported, while the JOIN goal remained unmet. Error disappearance must not be coded as the desired result.

**Verification limits.** The original jq version is unspecified, and the followup supplies no version. The followup refers to the original file2 excerpt and task, but neither full file nor an input hash is available. The intended joined output is explicitly not achieved in the report; no successful output is shown.

**Relation to seal2.** The sealed full-file packets supported next diagnostic actions, not successful original execution. This negative inputs[] followup does not overwrite those documentation judgments or establish a unique cause.

Evidence:

- [J1-E01](https://stackoverflow.com/questions/79694539#comment140574771_79694539) — 2025-07-08T19:11:16+00:00; other_participant. Another participant requested minimal versions of both files and the expected output.
- [J1-E02](https://stackoverflow.com/questions/79694539#comment140574783_79694539) — 2025-07-08T19:12:42+00:00; other_participant. Another participant suggested inputs[] as a replacement.
- [J1-E03](https://stackoverflow.com/questions/79694539#comment140577987_79694539) — 2025-07-09T20:03:18+00:00; questioner. The questioner says inputs[] permits successful exit but does not perform the JOIN.

## J2 — [79699191](https://stackoverflow.com/questions/79699191)

Window: 2025-07-12T10:23:08+00:00 through 2025-08-11T10:23:08+00:00. Current answers: 2; comments in window: 6.

The questioner posted a self-answer, then accepted a different answer that replaces the sed/jq cleanup route with yq XML options and a dictionary conversion on an illustrative one-event XML input.

A non-questioner split the pipeline across lines; the eventual answerer later added XML/yq tags. No complete original log or envelope was added.

Self-answer 79699725 first attributed successful execution to explicitly indexed array access, then replaced that account with a missing-EventData explanation and optional traversal. Answer 79700162 initially showed XML normalization only; its second revision added an explicit Name/Content dictionary conversion and sample null output. Revision metadata identifies both changes as their respective authors' edits.

**Attribution and execution.** The self-answer thanks a commenter; a separate answer is accepted. Neither signal alone verifies the original complete pipeline. The questioner reports two errors from suggested filters, supplies key-count diagnostic outputs, and revises an earlier works-for-me claim. The accepted answer shows answerer-provided example output, without a questioner report that the accepted yq route ran on the complete original evtx/log.

**Goal and route.** The accepted answer changes the processing route to yq, changes content naming to Content, and demonstrates one Event. The self-answer also reveals an event with UserData rather than EventData, beyond the frozen sample's missing-content issue.

**Verification limits.** No exact jq or yq version is supplied in the original or followups. The questioner names Security.json without supplying it; the accepted answer uses an illustrative input.xml with a single Event, not the complete original log. The accepted example contains a dictionary and null for the missing CommandLine content, but no complete all-event original output is supplied.

**Relation to seal2.** The sealed J2 full-file judgments were conditional transformations for the registered event path and missing-content rule. Later evidence identifies an additional missing-EventData case and an accepted yq route; it is attribution context, not a retrospective change to those packet judgments or to the preselected sed adjacency.

Acceptance timestamp: 2025-07-14T21:04:27+00:00. The timeline owner field refers to the answer owner, not an independently verified accepting actor.

Evidence:

- [J2-E01](https://stackoverflow.com/questions/79699191#comment140584408_79699191) — 2025-07-12T10:28:20+00:00; other_participant. A commenter recommended doing the pipeline cleanup in yq.
- [J2-E02](https://stackoverflow.com/questions/79699191#comment140584414_79699191) — 2025-07-12T10:33:50+00:00; other_participant. A commenter proposed converting individual Data entries to Name-key objects.
- [J2-E03](https://stackoverflow.com/questions/79699191#comment140584425_79699191) — 2025-07-12T10:42:00+00:00; other_participant. The same commenter proposed a map/from_entries dictionary update.
- [J2-E04](https://stackoverflow.com/questions/79699191#comment140584449_79699191) — 2025-07-12T11:06:26+00:00; questioner. The questioner reports null-iteration and string-indexing errors with the two proposed filters.
- [J2-E05](https://stackoverflow.com/questions/79699191#comment140584453_79699191) — 2025-07-12T11:09:24+00:00; questioner. The questioner identifies several named fields whose content is null, with occurrence counts.
- [J2-E06](https://stackoverflow.com/revisions/CE0C3B2C-23EA-43DE-8F89-4B01A7CC654A/view-source) — 2025-07-13T04:12:05+00:00; questioner. The initial self-answer reports success using an explicit index expression and speculates about iteration beyond the array; this account was later replaced.
- [J2-E07](https://stackoverflow.com/revisions/5931D56D-480F-4826-9124-71C9BDE946CB/view-source) — 2025-07-13T07:35:59+00:00; questioner. The questioner replaces the initial explanation with heterogeneous EventData/UserData keys, optional traversal, diagnostic counts, and continuing uncertainty about selection behavior.
- [J2-E08](https://stackoverflow.com/revisions/BCE0455B-00F3-447C-B891-B03B5B80D1EC/view-source) — 2025-07-13T18:10:51+00:00; answerer. The answerer initially demonstrates yq attribute/content naming on an illustrative XML example and recommends moving processing into yq.
- [J2-E09](https://stackoverflow.com/revisions/7AFEF78E-3B19-4DE1-8B20-FEB85A0491A7/view-source) — 2025-07-13T18:21:53+00:00; answerer. The answerer's next revision adds the dictionary transformation and an example output retaining missing content as null.
- [J2-E10](https://stackoverflow.com/posts/79699191/timeline) — 2025-07-14T21:04:27+00:00; answerer. The public timeline records acceptance of answer 79700162 within the 30-day window.

## J3 — [79711268](https://stackoverflow.com/questions/79711268)

Window: 2025-07-23T03:13:54+00:00 through 2025-08-22T03:13:54+00:00. Current answers: 1; comments in window: 5.

The sole answer reads the settings file and additional JSON file arguments through inputs, using the script's positional arguments. The questioner eventually reports that this file-based method works.

The question body remains identical to the frozen original; the additional revision record is metadata-only.

The sole answer has one body-bearing revision and is unchanged. The clarification occurs in comments rather than an edited answer.

**Attribution and execution.** An early thanks acknowledges a quoting suggestion; a later explicit success report follows clarification of $@. The questioner first reports a filename-too-long error after replacing $@ with JSON text, then reports success after leaving $@ as the script's filename arguments. This is a user execution claim, without an archived output file or independent reproduction.

**Goal and route.** The answer preserves the colorscheme-append goal but uses supplied filenames instead of passing the preloaded json_content variable. An initial attempt to pass JSON text as a filename fails, then the questioner adopts the positional-filename approach.

**Verification limits.** jq 1.7 and Ubuntu/WSL2 are stated only in the original. The successful followup does not restate or independently verify those versions. The questioner says one additional colorscheme JSON file is supplied, but no immutable input match or file hash is available. The questioner says the result is the same and works, but supplies no resulting settings.json.new body or applied Terminal result.

**Relation to seal2.** The sealed J3 packets remained incomplete because the required Bash/argv boundary was not fully documented in packet evidence. Later success with a file-argument alternative does not supply a missing pre-outcome citation or overwrite that result.

Evidence:

- [J3-E01](https://stackoverflow.com/questions/79711268#comment140610649_79711268) — 2025-07-23T03:16:21+00:00; other_participant. Another participant explains that Bash single quotes prevent variable expansion and suggests changing the command quoting.
- [J3-E02](https://stackoverflow.com/questions/79711268#comment140613089_79711268) — 2025-07-23T19:14:07+00:00; questioner. The questioner thanks that suggestion and says the explanation makes sense, without providing a successful transcript.
- [J3-E03](https://stackoverflow.com/revisions/D0B335C6-803E-4397-9B63-6FB8F341D246/view-source) — 2025-07-23T04:20:55+00:00; answerer. The answer uses jq inputs with the settings filename and the script's positional filename arguments, writing to a .new file.
- [J3-E04](https://stackoverflow.com/questions/79711268#comment140613110_79711304) — 2025-07-23T19:29:36+00:00; questioner. The questioner substitutes JSON text for the filename arguments and receives a filename-too-long error.
- [J3-E05](https://stackoverflow.com/questions/79711268#comment140613115_79711304) — 2025-07-23T19:34:07+00:00; answerer. The answerer clarifies that $@ means the arguments passed to the script and should be left in place.
- [J3-E06](https://stackoverflow.com/questions/79711268#comment140613190_79711304) — 2025-07-23T20:16:47+00:00; questioner. The questioner says the clarified method works with one additional colorscheme file and thanks the answerer.

## J4 — [79727040](https://stackoverflow.com/questions/79727040)

Window: 2025-08-06T08:59:59+00:00 through 2025-09-05T08:59:59+00:00. Current answers: 1; comments in window: 0.

The accepted answer gives parenthesized tag selection and from_entries alternatives, with array and object example outputs that retain Iops as null.

The questioner corrects the desired tag field from Tags.Name to Tags.Key and clarifies that other irrelevant tags can exist. Other revisions correct formatting, grammar, and tags.

The first answer already contains the transformation alternatives and sample outputs. The second revision adds an explanation of how comma/pipe grouping parses the original expression; its transformation code and outputs are unchanged.

**Attribution and execution.** Acceptance is recorded; no questioner comment or thanks was returned. The answerer supplies example outputs and the questioner accepts the answer. The retrieved 30-day record contains no questioner execution transcript or explicit success report.

**Goal and route.** The answer uses VolName, matching the stated sample/goal, and retains the absent Iops as null. It supports both permitted result shapes. This is an answerer's example rather than a questioner's run.

**Verification limits.** The original and followups do not establish jq or AWS CLI versions. Only the abbreviated describe-volumes sample is available; no complete original file or hash is supplied. Answerer-provided example outputs match the disclosed fields and null Iops, but no questioner-produced output is preserved.

**Relation to seal2.** The sealed J4 full-file packets support the required transformation. Acceptance and the answer's null example are consistent with that interpretation, but do not convert documentation sufficiency into observed original execution.

Acceptance timestamp: 2025-08-06T11:30:01+00:00. The timeline owner field refers to the answer owner, not an independently verified accepting actor.

Evidence:

- [J4-E01](https://stackoverflow.com/revisions/9D6F0AC7-7630-4A2F-9890-F26C78B073F1/view-source) — 2025-08-06T09:14:23+00:00; questioner. The questioner changes the tag-member name to Key and explains that unrelated tag elements must be ignored rather than excluding only version.
- [J4-E02](https://stackoverflow.com/revisions/53C19479-AE75-4E7C-B257-C76836AE1792/view-source) — 2025-08-06T09:34:27+00:00; answerer. The answerer proposes grouping the tag pipeline or using from_entries and supplies array/object outputs with null Iops.
- [J4-E03](https://stackoverflow.com/revisions/36D141D1-35DA-4E57-A1DC-E6DBFE382ED4/view-source) — 2025-08-06T09:45:43+00:00; answerer. The answerer adds a grouped rendering of the original expression to explain precedence; the solution code and output examples do not change.
- [J4-E04](https://stackoverflow.com/posts/79727040/timeline) — 2025-08-06T11:30:01+00:00; answerer. The public timeline records acceptance of answer 79727098 within 30 days.

## P1 — [79692729](https://stackoverflow.com/questions/79692729)

Window: 2025-07-07T10:46:01+00:00 through 2025-08-06T10:46:01+00:00. Current answers: 0; comments in window: 2.

No public answer was returned. A commenter suggests a modified include_graphics helper with format preferences; the questioner says this is already the approach in use and accepts it as adequate.

The questioner adds Pandoc's default-image-extension attempt and explains that explicit image extensions emitted by knitr prevent that option from choosing a different format.

No answer revisions exist; relevant new information is in the question edit and comments.

**Attribution and execution.** The questioner acknowledges that the custom-helper approach is acceptable, while noting a preference for something easier. The questioner reports currently using a modified-function approach. No helper code, image files, versions, selected SVG/EMF path, or PowerPoint output is supplied.

**Goal and route.** The followup supports the helper-permitted interpretation. It does not establish a built-in include_graphics option, and the helper was reportedly already used before the suggestion, so new adoption cannot be attributed to the comment.

**Verification limits.** No relevant R, knitr, rmarkdown, or Pandoc version is established. Only the original JPEG filename is known; alternate file existence and the helper's actual inputs remain unknown. No SVG/EMF selection trace or final presentation is preserved.

**Relation to seal2.** The sealed P1 result supports only the adjacent/full-file packet under the preregistered helper-permitted interpretation. The questioner's acknowledgement is consistent with that interpretation but does not validate the sealed proposed helper or prove built-in support.

Evidence:

- [P1-E01](https://stackoverflow.com/revisions/CAA8E83F-E796-4E6E-B94E-D4AB802B07F0/view-source) — 2025-07-08T10:45:08+00:00; questioner. The questioner explains why Pandoc's default extension setting does not affect image paths whose extensions knitr has already supplied.
- [P1-E02](https://stackoverflow.com/questions/79692729#comment140574340_79692729) — 2025-07-08T16:11:09+00:00; other_participant. Another participant says they know no built-in facility and suggests a modified include_graphics function that chooses a format by availability, output type, and preferences.
- [P1-E03](https://stackoverflow.com/questions/79692729#comment140579507_79692729) — 2025-07-10T10:54:35+00:00; questioner. The questioner says that custom-helper approach is already in use and seems acceptable, though an easier method was sought.

## P2 — [79701174](https://stackoverflow.com/questions/79701174)

Window: 2025-07-14T17:02:44+00:00 through 2025-08-13T17:02:44+00:00. Current answers: 0; comments in window: 0.

No answer, accepted answer, or 30-day comment was returned.

Only the original question revision was returned, and the current body is unchanged.

No public answer revisions were returned.

**Attribution and execution.** None observed. The only execution reports are in the original question: Typst compilation succeeds, while Pandoc conversion with the package import fails. No post-question success or failure experiment is publicly reported in the retrieved window.

**Goal and route.** No later route or goal change was observed. The original Typst compile success concerns a different tool/output and is not a Pandoc conversion success.

**Verification limits.** The original Pandoc 3.1.3, Typst 0.13.1 and CeTZ 0.3.4 context is known; there is no followup run to match. The original minimal text is present, but package contents/hashes and a successful followup input are absent. No successful test2.md output retaining the package import and value 123 is supplied.

**Relation to seal2.** All sealed P2 packets remained incomplete. The empty public followup record neither validates nor refutes that documentation result and must not be counted as an observed technical failure.

No followup statement was returned. The current-post, answer-list, comment-list and timeline API receipt IDs in the CSV and evidence details document this empty public result; absence is not coded as a technical failure.

## P3 — [79703916](https://stackoverflow.com/questions/79703916)

Window: 2025-07-16T19:06:20+00:00 through 2025-08-15T19:06:20+00:00. Current answers: 0; comments in window: 2.

No public answer was returned. A commenter recommends using pandoc/extra as a base image and customizing a new Dockerfile. The questioner reports a working Dockerfile after starting from a simple base.

The current question body equals the frozen original, with no subsequent body revision.

No answer revision exists; the resolution claim is a comment.

**Attribution and execution.** The questioner thanks the commenter, says the advice was correct, and offers to share the working Dockerfile; the retrieved record does not contain that file. The questioner reports a working Dockerfile but supplies no build log, Dockerfile, image digest, final command, or PDF. This is stronger than generic thanks but weaker than a verified original-dependency execution.

**Goal and route.** The general container-build goal is retained, while the implementation approach changes from adapting existing Dockerfiles to building a simpler custom one. Exact preservation of the custom template, both filters, and the multi-file PDF command is not documented.

**Verification limits.** No image digest, Pandoc version, filter versions, or LaTeX version is supplied in the followup. The six Markdown files and custom template remain unavailable; no final Dockerfile is shown. No resulting PDF is supplied, and the followup does not explicitly show the original multi-file PDF command completing.

**Relation to seal2.** P3 remains incomparable in the strict sealed comparison because the preregistered adjacent source version could not be pinned. A later working-Dockerfile claim does not repair that research-input vacancy or create an A/B win.

Evidence:

- [P3-E01](https://stackoverflow.com/questions/79703916#comment140594940_79703916) — 2025-07-16T19:18:05+00:00; other_participant. Another participant recommends starting from pandoc/extra:latest-ubuntu and adding files or a startup script in a new Dockerfile.
- [P3-E02](https://stackoverflow.com/questions/79703916#comment140597463_79703916) — 2025-07-17T15:23:20+00:00; questioner. The questioner says starting with a simple base Dockerfile and adding commands worked, thanks the commenter, and offers to share the file without posting it.

## P4 — [79714790](https://stackoverflow.com/questions/79714790)

Window: 2025-07-25T13:20:04+00:00 through 2025-08-24T13:20:04+00:00. Current answers: 1; comments in window: 0.

The sole accepted answer cites Pandoc's YAML metadata documentation and quotes the colon-containing title value.

Before the answer, the questioner changes the word semicolon to colon without changing the title characters. A later third-party edit adjusts formatting only.

The answer has a single body-bearing revision and is unchanged.

**Attribution and execution.** Acceptance is recorded; there are no returned comments or explicit questioner success statements. The accepted answer supplies the proposed syntax, and the timeline records acceptance 31 seconds after posting. No same-version execution transcript, metadata output, or PDF is supplied; acceptance is not execution evidence.

**Goal and route.** The answer addresses the same title scalar at the Markdown input boundary. It does not replace the named filters or claim a different document-build goal.

**Verification limits.** Pandoc 2.18 is stated in the original only; no followup execution is recorded. The proposed scalar retains the exact disclosed title text, but the complete original document and actual edited input are unavailable. No parsed metadata, command exit record, or resulting PDF is preserved.

**Relation to seal2.** The sealed P4 full-file packets support the input syntax correction. The accepted answer is consistent with that documentation conclusion but does not supply runtime confirmation. No P4 runtime rendering was performed in this followup work.

Acceptance timestamp: 2025-07-25T13:35:19+00:00. The timeline owner field refers to the answer owner, not an independently verified accepting actor.

Evidence:

- [P4-E01](https://stackoverflow.com/revisions/918E3FF7-BBCA-45ED-A82C-567530B5294F/view-source) — 2025-07-25T13:24:03+00:00; questioner. The questioner corrects the character's name from semicolon to colon, leaving the actual title and parse error unchanged.
- [P4-E02](https://stackoverflow.com/revisions/62EA7585-728E-44A7-9606-64E44A9A4864/view-source) — 2025-07-25T13:34:48+00:00; answerer. The answerer proposes a quoted YAML title that preserves the colon, based on the Pandoc manual.
- [P4-E03](https://stackoverflow.com/posts/79714790/timeline) — 2025-07-25T13:35:19+00:00; answerer. The timeline records acceptance 31 seconds after the answer was posted; it contains no execution trace.
- [P4-E04](https://stackoverflow.com/revisions/A615F619-2B64-4C1F-AA0C-8604BE1BD1B3/view-source) — 2025-07-25T14:48:14+00:00; other_participant. Another participant adds syntax formatting and reformats the error message without changing the underlying title or command.

## Files and reproduction

- [outcomes.csv](outcomes.csv): one stable row for each of the eight cases, with links, windows, roles, acceptance and verification fields.
- [evidence-details.json](evidence-details.json): per-case observations, exact body hashes, revision histories, author roles, and read-only sealed comparisons.
- [sources.jsonl](sources.jsonl): unified source-ledger fields plus exact API receipt details. All rows use Q7, post_seal2, count_minimum=false and count_group=post_outcome_attribution.
- [retrieval-index.json](retrieval-index.json): sanitized automatic metadata inventory.
- [assessment.json](assessment.json): explicit manual coding and paraphrases.
- [fetch_public_outcomes.py](fetch_public_outcomes.py) and [compile_outcomes.py](compile_outcomes.py): reproducible fetching, inspection, and compilation.

Run the fetch script with `fetch`, inspect a case with `read --case J2 --part answers` (or questions/comments/timeline), then run the compilation script. Existing cached successful URLs are reused. API backoff and Retry-After are respected; failures are logged. New fetching does not run submitted code or mutate primary judgments.
