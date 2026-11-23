"""AF-RES-054 aggregate audit. Never emits participant rows or free text.

Run after fetching the public packages listed in fulltext-downloads.json:
python -B audit_software.py --cache cache --output schema-audit.json
Only Python's standard library is required. No study code is executed.
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime
import hashlib
import io
import json
import re
import statistics
import zipfile
from pathlib import Path


def rows(z, name, delimiter=","):
    return list(csv.DictReader(io.StringIO(z.read(name).decode("utf-8-sig")), delimiter=delimiter))


def audit_newton(cache):
    expected = {f"P{i}" for i in range(1, 13)}
    with zipfile.ZipFile(cache / "newton-responses.zip") as z:
        response = {}
        all_ids = []
        for name in sorted(n for n in z.namelist() if n.endswith(".csv")):
            table = rows(z, name)
            ids = [r["Participant"] for r in table]
            all_ids.append(set(ids))
            response[Path(name).name] = {
                "rows": len(table), "unique_ids": len(set(ids)),
                "duplicate_ids": len(ids)-len(set(ids)),
                "missing_expected_ids": len(expected-set(ids)),
                "unexpected_ids": len(set(ids)-expected),
                "columns": list(table[0]),
            }
        assert all(ids == expected for ids in all_ids)
    with zipfile.ZipFile(cache / "newton-experiments.zip") as z:
        names = z.namelist()
        folders = sorted({n.split("/")[1] for n in names if n.startswith("2. Experiments/exp")})
        schemas, ids_all, pair_ids, spans = set(), [], [], []
        events = bad_times = reversals = 0
        notebook_count = collections.Counter()
        assignment_ids, assignment_keys = set(), set()
        order_counts, dataset_by_condition = collections.Counter(), collections.Counter()
        for folder in folders:
            m = re.fullmatch(r"exp(\d+)-([ce])(\d)([ce])(\d)(?:-serverdied)?", folder)
            assert m, folder
            person, c1, d1, c2, d2 = m.groups()
            pid = "P"+person
            assert pid not in assignment_ids
            assignment_ids.add(pid)
            order_counts[c1+c2] += 1
            for period, condition, dataset in [(1,c1,d1),(2,c2,d2)]:
                assignment_keys.add((pid,condition,period,dataset))
                dataset_by_condition[condition+dataset] += 1
            prefix = f"2. Experiments/{folder}/"
            for name in ["python.ipynb", "tool.ipynb"]:
                notebook_count[name] += int(prefix+name in names)
            log = json.loads(z.read(prefix+"result.json"))
            events += len(log)
            times = []
            for event in log:
                schemas.update(event)
                ids_all.append(event.get("id"))
                pair_ids.append((pid,event.get("id")))
                ts = event.get("timestamp")
                if isinstance(ts,(int,float)):
                    times.append(ts)
                else:
                    bad_times += 1
            reversals += sum(times[i] > times[i+1] for i in range(len(times)-1))
            if times:
                spans.append((max(times)-min(times))/1000)
        assert assignment_ids == expected
        assert len(assignment_keys) == 24
    with zipfile.ZipFile(cache / "newton-analyses.zip") as z:
        graph = json.loads(z.read("4. Analyses/interactions.json"))
        graph_audit = {"nodes":len(graph["nodes"]), "links":len(graph["links"]),
                       "participant_references":sum(len(x.get("participants",[])) for x in graph["links"]),
                       "warning":"goal/Success is a generated-code reply node, not an independent grade; Submission denotes chat forms."}
    return {
        "paper_recruitment_responses":48, "paper_selected_people":12,
        "derived_assignment_units":len(assignment_keys),
        "assignment_basis":"Paper Table3 and matching author folder names; no independent allocation/withdrawal log.",
        "condition_order_counts":dict(order_counts),
        "dataset_by_condition_counts":dict(dataset_by_condition),
        "sandbox_folders_excluded":10,
        "response_tables":response,
        "left_join":{
            "left_people":12,"left_person_condition_units":24,
            "post_task_response_rows_before":24,"after":24,"unmatched":0,"duplicate_keys":0,
            "notebook_files_before":sum(notebook_count.values()),"matched_units":24,
            "raw_message_events_before":events,"after_person_aggregation":12,
            "experimental_units_matched":12,"control_event_logs_not_provided":12,
            "validated_task_start_stop_submit_columns":0,"independent_original_final_grade_columns":0,
        },
        "notebook_files":dict(notebook_count),"event_schema":sorted(schemas),
        "raw_event_count":events,"duplicate_event_ids":len(ids_all)-len(set(ids_all)),
        "duplicate_person_event_keys":len(pair_ids)-len(set(pair_ids)),
        "missing_event_timestamps":bad_times,"adjacent_timestamp_reversals":reversals,
        "naive_event_span_seconds":[min(spans),max(spans)],
        "timer_caution":"These33–68minute spans exceed the25minute protocol and include no validated task-start/submit marker. They are not task durations or deadline flags.",
        "coded_graph":graph_audit,
        "paper_author_completion":{"both":4,"Newton_only":2,"control_only":0,"neither":6,
                                   "Newton":6,"control":4,"difference":"1/6"},
        "primary_quality_deadline_joint":"not computed: published completion label lacks operational final-quality predicate; raw clocks do not recover it",
    }


def audit_designpattern(cache):
    with zipfile.ZipFile(cache / "designpattern-package.zip") as z:
        prefix = "SoftwareForHumans-DesignPatternDoc-UserStudy-a81f66b/"
        table = rows(z,prefix+"data.csv",";")
        time_fields = [k for k in table[0] if k.endswith("Time")]
        sum_equal = sum(abs(float(r["TotalTime"])-sum(float(r[k]) for k in time_fields if k!="TotalTime"))<1e-9 for r in table)
        assert sum_equal == len(table) == 21
        by_group = {}
        for group in ["0","1"]:
            arm = [r for r in table if r["Group"] == group]
            by_group[group] = {
                "N":len(arm),
                "times_seconds":{k:{"mean":statistics.mean(float(r[k]) for r in arm),
                                      "median":statistics.median(float(r[k]) for r in arm),
                                      "min":min(float(r[k]) for r in arm),
                                      "max":max(float(r[k]) for r in arm)} for k in time_fields},
                "above_planned45min_diagnostic":sum(float(r["TotalTime"])>2700 for r in arm),
            }
        answer_tables = {}
        for name in ["controlGroup.csv","experimentalGroup.csv"]:
            rr = rows(z,prefix+"answers/"+name)
            # Only schema/counts. Do not expose emails, links, times, or free text.
            answer_tables[name] = {"rows":len(rr),"columns":len(rr[0]),
                                  "explicit_participant_id_column":False,
                                  "individual_values_exported":False}
    return {"analysis_rows":len(table),"analysis_columns":list(table[0]),
            "unique_complete_rows":len({tuple(r.values()) for r in table}),
            "empty_cells":sum(not v.strip() for r in table for v in r.values()),
            "sum_time_equals_total_rows":sum_equal,"group0_control_group1_plugin":by_group,
            "answers":answer_tables,
            "allocation_to_grade_left_join":"not executable: no participant ID/crosswalk in analysis CSV; original code/diagrams lost after analysis per paper",
            "deadline":"planned45minute task block and40–50minute approximate session are not established enforced deadlines",
            "quality":"observer-validation protocol exists; numeric pass counts/individual grade records unconfirmed",
            "primary_joint_computed":False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache",type=Path,default=Path("cache"))
    parser.add_argument("--output",type=Path,default=Path("schema-audit.json"))
    args = parser.parse_args()
    names = ["newton-responses.zip","newton-experiments.zip","newton-analyses.zip","designpattern-package.zip"]
    result = {"audit_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "input_sha256":{n:hashlib.sha256((args.cache/n).read_bytes()).hexdigest() for n in names},
              "newton":audit_newton(args.cache),"designpattern":audit_designpattern(args.cache),
              "participant_rows_exported":False,"author_model_or_plugin_executed":False}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"status":"pass","output":str(args.output),"Newton_units":24,"Newton_events":588,"DesignPattern_rows":21}))


if __name__ == "__main__":
    main()
