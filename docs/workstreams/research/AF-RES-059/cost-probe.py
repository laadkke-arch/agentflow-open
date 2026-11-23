"""Measure the additional retrieval, storage and replay cost of three evidence records."""
import argparse
import csv
import json
import shutil
import time
from pathlib import Path

from catalog import HERE, HttpJournal, digest, dump, utc_now
from replay import FIXTURES, json_lines, read_archive, run_probe, setup

VIEWS = ("V0", "V1", "V2")
REPLAYS = ("redisplay", "recalculate")


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_lines(path):
    return [json.loads(row) for row in path.read_text(encoding="utf-8").splitlines()]


def compact(record):
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def collect_cases(fixtures):
    evidence = HERE / "evidence"
    runs = {(row["distribution"], row["id"]): row for row in load_lines(HERE / "runs.jsonl")
            if row["step"] == "forward"}
    controls = {row["distribution"]: row for row in load_lines(evidence / "controls.jsonl")
                if row["step"] == "relabel"}
    candidates = {case["id"]: case for case in fixtures["predictions"]}
    queries = {row["id"]: row for row in fixtures["inputs"]}
    cases = []
    selections = (
        ("LAB-PY-B", "PYP-2023.2", "B21", "verified-local"),
        ("LAB-JS-B", "NPM-0.5.42", "B21", "verified-local"),
        ("LAB-JS-B23", "NPM-0.5.42", "B23", "verified-local"),
        ("LAB-PY-C", "PYP-2023.3", "B21", "verified-local"),
        ("LABEL-PY", "PYP-2023.2", "B21", "reject-member"),
        ("LABEL-JS", "NPM-0.5.42", "B21", "reject-member"),
        ("PANDAS-v2.0.0", "PYP-2023.2", "B21", "unknown"),
    )
    for case_id, package_id, query_id, truth in selections:
        pin = candidates[package_id]
        base = runs[package_id, query_id]
        observed = controls[package_id] if truth == "reject-member" else base
        case = {
            "id": case_id, "pin": pin, "input": queries[query_id], "view_source": pin["iana"],
            "receipt": observed, "authentic_member": base["loaded"],
            "recalculation_member_sha256": base["loaded"]["sha256"],
            "truth_old_output": observed["value"] if truth != "unknown" else None,
            "truth_application": truth,
            "scope": "candidate only" if truth == "unknown" else "measured Cloud process",
        }
        cases.append(case)
    image = load_json(evidence / "grafana-image.json")
    comparison = image["npm_comparison"]
    attached = image["extracted_table_replay"]
    observed = dict(attached["values"][0], loaded=json.loads(attached["receipt"]["stdout"])["loaded"],
                    process_id=attached["receipt"]["process_id"])
    cases.append({
        "id": "GRAF-v9.4.7", "input": queries["B21"], "view_source": "2023b",
        "pin": {"id": "NPM-0.5.38", "ecosystem": "npm", "package": "moment-timezone",
                "version": "0.5.38", "iana": "2022e", "url": comparison["url"],
                "file": "moment-timezone-0.5.38.tgz", "sha256": comparison["sha256"]},
        "receipt": observed, "authentic_member": observed["loaded"],
        "recalculation_member_sha256": comparison["packed_sha256"],
        "truth_old_output": observed["value"], "truth_application": "unknown",
        "scope": "paired image/member match, 2026 replay; historical user unknown",
        "image_data_equivalence": comparison["normalized_sha256"],
    })
    return cases


def views_for(case, upstream):
    edition = case["view_source"]
    source = upstream[edition]
    raw = f"https://raw.githubusercontent.com/eggert/tz/{source['commit']}/asia"
    why = "The edition's Beirut spring transition controls the April UTC-to-local date boundary."
    v0 = {"url": raw, "why": why}
    pin = case["pin"]
    v1 = {field: pin[field] for field in ("ecosystem", "package", "version", "url", "file", "sha256")}
    receipt = case["receipt"]
    v2 = {**v1, "zone_and_utc": case["input"], "scope": case["scope"],
          "loaded_member": receipt["loaded"],
          "recorded_value": receipt["value"],
          "process_id": receipt["process_id"],
          "authentic_member_sha256": case["authentic_member"]["sha256"],
          "recalculation_member_sha256": case["recalculation_member_sha256"]}
    if case.get("image_data_equivalence"):
        v2["json_equivalence_sha256"] = case["image_data_equivalence"]
    return {"V0": v0, "V1": v1, "V2": v2}


