"""Run hash-pinned timezone packages as isolated unpacked installations."""
import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from catalog import HERE, digest, dump, utc_now

FIXTURES = HERE / "fixtures.json"
UTC = timezone.utc
NODE_PACKED = "node_modules/moment-timezone/data/packed/latest.json"
BUNDLES = {
    "all": ("builds/moment-timezone-with-data.js", "full"),
    "ten": ("builds/moment-timezone-with-data-10-year-range.js", "rolling ±5 years around build year"),
    "1970-2030": ("builds/moment-timezone-with-data-1970-2030.js", "1970–2030"),
    "2012-2022": ("builds/moment-timezone-with-data-2012-2022.js", "2012–2022; query outside stated range"),
    "no-data": ("moment-timezone.js", "no loaded data"),
}


def member(path, root=None):
    path = path.resolve()
    content = path.read_bytes()
    return {"path": str(path), "member": str(path.relative_to(root)) if root else str(path),
            "bytes": len(content), "sha256": digest(content)}


def read_epoch(instant):
    return int(datetime.fromisoformat(instant.replace("Z", "+00:00")).timestamp())


def python_probe(job):
    from zoneinfo import TZPATH, ZoneInfo
    import _zoneinfo

    root = Path(job["root"]).resolve()
    default = job["mode"] == "default"
    origin = _zoneinfo.__spec__.origin
    runtime = {"executable": sys.executable, "python": sys.version, "tzpath": list(TZPATH),
               "extension": {"origin": origin, "file": member(Path(origin)) if origin != "built-in" else None}}
    zones = {}
    used = {}
    results = []
    for query in job["inputs"]:
        key = query["zone"]
        path = root / "tzdata" / "zoneinfo" / key
        if key not in zones:
            try:
                if default:
                    zone = ZoneInfo(key)
                    loaded = next((Path(directory) / key for directory in TZPATH
                                   if (Path(directory) / key).is_file()), path)
                else:
                    loaded = path
                    with loaded.open("rb") as tzif:
                        original_bytes = tzif.read()
                    zone = ZoneInfo.from_file(io.BytesIO(original_bytes), key=key)
                used[key] = member(loaded, root if loaded.is_relative_to(root) else None)
                zones[key] = zone
            except (KeyError, FileNotFoundError) as exc:
                results.append({**query, "missing": str(exc)})
                continue
        zone = zones[key]
        if job["mode"] == "wall-as-utc":
            clock = datetime.fromisoformat(query["utc"][:-1]).replace(tzinfo=zone)
        else:
            clock = datetime.fromtimestamp(query["unix_seconds"], tz=UTC).astimezone(zone)
        results.append({
            **query,
            "evaluated_unix_seconds": int(clock.timestamp()),
            "evaluated_utc": clock.astimezone(UTC).isoformat(),
            "value": {"offset_s": int(clock.utcoffset().total_seconds()),
                      "wall": clock.replace(tzinfo=None).isoformat(), "abbr": clock.tzname()},
            "loaded": used[key],
        })
    return {"runtime": runtime, "records": results}


def secure_names(names):
    for name in names:
        candidate = PurePosixPath(name)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError("Archive member escapes isolation: " + name)


def unpack_wheel(content, root):
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        secure_names(archive.namelist())
        archive.extractall(root)


def unpack_npm(content, root, name):
    destination = root / "node_modules" / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = root / "_staging"
    staging.mkdir()
    with tarfile.open(fileobj=io.BytesIO(content), mode="r:gz") as archive:
        names = archive.getnames()
        secure_names(names)
        if any(PurePosixPath(path).parts[0] != "package" for path in names):
            raise ValueError("Unexpected npm archive root")
        archive.extractall(staging, filter="data")
    (staging / "package").rename(destination)
    staging.rmdir()


def read_archive(path, pin):
    data = path.read_bytes()
    if digest(data) != pin:
        raise ValueError(f"Archive mismatch against sealed SHA-256 for {path.name}: {digest(data)}")
    return data


def setup(case, archive_dir, root, shared):
    root.mkdir(parents=True)
    data = read_archive(archive_dir / case["file"], case["sha256"])
    if case["ecosystem"] == "PyPI":
        unpack_wheel(data, root)
    else:
        unpack_npm(data, root, "moment-timezone")
        pin = shared["node_dependency"]
        dependency = read_archive(archive_dir / pin["filename"], pin["observed_sha256"])
        unpack_npm(dependency, root, pin["package"])
    return data


