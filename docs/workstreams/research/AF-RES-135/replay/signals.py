"""Freeze release-time signals and dependency resolution before any scale execution."""
import argparse
import concurrent.futures
import csv
import json
import pathlib
import re
import shutil
import subprocess

from artifacts import D3_PACKAGES, Fetcher, OL_TAR, REGISTRY, ROOT, archive, entry, sha, write_csv, write_json, write_jsonl

D3_LOCAL = {"index.js", "src/index.js", "src/linear.js", "src/continuous.js", "src/constant.js",
            "src/number.js", "src/array.js", "src/init.js"}
D3_DIRECT = {"d3-array": {"index.js", "src/index.js", "src/bisect.js", "src/bisector.js"},
             "d3-interpolate": {"index.js", "src/index.js", "src/value.js", "src/number.js", "src/round.js"}}
HTTP_PROBES = {
    "ol_latest": "https://openlayers.org/en/latest/apidoc/module-ol_interaction_Translate-Translate.html",
    "ol_6.6.1": "https://openlayers.org/en/v6.6.1/apidoc/module-ol_interaction_Translate-Translate.html",
    "ol_6.7.0": "https://openlayers.org/en/v6.7.0/apidoc/module-ol_interaction_Translate-Translate.html",
    "d3_current": "https://d3js.org/d3-scale/linear",
}


def read_inputs():
    return (list(csv.DictReader((ROOT / "releases.csv").open())),
            [json.loads(row) for row in (ROOT / "evidence/sections.jsonl").read_text().splitlines()],
            json.loads((ROOT / "evidence/roster.json").read_text()))


def resolve_locks(fetcher, roster):
    catalog = {}
    latest = roster["publish"][-1]["utc"]
    for name in ("d3-scale", *D3_PACKAGES):
        raw, info = fetcher.get(f"{REGISTRY}/{name}")
        if raw is None:
            raise RuntimeError(info)
        packument = json.loads(raw)
        catalog[name] = {
            version: {"utc": stamp, "dependencies": row.get("dependencies", {}),
                      "dist": {k: row["dist"][k] for k in ("tarball", "integrity", "shasum") if k in row["dist"]}}
            for version, row in packument["versions"].items()
            if (stamp := packument["time"].get(version)) and stamp <= latest
        }
    p = subprocess.run(["node", str(ROOT / "replay/resolve.mjs"), shutil.which("npm")],
                       input=json.dumps({"catalog": catalog, "releases": roster["publish"]}), text=True,
                       capture_output=True, check=True)
    locks = json.loads(p.stdout)
    write_json(ROOT / "replay/locks.json", locks)
    return locks


def package_fingerprint(files, paths, prefix, strictly_required=()):
    components = []
    for path in sorted(paths):
        if path not in files:
            if path in strictly_required:
                raise ValueError(f"{prefix}/{path} unavailable")
            continue
        raw = files[path]
        components.append({"file": f"{prefix}/{path}", "bytes": len(raw), "sha256": sha(raw)})
    return components


def translate_fingerprint(files):
    components = package_fingerprint(files, OL_TAR - {"interaction/Translate.js"}, "ol", OL_TAR)
    raw = files["interaction/Translate.js"]
    # The implementation fingerprint excludes comments. Costs include the whole file read.
    implementation = re.sub(rb"/\*.*?\*/", b"", raw, flags=re.S)
    implementation = re.sub(rb"(?m)^\s*//[^\r\n]*", b"", implementation)
    # A trailing generated source-map URI is a comment and outside the measured implementation.
    components.append({"file": "ol/interaction/Translate.js", "bytes": len(raw), "sha256": sha(implementation),
                       "raw_sha256": sha(raw)})
    return components


def d3_fingerprint(files, lock, fetcher):
    local = package_fingerprint(files, D3_LOCAL | {entry(json.loads(files["package.json"]))}, "d3-scale",
                                {"src/linear.js", "src/continuous.js"})
    all_components = list(local)
    for name, paths in D3_DIRECT.items():
        pkg = lock["packages"][f"node_modules/{name}"]
        dep_files, dep_manifest, _ = archive(fetcher, pkg["dist"], pkg["version"])
        main = entry(dep_manifest)
        all_components.extend(package_fingerprint(dep_files, paths | {main}, name, {main}))
    # Versions are attribution; the signal compares file path and bytes.
    return local, all_components


def aggregate(components):
    return sha(json.dumps(sorted((c["file"], c["sha256"]) for c in components), separators=(",", ":")).encode())


