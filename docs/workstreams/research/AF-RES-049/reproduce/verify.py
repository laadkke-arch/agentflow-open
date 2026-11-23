"""Verify the committed panel, witnesses, ledgers and two report tables."""
import csv
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with (ROOT / path).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def same(a, b, tol):
    return len(a) == len(b) and all(abs(m-n) <= tol for m, n in zip(a, b))


def main():
    plans = read_csv("expected.csv")
    runs = read_csv("runs.csv")
    expected_ids = [r["run_id"] for r in plans]
    assert len(expected_ids) == len(set(expected_ids)) == 28
    assert expected_ids == [r["run_id"] for r in runs]
    assert sum(r["panel"] == "primary" for r in runs) == 20
    assert sum(r["panel"] == "version" for r in runs) == 4
    assert sum(r["panel"] == "purpose" for r in runs) == 4
    print("28 unique panel IDs, exact ledger alignment")

    observations = {}
    checked_raster = 0
    for plan, row in zip(plans, runs):
        run_id = row["run_id"]
        directory = "evidence/runs/" + run_id
        observation = read_json(directory + "/observations.json")
        observations[run_id] = observation
        assert observation["plan"] == plan
        assert "instrumentation_error" not in observation
        assert row["status"] == observation["status"]
        if row["status"] == "saved":
            png = observation["png"]
            assert png["size_px_wh"] == ([500, 400] if row["case"] == "M03" else [1000, 300])
            assert row["save_status"] == "saved"
            for witness in ["file", "ink_mask"]:
                if witness in png:
                    artifact = png[witness]
                    fp = ROOT / directory / artifact["filename"]
                    assert artifact["sha256"] == hashlib.sha256(fp.read_bytes()).hexdigest()
                    assert artifact["bytes"] == fp.stat().st_size
            if row["case"] == "M03":
                assert png["axes_unchanged_for_alpha_zero"] and png["agrees_with_transform"]
                checked_raster += 1
        else:
            assert observation["status"] == "layout_failed" and row["save_status"] == "not_attempted"
            assert not (ROOT / directory / "figure.png").exists()
            assert len(observation["steps"]) == 1 and observation["steps"][0]["error_type"] == "TypeError"
            assert "after_save" not in observation
    assert checked_raster == 13
    print("28 JSON witnesses, 25 saved PNGs, 3 layout failures, 13 M03 transform/ink agreements")

    for repeat in ["R1", "R2"]:
        for factor_tag, factor in [("01", .01), ("001", .001)]:
            a = observations[f"{repeat}-M03-{factor_tag}-A"]
            b = observations[f"{repeat}-M03-{factor_tag}-B"]
            assert a["input"] == b["input"]
            for phase in ("before_layout", "after_layout_attempt", "after_save"):
                assert same(a[phase]["text_anchor_colorbar_axes_fraction"], [.5, .5], 1e-6)
                if phase not in b:
                    continue
                stage = b[phase]
                for axis in ("x", "y"):
                    assert stage["colorbar_axes"][axis+"scale"] == "linear"
                    assert same(stage["colorbar_axes"][axis+"lim"], [0, 99*factor], 1e-12)
                expect = .5 / (99*factor)
                assert same(stage["text_anchor_colorbar_axes_fraction"], [expect, expect], 1e-6)
            av = observations[f"V1-M03-{factor_tag}-A"]
            bv = observations[f"V1-M03-{factor_tag}-B"]
            assert av["png"]["file"]["sha256"] == bv["png"]["file"]["sha256"]
            assert same(bv["after_save"]["text_anchor_colorbar_axes_fraction"], [.5, .5], 1e-6)

        for count in [10, 30]:
            a, b, c = [observations[f"{repeat}-M02-{count}-{choice}"] for choice in "ABC"]
            assert a["input"] == b["input"] == c["input"] and c["legend"] is None
            for idx in (0, 2):
                assert same(b["after_save"][idx]["axes_bbox_pixels"], c["after_save"][idx]["axes_bbox_pixels"], .25)
            for var, expected_readable in [(a, 10 if count == 10 else 11),
                                           (b, 10 if count == 10 else 12)]:
                assert var["png"]["axes_unchanged_for_alpha_zero"]
                entries = var["legend"]["entries"]
                assert len(entries) == count
                assert sum(e["bbox_outside"] for e in entries) == count - expected_readable
                assert sum(e["ink_pixels"] > 0 for e in entries) == expected_readable
                assert sum(e["ink_pixels"] for e in entries) == var["png"]["changed_pixels"]
    print("M03 conditional arithmetic and M02 baseline/legend counts recomputed")

    pairs = read_json("evidence/replay-pairs.json")["pairs"]
    assert len(pairs) == 10
    assert all(p["max_px_delta"] == p["max_limits_or_fraction_delta"] == 0 for p in pairs)
    assert sum(p["comparison"] == "rgb_identical" and p["png"]["byte_equal"] for p in pairs) == 9
    assert sum(p["comparison"] == "matching_failure" for p in pairs) == 1
    assert all(row["exit_code"] == 0 for row in read_json("evidence/command-receipts.json"))
    print("9/9 exported replay pairs byte/RGB identical, 1 matching layout failure")

    raw_sources = (ROOT / "sources.jsonl").read_text(encoding="utf-8")
    sources = [json.loads(line) for line in raw_sources.splitlines()]
    ids = {s["source_id"] for s in sources}
    assert len(ids) == len(sources)
    for s in sources:
        for field in ("url", "checked_utc", "edition_locator", "confirmed", "limits", "assessment"):
            assert s[field]
        assert all(ancestor in ids for ancestor in s["evidence_lineage"])
    counted = [s for s in sources if s["counts_unique"]]
    assert len({s["work_id"] for s in counted}) == len(counted) == 34
    assert all(s["duplicate_of"] is None and s["read_status"] == "direct" for s in counted)
    quotas = {"요구·후속": 4, "구현·회귀": 6, "공식 환경": 4, "인쇄·도판": 4, "지도·라벨": 4}
    assert all(sum(s["category"] == q for s in counted) >= n for q, n in quotas.items())
    print("34 distinct original works, each category meets its minimum")

    result = (ROOT / "RESULT.md").read_text(encoding="utf-8")
    first = result.split("\n\n", 2)
    assert first[0].startswith("| 사례 | 실행 ID·반복 |")
    assert first[1].startswith("| 요구 | 원리가 내린 선택 |")
    assert len(first[0].splitlines()) - 2 == 24
    assert len(first[1].splitlines()) - 2 == 2
    assert all(sum(run_id in line for line in first[0].splitlines()) == 1 for run_id in expected_ids[:24])
    last = result.strip().split("\n\n")[-1]
    assert last.startswith("| 불일치 또는 약점 | 영향받는 결론 |")
    assert len(last.splitlines()) - 2 == 3
    assert all("Q" + str(num) in (ROOT / "SELF_CHECK.md").read_text() for num in range(1, 8))
    doc_names = ["RESULT.md", "SELF_CHECK.md", "cards.md", "request-alignment.md"]
    for doc in doc_names:
        p = ROOT / doc
        for url in re.findall(r"\]\(([^)]+)\)", p.read_text()):
            if "://" not in url:
                assert (p.parent / url.split("#")[0]).exists(), (doc, url)
    for condition in read_json("evidence/acceptance-evidence.json")["conditions"]:
        for item in condition["evidence"]:
            assert (ROOT / item["file"]).exists()
    print("Two required tables, 3 closing weaknesses, Q1–Q7, links and acceptance ledger checked")


if __name__ == "__main__":
    main()
