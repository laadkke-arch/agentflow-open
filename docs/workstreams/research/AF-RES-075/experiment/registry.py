"""Parser and decision model used by the capture and reader path."""
import ast
import csv
import fnmatch
import hashlib
import json
import posixpath
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAIMS = ("exists", "unique", "top")
VIEWS = ("A", "B", "C")
STATES = ("retained", "lost")
ENTRYPOINTS = {
    "PG": "https://github.com/pygments/pygments/blob/master/pygments/lexers/_mapping.py",
    "TZ": "https://data.iana.org/time-zones/tzdb/zone1970.tab",
}
RULE_IDS = {"PG": "pg-basename-v1", "TZ": "tz-membership-v1"}


def encode(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf8")


def write_jsonl(path, data):
    with path.open("wb") as stream:
        for row in data:
            stream.write(encode(row) + b"\n")


def write_csv(path, columns, data):
    with path.open("w", encoding="utf8", newline="") as stream:
        table = csv.DictWriter(stream, columns, lineterminator="\n")
        table.writeheader()
        table.writerows(data)


def parse(domain, raw):
    source = raw.decode("utf8")
    lines = source.splitlines()
    result = {}

    def record(row_id, key, line_number, extra):
        if row_id in result:
            raise ValueError(f"Duplicate candidate ID {row_id}")
        result[row_id] = {
            "key": list(key), "line": line_number, "clause": lines[line_number - 1],
            "fields": extra,
        }

    if domain == "PG":
        assignment, = ast.parse(source).body
        target, = assignment.targets
        if target.id != "LEXERS" or not isinstance(assignment.value, ast.Dict):
            raise ValueError("Expected one LEXERS dictionary")
        for node, value in zip(assignment.value.keys, assignment.value.values, strict=True):
            parts = ast.literal_eval(value)
            module, name, aliases, patterns, mimetypes = parts
            if node.lineno != value.end_lineno:
                raise ValueError("Registry row spans more than one line")
            record(ast.literal_eval(node), patterns, node.lineno, parts)
    elif domain == "TZ":
        for line_number, line in enumerate(lines, 1):
            if not line or line.startswith("#"):
                continue
            fields = line.split("\t")
            if len(fields) not in (3, 4):
                raise ValueError(f"Bad zone table row {line_number}")
            country, coordinates, row_id = fields[:3]
            codes = country.split(",")
            if any(not re.fullmatch(r"[A-Z]{2}", code) for code in codes):
                raise ValueError(f"Bad country token on line {line_number}")
            if len(codes) != len(set(codes)):
                raise ValueError(f"Duplicate country token on line {line_number}")
            record(row_id, codes, line_number, fields)
    else:
        raise ValueError(f"Unknown domain {domain}")
    return result


def check_rule(domain, rule):
    expected_names = {
        "id", "eligibility", "keys", "preferred", "other_eligible", "preference", "ties", "empty"
    }
    if (not isinstance(rule, dict) or set(rule) != expected_names
            or rule["id"] != RULE_IDS[domain]
            or rule["ties"] != "all IDs with maximal numeric score in Unicode code-point order"
            or rule["empty"] != []
            or type(rule["preferred"]) is not int
            or type(rule["other_eligible"]) is not int
            or rule["preferred"] <= rule["other_eligible"]):
        raise ValueError("missing or unrecognized historical rule")


def matched_key(domain, query, keys):
    if domain == "PG":
        basename = posixpath.basename(query)
        if not basename or "\0" in basename:
            raise ValueError("Expected a nonempty POSIX basename")
        matched = [key for key in keys if fnmatch.fnmatchcase(basename, key)]
        return sorted(matched, key=lambda key: (any(char in key for char in "*?["), key))
    if not re.fullmatch(r"[A-Z]{2}", query):
        raise ValueError("Expected a published-style country code")
    return [query] if query in keys else []


def inventory(rows):
    return [[row_id, rows[row_id]["key"]] for row_id in sorted(rows)]


def summarize(domain, query, keys, rule):
    check_rule(domain, rule)
    eligible = {}
    for row_id, key in keys:
        relevant = matched_key(domain, query, key)
        if relevant:
            if domain == "PG":
                preferred = not any(char in relevant[0] for char in "*?[")
            else:
                preferred = key[0] == query
            eligible[row_id] = rule["preferred"] if preferred else rule["other_eligible"]

    best = max(eligible.values(), default=None)
    winners = sorted(row_id for row_id, value in eligible.items() if value == best)
    return {
        "eligible": [[key, eligible[key]] for key in sorted(eligible)],
        "exists": bool(eligible), "unique": len(eligible) == 1, "top": winners,
        "boundary": {
            "scanned": len(keys), "eligible": len(eligible), "excluded": len(keys) - len(eligible),
            "max_score": best, "n_at_max": len(winners),
        },
    }


def receipt(rows, row_id):
    row = rows[row_id]
    return {"id": row_id, "line": row["line"], "clause_sha256": sha(row["clause"].encode())}
