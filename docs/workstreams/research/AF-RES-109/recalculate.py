#!/usr/bin/env python3
"""Independently verify and recalculate AF-RES-109's saved evidence.

Only the Python standard library is used.  No search, application experiment or
git mutation occurs.  --write writes exactly three owned report files; --check
recomputes their contents without writing.  Exit 0 means ledger-integrity pass,
NOT research COMPLETE.  Missing original editions, immutable model identity and
automatic-read measurements remain explicit PARTIAL gaps, never numeric zero.

The search seal authenticates raw search outputs, not the later blind packets.
Choice/test counts are sets of flagged keys within request and arm, with request
unions reported separately.  Prefixes are acquisition eligibility, not shorter
budget reruns or evidence that a proposal had already been formulated.
"""

import argparse
import csv
import hashlib
import html
import io
import json
import math
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PREFIX = "docs/workstreams/research/AF-RES-109/"
SEARCH_SEAL = "628e33709b0be7a19486f1bfeaef93f42e129394"
RECRUITMENT_SEAL = "629971"
REQUEST_IDS = tuple("R%d" % n for n in range(1, 7))
ARM_IDS = tuple(r + "-" + a for r in REQUEST_IDS for a in ("A", "B"))
RAW_NAMES = ("events.jsonl", "returns.json", "sources.jsonl", "notes.md")
OPEN_TYPES = {"open", "click", "find", "reopen"}
OUTPUTS = (
    "evidence/recalculated-metrics.json",
    "evidence/required-tables.md",
    "RESULT.md",
)
SOURCE_FIELDS = {
    "source_id", "original_url", "actual_url", "author_lineage", "edition",
    "published_utc", "direct_read_utc", "exact_section", "confirmed", "limits",
    "counter_observation", "unknown", "questions", "experiment_rows",
    "original_work_id", "counts_as_unique_primary", "count_category", "reader",
    "source_kind",
}
EXPECTED_PRIMARY_CATEGORIES = {
    "request": 6, "search_returned": 17, "counter": 6, "external": 4,
}


class LedgerError(Exception):
    """A reported integrity failure, distinct from a research evidence gap."""


class Checks:
    def __init__(self):
        self.errors = []

    def require(self, condition, message):
        if not condition:
            self.errors.append(message)

    def finish(self):
        if self.errors:
            raise LedgerError("; ".join(self.errors))


def owned(relative):
    p = Path(relative)
    if p.is_absolute() or ".." in p.parts:
        raise LedgerError("Non-owned path refused: %s" % relative)
    path = (ROOT / p).resolve()
    if not path.is_relative_to(ROOT):
        raise LedgerError("Path escapes workstream: %s" % relative)
    return path


def read_text(relative):
    try:
        return owned(relative).read_text(encoding="utf-8")
    except OSError as exc:
        raise LedgerError("Cannot read %s: %s" % (relative, exc)) from exc


def json_file(relative):
    return json.loads(read_text(relative))


def json_lines_text(text, label):
    rows = []
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise LedgerError("Invalid JSON at %s:%d: %s" % (label, number, exc)) from exc
        if not isinstance(row, dict):
            raise LedgerError("Expected object at %s:%d" % (label, number))
        rows.append(row)
    return rows


def json_lines(relative):
    return json_lines_text(read_text(relative), relative)


def csv_text(text, label):
    reader = csv.DictReader(io.StringIO(text, newline=""))
    fields = reader.fieldnames or []
    if not fields or len(fields) != len(set(fields)):
        raise LedgerError("Missing/duplicate CSV headers: %s" % label)
    rows = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise LedgerError("Malformed CSV row width: %s" % label)
    return fields, rows


def csv_file(relative):
    return csv_text(read_text(relative), relative)


def keyed(rows, key, label):
    result = {}
    for row in rows:
        value = row.get(key)
        if value in (None, "") or value in result:
            raise LedgerError("Missing/duplicate %s in %s: %r" % (key, label, value))
        result[value] = row
    return result


def flag(value, label="flag"):
    if value is True or value == 1:
        return True
    if value is False or value == 0:
        return False
    if isinstance(value, str) and value.strip().lower() in ("true", "1"):
        return True
    if isinstance(value, str) and value.strip().lower() in ("false", "0"):
        return False
    raise LedgerError("Invalid boolean %s: %r" % (label, value))


def integer(value, label):
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise LedgerError("Invalid integer %s: %r" % (label, value)) from exc
    if isinstance(value, float) and result != value:
        raise LedgerError("Non-integral %s: %r" % (label, value))
    return result


def utc(value, label):
    if not isinstance(value, str) or not value.strip():
        raise LedgerError("Missing UTC timestamp %s" % label)
    normalized = value.strip().replace(" UTC", "+00:00")
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        result = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise LedgerError("Invalid UTC timestamp %s: %r" % (label, value)) from exc
    if result.tzinfo is None or result.utcoffset().total_seconds() != 0:
        raise LedgerError("Explicit UTC required for %s: %r" % (label, value))
    return result.astimezone(timezone.utc)


def known(value):
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip().lower() not in {
            "", "none", "null", "unknown", "unavailable", "not exposed", "미확인", "未確認",
        }
    return True


