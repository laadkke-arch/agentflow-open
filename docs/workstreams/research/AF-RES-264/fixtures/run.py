"""Run the fixed Pandoc cells and controls in fresh working directories."""
import argparse
import csv
import itertools
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
from dataclasses import dataclass
from importlib.metadata import version as installed_version
from pathlib import Path
from urllib.parse import unquote

from receipt import digest, invoke, utc, write_json

FIXTURES = Path(__file__).resolve().parent
PINS = json.loads((FIXTURES / "downloads.json").read_text())
SHORT = {"2.2.3.2": "2232", "2.3": "23"}
TOKEN = "Archive Contents 264"
TITLE = "Field Notes 264"
HEADINGS = ["Orchard Signals", "Morning Count", "Harbor Bearings", "Evening Log"]
PASSES = 3


@dataclass(frozen=True)
class Case:
    name: str
    version: str
    toc: bool
    meta: str | None
    repeat: int = 1
    template: str = "builtin"
    control: str | None = None
    epoch: int | None = None
    depth: int | None = None


def main_cases():
    for version, toc, meta, repeat in itertools.product(SHORT, (False, True), (None, TOKEN), (1, 2)):
        yield Case(f"v{SHORT[version]}-{'on' if toc else 'off'}-"
                   f"{'unique' if meta else 'none'}-r{repeat}", version, toc, meta, repeat)


def controls():
    yield Case("old-with-new-template", "2.2.3.2", True, TOKEN, template="2.3", control="swap")
    yield Case("new-with-old-template", "2.3", True, TOKEN, template="2.2.3.2", control="swap")
    yield Case("new-without-conditional", "2.3", True, TOKEN, control="drop_conditional")
    yield Case("new-default-title", "2.3", True, "Contents", control="same_as_default")
    yield Case("new-no-bookmarks", "2.3", True, TOKEN, control="no_bookmarks")
    yield Case("new-explicit-toc-bookmark", "2.3", True, TOKEN, control="explicit_bookmark")
    yield Case("new-depth-one", "2.3", True, TOKEN, control="depth", depth=1)
    yield Case("new-epoch-a-r1", "2.3", True, TOKEN, control="epoch", epoch=1704067200)
    yield Case("new-epoch-a-r2", "2.3", True, TOKEN, repeat=2, control="epoch", epoch=1704067200)
    yield Case("new-epoch-b", "2.3", True, TOKEN, control="epoch", epoch=1704153600)


def template_override(case, tools, work):
    if case.template != "builtin":
        return tools / "raw" / ("embedded-" + case.template + ".latex")
    changes = {
        "drop_conditional": (r"$if(toc-title)$" + "\n" + r"\renewcommand*\contentsname{$toc-title$}"
                             + "\n$endif$\n", ""),
        "explicit_bookmark": ("\n" + r"\tableofcontents" + "\n",
                              "\n" + r"\pdfbookmark[1]{Navigation Index 264}{af-res-264-toc}"
                              + "\n" + r"\tableofcontents" + "\n"),
    }
    if case.control not in changes and case.control != "no_bookmarks":
        return None
    raw = (tools / "raw/embedded-2.3.latex").read_text()
    if case.control == "no_bookmarks":
        raw = r"\PassOptionsToPackage{bookmarks=false}{hyperref}" + "\n" + raw
    else:
        original, replacement = changes[case.control]
        if raw.count(original) != 1:
            raise ValueError("Template intervention location is not unique")
        raw = raw.replace(original, replacement)
    destination = work / "control.latex"
    destination.write_text(raw, encoding="utf-8")
    return destination


def read_page_lines(layout):
    found = {"doc_title": [], "toc_heading": [], "toc_entries": [], "body_headings": []}
    pages = layout.split("\f")
    if not pages[-1].strip():
        pages.pop()
    for index, page in enumerate(pages, 1):
        for line, raw in enumerate(page.splitlines(), 1):
            text = raw.strip()
            loc = {"page": index, "layout_line": line, "text": text}
            if text == TITLE:
                found["doc_title"].append(loc)
            elif text in (TOKEN, "Contents"):
                found["toc_heading"].append(loc)
            elif text in HEADINGS:
                found["body_headings"].append(loc)
            else:
                for heading in HEADINGS:
                    match = re.fullmatch(re.escape(heading) + r"[ .]+(\d+)", text)
                    if match:
                        found["toc_entries"].append(loc | {"label": heading, "printed_page": int(match[1])})
                        break
    return found | {"page_count": len(pages)}


