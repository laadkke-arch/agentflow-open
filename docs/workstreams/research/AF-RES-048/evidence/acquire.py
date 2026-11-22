"""Save separate public-response acquisitions or verify the pinned Matplotlib assets."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
PUBLISHER = {
    "new-pandoc": "https://pandoc.org/MANUAL.html",
    "new-vega-lite": "https://vega.github.io/vega-lite/docs/",
    "new-matplotlib-stable": "https://matplotlib.org/stable/users/index.html",
    "new-pypa": "https://packaging.python.org/en/latest/",
    "new-mta-static": "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip",
}


def pinned_assets():
    sources = (ROOT / "captures.jsonl", ROOT / "evidence/arrival-captures.jsonl")
    for source in sources:
        for line in source.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if row.get("fixed_asset"):
                yield row["acquisition_id"], row["fixed_asset"], row["response_sha256"]


def fetch(entry, output):
    name, url, expected = entry
    record = {"acquisition_id": name, "requested_url": url, "expected_sha256": expected}
    record["started_utc"] = datetime.now(timezone.utc).isoformat()
    try:
        request = Request(url, headers={"Accept-Encoding": "identity", "User-Agent": "AF-RES-048 public document verification"})
        try:
            response = urlopen(request, timeout=25)
        except HTTPError as error:
            response = error
        with response:
            data = response.read(30_000_001)
            if len(data) > 30_000_000:
                raise ValueError("response exceeds 30 MB")
            digest = hashlib.sha256(data).hexdigest()
            record.update(status=response.status, final_url=response.geturl(),
                          content_type=response.headers.get("Content-Type"),
                          content_encoding=response.headers.get("Content-Encoding"),
                          last_modified=response.headers.get("Last-Modified"),
                          response_sha256=digest, length=len(data),
                          expected_match=digest == expected if expected is not None else None)
            (output / f"{name}.raw").write_bytes(data)
    except (URLError, OSError, ValueError) as error:
        record.update(status=None, final_url=None, error=f"{type(error).__name__}: {error}")
    record["checked_utc"] = datetime.now(timezone.utc).isoformat()
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="A new output directory")
    parser.add_argument("--publisher", action="store_true", help="Attempt original live URLs in this environment")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    entries = ([(name, url, None) for name, url in PUBLISHER.items()]
               if args.publisher else list(pinned_assets()))
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(lambda entry: fetch(entry, args.output), entries))
    (args.output / "receipt.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    ok = sum(row["status"] == 200 and row.get("expected_match") is not False for row in rows)
    print(json.dumps({"total": len(rows), "matched_or_new_200": ok,
                      "mode": "new_publisher" if args.publisher else "pinned_asset_refetch"}))
    raise SystemExit(0 if ok == len(rows) else 2)


if __name__ == "__main__":
    main()
