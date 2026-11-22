#!/usr/bin/env python3
"""Build cards and replay pinned source sections with a key-free reader."""

import argparse
import ast
import csv
import hashlib
import json
import re
import time
import urllib.request
from collections import Counter
from pathlib import Path

SEED = "210922"
BUDGETS = (1, 2, 4)
FORMATS = ("A", "P", "M")
MODES = ("main", "permuted", "no-links", "mislinked")
ROOT = Path(__file__).resolve().parent
TOKEN = re.compile(r"--?[a-z0-9][a-z0-9_-]*|[a-z0-9_]+", re.I)
STOP = set("a an and are as at be by for from has have i if in into is it its of on or that the this to was were with you your".split())
NEGATIVE = re.compile(
    r"\b(?:cannot|can't|must not|does not|do not|did not|will not|won't|"
    r"not support(?:ed|s)?|not available|no longer|unsupported|removed|"
    r"not possible|not allowed|incompatible|never)\b", re.I
)
OPTIONAL = re.compile(r"\b(?:not (?:strictly )?required|no need|need not|optional|not necessary)\b", re.I)
POSITIVE = re.compile(
    r"\b(?:can|use[sd]?|allow(?:s|ed)?|provide[sd]?|support(?:s|ed)?|"
    r"enable[sd]?|accept(?:s|ed)?|defines?|sets?|returns?|runs?|sets up|"
    r"consists? of|defaults? to|added|requires?|specif(?:y|ies|ied|ying)|"
    r"initiali[sz](?:e|es|ed)|passed|generates?)\b", re.I
)
BLOCK = re.compile(r"\n[ \t]*\n|(?<=[.!?])\s+(?=[A-Z])")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def as_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def key_hash(*values):
    return digest(as_json(values).encode())


