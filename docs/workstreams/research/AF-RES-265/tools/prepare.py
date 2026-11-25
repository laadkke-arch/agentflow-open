"""Retrieve pinned public inputs into a separate scratch directory."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ASSETS = ("KhronosGroup/glTF-Sample-Assets", "e124e8d8d7330a5372bc2b4d00d39a4a9d7997ea")
THREE = ("mrdoob/three.js", "084ec06444244980752a420f0e1af5cd8f112aa1")
EPUB = ("IDPF/epub3-samples", "7651e2002b631e6577fadf7e9e0692fa6efb8746")
MODELS = ("Box", "BoxTextured", "AnisotropyBarnLamp")
BOOK = "30/cc-shared-culture/"
THREE_FILES = (
    "build/three.module.js", "build/three.core.js",
    "examples/jsm/loaders/GLTFLoader.js", "examples/jsm/loaders/KTX2Loader.js",
    "examples/jsm/utils/BufferGeometryUtils.js", "examples/jsm/utils/SkeletonUtils.js",
    "examples/jsm/utils/WorkerPool.js", "examples/jsm/math/ColorSpaces.js",
    "examples/jsm/libs/ktx-parse.module.js", "examples/jsm/libs/zstddec.module.js",
    "examples/jsm/libs/basis/basis_transcoder.js", "examples/jsm/libs/basis/basis_transcoder.wasm",
    "examples/jsm/environments/RoomEnvironment.js",
)


def git(cwd, *args):
    return subprocess.check_output(["git", "-C", cwd, *args], text=True).strip()


def index(root, group, repository, selected):
    project, commit = repository
    db = root / "_git" / group
    db.mkdir(parents=True, exist_ok=True)
    git(db, "init", "-q")
    url = f"https://github.com/{project}.git"
    print(f"git fetch --depth=1 --filter=blob:none {url} {commit}", flush=True)
    git(db, "fetch", "--quiet", "--depth=1", "--filter=blob:none", url, commit)
    assert git(db, "rev-parse", "FETCH_HEAD") == commit
    edition = git(db, "show", "-s", "--format=%cI", commit)
    records = []
    for line in git(db, "ls-tree", "-r", commit).splitlines():
        meta, path = line.split("\t", 1)
        _mode, kind, blob = meta.split()
        if kind != "blob" or not selected(path):
            continue
        from urllib.parse import quote
        records.append({
            "path": path,
            "repo": project,
            "commit": commit,
            "edition_date": edition,
            "tree_blob": blob,
            "group": group,
            "url": f"https://raw.githubusercontent.com/{project}/{commit}/{quote(path, safe='/')}",
        })
    return db, records


def fetch(root, record):
    out = root / record["group"] / record["path"]
    out.parent.mkdir(parents=True, exist_ok=True)
    process = subprocess.run(
        ["curl", "-fsSL", "--max-time", "45", "--retry", "1",
         "--write-out", "%{http_code}", "-o", str(out), record["url"]],
        capture_output=True, text=True,
    )
    if process.returncode:
        raise RuntimeError(f"{record['url']}: curl exit={process.returncode}, {process.stdout}, {process.stderr}")
    data = out.read_bytes()
    blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    if blob != record["tree_blob"]:
        raise RuntimeError(f"Git blob mismatch for {record['path']}: {blob}")
    return {**record, "http": int(process.stdout), "bytes": len(data), "git_blob": blob,
            "sha256": hashlib.sha256(data).hexdigest(), "stderr": process.stderr,
            "opened_utc": datetime.now(timezone.utc).isoformat()}


def selected_asset(path):
    parts = path.split("/")
    if len(parts) < 3 or parts[0] != "Models" or parts[1] not in MODELS:
        return False
    return (len(parts) == 3 and parts[2] == "README.md") or (
        len(parts) == 4 and (parts[2] in {"glTF", "glTF-Binary"} or
                            parts[1:] == ["AnisotropyBarnLamp", "glTF-KTX-BasisU", parts[3]]))


def book_archive(root, records):
    archive = root / "Shared-Culture-repacked.epub"
    pages = [r["path"] for r in records if r["group"] == "epub"]
    pages.sort(key=lambda path: (path != BOOK + "mimetype", path))
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as zf:
        for path in pages:
            name = path.removeprefix(BOOK)
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            zf.writestr(info, (root / "epub" / path).read_bytes())
    return {"file": archive.name, "entries": len(pages), "bytes": archive.stat().st_size,
            "sha256": hashlib.file_digest(archive.open("rb"), "sha256").hexdigest(),
            "kind": "deterministic local repack of pinned publisher tree"}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("output", type=Path)
    root = cli.parse_args().output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    db, assets = index(root, "assets", ASSETS, selected_asset)
    _, runtime = index(root, "three", THREE, lambda path: path in THREE_FILES)
    _, epub = index(root, "epub", EPUB, lambda path: path.startswith(BOOK))
    assert len(runtime) == len(THREE_FILES) and len(epub) >= 20
    with ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(lambda record: fetch(root, record), assets + runtime + epub))
    for r in rows:
        if r["path"].endswith(".glb"):
            original = subprocess.run(
                ["git", "-C", db, "fetch", "--quiet", "--depth=1", f"https://github.com/{r['repo']}.git", r["tree_blob"]],
                capture_output=True, text=True, check=True,
            )
            r["git_fetch_stderr"] = original.stderr
            r["git_cat_file_size"] = int(git(db, "cat-file", "-s", r["tree_blob"]))
            assert r["git_cat_file_size"] == r["bytes"]
        print(f"{r['http']} {r['bytes']:>9} {r['tree_blob']} {r['sha256']} {r['group']}/{r['path']}")
    result = {"files": rows, "epub_archive": book_archive(root, rows)}
    (root / "input-manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result["epub_archive"], ensure_ascii=False))


if __name__ == "__main__":
    main()
