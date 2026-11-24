"""Recount AF-RES-152 evidence and replay ledgers without importing replay.py."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MINIMUM = {"publication": 8, "maintenance": 6, "operations": 6, "cross_field": 4}
PRIMARY = {"IETF / HTTPAPI WG": "IETF", "IETF Datatracker": "IETF", "RFC Editor / IETF": "IETF"}


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def run_key(row):
    return tuple(row[name] for name in ("policy", "budget", "distribution"))


class Audit:
    def __init__(self, inputs, output):
        self.config = json.loads((inputs / "config.json").read_text(encoding="utf-8"))
        self.start = datetime.fromisoformat(self.config["start"])
        self.cut = int(self.hour(self.config["cut"]))
        self.end = int(self.hour(self.config["end"]))
        self.targets = self.config["targets"]
        self.sources = jsonl(inputs / "sources.jsonl")
        self.events = {r["event_id"]: r for r in jsonl(inputs / "events.jsonl") if r["comparison"]}
        self.visits = defaultdict(list)
        self.requests = defaultdict(list)
        self.outcomes = defaultdict(list)
        for name in ("visits", "requests", "outcomes"):
            for row in read_csv(output / f"{name}.csv"):
                assert row["scenario"] == "base", "Baseline ledger required"
                getattr(self, name)[run_key(row)].append(row)
        self.metrics = read_csv(output / "metrics.csv")

    def hour(self, stamp):
        return (datetime.fromisoformat(stamp) - self.start).total_seconds() / 3600

    def check_sources(self):
        ids = {s["source_id"] for s in self.sources}
        assert len(ids) == len(self.sources)
        included = [s for s in self.sources if s["counted"]]
        works = {s["work_id"] for s in included}
        categories = Counter(s["kind"] for s in included)
        assert all(s["access"] == "opened" and s["url"].startswith("https://") and s["section"]
                   and s["what_verified"] and s["limits"] and len(s["read_at_utc"]) == 2
                   for s in included)
        assert len(works) == len(included) >= 24
        assert all(categories[kind] >= minimum for kind, minimum in MINIMUM.items())
        assert all(set(row["source_ids"]) <= ids for row in [*self.events.values(), *self.targets.values()])
        providers = {e["supplier"] for e in self.events.values()}
        assert len(providers) >= 3 and "mozilla" in providers
        assert sum(t["stable"] for t in self.targets.values()) >= 8
        origins = {PRIMARY.get(s["publisher"], s["publisher"]) for s in included}
        releases = [row for row in self.events.values() if row["kind"] == "new"]
        before_end = [r for r in releases if any(t and self.hour(t) < self.end
                                                for t in r["first_observable_utc"].values())]
        assert len(releases) >= len(before_end) >= 24
        return {"counted_works": len(works), "source_rows": len(self.sources),
                "classes": categories, "publisher_groups": sorted(origins), "providers": sorted(providers),
                "stable_targets": sum(t["stable"] for t in self.targets.values()),
                "natural_rows": len(self.events), "release_rows": len(releases),
                "releases_visible_within_window": len(before_end)}

    def check_visits(self, key):
        earliest = {}
        weeks = defaultdict(Counter)
        for row in self.visits[key]:
            hour = int(row["hour"])
            mode = row["mode"]
            c = [int(row[k]) for k in self.config["currencies"]]
            assert c == self.config["costs"][mode]
            weeks[hour // 168].update(dict(zip(self.config["currencies"], c)))
            for event_id in filter(None, row["returned_events"].split("|")):
                event = self.events[event_id]
                assert event["supplier"] == row["supplier"]
                observed = self.hour(event["first_observable_utc"][mode])
                assert observed <= hour, (event_id, row)
                if mode == "catalog":
                    assert event["kind"] == "new"
                    assert hour - self.config["catalog_lookback_hours"] <= self.hour(event["replay_at_utc"]) <= hour
                else:
                    assert observed >= hour - self.config["feed_retention_hours"]
                earliest.setdefault(event_id, hour)
        budgets = dict(zip(self.config["currencies"], self.config["budgets"][key[1]]))
        assert all(all(week[currency] <= cap for currency, cap in budgets.items()) for week in weeks.values())
        for row in self.outcomes[key]:
            if row["kind"] != "new":
                continue
            end = self.cut if row["phase"] == "train" else self.end
            first = earliest.get(row["id"], end)
            found = first < end
            assert (row["status"] == "found") == found
            anchor = self.hour(row["anchor_utc"])
            if found:
                assert self.hour(row["first_seen_utc"]) == first
                assert abs(float(row["delay_h"]) - (first - anchor)) < 0.001
            else:
                assert not row["first_seen_utc"]
                assert abs(float(row["censored_at_h"]) - (end - anchor)) < 0.001
        return len(weeks)

    def truth_hours(self, target):
        spec = self.targets[target]
        next_state = [(self.hour(row["replay_at_utc"]), row["state"]) for row in self.events.values()
                      if row["target"] == target]
        next_state.sort(key=lambda v: v[0])
        state = spec["initial"]
        unknown = [(self.hour(a), self.hour(b)) for a, b in spec.get("unknown_windows", ())]
        pos = 0
        for now in range(self.end):
            while pos < len(next_state) and next_state[pos][0] <= now:
                state = next_state[pos][1]
                pos += 1
            yield None if any(a <= now < b for a, b in unknown) else state

    def check_target_hours(self, key, truth):
        by_target = defaultdict(set)
        for row in self.visits[key]:
            if row["mode"] == "body":
                now = int(row["hour"])
                by_target[row["key"]].add(now)
                expected = truth[row["key"]][now]
                assert row["access"] == (expected["availability"] if expected else "unknown")
        target_rows = {(o["phase"], o["id"]): o for o in self.outcomes[key] if o["kind"] in ("stable", "target")}
        assert len(target_rows) == 2 * len(self.targets)
        for target, timeline in truth.items():
            belief = self.targets[target]["initial"]
            visits = by_target[target]
            subtotal = defaultdict(Counter)
            for now, state in enumerate(timeline):
                phase = "train" if now < self.cut else "holdout"
                scores = subtotal[phase]
                scores["hours"] += 1
                if state is None:
                    scores["unknown_hours"] += 1
                    continue
                if now in visits:
                    belief = state
                truth_good = state["valid"] and state["availability"] == "available"
                scores["valid_hours"] += truth_good
                if key[0] == "O":
                    scores["no_shelf_hours"] += 1
                    continue
                local_deadline = self.hour(belief["deadline"]) if belief["deadline"] else self.end + 1
                belief_good = belief["valid"] and belief["availability"] == "available" and now < local_deadline
                scores["stale_hours"] += bool(belief_good and (not truth_good or belief["meaning"] != state["meaning"]))
                scores["false_exclusion_hours"] += bool(truth_good and not belief_good)
                scores["false_alarm_hours"] += bool(truth_good and belief["availability"] == "unavailable")
            for phase in ("train", "holdout"):
                row = target_rows[(phase, target)]
                for field in ("hours", "unknown_hours", "valid_hours", "no_shelf_hours", "stale_hours",
                              "false_exclusion_hours", "false_alarm_hours"):
                    assert int(row[field]) == subtotal[phase][field], (key, target, phase, field)

    def check_summary(self):
        traces = {}
        for key, rows in self.requests.items():
            trace = [(r["hour"], r["query"]) for r in rows]
            assert trace == traces.setdefault(key[2], trace), "Policies must face identical demand for each distribution"
        for row in self.metrics:
            key = run_key(row)
            phase = row["phase"]
            layer = row["layer"]
            layer_rows = [x for x in self.outcomes[key] if x["phase"] == phase
                          and (layer == "all" or x["supplier"] == layer)]
            new = [x for x in layer_rows if x["kind"] == "new"]
            target = [x for x in layer_rows if x["kind"] in ("stable", "target")]
            assert int(row["new_total"]) == len(new)
            assert int(row["new_unfound"]) == sum(x["status"] != "found" for x in new)
            visits = [x for x in self.visits[key] if x["phase"] == phase
                      and (layer == "all" or x["supplier"] == layer)]
            for c in self.config["currencies"]:
                assert int(row[c]) == sum(int(v[c]) for v in visits)
            assert int(row["target_hours"]) == sum(int(o["hours"]) for o in target)
            assert int(row["unknown_hours"]) == sum(int(o["unknown_hours"]) for o in target)
            demand = [x for x in self.requests[key] if x["phase"] == phase
                      and (layer == "all" or x["supplier"] == layer)]
            assert len(demand) == int(row["user_queries"])
            counts = Counter(x["score"] for x in demand)
            for status in ("correct", "stale", "false_exclusion", "deferred", "unknown", "no_reference"):
                assert counts[status] == int(row[status + "_queries"])
            if layer == "all":
                hours = self.cut if phase == "train" else self.end - self.cut
                assert len(demand) == hours // 12

    def run(self):
        source_counts = self.check_sources()
        truth = {t: list(self.truth_hours(t)) for t in self.targets}
        weeks = 0
        for key in self.visits:
            weeks += self.check_visits(key)
            self.check_target_hours(key, truth)
        self.check_summary()
        return dict(source_counts, runs=len(self.visits), run_weeks_with_spend=weeks,
                    target_ticks_holdout_per_run=len(self.targets) * (self.end - self.cut),
                    unknown_ticks_holdout_per_run=sum(sum(v is None for v in ticks[self.cut:]) for ticks in truth.values()),
                    missing_release_rows_holdout=sum(row["kind"] == "new" and row["phase"] == "holdout"
                                                      and row["status"] != "found"
                                                      for rows in self.outcomes.values() for row in rows),
                    results="verified")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inputs", type=Path, default=HERE)
    p.add_argument("--run-dir", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    result = Audit(args.inputs, args.run_dir).run()
    names = ("config.json", "sources.jsonl", "events.jsonl", "training.json", "control-input.json",
             "http-sample.csv")
    result["input_sha256"] = {n: sha256((args.inputs / n).read_bytes()).hexdigest() for n in names}
    for n in ("outcomes.csv", "metrics.csv", "requests.csv", "visits.csv"):
        result.setdefault("replay_output_sha256", {})[n] = sha256((args.run_dir / n).read_bytes()).hexdigest()
    args.out.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
