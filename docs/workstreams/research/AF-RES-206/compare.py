#!/usr/bin/env python3
"""Compare published fixture rows without performing a coordinate transformation."""
import argparse
from collections import Counter
import csv
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import urljoin
import warnings
import zipfile

HERE = Path(__file__).resolve().parent
UNKNOWN = "미확인"
NA = "해당없음"
IDS = {f"TP{i:02}" for i in range(1, 41)}
AXES_IN = ("lat", "lon", "ellipsoid_h")
AXES_OUT = ("E", "N", "H", "flag")
MEMBER_FIELDS = (
    "archive_status", "archive_sha256", "member", "size_bytes", "compressed_bytes", "crc32",
    "sha256", "dos_timestamp", "compression", "flags", "header_offset", "candidate_grid_line_count",
)


@dataclass(frozen=True)
class Row:
    tokens: tuple[str, ...]
    location: str
    full_tokens: tuple[str, ...] = ()


def log(event, **values):
    print(json.dumps({"event": event, **values}, ensure_ascii=False, sort_keys=True), flush=True)


def sha(blob):
    return sha256(blob).hexdigest()


def output_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def curl_get(url, path):
    temporary = path.with_suffix(path.suffix + ".download")
    headers = path.with_suffix(path.suffix + ".headers")
    command = [
        "curl", "--fail", "--silent", "--show-error", "--location", "--max-time", "120",
        "--proto", "=https", "--proto-redir", "=https", "--dump-header", str(headers),
        "--output", str(temporary), "--write-out", "%{json}", url,
    ]
    run = subprocess.run(command, capture_output=True, text=True, check=False)
    metadata = json.loads(run.stdout) if run.stdout else {}
    filtered_headers = []
    if headers.exists():
        for line in headers.read_text(encoding="iso-8859-1").splitlines():
            if line.lower().startswith(("http/", "location:", "content-length:", "content-type:",
                                        "content-encoding:", "etag:", "last-modified:", "date:")):
                filtered_headers.append(line)
    log("http", url=url, exit=run.returncode, stderr=run.stderr.strip(), headers=filtered_headers,
        **{key: metadata.get(key) for key in ("http_code", "http_connect", "url_effective", "size_download",
                                             "content_type", "num_redirects")})
    if run.returncode:
        temporary.unlink(missing_ok=True)
        return None
    temporary.replace(path)
    return metadata


class ResourceLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))


def download_publisher(config, work):
    page = work / "publisher-resources.html"
    page_meta = curl_get(config["resources_url"], page)
    if page_meta is None:
        return None
    parser = ResourceLinks()
    parser.feed(page.read_text(encoding="utf-8"))
    links = {
        urljoin(page_meta["url_effective"], link) for link in parser.links
        if PurePosixPath(link.split("?", 1)[0]).name.lower() == "ostn15-osgm15-developerspack.zip"
    }
    log("publisher_links", page=page_meta["url_effective"], page_bytes=page.stat().st_size,
        page_sha256=sha(page.read_bytes()), historical_target=config["plan_188_url"], full_pack=sorted(links))
    if links != {config["current_link_url"]}:
        raise ValueError("publisher link changed or is ambiguous; inspect the page and pin the new link")
    path = work / "publisher-full.zip"
    metadata = curl_get(next(iter(links)), path)
    return path if metadata is not None else None


