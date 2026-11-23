"""Exhaustive reference executable. This process receives a raw file and query."""
import argparse
import ast
import csv
import hashlib
import io
import json
import re
import tokenize
from pathlib import Path


def primary_patterns(line):
    tokens = list(tokenize.generate_tokens(io.StringIO(line.lstrip() + "\n").readline))
    first, colon, opening = tokens[:3]
    if first.type != tokenize.STRING or colon.string != ":" or opening.string != "(":
        raise ValueError("Unrecognized generated registry line")
    nesting = 1
    field = 0
    patterns = []
    for token in tokens[3:]:
        if token.string in ("(", "[", "{"):
            nesting += 1
        elif token.string in (")", "]", "}"):
            nesting -= 1
            if not nesting:
                break
        elif token.string == "," and nesting == 1:
            field += 1
        elif field == 3 and token.type == tokenize.STRING:
            patterns.append(ast.literal_eval(token.string))
    if nesting or field not in (4, 5):
        raise ValueError(f"Expected five registry fields, found {field + 1}")
    return ast.literal_eval(first.string), patterns


def filename_match(query, pattern):
    expression = []
    index = 0
    while index < len(pattern):
        char = pattern[index]
        if char == "*":
            expression.append(".*")
        elif char == "?":
            expression.append(".")
        elif char == "[" and "]" in pattern[index + 1:]:
            closing = pattern.index("]", index + 1)
            members = pattern[index + 1:closing]
            if not re.fullmatch(r"[A-Za-z0-9-]+", members):
                raise ValueError(f"Pattern outside the frozen oracle grammar: {pattern}")
            expression.append("[" + members + "]")
            index = closing
        else:
            expression.append(re.escape(char))
        index += 1
    return re.fullmatch("".join(expression), query, re.DOTALL) is not None


def solve(domain, query, raw):
    body = raw.decode("utf8")
    source_lines = body.splitlines()
    population = {}
    scores = {}
    if domain == "PG":
        subject = query.rsplit("/", 1)[-1]
        if not subject:
            raise ValueError("No basename")
        if source_lines[3] != "LEXERS = {" or source_lines[-1] != "}":
            raise ValueError("Unrecognized upstream registry wrapper")
        for number, clause in enumerate(source_lines[4:-1], 5):
            row_id, patterns = primary_patterns(clause)
            if row_id in population:
                raise ValueError("Duplicate lexer identifier")
            population[row_id] = number
            points = [
                1 if re.search(r"[\[?*]", pattern) else 2
                for pattern in patterns if filename_match(subject, pattern)
            ]
            if points:
                scores[row_id] = max(points)
    else:
        if not re.fullmatch("[A-Z]{2}", query):
            raise ValueError("No country code")
        for number, fields in enumerate(csv.reader(io.StringIO(body), delimiter="\t",
                                                  quoting=csv.QUOTE_NONE), 1):
            if not fields or fields[0].startswith("#"):
                continue
            country_field, _, row_id = fields[:3]
            if row_id in population:
                raise ValueError("Duplicate zone identifier")
            population[row_id] = number
            if country_field == query or query in country_field.split(","):
                scores[row_id] = 2 if country_field.partition(",")[0] == query else 1

    ordered = sorted(scores)
    selection = sorted(scores, key=lambda item: (-scores[item], item))
    best = scores[selection[0]] if selection else None
    return {
        "scanned": len(population), "eligible": [[item, scores[item]] for item in ordered],
        "exists": len(ordered) > 0, "unique": len(ordered) == 1,
        "top": [item for item in selection if scores[item] == best],
        "citations": [
            {
                "id": item, "line": population[item],
                "clause_sha256": hashlib.sha256(source_lines[population[item] - 1].encode()).hexdigest(),
            }
            for item in ordered
        ],
    }


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("domain", choices=("PG", "TZ"))
    cli.add_argument("query")
    cli.add_argument("file", type=Path)
    args = cli.parse_args()
    print(json.dumps(solve(args.domain, args.query, args.file.read_bytes()), ensure_ascii=False))