def tex_locations(tex, out):
    lines = tex.splitlines()
    choices = {
        "documentclass": r"^\\documentclass\b", "title": r"^\\title\{",
        "maketitle": r"^\\maketitle\b", "pdftitle": r"\bpdftitle=",
        "contentsname": r"^\\renewcommand\*?\\contentsname\{",
        "tableofcontents": r"^\\tableofcontents\b", "tocdepth": r"^\\setcounter\{tocdepth\}",
        "headings": r"^\\(?:sub)?section\{", "pdfbookmark": r"^\\pdfbookmark\b",
    }
    locations = {name: [i for i, line in enumerate(lines, 1) if re.search(pattern, line)]
                 for name, pattern in choices.items()}
    blocks = []
    for name, selected in locations.items():
        for i in selected:
            blocks.append(f"[{name}] matched L{i}")
            for j in range(max(i - 2, 1), min(i + 2, len(lines)) + 1):
                blocks.append(f"{j:04d} {lines[j - 1]}")
        if not selected:
            blocks.append(f"[{name}] 0 matches")
    out.write_text("\n".join(blocks) + "\n", encoding="utf-8")
    return locations


def ast_fields(ast):
    results = {"api_version": ast["pandoc-api-version"], "meta": ast["meta"], "headings": []}
    for block in ast["blocks"]:
        if block["t"] != "Header":
            continue
        level, attrs, inlines = block["c"]
        title = "".join(inline["c"] if inline["t"] == "Str" else " " for inline in inlines)
        results["headings"].append({"level": level, "id": attrs[0], "text": title})
    return results


def outline_agreement(mupdf, raw_cli, raw_root, pypdf):
    if mupdf["pages"] != len(pypdf["pages"]):
        raise ValueError("The outlines were read against different page counts")
    expected = []
    for m in mupdf["outline"]:
        expected.append((len(m["parents"]) + 1, m["title"], m["uri"]))
    outline_cli = []
    for line in raw_cli.splitlines():
        match = re.fullmatch(r"[+|\-](\t+)(.+)\t([^\t]+)", line)
        if not match:
            raise ValueError("Unrecognized mutool show outline line: " + line)
        outline_cli.append((len(match[1]), json.loads(match[2]), match[3]))
    if expected != outline_cli:
        raise ValueError("MuPDF outline CLI and JS walks differ")
    if len(expected) != len(pypdf["outline"]):
        raise ValueError("MuPDF and pypdf outline node counts differ")
    if (raw_root.strip() == "null") != (pypdf["outline_root_state"] == "absent"):
        raise ValueError("MuPDF and pypdf outline-root presence differs")
    for m, p in zip(mupdf["outline"], pypdf["outline"]):
        dest = p["target"]
        resolved = m["resolved"]
        uri_name = unquote(m["uri"].removeprefix("#nameddest=")) if m["uri"].startswith("#nameddest=") else None
        if (m["title"], m["parents"], uri_name, resolved["page"] + 1, "/" + resolved["type"]) != (
                p["title"], p["parents"], dest["name"], dest["page"], dest["mode"]):
            raise ValueError("Outline title, parent, name, page or mode differ")
        # These recipes use an unrotated article page with media/crop box origin (0,0).
        page = pypdf["pages"][dest["page"] - 1]
        if page["rotate"] or page["crop_box"][:2] != [0, 0] or page["media_box"] != page["crop_box"]:
            raise ValueError("Fixture coordinate transform needs review")
        x, y, zoom = dest["args"]
        actual_x, actual_y = resolved["x"], m["page_bounds"][3] - resolved["y"]
        if abs(x - actual_x) > 0.002 or abs(y - actual_y) > 0.002 or zoom != resolved["zoom"]:
            raise ValueError("Converted PDF destination coordinates differ")
    return {"nodes": len(expected), "root_state": pypdf["outline_root_state"],
            "tolerance_pdf_pt": 0.002, "status": "agree"}


