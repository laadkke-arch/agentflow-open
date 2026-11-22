"""Enumerate and sample the public declarations linked from the two T0 indexes."""

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

SEED = "AF-RES-024|2021-12-31|v1"
T0 = {
    "python": ("3.10.1", "python/cpython", "2cd268a3a9340346dd86b66db2e9b428b3f878fc",
               "Doc/library/index.rst", "https://www.python.org/downloads/release/python-3101/"),
    "node": ("17.3.0", "nodejs/node", "e5873d786249d9b6aa1d8c422f856036c2c53e5e",
             "doc/api/index.md", "https://nodejs.org/en/blog/release/v17.3.0"),
}
PY_DECL = re.compile(
    r"^\.\. (module|function|class|data)::\s+([a-zA-Z][\w.]*)"
    r"(?=[\s(\[]|$)"
)
PY_SCOPE = re.compile(r"^\.\. (?:module|currentmodule)::\s+([\w.]+)")
NODE_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
NODE_NAME = re.compile(r"^(?:--[a-zA-Z][\w-]*|[a-zA-Z$][\w.$]*)(?=[\s(=\[)]|$)")
PY_WARN = re.compile(r"(?m)^\s*\.\. (deprecated(?:-removed|-removed-pending)?)::([^\n]*)")
PY_MODULE_END = re.compile(r"^\.\. (?:attribute|currentmodule|method|object|exception)::")
PY_WARN_PROSE = re.compile(
    r"(?:is|has been) deprecated with removal planned|this module (?:is|has been) deprecated",
    re.I,
)
NODE_WARN = re.compile(r"(?im)^>\s*Stability:\s*0\b")
NODE_EXPERIMENT = re.compile(r"(?im)^>\s*Stability:\s*1(?:\s|\.|$)")
NODE_EXCLUDED = {"documentation", "synopsis", "addons", "n-api", "embedding", "deprecations"}
NODE_MODULES = {"modules", "esm", "module", "packages"}


@dataclass(frozen=True)
class Section:
    kind: str
    name: str
    group: str
    start: int
    text: str
    warned: bool
    experimental: bool = False

    @property
    def end(self):
        return self.start + len(self.text.splitlines()) - 1


def python_links(text, path):
    directory = PurePosixPath(path).parent
    for block in re.finditer(r"(?m)^\.\. toctree::[ \t]*\n((?:[ \t]+[^\n]*\n|\n)*)", text):
        for entry in block[1].splitlines():
            value = entry.strip()
            if not value or value.startswith(":"):
                continue
            if "<" in value and value.endswith(">"):
                value = value.rpartition("<")[2][:-1]
            if "/" in value or "*" in value:
                continue
            yield str(directory / (value if value.endswith(".rst") else f"{value}.rst"))


def node_links(text):
    for link in re.finditer(r"\]\(([a-z0-9_\-]+\.md)\)", text):
        yield f"doc/api/{link[1]}"


def python_warned(text):
    for match in PY_WARN.finditer(text):
        versions = [tuple(map(int, v.split("."))) for v in re.findall(r"\d+\.\d+", match[2])]
        if match[1] != "deprecated-removed" or len(versions) < 2 or versions[1] > (3, 10):
            return True
    return bool(PY_WARN_PROSE.search(text))


def python_sections(text, path):
    """Restrict the frame to titled module and non-nested public declarations."""
    lines = text.splitlines()
    declarations = [(i, match) for i, line in enumerate(lines) if (match := PY_DECL.match(line))]
    module_scope = [(i, match[1]) for i, line in enumerate(lines) if (match := PY_SCOPE.match(line))]
    primary = module_scope[0][1] if module_scope else PurePosixPath(path).stem
    module_ends = {}
    for offset, (i, match) in enumerate(declarations):
        if match[1] == "module":
            following = declarations[offset + 1][0] if offset + 1 < len(declarations) else len(lines)
            limit = min(following, i + 84)
            stop = next((j for j in range(i + 1, limit) if PY_MODULE_END.match(lines[j])), limit)
            module_ends[match[2]] = (i, stop)
    module_warnings = {name: python_warned("\n".join(lines[i:end]))
                       for name, (i, end) in module_ends.items()}

    for i, match in declarations:
        kind, name = match.groups()
        active = next((mod for j, mod in reversed(module_scope) if j <= i), primary)
        if kind == "module":
            end = module_ends[name][1]
            symbol = name
        else:
            if any(segment.startswith("_") for segment in name.split(".")):
                continue
            end = i + 1
            while end < len(lines) and (not lines[end] or lines[end][0].isspace()):
                end += 1
            symbol = name if name.startswith(f"{active}.") or not module_scope else f"{active}.{name}"
        block = "\n".join(lines[i:end]).rstrip()
        warning = module_warnings.get(active, module_warnings.get(primary, False))
        yield Section(kind, symbol, active.split(".")[0], i + 1, block,
                      warning or python_warned(block))


def node_sections(text, path):
    """Index literal Markdown API headings with their own explanatory text."""
    lines = text.splitlines()
    headings = [(i, len(match[1]), match[2]) for i, line in enumerate(lines)
                if (match := NODE_HEADING.match(line))]
    chapter = PurePosixPath(path).stem
    group = "modules" if chapter in NODE_MODULES else chapter
    top_end = headings[1][0] if len(headings) > 1 else len(lines)
    chapter_intro = "\n".join(lines[:top_end])
    warned = bool(NODE_WARN.search(chapter_intro))
    experimental = bool(NODE_EXPERIMENT.search(chapter_intro))

    for offset, (i, level, title) in enumerate(headings):
        literal = re.search(r"`([^`]+)`", title)
        if level < 2 or not literal:
            continue
        name = NODE_NAME.match(literal[1])
        if not name or title.startswith("Event:") or literal[1].startswith("new "):
            continue
        symbol = name[0]
        if symbol.startswith("--"):
            kind = "option"
        elif title.startswith("Class:"):
            kind = "class"
        elif "(" in literal[1]:
            kind = "method"
        elif "." in symbol or re.fullmatch(r"[A-Z][A-Za-z0-9_]+", symbol):
            kind = "property"
        else:
            continue
        end = headings[offset + 1][0] if offset + 1 < len(headings) else len(lines)
        block = "\n".join(lines[i:end]).rstrip()
        yield Section(kind, symbol, group, i + 1, block,
                      warned or bool(NODE_WARN.search(block)),
                      experimental or bool(NODE_EXPERIMENT.search(block)))


