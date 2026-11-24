"""Build a body-free replay projection with the pinned predecessor lexers."""

import argparse
import hashlib
import importlib.util
import json
import unicodedata
from pathlib import Path


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def read_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_predecessors(af122, af126):
    capture = read_module("af126_capture", af126 / "capture.py")
    prepare, legacy = capture.load_previous(af122)
    return prepare, legacy, capture


def body_projection(request_id, body, prepare, capture, cards, aliases, glossary):
    views, audits = prepare.prepare([{"request_id": request_id, "body": body}], cards, aliases)
    raw = unicodedata.normalize("NFC", body)
    view = next(view for view in views if view["view"] == "raw")
    runs, word_count = capture.sparse_runs(prepare, raw, glossary)
    extension = {"korean_retained_runs": runs, "korean_words": word_count}
    return {
        **view, **extension, "extended_projection_sha256": prepare.sha(prepare.packed(extension)),
        "original_sha256": audits[0]["original_sha256"], "normalized_codepoints": len(raw),
        "symbol_spans": [
            {name: span[name] for name in ("feature_id", "start", "end", "before")}
            for span in audits[0]["mask"]
        ],
    }


def project_requests(requests, openings, af122, af126):
    prepare, _, capture = load_predecessors(af122, af126)
    cards = prepare.read_csv(af122 / "catalog.csv")
    aliases = prepare.read_csv(af122 / "aliases.csv")
    glossary = capture.aliases_by_phrase(prepare, af122 / "aliases.csv")
    first = {(row["repository"].casefold(), row["issue_number"]): row for row in openings if row["access"] == "opening"}
    for request in requests:
        key = request["repository"].casefold(), request["issue_number"]
        row = first[key]
        body = row["body"]
        raw = unicodedata.normalize("NFC", body)
        if hashlib.sha256(raw.encode()).hexdigest() != request["nfc_sha256"]:
            raise ValueError(f"{request['request_id']}: first-body snapshot changed")
        for span in request["spans"]:
            start, end = span["start"], span["end"]
            if raw[start:end] != span["excerpt"] or prepare.sha(span["excerpt"]) != span["sha256"]:
                raise ValueError(f"{request['request_id']}: evidence span changed")
        yield body_projection(request["request_id"], body, prepare, capture, cards, aliases, glossary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", type=Path, required=True)
    parser.add_argument("--opening", type=Path, action="append", required=True)
    parser.add_argument("--af122", type=Path, required=True)
    parser.add_argument("--af126", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    requests = read_jsonl(args.requests)
    openings = [opening for path in args.opening for opening in read_jsonl(path)]
    rows = list(project_requests(requests, openings, args.af122, args.af126))
    with args.out.open("w", encoding="utf-8", newline="\n") as out:
        for row in rows:
            out.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"verified first-body and span fingerprints for {len(rows)} requests")


if __name__ == "__main__":
    main()
