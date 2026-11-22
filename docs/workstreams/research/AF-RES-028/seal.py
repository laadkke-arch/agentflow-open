#!/usr/bin/env python3
"""Freeze the released input claims, direct receipts, and independent source reading."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

from run import encode, load, write

HERE = Path(__file__).resolve().parent


def log_summary(r):
    return dict(exit=r["rc"], stdout_sha256=r.get("stdout_sha256"), stderr_sha256=r.get("stderr_sha256"),
                stdout_lines=len(r["stdout"].splitlines()), stderr_lines=len(r["stderr"].splitlines()),
                stderr_first_line=next(iter(r["stderr"].splitlines()), ""))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    inputs = json.loads((args.run / "summary.json").read_text())
    logs = {r["id"]: r for r in load(args.run / "raw.jsonl")}
    versions = {f"{r['ecosystem']}/{r['tag']}": r for r in load(args.run / "versions.jsonl")}
    docs = {r["id"]: r for r in json.loads((HERE / "sources.json").read_text())}
    packets = {r["cell_id"]: r for r in load(HERE / "packets.jsonl")}
    tests = load(HERE / "receipts/official-current.jsonl")
    output, sources = [], []
    for item in load(args.run / "observations.jsonl"):
        name, cell = item["contract"], item["cell_id"]
        t0, target = item["t0_values"], item["target_values"]
        release = packets[cell]["target"]
        row = dict(item)
        row["run_verdict_v1"] = item["verdict"]
        row["alternative_verdict"] = ""
        if name == "histogram":
            def passes(values):
                diagnostic = values.get("diagnostic", {})
                positive = values.get("positive", {})
                return (diagnostic.get("mapBrand") is True and diagnostic.get("viaMapGet") == 2 and
                        positive.get("min") == 1 and positive.get("max") == 2 and values.get("boundary") == [5, 5])

            if item["direct_pair"] and passes(t0) and passes(target):
                row["verdict"] = "supported"
                row["reason"] = "revision 2: native Map brand, native get, endpoints and reset all match"
        elif name == "netrc":
            if (item["direct_pair"] and t0["diagnostic"]["anonymous_fixture"] == "NetrcParseError"
                    and target["diagnostic"]["anonymous_fixture"] == "parsed"):
                row["alternative_verdict"] = "invalid"
                row["alternative_scope"] = "unqualified password implication includes the anonymous fixture"
        elif name == "webcrypto":
            if (item["direct_pair"] and t0["diagnostic"]["proprietary"]["result"] == "imported"
                    and target["diagnostic"]["proprietary"]["result"] != "imported"):
                row["alternative_verdict"] = "invalid"
                row["alternative_scope"] = "T0 legacy algorithm name rather than literal EcKeyImportParams ECDSA"
        if not item["direct_pair"]:
            row["remaining"] = "미확인"
        else:
            row["remaining"] = ""
        row["environment"] = inputs["environment"]
        row["logs"] = {phase: log_summary(logs[item[phase]]) for phase in ("t0", "target")}
        row["binaries"] = {phase: versions.get(item[phase].rsplit("/", 1)[0], {}).get("sha256")
                           for phase in ("t0", "target")}
        output.append(row)
        manual = f"MT-{name}-{release['tag']}"
        referenced = [r["id"] for r in docs.values() if r["id"].startswith("I-") and cell in r["cells"]]
        primary_tests = [dict(tag=t["tag"], test=t["test"], rc=t["rc"], mode=t["observation"])
                         for t in tests if t["contract"] == name and t["tag"] in (packets[cell]["t0"]["tag"], release["tag"])]
        if name == "wasi":
            test_scope = "v20.3.1 official test source passes explicit version; historical log unconfirmed"
        elif name == "netrc":
            test_scope = "dated test source and current reexecution verify local ordinary-mode control only"
        elif name == "imap" and release["tag"] == "v3.13.2":
            test_scope = "dated test source and current reexecution verify SSLContext alternate path"
        elif name == "venv" and release["tag"] == "v3.13.5":
            test_scope = "dated test source and current reexecution verify config flags"
        else:
            test_scope = "미확인"
        sources.append(dict(cell_id=cell, direct=row["verdict"], t0_source=f"M-{name}", target_source=manual,
                            target_document=docs[manual]["document_assessment"],
                            target_document_finding=docs[manual]["observed"],
                            static_sources=referenced, official_test_scope=test_scope,
                            current_upstream_test_results=primary_tests,
                            historical_official_execution="미확인"))
    assert len(output) == len(packets) == 42
    write(args.out / "observations.jsonl", output)
    write(args.out / "blind-review.jsonl", sources)
    core = ("cell_id", "contract", "t0_values", "target_values", "direct_pair", "verdict", "alternative_verdict")
    rows_for_hash = [{k: row[k] for k in core} for row in output]
    sealed = {}
    for folder, names in [(args.run, ("raw.jsonl", "observations.jsonl", "versions.jsonl", "summary.json")),
                          (args.out, ("observations.jsonl", "blind-review.jsonl")),
                          (HERE, ("scope-lock.json", "contracts.jsonl", "contract-amendments.jsonl", "sources.json"))]:
        key = "executed" if folder == args.run else "blinded" if folder == args.out else "design"
        sealed[key] = {name: sha256((folder / name).read_bytes()).hexdigest() for name in names}
    sealed["canonical_judgment_sha256"] = sha256(encode(rows_for_hash)).hexdigest()
    sealed["input_sha256"] = inputs["input_sha256"]
    sealed["answer_unopened"] = True
    (args.out / "observation-seal.json").write_text(json.dumps(sealed, indent=2, sort_keys=True) + "\n")
    print(sealed["canonical_judgment_sha256"])


if __name__ == "__main__":
    main()
