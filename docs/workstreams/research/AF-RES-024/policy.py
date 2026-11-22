"""Replay publication-time observations. This module never loads the answer key."""

import argparse
import csv
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

from acquire import HERE, read_csv, read_jsonl, write_jsonl
from cohort import order


@dataclass(frozen=True)
class Config:
    policy: str
    budget: int = 20
    threshold: int = 2
    cache: str = "cold"
    failure: str = "charged"
    shared: str = "once"
    ecosystem: str = "both"

    @property
    def label(self):
        return f"{self.policy}-{self.budget}-t{self.threshold}-{self.cache}-{self.failure}-{self.shared}-{self.ecosystem}"


@dataclass
class Remembered:
    last_blob: str
    warned: bool
    last_visit: int = -1
    invalid: bool = False
    signal_active: bool = False


class Inputs:
    def __init__(self, folder):
        self.folder = folder
        self.cohort = {r["id"]: r for r in read_csv(folder / "cohort.csv") if r["selected"] == "1"}
        self.releases = {(r["quarter"], r["ecosystem"]): r for r in read_csv(folder / "releases.csv")}
        self.quarters = sorted({q for q, _ in self.releases if q != "T0"})
        self.views = {q: read_jsonl(folder / "snapshots" / f"{q}.jsonl") for q in self.quarters}
        self.findings = defaultdict(list)
        used = {(q, doc["ecosystem"], doc["kind"], doc["path"]): doc
                for q, view in self.views.items() for doc in view}
        for row in read_csv(folder / "observed-findings.csv"):
            key = (row["quarter"], row["ecosystem"], row["kind"], row["path"])
            doc = used[key]
            assert doc["status"] == "ok" and row["id"] in self.cohort
            assert row["url"].split("#")[0] == doc["url"], row
            assert (row["commit"] == self.releases[key[:2]]["commit"] and
                    row["status"] in {"invalid", "warning", "supported", "uncertain", "restored"})
            self.findings[key].append(row)
        self.receipts = {}
        for cache in ("cold", "reuse1", "reuse2"):
            for q in self.quarters:
                for row in read_jsonl(folder / "evidence" / "receipts" / cache / f"{q}.jsonl"):
                    self.receipts[cache, q, row["ecosystem"], row["kind"], row["path"]] = row


class Quarter:
    def __init__(self, data, config, q, reasons, index):
        self.data = data
        self.config = config
        self.q = q
        self.reasons = reasons
        self.ecosystems = [e for e in ("python", "node") if any(r["ecosystem"] == e for r in reasons)]
        if index % 2:
            self.ecosystems.reverse()
        self.views = {(r["ecosystem"], r["kind"], r["path"]): r for r in data.views[q]}
        self.keys = {(r["ecosystem"], r["kind"]): k for k, r in self.views.items()
                     if r["kind"] != "manual"}
        self.network = 0
        self.reviews = 0
        self.actions = []
        self.opened = {}

    def visit(self, key, wanted, linked_from="", queue_rank=None):
        doc = self.views[key]
        conf = self.config
        receipt = self.data.receipts[(conf.cache, self.q, *key)]
        if key in self.opened:
            self.actions.append(self.action(doc, "shared", 0, 0, wanted, linked_from, queue_rank))
            return self.opened[key]
        network = receipt["http_attempts"]
        if conf.cache == "reuse1" and key[1] != "git_tree":
            receipt = self.data.receipts[("cold", self.q, *key)]
            network = receipt["http_attempts"]
        cost = int(key[1] != "git_tree")
        failed = (doc["status"] not in {"ok", "missing"} or
                  conf.failure.startswith("stress") and self.q == "2023Q4" and
                  key[0] == "python" and key[1] in {"manual", "release_notes"})
        if failed and conf.failure == "stress_free_review":
            cost = 0
        if self.network + network > conf.budget or self.reviews + cost > conf.budget:
            self.actions.append(self.action(doc, "budget", 0, 0, wanted, linked_from, queue_rank))
            return None
        self.network += network
        self.reviews += cost
        status = "failure" if failed else doc["status"]
        self.opened[key] = doc | {"status": status}
        self.actions.append(self.action(doc, status, network, cost, wanted, linked_from, queue_rank) |
                            {f: receipt[f] for f in ("http_body_bytes", "git_pack_bytes", "elapsed_s",
                                                    "local_reads", "local_bytes", "retries", "new_objects")})
        return self.opened[key]

    def action(self, doc, status, network, cost, wanted, linked_from, queue_rank):
        return {"scenario": self.config.label, "quarter": self.q, "ecosystem": doc["ecosystem"],
                "kind": doc["kind"], "path": doc["path"], "url": doc["url"], "status": status,
                "http_attempts": network, "review_units": cost, "opened_original": status == "ok" and
                doc["kind"] != "git_tree", "reason_id": wanted, "linked_from": linked_from,
                "queue_rank": queue_rank}

    def findings(self, doc):
        if not doc or doc["status"] != "ok":
            return {}
        key = (self.q, doc["ecosystem"], doc["kind"], doc["path"])
        return {r["id"]: r for r in self.data.findings[key]}


