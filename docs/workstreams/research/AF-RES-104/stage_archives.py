"""Stage byte-identical archive transports and materialize ranking ledgers in a temporary root."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
from concurrent.futures import ThreadPoolExecutor

SED = "https://deb.debian.org/debian/pool/main/s/sed/sed_4.9.orig.tar.xz"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def copy_archive(root, plan, receipt):
    label = plan["label"]
    origin = plan["archive_url"]
    if label == "SED":
        url = SED
    else:
        repo, revision = origin.removeprefix("https://api.github.com/repos/").split("/tarball/")
        url = f"https://codeload.github.com/{repo}/legacy.tar.gz/{revision}"
    target = root / "evidence" / "_cache" / "corpora" / label / "source.tar"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        raw = subprocess.check_output(["curl", "-fsSL", "--max-time", "90", url])
        if len(raw) != receipt["download_bytes"] or sha(raw) != receipt["archive_sha256"]:
            raise ValueError(f"archive transport drift: {label}")
        with target.open("xb") as stream:
            stream.write(raw)
    raw = target.read_bytes()
    if len(raw) != receipt["download_bytes"] or sha(raw) != receipt["archive_sha256"]:
        raise ValueError(f"existing archive content differs: {label}")
    return {"label": label, "transport_url": url, "origin_url": origin,
            "bytes": len(raw), "sha256": sha(raw)}


def materialize(root):
    files = [root / "corpus-files.jsonl.gz", *sorted((root / "evidence" / "ranking").glob("*.jsonl.gz"))]
    for path in files:
        raw = gzip.decompress(path.read_bytes())
        target = path.with_suffix("")
        if target.exists() and target.read_bytes() != raw:
            raise ValueError(f"existing logical ledger differs: {target}")
        if not target.exists():
            target.write_bytes(raw)
    return {"logical_ledgers": len(files)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cache", type=Path)
    parser.add_argument("--original-ranking-inputs", action="store_true")
    args = parser.parse_args()
    root = args.cache.resolve()
    if args.original_ranking_inputs:
        result = materialize(root)
    else:
        plans = json.loads((root / "corpus-plan.json").read_bytes())["repositories"]
        receipts = json.loads((root / "evidence" / "corpus-build-receipts.json").read_bytes())
        by_label = {row["label"]: row for row in receipts}
        with ThreadPoolExecutor(max_workers=7) as workers:
            result = list(workers.map(lambda plan: copy_archive(root, plan, by_label[plan["label"]]), plans))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
