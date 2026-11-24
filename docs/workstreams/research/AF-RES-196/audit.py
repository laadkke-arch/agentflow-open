"""Run the frozen citation-recovery comparison in isolated Linux workers."""
import argparse
import base64
import csv
import ctypes
import errno
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from make_bundles import github_pointer, json_bytes, mirror_key, read_json, sha256, verify_mirror, window_sha256

HERE = Path(__file__).resolve()
CACHED_PATTERNS = (
    re.compile(r"시험 주체 (?P<subject>\S+)의 (?P<date>\S+) EARL 단언은 \S+ 결과를 \S+로 보고했다\."),
    re.compile(r"(?P<subject>\S+)는 (?P<date>\S+)에 \S+에서 \S+를 반환했다\."),
)


def now():
    return datetime.now(timezone.utc).isoformat()


def lock_worker():
    """After input descriptors are opened, allow computation and descriptor I/O only."""
    libc = ctypes.CDLL("libseccomp.so.2")
    libc.seccomp_init.argtypes = [ctypes.c_uint32]
    libc.seccomp_init.restype = ctypes.c_void_p
    libc.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
    libc.seccomp_rule_add.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint]
    libc.seccomp_load.argtypes = [ctypes.c_void_p]
    libc.seccomp_release.argtypes = [ctypes.c_void_p]
    context = libc.seccomp_init(0x00050000 | errno.EPERM)
    if not context:
        raise RuntimeError("seccomp_init failed")
    try:
        for name in (
            "read", "write", "writev", "close", "lseek", "fstat", "getpid", "gettid",
            "brk", "mmap", "munmap", "mprotect", "mremap", "madvise", "futex",
            "getrandom", "clock_gettime", "gettimeofday", "rt_sigaction", "rt_sigprocmask",
            "rt_sigreturn", "sigaltstack", "exit", "exit_group",
        ):
            syscall = libc.seccomp_syscall_resolve_name(name.encode("ascii"))
            if syscall < 0 or libc.seccomp_rule_add(context, 0x7FFF0000, syscall, 0):
                raise RuntimeError(f"cannot install seccomp rule for {name}")
        result = libc.seccomp_load(context)
        if result:
            raise RuntimeError(f"seccomp_load failed: {result}")
    finally:
        libc.seccomp_release(context)


def blocked(operation):
    try:
        operation()
    except OSError as exc:
        if exc.errno == errno.EPERM:
            return "EPERM"
        raise
    raise RuntimeError("offline isolation probe unexpectedly succeeded")


class StagedFiles:
    def __init__(self, root):
        self.handles = {}
        self.reads = []
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                raise ValueError("unexpected symlink in trial")
            if path.is_file():
                key = path.relative_to(root).as_posix()
                if key != "bundle.json" and not key.startswith("mirror/"):
                    raise ValueError(f"unexpected file in trial: {key}")
                self.handles[key] = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)

    def read(self, path, role):
        if path not in self.handles:
            self.reads.append({"path": path, "role": role, "status": "missing"})
            return None
        fd = self.handles[path]
        os.lseek(fd, 0, os.SEEK_SET)
        data = b"".join(iter(lambda: os.read(fd, 65536), b""))
        self.reads.append({"path": path, "role": role, "status": "read",
                           "bytes": len(data), "sha256": sha256(data)})
        return data


def build_window(raw, ranges):
    lines = raw.splitlines(keepends=True)
    locator, parts = [], []
    for first, last in ranges:
        if not 1 <= first <= last <= len(lines):
            raise ValueError("line range outside the source")
        start = sum(map(len, lines[:first - 1]))
        part = b"".join(lines[first - 1:last])
        locator.append({"first_line": first, "last_line": last, "start_byte": start, "end_byte": start + len(part)})
        parts.append(part)
    return locator, parts


def receipt_ranges(raw):
    lines = raw.splitlines()

    def find(prefix, start=0):
        return next(i for i in range(start, len(lines)) if lines[i].startswith(prefix))

    first = find(b'  "run_id": ')
    event = find(b'  "event_id": ', first)
    started = find(b'  "started_utc": ')
    observation = find(b'  "observation": {')
    actual = find(b'    "actual": {', observation)
    end_actual = find(b'    }', actual + 1)
    return [[first + 1, event + 1], [started + 1, started + 1], [actual + 1, end_actual + 1]]


def unpack_excerpt(bundle):
    locator = bundle["locator"]
    parts = [base64.b64decode(part, validate=True) for part in bundle["excerpt_base64"]]
    if not locator or len(parts) != len(locator):
        raise ValueError("missing excerpt or locator")
    previous_line, previous_end = 0, 0
    for loc, part in zip(locator, parts, strict=True):
        first, last = loc["first_line"], loc["last_line"]
        start, end = loc["start_byte"], loc["end_byte"]
        if (not previous_line < first <= last or start < previous_end or end != start + len(part)
                or len(part.splitlines()) != last - first + 1):
            raise ValueError("invalid excerpt boundaries")
        previous_line, previous_end = last, end
    return locator, parts


