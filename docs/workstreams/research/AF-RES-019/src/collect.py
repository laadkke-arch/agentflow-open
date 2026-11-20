"""Collect dated public Git and registry observations without storing personal data."""
from argparse import ArgumentParser
from bisect import bisect_right
from collections import Counter, deque
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
import calendar
import csv
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from threading import Lock
import time
import tomllib
from urllib.parse import quote, urlsplit

STUDY = Path(__file__).resolve().parents[1]
DAY = 86_400
EPOCH = date(1970, 1, 1).toordinal()
HTTP_REQUEST = re.compile(r"Send header: (?:GET|POST) ")
HTTP_RESPONSE = re.compile(r"Recv header: HTTP(?:/[^ ]*)? ([0-9]{3})")
REPOSITORY = re.compile(r"https://(?:github\.com|gitlab\.com)/[\w.\-/]+\.git$")
VERSION_TAG = re.compile(r"(?:[vr]|release[-_/])?\d+[._]\d+", re.I)
NOTICE = re.compile(r"\b(deprecated|unmaintained|archived|maintenance mode|looking for maintainers|moved to)\b", re.I)
TARGET = re.compile(r"\b(?:this|our) (?:project|package|repository|repo|library|module|codebase|tool)\b", re.I)
GIT_BASE = ["git", "-c", "credential.helper=", "-c", "credential.interactive=false",
            "-c", "core.askPass=", "-c", "http.lowSpeedLimit=512", "-c", "http.lowSpeedTime=20"]
GIT_ENV = os.environ | {"GIT_TERMINAL_PROMPT": "0", "GIT_TRACE_CURL": "1",
                        "GIT_TRACE_CURL_NO_DATA": "1", "GIT_TRACE_REDACT": "1",
                        "GIT_OPTIONAL_LOCKS": "0", "LC_ALL": "C.UTF-8"}

SIGNALS = {
    "git_commits_90d": ("git", 3, -1),
    "git_commit_age": ("git", 90, 1),
    "git_authors_365d": ("git", 2, -1),
    "git_top_author_share": ("git", .8, 1),
    "git_tag_age": ("git", 180, 1),
    "git_tag_gap": ("git", 180, 1),
    "git_license_change": ("git", 1, 1),
    "git_readme_notice": ("git", 1, 1),
    "git_cla_added": ("git", 1, 1),
    "git_package_changed": ("git", 1, 1),
    "registry_release_gap": ("registry", 180, 1),
    "registry_inactive": ("registry", 1, 1),
    "registry_license_changed": ("registry", 1, 1),
}
WINDOWS = (12, 6, 3, 1)
LOCK = Lock()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    return Path(path).read_text(encoding="utf-8")


def load_json(path):
    return json.loads(read_json(path))


def save_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def previous_months(day, ago):
    y, m = divmod(day.year * 12 + day.month - 1 - ago, 12)
    return date(y, m + 1, min(day.day, calendar.monthrange(y, m + 1)[1]))


def day_of(epoch):
    return int(epoch) // DAY + EPOCH


def parse_day(value):
    return date.fromisoformat(value[:10]).toordinal()


def at_date(value):
    return date.fromordinal(value).isoformat()


def end_of_day(day):
    return at_date(day) + "T23:59:59Z"


def packs(repo):
    return sum(p.stat().st_size for p in (repo / ".git/objects/pack").glob("*.pack"))


def git(repo, args, traffic=None, timeout=80, check=True):
    start = time.monotonic()
    stamp = utc_now()
    before = packs(repo) if traffic is not None else 0
    code, out, trace = 124, b"", ""
    try:
        proc = subprocess.run(
            [*GIT_BASE, *(["-C", str(repo)] if repo.exists() else []), *args],
            env=GIT_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
        )
        code, out = proc.returncode, proc.stdout
        trace = proc.stderr.decode("utf-8", errors="replace")
    except subprocess.TimeoutExpired as exc:
        trace = (exc.stderr or b"").decode("utf-8", errors="replace")
    if traffic is not None:
        responses = [int(code) for code in HTTP_RESPONSE.findall(trace)]
        traffic.append({"operation": args[0], "at_utc": stamp, "exit_code": code,
                        "requests": len(HTTP_REQUEST.findall(trace)), "http_replies": responses,
                        "bytes": max(0, packs(repo) - before), "seconds": round(time.monotonic() - start, 5),
                        "timeout_seconds": timeout})
    if code and check:
        status = HTTP_RESPONSE.findall(trace)
        raise RuntimeError(f"{args[0]} exit={code} HTTP={status[-5:]}")
    return code, out


