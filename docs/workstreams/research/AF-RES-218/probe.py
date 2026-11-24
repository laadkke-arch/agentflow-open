"""Generate the matched FITS inputs, run isolated writers/readers, or replay the receipts."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
import itertools
import json
import mmap
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import traceback
import warnings

from reopen import digest


HERE = Path(__file__).resolve().parent
INPUT_PATH = HERE / "inputs.json"
INPUT = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
FIXTURE = INPUT["generated_fits"]
PHASES = ("before_flush_or_close", "after_flush", "after_hdul_close", "after_writer_exit")
MODES = {"readonly": "RO", "copyonwrite": "CW", "update": "UP"}
PATHS = {"direct": "D", "quantity": "Q"}
BOUNDARIES = {"close": "C", "flush_close": "FC"}
CONTROLS = (
    ("FC-EXPORT", "copyonwrite", "direct", "close", True),
    ("FC-DEEP", "update", "deep_copy", "flush_close", True),
    ("FC-NOOP", "update", "no_write", "close", True),
    ("FC-BUFFERED", "update", "direct", "flush_close", False),
    ("FC-HEADER", "update", "header_only", "flush_close", True),
    ("FC-EXISTING", "copyonwrite", "direct", "close", True),
)


def utc():
    return datetime.now(timezone.utc).isoformat()


def json_text(data, indent=None):
    return json.dumps(data, indent=indent, ensure_ascii=False, allow_nan=False) + "\n"


def sha_file(path):
    return digest(path.read_bytes())


def capture(argv, cwd, timeout=30):
    argv = [str(arg) for arg in argv]
    started = utc()
    try:
        run = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        code, out, err = run.returncode, run.stdout, run.stderr
    except subprocess.TimeoutExpired as exc:
        code = 124
        out = (exc.stdout or b"").decode("utf-8", "replace")
        err = (exc.stderr or b"").decode("utf-8", "replace") + "\nTimed out"
    return dict(argv=argv, cwd=str(cwd), started_utc=started, finished_utc=utc(),
                exit_code=code, stdout=out, stderr=err)


def child_args(program, *args):
    return [sys.executable, "-E", "-s", "-B", HERE / program, *args]


def reader(path):
    return capture(child_args("reopen.py", path, "--hdu", FIXTURE["hdu_index"],
                              "--pixel", FIXTURE["pixel_index"]), path.parent)


def decoded(receipt):
    if receipt and receipt["exit_code"] == 0:
        try:
            return json.loads(receipt["stdout"])
        except json.JSONDecodeError:
            pass
    return {}


def observed(sample, path):
    if not sample:
        return False
    return (sample["path"] == str(path) and sample["raw_pixel_value"] == sample["value"]
            and all(sample[key] == FIXTURE[key] for key in (
                "size_bytes", "hdu_index", "pixel_index", "bitpix", "naxis", "naxis1",
                "bunit", "unit", "data_offset"))
            and sample["dtype"] == FIXTURE["wire_dtype"]
            and sample["pixel_offset"] == FIXTURE["data_offset"] + 8 * FIXTURE["pixel_index"])


def check_environment():
    import astropy
    import numpy as np
    from astropy.io.fits import file
    from astropy.io.fits.hdu import base, hdulist, image
    from astropy.units import quantity

    runtime = {
        "system": platform.system(), "machine": platform.machine(),
        "python": platform.python_version(), "numpy": np.__version__,
        "astropy": astropy.__version__,
    }
    expected = INPUT["runtime"]
    if any(runtime[key] != expected[key] for key in runtime):
        raise RuntimeError(f"incorrect pinned environment: {runtime}")
    lock_sha = sha_file(HERE / expected["lock_path"])
    if lock_sha != expected["lock_sha256"]:
        raise RuntimeError("the A01 dependency lock has changed")
    runtime.update(
        system_detail=platform.platform(), python_build=sys.version, libc=platform.libc_ver(),
        python_executable=sys.executable, byteorder=sys.byteorder, utc=utc(),
        lock_sha256=lock_sha, input_sha256=sha_file(INPUT_PATH),
        probe_sha256=sha_file(HERE / "probe.py"), reader_sha256=sha_file(HERE / "reopen.py"),
        loaded_modules={mod.__name__: {"path": mod.__file__, "sha256": sha_file(Path(mod.__file__))}
                        for mod in (astropy, np, file, base, hdulist, image, quantity)},
    )
    return runtime


def generate_fixture(path):
    import numpy as np
    from astropy import units as u
    from astropy.io import fits

    hdu = fits.PrimaryHDU(np.asarray(FIXTURE["values"], dtype="float64"))
    hdu.header["BUNIT"] = u.Unit(FIXTURE["unit"]).to_string("fits")
    hdu.writeto(path, checksum=False, overwrite=False)
    if sha_file(path) != FIXTURE["sha256"]:
        raise RuntimeError("generated FITS bytes differ from the frozen fixture")
    sample = reader(path)
    seen = decoded(sample)
    if (not observed(seen, path) or seen["raw_pixel_hex"] != FIXTURE["pixel_before_hex"]
            or seen["value"] != FIXTURE["values"][FIXTURE["pixel_index"]]):
        raise RuntimeError(f"baseline reader disagrees: {sample}")
    return sample


def array_state(array):
    if array is None:
        return None
    return dict(value=float(array[FIXTURE["pixel_index"]]), dtype=array.dtype.str,
                dtype_name=array.dtype.name, shape=list(array.shape),
                writeable=bool(array.flags.writeable), ndarray_unit=None)


def quantity_from(array):
    from astropy import units as u

    return u.Quantity(array, unit=u.Unit(FIXTURE["unit"]), copy=False)


def set_pixel(array):
    array[FIXTURE["pixel_index"]] = FIXTURE["replacement"]


def action(fn):
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        outcome = {"state": "returned"}
        try:
            value = fn()
        except Exception as exc:
            value = None
            outcome = dict(state="raised", exception=type(exc).__name__, message=str(exc))
            traceback.print_exc()
    outcome["warnings"] = [dict(category=w.category.__name__, message=str(w.message),
                                filename=w.filename, lineno=w.lineno) for w in captured]
    for w in captured:
        warnings.showwarning(w.message, w.category, w.filename, w.lineno)
    return value, outcome


def array_mmap(array):
    base = array.base
    while base is not None and not isinstance(base, mmap.mmap):
        base = getattr(base, "base", None)
    return base


def heap_preflight():
    import numpy as np

    entries = []
    for name, dtype in (("PF-NATIVE", "float64"), ("PF-BIG-ENDIAN", FIXTURE["wire_dtype"])):
        original = np.array(FIXTURE["values"], dtype=dtype)
        output = quantity_from(original)
        values = output.value
        before = array_state(original)
        shares = bool(np.shares_memory(original, values))
        set_pixel(values)
        entries.append(dict(id=name, original_before=before, original_after=array_state(original),
                            output_after=array_state(values), shares_memory=shares,
                            unit=str(output.unit), pid=os.getpid()))
    print(json_text(entries), end="")


def write_case(case_id, path, mode, access, boundary, memmap):
    import numpy as np
    from astropy import units as u
    from astropy.io import fits

    before_sha = sha_file(path)
    if path.name != "original.fits" or before_sha != FIXTURE["sha256"]:
        raise RuntimeError("writer requires a fresh generated original.fits")
    parent_dir = path.parent
    new_path = parent_dir / "export.fits"
    data = dict(id=case_id, pid=os.getpid(), start_sha256=before_sha,
                path=str(path), memmap_requested=memmap, phases={}, actions={})
    hdul, data["actions"]["open"] = action(
        lambda: fits.open(path, mode=mode, memmap=memmap, lazy_load_hdus=False))
    if hdul is None:
        print(json_text(data), end="")
        sys.exit(10)
    try:
        hdu = hdul[FIXTURE["hdu_index"]]
        array, data["actions"]["data"] = action(lambda: hdu.data)
        if array is None:
            print(json_text(data), end="")
            sys.exit(11)
        mapping = array_mmap(array)
        original = array.copy() if access == "deep_copy" else array
        target, quantity = None, None
        data["hdu_before"] = array_state(array)
        data["bunit"] = hdu.header["BUNIT"]
        data["hdu_unit"] = str(u.Unit(data["bunit"], format="fits"))
        data["mapping"] = dict(array_backed=mapping is not None, file_memmap=bool(hdul._file.memmap))
        if access in ("quantity", "deep_copy"):
            quantity, data["actions"]["quantity"] = action(lambda: quantity_from(original))
            target = quantity.value if quantity is not None else None
        elif access == "direct":
            target = original
        data["quantity_unit"] = str(quantity.unit) if quantity is not None else None
        data["target_before"] = array_state(target)
        data["shares_hdu"] = bool(np.shares_memory(array, target)) if target is not None else None
        data["shares_call_input"] = (bool(np.shares_memory(original, target))
                                     if target is not None else None)
        if target is not None:
            _, data["actions"]["write"] = action(lambda: set_pixel(target))
        elif access == "header_only":
            hdu.header.add_history("AF-RES-218 header-only control")
        data["hdu_after"] = array_state(array)
        data["target_after"] = array_state(target)
        data["phases"]["before_flush_or_close"] = reader(path)

        if case_id == "FC-EXPORT":
            data["export_existed_before"] = new_path.exists()
            _, data["actions"]["writeto"] = action(lambda: hdul.writeto(new_path, overwrite=False))
            data["export_after_writeto"] = reader(new_path)
        if case_id == "FC-EXISTING":
            _, data["actions"]["writeto"] = action(lambda: hdul.writeto(path, overwrite=False))

        if boundary == "flush_close":
            _, data["actions"]["flush"] = action(hdul.flush)
            data["phases"]["after_flush"] = reader(path)
    finally:
        _, data["actions"]["close"] = action(hdul.close)

    data["hdu_file_closed"] = bool(hdul._file.closed)
    data["retained_array_mapping_closed"] = mapping.closed if mapping is not None else None
    data["phases"]["after_hdul_close"] = reader(path)
    print(json_text(data), end="")


def matrix_cases():
    spec = INPUT["matrix"]
    for mode, access, boundary, repeat in itertools.product(
        spec["modes"], spec["paths"], spec["boundaries"], spec["repeats"]
    ):
        case_id = f"{MODES[mode]}-{PATHS[access]}-{BOUNDARIES[boundary]}-r{repeat}"
        yield case_id, mode, access, boundary, spec["writer_memmap"]


def run_one(baseline, work, spec):
    case_id, mode, access, boundary, memmap = spec
    folder = work / case_id
    folder.mkdir()
    original = folder / "original.fits"
    shutil.copyfile(baseline, original)
    writer = capture(child_args("probe.py", "writer", case_id, original, mode, access,
                                boundary, str(int(memmap))), folder, timeout=120)
    after_exit = reader(original)
    new_file = folder / "export.fits"
    return dict(case_id=case_id, mode=mode, access=access, boundary=boundary, memmap=memmap,
                provenance="synthetic_fixture", original=str(original),
                baseline_sha256=sha_file(baseline), writer=writer, after_writer_exit=after_exit,
                new_after_writer_exit=reader(new_file) if new_file.exists() else None)


def compare_file(sample, baseline):
    if not sample:
        return "unverified"
    if sample["sha256"] == baseline["sha256"]:
        return "byte_identical"
    if sample["data_sha256"] == baseline["data_sha256"]:
        return "header_only"
    if (sample["header_sha256"] == baseline["header_sha256"]
            and sample["other_data_sha256"] == baseline["other_data_sha256"]
            and sample["raw_pixel_hex"] != baseline["raw_pixel_hex"]):
        return "target_pixel_only"
    return "other_or_mixed_changes"


def summarize(record, baseline):
    writer = decoded(record["writer"])
    actions = writer.get("actions", {})
    readings = writer.get("phases", {}) | {"after_writer_exit": record["after_writer_exit"]}
    expected_phases = list(PHASES)
    if record["boundary"] == "close":
        expected_phases.remove("after_flush")
    values = {name: decoded(readings.get(name)) for name in PHASES}
    last = values["after_writer_exit"]
    original = record["original"]
    expected_path = Path(original)
    checks = all(observed(values[name], expected_path) for name in expected_phases)
    if checks and writer:
        pids = {values[name]["pid"] for name in expected_phases}
        checks = len(pids) == len(expected_phases) and writer["pid"] not in pids
        checks = checks and record["after_writer_exit"]["started_utc"] >= record["writer"]["finished_utc"]
    diff = compare_file(last, baseline)
    state = "UNVERIFIED"
    if checks and writer and writer["hdu_file_closed"] and actions["close"]["state"] == "returned":
        if last["value"] == FIXTURE["replacement"] and last["raw_pixel_hex"] == FIXTURE["pixel_after_hex"]:
            state = "PERSISTED_IN_ORIGINAL_PATH"
        elif last["value"] == baseline["value"] and last["raw_pixel_hex"] == baseline["raw_pixel_hex"]:
            state = "ORIGINAL_PIXEL_UNCHANGED"
        else:
            state = "UNEXPECTED_PIXEL"
    execution = "OBSERVED" if state not in ("UNVERIFIED", "UNEXPECTED_PIXEL") else "FAILED"
    if any(actions.get(name, {}).get("state") == "raised" for name in ("quantity", "write", "flush", "close")):
        execution = "ACTION_EXCEPTION" if execution == "OBSERVED" else execution
    hdu_before = writer.get("hdu_before", {})
    hdu_after = writer.get("hdu_after", {})
    target_before = writer.get("target_before") or {}
    target_after = writer.get("target_after") or {}
    new_receipt = record["new_after_writer_exit"]
    new = decoded(new_receipt)
    if new_receipt is not None and not observed(new, expected_path.with_name("export.fits")):
        execution = "FAILED"
    row = dict(
        case_id=record["case_id"], mode=record["mode"], path=record["access"],
        boundary=record["boundary"], repeat=record["case_id"].split("-r")[-1] if "-r" in record["case_id"] else "",
        execution=execution, original_verdict=state, original_diff=diff,
        writer_memmap_requested=record["memmap"],
        writer_array_mapped=writer.get("mapping", {}).get("array_backed"),
        hdu_before=hdu_before.get("value"), hdu_after=hdu_after.get("value"),
        hdu_dtype=hdu_before.get("dtype"), hdu_writeable=hdu_before.get("writeable"),
        hdu_unit=writer.get("hdu_unit"), target_before=target_before.get("value"),
        target_after=target_after.get("value"), target_dtype=target_before.get("dtype"),
        target_writeable=target_before.get("writeable"), quantity_unit=writer.get("quantity_unit"),
        shares_hdu=writer.get("shares_hdu"), shares_call_input=writer.get("shares_call_input"),
        write_status=actions.get("write", {}).get("state", "skipped"),
        quantity_exception=actions.get("quantity", {}).get("exception"), write_exception=actions.get("write", {}).get("exception"),
        flush_status=actions.get("flush", {}).get("state", "not_called"),
        flush_warning=" | ".join(w["message"] for w in actions.get("flush", {}).get("warnings", [])),
        close_status=actions.get("close", {}).get("state"), writer_exit=record["writer"]["exit_code"],
        writer_pid=writer.get("pid"), original_path=original,
        original_before_sha256=record["baseline_sha256"], original_unit=last.get("unit"), BUNIT=last.get("bunit"),
        original_pixel_hex=last.get("raw_pixel_hex"), original_after_sha256=last.get("sha256"),
        original_header_sha256=last.get("header_sha256"), original_data_sha256=last.get("data_sha256"),
        new_path=new.get("path"), new_pixel=new.get("value"), new_unit=new.get("unit"),
        new_sha256=new.get("sha256"), new_reader_exit=new_receipt["exit_code"] if new_receipt else None,
    )
    for name in PHASES:
        row[f"original_{name}"] = values[name].get("value")
        row[f"reader_{name}_exit"] = readings[name]["exit_code"] if name in readings else None
        row[f"reader_{name}_pid"] = values[name].get("pid")
    return row


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_suite(group, work, output, jobs):
    environment = check_environment()
    work = work.resolve()
    output = output.resolve()
    work.mkdir()
    output.mkdir()
    baseline = work / "baseline.fits"
    baseline_receipt = generate_fixture(baseline)
    baseline_value = decoded(baseline_receipt)
    (output / "baseline-reader.json").write_text(json_text(baseline_receipt, indent=2), encoding="utf-8")
    environment["filesystem"] = capture(["stat", "-f", "-c", "%T", work], work)
    (output / "runtime.json").write_text(json_text(environment, indent=2), encoding="utf-8")
    if group == "matrix":
        heap = capture(child_args("probe.py", "heap"), work)
        probes = decoded(heap)
        if (not probes or not probes[0]["shares_memory"]
                or probes[0]["original_after"]["value"] != FIXTURE["replacement"]
                or probes[0]["unit"] != FIXTURE["unit"]):
            raise RuntimeError(f"native positive control failed: {heap}")
        preflight = run_one(baseline, work, ("PF-FITS", "copyonwrite", "quantity", "close", True))
        (output / "preflight.json").write_text(json_text({"heap": heap, "fits": preflight}, indent=2),
                                               encoding="utf-8")
    specs = list(matrix_cases()) if group == "matrix" else CONTROLS
    with ThreadPoolExecutor(max_workers=jobs) as executor:
        collected = list(executor.map(lambda spec: run_one(baseline, work, spec), specs))
    (output / f"{group}.jsonl").write_text("".join(json_text(row) for row in collected), encoding="utf-8")
    rows = [summarize(row, baseline_value) for row in collected]
    write_csv(output / ("persistence.csv" if group == "matrix" else "controls.csv"), rows)
    shutil.copyfile(baseline, output / "baseline.fits")
    print(json_text(dict(group=group, rows=len(rows),
                         execution_status=sorted(set(row["execution"] for row in rows)),
                         original_verdict=sorted(set(row["original_verdict"] for row in rows)),
                         baseline_sha256=sha_file(baseline))), end="")
    return int(any(row["execution"] == "FAILED" for row in rows))


def replay(group, receipts, output):
    file = receipts / f"{group}.jsonl"
    collected = [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines()]
    baseline = decoded(json.loads((receipts / "baseline-reader.json").read_text(encoding="utf-8")))
    specs = list(matrix_cases()) if group == "matrix" else CONTROLS
    expected = [spec[0] for spec in specs]
    if baseline["sha256"] != FIXTURE["sha256"] or [row["case_id"] for row in collected] != expected:
        raise RuntimeError("baseline or case order is missing or doesn't match the frame")
    rows = [summarize(row, baseline) for row in collected]
    write_csv(output, rows)
    print(json_text(dict(group=group, cases=len(rows), receipts_sha256=sha_file(file),
                         fixture_sha256=baseline["sha256"], output_sha256=sha_file(output),
                         failures=[r["case_id"] for r in rows if r["execution"] != "OBSERVED"])), end="")
    return int(any(row["execution"] == "FAILED" for row in rows))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    run.add_argument("group", choices=("matrix", "controls"))
    run.add_argument("--work", type=Path, required=True)
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--jobs", type=int, default=4)
    repeat = commands.add_parser("replay")
    repeat.add_argument("group", choices=("matrix", "controls"))
    repeat.add_argument("--receipts", type=Path, required=True)
    repeat.add_argument("--output", type=Path, required=True)
    commands.add_parser("heap")
    writer = commands.add_parser("writer")
    writer.add_argument("case_id")
    writer.add_argument("file", type=Path)
    writer.add_argument("mode", choices=tuple(MODES))
    writer.add_argument("access")
    writer.add_argument("boundary", choices=tuple(BOUNDARIES))
    writer.add_argument("memmap", choices=("0", "1"))
    args = parser.parse_args()
    if args.command == "run":
        return run_suite(args.group, args.work, args.output, args.jobs)
    if args.command == "replay":
        return replay(args.group, args.receipts, args.output)
    if args.command == "heap":
        heap_preflight()
    else:
        write_case(args.case_id, args.file, args.mode, args.access, args.boundary, args.memmap == "1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
