"""Cross-check committed AF-RES-217 records in a new process without OCR or network."""

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def csv_rows(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_main(pins, main, runs):
    slots = {}
    verified_paths = 0
    for raw in main:
        row = runs[raw["id"]]
        pin = pins[raw["assets"][0]]
        slot = (pin["id"], raw["oem"])
        assert raw["language"] == pin["language"]
        assert raw["input"]["sha256"] == digest(ROOT / "fixtures/page.png")
        assert raw["environment"].get("TESSDATA_PREFIX") is None
        assert raw["files_before"] == raw["files_after"] == [pin["file"]]
        path, entry = next(iter(raw["inventory"].items()))
        assert len(raw["inventory"]) == 1 and Path(path).parent == Path(raw["tessdata_dir"])
        assert entry["git_blob"] == raw["inventory_after"][path]["git_blob"] == pin["expected_git_blob"]
        assert entry["sha256"] == raw["inventory_after"][path]["sha256"] == pin["sha256"]
        assert entry["bytes"] == raw["inventory_after"][path]["bytes"] == pin["expected_bytes"]
        trace = ROOT / "receipts" / raw["trace"]
        assert digest(trace) == raw["trace_identity"]["sha256"]
        lines = trace.read_text().splitlines()
        calls = [line for line in lines if ".traineddata\"" in line and "open" in line]
        assert calls and all(f'"{path}"' in line and f"<{path}>" in line
                             and re.search(r"= [0-9]+<", line) for line in calls)
        assert any(f"<{path}>" in line and "read(" in line
                   and re.search(r"= [1-9][0-9]*$", line) for line in lines)
        assert row["opened_paths"] == path and pin["sha256"] in row["opened_fingerprints"]
        verified_paths += 1
        supported = not pin["predictions"][str(raw["oem"])].startswith("미지원")
        assert raw["returncode"] == (0 if supported else 1)
        assert row["init"] == ("0" if supported else "-1")
        assert ("components are not present" in raw["stderr"]) == (not supported)
        assert ("Could not initialize tesseract." in raw["stderr"]) == (not supported)
        assert raw["stdout"] == row["stdout_text"]
        assert bool(raw["stdout"].strip()) == supported
        assert int(row["input_read_B"]) > 0 if supported else int(row["input_read_B"]) == 0
        slots.setdefault(slot, {})[raw["repeat"]] = (
            raw["cwd"], raw["returncode"], row["init"], row["stdout_sha256"], row["verdict"]
        )
    assert len(main) == 24 and verified_paths == 24
    assert len({row["cwd"] for row in main}) == 24
    assert set(slots) == {(asset, oem) for asset in pins for oem in (0, 1)}
    for repeat in slots.values():
        assert set(repeat) == {1, 2}
        assert repeat[1][0] != repeat[2][0] and repeat[1][1:] == repeat[2][1:]
    positives = sum(pair[1][2] == "0" for pair in slots.values())
    assert positives == 7
    return {"unique_slots": len(slots), "repeat_pairs_equal": len(slots), "model_paths_read": verified_paths,
            "cli_processes": len(main), "positive_slots": positives, "explicit_negative_slots": len(slots)-positives}


def check_controls(runs, raw_controls):
    missing, malformed = runs["CT01"], runs["CT02"]
    assert missing["verdict"] == "model_path_missing" and "ENOENT" in missing["attempts"] and not missing["opened_paths"]
    assert malformed["verdict"] == "model_parse_rejected" and malformed["opened_paths"] and malformed["bytes_read_by_path"]
    for case, code, explicit, alternate in (("CT03","0","A01","A05"),("CT04","-1","A05","A01")):
        raw = raw_controls[case]
        _, alternative = next(iter(raw["alt_inventory"].items()))
        assert alternative["asset"] == alternate and raw["environment"]["TESSDATA_PREFIX"]
        assert runs[case]["asset_ids"] == explicit and runs[case]["init"] == code
        assert all(path not in runs[case]["attempts"] for path in raw["alt_inventory"])
    blank = runs["CT05"]
    assert blank["init"] == blank["exit"] == "0" and blank["stdout_B"] == "0" and int(blank["input_read_B"]) > 0
    assert runs["CT06"]["exit"] == runs["CT07"]["exit"] == "0"
    assert runs["CT06"]["verdict"] == "partial_language_success"
    assert runs["API-CT06"]["loaded_languages"] == "eng"
    assert runs["API-CT07"]["loaded_languages"] == "eng;ara"
    assert runs["API-A01-OEM0"]["init"] == runs["API-A01-OEM0"]["effective_oem_api"] == "0"
    assert runs["API-A05-OEM0"]["init"] == "-1"
    assert runs["CT08"]["stdout_text"] == "qzxvnotaword\n" and runs["CT08"]["exit"] == "0"
    assert all(runs[case]["exit"] == "1" and "Can't open" in runs[case]["stderr_text"] for case in ("CT09","CT10"))
    scopes = Counter(row["scope"] for row in runs.values())
    assert scopes["controls"] == 10 and scopes["validation"] == 4
    return dict(cli_controls=scopes["controls"], c_abi_probes=scopes["validation"])


def main():
    pins = json.loads((ROOT / "inputs.json").read_text())
    pins = {model["id"]: model for model in pins["models"]}
    data = ROOT / "receipts"
    models = csv_rows("components.csv")
    raw_models = jsonl(data / "components.jsonl")
    assert len(models) == len(raw_models) == 6
    assert all(row["directory_exit"] == row["network_exit"] == "0" and row["status"] == "complete" for row in models)
    assert all(row["file_minus_directory_offsets_B"] == "4" for row in models)
    assert sum(bool(row["legacy_present"]) for row in models) == 1
    assert all(len(row["lstm_present"].split(";")) == 3 for row in models)
    ledger = jsonl(ROOT / "sources.jsonl")
    assert len({row["source_id"] for row in ledger}) == len(ledger)
    selected = [row for row in ledger if row["counted"]]
    assert len({row["work_id"] for row in selected}) == len(selected)
    source_counts = Counter(row["category"] for row in selected)
    assert source_counts["model"] >= 6 and source_counts["collection-readme"] >= 3 and source_counts["engine-source"] >= 6
    assert source_counts["prior-ledger"] + source_counts["public-report"] >= 4
    assert source_counts["hunspell-contract"] + source_counts["hunspell-file"] >= 3
    assert len(selected) >= 22
    runs = {row["run_id"]: row for row in csv_rows("runs.csv")}
    raw_controls = {row["id"]: row for row in jsonl(data / "controls.jsonl")}
    frame = csv_rows("frame.csv")
    assert all(row["status"] != "planned" for row in frame)
    print(json.dumps({"components": len(models), **check_main(pins, jsonl(data/"main.jsonl"), runs),
                      **check_controls(runs, raw_controls), "sources": len(selected),
                      "sources_by_type": source_counts, "source_lineages": len({row["lineage_id"] for row in selected}),
                      "public_cases": source_counts["public-report"], "frame_rows": len(frame)}, sort_keys=True))


if __name__ == "__main__":
    main()