def inspect_archive(path, spec):
    """Return member evidence and the test-role mapping, without extracting paths."""
    if path is None:
        return [], {}, None, "publisher_body_unavailable"
    archive_hash = sha(path.read_bytes())
    if not zipfile.is_zipfile(path):
        return [], {}, archive_hash, "not_zip"
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        if len(infos) > 1000 or sum(x.file_size for x in infos) > 256 * 1024 * 1024:
            return [], {}, archive_hash, "archive_size_limit"
        duplicates = [
            name for name, count in Counter(x.filename.casefold() for x in infos).items() if count > 1
        ]
        by_name = {}
        inventory = []
        grids = []
        for item in infos:
            basename = PurePosixPath(item.filename).name
            by_name.setdefault(basename, []).append(item)
            inspect_grid = item.file_size >= 10 * 1024 * 1024 and Path(basename).suffix.lower() in {".txt", ".csv"}
            line_count = 0
            last_byte = b""
            with archive.open(item) as member:
                digest = sha256()
                for block in iter(lambda: member.read(1024 * 1024), b""):
                    digest.update(block)
                    if inspect_grid:
                        line_count += block.count(b"\n")
                        last_byte = block[-1:]
            if inspect_grid:
                line_count += int(last_byte != b"\n")
                if line_count in (876951, 876952):
                    grids.append(item.filename)
            inventory.append(dict(archive_sha256=archive_hash, member=item.filename, size_bytes=item.file_size,
                compressed_bytes=item.compress_size, crc32=f"{item.CRC:08x}", sha256=digest.hexdigest(),
                dos_timestamp="%04d-%02d-%02dT%02d:%02d:%02d" % item.date_time, compression=item.compress_type,
                flags=item.flag_bits, header_offset=item.header_offset,
                candidate_grid_line_count=line_count if inspect_grid else ""))
        required = spec["required_members"]
        unresolved = {role: value for role, value in required.items() if len(by_name.get(value, ())) != 1}
        paths = {role: by_name.get(name, []) for role, name in required.items()}
        log("zip_layout", archive_sha256=archive_hash, bytes=path.stat().st_size,
            entries=len(inventory), duplicate_paths=sorted(duplicates), missing_or_ambiguous=unresolved,
            roles={role: [item.filename for item in items] for role, items in paths.items()},
            full_grid_candidates=grids)
        if duplicates or unresolved or len(grids) != 1:
            return inventory, {}, archive_hash, "wrong_or_ambiguous_layout"
        if spec["current_sha256"] and archive_hash != spec["current_sha256"]:
            return inventory, {}, archive_hash, "different_from_pinned_archive"
        contents = {}
        for role, items in paths.items():
            item = items[0]
            if item.file_size > 2 * 1024 * 1024:
                raise ValueError(f"unexpected fixture size: {item.filename}")
            contents[role] = (item.filename, archive.read(item))
    return inventory, contents, archive_hash, "identified_layout"


def read_fixture(source, content, schema, role, version):
    lines = content.decode("utf-8-sig").splitlines()
    parsed = csv.reader(lines, strict=True)
    header = next(parsed, [])
    if header != schema:
        raise ValueError(f"{source}: header {header!r} differs from planned header {schema!r}")
    places = {
        "forward_input": (11, 11, 3),
        "forward_output": (3, 3, 3, 0),
        "reverse_input": (3, 3, 3),
        "reverse_output": (11, 11, 4, 0),
    }[role]
    fields = schema[2:6] if role == "reverse_output" else schema[1:1 + len(places)]
    rows = []
    for tokens in parsed:
        if not tokens:
            continue
        if len(tokens) != len(header):
            raise ValueError(f"{source}:{parsed.line_num}: wrong number of fields")
        if role == "reverse_output" and tokens[1] != "RESULT":
            if not tokens[1].isdigit():
                raise ValueError(f"{source}:{parsed.line_num}: unknown reverse-output row role")
            continue
        values = tuple(tokens[header.index(field)] for field in fields)
        rows.append((tokens[0], Row(values, f"{source}: L{parsed.line_num}", tuple(tokens))))
    result = keyed_rows(source, version, rows, IDS)
    for row in result.values():
        for value, precision in zip(row.tokens, places):
            pattern = r"[-+]?\d+" + (rf"\.\d{{{precision}}}" if precision else "")
            if re.fullmatch(pattern, value) is None:
                raise ValueError(f"{row.location}: {value!r} has wrong precision for {role}")
    return result


