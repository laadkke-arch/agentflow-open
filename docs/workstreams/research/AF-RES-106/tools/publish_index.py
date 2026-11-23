"""Describe/read a frozen Git index for authenticated Git-data API publishing.

Read-only helper. It does not store credentials, create commits, or move refs.
The caller checks returned object/tree IDs against this index before updating a ref.
"""
import argparse
import base64
import hashlib
import json
import subprocess

OWNED = "docs/workstreams/research/AF-RES-106/"


def git(*args):
    return subprocess.check_output(["git", *args])


def entries():
    remote_known = {line.split(b" ", 1)[0].decode() for line in
                    git("rev-list", "--objects", "HEAD", "refs/remotes/origin/work/research-af-res-102").splitlines()}
    names = git("diff", "--cached", "--name-only", "--no-renames", "-z").decode().split("\0")
    rows = []
    for path in filter(None, names):
        if not path.startswith(OWNED):
            raise ValueError("Outside owned path: " + path)
        found = git("ls-files", "-s", "--", path).decode().strip()
        if not found:
            rows.append({"path": path, "mode": "100644", "type": "blob", "sha": None, "size": 0, "deleted": True})
            continue
        mode, sha, stage = found.split("\t", 1)[0].split()
        if stage != "0":
            raise ValueError("Unmerged index: " + path)
        raw = git("cat-file", "blob", sha)
        try:
            raw.decode("utf-8")
            text = b"\x00" not in raw
        except UnicodeDecodeError:
            text = False
        rows.append({"path": path, "mode": mode, "type": "blob", "sha": sha,
                     "sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw), "text": text,
                     "existing_remote": sha in remote_known,
                     "large_or_binary": not text or len(raw) > 20000})
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["metadata", "chunk", "text-batch"])
    p.add_argument("--sha")
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--length", type=int, default=24000)
    p.add_argument("--batch", type=int, default=0)
    args = p.parse_args()
    if args.action == "chunk":
        if not args.sha or len(args.sha) != 40 or any(x not in "0123456789abcdef" for x in args.sha):
            raise ValueError("Full blob SHA required")
        raw = git("cat-file", "blob", args.sha)
        print(json.dumps({"data": base64.b64encode(raw[args.offset:args.offset + args.length]).decode()}))
        return
    rows = entries()
    batches, current, size = [], [], 0
    for row in rows:
        if row.get("large_or_binary") or row.get("existing_remote"):
            continue
        if size + row["size"] > 20000 and current:
            batches.append(current)
            current, size = [], 0
        current.append(row)
        size += row["size"]
    if current:
        batches.append(current)
    if args.action == "metadata":
        print(json.dumps({"parent": git("rev-parse", "HEAD").decode().strip(),
                          "base_tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
                          "index_tree": git("write-tree").decode().strip(), "entries": rows,
                          "text_batch_count": len(batches)}, ensure_ascii=False))
    else:
        result = []
        for row in batches[args.batch]:
            entry = {k: row[k] for k in ["path", "mode", "type"]}
            if row.get("deleted"):
                entry["sha"] = None
            else:
                entry["content"] = git("cat-file", "blob", row["sha"]).decode("utf-8")
            result.append(entry)
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
