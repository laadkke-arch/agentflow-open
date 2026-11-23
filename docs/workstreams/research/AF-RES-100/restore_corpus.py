"""Verify or restore the sealed AF-RES-100 primary-source cache.

Run from any directory with --offline (read-only, no network) or --restore.
The committed compressed inventory, plan, build receipts and corpus manifest
are inputs, never outputs. Only missing registered files and missing original
archives below evidence/_cache/corpora may be installed. Existing files are
never overwritten. Archive-byte drift is rejected, even if caused only by
different compression; this command cannot silently construct a new corpus.

No archive member is executed, and tarfile.extract/extractall are never used.
The JSON report goes to stdout; exit 0 means the complete registered corpus
was verified. A missing original archive is permitted in offline mode when
all its registered bodies are present, and is reported as unverified.
"""

import argparse
import collections
import datetime
import fnmatch
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import shlex
import stat
import sys
import tarfile
import tempfile
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parent
CACHE = PurePosixPath("evidence/_cache/corpora")
EXPECTED_FILES = 3488
MAX_LEDGER_BYTES = 32 * 1024 * 1024
CHUNK = 1024 * 1024
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
COMMIT = re.compile(r"[0-9a-f]{40}\Z")


class RestoreError(Exception):
    """A verification or safety failure; never an invitation to rebuild."""


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise RestoreError(message)


def relative_parts(value, description):
    require(isinstance(value, str) and value, description + ": empty/non-string path")
    require("\\" not in value and not any(ord(c) < 32 for c in value),
            description + ": backslash or control character")
    parts = value.split("/")
    require(all(p not in ("", ".", "..") for p in parts),
            description + ": absolute, empty, dot or traversal component")
    require(all(":" not in p for p in parts), description + ": drive or alternate-stream component")
    require(not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).drive,
            description + ": absolute or drive-qualified path")
    return parts


def cache_path(relative, create_parents=False):
    """Resolve only cache destinations; refuse symlink ancestors and targets."""
    parts = relative_parts(relative, "cache destination")
    require(parts[:3] == list(CACHE.parts), "destination is outside the corpus cache")
    current = ROOT
    for index, part in enumerate(parts):
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            if create_parents and index < len(parts) - 1:
                current.mkdir()
            continue
        require(not stat.S_ISLNK(info.st_mode), "symlink cache path: " + relative)
        if index < len(parts) - 1:
            require(stat.S_ISDIR(info.st_mode), "non-directory cache ancestor: " + relative)
    return current


def read_metadata(name, report):
    raw = (ROOT / name).read_bytes()
    report["metadata_inputs"].append({"path": name, "bytes": len(raw), "sha256": sha(raw)})
    return raw


def official_url(url, repository):
    """Permit only this pinned official endpoint and its pinned GitHub redirect."""
    parsed = urllib.parse.urlsplit(url)
    require(parsed.scheme == "https" and parsed.username is None and parsed.password is None
            and parsed.port in (None, 443) and not parsed.query and not parsed.fragment,
            "non-HTTPS, credential-bearing or parameterized archive URL")
    commit = repository.get("commit")
    if commit is not None:
        require(isinstance(commit, str) and COMMIT.fullmatch(commit), "invalid pinned commit")
        repo = repository["repo"]
        allowed = {
            ("api.github.com", "/repos/" + repo + "/tarball/" + commit),
            ("codeload.github.com", "/" + repo + "/legacy.tar.gz/" + commit),
            ("codeload.github.com", "/" + repo + "/tar.gz/" + commit),
        }
    else:
        require(repository["label"] == "SED" and repository["repo"] == "GNU/sed"
                and repository["version"] == "4.9", "unrecognized uncommitted release source")
        allowed = {("ftp.gnu.org", "/gnu/sed/sed-4.9.tar.xz")}
    require((parsed.hostname, parsed.path) in allowed, "unapproved or unpinned archive URL: " + url)


