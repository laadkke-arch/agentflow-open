#!/usr/bin/env python3
"""Verify recorded receipts and project pointer IDs onto stable score positions."""
import argparse
from collections import Counter
import csv
import hashlib
import itertools
import json
from pathlib import Path
import xml.etree.ElementTree as ET

PACKET = Path(__file__).resolve().parent.parent
REGULAR_STAGES = ["start", "immediate", "after_command", "before_save", "reopened"]
EDIT_STAGES = ["p2_edit", "p1_edit", "undo_p1"]
OBJECT_LOCATIONS = {
    "M1": ("master", 0), "M1F": ("master", 0), "M2": ("master", 4),
    "P1": ("Flute", 0), "P1F": ("Flute", 0), "P2": ("Oboe", 0),
    "C1": ("master", 1), "C1F": ("master", 1),
}
OBSERVATION_FIELDS = (
    "present", "flag", "mark", "tick", "track", "voice", "measure_ordinal",
    "note_ordinal", "type", "visible", "printing", "drop_target", "color",
    "cur_color", "selection_color", "offset_sp",
)


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def verified_file(root, proof):
    path = root / proof["path"]
    data = path.read_bytes()
    if len(data) != proof["bytes"] or hashlib.sha256(data).hexdigest() != proof["sha256"]:
        raise ValueError(f"receipt bytes changed: {path}")
    return path


def pointer_label(entry, ids, owners):
    label = ids[entry["id"]]
    role, _ = OBJECT_LOCATIONS[label]
    if owners[entry["score_id"]] != role:
        raise ValueError(f"pointer belongs to a different score: {label}")
    return label


def project_state(record):
    """Recompute membership and link peer labels without using flag as a proxy."""
    objects = record["objects"]
    scores = record["scores"]
    ids = {row["id"]: name for name, row in objects.items() if row["present"]}
    owners = {row["score_id"]: role for role, row in scores.items() if row["present"]}
    if len(ids) != sum(row["present"] for row in objects.values()):
        raise ValueError("two score positions refer to the same probe object")

    projected_scores = {}
    for role, row in scores.items():
        if not row["present"]:
            projected_scores[role] = None
            continue
        selection = {}
        for entry in row["selection"]:
            label = pointer_label(entry, ids, owners)
            if owners[entry["score_id"]] != role or entry["track"] != objects[label]["track"]:
                raise ValueError(f"selection contains an object outside {role}")
            if label in selection or entry["flag"] != objects[label]["flag"]:
                raise ValueError(f"invalid selection entry for {label}")
            selection[label] = entry["flag"]
        projected_scores[role] = {
            "state": row["selection_state"], "staves": row["staves"], "selection": selection,
        }

    projected = {}
    for label, row in objects.items():
        if not row["present"]:
            projected[label] = None
            continue
        role, track = OBJECT_LOCATIONS[label]
        if owners[row["score_id"]] != role or row["track"] != track:
            raise ValueError(f"location drift for {label}")
        if (row["tick"], row["measure_ordinal"], row["note_ordinal"]) != (0, 0, 0):
            raise ValueError(f"wrong note location for {label}")
        member = label in projected_scores[role]["selection"]
        if member != row["member"]:
            raise ValueError(f"membership and pointer ledger disagree for {label}")
        peers = sorted(pointer_label(peer, ids, owners) for peer in row["link_members"])
        item = {field: row[field] for field in OBSERVATION_FIELDS}
        item.update(member=member, peers=peers)
        if row["type"] == "Note":
            item.update(pitch=row["pitch"], tpc=row["tpc"])
        else:
            item["text"] = row["text"]
        projected[label] = item
    for label, item in projected.items():
        if item and item["peers"]:
            if label not in item["peers"] or len(set(item["peers"])) != len(item["peers"]):
                raise ValueError(f"invalid link group for {label}")
            if any(projected[peer]["peers"] != item["peers"] for peer in item["peers"]):
                raise ValueError(f"asymmetric link group for {label}")
    return {
        "stage": record["stage"], "objects": projected, "scores": projected_scores,
        "undo_available": record["undo_available"], "undo_index": record["undo_index"],
    }


