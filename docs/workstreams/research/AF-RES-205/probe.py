#!/usr/bin/env python3
"""Verify and exercise the exact AF-RES-205 wheels on Linux CPython 3.11."""

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
from email import message_from_bytes
import hashlib
import importlib
import importlib.metadata
import io
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback
import urllib.request
import zipfile


HERE = Path(__file__).resolve().parent
INPUT_PATH = HERE / "inputs.json"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")


def emit(obj):
    print(json.dumps(obj, ensure_ascii=False, allow_nan=False))


def check(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def fetch(cache, filename, url):
    path = cache / filename
    if not path.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "AF-RES-205 wheel audit"})
        with urllib.request.urlopen(request, timeout=60) as response:
            path.write_bytes(response.read())
    return path


def verify_wheels(config, cache):
    cache.mkdir(parents=True, exist_ok=True)
    for wheel_id, spec in config["wheels"].items():
        publisher_json = fetch(cache, wheel_id + ".pypi.json", spec["pypi_record"])
        published = next(row for row in json.loads(publisher_json.read_bytes())["urls"]
                         if row["filename"] == spec["filename"])
        check(published["packagetype"] == "bdist_wheel", f"{wheel_id} is not a wheel")
        check(published["url"] == spec["url"] and published["digests"]["sha256"] == spec["sha256"],
              f"{wheel_id} publisher record mismatch")
        check(published["yanked"] == spec["yanked"], f"{wheel_id} PyPI yank state changed")
        archive = fetch(cache, spec["filename"], spec["url"])
        digest = sha256(archive.read_bytes())
        check(digest == spec["sha256"] and archive.stat().st_size == published["size"] == spec["size_bytes"],
              f"{wheel_id} archive hash or size mismatch")
        with zipfile.ZipFile(archive) as wheel:
            metadata_path = spec["metadata_file"]
            metadata = message_from_bytes(wheel.read(metadata_path))
            wheel_info = message_from_bytes(wheel.read(metadata_path.replace("METADATA", "WHEEL")))
            check(metadata["Version"] == spec["version"] and wheel_info.get_all("Tag") == spec["wheel_tags"],
                  f"{wheel_id} version or wheel tag mismatch")
            record_text = wheel.read(metadata_path.replace("METADATA", "RECORD")).decode("utf-8")
            records = {row[0]: row[1:] for row in csv.reader(io.StringIO(record_text))}
            members = []
            for member in spec["files"]:
                packed = wheel.read(member["wheel_path"])
                tag_path = fetch(cache, member["source_id"] + ".source", member["raw_tag_url"])
                check(packed == tag_path.read_bytes(), f"{wheel_id} tag bytes differ")
                check(sha256(packed) == member["sha256"], f"{wheel_id} member hash mismatch")
                record_hash = base64.urlsafe_b64encode(hashlib.sha256(packed).digest()).decode().rstrip("=")
                check(records[member["wheel_path"]] == [f"sha256={record_hash}", str(len(packed))],
                      f"{wheel_id} RECORD mismatch")
                lines = packed.splitlines(keepends=True)
                regions = {}
                for location, expected in member["regions_sha256"].items():
                    first, last = map(int, location.split("-"))
                    regions[location] = sha256(b"".join(lines[first - 1:last]))
                    check(regions[location] == expected, f"{wheel_id} member region {location} mismatch")
                members.append(dict(path=member["wheel_path"], tag=member["raw_tag_url"],
                                    sha256=member["sha256"], regions_sha256=regions))
            emit(dict(wheel_id=wheel_id, filename=archive.name, sha256=digest, publisher=spec["pypi_record"],
                      url=spec["url"], uploaded_utc=published["upload_time_iso_8601"], tags=spec["wheel_tags"],
                      metadata_path=metadata_path, requires_python=metadata["Requires-Python"],
                      requires_dist=metadata.get_all("Requires-Dist", []), matches=members))


def plain(value):
    """Encode finite values and missing data without relying on repr or invalid JSON."""
    if isinstance(value, float) and not math.isfinite(value):
        if math.isnan(value):
            return {"nonfinite": "NaN"}
        return {"nonfinite": "+Inf" if value > 0 else "-Inf"}
    if isinstance(value, list):
        return [plain(item) for item in value]
    if hasattr(value, "item"):
        return plain(value.item())
    return value


