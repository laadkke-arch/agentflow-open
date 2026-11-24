"""Shared process and byte receipt for the experiment drivers."""
from datetime import datetime, timezone
from hashlib import file_digest
import json
import os
from pathlib import Path
import platform
import subprocess

from fixtures import blob, write_fixture

VERSION_LOCK = json.loads(Path(__file__).with_name("versions.json").read_text())


def file_hash(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def runtime(installation, tool, version):
    if tool == "csvkit":
        bin_dir = installation / f"csvkit-{version}" / "bin"
        version_info = subprocess.check_output([bin_dir / "csvformat", "--version"], text=True).strip()
        python = subprocess.check_output([bin_dir / "python", "-c", "import platform; print(platform.python_version())"], text=True).strip()
        expected = VERSION_LOCK["csvkit"][version]["python"]
        if version_info != f"csvformat {version}" or python != expected:
            raise ValueError(f"Expected csvkit {version} / Python {expected}, got {version_info} / {python}")
        artifacts = {"python": python, "csvkit_lock_sha256": VERSION_LOCK["csvkit"][version]["lock_sha256"]}
    else:
        bin_dir = installation / f"yq-{version}"
        binary = bin_dir / "yq_linux_amd64"
        version_info = subprocess.check_output([binary, "--version"], text=True).strip()
        sha256 = file_hash(binary)
        if not version_info.endswith(f" v{version}") or sha256 != VERSION_LOCK["yq"][version]["binary_sha256"]:
            raise ValueError(f"Unexpected yq release: {version_info}, {sha256}")
        artifacts = {"yq_binary_sha256": sha256}
    return bin_dir, {"cli_version": version_info, "os": platform.platform(), **artifacts}


def display(data):
    return {**blob(data), "text": data.decode("utf-8", errors="backslashreplace")}


class Probe:
    def __init__(self, fixture, variant, version, locale, workspace, bin_dir, runtime_info):
        self.directory = workspace / f'{fixture["id"]}_{version}_{variant}_{locale}'
        if self.directory.exists():
            raise FileExistsError(self.directory)
        write_fixture(fixture, self.directory)
        self.bin = bin_dir
        self.env = dict(os.environ, LC_ALL=locale, LANG=locale, TZ="UTC", PYTHONHASHSEED="0",
                        PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf8")
        self.row = {
            "run_id": self.directory.name, "case": fixture["case"], "fixture": fixture["id"],
            "fixture_grade": fixture["grade"], "source_id": fixture["source_id"], "source_url": fixture["source_url"],
            "version": version, "locale": locale, "variant": variant, "cwd": str(self.directory),
            "observed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "runtime": runtime_info,
            "inputs": {file: blob((self.directory / file).read_bytes()) for file in fixture["files"]},
            "commands": [],
        }
        if self.row["inputs"] != fixture["files"]:
            raise ValueError(f"Unexpected on-disk bytes: {fixture['id']}")

    def command(self, name, *args, stdin=None):
        argv = [str(self.bin / name), *args]
        receipt = {"argv": argv, "stdin": blob(stdin) if stdin is not None else None}
        try:
            result = subprocess.run(argv, cwd=self.directory, env=self.env, input=stdin if stdin is not None else b"",
                                    capture_output=True, timeout=20)
            receipt.update(status="success" if result.returncode == 0 else "failure", exit_code=result.returncode,
                           stdout=display(result.stdout), stderr=display(result.stderr))
        except subprocess.TimeoutExpired as error:
            receipt.update(status="unknown", exit_code=None, detail="timeout", stdout=display(error.stdout or b""),
                           stderr=display(error.stderr or b""))
        except OSError as error:
            receipt.update(status="unknown", exit_code=None, detail=str(error), stdout=display(b""), stderr=display(b""))
        self.row["commands"].append(receipt)
        return bytes.fromhex(receipt["stdout"]["hex"]), receipt["exit_code"]

    def finish(self, parsed):
        files = {p.name: blob(p.read_bytes()) for p in sorted(self.directory.iterdir()) if p.is_file()}
        previous = self.row["inputs"]
        self.row.update(files_after=files, changed_paths=[p for p in sorted(files.keys() | previous.keys())
                                                        if files.get(p) != previous.get(p)],
                        reinterpreted=parsed)
        statuses = {r["status"] for r in self.row["commands"]}
        self.row["execution"] = "unknown" if "unknown" in statuses else "failure" if "failure" in statuses else "success"
        print(json.dumps(self.row, ensure_ascii=False, sort_keys=True))


def options(description):
    import argparse

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("installation", type=lambda path: Path(path).resolve(), help="Directory with the locked CLI builds")
    parser.add_argument("workspace", type=lambda path: Path(path).resolve(), help="New directory for run inputs")
    opts = parser.parse_args()
    opts.workspace.mkdir(parents=True, exist_ok=False)
    return opts
