# AF-RES-029 — search, body, citation and frozen-use failure trace

Created 2026-11-22T13:24:17.440914+00:00. This exposed saved-receipt audit joins **12 questions × C/A/B = 36 observations**, all **44 returned candidate uses**, and **116 visits**, preserving **seven empty returns** and every common start. The sole verdict source is `evidence/candidate-decisions.jsonl`, SHA-256 `2d1ff41330f88ac89ddccf6e36d4bfe19328814a86f3cb30cbdfb9171d6b93a0`. No scores, frozen predicates, original files or prior masked outputs were changed. No network request was made.

The JSONL companion supplies one complete Q/route record with original search ranks, common eligibility and provider boundaries, route selections, visit IDs/delivered line ranges, original returned URL/sections, every candidate predicate status and next minimum source. This is diagnosis of the original observations, not new adjudication.

## Definitions and interpretation

`primary_stage` refers to the **frozen original request scope**. Separate partial/whole stage fields preserve useful partial progress without crediting a whole request. “Supported” requires an existing supported returned-section verdict for one individual candidate; candidates are never fused. Empty returns use `empty_route`, with the underlying discovery/body/policy cause recorded secondarily. An empty attempt receives no invented candidate verdict.

| Stage | Meaning in this trace |
|---|---|
| `not_appeared` | No eligible exact provider/component was identified in the relevant fixed search window or inherited provider set; not global absence. |
| `name_only` | An overview, index or symbol/type name lacks the required operational contract. |
| `exact_component_unread` | The exact implementation, entry point, header guard, test or operational clause was not delivered, although a nearby family/interface/page was read. |
| `version_environment_conflict` | A delivered contract positively conflicts with the frozen actor, environment, version-specific behavior or input/output policy. Mere version differences do not establish contradiction. |
| `citation_omission` | Opened evidence supports a predicate or candidate scope, but the original returned URL/section omits necessary supporting content. |
| `novelty_unverified` | Candidate identity/use is insufficient to resolve novelty. Already-named use is separate and is not itself this failure. |
| `evidence_unverified` | Relevant substantive material was read, but a mandatory conjunction remains unproved without positive contradiction. |
| `empty_route` | Zero candidates in the original sealed return; concrete causes remain in secondary stages. |
| `supported` | An existing candidate is supported on the exact returned-citation surface for the stated scope. |

Ranks are positions in a saved tool response, not certified global search-engine ranks. Common ranks are experiment provenance, not proof that B received the full SERP. Next minimum sources are evidentiary requirements, not promises that a compatible implementation exists; post-seal reading cannot improve an original return. When several candidates fail differently, the route primary selects the principal bottleneck described in the chain, while candidate-specific stages and all predicate statuses remain explicit.

## Table 2 input — all 36 observations

P/W cells preserve candidate verdict sets on returned sections: **S** supported, **U** unverified, **X** conflict, **∅** empty. X/U means different candidates have different verdicts. The partial stage is shown when it differs from the original-scope primary.

