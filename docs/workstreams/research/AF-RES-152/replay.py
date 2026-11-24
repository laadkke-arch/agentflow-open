"""Offline, time-gated replay of AF-RES-152 provider observations."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timedelta
from hashlib import sha256
import json
from pathlib import Path
from statistics import median

HERE = Path(__file__).resolve().parent
POLICIES = ("O", "P", "S", "F")
SCENARIOS = ("base", "no-sparse", "big-catalog", "late-recovery", "archive-catalog")
SCORES = ("correct", "stale", "false_exclusion", "unknown", "no_shelf", "deferred")


def parse_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def jsonl(path):
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest(value):
    return sha256(canonical(value).encode("utf-8")).hexdigest()


def write_json(path, value, *, sort_keys=True):
    path.write_text(json.dumps(value, sort_keys=sort_keys, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"No rows for {path.name}")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def before(events, boundary):
    """Keep the physical prefix, withholding any later channel even for early events."""
    prefix = []
    for event in events:
        if not event["comparison"] or event["replay_at_utc"] >= boundary:
            continue
        clipped = {mode: stamp if stamp and stamp < boundary else None
                   for mode, stamp in event["first_observable_utc"].items()}
        # A release unknown through every ingested channel may still be a grader candidate.
        # Preserve it for prefix evaluation, but fit() must never count it.
        prefix.append(dict(event, first_observable_utc=clipped))
    return prefix


def fit(config, prefix):
    cut = config["cut"]
    counts = dict.fromkeys(config["source_ids"], 0)
    assert prefix == before(prefix, cut), "Fit requires a physically clipped training prefix"
    for row in prefix:
        if row["kind"] == "new" and any(row["first_observable_utc"].values()):
            counts[row["supplier"]] += 1
    order = sorted(counts, key=lambda source: (-counts[source], source))
    return {"before_utc": cut, "first_advertised": counts, "order": order,
            "training_prefix_sha256": digest(prefix)}


class World:
    """Source interfaces return only material available through the requested channel."""

    def __init__(self, config, events, scenario):
        self.config = config
        self.start = parse_time(config["start"])
        self.cut = int(self.hour(config["cut"]))
        self.end = int(self.hour(config["end"]))
        self.scenario = scenario
        sparse = config["sparse_source"]
        self.sources = [s for s in config["source_ids"]
                        if scenario != "no-sparse" or s != sparse]
        self.targets = {key: target for key, target in config["targets"].items()
                        if target["supplier"] in self.sources}
        self.events = defaultdict(list)
        self.changes = defaultdict(list)
        for row in events:
            if not row["comparison"] or row["supplier"] not in self.sources:
                continue
            key = row["event_id"]
            at = self.hour(row["replay_at_utc"])
            obs = {k: self.hour(v) if v else None for k, v in row["first_observable_utc"].items()}
            if scenario == "late-recovery" and key == "PR-DEC-UP":
                at += 48
            if scenario == "late-recovery" and row["group"] == "PR-DEC":
                obs["feed"] += 48
            item = dict(row, at=at, observed=obs)
            self.events[row["supplier"]].append(item)
            if row["target"]:
                self.changes[row["target"]].append(item)
        for transitions in self.changes.values():
            transitions.sort(key=lambda row: row["at"])
        self.unknown = {key: [(self.hour(a), self.hour(b)) for a, b in spec.get("unknown_windows", [])]
                        for key, spec in self.targets.items()}
        self.costs = config["costs"]
        if scenario == "big-catalog":
            factors = {"catalog": 3, "feed": 2, "body": 2}
            self.costs = {key: [n, size * factors[key], seconds]
                          for key, (n, size, seconds) in config["costs"].items()}

    def hour(self, value):
        return (parse_time(value) - self.start).total_seconds() / 3600

    def stamp(self, hour):
        return (self.start + timedelta(hours=hour)).isoformat().replace("+00:00", "Z")

    def phase(self, now):
        return "train" if now < self.cut else "holdout"

    def catalog(self, source, now):
        after = 0 if self.scenario == "archive-catalog" else now - self.config["catalog_lookback_hours"]
        return [self.envelope(row) for row in self.events[source]
                if row["kind"] == "new" and row["observed"]["catalog"] is not None
                and after <= row["at"] <= now and row["observed"]["catalog"] <= now]

    def feed(self, source, now, previous):
        after = now - self.config["feed_retention_hours"]
        if previous is not None:
            after = max(after, previous - self.config["cursor_overlap_hours"])
        return [self.envelope(row) for row in self.events[source]
                if row["observed"]["feed"] is not None and after <= row["observed"]["feed"] <= now]

    @staticmethod
    def envelope(row):
        return {name: row[name] for name in ("event_id", "at", "kind", "target", "signal_authority")}

    def state_at(self, target, now):
        active = None
        for row in self.changes[target]:
            if row["at"] > now:
                break
            active = row
        state = active["state"] if active else self.targets[target]["initial"]
        if any(a <= now < b for a, b in self.unknown[target]):
            state = {"meaning": None, "valid": None, "availability": "unknown", "deadline": None}
        return state, active

    def body(self, target, now):
        return self.state_at(target, now)[0]

    def latest(self, source, now):
        eligible = [(row["at"], row["event_id"]) for row in self.events[source]
                    if row["kind"] == "new" and row["at"] <= now]
        return max(eligible, default=(None, None))[1]

    def requests_on(self, distribution, day):
        use = self.config["weights"][distribution]
        topics = {f"new:{source}" for source in self.sources}
        items = [(key, weight) for key, weight in use.items()
                 if key in self.targets or key in topics]
        total = sum(weight for _, weight in items)
        seed = self.config["demand_seed"]
        for slot, (first, hours) in enumerate(((6, 6), (14, 10))):
            drive = sha256(f"{seed}/{day}/{slot}".encode()).digest()
            when = day * 24 + first + int.from_bytes(drive[0:8], "big") % hours
            draw = int.from_bytes(drive[8:16], "big") % total
            for key, weight in items:
                if draw < weight:
                    yield when, key
                    break
                draw -= weight


def usable(state, now_utc):
    deadline = state["deadline"]
    return (state["valid"] and state["availability"] == "available"
            and (not deadline or now_utc < deadline))


def grade(view, actual, now_utc, empty):
    """Grade displayability and meaning separately from the transport response."""
    if actual["valid"] is None:
        return "unknown"
    if view is None:
        return empty
    if view["valid"] is None:
        return "deferred"
    good_now = bool(actual["valid"] and actual["availability"] == "available")
    shown = usable(view, now_utc)
    if shown and (not good_now or view["meaning"] != actual["meaning"]):
        return "stale"
    if not shown and good_now:
        return "false_exclusion"
    return "correct"


class Run:
    def __init__(self, world, order, policy, budget, dist, saved=None):
        self.world = world
        self.order = [source for source in order if source in world.sources]
        self.policy, self.budget, self.dist = policy, budget, dist
        self.limit = world.config["budgets"][budget]
        self.state = saved if saved is not None else {
            "next": 0, "week_costs": {}, "catalogs": {}, "feeds": {},
            "items": {}, "events_seen": {}, "direct": {}, "pending": {},
            "body_at": {}, "body_background": {},
            "views": {key: val["initial"] for key, val in world.targets.items()},
            "targets_scored": {}, "events_scored": {}, "visit_rows": [], "request_rows": [],
        }

    def keys(self):
        return {"scenario": self.world.scenario, "policy": self.policy,
                "budget": self.budget, "distribution": self.dist}

    def spend(self, hour, mode):
        week = str(hour // 168)
        used = self.state["week_costs"].setdefault(week, [0, 0, 0])
        need = self.world.costs[mode]
        if any(past + new > cap for past, new, cap in zip(used, need, self.limit)):
            return False
        self.state["week_costs"][week] = [past + new for past, new in zip(used, need)]
        return True

    def operation(self, now, mode, key, reason):
        if not self.spend(now, mode):
            return None
        state = self.state
        world = self.world
        rows = []
        verdict = ""
        if mode == "body":
            actual = world.body(key, now)
            previous = state["views"][key]
            verdict = actual["availability"]
            if actual["valid"] is not None:
                state["views"][key] = actual
            if self.policy in ("S", "F"):
                state["pending"].pop(key, None)
                if actual["availability"] != "available":
                    state["pending"][key] = now + 24
            state["body_at"][key] = now
            if reason != "demand":
                state["body_background"].setdefault(key, now)
            # This block records outcomes only. The scheduler never reads these maps.
            _, event = world.state_at(key, now)
            if event and actual["valid"] is not None:
                if event["kind"] != "recover" or previous["availability"] == "unavailable":
                    state["direct"].setdefault(event["event_id"], now)
        else:
            if mode == "catalog":
                rows = world.catalog(key, now)
                state["catalogs"][key] = now
            else:
                rows = world.feed(key, now, state["feeds"].get(key))
                state["feeds"][key] = now
                state["catalogs"][key] = now
            for item in rows:
                eid = item["event_id"]
                if item["kind"] == "new":
                    state["items"].setdefault(eid, [now, item["at"], key])
                elif eid not in state["events_seen"]:
                    state["events_seen"][eid] = now
                    target = item["target"]
                    state["pending"][target] = min(state["pending"].get(target, now + 1), now + 1)
        n, byte_count, seconds = world.costs[mode]
        state["visit_rows"].append(dict(
            hour=now, at_utc=world.stamp(now), phase=world.phase(now), mode=mode, key=key,
            reason=reason, requests=n, bytes=byte_count, reading_seconds=seconds,
            returned_events="|".join(x["event_id"] for x in rows), access=verdict,
            unchanged_seed=int(mode == "body" and world.targets[key]["stable"]),
        ))
        return rows if mode != "body" else actual

    def background(self, now):
        if self.policy == "O":
            return
        state = self.state
        world = self.world
        order = world.sources if now < world.cut else self.order
        if self.policy == "P":
            if now % 24 == world.config["background_hours"][0]:
                self.operation(now, "catalog", order[(now // 24) % len(order)], "background")
            else:
                keys = sorted(world.targets)
                self.operation(now, "body", keys[(now // 24) % len(keys)], "background")
            return
        sparse = world.config["sparse_source"]
        if self.policy == "F" and now % 168 == 3 and sparse in order:
            self.operation(now, "feed", sparse, "sparse_slot")
            return
        for target, due in sorted(state["pending"].items(), key=lambda x: (x[1], x[0])):
            if due <= now and self.operation(now, "body", target, "follow_up") is not None:
                return
        feeds = state["feeds"]
        if self.policy == "F":
            order = sorted(order, key=lambda source: feeds.get(source, -1))
        for source in order:
            if now - feeds.get(source, -1000) >= 72:
                self.operation(now, "feed", source, "background")
                break

    def request(self, now, key):
        world = self.world
        state = self.state
        cold = self.policy == "O"
        spend_outcome = "cache"
        old = ""
        first_untouched_stable = False
        stable_no_background = False
        if key.startswith("new:"):
            source = key.split(":", 1)[1]
            last = state["catalogs"].get(source, -1000)
            read = None
            if cold or now - last >= world.config["demand_topic_ttl_hours"]:
                read = self.operation(now, "catalog", source, "demand")
                spend_outcome = "read" if read is not None else "budget"
            if cold:
                visible = [(row["at"], row["event_id"]) for row in read or []]
            else:
                visible = [(at, eid) for eid, (_, at, supplier) in state["items"].items()
                           if supplier == source]
            old = max(visible, default=(None, None))[1]
            expected = world.latest(source, now)
            if expected is None:
                value = "no_reference"
            elif old is None:
                value = "deferred"
            else:
                value = "correct" if old == expected else "stale"
        else:
            source = world.targets[key]["supplier"]
            stable_no_background = world.targets[key]["stable"] and key not in state["body_background"]
            last = state["body_at"].get(key, 0)
            if cold or now - last >= world.config["demand_target_ttl_hours"]:
                first_untouched_stable = world.targets[key]["stable"] and key not in state["body_at"]
                read = self.operation(now, "body", key, "demand")
                spend_outcome = "read" if read is not None else "budget"
            view = state["views"][key]
            actual = world.body(key, now)
            expected = actual["meaning"]
            if cold and spend_outcome != "read":
                view = None
            if spend_outcome == "read" and actual["valid"] is None:
                view = actual
            old = view["meaning"] if view is not None else None
            value = grade(view, actual, world.stamp(now), "deferred")
        state["request_rows"].append(dict(
            hour=now, at_utc=world.stamp(now), phase=world.phase(now), supplier=source,
            query=key, expected=expected or "", returned=old or "", score=value,
            spend=spend_outcome, stable_first_on_demand=int(
                first_untouched_stable and value == "correct" and spend_outcome == "read"),
            stable_correct_without_background=int(stable_no_background and value == "correct"),
        ))

    def observe_tick(self, now):
        world = self.world
        state = self.state
        phase = world.phase(now)
        for target in world.targets:
            actual, event = world.state_at(target, now)
            view = None if self.policy == "O" else state["views"][target]
            value = grade(view, actual, world.stamp(now), "no_shelf")
            alarm = value == "false_exclusion" and view["availability"] == "unavailable"
            sound = bool(actual["valid"] and actual["availability"] == "available")
            tally = state["targets_scored"].setdefault(f"{phase}/{target}", {})
            tally[value] = tally.get(value, 0) + 1
            tally["valid_hours"] = tally.get("valid_hours", 0) + sound
            tally["false_alarm"] = tally.get("false_alarm", 0) + alarm
            if event:
                change = state["events_scored"].setdefault(f"{phase}/{event['event_id']}", {})
                change[value] = change.get(value, 0) + 1
                change["false_alarm"] = change.get("false_alarm", 0) + alarm

    def advance(self, end):
        world = self.world
        next_hour = self.state["next"]
        request_at = {}
        for day in range(next_hour // 24, (end + 23) // 24):
            request_at.update(world.requests_on(self.dist, day))
        for now in range(next_hour, end):
            if now % 24 in world.config["background_hours"]:
                self.background(now)
            if now in request_at:
                self.request(now, request_at[now])
            self.observe_tick(now)
        self.state["next"] = end

    def outputs(self):
        world = self.world
        state = self.state
        end = state["next"]
        for phase, begin, stop in [("train", 0, min(end, world.cut)),
                                   ("holdout", world.cut, end)]:
            if stop <= begin:
                continue
            for supplier in world.sources:
                for event in world.events[supplier]:
                    if not begin <= event["at"] < stop:
                        continue
                    yield self.event_row(phase, stop, event)
            for key, spec in world.targets.items():
                counts = state["targets_scored"][f"{phase}/{key}"]
                yield dict(self.keys(), phase=phase, supplier=spec["supplier"], id=key,
                           kind="stable" if spec["stable"] else "target", original_url=spec["url"],
                           evidence_ids="|".join(spec["source_ids"]), anchor_utc=world.stamp(begin),
                           signal_utc="", first_seen_utc="", direct_utc="", status="target_hours",
                           delay_h="", visible_delay_h="", censored_at_h="",
                           hours=sum(counts.get(k, 0) for k in SCORES), valid_hours=counts["valid_hours"],
                           stale_hours=counts.get("stale", 0),
                           false_exclusion_hours=counts.get("false_exclusion", 0),
                           false_alarm_hours=counts.get("false_alarm", 0),
                           unknown_hours=counts.get("unknown", 0),
                           no_shelf_hours=counts.get("no_shelf", 0))

    def event_row(self, phase, stop, event):
        world = self.world
        state = self.state
        eid = event["event_id"]
        first_signal = state["events_seen"].get(eid, stop)
        first_direct = state["direct"].get(eid, stop)
        origin = event["at"]
        available = [v for v in event["observed"].values() if v is not None]
        observable = min(available, default=None)
        if event["kind"] == "new":
            seen = state["items"].get(eid, [stop])[0]
            status = "found" if seen < stop else ("outside_view" if observable is None or observable >= stop else "unfound")
        else:
            seen = min(first_signal, first_direct)
            if first_direct < stop:
                status = "direct"
            elif first_signal < stop:
                status = "notice_only"
            else:
                status = "unjudged"
        hourly = state["events_scored"].get(f"{phase}/{eid}", {})
        return dict(self.keys(), phase=phase, supplier=event["supplier"], id=eid,
                    kind=event["kind"], original_url=event["original_url"],
                    evidence_ids="|".join(event["source_ids"]), anchor_utc=world.stamp(origin),
                    signal_utc=world.stamp(observable) if observable is not None and observable < stop else "",
                    first_seen_utc=world.stamp(seen) if seen < stop else "",
                    direct_utc=world.stamp(first_direct) if first_direct < stop else "", status=status,
                    delay_h=round(seen-origin, 3) if seen < stop else "",
                    visible_delay_h=round(seen-observable, 3) if seen < stop and observable is not None and seen >= observable else "",
                    censored_at_h=round(stop-origin, 3) if seen >= stop else "",
                    hours=sum(hourly.get(k, 0) for k in SCORES), valid_hours="",
                    stale_hours=hourly.get("stale", 0),
                    false_exclusion_hours=hourly.get("false_exclusion", 0),
                    false_alarm_hours=hourly.get("false_alarm", 0),
                    unknown_hours=hourly.get("unknown", 0), no_shelf_hours=hourly.get("no_shelf", 0))


def summarize(run, outcomes, visits, requests):
    for phase in ("train", "holdout"):
        phase_visits = [v for v in visits if v["phase"] == phase]
        phase_requests = [r for r in requests if r["phase"] == phase]
        phase_outcomes = [o for o in outcomes if o["phase"] == phase]
        if not phase_outcomes:
            continue
        for layer in ("all", *run.world.sources):
            vs = [v for v in phase_visits if layer == "all" or v["supplier"] == layer]
            req = [r for r in phase_requests if layer == "all" or r["supplier"] == layer]
            rows = [o for o in phase_outcomes if layer == "all" or o["supplier"] == layer]
            news = [o for o in rows if o["kind"] == "new"]
            found = [o for o in news if o["status"] == "found"]
            changes = [o for o in rows if o["kind"] in ("down", "recover", "meaning")]
            recovery = [o for o in changes if o["kind"] == "recover"]
            target_rows = [o for o in rows if o["kind"] in ("target", "stable")]
            checks = Counter(r["score"] for r in req)
            waiting = [o["delay_h"] for o in found]
            rc_delays = [round(run.world.hour(o["direct_utc"]) - run.world.hour(o["anchor_utc"]), 3)
                         for o in recovery if o["direct_utc"]]
            rc_notice = [o["delay_h"] for o in recovery if o["status"] == "notice_only"]
            maintenance_delays = [round(run.world.hour(o["direct_utc"]) - run.world.hour(o["anchor_utc"]), 3)
                                  for o in changes if o["direct_utc"]]
            yield dict(
                run.keys(), phase=phase, layer=layer, new_total=len(news), new_found=len(found),
                new_outside_view=sum(o["status"] == "outside_view" for o in news),
                new_unfound=len(news)-len(found),
                new_delay_median_h=median(waiting) if waiting else "",
                new_delay_max_h=max(waiting, default=""),
                new_study_end_lower_h=sum(o["censored_at_h"] for o in news if o["censored_at_h"] != ""),
                change_total=len(changes), change_direct=sum(o["status"] == "direct" for o in changes),
                change_notice_only=sum(o["status"] == "notice_only" for o in changes),
                change_unjudged=sum(o["status"] == "unjudged" for o in changes),
                change_direct_median_h=median(maintenance_delays) if maintenance_delays else "",
                recovery_total=len(recovery), recovery_direct=len(rc_delays),
                recovery_direct_median_h=median(rc_delays) if rc_delays else "",
                recovery_notice_only=sum(o["status"] == "notice_only" for o in recovery),
                recovery_notice_median_h=median(rc_notice) if rc_notice else "",
                target_hours=sum(o["hours"] for o in target_rows),
                valid_hours=sum(o["valid_hours"] for o in target_rows),
                stale_hours=sum(o["stale_hours"] for o in target_rows),
                false_exclusion_hours=sum(o["false_exclusion_hours"] for o in target_rows),
                false_alarm_hours=sum(o["false_alarm_hours"] for o in target_rows),
                unknown_hours=sum(o["unknown_hours"] for o in target_rows),
                no_shelf_hours=sum(o["no_shelf_hours"] for o in target_rows),
                user_queries=len(req), correct_queries=checks["correct"], stale_queries=checks["stale"],
                false_exclusion_queries=checks["false_exclusion"], deferred_queries=checks["deferred"],
                unknown_queries=checks["unknown"], no_reference_queries=checks["no_reference"],
                request_reads=sum(v["reason"] == "demand" for v in vs),
                stable_reads=sum(v["unchanged_seed"] for v in vs),
                stable_background_reads=sum(v["unchanged_seed"] for v in vs if v["reason"] != "demand"),
                stable_first_on_demand=sum(r["stable_first_on_demand"] for r in req),
                stable_correct_without_background=sum(r["stable_correct_without_background"] for r in req),
                stable_targets_unread=len({o["id"] for o in target_rows if o["kind"] == "stable"}
                                          - {v["key"] for v in vs if v["unchanged_seed"]}),
                requests=sum(v["requests"] for v in vs), bytes=sum(v["bytes"] for v in vs),
                reading_seconds=sum(v["reading_seconds"] for v in vs))


def execute(config, events, training, args):
    fingerprint = digest([config, events, training, args.scenario])
    world = World(config, events, args.scenario)
    end = int(world.hour(args.until)) if args.until else world.end
    if not 0 < end <= world.end:
        raise ValueError("Execution end is outside the study")
    checkpoint = read_json(args.resume) if args.resume else None
    if checkpoint and checkpoint["input_sha256"] != fingerprint:
        raise ValueError("Checkpoint inputs differ")
    if not checkpoint and training != fit(config, before(events, config["cut"])):
        raise ValueError("Training receipt disagrees with the clipped prefix")
    outputs, summaries, all_visits, all_requests = [], [], [], []
    saved = {}
    for policy in POLICIES:
        for budget in config["budgets"]:
            for dist in config["weights"]:
                key = f"{policy}/{budget}/{dist}"
                previous = checkpoint["runs"][key] if checkpoint else None
                run = Run(world, training["order"], policy, budget, dist, previous)
                if run.state["next"] > end:
                    raise ValueError("Checkpoint time exceeds the execution end")
                run.advance(end)
                if args.checkpoint:
                    saved[key] = run.state
                rows = list(run.outputs())
                visits = [dict(run.keys(), supplier=world.targets[v["key"]]["supplier"]
                               if v["mode"] == "body" else v["key"], **v)
                          for v in run.state["visit_rows"]]
                requests = [dict(run.keys(), **r) for r in run.state["request_rows"]]
                outputs.extend(rows)
                all_visits.extend(visits)
                all_requests.extend(requests)
                summaries.extend(summarize(run, rows, visits, requests))
    output = args.out
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in (("outcomes", outputs), ("metrics", summaries), ("visits", all_visits), ("requests", all_requests)):
        write_csv(output / f"{name}.csv", rows)
    if args.checkpoint:
        temp = args.checkpoint.with_suffix(".part")
        # A restart must retain the same ledger column order as a continuous run.
        write_json(temp, {"input_sha256": fingerprint, "runs": saved}, sort_keys=False)
        temp.replace(args.checkpoint)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=HERE / "config.json")
    parser.add_argument("--events", type=Path, default=HERE / "events.jsonl")
    sub = parser.add_subparsers(dest="mode", required=True)
    split_cmd = sub.add_parser("prefix")
    split_cmd.add_argument("--before")
    split_cmd.add_argument("--out", type=Path, required=True)
    fit_cmd = sub.add_parser("fit")
    fit_cmd.add_argument("--out", type=Path, required=True)
    run = sub.add_parser("run")
    run.add_argument("--out", type=Path, required=True)
    run.add_argument("--training", type=Path, default=HERE / "training.json")
    run.add_argument("--until")
    run.add_argument("--scenario", default="base", choices=SCENARIOS)
    run.add_argument("--checkpoint", type=Path)
    run.add_argument("--resume", type=Path)
    args = parser.parse_args()
    config = read_json(args.config)
    events = jsonl(args.events)
    if args.mode == "prefix":
        prefix = before(events, args.before or config["cut"])
        args.out.write_text("".join(canonical(row) + "\n" for row in prefix), encoding="utf-8")
    elif args.mode == "fit":
        write_json(args.out, fit(config, events))
    else:
        execute(config, events, read_json(args.training), args)


if __name__ == "__main__":
    main()
