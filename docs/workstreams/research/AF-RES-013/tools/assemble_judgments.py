"""Combine internal review shards and explicit root adjudications; never infer relevance."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def main():
    shards = sorted(ROOT.glob("evidence/judging-recovery/*/judgments.json"))
    assert len(shards) == 3
    rows = []
    provenance = []
    for path in shards:
        data = json.loads(path.read_text())
        provenance.append({"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "rows": len(data["judgments"])})
        for row in data["judgments"]:
            if "judged_date_status" in row:
                row.setdefault("original_date_status", row["date_status"])
                row["date_status"] = row["judged_date_status"]
            row["original_judgment_path"] = str(path.relative_to(ROOT))
            rows.append(row)
    by_key = {(r["case_id"], r["baseline"], r["rank"]): r for r in rows}
    assert len(by_key) == len(rows)
    review_files = sorted(ROOT.glob("evidence/judging-recovery/*/CROSS_REVIEW.json"))
    for path in review_files:
        data = json.loads(path.read_text())
        reviews = data if isinstance(data, list) else data.get("reviews", data.get("rows", []))
        for review in reviews:
            key = (review["case_id"], review["baseline"], review["rank"])
            assert key in by_key
            by_key[key].setdefault("cross_reviews", []).append({"recorded_in": str(path.relative_to(ROOT)), **review})
    adjudication_path = ROOT / "evidence/judging-recovery/ROOT_ADJUDICATIONS.json"
    adjudications = json.loads(adjudication_path.read_text()) if adjudication_path.exists() else {"overrides": [], "decisions": []}
    for change in adjudications.get("overrides", []):
        key = (change["case_id"], change["baseline"], change["rank"])
        row = by_key[key]
        old = {field: row.get(field) for field in change["replacement_fields"]}
        row.update(change["replacement_fields"])
        row["root_adjudication"] = {"judge": "작업자", "previous_fields": old, "reason": change["reason"], "evidence": change.get("evidence", []), "recorded_in": str(adjudication_path.relative_to(ROOT))}
    output = {
        "schema_version": 1,
        "task": "AF-RES-013",
        "source_commit": "a18d8d2e1575d9b679442134fd0f6f8e17423bfe",
        "preserved_run_input_commit": "caa2a814727dd485ed0eb9bb8530d6b16fab9584",
        "original_gold_commit": "f6f59a85949a001792b80260dd454c3fcc714a70",
        "protocol_commit": "2b798c7d2b7355b649691c18de196104ceabb0f0",
        "model_label": "GPT-6 Astra Pro",
        "judging_scope": "기존 원 응답342행의 문서 기반 L/E/H/T·항목 일치·시간 판정. 세 내부 별도 문맥에 분할하고 경계 행을 다른 내부 문맥과 작업자가 검토했다. 사람·다른 모델·사용자 또는 구현 효용 검증이 아니다.",
        "runtime_observation": "not_performed",
        "source_shards": provenance,
        "cross_review_files": [str(p.relative_to(ROOT)) for p in review_files],
        "root_adjudication_file": str(adjudication_path.relative_to(ROOT)) if adjudication_path.exists() else None,
        "judgments": sorted(by_key.values(), key=lambda r: (r["case_id"], r["baseline"], r["rank"])),
    }
    (ROOT / "JUDGMENTS.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"rows": len(rows), "shards": len(shards), "cross_review_files": len(review_files), "overrides": len(adjudications.get("overrides", []))}))


if __name__ == "__main__":
    main()
