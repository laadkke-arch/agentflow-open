"""Normalize the sealed packets without rewriting the source packets."""
from pathlib import Path
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SEALS = {
    "pandoc/packets-pre.json": "6a5dda48cc91acd5b3c88c84f32d8108637029ea",
    "pandoc/controls-pre.json": "0eb5235cd8f0f3d5ec3bfb92022990ee713d7d1c",
    "gdal/packets-pre.json": "0eb5235cd8f0f3d5ec3bfb92022990ee713d7d1c",
    "gdal/controls-pre.json": "0eb5235cd8f0f3d5ec3bfb92022990ee713d7d1c",
}


def dump_csv(name, rows):
    cols = list(dict.fromkeys(k for row in rows for k in row))
    with (ROOT / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k, v in row.items()})


frames = []
packets = []
initial_review = {r['case_id']:r for r in csv.DictReader((ROOT/'initial-version-review.csv').open())} if (ROOT/'initial-version-review.csv').exists() else {}
for stream, repo in [("pandoc", "jgm/pandoc"), ("gdal", "OSGeo/gdal")]:
    metadata_path = ROOT / "streams" / stream / ("current-metadata.json" if stream == "pandoc" else "metadata.json")
    metadata = json.loads(metadata_path.read_text())
    original_frames=json.loads((ROOT / "streams" / stream / "frame.json").read_text())
    extension_path=ROOT/'streams'/stream/'frame-extension.json'
    extension_frames=json.loads(extension_path.read_text()) if extension_path.exists() else []
    for f in original_frames + extension_frames:
        number = f.get("number", f.get("issue_number"))
        meta = next((m for m in metadata if m.get("number", m.get("n")) == number), {})
        frames.append({
            "frame_id": f.get("frame_id", f"{stream.upper()}-F{f.get('rank', f.get('sequence', 0)):02d}"),
            "repository": repo,
            "rank": f.get("rank", f.get("sequence", f.get("ordinal"))),
            "issue_number": f.get("number", f.get("issue_number")),
            "created_utc": f.get("created_at", f.get("created_utc")),
            "original_url": f.get("url", f.get("original_url", f.get("issue_url"))),
            "checked_utc": f.get("checked_utc", f.get("read_utc", meta.get("read_utc", meta.get("checked_utc")))),
            "selected": f.get("selected", f.get("selected_main", False)),
            "case_id": f.get("case_id"),
            "query_terms": f.get("query_terms", f.get("terms", [])),
            "status": f.get("status", f.get("selection_status", "selected_current_reconstruction" if f.get("selected") else "after_first_four_retained")),
            "exclusion_reason": f.get("exclusion_reason", f.get("reason")),
            "initial_status": f.get("initial_status", f.get("initial_version_status")),
            "body_sha256": f.get("body_sha256", f.get("current_body_sha256")),
            "source_ledger": f"streams/{stream}/frame-extension.json" if f in extension_frames else f"streams/{stream}/frame.json",
        })
        if frames[-1]['case_id'] in initial_review:
            frames[-1]['initial_status']='opened_event_verified_after_policy_seal; exact provenance in initial-version-review.csv; prior403 preserved'
    for fn in ["packets-pre.json", "controls-pre.json"]:
        path = ROOT / "streams" / stream / fn
        for p in json.loads(path.read_text()):
            p = dict(p)
            p["repository"] = repo
            p["stratum"] = "natural" if fn == "packets-pre.json" else "constructed"
            p["source_ledger"] = f"streams/{stream}/{fn}"
            p["source_ledger_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            p["seal_commit"] = SEALS[f"{stream}/{fn}"]
            p["normalization_note"] = "Source packet preserved verbatim except normalized stratum and provenance fields; later adjudication does not alter this pre view."
            packets.append(p)

dump_csv("frame.csv", frames)
with (ROOT / "packets.jsonl").open("w", encoding="utf-8") as f:
    for p in packets:
        f.write(json.dumps(p, ensure_ascii=False) + "\n")

# References are explicit annotations of the sealed prose, not newly discovered candidates.
A_LINKS = {
    "PAN-N1": [2], "PAN-N2": [1], "PAN-N3": [2], "PAN-N4": [],
    "PAN-C1": [], "PAN-C2": [2],
    "GDAL-N1": [1], "GDAL-N2": [2], "GDAL-N3": [2], "GDAL-N4": [2],
    "GDAL-C1": [1], "GDAL-C2": [1],
}
C_LINKS = {
    "PAN-N1": [[1], [2], [2]], "PAN-N2": [[1], [2], [1]],
    "PAN-N3": [[1], [2], [2]], "PAN-N4": [[1], [2], [1, 2]],
    "PAN-C1": [[1], [2], [1, 2]], "PAN-C2": [[2], [2], [2]],
    "GDAL-N1": [[1], [2], [1]], "GDAL-N2": [[1], [2], [2]],
    "GDAL-N3": [[1], [2], [2]], "GDAL-N4": [[1], [2], [2]],
    "GDAL-C1": [[1], [2], [1, 2]], "GDAL-C2": [[1], [1, 2], [1]],
}
policies = []
for p in packets:
    known = p.get("known_field_value", p.get("disclosed_value"))
    for policy in ["A", "B", "C"]:
        for idx, branch in enumerate(["value1", "value2", "no_answer"]):
            value = p["values"][idx] if idx < 2 else None
            key = policy if policy != "C" else ["C_value1", "C_value2", "C_none"][idx]
            ids = A_LINKS[p["case_id"]] if policy == "A" else [1, 2] if policy == "B" else C_LINKS[p["case_id"]][idx]
            urls = [p[f"candidate{i}"]["url"] for i in ids]
            policies.append({
                "row_id": f"{p['case_id']}-{policy}-{branch}",
                "case_id": p["case_id"], "stratum": p["stratum"],
                "policy": policy, "response_branch": branch, "scenario_value": value or "unobserved",
                "answer": p[key], "question": p["question"] if policy == "C" else "not_asked",
                "question_rounds_planned": int(policy == "C"),
                "completed_reply_rounds_in_scenario": int(policy == "C" and branch != "no_answer"),
                "scenario_kind": "hypothetical_value" if idx < 2 else "no_new_reply",
                "candidate_refs": ids, "answer_urls": urls,
                "displayed_link_references": len(urls), "distinct_answer_urls": len(set(urls)),
                "distinct_answer_documents": len(set(x.split("#")[0] for x in urls)),
                "pre_known_field_value": known or "unknown",
                "conflicts_with_pre_known_value": bool(known and value and known != value),
                "literal_lang_retention_ambiguity": p["case_id"] == "PAN-N2",
                "actual_user_response_to_our_policy": "not_measured_no_contact",
                "human_time": "not_measured", "response_probability": "not_measured",
                "seal_commit": p["seal_commit"], "source_ledger": p["source_ledger"],
            })
dump_csv("policies.csv", policies)
print(json.dumps({"frames": len(frames), "packets": len(packets), "policies": len(policies)}, ensure_ascii=False))
