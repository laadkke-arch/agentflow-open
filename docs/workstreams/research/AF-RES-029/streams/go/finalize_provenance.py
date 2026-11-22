#!/usr/bin/env python3
"""Preserve frame traversal, failed recovery, and nonselected first-text exposure."""
import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PREFIX='docs/workstreams/research/AF-RES-029/streams/go/'
questions=[json.loads(line) for line in (ROOT/'questions.jsonl').read_text().splitlines()]
selected={q['number']:q for q in questions}
rows=list(csv.DictReader((ROOT/'frame.csv').open()))
by_number={int(r['number']):r for r in rows}

# Eligibility decisions are made from recovered first text, never current outcomes.
# A filled partial stratum need not be further judged for substantive-text length.
decisions={
56094:('partial','selected','Q01','One sequence-to-discrete-variables assignment operation.','I would like to suggest a language change that can execute dynamic assignments to a list of discrete variables.'),
53468:('partial','excluded_short',None,'A bounded clone operation; two substantive prose sentences and no linked first design.','It would be nice to have `clone` feature instead of manually for/range copying.'),
51259:('partial','partial_quota_already_filled',None,'Adds struct-member access constraints to existing generics; one bounded language capability, not a replacement generics subsystem.','The proposal is to extend the interface/constraint syntax to support struct members.'),
56283:('partial','partial_quota_already_filled',None,'Adds function chaining syntax as a bounded composition operation; diverse examples do not turn it into a multi-operation subsystem.','Provide some way of chaining *functions*, either using a new operator such as `->`, `|>`, or `..` or by using the `.` operator used for calling a method to also call functions.'),
50673:('partial','excluded_short',None,'Two zip-operation problem bullets, fewer than four substantive sentences, with no linked first design.','Can\'t find the zip file size while adding files to the zip.'),
44819:('partial','partial_quota_already_filled',None,'Bounded URL redaction from error strings, configured on existing Client/Error types.','They wanted to log the failure but not with the URL present.'),
43744:('whole','selected','Q02','Complete unit-metadata protocol joins producer format/CLI, parser conflict handling, propagation, direction/statistical semantics and consumer integration.','I propose extending the [Go benchmark format](https://go.googlesource.com/proposal/+/master/design/14313-benchmark-format.md) with a way to specify properties of units.'),
58849:('partial','excluded_short',None,'CSV-writer injection protection is a bounded operation, but the first body has two substantive sentences and only a generic attack-description link, not a linked first design.','The CSV Writer does not provide protection against CSV injection.'),
59416:('partial','excluded_short',None,'String-to-Level conversion is bounded; three substantive prose sentences after excluding the code-introduction sentence and code, with no linked first design.','This is a proposal to add a method for converting a string to a Level.'),
70887:('partial','selected','Q03','One runtime failure branch changes from fatal termination to a recoverable panic; the whole map/request subsystem is not redesigned.','I propose that it be changed to a panic.'),
70897:('undetermined','excluded_initial_unrecoverable',None,'No first body was recovered. The current title suggests bounded struct-field layout optimization, but it is not substituted for initial-purpose coding.',None),
59599:('partial','excluded_short_and_status_only',None,'Two-sentence deprecation-status correction for an existing function; no substantive new operational design or linked first design.','The `reflect.PointerTo` function was added in version 1.18 to replace the `reflect.PtrTo` function.'),
66405:('partial','partial_quota_already_filled',None,'Expose the already matched request pattern through a field/accessor, one bounded observation within HTTP routing.','I suggest we export the `pat` for public access or provide some function to allow user to get the matched pattern, so that we can avoid much logic to use `*ServeMux.Handler` to parse the request again.'),
61256:('partial','partial_quota_already_filled',None,'Change seed generation for repeated test shuffles; one option/operation within the test runner.','This makes sense when the shuffle seed is set explicitly (`-shuffle=X` ) but for random value (`-shuffle=on`) we should generate a new one to increase test order randomness to cover more combinations.'),
60994:('partial','partial_quota_already_filled',None,'Expose one existing core-type computation as a public call.','Make the currently unexported [`coreType()`](https://cs.opensource.google/go/go/+/master:src/go/types/under.go;l=26;drc=59964663e58d60719c707d9d59d7424d6f2ea7e0) implementation in `go/types` exported for everyone to use.'),
60270:('partial','partial_quota_already_filled',None,'Establish one SSH connection through an HTTP proxy using the existing client API; no whole SSH subsystem redesign.','I need to etablish a ssh connexion over a HTTP proxy, and I don\'t find anyway to do it with the current package'),
59780:('partial','partial_quota_already_filled',None,'Supply nine insertion strings to one existing Windows event-log emission operation.','It would be great, if `golang.org/x/sys/windows/svc/eventlog` would support sending events with 9 strings.'),
61870:('partial','partial_quota_already_filled',None,'Expose parent ReaderAt/base position of SectionReader as bounded accessors, not a whole I/O protocol.','I propose exposing the r and base fields of SectionReader to support sendfile.'),
57975:('partial','partial_quota_already_filled',None,'One generic Parse[T] conversion call over the existing strconv functionality.','I\'d like to propose a generic interface to the functionality provided by `strconv`.'),
58678:('undetermined','excluded_initial_unrecoverable',None,'No first body recovered; current title only suggests bounded separator enumeration and cannot establish initial-purpose coding.',None),
61897:('undetermined','excluded_initial_unrecoverable',None,'Current title suggests a potentially whole iterator package, but no initial body was recovered, so it cannot be selected or coded as an eligible whole event.',None),
59205:('undetermined','excluded_initial_unrecoverable',None,'No first body recovered; current title suggests a bounded go.mod configuration option, but initial-purpose coding remains unverified.',None),
67116:('partial','partial_quota_already_filled',None,'Expose a more capable reader return type for the existing ZIP OpenRaw operation, one bounded API change.','Is there a good reason why the function returns `io.Reader` and not `io.NewSectionReader` so we can have more access to the bytes?'),
64493:('partial','partial_quota_already_filled',None,'One error-propagation operator inside the existing language; compiler details do not make it a complete replacement error-handling subsystem.','Add a new operator or use existing token to simplify `if err != nil { return ...(zero values)..., err }` to reduce the codes around error checking, passing and handling.'),
58584:('whole','selected','Q04','Complete interoperability bridge: compiler declaration, linker/instance export table, host argument marshaling and memory/stack boundary, then direct function invocation.','I propose to add some kind of mechanism to mark Go function to be exported in WASM module.')
}

