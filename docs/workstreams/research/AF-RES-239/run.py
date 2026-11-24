#!/usr/bin/env python3
"""Run pinned public contour APIs in fresh interpreters and save verbatim streams."""

import argparse
from copy import deepcopy
import hashlib
import importlib
import importlib.metadata
import inspect
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
INPUTS = json.loads((ROOT / "inputs.json").read_text())
ENGINE_NAMES = ("skimage", "contourpy")


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def fingerprint(value):
    return sha256(canonical(value).encode("utf-8"))


def save(path, data):
    with path.open("x", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, allow_nan=False, indent=2)
        file.write("\n")


def module_record(name):
    module = importlib.import_module(name)
    path = Path(module.__file__).resolve()
    return {"path": str(path), "sha256": sha256(path.read_bytes())}


def environment():
    modules = {
        name: module_record(name)
        for name in (
            "skimage", "skimage.measure._find_contours", "skimage.measure._find_contours_cy",
            "contourpy", "contourpy._contourpy", "numpy", "numpy._core._multiarray_umath",
        )
    }
    distributions = {}
    for wheel in json.loads((ROOT / "receipts/setup/wheels.json").read_text()):
        name = wheel["distribution"]
        dist = importlib.metadata.distribution(name)
        if dist.version != wheel["version"]:
            raise ValueError(f"{name} expected {wheel['version']}, found {dist.version}")
        distributions[name] = {
            "version": dist.version,
            "expected_wheel_sha256": wheel["sha256"],
            "wheel_metadata": dist.read_text("WHEEL"),
        }
    portable = {
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "machine": platform.machine(),
        "system": platform.system(),
        "libc": list(platform.libc_ver()),
        "distributions": distributions,
        "module_sha256": {key: value["sha256"] for key, value in modules.items()},
    }
    return {"recorded_at_utc": utc_now(), "runtime_fingerprint_sha256": fingerprint(portable),
            "fingerprint_fields": portable, "platform": platform.platform(),
            "python_executable": sys.executable, "prefix": sys.prefix,
            "base_prefix": sys.base_prefix, "modules": modules,
            "system_site_packages_enabled": sys.prefix == sys.base_prefix or
            "include-system-site-packages = true" in
            (Path(sys.prefix) / "pyvenv.cfg").read_text().lower()}


def encode(value, np):
    """Preserve leaf array types and numbers. Nonfinite float tokens are strings."""
    if isinstance(value, np.ndarray):
        return {"type": "numpy.ndarray", "dtype": str(value.dtype),
                "shape": list(value.shape), "values": encode(value.tolist(), np)}
    if isinstance(value, (list, tuple)):
        return {"type": type(value).__name__, "items": [encode(item, np) for item in value]}
    if isinstance(value, float) and not math.isfinite(value):
        return "NaN" if math.isnan(value) else ("+Inf" if value > 0 else "-Inf")
    return value


def worker(job):
    import numpy as np

    spec = job["spec"]
    if fingerprint(spec) != job["input_sha256"]:
        raise ValueError("input fingerprint mismatch")
    z = np.array(spec["z"], dtype=spec["dtype"])
    valid = np.ones(z.shape, dtype=bool)
    for row, column in spec["excluded_rc"]:
        valid[row, column] = False
    level = spec["level"]
    options = job["kwargs_passed"].copy()
    engine = job["engine"]
    comparison = None
    if engine == "skimage":
        from skimage import __version__ as version
        from skimage.measure import find_contours

        if not valid.all():
            options["mask"] = valid
        raw = find_contours(z, level, **options)
        effective = dict(inspect.signature(find_contours).bind(z, level, **options).arguments)
        effective = {
            "fully_connected": effective.get("fully_connected", "low"),
            "positive_orientation": effective.get("positive_orientation", "low"),
            "mask": None if valid.all() else valid.tolist(),
        }
        module = module_record("skimage.measure._find_contours_cy")
        coordinate_order = ["row", "column"]
    elif engine == "contourpy":
        import contourpy

        version = contourpy.__version__
        argument = z if valid.all() else np.ma.array(z, mask=~valid)
        generator = contourpy.contour_generator(z=argument, **options)
        raw = generator.lines(level)
        effective = {
            "generator": type(generator).__name__,
            "corner_mask": generator.corner_mask, "line_type": generator.line_type.name,
            "quad_as_tri": generator.quad_as_tri, "z_interp": generator.z_interp.name,
            "chunk_size_rc": list(generator.chunk_size), "chunk_count_rc": list(generator.chunk_count),
            "excluded_rc": spec["excluded_rc"], "thread_count": generator.thread_count,
        }
        module = module_record("contourpy._contourpy")
        coordinate_order = ["x", "y"]
        if "compare_line_type" in job:
            target_type = job["compare_line_type"]
            target_options = {**options, "line_type": target_type}
            expected = contourpy.contour_generator(z=argument, **target_options).lines(level)
            if generator.line_type.name in {"Separate", "SeparateCode"}:
                expected = contourpy.dechunk_lines(expected, target_type)
            converted = contourpy.convert_lines(raw, generator.line_type, target_type)
            expected = encode(expected, np)
            converted = encode(converted, np)
            comparison = {"line_type_to": target_type, "equal_recursive": converted == expected,
                          "converted": converted, "generator_reference": expected}
    else:
        from scipy import __version__ as version
        from scipy.ndimage import generate_binary_structure, label

        mask = z > level
        raw = [label(mask, structure=generate_binary_structure(2, neighbors)) for neighbors in (1, 2)]
        effective = {"predicate": "z > level", "connectivity_in_order": [4, 8]}
        module = module_record("scipy.ndimage._ni_label")
        coordinate_order = None
    if engine in ENGINE_NAMES and version != INPUTS["engines"][engine]["version"]:
        raise ValueError(f"{engine} unexpected version {version}")
    print(canonical({
        "job": job, "pid": os.getpid(), "ppid": os.getppid(), "engine_version": version,
        "numpy_version": np.__version__, "input_dtype": str(z.dtype),
        "input_shape": list(z.shape), "input_c_order_sha256": sha256(z.tobytes()),
        "module": module, "interpreter": sys.executable,
        "effective_options": effective, "raw_coordinate_order": coordinate_order,
        "return": encode(raw, np), "relative_comparison": comparison,
    }))


