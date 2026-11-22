"""Build the 48-run manifest or emit an unchanged single AF-RES-036 storage row."""
import argparse
import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path

DEPENDENCY = "5682b0d61a80edc159d4b510d213bbb4c69543be"
UPSTREAM = "docs/workstreams/research/AF-RES-036"
CONFIGS = {"C1": "C1_B_presealed", "C2": "C2_BH_with_provenance"}
REFS = [f"{family}{i:02}" for family in ("G", "R") for i in range(1, 7)]
TASKS = ["current", "restore"]
SEED = 39036
ROOT = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_file(name):
    return subprocess.check_output(["git", "show", f"{DEPENDENCY}:{UPSTREAM}/{name}"], cwd=ROOT)


def rows(data):
    for line in data.splitlines(keepends=True):
        yield json.loads(line), line


def storage():
    selected = {}
    for row, data in rows(git_file("retention-options.jsonl")):
        for short, configuration in CONFIGS.items():
            if row["configuration"] == configuration:
                key = (row["ref_id"], short)
                assert key not in selected
                selected[key] = (row, data)
    return selected


def manifest():
    selected = storage()
    components = {row["ref_id"]: sha(data) for row, data in rows(git_file("components.jsonl"))}
    scoring = {
        name: sha(git_file(name))
        for name in ("references.jsonl", "components.jsonl", "adjudication.csv")
    }
    pairs = [(ref, task) for ref in REFS for task in TASKS]
    random.Random(SEED).shuffle(pairs)
    assert set(selected) == {(ref, config) for ref in REFS for config in CONFIGS}
    for pair_index, (ref, task) in enumerate(pairs, 1):
        order = ("C1", "C2") if pair_index % 2 else ("C2", "C1")
        baseline = selected[(ref, "C1")][0]
        augmented = selected[(ref, "C2")][0]
        assert baseline["B"].encode() == augmented["B"].encode()
        for within_pair, config in enumerate(order, 1):
            row, data = selected[(ref, config)]
            assert sha(row["B"].encode()) == row["B_sha256"]
            history = row.get("H", "").encode()
            if config == "C2":
                assert sha(history) == row["H_sha256"]
            print(json.dumps({
                "order": (pair_index - 1) * 2 + within_pair,
                "pair_index": pair_index,
                "within_pair": within_pair,
                "seed": SEED,
                "algorithm_version": "1.0",
                "run_id": f"{ref}-{task}-{config}",
                "ref_id": ref,
                "task": task,
                "configuration": config,
                "storage_configuration": CONFIGS[config],
                "input_sha256": sha(data),
                "input_bytes": len(data),
                "B_sha256": row["B_sha256"],
                "B_bytes": len(row["B"].encode()),
                "H_sha256": row.get("H_sha256"),
                "H_bytes": len(history),
                "grader_only": {"file_sha256": scoring, "component_row_sha256": components[ref]},
                "worker_visibility": ["store.json", "replay.py", "task argument"],
            }, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", nargs=2, metavar=("REF", "CONFIG"))
    args = parser.parse_args()
    if args.packet:
        sys.stdout.buffer.write(storage()[tuple(args.packet)][1])
    else:
        manifest()


if __name__ == "__main__":
    main()
