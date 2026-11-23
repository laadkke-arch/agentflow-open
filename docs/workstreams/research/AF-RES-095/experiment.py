"""Run the AF-RES-095 matrix, calibration, or a separate diagnostic fixture."""

import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from measure import CENTER_ERROR_PT, DPI, read_pdf

HERE = Path(__file__).resolve().parent
PLAN = json.loads((HERE / "fixtures/plan.json").read_text(encoding="utf-8"))
OPTIONS = ["--to", "pdf", "-M", "keep-tex:true", "-M", "latex-clean:false",
           "-M", "latex-auto-install:false", "--pdf-engine-opt=-recorder", "--log-level", "debug"]
TEMPLATE_FILES = (
    "after-body.tex", "before-bib.tex", "before-body.tex", "before-title.tex", "biblio.tex",
    "citations.tex", "doc-class.tex", "graphics.tex", "pandoc.tex", "tables.tex",
    "template.patched", "tightlist.tex", "title.tex", "toc.tex",
)
TEMP_FILE = re.compile(r"quarto-(?:defaults.*\.yml|metadata.*\.yml|input.*\.md)")
TEX_KEY = re.compile(r"booktabs|\\(?:toprule|midrule|bottomrule|noalign|begin\{document\}|"
                     r"(?:begin|end)\{(?:longtable|tabular)\}|endhead|endlastfoot|subsubsection)")
TEX_ISSUE = re.compile(r"(?:^!|Warning:|Overfull|Underfull|Fatal error|Missing character:)", re.I)


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_env(work, shared):
    env = dict(os.environ)
    for key in ("QUARTO_PANDOC", "QUARTO_BIN_PATH", "QUARTO_SHARE_PATH", "QUARTO_TINYTEX", "TEXINPUTS"):
        env.pop(key, None)
    env.update(PATH="/usr/bin:/bin", TZ="UTC", LC_ALL="C.UTF-8")
    for key, path in {
        "TMPDIR": work / "temp",
        "XDG_CACHE_HOME": shared / "cache",
        "XDG_CONFIG_HOME": shared / "config",
        "XDG_DATA_HOME": shared / "data",
        "TEXMFVAR": shared / "texmf-var",
        "TEXMFCONFIG": shared / "texmf-config",
    }.items():
        path.mkdir(parents=True, exist_ok=True)
        env[key] = str(path)
    return env


def snapshot_pandoc_inputs(temp, captured):
    for path in sorted(temp.glob("quarto-session*/*/**/*")):
        if not (path.name in TEMPLATE_FILES or TEMP_FILE.fullmatch(path.name)):
            continue
        try:
            raw = path.read_bytes()
        except (FileNotFoundError, IsADirectoryError):
            continue
        if raw or path.name in TEMPLATE_FILES:
            (captured / path.name).write_bytes(raw)


def execute(args, work, evidence, env, captured=None):
    started = utc()
    timed_out = False
    with (evidence / "render.stdout.txt").open("wb") as out, (evidence / "render.stderr.txt").open("wb") as err:
        try:
            with subprocess.Popen(args, cwd=work, env=env, stdout=out, stderr=err, start_new_session=True) as proc:
                deadline = time.monotonic() + 120
                while proc.poll() is None:
                    if captured is not None:
                        snapshot_pandoc_inputs(Path(env["TMPDIR"]), captured)
                    if time.monotonic() > deadline:
                        os.killpg(proc.pid, signal.SIGKILL)
                        timed_out = True
                        break
                    time.sleep(0.015)
                rc = proc.wait()
        except OSError as exception:
            err.write(str(exception).encode("utf-8"))
            rc = None
    return dict(argv=args, cwd=str(work), exit_code=rc, timed_out=timed_out,
                started_utc=started, finished_utc=utc())


def trace_excerpt(trace, dest):
    lines = trace.read_text(encoding="utf-8", errors="replace").splitlines()
    selected = [
        line for line in lines
        if ("execve(" in line and line.endswith("= 0") and
            re.search(r'(?:/|")(?:(?:pandoc|xelatex|xdvipdfmx|tlmgr|quarto|deno))"', line))
        or ("openat(" in line and "O_RDONLY" in line and "ENOENT" not in line and
            ("/share/formats/pdf/pandoc/" in line or "template.patched" in line or "booktabs.sty" in line))
    ]
    dest.write_text("\n".join(selected) + "\n", encoding="utf-8")
    return selected


def record_pandoc_inputs(captured, evidence):
    stage = {}
    for path in sorted(captured.iterdir()):
        stage[path.name] = dict(sha256=digest(path), bytes=path.stat().st_size)
        for field, suffix in (("input", ".md"), ("metadata", ".yml"), ("defaults", ".yml")):
            if path.name.startswith("quarto-" + field) and path.name.endswith(suffix):
                name = "pandoc-" + field + suffix
                shutil.copyfile(path, evidence / name)
                stage[path.name]["file"] = name
    save_json(evidence / "pandoc-stage.json", stage)


