"""Normalize observed records and build bounded views. This tool never scores cases."""
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compact(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def jsonl(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def emit(path, rows):
    with path.open("w", encoding="utf-8", newline="\n") as out:
        for row in rows:
            out.write(compact(row) + "\n")


def record(records, key, kind, path, label=None, refs=None, **fields):
    records.append({"id": key, "type": kind, "path": path, "seq": len(records),
                    "label": label, "refs": refs or [], **fields})


def ref(field, target):
    return {"field": field, "to": target}


def drawing(raw):
    source = json.loads(raw)
    if source["type"] not in ("excalidraw", "excalidraw/clipboard"):
        raise ValueError("unsupported Excalidraw root")
    result = []
    for index, item in enumerate(source["elements"]):
        if item.get("isDeleted"):
            continue
        refs = [ref(f"{side}.elementId", item[side]["elementId"])
                for side in ("startBinding", "endBinding") if item.get(side)]
        refs.extend(ref(f'boundElements:{value["type"]}', value["id"])
                    for value in item.get("boundElements") or [])
        refs.extend(ref("boundElementIds", value) for value in item.get("boundElementIds") or [])
        if item.get("containerId"):
            refs.append(ref("containerId", item["containerId"]))
        record(result, item["id"], item["type"], f"/elements/{index}", item.get("text"), refs,
               xy=[item.get("x"), item.get("y")], size=[item.get("width"), item.get("height")],
               groups=item.get("groupIds"), font_size=item.get("fontSize"),
               element_version=item.get("version"))
    return result


def score_xml(raw):
    root = ET.fromstring(raw)
    if root.tag != "score-partwise":
        raise ValueError("instrument control requires partwise MusicXML")
    records = []
    for index, part in enumerate(root.findall("./part-list/score-part"), 1):
        key = part.attrib["id"]
        path = f"/score-partwise/part-list/score-part[{index}]"
        record(records, key, "score-part", path, part.findtext("part-name"))
        for pos, instrument in enumerate(part.findall("score-instrument"), 1):
            record(records, instrument.attrib["id"], "score-instrument",
                   f"{path}/score-instrument[{pos}]", instrument.findtext("instrument-name"), part=key)
    for pos, part in enumerate(root.findall("part"), 1):
        key = part.attrib["id"]
        path = f"/score-partwise/part[{pos}]"
        record(records, f"body:{key}", "part-body", path, refs=[ref("part@id", key)], part=key)
        for index, measure in enumerate(part.findall("measure"), 1):
            location = f"{path}/measure[{index}]"
            ordinal = measure.attrib.get("number")
            record(records, f"body:{key}/measure:{index}", "measure", location,
                   label=ordinal, part=key)
            for n, note in enumerate(measure.findall("note"), 1):
                npath = f"{location}/note[{n}]"
                pitch = note.find("pitch")
                label = None if pitch is None else pitch.findtext("step") + pitch.findtext("octave")
                record(records, note.attrib.get("id") or npath, "note", npath, label,
                       [ref("instrument@id", elem.attrib["id"]) for elem in note.findall("instrument")],
                       measure=ordinal, part=key, voice=note.findtext("voice"),
                       alter=None if pitch is None else pitch.findtext("alter"))
    return records


def native_score(raw):
    root = ET.fromstring(raw)
    if root.tag != "museScore":
        raise ValueError("unsupported native score root")
    score = root.find("Score")
    if score is None:
        raise ValueError("staged MSCX must have a Score root")
    records = []
    for pos, part in enumerate(score.findall("Part"), 1):
        location = f"/museScore/Score/Part[{pos}]"
        record(records, f"part:{pos}", "part", location, part.findtext("trackName"))
        for j, staff in enumerate(part.findall("Staff"), 1):
            key = staff.attrib["id"]
            record(records, f"staff-def:{key}", "staff-definition", f"{location}/Staff[{j}]", staff_id=key)
    for n, staff in enumerate(score.findall("Staff"), 1):
        staff_id = staff.attrib["id"]
        key = f"staff:{staff_id}"
        path = f"/museScore/Score/Staff[{n}]"
        record(records, key, "staff-content", path, refs=[ref("Staff@id", f"staff-def:{staff_id}")],
               staff_id=staff_id)
        counts = Counter()
        for block in staff:
            counts[block.tag] += 1
            block_id = f"{key}/{block.tag}:{counts[block.tag]}"
            block_path = f"{path}/{block.tag}[{counts[block.tag]}]"
            if block.tag in {"TBox", "VBox", "HBox", "FBox"}:
                record(records, block_id, "frame", block_path, block.tag)
                for j, text in enumerate(block.findall("Text"), 1):
                    record(records, f"{block_id}/Text:{j}", "frame-text", f"{block_path}/Text[{j}]",
                           "".join(text.find("text").itertext()), frame_style=text.findtext("style"),
                           frame_kind=block.tag)
            if block.tag == "Measure":
                record(records, block_id, "measure", block_path, str(counts[block.tag]),
                       repeats=[child.tag for child in block if child.tag in {"startRepeat", "endRepeat"}])
                for j, marker in enumerate(block.findall("Marker"), 1):
                    value = marker.findtext("label")
                    record(records, f"{block_id}/Marker:{j}", "marker", f"{block_path}/Marker[{j}]", value)
                for j, jump in enumerate(block.findall("Jump"), 1):
                    record(records, f"{block_id}/Jump:{j}", "jump", f"{block_path}/Jump[{j}]",
                           jump.findtext("text"),
                           target_labels={k: jump.findtext(k) for k in ("jumpTo", "playUntil", "continueAt")})
    by_marker = {}
    for item in records:
        if item["type"] == "marker":
            by_marker.setdefault(item["label"], []).append(item["id"])
    for item in records:
        for field, name in item.get("target_labels", {}).items():
            item["refs"].extend(ref(field, target) for target in by_marker.get(name, []))
    return records


PARSERS = {"excalidraw": drawing, "musicxml": score_xml, "mscx": native_score}


def matches(record, hint):
    if record["type"] != hint["type"]:
        return False
    label = record.get("label") or ""
    if "label" in hint and hint["label"] != label:
        return False
    return "contains" not in hint or hint["contains"] in label


def neighbors(records, seeds, mode):
    ids = {seed["id"] for seed in seeds}
    ordinary = [entry for entry in records if entry["id"] not in ids]
    if not seeds:
        return []
    if mode == "B":
        return sorted(ordinary, key=lambda r: (min(abs(r["seq"] - s["seq"]) for s in seeds), r["seq"]))
    outgoing = {edge["to"] for seed in seeds for edge in seed["refs"]}
    return [r for r in ordinary if r["id"] in outgoing or any(e["to"] in ids for e in r["refs"])]


def pack(request, records, seeds, method, budget):
    text = request["text"]
    if len(text) > budget:
        raise ValueError("opening request exceeds the common budget")
    planned = [] if method == "A" else seeds + neighbors(records, seeds, method)
    fragments = []
    start_ids = {r["id"] for r in seeds}
    for item in planned[:4]:
        line = compact({**item, "seed": item["id"] in start_ids})
        content_from = len(text) + 1
        if content_from >= budget:
            break
        text += "\n" + line[:budget - content_from]
        end = len(text)
        fragments.append({"id": item["id"], "path": item["path"], "seq": item["seq"],
                          "shown": [content_from, end], "complete": end - content_from == len(line),
                          "record_chars": len(line), "seed": item["id"] in start_ids})
    shown_seeds = {f["id"] for f in fragments if f["seed"] and f["complete"]}
    return {"view": method, "text": text, "chars": len(text), "request_chars": len(request["text"]),
            "budget": budget, "attempted_records": len(planned), "record_cap": 4,
            "fragments": fragments, "seed_complete": bool(start_ids) and start_ids == shown_seeds,
            "omitted_records": len(planned) - len(fragments),
            "truncated": any(not f["complete"] for f in fragments) or len(planned) > len(fragments)}


def make_views(inputs, cache):
    for case in inputs:
        if case["status"] != "ready":
            continue
        artifact = cache / f'{case["blob_sha256"]}.bin'
        raw = artifact.read_bytes()
        if digest(raw) != case["blob_sha256"]:
            raise ValueError(f'artifact digest mismatch for {case["id"]}')
        records = PARSERS[case["format"]](raw)
        if len({r["id"] for r in records}) != len(records):
            raise ValueError(f'duplicate record identity in {case["id"]}')
        request = case["request"]
        seeds = [r for r in records if matches(r, request["selector"])]
        ordinary = {kind: pack(request, records, seeds, kind, 1600) for kind in "ABC"}
        limit = min(ordinary[kind]["chars"] for kind in "BC")
        bset = {f["id"] for f in ordinary["B"]["fragments"] if f["complete"]}
        cset = {f["id"] for f in ordinary["C"]["fragments"] if f["complete"]}
        for layer in ("budget", "matched"):
            kinds = "ABC" if layer == "budget" else "BC"
            for kind in kinds:
                view = ordinary[kind] if layer == "budget" else pack(request, records, seeds, kind, limit)
                yield {**view, "input_id": case["id"], "tier": case["tier"], "length_layer": layer,
                       "edition": case["edition"], "request": {k: v for k, v in request.items() if k != "text"},
                       "candidate_set": case["candidate_set"], "open_scope": case["scope"],
                       "blob_sha256": case["blob_sha256"], "open_view_sha256": digest(view["text"].encode()),
                       "comparison": {"common": sorted(bset & cset), "b_only": sorted(bset - cset),
                                      "c_only": sorted(cset - bset), "matched_cap": limit}}


def main():
    args = argparse.ArgumentParser()
    args.add_argument("inputs", type=Path)
    args.add_argument("cache", type=Path)
    args.add_argument("views", type=Path)
    values = args.parse_args()
    emit(values.views, make_views(jsonl(values.inputs), values.cache))


if __name__ == "__main__":
    main()
