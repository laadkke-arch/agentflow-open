"""Post-seal grading and paired arithmetic using AF-RES-036's fixed excerpts."""
import argparse
import csv
import io
import json
import re
import subprocess
import tarfile
from collections import Counter
from functools import lru_cache
from pathlib import Path
from urllib.parse import urldefrag, urlsplit

from batch import read_manifest
from measure import file_path, load_lines, measure, write_csv
from prepare import ROOT, git_file, rows, sha

LEVELS = {"none": 0, "partial": 1, "equivalent": 2, "exact": 3}
METRICS = ("logical_gets", "http_exchanges", "total_body_bytes", "successful_body_bytes",
           "displayed_local_H_bytes", "validated_local_H_bytes", "serialized_input_bytes",
           "request_seconds_sum", "worker_wall_seconds", "tool_wall_seconds")
BUDGETS = ("logical", "strict")


def url_key(url):
    parts = urlsplit(urldefrag(url)[0])
    return (parts.hostname or "").removeprefix("www."), parts.path.rstrip("/"), parts.query


def normalize(text):
    return " ".join(text.split())


@lru_cache
def parser_class(path, name):
    namespace = {"__name__": "_pinned_af036_normalizer"}
    code = git_file(path)
    exec(compile(code, path, "exec"), namespace)
    return namespace[name]


def parse_span(path, span):
    data = path.read_bytes()
    if span.get("member"):
        try:
            with tarfile.open(fileobj=io.BytesIO(data)) as archive:
                member = archive.getmember(span["member"])
                if not member.isfile():
                    return None, "ARCHIVE_MEMBER_TYPE"
                with archive.extractfile(member) as file:
                    data = file.read()
        except KeyError:
            return None, "ARCHIVE_MEMBER_MISSING"
        except (tarfile.TarError, OSError):
            return None, "ARCHIVE_PARSE_ERROR"
    if span.get("page"):
        page = str(span["page"])
        command = subprocess.run(["pdftotext", "-layout", "-f", page, "-l", page, str(path), "-"],
                                 capture_output=True, check=False)
        if command.returncode:
            return None, "PDF_TEXT_EXTRACTION_FAILED"
        return command.stdout.decode("utf8", errors="replace"), None
    if span.get("normalization", "").startswith("HTMLParser"):
        parser = parser_class("collectors/gnu/parse_html.py", "Document")()
        parser.feed(data.decode("utf8", errors="replace"))
        return parser.text, None
    if span.get("text_format") == "cleaned HTML" or span.get("location") == "cleaned HTML text":
        parser = parser_class("collectors/bioc/html_extract.py", "TextParser")()
        parser.feed(data.decode("utf8", errors="replace"))
        return parser.result()[0], None
    return data.decode("utf8", errors="replace"), None


def cutoff(event, budget):
    found = []
    physical = 0
    for request in event["requests"]:
        for exchange in request["exchanges"]:
            physical += exchange["http_exchange"]
            if budget == "strict" and physical > 2:
                return found
            found.append((request, exchange))
    return found


def prefix_metrics(event, budget):
    view = cutoff(event, budget)
    return {
        "logical_gets": len({request["logical"] for request, _ in view}),
        "http_exchanges": sum(exchange["http_exchange"] for _, exchange in view),
        "body_bytes": sum(exchange["received_body_bytes"] for _, exchange in view),
        "successful_body_bytes": sum(exchange["received_body_bytes"] for _, exchange in view
                                     if exchange["status"] == 200 and not exchange["error"]),
    }


def reference_tables():
    pinned = read_manifest()[0]["grader_only"]["file_sha256"]
    for name, digest in pinned.items():
        assert sha(git_file(name)) == digest
    components = {row["ref_id"]: (row, sha(raw)) for row, raw in rows(git_file("components.jsonl"))}
    original = csv.DictReader(io.StringIO(git_file("adjudication.csv").decode()))
    old_actions = {a["ref_id"]: a for a in original}
    locators = {}
    for record, _ in rows(git_file("attempts.jsonl")):
        if record.get("stored_path") and record.get("final_url"):
            locators.setdefault(record["stored_path"], set()).update(
                x for x in (record["final_url"], record.get("url")) if x
            )
    return components, old_actions, locators


