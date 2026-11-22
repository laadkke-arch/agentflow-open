#!/usr/bin/env python3
"""Measure acquired bytes, preparation and successful probe work from receipts."""
import argparse
from collections import defaultdict
import csv
import json
from pathlib import Path

from run import load

HERE = Path(__file__).resolve().parent


def blob(name):
    return json.loads((HERE / "receipts" / name).read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--with-replay", action="store_true")
    args = parser.parse_args()
    entries = []

    def add(stage, key, outcome, seconds, bytes_, receipt, count=1):
        entries.append(dict(stage=stage, object=key, outcome=outcome, wall_s=seconds,
                            bytes=bytes_, count=count, receipt=receipt))

    releases = blob("acquisition.json")
    for release in releases:
        name = "/".join([release["ecosystem"], release["tag"]])
        for event in release["events"]:
            phase = event["phase"]
            size = ""
            if phase == "download":
                _, amount = event["response"].split()
                size = int(float(amount))
                phase = "asset_download"
                if event["file"] == "SHASUMS256.txt":
                    phase = "checksum_manifest"
            key = event.get("url", name)
            add(phase, key, "ok" if event["rc"] == 0 else f"failed:{event['rc']}",
                event["wall_s"], size, "receipts/acquisition.json")
    for eco in ("python", "node"):
        name = f"{eco}-tags.json"
        row = blob(name)
        add("tag_lookup", row["url"], "ok" if row["rc"] == 0 else f"failed:{row['rc']}",
            row["wall_s"], row["bytes"], f"receipts/{name}")
    for name in ("t0-manual-fetch.json", "official-file-fetch.json"):
        for row in blob(name):
            add("official_raw_file", row["url"], "ok" if row["rc"] == 0 else f"failed:{row['rc']}",
                row["wall_s"], row["bytes"], f"receipts/{name}")
    for row in blob("system-archives.json"):
        add("supplement_archive", row["url"], "ok", row["wall_s"], row["bytes"], "receipts/system-archives.json")
    for row in blob("tk-repair.json"):
        add("tk_repair", row["tag"], "ok" if row["rc"] == 0 else f"failed:{row['rc']}",
            row["wall_s"], "", "receipts/tk-repair.json")
    fixtures = {r["url"]: r for r in blob("python-first/fixtures-v1.json")}
    fixtures.update({r["url"]:r for r in json.loads((HERE/"probes/fixtures.json").read_text())})
    for url, row in fixtures.items():
        add("fixture_open", url, "ok", "", row["bytes"], "probes/fixtures.json and receipts/python-first/fixtures-v1.json")
    add("launch_preflight", "/usr/bin/time", "failed:127", "", "", "shell tool receipt and RESULT Q7")
    phases = ["node-first", "python-first", "first"]
    if args.with_replay:
        phases.append("clean-replay")
    for phase in phases:
        filename = f"receipts/{phase}/raw.jsonl"
        for row in load(HERE / filename):
            ok = row["grade"]=="direct"
            add(f"probe_{phase}", row["id"], "direct" if ok else ("unavailable" if row["rc"] is None else f"failed:{row['rc']}"),
                row["wall_s"], "", filename)
        versions = f"receipts/{phase}/versions.jsonl"
        for row in load(HERE / versions):
            add(f"version_verify_{phase}", f"{row['ecosystem']}/{row['tag']}",
                "ok" if row["valid"] else "failed", "", "", versions)
        if phase in ("first", "clean-replay"):
            time_file = f"receipts/{phase}/time.txt"
            timer = (HERE / time_file).read_text()
            elapsed = float(timer.split(";")[0].split("=")[1])
            code = int(timer.split("driver_rc=")[1].splitlines()[0])
            add(f"elapsed_{phase}", "all 42 cells", "ok" if code==0 else f"failed:{code}",
                elapsed, "", time_file)
    for row in load(HERE/"receipts/official-current.jsonl"):
        add("official_test_current", f"{row['tag']}/{row['test']}", "ok" if row["rc"]==0 else f"failed:{row['rc']}",
            row["wall_s"], "", "receipts/official-current.jsonl")
    for row in load(HERE/"receipts/pydoc-post-reveal.jsonl"):
        add("post_reveal_cli", f"{row['tag']}/{row['route']}", f"rc:{row['rc']}", row["wall_s"], "",
            "receipts/pydoc-post-reveal.jsonl")

    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out/"costs.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(entries[0]),lineterminator="\n")
        w.writeheader()
        w.writerows(entries)
    summary=defaultdict(lambda:dict(attempts=0,ok_or_direct=0,failed_or_unavailable=0,
                                    measured_bytes=0,sum_per_item_wall_s=0))
    for row in entries:
        totals=summary[row["stage"]]
        totals["attempts"]+=row["count"]
        success=row["outcome"] in {"ok","direct","rc:0"}
        totals["ok_or_direct"]+=int(success)*row["count"]
        totals["failed_or_unavailable"]+=int(not success)*row["count"]
        totals["measured_bytes"]+=row["bytes"] if row["bytes"]!="" else 0
        totals["sum_per_item_wall_s"]+=row["wall_s"] if row["wall_s"]!="" else 0
    for row in summary.values():
        row["sum_per_item_wall_s"]=round(row["sum_per_item_wall_s"],4)
    (args.out/"costs-summary.json").write_text(json.dumps(dict(summary),indent=2,sort_keys=True)+"\n")
    print(summary["official_raw_file"], summary["probe_first"])


if __name__ == "__main__":
    main()
