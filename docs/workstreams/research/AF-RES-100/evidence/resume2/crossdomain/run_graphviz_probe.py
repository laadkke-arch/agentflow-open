#!/usr/bin/env python3
"""Probe the external renderer only; this is not a Sphinx fixture execution."""
from __future__ import annotations

import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET


def main() -> None:
    output_dir = Path(__file__).resolve().parent
    cache_dir = output_dir.parents[1] / "_cache" / "resume2-crossdomain" / "runtime-graphviz"
    cache_dir.mkdir(parents=True, exist_ok=True)
    dot = shutil.which("dot")
    if dot is None:
        report = {"kind": "external_renderer_probe_only", "dot": None, "sphinx_fixture_run": False}
    else:
        version = subprocess.run([dot, "-V"], capture_output=True, text=True, check=False, timeout=10)
        # Explicit local graph based on the inspected upstream fixture class chain.
        # Sphinx's generated DOT, hyperlink mapping, filenames and markup are not reproduced.
        graph = 'digraph inheritance { "test.Foo" -> "test.DocHere"; "test.DocHere" -> "test.DocSubDir1"; "test.DocSubDir1" -> "test.DocSubDir2"; }\n'
        rendered = subprocess.run([dot, "-Tsvg"], input=graph.encode(), capture_output=True, check=False, timeout=10)
        svg_path = cache_dir / "fixture-chain.svg"
        svg_path.write_bytes(rendered.stdout)
        root = ET.fromstring(rendered.stdout) if rendered.returncode == 0 else None
        missing = cache_dir / "nonexistent-dot"
        if missing.exists():
            raise RuntimeError("Missing-executable control unexpectedly exists")
        try:
            subprocess.run([str(missing), "-V"], capture_output=True, check=False, timeout=10)
            missing_result = "unexpectedly executed"
        except FileNotFoundError as exc:
            missing_result = {"exception": type(exc).__name__, "errno": exc.errno}
        report = {
            "kind": "external_renderer_probe_only",
            "executed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "dot": dot,
            "version_command": [dot, "-V"],
            "version_returncode": version.returncode,
            "version_stdout": version.stdout,
            "version_stderr": version.stderr,
            "render_command": [dot, "-Tsvg"],
            "dot_input": graph,
            "render_returncode": rendered.returncode,
            "render_stderr": rendered.stderr.decode(),
            "svg_root_tag": root.tag if root is not None else None,
            "svg_sha256": hashlib.sha256(rendered.stdout).hexdigest(),
            "svg_bytes": len(rendered.stdout),
            "missing_executable_control": missing_result,
            "sphinx_fixture_run": False,
            "limitation": "Sphinx, docutils and pytest are unavailable; successful dot rendering does not establish Sphinx HTML, links, captions or upstream test success.",
        }
    (output_dir / "graphviz-runtime.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
