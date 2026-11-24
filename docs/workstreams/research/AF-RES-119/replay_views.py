"""Run only visible packets through a cold comparator twice in separate locations."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def emit(rows):
    return "".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    cli = argparse.ArgumentParser(__doc__)
    cli.add_argument("out", type=Path)
    cli.add_argument("--publish", action="store_true")
    args = cli.parse_args()
    views = jsonl(ROOT / "views.jsonl")
    cases = {r["id"]: r for r in jsonl(ROOT / "cases.jsonl")}
    packets = [v["input"] for v in views]
    input_bytes = emit(packets)
    results = []
    receipts = []
    for repeat in (1, 2):
        folder = args.out / f"r{repeat}"
        folder.mkdir(parents=True, exist_ok=False)
        script = folder / "judge.py"
        shutil.copyfile(ROOT / "judge.py", script)
        (folder / "packets.jsonl").write_bytes(input_bytes)
        command = [sys.executable, "-I", "-B", "judge.py"]
        run = subprocess.run(command, cwd=folder, input=input_bytes, capture_output=True, check=True)
        assert len(run.stdout.splitlines()) == len(views)
        (folder / "observations.jsonl").write_bytes(run.stdout)
        results.append(run.stdout)
        receipts.append({"repeat": repeat, "argv": command, "cwd": str(folder), "exit_code": run.returncode,
                         "input_sha256": sha(input_bytes), "program_sha256": sha(script.read_bytes()),
                         "output_sha256": sha(run.stdout), "stderr": run.stderr.decode(), "packets": len(views)})
    if results[0] != results[1]:
        raise RuntimeError("isolated rule outputs differ")
    scored = []
    for view, answer in zip(views, map(json.loads, results[0].splitlines()), strict=True):
        key = view["id"]
        scored.append({
            "id": key, "sample_layer": cases[key]["sample_layer"], "view": view["view"], "budget": view["budget"],
            "packet_sha256": sha(emit([view["input"]])),
            "structure_characters": view["structure_characters"],
            "visible_paths": [r["path"] for r in view["records"]], **answer,
            "mechanical_inputs": "request + common candidates + complete visible records only",
            "main_effect": "excluded: rule author previously read full specs; no independent blinded judgment",
            "same_worker_exposure": "full case and definitions; pre-seal comment snippets for V8627 and M3981" if key in ("V8627", "M3981") else "full case and definitions",
        })
    if args.publish:
        (ROOT / "choices.jsonl").write_bytes(emit(scored))
        (ROOT / "evidence" / "view-replays.json").write_text(json.dumps(receipts, indent=2) + "\n")
    print(len(scored), "view packets, two exact matching stdout fingerprints", receipts[0]["output_sha256"])


if __name__ == "__main__":
    main()
