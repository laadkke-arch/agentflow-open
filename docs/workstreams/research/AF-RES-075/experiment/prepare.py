"""Freeze scenario selection and regenerate isolated replay inputs offline."""
import argparse
import json
import random
from pathlib import Path

from registry import ROOT, matched_key, parse, sha, write_csv, write_json

SEED = 75075
NATURAL = {
    "PG": {
        "Android.bp": "new exact registration: E/U gain, R from empty",
        "example.h": "retained glob collision, E/U/R hold",
        "example.lean": "second eligible class joins at equal score: U falls, R grows",
        "example.m": "retained glob collision, E/U/R hold",
    },
    "TZ": {
        "CA": "multiple memberships including shared rows; E/U/R hold",
        "DE": "Berlin and shared Zurich remain, E/U/R hold",
        "MN": "Choibalsan moves outside the table, E/U hold, R shrinks",
        "PT": "published transition changes may leave membership and all claims unchanged",
    },
}
CONTROL = {
    "PG": (
        ("probe.abap", "add_tie", "ABAPLexer", "E holds, U falls, R adds a tie"),
        ("probe.abap", "remove_winner", "ABAPLexer", "E/U fall, R becomes empty"),
        ("example.m", "irrelevant_edit", "ABAPLexer", "E/U/R and representative clause hold"),
        ("example.m", "alias_and_order", "MatlabLexer", "E/U/R hold; alias and line may change"),
    ),
    "TZ": (
        ("AD", "add_tie", "Europe/Andorra", "E holds, U falls, R adds a tie"),
        ("DE", "remove_winner", "Europe/Berlin", "E holds, U rises, Zurich promoted"),
        ("DE", "irrelevant_edit", "Europe/Andorra", "E/U/R and representative clause hold"),
        ("DE", "reverse_order", None, "E/U/R hold; line changes; country roles preserved"),
    ),
}
PAIR_COLUMNS = (
    "pair_id", "domain", "kind", "query", "anchor_id", "mutation", "target_id", "seed",
    "before_edition", "after_edition", "before_path", "after_path", "before_url", "after_url",
    "before_sha256", "after_sha256", "expected",
)
BASE = "https://github.com/laadkke-arch/agentflow-open/blob/work/research-af-res-075/"
OWNED = "docs/workstreams/research/AF-RES-075/"


def changed(domain, raw, mutation, target):
    rows = parse(domain, raw)
    suffix = random.Random(SEED).randint(100000, 999999)
    new_id = f"ZZAF075{suffix}Lexer" if domain == "PG" else f"Europe/ZZAF075{suffix}"
    lines = raw.decode("utf8").splitlines(keepends=True)
    old = rows.get(target)
    if old:
        position = old["line"] - 1
    if mutation in ("add_tie", "swap_peer"):
        if domain == "PG":
            cloned = old["clause"].replace(repr(target), repr(new_id), 1)
        else:
            cloned = "\t".join([*old["fields"][:2], new_id, "synthetic control"])
        if mutation == "add_tie":
            lines.insert(position + 1, cloned + "\n")
        else:
            lines[position] = cloned + "\n"
    elif mutation == "remove_winner":
        del lines[position]
    elif mutation == "irrelevant_edit":
        if domain == "PG":
            module, name, aliases, patterns, mimetypes = old["fields"]
            value = (module, name + " AF075", aliases, patterns, mimetypes)
            lines[position] = f"    {target!r}: {value!r},\n"
        else:
            lines[position] = "\t".join([*old["fields"][:3], "synthetic control"]) + "\n"
    elif mutation in ("alias_and_order", "reverse_order"):
        if old:
            module, name, aliases, patterns, mimetypes = old["fields"]
            value = (module, name, (*aliases, f"af075-{suffix}"), patterns, mimetypes)
            lines[position] = f"    {target!r}: {value!r},\n"
        positions = sorted(row["line"] - 1 for row in rows.values())
        reverse = [lines[index] for index in reversed(positions)]
        for index, line in zip(positions, reverse, strict=True):
            lines[index] = line
    else:
        raise ValueError(mutation)
    data = "".join(lines).encode()
    parse(domain, data)
    return data