def describe(array):
    return dict(values=plain(array.tolist()), dtype=str(array.dtype), dtype_name=array.dtype.name,
                shape=list(array.shape), writeable=bool(array.flags.writeable),
                owns_data=bool(array.flags.owndata))


def compare_output(output, expected, source_snapshot, shares, protect_source, replacement,
                   null_equivalence=False):
    before = source_snapshot()
    result = describe(output)
    values = result["values"]
    matches = values == expected
    if null_equivalence:
        matches = [None if item == {"nonfinite": "NaN"} else item for item in values] == expected
    change = dict(index=0, requested=replacement, performed=False, propagated=None, reason=None)
    if not result["writeable"]:
        change["reason"] = "output_writeable_false"
    elif protect_source:
        change["reason"] = "input_is_readonly_or_arrow_immutable_and_overlaps"
    else:
        output[0] = replacement
        check(plain(output[0]) != values[0], "mutation sentinel did not change output")
        change["performed"] = True
    after = source_snapshot()
    if change["performed"]:
        change["propagated"] = after != before
    result.update(exact_values_match=values == expected, values_match=matches,
                  shares_original=shares, source_before=before, source_after=after,
                  mutation=change, output_after=plain(output.tolist()))
    return result


def observed_call(call):
    try:
        return call(), None
    except Exception as exc:
        traceback.print_exc()
        frames = traceback.extract_tb(exc.__traceback__)
        return None, dict(type=type(exc).__name__, module=type(exc).__module__, message=str(exc),
                          call_frames=[dict(filename=f.filename, line=f.lineno, function=f.name,
                                            code=f.line) for f in frames])


def hf_case(fixture_id, fixture, option, observe_intermediate):
    import numpy as np
    import pyarrow as pa
    from datasets.formatting.formatting import NumpyArrowExtractor

    arrow_type = getattr(pa, fixture["arrow_type"])()
    chunks = [pa.array(values, type=arrow_type) for values in fixture["chunks"]]
    table = pa.table({"x": pa.chunked_array(chunks)})
    column = table.column("x")
    roles = ("validity", "offsets", "data") if fixture["arrow_type"] == "string" else ("validity", "data")
    parts = []
    source_views = []
    for index, chunk in enumerate(column.chunks):
        for role, buffer in zip(roles, chunk.buffers()):
            if buffer is not None:
                parts.append((index, role, np.frombuffer(buffer, dtype=np.uint8)))
        view_info = dict(chunk=index)
        try:
            view = chunk.to_numpy(zero_copy_only=True)
        except pa.ArrowException as exc:
            view_info["exception"] = dict(type=type(exc).__name__, message=str(exc))
        else:
            view_info.update(describe(view))
            data = next(raw for i, role, raw in parts if i == index and role == "data")
            view_info["shares_arrow_data"] = bool(np.shares_memory(data, view))
        source_views.append(view_info)

    def snapshot():
        return dict(values=column.to_pylist(),
                    buffers=[dict(chunk=i, role=role, bytes=len(raw), sha256=sha256(raw.tobytes()))
                             for i, role, raw in parts])

    extractor = NumpyArrowExtractor()
    trace_observation = {}
    if observe_intermediate:
        helper_code = extractor._arrow_array_to_numpy.__func__.__code__

        def trace(frame, event, arg):
            if frame.f_code is helper_code:
                if event in ("return", "exception") and "array" in frame.f_locals:
                    array = frame.f_locals["array"]
                    trace_observation.update(kind=type(array).__name__,
                                             values=plain(list(array)),
                                             element_types=[type(v).__name__ for v in array],
                                             arrow_zero_copy_only=frame.f_locals.get("zero_copy_only"),
                                             last_line=frame.f_lineno)
                return trace
            return None

        sys.settrace(trace)

    try:
        if option == "column":
            output, error = observed_call(lambda: extractor.extract_column(table))
        else:
            output, error = observed_call(lambda: extractor.extract_batch(table)["x"])
    finally:
        if observe_intermediate:
            sys.settrace(None)

    info = dict(input=dict(type=str(column.type), class_name=type(column).__name__,
                           chunks=[len(chunk) for chunk in column.chunks],
                           null_count=column.null_count, unit=None, source_chunk_views=source_views),
                intermediate=dict(method="python_trace", **trace_observation) if observe_intermediate
                else dict(method="verified_wheel_source", kind="list", location="formatting.py:167–181",
                          aliases_original_numpy_buffer=None))
    if error:
        return dict(info, status="BEHAVIOR_ERROR", exception=error, source_before=snapshot(),
                    source_after=None, output=None, original_buffer_reference=None)
    per_buffer = [dict(chunk=i, role=role, shares=bool(np.shares_memory(raw, output)))
                  for i, role, raw in parts]
    # A primitive chunk represents all logical values directly only in H1.
    direct = column.chunk(0).to_numpy(zero_copy_only=True) if fixture_id == "H1" else None
    shares = bool(np.shares_memory(direct, output)) if direct is not None else None
    any_overlap = any(row["shares"] for row in per_buffer)
    result = compare_output(output, fixture["expected_values"], snapshot, shares, any_overlap,
                            fixture["mutation"], null_equivalence=(fixture_id == "H3"))
    result.update(unit=None, physical_buffer_overlap=per_buffer,
                  original_buffer_reference="single_int64_data_view" if fixture_id == "H1" else
                  "no_single_numpy_view_for_logical_column")
    return dict(info, status="RETURNED", output=result)


