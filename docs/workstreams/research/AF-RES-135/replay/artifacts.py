"""Acquire release artifacts and record document observations without executing package code."""
import argparse
import base64
import concurrent.futures
import csv
import datetime as dt
import hashlib
import io
import json
import pathlib
import re
import subprocess
import sys
import tarfile
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = "https://registry.npmjs.org"
RAW = "https://raw.githubusercontent.com"
GITHUB = "https://github.com"
PRE = "5cf6899ec26ec40045a62b4352076477793bd45a"
OL_PREFIX = f"{PRE}:docs/workstreams/research/AF-RES-131/"
OL_SOURCE = "src/ol/interaction/Translate.js"
OL_EXAMPLE = "examples/translate-features.html"
OL_TAR = {
    "interaction/Translate.js", "interaction.js", "interaction/Pointer.js", "Map.js",
    "Collection.js", "Feature.js", "geom/SimpleGeometry.js", "events/condition.js",
    "functions.js", "css.js", "MapBrowserEventType.js",
}
D3_SECTIONS = ("scaleLinear", "continuous", "continuous_invert", "continuous_clamp", "continuous_unknown")
D3_PACKAGES = ("d3-array", "d3-collection", "d3-color", "d3-format", "d3-interpolate", "d3-time", "d3-time-format", "internmap")


def utc():
    return dt.datetime.now(dt.UTC).isoformat(timespec="milliseconds")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as out:
        for row in rows:
            out.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def write_csv(path, rows):
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class Fetcher:
    def __init__(self, cache):
        self.cache = cache
        self.cache.mkdir(parents=True, exist_ok=True)

    def get(self, url, limit=50_000_000):
        key = sha(url.encode())
        body = self.cache / (key + ".bin")
        meta = self.cache / (key + ".json")
        if meta.is_file():
            info = json.loads(meta.read_text())
            info["served_from_local_cache"] = True
            return (body.read_bytes() if body.is_file() else None), info
        info = {"url": url, "utc": utc(), "served_from_local_cache": False}
        raw = None
        for attempt in range(3):
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "AF-RES-135 research receipt", "Accept-Encoding": "identity"})
                with urllib.request.urlopen(request, timeout=18) as response:
                    raw = response.read(limit + 1)
                    if len(raw) > limit:
                        raise ValueError("response byte limit exceeded")
                    info.update(status=response.status, final_url=response.url, bytes=len(raw), sha256=sha(raw),
                                content_type=response.headers.get("Content-Type", ""))
                break
            except (OSError, ValueError) as error:
                info.update(status=getattr(error, "code", "error"), error=str(error), bytes=0)
                if info["status"] in (403, 404, 410, 451):
                    break
        info.update(attempts=attempt + 1, completed_utc=utc())
        if raw is not None:
            body.write_bytes(raw)
            info.pop("error", None)
        write_json(meta, info)
        return raw, info


def git(*args, repo=None, allow_missing=False):
    p = subprocess.run(["git", *([] if repo is None else ["-C", str(repo)]), *args], capture_output=True)
    if p.returncode and not allow_missing:
        raise RuntimeError(p.stderr.decode())
    return p.stdout if p.returncode == 0 else None


def archive(fetcher, dist, version):
    raw, info = fetcher.get(dist["tarball"])
    if raw is None:
        raise ValueError(f"{dist['tarball']}: {info}")
    checks = {}
    checksum = dist.get("shasum")
    if checksum:
        checks["npm_sha1"] = hashlib.sha1(raw).hexdigest() == checksum
    for candidate in dist.get("integrity", "").split():
        algorithm, digest = candidate.split("-", 1)
        checks[algorithm] = base64.b64encode(hashlib.new(algorithm, raw).digest()).decode() == digest
    if not checks or not all(checks.values()):
        raise ValueError(f"integrity failure: {dist['tarball']}: {checks}")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        files = {m.name.removeprefix("package/"): tar.extractfile(m).read()
                 for m in tar if m.isfile() and m.name.startswith("package/")}
    manifest = json.loads(files["package.json"])
    if manifest["version"] != version:
        raise ValueError(f"archive version mismatch: {dist['tarball']}")
    return files, manifest, info | {"verified": checks, "file_count": len(files)}


