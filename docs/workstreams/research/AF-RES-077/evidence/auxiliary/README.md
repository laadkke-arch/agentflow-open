# Post-seal auxiliary probes — unscored

These are executed Python research probes of narrow input predicates. They are
**not Shotcut/Sigil GUI runs, original Qt unit tests, issue reproductions, complete
fixes, or additions to the sealed A/B pass counts**. The frozen packets and reader
outputs were not changed. The reversed Shotcut order and in-memory XHTML layouts
are explicitly supplemental diagnostics.

## Run and provenance

The captured worker ran from `2026-11-23T11:55:19.576993+00:00` to
`2026-11-23T11:55:19.710772+00:00`, under CPython 3.12.14 on Linux. Its exit code was
**0**, obtained from `subprocess.CompletedProcess.returncode`; stderr was empty.
The supervisor command also returned exit code 0. All input fingerprints were
unchanged before/after execution. This verifies completion of the auxiliary
program only; target application runtime tests executed: **0**.

The exact executable, version, platform, command arguments, working directory,
UTC interval, workspace commit, source/packet/fixture/script hashes, and output
hashes are in [the receipt](observed-run-20261123/receipt.json). The actual JSON
stdout is [stdout.json](observed-run-20261123/stdout.json); its companion
[stderr.txt](observed-run-20261123/stderr.txt) is retained even though empty.

Pinned source basis:

- Shotcut `v20.09.13`, commit `0898bdf3fc0f9f3fbf78336bad21d5506e19c118`:
  `recruitment/shotcut/source__src__util.cpp`, `getFileHash` / `getHash`, lines
  383–421; `source__src__dialogs__unlinkedfilesdialog.cpp`, `lookInDir`, lines
  85–132; `postseal/shotcut/src__mainwindow.cpp`, lines 1082–1092.
- SG input semantics come from frozen `packets/SG-common.json`, with its stated
  Sigil `0.9.17` operational pin `30419827123d533d10ad482b1634dcec05ff0e1b`.
  The SG probe is an independent URI/ID observation; it does not transcribe or
  execute Sigil anchor-update code.
- All five source/packet byte hashes are recorded in
  [probe-inputs.json](../../fixtures/research/probe-inputs.json) and again in the
  execution receipt. Release source pins do not verify the requesters' installed
  binaries or turn these researcher-authored cases into primary issue fixtures.

## SC-X: sampled edges versus changed middle

The deterministic generator writes **exactly 3,145,728 bytes (3 MiB)** at one
temporary path. Each of three blocks is 1,048,576 bytes. It writes repeated ASCII
`A`, `B`, `C`, then truncates/replaces that same path with `A`, `D`, `C`. The temporary
binary and its directory were removed; the exact generator, transient path, byte
ranges, lengths, and hashes remain in the descriptor and stdout.

The successful-read Python transcription follows the pinned source's decimal
**1,000,000-byte** edge reads. The first half-open interval is `[0, 1000000)` and
the last is `[2145728, 3145728)`. The changed middle block
`[1048576, 2097152)` intersects neither interval. The file's size chooses the
branch and seek offset; **size bytes are not appended to the digest**. This is a
precision clarification of the packet's shorthand, not a change to its frozen
input.

| Measurement | Original A/B/C | Replacement A/D/C |
| --- | --- | --- |
| File length | 3,145,728 bytes | 3,145,728 bytes |
| Sampled MD5 | `ba65d260d785c5cba4a218b48c1bcd07` | `ba65d260d785c5cba4a218b48c1bcd07` |
| Full SHA-256 | `eac30895efc5758ba7218a5b8e59885c50c2adcd7136bdeb13841bb196aa5052` | `4e3e217a98e9bcb06415261875c4b3d68c793df1a864c035314bad778151eb9e` |
| Content bytes returned to sampled hash | 2,000,000 | 2,000,000 |
| Content bytes returned to full hash | 3,145,728 | 3,145,728 |