def git_text(repo, args, traffic=None, timeout=80):
    return git(repo, args, traffic, timeout)[1].decode("utf-8", errors="replace")


def cache_name(text):
    return hashlib.sha256(text.encode()).hexdigest()[:20]


def prepare_repo(url, cache, full=False):
    if not REPOSITORY.fullmatch(url):
        raise ValueError(f"Unsupported public Git URL {url}")
    stem = cache_name(url) + ("-full" if full else "")
    repo, receipt = cache / stem, cache / (stem + ".json")
    if receipt.exists():
        previous = load_json(receipt)
        return repo, previous
    mode = "git_full_clone" if full else "git_partial_clone"
    args = ["clone", "--single-branch", "--no-checkout"]
    if not full:
        args.append("--filter=blob:none")
    traffic = []
    code, _ = git(repo, [*args, url, str(repo)], traffic=traffic, timeout=60 if full else 210, check=False)
    result = {"mode": mode, "url": url, **traffic[0]}
    if code == 0:
        result["head"] = git_text(repo, ["rev-parse", "HEAD"]).strip()
        result["commit_history_complete"] = git_text(repo, ["rev-parse", "--is-shallow-repository"]).strip() == "false"
        listing = git_text(repo, ["config", "--get-regexp", r"^remote\..*\.promisor$"]) if not full else ""
        result["promisor"] = "true" in listing
    save_json(receipt, result)
    return repo, result


def authors_bin(n):
    if n == 0:
        return "0"
    if n <= 3:
        return "1–3"
    if n <= 15:
        return "4–15"
    if n <= 63:
        return "16–63"
    return "64+"


def parse_commit_rows(text):
    """Dates are committer UTC; normalized addresses are used only in process."""
    rows = []
    for line in text.splitlines():
        fields = line.split("\t", maxsplit=1)
        if len(fields) != 2 or not fields[0].isdigit():
            continue
        author = fields[1].strip().casefold()
        rows.append((day_of(fields[0]), author or None))
    return sorted(rows, key=lambda row: row[0])


def match_facts(repo, t, repo_receipt):
    head = repo_receipt["head"]
    roots = git_text(repo, ["log", "--max-parents=0", "--format=%ct", head], timeout=100).splitlines()
    if not roots or not repo_receipt["commit_history_complete"]:
        return {"head": head, "unknown": "incomplete_git_history"}
    first = min(map(day_of, roots))
    facts = {"head": head, "first_commit_date": at_date(first), "first_commit_year": date.fromordinal(first).year,
             "default_roots": len(roots)}
    if t is None:
        return facts | {"unknown": "event_day_unknown"}
    if first >= t:
        return facts | {"unknown": "repo_first_commit_not_before_event"}
    hist = git_text(repo, ["log", "--no-merges", "--format=%ct%x09%aE",
                            "--since-as-filter=" + end_of_day(t - 366),
                            "--until=" + end_of_day(t - 1), head], timeout=100)
    authors = {a for d, a in parse_commit_rows(hist) if t - 365 <= d < t}
    if None in authors:
        return facts | {"unknown": "missing_author_identity"}
    return facts | {"authors_365d": len(authors), "author_bin": authors_bin(len(authors))}


def match_job(row, events, cache):
    url = row.get("repo_url")
    t = events[row.get("matched_event", row["id"])]["effective_date"]
    if not url:
        return {"id": row["id"], "unknown": "repo_not_applicable"}
    try:
        repo, receipt = prepare_repo(url, cache)
        if receipt["exit_code"]:
            return {"id": row["id"], "unknown": "git_clone_failed", "clone": receipt}
        return {"id": row["id"], **match_facts(repo, parse_day(t) if t else None, receipt), "clone": receipt}
    except (OSError, ValueError, RuntimeError) as exc:
        return {"id": row["id"], "unknown": str(exc)}


