"""Read-only field audit of the pinned CodeMend public package.

Does not run CodeMend, unpickle models, or reproduce the human experiment.
No original participant records or code/text payloads are written to disk.
Use the bundled runtime Python (includes xlrd). Output is structural metadata.
"""
import collections
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import urllib.request

import xlrd

SHA = "445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d"
BASE = "https://raw.githubusercontent.com/ronxin/codemend/" + SHA + "/"
receipts = []


def fetch(url):
    start = datetime.now(timezone.utc).isoformat()
    data = urllib.request.urlopen(url, timeout=30).read()
    receipts.append({"url": url, "started_utc": start,
                     "checked_utc": datetime.now(timezone.utc).isoformat(),
                     "bytes": len(data),
                     "sha256": hashlib.sha256(data).hexdigest()})
    return data


# A public GitHub API tree was saved via the existing connector after the
# unauthenticated replay request returned HTTP 403. No credentials are in it.
tree = json.loads(Path(__file__).with_name("codemend-tree.json").read_text())
assert tree["sha"] == SHA and tree["truncated"] is False
paths = {r["path"] for r in tree["tree"]}
csv_data = fetch(BASE + "codemend/models/eval-gt-2.csv")
reader = csv.DictReader(io.StringIO(csv_data.decode("utf-8")))
records = []
line_ends = []
for record in reader:
    records.append(record)
    line_ends.append(reader.line_num)

key_checks = []
for keys in [("case_study_no",), ("query_source",),
             ("case_study_no", "query_source"),
             ("case_study_no", "query"), tuple(reader.fieldnames)]:
    groups = collections.defaultdict(list)
    for rownum, record in enumerate(records, 2):
        groups[tuple(record[k] for k in keys)].append(rownum)
    key_checks.append({
        "candidate_key": list(keys), "input_rows": len(records),
        "unique_keys": len(groups),
        "duplicate_key_groups": sum(len(v) > 1 for v in groups.values()),
        "excess_rows": sum(len(v) - 1 for v in groups.values()),
        "null_key_rows": sum(any(not r[k].strip() for k in keys) for r in records),
        "duplicate_row_locations": [v for v in groups.values() if len(v) > 1]
        if keys == tuple(reader.fieldnames) else None,
    })

xls = []
for path in ["codemend/models/func_gt_pivot.xls",
             "codemend/models/funcarg_gt_pivot.xls"]:
    book = xlrd.open_workbook(file_contents=fetch(BASE + path), on_demand=True)
    sheets = []
    for sheet in book.sheets():
        header_cells = [sheet.cell_value(i, j)
                        for i in range(min(3, sheet.nrows))
                        for j in range(sheet.ncols)]
        sheets.append({"sheet": sheet.name, "rows": sheet.nrows,
                       "columns": sheet.ncols,
                       "recognized_header_labels": sorted({
                           s for s in header_cells
                           if isinstance(s, str) and
                           s in {"rank", "prank", "baseline", "query", "func"}}),
                       "unit": "query-by-model IR ranking, not participant trials"})
    xls.append({"path": path, "sheets": sheets})

db = sqlite3.connect(":memory:")
db.deserialize(fetch(BASE + "codemend/demo/data/code.sqlite3"))
db.execute("PRAGMA query_only=ON")
schema = [{"name": row[0], "type": row[1], "sql": row[2]}
          for row in db.execute("SELECT name,type,sql FROM sqlite_master")]
db.close()

requested_paths = [
    "codemend/demo/log-mode.txt",
    "codemend/demo/code-samples/user-study/practice.py",
    "codemend/demo/code-samples/user-study/task1.py",
    "codemend/demo/code-samples/user-study/task2.py",
    "codemend/demo/code-samples/before_afters/before1.py",
    "codemend/models/output/eval-log-0413.csv",
]
result = {
    "kind": "public_package_field_audit_not_human_effect_reanalysis",
    "study_id": "S04", "source_id": "BC-05", "commit": SHA,
    "tree_entries": len(tree["tree"]), "tree_truncated": tree["truncated"],
    "referenced_file_presence": {p: p in paths for p in requested_paths},
    "query_ledger": {"path": "codemend/models/eval-gt-2.csv",
                     "header": reader.fieldnames, "rows": len(records),
                     "physical_data_lines": [2, line_ends[-1]],
                     "case_counts": dict(collections.Counter(
                         r["case_study_no"] for r in records)),
                     "candidate_key_checks": key_checks,
                     "absent_human_fields": ["participant", "condition", "period",
                                             "start", "end", "elapsed", "score",
                                             "completion"]},
    "spreadsheets": xls, "database_schema": schema,
    "human_join": {"execution": "not_executed_missing_lab_ledger",
                   "left_rows": None, "right_rows": None, "joined_rows": None,
                   "unmatched_rows": None,
                   "reason": "The inspected 361 records are IR queries, not lab trials."},
    "receipts": receipts,
}
output = Path(__file__).with_name("artifact-inspection.json")
output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"output": str(output), "query_rows": len(records),
                  "full_row_unique": key_checks[-1]["unique_keys"],
                  "human_join": result["human_join"]["execution"]}))
