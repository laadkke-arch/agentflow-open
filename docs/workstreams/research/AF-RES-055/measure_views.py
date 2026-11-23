"""Measure the 24 AF-RES-055 views on separate cold and pre-acquired caches."""
import argparse
import csv
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from time import perf_counter_ns

from replay import (
    ARCHIVES, PAIRS, ROOT, compact, compile_archive, json_out, jsonl_out, ms, now,
    read_instants, read_jsonl, scoped_tzif, sha, tz_requirement_value,
)


class Access:
    def __init__(self, directory, shared_cache):
        self.directory = directory
        self.directory.mkdir(parents=True)
        self.shared_cache = shared_cache
        self.network = {}
        self.cache_keys = set()
        self.local_reads = []
        self.built = {}
        self.commands = []
        self.compute_ms = 0.0

    def get(self, url):
        if url in self.network:
            result = self.network[url]
            return Path(result["response_path"]) if result["usable_http"] else None
        path = self.directory / (sha(url.encode()) + ".body")
        command = ["curl", "--location", "--silent", "--show-error", "--max-time", "20",
                   "--write-out", "%{json}", "--output", str(path), url]
        started = now()
        result = subprocess.run(command, capture_output=True, timeout=25, check=False)
        stats = json.loads(result.stdout)
        usable = result.returncode == 0 and 200 <= stats["http_code"] < 300
        self.network[url] = {
            "command":command, "request_utc":started, "url":url, "final_url":stats["url_effective"],
            "status":stats["http_code"],"connect_status":stats["http_connect"], "usable_http":usable,
            "body_bytes":int(stats["size_download"]), "redirects":stats["num_redirects"],
            "wall_ms":round(stats["time_total"]*1000, 3), "exit_code":result.returncode,
            "stdout_sha256":sha(result.stdout),"stderr_sha256":sha(result.stderr),
            "error":result.stderr.decode(errors="replace").strip(),
            "response_path":str(path) if path.exists() else None,
            "body_sha256":sha(path.read_bytes()) if path.exists() else None,
        }
        return path if usable else None

    def local_read(self, identity, path):
        if identity not in self.cache_keys:
            self.cache_keys.add(identity)
            self.local_reads.append({"identity":identity, "path":str(path), "bytes":path.stat().st_size})

    def index(self, spec):
        if self.shared_cache:
            path = ROOT / "editions.csv"
            self.local_read(spec["entry"], path)
            with path.open(newline="") as file:
                versions = [x["label"] for x in csv.DictReader(file) if x["record"] == "frame" and x["provider"] == "IANA"]
        else:
            data = self.get(spec["entry"])
            if data is None:
                return False
            versions = re.findall(r'href="(?:[^"]*/)?tzdata(20\d{2}[a-z]+)\.tar\.gz"', data.read_text(), re.I)
        if not spec["editions"]:
            return False
        old, new = spec["editions"]
        return any((left, right) == (old, new) for left, right in zip(versions, versions[1:]))

    def version(self, spec, tag):
        if tag in self.built:
            return self.built[tag]
        if self.shared_cache:
            cache = self.shared_cache
            self.local_read(ARCHIVES[tag]["official_url"], cache / f"tzdata{tag}.tar.gz")
        else:
            original = ARCHIVES[tag]["official_url"]
            mirror = ARCHIVES[tag]["mirror_url"]
            body = self.get(original)
            if body is None and mirror:
                body = self.get(mirror)
            if body is None:
                return None
            cache = self.directory / "assets"
            cache.mkdir(exist_ok=True)
            shutil.copyfile(body, cache / f"tzdata{tag}.tar.gz")
        started = perf_counter_ns()
        compiled = compile_archive(cache, tag, self.directory / "build" / tag, self.commands)
        self.built[tag] = read_instants(compiled, spec["zone"], spec["instants"],
                                        self.directory / "reads" / tag, self.commands)
        self.compute_ms += ms(started)
        return self.built[tag]

    def past_receipt(self, receipt):
        started = perf_counter_ns()
        compiled = scoped_tzif(receipt, self.directory / "scoped-old", self.commands)
        values = read_instants(compiled, receipt["key"], receipt["utc"], self.directory / "scoped-reads", self.commands)
        self.compute_ms += ms(started)
        return values

    def totals(self):
        return {
            "gets":len(self.network), "failures":sum(not r["usable_http"] for r in self.network.values()),
            "redirects":sum(r["redirects"] for r in self.network.values()),
            "body_bytes":sum(r["body_bytes"] for r in self.network.values()),
            "cache_lookups":len(self.local_reads), "cache_local_bytes":sum(r["bytes"] for r in self.local_reads),
            "get_ms":round(sum(r["wall_ms"] for r in self.network.values()),3),
            "compute_ms":round(self.compute_ms,3),
        }


def record_for(requirement, level, spec, past):
    record = {
        "entry":spec["entry"],
        "reason":f'이 발행자의 자료로 같은 기준에서 {requirement["question"]}을 검증한다.',
    }
    if level in ("V1", "V2"):
        if spec["editions"]:
            old_tag = spec["editions"][0]
            ref = ARCHIVES[old_tag]
            record["historical"] = {
                "edition":old_tag,"archive":ref["official_url"],"archive_sha256":ref["sha256"],
                "members":{name:ref["members"][name]["sha256"] for name in ("version", spec["member"])},
            }
        else:
            record["historical"] = None
    if level == "V2":
        record["past_receipt"] = dict(past, unit=requirement["unit"]) if past else None
    return record


