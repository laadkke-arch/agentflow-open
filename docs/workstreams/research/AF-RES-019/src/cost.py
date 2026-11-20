"""Benchmark public retrieval and compute explicitly conditioned scale estimates."""
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime
from html.parser import HTMLParser
import io
from pathlib import Path
from statistics import mean, median
import subprocess
from threading import Lock
import time
from urllib.parse import urlsplit

from analyze import write_csv
from collect import STUDY, load_json, prepare_repo, save_json, utc_now

HOST_GUARD = Lock()
PAGE_HOST_STATUS = {}
PAGE_GAPS = {}
MAX_HEAD_BYTES = 1_500_000
TERMS = ("license", "end of life", "deprecated", "release", "retire", "support",
         "archive", "service", "removed", "version", "readme", "plans")


class PageScan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.muted = None
        self.tokens = set()

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.muted = tag

    def handle_endtag(self, tag):
        if tag == self.muted:
            self.muted = None

    def handle_data(self, data):
        if self.muted is None and data.strip():
            text = data.lower()
            self.tokens.update(term for term in TERMS if term in text)


def evidence_url(row, sources):
    if row.get("source_ids"):
        items = [sources[i] for i in row["source_ids"]]
        hosted = [s for s in items if urlsplit(s["url"]).hostname in
                  ("github.com", "raw.githubusercontent.com") and s["level"] == "D3-fetch"]
        return (hosted or items)[0]["url"]
    return row["no_event_check"]["source"]


def http_page(task):
    item_id, url = task
    host = urlsplit(url).hostname
    if urlsplit(url).scheme != "https" or host is None:
        raise ValueError("Only explicitly selected public HTTPS sources are supported.")
    start, stamp = time.monotonic(), utc_now()
    row = {"id": item_id, "mode": "source_page", "url": url, "at_utc": stamp}
    with HOST_GUARD:
        if host in PAGE_HOST_STATUS:
            return row | {"status": "host_previously_blocked", "blocked_reply": PAGE_HOST_STATUS[host]}
        if host in ("registry.npmjs.org", "pypi.org", "rubygems.org", "crates.io"):
            wait = 1.10 - (time.monotonic() - PAGE_GAPS.get(host, 0))
            if wait > 0:
                time.sleep(wait)
            PAGE_GAPS[host] = time.monotonic()
    command = ["curl", "--disable", "--silent", "--show-error", "--compressed", "--max-time", "20",
               "--max-filesize", str(MAX_HEAD_BYTES), "--user-agent", "AF-RES-019 public research/1.0",
               "--write-out", "\nAF019META %{http_code} %{http_connect} %{size_download}", url]
    res = subprocess.run(command, capture_output=True)
    elapsed = time.monotonic() - start
    body, _, meta = res.stdout.rpartition(b"\nAF019META ")
    if not meta:
        meta = b"0 0 0"
    http, connect, b = map(int, meta.split())
    status = "fetched" if http == 200 and res.returncode == 0 else "http_or_transport_failure"
    if http in (403, 429) or connect == 403:
        with HOST_GUARD:
            PAGE_HOST_STATUS[host] = connect if connect == 403 else http
    seconds_to_read, hits, pages = None, [], 0
    if status == "fetched":
        begin = time.monotonic()
        scan = PageScan()
        scan.feed(body.decode("utf-8", errors="replace"))
        hits = sorted(scan.tokens)
        seconds_to_read = round(time.monotonic() - begin, 6)
        pages = 1
    return row | {"status": status, "http_code": http or None, "connect": connect or None,
                  "requests": 1, "bytes": b, "seconds": round(elapsed, 5), "tool_read_seconds": seconds_to_read,
                  "pages_scanned": pages, "scope_tokens_found": hits, "exit_code": res.returncode}


def load_items():
    events = load_json(STUDY / "events/EVENTS.json")
    controls = load_json(STUDY / "controls/CONTROLS.json")
    sources = {s["id"]: s for s in load_json(STUDY / "sources.json")["sources"]}
    return events, controls, sources


def bench(scratch, jobs):
    events, controls, sources = load_items()
    items = events + controls
    access = load_json(STUDY / "VERIFICATION.json")["access"]
    for row in access:
        if 403 in row["http_replies"]:
            PAGE_HOST_STATUS[row["host"]] = 403
    paths = [(row["id"], evidence_url(row, sources)) for row in items]
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        direct = list(pool.map(http_page, paths))
    save_json(scratch / "page-cost.json", direct)
    limit = {}
    full_targets = []
    event_kinds = {r["id"]:r["type"] for r in events}
    for row in items:
        url = row.get("repo_url")
        if url is None:
            continue
        is_control = "matched_event" in row
        group = (event_kinds[row.get("matched_event", row["id"])], is_control)
        _, partial = prepare_repo(url, scratch / "repos")
        if partial["exit_code"] or partial["bytes"] > 10 * 1024 ** 2 or limit.get(group, 0) >= 2:
            continue
        limit[group] = limit.get(group, 0) + 1
        full_targets.append((row["id"], url, partial["bytes"]))
    def run_full(task):
        item_id, url, partial_bytes = task
        _, result = prepare_repo(url, scratch / "repos", full=True)
        return {"id": item_id, "paired_partial_bytes": partial_bytes, **result}
    with ThreadPoolExecutor(max_workers=min(4, jobs)) as pool:
        full = list(pool.map(run_full, full_targets))
    save_json(scratch / "full-cost.json", full)
    print("source pages", sum(r.get("pages_scanned", 0) for r in direct), "/", len(direct))
    print("full clones", sum(r["exit_code"] == 0 for r in full), "/", len(full))


