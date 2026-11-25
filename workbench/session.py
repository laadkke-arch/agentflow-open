"""Pin a small task handoff to a reviewed contract and check it before reuse.

No model calls, daemon, installation, merge, push, or private-file scanning.
An explicit --fetch refreshes remote-tracking refs; local refs alone never prove
remote freshness. Hashes detect drift, not source truth or author authenticity.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from workbench.cli import ID, MAX_FILE, ROOT, contained, read_json

CONTRACT = "docs/collaboration/contract.json"
TASK_DIR = "docs/tasks"
INTEGRATION = "chore/workspace-foundation"
SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")


def git(root, *args, check=True):
    result = subprocess.run(["git", *args], cwd=root, capture_output=True,
                            text=True, encoding="utf-8", timeout=60)
    if check and result.returncode:
        # Do not print remote URLs or potentially credential-bearing stderr.
        raise ValueError("Git operation failed: " + args[0])
    return result


def commit(root, ref):
    if not isinstance(ref, str) or not ref or ref.startswith("-"):
        raise ValueError("expected a Git commit/ref")
    return git(root, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}").stdout.strip()


def blob(root, sha, path):
    result = subprocess.run(["git", "show", sha + ":" + path], cwd=root,
                            capture_output=True, timeout=60)
    if result.returncode:
        return None
    if len(result.stdout) > MAX_FILE:
        raise ValueError("Git file is too large: " + path)
    return result.stdout


def branch(root, value):
    if not isinstance(value, str):
        raise ValueError("expected a branch name")
    if value.startswith("refs/heads/"):
        value = value[len("refs/heads/"):]
    if not value or value.startswith("-") or value.startswith("refs/"):
        raise ValueError("expected a branch name, not a URL or remote ref")
    git(root, "check-ref-format", "refs/heads/" + value)
    return value


def remote_name(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", value):
        raise ValueError("expected a configured Git remote name")
    return value


def path_name(root, value, directory=False):
    if not isinstance(value, str) or value.startswith("-"):
        raise ValueError("expected a repository-relative path")
    trailing = value.endswith("/")
    value = value.rstrip("/")
    contained(root, value, must_exist=False)
    if Path(value).as_posix() != value or "." in value.split("/"):
        raise ValueError("path must use canonical POSIX spelling")
    return value + ("/" if directory and trailing else "")


def contract_snapshot(root, ref=None):
    sha = commit(root, ref) if ref else None

    def read(path):
        path_name(root, path)
        if sha:
            content = blob(root, sha, path)
            if content is None:
                raise ValueError("missing contract file at integration ref: " + path)
        else:
            content = contained(root, path).read_bytes()
        if len(content) > MAX_FILE:
            raise ValueError("contract file is too large: " + path)
        return content

    raw = read(CONTRACT)
    data = json.loads(raw)
    if not isinstance(data, dict) or data.get("schema") != 1 or not isinstance(data.get("version"), str) or not data["version"]:
        raise ValueError("unsupported collaboration contract")
    files = data.get("files")
    if not isinstance(files, list) or not 1 <= len(files) <= 30 or len(set(files)) != len(files):
        raise ValueError("contract requires 1..30 unique file paths")
    hashes = {CONTRACT: hashlib.sha256(raw).hexdigest()}
    for path in files:
        hashes[path] = hashlib.sha256(read(path)).hexdigest()
    fingerprint = hashlib.sha256(json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"path": CONTRACT, "version": data["version"], "sha256": fingerprint, "files": hashes}


def refresh(root, integration, dependencies):
    remote = remote_name(integration["remote"])
    branches = {branch(root, integration["branch"])}
    branches.update(branch(root, dep["branch"]) for dep in dependencies)
    specs = ["refs/heads/" + name + ":refs/remotes/" + remote + "/" + name for name in sorted(branches)]
    git(root, "fetch", "--no-tags", "--no-write-fetch-head", remote, *specs)


def reference(root, integration, override):
    return commit(root, override or "refs/remotes/" + integration["remote"] + "/" + integration["branch"])


def dependency_specs(root, values):
    result = []
    for value in values:
        name, separator, sha = value.rpartition("=")
        if not separator or not SHA.fullmatch(sha):
            raise ValueError("dependency must be BRANCH=FULL_COMMIT_SHA")
        name = branch(root, name)
        if any(item["branch"] == name for item in result):
            raise ValueError("duplicate dependency branch")
        result.append({"branch": name, "commit": sha})
    return result


def dependency_errors(root, integration, dependencies):
    errors = []
    for dep in dependencies:
        ref = "refs/remotes/" + integration["remote"] + "/" + dep["branch"]
        actual = commit(root, ref)
        if actual != dep["commit"]:
            errors.append("dependency changed: " + dep["branch"])
    return errors


def start_task(root, task_id, allowed, dependencies=(), *, remote="origin", integration_branch=INTEGRATION,
               fetch=False, integration_ref=None):
    root = Path(root).resolve()
    if not ID.fullmatch(task_id):
        raise ValueError("invalid task id")
    if not allowed:
        raise ValueError("at least one --allow path is required")
    allowed = sorted(set(path_name(root, item, directory=True) for item in allowed))
    integration = {"remote": remote_name(remote), "branch": branch(root, integration_branch)}
    dependencies = dependency_specs(root, dependencies)
    if fetch and integration_ref:
        raise ValueError("--fetch and --integration-ref cannot be combined")
    if fetch:
        refresh(root, integration, dependencies)
    baseline = reference(root, integration, integration_ref)
    snapshot = contract_snapshot(root, baseline)
    if contract_snapshot(root) != snapshot:
        raise ValueError("working contract differs from integration; read and reconcile the current contract first")
    errors = dependency_errors(root, integration, dependencies)
    if errors:
        raise ValueError("; ".join(errors))
    return {"schema": 1, "task_id": task_id, "status": "active", "base_commit": commit(root, "HEAD"),
            "integration": {**integration, "commit": baseline}, "contract": snapshot,
            "allowed_paths": allowed, "dependencies": dependencies,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "freshness_at_start": "remote_checked" if fetch else "local_only"}


def load_task(root, path):
    path = contained(root, path)
    data = read_json(path)
    if not isinstance(data, dict) or data.get("schema") != 1 or not isinstance(data.get("task_id"), str) or not ID.fullmatch(data["task_id"]):
        raise ValueError("unsupported task manifest")
    if data.get("status") not in ("active", "closed") or not SHA.fullmatch(data.get("base_commit", "")):
        raise ValueError("invalid task status or base commit")
    integration = data.get("integration", {})
    remote_name(integration.get("remote"))
    branch(root, integration.get("branch", ""))
    if not SHA.fullmatch(integration.get("commit", "")):
        raise ValueError("integration commit must be a full SHA")
    pinned = data.get("contract", {})
    if pinned.get("path") != CONTRACT or not re.fullmatch(r"[0-9a-f]{64}", pinned.get("sha256", "")):
        raise ValueError("invalid pinned contract")
    allowed = data.get("allowed_paths")
    if not isinstance(allowed, list) or not allowed:
        raise ValueError("task requires allowed paths")
    for item in allowed:
        path_name(root, item, directory=True)
    dependencies = data.get("dependencies")
    if not isinstance(dependencies, list):
        raise ValueError("task dependencies must be a list")
    dependency_specs(root, [item["branch"] + "=" + item["commit"] for item in dependencies])
    return data, path.relative_to(root).as_posix()


def changed_paths(root, baseline):
    paths = set()
    for args in (("diff", "--name-only", "-z", "--no-renames", baseline, "HEAD", "--"),
                 ("diff", "--name-only", "-z", "--no-renames", "HEAD", "--"),
                 ("ls-files", "--others", "--exclude-standard", "-z")):
        paths.update(item for item in git(root, *args).stdout.split("\0") if item)
    return sorted(paths)


def check_task(root, manifest_path, *, fetch=False, integration_ref=None):
    root = Path(root).resolve()
    task, manifest_path = load_task(root, manifest_path)
    if fetch and integration_ref:
        raise ValueError("--fetch and --integration-ref cannot be combined")
    if fetch:
        refresh(root, task["integration"], task["dependencies"])
    baseline = reference(root, task["integration"], integration_ref)
    head = commit(root, "HEAD")
    errors = []
    if integration_ref and baseline == head and head != task["integration"]["commit"]:
        raise ValueError("cannot check changed task against itself; use the integration branch or its base SHA")
    if git(root, "merge-base", "--is-ancestor", task["base_commit"], head, check=False).returncode:
        errors.append("task base is not an ancestor of this checkout")
    unmerged = [item for item in git(root, "diff", "--name-only", "--diff-filter=U", "-z").stdout.split("\0") if item]
    if unmerged:
        errors.append("unresolved Git merge conflicts")
    current = contract_snapshot(root, baseline)
    if current != task["contract"]:
        errors.append("integration contract changed; review it and create a new task pin")
    if contract_snapshot(root) != task["contract"]:
        errors.append("working contract differs from task pin")
    errors.extend(dependency_errors(root, task["integration"], task["dependencies"]))
    scope_base = git(root, "merge-base", baseline, head).stdout.strip()
    changes = [item for item in changed_paths(root, scope_base) if item != manifest_path]
    outside = [item for item in changes if not any(
        item.startswith(rule) if rule.endswith("/") else item == rule for rule in task["allowed_paths"])]
    if outside:
        errors.append("changes outside task ownership")
    return {"status": "failed" if errors else "passed", "task_id": task["task_id"],
            "freshness": "remote_checked" if fetch else "local_only",
            "checked_at": datetime.now(timezone.utc).isoformat(), "checked_out_commit": head,
            "task_base_commit": task["base_commit"], "integration_commit": baseline,
            "scope_base_commit": scope_base, "contract_sha256": current["sha256"],
            "changed_paths": changes, "outside_paths": outside, "unmerged_paths": unmerged, "errors": errors,
            "boundary": "Git contract and ownership checks; not a new AI chat or product verification"}


def check_all(root, *, fetch=False, integration_ref=None):
    root = Path(root).resolve()
    # Even an empty queue must have a readable contract and referenced files.
    snapshot = contract_snapshot(root)
    paths = []
    directory = root / TASK_DIR
    if directory.is_dir():
        for path in sorted(directory.glob("*.json")):
            name = path.relative_to(root).as_posix()
            task, _ = load_task(root, name)
            if task["status"] == "active":
                paths.append(name)
    if not paths:
        return {"status": "not-executed", "reason": "no_active_sessions", "count": 0,
                "freshness": "not_checked", "contract_sha256": snapshot["sha256"]}
    if fetch and integration_ref:
        raise ValueError("--fetch and --integration-ref cannot be combined")
    results, integrated, integrated_baselines = [], [], set()
    for name in paths:
        task, _ = load_task(root, name)
        if fetch:
            refresh(root, task["integration"], task["dependencies"])
        baseline = reference(root, task["integration"], integration_ref)
        if integration_ref and baseline == commit(root, "HEAD") and baseline != task["integration"]["commit"]:
            raise ValueError("cannot check changed task against itself; use the integration branch or its base SHA")
        recorded = blob(root, baseline, name)
        if recorded is not None and recorded == contained(root, name).read_bytes():
            # A previously accepted task must not claim ownership of a later PR.
            integrated.append(task["task_id"])
            integrated_baselines.add(baseline)
            continue
        result = check_task(root, name, integration_ref=integration_ref)
        result["freshness"] = "remote_checked" if fetch else "local_only"
        results.append(result)
    if not results:
        # Reusing an accepted manifest must not hide new work. With no new task
        # to check, any changes since an integration baseline need a new pin.
        head = commit(root, "HEAD")
        changes = set()
        for baseline in integrated_baselines:
            scope_base = git(root, "merge-base", baseline, head).stdout.strip()
            changes.update(changed_paths(root, scope_base))
        if changes:
            return {"status": "failed", "reason": "new_task_pin_required", "count": 0,
                    "freshness": "remote_checked" if fetch else "local_only",
                    "integrated_tasks": integrated, "changed_paths": sorted(changes),
                    "errors": ["new changes have no unintegrated active task; create a new task pin"]}
        return {"status": "not-executed", "reason": "already_integrated", "count": 0,
                "freshness": "remote_checked" if fetch else "local_only", "integrated_tasks": integrated}
    return {"status": "passed" if all(item["status"] == "passed" for item in results) else "failed",
            "count": len(results), "freshness": "remote_checked" if fetch else "local_only",
            "integrated_tasks": integrated, "tasks": results}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    start = commands.add_parser("start")
    start.add_argument("task_id")
    start.add_argument("--allow", action="append", required=True)
    start.add_argument("--dependency", action="append", default=[])
    start.add_argument("--remote", default="origin")
    start.add_argument("--integration-branch", default=INTEGRATION)
    start.add_argument("--output", help="New repository-relative JSON file; omit to print only")
    check = commands.add_parser("check")
    check.add_argument("manifest")
    all_tasks = commands.add_parser("check-all")
    for command in (start, check, all_tasks):
        options = command.add_mutually_exclusive_group()
        options.add_argument("--fetch", action="store_true")
        options.add_argument("--integration-ref", help="Explicit local baseline; never proves remote freshness")
    args = parser.parse_args(argv)
    try:
        if args.command == "start":
            result = start_task(ROOT, args.task_id, args.allow, args.dependency, remote=args.remote,
                                integration_branch=args.integration_branch, fetch=args.fetch,
                                integration_ref=args.integration_ref)
            if args.output:
                target = contained(ROOT, args.output, must_exist=False)
                if target.suffix != ".json":
                    raise ValueError("manifest output must be a JSON file")
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("x", encoding="utf-8") as stream:
                    stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        elif args.command == "check":
            result = check_task(ROOT, args.manifest, fetch=args.fetch, integration_ref=args.integration_ref)
        else:
            result = check_all(ROOT, fetch=args.fetch, integration_ref=args.integration_ref)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get("status") == "failed" else 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
