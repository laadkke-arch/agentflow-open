"""Acquire, install and run exact public entries. No predictions are loaded."""
import argparse
import json
import shutil
from pathlib import Path

from cases import cases_for
from common import ROOT, Http, archive, json_in, process, sha, utc, write_json, write_jsonl

REPLAY = ROOT / "replay"
FLAGS = ["--ignore-scripts", "--no-audit", "--no-fund", "--offline"]


class Installer:
    def __init__(self, directory, http, event):
        self.directory = directory
        self.http = http
        self.event = event
        self.cached = set()
        (directory / "artifacts").mkdir(parents=True, exist_ok=True)
        (directory / "installs").mkdir(exist_ok=True)
        self.cache_dir = str(directory / "npm-cache")

    def install_and_run(self, release, selected, queries):
        package, version = release["package"], release["version"]
        work = self.directory / "installs" / f"{package}-{version}"
        work.mkdir(exist_ok=True)
        write_json(work / "package.json", selected["project"])
        write_json(work / "package-lock.json", selected["lock"])
        write_json(work / "cases.json", queries)
        for name in ("probe.cjs", "resolve.mjs"):
            shutil.copyfile(REPLAY / name, work / name)
        record = {"package": package, "version": version, "opened_utc": utc(), "loader": release["loader"],
                  "case_count": len(queries), "lock_sha256": sha((work / "package-lock.json").read_bytes()),
                  "inputs_sha256": sha((work / "cases.json").read_bytes()), "probe_sha256": sha((work / "probe.cjs").read_bytes())}
        if release.get("lock_sha256") and record["lock_sha256"] != release["lock_sha256"]:
            raise ValueError("lock byte drift")
        for location, item in selected["lock"]["packages"].items():
            if not location:
                continue
            url, integrity = item["resolved"], item["integrity"]
            if not url.startswith("https://registry.npmjs.org/"):
                raise ValueError(f"unexpected registry URL {url}")
            if (url, integrity) in self.cached:
                self.event("npm_content_cache_hit", {"url": url, "cache": "npm_content_hit", "bytes": 0})
                continue
            raw, wire = self.http.get(url)
            self.event("http", wire)
            if raw is None:
                return record | {"status": "archive_error", "cases": [], "failed_artifact": wire}
            direct_name = package if location == f"node_modules/{package}" else location.rsplit("node_modules/", 1)[1]
            dist = release["dist"] if direct_name == package else {"integrity": integrity}
            try:
                archive(raw, dist, direct_name, item["version"])
            except (OSError, ValueError, KeyError) as error:
                return record | {"status": "integrity_error", "cases": [], "error": str(error)}
            tar = self.directory / "artifacts" / (sha(raw) + ".tgz")
            tar.write_bytes(raw)
            add = process(["npm", "cache", "add", str(tar), *FLAGS, "--cache", self.cache_dir], work)
            self.event("npm_cache_add", add)
            if add["exit"] != 0:
                return record | {"status": "cache_add_error", "cases": [], "failed_command": add}
            self.cached.add((url, integrity))
        install = process(["npm", "ci", *FLAGS, "--cache", self.cache_dir], work)
        self.event("npm_ci", install)
        if install["exit"] != 0:
            return record | {"status": "install_error", "cases": [], "failed_command": install}
        receipt = process(["node", "probe.cjs", package, release["loader"], "cases.json", "snapshot.json"], work, timeout=12)
        self.event("node_probe", receipt)
        snapshot = work / "snapshot.json"
        if not snapshot.exists():
            return record | {"status": "probe_error", "cases": [], "failed_command": receipt}
        if receipt["exit"] not in (0, 1):
            return record | {"status": "probe_error", "cases": [], "failed_command": receipt}
        result = json_in(snapshot)
        if result["version"] != version or result["lock_sha256"] != record["lock_sha256"]:
            return record | {"status": "identity_mismatch", "cases": [], "mismatch": result}
        if release.get("entry") and result["status"] == "ok" and (
            result["entry"] != release["entry"] or result["entry_sha256"] != release["entry_sha256"]
            or result["direct"] != release["direct"]
        ):
            return record | {"status": "identity_mismatch", "cases": [], "mismatch": result}
        if result["status"] == "ok" and ((len(result["cases"]) != len(queries)) or receipt["exit"] != 0):
            return record | {"status": "case_count_or_exit_mismatch", "cases": []}
        return record | result | {"snapshot_sha256": sha(snapshot.read_bytes()), "probe_exit": receipt["exit"]}


def read_releases():
    return json_in(ROOT / "evidence/release-data.json"), json_in(REPLAY / "locks.json")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--calibration", action="store_true")
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=False)
    releases, locks = read_releases()
    if args.calibration:
        calibration = json_in(REPLAY / "calibration-locks.json")
        releases, locks = calibration["releases"], calibration["locks"]
    rows = []
    for release in releases:
        events = []
        installer = Installer(args.scratch / release["package"], Http(),
                              lambda kind, detail: events.append({"kind": kind} | detail))
        queries = list(cases_for(release["package"], args.calibration))
        record = installer.install_and_run(release, locks[release["package"] + "/" + release["version"]], queries)
        rows.append({"label": args.label, "cohort": "AF139-CAL" if args.calibration else "AF143",
                     "frozen_release_role": release.get("cohort"), "events": events} | record)
    write_jsonl(args.out, rows)


if __name__ == "__main__":
    main()