def match_all(rows, events, cache, out, jobs):
    """Persist resumable results in the specified scratch directory."""
    facts = {}
    target = out / "matching.json"
    if target.exists():
        facts = {r["id"]: r for r in load_json(target)}
    pending = [r for r in rows if r["id"] not in facts]
    with ThreadPoolExecutor(max_workers=jobs) as workers:
        for row in workers.map(lambda x: match_job(x, events, cache), pending):
            facts[row["id"]] = row
            save_json(target, list(facts.values()))
            print(row["id"], row.get("first_commit_year"), row.get("author_bin"), row.get("unknown", ""), flush=True)
    return facts



REGISTRY = {
    "npm": ("registry.npmjs.org", "/"),
    "pypi": ("pypi.org", "/pypi/"),
    "crates": ("crates.io", "/api/v1/crates/"),
    "rubygems": ("rubygems.org", "/api/v1/versions/"),
}
REGISTRY_LAST = {}
REGISTRY_BLOCKED = set()
MANIFEST_NAMES = ("package.json", "pyproject.toml", "setup.cfg", "Cargo.toml", "go.mod")
PATH_LICENSE = re.compile(r"^(?:(?:[^/]+/)*)(?:license|licence|copying)[^/]*$", re.I)
PATH_CLA = re.compile(r"^(?:\.github/)?(?:cla(?:[._-]|$)|contributor[-_ ](?:license|agreement))", re.I)


def registry_url(package):
    scheme, name = package.split(":", 1)
    host, prefix = REGISTRY[scheme]
    suffix = {"pypi": "/json", "rubygems": ".json"}.get(scheme, "")
    return scheme, host, "https://" + host + prefix + quote(name, safe="@") + suffix


def open_registry(package, directory):
    if not package:
        return {"unknown": "no_registry_package"}
    scheme, host, url = registry_url(package)
    stem = directory / cache_name(package)
    receipt = stem.with_suffix(".json")
    if receipt.exists():
        return load_json(receipt)
    with LOCK:
        if host in REGISTRY_BLOCKED:
            return {"package": package, "url": url, "unknown": "host_blocked_or_throttled"}
        now = time.monotonic()
        remaining = 1.10 - (now - REGISTRY_LAST.get(host, 0))
        if remaining > 0:
            time.sleep(remaining)
        REGISTRY_LAST[host] = time.monotonic()
    stamp = utc_now()
    start = time.monotonic()
    raw = stem.with_suffix(".download")
    cmd = ["curl", "--disable", "--silent", "--show-error", "--compressed", "--max-time", "35",
           "--max-filesize", "32000000", "--user-agent", "AF-RES-019 public research/1.0",
           "--output", str(raw), "--write-out", "%{http_code} %{http_connect} %{size_download}", url]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    http, connect, nbytes = map(int, (proc.stdout or "0 0 0").split())
    row = {"mode": "registry", "package": package, "url": url, "at_utc": stamp,
           "exit_code": proc.returncode, "http_code": http or None, "connect": connect or None,
           "bytes": nbytes, "seconds": round(time.monotonic() - start, 5),
           "requests": 1, "target_min_start_gap_seconds": 1.10}
    if http in (403, 429) or connect == 403:
        with LOCK:
            REGISTRY_BLOCKED.add(host)
    if http == 200 and proc.returncode == 0:
        try:
            row |= registry_metadata(scheme, load_json(raw))
        except (KeyError, ValueError, AttributeError, TypeError) as exc:
            row["unknown"] = "unusable_registry_response:" + type(exc).__name__
    else:
        row["unknown"] = "registry_http_or_transport_failure"
    if raw.exists():
        raw.unlink()
    save_json(receipt, row)
    return row


