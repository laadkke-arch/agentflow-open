"""Join the frozen predictions with runtime ground truth and replay fixed-URL queries."""
import json
from collections import Counter, defaultdict

from common import ROOT, json_in, read_csv, write_csv, write_json
from compare import cell_fingerprint, expected_cases, index_cohort, read_runs, semantic_outcome, verified_case

EVIDENCE = ROOT / "evidence"
POLICIES = ("A", "C", "D", "E", "F", "N", "E_absence")
METRICS = (
    "document_opens", "document_body_bytes", "archive_opens", "archive_body_bytes", "archive_transfer_wall_ms",
    "archive_verify_cpu_ms", "archive_verify_wall_ms",
    "notice_inventory_checks", "notice_bundled_opens", "notice_bundled_body_bytes", "notice_section_bytes",
    "notice_github_opens", "notice_github_body_bytes", "notice_unknown_body", "notice_bundled_absent",
    "hash_files", "hash_read_bytes", "document_read_wall_ms", "static_cpu_ms", "static_wall_ms", "function_ast_runs",
    "executions", "installations", "node_cpu_ms", "node_wall_ms", "install_cpu_ms", "install_wall_ms",
    "answer_cache_hits", "asset_cache_hits", "hash_cache_hits", "decision_cache_hits", "evaluated_edges",
    "forced_edges_read", "notice_time_forced_edges_read", "absence_sensitivity_forced_edges_read",
    "forced_executions", "carries", "correct", "wrong_carry", "held",
)


def stage(policy, row):
    if policy == "E_absence":
        return "force" if row["current_only_absence"] == "True" else row["E"]
    return row[policy]


def confusion(prediction, state):
    if state == "unknown":
        return "unknown"
    if prediction == "skip":
        return "FN" if state == "changed" else "TN"
    return "TP" if state == "changed" else "FP"


def lookup_signals():
    data = {}
    for row in read_csv(ROOT / "signals.csv"):
        data[row["order"], row["version"], row["function"]] = row
    for (order, version, function), row in data.items():
        if function == "any":
            row["current_only_absence"] = data[order, version, "quantile"]["current_only_absence"]
    return data


def load_details():
    details = defaultdict(dict)
    for row in read_runs(EVIDENCE / "signal-components.jsonl"):
        details[row["version"]][row["function"]] = row
    return details


def join_outputs(signals, details):
    comparison = read_csv(EVIDENCE / "output-comparison.csv")
    pairs = read_csv(EVIDENCE / "output-pairs.csv")
    counts = defaultdict(Counter)
    decisions = []
    truth = [(row, row["function"]) for row in comparison]
    for row in pairs:
        truth.extend((row | {"cell": name, "state": state}, name) for name, state in
                     (("any", row["state"]), ("quantile", row["quantile_state"]), ("median", row["median_state"])))
    for row, function in truth:
        order, before, after = (row[key] for key in ("order", "before", "after"))
        signal = signals[order, after, function]
        joint = signals[order, after, "any"]
        known = row["state"]
        response = {"order": order, "before": before, "after": after, "cell": row["cell"], "function": function,
                    "state": known, "outcome_delta": row.get("outcome_delta"), "array_state_delta": row.get("array_state_delta"),
                    "raw_run_ids": row["raw_run_ids"]}
        for policy in POLICIES:
            response[policy + "_function_action"] = stage(policy, signal)
            response[policy + "_package_action"] = stage(policy, joint)
            for level, source in (("function", signal), ("package", joint)):
                prediction = stage(policy, source)
                verdict = confusion(prediction, known)
                response[policy + "_" + level + "_verdict"] = verdict
                count = counts[order, row["cell"], level, policy]
                count[verdict] += 1
                count["forced"] += prediction == "force"
                count["forced_notice_time"] += prediction == "force" and policy in ("E", "E_absence", "N") and details[after]["quantile"]["notice"]["force"]
                count["unknown_run"] += known == "unknown" and prediction != "skip"
                count["unknown_skip"] += known == "unknown" and prediction == "skip"
        decisions.append(response)
    summaries = []
    for (order, cell, level, policy), counts_for_row in sorted(counts.items()):
        row = {"order": order, "cell": cell, "execution_scope": level, "policy": policy,
               **{name: counts_for_row[name] for name in ("TP", "FP", "FN", "TN", "unknown", "forced", "forced_notice_time")}}
        row["eligible"] = row["TP"] + row["FP"] + row["FN"] + row["TN"]
        row["sensitivity"] = row["TP"] / (row["TP"] + row["FN"]) if row["TP"] + row["FN"] else None
        for prefix, changed in (("unknown_all_changed", True), ("unknown_all_same", False)):
            increments = {
                "TP": counts_for_row["unknown_run"] if changed else 0,
                "FP": counts_for_row["unknown_run"] if not changed else 0,
                "FN": counts_for_row["unknown_skip"] if changed else 0,
                "TN": counts_for_row["unknown_skip"] if not changed else 0,
            }
            row.update({prefix + "_" + key: row[key] + value for key, value in increments.items()})
        summaries.append(row)
    write_csv(ROOT / "decisions.csv", decisions)
    write_csv(EVIDENCE / "cell-scores.csv", summaries)
    return pairs, comparison, summaries


