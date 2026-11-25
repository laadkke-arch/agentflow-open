"""Recompute the inventories, joins and nine wheel cells from committed evidence."""
import argparse
import csv
import gzip
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime
from email import policy
from email.parser import BytesParser
from itertools import product
from pathlib import Path
from unittest.mock import patch

import packaging
from packaging import _manylinux, tags
from packaging.specifiers import SpecifierSet
from packaging.utils import parse_wheel_filename


VERSIONS = ("1.13.1", "1.14.0", "1.14.1")
ARTIFACT_IDS = ("M1", "M2", "M5", "M8", "M9", "X-sdist", "X-macos", "X-free", "X-late")
ABSENT = "<absent>"
WHEEL_NAME = re.compile(
    r"scipy-(?P<version>[^-]+)-(?:[0-9][^-]*-)?"
    r"(?P<interpreter>[^-]+)-(?P<abi>[^-]+)-(?P<platform>[^-]+)\.whl"
)


def read_json(path):
    return json.loads(path.read_bytes())


def sha256(body):
    return hashlib.sha256(body).hexdigest()


def store_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bytes_from_receipt(prefix, body_path=None, content_type=None, url=None):
    raw = read_json(prefix.with_suffix(".transport.json"))
    curl = raw["curl"]
    assert raw["exit_code"] == 0 and curl["response_code"] == 200, prefix
    assert curl["ssl_verify_result"] == 0, prefix
    if url:
        assert raw["requested_url"] == curl["url_effective"] == url, prefix
    if content_type:
        assert curl["content_type"].split(";")[0] == content_type, prefix
    header = prefix.with_suffix(".headers.txt").read_bytes()
    assert sha256(header) == raw["headers_sha256"], prefix
    if body_path:
        body = body_path.read_bytes()
        if body_path.suffix == ".gz":
            body = gzip.decompress(body)
        assert len(body) == raw["body_bytes"] and sha256(body) == raw["body_sha256"], body_path
        return raw, body
    return raw, None


def index_summary(response):
    return {
        "url": response["requested_url"], "checked_utc": response["finished_utc"],
        "sha256": response["body_sha256"], "size_bytes": response["body_bytes"],
    }


def filename_version(filename):
    if match := WHEEL_NAME.fullmatch(filename):
        return match["version"]
    if filename.startswith("scipy-") and filename.endswith(".tar.gz"):
        return filename.removeprefix("scipy-").removesuffix(".tar.gz")
    if filename.startswith("scipy-") and filename.endswith(".zip"):
        return filename.removeprefix("scipy-").removesuffix(".zip")
    return None


def filename_tags(filename):
    """Independent wheel parsing using only the filename grammar and cartesian product."""
    if not filename.endswith(".whl"):
        return ()
    match = WHEEL_NAME.fullmatch(filename)
    assert match, filename
    return tuple(product(*(match[field].lower().split(".") for field in ("interpreter", "abi", "platform"))))


def model_tags(minor, free_threaded, glibc):
    abi = f"cp3{minor}" + ("t" if free_threaded else "")
    interpreter = f"cp3{minor}"
    with patch.object(_manylinux, "_get_glibc_version", return_value=glibc):
        with patch.dict(sys.modules, {"_manylinux": None}):
            platforms = tuple(_manylinux.platform_tags(("x86_64",))) + ("linux_x86_64",)
    return set(tags.cpython_tags((3, minor), (abi,), platforms)).union(
        tags.compatible_tags((3, minor), interpreter, platforms)
    )