def span_resource(span, locators):
    valid = {span["url"]} if span.get("url") else locators.get(span.get("path"), set())
    return {url_key(url) for url in valid}


def match_span(span, locators, view, capture, event, allowable_status):
    expected = span["text"]
    digest = sha(expected.encode())
    assert digest == span.get("text_sha256", span.get("sha256"))
    details = {
        "source_id": span["source_id"], "expected_span_sha256": digest,
        "target_urls": sorted({span["url"]} if span.get("url") else locators.get(span.get("path"), set())),
        "locator": span.get("location") or span.get("path"),
        "member": span.get("member"), "page": span.get("page"),
        "level": "none", "independent_body": False, "comparisons": [],
    }
    allowed_urls = span_resource(span, locators)
    for request, shot in view:
        if shot["status"] != allowable_status or not shot.get("body_file"):
            continue
        if url_key(shot["requested_url"]) not in allowed_urls and url_key(request["initial_url"]) not in allowed_urls:
            continue
        path = file_path(capture, event, shot)
        assert sha(path.read_bytes()) == shot["body_sha256"]
        text, error = parse_span(path, span)
        result = {
            "url": shot["requested_url"], "logical_get": request["logical"],
            "body_sha256": shot["body_sha256"], "body_sha256_matches_036": (
                shot["body_sha256"] == span["source_sha256"] if span.get("source_sha256") else None),
            "error": error,
        }
        if text is None:
            found = "none"
        elif expected in text:
            found = "exact"
            result["span_offset_in_normalized_body"] = text.index(expected)
            result["matched_span_sha256"] = digest
        elif normalize(expected) in normalize(text):
            found = "equivalent"
            result["matched_normalized_sha256"] = sha(normalize(expected).encode())
        else:
            found = "none"
            result["error"] = "EXPECTED_SPAN_CHANGED_OR_MISSING"
        result["level"] = found
        details["comparisons"].append(result)
        details["independent_body"] = True
        if LEVELS[found] > LEVELS[details["level"]]:
            details["level"] = found
    return details


def span_level(matches):
    levels = [LEVELS[match["level"]] for match in matches]
    if levels and min(levels) >= 2:
        return "exact" if min(levels) == 3 else "equivalent"
    return "partial" if any(levels) else "none"


def grades(event, budget, capture, component, locators, criterion):
    view = cutoff(event, budget)
    is_current = event["task"] == "current"
    restoration = {}
    for kind in ("N", "H"):
        status = 404 if kind == "N" and event["ref_id"] == "R01" else 200
        restoration[kind] = [
            match_span(span, locators, view, capture, event, status)
            for span in component[kind]["spans"]
        ]
    n = span_level(restoration["N"])
    h_independent = span_level(restoration["H"])
    display = event["local_history"]["displayed"]
    if display:
        card = (capture / event["run_id"] / "local-H.txt").read_bytes()
        _, delimiter, text = card.partition(b"\n\nPublisher excerpt(s):\n")
        assert delimiter and sha(card) == component["H"]["sha256"]
        assert sha(text) == component["H"]["raw_sha256"]
        assert all(span["text"].encode() in text for span in component["H"]["spans"])
    h = "exact" if display else h_independent
    action = event["provisional_action"]
    if budget == "strict" and is_current and event["http_exchanges"] > 2:
        full_urls = {exchange["requested_url"] for _, exchange in view if exchange["status"] == 200}
        qualifying = [req for req in event["requests"] if req["section"]["qualified"]]
        if not qualifying or qualifying[0]["final_url"] not in full_urls:
            action = "HOLD"
    if is_current:
        verified = bool(criterion["same_window_action"] and criterion["required_section_observed_in_main"]
                        and action == criterion["same_window_action"]
                        and any(ex["status"] == 200 and req["section"]["qualified"] for req, ex in view))
        state = "success" if verified else (
            "partial" if any(req["accepted_body"] for req, _ in view) else "hold")
        success = equivalent_success = verified
    else:
        success = n == h == "exact"
        equivalent_success = n in {"exact", "equivalent"} and h in {"exact", "equivalent"}
        state = ("success" if success else "content_equivalent" if equivalent_success
                 else "partial" if n != "none" or h != "none" else "failure")
    return {
        "state": state, "success": success, "equivalent_success": equivalent_success,
        "N": n, "H": h, "H_independent": h_independent, "H_local_displayed": display,
        "shown_action": action,
        "independently_opened_H_span_count": sum(span["independent_body"] for span in restoration["H"]),
        "exact_H_source_span_count": sum(span["level"] == "exact" for span in restoration["H"]),
        "holds_with_comparator": state == "hold" and bool(criterion["same_window_action"]),
        "budget_cost": prefix_metrics(event, budget),
        "match_receipts": restoration,
    }


