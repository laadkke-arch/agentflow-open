"""Project directly acquired openings and constructed bodies into replay inputs."""

import argparse
import importlib.util
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
PREVIOUS = "e69a3f837d400ba8a4820edb5bcd91223dc5f9cc"
PARTICLES = frozenset("은 는 이 가 을 를 에 에서 로 으로 와 과".split())
POLICIES = ("A", "B", "C", "D")
VIEWS = ("raw", "masked")


def load_previous(prior):
    """Load the two fixed predecessor modules without changing this workstream."""
    sys.path.insert(0, str(prior.resolve()))
    try:
        paths = [(name, prior / f"{name}.py") for name in ("prepare", "replay")]
        modules = []
        for name, path in paths:
            module_name = "prepare" if name == "prepare" else "af122_replay"
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules.append(module)
            if name == "prepare":
                sys.modules["prepare"] = module
    finally:
        sys.path.pop(0)
    return tuple(modules)


def aliases_by_phrase(prepare, alias_path):
    return {
        row["alias_id"]: (row["feature_id"], tuple(prepare.KOREAN_WORD.findall(row["surface"])))
        for row in prepare.read_csv(alias_path)
        if row["status"] == "active"
    }


def sparse_runs(prepare, body, glossary):
    """Keep only terms needed for any of B, C or D, plus intervening positions."""
    finals = {phrase[-1] for _, phrase in glossary.values()}
    prefixes = {term for _, phrase in glossary.values() for term in phrase[:-1]}
    runs = []
    examined = 0
    for run in prepare.KOREAN_RUN.finditer(body):
        sequence = []
        for token in prepare.KOREAN_WORD.finditer(run.group()):
            examined += 1
            word = token.group()
            keep = word in prefixes or any(final in word for final in finals)
            sequence.append([run.start() + token.start(), word] if keep else None)
        if any(sequence):
            runs.append(sequence)
    return runs, examined


def find_aliases(runs, glossary):
    matches = []
    inspection = defaultdict(int)
    for alias_id, (feature, phrase) in glossary.items():
        lead, final = phrase[:-1], phrase[-1]
        for run in runs:
            for first in range(len(run) - len(phrase) + 1):
                earlier = run[first:first + len(lead)]
                terminal = run[first + len(lead)]
                inspection["windows"] += 1
                if terminal is None or tuple(item[1] if item else None for item in earlier) != lead:
                    continue
                inspection["final_tokens"] += 1
                token_start, token = terminal
                offset = token.find(final)
                while offset != -1:
                    last_start = token_start + offset
                    end = last_start + len(final)
                    tail = token[offset + len(final):]
                    particle = tail if offset == 0 and tail in PARTICLES else ""
                    first_policy = "D" if offset or (tail and not particle) else ("C" if particle else "B")
                    matches.append({
                        "alias_id": alias_id,
                        "feature_id": feature,
                        "first_policy": first_policy,
                        "phrase": " ".join(phrase),
                        "start": earlier[0][0] if earlier else last_start,
                        "end": end,
                        "last_start": last_start,
                        "token_start": token_start,
                        "token_end": token_start + len(token),
                        "last_token": token,
                        "prefix": token[:offset],
                        "suffix": tail,
                        "particle": particle,
                    })
                    offset = token.find(final, offset + 1)
    return sorted(matches, key=lambda row: (row["start"], row["end"], row["alias_id"])), dict(inspection)


def context(body, start, end):
    """Return up to three surrounding words on each side of the same line."""
    line_start = body.rfind("\n", 0, start) + 1
    line_end = body.find("\n", end)
    left = list(re.finditer(r"\S+", body[line_start:start]))
    right = list(re.finditer(r"\S+", body[end:line_end if line_end != -1 else len(body)]))
    before = body[line_start + left[-3].start():start] if len(left) >= 3 else body[line_start:start]
    after = body[end:end + right[2].end()] if len(right) >= 3 else body[end:line_end if line_end != -1 else len(body)]
    return before.strip(), after.strip()


def project(snapshots, prior, prepare):
    cards = prepare.read_csv(prior / "catalog.csv")
    alias_path = prior / "aliases.csv"
    glossary = aliases_by_phrase(prepare, alias_path)
    views, audits = prepare.prepare(snapshots, cards, prepare.read_csv(alias_path))
    by_id = {row["request_id"]: row for row in snapshots}
    audit_by_id = {row["request_id"]: row for row in audits}
    rows, matched = [], []
    for view in views:
        request = view["request_id"]
        snapshot = by_id[request]
        raw = unicodedata.normalize("NFC", snapshot["body"])
        body = list(raw)
        if view["view"] == "masked":
            for span in audit_by_id[request]["mask"]:
                body[span["start"]:span["end"]] = span["after"]
        body = "".join(body)
        if prepare.sha(body) != view["view_sha256"]:
            raise ValueError(f"{request}: predecessor and capture disagree about view SHA")
        runs, words = sparse_runs(prepare, body, glossary)
        payload = {"korean_retained_runs": runs, "korean_words": words}
        rows.append({
            **view, **payload,
            "extended_projection_sha256": prepare.sha(prepare.packed(payload)),
        })
        for hit in find_aliases(runs, glossary)[0]:
            start, end = hit["start"], hit["token_end"]
            before, after = context(raw, start, end)
            preceding_lines = raw.count("\n", 0, start)
            matched.append({
                "request_id": request,
                "view": view["view"],
                **hit,
                "before": before,
                "surface": raw[start:end].replace("\n", "\\n"),
                "after": after,
                "source_line": snapshot.get("line_start", 1) + preceding_lines,
            })
    return rows, matched, audits


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prior", required=True, type=Path)
    parser.add_argument("--forum-bodies", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    prepare, _ = load_previous(args.prior)
    metadata = {row["request_id"]: row for row in prepare.read_jsonl(HERE / "openings.jsonl")}
    forum = prepare.read_jsonl(args.forum_bodies)
    if len(forum) != len(metadata) or {row["request_id"] for row in forum} != set(metadata):
        raise ValueError("forum inputs must cover each recorded opening exactly once")
    for row in forum:
        opening = metadata[row["request_id"]]
        if prepare.sha(unicodedata.normalize("NFC", row["body"])) != opening["raw_nfc_sha256"]:
            raise ValueError(f"{row['request_id']}: input SHA differs from the frozen opening")
        row["line_start"] = int(re.search(r"L(\d+)", opening["location"]).group(1))
    previous = prepare.read_jsonl(args.prior / "evidence/controls.jsonl")
    new = prepare.read_jsonl(HERE / "controls.jsonl")

    args.out.mkdir(parents=True, exist_ok=True)
    for group, snapshots in (("forum", forum), ("controls", previous + new)):
        rows, matches, audits = project(snapshots, args.prior, prepare)
        prepare.write_jsonl(args.out / f"{group}-inputs.jsonl", rows)
        prepare.write_jsonl(args.out / f"{group}-matches.jsonl", matches)
        prepare.write_jsonl(args.out / f"{group}-audit.jsonl", audits)


if __name__ == "__main__":
    main()
