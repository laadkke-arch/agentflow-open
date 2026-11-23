"""Replay AF-RES-055 from publisher-checksum-pinned archives."""
import argparse
from collections import Counter, defaultdict
import csv
from datetime import date, datetime, timedelta, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import sqlite3
import subprocess
import sys
import tarfile
from time import perf_counter_ns
import zipfile
import zoneinfo

ROOT = Path(__file__).resolve().parent
INPUT = json.loads((ROOT / "inputs.json").read_text())
ARCHIVES = INPUT["archives"]
PAIRS = INPUT["pairs"]
WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
ZIC = shutil.which("zic")
ZDUMP = shutil.which("zdump")
STRACE = shutil.which("strace")
TZ_ENV = {**os.environ, "LC_ALL": "C", "TZ": "UTC0", "PYTHONTZPATH": "", "TZDIR": ""}
zoneinfo.reset_tzpath(())
GTFS_FIELDS = {
    "routes.txt": ("route_id",),
    "calendar.txt": ("service_id", *WEEKDAYS, "start_date", "end_date"),
    "calendar_dates.txt": ("service_id", "date", "exception_type"),
    "trips.txt": ("trip_id", "route_id", "service_id"),
    "stop_times.txt": ("trip_id", "stop_sequence", "stop_id", "arrival_time", "departure_time"),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def ms(start):
    return round((perf_counter_ns() - start) / 1_000_000, 3)


def compact(record):
    return json.dumps(record, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def json_out(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def jsonl_out(path, records):
    path.write_text("".join(compact(row) + "\n" for row in records))


def execute(command, receipts, **kwargs):
    started, begin = now(), perf_counter_ns()
    run = subprocess.run(command, capture_output=True, check=False, timeout=90, **kwargs)
    receipts.append({
        "command": command, "cwd": str(kwargs.get("cwd", Path.cwd())), "started_utc": started,
        "exit_code": run.returncode, "wall_ms": ms(begin),
        "stdout_sha256": sha(run.stdout), "stderr_sha256": sha(run.stderr),
        "stdout": run.stdout.decode(errors="replace"), "stderr": run.stderr.decode(errors="replace"),
    })
    if run.returncode:
        raise RuntimeError(f"{shlex.join(command)} returned {run.returncode}: {run.stderr.decode(errors='replace')}")
    return run.stdout


def verified_archive(path, tag):
    data = path.read_bytes()
    info = ARCHIVES[tag]
    if len(data) != info["bytes"] or sha(data) != info["sha256"] or hashlib.sha512(data).hexdigest() != info["sha512"]:
        raise ValueError(f"{tag}: publisher archive identity mismatch at {path}")
    return data


def compile_archive(cache, tag, directory, receipts):
    path = cache / f"tzdata{tag}.tar.gz"
    data = verified_archive(path, tag)
    source = directory / "source"
    tzif = directory / "tzif"
    source.mkdir(parents=True)
    tzif.mkdir()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as arc:
        for member, identity in ARCHIVES[tag]["members"].items():
            if not arc.getmember(member).isfile():
                raise ValueError(f"{tag}: expected regular member {member}")
            extracted = arc.extractfile(member).read()
            if sha(extracted) != identity["sha256"] or len(extracted) != identity["bytes"]:
                raise ValueError(f"{tag}: wrong contents for {member}")
            (source / member).write_bytes(extracted)
    if (source / "version").read_text().strip() != tag:
        raise ValueError(f"{tag}: version mismatch")
    execute([ZIC, "-b", "slim", "-d", str(tzif), *INPUT["compile_members"]], receipts, cwd=source, env=TZ_ENV)
    return {"tag": tag, "archive": str(path), "source": source, "tzif": tzif}


def tz_path(built, key):
    root = built["tzif"].resolve()
    path = root / key
    if not path.is_file() or not path.resolve().is_relative_to(root):
        raise ValueError(f"compiled TZif missing or outside directory: {path}")
    return path


def instant(iso):
    parsed = datetime.fromisoformat(iso)
    if parsed.utcoffset() != timedelta(0):
        raise ValueError(f"required UTC instant: {iso}")
    return parsed


def from_file(path, key, at):
    with path.open("rb") as raw:
        if raw.read(4) != b"TZif":
            raise ValueError(f"bad TZif: {path}")
        raw.seek(0)
        zone = zoneinfo.ZoneInfo.from_file(raw, key=key)
        actual_path = raw.name
    local = at.astimezone(zone)
    return {"offset_s": int(local.utcoffset().total_seconds()),
            "wall": local.replace(tzinfo=None).isoformat(timespec="seconds"), "abbr": local.tzname()}, actual_path


def dump_offset(token):
    if not re.fullmatch(r"[+-](?:\d{2}){1,3}", token):
        raise ValueError(f"unexpected zdump offset: {token}")
    hh, mm, ss = (int((token[1:] + "0000")[i:i+2]) for i in (0, 2, 4))
    return (-1 if token[0] == "-" else 1) * (3600 * hh + 60 * mm + ss)


def from_zdump(path, at, trace, receipts):
    epoch = int(at.timestamp())
    cmd = [STRACE, "-f", "-e", "trace=openat,openat2", "-s", "400", "-o", str(trace),
           ZDUMP, "-i", "-t", f"{epoch},{epoch + 1}", str(path)]
    report = execute(cmd, receipts, env=TZ_ENV).decode()
    data = [line.split("\t") for line in report.splitlines() if "\t" in line]
    if len(data) != 1 or len(data[0]) < 3 or data[0][:2] != ["-", "-"]:
        raise ValueError(f"expected a singleton interval without an exact transition: {report!r}")
    interval = data[0]
    offset = dump_offset(interval[2])
    # zdump omits the abbreviation when it equals the displayed UTC offset.
    abbr = interval[3] if len(interval) > 3 and interval[3] else interval[2]
    wall = (at + timedelta(seconds=offset)).replace(tzinfo=None).isoformat(timespec="seconds")
    trace_data = trace.read_text()
    opened = []
    for filename in re.findall(r'openat2?\([^\n]*?"(/[^"]+)"[^\n]*?\) = \d+', trace_data):
        with open(filename, "rb") as trace_target:
            if trace_target.read(4) == b"TZif":
                opened.append(filename)
    if opened != [str(path)]:
        raise ValueError(f"zdump opened unexpected TZif files: {opened}")
    evidence = {"stdout": report, "opened_tzif": opened, "trace_path": str(trace),
                "trace_sha256": sha(trace_data.encode()), "epoch_window": [epoch, epoch + 1]}
    return {"offset_s": offset, "wall": wall, "abbr": abbr}, evidence


def read_instants(built, key, instants, directory, receipts):
    path = tz_path(built, key)
    directory.mkdir(parents=True, exist_ok=True)
    readings = []
    for index, iso in enumerate(instants, 1):
        at = instant(iso)
        first, opened = from_file(path, key, at)
        second, evidence = from_zdump(path, at, directory / f"{index}.openat", receipts)
        if first != second:
            raise ValueError(f"{key} {iso}: ZoneInfo {first} vs zdump {second}")
        readings.append({"utc": iso, "value": first, "zoneinfo_opened": opened,
                         "zdump_value": second, "zdump": evidence})
    return {"key": key, "tzif_path": str(path), "tzif_sha256": sha(path.read_bytes()),
            "tzif_header_hex": path.read_bytes()[:5].hex(), "instants": readings, "agree": True}


def source_rows(path, key):
    """Find the complete requested Zone record and all its directly named Rule rows."""
    lines = path.read_text().splitlines()
    rules, zone = defaultdict(list), []
    in_zone = False
    for number, line in enumerate(lines, 1):
        parts = line.partition("#")[0].split()
        if not parts:
            continue
        if parts[0] == "Rule":
            rules[parts[1]].append({"line": number, "row": line})
        if parts[0] == "Zone":
            in_zone = parts[1] == key
            if in_zone:
                zone.append({"line": number, "row": line})
        elif in_zone and line[0].isspace():
            zone.append({"line": number, "row": line})
        else:
            in_zone = False
    if not zone:
        raise ValueError(f"{key}: no Zone found in {path}")
    rule_names = {r["row"].split()[i] for i, r in [(3, zone[0]), *((1, r) for r in zone[1:])]}
    rows = [r for name in sorted(rule_names & rules.keys()) for r in rules[name]] + zone
    return sorted(rows, key=lambda row: row["line"])


def scoped_tzif(receipt, directory, receipts):
    directory.mkdir(parents=True)
    source = directory / "selection.zi"
    source.write_text("".join(row["row"] + "\n" for row in receipt["rows"]))
    bound = {"tzif": directory / "tzif"}
    execute([ZIC, "-b", "slim", "-d", str(bound["tzif"]), str(source)], receipts, env=TZ_ENV)
    result = tz_path(bound, receipt["key"])
    if sha(result.read_bytes()) != receipt["past_tzif_sha256"]:
        raise ValueError("past selection failed the independently pinned full-build TZif digest")
    return bound


def tz_requirement_value(reading, metric):
    if metric == "offset":
        return [r["value"]["offset_s"] for r in reading["instants"]]
    if metric == "local":
        return [[r["value"]["wall"], r["value"]["abbr"]] for r in reading["instants"]]
    raise ValueError(f"unknown metric {metric}")


def gtfs_members(path):
    with zipfile.ZipFile(path) as arc:
        if len(arc.namelist()) != len(set(arc.namelist())):
            raise ValueError("duplicate ZIP members")
        names = set(arc.namelist())
        wanted = set(GTFS_FIELDS) | {"agency.txt", "feed_info.txt", "directions.txt", "frequencies.txt"}
        members = {name: arc.read(name) for name in sorted(names & wanted)}
    mandatory = {"routes.txt", "trips.txt", "stop_times.txt"}
    if not mandatory <= members.keys() or not ({"calendar.txt", "calendar_dates.txt"} & members.keys()):
        raise ValueError("required GTFS inputs absent")
    return members


def csv_dicts(members, name):
    if name not in members:
        return []
    reader = csv.DictReader(io.StringIO(members[name].decode("utf-8-sig"), newline=""))
    if not set(GTFS_FIELDS.get(name, ())) <= set(reader.fieldnames or ()):
        raise ValueError(f"{name}: missing required fields")
    rows = []
    for number, row in enumerate(reader, 2):
        if None in row or None in row.values():
            raise ValueError(f"{name} CSV record {number}: column mismatch")
        rows.append((number, row))
    return rows


def gtfs_python(members, day, route, direction, ignore=()):
    compact_date = day.strftime("%Y%m%d")
    weekday = WEEKDAYS[day.weekday()]
    routes = csv_dicts(members, "routes.txt")
    if len([r for _, r in routes if r["route_id"] == route]) != 1:
        raise ValueError("route key missing or ambiguous")
    all_trips = csv_dicts(members, "trips.txt")
    if len({r["trip_id"] for _, r in all_trips}) != len(all_trips):
        raise ValueError("duplicate trip_id")
    keys = [(n, r) for n, r in all_trips if (r["route_id"], r.get("direction_id") or None) == (route, direction)]
    if not keys:
        raise ValueError("route/direction mapping unavailable; cannot infer service zero")
    calendars = csv_dicts(members, "calendar.txt")
    if len({row["service_id"] for _, row in calendars}) != len(calendars):
        raise ValueError("duplicate calendar.service_id")
    base = [(n, r) for n, r in calendars
            if r["start_date"] <= compact_date <= r["end_date"] and r[weekday] == "1"]
    active = {r["service_id"] for _, r in base}
    exceptions = [(n, r) for n, r in csv_dicts(members, "calendar_dates.txt") if r["date"] == compact_date]
    if len({r["service_id"] for _, r in exceptions}) != len(exceptions):
        raise ValueError("duplicated service/date exception")
    for _, item in exceptions:
        kind = item["exception_type"]
        if kind not in ("1", "2"):
            raise ValueError(f"invalid exception_type {kind}")
        if kind not in ignore:
            if kind == "1":
                active.add(item["service_id"])
            else:
                active.discard(item["service_id"])
    selected = {r["trip_id"]: (n, r["service_id"]) for n, r in keys if r["service_id"] in active}
    stops = defaultdict(list)
    for number, stop in csv_dicts(members, "stop_times.txt"):
        if stop["trip_id"] in selected:
            stops[stop["trip_id"]].append((int(stop["stop_sequence"]), number,
                                           [stop[k] for k in ("stop_id", "arrival_time", "departure_time")]))
    for key in selected:
        if not stops[key] or len({s[0] for s in stops[key]}) != len(stops[key]):
            raise ValueError(f"{key}: absent or non-unique stop_sequence")
    return {
        "members": {key: [s[2] for s in sorted(stops[key])] for key in sorted(selected)},
        "trip_rows": {k: list(selected[k]) for k in sorted(selected)},
        "stop_rows": {k: [s[1] for s in sorted(stops[k])] for k in sorted(selected)},
        "active": sorted(active), "calendar_rows": [n for n, _ in base],
        "exceptions": [[n, r["service_id"], r["exception_type"]] for n, r in exceptions],
    }


def gtfs_sqlite(members, day, route, direction):
    with sqlite3.connect(":memory:") as db:
        for filename, required in GTFS_FIELDS.items():
            table = filename.removesuffix(".txt")
            columns = (*required, "direction_id") if table == "trips" else required
            db.execute(f"CREATE TABLE {table} (" + ",".join(f"{col} TEXT" for col in columns) + ")")
            if filename not in members:
                continue
            content = csv.reader(io.StringIO(members[filename].decode("utf-8-sig"), newline=""))
            header = next(content)
            indexes = [header.index(col) if col in header else None for col in columns]
            db.executemany(f"INSERT INTO {table} VALUES (" + ",".join("?" for _ in columns) + ")",
                           ([row[i] if i is not None else None for i in indexes] for row in content if row))
        weekday = WEEKDAYS[day.weekday()]
        dates = {"d": day.strftime("%Y%m%d"), "route": route, "direction": direction}
        selected = f"""
            WITH base AS (
                SELECT service_id FROM calendar
                WHERE :d BETWEEN start_date AND end_date AND {weekday} = '1'
                UNION
                SELECT service_id FROM calendar_dates WHERE date = :d AND exception_type = '1'
            ), active AS (
                SELECT service_id FROM base
                EXCEPT
                SELECT service_id FROM calendar_dates WHERE date = :d AND exception_type = '2'
            ), chosen AS (
                SELECT DISTINCT trips.trip_id FROM trips
                JOIN active USING (service_id) JOIN routes USING (route_id)
                WHERE route_id = :route AND NULLIF(direction_id, '') IS :direction
            )
        """
        count = db.execute(selected + "SELECT COUNT(*) FROM chosen", dates).fetchone()[0]
        rows = db.execute(selected + """
            SELECT trip_id, stop_id, arrival_time, departure_time
            FROM chosen JOIN stop_times USING (trip_id)
            ORDER BY trip_id, CAST(stop_sequence AS INTEGER)
        """, dates)
        collection = {}
        for trip_id, *fields in rows:
            collection.setdefault(trip_id, []).append(fields)
        if count != len(collection):
            raise ValueError("SQLite trips without complete join")
        return count, collection


def gtfs_replay(path, day, route, direction):
    members = gtfs_members(path)
    feed_info = csv_dicts(members, "feed_info.txt")
    if len(feed_info) > 1:
        raise ValueError("ambiguous feed_info")
    if feed_info:
        bounds = feed_info[0][1]
        service_day = day.strftime("%Y%m%d")
        lower, upper = bounds.get("feed_start_date"), bounds.get("feed_end_date")
        if (lower and service_day < lower) or (upper and service_day > upper):
            raise ValueError(f"{day}: outside declared feed bounds {lower} to {upper}")
    joined = gtfs_python(members, day, route, direction)
    count, independently = gtfs_sqlite(members, day, route, direction)
    if count != len(joined["members"]) or independently != joined["members"]:
        raise ValueError("Python and SQLite regional service trip sets differ")
    return {"route": route, "direction": direction, "service_date": day.isoformat(),
            "archive": str(path), "archive_sha256": sha(path.read_bytes()),
            "member_sha256": {name: sha(content) for name, content in members.items()},
            "count": count, **joined, "sqlite_count": count, "sqlite_members": independently,
            "feed_info_bounds": {k:feed_info[0][1].get(k) for k in ("feed_start_date","feed_end_date")} if feed_info else None,
            "independent_agreement": True}


def gtfs_control_zip(path, changed):
    # A constructed GTFS control, outside the publication sample.
    files = {
        "agency.txt": "agency_id,agency_name,agency_url,agency_timezone\nX,Control,https://example.org,America/New_York\n",
        "routes.txt": "route_id,agency_id,route_short_name,route_type\nR,X,R,3\n",
        "stops.txt": "stop_id,stop_name,stop_lat,stop_lon\nS1,One,42.3,-71.0\nS2,Two,42.4,-71.1\n",
        "calendar.txt": ("service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n"
                         "WK,1,1,1,1,1,0,0,20240101,20240131\n"
                         "CANCEL,1,0,0,0,0,0,0,20240101,20240131\n"),
        "calendar_dates.txt": "service_id,date,exception_type\nCANCEL,20240108,2\nSPECIAL,20240108,1\n",
    }
    middle, late = ("renumbered", "replacement") if changed else ("middle", "late")
    trips = [(middle, "WK", "08:10:00", "08:20:00"),
             (late, "WK", "25:12:00" if changed else "25:10:00", "25:20:00"),
             ("cancelled", "CANCEL", "06:10:00", "06:20:00"),
             ("extra", "SPECIAL", "07:10:00", "07:20:00")]
    files["trips.txt"] = "route_id,service_id,trip_id,direction_id\n" + "".join(
        f"R,{service},{tid},0\n" for tid, service, _, _ in trips)
    files["stop_times.txt"] = "trip_id,arrival_time,departure_time,stop_id,stop_sequence\n" + "".join(
        f"{tid},{first},{first},S1,1\n{tid},{last},{last},S2,2\n" for tid, _, first, last in trips)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as arc:
        for name, content in files.items():
            arc.writestr(zipfile.ZipInfo(name), content)


def gtfs_controls(directory):
    directory.mkdir()
    old_path, new_path = directory / "old.zip", directory / "new.zip"
    gtfs_control_zip(old_path, changed=False)
    gtfs_control_zip(new_path, changed=True)
    day = date(2024, 1, 8)
    old = gtfs_replay(old_path, day, "R", "0")
    new = gtfs_replay(new_path, day, "R", "0")
    members = gtfs_members(old_path)
    ignore_all = gtfs_python(members, day, "R", "0", ignore=("1", "2"))
    ignore_removal = gtfs_python(members, day, "R", "0", ignore=("2",))
    tomorrow = gtfs_replay(old_path, day + timedelta(days=1), "R", "0")

    def signature(rows):
        return tuple((stop, tuple(map(int, arrival.split(":"))) if arrival else None,
                      tuple(map(int, departure.split(":"))) if departure else None)
                     for stop, arrival, departure in rows)

    old_signatures = {key:signature(rows) for key,rows in old["members"].items()}
    new_signatures = {key:signature(rows) for key,rows in new["members"].items()}
    multiplicity = [Counter(signatures.values()) for signatures in (old_signatures, new_signatures)]
    old_set, new_set = set(old["members"]), set(new["members"])
    unique_matches = [
        [left, right] for left in sorted(old_set-new_set)
        for right in sorted(new_set-old_set) if old_signatures[left] == new_signatures[right]
        and multiplicity[0][old_signatures[left]] == multiplicity[1][new_signatures[right]] == 1
    ]
    assert old["count"] == new["count"] == 3 and old_set != new_set
    assert unique_matches == [["middle", "renumbered"]]
    return {"classification": "constructed; no operator data", "base": old, "edited": new,
            "same_reported_count": True, "same_schedule_multiset": multiplicity[0] == multiplicity[1],
            "id_matches_at_identical_schedule":unique_matches,
            "ignore_both_exceptions": sorted(ignore_all["members"]),
            "ignore_removal_only": sorted(ignore_removal["members"]),
            "wrong_civil_day_following_midnight": sorted(tomorrow["members"])}


def tz_controls(compiled, output, receipts):
    output.mkdir()
    beirut = PAIRS["Z-N"]["zone"]
    instants = PAIRS["Z-N"]["instants"]
    repl = read_instants(compiled["2023c"], beirut, instants, output / "reversion", receipts)
    old = read_instants(compiled["2023a"], beirut, instants, output / "pre-reversion", receipts)
    late = read_instants(compiled["2023b"], beirut, instants, output / "reverted-edition", receipts)
    alias_instants = PAIRS["Z-D"]["instants"]
    cet = {}
    for edition, src in (("2024a", "europe"), ("2024b", "backward")):
        observed = read_instants(compiled[edition], "CET", alias_instants, output / edition, receipts)
        decl = [
            [i, line] for i, line in enumerate((compiled[edition]["source"] / src).read_text().splitlines(), 1)
            if re.match(r"^Zone\s+CET\s|^Link\s+Europe/Brussels\s+CET\s*$", line)
        ]
        cet[edition] = {"source": src, "declaration": decl, "read": observed}

    historical = {
        tag: read_instants(compiled[tag], "Asia/Choibalsan", ["2005-01-15T12:00:00Z"],
                           output / f"historical-{tag}", receipts)
        for tag in ("2024a", "2024b")
    }

    # A client labels its local target as UTC or forces the old TZif behind a same-name key.
    wall_as_utc = read_instants(compiled["2023b"], beirut, ["2023-04-21T00:00:00Z"],
                                output / "wall-as-utc", receipts)
    anchor = [
        read_instants(compiled[edition], beirut, ["2023-04-20T22:00:01Z"],
                      output / f"after-actual-anchor-{edition}", receipts)
        for edition in ("2023a", "2023b")
    ]
    wrong_zone = zoneinfo.ZoneInfo.from_file(io.BytesIO(tz_path(compiled["2023b"], beirut).read_bytes()), key=beirut)
    at = instant(instants[0])
    backwards = at.replace(tzinfo=wrong_zone).astimezone(timezone.utc)
    earlier = read_instants(compiled["2023b"], beirut, ["2023-03-25T23:00:00Z"],
                           output / "original-boundary-new", receipts)
    earlier_old = read_instants(compiled["2023a"], beirut, ["2023-03-25T23:00:00Z"],
                               output / "original-boundary-old", receipts)
    stale = read_instants(compiled["2023a"], beirut, [instants[0]], output / "stale-cache-read", receipts)
    cache_path = output / "wrong-cache"
    cache_path.mkdir()
    shutil.copyfile(compiled["2023a"]["archive"], cache_path / "tzdata2023b.tar.gz")
    try:
        verified_archive(cache_path / "tzdata2023b.tar.gz", "2023b")
    except ValueError as error:
        detected = str(error)
    else:
        raise AssertionError("edition collision not detected")
    return {"reversion": {"2023a": old, "2023b": late, "2023c": repl},
            "same_label_zone_to_link": cet, "choibalsan_historical": historical,
            "utc_controls": {"wall_midnight_mislabeled_utc": wall_as_utc,
                             "actual_boundary_plus_one_second_both":anchor,
                             "original_march_boundary_new":earlier, "original_march_boundary_old":earlier_old,
                             "reversed_operation": {"input": instants[0],"wrong_output":backwards.isoformat(),
                                                    "wrong_applied_offset_s":int(at.replace(tzinfo=wrong_zone).utcoffset().total_seconds()),
                                                    "correct":late["instants"][0]["value"]},
                             "cache_collision": {"stale_retrieval":stale, "wrong":stale["instants"][0]["value"],
                                                 "correct":late["instants"][0]["value"], "detected_by_digest":detected}}}


def run(cache, output, reverse_order=False):
    output.mkdir(parents=True)
    commands = []
    tools = {
        "timestamp_utc": now(), "python": sys.version, "python_path": sys.executable,
        "python_sha256": sha(Path(sys.executable).read_bytes()), "sqlite": sqlite3.sqlite_version,
        "TZPATH": list(zoneinfo.TZPATH), "locale": TZ_ENV["LC_ALL"], "TZ": TZ_ENV["TZ"],
    }
    for name, executable in (("zic", ZIC), ("zdump", ZDUMP), ("strace", STRACE)):
        if not executable:
            raise RuntimeError(f"required executable missing: {name}")
        version = execute([executable, "--version"], commands).decode().splitlines()[0]
        tools[name] = {"version":version, "path":executable, "sha256":sha(Path(executable).read_bytes())}
    results = []
    order = list(ARCHIVES)
    if reverse_order:
        order.reverse()
    tools["compile_tag_order"] = order
    compiled = {tag: compile_archive(cache, tag, output / "build" / tag, commands) for tag in order}
    past_inputs = {}
    for pair, spec in PAIRS.items():
        if spec["domain"] == "GTFS":
            for metric in ("count", "set"):
                for side, url in zip(("old", "next"), spec["candidate_urls"]):
                    results.append({"run_id": f"{pair}-{metric}-{side}", "pair":pair,"metric":metric,
                                    "side":side, "status":"blocked", "candidate_only_url":url,
                                    "reason":spec["missing"], "executed":False, "independent_agreement":None})
            continue
        version_reading = {}
        for tag in reversed(spec["editions"]) if reverse_order else spec["editions"]:
            started = perf_counter_ns()
            build = compiled[tag]
            reading = read_instants(build, spec["zone"], spec["instants"], output / "reads" / pair / tag, commands)
            member_path = build["source"] / spec["member"]
            rows = source_rows(member_path, spec["zone"])
            reading["ms"] = ms(started)
            reading["archive"] = build["archive"]
            reading["source_member"] = {"name":spec["member"],"path":str(member_path),
                                        "identity": ARCHIVES[tag]["members"][spec["member"]], "rows":rows}
            version_reading[tag] = reading
        past_tag = spec["editions"][0]
        past = version_reading[past_tag]
        past_inputs[pair] = {"key":spec["zone"], "utc":spec["instants"], "source_member":spec["member"],
                             "source_sha256":past["source_member"]["identity"]["sha256"],
                             "past_source_path":str(Path(past["source_member"]["path"]).relative_to(output)),
                             "rows":past["source_member"]["rows"], "past_tzif_sha256":past["tzif_sha256"],
                             "method":"zic -b slim read explicit TZif; signed seconds and UTC + offset",
                             "complete_scope":"all Zone eras and named Rule rows for this key in one member"}
        for metric in ("offset", "local"):
            for side, tag in zip(("old", "next"), spec["editions"]):
                reading = version_reading[tag]
                results.append({"run_id":f"{pair}-{metric}-{side}", "status":"verified", "executed":True,
                                "pair":pair, "side":side, "metric":metric, "edition":tag,
                                "edition_url":ARCHIVES[tag]["official_url"], "edition_sha256":ARCHIVES[tag]["sha256"],
                                "value":tz_requirement_value(reading, metric), "read":reading,
                                "independent_agreement": True})
    contrasts = {"tzdb":tz_controls(compiled, output / "tz-controls", commands),
                 "gtfs":gtfs_controls(output / "gtfs-controls")}
    jsonl_out(output / "runs.jsonl", results)
    json_out(output / "past-inputs.json", past_inputs)
    json_out(output / "contrasts.json", contrasts)
    json_out(output / "commands.json", {"commands":commands, "tools":tools,
                                       "argv":[sys.executable, "-B", *sys.argv]})


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def semantic(row):
    if not row["executed"]:
        return row
    reading = row["read"]
    return {k:v for k,v in row.items() if k != "read"} | {
        "tzif_sha256":reading["tzif_sha256"],
        "source_member":reading["source_member"]["identity"],
        "source_rows":reading["source_member"]["rows"],
        "paths_and_instants":[
            {"utc":x["utc"],"zoneinfo":x["value"],"zdump":x["zdump_value"]} for x in reading["instants"]
        ],
    }


def package_runs(first, second, output):
    (output / "evidence").mkdir(parents=True, exist_ok=True)
    original, repeat = (read_jsonl(directory / "runs.jsonl") for directory in (first, second))
    if len(original) != 16 or len(repeat) != 16:
        raise ValueError("must retain 16 rows including missing slots")
    if [semantic(x) for x in original] != [semantic(x) for x in repeat]:
        raise ValueError("replay semantic mismatch")
    if (first / "past-inputs.json").read_bytes() != (second / "past-inputs.json").read_bytes():
        raise ValueError("repeated past receipt changed")
    jsonl_out(output / "runs.jsonl", [
        a | {"repeat": b, "repeat_equivalence": "matching executed inputs and values" if a["executed"] else "still blocked"}
        for a, b in zip(original, repeat, strict=True)
    ])
    def normalize(value, directory):
        if isinstance(value, str):
            return value.replace(str(directory), "$RUN")
        if isinstance(value, dict):
            return {k: normalize(v, directory) for k, v in value.items() if k != "trace_sha256"}
        if isinstance(value, list):
            return [normalize(v, directory) for v in value]
        return value

    control_results = [normalize(json.loads((p / "contrasts.json").read_text()), p) for p in (first, second)]
    if control_results[0] != control_results[1]:
        raise ValueError("contrast results diverged between replay directories")
    shutil.copyfile(first / "contrasts.json", output / "evidence" / "contrasts.json")
    evidence = {
        "first": json.loads((first / "commands.json").read_text()),
        "repeat": json.loads((second / "commands.json").read_text()),
        "input_contract_sha256":sha((ROOT / "inputs.json").read_bytes()), "script_sha256":sha(Path(__file__).read_bytes()),
        "comparison":{"planned":len(original), "executed":sum(row["executed"] for row in original),
                      "semantic_match":sum(row["executed"] for row in repeat), "blocked":sum(not row["executed"] for row in repeat),
                      "past_inputs_repeat_sha256":sha((second / "past-inputs.json").read_bytes()),
                      "separate_paths":[str(first),str(second)],
                      "controls_normalized_sha256":sha(compact(control_results[0]).encode()),
                      "controls_match":True},
    }
    json_out(output / "evidence" / "receipts.json", evidence)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    replay = sub.add_parser("run")
    replay.add_argument("--cache", type=Path, required=True)
    replay.add_argument("--output", type=Path, required=True)
    replay.add_argument("--reverse-order", action="store_true")
    compare = sub.add_parser("package")
    compare.add_argument("--first", type=Path, required=True)
    compare.add_argument("--second", type=Path, required=True)
    compare.add_argument("--output", type=Path, required=True)
    gtfs = sub.add_parser("gtfs")
    gtfs.add_argument("zip", type=Path)
    gtfs.add_argument("service_date", type=date.fromisoformat)
    gtfs.add_argument("route")
    gtfs.add_argument("direction", choices=("0", "1", "missing"))
    args = parser.parse_args()
    if args.operation == "run":
        run(args.cache.resolve(), args.output.resolve(), args.reverse_order)
    elif args.operation == "package":
        package_runs(args.first.resolve(), args.second.resolve(), args.output.resolve())
    else:
        print(json.dumps(gtfs_replay(args.zip.resolve(), args.service_date, args.route,
                                     None if args.direction == "missing" else args.direction),
                         ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
