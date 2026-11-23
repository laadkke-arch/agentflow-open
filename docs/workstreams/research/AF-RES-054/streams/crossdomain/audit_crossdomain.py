"""Read the pinned public files and emit aggregates/schema only, never participant rows.

The cached input files are deliberately excluded from publication. See reproduce.md
for the exact download and dependency commands. This is an analysis-file audit;
it does not fabricate the missing original assignment ledger or pass threshold.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache"
sys.path.insert(0, str(CACHE / "deps"))

INPUTS = {
    "bichler-data.sav": (
        "https://osf.io/download/mykxc/",
        "9427aaccd8af49212834fa745424cb179c5da2c04079eef11fe3917aa7b734e8",
    ),
    "pillai-accuracy-e2.csv": (
        "https://osf.io/download/x9uge/",
        "6a94a61fc9c7ee704a8bfc4b4a8e115c81985da5f077f3a9994d5abf6aaf9de4",
    ),
    "pillai-ratings-e2.csv": (
        "https://osf.io/download/fseb4/",
        "4fed15c7506627a2e9784dd2e08e901b08cc54c450729a98562a2a23467654d3",
    ),
    "pillai-strategies-e2.csv": (
        "https://osf.io/download/t895q/",
        "cbf7e3542704edc78152c74a700d99b7da1703e20b6f1125ba1c38c03572b954",
    ),
}


def write(name: str, obj: object) -> None:
    (ROOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    import pandas as pd
    import pyreadstat

    CACHE.mkdir(exist_ok=True)
    inputs = []
    for name, (url, expected) in INPUTS.items():
        path = CACHE / name
        if args.download:
            req = urllib.request.Request(url, headers={"User-Agent": "AF-RES-054 public-record audit"})
            with urllib.request.urlopen(req, timeout=60) as response:
                path.write_bytes(response.read())
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == expected, f"Version changed: {name}"
        inputs.append({"file": name, "url": url, "sha256": digest, "bytes": path.stat().st_size})

    data, metadata = pyreadstat.read_sav(str(CACHE / "bichler-data.sav"))
    groups = []
    for (condition, pressure), group in data.groupby(["Cond", "TimeP"], dropna=False):
        groups.append({
            "Cond": int(condition), "TimeP": int(pressure),
            "n_analysis": len(group),
            "KPost_nonmissing": int(group.KPost.notna().sum()),
            "KPost_mean": float(group.KPost.mean()),
            "KPre_mean": float(group.KPre.mean()),
            "KDiff_mean": float(group.KDiff.mean()),
            "CL_nonmissing_by_task": {f"CL{i}": int(group[f"CL{i}"].notna().sum()) for i in range(1, 7)},
            "WMC_missing": int(group.WMC_mean.isna().sum()),
        })
    assert sum(g["n_analysis"] for g in groups) == 231
    assert all(g["n_analysis"] == g["KPost_nonmissing"] for g in groups)
    max_gain_residual = float((data.KPost - data.KPre - data.KDiff).abs().max())
    assert max_gain_residual < 1e-10
    replication = data.loc[data.TimeP == 0]
    comparison = [
        {"field": "PS/no-pressure KPre", "paper_Table_B2": 4.75,
         "public_data_mean": float(replication.loc[replication.Cond == 0, "KPre"].mean()),
         "agreement_at_2_decimals": False},
        {"field": "PS/no-pressure KPost", "paper_Table_B2": 8.16,
         "public_data_mean": float(replication.loc[replication.Cond == 0, "KPost"].mean()),
         "agreement_at_2_decimals": True},
        {"field": "PS/no-pressure KDiff", "paper_Table_B2": 3.59,
         "public_data_mean": float(replication.loc[replication.Cond == 0, "KDiff"].mean()),
         "agreement_at_2_decimals": True},
    ]
    write("bichler-analysis-aggregate.json", {
        "source_url": "https://osf.io/mykxc/", "source_sha256": INPUTS["bichler-data.sav"][1],
        "rows": len(data), "columns": len(data.columns),
        "full_row_duplicate_count": int(data.duplicated().sum()),
        "participant_key_present": False, "assignment_roster_present": False,
        "submission_time_present": False, "author_binary_final_pass_present": False,
        "same_wide_analysis_row": ["Cond", "TimeP", "KPre", "KPost", "KDiff"],
        "groups": groups, "max_KPost_minus_KPre_minus_KDiff": max_gain_residual,
        "paper_data_comparison": comparison,
        "critical_warning": "KPost is a 0–26 score with no original binary pass cutoff. CL1–CL6 are cognitive-load responses, not validated on-time submission flags. Whole-row duplicates do not identify unique people without an ID. Analysis rows exclude participants before publication.",
    })
    write("bichler-data-schema-audit.json", {
        "source_url": "https://osf.io/mykxc/", "rows": len(data), "columns": len(data.columns),
        "column_names_to_labels": dict(zip(metadata.column_names, metadata.column_labels)),
        "value_labels": metadata.variable_value_labels,
        "missing_by_column": {c: int(data[c].isna().sum()) for c in data},
        "distinct_values_by_column": {c: int(data[c].nunique()) for c in data},
    })

    accuracy = pd.read_csv(CACHE / "pillai-accuracy-e2.csv")
    ratings = pd.read_csv(CACHE / "pillai-ratings-e2.csv").rename(columns={"Subj_ID": "ID"})
    strategies_raw = pd.read_csv(CACHE / "pillai-strategies-e2.csv").rename(columns={"Subj_ID": "ID"})
    blank_rows = int(strategies_raw.isna().all(axis=1).sum())
    strategies = strategies_raw.dropna(how="all")
    joins = []
    for name, right in [("ratings", ratings), ("strategies", strategies)]:
        joined = accuracy.merge(right, on=["ID", "Condition"], how="left", validate="one_to_one", indicator=True)
        joins.append({
            "right_file": name, "left_basis": "published analyzed accuracy file, not assignment roster",
            "left_rows": len(accuracy), "right_rows": len(right), "after_rows": len(joined),
            "matched": int((joined._merge == "both").sum()),
            "left_unmatched": int((joined._merge == "left_only").sum()),
            "right_IDs_absent_on_left": len(set(right.ID) - set(accuracy.ID)),
            "duplicate_IDs_left": int(accuracy.ID.duplicated().sum()),
            "duplicate_IDs_right": int(right.ID.duplicated().sum()),
        })
        assert len(joined) == 112 and joins[-1]["matched"] == 112
    means = accuracy.groupby("Condition")[["Pretest", "Imm_Old", "Imm_Transfer", "Imm_Avg", "Del_Old", "Del_Transfer", "Del_Avg"]].mean()
    write("pillai-analysis-aggregate.json", {
        "study_id": "DX-E02", "selected_slot": False,
        "source_package": "https://osf.io/85tye/",
        "files": {"accuracy": {"rows": len(accuracy), "columns": list(accuracy.columns)},
                  "ratings": {"rows": len(ratings), "columns": list(ratings.columns)},
                  "strategies": {"rows_before_blank_removal": len(strategies_raw),
                                 "all_blank_rows_removed": blank_rows, "rows_after": len(strategies),
                                 "columns": list(strategies.columns)}},
        "condition_counts": {str(k): int(v) for k, v in accuracy.Condition.value_counts().items()},
        "missing_accuracy": {c: int(accuracy[c].isna().sum()) for c in accuracy},
        "joins": joins, "means": means.to_dict(orient="index"),
        "source_count_inconsistency": {"recruited_reported": 143,
            "reported_exclusions": [16, 11, 3], "arithmetic_remaining": 143 - 16 - 11 - 3,
            "analyzed_reported_and_public_rows": 112,
            "unexplained_count_difference": 1},
        "limits": ["No original assignment roster or excluded-person condition breakdown.",
                   "No submission timestamps; preregistration explicitly excludes people who ran out of time.",
                   "Do not add a new whole-test binary pass cutoff to accuracy proportions.",
                   "Imm_Old and Del_Old have eighth-step values despite four old problems in text; no item rubric/codebook was recovered to justify turning proportions into integer correct-item counts.",
                   "This is an outside-sample diagnostic; it does not fill E01 or D01."],
    })
    write("audit-crossdomain-receipt.json", {
        "checked_utc": datetime.now(timezone.utc).isoformat(), "exit_code": 0,
        "command": "python -B docs/workstreams/research/AF-RES-054/streams/crossdomain/audit_crossdomain.py",
        "inputs": inputs,
        "software": {"python": sys.version.split()[0], "pandas": pd.__version__, "pyreadstat": pyreadstat.__version__},
        "checks": ["Pinned public-file hashes match", "Bichler four cell counts sum to 231",
                   "Bichler score differences agree row-wise", "Pillai analyzed-file joins are one-to-one and complete",
                   "Original assignment join and joint pass-by-deadline calculations not performed because required inputs are absent"],
    })
    print("E01: 231 analysis rows; no assignment-left joint endpoint. DX-E02: 112 one-to-one analysis joins; 2 blank rows removed. Hash and arithmetic checks passed.")


if __name__ == "__main__":
    main()
