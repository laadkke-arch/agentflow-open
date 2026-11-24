"""Check the preregistered temporal join on a verified, normalized event ledger."""

import argparse
from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
import json
from pathlib import Path
import sys


@dataclass(frozen=True)
class Event:
    location: str
    participant: str
    task: str
    document: str
    kind: str
    tick: int
    stimulus: str
    version: str
    snapshot: str
    verified: bool

    @property
    def task_key(self):
        return self.participant, self.task

    @property
    def complete_key(self):
        return all((self.participant, self.task, self.document))

    @property
    def duplicate_signature(self):
        return (self.task_key, self.document, self.kind, self.tick, self.stimulus,
                self.version, self.snapshot, self.verified)

    @property
    def is_open(self):
        return self.kind == "open" and self.verified and bool(self.stimulus and self.version)

    @property
    def is_save(self):
        return self.kind == "save" and self.verified and bool(self.version and self.snapshot)


def load_events(path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != tuple(Event.__annotations__):
            raise ValueError("unexpected normalized event columns")
        events = []
        for row in reader:
            if row["verified"] not in {"0", "1"} or row["kind"] not in {"open", "save", "display", "assignment"}:
                raise ValueError(f"unexpected event kind or verification at {row['location']}")
            events.append(Event(**{**row, "tick": int(row["tick"]), "verified": row["verified"] == "1"}))
    if len({e.location for e in events}) != len(events):
        raise ValueError("event locations must be unique")
    return events


def link(events, gap, include_multi):
    opens = sorted((e for e in events if e.is_open), key=lambda e: e.tick)
    first = opens[0]
    if len({e.document for e in events if e.is_save or e.is_open}) != 1:
        return "ambiguous_document", [first.location]
    if len(opens) > 1 and first.tick == opens[1].tick:
        return "tied_opens", [first.location, opens[1].location]

    saves = [e for e in events if e.is_save]
    before = [e for e in saves if e.tick < first.tick]
    after = [e for e in saves if e.tick > first.tick]
    if any(e.tick == first.tick for e in saves):
        return "tied_save_and_open", [first.location]
    if not before and not after:
        return "both_missing", [first.location]
    if not before:
        return "pre_missing", [first.location]
    if not after:
        return "post_missing_saves_before_open", [first.location]
    pre = max(before, key=lambda e: e.tick)
    post = min(after, key=lambda e: e.tick)
    if sum(e.tick == pre.tick for e in before) > 1 or sum(e.tick == post.tick for e in after) > 1:
        return "tied_nearest_save", [first.location]
    if min(first.tick - pre.tick, post.tick - first.tick) < gap:
        return "too_close", [pre.location, first.location, post.location]
    intervening = [e for e in events if e.kind == "open" and e.stimulus != first.stimulus
                   and first.tick <= e.tick <= post.tick]
    if intervening and not include_multi:
        return "multi_stimulus", [pre.location, first.location, post.location]
    status = "unchanged" if pre.snapshot == post.snapshot else "snapshot_changed"
    return status, [pre.location, first.location, post.location]


def audit(events, gap=1, include_multi=False):
    seen = set()
    groups = defaultdict(list)
    duplicates = missing_key_rows = 0
    for e in events:
        if e.duplicate_signature in seen:
            duplicates += 1
            continue
        seen.add(e.duplicate_signature)
        if not e.complete_key:
            missing_key_rows += 1
            continue
        groups[e.task_key].append(e)

    flow = []
    save_only = no_verified_events = 0
    for key in sorted(groups):
        task = groups[key]
        if not any(e.is_open for e in task):
            if any(e.is_save for e in task):
                save_only += 1
            else:
                no_verified_events += 1
            continue
        status, locations = link(task, gap, include_multi)
        flow.append({"slot": len(flow) + 1, "selected": len(flow) < 4,
                     "status": status, "locations": locations})
    counts = Counter(row["status"] for row in flow)
    eligible = counts["snapshot_changed"] + counts["unchanged"]
    return {
        "rows": len(events),
        "exact_duplicate_rows": duplicates,
        "orphan_missing_key_rows": missing_key_rows,
        "participant_task_keys": len(groups),
        "save_only_task_keys": save_only,
        "no_verified_event_task_keys": no_verified_events,
        "gap_in_ticks": gap,
        "include_multi_stimulus": include_multi,
        "eligible_pairs": eligible,
        "selected_eligible_pairs": sum(
            row["selected"] and row["status"] in {"snapshot_changed", "unchanged"} for row in flow
        ),
        "counts": dict(counts),
        "flow": flow,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--gap", type=int, default=1)
    parser.add_argument("--include-multi-stimulus", action="store_true")
    parser.add_argument("--expected", type=Path)
    args = parser.parse_args()
    if args.gap < 1:
        parser.error("--gap must be positive")
    result = audit(load_events(args.file), args.gap, args.include_multi_stimulus)
    if args.expected and result != json.loads(args.expected.read_text(encoding="utf-8")):
        raise SystemExit("normalized join differs from the synthetic oracle")
    json.dump(result, sys.stdout, sort_keys=True, indent=2)
    print()


if __name__ == "__main__":
    main()
