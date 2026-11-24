# LilyPond recruitment receipt

Status: **PARTIAL**. This directory records the LilyPond recruitment and supplementary source-reading work. It does not contain a completed A/B recipient comparison.

## Frozen recruitment outcome

The four preregistered GitHub issue searches returned zero items. The repository metadata states that issues are disabled and that the repository is a mirror. This is a property of the searched endpoint, not evidence that LilyPond users made no relevant requests.

The official January 2022 date and thread indexes could not be retrieved through the tested original and official alias routes. The historical mbox directory and a later monthly index were accessible, but the January 2022 material needed to establish the first chronological 40 was not. Ranked search results were used only to diagnose access and locate supplementary material. They were not substituted for chronological recruitment.

Consequently, `frame.csv` has three explicit vacancies, and `safe-cases.json` is an empty array. The candidate denominator is **unknown**, not zero. `safe-posthoc.json` contains one historical request outside the recruitment years. It preserves original-request information only and must not be promoted into the main six-case comparison.

## Reading ledger and counting

`sources.jsonl` contains 24 rows: 13 directly read independent primary works and 11 failed-access or search-only records. The 13 works are distributed as follows. These are supplementary reading counts, not completed experimental cases.

| Reading allocation | Independent primary works | Main handoff cases |
| --- | ---: | ---: |
| Discriminating official documents or original examples | 5 | 0 |
| Independent regression or failure cases | 6 | 0 |
| Supplementary works not assigned to a required allocation | 2 | 0 |
| Eligible main public handoff requests | 0 | 0 |

Sections of the same manual, repeated openings, official aliases, translated copies, and generated regression indexes were not added to the independent-work count. Four regression source files were fetched from the publisher's own documentation host. Their generated wrappers identify distinct original upstream fixture filenames. The index itself is not counted again. `regression-receipts.json` records source URLs, access times, and SHA-256 digests. Full fetched source files are temporary ignored cache material; the committed evidence is the address, exact source locator, reading notes, limitations, and retrieval digest.

No LilyPond engine was invoked. A source fixture's stated expected behavior is recorded as such and is not a successful local test result. The historical failure request and later development changes document are explicitly outside the main 2022–2025 recruitment frame. The two supplementary unallocated works do not satisfy the missing three main linked requests.

## Separation and timestamps

The packet-author parent received only recruitment status, counts, source-file locations, access failures, and safe request metadata. Substantive source findings are in `sources.jsonl`; `full-records.json` points to that ledger and records the failure to establish a main-case denominator. The parent should keep these findings hidden until the relevant recipient answers are sealed.

The manual re-opening window and individual regression HTTP receipts have instrumented UTC timestamps. Other rows explicitly identify timestamps recorded after a research phase rather than implying exact per-call timing. Search snippets and unsuccessful page opens are marked accordingly and excluded from the independent primary-work count.

## Resume and verification

The next first action is to retrieve the official January 2022 date or thread index through a working original route, preserve its metadata, and then enumerate subsequent months in chronological order until the first 40 deduplicated matching threads are available. Do not choose the first three convenient search hits. The parent has separately recorded the protocol regular-expression correction in `protocol-amendment.json`; apply that explicit amendment when recruitment resumes. The original `protocol.json` and this directory's initial receipt remain unchanged.

From the repository root, the current accounting can be recalculated without external access:

```bash
python -B - <<'PY'
import csv
import json
from collections import Counter
from pathlib import Path
p = Path('docs/workstreams/research/AF-RES-112/recruitment/lilypond')
rows = [json.loads(line) for line in (p / 'sources.jsonl').read_text().splitlines()]
print('ledger rows:', len(rows))
primary = [row for row in rows if row['unique_primary']]
print('independent primary works:', len(primary))
print('allocation:', dict(Counter(row['counting_bucket'] for row in primary)))
print('main safe cases:', len(json.loads((p / 'safe-cases.json').read_text())))
with (p / 'frame.csv').open(newline='') as stream:
    print('vacant frame rows:', len(list(csv.DictReader(stream))))
PY
```

Expected output is 24 ledger rows, 13 independent primary works, allocation 5/6/2, zero main safe cases, and three frame vacancies. JSON parsing and CSV row counts were actually checked in the shared Python environment with exit code 0. This check does not verify chronological recruitment completeness, engine behavior, recipient independence, or the unseen material.

Core files were frozen for the parent's next commit. Further findings must be added in a separately named addendum rather than changing these recruitment receipts retrospectively.
