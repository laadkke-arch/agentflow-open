"""Read two development builds around the merge and the late 10.7 archives."""

import argparse
import hashlib
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path

from release_artifacts import verify_package
from release_rules import inspect

DEVS = ("6.6.2-dev.1629476146484", "6.6.2-dev.1629628221039")
LATE = ("10.7.0", "10.7.1", "10.7.2", "10.8.0")


def entries(cache, version):
    with tarfile.open(cache / f"ol-{version}.tgz", "r:gz") as package:
        return {member.name: hashlib.sha256(package.extractfile(member).read()).hexdigest()
                for member in package.getmembers() if member.isfile()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packument", type=Path)
    parser.add_argument("--cache", type=Path, required=True)
    args = parser.parse_args()
    packument = json.loads(args.packument.read_bytes())
    builds = {}
    for version in DEVS:
        dist = packument["versions"][version]["dist"]
        result = verify_package({"version": version, "tarball_url": dist["tarball"],
                                 "tarball_integrity": dist["integrity"], "tarball_npm_sha1": dist["shasum"]},
                                args.cache)
        assert result["tarball_status"] == "verified", result
        builds[version] = {
            "publish_utc": packument["time"][version],
            "npm_git_head": packument["versions"][version].get("gitHead"),
            "integrity": dist["integrity"],
            "url": dist["tarball"],
            **result, **inspect((args.cache / f"Translate-{version}.js").read_bytes()),
        }
    packages = {tag: entries(args.cache, tag) for tag in LATE}
    baseline = packages["10.7.0"]
    differences = {}
    for tag, version in packages.items():
        changed = sorted(key for key in baseline.keys() | version.keys() if baseline.get(key) != version.get(key))
        differences[tag] = {"regular_file_count": len(version), "changed_file_count": len(changed),
                            "only_changed_file_if_one": changed[0] if len(changed) == 1 else None,
                            "translate_changed": "package/interaction/Translate.js" in changed}
    print(json.dumps({"observed_utc": datetime.now(timezone.utc).isoformat(),
                      "boundary_development_builds": builds, "baseline": "10.7.0",
                      "regular_file_differences": differences}, indent=2))


if __name__ == "__main__":
    main()
