"""Build verifiable opening fixtures and A/B/C shipments from the frozen frame."""
import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re

from collect import ROOT, digest, make_frame

MAX_RECORDS = 4
MAX_CHARS = 1200
ARROW = re.compile(r"\s*(?:--+>|-\.-|---|==+>)\s*")
NODE = re.compile(r"^([\w]+)(?:\s*([{(\[].*))?$")
SUBGRAPH = re.compile(r"^subgraph\s+([\w]+)")
FRAGMENT = re.compile(r"^(alt|opt|par|loop|critical|break)\b", re.I)
PIE_SLICE = re.compile(r'^"([^"]+)"\s*:\s*(\d+(?:\.\d+)?)')


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def json_lines(path, values):
    path.write_text("".join(compact(value) + "\n" for value in values), encoding="utf-8")


def pointer(key):
    return str(key).replace("~", "~0").replace("/", "~1")


@dataclass
class Record:
    path: str
    value: object
    line: int | None = None

    def wire(self):
        return compact({"path": self.path, "value": self.value}) + "\n"


def vega_records(raw):
    try:
        spec = json.loads(raw)
        parse_state = "strict JSON"
    except json.JSONDecodeError:
        # Limited to the known pasted fixture with only trailing commas.
        spec = json.loads(re.sub(r",(?=\s*[}\]])", "", raw))
        parse_state = "record extraction only after trimming trailing commas"
    records = []

    def traverse(obj, path=""):
        for key, value in obj.items():
            item_path = path + "/" + pointer(key)
            if key in ("layer", "hconcat", "vconcat", "concat"):
                for index, unit in enumerate(value):
                    traverse(unit, f"{item_path}/{index}")
            elif key in ("encoding", "datasets"):
                records.extend(Record(f"{item_path}/{pointer(n)}", c) for n, c in value.items())
            elif key == "params":
                records.extend(Record(f"{item_path}/{index}", item) for index, item in enumerate(value))
            else:
                records.append(Record(item_path, value))

    traverse(spec)
    by_path = {r.path: r for r in records}
    refs = []
    for r in records:
        if r.path == "/data" and isinstance(r.value, dict) and r.value.get("name"):
            definition = "/datasets/" + pointer(r.value["name"])
            if definition in by_path:
                refs.append((r.path, definition, "data.name→datasets key"))
        if not isinstance(r.value, dict) or "/encoding/" not in r.path:
            continue
        condition = r.value.get("condition", {})
        if isinstance(condition, dict) and condition.get("param"):
            refs.extend(
                (r.path, d.path, "condition.param→params.name")
                for d in records if re.search(r"/params/\d+$", d.path)
                and d.value.get("name") == condition["param"]
            )
        axis = r.value.get("axis", {})
        if isinstance(axis, dict) and axis.get("formatType") not in (None, "number", "time"):
            if "/config" in by_path and "customFormatTypes" in by_path["/config"].value:
                refs.append((r.path, "/config", "local custom format→explicit config gate"))
    for r in records:
        if not re.search(r"/params/\d+$", r.path):
            continue
        selection = r.value.get("select", {})
        if isinstance(selection, dict):
            base = r.path.rsplit("/params/", 1)[0]
            for channel in selection.get("encodings", ()):
                path = f"{base}/encoding/{pointer(channel)}"
                if path in by_path:
                    refs.append((r.path, path, "select.encodings→channel definition"))
    return records, refs, parse_state