def keyed_rows(source, version, rows, expected):
    counts = Counter((version, point) for point, _ in rows)
    ids = {point for _, point in counts}
    duplicate = sorted(point for (_, point), count in counts.items() if count > 1)
    missing = sorted(expected - ids)
    extra = sorted(ids - expected)
    log("keys", file=source, version=version, rows=len(rows), unique=len(ids),
        missing=missing, duplicate=duplicate, extra=extra)
    if missing or duplicate or extra:
        raise ValueError(f"{source}: invalid point keys")
    return dict(rows)


class ArticleTables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.blocks = []

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            self.depth += 1
            if self.depth == 1:
                self.blocks.append([])

    def handle_endtag(self, tag):
        if tag == "pre":
            self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.blocks[-1].append(data)


def article_data(path, fixed, version):
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8", newline="") as stream:
            snapshot = list(csv.DictReader(stream))
        data = {
            part: [(record["point_id"], Row(tuple(record[f"value{i}"] for i in range(1, 4)),
                                          "X05: rendered L" + record["web_line"]))
                   for record in snapshot if record["table"] == part]
            for part in ("grid", "geographic")
        }
        expected = IDS if len(snapshot) > 2 * len(fixed) else fixed
        quality = "rendered_text_snapshot"
    else:
        document = ArticleTables()
        document.feed(path.read_text(encoding="utf-8"))
        data = {}
        for tokens in ("Eastings", "Latitude"):
            name = "grid" if tokens == "Eastings" else "geographic"
            candidates = ["".join(block) for block in document.blocks if tokens in "".join(block)]
            if len(candidates) != 1:
                raise ValueError(f"X05: {name} table could not be uniquely identified")
            data[name] = []
            for number, line in enumerate(candidates[0].splitlines(), 1):
                match = re.fullmatch(r"\s*(TP\d{2})\s+(\S+)\s+(\S+)\s+(\S+)\s*", line)
                if match:
                    point, *values = match.groups()
                    data[name].append((point, Row(tuple(values), f"X05: {name} block L{number}")))
        expected = IDS
        quality = "downloaded_html"
    tables = {part: keyed_rows(f"X05 {part}", version, rows, expected) for part, rows in data.items()}
    for part, table in tables.items():
        places = (3, 3, 3) if part == "grid" else (10, 10, 3)
        for row in table.values():
            if any(not re.fullmatch(rf"[-+]?\d+\.\d{{{precision}}}", value)
                   for value, precision in zip(row.tokens, places)):
                raise ValueError(f"X05: unexpected precision at {row.location}")
    log("article_snapshot", file=path.name, sha256=sha(path.read_bytes()), form=quality,
        paired_points=len(expected))
    return tables


