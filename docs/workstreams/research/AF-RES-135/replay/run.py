"""Install exact npm archives in fresh directories and probe their public entry points."""
import argparse
import concurrent.futures
import csv
import functools
import json
import os
import pathlib
import shutil
import subprocess

from artifacts import Fetcher, OL_PREFIX, PRE, ROOT, archive, git, sha, utc, write_csv, write_json, write_jsonl


@functools.lru_cache(maxsize=None)
def unpack(cache, name, version, url, integrity, shasum):
    files, manifest, receipt = archive(cache, {"tarball": url, "integrity": integrity, "shasum": shasum}, version)
    if manifest["name"] != name:
        raise ValueError(f"unexpected package name for {url}")
    return files, receipt


def install(cache, lock, folder):
    package_hashes = []
    for relative, pkg in lock["packages"].items():
        dist = pkg["dist"]
        files, info = unpack(cache, pkg["name"], pkg["version"], dist["tarball"], dist.get("integrity", ""),
                             dist.get("shasum", ""))
        target = folder / relative
        if not target.resolve().is_relative_to(folder):
            raise ValueError(f"path escapes installation: {relative}")
        for name, raw in files.items():
            output = target / name
            if not output.resolve().is_relative_to(target):
                raise ValueError(f"path escapes package: {name}")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(raw)
        package_hashes.append({"path": relative, "name": pkg["name"], "version": pkg["version"],
                               "tar_sha256": info["sha256"], "npm_integrity": dist.get("integrity", ""),
                               "npm_sha1": dist.get("shasum", ""), "tar_bytes": info["bytes"]})
    return package_hashes


def execute(lock, key, strategy, pair, folder, cache, inputs):
    path = folder / key
    path.mkdir()
    record = {"product": "d3-scale", "id": key, "strategy": strategy, "pair": pair, "version": lock["version"],
              "decision_cutoff_utc": lock["cutoff"], "publish_utc": lock.get("packages", {}).get("node_modules/d3-scale", {}).get("utc"),
              "input": inputs, "install_utc": utc()}
    try:
        if "error" in lock:
            raise ValueError(lock["error"])
        record["installed"] = install(cache, lock, path)
        record["direct_lock"] = lock["direct"]
    except (OSError, ValueError, KeyError) as failure:
        return record | {"status": "install_failed", "failure": str(failure), "completed_utc": utc()}
    shutil.copyfile(ROOT / "replay/probe.mjs", path / "probe.mjs")
    write_json(path / "case.json", {"inputs": inputs})
    env = {k: v for k, v in os.environ.items() if k not in {"NODE_PATH", "NODE_OPTIONS"}}
    p = subprocess.run(["node", "probe.mjs"], cwd=path, env=env, capture_output=True, text=True, timeout=30)
    record.update(exit=p.returncode, stderr=p.stderr)
    if p.returncode or not p.stdout.strip():
        return record | {"status": "process_failed", "stdout": p.stdout, "completed_utc": utc()}
    data = json.loads(p.stdout)
    if data["status"] == "observed":
        if data["node"] != inputs["node"]:
            raise ValueError(f"unexpected Node runtime: {data['node']}")
        if data["package_version"] != record["version"]:
            raise ValueError(f"unexpected root package: {data['package_version']}")
        if {n: d["version"] for n, d in data["direct"].items()} != lock["direct"]:
            raise ValueError(f"unexpected dependency versions in {key}")
    return record | data


def run(folder, cache, output):
    if folder.exists():
        raise SystemExit("Provide a new empty path for each replay.")
    folder.mkdir(parents=True)
    folder = folder.resolve()
    fetcher = Fetcher(cache)
    inputs = json.loads((ROOT / "replay/inputs.json").read_text())
    lock_path = ROOT / "replay/locks.json"
    locks = json.loads(lock_path.read_text())
    cases = [(lock, f"base-{v}", "publish-vintage", None) for v, lock in locks["base"].items()]
    for key, pair in locks["matched"].items():
        for index, lock in enumerate(pair.get("locks", [])):
            cases.append((lock, f"matched-{key}-{index + 1}", "matched-direct", key))
    # Preload verified archives once per path; application code is run only in the case folders.
    distinct = {}
    for lock, *_ in cases:
        for pkg in lock.get("packages", {}).values():
            distinct[(pkg["name"], pkg["version"])] = pkg
    preload_issues = []
    for package in distinct.values():
        dist = package["dist"]
        try:
            unpack(fetcher, package["name"], package["version"], dist["tarball"], dist.get("integrity", ""),
                   dist.get("shasum", ""))
        except (OSError, ValueError, KeyError) as failure:
            preload_issues.append(str(failure))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(lambda case: execute(*case, folder, fetcher, inputs), cases))
    write_jsonl(output, rows)
    receipt = {"folder": str(folder), "http_cache": str(cache), "lock_sha256": sha(lock_path.read_bytes()),
               "output_sha256": sha(output.read_bytes()), "unique_archives": len(distinct),
               "preload_issues": preload_issues, "planned": len(cases),
               "observed": sum(row["status"] == "observed" for row in rows), "replay_file": output.name,
               "node_version": subprocess.check_output(["node", "--version"], text=True).strip(),
               "npm_version": subprocess.check_output(["npm", "--version"], text=True).strip(), "finished_utc": utc()}
    write_json(output.with_suffix(".receipt.json"), receipt)
    print(json.dumps(receipt, ensure_ascii=False))


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def equality_value(cell):
    return {k: v for k, v in cell.items() if k != "message"}


