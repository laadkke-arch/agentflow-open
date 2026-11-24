"""Measure local archive and signal processing work without changing the policy seal."""
import argparse
import json
import resource
import subprocess
import time
from collections import defaultdict
from pathlib import Path

from common import Fetcher, ROOT, archive, json_in, sha, utc, write_json
from predict import notice


def measured(operation, combined=False):
    start_wall = time.perf_counter_ns()
    start_cpu = time.process_time_ns()
    child = resource.getrusage(resource.RUSAGE_CHILDREN)
    operation()
    cpu = (time.process_time_ns() - start_cpu) / 1_000_000
    if combined:
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        cpu += (after.ru_utime + after.ru_stime - child.ru_utime - child.ru_stime) * 1000
    return {"wall_ms": (time.perf_counter_ns() - start_wall) / 1_000_000, "cpu_ms": cpu}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("cache", "text-root", "parser"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    pop = json_in(ROOT / "evidence/roster.json")
    versions = {r["version"]: r for r in pop["catalog"] if r["status"] == "included"}
    details = defaultdict(list)
    with (ROOT / "evidence/signal-components.jsonl").open() as rows:
        for line in rows:
            row = json.loads(line)
            details[row["version"]].append(row)
    fetcher = Fetcher(args.cache)
    all_profiles = {}
    for version in pop["published_order"]:
        meta = versions[version]
        records = details[version]
        text = args.text_root / version / "package-text"
        raw, initial_receipt = fetcher.get(meta["tarball_url"])
        files, _, _ = archive(raw, meta, version)
        d_files = {item["path"] for row in records for item in row["broad_files"]}
        argv = ["node", str(ROOT / "replay/fingerprint.cjs"), str(text.resolve()), records[0]["entry"], str(args.parser.resolve())]
        computed = []

        def narrow():
            result = subprocess.run(argv, capture_output=True, timeout=15, check=True)
            computed.append(json.loads(result.stdout))

        profile = {
            "utc": utc(),
            "archive_local_verify_and_unpack": measured(lambda: archive(raw, meta, version)),
            "D_raw_hash": measured(lambda: [sha((text / path).read_bytes()) for path in sorted(d_files)]),
            "F_ast": measured(narrow, combined=True),
            "N_changelog": measured(lambda: notice(files, version, meta["publish_utc"], {}, True, "v" + version, meta["tarball_url"])),
            "initial_archive_observed_fetch_wall_ms": initial_receipt["wall_ms"],
        }
        assert all(computed[0][row["function"]] == row["function_body"] for row in records)
        all_profiles[version] = profile
    write_json(ROOT / "evidence/static-profiles.json", {
        "conditions": "One sequential replay on original staged package text and verified local tar bytes. F forks Node, three other operations use this Python process. C timings refer to original Git file reads. No historical latency asserted.",
        "versions": all_profiles,
    })


if __name__ == "__main__":
    main()
