#!/usr/bin/env python3
"""Serialize the AF-RES-029 Go initial-text sample before any supplier search."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREFIX = 'docs/workstreams/research/AF-RES-029/streams/go/'

def pred(identifier, requirement, sections, falsifier, inherited=None):
    value = {'predicate_id': identifier, 'requirement': requirement,
             'source_sections': sections, 'falsifying_input': falsifier}
    if inherited:
        value['inherited_from_whole'] = inherited
    return value

def section(identifier, heading, start, end):
    return {'section_id':identifier, 'heading':heading, 'line_start':start, 'line_end':end}

questions = [
    {
        'question_id':'Q01', 'number':56094, 'whole_or_partial':'partial',
        'boundary_reason':'One bounded destructuring assignment operation within the Go language; it does not replace a multi-operation language subsystem.',
        'caller':'A Go developer processing optional heterogeneous arguments in NewExtParam(value interface{}, opts ...interface{}).',
        'input':'An array or variadic sequence; concrete initial example is opts ...interface{}, plus an ordered list of destination variables.',
        'output':'Separate destination variables receive available sequence values from left to right; destinations past the input length receive a null/nil value.',
        'limits':['Only the initial heterogeneous options example and stated array/variadic boundary are fixed. The text does not resolve the static type of a missing value for every possible typed array.', 'Extra source elements do not require extra destinations; only specified destinations are assigned.', 'The long strconv/type-switch example illustrates existing caller processing, not a requirement that the supplier perform numeric parsing.', 'No speed target, concurrency guarantee, general pattern matching or generics requirement is supplied.'],
        'source_sections':[section('Q01-S1','Proposal: requested assignment and existing processing example',24,82),section('Q01-S2','Destructuring and null-check example',83,103),section('Q01-S3','Assignment mechanics',109,115),section('Q01-S4','Costs and named PHP list analogy',127,133)],
        'original_named_families':['Go','PHP','VB','C#'],
        'original_named_components':['NewExtParam','opts ...interface{}','strconv.ParseInt','type assertion','map second result','PHP list'],
        'template_named_components':['vet','gopls','gofmt','goimports'],
        'named_component_roles':{'PHP list':'Explicit existing analogy for the same value-retrieval use; rediscovery is not a new target.','VB/C#':'Author-background knowledge, not supplier requirements.','strconv.ParseInt':'Existing downstream type conversion, outside the destructuring action.'},
        'whole_must':[
            pred('Q01-W1','Provide a Go-level array/variadic destructuring assignment that binds separate destination variables without caller-written per-element length/index checks.',['Q01-S1','Q01-S2'],'In a Go function with opts=[]interface{}{7,"x"}, attempting a three-variable destructuring still requires the caller to implement len(opts) checks and opts[i] extraction.'),
            pred('Q01-W2','Assign the supplied destinations in left-to-right source order, and do not require more destinations than the caller specified.',['Q01-S3'],'Input [10,20,30] with two destinations produces (20,10), rejects the unused third value, or requires a third destination.'),
            pred('Q01-W3','For the heterogeneous options boundary, produce nil/null for a destination beyond the source length so the caller can test it.',['Q01-S2','Q01-S3'],'Input [10] with three interface-valued destinations panics, rejects the arity mismatch, or yields non-null fabricated values in positions two and three.')
        ],
        'partial_must':[
            pred('Q01-P1','Extract an ordered fixed-width group of values from an array/variadic-like sequence without the caller implementing individual element extraction.',['Q01-S1','Q01-S2','Q01-S3'],'For [10,20,30] and width two, the component only exposes raw indexing and requires the adapter to implement the extraction loop.',['Q01-W1','Q01-W2']),
            pred('Q01-P2','Preserve left-to-right values, truncate unused trailing source positions, and pad missing heterogeneous positions with null/nil.',['Q01-S2','Q01-S3'],'For input [10] and width three the result is not (10,null,null), or for [10,20,30] and width two it rejects rather than returning the first two values.',['Q01-W2','Q01-W3'])
        ],
        'independent_partial_purpose':'Prepare a fixed-width, null-padded tuple of optional argument values for validation before Go language syntax is integrated.',
        'independently_useful_next_action':'The caller can check the three extracted option positions for nil and perform the existing per-type processing.',
        'remaining_adapter':'Bind the prepared positions to Go variables and integrate any new compiler syntax/type rules; retain caller-specific numeric/type conversions. An adapter that implements sequence extraction or missing-value padding itself does not establish partial completion.',
        'preferences':['The example syntax is sz, sc, pr := opts...; punctuation is an illustrated syntax preference, while the assignment semantics are mandatory.','Less code clutter and easier understanding are motivations, not measured performance predicates.'],
        'false_same_name_criterion':'A list API that appends values, enumerates variable names, or returns a string representation does not perform ordered destructuring with missing-position nulls, even if it is named list/unpack.',
        'neutral_query':'array variadic destructuring assign variables left to right missing elements null',
        'a_queries':['array destructuring fixed number variables missing values null extra elements','variadic arguments unpack optional values null padding assignment']
    },
    {
        'question_id':'Q02', 'number':43744, 'whole_or_partial':'whole',
        'boundary_reason':'A complete benchmark-unit metadata protocol spanning producers, in-band and command-line representations, parser conflict handling, forward propagation, consumer direction/statistical semantics and tool integration.',
        'caller':'A benchmark producer and a consumer/comparison tool such as benchstat handling custom measurement units.',
        'input':'Benchmark results plus unit-name/key/value metadata supplied in the result stream or through a command-line flag.',
        'output':'A consistent per-unit interpretation of beneficial direction and statistical assumptions, applied to subsequent benchmark measurements; conflicting properties produce an error.',
        'limits':['Behavior for benchmark results preceding a unit declaration is explicitly unspecified.', 'Streaming consumers must not be forced to buffer all results merely in case a later property appears.', 'Normal-distribution support is deliberately omitted; no such mandatory requirement may be added.', 'The author expresses no strong opinion on exact syntax; Unit/key=value and -unit are concrete proposed representations, not an exclusive punctuation requirement.'],
        'source_sections':[section('Q02-S1','Motivation: custom unit properties and benchstat',1,1),section('Q02-S2','In-band and CLI representations and alternatives',3,12),section('Q02-S3','Conflict error and forward propagation',14,16),section('Q02-S4','Direction and statistical semantics',18,22),section('Q02-S5','Default-unit and exact-size examples',24,27)],
        'original_named_families':['Go benchmark format','Go testing package','benchstat'],
        'original_named_components':['Unit metadata record','-unit flag','Benchmark result line','higher/lower=better/worse','assume=nothing/exact','ns/op','MB/s','text-bytes'],
        'named_component_roles':{'benchstat':'Explicit intended consumer family; returning benchstat itself is already named, while a distinct previously unnamed component inside that family must be separately identified.','Go benchmark format':'Explicit existing format; the linked older format proposal is prior context, not this sampled event.'},
        'whole_must':[
            pred('Q02-W1','Carry per-unit key/value properties through both benchmark-stream declarations and an equivalent tool command-line configuration, and expose them to benchmark consumers.',['Q02-S1','Q02-S2'],'A custom text-bytes property supplied through a CLI option cannot reach the comparison tool, or only an unrelated benchmark-name tag is produced.'),
            pred('Q02-W2','Reject conflicting properties specified for the same unit.',['Q02-S3'],'The same unit is declared higher=better and lower=better, and the consumer silently accepts both or overwrites one without an error.'),
            pred('Q02-W3','Apply a declaration to all following benchmark results with that unit; allow streaming without requiring retrospective buffering.',['Q02-S3'],'After a custom-unit declaration, a later result uses no property or a different property, or the parser cannot emit earlier results until end of input.'),
            pred('Q02-W4','Support all four higher/lower combined with better/worse formulations and interpret beneficial direction consistently.',['Q02-S4'],'higher=better and lower=worse are treated as opposite meanings, or one of the four allowed forms is rejected.'),
            pred('Q02-W5','Support assume=nothing and assume=exact with nothing as default; nothing uses nonparametric treatment and exact does not require repeated sampling to increase confidence.',['Q02-S4','Q02-S5'],'An omitted assumption forces a normal model, or a file-size unit marked exact is rejected for lacking repeated samples.')
        ],
        'partial_must':[
            pred('Q02-P1','Parse a unit declaration/configuration into a unit-keyed property record usable by a benchmark tool.',['Q02-S2'],'Unit text-bytes lower=better assume=exact yields only raw text and requires the adapter to implement the unit/property parser.',['Q02-W1']),
            pred('Q02-P2','Normalize all four direction forms and the nothing/exact assumptions, preserving nothing as the default.',['Q02-S4'],'lower=worse is not recognized as larger-is-better, or omitting assume does not produce the nothing/default interpretation.',['Q02-W4','Q02-W5']),
            pred('Q02-P3','When merging declarations for one unit, signal contradictory properties as an error.',['Q02-S3'],'Merging higher=better with lower=better for ns/op silently succeeds.',['Q02-W2'])
        ],
        'independent_partial_purpose':'Validate and normalize benchmark-unit declarations into a usable per-unit metadata map before integrating them with a complete result stream and comparison UI.',
        'independently_useful_next_action':'A benchmark consumer can inspect the normalized direction/assumption map, reject conflicts, then use it when interpreting subsequent results.',
        'remaining_adapter':'Connect normalized records to the CLI and stream producers, apply them to following benchmark records, and wire their meanings into statistical/reporting consumers. If the adapter must implement the property parser, normalization or conflict rule, the component has not completed the partial action.',
        'preferences':['Unit and -unit key=value spellings are proposed concrete syntax; alternative equally expressive spellings are not automatically conflicts.','Built-in examples ns/op lower=better and MB/s higher=better illustrate expected defaults; no universal fixed list of units is specified.'],
        'false_same_name_criterion':'A physical-unit conversion API that converts metres to feet, or a test-runner unit label, does not supply benchmark direction/assumption metadata or conflict/propagation semantics.',
        'neutral_query':'benchmark result unit metadata higher lower better statistical assumptions exact nonparametric',
        'a_queries':['benchstat custom benchmark unit properties higher lower better assume exact','benchmark unit metadata key value parser conflicting properties command line streaming']
    },
    {
        'question_id':'Q03', 'number':70887, 'whole_or_partial':'partial',
        'boundary_reason':'A bounded change to the concurrent-map-write failure branch within the runtime; it does not redesign the map subsystem or the request-serving protocol.',
        'caller':'A Go runtime map-assignment path and an application/API request handler that has a recovery boundary.',
        'input':'A map write attempted while the runtime concurrent-write detection condition is true; initial code uses h.flags & hashWriting in mapassign_fast64.',
        'output':'A catchable panic for the detected concurrent map write, enabling a recovery boundary to contain the failure and respond to the affected request instead of immediately terminating the service.',
        'limits':['The author acknowledges correct map access should use a mutex; this request concerns handling a detected misuse, not making unsynchronized maps safe.', 'The first text does not establish memory safety or map integrity after a race. Such guarantees must not be inferred.', 'The cited 90% preference is the proposer’s claim, not a measured acceptance criterion.', 'No behavior is specified for concurrent races the existing detector misses.'],
        'source_sections':[section('Q03-S1','Proposal details and fatal-to-panic change',1,18),section('Q03-S2','Containment and HTTP 500 purpose',20,20),section('Q03-S3','With/without recover compatibility statement',22,24)],
        'original_named_families':['Go runtime','Go map implementation'],
        'original_named_components':['mapassign_fast64','maptype','hmap','h.flags & hashWriting','fatal','panic','plainError','recover','mutex','HTTP 500','raceenabled','getcallerpc','racewritepc','abi.FuncPCABIInternal','unsafe.Pointer'],
        'named_component_roles':{'panic/recover':'Already explicit mechanism; merely rediscovering generic panic/recover documentation is not a new implementation of the requested map-detector behavior.','mapassign_fast64':'Exact actor shown in the first draft; generic application error wrappers do not replace this runtime branch.'},
        'whole_must':[
            pred('Q03-W1','At the runtime concurrent-map-write detection branch, signal panic instead of an uncatchable fatal termination.',['Q03-S1'],'The hashWriting overlap branch still calls fatal, while only nil-map writes or unrelated application errors panic.'),
            pred('Q03-W2','Allow a valid recovery boundary to catch that specific concurrent-map-write panic and keep the process available.',['Q03-S2','Q03-S3'],'A request handler with an applicable recover boundary still loses the whole service when the detector reports concurrent map writes.'),
            pred('Q03-W3','Preserve a failing/terminating path for code without a recovery boundary while permitting the recovering API caller to produce an error response such as HTTP 500.',['Q03-S2','Q03-S3'],'Without recover the invalid write silently succeeds, or with recover the API cannot finish the affected request with an error response.')
        ],
        'partial_must':[
            pred('Q03-P1','Provide the actual map-detector-to-catchable-signal path for detected overlapping writes, rather than a generic panic helper outside the detector.',['Q03-S1'],'The component only offers recover() or an exception wrapper; Go’s concurrent-map-write branch still terminates via fatal.',['Q03-W1']),
            pred('Q03-P2','Demonstrate that the resulting signal can be caught at an appropriate recovery boundary without mandatory immediate process termination.',['Q03-S2','Q03-S3'],'The component reports a concurrent-write error by process exit or an uncatchable runtime failure.',['Q03-W2'])
        ],
        'independent_partial_purpose':'Contain the detected map-write failure as a recoverable runtime signal before adding request-specific response handling.',
        'independently_useful_next_action':'The application recovery boundary can log/translate the caught signal and finish the affected request with an error response.',
        'remaining_adapter':'Integrate the verified detector behavior into the target Go runtime/version and wire the application recovery boundary to request cleanup/HTTP error reporting. A generic wrapper that leaves fatal unchanged forces the adapter to implement the core action and fails partial completion.',
        'preferences':['HTTP 500 is the stated example of request containment, not a requirement for a particular web framework.','No requirement to restore a raced map to a valid state is invented.'],
        'false_same_name_criterion':'A function named Panic or Recover operating on ordinary returned errors or nil-map writes has the wrong triggering input/actor if concurrent-map-write detection still invokes fatal.',
        'neutral_query':'Go concurrent map writes runtime fatal recoverable panic request recovery',
        'a_queries':['Go runtime concurrent map writes change fatal panic recover','Go map concurrent write detection catch panic HTTP request recovery']
    },
    {
        'question_id':'Q04', 'number':58584, 'whole_or_partial':'whole',
        'boundary_reason':'An integrated Go-to-WebAssembly interoperability protocol: compiler export declaration, linker/instance export table, host-native argument preparation through memory/stack, and invocation across that boundary.',
        'caller':'A Go developer exposing a function and a JavaScript/WebAssembly host invoking the compiled function.',
        'input':'A Go function selected for export in a GOOS=js GOARCH=wasm build, a compiled module with its memory/stack interface, and native argument values; the concrete example is Bar(id int).',
        'output':'A directly exported WebAssembly instance symbol that the host can invoke after placing native values into the Go stack, with the Go function receiving the intended argument.',
        'limits':['The first text targets the js/wasm environment and does not require a standalone WASI environment.', 'The proposed compiler marker may be a directive or an instruction; exact //go:wasmexport spelling is an example.', 'Memory allocator access for strings/slices is mentioned as possibly needed, not a fully specified mandatory allocator API.', 'The abstract example’s stack offset and internal names are illustrative ABI details; no stable ABI guarantee is stated.', 'No numeric performance threshold or universal Go-type marshaller is required.'],
        'source_sections':[section('Q04-S1','Background and existing global/js.Value restriction',1,18),section('Q04-S2','Mark functions and publish direct instance exports',20,24),section('Q04-S3','Calling exports and memory/stack preparation',26,31),section('Q04-S4','Go and JavaScript abstract example',33,59)],
        'original_named_families':['Go','WebAssembly','JavaScript','Wasmer'],
        'original_named_components':['GOOS=js GOARCH=wasm','window/globalThis','wasm_exec.js','wasm_export_resume','js.Value','//go:wasmexport','CallImport','WebAssembly instance exports','DataView','DataView.setInt32','getsp','mem','foo·Bar','go._inst.exports','Bar(id int)','fmt.Println'],
        'named_component_roles':{'Wasmer':'Explicit original background export/import reference; a returned Wasmer component needs novelty coding within this named family.','DataView.setInt32':'Explicitly shown as the native integer argument-preparation component; rediscovery for this same use is already named.','wasm_exec.js':'Existing bridge context; a generic JS callback wrapper alone does not satisfy direct export requirements.'},
        'whole_must':[
            pred('Q04-W1','Provide a mechanism in the Go build/toolchain to select a Go function for a direct WebAssembly export.',['Q04-S2','Q04-S4'],'The only supported path wraps the function in js.Func/js.Value and attaches it to globalThis; the compiler cannot emit a selected direct export.'),
            pred('Q04-W2','Publish the selected function as a host-addressable WebAssembly instance export alongside the module’s built-in exports.',['Q04-S2','Q04-S4'],'The host can locate only built-in bridge symbols or a JavaScript global, not the selected Go function in the instance export table.'),
            pred('Q04-W3','Permit the host to prepare native argument values through the module’s Go memory/stack boundary, rather than limiting every argument to a wrapped js.Value.',['Q04-S1','Q04-S3','Q04-S4'],'For Bar(123), the host can pass only js.Value references, cannot reach the target stack memory, or writes an unrelated copy invisible to the Go function.'),
            pred('Q04-W4','Support invoking the directly exported function after argument preparation so the Go function observes the intended native value.',['Q04-S3','Q04-S4'],'After placing integer 123 into the designated argument slot, invoking the export does not call Bar or Bar observes a different/uninitialized value.')
        ],
        'partial_must':[
            pred('Q04-P1','Write a supplied native 32-bit integer at a caller-specified byte offset in a view of WebAssembly linear memory using the example’s little-endian representation.',['Q04-S3','Q04-S4'],'Given value 0x01020304 and a valid offset, the component cannot produce bytes 04 03 02 01 at that offset without the adapter implementing byte encoding/writing.',['Q04-W3']),
            pred('Q04-P2','Mutate the same memory buffer visible to the executing WebAssembly/Go module, so the prepared argument can be consumed by the subsequent export call.',['Q04-S3','Q04-S4'],'The memory-writing operation changes a detached copy or ordinary JS object, leaving the module’s designated stack argument bytes unchanged.',['Q04-W3','Q04-W4'])
        ],
        'independent_partial_purpose':'Prepare the integer argument bytes for an already exported low-level function in the module’s memory, an independently usable host-side step before invoking that function.',
        'independently_useful_next_action':'Once the stack argument slot contains the intended integer bytes, the host can invoke an already known direct export.',
        'remaining_adapter':'Implement/choose the Go export declaration and linker integration, obtain the export and stack pointer, select the ABI-correct offset, and invoke the function. The adapter may choose addresses but must not implement the component’s core integer encoding/memory write. A memory writer alone does not satisfy the whole Go-export protocol.',
        'preferences':['Compiler directive //go:wasmexport and foo·Bar naming are illustrative choices.','Allocator access for complex strings/slices remains an open integration issue in this first text.'],
        'false_same_name_criterion':'An export keyword that exports JavaScript module bindings, or a data-view API that formats values for display, has the wrong actor/output; neither emits a Go WebAssembly function nor writes its shared linear-memory argument slot.',
        'neutral_query':'Go WebAssembly export functions native values host memory stack calling exports',
        'a_queries':['Go WebAssembly direct function exports JavaScript stack memory native integer arguments','WebAssembly linear memory DataView setInt32 little endian exported function arguments']
    }
]

frame = list(csv.DictReader((ROOT/'frame.csv').open()))
by_number = {int(row['number']):row for row in frame}
sources=[]
for q in questions:
    number=q['number']; meta=by_number[number]
    r=json.loads((ROOT/f'receipts/{number}-archive-recovery.json').read_text())
    body=(ROOT/r['initial_body_file']).read_bytes()
    assert hashlib.sha256(body).hexdigest()==r['initial_body_sha256']
    q.update({'ledger':'go','canonical_id':meta['canonical_id'],'period':meta['period'],
        'period_order':int(meta['period_order']),'sha256_order_key':meta['sha256_order_key'],
        'title':r['title_at_open'],'current_title_at_frame':meta['title'],
        'initial_timestamp':r['issue_created_at'],'initial_url':meta['url'],
        'fixed_version':f"GitHub IssuesEvent {r['event_id']} action=opened; archive generation {r['archive_headers']['x-goog-generation']}",
        'initial_text_file':PREFIX+r['initial_body_file'],'initial_text_sha256':r['initial_body_sha256'],
        'initial_recovery_receipt':PREFIX+f'receipts/{number}-archive-recovery.json',
        'initial_event_capture':PREFIX+r['event_capture_file'],
        'initial_recovery_method':'Original GitHub public opened-event payload captured by third-party GHArchive; selected exact repository, issue number, action and creation timestamp.',
        'initial_recovery_limitations':['Native GitHub edit history was not recovered.','The archive is a third-party capture of official author content, not an official Golang-hosted immutable design blob.','The matched opened event has issue.created_at == issue.updated_at == event.created_at; current body is not used as first-version proof.'],
        'initial_body_read':'full exact initial body read from local captured file; source section ranges use decoded line order',
        'mandatory_preference_distinction':'Only whole_must/partial_must are mandatory; preferences and unspecified limits are not promoted to requirements.',
        'searches_performed':False,'routes_started':False,
        'source_id':f"GO-{q['question_id']}-INITIAL"})
    sources.append({'source_id':q['source_id'],'type':'original_design_content_in_third_party_opened_event_capture',
        'publisher':f"{r['author_login']} on official golang/go issue ledger; captured by GHArchive",
        'url':meta['url'],'archive_url':r['archive_url'],'version':q['fixed_version'],
        'date':r['issue_created_at'],'checked_utc':r['checked_utc'],
        'read_sections':[s['section_id'] for s in q['source_sections']],
        'finding':q['boundary_reason'],'limitations':q['initial_recovery_limitations'],
        'question_id':q['question_id'],'duplicate_group':f"golang-go-{number}-opened-{r['event_id']}",
        'counted':True,'counting_basis':'One initial author design event; GitHub page, local body and GHArchive mirror are one original-content group.',
        'original_body_read':True,'body_sha256':q['initial_text_sha256'],'body_file':q['initial_text_file'],
        'recovery_receipt':q['initial_recovery_receipt']})

(ROOT/'questions.jsonl').write_text(''.join(json.dumps(q,ensure_ascii=False)+'\n' for q in questions))
(ROOT/'sources.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in sources))
print(json.dumps({'questions':len(questions),'selected':[q['canonical_id'] for q in questions],
                  'all_initial_hashes_match':True,'supplier_searches':0}))
