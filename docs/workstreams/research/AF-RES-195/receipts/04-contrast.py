"""Reproduce the scoped counterexamples using de-identified tables and the fixed METR CSV."""

import argparse
import csv
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from decimal import Decimal
from pathlib import Path


METR_REV = "7ff2d7670235f531dff77eff58355bd77392f396"
METR_SHA = "1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746"
PAPER_SAMPLE_SOURCE = "1b680a318dcd072e14ad3de07ff8b29f85eb2fdc4fc3daebd6f74467d9a6bb16"
FIELDS = "bound_id case_id observed_value unit comparison_basis role_window state test evidence_ids limit".split()


def read(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def sha(value):
    return hashlib.sha256(value).hexdigest()


def time_or_missing(value):
    return Decimal(value) if value.strip() else None


def complete_minutes(*values):
    return sum(values) if all(value is not None for value in values) else None


def inspect_paper_sample(upstream, inv):
    result = {}
    with zipfile.ZipFile(upstream / "data/raw/ita.zip") as archive:
        for mode in ("pe1", "pe2"):
            row = next(r for r in inv if (
                r["language"], r["phase"], r["doc_id"], r["condition"], r["kind"]
            ) == ("ita", "main", "28", mode, "per"))
            data = archive.read(archive.infolist()[int(row["entry_index"]) - 1])
            assert sha(data) == row["sha256"]
            u = ET.fromstring(data).find("unit[@id='1']")
            annotations = u.findall("annotations/annotation")
            target = annotations[-1].find("PE")
            result[mode] = dict(
                entry=row["entry"], entry_index=row["entry_index"], per_sha256=row["sha256"],
                subject=row["subject_id"], producer_is_folder=target.get("producer").split(".", 1)[0] == row["subject_id"].split("_")[1],
                flores_id=u.get("orig_id"), source=sha(u.findtext("S").encode()),
                target=sha(target.text.encode()), draft=sha(u.findtext("MT").encode()),
                event_ms=sum(int(a.findall("events/*")[-1].get("t")) for a in annotations),
            )
        r = next(r for r in inv if (
            r["language"], r["phase"], r["doc_id"], r["condition"], r["kind"]
        ) == ("ita", "main", "29", "pe1", "per"))
        xml = ET.fromstring(archive.read(archive.infolist()[int(r["entry_index"]) - 1]))
        table_id_source = sha(xml.findtext("unit[@id='2']/S").encode())
    first, second = result["pe1"], result["pe2"]
    assert table_id_source != PAPER_SAMPLE_SOURCE
    assert first["source"] == second["source"] == PAPER_SAMPLE_SOURCE
    assert first["flores_id"] == second["flores_id"] == "518"
    assert first["target"] == second["target"]
    assert first["subject"] != second["subject"] and all(p["producer_is_folder"] for p in result.values())
    assert first["draft"] != first["target"] and second["draft"] == second["target"]
    return result | {"paper_printed_29_2_source_sha256_in_archive": table_id_source}


def summarize_pairs(pairs):
    result = {}
    for lang in ("ita", "tur", "all"):
        sample = [r for r in pairs if r["language"] == lang or lang == "all"]
        result[lang] = {}
        for metric in ("ms", "after_ge1000_ms", "after_ge60000_ms"):
            result[lang][metric] = {}
            for test, ref in (("pe1", "ht"), ("pe2", "ht"), ("pe2", "pe1")):
                diffs = [int(r[f"{test}_{metric}"]) - int(r[f"{ref}_{metric}"]) for r in sample]
                result[lang][metric][f"{test}_vs_{ref}"] = {
                    "higher": sum(x > 0 for x in diffs), "tie": sum(x == 0 for x in diffs),
                    "lower": sum(x < 0 for x in diffs), "pairs": len(diffs),
                }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--metr", type=Path, required=True)
    args = parser.parse_args()
    p = args.work
    segments = read(p / "segments.csv")
    selections = read(p / "receipts/03-pairs.csv")
    revisions = read(p / "receipts/03-revisions.csv")
    inventory = read(p / "inventory.csv")
    if subprocess.check_output(["git", "-C", str(args.metr), "rev-parse", "HEAD"], text=True).strip() != METR_REV:
        raise ValueError("pin the METR comparison Git revision")
    metr_file = args.metr / "data_complete.csv"
    if sha(metr_file.read_bytes()) != METR_SHA:
        raise ValueError("METR raw CSV hash mismatch")
    metr = read(metr_file)
    field = "post_review_implementation_time"
    repair = {r["issue_id"]: time_or_missing(r[field]) for r in metr}
    issue = {r["issue_id"]: r for r in metr}
    initial = {k: Decimal(r["initial_implementation_time"]) for k, r in issue.items()}
    paper_sample = inspect_paper_sample(args.upstream, inventory)
    diffs = summarize_pairs(selections)
    assert len(selections) == 32 and diffs["all"]["ms"]["pe1_vs_ht"] == dict(higher=9, tie=0, lower=23, pairs=32)
    assert diffs["all"]["ms"]["pe2_vs_ht"] == dict(higher=9, tie=0, lower=23, pairs=32)
    assert diffs["all"]["ms"]["pe2_vs_pe1"]["tie"] == 0
    extremes = {m: max(selections, key=lambda r: int(r[f"{m}_minus_ht_ms"])) for m in ("pe1", "pe2")}
    e4 = next(r for r in segments if r["prior_row_id"] == "E4")
    event_ms, p300, p1000 = (int(e4[k]) for k in ("event_time_ms", "pause_ge300_ms", "pause_ge1000_ms"))
    invalid_overlap = event_ms - p300 - p1000
    corrected_pauses = event_ms - p1000
    assert invalid_overlap < 0 and corrected_pauses == int(e4["after_ge1000_union_ms"]) == 32066
    unchanged = [r for r in segments if r["draft_equals_target"] == "True"]
    assert len(unchanged) == 4 and all(r["key_total"] == "0" and int(r["event_time_ms"]) > 0 for r in unchanged)
    missing = next(r for r in revisions if r["slot_id"] == "ita-2-ht" and r["unit_status"] == "STARTED")
    assert not missing["event_time_ms"] and missing["xml_status"] == "GOING_ON"
    assert complete_minutes(initial["1"], repair["1"]) == 242 and complete_minutes(initial["3"], repair["3"]) == 200
    assert issue["1"]["dev_id"] == issue["3"]["dev_id"] and issue["1"]["issue_id"] != issue["3"]["issue_id"]
    assert repair["2"] == 0 and repair["26"] is None
    assert complete_minutes(initial["2"], repair["2"]) == 36
    assert complete_minutes(initial["26"], repair["26"]) is None
    states = Counter("missing" if v is None else "zero" if v == 0 else "positive" for v in repair.values())
    assert states == {"missing": 16, "zero": 109, "positive": 121}
    treatment = issue["26"]["ai_treatment"]
    known = [v for k, v in repair.items() if v is not None and issue[k]["ai_treatment"] == treatment]
    imputed_repair = sum(known) / len(known)
    assert imputed_repair > 0 and complete_minutes(initial["26"], imputed_repair) > initial["26"]
    ocr_percent = Decimal(113) * 100 / Decimal(169619)
    assert round(Decimal(100) - ocr_percent, 2) == Decimal("99.93")
    assert complete_minutes(None, None) is None
    assert not any(s["reviewer_time_ms"] for s in segments)

    rows = []

    def add(id, case, value, unit, basis, role, state, test, sources, limit):
        rows.append(dict(zip(FIELDS, (id, case, value, unit, basis, role, state, test, sources, limit))))

    add("B01", "all Raw/author", 96, "condition-segment rows", "exact keys, hashes, times, pauses, 96/96",
        "PET translator", "verified", "positive", "CODE-01;CODE-02", "HF frozen exact join separate")
    add("B02", "prior E1-E5", "2061853;111", "ms;English source words", "raw + author + 181 + live-viewer projection",
        "PET translator", "verified", "positive", "PRIOR-EFFORT;HF-VIEW-01;RAW-TUR-0004", "only one document, condition HT")
    for id, mode in (("B03", "pe1"), ("B04", "pe2")):
        e = extremes[mode]
        add(id, e["case_id"], e[f"{mode}_minus_ht_ms"], "ms PE minus HT",
            f"{mode} slower in {diffs['all']['ms'][mode + '_vs_ht']['higher']}/32; ties 0/32",
            "PET translator", "observed contrast", "negative", "CODE-01;receipts/03-pairs.csv",
            "different producers on shared source")
    add("B05", "TUR E4", f"{invalid_overlap};{corrected_pauses}", "ms invalid double subtraction;ms one threshold remainder",
        f"logged {event_ms}; nested totals {p300} and {p1000}", "PET translator", "union only",
        "negative/positive", "PRIOR-EFFORT;RAW-TUR-0004;CODE-01", "only sensitivity; gaps can include reading or thinking")
    add("B06", "ita-2-ht / backup .per.2 / unit 3", "missing", "ms", "GOING_ON / STARTED; no annotation time",
        "PET translator", "missing", "negative", "receipts/03-revisions.csv entry 1567",
        "revision of completed slot; zero time cannot be imputed")
    add("B07", "TUR doc1 PE1 flores 207", "0;24202", "recorded keys;ms",
        "unchanged draft/final fingerprint; translator spent positive logged time", "PET translator",
        "verified zero keys", "positive", "receipts/03-pairs.csv;segments.csv",
        "zero edits provide no evidence of score or reviewer time")
    add("B08", "ITA doc28 unit1 (out of frame)", "4530;36203", "ms PE1;ms PE2",
        "one output SHA, two producer keys; source hash links Table 12 to raw 28.1, printed 29.2 does not match",
        "two PET translators", "verified alias counterexample", "negative", "DIAG-ITA-0259;DIAG-ITA-0905;DESIGN-01",
        "exclude from 32 cases; same final hash cannot key people and does not show quality")
    add("B09", "Kokos §3.2", f"113/169619;72;{ocr_percent:.6f}", "characters corrected / characters;words;% character rate",
        "independent proofread by two people and merged gold standard", "separate OCR QA",
        "count verified; QA timing missing", "positive/negative", "OCR-01;PRIOR-BOUNDS",
        "unknown proofread/adjudication minutes, known corrected count")
    for id, i in (("B10", "1"), ("B11", "3"), ("B12", "2"), ("B13", "26")):
        total = complete_minutes(initial[i], repair[i])
        state = "observed zero developer repair" if repair[i] == 0 else "missing developer repair" if repair[i] is None else "observed developer repair"
        add(id, f"METR issue {i}", f"{initial[i]};{repair[i]};{total}", "initial;repair;developer total minutes",
            "same-issue developer initial plus own repair when both supplied", "developer",
            state, "negative" if total is None else "positive", "METR-01;METR-02;METR-03;METR-04",
            "reviewer active time unknown; issue 1 versus 3 differ in work item")
    add("B14", "METR fixed CSV", "16;109;121;246", "missing;zero;positive;all issues",
        f"issue 26 treatment-mean repair {imputed_repair:.6f} min, model-only",
        "developer", "observed and imputed kept distinct", "negative/positive", "METR-01;METR-03;METR-04",
        "paper counts 27 unreviewed issues, definition/row mapping to CSV blanks unavailable")
    add("B15", "DivEMT independent QA", "unknown", "reviewer minutes and acceptance",
        "fixed schema search, paper §3.1, metrics implementation", "independent reviewer", "no public join",
        "negative", "DESIGN-01;DESIGN-03;CODE-01;CODE-05", "only translator role is measured")

    with (p / "bounds.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    out = dict(
        comparisons=diffs, n_revisions=len(revisions), missing_revision=missing,
        paper_sample=paper_sample, metr_repair_states=states,
        metr_issue_26_imputed_minutes=round(float(imputed_repair), 6),
        ocr_char_correction_percent=round(float(ocr_percent), 6),
        assertions="passed",
    )
    (p / "receipts/04-counterexamples.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(dict(ocr_char_correction_percent=out["ocr_char_correction_percent"],
                          metr_repair_states=states, comparisons=diffs["all"], assertions=out["assertions"]),
                     sort_keys=True))


if __name__ == "__main__":
    main()
