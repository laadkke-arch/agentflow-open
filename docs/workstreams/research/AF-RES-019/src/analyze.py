"""Deterministic paired warning evaluation and interval replay for AF-RES-019."""
from argparse import ArgumentParser
from datetime import date
import csv
import gzip
import json
from pathlib import Path
import random
from statistics import median

from collect import SIGNALS, STUDY, WINDOWS, at_date, parse_day, previous_months, signal_value
from collect import load_json, save_json

COMBINATIONS = {
    "A_OR": ("or", ("git_commit_age", "git_tag_age", "git_readme_notice")),
    "B_AND": ("and", ("git_commits_90d", "git_authors_365d")),
    "C_OR": ("or", ("git_license_change", "git_package_changed")),
}
KEYS = (*SIGNALS, *COMBINATIONS)


def alert(key, value):
    if value is None:
        return None
    if key in COMBINATIONS:
        return bool(value)
    _, cutoff, direction = SIGNALS[key]
    return value * direction >= cutoff * direction


def nullable_logic(mode, states):
    if mode == "or":
        if True in states:
            return True
        return None if None in states else False
    if False in states:
        return False
    return None if None in states else True


def scalar(history, key, day):
    if key not in COMBINATIONS:
        return signal_value(history, key, day)
    mode, constituents = COMBINATIONS[key]
    value = nullable_logic(mode, [alert(k, signal_value(history, k, day)) for k in constituents])
    return int(value) if value is not None else None


def first_alert(history, key, start, stop):
    if stop < start or not history:
        return None, None
    parts = COMBINATIONS[key][1] if key in COMBINATIONS else (key,)
    checkpoints = {start}
    for part in parts:
        checkpoints.update(d for d, _ in history.get(part, ()) if start <= d <= stop)
    seen = False
    for day in sorted(checkpoints):
        state = alert(key, scalar(history, key, day))
        if state:
            return True, day
        if state is False:
            seen = True
    return (False if seen else None), None


def auc(pairs):
    if not pairs:
        return None
    cases, controls = zip(*pairs)
    return sum((a > b) + .5 * (a == b) for a in cases for b in controls) / (len(pairs) ** 2)


def quantile(values, fraction):
    if not values:
        return None
    ordered = sorted(values)
    index = fraction * (len(ordered) - 1)
    lower, upper = int(index), min(int(index) + 1, len(ordered) - 1)
    return ordered[lower] * (upper - index) + ordered[upper] * (index - lower) if upper > lower else ordered[lower]


def boot_ci(pairs, seed=19019, n=2000):
    if len(pairs) < 2:
        return None
    rng = random.Random(seed)
    samples = [auc(rng.choices(pairs, k=len(pairs))) for _ in range(n)]
    return [quantile(samples, .025), quantile(samples, .975)]


def ratio(n, d):
    return n / d if d else None


def alert_window(event, mode):
    day = date.fromisoformat(event["effective_date"])
    start = previous_months(day, 12).toordinal()
    end = day.toordinal() - 1
    if mode == "pre_announcement":
        notice = event["announce_date"]
        end = min(end, parse_day(notice) - 1) if notice else start - 1
    return start, end


def scoring_sets(events, controls):
    lookup = {row["matched_event"]: row for row in controls}
    strict = []
    augmented = []
    for event in events:
        control = lookup.get(event["id"])
        if not control or not event["effective_date"]:
            continue
        if event["type"] == "shutdown" or control["status"] in {"service_analogue", "undated"}:
            continue
        both = (event, control)
        if control["status"] == "strict":
            strict.append(both)
        augmented.append(both)
    return {"strict": strict, "exploratory_including_strict": augmented}


