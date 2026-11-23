"""Read-only NCQ public artifact audit; emit aggregates, never original participant IDs/code.

Run from repository root with python -B PATH/audit_ncq.py.
No third-party packages, author program execution, installation, or raw data persistence.
"""
import collections
import csv
import datetime
import hashlib
import io
import json
import urllib.request

BASE = "https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/"


def audit(filename, prefix):
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with urllib.request.urlopen(BASE + filename, timeout=30) as response:
        raw = response.read()
    decoding_note = None
    try:
        decoded = raw.decode("utf-8-sig")
        encoding = "utf-8-sig"
    except UnicodeDecodeError as error:
        decoding_note = str(error)
        decoded = raw.decode("cp1252")
        encoding = "cp1252 (explicit fallback; no bytes dropped)"
    reader = csv.DictReader(io.StringIO(decoded, newline=""))
    rows, locations = [], []
    # Reading fieldnames consumes the physical header line.
    columns = reader.fieldnames
    previous = reader.line_num
    for logical_record, row in enumerate(reader, 1):
        rows.append(row)
        locations.append({"logical_data_record": logical_record,
                          "physical_line_start": previous + 1,
                          "physical_line_end": reader.line_num})
        previous = reader.line_num
    pair_keys = [(row["P"], row["T"]) for row in rows]
    unique_pairs = set(pair_keys)
    examples = []
    example_people = {}
    # Select only first source row in each observed T label. Replace person ID.
    # T is NOT promoted to a named task/condition without the absent mapping file.
    for label in sorted({r["T"] for r in rows}):
        i = next(i for i, r in enumerate(rows) if r["T"] == label)
        if rows[i]["P"] not in example_people:
            example_people[rows[i]["P"]] = prefix + "-example-person-" + str(len(example_people) + 1)
        examples.append({"example_id": prefix + "-trial-label-" + label,
                         "participant_id": example_people[rows[i]["P"]],
                         "source": filename, "location": locations[i],
                         "source_T_label": label,
                         "condition": "미확인 (T-to-condition codebook absent)",
                         "problem_task_id": "미확인 (five-task mapping absent)",
                         "used_flag": rows[i]["Used?"], "runs_flag": rows[i]["Runs?"],
                         "time": "미확인", "final_task_pass": "미확인"})
    flag_table = []
    for label in sorted({r["T"] for r in rows}):
        subset = [r for r in rows if r["T"] == label]
        counts = collections.Counter((r["Used?"], r["Runs?"]) for r in subset)
        flag_table.append({"source_T_label": label, "records": len(subset),
                           "participants": len({r["P"] for r in subset}),
                           "used_runs_counts": [{"Used?": a, "Runs?": b, "n": n}
                                                 for (a, b), n in sorted(counts.items())]})
    return {"source_url": BASE + filename, "version": "ce14f193f7014c120f04619826cb251818d99b0e",
            "checked_utc": started,
            "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "file": filename, "byte_count": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "encoding": encoding, "decoding_note": decoding_note,
            "columns": columns, "data_records": len(rows), "physical_lines": reader.line_num,
            "distinct_participant_labels": len({r["P"] for r in rows}),
            "distinct_P_T": len(unique_pairs),
            "non_unique_P_T_excess_records": len(rows) - len(unique_pairs),
            "distinct_P_T_Package": len({(r["P"], r["T"], r["Package"]) for r in rows}),
            "exact_duplicate_full_records": len(rows) - len({tuple(r[k] for k in columns) for r in rows}),
            "null_join_key_records": sum(not r["P"] or not r["T"] for r in rows),
            "empty_fields": {k: sum(r[k] == "" for r in rows) for k in columns},
            "flag_counts_by_T": flag_table,
            "record_join_key": "(file/study, logical_data_record)",
            "participant_trial_join_key_candidate": "(file/study, P, T); one-to-many to snippets",
            "missing_target_fields": ["condition codebook", "problem task ID", "assignment/period table",
                                      "task start", "package install time", "task finish", "activity intervals",
                                      "final code/score", "withdrawn-participant ledger"],
            "assignment_time_quality_join": "not executed; necessary files/keys not found in inspected artifact",
            "joined_time_quality_rows": "미확인", "target_analyzed_trials": 20,
            "examples": examples,
            "interpretation_boundary": "Snippet rows are not task-success rows; Runs? is not final task pass."
            }


if __name__ == "__main__":
    print(json.dumps({"audit": "NCQ public snippet row/key audit",
                      "kind": "read_only_public_artifact_analysis",
                      "files": [audit("data/user-study/codesnippets1.csv", "NA-C1"),
                                audit("data/user-study/codesnippets2.csv", "NA-C2")],
                      "cross_cohort_rule": "Do not join matching P labels across files; different cohorts.",
                      "raw_participant_rows_saved": False}, ensure_ascii=False, indent=2))