def digest(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def git_show(revision, relative):
    owned(relative)  # Refuse unowned paths even though git reads an object.
    command = ["git", "show", "%s:%s%s" % (revision, PREFIX, relative)]
    try:
        proc = subprocess.run(command, cwd=REPO, capture_output=True, timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise LedgerError("Cannot read sealed %s at %s: %s" % (relative, revision, exc)) from exc
    if proc.returncode:
        raise LedgerError("git show failed for owned %s at %s: %s" % (
            relative, revision, proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout


def verify_frozen(requests, baseline_fields, baseline, candidate_fields, candidates):
    checks = Checks()
    expected = {"evidence/search/%s/%s" % (arm, name) for arm in ARM_IDS for name in RAW_NAMES}
    actual = {str(p.relative_to(ROOT)) for p in owned("evidence/search").rglob("*") if p.is_file()}
    checks.require(actual == expected, "Raw search inventory must be exactly 48 expected files")
    manifest = []
    for relative in sorted(expected):
        current = owned(relative).read_bytes()
        sealed = git_show(SEARCH_SEAL, relative)
        checks.require(current == sealed, "Changed raw search evidence: " + relative)
        manifest.append({"path": relative, "sha256": digest(sealed), "bytes": len(sealed)})

    frozen_baseline_fields, frozen_baseline = csv_text(
        git_show(RECRUITMENT_SEAL, "baseline.csv").decode("utf-8"), "recruitment:baseline.csv")
    first_eight = frozen_baseline_fields[:8]
    checks.require(len(first_eight) == 8 and baseline_fields[:8] == first_eight,
                   "Baseline original first eight columns changed")
    current_b = [{k: row.get(k) for k in first_eight} for row in baseline]
    frozen_b = [{k: row.get(k) for k in first_eight} for row in frozen_baseline]
    checks.require(current_b == frozen_b, "Baseline original eight-column values/order changed")

    frozen_requests = json_lines_text(
        git_show(RECRUITMENT_SEAL, "requests.jsonl").decode("utf-8"), "recruitment:requests.jsonl")
    checks.require([r.get("id") for r in requests] == [r.get("id") for r in frozen_requests],
                   "Recruitment request identity/order changed")
    for original, current in zip(frozen_requests, requests):
        for key, value in original.items():
            checks.require(key in current and current[key] == value,
                           "Recruitment request original field changed: %s.%s" % (original.get("id"), key))

    frozen_cf, frozen_c = csv_text(
        git_show(SEARCH_SEAL, "candidates.csv").decode("utf-8"), "search-seal:candidates.csv")
    frozen_eight = frozen_cf[:8]
    checks.require(candidate_fields[:8] == frozen_eight, "Candidate original eight columns changed")
    checks.require([{k: r.get(k) for k in frozen_eight} for r in candidates] ==
                   [{k: r.get(k) for k in frozen_eight} for r in frozen_c],
                   "Candidate original ranks, identities, URLs or vacancy slots changed")
    checks.finish()
    return {
        "search_output_seal": SEARCH_SEAL,
        "recruitment_seal": RECRUITMENT_SEAL,
        "raw_search_files_verified": len(manifest),
        "raw_search_manifest_sha256": digest(json.dumps(manifest, sort_keys=True, separators=(",", ":"))),
        "raw_search_manifest": manifest,
        "baseline_original_columns_verified": first_eight,
        "request_original_fields_verified": {r["id"]: sorted(r) for r in frozen_requests},
        "candidate_original_columns_verified": frozen_eight,
        "packet_at_search_seal_claimed": False,
    }


def explicit(event):
    return event.get("event_type") in OPEN_TYPES


def actions(events):
    return [e for e in events if e.get("event_type") == "query" or explicit(e)]


def prefix(events, caps, chronological=False):
    ordered = sorted(actions(events), key=(
        (lambda e: (utc(e["started_utc"], "action start"), e["event_index"]))
        if chronological else (lambda e: e["event_index"])))
    included = []
    queries = opens = 0
    first_excluded = None
    for event in ordered:
        q = queries + int(event["event_type"] == "query")
        o = opens + int(explicit(event))
        if q > caps["queries"] or o > caps["explicit_opens"]:
            first_excluded = event["event_index"]
            break  # Do not skip an expensive action to admit later reads.
        queries, opens = q, o
        included.append(event["event_index"])
    return {"included_action_indices": included, "consumed_queries": queries,
            "consumed_explicit_opens": opens, "first_excluded_event_index": first_excluded}


def required_reads(acquisition, raw_sources):
    """Derive substantive/supporting read indices from the raw return record."""
    if isinstance(acquisition, int) and not isinstance(acquisition, bool):
        return {acquisition}
    if not isinstance(acquisition, dict):
        raise LedgerError("Unrecognized acquisition record: %r" % acquisition)
    result = set()
    for group in (
        ("direct_read_event", "direct_section_event", "direct_section_read"),
        ("open_event_indices",),
        ("open_event", "open_event_index", "direct_open"),
    ):
        found = [acquisition[key] for key in group if key in acquisition]
        if found:
            for value in found:
                result.update(value if isinstance(value, list) else [value])
            break
    for key, value in acquisition.items():
        if key.startswith("supporting_") and key != "supporting_source_ids":
            if isinstance(value, int) and not isinstance(value, bool):
                result.add(value)
            elif isinstance(value, list) and all(isinstance(x, int) for x in value):
                result.update(value)
    for sid in acquisition.get("supporting_source_ids", []):
        if sid not in raw_sources:
            raise LedgerError("Missing supporting raw source: " + sid)
        result.update(required_reads(raw_sources[sid].get("acquisition_event"), raw_sources))
    if not result or any(not isinstance(x, int) or isinstance(x, bool) for x in result):
        raise LedgerError("No unambiguous substantive read index: %r" % acquisition)
    return result


def model_identity(start):
    model = start.get("model", {})
    if not isinstance(model, dict):
        return None
    for key in ("exact_immutable_backend_version", "exact_backend_version", "immutable_backend_id"):
        if known(model.get(key)):
            return model[key]
    return None  # Displayed labels are not immutable backend identities.


def raw_execution(audit, request_map):
    checks = Checks()
    audit_arms = keyed(audit.get("arms", []), "arm_id", "audit arms")
    audit_pairs = keyed(audit.get("pairs", []), "request_id", "audit pairs")
    checks.require(set(audit_arms) == set(ARM_IDS), "Audit must cover all 12 arms")
    checks.require(set(audit_pairs) == set(REQUEST_IDS), "Audit must cover all 6 pairs")
    checks.finish()
    arms, raw = {}, {}
    for aid in ARM_IDS:
        rid, method = aid.split("-")
        events = json_lines("evidence/search/%s/events.jsonl" % aid)
        returned = json_file("evidence/search/%s/returns.json" % aid)
        source_rows = json_lines("evidence/search/%s/sources.jsonl" % aid)
        source_map = keyed(source_rows, "source_id", aid + " raw sources")
        checks.require([e.get("event_index") for e in events] == list(range(len(events))),
                       aid + " event indices are not contiguous from zero")
        starts = [e for e in events if e.get("event_type") == "start"]
        stops = [e for e in events if e.get("event_type") == "stop"]
        checks.require(len(starts) == len(stops) == 1, aid + " needs one start and stop")
        checks.finish()
        queries = [e for e in events if e.get("event_type") == "query"]
        opens = [e for e in events if explicit(e)]
        finals = returned.get("final_candidates", [])
        vacant = returned.get("vacancies", [])
        ranks = [integer(c.get("rank"), aid + " returned rank") for c in finals]
        vacancy_ranks = [integer(c.get("rank"), aid + " vacant rank") for c in vacant]
        checks.require(sorted(ranks + vacancy_ranks) == [1, 2, 3], aid + " ranks/vacancies must fill slots 1-3")
        observed = {
            "queries": len(queries), "explicit_opens": len(opens),
            "final_links": len(finals), "final_vacancies": len(vacant),
            "source_rows": len(source_rows),
            "logged_result_rows": sum(len(e.get("results", [])) for e in queries),
            "events": len(events),
        }
        checks.require(len(opens) == len(source_rows), aid + " source/read action count mismatch")
        checks.require(observed == audit_arms[aid].get("observed"), aid + " raw counts differ from audit")
        for key in ("queries", "explicit_opens"):
            expected_key = "actual_" + key
            checks.require(integer(returned.get(expected_key), aid + "." + expected_key) == observed[key],
                           aid + " returns count mismatch: " + key)
            checks.require(integer(stops[0].get(expected_key), aid + " stop " + key) == observed[key],
                           aid + " stop count mismatch: " + key)
        checks.require(len(queries) <= 3 and len(opens) <= 6, aid + " exceeded the recorded search caps")
        for event in events:
            checks.require(event.get("request_id") == rid and event.get("arm") == method,
                           aid + " event identity mismatch")
            begin = utc(event.get("started_utc"), aid + " event start")
            end = utc(event.get("ended_utc"), aid + " event end")
            checks.require(begin <= end, aid + " negative event interval")
        begin = utc(returned.get("start_utc"), aid + " run start")
        end = utc(returned.get("end_utc"), aid + " run end")
        wall = round((end - begin).total_seconds(), 6)
        checks.require(wall >= 0 and math.isclose(wall, float(audit_arms[aid]["wall_seconds"]), abs_tol=.002),
                       aid + " run wall time disagrees with audit")
        checks.require(returned.get("start_utc") == audit_arms[aid].get("start_utc") and
                       returned.get("end_utc") == audit_arms[aid].get("end_utc"), aid + " run bounds differ")
        expected_input = request_map[rid].get("experiment_input_sha256")
        checks.require(bool(expected_input) and starts[0].get("input_sha256") == expected_input and
                       returned.get("input_sha256") == expected_input, aid + " experiment input digest mismatch")
        identity = model_identity(starts[0])
        action_list = actions(events)
        unknown_auto = sum(not known(e.get("automatic_reads")) for e in action_list)
        auto_total = None if unknown_auto else sum(integer(e["automatic_reads"], aid + " automatic reads")
                                                  for e in action_list)
        arms[aid] = {
            "request_id": rid, "arm": method, **observed,
            "start_utc": returned["start_utc"], "end_utc": returned["end_utc"],
            "wall_seconds": wall, "immutable_model_identity": identity,
            "automatic_engine_reads": auto_total,
            "actions_with_unknown_automatic_reads": unknown_auto,
            "tokens": None, "money": None,
        }
        raw[aid] = {"events": events, "returns": returned, "sources": source_map}
    checks.finish()

    pairs = {}
    for rid in REQUEST_IDS:
        caps = {key: min(arms[rid + "-A"][key], arms[rid + "-B"][key])
                for key in ("queries", "explicit_opens")}
        checks.require(caps == audit_pairs[rid].get("common_caps"), rid + " common caps mismatch")
        paired = {"common_caps": caps, "arms": {}}
        for method in ("A", "B"):
            aid = rid + "-" + method
            audited = audit_pairs[rid]["arms"][aid]
            raw_arm = raw[aid]
            actual_reads = {integer(c["rank"], aid + " rank"): required_reads(c.get("acquisition_event"), raw_arm["sources"])
                            for c in raw_arm["returns"]["final_candidates"]}
            explicit_indices = {e["event_index"] for e in raw_arm["events"] if explicit(e)}
            for rank, necessary in actual_reads.items():
                checks.require(necessary <= explicit_indices, aid + " candidate has a non-read acquisition index")
            by_order = {}
            for name, chronological in (("event_index_prefix", False), ("utc_start_prefix", True)):
                computed = prefix(raw_arm["events"], caps, chronological)
                claimed = audited[name]
                checks.require(computed["included_action_indices"] == claimed["included_action_indices"],
                               aid + " " + name + " action order differs")
                for key in ("consumed_queries", "consumed_explicit_opens"):
                    checks.require(computed[key] == claimed[key], aid + " " + name + " cost differs")
                required_from_audit = {int(c["rank"]): set(c["required_read_event_indices"])
                                       for c in claimed["candidate_checks"]}
                checks.require(actual_reads == required_from_audit, aid + " substantive-read prerequisites differ from audit")
                inside = set(computed["included_action_indices"])
                eligible = sorted(rank for rank, needed in actual_reads.items() if needed <= inside)
                checks.require(eligible == claimed["eligible_final_candidate_ranks"], aid + " prefix candidate eligibility differs")
                computed["eligible_final_candidate_ranks"] = eligible
                by_order[name] = computed
            index_set = set(by_order["event_index_prefix"]["eligible_final_candidate_ranks"])
            time_set = set(by_order["utc_start_prefix"]["eligible_final_candidate_ranks"])
            certain = sorted(index_set & time_set)
            indeterminate = sorted(index_set ^ time_set)
            checks.require(certain == audited["unambiguous_eligible_ranks"] and
                           indeterminate == audited["indeterminate_ranks"], aid + " ambiguity was not preserved")
            paired["arms"][aid] = {**by_order, "unambiguous_eligible_ranks": certain,
                                    "indeterminate_ranks": indeterminate,
                                    "required_read_event_indices": {str(k): sorted(v) for k, v in actual_reads.items()}}
        pairs[rid] = paired
    checks.require(pairs["R3"]["arms"]["R3-B"]["unambiguous_eligible_ranks"] == [] and
                   pairs["R3"]["arms"]["R3-B"]["indeterminate_ranks"] == [1, 3],
                   "R3-B's documented rank 1/rank 3 ambiguity must remain explicit")
    totals = {key: sum(a[key] for a in arms.values()) for key in
              ("queries", "explicit_opens", "final_links", "final_vacancies", "source_rows", "logged_result_rows", "events")}
    checks.require(totals == audit.get("summary", {}).get("totals"), "Raw event totals differ from audit totals")
    checks.require(totals["final_links"] == 33 and totals["final_vacancies"] == 3,
                   "Expected 33 returned candidates and three retained vacancies")
    checks.finish()
    return arms, pairs, raw, totals


def unique_keys(rows, flag_column, key_column):
    keys = set()
    for row in rows:
        if flag(row.get(flag_column), flag_column):
            if not row.get(key_column):
                raise LedgerError("Flagged row lacks %s: %s" % (key_column, row.get("candidate_id")))
            keys.add(row[key_column])
    return sorted(keys)


def novelty(rows):
    choices = unique_keys(rows, "new_implementation_flag", "choice_key")
    tests = unique_keys(rows, "new_test_flag", "test_key")
    return {"implementation_choice_keys": choices, "test_keys": tests,
            "new_implementation_choices": len(choices), "new_discriminating_tests": len(tests)}


def adjudicated_counts(candidates, choices, costs, arms, pairs, raw):
    checks = Checks()
    cmap = keyed(candidates, "candidate_id", "candidates.csv")
    choice_map = keyed(choices, "candidate_id", "choices.csv")
    cost_map = keyed([dict(r, arm_id=r.get("request_id", "") + "-" + r.get("arm", "")) for r in costs],
                     "arm_id", "costs.csv")
    expected_ids = {"%s-%d" % (aid, rank) for aid in ARM_IDS for rank in (1, 2, 3)}
    checks.require(set(cmap) == expected_ids and len(candidates) == 36, "Candidate table must retain all 36 original slots")
    checks.require(len(choices) == 33 and set(choice_map) == {k for k, v in cmap.items() if v.get("return_state") == "returned"},
                   "Choices must have exactly the 33 returned candidate rows")
    checks.require(set(cost_map) == set(ARM_IDS), "Costs must cover each arm exactly once")
    checks.finish()
    for aid in ARM_IDS:
        finals = {int(c["rank"]): c for c in raw[aid]["returns"]["final_candidates"]}
        for rank in (1, 2, 3):
            candidate = cmap["%s-%d" % (aid, rank)]
            rid, method = aid.split("-")
            checks.require(candidate.get("request_id") == rid and candidate.get("arm") == method and
                           integer(candidate.get("returned_rank"), "returned_rank") == rank, aid + " candidate identity changed")
            if rank not in finals:
                checks.require(candidate.get("return_state") == "vacant", aid + " missing retained vacancy")
                checks.require(not flag(candidate.get("new_implementation_flag")) and not flag(candidate.get("new_test_flag")),
                               aid + " vacancy has novelty credit")
            else:
                original = finals[rank]
                for field in ("url", "source_ref", "source_id"):
                    checks.require(candidate.get(field) == str(original.get(field, "")), aid + " returned " + field + " changed")
                choice = choice_map[candidate["candidate_id"]]
                for field in ("request_id", "arm", "returned_rank", "choice_key", "test_key", "common_prefix_status"):
                    checks.require(choice.get(field) == candidate.get(field), candidate["candidate_id"] + " choice mismatch: " + field)
                for field in ("new_implementation_flag", "new_test_flag"):
                    checks.require(flag(choice.get(field)) == flag(candidate.get(field)), candidate["candidate_id"] + " flag mismatch")
                pa = pairs[rid]["arms"][aid]
                status = ("eligible" if rank in pa["unambiguous_eligible_ranks"] else
                          "indeterminate" if rank in pa["indeterminate_ranks"] else "excluded")
                checks.require(candidate.get("common_prefix_status") == status, candidate["candidate_id"] + " prefix status mismatch")
                checks.require(not flag(choice.get("experiment_executed")), candidate["candidate_id"] + " unexpectedly claims an executed experiment")
                checks.require(not flag(choice.get("new_distant_domain_principle")), candidate["candidate_id"] + " unexpectedly claims discovered distant-domain principle")
                checks.require(not flag(choice.get("strict_comparison_eligible")) and
                               not flag(candidate.get("strict_comparison_eligible")), candidate["candidate_id"] + " strict eligibility incorrectly credited")
                if rid == "R6":
                    checks.require(choice.get("current_eligibility") == "provisional_exposed_reader" and
                                   not flag(choice.get("original_discussion_blind")), "R6 provisional exposure status missing")
        own = [c for c in choices if c["request_id"] + "-" + c["arm"] == aid]
        eligible = [c for c in own if c["common_prefix_status"] == "eligible"]
        full = novelty(own)
        common = novelty(eligible)
        arms[aid]["full_novelty"] = full
        arms[aid]["common_prefix_novelty"] = common
        cost = cost_map[aid]
        for field, key in (("queries", "queries"), ("explicit_opens", "explicit_opens"),
                           ("final_links", "final_links"), ("vacancies", "final_vacancies")):
            checks.require(integer(cost.get(field), aid + " cost " + field) == arms[aid][key], aid + " cost mismatch: " + field)
        for field, value in (("full_unique_choices", full["new_implementation_choices"]),
                             ("full_unique_tests", full["new_discriminating_tests"]),
                             ("common_acquired_choice_keys", common["new_implementation_choices"]),
                             ("common_acquired_test_keys", common["new_discriminating_tests"])):
            checks.require(integer(cost.get(field), aid + " cost " + field) == value, aid + " deduplicated cost count mismatch: " + field)
        p = pairs[aid.split("-")[0]]["arms"][aid]
        for column, key in (("common_eligible_ranks", "unambiguous_eligible_ranks"),
                            ("common_indeterminate_ranks", "indeterminate_ranks")):
            checks.require(json.loads(cost.get(column, "[]")) == p[key], aid + " cost prefix ranks mismatch")
        checks.require(math.isclose(float(cost["wall_seconds"]), arms[aid]["wall_seconds"], abs_tol=.002), aid + " cost wall time mismatch")
        for field in ("automatic_reads", "tokens", "money"):
            checks.require(not known(cost.get(field)), aid + " unknown " + field + " must not be represented as a measured zero")
    checks.finish()
    request_counts = {}
    for rid in REQUEST_IDS:
        own = [c for c in choices if c["request_id"] == rid]
        request_counts[rid] = {
            **novelty(own), "unique_requests": 1, "comparison_classification": "비교 불가",
            "comparison_eligible_numerator": 0, "comparison_request_denominator": 1,
            "provisional_reader_exposure": rid == "R6",
            "arms": {a: arms[rid + "-" + a]["full_novelty"] for a in ("A", "B")},
            "common_prefix_novelty": novelty([c for c in own if c["common_prefix_status"] == "eligible"]),
        }
    return cmap, choice_map, cost_map, request_counts


def source_interval(row):
    for key in ("read_interval_utc", "verified_reopen_interval_utc", "retrieval_interval_utc", "attempt_interval_utc"):
        value = row.get(key)
        if isinstance(value, dict):
            value = [value.get("start") or value.get("started_utc") or value.get("start_utc"),
                     value.get("end") or value.get("ended_utc") or value.get("end_utc")]
        if isinstance(value, list) and len(value) == 2 and all(value):
            start, end = (utc(v, row["source_id"] + "." + key) for v in value)
            if start <= end:
                return value
    return None


def source_counts(sources, choices, raw=None):
    checks = Checks()
    smap = keyed(sources, "source_id", "sources.jsonl")
    credited, category_sets = {}, defaultdict(set)
    all_work_sets = defaultdict(set)
    rows_by_category = Counter()
    bounded_failures = []
    bounded_rereads = []
    search_excerpts = []
    raw_intervals = {}
    for aid, arm in (raw or {}).items():
        for sid, source in arm["sources"].items():
            ref = source.get("ref_id") or source.get("source_ref")
            matches = [event for event in arm["events"] if explicit(event)
                       and ref and ref in event.get("ref_ids", [])]
            if len(matches) == 1:
                event = matches[0]
                raw_intervals[sid] = {
                    "read_interval_utc": [event["started_utc"], event["ended_utc"]],
                    "interval_source": "evidence/search/%s/events.jsonl#event_index=%s" % (aid, event["event_index"]),
                }
    for row in sources:
        sid = row["source_id"]
        missing = sorted(SOURCE_FIELDS - set(row))
        checks.require(not missing, sid + " missing source schema fields: " + ", ".join(missing))
        if missing:
            continue
        work = row.get("original_work_id")
        category = row.get("count_category")
        checks.require(isinstance(work, str) and bool(work.strip()), sid + " missing original_work_id")
        checks.require(isinstance(category, str) and bool(category), sid + " missing count_category")
        rows_by_category[category] += 1
        all_work_sets[category].add(work)
        counted = flag(row["counts_as_unique_primary"], sid + " primary count")
        if counted:
            checks.require(work not in credited, "Duplicate primary count flag for original_work_id %s: %s / %s" %
                           (work, credited.get(work, {}).get("source_id"), sid))
            checks.require(category in EXPECTED_PRIMARY_CATEGORIES, sid + " primary flag in an inadmissible category: " + category)
            credited[work] = {"source_id": sid, "count_category": category}
            category_sets[category].add(work)
        if row.get("direct_read_utc"):
            utc(row["direct_read_utc"], sid + ".direct_read_utc")
        else:
            failure_text = " ".join(str(row.get(k, "")) for k in
                                    ("source_kind", "retrieval_status", "failure", "failure_detail", "confirmed", "count_category")).lower()
            failure = any(word in failure_text for word in ("fail", "access", "blocked", "landing", "404", "429", "inaccessible"))
            interval = source_interval(row)
            interval_origin = "source row"
            if interval is None and sid in raw_intervals:
                interval = source_interval(dict(row, read_interval_utc=raw_intervals[sid]["read_interval_utc"]))
                interval_origin = raw_intervals[sid]["interval_source"]
            excerpt = "search_excerpt_not_directly_read" in str(row.get("source_kind", ""))
            unused = row.get("used_for_judgment") is False and not row.get("linked_candidates")
            reread = "reread" in str(row.get("source_kind", "")) and bool(row.get("timestamp_basis"))
            if excerpt and unused and not counted and row.get("search_observed_utc"):
                utc(row["search_observed_utc"], sid + ".search_observed_utc")
                search_excerpts.append({"source_id": sid, "search_observed_utc": row["search_observed_utc"],
                                        "direct_read_claimed": False, "used_for_judgment": False})
            elif interval is not None and not counted and (failure or reread):
                record = {"source_id": sid, "read_interval_utc": interval, "interval_source": interval_origin}
                (bounded_failures if failure else bounded_rereads).append(record)
            else:
                checks.require(False, sid + " null read timestamp lacks an admissible uncredited failure/reread interval or unused search-excerpt observation")
    counts = {category: len(category_sets[category]) for category in EXPECTED_PRIMARY_CATEGORIES}
    checks.require(counts == EXPECTED_PRIMARY_CATEGORIES,
                   "Credited original-work/function families differ from expected allocation: " + json.dumps(counts, sort_keys=True))
    for choice in choices:
        ids = json.loads(choice.get("source_ids", "[]"))
        checks.require(isinstance(ids, list) and all(sid in smap for sid in ids),
                       choice["candidate_id"] + " has missing verification source references")
    checks.finish()
    return smap, {
        "source_rows": len(sources), "credited_unique_primary_work_total": len(credited),
        "credited_unique_primary_works_by_category": counts,
        "credited_work_ids_by_category": {k: sorted(v) for k, v in sorted(category_sets.items())},
        "credited_source_by_work_id": dict(sorted(credited.items())),
        "source_rows_by_category": dict(sorted(rows_by_category.items())),
        "all_recorded_work_ids_by_category": {k: sorted(v) for k, v in sorted(all_work_sets.items())},
        "uncredited_access_failures_with_bounded_utc": bounded_failures,
        "uncredited_rereads_with_bounded_utc": bounded_rereads,
        "unused_search_excerpts_without_direct_read": search_excerpts,
        "duplicate_primary_count_flags": 0,
        "count_semantics": "Audited original-work/function families; not independent implementations. Counter/external verification is not search discovery.",
    }


def frame_and_requests(frame, requests, baseline):
    checks = Checks()
    repositories = Counter(r.get("repository") for r in frame)
    checks.require(repositories == {"node-red/node-red": 80, "xyflow/xyflow": 80}, "Frame must contain 80 rows per repository")
    identities = {(r.get("repository"), r.get("number")) for r in frame}
    checks.require(len(identities) == 160, "Frame identities are not unique")
    checks.require(all(not flag(r.get("is_pr"), "frame.is_pr") for r in frame), "Frame includes a PR")
    for repository in repositories:
        part = [r for r in frame if r["repository"] == repository]
        checks.require(sorted(integer(r["frame_rank"], "frame rank") for r in part) == list(range(1, 81)),
                       repository + " frame ranks differ from 1-80")
    bmap = keyed(baseline, "id", "baseline.csv")
    request_map = keyed(requests, "id", "requests.jsonl")
    checks.require(set(request_map) == set(REQUEST_IDS) and set(bmap) == set(REQUEST_IDS), "Expected exactly six requests/baselines")
    checks.require(len({r.get("url") for r in requests}) == 6, "Requests are not six unique URLs")
    natural, synthetic, unknown_kind = [], [], []
    original_confirmed, original_missing = [], []
    for row in requests:
        rid = row["id"]
        checks.require((row["repository"], str(row["number"])) in identities, rid + " not in frame")
        selected = [f for f in frame if f.get("request_id") == rid]
        checks.require(len(selected) == 1 and selected[0]["url"] == row["url"], rid + " frame selection mismatch")
        kind = str(bmap[rid].get("input_kind", row.get("input_kind", ""))).lower()
        if kind.startswith("natural"):
            natural.append(rid)
        elif kind.startswith("synthetic"):
            synthetic.append(rid)
        else:
            unknown_kind.append(rid)
        status = str(row.get("original_version_status", "")).lower()
        missing = row.get("original_version_missing", True)
        # Never infer confirmation from a creation timestamp or current body.
        confirmed = (not flag(missing, rid + " original_version_missing") and
                     status in {"confirmed_original", "original_edition_confirmed", "verified_original", "verified_first_edition"})
        (original_confirmed if confirmed else original_missing).append(rid)
    checks.require(len(natural) == 6 and not synthetic and not unknown_kind, "Natural/synthetic request classification differs from six natural requests")
    checks.require(not original_confirmed, "This ledger has no authenticated original edition; confirmation unexpectedly asserted")
    checks.finish()
    return request_map, bmap, {
        "frame_total": len(frame), "frame_rows_by_repository": dict(sorted(repositories.items())),
        "unique_requests": len(request_map), "natural_requests": len(natural),
        "synthetic_requests": len(synthetic), "unknown_request_kind": len(unknown_kind),
        "original_editions_confirmed": len(original_confirmed), "original_editions_missing": original_missing,
    }


def cell(value):
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return html.escape(str(value if value is not None else "미확인"), quote=False).replace("|", "\\|").replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def full_link(url, label=None):
    if not isinstance(url, str) or not re.match(r"^https?://", url):
        raise LedgerError("Expected a full HTTP(S) URL for report: %r" % url)
    # Keep the full URL visible; escape Markdown destination delimiters only.
    target = url.replace("(", "%28").replace(")", "%29").replace(" ", "%20")
    return "[%s](%s)" % (cell(label if label is not None else url).replace("[", "\\[").replace("]", "\\]"), target)


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |",
                      "| " + " | ".join("---" for _ in headers) + " |"] +
                     ["| " + " | ".join(row) + " |" for row in rows])


def render_tables(requests, candidates, cost_map, source_map, counts, after_map, notes):
    checks = Checks()
    candidate_notes = notes.get("candidates", {})
    aftermath_notes = notes.get("aftermath", {})
    checks.require(set(aftermath_notes) == set(REQUEST_IDS), "Display notes need all six aftermath summaries")
    for candidate in candidates:
        cid = candidate["candidate_id"]
        if candidate["return_state"] == "returned":
            checks.require(cid in candidate_notes and all(known(candidate_notes[cid].get(k))
                           for k in ("edition_section", "change", "test", "limit")), cid + " missing display-note fields")
    checks.finish()
    rows1 = []
    for rid in REQUEST_IDS:
        r = requests[rid]
        rows1.append([
            cell(rid + " · " + r["title"]),
            cell("공개 현재본문·탐색층 / 원문 최초판 미확인"), full_link(r["url"]),
            cell(r["target_part"] + " · " + r["purpose"] + " / " + r["exact_location"]),
            cell("① " + r["condition_1"] + "\n② " + r["condition_2"]),
            cell(r["known_baseline"]), cell(r.get("unknowns") or "원문판·환경·사전 인지 미확인"),
        ])
    rows2 = []
    fit_labels = {"conditional": "조건부", "near_miss": "근접 실패", "source_contract_only": "원문 계약 범위",
                  "same_pair_interpretation_only": "동일 노드쌍 해석에 한정"}
    for c in sorted(candidates, key=lambda x: (REQUEST_IDS.index(x["request_id"]), x["arm"], int(x["returned_rank"]))):
        aid = c["request_id"] + "-" + c["arm"]
        cost = cost_map[aid]
        cost_text = "%s 전체 검색%s·명시열람%s·%.3f초; 자동열람·토큰·금액 미확인" % (
            aid, cost["queries"], cost["explicit_opens"], float(cost["wall_seconds"]))
        identity = cell("%s · 방식 %s · 원래 %s위" % (c["request_id"], c["arm"], c["returned_rank"]))
        if c["return_state"] == "vacant":
            rows2.append([identity, "공석", "반환 후보 없음; 타 분야 원리 없음", "—",
                          cell(c.get("vacancy_reason") or "공석 사유 미기록"), cell(cost_text)])
            continue
        n = candidate_notes[c["candidate_id"]]
        source = source_map.get(c["source_id"], {})
        actual = source.get("actual_url") or c["url"]
        linked = full_link(actual) + "<br>" + cell(n["edition_section"])
        change = cell(n["change"]) + "<br>" + cell("형태: %s; 새 구현%s·새 시험%s; 먼 타 분야 원리 없음" % (
            c.get("adjudicated_form", c.get("form", "미확인")), c["new_implementation_flag"], c["new_test_flag"]))
        limit = cell(n["limit"])
        fit = fit_labels.get(c.get("conditional_target_fit"), c.get("conditional_target_fit", "미확인"))
        limit += "<br>" + cell("현재 적합성: " + fit + "; 실제 실행 없음")
        if c["request_id"] == "R6":
            limit += "<br>R6 사후 논의 노출 독해자: 잠정 판정"
        rows2.append([identity, linked, change, cell(n["test"]), limit, cell(cost_text)])
    rows3 = []
    for rid in REQUEST_IDS:
        n = counts[rid]
        text = "구현%d·시험%d (요청 내 키 합집합; A %d/%d, B %d/%d)" % (
            n["new_implementation_choices"], n["new_discriminating_tests"],
            n["arms"]["A"]["new_implementation_choices"], n["arms"]["A"]["new_discriminating_tests"],
            n["arms"]["B"]["new_implementation_choices"], n["arms"]["B"]["new_discriminating_tests"])
        if rid == "R6":
            text = "잠정 · " + text
        followup = cell(aftermath_notes[rid]) + "<br>" + full_link(after_map[rid]["issue_url"], "공개 후속 기록")
        rows3.append([cell(rid + " · 고유 요청 1"), "비교 불가", cell(text), followup, "0/1"])
    return "\n\n".join([
        table(["요청", "층·원문판", "주소", "선택 부분", "두 조건", "이미 해본 안", "미확인"], rows1),
        table(["요청·방식·순위", "실제 반환 URL·판·절", "새 조작·타 분야 원리", "선택을 가를 입력", "반례·한계", "비용"], rows2),
        table(["고유 요청", "비교 분류", "새 구현·새 시험", "실제 후속", "비교 가능 분모"], rows3),
    ]) + "\n"


def validate_weakness_table(analysis):
    lines = analysis.rstrip().splitlines()
    if not lines or not lines[-1].lstrip().startswith("|"):
        raise LedgerError("result-analysis.md must end with the weakness table")
    first = len(lines) - 1
    while first and lines[first - 1].lstrip().startswith("|"):
        first -= 1
    block = lines[first:]
    if len(block) != 5:
        raise LedgerError("Trailing weakness table must have one header, one separator and exactly three data rows")
    divider = block[1].strip().strip("|").split("|")
    if not all(re.fullmatch(r"\s*:?-{3,}:?\s*", c) for c in divider):
        raise LedgerError("Invalid trailing weakness-table separator")
    context = " ".join(lines[max(0, first - 5):first + 1]).lower()
    if not any(word in context for word in ("약점", "한계", "weakness")):
        raise LedgerError("Trailing three-row table is not identified as a weakness/limitation table")
    return 3


def recalculate():
    requests = json_lines("requests.jsonl")
    baseline_fields, baseline = csv_file("baseline.csv")
    candidate_fields, candidates = csv_file("candidates.csv")
    _, choices = csv_file("choices.csv")
    _, costs = csv_file("costs.csv")
    _, frame = csv_file("frame.csv")
    _, aftermath = csv_file("aftermath.csv")
    sources = json_lines("sources.jsonl")
    audit = json_file("evidence/audit/execution-audit.json")
    notes = json_file("evidence/display-notes.json")
    analysis = read_text("result-analysis.md")

    frozen = verify_frozen(requests, baseline_fields, baseline, candidate_fields, candidates)
    request_map, baseline_map, population = frame_and_requests(frame, requests, baseline)
    arms, pairs, raw, totals = raw_execution(audit, request_map)
    candidate_map, choice_map, cost_map, per_request = adjudicated_counts(candidates, choices, costs, arms, pairs, raw)
    source_map, source_metrics = source_counts(sources, choices, raw)
    checks = Checks()
    after_map = keyed(aftermath, "request_id", "aftermath.csv")
    checks.require(set(after_map) == set(REQUEST_IDS), "Aftermath must cover all six requests")
    for rid, row in after_map.items():
        checks.require(row.get("issue_url") == request_map[rid]["url"], rid + " aftermath issue mismatch")
        checks.require(row.get("search_seal_sha") == SEARCH_SEAL, rid + " aftermath seal mismatch")
        checks.require(integer(row.get("reviewer_tests_executed"), rid + " aftermath executions") == 0,
                       rid + " reviewer execution unexpectedly claimed")
        checks.require("not_established" in row.get("recommendation_causal_effect", ""),
                       rid + " aftermath must not imply recommendation causality")
    checks.finish()
    weakness_rows = validate_weakness_table(analysis)

    missing_models = [aid for aid in ARM_IDS if arms[aid]["immutable_model_identity"] is None]
    missing_auto = [aid for aid in ARM_IDS if arms[aid]["automatic_engine_reads"] is None]
    gaps = [
        {"code": "original_editions_missing", "request_ids": population["original_editions_missing"],
         "effect": "Current opening posts and issue creation dates do not authenticate original request editions."},
        {"code": "immutable_backend_identity_missing", "arm_ids": missing_models,
         "effect": "Displayed model names do not establish a fixed backend/version."},
        {"code": "automatic_engine_reads_unmeasured", "arm_ids": missing_auto,
         "effect": "Automatic reads remain null/unknown, not zero; complete cost equality is not established."},
        {"code": "token_and_monetary_cost_unmeasured", "arm_ids": list(ARM_IDS)},
        {"code": "R3_B_prefix_identity_ambiguity", "candidate_ranks": [1, 3],
         "effect": "Neither identity receives unqualified common-prefix credit."},
        {"code": "R6_reader_outcome_exposure", "request_ids": ["R6"],
         "effect": "R6 descriptive novelty counts are provisional, not blind-comparison successes."},
        {"code": "no_candidate_experiments_executed", "executed": 0},
    ]
    strict_eligible = [rid for rid in REQUEST_IDS
                       if rid not in population["original_editions_missing"]
                       and all(arms[rid + "-" + a]["immutable_model_identity"] is not None
                               and arms[rid + "-" + a]["automatic_engine_reads"] is not None for a in ("A", "B"))
                       and bool(audit.get("summary", {}).get("strict_comparison_validated"))
                       and all(flag(c.get("strict_comparison_eligible")) for c in choices if c["request_id"] == rid)]
    if strict_eligible:
        raise LedgerError("Unexpected strict comparison eligibility: " + ", ".join(strict_eligible))
    novelty_totals = {
        "new_implementation_choices": sum(r["new_implementation_choices"] for r in per_request.values()),
        "new_discriminating_tests": sum(r["new_discriminating_tests"] for r in per_request.values()),
        "raw_implementation_flag_rows": sum(flag(c["new_implementation_flag"]) for c in choices),
        "raw_test_flag_rows": sum(flag(c["new_test_flag"]) for c in choices),
        "proposed_diagnostic_input_rows": len(choices),
        "executed_candidate_experiments": sum(flag(c["experiment_executed"]) for c in choices),
        "executed_reviewer_aftermath_tests": sum(int(r["reviewer_tests_executed"]) for r in aftermath),
        "distant_domain_discovered": sum(flag(c["new_distant_domain_principle"]) for c in choices),
        "R6_provisional": {k: per_request["R6"][k] for k in ("new_implementation_choices", "new_discriminating_tests")},
        "aggregation": "Sum of within-request unions of flagged keys, not raw flag sums; arm-specific sets are reported separately.",
    }
    input_paths = ["requests.jsonl", "baseline.csv", "candidates.csv", "choices.csv", "costs.csv", "frame.csv",
                   "sources.jsonl", "aftermath.csv", "evidence/audit/execution-audit.json",
                   "evidence/display-notes.json", "result-analysis.md"]
    metrics = {
        "schema_version": 1, "workstream": "AF-RES-109", "ledger_integrity": "pass",
        "research_status": "PARTIAL", "research_complete": False,
        "exit_zero_semantics": "Ledger-integrity pass only; does not mean research COMPLETE, source fit success or executed behavioral verification.",
        "frozen_checks": frozen, "population": population, "event_totals": totals,
        "candidate_slots": len(candidates), "returned_candidates": len(choices),
        "vacant_candidate_ids": sorted(c["candidate_id"] for c in candidates if c["return_state"] == "vacant"),
        "arms": arms, "common_prefix_pairs": pairs, "per_request": per_request,
        "novelty_totals": novelty_totals, "sources": source_metrics,
        "strict_comparison": {"eligible_requests": len(strict_eligible), "total_requests": len(REQUEST_IDS),
                              "fraction": "0/6", "classifications": {r: "비교 불가" for r in REQUEST_IDS},
                              "separate_from_descriptive_choice_counts": True},
        "research_gaps": gaps,
        "same_request_automatic_exposure_arms_from_audit": audit.get("summary", {}).get("known_same_request_auto_exposure_arms", []),
        "aftermath": {r: {"classification": after_map[r]["outcome_classification"],
                           "requester_execution_status": after_map[r]["requester_execution_status"],
                           "recommendation_causal_effect": after_map[r]["recommendation_causal_effect"]} for r in REQUEST_IDS},
        "report_tables": {"request_rows": 6, "candidate_rows_including_vacancies": 36,
                          "request_outcome_rows": 6, "trailing_weakness_data_rows": weakness_rows},
        "input_sha256": {path: digest(owned(path).read_bytes()) for path in input_paths},
    }
    tables = render_tables(request_map, candidates, cost_map, source_map, per_request, after_map, notes)
    result = tables.rstrip() + "\n\n" + analysis.strip() + "\n"
    if not tables.startswith("| 요청 |") or not result.startswith("| 요청 |"):
        raise LedgerError("The three required tables must come first")
    validate_weakness_table(result)
    outputs = {
        OUTPUTS[0]: json.dumps(metrics, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        OUTPUTS[1]: tables,
        OUTPUTS[2]: result,
    }
    return metrics, outputs


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="verify inputs and write the three owned derived reports")
    mode.add_argument("--check", action="store_true", help="recompute and byte-compare saved reports without mutations")
    args = parser.parse_args(argv)
    try:
        metrics, outputs = recalculate()
        if args.write:
            for relative, content in outputs.items():
                if relative not in OUTPUTS:
                    raise LedgerError("Unexpected report output: " + relative)
                path = owned(relative)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
        else:
            mismatches = []
            for relative, expected in outputs.items():
                path = owned(relative)
                if not path.is_file():
                    mismatches.append(relative + " (missing saved output)")
                elif path.read_bytes() != expected.encode("utf-8"):
                    mismatches.append(relative + " (stale or changed)")
            if mismatches:
                raise LedgerError("Derived-output mismatch: " + "; ".join(mismatches))
        print(json.dumps({
            "mode": "write" if args.write else "check", "ledger_integrity": "pass",
            "research_status": metrics["research_status"], "research_complete": False,
            "requests": metrics["population"]["unique_requests"], "candidate_slots": metrics["candidate_slots"],
            "returned_candidates": metrics["returned_candidates"], "vacancies": len(metrics["vacant_candidate_ids"]),
            "queries": metrics["event_totals"]["queries"], "explicit_opens": metrics["event_totals"]["explicit_opens"],
            "new_implementation_choices": metrics["novelty_totals"]["new_implementation_choices"],
            "new_tests_proposed": metrics["novelty_totals"]["new_discriminating_tests"],
            "executed_candidate_experiments": metrics["novelty_totals"]["executed_candidate_experiments"],
            "credited_primary_work_families": metrics["sources"]["credited_unique_primary_work_total"],
            "strict_comparison_denominator": metrics["strict_comparison"]["eligible_requests"],
            "R3_B_indeterminate_ranks": metrics["common_prefix_pairs"]["R3"]["arms"]["R3-B"]["indeterminate_ranks"],
            "exit_zero_means": "ledger_integrity_only",
        }, ensure_ascii=False, sort_keys=True))
        return 0
    except (LedgerError, OSError, ValueError, TypeError, KeyError, csv.Error) as exc:
        print(json.dumps({"mode": "write" if args.write else "check", "ledger_integrity": "fail",
                          "research_status": "PARTIAL", "research_complete": False,
                          "error_type": type(exc).__name__, "error": str(exc)}, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
