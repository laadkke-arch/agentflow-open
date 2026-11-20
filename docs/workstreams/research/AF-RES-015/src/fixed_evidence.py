"""Verify selected public tags and method sources with short, identified reading windows."""

import argparse
import hashlib
import json
import re

from collect import ROOT, Reader


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resume", action="store_true")
    mode = parser.parse_args().resume
    reader = Reader(1.06)
    path = ROOT / "results" / "fixed-evidence.jsonl"
    existing = {json.loads(l)["id"] for l in path.read_text().splitlines()} if mode else set()
    with path.open("a" if mode else "w", encoding="utf-8", buffering=1) as out:
        for text in (ROOT / "data" / "fixed-evidence-specs.txt").read_text().splitlines():
            if not text or text.startswith("#"):
                continue
            source, url, expression, title, finding = text.split("|", 4)
            if source in existing:
                continue
            info, body = reader.get(url)
            match = re.search(expression, body, re.IGNORECASE)
            record = {"id": source, "title": title, "pattern": expression,
                      "line": body.count("\n", 0, match.start()) + 1 if match else None,
                      "sha256_text": hashlib.sha256(body.encode()).hexdigest() if body else None,
                      "confirmed": finding if match else None, **info}
            if match:
                # Print header-free matching words to inspect the precise content in the session.
                start = body.rfind("\n", 0, match.start()) + 1
                end = body.find("\n", match.end())
                print(source, record["line"], body[start:end][:155], flush=True)
            else:
                print(source, info["http"], "no signature", flush=True)
            out.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
