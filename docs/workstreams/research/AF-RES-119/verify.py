"""Independently recompute archive, view, render and source evidence from saved bytes."""
import argparse
from collections import Counter
import csv
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import re
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent


def rows(file):
    return [json.loads(line) for line in (ROOT / file).read_bytes().split(b"\n") if line]


def checksum(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(file):
    return checksum(file.read_bytes())


def csv_rows(file):
    with (ROOT / file).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def compact(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def check_archive():
    frame = csv_rows("frame.csv")
    opening = rows("evidence/opening-frame.jsonl")
    assert len(frame) == len(opening)
    tally = {}
    bodies = {}
    for row, archived in zip(frame, opening, strict=True):
        assert (row["project"], int(row["number"])) == (archived["project"], archived["number"])
        assert row["created_utc"] == archived["created"]
        body = archived["body"]
        if body is None:
            assert row["body_sha256"] == "" and row["state"] in ("pull-request", "null-body")
            continue
        data = body.encode()
        assert len(data) == int(row["body_bytes"]) and checksum(data) == row["body_sha256"]
        case = row["project"] + row["number"]
        bodies[case] = data
        for block in json.loads(row["specs"]):
            assert checksum(data[block["start"]:block["end"]]) == block["sha256"]
            if "fence_start" in block:
                assert checksum(data[block["fence_start"]:block["fence_end"]]) == block["fence_sha256"]
    for project in ("V", "M"):
        selected = [r for r in frame if r["project"] == project]
        assert [(r["created_utc"], int(r["number"])) for r in selected] == sorted(
            (r["created_utc"], int(r["number"])) for r in selected
        )
        ranked = [r for r in selected if r["rank"]]
        assert [int(r["rank"]) for r in ranked] == list(range(1, 42))
        qualified = [r for r in ranked if r["selection"] == "selected"]
        assert len(qualified) == 3 and qualified == ranked[:3]
        tally[project] = {
            "api_rows_through_boundary": len(selected),
            "pr_excluded": sum(r["state"] == "pull-request" for r in selected),
            "issues": sum(r["state"] != "pull-request" for r in selected),
            "body_present": sum(bool(r["body_sha256"]) for r in selected),
            "code_ranks": len(ranked),
            "first_boundary": ranked[39]["number"],
            "excluded_boundary": ranked[40]["number"],
            "selected": [r["number"] for r in qualified],
        }
    cases = {r["id"]: r for r in rows("cases.jsonl")}
    for id, case in cases.items():
        raw = bodies[id]
        assert checksum(raw) == case["opening_body_sha256"]
        for t in case["request_spans"]:
            assert t["text"].encode() == raw[t["start"]:t["end"]]
        for spec in case["specs"]:
            original = (ROOT / spec["file"]).read_bytes()
            assert original == raw[spec["start"]:spec["end"]]
            assert checksum(original) == spec["sha256"]
    return tally, cases


def check_views(cases):
    by_cell = {}
    outcomes = {}
    exact_changes = []
    view_rows = rows("views.jsonl")
    choices = rows("choices.jsonl")
    truth = {t["id"]: t for t in csv_rows("truth.csv")}
    assert set(truth) == set(cases)
    for view, choice in zip(view_rows, choices, strict=True):
        cell = tuple(view[k] for k in ("id", "view", "budget"))
        assert cell == tuple(choice[k] for k in ("id", "view", "budget"))
        packet = view["input"]
        assert set(packet) == {"request", "options", "structure"}
        assert checksum((compact(packet) + "\n").encode()) == choice["packet_sha256"]
        rendered = packet["structure"]
        assert len(rendered) == view["structure_characters"] <= view["structure_cap"] <= 1200
        assert len(packet["request"]) + len(compact(packet["options"])) + len(rendered) == view["total_characters"]
        paths = [json.loads(l)["path"] for l in rendered.split("\n")[:-1]]
        assert paths == choice["visible_paths"] and len(paths) <= 4
        assert set(choice["basis_paths"]) <= set(paths)
        assert all(link["url"] == packet["options"][link["id"]]["url"] for link in choice["links"])
        if choice["result"] == "정확":
            assert {l["id"] for l in choice["links"]} <= set(json.loads(truth[view["id"]]["expected_links"]))
        by_cell[cell] = (view, choice)
        if choice["sample_layer"] == "natural":
            key = view["budget"] + ":" + view["view"]
            outcomes.setdefault(key, Counter())[choice["result"]] += 1
            assert "excluded" in choice["main_effect"]
    for id in cases:
        a = by_cell[id, "A", "cap"][0]
        b, c = (by_cell[id, v, "cap"][0] for v in "BC")
        bm, cm = (by_cell[id, v, "matched"][0] for v in "BC")
        assert bm["structure_cap"] == cm["structure_cap"] == min(b["structure_characters"], c["structure_characters"])
        assert bm["total_characters"] == cm["total_characters"]
        assert b["start_candidates"] == c["start_candidates"]
        for row in (b, c, bm, cm):
            assert row["input"]["options"] == a["input"]["options"]
            assert row["input"]["request"] == a["input"]["request"]
        if id in cases and cases[id]["sample_layer"] == "natural":
            if by_cell[id, "B", "matched"][1]["result"] != by_cell[id, "C", "matched"][1]["result"]:
                exact_changes.append(id)
    replays = json.loads((ROOT / "evidence/view-replays.json").read_text())
    assert replays[0]["output_sha256"] == replays[1]["output_sha256"]
    return {"serialized_cells": len(view_rows), "natural_cap_cells": 18, "natural_matched_cells": 12,
            "blind_main_effect_cells": 0, "same_worker_automated_tally": outcomes,
            "matched_B_C_status_changes": exact_changes}


def svg(run, name=None):
    name = name or run["svg_record_source"]
    return ElementTree.parse(ROOT / run["raw_receipt_dir"] / name).getroot()


def css_class(node, token):
    return token in node.get("class", "").split()


def texts(tree, class_name=None):
    return ["".join(node.itertext()).strip() for node in tree.iter()
            if node.tag.rsplit("}", 1)[-1] == "text" and (class_name is None or css_class(node, class_name))]


def svg_sha(run):
    return run["outputs"].get("output.svg", {}).get("sha256")


def browser(run):
    return json.loads((ROOT / run["raw_receipt_dir"] / "browser-observations.json").read_text())


def check_render():
    runs = rows("runs.jsonl")
    inputs = json.loads((ROOT / "fixtures" / "operations.json").read_text())
    assert len(runs) == 2 * len(inputs) == 66
    input_index = {(i["id"], i["variant"]): i for i in inputs}
    pairs = {}
    layers = {}
    artifact_count = 0
    for run in runs:
        key = run["id"], run["variant"]
        input = input_index[key]
        assert run["sha256"] == input["sha256"] == sha_file(ROOT / run["file"])
        for name, stamp in run["outputs"].items():
            path = ROOT / run["raw_receipt_dir"] / name
            assert sha_file(path) == stamp["sha256"] and path.stat().st_size == stamp["bytes"], path
            artifact_count += 1
        group = layers.setdefault(run["layer"], Counter())
        group["attempts"] += 1
        group["valid_svg"] += int(run["parsed_svg"])
        pairs.setdefault(key, {})[run["iteration"]] = run
    data = ROOT / "fixtures/data/data/seattle-weather.csv"
    assert len(data.read_bytes().splitlines()) == 1462
    assert sha_file(data) == "0845078a290b48e3149ab8639966824110a251db4e06fc144c06ebb534af23be"
    valid = 0
    for pair in pairs.values():
        one, two = pair[1], pair[2]
        assert one["parsed_svg"] == two["parsed_svg"]
        if one["parsed_svg"]:
            valid += 1
            assert svg_sha(one) == svg_sha(two)
            assert one["normalized_svg_sha256"] == two["normalized_svg_sha256"]
        else:
            assert not svg_sha(one) and not svg_sha(two)
            assert one["commands"][0]["stderr"].splitlines()[0] == two["commands"][0]["stderr"].splitlines()[0]
        if "active.svg" in one["outputs"]:
            assert one["outputs"]["active.svg"] == two["outputs"]["active.svg"]
    r = {key: pair[1] for key, pair in pairs.items()}

    def marks(run, filename=None):
        return [elem for elem in svg(run, filename).iter()
                if elem.get("aria-roledescription") == "bar"]

    def named_axis(run):
        return [t for t in texts(svg(run)) if t in set("ABCDE")]

    sort = {kind:named_axis(r["V8627", kind]) for kind in ("base","local","shared")}
    assert sort == {"base":list("ABCDE"), "local":list("ABCDE"), "shared":list("DAEBC")}
    assert svg_sha(r["V8627", "base"]) == svg_sha(r["V8627", "local"])
    fills = {k: Counter(m.get("fill") for m in marks(r["V8628", k], "active.svg"))
             for k in ("base", "local", "shared")}
    assert fills["base"]["lightgray"] == 49 and fills["local"]["steelblue"] == 49
    assert fills["base"] == fills["shared"]
    assert len({svg_sha(r["V8628", k]) for k in ("base", "local", "shared")}) == 1
    signals = {kind: [s["name"] for s in json.loads(
        (ROOT / r["V8628", kind]["raw_receipt_dir"] / "output.vg.json").read_text()
    )["signals"] if "_translate_" in s["name"]] for kind in ("base","local","shared")}
    assert len(signals["base"]) == len(signals["local"]) == 2 and not signals["shared"]

    pie = {}
    arcs = {}
    for kind in ("base","local","shared"):
        run = r["M3987", kind]
        source = (ROOT / run["file"]).read_text()
        counts = [Decimal(n) for n in re.findall(r'^\s*"[^"]+"\s*:\s*(\d+)', source, flags=re.M)]
        values = [int((Decimal(100) * n / sum(counts)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)) for n in counts]
        graph = svg(run)
        assert [f"{n}%" for n in values] == texts(graph, "slice")
        pie[kind] = {"counts": list(map(int, counts)), "display": values, "total": sum(values)}
        arcs[kind] = [n.get("d") for n in graph.iter() if css_class(n, "pieCircle")]
    assert pie["base"]["total"] == pie["shared"]["total"] == 101 and pie["local"]["total"] == 100
    assert arcs["base"] == arcs["shared"] and all(a != b for a, b in zip(arcs["base"], arcs["local"], strict=True))

    seq = {kind: [(n["text"], n["visibility"]) for n in browser(r["M3982", kind])
                  if "labelText" in n["class"].split()] for kind in ("base","local","shared")}
    assert seq["base"] == seq["local"] == [("alt", "visible"), ("opt", "visible")]
    assert seq["shared"] == [("alt", "hidden"), ("opt", "hidden")]
    assert "[If sick]" in texts(svg(r["M3982", "local"]), "loopText")
    assert not r["M3981", "base"]["parsed_svg"] and r["M3981", "local"]["parsed_svg"] and not r["M3981", "shared"]["parsed_svg"]
    assert "reading 'id'" in r["M3981", "base"]["commands"][0]["stderr"]
    groups = {
        kind:{n["id"]: n["box"] for n in browser(r["M3994", kind]) if css_class(n, "cluster")}
        for kind in ("base","local","shared")
    }
    assert groups["base"] == groups["local"] and groups["shared"] != groups["base"]
    assert set(groups["base"]) == {"AG", "MG"}
    homonyms = {kind:[n["fill"] for n in browser(r["C01",kind]) if n["tag"] == "rect"]
                for kind in ("base","local","shared")}
    assert homonyms["base"] == homonyms["local"]
    assert homonyms["base"][:2] == ["rgb(134, 239, 172)"] * 2
    assert homonyms["shared"][:2] == ["rgb(251, 191, 36)"] * 2
    assert homonyms["base"][-1] == homonyms["shared"][-1]
    assert svg_sha(r["C02","base"]) == svg_sha(r["C02","local"]) != svg_sha(r["C02","shared"])
    control_v = {}
    for kind in ("base","local","shared"):
        graph = svg(r["C03",kind])
        control_v[kind] = {style: Counter(n.get("fill") for n in graph.iter()
                                         if n.get("aria-roledescription") == role)
                           for style, role in (("bars", "bar"), ("points", "point"))}
    assert control_v == {
        "base":{"bars":{"#2563eb":3},"points":{"#e11d48":3}},
        "local":{"bars":{"#2563eb":3},"points":{"#a21caf":3}},
        "shared":{"bars":{"#15803d":3},"points":{"#e11d48":3}},
    }
    return {
        "attempts": len(runs), "raw_digest_checks": artifact_count,
        "valid_svg": 2 * valid, "matching_svg_pairs": valid,
        "per_layer": layers, "V8627_axis": sort, "V8628_active_bar_fills": fills,
        "V8628_translate_signals": signals, "M3982_keyword_visibility": seq,
        "M3987_pie": pie, "M3994_group_geometry": groups, "C01_rect_fills": homonyms, "C03_fills": control_v,
    }


def check_sources():
    sources = rows("sources.jsonl")
    assert len({r["source_id"] for r in sources}) == len(sources)
    keep = [r for r in sources if r["counted"]]
    assert len({r["origin_or_case_id"] for r in keep}) == len(keep)
    assert all(r["access"] == "read" and r["landed_url"] for r in keep)
    minimum = {"natural": 6, "definition": 8, "regression": 6, "library": 2, "typography": 2}
    distribution = Counter(r["category"] for r in keep)
    assert all(distribution[k] >= v for k, v in minimum.items())
    return {
        "source_rows": len(sources), "candidate_original_urls": len({r["original_url"] for r in sources}),
        "opened_rows": sum(r["access"] in ("read","machine-screened") and r.get("fetched_opening_body",True) for r in sources),
        "by_access": Counter(r["access"] for r in sources),
        "manually_read_primary_unique": len(keep), "primary_by_category": distribution,
    }


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--json", type=Path, help="write the continuous verification receipt")
    args = parser.parse_args()
    frame, cases = check_archive()
    result = {"frame":frame, "views":check_views(cases), "render":check_render(), "sources":check_sources()}
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        args.json.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
