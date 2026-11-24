"""Read-only integrity verification of AF-RES-106 research artifacts.

Checks ledgers, sealed inputs, actual path membership, captured fragment IDs,
payload/source bytes, source admissions, and required table shapes. Does not
execute external examples or certify semantic judgements/historical builds.
"""
from pathlib import Path
import csv
import datetime
import hashlib
import importlib.util
import json
import re
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]


class Ids(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])


def read(name):
    return json.loads((ROOT / name).read_text())


def csv_read(name):
    with (ROOT / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    checks = []

    def check(label, condition, detail=None):
        checks.append({"check": label, "passed": bool(condition), "detail": detail})

    spec = importlib.util.spec_from_file_location("recalculate", ROOT / "tools/recalculate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fresh = mod.calculate()
    check("recalculation gates", fresh["passed"], [x for x in fresh["checks"] if not x["passed"]])
    check("counts.json exact recalculation", fresh == read("counts.json"))

    for row in read("evidence/stage2-seal-manifest.json")["sealed_files"]:
        check("sealed " + row["path"], hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"])

    frame = csv_read("frame.csv")
    trees = {}
    for project, prefix in [("ggplot2", "ggplot2"), ("Matplotlib", "matplotlib")]:
        document = read("evidence/" + prefix + "/new-publication-tree.json")
        check(project + " new publication tree complete", document.get("truncated") is False)
        trees[project] = {r["path"] for r in document["tree"] if r["type"] == "blob"}
    mismatches = []
    for row in frame:
        if row["eligible"] != "YES":
            continue
        project = "Matplotlib" if row["project"].lower() == "matplotlib" else "ggplot2"
        present = row["old_resource_path"] in trees[project]
        stated = row.get("new_legacy_asset_present") or row.get("legacy_path_present")
        if stated != ("YES" if present else "NO"):
            mismatches.append(row["old_section_path"])
    check("all547 legacy resource membership from raw tree", not mismatches, mismatches)

    # Only committed-preservable evidence locations, never ignored network caches.
    fingerprints = {}
    for folder in ["evidence/ggplot2/raw", "evidence/ggplot2/payloads", "evidence/matplotlib/payloads", "evidence/matplotlib/observations"]:
        for path in (ROOT / folder).glob("*"):
            if path.is_file():
                fingerprints.setdefault(hashlib.sha256(path.read_bytes()).hexdigest(), []).append(str(path.relative_to(ROOT)))
    for row in csv_read("lineage.csv"):
        if row["vacant"] == "YES":
            continue
        stem = row["case_id"] + "-" + row["edition"]
        check(stem + " payload bytes preserved", row["payload_sha256"] in fingerprints)
        check(stem + " source bytes preserved", row["source_sha256"] in fingerprints)
        if row["project"] == "ggplot2":
            filename = row["section_url"].split("#", 1)[0].rsplit("/", 1)[-1]
            path = ROOT / "evidence/ggplot2/raw" / (row["edition"] + "-body-" + filename)
        else:
            path = ROOT / "evidence/matplotlib/observations" / (stem + "-section.html")
        ids = Ids()
        ids.feed(path.read_text())
        check(stem + " actual fragment in preserved HTML", row["actual_fragment"] in ids.ids)

    sources = [json.loads(line) for line in (ROOT / "sources.jsonl").read_text().splitlines() if line.strip()]
    for row in sources:
        if not row["countable"]:
            continue
        value = row["accessed_utc"]
        try:
            datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
            valid_time = True
        except (ValueError, TypeError):
            valid_time = False
        check(row["id"] + " primary source URL/time", row["original_url"].startswith("https://") and valid_time)
        check(row["id"] + " preserved evidence location", isinstance(row["preserved_location"], str) and (ROOT / row["preserved_location"]).is_file())
    check("count allowlist equals independent38", {s["id"] for s in sources if s["countable"]} == set(read("evidence/crossdomain/source-count-review.json")["counted_ids"]))

    result = (ROOT / "RESULT.md").read_text()
    blocks = re.findall(r"(?:^\|.*\n)+", result, re.M)
    table_sizes = [len(b.strip().splitlines()) - 2 for b in blocks]
    check("RESULT starts with required12/24/12 tables", result.startswith("|") and table_sizes[:3] == [12, 24, 12], table_sizes[:3])
    check("RESULT ends with exactly3 weakness rows", table_sizes[-1] == 3 and result.rstrip().endswith(blocks[-1].rstrip()))
    check("SELF_CHECK has7 question rows", len(re.findall(r"^\| Q[1-7] ", (ROOT / "SELF_CHECK.md").read_text(), re.M)) == 7)
    report = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "passed": all(r["passed"] for r in checks),
              "checks": len(checks), "failed": [r for r in checks if not r["passed"]],
              "scope": "Deterministic ledger/source/fragment/table integrity, no runtime/browser/historical G validation"}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
