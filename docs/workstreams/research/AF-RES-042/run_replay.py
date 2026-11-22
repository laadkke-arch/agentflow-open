"""Rebuild the AF-RES-042 version-locked environments and preserve raw receipts."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
WORK = "/tmp/af042"
VENV = f"{WORK}/venv/bin/python"
CASES = ("P04", "P06")
INPUTS = ("inputs.jsonl", "run_replay.py", "observe_case.py", "upstream/replay_api_contracts.py")
UNKNOWN = "미확인"
NA = "해당 없음"

FINGERPRINT = r"""
import hashlib
import importlib.metadata as metadata
import json
from pathlib import Path
import platform
import sys
import sysconfig

case, expected_pandas = sys.argv[1:]
expected = {'pandas': expected_pandas, 'numpy': '1.23.5', 'python-dateutil': '2.8.2',
            'pytz': '2022.2.1', 'six': '1.16.0'}
import numpy
import pandas
import dateutil
import pytz
import six

if case == 'P04':
    from pandas._libs.tslibs.parsing import guess_datetime_format
    helper = guess_datetime_format
else:
    from pandas.core.dtypes.cast import LossySetitemError, np_can_hold_element
    helper = np_can_hold_element

version = platform.python_version()
distributions = {p: metadata.version(p) for p in expected}
fingerprint = {
    'case': case, 'python': version, 'implementation': platform.python_implementation(),
    'python_full': sys.version, 'python_binary_sha256': hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
    'executable': sys.executable, 'prefix': sys.prefix, 'base_prefix': sys.base_prefix,
    'soabi': sysconfig.get_config_var('SOABI'), 'sys_platform': sysconfig.get_platform(),
    'machine': platform.machine(), 'libc': platform.libc_ver(), 'uname': platform.uname()._asdict(),
    'os_release': Path('/etc/os-release').read_text(),
    'distributions': distributions, 'helper': helper.__name__,
    'import_versions': {m.__name__: m.__version__ for m in (numpy, pandas, dateutil, pytz, six)},
    'expected_distributions': expected,
}
print(json.dumps(fingerprint, sort_keys=True))
actual_imports = {'numpy': '1.23.5', 'pandas': expected_pandas, 'dateutil': '2.8.2',
                  'pytz': '2022.2.1', 'six': '1.16.0'}