| Event / route | Original scope; candidates | Returned P / W | Original-scope primary | Secondary / partial distinction | Decision rows; visit rows |
|---|---|---|---|---|---|
| Q01-C | partial; 2 | S / X | `supported` | — | D 1–2; V 1–3 |
| Q01-A | partial; 2 | S / X | `supported` | — | D 3–4; V 4–6 |
| Q01-B | partial; 2 | S / X | `supported` | — | D 5–6; V 7–8 |
| Q02-C | whole; 0 | ∅ / ∅ | `empty_route` | not_appeared | D none; V 9 |
| Q02-A | whole; 2 | X/U / X/U | `version_environment_conflict` | evidence_unverified | D 7–8; V 10–14 |
| Q02-B | whole; 0 | ∅ / ∅ | `empty_route` | not_appeared | D none; V none |
| Q03-C | partial; 2 | X / X | `version_environment_conflict` | — | D 9–10; V 15–17 |
| Q03-A | partial; 0 | ∅ / ∅ | `empty_route` | version_environment_conflict | D none; V 18–21 |
| Q03-B | partial; 0 | ∅ / ∅ | `empty_route` | version_environment_conflict; exact_component_unread | D none; V 22 |
| Q04-C | whole; 1 | U / U | `exact_component_unread` | evidence_unverified | D 11; V 23–25 |
| Q04-A | whole; 1 | S / U | `exact_component_unread` | P: supported; name_only; evidence_unverified | D 12; V 26–31 |
| Q04-B | whole; 1 | U / U | `exact_component_unread` | evidence_unverified | D 13; V none |
| Q05-C | whole; 2 | U / U | `name_only` | exact_component_unread; evidence_unverified | D 14–15; V 32–34 |
| Q05-A | whole; 1 | U / X | `version_environment_conflict` | P: evidence_unverified; evidence_unverified; exact_component_unread | D 16; V 35–39 |
| Q05-B | whole; 1 | U / U | `evidence_unverified` | exact_component_unread | D 17; V 40–41 |
| Q06-C | partial; 1 | X / X | `version_environment_conflict` | evidence_unverified | D 18; V 42–44 |
| Q06-A | partial; 0 | ∅ / ∅ | `empty_route` | version_environment_conflict; exact_component_unread | D none; V 45–48 |
| Q06-B | partial; 1 | X / X | `version_environment_conflict` | — | D 19; V 49–52 |
| Q07-C | partial; 1 | U / U | `name_only` | exact_component_unread; novelty_unverified; evidence_unverified | D 20; V 53–55 |
| Q07-A | partial; 0 | ∅ / ∅ | `empty_route` | exact_component_unread; not_appeared; evidence_unverified | D none; V 56–59 |
| Q07-B | partial; 0 | ∅ / ∅ | `empty_route` | exact_component_unread; name_only; evidence_unverified | D none; V 60–63 |
| Q08-C | whole; 2 | U / U | `exact_component_unread` | evidence_unverified | D 21–22; V 64–66 |
| Q08-A | whole; 2 | X / X | `version_environment_conflict` | evidence_unverified | D 23–24; V 67–71 |
| Q08-B | whole; 2 | U / U | `exact_component_unread` | evidence_unverified | D 25–26; V 72–73 |
| Q09-C | partial; 2 | S / U | `supported` | — | D 27–28; V 74–76 |
| Q09-A | partial; 2 | S / U | `supported` | — | D 29–30; V 77–80 |
| Q09-B | partial; 1 | S / U | `supported` | — | D 31; V 81–84 |
| Q10-C | whole; 2 | U / X/U | `exact_component_unread` | evidence_unverified; version_environment_conflict | D 32–33; V 85–87 |
| Q10-A | whole; 2 | S/U / X/U | `evidence_unverified` | P: supported; version_environment_conflict; exact_component_unread | D 34–35; V 88–92 |
| Q10-B | whole; 2 | U / X | `exact_component_unread` | evidence_unverified; version_environment_conflict | D 36–37; V 93–96 |
| Q11-C | whole; 2 | U / U | `evidence_unverified` | P: citation_omission; citation_omission; exact_component_unread | D 38–39; V 97–99 |
| Q11-A | whole; 1 | U / U | `evidence_unverified` | P: citation_omission; citation_omission; name_only; exact_component_unread | D 40; V 100–103 |
| Q11-B | whole; 1 | S / U | `evidence_unverified` | P: supported; name_only; exact_component_unread | D 41; V 104–108 |
| Q12-C | partial; 1 | U / U | `exact_component_unread` | evidence_unverified | D 42; V 109–111 |
| Q12-A | partial; 1 | U / U | `exact_component_unread` | evidence_unverified | D 43; V 112–114 |
| Q12-B | partial; 1 | U / U | `exact_component_unread` | evidence_unverified | D 44; V 115–116 |

