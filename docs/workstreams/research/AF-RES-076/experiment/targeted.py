"""Open preselected source anchors for a separate post hoc reading comparison."""
import argparse
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from search import MAX_BODY, MAX_DISPLAY_WORDS, clean_lines, read_jsonl, sha, write_jsonl

THUMB_TEST = (
    "https://raw.githubusercontent.com/python-pillow/Pillow/"
    "693df7b42c666f88c719f9973be0ad71607328e0/Tests/test_image_thumbnail.py"
)

TARGETS = [
    ("A-CP01-P01", "CP01", "P01", [(26, 41)], "F-CP01-L-cold-1",
     "Complete the first candidate's thumbnail example; it now names the API and gives general bounds, "
     "with a different size than the calibration fixture."),
    ("A-CP01-T01", "CP01", "T-01", [(24, 43)], None,
     "One original test section supplies the Python L raster, 256x128 input, 100x100 bound, 100x50 expected "
     "result, and exact method invocation. Both conditions are visible before any additional source."),
    ("A-CD01-D03", "CD01", "D03", [(185, 201), (218, 228)], "F-CD01-L-cold-1",
     "One original document exposes the read_csv skip and temporary table API, explicitly typed input, "
     "and a raw line marked CAST. This is the published representative example, not a replay of the same fixture."),
    ("A-CD02-D05", "CD02", "D05", [(11, 18), (48, 52)], "F-CD02-L-cold-1",
     "The sentence defines the result-column scope and the EXCLUDE snippet demonstrates a named column. "
     "Direct base-table readback remains in T-05."),
    ("A-NP03-X03", "NP03", "X03", [(1708, 1714)], "F-NP03-S-cold-3",
     "Column suppression applies to web conversion output. This is the donor scope and leaves the TIFF to JPEG "
     "serialization problem unresolved."),
]


def run(root):
    docs = {r["candidate_id"]: r for r in read_jsonl(root / "corpus.jsonl")}
    for reading, request, candidate, spans, compared, finding in TARGETS:
        url = THUMB_TEST if candidate == "T-01" else docs[candidate]["fetch_url"]
        when = datetime.now(timezone.utc).isoformat()
        start = time.monotonic()
        req = urllib.request.Request(url, headers={"Accept-Encoding": "identity",
                                                  "User-Agent": "AF-RES-076 targeted reading"})
        with urllib.request.urlopen(req, timeout=20) as response:
            data = response.read(MAX_BODY)
            result_url, response_code = response.geturl(), response.status
        digest = sha(data)
        if candidate in docs:
            assert digest == docs[candidate]["document_sha256"], candidate
        view = "\n".join(line for n, line in clean_lines(data, url)
                         if any(first <= n <= last for first, last in spans))
        assert len(view.split()) <= MAX_DISPLAY_WORDS
        yield {
            "id": reading, "request_id": request, "candidate_id": candidate, "compared_main_fetch": compared,
            "kind": "posthoc targeted window", "utc": when, "source_url": url, "arrival_url": result_url,
            "http_status": response_code, "http_calls": 1, "network_body_b": len(data),
            "body_sha256": digest, "source_lines": spans, "display_text": view,
            "display_words": len(view.split()), "display_bytes": len(view.encode()), "display_sha256": sha(view.encode()),
            "elapsed_ms": round((time.monotonic() - start) * 1000), "finding": finding,
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    write_jsonl(args.output, run(args.root))