def astropy_case(fixture, option):
    import numpy as np
    import astropy.units as units

    ndarray = np.array(fixture["values"], dtype=fixture["source_dtype"])
    ndarray.setflags(write=fixture["source_writable"])
    if fixture["source_kind"] == "Quantity":
        original = units.Quantity(ndarray, unit=units.Unit(fixture["source_unit"]))
        source = original.value
    else:
        original = source = ndarray

    def snapshot():
        return dict(values=plain(source.tolist()), unit=fixture["source_unit"])

    kwargs = {}
    if fixture["requested_dtype"] is not None:
        kwargs["dtype"] = np.dtype(fixture["requested_dtype"])
    if option == "false":
        kwargs["copy"] = False
    target = units.Unit(fixture["target_unit"])
    output, error = observed_call(lambda: units.Quantity(original, unit=target, **kwargs))
    info = dict(input=dict(kind=fixture["source_kind"], unit=fixture["source_unit"], **describe(source)),
                request=dict(unit=str(target), dtype=fixture["requested_dtype"], copy=option))
    if error:
        return dict(info, status="BEHAVIOR_ERROR", exception=error, source_before=snapshot(),
                    source_after=None, output=None)
    shares = bool(np.shares_memory(source, output.value))
    result = compare_output(output.value, fixture["expected_values"], snapshot, shares,
                            not source.flags.writeable and shares, fixture["mutation"])
    result.update(unit=str(output.unit), unit_match=bool(output.unit == target), quantity_writeable=bool(output.flags.writeable))
    return dict(info, status="RETURNED", output=result)


def verify_imports(config, environment_id):
    env = config["environments"][environment_id]
    spec = config["wheels"][env["wheel"]]
    wanted = {"numpy": env["numpy"], spec["package"]: spec["version"]}
    if env["pyarrow"]:
        wanted["pyarrow"] = env["pyarrow"]
    modules = []
    for name, expected in wanted.items():
        module = importlib.import_module(name)
        check(module.__version__ == expected, f"{name}: wanted {expected}, got {module.__version__}")
        modules.append(dict(name=name, version=module.__version__, file=module.__file__,
                            dist_version=importlib.metadata.version(name)))
    source_files = []
    for file in spec["files"]:
        module_name = file["wheel_path"].removesuffix(".py").replace("/", ".")
        module = importlib.import_module(module_name)
        path = Path(module.__file__).resolve()
        digest = sha256(path.read_bytes())
        check(digest == file["sha256"], f"{module_name} does not match the downloaded wheel")
        installed_file = importlib.metadata.distribution(spec["package"]).locate_file(file["wheel_path"]).resolve()
        check(path == installed_file and path.is_relative_to(Path(sys.prefix).resolve()),
              f"{module_name} was not loaded from the intended venv")
        source_files.append(dict(module=module_name, path=str(path), sha256=digest))
    emit(dict(python=sys.version, executable=sys.executable, modules=modules, installed_source=source_files))