def registry_metadata(scheme, data):
    versions = {}
    current_inactive, latest = [], None
    sample_license = {}
    if scheme == "npm":
        latest = data.get("dist-tags", {}).get("latest")
        records = data.get("versions", {})
        current_inactive = [v for v, obj in records.items() if obj.get("deprecated")]
        versions = {v: t for v, t in data.get("time", {}).items() if v in records}
        sample_license = {v: str(obj["license"])[:100] for v, obj in records.items()
                          if v in versions and isinstance(obj.get("license"), str)}
    elif scheme == "pypi":
        latest = data.get("info", {}).get("version")
        for version, files in data.get("releases", {}).items():
            times = [f.get("upload_time_iso_8601") or f.get("upload_time") for f in files]
            valid = [value for value in times if value]
            if valid:
                versions[version] = min(valid)
            if files and any(f.get("yanked") for f in files):
                current_inactive.append(version)
    elif scheme == "crates":
        latest = data.get("crate", {}).get("max_version")
        for version in data.get("versions", []):
            versions[version["num"]] = version["created_at"]
            if version.get("yanked"):
                current_inactive.append(version["num"])
            if version.get("license"):
                sample_license[version["num"]] = str(version["license"])[:100]
    elif scheme == "rubygems":
        latest = data[0]["number"] if data else None
        for variant in data:
            version = variant["number"]
            released = variant.get("created_at") or variant.get("built_at")
            if released:
                versions[version] = min(versions.get(version, released), released)
    dated = sorted([[parse_day(v), k] for k, v in versions.items()])
    known_licenses = [[d, v, sample_license[v]] for d, v in dated if v in sample_license]
    changed = sum(prev[2] != curr[2] for prev, curr in zip(known_licenses, known_licenses[1:]))
    return {"dated_versions": dated, "latest_version": latest, "current_inactive_count": len(current_inactive),
            "current_latest_inactive": latest in current_inactive, "visible_license_versions": len(known_licenses),
            "visible_license_transitions": changed, "license_history_caution": "live version metadata can be mutable"}


def warm_registry(rows, scratch):
    directory = scratch / "registry"
    directory.mkdir(exist_ok=True)
    # Per host, a single sequential lane preserves the observed anonymous gap.
    hosts = {}
    for record in rows:
        package = record.get("package")
        if package and package.split(":", 1)[0] in REGISTRY:
            hosts.setdefault(package.split(":", 1)[0], set()).add(package)
    def lane(packages):
        for package in sorted(packages):
            row = open_registry(package, directory)
            print(package, row.get("http_code"), len(row.get("dated_versions", [])), flush=True)
    with ThreadPoolExecutor(max_workers=len(hosts) or 1) as pool:
        list(pool.map(lane, hosts.values()))


def license_family(content):
    text = " ".join(content.lower().split())[:5000]
    for token, family in (
        ("business source license", "BUSL"), ("redis source available license", "RSAL"),
        ("server side public license", "SSPL"), ("elastic license", "Elastic"),
        ("mozilla public license", "MPL"), ("gnu affero general public license", "AGPL"),
        ("gnu general public license", "GPL"), ("apache license", "Apache"),
        ("mit license", "MIT"), ("permission is hereby granted, free of charge", "MIT"),
        ("redistribution and use in source and binary forms", "BSD"),
    ):
        if token in text:
            return family
    return None


def normalize_repo(value):
    if isinstance(value, dict):
        value = value.get("url")
    if not isinstance(value, str) or not value.strip():
        return None
    value = value.strip().lower().removeprefix("git+")
    value = re.sub(r"^(?:ssh://)?git@([^:/]+)[:/]", r"https://\1/", value)
    value = re.sub(r"^(?:git|http)://", "https://", value)
    return value.rstrip("/").removesuffix(".git")


def read_manifest(path, text):
    try:
        if path.endswith("package.json"):
            info = json.loads(text)
            return info.get("name"), normalize_repo(info.get("repository"))
        if path.endswith(("pyproject.toml", "Cargo.toml")):
            info = tomllib.loads(text)
            project = info.get("project") or info.get("package") or info.get("tool", {}).get("poetry", {})
            links = {k.lower(): v for k, v in project.get("urls", {}).items()}
            url = project.get("repository") or links.get("repository") or links.get("source")
            return project.get("name"), normalize_repo(url)
        if path == "go.mod":
            match = re.search(r"^module\s+(\S+)", text, re.M)
            return (match.group(1), None) if match else (None, None)
        if path == "setup.cfg":
            name = re.search(r"^name\s*=\s*(.+)", text, re.M)
            url = re.search(r"^(?:repository|source)\s*=\s*(.+)", text, re.M | re.I)
            return name.group(1).strip() if name else None, normalize_repo(url.group(1)) if url else None
    except (KeyError, ValueError, AttributeError, TypeError):
        pass
    return None, None


