"""Reconcile saved PyPI version and Simple metadata by exact project, version and filename."""

import argparse
import csv
import gzip
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from html import unescape
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

from fetch import RELEASES, endpoints

TARGETS = {("matplotlib", "3.9.1"), ("pytest", "8.1.0")}
MISSING = object()
SHA256 = re.compile(r"[0-9a-fA-F]{64}")
FILE_COLUMNS = (
    "project", "version", "filename", "cohort", "baseline", "baseline_source_id", "baseline_csv_line",
    "file_type", "python_tag", "abi_tag", "platform_tag", "join", "json_count", "simple_count",
    "json_positions", "simple_positions", "json_duplicate_records", "simple_duplicate_records",
    "json_sha256", "simple_sha256", "sha256_comparison", "json_packagetype", "json_python_version",
    "tag_comparison", "json_yanked_type", "json_yanked_raw", "json_reason_type", "json_reason_raw",
    "simple_yanked_type", "simple_yanked_raw", "simple_reason_type", "flag_comparison", "reason_comparison",
    "json_upload_utc_raw", "simple_upload_utc_raw", "upload_comparison",
    "json_requires_python_raw", "simple_requires_python_raw", "requires_python_comparison",
    "json_url", "simple_url", "url_comparison", "html_file_lines", "html_banner",
    "html_yanked_datetime_raw", "html_comparison", "issues",
)


