import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
SHA = '0898bdf3fc0f9f3fbf78336bad21d5506e19c118'
REPO = 'https://github.com/mltframework/shotcut'

def blob(path, first=None, last=None):
    return f'{REPO}/blob/{SHA}/{path}' + (f'#L{first}' + (f'-L{last}' if last else '') if first else '')

decisions = {
    873: ('exclude', None, 'Title is Proxy mode, but current body is empty. No body-level author goal, observed behavior, or version evidence; PR patch deliberately not read.'),
    880: ('exclude', '20.04.12 (installer filename shotcut-win64-200412.exe)', 'Subtitle editing becomes slow and memory-intensive; no restoration of original/proxy relationship.'),
    908: ('exclude', '20.07.11 from Flatpak', 'UI says proxies are in use but project proxy directory is not populated. Proxy creation failure, without restoration or moved-original relationship.'),
    910: ('auxiliary_only', '20.09.13 on Windows 10', 'External resize and same-name replacement yields black timeline while Source plays; removing proxies did not help. No moved originals, distinct-folder basename collision, or explicit restoration of original/proxy relationship.'),
    914: ('exclude', '20.09.13', 'Size and position animation is shown in Shotcut but absent from export; no original/proxy restoration.'),
    923: ('exclude', '20.09.27 on Windows 10 Home 1909', 'QSV encoder is not used for proxy generation while export is okay; encoder selection, not association restoration.'),
    942: ('exclude', '20.09 (20.09.27)', 'macOS crash report. Inspected crash header and all body lines matching proxy/relink/original/moved/folder; matches are system stack/library names, not a media-restoration goal.'),
    987: ('exclude', '20.11.28 on Windows 10 Pro 2004', 'About one second freezes after a cut, also after export; reproduction explicitly uses no proxy.'),
    988: ('exclude', '20.11.28 on Windows 10 Pro 2004', 'Convert-to-edit-friendly after detaching audio turns video black. Reproduction explicitly uses no proxy, no restoration goal.'),
    1037: ('exclude', '20.11.28, 21.01.16, 21.01.29', 'Performance regression with same project and proxy preview; no restoration of original/proxy relationship.'),
}

candidates = json.loads((ROOT/'candidates.json').read_text())
for candidate in candidates:
    number = candidate['number']
    disposition, version, rationale = decisions[number]
    issue = json.loads((ROOT/candidate['body_file']).read_text())
    candidate.update(disposition=disposition, version_evidence=version, rationale=rationale,
        body_anchor=issue['html_url']+'#issue-'+str(issue['id']),
        body_read_scope='Direct current body via repository issues API; no comments/timeline/diff.',
        initial_text_verified=False)
    if number == 942:
        candidate['body_read_scope'] += ' Long crash log inspected at header and all relationship keyword matches; nonmatching address/stack lines not semantically analyzed.'
(ROOT/'candidates.json').write_text(json.dumps(candidates, indent=2)+'\n')

