#!/usr/bin/env python3
"""Read only: export the exact Git index for connected GitHub Git-data writes.

No tokens or network calls. The caller must create blobs/tree/commit via the
connected GitHub tool, compare tree hashes, and update only the leased task ref.
"""
import argparse
import base64
import hashlib
import json
import subprocess

ALLOWED = "docs/workstreams/research/AF-RES-102/"


def git(*args):
    return subprocess.check_output(["git", *args])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--path")
    p.add_argument("--text-start", type=int)
    p.add_argument("--text-budget", type=int, default=80000)
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--length", type=int, default=90000)
    a = p.parse_args()
    changed = [x for x in git("diff", "--cached", "--name-only", "-z").decode().split("\0") if x]
    if any(not x.startswith(ALLOWED) for x in changed):
        raise SystemExit("Refusing staged path outside task ownership")
    if a.text_start is not None:
        batch, used, index = [], 0, a.text_start
        while index < len(changed):
            path = changed[index]
            b = git("show", ":" + path)
            try:
                decoded = b.decode("utf-8")
            except UnicodeDecodeError:
                decoded = None
            if len(b) > a.text_budget or decoded is None:
                if not batch:
                    print(json.dumps({"large_path": path, "bytes": len(b), "next_index": index + 1}))
                    return
                break
            if used + len(b) > a.text_budget and batch:
                break
            batch.append({"path": path, "mode": "100644", "type": "blob", "content": decoded})
            used += len(b)
            index += 1
        print(json.dumps({"tree_elements": batch, "next_index": index}, ensure_ascii=False))
        return
    if a.path:
        if a.path not in changed:
            raise SystemExit("Requested path is not an exact staged change")
        b = git("show", ":" + a.path)
        print(json.dumps({"path": a.path, "offset": a.offset, "total_bytes": len(b),
                          "data_base64": base64.b64encode(b[a.offset:a.offset+a.length]).decode()}))
        return
    files = []
    for path in changed:
        blob = git("rev-parse", ":" + path).decode().strip()
        b = git("show", ":" + path)
        files.append({"path": path, "bytes": len(b), "git_blob": blob,
                      "sha256": hashlib.sha256(b).hexdigest(), "mode": "100644"})
    print(json.dumps({"parent": git("rev-parse", "HEAD").decode().strip(),
                      "base_tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
                      "expected_tree": git("write-tree").decode().strip(), "files": files}))


if __name__ == "__main__":
    main()
