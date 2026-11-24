"""Run the fixed inputs through the A/B adapters and the Gallim SQLite ledger."""
import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path
import platform
import sqlite3
import sys
from tempfile import TemporaryDirectory
from time import perf_counter

from adapters import evaluate, select
from lifecycle import checked, lifecycle, table_counts
from prototype import calibration, load_frozen

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ("inputs.jsonl", "facts.jsonl", "rules.json")
POLICY = "document-criteria.af111.1"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_inputs():
    allowed = {ROOT / name for name in INPUTS}
    accessed = []

    def audit(event, args):
        if event != "open" or not isinstance(args[0], (str, bytes)):
            return
        path = Path(args[0].decode() if isinstance(args[0], bytes) else args[0]).resolve()
        if not path.is_relative_to(ROOT):
            return
        if path not in allowed:
            raise PermissionError(f"workstream data outside input allowlist: {path.name}")
        accessed.append(path.name)

    sys.addaudithook(audit)
    values = {}
    fingerprints = {}
    for name in INPUTS:
        raw = (ROOT / name).read_bytes()
        fingerprints[name] = hashlib.sha256(raw).hexdigest()
        text = raw.decode("utf-8")
        values[name] = [json.loads(row) for row in text.splitlines()] if name.endswith(".jsonl") else json.loads(text)
    requests = values["inputs.jsonl"]
    cases = values["facts.jsonl"]
    assert len(requests) == 36 and len(cases) == 6
    assert values["rules.json"]["budget"]["candidates"] == 1
    for request in requests:
        assert set(request) == {"case_id", "id", "parts", "text"}
        assert request["id"].startswith("read-") and len(request["id"]) == 15
        assert set(request["parts"]) == {"operation", "preserve"}
        for span in request["parts"].values():
            assert span is None or (0 <= span[0] < span[1] <= len(request["text"]))
    return requests, cases, values["rules.json"], fingerprints, accessed


def store_facts(db, facts):
    for evidence in facts:
        source = evidence["source"]
        fragment_id = evidence["evidence_id"]
        doc = "capture/" + fragment_id
        quote = source["quote"]
        assert source["excerpt_sha256"] == digest(quote)
        db.add_document(doc, source["url"], source["source_id"])
        db.add_source(doc, "captured.1", quote, source["selector"])
        db.add_fragment(fragment_id, doc, "captured.1", 0, len(quote), source["url"])


def one_request(db, method, request, case, rules):
    request_id = request["id"]
    candidate = case["candidate"]
    cid = candidate["id"]
    edition_id = cid + "@" + candidate["version"]
    context_id = request_id + "/" + edition_id
    requirements = []
    for criterion, span in request["parts"].items():
        # The original request still carries the mandatory criterion when its
        # text has been omitted. No evidence is linked to this placeholder.
        start, end = span if span is not None else (0, len(request["text"]))
        requirements.append(dict(id=criterion, label=criterion, required=True, start_char=start, end_char=end))
    by_id = {f["evidence_id"]: f for f in case["evidence"]}
    edges = select(method, request, case, rules)
    with db.transaction():
        db.add_request(request_id, request_id, request["text"], requirements)
        db.add_resource(cid, cid, "research candidate")
        db.add_edition(edition_id, cid, candidate["version"])
        db.add_context(context_id, request_id, edition_id, canonical(case["public_map"]), candidate["configuration"])
        for edge in edges:
            if edge["direction"] is None:
                continue
            xid = canonical([request_id, edge["criterion"], edge["evidence_id"]])
            edge["claim_id"] = digest(xid)
            source = by_id[edge["evidence_id"]]
            db.add_claim(edge["claim_id"], context_id, context_id, edge["criterion"],
                         source["kind"], edge["direction"], edge["evidence_id"], source["statement"])
        numeric_run = db.publish_decision(context_id, method + "/" + request_id, evaluate, POLICY)
    run = db.get_decision(numeric_run)
    outcome = run["output"]
    verified_links = {
        claim_id for decision in outcome["criteria"].values() for claim_id in decision["used"]
    }
    active = {
        row["claim_id"] for row in db.conn.execute(
            "SELECT rc.claim_id FROM run_claim rc WHERE rc.run_id=? AND rc.eligibility='active'", (numeric_run,)
        )
    }
    assert verified_links == active
    input_sha = digest(canonical({"request": request, "case": case, "rules": rules}))
    proof_ids = {name: [] for name in request["parts"]}
    for edge in edges:
        accepted = edge.get("claim_id") in verified_links
        if accepted:
            proof_ids[edge["criterion"]].append(edge["evidence_id"])
        row = by_id[edge["evidence_id"]]
        src = row["source"]
        edge.update(
            method=method, id=request_id, run_id=numeric_run, candidate=cid,
            version=candidate["version"], input_sha256=input_sha, used=accepted,
            source_id=src["source_id"], source_url=src["url"], selector=src["selector"],
            original_start=src["origin_start"], original_end=src["origin_end"],
            original_sha256=src["origin_sha256"], excerpt_sha256=src["excerpt_sha256"],
        )
    receipt = {
        "layer": "main", "id": request_id, "case_id": case["case_id"], "method": method,
        "candidate": cid, "candidate_context": context_id, "version": candidate["version"],
        "run_id": numeric_run, "input_sha256": input_sha,
        "decision_input_sha256": digest(canonical(run["input"])),
        "decision_output_sha256": digest(canonical(outcome)),
        "operation_key": run["operation_key"], "status": outcome["status"], "parts": request["parts"],
        "states": {k: row["state"] for k, row in outcome["criteria"].items()},
        "evidence": {k: sorted(value) for k, value in proof_ids.items()},
        "used_claims": sorted(verified_links),
    }
    return receipt, edges


