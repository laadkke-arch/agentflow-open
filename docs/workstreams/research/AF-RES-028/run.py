#!/usr/bin/env python3
"""Replay blinded contracts with verified cached runtimes in fresh working directories."""
import argparse
import errno
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import pty
import select
import signal
import subprocess
import tempfile
import termios
import time

HERE = Path(__file__).resolve().parent
PREFIX = "AF028_JSON "


def load(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def encode(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def digest(data):
    return sha256(data).hexdigest()


def write(path, rows):
    path.write_bytes(b"".join(encode(row) + b"\n" for row in rows))


def call(command, cwd, env, *, timeout=12, data=None, detached=False):
    try:
        result = subprocess.run(command, cwd=cwd, env=env, input=data, capture_output=True, timeout=timeout,
                                start_new_session=detached)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as error:
        return 124, error.stdout or b"", (error.stderr or b"") + b"\nAF028 TIMEOUT\n"


def pseudo_terminal(command, cwd, env, password=None):
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(cwd)
        os.execve(command[0], command, env)
    raw = bytearray()
    echo_off, sent, code = None, False, None
    deadline = time.monotonic() + 8
    try:
        while time.monotonic() < deadline:
            if not select.select([fd], [], [], 0.25)[0]:
                continue
            try:
                part = os.read(fd, 4096)
                if not part:
                    break
                raw.extend(part)
            except OSError as error:
                if error.errno == errno.EIO:
                    break
                raise
            if password and b"Password: " in raw and not sent:
                echo_off = not bool(termios.tcgetattr(fd)[3] & termios.ECHO)
                os.write(fd, password + b"\n")
                sent = True
        waited, status = os.waitpid(pid, os.WNOHANG)
        # EIO/EOF can precede the final child status by a scheduler tick.
        while not waited and time.monotonic() < deadline:
            time.sleep(0.01)
            waited, status = os.waitpid(pid, os.WNOHANG)
        if waited:
            code = os.waitstatus_to_exitcode(status)
    finally:
        if code is None:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            os.waitpid(pid, 0)
            code = 124
        os.close(fd)
    return code, bytes(raw), echo_off


def getpass(binary, cwd, env):
    dummy = b"af028-pass-593"
    script = ('import getpass; value = getpass.getpass(); '
              'print("MATCHED", value == "af028-pass-593")')
    command = [binary, "-I", "-W", "default", "-c", script]
    rc, terminal, echo_off = pseudo_terminal(command, cwd, env, dummy)
    negative_rc, negative_stdout, negative_stderr = call(command, cwd, env, data=dummy + b"\n", detached=True)
    result = {"positive": dict(echo_off=echo_off, matched=b"MATCHED True" in terminal, echoed=dummy in terminal),
              "boundary": dict(warning=b"GetPassWarning" in negative_stderr, matched=b"MATCHED True" in negative_stdout),
              "diagnostic": {"pipe_rc": negative_rc, "pty_channels": "combined"}}
    if rc or negative_rc:
        result["blocked"] = "PTY or detached invocation failed"
    return command, rc, terminal + b"\n-- pipe stdout --\n" + negative_stdout, negative_stderr, result


def turtle(binary, cwd, env, system):
    command = [binary, "-I", "-W", "default", "-m", "turtledemo"]
    forbidden = dict(env)
    forbidden.pop("DISPLAY", None)
    negative_rc, neg_out, neg_err = call(command, cwd, forbidden, timeout=5)
    boundary = ("TclError" if b"TclError" in neg_err else
                "ModuleNotFoundError" if b"ModuleNotFoundError" in neg_err else "unexpected")
    result = {"positive": None, "boundary": boundary, "diagnostic": {"no_display_rc": negative_rc}}
    if boundary == "ModuleNotFoundError":
        result["blocked"] = "same-version build lacks _tkinter"
        return command, negative_rc, neg_out, neg_err, result
    lib = system / "usr/lib/x86_64-linux-gnu"
    xenv = dict(env, LD_LIBRARY_PATH=str(lib))
    xvfb = system / "usr/bin/Xvfb"
    if not xvfb.is_file():
        result["blocked"] = "Xvfb not present in the fixed supplemental cache"
        return command, 125, neg_out, neg_err, result
    launcher = [str(xvfb), "-displayfd", "1", "-screen", "0", "1024x768x24", "-nolisten", "tcp", "-ac"]
    with subprocess.Popen(launcher, cwd=cwd, env=xenv, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as xserver:
        ready = select.select([xserver.stdout], [], [], 5)[0]
        number = xserver.stdout.readline().strip() if ready else b""
        if not number.isdigit():
            xserver.terminate()
            _, xerror = xserver.communicate(timeout=5)
            result["blocked"] = "virtual display did not start"
            return command, 125, neg_out, xerror + neg_err, result
        gui_env = dict(xenv, DISPLAY=":" + number.decode())
        try:
            with subprocess.Popen(command, cwd=cwd, env=gui_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as gui:
                deadline = time.monotonic() + 5
                tree = b""
                while time.monotonic() < deadline and gui.poll() is None:
                    _, tree, _ = call(["xwininfo", "-root", "-tree"], cwd, gui_env, timeout=1)
                    if b"Python turtle-graphics examples" in tree:
                        result["positive"] = "viewer_window"
                        break
                    time.sleep(0.10)
                if gui.poll() is None:
                    gui.terminate()
                stdout, stderr = gui.communicate(timeout=3)
                result["diagnostic"]["gui_rc"] = gui.returncode
                if not result["positive"]:
                    result["blocked"] = "no matching viewer window in bounded display observation"
        finally:
            xserver.terminate()
            _, xerror = xserver.communicate(timeout=5)
    return command, 0 if result["positive"] else 125, stdout + tree + neg_out, stderr + xerror + neg_err, result


def execute(binary, eco, name, folder, env, system):
    if eco == "python" and name == "getpass":
        return getpass(binary, folder, env)
    if eco == "python" and name == "turtle":
        return turtle(binary, folder, env, system)
    if eco == "python":
        switches = ["-B", "-W", "default"]
        if name in {"distutils", "venv"}:
            switches.append("-I")
        command = [binary, *switches, str(HERE / "probes/python_probe.py"), name]
    else:
        switches = ["--trace-warnings"]
        if name == "wasi":
            switches.append("--experimental-wasi-unstable-preview1")
        command = [binary, *switches, str(HERE / "probes/node.cjs"), name]
    if name == "tty":
        rc, stdout, _ = pseudo_terminal(command, folder, env)
        stderr = b""
    else:
        rc, stdout, stderr = call(command, folder, env)
    values = next((json.loads(line.removeprefix(PREFIX)) for line in stdout.decode(errors="replace").splitlines()
                   if line.startswith(PREFIX)), {})
    return command, rc, stdout, stderr, values


def observe_version(record, cwd, env):
    binary = record["binary"]
    if record["ecosystem"] == "python":
        code = ("import json,platform,sys; print(json.dumps(dict(version=platform.python_version(),"
                " arch=platform.machine(), os=platform.system(), sys_version=sys.version, bits=64 if"
                " sys.maxsize>2**32 else 32)))")
        command = [binary, "-I", "-B", "-S", "-c", code]
    else:
        code = ("console.log(JSON.stringify({version:process.version.slice(1),arch:process.arch,os:process.platform,"
                "openssl:process.versions.openssl, uv:process.versions.uv}))")
        command = [binary, "-e", code]
    rc, stdout, stderr = call(command, cwd, env, timeout=5)
    info = json.loads(stdout) if rc == 0 else {}
    valid = (info.get("version") == record["version"] and info.get("arch") in ("x86_64", "x64")
             and info.get("os") in ("Linux", "linux")
             and digest(Path(binary).read_bytes()) == record["binary_sha256"])
    return dict(ecosystem=record["ecosystem"], tag=record["tag"], sha256=record["binary_sha256"],
                argv=command, rc=rc, stdout=stdout.decode(errors="replace"),
                stderr=stderr.decode(errors="replace"), valid=valid, reported=info)


def classify(t0, target, expected):
    first, last = t0["values"], target["values"]
    if t0["grade"] != "direct":
        return "unknown", t0["reason"]
    if "positive" not in first or "boundary" not in first:
        return "unknown", "T0 output incomplete"
    first_ok = first["positive"] == expected["expect_positive"]
    first_boundary = first["boundary"] == expected["expect_boundary"]
    if not first_ok:
        if first_boundary:
            return "initial_error", "T0 contract positive failed, boundary control observed"
        return "unknown", "T0 positive and control both differ"
    if target["grade"] != "direct":
        return "unknown", target["reason"]
    if "positive" not in last or "boundary" not in last:
        return "unknown", "target output incomplete"
    if not first_boundary:
        return "unknown", "T0 boundary differs from the fixed expectation"
    if last["positive"] != expected["expect_positive"]:
        return "invalid", "T0 contract passes and target positive differs"
    if last["boundary"] != expected["expect_boundary"]:
        return "unknown", "target boundary differs despite positive pass"
    return "supported", "both version positives and boundaries match"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("cache", "fixtures", "system", "out"):
        parser.add_argument("--" + option, type=Path, required=True)
    parser.add_argument("--only", choices=["python", "node"])
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    parts = [HERE / "packets.jsonl", HERE / "contracts.jsonl", HERE / "run.py",
             HERE / "probes/python_probe.py", HERE / "probes/node.cjs", HERE / "probes/fixtures.json"]
    input_digests = {str(path.relative_to(HERE)): digest(path.read_bytes()) for path in parts}
    for entry in json.loads(parts[-1].read_text()):
        path = args.fixtures / entry["name"]
        actual = digest(path.read_bytes())
        if actual != entry["sha256"]:
            raise ValueError(f"Fixture digest mismatch: {path}")
        input_digests["fixture/" + entry["name"]] = actual
    packets = [row for row in load(parts[0]) if args.only in (None, row["ecosystem"])]
    contracts = {cid: row for row in load(parts[1]) for cid in row["cells"]}
    versions = {}
    receipts = {}
    by_cell = []
    env = {"PATH": "/usr/bin:/bin", "TZ": "UTC", "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8",
           "PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1", "AF028_FIXTURES": str(args.fixtures.resolve())}

    def run(eco, release, contract):
        tag = release["tag"]
        key = (eco, tag, contract)
        if key in receipts:
            return receipts[key]
        file = args.cache / f"{eco}-{tag.removeprefix('v')}" / "build.json"
        record = json.loads(file.read_text()) if file.is_file() else {}
        rid = "/".join(key)
        start = time.monotonic()
        receipt = dict(id=rid, grade="none", rc=None, stdout="", stderr="", argv=[], values={},
                       reason=record.get("failure", "runtime unavailable"), mode=record.get("mode"))
        with tempfile.TemporaryDirectory(prefix="af028-", dir=args.out) as folder:
            run_env = dict(env, HOME=folder, TMPDIR=folder)
            if record.get("status") == "ready" and record["commit"] == release["commit"]:
                version_key = (eco, tag)
                if version_key not in versions:
                    versions[version_key] = observe_version(record, folder, run_env)
                if versions[version_key]["valid"]:
                    command, rc, stdout, stderr, values = execute(record["binary"], eco, contract, folder, run_env,
                                                                   args.system.resolve())
                    direct = bool(values) and not values.get("blocked") and rc == 0
                    receipt.update(grade="direct" if direct else "none", rc=rc, argv=command, values=values,
                                   stdout=stdout.decode(errors="replace"), stderr=stderr.decode(errors="replace"),
                                   combined_terminal=contract in {"getpass", "tty"},
                                   stdout_sha256=digest(stdout), stderr_sha256=digest(stderr),
                                   reason="" if direct else values.get("blocked", "probe failed before observation"))
                else:
                    receipt["reason"] = "runtime metadata or binary hash mismatch"
        receipt["wall_s"] = round(time.monotonic() - start, 4)
        receipts[key] = receipt
        return receipt

    for packet in packets:
        eco = packet["ecosystem"]
        cell = packet["cell_id"]
        details = contracts[cell]
        name = details["contract"]
        t0 = run(eco, packet["t0"], name)
        target = run(eco, packet["target"], name)
        verdict, why = classify(t0, target, details)
        by_cell.append(dict(cell_id=cell, contract=name, ecosystem=eco, quarter=packet["quarter"],
                            t0=t0["id"], target=target["id"], t0_values=t0["values"], target_values=target["values"],
                            t0_grade=t0["grade"], target_grade=target["grade"], direct_pair=t0["grade"] == target["grade"] == "direct",
                            verdict=verdict, reason=why))
    write(args.out / "observations.jsonl", by_cell)
    write(args.out / "raw.jsonl", receipts.values())
    write(args.out / "versions.jsonl", versions.values())
    inputs = {"files": input_digests, "runtime_binaries": {"/".join(key): value["sha256"] for key, value in versions.items()}}
    (args.out / "summary.json").write_bytes(encode(dict(
        cells=len(by_cell), unique_tests=len(receipts), direct_pairs=sum(row["direct_pair"] for row in by_cell),
        observation_sha256=digest((args.out / "observations.jsonl").read_bytes()), input_sha256=digest(encode(inputs)),
        inputs=inputs, environment=dict(system=platform.system(), kernel=platform.release(), machine=platform.machine(),
                                       libc=platform.libc_ver(), locale="C.UTF-8", timezone="UTC"))) + b"\n")
    print((args.out / "summary.json").read_text().strip())


if __name__ == "__main__":
    main()
