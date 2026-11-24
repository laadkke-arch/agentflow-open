"""Assemble sealed arm outputs without changing the arms' observed ordering.

Run once after all arms finish. No network calls. Does not adjudicate truth.
"""
from pathlib import Path
import csv
import hashlib
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parent


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def dump_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def flat(value):
    if value is None:
        return ""
    if isinstance(value, (dict, list, bool)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def collect():
    requests = read_jsonl(ROOT / "requests.jsonl")
    events, slots, source_rows, arm_receipts = [], [], [], []
    for request in requests:
        rid = request["id"]
        for arm in ("A", "B"):
            path = ROOT / "evidence" / "search" / f"{rid}-{arm}"
            result = json.loads((path / "returns.json").read_text())
            arm_events = read_jsonl(path / "events.jsonl")
            arm_sources = read_jsonl(path / "sources.jsonl")
            assert result["request_id"] == rid and result["arm"] == arm
            assert result["input_sha256"] == request["experiment_input_sha256"]
            assert result["actual_queries"] <= 3
            assert result["actual_explicit_opens"] <= 6
            finals = result["final_candidates"]
            assert len(finals) <= 3
            assert len({v["rank"] for v in finals}) == len(finals)
            assert all(v["rank"] in (1, 2, 3) for v in finals)
            for event in arm_events:
                event = dict(event)
                event.update(request_id=rid, arm=arm,
                             arm_record=str((path / "events.jsonl").relative_to(ROOT)))
                events.append(event)
            for source in arm_sources:
                source = dict(source)
                source["arm_record"] = str((path / "sources.jsonl").relative_to(ROOT))
                source["request_id"] = rid
                source["arm"] = arm
                source_rows.append(source)
            for rank in (1, 2, 3):
                candidate = next((v for v in finals if v["rank"] == rank), None)
                slot = {
                    "candidate_id": f"{rid}-{arm}-{rank}", "request_id": rid,
                    "arm": arm, "returned_rank": rank,
                    "return_state": "returned" if candidate else "vacant",
                    "url": "", "source_ref": "", "source_id": "", "title": "",
                    "provider": "", "product_feature": "", "version_or_date": "",
                    "exact_section": "", "form": "", "input_processing_observation": "",
                    "what_is_new_vs_baseline": "", "changed_choice": "",
                    "minimal_discriminating_input": "", "expected_output": "",
                    "conditions_supported": "", "limitations": "",
                    "counter_evidence": "", "historical_availability": "",
                    "acquisition_event": "", "vacancy_reason": "",
                    "actual_queries": result["actual_queries"],
                    "actual_explicit_opens": result["actual_explicit_opens"],
                    "start_utc": result["start_utc"], "end_utc": result["end_utc"],
                    "fit_condition_1": "unadjudicated", "fit_condition_2": "unadjudicated",
                    "lineage_id": "", "judgment": "unadjudicated", "novelty_class": "",
                    "judgment_reason": "", "blind_id": "",
                }
                if candidate:
                    for key in slot:
                        if key in candidate:
                            slot[key] = flat(candidate[key])
                else:
                    vacancies = result.get("vacancies", [])
                    slot["vacancy_reason"] = flat(vacancies) or "No final link returned for this rank."
                    slot["judgment"] = "vacant"
                slots.append(slot)
            arm_receipts.append({
                "request_id": rid, "arm": arm,
                "input_sha256": result["input_sha256"],
                "actual_queries": result["actual_queries"],
                "actual_explicit_opens": result["actual_explicit_opens"],
                "final_links": len(finals), "vacancies": 3 - len(finals),
                "start_utc": result["start_utc"], "end_utc": result["end_utc"],
                "output_hashes": {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                                  for f in path.iterdir() if f.is_file()},
            })
    for event in events:
        event["merged_sort_utc"] = (event.get("ended_utc") if event["event_type"] == "stop"
                                    else event.get("started_utc"))
        event["merged_sort_note"] = "wall-clock metadata; concurrent actions are not a proven sequential exposure order"
    events.sort(key=lambda row: (datetime.fromisoformat(row["merged_sort_utc"].replace("Z", "+00:00")),
                                 row["request_id"], row["arm"], row["event_index"]))
    dump_jsonl(ROOT / "search.jsonl", events)
    with (ROOT / "candidates.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(slots[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(slots)
    dump_jsonl(ROOT / "evidence" / "search-sources-unadjudicated.jsonl", source_rows)
    (ROOT / "evidence" / "search-execution-summary.json").write_text(
        json.dumps({"arms": arm_receipts, "planned_slots": 36,
                    "returned_slots": sum(row["return_state"] == "returned" for row in slots),
                    "vacant_slots": sum(row["return_state"] == "vacant" for row in slots)},
                   ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"arms": len(arm_receipts), "planned_slots": len(slots),
                      "events": len(events), "source_open_records": len(source_rows)}))


if __name__ == "__main__":
    collect()
