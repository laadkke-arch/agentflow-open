"""Freeze chronological npm membership without reading package implementation or expected output."""
import argparse
import re
from pathlib import Path

from common import Http, json_in, sha, write_json

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = {
    "simple-statistics": {"anchor": "7.8.1", "after": 16, "repo": "simple-statistics/simple-statistics", "tag": "v"},
    "d3-array": {"start": "2020-01-01", "take": 16, "repo": "d3/d3-array", "tag": "v"},
}
END = "2026-01-01"


def roster(package, config, data, receipt):
    times, versions = data["time"], data["versions"]
    start = times[config["anchor"]] if "anchor" in config else config["start"]
    limit = config.get("take", config.get("after", 0) + int("anchor" in config))
    rows, exceptions = [], []
    for version in sorted(set(times) | set(versions)):
        if not re.match(r"^\d+\.\d+\.\d+", version):
            continue
        published = times.get(version)
        if not published:
            exceptions.append({"version": version, "state": "missing_time"})
        elif published >= start and published < END:
            if not re.fullmatch(r"\d+\.\d+\.\d+", version):
                exceptions.append({"version": version, "published": published, "state": "prerelease_or_nonregular"})
            elif version not in versions:
                exceptions.append({"version": version, "published": published, "state": "time_only_no_distribution"})
            else:
                item = versions[version]
                rows.append({"version": version, "published": published, "dist": {
                    key: item["dist"].get(key) for key in ("tarball", "integrity", "shasum")
                }, "git_head": item.get("gitHead"), "deprecated_now": item.get("deprecated")})
    semver = lambda row: tuple(map(int, row["version"].split(".")))
    rows.sort(key=lambda row: (row["published"], semver(row)))
    selected = rows[:limit]
    for rank, row in enumerate(sorted(selected, key=semver), 1):
        row["semver_rank"] = rank
    for rank, row in enumerate(selected, 1):
        row["publish_rank"] = rank
        row["cohort"] = "baseline" if row["version"] == config.get("anchor") else "new"
    ties = [time for time in sorted({row["published"] for row in rows})
            if sum(row["published"] == time for row in rows) > 1]
    return {"package": package, "repo": config["repo"], "tag_prefix": config["tag"], "start": start,
            "end_exclusive": END, "archive_date_ties": ties, "packument": receipt, "selected": selected,
            "later_regular": [{"version": r["version"], "published": r["published"]} for r in rows[limit:]],
            "exceptions": exceptions}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--packuments", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    cohorts = []
    for package, config in PACKAGES.items():
        url = f"https://registry.npmjs.org/{package}"
        if args.packuments:
            path = args.packuments / f"{package}-packument.json"
            receipt = json_in(args.packuments / "packument-receipts.json")[package]
            raw = path.read_bytes()
        else:
            raw, receipt = Http().get(url)
        if raw is None or receipt.get("status") != 200:
            raise RuntimeError(f"packument unavailable: {receipt}")
        import json
        cohorts.append(roster(package, config, json.loads(raw), receipt | {"sha256": sha(raw), "bytes": len(raw)}))
    write_json(args.out, {"rule": "publication UTC, numeric SemVer tiebreak, current registry metadata", "cohorts": cohorts})


if __name__ == "__main__":
    main()