def independent_match(tag, minor, free_threaded, glibc):
    interpreter, abi, target = tag
    current = f"cp3{minor}"
    current_abi = current + ("t" if free_threaded else "")
    stable_abi = "abi3t" if free_threaded else "abi3"
    cpython_floor = re.fullmatch(r"cp3(\d+)", interpreter)
    if abi == "none":
        py_minor = re.fullmatch(r"py3(\d+)", interpreter)
        python_compatible = interpreter in (current, "py3") or (py_minor is not None and int(py_minor[1]) <= minor)
    elif abi == stable_abi:
        python_compatible = cpython_floor is not None and 2 <= int(cpython_floor[1]) <= minor
    else:
        python_compatible = (interpreter, abi) == (current, current_abi)
    if target == "any":
        return abi == "none" and python_compatible
    if target == "linux_x86_64":
        return python_compatible
    legacy = {"manylinux1_x86_64": (2, 5), "manylinux2010_x86_64": (2, 12), "manylinux2014_x86_64": (2, 17)}
    numbered = re.fullmatch(r"manylinux_(\d+)_(\d+)_x86_64", target)
    required_glibc = tuple(map(int, numbered.groups())) if numbered else legacy.get(target)
    return python_compatible and required_glibc is not None and glibc >= required_glibc


def candidate_traces(rows, digest_key, minor, free_threaded=False, glibc=(2, 17)):
    allowed = model_tags(minor, free_threaded, glibc)
    by_packaging, by_independent = [], []
    for index, item in rows:
        name = item["filename"]
        if not name.endswith(".whl"):
            continue
        implementation_tags = parse_wheel_filename(name)[3]
        independent_tags = filename_tags(name)
        assert {str(tag) for tag in implementation_tags} == {"-".join(tag) for tag in independent_tags}, name
        matched_packaging = sorted(str(tag) for tag in implementation_tags & allowed)
        matched_independent = sorted("-".join(tag) for tag in independent_tags
                                     if independent_match(tag, minor, free_threaded, glibc))
        base = {"index": index, "filename": name, "sha256": item[digest_key]["sha256"]}
        if matched_packaging:
            by_packaging.append({**base, "matched_tags": matched_packaging})
        if matched_independent:
            by_independent.append({**base, "matched_tags": matched_independent})
    return by_packaging, by_independent


def value(item, field):
    return item[field] if field in item else ABSENT


def serialized(value_):
    return value_ if isinstance(value_, str) else json.dumps(value_, ensure_ascii=False, sort_keys=True)


def join_key(item, digest_key):
    return item["filename"], item[digest_key]["sha256"]


def verify_artifact_observations(artifact_dir):
    result = {}
    for identity in ARTIFACT_IDS:
        prefix = artifact_dir / identity
        fact = read_json(prefix.with_suffix(".inspection.json"))
        download, _ = bytes_from_receipt(prefix)
        assert prefix.with_suffix(".inspection.exit").read_text().strip() == "0", prefix
        assert (fact["artifact_sha256"], fact["artifact_size"]) == (download["body_sha256"], download["body_bytes"])
        assert download["requested_url"].rsplit("/", 1)[-1] == fact["filename"]
        if fact["filename"].endswith(".whl"):
            metadata_prefix = artifact_dir / f"{identity}-metadata"
            _, metadata = bytes_from_receipt(metadata_prefix, prefix.with_suffix(".metadata.gz"),
                                             url=download["requested_url"] + ".metadata")
            original_wheel_headers = prefix.with_suffix(".WHEEL").read_bytes()
            assert sha256(original_wheel_headers) == fact["wheel_fingerprint"]["sha256"]
            headers = BytesParser(policy=policy.default).parsebytes(original_wheel_headers)
            assert headers.get_all("Tag") == fact["wheel_tags"]
            assert set(fact["wheel_tags"]) == {"-".join(tag) for tag in filename_tags(fact["filename"])}
            assert fact["sidecar_matches_zip"] is True
        else:
            metadata = gzip.decompress(prefix.with_suffix(".pkg-info.gz").read_bytes())
        parsed = BytesParser(policy=policy.default).parsebytes(metadata, headersonly=True)
        assert sha256(metadata) == fact["metadata_fingerprint"]["sha256"]
        assert parsed["Requires-Python"] == fact["requires_python"]
        assert parsed["Name"].lower() == "scipy"
        assert parsed["Version"] == fact["version"] == filename_version(fact["filename"])
        result[fact["filename"]] = {"id": identity, **fact}
    return result


def file_row(version, index, item, simple_pair, info, artifact, github):
    simple_index, simple = simple_pair if simple_pair else (-1, {})
    comparable = {
        "filename": "filename", "url": "url", "size": "size", "requires_python": "requires-python",
        "core-metadata": "core-metadata", "yanked": "yanked", "upload_time_iso_8601": "upload-time",
    }
    mismatches = [src for src, dest in comparable.items() if value(item, src) != value(simple, dest)]
    github_published = github["released_this_datetime_utc"]
    seconds = (datetime.fromisoformat(item["upload_time_iso_8601"]) - datetime.fromisoformat(github_published)).total_seconds()
    order = "before" if seconds < 0 else "after" if seconds > 0 else "same recorded timestamp"
    digest = item["digests"]["sha256"]
    publisher_sha = github["readme_checksums"].get(item["filename"], {}).get("sha256", ABSENT)
    parsed_tags = filename_tags(item["filename"])
    if not simple_pair:
        identity_join = "no filename+sha256 join"
    elif mismatches:
        identity_join = "filename+sha256; difference:" + ",".join(mismatches)
    else:
        identity_join = "filename+sha256; all shared fields equal"
    if artifact:
        md = value(item, "core-metadata")
        metadata_ok = md == {"sha256": artifact["metadata_fingerprint"]["sha256"]} if parsed_tags else md is False
        assert (artifact["artifact_sha256"], artifact["artifact_size"]) == (digest, item["size"])
        assert artifact["requires_python"] == value(item, "requires_python") and metadata_ok, artifact
    return {
        "scipy": version, "json_index_0": index, "simple_index_0": simple_index if simple_pair else "미확인",
        "filename": item["filename"], "packagetype": item["packagetype"], "url": item["url"], "sha256": digest,
        "size_bytes": item["size"], "upload_utc": item["upload_time_iso_8601"],
        "release_requires_python": value(info, "requires_python"), "json_file_requires_python": value(item, "requires_python"),
        "simple_requires_python": value(simple, "requires-python"), "json_core_metadata": serialized(value(item, "core-metadata")),
        "simple_core_metadata": serialized(value(simple, "core-metadata")),
        "simple_data_dist_info_metadata": serialized(value(simple, "data-dist-info-metadata")),
        "json_yanked": serialized(value(item, "yanked")), "simple_yanked": serialized(value(simple, "yanked")),
        "json_yanked_reason": serialized(value(item, "yanked_reason")), "simple_yanked_reason_key": serialized(value(simple, "yanked_reason")),
        "json_provenance": serialized(value(item, "provenance")), "simple_provenance": serialized(value(simple, "provenance")),
        "simple_sha256": simple.get("hashes", {}).get("sha256", ABSENT),
        "join": identity_join,
        "filename_expanded_tags": ";".join("-".join(tag) for tag in parsed_tags),
        "artifact_receipt": artifact["id"] if artifact else "미실행",
        "download_sha256": artifact["artifact_sha256"] if artifact else "미실행",
        "download_bytes": artifact["artifact_size"] if artifact else "미실행",
        "archive_requires_python": artifact["requires_python"] if artifact else "미실행",
        "zip_wheel_tags": ";".join(artifact["wheel_tags"]) if artifact and parsed_tags else "적용 대상 밖 (sdist)" if not parsed_tags else "미실행",
        "github_readme_sha256": publisher_sha,
        "github_release_datetime_utc": github_published,
        "github_asset_datetime_utc": github["assets"].get(item["filename"], {}).get("datetime_utc", ABSENT),
        "upload_vs_github_release": order, "upload_minus_github_release_seconds": f"{seconds:.6f}",
    }


