"""Acquire fixed release sources and produce predictions without loading package code."""
import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

from lxml import html

from common import (
    Fetcher, GIT_API, PACKAGE, ROOT, UPSTREAM, archive, git, json_in, sha, utc, write_csv, write_json, write_jsonl,
)

FUNCTIONS = ("quantile", "median")
VERSIONS = re.compile(r"(?m)^#{1,6}[ \t]+\[?v?(\d+\.\d+\.\d+)(?=[\]\s]|$)")
KEYWORDS = re.compile(
    r"(?<![A-Za-z0-9_])(?:quantile|quantiles|quantileSorted|quantileRank|quantileRankSorted|"
    r"percentile|percentiles|percentileRank|median|medians|medianSorted|"
    r"quartile|quartiles|interquartile|interquartileRange|IQR|interpolation|interpolate|interpolated)"
    r"(?![A-Za-z0-9_])", re.IGNORECASE,
)
DEP_FIELDS = ("dependencies", "optionalDependencies", "peerDependencies")
CONDITIONS = ("require", "node", "node-addons", "module-sync", "default")


def matched_words(text):
    text = re.sub(r"https?://[^\s)>\]]+", "", text)
    return sorted({hit.group().lower() for hit in KEYWORDS.finditer(text)})


def release_index(fetcher):
    api_url = GIT_API + "/releases?per_page=100&page=1"
    api, api_receipt = fetcher.get(api_url)
    if api and not api_receipt["link"]:
        data = json.loads(api)
        return {
            item["tag_name"]: {"url": item["html_url"], "published": item["published_at"],
                "updated": item.get("updated_at"), "immutable_now": item.get("immutable"),
                "bytes": len((item["body"] or "").encode()), "hits": matched_words(item["body"] or ""),
                "body_sha256": sha((item["body"] or "").encode()), "body_locator": "REST body"}
            for item in data if not item.get("draft")
        }, {"route": "REST", "complete_current_list": True, "pages": [api_receipt]}
    url = UPSTREAM + "/releases"
    visited, receipts, releases = set(), [api_receipt], {}
    while url:
        if url in visited or len(visited) >= 20:
            break
        visited.add(url)
        raw, receipt = fetcher.get(url)
        receipts.append(receipt)
        if not raw:
            break
        page = html.fromstring(raw)
        notices = page.xpath("//section[.//a[contains(@href, '/releases/tag/')]]")
        if not notices:
            break
        for section in notices:
            href = section.xpath(".//a[contains(@href, '/releases/tag/')]/@href")[0]
            tag = urllib.parse.unquote(href.rsplit("/", 1)[-1])
            date_nodes = section.xpath(".//relative-time[contains(@class, 'no-wrap')]/@datetime")
            body_nodes = section.xpath(".//*[@data-test-selector='body-content']")
            body = "\n".join(node.text_content() for node in body_nodes)
            locator = "release card .markdown-body"
            releases[tag] = {"url": urllib.parse.urljoin(url, href), "published": date_nodes[0] if date_nodes else None,
                             "updated": None, "immutable_now": None, "bytes": len(body.encode()),
                             "hits": matched_words(body), "body_sha256": sha(body.encode()), "body_locator": locator}
        next_page = page.xpath("//a[@rel='next']/@href")
        url = urllib.parse.urljoin(url, next_page[0]) if next_page else None
    return releases, {"route": "HTML", "complete_current_list": url is None, "pages": receipts}


def earlier_or_equal(left, right):
    return datetime.fromisoformat(left) <= datetime.fromisoformat(right)


