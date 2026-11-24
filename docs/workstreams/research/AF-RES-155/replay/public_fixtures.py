#!/usr/bin/env python3
"""Read fixed upstream tests and run the relevant small subset separately."""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from run import REPLAY, fingerprint, run_process

PINS = {
    "pandoc": "c3038dcd54152c4e18e49db31676b79ee7cc29b2",
    "prettier": "b86701dd1df5852f5024d322a17c9fb7ef97850c",
    "mustache-spec": "5d3b58ea35ae309c40d7a8111bfedc4c5bcd43a6",
    "python-markdown": "08dacae618775831243f6bbab47d9be590d511f2",
}


def emit(source, test, repository, receipt, matched, **extra):
    print(json.dumps({
        "source_id": source,
        "suite": repository,
        "upstream_commit": PINS[repository],
        "test": test,
        "matched": matched,
        "stage": receipt,
        **extra,
    }, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--tools", type=Path, required=True)
    args = parser.parse_args()
    upstream = args.upstream.resolve()
    tools = args.tools.resolve()
    node = shutil.which("node")
    assert node is not None
    for suite, expected in PINS.items():
        sha = subprocess.check_output(["git", "-C", upstream / suite, "rev-parse", "HEAD"], text=True).strip()
        assert sha == expected, (suite, sha)
    modules = tools / "node/node_modules"
    html = upstream / "pandoc/test/html-reader.html"
    golden = html.with_suffix(".native")
    expected = golden.read_bytes()
    receipt, actual = run_process("standalone-native",
                                  [tools / "pandoc-3.1.11/bin/pandoc", "-r", "html", "-w", "native", "-s", html],
                                  upstream, input_files={str(html): fingerprint(html.read_bytes())})
    # The full golden is published upstream. Keep the complete hash plus the observed literal slice.
    del receipt["stdout"]["utf8"]
    emit("F01", "HTML reader standalone native golden", "pandoc", receipt, actual == expected,
         expected=fingerprint(expected))

    path = upstream / "prettier/tests/format/markdown/fenced-code-block/jsfmt.spec.js"
    snapshot = path.parent / "__snapshots__/jsfmt.spec.js.snap"
    snippet_text = path.read_text(encoding="utf-8")
    input_text = json.loads(re.search(r'snippets: \[("(?:\\.|[^"])*")', snippet_text)[1])
    snap_text = snapshot.read_text(encoding="utf-8")
    expected = snap_text.split("=====================================output=====================================\n", 1)[1]
    expected = expected.split("\n\n================================================================================", 1)[0]
    expected = (expected.replace("\\`", "`") + "\n").encode()
    receipt, actual = run_process("format",
                                  [node, modules / "prettier/bin/prettier.cjs", "--no-config", "--no-editorconfig", "--parser", "markdown"],
                                  upstream, input_text.encode(), {str(path): fingerprint(path.read_bytes())})
    emit("F02", "first open-fence snapshot", "prettier", receipt, actual == expected,
         expected=fingerprint(expected), snapshot=fingerprint(snapshot.read_bytes()))

    spec = upstream / "mustache-spec/specs/interpolation.json"
    cases = {"HTML Escaping", "Triple Mustache", "Ampersand"}
    with tempfile.TemporaryDirectory(prefix="af155-public-") as scratch:
        for test in json.loads(spec.read_bytes())["tests"]:
            if test["name"] not in cases:
                continue
            binding = Path(scratch) / "binding.json"
            binding.write_text(json.dumps(test["data"]), encoding="utf-8")
            receipt, actual = run_process("render",
                                          [node, REPLAY / "pipeline.cjs", modules, "expand", binding],
                                          upstream, test["template"].encode(),
                                          {str(spec): fingerprint(spec.read_bytes()),
                                           "binding": fingerprint(binding.read_bytes())})
            expected = test["expected"].encode()
            emit("F03", test["name"], "mustache-spec", receipt, actual == expected,
                 expected=fingerprint(expected))

    test_module = "tests.test_syntax.extensions.test_fenced_code.TestFencedCode.testNestedFence"
    path = upstream / "python-markdown/tests/test_syntax/extensions/test_fenced_code.py"
    receipt, actual = run_process("unittest", [sys.executable, "-m", "unittest", test_module],
                                  upstream / "python-markdown",
                                  input_files={str(path): fingerprint(path.read_bytes())})
    emit("F05", test_module, "python-markdown", receipt, receipt["exit_code"] == 0)


if __name__ == "__main__":
    main()
