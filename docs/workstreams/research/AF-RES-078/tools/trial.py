"""Execute the AF-RES-078 cells and preserve commands, states and artifact bytes."""

from __future__ import annotations

import argparse
import base64
from collections import Counter
import os
from pathlib import Path
import select
import shutil
import signal
import stat
import subprocess
import sys
from tempfile import TemporaryDirectory
import time
from zipfile import ZipFile

from fixturegen import CELLS, OWNED, digest, json_lines, make_database, read_lines, utc, write_originals
from oracle import csv_middle, image_conditions, image_expectation, source_table, stage_images, table_final, zip_members

SCRIPTS = Path(__file__).resolve().parent
PY_IMG = os.environ.get("AF078_PY_IMAGE", sys.executable)
PY_CSV = os.environ.get("AF078_PY_CSV", shutil.which("python3.13") or "")
SQLITE = os.environ.get("AF078_SQLITE", shutil.which("sqlite3") or "")
ZIP = os.environ.get("AF078_ZIP", shutil.which("zip") or "")
UNZIP = os.environ.get("AF078_UNZIP", shutil.which("unzip") or "")
ACTOR = "AF-RES-078 작업자 / codex-cloud"
ROOT_ENV = dict(os.environ, TZ="UTC", LC_ALL="C.UTF-8")
for key in ("ZIPOPT", "ZIP", "UNZIPOPT", "UNZIP"):
    ROOT_ENV.pop(key, None)
QUERY = "SELECT row_key, cell FROM work ORDER BY row_key;"
TYPED_QUERY = (
    "SELECT row_key, CASE WHEN cell IS NULL THEN 'N' "
    "ELSE 'T' || hex(CAST(cell AS BLOB)) END AS cell FROM work ORDER BY row_key;"
)


class Artifacts:
    def __init__(self, path):
        self.path = path
        self.items = {r["sha256"]: r for r in read_lines(path)} if path.exists() else {}

    def add(self, content):
        value = {"sha256": digest(content), "bytes": len(content)}
        if value["sha256"] not in self.items:
            self.items[value["sha256"]] = dict(value, base64=base64.b64encode(content).decode("ascii"))
        return value

    def save(self):
        self.path.write_text(json_lines(self.items[k] for k in sorted(self.items)), encoding="utf-8")


def command_version():
    result = {}
    for label, args in {
        "sqlite": [SQLITE, "--version"], "csv": [PY_CSV, "-B", "-c", "import csv,sys; print(sys.version, csv.QUOTE_NOTNULL)"],
        "pillow": [PY_IMG, "-B", "-c", "import PIL,sys; print(PIL.__version__, sys.version)"],
        "zip": [ZIP, "-v"], "unzip": [UNZIP, "-v"],
    }.items():
        probe = subprocess.run(args, capture_output=True, text=True, timeout=8,
                               env=environment(label == "sqlite"))
        if probe.returncode:
            raise RuntimeError((label, probe.returncode, probe.stderr))
        result[label] = {"argv": args, "exit": probe.returncode, "stdout": probe.stdout,
                         "binary_sha256": digest(Path(args[0]).resolve().read_bytes())}
    return result


def environment(sqlite=False):
    if sqlite and "AF078_SQLITE_LIB" in os.environ:
        return dict(ROOT_ENV, LD_LIBRARY_PATH=os.environ["AF078_SQLITE_LIB"])
    return ROOT_ENV


