"""Check frozen source identities and the receipt ledger without the audit code."""
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
DATA = HERE.parent
REPO = Path(subprocess.check_output(["git", "-C", str(DATA), "rev-parse", "--show-toplevel"], text=True).strip())
FILES = {"bundle.json", "segments.csv", "assignments.csv", "source-units.csv"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(name):
    return json.loads((DATA / name).read_bytes())


def read_lines(name):
    return [json.loads(line) for line in (DATA / name).read_bytes().splitlines()]


def git_show(ref):
    return subprocess.check_output(["git", "-C", str(REPO), "show", ref])


def read_csv(name):
    with (DATA / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    inputs = read_json("inputs.json")
    for record in inputs["artifacts"].values():
        ref = record["commit"] + ":" + record["path"]
        data = git_show(ref)
        assert digest(data) == record["sha256"] and len(data) == record["bytes"], ref
    assert len(inputs["artifacts"]) == 17

    ledger = read_lines("sources.jsonl")
    gathered = [s for s in ledger if s["counted"]]
    min_by_type = {"AF-RES-195": 6, "AF-RES-196": 6, "cited_origin": 4, "standards_and_statistics": 4}
    counted = Counter(s["category"] for s in gathered)
    assert all(counted[key] >= needed for key, needed in min_by_type.items())
    assert len({s["work_id"] for s in gathered}) == len(gathered) == 30
    assert len({s["source_id"] for s in ledger}) == len(ledger) == 39
    assert len({s["lineage_id"] for s in gathered}) == 14
    assert all(s["access_status"] == "direct_open" for s in gathered)
    rail_source = next(s for s in gathered if s["source_id"] == "E06")
    assert digest((DATA / rail_source["local_snapshot"]).read_bytes()) == rail_source["local_snapshot_sha256"]

    gold = read_json("gold.json")
    source = inputs["artifacts"]["D03"]
    rows = list(csv.DictReader(io.StringIO(git_show(source["commit"] + ":" + source["path"]).decode())))
    identity = lambda r: "/".join((r["slot_id"], r["subject_id"], r["unit_id"], "FLORES-" + r["flores_id"]))
    for target in gold["main"]:
        if target["rows"]:
            match = [r for r in rows if identity(r) in set(target["rows"])]
            assert [identity(r) for r in match] == target["rows"]
            assert sum(int(r["event_time_ms"]) for r in match) == target["value"]
            assert sum(int(r["src_words"]) for r in match) == target["denominator"]["source_words"]
            assert len(match) == target["denominator"]["segments"]
        else:
            match = [r for r in rows if r["slot_id"] in target["support_assignment_keys"]]
            assert len(match) in (15, 9)
            assert all(not r["reviewer_time_ms"] and r["independent_qa_status"] == "no_public_independent_key" for r in match)
    assert [r["case_id"] for r in read_csv("frame.csv") if r["eligibility"] == "eligible"] == ["S1","S2","M1","M2","W1","W2"]

    core, controls = (read_lines(f"receipts/{phase}.jsonl") for phase in ("core", "controls"))
    assert (len(core), len(controls)) == (12, 8)
    for group, name in ((core, "core"), (controls, "controls")):
        output = (DATA / f"receipts/{name}.stdout.jsonl").read_bytes().splitlines(keepends=True)
        assert len(output) == len(group)
        for row, raw in zip(group, output):
            assert row["worker_exit"] == 0 and digest(raw) == row["stdout_sha256"] and json.loads(raw) == row["result"]
            assert set(row["stage_entries"]) == FILES | {"audit.py"}
            view = row["result"]
            assert set(view["preopened"]) == FILES
            assert {seen["path"] for seen in view["reads"]} <= FILES
            assert set(view["io_guard"].values()) == {"EPERM"}
    pair = {r["scheme"]: r["result"]["observation"] for r in controls if r["case_id"] == "C1"}
    authority = next(r for r in gold["main"] if r["case_id"] == "M1")
    assert pair["A"]["value"] == pair["B"]["value"] == authority["value"]
    assert pair["A"]["denominator"] == authority["denominator"] and pair["A"]["rows"] != authority["rows"]
    assert pair["A"]["status"] == "confirmed" and pair["B"]["reasons"] == ["source_cohort_mismatch"]

    matrix = read_csv("matrix.csv")
    assert len(matrix) == 16
    assert Counter((r["phase"], r["expression"]) for r in matrix) == {("core","A"):6,("core","B"):6,("controls","A/B"):4}
    core_matrix = [r for r in matrix if r["phase"] == "core"]
    for scheme in ("A", "B"):
        assert Counter(r[scheme.lower()+"_outcome"] for r in core_matrix if r["expression"] == scheme) == {"정답":4,"합리적 보류":2}
    ctl_matrix = [r for r in matrix if r["phase"] == "controls"]
    assert [r["case_id"] for r in ctl_matrix if r["a_outcome"] == "오승인"] == ["C1","C4"]
    assert all(r["b_outcome"] == "합리적 보류" for r in ctl_matrix)

    costs = read_csv("costs.csv")
    assert sum(int(r["additional_bytes"]) for r in costs) == 2335
    for row in costs:
        assert int(row["b_bytes"]) - int(row["a_bytes"]) == int(row["additional_bytes"])
        assert sum(int(v) for k,v in row.items() if k.endswith("_delta")) == int(row["additional_bytes"])
    sections = (DATA / "RESULT.md").read_text().strip().split("\n\n")
    tables = [section for section in sections if section.startswith("| ")]
    assert sections[1:4] == tables[:3] and sections[-1] == tables[-1] and len(tables) == 4
    assert [len(table.splitlines())-2 for table in tables] == [6, 10, 4, 3]
    print(f"{len(inputs['artifacts'])} pinned artifacts, {len(gathered)} unique sources, 6 frozen statements")
    print(f"{len(matrix)} matrix rows, {len(core)+len(controls)} guarded outputs, zero observed failures")
    print("C1 preserved values and denominators with a changed row set. The B receipt withheld.")
    print("Unit, missingness, duplicate controls and 2335 additional bytes reconciled.")
    print("Report tables are contiguous. The final table contains three weaknesses.")


if __name__ == "__main__":
    main()
