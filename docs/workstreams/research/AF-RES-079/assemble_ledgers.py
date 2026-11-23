"""Normalize retained research receipts; does not fetch or infer test success.

Run from any directory. Stream ledgers and the original prospective seal remain
the evidence of record. This script only builds the common source/frame/observation
views. Relation adjudication is authored separately in relations.csv.
"""
import csv
import datetime as dt
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent


def jl(path):
    return [json.loads(line) for line in (BASE / path).read_text().splitlines() if line.strip()]


def j(path):
    return json.loads((BASE / path).read_text())


def dump(path, value):
    (BASE / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def text(value):
    if value is None:
        return ""
    return json.dumps(value, ensure_ascii=False, sort_keys=True) if isinstance(value, (dict, list)) else str(value)


def csvout(path, rows):
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with (BASE / path).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({k: text(v) for k, v in row.items()})


streams = ["gis", "oss", "root", "standards"]
if (BASE / "streams/pil_archive/sources.jsonl").exists():
    streams.append("pil_archive")
sources = []
for stream in streams:
    for x in jl(f"streams/{stream}/sources.jsonl"):
        source = {
            "source_id": x["source_id"], "stream": stream,
            "independent_work_id": x.get("independent_work_id", x.get("work_id")),
            "publisher": x.get("publisher"), "title": x.get("title", x.get("section")),
            "original_url": x.get("original_url", x.get("source_url", x.get("url"))),
            "actually_opened_url": x.get("actual_opened_url", x.get("actually_opened_url", x.get("opened_url"))),
            "arrived_url": x.get("arrived_url"),
            "fixed_location": x.get("fixed_location", x.get("fixed_locator", x.get("fixed_url"))),
            "edition": x.get("edition"), "section": x.get("section"),
            "checked_utc": x.get("checked_utc"),
            "reader": x.get("reader", "root" if stream == "root" else "gis_evidence tool agent" if stream == "pil_archive" else f"{stream}_evidence tool agent"),
            "access_status": x.get("access_status", x.get("access")),
            "directly_read": x.get("directly_read", x.get("direct_read", x.get("access_status", x.get("access")) in ("direct_read", "directly_read", "direct_primary_text_read"))),
            "counts_minimum": bool(x.get("counts_minimum", x.get("count_toward_minimum", x.get("counted_independent_work", x.get("counted", False))))),
            "count_reason": x.get("count_reason"), "finding": x.get("finding"),
            "counterevidence": x.get("counterevidence"),
            "limitation": x.get("limitation", x.get("limitations")),
            "http_status": x.get("http_status", x.get("current_http_status")),
            "http_chain": x.get("http_chain", x.get("current_redirect_chain")),
            "sha256": x.get("sha256", x.get("body_sha256", x.get("content_sha256"))),
            "stream_record": f"streams/{stream}/sources.jsonl#{x['source_id']}",
        }
        # Source records distinguish a body read via web from a failed independent
        # shell GET; a 403 shell receipt does not erase the successful web read.
        source["opened_url_provenance"] = "explicit stream acquisition field" if source["actually_opened_url"] else "missing; original_url is not substituted as an observed fetch"
        if not source["fixed_location"]:
            source["fixed_location"] = {"url": source["original_url"], "edition": source["edition"], "section": source["section"], "sha256": source["sha256"]}
        if not source["finding"] and not source["directly_read"]:
            source["finding"] = "원문 본문 미확인. 접근 실패/미취득 상태만 관측했으며 본문 주장이나 원저작 수에 산입하지 않는다: " + str(source["access_status"])
        sources.append(source)
counted_work_ids = [x["independent_work_id"] for x in sources if x["counts_minimum"]]
assert len(counted_work_ids) == len(set(counted_work_ids)), "duplicate independent-work representative"
if (BASE / "streams/root/pin-map.json").exists():
    pin_map = {x["original_source_id"]: x for x in j("streams/root/pin-map.json")}
    for source in sources:
        if source["source_id"] in pin_map:
            pin = pin_map[source["source_id"]]
            source["original_locator_before_pin"] = source["fixed_location"]
            source["fixed_location"] = pin["fixed_url"]
            source["fixed_locator_provenance"] = pin["correspondence"]
            source["pin_source_id"] = pin["pin_source_id"]
with (BASE / "sources.jsonl").open("w") as f:
    for source in sources:
        f.write(json.dumps(source, ensure_ascii=False) + "\n")
source_ids = {x["source_id"] for x in sources}
source_map = {x["source_id"]: x for x in sources}
root_runs = {x["run_id"]: x for x in jl("streams/root/runtime-observations.jsonl")}

gis = j("streams/gis/events.json")
oss = j("streams/oss/events.json")
controls = j("streams/root/controls.json")
hist_path = BASE / "streams/oss/historical/paired-observations.jsonl"
historical = jl("streams/oss/historical/paired-observations.jsonl") if hist_path.exists() else []
assert all(x["native_pair_observed"] for x in historical)
historical_events = {x["event_id"] for x in historical}
gis_native_path = BASE / "streams/gis/historical/observations.jsonl"
gis_native = jl("streams/gis/historical/observations.jsonl") if gis_native_path.exists() else []
gis_native_events = {x["event_id"] for x in gis_native if x["actual_pair_run"]}
if gis_native:
    assert j("streams/gis/historical/native-summary.json")["validation_exit_code"] == 0
    assert gis_native_events == {"G02", "G03", "G04"}
historical_events |= gis_native_events
archive_available = (BASE / "streams/pil_archive/archive-verification.json").exists()
if archive_available:
    archive_check = j("streams/pil_archive/archive-verification.json")
    assert archive_check["exit_code"] == 0 and all(x["matches_dsc"] for x in archive_check["checks"])
frame = []
for events, domain in ((gis, "GIS_GDAL"), (oss, "OSS_SCIPY")):
    for slot, e in enumerate(events, 1):
        frame.append({
            "event_id": e["event_id"], "stratum": "natural", "frame": domain,
            "allocated_slot": slot, "recruitment_original_rank": e["recruitment_original_rank"],
            "selected_notice": e.get("notice_url", e.get("sources", [])),
            "old_version": e.get("old_edition", e.get("old_version")),
            "new_version": e.get("new_edition", e.get("new_version")),
            "status": "SELECTED_TWO_SOURCE_EDITIONS", "missing_reason": "",
            "historical_native_pair": e["event_id"] in historical_events,
            "historical_pair_evidence": ("streams/gis/historical/observations.jsonl" if e["event_id"] in gis_native_events else "streams/oss/historical/paired-observations.jsonl") if e["event_id"] in historical_events else "not observed",
            "screening_record": f"streams/{'gis' if domain == 'GIS_GDAL' else 'oss'}/recruitment.csv",
            "first_seal_commit": "dfdfe1b82ee1921f2f90c723dbd9fe8d22138ead",
            "source_checkpoint": "2f0afa4d415a9e97b6f3d510b23958aeafd54a34",
        })
for e in controls:
    frame.append({
        "event_id": e["event_id"], "stratum": "control", "frame": e["allocation"],
        "allocated_slot": 1, "recruitment_original_rank": "preselected_control",
        "selected_notice": e["declaration_sources"], "old_version": e["old_version"],
        "new_version": e["new_version"],
        "status": "SELECTED_ORIGINAL_ARCHIVE_PARTIAL" if e["event_id"] == "C02" and not archive_available else "SELECTED_TWO_SOURCE_EDITIONS",
        "missing_reason": "PIL1.1.7 original source archive not independently retrieved" if e["event_id"] == "C02" and not archive_available else "",
        "acquisition_supplement": "streams/pil_archive/archive-verification.json; original tarball matches Debian descriptor, PGP trust chain not verified" if e["event_id"] == "C02" and archive_available else "",
        "historical_native_pair": False, "screening_record": "SCOPE.md#2",
        "first_seal_commit": "dfdfe1b82ee1921f2f90c723dbd9fe8d22138ead",
        "source_checkpoint": "dd81c973210650690fa054e6c967919d1a1206db",
    })
csvout("frame.csv", frame)

events = {x["event_id"]: x for x in gis + oss + controls}
observations = []
for stream in ("gis", "oss", "root"):
    for x in jl(f"streams/{stream}/observations.jsonl"):
        e = events[x["event_id"]]
        refs = x.get("evidence_sources", x.get("evidence_source_ids", x.get("source_ids", [])))
        cited_times = [source_map[r]["checked_utc"] for r in refs if r in source_map and source_map[r]["checked_utc"]]
        cited_times += [root_runs[r]["checked_utc"] for r in x.get("run_ids", []) if r in root_runs]
        locations = [v if v.startswith(("https://", "http://", "streams/")) else f"streams/{stream}/{v}" for v in x.get("evidence_locations", [])]
        observation = {
            "observation_id": x["observation_id"], "event_id": x["event_id"],
            "stratum": e["stratum"], "question": x["question"],
            "old_id": e["old_id"], "new_id": e["new_id"],
            "old_edition": e.get("old_edition", e.get("old_version")),
            "new_edition": e.get("new_edition", e.get("new_version")),
            "input_environment": x.get("input_environment", {"input": x.get("input"), "environment": x.get("environment")}),
            "expected": x["expected"],
            "old_actual_or_prediction": x.get("old_observation_or_prediction", "see combined observation; no independent historical execution claimed"),
            "new_actual_or_prediction": x.get("new_observation_or_prediction", x.get("actual_or_unobserved", x.get("observed"))),
            "evidence_kind": x.get("observation_kind", x.get("evidence_kind")),
            "historical_pair_executed": False,
            "current_supplement_executed": x.get("executed", bool(x.get("run_ids")) or "current" in x.get("observation_kind", "").lower()),
            "source_ids": [r for r in refs if r in source_ids],
            "evidence_locations": locations,
            "evidence_artifacts": [f"streams/{stream}/{r}" for r in refs if r not in source_ids] + [f"streams/{stream}/observations.jsonl#{x['observation_id']}"] + [f"streams/root/runtime-observations.jsonl#{r}" for r in x.get("run_ids", [])],
            "norm_behavior_discrepancy": x.get("norm_behavior_mismatch", x.get("norm_behavior_disagreement", x.get("norm_behavior_discrepancy"))),
            "judgment": x.get("judgment", x.get("verdict", x.get("question_judgment"))),
            "limitation": x.get("limitation", x.get("limit", "not a paired historical runtime result")),
            "checked_utc": x.get("checked_utc") or max(cited_times, default=None),
            "timestamp_basis": "stream observation time" if x.get("checked_utc") else "latest cited source/run receipt; original acquisition/run timestamps remain separately retained",
            "reader": x.get("observer", "root" if stream == "root" else f"{stream}_evidence tool agent"),
        }
        observations.append(observation)

for h in historical:
    e = events[h["event_id"]]
    observations.append({
        "observation_id": "H-" + h["pair_id"], "event_id": h["event_id"], "stratum": "natural", "question": h["question"],
        "old_id": e["old_id"], "new_id": e["new_id"], "old_edition": h["old_version"], "new_edition": h["new_version"],
        "input_environment": {"old_input": h["old_input"], "new_input": h["new_input"], "old_input_sha256": h["old_input_sha256"], "new_input_sha256": h["new_input_sha256"], "exact_input_equal": h["exact_recorded_input_equal"], "input_mapping": h["input_mapping"], "environment": h["environment"]},
        "expected": "compare required values, type/shape, ordering, error and warning policy under the sealed P1/P2",
        "old_actual_or_prediction": {"actual_output": h["old_output"], "exception": h["old_exception"], "warnings": h["old_warnings"]},
        "new_actual_or_prediction": {"actual_output": h["new_output"], "exception": h["new_exception"], "warnings": h["new_warnings"]},
        "evidence_kind": "historical_native_pair_executed", "historical_pair_executed": True, "current_supplement_executed": False,
        "source_ids": e["sources"],
        "evidence_artifacts": ["streams/oss/historical/paired-observations.jsonl#"+h["pair_id"], "streams/oss/historical/"+h["old_file"]+"#"+h["old_row_id"], "streams/oss/historical/"+h["new_file"]+"#"+h["new_row_id"], "streams/oss/historical/paired-check.receipt.json"],
        "norm_behavior_discrepancy": {"values_equal": h["numeric_values_equal"], "representation_equal": h["output_shape_dtype_representation_equal"], "exception_type_equal": h["exception_type_equal"], "exception_message_equal": h["exception_message_equal"], "warning_types_equal": h["warning_types_equal"]},
        "judgment": h["comparison"], "limitation": h["limits"] + " O02 simps/cumtrapz not separately executed; multiple comparisons reuse one natural event.",
        "checked_utc": h["checked_utc"], "reader": "oss_evidence tool agent; root incorporates completed pair receipt",
    })
for x in gis_native:
    e = events[x["event_id"]]
    prefix = "docs/workstreams/research/AF-RES-079/"
    artifacts = [p.removeprefix(prefix) for p in x["command_receipts"] + x["raw_outputs"]]
    artifacts += ["streams/gis/historical/observations.jsonl#" + x["observation_id"], "streams/gis/historical/native-summary.json", "streams/gis/historical/environment-packages.json", "streams/resume-gis/audit.json"]
    limits = list(x["limitations"])
    if x["event_id"] == "G04":
        limits.append("Matched14.0.2 denotes Python pyarrow; actual writer metadata reports parquet-cpp-arrow14.0.1 for GDAL3.8 and14.0.2 for GDAL3.9. GN07 is the separate same3.9-environment encoding contrast.")
    observations.append({
        "observation_id": x["observation_id"], "event_id": x["event_id"], "stratum": "natural", "question": x["question"],
        "old_id": e["old_id"], "new_id": e["new_id"], "old_edition": e.get("old_edition"), "new_edition": e.get("new_edition"),
        "input_environment": {"input": x["input"], "environment": x["environment"], "run_ids": x["run_ids"]},
        "expected": x["expected"], "old_actual_or_prediction": "Actual named old/new run outputs are retained in the cited raw logs; use run_ids to distinguish editions.",
        "new_actual_or_prediction": x["observed"], "evidence_kind": x["evidence_kind"],
        "historical_pair_executed": x["actual_pair_run"], "historical_single_edition_executed": not x["actual_pair_run"], "current_supplement_executed": False,
        "source_ids": x["source_ids"], "evidence_artifacts": artifacts,
        "norm_behavior_discrepancy": x["norm_behavior_discrepancy"], "judgment": x["question_judgment"],
        "limitation": limits, "checked_utc": x["checked_utc"], "reader": "gis_evidence original runs; gis_resume_audit non-blind receipt validation and targeted replay; root integrates",
    })
if archive_available:
    for x in jl("streams/pil_archive/observations.jsonl"):
        observations.append({
            "observation_id": x["observation_id"], "event_id": "C02", "stratum": "control", "question": x["question"],
            "old_id": controls[1]["old_id"], "new_id": controls[1]["new_id"],
            "old_edition": "PIL1.1.7 original upstream tarball; Debian-preserved archive", "new_edition": controls[1]["new_version"],
            "input_environment": x["input"], "expected": x["expected"], "new_actual_or_prediction": x["observed"],
            "evidence_kind": x["kind"], "historical_pair_executed": False, "current_supplement_executed": False,
            "source_ids": x["sources"], "evidence_artifacts": ["streams/pil_archive/observations.jsonl#"+x["observation_id"], "streams/pil_archive/archive-verification.json"],
            "judgment": x["judgment"], "limitation": "source acquisition/digest check does not execute original PIL; PGP signature not verified",
            "checked_utc": archive_check["checked_utc"], "reader": "gis_evidence tool agent",
        })

def url_action(status, chain, requested, arrived):
    # The final non-2xx outcome takes priority over a preceding redirect.
    if not isinstance(status, int) or not 200 <= status < 300:
        return "hold"
    redirects = [r for r in chain if 300 <= r.get("status", 0) < 400]
    if redirects:
        if not all(r["status"] in (301, 308) for r in redirects):
            return "hold"
        return "repair_location_keep_record" if arrived else "hold"
    return "keep_record" if requested.split("#")[0] == (arrived or "").split("#")[0] else "hold"

ghttp = jl("streams/gis/http-acquisition.jsonl")
rhttp = {r["probe_id"]: r for r in jl("streams/root/http-probes.jsonl")}
policy = []
for event_id, e in events.items():
    if event_id.startswith("G"):
        old = [r for r in ghttp if r["requested_url"] == e["old_url"]][-1]
        status, chain = old.get("status"), old.get("redirect_chain", [])
        refs = e["primary_sources"]
        receipt = "streams/gis/http-acquisition.jsonl#" + old["key"]
    elif event_id.startswith("O"):
        old = next(r for r in e["observed_http"] if r["role"] == "live_old")
        status, chain = old.get("http_status"), old.get("chain", [])
        refs = e["sources"] + [f"OS-DOC-{event_id}-live_old"]
        receipt = f"streams/oss/http-observations.jsonl#{event_id}:live_old"
    else:
        old = rhttp[e["http_probe_old"]]
        status, chain = old.get("status"), old.get("chain", [])
        refs = e["declaration_sources"]
        receipt = "streams/root/http-probes.jsonl#" + e["http_probe_old"]
    action = url_action(status, chain, old["requested_url"], old.get("arrived_url"))
    row = {
        "event_id": event_id, "stratum": e["stratum"],
        "request_url": old["requested_url"], "arrived_url": old.get("arrived_url"),
        "final_http_status": status, "current_chain": chain,
        "fragment_present": old.get("requested_fragment_present", old.get("target_text_present")),
        "checked_utc": old["checked_utc"], "U_action": action,
        "historical_redirect_verified": False,
        "receipt": receipt,
        "independent_identity_criterion": "versioned publisher declaration and implementation/source contract; see relations.csv",
        "historical_native_criterion_available": event_id in historical_events,
        "real_production_record_supplied": False,
        "source_ids": [r for r in refs if r in source_ids],
    }
    policy.append(row)
    observations.append({
        "observation_id": f"{event_id}-HTTP-U", "event_id": event_id, "stratum": e["stratum"],
        "question": "Q1/Q4:prospectively_sealed_URL_only_U",
        "old_id": e["old_id"], "new_id": e["new_id"],
        "input_environment": {"requested_url": row["request_url"], "method": "GET"},
        "expected": "apply SCOPE U without reading page semantics; final failure remains hold",
        "new_actual_or_prediction": {"status": status, "arrived_url": row["arrived_url"], "chain": chain, "fragment_present": row["fragment_present"]},
        "evidence_kind": "current_HTTP_observation_and_sealed_policy_application",
        "historical_pair_executed": False, "current_supplement_executed": False,
        "HTTP_request_executed": True,
        "source_ids": row["source_ids"], "evidence_artifacts": [receipt],
        "judgment": action,
        "limitation": "current response only; not past redirect history or functional equivalence; fragments are not sent in HTTP",
        "checked_utc": row["checked_utc"], "reader": "root aggregates retained GET receipts",
    })
csvout("observations.csv", observations)
dump("evidence/url-policy-comparison.json", {"sealed_rule": "SCOPE.md#4", "rows": policy, "no_unobserved_production_merge_claim": True, "U_cannot_express_split": True})
dump("evidence/ledger-counts.json", {
    "assembled_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    "source_rows": len(sources), "independent_works": sum(x["counts_minimum"] for x in sources),
    "counted_work_ids": [x["independent_work_id"] for x in sources if x["counts_minimum"]],
    "source_rows_by_stream": {s: sum(x["stream"] == s for x in sources) for s in streams},
    "independent_works_by_stream": {s: sum(x["stream"] == s and x["counts_minimum"] for x in sources) for s in streams},
    "direct_body_read_rows": sum(x["directly_read"] for x in sources),
    "frame_rows": len(frame), "natural_pairs_with_two_source_editions": sum(x["stratum"] == "natural" and x["status"] == "SELECTED_TWO_SOURCE_EDITIONS" for x in frame),
    "natural_allocated": sum(x["stratum"] == "natural" for x in frame), "controls_allocated": sum(x["stratum"] == "control" for x in frame),
    "controls_with_complete_independent_source_artifacts": sum(x["stratum"] == "control" and x["status"] == "SELECTED_TWO_SOURCE_EDITIONS" for x in frame),
    "control_C02_original_archive_partial": not archive_available,
    "observations": len(observations), "non_HTTP_observations": len(observations) - len(policy),
    "current_HTTP_policy_rows": len(policy),
    "historical_native_pairs_at_source_checkpoint": 0,
    "historical_native_event_pairs_current": len(historical_events),
    "historical_native_event_ids": sorted(historical_events),
    "historical_native_comparison_rows": len(historical),
    "historical_native_comparison_rows_scope": "OSS individual pair rows only; do not add to GIS grouped observations as independent events",
    "oss_native_event_pairs": len({x["event_id"] for x in historical}),
    "gis_native_event_pairs": len(gis_native_events),
    "gis_native_observation_groups": len(gis_native),
    "gis_historical_pair_groups": sum(x["actual_pair_run"] for x in gis_native),
    "gis_same_edition_supplement_groups": sum(not x["actual_pair_run"] for x in gis_native),
    "historical_supplement_status": "validated paired receipts appended; original static/prediction rows preserved",
    "natural_U": {a: sum(r["stratum"] == "natural" and r["U_action"] == a for r in policy) for a in ("hold", "keep_record", "repair_location_keep_record")},
    "control_U": {a: sum(r["stratum"] == "control" and r["U_action"] == a for r in policy) for a in ("hold", "keep_record", "repair_location_keep_record")},
})
print(json.dumps({"sources": len(sources), "counted_independent_works": sum(x["counts_minimum"] for x in sources), "frame": len(frame), "observations": len(observations)}, ensure_ascii=False))
