"""Policy inputs computed from fetched release artifacts. No target functions are called."""
import json
import re
from pathlib import Path, PurePosixPath
from urllib.error import URLError

from common import ROOT, archive, process, sha, write_json

FUNCTIONS = {"simple-statistics": ("quantile", "median"),
             "d3-array": ("quantile", "quantileSorted", "median")}
ALIASES = (
    "quantile|quantiles|quantileSorted|quantileRank|quantileRankSorted|percentile|percentiles|"
    "percentileRank|median|medians|medianSorted|quartile|quartiles|interquartile|interquartileRange|"
    "IQR|interpolation|interpolate|interpolated"
)
WORDS = re.compile(r"\b(?:" + ALIASES + r")\b", re.I)


def entry(manifest):
    export = manifest.get("exports")
    root = export.get(".", export) if isinstance(export, dict) else export
    if isinstance(root, dict):
        if isinstance(root.get("require"), str):
            return "require", root["require"].removeprefix("./")
        main = root.get("import") or root.get("node") or root.get("default")
        return ("import", main.removeprefix("./")) if isinstance(main, str) else ("unknown", "")
    path = root or manifest.get("main", "index.js")
    if not isinstance(path, str):
        return "unknown", ""
    mode = "import" if path.endswith(".mjs") or manifest.get("type") == "module" and not path.endswith(".cjs") else "require"
    return mode, path.removeprefix("./")


def path_for(package, function):
    if package == "d3-array":
        return "src/quantile.js" if function == "quantileSorted" else f"src/{function}.js"
    return f"src/{function}.js"


def doc_path(package, function):
    return "README.md" if package == "d3-array" else path_for(package, function)


def section(package, function, document):
    source = document.decode("utf-8")
    if package == "simple-statistics":
        # Require an immediately adjacent JSDoc block for the named root.
        ending = re.search(r"\n(?:export\s+(?:default\s+)?)?function\s+" + re.escape(function) + r"\s*\(", source)
        if not ending or not source[:ending.start()].rstrip().endswith("*/"):
            return None
        end = ending.start()
        start = source.rfind("/**", 0, end)
        if start < 0:
            return None
        selected = source[start + 3:end].strip().removesuffix("*/")
        return re.sub(r"\s+", " ", re.sub(r"(?m)^\s*\* ?", "", selected)).strip().encode()
    anchor = rf'<a\b[^>]+\b(?:name|id)="{re.escape(function)}"'
    begin = re.search(anchor, source)
    if not begin:
        return None
    end = re.search(r'\n<a\b[^>]+\b(?:name|id)="', source[begin.end():])
    tail = len(source) if end is None else begin.end() + end.start()
    return re.sub(r"\s+", " ", source[begin.start():tail]).strip().encode()


def archive_notice(files, version):
    candidates = sorted(name for name in files if re.fullmatch(r"(?i)(?:changelog|changes)(?:\.(?:md|txt|rst))?", name))
    if not candidates:
        return {"bundled": "absent", "words": [], "logical_bytes": 0}
    name = candidates[0]
    raw = files[name]
    headers = list(re.finditer(r"(?im)^#{1,5}[ \t]+.*$", raw.decode("utf-8")))
    selector = re.compile(r"(?<![\d.])v?" + re.escape(version) + r"(?![\d.\w-])")
    found = [i for i, h in enumerate(headers) if selector.search(h.group())]
    if len(found) != 1:
        return {"bundled": "unresolved-section", "path": name, "reason": "CHANGELOG not divided by exact version",
                "words": [], "logical_bytes": len(raw)}
    i = found[0]
    level = len(headers[i].group().split()[0])
    end = next((h.start() for h in headers[i + 1:] if len(h.group().split()[0]) <= level), None)
    part = raw.decode("utf-8")[headers[i].start():end]
    return {"bundled": "available-at-npm-time", "path": name, "words": matches(part),
            "section_sha256": sha(part.encode()), "logical_bytes": len(raw)}