invariants = [
    {'id': 'SC-I1', 'kind': 'observed_pre_change_code_contract', 'statement': 'A proxied producer keeps an original resource separately from its active proxy resource. Normal non-proxy XML filtering restores that original into resource (and warp_resource for timewarp), and removes proxy/original-resource markers from emitted properties.',
     'sources': [blob('src/shotcut_mlt_properties.h',46,57),blob('src/proxymanager.cpp',70,78),blob('src/mltxmlchecker.cpp',593,636),blob('src/proxymanager.cpp',233,290),blob('src/mltcontroller.cpp',448,486)],
     'limitation': 'This describes existing code intent/behavior statically, not a maintainer demand and not a tested guarantee under corruption or an external replacement.'},
    {'id': 'SC-I2', 'kind': 'observed_pre_change_code_contract', 'statement': 'Proxy filenames and lookup use shotcut:hash plus a media extension. getHash reuses an existing stored hash; otherwise it hashes the original resource when proxied and writes the hash property. On explicit relink, the selected replacement path/hash are carried to rewritten resource/hash/caption and stream indices are updated when both hashes are nonempty and differ.',
     'sources': [blob('src/util.cpp',383,421),blob('src/proxymanager.cpp',378,407),blob('src/mltxmlchecker.cpp',448,487),blob('src/mltxmlchecker.cpp',263,291)],
     'limitation': 'Hash is MD5 over all bytes for files <=2,000,000 bytes and first/last 1,000,000 bytes for larger files. It is neither a full-content identity proof nor revalidated when a nonempty cached hash exists. util.cpp explicitly attributes the hashing routine to Kdenlive.'},
]
interfaces = [
    {'symbol':'ProxyManager::resource(Mlt::Service&)', 'purpose':'Resolve original media when proxy marker and original resource are present; otherwise ordinary/timewarp resource.', 'url':blob('src/proxymanager.cpp',70,78), 'writes':[]},
    {'symbol':'ProxyManager::generateVideoProxy / generateImageProxy', 'purpose':'Build hash-derived pending media path in selected proxy directory and queue generation.', 'url':blob('src/proxymanager.cpp',81,226), 'writes':['Create/truncate <hash>.pending.mp4 or <hash>.pending.jpg in proxy directory; enqueue media-writing job.']},
    {'symbol':'ProxyReplacePostJobAction::doAction / ProxyFinalizePostJobAction::doAction', 'purpose':'Finalize pending filename; replacement action creates proxied producer, retains original resource, invokes MAIN.replaceAllByHash.', 'url':blob('src/jobs/postjobaction.cpp',88,119), 'writes':['Rename generated pending file to final media filename.','Set shotcut:proxy and shotcut:resource in producer; delegate replaceAllByHash.','Delete pending path on rename failure.'], 'not_traced':'MAIN.replaceAllByHash implementation was not fetched; no assertion of its detailed fan-out semantics.'},
    {'symbol':'MltXmlChecker::check / checkForProxy / fixUnlinkedFile / fixStreamIndex', 'purpose':'Rewrite XML on load, substitute available proxy, apply replacement model and adjust hash/caption/stream metadata.', 'url':blob('src/mltxmlchecker.cpp',71,139), 'additional_urls':[blob('src/mltxmlchecker.cpp',219,294),blob('src/mltxmlchecker.cpp',448,487),blob('src/mltxmlchecker.cpp',593,675)], 'writes':['Temporary shotcut-XXXXXX.mlt beside input project.','In-memory replacement model, resource/hash/caption and stream properties.','utime calls touch proxy file timestamps.']},
    {'symbol':'UnlinkedFilesDialog::on_tableView_doubleClicked / lookInDir', 'purpose':'Manual replacement and directory discovery populate MissingColumn/ReplacementColumn and ShotcutHashRole.', 'url':blob('src/dialogs/unlinkedfilesdialog.cpp',49,141), 'writes':['Replacement path/hash and status icon in Qt model; Settings.setOpenPath for chosen directory.'], 'important_boundary':'lookInDir accepts hash match OR matching filename, marking differing-hash filename matches with warning icon. This is observed pre-change code, not evidence that auxiliary issue 910 used relinking.'},
    {'symbol':'ProxyManager::filterXML and file-local processProperties; Mlt::Controller::saveXML', 'purpose':'Emit original-backed project XML; save through temporary file and backup/rename handling.', 'url':blob('src/proxymanager.cpp',233,375), 'additional_urls':[blob('src/mltcontroller.cpp',448,550)], 'writes':['Filtered temporary XML file with restored original resource and no proxy markers.','Target project XML via MLT xml consumer; optional initial temp, copy of existing target to backup, target removal and rename of validated temp, removal of backup on success.']},
]

background = {
    'task':'AF-RES-077','project':'mltframework/shotcut','prepared_at_utc':NOW,
    'primary':None,'primary_vacancy_reason':'No candidate among prescribed raw REST query union first 10 has author goal + visible behavior + version evidence specifically about restoring original/proxy relationship.',
    'auxiliary':{'number':910,'url':REPO+'/issues/910#issue-709276970','author':'johnnydepup','created_at':'2020-09-25T20:54:23Z','updated_at':'2020-09-26T17:53:44Z','version':'20.09.13','tag':'v20.09.13','commit_sha':SHA,'commit_time_utc':'2020-09-13T22:26:56Z',
        'goal':'Recover normal timeline playback for a previously working clip after resizing it externally and reusing its filename. This goal is an inference from the author asking for cause/suggestions.',
        'visible_behavior':'The modified clip shows black in the timeline while other clips work and the same clip plays in Source; restart and removing proxies reportedly did not help.',
        'exclusion_boundary':'No distinct directories, moved originals, wrong-media replacement, or explicit original/proxy restoration are stated. No promotion to a primary case.',
        'initial_body_text_verified':False,'body_location':'Current issue opening body, paragraphs 1-4. Exact paragraph 1 names Windows 10/version and same-name external resize; paragraphs 2-3 describe failed workaround and Source-vs-timeline behavior.'},
    'source_supported_invariants':invariants,'pre_change_interfaces':interfaces,
    'outcome_exposure':{'post_request_comments_read':False,'timeline_read':False,'pr_patch_read':False,'test_results_read':False,'unavoidable_current_body_exposure':'Issue 910 body says restarting project and removing proxies did not help and Source plays. This is reported initial problem/workaround evidence, not independent downstream confirmation. Edit history was not checked.',
        'raw_status_metadata':'Raw REST receipts retain status/closure fields and PR links mechanically. They were not used to infer outcome; no comments, reviews, diffs, closing commits or release-note fixes were opened.',
        'extra_connector_candidate':'Connector omitted PR 873 and returned issue 1038 as the tenth result instead. Its body was incidentally visible in initial connector response. It is not in the canonical bounded sample or selection.'},
    'lineage':'All pinned target-code files form one source-code lineage (Shotcut). Util::getFileHash explicitly says it was copied from Kdenlive. No Kdenlive or other donor repository was read.',
    'tested_runtime':False,'source_pin_relationship':'The named release tag predates the auxiliary issue. No claim is made that it equals the exact binaries installed by the author.'
}
(ROOT/'background_packet.json').write_text(json.dumps(background,indent=2)+'\n')

