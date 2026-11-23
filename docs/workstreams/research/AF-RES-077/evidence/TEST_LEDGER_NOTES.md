# TESTS.csv — evidence classes, joins, and denominators

`TESTS.csv` contains exactly **9 records**: SC-N/E/X, MS-N/E/X and SG-N/E/X.
It is a flat CSV evidence registry with JSON cells for structured source material.
The common packets and all six reader outputs remain unchanged.

## Counts and what they measure

| Measure | Count | Meaning |
| --- | ---: | --- |
| Frozen case slots | 9 | Three research-authored specifications per project, including applicability defects |
| Native target GUI/runtime executions | **0/9** | No native case execution; this is not a measured pass rate or a claim that all nine cases are executable as frozen |
| Native pass/fail outcomes | **Unknown for all 9** | Unknown is stored explicitly, never converted to zero failures or a passing status |
| Original execution receipts for these cases | **0** | Relevant original test source and maintainer reports are separate; bounded absence does not establish historical nonexecution |
| Cases with captured auxiliary predicates | **5/9** | SC-E, SC-X, SG-N, SG-E, SG-X only |
| Complete frozen workflows executed by the auxiliary | **0/9** | No native repair/preview/undo/split/save/reopen candidate workflow was executed |
| Sealed reader files | 6 | Three A and three B, joined by brief and view |
| Chosen candidate predictions | 18 | One A and one B prediction for each case; all unexecuted |
| All candidate-by-case predictions | **39** | SC 12, MS 12, SG 15; exact strings, not 39 observations |
| Normalized A/B mechanism agreements | 3/3 brief pairs | Both views select the same normalized mechanism in each pair; no implementation-choice change is attributed to B |
| Confirmed primary samples | 0 | Existing recruitment vacancies remain; this ledger does not fill them |
| Independent causal-effect denominator | 0 | No causal estimate, source-effect rate, author-adoption effect, or time-saving estimate |

The auxiliary worker's exit code 0 describes completion of the Python probe.
It supplies no native pass and does not alter the sealed A/B predictions.
Original-source fixture parsing in MuseScore and historical-archive inspection
in Sigil are static evidence, separately labeled in `observed_facts_json`; they
do not increase the five-case auxiliary predicate count.

## Exact joins and integrity

- `test_id` is the original `packets/*-common.json` case ID; `input_case_pointer`
  locates its original object. Initial state, actions, observation list and
  condition are copied without revisions. There are 9 case-object joins and no
  omitted, added or duplicated case IDs.
- `brief_id` joins each row to two `VIEWS.csv` rows, yielding 18 case/view joins.
  The six selected IDs are SC A1/F, MS C1/local_excerpt_reset, and
  SG C1/scoped_relocation. Candidate sets match the respective reader files.
- Selected prediction text and every competing output are copied verbatim from
  the heterogeneous reader structures. `*_prediction_context_json` also retains
  the original surrounding case object. Failure/reversal criteria are preserved
  separately from post-seal observations and source interpretations.
- `view_choice_provenance_json` retains both packet and reader paths, SHA-256,
  source work/version/URLs, choice timestamps, and seal commits. The assembly
  verified all **9 distinct packet files** and
  **6 reader files** against their VIEWS hashes and exact
  Git-sealed bytes (15 distinct commit/file comparisons).
- Input/common and view packets are sealed at
  `9518c3dccbd21cda72cec715afe47eebd4dba543`. A choices are sealed at
  `7c1df93b11e06ca8b7f44ac5b7ff996879aebd09`; B choices at
  `7bc2d1f84c04b47711d72e7c110b8f927d97f4ad`.
- Existing source IDs are retained with their registry path. Original MuseScore
  test IDs come from `postseal/musescore/report.json`; Sigil post-seal code IDs
  come from its `report.json`. Where no source ID exists, an explicit local file,
  URL and SHA-256 is supplied rather than inventing an ID. For embedded Sigil
  code, both container and embedded-content hashes are retained.
- The captured auxiliary receipt's before/after input lists agree; its input and
  output SHA-256 values match current stored bytes. The worker's stdout and
  receipt hashes are cited in each of the five affected rows. No auxiliary
  execution was repeated to construct this ledger.
- CSV readback verifies exactly 9 records and 55 columns, all JSON cells,
  and all 18 selected-prediction-to-candidate-output joins.

## Evidence columns must not be collapsed

