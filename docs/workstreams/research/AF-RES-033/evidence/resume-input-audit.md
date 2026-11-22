# AF-RES-033 resumed input audit

Auditor: `/root/input_audit`, a separate model context. Checked UTC: 2026-11-22T17:05:01Z. Repository HEAD during the checks: `8358b5e75ca45fd9bf0e26cab70e2acc1bc39493`.

## Disposition

The eight input objects, sixteen query strings, opening-source byte identities and chronological selection ledger are internally consistent. The actual input file has SHA256 `672d624e1daa32afe2d4dfc1d738bbaa3fe10398556c871727d29a2284b3549e`, identical to the prepared seal. No query or source was changed by this audit. There is **one material interpretation qualification**, R04's conversion of recommended retrospective content into a mandatory matching condition, described below.

At the recorded check time, `inputs.jsonl` was not in HEAD and `rankings.csv` did not exist. Consequently the prepared local seal was not yet a completed remote input seal. The parent must commit the frozen input bundle before running the first ranking. This audit does not attest to a later remote write or ranking execution.

## Access boundary

The auditor read the repository's AGENTS, SCOPE and PROGRESS, the canonical input and source/condition packets, the sixteen prepared queries and their author checks, selected immutable-source local byte copies, recipient selection/frame/attempt records, and source-binding audit records. Initial source passages supporting every narrow target and every R query were displayed and checked. This was a passage-level semantic recheck, not a repeat full reading of every initial proposal.

The auditor did not open the provider corpus or its document titles, ranking output, field cases, later recipient comments, closure/merger outcomes or implementation results. SCOPE disclosed the already-prespecified provider sectors and publishers; the validation script also disclosed its prohibited-name screening strings. Those disclosures occurred in this audit **after** the original query-author work and were not used to rewrite a query. No claim of complete sector blindness is made for this auditor.

This is separate-model-context review, not independent human coding, a test of model pretraining exposure, or proof that a self-reported earlier author read history is exhaustive. The earlier query-author attestation says it read only the final eight full originals, the source/condition packet and one original PNG. Its string and packet hashes were independently checked here; its historical context isolation is still an attestation.

## Structural and lexical checks

| Check | Actual result | Evidence |
| --- | --- | --- |
| Initial input rows and repository split | 8, with 4 Rust and 4 Kubernetes | `inputs.jsonl`; `recipient/recipient_targets.jsonl` |
| Whole/partial design split | 3 whole, 5 partial | `recipient/recipient_selection.json`; source packets |
| Raw SHA256, LF SHA256 and Git blob SHA1 | All 8 agree with retained bytes | `inputs.jsonl.original_source`; immutable source paths listed below |
| Query strings survive integration unchanged | 16/16 equal the corresponding author strings | `recipient/queries_sealed.jsonl` |
| Exact query string SHA256 | 16/16 agree across author and canonical input | `recipient/queries_sealed.jsonl`; `inputs.jsonl` |
| Query author file SHA256 | `8045290cd5d926ea7abe066f94658d4a1bd8280290cefe4c81eb4ebf0d203c74` | `recipient/query_author_checks.json.query_file` |
| Target packet SHA256 | `361b497dfde4d6d875381aa6e5043562d229aa8709ecfa5b0861eb3aa452e1af` | Author checks; `recipient/recipient_targets.jsonl` |
| Narrow target changed by integrator | None, 8/8 packet objects equal | Canonical inputs versus target packets |
| S terms outside its own initial source | 0 for every S query | Independent NFC/lowercase `[a-z0-9]+` recomputation |
| Equal ceiling and language | All 16 within the 80-token ceiling; all English | Exact token counts below and direct text inspection |
| Full metadata-frame identities preserved | 3,415/3,415 match the metadata-only frame at `1c4706228af21a8183dd3c873d5864f06edbe206` | Repository, PR number, creation time, URL, year and page fields compared |
| Current annotated frame hash | Matches `recipient_selection.json.annotated_frame_sha256` | `recipient/recipient_frame.csv` |
| Final chronological prefix | Rust 6 rows; Kubernetes 17 rows; total 23 = 8 selected + 15 excluded | Selection cutoff recomputed from sorted creation time and PR number |
| Prefix structural exclusions | 15/15 have a unique complete archived opening event, matching event-projection hash/head/creation time, no file-cap flag and no added/renamed proposal Markdown | `recipient/recipient_attempts.jsonl` referenced by frame lines; `evidence/archive-recovery-checks.jsonl`; `evidence/prefix-archive-checks.jsonl` |