class Run:
    def __init__(self, artifacts, root, cell, scenario, attempt, fixture):
        self.artifacts = artifacts
        self.root = root
        self.data = {
            "run": f"{cell}.{scenario}.{attempt}", "cell": cell, "domain": fixture["domain"],
            "scenario": scenario, "attempt": attempt, "fixture": fixture["id"],
            "actor": ACTOR, "start_utc": utc(), "events": [], "snapshots": {},
            "environment": {"LC_ALL": "C.UTF-8", "TZ": "UTC", "sqlite_ld_library_path": os.environ.get("AF078_SQLITE_LIB")},
        }

    def event(self, stage, args, cwd, start, code, out, err, given, gate=None):
        entry = {
            "stage": stage, "argv": [str(a) for a in args], "cwd": str(cwd),
            "start_utc": start, "end_utc": utc(), "exit": code,
            "process_started": True, "stdin": self.artifacts.add(given) if given is not None else None,
            "stdout": self.artifacts.add(out), "stderr": self.artifacts.add(err),
            "stderr_text": err.decode("utf-8", "replace"),
        }
        if gate:
            entry["gate"] = gate
        self.data["events"].append(entry)
        return code, out

    def run(self, stage, argv, cwd=None, given=None, sqlite=False):
        cwd = cwd or self.root
        start = utc()
        proc = subprocess.run(argv, cwd=cwd, input=given, capture_output=True, timeout=15, env=environment(sqlite))
        return self.event(stage, argv, cwd, start, proc.returncode, proc.stdout, proc.stderr, given)

    def snapshot(self, name):
        items = {}
        for path in sorted(self.root.rglob("*")):
            attrs = path.stat()
            relative = path.relative_to(self.root).as_posix()
            if stat.S_ISREG(attrs.st_mode):
                items[relative] = dict(self.artifacts.add(path.read_bytes()), mtime_ns=attrs.st_mtime_ns)
            elif stat.S_ISFIFO(attrs.st_mode):
                items[relative] = {"kind": "fifo"}
            elif stat.S_ISDIR(attrs.st_mode):
                items[relative] = {"kind": "directory"}
        self.data["snapshots"][name] = items
        return items

    def finish(self, expected, middle, final, phase_status):
        required = final["conditions"]
        failed = [name for name, good in required.items() if not good]
        # An indeterminate or intentionally interrupted run has no current complete product.
        self.data.update(end_utc=utc(), expected=expected, middle=middle, final=final,
                         phase_status=phase_status, adoption=(not failed and phase_status == "complete"))
        self.data["first_loss"] = {
            key: "front" if not middle.get("conditions", {}).get(key, True) else "back/publication"
            for key in failed
        }
        return self.data


def optional(path):
    return path.read_bytes() if path.is_file() else None


def until(test, seconds=4):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        value = test()
        if value:
            return value
        time.sleep(0.008)
    raise TimeoutError("Child never reached the recorded stop point")


