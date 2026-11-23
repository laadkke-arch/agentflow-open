"""Reopen retained bytes and validate the AF-RES-099 observations."""
from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree

from run import C_PDF, INPUTS, VIEWPORT, decode_data, digest, metadata, svg_probe

ROOT = Path(__file__).resolve().parent
MATRIX = ROOT / "evidence/matrix"
SOURCE_MINIMUMS = {"request": 2, "pandoc": 7, "tex": 7, "web": 4, "graphviz": 2, "jupyter": 2}
ID_ORDER = ("A1", "A2", "B1", "B2", "C1", "C2")
LOOPBACK = "127.0.0.1:8765"


class ImageSources(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.sources = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.sources.append(dict(attrs).get("src"))


def jsonfile(path):
    return json.loads(path.read_text())


def jsonlines(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def browser(case):
    value = jsonfile(MATRIX / case / "browser.json")
    assert value["opened"] and value["viewport"] == VIEWPORT
    assert not value["navigatorOnline"]
    assert all(urlsplit(url).netloc == LOOPBACK for url in value["outbound_requests"])
    return value


def img_sources(path):
    return ImageSources(path.read_text()).sources


def verify_slots(rows):
    primary = {r["id"]: r for r in rows if r["kind"] == "primary"}
    assert set(primary) == set(ID_ORDER)
    for row in primary.values():
        assert row["input_sha256"] == INPUTS["question"]["tex_sha256"]
        assert all(step["exit_code"] == 0 for step in row["processes"])
    result = {}
    for case in ID_ORDER:
        row = primary[case]
        tag = row["route"]
        folder = MATRIX / case
        dom = browser(case)
        data = {"body_searchable": dom["before_after_searchable"], "loaded_image_count": 0}
        if tag in {"A", "B"}:
            blocks = jsonfile(folder / "reader.json")["blocks"]
            data["AST"] = Counter(b["t"] for b in blocks)
            assert data["AST"]["CodeBlock"] == 0
            assert data["body_searchable"] == [True, True]
            urls = img_sources(folder / "example.html")
            if tag == "A":
                assert data["AST"]["RawBlock"] == 0 and not row["child_processes"]
                assert not urls and not dom["images"]
            if tag == "B":
                raw = [b["c"] for b in blocks if b["t"] == "RawBlock"]
                assert len(raw) == 2 and sum("tikzpicture" in block for _, block in raw) == 1
                assert [p["exit_code"] for p in row["child_processes"]] == [0, 0]
                assert [p["tool"] for p in row["child_processes"]] == ["pdflatex", "pdf2svg"]
                assert len(urls) == 1 and urls[0].startswith("data:image/svg+xml;base64,")
                original = next(folder.glob("af096-tikz-*.svg"))
                decoded = folder / "decoded.svg"
                assert decode_data(urls[0]) == original.read_bytes() == decoded.read_bytes()
                assert dom["images"][0]["width"] > 0
                assert dom["images"][0]["decoded_sha256"] == digest(original)
                assert dom["sequence"][0].startswith("The following")
                assert dom["sequence"][-1].startswith("The above")
                assert "<img>" in dom["sequence"]
                data["loaded_image_count"] = 1
                data["svg"] = svg_probe(decoded)
                assert data["svg"]["element_counts"]["use"] == 16
                assert not data["svg"]["text_elements"]
                assert data["svg"]["local_use_targets_resolved"]
        else:
            assert row["svg_pages"] == ["out1.svg"] and dom["root"] == "svg"
            assert not (folder / "example.html").exists()
            assert "The following" in jsonfile(folder / "pdf.json")["text"]
            data["svg"] = svg_probe(folder / "out1.svg")
            root = ElementTree.parse(folder / "out1.svg").getroot()
            assert data["svg"]["local_use_targets_resolved"]
            assert data["svg"]["data_text_count"] == 67 and not data["svg"]["text_elements"]
            data["data_text_concatenated"] = "".join(n.get("data-text", "") for n in root.iter())
            assert "q1q2q3q4abababba" in data["data_text_concatenated"]
            for style in ("EXTERNAL", "EMBED"):
                wrapper = browser(f"CPLUS-{style}-{row['repetition']}")
                assert wrapper["images"][0]["width"] > 0 and wrapper["before_after_searchable"] == [False, False]
                if style == "EMBED":
                    assert wrapper["images"][0]["decoded_sha256"] == digest(folder / "out1.svg")
        result[case] = data
    missing = browser("CPLUS-MISSING-1")
    assert missing["images"][0]["width"] == 0 and missing["served"][-1]["status"] == 404
    assert not browser("B-NOPIC")["images"]
    assert browser("B-ONLY-HTML")["images"][0]["width"] > 0
    return result


def repeat_hashes():
    groups = {
        "A": ["example.html", "reader.json", "browser.png"],
        "B": ["example.html", "reader.json", "decoded.svg", "events/0-diagram.pdf", "browser.png"],
        "C": ["out1.svg", C_PDF, "pdf-page.png", "browser.png"],
    }
    return {
        route: {
            name: {
                "first": digest(MATRIX / f"{route}1" / name),
                "second": digest(MATRIX / f"{route}2" / name),
                "equal": digest(MATRIX / f"{route}1" / name) == digest(MATRIX / f"{route}2" / name),
            }
            for name in files
        }
        for route, files in groups.items()
    }


def pdf_geometry():
    import fitz

    paths = [MATRIX / f"{case}{n}" / pdf for case, pdf in (("B", "events/0-diagram.pdf"), ("C", C_PDF))
             for n in (1, 2)]
    records, coordinates = {}, []
    for path in paths:
        with fitz.open(path) as doc:
            drawing = doc[0].get_drawings()
            begin = drawing[0]["rect"]
            bounds = [(d["type"], len(d["items"]), [x - begin[i % 2] for i, x in enumerate(d["rect"])])
                      for d in drawing]
            assert len(bounds) == 24
            coordinates.append(bounds)
            records[str(path.relative_to(ROOT))] = {
                "drawing_operations": len(drawing), "creation_date": doc.metadata["creationDate"],
                "first_ring_bounds_pt": list(begin), "page_size_pt": [doc[0].rect.width, doc[0].rect.height],
            }
    base = coordinates[0]
    maximum = 0
    for candidate in coordinates[1:]:
        for row, other in zip(base, candidate, strict=True):
            assert row[:2] == other[:2]
            maximum = max(maximum, *(abs(a - b) for a, b in zip(row[2], other[2], strict=True)))
    assert maximum < 0.01
    return {"comparison": "type and item count; relative PDF path bounding rectangles",
            "maximum_delta_pt": maximum, "files": records}


def main():
    rows = jsonlines(ROOT / "runs.jsonl")
    sources = jsonlines(ROOT / "sources.jsonl")
    assert len({x["id"] for x in rows}) == len(rows)
    assert len({x["id"] for x in sources}) == len(sources)
    n_present = 0
    for row in rows:
        for name, expected in row.get("artifacts", {}).items():
            path = ROOT / row["path"] / name
            if row.get("artifact_retention") and not path.exists():
                continue
            assert metadata(path) == expected, path
            n_present += 1
    counts = Counter(s["category"] for s in sources if s["count"])
    assert all(counts[category] >= n for category, n in SOURCE_MINIMUMS.items())
    distinct = [s["pinned_url"] for s in sources if s["count"]]
    assert len(set(distinct)) == len(distinct)
    print(json.dumps({
        "status": "pass", "run_rows": len(rows), "audited_artifacts": n_present,
        "source_rows": len(sources), "eligible_by_category": counts,
        "slots": verify_slots(rows), "repeat_hashes": repeat_hashes(), "pdf_geometry": pdf_geometry(),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
