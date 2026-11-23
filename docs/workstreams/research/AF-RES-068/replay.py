"""Replay fixed first actions and bounded second actions from public GitHub source."""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
from urllib.parse import quote, unquote, urlsplit
from urllib.request import Request, urlopen

from projection import Block, markdown_blocks, rst_blocks, source_blocks
from select_routes import ROOT, read_json, read_jsonl, route_points, write_json

TOKENS = re.compile(r"\w+|[^\w\s]", re.UNICODE)
LIMIT = 500
ELIGIBLE_SUFFIXES = {".md", ".markdown", ".rst", ".ts", ".js", ".json", ".mjs", ".cjs", ".ttl", ".txt"}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def utf8(text):
    return text.encode("utf-8")


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(x, ensure_ascii=False, separators=(",", ":")) + "\n" for x in rows),
                    encoding="utf-8")


def write_csv(path, rows):
    names = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", encoding="utf-8", newline="") as stream:
        w = csv.DictWriter(stream, fieldnames=names, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def source_urls(repo, ref, path, line=None, last=None):
    pinned = f"{repo}/{ref}/{quote(path, safe='/')}"
    html = f"https://github.com/{repo}/blob/{ref}/{quote(path, safe='/')}"
    if line is not None:
        html += f"?plain=1#L{line}" + (f"-L{last}" if last and last != line else "")
    return html, f"https://raw.githubusercontent.com/{pinned}"


def read_raw(cache, url):
    key = sha256(utf8(url))
    stored = cache / key
    meta = cache / (key + ".json")
    if stored.exists():
        data = stored.read_bytes()
        receipt = read_json(meta)
        if sha256(data) != receipt["sha256"]:
            raise ValueError(f"Bad cache checksum for {url}")
        return data, {**receipt, "cache_hit": True}
    request = Request(url, headers={"User-Agent": "AF-RES-068 fixed source study"})
    with urlopen(request, timeout=25) as response:
        data = response.read()
        receipt = {"input_url": url, "url": response.geturl(), "http": response.status,
                   "bytes": len(data), "sha256": sha256(data),
                   "utc": datetime.now(timezone.utc).strftime("%FT%TZ")}
    stored.write_bytes(data)
    write_json(meta, receipt)
    return data, {**receipt, "cache_hit": False}


def project(blocks, start):
    text_parts = []
    index = []
    references = []
    count = code_tokens = absolute = 0
    omitted = Counter()
    stop = False
    max_token = 0
    clipped = False
    for block in blocks:
        if block.first < start:
            continue
        matches = list(TOKENS.finditer(block.text))
        if count == LIMIT and matches:
            clipped = True
            break
        omitted["images"] += block.images
        omitted["math"] += block.math
        if not matches:
            if text_parts and block.kind == "code":
                text_parts.append("")
                absolute += 1
            continue
        taken = matches[:LIMIT - count]
        extent = taken[-1].end() if len(taken) < len(matches) else len(block.text)
        kept = block.text[:extent]
        if len(taken) < len(matches):
            stop = True
            clipped = True
        if text_parts:
            absolute += 1
        left = absolute
        absolute += len(kept)
        source_last = block.last
        if stop and block.kind == "text" and block.last > block.first:
            source_last = min(block.last, block.first + kept.count("\n"))
        index.append([block.first, source_last, block.kind, count + 1, count + len(taken)])
        for link in block.links:
            if link.end <= extent and link.label.strip():
                references.append({"label": link.label, "href": link.href, "line": block.first,
                                   "end_char": left + link.end})
        text_parts.append(kept)
        count += len(taken)
        if block.kind == "code":
            code_tokens += len(taken)
        max_token = max(max_token, *(len(utf8(m[0])) for m in taken))
        if stop:
            break
    text = "\n".join(text_parts)
    omitted = {"images": omitted["images"], "math": omitted["math"]}
    return {"tokens": count, "space_words": len(text.split()), "code_tokens": code_tokens,
            "display_bytes": len(utf8(text)), "max_token_bytes": max_token, "sha256": sha256(utf8(text)),
            "clipped": clipped, **omitted, "source_index": index}, text, references


def target_path(repo, ref, path, href):
    uri = urlsplit(href)
    if uri.netloc:
        if uri.netloc.lower() != "github.com":
            return None
        prefixes = (f"/{repo}/blob/{ref}/", f"/{repo}/tree/{ref}/")
        prefix = next((p for p in prefixes if uri.path.startswith(p)), None)
        if prefix is None:
            return None
        target = unquote(uri.path[len(prefix):])
    elif uri.scheme:
        return None
    elif not uri.path:
        target = path
    elif uri.path.startswith("/"):
        target = unquote(uri.path[1:])
    else:
        target = posixpath.normpath(posixpath.join(posixpath.dirname(path), unquote(uri.path)))
    if target.startswith(("../", "/")) or "\\" in target:
        return None
    if target.endswith(".html"):
        target = target[:-5] + ".md"
    if PurePosixPath(target).suffix.lower() not in ELIGIBLE_SUFFIXES:
        return None
    return target, unquote(uri.fragment)


def fragment_start(blocks, fragment, total_lines):
    if not fragment:
        return 1
    line = re.fullmatch(r"L(\d+)(?:-L\d+)?", fragment)
    if line:
        n = int(line[1])
        return n if 1 <= n <= total_lines else None
    fragment = fragment.removeprefix("user-content-")
    return next((b.first for b in blocks if b.anchor == fragment), None)


def boundary_checks():
    output = []
    for n in (499, 500, 501):
        source = " ".join(f"w{k}" for k in range(n))
        blocks = markdown_blocks(source)
        row, text, _ = project(blocks, 1)
        assert row["tokens"] == min(n, LIMIT) and row["clipped"] == (n > LIMIT)
        assert text.split() == source.split()[:LIMIT]
        output.append({"case": f"{n}_words", "before": n, **row})
    markdown = "# Heading\n\n```js\nconst x = [1,2];\n```\n\n![alt](image.png) Text $x+y$ [test](#missing)\n"
    rst = "Heading\n=======\n\n.. code-block:: js\n\n   const x = [1,2];\n\nAn example :math:`x+y`.\n\n.. image:: ignored.png\n"
    for name, blocks, source, line in [("md", markdown_blocks(markdown), markdown, 4),
                                        ("rst", rst_blocks(rst), rst, 6)]:
        row, text, links = project(blocks, 1)
        assert source.splitlines()[line - 1].strip() in text
        assert any(i[0] == line and i[2] == "code" for i in row["source_index"])
        assert row["code_tokens"] == len(TOKENS.findall(source.splitlines()[line - 1]))
        assert row["images"] == row["math"] == 1 and "x+y" not in text
        if name == "md":
            assert links[0]["href"] == "#missing" and fragment_start(blocks, "missing", 8) is None
            assert fragment_start(blocks, "heading", 8) == 1
        output.append({"case": name, "source": source, "projection": text, "links": links, **row})
    source = "가" * 8000
    row, text, _ = project([Block(source, 1, 1, "text")], 1)
    assert row["tokens"] == 1 and row["max_token_bytes"] == 24000 and text == source
    output.append({"case": "one_unspaced_24000_bytes", "source_rule": "U+AC00 repeated 8000", **row})
    source = "[" + ",".join("0" for _ in range(400)) + "]"
    row, text, _ = project([Block(source, 1, 1, "code")], 1)
    assert row["tokens"] == row["code_tokens"] == 500 and row["clipped"] and len(text) == 500
    output.append({"case": "punctuated_code", "before": len(TOKENS.findall(source)), **row})
    assert target_path("org/repo", "ref", "docs/api.md", "#missing") == ("docs/api.md", "missing")
    output.append({"case": "broken_anchor", "action_2": "BAD_ANCHOR", "retry": False,
                   "source": "md test link → missing anchor"})
    return output


def replay(points, metadata, rules, cache):
    documents, windows, action_rows, route_rows = {}, {}, [], []
    masked = {}

    def get_doc(point, path):
        ident = point["pin"], path
        if ident not in documents:
            html, raw = source_urls(point["repo"], point["pin"], path)
            try:
                data, receipt = read_raw(cache, raw)
                source = data.decode("utf-8-sig")
                block_list = source_blocks(path, source)
                documents[ident] = (block_list, {**receipt, "html": html, "path": path,
                                                "line_count": len(source.splitlines())})
            except (OSError, UnicodeError, ValueError) as error:
                documents[ident] = ([], {"html": html, "path": path, "input_url": raw, "error": str(error)})
        return documents[ident]

    def open_window(point, path, start):
        key = point["pin"], path, start
        blocks, doc = get_doc(point, path)
        if "error" in doc:
            return None, [], "UNAVAILABLE"
        if key not in windows:
            info, text, links = project(blocks, start)
            if not info["tokens"]:
                return None, [], "EMPTY"
            lo = min(x[0] for x in info["source_index"])
            hi = max(x[1] for x in info["source_index"])
            ident = sha256(utf8("AF-RES-068 coded v1|" + "|".join(map(str, key))))[:12]
            url, raw = source_urls(point["repo"], point["pin"], path, lo, hi)
            windows[key] = ({
                "window": "W" + ident, "repo": point["repo"], "pin": point["pin"], "path": path,
                "start": start, "source_url": url, "raw_url": raw, "line_first": lo, "line_last": hi,
                "raw_bytes": doc["bytes"], "raw_sha256": doc["sha256"], **info,
            }, links)
            # Masked output has only ordered body and its original line numbers. Hash IDs do not encode a route letter.
            masked["W" + ident] = text
        info, links = windows[key]
        return info, links, "READ"

    allowed_words = set(rules["second_action"]["allowed_label_words"])
    for point in points:
        p, start = point["path"], point.get("display_line", point["line"])
        index = metadata[point["pin"]]
        ident = point["case_id"] + "/" + point["route"]
        url, raw = source_urls(point["repo"], point["pin"], p, start)
        first, links, state = open_window(point, p, start)
        route = {**point, "route_key": ident, "first_url": url, "first_raw": raw, "first_state": state,
                 "first_window": first["window"] if first else "", "first_range":
                 f'{first["line_first"]}–{first["line_last"]}' if first else "", "actions": 1,
                 "second_state": "NO_LINK", "second_url": "", "second_window": "", "second_range": ""}
        action_rows.append({"route_key": ident, "action": 1, "url": url, "state": state,
                            "window": route["first_window"]})
        if state != "READ":
            route["second_state"] = "NOT_ATTEMPTED"
        for link in links:
            if not (set(re.findall(r"[A-Za-z]+", link["label"].lower())) & allowed_words):
                continue
            candidate = target_path(point["repo"], point["pin"], p, link["href"])
            if candidate is None:
                continue
            dst, frag = candidate
            raw_second, _ = source_urls(point["repo"], point["pin"], dst)
            if dst not in index["paths"]:
                outcome = "BAD_PATH"
                line = None
            else:
                blocks, doc = get_doc(point, dst)
                line = fragment_start(blocks, frag, doc.get("line_count", 0))
                outcome = "UNAVAILABLE" if "error" in doc else "BAD_ANCHOR" if line is None else "READ"
            if dst == p and line == start:
                continue
            route["actions"] += 1
            second = None
            if outcome == "READ":
                second, _, outcome = open_window(point, dst, line)
            target_url = source_urls(point["repo"], point["pin"], dst, line)[0] if line else (
                raw_second + ("#" + quote(frag, safe="-") if frag else ""))
            route.update(second_state=outcome, second_window=second["window"] if second else "",
                         second_url=target_url, second_range=f'{second["line_first"]}–{second["line_last"]}' if second else "",
                         second_label=link["label"], second_origin_line=link["line"], second_origin_href=link["href"])
            action_rows.append({"route_key": ident, "action": 2, "url": target_url, "state": outcome,
                                "window": route["second_window"], "first_window": route["first_window"], **link})
            break
        route["strict_model"] = state == "READ" and route["actions"] <= rules["display"]["max_actions"]
        route_rows.append(route)
    uses = Counter(x["window"] for x in action_rows if x["window"])
    final_windows = [{**item, "route_actions_using": uses[item["window"]]} for item, _ in windows.values()]
    for route in route_rows:
        own = next(r for r in route_rows if r["case_id"] == route["case_id"] and r["route"] == "A")
        route["same_first_as_A"] = route["first_url"] == own["first_url"]
        route["same_window_as_A"] = bool(route["first_window"]) and route["first_window"] == own["first_window"]
    final_windows.sort(key=lambda w: w["window"])
    return route_rows, final_windows, action_rows, [d for _, d in documents.values()], masked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case")
    parser.add_argument("--pair", choices=("AB", "BC", "AC"),
                        help="Select two of three routes, retaining A as the reference internally.")
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--boundary", action="store_true")
    parser.add_argument("--emit-text", action="store_true", help="Write temporary masked bodies for human reading.")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.boundary:
        rows = boundary_checks()
        write_json(args.output / "boundary.json", rows)
        print("boundary checks", len(rows))
        return
    if args.cache is None:
        parser.error("--cache is required for source replay")
    args.cache.mkdir(parents=True, exist_ok=True)
    metadata = read_json(ROOT / "evidence/selector-metadata.json")
    rules = read_json(ROOT / "rules.json")
    points = route_points(read_json(ROOT / "selector-cases.json"), read_jsonl(ROOT / "mentions.jsonl"), rules, metadata)
    if args.case:
        points = [p for p in points if p["case_id"] == args.case]
        if not points:
            parser.error(f"unknown case {args.case}")
    if args.pair:
        points = [p for p in points if p["route"] in set(args.pair + "A")]
    rows, windows, actions, docs, masked = replay(points, metadata, rules, args.cache)
    if args.pair:
        rows = [x for x in rows if x["route"] in args.pair]
        retained = {x["route_key"] for x in rows}
        actions = [x for x in actions if x["route_key"] in retained]
        use = Counter(x["window"] for x in actions if x["window"])
        windows = [{**w, "route_actions_using": use[w["window"]]} for w in windows if use[w["window"]]]
    write_csv(args.output / "routes.csv", rows)
    write_jsonl(args.output / "windows.jsonl", windows)
    write_jsonl(args.output / "actions.jsonl", actions)
    write_jsonl(args.output / "retrieval.jsonl", docs)
    if args.emit_text:
        write_jsonl(args.output / "masked-text.jsonl",
                    [{"window": w["window"], "text": masked[w["window"]]} for w in windows])
    print("paths", len(rows), "actions", len(actions), "unique windows", len(windows),
          "outcomes", dict(Counter((a["action"], a["state"]) for a in actions)))


if __name__ == "__main__":
    main()
