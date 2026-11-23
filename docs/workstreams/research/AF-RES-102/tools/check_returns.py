#!/usr/bin/env python3
"""Check reader-facing versioned HTML destinations after prediction sealing.

These mirrors are not counted as new primary works. Does not execute a browser,
example code, or request the image bytes a second time.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    ("MP-G1", "demo_imagegrid_aspect", "setting-a-fixed-aspect-on-imagegrid-cells"),
    ("MP-G2", "demo_colorbar_with_axes_divider", "colorbar-with-axesdivider"),
    ("MP-C1", "demo_axes_hbox_divider", "hboxdivider-and-vboxdivider-demo"),
    ("MP-C2", "inset_locator_demo", "inset-locator-demo"),
]


def utc():
    return datetime.now(timezone.utc).isoformat()


class SectionParser(HTMLParser):
    def __init__(self, fragment):
        super().__init__()
        self.fragment = fragment
        self.depth = 0
        self.found = False
        self.images = []
        self.text = []
        self.start_line = None
        self.end_line = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("id") == self.fragment:
            self.found = True
            self.depth = 1
            self.start_line = self.getpos()[0]
        elif tag == "section" and self.depth:
            self.depth += 1
        if self.depth and tag == "img":
            self.images.append({"line": self.getpos()[0], "attributes": attrs})

    def handle_endtag(self, tag):
        if tag == "section" and self.depth:
            self.depth -= 1
            if self.depth == 0:
                self.end_line = self.getpos()[0]

    def handle_data(self, data):
        if self.depth:
            self.text.append(data)


def read_case(case):
    case_id, name, fragment = case
    url = f"https://matplotlib.org/3.7.0/gallery/axes_grid1/{name}.html"
    row = {"case_id": case_id, "original_url": url + "#" + fragment, "started_utc": utc(),
           "countable": False, "duplicate_reason": "Reader-facing mirror of the same pinned main example body"}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "AF-RES-102-return-url-audit"}), timeout=45) as r:
            b = r.read()
            row.update(status=r.status, final_url=r.geturl(), mime=r.headers.get("Content-Type"), bytes=len(b))
        parser = SectionParser(fragment)
        parser.feed(b.decode("utf-8"))
        expected = f"../../_images/sphx_glr_{name}_001.png"
        row.update(sha256=hashlib.sha256(b).hexdigest(), fragment=fragment,
                   fragment_present=parser.found, section_lines=[parser.start_line, parser.end_line],
                   images=parser.images, section_text_sha256=hashlib.sha256(" ".join(" ".join(parser.text).split()).encode()).hexdigest(),
                   first_reference_expected=expected,
                   first_reference_matches=bool(parser.images and parser.images[0]["attributes"].get("src") == expected))
        raw = json.loads((ROOT / "evidence/matplotlib/main-audit-raw.json").read_text())
        pinned = next(x for x in raw["records"] if x["case_id"] == case_id and x["edition"] == "new")
        row.update(fixed_source_url=pinned["body_url"], fixed_source_sha256=pinned["body_sha256"],
                   matches_pinned_body_bytes=row["sha256"] == pinned["body_sha256"])
        row["ok"] = (row["status"] == 200 and row["final_url"] == url and parser.found
                     and row["first_reference_matches"] and row["matches_pinned_body_bytes"])
    except Exception as exc:
        row.update(ok=False, error_type=type(exc).__name__, error=str(exc))
    row["finished_utc"] = utc()
    return row


def main():
    started = utc()
    with ThreadPoolExecutor(max_workers=4) as p:
        rows = list(p.map(read_case, CASES))
    output = {"started_utc": started, "finished_utc": utc(), "prediction_seal": "f1c5d6ff927fd5fbe108565598810ca7e94c5753",
              "scope": "Four rendered versioned reader URLs, exact fragments, primary image references and equality to pinned official publication HTML; no image refetch or JS/example execution",
              "records": rows, "passed": sum(r["ok"] for r in rows), "requested": len(rows)}
    (ROOT / "evidence/return-url-checks.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(r["ok"] for r in rows) else 1)


if __name__ == "__main__":
    main()
