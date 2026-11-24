"""Join the frozen signals to raw-only outcomes and replay the original query sequences."""
import argparse
import collections
import csv
import itertools
import json
import pathlib
import re

from artifacts import Fetcher, ROOT, archive, sha, write_csv, write_json
from run import equality_value, read_jsonl

OL_CELLS = ("OL-CF", "OL-CL", "OL-F", "OL-L")
POLICIES = "ABCD"
SCORE = {(True, "changed"): "TP", (True, "same"): "FP", (False, "changed"): "FN", (False, "same"): "TN"}


def load_csv(path):
    with (ROOT / path).open() as file:
        return list(csv.DictReader(file))


def release_order(rows, product, order="publish"):
    return sorted((r for r in rows if r["product"] == product), key=lambda r: int(r[order + "_rank"]))


def ol_contract(releases, cache):
    controls = {}
    for row in releases:
        digest = row["source_sha256"]
        if digest not in controls:
            dist = {"tarball": row["tarball_url"], "integrity": row["tarball_integrity"], "shasum": row["tarball_npm_sha1"]}
            files, _, _ = archive(cache, dist, row["version"])
            code = files["interaction/Translate.js"]
            assert sha(code) == digest
            lines = code.decode().splitlines()
            patterns = {
                "omission": r"\bfeatures_ = options\.features !== undefined \? options\.features : null",
                "layers_guard": r"if \(options\.layers(?: && !_?this\.features_)?\)",
                "layer_passed": r"layerFilter: this\.layerFilter_",
                "filter_configured": r"\bfilter_ = options\.filter(?: && !_?this\.features_)? \? options\.filter : TRUE",
                "filter_hit": r"this\.filter_\(feature, layer\)",
                "feature_collection": r"this\.features_\.getArray\(\)",
            }
            hits = {n: [i for i, line in enumerate(lines, 1) if re.search(pattern, line)]
                    for n, pattern in patterns.items()}
            controls[digest] = ({"representative": row["version"], "url": row["tarball_url"], "lines": hits,
                                 "confirmed": all(hits.values())})
        control = "veto" if controls[digest]["confirmed"] else "unconfirmed"
        row["contract"] = {"OL-CF": control, "OL-CL": control,
                           "OL-F": row["filter_with_features"], "OL-L": row["layers_with_features"]}
    write_json(ROOT / "evidence/ol-controls-source.json", controls)


def state(before, after):
    if before is None or after is None or "unconfirmed" in (before, after):
        return "unconfirmed"
    return "same" if before == after else "changed"


def score(rows):
    counts = collections.Counter(r["score"] for r in rows)
    forced = sum(r["alarm"] == "forced" for r in rows)
    known = sum(counts[s] for s in ("TP", "FP", "FN", "TN"))
    unresolved_action = sum(r["score"] == "U" and r["alarm"] != "skip" for r in rows)
    unresolved_skip = counts["U"] - unresolved_action
    return {
        "total": len(rows), "comparable": known, "changed": counts["TP"] + counts["FN"],
        "same": counts["FP"] + counts["TN"], **{k: counts[k] for k in ("TP", "FP", "FN", "TN", "U")},
        "forced": forced, "unconfirmed_requested": unresolved_action, "unconfirmed_skipped": unresolved_skip,
        "bounds_all_unknown_changed": [counts["TP"] + unresolved_action, counts["FP"], counts["FN"] + unresolved_skip, counts["TN"]],
        "bounds_all_unknown_same": [counts["TP"], counts["FP"] + unresolved_action, counts["FN"], counts["TN"] + unresolved_skip],
    }


def digest_vector(cell):
    return json.dumps({k: equality_value(v) for k, v in cell.items()}, sort_keys=True, ensure_ascii=False)


def outputs_from_runs(runs):
    vintage = {r["version"]: r for r in runs
               if r["product"] == "d3-scale" and r["route"] == "A" and r["strategy"] == "publish-vintage"}
    browser = collections.defaultdict(dict)
    for r in runs:
        if r["product"] == "ol":
            browser[r["version"]][OL_CELLS[int(r["cell"]) - 2]] = r
    return vintage, browser


