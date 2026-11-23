"""Rebuild or verify the three appended P2 fixtures from the pinned inputs."""

import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
VARIANTS = {
    "original": None,
    "sealed-macros": b"",
    "answer-macros": b"[2]",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    options = parser.parse_args()
    original = (HERE / "P2-original.qmd").read_bytes()
    original_lines = original.splitlines(keepends=True)
    assert original_lines[7] == b"\n"
    appendix = (HERE / "appendix.md").read_bytes()
    for name, arity in VARIANTS.items():
        base = (HERE / f"P2-{name}.qmd").read_bytes()
        if arity is not None:
            definitions = b"".join(
                b"\\renewcommand{\\" + rule + b"}" + arity + b"{}\n"
                for rule in (b"toprule", b"bottomrule")
            )
            assert base == b"".join(original_lines[:7] + [definitions] + original_lines[8:]), name
        output = HERE / f"P2-{name}-dual.qmd"
        if options.check:
            assert output.read_bytes() == base + appendix, output.name
        else:
            output.write_bytes(base + appendix)


if __name__ == "__main__":
    main()
