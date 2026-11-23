"""Download the exact released fixture assets into a disposable cache."""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent.parent / "evidence" / "runtime"


def fetch(directory, url, digest, name=None):
    directory.mkdir(exist_ok=True, parents=True)
    if name is None:
        name = Path(unquote(urlsplit(url).path)).name
    path = directory / name
    exists = path.is_file()
    if exists:
        data = path.read_bytes()
    else:
        with urlopen(url, timeout=30) as response:
            data = response.read()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError(f"Digest mismatch for {url}")
    if not exists:
        path.write_bytes(data)
    print(path, len(data), digest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cache", type=Path)
    args = parser.parse_args()
    for gem in json.loads((HERE / "ruby-gem-digests.json").read_bytes()):
        fetch(args.cache / "gems", gem["url"], gem["sha256"])
    for context in json.loads((HERE / "ld3-contexts.json").read_bytes()):
        fetch(args.cache / "contexts", context["source"], context["sha256"], context["name"])
    for package in json.loads((HERE / "jschon-pip-report.json").read_bytes())["install"]:
        distribution = package["download_info"]
        fetch(args.cache / "wheels", distribution["url"], distribution["archive_info"]["hashes"]["sha256"])