def load_inventory(report):
    plan = json.loads(read_metadata("corpus-plan.json", report))
    manifest = json.loads(read_metadata("evidence/corpus-manifest.json", report))
    receipts = json.loads(read_metadata("evidence/corpus-build-receipts.json", report))
    compressed = read_metadata("corpus-files.jsonl.gz", report)
    with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as stream:
        raw = stream.read(MAX_LEDGER_BYTES + 1)
    require(len(raw) <= MAX_LEDGER_BYTES, "inventory exceeds decompression limit")
    require(sha(raw) == manifest["corpus_file_sha256"], "logical inventory SHA-256 mismatch")
    require(report["metadata_inputs"][0]["sha256"] == manifest["plan_sha256"],
            "corpus plan SHA-256 mismatch")
    require(manifest["files"] == EXPECTED_FILES, "unexpected sealed corpus file count")
    require(not manifest.get("failed_repositories"), "original corpus has failed repositories")
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    require(len(rows) == EXPECTED_FILES, "inventory record count mismatch")
    repositories, builds = {}, {}
    for item in plan["repositories"]:
        label = item["label"]
        require(isinstance(label, str) and re.fullmatch(r"[A-Z][A-Z0-9]*", label),
                "invalid repository label")
        require(label not in repositories, "duplicate repository label: " + label)
        official_url(item["archive_url"], item)
        repositories[label] = item
    for receipt in receipts:
        label = receipt["label"]
        require(label in repositories and label not in builds, "unknown/duplicate build receipt")
        require(receipt["status_summary"] == "success", "unsuccessful original build: " + label)
        require(receipt["url"] == repositories[label]["archive_url"], "receipt URL mismatch: " + label)
        expected_sha = receipt.get("archive_sha256")
        require(expected_sha is None or (isinstance(expected_sha, str) and SHA256.fullmatch(expected_sha)),
                "invalid archive digest: " + label)
        require(type(receipt["download_bytes"]) is int and receipt["download_bytes"] > 0,
                "invalid archive byte count: " + label)
        builds[label] = receipt
    require(repositories.keys() == builds.keys(), "repository/receipt labels differ")
    ids, targets, host_targets = set(), set(), set()
    groups = collections.defaultdict(list)
    for row in rows:
        label = row["label"]
        require(label in repositories, "unknown inventory repository")
        item = repositories[label]
        relative_parts(row["path"], "registered member")
        expected_cache = str(CACHE / label / "files" / row["path"])
        require(row["cached_body"] == expected_cache, "registered cache path mismatch")
        require(row["file_id"] not in ids and expected_cache not in targets,
                "duplicate registered ID or path")
        require(os.path.normcase(expected_cache) not in host_targets,
                "registered paths collide on this platform")
        require(re.fullmatch(re.escape(label) + r"-\d{4,}", row["file_id"]), "invalid file ID")
        require(isinstance(row["sha256"], str) and SHA256.fullmatch(row["sha256"]),
                "invalid file SHA-256")
        require(type(row["bytes"]) is int and 0 <= row["bytes"] <= plan["max_file_bytes"],
                "invalid registered file size")
        require(type(row["line_count"]) is int and row["line_count"] >= 0, "invalid line count")
        for key in ("repo", "commit", "version", "published_utc", "archive_url"):
            require(row[key] == item.get(key), "inventory/plan mismatch for " + key)
        expected_url = item["file_url_template"].replace(
            "{path}", urllib.parse.quote(row["path"], safe="/"))
        require(row["url"] == expected_url, "registered provenance URL mismatch")
        require(any(fnmatch.fnmatchcase(row["path"], pat) for pat in item["include"])
                and not any(fnmatch.fnmatchcase(row["path"], pat) for pat in item.get("exclude", [])),
                "registered member falls outside the sealed plan")
        ids.add(row["file_id"])
        targets.add(expected_cache)
        host_targets.add(os.path.normcase(expected_cache))
        groups[label].append(row)
    for label, receipt in builds.items():
        require(len(groups[label]) == receipt["included_files"], "receipt file count mismatch: " + label)
    report["inventory"] = {
        "files": len(rows), "logical_sha256": sha(raw), "logical_bytes": len(raw),
        "compressed_sha256": sha(compressed), "plan_hash_matches_manifest": True,
        "body_bytes": sum(row["bytes"] for row in rows),
    }
    return rows, repositories, builds, groups


def validate_body(data, row):
    require(len(data) == row["bytes"], "byte count mismatch: " + row["file_id"])
    require(sha(data) == row["sha256"], "SHA-256 mismatch: " + row["file_id"])
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise RestoreError("invalid UTF-8: " + row["file_id"] + " at byte " + str(exc.start)) from exc
    require("\x00" not in text, "NUL in registered text: " + row["file_id"])
    require(len(text.splitlines()) == row["line_count"], "line count mismatch: " + row["file_id"])


def verify_bodies(rows):
    missing, invalid, valid = [], [], 0
    for row in rows:
        try:
            path = cache_path(row["cached_body"])
            try:
                info = path.lstat()
            except FileNotFoundError:
                missing.append(row["file_id"])
                continue
            require(stat.S_ISREG(info.st_mode), "nonregular cached body: " + row["file_id"])
            require(info.st_size == row["bytes"], "byte count mismatch: " + row["file_id"])
            with path.open("rb") as stream:
                data = stream.read(row["bytes"] + 1)
            validate_body(data, row)
            valid += 1
        except (RestoreError, OSError) as exc:
            invalid.append({"file_id": row["file_id"], "error": str(exc)})
    return {"valid": valid, "missing": missing, "invalid": invalid}


