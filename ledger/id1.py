"""08 I52: 장부의 같은 대상 규칙(n1 정규화 키)을 ID1 고정 묶음(61쌍, opensource 모델 판정)과 견준다.

  python3 -I ledger/id1.py      out/id1_same_target.json을 쓴다(네트워크 없음)

문서 합침 = 두 주소의 page 키가 같음, 프로젝트 합침 = 두 target 키가 같고 비어 있지 않음. 별칭은 넣지 않는다.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from afledger import normalize  # noqa: E402

FIX = HERE / "fixtures" / "id1"
OTHER = ("name_only", "unrelated", "alternative")
SAME_DOC = ("same_page", "mirror", "translation", "other_version")


def rows() -> list[dict]:
    lines = [l for l in (FIX / "ID1-D1.txt").read_text(encoding="utf-8").splitlines() if l and not l.startswith("@@")]
    return list(csv.DictReader(lines, delimiter="\t"))


def judge(a: str, b: str) -> dict:
    ka, kb = normalize.keys(a), normalize.keys(b)
    return {"doc_merge": ka["page"] is not None and ka["page"] == kb["page"],
            "project_merge": ka["target"] is not None and ka["target"] == kb["target"],
            "edition_a": ka["edition"], "edition_b": kb["edition"], "page_a": ka["page"], "page_b": kb["page"]}


def run() -> dict:
    rs = rows()
    pick = {r["n"]: r["pick"] for r in csv.DictReader(open(FIX / "ID1-pairs.tsv", encoding="utf-8"), delimiter="\t")}
    per, skipped = [], []
    for r in rs:
        if r["relation"] == "?":
            skipped.append(r["n"])
            continue
        per.append({"n": r["n"], "pick": pick.get(r["n"]), "relation": r["relation"], **judge(r["a"], r["b"])})
    other_merged = [x for x in per if x["relation"] in OTHER and (x["doc_merge"] or x["project_merge"])]
    split = [x for x in per if x["relation"] in SAME_DOC and not x["doc_merge"]]
    ov = [x for x in per if x["relation"] == "other_version"]
    ov_kind = Counter("split" if not x["doc_merge"] else
                      "edition_kept" if x["edition_a"] and x["edition_b"] and x["edition_a"] != x["edition_b"] else
                      "edition_lost" for x in ov)
    sp = [x for x in per if x["relation"] == "same_project"]
    out = {"note": "08 I52. 장부 n1 키로 본 같은 대상 판정과 ID1 relation(모델 판정) 견주기. 별칭 없음.",
           "pairs": len(rs), "skipped_unknown_relation": skipped, "relations": dict(Counter(x["relation"] for x in per)),
           "i_other_target_merged": {"count": len(other_merged), "n": [x["n"] for x in other_merged]},
           "ii_same_document_split": {"count": len(split), "by_relation": dict(Counter(x["relation"] for x in split)),
                                      "of": sum(1 for x in per if x["relation"] in SAME_DOC)},
           "iii_other_version": dict(ov_kind) | {"of": len(ov)},
           "iv_same_project": {"project_merge": sum(1 for x in sp if x["project_merge"]),
                               "doc_merge": sum(1 for x in sp if x["doc_merge"]),
                               "neither": sum(1 for x in sp if not x["project_merge"] and not x["doc_merge"]), "of": len(sp)},
           "catalog_reference": {"other_target_merged": 2, "same_document_split": 19, "same_project": "14 합침, 7 가름"},
           "per_pair": per}
    (HERE / "out" / "id1_same_target.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    r = run()
    print({k: v for k, v in r.items() if k not in ("per_pair",)})
