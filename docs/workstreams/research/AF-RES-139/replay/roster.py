"""Freeze publication order from registry metadata with a strict stable-version filter."""
import argparse
import json
import re

from common import Fetcher, REGISTRY, ROOT, write_json

STABLE = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)\Z")
LAST_DAY_EXCLUSIVE = "2026-01-01T00:00:00.000Z"


def semver(version):
    return tuple(map(int, STABLE.fullmatch(version).groups()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", required=True)
    args = parser.parse_args()
    raw, receipt = Fetcher(args.cache).get(REGISTRY)
    registry = json.loads(raw)
    times = registry["time"]
    versions = registry["versions"]
    start = times["6.0.0"]
    candidates = [
        version for version in versions
        if STABLE.fullmatch(version) and start <= times.get(version, "") < LAST_DAY_EXCLUSIVE
        and (version == "6.0.0" or times[version] > start
             or (times[version] == start and semver(version) > (6, 0, 0)))
    ]
    candidates.sort(key=lambda version: (times[version], semver(version)))
    assert candidates[0] == "6.0.0"
    selected = candidates[:30]
    semvers = sorted(selected, key=semver)
    rows = []
    for version in sorted(set(versions) | (set(times) - {"created", "modified"})):
        data = versions.get(version)
        published = times.get(version)
        if not published:
            status = "version_without_clock"
        elif data is None:
            status = "clock_without_version"
        elif published < start or published >= LAST_DAY_EXCLUSIVE:
            status = "outside_utc_window"
        elif not STABLE.fullmatch(version):
            status = "not_stable"
        elif version in selected:
            status = "included"
        elif version in candidates:
            status = "stable_after_cap"
        else:
            status = "before_baseline_tiebreak"
        row = {"version": version, "publish_utc": published, "status": status}
        if status in {"included", "not_stable", "stable_after_cap"}:
            dist = data.get("dist", {})
            row.update(git_head=data.get("gitHead"), tarball_url=dist.get("tarball"),
                       integrity=dist.get("integrity"), shasum=dist.get("shasum"),
                       deprecation_metadata_present=bool(data.get("deprecated")))
        if version in selected:
            row.update(publish_rank=selected.index(version) + 1, semver_rank=semvers.index(version) + 1)
        rows.append(row)
    write_json(ROOT / "evidence/roster.json", {
        "registry": receipt, "start": start, "end_exclusive": LAST_DAY_EXCLUSIVE,
        "dist_tags_on_read": registry["dist-tags"], "unpublished_metadata_present": "unpublished" in times,
        "published_order": selected, "semver_order": semvers,
        "same_instant_groups_in_window": {
            ts: sorted(version for version in times if version not in {"created", "modified"} and times[version] == ts)
            for ts in sorted({times[version] for version in versions if start <= times.get(version, "") < LAST_DAY_EXCLUSIVE})
            if sum(value == ts for version, value in times.items() if version not in {"created", "modified"}) > 1
        },
        "catalog": rows,
    })
    print(f"{len(selected)} selected / {len(candidates)} stable in window")
    print("publication order:", " ".join(selected))
    print("semver order:", " ".join(semvers))


if __name__ == "__main__":
    main()
