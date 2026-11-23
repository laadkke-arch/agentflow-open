"""Fetch only missing pinned public inputs, or verify the existing local cache.

No archive content is executed, extracted, or published. A changed hash stops
the run; it is not silently treated as the originally read version.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parent
INPUTS = [
    ("streams/software/cache/newton-responses.zip",
     "https://zenodo.org/api/records/10459420/files/3.%20Responses.zip/content",
     "b65f818fd2f94dde7574ca53ed9789bdabcce5f637514736b3ee79379ddbd931"),
    ("streams/software/cache/newton-experiments.zip",
     "https://zenodo.org/api/records/10459420/files/2.%20Experiments.zip/content",
     "2e6e67db3e37d599e15148a38c898a501a709fa793481324d675c891d2df9b57"),
    ("streams/software/cache/newton-analyses.zip",
     "https://zenodo.org/api/records/10459420/files/4.%20Analyses.zip/content",
     "59d9e8c6673c326a29908a37e0a0ac84dadbb3e957592c0fd56f9f458b6c31a3"),
    ("streams/software/cache/designpattern-package.zip",
     "https://zenodo.org/api/records/10849702/files/SoftwareForHumans/DesignPatternDoc-UserStudy-v1.0.zip/content",
     "6e724fe2185e9cd4a917afe3ef1810cb3a6bfcad2503c1e13ddfc3b2642fca71"),
    ("streams/root/cache/casdoc-artifact.zip",
     "https://zenodo.org/api/records/14868205/files/artifact.zip/content",
     "02579d60c09f7fed325fa18bccd17a7b52f5510b52b29f52af341fb38cb45260"),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true", help="download missing files only")
    args = parser.parse_args()
    records = []
    for relative, url, expected in INPUTS:
        path = ROOT / relative
        downloaded = False
        if not path.exists():
            if not args.download:
                raise FileNotFoundError(f"{relative}: rerun with --download")
            path.parent.mkdir(parents=True, exist_ok=True)
            request = urllib.request.Request(url, headers={"User-Agent": "AF-RES-054 public-record reproduction"})
            with urllib.request.urlopen(request, timeout=45) as response:
                data = response.read()
            digest = hashlib.sha256(data).hexdigest()
            if digest != expected:
                raise ValueError(f"Version changed at {url}: {digest}; expected {expected}")
            path.write_bytes(data)
            downloaded = True
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected:
            raise ValueError(f"Cached version mismatch: {relative}; preserve it and recover the pinned version")
        records.append({"file": relative, "url": url, "sha256": digest,
                        "bytes": path.stat().st_size, "downloaded_in_this_run": downloaded})
    receipt = {"utc": datetime.now(timezone.utc).isoformat(), "status": "passed",
               "inputs": records, "participant_rows_exported": False,
               "external_study_code_executed": False}
    (ROOT / "evidence/input-fetch-check.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": "passed", "pinned_files_verified": len(records),
                      "downloaded": sum(r["downloaded_in_this_run"] for r in records)}))


if __name__ == "__main__":
    main()
