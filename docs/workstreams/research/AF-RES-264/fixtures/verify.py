"""Validate the archived receipts and compare a full fresh replay to the fixed inputs."""
import argparse
import csv
import hashlib
import json
import re
import tarfile
from collections import Counter
from pathlib import Path

from compare import (compare, control_pairs, main_pairs, mask_pdf_bytes, pdf_geom, read_cases,
                     strip_object_refs)
from receipt import digest
from run import HEADINGS, PASSES, TITLE, TOKEN, controls, main_cases

OWNED = Path(__file__).resolve().parents[1]
EXPECTED_BUCKETS = {"request-change-release": 4, "pandoc-code-template-test": 6,
                    "tex-pdf-parser": 5, "epub": 5}


def require(ok, label):
    if not ok:
        raise ValueError(label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def json_lines(text):
    return [json.loads(line) for line in text.splitlines()]


def pass_archive(folder, summary):
    streams = 0
    with tarfile.open(folder / "passes.tar.gz") as archive:
        for step in summary["passes"]:
            step_id = "pass-" + str(step["number"])

            def read(name):
                with archive.extractfile(step_id + "/" + name) as stream:
                    return stream.read()

            require(step == json.loads(read("pass.json")), f"Pass summary changed in {folder}/{step_id}")
            for name, checksum in step["files"].items():
                require(sha(read(name)) == checksum, f"Output digest changed in {folder}/{step_id}/{name}")
            for command in json_lines(read("commands.jsonl").decode("utf-8")):
                require(command["exit"] == 0, f"Command failure in {folder}/{step_id}/{command['name']}")
                for name in ("stdout", "stderr"):
                    require(sha(read(command[name])) == command[name + "_sha256"],
                            f"Command {name} hash changed in {folder}/{step_id}")
                    streams += 1
    return streams


def check_main(folder, run, case):
    for step in run["passes"]:
        number = step["number"]
        page = step["page"]
        title_list = [line["text"] for line in page["doc_title"]]
        require(title_list == [TITLE] and step["pdf_title"] == TITLE, f"Document title changed: {folder}")
        require(page["page_count"] == 1, f"Page count changed: {folder}")
        require([line["text"] for line in page["body_headings"]] == HEADINGS, f"Missing body headings: {folder}")
        caption = [TOKEN if case.version == "2.3" and case.meta else "Contents"] if case.toc else []
        require([line["text"] for line in page["toc_heading"]] == caption, f"Page TOC title mismatch: {folder}")
        entries = HEADINGS if case.toc and number > 1 else []
        require([line["label"] for line in page["toc_entries"]] == entries, f"Page TOC entries mismatch: {folder}")
        require(all(line["printed_page"] == 1 for line in page["toc_entries"]), f"Wrong printed page number: {folder}")
        nodes = [] if number == 1 else HEADINGS
        expected_root = "absent" if number == 1 else "populated"
        require(step["outline_agreement"]["root_state"] == expected_root, f"Unexpected outline state: {folder}")
        require([node["title"] for node in step["outline"]] == nodes, f"Outline nodes mismatch: {folder}")
        expected_parents = [] if number == 1 else [[], [HEADINGS[0]], [], [HEADINGS[2]]]
        require([node["parents"] for node in step["outline"]] == expected_parents, f"Outline parents mismatch: {folder}")
    key = run["ast"]["meta"].get("toc-title")
    require(key == ({"t": "MetaString", "c": TOKEN} if case.meta else None), f"AST toc-title mismatch: {folder}")
    require(bool(run["tex"]["tableofcontents"]) == case.toc, f"TeX TOC macro mismatch: {folder}")
    require(bool(run["tex"]["contentsname"]) == (case.version == "2.3" and case.toc and bool(case.meta)),
            f"TeX contentsname mismatch: {folder}")


def check_case(folder, run, case, environment):
    require(run["case"] == vars(case) and run["status"] == "observed", f"Unexpected case or status: {folder}")
    require(run["fresh_initial_entries"] == [], f"Working directory was not initially empty: {folder}")
    require(run["environment_sha256"] == digest(environment), f"Environment hash differs: {folder}")
    require(run["input_sha256"] == digest(OWNED / "fixtures/document.md"), f"Different fixture: {folder}")
    require(len(run["passes"]) == PASSES, f"Pass count differs: {folder}")
    for index, step in enumerate(run["passes"], 1):
        require(step["number"] == index and step["tex_exit"] == 0, f"Build failed: {folder} pass {index}")
        require(step["outline_agreement"]["status"] == "agree", f"Parsers disagree: {folder} pass {index}")
    require(run["passes"][0]["previous_aux"] == ["case.tex"], f"Stale TeX files before pass 1: {folder}")
    final = run["passes"][-1]
    require(digest(folder / "case.pdf") == final["files"]["case.pdf"], f"Final PDF hash differs: {folder}")
    require(digest(folder / "ast.json") == run["ast_sha256"], f"AST hash differs: {folder}")
    require(digest(folder / "case.tex") == run["tex_sha256"], f"TeX hash differs: {folder}")
    for command in json_lines((folder / "commands.jsonl").read_text()):
        require(command["exit"] == 0, f"Pandoc failed: {folder}")
        for stream in ("stdout", "stderr"):
            require(digest(folder / command[stream]) == command[stream + "_sha256"],
                    f"Pandoc {stream} hash differs: {folder}")
    return pass_archive(folder, run)


def check_ledger():
    ledger = json_lines((OWNED / "sources.jsonl").read_text())
    fields = {"source_id", "work_id", "lineage_id", "bucket", "q", "case", "url", "publisher", "version_or_sha",
              "publication_date", "checked_utc", "location", "observed", "units", "evidence_type",
              "limit_or_alternative", "access", "counted", "count_reason"}
    require(all(fields <= row.keys() for row in ledger), "Source ledger field missing")
    require(len({row["source_id"] for row in ledger}) == len(ledger), "Repeated source IDs")
    counted = [row for row in ledger if row["counted"]]
    require(len(counted) == len({row["work_id"] for row in counted}), "Duplicated counted work")
    require(all(row["access"] == "성공" for row in counted), "Failed access counted")
    buckets = Counter(row["bucket"] for row in counted)
    require(all(buckets[key] >= value for key, value in EXPECTED_BUCKETS.items()), "Source minimum missing")
    lineages = {row["lineage_id"] for row in counted}
    print(f"Sources: {len(ledger)} ledger rows, {len(counted)} counted works, {len(lineages)} lineages, {dict(buckets)}")


def check_report():
    text = (OWNED / "RESULT.md").read_text()
    tables = re.findall(r"(?:^\|.*\|\n)+", text, re.M)
    require(text.startswith("| 판·입력·반복 |"), "RESULT does not start with Table 1")
    require(tables[1].startswith("| 통제·바꾼 한 가지 |"), "Table 2 is out of order")
    require(tables[-1].startswith("| 가장 중요한 불일치·약점 |") and text.endswith(tables[-1]),
            "Q-end table is not last")
    expect = ((tables[0], 18, 6), (tables[1], 13, 5), (tables[-1], 5, 4))
    for table, lines, columns in expect:
        require(len(table.splitlines()) == lines and all(l.count("|") == columns + 1 for l in table.splitlines()),
                "Mandatory result table dimensions differ")
    require(all(f"## Q{q}." in text for q in range(1, 8)), "Q coverage in RESULT incomplete")

    for path in re.findall(r"\]\(([^)]+)\)", text):
        if not path.startswith("https://"):
            require((OWNED / path.split("#")[0]).exists(), f"Broken local result link: {path}")
    commits = set(re.findall(r"github\.com/laadkke-arch/agentflow-open/blob/([0-9a-f]{40})/", tables[0]))
    require(len(commits) == 1, "Table 1 source links do not share a pinned SHA")
    print("RESULT mandatory tables: 16×6, 11×5, 3×4 data rows; seven questions and local links checked")


def check_comparisons(cases):
    stored = load_json(OWNED / "receipts/comparisons.json")
    actual = [compare(name, a, b, cases) for name, a, b in list(main_pairs()) + list(control_pairs())]
    require(stored == actual, "Comparison receipts do not match archived PDFs")
    repeats = [c for c in actual if c["comparison"] == "independent_repeat"]
    require(len(repeats) == 8 and all(not row["pdf_bytes_equal"] and
            row["pdf_bytes_equal_after_masking_only_literal_dates_and_trailer_id"] for row in repeats),
            "Independent-repeat hashes no longer reproduce recorded mismatch")
    print("Comparisons: 24 fixed pairs, 8 raw-repeat PDF mismatches limited to dates/ID")


def check_epub(out):
    expected = {"cc-shared-culture": (True, 8, 6), "page-blanche": (False, 10, 2)}
    for name, picture in expected.items():
        folder = out / name
        evidence = load_json(folder / "result.json")
        doc = evidence["frozen"]
        toc = next(item for item in doc["nav_sections"] if item["type"] == "toc")
        require((doc["nav_in_spine"], len(doc["spine_sequence"]), len(toc["links"])) == picture,
                f"{name} spine/TOC relation changed")
        require(evidence["views_equal"] and doc == evidence["shipped"], f"{name} shipped XML view differs")
        archive = evidence["epub"]
        require(archive["member_matches_pinned_git_blob"] == {"opf": False, "nav": False}, "Unexpected blob equality")
        require(all(item["equal_after_crlf_to_lf"] for item in archive["member_line_endings"].values()),
                "Released XML differs by more than line endings")
        require(digest(folder / "container.xml") == archive["container_sha256"], "Container checksum changed")


def check_invalid(out):
    folder = out / "invalid-pdf"
    expected = load_json(folder / "result.json")
    require(expected["both_nonzero"] and expected["sha256"] == digest(folder / "invalid.pdf.txt"),
            "Invalid fixture failure receipt missing")
    steps = json_lines((folder / "commands.jsonl").read_text())
    require({step["name"] for step in steps if step["exit"] == 1} == {"mutool", "pypdf"},
            "Invalid input parser exits differ")
    for step in steps:
        require((folder / step["stderr"]).stat().st_size > 0, "No parser error text")


def compare_replay(stored, replay):
    require(stored.keys() == replay.keys(), "Replay case enumeration differs")
    raw_equal = 0
    for name, (folder, original) in stored.items():
        fresh_dir, fresh = replay[name]
        for key in ("input_sha256", "writer_sha256", "template_sha256", "ast_sha256", "tex_sha256"):
            require(original[key] == fresh[key], f"Replay {name} differs in {key}")
        require(load_json(folder / "tex-inputs.json") == load_json(fresh_dir / "tex-inputs.json"),
                f"Replay {name} read different TeX dependencies")
        require(pdf_geom(folder / "bbox.html") == pdf_geom(fresh_dir / "bbox.html"),
                f"Replay {name} page geometry differed")
        first, second = (p.read_bytes() for p in (folder / "case.pdf", fresh_dir / "case.pdf"))
        require(mask_pdf_bytes(first) == mask_pdf_bytes(second), f"Replay {name} changed outside dates and IDs")
        raw_equal += first == second
        for p, q in zip(original["passes"], fresh["passes"]):
            require(p["page"] == q["page"] and p["outline_agreement"] == q["outline_agreement"],
                    f"Replay {name} pass {p['number']} page or agreement differed")
            require(strip_object_refs(p["outline"]) == strip_object_refs(q["outline"]),
                    f"Replay {name} pass {p['number']} outline differed")
        require(original["passes"][-1]["png_96dpi_sha256"] == fresh["passes"][-1]["png_96dpi_sha256"],
                f"Replay {name} raster differed")
    print(f"Replay: {len(replay)} fresh folders, {len(replay) * PASSES} pdflatex passes;"
          f" all AST/TeX and dated/ID-masked final PDFs match; {raw_equal} original byte matches")


def verify(replay):
    root = OWNED / "receipts"
    stored = read_cases(root / "matrix", root / "controls")
    main = list(main_cases())
    control = list(controls())
    require(len(stored) == 26, "Fixed PDF receipt count differs")
    streams = 0
    for group, plan in (("matrix", main), ("controls", control)):
        for case in plan:
            folder, run = stored[case.name]
            streams += check_case(folder, run, case, root / group / "environment/environment.json")
            if group == "matrix":
                check_main(folder, run, case)
    with (OWNED / "matrix.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require([r["case_id"] for r in rows] == [c.name for c in main], "CSV grid or order differs")
    for row in rows:
        folder, run = stored[row["case_id"]]
        require(row["final_pdf_sha256"] == digest(folder / "case.pdf") and row["status"] == "observed",
                "CSV digest/status does not match the archived PDF")
        require(row["receipt"] == str((folder / "run.json").relative_to(OWNED)), "CSV receipt address differs")
    check_ledger()
    check_report()
    check_comparisons(stored)
    check_epub(root / "epub")
    check_invalid(root / "controls")
    print(f"Fixed receipts: 16 matrix, 10 controls, 78 passes, {streams} hashed command streams,"
          " two EPUB observations, two expected invalid-parser exits")
    if replay is not None:
        fresh = read_cases(replay / "matrix", replay / "controls")
        compare_replay(stored, fresh)
        check_invalid(replay / "controls")
        check_epub(replay / "epub")
        for folder in (root / "epub").glob("*/result.json"):
            counterpart = replay / "epub" / folder.parent.name / "result.json"
            require(load_json(folder) == load_json(counterpart), "Replay EPUB read changed")
        print("Replay: both frozen and shipped EPUB XML views, archive hashes and line endings match")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay-root", type=Path)
    args = parser.parse_args()
    verify(args.replay_root)