def copy_outputs(work, evidence, stem):
    out = {}
    for suffix in (".pdf", ".tex", ".fls", ".log"):
        source = work / (stem + suffix)
        if not source.is_file():
            continue
        name = source.name if suffix != ".log" else f"{stem}.tex-log.txt"
        target = evidence / name
        shutil.copyfile(source, target)
        out[suffix] = dict(file=name, sha256=digest(target), bytes=target.stat().st_size)
    return out


def reader_probe(executable, evidence, work, env):
    markdown = evidence / "pandoc-input.md"
    if not markdown.is_file():
        return dict(exit_code=None, error="actual staged Markdown unavailable")
    share = executable.parents[3] / "share"
    metadata = evidence / "pandoc-metadata.yml"
    if not metadata.is_file():
        return dict(exit_code=None, error="actual staged metadata unavailable")
    # The primary PDF run records its actual Lua reader and filter trace.
    # This auxiliary pass changes only the sink and uses empty filter params.
    probe_env = dict(env, QUARTO_SHARE_PATH=str(share), QUARTO_FILTER_PARAMS="e30=")
    args = [str(executable), "--from", str(share / "filters/qmd-reader.lua"), "--to=json",
            "--data-dir", str(share / "pandoc/datadir"), "--metadata-file", str(metadata), str(markdown)]
    output = evidence / "reader.json"
    with output.open("wb") as out, (evidence / "reader.stderr.txt").open("wb") as err:
        rc = subprocess.run(args, cwd=work, env=probe_env, stdout=out, stderr=err, check=False).returncode
    return dict(argv=args, exit_code=rc, file=output.name, sha256=digest(output),
                boundary="same staged Markdown and metadata, bundled Qmd reader, empty filter params, before Quarto main.lua")


def run_quarto(run_id, source, expected, quarto, work_root, evidence_root):
    work = work_root / run_id
    work.mkdir()
    evidence = evidence_root / run_id
    evidence.mkdir(parents=True)
    input_file = work / "document.qmd"
    shutil.copyfile(source, input_file)
    env = render_env(work, work_root / "shared")
    trace = work / "process.strace"
    quarto_args = [str(quarto), "render", input_file.name, *OPTIONS]
    args = ["/usr/bin/strace", "-f", "-s", "8192", "-y", "-e", "trace=execve,openat",
            "-o", str(trace), *quarto_args]
    captured = work / "captured"
    captured.mkdir()
    receipt = execute(args, work, evidence, env, captured=captured)
    record_pandoc_inputs(captured, evidence)
    files = copy_outputs(work, evidence, "document")
    trace_lines = trace_excerpt(trace, evidence / "process.txt") if trace.exists() else []
    renderer_lines = [line for line in trace_lines if "execve(" in line and '/xelatex"' in line]
    pandoc_lines = [line for line in trace_lines if "execve(" in line and '/pandoc"' in line]
    phase_log = (evidence / "render.stderr.txt").read_text(encoding="utf-8", errors="replace").splitlines()
    tex_path = evidence / "document.tex"
    tex_lines = [dict(line=n, text=line) for n, line in enumerate(
        tex_path.read_text(encoding="utf-8").splitlines(), 1) if TEX_KEY.search(line)] if tex_path.exists() else []
    log_path = evidence / "document.tex-log.txt"
    log_lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines() if log_path.exists() else []
    issues = [dict(line=n, text=line) for n, line in enumerate(log_lines, 1) if TEX_ISSUE.search(line)]
    tables = {}
    detector = dict(exit_code=None, error="PDF missing")
    negatives = []
    if ".pdf" in files:
        try:
            metrics = read_pdf(evidence / "document.pdf", expected, evidence, work)
            save_json(evidence / "pdf-raw.json", metrics)
            for name, result in metrics["tables"].items():
                save_json(evidence / f"{name}.json", result)
            detector = dict(exit_code=0, file="pdf-raw.json", sha256=digest(evidence / "pdf-raw.json"),
                            dpi=DPI, rasterizer=metrics["rasterizer"])
            tables = {name: {key: result.get(key) for key in (
                "status", "error", "rows", "rules_by_zone", "vector", "raster", "region_pt",
                "columns_pt", "cell_rows", "heading_bbox_pt", "crop"
            )} for name, result in metrics["tables"].items()}
            for name, item in tables.items():
                if item["raster"] is not None:
                    item["raster"] = {key: value for key, value in item["raster"].items()
                                      if key != "longest_dark_each_y_px"}
                item["cells_match"] = item["rows"] == expected[name]["rows"]
            negatives = [dict(text=item["text"], vector=len(item["vector"]), raster=len(item["raster"]["stripes"]))
                         for item in metrics["negatives"]]
        except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
            detector = dict(exit_code=1, error=str(error))
    executable = quarto.parent / "tools/x86_64/pandoc"
    reader = reader_probe(executable, evidence, work, env)
    statuses = {
        "attempted": receipt["exit_code"] is not None,
        "render_exit_failure": receipt["exit_code"] != 0,
        "engine_invoked": bool(renderer_lines),
        "engine_error": any(line["text"].startswith("!") or "Fatal error" in line["text"] for line in issues)
                        or (bool(renderer_lines) and any("Success: false" in line for line in phase_log)),
        "tex_warnings": [line for line in issues if not line["text"].startswith("!")],
        "pdf_missing": ".pdf" not in files,
        "detection_failure": detector["exit_code"] != 0 or
                             any(item["status"] != "readable" for item in tables.values()),
        "cell_loss": any(item["rows"] is not None and not item["cells_match"] for item in tables.values()),
    }
    return dict(run_id=run_id, input=dict(file=source.name, sha256=digest(input_file), bytes=input_file.stat().st_size),
                quarto_argv=quarto_args, execution=receipt, statuses=statuses,
                engine={"execve": renderer_lines, "program": "/usr/bin/xelatex" if renderer_lines else None},
                pandoc={"execve": pandoc_lines, "reader": reader},
                files=files, tex_locations=tex_lines, detector=detector, tables=tables,
                negatives=negatives, evidence_index={p.name: digest(p) for p in sorted(evidence.iterdir()) if p.is_file()})