source_notes = {
    'task':'AF-RES-077','recorded_at_utc':NOW,
    'selection':{'primary':None,'auxiliary':REPO+'/issues/910'},
    'canonical_search':'GitHub public REST /search/issues, both issues and PRs; exact queries, created ascending, per_page=10, page=1. The two connector requests were replayed because normalized results lacked dates and failed to include the PR.',
    'receipts':['connector_query_receipt.json','raw_query_receipt.json','raw_query_proxy.json','raw_query_relink.json','http_calls.jsonl'],
    'verified':['Raw query result order and total_count/incomplete_results.','Union dedup by repository and number; sorting by created_at then number.','All 10 canonical candidates fetched directly through /repos/mltframework/shotcut/issues/NUMBER, current body and author/timestamps.','v20.09.13 lightweight tag resolves to exact commit SHA; Git commit date predates auxiliary issue.','Source blob SHAs and content at pinned commit; interfaces and storage writes statically inspected.'],
    'not_verified':['Initial unedited issue body or edit history.','Whether actual author build matches tag bit for bit.','Runtime reproduction, tests, or resolution.','Comments and PR patches.','Completeness outside the prescribed first ten union positions.','Historical GitHub search index as of 2025-12-31; query is executed in 2026 over issues created in requested interval.'],
    'access_failures':[],
    'provider_anomaly':{'provider':'github_search_issues','effect':'Silently excluded PR 873 despite unqualified query, replacing it with issue 1038. All created_at fields also null.','remedy':'Canonical public REST search preserved and used instead; no criteria/query expansion.'},
    'source_works':[
        {'lineage_id':'shotcut-issue-910-johnnydepup','kind':'independently_authored_request','url':REPO+'/issues/910#issue-709276970','author':'johnnydepup','used_for':'Auxiliary goal/visible behavior/version only.'},
        {'lineage_id':'shotcut-code-v20.09.13','kind':'target_code','url':REPO+'/tree/'+SHA,'commit':SHA,'used_for':'All target interfaces, writes, and invariants; eleven files count as one code lineage.','dependency_lineage_note':'util.cpp:385 explicitly attributes getFileHash to Kdenlive. This copied routine does not supply independent Shotcut-versus-Kdenlive corroboration.'},
        {'lineage_id':'github-search-and-object-metadata','kind':'provider_metadata','url':'https://api.github.com/search/issues','used_for':'Recruitment receipts, ranking, tag and commit metadata; not an independent mechanism source.'}
    ],
    'source_files':[],
    'call_costs':{'connector_calls':16,'connector_breakdown':{'search_issues':2,'fetch_tag_commit_tree':3,'fetch_file':11},'public_http_gets':13,'public_http_breakdown':{'initial_issue_910_connectivity_probe':1,'canonical_search_queries':2,'canonical_candidate_issue_fetches':10},'recorded_http_calls':12,'recorded_http_elapsed_seconds_sum':120.983,'initial_probe_elapsed_seconds':8.806421458,'external_endpoint_calls_total':29,'currency_charge':'No monetary charge returned by tools; paid APIs not used.','model_tokens':'Unavailable to this investigator.','notes':'Connector durations not measured; parallel calls overlap, so elapsed sums are not wall-clock duration.'}
}
for receipt in sorted(ROOT.glob('source__*.receipt.json')):
    item=json.loads(receipt.read_text())
    source=receipt.with_name(receipt.name.removesuffix('.receipt.json'))
    item.update(local_file=source.name,sha256=hashlib.sha256(source.read_bytes()).hexdigest(),lineage_id='shotcut-code-v20.09.13')
    source_notes['source_files'].append(item)
