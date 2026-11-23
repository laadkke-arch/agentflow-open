#!/usr/bin/env python3
"""Run every sealed MuseScore cell twice in fresh process work directories."""
import argparse
import csv
import datetime as dt
import hashlib
import itertools
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

PACKET = Path(__file__).resolve().parent.parent
FIXTURE = PACKET / "fixtures/two-parts.mscx"
SOURCE = "f4fcf53ff65c56f0efb616a3af209d3faba9b342"
VARIANTS = "UGL"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def run_case(cell, case, variant, repeat, binary, binary_hash, out):
    label = f"{cell:02d}-{case['case_id']}-{variant}/r{repeat}"
    result_dir = out / "evidence/runs" / label
    result_dir.mkdir(parents=True)
    record = {
        "cell": cell, "case_id": case["case_id"], "build": variant, "repeat": repeat,
        "layer": case["layer"], "source_commit": SOURCE, "input_sha256": digest(FIXTURE),
        "binary_sha256": binary_hash, "start_utc": utc(), "exit_code": None,
        "qpa": "offscreen", "artifacts": {},
    }
    if not binary.is_file():
        record.update(status="not_run", reason=f"missing executable {binary}", finish_utc=utc())
        return record
    with tempfile.TemporaryDirectory(prefix="af081-") as folder:
        workdir = Path(folder)
        if any(workdir.iterdir()):
            raise RuntimeError(f"run directory was not initially empty: {workdir}")
        runtime = workdir / "runtime"
        runtime.mkdir(mode=0o700)
        env = {
            **os.environ, "QT_QPA_PLATFORM": "offscreen", "LC_ALL": "C.UTF-8",
            "XDG_RUNTIME_DIR": str(runtime), "XDG_CONFIG_HOME": str(workdir / "config"),
            "XDG_DATA_HOME": str(workdir / "data"), "XDG_CACHE_HOME": str(workdir / "cache"),
        }
        argv = [str(binary), case["case_id"], str(FIXTURE), "roundtrip.mscx"]
        record.update(argv=argv, cwd=str(workdir), empty_at_start=True)
        started = time.monotonic()
        try:
            process = subprocess.run(argv, cwd=workdir, env=env, capture_output=True, timeout=30)
            stdout, stderr = process.stdout, process.stderr
            record.update(exit_code=process.returncode, status="completed" if process.returncode == 0 else "failed")
        except subprocess.TimeoutExpired as error:
            stdout, stderr = error.stdout or b"", error.stderr or b""
            record.update(status="failed", reason="timeout after 30 seconds")
        except OSError as error:
            stdout, stderr = b"", str(error).encode()
            record.update(status="failed", reason="process launch error")
        record["elapsed_seconds"] = round(time.monotonic() - started, 6)
        record["finish_utc"] = utc()
        (result_dir / "stdout.jsonl").write_bytes(stdout)
        (result_dir / "stderr.txt").write_bytes(stderr)
        written = workdir / "roundtrip.mscx"
        if written.is_file():
            shutil.copyfile(written, result_dir / written.name)
        for filename in ("stdout.jsonl", "stderr.txt", "roundtrip.mscx"):
            path = result_dir / filename
            if path.is_file():
                record["artifacts"][filename] = {
                    "path": str(path.relative_to(out)), "sha256": digest(path), "bytes": path.stat().st_size,
                }
    return record


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--binaries", type=Path, required=True)
    cli.add_argument("--out", type=Path, required=True, help="new output directory")
    args = cli.parse_args()
    with (PACKET / "cases.csv").open(newline="") as stream:
        cases = list(csv.DictReader(stream))
    if any(row["input_sha256"] != digest(FIXTURE) for row in cases):
        cli.error("input digest differs from the sealed cases")
    binaries = {v: args.binaries.resolve() / f"af_res_081-{v}" for v in VARIANTS}
    hashes = {v: digest(path) if path.is_file() else None for v, path in binaries.items()}
    args.out.mkdir()
    failed = False
    with (args.out / "runs.jsonl").open("x") as ledger:
        for cell, (case, variant) in enumerate(itertools.product(cases, VARIANTS), start=1):
            for repeat in (1, 2):
                record = run_case(cell, case, variant, repeat, binaries[variant], hashes[variant], args.out)
                print(json.dumps(record, ensure_ascii=False), file=ledger, flush=True)
                print(cell, case["case_id"], variant, repeat, record["status"], record["exit_code"])
                failed |= record["status"] != "completed"
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
