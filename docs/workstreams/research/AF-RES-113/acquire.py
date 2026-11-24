"""Public text acquisition, deterministic exposure extraction, and receipts.

Run with python -B. No authentication, installation, or project execution.
Raw fetched material is a disposable ignored cache. Persist only receipts,
hashes, source locations, and the researcher's original analysis.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.request
from urllib.parse import urljoin

from lxml import html

ROOT = Path(__file__).resolve().parent


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        super().__init__()
        self.steps = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.steps.append({"from": req.full_url, "status": code, "to": newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, source_id, cache=True):
    redirects = Redirects()
    opener = urllib.request.build_opener(redirects)
    begin = time.monotonic()
    rec = {"source_id": source_id, "requested_url": url, "opened_at": now(),
           "actor": "root_acquisition", "explicit_open": 1, "redirects": redirects.steps,
           "money": "unobserved", "tokens": "unobserved"}
    raw = b""
    try:
        with opener.open(urllib.request.Request(url, headers={"User-Agent": "AF-RES-113 public research"}), timeout=35) as r:
            raw = r.read()
            rec.update({"status": r.status, "actual_url": r.url,
                        "content_type": r.headers.get("Content-Type", ""),
                        "last_modified": r.headers.get("Last-Modified"),
                        "etag": r.headers.get("ETag"), "success": True})
    except Exception as e:
        rec.update({"success": False, "error": type(e).__name__ + ": " + str(e),
                    "actual_url": getattr(e, "url", url), "status": getattr(e, "code", None)})
    rec.update({"closed_at": now(), "elapsed_seconds": round(time.monotonic()-begin, 6),
                "byte_count": len(raw), "sha256": digest(raw)})
    if cache:
        d = ROOT / "evidence/cache"
        d.mkdir(parents=True, exist_ok=True)
        (d / (source_id + ".raw")).write_bytes(raw)
        (d / (source_id + ".fetch.json")).write_text(json.dumps(rec, ensure_ascii=False, indent=2)+"\n")
    return raw, rec


def node_text(node):
    """DOM text order, strip each text fragment, join nonempty fragments by LF.

    White space inside a fragment collapses to one space. Headerlink widgets,
    scripts, styles, nav/footer and hidden nodes are removed, never reordered.
    """
    node = copy.deepcopy(node)
    for x in node.xpath('.//script|.//style|.//nav|.//footer|.//*[@hidden]|.//*[contains(concat(" ",normalize-space(@class)," ")," headerlink ")]'):
        x.drop_tree()
    fragments = []
    for x in node.itertext():
        s = re.sub(r"\s+", " ", x).strip()
        if s:
            fragments.append(s)
    return "\n".join(fragments)


def parse(raw, url, symbol=None):
    doc = html.fromstring(raw, base_url=url, parser=html.HTMLParser(encoding="utf-8", huge_tree=True))
    if symbol:
        nodes = doc.xpath('//*[@id=$symbol]', symbol=symbol)
        if not nodes:
            raise ValueError("symbol anchor absent: " + symbol)
        n = nodes[0]
        if n.tag == "dt" and n.getparent().tag == "dl":
            node = n.getparent()
        else:
            node = n
    else:
        nodes = doc.xpath('//article[@role="main"]|//main|//*[@role="main"]')
        if not nodes:
            nodes = doc.xpath('//article')
        node = nodes[0] if nodes else doc
    txt = node_text(node)
    links = [{"order": i+1, "label": " ".join(a.itertext()).strip(),
              "href": a.get("href"), "url": urljoin(url, a.get("href")),
              "ancestor_heading": ""}
             for i, a in enumerate(node.xpath('.//a[@href]'))]
    title = doc.xpath('string(//title)')
    return {"title": title, "symbol": symbol, "text": txt,
            "codepoints": len(txt), "text_sha256": digest(txt.encode()), "links": links}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_id")
    ap.add_argument("url")
    ap.add_argument("--symbol")
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    raw, receipt = fetch(a.url, a.source_id)
    if receipt["success"] and "html" in receipt["content_type"]:
        parsed = parse(raw, receipt["actual_url"], a.symbol)
        if a.limit is not None:
            parsed["text"] = parsed["text"][:a.limit]
            parsed["codepoints"] = len(parsed["text"])
            parsed["text_sha256"] = digest(parsed["text"].encode())
        (ROOT/"evidence/cache"/(a.source_id+".text.json")).write_text(json.dumps(parsed, ensure_ascii=False, indent=2)+"\n")
        print(json.dumps({"receipt": receipt, "parsed": parsed}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