def entry(manifest):
    exports = manifest.get("exports")
    if isinstance(exports, dict):
        exports = exports.get(".", exports)
        if isinstance(exports, dict):
            exports = exports.get("default") or exports.get("import") or exports.get("require")
    value = exports or manifest.get("main", "index.js")
    return value.removeprefix("./")


def normalized(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = []
    for line in text.splitlines():
        line = re.sub(r"^\s*\*(?:\s|$)", "", line).strip()
        if not line:
            continue
        if re.fullmatch(r"(?:[#/!*]+\s*)?(?:version\s+|v)\d+\.\d+\.\d+(?:\s*)", line, re.IGNORECASE):
            line = "<version-banner>"
        lines.append(re.sub(r"[ \t]+", " ", line))
    return "\n".join(lines)


def openlayers_section(raw):
    if raw is None:
        return None, {}
    text = raw.decode()
    match = re.search(r"/\*\*\s*\n\s*\*\s*@typedef\s+\{Object\}\s+Options\b.*?\*/", text, re.S)
    if not match:
        return None, {}
    return match.group(), {"Options": [text.count("\n", 0, match.start()) + 1,
                                        text.count("\n", 0, match.end()) + 1]}


def d3_section(raw):
    if raw is None:
        return None, {}
    text = raw.decode()
    heads = list(re.finditer(r'(?m)^<a\s+(?:name|id)="([^"]+)"[^\n]*|^(#{2,6})\s+[^\n]+', text))
    parts, lines = [], {}
    for i, head in enumerate(heads):
        name = head.group(1)
        if name == "_continuous":
            name = "continuous"
        if name not in D3_SECTIONS:
            continue
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        parts.append(text[head.start():end])
        lines[name] = [text.count("\n", 0, head.start()) + 1, text.count("\n", 0, end)]
    if "scaleLinear" not in lines or not {"continuous", "continuous_clamp", "continuous_invert"} <= lines.keys():
        return None, lines
    return "".join(parts), lines


def make_doc(product, version, path, ref, raw, packaged, lines, section, readme_info, alternate):
    return {
        "product": product, "version": version, "logical_locator": path,
        "permalink": f"{GITHUB}/{ref[0]}/blob/{ref[1]}/{path.split('::')[0]}" if ref[1] else "",
        "section_lines": lines, "static_status": "resolved" if section is not None else "unresolved",
        "file_bytes": len(raw) if raw is not None else 0, "file_sha256": sha(raw) if raw is not None else "",
        "section_bytes": len(section.encode()) if section is not None else 0,
        "section_sha256": sha(section.encode()) if section is not None else "",
        "normalized_section_sha256": sha(normalized(section).encode()) if section is not None else "",
        "packaged_doc_sha256": sha(packaged) if packaged is not None else "",
        "packaged_doc_bytes": len(packaged) if packaged is not None else 0,
        "file_acquisition": readme_info, "other_acquisitions": alternate,
    }


def d3_release(version, packument, repo, fetcher):
    row = packument["versions"][version]
    publish = packument["time"][version]
    tag = f"v{version}"
    object_id = git("rev-parse", "--verify", tag, repo=repo, allow_missing=True)
    tag_commit = git("rev-parse", "--verify", f"{tag}^{{commit}}", repo=repo, allow_missing=True)
    tag_type = git("cat-file", "-t", tag, repo=repo, allow_missing=True)
    tag_commit = tag_commit.decode().strip() if tag_commit else ""
    head = row.get("gitHead", "")
    chosen_commit = tag_commit or head
    clock = ""
    clock_kind = ""
    if tag_type == b"tag\n":
        clock = git("for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{tag}", repo=repo).decode().strip()
        clock_kind = "tagger"
    elif tag_commit:
        clock = git("show", "-s", "--format=%cI", tag_commit, repo=repo).decode().strip()
        clock_kind = "commit_not_tag_clock"
    files, manifest, tar_info = archive(fetcher, row["dist"], version)
    path = entry(manifest)
    package_src = files.get("src/continuous.js") or files.get(path)
    tag_src = git("show", f"{chosen_commit}:src/continuous.js", repo=repo, allow_missing=True) if chosen_commit else None
    readme = git("show", f"{chosen_commit}:README.md", repo=repo, allow_missing=True) if chosen_commit else None
    packaged_readme = next((content for name, content in files.items() if name.lower() == "readme.md"), None)
    section, lines = d3_section(readme)
    delta = (dt.datetime.fromisoformat(publish) - dt.datetime.fromisoformat(clock)).total_seconds() if clock else ""
    release = {
        "product": "d3-scale", "version": version, "publish_utc": publish,
        "npm_git_head": head, "tag": tag if tag_commit else "", "tag_object": object_id.decode().strip() if object_id else "",
        "tag_commit": tag_commit, "tag_clock_utc": clock, "tag_clock_kind": clock_kind,
        "publish_minus_tag_seconds": delta, "clock_reversal": (delta < 0) if clock else "unconfirmed",
        "tag_githead_agree": tag_commit == head if tag_commit and head else "unconfirmed",
        "tarball_url": row["dist"]["tarball"], "tarball_integrity": row["dist"].get("integrity", ""),
        "tarball_npm_sha1": row["dist"].get("shasum", ""), "tarball_sha256": tar_info["sha256"],
        "tarball_verified": True, "deprecated_now": row.get("deprecated",""),
        "entry_path": path, "entry_format": "esm" if manifest.get("type") == "module" else "commonjs_umd",
        "entry_sha256": sha(files[path]), "source_path": "src/continuous.js" if "src/continuous.js" in files else path,
        "source_sha256": sha(package_src), "source_tag_sha256": sha(tag_src) if tag_src else "",
        "tag_source_equals_package": tag_src == package_src if tag_src else "unconfirmed",
        "dependencies": json.dumps(manifest.get("dependencies", {}), sort_keys=True),
        "same_number_republish_evidence": "unconfirmed_single_snapshot",
    }
    readme_path = f"{GITHUB}/d3/d3-scale/blob/{chosen_commit}/README.md"
    readme_info = {"url": readme_path, "kind": "git_show", "utc": utc(), "attempts": 1,
                   "bytes": len(readme) if readme is not None else 0, "status": "ok" if readme is not None else "missing"}
    doc = make_doc("d3-scale", version, "README.md::scaleLinear", ("d3/d3-scale", chosen_commit), readme,
                   packaged_readme, lines, section, readme_info, {"tarball": tar_info})
    return release, doc


def ol_release(row, fetcher, seen):
    version = row["version"]
    ref = row["tag_commit"] or row["npm_git_head"]
    if version == "10.7.2" and not ref:
        ref = seen["10.7.0"]["tag_commit"]
    base = f"{RAW}/openlayers/openlayers/{ref}"
    source, source_info = fetcher.get(f"{base}/{OL_SOURCE}")
    readme, README_info = fetcher.get(f"{base}/README.md")
    example, example_info = fetcher.get(f"{base}/{OL_EXAMPLE}")
    dist = {"tarball": row["tarball_url"], "integrity": row["tarball_integrity"], "shasum": row["tarball_npm_sha1"]}
    files, manifest, tar_info = archive(fetcher, dist, version)
    assert row["translate_sha256"] == sha(files["interaction/Translate.js"]), version
    assert row["tarball_sha256"] == tar_info["sha256"], version
    section, lines = openlayers_section(source)
    release = {"product": "ol", **row, "entry_path": "interaction.js", "entry_format": "module_source",
               "entry_sha256": sha(files["interaction.js"]), "source_path": "interaction/Translate.js",
               "source_sha256": row["translate_sha256"], "tarball_verified": True,
               "clock_reversal": float(row["publish_minus_tag_seconds"]) < 0 if row["publish_minus_tag_seconds"] else "unconfirmed",
               "same_number_republish_evidence": "unconfirmed_single_snapshot"}
    doc = make_doc("ol", version, OL_SOURCE + "::Options", ("openlayers/openlayers", ref), source, None, lines,
                   section, source_info, {"readme": README_info, "example": example_info, "tarball": tar_info})
    doc["example_normalized_sha256"] = sha(normalized(example.decode()).encode()) if example else ""
    return release, doc


def acquire(cache, d3_repo):
    f = Fetcher(cache)
    roster = json.loads((ROOT / "evidence/roster.json").read_text())
    raw, registry = f.get("https://registry.npmjs.org/d3-scale")
    packument = json.loads(raw)
    assert all(packument["time"][row["version"]] == row["utc"] for row in roster["publish"])
    previous = list(csv.DictReader(git("show", OL_PREFIX + "releases.csv").decode().splitlines()))
    seen = {r["version"]: r for r in previous}

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
        tasks = [pool.submit(ol_release, row, f, seen) for row in previous]
        tasks += [pool.submit(d3_release, row["version"], packument, d3_repo, f) for row in roster["publish"]]
        result = [task.result() for task in tasks]
        dep_tasks = {p: pool.submit(f.get, f"{REGISTRY}/{p}") for p in D3_PACKAGES}
        dep_registry = {p: future.result()[1] for p, future in dep_tasks.items()}

    releases, docs = map(list, zip(*result))
    for product in ("ol", "d3-scale"):
        group = [r for r in releases if r["product"] == product]
        for r in group:
            r["same_entry_versions"] = " ".join(other["version"] for other in group
                                                 if r["entry_sha256"] == other["entry_sha256"] and r != other)
            r["same_source_versions"] = " ".join(other["version"] for other in group
                                                  if r["source_sha256"] == other["source_sha256"] and r != other)
            r["same_tarball_versions"] = " ".join(other["version"] for other in group
                                                   if r["tarball_sha256"] == other["tarball_sha256"] and r != other)
        for rank, r in enumerate(sorted(group, key=lambda row: tuple(map(int, row["version"].split(".")))), 1):
            r["semver_rank"] = rank
        for rank, r in enumerate(sorted(group, key=lambda row: (row["publish_utc"], row["semver_rank"])), 1):
            r["publish_rank"] = rank
    write_csv(ROOT / "releases.csv", releases)
    write_jsonl(ROOT / "evidence/sections.jsonl", docs)
    extras = []
    for v, item in packument["versions"].items():
        m = re.match(r"^(\d+)\.(\d+)\.(\d+)-", v)
        if m:
            base = tuple(map(int, m.groups()))
            extras.append({"version": v, "in_numeric_window": (1, 0, 0) <= base <= (4, 0, 2),
                           "publish_utc": packument["time"].get(v, ""), "git_head": item.get("gitHead", ""),
                           "integrity": item["dist"].get("integrity", ""), "tarball_url": item["dist"]["tarball"],
                           "module_status": "excluded_not_opened"})
    write_csv(ROOT / "evidence/d3-prereleases.csv", extras)
    write_json(ROOT / "evidence/acquisition.json", {"root_registry": registry, "dependency_registries": dep_registry,
               "products": {p: sum(r["product"] == p for r in releases) for p in ("ol", "d3-scale")}})
    print(f"release entries {len(releases)}; resolved sections {sum(d['static_status'] == 'resolved' for d in docs)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", required=True, type=pathlib.Path)
    parser.add_argument("--d3-git", required=True, type=pathlib.Path)
    args = parser.parse_args()
    acquire(args.cache, args.d3_git)


if __name__ == "__main__":
    main()
