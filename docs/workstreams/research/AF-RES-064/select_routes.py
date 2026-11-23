"""Use frozen feature origins plus provider metadata to select A/B/P starts."""

import argparse
import csv
import json
from pathlib import Path
import re

from provider_text import read_blocks, urls

HERE = Path(__file__).resolve().parent


def normalized(text):
    import unicodedata

    return re.sub(r"[^\w$]+", " ", unicodedata.normalize("NFKC", text).casefold()).strip()


def point(doc, block, label=None, anchor=None):
    marker = block.anchor if anchor is None else anchor
    return {"doc": doc, "line": block.start, "label": label if label is not None else block.text, "anchor": marker}


def neighboring_heading(blocks, start):
    headings = [block for block in blocks if block.level]
    if not headings:
        return None
    if start.level:
        pivot = start
    else:
        return next((block for block in headings if block.start > start.start), None)
    following = [block for block in headings if block.start > pivot.start and block.start != start.start]
    preceding = [block for block in headings if block.start < pivot.start and block.start != start.start]
    next_peer = next((block for block in following if block.level == pivot.level), None)
    previous_peer = next((block for block in reversed(preceding) if block.level == pivot.level), None)
    return next_peer or previous_peer or next(iter(following), None)


def choose(cache):
    docs = json.loads((HERE / "evidence/provider-documents.json").read_bytes())
    rules = json.loads((HERE / "evidence/anchor-rules.json").read_bytes())
    slots = list(csv.DictReader((HERE / "slots.csv").open(encoding="utf-8")))
    candidates = {}
    structure = []
    for root in docs:
        provider = root["id"]
        rule = rules[provider]
        blocks, receipt = read_blocks(root, cache)
        # The recorded origin must really contain the frozen feature words.
        title = json.loads(next(slot["feature_hits"] for slot in slots if slot["catalog_id"] == provider))[0]
        assert any(block.start <= rule["origin_line"] <= block.end and
                   normalized(title) in normalized(block.text) for block in blocks), provider
        a_start = blocks[0]
        first = rule.get("first")
        destination = {**root, "path": first.get("path", root["path"])} if first else root
        destination_blocks, destination_receipt = (read_blocks(destination, cache) if destination != root
                                                  else (blocks, receipt))
        b_start = next((block for block in destination_blocks if block.start == first["line"]), None) if first else a_start
        assert b_start is not None
        if first and first["anchor"].startswith("L"):
            assert first["label"].casefold() in b_start.text.casefold()
        elif first:
            assert b_start.anchor == first["anchor"] and normalized(b_start.text) == normalized(first["label"])
            if rule["selection_status"] == "exact_heading":
                assert normalized(b_start.text) == normalized(title)
        placebo = neighboring_heading(destination_blocks, b_start)
        candidates[provider] = {
            "A": point(root, a_start, label="Published document body start", anchor=""),
            "B": point(destination, b_start, label=first["label"], anchor=first["anchor"]) if first else point(
                root, a_start, label="Published document body start", anchor=""),
            "P": point(destination, placebo) if placebo else None,
            "status": rule["selection_status"], "selection": rule["selection"],
            "other_status": rule["other_status"], "origin_line": rule["origin_line"],
        }
        assert candidates[provider]["P"] != candidates[provider]["B"]
        if first is None:
            assert candidates[provider]["A"] == candidates[provider]["B"]
        for doc, content, source in [(root, blocks, receipt), (destination, destination_blocks, destination_receipt)]:
            if any(entry["fixed_url"] == urls(doc)[0] for entry in structure):
                continue
            markers = [{"label": b.text, "line": b.start, "anchor": b.anchor, "level": b.level} for b in content if b.level]
            links = [{"line": b.start, "label": l.label, "path": l.href} for b in content for l in b.links if l.label]
            structure.append({"fixed_url": urls(doc)[0], "headings": markers, "links": links,
                              "raw_bytes": source["raw_bytes"], "sha256": source["raw_sha256"]})

    out = []
    for slot in slots:
        candidate = slot["catalog_id"]
        if not candidate:
            continue
        out.append({
            "pair_id": f"{slot['case_id']}/{candidate}", "slot_id": slot["slot_id"],
            "case_id": slot["case_id"], "catalog_id": candidate, "slot": int(slot["slot"]),
            "published_rank": int(slot["posted_rank"]), "published_url": slot["published_url"],
            "feature_hits": json.loads(slot["feature_hits"]),
            **candidates[candidate],
        })
    assert len(out) == 11
    return out, structure


def write_json(path, rows):
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=HERE / "evidence")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    plan, metadata = choose(args.cache)
    write_json(args.output / "selection.json", plan)
    write_json(args.output / "selector-metadata.json", metadata)
    for row in plan:
        print(row["pair_id"], row["status"], *(f"{view}:{row[view]['line']}" if row[view] else f"{view}:empty"
                                               for view in ("A", "B", "P")))
