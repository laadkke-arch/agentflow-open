"""Compare the entire sealed UCD data row and its argument bytes, excluding LF."""

import csv
import hashlib
from pathlib import Path
import sys


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


directory = Path(sys.argv[1])
inputs = Path(sys.argv[2])
with inputs.open(newline="", encoding="utf-8") as f:
    template = list(csv.DictReader(f))
writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
writer.writerow(["ucd_version", "source_id", "line", "input_id", "ascii_hex",
                 "raw_row_sha256", "file_sha256", "byte_equal", "alias_kind"])
for version, alias_id, name_id in (("15.1.0", "U03", "U04"),
                                   ("16.0.0", "U01", "U02")):
    selected = set(row["code_point"].encode() for row in template)
    for source_id, alias in ((alias_id, True), (name_id, False)):
        raw_file = (directory / f"{source_id}-archive").read_bytes()
        corpus = {}
        for i, raw in enumerate(raw_file.splitlines(), 1):
            fields = raw.split(b";")
            if fields[0] in selected:
                corpus[(fields[0], fields[1] if alias else b"")] = (i, raw)
        rows = [row for row in template if (row["role"] == "alias") == alias]
        if len(rows) != len(corpus):
            raise SystemExit(f"{source_id}: sample row count mismatch {len(rows)} vs {len(corpus)}")
        for row in rows:
            literal = row["literal"].encode("ascii")
            cp_key = row["code_point"].encode("ascii")
            i, raw = corpus[cp_key, literal if alias else b""]
            same = (raw == row["basis_original_row"].encode("ascii")
                    and raw.split(b";")[1] == literal and literal.hex() == row["ascii_hex"])
            writer.writerow([version, source_id, i, row["input_id"], literal.hex(),
                             digest(raw), digest(raw_file), int(same), row["alias_type"] or "field1"])
            if not same:
                raise SystemExit(f"{source_id}:{i} row or input differs for {row['input_id']}")
