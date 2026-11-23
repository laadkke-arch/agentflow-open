"""Post-seal Pandoc-stage probes; never updates frozen route judgments.

Requires the official 3.6 binary and R0 API bodies described in binary-receipt.json
and read-log.jsonl. All transient inputs, outputs and compiler files stay in _cache.
No R interpreter or system package installer is invoked.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import html.parser
import json
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CACHE = HERE / "_cache"
PANDOC = CACHE / "pandoc-3.6"
SEAL2 = "d03ca37daf0c43688c68bc39417d84a9b84803e9"


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


class CodeBlocks(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.blocks = []
        self.current = []

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            self.depth += 1
            self.current = []

    def handle_endtag(self, tag):
        if tag == "pre":
            self.blocks.append("".join(self.current))
            self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.current.append(data)


def r0_blocks(filename):
    path = CACHE / "inputs" / filename
    if not path.exists():
        path = ROOT / "evidence/outcomes/_cache" / filename
    data = path.read_bytes()
    parser = CodeBlocks()
    parser.feed(data.decode())
    return parser.blocks, {"source_cache": str(path.relative_to(ROOT)), "sha256": sha(data)}


def execute(args, cwd, label):
    env = os.environ.copy()
    for key, name in [("TMPDIR", "tmp"), ("TEXMFVAR", "texmf-var"), ("TEXMFCONFIG", "texmf-config")]:
        path = CACHE / name
        path.mkdir(exist_ok=True)
        env[key] = str(path)
    record = {"label": label, "command": [str(x) for x in args], "cwd": str(cwd), "started_utc": utc()}
    try:
        proc = subprocess.run([str(x) for x in args], cwd=cwd, env=env, capture_output=True, text=True, timeout=60)
        record.update(exit_code=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
    except subprocess.TimeoutExpired as exc:
        record.update(exit_code=None, timeout_seconds=60, error=str(exc))
    record["finished_utc"] = utc()
    return record


def table_metrics(path, original):
    text = path.read_text()
    match = re.search(r"<table\b.*?</table>", text, re.S)
    table = match.group(0) if match else ""
    return {
        "output_sha256": sha(text.encode()),
        "output_bytes": path.stat().st_size,
        "table_count": len(re.findall(r"<table\b", text)),
        "table_br_count": len(re.findall(r"<br\b", table)),
        "document_br_count": len(re.findall(r"<br\b", text)),
        "tr_count": len(re.findall(r"<tr\b", table)),
        "td_count": len(re.findall(r"<td\b", table)),
        "original_table_byte_equal": table == original,
        "required_text_present": {v: v in table for v in ["Approver 1 Role", "User Name, Approver 2 Role", "14 Jan 2025 13:18", "Date"]},
    }


def main():
    receipt = json.loads((HERE / "binary-receipt.json").read_text())
    assert receipt["matches_frozen_source_sha"]
    assert sha(PANDOC.read_bytes()) == receipt["binary_sha256"]
    report = {
        "started_utc": utc(),
        "classification": "post-seal auxiliary execution, outside A/B four-body budget",
        "pre_judgments_changed": False,
        "binary_sha256": receipt["binary_sha256"],
        "source_sha": receipt["source_sha"],
        "R_end_to_end": False,
        "system_packages_installed": False,
        "probes": [],
    }
    p3, source3 = r0_blocks("question-79375162-1B054996-200D-4090-BAC2-A656EDCBC92D.html")
    template, rmd = p3
    signature_literal = re.search(r'SIGNATURE <- ("[^\n]*")', rmd).group(1)
    signature = json.loads(signature_literal)
    assert "`" not in signature and "'" not in signature
    work3 = CACHE / "p3"
    work3.mkdir(exist_ok=True)
    (work3 / "RMtemplate.html").write_text(template)
    for name, value, reader in [
        ("baseline", signature, "markdown"),
        ("frozen_raw_patch", "`" + signature + "`{=html}", "markdown"),
        ("post_answer_option", signature, "markdown-markdown_in_html_blocks"),
    ]:
        body = "---\ntitle: 'Report Title'\nsignature: '" + value + "'\n---\n"
        inp, out = work3 / (name + ".md"), work3 / (name + ".html")
        inp.write_text(body)
        command = [PANDOC, "--standalone", "--from=" + reader, "--to=html5", "--template=" + str(work3 / "RMtemplate.html"), str(inp), "--output=" + str(out)]
        rec = execute(command, work3, "P3-" + name)
        rec.update(case_id="P3", source=source3, input_sha256=sha(body.encode()), template_sha256=sha(template.encode()), input_derivation="Original R0 template and exact SIGNATURE literal; R evaluation and version-reporting body omitted. Synthetic post-knitr metadata probe, not an actual knitted .md.")
        if rec.get("exit_code") == 0:
            rec["metrics"] = table_metrics(out, signature)
        report["probes"].append(rec)
    p4, source4 = r0_blocks("question-79393445-5938869D-E61B-410C-97F5-035731293446.html")
    tex = p4[0]
    work4 = CACHE / "p4"
    work4.mkdir(exist_ok=True)
    texpath = work4 / "example.tex"
    texpath.write_text(tex)
    filterpath = ROOT / "evidence/pandoc/p4-raw-tikz.lua"
    filterbytes = filterpath.read_bytes()
    repo = ROOT.parents[3]
    relfilter = filterpath.relative_to(repo)
    sealed = subprocess.run(["git", "show", SEAL2 + ":" + str(relfilter)], cwd=repo, capture_output=True, check=True).stdout
    assert sealed == filterbytes, "Frozen synthesis changed; abort rather than silently alter experiment"
    nativepath = work4 / "native.json"
    rec = execute([PANDOC, "--from=latex+raw_tex", "--to=json", texpath, "--output=" + str(nativepath)], work4, "P4-native-boundary")
    rec.update(case_id="P4", source=source4, input_sha256=sha(tex.encode()))
    if rec.get("exit_code") == 0:
        native = json.loads(nativepath.read_text())
        raw = [b for b in native["blocks"] if b["t"] == "RawBlock"]
        rec["metrics"] = {"raw_blocks": len(raw), "tikz_raw_blocks": sum("\\begin{tikzpicture}" in b["c"][1] for b in raw), "raw_formats": sorted(set(b["c"][0] for b in raw)), "output_sha256": sha(nativepath.read_bytes())}
    report["probes"].append(rec)
    out4 = work4 / "example.html"
    rec = execute([PANDOC, "--standalone", "-N", "--from=latex+raw_tex", "--to=html5", "--lua-filter=" + str(filterpath), "--embed-resources", texpath, "--output=" + str(out4)], work4, "P4-frozen-synthesis")
    rec.update(case_id="P4", source=source4, input_sha256=sha(tex.encode()), filter_sha256=sha(filterbytes), filter_source_commit=SEAL2, filter_modified=False)
    if rec.get("exit_code") == 0:
        output = out4.read_text()
        rec["metrics"] = {"output_sha256": sha(output.encode()), "image_count": len(re.findall(r"<img\b", output)), "embedded_svg": "data:image/svg+xml" in output}
    report["probes"].append(rec)
    report["finished_utc"] = utc()
    (HERE / "execution.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