The non-empty cached `getHash` branch is separately represented: a stipulated old
`shotcut:hash` returns without a new file-content read (zero content bytes). Even
clearing that cache and applying this sampled recipe again gives the same digest
for these constructed inputs. The full-content digest distinguishes them.

This is an unsampled-content equality example, not an MD5 cryptanalysis claim.
Read-byte counts are logical bytes returned by the Python reads, excluding
metadata calls, operating-system cache traffic, physical I/O and performance.
The files are not valid media. No metadata-copy behavior, media decoding, proxy
job, preview, intended-source mismatch on screen, or application recovery was
executed or observed.

## SC-E: first matching suggestion and the separate confirmation gate

The bounded replay uses the frozen symbolic hashes and stipulated candidate
order. It covers one unresolved replacement row. Actual filesystem enumeration
and recursive QDir ordering are outside the probe.

| Input order | Replacement suggested by replay | Model decoration | Later candidate |
| --- | --- | --- | --- |
| Frozen: BLUE then RED | `/new/camB/clip.mp4` (`H_BLUE`) | Filename-only warning icon `task-attempt.png` | RED not evaluated after the row is filled and outstanding reaches zero |
| Supplemental, unscored: RED then BLUE | `/new/camA/clip.mp4` (`H_RED`) | Hash-match icon `task-complete.png` | BLUE not evaluated |

The predicate is `candidate_hash == missing_hash OR filename == missing_basename`.
The first BLUE candidate therefore populates a **suggestion in the dialog model**
with a warning icon. This does not establish a popup warning, human identity
confirmation, project mutation, or a saved replacement. The source's non-null
replacement-hash guard also prevents an already populated row from being matched
again on a later search call unless another operation resets it.

`MainWindow` separately requires `dialog.exec() == QDialog::Accepted`, then
`checker.check(fileName) && checker.isCorrected()`, before calling
`saveRepairedXmlFile`. None of those calls was executed here. In particular,
"do not provide human identity confirmation" in the frozen scenario does **not**
establish that `QDialog::Accepted` occurred. There is no claim that p1 changed,
p2 was preserved or damaged, proxy state changed, or save/reopen succeeded.

## SG-N/E/X: original document scope and URI observations

Five actual XHTML text files retain the exact decoded frozen body strings,
including split comments. Only an XML declaration, XHTML namespace, minimal
`head`/`title`, and outer `html`/`body` elements were added. The original fragments
and wrapper strings are in the descriptor, and the worker verifies the complete
expected bytes. No fragment unescaping, XML reserialization, anchor renaming,
content edits, or EPUB packaging was performed.

`xml.etree.ElementTree` supplies element/ID inspection. Standard-library
`urllib.parse.urljoin`, `urlsplit`, and `unquote` resolve each href from its source
document. A synthetic `https://auxiliary.invalid/` origin provides a common URI
base; **no network access occurs**. The resolver records all matching IDs and
returns a chosen text only when the target document contains exactly one match.
This strict uniqueness policy is a research predicate, not a claimed browser or
Sigil duplicate-ID selection rule.

| Case | Original input observation | What remains unknown |
| --- | --- | --- |
| SG-N | `Text/ch1.xhtml` + `#fn` resolves uniquely to `FOOTNOTE_A`; no ID collision | Whether Sigil preserves that identity during split/save/reopen |
| SG-E | The self link and toc A resolve to `Text/ch1.xhtml#fn` / `FOOTNOTE_A`; toc B resolves to `Text/ch2.xhtml#fn` / `FOOTNOTE_B`. Repeated `fn` occurs across two documents, with no within-document duplicate. | Whether the pinned application updates each relevant href and leaves other chapters intact |
| SG-X | `Text/ch1.xhtml#fn` has two matches, `FIRST` and `SECOND`; chosen target remains null | The trusted pre-edit intended target, absent from the frozen input |