def notice(files, version, published, releases, list_complete, tag, tarball):
    github = next((releases[k] for k in (tag, "v" + version, version, PACKAGE + "@" + version) if k in releases), None)
    gh = "no_current_listing" if list_complete else "index_unavailable"
    if github:
        if not github["published"]:
            gh = "publication_unknown"
        elif not earlier_or_equal(github["published"], published):
            gh = "published_after_npm"
        elif github["updated"] and earlier_or_equal(github["updated"], published):
            gh = "verified_by_npm_time"
        else:
            gh = "body_at_npm_time_unknown"

    changelog_path = next((path for path in files if re.fullmatch(r"change[-_ ]?log(?:\.[^.]+)?", path, re.I)), "")
    bundled = {"status": "not_packaged", "path": None, "url": tarball, "bytes": 0, "hits": [], "lines": []}
    if changelog_path:
        raw = files[changelog_path]
        bundled.update(path=changelog_path, bytes=len(raw), sha256=sha(raw), status="missing_version_boundary")
        text = raw.decode()
        headings = list(VERSIONS.finditer(text))
        for position, head in enumerate(headings):
            if head.group(1) == version:
                end = headings[position + 1].start() if position + 1 < len(headings) else len(text)
                section = text[head.start():end]
                bundled.update(status="verified_at_npm_time", hits=matched_words(text[head.end():end]),
                               lines=[text.count("\n", 0, head.start()) + 1, text.count("\n", 0, end)],
                               section_sha256=sha(section.encode()), section_bytes=len(section.encode()))
                break
    force = gh in {"index_unavailable", "publication_unknown", "body_at_npm_time_unknown"} or bundled["status"] == "missing_version_boundary"
    at_time = bundled["hits"] + (github["hits"] if gh == "verified_by_npm_time" else [])
    return {"github_status": gh, "github": github, "bundled": bundled, "hits_at_npm": sorted(set(at_time)),
            "force": force, "current_only_absence": gh == "no_current_listing" and bundled["status"] == "not_packaged",
            "cutoff_utc": published}


def get_entry(manifest, files):
    rule = manifest.get("exports")
    if isinstance(rule, dict) and "." in rule:
        rule = rule["."]
    while isinstance(rule, dict):
        choice = next((key for key in rule if key in CONDITIONS), None)
        rule = rule.get(choice) if choice else rule.get("import")
    candidate = (rule or manifest.get("main") or "index.js").removeprefix("./")
    for path in (candidate, candidate + ".js", candidate.rstrip("/") + "/index.js"):
        if path in files:
            return path
    return None


def elapsed(command, folder, cache):
    env = os.environ | {"LANG": "C.UTF-8", "TZ": "UTC", "npm_config_cache": str(cache), "npm_config_update_notifier": "false"}
    start = time.perf_counter()
    result = subprocess.run(command, cwd=folder, env=env, capture_output=True, text=True, timeout=60, check=False)
    return result, (time.perf_counter() - start) * 1000


def make_lock(folder, version, dist, manifest, cache):
    package_json = {"name": "af-res-139-probe", "version": "1.0.0", "private": True, "dependencies": {PACKAGE: dist["tarball_url"]}}
    write_json(folder / "package.json", package_json)
    result, wall = elapsed(["npm", "install", "--package-lock-only", "--ignore-scripts", "--no-audit", "--no-fund"], folder, cache)
    if result.returncode:
        raise ValueError(f"{version} npm lock failed: {result.stderr}")
    lock = json_in(folder / "package-lock.json")
    pin = lock["packages"]["node_modules/" + PACKAGE]
    assert lock["lockfileVersion"] == 3 and pin["version"] == version and pin["resolved"] == dist["tarball_url"]
    if dist["integrity"]:
        assert pin["integrity"] == dist["integrity"]
    dependencies = {}
    for field in DEP_FIELDS:
        for name, requirement in manifest.get(field, {}).items():
            locations = [f"node_modules/{PACKAGE}/node_modules/{name}", f"node_modules/{name}"]
            resolved = next((lock["packages"][p] for p in locations if p in lock["packages"]), None)
            dependencies[name] = {"field": field, "range": requirement, "version": resolved["version"] if resolved else None,
                                  "integrity": resolved.get("integrity") if resolved else None}
    return {"package_json": package_json, "lock": lock, "lock_sha256": sha((folder / "package-lock.json").read_bytes()),
            "direct": dependencies, "lock_wall_ms": wall, "lock_stderr": result.stderr.strip()}


