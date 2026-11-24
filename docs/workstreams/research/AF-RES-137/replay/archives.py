"""Read official Python release archives and preserve targeted source files."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import tarfile
from urllib.request import urlopen

PACKAGES = {
    "scikit-image": (
        "0.24.0", "0.25.0rc0", "0.25.0rc1", "0.25.0rc2", "0.25.0", "0.25.1",
        "0.25.2rc0", "0.25.2", "0.26.0rc0", "0.26.0rc1", "0.26.0rc2", "0.26.0",
    ),
    "xarray": ("2024.9.0", "2024.10.0", "2024.11.0", "2025.1.0", "2025.1.1", "2025.1.2"),
}
FILES = {
    "xarray": (
        "pyproject.toml", "xarray/core/datatree.py", "xarray/core/utils.py",
        "xarray/coding/times.py", "xarray/conventions.py", "xarray/coders.py",
    ),
    "scikit-image": (
        "pyproject.toml", "skimage/graph/_graph.py", "src/skimage/graph/_graph.py",
        "doc/examples/filters/plot_deconvolution.py", "skimage/restoration/deconvolution.py",
        "src/skimage/restoration/deconvolution.py", ".github/workflows/wheels-recipe.yaml",
    ),
}
SKIMAGE_RC0 = "https://github.com/scikit-image/scikit-image/archive/refs/tags/v0.26.0rc0.tar.gz"


def download(url):
    with urlopen(url, timeout=35) as response:
        return response.read()


def select_files(source, known_paths, destination):
    selected = {}
    with tarfile.open(fileobj=BytesIO(source)) as archive:
        for member in archive:
            path = member.name.split("/", 1)[-1]
            if path in known_paths and member.isfile():
                file = archive.extractfile(member).read()
                (destination / path.replace("/", "__")).write_bytes(file)
                selected[path] = sha256(file).hexdigest()
    return selected


def read_archive(root, package, version):
    metadata_url = f"https://pypi.org/pypi/{package}/{version}/json"
    metadata = json.loads(download(metadata_url))
    files = metadata["urls"]
    source = next((file for file in files if file.get("packagetype") == "sdist"), None)
    receipt = {
        "package": package, "version": version, "pypi_url": metadata_url,
        "first_upload_utc": min((file["upload_time_iso_8601"] for file in files), default=None),
        "requires_python": metadata["info"]["requires_python"],
        "requires_dist": metadata["info"]["requires_dist"],
        "release_files": len(files),
        "free_threaded_wheels": [{"filename": file["filename"], "url": file["url"],
                                  "upload_utc": file["upload_time_iso_8601"], "sha256": file["digests"]["sha256"]}
                                 for file in files if "cp313t" in file["filename"]],
        "observed_utc": datetime.now(timezone.utc).isoformat(),
    }
    destination = root / package / version
    destination.mkdir(parents=True, exist_ok=True)
    if source or (package, version) == ("scikit-image", "0.26.0rc0"):
        url = source["url"] if source else SKIMAGE_RC0
        receipt["pypi_sdist"] = bool(source)
        try:
            body = download(url)
            digest = sha256(body).hexdigest()
            if source and digest != source["digests"]["sha256"]:
                raise ValueError(f"PyPI archive hash mismatch at {url}")
            receipt["archive"] = {
                "url": url, "sha256": digest, "upload_utc": source["upload_time_iso_8601"] if source else None,
                "files": select_files(body, FILES[package], destination),
            }
        except OSError as error:
            receipt["archive_failure"] = {"url": url, "error": str(error)}
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    combinations = [(pkg, v) for pkg, versions in PACKAGES.items() for v in versions]
    with ThreadPoolExecutor(max_workers=5) as threads:
        for receipt in threads.map(lambda p: read_archive(args.output, *p), combinations):
            print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
