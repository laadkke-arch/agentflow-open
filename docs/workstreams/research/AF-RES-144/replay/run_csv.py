"""Run the pinned csvkit probes with byte receipts and consumer-side CSV/TSV reads."""
import csv
from datetime import datetime
import io
import re

from fixtures import catalog
from harness import Probe, options, runtime

DEFAULT_LOCALE = "C.UTF-8"
REPORTED_DATE_FORMAT = "%d/%m/%Y"


def read_csv(data, delimiter=",", **fmt):
    return list(csv.reader(io.StringIO(data.decode("utf8"), newline=""), delimiter=delimiter, strict=True, **fmt))


def tsv_split(data):
    return [line.split("\t") for line in data.decode("utf8").splitlines()]


def compare_csv(data, delimiter, input_rows, dialect):
    try:
        rows = read_csv(data, delimiter, **dialect)
    except (ValueError, csv.Error) as error:
        return {"error": str(error)}
    return {"rows": rows, "columns_per_record": [len(row) for row in rows], "equals_input_fields": rows == input_rows}


def formats(rows, opts):
    bin_dir, info = runtime(opts.installation, "csvkit", "1.0.7")
    variants = [
        ("default", [], ",", {}),
        ("tab-default", ["-T"], "\t", {}),
        ("no-double", ["-T", "-B"], "\t", {"doublequote": False}),
        ("escape-x", ["-T", "-B", "-P", "X"], "\t", {"doublequote": False, "escapechar": "X"}),
        ("escape-empty", ["-T", "-B", "-P", ""], "\t", {"doublequote": False}),
        ("quote-tilde", ["-T", "-Q", "~"], "\t", {"quotechar": "~"}),
        ("quote-crab", ["-T", "-Q", "🦀"], "\t", {"quotechar": "🦀"}),
        ("quote-tilde-no-double", ["-T", "-B", "-Q", "~"], "\t", {"quotechar": "~", "doublequote": False}),
        ("quote-empty", ["-u", "3", "-U", "3", "-Q", ""], ",", {"quoting": csv.QUOTE_NONE}),
    ]
    for fixture in rows:
        data = bytes.fromhex(fixture["files"]["test.csv"]["hex"])
        values = read_csv(data)
        for name, args, delimiter, dialect in variants:
            probe = Probe(fixture, name, "1.0.7", DEFAULT_LOCALE, opts.workspace, bin_dir, info)
            output, rc = probe.command("csvformat", *args, stdin=data)
            parsed = {"input_fields": values, "delimiter": delimiter, "declared_reader_dialect": dialect,
                      "reader": "separate CPython csv.reader (strict); bare TSV is split on tabs without quote or escape processing"}
            if rc == 0:
                parsed["declared"] = compare_csv(output, delimiter, values, dialect)
                if delimiter == "\t":
                    bare = tsv_split(output)
                    parsed["bare_tsv"] = {"rows": bare, "columns_per_record": [len(row) for row in bare], "equals_input_fields": bare == values}
                    parsed["default_quote_tsv"] = compare_csv(output, "\t", values, {})
            probe.finish(parsed)


def statistics(output):
    lines = output.decode().splitlines()
    start = next((i for i, line in enumerate(lines) if re.match(r'^\s*2\. "date"', line)), None)
    if start is None:
        return {}
    fields = [line.strip().split(":", 1) for line in lines[start + 1:] if ":" in line]
    return {k: v.strip() for k, v in fields}


def date_audit(data):
    values = []
    for label, field in read_csv(data)[1:]:
        if not field:
            values.append({"row_name": label, "value": field, "under_reported_pattern": None})
            continue
        try:
            inferred = datetime.strptime(field, REPORTED_DATE_FORMAT).date().isoformat()
            values.append({"row_name": label, "value": field, "under_reported_pattern": inferred})
        except ValueError as error:
            values.append({"row_name": label, "value": field, "error": str(error)})
    return values


def dates(rows, opts):
    for version in ("1.0.5", "1.1.0"):
        bin_dir, info = runtime(opts.installation, "csvkit", version)
        for fixture in rows:
            data = bytes.fromhex(fixture["files"]["test.csv"]["hex"])
            for variant in ("direct", "direct-date-flag", "pipe"):
                locale_matrix = (DEFAULT_LOCALE, "en_US.utf8", "en_GB.UTF-8") if fixture["id"].endswith("ambiguous-only") else (DEFAULT_LOCALE,)
                for locale in locale_matrix:
                    probe = Probe(fixture, variant, version, locale, opts.workspace, bin_dir, info)
                    parsed = {"pattern": REPORTED_DATE_FORMAT, "input_rows": read_csv(data),
                              "independent_row_audit": date_audit(data), "intermediate_fields": None}
                    if variant == "pipe":
                        middle, in2_rc = probe.command("in2csv", "test.csv", "--date-format", REPORTED_DATE_FORMAT)
                        if in2_rc == 0:
                            parsed["intermediate_fields"] = read_csv(middle)
                        # Feed the exact bytes, like a pipeline, and keep both exit codes.
                        stdout, rc = probe.command("csvstat", stdin=middle)
                    else:
                        args = ["-v", "test.csv"] if variant == "direct" else ["--date-format", REPORTED_DATE_FORMAT, "test.csv"]
                        stdout, rc = probe.command("csvstat", *args)
                    parsed["csvstat_date_column"] = statistics(stdout) if rc == 0 else None
                    probe.finish(parsed)


if __name__ == "__main__":
    opts = options(__doc__)
    fixtures = catalog()
    formats([row for row in fixtures if row["case"] == "C3"], opts)
    dates([row for row in fixtures if row["case"] == "C4"], opts)
