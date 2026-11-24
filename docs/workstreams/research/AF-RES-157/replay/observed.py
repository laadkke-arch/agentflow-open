"""Compare decoded snapshot structure and produce the published opaque pilot-event ledger."""

import argparse
import csv
from collections import Counter, defaultdict
import json
from pathlib import Path
import sys

from pilot import SNAPSHOTS, diagnostic_slots, maps, read_pilot


def ref_profile(rows, ref, actor, field):
    authors = defaultdict(set)
    snapshots = defaultdict(set)
    for row in rows:
        authors[row[ref]].add(row[actor])
        snapshots[row[ref]].add(row[field])
    return {
        "refs": len(snapshots),
        "refs_with_multiple_actor_labels": sum(len(items) > 1 for items in authors.values()),
        "refs_with_multiple_byte_payloads": sum(len(items) > 1 for items in snapshots.values()),
        "distinct_byte_payloads": len(set().union(*snapshots.values())),
    }


def inspect_snapshots(rows):
    decoded = [[json.loads(row[field]) for field in SNAPSHOTS] for row in rows]
    export_duplicates = sum(len(records) - 1 for records in maps(rows).values())
    equal_by_group = defaultdict(lambda: {"equal": 0, "rows": 0})
    for row, (example, final) in zip(rows, decoded, strict=True):
        group = equal_by_group[row["sim_group"]]
        group["rows"] += 1
        group["equal"] += example == final
    return {
        "record_numbering": "one-based logical CSV records after the header",
        "source_snapshot_counts": [len(rows), len(rows)],
        "arrays_parsed": [sum(isinstance(v, list) for v, _ in decoded),
                          sum(isinstance(v, list) for _, v in decoded)],
        "empty_arrays": [sum(not v for v, _ in decoded), sum(not v for _, v in decoded)],
        "rowwise_equal_arrays_cross_roles": sum(a == b for a, b in decoded),
        "rowwise_equal_by_sim_group_label": dict(equal_by_group),
        "final_ref": ref_profile(rows, "id_completed_sketch", "id_user", SNAPSHOTS[1]),
        "example_ref": ref_profile(rows, "id_peeked_sketch", "id_user_peeked", SNAPSHOTS[0]),
        "repeated_csv_rows_per_final_ref_beyond_first": export_duplicates,
        "label_counts": dict(Counter(row["vote"] for row in rows)),
        "verified_repeat_saves": None,
        "strict_pairs": 0,
        "selected_payloads": [
            {
                "slot": index,
                "record": number,
                "example_strokes": len(decoded[number - 1][0]),
                "final_strokes": len(decoded[number - 1][1]),
                "equal": decoded[number - 1][0] == decoded[number - 1][1],
            }
            for index, slot in enumerate(diagnostic_slots(rows), 1)
            for number in [slot["lowest_numeric_timestamp_record"]]
        ],
    }


def write_events(rows):
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["event_id", "study", "layer", "record", "roles_in_record",
                     "links_in_record", "task_key", "clock_order", "source_ids", "strict"])
    for number, _ in enumerate(rows, 1):
        writer.writerow([
            f"A03-PIL-{number:03d}", "A03", "pilot-proxy", number,
            "예시 참조와 완료 참조, 검증된 개봉·저장 사건 0",
            "id_user/id_peek/id_user_peeked/id_peeked_sketch/id_completed_sketch 열",
            "미확인: room/task 열 없음",
            "정수 timestamp 한 개; 개봉/투표 원점 및 전후 순서 미확인",
            "S03;S43", 0,
        ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--events", action="store_true")
    args = parser.parse_args()
    rows = read_pilot(args.file)
    if args.events:
        write_events(rows)
    else:
        json.dump(inspect_snapshots(rows), sys.stdout, sort_keys=True, ensure_ascii=False, indent=2)
        print()


if __name__ == "__main__":
    main()
