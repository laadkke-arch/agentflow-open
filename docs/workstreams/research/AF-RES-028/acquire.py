#!/usr/bin/env python3
"""Fetch and build the exact queued versions. Keep archives and complete logs in a cache."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import time

REPOS = {"python": "python/cpython", "node": "nodejs/node"}
HERE = Path(__file__).resolve().parent


def sha(path, algorithm="sha256"):
    with path.open("rb") as f:
        return hashlib.file_digest(f, algorithm).hexdigest()


def download(folder, url, filename, events):
    dest = folder / filename
    command = ["curl", "--fail", "--location", "--silent", "--show-error", "--max-time", "95",
               "--output", str(dest) + ".part", "--write-out", "%{http_code} %{size_download}", url]
    start = time.monotonic()
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    events.append(dict(phase="download", url=url, command=command, rc=result.returncode,
                       response=result.stdout, stderr=result.stderr.strip(), wall_s=round(time.monotonic() - start, 3),
                       file=filename))
    if result.returncode:
        Path(str(dest) + ".part").unlink(missing_ok=True)
        return None
    Path(str(dest) + ".part").replace(dest)
    return dest


def process(folder, phase, command, cwd, events, env=None, timeout=900):
    path = folder / (phase + ".log")
    start = time.monotonic()
    try:
        with path.open("wb") as log:
            result = subprocess.run(command, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT,
                                    timeout=timeout)
        rc = result.returncode
    except subprocess.TimeoutExpired:
        rc = 124
    events.append(dict(phase=phase, command=command, cwd=str(cwd), rc=rc,
                       log=path.name, log_sha256=sha(path), bytes=path.stat().st_size,
                       wall_s=round(time.monotonic() - start, 3)))
    return rc


def extract(path, dest):
    dest.mkdir(exist_ok=True)
    with tarfile.open(path) as archive:
        archive.extractall(dest, filter="data")
    children = sorted(dest.iterdir())
    if len(children) != 1 or not children[0].is_dir():
        raise ValueError(f"Unexpected archive roots: {children}")
    return children[0]


def acquire(cache, eco, release, refinfo, jobs, system):
    tag, commit = release["tag"], release["commit"]
    version = tag.removeprefix("v")
    folder = cache / f"{eco}-{version}"
    folder.mkdir(exist_ok=True)
    status_path = folder / "build.json"
    if status_path.is_file():
        record = json.loads(status_path.read_text())
        if record["status"] == "ready" and Path(record["binary"]).is_file():
            return {**record, "reused_in_acquisition": True}
    events = []
    row = dict(ecosystem=eco, version=version, commit=commit, public_date=release["public_date"],
               tag=tag, tag_object=refinfo.get("refs/tags/" + tag, ""),
               tag_verified=refinfo.get("refs/tags/" + tag + "^{}", refinfo.get("refs/tags/" + tag)) == commit,
               archive_url="", sha256="", checksum_origin="", checksum_url="", bytes=0,
               binary="", binary_sha256="", mode="", status="unavailable", events=events)
    try:
        if not row["tag_verified"]:
            raise ValueError("published tag did not resolve to the pinned Git commit")
        if eco == "node":
            name = f"node-{tag}-linux-x64.tar.xz"
            base = f"https://nodejs.org/dist/{tag}/"
            row["archive_url"] = base + name
            row["checksum_url"] = base + "SHASUMS256.txt"
            manifest = download(folder, row["checksum_url"], "SHASUMS256.txt", events)
            path = download(folder, row["archive_url"], name, events)
            if manifest is None or path is None:
                raise ValueError("official archive or checksum unavailable")
            expected = dict((parts[1], parts[0]) for line in manifest.read_text().splitlines()
                            if len(parts := line.split()) == 2)[name]
            if sha(path) != expected:
                raise ValueError("official checksum mismatch")
            row["checksum_origin"] = "Node release SHA-256"
            row["mode"] = "official_linux_x64_binary"
        else:
            orig_name = f"Python-{version}.tar.xz"
            preferred = f"https://www.python.org/ftp/python/{version}/{orig_name}"
            row["archive_url"] = f"https://codeload.github.com/python/cpython/tar.gz/{commit}"
            if version == "3.10.1":
                # Save the official download attempt before selecting the alternate,
                # commit-addressed distribution route used uniformly for CPython.
                download(folder, preferred, orig_name, events)
            path = download(folder, row["archive_url"], f"cpython-{commit}.tar.gz", events)
            if path is None:
                raise ValueError("commit-addressed upstream archive unavailable")
            row["checksum_origin"] = "observed SHA-256 of commit-addressed GitHub archive; tag verified separately"
            row["mode"] = "official_tag_local_source_build"
        row["sha256"], row["bytes"] = sha(path), path.stat().st_size
        start = time.monotonic()
        extract_dir = folder / "source"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        src = extract(path, extract_dir)
        events.append(dict(phase="extract", file=path.name, rc=0, wall_s=round(time.monotonic() - start, 3)))
        if eco == "node":
            binary = src / "bin/node"
        else:
            prefix = folder / "install"
            env = os.environ.copy()
            args = [str(src / "configure"), f"--prefix={prefix}", "--with-ensurepip=no"]
            tk = system / "usr/include/tcl8.6"
            if tk.is_dir() and version.startswith("3.10."):
                args.extend([f"--with-tcltk-includes=-I{tk}", "--with-tcltk-libs=-ltk8.6 -ltcl8.6"])
            elif tk.is_dir():
                env["TCLTK_CFLAGS"] = f"-I{tk}"
                env["TCLTK_LIBS"] = "-ltk8.6 -ltcl8.6"
            for phase, command in (("configure", args), ("make", ["make", f"-j{jobs}"]),
                                   ("install", ["make", f"-j{jobs}", "install", "TESTSUBDIRS="])):
                if process(folder, phase, command, src, events, env=env):
                    raise ValueError(f"{phase} failed; see build log")
            binary = prefix / "bin" / f"python{version.rsplit('.', 1)[0]}"
        if not binary.is_file():
            raise ValueError(f"Missing output binary {binary}")
        row.update(status="ready", binary=str(binary), binary_sha256=sha(binary))
    except (ValueError, OSError, KeyError, tarfile.TarError) as e:
        row["failure"] = str(e)
    status_path.write_text(json.dumps(row, indent=2) + "\n")
    print(eco, version, row["status"], row.get("failure", ""), flush=True)
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packets", type=Path, default=HERE / "packets.jsonl")
    ap.add_argument("--cache", required=True, type=Path)
    ap.add_argument("--system", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--build-workers", type=int, default=1)
    options = ap.parse_args()
    options.cache = options.cache.resolve()
    options.cache.mkdir(parents=True, exist_ok=True)
    options.system = options.system.resolve()
    releases = {}
    for packet in map(json.loads, options.packets.read_text().splitlines()):
        for release in (packet["t0"], packet["target"]):
            releases[packet["ecosystem"], release["tag"]] = release
    refs = {}
    for eco, repo in REPOS.items():
        patterns = [f"refs/tags/{tag}{suffix}" for domain, tag in releases if domain == eco
                    for suffix in ("", "^{}")]
        url = f"https://github.com/{repo}.git"
        start = time.monotonic()
        result = subprocess.run(["git", "ls-remote", url, *patterns], capture_output=True, check=True)
        raw = options.cache / f"{eco}-tags.txt"
        raw.write_bytes(result.stdout)
        (options.cache / f"{eco}-tags.json").write_text(json.dumps(
            dict(url=url, command=["git", "ls-remote", url, *patterns], rc=result.returncode,
                 sha256=sha(raw), bytes=raw.stat().st_size, wall_s=round(time.monotonic() - start, 3))) + "\n")
        refs[eco] = {ref: commit for commit, ref in (line.split() for line in result.stdout.decode().splitlines())}

    # Baseline first, then oldest quarter first. Later lines may reuse an already acquired version.
    work = sorted(releases.items(), key=lambda pair: (pair[0][0], pair[1]["public_date"]))
    with ThreadPoolExecutor(max_workers=options.build_workers) as builds, ThreadPoolExecutor(max_workers=4) as binaries:
        futures = [(builds if eco == "python" else binaries).submit(
            acquire, options.cache, eco, release, refs[eco], options.jobs, options.system)
                   for (eco, _), release in work]
        rows = [future.result() for future in futures]
    options.out.write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
