"""Read the SQLite CLI exchange format and publish typed JSONL in one replace."""

import argparse
import csv
import json
import os
from pathlib import Path
import sys


def unwrap(value):
    if value == "N":
        return None
    if value.startswith("T"):
        return bytes.fromhex(value[1:]).decode("utf-8")
    raise ValueError("Expected typed N or T-prefixed hexadecimal TEXT")


def convert(source, target, mode, pause):
    quoting = csv.QUOTE_NOTNULL if mode == "notnull" else csv.QUOTE_MINIMAL
    partial = target.with_suffix(".part")
    with source.open(encoding="utf-8", newline="") as stream, partial.open("w", encoding="utf-8") as out:
        rows = csv.reader(stream, quoting=quoting, strict=True)
        if next(rows, None) != ["row_key", "cell"]:
            raise ValueError("Missing or mismatched CSV heading")
        for index, (row_key, value) in enumerate(rows):
            if mode == "typed":
                value = unwrap(value)
            row = {"key": row_key, "value": value}
            out.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            if pause and index == 0:
                out.flush()
                os.fsync(out.fileno())
                print("checkpoint: first row fsynced", flush=True)
                if not sys.stdin.readline():
                    raise RuntimeError("Checkpoint released without a resume token")
        out.flush()
        os.fsync(out.fileno())
    os.replace(partial, target)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", type=Path)
    p.add_argument("target", type=Path)
    p.add_argument("mode", choices=("excel", "notnull", "typed"))
    p.add_argument("--pause", action="store_true")
    args = p.parse_args()
    convert(args.source, args.target, args.mode, args.pause)


if __name__ == "__main__":
    main()
