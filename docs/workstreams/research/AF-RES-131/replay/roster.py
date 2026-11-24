"""Enumerate the public npm packument at an explicit UTC cutoff."""

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

PACKUMENT = "https://registry.npmjs.org/ol"
LOW = (6, 0, 0)
HIGH = (10, 11, 0)
COLUMNS = [
    "semver_rank", "publish_rank", "version", "channel", "publish_utc",
    "npm_git_head", "tarball_url", "tarball_integrity", "tarball_npm_sha1",
    "deprecated", "stable_from_packument",
]


def enumerate_releases(packument, cutoff):
    rows = []
    for version, metadata in packument["versions"].items():
        match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:-([\w.-]+))?", version)
        if not match:
            continue
        version_core = tuple(map(int, match.groups()[:3]))
        if not LOW <= version_core <= HIGH:
            continue
        published = packument["time"][version]
        if datetime.fromisoformat(published) > cutoff:
            continue
        dist = metadata["dist"]
        rows.append({
            "version": version,
            "channel": "prerelease" if match[4] else "stable",
            "publish_utc": published,
            "npm_git_head": metadata.get("gitHead", ""),
            "tarball_url": dist["tarball"],
            "tarball_integrity": dist.get("integrity", ""),
            "tarball_npm_sha1": dist.get("shasum", ""),
            "deprecated": metadata.get("deprecated", ""),
            "stable_from_packument": not match[4],
            "_core": version_core,
        })
    stable = sorted((r for r in rows if r["stable_from_packument"]), key=lambda r: r["_core"])
    for rank, row in enumerate(stable, 1):
        row["semver_rank"] = rank
    for rank, row in enumerate(sorted(stable, key=lambda r: (r["publish_utc"], r["_core"])), 1):
        row["publish_rank"] = rank
    prerelease = sorted((r for r in rows if not r["stable_from_packument"]),
                        key=lambda r: (r["_core"], r["publish_utc"], r["version"]))
    return stable, prerelease


def write_csv(path, rows, columns=COLUMNS):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packument", type=Path)
    parser.add_argument("--cutoff", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prereleases", type=Path, required=True)
    args = parser.parse_args()
    cutoff = datetime.fromisoformat(args.cutoff)
    if cutoff.utcoffset() is None:
        parser.error("--cutoff requires a timezone")
    raw = args.packument.read_bytes()
    stable, prerelease = enumerate_releases(json.loads(raw), cutoff)
    write_csv(args.output, stable)
    write_csv(args.prereleases, prerelease, ["version", "publish_utc", "npm_git_head"])
    print(json.dumps({
        "source": PACKUMENT, "cutoff_utc": cutoff.isoformat(),
        "bytes": len(raw), "packument_sha256": hashlib.sha256(raw).hexdigest(),
        "stable": len(stable), "prerelease_core_in_range": len(prerelease),
        "prerelease_kinds": dict(Counter(row["version"].split("-", 1)[1].split(".")[0]
                                         for row in prerelease)),
        "first_stable": stable[0]["version"], "last_stable": stable[-1]["version"],
    }, indent=2))


if __name__ == "__main__":
    main()
