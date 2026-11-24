"""Fetch pinned wheels and replay the fixed AF-RES-229 HTML-index experiment."""

import argparse
from contextlib import contextmanager
import email
import hashlib
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, HTTPServer
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from threading import Thread
from datetime import datetime, timezone
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "inputs.json"
LOCAL_PROJECT = "/simple/pytest/"
WHEEL_PREFIX = "/files/"
HTML_CONTENT_TYPE = "text/html; charset=utf-8"
MAIN_VARIANTS = ("baseline", "unmarked")
CONTROL_VARIANTS = ("empty", "missing")
VARIANTS = (*MAIN_VARIANTS, *CONTROL_VARIANTS)
INVENTORY = """import importlib.metadata, json, platform, sys
print(json.dumps({
    "python": platform.python_version(),
    "is_venv": sys.prefix != sys.base_prefix,
    "packages": {d.metadata["Name"].lower(): d.version for d in importlib.metadata.distributions()},
}, sort_keys=True))
"""


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, data):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, indent=2, ensure_ascii=False)
        stream.write("\n")


def read_json(path):
    return json.loads(path.read_bytes())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def wheel_fingerprint(item, data):
    name = item["filename"]
    require(len(data) == item["size_bytes"], f"{name}: size mismatch")
    sha = digest(data)
    require(sha == item["sha256"], f"{name}: SHA-256 mismatch")

    dist_info = f"{item['name']}-{item['version']}.dist-info"
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        metadata = archive.read(f"{dist_info}/METADATA")
        wheel = archive.read(f"{dist_info}/WHEEL")
    pkg = email.message_from_bytes(metadata)
    build = email.message_from_bytes(wheel)
    require(pkg["Name"].lower() == item["name"], f"{name}: METADATA Name mismatch")
    require(pkg["Version"] == item["version"], f"{name}: METADATA Version mismatch")
    require(pkg["Requires-Python"] == item["requires_python"], f"{name}: Requires-Python mismatch")
    require(build.get_all("Tag") == item["tags"], f"{name}: WHEEL Tag mismatch")
    require(name.endswith("-" + "-".join(item["tags"]) + ".whl"), f"{name}: filename Tag mismatch")
    return {
        "filename": name,
        "size_bytes": len(data),
        "sha256": sha,
        "metadata": {
            "path": f"{dist_info}/METADATA",
            "sha256": digest(metadata),
            "metadata_version": pkg["Metadata-Version"],
            "name": pkg["Name"],
            "version": pkg["Version"],
            "requires_python": pkg["Requires-Python"],
        },
        "wheel": {
            "path": f"{dist_info}/WHEEL",
            "sha256": digest(wheel),
            "wheel_version": build["Wheel-Version"],
            "root_is_purelib": build["Root-Is-Purelib"],
            "generator": build["Generator"],
            "tags": build.get_all("Tag"),
        },
    }


def fetch_wheels(inputs, wheelhouse, receipt_path):
    wheelhouse.mkdir(parents=True)
    require(not receipt_path.exists(), "fetch receipt already exists")
    rows = []
    for item in (inputs["pip"], *inputs["wheels"]):
        url = item["url"]
        record = {"url": url, "started_utc": utc()}
        rows.append(record)
        try:
            location = urlsplit(url)
            require(
                location.scheme == "https" and location.netloc == "files.pythonhosted.org"
                and location.path.endswith("/" + item["filename"]) and not location.query
                and not location.fragment,
                "unexpected wheel origin",
            )
            request = Request(url, headers={"User-Agent": "AF-RES-229 pinned wheel fetch"})
            with urlopen(request, timeout=30) as response:
                record.update(final_url=response.url, http_status=response.status, headers={
                    key: response.headers[key] for key in (
                        "Date", "Content-Type", "Content-Length", "ETag", "Last-Modified",
                    ) if key in response.headers
                })
                require(response.url == url and response.status == 200, "unexpected HTTP result")
                data = response.read(item["size_bytes"] + 1)
            record.update(wheel_fingerprint(item, data))
            file = wheelhouse / item["filename"]
            file.write_bytes(data)
            file.chmod(0o444)
            record["status"] = "verified"
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
            record.update(status="failed", error=f"{type(error).__name__}: {error}")
        record["finished_utc"] = utc()
    dump(receipt_path, {"inputs_sha256": digest(INPUTS.read_bytes()), "wheels": rows})
    return all(row["status"] == "verified" for row in rows)