def check_cells(html_rows, releases, simple_of_version, verified_artifacts, local):
    cells, traces = [], {}
    for html in html_rows:
        cell, version, python = (html[k] for k in ("cell", "scipy", "python"))
        minor = int(python.split(".")[-1])
        info, release_files = releases[version]["info"], releases[version]["urls"]
        simple_rows = simple_of_version[version]
        options = {}
        for source, entries, key in (("version_json", enumerate(release_files), "digests"),
                                     ("simple_json", simple_rows, "hashes")):
            pkg, independent = candidate_traces(entries, key, minor)
            options[source] = {"packaging": pkg, "independent": independent, "equal": pkg == independent}
        traces[cell] = options
        pkg = options["version_json"]["packaging"]
        simple = options["simple_json"]["packaging"]
        names = [f["filename"] for f in pkg]
        same_keys = {(f["filename"], f["sha256"]) for f in pkg} == {(f["filename"], f["sha256"]) for f in simple}
        previous = html["filename"]
        same_html = names == ([previous] if previous else []) and (not previous or pkg[0]["sha256"] == html["sha256_display"])
        tagged = [release_files[m["index"]] for m in pkg]
        simple_by_index = dict(simple_rows)
        eligible = [f for f in tagged if SpecifierSet(f["requires_python"]).contains(python) and f["yanked"] is False]
        found = verified_artifacts.get(previous)
        test = "적용 대상 밖"
        if found:
            test = "import + linalg.solve exit=0" if found["artifact_sha256"] == local["wheel_sha256"] else "미실행"
        cells.append({
            "cell": cell, "scipy": version, "python": python, "abi": html["abi"], "platform": "Linux glibc 2.17+ x86_64",
            "html_state_248": html["html_state"], "html_sha256_248": html["sha256_display"],
            "html_time_248": html["upload_date_display"], "html_url_248": html["url"],
            "html_release_requires_python_248": html["requires_python_release_html"],
            "html_file_requires_python_248": html["file_requires_python"],
            "release_files": len(release_files), "simple_release_files": len(simple_rows),
            "json_packaging": len(pkg), "json_independent": len(options["version_json"]["independent"]),
            "simple_packaging": len(simple), "simple_independent": len(options["simple_json"]["independent"]),
            "matched_tags_version_json": sum(len(f["matched_tags"]) for f in pkg),
            "yield_after_file_requires_python_and_yanked": len(eligible),
            "release_requires_python": info["requires_python"],
            "release_requires_python_allows": SpecifierSet(info["requires_python"]).contains(python),
            "release_requires_python_agrees_with_248": info["requires_python"] == html["requires_python_release_html"],
            "json_file_requires_python": ";".join(f["requires_python"] for f in tagged) if tagged else "적용 대상 밖",
            "simple_file_requires_python": ";".join(simple_by_index[f["index"]]["requires-python"] for f in simple) if simple else "적용 대상 밖",
            "state_now": ("confirmed_candidate" if pkg else "confirmed_no_match_current") if same_keys else "inventory_disagreement",
            "matched_files": ";".join(names), "matched_file_sha256": ";".join(f["sha256"] for f in pkg),
            "matched_json_indices_0": ";".join(str(f["index"]) for f in pkg),
            "matched_simple_indices_0": ";".join(str(f["index"]) for f in simple),
            "joins_to_248": same_html, "filename_sha256_join_agrees": same_keys,
            "url_agrees_with_248": [f["url"] for f in tagged] == [html["url"]] if previous else "적용 대상 밖",
            "utc_day_agrees_with_display_248": [f["upload_time_iso_8601"][:10] for f in tagged] == [html["upload_date_display"]]
            if previous else "적용 대상 밖",
            "artifact_receipt": found["id"] if found else "적용 대상 밖",
            "archive_requires_python": found["requires_python"] if found else "적용 대상 밖",
            "local_test": test,
            "historical_ci_digest_and_test": "미확인" if found else "적용 대상 밖",
        })
    return cells, traces


