"""Check the stored pandas evidence without fetching or executing any date transform."""
import csv
import datetime
import hashlib
import json
import pathlib
import re

P = pathlib.Path(__file__).resolve().parent

def read_json(name):
    return json.loads((P / name).read_text())

def read_csv(name):
    with (P / name).open(newline="") as handle:
        return list(csv.DictReader(handle))

def main():
    checks = []
    def require(name, condition):
        checks.append({"name": name, "passed": bool(condition)})
        if not condition:
            raise AssertionError(name)

    seal = read_json("frame-seal.json")
    census = read_json("title-census.json")
    pattern = re.compile(seal["regex"], re.I)
    expected = sorted((x for x in census if pattern.search(x["title"])),
                      key=lambda x: (x["created_at"], x["number"]))[:30]
    frame = read_csv("frame.csv")
    require("unique title census 1899", len(census) == len({x["number"] for x in census}) == 1899)
    require("frame equals title-only earliest30", [int(x["issue_number"]) for x in frame] == [x["number"] for x in expected])
    require("selection first3 eligible", [x["case_id"] for x in frame if x["eligible"] == "True"][:3] == ["N-P1", "N-P2", "N-P3"])
    acquisition = read_json("body-acquisition.json")
    require("30 successful body opens", len(acquisition) == 30 and all(x["status"] == 200 for x in acquisition))
    utc = lambda value: datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    require("all body opens after frame seal", all(utc(x["opened_utc"]) > utc(seal["sealed_utc"]) for x in acquisition))
    contexts = read_json("report-context.json")
    require("body metadata fingerprints retained", {x["number"]: x["body_sha256"] for x in acquisition} == {x["number"]: x["body_sha256"] for x in contexts})

    receipts = read_json("receipts.json")
    views = read_json("views.json")
    candidates = read_json("candidate-editions.json")
    require("selected receipt count3", len(receipts) == len(read_csv("receipts.csv")) == 3)
    require("date output2 any output3", sum(x["date_output_published"] for x in receipts) == 2 and all(x["any_output_published"] for x in receipts))
    require("loaded edition0 full chain0", not any(x["loaded_tzdb_version_confirmed"] or x["same_process_full_chain"] for x in receipts))
    require("N-P2 call conflict separate from value presence", receipts[1]["date_output_published"] and receipts[1]["declared_call_value_consistent"] is False)
    require("N-P3 error not calendar output", not receipts[2]["date_output_published"] and receipts[2]["any_output_published"])
    require("9 distinct view cells", len(views) == len(read_csv("views.csv")) == len({(x["case_id"], x["view"]) for x in views}) == 9)
    require("8 candidate rows", len(candidates) == len(read_csv("candidate-editions.csv")) == 8)
    wheels = read_json("candidate-member-evidence.json")["rows"]
    require("two public wheels hash verified", len(wheels) == 2 and all(x["registry_match"] and x["archive_sha256"] == x["registry_sha256"] for x in wheels))
    require("Berlin bytes identical while archives differ", len({x["berlin_member"]["sha256"] for x in wheels}) == 1 and len({x["archive_sha256"] for x in wheels}) == 2)
    require("raw whole issue/comment caches removed", not (P / "body-snapshots.jsonl").exists() and not (P / "comment-snapshots.json").exists())

    sources = [json.loads(x) for x in (P / "sources.jsonl").read_text().splitlines() if x]
    require("43 unique source records", len(sources) == len({x["source_id"] for x in sources}) == 43)
    require("all selected sources exist", all(x["source_id"] in {s["source_id"] for s in sources} for x in receipts))
    missing = []
    for url in re.findall(r"\]\(([^)]+)\)", (P / "notes.md").read_text()):
        if "://" not in url and not (P / url.split("#")[0]).exists():
            missing.append(url)
    require("notes local links resolve", not missing)
    inputs = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(P.iterdir())
              if path.is_file() and path.name not in {"validation.json"}}
    result = {"checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "checker": "pandas_reports agent / provided Linux Python",
              "command": "python -B docs/workstreams/research/AF-RES-063/evidence/pandas/validate.py",
              "exit_code": 0, "checks": checks, "input_sha256": inputs,
              "scope": "Stored frame, receipt, source and count/link consistency only",
              "not_performed": ["historical date transform replay", "historical process/file identity", "root workbench.session check", "remote fixed-commit re-open"]}
    (P / "validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"checks": len(checks), "passed": len(checks), "exit_code": 0}))

if __name__ == "__main__":
    main()

