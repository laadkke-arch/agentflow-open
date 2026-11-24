"""Compare candidates using only the emitted request and visible complete records."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def serialized(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stamp(value):
    return hashlib.sha256(serialized(value).encode()).hexdigest()


def infer(text):
    """Read a narrow set of explicit request patterns. Unknown wording is held."""
    wording = text.casefold()
    if "text wrapping" in wording:
        return {"intent": "edit-wrapped-text"}
    if "expected order of measures" in wording:
        old = re.search(r"\bnot\s+\.*([\d,]+)", text, re.I)
        new = re.search(r"\bshould be\s+\.*([\d,]+)", text, re.I)
        if old and new:
            old_tokens, new_tokens = old[1].split(","), new[1].split(",")
            common = []
            for before, after in zip(reversed(old_tokens), reversed(new_tokens)):
                if before != after:
                    break
                common.insert(0, before)
            return {"intent": "correct-expectation", "old": old[1], "new": new[1],
                    "suffix": ",".join(common), "anchors": [[old.start(1), old.end(1)], [new.start(1), new.end(1)]]}
    if "rename" in wording and "arrow head attached" in wording:
        return {"intent": "edit-text"}
    instrument = re.search(r"rename the stored (.+?) instrument definition", text, re.I)
    if instrument:
        return {"intent": "rename-instrument-definition", "label": instrument[1],
                "anchors": [[instrument.start(1), instrument.end(1)]]}
    return {"intent": None}


def rows_in(view):
    if view["method"] == "A":
        return []
    section = view["text"][view["request_chars"]:]
    found = []
    offset = view["request_chars"]
    for line in section.splitlines():
        stop = offset + len(line)
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            offset = stop + 1
            continue
        found.append({**item, "chars": [offset, stop]})
        offset = stop + 1
    return found


def locator(item, field):
    return {"record": item["id"], "origin": item["path"], "view_chars": item["chars"], "field": field}


def node_guard(candidate, request, seed, records):
    if candidate["guard"] == "literal":
        if (seed["type"] != candidate["subject"] or not request["suffix"]
                or (seed["label"] or "").count(request["old"]) != 1):
            return "hold", "literal-or-preservation-unverified", None, [], []
        return ("support", "stored-literal-and-suffix", [seed["id"]],
                [f'{seed["id"]}/text:{request["suffix"]}'], [locator(seed, "label")])
    if candidate["guard"] != "relation":
        return "hold", "candidate-operation-has-no-local-preservation-evidence", None, [], []
    if candidate["target"] == "seed" and seed["type"] != candidate["subject"]:
        return "hold", "editing-object-not-visible", None, [], []
    field = candidate["field"]
    outward = candidate["direction"] == "out"
    joined = []
    for other in records:
        if other["type"] != candidate["neighbor_type"] or other["id"] == seed["id"]:
            continue
        start, end = (seed, other) if outward else (other, seed)
        if {"field": field, "to": end["id"]} in start["refs"]:
            joined.append((other, start, end))
    if len(joined) != 1:
        return "hold", "no-visible-unique-endpoint", None, [], []
    other, start, end = joined[0]
    proof = [locator(start, field), locator(end, "id")]
    if required_back := candidate.get("back_field"):
        if {"field": required_back, "to": start["id"]} not in end["refs"]:
            return "hold", "conflicting-back-reference", None, [], proof
        proof.append(locator(end, required_back))
    target = seed if candidate["target"] == "seed" else other
    if target["type"] != candidate["subject"]:
        return "refute", "wrong-entity-type", None, [], proof
    if request.get("label") and target["label"] != request["label"]:
        proof.append(locator(target, "label"))
        return "refute", "endpoint-has-different-name", None, [], proof
    return "support", "direction-and-ref-confirmed", [target["id"]], [f'{start["id"]}.{field}'], proof


def judge(candidate, request, view, records, seeds):
    proof = []
    picks = None
    preserve = []
    if not request["intent"]:
        statement, reason = "hold", "opening-intent-unparsed"
    elif candidate.get("intent", candidate["operation"]) != request["intent"]:
        statement, reason = "refute", "different-operation"
    elif candidate["edition"] != view["edition"]:
        statement, reason = "hold", "same-edition-not-established"
    elif candidate["guard"] == "clause-literal":
        if request["new"] == candidate["clause_value"]:
            statement, reason = "refute", "clause-reference-already-matches-request"
            proof = [{"source": candidate["clause_url"], "scope": "compiled reference literal"}]
        else:
            statement, reason = "hold", "clause-reference-not-resolved"
    elif not view["seed_complete"] or len(seeds) != 1:
        statement, reason = "hold", "ambiguous-selection" if len(seeds) > 1 else "selection-not-visible"
    else:
        statement, reason, picks, preserve, proof = node_guard(candidate, request, seeds[0], records)
    return {"candidate": candidate["id"], "url": candidate["url"], "section": candidate["section"],
            "status": statement, "reason": reason, "selection": picks, "preserve": preserve, "proof": proof}


def evaluate(view, candidates):
    text = view["text"][:view["request_chars"]]
    request = infer(text)
    records = rows_in(view)
    seeds = [r for r in records if r["seed"]]
    rows = [judge(c, request, view, records, seeds) for c in candidates]
    supported = [r for r in rows if r["status"] == "support"]
    winner = supported[0] if len(supported) == 1 else None
    return {
        "input_id": view["input_id"], "method": view["method"], "length_layer": view["length_layer"],
        "view_input_sha256": stamp(view), "candidate_input_sha256": stamp(candidates),
        "candidate_set": view["candidate_set"], "candidates": rows,
        "opening_anchors": request.get("anchors", []),
        "seed_set": [r["id"] for r in seeds] if view["seed_complete"] else None,
        "opened_records": [{"id": r["id"], "origin": r["path"], "view_chars": r["chars"], "refs": r["refs"]}
                           for r in records],
        "outcome": "supported" if winner else "hold",
        "winner": winner["candidate"] if winner else None,
        "selected": winner["selection"] if winner else None,
        "preserved_links": winner["preserve"] if winner else [],
        "application_effect": "unknown",
        "chars": len(view["text"]),
    }


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("views", type=Path)
    cli.add_argument("candidates", type=Path)
    cli.add_argument("output", type=Path)
    cli.add_argument("audit", type=Path)
    args = cli.parse_args()
    permitted = {str(args.views.resolve()): "r", str(args.candidates.resolve()): "r",
                 str(args.output.resolve()): "w", str(args.audit.resolve()): "w"}
    accesses = []

    def audit(event, data):
        if event != "open":
            return
        target, mode = data[:2]
        if not isinstance(target, str) or mode not in {"r", "w"} or permitted.get(target) != mode:
            raise PermissionError(f"unlisted comparator access: {target}")
        accesses.append({"file": Path(target).name, "mode": mode})

    sys.addaudithook(audit)
    views = [json.loads(line) for line in args.views.read_text(encoding="utf-8").splitlines()]
    groups = json.loads(args.candidates.read_text(encoding="utf-8"))
    with args.output.open("w", encoding="utf-8") as out:
        for view in views:
            evaluated = evaluate(view, groups[view["candidate_set"]])
            out.write(serialized({**evaluated, "result_sha256": stamp(evaluated)}) + "\n")
    with args.audit.open("w", encoding="utf-8") as out:
        out.write(serialized({"accesses": accesses, "view_rows": len(views)}) + "\n")


if __name__ == "__main__":
    main()