def load_json(path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def read_jsonl(path):
    with path.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(as_json(row) + "\n")


def tokens(text):
    return TOKEN.findall(text.lower())


def words(text):
    result = set()
    for word in tokens(text):
        if word.startswith("--"):
            result.add(word[2:])
        if word.isalpha() and len(word) > 4 and word.endswith("s") and not word.endswith(("ss", "us")):
            word = word[:-1]
        if word not in STOP:
            result.add(word)
    return result


def source_headings(code, lines, syntax, filename):
    if syntax == "py":
        def walk(nodes, prefix):
            for node in nodes:
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    start = min([node.lineno] + [deco.lineno for deco in node.decorator_list])
                    name = ".".join([*prefix, node.name])
                    yield start, name
                    if isinstance(node, ast.ClassDef):
                        yield from walk(node.body, [*prefix, node.name])

        return dict([(1, filename), *walk(ast.parse(code).body, [])])

    headings = {1: filename}
    fence = None
    for i, line in enumerate(lines):
        if syntax == "md":
            fence_token = re.match(r"^\s*(`{3,}|~{3,})", line)
            if fence_token:
                marker = fence_token[1]
                if fence is None:
                    fence = marker
                elif marker[0] == fence[0] and len(marker) >= len(fence):
                    fence = None
                continue
            if fence:
                continue
            match = re.fullmatch(r"#{1,6}\s+(.+?)\s*#*\s*", line)
            if match:
                headings[i + 1] = match[1]
        elif syntax == "rst" and i + 1 < len(lines):
            under = lines[i + 1].strip()
            if line and not line[0].isspace() and len(under) >= 3 and len(under) >= len(line.rstrip()) - 1:
                if len(set(under)) == 1 and under[0] in "=-~^\"+'*`:#_":
                    headings[i + 1] = line.rstrip()
    return headings


def materialize(registry, cache, stage):
    cache.mkdir(parents=True, exist_ok=True)
    folder = stage / "sections"
    folder.mkdir(parents=True, exist_ok=True)
    result = []
    for doc in load_json(registry):
        cached = cache / doc["id"]
        if not cached.exists():
            with urllib.request.urlopen(doc["raw_url"], timeout=25) as response:
                cached.write_bytes(response.read())
        blob = cached.read_bytes()
        if digest(blob) != doc["sha256"]:
            raise ValueError(f'changed remote bytes: {doc["id"]}')
        code = blob.decode("utf-8")
        lines = code.splitlines()
        syntax = doc["syntax"]
        if syntax == "cmake":
            start, delimiters = next((i, re.fullmatch(r"#\[(=*)\[\.rst:", line))
                                     for i, line in enumerate(lines) if re.fullmatch(r"#\[(=*)\[\.rst:", line))
            end = lines.index("#]" + delimiters[1] + "]", start + 1)
            lines = [""] * (start + 1) + lines[start + 1:end]
            syntax = "rst"
        headings = source_headings(code, lines, syntax, Path(doc["path"]).stem)
        bounds = sorted(headings) + [len(lines) + 1]
        for first, after in zip(bounds, bounds[1:]):
            for start in range(first, after, 32):
                stop = min(start + 31, after - 1)
                text = "\n".join(lines[start - 1:stop])
                if not text.strip():
                    continue
                ident = f'{doc["id"]}:{start}-{stop}'
                name = ident.replace(":", "_") + ".txt"
                path = folder / name
                path.write_text(text, encoding="utf-8")
                result.append({
                    "id": ident, "doc": doc["id"], "title": headings[first],
                    "file": name, "first": start, "last": stop, "sha256": digest(text.encode()),
                    "name": Path(doc["path"]).stem, "url": doc["url"],
                    "location": f'{doc["url"]}#L{start}-L{stop}',
                })
    write_json(stage / "index.json", result)


def locate(sections, doc, line):
    matches = [s["id"] for s in sections if s["doc"] == doc and s["first"] <= line <= s["last"]]
    if len(matches) != 1:
        raise ValueError(f"location cannot resolve: {doc} L{line}")
    return matches[0]


def public_cases(cases):
    for case in sorted(cases, key=lambda row: (row["published_utc"], row["id"])):
        question = {k: case[k] for k in ("id", "original_excerpt", "requirements")}
        candidate_fields = ("id", "label", "use", "description", "identifiers", "release")
        question["candidates"] = [
            {k: c[k] for k in candidate_fields}
            for c in sorted(case["candidates"], key=lambda c: key_hash(SEED, case["id"], c["id"]))
        ]
        yield question


def build(input_dir, stage, receipts):
    started = time.perf_counter()
    cases = list(public_cases(read_jsonl(input_dir / "cases.jsonl")))
    plan = {x["row"]: x for x in read_jsonl(input_dir / "evidence/card-plan.jsonl")}
    index = load_json(stage / "index.json")
    documents = {s["doc"]: s["url"] for s in index}
    activities = Counter()
    elapsed = Counter()
    packets = []
    equivalence = []
    for case in cases:
        for candidate in case["candidates"]:
            row = candidate["id"]
            rule = plan[row]
            doc = rule["doc"]
            shared = {k: candidate[k] for k in ("id", "label", "use", "description", "release")}
            shared.update({"question": case["id"], "source": doc, "url": documents[doc]})
            links = []
            for fmt in FORMATS:
                tic = time.perf_counter_ns()
                locations = [] if fmt == "A" else list(dict.fromkeys(locate(index, doc, l) for l in rule["positions"]))
                if fmt == "M":
                    permitted = {"use"} | {r["id"] for r in case["requirements"]}
                    for key, raw_positions in sorted(rule["links"].items()):
                        if key not in permitted:
                            raise ValueError(f"unknown criterion key: {row} {key}")
                        linked = list(dict.fromkeys(locate(index, doc, line) for line in raw_positions))
                        if not set(linked) <= set(locations):
                            raise ValueError(f"link outside P's position list: {row}")
                        links.extend({"from": key, "to": target} for target in linked)
                payload = {**shared, "positions": locations, "links": links if fmt == "M" else []}
                n_tokens = len(tokens(as_json(payload)))
                if n_tokens > 256:
                    raise ValueError(f"card token cap exceeded: {row} {fmt} {n_tokens}")
                packets.append({**payload, "format": fmt, "tokens": n_tokens})
                activities[f"{fmt}_cards"] += 1
                activities[f"{fmt}_locations"] += len(locations)
                activities[f"{fmt}_links"] += len(payload["links"])
                elapsed[fmt] += time.perf_counter_ns() - tic
            a, p, m = packets[-3:]
            common = [key_hash({k: packet[k] for k in shared}) for packet in (a, p, m)]
            lists = [key_hash(packet["positions"]) for packet in (p, m)]
            sets = [key_hash(sorted(set(packet["positions"]))) for packet in (p, m)]
            if len(set(common)) != 1 or lists[0] != lists[1] or sets[0] != sets[1]:
                raise ValueError(f"treatment equivalence failed: {row}")
            equivalence.append({"row": row, "common": common[0], "positions": lists[0],
                                "position_set": sets[0], "tokens": [x["tokens"] for x in (a, p, m)]})
    write_jsonl(stage / "questions.jsonl", cases)
    write_jsonl(stage / "packets.jsonl", packets)
    write_json(receipts, {"seed": SEED, "rows": equivalence, "counts": dict(activities),
                          "render_ns": dict(elapsed), "wall_s": round(time.perf_counter() - started, 6),
                          "read": ["cases.jsonl", "evidence/card-plan.jsonl", "index.json"]})


def identifiers(candidate):
    return set().union(*(words(name) for name in candidate["identifiers"]))


def rank(index, inquiry, candidate, packet, mode):
    if packet["format"] == "A":
        available = index
    else:
        positions = packet["positions"]
        if mode == "permuted":
            positions = sorted(positions, key=lambda loc: key_hash(SEED, mode, packet["id"], loc))
        by_id = {s["id"]: s for s in index}
        available = [by_id[loc] for loc in positions]
    ids = identifiers(candidate)
    required = [r for r in inquiry["requirements"] if r["kind"] in ("required", "forbidden")]
    required_ids = {r["id"] for r in required}
    query = words(inquiry["original_excerpt"])
    terms = words(candidate["description"] + " " + candidate["use"])
    for req in required:
        terms.update(words(" ".join(req["terms"])))
    graph = {}
    for link in packet["links"] if mode != "no-links" else ():
        target = link["to"]
        if mode == "mislinked" and len(available) > 1:
            order = sorted(s["id"] for s in available)
            target = order[(order.index(target) + 1) % len(order)]
        priority = 1 if link["from"] == "use" else 2 if link["from"] in required_ids else 0
        graph[target] = max(graph.get(target, 0), priority)

    def sort_key(section):
        text = words(section["title"] + " " + section["name"])
        score = 3 * len(text & ids) + 2 * len(text & (terms - ids)) + len(text & (query - terms - ids))
        return (-graph.get(section["id"], 0), -score,
                key_hash(SEED, inquiry["id"], candidate["id"], section["id"]))

    work = [(sort_key(s), s) for s in available]
    return sorted(work, key=lambda x: x[0])


def assess(section, text, inquiry, candidate):
    ids = identifiers(candidate)
    heading_words = words(section["title"])
    reqs = [r for r in inquiry["requirements"] if r["kind"] in ("required", "forbidden")]
    observations = []
    fragments = BLOCK.split(text)
    for req in reqs:
        cue = words(" ".join(req["terms"]))
        for fragment in fragments:
            seen = words(fragment)
            if (not ids & (seen | heading_words)) or (cue and not cue & seen):
                continue
            negative = NEGATIVE.search(fragment)
            optional = OPTIONAL.search(fragment)
            positive = POSITIVE.search(fragment)
            if optional and not negative:
                observations.append({"req": req["id"], "signal": "optional", "cue": optional[0].lower()})
                continue
            invocation = any(re.search(r"\b" + re.escape(name) + r"\s*(?:\(|=|:)", fragment, re.I)
                             for name in candidate["identifiers"])
            if not (positive or negative or invocation):
                continue
            grants = negative is None
            matches = grants == (req["kind"] != "forbidden")
            observations.append({"req": req["id"], "signal": "support" if matches else "conflict",
                                 "cue": (negative or positive)[0].lower() if (negative or positive) else "call"})
    return sorted({as_json(o): o for o in observations}.values(),
                  key=lambda o: (o["req"], o["signal"], o["cue"]))


def summarize(opened, inquiry):
    supports = {event["id"] for event in opened for signal in event.get("signals", [])
                if signal["signal"] == "support"}
    conflicts = {event["id"] for event in opened for signal in event.get("signals", [])
                 if signal["signal"] == "conflict"}
    reqs = {r["id"] for r in inquiry["requirements"] if r["kind"] in ("required", "forbidden")}
    met = {signal["req"] for event in opened for signal in event.get("signals", [])
           if signal["signal"] == "support"}
    if conflicts:
        return {"verdict": "conflict", "cited": sorted(conflicts)}
    if met == reqs and supports:
        return {"verdict": "support", "cited": sorted(supports)}
    return {"verdict": "hold", "cited": sorted(supports)}


def replay(stage, out, mode, receipt):
    start = time.perf_counter()
    stage = stage.resolve()
    index = load_json(stage / "index.json")
    questions = read_jsonl(stage / "questions.jsonl")
    packets = read_jsonl(stage / "packets.jsonl")
    by_question = {x["id"]: x for x in questions}
    candidates = {c["id"]: c for question in questions for c in question["candidates"]}
    by_doc = {}
    for section in index:
        by_doc.setdefault(section["doc"], []).append(section)

    manifest = {}
    for name in ("index.json", "questions.jsonl", "packets.jsonl"):
        manifest[name] = digest((stage / name).read_bytes())
    # The section inventory comes from hashes in the verified index. Bodies are read below on demand.
    manifest["sections"] = key_hash({s["file"]: s["sha256"] for s in index})
    outcomes = []
    timing = []
    for packet in packets:
        before = time.perf_counter_ns()
        question, candidate = by_question[packet["question"]], candidates[packet["id"]]
        sections = by_doc[packet["source"]]
        ranked = rank(sections, question, candidate, packet, mode)
        opened = []
        for score, section in ranked[:4]:
            file = stage / "sections" / section["file"]
            event = {"id": section["id"], "route": [abs(score[0]), abs(score[1])],
                     "sha256": section["sha256"], "order": len(opened) + 1}
            try:
                data = file.read_bytes()
                if digest(data) != event["sha256"]:
                    raise ValueError("section hash mismatch")
                event["signals"] = assess(section, data.decode("utf-8"), question, candidate)
            except (ValueError, OSError) as error:
                event["error"] = str(error).replace(str(stage), "<stage>")
            opened.append(event)
        eligible = {s["id"] for _, s in ranked}
        exclusions = {s["id"]: "budget" for _, s in ranked[4:]}
        exclusions.update({s["id"]: "outside_positions" for s in sections if s["id"] not in eligible})
        # One contiguous section-ID inventory is enough to audit the large URL-only pools.
        grouped = {reason: [s["id"] for s in sections if exclusions.get(s["id"]) == reason]
                   for reason in ("budget", "outside_positions")}
        outcomes.append({"q": question["id"], "row": candidate["id"], "format": packet["format"],
                         "mode": mode, "reader": "python-rule", "eligible": len(ranked), "opened": opened,
                         "excluded": {k: {"count": len(v), "ids_sha256": key_hash(v), "first": v[:4]}
                                      for k, v in grouped.items()},
                         "at": {str(budget): summarize(opened[:budget], question) for budget in BUDGETS}})
        timing.append({"row": candidate["id"], "format": packet["format"],
                       "elapsed_ns": time.perf_counter_ns() - before})
    write_jsonl(out, outcomes)
    write_json(receipt, {"allowlist": ["index.json", "questions.jsonl", "packets.jsonl", "sections/*.txt"],
                         "input": manifest, "partition": list(by_question), "mode": mode,
                         "runs_sha256": digest(out.read_bytes()), "rows": len(outcomes),
                         "wall_s": round(time.perf_counter() - start, 6), "timings": timing})


def measures(rows, key_by_row, basis, budget):
    counters = Counter(questions=len({row["q"] for row in rows}), rows=len(rows))
    for row in rows:
        key = key_by_row[row["row"]]
        target = key[basis]
        expect = target["verdict"]
        pred = row["at"][str(budget)]
        opened = {e["id"] for e in row["opened"][:budget] if "error" not in e}
        counters["opened"] += len(opened)
        counters["read_errors"] += sum("error" in e for e in row["opened"][:budget])
        counters["ref_positive"] += expect == "support"
        counters["ref_conflict"] += expect == "conflict"
        counters["ref_hold"] += expect == "hold"
        counters["pred_hold"] += pred["verdict"] == "hold"
        counters["pred_support"] += pred["verdict"] == "support"
        counters["pred_conflict"] += pred["verdict"] == "conflict"
        mapped = target["allowed"]
        reached = any(set(group) <= opened for group in mapped)
        cited = any(set(group) <= opened and set(group) & set(pred["cited"]) for group in mapped)
        counters["mapped"] += bool(mapped)
        counters["reached"] += reached
        counters["unreached"] += bool(mapped) and not reached
        counters["unmapped_decidable"] += expect != "hold" and not mapped
        counters["pos_reached"] += expect == "support" and reached
        counters["pos_recovered"] += expect == "support" and pred["verdict"] == "support" and cited
        counters["pos_rejected"] += expect == "support" and pred["verdict"] == "conflict"
        counters["all_wrong_approved"] += expect == "conflict" and pred["verdict"] == "support"
        counters["near"] += expect == "conflict" and key["natural_near"]
        counters["near_approved"] += expect == "conflict" and key["natural_near"] and pred["verdict"] == "support"
    return counters


METRICS = (
    "questions", "rows", "ref_positive", "ref_conflict", "ref_hold",
    "pred_support", "pred_conflict", "pred_hold", "mapped", "reached", "unreached",
    "unmapped_decidable", "pos_reached", "pos_recovered", "pos_rejected",
    "all_wrong_approved", "near", "near_approved", "opened", "read_errors",
)


def score(runs, keys, out):
    logs = [row for path in runs for row in read_jsonl(path)]
    key_by_row = {row["row"]: row for row in read_jsonl(keys)}
    qids = sorted({row["q"] for row in logs})
    formats = {(row["mode"], row["row"], row["format"]) for row in logs}
    if len(formats) != len(logs):
        raise ValueError("duplicate run rows")
    if {row["row"] for row in logs if row["mode"] == "main"} != set(key_by_row):
        raise ValueError("main run and key row sets differ")
    modes = sorted({row["mode"] for row in logs}, key=MODES.index)
    rows = []
    for mode in modes:
        group = [row for row in logs if row["mode"] == mode]
        for qid in ["ALL", *qids]:
            sample = group if qid == "ALL" else [row for row in group if row["q"] == qid]
            for basis in ("official", "history"):
                for budget in BUDGETS:
                    measured = {}
                    for fmt in FORMATS:
                        subset = [row for row in sample if row["format"] == fmt]
                        value = measures(subset, key_by_row, basis, budget)
                        measured[fmt] = value
                        entry = {k: value[k] for k in METRICS}
                        per = value["opened"] / value["pos_recovered"] if value["pos_recovered"] else ""
                        rows.append({"mode": mode, "q": qid, "basis": basis, "budget": budget,
                                     "format": fmt, **entry, "opened_per_success": per})
                    if len({v["rows"] for v in measured.values()}) != 1:
                        raise ValueError(f"format denominator differs: {mode} {qid}")
                    for new, old in (("P", "A"), ("M", "P")):
                        delta = {k: measured[new][k] - measured[old][k] for k in METRICS}
                        rows.append({"mode": mode, "q": qid, "basis": basis, "budget": budget,
                                     "format": f"{new}-{old}", **delta, "opened_per_success": ""})
    with out.open("w", encoding="utf-8", newline="") as file:
        wr = csv.DictWriter(file, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(required=True, dest="action")
    corpus = commands.add_parser("index")
    corpus.add_argument("--registry", type=Path, default=ROOT / "evidence/documents.json")
    corpus.add_argument("--cache", type=Path, required=True)
    corpus.add_argument("--stage", type=Path, required=True)
    cards = commands.add_parser("build")
    cards.add_argument("--input", type=Path, default=ROOT)
    cards.add_argument("--stage", type=Path, required=True)
    cards.add_argument("--receipt", type=Path, required=True)
    read = commands.add_parser("read")
    read.add_argument("--stage", type=Path, required=True)
    read.add_argument("--out", type=Path, required=True)
    read.add_argument("--receipt", type=Path, required=True)
    read.add_argument("--mode", choices=MODES, default="main")
    judge = commands.add_parser("score")
    judge.add_argument("--runs", type=Path, nargs="+", required=True)
    judge.add_argument("--keys", type=Path, required=True)
    judge.add_argument("--out", type=Path, required=True)
    cmd = parser.parse_args()
    if cmd.action == "index":
        materialize(cmd.registry, cmd.cache, cmd.stage)
    elif cmd.action == "build":
        build(cmd.input, cmd.stage, cmd.receipt)
    elif cmd.action == "read":
        replay(cmd.stage, cmd.out, cmd.mode, cmd.receipt)
    elif cmd.action == "score":
        score(cmd.runs, cmd.keys, cmd.out)


if __name__ == "__main__":
    main()