def notice_state(text, project):
    matches = []
    project_name = re.split(r"\s+(?:v?\d|self-hosted|community)", project.lower(), maxsplit=1)[0]
    for line in text.splitlines()[:220]:
        phrase = NOTICE.search(line)
        if not phrase:
            continue
        low = line.lower().replace("**", "").replace("`", "")
        heading = line.lstrip().startswith("#")
        self_named = len(project_name) > 2 and bool(re.search(r'(?<!\w)' + re.escape(project_name) + r'(?!\w)', low)) and not any(x in low for x in ("changelog", "version of"))
        full_text = TARGET.search(low) is not None
        if (heading or self_named or full_text) and not re.search(r"\bnot (?:yet )?(?:deprecated|archived|unmaintained)\b", low):
            matches.append(phrase.group(1).casefold())
    return sorted(set(matches))


def latest_day(values, day):
    idx = bisect_right(values, day) - 1
    return (idx, values[idx]) if idx >= 0 else (-1, None)


def first_parent(repo, head):
    text = git_text(repo, ["log", "--first-parent", "--format=%ct%x09%H", head], timeout=110)
    stamped = [row.split("\t") for row in text.splitlines()]
    return [(day_of(stamp), sha) for stamp, sha in sorted(reversed(stamped), key=lambda r: int(r[0]))]


def first_parent_path_changes(repo, head, span):
    keys = ["readme*", "docs/readme*", "license*", "licence*", "copying*", "cla*",
            ".github/cla*", "contributor-license*", ".github/contributor-license*",
            "package.json", "pyproject.toml", "setup.cfg", "Cargo.toml", "go.mod",
            "directus/package.json", "packages/react-dom/package.json"]
    out = git_text(repo, ["log", "--first-parent", "--diff-merges=first-parent", "--no-renames",
                          "--format=%x1e%ct%x09%H", "--name-status",
                          "--since-as-filter=" + end_of_day(span[0] - 1),
                          "--until=" + end_of_day(span[1]), head, "--",
                          *[":(icase,glob)" + k for k in keys]], timeout=100)
    changes = []
    for block in out.split("\x1e"):
        lines = [x for x in block.splitlines() if x]
        if not lines:
            continue
        stamp, sha = lines[0].split("\t")
        pairs = [x.split("\t", 1) for x in lines[1:] if "\t" in x]
        changes.append((day_of(stamp), sha, pairs))
    return sorted(changes, key=lambda x: x[0])


def root_markers(repo, head):
    return git_text(repo, ["ls-tree", "--name-only", head]).splitlines()


def file_paths(repo, head, package=None):
    files = root_markers(repo, head)
    readme = next((x for x in files if x.lower() in ("readme.md", "readme.rst", "readme")), None)
    if not readme:
        readme = next((x for x in files if x.lower().startswith("readme")), None)
    manifest = next((x for x in MANIFEST_NAMES if x in files), None)
    if package == "npm:react-dom":
        manifest = "packages/react-dom/package.json"
    if package == "npm:directus" and "directus" in files:
        manifest = "directus/package.json"
    license_file = next((x for x in files if PATH_LICENSE.fullmatch(x)), None)
    return readme, manifest, license_file


def snapshot_set(repo, snapshots, package, project, traffic):
    """Read selected historical files only, batching promisor blob IDs when possible."""
    related = {}
    for sha in dict.fromkeys(snapshots.values()):
        if not sha:
            continue
        paths = file_paths(repo, sha, package)
        concrete = [p for p in paths if p]
        listing = git_text(repo, ["ls-tree", "--full-tree", sha, "--", *concrete]) if concrete else ""
        blobs = {}
        for row in listing.splitlines():
            info, name = row.split("\t", 1)
            _, kind, obj = info.split()
            if kind == "blob":
                blobs[name] = obj
        related[sha] = (paths, blobs)
    oid_refs = {oid: (sha, path) for sha, (_, by_name) in related.items() for path, oid in by_name.items()}
    if oid_refs:
        # Known tree references from the clone; one public fetch may replace many lazy fetches.
        git(repo, ["fetch", "--no-tags", "--no-write-fetch-head", "--filter=blob:none",
                   "origin", *oid_refs], traffic, timeout=45, check=False)
    texts = {}
    for oid, (sha, path) in oid_refs.items():
        code, content = git(repo, ["show", f"{sha}:{path}"], traffic, timeout=20, check=False)
        texts[oid] = content.decode("utf-8", errors="replace")[:180_000] if code == 0 else None
    result = {}
    for day, sha in snapshots.items():
        if not sha:
            continue
        paths, by_name = related[sha]
        readme, manifest, lic = (texts.get(by_name.get(p)) for p in paths)
        name, repository = read_manifest(paths[1], manifest) if manifest is not None else (None, None)
        result[day] = {"sha": sha, "paths": paths, "readme_exists": readme is not None,
                       "notices": notice_state(readme, project) if readme is not None else None,
                       "raw_notice": bool(NOTICE.search(readme)) if readme is not None else None,
                       "manifest": [name, repository], "license": license_family(lic) if lic is not None else None,
                       "readme_digest": hashlib.sha256(readme.encode()).hexdigest() if readme is not None else None,
                       "license_digest": hashlib.sha256(lic.encode()).hexdigest() if lic is not None else None}
    return result


