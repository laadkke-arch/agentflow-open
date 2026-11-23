#!/usr/bin/env python3
"""Record official stable-release and wheel-to-tag observations."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from email.parser import BytesParser
import hashlib
import io
import json
from pathlib import Path
from urllib.request import urlopen
import zipfile

from build_catalogs import REMOTES, ensure_repos, git, read_tree

try:
    from packaging.version import Version
except ImportError:
    from pip._vendor.packaging.version import Version


CUTOFF = datetime.fromisoformat("2026-11-22T00:00:00+00:00")
DIST_TYPES = {"bdist_wheel", "sdist"}


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat()


def obtain(url, path=None):
    if path and path.exists():
        body = path.read_bytes()
        return body, {"access": "saved response", "url": url, "sha256": digest(body), "bytes": len(body)}
    with urlopen(url, timeout=25) as response:
        body = response.read()
        receipt = {"access": "public HTTPS", "url": response.geturl(), "http_status": response.status,
                   "utc": utc(), "sha256": digest(body), "bytes": len(body),
                   "server_date": response.headers.get("Date")}
    if path:
        path.write_bytes(body)
    return body, receipt


def dist_row(data):
    return {
        "filename": data["filename"], "type": data["packagetype"],
        "upload_utc": data["upload_time_iso_8601"], "yanked": data["yanked"],
        "sha256": data["digests"]["sha256"], "url": data["url"],
        "requires_python": data.get("requires_python"),
    }


def release_rows(metadata):
    eligible = []
    rows = []
    for label, files in metadata["releases"].items():
        version = Version(label)
        releases = [dist_row(f) for f in files if f["packagetype"] in DIST_TYPES]
        live = [datetime.fromisoformat(f["upload_utc"]) for f in releases if f["yanked"] is False]
        first = min(live) if live else None
        passes = bool(first and first < CUTOFF and not version.is_prerelease and not version.is_devrelease)
        rows.append({"version": label, "stable": not (version.is_prerelease or version.is_devrelease),
                     "first_current_nonyanked_utc": first.isoformat() if first else None,
                     "eligible_before_cutoff": passes, "distributions": releases})
        if passes:
            eligible.append((first, version, label))
    return rows, sorted(eligible, reverse=True)


def compare_wheel(repo, pinned, dist, cache):
    wheel, source = obtain(dist["url"], cache / dist["filename"])
    if source["sha256"] != dist["sha256"]:
        raise ValueError(f"Official wheel checksum mismatch: {dist['filename']}")
    commit = git(repo, "rev-parse", f"refs/tags/{pinned['tag']}^{{commit}}").decode().strip()
    if commit != pinned["commit"]:
        raise ValueError(f"Tag no longer points to pinned commit: {pinned['tag']}")
    names = ("click/",) if pinned["package"] == "click" else ("attr/", "attrs/")
    matched, different, missing = [], [], []
    with zipfile.ZipFile(io.BytesIO(wheel)) as archive:
        path = next(p for p in archive.namelist() if p.endswith(".dist-info/METADATA"))
        metadata = BytesParser().parsebytes(archive.read(path))
        if str(Version(metadata["Version"])) != str(Version(pinned["version"])):
            raise ValueError("PyPI wheel METADATA version differs from requested version")
        tree = read_tree(repo, commit)
        for member in sorted(archive.namelist()):
            if not (member.startswith(names) and member.endswith(".py")):
                continue
            target = f"src/{member}" if f"src/{member}" in tree else member
            if target not in tree:
                missing.append(member)
                continue
            original = git(repo, "cat-file", "blob", tree[target])
            shipped = archive.read(member)
            if original == shipped:
                matched.append(target)
            else:
                different.append({"path": target, "tag_sha256": digest(original), "wheel_sha256": digest(shipped)})
    return {
        "distribution": dist, "read": source, "wheel_metadata_path": path,
        "wheel_metadata_name": metadata["Name"], "wheel_metadata_version": metadata["Version"],
        "tag_url": f"https://github.com/{REMOTES[pinned['package']]}/tree/{commit}",
        "tag_object": git(repo, "rev-parse", f"refs/tags/{pinned['tag']}").decode().strip(),
        "tag": pinned["tag"], "commit": commit, "matched_python_source_count": len(matched),
        "matched_python_sources": matched, "wheel_only_python_sources": missing,
        "different_python_sources": different,
        "compared_utc": utc(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--versions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--live", action="store_true", help="Bypass previously saved index response")
    args = parser.parse_args()
    args.workspace.mkdir(parents=True, exist_ok=True)
    pins = json.loads(args.versions.read_text())
    repos = ensure_repos(args.workspace, pins)
    packages = {}
    for package, repo in repos.items():
        url = f"https://pypi.org/pypi/{package}/json"
        body, receipt = obtain(url, None if args.live else args.workspace / f"{package}.pypi.json")
        metadata = json.loads(body)
        entries, eligible = release_rows(metadata)
        by_version = {row["version"]: row for row in entries}
        selection = eligible[0][2]
        releases = []
        for pinned in pins:
            if pinned["package"] != package:
                continue
            actual = by_version[pinned["version"]]
            wheels = [f for f in actual["distributions"] if f["type"] == "bdist_wheel"]
            wheel = min(wheels, key=lambda f: (f["yanked"], f["upload_utc"], f["filename"]))
            record = compare_wheel(repo, pinned, wheel, args.workspace)
            record["role"] = "cutoff-reference" if pinned["version"] == selection else "additional-exact"
            releases.append(record)
        packages[package] = {
            "index": receipt, "index_serial": metadata.get("last_serial"),
            "selected_reference": selection, "selection_order": [value[2] for value in eligible],
            "all_public_release_records_seen": entries, "pinned_artifacts": releases,
        }
    output = {
        "cutoff_utc": CUTOFF.isoformat(), "read_utc": utc(), "packages": packages,
        "limitations": [
            "Current yanked flags are observable. PyPI project JSON does not provide their complete history.",
            "Deleted files and metadata missing from the live index are outside this observation.",
            "Tag equivalence check compares shipped Python files and wheel METADATA. Documentation, wheel build process, tests and compiled files are outside this comparison.",
        ],
    }
    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
