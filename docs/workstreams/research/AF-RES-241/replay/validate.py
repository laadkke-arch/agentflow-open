"""Check the link between recorded evidence, the fixed denominator and the result tables."""
import collections
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANCHORS = {"A1-1", "A1-2", "A2-1", "A2-2", "A3-1", "A3-2", "R1-1", "R1-2"}


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def rows(path):
    with (ROOT / path).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def verify_journeys():
    journeys = rows("journeys.csv")
    assert len(journeys) == 16
    assert {row["journey_id"] for row in journeys} == {f"{a}-{kind}" for a in ANCHORS for kind in "SB"}
    by_id = {}
    for row in journeys:
        receipt = read_json(row["receipt"])
        stages = receipt["stages"]
        by_id[row["journey_id"]] = receipt
        assert row["journey_id"] == receipt["id"]
        assert receipt["harness_completed"] and not receipt["errors"]
        assert row["missing_required_stages"] == "" and row["returned_to_origin"] == "True"
        assert row["first_focus"] == row["return_focus"] == "BODY" and row["return_errors"] == "[]"
        assert row["ax_role"] == "link" and row["visible_text"] == "Change"
        assert " ".join(row["raw_ax_name"].split()) == row["expected_normalized_ax"]
        suffix = row["expected_normalized_ax"].removeprefix("Change ")
        assert row["raw_ax_name"] == f"Change \xa0 {suffix}\xa0"
        assert stages["origin"]["summaryLinks"] and stages["origin"]["locale"] == "en"
        assert receipt["tabSteps"][-1][0] == int(row["dom_ordinal"])
        assert receipt["nav"][0]["href"] == receipt["nav"][0]["landed"] == row["first_edit_url"]
        assert row["return_url"] == stages["return"]["url"] == stages["origin"]["url"]
        first_fields = json.loads(row["first_inputs"])
        assert any(field["visible"] for field in first_fields)
        assert row["screen_reader_utterance"] == "미확인"
        if row["journey"] == "B":
            assert receipt["nav"][-1]["method"] == "app back/cancel"
            assert receipt["models"]["before"] == receipt["models"]["after"]
            assert stages["origin"]["summaryRows"] == stages["return"]["summaryRows"]
    for anchor in ANCHORS:
        save = by_id[f"{anchor}-S"]
        back = by_id[f"{anchor}-B"]
        assert save["stages"]["origin"]["summaryRows"] == back["stages"]["origin"]["summaryRows"]
        peer = anchor.removesuffix(anchor[-1]) + ("2" if anchor.endswith("1") else "1")
        assert save["selectedSuffix"] != by_id[f"{peer}-S"]["selectedSuffix"]
        for trial in (save, back):
            suffixes = {
                span["raw"].strip()
                for link in trial["stages"]["origin"]["summaryLinks"]
                for span in link["hidden"]
            }
            assert {save["selectedSuffix"], by_id[f"{peer}-S"]["selectedSuffix"]} <= suffixes
    target_models = (
        ("A1-1", "reference", "referee_type", "professional"),
        ("A1-2", "reference", "name", "Morgan Edited"),
        ("A2-1", "current_course", "name_and_code", "AF241 English (T242)"),
        ("A2-2", "current_course", "study_mode", "part_time"),
        ("A3-1", "application_form", "phone_number", "07700 900242"),
        ("A3-2", "application_form", "address_line1", "25 Example Street"),
        ("R1-1", "trainee", "training_route", "school_direct_salaried"),
        ("R1-2", "trainee", "course_education_phase", "primary"),
    )
    for anchor, model, field, value in target_models:
        states = by_id[f"{anchor}-S"]["models"]
        assert states["before"][model][field] != value
        assert states["after"][model][field] == value
    assert by_id["R1-1-S"]["models"]["after"]["progress"]["course_details"] is False
    assert by_id["R1-2-S"]["models"]["after"]["progress"]["course_details"] is True
    return journeys


