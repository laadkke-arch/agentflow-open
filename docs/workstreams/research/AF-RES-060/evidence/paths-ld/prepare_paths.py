"""Prepare P1/P2/P3 from already acquired provider responses; no network calls.

Run only when the parent freezes the stage-3 case/provider plan. This program
does not inspect requirements, rank suppliers, or decide C1/C2. Its output is a
source/window/link plan for an independent subsequent direct-reading step.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import importlib.util
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

from lxml import html

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FEATURES = HERE.parent / "features-ld"
OWNED = HERE.parents[1]
F1_SHA = "412192e28356bee13e4c11f20511ab5ec590662c"
MODULE = importlib.util.spec_from_file_location("frozen_f1_renderer", FEATURES / "render_windows.py")
RENDERER = importlib.util.module_from_spec(MODULE)
assert MODULE.loader is not None
MODULE.loader.exec_module(RENDERER)
BLOCK = RENDERER.BLOCK


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def heading_slug(text: str) -> str:
    """ASCII GFM heading fragment, with conservative Unicode punctuation removal.

    Explicit HTML id/name always wins. A non-ASCII generated fragment is flagged
    in the plan for source-anchor verification; it is not silently exact-matched.
    """
    value = "".join(
        c for c in text.lower()
        if c in "-_ " or not unicodedata.category(c).startswith(("P", "S", "C"))
    )
    return value.replace(" ", "-")


def clean_document(raw: str, suffix: str):
    tree = html.fragment_fromstring(RENDERER.render(raw, suffix), create_parent="div")
    if suffix == ".html":
        areas = tree.xpath(".//main") or tree.xpath(".//article")
        if areas:
            tree = areas[0]
    # The provider README is already isolated from GitHub's repository chrome.
    # For HTML introductions, retain readable document text and remove UI chrome.
    for node in list(tree.xpath(
        ".//script|.//style|.//nav|.//footer|.//button|.//svg|"
        ".//*[@role='navigation']|.//*[@role='banner']|.//*[@role='contentinfo']"
    )):
        if node.getparent() is not None:
            node.drop_tree()
    for anchor in list(tree.xpath(".//a")):
        href = anchor.get("href", "")
        imgs = anchor.xpath(".//img")
        image_sources = " ".join(n.get("src", "") for n in imgs)
        label = " ".join(anchor.text_content().split())
        if (imgs and not label) or re.search(r"badge|shields\.io", href + " " + image_sources, re.I):
            anchor.drop_tree()
        elif label in {"#", "§"}:
            anchor.drop_tree()
    for node in list(tree.xpath(".//img")):
        if node.getparent() is not None:
            node.drop_tree()
    return tree


def visible_document(raw: str, suffix: str) -> dict:
    tree = clean_document(raw, suffix)
    parts, headings, anchors, ids = [], [], [], {}
    offset, slug_counts = 0, {}

    def add(text):
        nonlocal offset
        if text:
            parts.append(text)
            offset += len(text)

    def walk(node):
        tag = node.tag if isinstance(node.tag, str) else ""
        if not tag:
            return
        if tag in BLOCK:
            add("\n")
        start = offset
        for attribute in ("id", "name"):
            if node.get(attribute):
                ids[node.get(attribute)] = {"start": start, "type": "explicit_html_anchor"}
        if re.fullmatch(r"h[1-6]", tag):
            title = " ".join(node.text_content().split())
            slug = heading_slug(title)
            count = slug_counts.get(slug, 0)
            slug_counts[slug] = count + 1
            slug = slug if count == 0 else f"{slug}-{count}"
            heads = {"heading": title, "start": start, "slug": slug}
            headings.append(heads)
            if slug not in ids:
                ids[slug] = {
                    "start": start,
                    "type": "generated_ascii_heading" if title.isascii() else "generated_unicode_heading_needs_verification",
                }
        if node.text:
            add(node.text)
        for child in node:
            walk(child)
            if child.tail:
                add(child.tail)
        end = offset
        if tag == "a":
            anchors.append({
                "label": " ".join(node.text_content().split()),
                "href": node.get("href"),
                "start": start,
                "end": end,
            })
        if tag in BLOCK:
            add("\n")

    walk(tree)
    return {"text": "".join(parts), "headings": headings, "links": anchors, "ids": ids}


def first_window(raw: str, suffix: str, fragment: str = "") -> dict:
    doc = visible_document(raw, suffix)
    chosen = doc["headings"][0] if doc["headings"] else {"heading": "NO_HEADING_DOCUMENT_START", "start": 0}
    start = chosen["start"]
    anchor_status = "first_actual_heading"
    if fragment:
        anchor = doc["ids"].get(unquote(fragment))
        if not anchor or anchor["type"] == "generated_unicode_heading_needs_verification":
            return {
                "status": "fragment_unresolved_in_cache",
                "fragment": fragment,
                "text": "",
                "words": 0,
                "links": [],
                "reason": "Exact source anchor is required; no fallback to a more useful section.",
            }
        start = anchor["start"]
        chosen = {"heading": "fragment:" + fragment, "start": start}
        anchor_status = anchor["type"]
    words = list(re.finditer(r"\S+", doc["text"][start:]))
    end = start + (words[499].end() if len(words) >= 500 else len(doc["text"][start:]))
    text = doc["text"][start:end].strip()
    visible_links = []
    for link in doc["links"]:
        if link["start"] < end and link["end"] > start:
            item = dict(link)
            item["visible_label"] = " ".join(doc["text"][max(link["start"], start):min(link["end"], end)].split())
            item["window_word_position"] = len(doc["text"][start:max(start, link["start"])].split()) + 1
            visible_links.append(item)
    return {
        "status": "cached_window_ready_not_yet_case_judged",
        "heading": chosen["heading"],
        "anchor_status": anchor_status,
        "text": text,
        "words": len(text.split()),
        "links": visible_links,
        "window_sha256": sha256(text.encode()),
        "boundary": "first actual body heading or exact original fragment; at most 500 rendered whitespace words",
    }


def information_link(link: dict, base_url: str) -> dict:
    item = dict(link)
    href = item.get("href") or ""
    item["absolute_url"] = urljoin(base_url, href)
    parsed = urlsplit(item["absolute_url"])
    reason = None
    if not item.get("visible_label") or not href or href == "#":
        reason = "empty_text_or_non_destination"
    elif parsed.scheme not in {"http", "https"}:
        reason = "non_document_scheme"
    elif re.search(r"badge|shields\.io", item["absolute_url"], re.I):
        reason = "badge"
    elif re.search(r"^/(?:login|logout|signup|session|sessions)(?:/|$)", parsed.path, re.I):
        reason = "authentication_chrome"
    elif parsed.hostname in {"github.com", "www.github.com"} and re.fullmatch(
        r"/[^/]+/[^/]+/(?:actions|issues|pulls|discussions|stargazers|watchers|network|fork|forks)/?", parsed.path
    ):
        reason = "repository_activity_chrome"
    item["eligible"] = reason is None
    item["exclusion_reason"] = reason
    item["role_policy"] = (
        "Readable body link admitted by default; standards, install, usage, API, examples and internal fragments included. "
        "Destination content has not been opened to select this link."
    )
    return item


def acquisitions() -> dict:
    values = json.loads((FEATURES / "acquisition.json").read_text())
    values += [json.loads((FEATURES / f"{key}-crate-metadata.json").read_text()) for key in ("LD-020", "LD-021")]
    return {item["id"]: item for item in values}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ids", required=True, help="Frozen stage-3 provider IDs, comma separated; no ranking is computed")
    parser.add_argument("--stage3-sha", required=True)
    parser.add_argument("--output", default=str(HERE / "prepared-plan.json"))
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if not output.is_relative_to(HERE):
        raise SystemExit("Output must stay under evidence/paths-ld/")
    requested = set(args.ids.split(","))
    acq = acquisitions()
    with (OWNED / "inputs/af-res-056/catalog.csv").open() as stream:
        catalog = [row for row in csv.DictReader(stream) if row["catalog_id"] in requested]
    if {row["catalog_id"] for row in catalog} != requested:
        raise SystemExit("Unknown provider ID")
    rows = []
    window_dir = HERE / "first-windows"
    window_dir.mkdir(exist_ok=True)
    for row in catalog:
        key = row["catalog_id"]
        source = acq.get(key)
        result = {"catalog_id": key, "original_url": row["destination_url"], "paths": []}
        if not source or source.get("fetch_status") != "success":
            result.update({"status": "source_unavailable", "reason": "No successful frozen provider response; do not substitute another supplier or version."})
            rows.append(result)
            continue
        cache = Path(source["raw_file"])
        if not cache.is_absolute():
            cache = OWNED.parents[3] / cache
        payload = cache.read_bytes()
        fragment = urlsplit(row["destination_url"]).fragment
        window = first_window(payload.decode("utf-8"), cache.suffix, fragment)
        # For a README blob, relative links resolve against that immutable blob.
        # For a crate HTML response, record its acquired final URL as the base.
        base = source.get("final_url") or source["fixed_url"]
        audited, selected, seen = [], [], set()
        for candidate in window["links"]:
            item = information_link(candidate, base)
            if item["eligible"] and item["absolute_url"] in seen:
                item.update({"eligible": False, "exclusion_reason": "exact_url_duplicate"})
            if item["eligible"]:
                seen.add(item["absolute_url"])
                if len(selected) < 2:
                    selected.append(item)
                    item["selected_link_order"] = len(selected)
            audited.append(item)
        first_file = window_dir / f"{key}.txt"
        first_file.write_text(window.pop("text") + "\n")
        first_document = {
            "requested_url": row["destination_url"],
            "fixed_response_url": source["fixed_url"],
            "implementation_sha": source.get("sha"),
            "implementation_version": source.get("version"),
            "raw_sha256": sha256(payload),
            "window_file": str(first_file.relative_to(HERE)),
            "window": {k: v for k, v in window.items() if k != "links"},
            "status": "prepared_from_cache; direct_case_read_pending",
        }
        result.update({"status": window["status"], "link_base_url": base, "link_audit": audited})
        result["paths"].append({"path_id": "P1", "documents": [first_document]})
        for number in (1, 2):
            second = (
                {"requested_url": selected[number - 1]["absolute_url"], "selection": selected[number - 1], "status": "not_fetched_or_read", "max_window_words": 500}
                if len(selected) >= number
                else {"status": "no_eligible_information_link", "required_link_order": number}
            )
            result["paths"].append({"path_id": "P" + str(number + 1), "documents": [first_document, second], "independent_path": True})
        rows.append(result)
    receipt = {
        "prepared_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "f1_frozen_sha": F1_SHA,
        "stage3_frozen_sha": args.stage3_sha,
        "network_requests": 0,
        "judgments_made": 0,
        "supplier_conditions_read": False,
        "rule": "Original destination, same cached response, first actual heading/fragment, first and second eligible exact-URL-distinct body links",
        "rows": rows,
    }
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(output), "rows": len(rows), "network_requests": 0, "judgments_made": 0}))


if __name__ == "__main__":
    main()