def job_for(case, engine, repeat, *, run_id=None, kwargs=None, spec=None):
    spec = deepcopy(INPUTS["primary"][case]["spec"] if spec is None else spec)
    if kwargs is None:
        kwargs = INPUTS["engines"][engine]["default_keywords_passed"]
    return {
        "id": run_id or f"{case}-{engine}-{repeat}", "case": case,
        "engine": engine, "repeat": repeat, "spec": spec,
        "input_sha256": fingerprint(spec), "kwargs_passed": kwargs,
        "api_input_sha256": fingerprint([engine, spec, kwargs]),
    }


def control_jobs():
    for control in INPUTS["register_controls"]:
        control_id = control["id"]
        case = control["case"]
        spec = deepcopy(INPUTS["primary"][case]["spec"])
        grid = spec["z"]
        if control_id == "C4-nw-minus":
            grid[0][0] -= 2**-20
        elif control_id == "C4-nw-plus":
            grid[0][0] += 2**-20
        elif control_id == "C3-transpose":
            spec["z"] = [list(column) for column in zip(*grid)]
        elif control_id == "C3-flip-lr":
            spec["z"] = [row[::-1] for row in grid]
        elif control_id == "C3-flip-ud":
            spec["z"] = grid[::-1]
        elif control_id == "C3-negate":
            spec["z"] = [[-value for value in row] for row in grid]
        elif "-mask-nw" in control_id:
            spec["excluded_rc"] = [[0, 0]]
        elif control_id == "corner-exact":
            spec["z"] = [[0, -1], [1, -1]]
        elif control_id == "side-exact":
            spec["z"] = [[0, 0], [1, 1]]
        engines = (control["only_engine"],) if "only_engine" in control else ENGINE_NAMES
        for engine in engines:
            kwargs = INPUTS["engines"][engine]["default_keywords_passed"].copy()
            if control_id.endswith("-no-corner"):
                kwargs["corner_mask"] = False
            elif control_id == "C3-high-connected":
                kwargs["fully_connected"] = "high"
            yield job_for(case, engine, 1, run_id=f"{control_id}-{engine}", kwargs=kwargs, spec=spec)


def published_jobs():
    yield job_for("R1", "skimage", 1, run_id="R1-original-high",
                  kwargs={"positive_orientation": "high"})
    yield job_for("R2", "contourpy", 1, run_id="R2-original-Separate",
                  kwargs={"line_type": "Separate", "chunk_size": 0})
    relative = job_for("R2", "contourpy", 1, run_id="R2-original-SeparateCode-to-Offset",
                       kwargs={"line_type": "SeparateCode", "chunk_size": 0})
    relative["compare_line_type"] = "ChunkCombinedOffset"
    yield relative


def domain_jobs():
    for case in ("C4", "C5"):
        yield job_for(case, "scipy", 1, run_id=f"{case}-scipy-label4and8", kwargs={})


def capture(job, out, run_environment):
    command = [sys.executable, "-I", str(Path(__file__).resolve()), "_worker", canonical(job)]
    started = utc_now()
    tick = time.monotonic()
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        try:
            stdout, stderr = process.communicate(timeout=45)
            timed_out = False
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            timed_out = True
        result = {
            "id": job["id"], "job": job, "command_argv": command, "cwd": os.getcwd(),
            "started_utc": started, "finished_utc": utc_now(),
            "duration_seconds": time.monotonic() - tick,
            "parent_pid": os.getpid(), "pid": process.pid, "timeout": timed_out,
            "exit_code": process.returncode, "environment_sha256": run_environment["runtime_fingerprint_sha256"],
            "stdout_sha256": sha256(stdout), "stdout": stdout.decode("utf-8"),
            "stderr_sha256": sha256(stderr), "stderr": stderr.decode("utf-8"),
        }
    save(out / f"{job['id']}.json", result)
    print(f"{job['id']} pid={result['pid']} exit={result['exit_code']}")
    return result["exit_code"] == 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "_worker":
        worker(json.loads(sys.argv[2]))
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("group", choices=("primary", "published", "controls", "replay", "domain"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    output = args.out
    output.mkdir(parents=True, exist_ok=True)
    run_environment = environment()
    save(output / "environment.json", run_environment)
    if args.group in {"primary", "replay"}:
        cases = INPUTS["primary"] if args.group == "primary" else ("C3", "C4", "R1", "R2")
        repeats = (1, 2) if args.group == "primary" else (1,)
        jobs = [job_for(case, engine, rep) for case in cases
                for engine in ENGINE_NAMES for rep in repeats]
    elif args.group == "controls":
        jobs = list(control_jobs())
    elif args.group == "published":
        jobs = list(published_jobs())
    else:
        jobs = list(domain_jobs())
    passed = [capture(job, output, run_environment) for job in jobs]
    return 0 if all(passed) else 1


if __name__ == "__main__":
    sys.exit(main())
