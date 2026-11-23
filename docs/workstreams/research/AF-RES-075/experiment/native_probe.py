"""Run upstream's filename APIs in the two verified Pygments sdists."""
import argparse
import json
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

from registry import ROOT, sha, write_jsonl

PROGRAM = """
import json
import sys

sys.path.insert(0, sys.argv[1])
import pygments
from pygments.lexers import find_lexer_class_for_filename, guess_lexer_for_filename
from pygments.plugin import find_plugin_lexers
from pygments.util import ClassNotFound

def cls_name(cls):
    return cls.__name__ if cls is not None else None

plugins = list(find_plugin_lexers())
assert not plugins, plugins
rows = []
for query, name, text in json.load(sys.stdin):
    find = find_lexer_class_for_filename(query, text)
    outcome = None
    if text is not None:
        try:
            outcome = type(guess_lexer_for_filename(query, text)).__name__
        except ClassNotFound:
            pass
    rows.append(dict(edition=pygments.__version__, query=query, example=name,
                     content=text, find=cls_name(find), guess=outcome, plugins=len(plugins)))
print(json.dumps(rows, ensure_ascii=False))
"""
CASES = [
    (query, "filename only", None)
    for query in ("example.h", "example.lean", "example.m", "Android.bp")
] + [
    ("example.h", "C declaration", "#include <stdio.h>\nint main(void);\n"),
    ("example.h", "Objective-C", "#import <Foundation/Foundation.h>\n@interface Sample : NSObject\n@end\n"),
    ("example.m", "Objective-C", "#import <Foundation/Foundation.h>\n@interface Sample : NSObject\n@end\n"),
    ("example.m", "Matlab", "function y = square(x)\ny = x.^2;\nend\n"),
    ("example.m", "Octave", "## Octave line\nfunction y = square(x)\ny = x.^2;\nendfunction\n"),
    ("example.lean", "uppercase import", "import Mathlib\n#check Nat\n"),
    ("example.lean", "lowercase import", "import data.nat.basic\n#check nat\n"),
]


def probe(archive_dir, output):
    editions = json.loads((ROOT / "inputs/manifest.json").read_bytes())["editions"]
    results = []
    for item in editions:
        if item["domain"] != "PG":
            continue
        tag = item["tag"]
        archive = archive_dir / f"PG-{tag}.tar.gz"
        if sha(archive.read_bytes()) != item["archive_used_sha256"]:
            raise ValueError(f"Invalid Pygments sdist digest for {tag}")
        with tempfile.TemporaryDirectory(prefix="af075-native-") as directory:
            with tarfile.open(archive) as bundle:
                bundle.extractall(directory, filter="data")
            source = Path(directory) / f"pygments-{tag}"
            if sha((source / item["file"]).read_bytes()) != item["sha256"]:
                raise ValueError("Native archive and scored registry differ")
            command = [sys.executable, "-I", "-S", "-B", "-c", PROGRAM, str(source)]
            result = subprocess.run(command, input=json.dumps(CASES), check=True, capture_output=True,
                                    encoding="utf8", cwd=directory, env={})
            edition = json.loads(result.stdout)
            assert {row["edition"] for row in edition} == {tag}
            results.extend(edition)
    write_jsonl(output, results)
    print(f"{len(results)} native API observations")


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--archive-dir", type=Path, required=True)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    probe(args.archive_dir, args.output)