def stop_csv(record, args):
    start = utc()
    with subprocess.Popen(args, cwd=record.root, env=ROOT_ENV, stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        try:
            if not select.select([p.stdout], [], [], 5)[0]:
                raise TimeoutError("No CSV checkpoint")
            checkpoint = p.stdout.readline()
            if checkpoint != b"checkpoint: first row fsynced\n":
                raise RuntimeError(f"Wrong CSV checkpoint: {checkpoint!r}")
            record.snapshot("at_downstream_checkpoint")
            p.terminate()
            p.wait(timeout=5)
            out, err = p.communicate()
        finally:
            if p.poll() is None:
                p.kill()
                p.wait()
    return record.event("back", args, record.root, start, p.returncode, checkpoint + out, err, b"",
                        {"kind": "actual SIGTERM", "pid": p.pid, "point": "Python after first JSONL row flush+fsync, before replace"})


def pipe_wait(p):
    proc_dir = Path("/proc") / str(p.pid)
    try:
        if not (proc_dir / "exe").samefile(ZIP):
            return None
        wchan = (proc_dir / "wchan").read_text().strip()
        return wchan if "pipe" in wchan else None
    except FileNotFoundError:
        return None


def stop_zip(record, args, cwd, member_list):
    start = utc()
    with subprocess.Popen(args, cwd=cwd, env=ROOT_ENV, stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        try:
            p.stdin.write(member_list)
            p.stdin.flush()
            wchan = until(lambda: pipe_wait(p))
            record.snapshot("at_downstream_checkpoint")
            p.terminate()
            p.wait(timeout=5)
            out, err = p.communicate()
        finally:
            if p.poll() is None:
                p.kill()
                p.wait()
    return record.event("back", args, cwd, start, p.returncode, out, err, member_list,
                        {"kind": "actual SIGTERM", "pid": p.pid, "wchan": wchan,
                         "point": "Info-ZIP native -@ waits for stdin EOF; before archive temp creation"})


def csv_options(null_value, query, framing=False):
    headers = ".headers on"
    if framing:
        headers = ".headers off\n.print row_key,cell"
    return f'.bail on\n.mode csv\n{headers}\n.nullvalue "{null_value}"\n{query}\n'.encode("utf-8")


def sqlite_export(record, db, destination, null_value, query=QUERY, framing=False):
    args = [SQLITE, "-batch", "-bail", "-readonly", "-init", "/dev/null", db]
    code, out = record.run("front", args, given=csv_options(null_value, query, framing), sqlite=True)
    destination.write_bytes(out)
    return code


def consume_argv(mid, final, mode, py=PY_CSV, pause=False):
    args = [py, "-B", SCRIPTS / "consume.py", mid, final, mode]
    if pause:
        args.append("--pause")
    return args


def run_table(record, fixture, registry, stop=False, typed=False, query=None, framing=False):
    root = record.root
    db, mid, final = root / "source.db", root / "exchange.csv", root / "final.jsonl"
    if not db.exists():
        make_database(db, fixture)
    if record.data["scenario"] == "retry" and stop:
        old = registry["t-old"]
        old_input = root / "previous.csv"
        old_input.write_bytes(b"row_key,cell\r\nold-cert,previous release\r\n")
        result, _ = record.run("prior", consume_argv(old_input, final, "excel"))
        if result != 0 or not all(table_final(final.read_bytes(), old)["conditions"].values()):
            raise RuntimeError("Could not stage earlier successful table artifact")
    pre = record.snapshot("before_front")
    expected = source_table(db, fixture)
    col = "NULL" if record.data["cell"][1:2] == "1" else ""
    reader = "notnull" if record.data["cell"][2:] == "1" else "excel"
    if typed:
        reader = "typed"
    code = sqlite_export(record, db, mid, col, query or (TYPED_QUERY if typed else QUERY), framing)
    record.snapshot("after_front")
    middle = csv_middle(mid.read_bytes(), fixture, typed=typed)
    args = consume_argv(mid, final, reader, pause=stop)
    if code != 0:
        disposition = "front_failed"
    elif stop:
        stop_csv(record, args)
        disposition = "interrupted"
    else:
        status, _ = record.run("back", args)
        disposition = "complete" if status == 0 else "back_failed"
    post = record.snapshot("after_back")
    record.data["originals_unchanged"] = pre["source.db"]["sha256"] == post["source.db"]["sha256"]
    record.data["bytes"] = {"original": db.stat().st_size, "middle": mid.stat().st_size,
                            "final": final.stat().st_size if final.exists() else None}
    record.data["transport"] = {"nullvalue": col, "reader": reader, "typing_adapter": typed}
    return record.finish(expected, middle, table_final(optional(final), fixture), disposition)


def zip_args(target, temp, junk, listed=True):
    args = [ZIP, "-X", "-q", "-b", temp]
    if junk:
        args.append("-j")
    if listed:
        args.append("-@")
    return args + [target]


def member_bytes(names):
    return ("".join(name + "\n" for name in names)).encode("utf-8")


def convert_argv(source, stage, names, flat, direction="normalize", mtime=1650000000):
    return [PY_IMG, "-B", SCRIPTS / "convert.py", source, stage, "flat" if flat else "keep",
            *names, "--direction", direction, "--mtime", str(mtime)]


def run_image(record, fixture, registry, stop=False, direction="normalize", repair=None, mtime=1650000000):
    root = record.root
    source, stage, target, temp = (root / p for p in ("source", "stage", "artifact.zip", "zip-temp"))
    temp.mkdir(exist_ok=True)
    stage.mkdir(exist_ok=True)
    if not source.exists():
        write_originals(source, fixture)
    if record.data["scenario"] == "retry" and stop:
        old = registry["i-old"]
        old_path = root / "previous"
        write_originals(old_path, old)
        for f in old_path.rglob("*.png"):
            os.utime(f, (1580000000, 1580000000))
        assert_old = [r["path"] for r in old["images"]]
        status, _ = record.run("prior", zip_args(target, temp, False), old_path, member_bytes(assert_old))
        if status != 0 or [r["name"] for r in zip_members(target.read_bytes())["members"]] != assert_old:
            raise RuntimeError("Could not stage earlier valid ZIP")
    pre = record.snapshot("before_front")
    expected = image_expectation(source, fixture)
    names = sorted(expected)
    flat = record.data["cell"][1:2] == "1"
    junk = record.data["cell"][2:] == "1"
    code, reports = record.run("front", convert_argv(source, stage, names, flat, direction, mtime))
    record.snapshot("after_front")
    stage_data = stage_images(stage)
    middle = {"members": stage_data, "conditions": image_conditions(stage_data, expected),
              "conversion_output": reports.decode("utf-8", "replace")}
    given = member_bytes([r["name"] for r in stage_data])
    output = root / "new.zip" if repair == "fresh" else target
    args = zip_args(output, temp, junk)
    if code != 0:
        disposition = "front_failed"
    elif stop:
        stop_zip(record, args, stage, given)
        disposition = "interrupted"
    else:
        status, _ = record.run("back", args, stage, given)
        if status == 0 and repair == "fresh":
            record.snapshot("before_adapter_replace")
            os.replace(output, target)
        disposition = "complete" if status == 0 else "back_failed"
    out = optional(target)
    decoded = zip_members(out, "utf-8" if repair == "utf8" else None, extract=names)
    decoded["conditions"] = image_conditions(decoded["members"], expected, decoded["accessed_by_name"])
    if out is not None:
        zstatus, zout = record.run("oracle_unzip", [UNZIP, "-Z", "-1", target])
        decoded["unzip_cli"] = {"exit": zstatus, "names": zout.decode("utf-8", "backslashreplace").splitlines()}
    else:
        decoded["unzip_cli"] = None
    post = record.snapshot("after_back")
    keys = [key for key in pre if key.startswith("source/") and "sha256" in pre[key]]
    record.data["originals_unchanged"] = all(pre[key]["sha256"] == post[key]["sha256"] for key in keys)
    record.data["bytes"] = {"original": sum(pre[k]["bytes"] for k in keys),
                            "middle": sum(r["bytes"] for r in stage_data), "final": None if out is None else len(out)}
    record.data["transport"] = {"flat": flat, "junk": junk, "direction": direction, "adapter": repair, "mtime": mtime}
    return record.finish(expected, middle, decoded, disposition)


def solo_runs(artifacts, registry):
    rows = []
    for column in (0, 1):
        with TemporaryDirectory(prefix="af078-solo-") as temp:
            root = Path(temp)
            fixture = registry["t-normal"]
            # The writer's input omits the coincident literal NULL.
            input_fixture = dict(fixture, rows=[r for r in fixture["rows"] if r["role"] != "literal"])
            record = Run(artifacts, root, f"T{column}x", "solo-writer", 0, input_fixture)
            db, csv = root / "source.db", root / "solo.csv"
            make_database(db, input_fixture)
            code = sqlite_export(record, db, csv, "NULL" if column else "")
            record.data.update(expected=source_table(db, input_fixture), parsed=csv_middle(csv.read_bytes(), input_fixture),
                               status=code, utc=utc(), bytes_in=db.stat().st_size, bytes_out=csv.stat().st_size)
            record.snapshot("after")
            rows.append(record.data)
        with TemporaryDirectory(prefix="af078-solo-") as temp:
            root = Path(temp)
            fixture = registry["t-normal"]
            record = Run(artifacts, root, f"Tx{column}", "solo-reader", 0, fixture)
            manual = b'row_key,cell\r\nnull,\r\nempty,""\r\nliteral,NULL\r\npunct,"a,""b""\r\nline"\r\n'
            csv, final = root / "manual.csv", root / "final.jsonl"
            csv.write_bytes(manual)
            code, _ = record.run("back", consume_argv(csv, final, "notnull" if column else "excel"))
            record.data.update(authored_csv=manual.decode(), parsed=optional(final).decode() if final.exists() else None,
                               status=code, utc=utc(), bytes_in=len(manual), bytes_out=final.stat().st_size if final.exists() else None)
            record.snapshot("after")
            rows.append(record.data)
        with TemporaryDirectory(prefix="af078-solo-") as temp:
            root = Path(temp)
            fixture = registry["i-normal"]
            singleton = dict(fixture, images=[fixture["images"][1]])
            record = Run(artifacts, root, f"I{column}x", "solo-converter", 0, singleton)
            source, stage = root / "source", root / "stage"
            write_originals(source, singleton)
            expected = image_expectation(source, singleton)
            code, _ = record.run("front", convert_argv(source, stage, list(expected), bool(column)))
            images = stage_images(stage)
            record.data.update(expected=expected, parsed=images, status=code, utc=utc(),
                               bytes_in=next(source.rglob("*.png")).stat().st_size, bytes_out=sum(r["bytes"] for r in images))
            record.snapshot("after")
            rows.append(record.data)
        with TemporaryDirectory(prefix="af078-solo-") as temp:
            root = Path(temp)
            fixture = registry["i-normal"]
            singleton = dict(fixture, images=[fixture["images"][1]])
            record = Run(artifacts, root, f"Ix{column}", "solo-zip", 0, singleton)
            write_originals(root / "manual", singleton)
            name = singleton["images"][0]["path"]
            source = root / "manual" / name
            os.utime(source, (1650000000, 1650000000))
            target = root / "solo.zip"
            code, _ = record.run("back", zip_args(target, root, bool(column)), root / "manual", member_bytes([name]))
            record.data.update(member_list=[name], parsed=zip_members(optional(target)), status=code, utc=utc(),
                               bytes_in=source.stat().st_size, bytes_out=target.stat().st_size if target.exists() else None)
            record.snapshot("after")
            rows.append(record.data)
    return rows


def experiment(artifacts, registry, phase):
    for domain, cells in CELLS.items():
        handler = run_table if domain == "T" else run_image
        for cell in cells:
            scenario = "edge" if phase == "edge" else "normal"
            fixture = registry[domain.lower() + "-" + scenario]
            for attempt in (1, 2):
                with TemporaryDirectory(prefix=f"af078-{cell}-{scenario}-") as tmp:
                    record = Run(artifacts, Path(tmp), cell, scenario, attempt, fixture)
                    yield handler(record, fixture, registry)
            if phase == "main":
                with TemporaryDirectory(prefix=f"af078-{cell}-retry-") as tmp:
                    root = Path(tmp)
                    stopped = Run(artifacts, root, cell, "retry", "stop", fixture)
                    yield handler(stopped, fixture, registry, stop=True)
                    resumed = Run(artifacts, root, cell, "retry", "resume", fixture)
                    yield handler(resumed, fixture, registry)


def diagnose(artifacts, registry):
    t_normal, i_normal = (registry[key] for key in ("t-normal", "i-normal"))
    cases = [
        ("T01", "zero_default", registry["t-empty"], {}),
        ("T01", "zero_framed", registry["t-empty"], {"framing": True}),
        ("T01", "zero_failed_query", registry["t-empty"], {"query": "SELECT nonexistent FROM work;"}),
        ("T01", "nul_text", registry["t-nul"], {}),
        ("T00", "typed_adapter", registry["t-nul"], {"typed": True}),
        ("I00", "raw_orientation_tag", i_normal, {"direction": "raw"}),
        ("I00", "stale_orientation_tag", i_normal, {"direction": "stale"}),
        ("I00", "same_meaning_different_dates", i_normal, {"mtime": 1720000000}),
        ("I00", "utf8_reader_adapter", registry["i-edge"], {"repair": "utf8"}),
    ]
    for cell, scenario, fixture, options in cases:
        with TemporaryDirectory(prefix=f"af078-diag-{scenario}-") as tmp:
            record = Run(artifacts, Path(tmp), cell, scenario, 1, fixture)
            handler = run_table if fixture["domain"] == "T" else run_image
            yield handler(record, fixture, registry, **options)
    with TemporaryDirectory(prefix="af078-diag-fresh-") as tmp:
        root = Path(tmp)
        stop = Run(artifacts, root, "I00", "retry", "stop", i_normal)
        baseline = run_image(stop, i_normal, registry, stop=True)
        baseline.update(run="I00.fresh_adapter.stop", scenario="fresh_adapter")
        yield baseline
        record = Run(artifacts, root, "I00", "fresh_adapter", "resume", i_normal)
        yield run_image(record, i_normal, registry, repair="fresh")
    with TemporaryDirectory(prefix="af078-diag-python312-") as tmp:
        root = Path(tmp)
        source, target = root / "hand.csv", root / "final.jsonl"
        hand = b'row_key,cell\r\nnull,\r\nempty,""\r\n'
        source.write_bytes(hand)
        f = {"id": "t-reader-version", "domain": "T", "rows": [
            {"key": "null", "role": "null", "value": None}, {"key": "empty", "role": "empty", "value": ""}]}
        record = Run(artifacts, root, "T01", "reader_version312", 1, f)
        record.snapshot("before_front")
        code, _ = record.run("back", consume_argv(source, target, "notnull", py=PY_IMG))
        record.snapshot("after_back")
        yield record.finish(f["rows"], csv_middle(hand, f), table_final(optional(target), f),
                            "complete" if code == 0 else "back_failed")
    with TemporaryDirectory(prefix="af078-diag-emptyzip-") as tmp:
        root = Path(tmp)
        target = root / "donothing.zip"
        record = Run(artifacts, root, "I00", "zip_empty", 1, {"id": "i-empty", "domain": "I"})
        pre = record.snapshot("before_front")
        code, _ = record.run("back", zip_args(target, root, False), given=b"")
        failed = zip_members(optional(target))
        with ZipFile(root / "defined-empty.zip", "w"):
            pass
        valid = zip_members((root / "defined-empty.zip").read_bytes())
        record.snapshot("after_back")
        record.data.update(expected={"members": 0}, middle={"conditions": {}}, final={
            "conditions": {"empty_created_by_zip": failed["readable"], "legal_empty_zip": valid["readable"]},
            "zip_empty": failed, "stdlib_empty": valid}, end_utc=utc(), phase_status=f"Info-ZIP exit {code}",
            adoption=None, first_loss={})
        yield record.data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, choices=("versions", "solo", "main", "edge", "diag"))
    parser.add_argument("--out", type=Path, default=OWNED)
    args = parser.parse_args()
    out = args.out.resolve()
    (out / "evidence").mkdir(parents=True, exist_ok=True)
    artifacts = Artifacts(out / "evidence/artifacts.jsonl")
    if args.phase == "versions":
        import json
        result = command_version()
        (out / "evidence/runtime-versions.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        for name, proof in result.items():
            print(name, proof["stdout"].splitlines()[0])
        return
    registry = {item["id"]: item for item in read_lines(OWNED / "fixtures.jsonl")}
    if args.phase == "solo":
        rows = solo_runs(artifacts, registry)
        selected = out / "evidence/solo.jsonl"
    elif args.phase == "diag":
        rows = list(diagnose(artifacts, registry))
        selected = out / "evidence/diagnostics.jsonl"
    else:
        rows = list(experiment(artifacts, registry, args.phase))
        selected = out / "runs.jsonl"
        if selected.exists():
            preserved = [r for r in read_lines(selected)
                         if (r["scenario"] == "edge") == (args.phase != "edge")]
            rows = sorted(preserved + rows, key=lambda r: r["run"])
    artifacts.save()
    selected.write_text(json_lines(rows), encoding="utf-8")
    print(f"{args.phase}: {len(rows)} retained rows; {sum(len(r['events']) for r in rows)} subprocesses")
    print(Counter(r.get("phase_status") or str(r.get("status")) for r in rows))


if __name__ == "__main__":
    main()
