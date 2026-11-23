"""Check and copy the AF-RES-060 comparison frame without its outcome fields."""

import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
PARENT = "docs/workstreams/research/AF-RES-060"
PIN = "ccde193ec33f68fea5eaef1cc6f6cea803e1823f"
HANDOFF = "87bd0362f7adce5a5e002036dc71a6fc93eeead1"
DIGESTS = {
    "RESULT.md": "a9ef912fcc66cbe4619a0801de388f6329af230de57e12f578ed01723485fcb7",
    "features.csv": "3ae6f5bab20cf121ecf9197aa38f4f666734d3a5d2a7a53e7022c7d160739dd7",
    "evidence/next-checks/js6-fixtures.json": "293a25b2112d53e36cc327af70d395b14a625a2cfb5c84f1b154e9d41bea2db7",
    "evidence/next-checks/js6-probe.cjs": "3035830ab16431fea5adf0f2c0423c3991328735ea3b700eb0351b388b7d4033",
    "matches.csv": "947e6a476cdbe02dfa5fb0d9085277e442be12f5b6c1c9e99293ac762f79508d",
    "paths.csv": "805fc4d0a3d329319c3c29166980771f97d2dd0eceb38ff0eca68816ae187d12",
    "requirements.json": "607bd986999cac6a9adbef7b4a0283026b5e627950a6dfe108fc28a343c1067e",
    "slots.csv": "81354b1b74ffe51202d8060dc19a367cdf0272cd93a31ceca4dafc793f059c40",
}


def read(pin, path):
    return subprocess.check_output(["git", "show", f"{pin}:{PARENT}/{path}"], cwd=HERE)


def csv_rows(data):
    stream = csv.DictReader(io.StringIO(data.decode()))
    rows = []
    for row in stream:
        rows.append((stream.line_num, row))
    return rows


def emit_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    inputs = {key: read(PIN, key) for key in DIGESTS}
    digest = {key: hashlib.sha256(val).hexdigest() for key, val in inputs.items()}
    if digest != DIGESTS:
        raise SystemExit(f"Changed inherited bytes: {digest}")
    handoff = read(HANDOFF, "HANDOFF.md")
    requirements = json.loads(inputs["requirements.json"])
    cases = {row["case_id"]: row for row in requirements}
    matches = {
        row["case_id"]: (line, row)
        for line, row in csv_rows(inputs["matches.csv"])
        if (row["query"], row["fields"]) == ("V", "F1")
    }
    features = {row["catalog_id"]: (line, row) for line, row in csv_rows(inputs["features.csv"])}
    slots = []
    for line, row in csv_rows(inputs["slots.csv"]):
        if (row["query"], row["fields"]) != ("V", "F1"):
            continue
        case = row["case_id"]
        number = int(row["slot"])
        match_line, match = matches[case]
        ordered = json.loads(match["all_matches_json"])
        item = ordered[number - 1] if number <= len(ordered) else None
        assert row["catalog_id"] == (item["catalog_id"] if item else "")
        projection = {
            "slot_id": row["slot_id"], "case_id": case, "layer": row["layer"],
            "slot": number, "catalog_id": row["catalog_id"], "posted_rank": row["posted_rank"],
            "published_url": row["destination_url"], "empty_reason": row["empty_reason"],
            "af060_slots_line": line, "af060_matches_line": match_line,
            "af060_features_line": "", "provider_title": "", "editor_fixed_url": "",
            "implementation_sha": "", "inherited_release": "", "version_status": "",
            "role": "", "engine_as_inherited": "", "feature_hits": "", "feature_origins": "",
        }
        assert row["layer"] == cases[case]["layer"] == match["layer"]
        if item:
            feature_line, feature = features[item["catalog_id"]]
            assert int(row["posted_rank"]) == item["posted_rank"] == int(feature["posted_rank"])
            assert row["destination_url"] == item["url"] == feature["original_destination_url"]
            assert row["empty_reason"] == ""
            hits = list(dict.fromkeys(hit["field_value"] for hit in item["hits"] if hit["field_kind"] == "F1"))
            origins = [
                {key: origin[key] for key in (
                    "term", "source_id", "source_url", "window_file", "window_line", "anchor",
                    "raw_eligible_occurrence_line", "eligible_needle", "eligible_structure_tags"
                ) if key in origin}
                for origin in json.loads(feature["feature_evidence_json"]) if origin["term"] in hits
            ]
            assert {origin["term"] for origin in origins} == set(hits)
            projection.update(
                af060_features_line=feature_line, provider_title=feature["title"],
                editor_fixed_url=feature["editor_fixed_url"], implementation_sha=feature["implementation_sha"],
                inherited_release=feature["implementation_version"], version_status=feature["version_status"],
                role=feature["role"], engine_as_inherited=feature["engine_lineage"],
                feature_hits=json.dumps(hits, ensure_ascii=False),
                feature_origins=json.dumps(origins, ensure_ascii=False),
            )
        else:
            assert row["posted_rank"] == row["destination_url"] == ""
            assert row["empty_reason"] == ("matched_pool_exhausted" if ordered else "observed_no_match")
        slots.append(projection)

    assert list(matches) == list(cases)
    assert [(s["case_id"], s["slot"]) for s in slots] == [(key, i) for key in cases for i in range(1, 4)]
    filled = [s for s in slots if s["catalog_id"]]
    assert len(cases) == 12 and sum(c["layer"] == "existing_tuning" for c in requirements) == 8
    assert len(slots) == 36 and len(filled) == len({(s["case_id"], s["catalog_id"]) for s in filled}) == 11
    assert sum(s["empty_reason"] == "observed_no_match" for s in slots) == 18
    assert sum(s["empty_reason"] == "matched_pool_exhausted" for s in slots) == 7
    emit_csv(HERE / "slots.csv", slots)
    for source in ("evidence/next-checks/js6-fixtures.json", "evidence/next-checks/js6-probe.cjs"):
        (HERE / "fixtures" / Path(source).name).write_bytes(inputs[source])
    receipt = {
        "result_sha": PIN, "handoff_sha": HANDOFF, "handoff_sha256": hashlib.sha256(handoff).hexdigest(),
        "files_sha256": digest, "requirements": len(cases), "slots": len(slots),
        "filled": len(filled), "observed_no_match": 18, "matched_pool_exhausted": 7,
        "cases_with_candidates": len({s["case_id"] for s in filled}),
        "scheduled_ab": len(filled) * 2, "scheduled_placebo": len(filled),
    }
    (HERE / "evidence" / "input-check.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
