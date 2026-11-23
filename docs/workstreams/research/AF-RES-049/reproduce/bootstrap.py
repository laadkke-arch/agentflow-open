"""Install one locked legacy plotting prefix from fresh, verified downloads."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
from urllib.request import urlopen
from zipfile import ZipFile


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", choices=("3.0.2", "2.2.2"), required=True)
    parser.add_argument("--prefix", type=Path, required=True)
    args = parser.parse_args()
    if platform.system() != "Linux" or platform.machine() != "x86_64":
        parser.error("The locked distribution set is for Linux x86_64.")

    prefix = args.prefix.resolve()
    owned = Path(__file__).resolve().parents[1]
    git_root = owned.parents[3]
    if prefix.is_relative_to(git_root):
        parser.error("Create the disposable software prefix outside the checkout.")
    prefix.mkdir(parents=True, exist_ok=False)
    locked = json.loads(Path(__file__).with_name("distributions.json").read_text())
    env = dict(os.environ, PYTHONNOUSERSITE="1", PIP_CONFIG_FILE=os.devnull)
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)

    with tempfile.TemporaryDirectory(prefix="af049-fresh-downloads-") as cache:
        if list(Path(cache).iterdir()):
            raise RuntimeError("Download cache was not empty.")
        wheels = []
        for item in locked["distributions"]:
            if item.get("name") == "matplotlib" and item["version"] != args.version:
                continue
            path = Path(cache, item["filename"])
            with urlopen(item["url"], timeout=60) as response, path.open("xb") as out:
                shutil.copyfileobj(response, out)
            digest = sha256(path)
            if digest != item["sha256"]:
                raise ValueError("Hash mismatch for " + path.name)
            print("sha256", digest, path.name, flush=True)
            if item["role"] == "python_runtime":
                subprocess.run(["tar", "--extract", "--bzip2", "--no-same-owner",
                                "--no-same-permissions", "--exclude=info",
                                "--directory", str(prefix), "--file", str(path)], check=True)
            elif item["role"] == "pip_bootstrap":
                with ZipFile(path) as archive:
                    archive.extractall(prefix / "lib/python3.6/site-packages")
            else:
                wheels.append(path)

        python = str(prefix / "bin/python3.6")
        pip = [python, "-B", "-s", "-m", "pip", "--disable-pip-version-check"]
        subprocess.run([*pip, "install", "--no-index", "--no-deps", "--no-cache-dir",
                        *(str(wheel) for wheel in wheels)], env=env, check=True)
        subprocess.run([*pip, "check"], env=env, check=True)
        subprocess.run([*pip, "freeze", "--all"], env=env, check=True)


if __name__ == "__main__":
    main()