def mermaid_records(raw):
    records = [
        Record(f"/line/{line}", text, line)
        for line, text in enumerate(raw.splitlines(), 1) if text.strip() and not text.strip().startswith("%%")
    ]
    diagram = records[0].value.strip().lower()
    refs, scope, definitions, uses, slices = [], [], {}, [], []

    def define(key, record):
        definitions.setdefault(key, []).append(record.path)

    for r in records:
        text = r.value.strip()
        if diagram.startswith("pie"):
            if PIE_SLICE.match(text):
                slices.append(r.path)
        elif diagram == "sequencediagram":
            if text.lower() == "end" and scope:
                refs.append((scope.pop(), r.path, "fragment→closing end"))
            elif FRAGMENT.match(text):
                if scope:
                    refs.append((scope[-1], r.path, "fragment→nested fragment"))
                scope.append(r.path)
            elif scope:
                refs.append((scope[-1], r.path, "fragment→direct content"))
        else:
            group = SUBGRAPH.match(text)
            if text == "end" and scope:
                refs.append((scope.pop(), r.path, "subgraph→closing end"))
                continue
            if scope:
                refs.append((scope[-1], r.path, "subgraph→direct member or statement"))
            if group:
                define(group[1], r)
                scope.append(r.path)
                continue
            endpoints = ARROW.split(text)
            for part in endpoints:
                node = NODE.match(part)
                if not node:
                    continue
                if len(endpoints) == 1 or node[2]:
                    define(node[1], r)
                if len(endpoints) > 1:
                    uses.append((node[1], r.path))
    for key, use in uses:
        for definition in definitions.get(key, ()):
            if use != definition:
                refs.append((use, definition, f"edge endpoint→declaration:{key}"))
    if slices:
        refs.extend((records[0].path, path, "pie root→one input slice for total") for path in slices)
    return records, refs, "line records, lexical occurrence IDs"


def anchors(records, project, tokens):
    seeds = []
    for r in records:
        if project == "V":
            if not isinstance(r.value, dict):
                continue
            selection = r.value.get("select", {})
            sorting = r.value.get("sort", {})
            match = (
                ("temporal" in tokens and r.value.get("type") == "temporal")
                or ("descending" in tokens and isinstance(sorting, dict) and sorting.get("order") == "descending")
                or ("interval" in tokens and isinstance(selection, dict) and selection.get("type") == "interval")
                or ("color" in tokens and r.path.endswith("/encoding/color"))
            )
        else:
            text = r.value.strip()
            match = any(
                text.replace(" ", "") == token if "-->" in token
                else (token == "percentages" and bool(PIE_SLICE.match(text)))
                or re.match(rf"(?i)^{re.escape(token)}\b", text)
                for token in tokens
            )
        if match:
            seeds.append(r.path)
    return seeds


def neighborhood(records, refs, seeds, mode):
    positions = {r.path: i for i, r in enumerate(records)}
    if mode == "A" or not seeds:
        return []
    if mode == "B":
        seed_places = [positions[p] for p in seeds]
        neighbors = sorted(
            (p for p in positions if p not in seeds),
            key=lambda p: (min(abs(positions[p] - n) for n in seed_places), positions[p]),
        )
    else:
        neighbors = {
            b if a in seeds else a
            for a, b, _ in refs if a in seeds or b in seeds
        } - set(seeds)
        neighbors = sorted(neighbors, key=positions.get)
    return [records[positions[p]] for p in seeds + list(neighbors)]


def pack(records, limit):
    parts = []
    visible = []
    clips = []
    left = limit
    for i, r in enumerate(records):
        wire = r.wire()
        count = min(left, len(wire)) if i < MAX_RECORDS else 0
        if count == len(wire):
            visible.append(asdict(r))
        elif count:
            clips.append({"path": r.path, "characters": count, "full_characters": len(wire),
                          "reason": "character cap", "fragment": wire[:count]})
        else:
            clips.append({"path": r.path, "characters": 0, "full_characters": len(wire),
                          "reason": "record cap" if i >= MAX_RECORDS else "character cap"})
        parts.append(wire[:count])
        left -= count
    return "".join(parts), visible, clips


def views(case, records, refs, seeds, menu):
    request = case["request"]
    options = {k: menu[k] for k in case["candidates"]}
    rankings = {v: neighborhood(records, refs, seeds, v) for v in "ABC"}
    matched_size = min(len(pack(rankings[v], MAX_CHARS)[0]) for v in "BC")
    menu_chars = len(compact(options))
    for kind in "ABC":
        for tier, limit in ([("cap", MAX_CHARS)] if kind == "A" else [("cap", MAX_CHARS), ("matched", matched_size)]):
            text, included, cut = pack(rankings[kind], limit)
            paths = {record["path"] for record in included}
            yield {
                "id": case["id"],
                "view": kind,
                "budget": tier,
                "request_characters": len(request),
                "menu_characters": menu_chars,
                "common_total_character_cap": len(request) + menu_chars + MAX_CHARS,
                "structure_cap": limit,
                "structure_characters": len(text),
                "total_characters": len(request) + menu_chars + len(text),
                "start_candidates": seeds if kind != "A" else [],
                "records": included,
                "cut_records": cut,
                "both_endpoints_visible": [
                    list(e) for e in refs if {e[0], e[1]} <= paths
                ],
                "input": {"request": request, "options": options, "structure": text},
            }


