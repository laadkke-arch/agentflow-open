"""Fetch fixed upstream tree archives and prepare the exact input files for replay."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tarfile
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TZ_MEMBERS = ("africa", "antarctica", "asia", "australasia", "europe",
              "northamerica", "southamerica", "etcetera", "backward")
# Parent files for the sampled branches and the optional en_US role comparison.
CLDR_LOCALES = ("en_ZA", "en_001", "en_US", "en", "ar_EG", "ar", "de_DE", "de", "root")
CLDR_MEMBERS = {f"common/main/{loc}.xml" for loc in CLDR_LOCALES} | {
    "common/supplemental/supplementalData.xml",
    "common/supplemental/supplementalMetadata.xml",
    "common/supplemental/numberingSystems.xml",
    "common/dtd/ldml.dtd",
}


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def get_editions():
    with (ROOT / "editions.csv").open(encoding="utf-8", newline="") as stream:
        return [row for row in csv.DictReader(stream) if row["selection"] == "included"]


def acquire(scratch, edition, expected, fetch):
    identity = f'{edition["family"]}-{edition["edition"]}'
    archive = scratch / "downloads" / f"{identity}.tar.gz"
    request_receipt = None
    if not archive.exists():
        if not fetch:
            raise FileNotFoundError(f"archive missing: {archive}; add --fetch")
        started = utc()
        then = time.perf_counter()
        uri = edition["fixed_tree_archive"]
        request = Request(uri, headers={"Accept-Encoding": "identity", "User-Agent": "AF-RES-147"})
        temporary = archive.with_suffix(".part")
        try:
            with urlopen(request, timeout=90) as response, temporary.open("wb") as out:
                shutil.copyfileobj(response, out, length=128 * 1024)
                request_receipt = {
                    "started_utc": started, "status": response.status, "url": uri,
                    "effective_url": response.url,
                    "content_encoding": response.getheader("Content-Encoding"),
                    "http_entity_body_bytes": out.tell(),
                }
            temporary.replace(archive)
        finally:
            temporary.unlink(missing_ok=True)
        request_receipt["wall_ms"] = round((time.perf_counter() - then) * 1000, 3)
    digest = sha256(archive)
    if expected and digest != expected[identity]["archive_sha256"]:
        raise ValueError(f"archive SHA-256 mismatch for {identity}: {digest}")
    return identity, archive, request_receipt, digest


def run(command, directory):
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=90,
                            env={**os.environ, "LC_ALL": "C"})
    if result.returncode:
        raise RuntimeError(f"{command}: {result.returncode}\n{result.stdout}\n{result.stderr}")
    return {"command": command, "exit": result.returncode, "stderr": result.stderr,
            "stdout": result.stdout}


def prepare_tz(archive, source, prepared, version):
    with tarfile.open(archive) as package:
        prefix = PurePosixPath(package.getmembers()[0].name).parts[0]
        package.extractall(source, filter="data")
    tree = source / prefix
    # The Git tree omits the dist-generated version file. Its announced tag is fixed in editions.csv.
    if not (tree / "version").exists():
        (tree / "version").write_text(version + "\n", encoding="ascii")
    elif (tree / "version").read_text(encoding="ascii").strip() != version:
        raise ValueError(f"upstream version mismatch in {tree}")
    compile_command = run(["make", "CC=cc", "zic"], tree)
    prepared.mkdir(parents=True)
    create_command = run(["./zic", "-b", "fat", "-d", str(prepared), *TZ_MEMBERS], tree)
    zic = run(["./zic", "--version"], tree)["stdout"].strip()
    return tree, {"compiler": zic, "binary_sha256": sha256(tree / "zic"),
                  "flags": ["-b", "fat"], "commands": [compile_command, create_command]}


def prepare_cldr(archive, prepared):
    with tarfile.open(archive) as package:
        for item in package:
            path = "/".join(PurePosixPath(item.name).parts[1:])
            if path not in CLDR_MEMBERS or not item.isfile():
                continue
            target = prepared / path
            target.parent.mkdir(parents=True, exist_ok=True)
            with package.extractfile(item) as source, target.open("wb") as out:
                shutil.copyfileobj(source, out)
    return prepared, {"extracted_files": sorted(p.relative_to(prepared).as_posix()
                                                for p in prepared.rglob("*.xml"))}


def prepare_one(scratch, edition, expected, fetch):
    identity, archive, http, digest = acquire(scratch, edition, expected, fetch)
    family = edition["family"]
    version = edition["edition"]
    prepared = scratch / "prepared" / family / version
    source = scratch / "source" / family / version
    if prepared.exists() or source.exists():
        raise FileExistsError(f"prepare needs empty output trees: {prepared}, {source}")
    then = time.perf_counter()
    if family == "tzdb":
        tree, details = prepare_tz(archive, source, prepared, version)
        members = (*TZ_MEMBERS, "NEWS", "theory.html", "zic.8", "tzfile.5", "zone1970.tab")
    else:
        tree, details = prepare_cldr(archive, prepared)
        members = sorted(CLDR_MEMBERS)
    fingerprints = {key: sha256(tree / key) for key in members if (tree / key).is_file()}
    if expected and fingerprints != expected[identity]["source_member_sha256"]:
        raise ValueError(f"source member fingerprints differ for {identity}")
    return identity, {
        "edition": version, "family": family, "commit": edition["commit"],
        "archive_url": edition["fixed_tree_archive"], "archive_sha256": digest,
        "archive_bytes": archive.stat().st_size, "http": http,
        "prepared_wall_ms": round((time.perf_counter() - then) * 1000, 3),
        "source_member_sha256": fingerprints,
        "prep": details, "source_relative": tree.relative_to(scratch).as_posix(),
    }


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--scratch", type=Path, required=True)
    cli.add_argument("--fetch", action="store_true")
    cli.add_argument("--initialize-digests", action="store_true",
                     help="first evidence collection only; record digests for later replays")
    cli.add_argument("--receipt", type=Path, required=True)
    args = cli.parse_args()
    scratch = args.scratch.resolve()
    (scratch / "downloads").mkdir(parents=True, exist_ok=True)
    expected = None if args.initialize_digests else json.loads(
        (ROOT / "evidence" / "artifacts.json").read_text(encoding="utf-8"))
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(prepare_one, scratch, edition, expected, args.fetch)
                   for edition in get_editions()]
        results = dict(future.result() for future in futures)
    args.receipt.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