def sections(ecosystem, text, path):
    parser = python_sections if ecosystem == "python" else node_sections
    return list(parser(text, path))


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def order(stage, identity):
    return digest(f"{SEED}|{stage}|{identity}")


def build(root):
    rows = {}
    exclusions = []
    for eco, (version, repo, commit, index, _release) in T0.items():
        links = python_links if eco == "python" else lambda value, _: node_links(value)
        queue = [index]
        done = set()
        while queue:
            path = queue.pop(0)
            if path in done:
                continue
            done.add(path)
            local = root / eco / path
            if not local.is_file():
                exclusions.append([eco, path, "linked_source_unavailable"])
                continue
            raw = local.read_bytes()
            value = raw.decode("utf-8")
            queue.extend(links(value, path) if eco == "python" or path == index else [])
            if eco == "node" and PurePosixPath(path).stem in NODE_EXCLUDED:
                exclusions.append([eco, path, "nonframe_chapter"])
                continue
            found = sections(eco, value, path)
            if not found:
                exclusions.append([eco, path, "no_public_declaration_in_parser"])
            for section in found:
                identity = f"{eco}/{PurePosixPath(path).stem}/{section.kind}/{section.name}"
                if identity in rows:
                    continue
                rows[identity] = dict(
                    id=identity, ecosystem=eco, group=section.group, kind=section.kind,
                    symbol=section.name, selected=0, warned=int(section.warned),
                    experimental=int(section.experimental), path=path,
                    t0_url=f"https://github.com/{repo}/blob/{commit}/{path}#L{section.start}-L{section.end}",
                    t0_version=version, t0_sha=commit, start=section.start, end=section.end,
                    blob=hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest(),
                    section_sha256=digest(section.text), section=section.text,
                )
    return rows, exclusions


def sample(rows):
    for eco in T0:
        groups = defaultdict(list)
        for row in rows.values():
            if row["ecosystem"] == eco:
                groups[row["group"]].append(row)
        group_warned = {group: any(row["warned"] for row in values) for group, values in groups.items()}
        counts = Counter(group_warned.values())
        quotas = {True: min(8, counts[True]), False: min(32 - min(8, counts[True]), counts[False])}
        quotas[True] = 32 - quotas[False]
        if quotas[True] > counts[True]:
            raise ValueError(f"{eco}: {counts} cannot furnish 32 groups")
        for warned, quota in quotas.items():
            ordered = sorted((g for g in groups if group_warned[g] == warned),
                             key=lambda group: order("group", f"{eco}/{group}"))
            for rank, group in enumerate(ordered, 1):
                eligible = [row for row in groups[group] if row["warned"] == int(warned)]
                first = min(eligible, key=lambda row: order("candidate", row["id"]))
                for row in groups[group]:
                    selectable = row in eligible
                    chosen = rank <= quota and row is first
                    row.update(
                        stratum="warned" if warned else "ordinary",
                        selected=int(chosen), group_rank=rank, group_frame_n=len(ordered),
                        group_quota=quota, candidate_n=len(eligible),
                        prob_group=f"{quota}/{len(ordered)}",
                        prob_within=f"1/{len(eligible)}" if selectable else "0",
                        inclusion_prob=f"{quota}/{len(ordered) * len(eligible)}" if selectable else "0",
                        selection_rule=("chosen" if chosen else "warned_group_other_candidate"
                                        if not selectable else "hash_not_selected"),
                    )
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--t0-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--claims", type=Path)
    parser.add_argument("--review-out", type=Path)
    args = parser.parse_args()
    rows, exclusions = build(args.t0_root)
    sample(rows)
    claims = json.loads(args.claims.read_text()) if args.claims else {}
    selected = {r["id"] for r in rows.values() if r["selected"]}
    if args.claims and set(claims) != selected:
        raise ValueError(f"claims mismatch; missing {selected - set(claims)}; extra {set(claims) - selected}")
    ordered = sorted(rows.values(), key=lambda row: row["id"])
    if args.review_out:
        with args.review_out.open("w") as review:
            for row in ordered:
                if row["selected"]:
                    review.write(f"\n{'=' * 18} {row['id']} L{row['start']}–{row['end']} "
                                 f"warned={row['warned']} experimental={row['experimental']}\n"
                                 f"{row['section']}\n")
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "cohort.csv").open("w", newline="") as stream:
        fields = [k for k in ordered[0] if k != "section"] + ["initial", "claim", "platform", "alternatives"]
        writer = csv.DictWriter(stream, fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in ordered:
            writer.writerow(row | claims.get(row["id"], {}))
    with (args.out / "frame-exclusions.csv").open("w", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["ecosystem", "path", "why"])
        writer.writerows(sorted(exclusions))
    print(Counter((r["ecosystem"], r["stratum"], r["selected"]) for r in rows.values()))
    print(Counter((r["ecosystem"], r["stratum"]) for r in rows.values() if r["selected"]))


if __name__ == "__main__":
    main()