def judge(requirement, record, spec, access, old_truth, next_truth):
    start = perf_counter_ns()
    past = None
    index_ready = False
    details = []
    if spec["editions"]:
        past_tag, next_tag = spec["editions"]
        if record.get("past_receipt"):
            past = access.past_receipt(record["past_receipt"])
            details.append("old selected rows recompiled; explicit TZif matched past digest")
        elif record.get("historical"):
            past = access.version(spec, past_tag)
            details.append("named past archive lookup")
        else:
            index_ready = access.index(spec)
            if index_ready:
                past = access.version(spec, past_tag)
            details.append("past archive located through entry index if available")
    else:
        details.append("eligible pair, service day, and key unavailable")

    current_past = tz_requirement_value(past, requirement["metric"]) if past else None
    before_next = access.totals()
    index_ready = index_ready or access.index(spec)
    if index_ready:
        new = access.version(spec, next_tag)
    else:
        new = None
    current_next = tz_requirement_value(new, requirement["metric"]) if new else None
    next_relation = "hold"
    if current_past is not None and current_next is not None:
        next_relation = "keep" if current_past == current_next else "replace"
    if old_truth is None or next_truth is None:
        past_score, next_score = "unscored", "unscored"
        truth_denom = 0
        shortcut_next = "unscored"
    else:
        past_score = "hold" if current_past is None else "match" if current_past == old_truth else "error"
        truth_relation = "keep" if old_truth == next_truth else "replace"
        next_score = "hold" if next_relation == "hold" else "match" if next_relation == truth_relation else "error"
        truth_denom = 1
        shortcut_next = "match" if truth_relation == "keep" else "error"
    after_next = access.totals()
    return {
        "past_value":current_past, "next_value_separately_read":current_next,
        "past_judgment":"restored" if current_past is not None else "hold", "next_judgment":next_relation,
        "past_score":past_score,"next_score":next_score,"truth_denominator_each":truth_denom,
        "direct_link_shortcut":{"past":"asserts restoration without a value" if truth_denom else "unscored",
                                "next":shortcut_next},
        "index_available":index_ready,
        "past_cost":before_next, "next_extra_cost":{k:round(after_next[k]-before_next[k],3) for k in after_next},
        "total_cost":after_next,"total_wall_ms":ms(start),"details":details,
        "get_receipts":list(access.network.values()),"cache_receipts":access.local_reads,
        "commands":access.commands,
    }


def run(base, cache, directory, destination):
    readings = {row["run_id"]:row.get("value") for row in read_jsonl(base / "runs.jsonl")}
    past_inputs = json.loads((base / "past-inputs.json").read_text())
    with (ROOT / "expectations.csv").open(newline="") as f:
        requirements = list(csv.DictReader(f))
    rows, stored, traces = [], [], []
    for requirement in requirements:
        rid = requirement["requirement"]
        pair = requirement["pair"]
        spec = PAIRS[pair]
        past_truth, next_truth = readings[rid + "-old"], readings[rid + "-next"]
        for level in ("V0", "V1", "V2"):
            view_id = rid + "-" + level
            record = record_for(requirement, level, spec, past_inputs.get(pair))
            canonical = compact(record).encode()
            expected = {"view_id":view_id,"requirement":rid,"level":level,"storage_bytes":len(canonical),
                        "storage_sha256":sha(canonical)}
            stored.append(expected | {"record":record})
            profiles = {}
            for mode, available in (("cold", None), ("warm", cache)):
                access = Access(directory / view_id / mode, available)
                measured = judge(requirement, record, spec, access, past_truth, next_truth)
                profiles[mode] = measured
                traces.append({"view_id":view_id, "cache":mode, **measured})
            row = dict(expected)
            row.update({
                "past_planned":1,"next_planned":1,
                "past_truth_denominator":profiles["cold"]["truth_denominator_each"],
                "next_truth_denominator":profiles["cold"]["truth_denominator_each"],
                "past_shortcut":"unsupported" if profiles["cold"]["truth_denominator_each"] else "unscored",
                "next_shortcut":profiles["cold"]["direct_link_shortcut"]["next"],
                "evidence_address":spec["entry"],
                "unverified":spec.get("missing","cold reachability follows this shell policy; publishing/installation per consumer untested"),
            })
            for mode, profile in profiles.items():
                for field in ("past_judgment","next_judgment","past_score","next_score"):
                    row[f"{mode}_{field}"] = profile[field]
                for field, value in profile["total_cost"].items():
                    row[f"{mode}_{field}"] = value
                row[f"{mode}_past_value"] = compact(profile["past_value"])
                row[f"{mode}_next_value"] = compact(profile["next_value_separately_read"])
            rows.append(row)
    (destination / "evidence").mkdir(parents=True, exist_ok=True)
    with (destination / "views.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    jsonl_out(destination / "evidence" / "view-records.jsonl", stored)
    json_out(destination / "evidence" / "view-execution.json", {
        "argv":[sys.executable, "-B", *sys.argv],
        "measured_results":traces, "storage_serialization":"compact sorted-key UTF-8 JSON, no framing newline",
        "cache_protocol":"independent scratch for each view and profile; pinned common files for warm",
        "provisioning_not_charged":"web origin discovery and byte-equivalent archive preparation in acquisitions and preparation receipts",
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("base", "cache", "scratch", "output"):
        parser.add_argument("--" + option, required=True, type=Path)
    arg = parser.parse_args()
    run(arg.base.resolve(), arg.cache.resolve(), arg.scratch.resolve(), arg.output.resolve())
