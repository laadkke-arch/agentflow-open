#!/usr/bin/env python3
"""Copy explicit, synthetic inputs and outputs, leaving the app profiles in scratch."""
import argparse
import csv
from pathlib import Path
import shutil


def collect(raw, evidence):
    evidence.mkdir(parents=True)
    for file in sorted(raw.iterdir()):
        if not file.is_file():
            continue
        if file.name in {"app.jsonl", "app.stderr", "steps.jsonl", "result.json"} or file.suffix == ".png":
            shutil.copyfile(file, evidence / file.name)
        elif file.name in {"after-v.mscx", "after-undo.mscx"}:
            shutil.copyfile(file, evidence / file.name)
    for name in ("read-e", "read-u"):
        if (raw / name).is_dir():
            collect(raw / name, evidence / name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--dest", type=Path, required=True)
    parser.add_argument("--phase", choices=("controls", "main", "auxiliary"), required=True)
    args = parser.parse_args()
    if args.phase == "auxiliary":
        for case in ("F-P", "F-X", "PEER", "VV"):
            for build in "GL":
                run = f"{case}-{build}"
                collect(args.raw / run, args.dest / run)
        return
    packet = Path(__file__).resolve().parents[1]
    with (packet / "cases.csv").open(newline="") as file:
        for row in csv.DictReader(file):
            if (row["case"] in {"P", "N"}) == (args.phase == "controls"):
                run = row["run_id"]
                collect(args.raw / run, args.dest / run)


if __name__ == "__main__":
    main()