D means `evidence/candidate-decisions.jsonl`; V means `visits.jsonl`. `returns.jsonl`, `routes.jsonl` and the new failure-trace JSONL use the same 1–36 row order as this table. Candidate pointers and stable visit IDs are in the JSONL. B Q02/Q04 have no additional visits; Q04 nevertheless has a nonempty common-specification return.

### Both-failure events and common support

| Event | Original scope | C partial | A partial | B partial | Both A/B fail original? | Both A/B fail partial? |
|---|---|---|---|---|---|---|
| Q01 | partial | S | S | S | no | no |
| Q02 | whole | — | — | — | yes | yes |
| Q03 | partial | — | — | — | yes | yes |
| Q04 | whole | — | S | — | yes | no |
| Q05 | whole | — | — | — | yes | yes |
| Q06 | partial | — | — | — | yes | yes |
| Q07 | partial | — | — | — | yes | yes |
| Q08 | whole | — | — | — | yes | yes |
| Q09 | partial | S | S | S | no | no |
| Q10 | whole | — | S | — | yes | no |
| Q11 | whole | — | — | S | yes | no |
| Q12 | partial | — | — | — | yes | yes |

**Ten events have both A/B fail their original scope.** Only Q01 and Q09 have supported original-scope candidates. The frozen-partial both-failure set is **Q02, Q03, Q05, Q06, Q07, Q08 and Q12**. Q04 A, Q10 A and Q11 B add supported partial operations while the original whole requests remain unsupported. There is no supported whole candidate. These are summaries of the preserved candidate decisions; the 36 route rows are not 36 independent design events.

## Per-question chain and next evidence

### Q01 — proposal: Go 2: Array or variadic destructuring to discrete variables

Frozen boundary: **partial**, `judging/frozen-questions.jsonl` row 1.

**C.** Common ranks 1 PHP and 2 MDN were opened. Returned destructuring/default sections support fixed-width, ordered extraction with null padding; the whole Go assignment action conflicts with their source-language environment. PHP is already named; JavaScript is a new target, with practical Go bridging unverified. Evidence: `returns.jsonl` row 1; `common/Q01/start.json`; V 1–3; D 1–2.

**A.** Search 1 rank 1 rediscovered MDN; search 2 rank 7 SWIG Varargs was opened but its wrapper/type boundary was not retained. A returned the common PHP/JavaScript operations, retaining partial support and the whole Go mismatch. Evidence: `returns.jsonl` row 2; `routes/A/Q01/route.json`; V 4–6; D 3–4; `routes/A/Q01/search_hits.jsonl` for exact per-query positions.

**B.** B followed the actual PHP Language Reference and Types index links, adding no required operation. It returned the common PHP/JavaScript bodies with explicit JavaScript null defaults. Partial support is retained; whole Go integration is absent. Evidence: `returns.jsonl` row 3; `routes/B/Q01/route.json`; V 7–8; D 5–6.

**Next minimum source:** Whole: a versioned Go compiler or Go-callable component implementing ordered destructuring and nil padding, with a compatible value boundary. A bridge test would clarify practical use of the already-supported partial.

### Q02 — proposal: benchmark unit properties

Frozen boundary: **whole**, `judging/frozen-questions.jsonl` row 2.

**C.** No first-ten common hit identified an eligible provider of unit-keyed benchmark metadata parsing/normalization. Zero bodies were opened and the common return is empty. This fixed-window absence is not global nonexistence. Evidence: `returns.jsonl` row 4; `common/Q02/start.json`; V 9.

**A.** Search 1 ranks 1/4 supplied benchstat/benchfmt; search 2 rank 1 supplied reader.go. All three documents were read and returned in two candidates. The parser rejects equal-key differing values but accepts the frozen semantically contradictory cross-key directions; four-form normalization and CLI/stream application are incomplete. Evidence: `returns.jsonl` row 5; `routes/A/Q02/route.json`; V 10–14; D 7–8; `routes/A/Q02/search_hits.jsonl` for exact per-query positions.

