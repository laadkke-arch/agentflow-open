#!/usr/bin/env python3
"""Capture an official document for the AF-RES-033 donor-only corpus.

Raw content and full extracted text are local cache, not public-repo artifacts.
This utility does not choose sources or inspect recipient materials.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

from lxml import html


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract_html(raw: bytes, xpath: str | None) -> tuple[str, str, str]:
    tree = html.fromstring(raw)
    title = " ".join(tree.xpath("//title/text()"))
    if xpath:
        roots = tree.xpath(xpath)
        if not roots:
            raise ValueError(f"No nodes matched explicit XPath: {xpath}")
    else:
        for candidate in (
            "//main", "//*[@role='main']", "//*[@id='main-content']",
            "//*[@id='content']", "//article", "//body",
        ):
            roots = tree.xpath(candidate)
            if roots:
                xpath = candidate
                break
        else:
            roots = [tree]
            xpath = "/"
    pieces = []
    blocks = {
        "address", "blockquote", "br", "caption", "dd", "div", "dl", "dt",
        "figcaption", "figure", "h1", "h2", "h3", "h4", "h5", "h6", "hr",
        "li", "ol", "p", "pre", "section", "table", "td", "th", "tr", "ul",
    }
    for root in roots:
        for node in root.xpath(".//script|.//style|.//nav|.//header|.//footer|.//aside|.//noscript|.//svg|.//h1"):
            node.drop_tree()
        for node in root.iter():
            if node.tag in blocks:
                node.text = "\n" + re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", node.text or "")
                node.tail = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", node.tail or "") + "\n"
        pieces.append(root.text_content())
    lines = [re.sub(r"[^\S\n]+", " ", line).strip() for line in "\n".join(pieces).splitlines()]
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"
    return text, str(xpath), title


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--xpath")
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--timeout", type=int, default=45)
    args = ap.parse_args()
    base = Path(__file__).resolve().parent
    cache = base / "cache"
    cache.mkdir(exist_ok=True)
    when = dt.datetime.now(dt.timezone.utc).isoformat()
    record = {"document_id": args.id, "requested_url": args.url, "retrieved_at": when}
    request = urllib.request.Request(args.url, headers={"User-Agent": "Mozilla/5.0 (compatible; AF-RES-033 research capture)", "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.8"})
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            raw = response.read()
            record.update({"http_status": response.status, "final_url": response.url, "content_type": response.headers.get("Content-Type"), "last_modified_header": response.headers.get("Last-Modified"), "etag": response.headers.get("ETag")})
        pdf = raw.startswith(b"%PDF")
        raw_path = cache / f"{args.id}.{'pdf' if pdf else 'html'}"
        raw_path.write_bytes(raw)
        if pdf:
            text_path = cache / f"{args.id}.txt"
            subprocess.run(["pdftotext", "-layout", "-nopgbrk", str(raw_path), str(text_path)], check=True)
            body = text_path.read_text(encoding="utf-8")
            extraction = "pdftotext -layout -nopgbrk; whole document"
            title = None
        else:
            body, selected_xpath, title = extract_html(raw, args.xpath)
            extraction = f"lxml HTML visible text; XPath {selected_xpath}; omit h1 title/script/style/nav/header/footer/aside/noscript/svg; normalize whitespace"
        if args.start:
            if args.start not in body:
                raise ValueError(f"Start marker not present: {args.start!r}")
            body = body[body.index(args.start):]
            extraction += f"; start marker {args.start!r}"
        if args.end:
            if args.end not in body:
                raise ValueError(f"End marker not present: {args.end!r}")
            body = body[:body.index(args.end)]
            extraction += f"; stop before marker {args.end!r}"
        body = body.strip() + "\n"
        text_path = cache / f"{args.id}.txt"
        text_path.write_text(body, encoding="utf-8")
        record.update({"status": "captured", "raw_path": str(raw_path.relative_to(base)), "raw_sha256": sha256(raw), "text_path": str(text_path.relative_to(base)), "text_sha256": sha256(body.encode("utf-8")), "text_characters": len(body), "text_whitespace_words": len(body.split()), "html_title": title, "extraction": extraction})
    except Exception as exc:
        record.update({"status": "failed", "error_type": type(exc).__name__, "error": str(exc)})
    (cache / f"{args.id}.capture.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False))
    if record["status"] != "captured":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
