"""Recount the study and compare an independent replay to the sealed matrix."""
import argparse
from collections import Counter
import copy
import csv
import json
from pathlib import Path

from fixtures import blob, catalog

STUDY = Path(__file__).resolve().parent.parent
PLANNED = {"C3": 18, "C4": 36, "Y2": 51, "Y3": 20, "Y4": 12}
MINIMUM = {"issue": 5, "cli": 5, "upstream": 6, "contract": 2, "news": 2, "music": 2}


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf8").splitlines()]


def verify_bytes(info):
    if info is not None:
        assert blob(bytes.fromhex(info["hex"])) == {key: info[key] for key in ("size", "sha256", "hex")}


def audit_runs(runs, fixture_by_id, sources):
    assert dict(Counter(run["case"] for run in runs)) == PLANNED
    assert len({run["run_id"] for run in runs}) == len(runs)
    for run in runs:
        assert run["source_id"] in sources
        assert run["inputs"] == fixture_by_id[run["fixture"]]["files"]
        assert run["execution"] in {"success", "failure", "unknown"}
        before = run["inputs"]
        after = run["files_after"]
        for value in [*before.values(), *after.values()]:
            verify_bytes(value)
        assert {p for p in before.keys() | after.keys() if before.get(p) != after.get(p)} == set(run["changed_paths"])
        for command in run["commands"]:
            for key in ("stdin", "stdout", "stderr"):
                verify_bytes(command[key])
    index = {(r["fixture"],r["version"],r["variant"],r["locale"]):r for r in runs}
    def get(fixture, version, variant):
        return index[(fixture,version,variant,"C.UTF-8")]
    assert get("c3-public", "1.0.7","no-double")["commands"][0]["exit_code"] == 1
    escape = get("c3-public","1.0.7","escape-x")["reinterpreted"]
    assert escape["declared"]["equals_input_fields"] and not escape["bare_tsv"]["equals_input_fields"]
    tilde = get("c3-special","1.0.7","quote-tilde")["reinterpreted"]
    assert tilde["declared"]["equals_input_fields"] and tilde["bare_tsv"]["columns_per_record"][1] == 3
    for version in ("1.0.5","1.1.0"):
        assert get("c4-public",version,"pipe")["reinterpreted"]["csvstat_date_column"]["Type of data"] == "Date"
        mixed = get("c4-mixed",version,"pipe")
        assert mixed["execution"] == "success" and mixed["reinterpreted"]["csvstat_date_column"]["Type of data"] == "Text"
        assert get("c4-ambiguous-only",version,"direct")["reinterpreted"]["csvstat_date_column"]["Largest value"] == "2023-04-05"
        assert get("c4-ambiguous-only",version,"pipe")["reinterpreted"]["csvstat_date_column"]["Largest value"] == "2023-05-04"
    assert get("y2-lf3","4.30.6","merge")["execution"] == "failure"
    for version in ("4.30.5","4.30.7"):
        assert get("y2-lf3",version,"merge")["reinterpreted"]["output"]["values"] == [{"test":None}]
    for fixture in ("y2-cr3","y2-crlf3"):
        assert get(fixture,"4.30.6","merge")["execution"] == "success"
    crlf = get("y3-crlf-tail","4.30.6","literal")["reinterpreted"]
    normalized = get("y3-crlf-tail","4.30.6","lf-copy")["reinterpreted"]
    assert crlf["scalar"]["equals_original_bytes"] and crlf["scalar"]["terminal"] == "CRLF"
    assert normalized["scalar"]["equals_loaded_bytes"] and not normalized["scalar"]["equals_original_bytes"]
    assert normalized["scalar"]["terminal"] == "LF"
    assert get("y4-public","4.30.6","prepend")["reinterpreted"]["matches_requested_order"]
    for variant, flow in (("prepend",False),("prepend-assign",True)):
        out = get("y4-styled-flow","4.30.6",variant)
        assert out["reinterpreted"]["output"]["nodes"][0]["flow"] == flow
        assert ("# sequence end" in out["commands"][0]["stdout"]["text"]) == flow


