"""Materialize the 12 planned seats, their 48 judgments, and paired denominators."""

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

SEATS = tuple(f"{prefix}{n:02}" for prefix in ("CN", "AN", "CC", "AC") for n in range(1, 4))
CELLS = {"NR": ("narrow", "reference"), "BR": ("broad", "reference"),
         "NE": ("narrow", "exact"), "BE": ("broad", "exact")}
STATUSES = ("positive", "refuted", "absent-in-scope", "unknown")
RECOVERY = ("scope-only", "edition-only", "joint-only", "either-axis",
            "all-positive", "no-recovery", "nonmonotone", "unjudged")
REPO = {"C": "pallets/click", "A": "python-attrs/attrs"}
FLAG_NAMES = ("seat", "edition", "scope", "listed", "joint", "conflict")
MATCH_FIELDS = [
    "seat_id", "stratum", "repo", "issue_url", "cell", "scope", "edition_axis",
    "version", "catalog_id", "tag", "commit", "same_version", "recruitment",
    "candidate_ids", "related_menu_ids", "listed", "joint", "conflict", "status", "acquired_status", "C1", "C2",
    "prohibited", "environment", "evidence", "scope_outside", "missing",
    "gold_function_ids", "gold_listed_ids", "gold_join", "acquired_gold_join", "alternative_ids",
]


def read_jsonl(path):
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def index(rows, field):
    result = {row[field]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"Duplicate {field}")
    return result


def stable_dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def status(*, seat, edition, scope, listed, joint, conflict):
    if joint and (not listed or conflict):
        raise ValueError("Joint support requires a listed candidate without conflicting evidence")
    if conflict and not listed:
        raise ValueError("Direct contradiction requires a listed candidate")
    if not all((seat, edition, scope)):
        return "unknown"
    if joint:
        return "positive"
    if conflict:
        return "refuted"
    if not listed:
        return "absent-in-scope"
    return "unknown"


def run_scoring_cases(path):
    cases = json.loads(path.read_text(encoding="utf-8"))
    observations = []
    for case in cases:
        actual = status(**{key: case[key] for key in FLAG_NAMES})
        assert actual == case["expect"], (case["id"], actual, case["expect"])
        observations.append({"id": case["id"], "expected": case["expect"], "observed": actual})
    assert set(STATUSES) == {row["observed"] for row in observations}
    return observations


def pattern(values):
    if "unknown" in values:
        return "unjudged"
    nr, br, ne, be = (value == "positive" for value in values)
    if nr and br and ne and be:
        return "all-positive"
    if nr or ((br or ne) and not be):
        return "nonmonotone"
    if not be:
        return "no-recovery"
    if br and ne:
        return "either-axis"
    if br:
        return "scope-only"
    if ne:
        return "edition-only"
    return "joint-only"


def tally(matches, requests, *, status_field="status"):
    result = {}
    for stratum in ("natural", "calibration"):
        rows = [row for row in matches if row["stratum"] == stratum]
        grouped = {seat: [row for row in rows if row["seat_id"] == seat]
                   for seat in SEATS if rows and any(row["seat_id"] == seat for row in rows)}
        assert all([row["cell"] for row in seat_rows] == list(CELLS)
                   for seat_rows in grouped.values())
        seat_values = {seat: [row[status_field] for row in seat_rows]
                       for seat, seat_rows in grouped.items()}
        modes = Counter(map(pattern, seat_values.values()))
        pairs = {}
        for from_code, to_code in (("NR", "BR"), ("NE", "BE"), ("NR", "NE"), ("BR", "BE")):
            left, right = tuple(CELLS).index(from_code), tuple(CELLS).index(to_code)
            known = [(cells[left], cells[right]) for cells in seat_values.values()
                     if cells[left] != "unknown" and cells[right] != "unknown"]
            subset = [(before, after) for before, after in known if before != "positive"]
            pairs[f"{from_code}->{to_code}"] = {
                "both_observed_denom": len(known),
                "recovery_opportunity_denom": len(subset),
                "recovered": sum(after == "positive" for _, after in subset),
                "lost": sum(before == "positive" and after != "positive" for before, after in known),
            }
        result[stratum] = {
            "planned_seats": len(grouped), "planned_cell_count": len(rows),
            "recruited_seats": sum(requests[seat]["recruitment"] == "selected" for seat in grouped),
            "acquired_seats": sum(requests[seat]["recruitment"] != "vacant" for seat in grouped),
            "same_version_seats": sum(seat_rows[0]["same_version"] == "yes" for seat_rows in grouped.values()),
            "different_version_seats": sum(seat_rows[0]["same_version"] == "no" for seat_rows in grouped.values()),
            "complete": sum("unknown" not in values for values in seat_values.values()),
            "recovery_opportunity": sum("unknown" not in values and values[0] != "positive"
                                        for values in seat_values.values()),
            "cell_statuses": {
                code: {s: sum(row["cell"] == code and row[status_field] == s for row in rows) for s in STATUSES}
                for code in CELLS
            },
            "patterns": {mode: modes[mode] for mode in RECOVERY},
            "seats": {seat: {"statuses": values, "pattern": pattern(values)}
                      for seat, values in seat_values.items()},
            "pairs": pairs,
        }
    return result


