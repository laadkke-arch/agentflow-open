# AF-RES-077 — Shotcut recruitment result

## Decision

**Primary case remains vacant.** The required bounded sample contains no request with author goal, visible behavior and version evidence specifically about restoring an original/proxy relationship. The nearest case, [issue #910](https://github.com/mltframework/shotcut/issues/910#issue-709276970), is retained as **auxiliary only**. Its author describes replacing a video externally under the same filename and then seeing a black timeline, while Source playback works. The body does not say the original moved, that equal filenames existed in distinct folders, or that wrong media was selected when reconnecting original and proxy. Those recruitment hints have not been rewritten as maintainer demands.

## Search receipt and bounded sample

Executed on 2026-11-23 UTC using exactly:

- `repo:mltframework/shotcut proxy created:2019-01-01..2025-12-31`
- `repo:mltframework/shotcut relink created:2019-01-01..2025-12-31`

Public REST parameters were `sort=created`, `order=asc`, `per_page=10`, `page=1`. Proxy returned total 36, `incomplete_results=false`, first ten **873, 880, 908, 910, 914, 923, 942, 987, 988, 1037**. Relink returned total zero, `incomplete_results=false`. Deduplication and `(created_at, number)` sorting produce the same ten-item order. First HTTP request began 2026-11-23T11:25:57.477845Z; last candidate body fetch completed 2026-11-23T11:26:48.112459Z.

The initial connector `search_issues` response silently omitted PR #873 and returned issue #1038 instead; its date fields were null. The raw public REST replay is authoritative here. Both receipts and original orders are preserved. Issue #1038's current body was incidentally exposed by that connector response, but it is excluded from the canonical bounded sample. No replacement query or expanded sample was used.

| Rank | Request | Created UTC | Author | Decision basis from current body |
|---:|---|---|---|---|
| 1 | [#873](https://github.com/mltframework/shotcut/pull/873) | 2020-05-30T06:41:59Z | ddennedy | Title is Proxy mode, but current body is empty. No body-level author goal, observed behavior, or version evidence; PR patch deliberately not read. |
| 2 | [#880](https://github.com/mltframework/shotcut/issues/880) | 2020-06-18T19:15:15Z | ychang4 | Subtitle editing becomes slow and memory-intensive; no restoration of original/proxy relationship. |
| 3 | [#908](https://github.com/mltframework/shotcut/issues/908) | 2020-09-05T01:27:19Z | survivor303 | UI says proxies are in use but project proxy directory is not populated. Proxy creation failure, without restoration or moved-original relationship. |
| 4 | [#910](https://github.com/mltframework/shotcut/issues/910) | 2020-09-25T20:54:23Z | johnnydepup | External resize and same-name replacement yields black timeline while Source plays; removing proxies did not help. No moved originals, distinct-folder basename collision, or explicit restoration of original/proxy relationship. |
| 5 | [#914](https://github.com/mltframework/shotcut/issues/914) | 2020-09-30T16:39:42Z | seema84 | Size and position animation is shown in Shotcut but absent from export; no original/proxy restoration. |
| 6 | [#923](https://github.com/mltframework/shotcut/issues/923) | 2020-10-15T14:48:59Z | maulonobile | QSV encoder is not used for proxy generation while export is okay; encoder selection, not association restoration. |
| 7 | [#942](https://github.com/mltframework/shotcut/issues/942) | 2020-11-05T23:51:03Z | ghost | macOS crash report. Inspected crash header and all body lines matching proxy/relink/original/moved/folder; matches are system stack/library names, not a media-restoration goal. |
| 8 | [#987](https://github.com/mltframework/shotcut/issues/987) | 2020-12-20T20:44:36Z | PontiacCZ | About one second freezes after a cut, also after export; reproduction explicitly uses no proxy. |
| 9 | [#988](https://github.com/mltframework/shotcut/issues/988) | 2020-12-21T12:17:39Z | PontiacCZ | Convert-to-edit-friendly after detaching audio turns video black. Reproduction explicitly uses no proxy, no restoration goal. |
| 10 | [#1037](https://github.com/mltframework/shotcut/issues/1037) | 2021-02-11T20:43:05Z | pauweh | Performance regression with same project and proxy preview; no restoration of original/proxy relationship. |

Each canonical candidate was fetched directly via the repository issues API, which also returns a PR's opening description without its diff. For #942, the crash header and every line containing proxy/relink/original/moved/folder were inspected; nonmatching stack/address lines were not semantically analyzed. Current bodies are not certified as their creation-time text. Search is a current index queried by creation interval, not a reconstruction of the index at the end of 2025.

## Auxiliary request and version pin

The [opening body of #910](https://github.com/mltframework/shotcut/issues/910#issue-709276970) is by **johnnydepup**, created **2020-09-25T20:54:23Z**, updated **2020-09-26T17:53:44Z**. Paragraph 1 specifies **Windows 10 / Shotcut 20.09.13** and external resize under the same name. Paragraphs 2–3 report restart/proxy-removal failure and working Source playback. Recovering normal timeline playback is an inferred author goal from that body and request for suggestions; it is not an attributed formal requirement.

[Tag `v20.09.13`](https://api.github.com/repos/mltframework/shotcut/git/ref/tags/v20.09.13) resolves directly to commit **`0898bdf3fc0f9f3fbf78336bad21d5506e19c118`**. [Git commit metadata](https://api.github.com/repos/mltframework/shotcut/git/commits/0898bdf3fc0f9f3fbf78336bad21d5506e19c118) gives **2020-09-13T22:26:56Z**, before the issue. This is the exact release source pin, not proof of the reporter's exact installed binary.

## Two source-supported pre-change invariants

1. **Keep the original resource separately while proxy media is active.** `ProxyManager::resource` prefers saved `shotcut:resource` when `shotcut:proxy` is set. `MltXmlChecker::checkForProxy` switches the active resource to a hash-named proxy and appends the saved original path. `processProperties` in the proxy manager restores that original for normal non-proxy XML output and removes both proxy markers. The save path calls this filter when `proxy=false`. Sources: [resource resolver](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/proxymanager.cpp#L70-L78), [load substitution](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/mltxmlchecker.cpp#L593-L636), [XML restoration](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/proxymanager.cpp#L233-L290), [save entry point](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/mltcontroller.cpp#L448-L486).

2. **Carry identity metadata consistently through proxy lookup and explicit relink.** Proxy lookup uses `shotcut:hash` plus extension; `Util::getHash` caches the value and otherwise hashes the original resource. Explicit relink carries the replacement path and hash into resource/hash/caption rewrites, and updates stream indices when nonempty old/new hashes differ. Sources: [hash implementation](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/util.cpp#L383-L421), [proxy lookup](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/proxymanager.cpp#L378-L407), [replacement application](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/mltxmlchecker.cpp#L448-L487), [XML metadata update](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/mltxmlchecker.cpp#L263-L291). This hash samples first/last 1 MB for files over 2 MB; it is not full-file identity verification and a cached value is not rechecked.

These are static observations of existing contracts, not runtime verification, a diagnosis of #910, or inferred maintainer requests. `UnlinkedFilesDialog::lookInDir` accepts **matching hash OR matching filename**, with a warning icon for a filename-only differing-hash candidate. That [pre-change boundary](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/dialogs/unlinkedfilesdialog.cpp#L85-L132) is relevant background, but no sampled request is claimed to exercise it.

## Interface and storage boundaries

- `ProxyManager::resource`, `fileExists`, `filePending`, `generateVideoProxy`, `generateImageProxy`, `generateIfNotExists` expose resource selection, hash-derived media lookup and generation. Generation writes/truncates `<hash>.pending.mp4` or `.pending.jpg` in either the project proxy directory or configured proxy folder.
- `ProxyReplacePostJobAction::doAction` renames the pending file, marks the new producer as proxy, saves the original resource and calls `MAIN.replaceAllByHash`; finalization also renames the generated file. [Source](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/jobs/postjobaction.cpp#L88-L119). The implementation of `MAIN.replaceAllByHash` was not fetched, so its detailed fan-out is not claimed.
- `MltXmlChecker::check`, `checkForProxy`, `fixUnlinkedFile`, `fixStreamIndex` read project properties and write a temporary `shotcut-XXXXXX.mlt`. The replacement Qt model carries missing/replacement paths and `ShotcutHashRole`; proxy lookup touches proxy file timestamps. [Load entry point](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/mltxmlchecker.cpp#L71-L139), [model interface](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/mltxmlchecker.h#L32-L78).
- `UnlinkedFilesDialog::on_tableView_doubleClicked` and `lookInDir` populate replacement path/hash and status icon; manual selection updates `Settings.setOpenPath`. [Source](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/dialogs/unlinkedfilesdialog.cpp#L49-L141).
- `ProxyManager::filterXML` restores original-backed properties into temporary XML. `Mlt::Controller::saveXML` writes through MLT's XML consumer and, when filtering/saving through its checked path, copies an existing target to a backup, removes the old target, renames the temporary output and removes the backup on success. [Source](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/mltcontroller.cpp#L448-L550).

Exact symbols, URL anchors and write descriptions are also in `background_packet.json`; immutable source bodies and blob receipts are retained alongside this report.

## Separation, lineage, limitations and cost

No issue comments, PR patches, reviews, post-request tests, closing commits, resolution statements or later release fixes were read. Unavoidable exposure: #910's current body says restart and deleting proxies failed and Source works. Edit history was not inspected. Raw API snapshots mechanically include state/closure fields; those fields were not surfaced as evidence or used to infer outcomes.

All eleven pinned code files count as **one Shotcut source-code lineage**. The #910 request is a separately authored request work. `src/util.cpp:385` explicitly says `getFileHash` was copied from **Kdenlive**; it cannot be treated as independent corroboration of Kdenlive code. No donor repository or donor-field source was consulted. Metadata/search receipts are provenance, not an additional mechanism source.

There were **29 external endpoint calls**: 16 connector calls (2 searches, tag/commit/tree 3, source files 11) and 13 public HTTP GETs (one initial #910 connectivity probe, two canonical query replays, ten canonical candidate fetches). Twelve recorded HTTP calls total 120.983 request-seconds, overlapping in time; the initial probe took 8.806 seconds. Tool billing and token use were not returned. No paid API was used. There were no access failures; the connector's PR omission is recorded as a provider anomaly. No runtime behavior or tests were executed.