def original_inputs():
    manifest = json.loads((ROOT / "inputs/manifest.json").read_bytes())
    versions = {"PG": [], "TZ": []}
    for item in manifest["editions"]:
        raw = (ROOT / item["copy"]).read_bytes()
        if sha(raw) != item["sha256"] or len(parse(item["domain"], raw)) != item["rows"]:
            raise ValueError(f"Upstream pin mismatch: {item['copy']}")
        versions[item["domain"]].append({
            "data": raw, "sha256": item["sha256"], "edition": item["edition"],
            "path": item["copy"], "url": item["source_url"],
            "publisher_url": item["publisher_listing_url"], "row_count": item["rows"],
        })
    return versions


def scenarios():
    pairs = []
    for domain, (old, new) in original_inputs().items():
        older = parse(domain, old["data"])
        newer = parse(domain, new["data"])
        union = sorted(older.keys() | newer.keys())
        anchors = []
        for query, expected in NATURAL[domain].items():
            anchor = next(
                row_id for row_id in union
                if any(row_id in data and matched_key(domain, query, data[row_id]["key"])
                       for data in (older, newer))
            )
            anchors.append((anchor, query, expected))
        for index, (anchor, query, expected) in enumerate(sorted(anchors), 1):
            pairs.append({
                "pair_id": f"{domain}-N{index:02}", "domain": domain, "kind": "natural",
                "query": query, "anchor_id": anchor, "mutation": "published_release",
                "target_id": "", "seed": "", "before": old, "after": new, "expected": expected,
            })
        controls = [(f"{domain}-C{index:02}", spec) for index, spec
                    in enumerate(CONTROL[domain], 1)]
        if domain == "PG":
            controls.append(("SWAP01", ("example.m", "swap_peer", "ObjectiveCLexer",
                                         "equal kept clause and counts; different R peer ID")))
        for pair_id, (query, mutation, target, expected) in controls:
            data = changed(domain, new["data"], mutation, target)
            sha256 = sha(data)
            path = f"inputs/controls/{pair_id}.txt"
            after = {
                "data": data, "sha256": sha256, "edition": f"capture-{sha256[:16]}",
                "path": path, "url": BASE + OWNED + path, "publisher_url": None,
                "row_count": len(parse(domain, data)),
            }
            pairs.append({
                "pair_id": pair_id, "domain": domain,
                "kind": "supplemental" if pair_id == "SWAP01" else "injected",
                "query": query, "anchor_id": "", "mutation": mutation,
                "target_id": target or "", "seed": SEED, "before": new, "after": after,
                "expected": expected,
            })
    return sorted(pairs, key=lambda case: (case["domain"], case["kind"] != "natural",
                                            case["pair_id"] == "SWAP01", case["pair_id"]))


def wire_pair(case):
    return {key: value for key, value in case.items() if key not in ("before", "after")} | {
        "before": {key: value for key, value in case["before"].items() if key != "data"},
        "after": {key: value for key, value in case["after"].items() if key != "data"},
    }


def table_pair(case):
    row = {key: value for key, value in case.items() if key not in ("before", "after")}
    for phase in ("before", "after"):
        for key in ("edition", "path", "url", "sha256"):
            row[f"{phase}_{key}"] = case[phase][key]
    return row


def prepare(out, freeze):
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        raise ValueError(f"Output directory must be empty: {out}")
    cases = scenarios()
    for role in ("broker-assets", "oracle-assets", "blind-cwd", "oracle-cwd"):
        (out / role).mkdir()
    for case in cases:
        for phase in ("before", "after"):
            asset = case[phase]
            if phase == "after" and case["kind"] != "natural":
                copy = ROOT / asset["path"]
                if freeze:
                    copy.parent.mkdir(parents=True, exist_ok=True)
                    copy.write_bytes(asset["data"])
                elif copy.read_bytes() != asset["data"]:
                    raise ValueError(f"Synthetic file does not match its seed: {copy}")
            for role in ("broker-assets", "oracle-assets"):
                path = out / role / asset["sha256"]
                if not path.exists():
                    path.write_bytes(asset["data"])
    write_json(out / "sealed.json", [wire_pair(case) for case in cases])
    write_csv(out / "pairs.csv", PAIR_COLUMNS, map(table_pair, cases))
    if freeze:
        (ROOT / "pairs.csv").write_bytes((out / "pairs.csv").read_bytes())
    elif (ROOT / "pairs.csv").read_bytes() != (out / "pairs.csv").read_bytes():
        raise ValueError("Regenerated selection differs from the committed pair ledger")
    print(f"sealed {len(cases) - 1} primary pairs and SWAP01, seed={SEED}")


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--out", type=Path, required=True)
    cli.add_argument("--freeze", action="store_true", help="author the initial pair and control files")
    args = cli.parse_args()
    prepare(args.out, args.freeze)