The SG-E bare-global-ID demonstration discards the document path. Its collision
preserving index contains both A and B under `fn`; an explicitly illustrative
last-wins single-value map over document order `ch1`, `ch2`, `toc` returns B even
for A's links. That toy order is **not** asserted to reproduce Qt QHash iteration
or Sigil's caller-selected resource set. It demonstrates that a single bare-ID
entry cannot express both original targets. Source-document-plus-fragment keys
do express both in this input.

For SG-X, adding the document path still leaves two candidates under one scoped
key. Unchanged document bytes or an unchanged full digest do not provide the
missing intended-target choice. Selecting FIRST by one policy, or SECOND by a
last-wins policy, would be an additional choice rather than evidence of the
original intent.

The stdout also contains a **mechanical in-memory split without href rewriting**.
It is a counterfactual layout check, not a Sigil result. Under that layout,
unchanged SG-N and the A links in SG-E no longer find their old targets; toc B in
SG-E still finds B. Candidate location queries `ch1_1.xhtml#fn` for N and
`parts/ch1_tail.xhtml#fn` for E resolve to A from the stated reference bases, but
these candidate hrefs are never applied to an application or saved as a fix.
For X, `Text/ch1_1.xhtml` is labeled a supplemental diagnostic path because the
frozen case does not prescribe a tail filename. The remaining `#fn` can now find
FIRST uniquely in that mechanical layout, which still does not establish the
trusted pre-edit identity. No candidate-preservation href is selected for X.

## Conditions under which this cannot discriminate A and B

These observations cannot choose between proposals merely because one is called
A and another B. No selected proposal implementation is run.

- SC-X can distinguish the stipulated sample/cache predicate from a fresh full
  digest on these bytes. It does not distinguish proposals that both recompute a
  full digest, both share the shortcut, or differ in unexecuted preview/commit
  behavior.
- SC-E exposes order sensitivity of the specified first-match suggestion. It does
  not distinguish proposals that both reject filename-only candidates or require
  explicit confirmation, and does not measure downstream mutation.
- SG-N and SG-E do not distinguish proposals that both preserve scoped identity
  and yield the same target paths. A one-document normal input alone cannot expose
  a cross-document key collision.
- SG-X has insufficient target provenance for a unique preservation answer.
  Refusal and requesting a trusted choice remain different possible designs;
  these observations test neither design's application behavior or usability.

## Reproduce

Run from `docs/workstreams/research/AF-RES-077` with Python 3.12 or newer:

```sh
python evidence/auxiliary/run_probes.py --prepare-inputs
python evidence/auxiliary/run_probes.py --record-run rerun-001
```

Preparation creates missing deterministic textual fixtures and refuses to
overwrite different existing inputs. A record run uses a new output-directory
label, invokes a separate worker, captures raw stdout/stderr and the actual exit
code, and records before/after input fingerprints. Changed pinned source or
fixture hashes cause an error. Large binaries exist only in a temporary directory
under `fixtures/research` while SC-X executes. Do not turn an auxiliary-program
exit code into a Shotcut/Sigil test score.

## Retained files produced by this task

All paths below are relative to `docs/workstreams/research/AF-RES-077`:

```text
evidence/auxiliary/README.md
evidence/auxiliary/run_probes.py
evidence/auxiliary/observed-run-20261123/stdout.json
evidence/auxiliary/observed-run-20261123/stderr.txt
evidence/auxiliary/observed-run-20261123/receipt.json
fixtures/research/probe-inputs.json
fixtures/research/SG-N/original/Text/ch1.xhtml
fixtures/research/SG-E/original/Text/ch1.xhtml
fixtures/research/SG-E/original/Text/ch2.xhtml
fixtures/research/SG-E/original/Text/toc.xhtml
fixtures/research/SG-X/original/Text/ch1.xhtml
```

The README was written after inspecting the captured run; it is a report about
the run, not one of its input files. No commits were made by the auxiliary worker.
