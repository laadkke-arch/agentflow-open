"""Compare actual PDF bytes, page geometry, and outline semantics for fixed pairs."""
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from receipt import write_json
from run import main_cases

DATE_TOKEN = re.compile(rb"(/(?:CreationDate|ModDate)\s*\(D:)[0-9]{14}(Z\))")
ID_TOKEN = re.compile(rb"(/ID\s*\[\s*<)[0-9A-Fa-f]{32}(>\s*<)[0-9A-Fa-f]{32}(>\s*\])")


def mask_pdf_bytes(raw):
    masked, dates = DATE_TOKEN.subn(rb"\g<1>00000000000000\g<2>", raw)
    masked, ids = ID_TOKEN.subn(
        rb"\g<1>00000000000000000000000000000000\g<2>00000000000000000000000000000000\g<3>", masked)
    if (dates, ids, len(masked)) != (2, 1, len(raw)):
        raise ValueError("The fixed PDF's two literal dates and paired ID were not found unambiguously")
    return masked


def pdf_geom(path):
    # Poppler adds volatile PDF Info metadata to XHTML's <head>.
    return [ET.tostring(page) for page in ET.parse(path).findall(".//{*}page")]


def read_cases(*roots):
    return {path.parent.name: (path.parent, json.loads(path.read_text()))
            for root in roots for path in root.glob("*/run.json")}


def main_pairs():
    for case in main_cases():
        if case.repeat == 1:
            yield ("independent_repeat", case.name, case.name[:-1] + "2")
    for version in ("2232", "23"):
        for toc in ("off", "on"):
            yield ("title_presence", f"v{version}-{toc}-none-r1", f"v{version}-{toc}-unique-r1")
    yield ("toc_switch", "v23-off-unique-r1", "v23-on-unique-r1")


def control_pairs():
    yield ("writer_only_with_new_template", "v23-on-unique-r1", "old-with-new-template")
    yield ("writer_only_with_old_template", "v2232-on-unique-r1", "new-with-old-template")
    yield ("new_template_only_old_writer", "v2232-on-unique-r1", "old-with-new-template")
    yield ("old_template_only_new_writer", "v23-on-unique-r1", "new-with-old-template")
    yield ("remove_contentsname_conditional", "v23-on-unique-r1", "new-without-conditional")
    yield ("default_value_override", "v23-on-none-r1", "new-default-title")
    yield ("hyperref_bookmarks_disabled", "v23-on-unique-r1", "new-no-bookmarks")
    yield ("tex_explicit_bookmark", "v23-on-unique-r1", "new-explicit-toc-bookmark")
    yield ("toc_depth_one", "v23-on-unique-r1", "new-depth-one")
    yield ("same_pinned_epoch_repeat", "new-epoch-a-r1", "new-epoch-a-r2")
    yield ("different_pinned_epoch", "new-epoch-a-r1", "new-epoch-b")


def strip_object_refs(rows):
    return [{key: value for key, value in row.items()
             if key not in {"object", "parent_object", "page_object"}}
            | {"target": {k: v for k, v in row["target"].items() if k != "page_object"}}
            for row in rows]


def compare(name, left, right, cases):
    folder_a, a = cases[left]
    folder_b, b = cases[right]
    a3, b3 = a["passes"][-1], b["passes"][-1]
    pdf_a, pdf_b = (folder_a / "case.pdf").read_bytes(), (folder_b / "case.pdf").read_bytes()
    masked_a, masked_b = mask_pdf_bytes(pdf_a), mask_pdf_bytes(pdf_b)
    return {
        "comparison": name, "left": left, "right": right,
        "ast_bytes_equal": a["ast_sha256"] == b["ast_sha256"],
        "tex_bytes_equal": a["tex_sha256"] == b["tex_sha256"],
        "pdf_bytes_equal": pdf_a == pdf_b,
        "pdf_bytes_equal_after_masking_only_literal_dates_and_trailer_id": masked_a == masked_b,
        "masked_sha256": [hashlib.sha256(data).hexdigest() for data in (masked_a, masked_b)],
        "date": [run["pdf_metadata"]["/CreationDate"] for run in (a3, b3)],
        "ids_hex": [run["pdf_ids_hex"] for run in (a3, b3)],
        "pdftotext_layout_equal": a3["pages_text_sha256"] == b3["pages_text_sha256"],
        "bbox_entire_xhtml_equal": a3["bounding_boxes_sha256"] == b3["bounding_boxes_sha256"],
        "bbox_pages_only_equal": pdf_geom(folder_a / "bbox.html") == pdf_geom(folder_b / "bbox.html"),
        "raster96_equal": a3["png_96dpi_sha256"] == b3["png_96dpi_sha256"],
        "outline_title_parent_target_equal": strip_object_refs(a3["outline"]) == strip_object_refs(b3["outline"]),
        "outline_states": [run["outline_agreement"]["root_state"] for run in (a3, b3)],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--controls", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cases = read_cases(args.matrix, args.controls)
    pairs = list(main_pairs()) + list(control_pairs())
    write_json(args.output, [compare(name, a, b, cases) for name, a, b in pairs])
