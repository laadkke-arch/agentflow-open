"""Replay the two frozen public table cells in fresh, traced subprocesses."""

import argparse
import csv
import io
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import date, datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

from independent import calculate as independent_calculation

TASK = Path(__file__).resolve().parent
STAT_FIELDS = ("BX_CASE_COUNT", "BK_CASE_COUNT")
MISSING = {"", "NA", ":"}
WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


def utc():
    return datetime.now(timezone.utc).isoformat()


def canonical(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(data):
    return sha256(data).hexdigest()


class AccessDetected(Exception):
    """Signals the exact field lookup in the separate diagnostic process."""


class GuardedRecord(dict):
    def __init__(self, values, trap):
        super().__init__(values)
        self.trap = trap

    def __getitem__(self, field):
        if field == self.trap:
            raise AccessDetected(field)
        return super().__getitem__(field)


class InputReader:
    def __init__(self, root, paths, trap):
        self.root = root
        self.paths = set(paths)
        self.trap = trap
        self.opens = []
        self.keys = []
        self.scan = Counter()

    def rows(self, path):
        data = (self.root / path).read_bytes()
        self.opens.append({"path": path, "mode": "table", "bytes": len(data)})
        stream = io.StringIO(data.decode("utf-8"), newline="")
        parser = csv.reader(stream, strict=True)
        header = next(parser)
        if len(header) != len(set(header)):
            raise ValueError(f"Duplicate header in {path}")
        for cells in parser:
            if len(cells) != len(header):
                raise ValueError(f"Unexpected row width in {path}:{parser.line_num}")
            values = dict(zip(header, cells, strict=True))
            if self.trap and [path, parser.line_num] == self.trap[:2]:
                values = GuardedRecord(values, self.trap[2])
            yield (path, parser.line_num, values)

    def header(self, path):
        raw = bytearray()
        with (self.root / path).open("rb", buffering=0) as handle:
            for byte in iter(lambda: handle.read(1), b""):
                raw.extend(byte)
                if byte == b"\n":
                    break
        header = next(csv.reader([raw.decode("utf-8")], strict=True))
        self.opens.append({"path": path, "mode": "header", "bytes": len(raw), "header_columns": len(header)})

    def values(self, row, *fields, scan=False):
        path, line, values = row
        selected = {field: values[field] for field in fields}
        if scan:
            for field in fields:
                self.scan[(path, field)] += 1
        else:
            self.keys.append({"path": path, "line": line, "fields": selected})
        return selected

    def scan_receipt(self):
        return [{"path": path, "field": field, "count": count}
                for (path, field), count in sorted(self.scan.items())]


def install_audit(root, names):
    permitted = {str(root / name) for name in names}

    def audit(event, args):
        if event == "open" and (args[0] not in permitted or args[2] & os.O_ACCMODE != os.O_RDONLY):
            raise PermissionError(f"Open outside the analysis allowlist: {args[0]}")
        if event.startswith("socket."):
            raise PermissionError("The analysis process accepts local files only")

    sys.addaudithook(audit)


def rounded(value):
    return ((value + 50) // 100) * 100 if value is not None else None


def statistic(reader, spec):
    key = date.fromisoformat(spec["date"]).strftime("%m/%d/%Y")
    contributors = []
    matched = False
    for row in reader.rows("statistics.csv"):
        if reader.values(row, "date_of_interest", scan=True)["date_of_interest"] != key:
            continue
        if matched:
            raise ValueError(f"Repeated statistics key: {key}")
        matched = True
        selected = reader.values(row, *STAT_FIELDS)
        valid = {field: int(value) for field, value in selected.items() if value not in MISSING}
        if valid:
            contributors.append({"path": row[0], "line": row[1], "key": key, "fields": valid})
    valid = contributors[0]["fields"] if contributors else {}
    raw = sum(valid.values()) if valid else None
    output = {
        "id": f"S-BXBK-{spec['date']}", "raw": raw, "report": rounded(raw),
        "valid": len(valid), "contributors": contributors, "unit": "persons",
    }
    transform = {"kind": "sum-round", "increment": 100, "tie": "up", "keys": [key],
                 "fields": list(STAT_FIELDS), "missing": sorted(MISSING)}
    return output, transform


def services(reader, day):
    key = day.strftime("%Y%m%d")
    weekday = WEEKDAYS[day.weekday()]
    active = set()
    if "calendar.txt" in reader.paths:
        for row in reader.rows("calendar.txt"):
            fields = reader.values(row, "service_id", "start_date", "end_date", weekday)
            if fields["start_date"] <= key <= fields["end_date"] and fields[weekday] == "1":
                active.add(fields["service_id"])
    if "calendar_dates.txt" in reader.paths:
        for row in reader.rows("calendar_dates.txt"):
            exception = reader.values(row, "date", "service_id", "exception_type")
            if exception["date"] == key:
                if exception["exception_type"] == "1":
                    active.add(exception["service_id"])
                elif exception["exception_type"] == "2":
                    active.discard(exception["service_id"])
                else:
                    raise ValueError(f"Invalid exception_type in {row[0]}:{row[1]}")
    return active


def transit(reader, spec):
    route = spec["route"]
    direction = spec["direction"]
    matches = [row[1] for row in reader.rows("routes.txt") if reader.values(row, "route_id")["route_id"] == route]
    if len(matches) != 1:
        raise ValueError(f"Expected one route record for {route!r}")
    active = services(reader, date.fromisoformat(spec["date"]))
    contributors = []
    rejected_direction = []
    for row in reader.rows("trips.txt"):
        gate = reader.values(row, "route_id", "service_id")
        if gate["route_id"] != route or gate["service_id"] not in active:
            continue
        trip = reader.values(row, "trip_id", "direction_id")
        if trip["direction_id"] == direction:
            contributors.append({"path": row[0], "line": row[1], "key": trip["trip_id"], "fields": gate | trip})
        else:
            rejected_direction.append({"line": row[1], "trip_id": trip["trip_id"], "direction_id": trip["direction_id"]})
    ids = sorted({item["key"] for item in contributors})
    output = {"id": f"T-{route}-{spec['date']}-D{direction}", "raw": len(ids), "report": len(ids),
              "trips": ids, "contributors": contributors, "unit": "trip IDs"}
    transform = {"kind": "active-direction-distinct", "route": route, "route_line": matches[0], "direction": direction,
                 "date": spec["date"], "active": sorted(active), "rejected_direction": rejected_direction}
    return output, transform


def child(root, spec):
    install_audit(root, spec["paths"])
    reader = InputReader(root, spec["paths"], spec.get("trap"))
    try:
        if spec["probe"]:
            reader.header(spec["probe"])
        analysis = statistic if spec["domain"] == "S" else transit
        output, transform = analysis(reader, spec)
    except AccessDetected:
        print(canonical({"diagnostic_trapped": spec["trap"]}))
        return 19
    print(canonical({"opens": reader.opens, "key_reads": reader.keys, "field_scans": reader.scan_receipt(),
                     "transform": transform, "output": output}))
    return 0


def checked_payload(cache, descriptor, cap, fetch):
    path = cache / descriptor["cache_name"]
    if not path.exists() and fetch:
        with urlopen(descriptor["url"], timeout=25) as response:
            payload = response.read(cap + 1)
        if len(payload) != descriptor["size_bytes"] or digest(payload) != descriptor["sha256"]:
            raise ValueError(f"Download did not match the pinned object: {descriptor['url']}")
        path.write_bytes(payload)
    if path.stat().st_size > cap:
        raise ValueError(f"File exceeded the scope cap: {path}")
    payload = path.read_bytes()
    if len(payload) != descriptor["size_bytes"] or digest(payload) != descriptor["sha256"]:
        raise ValueError(f"Cached bytes do not match the publisher pin: {path}")
    return payload


def bundle(domain, descriptor, cache, fetch):
    if domain == "S":
        return {"statistics.csv": checked_payload(cache, descriptor, 262144, fetch)}
    raw = checked_payload(cache, descriptor, 131072, fetch)
    with ZipFile(io.BytesIO(raw)) as archive:
        result = {}
        for info in archive.infolist():
            pin = descriptor["members"][info.filename]
            if info.file_size > 131072 or Path(info.filename).name != info.filename or info.filename in result:
                raise ValueError(f"Invalid member in frozen GTFS ZIP: {info.filename}")
            member = archive.read(info)
            if len(member) != pin["size_bytes"] or digest(member) != pin["sha256"]:
                raise ValueError(f"Unexpected member bytes: {info.filename}")
            result[info.filename] = member
        if result.keys() != descriptor["members"].keys():
            raise ValueError("GTFS member inventory did not match")
    return result


def edit_cell(data, line, field, change):
    """Modify one plain-text cell while retaining all other bytes."""
    rows = data.splitlines(keepends=True)
    header = rows[0].decode("utf-8").rstrip("\r\n").split(",")
    before = rows[line - 1]
    value_bytes = before.rstrip(b"\r\n")
    if b'"' in value_bytes:
        raise ValueError("Controlled edit requires an unquoted target row")
    cells = value_bytes.decode("utf-8").split(",")
    column = header.index(field)
    old = cells[column]
    new = change(old)
    if new == old or any(character in new for character in ',\r\n"'):
        raise ValueError("Expected exactly one logical field change")
    cells[column] = new
    rows[line - 1] = ",".join(cells).encode() + before[len(value_bytes):]
    return b"".join(rows), {"line": line, "field": field, "old": old, "new": new}


def add_count(delta):
    return lambda value: str(int(value) + delta)


def stage_main(truth, chosen, base):
    domain = truth["domain"]
    condition = int(truth["condition"])
    path = truth["candidate_path"]
    line = chosen["selected_line"] if domain == "S" else chosen[
        "filtered_trip_line" if condition == 4 else "primary_trip_line"]
    original = "statistics.csv" if domain == "S" else "trips.txt"
    payload = dict(base)
    probe = None
    preparation = []
    if condition == 2:
        payload[path] = payload[original]
        preparation.append({"path": path, "kind": "byte-identical unopened copy", "from": original})
    if condition == 3:
        probe = path
        auxiliary_field = "QN_CASE_COUNT" if domain == "S" else "trip_headsign"
        auxiliary_edit = add_count(2) if domain == "S" else lambda value: value + " [PROBE]"
        payload[path], detail = edit_cell(payload[original], line, auxiliary_field, auxiliary_edit)
        preparation.append({"path": path, "kind": "header-only modified control", **detail})
    target = {"path": path, "line": line, "field": truth["field"],
              "key": chosen["csv_key"] if domain == "S" else chosen[
                  "filtered_trip" if condition == 4 else "primary_trip"]}
    config = {"domain": domain, "date": chosen["date"], "probe": probe}
    if domain == "T":
        config.update(route=chosen["route"], direction=chosen["direction"])
    return payload, config, target, preparation


def trace_summary(trace, root):
    events = {}
    network = []
    for line in trace.splitlines():
        if re.search(r"\b(?:socket|connect)\(", line):
            network.append(line.strip())
        if str(root) + "/" not in line:
            continue
        operation = re.search(r"\b(openat2?|open|read|pread64|mmap)\(", line)
        return_value = re.search(r" = (\d+)(?:[< ]|$)", line)
        relative = re.search(re.escape(str(root)) + r'/([^">]+)', line)
        if not (operation and return_value and relative):
            raise ValueError(f"Unparsed fixture syscall: {line}")
        path = relative.group(1)
        state = events.setdefault(path, {"opens": 0, "read_calls": 0, "read_bytes": 0, "mmap_calls": 0})
        call = operation.group(1)
        if call.startswith("open"):
            state["opens"] += 1
        elif call in {"read", "pread64"}:
            state["read_calls"] += 1
            state["read_bytes"] += int(return_value.group(1))
        else:
            state["mmap_calls"] += 1
    return {"by_path": events, "network_calls": network}


def job_command(root, config):
    return [sys.executable, "-B", str(Path(__file__).resolve()), "--child", str(root), canonical(config)]


def run_job(run_id, parent, edition, config, payload, target, preparation, expected, *,
            diagnostic=False, structural=None):
    started_at = utc()
    with tempfile.TemporaryDirectory(prefix=f"af-res-051-{run_id}-") as workspace:
        root = Path(workspace) / "files"
        root.mkdir()
        for name, data in sorted(payload.items()):
            file = root / name
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(data)
        config = config | {"paths": sorted(payload)}
        trace_path = Path(workspace) / "strace.txt"
        command = ["strace", "-f", "-qq", "-yy", "-s", "1", "-e",
                   "trace=open,openat,openat2,read,pread64,mmap,socket,connect", "-o", str(trace_path)]
        command += job_command(root, config)
        result = subprocess.run(command, check=True, cwd=root, capture_output=True, text=True)
        receipt = json.loads(result.stdout)
        trace = trace_summary(trace_path.read_text(), root)
        os_paths = set(trace["by_path"])
        app_paths = {entry["path"] for entry in receipt["opens"]}
        if os_paths != app_paths or trace["network_calls"]:
            raise AssertionError(f"OS/application scope differed for {run_id}: {trace}")
        for entry in receipt["opens"]:
            path = entry["path"]
            counts = trace["by_path"][path]
            expected_reads = entry["bytes"] if entry["mode"] == "header" else None
            if (counts["opens"] != 1 or counts["read_bytes"] != entry["bytes"] or counts["mmap_calls"]
                    or (expected_reads is not None and counts["read_calls"] != expected_reads)):
                raise AssertionError(f"OS bytes did not match the recorded mode for {run_id}: {trace}")
        audit = independent_calculation(root, config)
        for key in ("raw", "report", "trips", "valid"):
            if key in expected and (audit[key] != expected[key] or receipt["output"][key] != expected[key]):
                raise AssertionError(f"{run_id}:{key} differs from the sealed expectation {expected[key]!r}")
        lookup = None
        if diagnostic:
            coordinates = [target["path"], target["line"], target["field"]]
            tested = subprocess.run(job_command(root, config | {"trap": coordinates}),
                                    cwd=root, capture_output=True, text=True)
            expected_trap = structural["key_read"] == "yes"
            if tested.returncode not in {0, 19} or (tested.returncode == 19) != expected_trap:
                raise AssertionError(f"Field guard differed for {run_id}: {tested.returncode} {tested.stderr}")
            if tested.returncode == 19 and json.loads(tested.stdout)["diagnostic_trapped"] != coordinates:
                raise AssertionError(f"Unexpected diagnostic coordinates for {run_id}")
            lookup = {"method": "separate subprocess; dict subscription traps exact path/row/field",
                      "exit_code": tested.returncode, "trapped": expected_trap, "coordinates": coordinates}
    object_pin = edition["sha256"] if config["domain"] == "S" else edition["members"]["trips.txt"]["sha256"]
    visible = {path: {"sha256": digest(data), "bytes": len(data)} for path, data in sorted(payload.items())}
    return {"run_id": run_id, "parent_run_id": parent, "truth_id": structural["truth_id"] if structural else None,
            "domain": config["domain"], "condition": int(structural["condition"]) if structural else None,
            "edition_source_id": edition["source_id"], "edition": edition["edition"], "publisher_url": edition["url"],
            "distribution_sha256": edition["distribution"]["sha256"], "publisher_file_sha256": object_pin,
            "target": target, "visible": visible, "preparation": preparation, "receipt": receipt,
            "os": trace, "independent": audit | {"field_trap": lookup, "method": "separate SQL and plain line parser"},
            "start_utc": started_at, "end_utc": utc(), "coverage": "complete-for-staged-regular-files-and-explicit-lookup",
            "exit_code": result.returncode}


def pair_edit(domain, condition, selected, target, baseline):
    if not selected:
        if domain == "S":
            return "QN_CASE_COUNT", add_count(1)
        return "trip_headsign", lambda value: value + " [CONTROL]"
    if domain == "S":
        expectation = baseline["paired_selected_expected"][f"S{condition}"]
        return target["field"], add_count(int(expectation["after"]) - int(expectation["before"]))
    if condition == 4:
        return target["field"], lambda value: value + "_AF_ALT"
    return target["field"], lambda value: "1" if value == "0" else "0"


def main_runs(inputs, baseline, originals, truths):
    for truth in truths:
        run = truth["run_id"]
        domain = truth["domain"]
        condition = int(truth["condition"])
        edition = inputs[domain]["main"]
        base = baseline["primary"][domain]
        payload, config, target, preparation = stage_main(
            truth, inputs["selection"][domain], originals[(domain, "main")])
        observation = run_job(run, None, edition, config, payload, target, preparation, base,
                              diagnostic=True, structural=truth)
        yield observation
        for selected, tag in [(True, "SEL"), (False, "NON")]:
            field, change = pair_edit(domain, condition, selected, target, baseline)
            path = target["path"]
            revised, edit = edit_cell(payload[path], target["line"], field, change)
            expected = baseline["paired_selected_expected"][f"{domain}{condition}"] if selected else base
            variant = run_job(f"{run}-{tag}", run, edition, config, payload | {path: revised}, target,
                              preparation + [{"path": path, "kind": tag, **edit}], expected)
            yield variant


def sensitivity_runs(inputs, baseline, originals):
    for run, expected in baseline["other_predictions"].items():
        domain, edition = expected["domain"], expected["edition"]
        config = {"domain": domain, "date": expected["date"], "probe": None}
        if domain == "T":
            config.update(route=expected["route"], direction=expected["direction"])
        payload = dict(originals[(domain, edition)])
        preparation = []
        if run == "S-A-MISS":
            path = "statistics.csv"
            payload[path], edit = edit_cell(payload[path], inputs["selection"]["S"]["selected_line"],
                                             "BX_CASE_COUNT", lambda value: "")
            preparation.append({"path": path, "kind": "blank one selected field", **edit})
        yield run_job(run, expected["parent"], inputs[domain][edition], config, payload, None, preparation, expected)


def replay(args):
    if not shutil.which("strace"):
        raise SystemExit("strace is required for independently measured open/read coverage")
    start = utc()
    evidence = TASK / "evidence"
    inputs = json.loads((evidence / "inputs.json").read_text())
    baseline = json.loads((evidence / "baseline.json").read_text())
    with (TASK / "truth.csv").open(newline="") as f:
        truths = list(csv.DictReader(f))
    args.cache.mkdir(parents=True, exist_ok=True)
    originals = {
        (domain, name): bundle(domain, asset, args.cache, args.fetch)
        for domain in ["S", "T"] for name, asset in inputs[domain].items()
    }
    runs = list(main_runs(inputs, baseline, originals, truths))
    runs.extend(sensitivity_runs(inputs, baseline, originals))
    args.output.mkdir(parents=True, exist_ok=True)
    ledger = args.output / "runs.jsonl"
    ledger.write_text("".join(canonical(row) + "\n" for row in runs), encoding="utf-8")
    receipt = {
        "argv": sys.argv, "started_utc": start, "ended_utc": utc(), "exit_code": 0,
        "os": platform.platform(), "python": platform.python_version(),
        "strace": subprocess.check_output(["strace", "--version"], text=True).splitlines()[0],
        "main": len(truths), "paired_variants": sum(run["run_id"].endswith(("-SEL", "-NON")) for run in runs),
        "sensitivity": len(baseline["other_predictions"]), "field_trap_processes": len(truths),
        "runs_sha256": digest(ledger.read_bytes()),
    }
    (args.output / "execution.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(canonical(receipt))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--child", nargs=2, metavar=("ROOT", "SPEC"))
    parser.add_argument("--cache", type=Path, help="Directory for the verified original publisher payloads")
    parser.add_argument("--output", type=Path, help="Directory for the run ledger and execution receipt")
    parser.add_argument("--fetch", action="store_true", help="Download missing pinned files before analysis")
    args = parser.parse_args()
    if args.child:
        return child(Path(args.child[0]), json.loads(args.child[1]))
    if args.cache is None or args.output is None:
        parser.error("--cache and --output are required when replaying the panel")
    replay(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
