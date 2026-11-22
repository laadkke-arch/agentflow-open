"""Rebuild the AF-RES-048 views and replay the frozen two-action paths, read-only."""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def csv_rows(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def jsonl_rows(name):
    path = ROOT / name
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def load_cases():
    return json.loads((ROOT / "evidence/cases.json").read_text(encoding="utf-8"))


def group(pool, cases, *, drop_version=False):
    views = []
    for case, record in cases.items():
        known = record["status"] == "acquired"
        members = [row for row in pool if row["case"] == case and row["state"] == "observed"]
        for method in "ABC":
            keyed = {}
            for row in members:
                fields = json.loads(row["c_key"])
                if drop_version:
                    fields[3] = None
                key = {"A": row["url"], "B": row["upstream"], "C": fields}[method]
                if not key or (isinstance(key, list) and not all(key)):
                    key = ["singleton", row["id"]]
                hashable = tuple(key) if isinstance(key, list) else key
                keyed.setdefault(hashable, []).append(row["id"])
            groups = [
                {"key": list(key) if isinstance(key, tuple) else key,
                 "members": ids, "representative": ids[0]}
                for key, ids in keyed.items()
            ]
            reps = [entry["representative"] for entry in groups[:3]]
            views.append(dict(case=case, method=method, state="observed" if known else "missing",
                              label="원문 보기", description="", siblings_label="관련 링크",
                              groups=groups if known else None,
                              representatives=(reps + [None] * 3)[:3] if known else None,
                              reason=record["missing_reason"]))
    return views


def plan_paths(views, by_member, windows, cases):
    paths = {}
    for view in views:
        if view["state"] == "missing":
            continue
        case, method = view["case"], view["method"]
        reps = [item for item in view["representatives"] if item]

        def card_action(member, action):
            row = by_member[member]
            return dict(ui=action, member=member, url=row["url"], raw_href=row["raw_href"],
                        parent_sha256=cases[case]["parent_response_sha256"],
                        parent_location=row["html_line"])

        for rep in reps:
            first = card_action(rep, "representative")
            routes = [("direct", [first])]
            for other in reps:
                if other != rep:
                    routes.append(("representative_pair", [first, card_action(other, "representative")]))
            siblings = next(entry for entry in view["groups"] if entry["representative"] == rep)
            disclosure = dict(ui="siblings", member=rep, url=None, raw_href=None,
                              parent_sha256=cases[case]["parent_response_sha256"])
            for member in siblings["members"]:
                routes.append(("sibling_member", [disclosure, card_action(member, "member")]))
            window = windows[first["url"]]
            for rank, link in enumerate(window["links"][:2], 1):
                routes.append(("document_href", [first, dict(
                    ui="in_document_href", member=None, url=link["url"], raw_href=link["raw_href"],
                    parent_sha256=window["sha256"], parent_location=link["html_line"], href_rank=rank)]))
            for kind, steps in routes:
                signature = case, kind, tuple((s["ui"], s["member"], s["url"], s.get("href_rank")) for s in steps)
                if signature not in paths:
                    paths[signature] = dict(id=f"T{len(paths) + 1:03}", case=case, kind=kind, methods=[], steps=steps)
                paths[signature]["methods"].append(method)
    return list(paths.values())


class Evidence:
    def __init__(self, rows):
        self.requirements = defaultdict(set)
        self.observations = defaultdict(list)
        for row in rows:
            self.requirements[row["case"], row["alternative_id"]].add(row["atom"])
            self.observations[row["case"], row["url"]].append(row)

    def complete(self, case, urls):
        present = defaultdict(set)
        ids = []
        for url in dict.fromkeys(urls):
            for row in self.observations[case, url]:
                ids.append(row["evidence_id"])
                if row["verdict"] == "yes":
                    present[row["alternative_id"]].add(row["atom"])
        complete = sorted(alt for alt, atoms in present.items()
                          if self.requirements[case, alt] <= atoms)
        return complete, ids


def navigate(trial, windows, evidence):
    """Execute a new empty-state navigation over the stored response projections."""
    arrivals = []
    current = None
    visited = []
    action_count = 0
    for step in trial["steps"]:
        kind = step["ui"]
        if kind == "in_document_href" and (current is None or current["state"] != "arrived"):
            arrivals.append({**step, "state": "not_executed_previous_arrival", "action": None})
            continue
        action_count += 1
        if kind == "siblings":
            arrivals.append({**step, "state": "list_only", "action": action_count})
            continue
        if kind == "in_document_href":
            href = current["links"][step["href_rank"] - 1]
            assert href["raw_href"] == step["raw_href"] and href["url"] == step["url"]
            assert current["sha256"] == step["parent_sha256"]
        target = windows[step["url"]]
        current = target
        arrivals.append({**step, "state": target["state"], "action": action_count,
                         "section": target.get("section"), "arrival_sha256": target.get("sha256"),
                         "arrival_edition": target.get("edition"), "capture_id": target.get("capture_id"),
                         "fixed_asset": target.get("fixed_asset"), "error": target.get("error")})
        if target["state"] == "arrived":
            visited.append(step["url"])
    complete, proof = evidence.complete(trial["case"], visited)
    successful_landing = sum(step["state"] in ("arrived", "arrived_toc", "arrived_asset") for step in arrivals)
    failed = sum(step["state"] not in ("arrived", "arrived_toc", "arrived_asset", "list_only") for step in arrivals)
    state = "completed" if not failed else ("partial" if successful_landing else "failed")
    return dict(id=trial["id"], run_id="stored-r1", case=trial["case"], kind=trial["kind"],
                methods="".join(trial["methods"]), actions=action_count,
                state=state, successful_landings=successful_landing,
                material_landings=sum(step["state"] in ("arrived", "arrived_asset") for step in arrivals),
                complete_ids=complete,
                evidence_ids=proof, steps=arrivals)


def measure(views, trials, by_member, evidence):
    records = []
    for view in views:
        case, method = view["case"], view["method"]
        subset = [p for p in trials if p["case"] == case and method in p["methods"]]
        if view["state"] == "missing":
            records.append(dict(case=case, method=method, state="missing", representatives=None,
                                original_pool_ids=None, direct=None, reachable=None, max_in_one=None,
                                gain_direct=None, loss_direct=None, gain_reachable=None, loss_reachable=None,
                                id_trial_counts=None, trial_ids=None, hidden_known_members=None))
            continue
        original, _ = evidence.complete(case, (r["url"] for r in by_member.values()
                                               if r["case"] == case and r["state"] == "observed"))
        original = set(original)
        reachable = [set(p["complete_ids"]) & original for p in subset]
        direct = set().union(*(ids for p, ids in zip(subset, reachable) if p["kind"] == "direct"))
        any_path = set().union(*reachable)
        record = dict(case=case, method=method, state="observed", representatives=view["representatives"],
                      original_pool_ids=sorted(original), direct=sorted(direct), reachable=sorted(any_path),
                      max_in_one=max((len(x) for x in reachable), default=0),
                      id_trial_counts={alt: sum(alt in ids for ids in reachable) for alt in sorted(original)},
                      trial_ids=[p["id"] for p in subset],
                      hidden_known_members=[m for g in view["groups"] for m in g["members"]
                                            if m not in view["representatives"]])
        baseline = record if method == "A" else next(r for r in records if r["case"] == case and r["method"] == "A")
        for dst in ("direct", "reachable"):
            record[f"gain_{dst}"] = sorted(set(record[dst]) - set(baseline[dst]))
            record[f"loss_{dst}"] = sorted(set(baseline[dst]) - set(record[dst]))
        records.append(record)
    return records


def check_screen(pool, cases):
    start = json.loads((ROOT / "evidence/matplotlib-start.json").read_text(encoding="utf-8"))
    assert [r["order"] for r in start if r["order"]] == list(range(1, 21))
    scan = jsonl_rows("evidence/M-screen.jsonl.gz")
    selected = []
    for row in scan:
        if "links" not in row:
            continue
        links = row["links"]
        pairs = []
        for a, b in combinations(range(len(links)), 2):
            key = links[a]["c_key"]
            if all(key) and key == links[b]["c_key"] and links[a]["url"] != links[b]["url"]:
                pairs.append([a + 1, b + 1])
        assert sorted(pairs) == sorted(row["distinct_url_pairs"])
        if pairs:
            selected.append(row)
    assert len(selected) == 2
    for case, selection in zip(("M1", "M2"), selected):
        assert cases[case]["parent_capture"] == selection["aid"]
        from_pool = [r for r in pool if r["case"] == case and r["state"] == "observed"]
        assert [r["url"] for r in from_pool] == [r["url"] for r in selection["links"]]
        assert [r["raw_href"] for r in from_pool] == [r["raw_href"] for r in selection["links"]]
        assert [int(r["dom_ordinal"]) for r in from_pool] == [r["dom_ordinal"] for r in selection["links"]]
    return [r["order"] for r in start if r["order"]], selected


def check_captures(windows, raw_dir):
    recs = jsonl_rows("captures.jsonl") + jsonl_rows("evidence/arrival-captures.jsonl")
    hashes = {rec["acquisition_id"]: rec.get("response_sha256") for rec in recs}
    for asset in windows.values():
        if asset.get("capture_id"):
            assert asset["sha256"] == hashes[asset["capture_id"]]
    if raw_dir is None:
        return
    pinned = {r["acquisition_id"] for r in recs if r.get("fixed_asset")}
    pinned.update(v["capture_id"] for v in windows.values() if v.get("fixed_asset"))
    for key in sorted(pinned):
        data = (raw_dir / f"{key}.raw").read_bytes()
        assert hashlib.sha256(data).hexdigest() == hashes[key], key


def digest(records):
    return hashlib.sha256(json.dumps(records, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def csv_text(rows):
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: json.dumps(v, separators=(",", ":"), ensure_ascii=False)
                         if isinstance(v, (dict, list)) else v for k, v in row.items()})
    return stream.getvalue()


def smoke():
    dummy_case = {"X": {"status": "acquired", "missing_reason": ""}}
    keys = [["U", k, k, "1", "reference"] for k in ["p", "q", "r", "s", "s"]]
    sample = [dict(case="X", id=f"X-{i}", url=f"https://example.com/{i}", c_key=json.dumps(key),
                   upstream="U", state="observed") for i, key in enumerate(keys, 1)]
    a, b, c = group(sample, dummy_case)
    assert len(a["groups"]) == 5 and len(c["groups"]) == 4
    assert a["representatives"] == c["representatives"]
    assert len(b["groups"]) == 1
    assert len(group(sample, dummy_case, drop_version=True)[2]["groups"]) == 5
    sample[1]["c_key"] = sample[0]["c_key"]
    a, _, c = group(sample, dummy_case)
    assert a["representatives"] == ["X-1", "X-2", "X-3"]
    assert c["representatives"] == ["X-1", "X-3", "X-4"]
    return {"structural_only": True, "checks": 6}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials-csv", action="store_true")
    parser.add_argument("--changes-csv", action="store_true")
    parser.add_argument("--raw-dir", type=Path, help="Also verify separately downloaded original publication files")
    parser.add_argument("--smoke", action="store_true", help="Run synthetic mechanics checks only")
    args = parser.parse_args()
    if args.smoke:
        print(json.dumps(smoke()))
        return

    pool = csv_rows("pool.csv")
    cases = load_cases()
    assert len(cases) == 9 and len(pool) == 54
    for case in cases:
        assert [r["slot"] for r in pool if r["case"] == case] == [str(i) for i in range(1, 7)]
    screen_order, selection = check_screen(pool, cases)
    by_member = {row["id"]: row for row in pool}
    views = group(pool, cases)
    assert views == jsonl_rows("groups.jsonl") and len(views) == 27
    windows = {row["url"]: row for row in jsonl_rows("evidence/windows.jsonl")}
    check_captures(windows, args.raw_dir)
    plan = plan_paths(views, by_member, windows, cases)
    assert plan == jsonl_rows("evidence/trial-plan.jsonl")
    evidence = Evidence(csv_rows("gold.csv"))
    trials = [navigate(row, windows, evidence) for row in plan]
    assert all(1 <= row["actions"] <= 2 for row in trials)
    changes = measure(views, trials, by_member, evidence)

    if args.trials_csv:
        print(csv_text(trials), end="")
        return
    if args.changes_csv:
        print(csv_text(changes), end="")
        return
    for file, rows in (("trials.csv", trials), ("changes.csv", changes)):
        assert (ROOT / file).read_text(encoding="utf-8") == csv_text(rows), file
    summary = dict(run_id="stored-r1", slots=dict(Counter(r["state"] for r in pool)),
                   views=dict(Counter(v["state"] for v in views)), cases=len(cases),
                   fixed_publication_starts=screen_order,
                   selected=[(row["aid"], row["section"]["fragment"]) for row in selection],
                   pool_sha256=digest(pool), views_sha256=digest(views), plan_sha256=digest(plan),
                   trials_sha256=digest(trials), changes_sha256=digest(changes),
                   unique_planned=len(plan), applications=sum(len(p["methods"]) for p in plan),
                   kinds=dict(Counter(p["kind"] for p in plan)),
                   statuses=dict(Counter(row["state"] for row in trials)),
                   actions=sum(row["actions"] for row in trials),
                   successful_landings=sum(row["successful_landings"] for row in trials),
                   material_landings=sum(row["material_landings"] for row in trials),
                   max_actions=max(row["actions"] for row in trials),
                   out_of_budget_href_applications=len(jsonl_rows("evidence/outside-href-budget.jsonl.gz")),
                   all_display_version_fields_missing_C_views=[v["representatives"] for v in group(pool, cases, drop_version=True)
                                            if v["method"] == "C"],
                   checked_raw=args.raw_dir is not None)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
