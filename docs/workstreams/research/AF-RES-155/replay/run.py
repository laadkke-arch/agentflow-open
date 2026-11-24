#!/usr/bin/env python3
"""Replay the sealed input paths and write byte-level receipts as JSONL to stdout."""

import argparse
import base64
import hashlib
import json
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

REPLAY = Path(__file__).resolve().parent
WORK = REPLAY.parent

PANDOC_PATHS = (
    ("E2-default", "E2-author", "table.md", (), "author command"),
    ("E2-drop-pre", "E2-no-pre", "table.md", (), "author-described modification"),
    ("E2-with-span", "E2-span", "table.md", (), "configured wrapper"),
    ("E2-default-lf", "E2-lf", "table.md", (), "configured EOL"),
    ("E2-html-reader", "E2-author", "table.md", ("-f", "html"), "configured reader"),
    ("E3-default", "E3-author", "code.md", (), "author command"),
    ("E3-commonmark", "E3-author", "code.md", ("-f", "commonmark"), "maintainer-suggested reader"),
    ("E3-braced", "E3-braces", "code.md", (), "maintainer-suggested syntax"),
    ("E3-lang-only", "E3-language-only", "code.md", (), "configured metadata deletion"),
)
TEMPLATE_PATHS = (
    ("X05-static-example", "X05-static", None, "author snippet, engines configured"),
    ("X05-nested-example", "X05-template", "X05-bind-nested", "author snippet, binding inferred and engines configured"),
    ("X05-static-boundary", "X05-static-tail", None, "configured next paragraph"),
    ("X05-plain-boundary", "X05-template-tail", "X05-bind-plain", "configured plain binding"),
    ("X05-nested-boundary", "X05-template-tail", "X05-bind-nested", "configured nested binding"),
    ("X05-format-expanded", "X05-template-tail", "X05-bind-nested", "configured nested binding, format after expansion"),
)