def runtime():
    records = read_runs(ROOT / "runs.jsonl")
    by_cohort = defaultdict(list)
    for record in records:
        by_cohort[record["cohort"]].append(record)
    first = {row["intended_version"]: row for row in by_cohort["A"]}
    indexes = [index_cohort(by_cohort[cohort]) for cohort in ["A", "B"]]
    cases = expected_cases(json_in(ROOT / "replay/inputs.json"))
    observations = {}
    for version in first:
        values = [verified_case(indexes, version, cell) for cell, *_ in cases]
        if all(case is not None for case in values):
            observations[version] = {case["cell"]: case for case in values}
    return first, observations


def investigate(pairs, comparison, signals, details, observations):
    tally = Counter()
    contrast_examples = []
    for version, cells in observations.items():
        for cell in cells.values():
            if cell["mode"] != "direct":
                continue
            companion = cells[cell["cell"].replace("/direct", "/sorted_copy")]
            tally["mode_comparisons"] += 1
            if semantic_outcome(cell) != semantic_outcome(companion):
                tally["mode_value_differences"] += 1
                if version == next(iter(observations)):
                    contrast_examples.append({"version": version, "direct": cell["cell"], "sorted_copy": companion["cell"],
                        "before": [cell["argument_before"], companion["argument_before"]],
                        "outputs": [semantic_outcome(cell), semantic_outcome(companion)]})
            if cell["fn"] == "median":
                for mode in ("direct", "sorted_copy"):
                    median = cells[f"median/{cell['input_id']}/-/{mode}"]
                    quantile = cells[f"quantile/{cell['input_id']}/0.5/{mode}"]
                    tally["median_p05_checked"] += 1
                    tally["median_p05_difference"] += cell_fingerprint(median) != cell_fingerprint(quantile)
    public = [row for row in pairs if row["order"] == "publish"]
    examples = defaultdict(list)
    for pair in public:
        before, after = pair["before"], pair["after"]
        packages = signals["publish", after, "any"]
        a, b = details[before], details[after]
        short = before + "→" + after
        if pair["state"] == "changed" and packages["N"] == "skip":
            examples["observed_change_without_notice"].append(short)
        if pair["state"] == "changed" and packages["F"] == "skip":
            examples["observed_beyond_direct_delegates_candidate"].append(short)
        if pair["state"] == "same" and packages["N"] == "run":
            examples["notice_hit_with_same_scalar_contract"].append(short)
        if pair["state"] == "same":
            for name in b:
                x, y = a[name], b[name]
                if (x["doc"]["raw_section_sha256"] != y["doc"]["raw_section_sha256"] and
                        x["doc"]["text_sha256"] == y["doc"]["text_sha256"]):
                    examples["raw_doc_section_changed_but_normalized_same"].append(short + ": " + name)
                if (x["broad_files"][0]["sha256"] != y["broad_files"][0]["sha256"] and
                        x["broad_files"][1:] == y["broad_files"][1:] and
                        signals["publish", after, name]["F"] == "skip" and x["direct"] == y["direct"]):
                    examples["entry_changed_same_target_file_and_narrow_signal"].append(short + ": " + name)
                if x["direct"] != y["direct"]:
                    examples["direct_dependency_fingerprint_changed"].append(short + ": " + name)
    mutation_only = [r["before"] + "→" + r["after"] + ":" + r["cell"] for r in comparison
                     if r["order"] == "publish" and r["outcome_delta"] == "False" and r["array_state_delta"] == "True"]
    required_searches = ("observed_change_without_notice", "observed_beyond_direct_delegates_candidate",
                         "notice_hit_with_same_scalar_contract", "raw_doc_section_changed_but_normalized_same",
                         "entry_changed_same_target_file_and_narrow_signal", "direct_dependency_fingerprint_changed")
    write_json(EVIDENCE / "counterexamples.json", {
        "published_pairs_searched": len(public),
        "published_input_pair_cells_searched": sum(r["order"] == "publish" for r in comparison),
        **{key: examples[key] for key in required_searches},
        "observed_mutation_only_cells": mutation_only,
        "within_version_contrasts": {key: tally[key] for key in ("mode_comparisons", "mode_value_differences",
                                                                 "median_p05_checked", "median_p05_difference")},
        "mode_contrast_examples_in_first": contrast_examples,
    })


