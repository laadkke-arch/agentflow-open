#!/usr/bin/env python3
"""Independent read-only checks of AF-RES-116's sealed source/recruitment inputs.

Only output under evidence/audit is written. This does not inspect recipient logs,
answers, hints, or treatment text. Packet inspection projects version metadata only.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import csv
import gzip
import hashlib
import io
import json
import re
import subprocess
import tarfile

OWN = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent
REPO = Path(subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], cwd=OWN, text=True).strip())
PREFIX = str(OWN.relative_to(REPO)) + "/"
SEALED = "8b57d241d88cb6c5ddf3454d2b28fa3fb46fd473"


def blob(path, revision=SEALED):
    return subprocess.check_output(["git", "show", revision + ":" + PREFIX + path], cwd=REPO)


def js(path, revision=SEALED):
    return json.loads(blob(path, revision))


def jl(path, revision=SEALED):
    return [json.loads(line) for line in blob(path, revision).decode().splitlines() if line.strip()]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    rows = jl("sources.jsonl")
    summary = js("analysis/source-counts.json")
    counted = [r for r in rows if r["unique_counted"]]
    allocation = Counter(r["allocation"] for r in counted)
    assert len(rows) == 195
    assert len({r["source_id"] for r in rows}) == 195
    assert len(counted) == len({r["work_id"] for r in counted}) == 37
    assert dict(allocation) == summary["counted_by_allocation"]
    assert sum(allocation[k] for k in summary["quota_minimum"]) == 34
    assert all(allocation[k] >= v for k, v in summary["quota_minimum"].items())
    assert all(r["primary"] and r["read_sections"] for r in counted)
    inventory = list(csv.DictReader(io.StringIO(blob("analysis/source-inventory.csv").decode())))
    assert {(r["work_id"], r["representative_source_id"], r["allocation"]) for r in inventory} == {
        (r["work_id"], r["source_id"], r["allocation"]) for r in counted}
    for path, digest in summary["input_sha256"].items():
        assert sha(blob(path)) == digest

    frames = []
    receipts = js("recruitment/receipts.json")
    frame = list(csv.DictReader(io.StringIO(blob("frame.csv").decode())))
    for project, words in [("pandoc", ["table", "image"]), ("imagemagick", ["profile", "alpha"])]:
        union = {}
        rx = re.compile(r"\b(?:" + "|".join(words) + r")\b", re.I)
        searches = []
        for word in words:
            raw = gzip.decompress(blob(f"recruitment/{project}/search-{word}.json.gz"))
            data = json.loads(raw)
            receipt = next(r for r in receipts if r["project"] == project and r["word"] == word)
            assert sha(raw) == receipt["sha256"]
            assert len(data["items"]) == receipt["returned"]
            assert data["incomplete_results"] is False
            assert data["items"] == sorted(data["items"], key=lambda x: (x["created_at"], x["number"]))
            for item in data["items"]:
                if "pull_request" not in item and rx.search(item.get("body") or ""):
                    union[item["number"]] = item
            searches.append({"word": word, "returned": receipt["returned"],
                             "total_count": receipt["total_count"], "last_created_at": receipt["last_created_at"]})
        expected = sorted(union.values(), key=lambda x: (x["created_at"], x["number"]))[:50]
        actual = js(f"recruitment/{project}/first50.json")
        csvrows = [r for r in frame if r["project"] == project]
        assert len(expected) == len(actual) == len(csvrows) == 50
        for item, saved, record in zip(expected, actual, csvrows):
            assert item["number"] == saved["number"] == int(record["number"])
            assert item["body"] == saved["body"]
            assert sha(item["body"].encode()) == saved["body_sha256"] == record["body_sha256"]
            assert "2023-01-01T00:00:00Z" <= item["created_at"] < "2026-01-01T00:00:00Z"
        assert all(r["last_created_at"] > expected[-1]["created_at"] for r in searches)
        frames.append({"project": project, "verified_rows": 50, "first_number": expected[0]["number"],
                       "last_number": expected[-1]["number"], "threshold_utc": expected[-1]["created_at"],
                       "search_receipts": searches})
    cases = js("cases.json")["cases"]
    for case in cases:
        original = js(f"recruitment/{case['project']}/issue-{case['number']}.json")
        assert sha(original["body"].encode()) == case["original_body_sha256"]

    sealed_files = []
    for rev, paths in [
        ("7a76c8ccefb6243b84e86efce16b62ba8b47ec2d", ["SCOPE.md"]),
        ("878f2e1b8d053f6eea4e3473d5b467ca98476a01", ["cases.json", "frame.csv",
            "recruitment/pandoc/first50.json", "recruitment/imagemagick/first50.json"]),
        ("762fe1fc57b3b5f765f9d13537fa9c15b71b5b80", ["authoring/author-exposure.jsonl"]),
    ]:
        for path in paths:
            assert blob(path, rev) == blob(path)
            sealed_files.append({"path": path, "first_seal": rev, "unchanged_at_source_seal": True})
    assert blob("sources.jsonl", "878f2e1b8d053f6eea4e3473d5b467ca98476a01") == blob("recruitment/sealed-sources.jsonl")
    packet_diff = subprocess.check_output(["git", "diff", "--name-only",
        "762fe1fc57b3b5f765f9d13537fa9c15b71b5b80", SEALED, "--",
        PREFIX + "authoring", PREFIX + "packets.jsonl", PREFIX + "inputs"], cwd=REPO, text=True)
    assert not packet_diff.strip()

    cache = OWN / "evidence/document-cache.tar.gz"
    assert subprocess.check_output(["git", "hash-object", str(cache)], cwd=REPO, text=True).strip() == \
        subprocess.check_output(["git", "rev-parse", SEALED + ":" + PREFIX + "evidence/document-cache.tar.gz"], cwd=REPO, text=True).strip()
    version_specs = [("P1", "pandoc", "2.19.2", "p2192"), ("P2", "pandoc", "3.8.3", "p383"),
        ("P3", "pandoc", "2.14.0.3", "p21403"), ("I1", "imagemagick", "7.1.1-3", "i7113_processing"),
        ("I2", "imagemagick", "7.1.1-4", "i7114_processing"), ("I3", "imagemagick", "7.1.1-6", "i7116_processing")]
    versions = []
    with tarfile.open(cache) as archive:
        releases = json.load(archive.extractfile("documents/metadata/pandoc-releases.json"))
        eligible = [r for r in releases if not r["draft"] and not r["prerelease"]
                    and r["published_at"] <= "2025-12-31T23:59:59Z"]
        assert max(eligible, key=lambda r: r["published_at"])["tag_name"] == "3.8.3"
        catalog = [json.loads(line) for line in archive.extractfile("documents/catalog.jsonl").read().decode().splitlines()]
        # Only these three fields from packets are retained or evaluated. No hint text or answers.
        packet_versions = [{k: r[k] for k in ["case_id", "document_version", "start_doc_id"]}
                           for r in jl("packets.jsonl")]
        for case, project, version, doc_id in version_specs:
            commit = json.load(archive.extractfile(f"documents/metadata/{project}-{version}-commit.json"))
            start = next(r for r in catalog if r["id"] == doc_id)
            assert start["upstream_commit"] == commit["sha"] and start["version"] == version
            ps = [r for r in packet_versions if r["case_id"] == case]
            assert len(ps) == 3 and all(r["document_version"] == version and r["start_doc_id"] == doc_id for r in ps)
            versions.append({"case_id": case, "version": version, "start_doc_id": doc_id,
                             "commit": commit["sha"], "matched_packets": 3})

    index = js("evidence/reference-cache/index.json")
    file_index = {r["path"]: r for r in index["files"]}
    verified_members = 0
    for entry in index["archives"]:
        path = OWN / entry["path"]
        assert sha(path.read_bytes()) == entry["sha256"]
        with tarfile.open(path) as archive:
            for member in archive.getmembers():
                if member.isfile():
                    data = archive.extractfile(member).read()
                    recorded = file_index[member.name]
                    assert sha(data) == recorded["sha256"] and len(data) == recorded["bytes"]
                    verified_members += 1
    snapshot_checks = []
    for path in ["gold-work/pandoc/sources-pandoc.jsonl", "gold-work/imagemagick/sources-imagemagick.jsonl"]:
        for row in jl(path):
            if not row["unique_counted"]:
                continue
            relative = row.get("snapshot", row.get("snapshot_path"))
            resolved = OWN / relative if relative.startswith(("documents/", "gold-work/")) else OWN / "gold-work/imagemagick" / relative
            assert sha(resolved.read_bytes()) == row.get("sha256", row.get("source_sha256"))
            snapshot_checks.append(row["source_id"])
    result = {"audit": "sealed sources, recruitment, version metadata and storage integrity",
        "checked_utc": datetime.now(timezone.utc).isoformat(), "sealed_input_commit": SEALED,
        "result": "PASS", "source_rows": 195, "counted_works": 37,
        "required_class_works": 34, "allocation": dict(allocation), "frame_checks": frames,
        "selected_original_body_hashes_verified": 6, "sealed_file_checks": sealed_files,
        "original_source_ledger_relocated_byte_identically": True,
        "authoring_packet_input_file_names_changed_between_packet_and_gold_seals": [],
        "version_metadata_checks": versions, "reference_archives_verified": len(index["archives"]),
        "reference_archive_members_verified": verified_members,
        "counted_reference_representative_snapshot_hashes_verified": snapshot_checks,
        "limitations": ["Eligibility and same-work semantics are separately reviewed in audit.md; field checks are not semantic proof.",
                        "Git commit dates and reported read times are not independent server-side ref-update timestamps.",
                        "No recipient logs, answers, treatment text, or A/B/C outcomes are inspected."]}
    (AUDIT / "checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["result", "source_rows", "counted_works", "required_class_works",
        "allocation", "selected_original_body_hashes_verified", "reference_archives_verified", "reference_archive_members_verified"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
