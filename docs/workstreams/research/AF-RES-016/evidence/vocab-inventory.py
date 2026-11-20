"""Read only the seven AF-RES-016 fixed inputs; write only the owned evidence file."""
import collections
import csv
import io
import json
import pathlib
import subprocess
from datetime import datetime, timezone

BASE = pathlib.Path(__file__).resolve().parent
REPO = BASE.parents[4]
SHAS = {
    "001": "4d6208c08f6f2657865ba000d6768f6537e832b6",
    "002": "62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1",
    "003": "b13db3931b4021ff9e1ac6e404590c09526c3087",
    "004": "2b798c7d2b7355b649691c18de196104ceabb0f0",
    "010": "0603f0d2990c7a501dbdfc45fbbba79155f505fc",
    "011": "478c301b693896e2c6d777f46ac441f071bfdfe8",
    "012": "cb602858378db90adb1f085953016267f9afbd6d",
}


def read(task, file):
    return subprocess.check_output(
        ["git", "show", f"{SHAS[task]}:docs/workstreams/research/AF-RES-{task}/{file}"],
        cwd=REPO, text=True,
    )


def values(rows, key):
    return dict(sorted(collections.Counter(str(row.get(key)) for row in rows).items()))


result = {"study_id": "AF-RES-016", "purpose": "Q8 fixed-vocabulary inventory, not recoding",
          "input_shas": SHAS, "level": "D3-run", "counts": {}}
input_cases = json.loads(read("001", "CASES.json"))["cases"]
proposals = [p for c in input_cases for p in c["formulations"]["C_ai_decomposition_proposal"]["proposals"]]
readback = [p for c in input_cases for p in c["formulations"]["C_ai_decomposition_proposal"]["input_read_back"]]
result["counts"]["001"] = {"cases": len(input_cases), "proposals": len(proposals),
    "proposal_status": values(proposals, "status"), "user_confirmed": values(proposals, "user_confirmed"),
    "reading_status": values(readback, "reading_status")}
expected = json.loads(read("004", "EXPECTED.json"))["rows"]
result["counts"]["004"] = {"rows": len(expected), **{k: values(expected, k) for k in ["label", "role", "L", "E", "T", "H_assessment_scope"]},
    "H": values([h for row in expected for h in row["H"]], "status")}
judgments = []
for file in ["evidence/p1-judgments.json", "evidence/p2-judgments.json"]:
    for row in json.loads(read("010", file))["judgments"]:
        judgments.append({"file": file, **{k: row[k] for k in ["candidate_id", "T", "label", "bucket"]}})
result["counts"]["010"] = {"rows": len(judgments), **{k: values(judgments, k) for k in ["T", "label", "bucket"]}}
result["010_rows"] = judgments
cases = json.loads(read("011", "CASES.json"))["cases"]
answers = [a for c in cases for a in c["answers"]]
result["counts"]["011"] = {"threads": len(cases), "answer_units": len(answers), "role": values(answers, "role"),
    "asker_response": values([a["outcome"] for a in answers], "asker_response"),
    "accepted": values([a["outcome"] for a in answers], "accepted")}
result["counts"]["012"] = {"corpus_role": values([json.loads(l) for l in read("012", "corpus/entries.jsonl").splitlines()], "role")}
result["012_counterexamples"] = []
for file in ["qrels/qrels.tsv", "qrels/independent.tsv"]:
    rows = list(csv.DictReader(io.StringIO(read("012", file)), delimiter="\t"))
    result["counts"]["012"][file] = {"explicit_rows": len(rows), "grade": values(rows, "grade")}
    for row in rows:
        if (row["entry_id"] == "paperless-ngx" and row["query_id"].startswith("K02")) or (row["entry_id"] == "ct-merkle" and row["query_id"].startswith("P04")) or row["entry_id"] == "jiandu":
            result["012_counterexamples"].append({"file": file, **row})
assert result["counts"]["004"]["rows"] == 18
assert result["counts"]["010"]["rows"] == 25
assert result["counts"]["012"]["qrels/qrels.tsv"]["explicit_rows"] == 235
assert result["counts"]["012"]["qrels/independent.tsv"]["explicit_rows"] == 277
out = BASE / "vocab-inventory.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"output": str(out.relative_to(REPO)), "counts": result["counts"]}, ensure_ascii=False, indent=2))