def hash_archive(path, receipt, result):
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode), "nonregular archive: " + receipt["label"])
    digest, size = hashlib.sha256(), 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(CHUNK), b""):
            digest.update(chunk)
            size += len(chunk)
    result.update({"actual_sha256": digest.hexdigest(), "actual_bytes": size})
    expected = receipt.get("archive_sha256")
    require(expected is None or digest.hexdigest() == expected,
            "original archive SHA-256 mismatch: " + receipt["label"]
            + "; rejected (including possible upstream recompression); no new corpus accepted")
    require(size == receipt["download_bytes"], "original archive byte count mismatch: " + receipt["label"])
    result["archive_hash_verified"] = expected is not None
    result["archive_hash_status"] = "matched_original" if expected else "not_recorded_in_receipt"


class PinnedRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        official_url(newurl, self.repository)
        return super().redirect_request(request, fp, code, msg, headers, newurl)


def install_missing(staged, relative):
    """Atomic no-clobber installation; the stage and destination share a filesystem."""
    destination = cache_path(relative, create_parents=True)
    try:
        os.link(staged, destination, follow_symlinks=False)
    except FileExistsError as exc:
        raise RestoreError("refusing to replace an existing/concurrently created cache file: " + relative) from exc


def download_archive(repository, receipt, relative, report, result):
    destination = cache_path(relative, create_parents=True)
    limit = max(receipt["download_bytes"] * 2 + 16 * CHUNK, 16 * CHUNK)
    request = urllib.request.Request(repository["archive_url"], headers={
        "User-Agent": "AF-RES-100-sealed-corpus-restorer", "Accept-Encoding": "identity"})
    opener = urllib.request.build_opener(PinnedRedirect(repository))
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix=".archive-", suffix=".part", dir=destination.parent,
                                         delete=False) as output:
            temporary = Path(output.name)
            report["network_requests"] += 1
            with opener.open(request, timeout=30) as response:
                official_url(response.geturl(), repository)
                require(response.status == 200, "archive HTTP status is not 200")
                result["resolved_url"] = response.geturl()
                size = 0
                for chunk in iter(lambda: response.read(CHUNK), b""):
                    size += len(chunk)
                    require(size <= limit, "archive download exceeds the safety limit; rejected")
                    output.write(chunk)
            output.flush()
            os.fsync(output.fileno())
        hash_archive(temporary, receipt, result)
        install_missing(temporary, relative)
        result["downloaded"] = True
        report["writes"]["archives_installed"] += 1
        return destination
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def scan_archive(path, rows, missing, restore, result, report):
    """Validate original names and every registered payload before publishing any body."""
    registered = {row["path"]: row for row in rows}
    seen, roots, staged = set(), set(), []
    counts = {"members_checked": 0, "registered_members_verified": 0,
              "unregistered_regular_skipped": 0, "unregistered_nonregular_skipped": 0}
    stage_context = tempfile.TemporaryDirectory(prefix=".restore-", dir=path.parent) if restore and missing else None
    try:
        with tarfile.open(path, mode="r|*") as archive:
            for member in archive:
                counts["members_checked"] += 1
                name = member.name[:-1] if member.isdir() and member.name.endswith("/") else member.name
                parts = relative_parts(name, "original archive member")
                roots.add(parts[0])
                require(len(roots) == 1, "archive contains multiple top-level roots")
                if len(parts) == 1:
                    require(member.isdir(), "archive root is not a directory")
                    counts["unregistered_nonregular_skipped"] += 1
                    continue
                relative = "/".join(parts[1:])
                if relative not in registered:
                    key = "unregistered_regular_skipped" if member.isfile() else "unregistered_nonregular_skipped"
                    counts[key] += 1
                    continue
                row = registered[relative]
                require(relative not in seen, "duplicate registered archive member: " + row["file_id"])
                seen.add(relative)
                require(member.isfile() and member.sparse is None,
                        "registered member is a link, special or sparse file: " + row["file_id"])
                require(member.size == row["bytes"], "archive member size mismatch: " + row["file_id"])
                source = archive.extractfile(member)
                require(source is not None, "registered archive member cannot be read")
                with source:
                    data = source.read(row["bytes"] + 1)
                validate_body(data, row)
                counts["registered_members_verified"] += 1
                if restore and row["file_id"] in missing:
                    staged_path = Path(stage_context.name) / row["file_id"]
                    staged_path.write_bytes(data)
                    staged.append((staged_path, row["cached_body"]))
        require(seen == registered.keys(), "archive is missing registered members")
        result.update(counts)
        result["archive_root"] = next(iter(roots))
        result["member_safety_checked"] = True
        for staged_path, relative in staged:
            install_missing(staged_path, relative)
            report["writes"]["bodies_installed"] += 1
    finally:
        if stage_context is not None:
            stage_context.cleanup()