def t05_vectors(content, geographic, version):
    text = content.decode("utf-8")
    vectors = {}
    for name in ("lat", "lon", "e", "n", "out.e", "out.n"):
        match = re.search(rf"(?m)^{re.escape(name)} <- c\(\s*([-+.0-9,\s]+)\)", text)
        if match is None:
            raise ValueError(f"T05 vector {name} missing")
        values = [(item.group(), text.count("\n", 0, match.start(1) + item.start()) + 1)
                  for item in re.finditer(r"[-+]?\d+\.\d+", match[1])]
        if len(values) != 39:
            raise ValueError(f"T05 vector {name}: expected 39 values, found {len(values)}")
        vectors[name] = values
    by_geo = {}
    for point, row in geographic.items():
        key = tuple(Decimal(n) for n in row.tokens[:2])
        if key in by_geo:
            raise ValueError("T05: geographic match key ambiguous")
        by_geo[key] = point
    standalone = re.search(
        r"list\(([-+0-9.]+), ([-+0-9.]+)\), epsg=27700\)\)\)\s*-\s*c\(([-+0-9.]+), ([-+0-9.]+)\)",
        text,
    )
    forward_single = re.search(
        r"list\(([-+0-9.]+), ([-+0-9.]+)\), epsg=4258\)\)\)\s*-\s*c\(([-+0-9.]+), ([-+0-9.]+)\)",
        text,
    )
    if standalone is None or forward_single is None:
        raise ValueError("T05 standalone fixture missing")
    e, n, lon, lat = standalone.groups()
    point = by_geo[(Decimal(lat), Decimal(lon))]
    f_lon, f_lat, f_e, f_n = forward_single.groups()
    if point != "TP01" or (f_lon, f_lat) != (lon, lat):
        raise ValueError("T05 standalone fixture key differs")
    reverse = [(point, Row((e, n), "T05 L218–219 standalone"))]
    forward = [(point, Row((f_e, f_n), "T05 L230–231 standalone"))]
    for index, (lat_item, lon_item) in enumerate(zip(vectors["lat"], vectors["lon"])):
        key = (Decimal(lat_item[0]), Decimal(lon_item[0]))
        point = by_geo[key]
        for out, prefix in ((reverse, ""), (forward, "out.")):
            ev, el = vectors[prefix + "e"][index]
            nv, nl = vectors[prefix + "n"][index]
            out.append((point, Row((ev, nv), f"T05 L{el}, L{nl}, geographic L{lat_item[1]}/{lon_item[1]}")))
    return {
        "reverse": keyed_rows("T05 reverse input", version, reverse, IDS),
        "forward": keyed_rows("T05 forward expected", version, forward, IDS),
    }


def equal_numeric(a, b):
    return tuple(map(Decimal, a.tokens)) == tuple(map(Decimal, b.tokens))


def signed(a, b):
    delta = Decimal(a) - Decimal(b)
    return f"{delta:+f}" if delta else "0"