def in_child(config, args):
    if args.action == "imports":
        verify_imports(config, args.environment)
        return 0
    if args.action == "one":
        fixture = config["fixtures"][args.fixture]
        if args.fixture.startswith("H"):
            data = hf_case(args.fixture, fixture, args.option, args.trace_intermediate)
        else:
            if args.implicit_dtype:
                fixture = {**fixture, "requested_dtype": None}
            data = astropy_case(fixture, args.option)
        emit(dict(data, fixture=args.fixture, option=args.option, pid=os.getpid()))
        return 0 if data["status"] == "RETURNED" else 10
    raise ValueError(args.action)


def child_receipt(receipt_id, command, cwd, env):
    started = datetime.now(timezone.utc).isoformat()
    tick = time.monotonic()
    outcome = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8")
    return dict(id=receipt_id, argv=[str(arg) for arg in command], cwd=str(cwd), started_utc=started,
                elapsed_seconds=round(time.monotonic() - tick, 3), exit_code=outcome.returncode,
                stdout=outcome.stdout, stderr=outcome.stderr)


def stop_code(receipt, stage):
    if receipt["exit_code"] == 0:
        return "OK"
    message = receipt["stdout"] + receipt["stderr"]
    if stage == "install":
        if "ResolutionImpossible" in message:
            return "DECLARED_CONFLICT"
        if "No matching distribution found" in message or "not a supported wheel" in message:
            return "COMPATIBLE_WHEEL_UNAVAILABLE"
        return "INSTALL_ERROR"
    if any(mark in message for mark in ("numpy.dtype size changed", "_ARRAY_API not found",
                                        "numpy.core.multiarray failed to import", "compiled using NumPy 1.x")):
        return "ABI_FAILURE"
    return "IMPORT_ERROR"


def save_install_report(report_path, output_dir, spec):
    raw = report_path.read_bytes()
    report = json.loads(raw)
    packages = []
    locked = []
    for item in sorted(report["install"], key=lambda row: row["metadata"]["name"].lower()):
        name = item["metadata"]["name"]
        version = item["metadata"]["version"]
        download = item["download_info"]
        digest = download["archive_info"]["hashes"]["sha256"]
        if name.lower() == spec["package"]:
            check(digest == spec["sha256"], "pip installed an unexpected downstream wheel")
        locked.append(f"{name}=={version} --hash=sha256:{digest}")
        packages.append(dict(name=name, version=version, sha256=digest, url=download["url"],
                             requested=item["requested"], yanked=item["is_yanked"]))
    (output_dir / "requirements.lock").write_text("\n".join(locked) + "\n", encoding="utf-8")
    write_json(output_dir / "install-hashes.json",
               dict(pip_report_sha256=sha256(raw), pip_version=report["pip_version"],
                    environment=report["environment"], packages=packages))


