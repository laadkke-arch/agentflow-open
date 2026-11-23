"""Recreate AF-RES-064 display windows and the first eligible second action."""

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
import posixpath
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
WORD_LIMIT = 500
# Count punctuation independently so minified JSON does not become one token.
TOKEN = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def measure(text):
    tokens = TOKEN.findall(text)
    return {
        "words": len(tokens),
        "bytes": len(text.encode("utf-8")),
        "lines": len(text.splitlines()),
        "max_token_bytes": max((len(word.encode("utf-8")) for word in tokens), default=0),
        "sha256": sha256(text.encode("utf-8")),
    }


def budget(text, limit=WORD_LIMIT):
    for index, match in enumerate(TOKEN.finditer(text)):
        if index == limit:
            return text[:match.start()].rstrip(), True
    return text, False


def boundary_tests():
    fixtures = [(f"words_{n}", " ".join(["w"] * n), n) for n in (499, 500, 501, 611)]
    fixtures.extend([
        ("title_code_json_math", "제목\nlet x = 1;\n{\"a\":1}\n∑x² + y", 17),
        ("json_no_space", "[" + ",".join('{"key":1}' for _ in range(100)) + "]", 801),
        ("single_identifier", "한" * 8000, 1),
        ("line_ranges_and_nbsp", "line\r\n\r\nline\u00a0line", 3),
    ])
    outcomes = []
    for name, inp, size in fixtures:
        shown, cut = budget(inp)
        before = measure(inp)
        after = measure(shown)
        assert before["words"] == size, (name, before, size)
        assert after["words"] == min(size, WORD_LIMIT)
        assert cut == (size > WORD_LIMIT)
        assert inp.startswith(shown) and budget(shown) == (shown, False)
        outcomes.append({"fixture": name, "input": before, "shown": after, "truncated": cut})
    return outcomes


ELIGIBLE_LINK_WORDS = {"example", "examples", "test", "tests", "spec", "specs"}
BLOB_REF_PATH = re.compile(r"^/([^/]+/[^/]+)/(?:blob|tree|raw)/([^/]+)/(.+)$")
SOURCE_LINE = re.compile(r"^L\d+(?:-L\d+)?$")


def destination_url(point):
    from provider_text import urls

    page = urls(point["doc"])[0]
    frag = point["anchor"]
    if SOURCE_LINE.fullmatch(frag):
        page += "?plain=1"
    return page + ("#" + frag if frag else "")


def displayed(blocks, start):
    blocks = blocks[start:]
    whole = "\n".join(block.text for block in blocks)
    text, truncated = budget(whole)
    segments = []
    visible_links = []
    offset = 0
    for block in blocks:
        if offset >= len(text):
            break
        stop = min(offset + len(block.text), len(text))
        segments.append({"start": block.start, "end": block.end, "from": offset, "to": stop,
                         "partial": stop < offset + len(block.text)})
        visible_links.extend((link, block.start) for link in block.links if offset + link.end <= len(text))
        offset += len(block.text) + 1
    return text, truncated, segments, visible_links


def resolve_internal(doc, href):
    parts = urlsplit(href)
    path = unquote(parts.path)
    original_ref = doc["ref"]
    if parts.netloc:
        if parts.netloc.lower() != "github.com":
            return None
        github = BLOB_REF_PATH.fullmatch(path)
        if not github or github.group(1).lower() != doc["repo"].lower():
            return None
        original_ref, path = github.group(2, 3)
        if original_ref not in {doc["ref"], "main", "master"}:
            return None
    elif path and not path.startswith("/"):
        path = posixpath.normpath(posixpath.join(posixpath.dirname(doc["path"]), path))
    elif not path:
        path = doc["path"]
    else:
        return None
    if path.startswith("../") or not Path(path).suffix:
        return None
    return {**doc, "path": path}, unquote(parts.fragment), original_ref


def eligible_target(point, link):
    parts = urlsplit(link.href)
    target = resolve_internal(point["doc"], link.href)
    if not target:
        return None
    _, fragment, _ = target
    words = re.findall(r"[a-z]+", (link.label + " " + unquote(parts.path) + " " + fragment).lower())
    if not (set(words) & ELIGIBLE_LINK_WORDS):
        return None
    return target


def window_location(window):
    rows = window["source_segments"]
    if not rows:
        return ""
    return f"L{min(row['start'] for row in rows)}–L{max(row['end'] for row in rows)}"