def xml_notes(path):
    """Read the saved artifact independently of the native reopen."""
    root = ET.parse(path).getroot()
    if root.tag != "museScore" or root.attrib["version"] != "3.01":
        raise ValueError(f"unexpected score format: {path}")
    master = root.find("Score")
    if master is None:
        raise ValueError("master Score is missing")
    documents = {"master": master}
    for part in master.findall("Score"):
        documents[part.findtext("name")] = part
    notes = {}
    for label, (role, track) in OBJECT_LOCATIONS.items():
        if label.endswith("F") or role not in documents:
            continue
        staff, voice = divmod(track, 4)
        measure = documents[role].find(f"./Staff[@id='{staff + 1}']/Measure")
        voices = measure.findall("voice")
        if voice >= len(voices):
            continue
        note = voices[voice].find("Chord/Note")
        if note is not None:
            notes[label] = {
                "pitch": int(note.findtext("pitch")),
                "has_link_marker": note.find("linkedMain") is not None or note.find("linked") is not None,
            }
    return {
        "notes": notes,
        "selected_or_mark_tags": sum(node.tag in {"selected", "mark"} for node in root.iter()),
    }


def validate_score_roundtrip(saved, reopened):
    present = {label: note for label, note in reopened["objects"].items()
               if note and note["type"] == "Note"}
    if set(saved["notes"]) != set(present):
        raise ValueError("saved and reopened scores have different note positions")
    for label, note in present.items():
        if saved["notes"][label] != {"pitch": note["pitch"], "has_link_marker": bool(note["peers"])}:
            raise ValueError(f"saved pitch or link marker differed from reopened {label}")


def expected_immediate(case, build):
    # Direct projection of cases.csv. The observer emits no predicted values.
    if case == "E03":
        return "P1F", (build == "U", False, None)
    if case == "E05":
        return "C1", (build in {"U", "L"}, False, False)
    return "P1", (case in {"E01", "E04"} and build == "U", False, case == "E06")


def assess_expectation(row, stages, reopened, saved):
    case = row["case_id"]
    label, expected = expected_immediate(case, row["build"])
    immediate = stages["immediate"]["objects"][label]
    comparisons = {
        "immediate_flag_member_mark": tuple(immediate[k] for k in ("flag", "member", "mark")) == expected,
        "immediate_selection_color": (immediate["cur_color"] == immediate["selection_color"]) == bool(expected[0] or expected[2]),
        "all_reopened_selection_empty": all(not score["selection"] for score in reopened["scores"].values() if score),
        "all_reopened_flags_and_marks_clear": all(not obj["flag"] and not obj["mark"] for obj in reopened["objects"].values() if obj),
        "file_has_no_selected_or_mark_tags": saved["selected_or_mark_tags"] == 0,
        "fresh_reopen_undo_empty": not reopened["undo_available"],
    }
    for phase, state in stages.items():
        objects = state["objects"]
        p1_present = case != "E05" and phase != "start"
        copied_present = case == "E05" and phase != "start"
        pitch1 = 62 if phase == "p1_edit" else 60
        pitch2 = 69 if case == "E04" and phase in {"p2_edit", "p1_edit", "undo_p1", "before_save", "reopened"} else 67
        for label2, pitch, peers, offset in (
            ("M1", pitch1, ["M1", "P1"] if p1_present else [], [0, 0]),
            ("M2", pitch2, ["M2", "P2"], [0.75, 0]),
            ("P2", pitch2, ["M2", "P2"], [0.75, 0]),
            ("P1", pitch1, ["M1", "P1"], [0, 0]),
            ("C1", pitch1, [], [0, 0]),
        ):
            obj = objects[label2]
            required = label2 in {"M1", "M2", "P2"} or (label2 == "P1" and p1_present) or (label2 == "C1" and copied_present)
            if required:
                tpc = {60: 14, 62: 16, 67: 15, 69: 17}[pitch]
                actual = (obj["pitch"], obj["tpc"], obj["peers"], obj["offset_sp"]) if obj else None
                comparisons[f"{phase}:{label2}:music"] = actual == (pitch, [tpc, tpc], peers, offset)
            else:
                comparisons[f"{phase}:{label2}:absent"] = obj is None
        if case == "E03" and phase != "start":
            comparisons[f"{phase}:fingering"] = objects["P1F"]["peers"] == ["M1F", "P1F"] and objects["P1F"]["text"] == "1"
    return [name for name, matched in comparisons.items() if not matched]


