"""Probe CPython names and provide the same byte-preserving cases to probe.c."""

import argparse
import csv
from hashlib import sha256
import json
from pathlib import Path
import sys
import unicodedata
import zoneinfo


HERE = Path(__file__).resolve().parent
TZ_KEYS = ("US/Eastern", "America/New_York", "Asia/Calcutta", "Asia/Kolkata",
           "Invalid/AF_RES_240")


def emit(**record):
    print(json.dumps(record, ensure_ascii=True, sort_keys=True))


def require_versions():
    if (sys.implementation.name, sys.version_info[:3], unicodedata.unidata_version) != (
        "cpython", (3, 13, 0), "15.1.0"
    ):
        raise SystemExit(f"Wrong target: {sys.version}; UCD {unicodedata.unidata_version}")


def file_sha(path):
    with Path(path).open("rb") as f:
        return sha256(f.read()).hexdigest()


def cases(phase):
    filename = "inputs.csv" if phase == "main" else "controls.csv"
    with (HERE / filename).open(encoding="utf-8", newline="") as src:
        rows = list(csv.DictReader(src))
    if phase == "main":
        for row in rows:
            literal = row["literal"]
            if literal.encode("ascii").hex() != row["ascii_hex"]:
                raise ValueError(f"Input bytes differ: {row['input_id']}")
            if row["role"] != "placeholder":
                yield row["input_id"], row["code_point"], "lookup", literal
        for code in dict.fromkeys(row["code_point"] for row in rows):
            yield f"{code}-name", code, "name", ""
    else:
        for row in rows:
            yield row["input_id"], row["code_point"], row["operation"], row["literal"]


def probe_names(phase, repeat):
    emit(kind="metadata", phase=phase, repeat=repeat,
         sys_version=sys.version, implementation=sys.implementation.name,
         ucd=unicodedata.unidata_version, executable=sys.executable,
         executable_sha256=file_sha(sys.executable),
         module=unicodedata.__file__, module_sha256=file_sha(unicodedata.__file__))
    operations = {"lookup": (("lookup", unicodedata.lookup),),
                  "name": (("name", unicodedata.name),
                           ("name(None)", lambda c: unicodedata.name(c, None)))}
    for case_id, code, operation, literal in cases(phase):
        if operation not in operations:  # ICU-only buffer controls.
            continue
        arg = literal if operation == "lookup" else chr(int(code, 16))
        for choice, call in operations[operation]:
            record = {"kind": "call", "repeat": repeat, "input_id": case_id,
                      "code_point": code, "operation": operation, "choice": choice,
                      "input_ascii_hex": literal.encode("ascii").hex(),
                      "input": literal if operation == "lookup" else f"U+{code}"}
            try:
                value = call(arg)
            except (KeyError, ValueError) as exc:
                emit(**record, exception=type(exc).__name__, exception_repr=repr(exc))
            else:
                if operation == "lookup":
                    emit(**record, value=value, code_points=[ord(c) for c in value])
                else:
                    emit(**record, value=value)


def probe_zones(path):
    zoneinfo.reset_tzpath((str(path.resolve()),))
    emit(kind="metadata", tzpath=zoneinfo.TZPATH, sys_version=sys.version)
    for key in TZ_KEYS:
        try:
            zone = zoneinfo.ZoneInfo(key)
        except zoneinfo.ZoneInfoNotFoundError as exc:
            emit(kind="timezone", input=key, exception=type(exc).__name__,
                 exception_repr=repr(exc))
        else:
            emit(kind="timezone", input=key, key=zone.key, text=str(zone))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("main", "controls", "tz"))
    parser.add_argument("--repeat", required=False, choices=(1, 2), default=1, type=int)
    parser.add_argument("--emit-icu", action="store_true")
    parser.add_argument("--tzdir", type=Path)
    args = parser.parse_args()
    require_versions()
    if args.phase == "tz":
        if args.tzdir is None:
            parser.error("tz requires --tzdir")
        probe_zones(args.tzdir)
    elif args.emit_icu:
        for case in cases(args.phase):
            try:
                joined = "\t".join(case).encode("ascii")
            except UnicodeEncodeError as exc:
                raise ValueError(f"Case is not ASCII: {case[0]}") from exc
            if any(sep in case[-1] for sep in ("\t", "\r", "\n")):
                raise ValueError(f"Case contains a TSV delimiter: {case[0]}")
            sys.stdout.buffer.write(joined + b"\n")
    else:
        probe_names(args.phase, args.repeat)


if __name__ == "__main__":
    main()