def method_db(path, method, requests, cases, rules):
    from store import Ledger

    runs, links = [], []
    with Ledger(path) as db:
        initial_counts = table_counts(db)
        by_case = {c["case_id"]: c for c in cases}
        for case in cases:
            store_facts(db, case["evidence"])
        for request in requests:
            receipt, edges = one_request(db, method, request, by_case[request["case_id"]], rules)
            runs.append(receipt)
            links.extend(edges)
        checked(db)
        counts = table_counts(db)
        summary = {
            "initial_counts": initial_counts, "table_counts": counts,
            "freelist_pages": db.conn.execute("PRAGMA freelist_count").fetchone()[0],
            "page_count": db.conn.execute("PRAGMA page_count").fetchone()[0],
            "page_size": db.conn.execute("PRAGMA page_size").fetchone()[0],
        }
    summary["database_bytes"] = path.stat().st_size
    return runs, links, summary


def controls(cases, rules):
    from store import Ledger

    # The controls are derived from the source category, outside the 36 requests.
    d3 = next(c for c in cases if c["case_id"] == "D3")
    two_names = copy.deepcopy(d3)
    for obj in two_names["public_map"]["objects"][:2]:
        obj["names"].append("clone Alpha")
    no_version = copy.deepcopy(d3)
    no_version["context"]["version"] = None
    spaces = (
        ("equal-name", two_names, "Relink the clone Alpha to the yellow square. Keep the clone Alpha visible."),
        ("unclear-pronoun", d3, "Relink it to the yellow square. Keep it visible."),
        ("version-absent", no_version, "The clone should relink to the yellow square. select the clone (right red square)."),
        ("literal-collision", d3,
         "The clone should not relink to the yellow square. select the clone (right red square)."),
        ("provided-component-names", d3,
         "Relink the right red square to the yellow square. Keep the right red square visible."),
    )
    result = []
    for name, case, text in spaces:
        part = text.index(".") + 1
        request = {"id": "control-" + name, "case_id": case["case_id"],
                   "text": text, "parts": {"operation": [0, part], "preserve": [part+1, len(text)]}}
        for method in ("A", "B"):
            with Ledger(":memory:") as db:
                store_facts(db, case["evidence"])
                found, trace = one_request(db, method, request, case, rules)
                checked(db)
            result.append({"control": name, "input_origin": "researcher-authored",
                           "input": request, "run": found, "links": trace})
    return result


def write_jsonl(path, rows):
    path.write_text("".join(canonical(row) + "\n" for row in rows), encoding="utf-8")


def csv_value(value):
    return canonical(value) if isinstance(value, (dict, list)) else value


def write_csv(path, rows):
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows({k: csv_value(v) for k, v in row.items()} for row in rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    options = parser.parse_args()
    out = options.out.resolve()
    if out.is_relative_to(ROOT):
        parser.error("use a new temporary directory outside the workstream")
    out.mkdir(parents=True, exist_ok=False)
    requests, cases, rules, inputs, accessed = read_inputs()
    runs, links, costs = [], [], {}
    with TemporaryDirectory(prefix="af111-python-") as temporary:
        folder = Path(temporary)
        pins = load_frozen(folder)
        for method in ("A", "B"):
            t0 = perf_counter()
            observed, edges, costs[method] = method_db(out / (method + ".sqlite"), method, requests, cases, rules)
            costs[method]["duration_seconds"] = perf_counter() - t0
            runs.extend(observed)
            links.extend(edges)
        history = lifecycle(out / "original-history.sqlite")
        initial = calibration(folder)
        extras = controls(cases, rules)
    write_jsonl(out / "runs.jsonl", runs)
    write_csv(out / "links.csv", links)
    write_csv(out / "lifecycle.csv", history)
    write_jsonl(out / "calibration.jsonl", initial)
    write_jsonl(out / "controls.jsonl", extras)
    report = {
        "python": platform.python_version(), "sqlite": sqlite3.sqlite_version, "platform": platform.platform(),
        "frozen_blobs": pins, "input_files": inputs, "observed_workstream_input_opens": accessed,
        "planned": 72, "main": len(runs), "edges": len(links), "lifecycle": len(history),
        "calibration": len(initial), "post_recruitment_controls": len(extras),
        "db_costs": costs,
        "results_sha256": {name: hashlib.sha256((out / name).read_bytes()).hexdigest() for name in
            ("runs.jsonl", "links.csv", "lifecycle.csv", "calibration.jsonl", "controls.jsonl")},
    }
    (out / "receipt.json").write_text(canonical(report) + "\n", encoding="utf-8")
    print(canonical(report))


if __name__ == "__main__":
    main()