def fingerprint(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def retain_bytes(data):
    result = fingerprint(data)
    try:
        result["utf8"] = data.decode("utf-8")
    except UnicodeDecodeError:
        result["base64"] = base64.b64encode(data).decode("ascii")
    return result


def run_process(label, argv, cwd, input_bytes=None, input_files=None):
    argv = [str(arg) for arg in argv]
    start = time.monotonic_ns()
    timestamp = datetime.now(timezone.utc).isoformat()
    error = None
    exit_code = None
    try:
        result = subprocess.run(argv, cwd=cwd, input=input_bytes, capture_output=True, timeout=30)
        exit_code, stdout, stderr = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as exc:
        error = "timeout at 30 seconds"
        stdout, stderr = exc.stdout or b"", exc.stderr or b""
    except OSError as exc:
        error = f"{type(exc).__name__}: {exc}"
        stdout, stderr = b"", b""
    duration_ns = time.monotonic_ns() - start
    receipt = {
        "stage": label,
        "argv": argv,
        "cwd": str(cwd),
        "started_at_utc": timestamp,
        "duration_ns": duration_ns,
        "input_files": input_files or {},
        "stdin": fingerprint(input_bytes) if input_bytes is not None else None,
        "exit_code": exit_code,
        "error": error,
        "stdout": retain_bytes(stdout),
        "stderr": retain_bytes(stderr),
    }
    return receipt, stdout if exit_code == 0 else None


def read_inputs():
    return {
        item["input_id"]: item
        for item in map(json.loads, (WORK / "inputs.jsonl").read_text(encoding="utf-8").splitlines())
    }


def open_fixture(inputs, input_id):
    record = inputs[input_id]
    path = WORK / record["file"]
    data = path.read_bytes()
    assert fingerprint(data) == {"bytes": record["utf8_bytes"], "sha256": record["sha256"]}, path
    return path, data


def nodes(value):
    if isinstance(value, dict):
        if "t" in value:
            yield value
        yield from nodes(value.get("c"))
    elif isinstance(value, list):
        for item in value:
            yield from nodes(item)


def summarize_pandoc(raw_ast, plain):
    if raw_ast is None or plain is None:
        return None
    document = json.loads(raw_ast)
    blocks = document["blocks"]
    all_nodes = list(nodes(blocks))
    table_cells = []
    for block in blocks:
        if block["t"] == "Table":
            for body in block["c"][4]:
                for _, row in body[3]:
                    table_cells.append([
                        [{"type": n["t"], "value": n.get("c")} for n in nodes(cell[-1])
                         if n["t"] in {"Str", "Space", "CodeBlock"}]
                        for cell in row
                    ])
    return {
        "top_level": [block["t"] for block in blocks],
        "raw_blocks": [n["c"] for n in all_nodes if n["t"] == "RawBlock"],
        "native_table_body_cells": table_cells,
        "code_blocks": [n["c"] for n in all_nodes if n["t"] == "CodeBlock"],
        "prose_words": [n["c"] for n in all_nodes if n["t"] == "Str"],
        "plain_lines": plain.decode("utf-8").splitlines(),
    }


def pandoc_path(pandoc, inputs, spec, workdir):
    path_id, input_id, filename, flags, layer = spec
    _, data = open_fixture(inputs, input_id)
    (workdir / filename).write_bytes(data)
    file_digests = {filename: fingerprint(data)}
    plain, plain_bytes = run_process("plain", [pandoc, *flags, "-t", "plain", filename], workdir,
                                     input_files=file_digests)
    ast, ast_bytes = run_process("ast", [pandoc, *flags, "-t", "json", filename], workdir,
                                 input_files=file_digests)
    summary = summarize_pandoc(ast_bytes, plain_bytes)
    return {"path_id": path_id, "input_id": input_id, "layer": layer,
            "stages": [plain, ast], "summary": summary}


def template_path(node, modules, inputs, spec, workdir):
    path_id, input_id, binding_id, layer = spec
    _, data = open_fixture(inputs, input_id)
    if binding_id is not None:
        binding_path, binding = open_fixture(inputs, binding_id)
        binding_args = [binding_path]
        binding_files = {str(binding_path): fingerprint(binding)}
    else:
        binding_args = []
        binding_files = {}
    prettify = [node, modules / "prettier/bin/prettier.cjs", "--no-config", "--no-editorconfig", "--parser", "markdown"]
    helper = [node, REPLAY / "pipeline.cjs", modules]
    stages = []

    def invoke(label, cmd, upstream, files=None):
        if upstream is None:
            stages.append({"stage": label, "exit_code": None, "status": "upstream failed"})
            return None
        record, stdout = run_process(label, cmd, workdir, upstream, files)
        stages.append(record)
        return stdout

    expanded = invoke("expand-original", [*helper, "expand", *binding_args], data, binding_files)
    original_parsed = invoke("parse-original-expanded", [*helper, "parse"], expanded)
    if path_id == "X05-format-expanded":
        formatted_expanded = invoke("format-after-expansion", prettify, expanded)
    else:
        formatted = invoke("format-template", prettify, data)
        formatted_expanded = invoke("expand-formatted", [*helper, "expand", *binding_args], formatted, binding_files)
    formatted_parsed = invoke("parse-formatted-expanded", [*helper, "parse"], formatted_expanded)
    return {"path_id": path_id, "input_id": input_id, "binding_id": binding_id,
            "input": fingerprint(data), "binding": binding_files, "layer": layer, "stages": stages,
            "summary": {
                "original": json.loads(original_parsed) if original_parsed is not None else None,
                "formatted": json.loads(formatted_parsed) if formatted_parsed is not None else None,
            }}


def git(args):
    return subprocess.check_output(["git", "-C", str(WORK), *args], text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tools", type=Path, required=True)
    parser.add_argument("--repeat", required=True, help="Label for this fresh checkout")
    args = parser.parse_args()
    tools = args.tools.resolve()
    pandoc = tools / "pandoc-3.1.11/bin/pandoc"
    modules = tools / "node/node_modules"
    node = shutil.which("node")
    if not node:
        raise SystemExit("Node is required.")
    versions = {
        "pandoc": subprocess.check_output([pandoc, "--version"], text=True).splitlines()[0],
        "node": subprocess.check_output([node, "--version"], text=True).strip(),
    }
    assert versions["pandoc"] == "pandoc 3.1.11", versions
    for name, expected in {"prettier": "3.1.1", "mustache": "4.2.0", "commonmark": "0.30.0"}.items():
        versions[name] = json.loads((modules / name / "package.json").read_text(encoding="utf-8"))["version"]
        assert versions[name] == expected, versions
    inputs = read_inputs()
    for input_id in inputs:
        open_fixture(inputs, input_id)
    base = {"repeat": args.repeat, "checkout": git(["rev-parse", "HEAD"]),
            "checkout_root": git(["rev-parse", "--show-toplevel"]),
            "checkout_clean_at_start": not git(["status", "--porcelain"]),
            "versions": versions, "pandoc_executable": fingerprint(pandoc.read_bytes()),
            "lockfile": fingerprint((REPLAY / "package-lock.json").read_bytes()),
            "driver_argv": [str(REPLAY / "run.py"), "--tools", str(tools), "--repeat", args.repeat]}
    with tempfile.TemporaryDirectory(prefix="af155-replay-") as scratch:
        for path in PANDOC_PATHS + TEMPLATE_PATHS:
            cwd = Path(scratch) / path[0]
            cwd.mkdir()
            result = (pandoc_path(pandoc, inputs, path, cwd) if path in PANDOC_PATHS
                      else template_path(node, modules, inputs, path, cwd))
            print(json.dumps(base | {"status": "attempted"} | result, ensure_ascii=False), flush=True)
    print(json.dumps(base | {
        "status": "blocked_before_execution", "path_id": "E4-same-function", "input_id": "E4-input",
        "stages": [], "summary": None, "layer": "author path",
        "reason": "Input addCartItem differs from the output/expected updateCartItem; no verified effective config or paired source.",
    }, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
