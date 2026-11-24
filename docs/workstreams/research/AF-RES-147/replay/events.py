"""Declare the same fixed event streams for every store and cache policy."""
import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SELECTION = json.loads((ROOT / "replay" / "selection.json").read_text(encoding="utf-8"))
FIXTURE = "https://af-res-147.invalid/numbers"
CAPTURE = "https://af-res-147.invalid/first-acquisition"
MIRROR = "https://af-res-147.invalid/alternate-publication"
DIGITS = {"latn": "0123456789", "arab": "٠١٢٣٤٥٦٧٨٩"}


def encoded(item):
    return json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def query_input(mode, *, role=None, literal=None, system="latn", utc=None):
    return {
        "mode": mode, "role": role, "literal": literal, "utc": utc,
        "number_system": system if role else None,
        "digits": DIGITS[system] if role else None,
        "number": {"decimal": "12.5", "group": "1234"}.get(role),
    }


def public_events(profile, positions, editions):
    prefix = {"dense": "D", "sparse": "P"}[profile]
    tick = 0
    for family in SELECTION["family_edition_order"]:
        url = SELECTION["registrations"][family]
        cells = SELECTION[family]
        catalogue = {"sequence": profile, "cohort": "public", "family": family, "url": url}
        for op in ("register", "catalog", "bookmark"):
            tick += 1
            yield {**catalogue, "id": f"{prefix}-{family}-{op.upper()}", "action": op, "at": tick}
        last = {}
        history = []
        for entry in editions[family]:
            edition = entry["edition"]
            tag = f"{prefix}-{family}-{edition}"
            tick += 1
            yield {**catalogue, "id": tag + "-PUBLISH", "action": "publish", "edition": edition,
                   "published": entry["announcement_utc"] or entry["published_date"], "at": tick}
            if int(entry["sort_order"]) not in positions:
                continue
            for cell in cells:
                key = cell["id"]
                for p in ("P1", "P2"):
                    if earlier := last.get((key, p)):
                        tick += 1
                        yield {**catalogue, "id": f"{tag}-{key}-OLD-{p}", "action": "history",
                               "target": earlier, "at": tick}
                if family == "tzdb":
                    primary = query_input("instant", utc=cell["utc"])
                    secondary = query_input("literal", literal=cell["literal"], utc=cell["utc"])
                else:
                    primary = query_input("magnitude", role=cell["role"], system=cell["number_system"])
                    secondary = query_input("literal", role=cell["role"], system=cell["number_system"],
                                            literal=cell["literal"])
                for code, p, req in (("P1", "P1", primary), ("RETRY", "P1", primary),
                                     ("P2", "P2", secondary)):
                    tick += 1
                    eid = f"{tag}-{key}-{code}"
                    predecessor = last.get((key, p))
                    yield {**catalogue, "id": eid, "action": "current", "at": tick, "selector": "latest",
                           "key": key, "project": f"{family}-{p}", "input": req, "scope": None,
                           "prior": predecessor, "retry": code == "RETRY"}
                    if code != "RETRY":
                        last[key, p] = eid
                        history.append(eid)
        for original in history:
            tick += 1
            yield {**catalogue, "id": original + "-FINAL", "action": "history",
                   "target": original, "at": tick}


