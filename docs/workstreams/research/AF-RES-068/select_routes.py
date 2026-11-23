"""Build and apply a metadata-only index for the three frozen first actions."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

from projection import source_blocks

ROOT = Path(__file__).resolve().parent
PUBLIC_DOCS = {
    "docs/api.md", "docs/options.md", "docs/json-schema.md",
    "docs/json-type-definition.md", "docs/guide/typescript.md", "docs/keywords.md",
}
NAME = r"[@$A-Za-z_][@$A-Za-z_0-9]*"
RECEIVERS = ("jsonld.promises.", "ajvInstance.", "jsonld.", "ajv.")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalized_name(symbol):
    for prefix in RECEIVERS:
        if symbol.startswith(prefix):
            return symbol[len(prefix):]
    return symbol


def official_doc(path):
    return path == "README.md" or (
        path.startswith("docs/") and path.endswith((".md", ".rst"))
        and not path.startswith(("docs/news/", "docs/packages/"))
        and PurePosixPath(path).stem not in {"security", "testimonials"}
    )


def clean_title(title):
    return " ".join(re.sub(r"<[^>]+>", "", title).split())


def heading_names(title, path):
    if path not in PUBLIC_DOCS and path != "README.md":
        return []
    if re.fullmatch(NAME, title):
        return [title]
    declaration = re.match(r"^(?:new\s+)?(?:ajv\.)?(" + NAME + r")\(", title)
    if declaration and path == "docs/api.md":
        return [declaration[1]]
    return []


def public_code(path, lines):
    for no, line in enumerate(lines, 1):
        if path == "lib/jsonld.js":
            for symbol in re.findall(r"\bjsonld\.(" + NAME + r")\s*=", line) if line.startswith("jsonld.") else []:
                start = no
                if no >= 2 and lines[no - 2].strip() == "*/":
                    start = next((i for i in range(no - 2, 0, -1)
                                  if lines[i - 1].lstrip().startswith("/**")), no)
                yield symbol, no, start, "entry_api"
        if path == "lib/context.js":
            key = re.match(r"^    case '(@\w+)':\s*$", line)
            if key:
                yield key[1], no, no, "language_keyword"
        if path.startswith("lib/vocabularies/"):
            key = re.match(r'^\s*keyword:\s*["\'](' + NAME + r')["\']', line)
            if key:
                yield key[1], no, no, "schema_keyword"
        if path in {"lib/ajv.ts", "lib/2019.ts", "lib/2020.ts", "lib/jtd.ts",
                    "lib/core.ts", "lib/types/json-schema.ts", "lib/types/jtd-schema.ts"}:
            export = re.match(r"^export (?:default )?(?:abstract )?(?:type|interface|class|function) (" + NAME + r")", line)
            if export:
                yield export[1], no, no, "public_export"


def git(path, *args):
    return subprocess.check_output(["git", "-C", str(path), *args])


def build_metadata(repos):
    pins = read_json(ROOT / "evidence/pins.json")
    metadata = {}
    for package, item in pins.items():
        repo = repos / (item["package"] + ".git")
        ref = item["pin"]
        entries = [entry.split("\t", 1) for entry in git(repo, "ls-tree", "-r", ref).decode().splitlines()]
        files = {path for mode, path in entries if mode.split()[1] == "blob"}
        docs = []
        symbols = []
        manifest = read_json(ROOT / "evidence/pins.json")[package]
        package_file = git(repo, "show", f"{ref}:package.json")
        package_info = json.loads(package_file)
        if package_info["version"] != manifest["version"]:
            raise ValueError(f"{package} version differs from {ref}:package.json")
        for path in sorted(files):
            if official_doc(path):
                source = git(repo, "show", f"{ref}:{path}").decode()
                for block in source_blocks(path, source):
                    if block.kind != "heading":
                        continue
                    title = clean_title(block.text)
                    record = {"path": path, "line": block.first, "label": title, "anchor": block.anchor}
                    docs.append(record)
                    for symbol in heading_names(title, path):
                        symbols.append({**record, "symbol": symbol, "tier": 0,
                                        "namespace": "official_heading", "display_line": block.first})
            if (path in {"lib/ajv.ts", "lib/core.ts", "lib/2019.ts", "lib/2020.ts", "lib/jtd.ts",
                         "lib/types/json-schema.ts", "lib/types/jtd-schema.ts", "lib/jsonld.js", "lib/context.js"}
                    or path.startswith("lib/vocabularies/") and path.endswith(".ts")):
                src = git(repo, "show", f"{ref}:{path}").decode()
                for name, line, display, kind in public_code(path, src.splitlines()):
                    symbols.append({"symbol": name, "path": path, "line": line, "display_line": display,
                                    "label": name, "anchor": "", "tier": 1, "namespace": kind})
        test_paths = sorted(p for p in files if p.startswith(("test/", "tests/", "spec/")))
        gitlinks = {p: mode.split()[2] for mode, p in entries if mode.split()[1] == "commit"}
        metadata[ref] = {"package": package, "repo": item["repo"], "pin": ref,
                         "package_sha256": hashlib.sha256(package_file).hexdigest(),
                         "package_entry": package_info.get("main"), "paths": sorted(files),
                         "docs": docs, "symbols": symbols, "test_paths": test_paths, "gitlinks": gitlinks}
    return metadata


def route_points(cases, mentions, rules, metadata):
    by_case = defaultdict(list)
    for token in mentions:
        by_case[token["case_id"]].append(token)
    route_list = []
    for case in cases:
        ref = case["pin"]
        index = metadata[ref]
        a = {"path": rules["A"]["path"], "line": rules["A"]["line"], "label": "README start",
             "selection": "A_README", "reason": "fixed root README start"}
        patterns = rules["B"]["title_order"][case["operation_family"]]
        b_matches = [(i, h["path"], h["line"], h)
                     for i, pat in enumerate(patterns)
                     for h in index["docs"] if re.fullmatch(pat, h["label"].casefold())]
        if b_matches:
            rank, _, _, b = min(b_matches, key=lambda x: x[:3])
            b = {**b, "selection": "B_TITLE", "reason": patterns[rank], "rank": rank + 1,
                 "candidate_count": len(b_matches)}
        else:
            b = {**a, "selection": "B_NO_TITLE", "reason": "no frozen family/title match", "candidate_count": 0}
        symbols = defaultdict(list)
        for hit in index["symbols"]:
            symbols[hit["symbol"]].append(hit)
        tokens = sorted(by_case[case["case_id"]], key=lambda x: (x["line"], x["column"]))
        matched = [(m, symbols[normalized_name(m["token"])]) for m in tokens if normalized_name(m["token"]) in symbols]
        if matched:
            origin, options = matched[0]
            first = min(options, key=lambda d: (d["tier"], d["path"], d["line"]))
            c = {**first, "selection": "C_EXACT", "reason": "body order → exact heading/declaration → path/line",
                 "body_token": origin["token"], "body_line": origin["line"], "body_column": origin["column"],
                 "body_form": origin["form"], "candidate_count": len(options), "matched_tokens_total": len(matched)}
        else:
            c = {**a, "selection": "C_NO_EXACT", "reason": "no exact match in frozen public index",
                 "candidate_count": 0, "matched_tokens_total": 0}
        for name, point in zip("ABC", (a, b, c), strict=True):
            route_list.append({**case, **point, "route": name})
    return route_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repos", type=Path, required=True, help="Directory containing ajv.git and jsonld.git")
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args()
    options.output.mkdir(parents=True, exist_ok=True)
    metadata = build_metadata(options.repos)
    write_json(options.output / "selector-metadata.json", metadata)
    for item in metadata.values():
        print(item["package"], len(item["docs"]), len(item["symbols"]), len(item["test_paths"]))


if __name__ == "__main__":
    main()