def check_counterexamples(releases, simple_of_version, facts):
    controls = {}
    for name in ("X-macos", "X-sdist", "X-free", "X-late"):
        file = next(f for f in facts.values() if f["id"] == name)
        version = file["version"]
        rows = [(i, row) for i, row in simple_of_version[version] if row["filename"] == file["filename"]]
        assert len(rows) == 1 and rows[0][1]["hashes"]["sha256"] == file["artifact_sha256"]
        expected_metadata = {"sha256": file["metadata_fingerprint"]["sha256"]} if file["wheel_tags"] else False
        assert rows[0][1]["core-metadata"] == expected_metadata
        minor = {"X-sdist": 13, "X-macos": 10, "X-free": 13, "X-late": 12}[name]
        packaging_match, independent = candidate_traces(rows, "hashes", minor)
        assert packaging_match == independent
        row = {"version": version, "filename": file["filename"], "sha256": file["artifact_sha256"],
               "simple_index_0": rows[0][0], "linux_gil_matches": len(packaging_match), "wheel_tags": file["wheel_tags"],
               "metadata_gate_allows": SpecifierSet(file["requires_python"]).contains(f"3.{minor}")}
        if name == "X-free":
            compatible, second = candidate_traces(rows, "hashes", 13, free_threaded=True)
            assert compatible == second
            row["linux_313t_matches"] = len(compatible)
        controls[name] = row
    for name, options in (("free_threaded_13", {"free_threaded": True}), ("glibc_2_16", {"glibc": (2, 16)})):
        results = {}
        for version in VERSIONS:
            values = {}
            for minor in (13,) if name == "free_threaded_13" else (9, 10, 13):
                pkg, independent = candidate_traces(enumerate(releases[version]["urls"]), "digests", minor, **options)
                simple, other = candidate_traces(simple_of_version[version], "hashes", minor, **options)
                assert pkg == independent and simple == other
                values[f"3.{minor}"] = {"release": len(pkg), "simple": len(simple)}
            results[version] = values
        controls[name] = results
    return controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert packaging.__version__ == "26.3", "Use the verified packaging wheel in receipts/tools on PYTHONPATH"
    output, root = args.output, args.data / "receipts"
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        parser.error(f"output directory must be empty: {output}")

    release_path = root / "index"
    simple_http, simple_raw = bytes_from_receipt(release_path / "simple-scipy", release_path / "simple-scipy.json.gz",
                                                "application/vnd.pypi.simple.v1+json", "https://pypi.org/simple/scipy/")
    simple = json.loads(simple_raw)
    assert simple["name"] == "scipy" and simple["meta"]["api-version"].split(".")[0] == "1"
    assert isinstance(simple["files"], list) and set(VERSIONS).issubset(simple["versions"])
    simple_of_version = {v: [] for v in (*VERSIONS, "1.15.0")}
    for i, item in enumerate(simple["files"]):
        if (version := filename_version(item["filename"])) in simple_of_version:
            simple_of_version[version].append((i, item))
    artifacts = verify_artifact_observations(root / "artifacts")
    published = read_json(root / "ci/public-github.json")["releases"]
    local = read_json(root / "local/smoke.stdout.txt")
    local_receipt = read_json(root / "local/smoke.run.json")
    assert local_receipt["exit_code"] == 0 and sha256((root / "local/smoke.stdout.txt").read_bytes()) == local_receipt["stdout_sha256"]
    assert local["installed_native_sha256"] == local["wheel_native_sha256"]
    prior = (root / "af-res-248.matrix.csv").read_bytes()
    assert sha256(prior) == "c766342e90532c2270074e591fda574a5b8b77f2cf8bb87f2c975dc243860f20"
    html = [row for row in csv.DictReader(prior.decode("utf-8").splitlines()) if row["kind"] == "main"]
    assert [(row["scipy"], row["python"]) for row in html] == list(product(VERSIONS, ("3.9", "3.10", "3.13")))

    releases, inventory, files, events = {}, {}, [], []
    for version in VERSIONS:
        prefix = release_path / ("scipy-" + version.replace(".", "_"))
        http, body = bytes_from_receipt(prefix, prefix.with_suffix(".json"), "application/json",
                                       f"https://pypi.org/pypi/scipy/{version}/json")
        release = json.loads(body)
        info, items = release["info"], release["urls"]
        assert info["name"].lower() == "scipy" and info["version"] == version and isinstance(items, list)
        assert all(filename_version(item["filename"]) == version for item in items)
        releases[version] = release
        by_key = {join_key(item, "hashes"): (index, item) for index, item in simple_of_version[version]}
        release_keys = {join_key(item, "digests") for item in items}
        assert len(by_key) == len(simple_of_version[version]) and len(release_keys) == len(items)
        rows = [file_row(version, i, item, by_key.get(join_key(item, "digests")), info,
                         artifacts.get(item["filename"]), published[version]) for i, item in enumerate(items)]
        files.extend(rows)
        inventory[version] = {
            **index_summary(http), "info_version": info["version"], "info_requires_python": info["requires_python"],
            "info_python_classifiers": [c for c in info["classifiers"] if c.startswith("Programming Language :: Python")],
            "last_serial": release["last_serial"], "urls_files": len(items), "simple_release_files": len(by_key),
            "wheels": sum(x["packagetype"] == "bdist_wheel" for x in items), "join_common": len(set(by_key) & release_keys),
            "relative_simple_file_order_matches": [join_key(item, "digests") for item in items] == list(by_key),
            "version_json_only_keys": sorted(release_keys - set(by_key)), "simple_only_keys": sorted(set(by_key) - release_keys),
            "github_assets_same_filenames": {row["filename"] for row in rows} == set(published[version]["assets"]),
            "publisher_checksum_matches": sum(row["sha256"] == row["github_readme_sha256"] for row in rows),
            "publisher_checksum_absent_files": [row["filename"] for row in rows if row["github_readme_sha256"] == ABSENT],
            "field_differences": [row["filename"] for row in rows if "difference:" in row["join"]],
        }
        times = [row["upload_utc"] for row in rows]
        event_order = Counter(row["upload_vs_github_release"] for row in rows)
        events.append({"scipy": version, "github_release_datetime_utc": published[version]["released_this_datetime_utc"],
                       "first_observed_upload_record_utc": min(times), "last_observed_upload_record_utc": max(times),
                       "upload_before": event_order["before"], "upload_after": event_order["after"],
                       "equal_recorded_time": event_order["same recorded timestamp"], "release_file_population": len(rows),
                       "post_announcement_filenames": ";".join(row["filename"] for row in rows if row["upload_vs_github_release"] == "after")})
    cells, traces = check_cells(html, releases, simple_of_version, artifacts, local)
    controls = check_counterexamples(releases, simple_of_version, artifacts)
    for identity in ("M9", "X-late"):
        artifact = next(a for a in artifacts.values() if a["id"] == identity)
        mirror_key = "github-M9" if identity == "M9" else "github-late"
        observed, _ = bytes_from_receipt(root / "ci" / mirror_key)
        assert (observed["body_sha256"], observed["body_bytes"]) == (artifact["artifact_sha256"], artifact["artifact_size"])
        controls[mirror_key] = {"same_filename": artifact["filename"], "equal_bytes_by_sha256_and_size": True,
                                "sha256": observed["body_sha256"], "size_bytes": observed["body_bytes"]}
    write_csv(output / "files.csv", files)
    write_csv(output / "cells.csv", cells)
    write_csv(output / "release-events.csv", events)
    store_json(output / "parsers.json", traces)
    store_json(output / "counterexamples.json", controls)
    summary = {
        "packaging_version": packaging.__version__,
        "simple": {**index_summary(simple_http), **simple["meta"], "versions": len(simple["versions"]), "files": len(simple["files"])},
        "releases": inventory, "files": len(files), "cells": len(cells),
        "shared_field_consistency": dict(Counter(row["join"] for row in files)),
        "normal_vacancies": sum(row["state_now"] == "confirmed_no_match_current" for row in cells),
        "positive_cells": sum(row["state_now"] == "confirmed_candidate" for row in cells),
        "verified_local_runs": sum(row["local_test"].endswith("exit=0") for row in cells),
        "artifact_extractions": len(artifacts), "cell_joins_to_prior": sum(row["joins_to_248"] for row in cells),
        "parser_comparisons_equal": sum(source["equal"] for outputs in traces.values() for source in outputs.values()),
        "two_tag_file_matches": sum(row["matched_tags_version_json"] == 2 for row in cells),
        "github_published_file_order": dict(Counter(row["upload_vs_github_release"] for row in files)),
    }
    store_json(output / "inventory.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