def compare_output(inputs, work, files, official, x05, version):
    columns = inputs["columns"]
    replicas = {}
    for id, role in {
        "X15": "forward_input", "X23": "forward_input", "X16": "forward_output",
        "X17": "forward_output", "X20": "reverse_input", "X22": "reverse_input", "X21": "reverse_output",
    }.items():
        replicas[id] = read_fixture(id, files[id], columns[role], role, version)
    for first, second in (("X16", "X17"), ("X20", "X22"), ("X15", "X23")):
        log("mirror_pair", first=first, second=second, byte_equal=files[first] == files[second],
            normalized_all_lines_equal=files[first].splitlines() == files[second].splitlines(),
            token_equal=sum(replicas[first][p].tokens == replicas[second][p].tokens for p in IDS),
            numeric_equal=sum(equal_numeric(replicas[first][p], replicas[second][p]) for p in IDS))
    tables = {
        role: read_fixture(f"OS01/{name}", blob, columns[role], role, version)
        for role, (name, blob) in official.items() if role in columns
    }
    primary_in = tables.get("forward_input", replicas["X15"])
    primary_out = tables.get("forward_output", replicas["X16"])
    reverse_in = tables.get("reverse_input", replicas["X20"])
    t05 = t05_vectors(files["T05"], replicas["X15"], version)
    for role, replica in (("forward_input","X15"),("forward_output","X16"),("reverse_input","X20"),("reverse_output","X21")):
        if role in tables:
            expected = tables[role]
            log("official_vs_copy", role=role, copy=replica,
                key_raw_equal=sum(replicas[replica][p].tokens == expected[p].tokens for p in IDS),
                normalized_entire_file_equal=official[role][1].splitlines() == files[replica].splitlines())
    grid = x05["grid"]
    geo = x05["geographic"]
    quantum = Decimal("0.0000000001")
    log("direction_check", x05_grid_rows=len(grid), x05_geo_rows=len(geo),
        x05_grid_reverse_matches=sum(row.tokens == reverse_in[p].tokens for p, row in grid.items()),
        x05_grid_forward_differences=[p for p, row in grid.items() if row.tokens != primary_out[p].tokens[:3]],
        x05_geo_lat_lon_rounded_matches=sum(tuple(map(Decimal, row.tokens[:2])) ==
            tuple(Decimal(n).quantize(quantum, rounding=ROUND_HALF_UP) for n in primary_in[p].tokens[:2])
            for p, row in geo.items()),
        x05_geo_height_raw_matches=sum(row.tokens[2] == primary_in[p].tokens[2] for p, row in geo.items()),
        t05_reverse_matches=sum(t05["reverse"][p].tokens == reverse_in[p].tokens[:2] for p in IDS),
        t05_forward_matches=sum(t05["forward"][p].tokens == primary_out[p].tokens[:2] for p in IDS))

    rows_188 = list(csv.DictReader(files["B01"].decode("utf-8").splitlines()))
    baseline = {r["slot"]: r for r in rows_188}
    expected_slots = {s: p for s, p in inputs["fixed_slots"].items() if not s.startswith("C")}
    if len(rows_188) != len(expected_slots) or {s:r["point_id"] for s,r in baseline.items()} != expected_slots:
        raise ValueError("AF-RES-188 point slots differ from the approved frame")
    points, deltas = [], []
    for slot, point in inputs["fixed_slots"].items():
        previous = baseline.get(slot)
        a, b = primary_in[point], primary_out[point]
        row = dict(slot=slot, point_id=point, version_key=version, case="requirement" if previous else "conflict",
            official_status="direct" if tables else UNKNOWN,
            official_input_locator=a.location if tables else UNKNOWN,
            official_output_locator=b.location if tables else UNKNOWN,
            previous_slot_locator=f"B01: L{2 + list(baseline).index(slot)}" if previous else NA,
            reference_input=",".join((point,*a.tokens)), reference_output=",".join((point,*b.tokens)),
            reference_input_locator=a.location, reference_output_locator=b.location,
            historical_archive_identity=UNKNOWN, official_point_tolerance=UNKNOWN,
            datum=columns["flag_labels"][b.tokens[-1]])
        prior = (*previous["raw_input_row"].split(",")[1:], *previous["raw_output_row"].split(",")[1:5]) if previous else ()
        for axis, value in zip((*AXES_IN,*AXES_OUT), (*a.tokens,*b.tokens)):
            row[f"reference_{axis}"] = value
            row[f"official_{axis}"] = value if tables else UNKNOWN
        row["versus_188_raw"] = str(prior == (*a.tokens,*b.tokens)).lower() if previous else NA
        row["versus_188_decimal"] = str(tuple(map(Decimal,prior)) ==
            tuple(map(Decimal,(*a.tokens,*b.tokens)))).lower() if previous else NA
        row["versus_188_full_fixture_tokens"] = (
            str(tuple(previous["raw_output_row"].split(",")) == b.full_tokens).lower() if previous else NA
        )
        points.append(row)
        log("point", slot=slot, point=point, official=row["official_status"],
            input=a.location, output=b.location, raw_input=row["reference_input"], raw_output=row["reference_output"],
            raw_vs_188=row["versus_188_raw"], decimal_vs_188=row["versus_188_decimal"])

    fixed = set(inputs["fixed_slots"].values())
    for point in sorted(fixed | set(inputs["supplemental_ids"])):
        for orient, axes in (("forward_input", AXES_IN), ("forward_output", AXES_OUT)):
            is_input = orient == "forward_input"
            reference = (primary_in if is_input else primary_out)[point]
            others = {
                "grid_banger": replicas["X15" if is_input else "X16"][point],
                "sgo": replicas["X23" if is_input else "X17"][point],
                "X05": (geo if is_input else grid)[point],
                "reverse_input": None if is_input else reverse_in[point],
                "T05_reverse_input": None if is_input else t05["reverse"][point],
                "T05_forward_expected": None if is_input else t05["forward"][point],
            }
            for index, axis in enumerate(axes):
                value = reference.tokens[index]
                item = dict(point_id=point, scope="fixed" if point in fixed else "supplemental",
                    direction=orient, axis=axis, unit="degree" if axis in AXES_IN[:2] else
                    ("category" if axis == "flag" else "m"), version_key=version,
                    official_raw=value if tables else UNKNOWN, reference_raw=value, reference_locator=reference.location)
                for name, source in others.items():
                    raw = source.tokens[index] if source and index < len(source.tokens) else None
                    item[f"{name}_raw"] = raw if raw is not None else NA
                    item[f"{name}_location"] = source.location if source else NA
                    if raw is None:
                        difference = NA
                    elif axis == "flag":
                        difference = "equal" if raw == value else "different"
                    else:
                        difference = signed(raw,value)
                    item[f"{name}_minus_reference"] = difference
                    item[f"{name}_raw_equal"] = ("yes" if raw == value else "no") if raw is not None else NA
                deltas.append(item)
    output_csv(work / "points.csv", list(points[0]), points)
    output_csv(work / "deltas.csv", list(deltas[0]), deltas)
    return points



