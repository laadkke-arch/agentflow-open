"""Reproduce the fixed slots and select equal-codepoint source excerpts."""
from __future__ import annotations

import argparse
from bisect import bisect_left
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import re
from time import perf_counter
import unicodedata

ROOT = Path(__file__).resolve().parent
TOKEN = re.compile(r"[a-z0-9_]+")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def jsonl(rows):
    return b"".join(json.dumps(row, ensure_ascii=False, sort_keys=True,
                               separators=(",", ":")).encode("utf-8") + b"\n" for row in rows)


def read_jsonl(raw):
    return [json.loads(line) for line in raw.split(b"\n") if line]


def normalized(text):
    return unicodedata.normalize("NFKC", text).casefold()


def tokens(text):
    return set(TOKEN.findall(normalized(text)))


def normalized_with_origins(text):
    """Carry original codepoint spans through NFKD, canonical composition and folding."""
    if text.isascii():
        return text.casefold(), None
    ordered = []
    nonstarters = []
    for index, char in enumerate(text):
        for part in unicodedata.normalize("NFKD", char):
            record = (part, index, index + 1)
            if unicodedata.combining(part):
                nonstarters.append(record)
            else:
                ordered.extend(sorted(nonstarters, key=lambda item: unicodedata.combining(item[0])))
                nonstarters.clear()
                ordered.append(record)
    ordered.extend(sorted(nonstarters, key=lambda item: unicodedata.combining(item[0])))

    composed = []
    starter = None
    last_class = 0
    for char, start, end in ordered:
        mark_class = unicodedata.combining(char)
        if starter is not None and (last_class == 0 or last_class < mark_class):
            base, base_start, base_end = composed[starter]
            merged = unicodedata.normalize("NFC", base + char)
            if len(merged) == 1:
                composed[starter] = (merged, min(base_start, start), max(base_end, end))
                continue
        if not mark_class:
            starter = len(composed)
        composed.append((char, start, end))
        last_class = mark_class

    pieces, origins = [], []
    for char, start, end in composed:
        folded = char.casefold()
        pieces.append(folded)
        origins.extend([(start, end)] * len(folded))
    value = "".join(pieces)
    if value != normalized(text):
        raise ValueError("NFKC/casefold provenance decomposition disagrees with Python")
    return value, origins


def occurrences(text, wanted):
    value, origins = normalized_with_origins(text)
    hits = []
    for match in TOKEN.finditer(value):
        token = match.group()
        if token in wanted:
            start, end = match.span()
            if origins is not None:
                provenance = origins[start:end]
                start = min(item[0] for item in provenance)
                end = max(item[1] for item in provenance)
            hits.append((start, end, token))
    return sorted(hits)


def first_window(text, queries):
    matched = set().union(*queries) & tokens(text)
    anchor = None
    if matched:
        options = "|".join(re.escape(token) for token in sorted(matched))
        match = re.search(r"(?<![a-z0-9_])(?:" + options + r")(?![a-z0-9_])", text, re.I)
        if match is not None:
            anchor = match.start()
    start = max(0, (anchor or 0) - 200)
    return (start, min(len(text), start + 1200)), anchor


def start_candidates(size, width, hits):
    last = size - width
    return {0, last, *(min(last, max(0, start - 100)) for start, _, _ in hits)}


def clamp(start, last):
    return max(0, min(last, start))


def candidate_pairs(size, first, second, hits):
    left_base = start_candidates(size, first, hits)
    right_base = start_candidates(size, second, hits)
    # One symmetric expansion from base starts adds adjacent boundaries.
    left = left_base | {clamp(start - first, size - first) for start in right_base}
    right = right_base | {clamp(start + first, size - second) for start in left_base}
    return sorted(left), sorted(right)


def unique_token_masks(starts, width, hits, bits):
    offsets = [start for start, _, _ in hits]
    masks = {}
    for start in starts:
        end = start + width
        mask = 0
        for index in range(bisect_left(offsets, start), bisect_left(offsets, end)):
            _, token_end, token = hits[index]
            if token_end <= end:
                mask |= bits[token]
        masks[start] = mask
    return masks