def examine_run(root, row, fixture_digest):
    artifacts = {name: verified_file(root, proof) for name, proof in row["artifacts"].items()}
    if row["input_sha256"] != fixture_digest:
        raise ValueError("receipt used a different fixture")
    if row["status"] != "completed":
        return {"state": row["status"], "reason": row.get("reason", "nonzero exit")}
    if row["exit_code"] != 0 or not row.get("empty_at_start"):
        raise ValueError("inconsistent completion receipt")
    try:
        records = read_jsonl(artifacts["stdout.jsonl"])
        saved = xml_notes(artifacts["roundtrip.mscx"])
        projected = [project_state(record) for record in records]
        expected_stages = REGULAR_STAGES
        if row["case_id"] == "E04":
            expected_stages = REGULAR_STAGES[:3] + EDIT_STAGES + REGULAR_STAGES[3:]
        if [record["stage"] for record in projected] != expected_stages:
            return {"state": "unreadable", "reason": "missing, additional, or reordered checkpoints"}
        stages = {record["stage"]: record for record in projected}
        validate_score_roundtrip(saved, stages["reopened"])
        if records[-2]["scores"]["master"]["score_id"] == records[-1]["scores"]["master"]["score_id"]:
            raise ValueError("reopened object identity was not fresh")
        return {
            "state": "readable", "stages": stages, "saved": saved,
            "saved_sha256": row["artifacts"]["roundtrip.mscx"]["sha256"],
            "expectation_differences": assess_expectation(row, stages, stages["reopened"], saved),
        }
    except (KeyError, TypeError, ValueError, ET.ParseError) as error:
        return {"state": "unreadable", "reason": str(error)}


def projection(inspected):
    return inspected["stages"], inspected["saved"]


def summarize(root):
    with (PACKET / "cases.csv").open(newline="") as stream:
        cases = list(csv.DictReader(stream))
    rows = read_jsonl(root / "runs.jsonl")
    expected_rows = [(cell, case["case_id"], b, rep)
                     for cell, (case, b) in enumerate(itertools.product(cases, "UGL"), start=1)
                     for rep in (1, 2)]
    row_key = ("cell", "case_id", "build", "repeat")
    if [tuple(row[key] for key in row_key) for row in rows] != expected_rows:
        raise ValueError("run ledger does not have the sealed cell/repeat order")
    fixture_digest = hashlib.sha256((PACKET / "fixtures/two-parts.mscx").read_bytes()).hexdigest()
    cells = {}
    for cell, group in itertools.groupby(rows, key=lambda row: row["cell"]):
        pair = list(group)
        reads = [examine_run(root, row, fixture_digest) for row in pair]
        pair_status = "unreadable"
        if all(read["state"] == "readable" for read in reads):
            pair_status = "same" if projection(reads[0]) == projection(reads[1]) else "different"
        cells[cell] = {"receipts": pair, "readings": reads, "repeat_consistency": pair_status}

    contrasts = {}
    for offset, case in enumerate(cases):
        variants = {b: cells[3 * offset + i] for i, b in enumerate("UGL", 1)}
        comparisons = {}
        for left, right in ("UG", "UL", "GL"):
            a, b = variants[left], variants[right]
            if a["repeat_consistency"] != "same" or b["repeat_consistency"] != "same":
                comparisons[left+right] = "unknown"
                continue
            ar, br = a["readings"][0], b["readings"][0]
            comparisons[left+right] = "same" if projection(ar) == projection(br) else "different"
            comparisons[left+right+"_saved_bytes_equal"] = ar["saved_sha256"] == br["saved_sha256"]
        contrasts[case["case_id"]] = comparisons
    status = Counter(row["status"] for row in rows)
    state = Counter(read["state"] for cell in cells.values() for read in cell["readings"])
    return {"status": status, "readability": state, "cells": cells, "contrasts": contrasts}


def instance(obj):
    if obj is None:
        return "공석"
    mark = "해당 없음" if obj["mark"] is None else str(int(obj["mark"]))
    return f"{int(obj['flag'])}/{int(obj['member'])}/{mark}"


