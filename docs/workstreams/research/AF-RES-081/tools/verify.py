#!/usr/bin/env python3
"""Audit the sealed experiment and optionally compare a fresh replay."""
import argparse
from collections import Counter
from contextlib import redirect_stdout
import datetime as dt
import hashlib
import io
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from compare import PACKET, markdown, read_jsonl, summarize, verified_file


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--replay", type=Path, help="new output directory created by run_matrix.py")
    cli.add_argument("--pixels", action="store_true", help="recompute PNG regions using Pillow")
    args = cli.parse_args()
    reading = summarize(PACKET)
    assert reading["status"] == {"completed": 36}
    assert reading["readability"] == {"readable": 36}
    assert len(reading["cells"]) == 18
    assert all(cell["repeat_consistency"] == "same" for cell in reading["cells"].values())
    assert all(not r["expectation_differences"] for cell in reading["cells"].values() for r in cell["readings"])

    builds = json.loads((PACKET / "evidence/build/build-info.json").read_text())
    for filename, expected in builds["patch_sha256"].items():
        assert sha(PACKET / "patches" / filename) == expected
    assert sha(PACKET / "fixtures/two-parts.mscx") == builds["fixture_sha256"]
    assert len({proof["binary_sha256"] for proof in builds["variants"].values()}) == 3
    valid_links = {"E01", "E02", "E03", "E04", "E05", "E06"}
    expected_selected = {"E01": "M1", "E03": "M1F", "E04": "M1", "E05": "M1"}
    for cell in reading["cells"].values():
        assert len({r["saved_sha256"] for r in cell["readings"]}) == 1
        for receipt, r in zip(cell["receipts"], cell["readings"], strict=True):
            assert receipt["case_id"] in valid_links
            assert receipt["source_commit"] == builds["source_commit"]
            assert receipt["binary_sha256"] == builds["variants"][receipt["build"]]["binary_sha256"]
            case = receipt["case_id"]
            selection = {expected_selected[case]: True} if case in expected_selected else {}
            for stage in ("start", "immediate", "after_command"):
                observation = r["stages"][stage]
                assert observation["scores"]["master"]["selection"] == selection
                assert not observation["scores"]["Oboe"]["selection"]
            assert set(receipt["artifacts"]) == {"stdout.jsonl", "stderr.txt", "roundtrip.mscx"}
            for item in receipt["artifacts"].values():
                verified_file(PACKET, item)

    counts = Counter(row["GL"] for row in reading["contrasts"].values())
    assert counts == {"same": 5, "different": 1}
    assert reading["contrasts"]["E05"]["GL"] == "different"
    assert all(row[pair + "_saved_bytes_equal"] for pair in ("UG", "UL", "GL")
               for row in reading["contrasts"].values())
    captured_table = io.StringIO()
    with redirect_stdout(captured_table):
        markdown(reading)
    assert captured_table.getvalue() in (PACKET / "RESULT.md").read_text()

    sources = read_jsonl(PACKET / "sources.jsonl")
    ledger_fields = {"source_id", "lineage_id", "kind", "original_url", "pinned_locator", "read_utc",
                     "qs", "case_ids", "confirmed", "limit", "supports_or_challenges"}
    assert len({row["source_id"] for row in sources}) == len(sources)
    for row in sources:
        assert ledger_fields <= set(row)
        assert dt.datetime.fromisoformat(row["read_utc"]).utcoffset() == dt.timedelta(0)
    lineages = {row["lineage_id"] for row in sources if row["eligible"]}
    fields = {row["lineage_id"] for row in sources if row["eligible"] and row["field"] != "notation"}
    reversals = {row["lineage_id"] for row in sources if row["independent_failure_or_no_change"]}
    assert (len(sources), len(lineages), len(fields), len(reversals)) == (43, 28, 13, 8)

    originals = json.loads((PACKET / "evidence/original-summary.json").read_text())
    original_checks = 0
    for build, data in originals.items():
        directory = PACKET / "evidence/original" / build
        assert int((directory / "exit.txt").read_text()) == data["ctest_exit"] == 0
        assert sha(directory / "ctest.stdout") == data["ctest_stdout_sha256"]
        assert len(data["suites"]) == 7
        for name, suite in data["suites"].items():
            xml_file = directory / f"{name}.xml"
            assert sha(xml_file) == suite["file_sha256"]
            root = ET.parse(xml_file).getroot()
            case_status = Counter(case.attrib["result"] for case in root.findall("testcase"))
            assert case_status == suite["testcase_results"]
            assert set(case_status) == {"pass"}
            assert not list(root.iter("error")) and not list(root.iter("failure"))
            original_checks += 1

    desktop = json.loads((PACKET / "evidence/desktop-pixels.json").read_text())
    assert set(desktop) == {f"{build}-{i}" for build in "UGL" for i in (1, 2)}
    for identifier, record in desktop.items():
        directory = PACKET / "evidence/desktop" / identifier
        assert sha(directory / "steps.txt") == record["steps_sha256"]
        assert record["fixture_sha256"] == builds["fixture_sha256"]
        assert int((directory / "exit.txt").read_text()) == record["exit"] == 0
        for name, proof in record["pixels"].items():
            png = directory / f"{name}.png"
            assert sha(png) == proof["sha256"]
            if args.pixels:
                from PIL import Image
                with Image.open(png) as image:
                    region = image.convert("RGB").crop(proof["rect_ltrb"])
                    pixels = (region.getpixel((x, y)) for y in range(region.height) for x in range(region.width))
                    actual_blue = sum(b > r + 55 and b > g + 28 for r, g, b in pixels)
                assert actual_blue == proof["blue_pixels"]
        blue = [record["pixels"][k]["blue_pixels"] for k in ("master-selected", "flute", "oboe")]
        assert blue == ([65, 65, 0] if identifier.startswith("U") else [65, 0, 0])

    replay_verified = 0
    if args.replay:
        replay = summarize(args.replay)
        assert replay["contrasts"] == reading["contrasts"]
        for cell, pair in reading["cells"].items():
            other = replay["cells"][cell]
            assert other["repeat_consistency"] == "same"
            for before, after in zip(pair["readings"], other["readings"], strict=True):
                for key in ("stages", "saved", "saved_sha256", "expectation_differences"):
                    assert before[key] == after[key], (cell, key)
                replay_verified += 1
    report = {
        "native_cells": len(reading["cells"]),
        "native_completed": reading["status"]["completed"],
        "native_readable": reading["readability"]["readable"],
        "g_l_normalized": counts,
        "independent_sources": len(lineages),
        "cross_field_sources": len(fields),
        "independent_reversals": len(reversals),
        "legacy_suite_targets_passed": original_checks,
        "desktop_completed": len(desktop),
        "pixels_recomputed": args.pixels,
        "fresh_replay_matching_operations": replay_verified,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
