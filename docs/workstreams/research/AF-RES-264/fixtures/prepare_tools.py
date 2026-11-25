"""Fetch the recorded official packages and check their hashes before extraction."""
import argparse
import json
import os
from pathlib import Path

from receipt import digest, invoke, write_json

FIXTURES = Path(__file__).resolve().parent
PINS = json.loads((FIXTURES / "downloads.json").read_text(encoding="utf-8"))


def prepare(root, receipts):
    root.mkdir(parents=True)
    receipts.mkdir(parents=True)
    (root / "raw").mkdir()
    (root / "bin").mkdir()
    observations = []

    def checked(name, *argv, env=None, output=None):
        command = invoke(receipts, name, argv, cwd=root, env=env, output=output)
        if command["exit"] != 0:
            raise SystemExit(f"{name} failed; see {receipts}")

    def install(spec, prefix):
        name = spec["url"].rsplit("/", 1)[-1]
        package = root / "raw" / name
        checked(name + "-download", "curl", "--fail", "--location", "--silent", "--show-error",
                "--max-time", "60", "--output", package,
                "--write-out", "%{http_code} %{size_download}\n", spec["url"])
        sha = digest(package)
        size = package.stat().st_size
        if sha != spec["sha256"] or size != spec.get("bytes", size):
            raise SystemExit("Package fingerprint mismatch: " + name)
        checked(name + "-fields", "dpkg-deb", "-f", package, "Package", "Version", "Architecture")
        checked(name + "-extract", "dpkg-deb", "-x", package, prefix)
        observations.append(dict(file=name, bytes=size, sha256=sha, url=spec["url"]))

    repo = root / "pandoc-source"
    repo.mkdir()
    checked("git-init", "git", "-C", repo, "init", "-q")
    tags = [f"refs/tags/{version}:refs/tags/{version}" for version in PINS["pandoc"]]
    checked("git-fetch-tags", "git", "-C", repo, "fetch", "--depth=1", "--no-tags",
            "https://github.com/jgm/pandoc.git", *tags)
    for version, spec in PINS["pandoc"].items():
        prefix = root / "bin" / ("pandoc-" + version)
        install(spec, prefix)
        binary = prefix / "usr/bin/pandoc"
        if digest(binary) != spec["binary_sha256"]:
            raise SystemExit("Pandoc executable fingerprint mismatch: " + version)
        checked("pandoc-" + version + "-version", binary, "--version")
        version_text = (receipts / ("pandoc-" + version + "-version.stdout")).read_text()
        if version_text.splitlines()[0] != "pandoc " + version:
            raise SystemExit("Pandoc version mismatch: " + version)
        checked("tag-" + version, "git", "-C", repo, "rev-parse", version + "^{commit}")
        actual_tag = (receipts / ("tag-" + version + ".stdout")).read_text().strip()
        if actual_tag != spec["tag_commit"]:
            raise SystemExit("Tag commit mismatch: " + version)
        raw = root / "raw" / ("embedded-" + version + ".latex")
        tagged = root / "raw" / ("tagged-" + version + ".latex")
        checked("tag-template-" + version, "git", "-C", repo, "show",
                actual_tag + ":data/templates/default.latex", output=tagged)
        checked("embedded-template-" + version, binary, "--print-default-template=latex", output=raw)
        if digest(raw) != spec["template_sha256"] or raw.read_bytes() != tagged.read_bytes():
            raise SystemExit("Built-in and tagged template bytes differ: " + version)
        observations[-1].update(tag_commit=actual_tag, executable_sha256=digest(binary),
                                embedded_template_sha256=digest(raw), tag_template_equal=True)

    prefix = root / "bin/mupdf"
    for spec in PINS["mupdf_packages"]:
        install(spec, prefix)
    mutool = prefix / "usr/bin/mutool"
    if digest(mutool) != PINS["mutool_sha256"]:
        raise SystemExit("mutool executable fingerprint mismatch")
    engine_env = os.environ | {"LD_LIBRARY_PATH": str(prefix / "usr/lib/x86_64-linux-gnu")}
    checked("mutool-version", mutool, "-v", env=engine_env)
    checked("mutool-ldd", "ldd", mutool, env=engine_env)
    write_json(receipts / "packages.json", observations)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tools", type=Path, required=True)
    parser.add_argument("--receipts", type=Path, required=True)
    args = parser.parse_args()
    prepare(args.tools.resolve(), args.receipts.resolve())