def run_probe(root, name, ecosystem, inputs, mode, bundle=None, empty_tzpath=False):
    job = {"root": str(root), "inputs": inputs, "mode": mode, "bundle": bundle}
    job_file = root / f"{name}.probe.json"
    dump(job_file, job)
    env = os.environ.copy()
    for key in ("PYTHONPATH", "PYTHONTZPATH", "PYTHONHOME", "NODE_OPTIONS", "NODE_PATH", "TZ"):
        env.pop(key, None)
    env.update(PYTHONNOUSERSITE="1", TZ="UTC")
    if mode == "default":
        env["PYTHONPATH"] = str(root)
    if empty_tzpath:
        env["PYTHONTZPATH"] = ""
    if ecosystem == "PyPI":
        argv = [sys.executable, "-B", str(Path(__file__)), "probe", str(job_file)]
    else:
        argv = ["node", str(HERE / "read-packed.cjs"), str(job_file)]
    trace = root / f"{name}.openat"
    traced_argv = ["strace", "-qq", "-f", "-s", "384", "-e", "trace=openat", "-o", str(trace),
                   *argv] if shutil.which("strace") else argv
    start = time.monotonic()
    when = utc_now()
    process = subprocess.run(traced_argv, cwd=root, env=env, capture_output=True, text=True, timeout=40)
    observation = {
        "process_id": name, "argv": traced_argv, "cwd": str(root), "input": job,
        "input_sha256": digest(job_file.read_bytes()), "started_utc": when,
        "wall_ms": round((time.monotonic() - start) * 1000, 3),
        "path_env": {key: env[key] for key in ("TZ", "PYTHONNOUSERSITE", "PYTHONPATH", "PYTHONTZPATH")
                     if key in env},
        "exit_code": process.returncode, "stdout": process.stdout, "stderr": process.stderr,
        "stdout_sha256": digest(process.stdout.encode()), "stderr_sha256": digest(process.stderr.encode()),
    }
    if trace.exists():
        trace_text = trace.read_text()
        observation["trace_sha256"] = digest(trace_text.encode())
        # Paths to the loaded data, loader, and fallback only. Full audit trace remains local.
        observation["trace_selected_opens"] = [
            line for line in trace_text.splitlines()
            if re.search(r'tzdata/zoneinfo/(?:Asia/Beirut|America/New_York)|'
                         r'/zoneinfo/(?:Asia/Beirut|America/New_York)|'
                         r'node_modules/(?:moment-timezone/.+(?:\.json|\.js)|moment/moment\.js)', line)
        ]
    output = {}
    if process.returncode == 0:
        try:
            output = json.loads(process.stdout)
        except ValueError as exc:
            observation["protocol_error"] = str(exc)
    return observation, output


def flatten(case, step, process, output, inputs, expected=None):
    found = {x["id"]: x for x in output.get("records", [])}
    rows = []
    for query in inputs:
        observed = found.get(query["id"])
        row = {"distribution": case["id"], "archive_sha256": case["sha256"],
               "ecosystem": case["ecosystem"], "label": case["iana"], "step": step,
               "process_id": process["process_id"], "exit_code": process["exit_code"], **query}
        if observed is None:
            row["status"] = "process-failed"
        elif "value" not in observed:
            row.update(status="zone-missing", reason=observed.get("missing"))
        else:
            row.update(observed, status="read")
            if "loaded" not in row:
                row["loaded"] = output.get("loaded")
        if expected:
            row["expected"] = expected.get(query["id"])
            row["agrees_with_prediction"] = row.get("value") == row["expected"]
        rows.append(row)
    return rows


def json_lines(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
                    encoding="utf-8")


def finger_inputs(shared):
    return [{"id": f"F{number}", "zone": "Asia/Beirut", "utc": instant,
             "unix_seconds": read_epoch(instant)}
            for number, instant in enumerate(shared["fingerprint_instants_utc"], 1)]


def save_failure(case, process_id, root, error):
    return {"process_id": process_id, "cwd": str(root), "case": case, "phase": "unpack-or-probe",
            "exit_code": None, "error": f"{type(error).__name__}: {error}"}