def evaluate(events, controls, histories):
    auc_rows, confusions, leads, trajectories = [], [], [], []
    for cohort, pairs in scoring_sets(events, controls).items():
        for key in KEYS:
            direction = SIGNALS.get(key, ("combo", 1, 1))[2]
            for m in WINDOWS:
                ranked, ids, raw = [], [], []
                for ev, ctrl in pairs:
                    day = previous_months(date.fromisoformat(ev["effective_date"]), m).toordinal()
                    a, b = tuple(scalar(histories[row["id"]], key, day) for row in (ev, ctrl))
                    if a is not None and b is not None:
                        ranked.append((a * direction, b * direction))
                        raw.append((a, b))
                        ids.append(ev["id"])
                auc_rows.append({"cohort": cohort, "signal": key, "as_of": f"T-{m}m",
                                 "pairs": len(ranked), "eligible_pairs": len(pairs),
                                 "auc": auc(ranked), "ci95_percentile": boot_ci(ranked), "event_ids": ids})
                trajectories.append({"cohort": cohort, "signal": key, "as_of": f"T-{m}m",
                                     "pairs": len(raw),
                                     "event_median": median([a for a, _ in raw]) if raw else None,
                                     "control_median": median([b for _, b in raw]) if raw else None,
                                     "paired_median_difference": median([a - b for a, b in raw]) if raw else None})
            for mode in ("pre_event", "pre_announcement"):
                cells = {k: [] for k in ("TP", "FP", "FN", "TN")}
                covered = 0
                for ev, ctrl in pairs:
                    window = alert_window(ev, mode)
                    case, control = (first_alert(histories[x["id"]], key, *window) for x in (ev, ctrl))
                    if case[0] is None or control[0] is None:
                        continue
                    covered += 1
                    for (state, day), name, item in ((case, "TP" if case[0] else "FN", ev),
                                                     (control, "FP" if control[0] else "TN", ctrl)):
                        item_id = item["id"]
                        cells[name].append(item_id)
                        leads.append({"cohort": cohort, "mode": mode, "signal": key,
                                      "item_id": item_id, "event_id": ev["id"], "classification": name,
                                      "start_utc": at_date(window[0]), "end_utc": at_date(window[1]),
                                      "first_alert": at_date(day) if day else None,
                                      "lead_days": parse_day(ev["effective_date"]) - day if day else None,
                                      "left_censored": day == window[0]})
                tp, fp, fn, tn = (len(cells[x]) for x in ("TP", "FP", "FN", "TN"))
                current_leads = [r for r in leads if r["cohort"] == cohort and r["mode"] == mode and
                                 r["signal"] == key and r["classification"] == "TP"]
                confusions.append({"cohort": cohort, "mode": mode, "signal": key,
                                   "eligible_pairs": len(pairs), "observed_pairs": covered,
                                   "TP": tp, "FP": fp, "FN": fn, "TN": tn,
                                   "precision": ratio(tp, tp + fp), "recall": ratio(tp, tp + fn),
                                   "lead_days_median": median([r["lead_days"] for r in current_leads]) if current_leads else None,
                                   "left_censored_tp": sum(r["left_censored"] for r in current_leads),
                                   "miss_example": next(iter(cells["FN"]), None),
                                   "false_alarm_example": next(iter(cells["FP"]), None),
                                   "event_alert_examples": ",".join(cells["TP"])})
    return auc_rows, confusions, leads, trajectories


def schedule(start, stop, frequency, phase=0):
    if isinstance(frequency, int):
        return range(start + phase, stop + 1, frequency)
    step = {"monthly": 1, "quarterly": 3, "yearly": 12}[frequency]
    current = date.fromordinal(start)
    month = current.year * 12 + current.month - 1
    checks = []
    while True:
        year, idx = divmod(month, 12)
        day = date(year, idx + 1, 1).toordinal()
        if day > stop:
            return checks
        if day >= start and idx % step == 0:
            checks.append(day)
        month += 1