class Anchors(HTMLParser):
    def __init__(self, raw):
        super().__init__()
        self.items = []
        self.feed(raw.decode("utf-8"))
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.items.append(dict(attrs))


def read_fixtures(inputs):
    require(
        inputs["project"] == "pytest" and len(inputs["wheels"]) == 3
        and inputs["wheels"][-1]["version"] == inputs["max_version"],
        "unexpected artifact inventory",
    )
    pages = {kind: (ROOT / "index" / f"{kind}.html").read_bytes() for kind in VARIANTS}
    baseline = pages["baseline"]
    target = next(item for item in inputs["wheels"] if item["version"] == inputs["target_version"])
    marker = f' data-yanked="{target["version_json"]["yanked_reason"]}"'.encode()
    target_anchor = [
        line for line in baseline.splitlines(keepends=True)
        if line.startswith(f'<a href="/files/{target["filename"]}#'.encode())
    ]
    require(len(target_anchor) == 1 and baseline.count(marker) == 1, "invalid baseline marker")
    expected_variants = {
        "unmarked": baseline.replace(marker, b"", 1),
        "empty": baseline.replace(marker, b' data-yanked=""', 1),
        "missing": baseline.replace(target_anchor[0], b"", 1),
    }
    for kind, expected in expected_variants.items():
        require(pages[kind] == expected, f"{kind}: page differs beyond intended change")

    anchors = Anchors(baseline).items
    require(len(anchors) == len(inputs["wheels"]), "baseline anchor count")
    for anchor, item in zip(anchors, inputs["wheels"]):
        expected = {
            "href": f'{WHEEL_PREFIX}{item["filename"]}#sha256={item["sha256"]}',
            "data-requires-python": item["requires_python"],
        }
        if item["version_json"]["yanked"]:
            expected["data-yanked"] = item["version_json"]["yanked_reason"]
        require(anchor == expected, f'baseline anchor mismatch: {item["filename"]}')
    root_page = (ROOT / "index/root.html").read_bytes()
    require(Anchors(root_page).items == [{"href": "pytest/"}], "unexpected Simple project list")
    return pages, root_page


class ReadOnlyIndex(BaseHTTPRequestHandler):
    def do_GET(self):
        self.serve_resource(send_body=True)

    def do_HEAD(self):
        self.serve_resource(send_body=False)

    def log_message(self, *_):
        pass

    def serve_resource(self, send_body):
        resources = self.server.resources
        if self.path == LOCAL_PROJECT:
            resource = (HTML_CONTENT_TYPE, self.server.page)
        else:
            resource = resources.get(self.path)

        if resource is None:
            content_type, body, status = "text/plain", b"", 404
        else:
            content_type, body = resource
            status = 200
        observed = {
            "utc": utc(), "method": self.command, "path": self.path,
            "host": self.headers.get("Host"), "accept": self.headers.get("Accept"),
            "range": self.headers.get("Range"), "status": status,
            "content_type": content_type, "content_length": len(body),
            "representation_sha256": digest(body), "body_bytes_sent": None,
        }
        self.server.events.append(observed)
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if send_body:
            self.wfile.write(body)
        observed["body_bytes_sent"] = len(body) if send_body else 0