def main(archives, work, shared):
    archives = archives.resolve()
    work = work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    output = work / "out"
    output.mkdir()
    queries = shared["inputs"]
    for query in queries:
        if read_epoch(query["utc"]) != query["unix_seconds"]:
            raise ValueError(f"Inconsistent frozen Unix seconds for {query['id']}")
    predictions = shared["predictions"]
    fingerprints = finger_inputs(shared)
    receipts, rows, controls, finger_rows = [], [], [], []
    order = {}
    selected_roots = {}
    for step in ("forward", "reverse"):
        ordered = predictions if step == "forward" else list(reversed(predictions))
        order[step] = [case["id"] for case in ordered]
        for case in ordered:
            case_id = case["id"]
            root = work / step / case_id
            pid = f"{step}-{case_id}"
            try:
                setup(case, archives, root, shared)
                selected_roots[(step, case_id)] = root
                proc, observed = run_probe(root, pid, case["ecosystem"], [*queries, *fingerprints], "exact")
            except (ValueError, OSError, tarfile.TarError, zipfile.BadZipFile, subprocess.TimeoutExpired) as exc:
                proc, observed = save_failure(case_id, pid, root, exc), {}
            receipts.append(proc)
            rows.extend(flatten(case, step, proc, observed, queries, case["expected"]))
            for row in flatten(case, step, proc, observed, fingerprints):
                index = int(row["id"][1:]) - 1
                expected = case["fingerprint_offset_abbr"]
                if expected is not None:
                    row["expected_offset_abbr"] = expected[index]
                    value = row.get("value", {})
                    row["agrees_with_prediction"] = [value.get("offset_s"), value.get("abbr")] == expected[index]
                finger_rows.append(row)

    def control(case, label, root, inputs, mode, bundle=None, **kwargs):
        pid = f"{label}-{case['id']}"
        try:
            proc, observed = run_probe(root, pid, case["ecosystem"], inputs, mode, bundle, **kwargs)
        except (OSError, subprocess.TimeoutExpired) as exc:
            proc, observed = save_failure(case["id"], pid, root, exc), {}
        receipts.append(proc)
        return flatten(case, label, proc, observed, inputs, case["expected"])

    first_query = queries[:1]
    for ecosystem in ("PyPI", "npm"):
        cases = [case for case in predictions if case["ecosystem"] == ecosystem]
        wanted = next((item for item in cases if item["iana"] == "2023b"), cases[1])
        donor = [item for item in cases[:cases.index(wanted)] if item["iana"] != "2023b"][-1]
        root = work / "controls" / f"donor-in-{wanted['id']}"
        setup(wanted, archives, root, shared)
        relabel_path = "tzdata/zoneinfo/Asia/Beirut" if ecosystem == "PyPI" else NODE_PACKED
        file = root / relabel_path
        expected = member(file, root)
        old = selected_roots[("forward", donor["id"])] / relabel_path
        donor_bytes = old.read_bytes()
        if ecosystem == "npm":
            donor_bytes = re.sub(rb'"version"\s*:\s*"[^"]+"',
                                 f'"version": "{wanted["iana"]}"'.encode(), donor_bytes, count=1)
        file.write_bytes(donor_bytes)
        injected = control(wanted, "relabel", root, first_query, "exact")
        for row in injected:
            loaded = row.get("loaded")
            row.update(injection="deliberately replaced one member in a private copy",
                       donor=donor["id"], donor_original_sha256=digest(old.read_bytes()),
                       authentic_member=expected,
                       strict_accept=loaded["sha256"] == expected["sha256"] if loaded else None)
        controls.extend(injected)
        clean = work / "controls" / wanted["id"]
        setup(wanted, archives, clean, shared)
        controls.extend(control(wanted, "wall-as-utc", clean, first_query, "wall-as-utc"))
        if ecosystem == "PyPI":
            controls.extend(control(wanted, "host-default", clean, first_query, "default"))
            controls.extend(control(wanted, "wheel-fallback", clean, first_query, "default", empty_tzpath=True))
        else:
            controls.extend(control(wanted, "host-icu", clean, first_query, "intl"))
            for case in cases:
                root = work / "bundles" / case["id"]
                setup(case, archives, root, shared)
                for variant, (bundle, coverage) in BUNDLES.items():
                    if (root / "node_modules/moment-timezone" / bundle).is_file():
                        bundle_rows = control(case, f"bundle-{variant}", root, queries, "bundle", bundle)
                        controls.extend({**row, "published_coverage": coverage} for row in bundle_rows)
                    else:
                        controls.extend({"distribution": case["id"], "step": f"bundle-{variant}",
                                         "published_coverage": coverage, "status": "bundle-missing", **query}
                                        for query in queries)

    json_lines(output / "runs.jsonl", rows)
    json_lines(output / "fingerprints.jsonl", finger_rows)
    json_lines(output / "controls.jsonl", controls)
    tools = {"python": member(Path(sys.executable)), "node": member(Path(shutil.which("node"))),
             "strace": member(Path(shutil.which("strace"))) if shutil.which("strace") else None}
    dump(output / "run-receipts.json", {
        "started_from": str(work), "order": order, "tools": tools,
        "fixture_sha256": digest(FIXTURES.read_bytes()),
        "script_sha256": {name: digest((HERE / name).read_bytes())
                          for name in ("replay.py", "read-packed.cjs", "catalog.py")},
        "output_sha256": {name: digest((output / name).read_bytes()) for name in
                          ("runs.jsonl", "fingerprints.jsonl", "controls.jsonl")},
        "processes": receipts,
    })
    print(f"{len(rows)} main slots, {len(finger_rows)} fingerprint slots, {len(controls)} control slots")
    print(f"{sum(row.get('agrees_with_prediction', False) for row in rows)} main predictions matched")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    probe = subparsers.add_parser("probe")
    probe.add_argument("spec", type=Path)
    run = subparsers.add_parser("run")
    run.add_argument("archives", type=Path)
    run.add_argument("work", type=Path)
    args = parser.parse_args()
    if args.command == "probe":
        print(json.dumps(python_probe(json.loads(args.spec.read_text())), sort_keys=True))
    else:
        main(args.archives, args.work, json.loads(FIXTURES.read_text()))