**B.** The common provider set and observed-link set are empty, so B makes zero calls and returns no candidates. It cannot import the later A discovery into its original provider-restricted route. Evidence: `returns.jsonl` row 6; `routes/B/Q02/route.json`; V none.

**Next minimum source:** Official direction normalization/merge implementation or tests for all four higher/lower=better/worse forms and rejection of higher=better plus lower=better; whole also needs CLI/stream equivalence and following-result application.

### Q03 — proposal: Change concurrent map writes from fatal to panic

Frozen boundary: **partial**, `judging/frozen-questions.jsonl` row 3.

**C.** Common ranks 1/2 opened two runtime HACKING versions/mirrors; concrete map-source hits at ranks 6/9 were not opened. Returned guidance positively assigns racing map writes to fatal/unrecoverable behavior, conflicting with the frozen detector-to-catchable-signal action. Evidence: `returns.jsonl` row 7; `common/Q03/start.json`; V 15–17; D 9–10.

**A.** Search 1 rank 9 runtime_fast64.go and rank 3 runtime.go were opened for the actual detector. The delivered branches call fatal. A sealed an empty return; a generic recover wrapper would leave the core operation to the adapter. Evidence: `returns.jsonl` row 8; `routes/A/Q03/route.json`; V 18–21; `routes/A/Q03/search_hits.jsonl` for exact per-query positions.

**B.** The common runtime mirror led to Go Spec, a language-reference excerpt rather than a replacement detector. B returned no candidate; common fatal counterevidence is not repaired by generic panic/recover language guidance. Evidence: `returns.jsonl` row 9; `routes/B/Q03/route.json`; V 22.

**Next minimum source:** A version-pinned actual concurrent-map-write detector and official recovery test showing a catchable signal at that branch. Generic recover guidance cannot supply the requested change.

### Q04 — proposal: cmd/compile: ability to export functions as WASM exports

Frozen boundary: **whole**, `judging/frozen-questions.jsonl` row 4.

**C.** Common rank 1 W3C core failed for excessive content length; rank 2 GC core PDF delivered export/memory representation clauses. Go linker/compiler results at ranks 4/6/8/10 were unselected after the two-body cap. The returned standard does not supply a Go ABI or the operational memory-preparation action. Evidence: `returns.jsonl` row 10; `common/Q04/start.json`; V 23–25; D 11.

**A.** Compiler doc.go appeared at search 1 rank 9, but its delivered L0–1239 has no wasmexport. Search 2 ranks 1/5 led to Memory/DataView and an observed setInt32 link. The exact little-endian native-memory preparation partial is supported; whole compiler/export/call integration remains unverified. Evidence: `returns.jsonl` row 11; `routes/A/Q04/route.json`; V 26–31; D 12; `routes/A/Q04/search_hits.jsonl` for exact per-query positions.

**B.** The frozen provider set contains only the two specification providers. The failed W3C body yields no links; the PDF gives an external ACM reference at L1117 and no eligible in-project navigation. With zero new calls, B retains only the non-operational representation contract. Evidence: `returns.jsonl` row 12; `routes/B/Q04/route.json`; V none; D 13.

**Next minimum source:** A delivered version-pinned Go wasmexport implementation/API and end-to-end host export/argument/stack behavior. C/B partial also needs a real native-memory write API; representation clauses alone are insufficient.

### Q05 — Consistent views of namespaces

Frozen boundary: **whole**, `judging/frozen-questions.jsonl` row 5.

**C.** Common ranks 1/6 opened current and 3.11 inspect pages. Returned f_locals attribute tables identify a namespace but do not establish write-through mutation, retained reverse freshness or generator/coroutine/thread resumption behavior; both candidates remain unverified. Evidence: `returns.jsonl` row 13; `common/Q05/start.json`; V 32–34; D 14–15.

