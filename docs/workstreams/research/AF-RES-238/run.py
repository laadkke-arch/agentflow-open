"""Fetch and replay AF-RES-238 through the public publisher endpoints in inputs.json."""
import argparse
from base64 import b64encode
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, localcontext
from fractions import Fraction
from hashlib import sha256, file_digest
import hmac
import io
import json
import os
from pathlib import Path
import platform
import re
import secrets
import subprocess
import sys
from urllib.parse import parse_qs, quote, urlparse
from zipfile import BadZipFile, ZipFile

HERE = Path(__file__).resolve().parent
ROLES = {"001": "total_age16plus", "003": "civilian_labor_force", "005": "unemployed"}
SUFFIXES = ("E", "M", "EA", "MA")
NUMERIC = ("E", "M")
SPECIAL = {"-222222222", "-333333333", "-555555555", "-666666666", "-888888888", "-999999999"}
CARD_COLUMNS = ("card_id", "source_url", "statement", "numerator_role", "denominator_role",
                "input_integers", "formula", "edition", "member_keys")
METHODS = {
    "union": "ratio_of_sums", "wrong_denominator": "ratio_of_sums",
    "county_mean": "mean_of_ratios", "repeat_county": "ratio_of_sums",
    "state_overlaps_county": "ratio_of_sums",
}
REASONS = {
    "union": "두 카운티는 동판의 서로 다른 행이며 실업자 합을 민간 노동력 합으로 나눈다.",
    "wrong_denominator": "분모가 B23025_001E 전체 16세 이상으로 바뀌었다.",
    "county_mean": "카운티율에 같은 가중치를 줬다. 합집합은 민간 노동력 가중이다.",
    "repeat_county": "동일 판·동일 GEO_ID가 반복되어 구성원을 중복 집계했다.",
    "state_overlaps_county": "주 전체에 이미 포함된 카운티를 한 번 더 집계했다.",
}