def judges(releases, signals, outputs, browser):
    by_row = {(r["product"], r["version"]): r for r in signals}
    ol = [x for x in releases if x["product"] == "ol"]
    outcome_rows = []
    for order in ("publish", "semver"):
        for left, right in itertools.pairwise(release_order(ol, "ol", order)):
            cells = {cell: state(left["contract"][cell], right["contract"][cell]) for cell in OL_CELLS}
            cells["any"] = "changed" if "changed" in cells.values() else ("unconfirmed" if "unconfirmed" in cells.values() else "same")
            both = all(r["version"] in browser for r in (left, right))
            outcome_rows.append(("ol", order, "source_contract", left["version"], right["version"], cells, both))
            measured = {}
            for cell in OL_CELLS:
                x = browser.get(left["version"], {}).get(cell)
                y = browser.get(right["version"], {}).get(cell)
                measured[cell] = state(x["category"] if x else None, y["category"] if y else None)
            measured["any"] = ("changed" if "changed" in measured.values() else
                               "unconfirmed" if "unconfirmed" in measured.values() else "same")
            outcome_rows.append(("ol", order, "browser_only", left["version"], right["version"], measured, both))
        for row in (x for x in outputs if x["order"] == order):
            cells = {k: v for k, v in row.items() if "." in k}
            outcome_rows.append(("d3-scale", order, row["strategy"], row["before"], row["after"],
                                 cells | {"any": row["state"]}, True))

    summary = collections.defaultdict(list)
    output = []
    for product, order, strategy, left, right, cells, browser_comparable in outcome_rows:
        before, after = by_row[(product, left)], by_row[(product, right)]
        assert after[order + "_previous"] == left
        for policy in POLICIES:
            alarm = after[f"{order}_{policy}"]
            action = alarm != "skip"
            for cell, outcome in cells.items():
                row = {
                    "product": product, "order": order, "evidence_mode": strategy, "before": left, "after": right,
                    "cell": cell, "expected_condition": "compare designated input and output types",
                    "evidence": ("browser_raw" if browser_comparable else "browser_pair_unmeasured") if strategy == "browser_only" else
                                "browser_and_source" if product == "ol" and browser_comparable else
                                "source_only" if product == "ol" else "node_raw",
                    "policy": policy, "outcome": outcome, "alarm": alarm,
                    "score": SCORE.get((action, outcome), "U"), "forced": alarm == "forced",
                    "doc_changed": before["text_sha256"] != after["text_sha256"],
                    "code_changed": before["implementation_sha256"] != after["implementation_sha256"],
                    "doc_bytes_for_one_cold_decision": int(after["docs_bytes"]) if policy != "A" or action else 0,
                    "hash_files_for_one_cold_decision": (1 if policy in "CD" else 0) + (int(after["code_files"]) if policy == "D" else 0),
                    "hash_file_bytes_for_one_cold_decision": (int(after["docs_bytes"]) if policy in "CD" else 0)
                        + (int(after["code_bytes"]) if policy == "D" else 0),
                    "validation_sections": int(action), "node_runs": int(action and product == "d3-scale"),
                    "map_source_review": int(action and product == "ol"), "permalink_before": before["permalink"],
                    "permalink_after": after["permalink"],
                }
                output.append(row)
                summary[(product, order, strategy, cell, policy)].append(row)
    aggregate = {"|".join(key): score(rows) for key, rows in summary.items()}
    write_csv(ROOT / "decisions.csv", output)
    write_json(ROOT / "evidence/scores.json", aggregate)
    return output


class Journey:
    def __init__(self, product, policy, signals, docs, releases, components, archive_weights):
        self.product = product
        self.policy = policy
        self.signals = {r["version"]: r for r in signals}
        self.docs = docs
        self.releases = releases
        self.components = components
        self.archive_weights = archive_weights
        self.asset_cache = set()
        self.hash_cache = set()
        self.validation = {}
        self.decisions = set()
        self.count = collections.Counter()

    def asset(self, key, kind, size):
        if key in self.asset_cache:
            self.count["asset_reuses"] += 1
        else:
            self.asset_cache.add(key)
            self.count[kind + "_bytes"] += int(size)
            self.count[kind + "_opens"] += 1

    def hash(self, source, size):
        if source in self.hash_cache:
            self.count["hash_reuses"] += 1
        else:
            self.hash_cache.add(source)
            self.count["hash_read_files"] += 1
            self.count["hash_read_bytes"] += int(size)

    def get_doc(self, version):
        doc = self.docs[version]
        acquisition = doc["file_acquisition"]
        self.asset(acquisition["url"], "document", acquisition["bytes"])

    def get_archive(self, url, size):
        self.asset(url, "archive", size)

    def scan(self, version):
        row = self.signals[version]
        if version in self.decisions:
            self.count["decision_reuses"] += 1
            return row[f"publish_{self.policy}"]
        self.decisions.add(version)
        self.count["signal_evaluations"] += 1
        if self.policy in "BCD":
            self.get_doc(version)
        if self.policy in "CD":
            self.hash((row["permalink"], "document"), row["docs_bytes"])
        if self.policy == "D":
            release = self.releases[version]
            self.get_archive(release["tarball_url"], row["archive_bytes"])
            delegates = {}
            for item in self.components[version]["components"]:
                name = item["file"].split("/")[0]
                if self.product == "d3-scale" and name != self.product:
                    url, size = self.archive_weights[version][f"node_modules/{name}"]
                    delegates[url] = size
                else:
                    url = release["tarball_url"]
                self.hash((url, item["file"]), item["bytes"])
            for url, size in delegates.items():
                self.get_archive(url, size)
        return row[f"publish_{self.policy}"]

    def verify(self, version):
        if version in self.validation:
            return
        self.get_doc(version)
        self.count["sections_read"] += 1
        if self.product == "d3-scale":
            for tarball, size in dict(self.archive_weights[version].values()).items():
                self.get_archive(tarball, size)
            self.count["node_runs"] += 1
        else:
            release = self.releases[version]
            self.get_archive(release["tarball_url"], self.signals[version]["archive_bytes"])
            self.count["map_source_reviews"] += 1
        self.validation[version] = self.signals[version]["publish_utc"]


