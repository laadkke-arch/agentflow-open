"""Project official registry metadata into the preregistered release frame."""
import argparse
import base64
import csv
import hashlib
import io
import json
import re
import tarfile
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from packaging.version import Version

HERE = Path(__file__).resolve().parent
PYPI = "https://pypi.org/pypi/tzdata/json"
NPM = "https://registry.npmjs.org/moment-timezone"
MOMENT = "https://registry.npmjs.org/moment"
STABLE_SEMVER = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:\+[0-9A-Za-z.-]+)?\Z")


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def time_key(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def digest(data, algorithm="sha256"):
    return hashlib.new(algorithm, data).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class HttpJournal:
    """Record application bodies, failures, redirects and local cache reads."""

    def __init__(self, cache=None):
        self.cache = cache
        self.events = []
        if self.cache is not None:
            self.cache.mkdir(parents=True, exist_ok=True)

    def get(self, url):
        cache_path = None
        if self.cache is not None:
            cache_path = self.cache / digest(url.encode())
            if cache_path.is_file():
                content = cache_path.read_bytes()
                self.events.append(dict(url=url, method="cache-read", utc=utc_now(),
                                        bytes=len(content), sha256=digest(content)))
                return content
        redirects = []

        class Follow(HTTPRedirectHandler):
            def redirect_request(self, request, fp, code, message, headers, newurl):
                body = fp.read()
                redirects.append(dict(url=request.full_url, to=newurl, status=code,
                                      bytes=len(body), sha256=digest(body)))
                return super().redirect_request(request, fp, code, message, headers, newurl)

        start = time.monotonic()
        event = {"url": url, "method": "GET", "utc": utc_now(), "redirects": redirects}
        request = Request(url, headers={"User-Agent": "AF-RES-059 public evidence replay",
                                        "Accept-Encoding": "identity"})
        try:
            with build_opener(Follow()).open(request, timeout=40) as response:
                content = response.read()
                event.update(status=response.status, final_url=response.url,
                             last_modified=response.headers.get("Last-Modified"),
                             etag=response.headers.get("ETag"))
        except HTTPError as exc:
            content = exc.read()
            event.update(status=exc.code, final_url=exc.url, error=str(exc))
        except (URLError, TimeoutError, OSError) as exc:
            content = b""
            event.update(status=None, error=str(exc))
        event.update(bytes=len(content), sha256=digest(content),
                     elapsed_ms=round((time.monotonic() - start) * 1000, 3))
        self.events.append(event)
        if "error" in event:
            return None
        if cache_path is not None:
            cache_path.write_bytes(content)
        return content


def npm_key(version):
    match = STABLE_SEMVER.fullmatch(version)
    if match:
        return tuple(map(int, match.groups()))


def stable_pypi(version):
    parsed = Version(version)
    return None if parsed.is_prerelease or parsed.is_devrelease else parsed


def frame(ecosystem, releases, start, end):
    rows = []
    for version, (published, available, yanked_or_deprecated) in releases.items():
        if ecosystem == "PyPI":
            sortable = stable_pypi(version)
        else:
            sortable = npm_key(version)
        rows.append(dict(ecosystem=ecosystem, version=version, record="release",
                         release_utc=published, registry_version_entry=available,
                         withdrawn_or_deprecated=yanked_or_deprecated, stable=sortable is not None))
    stable_timed = [row for row in rows if row["stable"] and row["release_utc"]]

    def stack_key(row):
        order = stable_pypi(row["version"]) if ecosystem == "PyPI" else npm_key(row["version"])
        return time_key(row["release_utc"]), order, row["version"]

    stable_timed.sort(key=stack_key)
    before = [row["version"] for row in stable_timed if time_key(row["release_utc"]) < start]
    after = [row["version"] for row in stable_timed if time_key(row["release_utc"]) >= end]
    for row in rows:
        published = row["release_utc"]
        if not published:
            row["selection"] = "no-public-time"
        elif not row["stable"]:
            row["selection"] = "pre/dev"
        elif start <= time_key(published) < end:
            row["selection"] = "window"
        elif before and row["version"] == before[-1]:
            row["selection"] = "before"
        elif after and row["version"] == after[0]:
            row["selection"] = "after"
        else:
            row["selection"] = "outside"
    return sorted(rows, key=lambda row: (
        time_key(row["release_utc"]) if row["release_utc"] else datetime.max.replace(tzinfo=timezone.utc),
        stack_key(row)[1] if row["stable"] and row["release_utc"] else
        (Version("0") if ecosystem == "PyPI" else (0, 0, 0)),
        row["version"],
    ))


def pypi_releases(package):
    return {version: (
        min((file["upload_time_iso_8601"] for file in files), key=time_key, default=None),
        bool(files), "; ".join(file.get("yanked_reason") or file["filename"]
                              for file in files if file.get("yanked")),
    ) for version, files in package["releases"].items()}


def npm_releases(package):
    versions = package["versions"]
    times = package["time"]
    return {version: (times.get(version), version in versions,
                      versions.get(version, {}).get("deprecated", ""))
            for version in versions.keys() | (times.keys() - {"created", "modified", "unpublished"})}


def pypi_files(package, version):
    for item in sorted(package["urls"], key=lambda file: (
            time_key(file["upload_time_iso_8601"]), file["filename"], file["digests"]["sha256"])):
        yield dict(ecosystem="PyPI", package="tzdata", version=version, filename=item["filename"],
                   kind=item["packagetype"], original_url=item["url"], declared_bytes=item["size"],
                   file_utc=item["upload_time_iso_8601"], registry_sha256=item["digests"]["sha256"],
                   yanked=item["yanked"], withdrawn_or_deprecated=item.get("yanked_reason"))


def npm_file(package, name, version):
    version_entry = package["versions"].get(version, {})
    dist = version_entry.get("dist", {})
    link = dist.get("tarball")
    return dict(ecosystem="npm", package=name, version=version,
                filename=link.rsplit("/", 1)[-1] if link else None, kind="tarball",
                original_url=link, file_utc=package["time"].get(version),
                declared_bytes=None, registry_unpacked_bytes=dist.get("unpackedSize"),
                registry_sha1=dist.get("shasum"), registry_integrity=dist.get("integrity"),
                withdrawn_or_deprecated=version_entry.get("deprecated"),
                git_head=version_entry.get("gitHead"))


def verify(content, meta):
    if meta.get("registry_integrity"):
        algorithm, expected = meta["registry_integrity"].split("-", 1)
        return base64.b64encode(hashlib.new(algorithm, content).digest()).decode() == expected
    if meta.get("registry_sha256"):
        return digest(content) == meta["registry_sha256"]
    return False


def archive_metadata(content, item):
    """Inspect labels and declared ranges without decoding conversion outputs."""
    if item["kind"] == "bdist_wheel":
        with zipfile.ZipFile(io.BytesIO(content)) as arc:
            init = arc.read("tzdata/__init__.py").decode()
            metadata = next(name for name in arc.namelist() if name.endswith(".dist-info/METADATA"))
            version_line = next(line for line in arc.read(metadata).decode().splitlines()
                                if line.startswith("Version: "))
            return dict(label=re.search(r'IANA_VERSION\s*=\s*"([^"]+)"', init)[1],
                        distribution_version=version_line.split(": ", 1)[1],
                        label_path="tzdata/__init__.py", metadata_path=metadata)
    with tarfile.open(fileobj=io.BytesIO(content), mode="r:gz") as arc:
        if item["ecosystem"] == "PyPI":
            init_name = next(name for name in arc.getnames() if name.endswith("/tzdata/__init__.py"))
            init = arc.extractfile(init_name).read().decode()
            return dict(label=re.search(r'IANA_VERSION\s*=\s*"([^"]+)"', init)[1],
                        label_path=init_name)
        metadata = json.load(arc.extractfile("package/package.json"))
        attribution = dict(distribution_version=metadata["version"], metadata_path="package/package.json",
                           moment_range=metadata.get("dependencies", {}).get("moment"))
        data_path = "package/data/packed/latest.json"
        if item["package"] == "moment-timezone":
            # The packed member declares its edition first. Do not parse or expose its zone rows here.
            prefix = arc.extractfile(data_path).read(160).decode()
            attribution.update(label=re.search(r'"version"\s*:\s*"([^"]+)"', prefix)[1],
                               label_path=data_path,
                               bundles=sorted(name for name in arc.getnames() if name.startswith("package/builds/")))
        return attribution


def choose_moment(data, end, ranges):
    # The selected historical packuments use the same one comparator caret range.
    # Fail closed on the assumption so a later dataset can be assessed explicitly.
    caret = {tuple(map(int, re.fullmatch(r"\^(\d+)\.(\d+)\.(\d+)", value).groups()))
             for value in ranges}
    candidates = []
    for version, date in data["time"].items():
        order = npm_key(version)
        if not order or time_key(date) >= end or version not in data["versions"]:
            continue
        if all(lower[0] > 0 and order[0] == lower[0] and order >= lower for lower in caret):
            candidates.append((time_key(date), order, version))
    return max(candidates)[2]


def record_file(http, out, item):
    item["acquisition"] = "listing-missing"
    if not item["original_url"]:
        return item
    content = http.get(item["original_url"])
    event = http.events[-1]
    item.update(final_url=event.get("final_url"), observed_bytes=event["bytes"],
                observed_sha256=event["sha256"], acquired_utc=event["utc"])
    if content is None:
        item.update(acquisition="GET-failed", error=event["error"])
        return item
    item["observed_sha512"] = digest(content, "sha512")
    if not verify(content, item) or (
        item.get("declared_bytes") is not None and len(content) != item["declared_bytes"]
    ):
        item.update(acquisition="registry-integrity-mismatch")
        return item
    (out / item["filename"]).write_bytes(content)
    item.update(acquisition="verified")
    try:
        item.update(archive_metadata(content, item))
    except (KeyError, StopIteration, TypeError, ValueError, zipfile.BadZipFile, tarfile.TarError) as exc:
        item["inspection_error"] = f"{type(exc).__name__}: {exc}"
    return item


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    archives = args.work / "archives"
    archives.mkdir(exist_ok=True)
    http = HttpJournal()
    deposits = {}

    def get_json(url):
        content = http.get(url)
        if content is None:
            raise RuntimeError(f"metadata GET failed: {url}")
        record = http.events[-1]
        (args.work / ("metadata-" + record["sha256"] + ".json")).write_bytes(content)
        deposits[url] = record["sha256"]
        return json.loads(content)

    window = json.loads((HERE / "fixtures.json").read_text())["window_utc"]
    start = time_key(window["start_inclusive"])
    end = time_key(window["end_exclusive"])
    pypi = get_json(PYPI)
    npm = get_json(NPM)
    rows = frame("PyPI", pypi_releases(pypi), start, end)
    rows += frame("npm", npm_releases(npm), start, end)
    files = []
    for row in rows:
        row["index_url"] = PYPI if row["ecosystem"] == "PyPI" else NPM
        if row["selection"] not in {"window", "before", "after"}:
            continue
        version = row["version"]
        if row["ecosystem"] == "PyPI":
            url = f"https://pypi.org/pypi/tzdata/{version}/json"
            package = get_json(url)
            row["release_metadata_url"] = url
            row["metadata_file_count"] = len(package["urls"])
            row["metadata_matches_project"] = package["urls"] == pypi["releases"][version]
            selected = pypi_files(package, version)
        else:
            selected = [npm_file(npm, "moment-timezone", version)]
        files.extend(record_file(http, archives, file) for file in selected)
    moment = get_json(MOMENT)
    ranges = {file["moment_range"] for file in files if file.get("moment_range")}
    version = choose_moment(moment, end, ranges)
    dependency = record_file(http, archives, npm_file(moment, "moment", version))
    dump(args.work / "catalog.json", dict(rows=rows, files=files, moment=dependency,
                                         metadata=deposits, http=http.events))
    headers = ["ecosystem", "version", "stable", "release_utc", "registry_version_entry",
               "withdrawn_or_deprecated", "selection", "index_url", "release_metadata_url",
               "metadata_file_count", "metadata_matches_project"]
    with (args.work / "release-frame.csv").open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=headers, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        if row["selection"] in {"before", "window", "after"}:
            print(row["ecosystem"], row["version"], row["release_utc"], row["selection"])
    for file in [*files, dependency]:
        print(file["filename"], file["file_utc"], file["acquisition"], file.get("label"),
              file.get("moment_range"), file.get("observed_bytes"), file.get("git_head"))


if __name__ == "__main__":
    main()