def matches_for(requests, decisions, catalogs, editions, gold):
    for seat in SEATS:
        request = requests[seat]
        repo = REPO[seat[0]]
        reference = editions["reference"][repo]
        exact = request.get("exact_version") or ""
        recruited = request["recruitment"] == "selected"
        acquired = request["recruitment"] in ("selected", "provisional")
        combined = gold.get(seat, {})
        gold_ids = combined.get("function_ids") or []
        for code, (scope, axis) in CELLS.items():
            version = reference if axis == "reference" else exact
            catalog = catalogs.get((repo, version, scope))
            raw = decisions.get(f"{seat}:{code}", {})
            candidates = raw.get("candidate_ids", [])
            supported = raw.get("joint", False)
            conflict = raw.get("conflict", False)
            complete = bool(catalog and raw.get("scope_observed"))
            conditions = dict(edition=bool(version and catalog), scope=complete,
                              listed=bool(candidates), joint=supported, conflict=conflict)
            decision = status(seat=recruited, **conditions)
            acquired_decision = status(seat=acquired, **conditions)
            missing = raw.get("missing", "")
            if not acquired:
                missing = request["recruitment_reason"]
            elif not version:
                missing = "소비판 정확 배포 미확인"
            elif not catalog:
                missing = "태그 또는 고정 목록 미확인"
            elif not raw:
                missing = "공동 판독 미확인"
            elif acquired_decision == "unknown":
                assert missing, (seat, code)
            if acquired and not recruited:
                missing = "최초 게시판 미복원" + (f" · {missing}" if missing else "")
            features = catalog_function_ids(catalog) if catalog else set()
            candidate_set = set(candidates)
            assert candidate_set <= features, (seat, code, candidate_set - features)
            matched_gold_ids = sorted(set(gold_ids) & features)
            gold_join = "unopened" if not gold else "no-author-confirmation"
            if combined.get("status") == "author-confirmed":
                if not gold_ids:
                    gold_join = "no-explicit-upstream-unit"
                elif not catalog or not acquired:
                    gold_join = "unknown"
                elif set(gold_ids) <= features:
                    gold_join = "present"
                elif complete:
                    gold_join = "absent-in-scope"
                else:
                    gold_join = "unknown"
            yield {
                "seat_id": seat, "stratum": request["stratum"], "repo": repo,
                "issue_url": request.get("issue_url", ""), "cell": code,
                "scope": scope, "edition_axis": axis, "version": version,
                "catalog_id": (catalog or {}).get("id", ""), "tag": (catalog or {}).get("tag", ""),
                "commit": (catalog or {}).get("commit", ""),
                "same_version": ("yes" if exact == reference else "no") if exact else "unknown",
                "recruitment": request["recruitment"],
                "candidate_ids": "|".join(candidates),
                "related_menu_ids": "|".join(raw.get("related_menu_ids", [])),
                "listed": "yes" if candidates else ("no" if complete else "unknown"),
                "joint": "yes" if supported else ("no" if conflict or not candidates and complete else "unknown"),
                "conflict": "yes" if conflict else ("no" if supported or not candidates and complete else "unknown"),
                "status": decision, "acquired_status": acquired_decision, "C1": raw.get("C1", ""), "C2": raw.get("C2", ""),
                "prohibited": raw.get("prohibited", ""), "environment": raw.get("environment", ""),
                "evidence": raw.get("evidence", ""), "scope_outside": raw.get("scope_outside", ""),
                "missing": missing, "gold_function_ids": "|".join(gold_ids),
                "gold_listed_ids": "|".join(matched_gold_ids),
                "gold_join": gold_join if recruited or gold_join == "unopened" else "unknown",
                "acquired_gold_join": gold_join,
                "alternative_ids": "|".join(raw.get("alternative_ids", [])),
            }


def catalog_function_ids(catalog):
    return {unit["id"] for unit in catalog["features"]}


