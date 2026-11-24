"""Run the normal replay command on synthetic files and check the committed partial output."""
from collections import Counter
import csv
from fractions import Fraction
from hashlib import sha256
import io
import json
import runpy
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.parse import parse_qs, urlparse
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def invoke(inputs, out, *flags, expected):
    args = [sys.executable, "-I", str(HERE / "run.py"), "--inputs", str(inputs), "replay",
            "--out", str(out), *map(str, flags)]
    result = subprocess.run(args, text=True, capture_output=True)
    if result.returncode != expected:
        raise AssertionError(f"unexpected exit {result.returncode}\n{result.stdout}{result.stderr}")
    return result.stdout.strip()


def fixture(directory, inputs):
    """Independent small fixtures with deliberately uneven weights and CRLF line bytes."""
    geo = list(inputs["geographies"])
    counts = {
        geo[0]: [1400, 90, 1000, 120, 50, 2],
        geo[1]: [2500, 65, 2000, 120, 101, 2],
        geo[2]: [1200000, 80, 1000000, 70, 60000, 1200],
        geo[3]: [130, -555555555, 100, 12, 0, 10],
        geo[4]: [10000, 200, 8000, 210, 480, 54],
        geo[5]: [2500000, 250, 2000000, 170, 140000, 1200],
    }
    dat_columns = ["GEO_ID", "B23025_E001", "B23025_M001", "B23025_E003", "B23025_M003", "B23025_E005", "B23025_M005"]
    api_columns = ["B23025_001E", "B23025_001M", "B23025_003E", "B23025_003M", "B23025_005E", "B23025_005M"]
    lines = ["|".join(dat_columns)]
    # Different county with the same value, to distinguish a repeated value from a repeated key.
    lines.append("0500000US01001|150|7|120|3|0|5")
    lines.extend("|".join(map(str, [key, *values])) for key, values in counts.items())
    (directory / "dat23.body").write_bytes(("\r\n".join(lines) + "\r\n").encode())
    (directory / "dat22.body").write_bytes(("\n".join(lines) + "\n").encode())

    subsets = {"ca": geo[:2], "tx": geo[2:4], "states": geo[4:]}
    percentages = dict(zip(geo[:4], ("5.0", "5.1", "6.0", "0.0")))
    for name, spec in inputs["requests"].items():
        if name.startswith(("api-", "s2301-", "dp03-")):
            service, place = name.split("-")
            fields = parse_qs(urlparse(spec["url"]).query)["get"][0].split(",")
            fields += ["state"] if place == "states" else ["state", "county"]
            frame = [fields]
            for key in subsets[place]:
                fips = key.split("US")[1]
                tokens = dict(NAME=inputs["geographies"][key], GEO_ID=key, state=fips[:2], county=fips[2:])
                tokens.update(dict(zip(api_columns, (str(x) for x in counts[key]))))
                tokens["B23025_001MA"] = "*****" if key == geo[3] else None
                tokens["B23025_005EA"] = ""
                if service != "api":
                    tokens.update(S2301_C04_001E=percentages[key],
                                  DP03_0009PE=percentages[key] if key != geo[3] else "-888888888")
                frame.append([tokens.get(field) for field in fields])
            write_json(directory / f"{name}.body", frame)

    vre = io.StringIO()
    writer = csv.writer(vre)
    writer.writerow(["TBLID", "GEOID", "ORDER", "ESTIMATE", "MOE", "CME", *(f"Var_Rep{i}" for i in range(1, 81))])
    writer.writerow(["fixture label row"])
    writer.writerow(["fixture units row"])
    for key in geo[:4]:
        for order, offset in ((3, 2), (5, 4)):
            point, moe = counts[key][offset:offset + 2]
            replicate = [point for _ in range(80)]
            if key in geo[:2] and order == 3:
                replicate[0] = 0
            if order == 5:
                replicate[1] = point + 1
            writer.writerow(["B23025", key, order, point, moe, "", *replicate])
    with ZipFile(directory / "vre23.body", "w") as archive:
        archive.writestr("B23025.csv", vre.getvalue())

    player = inputs["mlb_player_id"]
    for game, ab in zip(inputs["mlb_game_ids"], (5, 4)):
        hitter = {"person": {"id": player}, "stats": {"batting": {"hits": 1, "atBats": ab}}}
        write_json(directory / f"mlb-{game}.body",
                   {"teams": {"home": {"players": {f"ID{player}": hitter}}, "away": {"players": {}}}})

    for name, spec in inputs["requests"].items():
        path = directory / f"{name}.body"
        if path.exists():
            metadata = {"request": {"url": spec["url"]}, "status": 200, "exit": 0,
                        "size": path.stat().st_size, "sha256": sha(path), "header_sha256": None}
            write_json(directory / f"{name}.json", metadata)
            spec["sha256"] = sha(path)