def replay(plan, cache):
    from provider_text import read_blocks

    docs = {}
    unique = {}
    windows = []
    route_receipts = []
    summary = []

    def document(doc):
        key = (doc["repo"], doc["ref"], doc["path"])
        if key not in docs:
            docs[key] = read_blocks(doc, cache)
        return docs[key]

    def create_window(point):
        blocks, source = document(point["doc"])
        start = next(i for i, block in enumerate(blocks) if block.start == point["line"])
        target = destination_url(point)
        key = (source["raw_url"], point["line"])
        text, truncated, segments, links = displayed(blocks, start)
        if key not in unique:
            window = {
                "id": f"W{len(windows) + 1:02}", "start_line": point["line"],
                "source_segments": segments, **measure(text),
                "truncated": truncated, "source": source, "text": text, "route_actions": [],
            }
            windows.append(window)
            unique[key] = window
        return unique[key], target, links

    for pair in plan:
        result = {key: pair[key] for key in (
            "pair_id", "slot_id", "case_id", "catalog_id", "slot", "published_rank", "published_url",
            "feature_hits", "status", "origin_line", "selection", "other_status"
        )}
        result["provider_sha"] = pair["A"]["doc"]["ref"]
        row = {key: (json.dumps(value, ensure_ascii=False) if isinstance(value, list) else value)
               for key, value in result.items()}
        for view in ("A", "B", "P"):
            route = {"pair_id": pair["pair_id"], "view": view, "actions": [], "logical_raw_bytes": 0,
                     "status": "empty", "second_link": None, "strict_budget": False}
            result[view] = route
            point = pair[view]
            if point:
                shown, target, links = create_window(point)
                route["actions"].append({"action": 1, "url": target, "window": shown["id"],
                                         "source_lines": window_location(shown)})
                route["logical_raw_bytes"] += shown["source"]["raw_bytes"]
                shown["route_actions"].append({"pair_id": pair["pair_id"], "view": view, "action": 1})
                route["status"] = "read"
                for link, line in links:
                    destination = eligible_target(point, link)
                    if not destination:
                        continue
                    doc, fragment, original_ref = destination
                    if doc == point["doc"] and fragment == point["anchor"]:
                        continue
                    route["second_link"] = {"label": link.label, "href": link.href,
                                            "source_line": line, "original_ref": original_ref}
                    try:
                        blocks, source = document(doc)
                        marker = next((block for block in blocks if block.anchor and block.anchor == fragment), None) if fragment else blocks[0]
                        if not marker:
                            raise ValueError(f"Missing fragment {fragment}")
                        second = {"doc": doc, "line": marker.start, "anchor": fragment}
                        next_window, second_url, _ = create_window(second)
                        route["actions"].append({"action": 2, "url": second_url, "window": next_window["id"],
                                                  "source_lines": window_location(next_window)})
                        route["logical_raw_bytes"] += source["raw_bytes"]
                        next_window["route_actions"].append({"pair_id": pair["pair_id"], "view": view, "action": 2})
                    except (OSError, ValueError) as error:
                        route["actions"].append({"action": 2, "url": destination_url({"doc": doc, "anchor": fragment}),
                                                  "error": str(error)})
                        route["status"] = "second_unavailable"
                    break
                route["strict_budget"] = len(route["actions"]) <= 2 and all(
                    next(window["words"] for window in windows if window["id"] == action["window"]) <= WORD_LIMIT
                    for action in route["actions"] if "window" in action
                )
            route_receipts.append(route)
            for action in (1, 2):
                details = next((item for item in route["actions"] if item["action"] == action), {})
                win = next((item for item in windows if item["id"] == details.get("window")), {})
                for field in ("url", "source_lines", "window"):
                    row[f"{view}{action}_{field}"] = details.get(field, "")
                for field in ("words", "bytes"):
                    row[f"{view}{action}_{field}"] = win.get(field, "")
                row[f"{view}{action}_raw_bytes"] = win.get("source", {}).get("raw_bytes", "")
            row[f"{view}_second_label"] = (route["second_link"] or {}).get("label", "")
            row[f"{view}_status"] = route["status"]
            row[f"{view}_strict"] = route["strict_budget"]
            row[f"{view}_logical_raw_bytes"] = route["logical_raw_bytes"]
        summary.append(row)
    assert len(route_receipts) == len(plan) * 3
    return summary, windows, route_receipts, [source for _, source in docs.values()]


def write_output(root, rows, windows, routes, documents):
    root.mkdir(exist_ok=True, parents=True)
    (root / "evidence").mkdir(exist_ok=True)
    with (root / "routes.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    for name, records in (("windows.jsonl", windows), ("evidence/route-actions.jsonl", routes),
                          ("evidence/raw-retrieval.jsonl", documents)):
        (root / name).write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
                                         for row in records), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--selection", type=Path, default=HERE / "evidence/selection.json")
    parser.add_argument("--output", type=Path, default=HERE)
    parser.add_argument("--pair")
    parser.add_argument("--boundary", action="store_true")
    args = parser.parse_args()
    if args.boundary or not args.cache:
        print(json.dumps(boundary_tests(), indent=2, ensure_ascii=False))
    else:
        pair_plan = json.loads(args.selection.read_bytes())
        if args.pair:
            pair_plan = [row for row in pair_plan if row["pair_id"] == args.pair]
            if not pair_plan:
                parser.error(f"Unknown pair {args.pair}")
        results = replay(pair_plan, args.cache)
        write_output(args.output, *results)
        rows, windows, routes, sources = results
        print(json.dumps({"pairs": len(rows), "logical_routes": len(routes), "unique_display_windows": len(windows),
                          "logical_actions": sum(len(row["actions"]) for row in routes),
                          "physical_raw_documents": len(sources)}, ensure_ascii=False))
