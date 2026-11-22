"""Build short source evidence from already fetched public originals.

Run after fetching the URLs in sources.jsonl into raw/<source_id>.html.
The original response hash is preserved; short quotations avoid redistributing
entire third-party essays/catalogue interfaces. No network request is made here.
"""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.suppressed = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.suppressed += 1
        if tag in ("p", "div", "tr", "li", "h1", "h2", "h3", "h4", "br"):
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.suppressed = max(0, self.suppressed - 1)
        self.parts.append(" ")

    def handle_data(self, data):
        if not self.suppressed:
            self.parts.append(data)


def quotations_from_evidence():
    """The sealed evidence files are the quote manifest; do not duplicate quotations."""
    return {path.stem: [x["text"] for x in json.loads(path.read_text())["excerpts"]]
            for path in sorted((HERE / "extracts").glob("CX-*.json"))}



def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    target = HERE / "extracts"
    target.mkdir(exist_ok=True)
    results = []
    for source_id, quotations in quotations_from_evidence().items():
        raw_path = HERE / "raw" / (source_id + ".html")
        raw = raw_path.read_bytes()
        parser = Text()
        parser.feed(raw.decode("utf-8", errors="replace"))
        normalized = " ".join("".join(parser.parts).split())
        excerpts = []
        for text in quotations:
            begin = normalized.find(text)
            if begin < 0:
                raise ValueError(source_id + ": quotation not found: " + text)
            excerpts.append({"text": text, "normalized_character_start": begin,
                             "normalized_character_end": begin + len(text),
                             "utf8_bytes": len(text.encode()), "sha256": digest(text.encode())})
        word_count = sum(len(q.split()) for q in quotations)
        if word_count > 25:
            raise ValueError(source_id + ": more than 25 quoted words")
        evidence = {"source_id": source_id, "response_sha256": digest(raw),
                    "response_bytes": len(raw),
                    "normalization": "HTMLParser(convert_charrefs=True), ignore script/style, whitespace collapse; prepare_evidence.py Text",
                    "normalized_text_sha256": digest(normalized.encode()),
                    "excerpts": excerpts, "quoted_words": word_count,
                    "full_body_retained_in_deliverable": False}
        path = target / (source_id + ".json")
        path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        results.append({"source_id": source_id, "excerpt_file": path.name,
                        "excerpt_file_bytes": path.stat().st_size,
                        "excerpt_file_sha256": digest(path.read_bytes())})
    (HERE / "excerpt-receipt.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"source_evidence_files": len(results), "exact_quotation_checks": "passed"}))


if __name__ == "__main__":
    main()
