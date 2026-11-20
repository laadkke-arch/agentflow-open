#!/usr/bin/env python3
"""Assemble researcher-coded case records; does not discover or judge sources."""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = ["같은 목적 완성품", "재사용 부품", "같은 분야의 다른 설계", "다른 언어·생태계", "다른 분야 원리", "표준·논문"]


def read(path):
    return json.loads((ROOT / path).read_text())


def write(path, data):
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def main():
    manifest = read("cases/PREFIX_MANIFEST.json")
    mapping = {x["canonical_id"]: x for x in manifest["prefixes"]}
    drafts = []
    for group in ("kep", "rust", "ps"):
        data = read(f"evidence/cases-{group}/draft-cases.json")
        drafts.extend(data if isinstance(data, list) else data["cases"])
    cases = []
    for case in drafts:
        canonical = case["id"]
        entry = mapping[canonical]
        case["canonical_id"] = canonical
        case["id"] = entry["id"]
        case["prefix_file"] = entry["prefix_path"]
        case["prefix_sha256"] = entry["sha256"]
        case["prefix_commit"] = {"P0563": "c9936188a885848a16b55b4e11ac965bd2d0b204", "P0386": "ba1cc08705e4a1c56fcdb1a8062193ca4748992e"}.get(canonical, "8cb2b8e58f7d4278c11073956b31b30ad43aff18")
        assert case["decision_date"] == entry["cutoff_date"], (canonical, case["decision_date"], entry["cutoff_date"])
        assert hashlib.sha256((ROOT / entry["prefix_path"]).read_bytes()).hexdigest() == entry["sha256"]
        case["mandatory_constraints"] = [
            {"id": f"H{i}", "text": c} if isinstance(c, str) else c
            for i, c in enumerate(case["mandatory_constraints"], 1)
        ]
        case.setdefault("review_gold_items", [])
        case["gold_coding_author"] = "연구자/내부 별도 검토의 원문 항목 추출·분절·역할 분류; 원문 저자와 독립된 새 정답 창작 아님"
        case["coding_source"] = f"evidence/cases-{'kep' if canonical.startswith('K') else 'rust' if canonical.startswith('R') else 'ps'}/draft-cases.json"
        for i, item in enumerate(case["gold_items"], 1):
            item.setdefault("id", f"{canonical}-G{i:02d}")
            assert item["role"] in ROLES, item
            assert item["stance"] in ("adopted", "rejected", "referenced"), item
            for field in ("name", "url", "role", "stance", "reason", "added_in_review", "boundary_note"):
                assert field in item, (canonical, field)
            named = {"P0201-G01", "P0201-G04", "P0202-G01", "P0202-G02", "P0204-G01", "P0204-G03", "P0386-G01", "P0386-G02", "P0386-G03", "P0386-G04", "P0386-G05", "P0433-G06", "P0433-G07", "P0433-G08", "P0433-G09", "P0433-G10", "P0509-G04", "P0509-G05", "P0509-G06", "P0509-G07", "P0509-G08", "S0018-G06", "S0018-G07", "S0027-G04", "S0027-G05"}
            item.setdefault("match_kind", "external_entity" if item.get("item_kind") == "external_reference" or item["id"] in named else "structural_design")
            if item["id"] == "R0042-G02":
                item["match_kind"] = "structural_design"
                item["match_note"] = "특정 라이브러리 실체가 아닌 기존 라이브러리 바인딩이라는 구성 전략. 부품 역할과 실체 일치는 다른 축이다."
        assert len(case["gold_items"]) >= 3
        cases.append(case)
    cases.sort(key=lambda c: c["id"])
    assert len(cases) == len(mapping) == 31 and len({x["id"] for x in cases}) == 31
    families = collections.Counter(c["family"] for c in cases)
    assert len(families) >= 4 and max(families.values()) <= len(cases) / 2
    write("cases/CASES.json", {"schema_version": 1, "source_commit": "a18d8d2e1575d9b679442134fd0f6f8e17423bfe", "prefix_commit": "8cb2b8e58f7d4278c11073956b31b30ad43aff18", "prefix_correction_commit": "c9936188a885848a16b55b4e11ac965bd2d0b204", "gold_scope": "본문 비교절의 관측 항목(리뷰에서 추가되어 본문에 반영된 항목 포함); 본문에 반영되지 않은 별도 review pool은 확대 민감도에서만 합치며 alias 중복을 제거", "case_coding": "연구자 분절·분류", "cases": cases})
    roles = collections.Counter(g["role"] for c in cases for g in c["gold_items"])
    audit = {"cases": len(cases), "families": dict(families), "gold_items": sum(roles.values()), "roles": {r: roles[r] for r in ROLES}, "minimum_gold_per_case": min(len(c["gold_items"]) for c in cases), "prefixes_hash_match": True, "supersession_records": [{"id": c["id"], "canonical_id": c["canonical_id"], "superseded_by": c["superseded_by"]} for c in cases if c.get("superseded_by")], "limits": "기계 검사는 실제 원문 품질·역할 판정·날짜 증명의 정확성을 대체하지 않는다."}
    write("evidence/CORPUS_CHECK.json", audit)
    print(json.dumps({k:v for k,v in audit.items() if k != "supersession_records"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