def packet_check(directory):
    manifest = read_json(directory / "packet-manifest.json")
    private = read_json(directory / "key.json")
    positions = {entry["card_id"]: entry for entry in private["entries"]}
    assert len(positions) == 30
    assert len(bytes.fromhex(private["seed_hex"])) == 32
    assert "seed" not in (directory / "packet-manifest.json").read_text()
    statements = {}
    random_order = []
    for layer in manifest["reading_order"]:
        name = f"blind/{layer}.csv"
        path = directory / name
        assert sha(path) == manifest["files"][name]["sha256"]
        cards = read_csv(path)
        assert len(cards) == manifest["files"][name]["rows"] == 10
        chronology = []
        for card in cards:
            assert len(card) == 9 and len(card["card_id"]) == 24
            answer = positions[card["card_id"]]
            assert answer["layer"] == layer
            chrono_key = (answer["pair"], answer["case"])
            chronology.append(chrono_key)
            assert statements.setdefault(chrono_key, card["statement"]) == card["statement"]
            assert answer["correct"] == (answer["case"] == "union")
            assert bool(card["input_integers"]) == (layer != "A")
            assert bool(card["member_keys"]) == (layer == "C")
        random_order.append(chronology)
    assert len({tuple(order) for order in random_order}) == 3


def checks_on_undefined_rates():
    run = runpy.run_path(str(HERE / "run.py"))
    assert run["sum_ratio"]([(0, 0)]) is None
    assert run["sum_ratio"]([(0, 0), (1, 4)]) == Fraction(1, 4)
    assert run["mean_ratio"]([(0, 0), (1, 4)]) is None
    assert run["fraction_of"](0, 4) == Fraction(0)
    assert run["cell_token"]({"EA": None}, "EA", "EA", "row_missing") == (None, "api_null")
    assert run["cell_token"]({"EA": ""}, "EA", "EA", "row_missing") == ("", "empty_annotation")
    print("zero denominator, genuine zero, JSON null and blank annotation distinguished")


def main():
    checks_on_undefined_rates()
    committed = HERE / "inputs.json"
    with TemporaryDirectory(prefix="af238-check-") as path:
        root = Path(path)
        archived = root / "archived"
        print(invoke(committed, archived, "--attempts", HERE / "receipts" / "http-attempts.jsonl", expected=2))
        for name in ("rows.csv", "ratios.csv", "packet-manifest.json", "key.json", "receipts/state-cells.csv",
                     "blind/A.csv", "blind/B.csv", "blind/C.csv"):
            assert sha(archived / name) == sha(HERE / name), name
        print("archived failure replay: 8 byte-identical deliverables")

        inputs = read_json(committed)
        staged = root / "synthetic-downloads"
        staged.mkdir()
        fixture(staged, inputs)
        config = root / "synthetic-inputs.json"
        write_json(config, inputs)
        out = root / "synthetic-result"
        print(invoke(config, out, "--download-dir", staged, expected=0))
        rows = read_csv(out / "rows.csv")
        assert len(rows) == 48
        assert Counter(r["api_status"] for r in rows)["api_null"] == 19
        assert Counter(r["api_status"] for r in rows)["empty_annotation"] == 4
        assert Counter(r["dat_status"] for r in rows)["statistical_special"] == 1
        assert Counter(r["dat_status"] for r in rows)["zero"] == 1
        assert Counter(r["dat_status"] for r in rows)["field_absent"] == 24
        assert all(r["em_crosscheck"] == "equal" for r in rows if r["unit"] == "persons")
        assert len(read_csv(out/"receipts"/"state-cells.csv")) == 24
        ratios = {(r["pair"], r["case"]): r for r in read_csv(out/"ratios.csv")}
        ca = ratios["CA", "union"]
        assert (ca["numerator_sum"], ca["denominator_sum"], ca["value"], ca["display_percent"]) == (
            "151", "3000", "151/3000", "5.0")
        assert ratios["CA", "repeat_county"]["display_tie_with_union"] == "True"
        assert ratios["TX", "union"]["weighted_recheck"] == "600/10001"
        receipt = read_json(out/"receipts"/"replay.json")
        assert receipt["calculations"][0]["approximate"]["method"] == "ratio_plus_fallback"
        assert receipt["calculations"][0]["sdr"]["zero_denominator_replicates"] == [1]
        assert receipt["extractions"]["dat23"]["same_count_other_county"]["0"]["geo_id"] == "0500000US01001"
        assert receipt["mlb"]["calculation"]["weighted_fraction"] == "2/9"
        assert receipt["mlb"]["calculation"]["mean_fraction"] == "9/40"
        assert receipt["mlb"]["calculation"]["raw_duplicate_fraction"] == "3/14"
        assert receipt["mlb"]["calculation"]["unique_keys"] == 2
        packet_check(out)
        rerun = root/"fresh-replay"
        invoke(config, rerun, "--download-dir", staged, "--key", out / "key.json", expected=0)
        assert sha(out / "packet-manifest.json") == sha(rerun / "packet-manifest.json")
        assert sha(out / "key.json") == sha(rerun / "key.json")
        print("synthetic: all 48 slots, 6 rows, 2 ratios, SDR and fallback, 30 opaque cards, repeatable seed")

        (staged/"dat23.body").write_bytes(b"invalid\r\n")
        bad = root/"tampered-result"
        invoke(config, bad, "--download-dir", staged, expected=2)
        assert read_json(bad/"receipts"/"replay.json")["requests"]["dat23"] == "receipt_fingerprint_mismatch"
        assert read_json(bad/"packet-manifest.json")["status"] == "withheld_unverified_county_inputs"
        print("tampered DAT: refused, packet withheld")


if __name__ == "__main__":
    main()