def pair_outputs(left, right, inputs):
    if any(not x or x["status"] != "observed" for x in (left, right)):
        return {test: "unconfirmed" for test in inputs["checks"]}
    return {test: "same" if equality_value(left["outputs"][test]) == equality_value(right["outputs"][test]) else "changed"
            for test in inputs["checks"]}


def combine(first, second):
    a, b = read_jsonl(first), read_jsonl(second)
    assert [r["id"] for r in a] == [r["id"] for r in b]
    basis = ("status", "node", "mode", "version", "entry", "entry_sha256", "direct", "installed", "outputs")
    mismatches = [x["id"] for x, y in zip(a, b) if any(x.get(field) != y.get(field) for field in basis)]
    inputs = json.loads((ROOT / "replay/inputs.json").read_text())
    roster = json.loads((ROOT / "evidence/roster.json").read_text())
    base = {x["version"]: x for x in a if x["strategy"] == "publish-vintage"}
    second_by_id = {x["id"]: x for x in b}
    first_by_id = {x["id"]: x for x in a}
    pairs = []
    for ordering, versions in (("publish", [r["version"] for r in roster["publish"]]), ("semver", roster["semver"])):
        for left, right in zip(versions, versions[1:]):
            name = f"{left}..{right}"
            for strategy, x, y in (("publish-vintage", base[left], base[right]),
                                   ("matched-direct", first_by_id.get(f"matched-{name}-1"),
                                    first_by_id.get(f"matched-{name}-2"))):
                cells = pair_outputs(x, y, inputs)
                state = "changed" if "changed" in cells.values() else "unconfirmed" if "unconfirmed" in cells.values() else "same"
                pairs.append({"order": ordering, "strategy": strategy, "before": left, "after": right, "state": state,
                              "left_run": x["id"] if x else "", "right_run": y["id"] if y else "", **cells})
    write_csv(ROOT / "evidence/output-comparison.csv", pairs)
    focused = []
    prior = {x["run_id"]: x for x in csv.DictReader(git("show", OL_PREFIX + "predictions.csv").decode().splitlines())}
    for line in git("show", OL_PREFIX + "runs.jsonl").decode().splitlines():
        x = json.loads(line)
        if x["mode"] != "main" or x["cell"] not in {"02", "03", "04", "05"}:
            continue
        raw = git("show", OL_PREFIX + x["raw_log"])
        x["product"] = "ol"
        x["strategy"] = "inherited_browser"
        x["predecessor_claim"] = prior[x["id"]]["rationale"]
        x["raw_sha256"] = sha(raw)
        x["raw_log"] = f"https://github.com/laadkke-arch/agentflow-open/blob/{PRE}/docs/workstreams/research/AF-RES-131/{x['raw_log']}"
        # The predecessor's raw browser file was opened and both trace and its hashed reference are retained.
        assert isinstance(json.loads(raw), dict)
        focused.append(x)
    write_jsonl(ROOT / "runs.jsonl", [dict(r, route="A") for r in a] + [dict(r, route="B") for r in b] + focused)
    maps = sorted({x["version"] for x in focused})
    assert len(second_by_id) == len(a)
    receipt = {"route_A": json.loads(first.with_suffix(".receipt.json").read_text()),
               "route_B": json.loads(second.with_suffix(".receipt.json").read_text()),
               "replay_rows_compared": len(a), "different_rows": mismatches, "inherited_browser_rows": len(focused),
               "inherited_browser_versions": maps, "output_cells_per_vector": len(inputs["checks"])}
    write_json(ROOT / "evidence/replay.json", receipt)
    print(json.dumps(receipt, ensure_ascii=False))
    if mismatches:
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    measure = commands.add_parser("run")
    for key in ("folder", "cache", "output"):
        measure.add_argument(f"--{key}", type=pathlib.Path, required=True)
    merge = commands.add_parser("combine")
    for key in ("first", "second"):
        merge.add_argument(f"--{key}", type=pathlib.Path, required=True)
    args = parser.parse_args()
    if args.command == "run":
        run(args.folder, args.cache, args.output)
    else:
        combine(args.first, args.second)


if __name__ == "__main__":
    main()