| Column | Permitted interpretation |
| --- | --- |
| `original_test_source_json` | Existing test code, inputs and expected files, or an explicit bounded source gap. A source fixture is not an execution receipt. |
| `original_execution_receipt_json` | Retrieved historical execution evidence. None establishes a result for the frozen cases. Empty current status lists are not failed/pending historical jobs. |
| `maintainer_report_json` | Contributor/maintainer/request-author statements, posted debug material, or adopted changes. These remain reports and historical facts. |
| `researcher_auxiliary_run_json` | Captured narrow Python predicates with actual command, UTC interval, exit code and fingerprints. No target/candidate implementation ran. |
| `specification_prediction_json` | Sealed candidate predictions and later explicitly unexecuted source-derived assessments. |
| `target_not_run` | `true` in every row, together with explicit unknown native pass/fail. |
| `observed_facts_json` | Typed static-file or auxiliary observations; target runtime observations are null. |
| `source_paths_hashes_urls_json` | Evidence locators and fingerprints, not additional independent works or test counts. |

## Material case limits and reversals

| Case | Consequence for interpretation |
| --- | --- |
| SC-N | Symbolic media and no native round trip. Both chosen candidates predict the same restoration. |
| SC-E | BLUE is a warning-bearing **suggestion** only under the stipulated order. Actual enumeration is unmeasured. Native commit requires dialog acceptance and checker correction; no identity confirmation does not fix generic OK behavior. p1/p2 and save/reopen remain unobserved. |
| SC-X | Synthetic 3 MiB non-media input. Sampled MD5 is equal while full SHA-256 differs for a known before/after pair. Actual edge reads are decimal 1,000,000 bytes; file size is not digest input. A legacy binding lacking an old full digest can be refused as unverified but cannot thereby be called a detected historical change. |
| MS-N | Initially false selection does not separate inherited versus cleared selection. Whole-state and scoped rollback can agree because no unrelated change or stale snapshot intervenes. |
| MS-E | Immediate flag/list/color observation after part creation is required to test inherited UI selection. The frozen checkpoint is ambiguous; reopening can erase the distinction. Both proposed local/global fixes predict the same stated successful outputs, and no whole/scoped rollback preference follows. |
| MS-X | No stored former pitch or accessible undo record; refusal/no-op is consistent with either design. Pitch60 from the other cases must not be imported into this input. |
| SG-N | The comment marker needs an explicit manual-cursor interpretation; it is not Sigil's automatic `hr` marker. This between-node split exercises an existing branch, not the historical same-file repair. |
| SG-E | Native nested-folder move to `Text/parts/ch1_tail.xhtml` is unsupported in 0.9.17. Fixed category folders/slash rejection/import normalization are direct source constraints. No flat-name or external-ZIP substitute was used. |
| SG-X | Same-document duplicate IDs violate uniqueness assumptions; the source can collapse to the later section. The auxiliary strict resolver cannot establish FIRST versus SECOND intent. Predicted refusal was not executed. |

Sigil's later historical diagnosis moved **both reference and target together**,
unlike frozen N/E. The retained public fixture additionally has a literal href
resolving to a missing archive member and no golden output EPUB. Its metadata and
later tester statements do not establish the original reporter's build or a
frozen-case result. MuseScore's historical patch adopted **global constructor
deselection**, the competing scope to both readers' local preference; that is
adoption evidence, not proof that either implementation passed the preservation
conditions. Shotcut's closed issue retained a final author report of black
output, with cause and successful recovery unknown.

These facts constrain applicability and the strength of a proposed preference.
They do not retroactively change sealed inputs, predictions or choices. No
source report or ported predicate earns a target pass. Failure criteria and
minimum contrary evidence remain prospective where no implementation ran.

## Reproduction and scope

Run `python evidence/assemble_tests.py` from the workstream directory (or pass the
script's full path). The helper reads local evidence and Git objects, validates
the joins/hashes, and rewrites only `TESTS.csv` and this note. It makes no network
requests, launches no target application, reruns no auxiliary probe, changes no
sealed input, and creates no commit. The ledger is a structured evidence export;
no workbook formula or native application outcome is implied by CSV generation.

The capture interval and runtime details remain those in the existing auxiliary
receipt; assembly time is not substituted for execution time. The output CSV
SHA-256 is `98cd0dbedf41de1f73d00cb3e635614cae873c925a221526d9c8359f990f0e03`.