**A.** Search 1 rank 2 supplied the versioned 3.13 frame API; observed locals and Reflection links were followed. The builtins attempt did not deliver the locals section. The returned APIs support write-through/freshness fragments but leave partial resumption/thread coverage unverified; whole live-locals and old-C-API requirements conflict with the supplied later contract. Evidence: `returns.jsonl` row 14; `routes/A/Q05/route.json`; V 35–39; D 16; `routes/A/Q05/search_hits.jsonl` for exact per-query positions.

**B.** A tied observed type-reference link led to the data model; a charged expansion delivered the frame section. Write-through alone does not prove immediate freshness of the same retained mapping and the full resumption/thread conjunction; partial and whole stay unverified. Evidence: `returns.jsonl` row 15; `routes/B/Q05/route.json`; V 40–41; D 17.

**Next minimum source:** Same-version retained-proxy freshness and generator/coroutine/thread resumption tests; whole would additionally require truly live locals() and the frozen old/new C API behavior.

### Q06 — Make UTF-8 mode default

Frozen boundary: **partial**, `judging/frozen-questions.jsonl` row 6.

**C.** Common ranks 1/2 opened CPython OS source/rendered manuals. Implicit UTF-8 I/O is documented, but getpreferredencoding is overridden to UTF-8, positively conflicting with the frozen requirement that it remain locale based. Explicit encoding=locale is not established by the returned OS clause. Evidence: `returns.jsonl` row 16; `common/Q06/start.json`; V 42–44; D 18.

**A.** Search 1 ranks 1/6 selected I/O and locale source pages; their delivered responses are scaffold-only according to the route semantic assessments. A returned nothing because common mode behavior already conflicts with getpreferredencoding isolation and the new attempts provide no usable core body. Evidence: `returns.jsonl` row 17; `routes/A/Q06/route.json`; V 45–48; `routes/A/Q06/search_hits.jsonl` for exact per-query positions.

**B.** B followed the observed locale.getpreferredencoding and open links, then located/expanded the open section. Explicit locale decoding is now covered, but the unchanged-getpreferredencoding predicate still conflicts. Replacing it with later getencoding would rewrite the frozen request. Evidence: `returns.jsonl` row 18; `routes/B/Q06/route.json`; V 49–52; D 19.

**Next minimum source:** A same-version mode contract/test retaining locale-based getpreferredencoding under non-UTF-8 locale while default file I/O is UTF-8. Substituting getencoding or choosing a UTF-8-only locale is not a resolution.

### Q07 — Documentation Metadata in Typing

Frozen boundary: **partial**, `judging/frozen-questions.jsonl` row 7.

**C.** Common ranks 1/2 opened CPython typing overview/source. The sole returned overview candidate provides neither the exact documentation carrier constructor nor its original-string attribute/retrieval action; novelty is also unverified. A typing module name is not the carrier operation. Evidence: `returns.jsonl` row 19; `common/Q07/start.json`; V 53–55; D 20.

**A.** Search 1 ranks 1/2 rediscovered typing, rank 3 was the excluded current PEP and rank 5 qualifiers was opened; search 2 rank 1 annotations best practices was opened. These provide Annotated transport/inspection, not a single-string DocInfo-style carrier. A returns empty rather than implement the core carrier in an adapter. Evidence: `returns.jsonl` row 20; `routes/A/Q07/route.json`; V 56–59; `routes/A/Q07/search_hits.jsonl` for exact per-query positions.

**B.** B cannot follow observed typing_extensions or typing.python.org links outside the CPython provider set. Both permitted directory indexes fail; charged known-page lookups deliver Annotated and no DocInfo match. The packet remains empty after two navigation/four body debits; no global absence is claimed. Evidence: `returns.jsonl` row 21; `routes/B/Q07/route.json`; V 60–63.

**Next minimum source:** A versioned supplier single-string carrier constructor, documentation attribute and exact Annotated retrieval/round-trip example; whole adds frozen normalization and symbol association. An outside-provider source would be post-seal, not an original B repair.

### Q08 — Supporting Symlinks in Wheels