def build(pages):
    decisions = json.loads((ROOT / "selection.json").read_text())
    menu = json.loads((ROOT / "links.json").read_text())
    all_cases, all_views, graphs, archive = [], [], [], []
    original = ROOT / "fixtures" / "original"
    original.mkdir(parents=True, exist_ok=True)
    for project in "VM":
        for row, state, rank, specs, _ in make_frame(pages, project):
            archive.append(dict(row, project=project))
            id = f"{project}{row['number']}"
            decision = decisions.get(id, {})
            if decision.get("selection") not in ("selected", "auxiliary"):
                continue
            body = row["body"]
            spans = []
            for passage in decision["request"]:
                i = body.index(passage)
                start = len(body[:i].encode("utf-8"))
                spans.append({"start": start, "end": start + len(passage.encode("utf-8")), "text": passage})
            case = {
                "id": id,
                "project": project,
                "sample_layer": "natural" if decision["selection"] == "selected" else "natural-outside-quota",
                "frame_rank": rank,
                "opening_title": row["title"],
                "issue_url": row["html"],
                "api_url": row["api"],
                "value_source": "author's GitHub opening Markdown API field",
                "opening_body_sha256": digest(body),
                "opening_bytes": len(body.encode("utf-8")),
                "created_utc": row["created"],
                "updated_utc": row["updated"],
                "retrieved_utc": row["retrieved_utc"],
                "revision_state": "first revision unverified",
                "request_spans": spans,
                "request": row["title"] + "\n" + "\n".join(decision["request"]),
                "author_target": decision["target"],
                "preserve": decision["preserve"],
                "versions": decision["edition"],
                "version_state": decision["edition_state"],
                "candidates": decision["candidates"],
                "still_unknown": decision["still_unknown"],
                "related_media": [
                    {"url": url, "kind": "visual output or external editor; not used as source bytes"}
                    for url in dict.fromkeys(re.findall(r"https?://[^\s)>\"\]]+", body))
                    if re.search(r"user-images\.githubusercontent|mermaid\.live|codepen\.io|vega\.github\.io/editor", url)
                ],
                "specs": [],
            }
            for i, spec in enumerate(specs, 1):
                ext = "mmd" if project == "M" else "jsonc" if spec["format"] == "vega-lite-partial" else "json"
                path = original / f"{id}-{i}.{ext}"
                path.write_bytes(spec["raw"].encode("utf-8"))
                case["specs"].append({
                    **{k: v for k, v in spec.items() if k != "raw"},
                    "file": path.relative_to(ROOT).as_posix(),
                    "source": row["html"],
                    "role": "main" if i == decision["main_spec"] else "author comparison example",
                })
            raw = specs[decision["main_spec"] - 1]["raw"]
            records, refs, parsed = (vega_records if project == "V" else mermaid_records)(raw)
            seeds = anchors(records, project, decision["seed_tokens"])
            case["seed_anchors"] = {"literal_cues": decision["seed_tokens"], "computed_paths": seeds,
                                   "method": "worker maps author prose to matching records", "parse": parsed}
            # URLs are evidence; scoring ships the common candidate menu and only the visible sample.
            all_cases.append(case)
            all_views.extend(views(case, records, refs, seeds, menu))
            graphs.append({"id": id, "records": [asdict(r) for r in records], "references": refs,
                           "start_candidates": seeds, "seed_cues": decision["seed_tokens"]})
    json_lines(ROOT / "cases.jsonl", all_cases)
    json_lines(ROOT / "views.jsonl", all_views)
    json_lines(ROOT / "evidence" / "opening-frame.jsonl", archive)
    json_lines(ROOT / "evidence" / "record-index.jsonl", graphs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("pages", type=Path)
    build(parser.parse_args().pages)
