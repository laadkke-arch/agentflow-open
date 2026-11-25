"""Capture one HTTP response, including failures and hashes of received bytes."""
import argparse
import gzip
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit, urlunsplit


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def public_url(url):
    if url and urlsplit(url).hostname == "release-assets.githubusercontent.com":
        parts = urlsplit(url)
        return urlunsplit(parts._replace(query="", fragment=""))
    return url


def public_headers(raw):
    def sanitize(line):
        name, _, value = line.group().partition(b":")
        if name.lower() == b"location":
            redacted = public_url(value.strip().decode("ascii"))
            return name + b": " + redacted.encode("ascii")
        return name + b": [redacted]"

    return re.sub(rb"^(?:set-cookie|authorization|proxy-authorization|location):[^\r\n]*",
                  sanitize, raw, flags=re.IGNORECASE | re.MULTILINE)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path, help="Path prefix for headers and transport JSON")
    parser.add_argument("url")
    parser.add_argument("--accept", default="*/*")
    parser.add_argument("--body", type=Path, required=True)
    parser.add_argument("--gzip", action="store_true", help="Losslessly compress the stored HTTP body")
    parser.add_argument("--discard-body", action="store_true", help="Keep only the response digest/size")
    args = parser.parse_args()
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    header_path = args.receipt.with_suffix(".headers.txt")
    stderr_path = args.receipt.with_suffix(".stderr.txt")
    with TemporaryDirectory(prefix="af-res-266-http-") as dirname:
        temporary_body = Path(dirname, "body")
        command = [
            "curl", "--silent", "--show-error", "--location", "--max-redirs", "5",
            "--proto", "=https", "--proto-redir", "=https", "--connect-timeout", "12",
            "--max-time", "85", "--header", "Accept: " + args.accept, "--header",
            "Accept-Encoding: identity", "--user-agent", "AF-RES-266-public-audit/1.0",
            "--dump-header", str(header_path), "--output", str(temporary_body),
            "--write-out", "%{json}", args.url,
        ]
        started = utc()
        process = subprocess.run(command, capture_output=True, check=False)
        finished = utc()
        body = temporary_body.read_bytes() if temporary_body.is_file() else None
        body_received = body is not None
        if body_received and not args.discard_body:
            args.body.parent.mkdir(parents=True, exist_ok=True)
            args.body.write_bytes(gzip.compress(body, mtime=0) if args.gzip else body)
        if process.stderr:
            stderr_path.write_bytes(process.stderr)

    curl = json.loads(process.stdout) if process.stdout else {}
    curl["url_effective"] = public_url(curl.get("url_effective"))
    raw_headers = header_path.read_bytes() if header_path.exists() else b""
    headers = public_headers(raw_headers)
    if headers != raw_headers:
        header_path.write_bytes(headers)
    fields = ["response_code", "http_version", "url_effective", "content_type",
              "num_redirects", "size_download", "time_total", "ssl_verify_result", "errormsg"]
    receipt = {
        "requested_url": args.url, "accept": args.accept, "started_utc": started,
        "finished_utc": finished, "command": command, "exit_code": process.returncode,
        "curl": {name: curl.get(name) for name in fields},
        "headers_sha256": hashlib.sha256(headers).hexdigest() if header_path.exists() else None,
        "raw_headers_sha256": hashlib.sha256(raw_headers).hexdigest() if headers != raw_headers else None,
        "header_storage": "redacted session headers/redirect query" if headers != raw_headers else "verbatim",
        "body_sha256": hashlib.sha256(body).hexdigest() if body_received else None,
        "body_bytes": len(body) if body_received else None,
        "body_filename": args.body.name if body_received and not args.discard_body else None,
        "body_storage": ("gzip" if args.gzip else "verbatim") if body_received and not args.discard_body else "none",
    }
    args.receipt.with_suffix(".transport.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, ensure_ascii=False))
    return process.returncode or (0 if curl.get("response_code") == 200 and body_received else 1)


if __name__ == "__main__":
    raise SystemExit(main())