receipt_index={}
if (ROOT/'recovery-receipts.jsonl').exists():
    for line in (ROOT/'recovery-receipts.jsonl').read_text().splitlines():
        old=json.loads(line);receipt_index[old['receipt_filename']]=old
for path in sorted((ROOT/'receipts').glob('*.json')):
    if path.name.endswith('-event.json'):
        continue
    receipt=json.loads(path.read_text())
    # Reduce an early schema diagnostic: only comment edit timestamps/keys were
    # displayed; no comment bodies or outcome fields were displayed.
    if 'edit_node_schema_debug' in receipt:
        receipt['schema_debug_exposure']={'comment_edit_metadata_nodes':len(receipt.pop('edit_node_schema_debug')),
            'body_or_outcome_text_displayed':False}
        receipt['later_timeline_fields_read_by_model']='edit-metadata schema only; no substantive comment fields'
    receipt['receipt_filename']=path.name
    if receipt.get('result')=='initial_opened_event_recovered' and int(receipt['canonical_id'].split('#')[1]) not in selected:
        receipt['capture_after_compaction']='nonselected-initial-captures.jsonl, keyed by canonical_id/event_id'
        receipt['original_individual_capture_files_removed_after_consolidation']=True
    receipt_index[path.name]=receipt
all_receipts=[receipt_index[name] for name in sorted(receipt_index)]

recovered={}
for r in all_receipts:
    if r.get('result')=='initial_opened_event_recovered':
        number=int(r['canonical_id'].split('#')[1]); recovered[number]=r

traversal=[]
for row in rows:
    number=int(row['number'])
    if number not in decisions: continue
    boundary,decision,qid,reason,purpose=decisions[number]
    r=recovered.get(number)
    item={**{k:row[k] for k in ['canonical_id','period','period_order','sha256_order_key','first_public_date','url']},
        'current_title_at_frame':row['title'],'initial_title':r.get('title_at_open') if r else None,
        'title_renamed_since_open':r['title_at_open']!=row['title'] if r else None,
        'whole_or_partial':boundary,'decision':decision,'question_id':qid,'reason':reason,
        'initial_purpose_excerpt':purpose,'initial_purpose_excerpt_kind':'verbatim or explicitly shortened first-text purpose, not current body' if purpose else None,
        'initial_body_sha256':r.get('initial_body_sha256') if r else None,
        'initial_event_id':r.get('event_id') if r else None,
        'recovery_receipts':[x['receipt_filename'] for x in all_receipts if x.get('canonical_id')==row['canonical_id']],
        'recovery_receipt_lookup':'recovery-receipts.jsonl, keyed by receipt_filename',
        'outcome_used':False}
    traversal.append(item)
