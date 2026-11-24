# AF-RES-188 HANDOFF

**Worker verdict: PARTIAL.** Research and documentation committed; do not promote the worker verdict to DONE based on a central state transition. No software installation, new coordinate transformation, PROJ execution, benchmark comparison, paid API, or independent review performed.

## Fixed input / result
- Branch: `work/research-af-res-188`; owned path: `docs/workstreams/research/AF-RES-188/`.
- Planning baseline: `0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6`. Actual integration start: `72cf39aea54e2de2ba78a245593aefdc40205a16`. Dependency AF-RES-179: `51e726b67b53e00f0134b16bd762b3a684b86d04`, worker PARTIAL; no other round dependency waited on.
- **Result commit immediately before this handoff:** `4f7f76d981f10b6d6efbfe396751a1180b8dbd85`. [Fixed RESULT](https://github.com/laadkke-arch/agentflow-open/blob/4f7f76d981f10b6d6efbfe396751a1180b8dbd85/docs/workstreams/research/AF-RES-188/RESULT.md), [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/4f7f76d981f10b6d6efbfe396751a1180b8dbd85/docs/workstreams/research/AF-RES-188/SELF_CHECK.md), [source ledger](https://github.com/laadkke-arch/agentflow-open/blob/4f7f76d981f10b6d6efbfe396751a1180b8dbd85/docs/workstreams/research/AF-RES-188/sources.jsonl).
- Other files: SCOPE.md, frame.csv, points.csv, operations.csv, answers.csv, CONTRASTS.md. Read the result, the source rows named there and the point/operation tables before extending.
- Commit chain: scope `67e998698aee367e41928d95abea61ea63b4a39a`; source/frame `4a9930731ddc622a475d2f731a6eee166784d80d`; point/operation `b45c2eeb38b41ad8373ea6653cf148604e6c46d7`; contrasts/answers `9b24acf0106cde88f19177669d7d90c9b32daec0`; recovered mirror flags and added evidence `349ae4e2515afb79028b49d49ac332f5e0d10f36`; final tables/self-check `4f7f76d981f10b6d6efbfe396751a1180b8dbd85`. No write outside owned path; dot-control.json untouched.

## Delivered / limits
- 50 distinct URL/source IDs in ledger, 46 directly opened, 4 access failures (X01/X02/X06/X19); 31 qualifying primary source documents, 14 lineages. OS 6/5, EPSG/PROJ 10/5, tests 5/4, user/maintainer event sources 3/4, calibration/tidal 7/4. Overall 22 minimum exceeded but event category short one, and strictly within the original #1534 recruitment boundary only 1 qualifying event document (short 3). Do not count mirrored OS test rows or same-event logs as independent events. 15 directly opened exclusions preserved.
- Six question slots retained, four unique reproduced point IDs TP01, TP02, TP03, TP21. Two reproduced test tables agree on these selected rows; direct OS datum flag key checked. Original OS ZIP not retrieved; directly verified original rows **0/6**, explicit official per-point tolerances **0/6**. No claim of certified absolute accuracy, nor proof of strict mainland interior merely from flag 1 (possible coastal buffer). Thus the required directly authenticated horizontal and height point condition is still unmet. TP31/32 differences in other reproduced rows warn against assuming all copies identical. See points.csv for full preserved values and limitations, not a new calculation.
- #1534 reported coordinate discrepancy preserved, but original reporter's effective operation/grid not established. Maintainer candidates (including rail-specific and OSTN15 missing grids) are not the reporter's execution. E2/E3 remain unfilled under direct-link/eligibility rule; linked China CRS discussion was excluded for no coordinate-output pair. #2173 is a separately labelled supplemental event: published debug log shows vertical grid opened yet ballpark vertical was selected, while horizontal transformation was performed; corrected compound CRS reply did not supply a new numeric output. Two distinct user events total, only one in fixed recruitment frame. No evidence to claim that every grid-present path succeeds.
- Conditional recommendation: GB mainland horizontal-only needs appropriate OSTN15 data and CRS/axis/units; mainland ODN height adds OSGM15 GB vertical grid; Scilly St Marys and Isle of Man Douglas02 have different vertical reference surfaces; Northern Ireland Belfast is a separate branch. Ask region/height reference if unknown, and distinguish accuracy/availability/candidate from actual selected operation. Calibration and tidal station comparisons support scope/epoch/datum-bound evidence, not interchangeable offsets. Manufacturer MC6 numeric certificate values remain unverified. No DB/API/ranking decision.
- SELF_CHECK Q1 O03 guide canonical URL is https://www.ordnancesurvey.co.uk/documents/resources/guide-coordinate-systems-great-britain.pdf ; the datum flag PDF linked alongside it is O04 https://www.ordnancesurvey.co.uk/documents/resources/updated-transformations-uk-ireland-geoid-model.pdf . Use sources.jsonl for canonical mappings, including test code T03–T05.

## Verification and exact next action
Self-check: same worker only; directly re-read all nine representative files from fixed result commit, parsed source ledger (50 distinct IDs/URLs; counts above), checked six point rows, Q1–Q7 rows and required initial three table headers and final exactly three weakness rows. RESULT blob `4aed98280819d87e88b5d758adf5f918a765bd39`, SELF_CHECK blob `45a3e6af25617b05029e460ef35cc735be3d4e1b`, ledger blob `946373e3c58a9ff7964d86e242e5696fd6a43a60`. No independent reviewer or executed checkout/CI/contract checks. The GitHub connector was used instead of a local checkout; the official ZIP binary fetch was unavailable. Do not infer checker pass or official archive validity from this readback.

**First action for Codex Cloud / successor:** retrieve the actual OS publisher developer pack in an isolated temporary directory, not another mirror. If the exact URL changed, reopen the official resources page and follow its current developer pack link; preserve both attempted and resolved URL. For the following commands assume a fresh authorized checkout and ordinary public network access; do not change the control file or write outside owned path in the repository. Save any new evidence in owned path only and commit in a successor update. The commands are proposed, not executed:

```sh
git fetch origin work/research-af-res-188
git checkout 4f7f76d981f10b6d6efbfe396751a1180b8dbd85
git diff --name-only 72cf39aea54e2de2ba78a245593aefdc40205a16 HEAD
tmp=$(mktemp -d)
curl -fL --retry 2 'https://www.ordnancesurvey.co.uk/documents/resources/OSTN15-OSGM15-DevelopersPack.zip' -o "$tmp/OS-pack.zip"
sha256sum "$tmp/OS-pack.zip"
unzip -l "$tmp/OS-pack.zip"
unzip -q "$tmp/OS-pack.zip" -d "$tmp/os"
find "$tmp/os" -type f
find "$tmp/os" -type f -iname '*Test*' -print
find "$tmp/os" -type f -iname '*Test*.txt' -exec grep -nE '^TP(01|02|03|21|31|32),' {} +
```

Inspect the original input/output headers, IDs/order, height datum flags, units, instructions and any explicit tolerances; compare all selected rows against points.csv, and investigate discrepancies TP31/TP32 (and other differences recorded in CONTRASTS.md). Retain actual line numbers, archive SHA256, publisher URL, version and date. If official test instructions have no tolerance, explicitly record that rather than substituting OS aggregate accuracy or the third-party test assertions. Confirm eligibility of mainland points by original description/area where possible. A failed ZIP download is a failed observation, not authorization to use a mirror as official evidence.

Next obtain the #1534 reporter's actual version/operation/path/network/warnings only if present in public original record; do not merge maintainer candidates with reporter output. Inspect direct links for the two eligible original reports (leave unfilled otherwise). This task excludes new PROJ runs; a separate authorized runtime study could collect fixed input/CRS/axis/grid availability and selected operation with version and AOI, but no such results are implied here.

Repository checks, if available in Codex checkout (no changes to central task records):
```sh
python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
python scripts/check.py --require-git
```
AGENTS.md also specifies `workbench.session start` and `workbench.session check --fetch`; if a fresh contract is required, write the generated contract only inside owned path (not the example docs/tasks central path), using actual branch context and the documented CLI:
```sh
python -m workbench.session start AF-RES-188 --allow docs/workstreams/research/AF-RES-188/ --output docs/workstreams/research/AF-RES-188/session.json --fetch
python -m workbench.session check docs/workstreams/research/AF-RES-188/session.json --fetch
```
Run on a clean authorized successor branch/worktree if needed, not to modify this fixed result. Do not report PASS until actual output is available.

**Index proposal:** AF-RES-188 — OSTN15/OSGM15 offline recommendation conditional on CRS, area, height datum, effective operation and official control row; PARTIAL (31 primary sources, 6 reproduced point slots/4 IDs, original pack and tolerance unverified, one event-source deficit; #2173 vertical fallback counterexample).