def collect_environment(config, environment_id, work, output, cache, locks):
    spec_env = config["environments"][environment_id]
    spec_wheel = config["wheels"][spec_env["wheel"]]
    out_dir = output / environment_id
    out_dir.mkdir()
    env_work = work / environment_id
    env_work.mkdir()
    venv = env_work / "venv"
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1",
               HF_HUB_OFFLINE="1", HF_DATASETS_OFFLINE="1", HF_HUB_DISABLE_TELEMETRY="1",
               XDG_CACHE_HOME=str(env_work / "xdg"))
    py = venv / "bin" / "python"
    install_report = env_work / "pip-report.json"
    pip = [py, "-m", "pip", "--isolated", "--disable-pip-version-check", "--no-input"]
    setup = []

    def step(name, command):
        item = child_receipt(f"{environment_id}.{name}", command, env_work, env)
        setup.append(item)
        return item

    stage = "venv"
    state = "VENV_ERROR"
    if step(stage, [sys.executable, "-m", "venv", venv])["exit_code"] == 0:
        step("pip_version", [*pip, "--version"])
        stage = "install"
        if locks is not None and (locks / environment_id / "requirements.lock").is_file():
            requirements = ["--require-hashes", "-r", locks / environment_id / "requirements.lock"]
        else:
            requirements = [f'numpy=={spec_env["numpy"]}', cache / spec_wheel["filename"]]
            if spec_env["pyarrow"]:
                requirements.append(f'pyarrow=={spec_env["pyarrow"]}')
        install = step(stage, [*pip, "--cache-dir", work / "pip-cache", "install", "--only-binary=:all:",
                              "--index-url", config["index_url"], "--report", install_report, *requirements])
        state = stop_code(install, stage)
        step("pip_freeze", [*pip, "freeze", "--all"])
        if state == "OK":
            save_install_report(install_report, out_dir, spec_wheel)
            stage = "pip_check"
            state = "PIP_CHECK_ERROR" if step(stage, [*pip, "check"])["exit_code"] else "OK"
            if state == "OK":
                stage = "imports"
                state = stop_code(step(stage, [py, __file__, "imports", environment_id]), stage)
    write_jsonl(out_dir / "setup.jsonl", setup)
    write_json(out_dir / "state.json", dict(status=state, stage=stage, environment=spec_env,
                                          receipt_id=f"{environment_id}.{stage}"))
    if state == "OK":
        rows = []
        for fixture_id in config["fixtures"]:
            if fixture_id[0] != environment_id[0]:
                continue
            for option in config["runtime"]["primary_calls"][fixture_id[0]]:
                for repeat in range(1, config["runtime"]["repetitions"] + 1):
                    rid = f"{environment_id}-{fixture_id}.{option}.r{repeat}"
                    rows.append(child_receipt(rid, [py, __file__, "one", fixture_id, option], env_work, env))
        write_jsonl(out_dir / "runs.jsonl", rows)
    return environment_id, state


def run(config, args):
    check(platform.system() == "Linux" and platform.machine() == "x86_64" and
          platform.python_implementation() == "CPython" and sys.version_info[:2] == (3, 11),
          "requires Linux x86_64 / CPython 3.11")
    work = args.work.resolve()
    cache = args.cache.resolve() if args.cache else work / "artifacts"
    locks = args.locks.resolve() if args.locks else None
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    runtime = dict(utc=datetime.now(timezone.utc).isoformat(), python=sys.version, executable=sys.executable,
                   platform=platform.platform(), os_release=platform.freedesktop_os_release(),
                   libc=platform.libc_ver(), inputs_sha256=sha256(INPUT_PATH.read_bytes()),
                   probe_sha256=sha256(Path(__file__).read_bytes()), workers=args.jobs)
    write_json(out / "runtime.json", runtime)
    proc = child_receipt("verify_wheels", [sys.executable, __file__, "verify", "--cache", cache], work, os.environ)
    write_json(out / "verify-wheels.json", proc)
    check(proc["exit_code"] == 0, f"wheel verification failed: {proc['stderr']}")
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(collect_environment, config, eid, work, out, cache, locks)
                   for eid in config["environments"]]
        for future in futures:
            print(*future.result(), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    verification = commands.add_parser("verify")
    verification.add_argument("--cache", type=Path, required=True)
    matrix = commands.add_parser("run")
    matrix.add_argument("--work", type=Path, required=True)
    matrix.add_argument("--output", type=Path, required=True)
    matrix.add_argument("--cache", type=Path)
    matrix.add_argument("--locks", type=Path)
    matrix.add_argument("--jobs", type=int, default=4)
    imports = commands.add_parser("imports")
    imports.add_argument("environment")
    one = commands.add_parser("one")
    one.add_argument("fixture")
    one.add_argument("option", choices=["column", "batch", "default", "false"])
    one.add_argument("--trace-intermediate", action="store_true")
    one.add_argument("--implicit-dtype", action="store_true")
    args = parser.parse_args()
    config = json.loads(INPUT_PATH.read_bytes())
    if args.action == "verify":
        verify_wheels(config, args.cache)
    elif args.action == "run":
        run(config, args)
    else:
        return in_child(config, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