def tool_versions(out, tools, env):
    binaries = {
        "pdflatex": shutil.which("pdflatex"),
        "pdftotext": shutil.which("pdftotext"),
        "pdffonts": shutil.which("pdffonts"),
        "pdfinfo": "/usr/bin/pdfinfo",
        "mutool": str(tools / "bin/mupdf/usr/bin/mutool"),
        "python": sys.executable,
        "kpsewhich": shutil.which("kpsewhich"),
    }
    for version in SHORT:
        binaries["pandoc-" + version] = str(tools / "bin" / ("pandoc-" + version) / "usr/bin/pandoc")
    binary_pins = {"mutool": PINS["mutool_sha256"]}
    for version, spec in PINS["pandoc"].items():
        binary_pins["pandoc-" + version] = spec["binary_sha256"]
        if digest(tools / "raw" / ("embedded-" + version + ".latex")) != spec["template_sha256"]:
            raise ValueError("Pinned template changed")
    if installed_version("pypdf") != PINS["pypdf_version"]:
        raise ValueError("Pinned pypdf not available")
    out.mkdir()
    result = {"binaries": {}, "pypdf": installed_version("pypdf"),
              "environment": {key: env.get(key) for key in ("LC_ALL", "TZ", "TEXMFHOME")}}
    for name, binary in binaries.items():
        entry = result["binaries"][name] = {"path": binary, "sha256": digest(binary)}
        if name in binary_pins and entry["sha256"] != binary_pins[name]:
            raise ValueError(f"Pinned executable changed: {name}")
        flag = "-v" if name in {"pdftotext", "pdffonts", "pdfinfo", "mutool"} else "--version"
        receipt = invoke(out, name + "-version", [binary, flag], cwd=out, env=env)
        entry["version_exit"] = receipt["exit"]
        if receipt["exit"]:
            raise ValueError(f"Version probe failed for {name}")
    details = invoke(out, "system", ["uname", "-srm"], cwd=out, env=env)
    result["system_exit"] = details["exit"]
    shutil.copyfile("/etc/os-release", out / "os-release")
    write_json(out / "environment.json", result)
    return binaries, digest(out / "environment.json")


def read_pdf(case, folder, work, pdf, binaries, env, final):
    mu = binaries["mutool"]
    commands = [
        ("pages", [binaries["pdftotext"], "-layout", "-enc", "UTF-8", pdf, "-"], "pages.txt"),
        ("mutool-outline", [mu, "show", pdf, "outline"], "mutool-outline.txt"),
        ("mutool-root", [mu, "show", pdf, "trailer/Root/Outlines"], "mutool-root.txt"),
        ("mutool-resolved", [mu, "run", FIXTURES / "observe_mupdf.js", pdf], "mutool-resolved.json"),
        ("pypdf", [sys.executable, FIXTURES / "observe_pdf.py", pdf], "pypdf.json"),
    ]
    if final:
        commands += [
            ("bbox", [binaries["pdftotext"], "-bbox-layout", "-enc", "UTF-8", pdf, "-"], "bbox.html"),
            ("pdfinfo", [binaries["pdfinfo"], "-isodates", "-box", pdf], "pdfinfo.txt"),
            ("pdffonts", [binaries["pdffonts"], pdf], "pdffonts.txt"),
            ("mutool-objects", [mu, "show", "-g", pdf, "grep"], "mutool-objects.txt"),
            ("mutool-names", [mu, "show", pdf, "trailer/Root/Names/Dests",
                              "trailer/Root/Names/Dests/Names/*", "trailer/Root/Names/Dests/Kids/*/Names/*",
                              "pages"], "mutool-names.txt"),
            ("mutool-draw", [mu, "draw", "-q", "-F", "png", "-r", "96", "-o",
                             str(work / "draw-%d.png"), pdf], "mutool-draw.stdout"),
        ]
    results = [invoke(folder, name, argv, cwd=work, env=env, output=folder / filename)
               for name, argv, filename in commands]
    failures = [entry["name"] for entry in results if entry["exit"]]
    if failures:
        return {"status": "parser_failed", "failed_commands": failures}

    pages = read_page_lines((folder / "pages.txt").read_text(encoding="utf-8"))
    mp = json.loads((folder / "mutool-resolved.json").read_text(encoding="utf-8"))
    pp = json.loads((folder / "pypdf.json").read_text(encoding="utf-8"))
    try:
        agree = outline_agreement(mp, (folder / "mutool-outline.txt").read_text(encoding="utf-8"),
                                  (folder / "mutool-root.txt").read_text(encoding="utf-8"), pp)
    except ValueError as exc:
        agree = {"status": "disagree", "error": str(exc)}
    detail = dict(status="read" if agree["status"] == "agree" else "parser_disagreement",
                  page=pages, outline_agreement=agree, outline=pp["outline"],
                  pdf_title=pp["metadata"].get("/Title"), pdf_ids_hex=pp["pdf_ids_hex"],
                  pdf_metadata=pp["metadata"], pdf_version=pp["pdf_header"], page_mode=pp["page_mode"],
                  pdf_links=[page["links"] for page in pp["pages"]],
                  pages_text_sha256=digest(folder / "pages.txt"))
    if final:
        detail["png_96dpi_sha256"] = [digest(p) for p in sorted(work.glob("draw-*.png"))]
        detail["bounding_boxes_sha256"] = digest(folder / "bbox.html")
    return detail


