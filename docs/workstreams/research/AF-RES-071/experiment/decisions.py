"""Check each recommendation with its fixed request and a changed local setting."""
from dataclasses import replace
import tempfile
from pathlib import Path

from model import ROOT, baseline, load_json, run_local
from oracle import verify_observation
from run import write_jsonl
from storage import BASIS


def check(output):
    rows = []
    with tempfile.TemporaryDirectory(prefix="af071-condition-") as folder:
        for obj in load_json(ROOT / "inputs" / "objects.json"):
            base = baseline(obj)
            changed_policy = "reverse" if obj["domain"] == "A" else "temperature_only"
            changed = replace(base, id=base.id + ".decision-test", policy=changed_policy, synthetic=True)
            old = run_local(obj, base, base.materialize(Path(folder)), obj["id"] + "/D/old")
            new = run_local(obj, changed, changed.materialize(Path(folder)), obj["id"] + "/D/new")
            for edition, run in ((base, old), (changed, new)):
                verify_observation(obj, edition, run)
            assert old["value"]["reason_holds"] and not new["value"]["reason_holds"]
            rows.append({"id": "DEC-" + obj["id"], "object": obj["id"], "source_id": obj["source"],
                         "recommendation_url": obj["url"], "design": obj["design"],
                         "claimed_condition": BASIS[obj["domain"]], "synthetic": True,
                         "input_change": changed_policy, "source_bytes_changed": base.files != changed.files,
                         "same_request": obj.get("anchor") or obj["window"], "before": old["value"],
                         "after": new["value"], "before_run": old["id"], "after_run": new["id"],
                         "denominator": "supplemental recommendation probes; outside paired-change totals"})
    write_jsonl(output, rows)
    print("recommendation condition changed for 8/8 settings probes")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    check(parser.parse_args().output)
