"""Audit public stimuli/exposure schema; never threshold ratings into acceptance.

Run from repository root:
python -B docs/workstreams/research/AF-RES-062/streams/a/audit_transparent_cis.py --fetch
Only aggregate output is written; public worker rows remain in ignored .cache.
"""
import argparse
import ast
import collections
import csv
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
SHA = "065ae48c802e5fcaf9f4c202fad6bfb0aaf0650d"
REPO = "https://raw.githubusercontent.com/iai-group/sigir2024-transparentCIS/"
FILES = {
    "raw": "results/user_study_output/mturk_output.csv",
    "stimuli": "data/input/input_data.csv",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    cache = ROOT / ".cache" / "transparent"
    cache.mkdir(parents=True, exist_ok=True)
    paths = {k: cache / v.replace("/", "__") for k, v in FILES.items()}
    if args.fetch:
        for key, path in paths.items():
            path.write_bytes(urllib.request.urlopen(REPO + SHA + "/" + FILES[key], timeout=45).read())
    with paths["raw"].open() as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        headers = reader.fieldnames
    with paths["stimuli"].open() as stream:
        stimuli = list(csv.DictReader(stream))
    grouped = collections.defaultdict(list)
    for row in rows:
        cells = ast.literal_eval(row["Input.experimental_cond"])
        assert len(cells) == 10 and len(set(cells)) == 1
        grouped[cells[0]].append(row)
    response_versions = {}
    output = {
        "repo_sha": SHA,
        "inputs": {k: {"url": REPO + SHA + "/" + FILES[k], "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for k, p in paths.items()},
        "unit": "retained worker-HIT; each contains 10 item ratings",
        "retained_workers": len(rows),
        "unique_retained_workers": len({row["WorkerId"] for row in rows}),
        "conditions": {},
        "same_answer_text_comparisons": {},
        "acceptance_endpoint": "해당 없음 — no final chosen-answer variable; four-point correctness/factuality ratings must not be thresholded",
        "assigned_all_273_by_condition": "미확인 — public file contains retained160 only;113 rejected submissions absent",
        "exposure_limits": "p_clicked_details is a raw expandable-source label with timestamp; p_clicked_links mixes generic Sources labels with URLs. Client event dictionary and source-reading/scroll/dwell are not published in inspected tree. Nonempty counts are raw field counts, not confirmed reading.",
    }
    for condition, group in grouped.items():
        versions = collections.defaultdict(set)
        all_ids = []
        for row in group:
            ids = ast.literal_eval(row["Input.query_id"])
            all_ids.extend(ids)
            for qid, answer in zip(ids, ast.literal_eval(row["Input.response"])):
                versions[qid].add(answer)
        response_versions[condition] = versions
        output["conditions"][condition] = {
            "retained_workers": len(group),
            "retained_item_ratings": len(all_ids),
            "item_id_counts": dict(sorted(collections.Counter(all_ids).items())),
            "distinct_answer_versions_per_item": {k: len(v) for k, v in sorted(versions.items())},
            "workers_with_nonempty_details_field": sum(bool(x["Answer.p_clicked_details"]) for x in group),
            "workers_with_nonempty_links_field": sum(bool(x["Answer.p_clicked_links"]) for x in group),
            "raw_correctness_boolean_tokens": sorted({row[f"Answer.correctness_{qid}.option_{option}"] for row in group for qid in range(1, 11) for option in range(1, 5)}),
            "raw_correctness_single_option_per_item": all(sum(row[f"Answer.correctness_{qid}.option_{option}"].strip().upper() == "TRUE" for option in range(1, 5)) == 1 for row in group for qid in range(1, 11)),
        }
    for condition, reference in [("EC1", "EC9"), ("EC3", "EC10"), ("EC2", "EC9"), ("EC4", "EC10")]:
        matches = [qid for qid in range(1, 11) if response_versions[condition][qid] == response_versions[reference][qid]]
        output["same_answer_text_comparisons"][condition + "_vs_" + reference] = {"identical_item_ids": matches, "denominator_items": 10}
    output["raw_join_fields"] = ["WorkerId", "Input.experimental_cond", "Input.query_id", "Input.response", "Input.sources", "Input.source_links", "Answer.correctness_{id}.option_{1..4}", "Answer.factuality_{id}.option_{1..4}", "Answer.p_clicked_details", "Answer.p_clicked_links"]
    output["stimuli_ids"] = [row["Id"] for row in stimuli]
    assert output["retained_workers"] == output["unique_retained_workers"] == 160
    assert all(v["retained_workers"] == 16 and v["retained_item_ratings"] == 160 for v in output["conditions"].values())
    assert all(v["raw_correctness_single_option_per_item"] for v in output["conditions"].values())
    (ROOT / "transparent-cis-audit.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"retained_workers": len(rows), "conditions": len(grouped), "item_ratings": sum(x["retained_item_ratings"] for x in output["conditions"].values()), "acceptance_cells_recovered": 0, "status": "schema/stimulus audit passed"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
