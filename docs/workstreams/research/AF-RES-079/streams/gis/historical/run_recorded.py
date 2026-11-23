"""Run a task-local environment/probe command and preserve its exact receipt."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("label")
parser.add_argument("command", nargs=argparse.REMAINDER)
args = parser.parse_args()
command = args.command[1:] if args.command[:1] == ["--"] else args.command
environment = dict(os.environ)
scoped = {"MAMBA_ROOT_PREFIX": str(ROOT / "cache/mamba"),
          "CONDA_PKGS_DIRS": str(ROOT / "cache/pkgs"),
          "XDG_CACHE_HOME": str(ROOT / "cache/xdg"),
          "PYTHONPYCACHEPREFIX": str(ROOT / "cache/pycache")}
environment.update(scoped)
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
start = time.monotonic()
log = ROOT / (args.label + ".log")
with log.open("wb") as output:
    process = subprocess.run(command, cwd=ROOT, env=environment, stdout=output,
                             stderr=subprocess.STDOUT)
record = {"check_id": args.label, "actor": "gis_evidence tool agent",
          "location": "ChatGPT cloud Linux isolated task-local environment",
          "started_utc": started,
          "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "command": command, "cwd": str(ROOT), "scoped_environment": scoped,
          "exit_code": process.returncode, "elapsed_seconds": time.monotonic()-start,
          "output_file": log.name,
          "output_sha256": hashlib.sha256(log.read_bytes()).hexdigest()}
(ROOT / (args.label + ".json")).write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
print(log.read_text(errors="replace")[-12000:])
raise SystemExit(process.returncode)