def normal(run):
    output = copy.deepcopy(run)
    for key in ("cwd", "observed_utc"):
        output.pop(key)
    for cmd in output["commands"]:
        binary = Path(cmd["argv"][0])
        install = binary.parents[2 if run["case"].startswith("C") else 1]
        cmd["argv"][0] = str(binary.relative_to(install))
        # Python tracebacks print the actual environment's absolute location; substitute only this prefix.
        stderr = bytes.fromhex(cmd["stderr"]["hex"])
        scrubbed = stderr.replace(str(install).encode()+b"/", b"@install/")
        cmd["stderr"] = {**blob(scrubbed), "text": scrubbed.decode("utf8", errors="backslashreplace")}
    return output


def compare(sealed, other):
    assert len(sealed) == len(other)
    original = {row["run_id"]:row for row in sealed}
    repeated = {row["run_id"]:row for row in other}
    assert original.keys() == repeated.keys()
    differences = [key for key in original if normal(original[key]) != normal(repeated[key])]
    assert not differences, differences
    return {
        "equal_input_and_semantics_rows": len(original),
        "stdout_bytes_equal_rows": sum([c["stdout"]["sha256"] for c in original[k]["commands"]]
                                      == [c["stdout"]["sha256"] for c in repeated[k]["commands"]] for k in original),
        "raw_stderr_changed_rows": sorted(k for k in original if [c["stderr"]["sha256"] for c in original[k]["commands"]]
                                         != [c["stderr"]["sha256"] for c in repeated[k]["commands"]]),
        "raw_envelopes_changed_rows": sum(original[k] != repeated[k] for k in original),
        "normalized_fields": ["cwd", "observed_utc", "argv[0] install prefix", "stderr install prefix"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", type=Path, action="append", default=[])
    opts = parser.parse_args()
    catalog_rows = jsonl(STUDY/"fixtures.jsonl")
    assert catalog_rows == catalog()
    fixtures = {row["id"]:row for row in catalog_rows}
    source_rows = jsonl(STUDY/"sources.jsonl")
    sources = {row["source_id"]:row for row in source_rows}
    counted = [row for row in source_rows if row["counted"]]
    assert len(sources) == len(source_rows)
    assert len({row["work_id"] for row in counted}) == len(counted)
    groups = Counter(row["category"] for row in counted)
    assert sum(groups.values()) >= 22 and all(groups[group] >= total for group,total in MINIMUM.items())
    with (STUDY/"timeline.csv").open() as stream:
        time = list(csv.DictReader(stream))
    with (STUDY/"decisions.csv").open() as stream:
        decisions = list(csv.DictReader(stream))
    assert len(decisions) == len({r["case"] for r in decisions}) == 5
    assert all(r["selected_link_id"] in sources for r in decisions)
    issue = [r for r in time if r["layer"]=="current-issue"]
    comment = [r for r in time if r["layer"]=="followup-comment"]
    runs = jsonl(STUDY/"runs.jsonl")
    audit_runs(runs, fixtures, sources)
    result = {
        "sources": {"read_rows": len(sources), "counted_works": len(counted), "by_category": groups},
        "timeline": {"issue_rows":len(issue),"proven_first_editions":sum(r["first_edition"]=="proven" for r in issue),
                     "comments":len(comment),"html_created_at":sum(bool(r["created_html"]) for r in comment),
                     "html_last_edited_at":sum(bool(r["last_edited_html"]) for r in comment),
                     "rest_updated_at":sum(bool(r["rest_updated_at"]) for r in comment)},
        "fixtures": {"total":len(fixtures),"by_grade":Counter(r["grade"] for r in catalog_rows)},
        "runs": {"by_case":PLANNED,"total":len(runs),"commands":sum(len(r["commands"]) for r in runs),
                 "states":Counter(r["execution"] for r in runs)},
        "decision_technical_gate_misclassified": [r["case"] for r in decisions if r["technical_gate_misclassified"]=="True"],
        "replays": [],
    }
    for path in opts.replay:
        other = jsonl(path)
        audit_runs(other, fixtures, sources)
        result["replays"].append({"path":str(path),**compare(runs,other)})
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
