#!/usr/bin/env python3
"""Read local release trees and produce input-only candidate previews."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re

SQL = {
    "S1": (("null",), r"(?:<>|!=|==|(?<![<>!=])=(?!=))"),
    "S2": (("func", "sum"), r"\b(?:sum|total)\s*\("),
    "S3": (("select1", "sort"), r"\border\s+by\b"),
    "S4": (("window1", "window2"), r"\b\d+\s+(?:preceding|following)\b"),
}
CSS = {
    "F1": r"(?=.*margin)(?=.*auto)",
    "F2": r"wrap",
    "F3": r"align-items|align-self|justify-content",
    "F4": r"direction",
}
TEST = re.compile(r"(?m)^\s*(do_test|do_execsql_test)\s+([\w.-]+)\s*(\{)")
COMMENT = re.compile(r"/\*[\s\S]*?\*/|<!--(?:[\s\S]*?)-->")


def digest(data):
    return sha256(data).hexdigest()


def close_brace(source, start):
    depth = 0
    escaped = False
    for i in range(start, len(source)):
        char = source[i]
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError(f"unclosed Tcl braces at {start}")


def sql_cases(root, stem):
    path = f"test/{stem}.test"
    parent = root / "upstream" / "sqlite" / path
    if not parent.exists():
        return []
    raw = parent.read_bytes()
    source = raw.decode()
    rows = []
    for match in TEST.finditer(source):
        start = match.start(3)
        end = close_brace(source, start)
        expected = re.match(r"\s*(\{)", source[end + 1:])
        estart = end if expected is None else end + 1 + expected.start(1)
        eend = estart if expected is None else close_brace(source, estart)
        body = source[start + 1:end]
        sql_start = start + 1
        if match[1] == "do_test":
            wrapped = re.fullmatch(r"\s*execsql\s*\{([\s\S]*)\}\s*", body)
            if wrapped is None:
                continue
            sql_start += wrapped.start(1)
            body = wrapped[1]
        safe = re.sub(r"(?m)--[^\n]*", "", COMMENT.sub("", body)).strip()
        rows.append({
            "path": path,
            "id": match[2],
            "line": source.count("\n", 0, sql_start) + 1,
            "raw_sha256": digest(raw),
            "sql": safe,
            "static": not any(c in safe for c in "$\\"),
            "expectation": {
                "path": path,
                "lines": [source.count("\n", 0, estart) + 1,
                          source.count("\n", 0, eend) + 1],
                "suffix": source[estart + 1:eend],
                "sha256": digest(source[estart + 1:eend].encode()),
            },
        })
    return rows


def preview_sql(root, case):
    stems, pattern = SQL[case]
    inbox = root / "inbox"
    private = root / "private"
    candidates = []
    for stem in stems:
        upstream = sql_cases(root, stem)
        setup = []
        for row in upstream:
            expectation = row.pop("expectation")
            if re.search(pattern, row["sql"], re.I) and re.search(r"\b(?:select|with)\b", row["sql"], re.I):
                candidates.append(dict(row, setup_available=setup.copy()))
                (private / (case + "_" + row["id"] + ".json")).write_text(
                    json.dumps(expectation, ensure_ascii=False) + "\n")
            if row["static"]:
                for statement in row["sql"].split(";"):
                    s = statement.strip()
                    if re.match(r"(?:create|insert|update|delete|drop|replace)\b", s, re.I):
                        setup.append({"id": row["id"], "sql": s + ";"})
    candidates.sort(key=lambda row: (row["path"], row["id"]))
    (inbox / (case + ".json")).write_text(json.dumps(candidates[:30], indent=2) + "\n")
    for row in candidates[:8]:
        print(row["id"], row["line"], row["sql"][:700].replace("\n", " "), "setup", len(row["setup_available"]))


def css_paths(root, case):
    paths = (root / "raw" / "wpt-paths.txt").read_text().splitlines()
    return sorted(path for path in paths
                  if path.lower().endswith((".html", ".htm", ".xhtml"))
                  and re.search(CSS[case], Path(path).name.lower())
                  and not re.search(r"(?:^|[-_/])(?:ref|reference)(?:[.-]|$)", path)
                  and "/support/" not in path)[:30]


def mask_css(raw):
    source = raw.decode("utf-8-sig")
    without_comments = COMMENT.sub("", source)
    references = re.findall(r'<link\b[^>]*\brel\s*=\s*["\']?(?:match|mismatch)\b[^>]*>',
                            without_comments, re.I)
    scripts = re.findall(r"<script\b[^>]*>[\s\S]*?</script\s*>", without_comments, re.I)
    attrs = re.findall(r'\sdata-[\w-]+\s*=\s*(?:["\'][^"\']*["\']|[^\s>]+)',
                       without_comments, re.I)
    masked = re.sub(r"<title\b[^>]*>[\s\S]*?</title\s*>", "", without_comments, flags=re.I)
    for item in references + scripts + attrs:
        masked = masked.replace(item, "")
    masked = re.sub(r'<link\b[^>]*\brel\s*=\s*["\']?(?:help|author)\b[^>]*>', "",
                    masked, flags=re.I)
    masked = re.sub(r'<meta\b[^>]*\bname\s*=\s*["\']?assert\b[^>]*>', "", masked, flags=re.I)
    masked = re.sub(r'\s+on\w+\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+)', "", masked, flags=re.I)
    paragraphs = re.findall(r"<p\b[^>]*>[\s\S]*?</p\s*>", masked, re.I)
    assertions = [p for p in paragraphs if re.search(
        r"\b(?:should|passes if|must be|expect(?:ed)?)\b", p, re.I)]
    for item in assertions:
        masked = masked.replace(item, "<p>[masked fixture prose]</p>")
    oracle = references + scripts + attrs + assertions
    return masked.strip() + "\n", {
        "reference_count": len(references),
        "script_count": len(scripts),
        "expected_attributes": len(attrs),
        "sealed_parts": oracle,
        "parts_sha256": digest(json.dumps(oracle, ensure_ascii=False).encode()),
        "raw_sha256": digest(raw),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cache", type=Path)
    parser.add_argument("case", choices=tuple(SQL) + tuple(CSS))
    parser.add_argument("--candidate", type=int)
    args = parser.parse_args()
    if args.case in SQL:
        preview_sql(args.cache, args.case)
        return
    paths = css_paths(args.cache, args.case)
    if args.candidate is None:
        print("\n".join(f"{i:2} {p}" for i, p in enumerate(paths, 1)))
        return
    path = paths[args.candidate - 1]
    raw = (args.cache / "upstream" / "wpt" / path).read_bytes()
    masked, private = mask_css(raw)
    stem = f"{args.case}_{args.candidate:02}"
    (args.cache / "private" / (stem + ".json")).write_text(json.dumps(private) + "\n")
    (args.cache / "inbox" / (stem + ".html")).write_text(masked)
    print(path, {k: v for k, v in private.items() if k != "sealed_parts"})
    print(masked)


if __name__ == "__main__":
    main()
