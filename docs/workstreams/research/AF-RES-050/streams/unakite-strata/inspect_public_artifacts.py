"""Read-only inspection of two author-published static artifacts.

No browser execution, authentication, database requests, participant export,
archive extraction, or repository mutation. The output describes public source
structure and aggregate chart caches only; it is not experimental microdata.
Run: python -B <this file> {strata|unakite}
"""

import datetime
import hashlib
import io
import json
import pathlib
import re
import sys
import tarfile
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read(35_000_001)
    if len(data) > 35_000_000:
        raise RuntimeError("Unexpected artifact size; inspect manually")
    return data


def digest(data):
    return hashlib.sha256(data).hexdigest()


def strata():
    url = "https://arxiv.org/src/2102.06231v2"
    data = fetch(url)
    ns = {"c": "http://schemas.openxmlformats.org/drawingml/2006/chart"}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        names = archive.getnames()
        chart_path = "assets/images/ppt/charts/chart1.xml"
        chart_data = archive.extractfile(chart_path).read()
        chart = ET.fromstring(chart_data)
        rows = []
        for series in chart.findall(".//c:ser", ns):
            condition = series.find("c:tx/c:strRef/c:strCache/c:pt/c:v", ns).text
            cats = series.findall("c:cat/c:strRef/c:strCache/c:pt/c:v", ns)
            values = series.findall("c:val/c:numRef/c:numCache/c:pt/c:v", ns)
            ref = series.find("c:val/c:numRef/c:f", ns).text
            for i, (cat, value) in enumerate(zip(cats, values)):
                rows.append({"condition": condition, "task": cat.text,
                             "recall_cache_fraction": float(value.text),
                             "cache_index": i, "workbook_formula": ref})
        rel_path = "assets/images/ppt/charts/_rels/chart1.xml.rels"
        rel_data = archive.extractfile(rel_path).read()
        relationships = []
        for rel in ET.fromstring(rel_data):
            target = rel.attrib.get("Target", "")
            # A local author pathname appears in the public source. Retain
            # only the workbook basename needed to locate the missing file.
            relationships.append({
                "relationship_type": rel.attrib.get("Type", "").rsplit("/", 1)[-1],
                "mode": rel.attrib.get("TargetMode"),
                "scheme": urllib.parse.urlparse(target).scheme,
                "target_basename": pathlib.PurePosixPath(
                    urllib.parse.unquote(target).replace("\\", "/")
                ).name,
            })
        raw_candidates = [n for n in names if pathlib.PurePosixPath(n).suffix.lower()
                          in {".csv", ".tsv", ".xlsx", ".xls", ".r", ".py"}]
    keys = [(r["condition"], r["task"]) for r in rows]
    return {"url": url, "sha256": digest(data), "member_count": len(names),
            "raw_file_suffix_candidates": raw_candidates,
            "chart_path": chart_path, "chart_sha256": digest(chart_data),
            "aggregate_rows": rows, "row_count": len(rows),
            "unique_condition_task_keys": len(set(keys)),
            "relationship_path": rel_path,
            "relationship_sha256": digest(rel_data),
            "relationships_redacted": relationships,
            "participant_rows": "미확인; aggregate caches only"}


def unakite():
    url = "https://unakite-v2.firebaseapp.com/static/js/main.bb8e5ba3.js.map"
    data = fetch(url)
    obj = json.loads(data)
    targets = ["task_functions.js", "piece_functions.js", "timer_functions.js",
               "instrument_v1_event_types.js", "instrument_v1_functions.js",
               "ActivityStats.js"]
    sources = []
    caller_terms = ["setTaskStartTime", "setTaskEndTime", "addActionTimestamps"]
    callers = {term: [] for term in caller_terms}
    for index, (name, content) in enumerate(zip(obj["sources"], obj["sourcesContent"])):
        if not content or index == 0 or "/node_modules/" in name:
            continue
        lines = content.splitlines()
        if name.rsplit("/", 1)[-1] in targets:
            sources.append({"index": index, "source": name,
                            "lines": len(lines), "sha256": digest(content.encode())})
        if name.endswith("timer_functions.js"):
            continue
        for term in caller_terms:
            for number, line in enumerate(lines, 1):
                if term in line:
                    callers[term].append({"source": name, "line": number})
    return {"url": url, "sha256": digest(data),
            "source_count": len(obj["sources"]), "inspected_sources": sources,
            "symbol_references_outside_definition": callers,
            "observation": "Static schemas and possible recording paths, not released study records",
            "study_build_identity": "미확인",
            "participant_rows": "미확인; no database access performed"}


if __name__ == "__main__":
    modes = {"strata": strata, "unakite": unakite}
    if len(sys.argv) != 2 or sys.argv[1] not in modes:
        raise SystemExit("Usage: python -B inspect_public_artifacts.py {strata|unakite}")
    result = modes[sys.argv[1]]()
    result["checked_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(json.dumps(result, ensure_ascii=False, indent=2))