def schedule_rows(events, histories, end, alarm="A_OR"):
    windows = ("monthly", "quarterly", "yearly", 14, 90, 365)
    result = []
    details = []
    for frequency in windows:
        phases = sorted({phase * frequency // 32 for phase in range(32)}) if isinstance(frequency, int) else [0]
        data = {m: [] for m in ("source", "signal", "signal_then_source")}
        for phase in phases:
            for event in events:
                if not event["effective_date"]:
                    continue
                eid, t = event["id"], parse_day(event["effective_date"])
                notice = min(t, parse_day(event["announce_date"])) if event["announce_date"] else t
                start, _ = alert_window(event, "pre_event")
                stop = min(t + 365, end)
                dates = schedule(start, stop, frequency, phase)
                checks = [d for d in dates if alert(alarm, scalar(histories[eid], alarm, d))]
                signals_known = any(scalar(histories[eid], alarm, d) is not None for d in dates)
                paired = {
                    "source": next((d for d in dates if d >= notice), None),
                    "signal": next(iter(checks), None),
                    "signal_then_source": next((d for d in checks if d >= notice), None),
                }
                for method, found in paired.items():
                    row = {"alarm": alarm, "method": method, "cadence": frequency if isinstance(frequency, str) else f"on_request_{frequency}d",
                           "request_phase_days": phase, "event_id": eid, "check_count": len(dates),
                           "notice_day": at_date(notice), "signal_check_count": len(checks),
                           "signal_known": signals_known, "detected_day": at_date(found) if found else None,
                           "delay_effective_days": found - t if found else None,
                           "delay_notice_days": found - notice if found else None}
                    data[method].append(row)
                    details.append(row)
        for method, rows in data.items():
            d = [item["delay_effective_days"] for item in rows if item["delay_effective_days"] is not None]
            notices = [item["delay_notice_days"] for item in rows if item["delay_notice_days"] is not None]
            miss = [sum(row["request_phase_days"] == phase and row["detected_day"] is None for row in rows)
                    for phase in phases]
            result.append({"alarm": alarm, "method": method, "cadence": rows[0]["cadence"],
                           "events": len(rows) // len(phases), "phases": len(phases), "event_phase_n": len(rows),
                           "detected_event_phases": len(d), "delay_p10_days": quantile(d, .1),
                           "delay_p50_days": quantile(d, .5), "delay_p90_days": quantile(d, .9),
                           "delay_median_notice_days": quantile(notices, .5),
                           "missed_median_events": median(miss), "missed_min_events": min(miss),
                           "missed_max_events": max(miss), "hypothetical_checks": sum(r["check_count"] for r in rows),
                           "signal_known_event_phases": sum(r["signal_known"] for r in rows),
                           "signal_positive_checks": sum(r["signal_check_count"] for r in rows)})
    return result, details


def write_csv(file, rows):
    if not rows:
        raise ValueError(f"Expected rows for {file}")
    with file.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def inputs():
    events = load_json(STUDY / "events/EVENTS.json")
    controls = load_json(STUDY / "controls/CONTROLS.json")
    histories = json.loads(gzip.decompress((STUDY / "signals/DAYS.json.gz").read_bytes()))
    return events, controls, histories


def main():
    parser = ArgumentParser()
    parser.add_argument("--results", type=Path, default=STUDY / "results")
    parser.add_argument("--only", choices=("warning", "cadence", "both"), default="both")
    parser.add_argument("--end", default="2026-11-20")
    args = parser.parse_args()
    args.results.mkdir(parents=True, exist_ok=True)
    events, controls, histories = inputs()
    if args.only in ("warning", "both"):
        auc_rows, confusions, leads, trajectories = evaluate(events, controls, histories)
        save_json(args.results / "auc.json", {"bootstrap_iterations": 2000, "seed": 19019,
                                                "unit": "same pair samples for cases and controls", "rows": auc_rows})
        write_csv(args.results / "confusion.csv", confusions)
        write_csv(args.results / "leadtime.csv", leads)
        write_csv(args.results / "trajectories.csv", trajectories)
    if args.only in ("cadence", "both"):
        cadence, details = schedule_rows(events, histories, parse_day(args.end))
        write_csv(args.results / "cadence.csv", cadence)
        write_csv(args.results / "cadence-events.csv", details)


if __name__ == "__main__":
    main()
