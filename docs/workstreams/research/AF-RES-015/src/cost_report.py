"""Summarize network and reading observations without equating tool calls and HTTP."""

import csv
import json
from datetime import datetime
from statistics import mean, median

from collect import ROOT, rows


def main():
    network = rows(ROOT / "results/cost-network.jsonl")
    review = rows(ROOT / "results/cost-review.jsonl")
    ledger = {x["reason_id"]: x for x in rows(ROOT / "REASONS.jsonl")}
    reads = {(x["mode"], x["reason_id"]): x for x in review if x["mode"] != "pilot"}
    checks = {(x["mode"], x["reason_id"]): x for x in network}
    measured = []
    summary = {}
    for mode in "ABC":
        bundle = []
        for key, truth in ledger.items():
            if ("A", key) not in reads:
                continue
            io = checks.get((mode.lower(), key), {})
            judgement = reads.get((mode, key), {})
            observed = {"reason_id": key, "mode": mode,
                        "known_http_requests": io.get("requests", 0),
                        "web_page_operations": judgement.get("web_operations", 0),
                        "unexposed_internal_http": bool(judgement),
                        "body_pages_read": judgement.get("viewable_surfaces", 0),
                        "metadata_pages_parsed": io.get("metadata_pages", 0),
                        "auto_seconds": io.get("seconds", 0),
                        "web_then_seconds": judgement.get("retrieval_seconds", 0),
                        "alert": io.get("alert"), "now_verdict": truth["now_verdict"],
                        "then_verdict": truth["then_verdict"]}
            observed["active_seconds"] = observed["auto_seconds"] + observed["web_then_seconds"]
            bundle.append(observed)
        page = [x for x in review if x["mode"] == mode]
        calls = [x for x in network if x["mode"] == mode.lower()]
        review_elapsed = None
        collection_elapsed = None
        if page:
            lo = min(datetime.fromisoformat(x["opened_at_utc"]) for x in page)
            hi = max(datetime.fromisoformat(x["returned_at_utc"]) for x in page)
            review_elapsed = (hi - lo).total_seconds()
        if calls:
            lo = min(datetime.fromisoformat(x["started_at_utc"]) for x in calls)
            hi = max(datetime.fromisoformat(x["finished_at_utc"]) for x in calls)
            collection_elapsed = (hi - lo).total_seconds()
        measured.extend(bundle)
        summary[mode] = {"n": len(bundle), "manual_reviews": len(page),
                         "review_retrieval_window_seconds": review_elapsed,
                         "network_collection_window_seconds": collection_elapsed,
                         "known_http_requests": sum(x["known_http_requests"] for x in bundle),
                         "web_page_operations": sum(x["web_page_operations"] for x in bundle),
                         "metadata_pages_parsed": sum(x["metadata_pages_parsed"] for x in bundle),
                         "body_pages_read": sum(x["body_pages_read"] for x in bundle),
                         "active_seconds_mean": mean(x["active_seconds"] for x in bundle),
                         "active_seconds_median": median(x["active_seconds"] for x in bundle),
                         "flagged_now_broken": [x["reason_id"] for x in bundle
                                                if x["alert"] is True and x["now_verdict"] == "무너짐"],
                         "unflagged_now_broken": [x["reason_id"] for x in bundle
                                                  if mode != "A" and x["alert"] is not True
                                                  and x["now_verdict"] == "무너짐"]}
    with (ROOT / "results" / "cost.csv").open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(measured[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(measured)
    (ROOT / "results" / "cost.json").write_text(json.dumps({
        "fixture": "data/cost-bench.txt",
        "counting": "HTTP from runner plus separate web operations; internal web HTTP is unknown",
        "manual_reviewer": "single Codex research worker; zero human participants",
        "one_item_wall": "network and browser retrieval; reviewer-only time not isolated",
        "summary": summary,
    }, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
