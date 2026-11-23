"""Run each file-reader-repeat in a separate process and retain its output."""
import argparse
import csv
import json
import subprocess
from pathlib import Path

from generate import HERE, PLAN, utc


def read_one(lab, ident, file, expected_hash, role, repeat, log_dir):
    cmd = [
        str(lab / f"venv-{role}/bin/python"), "-B", str(HERE / "observe.py"),
        role, str(lab / f"src-{role}"), ident, str(file), expected_hash, str(repeat),
    ]
    start = utc()
    process = subprocess.run(cmd, text=True, capture_output=True)
    end = utc()
    stderr = None
    if process.stderr:
        path = log_dir / f"{ident}-{role}-{repeat}.stderr.txt"
        path.write_text(process.stderr)
        stderr = path.name
    try:
        record = json.loads(process.stdout)
    except json.JSONDecodeError:
        record = {"outcome": "environment_or_harness_failure", "stdout": process.stdout}
    return {
        "file_id": ident, "role": role, "repeat": repeat,
        "command": cmd, "start_utc": start, "finish_utc": end,
        "process_exit": process.returncode, "stderr_log_basename": stderr,
        **record,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lab", type=Path)
    parser.add_argument("input", type=Path, help="directory with files.csv and fixtures")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    work = args.input.resolve()
    log_dir = args.output / "evidence/reads"
    log_dir.mkdir(parents=True, exist_ok=True)
    with (work / "files.csv").open(newline="") as summary:
        files = {r["file_id"]: r for r in csv.DictReader(summary)}
    records = []
    for file_id in PLAN["files"]:
        row = files[file_id]
        for role in PLAN["readers"]:
            for repeat in range(1, PLAN["repetitions_per_cell"] + 1):
                if row["status"] == "generation_failed":
                    record = {"file_id": file_id, "role": role, "repeat": repeat,
                              "outcome": "reader_skip", "reason": "generation_failed",
                              "process_exit": None}
                else:
                    record = read_one(args.lab, file_id, work / row["file"], row["file_sha256"],
                                      role, repeat, log_dir)
                records.append(record)
    with (args.output / "runs.jsonl").open("w") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
    print(json.dumps([(r["file_id"], r["role"], r["repeat"], r["process_exit"], r["outcome"])
                      for r in records], indent=2))
    return int(any(r["outcome"] not in {"preserved", "silent_loss", "explicit_rejection"} for r in records))


if __name__ == "__main__":
    raise SystemExit(main())
