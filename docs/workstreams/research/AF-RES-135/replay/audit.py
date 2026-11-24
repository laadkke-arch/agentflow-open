"""Recount the committed evidence without using the decision or cost generator."""
import collections
import csv
import hashlib
import itertools
import json
import pathlib
import re
import subprocess
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]


def rows(path):
    with (ROOT / path).open() as f:
        return list(csv.DictReader(f))


def jsonl(path):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines()]


def same_cell(x, y):
    return (x.get("kind"), x.get("value"), x.get("name"), x.get("code")) == (
        y.get("kind"), y.get("value"), y.get("name"), y.get("code")
    )


def scope():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    base = manifest["base_commit"]
    args = ["git", "diff", "--name-only", base, "HEAD"]
    paths = subprocess.check_output(args, text=True).splitlines()
    assert all(any(path.startswith(p) for p in manifest["allowed_paths"]) for path in paths)
    return base, len(paths)


def validate_release_and_logs():
    releases = rows("releases.csv")
    release_key = {(r["product"], r["version"]): r for r in releases}
    assert len(release_key) == len(releases) == 91
    assert collections.Counter(r["product"] for r in releases) == {"ol": 64, "d3-scale": 27}
    for product, count in (("ol", 64), ("d3-scale", 27)):
        subset = [r for r in releases if r["product"] == product]
        assert sorted(int(r["publish_rank"]) for r in subset) == list(range(1, count + 1))
        assert len({r["tarball_sha256"] for r in subset}) == count
        assert all(r["tarball_verified"] == "True" for r in subset)
    signals = rows("signals.csv")
    assert {(r["product"], r["version"]) for r in signals} == release_key.keys()
    assert all(r["static_status"] == "resolved" and not r["implementation_error"] for r in signals)
    lock = json.loads((ROOT / "replay/locks.json").read_text())
    runs = jsonl("runs.jsonl")
    node = {(r["route"], r["id"]): r for r in runs if r["product"] == "d3-scale"}
    versions = set()
    assert len(node) == 158 and len(lock["matched"]) == 26
    for (route, id_), a in node.items():
        product_release = release_key[("d3-scale", a["version"])]
        assert a["status"] == "observed" and a["exit"] == 0 and a["node"] == "v24.22.1"
        assert a["entry"] == "node_modules/d3-scale/" + product_release["entry_path"]
        assert a["entry_sha256"] == product_release["entry_sha256"]
        root_hash = next(p["tar_sha256"] for p in a["installed"] if p["path"] == "node_modules/d3-scale")
        assert root_hash == product_release["tarball_sha256"]
        assert len(a["outputs"]) == 14
        peer = node[("B" if route == "A" else "A", id_)]
        assert a["outputs"] == peer["outputs"] and a["direct"] == peer["direct"] and a["installed"] == peer["installed"]
        versions.add(a["version"])
    assert len(versions) == 27
    for pair, entry in lock["matched"].items():
        assert not entry["failures"]
        a, b = (node[("A", f"matched-{pair}-{side}")] for side in (1, 2))
        for dep, pin in entry["pins"].items():
            assert a["direct"][dep]["version"] == b["direct"][dep]["version"] == pin
    for pair in rows("evidence/output-comparison.csv"):
        a = node[("A", pair["left_run"])]
        b = node[("A", pair["right_run"])]
        changes = [k for k in a["outputs"] if not same_cell(a["outputs"][k], b["outputs"][k])]
        assert (pair["state"] == "changed") == bool(changes)
        assert set(changes) == {k for k in a["outputs"] if pair[k] == "changed"}
    browser = [r for r in runs if r["product"] == "ol"]
    assert len(browser) == 32 and len({r["version"] for r in browser}) == 4
    for r in browser:
        raw = r["raw_log"].split("/blob/")[-1]
        revision, path = raw.split("/", 1)
        data = subprocess.check_output(["git", "show", f"{revision}:{path}"])
        assert hashlib.sha256(data).hexdigest() == r["raw_sha256"]
        raw_data = json.loads(data)
        assert raw_data["scenario"]["collection"] == r["collection"]
        assert raw_data["scenario"]["filter"] == r["filter"] and raw_data["scenario"]["layers"] == r["layers"]
        final_state = raw_data["steps"][-1]["state"]
        assert all(final_state[k] == v for k, v in r["settled"].items())
        if r["cell"] in {"02", "03"}:
            assert r["geometry_delta"] == [0, 0] and r["center_delta"] == [-64, 36]
    print("release rows 91, Node rows 158 (79 cases x 2), raw map refs 32, output-comparison rows 104")