def query_timeline(signals, scenario):
    end = len(signals)
    if scenario == "pinned":
        return [(end, signals[0]["version"])]
    if scenario == "dual":
        return [(end, r["version"]) for r in (signals[0], signals[-1]) * 3]
    latest, result = signals[0], []
    for row in signals:
        if int(row["semver_rank"]) > int(latest["semver_rank"]):
            latest = row
        result.append((int(row["publish_rank"]), latest["version"]))
    return result


def simulate(product, signals, docs, releases, components, weights, truths, browser_pins):
    rows = []
    versions = [r["version"] for r in signals]
    index = {v: i for i, v in enumerate(versions)}
    evidence = {r["version"]: r["permalink"] for r in signals}
    stamp = {r["version"]: r["hash_utc"] for r in signals}
    for scenario, policy, mode in itertools.product(("pinned", "latest", "dual"), POLICIES, ("batch", "on_request")):
        meter = Journey(product, policy, signals, docs, releases, components, weights)
        answers = {}
        seen_requests = set()
        published = 0
        for qi, (current, target) in enumerate(query_timeline(signals, scenario), 1):
            counts_before = meter.count.copy()
            if mode == "batch":
                for v in versions[published:current]:
                    alarm = meter.scan(v)
                    if alarm != "skip":
                        meter.verify(v)
                    answers[v] = next(reversed(meter.validation))
                published = current
            if target in answers:
                requested = answers[target]
                meter.count["answer_lookups"] += 1
                if target in seen_requests:
                    meter.count["answer_cache_reuses"] += 1
            else:
                earlier = [v for v in meter.validation if index[v] <= index[target]]
                previous = max(earlier, key=lambda v: index[v], default=None)
                if previous is None:
                    meter.scan(target)
                    meter.verify(target)
                else:
                    start = index[previous] + 1
                    alarms = [meter.scan(v) for v in versions[start:index[target] + 1]]
                    if any(alarm != "skip" for alarm in alarms):
                        meter.verify(target)
                requested = target if target in meter.validation else previous
                answers[target] = requested
            seen_requests.add(target)
            if requested != target:
                meter.count["carried_answers"] += 1
            candidates = [v for v in meter.validation if index[v] <= index[target]
                          and (product == "d3-scale" or v in browser_pins)]
            observed = max(candidates, key=lambda v: index[v], default="")
            if product == "ol" and target in browser_pins:
                observed = target  # independently inherited actual evidence, including if this policy did not request it
            row = {
                "product": product, "scenario": scenario, "policy": policy, "mode": mode, "request": qi,
                "available_release": versions[current - 1], "request_asof_publish_utc": releases[versions[current - 1]]["publish_utc"],
                "target": target, "target_permalink": evidence[target], "validated_version": requested,
                "dated_source_check_utc": stamp[requested], "evidence_permalink": evidence[requested],
                "last_measured_eligible_version": observed, "answer": "preserved" if truths[target] == truths[requested] else "wrong",
                "before_received_q_count": qi - 1,
            }
            row.update({k: meter.count[k] - counts_before[k] for k in meter.count})
            rows.append(row)
    return rows