def doc_section(upstream, commit, files, function):
    path = "src/" + function + ".js"
    now = utc()
    time_start = time.perf_counter()
    cpu_start = time.process_time()
    raw = git(upstream, "show", commit + ":" + path, missing=True) if commit else None
    locator = {"path": path, "url": f"{UPSTREAM}/blob/{commit}/{path}" if commit else None,
               "opened_utc": now, "bytes": len(raw) if raw else None,
               "acquisition": "git show at tag commit; bytes exclude Git pack transport"}
    pattern = re.compile(r"/\*\*(?:(?!\*/)[\s\S])*\*/\s*(?=(?:export\s+(?:default\s+)?)?function\s+"
                         + function + r"\s*\()")
    match = pattern.search(raw.decode()) if raw else None
    if not match:
        return locator | {"status": "unresolved", "reason": "missing tag-linked target JSDoc"}
    section = match.group().rstrip()
    text = section.removeprefix("/**").removesuffix("*/")
    cleaned = [re.sub(r"^\s*\*\s?", "", line).strip() for line in text.splitlines()]
    normalized = " ".join(" ".join(line.split()) for line in cleaned if line and
                          not re.fullmatch(r"(?:generated|(?:version\s+|v)\d+\.\d+\.\d+)", line, re.I))
    row = locator | {
        "lines": [raw.decode().count("\n", 0, match.start()) + 1, raw.decode().count("\n", 0, match.start() + len(section)) + 1],
        "raw_doc_sha256": sha(raw), "raw_section_sha256": sha(section.encode()), "text_sha256": sha(normalized.encode()),
        "section_bytes": len(section.encode()), "status": "resolved" if files.get(path) == raw else "unresolved",
        "availability": "packaged_file_identical_at_publish" if files.get(path) == raw else "tag_document_differs_from_or_absent_in_tar",
        "read_wall_ms": (time.perf_counter() - time_start) * 1000, "hash_cpu_ms": (time.process_time() - cpu_start) * 1000,
    }
    row["reason"] = "" if row["status"] == "resolved" else "tag JSDoc time uncorroborated by packaged file"
    return row


def source_bytes(files, paths):
    return [{"path": path, "bytes": len(files[path]), "sha256": sha(files[path])} for path in dict.fromkeys(paths)
            if path and path in files]


def git_publish_data(upstream, version, row, files, entry):
    tag = "v" + version
    obj = git(upstream, "rev-parse", "--verify", "refs/tags/" + tag, missing=True)
    if not obj:
        return {"tag": tag, "tag_status": "missing_tag", "tag_commit": None}
    commit = git(upstream, "rev-parse", "refs/tags/" + tag + "^{commit}").decode().strip()
    stamp = git(upstream, "for-each-ref", "--format=%(taggerdate:iso-strict)", "refs/tags/" + tag).decode().strip()
    commit_stamp = git(upstream, "show", "-s", "--format=%cI", commit).decode().strip()
    git_head = row.get("git_head")
    paths = ("package.json", "README.md", "CHANGELOG.md", "index.js", "index.d.ts",
             "src/quantile.js", "src/median.js", "src/quantile_sorted.js", "src/quickselect.js", entry)
    compare = {}
    for path in dict.fromkeys(paths):
        if not path:
            continue
        upstream_raw = git(upstream, "show", commit + ":" + path, missing=True)
        tar_raw = files.get(path)
        if upstream_raw is not None and tar_raw is not None:
            compare[path] = "equal" if upstream_raw == tar_raw else "different"
        else:
            compare[path] = "tag_only" if upstream_raw is not None else "tar_only" if tar_raw is not None else "absent_both"
    offset = (datetime.fromisoformat(row["publish_utc"]) - datetime.fromisoformat(stamp or commit_stamp)).total_seconds()
    return {"tag": tag, "tag_commit": commit, "tag_object": obj.decode().strip(), "tagger_time": stamp or None,
            "tag_commit_time": commit_stamp, "publish_minus_tag_clock_seconds": offset,
            "tag_status": "gitHead_missing" if not git_head else "match" if git_head == commit else "different_from_gitHead",
            "tag_file_comparison": compare}


