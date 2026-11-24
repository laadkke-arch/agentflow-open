"""End-to-end request-path measurements with real public HTTP and locked offline npm."""
import argparse
import json
from collections import Counter
from pathlib import Path
from statistics import median
import time

from cases import cases_for, observation
from common import ROOT, Http, cpu_seconds, read_jsonl, sha, utc, write_csv, write_json, write_jsonl
from prepare import parser_install
from run import Installer, read_releases
from signals import (FUNCTIONS, after_edge, c_fingerprint, d_fingerprint, doc_path, e_fingerprint, notice,
                     release_assets)

POLICIES = ["A", "C", "D", "E", "E2"]


class RequestPath:
    def __init__(self, releases, locks, queries, parser_root, directory, policy):
        self.policy = policy
        self.releases_by_version = {r["version"]: r for r in releases}
        self.versions = list(self.releases_by_version)
        self.locks = locks
        self.queries = queries
        self.functions = FUNCTIONS[releases[0]["package"]]
        self.parser_root = parser_root
        self.directory = directory
        self.events = []
        self.http = Http()
        self.installer = Installer(directory, self.http, self.event)
        self.artifacts, self.docs, self.signals, self.decisions = {}, {}, {}, {}
        self.answers, self.measured = {}, {}

    def event(self, kind, detail):
        self.events.append({"kind": kind} | detail)

    def artifact(self, release):
        url = release["dist"]["tarball"]
        if url in self.artifacts:
            self.event("artifact_cache_hit", {"url": url})
            return self.artifacts[url]
        raw, rec = self.http.get(url)
        self.event("http", rec)
        if raw is None:
            return {}
        files, _, checks = release_assets(release, raw)
        self.event("archive_integrity", {"url": url, "body_bytes": len(raw), "checks": checks})
        self.artifacts[url] = files
        return files

    def documents(self, release):
        version, package = release["version"], release["package"]
        if version in self.docs:
            self.event("document_section_cache_hit", {"requested": version})
            return self.docs[version]
        docs = {}
        for name in self.functions:
            url = release["doc_urls"][name]
            if url == release["dist"]["tarball"]:
                doc = self.artifact(release).get(doc_path(package, name))
            else:
                doc, receive = self.http.get(url)
                self.event("http", receive)
            expected = release["doc_sha256"][name]
            if doc is not None and expected and sha(doc) != expected:
                self.event("document_identity_failure", {"url": url, "wanted_sha256": expected})
                doc = None
            docs[name] = doc
        if all(doc is not None for doc in docs.values()):
            self.docs[version] = docs
        return docs

    def fingerprint(self, version):
        if version in self.signals:
            self.event("fingerprint_cache_hit", {"requested": version, "policy": self.policy})
            return self.signals[version]
        release = self.releases_by_version[version]
        package = release["package"]
        p = self.policy
        result = {}
        if p in {"C", "D"}:
            docs = self.documents(release)
            result["C"] = {fn: c_fingerprint(package, fn, docs[fn]) for fn in self.functions}
            self.event("logical_hash", {"component": "C", "version": version,
                                        "bytes": sum(x["logical_bytes"] for x in result["C"].values())})
        if p == "D":
            files = self.artifact(release)
            result["D"] = {fn: d_fingerprint(release, files, fn, result["C"][fn]) for fn in self.functions}
            self.event("logical_hash", {"component": "D", "version": version,
                                        "bytes": sum(x["logical_bytes"] for x in result["D"].values())})
        if p in {"E", "E2"}:
            files = self.artifact(release)
            depth = 1 if p == "E" else 2
            es, parsed, err = e_fingerprint(release, files, self.parser_root, self.directory / "trees" / version, depth)
            read = es.get("reads", {})
            result.update(E=es.get("functions", {}), E_error=err, notice=notice(files, release))
            if parsed:
                self.event("node_static", {k: v for k,v in parsed.items() if k != "stdout"} |
                           {"stdout_sha256": sha(parsed["stdout"].encode()), "version": version, "reads": read})
            self.event("logical_hash", {"component": p, "version": version,
                                        "bytes": sum(x["bytes"] for x in read.values()) + result["notice"]["logical_bytes"]})
        self.signals[version] = result
        return result

    def decision(self, previous, version):
        key = previous, version
        if key in self.decisions:
            self.event("decision_cache_hit", {"previous": previous, "requested": version})
            return self.decisions[key]
        before, after = self.fingerprint(previous), self.fingerprint(version)
        decoded = {fn: after_edge(self.policy, before, after, fn) for fn in self.functions}
        self.event("edge_checked", {"previous": previous, "requested": version, "decisions": decoded})
        self.decisions[key] = decoded
        return decoded

    def key(self, release, item):
        return release["package"], release["version"], item["function"], item["input_sha256"], release["loader"]

    def query(self, version):
        release = self.releases_by_version[version]
        keys = [self.key(release, item) for item in self.queries]
        missing = [key for key in keys if key not in self.answers]
        self.event("answer_cache", {"requested": version, "hits": len(keys) - len(missing), "misses": len(missing)})
        if not missing:
            return [self.answers[key] for key in keys], "cache", ""
        self.documents(release)
        index = self.versions.index(version)
        earlier = [v for v in self.versions[:index] if v in self.measured]
        last = earlier[-1] if earlier else None
        if version in self.measured:
            action = "retry_missing_cells"
        elif not last or self.policy == "A":
            action = "exact-anchor" if not last else "exact-policy-A"
        else:
            edge_start = self.versions.index(last)
            verdicts = [self.decision(a,b) for a,b in zip(self.versions[edge_start:index], self.versions[edge_start + 1:index + 1])]
            conditions = [pair[0] for edge in verdicts for pair in edge.values()]
            action = "forced" if "forced" in conditions else "alert" if "alert" in conditions else "carry"
        if action == "carry":
            basis, data = last, self.measured[last]
        else:
            lock = self.locks[release["package"] + "/" + version]
            result = self.installer.install_and_run(release, lock, self.queries)
            basis, data = version, {case["id"]: case for case in result["cases"]} if result["status"] == "ok" else {}
            self.event("exact_result", {"requested": version, "status": result["status"],
                                        "lock_sha256": result["lock_sha256"], "entry_sha256": result.get("entry_sha256"),
                                        "snapshot_sha256": result.get("snapshot_sha256"),
                                        "timeouts": sum(case["result"]["type"] == "timeout" for case in result["cases"])})
            if data:
                self.measured[version] = data
        answers = []
        for key, item in zip(keys, self.queries):
            if key in self.answers:
                answers.append(self.answers[key])
                continue
            cell = data.get(item["id"])
            usable = cell is not None and cell["result"]["type"] != "timeout"
            answer = (basis if usable else None, cell if usable else None)
            if usable:
                self.answers[key] = answer
            answers.append(answer)
        return answers, action, basis


