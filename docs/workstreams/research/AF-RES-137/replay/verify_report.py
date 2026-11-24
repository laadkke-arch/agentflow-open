"""Independently derive report counts from frozen public ID and experiment receipts."""

import argparse
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def page_sets(first, second):
    direct, reread, phases = defaultdict(set), defaultdict(set), defaultdict(list)
    for row in first:
        if row["kind"] not in ("threads", "metadata"):
            assert row["response_ok"]
            key = row["pr"], row["kind"]
            assert row["n"] == len(row["ids"])
            assert not direct[key].intersection(row["ids"]), key
            direct[key].update(row["ids"])
            phases["25", key].append((row["page"], len(row["ids"])))
    for row in second:
        assert row["ok"]
        if row["kind"] != "issue":
            key = row["pr"], row["kind"]
            assert not reread[key].intersection(row["ids"]), key
            reread[key].update(row["ids"])
            phases["50", key].append((row["page"], len(row["ids"])))
    assert direct == reread
    assert len(direct) == 40
    for kind, positions in phases.items():
        positions.sort()
        assert positions[-1][1] == 0, kind
        assert [page for page, _ in positions] == list(range(1, len(positions) + 1)), kind
    return direct, phases


def verify_pages(p):
    first = read_jsonl(p / "evidence/public-pages.jsonl")
    second = read_jsonl(p / "evidence/rechecked-public-pages.jsonl")
    index = read_jsonl(p / "evidence/public-index.jsonl")
    coverage = {(row["pr"], row["category"]): row for row in read_csv(p / "coverage.csv")}
    direct, phases = page_sets(first, second)
    replies = defaultdict(dict)
    review_states = Counter()
    for row in second:
        pr = row["pr"]
        if row["kind"] == "issue":
            assert len(row["pr_url"]) and int(coverage[pr, "issue_comments"]["unique"]) == row["comments"]
        for child, parent in row.get("reply_pairs", []):
            replies[pr][str(child)] = str(parent)
        review_states.update(row.get("review_states", []))
    by_pr, overlaps, seen_bodies = {}, Counter(), Counter()
    for pr, category in direct:
        if category != "inline":
            assert len(direct[pr, category]) == int(coverage[pr, category]["unique"])
            continue
        full = direct[pr, category]
        assert set(replies[pr]) <= full and set(replies[pr].values()) <= full
        assert len(replies[pr]) == int(coverage[pr, "replies"]["unique"])
        assert len(full - replies[pr].keys()) == int(coverage[pr, "inline"]["unique"])
        overlap = set()
        for label, original in (("commented", "issue_comments"), ("reviewed", "reviews"), ("committed", "commits")):
            overlap |= {f"{label}:{i}" for i in direct[pr, original]} & direct[pr, "timeline"]
        overlaps[pr] = len(overlap)
        assert overlaps[pr] == int(coverage[pr, "timeline"]["timeline_reposts"])
        by_pr[pr] = {
            "discussion": len(direct[pr, "issue_comments"]),
            "submitted_review": len(direct[pr, "reviews"]),
            "inline_root": len(full - replies[pr].keys()), "inline_reply": len(replies[pr]),
            "commit": len(direct[pr, "commits"]), "timeline": len(direct[pr, "timeline"]),
        }
    for group in (row for row in first if row["kind"] == "threads"):
        gql = {str(comment_id) for thread in group["threads"] for comment_id in thread["comment_ids"]}
        assert gql == direct[group["pr"], "inline"]
    for row in index:
        if row["body_chars"] and row["kind"] in ("metadata", "issue_comments", "reviews", "inline"):
            seen_bodies[row["pr"]] += 1
    totals = dict(sum((Counter(pr_counts) for pr_counts in by_pr.values()), Counter()))
    return index, {
        "PRs": by_pr, "totals": totals, "current_body_counts": dict(seen_bodies),
        "timeline_reposts": sum(overlaps.values()),
        "timeline_other_events": totals["timeline"] - sum(overlaps.values()),
        "review_states": dict(review_states), "verified_page_sequences": len(phases),
        "coverage_rows": len(coverage),
    }


