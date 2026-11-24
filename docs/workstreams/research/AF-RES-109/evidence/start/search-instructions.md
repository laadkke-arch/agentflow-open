# Exact arm instruction text (request body omitted)

You are one isolated search arm in a controlled research task. You have no prior research results. Do only the assigned request and method below. Read no other request/arm/repository file, parent conversation, HANDOFF, or sibling output. Do not delegate. Do not inspect source-issue comments, status, linked PRs, releases, or its later resolution. If search results automatically expose them, log that exposure and continue honestly. Do not ask the user anything.

Find useful primary-source links that add a concrete design choice or discriminating failure test for the supplied natural request. Existing implementation mentioned by its author is a baseline, not a new invention. An unmentioned alternative is only absent from the supplied list, not proved unknown to its author. Do not invent missing requirements. Return up to THREE actual links; zero or vacant slots are allowed.

EXPERIMENT BUDGET: at most THREE individual queries using ONLY tools.mcp__codex_apps__search_service_web_run system2_search_query (English), at most SIX explicit opens total using that same tool. Each open/click/find/reopen/failed open consumes one open slot. Search queries count by query items, not tool calls. No other internet retrieval or shell networking or GitHub API fallback within this arm. The natural input below is provided equally and is not an open. Query results are exposure, not direct reading. Only use primary/official sources for technical claims. Record search top FIVE exactly in displayed order and all additionally exposed results; mark missing ranks if fewer than5. Do not improve/reorder search rankings. Do not open the original request URL or later same-issue PR to learn a solution.

Log actual UTC before/after EACH tool action, elapsed seconds, actual query, output refs, original/final URL and any redirect/failure. Keep explicit-open count; automatic engine reads, token use, exact immutable backend version and money cost are UNKNOWN if not provided (never0). Model is inherited from parent, displayed parent label GPT-6 Astra Pro; verify only what is actually exposed. Query strategy is allowed to adapt after every result; no requirement to spend all budget. Do not add extra queries merely to fill a quota. Use functions store for raw responses and retain them only in ignored .cache if helpful; do not commit/copy full third-party pages into output. Each page summary <=160 words and total direct quotes <=20 words per source.

WRITE ONLY your assigned evidence/search/Rn-ARM directory. No git changes or commits, no central ledger edits. Create:
1) events.jsonl: start event (model/tool/input hash/context status); every query/open with sequential event_index, request_id,arm,started_utc,ended_utc,elapsed_seconds,event_type,query or requested_url,actual_url,status,ref_ids,results [{displayed_rank,title,url,ref,seen_content}], top5_missing_ranks, exposure_notes, automatic_reads:null, monetary_cost:null. Include stop event with actual counts and elapsed time.
2) returns.json: request_id,arm,input_sha256,actual_queries,actual_explicit_opens,start_utc,end_utc,unknown_costs,method_notes,final_candidates array [{rank,url,source_ref,source_id,title,provider,product_feature,version_or_date,exact_section,form (product/function/same_domain_component/cross_domain_principle/lexical_only),input_processing_observation,what_is_new_vs_baseline,changed_choice,minimal_discriminating_input,expected_output,conditions_supported,limitations,counter_evidence,historical_availability,acquisition_event}]. Evidence not verified must say unknown. Add vacancies for remaining ranks1..3 with reasons. Each candidate must be an actual discovered link; distinguish snippet only from directly read.
3) sources.jsonl: one row per explicit open, including failed ones; source_id,original_url,actual_url,author_lineage,edition,published_utc(if known),direct_read_utc,exact_section,confirmed,limits,counter_observation,unknown,questions:[Q3,Q4,Q5,Q6],experiment_rows,original_work_id,counts_as_unique_primary (false for failure/snippet/reopen/duplicate),count_category:'search_returned',reader,source_kind,ref_id. Do not equate different anchors with independent works.
4) notes.md: input and baseline understanding, actual search strategy, unfilled requirements, unintended exposure and what was NOT tested. State whether each new test is only proposed (default) or actually executed (none is expected).

Tool access: functions.exec permits tools.mcp__codex_apps__search_service_web_run; use tools.exec_command only for local file reads/writes, hashes/time. Tool schema available in system developer instructions; tools.apply_patch may write files. Root will integrate and verify. When done report the files and counts, no unperformed outcomes.


## A

METHOD A: Act as a generally skilled model with web search. Choose any search strategy you think useful, including same-domain alternatives, unfamiliar domains, reformulation or any mix. No particular decomposition or donor domain is required.

## B

METHOD B: First decompose target part, preserved conditions, and the operative input→processing→observation relationship. Search for same-domain candidates AND try a relational query without naming a donor field or a target product. Choose the relation from the request itself. No donor domain or answer is provided. Do not add requirements while decomposing.

## Shared natural input

Each assignment appended only its ID, arm, original URL, posted date, input hash, output directory, then title + two newlines + current body. Exact body hashes are in requests.jsonl. Natural text was identical in both arms and is not republished here.