def timeline_days(t, end):
    first = previous_months(date.fromordinal(t), 12).toordinal()
    return first, min(t + 365, end)


def scoped_git(repo, row, t, end, match, receipt):
    head = receipt["head"]
    first, last = timeline_days(t, end)
    genesis = parse_day(match["first_commit_date"])
    baseline = git_text(repo, ["log", "--no-merges", "--format=%ct%x09%aE",
                               "--since-as-filter=" + end_of_day(first - 366),
                               "--until=" + end_of_day(last), head], timeout=100)
    rows = parse_commit_rows(baseline)
    preceding = git_text(repo, ["log", "-1", "--no-merges", "--format=%ct",
                                "--before=" + end_of_day(first - 366), head]).strip()
    if preceding:
        rows.insert(0, (day_of(preceding), None))
    traffic = []
    tags_code, _ = git(repo, ["fetch", "--tags", "--no-write-fetch-head", "--filter=blob:none", "origin"],
                       traffic, timeout=150, check=False)
    tags = []
    if tags_code == 0:
        ref_tags = git_text(repo, ["for-each-ref", "--format=%(creatordate:unix)%09%(refname:short)", "refs/tags"])
        tags = sorted(day_of(stamp) for stamp, tag in
                      (line.split("\t", 1) for line in ref_tags.splitlines())
                      if stamp.isdigit() and VERSION_TAG.match(tag))
    points = first_parent(repo, head)
    point_days = [p[0] for p in points]
    changes = first_parent_path_changes(repo, head, (first - 366, last))
    license_days, cla_days, extra_readme = set(), set(), set()
    for day, _, paths in changes:
        if day > genesis and any(PATH_LICENSE.fullmatch(p) for _, p in paths):
            license_days.add(day)
        if any(status == "A" and PATH_CLA.search(path) for status, path in paths):
            cla_days.add(day)
        if len(extra_readme) < 24 and first <= day <= last and any("readme" in p.lower() for _, p in paths):
            extra_readme.add(day)
    evaluation = {first, t - 1, t, t + 1, last,
                  *[previous_months(date.fromordinal(t), m).toordinal() for m in WINDOWS],
                  *extra_readme}
    checkpoint = {d for d in evaluation | {first - 365, *(v - 365 for v in evaluation)} if d <= last}
    refs = {}
    for day in sorted(checkpoint):
        idx, _ = latest_day(point_days, day)
        refs[day] = points[idx][1] if idx >= 0 else None
    snapshots = snapshot_set(repo, refs, row.get("package"), row["project"], traffic)
    risk = {}
    for day in sorted(evaluation & set(snapshots)):
        current = snapshots[day]
        past = snapshots.get(day - 365)
        differences = [x != y for x, y in zip(current["manifest"], past["manifest"])
                       if x is not None and y is not None] if past else []
        risk[day] = {"git_readme_notice": int(bool(current["notices"])) if current["notices"] is not None else None,
                     "git_package_changed": int(any(differences)) if differences else None}
    features = {"head": head, "repo_first_day": genesis, "tags": tags,
                "license_days": sorted(license_days), "cla_days": sorted(cla_days), "tag_fetch_exit": tags_code}
    return features, rows, risk, snapshots, traffic