def input_manifest(fls):
    unique_files = {}
    for line in fls.read_text().splitlines():
        if not line.startswith("INPUT "):
            continue
        path = Path(line[6:])
        if path.is_absolute() and path.is_file():
            unique_files[str(path)] = digest(path)
    return dict(sorted(unique_files.items()))


def execute(case, tools, out, bins, env, env_sha):
    receipt = out / case.name
    receipt.mkdir()
    results = {"case": vars(case), "started_utc": utc(), "environment_sha256": env_sha,
               "input_sha256": digest(FIXTURES / "document.md"),
               "writer_sha256": PINS["pandoc"][case.version]["binary_sha256"], "passes": []}
    with tempfile.TemporaryDirectory(prefix="af264-" + case.name + "-") as temp:
        temp = Path(temp)
        work = temp / "build"
        work.mkdir()
        results["fresh_initial_entries"] = sorted(entry.name for entry in work.iterdir())
        env = env.copy()
        env["TEXMFHOME"] = str(work / "empty-data")
        if case.epoch is not None:
            env["SOURCE_DATE_EPOCH"] = str(case.epoch)
        (work / "empty-data").mkdir()
        shutil.copyfile(FIXTURES / "document.md", work / "document.md")
        options = ["--data-dir=empty-data", "-f", "markdown"]
        if case.toc:
            options.append("--toc")
        if case.depth is not None:
            options.append(f"--toc-depth={case.depth}")
        if case.meta is not None:
            options.append("--metadata=toc-title:" + case.meta)
        template = template_override(case, tools, work)
        latex_only = ["--template=" + str(template)] if template is not None else []
        if template is not None:
            results["template_sha256"] = digest(template)
        else:
            results["template_sha256"] = PINS["pandoc"][case.version]["template_sha256"]
        pd = bins["pandoc-" + case.version]
        ast = invoke(receipt, "pandoc-ast", [pd, *options, "-t", "json", "document.md"],
                     cwd=work, env=env, output=receipt / "ast.json")
        tex = invoke(receipt, "pandoc-tex", [pd, *options, *latex_only, "-s", "-t", "latex", "document.md"],
                     cwd=work, env=env, output=receipt / "case.tex")
        if ast["exit"] == 0:
            results["ast"] = ast_fields(json.loads((receipt / "ast.json").read_text()))
            results["ast_sha256"] = digest(receipt / "ast.json")
        built = tex["exit"] == 0
        if built:
            results["tex"] = tex_locations((receipt / "case.tex").read_text(), receipt / "tex-context.txt")
            results["tex_sha256"] = digest(receipt / "case.tex")
            shutil.copyfile(receipt / "case.tex", work / "case.tex")

        for number in range(1, PASSES + 1):
            if not built:
                results["passes"].append({"number": number, "status": "not_executed"})
                continue
            folder = temp / f"pass-{number}"
            folder.mkdir()
            state = {"number": number, "previous_aux": sorted(x.name for x in work.glob("case.*"))}
            cmd = [bins["pdflatex"], "-interaction=nonstopmode", "-no-shell-escape",
                   "-halt-on-error", "-file-line-error", "-recorder", "-jobname=case",
                   r"\listfiles\input{case.tex}"]
            state["tex_exit"] = invoke(folder, "pdflatex", cmd, cwd=work, env=env)["exit"]
            state["files"] = {}
            for source in sorted(work.glob("case.*")):
                if source.name == "case.tex":
                    continue
                shutil.copyfile(source, folder / source.name)
                state["files"][source.name] = digest(source)
            built = state["tex_exit"] == 0 and "case.pdf" in state["files"]
            if built:
                state.update(read_pdf(case, folder, work, work / "case.pdf", bins, env, number == PASSES))
                if number == PASSES:
                    write_json(receipt / "tex-inputs.json", input_manifest(work / "case.fls"))
                    log = (work / "case.log").read_text()
                    file_list = log.split(" *File List*\n", 1)[1].split("***********", 1)[0]
                    (receipt / "latex-file-list.txt").write_text(file_list, encoding="utf-8")
                    shutil.copyfile(work / "case.pdf", receipt / "case.pdf")
                    public = ("pages.txt", "bbox.html", "pdfinfo.txt", "pdffonts.txt", "mutool-outline.txt",
                              "mutool-root.txt", "mutool-resolved.json", "mutool-objects.txt",
                              "mutool-names.txt", "pypdf.json")
                    for filename in public:
                        if (folder / filename).is_file():
                            shutil.copyfile(folder / filename, receipt / filename)
                    if template is not None:
                        results["template_input"] = template.name
            else:
                state["status"] = "tex_failed"
            write_json(folder / "pass.json", state)
            results["passes"].append(state)

        with tarfile.open(receipt / "passes.tar.gz", "w:gz", compresslevel=9) as archive:
            for folder in sorted(temp.glob("pass-*")):
                archive.add(folder, arcname=folder.name)
    results["status"] = ("observed" if ast["exit"] == 0 and
                         all(item["status"] == "read" for item in results["passes"]) else "partial")
    results["ended_utc"] = utc()
    write_json(receipt / "run.json", results)
    return results


