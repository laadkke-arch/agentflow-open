import argparse
import base64
import json
import os
import secrets
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import URLError
from urllib.request import ProxyHandler, Request, build_opener

from pyhanko.keys import load_cert_from_pemder

from fixtures import NAMES, fingerprint, inspect_pdf


APP = "ghcr.io/paperless-ngx/paperless-ngx@sha256:096719d7f44e5f8538ca4cf8c717d3a10d8fec699c85f494cdf94ded91bed666"
REDIS = "redis@sha256:090276da2603db19b154602c374f505d94c10ea57e9749fc3e68e955284bf0fd"
REVISION = "a7ac71971162838b8b1ee9e3b431543e69618e21"
APP_ROOT = "/usr/src/paperless"
DATA = APP_ROOT + "/data"
CONSUME = APP_ROOT + "/consume"
MEDIA = APP_ROOT + "/media"
ORIGINALS = MEDIA + "/documents/originals"
ARCHIVE = MEDIA + "/documents/archive"
PORT = "8000/tcp"
TIMEOUT = 100
SNAPSHOT = """
import json, sqlite3, sys
conn = sqlite3.connect('file:' + sys.argv[1] + '?mode=ro', uri=True, timeout=10)
conn.row_factory = sqlite3.Row
def rows(query): return [dict(row) for row in conn.execute(query)]
print(json.dumps(dict(
    docs=rows('select id, original_filename, filename, archive_filename, checksum, archive_checksum, length(content) as content_length from documents_document order by id'),
    tasks=rows("select id, task_id, task_name, status, task_args, result from django_celery_results_taskresult where task_name = 'documents.tasks.consume_file' order by id"),
)))
"""
VERSIONS = """
import importlib.metadata as m, json, sys
names = ('ocrmypdf', 'pikepdf', 'django', 'celery', 'redis', 'pillow')
print(json.dumps({'python': sys.version.split()[0], **{n: m.version(n) for n in names}}))
"""


def docker(*args, check=True):
    cmd = ("docker", *(str(arg) for arg in args))
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    if check and result.returncode:
        # Never print docker run arguments, which contain the throwaway admin credentials.
        raise RuntimeError(f"docker {args[0]} exited {result.returncode}: {result.stderr.strip()}")
    return result


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def startup_setting(setting):
    if setting == "A":
        return {"PAPERLESS_OCR_SKIP_ARCHIVE_FILE": "always"}
    if setting == "X":
        return {"PAPERLESS_OCR_USER_ARGS": '{"invalidate_digital_signatures":true}'}
    return {}


