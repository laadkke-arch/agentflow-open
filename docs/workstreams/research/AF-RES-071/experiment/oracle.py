"""Separate oracle for the small sealed inputs. It never imports the reader or a view."""
import csv
from datetime import date
from hashlib import sha256
from pathlib import Path
import re

CAPTURES = Path(__file__).resolve().parents[1] / "inputs"
TEMPERATURE = "DAILY MEAN TEMPERATURE"
PRECIPITATION = "DAILY TOTAL PRECIPITATION"
UNITS = {TEMPERATURE: "°C", PRECIPITATION: "mm"}


def archived_text(spec):
    rows = dict(row.split("\t", 1) for row in
                (CAPTURES / (spec["id"] + ".txt")).read_text().splitlines())
    results = [rows[f"L{number}"] for number in spec["sentence_lines"]]
    if spec["id"] == "A1":
        results = [sentence.partition(". ")[2] for sentence in results]
    return results


def archived_threads(spec):
    options = []
    names = {}
    for line in (CAPTURES / (spec["id"] + ".txt")).read_text().splitlines():
        group, contents = line.split("\t", 1)
        fields = re.split(r"\s*\|\s*", contents.strip())
        if group == "Composite Station Metadata":
            names[fields[1]] = fields[0]
        elif fields[0] == "" and len(fields) == 7:
            _, element, name, station, _, start, end = fields
            names[station] = name
            options.append((element, start.replace("/", "-"), end.replace("/", "-"),
                            station, UNITS[element]))
        elif len(fields) == 5 and fields[1].isdigit():
            name, station, _, start, end = fields
            names[station] = name
            options.append((options[-1][0], start.replace("/", "-"), end.replace("/", "-"),
                            station, UNITS[options[-1][0]]))
    return options, names


def span(edition, role, text):
    needle = text.encode()
    raw = edition.files[role]
    offset = raw.find(needle)
    assert offset >= 0 and raw.count(needle) == 1, (edition.id, role, text)
    return {"role": role, "path": edition.paths[role], "start": offset,
            "end": offset + len(needle), "text": text}


def cite(edition, role, key, text):
    return {"cell": key, "input": span(edition, role, text)}


def read_quote(spec, edition):
    original = archived_text(spec)
    first, _, last = original
    body_text = edition.files["body"].decode()
    assert first + "\n" in body_text and original[1] + "\n" in body_text
    end_variants = {last, last + " ⟦synthetic⟧"}
    present = end_variants.intersection(body_text.split("\n"))
    assert len(present) == 1
    order = [next(iter(present)), first] if edition.policy == "reverse" else [first, next(iter(present))]
    answer = {"sentences": order, "unit": "source sentence", "reason_holds": order[0] == first}
    return answer, [cite(edition, "body", f"sentences[{index}]", text) for index, text in enumerate(order)]


def read_station(spec, edition):
    expectations, source_names = archived_threads(spec)
    assert list(map(list, expectations)) == spec["threads"]
    assert source_names == spec["names"]
    raw_names = dict(csv.reader(edition.files["context"].decode().splitlines(), delimiter="\t"))
    assert all(name in {source_names[key], source_names[key] + " [synthetic]"}
               for key, name in raw_names.items())
    bounds = tuple(map(date.fromisoformat, spec["window"]))
    records = edition.files["body"].decode().splitlines()
    registry = list(csv.reader((line for line in records if not line.startswith("#")), delimiter="\t"))
    answer_id = spec["answer_station"]
    accepted = {}
    for source_row, read_row in zip(expectations, registry, strict=True):
        element, starts, ends, station, unit = read_row
        assert (element, starts, station, unit) == (source_row[0], source_row[1], source_row[3], source_row[4])
        assert ends in {source_row[2], "2010-01-30"}
        if station != answer_id or (edition.policy == "temperature_only" and element == PRECIPITATION):
            continue
        if date.fromisoformat(starts) <= bounds[0] and bounds[1] <= date.fromisoformat(ends):
            assert element not in accepted
            accepted[element] = read_row
    assert len(accepted) in (1, 2) and TEMPERATURE in accepted
    order = sorted(accepted, key=(TEMPERATURE, PRECIPITATION).index)
    answer = {"station_id": answer_id, "station": raw_names[answer_id],
              "elements": [[element, UNITS[element]] for element in order],
              "reason_holds": set(accepted) == set(UNITS)}
    cells = [cite(edition, "context", "station", answer_id + "\t" + raw_names[answer_id])]
    cells.extend(cite(edition, "body", f"elements[{i}]", "\t".join(accepted[element]))
                 for i, element in enumerate(order))
    return answer, cells


def ground(spec, edition):
    return (read_quote if spec["domain"] == "A" else read_station)(spec, edition)


def verify_observation(spec, edition, run):
    value, cells = ground(spec, edition)
    assert (run["value"], run["cells"]) == (value, cells), run["id"]
    opened = []
    received = {}
    for event in run["trace"]:
        role = event["role"]
        assert event["path"] == edition.paths[role] and role != "registered"
        if event["event"] == "open":
            assert role not in opened
            opened.append(role)
            received[role] = bytearray()
            continue
        raw = bytes.fromhex(event["returned_hex"])
        assert role == opened[-1] and event["start"] == len(received[role])
        assert event["end"] == event["start"] + len(raw)
        assert event["sha256"] == sha256(raw).hexdigest()
        received[role].extend(raw)
    assert tuple(opened) == edition.order
    assert set(received) == {"body", "context"}
    for role, raw in received.items():
        assert raw == edition.files[role]
        for parsed in run["parsed"][role]:
            assert parsed["text"].encode() == raw[parsed["start"]:parsed["end"]]
    for row in run["discarded"]:
        raw = received[row["role"]][row["start"]:row["end"]]
        assert raw.startswith(b"#") and sha256(raw).hexdigest() == row["sha256"]
    more = [*run["guards"].values(), *(cell["input"] for cell in cells)]
    assert all(fragment in run["parsed"][fragment["role"]] for fragment in more)
    return value, cells


def effects(before, after, old, new, old_trace, new_trace):
    return (old[0] != new[0], old[0]["reason_holds"] != new[0]["reason_holds"],
            (before.address, old[1]) != (after.address, new[1]),
            old_trace["order"] != new_trace["order"])