def calibration(quarto, work_root, evidence_root):
    evidence = evidence_root / "CAL-RULER"
    work = work_root / "CAL-RULER"
    evidence.mkdir(parents=True)
    work.mkdir()
    source = HERE / "fixtures/ruler.tex"
    shutil.copyfile(source, work / source.name)
    env = render_env(work, work_root / "shared")
    args = ["/usr/bin/xelatex", "-interaction=batchmode", "-halt-on-error", "-recorder", "ruler.tex"]
    receipt = execute(args, work, evidence, env)
    outputs = copy_outputs(work, evidence, "ruler")
    data = read_pdf(evidence / "ruler.pdf", {}, evidence, work, calibration=True)
    save_json(evidence / "pdf-raw.json", data)
    known = data["tables"]["known_rule"]
    vector_shape = [[*rule["x"], rule["y"], rule["thickness"]] for rule in known["vector"]]
    negative = {item["text"]: [len(item["vector"]), len(item["raster"]["stripes"])] for item in data["negatives"]}
    passes = (receipt["exit_code"] == 0 and known["vector_raster_agree"] and len(known["vector"]) == 1 and
              all(abs(x - y) < 0.02 for x, y in zip(vector_shape[0], [72, 144, 143.6, 0.8])) and
              negative == {"OutsideTitle 987": [0, 0], "underline-length decoy": [0, 0], "page-edge decoy": [0, 1]})
    pilot = run_quarto("CAL-ORIGINAL", HERE / "fixtures/P2-original-dual.qmd", PLAN["expected_tables"],
                       quarto, work_root, evidence_root)
    pilot_passes = pilot["execution"]["exit_code"] == 0 and all(
        t["status"] == "readable" and t["cells_match"] and
        list(t["rules_by_zone"].values()) == PLAN["expected_tables"][name]["baseline_rules"]
        for name, t in pilot["tables"].items()
    ) and len(pilot["tables"]) == 2 and all(
        item["vector"] == item["raster"] == 0 for item in pilot["negatives"])
    data = {"dpi": DPI, "max_center_error_pt": CENTER_ERROR_PT,
            "ruler": {"execution": receipt, "files": outputs, "expected_pt": [72, 144, 143.6, 0.8],
                      "negative_counts_vector_raster": negative, "passed": passes},
            "original": {**pilot, "passed": pilot_passes}}
    save_json(evidence_root / "calibration.json", data)
    return 0 if passes and pilot_passes else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("calibrate", "matrix", "probe"))
    parser.add_argument("--quarto", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output-name", default="PROBE")
    args = parser.parse_args()
    quarto, work, evidence = (path.resolve() for path in (args.quarto, args.work, args.evidence))
    work.mkdir(parents=True)
    evidence.mkdir(parents=True)
    if args.mode == "calibrate":
        return calibration(quarto, work, evidence)
    if args.mode == "probe":
        if args.input is None:
            parser.error("probe requires --input")
        row = run_quarto(args.output_name, args.input, PLAN["expected_tables"], quarto, work, evidence)
        save_json(evidence / f"{args.output_name}.json", row)
        code = row["execution"]["exit_code"]
        return 1 if code is None else code
    with (evidence / "runs.jsonl").open("x", encoding="utf-8") as log:
        for run_id in PLAN["run_ids"]:
            condition, variant, _ = run_id.split("-")
            suffix = "-dual" if condition == "D" else ""
            fixture = f"P2-{PLAN['variants'][variant]}{suffix}.qmd"
            source = HERE / "fixtures" / fixture
            if digest(source) != PLAN["input_sha256"][fixture]:
                raise ValueError(f"fixture bytes differ from the committed plan: {fixture}")
            expected = {name: PLAN["expected_tables"][name] for name in PLAN["conditions"][condition]}
            row = run_quarto(run_id, source, expected, quarto, work, evidence)
            log.write(json.dumps(row, ensure_ascii=False) + "\n")
            log.flush()
            print(run_id, row["execution"]["exit_code"], {
                name: item["rules_by_zone"] for name, item in row["tables"].items()
            }, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