def matches(text):
    return sorted({match.group().lower() for match in WORDS.finditer(text)})


def notice(files, release):
    bundled = archive_notice(files, release["version"])
    official = release["notice"]["state"]
    reason = bundled.get("reason") or (official if official in {"time-unverified", "inventory-unavailable"} else "")
    return bundled | {"official": official, "reason": reason, "source_url": release["notice"].get("url")}


def release_assets(release, raw):
    files, manifest, checks = archive(raw, release["dist"], release["package"], release["version"])
    return files, manifest, checks


def c_fingerprint(package, fn, document):
    if document is None:
        return {"state": "unknown", "reason": "edition document unavailable", "logical_bytes": 0}
    part = section(package, fn, document)
    if part is None:
        return {"state": "unknown", "reason": "function document section unresolved", "logical_bytes": 0}
    return {"state": "resolved", "sha256": sha(part), "logical_bytes": len(part)}


def d_fingerprint(release, files, fn, c):
    source = path_for(release["package"], fn)
    target = release["entry"]
    if c["state"] != "resolved" or not target or target not in files or source not in files or "direct" not in release:
        return {"state": "unknown", "reason": "C, entry, target source or lock unresolved", "logical_bytes": 0}
    paths = sorted({target, source})
    pieces = {path: sha(files[path]) for path in paths}
    direct = json.dumps(release["direct"], sort_keys=True, separators=(",", ":")).encode()
    fingerprint = json.dumps([c["sha256"], release["loader"], pieces, sha(direct)], sort_keys=True).encode()
    return {"state": "resolved", "sha256": sha(fingerprint), "files": pieces,
            "direct_sha256": sha(direct), "logical_bytes": sum(len(files[path]) for path in paths) + len(direct)}


def e_fingerprint(release, files, parser_root, dest, depth):
    functions = FUNCTIONS[release["package"]]
    if not release["entry"] or release["entry"] not in files:
        return {}, None, "declared public entry absent"
    for name, raw in files.items():
        pure = PurePosixPath(name)
        if not pure.is_absolute() and ".." not in pure.parts and (name.endswith((".js", ".mjs", ".map"))):
            path = dest / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
    check = process(["node", str(ROOT / "replay/fingerprint.cjs"), str(dest), release["entry"],
                     str(parser_root), release["package"], str(depth)], timeout=15)
    if check["exit"] != 0:
        return {}, check, "static parser process failed"
    parsed = json.loads(check["stdout"])
    if set(parsed["functions"]) != set(functions):
        raise ValueError("parser returned incorrect function roster")
    return parsed, check, ""


def after_edge(policy, previous, current, fn):
    if policy == "A":
        return "alert", "exact-request"
    if policy in {"C", "D"}:
        before = previous[policy][fn]
        target = current[policy][fn]
        if before["state"] != "resolved" or target["state"] != "resolved":
            return "forced", "/".join(sorted({r["reason"] for r in (before, target) if r["state"] != "resolved"}))
        return ("alert", policy + " fingerprint changed") if before["sha256"] != target["sha256"] else ("skip", policy + " equal")
    depth = "1" if policy == "E" else "2"
    unknown = set()
    before = previous["E"].get(fn, {}).get(depth, {})
    target = current["E"].get(fn, {}).get(depth, {})
    for record, body in ((previous, before), (current, target)):
        if body.get("status") != "resolved":
            unknown.add(body.get("reason") or record["E_error"])
    if current["notice"]["reason"]:
        unknown.add(current["notice"]["reason"])
    if unknown:
        return "forced", "/".join(sorted(unknown))
    if current["notice"]["words"]:
        return "alert", "notice: " + ",".join(current["notice"]["words"])
    if before["signature"] != target["signature"]:
        return "alert", "static closure changed at depth " + depth
    return "skip", "static closure and admissible notice unchanged"