def recalculate(case, view, record, http, root, fixtures, upstream, shared):
    data = http.get(record["url"])
    metrics = {"dependency_source_reads": 0, "dependency_source_bytes": 0, "stage_archive_read_bytes": 0}
    evidence = {"value": None, "upstream_only": None, "process": None, "metrics": metrics}
    if data is None:
        return evidence
    if view == "V0":
        label = case["view_source"]
        source = upstream[label]["Lebanon"]
        if digest(data) == source["sha256"]:
            key = case["input"]["id"]
            if key == "B21":
                key = "B21_2023b" if label == "2023b" else "B21_normal"
            evidence["upstream_only"] = fixtures["reference"][key]
        return evidence
    if digest(data) != record["sha256"]:
        evidence["archive_hash_mismatch"] = True
        return evidence
    archive_dir = root / "archives"
    archive_dir.mkdir(parents=True)
    (archive_dir / record["file"]).write_bytes(data)
    if record["ecosystem"] == "npm":
        required = fixtures["node_dependency"]["filename"]
        common = shared / required
        shutil.copyfile(common, archive_dir / required)
        metrics["dependency_source_reads"] += 1
        metrics["dependency_source_bytes"] += common.stat().st_size
    metrics["stage_archive_read_bytes"] = len(data) + metrics["dependency_source_bytes"]
    isolated = root / "isolated"
    setup(case["pin"], archive_dir, isolated, fixtures)
    proc, observed = run_probe(isolated, case["id"] + "-" + view, record["ecosystem"],
                               [case["input"]], "exact")
    evidence["process"] = proc
    readings = observed.get("records", [])
    if not readings or "value" not in readings[0]:
        return evidence
    loaded = readings[0].get("loaded", observed.get("loaded"))
    if view == "V2" and loaded["sha256"] != record["recalculation_member_sha256"]:
        evidence["archive_hash_mismatch"] = True
        return evidence
    evidence.update(value=readings[0]["value"], loaded=loaded)
    return evidence


def score(case, view, record, mode, evidence):
    value = None
    rejected = bool(evidence.get("archive_hash_mismatch"))
    if view == "V2":
        valid = record["loaded_member"]["sha256"] == record["authentic_member_sha256"]
        rejected |= not valid
        if valid and mode == "redisplay":
            value = record["recorded_value"]
    if mode == "recalculate":
        value = evidence.get("value")
    if rejected:
        output = "reject-receipt"
    elif value is not None:
        output = "redisplayed" if mode == "redisplay" else "recalculated"
        if case["truth_old_output"] is None:
            output += "-candidate"
    else:
        output = "upstream-only" if evidence.get("upstream_only") else "held"
    application = "held"
    if rejected:
        application = "reject-member"
    elif view == "V2" and case["truth_application"] == "verified-local":
        if mode == "redisplay" or value is not None:
            application = "verified-local"
    old_truth = case["truth_old_output"]
    if old_truth is None:
        score_value = "unscored"
    elif rejected:
        score_value = "correct" if case["truth_application"] == "reject-member" else "wrong"
    elif value is None:
        score_value = "held"
    elif case["truth_application"] == "reject-member":
        # A verified archive can reproduce the intended edition. It does not reproduce the
        # output of the observed substituted installation that this case asks about.
        score_value = "held"
    else:
        score_value = "correct" if value == old_truth else "wrong"
    if case["truth_application"] == "unknown":
        score_application = "unscored"
    elif application == "held":
        score_application = "held"
    else:
        score_application = "correct" if application == case["truth_application"] else "wrong"
    unbound = evidence.get("upstream_only") or evidence.get("value")
    shortcut = (
        "unscored" if old_truth is None or unbound is None else "matches" if unbound == old_truth else "wrong"
    )
    return {
        "old_output_status": output, "old_output_score": score_value, "application_status": application,
        "application_score": score_application, "old_truth_available": old_truth is not None,
        "application_truth_available": case["truth_application"] != "unknown",
        "value": value, "upstream_value": evidence.get("upstream_only"),
        "blind_value_if_equated_with_actual": shortcut,
    }


