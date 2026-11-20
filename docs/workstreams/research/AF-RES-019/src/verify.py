"""Verify the frozen research artifact, not external event correctness."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
import csv
from pathlib import Path
import subprocess

from collect import SIGNALS, STUDY, WINDOWS, load_json, save_json, utc_now

HEADERS = (
    "사건 유형 / 사건 수 / 정확한 날짜 수 / 대조군 수 / 공지→시행 선행 기간 중앙값 / git·레지스트리 신호 계산 가능 수 / 대표 사건 / 미확인",
    "신호(임계값) / 계산 가능 사건·대조 수(분모) / 사건군 경보 수 / 대조군 경보 수 / 정밀도 / 재현율 / AUC(95% 구간) / 선행 기간 중앙값 / 대표 놓침 / 대표 오경보 / 015 당일 결과 / 미확인",
    "방식·주기 / 항목당 요청 수 / 항목당 시간(초) / 항목당 내려받은 바이트 / 발견 지연 중앙값(사건 수) / 놓친 사건 수 / 1만 항목 외삽 비용 / 미확인",
    "015 이유 유형 / 015 분모 / 대응하는 사건 유형 / 이번 신호로 덮이는가 / 덮이는 이유 수와 비율 / 덮이지 않는 이유 / 미확인",
    "주장 / 근거 자료 주소 / 확인한 내용 / 반증 시도 / 미확인",
)
BASE = "ded7f3838fe16f1cf401789e99e957b1ebebff1b"
OWNED = "docs/workstreams/research/AF-RES-019/"


def csv_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def check():
    events = load_json(STUDY / "events/EVENTS.json")
    controls = load_json(STUDY / "controls/CONTROLS.json")
    bibliography = load_json(STUDY / "sources.json")
    sources = {r["id"]: r for r in bibliography["sources"]}
    assert len(sources) == len(bibliography["sources"])
    by_type = Counter(e["type"] for e in events)
    ecosystems = Counter(e["ecosystem"] for e in events)
    organizations = Counter(e["organization"] for e in events)
    exact = sum(bool(e["effective_date"]) and e["date_precision"] == "day" for e in events)
    assert len(by_type) >= 5 and min(by_type.values()) >= 8 and exact >= 30
    assert len(ecosystems) >= 4 and max(ecosystems.values()) <= len(events) * .4
    assert max(organizations.values()) <= 2
    assert all(e["source_ids"] and all(sid in sources for sid in e["source_ids"]) for e in events)
    assert {e["id"] for e in events} == {c["matched_event"] for c in controls}
    complete = [c for c in controls if c["status"] == "strict"]
    assert all(c["matching_fields"]["first_commit_year_distance"] <= 2
               and c["matching_fields"]["author_bin_equal"]
               and c["matching_fields"]["category_fit"] == "정확"
               and c["no_event_check"]["check"] == "scoped_history_supported" for c in complete)

    signals = csv_rows(STUDY / "signals/SIGNALS.csv")
    assert len(signals) == (len(events) + len(controls)) * len(SIGNALS) * len(WINDOWS)
    assert len({(row["item"], row["signal"], row["timepoint"]) for row in signals}) == len(signals)
    filled = defaultdict(set)
    for r in signals:
        assert bool(r["value"]) ^ bool(r["missing_reason"])
        if r["value"]:
            filled[r["signal"]].add((r["group"], r["timepoint"]))
    common = sorted(k for k, times in filled.items() if len(times) == 2 * len(WINDOWS))
    assert len(common) >= 8

    direct = csv_rows(STUDY / "results/cadence.csv")
    assert len(direct) == 18 and len({(r["method"], r["cadence"]) for r in direct}) == 18
    assert all(int(r["events"]) == exact for r in direct)
    auc = load_json(STUDY / "results/auc.json")
    assert len(auc["rows"]) == 2 * len(WINDOWS) * (len(SIGNALS) + 3)
    assert all((r["ci95_percentile"] is not None) == (r["pairs"] >= 2) for r in auc["rows"])

    document = (STUDY / "RESULT.md").read_text(encoding="utf-8")
    for header in HEADERS:
        assert "| " + " | ".join(header.split(" / ")) + " |" in document, header
    gap_section = document.split("## §4 ", 1)[1].split("## §5 ", 1)[0]
    assert sum(line.startswith(("1. ", "2. ", "3. ", "4. ")) for line in gap_section.splitlines()) == 3
    methods = [s for s in sources.values() if s.get("method_minimum_counted")]
    assert len(methods) >= 25 and max(Counter(s["site_for_cap"] for s in methods).values()) <= 3
    cost_rows = csv_rows(STUDY / "results/cost.csv")
    good = {r["id"] for r in cost_rows if r["status"] in ("measured", "fetched")}
    tracked = subprocess.check_output(["git", "diff", "--name-only", BASE, "HEAD"], text=True).splitlines()
    assert all(path.startswith(OWNED) for path in tracked)
    return {"at_utc": utc_now(), "format_and_scope": "pass", "events": len(events),
            "dated": exact, "event_types": dict(by_type), "selected_comparators": len(controls),
            "strict_pairs": len(complete), "signal_cells": len(signals), "signals_observed_in_both_groups_four_times": common,
            "cadence_rows": len(direct), "cost_rows": len(cost_rows), "distinct_cost_measured_items": len(good),
            "methods_after_cap": len(methods), "tracked_paths_in_scope": len(tracked)}


def main():
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    r = check()
    if args.output:
        save_json(args.output, r)
    print(r)


if __name__ == "__main__":
    main()