def metric_row(id_, mode, result):
    if result is None:
        return {"id": id_, "mode": mode, "status": "not_applicable", "requests": None, "bytes": None,
                "seconds": None, "tool_read_seconds": None, "pages_scanned": None, "at_utc": None,
                "url": None, "http_code": None}
    code = result.get("http_code")
    if code is None and result.get("http_replies"):
        code = result["http_replies"][-1]
    status = result.get("status")
    if status is None:
        status = "measured" if result.get("exit_code", 1) == 0 else result.get("unknown", "failed")
    return {"id": id_, "mode": mode, "status": status, "requests": result.get("requests"),
            "bytes": result.get("bytes"), "seconds": result.get("seconds"), "tool_read_seconds": result.get("tool_read_seconds"),
            "pages_scanned": result.get("pages_scanned"), "at_utc": result.get("at_utc"),
            "url": result.get("url"), "http_code": code}


def summarize(rows, mode):
    applicable = [r for r in rows if r["mode"] == mode]
    data = [r for r in applicable if r["status"] in ("measured", "fetched")]
    counts = {k: sum(1 for row in data if row[k] is not None)
              for k in ("requests", "bytes", "seconds", "tool_read_seconds", "pages_scanned")}
    means, medians = {}, {}
    for key in counts:
        values = [r[key] for r in data if r[key] is not None]
        means[key] = mean(values) if values else None
        medians[key] = median(values) if values else None
    return {"attempted_or_applicable_rows": len(applicable), "successful_rows": len(data),
            "metric_n": counts, "mean": means, "median": medians}


def estimates(cost_rows, cadence):
    keys = ("requests", "seconds", "bytes")
    def operation_means(row):
        return {k: row["mean"][k] or 0 for k in keys}
    direct = operation_means(cost_rows["source_page"])
    git = operation_means(cost_rows["git_cold_signal"])
    reg = operation_means(cost_rows["registry"])
    item_reg_share = cost_rows["registry"]["successful_rows"] / cost_rows["git_cold_signal"]["successful_rows"]
    signal = {k: git[k] + reg[k] * item_reg_share for k in keys}
    per_year = {"monthly": 12, "quarterly": 4, "yearly": 1,
                "on_request_14d": 365 / 14, "on_request_90d": 365 / 90, "on_request_365d": 1}
    result = []
    for row in cadence:
        method = row["method"]
        fraction = int(row["signal_positive_checks"]) / int(row["hypothetical_checks"])
        if method == "source":
            unit = direct
        elif method == "signal":
            unit = signal
        else:
            unit = {k: signal[k] + fraction * direct[k] for k in keys}
        annual_checks = per_year[row["cadence"]]
        result.append({"method": method, "cadence": row["cadence"], "annual_checks_per_item": annual_checks,
                       "simulated_positive_fraction": fraction, "unit_cold_check": unit,
                       "annual_1k": {k: v * annual_checks * 1_000 for k, v in unit.items()},
                       "annual_10k": {k: v * annual_checks * 10_000 for k, v in unit.items()}})
    return result


def summarize_bench(scratch, output):
    page = load_json(scratch / "page-cost.json")
    full = load_json(scratch / "full-cost.json")
    signals = load_json(output / "collection-receipts.json")
    rows = [metric_row(r["id"], "source_page", r) for r in page]
    rows.extend(metric_row(r["id"], "git_full_clone", r) for r in full)
    for row in signals:
        id_ = row["id"]
        clone = row["clone"]
        registry = row["registry"] if row["registry"] and row["registry"].get("url") else None
        rows.append(metric_row(id_, "git_partial_clone", clone))
        rows.append(metric_row(id_, "registry", registry))
        if clone and clone["exit_code"] == 0:
            overhead = row["git_overhead"] or {}
            measured = {"exit_code": 0, "requests": clone["requests"] + overhead.get("requests", 0),
                        "bytes": clone["bytes"] + overhead.get("bytes", 0),
                        "seconds": clone["seconds"] + overhead.get("wall_seconds", 0),
                        "at_utc": clone["at_utc"], "url": clone["url"]}
            rows.append(metric_row(id_, "git_cold_signal", measured))
    write_csv(output / "cost.csv", rows)
    with (output / "cadence.csv").open(newline="", encoding="utf-8") as stream:
        cadence = list(csv.DictReader(stream))
    summary = {mode: summarize(rows, mode) for mode in sorted({r["mode"] for r in rows})}
    save_json(output / "cost-model.json",
              {"metric_summary": summary, "annual_check_extrapolation": estimates(summary, cadence),
               "assumptions": ["application scales without caching; seconds are summed per-item tool wall time",
                               "git pack bytes and HTTPS response-body bytes exclude TLS and headers",
                               "direct costs extrapolate success-only chosen known URLs; agent semantic time absent",
                               "confirmation gate uses case-only simulated A_OR trigger fraction; operational base rate unknown",
                               "per-check registry share uses measured registry successes per Git cold-signal observation",
                               "registry pacing and concurrent network contention measured separately from budgeted per-item time"]})
    save_json(output / "cost-receipts.json", {"pages": page, "full_clones": full})
    return summary


def main():
    parser = ArgumentParser()
    parser.add_argument("--scratch", required=True, type=Path)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--bench", action="store_true")
    parser.add_argument("--summarize", action="store_true")
    parser.add_argument("--results", type=Path, default=STUDY / "results")
    args = parser.parse_args()
    if args.bench:
        bench(args.scratch, args.jobs)
    if args.summarize:
        result = summarize_bench(args.scratch, args.results)
        print({k: v["successful_rows"] for k, v in result.items()})


if __name__ == "__main__":
    main()