def daily_values(first, last, features, rows, snapshot_risks, registry):
    git_available = features is not None
    ckpt_dates = sorted(snapshot_risks)
    tags = features["tags"] if git_available else []
    license_days = features["license_days"] if git_available else []
    cla_days = features["cla_days"] if git_available else []
    releases = [r[0] for r in registry.get("dated_versions", [])]
    day90, day365, authors = deque(), deque(), Counter()
    cursor, newest = 0, None
    history = {key: [] for key in SIGNALS}
    for day in range(first, last + 1):
        values = dict.fromkeys(SIGNALS)
        while cursor < len(rows) and rows[cursor][0] <= day:
            record = rows[cursor]
            day90.append(record[0])
            day365.append(record)
            authors[record[1]] += 1
            newest = record[0]
            cursor += 1
        while day90 and day90[0] <= day - 90:
            day90.popleft()
        while day365 and day365[0][0] <= day - 365:
            _, author = day365.popleft()
            authors[author] -= 1
            if authors[author] == 0:
                del authors[author]
        if git_available and day >= features["repo_first_day"]:
            ti, tag = latest_day(tags, day)
            _, lic = latest_day(license_days, day)
            _, cla = latest_day(cla_days, day)
            _, cs = latest_day(ckpt_dates, day)
            values.update({
                "git_commits_90d": len(day90),
                "git_commit_age": day - newest if newest is not None else None,
                "git_authors_365d": len(authors) if None not in authors else None,
                "git_top_author_share": round(max(authors.values()) / len(day365), 8)
                                        if day365 and None not in authors else None,
                "git_tag_age": day - tag if tag is not None else None,
                "git_tag_gap": tag - tags[ti - 1] if ti >= 1 else None,
                "git_license_change": int(lic is not None and lic > day - 90),
                "git_cla_added": int(cla is not None and cla > day - 365),
            })
            if cs is not None:
                values.update(snapshot_risks[cs])
        ri, release = latest_day(releases, day)
        if ri >= 1:
            values["registry_release_gap"] = release - releases[ri - 1]
        for key, value in values.items():
            if not history[key] or history[key][-1][1] != value:
                history[key].append([day, value])
    return history


def signal_value(history, key, day):
    timeline = history.get(key, ())
    i = bisect_right(timeline, day, key=lambda x: x[0]) - 1
    return timeline[i][1] if i >= 0 else None


def collect_item(row, event, facts, scratch, end):
    stamp = utc_now()
    item_id = row["id"]
    url = row.get("repo_url")
    cache = scratch / "repos"
    directory = scratch / "registry"
    item_dir = scratch / "items"
    saved = item_dir / (item_id + ".json")
    if saved.exists():
        return load_json(saved)
    features, commits, paths, snapshots, traffic, repo_receipt = None, [], {}, {}, [], None
    outcome = {"id": item_id, "at_utc": stamp, "scope": event["category"]}
    t = event.get("effective_date")
    registry = open_registry(row.get("package"), directory)
    if url:
        path, repo_receipt = prepare_repo(url, cache)
    outcome["clone"] = repo_receipt
    outcome["registry"] = {k: v for k, v in registry.items() if k != "dated_versions"}
    if not t:
        outcome["unknown"] = "exact_event_date_missing"
        outcome["history"] = {}
    else:
        t = parse_day(t)
        first, last = timeline_days(t, end)
        match = facts[row.get("candidate_id", item_id)]
        git_started = time.monotonic()
        if url and repo_receipt["exit_code"] == 0 and "first_commit_date" in match:
            try:
                features, commits, paths, snapshots, traffic = scoped_git(path, row, t, end, match, repo_receipt)
            except (OSError, ValueError, RuntimeError) as exc:
                outcome["git_unknown"] = str(exc)
        else:
            outcome["git_unknown"] = match.get("unknown", "repo_not_applicable")
        outcome["history"] = daily_values(first, last, features, commits, paths, registry)
        outcome["first"], outcome["last"] = first, last
        outcome["features"] = features
        outcome["text_checks"] = {at_date(d): s for d, s in snapshots.items() if d >= first}
        outcome["git_overhead"] = {"wall_seconds": round(time.monotonic() - git_started, 5),
                                   "operations": len(traffic), "requests": sum(r["requests"] for r in traffic),
                                   "bytes": sum(r["bytes"] for r in traffic),
                                   "seconds": round(sum(r["seconds"] for r in traffic), 5),
                                   "nonzero": sum(bool(r["exit_code"]) for r in traffic)}
    save_json(saved, outcome)
    print("signals", item_id, outcome.get("git_unknown", "ok"), flush=True)
    return outcome


