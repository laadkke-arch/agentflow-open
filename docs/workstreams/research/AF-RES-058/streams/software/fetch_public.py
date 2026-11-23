"""Fetch a public original for manual reading; do not execute downloaded code.

Downloaded files stay in ignored _cache. Receipts are not proof of reading.
Usage: python -B fetch_public.py LABEL URL [EXT]
"""
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent

def fetch(label, url, extension="pdf"):
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", label):
        raise ValueError("simple label required")
    if extension not in ("pdf", "html", "json", "zip", "txt", "tar.gz"):
        raise ValueError("unsupported cache format")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt = {"label": label, "url": url, "started_utc": now,
               "actor": "software_ir assistant cloud workspace",
               "read_status": "retrieved_not_yet_read"}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            receipt.update(status=response.status, final_url=response.url,
                           content_type=response.headers.get("Content-Type"))
        output = ROOT / "_cache" / (label + "." + extension)
        output.parent.mkdir(exist_ok=True)
        output.write_bytes(data)
        receipt.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                       cache_path=output.relative_to(ROOT).as_posix())
        if extension == "pdf" and data.startswith(b"%PDF"):
            converted = subprocess.run(["pdftotext", "-layout", str(output),
                                        str(output.with_suffix(".txt"))],
                                       capture_output=True, text=True)
            receipt["pdftotext_exit_code"] = converted.returncode
        elif extension == "pdf":
            receipt["read_status"] = "non_pdf_response"
    except Exception as exc:
        receipt.update(status="failed", error=str(exc), read_status="access_failed")
    receipt["finished_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (ROOT / "fetch-receipts.jsonl").open("a") as handle:
        handle.write(json.dumps(receipt, ensure_ascii=False) + "\n")
    print(json.dumps(receipt, ensure_ascii=False))
    return receipt

if __name__ == "__main__":
    fetch(*sys.argv[1:])
