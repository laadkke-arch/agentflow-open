"""Join native receipts without modifying the sealed sample or earlier GIS files."""
from pathlib import Path
import datetime
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
REL = "docs/workstreams/research/AF-RES-079/streams/gis/historical/"


def clean(value):
    if isinstance(value, float) and not math.isfinite(value):
        return {"non_finite_float": "NaN" if math.isnan(value) else str(value)}
    if isinstance(value, list):
        return [clean(item) for item in value]
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items()}
    return value


def output(label):
    text = (ROOT / (label + ".log")).read_text()
    # Native stderr warnings can precede/follow the probe JSON. Preserve raw log.
    return clean(json.JSONDecoder().raw_decode(text[text.index("{"):])[0])


def receipt(label):
    return json.loads((ROOT / (label + ".json")).read_text())


def artifact(name):
    path = ROOT / name
    return {"path": REL + name, "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


environments = {name: output("details-" + name) for name in
                ["gdal37", "gdal38a10", "gdal38", "gdal39"]}
raw_labels = []
for phase in ["g03", "g04", "arg"]:
    raw_labels += [row["label"] for row in
                   json.loads((ROOT / ("matrix-" + phase + ".json")).read_text())["runs"]]
raw_labels += ["contract-" + row["label"] for row in
               json.loads((ROOT / "matrix-contract.json").read_text())]
native_runs = {label: {"receipt_file": REL + label + ".json",
                       "raw_output_file": REL + label + ".log",
                       "command": receipt(label)["command"],
                       "exit_code": receipt(label)["exit_code"],
                       "output": output(label)} for label in raw_labels}
observations = []


def add(number, event, question, inputs, expected, labels, sources, observed,
        judgment, limits, pair=True, mismatch=""):
    observations.append({
        "observation_id": "GN" + str(number).zfill(2), "event_id": event,
        "question": question, "input": inputs,
        "environment": "See native-summary.json environment profiles and environment-packages.json; pinned version strings, distinct binary builds/PROJ remain.",
        "expected": expected, "observed": observed,
        "output": {label: native_runs[label]["output"] for label in labels},
        "evidence_kind": "native_execution_of_downloaded_historical_binary",
        "source_ids": sources, "run_ids": labels,
        "command_receipts": [native_runs[label]["receipt_file"] for label in labels],
        "raw_outputs": [native_runs[label]["raw_output_file"] for label in labels],
        "commands": [native_runs[label]["command"] for label in labels],
        "actual_pair_run": pair, "executed": True,
        "norm_behavior_discrepancy": mismatch, "question_judgment": judgment,
        "limitations": limits, "actor": "gis_evidence tool agent",
        "location": "ChatGPT cloud Linux, task-local conda-forge environments",
        "checked_utc": max(native_runs[label]["output"]["checked_utc"] for label in labels),
        "additional_natural_events": 0, "additional_independent_works": 0,
    })


vector_input = {"path": "docs/workstreams/research/AF-RES-079/streams/gis/inputs/vector.json",
                "sha256": hashlib.sha256((ROOT.parent / "inputs/vector.json").read_bytes()).hexdigest(),
                "rows": [[1, "가", "POINT (0 0)"], [2, "b", "POINT (1 1)"]]}
boundary_input = {"path": "docs/workstreams/research/AF-RES-079/streams/gis/inputs/point-boundary.json",
                  "sha256": hashlib.sha256((ROOT.parent / "inputs/point-boundary.json").read_bytes()).hexdigest(),
                  "geometry_sequence": ["POINT (1 2)", None, "POINT EMPTY", "POINT (1 2)"],
                  "fixture_status": "Research serialization of directly read supplier boundary input; not another natural event."}
arg_input = {"binary": artifact("runs/arg-input/sealed.arg"),
             "sidecar": artifact("runs/arg-input/sealed.json"),
             "values": [1, 2, 3, -9999], "expected_nodata": -9999,
             "dtype": "Int16", "epsg": 4326, "geotransform": [0, 1, 0, 2, 0, -1]}
normal_limits = [
    "Two diagonal Point coordinates and no null values: no coordinate transformation test or general null-processing certification.",
    "CRS authority, data-axis mapping, field/Arrow nullability and actual metadata are observed; metadata version is not full specification-conformance certification.",
    "Version strings were matched for Python/NumPy/Arrow within the comparison; binary build IDs, PROJ and transitive dependencies differ, so this is not GDAL-only causal isolation.",
]
add(1, "G03", "P1", {"creation_input": vector_input, "same_file_read_twice": artifact("runs/g03-old.parquet")},
    "Existing named Parquet reader preserves fields, ordered values, geometry and CRS state.",
    ["g03-old-write", "g03-p1-old", "g03-p1-new", "contract-g03-p1-old", "contract-g03-p1-new"],
    ["G-parquet-doc-3.7", "G-parquet-doc-3.8", "G-parquet-test-3.7", "G-parquet-test-3.8"],
    "Same old-file SHA256 was read by3.7 and3.8. Both returned id Integer, label String, exact UTF-8 values/order/Point WKT, EPSG4326 and data-axis mapping[2,1]. OGR/Arrow fields are nullable; actual null counts are0.",
    "Accepted for the recorded normal fixture and properties; broader input domain remains unverified.", normal_limits)
add(2, "G03", "P2", {"same_writer_input": vector_input, "old_output": artifact("runs/g03-old.parquet"), "new_output_read_by_old_consumer": artifact("runs/g03-new.parquet")},
    "New writer output remains usable by pinned3.7 consumer while preserving required normal data.",
    ["g03-old-write", "g03-new-write", "g03-p2-old-consumer", "contract-g03-p2-old-consumer"],
    ["G-NEWS-3.8.0", "G-parquet-writer3.7", "G-parquet-writer3.8", "G-parquet-doc-3.8"],
    "3.7 output metadata is beta.1;3.8 output is1.0.0. The3.7 consumer read the latter file successfully with required fields/order/geometry/EPSG4326/[2,1]. This counters a blanket claim that edition change necessarily breaks old consumers.",
    "Conditional P2 normal-case acceptance; exact beta-version consumers and untested inputs are outside this result.", normal_limits,
    mismatch="3.8 manual says beta1 while same-version writer emits1.0.0; native output confirms implementation evidence.")
add(3, "G03", "P2", {"same_fixture": vector_input, "invalid_cases": ["COMPRESSION=invalid", "PointM layer declaration"]},
    "Unsupported compression and measured layer declaration are explicitly rejected at the same call stage.",
    ["g03-invalid-compression-3.7.0", "g03-invalid-point-m-3.7.0", "g03-invalid-compression-3.8.0", "g03-invalid-point-m-3.8.0"],
    ["G-parquet-test-3.7", "G-parquet-test-3.8"],
    "All four probes reached installed Parquet and raised recorded RuntimeError with probe exit3. These are expected feature/input rejections, not installation failures.",
    "Expected rejection matched on these two invalid inputs.",
    ["Does not test all corrupt files or all geometry dimensions; PointM is the layer declaration test, not a successful M-ordinate serialization."])
add(4, "G04", "P1", {"old_file": artifact("runs/g03-new.parquet"), "file_creation": "g03-new-write inGDAL3.8/Arrow10.0.1; reader pairGDAL3.8/3.9 bothArrow14.0.2"},
    "Existing named default-WKB read preserves the recorded normal contract.",
    ["g04-p1-wkb-3.8.0", "g04-p1-wkb-3.9.0", "contract-g04-p1-old", "contract-g04-p1-new"],
    ["G-parquet-doc-3.8", "G-parquet-doc-3.9"],
    "Same old-file hash yielded same required fields, values/order, Point WKT, EPSG4326, data-axis[2,1], nullable declarations and metadata in3.8/3.9.",
    "P1 accepted within recorded WKB fixture scope.", normal_limits)
add(5, "G04", "P2", {"same_writer_input": boundary_input, "new_struct_file_read_by_both": artifact("runs/g04-new-same-name.parquet")},
    "Unchanged GEOARROW option output must still supply geometry and CRS to the old3.8 consumer.",
    ["g04-old-write", "g04-new-same-name-write", "g04-old-reads-new-name", "g04-new-reads-new-name", "contract-g04-new-name-old-consumer", "contract-g04-new-name-new-consumer"],
    ["G-parquet-doc-3.9", "G-parquet-test-3.9", "G-gp-spec1.1"],
    "Both consumers returned exit0 for the same3.9 struct file.3.8 returned zero geometry fields/no CRS and exposed geometry.x/y plus bbox as ordinary Real attributes;3.9 returned one geometry field, EPSG4326/[2,1] and preserved null versus EMPTY. Successful open did not satisfy the old consumer's required geometry/error contract.",
    "Reject blind same-name substitution for the pinned3.8 geometry consumer, despite process success.",
    ["This is a task-contract failure, not a claim that exposing attributes from an unsupported encoding is a universal GDAL bug.",
     "Arrow version14.0.2 matched; package builds and dependencies differ. Same3.9-environment encoding contrast inGN07 separately supports representation distinction."],
    mismatch="URL/name continuity with exit0 hides geometry/CRS loss for the old consumer.")
add(6, "G04", "P2", {"writer_input": boundary_input, "renamed_legacy_output": artifact("runs/g04-new-alias.parquet"), "old_legacy_output": artifact("runs/g04-old.parquet")},
    "Version-scoped alias should retain the old interleaved function; evaluate required-field and exact-schema consumers separately.",
    ["g04-old-read", "g04-new-alias-write", "g04-old-reads-alias", "g04-new-reads-alias", "contract-g04-old-encoding", "contract-g04-alias-old-consumer", "contract-g04-alias-new-consumer"],
    ["G-parquet-doc-3.9", "G-parquet-test-3.9"],
    "GEOARROW_INTERLEAVED restored Point geometry and EPSG4326/[2,1] for3.8. Four bbox attributes appeared for3.8 but not3.9. Required id/label values/order were retained. Null→EMPTY occurred in the original3.8 interleaved output too; raw Arrow geometry null_count is0 for both old and alias files.",
    "Scoped alias supported for legacy representation. Extra fields reject exact-schema consumers only; they alone do not fail a required-id/label subset consumer. Strict null-preservation requirement already failed in the old representation.",
    ["Do not count old null→EMPTY behavior as a new migration-induced loss.",
     "An observed1.0.0 metadata string on the legacy extension is not proof of full GeoParquet1.0 conformance."])
add(7, "G04", "P2", {"same3_9_writer_input": boundary_input, "files": [artifact("runs/g04-new-same-name.parquet"), artifact("runs/g04-new-alias.parquet")]},
    "Determine whether two encoding names identify the same behavior under the same3.9 environment.",
    ["g04-new-same-name-write", "g04-new-alias-write", "g04-new-reads-new-name", "g04-new-reads-alias", "contract-g04-new-name-new-consumer", "contract-g04-alias-new-consumer"],
    ["G-parquet-doc-3.9", "G-parquet-test-3.9"],
    "Same3.9 binary and input produce struct with one null geometry underGEOARROW, and FixedSizeList with zero null geometries/EMPTY substitution underGEOARROW_INTERLEAVED. Values/order otherwise agree.",
    "Behavioral distinction supports separate encoding IDs plus a version-scoped alias, not global same-name merging.",
    ["Same-edition discriminator, not an additional natural event or independent old/new migration."], pair=False)
add(8, "G02", "P1", {"same_binary_and_sidecar": arg_input, "calls": "OpenEx with allowed_drivers=[ARG], default config in3.7/3.8/3.9"},
    "Keep the old public reader/default while retaining the required old data.",
    ["arg-default-3.7.0", "arg-default-3.8.0", "arg-default-3.9.0"],
    ["G-arg-code-3.7", "G-arg-code-3.8", "G-gdal-manager-3.8", "G-arg-reg3.9"],
    "3.7 opened;3.8 default rejected with the documented deprecation gate;3.9 rejected becauseARG is absent.3.7 already reported nodata-32767 instead of sealed-9999, so the full nodata requirement was not a passing baseline.",
    "New default-call unavailability observed; separate the pre-existing nodata limitation from the migration change.",
    ["Named-driver call tested; automatic driver detection not separately measured.", "Logged values use Float64 conversion for readable JSON; actual band type isInt16."])
add(9, "G02", "P1", {"same_binary_and_sidecar": arg_input, "change": "3.8 GDAL_ENABLE_DEPRECATED_DRIVER_ARG=YES"},
    "Determine what the explicit opt-in restores without silently changing the sealed nodata requirement.",
    ["arg-default-3.7.0", "arg-opt-in-3.8.0"],
    ["G-gdal-manager-3.8", "G-arg-test-3.8"],
    "Both read Int16 values1,2,3,-9999, expected geotransform and EPSG4326; both report nodata-32767. Opt-in restores the partial read contract but changes the default/config and does not fix nodata.",
    "Not P1 full acceptance: changed config plus original nodata mismatch. Useful bounded recovery path.",
    ["The -9999 value is preserved as a regular pixel, not recognized as nodata."])
add(10, "G02", "P2", {"source": "MEM2x2 Int16 [1,2,3,-9999], nodata-9999,EPSG4326,geotransform[0,1,0,2,0,-1]", "output_binary": artifact("runs/new.arg"), "output_sidecar": artifact("runs/new.json"), "invalid_case": "same source with2 bands"},
    "3.8 opt-in CreateCopy output must retain required raster metadata for3.7 and reject unsupported band count.",
    ["arg-write-3.8.0", "arg-old-consumer", "arg-invalid-bands"],
    ["G-arg-code-3.8", "G-arg-test-3.8", "G-arg-reg3.9"],
    "Write and old read completed; values/type/geotransform/CRS survived but nodata read back as-32767. Two-band output was explicitly rejected with exit3.3.9 has noARG driver as separately observed inenv-3.9.0.",
    "Reject full nodata-preserving P2; expected two-band error matched. Do not label the pre-existing fixed sentinel a newly introduced3.8 loss.",
    ["No3.9 writer exists in this build; no fictional replacement driver is supplied."])
add(11, "G02", "P1", {"binary": artifact("runs/arg-input/supplier-int16.arg"), "sidecar": artifact("runs/arg-input/supplier-int16.json"), "values": [-32768, 2, -3, -4]},
    "Check the supplier int16 sentinel against the actual reader's nodata metadata.",
    ["arg-sentinel-3.8.0"], ["G-arg-test-3.8", "G-arg-code-3.8"],
    "3.8 opt-in returned the-32768 pixel while declaring nodata-32767. This directly confirms the previously static fixture/implementation sentinel discrepancy.",
    "Observed limitation; not a new temporal change or independent event.",
    ["This supplemental sentinel read is one edition only."], pair=False)

validation = []
for writer, readers in [
    ("g03-old-write", ["g03-p1-old", "g03-p1-new"]),
    ("g03-new-write", ["g03-p2-old-consumer", "g04-p1-wkb-3.8.0", "g04-p1-wkb-3.9.0"]),
    ("g04-old-write", ["g04-old-read", "g04-new-reads-old"]),
    ("g04-new-same-name-write", ["g04-old-reads-new-name", "g04-new-reads-new-name"]),
    ("g04-new-alias-write", ["g04-old-reads-alias", "g04-new-reads-alias"]),
]:
    for reader in readers:
        validation.append({"writer": writer, "reader": reader,
                           "same_hash": output(writer)["output_sha256"] == output(reader)["input_sha256"]})
assert all(row["same_hash"] for row in validation)
summary = {
    "actor": "gis_evidence tool agent", "location": "ChatGPT cloud Linux",
    "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "NATIVE_SUPPLEMENT_COMPLETE_WITH_BOUNDED_RESULTS",
    "previous_snapshot": "Earlier GIS_NOTES.md and observations.jsonl retain the earlier0/4 native status; this dated supplement adds observations without changing recruitment or source judgments.",
    "native_events_examined": ["G02", "G03", "G04"],
    "native_event_numerator": 3, "natural_denominator": 4,
    "G01_status": "No rasdaman server/build; full georeferencing and writer requirements were already inapplicable, pixel-only run remains unobserved.",
    "additional_natural_events": 0, "additional_independent_works": 0,
    "environments": environments,
    "package_manifest": REL + "environment-packages.json",
    "source_versions": {"G03": "GDAL3.7.0/3.8.0 with Python3.10.13,NumPy1.26.4,Arrow10.0.1", "G04": "GDAL3.8.0/3.9.0 with Python3.10.13,NumPy1.26.4,Arrow14.0.2"},
    "confounding": "Same version strings do not imply identical rebuilds. Python,Arrow build IDs,PROJ and other dependencies differ. No claim of original release-day binaries or isolated GDAL-version causality.",
    "observations": observations, "runs": native_runs,
    "same_file_hash_links": validation,
    "validation_exit_code": 0,
    "raw_log_format": "Raw probe logs may include warnings and Python JSON NaN. Summary normalizes non-finite floats to explicit typed objects; raw outputs are retained unchanged.",
}
(ROOT / "native-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
with (ROOT / "observations.jsonl").open("w") as destination:
    for observation in observations:
        destination.write(json.dumps(observation, ensure_ascii=False, allow_nan=False) + "\n")
print(json.dumps({"observations": len(observations), "native_runs": len(native_runs),
                  "same_hash_links": len(validation), "exit_code": 0}))