def split_window(text, queries, first_range):
    size = len(text)
    budget = first_range[1] - first_range[0]
    if budget < 2:
        return [first_range], {"status": "same-as-W1-under-two-codepoints"}
    query_union = set().union(*queries)
    bits = {token: 1 << index for index, token in enumerate(sorted(query_union))}
    query_masks = [sum(bits[token] for token in query) for query in queries]
    hits = occurrences(text, query_union)
    small, large = budget // 2, (budget + 1) // 2
    orientations = sorted({(small, large), (large, small)})
    best_key, best_ranges, best_mask = None, None, 0
    profiles = []
    for left_size, right_size in orientations:
        left, right = candidate_pairs(size, left_size, right_size, hits)
        left_masks = unique_token_masks(left, left_size, hits, bits)
        right_masks = unique_token_masks(right, right_size, hits, bits)
        tested = 0
        for first in left:
            next_right = bisect_left(right, first + left_size)
            for second in right[next_right:]:
                tested += 1
                union_mask = left_masks[first] | right_masks[second]
                count1 = (union_mask & query_masks[0]).bit_count()
                count2 = (union_mask & query_masks[1]).bit_count()
                key = (-min(count1, count2), -(count1 + count2), first, second, left_size)
                if best_key is None or key < best_key:
                    best_key, best_mask = key, union_mask
                    best_ranges = [(first, first + left_size), (second, second + right_size)]
        profiles.append({
            "widths": [left_size, right_size], "start_counts": [len(left), len(right)],
            "candidate_start_sha256": digest(jsonl([left, right])), "disjoint_pairs_tested": tested,
        })
    if best_ranges is None:
        raise ValueError("no disjoint pair at required budget")
    return best_ranges, {
        "status": "two-segments", "normalized_query_occurrences": len(hits),
        "occurrence_sha256": digest(jsonl(hits)), "orientations": profiles,
        "objective": [-best_key[0], -best_key[1]], "selected_query_hits": [
            sorted(token for token in query if best_mask & bits[token]) for query in queries
        ],
    }


def make_segment(raw, text, start, end):
    byte_start = len(text[:start].encode("utf-8"))
    byte_end = len(text[:end].encode("utf-8"))
    data = raw[byte_start:byte_end]
    if data != text[start:end].encode("utf-8"):
        raise ValueError("source coordinate round trip failed")
    first_line = text.count("\n", 0, start) + 1
    last_line = text.count("\n", 0, max(start, end - 1)) + 1
    return {"unicode": [start, end], "utf8": [byte_start, byte_end], "lines_lf": [first_line, last_line],
            "chars": end - start, "bytes": byte_end - byte_start, "sha256": digest(data)}


def header(case, slots):
    preconditions = [f"{c['id']} {c['requirement']}" for c in case["conditions"]]
    return "\n".join([case["title"], case["revision_url"], *case["question_context"],
                      *preconditions, *(f"{s['slot']} {s['url'] or '공석'}" for s in slots)]) + "\n"


def checked_input(root, file_name, sha):
    raw = (root / file_name).read_bytes()
    if digest(raw) != sha:
        raise ValueError(f"pinned input digest mismatch: {file_name}")
    return raw


def originals(root, protocol):
    data = {name: checked_input(root, name, sha)
            for name, sha in protocol["sealed_inputs_sha256"].items()}
    source = read_jsonl(gzip.decompress(data["corpus-files.jsonl.gz"]))
    s_packets = [row for row in read_jsonl(data["packets.jsonl"]) if row["mode"] == "S"]
    packet_index = {(row["case_id"], row["policy"]): row for row in s_packets}
    if len(s_packets) != len(packet_index) or len(packet_index) != 16:
        raise ValueError("prior S ledger must contain 16 unique case-policy rows")
    return {row["file_id"]: row for row in source}, packet_index


def source_data(root, registered):
    body = (root / registered["cached_body"]).resolve()
    if not body.is_relative_to((root / "evidence" / "_cache").resolve()):
        raise ValueError("invalid cache path")
    raw = body.read_bytes()
    if len(raw) != registered["bytes"] or digest(raw) != registered["sha256"]:
        raise ValueError(f"source byte fingerprint mismatch: {registered['file_id']}")
    return raw, raw.decode("utf-8")