def source_fields(kind, parts):
    if kind == "historical":
        assertion, = parts
        text = assertion.decode()
        patterns = {
            "subject": r"#subject> <([^>]+)>",
            "reference_date": r'dc:date "([^"]+)"',
            "value": r"#outcome> <http://www.w3.org/ns/earl#([^>]+)>",
            "event": r"#test> <([^>]+)>",
            "assertor": r"#assertedBy> <([^>]+)>",
        }
        result = {}
        for field, pattern in patterns.items():
            found = re.findall(pattern, text)
            if len(found) != 1:
                raise ValueError(f"expected one EARL {field}")
            result[field] = found[0]
        return result

    def members(window):
        return json.loads(b"{" + window.strip().removesuffix(b",") + b"}")

    identity, time, observation = map(members, parts)
    return {"subject": identity["engine"], "reference_date": time["started_utc"],
            "value": observation["actual"]["value"], "event": identity["run_id"], "assertor": None}


def cached_fields(sentence):
    if sentence:
        for pattern in CACHED_PATTERNS:
            match = pattern.fullmatch(sentence)
            if match:
                return {"subject": match["subject"], "reference_date": match["date"]}
    return {}


def recover(bundle, staged, control=""):
    pointer = github_pointer(bundle["url"])
    kind = "historical" if pointer["path"].endswith(".ttl") else "new"
    if "excerpt_sha256" in bundle:
        if (bundle["revision"], bundle["relative_path"], bundle["type"]) != (
                pointer["revision"], pointer["path"], kind):
            raise ValueError("bundle metadata conflicts with the published pointer")
    result = {"sentence": bundle.get("sentence"), "cached_fields": cached_fields(bundle.get("sentence")),
              "pointer": pointer, "source_fields": {}, "source_mode": None, "source_status": "missing",
              "hash_status": "not_compared", "stored_sha256": bundle.get("excerpt_sha256"),
              "observed_sha256": None, "locator": None, "excerpt_reads": 0}
    try:
        if "excerpt_base64" in bundle:
            result["source_mode"] = "package_excerpt"
            locator, parts = unpack_excerpt(bundle)
            result["excerpt_reads"] = 1
        else:
            requested = f"mirror/{mirror_key(pointer)}"
            raw = staged.read(requested, "source")
            if raw is None:
                return result
            result["source_mode"] = "mirror_file"
            ranges = pointer["line_ranges"] if kind == "historical" else receipt_ranges(raw)
            locator, parts = build_window(raw, ranges)
        line_ranges = [[loc["first_line"], loc["last_line"]] for loc in locator]
        if pointer["line_ranges"] and line_ranges != pointer["line_ranges"]:
            raise ValueError("excerpt locator conflicts with the link")
        result["locator"] = locator
        result["pointer"] = {**pointer, "line_ranges": line_ranges}
        actual_hash = window_sha256(parts)
        result["observed_sha256"] = actual_hash
        expected_hash = result["stored_sha256"]
        if expected_hash and expected_hash != actual_hash:
            result.update(source_status="hash_mismatch", hash_status="mismatch")
            return result
        result["hash_status"] = "match" if expected_hash else "no_stored_hash"
        result["source_fields"] = source_fields(kind, parts)
        result["source_status"] = "reopened"
    except (ValueError, KeyError, StopIteration) as exc:
        result["source_status"] = "unreadable"
        result["error"] = str(exc)
    return result


def worker(control):
    root = Path.cwd()
    staged = StagedFiles(root)
    lock_worker()
    guards = {"new_file": blocked(lambda: os.open(HERE, os.O_RDONLY)),
              "new_socket": blocked(lambda: socket.socket(socket.AF_INET, socket.SOCK_STREAM))}
    raw_bundle = staged.read("bundle.json", "bundle")
    result = recover(json.loads(raw_bundle), staged, control)
    result.update({"read_log": staged.reads, "guard": guards, "preopened_files": len(staged.handles),
                   "staged_mirror_files": len(staged.handles) - 1, "worker_exit_code": 0})
    sys.stdout.buffer.write(json_bytes(result))


def mark(observed, expected):
    if observed is None:
        return "unconfirmed"
    return "match" if observed == expected else "wrong"


