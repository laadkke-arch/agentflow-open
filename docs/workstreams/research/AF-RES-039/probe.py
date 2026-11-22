"""Meter explicitly supplied post-seal diagnostic or primary-source document URLs."""
import argparse
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

from replay import get

PHASES = ("diagnostic", "source_http", "gold_http")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=PHASES)
    parser.add_argument("capture_dir", type=Path)
    parser.add_argument("urls", type=Path, help="JSON list of [stable receipt ID, public URL]")
    args = parser.parse_args()
    capture = args.capture_dir.resolve()
    capture.mkdir(parents=True, exist_ok=True)
    if list(capture.iterdir()):
        parser.error("capture directory must be empty")
    urls = json.loads(args.urls.read_bytes())
    for source_id, url in urls:
        if not source_id.replace("-", "").isalnum():
            parser.error(f"invalid receipt ID {source_id}")
        old_cwd = Path.cwd()
        with tempfile.TemporaryDirectory(prefix="af039-public-source-") as work:
            try:
                os.chdir(work)
                Path("received").mkdir()
                request, _ = get(url, 1, args.phase)
                print(json.dumps({"phase": args.phase, "event": "request", "source_id": source_id,
                                  "request": request}, ensure_ascii=False), flush=True)
                shutil.move("received", capture / source_id)
            finally:
                os.chdir(old_cwd)


if __name__ == "__main__":
    sys.exit(main())
