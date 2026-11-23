"""Validate packets and reconstruct matched comparisons plus post-lock audit records."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import io
import json
from pathlib import Path

from reader_input import load
from select_passages import ROOT, digest, jsonl, make_segment, read_jsonl

LABELS = ("left_only", "right_only", "both", "neither", "incomparable")


def read(path):
    return json.loads(path.read_bytes())


def contained(ranges, start, end):
    return any(left <= start < end <= right for left, right in ranges)


def overlapping_chars(ranges, start, end):
    cursor = start
    size = 0
    for left, right in sorted(ranges):
        size += max(0, min(right, end) - max(left, cursor))
        cursor = max(cursor, right)
    return size


def slot_spans(packet):
    return {slot["file_id"]: [span["unicode"] for span in slot["segments"]]
            for slot in packet["slots"] if not slot["empty"]}


def line_span(raw, source, first, last):
    lines = source.split("\n")
    if not 1 <= first <= last <= len(lines):
        raise ValueError("lines out of bounds")
    start = sum(len(line) + 1 for line in lines[:first - 1])
    end = min(len(source), sum(len(line) + 1 for line in lines[:last]))
    return make_segment(raw, source, start, end)


def historical(cache, revised, current, bodies, decisions):
    prior_packets = read_jsonl((cache / "packets.jsonl").read_bytes())
    old_map = {(p["case_id"], p["policy"], p["mode"]): p for p in prior_packets}
    old_by_id = {p["packet_id"]: p for p in prior_packets}
    old_judgments = read_jsonl((cache / "judgments.jsonl").read_bytes())
    prev = {j["packet_id"]: j for j in old_judgments}
    previous_metrics = read(cache / "evidence" / "derived" / "metrics.json")
    if len(old_map) != 32 or len(prev) != 32:
        raise ValueError("unexpected prior cardinality")
    audit, old_states, f_display = [], {}, {}
    for judgment in old_judgments:
        packet = old_by_id[judgment["packet_id"]]
        key = tuple(packet[field] for field in ("case_id", "policy", "mode"))
        new_ids = {w: revised[key[0], key[1], w]["packet_id"] for w in ("W1", "W2")}
        shown = {w: slot_spans(revised[key[0], key[1], w]) for w in new_ids}
        if key[2] == "F":
            f_display[key[:2]] = defaultdict(list)
            events = read_jsonl((cache / "evidence" / "packet-access" / f"{packet['packet_id']}.jsonl").read_bytes())
            for event in events:
                if event.get("status") == "success" and event["finished_utc"] <= judgment["initial_judgment_recorded_utc"]:
                    for segment in event.get("displayed_segments", []):
                        f_display[key[:2]][event["file_id"]].append((segment["char_start"], segment["char_end"]))
        for cond in judgment["conditions"]:
            cond_id = cond["id"]
            old_states[(*key, cond_id)] = cond["status"]
            roles = decisions["prior_citation_roles"]["/".join(key)][cond_id]
            for index, (cite, role) in enumerate(zip(cond["citations"], roles, strict=True), 1):
                source_id = cite["file_id"]
                slot = packet["slots"][cite["slot"] - 1]
                raw, text = bodies[source_id]
                lo, hi = (cite["char_start"], cite["char_end"])
                checked = make_segment(raw, text, lo, hi)
                if source_id != slot["file_id"] or cite["url"] != slot["url"] or not slot["char_start"] <= lo < hi <= slot["char_end"]:
                    raise ValueError("old citation outside its pinned slot")
                if checked["utf8"] != [cite["byte_start"], cite["byte_end"]]:
                    raise ValueError("old citation UTF-8 mismatch")
                coverage = {}
                for window in shown:
                    spans = shown[window].get(source_id, [])
                    overlap = overlapping_chars(spans, lo, hi)
                    coverage[window] = {"packet_id": new_ids[window], "overlap_codepoints": overlap,
                                        "union_full": overlap == hi - lo, "single_segment_full": contained(spans, lo, hi)}
                audit.append({"prior_mode": key[2], "prior_packet_id": packet["packet_id"],
                              "case_id": key[0], "policy": key[1], "condition_id": cond_id, "citation_ordinal": index,
                              "role": decisions["role_legend"][role], "file_id": source_id, "url": cite["url"],
                              "section": cite["section"], "prior_relation": cite["relation"],
                              "source_sha256": slot["sha256"], "checked_range": checked, "window_coverage": coverage})
    if len(audit) != previous_metrics["citations_checked"] or len(audit) != 115:
        raise ValueError("all original citations require roles and byte validation")

    old_f = defaultdict(list)
    for item in audit:
        if item["prior_mode"] == "F":
            old_f[item["case_id"], item["policy"], item["condition_id"]].append(item)
    effects = []
    for row in current:
        packet = packet_by_id(revised, row["packet_id"])
        case, policy, mode = (packet[k] for k in ("case_id", "policy", "window"))
        key = case, policy, row["condition_id"]
        proofs = old_f[key]
        old_sources_fully_inside = [f"{c['prior_packet_id']}:{c['condition_id']}:{c['citation_ordinal']}"
                                    for c in proofs if c["window_coverage"][mode]["single_segment_full"]]
        effects.append({
            "phase": "post_lock_F_audit", "packet_id": row["packet_id"], "condition_id": row["condition_id"],
            "prior_F_status": old_states[case, policy, "F", key[-1]],
            "prior_S_status": old_states[case, policy, "S", key[-1]],
            "prior_F_citations": len(proofs), "prior_F_citations_whole_in_single_segment": old_sources_fully_inside,
            "alternate_proof_of_same_condition": decisions["replacement"].get("/".join((case, policy, mode, key[-1]))),
            "exact_earlier_citation_overlap_is_not_semantic_support": True,
        })
    prior_full = {(c, p, m): prev[packet["packet_id"]]["complete"] for (c, p, m), packet in old_map.items()}
    return audit, effects, prior_full, f_display, previous_metrics


def packet_by_id(packets, packet_id):
    return next(p for p in packets.values() if p["packet_id"] == packet_id)


def feature_audit(decisions, revised, f_display, bodies):
    output = []
    for feature in decisions["features"]:
        raw, text = bodies[feature["file_id"]]
        checked = line_span(raw, text, *feature["lines"])
        for policy in feature["policies"]:
            key = feature["case"], policy
            modes = {w: slot_spans(revised[(*key, w)]).get(feature["file_id"], []) for w in ("W1", "W2")}
            modes["F"] = f_display[key].get(feature["file_id"], [])
            flags = {w: contained(spans, *checked["unicode"]) for w, spans in modes.items()}
            output.append({**feature, "policy": policy, "range": checked, "fully_in_one_displayed_segment": flags})
    return output


def usable(left, right, axis):
    if left["metrics"]["empty_slots"] or right["metrics"]["empty_slots"]:
        return "P3-B slots 3 and 4 have no reproducible fixed Docker release corpus"
    if any(slot.get("prior_s_differences") for p in (left, right) for slot in p["slots"]):
        return "legacy S slot replay differs"
    if axis == "W1/W2":
        for a, b in zip(left["slots"], right["slots"], strict=True):
            if (a["slot"], a["file_id"], a["sha256"]) != (b["slot"], b["file_id"], b["sha256"]):
                return "file identity differs"
            if sum(s["chars"] for s in a["segments"]) != sum(s["chars"] for s in b["segments"]):
                return "slot codepoint budgets differ"
        if left["reader_metadata_sha256"] != right["reader_metadata_sha256"]:
            return "fixed reader metadata differs"
    return ""


def classify(left, right, exclusion):
    if exclusion:
        return "incomparable"
    return {(True, True): "both", (True, False): "left_only",
            (False, True): "right_only", (False, False): "neither"}[left, right]


def aggregates(rows):
    result = {}
    for axis in ("W1/W2", "A/B"):
        items = [p for p in rows if p["axis"] == axis]
        counts = Counter(p["result"] for p in items)
        result[axis] = {"assigned": len(items), "eligible": len(items) - counts["incomparable"],
                        **{name: counts[name] for name in LABELS}}
    return result


def pairs(cases, revised, completed, audit, features):
    all_pairs = []
    f_recall = defaultdict(list)
    for item in audit:
        if item["prior_mode"] == "F":
            f_recall[item["case_id"], item["policy"]].append(item)
    for axis, labels in (("W1/W2", ("A", "B")), ("A/B", ("W1", "W2"))):
        for case in cases:
            for label in labels:
                cid = case["case_id"]
                routes = [(label, w) for w in ("W1", "W2")] if axis == "W1/W2" else [(p, label) for p in ("A", "B")]
                left, right = [revised[cid, p, w] for p, w in routes]
                exclusion = usable(left, right, axis)
                lhs, rhs = (completed[p["packet_id"]] for p in (left, right))
                recall = [f"{sum(v['window_coverage'][w]['single_segment_full'] for v in f_recall[cid, p])}/{len(f_recall[cid, p])}"
                          for p, w in routes]
                shown = [{x["id"] for x in features if x["case"] == cid and x["policy"] == pol
                          and x["fully_in_one_displayed_segment"][w]} for pol, w in routes]
                all_pairs.append({"axis": axis, "pair_id": f"{'WIN' if axis == 'W1/W2' else 'POL'}-{cid}-{label}",
                                  "case_id": cid, "comparison": label, "stratum": case["stratum"],
                                  "left_packet": left["packet_id"], "right_packet": right["packet_id"],
                                  "left_complete": lhs, "right_complete": rhs, "eligible": not exclusion,
                                  "result": classify(lhs, rhs, exclusion), "exclusion": exclusion,
                                  "left_earlier_F_exact": recall[0], "right_earlier_F_exact": recall[1],
                                  "left_only_feature_ids": " ".join(sorted(shown[0] - shown[1])),
                                  "right_only_feature_ids": " ".join(sorted(shown[1] - shown[0]))})
    if len(all_pairs) != 32 or len({p["pair_id"] for p in all_pairs}) != 32:
        raise ValueError("unbalanced pair axes")
    return all_pairs


def exact_validation(cases, packets, bodies, initial):
    case_conditions = {case["case_id"]: {c["id"] for c in case["conditions"]} for case in cases}
    by_packet = {p["packet_id"]: p for p in packets}
    if len(packets) != 32 or len(by_packet) != 32 or sum(len(p["slots"]) for p in packets) != 128:
        raise ValueError("unexpected packet cardinality")
    for packet in packets:
        for index, slot in enumerate(packet["slots"], 1):
            if index != slot["slot"] or slot["charged_accesses"] != 1:
                raise ValueError("invalid slot reordering or cost")
            if slot["empty"]:
                if slot["segments"]:
                    raise ValueError("vacancy unexpectedly displays text")
                continue
            raw, text = bodies[slot["file_id"]]
            prior_end = 0
            for span in slot["segments"]:
                start, end = span["unicode"]
                if not (prior_end <= start < end <= len(text)) or span != make_segment(raw, text, start, end):
                    raise ValueError("bad UTF-8 pair or segment overlap")
                prior_end = end
    grouped = defaultdict(dict)
    n_citations = 0
    for j in initial:
        p = by_packet[j["packet_id"]]
        if j["condition_id"] in grouped[j["packet_id"]]:
            raise ValueError("duplicate condition")
        grouped[j["packet_id"]][j["condition_id"]] = j["status"]
        for cite in j["citations"]:
            stored = p["slots"][cite["slot"] - 1]
            span = stored["segments"][cite["segment"] - 1]
            file = stored["file_id"]
            raw, text = bodies[file]
            recomputed = make_segment(raw, text, *cite["unicode"])
            if (file != cite["file_id"] or stored["url"] != cite["url"]
                    or not contained([span["unicode"]], *cite["unicode"])
                    or not contained([span["utf8"]], *cite["utf8"])
                    or any(cite[k] != recomputed[k] for k in ("utf8", "sha256", "lines_lf"))):
                raise ValueError("current citation outside its displayed window")
            n_citations += 1
    for pid, packet in by_packet.items():
        if grouped[pid].keys() != case_conditions[packet["case_id"]]:
            raise ValueError("a packet lacks condition observations")
    return {pid: all(s == "supported" for s in conditions.values()) for pid, conditions in grouped.items()}, n_citations


def sensitivities(primary):
    scenarios = {}
    scenarios["P1_builtin_only_same_call"] = aggregates(primary)
    scenarios["P1_original_main_tag_required"] = aggregates([r for r in primary if r["case_id"] != "P1"])
    stricter = []
    for r in primary:
        if r["case_id"] == "J1":
            stricter.append({**r, "result": classify(False, False, r["exclusion"])})
        else:
            stricter.append(r)
    scenarios["J1_final_join_success_required"] = aggregates(stricter)
    return scenarios


def read_exposures(packets, cases):
    prior_files = set()
    by_case = []
    for case in cases:
        cid = case["case_id"]
        rows = sorted([p for p in packets if p["case_id"] == cid], key=lambda p: p["packet_id"])
        source_ids = set().union(*(set(slot_spans(p)) for p in rows))
        physical = {(file_id, tuple(span)) for p in rows for file_id, spans in slot_spans(p).items() for span in spans}
        count = sum(len(s["segments"]) for p in rows for s in p["slots"])
        record = {"case_id": cid, "opaque_packet_ids_in_view_order": [p["packet_id"] for p in rows],
                  "packet_segment_occurrences": count, "physical_segments_printed_once": len(physical),
                  "same_file_exposed_in_prior_case": sorted(source_ids & prior_files),
                  "cross_case_exposed_positions": sum(bool(set(slot_spans(p)) & prior_files) for p in rows),
                  "same_case_routes_presented_together": len(rows),
                  "cross_case_overlap_by_packet": {
                      p["packet_id"]: sorted(set(slot_spans(p)) & prior_files) for p in rows
                  }}
        by_case.append(record)
        prior_files.update(source_ids)
    return by_case


def verify_or_save(name, raw, check):
    p = ROOT / name
    if check:
        if p.read_bytes() != raw:
            raise ValueError(f"reproduced output differs from {name}")
    else:
        p.write_bytes(raw)


def pretty(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    protocol = read(ROOT / "protocol.json")
    packets, bodies = load(args.cache, ROOT / "packets.jsonl", protocol)
    cases = protocol["cases"]
    revised = {(p["case_id"], p["policy"], p["window"]): p for p in packets}
    judgments = read_jsonl((ROOT / "judgments.jsonl").read_bytes())
    initial = [row for row in judgments if row["phase"] == "initial_opaque_self_read"]
    lock = read(ROOT / "evidence" / "initial-read-lock.json")
    if digest(jsonl(initial)) != lock["sha256"]:
        raise ValueError("first-pass judgment bytes differ from remote seal")
    completed, citations = exact_validation(cases, packets, bodies, initial)
    decisions = read(ROOT / "evidence" / "audit-decisions.json")
    audit, effects, old_complete, f_display, old_metrics = historical(args.cache, revised, initial, bodies, decisions)
    features = feature_audit(decisions, revised, f_display, bodies)
    primary = pairs(cases, revised, completed, audit, features)
    f_lost = []
    changes = []
    for (case, policy, window), packet in revised.items():
        if window == "W1":
            if old_complete[case, policy, "F"] and not old_complete[case, policy, "S"]:
                f_lost.append({"case": case, "policy": policy, **{w: completed[revised[case, policy, w]["packet_id"]] for w in ("W1", "W2")}})
            for row in effects:
                if row["packet_id"] == packet["packet_id"]:
                    now = next(j["status"] for j in initial if (j["packet_id"], j["condition_id"]) == (row["packet_id"], row["condition_id"]))
                    if now != row["prior_S_status"]:
                        changes.append({"case": case, "policy": policy, "condition": row["condition_id"],
                                        "previous_S": row["prior_S_status"], "current_W1": now})
    exposure = read_exposures(packets, cases)
    original_f = [r for r in audit if r["prior_mode"] == "F"]
    current_packets = {p["packet_id"]: p for p in packets}
    source_rows = read_jsonl((ROOT / "sources.jsonl").read_bytes())
    counted = [s for s in source_rows if s["census_counted"]]
    if len({s["fixed_url"] for s in counted}) != len(counted):
        raise ValueError("duplicate fixed URL in source census")
    groups = Counter(r["census_group"] for r in counted)
    cross_groups = Counter(r["question_and_case"][-1] for r in counted if r["census_group"] == "crossdomain")
    if (len(counted) < 26 or groups["inherited_r0"] != 8 or groups["inherited_main"] < 8
            or groups["inherited_adjacent"] < 6 or cross_groups["SQLite"] < 2 or cross_groups["CSS Grid"] < 2):
        raise ValueError("source census misses a required fixed group")
    metrics = {
        "schema": "af-res-104-v1", "cases": len(cases), "packets": len(packets), "slots": sum(len(p["slots"]) for p in packets),
        "initial_condition_judgments": len(initial), "initial_citations_verified_visible": citations,
        "current_complete": {w: sum(v for pid, v in completed.items() if current_packets[pid]["window"] == w)
                             for w in ("W1", "W2")},
        "comparisons": aggregates(primary), "sensitivity": sensitivities(primary),
        "retained_F_to_S_loss_routes": f_lost,
        "F_to_S_loss_routes_recovered": {w: sum(r[w] for r in f_lost) for w in ("W1", "W2")},
        "same_s_range_condition_label_changes": changes,
        "same_s_range_packet_complete_changes": [
            [case, policy] for (case, policy, w), p in revised.items()
            if w == "W1" and completed[p["packet_id"]] != old_complete[case, policy, "S"]
        ],
        "old_citations": {"all_checked": len(audit), "F_checked": len(original_f),
                          "by_role_and_mode": {mode: dict(Counter(r["role"] for r in audit if r["prior_mode"] == mode)) for mode in ("F", "S")},
                          "F_whole_in_single_segment": {w: sum(r["window_coverage"][w]["single_segment_full"] for r in original_f) for w in ("W1", "W2")},
                          "F_whole_in_union": {w: sum(r["window_coverage"][w]["union_full"] for r in original_f) for w in ("W1", "W2")},
                          "F_any_overlap": {w: sum(r["window_coverage"][w]["overlap_codepoints"] > 0 for r in original_f) for w in ("W1", "W2")}},
        "new_refuted_conditions": sum(r["status"] == "refuted" for r in initial),
        "source_census": {"rows": len(source_rows), "counted": len(counted), "by_group": dict(groups),
                          "new_main_case_sample": 0},
        "prior_author_execution_verified_count": old_metrics["outcomes"]["same_version_input_output_verified"],
        "feature_visibility": {
            kind: {"placements": len(items), "F_visible": sum(x["F"] for x in items),
                   "W1_only": sum(x["W1"] and not x["W2"] for x in items),
                   "W2_only": sum(x["W2"] and not x["W1"] for x in items),
                   "F_visible_lost_in_W1": sum(x["F"] and not x["W1"] for x in items),
                   "F_visible_lost_in_W2": sum(x["F"] and not x["W2"] for x in items)}
            for kind in sorted({r["kind"] for r in features})
            for items in [[r["fully_in_one_displayed_segment"] for r in features if r["kind"] == kind]]
        },
        "case_group_overlap": {"positions_with_prior_case_file": sum(x["cross_case_exposed_positions"] for x in exposure),
                               "case_groups": len(exposure), "within_group_possible_for": 32},
        "packet_costs": read(ROOT / "evidence" / "packet-costs.json"),
        "repeat_receipts": read(ROOT / "evidence" / "packet-replay.json")["exact_cmp"],
    }
    if len(f_lost) != old_metrics["F_to_S_complete_losses"]:
        raise ValueError("prior F/S transition tally differs")
    table = io.StringIO()
    csv_writer = csv.DictWriter(table, fieldnames=list(primary[0]), lineterminator="\n")
    csv_writer.writeheader()
    csv_writer.writerows(primary)
    for name, raw in [
        ("judgments.jsonl", jsonl(initial + effects)),
        ("pairs.csv", table.getvalue().encode()),
        ("metrics.json", pretty(metrics)),
        ("evidence/prior-citations-audit.jsonl", jsonl(audit)),
        ("evidence/feature-visibility.jsonl", jsonl(features)),
        ("evidence/exposure.json", pretty(exposure)),
    ]:
        verify_or_save(name, raw, args.check)
    print(json.dumps({"checked": args.check, "first_judgments": len(initial), "new_citations": citations,
                      "old_citations": len(audit), "comparison": metrics["comparisons"],
                      "source_census": metrics["source_census"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
