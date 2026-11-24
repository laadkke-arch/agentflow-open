"""Summarize the prescribed sixteen raw Rails/browser journeys without inferring unseen stages."""
import csv
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
CASES = (
    ("A1-1", "Apply · Accept offer / references", "reference type for Morgan Example", "referee_type"),
    ("A1-2", "Apply · Accept offer / references", "name for Morgan Example", "name"),
    ("A2-1", "Apply · Course review", "course for AF241 Mathematics (T241)", "course_id"),
    ("A2-2", "Apply · Course review", "full time or part time for AF241 Mathematics (T241)", "study_mode"),
    ("A3-1", "Apply · Contact review", "phone number", "phone_number"),
    ("A3-2", "Apply · Contact review", "address", "address_type"),
    ("R1-1", "Register · Check details", "course", "training_route"),
    ("R1-2", "Register · Check details", "education phase", "course_education_phase"),
)


def differences(before, after):
    changed = {}
    for key in sorted(before.keys() | after.keys()):
        old, new = before.get(key), after.get(key)
        if old == new:
            continue
        changed[key] = differences(old, new) if isinstance(old, dict) and isinstance(new, dict) else [old, new]
    return changed


def encode(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def journey(case, trial):
    anchor, screen, suffix, first_field = case
    jid = f"{anchor}-{trial}"
    receipt = ROOT / "receipts" / "journeys" / f"{jid}.json"
    data = json.loads(receipt.read_text())
    stages = data["stages"]
    before = stages.get("origin", {})
    edit = stages.get("first_edit", {})
    after = stages.get("return", {})
    matches = [a for a in before.get("summaryLinks", []) if any(h["raw"].strip() == suffix for h in a["hidden"])]
    match = matches[0] if len(matches) == 1 else {}
    ax = (match.get("ax") or {}).get("cdpNode", {})
    inputs = [
        dict((key, field[key]) for key in ("name", "id", "type", "value", "checked", "visible"))
        for field in edit.get("inputs", [])
        if field["name"].endswith(f"[{first_field}]")
    ]
    maps = data["models"]
    observed_diff = differences(maps["before"], maps["after"]) if {"before", "after"} <= maps.keys() else "미확인"
    base_url = before.get("url")
    ret_url = after.get("url")
    expected_end = data.get("originPath")
    origin_return = ret_url == base_url and bool(ret_url)
    target_observed = ax.get("role", {}).get("value") == "link" and bool(ax.get("name", {}).get("value"))
    first_observed = bool(edit.get("url")) and bool(inputs) and bool(data.get("tabSteps"))
    missing = []
    if not target_observed:
        missing.append("origin DOM/AX")
    if not first_observed:
        missing.append("Tab/Enter 또는 first edit controls")
    if observed_diff == "미확인":
        missing.append("model before/after")
    if not ret_url:
        missing.append("return")
    return {
        "journey_id": jid, "screen": screen, "anchor_id": anchor, "journey": trial,
        "expected_visible": "Change", "expected_normalized_ax": f"Change {suffix}",
        "expected_first_field": first_field, "expected_origin_path": expected_end,
        "observed_origin_url": base_url, "row_key": match.get("rowKey"), "visible_text": match.get("visibleText"),
        "raw_dom_text": match.get("rawText"), "raw_ax_name": ax.get("name", {}).get("value"),
        "ax_description": ax.get("description", {}).get("value", "AX 필드 없음") if ax else "미확인",
        "ax_role": ax.get("role", {}).get("value"), "dom_ordinal": match.get("documentOrdinal"),
        "ax_ordinal": (match.get("ax") or {}).get("treeOrdinal"), "raw_href": match.get("rawHref"),
        "first_edit_url": edit.get("url"), "first_edit_title": edit.get("title"),
        "first_edit_heading": encode(edit.get("h1", [])), "first_focus": edit.get("focused", {}).get("tag"),
        "first_inputs": encode(inputs), "tab_count": len(data.get("tabSteps", [])),
        "resource_ids": encode(data["resource"]), "inputs_changed_or_reentered": encode(data["inputs_author_changed"]),
        "model_diff": encode(observed_diff), "last_nav_method": data["nav"][-1]["method"] if data["nav"] else "미확인",
        "return_url": ret_url, "return_path": urlsplit(ret_url).path if ret_url else "미확인",
        "return_focus": after.get("focused", {}).get("tag"), "returned_to_origin": origin_return,
        "return_errors": encode(after.get("errors", [])), "harness_errors": encode(data["errors"]),
        "observed_stages": encode(list(stages)), "missing_required_stages": "; ".join(missing),
        "screen_reader_utterance": "미확인", "receipt": str(receipt.relative_to(ROOT)),
    }


with (Path(sys.argv[1]) if len(sys.argv) == 2 else ROOT / "journeys.csv").open(
    "w", encoding="utf-8", newline=""
) as output:
    records = [journey(case, trial) for case in CASES for trial in ("S", "B")]
    writer = csv.DictWriter(output, fieldnames=list(records[0]), quoting=csv.QUOTE_ALL, lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
