"""Join measured route counters and recorded construction costs without qrels."""
import argparse
import csv
from datetime import datetime
import json
from pathlib import Path

from search import ARMS, MODES, read_jsonl, write_csv


def make_costs(root, route_costs):
    cases = {r["id"]: r["stratum"] for r in read_jsonl(root / "requests.jsonl")}
    receipts = read_jsonl(root / "evidence/build-fetches.jsonl")
    seal = json.loads((root / "evidence/card-seal.json").read_text())
    input_root = root / "experiment/inputs"
    stored = {arm: (input_root / (arm + ".jsonl")).stat().st_size for arm in ARMS}
    common = (input_root / "documents.jsonl").stat().st_size
    data = list(csv.DictReader(route_costs.open()))
    columns = list(data[0].keys())[3:]
    build_bytes = sum(row["bytes"] for row in receipts)
    build_fetch_ms = sum(row["wall_ms"] for row in receipts)
    build_wall_ms = round(1000 * (
        datetime.fromisoformat(seal["sealed_utc"]) -
        datetime.fromisoformat(seal["receipt_span_started_utc"])
    ).total_seconds())

    def row(phase, arm, stratum, mode, request_id="", n=0):
        return {
            "phase": phase, "arm": arm, "stratum": stratum, "cache": mode,
            "request_id": request_id, "unique_requests": n,
            "build_calls": "" if phase == "request" else 0 if arm == "L" else len(receipts),
            "build_http_b": "" if phase == "request" else 0 if arm == "L" else build_bytes,
            "build_sum_fetch_ms": "" if phase != "build" else 0 if arm == "L" else build_fetch_ms,
            "build_wall_span_ms": "" if phase != "build" or arm == "L" else build_wall_ms,
            "representation_file_b": stored[arm], "common_harness_file_b": common,
            "max_raw_cache_b": "", **dict.fromkeys(columns, ""),
        }

    output = [row("build", arm, "all", "n/a") for arm in ARMS]
    raw_resident = {(r["request_id"], r["arm"]): int(r["new_cache_b"]) for r in data if r["cache"] == "cold"}
    for route in data:
        rid, arm, mode = (route[key] for key in ("request_id", "arm", "cache"))
        result = row("request", arm, cases[rid], mode, rid, 1)
        result.update({key: int(route[key]) for key in columns})
        result["max_raw_cache_b"] = raw_resident[(rid, arm)]
        output.append(result)

    request_rows = output[len(ARMS):]
    for stratum in ("natural", "calibration"):
        for arm in ARMS:
            for mode in MODES:
                group = [r for r in request_rows if (r["stratum"], r["arm"], r["cache"]) == (stratum, arm, mode)]
                result = row("summary_sum", arm, stratum, mode, n=len(group))
                result.update({key: sum(r[key] for r in group) for key in columns})
                result["max_raw_cache_b"] = max(r["max_raw_cache_b"] for r in group)
                output.append(result)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("route_costs", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    write_csv(args.output, make_costs(args.root, args.route_costs))