(ROOT/'traversal.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in traversal))
(ROOT/'recovery-receipts.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in all_receipts))

nonselected=[]
extra_exposures=[]
previous_captures={}
if (ROOT/'nonselected-initial-captures.jsonl').exists():
    previous_captures={json.loads(line)['canonical_id']:json.loads(line) for line in (ROOT/'nonselected-initial-captures.jsonl').read_text().splitlines()}
for number,r in sorted(recovered.items(),key=lambda pair:(by_number[pair[0]]['period'],int(by_number[pair[0]]['period_order']))):
    if number in selected: continue
    event_path=ROOT/r['event_capture_file']
    if event_path.exists():
        event=json.loads(event_path.read_text());issue=event['payload']['issue']
    else:
        issue={'body':previous_captures[r['canonical_id']]['body']}
    meta=by_number[number]
    text_read='first 5000 decoded characters' if number in [51259,56283] else 'full initial body'
    nonselected.append({'canonical_id':r['canonical_id'],'event_id':r['event_id'],'archive_url':r['archive_url'],
        'event_created_at':r['event_created_at'],'issue_created_at':r['issue_created_at'],
        'issue_updated_at_at_capture':r['issue_updated_at_at_capture'],'initial_title':r['title_at_open'],
        'body':issue.get('body') or '', 'body_sha256':r['initial_body_sha256'],
        'read_extent':text_read,'counted':False,'reason':'Not one of the four selected Go events.'})
    if number not in decisions:
        extra_exposures.append({'canonical_id':r['canonical_id'],'period':meta['period'],'period_order':int(meta['period_order']),
            'initial_title':r['title_at_open'],'read_extent':text_read,
            'why':'Batch recovery/read overshot the eventual stopping point while whole-boundary coding or prior-candidate recovery was unresolved.',
            'selection_use':'None: quota filled at early rank 7 and late rank 18; extras do not replace the frozen-order selected event.',
            'outcome_or_later_comment_read':False})
(ROOT/'nonselected-initial-captures.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in nonselected))

exposures=[
    {'kind':'current_titles_in_metadata_frame','detail':'All 2,841 current issue titles/date/IDs were enumerated; only prefixes were printed. Current titles can have been renamed. Canonical issue IDs, not titles, determine the hash order. Initial titles and purpose govern selected-event coding.','outcome_or_later_comment_read':False},
    {'kind':'uninspected_broad_api_payload','detail':'REST issue-search responses contain body/state/labels but were programmatically reduced to metadata before display. Full unrelated responses were not committed; their response hashes and public restoration URLs are retained.','outcome_or_later_comment_read':False},
    {'kind':'issue_html_schema_probe','detail':'The schema probe printed keys and lastEditedAt timestamps of comment nodes before the initial Issue node was identified; no comment bodies or outcome fields were displayed. Initial Issue lacks lastEditedAt, so no unedited-body claim was made.','outcome_or_later_comment_read':False},
    {'kind':'web_open_recovery','detail':'Two current issue pages (#56094/#58849) were opened for initial-version metadata. The model saw only page titles/navigation starts and filtered opening-date/header lines; current bodies and later comments were withheld. Neither page is counted as recovered first text.','outcome_or_later_comment_read':False},
    {'kind':'official_proposal_tree_metadata','detail':'The golang/proposal tree at 83ee2aaf9fdcc1a1cf4bb4d20216fc979635cf04 was enumerated as a possible earliest-blob fallback. Filenames and blob hashes, including out-of-window names, were displayed; no design bodies or acceptance fields were read. It did not set the sample.','outcome_or_later_comment_read':False},
    {'kind':'researcher_boundary_clarification','detail':'The integration worker clarified whole as multi-operation subsystem or complete protocol with integration; confirmed benchmark metadata and Go/WASM bridge boundaries from their initial purpose. This is coding clarification, not proposal acceptance/outcome evidence.','outcome_or_later_comment_read':False},
    {'kind':'batch_overshoot','events':extra_exposures,'outcome_or_later_comment_read':False}
]
(ROOT/'exposures.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in exposures))

# Keep the frozen full frame, plus append-only interpretation columns. Rebuilding
# frame.csv from the metadata snapshot restores ordering; re-running this script
# restores the observed first-title/traversal columns.
extra_cols=['current_title_at_frame','initial_title','initial_purpose_excerpt','purpose_recovery_status','sampling_decision']
for row in rows:
    number=int(row['number']);r=recovered.get(number);d=decisions.get(number)
    row['current_title_at_frame']=row['title']
    row['initial_title']=r['title_at_open'] if r else ''
    row['initial_purpose_excerpt']=d[4] or '' if d else ''
    row['purpose_recovery_status']='initial_opened_event_recovered' if r else ('recovery_attempt_failed' if d else 'not_read_after_stratum_quota')
    row['sampling_decision']=d[1] if d else ('extra_first_text_exposure_not_selected' if r else 'not_traversed_after_stratum_quota')
with (ROOT/'frame.csv').open('w',newline='') as stream:
    fields=list(rows[0]);writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(rows)

sources=[json.loads(line) for line in (ROOT/'sources.jsonl').read_text().splitlines() if json.loads(line).get('question_id') in {q['question_id'] for q in questions}]
for capture in nonselected:
    number=int(capture['canonical_id'].split('#')[1]);r=recovered[number];decision=decisions.get(number)
    sources.append({'source_id':f'GO-NONSELECTED-{number}','type':'nonselected_initial_design_capture',
        'publisher':f"{r['author_login']} on official golang/go; capture by GHArchive",'url':by_number[number]['url'],
        'archive_url':r['archive_url'],'version':f"GitHub IssuesEvent {r['event_id']} action=opened",'date':r['issue_created_at'],
        'checked_utc':r['checked_utc'],'read_sections':[capture['read_extent']],
        'finding':decision[3] if decision else 'Extra initial-text exposure after eventual cell stopping point; not used to select a later event.',
        'limitations':['Third-party opening-event mirror; native edit history not recovered.','Excluded/nonselected; not part of the four-event original-content count.'],
        'question_id':None,'duplicate_group':f"golang-go-{number}-opened-{r['event_id']}",'counted':False,
        'body_sha256':r['initial_body_sha256'],'capture_file':PREFIX+'nonselected-initial-captures.jsonl'})
for number,d in decisions.items():
    if number in recovered: continue
    attempts=[r for r in all_receipts if r.get('canonical_id')==by_number[number]['canonical_id']]
    sources.append({'source_id':f'GO-RECOVERY-FAIL-{number}','type':'initial_version_recovery_attempt_only',
        'publisher':'GitHub and GHArchive','url':by_number[number]['url'],'version':'Unrecovered initial body; creation-hour/adjacent-hour archive attempts retained',
        'date':by_number[number]['first_public_date'],'checked_utc':max((r['checked_utc'] for r in attempts),default=None),
        'read_sections':['Matching event metadata search only; no first body read.'],'finding':d[3],
        'limitations':['An inaccessible/missing initial source is not evidence that no design existed.','Current body/title are not silently substituted.'],
        'question_id':None,'duplicate_group':f'golang-go-{number}-recovery-attempts','counted':False,
        'receipt_file':PREFIX+'recovery-receipts.jsonl'})
sources.append({'source_id':'GO-FRAME','type':'official_ledger_metadata','publisher':'GitHub / golang/go',
    'url':'https://github.com/golang/go/issues?q=is%3Aissue+label%3AProposal+created%3A2021-01-01..2024-12-31',
    'version':'30 annual REST search pages, 100 items/page, current Proposal label, 2026-11-22 retrieval',
    'date':'2026-11-22','checked_utc':'2026-11-22','read_sections':['title, creation timestamp, canonical issue number, URL; no state/comment bodies'],
    'finding':'2,841 distinct issues, 1,203 early-period and 1,638 late-period, exact SHA-256 traversal preserved.',
    'limitations':['Current Proposal label membership; removed historical labels are not reconstructed.','Current titles may differ from opening titles; initial titles are separately preserved for recovered candidates.'],
    'question_id':None,'duplicate_group':'go-frame-metadata-20261122','counted':False})
(ROOT/'sources.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in sources))

metadata_path=ROOT/'frame-metadata.json'
if metadata_path.exists():
    payload=metadata_path.read_bytes()
    (ROOT/'frame-metadata.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    (ROOT/'metadata-snapshot-manifest.json').write_text(json.dumps({'file':'frame-metadata.json.gz','uncompressed_sha256':hashlib.sha256(payload).hexdigest(),
        'uncompressed_bytes':len(payload),'rows':2841,'role':'Frozen original metadata, before eligibility coding; decompress to reproduce build_frame.py.'},indent=2)+'\n')

print(json.dumps({'selected':len(questions),'traversed':len(traversal),'early_prefix':7,'late_prefix':18,
    'nonselected_initial_captures':len(nonselected),'extra_first_text_exposures':len(extra_exposures),
    'sources_counted':sum(s['counted'] for s in sources),'outcome_used':False}))
