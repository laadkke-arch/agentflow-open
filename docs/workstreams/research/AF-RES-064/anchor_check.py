"""Verify frozen first-navigation GitHub fragment IDs without printing page text."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.request import Request, urlopen

from provider_text import urls

HERE = Path(__file__).resolve().parent


class IDs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        anchor = dict(attrs).get("id")
        if anchor:
            self.ids.add(anchor)


def verify(target):
    url, anchors = target
    receipt = {"url": url, "utc": datetime.now(timezone.utc).isoformat()}
    try:
        with urlopen(Request(url, headers={"User-Agent": "AF-RES-064 anchor check"}), timeout=20) as response:
            data = response.read()
            receipt.update(final_url=response.geturl(), raw_bytes=len(data), status=response.status)
        parser = IDs()
        parser.feed(data.decode("utf-8", errors="replace"))
        receipt["fragments"] = {
            anchor: anchor if anchor in parser.ids else "user-content-" + anchor
            if "user-content-" + anchor in parser.ids else None
            for anchor in sorted(anchors)
        }
    except (OSError, ValueError) as error:
        receipt.update(error=str(error), fragments={anchor: None for anchor in sorted(anchors)})
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, default=HERE / "evidence/selection.json")
    args = parser.parse_args()
    plan = json.loads(args.selection.read_bytes())
    targets = {}
    for pair in plan:
        for view in ("B", "P"):
            point = pair[view]
            if point and point["anchor"]:
                url = urls(point["doc"])[0]
                if point["anchor"][0] == "L" and point["anchor"][1:].isdigit():
                    url += "?plain=1"
                targets.setdefault(url, set()).add(point["anchor"])
    with ThreadPoolExecutor(max_workers=10) as workers:
        receipts = list(workers.map(verify, targets.items()))
    print(json.dumps(receipts, ensure_ascii=False, indent=2))
