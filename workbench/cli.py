"""File-based workbench. Executes only reviewed, manifest-declared tasks.

NOT a sandbox, agent daemon, secret scanner, or proof of source truth.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"[a-z][a-z0-9-]{0,47}\Z")
MAX_FILE = 256_000


def read_json(path):
    if path.stat().st_size > MAX_FILE:
        raise ValueError(f"JSON exceeds {MAX_FILE} bytes: {path.name}")
    return json.loads(path.read_text(encoding="utf-8"))


def contained(root, relative, must_exist=True):
    """Resolve a relative file within root, rejecting symlink/path escapes."""
    if not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative:
        raise ValueError("expected a nonempty POSIX relative path")
    path = Path(relative)
    if path.is_absolute() or any(p in ("..", ".git") for p in path.parts):
        raise ValueError("absolute, parent and .git paths are not allowed")
    target = (root / path).resolve()
    if not target.is_relative_to(root.resolve()) or target == root.resolve():
        raise ValueError("path escapes its declared workspace")
    if must_exist and not target.is_file():
        raise ValueError(f"missing regular file: {relative}")
    return target


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def catalog(root=ROOT):
    root = Path(root).resolve()
    obj = read_json(root / "workbench/catalog.json")
    if obj.get("schema") != 1 or not isinstance(obj.get("projects"), dict):
        raise ValueError("unsupported catalog")
    for name, path in obj["projects"].items():
        if not ID.fullmatch(name):
            raise ValueError("invalid project id")
        contained(root, path + "/project.json")
    return obj["projects"]


def project(name, root=ROOT):
    root = Path(root).resolve()
    entries = catalog(root)
    if name not in entries:
        raise ValueError("unknown project: " + name)
    base = contained(root, entries[name] + "/project.json").parent
    obj = read_json(base / "project.json")
    if obj.get("schema") != 1 or obj.get("id") != name:
        raise ValueError("project identity mismatch")
    for key in ("context", "inputs"):
        if not isinstance(obj.get(key), list) or not obj[key]:
            raise ValueError("project requires " + key)
        for item in obj[key]:
            contained(base, item)
    if "STATE.md" not in obj["context"] or "BRIEF.md" not in obj["context"]:
        raise ValueError("context must include STATE.md and BRIEF.md")
    if not isinstance(obj.get("tasks"), dict) or not obj["tasks"]:
        raise ValueError("project requires tasks")
    for task, spec in obj["tasks"].items():
        if not ID.fullmatch(task) or not isinstance(spec, dict):
            raise ValueError("invalid task")
        args = spec.get("argv")
        if not isinstance(args, list) or not args or args[0] != "{python}":
            raise ValueError("tasks must start with the current Python interpreter")
        if any(not isinstance(a, str) or "\x00" in a for a in args):
            raise ValueError("task argv must be strings without NUL")
        timeout = spec.get("timeout", 30)
        if type(timeout) is not int or not 1 <= timeout <= 120:
            raise ValueError("task timeout must be 1..120 seconds")
    return base, obj


def source_check(path):
    records = read_json(path)
    if not isinstance(records, list) or not records:
        raise ValueError("research sources must be a nonempty list")
    seen = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("source must be an object")
        for key in ("id", "url", "checked_on", "claim", "decision", "reason", "level"):
            if not isinstance(record.get(key), str) or not record[key].strip():
                raise ValueError("source missing " + key)
        if record["id"] in seen:
            raise ValueError("duplicate source id")
        seen.add(record["id"])
        from urllib.parse import urlsplit
        url = urlsplit(record["url"])
        if url.scheme != "https" or not url.hostname or url.username is not None or url.password is not None:
            raise ValueError("source URL must use HTTPS without credentials")
        datetime.strptime(record["checked_on"], "%Y-%m-%d")
        if record["decision"] not in ("adopt", "reference", "defer", "reject"):
            raise ValueError("unknown source decision")
        if record["level"] not in ("official-docs", "upstream-example", "locally-exercised"):
            raise ValueError("unknown evidence level")
    return len(records)


def context(name, query="", budget=12000, root=ROOT):
    root = Path(root).resolve()
    if not 1000 <= budget <= 64000:
        raise ValueError("context budget must be 1000..64000 characters")
    base, obj = project(name, root)
    terms = query.casefold().split()
    files = []
    for relative in obj["context"]:
        path = contained(base, relative)
        if path.stat().st_size > MAX_FILE:
            raise ValueError("context file too large")
        text = path.read_text(encoding="utf-8")
        score = sum(text.casefold().count(term) for term in terms)
        mandatory = relative in ("BRIEF.md", "STATE.md")
        if mandatory or not terms or score:
            files.append((not mandatory, -score, relative, text, path))
    files.sort(key=lambda x: (x[0], x[1], x[2]))
    out = {"schema": 1, "project": name, "query": query,
           "scope": "declared files of this project only; no other project or hidden files",
           "files": [], "omitted": [], "content_characters": 0}
    for _, _, relative, text, path in files:
        if out["content_characters"] + len(text) > budget:
            out["omitted"].append(relative)
            continue
        out["files"].append({"path": path.relative_to(root).as_posix(),
                             "sha256": digest(path), "text": text})
        out["content_characters"] += len(text)
    if any(x not in [Path(f["path"]).name for f in out["files"]] for x in ("BRIEF.md", "STATE.md")):
        raise ValueError("budget cannot include required handover files")
    return out


def tracked_inputs(base, obj, root):
    root = Path(root).resolve()
    base = Path(base).resolve()
    paths = {contained(base, f) for f in obj["inputs"]}
    paths.add(base / "project.json")
    # Explicit shared dependency surface. No recursive private-directory scan.
    for name in ("__init__.py", "__main__.py", "cli.py", "urls.py"):
        paths.add(contained(root, "workbench/" + name))
    return {p.relative_to(root).as_posix(): digest(p) for p in sorted(paths)}


def git_state(root):
    try:
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                             capture_output=True, text=True, timeout=5, check=True).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=root,
                                   capture_output=True, text=True, timeout=5, check=True).stdout.strip())
        return {"commit": sha, "dirty": dirty}
    except (OSError, subprocess.SubprocessError):
        return {"commit": None, "dirty": None}


def run_task(name, task, root=ROOT):
    root = Path(root).resolve()
    base, obj = project(name, root)
    if task not in obj["tasks"]:
        raise ValueError("task is not declared in project.json")
    spec = obj["tasks"][task]
    args = [sys.executable if a == "{python}" else a for a in spec["argv"]]
    inputs = tracked_inputs(base, obj, root)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-") + uuid.uuid4().hex[:12]
    folder = root / ".workbench/runs" / name / run_id
    folder.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    env.update(PYTHONPATH=str(root), PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    source_before = git_state(root)
    started = time.monotonic()
    status, code = "failed", None
    with (folder / "stdout.txt").open("wb") as out, (folder / "stderr.txt").open("wb") as err:
        try:
            proc = subprocess.run(args, cwd=base, stdout=out, stderr=err,
                                  timeout=spec.get("timeout", 30), env=env, check=False)
            code = proc.returncode
            status = "passed" if code == 0 else "failed"
        except subprocess.TimeoutExpired:
            status, code = "timed-out", 124
        except OSError as exc:
            err.write(str(exc).encode("utf-8"))
            status, code = "launch-error", 127
    tracking_error = None
    try:
        changed = inputs != tracked_inputs(base, obj, root)
    except (OSError, ValueError) as exc:
        changed, tracking_error = True, str(exc)
    source_after = git_state(root)
    changed = changed or source_before["commit"] != source_after["commit"]
    if changed:
        status = "inputs-changed"
    receipt = {"schema": 1, "id": run_id, "project": name, "task": task,
               "status": status, "returncode": code, "attempts": 1, "tracking_error": tracking_error,
               "duration_seconds": round(time.monotonic() - started, 3),
               "inputs": inputs, "source": source_before, "python": sys.version.split()[0],
               "workflow_run": os.environ.get("GITHUB_RUN_ID"),
               "stdout_sha256": digest(folder / "stdout.txt"),
               "stderr_sha256": digest(folder / "stderr.txt"),
               "boundary": "trusted repository tasks, not a sandbox or factual certification"}
    (folder / "receipt.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return folder / "receipt.json", receipt


def verify_receipt(path, name, root=ROOT):
    root = Path(root).resolve()
    base, obj = project(name, root)
    path = contained(root, Path(path).resolve().relative_to(root).as_posix())
    data = read_json(path)
    if data.get("schema") != 1 or data.get("project") != name or data.get("task") not in obj["tasks"]:
        raise ValueError("receipt identity mismatch")
    if data.get("status") != "passed" or type(data.get("returncode")) is not int or data["returncode"] != 0:
        raise ValueError("receipt does not describe a successful run")
    if data.get("inputs") != tracked_inputs(base, obj, root):
        raise ValueError("receipt is stale: declared inputs changed")
    for kind in ("stdout", "stderr"):
        log = contained(root, path.with_name(kind + ".txt").relative_to(root).as_posix())
        if not log.is_file() or digest(log) != data.get(kind + "_sha256"):
            raise ValueError("receipt log missing or altered")
    return {"status": "matched", "project": name, "id": data["id"],
            "limitation": "hash consistency, not authenticity or test adequacy"}


def export_project(name, destination, root=ROOT):
    """Export an explicit single-project snapshot, excluding all other projects."""
    root = Path(root).resolve()
    base, obj = project(name, root)
    destination = Path(destination).resolve()
    if destination.exists() or destination.is_relative_to(root.resolve()):
        raise ValueError("export target must be new and outside this workspace")
    relative = base.relative_to(root).as_posix()
    files = {base / "project.json"}
    files.update(contained(base, f) for f in obj["inputs"] + obj["context"])
    for name_ in ("__init__.py", "__main__.py", "cli.py", "urls.py"):
        files.add(contained(root, "workbench/" + name_))
    procedure = root / "docs/procedures/evidence-first.md"
    if procedure.is_file():
        files.add(contained(root, "docs/procedures/evidence-first.md"))
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".workbench-export-", dir=destination.parent))
    try:
        hashes = {}
        for src in sorted(files):
            rel = src.relative_to(root)
            dest = stage / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(src.read_bytes())
            hashes[rel.as_posix()] = digest(src)
        (stage / "workbench/catalog.json").write_text(json.dumps({"schema": 1, "projects": {name: relative}}, indent=2) + "\n", encoding="utf-8")
        (stage / ".gitignore").write_text(".workbench/\n__pycache__/\n*.pyc\n.env\n.env.*\n", encoding="utf-8")
        (stage / "README.md").write_text(f"# {name}\n\nExported single-project snapshot.\n\nRun: `python -m workbench run {name} test`\n\nRead: `python -m workbench context {name}`\n\nNo remote account, credentials, Git history, or other project was copied.\n", encoding="utf-8")
        (stage / "EXPORT.json").write_text(json.dumps({"schema": 1, "project": name, "files": hashes,
                                                       "source": git_state(root)}, indent=2) + "\n", encoding="utf-8")
        stage.rename(destination)
    except BaseException:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return {"project": name, "destination": str(destination), "copied_files": len(hashes)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    sub.add_parser("list")
    ctx = sub.add_parser("context")
    ctx.add_argument("project")
    ctx.add_argument("--query", default="")
    ctx.add_argument("--budget", type=int, default=12000)
    run = sub.add_parser("run")
    run.add_argument("project")
    run.add_argument("task")
    verify = sub.add_parser("verify-receipt")
    verify.add_argument("project")
    verify.add_argument("path")
    exp = sub.add_parser("export")
    exp.add_argument("project")
    exp.add_argument("destination")
    args = parser.parse_args(argv)
    try:
        if args.command == "doctor":
            data = {"python": sys.version.split()[0], "supported": sys.version_info >= (3, 12),
                    "projects": list(catalog()), "git": git_state(ROOT),
                    "network_required": False, "agent_daemon": False}
            for name in data["projects"]:
                project(name)
            if not data["supported"]:
                raise ValueError("Python 3.12+ is required")
        elif args.command == "list":
            data = catalog()
        elif args.command == "context":
            data = context(args.project, args.query, args.budget)
        elif args.command == "run":
            path, data = run_task(args.project, args.task)
            data = {**data, "receipt": path.relative_to(ROOT).as_posix()}
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return 0 if data["status"] == "passed" else 1
        elif args.command == "verify-receipt":
            data = verify_receipt(ROOT / args.path, args.project)
        elif args.command == "export":
            data = export_project(args.project, args.destination)
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("WORKBENCH_ERROR: " + str(exc), file=sys.stderr)
        return 2