@contextmanager
def serve(wheels, root_page):
    with HTTPServer(("127.0.0.1", 0), ReadOnlyIndex) as server:
        server.resources = {
            "/simple/": (HTML_CONTENT_TYPE, root_page),
            **{WHEEL_PREFIX + name: ("application/octet-stream", data) for name, data in wheels.items()},
        }
        thread = Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
        thread.start()
        try:
            yield server
        finally:
            server.shutdown()
            thread.join()


def command(argv, env, cwd):
    started = utc()
    try:
        result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, timeout=60)
        out, err = result.stdout, result.stderr
        code, timed_out = result.returncode, False
    except subprocess.TimeoutExpired as error:
        out, err = error.stdout or b"", error.stderr or b""
        code, timed_out = None, True
    return {
        "argv": argv, "started_utc": started, "finished_utc": utc(),
        "exit_code": code, "timed_out": timed_out,
        "stdout_sha256": digest(out), "stderr_sha256": digest(err),
    }, out, err


def clean_env(case_path):
    profile = {}
    if os.name == "nt":
        profile["USERPROFILE"] = str(case_path)
        profile["SYSTEMROOT"] = os.environ["SYSTEMROOT"]
    else:
        profile["HOME"] = str(case_path)
    return {
        **profile, "PATH": os.defpath, "TMPDIR": str(case_path), "TEMP": str(case_path),
        "TMP": str(case_path), "LC_ALL": "C.UTF-8", "TZ": "UTC", "PYTHONIOENCODING": "utf-8",
        "PYTHONNOUSERSITE": "1", "PIP_CONFIG_FILE": os.devnull, "NO_PROXY": "127.0.0.1",
    }


def case_plan(inputs, group):
    cases = []
    if group in ("main", "all"):
        for repeat, order in enumerate((MAIN_VARIANTS, MAIN_VARIANTS[::-1]), 1):
            for request_id, requirement in inputs["requests"].items():
                cases.extend(("main", request_id, requirement, variant, repeat) for variant in order)
    if group in ("controls", "all"):
        cases.extend(("controls", "pin-target", inputs["requests"]["pin-target"], variant, 1)
                     for variant in CONTROL_VARIANTS)
    return cases


def execute_case(case, out, server, pages, inputs, pip_wheel, temp):
    group, request_id, requirement, variant, repeat = case
    run_id = f"{request_id}-{variant}-r{repeat}"
    receipt = out / run_id
    receipt.mkdir()
    work = temp / run_id
    work.mkdir()
    env = clean_env(work)
    venv = work / "venv"
    venv_python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    pip = [str(venv_python), "-m", "pip", "--disable-pip-version-check", "--no-input", "--no-color"]
    index = f"http://127.0.0.1:{server.server_port}/simple/"
    report = receipt / "report.json"
    server.page, server.events = pages[variant], []
    record = {
        "run_id": run_id, "group": group, "request_id": request_id,
        "requirement": requirement, "variant": variant, "repeat": repeat,
        "index_url": index, "index_sha256": digest(server.page),
        "environment": env, "working_directory": str(work), "preflight": {},
    }
    setup = record["preflight"]

    def stage(key, argv):
        details, out_bytes, err_bytes = command(argv, env, work)
        setup[key] = {
            **details, "stdout": out_bytes.decode("utf-8", errors="replace"),
            "stderr": err_bytes.decode("utf-8", errors="replace"),
        }
        require(details["exit_code"] == 0, f"{key} failed")
        return out_bytes

    expected = {"python": inputs["python_version"], "is_venv": True, "packages": {"pip": inputs["pip"]["version"]}}
    try:
        stage("new_venv", [sys.executable, "-m", "venv", str(venv)])
        stage("bootstrap", [
            *pip, "install", "--no-index", "--no-deps", "--no-cache-dir",
            "--force-reinstall", "--progress-bar", "off", str(pip_wheel),
        ])
        stage("pip_version", [*pip, "--version"])
        inventory = [str(venv_python), "-c", INVENTORY]
        before = json.loads(stage("inventory_before", inventory))
        require(before == expected, "unexpected initial environment")
        argv = [
            *pip, "install", "--dry-run", "--ignore-installed", "--no-deps",
            "--only-binary=:all:", "--no-cache-dir", "--report", str(report),
            "--index-url", index, "--retries", "0", "--timeout", "10",
            "--progress-bar", "off", requirement,
        ]
        details, stdout, stderr = command(argv, env, work)
        (receipt / "stdout.txt").write_bytes(stdout)
        (receipt / "stderr.txt").write_bytes(stderr)
        record["resolver"] = details
        after = json.loads(stage("inventory_after", inventory))
        require(after == before, "installed distribution inventory changed in dry run")
        record["status"] = "timed_out" if details["timed_out"] else "observed"
    except (OSError, ValueError) as error:
        record.update(status="environment_error", error=f"{type(error).__name__}: {error}")
    if report.exists():
        record["report_sha256"] = digest(report.read_bytes())
    with (receipt / "http.jsonl").open("x", encoding="utf-8") as stream:
        for event in server.events:
            stream.write(json.dumps(event, ensure_ascii=False) + "\n")
    dump(receipt / "run.json", record)
    print(f'{run_id} {record["status"]} exit={record.get("resolver", {}).get("exit_code")}', flush=True)
    return record