Frozen boundary: **whole**, `judging/frozen-questions.jsonl` row 8.

**C.** Current/companion proposals at common ranks 1/2 were excluded; ranks 3/4 opened PyPA wheel and installed-project contracts. Version gating, unpack/spread and RECORD bookkeeping do not supply the frozen same-wheel endpoint/missing-target/cycle validator. Evidence: `returns.jsonl` row 22; `common/Q08/start.json`; V 64–66; D 21–22.

**A.** Search 2 rank 7 Goomba and rank 5 Bazel FilesetOutputTree were read; rank 2 installer.ts yielded scaffold and was not returned. Goomba allows inter-package targets inside a Conda prefix; Bazel tolerates outside-Fileset targets and warns/prunes rather than rejecting the invalid plan. Those policies positively conflict with the frozen wheel validator. Evidence: `returns.jsonl` row 23; `routes/A/Q08/route.json`; V 67–71; D 23–24; `routes/A/Q08/search_hits.jsonl` for exact per-query positions.

**B.** B followed PyPA Specifications and distribution-metadata indexes inside its sole provider. No exact link validator was added; the return repeats surrounding wheel/RECORD contracts. Implementing the missing validator is core work, not residual integration. Evidence: `returns.jsonl` row 24; `routes/B/Q08/route.json`; V 72–73; D 25–26.

**Next minimum source:** A wheel-aware validator with tests for both resolved endpoints confined to this wheel, absent extracted-tree target, cycle and depth overflow, rejecting the whole invalid plan before creation; whole adds LINKS/version/platform/backend/removal integration.

### Q09 — NEP 50 — Promotion rules for Python scalars

Frozen boundary: **partial**, `judging/frozen-questions.jsonl` row 9.

**C.** Common ranks 1/3 opened stable/development NumPy promotion manuals. The returned rules support the frozen partial dtype resolver; whole can_cast coverage is incomplete. Already-named use remains supported rather than being promoted to a new target. Evidence: `returns.jsonl` row 25; `common/Q09/start.json`; V 74–76; D 27–28.

**A.** NumPy promotion was rank 1 in both searches; search 1 rank 6 yielded a PyArray_ResultType locator, and search 2 rank 13 supplied JAX weak-type promotion. Existing decisions support each returned partial candidate separately. Whole typed-scalar can_cast coverage remains unverified; the candidates are not combined. Evidence: `returns.jsonl` row 26; `routes/A/Q09/route.json`; V 77–80; D 29–30; `routes/A/Q09/search_hits.jsonl` for exact per-query positions.

**B.** B followed Array objects and Routines indexes and then dtype references within NumPy. The final promotion/dtype sections retain partial support using common rules; the whole cast-safety requirement remains unverified. Evidence: `returns.jsonl` row 27; `routes/B/Q09/route.json`; V 81–84; D 31.

**Next minimum source:** Whole: a direct supplier can_cast contract/test for the frozen typed-scalar/value-independence example. The partial resolver is already supported.

### Q10 — NEP 47 — Adopting the array API standard

Frozen boundary: **whole**, `judging/frozen-questions.jsonl` row 10.

**C.** Common ranks 1/2 opened SciPy integration and Array API interchange; rank 3 NumPy interoperability was not opened after the cap. Namespace routing and a protocol contract do not establish a concrete producer-to-NumPy-ndarray no-copy operation; SciPy whole input policy also conflicts. Evidence: `returns.jsonl` row 28; `common/Q10/start.json`; V 85–87; D 32–33.

**A.** Search 2 ranks 1/2 supplied NumPy from_dlpack and interoperability examples; an observed link supplied array-api-strict. NumPy interchange supports the partial. Its ordinary ndarray API conflicts with whole dunder-only requirements, while the separate strict wrapper leaves multiple whole clauses unverified; no candidate fusion is permitted. Evidence: `returns.jsonl` row 29; `routes/A/Q10/route.json`; V 88–92; D 34–35; `routes/A/Q10/search_hits.jsonl` for exact per-query positions.

