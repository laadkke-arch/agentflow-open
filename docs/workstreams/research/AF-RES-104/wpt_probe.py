"""Run the pinned WPT axis-scope test with local Chromium and its upstream harness."""
import argparse
from datetime import datetime, timezone
from functools import partial
from hashlib import sha256
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import subprocess
from threading import Thread

from crossdomain import WPT, WPT_ROOT

FIXTURE = "grid-item-minimum-size-single-axis-scroll-container.html"
FIXTURE_PATH = f"css/css-grid/grid-items/{FIXTURE}"
HARNESS = ("testharness.js", "testharnessreport.js", "check-layout-th.js")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def fetch(root):
    urls = {FIXTURE_PATH: WPT_ROOT + FIXTURE}
    urls.update({f"resources/{name}": f"https://raw.githubusercontent.com/web-platform-tests/wpt/{WPT}/resources/{name}"
                 for name in HARNESS})
    files = []
    for path, url in urls.items():
        dst = root / path
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            subprocess.run(["curl", "-fsSL", "--max-time", "25", url, "-o", str(dst)], check=True)
        data = dst.read_bytes()
        files.append({"url": url, "path": path, "bytes": len(data), "sha256": sha256(data).hexdigest()})
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cache", type=Path)
    args = parser.parse_args()
    base = args.cache.resolve()
    target = base / "wpt"
    files = fetch(target)
    started = datetime.now(timezone.utc).isoformat()
    chromium = subprocess.check_output(["chromium", "--version"], text=True).strip()
    site = partial(QuietHandler, directory=str(target))
    with ThreadingHTTPServer(("127.0.0.1", 0), site) as server:
        Thread(target=server.serve_forever, daemon=True).start()
        url = f"http://127.0.0.1:{server.server_port}/{FIXTURE_PATH}"
        command = ["chromium", "--headless", f"--user-data-dir={base}/wpt-chrome",
                   "--disable-gpu", "--virtual-time-budget=4000", "--dump-dom"]
        command.append(url)
        try:
            run = subprocess.run(command, capture_output=True, text=True, timeout=25)
            (base / "wpt-dom.html").write_text(run.stdout)
            statuses = re.findall(r'<tr[^>]*class="(pass|fail|timeout|notrun)"[^>]*>', run.stdout)
            result = {"exit_code": run.returncode, "harness_result_rows": statuses,
                      "document_sha256": sha256(run.stdout.encode()).hexdigest(),
                      "stderr_last": run.stderr.splitlines()[-5:]}
        except subprocess.TimeoutExpired:
            result = {"exit_code": 124, "harness_result_rows": [], "error": "chromium timeout"}
        finally:
            server.shutdown()
    result.update(command=command, chromium=chromium, started_utc=started, files=files,
                  finished_utc=datetime.now(timezone.utc).isoformat())
    print(json.dumps(result, indent=2))
    return 0 if result["exit_code"] == 0 and result["harness_result_rows"] == ["pass"] * 4 else 1


if __name__ == "__main__":
    raise SystemExit(main())
