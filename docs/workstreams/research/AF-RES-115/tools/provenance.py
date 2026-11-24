"""Check the two external datasets and perform targeted post-replay counterchecks."""
import argparse
import csv
import json
from pathlib import Path

from compare import infer, node_guard, rows_in
from frame import fetch
from materialize import cached
from replay import runner_envelope
from structure import digest, jsonl

HERE = Path(__file__).resolve().parent.parent
NGA = "9ad7adae7bb0ade0b14c07ca454a4f5eaf2fe15c"
SAKAY = "b7394ccd0c22e7fcc18cc6b53baa1200e99e8a87"
GITHUB_RAW = "https://raw.githubusercontent.com"
EXTERNAL = {
    "nga-dict": f"{GITHUB_RAW}/NationalGalleryOfArt/opendata/{NGA}/data/objects.csv",
    "sakay-routes.txt": f"{GITHUB_RAW}/sakayph/gtfs/{SAKAY}/routes.txt",
    "sakay-trips.txt": f"{GITHUB_RAW}/sakayph/gtfs/{SAKAY}/trips.txt",
    "sakay-feed_info.txt": f"{GITHUB_RAW}/sakayph/gtfs/{SAKAY}/feed_info.txt",
}


def read_csv(path, fields, predicate):
    csv.field_size_limit(5_000_000)
    with path.open(newline="", encoding="utf-8") as stream:
        return [{"record": index, **{k: row[k] for k in fields}}
                for index, row in enumerate(csv.DictReader(stream), 2) if predicate(row)]


def two_domains(store):
    store.mkdir(exist_ok=True, parents=True)
    sources = {}
    for key, origin in EXTERNAL.items():
        path = store / key
        if not path.exists():
            _, data, _ = fetch(origin)
            path.write_bytes(data)
        sources[key] = {"raw": origin, "sha256": digest(path.read_bytes())}
    museum = read_csv(store / "nga-dict", ["objectid", "accessionnum", "parentid", "isvirtual"],
                      lambda r: r["objectid"] == "206122" or r["parentid"] == "206122")
    route = read_csv(store / "sakay-routes.txt", ["route_id", "route_short_name", "agency_id"],
                     lambda r: r["route_id"] == "ROUTE_880801")
    trips = read_csv(store / "sakay-trips.txt", ["route_id", "service_id", "trip_id", "trip_headsign"],
                     lambda r: r["trip_id"] in {"880815", "882129"})
    info = read_csv(store / "sakay-feed_info.txt", ["feed_publisher_name"], lambda r: True)
    assert {r["objectid"] for r in museum} == {"206122", "2", "3", "4"}
    assert {r["parentid"] for r in museum} == {"", "206122"}
    assert next(r for r in museum if r["objectid"] == "206122")["isvirtual"] == "1"
    assert len(route) == 1 and len(trips) == 2
    assert {r["route_id"] for r in trips} == {route[0]["route_id"]}
    assert info[0]["feed_publisher_name"] == "Sakay.ph"
    return {"sources": sources, "NGA-206122": museum, "route": route, "trips": trips, "feed": info}


def patch_check(cache):
    data = next(a for a in jsonl(HERE / "inputs.jsonl") if a["id"] == "M60")
    original = cached(cache, data["blob_sha256"])
    fixed = cached(cache, data["fixed_blob_sha256"])
    old, new = b"10,20,21,22,23", b"19,20,21,22,23"
    assert original.count(old) == 1 and original.replace(old, new, 1) == fixed
    changed = [i for i, (a, b) in enumerate(zip(original, fixed, strict=True)) if a != b]
    assert len(changed) == 1
    return {"before": data["blob_sha256"], "after": data["fixed_blob_sha256"],
            "changed_byte_offsets_zero_based": changed, "n_bytes": len(original),
            "unaltered_offsets": len(original) - len(changed),
            "changed_path": "/museScore/Score/Staff[1]/TBox[1]/Text[1]/text",
            "app_execution": "unknown"}