def score(release, queries, answers, truth):
    pending = {}
    states, source_counts = Counter(), Counter()
    observed = truth.get((release["package"], release["version"]), {})
    for item, (basis, cell) in zip(queries, answers):
        target = observed.get(item["id"])
        if cell is None:
            state = "held"
        elif target is None:
            state = "unknown"
        elif target["result"]["type"] == "timeout":
            state = "unknown"
        elif target["result"]["type"] == "load_error":
            state = "wrong_carry" if basis != release["version"] else "direct_disagreement"
        else:
            state = "correct" if observation(target) == observation(cell) else "wrong_carry" if basis != release["version"] else "direct_disagreement"
        states[state] += 1
        source_counts[basis or "-"] += 1
        pending.setdefault((basis or "-", state), []).append(item["id"])
    return (states, source_counts,
            [{"basis": basis, "state": state, "cells": cells} for (basis, state), cells in pending.items()])


def event_counts(events):
    http = [event for event in events if event["kind"] == "http"]
    misses = [event for event in http if event["cache"] == "miss"]
    hits = sum(event["cache"] == "local_url_hit" for event in http)
    return {"http_calls": len(misses), "actual_body_bytes": sum(e.get("bytes") or 0 for e in misses),
            "body_unmeasured": sum(e["bytes"] is None for e in misses),
            "http_non_200": sum(e["status"] != 200 for e in misses),
            "http_304": sum(e["status"] == 304 for e in misses), "url_cache_hits": hits,
            "logical_hash_bytes": sum(e["bytes"] for e in events if e["kind"] == "logical_hash"),
            "npm_cache_adds": sum(e["kind"] == "npm_cache_add" for e in events),
            "npm_content_hits": sum(e["kind"] == "npm_content_cache_hit" for e in events),
            "installs": sum(e["kind"] == "npm_ci" for e in events),
            "node_probes": sum(e["kind"] == "node_probe" for e in events),
            "node_static": sum(e["kind"] == "node_static" for e in events),
            "answers_hit": sum(e["hits"] for e in events if e["kind"] == "answer_cache")}


def run_phase(path, versions, descriptor, truth, events_out, answers_out):
    start, cpu = time.perf_counter(), cpu_seconds()
    output = []
    for index, version in enumerate(versions, 1):
        path.events = []
        wall0, cpu0 = time.perf_counter(), cpu_seconds()
        answers, action, basis = path.query(version)
        wall_ms, cpu_ms = (time.perf_counter() - wall0) * 1000, (cpu_seconds() - cpu0) * 1000
        output.append((index, version, answers, action, basis, path.events, wall_ms, cpu_ms))
    phase_time = {"phase_wall_ms": round((time.perf_counter() - start) * 1000, 3),
                  "phase_cpu_ms": round((cpu_seconds() - cpu) * 1000, 3)}
    rows, merged = [], []
    for index, version, answers, action, basis, events, wall, user_cpu in output:
        release = path.releases_by_version[version]
        count, source, groups = score(release, path.queries, answers, truth)
        event_id = "-".join(str(descriptor[k]) for k in ("package","sequence","policy","rep","cache")) + f"-{index}"
        events_out.append({"event_id": event_id, "requested": version, "events": events})
        answers_out.append({"event_id": event_id, "requested": version, "loader": release["loader"], "outcomes": groups})
        merged.extend(events)
        rows.append(descriptor | {"event_id": event_id, "query": index, "requested": version,
                                  "attempted_or_carried_basis": basis, "measured_basis_counts": dict(source),
                                  "action": action, "responses": len(path.queries),
                                  **{k: count[k] for k in ("correct","wrong_carry","held","unknown","direct_disagreement")},
                                  **event_counts(events), "wall_ms": round(wall,3), "cpu_ms": round(user_cpu,3)})
    phase = descriptor | phase_time | event_counts(merged) | {
        key: sum(row[key] for row in rows) for key in ("responses", "correct","wrong_carry","held","unknown","direct_disagreement")
    }
    phase.update(queries=len(rows), first=versions[0], last=versions[-1],
                 last_measured_basis_counts=rows[-1]["measured_basis_counts"])
    return rows, phase


