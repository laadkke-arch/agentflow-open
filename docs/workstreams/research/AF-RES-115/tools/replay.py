"""Build minimal replay inputs and invoke two copies in different fresh directories."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from structure import digest, emit, jsonl

HERE = Path(__file__).resolve().parent.parent


def runner_envelope(view):
    return {
        "candidate_set": view["candidate_set"], "input_id": view["input_id"],
        "method": view["view"], "length_layer": view["length_layer"],
        "text": view["text"], "request_chars": view["request_chars"],
        "seed_complete": view["seed_complete"], "edition": view["edition"],
    }


def main():
    args = argparse.ArgumentParser()
    args.add_argument("new_directory", type=Path)
    args.add_argument("--views", type=Path, default=HERE / "views.jsonl")
    opts = args.parse_args()
    root = opts.new_directory.resolve()
    root.mkdir(exist_ok=False, parents=True)
    inputs = [runner_envelope(view) for view in jsonl(opts.views)]
    receipts, results = [], []
    for label in ("one", "two"):
        run = root / label
        run.mkdir()
        envelope = run / "visible.jsonl"
        emit(envelope, inputs)
        candidates = run / "candidates.json"
        shutil.copyfile(HERE / "candidate-conditions.json", candidates)
        program = run / "compare.py"
        shutil.copyfile(HERE / "tools" / "compare.py", program)
        output, audit = run / "runs.jsonl", run / "audit.json"
        command = [sys.executable, "-I", "-B", str(program), str(envelope),
                   str(candidates), str(output), str(audit)]
        subprocess.run(command, cwd=run, check=True)
        counts = json.loads(audit.read_text())
        receipts.append({"replay": label, "command": ["python", "-I", "-B", "compare.py",
                         "visible.jsonl", "candidates.json", "runs.jsonl", "audit.json"],
                         "cwd": label, **counts,
                         "program_sha256": digest(program.read_bytes()),
                         "input_sha256": digest(envelope.read_bytes()),
                         "candidate_sha256": digest(candidates.read_bytes()),
                         "run_sha256": digest(output.read_bytes())})
        results.append(jsonl(output))
    if results[0] != results[1]:
        raise RuntimeError("replays differ from fresh paths")
    emit(root / "runs.jsonl", (dict(row, replay="one") for row in results[0]))
    with (root / "runs.jsonl").open("a", encoding="utf-8") as out:
        for row in results[1]:
            out.write(json.dumps(dict(row, replay="two"), ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")) + "\n")
    (root / "replays.json").write_text(json.dumps({"runs": receipts, "all_equal": True}, indent=2)+"\n")
    print(f"{len(results[0])} comparisons per fresh path, SHA-256 {receipts[0]['run_sha256']}")


if __name__ == "__main__":
    main()