def run(mode):
    report = {
        "schema": "af-res-100-corpus-restore-v1", "mode": mode,
        "started_utc": now(), "command": shlex.join(getattr(sys, "orig_argv", [sys.executable, *sys.argv])),
        "implementation": {"path": "restore_corpus.py", "sha256": sha(Path(__file__).read_bytes()),
                           "python": sys.version},
        "network_requests": 0, "metadata_inputs": [], "repositories": [], "errors": [],
        "writes": {"archives_installed": 0, "bodies_installed": 0},
        "hash_scope": {
            "inventory": "Exact decompressed committed corpus-files.jsonl.gz bytes, anchored to corpus-manifest.json",
            "bodies": "Every registered original raw byte sequence: SHA-256, byte length, strict UTF-8, no NUL, splitlines count; no newline normalization",
            "archives": "Every available/used original compressed archive: recorded SHA-256 and byte size; all member paths and every registered payload validated",
            "write_scope": str(CACHE) + "/ only; no tracked ledgers, receipts, judgments, recruitment or source programs are written/executed",
        },
        "limitations": [
            "Missing archives are not fetched in offline mode; available bodies still must all verify.",
            "Archive compression or packaging drift is rejected; there is no accept-new-hash override.",
            "Existing invalid files are reported, never repaired or overwritten automatically.",
            "Only the registered primary-source corpus is restored; other ignored cache categories are outside this command.",
            "Atomic installation requires same-filesystem hard-link support and a filesystem preserving the registered paths.",
        ],
    }
    try:
        rows, repositories, builds, groups = load_inventory(report)
        before = verify_bodies(rows)
        report["bodies_before"] = before
        # Never download or publish anything while existing evidence differs.
        may_restore = mode == "restore" and not before["invalid"]
        if before["invalid"]:
            report["errors"].append("existing cache validation failed; restoration is disabled")
        missing = set(before["missing"])
        for label, repository in repositories.items():
            receipt = builds[label]
            relative = str(CACHE / label / "source.tar")
            result = {"label": label, "archive_path": relative,
                      "registered_files": len(groups[label]), "url": repository["archive_url"],
                      "expected_sha256": receipt.get("archive_sha256"),
                      "expected_bytes": receipt["download_bytes"], "downloaded": False,
                      "archive_hash_verified": False, "member_safety_checked": False}
            report["repositories"].append(result)
            try:
                path = cache_path(relative)
                needed = {row["file_id"] for row in groups[label]} & missing
                if not path.exists():
                    if may_restore and needed:
                        path = download_archive(repository, receipt, relative, report, result)
                    else:
                        result["status"] = "archive_absent_not_verified"
                        continue
                if not result["downloaded"]:
                    hash_archive(path, receipt, result)
                scan_archive(path, groups[label], needed, may_restore, result, report)
                result["status"] = "verified"
            except (RestoreError, OSError, tarfile.TarError, ValueError) as exc:
                result["status"] = "failed"
                result["error"] = str(exc)
                report["errors"].append(label + ": " + str(exc))
        after = verify_bodies(rows) if report["writes"]["bodies_installed"] else before
        report["bodies_after"] = after
        report["counts"] = {
            "registered_files": len(rows), "verified_files": after["valid"],
            "missing_files": len(after["missing"]), "invalid_files": len(after["invalid"]),
            "archives_hash_verified": sum(r["archive_hash_verified"] for r in report["repositories"]),
            "archives_member_safety_checked": sum(r["member_safety_checked"] for r in report["repositories"]),
            "registered_archive_payloads_verified": sum(r.get("registered_members_verified", 0) for r in report["repositories"]),
        }
        if after["missing"]:
            report["errors"].append("registered bodies remain missing")
        if after["invalid"]:
            report["errors"].append("registered bodies remain invalid")
    except (RestoreError, OSError, ValueError, KeyError, TypeError, gzip.BadGzipFile, EOFError) as exc:
        report["errors"].append(type(exc).__name__ + ": " + str(exc))
    report["exit_code"] = 1 if report["errors"] else 0
    report["finished_utc"] = now()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--offline", action="store_true", help="verify all fixed bodies and available archives without network or writes")
    modes.add_argument("--restore", action="store_true", help="restore missing fixed bodies using only verified pinned official archives")
    args = parser.parse_args()
    report = run("offline" if args.offline else "restore")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
