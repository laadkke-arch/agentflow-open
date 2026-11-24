"""Materialize the study's input bytes without newline conversion."""
import argparse
import hashlib
import json
from pathlib import Path

ISSUES = {
    "C3": "https://github.com/wireservice/csvkit/issues/1194",
    "C4": "https://github.com/wireservice/csvkit/issues/1195",
    "Y2": "https://github.com/mikefarah/yq/issues/1501",
    "Y3": "https://github.com/mikefarah/yq/issues/1506",
    "Y4": "https://github.com/mikefarah/yq/issues/1513",
}
BODY = "author-body-example"
CONTROL = "researcher-control"
THIRD_PARTY = "third-party-reconstruction"
C3 = b'Software,Year\n"The ""best"" software",2023\n'
C4 = b'name,date\n"a","17/04/2023"\n'
Y3_BASE = b"values: |\n  abc\n"
Y4 = b"- b\n- c\n- d\n"


def blob(data):
    return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest(), "hex": data.hex()}


def catalog():
    rows = []

    def add(case, name, grade, source, basis, **files):
        rows.append({
            "case": case,
            "id": f"{case.lower()}-{name}",
            "grade": grade,
            "source_id": source,
            "source_url": ISSUES[case] + ("#issuecomment-1372294143" if source == "I-Y2-min" else ""),
            "basis": basis,
            "files": {name: blob(data) for name, data in sorted(files.items())},
        })

    add("C3", "public", BODY, "I-C3", "Author's printf specifies LF and terminal LF.", **{"test.csv": C3})
    add("C3", "special", CONTROL, "I-C3", "Interior tab, leading double quote, literal output escape X and output quote ~.",
        **{"test.csv": b'Software,Year\n"has\ttab",2023\n"""lead""",2024\n"X""embedded"" ~",2025\n'})
    add("C4", "public", BODY, "I-C4", "Code block spelling incl. quotes, LF chosen; original file unavailable.", **{"test.csv": C4})
    valid = C4 + b'"ambiguous","04/05/2023"\n"empty",""\n'
    add("C4", "valid-blank", CONTROL, "I-C4", "Public row plus ambiguous date and blank, reported format declared.",
        **{"test.csv": valid})
    add("C4", "mixed", CONTROL, "I-C4", "Valid/blank fixture plus impossible day, detects whole-column fallback.",
        **{"test.csv": valid + b'"invalid","31/02/2023"\n'})
    add("C4", "ambiguous-only", CONTROL, "I-C4", "Only a day/month ambiguous token, to isolate pattern and locale.",
        **{"test.csv": b'name,date\n"ambiguous","04/05/2023"\n'})

    for name, br in (("lf", b"\n"), ("cr", b"\r"), ("crlf", b"\r\n")):
        for count in (2, 3):
            add("Y2", f"{name}{count}", THIRD_PARTY if name == "lf" else CONTROL, "I-Y2-min",
                "Published cat shape and command; line-ending bytes unavailable." if name == "lf" else "Alternate bytes; cat transcript does not identify encoding.",
                **{"blank.yaml": br * count, "notempty.yaml": b"test:\n"})
    for name, value in (("zero", b""), ("null", b"null\n"), ("map", b"{}\n")):
        add("Y2", name, CONTROL, "I-Y2-min", "Same merge with distinct YAML input class.",
            **{"blank.yaml": value, "notempty.yaml": b"test:\n"})
    add("Y2", "nulls-in-map", CONTROL, "I-Y2-min", "Null within map is a different contract from a top-level null document.",
        **{"blank.yaml": b"test: keep\n", "notempty.yaml": b"test: null\n"})
    for ending, br in (("lf", b"\n"), ("crlf", b"\r\n")):
        for last in (False, True):
            payload = b'image:' + br + b'  tag: "0.0.1"' + (br if last else b"")
            add("Y3", f"{ending}-{'tail' if last else 'no-tail'}", CONTROL, "I-Y3",
                "Issue spelling; byte matrix inferred by researcher. Path 2.yaml follows command; 2.yml displayed in body.",
                **{"1.yml": Y3_BASE, "2.yaml": payload})
    add("Y4", "public", BODY, "I-Y4", "Array code block spelling, LF chosen, comparison version only.", **{"data1.yaml": Y4})
    add("Y4", "styled-flow", CONTROL, "I-Y4", "Compare syntax and comments on a flow array.",
        **{"data1.yaml": b"# sequence head\n['b', c, d] # sequence end\n"})
    add("Y4", "styled-block", CONTROL, "I-Y4", "Compare sequence comment and item-level style on a block array.",
        **{"data1.yaml": b"# sequence head\n- 'b' # first item\n- c\n- d\n"})
    return rows


def write_fixture(row, directory):
    directory.mkdir(parents=True, exist_ok=True)
    for name, metadata in row["files"].items():
        (directory / name).write_bytes(bytes.fromhex(metadata["hex"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--to", type=Path, help="Also generate a directory per fixture")
    options = parser.parse_args()
    for row in catalog():
        if options.to:
            write_fixture(row, options.to / row["id"])
        print(json.dumps(row, ensure_ascii=False, sort_keys=True))
