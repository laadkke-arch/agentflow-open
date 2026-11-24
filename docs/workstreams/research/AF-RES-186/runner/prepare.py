#!/usr/bin/env python3
"""Verify the three checkouts and build each engine's invocation independently."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

RUNNER = Path(__file__).resolve().parent
INPUTS = RUNNER.parent / "inputs.json"


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def written_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def trace(log_dir, name, argv, cwd, extra_env=None):
    env = dict(os.environ)
    for key in ("NODE_OPTIONS", "NODE_PATH", "GOFLAGS"):
        env.pop(key, None)
    changes = {"TZ": "UTC", "LC_ALL": "C.UTF-8", **(extra_env or {})}
    env.update(changes)
    command = list(map(str, argv))
    try:
        done = subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=240, check=False)
        stdout, stderr, status = done.stdout, done.stderr, done.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, stderr, status = exc.stdout or b"", (exc.stderr or b"") + b"\nTimed out.\n", 124
    except OSError as exc:
        stdout, stderr, status = b"", (str(exc) + "\n").encode(), 127
    receipt = {"argv": command, "cwd": str(cwd), "environment_overrides": changes, "exit_code": status}
    for stream, content in (("stdout", stdout), ("stderr", stderr)):
        p = log_dir / f"{name}.{stream}.log"
        p.write_bytes(content)
        receipt[stream] = {"path": p.name, "bytes": len(content), "sha256": hash_file(p)}
    written_json(log_dir / f"{name}.json", receipt)
    if status:
        raise RuntimeError(f"{name} exited {status}; see {name}.json")
    return stdout.decode().strip()


def verify_checkout(role, root, pin, log_dir):
    revision = trace(log_dir, f"{role}-revision", ["git", "rev-parse", "HEAD", "HEAD^{tree}"], root).splitlines()
    tracked_changes = trace(log_dir, f"{role}-tracked-status", ["git", "status", "--porcelain", "--untracked-files=no"], root)
    if revision != [pin["commit"], pin["tree"]] or tracked_changes:
        raise RuntimeError(f"{role}: wrong revision, tree or tracked file changes")
    return {"checkout": str(root), "commit": revision[0], "tree": revision[1]}


def gold_setup(root, path, scratch, logs, env):
    go = Path(shutil.which(path) or path).resolve()
    actual_go = trace(logs, "gold-runtime", [go, "version"], root)
    if actual_go != env["go"]:
        raise RuntimeError(f"Gold: expected {env['go']}, got {actual_go}")
    go_env = {
        "GOTOOLCHAIN": "local", "GOPROXY": "https://proxy.golang.org",
        "GOSUMDB": "sum.golang.org", "GOWORK": "off", "GOENV": "off",
        "CGO_ENABLED": "0", "GOPATH": str(scratch / "gopath"),
        "GOMODCACHE": str(scratch / "go-mod"), "GOCACHE": str(scratch / "go-cache"),
    }
    runtime_module = "github.com/pquerna/cachecontrol@v0.0.0-20180517163645-1555304b9b35"
    resolved = json.loads(trace(logs, "gold-download", [go, "mod", "download", "-json", runtime_module], root, go_env))
    trace(logs, "gold-module-verify", [go, "mod", "verify"], root, go_env)
    binary = scratch / "json-gold-driver"
    trace(logs, "gold-build", [go, "build", "-mod=readonly", "-trimpath", "-buildvcs=false",
                              "-o", binary, RUNNER / "gold.go"], root, go_env)
    build = trace(logs, "gold-build-info", [go, "version", "-m", binary], root, go_env)
    if resolved["Sum"] not in build or "github.com/piprate/json-gold" not in build:
        raise RuntimeError("Gold: build info does not match the resolved module")
    return {
        "runtime": actual_go,
        "runtime_path": str(go),
        "runtime_sha256": hash_file(go),
        "module_declaration_sha256": hash_file(root / "go.mod"),
        "module_lock_sha256": hash_file(root / "go.sum"),
        "resolved_linked_modules": [{k: resolved[k] for k in ("Path", "Version", "Sum", "GoModSum")}],
        "adapter_sha256": hash_file(RUNNER / "gold.go"),
        "binary_sha256": hash_file(binary),
        "argv": [str(binary)],
        "environment_overrides": {},
    }


def js_setup(root, node_path, npm_path, scratch, logs, env):
    node = Path(shutil.which(node_path) or node_path).resolve()
    npm = shutil.which(npm_path) or npm_path
    actual_node = trace(logs, "js-runtime", [node, "--version"], root)
    actual_npm = trace(logs, "js-npm", [npm, "--version"], root)
    if (actual_node, actual_npm) != (env["node"], env["npm"]):
        raise RuntimeError(f"JS: expected {env['node']}/{env['npm']}, got {actual_node}/{actual_npm}")
    upstream = json.loads((root / "package.json").read_bytes())
    isolated = scratch / "js-runtime-deps"
    isolated.mkdir(exist_ok=True)
    for name in ("package.json", "package-lock.json"):
        shutil.copyfile(RUNNER / "js-deps" / name, isolated / name)
    declaration = json.loads((isolated / "package.json").read_bytes())
    lock = json.loads((isolated / "package-lock.json").read_bytes())
    if upstream["dependencies"] != declaration["dependencies"] or lock["packages"][""]["dependencies"] != declaration["dependencies"]:
        raise RuntimeError("JS: runtime-only npm manifest/lock diverged from pinned source declaration")
    if (root / "node_modules").exists():
        raise RuntimeError("JS: checkout has its own node_modules; clean checkout required")
    trace(logs, "js-ci", [node, Path(npm).resolve(), "--prefix", isolated, "ci", "--omit=dev",
                         "--ignore-scripts", "--no-audit", "--no-fund",
                         "--registry=https://registry.npmjs.org", f"--cache={scratch / 'npm-cache'}"], root)
    trace(logs, "js-installed-tree", [node, Path(npm).resolve(), "--prefix", isolated, "ls",
                                     "--all", "--omit=dev", "--json"], root)
    dependencies = []
    for relative, entry in lock["packages"].items():
        if not relative:
            continue
        installed = isolated / relative / "package.json"
        if not installed.exists() and entry.get("optional"):
            continue
        version = json.loads(installed.read_bytes())["version"]
        if version != entry["version"] or not entry.get("integrity"):
            raise RuntimeError(f"JS: wrong installed version or integrity for {relative}")
        dependencies.append({"path": relative, "version": version})
    js_env = {"NODE_PATH": str(isolated / "node_modules")}
    entrypoint = trace(logs, "js-entrypoint", [node, "-p", "require.resolve(process.argv[1])", root], root, js_env)
    if Path(entrypoint) != root / upstream["main"]:
        raise RuntimeError("JS: wrong installed source entrypoint")
    trace(logs, "js-components", [node, "-p", "JSON.stringify(process.versions)"], root)
    return {
        "runtime": actual_node,
        "runtime_path": str(node),
        "runtime_sha256": hash_file(node),
        "npm_version": actual_npm,
        "package_version": upstream["version"],
        "package_declaration_sha256": hash_file(root / "package.json"),
        "npm_lock_sha256": hash_file(isolated / "package-lock.json"),
        "runtime_manifest_sha256": hash_file(isolated / "package.json"),
        "entrypoint": entrypoint,
        "entrypoint_sha256": hash_file(Path(entrypoint)),
        "algorithm_sha256": hash_file(root / "lib/jsonld.js"),
        "installed_package_count": len(dependencies),
        "direct_dependencies": {
            name: next(dep["version"] for dep in dependencies if dep["path"] == f"node_modules/{name}")
            for name in upstream["dependencies"]
        },
        "adapter_sha256": hash_file(RUNNER / "js.cjs"),
        "argv": [str(node), str(RUNNER / "js.cjs"), str(root)],
        "environment_overrides": js_env,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for item in ("suite", "gold", "js", "scratch", "logs"):
        parser.add_argument("--" + item, required=True, type=lambda p: Path(p).resolve())
    parser.add_argument("--go", default="go")
    parser.add_argument("--node", default="node")
    parser.add_argument("--npm", default="npm")
    args = parser.parse_args()
    plan = json.loads(INPUTS.read_bytes())
    args.scratch.mkdir(parents=True, exist_ok=True)
    args.logs.mkdir(parents=True, exist_ok=True)
    results = {}
    for role in ("suite", "gold", "js"):
        try:
            root = getattr(args, role)
            result = verify_checkout(role, root, plan["upstream"][role], args.logs)
            if role == "gold":
                result.update(gold_setup(root, args.go, args.scratch, args.logs, plan["environment"]))
            if role == "js":
                result.update(js_setup(root, args.node, args.npm, args.scratch, args.logs, plan["environment"]))
        except (ValueError, RuntimeError, OSError) as exc:
            results[role] = {"ready": False, "reason": str(exc)}
        else:
            results[role] = {"ready": True, **result}
    written_json(args.logs / "runtime.json", results)
    print(json.dumps({role: value["ready"] for role, value in results.items()}))
    return 0 if all(value["ready"] for value in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