class Instance:
    def __init__(self, report_dir, setting):
        self.folder = report_dir
        self.folder.mkdir()
        self.setting = setting
        prefix = "af154-" + secrets.token_hex(5)
        self.network, self.redis, self.web = prefix + "-net", prefix + "-redis", prefix + "-web"
        self.resources = []
        self.password = secrets.token_urlsafe(24)
        self.secret_key = secrets.token_urlsafe(48)
        self.opener = build_opener(ProxyHandler({}))
        self.port = None
        self.info = {"mode": setting, "startup_setting": startup_setting(setting)}

    def command(self, *args, user="paperless", check=True):
        return docker("exec", "--user", user, self.web, *args, check=check)

    def http(self, path):
        login = base64.b64encode(("af154:" + self.password).encode()).decode()
        req = Request(
            f"http://127.0.0.1:{self.port}{path}",
            headers={"Authorization": "Basic " + login},
        )
        with self.opener.open(req, timeout=5) as response:
            headers = {
                key: response.headers[key]
                for key in ("Content-Type", "Content-Disposition")
                if key in response.headers
            }
            return response.status, headers, response.read()

    def start(self):
        started = time.monotonic()
        try:
            self._start()
        finally:
            self.info["startup_seconds"] = round(time.monotonic() - started, 3)
            write_json(self.folder / "startup.json", self.info)

    def _start(self):
        docker("network", "create", self.network)
        self.resources.append(("network", "rm", self.network))
        docker(
            "run", "--pull=never", "--platform", "linux/amd64", "-d", "--name", self.redis,
            "--network", self.network, "--network-alias", "redis", REDIS,
        )
        self.resources.append(("rm", "-fv", self.redis))
        settings = {
            "PAPERLESS_REDIS": "redis://redis:6379",
            "PAPERLESS_ADMIN_USER": "af154",
            "PAPERLESS_ADMIN_PASSWORD": self.password,
            "PAPERLESS_SECRET_KEY": self.secret_key,
            "PAPERLESS_TASK_WORKERS": "1",
            "PAPERLESS_THREADS_PER_WORKER": "1",
            **startup_setting(self.setting),
        }
        options = [arg for item in settings.items() for arg in ("--env", "=".join(item))]
        wrapper = Path(__file__).with_name("tesseract").resolve()
        result = docker(
            "run", "--pull=never", "--platform", "linux/amd64", "-d", "--name", self.web,
            "--network", self.network, "-p", "127.0.0.1::8000",
            "--mount", f"type=bind,src={wrapper},target=/usr/local/bin/tesseract,readonly",
            *options, APP,
        )
        self.resources.append(("rm", "-fv", self.web))
        self.info["container_id"] = result.stdout.strip()
        self.port = docker("port", self.web, PORT).stdout.strip().split(":")[-1]
        deadline = time.monotonic() + TIMEOUT
        last_error = "watcher has not reported readiness"
        while time.monotonic() < deadline:
            if "Using inotify to watch directory for changes:" in self.read_log("paperless"):
                try:
                    status, _, _ = self.http("/api/documents/")
                    if status == 200:
                        break
                except (URLError, TimeoutError) as e:
                    last_error = str(e)
            time.sleep(0.4)
        else:
            raise RuntimeError(f"service readiness timed out: {last_error}")
        snap = self.snapshot()
        if snap["docs"] or snap["tasks"]:
            raise RuntimeError("Instance did not initialize with empty document and consume-task tables")
        self.info["initial_db"] = snap
        self.info["redis_ping"] = docker("exec", self.redis, "redis-cli", "ping").stdout.strip()
        self.info["versions"] = json.loads(self.command("python", "-c", VERSIONS).stdout)
        binaries = self.command(
            "sh", "-c",
            "command -v tesseract && tesseract --version && tesseract --list-langs"
            " && echo Poppler && pdftotext -v && echo Ghostscript && gs --version"
            " && dpkg-query -W tesseract-ocr poppler-utils ghostscript unpaper",
        )
        (self.folder / "versions.stdout").write_text(binaries.stdout)
        (self.folder / "versions.stderr").write_text(binaries.stderr)
        self.info["engine_path"] = binaries.stdout.splitlines()[0]
        starts = [line for line in self.trace().splitlines() if "\tstart\tprobe\t" in line]
        self.info["probe_count"] = len(starts)
        if self.info["engine_path"] != "/usr/local/bin/tesseract" or len(starts) < 2:
            raise RuntimeError("Engine process observation preflight failed")

    def snapshot(self):
        return json.loads(self.command("python", "-c", SNAPSHOT, f"{DATA}/db.sqlite3").stdout)

    def read_log(self, name):
        return self.command("cat", f"{DATA}/log/{name}.log", check=False).stdout

    def trace(self):
        return self.command("cat", f"{DATA}/af154-tesseract.tsv", check=False).stdout

    def close(self):
        if self.resources and self.resources[-1][-1] == self.web:
            logs = docker("logs", "--timestamps", self.web, check=False)
            (self.folder / "container.stdout").write_text(logs.stdout)
            (self.folder / "container.stderr").write_text(logs.stderr)
        removes = []
        for args in reversed(self.resources):
            result = docker(*args, check=False)
            removes.append({"argv": result.args, "exit_code": result.returncode, "stderr": result.stderr})
        write_json(self.folder / "cleanup.json", removes)

    def file_receipt(self, path):
        exists = self.command("test", "-f", path, check=False).returncode
        if exists == 1:
            return {"exists": False, "path": path}
        if exists:
            raise RuntimeError(f"test -f exited {exists}: {path}")
        sha = self.command("sha256sum", path).stdout.split()[0]
        info = self.command("stat", "-c", "%s\t%a\t%u\t%g\t%Y", path).stdout.strip().split("\t")
        return dict(exists=True, path=path, sha256=sha, bytes=int(info[0]),
                    mode=info[1], uid=int(info[2]), gid=int(info[3]), mtime_epoch=int(info[4]))

    def original_paths(self):
        return self.command("find", ORIGINALS, "-maxdepth", "2", "-type", "f").stdout.splitlines()

    def set_original_permissions(self, mode):
        self.command("chmod", mode, ORIGINALS, user="0")
        return {
            "directory": ORIGINALS,
            "mode": self.command("stat", "-c", "%a", ORIGINALS).stdout.strip(),
            "writable_test_exit": self.command("test", "-w", ORIGINALS, check=False).returncode,
        }

    def wait_result(self, old_ids, source_name):
        deadline = time.monotonic() + TIMEOUT
        while time.monotonic() < deadline:
            snap = self.snapshot()
            matches = [
                row for row in snap["tasks"]
                if row["task_id"] not in old_ids
                and row["status"] in {"SUCCESS", "FAILURE"}
                and source_name in (row["task_args"] or "") + (row["result"] or "")
            ]
            if len(matches) == 1:
                return matches[0], snap
            if matches:
                raise RuntimeError(f"Ambiguous queue receipt for {source_name}")
            time.sleep(0.2)
        raise RuntimeError(f"No terminal Celery result for {source_name}")

    def download(self, doc_id, kind, folder, source, root, moment):
        suffix = "?original=true" if kind == "original" else ""
        path = f"/api/documents/{doc_id}/download/{suffix}"
        started = time.monotonic()
        status, headers, data = self.http(path)
        transport_seconds = round(time.monotonic() - started, 4)
        target = folder / f"{kind}.pdf"
        target.write_bytes(data)
        verify = inspect_pdf(target, root, moment)
        return {
            "route": path,
            "status": status,
            "headers": headers,
            "download_seconds": transport_seconds,
            "verify_seconds": round(time.monotonic() - started - transport_seconds, 4),
            "bytes_equal": data == source.read_bytes(),
            **verify,
        }

    def run(self, run_id, source, root, moment, preflight):
        folder = self.folder / run_id
        folder.mkdir()
        incoming = f"{run_id.lower()}-{source.name}"
        target = f"{CONSUME}/{incoming}"
        staging = f"{CONSUME}/.{incoming}.tmp"
        before = self.snapshot()
        previous_ids = {row["task_id"] for row in before["tasks"]}
        before_logs = {name: self.read_log(name) for name in ("paperless", "celery")}
        before_trace = self.trace()
        started = time.monotonic()
        docker("cp", source, f"{self.web}:{staging}")
        self.command("chown", "paperless:paperless", staging, user="0")
        self.command("chmod", "0644", staging)
        provided = self.file_receipt(staging)
        input_bytes = fingerprint(source.read_bytes())
        if provided["sha256"] != input_bytes["sha256"] or provided["bytes"] != input_bytes["bytes"]:
            raise RuntimeError(f"Staged bytes differ for {run_id}")
        stage_seconds = round(time.monotonic() - started, 4)
        moved_utc = datetime.now(UTC).isoformat()
        started = time.monotonic()
        self.command("mv", staging, target)
        task, after = self.wait_result(previous_ids, incoming)
        process_seconds = round(time.monotonic() - started, 4)
        logs = {}
        for name, prefix in before_logs.items():
            current = self.read_log(name)
            if not current.startswith(prefix):
                raise RuntimeError(f"{name} log coverage lost for {run_id}")
            logs[name] = current[len(prefix):]
            (folder / f"{name}.log").write_text(logs[name])
        current_trace = self.trace()
        if not current_trace.startswith(before_trace):
            raise RuntimeError(f"Engine journal coverage lost for {run_id}")
        trace = current_trace[len(before_trace):]
        (folder / "tesseract.tsv").write_text(trace)
        events = [line.split("\t", 4) for line in trace.splitlines()]
        wrapper = [line for line in logs["paperless"].splitlines() if "Calling OCRmyPDF with args:" in line]
        skipped = "skipping OCRmyPDF entirely." in logs["paperless"]
        terminal_line = [
            line for line in logs["celery"].splitlines()
            if task["task_id"] in line and ("raised unexpected" in line or "succeeded in" in line)
        ]
        doc_count = len(after["docs"])
        doc_delta = doc_count - len(before["docs"])
        stored = None
        downloads = {}
        if task["status"] == "SUCCESS":
            doc, = [row for row in after["docs"] if row["original_filename"] == incoming]
            if doc_delta != 1:
                raise RuntimeError(f"Success did not add one document for {run_id}")
            original = self.file_receipt(f"{ORIGINALS}/{doc['filename']}")
            archive = self.file_receipt(f"{ARCHIVE}/{doc['archive_filename']}") if doc["archive_filename"] else None
            api_status, _, raw_doc = self.http(f"/api/documents/{doc['id']}/")
            stored = {
                "row": doc, "original": original, "archive": archive,
                "api_document_status": api_status, "api_indexed_text": json.loads(raw_doc)["content"],
            }
            for kind in ("original", "default"):
                downloads[kind] = self.download(doc["id"], kind, folder, source, root, moment)
        outcome = {
            "run_id": run_id, "status": task["status"].lower(), "input": input_bytes,
            "preflight": preflight, "source_name": source.name, "consume_file": incoming,
            "queued_log": f"Adding {target} to the task queue." in logs["paperless"],
            "stage_seconds": stage_seconds, "moved_utc": moved_utc,
            "process_seconds_to_task_terminal_including_poll": process_seconds,
            "consume_path_after": self.file_receipt(target),
            "provider_path_after": fingerprint(source.read_bytes()),
            "staged_file": provided,
            "task": task, "celery_terminal_lines": terminal_line,
            "db_count_before": len(before["docs"]), "db_count_after": doc_count, "db_delta": doc_delta,
            "stored": stored,
            "wrapper": {"count": len(wrapper), "calls": wrapper, "early_return_log": skipped},
            "engine": {
                "process_starts": {
                    kind: sum(e[2] == "start" and e[3] == kind for e in events)
                    for kind in ("probe", "orientation", "recognition", "other")
                },
                "process_exit_zero": {
                    kind: sum(e[2] == "exit" and e[3] == kind and e[4] == "0" for e in events)
                    for kind in ("probe", "orientation", "recognition", "other")
                },
                "observation_preflight_passed": True,
            },
            "pdfa_log": [
                line for line in logs["paperless"].splitlines() if "Output file is a PDF/A" in line
            ] + [
                line for line in logs["celery"].splitlines() if "Output file is a PDF/A" in line
            ],
            "downloads": downloads,
        }
        write_json(folder / "receipt.json", outcome)
        return outcome

    def retry_probe(self, prefix, input_dir, root, moment):
        source = input_dir / NAMES["WT"]
        prior = self.original_paths()
        mode = self.command("stat", "-c", "%a", ORIGINALS).stdout.strip()
        denied = self.set_original_permissions("a-w")
        if denied["writable_test_exit"] != 1:
            raise RuntimeError("Originals directory is still writable to the application")
        try:
            failed = self.run(prefix + "-W", source, root, moment, denied)
            after_failed = self.original_paths()
        finally:
            restored = self.set_original_permissions(mode)
        if restored["writable_test_exit"] != 0:
            raise RuntimeError("Originals directory did not become writable")
        retry = self.run(prefix + "-R", source, root, moment, restored)
        duplicate = self.run(prefix + "-DUP", source, root, moment, restored)
        write_json(self.folder / "write-retry.json", {
            "directory_before": prior, "directory_after_failure": after_failed,
            "directory_after_retry_and_duplicate": self.original_paths(),
            "still_present_failed_intake_after_retry": self.file_receipt(
                f"{CONSUME}/{failed['consume_file']}"
            ),
            "ids": [failed["run_id"], retry["run_id"], duplicate["run_id"]],
        })
        return failed, retry, duplicate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).with_name("fixtures"))
    parser.add_argument("--phase", choices=("matrix", "controls", "full"), default="full")
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    inputs = args.fixtures.resolve()
    root = load_cert_from_pemder(str(inputs / "qa-root.pem"))
    moment = datetime.fromisoformat((inputs / "validation-time.txt").read_text().strip())
    image_meta = {}
    for image in (APP, REDIS):
        result = docker("image", "inspect", "--format", "{{.Id}} {{.Os}}/{{.Architecture}}", image)
        image_meta[image] = result.stdout.strip()
    revision = docker("image", "inspect", "--format",
                      '{{index .Config.Labels "org.opencontainers.image.revision"}}', APP).stdout.strip()
    if revision != REVISION:
        raise RuntimeError("Image source revision mismatch")
    version = docker("version", "--format", "{{.Client.Version}} / {{.Server.Version}}").stdout.strip()
    write_json(out / "platform.json", {
        "images": image_meta, "source_revision": revision, "docker_client_server": version,
        "host": list(os.uname())[:1] + list(os.uname())[2:],
        "verification_time": moment.isoformat(),
        "fixtures": {key: fingerprint((inputs / name).read_bytes()) for key, name in NAMES.items()},
    })
    groups = []
    if args.phase in {"matrix", "full"}:
        groups.extend((f"R{n}-{mode}", mode, ("UT", "UI", "ST", "SI"))
                      for n in (1, 2) for mode in ("D", "A"))
    if args.phase in {"controls", "full"}:
        groups.append(("S1-X", "X", ("SI",)))
    errors = []
    for group, setting, fixtures in groups:
        instance = Instance(out / group, setting)
        print(f"{group} starting", flush=True)
        try:
            instance.start()
            for fixture in fixtures:
                row = instance.run(f"{group}-{fixture}", inputs / NAMES[fixture], root, moment, None)
                print(f"{row['run_id']} {row['status']}", flush=True)
            if setting == "A" and args.phase == "full":
                for row in instance.retry_probe(group, inputs, root, moment):
                    print(f"{row['run_id']} {row['status']}", flush=True)
        except (OSError, URLError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
            errors.append({"group": group, "error": str(error)})
            print(f"{group} harness error: {error}", flush=True)
        finally:
            instance.close()
    write_json(out / "harness-errors.json", errors)
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
