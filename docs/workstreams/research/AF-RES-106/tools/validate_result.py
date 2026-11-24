"""Run required checks at one clean result SHA; write receipts only afterwards."""
from pathlib import Path
import datetime
import hashlib
import json
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
OUT = ROOT / "evidence/validation"


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO, text=True).strip()


def main():
    head = git("rev-parse", "HEAD")
    dirty = git("status", "--porcelain")
    if dirty:
        raise SystemExit("Requires a completely clean committed result checkout, including untracked files.")
    commands = [
        ("research_structure", ["python", "-B", "docs/workstreams/research/AF-RES-106/tools/verify.py"]),
        ("session_check", ["python", "-B", "-m", "workbench.session", "check", "docs/workstreams/research/AF-RES-106/manifest.json", "--fetch"]),
        ("cloud_check", ["python", "-B", "scripts/cloud_check.py", "--environment", "codex-cloud", "--fetch-contract", "--require-clean"]),
    ]
    records, outputs = [], {}
    for label, argv in commands:
        started, before = utc(), git("status", "--porcelain")
        run = subprocess.run(argv, cwd=REPO, capture_output=True, timeout=600)
        finished, after = utc(), git("status", "--porcelain")
        outputs[label + ".stdout.txt"] = run.stdout
        outputs[label + ".stderr.txt"] = run.stderr
        records.append({"name": label, "command": argv, "command_text": " ".join(argv),
                        "started_utc": started, "finished_utc": finished, "result_sha": head,
                        "head_after": git("rev-parse", "HEAD"), "exit_code": run.returncode,
                        "clean_before": not before, "clean_after": not after,
                        "stdout_path": "evidence/validation/" + label + ".stdout.txt",
                        "stderr_path": "evidence/validation/" + label + ".stderr.txt",
                        "stdout_sha256": hashlib.sha256(run.stdout).hexdigest(),
                        "stderr_sha256": hashlib.sha256(run.stderr).hexdigest()})
    final_clean = not git("status", "--porcelain")
    evidence = {"result_sha": head, "branch": git("branch", "--show-current"), "receipt_written_utc": utc(),
                "python": sys.version, "platform": platform.platform(), "clean_at_start": True,
                "clean_after_all_commands_before_receipt": final_clean, "commands": records,
                "scope": "Research integrity plus explicit manifest1 and required common repository checks. Environment label codex-cloud is caller supplied, not account-connection proof.",
                "passed": final_clean and all(r["exit_code"] == 0 and r["clean_before"] and r["clean_after"] and r["head_after"] == head for r in records)}
    # All requested --require-clean commands have finished before these writes.
    OUT.mkdir(parents=True, exist_ok=True)
    for name, data in outputs.items():
        (OUT / name).write_bytes(data)
    common = REPO / ".workbench/cloud-check.json"
    if common.exists():
        raw = common.read_bytes()
        (OUT / "cloud-check.receipt.json").write_bytes(raw)
        evidence["cloud_receipt_sha256"] = hashlib.sha256(raw).hexdigest()
    (OUT / "run.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"result_sha": head, "passed": evidence["passed"], "commands": [{k: v for k, v in r.items() if k in ["name", "exit_code", "started_utc", "finished_utc", "clean_before", "clean_after"]} for r in records]}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if evidence["passed"] else 1)


if __name__ == "__main__":
    main()