def old_s_check(pinned_slot, descriptor_slot, segment, anchor, raw, text):
    actual = dict(char_start=segment["unicode"][0], char_end=segment["unicode"][1],
                  byte_start=segment["utf8"][0], byte_end=segment["utf8"][1],
                  exposed_chars=segment["chars"], exposed_bytes=segment["bytes"],
                  exposed_sha256=segment["sha256"], source_chars=len(text), source_bytes=len(raw),
                  git_blob_sha=git_blob(raw), sha256=digest(raw))
    differences = {}
    for field, value in actual.items():
        if pinned_slot[field] != value or descriptor_slot[field] != value:
            differences[field] = [pinned_slot[field], descriptor_slot[field], value]
    if pinned_slot["anchor_char"] != anchor or pinned_slot["anchor_fallback"] != (anchor is None):
        differences["anchor"] = [pinned_slot["anchor_char"], pinned_slot["anchor_fallback"], anchor]
    return differences


def build(cache, protocol, protocol_digest):
    inventory, old_packets = originals(cache, protocol)
    packets, plan = [], {}
    preparation = Counter()
    for case in protocol["cases"]:
        case_id = case["case_id"]
        queries = [set(words) for words in case["query_tokens"]]
        for policy in ("A", "B"):
            old = old_packets[case_id, policy]
            descriptor_name = f"evidence/packet-descriptors/{old['packet_id']}.json"
            descriptor = json.loads(checked_input(cache, descriptor_name, protocol["s_descriptors_sha256"][old["packet_id"]]))
            if old["query_tokens"] != case["query_tokens"] or old["question_id"] != case["question_id"]:
                raise ValueError(f"case tokens or question changed: {case_id}")
            if len(old["slots"]) != 4 or len(descriptor["slots"]) != 4:
                raise ValueError("expected four slots, including vacancies")
            route_slots = {"W1": [], "W2": []}
            for previous, public in zip(old["slots"], descriptor["slots"], strict=True):
                slot_number = previous["slot"]
                source_id = previous["file_id"]
                for field in ("slot", "file_id", "empty", "url", "sha256"):
                    if previous[field] != public[field]:
                        raise ValueError(f"prior S descriptor differs from ledger: {case_id} {policy} {field}")
                slot = {key: previous.get(key) for key in
                        ("slot", "file_id", "empty", "role", "url", "sha256", "git_blob_sha", "repo", "path",
                         "version", "commit", "within_role_rank", "score", "empty_reason")}
                slot["charged_accesses"] = 1
                if source_id is None:
                    route_slots["W1"].append({**slot, "segments": [], "prior_s_differences": {}})
                    route_slots["W2"].append({**slot, "segments": []})
                    continue
                if (case_id, source_id) not in plan:
                    raw, text = source_data(cache, inventory[source_id])
                    baseline, anchor = first_window(text, queries)
                    chosen, stats = split_window(text, queries, baseline)
                    initial = make_segment(raw, text, *baseline)
                    split = [make_segment(raw, text, *bounds) for bounds in chosen]
                    if sum(segment["chars"] for segment in split) != initial["chars"]:
                        raise ValueError("not equal codepoint budgets")
                    if len(split) == 2 and split[0]["unicode"][1] > split[1]["unicode"][0]:
                        raise ValueError("overlapping disjoint windows")
                    plan[case_id, source_id] = initial, split, stats, anchor, raw, text
                    preparation["case_file_computations"] += 1
                    preparation["raw_chars_scanned_per_method"] += len(text)
                    preparation["raw_bytes_scanned_per_method"] += len(raw)
                    preparation["W1_raw_regex_searches"] += int(bool(set().union(*queries) & tokens(text)))
                    preparation["W2_normalized_occurrences"] += stats.get("normalized_query_occurrences", 0)
                    preparation["W2_eligible_candidate_pairs"] += sum(o["disjoint_pairs_tested"] for o in stats.get("orientations", []))
                initial, split, stats, anchor, raw, text = plan[case_id, source_id]
                if inventory[source_id]["sha256"] != previous["sha256"] or inventory[source_id]["url"] != previous["url"]:
                    raise ValueError(f"selected file identity differs from corpus: {source_id}")
                differences = old_s_check(previous, public, initial, anchor, raw, text)
                slot["source_chars"] = len(text)
                slot["source_bytes"] = len(raw)
                route_slots["W1"].append({**slot, "segments": [initial], "prior_s_differences": differences,
                                           "first_raw_anchor": anchor})
                route_slots["W2"].append({**slot, "segments": split, "search": stats})
            if [slot["slot"] for slot in route_slots["W1"]] != [1, 2, 3, 4]:
                raise ValueError("original slot order changed")
            if sum(slot["segments"][0]["chars"] for slot in route_slots["W1"] if slot["segments"]) != old["total_exposed_chars"]:
                preparation["prior_s_packet_total_mismatches"] += 1
            for mode, slots in route_slots.items():
                identity = "\0".join((case_id, policy, mode, protocol_digest)).encode()
                meta = header(case, slots)
                metrics = Counter({"charged_accesses": 4, "additional_moves": 0,
                                   "display_chars": 0, "display_utf8_bytes": 0,
                                   "empty_slots": sum(s["empty"] for s in slots),
                                   "fixed_reader_metadata_chars": len(meta),
                                   "fixed_reader_metadata_utf8_bytes": len(meta.encode()),
                                   "segment_boundary_markers": 0})
                for slot in slots:
                    for item in slot["segments"]:
                        metrics["display_chars"] += item["chars"]
                        metrics["display_utf8_bytes"] += item["bytes"]
                        metrics["segment_boundary_markers"] += 1
                packets.append({"schema": 1, "packet_id": digest(identity)[:16],
                                "case_id": case_id, "question_id": case["question_id"], "policy": policy,
                                "window": mode, "prior_S_packet_id": old["packet_id"], "slots": slots,
                                "metrics": dict(metrics), "reader_metadata_sha256": digest(meta.encode()),
                                "prior_s_packet_total_chars": old["total_exposed_chars"]})
    if len(packets) != 32 or len({p["packet_id"] for p in packets}) != 32:
        raise ValueError("expected 32 distinct packet ids")
    return packets, dict(preparation)