**B.** B is restricted to SciPy and data-apis.org/array-api/. Two standard indexes then array_object and __array_namespace__ remain within that boundary; NumPy, DLPack and sibling strict/compat/extra projects remain excluded. The return supplies interfaces and SciPy routing, not concrete NumPy no-copy exchange, and current whole methods/input policies conflict. Evidence: `returns.jsonl` row 30; `routes/B/Q10/route.json`; V 93–96; D 36–37.

**Next minimum source:** C/B partial: concrete NumPy DLPack producer/consumer and shared-memory/view lifetime documentation. Whole: one implementation/version/configuration supplying every frozen clause without combining unrelated candidates.

### Q11 — NEP 55 — Add a UTF-8 Variable-Width String DType to NumPy

Frozen boundary: **whole**, `judging/frozen-questions.jsonl` row 11.

**C.** Common ranks 1/2 opened the string guide and generic NumPy PDF. Opened evidence supports the partial, but returned string ranges omit L46–50 (Python-string/indexing contract), and the generic PDF return omits exact type/strict-construction passages. Returned partial is unverified by citation omission; whole remains incomplete. Evidence: `returns.jsonl` row 31; `common/Q11/start.json`; V 97–99; D 38–39.

**A.** Search 1 rank 6 added the string C API. The exact StringDType link yields a type-family index with only the name at L104. The returned guide ranges still omit already-opened L46–50, so partial is supported opened but unverified returned. Whole lifetime/growth/cast/serialization evidence is still incomplete. Evidence: `returns.jsonl` row 32; `routes/A/Q11/route.json`; V 100–103; D 40; `routes/A/Q11/search_hits.jsonl` for exact per-query positions.

**B.** The fresh B worker used a fundamentals index, exact type link, PDF locator/expansion and observed thread-safety chapter. Its citations include guide L46–50 plus strict construction, so partial is supported. Whole freeing/lifetime, growth, complete cast matrix, pickle-free serialization and full integration remain unverified. Evidence: `returns.jsonl` row 33; `routes/B/Q11/route.json`; V 104–108; D 41.

**Next minimum source:** C/A partial: include already-delivered string-guide L46–50 with strict construction; original citations remain unchanged. Whole: C lifetime/freeing, supported growth/concurrency, complete cast/ufunc matrix and allow_pickle=False npy/npz tests.

### Q12 — NEP 53 — Evolving the NumPy C-API for NumPy 2.0

Frozen boundary: **partial**, `judging/frozen-questions.jsonl` row 12.

**C.** Common ranks 1/2 opened NumPy C-API source/rendered manuals; downstream-build manuals at ranks 3/4 were unselected. Target macros and import checks do not establish the complete older-default/hiding/baseline-compatibility conjunction; exact header guards are unread. Evidence: `returns.jsonl` row 34; `common/Q12/start.json`; V 109–111; D 42.

**A.** Search 1 rank 1 supplied the downstream package manual, returned with the common version section. Older-default/compatibility evidence improves, but hiding newer struct fields AND functions still lacks direct target guards or negative compile tests. Partial and whole stay unverified. Evidence: `returns.jsonl` row 35; `routes/A/Q12/route.json`; V 112–114; D 43; `routes/A/Q12/search_hits.jsonl` for exact per-query positions.

**B.** Both observed reference/c-api directory links fail. Textual header names and an unlinked downstream reference do not authorize guessed URLs. The returned common target/import sections retain their earlier guard/default/compatibility gaps. Evidence: `returns.jsonl` row 36; `routes/B/Q12/route.json`; V 115–116; D 44.

**Next minimum source:** Same-version numpyconfig.h/ndarraytypes.h and generated C-API target guards, or official negative compile tests proving newer fields and functions hidden without opt-in; C/B additionally need a named older-runtime compatibility contract.

## Provider-boundary cases

