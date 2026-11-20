"""Collect metadata for explicit repository mappings absent from the content sample."""

import json

from collect import ROOT, Reader, repo_current, repo_signals, rows


def append_file(path, items):
    with path.open("a", buffering=1, encoding="utf-8") as output:
        for item in items:
            output.write(json.dumps(item, ensure_ascii=False) + "\n")


def main():
    repo_file = ROOT / "results" / "repo-now.jsonl"
    timed_file = ROOT / "results" / "repo-signals.jsonl"
    seen = {item["repo"] for item in rows(repo_file)}
    timed = {item["repo"] for item in rows(timed_file)}
    mapped = {line.split("|")[1]
              for line in (ROOT / "data/signal-repo-map.txt").read_text().splitlines()
              if line and not line.startswith("#")}
    reader = Reader(1.06)
    append_file(repo_file, repo_current(reader, {name: [] for name in sorted(mapped - seen)}, False))
    append_file(timed_file, repo_signals(reader, timed))


if __name__ == "__main__":
    main()