def describe_music(stages):
    immediate = stages["immediate"]["objects"]
    narrative = []
    for first, second in (("M1", "P1"), ("M2", "P2")):
        a, b = immediate[first], immediate[second]
        if b is None:
            narrative.append(f"{first} {a['pitch']}, {second} 공석")
            continue
        paired = set(a["peers"]) == {first, second} and a["peers"] == b["peers"]
        side = f"{first}↔{second}" if paired else f"{first}/{second} 링크 확인 필요"
        trace = []
        for state in stages.values():
            left, right = state["objects"][first], state["objects"][second]
            if right is None:
                continue
            value = str(left["pitch"])
            if left["pitch"] != right["pitch"]:
                value += f"/{right['pitch']}"
            if not trace or trace[-1] != value:
                trace.append(value)
        narrative.append(f"{side} {'→'.join(trace)}")
    if immediate["C1"]:
        c1 = immediate["C1"]
        link = "무링크" if not c1["peers"] else "/".join(c1["peers"])
        narrative.append(f"C1 {c1['pitch']} {link}")
    narrative.append(f"P2 offset {immediate['P2']['offset_sp'][0]}")
    return ", ".join(narrative)


def markdown(summary):
    print("| 입력ID | 빌드·반복 | flag·목록·mark | 링크·음·다른 파트 | 저장·재열기 관측 | 원 출력·종료값 | 미실시·미확인 |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for cell, info in summary["cells"].items():
        first, second = info["receipts"]
        case = first["case_id"]
        builds = f"{first['build']} 1·2 ({cell:02d})"
        paths = []
        for row in (first, second):
            result = row["artifacts"].get("stdout.jsonl", {}).get("path")
            paths.append(f"[r{row['repeat']}]({result})" if result else f"r{row['repeat']} 공석")
        raw = " · ".join(paths) + f" · exit {first['exit_code']} · {second['exit_code']}"
        if info["repeat_consistency"] != "same":
            problems = ", ".join(r.get("reason", info["repeat_consistency"]) for r in info["readings"])
            print(f"| {case} | {builds} | 판별불능 | 판별불능 | 판별불능 | {raw} | {problems} |")
            continue
        captured = info["readings"][0]
        immediate = captured["stages"]["immediate"]
        objects = immediate["objects"]
        target = {"E03": "P1F", "E05": "C1"}.get(case, "P1")
        owner, _ = OBJECT_LOCATIONS[target]
        selection_count = len(immediate["scores"][owner]["selection"])
        flag = f"{target} {instance(objects[target])}, 목록 {selection_count}개"
        if case == "E03":
            flag += f", P1 음 {instance(objects['P1'])}"
        obj = objects[target]
        color = "선택색" if obj["cur_color"] == obj["selection_color"] else "기본색"
        flag += f", {color}"
        music = describe_music(captured["stages"])
        if case == "E03":
            music += f", 핑거링 {objects['P1F']['text']} 링크 {'↔'.join(objects['P1F']['peers'])}"
        before, after = (captured["stages"][stage]["objects"] for stage in ("before_save", "reopened"))
        musical_fields = ("pitch", "tpc", "offset_sp", "peers", "text")
        preserved = all((a is None and after[label] is None) or (
            a is not None and after[label] is not None
            and all(a.get(field) == after[label].get(field) for field in musical_fields)
        ) for label, a in before.items())
        reopened = "음·링크 유지" if preserved else "음 또는 링크 변화"
        reopened += f", {target} {instance(after[target])}"
        if case == "E04":
            reopened += ", undo 있음" if captured["stages"]["reopened"]["undo_available"] else ", undo 없음"
        if case == "E05":
            reopened += f", C1 track {after['C1']['track']}"
        if case == "E06":
            reopened += f", 색 {after[target]['cur_color']}"
        deviations = ", ".join(captured["expectation_differences"]) or "—"
        print(f"| {case} | {builds} | {flag} | {music} | {reopened} | {raw} | {deviations} |")


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", type=Path, default=PACKET)
    cli.add_argument("--format", choices=("json", "markdown"), default="json")
    args = cli.parse_args()
    answer = summarize(args.root)
    if args.format == "markdown":
        markdown(answer)
    else:
        print(json.dumps(answer, ensure_ascii=False, indent=2))
