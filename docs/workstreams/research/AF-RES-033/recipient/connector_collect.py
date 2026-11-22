#!/usr/bin/env python3
"""Transport bridge for approved connector requests, with a projected local cache.
This imports the sealed collection rules without changing their selection logic.
Only the caller's in-process projections enter the cache. No PR states, bodies,
comments, patches, or messages may enter a metadata cache record.
"""
import argparse
import hashlib
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CACHE = ROOT / "originals" / "_transport_cache"

class NeedRequest(Exception):
    def __init__(self, url, cache_path):
        self.url, self.cache_path = url, cache_path


def cached_request(url):
    path = CACHE / (hashlib.sha256(url.encode()).hexdigest() + ".json")
    if not path.exists():
        raise NeedRequest(url, str(path))
    row = json.loads(path.read_text())
    if row["request_url"] != url:
        raise ValueError("Connector cache URL identity mismatch")
    return row["projected_data"], row.get("pagination_link", "")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["inspect", "audit", "restore"])
    parser.add_argument("repository", choices=["rust-lang/rfcs", "kubernetes/enhancements"])
    parser.add_argument("number", type=int)
    parser.add_argument("--sha")
    parser.add_argument("--path")
    parser.add_argument("--blob-sha")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("recipient_sealed_collector", ROOT / "collect_initials.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.request_json = cached_request
    try:
        if args.mode == "inspect":
            result = module.inspect_initial(args.repository, args.number)
        elif args.mode == "audit":
            result = module.audit_force_push(args.repository, args.number)
        else:
            if not all([args.sha, args.path, args.blob_sha]):
                parser.error("restore requires sha, path and blob-sha")
            result = module.restore(args.repository, args.number, args.sha, args.path, args.blob_sha)
        print(json.dumps({"status": "complete", "result": result}, ensure_ascii=False))
    except NeedRequest as request:
        print(json.dumps({"status": "request_needed", "request_url": request.url,
                          "cache_path": request.cache_path}))

if __name__ == "__main__":
    main()