def verify_catalogs(catalog_rows):
    seen = {}
    unique_bytes = {}
    scoped_files = 0
    catalog_counts = {}
    for catalog in catalog_rows:
        key = (catalog["repo"], catalog["version"], catalog["scope"])
        assert key not in seen, key
        seen[key] = catalog
        locator = f"https://github.com/{catalog['repo']}/blob/{catalog['commit']}/"
        ids = catalog_function_ids(catalog)
        assert len(ids) == len(catalog["features"]), key
        paths = index(catalog["files"], "path")
        aliases = {name for entry in catalog["features"] for name in entry["names"]}
        locations = {(entry["id"], where["path"], where["line_start"], where["line_end"])
                     for entry in catalog["features"] for where in entry["locations"]}
        for _, path, start, end in locations:
            assert path in paths and 1 <= start <= end <= paths[path]["lines"], (key, path, start, end)
        catalog_counts[catalog["id"]] = {
            "files": len(paths), "units": len(ids), "names_without_merging": len(aliases),
            "locations_if_each_location_counted": len(locations),
            "combinations": sum(entry["kind"] != "single" for entry in catalog["features"]),
        }
        for path, record in paths.items():
            assert record["url"].startswith(locator), (path, record["url"])
            value, size = record["sha256"], record["bytes"]
            assert len(value) == 64 and size >= 0, (value, size)
            assert unique_bytes.setdefault(value, size) == size, value
            scoped_files += 1
    for (repo, version, scope), catalog in seen.items():
        if scope != "narrow":
            continue
        broad = seen[(repo, version, "broad")]
        assert catalog["commit"] == broad["commit"]
        assert catalog_function_ids(catalog) <= catalog_function_ids(broad)
        assert {f["path"] for f in catalog["files"]} <= {f["path"] for f in broad["files"]}
    return seen, {"catalog_rows": len(seen), "scoped_file_reads": scoped_files,
                  "unique_file_blobs": len(unique_bytes), "unique_source_bytes": sum(unique_bytes.values()),
                  "catalog_counts": catalog_counts}


def verify_sources(path):
    rows = read_jsonl(path)
    index(rows, "id")
    counted = [row for row in rows if row["counted"]]
    assert len({row["independent_work"] for row in counted}) == len(counted)
    for row in rows:
        assert all(row[key] for key in ("url", "version", "locator", "read_utc", "finding", "limit")), row["id"]
    return {"sources_rows": len(rows), "independent_originals": len(counted),
            "cross_domain_originals": sum(row.get("kind") == "authority" for row in counted)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--sealed", action="store_true", help="Suppress all answer input")
    parser.add_argument("--compare", action="store_true", help="Compare regenerated matches and summaries")
    args = parser.parse_args()
    root, out = args.root, args.output
    out.mkdir(parents=True, exist_ok=True)

    requests = index(read_jsonl(root / "requests.jsonl"), "seat_id")
    assert set(requests) == set(SEATS)
    decisions = index(read_jsonl(root / "evidence/initial-decisions.jsonl"), "id")
    editions = json.loads((root / "evidence/editions.json").read_text(encoding="utf-8"))
    catalogs, inventory = verify_catalogs(read_jsonl(root / "catalogs.jsonl"))
    gold_path = root / "gold.jsonl"
    gold = {} if args.sealed or not gold_path.exists() else index(read_jsonl(gold_path), "seat_id")
    assert not gold or set(gold) == set(SEATS)
    matches = list(matches_for(requests, decisions, catalogs, editions, gold))
    assert len(matches) == len(SEATS) * len(CELLS)
    assert len({(r["seat_id"], r["cell"]) for r in matches}) == len(matches)
    csv_path = out / "matches.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=MATCH_FIELDS)
        writer.writeheader()
        writer.writerows(matches)

    summary = {
        "tables": tally(matches, requests),
        "acquired_sensitivity": tally(matches, requests, status_field="acquired_status"),
        "inventory": inventory,
        "scorer_cases": run_scoring_cases(root / "fixtures/scoring-cases.json"),
        "matches_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
    }
    if (root / "sources.jsonl").exists():
        summary["sources"] = verify_sources(root / "sources.jsonl")
    result_path = out / "metrics.json"
    result_path.write_text(stable_dump(summary), encoding="utf-8")
    if args.compare:
        assert csv_path.read_bytes() == (root / "matches.csv").read_bytes()
        assert result_path.read_bytes() == (root / "evidence/metrics.json").read_bytes()
    print(stable_dump(summary), end="")


if __name__ == "__main__":
    main()
