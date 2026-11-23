"""Reconstruct ignored probe inputs from pinned public primary sources.

Run this, then run-probes.py, from a clean result checkout. No system packages
are installed. R0 full bodies and official binary are cached, never committed.
Hashes reject changed inputs instead of silently treating them as the experiment.
"""
import datetime
import hashlib
import json
from pathlib import Path
import tarfile
import urllib.parse
import urllib.request

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
ARCHIVE_URL = "https://github.com/jgm/pandoc/releases/download/3.6/pandoc-3.6-linux-amd64.tar.gz"
ARCHIVE_SHA256 = "8e3702b195f75412e425df46f8f3f08241b66a2b33abbd9e04eda501bfde860c"
BINARY_SHA256 = "7f1ac56064cdc02cdf8bd913f9ea45ba07fbb74419e755328c4571e4470769b2"
INPUTS = [
    (79375162, "1B054996-200D-4090-BAC2-A656EDCBC92D", "aa68802d57a2ab46c2fa48e6e484407046ae0c6344c788862037f478cc88793c"),
    (79393445, "5938869D-E61B-410C-97F5-035731293446", "ddb73cf5ed41e2931fdefc58a7e180391b3741ca3b18ed7d0b8243a3f1ff28bf"),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": "AF-RES-096-post-seal-replay"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def main():
    CACHE.mkdir(exist_ok=True)
    (CACHE / "inputs").mkdir(exist_ok=True)
    records = []
    archive = CACHE / "pandoc-3.6-linux-amd64.tar.gz"
    data = archive.read_bytes() if archive.exists() else get(ARCHIVE_URL)
    assert sha(data) == ARCHIVE_SHA256, "Official release archive bytes differ from recorded probe input"
    archive.write_bytes(data)
    with tarfile.open(archive, "r:gz") as tar:
        members = [m for m in tar.getmembers() if m.isfile() and m.name.endswith("/bin/pandoc")]
        assert len(members) == 1
        binary = tar.extractfile(members[0]).read()
    assert sha(binary) == BINARY_SHA256
    executable = CACHE / "pandoc-3.6"
    executable.write_bytes(binary)
    executable.chmod(0o755)
    records.append({"kind": "official_binary", "url": ARCHIVE_URL, "archive_sha256": ARCHIVE_SHA256, "binary_sha256": BINARY_SHA256})
    for question_id, guid, expected in INPUTS:
        params = urllib.parse.urlencode({"site": "stackoverflow", "filter": "!R1.Y5iw_Z1WCrEMwmtA2p"})
        url = "https://api.stackexchange.com/2.3/revisions/" + guid + "?" + params
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        response = json.loads(get(url))
        matches = [x for x in response.get("items", []) if x.get("revision_guid", "").upper() == guid and x.get("body")]
        assert len(matches) == 1, "Exact R0 revision body unavailable"
        body = matches[0]["body"].encode()
        assert sha(body) == expected, "R0 body bytes differ from recorded source"
        target = CACHE / "inputs" / ("question-" + str(question_id) + "-" + guid + ".html")
        target.write_bytes(body)
        records.append({"kind": "R0", "question_id": question_id, "revision_guid": guid, "url": url, "started_utc": started, "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "body_sha256": expected, "cache": str(target.relative_to(HERE)), "minimum_count_eligible": False, "reason": "Repeat source reconstruction after seal; original R0 already counted."})
    output = {"checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "records": records, "system_packages_installed": False}
    (HERE / "prepare-receipt.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
