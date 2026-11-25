"""Store command, UTC timing, output streams and exit status without ambient secrets."""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def invoke(folder, name, argv, *, cwd, env=None, output=None, timeout=90):
    argv = [str(item) for item in argv]
    started = utc()
    output = output or folder / (name + ".stdout")
    error = folder / (name + ".stderr")
    try:
        with output.open("wb") as stdout, error.open("wb") as stderr:
            status = subprocess.run(argv, cwd=cwd, env=env, stdout=stdout,
                                    stderr=stderr, check=False, timeout=timeout).returncode
    except (OSError, subprocess.TimeoutExpired) as exc:
        status = 124 if isinstance(exc, subprocess.TimeoutExpired) else 127
        with error.open("a", encoding="utf-8") as stderr:
            stderr.write(str(exc) + "\n")
    entry = dict(name=name, argv=argv, cwd=str(cwd), started_utc=started, ended_utc=utc(),
                 exit=status, stdout=output.name, stdout_sha256=digest(output),
                 stderr=error.name, stderr_sha256=digest(error))
    if env is not None:
        entry["environment"] = {key: env.get(key) for key in
                                ("LC_ALL", "TZ", "SOURCE_DATE_EPOCH", "FORCE_SOURCE_DATE",
                                 "TEXMFHOME", "LD_LIBRARY_PATH")}
    with (folder / "commands.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry
