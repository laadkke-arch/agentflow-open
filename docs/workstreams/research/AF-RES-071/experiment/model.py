"""Sealed local editions and an instrumented, byte-addressed reader."""
from dataclasses import dataclass, replace
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOW = ("2010-01-01", "2010-01-31")
ITEMS = ("DAILY MEAN TEMPERATURE", "DAILY TOTAL PRECIPITATION")
DEFAULT_ORDER = ("body", "context")
BUDGET_BYTES = 64 * 1024
BUDGET_REQUESTS = 2
TRANSFORM = "quote-and-thread/1"
BASIS = {
    "A": "The transcript supports showing the preceding and following sentences in source order.",
    "B": "The threads support both requested elements and their station name throughout the requested interval.",
}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(data):
    return sha256(data).hexdigest()


def text_digest(value):
    return digest(canonical(value).encode())


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class Edition:
    object_id: str
    id: str
    tag: str
    address: str
    files: dict
    paths: dict
    order: tuple = DEFAULT_ORDER
    policy: str = "standard"
    synthetic: bool = False

    def fingerprints(self):
        return {self.paths[role]: digest(raw) for role, raw in self.files.items()}

    def materialize(self, root):
        directory = root / self.id
        directory.mkdir(exist_ok=True, parents=True)
        for role, raw in self.files.items():
            (directory / self.paths[role]).write_bytes(raw)
        return directory


@dataclass(frozen=True)
class Pair:
    id: str
    type: str
    change: str
    spec: dict
    before: Edition
    after: Edition
    main: bool
    expected: tuple
    old_recipe_public: bool = True


def baseline(spec):
    if spec["domain"] == "A":
        rows = spec["sentences"]
        context = "transcript\t" + spec["location"]
    else:
        rows = ["\t".join(row) for row in spec["threads"]]
        context = "\n".join(name + "\t" + label for name, label in spec["names"].items())
    body = "\n".join(["# lead", *rows, "# note-A", ""]).encode()
    files = {"body": body, "context": (context + "\n").encode(), "registered": b"declared sidecar\n"}
    return Edition(spec["id"], spec["id"] + ".C0", spec["edition"], f"study://{spec['id']}/report",
                   files, {"body": "body.txt", "context": "context.tsv", "registered": "declared.txt"})


def revise(edition, suffix, *, tag=None, **changes):
    return replace(edition, id=f"{edition.object_id}.{suffix}", synthetic=True,
                   tag=tag or edition.tag, **changes)


def edit(edition, suffix, role, content):
    return revise(edition, suffix, tag=f"synthetic:{suffix}",
                  files={**edition.files, role: content})


def change_answer(base, spec, suffix):
    if spec["domain"] == "A":
        original = spec["sentences"][2].encode() + b"\n"
        return edit(base, suffix, "body", base.files["body"].replace(
            original, original[:-1] + " ⟦synthetic⟧\n".encode(), 1))
    label = spec["names"][spec["answer_station"]].encode()
    return edit(base, suffix, "context", base.files["context"].replace(
        label + b"\n", label + b" [synthetic]\n", 1))


def shorten_precipitation(base, spec):
    lines = base.files["body"].decode().splitlines()
    for i, line in enumerate(lines):
        fields = line.split("\t")
        if fields[0] != ITEMS[1] or fields[3] != spec["answer_station"]:
            continue
        if fields[1] <= WINDOW[0] and fields[2] >= WINDOW[1]:
            fields[2] = "2010-01-30"
            lines[i] = "\t".join(fields)
    return edit(base, "T2-value", "body", ("\n".join(lines) + "\n").encode())


def design(specs):
    for spec in specs:
        base = baseline(spec)
        rank = int(spec["id"][1:])
        variants = []
        if rank in (1, 4):
            renamed = revise(base, "T1", address=base.address + "-renamed",
                             paths={**base.paths, "body": "renamed.txt"})
            variants.append(("T1", "rename", base, renamed, True, (False, False, True, False)))
        if rank == 1:
            edited = edit(base, "T2-note", "body", base.files["body"].replace(b"# note-A", b"# note-B"))
            variants.append(("T2", "discarded_note", base, edited, True, (False, False, False, False)))
        if rank == 2:
            edited = (change_answer(base, spec, "T2-value") if spec["domain"] == "A"
                      else shorten_precipitation(base, spec))
            variants.append(("T2", "value", base, edited, True, (True, spec["domain"] == "B", True, False)))
        if rank == 3:
            edited = edit(base, "T2-offset", "body", base.files["body"].replace(
                b"# lead\n", b"# expanded synthetic padding\n", 1))
            variants.append(("T2", "offset", base, edited, True, (False, False, True, False)))
        if rank in (1, 3):
            edited = edit(base, "T3", "registered", b"synthetic unused sidecar change\n")
            variants.append(("T3", "unopened", base, edited, True, (False, False, False, False)))
        if rank == 2:
            edited = revise(base, "T4-order", order=tuple(reversed(base.order)))
            variants.append(("T4", "load_order", base, edited, True, (False, False, False, True)))
        if rank == 4:
            policy = "reverse" if spec["domain"] == "A" else "temperature_only"
            edited = revise(base, "T4-config", policy=policy)
            variants.append(("T4", "policy", base, edited, True, (True, True, True, False)))
        if rank in (3, 4):
            edited = change_answer(base, spec, "T5-edit")
            restored = revise(base, "T5-restore")
            variants.append(("T5", "advance", base, edited, False, (True, False, True, False)))
            variants.append(("T5", "restore", edited, restored, True, (True, False, True, False)))
        for kind, change, before, after, in_main, expected in variants:
            yield Pair(f"{spec['id']}-{kind}-{change}", kind, change, spec, before, after,
                       in_main, expected, old_recipe_public=change != "policy")