def run_suite(inputs, wheelhouse, out, group):
    require(platform.python_version() == inputs["python_version"], "use the pinned Python version")
    pages, root_page = read_fixtures(inputs)
    pip_wheel = wheelhouse / inputs["pip"]["filename"]
    wheel_fingerprint(inputs["pip"], pip_wheel.read_bytes())
    wheels = {}
    for item in inputs["wheels"]:
        data = (wheelhouse / item["filename"]).read_bytes()
        wheel_fingerprint(item, data)
        wheels[item["filename"]] = data

    out.mkdir(parents=True)
    started = utc()
    with tempfile.TemporaryDirectory(prefix="af229-venvs-") as directory, serve(wheels, root_page) as server:
        observations = [
            execute_case(case, out, server, pages, inputs, pip_wheel, Path(directory))
            for case in case_plan(inputs, group)
        ]
    dump(out / "suite.json", {
        "group": group, "started_utc": started, "finished_utc": utc(),
        "python": platform.python_version(), "platform": platform.platform(),
        "compiler": platform.python_compiler(), "architecture": platform.machine(),
        "inputs_sha256": digest(INPUTS.read_bytes()), "runner_sha256": digest(Path(__file__).read_bytes()),
        "pip_wheel_sha256": inputs["pip"]["sha256"],
        "project_page_sha256": {key: digest(page) for key, page in pages.items()},
        "wheel_sha256": {key: digest(data) for key, data in wheels.items()},
        "planned": len(case_plan(inputs, group)), "run_ids": [record["run_id"] for record in observations],
        "execution_errors": [record["run_id"] for record in observations if record["status"] != "observed"],
    })
    return all(record["status"] == "observed" for record in observations)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    operations = parser.add_subparsers(dest="operation", required=True)
    fetch = operations.add_parser("fetch", help="download and verify the four pinned public wheels")
    fetch.add_argument("--wheelhouse", type=Path, required=True)
    fetch.add_argument("--receipt", type=Path, required=True)
    replay = operations.add_parser("run", help="run only against the local read-only HTML index")
    replay.add_argument("--wheelhouse", type=Path, required=True)
    replay.add_argument("--out", type=Path, required=True)
    replay.add_argument("--group", choices=("main", "controls", "all"), required=True)
    args = parser.parse_args()
    inputs = read_json(INPUTS)
    require(inputs["schema"] == 1, "unsupported inputs schema")
    wheelhouse = args.wheelhouse.resolve()
    if args.operation == "fetch":
        passed = fetch_wheels(inputs, wheelhouse, args.receipt.resolve())
    else:
        passed = run_suite(inputs, wheelhouse, args.out.resolve(), args.group)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
