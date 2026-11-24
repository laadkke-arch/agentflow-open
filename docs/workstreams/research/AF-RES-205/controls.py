#!/usr/bin/env python3
"""Collect controls and counterexamples outside the 32 primary matrix cells."""

import argparse
import mmap
import os
from pathlib import Path
import sys
import tempfile

from probe import check, child_receipt, compare_output, describe, emit, observed_call, write_jsonl


HERE = Path(__file__).resolve().parent
EXPECTED = [0, 1, 2]


def numpy_control(kind):
    import numpy as np

    source = np.array(EXPECTED, dtype=np.int64)
    source.setflags(write=kind != "readonly_view")
    output = source.copy() if kind == "copy" else source.view()
    result = compare_output(output, EXPECTED, source.tolist, bool(np.shares_memory(source, output)),
                            not source.flags.writeable, 99)
    expected = {
        "copy": (False, True, False),
        "mutable_view": (True, True, True),
        "readonly_view": (True, False, None),
    }
    classification = result["shares_original"], result["writeable"], result["mutation"]["propagated"]
    check(result["values_match"] and classification == expected[kind], f"{kind} control failed")
    return dict(status="PASS", numpy=np.__version__, input_writeable=bool(source.flags.writeable), output=result)


def numpy_strict(kind):
    import numpy as np

    source = list(EXPECTED) if kind == "list" else np.array(EXPECTED, dtype=np.int64)
    ndarray = isinstance(source, np.ndarray)
    if kind == "readonly":
        source.setflags(write=False)
    dtype = np.float64 if kind == "cast" else None
    output, error = observed_call(lambda: np.asarray(source, dtype=dtype, copy=False))
    details = dict(numpy=np.__version__, source=describe(source) if ndarray else source,
                   call="np.asarray(source, dtype=target, copy=False)", target_dtype="float64" if dtype else None)
    if error:
        return dict(details, status="BEHAVIOR_ERROR", exception=error)
    result = compare_output(output, EXPECTED, source.tolist, bool(np.shares_memory(source, output)),
                            not source.flags.writeable, 99)
    return dict(details, status="RETURNED", output=result)


def arrow_direct(kind):
    import numpy as np
    import pyarrow as pa

    original = pa.array(EXPECTED, type=pa.int64())
    raw = np.frombuffer(original.buffers()[1], dtype=np.int64)
    writable = kind == "writable"
    output = original.to_numpy(zero_copy_only=not writable, writable=writable)
    shares = bool(np.shares_memory(raw, output))
    result = compare_output(output, EXPECTED, original.to_pylist, shares, shares, 99)
    check(result["values_match"] and result["writeable"] == writable and shares != writable,
          f"Arrow direct control failed: {kind}")
    return dict(status="PASS", numpy=np.__version__, pyarrow=pa.__version__, output=result)


def mmap_control(kind):
    import numpy as np

    access = {"shared": mmap.ACCESS_WRITE, "private": mmap.ACCESS_COPY, "readonly": mmap.ACCESS_READ}
    with tempfile.TemporaryFile() as backing:
        backing.write(bytes(EXPECTED))
        backing.flush()
        fd = backing.fileno()
        with mmap.mmap(fd, 3, access=mmap.ACCESS_READ) as observer, mmap.mmap(fd, 3, access=access[kind]) as target:
            source = np.frombuffer(observer, dtype=np.uint8)
            output = np.frombuffer(target, dtype=np.uint8)
            before = list(os.pread(fd, 3, 0))
            result = compare_output(output, EXPECTED, source.tolist,
                                    bool(np.shares_memory(source, output)), False, 99)
            if kind == "shared":
                target.flush()
            after = list(os.pread(fd, 3, 0))
            del output, source
    expected = {"shared": True, "private": False, "readonly": None}
    check(result["values_match"] and result["mutation"]["propagated"] == expected[kind],
          f"mmap {kind} write propagation differed")
    check((after != before) == (kind == "shared"), f"mmap {kind} file modification differed")
    return dict(status="PASS", numpy=np.__version__, mode=kind, backing_before=before,
                backing_after=after, output=result)


def collect(work, output):
    plan = []
    for env in ("H01", "H04"):
        plan.extend((env, f"CTRL-{env}-{case}", "numpy", case)
                    for case in ("copy", "mutable_view", "readonly_view"))
        plan.extend((env, f"STRICT-{env}-{case}", "strict", case)
                    for case in ("alias", "readonly", "list", "cast"))
    plan.extend(("H04", f"ARROW-{case}", "arrow", case) for case in ("readonly", "writable"))
    plan.extend(("H04", f"MMAP-{case}", "mmap", case) for case in ("shared", "private", "readonly"))

    rows = []
    for env, receipt_id, group, case in plan:
        env_work = work / env
        python = env_work / "venv" / "bin" / "python"
        for repetition in (1, 2):
            rows.append(child_receipt(f"{receipt_id}.r{repetition}",
                                      [python, __file__, group, case], env_work, os.environ))
    for env in ("H02", "H04"):
        env_work = work / env
        python = env_work / "venv" / "bin" / "python"
        for fixture in ("H1", "H2", "H3", "H4"):
            for repetition in (1, 2):
                rows.append(child_receipt(f"TRACE-{env}-{fixture}.r{repetition}",
                    [python, HERE / "probe.py", "one", fixture, "column", "--trace-intermediate"],
                    env_work, os.environ))
    env_work = work / "A04"
    python = env_work / "venv" / "bin" / "python"
    for repetition in (1, 2):
        rows.append(child_receipt(f"A04-A3-implicit.false.r{repetition}",
            [python, HERE / "probe.py", "one", "A3", "false", "--implicit-dtype"],
            env_work, os.environ))
    write_jsonl(output, rows)
    print(f"{len(rows)} supplemental subprocess receipts at {output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    group = commands.add_parser("collect")
    group.add_argument("--work", type=Path, required=True)
    group.add_argument("--output", type=Path, required=True)
    controls = {
        "numpy": numpy_control,
        "strict": numpy_strict,
        "arrow": arrow_direct,
        "mmap": mmap_control,
    }
    for name in controls:
        commands.add_parser(name).add_argument("case")
    args = parser.parse_args()
    if args.action == "collect":
        collect(args.work.resolve(), args.output.resolve())
        return 0
    result = controls[args.action](args.case)
    emit(result)
    return 10 if result["status"] == "BEHAVIOR_ERROR" else 0


if __name__ == "__main__":
    raise SystemExit(main())