def control_events(reversed_order):
    profile = "reversed" if reversed_order else "control"
    base = {"sequence": profile, "cohort": "constructed", "family": "fixture"}
    numeric = query_input("magnitude", role="decimal")
    literal = query_input("literal", role="decimal", literal=",")
    changed_input = query_input("literal", role="decimal", literal=".")
    unknown = query_input("unknown", role="decimal")

    def event(eid, at, action, url=FIXTURE, **fields):
        return {**base, "id": eid, "at": at, "action": action, "url": url, **fields}

    def query(eid, at, key, request=numeric, *, url=FIXTURE, project="calc", scope=None,
              selector="latest", prior=None, retry=False):
        return event(eid, at, "current", url, key=key, input=request, project=project, scope=scope,
                     selector=selector, prior=prior, retry=retry)

    yield event("S-REG", 0, "register")
    yield event("S-CAPTURE-REG", 0, "register", CAPTURE)
    yield event("S-UNOBS", 1, "catalog")
    yield event("S-LINK", 1, "bookmark")
    yield event("S-PUB1", 2, "publish", edition="f1")
    yield event("S-CAPTURE-PUB", 2, "publish", CAPTURE, edition="f1")
    yield query("S-BASE", 2, "primary")
    for t in (3, 4, 5, 6):
        yield query(f"S-T{t}", t, "recovery", project="recover", prior=f"S-T{t - 1}" if t > 3 else None, retry=t > 3)
        yield query(f"S-FIRST{t}", t, "recovery", url=CAPTURE, project="capture",
                    prior=f"S-FIRST{t - 1}" if t > 3 else None, retry=t > 3)
    yield query("S-ABS1", 7, "absent")
    yield query("S-OTHER", 8, "primary", literal, project="editor")
    yield query("S-ABS2", 11, "absent", prior="S-ABS1", retry=True)
    yield query("S-UNSET", 12, "primary", unknown, project="preference-missing")
    yield query("S-INPUT", 14, "primary", changed_input, project="editor", prior="S-OTHER")
    yield query("S-ALT-A", 15, "dual", scope="section-a")
    yield query("S-ALT-B", 16, "dual", project="second-format", scope="section-b")
    yield event("S-DUP1", 17, "ingest", edition="f1", key="packet", scope=None, delivery_id="pkt-repeat")
    yield event("S-DUP2", 18, "ingest", edition="f1", key="packet", scope=None, delivery_id="pkt-repeat")
    yield event("S-KNOWN-BEFORE", 19, "asof", edition="f1", key="primary", scope=None, cutoff=1)
    yield event("S-KNOWN-AFTER", 19, "asof", edition="f1", key="primary", scope=None, cutoff=2)
    yield event("S-RECON", 19, "reconstruct", edition="f1", key="primary", scope=None,
                cutoff=2, input=numeric, target="S-BASE")
    yield query("S-ENTRY-V1", 19, "entry", project="loader")
    yield event("S-PUB2", 20, "publish", edition="f2")
    yield query("S-NEXT", 20, "primary", prior="S-BASE")
    yield query("S-NEW-OBS", 20, "primary", project="another-current")
    order = ("f1", "f2") if reversed_order else ("f2", "f1")
    for t, edition in enumerate(order, 21):
        yield event("S-ARRIVE-" + edition, t, "ingest", edition=edition, key="ordered", scope=None,
                    delivery_id="pkt-" + edition)
    yield event("S-KNOWN-LATE", 23, "asof", edition="f1", key="ordered", scope=None, cutoff=21)
    yield query("S-LATE-OLD", 23, "ordered", selector="f1")
    yield query("S-LATE-NOW", 24, "ordered")
    yield query("S-LATE-P2", 25, "ordered", literal, project="editor")
    yield query("S-ENTRY-V2", 25, "entry", project="loader", prior="S-ENTRY-V1")
    yield query("S-SAME-A", 26, "same", selector="f1", scope="source-a")
    yield query("S-SAME-B", 27, "same", selector="f1", scope="source-b", project="second-format")
    yield event("S-MIRROR-REG", 27, "register", MIRROR)
    yield event("S-MIRROR-PUB", 28, "publish", MIRROR, edition="f2")
    yield query("S-MIRROR", 28, "primary", url=MIRROR)
    yield event("S-PUB3", 29, "publish", edition="f3")
    yield event("S-H-BASE", 29, "history", target="S-BASE")
    yield event("S-H-TEMP", 29, "history", target="S-T3")
    yield event("S-H-NEXT", 29, "history", target="S-NEXT")
    yield event("S-H-DUP-PROOF", 29, "history", target="S-SAME-B")
    yield query("S-OUT-NOW", 30, "primary", prior="S-NEXT")


def all_events():
    with (ROOT / "editions.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    editions = {f: [row for row in rows if row["family"] == f and row["selection"] == "included"]
                for f in SELECTION["family_edition_order"]}
    for profile, order in SELECTION["profile_edition_orders"].items():
        yield from public_events(profile, order, editions)
    yield from control_events(False)
    yield from control_events(True)
    for e in ("785", "786", "787"):
        yield {"id": "CAL-143-"+e, "sequence": "calibration", "cohort": "inherited-calibration",
               "action": "prior_observation", "edition": ".".join(e), "family": "simple-statistics",
               "url": f'https://registry.npmjs.org/simple-statistics/-/simple-statistics-{".".join(e)}.tgz'}


if __name__ == "__main__":
    for entry in all_events():
        sys.stdout.write(encoded(entry) + "\n")