class IncompleteEvidence(ValueError):
    pass


class Reader:
    def __init__(self, opener, paths):
        self.opener = opener
        self.paths = paths
        self.events = []

    def read(self, role):
        self.events.append({"event": "open", "role": role, "path": self.paths[role]})
        with self.opener(role) as handle:
            blocks = []
            while True:
                start = handle.tell()
                block = handle.read(256)
                end = handle.tell()
                self.events.append({"event": "read", "role": role, "path": self.paths[role],
                                    "start": start, "end": end,
                                    "returned_hex": block.hex(), "sha256": digest(block)})
                if not block:
                    break
                blocks.append(block)
            return b"".join(blocks)


def records(role, path, raw):
    offset = 0
    found, ignored = [], []
    for line in raw.splitlines(keepends=True):
        cell = line.rstrip(b"\r\n")
        if cell and not cell.startswith(b"#"):
            found.append({"role": role, "path": path, "start": offset,
                          "end": offset + len(cell), "text": cell.decode()})
        elif cell.startswith(b"#"):
            ignored.append({"role": role, "path": path, "kind": "ignored_note" if cell.startswith(b"# note") else "padding",
                            "start": offset, "end": offset + len(cell), "sha256": digest(cell)})
        offset += len(line)
    return found, ignored


def quote(spec, parsed, policy):
    real = parsed["body"]
    guards = [row for row in parsed["context"] if row["text"].startswith("transcript\t")]
    anchors = [i for i, row in enumerate(real) if row["text"].startswith(spec["anchor"])]
    if len(guards) != 1 or len(anchors) != 1 or not 0 < anchors[0] < len(real) - 1:
        raise IncompleteEvidence("transcript boundary or unique anchor unavailable")
    index = anchors[0]
    witness = {"source_before": real[index - 1], "source_after": real[index + 1]}
    keys = ["source_after", "source_before"] if policy == "reverse" else list(witness)
    value = {"sentences": [witness[key]["text"] for key in keys], "unit": "source sentence",
             "reason_holds": policy != "reverse"}
    cells = [{"cell": f"sentences[{i}]", "input": witness[key]} for i, key in enumerate(keys)]
    return value, cells, {"anchor": real[index], "scope": guards[0]}


def station(spec, parsed, policy):
    low, high = spec["window"]
    candidates = {}
    for row in parsed["body"]:
        element, start, end, station_id, unit = row["text"].split("\t")
        if element not in ITEMS or (policy == "temperature_only" and element == ITEMS[1]):
            continue
        if start <= low and high <= end:
            if element in candidates:
                raise IncompleteEvidence("more than one matching thread for an element")
            candidates[element] = (station_id, unit, row)
    stations = {row[0] for row in candidates.values()}
    if len(stations) != 1:
        raise IncompleteEvidence("no unique station across eligible elements")
    station_id = next(iter(stations))
    names = [row for row in parsed["context"] if row["text"].split("\t", 1)[0] == station_id]
    if len(names) != 1:
        raise IncompleteEvidence("station-name fragment unavailable")
    ordered = [element for element in ITEMS if element in candidates]
    value = {"station_id": station_id, "station": names[0]["text"].split("\t", 1)[1],
             "elements": [[element, candidates[element][1]] for element in ordered],
             "reason_holds": len(ordered) == len(ITEMS)}
    cells = [{"cell": "station", "input": names[0]}]
    cells.extend({"cell": f"elements[{i}]", "input": candidates[key][2]}
                 for i, key in enumerate(ordered))
    return value, cells, {}


def solve(spec, parsed, policy):
    return (quote if spec["domain"] == "A" else station)(spec, parsed, policy)


def execute(spec, order, policy, reader, address, tag, run_id):
    parsed = {}
    discarded = []
    for role in order:
        parsed[role], ignored = records(role, reader.paths[role], reader.read(role))
        discarded.extend(ignored)
    value, cells, guards = solve(spec, parsed, policy)
    return {"id": run_id, "address": address, "tag": tag, "transform": TRANSFORM,
            "order": list(order), "policy": policy, "trace": reader.events, "parsed": parsed,
            "cells": cells, "guards": guards, "discarded": discarded, "value": value}


def run_local(spec, edition, directory, run_id):
    reader = Reader(lambda role: (directory / edition.paths[role]).open("rb"), edition.paths)
    return execute(spec, edition.order, edition.policy, reader, edition.address, edition.tag, run_id)


def run_package(spec, package):
    reader = Reader(lambda role: BytesIO(package["files"][role].encode()), package["paths"])
    return execute(spec, package["order"], package["policy"], reader,
                   package["address"], package["tag"], "recalculation")


def link_key(address, cells):
    return [address, cells]