def omission_checks():
    views = {r["input_id"]: runner_envelope(r) for r in jsonl(HERE / "views.jsonl")
             if r["view"] == "C" and r["length_layer"] == "budget"}
    candidates = json.loads((HERE / "candidate-conditions.json").read_text())
    v = views["CM-r"]
    records = rows_in(v)
    request = infer(v["text"][:v["request_chars"]])
    seed = next(r for r in records if r["seed"])
    rule = candidates["instrument"][0]
    named = node_guard(rule, request, seed, records)
    without_name = node_guard(rule, {k: x for k, x in request.items() if k != "label"}, seed, records)
    assert named[0] == "refute" and without_name[:3] == ("support", "direction-and-ref-confirmed", ["IOb"])

    v = views["CE-d"]
    records = rows_in(v)
    seeds = [r for r in records if r["seed"]]
    assert len(seeds) == 2
    pick_first = node_guard(candidates["bind"][0], infer(v["text"][:v["request_chars"]]), seeds[0], records)
    assert pick_first[:3] == ("support", "direction-and-ref-confirmed", ["e-label"])

    v = views["CE"]
    records = rows_in(v)
    request = infer(v["text"][:v["request_chars"]])
    seed = next(r for r in records if r["seed"])
    for r in records:
        if r["type"] == "arrow":
            for edge in r["refs"]:
                edge["field"] = {"startBinding.elementId":"endBinding.elementId",
                                 "endBinding.elementId":"startBinding.elementId"}[edge["field"]]
    strict = node_guard(candidates["bind"][0], request, seed, records)
    relaxed = node_guard({**candidates["bind"][0], "field": "startBinding.elementId"}, request, seed, records)
    assert strict[0] == "hold" and relaxed[0] == "support"
    return {"CM-r/omitted-requested-name":{"literal_guard":named[0],"without_guard":without_name[2]},
            "CE-d/omitted-ambiguity":{"actual_seeds":[r["id"] for r in seeds],"first_only":pick_first[2]},
            "CE/reversed-ends-untyped-association":{"strict_end_guard":strict[0],"accept_start_as_end":relaxed[2]}}


def validate_musicxml(schema, inputs, cache):
    from lxml import etree

    class Local(etree.Resolver):
        def resolve(self, url, pubid, context):
            filename = url.rsplit("/", 1)[-1]
            if filename in {"xml.xsd", "xlink.xsd"}:
                return self.resolve_filename(str(schema / filename), context)
            return None

    parser = etree.XMLParser(no_network=True, resolve_entities=False)
    parser.resolvers.add(Local())
    xsd = etree.XMLSchema(etree.parse(str(schema / "musicxml.xsd"), parser))
    valid = {}
    for item in jsonl(inputs):
        if item.get("format") == "musicxml":
            data = cached(cache, item["blob_sha256"])
            xsd.assertValid(etree.fromstring(data, parser))
            valid[item["id"]] = {"xsd": "valid", "artifact": item["blob_sha256"]}
    return {"validator": f"lxml {'.'.join(map(str, etree.LXML_VERSION[:3]))}",
            "schema_sha256": digest((schema / "musicxml.xsd").read_bytes()), "cases": valid}


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("cache", type=Path)
    cli.add_argument("external_cache", type=Path)
    cli.add_argument("expanded_inputs", type=Path)
    cli.add_argument("schema", type=Path)
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    output = {"external": two_domains(args.external_cache), "repeat_bytes": patch_check(args.cache),
              "omissions": omission_checks(),
              "musicxml_validation": validate_musicxml(args.schema.resolve(), args.expanded_inputs, args.cache)}
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n")
    print("NGA and Sakay joins, exact upstream byte patch, omissions and 3 pinned XSD checks passed.")


if __name__ == "__main__":
    main()
