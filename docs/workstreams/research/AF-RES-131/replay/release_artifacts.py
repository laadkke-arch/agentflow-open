"""Verify each npm tarball and cross-reference the Translate blob in Git."""

import argparse
import base64
import csv
import hashlib
import io
import json
import re
import subprocess
import tarfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

MODULE = "interaction/Translate.js"
SOURCE = "src/ol/" + MODULE
FIELDS = [
    "tag", "tag_object", "tag_commit", "tag_clock_utc", "tag_clock_kind",
    "publish_minus_tag_seconds", "tag_source_blob", "githead_source_blob",
    "translate_git_blob", "translate_sha256", "tarball_sha256", "tarball_status",
    "tag_source_status", "githead_source_status", "githead_tag_identity",
]


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def tags(repo):
    result = git(repo, "for-each-ref",
                 "--format=%(refname:short)|%(objectname)|%(*objectname)|%(objecttype)|%(creatordate:iso-strict)",
                 "refs/tags")
    return {name: (obj, peeled or obj, kind, clock)
            for name, obj, peeled, kind, clock in (line.split("|") for line in result.splitlines())}


def verify_package(row, cache):
    version = row["version"]
    archive = cache / f"ol-{version}.tgz"
    try:
        if not archive.exists():
            temporary = archive.with_suffix(".download")
            result = subprocess.run(["curl", "-fsSL", "--retry", "3", "--max-time", "90",
                                     row["tarball_url"], "-o", str(temporary)],
                                    text=True, capture_output=True)
            if result.returncode:
                return {"tarball_status": f"curl {result.returncode}: {result.stderr.strip()}"}
            temporary.replace(archive)
        raw = archive.read_bytes()
        sri = "sha512-" + base64.b64encode(hashlib.sha512(raw).digest()).decode("ascii")
        if row["tarball_integrity"] != sri or row["tarball_npm_sha1"] != hashlib.sha1(raw).hexdigest():
            return {"tarball_status": "npm integrity or shasum mismatch"}
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as package:
            metadata, source = [package.extractfile("package/" + file).read()
                                for file in ("package.json", MODULE)]
        if json.loads(metadata).get("version") != version:
            return {"tarball_status": "dist package version mismatch"}
        sha = hashlib.sha256(source).hexdigest()
        (cache / f"Translate-{version}.js").write_bytes(source)
        blob_header = f"blob {len(source)}\0".encode("ascii")
        return {
            "tarball_status": "verified",
            "tarball_sha256": hashlib.sha256(raw).hexdigest(),
            "translate_sha256": sha,
            "translate_git_blob": hashlib.sha1(blob_header + source).hexdigest(),
        }
    except (OSError, ValueError, KeyError, tarfile.TarError) as error:
        return {"tarball_status": f"{type(error).__name__}: {error}"}


def source_status(artifact_blob, source_blob, source_commit):
    if not source_commit:
        return "missing-ref"
    if not source_blob:
        return "missing-path-or-commit"
    if not artifact_blob:
        return "artifact-unverified"
    return "same" if artifact_blob == source_blob else "different"


def compare(repo, row, tag_index):
    tag = "v" + row["version"]
    tag_object, tag_commit, tag_type, clock = tag_index.get(tag, ("", "", "", ""))
    tag_time = datetime.fromisoformat(clock).astimezone(timezone.utc) if clock else None
    publish_time = datetime.fromisoformat(row["publish_utc"])
    githead = row["npm_git_head"]
    assert not githead or re.fullmatch(r"[a-f0-9]{40}", githead)
    tag_source = git(repo, "rev-parse", "--verify", f"{tag_commit}:{SOURCE}") if tag_commit else ""
    head_source = git(repo, "rev-parse", "--verify", f"{githead}:{SOURCE}") if githead else ""
    artifact = row.get("translate_git_blob")
    row.update({
        "tag": tag,
        "tag_object": tag_object,
        "tag_commit": tag_commit,
        "tag_clock_utc": tag_time.isoformat() if tag_time else "",
        "tag_clock_kind": {"tag": "tagger", "commit": "commit-as-lightweight-tag-proxy"}.get(tag_type, ""),
        "publish_minus_tag_seconds": (publish_time - tag_time).total_seconds() if tag_time else "",
        "tag_source_blob": tag_source,
        "githead_source_blob": head_source,
        "tag_source_status": source_status(artifact, tag_source, tag_commit),
        "githead_source_status": source_status(artifact, head_source, githead),
        "githead_tag_identity": "same" if githead and githead == tag_commit else
                                "different" if githead and tag_commit else "missing-ref",
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roster", type=Path)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    with args.roster.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        columns = reader.fieldnames
    tag_index = tags(args.upstream)
    if not tag_index:
        parser.error("no upstream tags found")
    with ThreadPoolExecutor(max_workers=8) as pool:
        updates = pool.map(lambda row: verify_package(row, args.cache), rows)
        for row, values in zip(rows, updates, strict=True):
            row.update(values)
            compare(args.upstream, row, tag_index)
            print(row["version"], row["tarball_status"], row["tag_source_status"],
                  row["githead_source_status"], flush=True)
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, [*columns, *FIELDS], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return int(any(row["tarball_status"] != "verified" for row in rows))


if __name__ == "__main__":
    raise SystemExit(main())
