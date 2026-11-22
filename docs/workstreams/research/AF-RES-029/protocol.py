"""Small prospective serialization gates for AF-RES-029, not a search engine.

Run with PYTHONDONTWRITEBYTECODE=1. No network, model calls, or repository-wide writes.
Route workers call write_return before any final-return file is created. Rejected
attempts are logged; an after-the-fact truncation is never substituted silently.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urldefrag

ROOT = Path(__file__).resolve().parent


def utc():
    return datetime.now(timezone.utc).isoformat()


def document_url(url):
    # Parameters may distinguish versions; only fragments are collapsed.
    return urldefrag(url)[0]


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_return(path, packet):
    """Validate original packet and create it once. Never clip/reorder candidates."""
    path = Path(path).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("return outside owned path")
    if path.exists():
        raise ValueError("sealed return already exists; append correction separately")
    if packet.get("route") not in ("A", "B", "C"):
        raise ValueError("route must be A, B or common-only C")
    candidates = packet.get("candidates", [])
    urls = set()
    if len(candidates) > 3:
        raise ValueError("more than three original candidates")
    for ordinal, candidate in enumerate(candidates, 1):
        if candidate.get("rank") != ordinal:
            raise ValueError("original ranks must be contiguous")
        citations = candidate.get("citations", [])
        if not citations:
            raise ValueError("nonempty candidate must cite an actually read URL/section")
        for citation in citations:
            if not citation.get("url", "").startswith(("https://", "http://")) or not citation.get("section"):
                raise ValueError("citation needs public URL and exact read section")
            urls.add(document_url(citation["url"]))
    if len(urls) > 3:
        raise ValueError("more than three original document URLs")
    budget = packet.get("budget", {})
    if packet["route"] != "C":
        if budget.get("navigation", 0) > 2 or budget.get("body_opens", 0) > 4:
            raise ValueError("route budget exceeded; preserve as violation rather than compliant return")
    packet["serialization_gate"] = {
        "checked_utc": utc(), "candidate_count": len(candidates),
        "distinct_document_urls": sorted(urls), "url_count": len(urls),
        "posthoc_truncation": False,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(packet, ensure_ascii=False, indent=2) + "\n"
    path.write_text(data, encoding="utf-8")
    return hashlib.sha256(data.encode()).hexdigest()


def seal_files(files, destination, label):
    destination = Path(destination).resolve()
    if not destination.is_relative_to(ROOT) or destination.exists():
        raise ValueError("seal must be a new owned file")
    record = {"label": label, "created_utc": utc(), "files": {}}
    for value in sorted(map(str, files)):
        path = Path(value).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError("sealed file outside owned path")
        record["files"][str(path.relative_to(ROOT))] = sha256_file(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    return record