def observation(row, doc, lock, fetcher):
    product, version = row["product"], row["version"]
    dist = {"tarball": row["tarball_url"], "integrity": row["tarball_integrity"], "shasum": row["tarball_npm_sha1"]}
    files, _, tar_info = archive(fetcher, dist, version)
    components = []
    error = ""
    try:
        local, components = ([], translate_fingerprint(files)) if product == "ol" else d3_fingerprint(files, lock, fetcher)
    except (ValueError, KeyError) as failure:
        local = []
        error = str(failure)
    alternate = doc["other_acquisitions"]
    signal = {
        "product": product, "version": version, "publish_utc": row["publish_utc"],
        "publish_rank": row["publish_rank"], "semver_rank": row["semver_rank"],
        "logical_locator": doc["logical_locator"], "permalink": doc["permalink"], "static_status": doc["static_status"],
        "raw_doc_sha256": doc["file_sha256"], "raw_section_sha256": doc["section_sha256"],
        "text_sha256": doc["normalized_section_sha256"], "example_sha256": doc.get("example_normalized_sha256", ""),
        "implementation_sha256": aggregate(components) if not error else "",
        "local_implementation_sha256": aggregate(local) if local else "",
        "implementation_error": error,
        "docs_bytes": doc["file_bytes"], "docs_opens": doc["file_acquisition"]["attempts"],
        "readme_opens": alternate.get("readme", {}).get("attempts", 1 if product == "d3-scale" else 0),
        "readme_bytes": alternate.get("readme", {}).get("bytes", doc["file_bytes"] if product == "d3-scale" else 0),
        "archive_bytes": tar_info["bytes"], "archive_opens": alternate["tarball"]["attempts"],
        "code_files": len(components), "code_bytes": sum(item["bytes"] for item in components),
        "section_bytes": doc["section_bytes"], "hash_utc": doc["file_acquisition"]["utc"],
    }
    return signal, {"product": product, "version": version, "components": components, "error": error}


def apply(before, after):
    if before is None:
        return {p: "initial" for p in "ABCD"}
    locator_moved = before["logical_locator"] != after["logical_locator"]
    unresolved = locator_moved or any(r["static_status"] != "resolved" for r in (before, after))
    c = before["text_sha256"] != after["text_sha256"]
    d = before["implementation_sha256"] != after["implementation_sha256"]
    code_missing = any(r["implementation_error"] for r in (before, after))
    return {"A": "trigger", "B": "forced" if unresolved else "skip",
            "C": "forced" if unresolved else "trigger" if c else "skip",
            "D": "forced" if unresolved or code_missing else "trigger" if c or d else "skip"}


def scan_signals(cache):
    fetcher = Fetcher(cache)
    releases, docs, roster = read_inputs()
    locks = resolve_locks(fetcher, roster)
    doc_by_key = {(d["product"], d["version"]): d for d in docs}
    entries = []
    for row in sorted(releases, key=lambda r: (r["product"], int(r["publish_rank"]))):
        product, version = key = (row["product"], row["version"])
        current, receipt = observation(row, doc_by_key[key], locks["base"].get(version), fetcher)
        entries.append((current, receipt))
    for product in ("ol", "d3-scale"):
        for order in ("publish", "semver"):
            prev = None
            for row in sorted((entry[0] for entry in entries if entry[0]["product"] == product),
                              key=lambda r: int(r[order + "_rank"])):
                row[order + "_previous"] = prev["version"] if prev else ""
                row.update({f"{order}_{name}": val for name, val in apply(prev, row).items()})
                prev = row
    write_csv(ROOT / "signals.csv", [x[0] for x in entries])
    write_jsonl(ROOT / "evidence/components.jsonl", [x[1] for x in entries])

    def probe(item):
        name, url = item
        raw, info = fetcher.get(url)
        lowered = raw.lower() if raw else b""
        terms = (b"scaleLinear", b"linear-unknown") if name == "d3_current" else (b"features", b"not used if")
        return name, info | {"literal_bytes_found": {t.decode(): t.lower() in lowered for t in terms},
                            "historic_http_status": "unconfirmed"}

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        probes = dict(pool.map(probe, HTTP_PROBES.items()))
    write_json(ROOT / "evidence/current-http.json", probes)
    print(f"Signal rows {len(entries)}, source/delegate gaps {sum(bool(x[1]['error']) for x in entries)}")
    print(f"Lock base errors {sum(bool(r.get('error')) for r in locks['base'].values())}")
    print("Unmatched shared ranges:", [key for key, pair in locks["matched"].items() if pair["failures"]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", required=True, type=pathlib.Path)
    scan_signals(parser.parse_args().cache)