def digest(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_csv(path, columns, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fetch_one(directory, item):
    name, spec = item
    url = spec["url"]
    key = os.environ.get("CENSUS_API_KEY") if urlparse(url).hostname == "api.census.gov" else None
    real_url = url + "&key=" + quote(key, safe="") if key else url
    body, headers = (directory / f"{name}.{ext}" for ext in ("body", "headers"))
    body.unlink(missing_ok=True)
    headers.unlink(missing_ok=True)
    started = utc()
    command = ["curl", "--silent", "--show-error", "--location", "--max-redirs", "5",
               "--connect-timeout", "12", "--max-time", "90", "--proto", "=https",
               "--proto-redir", "=https", "--header", "Accept-Encoding: identity",
               "--dump-header", str(headers), "--output", str(body), "--write-out", "%{json}",
               "--config", "-"]
    completed = subprocess.run(command, input="url = " + json.dumps(real_url) + "\n",
                               text=True, capture_output=True)
    transfer = json.loads(completed.stdout) if completed.stdout else {}

    def redact(value):
        if value is None or not key:
            return value
        return value.replace(quote(key, safe=""), "[REDACTED]").replace(key, "[REDACTED]")

    if headers.exists():
        kept = []
        for line in headers.read_bytes().splitlines(keepends=True):
            if line.lower().startswith((b"set-cookie:", b"authorization:", b"proxy-authorization:")):
                line = line.split(b":", 1)[0] + b": [REDACTED]\r\n"
            kept.append(line)
        original = b"".join(kept)
        safe = redact(original.decode("iso-8859-1")).encode("iso-8859-1")
        headers.write_bytes(safe)
    receipt = {
        "request": {"method": "GET", "url": url, "headers": {"Accept-Encoding": "identity"},
                    "census_key_supplied": bool(key)},
        "started_utc": started, "ended_utc": utc(), "exit": completed.returncode,
        "status": transfer.get("http_code") or None, "proxy_connect_status": transfer.get("http_connect") or None,
        "final_url": redact(transfer.get("url_effective")), "media_type": transfer.get("content_type"),
        "redirects": transfer.get("num_redirects"), "size": body.stat().st_size if body.exists() else None,
        "sha256": digest(body) if body.exists() else None,
        "header_sha256": digest(headers) if headers.exists() else None,
        "stderr": redact(completed.stderr), "header_kind": "curl header blocks with sensitive fields redacted",
    }
    save_json(directory / f"{name}.json", receipt)
    return name, receipt


def payload(name, inputs, directory, attempts):
    spec = inputs["requests"][name]
    if directory is not None and (directory / f"{name}.json").exists():
        receipt = read_json(directory / f"{name}.json")
    else:
        receipt = attempts.get(name)
    if receipt is None:
        return None, "request_not_run"
    if receipt["request"]["url"] != spec["url"]:
        return None, "request_url_mismatch"
    if receipt["status"] != 200 or receipt["exit"] != 0:
        return None, "request_failed"
    if directory is None:
        return None, "no_body_in_archived_receipt"
    body = directory / f"{name}.body"
    if not body.is_file() or not receipt["sha256"]:
        return None, "missing_response_bytes"
    if body.stat().st_size != receipt["size"] or digest(body) != receipt["sha256"]:
        return None, "receipt_fingerprint_mismatch"
    if spec["sha256"] and spec["sha256"] != receipt["sha256"]:
        return None, "pinned_fingerprint_mismatch"
    headers = directory / f"{name}.headers"
    if receipt["header_sha256"] and (not headers.is_file() or digest(headers) != receipt["header_sha256"]):
        return None, "header_fingerprint_mismatch"
    return body, "verified_receipt" if spec["sha256"] else "first_observation"


def cell_token(tokens, key, suffix, stream_status):
    if tokens is None:
        return None, stream_status
    if key not in tokens:
        return None, "field_absent"
    token = tokens[key]
    if token is None:
        return token, "api_null"
    if token == "":
        return token, "empty_annotation" if suffix.endswith("A") else "empty_numeric"
    if suffix.endswith("A"):
        return token, "annotation_text" if isinstance(token, str) else "invalid_token"
    if type(token) not in (int, str):
        return token, "invalid_token"
    if str(token) in SPECIAL:
        return token, "statistical_special"
    if not re.fullmatch(r"[0-9]+", str(token)):
        return token, "invalid_token"
    return token, "zero" if int(token) == 0 else "observed_number"


def extract_dat(path, targets):
    """Compare a CSV parser with a second exact byte-split pass and keep the physical lines."""
    targets = set(targets)
    with path.open("rb") as stream:
        raw_header = next(stream)
        columns = next(csv.reader([raw_header.decode("utf-8-sig")], delimiter="|", strict=True))
        if len(set(columns)) != len(columns) or "GEO_ID" not in columns:
            raise ValueError("invalid DAT column names")
        mandatory = {f"B23025_{suffix}{position}" for position in ROLES for suffix in NUMERIC}
        if not mandatory.issubset(columns):
            raise ValueError("missing DAT E/M columns")
        geo_index = columns.index("GEO_ID")
        rows = {}
        for line_number, raw_line in enumerate(stream, 2):
            values = next(csv.reader([raw_line.decode("utf-8")], delimiter="|", strict=True))
            if len(values) != len(columns):
                raise ValueError(f"invalid field count on DAT line {line_number}")
            geo = values[geo_index]
            if geo in targets:
                if geo in rows:
                    raise ValueError(f"duplicate DAT geography {geo}")
                rows[geo] = {
                    "line": line_number, "row_b64": b64encode(raw_line).decode(),
                    "sha256": sha256(raw_line).hexdigest(), "tokens": dict(zip(columns, values)),
                }
    wanted = {item.encode() for item in targets}
    crosscheck = {}
    collisions = {}
    geo_bytes = re.compile(rb"0500000US[0-9]{5}")
    unemployed = columns.index("B23025_E005")
    values_to_check = {record["tokens"]["B23025_E005"].encode() for record in rows.values()
                       if record["tokens"]["B23025_E005"].isdigit()}
    with path.open("rb") as stream:
        next(stream)
        for line_number, line in enumerate(stream, 2):
            fields = line.rstrip(b"\r\n").split(b"|")
            key = fields[geo_index]
            if key in wanted:
                geo = key.decode("ascii")
                crosscheck[geo] = (line_number, [part.decode("utf-8") for part in fields])
            elif geo_bytes.fullmatch(key) and fields[unemployed] in values_to_check:
                # Preserve one actual foil per raw count, with its original line and byte identity.
                collisions.setdefault(fields[unemployed].decode(), {
                    "geo_id": key.decode(), "line": line_number, "sha256": sha256(line).hexdigest(),
                    "row_b64": b64encode(line).decode(),
                })
    first = {key: (row["line"], list(row["tokens"].values())) for key, row in rows.items()}
    if first != crosscheck:
        raise ValueError("DAT extraction paths disagree")
    return {
        "header_b64": b64encode(raw_header).decode(), "header_sha256": sha256(raw_header).hexdigest(),
        "columns": columns, "encoding": "strict UTF-8", "delimiter": "|",
        "rows": rows, "same_count_other_county": collisions, "independent_extraction_agrees": True,
    }


def extract_api(path, url, targets):
    frame = read_json(path)
    if (not isinstance(frame, list) or not frame or not isinstance(frame[0], list)
            or "GEO_ID" not in frame[0] or len(set(frame[0])) != len(frame[0])):
        raise ValueError("expected API JSON array with GEO_ID header")
    fields = frame[0]
    requested = set(parse_qs(urlparse(url).query)["get"][0].split(","))
    if not requested.issubset(fields):
        raise ValueError("API result does not cover requested columns")
    output = {}
    for index, row in enumerate(frame[1:], 2):
        if not isinstance(row, list) or len(row) != len(fields):
            raise ValueError("unexpected API row shape")
        values = dict(zip(fields, row))
        geo = values["GEO_ID"]
        if geo not in targets or geo in output:
            raise ValueError("unexpected or duplicate API GEO_ID")
        expected = values["state"] + values["county"] if "county" in values else values["state"]
        if geo.split("US")[1] != expected:
            raise ValueError("API FIPS padding or geography mismatch")
        output[geo] = {"json_array_row": index, "tokens": values, "raw_json_values": row}
    return {"columns": fields, "rows": output, "body_b64": b64encode(path.read_bytes()).decode()}


def extract_vre(path, targets):
    """Read the release archive without expanding the whole CSV into the repository."""
    needed = ("GEOID", "ORDER", "ESTIMATE", "MOE", "CME", *(f"VAR_REP{i}" for i in range(1, 81)))
    rows = {}
    with ZipFile(path) as archive:
        [name] = [item for item in archive.namelist() if Path(item).name.lower() == "b23025.csv"]
        with io.TextIOWrapper(archive.open(name), encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            for _ in range(3):
                header = [col.strip().upper() for col in next(reader)]
                if set(needed).issubset(header):
                    break
            if len(set(header)) != len(header) or not set(needed).issubset(header):
                raise ValueError("unrecognized B23025 VRE header")
            positions = {field: header.index(field) for field in needed}
            for row in reader:
                if len(row) != len(header):
                    if reader.line_num <= 3:
                        continue
                    raise ValueError(f"unexpected VRE row shape on line {reader.line_num}")
                geo = row[positions["GEOID"]]
                if geo not in targets:
                    continue
                order = Decimal(row[positions["ORDER"]])
                if order not in (3, 5):
                    continue
                key = f"{geo}:{int(order):03}"
                if key in rows:
                    raise ValueError(f"duplicate VRE row {key}")
                if "TBLID" in header and row[header.index("TBLID")].upper() != "B23025":
                    raise ValueError(f"unexpected table ID for {key}")
                rows[key] = {"line": reader.line_num, "tokens": {field: row[positions[field]] for field in needed}}
    return {"archive_member": name, "columns": header, "rows": rows}


def fraction_of(numerator, denominator):
    if numerator is None or denominator is None or denominator <= 0 or not 0 <= numerator <= denominator:
        return None
    return Fraction(numerator, denominator)


def sum_ratio(terms):
    if any(n is None or d is None or d < 0 or not 0 <= n <= d for n, d in terms):
        return None
    return fraction_of(sum(n for n, _ in terms), sum(d for _, d in terms))


def mean_ratio(terms):
    rates = [fraction_of(n, d) for n, d in terms]
    if any(rate is None for rate in rates):
        return None
    return sum(rates) / len(rates)


def display(value, scale=100, places=1):
    """Round a nonnegative exact Fraction once with integer arithmetic."""
    if value is None:
        return ""
    factor = 10**places
    scaled = value * scale * factor
    quotient, remainder = divmod(scaled.numerator, scaled.denominator)
    quotient += 2 * remainder >= scaled.denominator
    return f"{quotient // factor}.{quotient % factor:0{places}d}"


def dec(value):
    return Decimal(value.numerator) / Decimal(value.denominator)


def moe_approx(p, d, u_moes, labor_moes):
    if p is None or p in (0, 1):
        return {"status": "unavailable_or_boundary"}
    if any(x is None for x in (*u_moes, *labor_moes)):
        return {"status": "count_moe_missing_or_special"}
    a = sum(m * m for m in u_moes)
    b = sum(m * m for m in labor_moes)
    radicand = a - p * p * b
    method = "subset_minus"
    if radicand < 0:
        radicand = a + p * p * b
        method = "ratio_plus_fallback"
    with localcontext() as ctx:
        ctx.prec = 45
        pp = 100 * dec(radicand).sqrt() / d
    return {"status": "approximation_90pct", "pp": str(pp), "method": method,
            "sum_u_moe_sq": a, "sum_labor_moe_sq": b, "radicand_exact": str(radicand),
            "assumption": "No between-geography covariance and no controlled inputs"}


def moe_sdr(p, members, vre, counts):
    if p is None or p in (0, 1):
        return {"status": "unavailable_or_boundary"}
    keys = [f"{geo}:{role}" for geo in members for role in ("005", "003")]
    if not all(key in vre for key in keys):
        return {"status": "vre_rows_unavailable"}
    rows = [vre[key]["tokens"] for key in keys]
    if any(row["CME"].strip() == "*****" for row in rows):
        return {"status": "controlled_case_requires_separate_treatment"}
    u1, d1, u2, d2 = rows
    try:
        if any(Fraction(row["ESTIMATE"]) != counts[key.split(":")[0]][key.split(":")[1]][0]
               for key, row in zip(keys, rows)):
            return {"status": "vre_estimate_disagrees_with_dat"}
        sums = []
        undefined = []
        for i in range(1, 81):
            field = f"VAR_REP{i}"
            n = Fraction(u1[field]) + Fraction(u2[field])
            d = Fraction(d1[field]) + Fraction(d2[field])
            if not d:
                undefined.append(i)
            sums.append((n, d))
        ss = sum((p - n / d if d else p) ** 2 for n, d in sums)
    except (ValueError, ZeroDivisionError):
        return {"status": "unusable_vre_token"}
    if ss == 0:
        return {"status": "zero_sdr_variance_requires_model"}
    variance = Fraction(4, 80) * ss
    with localcontext() as ctx:
        ctx.prec = 45
        pp = 100 * Decimal("1.645") * dec(variance).sqrt()
    return {"status": "sdr_90pct", "pp": str(pp), "variance_exact": str(variance),
            "replicate_count": len(sums), "zero_denominator_replicates": undefined,
            "vre_record_keys": keys}


def integer_cell(tokens, variable, suffix):
    raw, status = cell_token(tokens, variable, suffix, "row_missing")
    return int(raw) if status in ("observed_number", "zero") else None


def target_cells(inputs, dat, apis, statuses):
    cells = []
    counts = {}
    for geo, label in inputs["geographies"].items():
        api_id = "api-states" if geo.startswith("040") else "api-ca" if geo[9:11] == "06" else "api-tx"
        dat_row = dat.get(geo, {})
        api_row = apis.get(geo, {})
        dat_tokens, api_tokens = dat_row.get("tokens"), api_row.get("tokens")
        counts[geo] = {}
        for number, role in ROLES.items():
            counts[geo][number] = tuple(integer_cell(dat_tokens, f"B23025_{suffix}{number}", suffix)
                                        for suffix in NUMERIC)
            if ((api_tokens and api_tokens.get(f"B23025_{number}MA") == "*****")
                    or (dat_tokens and dat_tokens.get(f"B23025_MA{number}") == "*****")):
                counts[geo][number] = (counts[geo][number][0], None)
            for suffix in SUFFIXES:
                dat_field, api_field = f"B23025_{suffix}{number}", f"B23025_{number}{suffix}"
                dat_status = statuses["dat23"] if statuses["dat23"] not in ("first_observation", "verified_receipt") else "row_missing"
                api_status = statuses[api_id] if statuses[api_id] not in ("first_observation", "verified_receipt") else "row_missing"
                dt, ds = cell_token(dat_tokens, dat_field, suffix, dat_status)
                at, a_s = cell_token(api_tokens, api_field, suffix, api_status)
                if suffix not in NUMERIC and not dat_row:
                    ds = "format_excludes_annotation; actual_header_unobserved"
                match = ""
                if suffix in NUMERIC and ds in ("observed_number", "zero", "statistical_special") and a_s in (
                        "observed_number", "zero", "statistical_special"):
                    match = "equal" if int(dt) == int(at) else "different"
                cells.append({
                    "geo_id_expected": geo, "geo_id_observed_dat": geo if dat_row else "",
                    "region": label, "edition": inputs["edition"], "variable": api_field, "role": role,
                    "unit": "annotation" if suffix.endswith("A") else "persons",
                    "dat_field": dat_field if suffix in NUMERIC or dat_tokens and dat_field in dat_tokens else "",
                    "dat_token_json": json.dumps(dt, ensure_ascii=False) if dat_tokens is not None and dat_field in dat_tokens else "",
                    "dat_status": ds, "dat_line": dat_row.get("line", ""), "dat_row_sha256": dat_row.get("sha256", ""),
                    "api_request": api_id,
                    "api_token_json": json.dumps(at, ensure_ascii=False) if api_tokens is not None and api_field in api_tokens else "",
                    "api_status": a_s, "api_array_row": api_row.get("json_array_row", ""),
                    "em_crosscheck": match,
                })
    return cells, counts


def rates(inputs, counts, vre):
    output = []
    for pair, (first, second, state) in inputs["pairs"].items():
        spec = [(first, second, "003"), (first, second, "001"), (first, second, "003"),
                (first, second, second, "003"), (state, first, "003")]
        baseline = None
        for (case, formula), (*members, denominator) in zip(METHODS.items(), spec):
            terms = [(counts[key]["005"][0], counts[key][denominator][0]) for key in members]
            value = mean_ratio(terms) if formula == "mean_of_ratios" else sum_ratio(terms)
            complete = all(n is not None and d is not None for n, d in terms)
            n = sum(count[0] for count in terms) if complete and formula == "ratio_of_sums" else None
            d = sum(count[1] for count in terms) if complete and formula == "ratio_of_sums" else None
            shown = display(value, places=inputs["rounding_pct"]["digits"])
            alternative = None
            if value is not None and formula == "ratio_of_sums":
                # Independent algebra uses individual rates and denominator weights, skipping 0/0 components.
                alternative = sum(Fraction(x, y) * y for x, y in terms if y) / d
                if value != alternative:
                    raise ValueError("exact calculation paths disagree")
            if case == "union":
                baseline = value
                approx = moe_approx(value, d, [counts[k]["005"][1] for k in members],
                                    [counts[k]["003"][1] for k in members])
                sdr = moe_sdr(value, members, vre, counts)
            else:
                approx = sdr = {"status": "control_no_union_moe"}
            difference = 100 * (value - baseline) if value is not None and baseline is not None else None
            reason = "ok"
            if not complete:
                reason = "source_input_missing"
            elif value is None:
                zero_denominator = d == 0 or (formula == "mean_of_ratios" and any(y == 0 for _, y in terms))
                reason = "zero_denominator" if zero_denominator else "count_out_of_domain"
            output.append(dict(pair=pair, case=case, members=members, denominator=denominator, terms=terms,
                               numerator_sum=n, denominator_sum=d, formula=formula, value=value,
                               display_percent=shown, weighted_recheck=alternative, status=reason,
                               delta_pp=difference, display_tie_with_union=(shown == display(baseline)) if shown else None,
                               approximate=approx, sdr=sdr))
    return output


def write_packet(out, inputs, results, ready, previous_key):
    key = {"entries": []}
    if ready:
        seed = bytes.fromhex(read_json(previous_key)["seed_hex"]) if previous_key else secrets.token_bytes(32)
        if len(seed) != 32:
            raise ValueError("expected 32-byte card seed")
        key["seed_hex"] = seed.hex()
    hashes = {}
    for layer in ("A", "B", "C"):
        cards = []
        if ready:
            for item in results:
                first, second, _ = inputs["pairs"][item["pair"]]
                region = f'{inputs["geographies"][first]} and {inputs["geographies"][second]}'
                text = f'The combined unemployment rate for {region} was {item["display_percent"]}% in the {inputs["edition"]} estimates.'
                token = f'{layer}/{item["pair"]}/{item["case"]}'.encode()
                opaque = hmac.new(seed, b"card-id/" + token, sha256).hexdigest()[:24]
                sort_key = hmac.new(seed, b"shuffle/" + token, sha256).digest()
                card = dict.fromkeys(CARD_COLUMNS, "")
                card.update(card_id=opaque, source_url=inputs["requests"]["dat23"]["url"], statement=text)
                if layer in ("B", "C"):
                    card.update(numerator_role="B23025_005E (unemployed persons)",
                                denominator_role=f'B23025_{item["denominator"]}E ({ROLES[item["denominator"]]})',
                                input_integers=json.dumps(item["terms"], separators=(",", ":")),
                                formula=item["formula"])
                if layer == "C":
                    card.update(edition=inputs["edition"] + " / B23025 / boundaries " + inputs["geography_date"],
                                member_keys=json.dumps(item["members"], separators=(",", ":")))
                cards.append((sort_key, card))
                key["entries"].append(dict(layer=layer, card_id=opaque, pair=item["pair"], case=item["case"],
                                           correct=item["case"] == "union", reason=REASONS[item["case"]],
                                           ratio_exact=str(item["value"])))
        path = out / "blind" / f"{layer}.csv"
        save_csv(path, CARD_COLUMNS, [card for _, card in sorted(cards)])
        hashes[f"blind/{layer}.csv"] = {"rows": len(cards), "sha256": digest(path)}
    seen = {entry["card_id"] for entry in key["entries"]}
    if len(seen) != len(key["entries"]):
        raise ValueError("card ID collision")
    save_json(out / "key.json", key)
    save_json(out / "packet-manifest.json", {
        "status": "ready" if ready else "withheld_unverified_county_inputs",
        "reading_order": ["A", "B", "C"], "expected_cards_per_layer": 10, "files": hashes,
    })


def baseball(paths, inputs):
    batting = []
    player = str(inputs["mlb_player_id"])
    for game_id in inputs["mlb_game_ids"]:
        path = paths[f"mlb-{game_id}"]
        if path is None:
            continue
        data = read_json(path)
        players = [data["teams"][side]["players"][f"ID{player}"]
                   for side in ("home", "away") if f"ID{player}" in data["teams"][side]["players"]]
        [batter] = players
        stats = batter["stats"]["batting"]
        if str(batter["person"]["id"]) != player:
            raise ValueError("unexpected MLB player")
        batting.append({"game_id": game_id, "player_id": int(player), "scope": "game_batting",
                        "hits": stats["hits"], "at_bats": stats["atBats"]})
    output = {"observed": len(batting), "rows": batting}
    if len(batting) == 2:
        pairs = [(row["hits"], row["at_bats"]) for row in batting]
        correct, mean, duplicate = sum_ratio(pairs), mean_ratio(pairs), sum_ratio([*pairs, pairs[0]])
        output["calculation"] = {
            "weighted_fraction": str(correct), "weighted_display": display(correct, scale=1, places=3),
            "mean_fraction": str(mean), "mean_display": display(mean, scale=1, places=3),
            "duplicated_game_id": batting[0]["game_id"], "raw_duplicate_fraction": str(duplicate),
            "raw_duplicate_display": display(duplicate, scale=1, places=3),
            "unique_keys": len({(row["game_id"], row["player_id"], row["scope"]) for row in [*batting, batting[0]]}),
        }
    return output


def compare_tables(inputs, apis, counts):
    pairs = (("s2301", "S2301_C04_001E", "S2301_C04_001M", "S2301_C04_001EA", "S2301_C04_001MA"),
             ("dp03", "DP03_0009PE", "DP03_0009PM", "DP03_0009PEA", "DP03_0009PMA"))
    output = []
    for geo in inputs["geographies"]:
        if not geo.startswith("050"):
            continue
        point = fraction_of(counts[geo]["005"][0], counts[geo]["003"][0])
        for dataset, estimate, moe, annotation, moe_note in pairs:
            row = apis[dataset].get(geo)
            token = row["tokens"][estimate] if row else None
            calculated = display(point)
            check = "unverified"
            if calculated and isinstance(token, (str, int, float)):
                try:
                    value = Decimal(str(token))
                except InvalidOperation:
                    value = Decimal("NaN")
                if value.is_finite() and 0 <= value <= 100:
                    check = "equal" if value == Decimal(calculated) else "different"
            output.append({"geo_id": geo, "source": dataset, "edition": inputs["edition"],
                           "pct": token, "moe_pp": row["tokens"][moe] if row else None,
                           "annotation": row["tokens"][annotation] if row else None,
                           "moe_annotation": row["tokens"][moe_note] if row else None,
                           "county_calculated_pct": calculated, "display_comparison": check})
    return output


def replay(args, inputs):
    archive = args.attempts
    attempts = {row["request_id"]: row for row in (
        json.loads(line) for line in archive.read_text(encoding="utf-8").splitlines())} if archive else {}
    files, statuses = {}, {}
    for request in inputs["requests"]:
        files[request], statuses[request] = payload(request, inputs, args.download_dir, attempts)
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    if args.download_dir is not None:
        fresh = {}
        for request in inputs["requests"]:
            metadata = args.download_dir / f"{request}.json"
            header = args.download_dir / f"{request}.headers"
            if metadata.is_file():
                item = read_json(metadata)
                if header.is_file() and digest(header) == item["header_sha256"]:
                    item["raw_header_b64"] = b64encode(header.read_bytes()).decode()
                fresh[request] = item
        save_json(out/"receipts"/"publisher-http.json", fresh)
    extracts, failures = {}, {}

    def extract(name, parser, *extra):
        body = files[name]
        if body is not None:
            try:
                extracts[name] = parser(body, *extra)
                return extracts[name].get("rows", {})
            except (ValueError, TypeError, KeyError, IndexError, OSError, StopIteration, InvalidOperation,
                    csv.Error, BadZipFile, UnicodeError) as error:
                statuses[name] = "invalid_payload"
                failures[name] = str(error)
        return {}

    targets = sorted(inputs["geographies"])
    county_ids = [key for key in targets if key.startswith("050")]
    dat_rows = extract("dat23", extract_dat, targets)
    extract("dat22", extract_dat, county_ids)
    vre = extract("vre23", extract_vre, county_ids)
    apis = {"b23025": {}, "s2301": {}, "dp03": {}}
    for key, (first, second, _) in inputs["pairs"].items():
        region = key.lower()
        for dataset, prefix in (("b23025", "api"), ("s2301", "s2301"), ("dp03", "dp03")):
            name = f"{prefix}-{region}"
            apis[dataset].update(extract(name, extract_api, inputs["requests"][name]["url"], [first, second]))
    apis["b23025"].update(extract("api-states", extract_api, inputs["requests"]["api-states"],
                                  [key for key in targets if key.startswith("040")]))
    cells, counts = target_cells(inputs, dat_rows, apis["b23025"], statuses)
    county = [cell for cell in cells if cell["geo_id_expected"].startswith("050")]
    states = [cell for cell in cells if cell["geo_id_expected"].startswith("040")]
    save_csv(out/"rows.csv", list(cells[0]), county)
    save_csv(out/"receipts"/"state-cells.csv", list(cells[0]), states)
    results = rates(inputs, counts, vre)
    ratio_rows = []
    for item in results:
        row = {key: value for key, value in item.items() if key not in ("approximate", "sdr")}
        row["members"] = json.dumps(row["members"], separators=(",", ":"))
        row["terms"] = json.dumps(row["terms"], separators=(",", ":"))
        row.update(approx_moe_pp=item["approximate"].get("pp", ""), approx_status=item["approximate"]["status"],
                   sdr_moe_pp=item["sdr"].get("pp", ""), sdr_status=item["sdr"]["status"],
                   receipt_key=f'{item["pair"]}/{item["case"]}')
        ratio_rows.append(row)
    save_csv(out/"ratios.csv", list(ratio_rows[0]), ratio_rows)
    observed_em = {"observed_number", "zero", "statistical_special"}
    observed_ann = {"annotation_text", "empty_annotation", "api_null"}
    known_cells = sum(cell["api_status"] in observed_ann if cell["unit"] == "annotation"
                      else cell["dat_status"] in observed_em for cell in county)
    distinct = all(counts[key]["001"][0] is not None and counts[key]["003"][0] is not None
                   and counts[key]["003"][0] <= counts[key]["001"][0] for key in counts)
    ready = (known_cells == 48 and len(dat_rows) == 6 and distinct
             and all(item["status"] == "ok" for item in results)
             and all(cell["em_crosscheck"] != "different" for cell in cells))
    write_packet(out, inputs, results, ready, args.key)
    try:
        mlb = baseball(files, inputs)
    except (KeyError, TypeError, ValueError) as error:
        mlb = {"observed": 0, "parse_problem": str(error)}
    rate_proofs = []
    for item in results:
        proof = {key: str(value) if isinstance(value, Fraction) else value for key, value in item.items()}
        rate_proofs.append(proof)
    save_json(out/"receipts"/"replay.json", {
        "inputs_sha256": digest(args.inputs), "requests": statuses, "parse_failures": failures,
        "payload_sha256": {name: digest(path) for name, path in files.items() if path is not None},
        "extractions": extracts, "calculations": rate_proofs,
        "cross_tables": compare_tables(inputs, apis, counts), "mlb": mlb,
        "observed": {"county_rows": len(set(dat_rows) & set(county_ids)),
                     "state_rows": len(set(dat_rows) - set(county_ids)), "county_cells": known_cells,
                     "union_rates": sum(row["status"] == "ok" and row["case"] == "union" for row in results),
                     "ready_cards": 30 if ready else 0},
        "python": platform.python_version(),
    })
    print(f"county_cells={known_cells}/48 county_dat_rows={len(set(dat_rows)&set(county_ids))}/4 "
          f"state_dat_rows={len(set(dat_rows)-set(county_ids))}/2 packet_rows={30 if ready else 0}/30")
    for name, status in statuses.items():
        print(f"{name}: {status}")
    return 0 if ready else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=HERE / "inputs.json")
    actions = parser.add_subparsers(dest="action", required=True)
    download = actions.add_parser("fetch", help="store transient bodies and HTTP receipt files")
    download.add_argument("--download-dir", type=Path, required=True)
    download.add_argument("--only", nargs="+", help="fetch only these request IDs")
    redo = actions.add_parser("replay", help="check SHA256, recover rows, and produce calculation and packet files")
    redo.add_argument("--download-dir", type=Path)
    redo.add_argument("--attempts", type=Path, help="optional archived failure receipts")
    redo.add_argument("--out", type=Path, required=True)
    redo.add_argument("--key", type=Path, help="reuse a previously sealed seed")
    args = parser.parse_args()
    inputs = read_json(args.inputs)
    if args.action == "fetch":
        if args.download_dir.resolve().is_relative_to(HERE):
            parser.error("full publisher bodies belong in a scratch directory outside the owned path")
        args.download_dir.mkdir(parents=True, exist_ok=True)
        names = args.only or list(inputs["requests"])
        missing = False
        with ThreadPoolExecutor(max_workers=4) as pool:
            requests = [(name, inputs["requests"][name]) for name in names]
            for name, info in pool.map(lambda item: fetch_one(args.download_dir, item), requests):
                print(f"{name}: HTTP {info['status']} CONNECT {info['proxy_connect_status']} "
                      f"exit {info['exit']} bytes {info['size']} sha256 {info['sha256']}")
                missing |= info["status"] != 200 or info["exit"] != 0
        return 2 if missing else 0
    return replay(args, inputs)


if __name__ == "__main__":
    sys.exit(main())
