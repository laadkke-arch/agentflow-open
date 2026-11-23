#!/usr/bin/env python3
"""AF-RES-053 frozen researcher replay. All writes stay below this directory.

Usage: python reproduce.py setup | render | analyze
This does not read issue comments, patches, or later public output.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.request

BASE = Path(__file__).resolve().parent
SCRATCH = BASE / "scratch"
RUNTIME = SCRATCH / "runtime"
LOGS = BASE / "logs"
FROZEN_SHA = "9b13473a76a381fe27d775524aa65416ec28f591"

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def fetch(name, url, expected=None):
    path = SCRATCH / name
    before = utc()
    req = urllib.request.Request(url, headers={"User-Agent": "AF-RES-053-public-research"})
    with urllib.request.urlopen(req, timeout=45) as response:
        data = response.read()
        row = dict(url=url, final_url=response.url, status=response.status,
                   started_UTC=before, finished_UTC=utc(), bytes=len(data), sha256=sha(data))
    if expected and sha(data) != expected:
        raise RuntimeError(f"Integrity mismatch for {url}")
    path.write_bytes(data)
    row["cache"] = str(path.relative_to(BASE))
    receipts_path = BASE / "setup-retrieval-receipts.json"
    receipts = json.loads(receipts_path.read_text()) if receipts_path.exists() else []
    receipts.append(row)
    save_json(receipts_path, receipts)
    return data

def run_record(label, args, cwd):
    LOGS.mkdir(exist_ok=True)
    env = os.environ.copy()
    env["npm_config_cache"] = str(SCRATCH / "npm-cache")
    env["npm_config_audit"] = "false"
    env["npm_config_fund"] = "false"
    env["YARN_CACHE_FOLDER"] = str(SCRATCH / "yarn-cache")
    env["TZ"] = "UTC"
    start = utc()
    p = subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True)
    (LOGS / f"{label}.stdout.txt").write_text(p.stdout)
    (LOGS / f"{label}.stderr.txt").write_text(p.stderr)
    rec = dict(label=label, argv=args, cwd=str(cwd.relative_to(BASE)) or ".",
               started_UTC=start, finished_UTC=utc(), exit_code=p.returncode,
               stdout=f"logs/{label}.stdout.txt", stderr=f"logs/{label}.stderr.txt",
               stdout_sha256=sha(p.stdout.encode()), stderr_sha256=sha(p.stderr.encode()))
    save_json(LOGS / f"{label}.receipt.json", rec)
    print(json.dumps(rec, ensure_ascii=False))
    print(p.stdout, end="")
    if p.stderr:
        print(p.stderr, file=sys.stderr, end="")
    if p.returncode:
        raise SystemExit(p.returncode)

def setup():
    SCRATCH.mkdir(exist_ok=True)
    RUNTIME.mkdir(exist_ok=True)
    package_path = SCRATCH / "vega-lite-v5.1.0-package.json"
    lock_path = SCRATCH / "vega-lite-v5.1.0-yarn.lock"
    registry_path = SCRATCH / "vega-lite-v5.1.0-registry.json"
    resources = [
        (package_path, "https://raw.githubusercontent.com/vega/vega-lite/v5.1.0/package.json", "18af378d9658a2e5fe85e74a7c7c65cac2ffe496c703e34ea4d63a8ffcd00dd6"),
        (lock_path, "https://raw.githubusercontent.com/vega/vega-lite/v5.1.0/yarn.lock", "3566c36709b3bbfd6bf586e8936a2dcbd402fad270229beab5505b397e0732fe"),
        (registry_path, "https://registry.npmjs.org/vega-lite/5.1.0", None),
    ]
    for path, url, expected in resources:
        if not path.exists():
            fetch(path.name, url, expected)
        elif expected and sha(path.read_bytes()) != expected:
            raise RuntimeError(f"Cached source hash mismatch: {path.name}")
    package = json.loads(package_path.read_text())
    registry = json.loads(registry_path.read_text())
    assert package["version"] == registry["version"] == "5.1.0"
    assert package["peerDependencies"]["vega"] == "^5.20.0"
    assert registry["dist"]["tarball"] == "https://registry.npmjs.org/vega-lite/-/vega-lite-5.1.0.tgz"
    assert registry["dist"]["integrity"] == "sha512-HEyf0iHnCNmWkWFIbEmMphcJwZpcBnfnU8v+Ojrndr7ihDueojHMOSikoyz/GNpdkai+QFxLboA6DDCTtFv9iQ=="
    lock = lock_path.read_text()
    assert 'vega@5.20.2:\n  version "5.20.2"' in lock
    # The release is the root project, hence it has no own entry in its yarn.lock.
    # Add exactly its npm release metadata; retain every original transitive pin.
    entry = ['\nvega-lite@5.1.0:', '  version "5.1.0"',
             '  resolved ' + json.dumps(registry["dist"]["tarball"]),
             '  integrity ' + registry["dist"]["integrity"], '  dependencies:']
    for name, version in sorted(registry["dependencies"].items()):
        entry.append('    ' + json.dumps(name) + ' ' + json.dumps(version))
    frozen_lock = lock + "\n".join(entry) + "\n"
    (RUNTIME / "yarn.lock").write_text(frozen_lock)
    save_json(RUNTIME / "package.json", {
        "name": "af-res-053-researcher-replay", "version": "1.0.0", "private": True,
        "dependencies": {"vega-lite": "5.1.0", "vega": "5.20.2"}
    })
    save_json(BASE / "dependency-pins.json", {
        "frozen_prediction_sha": FROZEN_SHA,
        "vega_lite": "5.1.0", "vega": "5.20.2", "package_manager": "yarn@1.22.10",
        "vega_selection": "v5.1.0 yarn.lock entry vega@5.20.2; satisfies peer ^5.20.0",
        "release_package_sha256": sha(package_path.read_bytes()),
        "release_yarn_lock_sha256": sha(lock_path.read_bytes()),
        "runtime_yarn_lock_sha256": sha(frozen_lock.encode()),
        "release_tarball_integrity": registry["dist"]["integrity"],
        "release_tarball_shasum": registry["dist"]["shasum"],
        "installation": "Original release transitive lock retained; add only top-level vega-lite release entry. Ignore lifecycle scripts and optional packages; no canvas native installation.",
        "limits": "Modern Node host is not historical author runtime. SVG structural/semantic replay; font/raster geometry and historical author acceptance are not established."
    })
    run_record("install", ["npm", "exec", "--yes", "--package=yarn@1.22.10", "--", "yarn",
                "install", "--frozen-lockfile", "--ignore-scripts", "--ignore-optional",
                "--non-interactive", "--cache-folder", str(SCRATCH / "yarn-cache")], RUNTIME)
    assert sha((RUNTIME / "yarn.lock").read_bytes()) == sha(frozen_lock.encode())
    run_record("versions", ["node", str(BASE / "reproduce.cjs"), "--versions"], BASE)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["setup", "render", "analyze"])
    arg = parser.parse_args()
    if arg.stage == "setup":
        setup()
    elif arg.stage == "render":
        run_record("render", ["node", str(BASE / "reproduce.cjs")], BASE)
    elif arg.stage == "analyze":
        run_record("analyze", [sys.executable, str(BASE / "analyze.py")], BASE)

if __name__ == "__main__":
    main()