class Replay:
    def __init__(self, policy, mode, sequence, signals, details, profiles, runs, observations):
        self.policy, self.mode, self.sequence = policy, mode, sequence
        self.signals, self.details, self.profiles, self.runs, self.observations = signals, details, profiles, runs, observations
        self.assets, self.hashed, self.evaluated = set(), set(), set()
        self.answered, self.prepared = {}, set()
        self.measurements, self.batch_answers = {}, {}
        self.next_rank, self.latest = 0, None
        self.cost = Counter()

    def charge_profile(self, profile, key, prefix):
        self.cost[prefix + "_cpu_ms"] += profile[key]["cpu_ms"]
        self.cost[prefix + "_wall_ms"] += profile[key]["wall_ms"]

    def asset(self, key, kind, count):
        if key in self.assets:
            self.cost["asset_cache_hits"] += 1
            return False
        self.assets.add(key)
        self.cost[kind + "_opens"] += 1
        self.cost[kind + "_body_bytes"] += count or 0
        return True

    def hash(self, key, bytes_read):
        if key in self.hashed:
            self.cost["hash_cache_hits"] += 1
            return
        self.hashed.add(key)
        self.cost["hash_files"] += 1
        self.cost["hash_read_bytes"] += bytes_read

    def documents(self, version, fingerprint=False):
        for detail in self.details[version].values():
            doc = detail["doc"]
            key = ("doc", doc["url"] or (version, detail["function"]))
            if self.asset(key, "document", doc.get("bytes")):
                self.cost["document_read_wall_ms"] += doc.get("read_wall_ms", 0)
            if fingerprint and key not in self.hashed:
                self.cost["static_cpu_ms"] += doc.get("hash_cpu_ms", 0)
                self.hash(key, doc["bytes"] or 0)

    def distribution(self, version):
        artifact = self.details[version]["quantile"]["tarball"]
        if self.asset(("tar", artifact["url"]), "archive", artifact["bytes"]):
            self.cost["archive_transfer_wall_ms"] += artifact["wall_ms"]
            self.charge_profile(self.profiles[version], "archive_local_verify_and_unpack", "archive_verify")

    def fingerprint(self, version):
        policy = self.policy
        if policy in ("C", "D"):
            self.documents(version, fingerprint=True)
        if policy == "C":
            return
        self.distribution(version)
        rows = list(self.details[version].values())
        profile = self.profiles[version]
        field = "broad_files" if policy == "D" else "narrow_files" if policy in ("E", "F", "E_absence") else None
        if field:
            file_set = {item["path"]: item["bytes"] for row in rows for item in row[field]}
            for path, length in file_set.items():
                self.hash((version, path), length)
            self.charge_profile(profile, "D_raw_hash" if policy == "D" else "F_ast", "static")
            self.cost["function_ast_runs"] += field == "narrow_files"
        if policy in ("N", "E", "E_absence"):
            self.cost["notice_inventory_checks"] += 1
            notice = rows[0]["notice"]
            bundled = notice["bundled"]
            self.cost["notice_bundled_absent"] += bundled["status"] == "not_packaged"
            if bundled["path"]:
                self.cost["notice_bundled_opens"] += 1
                self.cost["notice_bundled_body_bytes"] += bundled["bytes"]
                self.cost["notice_section_bytes"] += bundled.get("section_bytes", 0)
                self.hash((version, bundled["path"]), bundled["bytes"])
            self.cost["notice_unknown_body"] += notice["force"]
            if notice["github"]:
                github = notice["github"]
                self.asset(("github notice", github["url"]), "notice_github", github["bytes"])
            self.charge_profile(profile, "N_changelog", "static")

    def edge(self, rank):
        version = self.sequence[rank]
        signal = self.signals["publish", version, "any"]
        answer = stage(self.policy, signal)
        if rank in self.evaluated:
            self.cost["decision_cache_hits"] += 1
            return answer
        self.evaluated.add(rank)
        self.cost["evaluated_edges"] += rank > 0
        self.cost["forced_edges_read"] += answer == "force"
        notice = self.details[version]["quantile"]["notice"]
        self.cost["notice_time_forced_edges_read"] += answer == "force" and notice["force"] and self.policy in ("E", "E_absence", "N")
        self.cost["absence_sensitivity_forced_edges_read"] += answer == "force" and notice["current_only_absence"] and self.policy == "E_absence"
        if self.policy != "A":
            for inspected in self.sequence[max(0, rank - 1):rank + 1]:
                if inspected not in self.prepared:
                    self.fingerprint(inspected)
                    self.prepared.add(inspected)
        return answer

    def execute(self, version, forced=False):
        if version in self.measurements:
            return self.measurements[version]
        self.distribution(version)
        observed = self.runs[version]
        for kind, field in (("install", "install"), ("node", "node_process")):
            if field in observed:
                rec = observed[field]
                self.cost[kind + "_cpu_ms"] += rec["cpu_user_ms"] + rec["cpu_sys_ms"]
                self.cost[kind + "_wall_ms"] += rec["wall_ms"]
                self.cost["executions" if kind == "node" else "installations"] += 1
        self.cost["forced_executions"] += forced
        measured = version if version in self.observations else None
        self.measurements[version] = measured
        return measured

    def batch_until(self, limit):
        for rank in range(self.next_rank, limit + 1):
            version = self.sequence[rank]
            action = self.edge(rank)
            if action != "skip":
                self.latest = self.execute(version, forced=action == "force")
            self.batch_answers[version] = self.latest
        self.next_rank = limit + 1

    def on_request(self, target):
        rank = self.sequence.index(target)
        if self.policy == "A":
            self.edge(rank)
            return self.execute(target)
        prior = [self.sequence.index(version) for version, value in self.measurements.items() if value and self.sequence.index(version) < rank]
        if not prior:
            return self.execute(target)
        start = max(prior)
        actions = [self.edge(n) for n in range(start + 1, rank + 1)]
        if any(action != "skip" for action in actions):
            return self.execute(target, forced="force" in actions)
        return self.sequence[start]

    def query(self, target, ceiling):
        self.cost.clear()
        if self.mode == "batch":
            self.batch_until(ceiling)
        self.documents(target)
        if target in self.answered:
            self.cost["answer_cache_hits"] += 1
        else:
            value = self.batch_answers[target] if self.mode == "batch" else self.on_request(target)
            self.answered[target] = value
        measured = self.answered[target]
        differences = None
        if measured in self.observations and target in self.observations:
            differences = sum(cell_fingerprint(case) != cell_fingerprint(self.observations[measured][key])
                              for key, case in self.observations[target].items())
        disposition = "held" if differences is None else "wrong_carry" if differences else "correct"
        self.cost[disposition] += 1
        self.cost["carries"] += measured is not None and measured != target
        run = self.runs.get(measured, {})
        return {
            "requested_release": target, "returned_release": target if disposition != "held" else None,
            "last_measured_release": measured, "last_measured_utc": run.get("finished_utc"),
            "measured_run_id": run.get("run_id"), "lock_sha256": run.get("lock_sha256"), "disposition": disposition,
            "cells_different": differences, "target_publish_utc": self.details[target]["quantile"]["npm_utc"],
            "target_quantile_section": self.details[target]["quantile"]["doc"]["url"],
            "target_median_section": self.details[target]["median"]["doc"]["url"],
            **{key: round(self.cost[key], 4) for key in METRICS},
        }