def counterexamples(releases, decisions, vintage, outcomes):
    all_aba = {}
    for product in ("ol", "d3-scale"):
        ordered = release_order(releases, product)
        if product == "ol":
            series = {cell: [r["contract"][cell] for r in ordered] for cell in OL_CELLS}
        else:
            series = {cell: [equality_value(vintage[r["version"]]["outputs"][cell]) for r in ordered]
                      for cell in next(iter(vintage.values()))["outputs"]}
        all_aba[product] = {}
        for cell, values in series.items():
            triples = list(itertools.combinations(range(len(values)), 3))
            eligible = [(i, j, k) for i, j, k in triples if values[i] == values[k]]
            matches = [[ordered[t]["version"] for t in (i, j, k)] for i, j, k in eligible if values[i] != values[j]]
            all_aba[product][cell] = {"searched_triples": len(triples), "equal_endpoint_triples": len(eligible),
                                      "changed_middle_count": len(matches), "examples": matches[:10]}
    out_pairs = [r for r in outcomes if r["order"] == "publish" and r["strategy"] == "publish-vintage"]
    d3_by_v = {r["version"]: r for r in release_order(releases, "d3-scale")}
    stable_new_bytes = [[r["before"], r["after"]] for r in out_pairs if r["state"] == "same"
                        and d3_by_v[r["after"]]["entry_sha256"] != d3_by_v[r["before"]]["entry_sha256"]]
    ol_bytes = {r["version"]: r["source_sha256"] for r in release_order(releases, "ol")}
    write_json(ROOT / "evidence/counterexamples.json", {
        "equal_endpoints_changed_middle": all_aba, "scale_changed_entry_same_vector": stable_new_bytes,
        "ol_10_7_2_10_8_0_same_module": ol_bytes["10.7.2"] == ol_bytes["10.8.0"],
        "unchanged_text_changed_answer": [{k: r[k] for k in ("product", "before", "after", "permalink_before", "permalink_after")}
            for r in decisions if r["cell"] == "any" and r["order"] == "publish" and
            r["evidence_mode"] in {"source_contract", "publish-vintage"} and r["policy"] == "C" and r["score"] == "FN"],
        "changed_text_equal_answer": [{k: r[k] for k in ("product", "before", "after", "permalink_before", "permalink_after")}
            for r in decisions if r["cell"] == "any" and r["order"] == "publish" and
            r["evidence_mode"] in {"source_contract", "publish-vintage"} and r["policy"] == "C" and r["score"] == "FP"],
    })


def main(cache):
    releases = load_csv("releases.csv")
    signals = load_csv("signals.csv")
    observed = load_csv("evidence/output-comparison.csv")
    runs = read_jsonl(ROOT / "runs.jsonl")
    vintage, browser = outputs_from_runs(runs)
    ol_contract(release_order(releases, "ol"), cache)
    decisions = judges(releases, signals, observed, browser)
    sections = read_jsonl(ROOT / "evidence/sections.jsonl")
    components = read_jsonl(ROOT / "evidence/components.jsonl")
    lock = json.loads((ROOT / "replay/locks.json").read_text())
    archive_weights = {
        version: {item["path"]: (lock["base"][version]["packages"][item["path"]]["dist"]["tarball"], item["tar_bytes"])
                  for item in run["installed"]}
        for version, run in vintage.items()
    }
    queries = []
    for product in ("ol", "d3-scale"):
        ordered = release_order(releases, product)
        truth = {r["version"]: r["contract"] if product == "ol" else digest_vector(vintage[r["version"]]["outputs"])
                 for r in ordered}
        results = simulate(product, release_order(signals, product),
                           {r["version"]: r for r in sections if r["product"] == product},
                           {r["version"]: r for r in ordered},
                           {r["version"]: r for r in components if r["product"] == product}, archive_weights, truth, browser)
        queries.extend(results)
    write_csv(ROOT / "evidence/query-replay.csv", queries)
    groups = collections.defaultdict(list)
    for row in queries:
        groups[tuple(row[k] for k in ("product", "scenario", "policy", "mode"))].append(row)
    costs = []
    metrics = ("document_bytes", "document_opens", "archive_bytes", "archive_opens",
               "hash_read_files", "hash_read_bytes", "sections_read", "node_runs", "map_source_reviews",
               "asset_reuses", "hash_reuses", "answer_cache_reuses", "carried_answers", "signal_evaluations", "decision_reuses")
    for (product, scenario, policy, mode), rows in groups.items():
        start = dict.fromkeys(metrics, 0)
        for k in metrics:
            start[k] = rows[0].get(k, 0)
        replay = {k: sum(r.get(k, 0) for r in rows[1:]) for k in metrics}
        costs.append({"product": product, "scenario": scenario, "policy": policy, "mode": mode, "queries": len(rows),
                      "preserved": sum(r["answer"] == "preserved" for r in rows),
                      "wrong": sum(r["answer"] == "wrong" for r in rows),
                      **{"first_" + k: v for k, v in start.items()}, **{"repeat_" + k: v for k, v in replay.items()}})
    write_csv(ROOT / "evidence/costs.csv", costs)
    counterexamples(releases, decisions, vintage, observed)
    print(f"decisions: {len(decisions)}; queries: {len(queries)}; cost rows: {len(costs)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", required=True, type=pathlib.Path)
    main(Fetcher(parser.parse_args().cache))
