"""Generate the fixed experiment cases and predictions before pointer playback."""

import csv
import hashlib
import json
import random
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixture"
MODULES = [
    "Map.js", "MapBrowserEvent.js", "MapBrowserEventHandler.js",
    "interaction/Translate.js", "interaction/Pointer.js", "interaction/DragPan.js",
    "interaction/Select.js", "events/condition.js", "renderer/Map.js",
    "renderer/canvas/VectorLayer.js", "render/canvas/ExecutorGroup.js", "View.js",
    "util.js",
]
BOUNDARY = {"6.6.1", "6.7.0"}
SUPPLEMENT_LIST_ONLY = {
    "cell": "list-only", "collection": "included", "filter": "omitted", "layers": "omitted",
    "hitTolerance": 5,
}


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def version_pins(row):
    version = row["version"]
    with tarfile.open(ROOT / ".scratch" / "npm-artifacts" / f"ol-{version}.tgz", "r:gz") as package:
        names = MODULES + (["PluggableMap.js", "MapBrowserPointerEvent.js"] if version == "6.0.0" else [])
        hashes = {name: hashlib.sha256(package.extractfile("package/" + name).read()).hexdigest()
                  for name in names}
    assert hashes["interaction/Translate.js"] == row["translate_sha256"]
    return {
        "npm_alias": "ol-" + version.replace(".", "-"),
        "git_commit": row["tag_commit"] or row["npm_git_head"],
        "npm_tarball": row["tarball_url"],
        "npm_integrity": row["tarball_integrity"],
        "tarball_sha256": row["tarball_sha256"],
        "package_files": hashes,
        "translate_condition": row["translate_condition"],
        "select_null_style": version != "6.0.0",
        "filter_with_features": row["filter_with_features"],
        "layers_with_features": row["layers_with_features"],
    }


def predict(case, version):
    """Infer minima from hit eligibility, then infer gesture ownership."""
    has_collection = case["collection"] != "omitted"
    layer_enabled = (case["layers"] != "omitted" and version["layers_with_features"] != "option-absent"
                     and not (has_collection and version["layers_with_features"] == "collection-first"))
    filter_enabled = (case["filter"] != "omitted" and version["filter_with_features"] != "option-absent"
                      and not (has_collection and version["filter_with_features"] == "collection-first"))
    layer_pass = not layer_enabled or case["layers"] == "allow"
    hit = case["position"] == "feature"
    translate_active = case["translateActive"]
    candidate_reaches_filter = translate_active and hit and layer_pass
    filter_pass = not filter_enabled or case["filter"] == "allow"
    accept = candidate_reaches_filter and filter_pass and case["collection"] != "empty"
    measure = case["observers"]
    filter_min = (">=1" if candidate_reaches_filter and filter_enabled else "0") if measure else "unobserved"
    layer_min = (">=1" if translate_active and layer_enabled else "0") if measure else "unobserved"
    category = "stable-both"
    if case["gesture"] == "drag":
        category = "geometry-only" if accept else "center-only"
    return {
        "run_id": case["id"], "version": case["version"], "mode": case["mode"], "cell": case["cell"],
        "repeat": case["repeat"], "collection": case["collection"], "filter": case["filter"],
        "layers": case["layers"], "predicted_hit": "parcel-01/owned" if hit else "none",
        "predicted_translate_accept": accept,
        "filter_down_min": filter_min, "layers_down_min": layer_min,
        "filter_total_min": filter_min, "layers_total_min": layer_min, "category": category,
        "rationale": "Translate accepts before pan" if accept else "Translate passes to pan or absent",
    }


def main():
    plan = json.loads((FIXTURE / "input.json").read_text())
    versions = json.loads((ROOT / "evidence" / "release-rules.json").read_text())["browser_versions"]
    with (ROOT / "releases.csv").open() as stream:
        pins = {row["version"]: version_pins(row) for row in csv.DictReader(stream)
                if row["version"] in versions}
    write_json(FIXTURE / "versions.json", pins)
    cases = []
    rng = random.Random(plan["seed"]["executionOrderSeed"])
    for mode in ("main", "controls", "supplement", "bare"):
        batch = []
        for version in versions:
            if mode in ("supplement", "bare") and version not in BOUNDARY:
                continue
            if mode == "bare":
                specifications = [row for row in plan["main"] if row["cell"] in plan["wrapperFreeCells"]]
            else:
                specifications = plan[mode]
                if mode == "supplement":
                    specifications = [*specifications, SUPPLEMENT_LIST_ONLY]
            repeats = plan["wrapperFreeRepeats"] if mode == "bare" else plan["repeats"]
            for row in specifications:
                for repeat in range(1, repeats + 1):
                    batch.append({
                        "id": f"{mode}-{version}-{row['cell']}-r{repeat}",
                        "mode": mode, "version": version, "repeat": repeat, "observers": mode != "bare",
                        "translateActive": True, "collection": "omitted", "filter": "allow", "layers": "allow",
                        "position": "feature", "gesture": "drag", "hitTolerance": plan["hitToleranceCssPx"],
                        **row,
                    })
        rng.shuffle(batch)
        cases.extend(batch)
    write_json(FIXTURE / "cases.json", cases)
    rows = [predict(case, pins[case["version"]]) for case in cases]
    with (ROOT / "predictions.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