def dump(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def normalized_name(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def filename_parts(filename):
    """Return identity, distribution type and tags from names in scope."""
    if filename.endswith(".whl"):
        parts = filename.removesuffix(".whl").split("-")
        if len(parts) in (5, 6) and all(parts):
            return normalized_name(parts[0]), parts[1], "wheel", tuple(parts[-3:])
    for suffix in (".tar.gz", ".zip"):
        if filename.endswith(suffix):
            name, sep, version = filename.removesuffix(suffix).partition("-")
            if name and sep and version:
                return normalized_name(name), version, "sdist", ("N/A", "N/A", "source")
    return None


def location_name(url):
    if not isinstance(url, str):
        return ""
    return unquote(urlsplit(url).path.rsplit("/", 1)[-1])


def raw_field(record, key):
    return dump(record[key]) if key in record else ""


def raw_type(value):
    if value is MISSING:
        return "missing"
    if value is None:
        return "null"
    if type(value) is bool:
        return "true" if value else "false"
    if isinstance(value, str):
        return "nonempty_string" if value else "empty_string"
    return type(value).__name__


def json_flag(record):
    value = record.get("yanked", MISSING)
    return raw_type(value), value if type(value) is bool else None


def simple_flag(record):
    value = record.get("yanked", MISSING)
    if type(value) is bool:
        return raw_type(value), value
    if isinstance(value, str) and value:
        return "nonempty_string", True
    return raw_type(value), None


def compare(a, b):
    if a is None or b is None:
        return "unavailable"
    return "match" if a == b else "mismatch"


def reason_relation(json_record, simple_record, j_flag, s_flag):
    if j_flag is None or s_flag is None or j_flag != s_flag:
        return "unavailable"
    reason = json_record.get("yanked_reason", MISSING)
    reason_kind = raw_type(reason)
    simple_value = simple_record["yanked"]
    if isinstance(simple_value, str):
        if reason_kind != "nonempty_string":
            return f"json_{reason_kind}_simple_reason"
        return "exact" if reason == simple_value else "reason_mismatch"
    if reason_kind == "null":
        return "no_reason_exposed"
    return f"json_{reason_kind}_simple_{raw_type(simple_value)}"


def sha256_value(record, key):
    hashes = record.get(key)
    return hashes.get("sha256") if isinstance(hashes, dict) else None


def compare_sha(a, b):
    if not all(isinstance(value, str) and SHA256.fullmatch(value) for value in (a, b)):
        return "missing_or_invalid"
    return compare(a.lower(), b.lower())


def datetime_utc(raw):
    if not isinstance(raw, str):
        return None
    try:
        value = datetime.fromisoformat(raw)
    except ValueError:
        return None
    return value if value.utcoffset() is not None else None


def read_receipts(directory, group):
    expected = dict((sid, (project, version, url, mime)) for sid, project, version, url, mime in endpoints(group))
    receipts = json.loads((directory / "http.json").read_text(encoding="utf-8"))
    if Counter(row["source_id"] for row in receipts) != Counter(expected.keys()):
        raise ValueError(f"{directory}: missing or duplicate endpoint receipt")
    documents = {}
    for receipt in receipts:
        sid = receipt["source_id"]
        identity = tuple(receipt[k] for k in ("project", "version", "request_url", "request_accept"))
        if identity != expected[sid]:
            raise ValueError(f"{sid}: incorrect endpoint identity")
        body = None
        if receipt["body"] is not None:
            body = gzip.decompress((directory / receipt["body"]).read_bytes())
            if len(body) != receipt["body_bytes"] or hashlib.sha256(body).hexdigest() != receipt["sha256"]:
                raise ValueError(f"{sid}: response body fingerprint mismatch")
        if receipt["error"]:
            continue
        actual_type = (receipt["content_type"] or "").split(";", 1)[0].strip().lower()
        if receipt["http_status"] != 200 or body is None or actual_type != expected[sid][-1]:
            raise ValueError(f"{sid}: receipt marked successful without matching response")
        documents[sid] = body
    return receipts, documents


def parse_html(data, project, version):
    """Read Warehouse's current release header and file table from the saved page."""
    content = data.decode("utf-8")
    title = re.search(r'<h1 class="project-header__name">([^<]+)</h1>', content)
    cards = list(re.finditer(r'class="release release--current( release--yanked)?"', content))
    if title is None or unescape(title[1]).strip() != f"{project} {version}" or len(cards) != 1:
        raise ValueError(f"{project} {version}: release heading/card missing or wrong")
    if 'id="files"' not in content:
        raise ValueError(f"{project} {version}: file tab missing")
    banner = re.search(r'class="project-status project-status--yanked"', content)
    reason = re.search(r'<strong>Reason given by maintainers:</strong>(.*?)</p>', content, re.S)
    preferred = re.search(r'Consider using <a href="([^"]+)"', content)
    dates = set(re.findall(r'<strong>Yanked:</strong>\s*<time datetime="([^"]+)"', content))
    if len(dates) > 1:
        raise ValueError(f"{project} {version}: inconsistent Key dates")
    files = defaultdict(list)
    for match in re.finditer(r'<span class="file-info__name">\s*<a href="([^"]+)"', content):
        url = unescape(match[1])
        files[location_name(url)].append(content.count("\n", 0, match.start(1)) + 1)
    return {
        "banner": bool(banner), "current_card_yanked": bool(cards[0][1]),
        "banner_line": content.count("\n", 0, banner.start()) + 1 if banner else None,
        "current_card_line": content.count("\n", 0, cards[0].start()) + 1,
        "reason": unescape(reason[1]).strip() if reason else None,
        "key_dates_yanked_datetime_raw": next(iter(dates), None),
        "preferred_url": urljoin("https://pypi.org", preferred[1]) if preferred else None,
        "files": dict(files),
    }


def read_baseline(path):
    baseline, deleted_groups = {}, []
    with path.open(encoding="utf-8", newline="") as f:
        for line, row in enumerate(csv.DictReader(f), 2):
            row["csv_line"] = line
            if row["listing_status"] != "listed":
                deleted_groups.append(row)
                continue
            key = (row["project"], row["version"], row["filename"])
            if key in baseline:
                raise ValueError(f"duplicate baseline key: {key}")
            baseline[key] = row
    return baseline, deleted_groups


def collect_records(version_documents, simple_documents, scope):
    versions, simple = defaultdict(list), defaultdict(list)
    ignored, stray = Counter(), []
    for (project, version), (source, doc) in version_documents.items():
        for index, record in enumerate(doc["urls"]):
            key = (project, version, record["filename"])
            versions[key].append((f"{source}#/urls/{index}", record))
    for project, (source, doc) in simple_documents.items():
        for index, record in enumerate(doc["files"]):
            filename = record["filename"]
            pointer = f"{source}#/files/{index}"
            parsed = filename_parts(filename)
            if parsed is None:
                ignored[(project, "unparsed")] += 1
                if any(filename.startswith(f"{p}-{v}-") for p, v in scope if p == project):
                    stray.append({"location": pointer, "record": record, "issue": "unparsed_target_like_filename"})
                continue
            file_project, version, _, _ = parsed
            if (project, version) not in scope:
                ignored[(project, "outside_fixed_versions")] += 1
                continue
            if project != file_project:
                stray.append({"location": pointer, "record": record, "issue": "wrong_simple_project"})
                continue
            simple[project, version, filename].append((pointer, record))
    return versions, simple, {
        "ignored_simple_records": {f"{p}/{reason}": n for (p, reason), n in sorted(ignored.items())},
        "unjoined_target_like_simple_records": stray,
    }


def availability(j_count, s_count, json_available, simple_available):
    if not json_available or not simple_available:
        unavailable = [name for name, available in (("json", json_available), ("simple", simple_available))
                       if not available]
        return "_and_".join(unavailable) + "_unavailable"
    return {(True, True): "both", (True, False): "json_only", (False, True): "simple_only",
            (False, False): "both_absent"}[bool(j_count), bool(s_count)]


def file_row(key, baseline, json_records, simple_records, json_available, simple_available, html):
    project, version, filename = key
    parsed = filename_parts(filename)
    file_type, tags = parsed[2:] if parsed else ("unparsed", ("", "", ""))
    issues = []
    if not parsed or parsed[:2] != key[:2]:
        issues.append("filename_identity_mismatch")
    json_count, simple_count = len(json_records), len(simple_records)
    if json_count > 1:
        issues.append("duplicate_version_filename")
    if simple_count > 1:
        issues.append("duplicate_simple_filename")
    joined = availability(json_count, simple_count, json_available, simple_available)

    old = baseline.get(key)
    if old and (file_type, *tags) != tuple(old[k] for k in ("file_type", "python_tag", "abi_tag", "platform_tag")):
        issues.append("baseline_tag_mismatch")
    j_record = json_records[0][1] if json_count == 1 else {}
    s_record = simple_records[0][1] if simple_count == 1 else {}
    j_type, j_flag = json_flag(j_record)
    s_type, s_flag = simple_flag(s_record)
    j_reason = raw_type(j_record.get("yanked_reason", MISSING))
    j_hash = sha256_value(j_record, "digests")
    s_hash = sha256_value(s_record, "hashes")
    j_url, s_url = j_record.get("url"), s_record.get("url")
    for label, record in (("json", j_record), ("simple", s_record)):
        if record and location_name(record.get("url")) != filename:
            issues.append(f"{label}_url_filename_mismatch")
    if j_record and parsed:
        expected_package = {"wheel": "bdist_wheel", "sdist": "sdist"}[file_type]
        if j_record.get("packagetype") != expected_package:
            issues.append("json_packagetype_mismatch")
        expected_python = tags[0] if file_type == "wheel" else "source"
        if j_record.get("python_version") != expected_python:
            issues.append("json_python_tag_mismatch")
    if j_url and s_url and filename_parts(location_name(j_url)) != filename_parts(location_name(s_url)):
        issues.append("link_tag_mismatch")

    j_upload, s_upload = j_record.get("upload_time_iso_8601"), s_record.get("upload-time")
    digest_compare = compare_sha(j_hash, s_hash) if j_record and s_record else "unavailable"
    flag_compare = compare(j_flag, s_flag)
    reason_compare = reason_relation(j_record, s_record, j_flag, s_flag)
    upload_compare = compare(datetime_utc(j_upload), datetime_utc(s_upload))
    requires_compare = compare(j_record.get("requires_python"), s_record.get("requires-python"))
    url_compare = compare(j_url, s_url)
    if j_record and s_record:
        for field, status in (("sha256", digest_compare), ("flag", flag_compare),
                              ("upload", upload_compare), ("requires_python", requires_compare),
                              ("url", url_compare)):
            if status != "match":
                issues.append(f"{field}_{status}")
        if reason_compare not in ("exact", "no_reason_exposed", "unavailable"):
            issues.append(f"reason_{reason_compare}" if not reason_compare.startswith("reason_") else reason_compare)

    html_compare = "unavailable"
    html_lines = []
    if html is not None:
        html_lines = html["files"].get(filename, [])
        if len(html_lines) != 1:
            issues.append("html_filename_missing" if not html_lines else "duplicate_html_filename")
        if html["banner"] != html["current_card_yanked"]:
            issues.append("html_banner_current_card_mismatch")
        if j_flag is not None and s_flag is not None:
            agrees = html["banner"] == j_flag == s_flag
            if agrees and j_flag and html["reason"] != j_record.get("yanked_reason"):
                agrees = False
            html_compare = "match" if agrees else "mismatch"
            if not agrees:
                issues.append("html_banner_or_reason_mismatch")

    tag_issues = any("tag" in issue or issue in ("filename_identity_mismatch", "json_packagetype_mismatch")
                     for issue in issues)
    return dict(
        project=project, version=version, filename=filename,
        cohort="target" if key[:2] in TARGETS else "adjacent",
        baseline="existing" if old else "new", baseline_source_id=old["source_id"] if old else "",
        baseline_csv_line=old["csv_line"] if old else "", file_type=file_type,
        python_tag=tags[0], abi_tag=tags[1], platform_tag=tags[2], join=joined,
        json_count=json_count, simple_count=simple_count,
        json_positions=dump([p for p, _ in json_records]), simple_positions=dump([p for p, _ in simple_records]),
        json_duplicate_records=dump(json_records) if json_count > 1 else "",
        simple_duplicate_records=dump(simple_records) if simple_count > 1 else "",
        json_sha256=j_hash, simple_sha256=s_hash, sha256_comparison=digest_compare,
        json_packagetype=j_record.get("packagetype"), json_python_version=j_record.get("python_version"),
        tag_comparison="mismatch" if tag_issues else "match" if json_count == simple_count == 1 else "unavailable",
        json_yanked_type=j_type if json_count == 1 else "duplicate" if json_count else "absent_record",
        json_yanked_raw=raw_field(j_record, "yanked"), json_reason_type=j_reason,
        json_reason_raw=raw_field(j_record, "yanked_reason"),
        simple_yanked_type=s_type if simple_count == 1 else "duplicate" if simple_count else "absent_record",
        simple_yanked_raw=raw_field(s_record, "yanked"),
        simple_reason_type=s_type if s_type in ("nonempty_string", "empty_string") else "not_separate",
        flag_comparison=flag_compare, reason_comparison=reason_compare,
        json_upload_utc_raw=j_upload, simple_upload_utc_raw=s_upload, upload_comparison=upload_compare,
        json_requires_python_raw=raw_field(j_record, "requires_python"),
        simple_requires_python_raw=raw_field(s_record, "requires-python"),
        requires_python_comparison=requires_compare, json_url=j_url, simple_url=s_url, url_comparison=url_compare,
        html_file_lines=dump(html_lines), html_banner=html["banner"] if html is not None else "",
        html_yanked_datetime_raw=html["key_dates_yanked_datetime_raw"] if html is not None else None,
        html_comparison=html_compare, issues=issues,
    )


def reconcile(baseline, version_documents, simple_documents, html_documents, scope):
    versions, simple, index_notes = collect_records(version_documents, simple_documents, scope)
    # Only full keys cross sources. A mislabelled version object remains visible as an issue.
    merged = sorted(baseline.keys() | versions.keys() | simple.keys())
    rows = [file_row(key, baseline, versions.get(key, []), simple.get(key, []),
                     key[:2] in version_documents, key[0] in simple_documents, html_documents.get(key[:2]))
            for key in merged]
    return rows, index_notes


def summarize(rows):
    return {
        "keys": len(rows), "baseline": sum(r["baseline"] == "existing" for r in rows),
        "current_union": sum(bool(r["json_count"] or r["simple_count"]) for r in rows),
        "new_keys": sum(r["baseline"] == "new" for r in rows),
        "join_counts": dict(Counter(r["join"] for r in rows)),
        "json_records": sum(r["json_count"] for r in rows), "simple_records": sum(r["simple_count"] for r in rows),
        "sha256_match": sum(r["sha256_comparison"] == "match" for r in rows),
        "tag_match": sum(r["tag_comparison"] == "match" for r in rows),
        "upload_match": sum(r["upload_comparison"] == "match" for r in rows),
        "requires_python_match": sum(r["requires_python_comparison"] == "match" for r in rows),
        "url_match": sum(r["url_comparison"] == "match" for r in rows),
        "html_match": sum(r["html_comparison"] == "match" for r in rows),
        "both_with_no_issues": sum(r["join"] == "both" and not r["issues"] for r in rows),
        "json_flags": dict(Counter(r["json_yanked_type"] for r in rows)),
        "simple_flags": dict(Counter(r["simple_yanked_type"] for r in rows)),
        "reason_comparisons": dict(Counter(r["reason_comparison"] for r in rows)),
        "issues": dict(Counter(issue for r in rows for issue in r["issues"])),
    }


def write_results(args):
    baseline, deleted_groups = read_baseline(args.baseline)
    api, decoded = read_receipts(args.api, "api")
    html, pages = read_receipts(args.html, "html")
    version_documents, simple_documents, html_documents = {}, {}, {}
    for record in api:
        sid, project, version = [record[key] for key in ("source_id", "project", "version")]
        if sid not in decoded:
            continue
        obj = json.loads(decoded[sid])
        if version:
            if (normalized_name(obj["info"]["name"]), obj["info"]["version"]) != (project, version):
                raise ValueError(f"{sid}: version identity mismatch")
            version_documents[project, version] = (sid, obj)
        else:
            if normalized_name(obj["name"]) != project:
                raise ValueError(f"{sid}: project identity mismatch")
            simple_documents[project] = (sid, obj)
    for record in html:
        sid, project, version = [record[key] for key in ("source_id", "project", "version")]
        if sid in pages:
            html_documents[project, version] = parse_html(pages[sid], project, version)

    rows, index_notes = reconcile(baseline, version_documents, simple_documents, html_documents, set(RELEASES))
    releases = {}
    for key in RELEASES:
        selected = [row for row in rows if (row["project"], row["version"]) == key]
        r = summarize(selected)
        uploads = [row["json_upload_utc_raw"] for row in selected if row["json_upload_utc_raw"]]
        r["upload_utc_range"] = [min(uploads), max(uploads)] if uploads else []
        r["requires_python"] = sorted({row["json_requires_python_raw"] for row in selected})
        r["windows_wheels"] = sum(row["file_type"] == "wheel" and row["platform_tag"].startswith("win")
                                  and (row["json_count"] or row["simple_count"]) > 0 for row in selected)
        version_document = version_documents.get(key)
        if version_document:
            info = version_document[1]["info"]
            r["version_info_context"] = {name: info[name] for name in ("yanked", "yanked_reason", "requires_python")
                                         if name in info}
        if key in html_documents:
            page = html_documents[key]
            file_names = {row["filename"] for row in selected if row["json_count"] or row["simple_count"]}
            r["html"] = {name: value for name, value in page.items() if name != "files"}
            r["html"]["files"] = len(page["files"])
            r["html"]["html_only"] = sorted(page["files"].keys() - file_names)
            r["html"]["api_only"] = sorted(file_names - page["files"].keys())
        releases["/".join(key)] = r
    summary = {
        "kind": "observed_public_https_replay", "baseline_sha256": hashlib.sha256(args.baseline.read_bytes()).hexdigest(),
        "api_ok": len(decoded), "html_ok": len(html_documents),
        "endpoint_errors": [{"id": r["source_id"], "url": r["request_url"], "error": r["error"]}
                            for r in api + html if r["error"]],
        "deleted_groups": [{key: r[key] for key in ("project", "version", "listing_status", "csv_line")}
                           for r in deleted_groups],
        "overall": summarize(rows),
        "target": summarize([row for row in rows if row["cohort"] == "target"]),
        "adjacent": summarize([row for row in rows if row["cohort"] == "adjacent"]),
        "releases": releases,
        **index_notes,
    }
    args.out.mkdir(parents=True, exist_ok=False)
    with (args.out / "files.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FILE_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows({**row, "issues": dump(row["issues"])} for row in rows)
    (args.out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(dump({name: summary[name] for name in ("api_ok", "html_ok", "overall", "target", "adjacent")}))
    return int(bool(summary["endpoint_errors"]))


def run_controls(fixture, out):
    data = json.loads(fixture.read_text(encoding="utf-8"))
    if data["kind"] != "researcher_synthetic_not_pypi":
        raise ValueError("control fixture is not marked synthetic")
    results = []
    for scenario in data["scenarios"]:
        base = {(r["project"], r["version"], r["filename"]): r for r in scenario["baseline"]}
        versions = {(r["project"], r["version"]): (r["source_id"], r["body"])
                    for r in scenario["version_responses"]}
        simple = {r["project"]: (r["source_id"], r["body"]) for r in scenario["simple_responses"]}
        rows, notes = reconcile(base, versions, simple, {}, {tuple(key) for key in scenario["scope"]})
        rows_by_key = {(row["project"], row["version"], row["filename"]): row for row in rows}
        expected_keys = {tuple(check["key"]) for check in scenario["expected_rows"]}
        results.append({
            "id": scenario["id"] + "_keyset",
            "expected": {"keys": sorted(expected_keys), "ignored": scenario["expected_ignored"]},
            "actual": {"keys": sorted(rows_by_key), "ignored": notes["ignored_simple_records"]},
        })
        for check in scenario["expected_rows"]:
            row = rows_by_key.get(tuple(check["key"]), {})
            expected = check["fields"]
            actual = {field: row.get(field) for field in expected}
            results.append({"id": check["id"], "expected": expected, "actual": actual})
    for result in results:
        result["passed"] = result["actual"] == result["expected"]
        print(f"{result['id']} {'PASS' if result['passed'] else 'FAIL'}")
    report = {
        "kind": data["kind"], "fixture_sha256": hashlib.sha256(fixture.read_bytes()).hexdigest(),
        "passed": sum(result["passed"] for result in results), "total": len(results), "results": results,
    }
    out.mkdir(parents=True, exist_ok=False)
    (out / "controls-result.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return int(report["passed"] != report["total"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--api", type=Path)
    parser.add_argument("--html", type=Path)
    parser.add_argument("--controls", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    measured_inputs = (args.baseline, args.api, args.html)
    if args.controls:
        if any(measured_inputs):
            parser.error("--controls is separate from --baseline, --api and --html")
        return run_controls(args.controls, args.out)
    if not all(measured_inputs):
        parser.error("use --baseline, --api and --html for public response replay")
    return write_results(args)


if __name__ == "__main__":
    raise SystemExit(main())
