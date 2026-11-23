"""Run the Graphviz and Jupyter controls in a fresh evidence directory."""
from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import re
import subprocess
from xml.etree import ElementTree

from run import browser_probe, execute, find_system, metadata, wrap_svg, write_json

GRAPHVIZ_SHA = "00d9fb4479c21b021e510dfb2633f1058d695db7"
JUPYTER_SHA = "2ba58585f649c1a2024aadd58007ec138457cc58"
SVG = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}"
DIRECTED = '''digraph {
    rankdir=LR;
    A -> B [label="go", URL="https://example.invalid/go"];
    B -> A [label="back", URL="https://example.invalid/back"];
}
'''


def get_git_file(repo, revision, path):
    return subprocess.check_output(["git", "-C", repo, "show", f"{revision}:{path}"])


def xml_metrics(path):
    root = ElementTree.parse(path).getroot()
    return {
        "file": metadata(path),
        "edges": [{
            "name": group.findtext(SVG + "title"),
            "labels": [value.text for value in group.iter(SVG + "text")],
            "arrow_polygons": sum(1 for _ in group.iter(SVG + "polygon")),
        } for group in root.iter(SVG + "g") if group.get("class") == "edge"],
        "links": [link.get(XLINK + "href") or link.get("href") for link in root.iter(SVG + "a")],
        "texts": [value.text for value in root.iter(SVG + "text")],
        "paths": sum(1 for _ in root.iter(SVG + "path")),
        "uses": sum(1 for _ in root.iter(SVG + "use")),
    }


def run_graphviz(tools, out):
    graph = out / "graphviz"
    graph.mkdir()
    repo = tools / "graphviz"
    (graph / "simple.dot").write_text("digraph { a->b }\n")
    (graph / "links.dot").write_text(DIRECTED)
    (graph / "noheads.dot").write_text(DIRECTED.replace("rankdir=LR;", "rankdir=LR; edge[dir=none];"))
    for dest, upstream in (("fsm.dot", "graphs/directed/fsm.gv"), ("url.dot", "tests/graphs/url.gv"),
                           ("upstream-expected.svg", "tests/linux.x86/url_dot.svg")):
        (graph / dest).write_bytes(get_git_file(repo, GRAPHVIZ_SHA, upstream))
    jobs = [(name, "svg", name) for name in ("simple", "links", "noheads", "fsm", "url")]
    jobs.append(("links", "svg:cairo", "links-cairo"))
    steps = [execute(["dot", "-V"], graph, os.environ, "version")]
    metrics = {}
    for input_name, kind, output_name in jobs:
        svg = graph / f"{output_name}.svg"
        steps.append(execute(["dot", f"-T{kind}", f"{input_name}.dot", "-o", svg.name],
                             graph, os.environ, output_name))
        if svg.is_file():
            metrics[output_name] = xml_metrics(svg)
    metrics["upstream-expected"] = xml_metrics(graph / "upstream-expected.svg")
    metrics["inputs"] = {p.name: metadata(p) for p in sorted(graph.glob("*.dot"))}
    fsm = re.findall(r'(LR_\d+) -> (LR_\d+) \[ label = "([^"]+)"', (graph / "fsm.dot").read_text())
    metrics["fsm_matched"] = sum(
        {"name": f"{a}->{b}", "labels": [label], "arrow_polygons": 1}
        in metrics["fsm"]["edges"] for a, b, label in fsm
    )
    metrics["fsm_expected"] = len(fsm)
    browser = find_system("chromium")
    image, inline = graph / "links-image.html", graph / "links-inline.html"
    image.write_text(wrap_svg("links.svg"))
    tag = (graph / "links.svg").read_text().split("<svg", 1)[1]
    inline.write_text("<!doctype html><html><meta charset=utf-8><title>Links</title><svg" + tag)
    views = {}
    for name in ("links.svg", image.name, inline.name, "links-cairo.svg", "noheads.svg", "url.svg"):
        key = name.replace(".", "-")
        views[key] = browser_probe(browser, graph / name, graph / f"{key}.png")
    return {"source_sha": GRAPHVIZ_SHA, "commands": steps, "metrics": metrics, "views": views}


def run_jupyter(tools, out):
    from PIL import Image, ImageDraw

    jupyter = out / "jupyter"
    jupyter.mkdir()
    python = tools / "jupyter/bin/python"
    img = Image.new("RGB", (90, 34), "#dce7f8")
    pen = ImageDraw.Draw(img)
    pen.text((9, 10), "DISPLAY", fill="#183762")
    img.save(jupyter / "display.png")
    img = Image.new("RGB", (86, 33), "#d4f5de")
    pen = ImageDraw.Draw(img)
    pen.text((9, 10), "MARKDOWN", fill="#19442b")
    img.save(jupyter / "local.png")
    base64_image = base64.b64encode((jupyter / "display.png").read_bytes()).decode()
    notebook = {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {"language_info": {"name": "python"}},
        "cells": [
            {"id": "local", "cell_type": "markdown", "metadata": {}, "source": "![local image](local.png)"},
            {"id": "result", "cell_type": "code", "metadata": {}, "source": "",
             "execution_count": 1,
             "outputs": [{"output_type": "display_data", "metadata": {},
                          "data": {"image/png": base64_image, "text/plain": "DISPLAY FALLBACK"}}]},
        ],
    }
    path = jupyter / "display.ipynb"
    write_json(path, notebook)
    cli = [python, "-B", "-m", "nbconvert", "--to=html"]
    env = dict(os.environ, JUPYTER_CONFIG_DIR=str(jupyter / "config"),
               JUPYTER_DATA_DIR=str(jupyter / "data"), JUPYTER_RUNTIME_DIR=str(jupyter / "runtime"))
    variants = {
        "default": [], "embedded": ["--embed-images"],
        "no-output": ["--embed-images", "--TemplateExporter.exclude_output=True"],
    }
    for variant in variants:
        (jupyter / variant).mkdir()
    steps = [
        execute([*cli, *options, f"--output-dir={variant}", "display.ipynb"],
                jupyter, env, variant) for variant, options in variants.items()
    ]
    views = {}
    html_bytes = {}
    for variant in variants:
        html = jupyter / variant / "display.html"
        if html.is_file():
            views[variant] = browser_probe(find_system("chromium"), html, html.parent / "browser.png")
            html_bytes[variant] = metadata(html)
    return {
        "source_sha": JUPYTER_SHA, "versions": execute([python, "-B", "-c",
         "import nbformat, nbconvert; print(nbformat.__version__, nbconvert.__version__)"],
         jupyter, env, "versions"),
        "commands": steps, "views": views, "html_files": html_bytes,
        "inputs": {p.name: metadata(p) for p in (path, jupyter / "display.png", jupyter / "local.png")},
    }


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--tools", type=Path, required=True)
    args.add_argument("--output", type=Path, required=True)
    parsed = args.parse_args()
    out = parsed.output.resolve()
    tools = parsed.tools.resolve()
    out.mkdir(parents=True, exist_ok=False)
    write_json(out / "cross-results.json",
               {"graphviz": run_graphviz(tools, out), "jupyter": run_jupyter(tools, out)})


if __name__ == "__main__":
    main()