def verify_events(p, index):
    events = read_jsonl(p / "events.jsonl")
    sources = read_jsonl(p / "sources.jsonl")
    source_ids = {source["source_id"] for source in sources}
    assert len(source_ids) == len(sources)
    work_ids = {source["work_id"] for source in sources if source["minimum_count"]}
    counted = Counter(source["minimum_bucket"] for source in sources if source["minimum_count"])
    assert len(work_ids) == sum(counted.values())
    for bucket, minimum in (("sample_pr", 8), ("supplier", 5), ("test_release", 5),
                            ("statistical_correction", 2), ("standards_correction", 2)):
        assert counted[bucket] >= minimum
    location = {(int(row["pr"]), row["id"]) for row in index}
    assert len({row["id"] for row in events}) == len(events)
    classes, findings = Counter(), Counter()
    for row in events:
        assert set(row["source_ids"]) <= source_ids
        for related in (row["proposal"], row["response_or_comparison"]):
            if related:
                assert (row["pr"], str(related["id"])) in location
        classes[row["class"]] += 1
        findings[row["verdict"]] += 1
    known_public_implementations = [r for r in events if r["class"] == "linked_public_feature"]
    strict = sum(r["verdict"] == "direct_link_runtime" and r["first_awareness"] != "unverified"
                 and bool(r["first_relevant_change"] and r["first_relevant_change"]["same_as_pr_author"])
                 for r in known_public_implementations)
    return {
        "event_rows": len(events), "cases_by_pr": dict(Counter(str(e["pr"]) for e in events)),
        "event_classes": dict(classes), "verdicts": dict(findings),
        "strict_public_runtime_examples": [r["id"] for r in known_public_implementations],
        "strict_confirmed": strict, "human_labor_reported": sum(e["human_labor_minutes"] is not None for e in events),
        "source_rows": len(sources), "source_access_success": sum(s["access_success"] for s in sources),
        "counted_works": len(work_ids), "minimum_buckets": dict(counted),
    }


def verify_runs(p):
    legacy = json.loads((p / "evidence/sparse-old-run.json").read_text())
    sparse = json.loads((p / "evidence/sparse-run.json").read_text())
    image = json.loads((p / "evidence/image-run.json").read_text())
    preimage = json.loads((p / "evidence/image-prev-run.json").read_text())
    sparse_modes = {row["case"]: row for row in sparse["rows"]}
    base = legacy["rows"][0]
    assert base["adjacency"]["values"] == sparse_modes["default"]["adjacency"]["values"]
    assert base["nodes"] == sparse_modes["default"]["nodes"]
    assert sparse_modes["array"]["star"]["sum"] == 6
    assert sparse_modes["default"]["star"]["sum"] == 10
    assert sparse_modes["matrix-array-delta"]["at_linf"] == 0
    native, *rows = image["rows"]
    assert native["case"] == "unmodified-gallery" and native["rng_seed"] is None
    assert native["output"]["shape"] == [512, 512]
    assert native["output"]["maximum"] == 1.0 and native["repeat_equal"]
    assert rows == preimage["rows"]
    boundary = {str((r["normalize"], r["clip"])): r["output"]["maximum"]
                for r in rows if r["case"] == "boundary"}
    assert boundary["(False, False)"] > boundary["(True, False)"] > boundary["(True, True)"]
    assert boundary["(True, True)"] == 1.0
    return {"compatibility_rows": len(read_csv(p / "compatibility.csv")), "boundary_maxima": boundary,
            "archive_rows": len(read_jsonl(p / "evidence/release-artifacts.jsonl")),
            "release_rows": len(read_csv(p / "releases.csv")),
            "correction_rows": len(read_csv(p / "corrections.csv"))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("owned_path", type=Path)
    p = parser.parse_args().owned_path
    index, pages = verify_pages(p)
    print(json.dumps({**pages, **verify_events(p, index), **verify_runs(p)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