def verify_controls(source_ids):
    controls = rows("controls.csv")
    for row in controls:
        for s in row["source_ids"].split(";"):
            assert s in source_ids, s
        for f in row["receipts"].split(";"):
            assert (ROOT / f).is_file(), f
    for f in ("apply-a2-spec", "apply-controls", "register-controls", "apply-clean-final"):
        assert (ROOT / f"receipts/controls/{f}.exit").read_text().strip() == "0"
    for service in ("apply", "register"):
        assert (ROOT / f"receipts/attempts/{service}-fixed.exit").read_text().strip() == "0"
    positive = read_json("receipts/controls/A3-1-POS.json")
    invalid = read_json("receipts/controls/A3-1-ERR.json")
    assert positive["models"]["before"]["application_form"]["phone_number"] == "07700 900241"
    assert positive["models"]["after"]["application_form"]["phone_number"] == "07700 900242"
    assert positive["stages"]["return"]["url"] == positive["stages"]["origin"]["url"]
    assert invalid["models"]["before"]["application_form"] == invalid["models"]["after"]["application_form"]
    assert invalid["stages"]["validation"]["focused"]["tag"] == "DIV"
    assert invalid["stages"]["validation"]["errors"]
    duplicate = read_json("receipts/controls/C-A1-DUP.json")["originTargets"]
    assert len({link["ax"]["cdpNode"]["name"]["value"] for link in duplicate}) == 1
    assert len({link["rawHref"] for link in duplicate}) == 2
    middle = read_json("receipts/controls/C-A3-MID.json")["models"]
    assert [middle[s]["application_form"]["country"] for s in ("before", "after_unchanged_uk", "after")] == ["GB", "", ""]
    f1, f2 = (read_json(f"receipts/controls/C-R-F{k}.json") for k in (1, 2))
    for receipt in (f1, f2):
        assert receipt["models"]["before"] == receipt["models"]["after"] == {"feedback_item_count": 0}
        assert receipt["stages"]["first_edit"]["focused"]["tag"] == "BODY"
    for stage in ("first_edit", "return"):
        assert f1["stages"][stage]["url"] == f2["stages"][stage]["url"]
    def fields(run):
        return {
            (entry["id"], entry["value"], entry["checked"], tuple(entry["labels"]))
            for entry in run["stages"]["first_edit"]["inputs"]
        }

    assert fields(f1) == fields(f2)
    library = read_json("receipts/controls/library.json")
    assert library["observed_action_count"] == library["observed_actual_holding_id_count"] == 0
    assert library["records"][0]["extracted_action_text"] == library["records"][1]["extracted_action_text"]
    assert len({item["bib_id"] for item in library["records"]}) == 3
    return controls


def main():
    ledger = [json.loads(line) for line in (ROOT / "sources.jsonl").read_text(encoding="utf-8").splitlines()]
    ids = {row["source_id"] for row in ledger}
    assert len(ledger) == len(ids) and all(row["confirmed_utc"]["start"] <= row["confirmed_utc"]["end"] for row in ledger)
    counted = [row for row in ledger if row["counted"]]
    assert len(counted) == len({row["work_id"] for row in counted}) >= 22
    assert all(row["access_result"] == "opened_and_read" and not row["url"].startswith("http:") for row in counted)
    categories = collections.Counter(row["category"] for row in counted)
    assert all(categories[c] >= n for c, n in {
        "view": 5, "route_form_fixture": 6, "test_setup": 5, "standard": 3, "library": 3,
    }.items())
    journeys = verify_journeys()
    controls = verify_controls(ids)

    result = (ROOT / "RESULT.md").read_text(encoding="utf-8")
    assert result.startswith("| 화면·앵커·여정 | 보이는 이름·AX 이름 | 실제 href·포커스·필드 | 저장값·다른 값 | 실제 복귀·원영수증 | 미확인 |\n")
    assert "| 반례·기존 시험 | 소스의 단언 | 실제 관측 단계 | 추천 문구에 넣을 구별값 | 남은 한계 |" in result
    assert re.findall(r"^## (Q[1-7])\.", result, flags=re.M) == [f"Q{i}" for i in range(1, 8)]
    assert len(result.rsplit("| 중요한 불일치 또는 약점 |", 1)[-1].strip().splitlines()) == 5
    assert len(re.findall(r"^\| (?:Apply|Register).*? · [AR]\d-\d [SB] \|", result, flags=re.M)) == 16
    for link in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", result):
        if not link.startswith("https://"):
            assert (ROOT / link).exists(), link
    print(json.dumps({
        "ledger_rows": len(ledger), "counted_works": len(counted),
        "counted_lineages": len({r["lineage_id"] for r in counted}),
        "count_by_category": categories, "journeys": len(journeys), "control_rows": len(controls),
        "tab_min": min(int(row["tab_count"]) for row in journeys),
        "tab_max": max(int(row["tab_count"]) for row in journeys),
        "same_initial_summary_pairs": len(ANCHORS), "source_and_result_checks": "passed",
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
