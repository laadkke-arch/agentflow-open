"""Inputs and byte-preserving command receipts for the AF-RES-217 scripts."""

import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
PINS = json.loads((HERE / "inputs.json").read_text(encoding="utf-8"))


def utc():
    return datetime.now(timezone.utc).isoformat()


def identity(path):
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"bytes": path.stat().st_size, "sha256": digest}


def model_identity(path):
    return {
        **identity(path),
        "git_blob": subprocess.check_output(
            ["git", "hash-object", "--no-filters", str(path)], text=True
        ).strip(),
    }


def matches_model(found, pin):
    return found == {
        "bytes": pin["expected_bytes"],
        "sha256": pin["sha256"],
        "git_blob": pin["expected_git_blob"],
    }


def require_identity(path, pin):
    expected = {key: pin[key] for key in ("bytes", "sha256")}
    if identity(path) != expected:
        raise ValueError(f"byte fingerprint mismatch: {path}")
    return path


def tool(root, name):
    info = PINS["engine"]["files"][name]
    return require_identity(root / info["path"], info)


def environment(root, prefix=None):
    env = {
        "PATH": "/usr/bin:/bin",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "OMP_THREAD_LIMIT": "1",
        "LD_LIBRARY_PATH": str(root / "root/usr/lib/x86_64-linux-gnu"),
    }
    if prefix is not None:
        env["TESSDATA_PREFIX"] = str(prefix)
    return env


def capture(argv, cwd, env, stdin=None):
    argv = list(map(str, argv))
    started = utc()
    error = None
    try:
        process = subprocess.run(
            argv, cwd=cwd, env=env, input=stdin, capture_output=True, check=False, timeout=60
        )
        stdout, stderr, status = process.stdout, process.stderr, process.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, stderr, status = exc.stdout or b"", exc.stderr or b"", None
        error = "timeout after 60 seconds"
    except OSError as exc:
        stdout, stderr, status = b"", b"", None
        error = str(exc)
    return {
        "argv": argv,
        "cwd": str(cwd),
        "environment": env,
        "utc_start": started,
        "utc_end": utc(),
        "returncode": status,
        "capture_error": error,
        "stdout": stdout.decode("utf-8", "surrogateescape"),
        "stderr": stderr.decode("utf-8", "surrogateescape"),
    }


def write_jsonl(path, rows):
    with path.open("x", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=True) + "\n")


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_csv(path, rows, *, fields=None):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields or list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