def score(result, case):
    pointer = result["pointer"]
    source = result["source_fields"]
    best = {**source, **result["cached_fields"]}
    ranges = [[loc["first_line"], loc["last_line"]] for loc in case["locator"]]
    actual = result["source_status"] == "reopened"
    states = {
        "sentence": mark(result["sentence"], case["sentence"]),
        "subject": mark(best.get("subject"), case["subject"]),
        "reference_date": mark(best.get("reference_date"), case["reference_date"]),
        "file_pointer": mark(mirror_key(pointer), case["mirror_key"]),
        "citation_location": mark(pointer["line_ranges"] or None, ranges),
        "source_subject": mark(source.get("subject"), case["subject"]),
        "source_date": mark(source.get("reference_date"), case["reference_date"]),
        "source_value": mark(source.get("value"), case["source_value"]),
        "source_event": mark(source.get("event"), case["event"]),
        "original_window": mark(result["observed_sha256"], case["excerpt_sha256"]) if actual else "unconfirmed",
    }
    wrong = [key for key, value in states.items() if value == "wrong"]
    held = [key for key, value in states.items() if value == "unconfirmed"]
    return {**states, "outcome": "wrong" if wrong else "withheld" if held else "recovered",
            "wrong_fields": "|".join(wrong), "withheld_fields": "|".join(held)}


def execute_trial(bundle, mirror, control=""):
    with tempfile.TemporaryDirectory(prefix="af-res-196-trial-") as tmp:
        stage = Path(tmp)
        (stage / "bundle.json").write_bytes(bundle)
        if mirror is not None:
            shutil.copytree(mirror, stage / "mirror")
        process = subprocess.run([sys.executable, "-B", str(HERE), "worker", control],
                                 cwd=stage, stdin=subprocess.DEVNULL, capture_output=True,
                                 env={"LC_ALL": "C.UTF-8", "TZ": "UTC"}, timeout=20, check=False)
        if process.returncode:
            raise RuntimeError(f"isolated worker exit {process.returncode}: {process.stderr.decode(errors='replace')}")
        value = json.loads(process.stdout)
        if process.stderr or value["guard"] != {"new_file": "EPERM", "new_socket": "EPERM"}:
            raise RuntimeError("trial stderr or isolation probe mismatch")
        return value


MATRIX_FIELDS = [
    "group", "case_id", "evidence_type", "scheme", "availability", "input_status",
    "sentence", "subject", "reference_date", "file_pointer", "citation_location", "source_subject",
    "source_date", "source_value", "source_event", "original_window", "source_status", "source_mode",
    "hash_status", "outcome", "wrong_fields", "withheld_fields", "receipt", "receipt_sha256",
    "bundle_bytes", "bundle_sha256", "bundle_reads", "source_reads", "excerpt_reads", "failed_reads", "reason",
]
COST_FIELDS = [
    "group", "case_id", "scheme", "availability", "bundle_bytes", "address_utf8_bytes",
    "metadata_delta_bytes", "excerpt_and_locator_delta_bytes", "raw_excerpt_bytes",
    "bundle_reads", "source_reads", "excerpt_reads", "failed_reads", "source_file_bytes_read",
]