| Recipient | S raw tokens | R raw tokens | Meaning check |
| --- | ---: | ---: | --- |
| R01 | 64 | 64 | Rename with identical behavior, forwarding and explicit future semantic-change warning are source-grounded; feature-gate placement remains unresolved. |
| R02 | 73 | 71 | Implicit ancestor shadowing, explicit ambiguity and qualified access remain distinct; overriding is not invented. |
| R03 | 74 | 73 | Input initialization, ordinary-output reservation, late-output read-before-write condition and final output transfer are all grounded. |
| R04 | 76 | 74 | Archival, read-only repository, leaders/liaison/consensus and reassessment are grounded; the strength of retrospective-content obligations is qualified below. |
| R05 | 64 | 71 | API acceptance and controller handoff are distinguished from the provider's actual exposure capability; the activation-control alternative remains open. |
| R06 | 75 | 73 | File/type separation, initial cross-placement rejection, flag precedence and shared-refresh scope are grounded. |
| R07 | 78 | 68 | All four creation cases, N+4 backfill removal, immutable fields, authoritative new consumers and continued permissive annotation updates are preserved. |
| R08 | 56 | 66 | The requested change is default activation; eviction mechanics are explicitly pre-existing and functionality is preserved. |

The same maximum budget does not imply identical query lengths, abstraction depth, or identical effective unique-term counts. R remains partly expressed in recipient technical vocabulary. A comparison must describe these actual S/R formulations and must not generalize to every possible relational rewrite.

## R04 obligation-strength qualification

The frozen R04-M07 requires communication of archival **and preservation of an account of outputs/process**, alongside infrastructure archival and omission of private feedback. The source separates the archival announcement from proposed retrospective practice:

- [Original archival steps, lines 123–134](https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md#L123-L134): the public announcement is a workflow step, but inclusion of decisions, outputs and process reflections is described as desirable content and a non-exhaustive selection.
- [Original retrospectives, lines 343–351](https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md#L343-L351): public retrospective discussion and output/process coverage are recommendations; withholding feedback members wish to keep private is explicit.

Therefore labeling every combined subclause as an unqualified mandatory requirement is stronger than the source's wording. The R query likewise states the complete public account as an action without preserving that modal distinction. This is a requirement-strength issue, not evidence of provider-answer leakage.

Do not silently replace the existing query or lower a matching threshold after seeing results. Preserve the original strict target as the registered analysis, flag R04, and separately report exclusion of R04 from the paired denominator. A clearly labeled obligation-strength sensitivity may drop only the recommended outputs/process subclause from R04-M07 while retaining archival communication, repository/chat archival, privacy restriction and R04-M06/M08. Any such sensitivity must identify its exact changed predicate and remain separate from the original sixteen queries/rankings. It must not turn a shared archival word into support by itself.

## Selection and provenance limits

The original frame contains 638 Rust and 2,777 Kubernetes PRs, but the final sample is the first qualifying 2020 prefix. It is not a balanced sample across 2020–2024. All eight initial source objects are bound to archived opening heads; that proves the submitted snapshot at the event head within the retained evidence, not the first privately authored draft. Prior restoration failures and provisional reads were retained rather than deleted. All 15 excluded prefix entries are structural modifications of existing documents, not new proposal paths under the prespecified rule.

No new remote acquisition was performed by this resumed audit. The previous source-binding audit's GitHub commit/tree/path/blob records were read, and its local-byte claims were recomputed. The parent remains responsible for the requested remote sealing and final fixed-result reread.

## Original passages checked

| ID | Fixed original | Semantic passage ranges read in this audit |
| --- | --- | --- |
| R01 | [Opening snapshot](https://github.com/rust-lang/rfcs/blob/d5fe87812fc95f2699e770993848179b6c071f2c/text/0000-llvm-asm.md) | 9–10, 15–20, 31–33, 44–46, 60 |
| R02 | [Opening snapshot](https://github.com/rust-lang/rfcs/blob/6fb5bd5a6132b15bfe2d9dade6a48d7a77eb2b24/text/0000-supertrait-item-shadowing.md) | 9, 137–142, 146–235, 254–261, 315 |
| R03 | [Opening snapshot](https://github.com/rust-lang/rfcs/blob/5559913ccacbe1e6c6c5d26d33a08f9b09641c5e/text/0000-inline-asm.md) | 128–164, 213–246, 286–301, 336–377, 513–524 |
| R04 | [Opening snapshot](https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md) | 84–97, 112–144, 156–170, 329–351 |
| R05 | [Opening snapshot](https://github.com/kubernetes/enhancements/blob/6d97b64e59854ec7744d8bc3bfb9fadac29b52fe/keps/sig-network/20200103-mixed-protocol-lb.md) | 77–91, 98–117, 123, 142–148, 179–195, 252–286 |
| R06 | [Opening snapshot](https://github.com/kubernetes/enhancements/blob/50f8b89cb8f0b3d10b1b0d5bc278122abbd23c84/keps/sig-cluster-lifecycle/wgs/20200108-instance-specific-componentconfig.md) | 158–166, 208–223, 348–356 |
| R07 | [Opening snapshot](https://github.com/kubernetes/enhancements/blob/63f35ac4f5d381ffae6bb5f9bacd67dfd93ba7a7/keps/sig-node/20200110-apparmor-ga.md) | 149–156, 260–294 |
| R08 | [Opening snapshot](https://github.com/kubernetes/enhancements/blob/2cef2aacc29238c4fffad906b429cedef2dba21d/keps/sig-scheduling/20200114-taint-based-evictions.md) | 42–45, 55–65, 70–97 |

Adjacent context of one line on each side was included. The R04 PNG was not displayed by this audit; the earlier visual inspection and independent byte binding remain separate evidence.

## Reproduction

The existing `python -B docs/workstreams/research/AF-RES-033/validate_inputs.py` reproduces the source/query invariants and writes its validation receipt. It was inspected but deliberately not invoked by this auditor because it would overwrite another owned evidence file. Independent inline Python recomputed the hashes, token counts, metadata projection and prefix-exclusion joins without writing. Its assertions and outputs all completed with exit code 0.

Minimal read-only reproduction of the input checks:

```python
import hashlib, json, re, unicodedata
from pathlib import Path
p = Path('docs/workstreams/research/AF-RES-033')
load = lambda path: [json.loads(s) for s in (p / path).read_text().splitlines()]
inputs = load('inputs.jsonl')
queries = {r['recipient_id']: r for r in load('recipient/queries_sealed.jsonl')}
targets = {r['recipient_id']: r for r in load('recipient/recipient_targets.jsonl')}
sha = lambda data: hashlib.sha256(data).hexdigest()
tokens = lambda text: re.findall('[a-z0-9]+', unicodedata.normalize('NFC', text).lower())
assert len(inputs) == len(queries) == len(targets) == 8
for row in inputs:
    rid = row['recipient_id']
    raw = Path(row['snapshot_path']).read_bytes()
    source = row['original_source']
    assert sha(raw) == source['raw_sha256']
    assert sha(raw.replace(b'\r\n', b'\n')) == source['canonical_lf_sha256']
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == source['git_blob_sha']
    assert row['frozen_partial_target'] == targets[rid]['frozen_partial_target']
    for route in ('s', 'r'):
        query = row['query_' + route]
        assert query == queries[rid][route.upper()]
        assert sha(query.encode()) == row['query_' + route + '_sha256']
        assert len(tokens(query)) <= 80
    assert not set(tokens(row['query_s'])) - set(tokens(raw.decode()))
print('Eight source identities and sixteen query strings agree.')
```

No commit, branch mutation, push, source edit or query edit was performed by this auditor. Its only written artifact is this report.