def validate_counts():
    scores = json.loads((ROOT / "evidence/scores.json").read_text())
    decisions = rows("decisions.csv")
    groups = collections.defaultdict(list)
    for row in decisions:
        key = "|".join(row[k] for k in ("product", "order", "evidence_mode", "cell", "policy"))
        groups[key].append(row)
    assert groups.keys() == scores.keys()
    for key, group in groups.items():
        flags = collections.Counter(r["score"] for r in group)
        summary = scores[key]
        assert len(group) == summary["total"]
        assert all(flags[s] == summary[s] for s in ("TP", "FP", "FN", "TN", "U"))
        assert sum(flags.values()) == summary["total"]
        assert sum(r["alarm"] == "forced" for r in group) == summary["forced"]
        assert sum(summary["bounds_all_unknown_changed"]) == summary["total"]
        assert sum(summary["bounds_all_unknown_same"]) == summary["total"]
    expected = {"ol|publish|source_contract": [(1, 62, 0, 0), (0, 0, 1, 62), (1, 5, 0, 57), (1, 31, 0, 31)],
                "d3-scale|publish|publish-vintage": [(2, 24, 0, 0), (0, 0, 2, 24), (1, 5, 1, 19), (2, 23, 0, 1)]}
    for prefix, metrics in expected.items():
        for name, values in zip("ABCD", metrics):
            assert tuple(scores[f"{prefix}|any|{name}"][key] for key in ("TP", "FP", "FN", "TN")) == values
    count_cells = {"ol": 5, "d3-scale": 15}
    assert len(decisions) == sum(pair_total * count_cells[p] * 16 for p, pair_total in (("ol", 63), ("d3-scale", 26)))
    print(f"decision rows {len(decisions)}, all {len(groups)} score groups recounted")


def validate_costs_and_sources():
    queries, costs = rows("evidence/query-replay.csv"), rows("evidence/costs.csv")
    group_keys = ("product", "scenario", "policy", "mode")
    grouped = collections.defaultdict(list)
    for row in queries:
        grouped[tuple(row[k] for k in group_keys)].append(row)
    assert len(queries) == 840 and len(costs) == len(grouped) == 48
    for cost in costs:
        group = grouped[tuple(cost[k] for k in group_keys)]
        assert int(cost["queries"]) == len(group)
        assert int(cost["preserved"]) == sum(r["answer"] == "preserved" for r in group)
        for k, v in cost.items():
            stage, separator, field = k.partition("_")
            if separator and stage in {"first", "repeat"}:
                slice_ = group[:1] if stage == "first" else group[1:]
                assert int(v) == sum(int(r.get(field) or 0) for r in slice_)
    sources = jsonl("sources.jsonl")
    counted = [r for r in sources if r["counts_unique_minimum"]]
    assert len(sources) == len({r["source_id"] for r in sources}) == 48
    assert sum(r["opened"] for r in sources) == 42
    assert len({r["work_id"] for r in counted}) == len(counted) == 32
    minima = {"d3": 8, "ol": 6, "publication": 4, "map": 3, "transit": 3}
    coverage = collections.Counter(r["category"] for r in counted)
    assert all(coverage[k] >= v for k, v in minima.items())
    assert all(r["opened"] for r in counted)
    for r in sources:
        assert urlparse(r["url"]).scheme == "https"
        assert all(r[field] for field in ("type", "publisher", "version_or_commit", "location", "checked_utc",
                                          "utc_precision", "questions", "claim_ids", "observed", "limits"))
    print("query rows 840; cost rows 48; sources 48/42/32 (candidate/open/eligible)", dict(coverage))


def validate_documents():
    for path in ROOT.rglob("*.md"):
        contents = path.read_text()
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", contents):
            local = link.split("#", 1)[0]
            if local and not urlparse(local).scheme:
                assert (path.parent / local).is_file(), (path, local)
        if path.name in {"RESULT.md", "HANDOFF.md"}:
            ending_table = itertools.takewhile(lambda line: line.startswith("| "), reversed(contents.rstrip().splitlines()))
            assert len(list(ending_table)) == 5
    print("local Markdown targets and three-row ending tables pass")


if __name__ == "__main__":
    validate_release_and_logs()
    validate_counts()
    validate_costs_and_sources()
    validate_documents()
    print("path scope:", *scope())
