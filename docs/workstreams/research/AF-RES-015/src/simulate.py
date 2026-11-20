"""Replay observed break intervals against explicitly hypothetical checking calendars."""

import calendar
import csv
import json
from collections import defaultdict
from datetime import date, timedelta
from statistics import median

from collect import ROOT, rows
from extract import upstream

AS_OF = date(2026, 11, 20)
PERIODS = {
    "월": (1, None), "분기": (3, None), "연": (12, None),
    "요청 14일 간격 가정": (None, 14), "요청 90일 간격 가정": (None, 90),
    "요청 365일 간격 가정": (None, 365), "요청 없음": (None, None),
}


def months_after(day, months):
    ordinal = day.year * 12 + day.month - 1 + months
    year, month = divmod(ordinal, 12)
    month += 1
    return date(year, month, min(day.day, calendar.monthrange(year, month)[1]))


def calendar_checks(anchor, months, days, horizon=AS_OF):
    if months is None and days is None:
        return []
    dates = []
    for step in range(1, 10001):
        when = months_after(anchor, months * step) if months else anchor + timedelta(days=days * step)
        if when > horizon:
            return dates
        dates.append(when)
    raise ValueError("unexpected calendar horizon")


def first_detection(checks, break_date):
    return next((when for when in checks if when >= break_date), None)


def event_input(reasons):
    text = upstream("CASES.json")
    roots = {thread["id"]: thread["date"] for thread in text["cases"]}
    events = {}
    for reason in reasons:
        span = reason["break_interval"]
        if reason["then_verdict"] != "성립" or reason["now_verdict"] != "무너짐" or not span:
            continue
        answer = reason["answer_date"]
        anchor_basis = "확인 답 날짜" if answer else "질문 날짜 대용(민감도만)"
        anchor = date.fromisoformat(answer or roots[reason["answer_ref"][:4]])
        begin = date.fromisoformat(span["lower_exclusive"]) + timedelta(days=1)
        end = date.fromisoformat(span["upper_inclusive"])
        begin = max(begin, anchor + timedelta(days=1))
        if begin > end:
            continue
        key = (reason["candidate"], reason["predicate"], span["lower_exclusive"],
               span["upper_inclusive"])
        event = events.setdefault(key, {"candidate": reason["candidate"], "predicate": reason["predicate"],
                                      "answer_refs": [], "anchor": anchor.isoformat(),
                                      "anchor_basis": anchor_basis, "earliest": begin.isoformat(),
                                      "latest": end.isoformat(), "source_id": span["basis"],
                                      "scope": reason["reason_direction"]})
        event["answer_refs"].append(reason["answer_ref"])
    return list(events.values())


def run(events, horizon=AS_OF):
    for event in events:
        anchor = date.fromisoformat(event["anchor"])
        start, end = (date.fromisoformat(event[k]) for k in ("earliest", "latest"))
        for mode, (month, day) in PERIODS.items():
            candidates = calendar_checks(anchor, month, day, horizon)
            # The earliest/latest events are boundary scenarios. Interior phases are not bounded by
            # their lag values. A second replay uses only the confirmatory snapshot at the upper edge.
            for scenario, change in (("early", start), ("late", end), ("first_public_proof", end)):
                detected = first_detection(candidates, change)
                yield {"event": event["candidate"], "predicate": event["predicate"],
                       "answer_refs": ",".join(event["answer_refs"]), "anchor": event["anchor"],
                       "anchor_basis": event["anchor_basis"], "scenario": scenario, "mode": mode,
                       "break_date_assumed": change.isoformat(),
                       "first_discovery": detected.isoformat() if detected else None,
                       "delay_days": (detected - change).days if detected else None,
                       "checks_through_window": len(candidates),
                       "right_censored": not detected}


def summarize(values):
    grouped = defaultdict(list)
    for row in values:
        grouped[("all", row["mode"], row["scenario"])].append(row)
        if row["anchor_basis"] == "확인 답 날짜":
            grouped[("exact_date", row["mode"], row["scenario"])].append(row)
    output = []
    for (cohort, mode, scenario), records in grouped.items():
        delays = [x["delay_days"] for x in records if x["delay_days"] is not None]
        output.append({"cohort": cohort, "mode": mode, "scenario": scenario, "n": len(records),
                       "detected": len(delays), "right_censored": len(records) - len(delays),
                       "median_delay_days": median(delays) if delays else None,
                       "checks_per_item_median": median(x["checks_through_window"] for x in records)})
    return output


def main():
    events = event_input(rows(ROOT / "REASONS.jsonl"))
    series = list(run(events))
    with (ROOT / "results" / "cadence.csv").open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(series[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(series)
    store = {"as_of": AS_OF.isoformat(), "events": events, "summary": summarize(series)}
    (ROOT / "results" / "cadence.json").write_text(json.dumps(store, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
