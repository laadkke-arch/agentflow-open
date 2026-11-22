"""Check frozen raw href coordinates with the interpreter's standalone HTML parser."""
import argparse
import collections
import csv
import gzip
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent.parent


class Anchors(HTMLParser):
    literal = re.compile(r"""(?:^|\s)href\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        href = dict(attrs).get("href")
        if tag == "a" and href is not None:
            match = self.literal.search(self.get_starttag_text())
            raw = next(value for value in match.groups() if value is not None) if match else None
            self.anchors.append((href, raw, self.getpos()[0]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", type=Path)
    args = parser.parse_args()
    receipts = {}
    for line in (ROOT / "captures.jsonl").read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        if item.get("fixed_asset"):
            receipts[item["acquisition_id"]] = item
    checks = collections.defaultdict(list)
    start = json.loads((ROOT / "evidence/matplotlib-start.json").read_text(encoding="utf-8"))
    checks["M48-pub"].extend(start)
    with gzip.open(ROOT / "evidence/M-screen.jsonl.gz", "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            checks[row["aid"]].extend(row.get("links", []))
    tested = 0
    anchors = 0
    for aid, rows in checks.items():
        item = receipts[aid]
        data = (args.raw_dir / f"{aid}.raw").read_bytes()
        assert hashlib.sha256(data).hexdigest() == item["response_sha256"]
        html = Anchors()
        html.feed(data.decode(item.get("charset") or "utf-8"))
        anchors += len(html.anchors)
        for row in rows:
            href, raw, line = html.anchors[row["dom_ordinal"] - 1]
            assert (href, raw, line) == (row["href"], row["raw_href"], row["html_line"]), (aid, row)
            assert urljoin(item["publication_url"], href.strip()) == row["url"], (aid, row)
            tested += 1
    print(json.dumps({"python": sys.version.split()[0], "parser": "stdlib HTMLParser",
                      "documents": len(checks), "all_href_positions": anchors,
                      "checked_selection_and_screen_rows": tested, "matched": tested}))


if __name__ == "__main__":
    main()