def check_control(name, passed, **observations):
    log("control", name=name, verdict="pass" if passed else "fail", **observations)
    if not passed:
        raise ValueError(f"control {name} failed")


def run_controls(inputs, work, files, x05, version, negative):
    fixture = files["X16"]
    schema = inputs["columns"]["forward_output"]
    baseline = read_fixture("X16 control baseline", fixture, schema, "forward_output", version)
    lines = fixture.decode("utf-8").splitlines()

    def load_variant(name, variant):
        return read_fixture(name, ("\n".join(variant) + "\n").encode(),
                            schema, "forward_output", version)

    reordered = load_variant("control reorder", [lines[0], *reversed(lines[1:])])
    ordinal_would_fail = sum(a != b for a, b in zip(baseline, reordered))
    joined_matches = sum(equal_numeric(baseline[point], reordered[point]) for point in IDS)
    check_control("row_reordering", joined_matches == 40 and ordinal_would_fail == 40,
                  id_matches=joined_matches, ordinal_mismatches=ordinal_would_fail)

    for name, point, columns, replacements, expected_changed in (
        ("east_north_swap", "TP02", (1, 2), ("11572.405", "170370.718"), [1, 2]),
        ("metres_as_millimetres", "TP02", (1, 2, 3), ("170370718.000","11572405.000","71264.000"), [1, 2, 3]),
        ("plus_0_001_m", "TP02", (3,), ("71.265",), [3]),
        ("same_height_other_datum", "TP01", (4,), ("1",), [4]),
    ):
        variant = lines.copy()
        index = next(i for i,line in enumerate(variant) if line.startswith(point + ","))
        fields = variant[index].split(",")
        for column, value in zip(columns, replacements):
            fields[column] = value
        variant[index] = ",".join(fields)
        tested = load_variant(name, variant)[point]
        original = baseline[point]
        changed = [i for i, (a,b) in enumerate(zip(original.tokens,tested.tokens), 1)
                   if Decimal(a) != Decimal(b)]
        check_control(name, changed == expected_changed, point=point,
                      original=original.tokens, mutated=tested.tokens, changed_columns=changed)

    variant = [line.replace("TP03,", "TP02,", 1) if line.startswith("TP03,") else line for line in lines]
    try:
        load_variant("control duplicate/missing", variant)
    except ValueError as error:
        check_control("duplicate_id", str(error).endswith("invalid point keys"), rejected=str(error))
    else:
        check_control("duplicate_id", False)

    geographic = read_fixture("X15 control baseline", files["X15"], inputs["columns"]["forward_input"],
                              "forward_input", version)
    original_lat, original_lon = geographic["TP02"].tokens[:2]
    article_lat, article_lon = x05["geographic"]["TP02"].tokens[:2]
    same_value = Decimal(original_lat) == Decimal(article_lat) and original_lat != article_lat
    rounded_lon = Decimal(original_lon).quantize(Decimal("0.0000000001"), rounding=ROUND_HALF_UP)
    same_display = rounded_lon == Decimal(article_lon) != Decimal(original_lon)
    check_control("text_decimal_and_display", same_value and same_display,
                  X15=[original_lat, original_lon], X05=[article_lat, article_lon],
                  rounded_lon=str(rounded_lon), longitude_delta_degree=signed(article_lon,original_lon))

    reverse_output = read_fixture("X21 control baseline", files["X21"], inputs["columns"]["reverse_output"],
                                  "reverse_output", version)
    height = Decimal(reverse_output["TP31"].tokens[2])
    up = height.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    even = height.quantize(Decimal("0.001"), rounding=ROUND_HALF_EVEN)
    check_control("reverse_height_direction_and_tie", up == Decimal("100.001") and even == Decimal("100.000"),
                  source="X21: L154 RESULT", raw=str(height), half_up=str(up), half_even=str(even))

    first = ("9414290", "MLLW", "1983–2001", Decimal("0.000"))
    second = ("8454000", "MLLW", "1983–2001", Decimal("0.000"))
    check_control("tidal_station_zero", first[-1] == second[-1] and first[:3] != second[:3],
                  source_ids=["C02","C03"], same_number=True, first_station=first[0], second_station=second[0],
                  NAVD88_difference_m=signed("0.754","-0.018"))
    indicated, uncertainty = map(Decimal, ("40.01", "1.2"))
    lower, upper = map(Decimal, ("39.50", "40.50"))
    simple = lower <= indicated <= upper
    guarded = lower <= indicated - uncertainty and indicated + uncertainty <= upper
    check_control("calibration_decision_rule", simple and not guarded, source="C04 A6047713 p.1–2",
                  indication_psi=str(indicated), uncertainty_psi=str(uncertainty), limits_psi=[str(lower), str(upper)],
                  interval_psi=[str(indicated-uncertainty),str(indicated+uncertainty)],
                  stated_rule_accepts=simple, conceptual_guarded_rule_accepts=guarded)

    folder = work / "controls"
    folder.mkdir(exist_ok=True)
    html = folder / "archive-with-html-body.zip"
    html.write_text("<!doctype html><title>Not a downloadable ZIP</title>\n",encoding="utf-8")
    _, found, digest, status = inspect_archive(html,inputs["archive"])
    check_control("html_body_under_zip_name", not found and status=="not_zip", sha256=digest,
                  archive_status=status, control_body_is_synthetic=True)
    duplicate = folder / "archive-with-duplicate-entry.zip"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(duplicate,"w") as archive:
            name = inputs["archive"]["required_members"]["forward_output"]
            archive.writestr(zipfile.ZipInfo(name), fixture)
            archive.writestr(zipfile.ZipInfo(name), fixture)
    members, found, digest, status = inspect_archive(duplicate,inputs["archive"])
    check_control("duplicate_zip_entry", not found and len(members)==2 and status=="wrong_or_ambiguous_layout",
                  sha256=digest, entries=len(members), archive_status=status)
    if negative:
        members, found, digest, status = inspect_archive(negative,inputs["archive"])
        check_control("downloaded_repository_zip_wrong_edition",
                      not found and digest==inputs["negative_archive"]["sha256"] and status=="wrong_or_ambiguous_layout",
                      sha256=digest, entries=len(members), archive_status=status)
        duplicate_copy = folder / "same-repository-zip-bytes.zip"
        duplicate_copy.write_bytes(negative.read_bytes())
        hashes = {sha(path.read_bytes()) for path in (negative, duplicate_copy)}
        check_control("two_archive_names_one_payload", len(hashes)==1, file_count=2, distinct_sha256=len(hashes))
        output_csv(folder/"wrong-zip-members.csv", MEMBER_FIELDS,
                   (dict(archive_status=status,**member) for member in members))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True, help="temporary inputs and generated results")
    parser.add_argument("--fetch-comparators", action="store_true")
    parser.add_argument("--download-publisher", action="store_true")
    parser.add_argument("--download-x05", action="store_true")
    parser.add_argument("--archive", type=Path, help="a supplied ZIP is official only when its SHA matches the pin")
    parser.add_argument("--x05", type=Path, help="full HTML or CSV transcript from the rendered source")
    parser.add_argument("--controls", action="store_true", help="run mutation and alternative ZIP controls")
    parser.add_argument("--negative-archive", type=Path, help="local copy of the pinned wrong-package control")
    args = parser.parse_args()
    work = args.work
    work.mkdir(parents=True, exist_ok=True)
    inputs = json.loads((HERE / "inputs.json").read_text(encoding="utf-8"))
    config = inputs["archive"]
    log("runtime", python=sys.version.split()[0], curl=subprocess.check_output(["curl","--version"],text=True).splitlines()[0],
        inputs_sha256=sha((HERE/"inputs.json").read_bytes()))
    files = {}
    for id, spec in inputs["pinned_files"].items():
        path = work / spec["local_name"]
        if args.fetch_comparators and curl_get(spec["url"], path) is None:
            raise ValueError(f"{id}: fetch failed")
        blob = path.read_bytes()
        if sha(blob) != spec["sha256"]:
            raise ValueError(f"{id}: SHA256 differs from pin")
        files[id] = blob
        log("pinned_file", id=id, bytes=len(blob), sha256=sha(blob))
    path = download_publisher(config,work) if args.download_publisher else args.archive
    inventory, candidate, archive_hash, archive_status = inspect_archive(path,config)
    provenance = args.download_publisher or (archive_hash and archive_hash == config["current_sha256"])
    official = candidate if provenance else {}
    if candidate and not official:
        archive_status = "unverified_local_provenance"
    if not inventory:
        inventory = [dict(archive_sha256=archive_hash or UNKNOWN,member=UNKNOWN)]
    output_csv(work/"members.csv",MEMBER_FIELDS,
        (dict(archive_status=archive_status,**item) for item in inventory))
    log("publisher_status", status=archive_status, official_file_roles=sorted(official),
        publisher_sha256=archive_hash, historic_sha256=config["historical_188_sha256"])
    x05_input = args.x05 or HERE / inputs["x05"]["receipt_selected"]
    if args.x05 is None and sha(x05_input.read_bytes()) != inputs["x05"]["receipt_selected_sha256"]:
        raise ValueError("X05 selected transcript differs from its pin")
    if args.download_x05:
        html = work/"X05.html"
        if curl_get(inputs["x05"]["url"],html) is not None:
            x05_input = html
    version = (f"OS-full-sha256:{archive_hash}" if official else
               "OSTN15-OSGM15-replicas:unverified-publisher-build")
    x05 = article_data(x05_input,set(inputs["fixed_slots"].values())|set(inputs["supplemental_ids"]),version)
    points = compare_output(inputs,work,files,official,x05,version)
    if args.controls:
        negative = args.negative_archive
        if negative is None and args.fetch_comparators:
            negative = work / inputs["negative_archive"]["local_name"]
            if curl_get(inputs["negative_archive"]["url"],negative) is None:
                raise ValueError("negative archive fetch failed")
        run_controls(inputs,work,files,x05,version,negative)
    log("summary", fixed_slots=6, fixed_unique=4, conflict_ids=2,
        publisher_slots=sum(p["official_status"]=="direct" for p in points[:6]),
        compared_to_188_slots=sum(p["versus_188_raw"]=="true" for p in points[:6]),
        exit=0 if official else 2)
    return 0 if official else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, csv.Error, zipfile.BadZipFile) as error:
        log("error", kind=type(error).__name__, detail=str(error), exit=1)
        sys.exit(1)
