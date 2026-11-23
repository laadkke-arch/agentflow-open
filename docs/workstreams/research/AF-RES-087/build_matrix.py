"""Build four files, record writer processes, and compare independent footers."""
import argparse
import csv
import json
import subprocess
from pathlib import Path

from generate import HERE, PLAN, utc

FIELDS = [
    "file_id", "writer", "schema_version", "requested_encoding", "actual_encoding",
    "input_sha256", "file_sha256", "footer_sha256", "bytes", "status", "writer_exit",
    "footer_exit", "file", "writer_log", "footer",
]


def invoke(argv, log):
    start = utc()
    result = subprocess.run(argv, text=True, capture_output=True)
    log.with_suffix(".stdout.json").write_text(result.stdout)
    log.with_suffix(".stderr.txt").write_text(result.stderr)
    log.with_suffix(".process.json").write_text(json.dumps({
        "command": [str(arg) for arg in argv],
        "utc_start": start,
        "utc_finish": utc(),
        "exit": result.returncode,
    }, indent=2) + "\n")
    return result.returncode, json.loads(result.stdout) if result.stdout.strip() else {}


def differences(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        for key in sorted(a.keys() | b.keys()):
            yield from differences(a.get(key, "<absent>"), b.get(key, "<absent>"), f"{path}/{key}")
    elif a != b:
        yield {"path": path, "left": a, "right": b}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lab", type=Path, help="directory containing venv-O/N and src-O/N")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    lab = args.lab.resolve()
    evidence = output / "evidence/build"
    fixtures = output / "fixtures"
    evidence.mkdir(parents=True, exist_ok=True)
    fixtures.mkdir(parents=True, exist_ok=True)
    envs, footers, rows = {}, {}, []
    for role in ("O", "N"):
        exit_code, env = invoke([
            lab / f"venv-{role}/bin/python", "-B", HERE / "generate.py",
            "env", role, lab / f"src-{role}",
        ], evidence / f"env-{role}")
        envs[role] = {"exit": exit_code, **env}
    (output / "environments.json").write_text(json.dumps(envs, ensure_ascii=False, indent=2) + "\n")
    for file_id, config in PLAN["files"].items():
        role = config["writer"]
        file_name = f"fixtures/{file_id}.parquet"
        path = output / file_name
        writer_exit, writer = invoke([
            lab / f"venv-{role}/bin/python", "-B", HERE / "generate.py",
            "write", file_id, lab / f"src-{role}", path,
        ], evidence / f"{file_id}-writer")
        row = {
            "file_id": file_id, "writer": role, "schema_version": config["schema_version"],
            "requested_encoding": config["encoding"], "input_sha256": PLAN["common_input_sha256"],
            "writer_exit": writer_exit, "writer_log": f"evidence/build/{file_id}-writer.stdout.json",
        }
        if writer_exit != 0:
            rows.append(row | {"status": "generation_failed"})
            continue
        footer_exit, footer = invoke([
            lab / "venv-N/bin/python", "-B", HERE / "generate.py", "footer", path,
        ], evidence / f"{file_id}-footer")
        row.update(footer_exit=footer_exit, file=file_name, file_sha256=writer["file_sha256"],
                   bytes=writer["bytes"], footer=f"evidence/build/{file_id}-footer.stdout.json")
        if footer_exit != 0 or footer["file_sha256"] != row["file_sha256"]:
            rows.append(row | {"status": "footer_failed"})
            continue
        footers[file_id] = footer
        rows.append(row | {
            "actual_encoding": "/".join(c["encoding"] for c in footer["geo"]["columns"].values()),
            "footer_sha256": footer["footer_sha256"],
            "status": "generated",
        })
    with (output / "files.csv").open("w", newline="") as file:
        csv_writer = csv.DictWriter(file, fieldnames=FIELDS)
        csv_writer.writeheader()
        csv_writer.writerows(rows)

    keys = ("geo", "crs", "pandas_metadata", "arrow_fields", "parquet_columns",
            "schema_metadata_sha256", "format_version", "created_by", "rows", "row_groups")
    pairs = {}
    for left, right in (("F1", "F2"), ("F2", "F3"), ("F3", "F4")):
        if left in footers and right in footers:
            pairs[f"{left}/{right}"] = list(differences(
                {k: footers[left][k] for k in keys}, {k: footers[right][k] for k in keys}
            ))
    (evidence / "footer-differences.json").write_text(
        json.dumps(pairs, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps({"files": rows, "footer_pairs": list(pairs)}))
    return int(len(footers) != len(PLAN["files"]) or any(env["exit"] for env in envs.values()))


if __name__ == "__main__":
    raise SystemExit(main())
