"""Materialize the pre-followup candidate freeze without adding new evidence."""
from pathlib import Path
import csv
import json
from assemble_initial import write_csv, normalize_source

ROOT = Path(__file__).resolve().parent


def main():
    initial = {r["case_id"]: r for r in csv.DictReader((ROOT / "initial.csv").open())}
    rows = []
    for tag in ("imagemagick", "typst"):
        part = json.loads((ROOT / "evidence" / tag / "candidate-part.json").read_text())
        for c in part:
            im = tag == "imagemagick"
            blank = c["blank"]
            a = c.get("a", {})
            b = c.get("b", {})
            origins = c.get("origin_urls", c.get("evidence", []))
            rows.append({
                "case_id": c["case_id"], "candidate_id": c["candidate_id"],
                "question_id": initial[c["case_id"]]["question_id"],
                "original_rank": c["original_rank"], "blank": blank,
                "blank_reason": c.get("blank_reason", ""),
                "first_proposal_utc": c.get("first_proposal_utc", c.get("proposal_utc")),
                "original_proposal_url": origins[0].get("url") if im and not blank else c.get("original_proposal_url"),
                "original_fixed_url": origins[0].get("revision_url") if im and not blank else c.get("original_fixed_url"),
                "original_links": c.get("original_links", []),
                "other_links_in_source": c.get("other_links_in_source", []),
                "operation": c.get("operation"),
                "product": c.get("candidate_product", c.get("product")),
                "engine_name": c.get("engine_name"), "wrapper_name": c.get("wrapper_name"),
                "product_match_level": c.get("product_match_level", "named_product"),
                "same_product_as_known_actual_use": c.get("same_product", c.get("same_product_as_actual_use")),
                "product_identity_proof": c.get("same_product_proof", c.get("product_identity_proof")),
                "same_operation_as_actual_attempt": c.get("same_operation", c.get("same_operation_as_actual_attempt")),
                "operation_identity_proof": c.get("same_operation_proof", c.get("operation_identity_proof")),
                "difference_from_attempt": c.get("difference_from_attempt", c.get("difference_from_initial")),
                "identity_limits": c.get("identity_edge_cases", c.get("identity_unknowns", [])),
                "A_decision": ("blank" if blank else ("exclude" if a["excluded"] else "keep")) if im else c["A_decision"],
                "A_reason": a.get("reason") if im else c["A_reason"] if not blank else c["blank_reason"],
                "B_decision": ("blank" if blank else ("exclude" if b["excluded"] else "keep")) if im else c["B_decision"],
                "B_reason": b.get("reason") if im else c["B_reason"] if not blank else c["blank_reason"],
                "A_returned_position": a.get("returned_rank") if im else c["A_returned_position"],
                "B_returned_position": b.get("returned_rank") if im else c["B_returned_position"],
                "A_rank_shift": a.get("rank_shift") if im else c["A_rank_shift"],
                "B_rank_shift": b.get("rank_shift") if im else c["B_rank_shift"],
                "judged_utc": c["judged_utc"],
                "origin_evidence": origins,
                "related_or_merged_origins": c.get("duplicated_relation", c.get("merged_origin_urls", [])),
                "historical_limit": c.get("comment_history_limit", c.get("historical_limit")),
                "literal_cautions": c.get("literal_cautions", []),
                "source_record": "evidence/" + tag + "/candidate-part.json",
                "official_behavior_at_freeze": "not_read",
                "author_followup_at_freeze": "not_read; indirect exposure separately logged",
            })
    assert len(rows) == 24 and len({r["candidate_id"] for r in rows}) == 24
    assert sum(not r["blank"] for r in rows) == 18
    for case in initial:
        cs = [r for r in rows if r["case_id"] == case]
        assert sorted(r["original_rank"] for r in cs) == [1, 2, 3]
        for policy in ("A", "B"):
            expected = [r["candidate_id"] for r in cs if r[policy + "_decision"] == "keep"][:2]
            actual = [r["candidate_id"] for r in cs if r[policy + "_returned_position"]]
            assert expected == actual, (case, policy, expected, actual)
    write_csv(ROOT / "candidates.csv", rows)
    current = [json.loads(line) for line in (ROOT / "sources.jsonl").read_text().splitlines() if line]
    known = {r["source_id"] for r in current}
    for tag in ("imagemagick", "typst"):
        p = ROOT / "evidence" / tag / "sources-proposals.jsonl"
        for line in p.read_text().splitlines():
            s = normalize_source(json.loads(line))
            assert not s["counted"], "Proposal is within an already counted request lineage"
            if s["source_id"] not in known:
                current.append(s)
                known.add(s["source_id"])
    (ROOT / "sources.jsonl").write_text("".join(json.dumps(s, ensure_ascii=False) + "\n" for s in current))
    print(json.dumps({"slots": len(rows), "actual": sum(not r["blank"] for r in rows), "blank": sum(r["blank"] for r in rows),
                      "A_returned": sum(bool(r["A_returned_position"]) for r in rows), "B_returned": sum(bool(r["B_returned_position"]) for r in rows),
                      "A_excluded": sum(r["A_decision"] == "exclude" for r in rows), "B_excluded": sum(r["B_decision"] == "exclude" for r in rows)}))


if __name__ == "__main__":
    main()