def run(work, archives):
    work = work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    archives = archives.resolve()
    fixtures = load_json(FIXTURES)
    upstream = load_json(HERE / "evidence" / "upstream-rules.json")
    http_prep = load_json(HERE / "evidence" / "acquisition.json")
    rows, operations, references, substitutions = [], [], [], []
    for case in collect_cases(fixtures):
        for view, entry in views_for(case, upstream).items():
            mark = work / case["id"] / view
            mark.mkdir(parents=True)
            view_bytes = compact(entry)
            record_path = mark / "record.json"
            record_path.write_bytes(view_bytes)
            references.append({"case_id": case["id"], "view": view, "record": entry,
                               "stored_bytes": len(view_bytes), "sha256": digest(view_bytes)})
            for mode in REPLAYS:
                http = HttpJournal(mark / mode / "cache")
                for profile in ("cold", "warm"):
                    start = time.monotonic()
                    stored = record_path.read_bytes()
                    record = json.loads(stored)
                    initial_events = len(http.events)
                    if mode == "recalculate":
                        outcome = recalculate(case, view, record, http, mark / mode / profile,
                                              fixtures, upstream, archives)
                    else:
                        outcome = {"metrics": {"dependency_source_reads": 0, "dependency_source_bytes": 0,
                                               "stage_archive_read_bytes": 0}}
                    decision = score(case, view, record, mode, outcome)
                    reads = http.events[initial_events:]
                    new_fetch = [item for item in reads if item["method"] == "GET"]
                    cache_fetch = [item for item in reads if item["method"] == "cache-read"]
                    redirects = [hop for item in new_fetch for hop in item["redirects"]]
                    row = {
                        "case_id": case["id"], "input_id": case["input"]["id"], "view": view,
                        "mode": mode, "profile": profile, "scope": case["scope"],
                        "additional_gets": len(new_fetch) + len(redirects),
                        "redirects": len(redirects),
                        "failed_requests": sum("error" in item for item in new_fetch),
                        "received_body_bytes": sum(item["bytes"] for item in new_fetch + redirects),
                        "cache_lookups": len(reads), "cache_reads": len(cache_fetch),
                        "cache_read_body_bytes": sum(item["bytes"] for item in cache_fetch),
                        "stored_bytes": len(view_bytes), "stored_sha256": digest(view_bytes),
                        "record_reads": 1, "record_read_bytes": len(stored),
                        "processing_ms": round((time.monotonic() - start) * 1000, 3),
                        **outcome["metrics"], **decision,
                    }
                    rows.append(row)
                    operations.append({"case_id": case["id"], "view": view, "mode": mode,
                                       "profile": profile, "http": reads, "replay": outcome.get("process"),
                                       "replay_loaded": outcome.get("loaded")})
        if case["id"].startswith("LABEL-"):
            donor = case["receipt"]["donor"]
            donor_pin = next(row for row in fixtures["predictions"] if row["id"] == donor)
            old = (archives / donor_pin["file"]).read_bytes()
            try:
                read_archive(archives / donor_pin["file"], case["pin"]["sha256"])
                rejected = False
            except ValueError:
                rejected = True
            substitutions.append({"case_id": case["id"], "declared": case["pin"]["file"],
                                  "expected_sha256": case["pin"]["sha256"], "actual": donor_pin["file"],
                                  "actual_sha256": digest(old), "wrong_archive_rejected": rejected,
                                  "local_file_bytes": len(old), "network_gets": 0})
    with (work / "costs.csv").open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: compact(v).decode() if isinstance(v, dict) else v for k, v in row.items()})
    json_lines(work / "cost-records.jsonl", references)
    dump(work / "cost-receipts.json", {
        "measured_at_utc": utc_now(), "fixture_sha256": digest(FIXTURES.read_bytes()),
        "script_sha256": digest(Path(__file__).read_bytes()),
        "preparation": {
            "registry_gets": len(http_prep["http"]),
            "registry_received_body_bytes": http_prep["bytes_received"],
            "registry_elapsed_ms_sum": sum(event["elapsed_ms"] for event in http_prep["http"]),
            "node_dependency_original_bytes": http_prep["moment"]["observed_bytes"],
            "fixed_fixture_bytes": FIXTURES.stat().st_size,
            "pricing_note": "The common pinned Node dependency is copied and read locally per recalculation. "
                            "Additional GETs exclude this one-time registry acquisition and consumer evidence preparation.",
        },
        "substituted_archive_checks": substitutions,
        "operations": operations,
    })
    print(f"{len(references)} stored records, {len(rows)} measured decisions")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    parser.add_argument("shared_archives", type=Path)
    args = parser.parse_args()
    run(args.work, args.shared_archives)