**Q04 B:** the two opened specification providers determine its boundary. The W3C fetch yields no body/links; the PDF has only an out-of-boundary ACM reference at L1117. Go linker/compiler entries exist at common ranks 4, 6, 8 and 10 but were not opened into that provider set. B cannot select them. Its zero-call return is a limited specification candidate, not an empty route or a Go export implementation (`common/Q04/start.json`; `routes/B/Q04/route.json` `/selection`; D13).

**Q10 B:** NumPy interoperability is common rank 3, after SciPy and Array API consumed both common body attempts. The allowed providers include SciPy and `/array-api/`, not NumPy, DLPack or the sibling `/array-api-strict/` project. Two index operations plus two API bodies remain interface-level. A independently reaches the concrete NumPy operation and obtains partial support; B cannot inherit that discovery (`common/Q10/start.json`; `routes/B/Q10/route.json` `/selection`; V93–96; D34–37).

**Q07 B:** observed typing_extensions and type-system-provider links are outside the CPython-only boundary. Two permitted indexes fail, Annotated is read, and the DocInfo find returns no matching text. Neither metadata transport nor a provider name supplies the carrier constructor/original-string attribute. A does reach the separate type-qualifiers provider, but it too returns only transport; both packets remain empty (`routes/B/Q07/selection-1.json`; `routes/B/Q07/route.json` `/stop_reason`; V58–63; common D20).

## Names, omitted bodies and omitted citations

A Q04 separates finding a name from receiving its body: compiler doc.go is search-1 rank 9, but delivered L0–1239 has no wasmexport occurrence. The document’s reported total length is not read evidence. A Q11’s exact StringDType link yields only its index name at L104. These attempts do not supply the required whole contracts. Q11’s partial difference is more specific: the needed guide L46–50 was already opened but omitted by C/A; B cites it. That is citation omission, not a claim the supplier lacks the operation (V28, V103/105; D38–41).

Q02 A and Q08 A fail after substantive component reading: the parser and symlink algorithms are real, but semantic conflict detection or root/output policies differ from the frozen use. A familiar name or similar algorithm cannot cure those contradictions; an adapter adding the missing validator would implement the core. Q12 A is incomplete without a positive contradiction: older-default compatibility does not entail every field/function visibility guard (D7–8, D23–24, D43/Q12-P02).

## Receipt limits, score preservation and input hashes

The trace keeps visit flags and route semantic assessments separately. A Q06’s two source responses and A Q08’s installer.ts response have numbered lines and are labeled substantive in `visits.jsonl`, while the route records explicitly assess their original bodies as scaffold-only. The narrative respects that semantic limitation without changing flags/counters. Readable indexes and headings also remain name-only when the target contract is absent. A title, requested URL, numbered wrapper and total_lines never establish missing operational text.

Candidate tokens, original ranks, opened/returned partial/whole verdicts, novelty and predicate evidence are preserved. Next-source recommendations do not rewrite first designs, change scores or add post-seal wins. This audit reads the explicitly assigned integrated candidate-decisions ledger, not reader_2/reader_3 judgment files. The three original reader_1 files and the prior exposure audit were hash-checked unchanged. Only `evidence/failure-trace.jsonl` and `audits/failure-trace.md` were written.

- `judging/frozen-questions.jsonl` — `38816d4705d669eebc09360c1bda64517f392f51536773dba542feb3cfe4b34e`
- `evidence/candidate-decisions.jsonl` — `2d1ff41330f88ac89ddccf6e36d4bfe19328814a86f3cb30cbdfb9171d6b93a0`
- `returns.jsonl` — `3df3481467cbda0a2992cfa798b1558f107759c3accb1a7530491e381b7c73c3`
- `routes.jsonl` — `a2084b74a48426f972567307e58fd3f48ebc5f9e56d137c3ce2f4b17011313d1`
- `visits.jsonl` — `4332205171f8c096af44ee6032c2b27da5938e16e5f91ad6227fd90211b6746c`