def ranked(queues, ecosystems):
    for score in sorted({score for score, _ in queues}, reverse=True):
        while any(queues[score, eco] for eco in ecosystems):
            for eco in ecosystems:
                if queues[score, eco]:
                    yield queues[score, eco].popleft()


def replay(data, config):
    reasons = [r for r in data.cohort.values()
               if config.ecosystem == "both" or config.ecosystem == r["ecosystem"]]
    memories = {r["id"]: Remembered(r["blob"], r["warned"] == "1") for r in reasons}
    previous = {r["ecosystem"]: r["tag"] for k, r in data.releases.items() if k[0] == "T0"}
    results, actions = [], []
    for index, q in enumerate(data.quarters):
        quarter = Quarter(data, config, q, reasons, index)
        rows = {r["id"]: {"scenario": config.label, "quarter": q, "ecosystem": r["ecosystem"],
                          "id": r["id"], "path": r["path"], "stratum": r["stratum"], "score": 0,
                          "tree_signal": "", "warning_prior": memories[r["id"]].warned,
                          "new_version": False, "signal": False, "new_signal": False,
                          "outcome": "initial_error" if r["initial"] != "supported" else "no_visit",
                          "queue_rank": None, "new_report": False, "proof": "", "proof_kind": "",
                          "last_success_index": memories[r["id"]].last_visit}
                for r in reasons}
        queues = defaultdict(deque)
        guides, trees = {}, {}
        starts = sorted(reasons, key=lambda r: (memories[r["id"]].last_visit, order("queue", r["id"])))
        if config.policy != "N":
            for eco in quarter.ecosystems:
                quarter.visit(quarter.keys[eco, "catalog"], "")
                guides[eco] = quarter.visit(quarter.keys[eco, "release_index"], "")
            if config.policy == "S":
                for eco in quarter.ecosystems:
                    trees[eco] = quarter.visit(quarter.keys[eco, "git_tree"], "")
            for reason in starts:
                id, eco = reason["id"], reason["ecosystem"]
                if rows[id]["outcome"] == "initial_error":
                    continue
                release = data.releases[q, eco]
                row, memory = rows[id], memories[id]
                row["new_version"] = release["tag"] != previous[eco]
                doc = quarter.views[eco, "manual", reason["path"]]
                if config.policy == "S":
                    tree = trees.get(eco)
                    known = bool(tree and tree["status"] == "ok")
                    changed = known and doc["blob"] != memory.last_blob
                    row["tree_signal"] = "changed" if changed else "same" if known else "unknown"
                    row["score"] = 2 * int(changed) + int(memory.warned) + int(row["new_version"])
                    row["signal"] = row["score"] >= config.threshold
                    row["new_signal"] = row["signal"] and not memory.signal_active
                    memory.signal_active = row["signal"]
                    if not row["signal"]:
                        row["outcome"] = "below_threshold"
                        continue
                queues[row["score"], eco].append(reason)
        used_release = set()
        pending = []
        for rank, reason in enumerate(ranked(queues, quarter.ecosystems), 1):
            id, eco = reason["id"], reason["ecosystem"]
            row, memory = rows[id], memories[id]
            row["queue_rank"] = rank
            key = (eco, "manual", reason["path"])
            doc = quarter.visit(key, id, reason["t0_url"], rank)
            if not doc:
                row["outcome"] = "budget"
                continue
            if doc["status"] not in {"ok", "missing"}:
                row["outcome"] = "failed"
                continue
            detail = next(r for r in doc["reasons"] if r["id"] == id)
            finding = quarter.findings(doc).get(id)
            row["outcome"] = "evidence_gap"
            if doc["status"] == "ok":
                memory.last_blob = doc["blob"]
                memory.last_visit = index
                if finding:
                    apply_finding(row, memory, finding)
                elif detail["section"] == "present":
                    if detail["warned"]:
                        memory.warned = True
                    row["outcome"] = "manual_warning" if detail["warned"] else "manual_present"
            if row["outcome"] not in {"evidence_gap", "manual_uncertain"}:
                continue
            guide = guides.get(eco)
            if not guide or guide["status"] != "ok" or not guide["release_path"]:
                continue
            link = (eco, "release_notes", guide["release_path"])
            if link not in quarter.views:
                continue
            if eco not in used_release:
                follow = quarter.visit(link, id, guide["url"], rank)
                used_release.add(eco)
                for target, claim in quarter.findings(follow).items():
                    if rows[target]["outcome"] == "initial_error":
                        continue
                    pending.append((target, claim, id))
        for target, claim, trigger in pending:
            row, memory = rows[target], memories[target]
            if config.shared == "per_reason" and target != trigger:
                if quarter.reviews >= config.budget:
                    row["shared_deferred"] = True
                    continue
                quarter.reviews += 1
                doc = quarter.views[(claim["ecosystem"], claim["kind"], claim["path"])]
                quarter.actions.append(quarter.action(doc, "semantic_share", 0, 1, target,
                                                       claim["url"], row["queue_rank"]))
            apply_finding(row, memory, claim)
            if claim["status"] in {"invalid", "restored"}:
                memory.last_visit = index
                observed_tree = trees.get(row["ecosystem"])
                if observed_tree and observed_tree["status"] == "ok":
                    memory.last_blob = quarter.views[row["ecosystem"], "manual", row["path"]]["blob"]
        for reason in reasons:
            row = rows[reason["id"]]
            row["predicted_invalid"] = memories[row["id"]].invalid
        for eco in quarter.ecosystems:
            previous[eco] = data.releases[q, eco]["tag"]
        assert quarter.network <= config.budget and quarter.reviews <= config.budget
        actions.extend(quarter.actions)
        results.extend(rows.values())
    return results, actions


def apply_finding(row, memory, finding):
    status = finding["status"]
    if status == "invalid":
        row["new_report"] |= not memory.invalid
        memory.invalid = True
        memory.warned = False
    elif status == "restored":
        memory.invalid = False
        memory.warned = False
    elif status == "warning":
        memory.warned = True
    elif status == "supported":
        memory.warned = False
    row["outcome"] = f"{finding['kind']}_{status}"
    row["proof"] = finding["url"]
    row["proof_kind"] = finding["kind"]


def write_csv(path, rows):
    keys = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, keys, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=HERE)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--policy", choices=("N", "D", "S"), required=True)
    parser.add_argument("--budget", type=int, choices=(10, 20, 40), default=20)
    parser.add_argument("--threshold", type=int, choices=(1, 2, 3), default=2)
    parser.add_argument("--cache", choices=("cold", "reuse1", "reuse2"), default="cold")
    args = parser.parse_args()
    config = Config(args.policy, args.budget, args.threshold, args.cache)
    results, actions = replay(Inputs(args.inputs), config)
    args.out.mkdir(parents=True, exist_ok=True)
    write_csv(args.out / "reason-visits.csv", results)
    write_jsonl(args.out / "network-visits.jsonl", actions)


if __name__ == "__main__":
    main()