def missing_reason(key, outcome, point):
    if not outcome.get("history"):
        return "exact_event_date_missing"
    if point > outcome["last"]:
        return "right_censored"
    if key == "registry_inactive":
        return "historical_flag_timestamp_unavailable"
    if key == "registry_license_changed":
        return "historical_metadata_revision_unverified"
    if key == "registry_release_gap" and outcome["registry"].get("unknown"):
        return outcome["registry"]["unknown"]
    if key.startswith("git") and outcome.get("git_unknown"):
        return outcome["git_unknown"]
    if key in {"git_tag_age", "git_tag_gap"} and (outcome.get("features") or {}).get("tag_fetch_exit"):
        return "remote_tags_fetch_failed"
    if outcome.get("features") and point < outcome["features"]["repo_first_day"] and key.startswith("git"):
        return "before_first_reachable_commit"
    return "required_versions_or_file_or_authors_unavailable"


def collect_all(rows, events, facts, scratch, jobs, end, output):
    for d in ("registry", "items"):
        (scratch / d).mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        records = list(pool.map(lambda row: collect_item(row, events[row.get("matched_event", row["id"])],
                                                         facts, scratch, end), rows))
    (output / "signals").mkdir(exist_ok=True)
    (output / "results").mkdir(exist_ok=True)
    with (output / "signals/SIGNALS.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["item", "group", "matched_event", "signal", "timepoint", "as_of_utc", "value",
                         "collected_at_utc", "source", "missing_reason"])
        for row, observed in zip(rows, records):
            ev = events[row.get("matched_event", row["id"])]
            for months in WINDOWS:
                point = previous_months(date.fromisoformat(ev["effective_date"]), months).toordinal() if ev["effective_date"] else None
                for key, (origin, _, _) in SIGNALS.items():
                    v = signal_value(observed["history"], key, point) if point else None
                    writer.writerow([row["id"], "control" if "matched_event" in row else "event", ev["id"], key,
                                     f"T-{months}m", at_date(point) if point else "", v,
                                     observed["at_utc"], origin,
                                     ("" if v is not None else missing_reason(key, observed, point))])
    compressed = json.dumps({r["id"]: r["history"] for r in records}, ensure_ascii=False,
                            separators=(",", ":")).encode()
    (output / "signals/DAYS.json.gz").write_bytes(gzip.compress(compressed, mtime=0))
    save_json(output / "signals/DETAILS.json", [{k: v for k, v in r.items() if k not in
                                                          {"history", "git_overhead", "clone"}} for r in records])
    save_json(output / "results/collection-receipts.json", [
        {k: r.get(k) for k in ("id", "at_utc", "clone", "registry", "git_overhead", "unknown", "git_unknown")}
        for r in records])
    return records

def main():
    parser = ArgumentParser()
    parser.add_argument("--scratch", required=True, type=Path)
    parser.add_argument("--jobs", type=int, default=5)
    parser.add_argument("--match", action="store_true")
    parser.add_argument("--registry", action="store_true")
    parser.add_argument("--signals", action="store_true")
    parser.add_argument("--end", default="2026-11-20", help="UTC observation cutoff for timeline")
    parser.add_argument("--output", type=Path, default=STUDY)
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    cache = args.scratch / "repos"
    cache.mkdir(exist_ok=True)
    records = load_json(STUDY / "events/EVENTS.json")
    events = {e["id"]: e for e in records}
    candidates = load_json(STUDY / "controls/CANDIDATES.json")
    if args.match:
        match_all([*records, *candidates], events, cache, args.scratch, args.jobs)
    if args.registry:
        warm_registry([*records, *candidates], args.scratch)
    if args.signals:
        controls = load_json(STUDY / "controls/CONTROLS.json")
        facts = {r["id"]: r for r in load_json(args.scratch / "matching.json")}
        collect_all([*records, *controls], events, facts, args.scratch, args.jobs,
                    parse_day(args.end), args.output)


if __name__ == "__main__":
    main()
