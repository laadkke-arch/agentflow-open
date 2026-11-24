"""Record a published commit's paths and immutable object fingerprints."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNED = "docs/workstreams/research/AF-RES-106/"


def git(*args):
    return subprocess.check_output(["git", *args])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("stage")
    p.add_argument("sha")
    p.add_argument("utc")
    args = p.parse_args()
    assert len(args.sha) == 40 and all(c in "0123456789abcdef" for c in args.sha)
    parent = git("rev-parse", args.sha + "^").decode().strip()
    names = git("diff", "--name-only", "--no-renames", "-z", parent, args.sha).decode().split("\0")
    entries = []
    for path in filter(None, names):
        assert path.startswith(OWNED), path
        found = git("ls-tree", args.sha, "--", path).decode().strip()
        if not found:
            entries.append({"path": path, "deleted": True})
            continue
        mode, kind, sha = found.split("\t", 1)[0].split()
        raw = git("cat-file", "blob", sha)
        entries.append({"path": path, "mode": mode, "type": kind, "sha": sha,
                        "sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw)})
    record = {"stage": args.stage, "sha": args.sha, "parent": parent, "utc": args.utc,
              "tree": git("rev-parse", args.sha + "^{tree}").decode().strip(), "entries": entries}
    path = ROOT / "evidence" / ("checkpoint-" + args.stage + ".json")
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    path = ROOT / "evidence" / "checkpoints.json"
    data = json.loads(path.read_text()) if path.exists() else {"checkpoints": []}
    if not any(x["sha"] == args.sha for x in data["checkpoints"]):
        data["checkpoints"].append(record)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k != "entries"}, ensure_ascii=False))
    print("Changed owned paths:", len(entries))


if __name__ == "__main__":
    main()
