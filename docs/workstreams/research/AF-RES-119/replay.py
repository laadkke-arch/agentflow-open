"""Render each sealed fixture twice, retain raw artifacts and compare visible SVG records."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
ENGINE_FILES = {
    "v55": ["vega-lite", "vega"],
    "v417": ["vega-lite", "vega"],
    "v56": ["vega-lite", "vega"],
    "m93": ["@mermaid-js/mermaid-cli", "mermaid", "puppeteer"],
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def normalized_local(tag):
    return tag.rsplit("}", 1)[-1]


def json_sha(item):
    return sha(json.dumps(item, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode())


def svg_records(raw):
    root = ET.fromstring(raw)
    if normalized_local(root.tag) != "svg":
        raise ValueError("CLI did not emit an SVG root")
    root_id = root.get("id")
    replacement = "$svg" if root_id else None
    records = []

    def normal(s):
        if root_id and s:
            return re.sub(rf"(?<=#){re.escape(root_id)}\b", replacement, s)
        return s

    def visit(element, path, parent_class):
        tag = normalized_local(element.tag)
        attrs = dict(element.attrib)
        cls = attrs.get("class", "")
        label = "".join(element.itertext()).strip() if tag in ("text", "title", "desc", "foreignObject", "style") else ""
        observations = {
            "xml_path": path, "tag": tag, "attributes": attrs, "text": label, "parent_class": parent_class,
        }
        records.append(observations)
        counts = {}
        for child in element:
            subtag = normalized_local(child.tag)
            counts[subtag] = counts.get(subtag, 0) + 1
            visit(child, f"{path}/{subtag}[{counts[subtag]}]", cls or parent_class)

    visit(root, "/svg", "")
    canonical = []
    for r in records:
        a = {key: normal(value) for key, value in r["attributes"].items()}
        if r["xml_path"] == "/svg" and root_id:
            a["id"] = replacement
        canonical.append({**r, "attributes": a, "text": normal(r["text"]) if r["tag"] == "style" else r["text"]})
    return records, json_sha(canonical)


def commands(engine, directory, op, flags, mermaid_backend):
    bins = engine / "node_modules" / ".bin"
    if op["engine"] == "m93":
        if mermaid_backend == "browser-script":
            return [
                ("svg", ["node", str(ROOT / "mermaid-render.cjs"), str(engine), "input.mmd", "output.svg",
                         str(flags["mermaid"]), str(flags["puppeteer"])]),
            ]
        return [
            ("svg", [str(bins / "mmdc"), "-i", "input.mmd", "-o", "output.svg",
                     "-c", str(flags["mermaid"]), "-p", str(flags["puppeteer"]), "-b", "transparent",
                     "-w", "800", "-H", "600"]),
        ]
    cmds = [
        ("svg", [str(bins / "vl2svg"), directory.name + (".jsonc" if op["file"].endswith(".jsonc") else ".json"),
                 "output.svg", "-b", str(ROOT / "fixtures" / "data") + "/", "-c", str(flags["vega"])]),
    ]
    if op["id"] in ("V8627", "V8628"):
        cmds.append(("vg", [str(bins / "vl2vg"), directory.name + ".json", "output.vg.json", "-p", "-c", str(flags["vega"])]))
    if op["id"] == "V8628":
        cmds.append(("active", ["node", str(ROOT / "vega-active.cjs"), str(engine), "output.vg.json",
                                str(ROOT / "fixtures" / "data") + "/", "active.svg"]))
    return cmds


def run_operation(op, iteration, args, env, configs):
    id = op["id"]
    variant = op["variant"]
    directory = args.out / f"r{iteration}" / f"{id}-{variant}"
    directory.mkdir(parents=True, exist_ok=False)
    source = ROOT / op["file"]
    raw = source.read_bytes()
    if sha(raw) != op["sha256"]:
        raise ValueError(f"sealed fixture changed: {source}")
    copy_name = "input.mmd" if op["engine"] == "m93" else directory.name + source.suffix
    (directory / copy_name).write_bytes(raw)
    commands_run = []
    for kind, command in commands(args.engines / op["engine"], directory, op, configs, args.mermaid_backend):
        run = subprocess.run(command, cwd=directory, env=env, capture_output=True, timeout=55, check=False)
        for stream in ("stdout", "stderr"):
            (directory / f"{kind}.{stream}.txt").write_bytes(getattr(run, stream))
        commands_run.append({
            "artifact_type": kind, "argv": command, "exit_code": run.returncode,
            "stdout": run.stdout.decode("utf-8", "replace"),
            "stderr": run.stderr.decode("utf-8", "replace"),
        })
    svg = directory / "output.svg"
    parsed, fingerprint, failure = [], None, None
    source_artifact = None
    raw_svg_xml_error = None
    browser_xml = directory / "output.browser.xml"
    if svg.exists():
        try:
            parsed, fingerprint = svg_records(svg.read_bytes())
            source_artifact = svg.name
        except (ET.ParseError, ValueError) as err:
            raw_svg_xml_error = str(err)
            if browser_xml.exists():
                parsed, fingerprint = svg_records(browser_xml.read_bytes())
                source_artifact = browser_xml.name
            else:
                failure = raw_svg_xml_error
    else:
        failure = "no SVG artifact"
    active = directory / "active.svg"
    active_records = svg_records(active.read_bytes())[0] if active.exists() else []
    vg = directory / "output.vg.json"
    output_files = {file.name: {"sha256": sha(file.read_bytes()), "bytes": file.stat().st_size}
                    for file in sorted(directory.iterdir()) if file.name != copy_name}
    if vg.exists():
        compiled = json.loads(vg.read_text())
        compiled_summary = {
            "signal_names": [s["name"] for s in compiled.get("signals", [])],
            "interaction_signals": [
                s for s in compiled.get("signals", [])
                if "brush" in s.get("name", "") or "translate" in s.get("name", "")
            ],
            "scales": compiled.get("scales", []),
        }
    else:
        compiled_summary = None
    return {
        **op, "iteration": iteration, "work_dir": str(directory), "commands": commands_run,
        "outputs": output_files, "parsed_svg": fingerprint is not None, "svg_failure": failure,
        "normalized_svg_sha256": fingerprint, "svg_objects": parsed, "compiled": compiled_summary,
        "svg_record_source": source_artifact, "raw_svg_xml_error": raw_svg_xml_error,
        "active_svg_marks": [r for r in active_records if "role-mark" in r["parent_class"] and r["tag"] == "path"],
        "input_copy_name": copy_name, "raw_receipt_dir": f"evidence/render/r{iteration}/{directory.name}",
    }


def configuration(root, chromium):
    values = {
        "vega": {"font": "DejaVu Sans"},
        "mermaid": {"fontFamily": "DejaVu Sans", "deterministicIds": True,
                    "deterministicIDSeed": "af-res-119", "securityLevel": "strict"},
        "puppeteer": {
            "executablePath": chromium, "headless": True,
            "args": ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage",
                     "--disable-background-networking", "--disable-gpu"],
        },
    }
    paths = {}
    for kind, value in values.items():
        path = root / f"{kind}.json"
        path.write_text(json.dumps(value, indent=2) + "\n")
        paths[kind] = path
    return paths, values


def variations(runs):
    results = []
    baselines = {(r["id"], r["iteration"]): r for r in runs if r["variant"] == "base"}
    for r in runs:
        ref = baselines[r["id"], r["iteration"]]
        before = (ROOT / ref["file"]).read_bytes()
        after = (ROOT / r["file"]).read_bytes()
        changed = [
            {"op": op, "baseline_bytes": [i, j], "edited_bytes": [k, l],
             "baseline_raw": before[i:j].decode("utf-8", "replace"),
             "edited_raw": after[k:l].decode("utf-8", "replace")}
            for op, i, j, k, l in difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes() if op != "equal"
        ]
        results.append(dict(r, storage_byte_diff=changed, base_sha256=ref["sha256"]))
    return results


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument("--engines", type=Path, required=True, help="prefix with version-pinned npm install folders")
    ap.add_argument("--out", type=Path, required=True, help="new scratch output directory")
    ap.add_argument("--chromium", default="/usr/bin/chromium")
    ap.add_argument("--font", type=Path, default=Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    ap.add_argument("--mermaid-backend", choices=("browser-script", "mmdc"), default="browser-script")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--id", action="append", help="run only selected cases")
    ap.add_argument("--publish", action="store_true", help="copy raw artifacts and ledger into owned evidence")
    args = ap.parse_args()
    args.engines = args.engines.resolve()
    args.out = args.out.resolve()
    if args.publish and args.id:
        ap.error("--publish requires the complete matrix")
    args.out.mkdir(parents=True, exist_ok=False)
    cfgs, cfg_values = configuration(args.out, args.chromium)
    env = dict(os.environ, TZ="UTC", LANG="C.UTF-8", LC_ALL="C.UTF-8")
    env.update(XDG_CACHE_HOME=str(args.out / "cache"), XDG_CONFIG_HOME=str(args.out / "config"))
    versions = {
        engine: {
            pkg: json.loads((args.engines / engine / "node_modules" / pkg / "package.json").read_text())["version"]
            for pkg in packages
        }
        for engine, packages in ENGINE_FILES.items()
    }
    versions["node"] = subprocess.check_output(["node", "--version"], text=True).strip()
    versions["chromium"] = subprocess.check_output([args.chromium, "--version"], text=True).strip()
    mermaid_bundle = args.engines / "m93" / "node_modules" / "@mermaid-js" / "mermaid-cli" / "dist"
    versions["mmdc_inline_bundle_sha256"] = sha((mermaid_bundle / "index.html").read_bytes())
    direct_bundle = args.engines / "m93" / "node_modules" / "mermaid" / "dist" / "mermaid.min.js"
    versions["mermaid_direct_bundle_sha256"] = sha(direct_bundle.read_bytes())
    versions["font_file"] = {"path": str(args.font), "sha256": sha(args.font.read_bytes())}
    operations = json.loads((ROOT / "fixtures" / "operations.json").read_text())
    applicable = [op for op in operations if not args.id or op["id"] in args.id]
    tasks = [(op, iteration) for iteration in (1, 2) for op in applicable]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        runs = list(pool.map(lambda row: run_operation(*row, args, env, cfgs), tasks))
    runs = variations(runs)
    for run in runs:
        run["versions"] = versions[run["engine"]]
        run["normalization"] = "SVG tree order and raw attrs; replace root id and CSS/url fragment prefix only; use Chromium DOM XML when author htmlLabels require it; hash canonical JSON"
    run_file = args.out / "runs.jsonl"
    run_file.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in runs))
    matrix_summary = {"engines": versions, "configuration": cfg_values,
                      "mermaid_backend": args.mermaid_backend,
                      "timezone": env["TZ"], "locale": env["LC_ALL"],
                      "planned_attempts": len(tasks), "parsed_svg_attempts": sum(r["parsed_svg"] for r in runs),
                      "svg_failures": [f"{r['id']}:{r['variant']}:r{r['iteration']}" for r in runs if not r["parsed_svg"]]}
    smoke = args.out / "matrix.json"
    smoke.write_text(json.dumps(matrix_summary, ensure_ascii=False, indent=2) + "\n")
    if args.publish:
        target = ROOT / "evidence" / "render"
        target.mkdir(exist_ok=False)
        for run in runs:
            raw_dir = ROOT / run["raw_receipt_dir"]
            raw_dir.mkdir(parents=True, exist_ok=False)
            src = Path(run["work_dir"])
            for output in run["outputs"]:
                shutil.copyfile(src / output, raw_dir / output)
        shutil.copyfile(run_file, ROOT / "runs.jsonl")
        shutil.copyfile(smoke, ROOT / "evidence" / "render-matrix.json")
    print(json.dumps(matrix_summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
