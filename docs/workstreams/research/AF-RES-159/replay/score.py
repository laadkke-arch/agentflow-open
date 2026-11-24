#!/usr/bin/env python3
"""Reconcile the sealed candidate links with the bindings and the observed PO/MO."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
from statistics import median

from seal import ROOT, dump_csv


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def read_jsonl(path):
    with path.open(encoding="utf-8") as source:
        return [json.loads(line) for line in source]


def compare(predictions, packets, calls, lookup):
    for before in predictions:
        call = calls[before["call_id"]]
        run = lookup[before["call_id"], before["language"], "context"]
        links = json.loads(before["candidate_urls"])
        view = before["view"]
        packet = packets[before["packet_id"]]
        right_link = call["return_url"]
        if before["decision"] == "유일":
            status = "유일_일치" if links == [right_link] else "오승인"
        elif not links:
            status = "보류_목표누락"
        else:
            status = "여럿_목표포함" if right_link in links else "여럿_목표누락"
        yield dict(
            packet_id=packet["packet_id"], call_id=call["id"], group=call["group"],
            language=before["language"], view=view,
            candidate_count=len(links), pre_decision=before["decision"],
            target_source=call["anchor_url"], target_function=right_link, function_result=status,
            po_state=run["po_state"], po_url=run["po_url"], msgstr=run["po_msgstr"],
            observed=run["stdout"], falls_back=run["fallback_to_msgid"],
            string_result="원문 반환" if run["fallback_to_msgid"] else "원판 번역 바이트 일치"
            if run["po_msgstr"] == run["stdout"] and run["mo_has_key"] else "불일치",
            role=call["role"], cost_bytes=packet["payload_bytes"],
            increment_bytes=packet["extra_bytes"], context_reference_bytes=packet["reference_bytes"],
        )


def neighbor(rows, packet_index, calls, sources):
    """Post-opening sensitivity: wrongly use an unrelated token as a source file hint."""
    for row in rows:
        if row["layer"] != "natural_candidate" or row["status"] != "sealed":
            continue
        group = row["id"]
        keys = json.loads(row["all_refs"])
        root = sources[group[0]]
        for side, peer in ("ab", "ba"):
            own = calls[group + side]
            for contrast, origin in (("same-file", side), ("swapped", peer)):
                p = packet_index[(group + origin, "ko", "C")]
                evidence = p["source_span"]
                token = evidence["text"]
                b = packet_index[(group + side, "ko", "B")]
                contexts = []
                for key in keys:
                    for file, _ in key["references"]:
                        path = root / file
                        if path.is_file() and token.encode() in path.read_bytes():
                            contexts.append(key["context"])
                            break
                singleton = len(contexts) == 1
                fits = p["reference_bytes"] <= b["reference_bytes"]
                verdict = "budget_exceeded"
                if fits:
                    verdict = "ambiguous" if not singleton else (
                        "accidental_correct" if contexts[0] == own["context"] else "false_certainty"
                    )
                yield dict(
                    group=group, call_id=own["id"], variant=contrast, token=token,
                    token_origin=f'{evidence["path"]}:{evidence["line"]}',
                    actual_context=own["context"], contexts_matching_any_candidate_file=json.dumps(
                        contexts, ensure_ascii=False
                    ), verdict=verdict, token_bytes=p["reference_bytes"],
                    available_bytes=b["reference_bytes"],
                )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gimp", required=True, type=Path)
    parser.add_argument("--inkscape", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "evidence")
    args = parser.parse_args()
    predictions = read_csv(ROOT / "predictions.csv")
    frame = read_csv(ROOT / "frame.csv")
    calls = {r["id"]: r for r in read_csv(ROOT / "calls.csv")}
    packets = {r["packet_id"]: r for r in read_jsonl(ROOT / "packets.jsonl")}
    packet_index = {(r["call_id"], r["payload"]["language"], r["view"]): r for r in packets.values()}
    lookup = {(r["call_id"], r["language"], r["mode"]): r
              for r in read_jsonl(ROOT / "runs.jsonl") if (
                  r["row_type"] == "lookup" and r["repeat"] == "W1" and r["catalog"] == "compiled"
              )}
    results = list(compare(predictions, packets, calls, lookup))
    weak = list(neighbor(frame, packet_index, calls, {"G": args.gimp, "I": args.inkscape}))
    dump_csv(args.output / "scores.csv", results)
    dump_csv(args.output / "neighbor-sensitivity.csv", weak)
    for r in results:
        if r["view"] == "B" and r["function_result"] != "유일_일치":
            raise AssertionError(r)
    print("function", Counter((r["view"], r["function_result"]) for r in results))
    print("neighbor", Counter((r["variant"], r["verdict"]) for r in weak))
    cost = [(r["view"], r["increment_bytes"]) for r in results]
    for view in dict.fromkeys(v for v, _ in cost):
        values = [amount for v, amount in cost if v == view]
        print(view, min(values), median(values), max(values))
    same = Counter()
    for r in lookup.values():
        if r["mode"] == "wrong_live":
            correct = lookup[r["call_id"], r["language"], "context"]
            same[(r["language"], r["stdout"] == correct["stdout"], r["mo_has_key"])] += 1
    print("wrong_live matches", same)


if __name__ == "__main__":
    main()