def totals(packets):
    result = {}
    for mode in ("W1", "W2"):
        items = [p for p in packets if p["window"] == mode]
        sums = Counter()
        selected = {}
        files, spans = set(), set()
        for packet in items:
            sums.update(packet["metrics"])
            for slot in packet["slots"]:
                if not slot["empty"]:
                    identity = (slot["file_id"], slot["sha256"])
                    files.add(identity)
                    selected[identity] = selected.get(identity, []) + [
                        tuple(s["unicode"]) for s in slot["segments"]
                    ]
                    spans.update((identity, *s["unicode"]) for s in slot["segments"])
        distinct_chars = 0
        for intervals in selected.values():
            last = 0
            for start, end in sorted(intervals):
                distinct_chars += max(0, end - max(last, start))
                last = max(last, end)
        result[mode] = {**sums, "packets": len(items), "unique_file_ids": len(files),
                        "unique_spans": len(spans), "unique_source_codepoints": distinct_chars}
    result["prior_s"] = {
        "compared_real_slots": sum(not s["empty"] for p in packets if p["window"] == "W1" for s in p["slots"]),
        "slot_mismatches": [{"packet_id": p["packet_id"], "slot": s["slot"], "diff": s["prior_s_differences"]}
                            for p in packets if p["window"] == "W1" for s in p["slots"] if s["prior_s_differences"]],
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = (ROOT / "protocol.json").read_bytes()
    start_utc = datetime.now(timezone.utc).isoformat()
    start = perf_counter()
    packets, preparation = build(args.cache.resolve(), json.loads(raw), digest(raw))
    report = {"protocol_sha256": digest(raw), "unicode_database": unicodedata.unidata_version,
              "packets": totals(packets), "preparation": preparation}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "packets.jsonl").write_bytes(jsonl(packets))
    (args.output / "packet-costs.json").write_bytes(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n")
    print(json.dumps({"started_utc": start_utc, "finished_utc": datetime.now(timezone.utc).isoformat(),
                      "elapsed_seconds": perf_counter() - start, "packet_sha256": digest(jsonl(packets)),
                      "costs_sha256": digest((args.output / "packet-costs.json").read_bytes())}, sort_keys=True))


if __name__ == "__main__":
    main()