def predict_version(row, args, fetcher, releases, list_complete):
    version = row["version"]
    work = args.work / version
    work.mkdir()
    raw, fetched = fetcher.get(row["tarball_url"])
    files, manifest, integrity = archive(raw, row, version)
    entry = get_entry(manifest, files)
    provenance = git_publish_data(args.upstream, version, row, files, entry)
    lock = make_lock(work, version, row, manifest, args.lock_cache)
    status = notice(files, version, row["publish_utc"], releases, list_complete, provenance["tag"], row["tarball_url"])
    src_work = work / "package-text"
    src_work.mkdir()
    for name, content in files.items():
        if name.startswith("src/") or name in (entry, (entry or "") + ".map"):
            target = (src_work / name).resolve()
            if not target.is_relative_to(src_work.resolve()):
                raise ValueError(f"unsafe archive path {name}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    start = time.perf_counter()
    call = subprocess.run(["node", str(ROOT / "replay/fingerprint.cjs"), str(src_work), entry or "",
                           str(args.parser)], capture_output=True, text=True, timeout=15, check=True)
    elapsed_ms = (time.perf_counter() - start) * 1000
    functions = json.loads(call.stdout)
    detail = []
    for name in FUNCTIONS:
        doc = doc_section(args.upstream, provenance["tag_commit"], files, name)
        func = functions[name]
        implementation = "src/" + name + ".js" if "src/" + name + ".js" in files else entry
        broad = source_bytes(files, [entry, implementation])
        narrow = source_bytes(files, [
            entry, func.get("map_path"), implementation,
            *[item["path"] for item in func.get("delegates", {}).values()]
        ])
        detail.append({"version": version, "function": name, "npm_utc": row["publish_utc"],
                       "tarball": fetched, "doc": doc, "broad_files": broad, "function_body": func,
                       "narrow_files": narrow, "notice": status, "entry": entry, "static_node_wall_ms": elapsed_ms,
                       "direct": lock["direct"], "hashed_utc": utc()})
    return row | provenance | {
        "archive_status": "verified", "archive_bytes": len(raw), "archive_sha256": fetched["sha256"],
        "verified_sha1": integrity.get("sha1"), "verified_sha512": integrity.get("sha512"), "entry": entry,
        "entry_sha256": sha(files[entry]) if entry else None, "entry_bytes": len(files[entry]) if entry else None,
        "manifest_main": manifest.get("main"), "manifest_module": manifest.get("module"),
        "manifest_exports": manifest.get("exports"), "manifest_type": manifest.get("type"),
        "direct": lock["direct"], "lock_sha256": lock["lock_sha256"], "archive_opened_utc": fetched["opened_utc"],
    }, detail, lock


def summarize_pair(left, right):
    reasons = {}
    prev_doc, doc = left["doc"], right["doc"]
    if {prev_doc["status"], doc["status"]} != {"resolved"} or prev_doc["path"] != doc["path"]:
        reasons["C"] = ("force", "fixed_docs_unresolved_or_moved")
    else:
        change = prev_doc["text_sha256"] != doc["text_sha256"]
        reasons["C"] = ("run" if change else "skip", "normalized_docs_changed" if change else "")
    d_paths = lambda x: [value["path"] for value in x["broad_files"]]
    if reasons["C"][0] == "force" or any(not side["entry"] for side in (left, right)) or d_paths(left) != d_paths(right) or any(
        dep["version"] is None for side in (left, right) for dep in side["direct"].values()):
        reasons["D"] = ("force", "docs_entry_path_or_lock_unresolved")
    else:
        change = reasons["C"][0] == "run" or left["broad_files"] != right["broad_files"] or left["direct"] != right["direct"]
        reasons["D"] = ("run" if change else "skip", "docs_entry_impl_or_lock_changed" if change else "")
    a, b = left["function_body"], right["function_body"]
    root_changed = a.get("root", {}).get("token_sha256") != b.get("root", {}).get("token_sha256")
    delegates_changed = ({k: v["token_sha256"] for k, v in a.get("delegates", {}).items()} !=
                         {k: v["token_sha256"] for k, v in b.get("delegates", {}).items()})
    if {a["status"], b["status"]} != {"resolved"}:
        reasons["F"] = ("force", "function_or_delegate_unresolved")
    else:
        changed = root_changed or delegates_changed
        reasons["F"] = ("run" if changed else "skip", "root_or_direct_delegate_tokens_changed" if changed else "")
    notice_data = right["notice"]
    reasons["N"] = ("force", "notice_at_publication_unconfirmed") if notice_data["force"] else (
        ("run", "notice_word_at_publication") if notice_data["hits_at_npm"] else ("skip", ""))
    reasons["E"] = best([reasons["F"], reasons["N"]])
    return reasons, root_changed, delegates_changed


def best(states):
    weights = {"skip": 0, "run": 1, "force": 2, "initial": 3}
    high = max(states, key=lambda state: weights[state[0]])[0]
    return high, "+".join(sorted({reason for pair, reason in states if reason and pair == high}))


def pair_rows(pop, details):
    lookup = {(d["version"], d["function"]): d for d in details}
    policies = ("A", "C", "D", "E", "F", "N")
    for order in ("publish", "semver"):
        sequence = pop["published_order" if order == "publish" else "semver_order"]
        for position, version in enumerate(sequence):
            previous = sequence[position - 1] if position else None
            summaries = {}
            base = {"order": order, "previous": previous, "version": version, "rank": position + 1}
            for name in FUNCTIONS:
                right = lookup[version, name]
                summaries[name] = (
                    summarize_pair(lookup[previous, name], right) if previous else
                    ({policy: ("initial", "first_measurement") for policy in policies}, None, None)
                )
                states, root, delegates = summaries[name]
                states.setdefault("A", ("run", "always"))
                yield base | {
                    "function": name, **{p: states[p][0] for p in policies}, **{p + "_reason": states[p][1] for p in policies},
                    "root_token_difference": root, "delegate_token_difference": delegates,
                    "cutoff_utc": right["npm_utc"], "signal_as_of_utc": max(right["npm_utc"], lookup[previous, name]["npm_utc"]) if previous else right["npm_utc"],
                    "fingerprinted_utc": right["hashed_utc"], "doc_url": right["doc"]["url"],
                    "archive_url": right["tarball"]["url"], "notice_url": (right["notice"]["github"] or {}).get("url"),
                    "notice_status": right["notice"]["github_status"], "changelog_status": right["notice"]["bundled"]["status"],
                    "current_only_absence": right["notice"]["current_only_absence"],
                    "notice_words": " ".join(right["notice"]["hits_at_npm"]),
                    "F_status": right["function_body"]["status"],
                    "F_relation": right["function_body"].get("relation"),
                }
            pack_states = {policy: best([summaries[name][0][policy] for name in FUNCTIONS]) for policy in policies}
            yield base | {"function": "any", **{p: pack_states[p][0] for p in policies},
                          **{p + "_reason": pack_states[p][1] for p in policies}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("cache", "upstream", "work", "parser", "lock-cache"):
        parser.add_argument("--" + arg, required=True, type=lambda value: Path(value).resolve())
    args = parser.parse_args()
    args.work.mkdir()
    pop = json_in(ROOT / "evidence/roster.json")
    selected = sorted((row for row in pop["catalog"] if row["status"] == "included"), key=lambda row: row["publish_rank"])
    fetcher = Fetcher(args.cache)
    releases, receipts = release_index(fetcher)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        tasks = [pool.submit(predict_version, row, args, fetcher, releases, receipts["complete_current_list"]) for row in selected]
        observations = [task.result() for task in tasks]
    observed = {release["version"]: release for release, _, _ in observations}
    details = [detail for _, records, _ in observations for detail in records]
    locks = {release["version"]: lock for release, _, lock in observations}
    released_rows = list(observed.values()) + [r for r in pop["catalog"] if r["status"] != "included"]
    catalog_versions = {r["version"] for r in pop["catalog"]}
    for tag in git(args.upstream, "tag", "--list").decode().splitlines():
        if not re.fullmatch(r"v\d+\.\d+\.\d+", tag) or tag[1:] in catalog_versions:
            continue
        ref = git(args.upstream, "show", "-s", "--format=%H %cI", tag + "^{commit}").decode().strip().split()
        if earlier_or_equal(pop["start"], ref[1]) and earlier_or_equal(ref[1], pop["end_exclusive"]):
            released_rows.append({"version": tag[1:], "tag": tag, "tag_commit": ref[0], "tag_commit_time": ref[1],
                                  "status": "upstream_tag_without_registry_row"})
    for row in released_rows:
        for name in ("tag_file_comparison", "direct", "manifest_exports"):
            if row.get(name) is not None:
                row[name] = json.dumps(row[name], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    write_csv(ROOT / "releases.csv", released_rows)
    write_csv(ROOT / "signals.csv", list(pair_rows(pop, details)))
    write_jsonl(ROOT / "evidence/signal-components.jsonl", details)
    write_json(ROOT / "evidence/release-index.json", receipts | {
        "visible_tags": list(releases), "included_listed_tags": [tag for tag in releases if tag.removeprefix("v") in observed],
        "opened_tarballs": len(observed), "tarball_body_bytes": sum(row["archive_bytes"] for row in observed.values()),
        "historical_absence_limit": "current official index cannot establish that an older release was not removed",
    })
    write_json(ROOT / "replay/locks.json", {"tool": "npm 11.9.0", "current_lockfile_version": 3, "versions": locks})
    print(f"predicted {len(observed)} releases; {len(details)} function snapshots; {len(releases)} public release cards")


if __name__ == "__main__":
    main()
