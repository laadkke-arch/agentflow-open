"""Prepare the pinned tools in a new Linux amd64 scratch directory."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

from harness import VERSION_LOCK, file_hash

SOURCE = Path(__file__).resolve().parent


def run(argv, directory, env=None):
    print("+", subprocess.list2cmdline([str(arg) for arg in argv]), flush=True)
    subprocess.run(argv, cwd=directory, env=env, check=True)


def download(url, target, sha256):
    run(["curl", "-fsSL", "--retry", "1", url, "-o", target], target.parent)
    if file_hash(target) != sha256:
        raise ValueError(f"SHA-256 mismatch for {target.name}")


def setup_yq(root):
    for version, lock in VERSION_LOCK["yq"].items():
        archive = root / lock["file"]
        download(lock["archive"], archive, lock["archive_sha256"])
        release = root / f"yq-{version}"
        release.mkdir()
        run(["tar", "-xzf", archive, "-C", release, "yq_linux_amd64"], root)
        binary = release / "yq_linux_amd64"
        if file_hash(binary) != lock["binary_sha256"]:
            raise ValueError(f"Mismatched yq {version} archive member")
        run([binary, "--version"], root)


def setup_csv(root, jobs, includes, libraries):
    build_env = os.environ.copy()
    if includes:
        build_env["CPPFLAGS"] = f"-I{includes}"
    if libraries:
        build_env["LDFLAGS"] = f"-L{libraries}"
    binaries = {}
    for version, lock in VERSION_LOCK["cpython"].items():
        archive = root / lock["file"]
        download(lock["archive"], archive, lock["sha256"])
        run(["tar", "-xzf", archive], root)
        source = root / f"cpython-{version}"
        run(["./configure", f"--prefix={root / ('python-' + version)}", "--with-ensurepip=no"], source, build_env)
        run(["make", "-j", str(jobs)], source, build_env)
        binaries[version] = source / "python"
        run([binaries[version], "-c", "import bz2,lzma,sys; print(sys.version)"], source)
    for version, lock in VERSION_LOCK["csvkit"].items():
        venv = root / f"csvkit-{version}"
        environment(root, venv, binaries[lock["python"]], lock["lock"], lock["lock_sha256"])
        for command in ("csvformat", "csvstat", "in2csv"):
            run([venv / "bin" / command, "--version"], root)


def environment(root, venv, python, filename, sha256):
    lock = SOURCE / filename
    if file_hash(lock) != sha256:
        raise ValueError(f"Unexpected package lock: {lock}")
    env = dict(os.environ, UV_CACHE_DIR=str(root / "uv-cache"))
    run(["uv", "venv", "--no-project", "--python", python, venv], root, env)
    run(["uv", "pip", "sync", "--python", venv / "bin" / "python", "--require-hashes", lock], root, env)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=lambda p: Path(p).resolve())
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--build-includes", type=Path)
    parser.add_argument("--build-libraries", type=Path)
    options = parser.parse_args()
    root = options.directory
    root.mkdir(parents=True, exist_ok=False)
    setup_yq(root)
    setup_csv(root, options.jobs, options.build_includes, options.build_libraries)
    lock = VERSION_LOCK["yaml_reader"]
    environment(root, root / "yaml-reader", sys.executable, lock["lock"], lock["lock_sha256"])