def matrix_csv(out, results):
    fields = ["case_id", "pandoc_version", "toc", "toc_title_cli", "repeat", "status",
              "document_sha256", "pandoc_sha256", "template_sha256", "environment_sha256",
              "ast_sha256", "ast_toc_title", "tex_sha256", "tex_locations", "pass_exit_codes",
              "final_pdf_sha256", "page_count", "document_title_page", "toc_heading_page", "toc_entries_page",
              "body_headings_page", "pdf_metadata_title", "outline_title_parent_destination",
              "outline_agreement", "pdf_ids_hex", "page_raster_sha256", "receipt", "unknown"]
    with (out / "matrix.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in results:
            case, final = row["case"], row["passes"][-1]
            page = final.get("page", {})
            unknown = "" if row["status"] == "observed" else "See run.json for failed or unexecuted commands"
            def encode(value):
                return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            writer.writerow(dict(
                case_id=case["name"], pandoc_version=case["version"], toc=case["toc"],
                toc_title_cli=case["meta"], repeat=case["repeat"], status=row["status"],
                document_sha256=row["input_sha256"], pandoc_sha256=row["writer_sha256"],
                template_sha256=row["template_sha256"], environment_sha256=row["environment_sha256"],
                ast_sha256=row.get("ast_sha256"), ast_toc_title=encode(row.get("ast", {}).get("meta", {}).get("toc-title")),
                tex_sha256=row.get("tex_sha256"), tex_locations=encode(row.get("tex")),
                pass_exit_codes=encode([item.get("tex_exit") for item in row["passes"]]),
                final_pdf_sha256=final.get("files", {}).get("case.pdf"), page_count=page.get("page_count"),
                document_title_page=encode(page.get("doc_title")), toc_heading_page=encode(page.get("toc_heading")),
                toc_entries_page=encode(page.get("toc_entries")), body_headings_page=encode(page.get("body_headings")),
                pdf_metadata_title=final.get("pdf_title"),
                outline_title_parent_destination=encode(final.get("outline")),
                outline_agreement=encode(final.get("outline_agreement")),
                pdf_ids_hex=encode(final.get("pdf_ids_hex")), page_raster_sha256=encode(final.get("png_96dpi_sha256")),
                receipt="receipts/matrix/" + case["name"] + "/run.json", unknown=unknown))


def invalid_pdf(out, tools, env):
    folder = out / "invalid-pdf"
    folder.mkdir()
    pdf = folder / "invalid.pdf.txt"
    pdf.write_text("Intentionally invalid input for the parser-error control.\n")
    mu = tools / "bin/mupdf/usr/bin/mutool"
    outcomes = [
        invoke(folder, "mutool", [mu, "show", pdf, "outline"], cwd=folder, env=env),
        invoke(folder, "pypdf", [sys.executable, FIXTURES / "observe_pdf.py", pdf], cwd=folder, env=env),
    ]
    write_json(folder / "result.json", {"sha256": digest(pdf), "expected_nonzero": True,
                                      "both_nonzero": all(c["exit"] != 0 for c in outcomes)})


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=("matrix", "controls"))
    p.add_argument("--tools", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True)
    tools = args.tools.resolve()
    env = os.environ.copy()
    for key in ("SOURCE_DATE_EPOCH", "FORCE_SOURCE_DATE", "TEXINPUTS", "TEXMFOUTPUT",
                "TEXMFHOME", "TEXMFVAR", "TEXMFCNF", "TEXFORMATS"):
        env.pop(key, None)
    env.update(LC_ALL="C.UTF-8", LANG="C.UTF-8", TZ="UTC",
               LD_LIBRARY_PATH=str(tools / "bin/mupdf/usr/lib/x86_64-linux-gnu"))
    bins, env_sha = tool_versions(out / "environment", tools, env)
    cases = main_cases() if args.mode == "matrix" else controls()
    results = []
    for case in cases:
        result = execute(case, tools, out, bins, env, env_sha)
        results.append(result)
        print(case.name, result["status"], flush=True)
    if args.mode == "matrix":
        matrix_csv(out, results)
    else:
        invalid_pdf(out, tools, env)
    sys.exit(not all(r["status"] == "observed" for r in results))
