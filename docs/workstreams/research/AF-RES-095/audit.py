"""Verify committed primary evidence and recalculate result counts and table 2."""

import argparse
import json
import re
from collections import Counter
from tempfile import TemporaryDirectory
from pathlib import Path

import pymupdf

from experiment import HERE, PLAN, digest, save_json
from measure import read_pdf

ZONE_KEYS = ("top", "interior", "bottom")
MATRIX = HERE / "evidence/matrix"


def rows_from(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def close(a, b, tolerance):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(close(x, y, tolerance) for x, y in zip(a, b))
    if type(a) != type(b):
        return False
    if isinstance(a, float):
        return abs(a - b) <= tolerance
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(close(a[k], b[k], tolerance) for k in a)
    return a == b


def validate_row(run, templates, environment, reread):
    run_id = run["run_id"]
    evidence = MATRIX / run_id
    assert PLAN["input_sha256"][run["input"]["file"]] == run["input"]["sha256"], run_id
    assert digest(HERE / "fixtures" / run["input"]["file"]) == run["input"]["sha256"], run_id
    for file, sha in run["evidence_index"].items():
        assert digest(evidence / file) == sha, (run_id, file)
    for artifact in run["files"].values():
        file = evidence / artifact["file"]
        assert file.stat().st_size == artifact["bytes"] and digest(file) == artifact["sha256"], file
    assert run["statuses"]["attempted"] and run["execution"]["exit_code"] == 0, run_id
    assert len(run["engine"]["execve"]) == 2 and len(run["pandoc"]["execve"]) == 1, run_id
    assert environment["binaries"]["bundled_pandoc"]["path"] in run["pandoc"]["execve"][0], run_id
    assert run["engine"]["program"] == environment["binaries"]["xelatex"]["path"], run_id
    assert run["pandoc"]["reader"]["exit_code"] == 0, run_id
    assert run["detector"]["exit_code"] == 0, run_id
    debug_log = (evidence / "render.stderr.txt").read_text()
    assert "Quarto version: 1.4.553" in debug_log and "Success: false" not in debug_log, run_id
    assert "to: latex" in (evidence / "pandoc-defaults.yml").read_text(), run_id
    report = (evidence / "document.tex-log.txt").read_text()
    for line in ("LaTeX2e <2024-11-01> patch level 2", "Package: booktabs 2020/01/12 v1.61803398"):
        assert line in report, (run_id, line)
    fls = (evidence / "document.fls").read_text().splitlines()
    for item in environment["tex_locator_observations"].values():
        if item["role"] == "runtime input":
            assert "INPUT " + item["file"]["path"] in fls, run_id
    staged = json.loads((evidence / "pandoc-stage.json").read_text())
    assert all(staged[name]["sha256"] == sha for name, sha in templates.items()), run_id
    for name in templates:
        assert f"/{name} from " in debug_log, (run_id, name)
    tex = (evidence / "document.tex").read_text().splitlines()
    assert all(tex[item["line"]-1] == item["text"] for item in run["tex_locations"]), run_id

    raw = json.loads((evidence / "pdf-raw.json").read_text())
    expected = {name: PLAN["expected_tables"][name] for name in PLAN["conditions"][run_id[0]]}
    assert list(run["tables"]) == list(raw["tables"]) == list(expected), run_id
    ast = json.loads((evidence / "reader.json").read_text())
    ast_tables = [block["c"] for block in ast["blocks"] if block["t"] == "Table"]
    assert [len(table[3][1]) for table in ast_tables] == [0] + [1] * (len(expected) - 1), run_id
    if reread:
        with TemporaryDirectory(prefix="af-res-095-audit-") as directory:
            scratch = Path(directory)
            recomputed = read_pdf(evidence / "document.pdf", expected, scratch, scratch)
            assert close(raw["drawings"], recomputed["drawings"], 0.01), run_id
            assert close(raw["words"], recomputed["words"], 0.01), run_id
            assert close(raw["tables"], recomputed["tables"], 0.01), run_id
    for name, item in run["tables"].items():
        full = raw["tables"][name]
        assert json.loads((evidence / f"{name}.json").read_text()) == full, (run_id, name)
        assert full["vector_raster_agree"] and item["status"] == "readable", (run_id, name)
        assert item["rows"] == full["rows"] == expected[name]["rows"] and item["cells_match"], (run_id, name)
        assert item["vector"] == full["vector"], (run_id, name)
        assert [item["rules_by_zone"][zone] for zone in ZONE_KEYS] == [
            sum(vector["zone"] == zone for vector in full["vector"]) for zone in ZONE_KEYS
        ], (run_id, name)
        desired = list(expected[name]["baseline_rules"])
        if run_id.split("-")[1] != "O":
            desired[0] = desired[2] = 0
        assert list(item["rules_by_zone"].values()) == desired, (run_id, name)
    assert {item["text"] for item in run["negatives"]} == {"1", "Test"}, run_id
    assert all(item["vector"] == item["raster"] == 0 for item in run["negatives"]), run_id
    with pymupdf.open(evidence / "document.pdf") as pdf:
        metadata = pdf.metadata
        creation = metadata["creationDate"]
        trailer_ids = re.search(r"/ID\s*\[\s*<([^>]+)>\s*<([^>]+)>", pdf.pdf_trailer())
    return dict(tables=raw["tables"], words=raw["words"], drawings=raw["drawings"],
                creation_date=creation, trailer_ids=list(trailer_ids.groups()) if trailer_ids else None)


def count_evidence(rows, raw_pages):
    source_rows = rows_from(HERE / "sources.jsonl")
    assert len({source["id"] for source in source_rows}) == len(source_rows)
    counted = [source for source in source_rows if source["counted"]]
    assert len({source["source_url"] for source in counted}) == len(counted)
    source_groups = dict(Counter(source["category"] for source in counted))
    for category, minimum in {"Stack Overflow": 2, "Quarto": 6, "Pandoc": 6,
                               "TeX/PDF": 6, "CSS": 2, "Calc": 2}.items():
        assert source_groups[category] >= minimum
    calibration = json.loads((HERE / "evidence/calibration/calibration.json").read_text())
    assert calibration["ruler"]["passed"] and calibration["original"]["passed"]
    repeats = []
    for left, right in zip(rows[::2], rows[1::2]):
        a, b = left["run_id"], right["run_id"]
        assert a[:-1] == b[:-1] and a.endswith("1") and b.endswith("2")
        measurements = ("tables", "words", "drawings")
        repeats.append(dict(ids=[a, b], measured_equal=all(
            close(raw_pages[a][key], raw_pages[b][key], PLAN["repeat_coordinate_tolerance_pt"])
            for key in measurements
        ), pdf_bytes_equal=left["files"][".pdf"]["sha256"] == right["files"][".pdf"]["sha256"]))
    variants_equal = []
    for condition in ("S", "D"):
        for repeat in (1, 2):
            ids = [f"{condition}-Z-{repeat}", f"{condition}-T-{repeat}"]
            a, b = (raw_pages[run_id] for run_id in ids)
            variants_equal.append(dict(ids=ids, measured_equal=all(
                close(a[key], b[key], PLAN["repeat_coordinate_tolerance_pt"])
                for key in ("tables", "words", "drawings")
            )))
    edits = [row for row in rows if row["run_id"].split("-")[1] != "O"]
    edited_controls = [row["tables"]["control"] for row in edits if "control" in row["tables"]]
    all_tables = [table for row in rows for table in row["tables"].values()]
    original_controls = [row for row in rows if row["run_id"].split("-")[1] == "O"]
    changed_target = [row["tables"]["target"] for row in edits]
    return {
        "planned_render_slots": len(PLAN["run_ids"]), "actual_renders": len(rows),
        "pdfs": sum(".pdf" in row["files"] for row in rows),
        "detected_tables": sum(table["status"] == "readable" for table in all_tables),
        "planned_tables": sum(len(PLAN["conditions"][run[0]]) for run in PLAN["run_ids"]),
        "retained_cell_tables": sum(table["cells_match"] for table in all_tables),
        "retained_cell_count": sum(sum(len(r) for r in table["rows"]) for table in all_tables if table["cells_match"]),
        "positive_original_renders": len(original_controls),
        "target_outer_removed": sum(
            item["cells_match"] and item["rules_by_zone"] == dict(top=0, interior=0, bottom=0)
            for item in changed_target
        ),
        "target_variant_slots": len(changed_target),
        "control_spread": sum(item["rules_by_zone"] == dict(top=0, interior=1, bottom=0)
                              for item in edited_controls),
        "control_spread_denominator": len(edited_controls),
        "repeat_pairs": repeats, "macro_variant_pairs": variants_equal,
        "pdf_distinct_shas": len({row["files"][".pdf"]["sha256"] for row in rows}),
        "pdf_metadata": {key: dict(creation_date=value["creation_date"], trailer_ids=value["trailer_ids"])
                         for key, value in raw_pages.items()},
        "failures": {flag: sum(bool(row["statuses"][flag]) for row in rows) for flag in (
            "render_exit_failure", "engine_error", "tex_warnings", "pdf_missing", "detection_failure", "cell_loss"
        )},
        "negative_windows": sum(len(row["negatives"]) for row in rows),
        "source_ledger_rows": len(source_rows), "qualified_primary_materials": len(counted),
        "source_group_counts": source_groups, "independent_event_groups": len({source["event_id"] for source in counted}),
        "original_author_success_rate": "산출 불가 (환경·명령·출력 완비 분모 0)",
    }


def check_supplemental():
    probes = HERE / "evidence/probes"
    rows = {row["run_id"]: row for row in rows_from(probes / "probes.jsonl")}
    assert len(rows) == 11
    for run_id in ("P-LOCAL-Z", "P-LOCAL-T", "P-HEADER-T", "P-INCLUDE-T", "P-TRACE-T"):
        row = rows[run_id]
        assert row["execution"]["exit_code"] == 0
        assert all(table["cells_match"] for table in row["tables"].values())
        counts = [list(row["tables"][key]["rules_by_zone"].values()) for key in ("target", "control")]
        assert counts == [[0, 0, 0], [1, 1, 1] if "LOCAL" in run_id else [0, 1, 0]], run_id
    trace = (probes / "P-TRACE-T/document.tex-log.txt").read_text()
    assert trace.count(r"A=[\noalign ] B=[]") == 4
    tabular = [rows[f"P-TABULAR-{variant}"] for variant in ("O", "Z", "T")]
    assert all(row["execution"]["exit_code"] == 0 for row in tabular)
    assert "Stable" in tabular[0]["text"] and "Stable" in tabular[1]["text"]
    assert "\nable\n71" in tabular[2]["text"] and "Stable" not in tabular[2]["text"]
    assert "[1.6pt] Widths" in tabular[1]["text"] and ".6pt] Widths" in tabular[2]["text"]
    assert abs(tabular[1]["before_after_y_delta_pt"] - tabular[2]["before_after_y_delta_pt"] - 8) < 0.01
    last = rows["P-BARE-BOTTOM-T"]
    assert last["execution"]["exit_code"] == 1 and ".pdf" not in last["files"] and last["errors"]
    for variant in "OZ":
        row = rows[f"P-BARE-BOTTOM-{variant}"]
        assert row["execution"]["exit_code"] == 0 and ".pdf" in row["files"]
    replay = rows_from(probes / "engine-replay.jsonl")
    assert len(replay) == 6
    for row in replay:
        assert row["input_sha256"] == digest(MATRIX / row["input_run_id"] / "document.tex")
        assert [len(p["warnings"]) for p in row["passes"]] == [4, 0]
        assert [p["exit_code"] for p in row["passes"]] == [0, 0]

    cross = HERE / "evidence/cross"
    css = json.loads((cross / "css.json").read_text())
    for key, expected in {"baseline": [2, 2], "all-hidden": [0, 0], "one-hidden": [0, 2],
                          "none-conflict": [2, 2], "hidden-conflict": [0, 2]}.items():
        tables = css["conditions"][key]["tables"]
        assert [len(table["blue_bands_y_px"]) for table in tables] == expected
        assert [table["rows"] for table in tables] == [
            [["Alpha", "411"], ["Beta", "522"]], [["Delta", "633"], ["Epsilon", "744"]]
        ]
    assert css["wpt"]["exact_raster_match"]
    calc = json.loads((cross / "calc.json").read_text())
    for name, counts in {"shared-on": [5, 5], "shared-off": [0, 0], "split": [5, 0],
                         "one-explicit": [3, 0]}.items():
        row = calc["results"][name]
        assert row["exit_code"] == 0
        assert digest(cross / f"{name}.ods") == row["ods_sha256"]
        assert digest(cross / f"{name}.pdf") == row["pdf_sha256"]
        pages = row["pages"]
        assert [len(page["drawings"]) for page in pages] == counts
        assert [page["text"].split() for page in pages] == [
            ["Alpha", "411", "Beta", "522"], ["Delta", "633", "Epsilon", "744"]
        ]
    red = calc["results"]["one-explicit"]["pages"][0]["drawings"]
    assert len({tuple(drawing["rect"]) for drawing in red}) == 2


def result_row(run):
    run_id = run["run_id"]
    condition, variant, repeat = run_id.split("-")
    folder = f"evidence/matrix/{run_id}"
    title = (
        f"[{run_id}]({folder}/) · "
        f"{'한 표' if condition == 'S' else '두 표'} · "
        f"{dict(O='원본', Z='무인수', T='두 인수')[variant]} · {repeat}"
    )
    parts = []
    for name, table in run["tables"].items():
        lines = []
        for zone in ZONE_KEYS:
            points = [rule for rule in table["vector"] if rule["zone"] == zone]
            portion = f"{dict(top='상',interior='내',bottom='하')[zone]} {len(points)}"
            for rule in points:
                portion += f" @ {rule['y']:.3f}/{rule['thickness']:.4f}"
            lines.append(portion)
        cells = " → ".join("/".join(cell) for cell in table["rows"])
        label = "대상" if name == "target" else "대조"
        part = f"[{label}]({folder}/{name}.json) " + " · ".join(lines)
        if table["vector"]:
            a, b = table["vector"][0]["x"]
            part += f", x {a:.3f}–{b:.3f}"
        parts.append(part + f" · {cells} ([이미지]({folder}/{name}.png))")

    definition = [line["line"] for line in run["tex_locations"]
                  if line["text"].startswith(r"\renewcommand")]
    location = "booktabs L55, " + (f"재정의 L{definition[0]}–{definition[-1]}" if definition else "재정의 없음")
    regions = [line["line"] for line in run["tex_locations"] if "longtable}" in line["text"]]
    for start, end in zip(regions[::2], regions[1::2]):
        calls = [str(line["line"]) for line in run["tex_locations"] if start < line["line"] < end
                 and r"\noalign" in line["text"]]
        location += f"; {start}–{end}행 호출 {','.join(calls)}"
    return "| " + " | ".join([
        title, "Quarto 1.4.553 / 번들 Pandoc 3.1.11 / XeTeX ×2 / 0",
        f"[{location.replace(';', ' ·')}]({folder}/document.tex#L55)", "<br>".join(parts),
        f"[PDF]({folder}/document.pdf) · [TeX 로그]({folder}/document.tex-log.txt) · [실행]({folder}/process.txt)",
        "최종 경고 0 · 셀 손실 0",
    ]) + " |"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-metrics", action="store_true")
    parser.add_argument("--reread-pdfs", action="store_true")
    options = parser.parse_args()
    rows = rows_from(HERE / "runs.jsonl")
    assert [row["run_id"] for row in rows] == PLAN["run_ids"]
    environment = json.loads((HERE / "environment.json").read_text())
    templates = {name: item["staged_sha256"] for name, item in environment["templates"].items()}
    raw_pages = {row["run_id"]: validate_row(row, templates, environment, options.reread_pdfs) for row in rows}
    metrics = count_evidence(rows, raw_pages)
    check_supplemental()
    path = HERE / "metrics.json"
    if options.write_metrics:
        save_json(path, metrics)
    else:
        assert json.loads(path.read_text()) == metrics
        result = (HERE / "RESULT.md").read_text()
        table = result.split("## 표 2", 1)[1].split("## 표 3", 1)[0]
        assert [line for line in table.splitlines() if line.startswith("| [")] == [result_row(r) for r in rows]
    digest_summary = {key: metrics[key] for key in (
        "planned_render_slots", "actual_renders", "pdfs", "detected_tables", "retained_cell_count",
        "target_outer_removed", "control_spread", "qualified_primary_materials", "independent_event_groups"
    )}
    digest_summary["repeat_pairs_agree"] = sum(row["measured_equal"] for row in metrics["repeat_pairs"])
    print(json.dumps(digest_summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
