"""Verify and read the preserved upstream archive; no old code is executed."""
from pathlib import Path
import datetime
import gzip
import hashlib
import json
import re
import tarfile

ROOT = Path(__file__).parent
archive = ROOT / "cache/orig"
dsc = (ROOT / "cache/dsc").read_text()
receipts = {row["probe_id"]: row for row in
            map(json.loads, (ROOT / "http-receipts.jsonl").read_text().splitlines())}
checks = []
for key, filename in [("orig", "python-imaging_1.1.7.orig.tar.gz"),
                      ("debian-patch", "python-imaging_1.1.7-2.diff.gz")]:
    data = (ROOT / "cache" / key).read_bytes()
    for algorithm in ("sha256", "sha1", "md5"):
        value = hashlib.new(algorithm, data).hexdigest()
        checks.append({"file": filename, "algorithm": algorithm, "actual": value,
                       "bytes": len(data), "matches_dsc":
                       (value + " " + str(len(data)) + " " + filename) in dsc})
members = []
selected = ["README", "setup.py", "selftest.py", "PIL/Image.py", "PIL/__init__.py",
            "PIL/ImageFile.py", "PIL/PngImagePlugin.py"]
with tarfile.open(archive, "r:gz") as tar:
    member_count = len(tar.getmembers())
    for name in selected:
        member = tar.getmember("Imaging-1.1.7/" + name)
        data = tar.extractfile(member).read()
        (ROOT / "cache" / name.replace("/", "_")).write_bytes(data)
        members.append({"member": member.name, "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest(),
                        "mtime_utc": datetime.datetime.fromtimestamp(
                            member.mtime, datetime.timezone.utc).isoformat(),
                        "lines": len(data.splitlines())})
patch = gzip.decompress((ROOT / "cache/debian-patch").read_bytes()).decode()
patch_paths = re.findall(r"^\+\+\+ (\S+)", patch, flags=re.M)
image_bytes = (ROOT / "cache/PIL_Image.py").read_bytes()
record = {
    "check_id": "PIL-ARCHIVE-VERIFY-01", "actor": "gis_evidence tool agent",
    "location": "ChatGPT cloud Linux; isolated repository research directory",
    "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "command": "python3 streams/pil_archive/inspect_archive.py",
    "archive_url": receipts["orig"]["opened_url"],
    "archive_sha256": receipts["orig"]["sha256"],
    "archive_members": member_count, "checks": checks,
    "image_py_matches_debian_sources_1_1_7_2":
        image_bytes == (ROOT / "cache/debian-image-patched").read_bytes(),
    "patch_paths": patch_paths,
    "debian_patch_applied_to_original": False,
    "upstream_code_executed": False,
    "pgp_signature_verified": False,
    "provenance_scope": "Official Debian archive labels this orig upstream archive; separate Debian diff and signed descriptor agree on all computed digests. Upstream host response at release time and PGP trust chain were not independently verified.",
    "additional_independent_works": 0,
    "exit_code": 0 if all(x["matches_dsc"] for x in checks) else 1,
}
(ROOT / "archive-verification.json").write_text(json.dumps(record, indent=2) + "\n")
(ROOT / "source-members.json").write_text(json.dumps(members, indent=2) + "\n")
print(json.dumps(record, indent=2))
raise SystemExit(record["exit_code"])