(ROOT/'source_notes.json').write_text(json.dumps(source_notes,indent=2)+'\n')

rows=[]
for c in candidates:
    rows.append(f"| {c['union_rank']} | [#{c['number']}]({c['url']}) | {c['created_at']} | {c['author']} | {c['rationale']} |")
report=f'''# AF-RES-077 — Shotcut recruitment result

## Decision

**Primary case remains vacant.** The required bounded sample contains no request with author goal, visible behavior and version evidence specifically about restoring an original/proxy relationship. The nearest case, [issue #910]({REPO}/issues/910#issue-709276970), is retained as **auxiliary only**. Its author describes replacing a video externally under the same filename and then seeing a black timeline, while Source playback works. The body does not say the original moved, that equal filenames existed in distinct folders, or that wrong media was selected when reconnecting original and proxy. Those recruitment hints have not been rewritten as maintainer demands.

## Search receipt and bounded sample

Executed on 2026-11-23 UTC using exactly:

- `repo:mltframework/shotcut proxy created:2019-01-01..2025-12-31`
- `repo:mltframework/shotcut relink created:2019-01-01..2025-12-31`

Public REST parameters were `sort=created`, `order=asc`, `per_page=10`, `page=1`. Proxy returned total 36, `incomplete_results=false`, first ten **873, 880, 908, 910, 914, 923, 942, 987, 988, 1037**. Relink returned total zero, `incomplete_results=false`. Deduplication and `(created_at, number)` sorting produce the same ten-item order. First HTTP request began 2026-11-23T11:25:57.477845Z; last candidate body fetch completed 2026-11-23T11:26:48.112459Z.

The initial connector `search_issues` response silently omitted PR #873 and returned issue #1038 instead; its date fields were null. The raw public REST replay is authoritative here. Both receipts and original orders are preserved. Issue #1038's current body was incidentally exposed by that connector response, but it is excluded from the canonical bounded sample. No replacement query or expanded sample was used.

| Rank | Request | Created UTC | Author | Decision basis from current body |
|---:|---|---|---|---|
{chr(10).join(rows)}

Each canonical candidate was fetched directly via the repository issues API, which also returns a PR's opening description without its diff. For #942, the crash header and every line containing proxy/relink/original/moved/folder were inspected; nonmatching stack/address lines were not semantically analyzed. Current bodies are not certified as their creation-time text. Search is a current index queried by creation interval, not a reconstruction of the index at the end of 2025.

## Auxiliary request and version pin

The [opening body of #910]({REPO}/issues/910#issue-709276970) is by **johnnydepup**, created **2020-09-25T20:54:23Z**, updated **2020-09-26T17:53:44Z**. Paragraph 1 specifies **Windows 10 / Shotcut 20.09.13** and external resize under the same name. Paragraphs 2–3 report restart/proxy-removal failure and working Source playback. Recovering normal timeline playback is an inferred author goal from that body and request for suggestions; it is not an attributed formal requirement.

[Tag `v20.09.13`](https://api.github.com/repos/mltframework/shotcut/git/ref/tags/v20.09.13) resolves directly to commit **`{SHA}`**. [Git commit metadata](https://api.github.com/repos/mltframework/shotcut/git/commits/{SHA}) gives **2020-09-13T22:26:56Z**, before the issue. This is the exact release source pin, not proof of the reporter's exact installed binary.

## Two source-supported pre-change invariants

1. **Keep the original resource separately while proxy media is active.** `ProxyManager::resource` prefers saved `shotcut:resource` when `shotcut:proxy` is set. `MltXmlChecker::checkForProxy` switches the active resource to a hash-named proxy and appends the saved original path. `processProperties` in the proxy manager restores that original for normal non-proxy XML output and removes both proxy markers. The save path calls this filter when `proxy=false`. Sources: [resource resolver]({blob('src/proxymanager.cpp',70,78)}), [load substitution]({blob('src/mltxmlchecker.cpp',593,636)}), [XML restoration]({blob('src/proxymanager.cpp',233,290)}), [save entry point]({blob('src/mltcontroller.cpp',448,486)}).

2. **Carry identity metadata consistently through proxy lookup and explicit relink.** Proxy lookup uses `shotcut:hash` plus extension; `Util::getHash` caches the value and otherwise hashes the original resource. Explicit relink carries the replacement path and hash into resource/hash/caption rewrites, and updates stream indices when nonempty old/new hashes differ. Sources: [hash implementation]({blob('src/util.cpp',383,421)}), [proxy lookup]({blob('src/proxymanager.cpp',378,407)}), [replacement application]({blob('src/mltxmlchecker.cpp',448,487)}), [XML metadata update]({blob('src/mltxmlchecker.cpp',263,291)}). This hash samples first/last 1 MB for files over 2 MB; it is not full-file identity verification and a cached value is not rechecked.

These are static observations of existing contracts, not runtime verification, a diagnosis of #910, or inferred maintainer requests. `UnlinkedFilesDialog::lookInDir` accepts **matching hash OR matching filename**, with a warning icon for a filename-only differing-hash candidate. That [pre-change boundary]({blob('src/dialogs/unlinkedfilesdialog.cpp',85,132)}) is relevant background, but no sampled request is claimed to exercise it.

## Interface and storage boundaries

- `ProxyManager::resource`, `fileExists`, `filePending`, `generateVideoProxy`, `generateImageProxy`, `generateIfNotExists` expose resource selection, hash-derived media lookup and generation. Generation writes/truncates `<hash>.pending.mp4` or `.pending.jpg` in either the project proxy directory or configured proxy folder.
- `ProxyReplacePostJobAction::doAction` renames the pending file, marks the new producer as proxy, saves the original resource and calls `MAIN.replaceAllByHash`; finalization also renames the generated file. [Source]({blob('src/jobs/postjobaction.cpp',88,119)}). The implementation of `MAIN.replaceAllByHash` was not fetched, so its detailed fan-out is not claimed.
- `MltXmlChecker::check`, `checkForProxy`, `fixUnlinkedFile`, `fixStreamIndex` read project properties and write a temporary `shotcut-XXXXXX.mlt`. The replacement Qt model carries missing/replacement paths and `ShotcutHashRole`; proxy lookup touches proxy file timestamps. [Load entry point]({blob('src/mltxmlchecker.cpp',71,139)}), [model interface]({blob('src/mltxmlchecker.h',32,78)}).
- `UnlinkedFilesDialog::on_tableView_doubleClicked` and `lookInDir` populate replacement path/hash and status icon; manual selection updates `Settings.setOpenPath`. [Source]({blob('src/dialogs/unlinkedfilesdialog.cpp',49,141)}).
- `ProxyManager::filterXML` restores original-backed properties into temporary XML. `Mlt::Controller::saveXML` writes through MLT's XML consumer and, when filtering/saving through its checked path, copies an existing target to a backup, removes the old target, renames the temporary output and removes the backup on success. [Source]({blob('src/mltcontroller.cpp',448,550)}).

Exact symbols, URL anchors and write descriptions are also in `background_packet.json`; immutable source bodies and blob receipts are retained alongside this report.

## Separation, lineage, limitations and cost

No issue comments, PR patches, reviews, post-request tests, closing commits, resolution statements or later release fixes were read. Unavoidable exposure: #910's current body says restart and deleting proxies failed and Source works. Edit history was not inspected. Raw API snapshots mechanically include state/closure fields; those fields were not surfaced as evidence or used to infer outcomes.

All eleven pinned code files count as **one Shotcut source-code lineage**. The #910 request is a separately authored request work. `src/util.cpp:385` explicitly says `getFileHash` was copied from **Kdenlive**; it cannot be treated as independent corroboration of Kdenlive code. No donor repository or donor-field source was consulted. Metadata/search receipts are provenance, not an additional mechanism source.

There were **29 external endpoint calls**: 16 connector calls (2 searches, tag/commit/tree 3, source files 11) and 13 public HTTP GETs (one initial #910 connectivity probe, two canonical query replays, ten canonical candidate fetches). Twelve recorded HTTP calls total 120.983 request-seconds, overlapping in time; the initial probe took 8.806 seconds. Tool billing and token use were not returned. No paid API was used. There were no access failures; the connector's PR omission is recorded as a provider anomaly. No runtime behavior or tests were executed.
'''
(ROOT/'REPORT.md').write_text(report)
print(json.dumps({'primary':None,'auxiliary':910,'candidate_count':len(candidates),'source_file_count':len(source_notes['source_files']),'report':str(ROOT/'REPORT.md'),'prepared_at_utc':NOW},indent=2))