def costs(signals, details, runs, observations):
    roster = json_in(EVIDENCE / "roster.json")
    sequence = roster["published_order"]
    support = json_in(EVIDENCE / "replay.json")["supported_versions"]
    profiles = json_in(EVIDENCE / "static-profiles.json")["versions"]
    last_rank = len(sequence) - 1
    chosen = {
        "pinned": [(sequence[0], last_rank)],
        "each_publish": [(version, rank) for rank, version in enumerate(sequence)],
        "dual": [(version, last_rank) for version in [support[0], support[-1]] * 3],
    }
    if roster["semver_order"] != sequence:
        chosen["highest_semver"] = [
            (max(sequence[:rank + 1], key=roster["semver_order"].index), rank) for rank in range(len(sequence))
        ]
    records, summaries = [], []
    for name, queries in chosen.items():
        for policy in POLICIES:
            for mode in ("batch", "on_request"):
                model = Replay(policy, mode, sequence, signals, details, profiles, runs, observations)
                unit = {"scenario": name, "policy": policy, "mode": mode}
                scenario_rows = [unit | {"query": index, "published_ceiling": sequence[ceiling]} | model.query(version, ceiling)
                                 for index, (version, ceiling) in enumerate(queries, 1)]
                records.extend(scenario_rows)
                first, repeat = scenario_rows[0], scenario_rows[1:]
                summaries.append(unit | {
                    "queries": len(scenario_rows), "first_target": first["requested_release"], "first_measured": first["last_measured_release"],
                    "last_target": scenario_rows[-1]["requested_release"], "last_measured": scenario_rows[-1]["last_measured_release"],
                    "correct": sum(r["correct"] for r in scenario_rows),
                    "wrong_carry": sum(r["wrong_carry"] for r in scenario_rows), "held": sum(r["held"] for r in scenario_rows),
                    **{"first_" + key: first[key] for key in METRICS},
                    **{"repeat_" + key: round(sum(row[key] for row in repeat), 4) for key in METRICS},
                })
    write_csv(ROOT / "costs.csv", records)
    write_csv(EVIDENCE / "cost-summary.csv", summaries)


def main():
    signals = lookup_signals()
    details = load_details()
    pairs, comparison, scores = join_outputs(signals, details)
    runs, observations = runtime()
    investigate(pairs, comparison, signals, details, observations)
    costs(signals, details, runs, observations)
    print(f"{len(pairs)} adjacent pairs counted in two orders; {len(comparison)} cell comparisons; {len(scores)} score rows")


if __name__ == "__main__":
    main()
