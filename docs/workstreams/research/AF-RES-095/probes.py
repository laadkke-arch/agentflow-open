"""Run separate scope, token-shape, and error probes under the same binaries."""

import argparse
import json
import shutil
from pathlib import Path

import pymupdf

from experiment import HERE, PLAN, copy_outputs, digest, execute, render_env, run_quarto, save_json
from measure import horizontal_paths, serialize

PROBES = HERE / "fixtures/probes"
QUARTO_PROBES = {
    "P-LOCAL-T": "local-T.qmd", "P-LOCAL-Z": "local-Z.qmd",
    "P-HEADER-T": "header-T.qmd", "P-INCLUDE-T": "include-T.qmd", "P-TRACE-T": "trace-T.qmd",
}
DEFINITIONS = {
    "O": "% use package definitions\n",
    "Z": "\\renewcommand{\\toprule}{}\n\\renewcommand{\\bottomrule}{}\n",
    "T": "\\renewcommand{\\toprule}[2]{}\n\\renewcommand{\\bottomrule}[2]{}\n",
}


def tabular_probe(name, variant, work_root, evidence_root):
    run_id = f"P-{name.upper()}-{variant}"
    work = work_root / run_id
    dest = evidence_root / run_id
    work.mkdir()
    dest.mkdir()
    source = PROBES / (name + ".tex")
    shutil.copyfile(source, work / "document.tex")
    definitions = work / "definitions.tex"
    definitions.write_text(DEFINITIONS[variant])
    shutil.copyfile(definitions, dest / definitions.name)
    env = render_env(work, work_root / "shared")
    args = ["/usr/bin/xelatex", "-interaction=batchmode", "-halt-on-error", "-recorder", "document.tex"]
    status = execute(args, work, dest, env)
    files = copy_outputs(work, dest, "document")
    log = (dest / "document.tex-log.txt").read_text().splitlines()
    receipt = {"run_id": run_id, "source": source.name, "input_sha256": digest(source),
               "definition_sha256": digest(definitions), "execution": status, "files": files,
               "errors": [line for line in log if line.startswith("!")]}
    if ".pdf" in files:
        with pymupdf.open(dest / "document.pdf") as document:
            page = document[0]
            words = page.get_text("words")
            marks = {word[4]: word[1] for word in words if word[4] in {"Before", "After"}}
            data = {"text": page.get_text(), "words": serialize(words),
                    "horizontal_paths": horizontal_paths(page.get_drawings())}
            if len(marks) == 2:
                data["before_after_y_delta_pt"] = marks["After"] - marks["Before"]
            save_json(dest / "pdf-raw.json", data)
            receipt.update(data)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quarto", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    options = parser.parse_args()
    quarto, work, evidence = (p.resolve() for p in (options.quarto, options.work, options.evidence))
    work.mkdir(parents=True)
    evidence.mkdir(parents=True)
    rows = [run_quarto(run_id, PROBES / file, PLAN["expected_tables"], quarto, work, evidence)
            for run_id, file in QUARTO_PROBES.items()]
    rows.extend(tabular_probe(name, variant, work, evidence)
                for name in ("tabular", "bare-bottom") for variant in DEFINITIONS)
    (evidence / "probes.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    for row in rows:
        print(row["run_id"], row["execution"]["exit_code"])


if __name__ == "__main__":
    main()
