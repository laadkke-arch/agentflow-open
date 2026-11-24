"""Audit the pinned public Sketchy pilot export. Outputs aggregate JSON or a selection CSV."""

import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

SHA256 = "aec34f174ac350448b62a2223a859303ae496f99ba526775e027e914a4a1afbc"
BLOB = "e2a18ceca7542a754ba2c039ad4c9ed33c921ac5"
BYTES = 15_062_721
COMMIT = "f01bb57fbc7f5f14b6bd057b01221f5c3618f69e"
SOURCE = (
    f"https://raw.githubusercontent.com/brownhci/sketchy-1.0/{COMMIT}"
    "/data/pilot_data/sketchy_dec6_dec13_peeks_updated.csv"
)
KEYS = ("id_peek", "id_user", "id_user_peeked", "id_peeked_sketch", "id_completed_sketch")
FIELDS = (
    "sim_group", "id_peek", "id_user", "exp", "id_user_peeked", "exp_peeked", "vote",
    "id_peeked_sketch", "id_completed_sketch", "timestamp", "empty", "repeat", "similarity",
    "peeked_sketch_strokes", "peeked_sketch_strokes_quickdraw", "peeked_num_strokes",
    "peeked_num_points", "peeked_width", "peeked_height", "complete_sketch_strokes",
    "complete_sketch_strokes_quickdraw", "complete_num_strokes", "complete_num_points",
    "complete_width", "complete_height",
)
SNAPSHOTS = ("peeked_sketch_strokes", "complete_sketch_strokes")


def read_pilot(path):
    with path.open("rb") as stream:
        hasher = sha256()
        for block in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(block)
    if path.stat().st_size != BYTES or hasher.hexdigest() != SHA256:
        raise ValueError("pilot size or checksum differs from the pinned input")

    csv.field_size_limit(16 * 1024 * 1024)
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("unexpected pilot columns")
        rows = list(reader)
    for number, row in enumerate(rows, 1):
        if None in row or None in row.values():
            raise ValueError(f"bad column count at logical record {number}")
        if not all(re.fullmatch(r"[0-9]+", row[key]) for key in KEYS + ("timestamp",)):
            raise ValueError(f"expected opaque numeric keys at logical record {number}")
    return rows


def maps(rows):
    looker = defaultdict(list)
    for number, row in enumerate(rows, 1):
        looker[row["id_user"], row["id_completed_sketch"]].append((number, row))
    return looker


def diagnostic_slots(rows):
    looker = maps(rows)
    for key in sorted(looker)[:4]:
        records = looker[key]
        numbers = [number for number, _ in records]
        earliest = min(records, key=lambda record: int(record[1]["timestamp"]))[0]
        yield {"first_export_record": numbers[0], "export_records": numbers,
               "lowest_numeric_timestamp_record": earliest}


def intersections(left, right):
    return {
        "left_distinct": len(left), "right_distinct": len(right),
        "intersect_distinct": len(left & right),
        "left_only": len(left - right), "right_only": len(right - left),
    }


def profile(rows):
    looker = maps(rows)
    counts = {key: Counter(row[key] for row in rows) for key in KEYS}
    recipient_pairs = Counter((r["id_user"], r["id_user_peeked"]) for r in rows)
    final_refs = set(counts["id_completed_sketch"])
    example_refs = set(counts["id_peeked_sketch"])
    ts = [int(r["timestamp"]) for r in rows]
    calendar = Counter(
        (r["sim_group"], datetime.fromtimestamp(t // 1000, timezone.utc).date().isoformat())
        for r, t in zip(rows, ts, strict=True)
    )
    return {
        "input": {"revision": COMMIT, "sha256": SHA256, "bytes": BYTES, "git_blob": BLOB},
        "record_numbering": "one-based logical CSV records after the header",
        "rows": len(rows), "columns": list(FIELDS),
        "distinct_keys": {k: len(v) for k, v in counts.items()},
        "full_duplicate_rows": len(rows) - len({tuple(r.values()) for r in rows}),
        "duplicate_peek_id_rows": len(rows) - len(counts["id_peek"]),
        "missing_keys": {k: counts[k].get("", 0) for k in KEYS},
        "focal_final": {
            "pair_keys": len(looker),
            "multiple_rows_keys": sum(len(v) > 1 for v in looker.values()),
            "max_rows_per_key": max(map(len, looker.values())),
        },
        "focal_target": {
            "pair_keys": len(recipient_pairs),
            "multiple_rows_keys": sum(v > 1 for v in recipient_pairs.values()),
            "max_rows_per_key": max(recipient_pairs.values()),
            "focal_with_multiple_targets": sum(
                len({r["id_user_peeked"] for _, r in records}) > 1
                for records in looker.values()
            ),
            "target_with_multiple_focals": sum(
                len({left for left, right in recipient_pairs if right == target}) > 1
                for target in counts["id_user_peeked"]
            ),
            "same_focal_as_target_rows": sum(r["id_user"] == r["id_user_peeked"] for r in rows),
        },
        "user_id_intersection_focal_target": intersections(
            set(counts["id_user"]), set(counts["id_user_peeked"])
        ),
        "sketch_id_intersection_final_example": intersections(final_refs, example_refs),
        "timestamp": {
            "digits_histogram": dict(Counter(len(r["timestamp"]) for r in rows)),
            "duplicate_numeric_ticks": len(ts) - len(set(ts)),
            "decreasing_adjacent_in_export_order": sum(a > b for a, b in zip(ts, ts[1:])),
            "hypothetical_unix_ms_utc_date_by_sim_group": {
                f"{group}/{day}": count for (group, day), count in calendar.items()
            },
            "meaning": "opening vs view/review/export clock unresolved; no save timestamps",
        },
        "occupied_snapshot_cells": {k: sum(bool(r[k].strip()) for r in rows) for k in SNAPSHOTS},
        "eligible_task_slots": 0,
        "strict_pairs": 0,
        "strict_missing": "no verified task or pre/open/post event chain in this export",
        "diagnostic_slots": list(diagnostic_slots(rows)),
    }


def write_selection(rows):
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["study", "layer", "planned_slot", "selection_status",
                     "first_record", "export_records", "lowest_timestamp_record", "reason"])
    missing = [
        ("A03", "core", "본 실험 ZIP과 익명 과제·저장 사건 미확인"),
        ("B07", "core", "ZIP·작품 및 개봉 키 미확인"),
        ("X11", "supplement", "OSF 파일 및 Jamboard·개봉 조인 미확인"),
        ("B04", "extension", "익명 패킷·개봉·작품 키 미확인"),
        ("B06", "extension", "익명 봉투·개봉·작품 키 미확인"),
        ("B09", "extension", "익명 중간-최종·개봉 키 미확인"),
    ]
    for study, layer, reason in missing:
        for slot in range(1, 5):
            writer.writerow([study, layer, slot, "미확인", "미확인", "미확인", "미확인", reason])
    for slot, evidence in enumerate(diagnostic_slots(rows), 1):
        writer.writerow(["A03", "pilot-diagnostic", slot, "진단만", evidence["first_export_record"],
                         "|".join(map(str, evidence["export_records"])),
                         evidence["lowest_numeric_timestamp_record"],
                         "참가자×최종 참조의 첫 4개, 과제키·직전판·개봉 및 첫 저장 시계 미확인"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--selection", action="store_true")
    args = parser.parse_args()
    rows = read_pilot(args.file)
    if args.selection:
        write_selection(rows)
    else:
        json.dump(profile(rows), sys.stdout, sort_keys=True, ensure_ascii=False, indent=2)
        print()


if __name__ == "__main__":
    main()
