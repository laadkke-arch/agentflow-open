"""Audit committed tables, receipts and the second checkout's browser replay."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
from itertools import product
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_bytes())


def rows(path):
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def step_map(raw):
    return {(s["phase"], s["step"]): s for s in raw["snapshots"]}


def event_stable(event):
    return {k: v for k, v in event.items() if k not in ("time", "observedAt")}


def stable_components(raw):
    return {
        "scenario": raw["scenario"], "status": raw["status"], "notices": raw["notices"],
        "chart": {k: v for k, v in raw["chart"].items() if k != "timeOrigin"},
        "compiled": raw["compiledSha256"], "initialization": raw.get("initialization"),
        "inputs": [tuple(t[k] for k in ("phase", "step", "client")) for t in raw["trajectory"]],
        "snapshots": [{k: v for k, v in s.items() if k not in ("raf", "raf2")} for s in raw["snapshots"]],
        "invariants": raw["invariants"], "finalPaint": raw["finalPaintSha256"],
        "callbacks": [event_stable(e) for e in raw["events"]]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", type=Path, help="fresh output containing main/ and controls/")
    parser.add_argument("--out", type=Path, help="write the audit report to this path")
    parser.add_argument("--draft", action="store_true", help="audit receipts before result tables have been written")
    args = parser.parse_args()

    plan = load(ROOT / "plan.json")
    runs = rows(ROOT / "runs.jsonl")
    events = rows(ROOT / "events.jsonl")
    sources = rows(ROOT / "sources.jsonl")
    recorded = Counter((r["variant"], r["renderer"], r["state"], r["position"], r["repeat"])
                       for r in runs if r["kind"] == "main")
    design = product(("original", "local", "shared"), ("svg", "canvas"), ("empty", "active"),
                     ("mark", "plot"), (1, 2))
    assert recorded == Counter(design)
    assert [r["id"] for r in runs] == [c["id"] for mode in ("matrix", "controls") for c in plan["cases"][mode]]
    planned_main = [r for r in runs if r["kind"] == "main"]
    planned_controls = [r for r in runs if r["kind"] == "controls"]
    assert len(planned_main) == 48 and len(planned_controls) == 36
    assert len({r["id"] for r in runs}) == len(runs)
    assert len({s["source_id"] for s in sources}) == len(sources)
    for s in sources:
        assert all(s[k] for k in ("source_id", "lineage_id", "source_url", "publisher",
                                  "read_section", "observation", "limitation", "confirmed_utc", "questions"))
        if s["counted"]:
            assert s["access"] == "read"
    counted = [s for s in sources if s["counted"]]
    assert len({s["lineage_id"] for s in counted}) == len(counted) >= 20

    checked = {}
    discrepancies = []
    replay_hashes = {}
    stage_count = 0
    grouped = {r["id"]: [] for r in runs}
    for event in events:
        grouped[event["run_id"]].append(event)

    for r in runs:
        file = ROOT / r["raw_path"]
        assert sha(file) == r["raw_sha256"]
        raw = checked[r["id"]] = load(file)
        assert raw["scenario"]["id"] == r["id"]
        assert raw["compiledSha256"] == sha(ROOT / "evidence/compiled" / (r["variant"] + ".json"))
        assert sum(bar["count"] for bar in raw["chart"]["bars"]) == 1461
        assert len(raw["chart"]["bars"]) == 54
        assert len(raw["chart"]["scales"]["bands"]) == 12
        if r["state"] == "active":
            assert raw["initialization"]["observed"]["months"] == plan["seed"]["months"]

        stages = step_map(raw)
        for label, derived in r["steps"].items():
            state = stages["test", label]["first"]
            assert state["visual"] == derived["visual"]
            assert state["projected"] == derived["projected_ms"]
            assert Counter(state["fills"].values()) == derived["color_counts"]
            assert state["invariantsSha256"] == derived["invariants_sha256"]
            stage_count += 1
        for item, derived in zip(raw["events"], grouped[r["id"]], strict=True):
            assert derived["raw_sha256"] == r["raw_sha256"]
            assert derived["raw_path"] == r["raw_path"]
            assert all(derived[k] == v for k, v in item.items())
            observed = stages[item["phase"], item["step"]]["first"]
            state = derived["state_after_step"]
            assert state["visual"] == observed["visual"] and state["projected_ms"] == observed["projected"]
            assert state["color_counts"] == Counter(observed["fills"].values())

        if args.replay:
            replay_file = args.replay / r["kind"] / (r["id"] + ".json")
            if not replay_file.exists():
                discrepancies.append({"id": r["id"], "different": ["missing replay file"]})
                continue
            replay_hashes[r["id"]] = sha(replay_file)
            reference = stable_components(raw)
            replayed = stable_components(load(replay_file))
            differences = [k for k in reference if reference[k] != replayed[k]]
            if differences:
                discrepancies.append({"id": r["id"], "different": differences})

    observer_comparisons = []
    for r in planned_controls:
        if r["observers"]:
            continue
        target = f"M-original-{r['renderer']}-empty-mark-{r['repeat']}"
        a, b = checked[r["id"]], checked[target]
        assert len(a["events"]) == 0 and len(b["events"]) > 0
        probe_a, probe_b = step_map(a), step_map(b)
        keys = ("visual", "projected", "fills", "brush", "invariantsSha256")
        matching = all(probe_a["test", phase]["first"][k] == probe_b["test", phase]["first"][k]
                       for phase in ("down", "first", "up") for k in keys)
        observer_comparisons.append({"disabled": r["id"], "enabled": target, "stages_equal": matching,
                                     "final_surface_equal": a["finalPaintSha256"] == b["finalPaintSha256"]})

    tables = None
    if not args.draft:
        result = (ROOT / "RESULT.md").read_text()
        tables = [block.splitlines()[2:] for block in re.findall(r"(?m)(?:^\|[^\n]*\|\n)+", result)]
        assert len(tables[1]) == 24 and len(tables[-1]) == 3
        for r in planned_main:
            assert sum(1 for line in tables[1] if r["raw_path"] in line) == 1
        with (ROOT / "decisions.csv").open(encoding="utf-8", newline="") as f:
            decisions = list(csv.DictReader(f))
        assert {r["run_id"] for r in decisions} == {r["id"] for r in planned_main}
        assert len(decisions) == len(planned_main)
        self_check = (ROOT / "SELF_CHECK.md").read_text()
        assert set(re.findall(r"(?m)^\| (Q[1-7]) ", self_check)) == {f"Q{i}" for i in range(1, 8)}
        for document in ("RESULT.md", "SELF_CHECK.md", "reproduce.md", "evidence/controls/RECEIPT.md",
                         "evidence/cross-domain.md"):
            path = ROOT / document
            for link in re.findall(r"\]\(([^)\s]+)\)", path.read_text()):
                if link.startswith(("https://", "#")):
                    continue
                assert (path.parent / link.split("#", 1)[0]).exists(), (document, link)

    report = {
        "subjects": {"browser_replay": "Codex Cloud task worker", "ledger_audit": "same worker, independent code",
                     "independent_human_or_ai_reader": None},
        "main_rows": len(planned_main), "main_outcomes": Counter(r["status"] for r in planned_main),
        "control_rows": len(planned_controls), "control_outcomes": Counter(r["status"] for r in planned_controls),
        "main_comparable": sum(bool(r.get("comparable")) for r in planned_main),
        "control_comparable": sum(bool(r.get("comparable")) for r in planned_controls),
        "main_first_residual_css_px": Counter(str(r["steps"]["first"]["residual_css_px"]) for r in planned_main),
        "event_rows": len(events), "stage_crosschecks": stage_count, "raw_sha256_matches": len(checked),
        "source_candidate_addresses": len({s["source_url"] for s in sources}),
        "source_read_addresses": len({s["source_url"] for s in sources if s["access"] == "read"}),
        "source_access_failures": len({s["source_url"] for s in sources if s["access"] == "failed"}),
        "unique_primary_works": len(counted), "primary_by_group": Counter(s["group"] for s in counted),
        "required_table_rows": [len(t) for t in tables[:3]] if tables else None,
        "weakness_table_rows": len(tables[-1]) if tables else None,
        "observer_pairs": observer_comparisons, "replayed_receipt_count": len(replay_hashes),
        "replayed_raw_sha256": replay_hashes, "replay_discrepancies": discrepancies,
        "excluded_timing_fields": ["startedUtc", "finishedUtc", "timeOrigin", "time", "observedAt",
                                   "commandedAt", "raf", "raf2"]
    }
    if args.out:
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in ("replayed_raw_sha256", "observer_pairs")},
                     ensure_ascii=False))
    if discrepancies or not all(p["stages_equal"] and p["final_surface_equal"] for p in observer_comparisons):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
