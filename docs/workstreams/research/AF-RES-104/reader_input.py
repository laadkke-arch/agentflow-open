"""Project sealed packets into opaque reader views or validate first-judgment evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from select_passages import ROOT, jsonl, make_segment, originals, read_jsonl, source_data

MARKER = "\n⟦표시 구간⟧\n"


def load(cache, packets_path, protocol):
    inventory, _ = originals(cache, protocol)
    bodies = {}
    packets = read_jsonl(packets_path.read_bytes())
    for packet in packets:
        for slot in packet["slots"]:
            source = slot["file_id"]
            if source in bodies or source is None:
                continue
            bodies[source] = source_data(cache, inventory[source])
    return packets, bodies


def shown_lines(text, bounds):
    start, end = bounds
    line = text.count("\n", 0, start) + 1
    out = []
    for value in text[start:end].splitlines(keepends=True):
        out.append(f"{line:>5} {value.rstrip(chr(13) + chr(10))}")
        line += value.count("\n")
    return "\n".join(out)


def project(case, packets, bodies):
    """Print shared snippets once per question. Each opaque route keeps its own slots."""
    print(case["title"], case["revision_url"], *case["question_context"], sep="\n")
    for condition in case["conditions"]:
        print(condition["id"], condition["requirement"])
    print("주 해석", case["primary_interpretation"])
    chunks = {}
    for packet in sorted(packets, key=lambda item: item["packet_id"]):
        print(f"\n## {packet['packet_id']}")
        for slot in packet["slots"]:
            source = slot["file_id"]
            if source is None:
                print(f"  {slot['slot']} 공석")
                continue
            labels = []
            for j, segment in enumerate(slot["segments"], 1):
                key = (source, *segment["unicode"])
                if key not in chunks:
                    chunks[key] = str(len(chunks) + 1)
                labels.append(f"{j}={chunks[key]}")
            print(f"  {slot['slot']} {slot['url']} {','.join(labels)}")
    for (source, start, end), label in chunks.items():
        print(f"{MARKER}구간 {label} {source} [{start},{end})")
        print(shown_lines(bodies[source][1], (start, end)))


def visible_citation(slot, segment_number, lo_line, hi_line, bodies):
    if not 1 <= segment_number <= len(slot["segments"]):
        raise ValueError("citation segment absent")
    segment = slot["segments"][segment_number - 1]
    lo, hi = segment["unicode"]
    visible_lo_line, visible_hi_line = segment["lines_lf"]
    if not visible_lo_line <= lo_line <= hi_line <= visible_hi_line:
        raise ValueError(f"citation LF lines outside shown segment: {[lo_line, hi_line]} vs {segment['lines_lf']}")
    raw, text = bodies[slot["file_id"]]
    line = visible_lo_line
    start, end = lo, hi
    for index in range(lo, hi):
        if line < lo_line:
            start = index + 1
        if text[index] == "\n":
            if line == hi_line:
                end = index + 1
                break
            line += 1
    if not lo <= start < end <= hi:
        raise ValueError("empty or out-of-window citation")
    checked = make_segment(raw, text, start, end)
    return {**checked, "slot": slot["slot"], "segment": segment_number,
            "file_id": slot["file_id"], "url": slot["url"]}


def parse_first(notes, packet_map, cases, bodies):
    rows = []
    covered = set()
    for line in notes.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        packet_id, condition_id, status, locations, reason = line.split("|", 4)
        packet = packet_map[packet_id]
        preconditions = {item["id"]: item["requirement"] for item in cases[packet["case_id"]]["conditions"]}
        key = packet_id, condition_id
        if key in covered or condition_id not in preconditions:
            raise ValueError(f"invalid or repeated judgment {key}")
        covered.add(key)
        citations = []
        for location in locations.split(",") if locations else []:
            slot_number, segment_number, lo_line, hi_line = map(int, location.split("."))
            if not 1 <= slot_number <= len(packet["slots"]):
                raise ValueError("no such slot")
            citations.append(visible_citation(packet["slots"][slot_number - 1],
                                               segment_number, lo_line, hi_line, bodies))
        if status not in {"supported", "partial", "refuted", "unknown"}:
            raise ValueError(f"invalid status {status}")
        if status != "unknown" and not citations:
            raise ValueError(f"status {status} needs a visible citation {key}")
        rows.append({"phase": "initial_opaque_self_read", "packet_id": packet_id,
                     "condition_id": condition_id, "status": status, "reason": reason,
                     "citations": citations})
    expected = {(pid, item["id"]) for pid, packet in packet_map.items()
                for item in cases[packet["case_id"]]["conditions"]}
    if covered != expected:
        raise ValueError(f"missing judgments {sorted(expected - covered)}")
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--packets", type=Path, default=ROOT / "packets.jsonl")
    command = parser.add_mutually_exclusive_group(required=True)
    command.add_argument("--case", choices=["J1", "J2", "J3", "J4", "P1", "P2", "P3", "P4"])
    command.add_argument("--validate-first", type=Path)
    command.add_argument("--marker-cost", action="store_true")
    args = parser.parse_args()
    protocol = json.loads((ROOT / "protocol.json").read_bytes())
    cases = {c["case_id"]: c for c in protocol["cases"]}
    packets, bodies = load(args.cache, args.packets, protocol)
    if args.case:
        project(cases[args.case], [packet for packet in packets if packet["case_id"] == args.case], bodies)
    elif args.validate_first:
        rows = parse_first(args.validate_first, {p["packet_id"]: p for p in packets}, cases, bodies)
        import sys
        sys.stdout.buffer.write(jsonl(rows))
    else:
        overhead = {w: {"markers": sum(p["metrics"]["segment_boundary_markers"] for p in packets if p["window"] == w)}
                    for w in ("W1", "W2")}
        for counts in overhead.values():
            counts.update(chars=counts["markers"] * len(MARKER), utf8_bytes=counts["markers"] * len(MARKER.encode()))
        print(json.dumps(overhead, sort_keys=True))


if __name__ == "__main__":
    main()