def pair_state(left, right):
    if left and right:
        return "both_success"
    if left:
        return "C1_only"
    if right:
        return "C2_only"
    return "both_fail"


def simulated():
    data = git_file("replay-costs.csv")
    original = csv.DictReader(io.StringIO(data.decode()))
    task_names = {"current_decision_N": "current", "reconstruct_evidence_body_NH": "restore"}
    return {
        (row["ref_ids"], task_names[row["task"]], row["configuration"]): row
        for row in original if row["ref_ids"] in {r["ref_id"] for r in read_manifest()}
        and row["task"] in task_names and row["configuration"] in {"C1", "C2"}
    }, sha(data)


def add_comparison(left, right, sim, baseline, origin):
    task, ref = left["task"], left["ref_id"]
    c1, c2 = sim[(ref, task, "C1")], sim[(ref, task, "C2")]
    challenges = {"real_budgeted_attempts_vs_known_complete_routes"}
    if left["requests_with_errors"] or right["requests_with_errors"]:
        challenges.add("proxy_or_HTTP_refusal")
    if any("publisher_index" == req["purpose"] or "history_discovery" == req["purpose"]
           for ev in origin for req in ev["requests"]):
        challenges.add("locator_discovery_or_index_budget")
    if ref == "G02":
        challenges.add("HTML_response_bytes_changed_exact_N_excerpt_survived")
        if task == "restore":
            challenges |= {"README_redirect_uses_2_exchanges", "two_H_spans_distinct_sources"}
    if ref == "R01":
        challenges.add("historical_tarball_and_replacement_HTML_are_different")
    if ref == "G03":
        challenges.add("2018_target_edition_B_already_contains")
    if task == "current":
        challenges.add("simulation_constructs_N_live_scores_current_action")
    comparison = {
        "ref_id": ref, "task": task, "C1_run": left["run_id"], "C2_run": right["run_id"],
        "036_criterion": baseline["criterion_action"],
        "same_window_action": left["same_window_action"], "criterion_source_ids": left["criterion_source_ids"],
        "observable_action_change": task == "current" and left["provisional_action"] != right["provisional_action"],
    }
    for budget in BUDGETS:
        comparison[f"{budget}_pair_state"] = pair_state(left[f"{budget}_success"], right[f"{budget}_success"])
        comparison[f"{budget}_equivalent_pair_state"] = pair_state(
            left[f"{budget}_equivalent_success"], right[f"{budget}_equivalent_success"])
        for config, row in (("C1", left), ("C2", right)):
            for metric in ("state", "N", "H", "H_independent", "http_exchanges", "body_bytes"):
                comparison[f"{config}_{budget}_{metric}"] = row[f"{budget}_{metric}"]
    for metric in METRICS:
        for config, row in (("C1", left), ("C2", right)):
            comparison[f"{config}_{metric}"] = row[metric]
        comparison[f"C2_minus_C1_{metric}"] = round(right[metric] - left[metric], 6)
    for key in ("modeled_request_operations", "modeled_http_exchanges", "modeled_body_bytes",
                "operation_count_within_budget", "strict_exchange_count_within_budget", "local_H_read_bytes"):
        comparison[f"C1_sim_{key}"] = c1[key]
        comparison[f"C2_sim_{key}"] = c2[key]
    comparison["sim_cost_ids"] = c1["cost_id"] + ";" + c2["cost_id"]
    comparison["cost_comparability"] = (
        "NH excerpt objective; equal-output timing/bytes requires both successes"
        if task == "restore" else "counting units only; current decision and complete N reconstruction differ")
    comparison["broken_or_unverified_assumptions"] = ";".join(sorted(challenges))
    return comparison


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("capture_dir", type=Path)
    capture = args.parse_args().capture_dir
    components, original, locators = reference_tables()
    frozen = {row["run_id"]: row for row in read_manifest()}
    criteria = {row["ref_id"]: row for row in load_lines(ROOT / "evidence/current-criteria.jsonl")}
    events = load_lines(ROOT / "attempts.jsonl", "main")
    assert len(events) == len(frozen) == 48
    simulation, simulation_hash = simulated()
    assert len(simulation) == 48
    runs = []
    span_matches = []
    for event in events:
        rid = event["ref_id"]
        execution = measure(event)
        component, component_digest = components[rid]
        assert component_digest == frozen[event["run_id"]]["grader_only"]["component_row_sha256"]
        criterion = criteria[rid]
        execution.update(
            same_window_action=criterion["same_window_action"], criterion_scope=criterion["verification"],
            criterion_source_ids=";".join(criterion["source_ids"]), original_criterion=original[rid]["criterion_action"],
        )
        reported = {"run_id": execution["run_id"], "ref_id": rid, "task": event["task"], "budgets": {}}
        for budget in BUDGETS:
            checked = grades(event, budget, capture, component, locators, criterion)
            for key in ("state", "success", "equivalent_success", "N", "H", "H_independent",
                        "independently_opened_H_span_count", "exact_H_source_span_count"):
                execution[f"{budget}_{key}"] = checked[key]
            for key, value in checked["budget_cost"].items():
                execution[f"{budget}_{key}"] = value
            reported["budgets"][budget] = checked
        span_matches.append(reported)
        runs.append(execution)
    comparisons = []
    for i in range(0, len(runs), 2):
        pair = {row["configuration"]: row for row in runs[i:i + 2]}
        comparisons.append(add_comparison(pair["C1"], pair["C2"], simulation,
                                          original[pair["C1"]["ref_id"]], events[i:i + 2]))
    write_csv(ROOT / "runs.csv", runs)
    write_csv(ROOT / "pairs.csv", comparisons)
    (ROOT / "evidence/span-matches.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in span_matches), encoding="utf-8")
    summary = {"simulation_sha256": simulation_hash, "groups": {}}
    for task in ("current", "restore"):
        summary["groups"][task] = {}
        for budget in BUDGETS:
            paired = [row for row in comparisons if row["task"] == task]
            stats = dict(Counter(row[f"{budget}_pair_state"] for row in paired))
            separate = {}
            for config in ("C1", "C2"):
                selected = [r for r in runs if r["task"] == task and r["configuration"] == config]
                separate[config] = {
                    "states": dict(Counter(row[f"{budget}_state"] for row in selected)),
                    "N": dict(Counter(row[f"{budget}_N"] for row in selected)),
                    "H": dict(Counter(row[f"{budget}_H"] for row in selected)),
                    "independent_H": dict(Counter(row[f"{budget}_H_independent"] for row in selected)),
                    "body_bytes": sum(row[f"{budget}_body_bytes"] for row in selected),
                    "logical_gets": sum(row[f"{budget}_logical_gets"] for row in selected),
                    "http_exchanges": sum(row[f"{budget}_http_exchanges"] for row in selected),
                    "successful_body_bytes": sum(row[f"{budget}_successful_body_bytes"] for row in selected),
                    # Time fields here are observed run-wide durations for either view.
                    **{m: round(sum(row[m] for row in selected), 6) for m in METRICS[4:]},
                }
            summary["groups"][task][budget] = {"pairs": stats, **separate}
    (ROOT / "evidence/paired-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
