"""Fetch immutable public snapshots and write receipts for actual remote/local I/O."""

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from cohort import T0, node_links, python_links, sections

HERE = Path(__file__).resolve().parent
TRACE_FIELDS = ("http_attempts", "http_body_bytes", "git_pack_bytes", "new_objects",
                "local_reads", "local_bytes", "retries", "elapsed_s")
ROLE_PATHS = {
    "python": {"catalog": "Doc/library/index.rst", "release_index": "Doc/whatsnew/index.rst"},
    "node": {"catalog": "doc/api/index.md", "release_index": "CHANGELOG.md"},
}
RAW = "https://raw.githubusercontent.com"
UTC = timezone.utc


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def read_jsonl(path):
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream]


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def now():
    return datetime.now(UTC).isoformat(timespec="seconds")


def blob_id(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def frozen_url(release, path):
    return f"{RAW}/{release['repository']}/{release['commit']}/{path}"


def base_receipt(release, kind, path, url):
    return {
        "quarter": release["quarter"], "ecosystem": release["ecosystem"], "kind": kind,
        "path": path, "url": url, "measured_utc": now(), "http_attempts": 0,
        "http_body_bytes": 0, "git_pack_bytes": 0, "new_objects": 0,
        "local_reads": 0, "local_bytes": 0, "retries": 0,
        "http_status": "", "errors": [],
    }


def raw_read(cache, release, kind, path, expected, url=None):
    source = url or frozen_url(release, path)
    receipt = base_receipt(release, kind, path, source)
    start = perf_counter()
    key = hashlib.sha256(source.encode()).hexdigest()
    metadata = cache / "http" / f"{key}.json"
    payload = cache / "http" / f"{key}.body"
    if metadata.exists():
        got = metadata.read_bytes()
        old = json.loads(got)
        data = payload.read_bytes() if old["http_status"] == 200 else b""
        receipt.update(status=old["status"], http_status=old["http_status"], route="local_http_cache",
                       local_reads=1 + int(old["http_status"] == 200),
                       local_bytes=len(got) + len(data))
    else:
        data = b""
        receipt.update(route="network_http")
        for attempt in range(2):
            receipt["http_attempts"] += 1
            try:
                request = Request(source, headers={"User-Agent": "AF-RES-024 public release research",
                                                   "Accept-Encoding": "identity"})
                with urlopen(request, timeout=20) as response:
                    data = response.read()
                    receipt["http_status"] = response.status
                    receipt["http_body_bytes"] += len(data)
                consistent = (expected == blob_id(data)) if expected else (
                    expected is None or expected == "unverified")
                receipt["status"] = "ok" if consistent else "blob_mismatch"
            except HTTPError as exception:
                body = exception.read()
                receipt["http_body_bytes"] += len(body)
                receipt["http_status"] = exception.code
                receipt["status"] = "missing" if exception.code == 404 and expected == "" else "failure"
                receipt["errors"].append(f"HTTP {exception.code}")
                if 500 <= exception.code < 600 and attempt == 0:
                    receipt["retries"] += 1
                    continue
            except (URLError, TimeoutError, OSError) as exception:
                receipt["status"] = "failure"
                receipt["errors"].append(str(exception))
                if attempt == 0 and "403 Forbidden" not in str(exception):
                    receipt["retries"] += 1
                    continue
            break
        if receipt["status"] in {"ok", "missing"}:
            if receipt["http_status"] == 200:
                payload.write_bytes(data)
            metadata.write_text(json.dumps({k: receipt[k] for k in ("status", "http_status")}))
    receipt["elapsed_s"] = round(perf_counter() - start, 6)
    receipt["content_bytes"] = len(data) if receipt["status"] == "ok" else 0
    receipt["body_sha256"] = hashlib.sha256(data).hexdigest() if receipt["status"] == "ok" else ""
    return receipt, data if receipt["status"] == "ok" else b""


def git_read(cache, release):
    work = cache / f"git-{release['ecosystem']}"
    url = f"https://github.com/{release['repository']}.git"
    tag = f"refs/tags/{release['tag']}"
    receipt = base_receipt(release, "git_tree", tag, url)
    start = perf_counter()
    if not work.exists():
        subprocess.run(["git", "init", "--bare", "-q", str(work)], check=True)
    git = ["git", "-C", str(work), "-c", "protocol.version=2", "-c", "fetch.unpackLimit=1"]
    existence = subprocess.run([*git, "rev-parse", "--verify", f"{tag}^{{commit}}"], capture_output=True,
                               text=True)
    if existence.returncode == 0:
        receipt["route"] = "local_git"
        pinned = existence.stdout.strip()
    else:
        receipt["route"] = "network_git"
        pinned = ""
        old = set((work / "objects" / "pack").glob("*.pack"))
        for attempt in range(2):
            env = os.environ | {"GIT_TRACE_CURL": "1", "GIT_TERMINAL_PROMPT": "0"}
            got = subprocess.run(
                [*git, "fetch", "--depth=1", "--filter=blob:none", "--no-tags",
                 "--no-auto-maintenance", url, f"{tag}:{tag}"],
                env=env, capture_output=True, timeout=60,
            )
            # Count trace headers and incoming data sizes. The raw trace is never persisted.
            trace = got.stderr.decode(errors="replace")
            receipt["http_attempts"] += len(re.findall(r"=> Send header: (?:GET|POST) ", trace))
            receipt["http_body_bytes"] += sum(
                int(m[1]) for m in re.finditer(r"<= Recv data, 0*([0-9]+) bytes", trace)
            )
            if got.returncode == 0:
                pinned = subprocess.check_output([*git, "rev-parse", f"{tag}^{{commit}}"], text=True).strip()
                break
            receipt["errors"].extend(line for line in trace.splitlines() if line.startswith(("error:", "fatal:")))
            receipt["retries"] += int(attempt == 0)
        for pack in set((work / "objects" / "pack").glob("*.pack")) - old:
            receipt["git_pack_bytes"] += pack.stat().st_size
            indexes = subprocess.check_output([*git, "show-index"], input=pack.with_suffix(".idx").read_bytes())
            receipt["new_objects"] += len(indexes.splitlines())
    tree = {}
    if pinned == release["commit"]:
        paths = ["Doc/library", "Doc/whatsnew", "doc/api", "doc/changelogs", "CHANGELOG.md"]
        got = subprocess.run([*git, "ls-tree", "-r", "-z", pinned, "--", *paths], check=True, capture_output=True)
        for line in got.stdout.decode().rstrip("\0").split("\0"):
            if line:
                header, path = line.split("\t", 1)
                tree[path] = header.split()[2]
        receipt.update(status="ok", local_reads=1, local_bytes=len(got.stdout))
    else:
        receipt["status"] = "failure"
    receipt["elapsed_s"] = round(perf_counter() - start, 6)
    receipt["content_bytes"] = receipt["local_bytes"]
    receipt["body_sha256"] = ""
    return receipt, tree


def linked_path(eco, index_text, tag):
    version = tag.removeprefix("v").split(".")
    if eco == "python":
        path = f"Doc/whatsnew/{'.'.join(version[:2])}.rst"
        links = python_links(index_text, ROLE_PATHS[eco]["release_index"])
        return path if path in links else ""
    path = f"doc/changelogs/CHANGELOG_V{version[0]}.md"
    return path if re.search(r"\]\(" + re.escape(path) + r"\)", index_text) else ""


def doc_record(release, kind, path, tree, receipt):
    return {
        "quarter": release["quarter"], "cutoff": release["cutoff"], "ecosystem": release["ecosystem"],
        "kind": kind, "path": path, "url": receipt["url"], "status": receipt["status"],
        "raw_status": receipt["http_status"], "blob": tree.get(path, ""),
        "content_bytes": receipt["content_bytes"], "sha256": receipt["body_sha256"],
    }


def make_sections(eco, path, data, reasons):
    found = sections(eco, data.decode("utf-8"), path) if data else []
    result = []
    for reason in reasons:
        matching = [s for s in found if s.name == reason["symbol"] and s.kind == reason["kind"]]
        section = matching[0] if matching else None
        result.append({
            "id": reason["id"], "section": "present" if section else "unlocated",
            "start": section.start if section else None, "end": section.end if section else None,
            "section_sha256": hashlib.sha256(section.text.encode()).hexdigest() if section else "",
            "warned": section.warned if section else None, "location_count": len(matching),
        })
    return result


def ecosystem_snapshot(release, reasons, cache, workers):
    eco = release["ecosystem"]
    tree_receipt, tree = git_read(cache, release)
    receipts = [tree_receipt]
    records = [doc_record(release, "git_tree", tree_receipt["path"], tree, tree_receipt)]
    groups = {}
    for reason in reasons:
        groups.setdefault(reason["path"], []).append(reason)
    sources = {path: role for role, path in ROLE_PATHS[eco].items()}
    sources.update({path: "manual" for path in groups})

    def download(path, kind):
        expected = tree.get(path, "") if tree_receipt["status"] == "ok" else None
        return raw_read(cache, release, kind, path, expected)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        jobs = {path: pool.submit(download, path, kind) for path, kind in sources.items()}
        for path, job in jobs.items():
            receipt, raw = job.result()
            kind = sources[path]
            doc = doc_record(release, kind, path, tree, receipt)
            if kind == "release_index":
                link = linked_path(eco, raw.decode("utf-8"), release["tag"])
                doc["release_path"] = link
                if link:
                    follow, _ = download(link, "release_notes")
                    receipts.append(follow)
                    records.append(doc_record(release, "release_notes", link, tree, follow) |
                                   {"discovered_from": path})
            elif kind == "catalog":
                links = python_links(raw.decode("utf-8"), path) if eco == "python" else node_links(raw.decode("utf-8"))
                doc["linked_paths"] = list(links)
            else:
                doc["reasons"] = make_sections(eco, path, raw, groups[path])
            records.append(doc)
            receipts.append(receipt)
    return records, receipts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=HERE)
    parser.add_argument("--quarters", nargs="+", required=True)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--run", required=True, choices=("cold", "reuse1", "reuse2"))
    parser.add_argument("--workers", type=int, default=10)
    args = parser.parse_args()
    (args.cache / "http").mkdir(parents=True, exist_ok=True)
    releases = read_csv(args.inputs / "releases.csv")
    reasons = [r for r in read_csv(args.inputs / "cohort.csv") if r["selected"] == "1"]
    for quarter in args.quarters:
        start = perf_counter()
        receipts = []
        records = []
        for release in (r for r in releases if r["quarter"] == quarter):
            batch, measured = ecosystem_snapshot(
                release, [r for r in reasons if r["ecosystem"] == release["ecosystem"]],
                args.cache, args.workers,
            )
            receipts.extend(measured)
            records.extend(batch)
        if not records:
            raise ValueError(f"Unknown quarter: {quarter}")
        wall = round(perf_counter() - start, 6)
        write_jsonl(args.out / "snapshots" / f"{quarter}.jsonl", records)
        write_jsonl(args.out / "evidence" / "receipts" / args.run / f"{quarter}.jsonl", receipts)
        print(json.dumps({"quarter": quarter, "run": args.run, "wall_s": wall,
                          "records": len(records), "ok": sum(r["status"] == "ok" for r in receipts),
                          "missing": sum(r["status"] == "missing" for r in receipts),
                          "failed": sum(r["status"] == "failure" for r in receipts),
                          **{key: round(sum(r[key] for r in receipts), 6) for key in TRACE_FIELDS}}),
              flush=True)


if __name__ == "__main__":
    main()