def csv_write(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_metrics(result):
    logs = result["read_log"]
    return {"bundle_reads": sum(r["role"] == "bundle" and r["status"] == "read" for r in logs),
            "source_reads": sum(r["role"] == "source" and r["status"] == "read" for r in logs),
            "excerpt_reads": result["excerpt_reads"],
            "failed_reads": sum(r["status"] == "missing" for r in logs)}


def result_rows(group, case, scheme, availability, blob, result, log, receipt_name, record_index):
    reads = read_metrics(result)
    record = {"group": group, "case_id": case["case_id"], "scheme": scheme, "availability": availability,
              "result": result, "score": score(result, case)}
    encoded = json_bytes(record)
    log.write(encoded)
    row = {"group": group, "case_id": case["case_id"], "evidence_type": case["evidence_type"],
           "scheme": scheme, "availability": availability, "input_status": "measured", **record["score"],
           "source_status": result["source_status"], "source_mode": result["source_mode"],
           "hash_status": result["hash_status"], "receipt": f"{receipt_name}#L{record_index}",
           "receipt_sha256": sha256(encoded), "bundle_bytes": len(blob), "bundle_sha256": sha256(blob), **reads}
    cost = {"group": group, "case_id": case["case_id"], "scheme": scheme, "availability": availability,
            "bundle_bytes": len(blob), "address_utf8_bytes": len(case["url"].encode()), **reads,
            "source_file_bytes_read": sum(r.get("bytes", 0) for r in result["read_log"] if r["role"] == "source")}
    return row, cost


def load_bundles(args, cases):
    manifest = read_json(args.bundles / "package-manifest.json")
    if (manifest["gold_sha256"], manifest["inputs_sha256"]) != (
            sha256(args.gold.read_bytes()), sha256(args.inputs.read_bytes())):
        raise ValueError("package manifest does not use current sealed inputs")
    bundles = {}
    for entry in manifest["packages"]:
        key = entry["case_id"], entry["scheme"]
        data = (args.bundles / entry["file"]).read_bytes()
        if entry["bytes"] != len(data) or entry["sha256"] != sha256(data) or key in bundles:
            raise ValueError(f"package inventory mismatch: {key}")
        bundles[key] = data
    if set(bundles) != {(key, scheme) for key in cases for scheme in ("A", "B", "C")}:
        raise ValueError("package inventory does not cover the selected cases")
    return bundles


def run_main(args):
    started = now()
    inputs = read_json(args.inputs)
    cases = {case["case_id"]: case for case in read_json(args.gold)["cases"]}
    bundles = load_bundles(args, cases)
    mirrored = verify_mirror(args.mirror, inputs)
    if set(cases) != {s["case_id"] for s in inputs["slots"] if s["status"] == "present"}:
        raise ValueError("gold cases and planned available cases differ")
    receipt_dir = args.out / "receipts"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    matrix, costs, record_index = [], [], 0
    with (receipt_dir / "core.jsonl").open("wb") as log:
        for slot in inputs["slots"]:
            case_id = slot["case_id"]
            for scheme in inputs["schemes"]:
                for availability in inputs["availability"]:
                    if slot["status"] == "missing":
                        matrix.append({"group": "main", "case_id": case_id, "evidence_type": slot["evidence_type"],
                                       "scheme": scheme, "availability": availability, "input_status": "source_missing",
                                       "outcome": "not_measured", "reason": slot["reason"]})
                        continue
                    case = cases[case_id]
                    blob = bundles[case_id, scheme]
                    result = execute_trial(blob, args.mirror if availability == "mirror" else None)
                    if result["staged_mirror_files"] != (mirrored if availability == "mirror" else 0):
                        raise ValueError("trial has unexpected mirror visibility")
                    record_index += 1
                    row, cost = result_rows("main", case, scheme, availability, blob, result, log,
                                            "receipts/core.jsonl", record_index)
                    a, b, c = [len(bundles[case_id, s]) for s in ("A", "B", "C")]
                    cost.update(metadata_delta_bytes=b - a if scheme in {"B", "C"} else 0,
                                excerpt_and_locator_delta_bytes=c - b if scheme == "C" else 0,
                                raw_excerpt_bytes=case["excerpt_bytes"] if scheme == "C" else 0)
                    matrix.append(row)
                    costs.append(cost)
    if len(matrix) != inputs["planned_cells"]:
        raise ValueError("wrong number of planned cells")
    csv_write(args.out / "matrix.csv", MATRIX_FIELDS, matrix)
    csv_write(args.out / "costs.csv", COST_FIELDS, costs)
    return {"planned": len(matrix), "measured": record_index, "source_missing": len(matrix) - record_index,
            "mirror_files": mirrored}, started, ["matrix.csv", "costs.csv", "receipts/core.jsonl"]


def record_run(args, phase, summary, started, outputs):
    version = subprocess.run(["dpkg-query", "-W", "-f=${Version}", "libseccomp2"],
                             capture_output=True, text=True, check=False)
    manifest_path = args.bundles / "package-manifest.json"
    environment = {"python": sys.version.split()[0], "executable": sys.executable,
                   "platform": platform.platform(), "libseccomp2_package": version.stdout or None}
    inputs = {"inputs.json": args.inputs, "gold.json": args.gold, "audit.py": HERE,
              "make_bundles.py": HERE.with_name("make_bundles.py"), "package-manifest.json": manifest_path}
    record = {"phase": phase, "started_utc": started, "finished_utc": now(), "exit_code": 0,
              "working_directory": str(Path.cwd()), "argv": [sys.executable, *sys.orig_argv[1:]],
              "environment": environment, "summary": summary,
              "input_file_sha256": {key: sha256(path.read_bytes()) for key, path in inputs.items()},
              "output_file_sha256": {path: sha256((args.out / path).read_bytes()) for path in outputs}}
    (args.out / "receipts" / f"{phase}-run.json").write_bytes(json_bytes(record))
    print(json_bytes(summary).decode(), end="")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    child = subs.add_parser("worker", help=argparse.SUPPRESS)
    child.add_argument("control")
    run = subs.add_parser("run")
    for name in ("inputs", "gold", "mirror", "bundles", "out"):
        run.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "worker":
        worker(args.control)
        return
    summary, started, outputs = run_main(args)
    record_run(args, "core", summary, started, outputs)


if __name__ == "__main__":
    main()