def summarize(phases):
    groups = {}
    for row in phases:
        key = tuple(row[k] for k in ("package", "sequence", "policy", "cache"))
        groups.setdefault(key, []).append(row)
    result = []
    for key, reps in groups.items():
        row = dict(zip(("package", "sequence", "policy", "cache"), key)) | {"repeats": len(reps), "queries_per_rep": reps[0]["queries"]}
        for k in ("actual_body_bytes", "logical_hash_bytes", "installs", "node_probes", "node_static",
                  "phase_wall_ms", "phase_cpu_ms"):
            values = [r[k] for r in reps]
            row |= {k + "_median": median(values), k + "_min": min(values), k + "_max": max(values)}
        for k in ("responses", "correct", "wrong_carry", "held", "unknown", "direct_disagreement",
                  "http_non_200", "body_unmeasured", "answers_hit"):
            row[k + "_sum"] = sum(r[k] for r in reps)
        result.append(row)
    return result


def truth_table():
    raw = read_jsonl(ROOT / "runs.jsonl")
    first = {(r["package"], r["version"]): r for r in raw if r["label"] == "A"}
    second = {(r["package"], r["version"]): r for r in raw if r["label"] == "B"}
    truth = {}
    for key, run in first.items():
        check = second[key]
        if run["status"] != "ok" or check["status"] != "ok":
            if run["status"] == check["status"] == "load_error" and run["error"]["code"] == check["error"]["code"]:
                truth[key] = {c["id"]: {"result": {"type": "load_error"}} for c in cases_for(key[0])}
            continue
        b = {c["id"]: c for c in check["cases"]}
        truth[key] = {a["id"]: a for a in run["cases"] if a["id"] in b and observation(a) == observation(b[a["id"]])}
    return truth


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--scratch", type=Path, required=True)
    args.add_argument("--out", type=Path, required=True)
    args.add_argument("--repeat", type=int, default=3)
    opt = args.parse_args()
    opt.scratch.mkdir(parents=True, exist_ok=False)
    opt.out.mkdir(parents=True, exist_ok=True)
    parser_root = opt.scratch / "parser"
    parser_receipt = parser_install(parser_root, opt.scratch / "parser-npm")
    releases, locks = read_releases()
    truth = truth_table()
    all_rows, phases, events, answers = [], [], [], []
    for rep in range(1, opt.repeat + 1):
        shift = (rep - 1) * 2 % len(POLICIES)
        order = POLICIES[shift:] + POLICIES[:shift]
        for package in FUNCTIONS:
            members = [r for r in releases if r["package"] == package]
            versions = [r["version"] for r in members]
            queries = list(cases_for(package))
            for scenario, sequence in (("dense", versions), ("ends", [versions[0], versions[-1]] * 3)):
                for slot, policy in enumerate(order, 1):
                    directory = opt.scratch / f"{package}-{scenario}-{rep}-{policy}"
                    path = RequestPath(members, locks, queries, parser_root, directory, policy)
                    for cache in ("cold", "retained"):
                        desc = dict(package=package, sequence=scenario, policy=policy, rep=rep, order_slot=slot, cache=cache)
                        rows, phase = run_phase(path, sequence, desc, truth, events, answers)
                        all_rows.extend(rows)
                        phases.append(phase)
                    write_json(directory / "completed-phases.json", phases[-2:])
                    print(package, scenario, rep, policy, phases[-2]["phase_wall_ms"], phases[-1]["phase_wall_ms"], flush=True)
    for row in all_rows:
        row["measured_basis_counts"] = json.dumps(row["measured_basis_counts"], sort_keys=True, separators=(",", ":"))
    write_csv(opt.out / "costs.csv", all_rows)
    write_csv(opt.out / "cost-summary.csv", summarize(phases))
    write_jsonl(opt.out / "cost-phases.jsonl", phases)
    write_jsonl(opt.out / "cost-events.jsonl", events)
    write_jsonl(opt.out / "cost-answers.jsonl", answers)
    write_json(opt.out / "cost-setup.json", {"comparison": "cold then immediate identical retained",
                                          "completed_utc": utc(), "communicated_units": "HTTP response body and Linux elapsed/CPU",
                                          "parser_install_common_setup": parser_receipt})


if __name__ == "__main__":
    main()