assert version == '3.10.6' and platform.python_implementation() == 'CPython'
assert sys.prefix != sys.base_prefix and fingerprint['machine'] == 'x86_64'
assert fingerprint['soabi'].startswith('cpython-310-')
assert distributions == expected and fingerprint['import_versions'] == actual_imports
"""


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    return sha(path.read_bytes())


def json_line(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n"


class Attempt:
    def __init__(self, out, round_name, case, input_hashes):
        self.out = out
        self.case = case
        self.round = round_name
        self.prefix = f"{'F' if round_name == 'first' else 'R'}-{case}"
        self.logs = out / "logs" / f"{self.prefix}.commands.jsonl"
        self.input_hashes = input_hashes
        self.rows = []
        self.first_failure = None

    def run(self, stage, argv, *, timeout=90, artifact=None):
        started = utc()
        try:
            result = subprocess.run(argv, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            stdout, stderr, code = exc.stdout or b"", exc.stderr or b"", 124
        except OSError as exc:
            stdout, stderr, code = b"", str(exc).encode(), 127
        else:
            stdout, stderr, code = result.stdout, result.stderr, result.returncode
        finished = utc()
        if code != 0 and self.first_failure is None:
            self.first_failure = stage
        log = {
            "id": f"{self.prefix}-{stage}", "stdout": stdout.decode("utf-8", errors="surrogateescape"),
            "stderr": stderr.decode("utf-8", errors="surrogateescape"),
        }
        with self.logs.open("a") as stream:
            stream.write(json.dumps(log, ensure_ascii=True) + "\n")
        row = {
            "id": log["id"], "case": self.case, "round": self.round, "stage": stage,
            "started_utc": started, "finished_utc": finished, "argv": argv, "exit_code": code,
            "failure_stage": stage if code else NA,
            "retry_of": f"F-{self.case}-{stage}" if self.round == "replay" else NA,
            "input_sha256": self.input_hashes,
            "stdout_sha256": sha(stdout), "stdout_bytes": len(stdout),
            "stderr_sha256": sha(stderr), "stderr_bytes": len(stderr),
            "raw_log": str(self.logs.relative_to(self.out)),
            "raw_log_line": len(self.rows) + 1,
            "test_methods_run": UNKNOWN if stage == "driver" else NA,
        }
        if artifact and code == 0:
            artifact_path = self.out / "logs" / f"{self.prefix}.{artifact}"
            artifact_path.write_bytes(stdout)
            row.update(artifact=str(artifact_path.relative_to(self.out)), artifact_sha256=sha(stdout))
        if stage == "driver" and (match := re.search(rb"Ran (\d+) tests?", stderr)):
            row["test_methods_run"] = int(match.group(1))
        self.rows.append(row)
        print(f"{log['id']}: {code}", flush=True)
        return code, stdout

    def write_receipts(self):
        with (self.out / "runs.jsonl").open("a") as stream:
            stream.writelines(json_line(row) for row in self.rows)


def stage_inputs(staging, wheels):
    for name in INPUTS:
        dest = staging / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(HERE / name, dest)
    wheel_dir = staging / "wheels"
    wheel_dir.mkdir()
    lock_lines = [
        f"{wheel['project']}=={wheel['version']} --hash=sha256:{wheel['published_sha256']}"
        for wheel in wheels
    ]
    (staging / "requirements.txt").write_text("\n".join(lock_lines) + "\n")
    return wheel_dir


def replay(attempt, lock, wheels, staging):
    wheel_dir = stage_inputs(staging, wheels)
    for wheel in wheels:
        dest = wheel_dir / wheel["filename"]
        code, _ = attempt.run(
            f"fetch-{wheel['project']}",
            ["curl", "--fail", "--silent", "--show-error", "--location", "--max-time", "120",
             "--output", str(dest), wheel["url"]],
            timeout=125,
        )
        if code:
            return
        code, raw = attempt.run(
            f"hash-{wheel['project']}", ["sha256sum", str(dest)]
        )
        observed = raw.decode().split()
        matched = not code and bool(observed) and observed[0] == wheel["published_sha256"]
        attempt.rows[-1]["verified_expected_sha256"] = wheel["published_sha256"]
        attempt.rows[-1]["observed_sha256"] = observed[0] if observed else UNKNOWN
        attempt.rows[-1]["hash_match"] = matched
        if not matched:
            attempt.rows[-1]["failure_stage"] = f"hash-{wheel['project']}"
            attempt.first_failure = attempt.rows[-1]["failure_stage"]
            return
    code, raw = attempt.run("create", [
        "docker", "create", "--pull=never", "--platform", lock["platform"],
        "--network", "none", "--env", "TZ=UTC", "--env", "LC_ALL=C.UTF-8",
        "--env", "PYTHONDONTWRITEBYTECODE=1", "--env", "OPENBLAS_NUM_THREADS=1",
        lock["reference"], "sleep", "600",
    ])
    if code:
        return
    cid = raw.decode().strip()
    if not re.fullmatch(r"[0-9a-f]{64}", cid):
        raise ValueError("Docker create did not return a container ID")
    try:
        code, description = attempt.run("verify-container", [
            "docker", "container", "inspect", "--format",
            "{{.Image}} {{.HostConfig.NetworkMode}}", cid,
        ])
        if code:
            return
        if description.decode().strip() != f"{lock['config_digest']} none":
            attempt.first_failure = "verify-container"
            attempt.rows[-1]["failure_stage"] = attempt.first_failure
            return
        code, _ = attempt.run("start", ["docker", "start", cid])
        if code:
            return
        code, _ = attempt.run("copy-inputs", ["docker", "cp", str(staging), f"{cid}:{WORK}"])
        if code:
            return
        run_in = ["docker", "exec", cid]
        for step, argv, artifact in [
            ("venv", ["python", "-B", "-m", "venv", f"{WORK}/venv"], None),
            ("preinstall", [VENV, "-B", "-m", "pip", "freeze", "--all"], "preinstall.txt"),
            ("install", [VENV, "-B", "-m", "pip", "--isolated", "--disable-pip-version-check", "install",
                         "--no-index", "--no-deps", "--no-cache-dir", "--only-binary=:all:", "--require-hashes",
                         f"--find-links={WORK}/wheels", "-r", f"{WORK}/requirements.txt"], None),
            ("pip-check", [VENV, "-B", "-m", "pip", "check"], None),
            ("freeze", [VENV, "-B", "-m", "pip", "freeze", "--all"], "freeze.txt"),
            ("imports", [VENV, "-B", "-c", FINGERPRINT, attempt.case,
                         next(wheel["version"] for wheel in wheels if wheel["project"] == "pandas")], "fingerprint.json"),
        ]:
            code, _ = attempt.run(step, run_in + argv, artifact=artifact)
            if code:
                return
        attempt.run("driver", run_in + [
            VENV, "-B", f"{WORK}/upstream/replay_api_contracts.py", "--case", attempt.case,
            "--expected-numpy", "1.23.5", "--report", f"{WORK}/driver.json",
        ])
        code, report = attempt.run(
            "driver-report", run_in + ["cat", f"{WORK}/driver.json"], artifact="driver.json"
        )
        if not code:
            actual = json.loads(report)
            driver_receipt = attempt.rows[-2]
            driver_receipt["test_methods_run"] = actual.get("test_methods_run", 0)
            driver_receipt["expected_failures"] = actual.get("expected_failure_count_observed", 0)
            driver_receipt["unexpected_successes"] = len(actual.get("unexpected_successes", []))
            driver_receipt["report_sha256"] = sha(report)
            driver_receipt["driver_status"] = actual["status"]
        attempt.run("observer", run_in + [
            VENV, "-B", f"{WORK}/observe_case.py", "--case", attempt.case,
            "--output", f"{WORK}/observer.json",
        ])
        code, report = attempt.run(
            "observer-report", run_in + ["cat", f"{WORK}/observer.json"], artifact="observer.json"
        )
        if not code:
            actual = json.loads(report)
            observer_receipt = attempt.rows[-2]
            observer_receipt["ordinary_probes"] = actual["ordinary_probes"]
            observer_receipt["probes_matched"] = actual["probes_matched"]
            observer_receipt["report_sha256"] = sha(report)
    finally:
        attempt.run("remove-container", ["docker", "rm", "-f", cid])


def stable_json(path):
    record = json.loads(path.read_bytes())
    for field in ("software_replay_started_utc", "software_replay_finished_utc"):
        record.pop(field, None)
    record.get("environment", {}).get("uname", {}).pop("node", None)
    record.get("uname", {}).pop("node", None)
    return record


def compare(first, repeated, out):
    summaries = {}
    for case in CASES:
        first_rows, repeated_rows = [
            {row["stage"]: row for line in (path / "runs.jsonl").read_text().splitlines()
             if (row := json.loads(line)).get("case") == case}
            for path in (first, repeated)
        ]
        stages = sorted(set(first_rows) | set(repeated_rows))
        checks = {
            "exit_codes": all(
                first_rows.get(s, {}).get("exit_code") == repeated_rows.get(s, {}).get("exit_code") == 0
                for s in stages
            ),
            "input_bytes": bool(stages) and all(
                first_rows.get(s, {}).get("input_sha256") == repeated_rows.get(s, {}).get("input_sha256")
                for s in stages
            ),
            "wheel_hashes": sum(
                bool(first_rows[s].get("hash_match"))
                and bool(repeated_rows.get(s, {}).get("hash_match"))
                and first_rows[s].get("observed_sha256") == repeated_rows[s].get("observed_sha256")
                for s in first_rows if s.startswith("hash-")
            ) == 5,
        }
        hashes = {}
        for name in ("driver.json", "observer.json", "fingerprint.json", "preinstall.txt", "freeze.txt"):
            left = first / "logs" / f"F-{case}.{name}"
            right = repeated / "logs" / f"R-{case}.{name}"
            if not left.is_file() or not right.is_file():
                checks[name], hashes[name] = False, UNKNOWN
                continue
            hashes[name] = {"first": sha_file(left), "replay": sha_file(right)}
            if name.endswith(".json"):
                checks[name] = stable_json(left) == stable_json(right)
            else:
                checks[name] = left.read_bytes() == right.read_bytes()
        summaries[case] = {"matches": all(checks.values()), "checks": checks, "raw_hashes": hashes}
    report = {
        "same_input_and_output": all(summary["matches"] for summary in summaries.values()),
        "cases": summaries,
        "excluded_from_semantic_match": [
            "receipt UTC, container IDs and local staging paths",
            "driver start/end UTC, unittest elapsed time and container hostname (uname.node)",
        ],
        "retained_for_semantic_match": [
            "all other driver and observer JSON (values, Python types, dtype, warnings, exceptions, frames, post-state)",
            "interpreter SHA-256, SOABI, libc/OS, platform, dependency freeze and all wheel hashes",
            "stage exit codes, installed package versions, input hashes",
        ],
    }
    (out / "comparison.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return int(not report["same_input_and_output"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round", choices=("first", "replay", "both"))
    parser.add_argument("--compare", nargs=2, metavar=("FIRST", "REPLAY"), type=Path)
    parser.add_argument("--case", choices=CASES, action="append")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if bool(args.round) == bool(args.compare):
        parser.error("use exactly one of --round or --compare")
    args.out.mkdir(parents=True, exist_ok=False)
    if args.compare:
        return compare(*args.compare, args.out)
    env = json.loads((HERE / "environments.json").read_text())
    artifacts = env["observed"]["artifact_lock"]
    common_hashes = {name: sha_file(HERE / name) for name in INPUTS}
    if common_hashes["upstream/replay_api_contracts.py"] != env["pre_observation_contract"]["driver_sha256"]:
        parser.error("the upstream driver SHA-256 does not match the frozen input")
    rounds = ("first", "replay") if args.round == "both" else (args.round,)
    ok = True
    infrastructure = artifacts["image"]
    for round_name in rounds:
        out = args.out / round_name if len(rounds) == 2 else args.out
        (out / "logs").mkdir(parents=True)
        for case in args.case or CASES:
            wheels = [wheel for wheel in artifacts["wheels"] if case in wheel["cases"]]
            input_hashes = {
                **common_hashes, "interpreter_image_manifest": infrastructure["platform_manifest_digest"],
                **{wheel["filename"]: wheel["published_sha256"] for wheel in wheels},
            }
            attempt = Attempt(out, round_name, case, input_hashes)
            try:
                with tempfile.TemporaryDirectory(prefix=f"af042-{round_name}-{case}-") as temp:
                    replay(attempt, infrastructure, wheels, Path(temp))
            finally:
                attempt.write_receipts()
            ok = ok and attempt.first_failure is None
    if len(rounds) == 2:
        ok = compare(args.out / "first", args.out / "replay", args.out) == 0 and ok
    return int(not ok)


if __name__ == "__main__":
    raise SystemExit(main())
