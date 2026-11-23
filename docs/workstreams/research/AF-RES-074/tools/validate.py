#!/usr/bin/env python3
"""Validate AF-RES-074's evidence ledgers, independently of their builders.

This checks structural consistency and committed transport artifacts.  PASS is
not a claim that missing original requests or historical executions were found.
No network, Git mutations, or product execution is performed.
"""
from __future__ import annotations

import argparse
import base64
import collections
import csv
import datetime as dt
import hashlib
import json
import re
import shlex
import struct
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

OWNED = "docs/workstreams/research/AF-RES-074/"
ROOT = Path(__file__).resolve().parents[5]
TASK = ROOT / OWNED
STATUSES = ("correct_single", "conditional_actionable", "wrong", "hold", "enumeration_unresolved", "unjudgeable")
POLICIES = ("A", "B", "C")
BRANCHES = ("value1", "value2", "no_answer")
HEADERS = {
    "frame.csv": "frame_id repository rank issue_number created_utc original_url checked_utc selected case_id query_terms status exclusion_reason initial_status body_sha256 source_ledger",
    "policies.csv": "row_id case_id stratum policy response_branch scenario_value answer question question_rounds_planned completed_reply_rounds_in_scenario scenario_kind candidate_refs answer_urls displayed_link_references distinct_answer_urls distinct_answer_documents pre_known_field_value conflicts_with_pre_known_value literal_lang_retention_ambiguity actual_user_response_to_our_policy human_time response_probability seal_commit source_ledger",
    "criteria.csv": "criterion_id case_id stratum version field value1 value2 input1 input2 expected_output1 expected_output2 criterion_urls same_version same_input only_one_field_changed expected_equal historical_execution_status historical_execution_output1 historical_execution_output2 researcher_execution_version researcher_execution_output1 researcher_execution_output2 evidence_level technical_pair_denominator strict_initial_effect_denominator limit source_ledger equality_scope analytical_discriminator",
    "events.csv": "event_id case_id url source_id actor actor_role created_utc updated_utc text_version event_kind selected_field_value new_selected_field_information observed_choice author_success_report independent_success summary limitation actual_response_to_our_policy source_ledger elicitation_kind stimulus_event_id",
    "scores.csv": "row_id case_id stratum policy response_branch scenario_value status original_stream_status technical_judgment_denominator strict_initial_effect_denominator inconsistent_counterfactual criterion_id criterion_urls reason avoidable_question avoidable_question_basis necessary_question_omitted necessary_condition_omitted observed_user_selection observed_independent_success condition_identification displayed_link_references distinct_answer_documents planned_question_rounds completed_reply_rounds_in_scenario actual_dialogue_rounds human_time response_probability source_ledger user_selection_scope post_adjudication_note",
    "policy-summary.csv": "stratum policy response_branch total_slots technical_judgment_denominator strict_initial_effect_denominator correct_single conditional_actionable wrong hold enumeration_unresolved unjudgeable avoidable_questions avoidable_question_unknown necessary_question_omitted observed_user_selection row_ids",
    "costs.csv": "case_id stratum A_known_wrong C_known_wrong known_scenarios_per_policy independent_criterion_available valid_alternatives_no_answer C_avoidable_question human_time response_probability potentially_valid_candidate_commands_no_answer distinct_valid_action_classes_no_answer A_no_answer_status A_link_references_no_answer A_distinct_documents_no_answer A_planned_rounds B_no_answer_status B_link_references_no_answer B_distinct_documents_no_answer B_planned_rounds C_no_answer_status C_link_references_no_answer C_distinct_documents_no_answer C_planned_rounds",
    "initial-version-review.csv": "case_id repository issue_number original_url archive_url event_id event_created_utc recovered_utc opening_body_sha256 current_body_sha256 exact_body_equal goal_constraints_changed opening_verified verified_before_policy_seal difference_summary source_ledger prior_failure_ledger",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tri(value):
    """Parse CSV/JSON Booleans case-insensitively; never map unknown to false."""
    if value is None or value == "" or str(value).casefold() in {"null", "none", "unknown", "not_measured"}:
        return None
    if value is True or str(value).casefold() == "true":
        return True
    if value is False or str(value).casefold() == "false":
        return False
    raise ValueError(f"Not a Boolean/null: {value!r}")


def jcell(value):
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return value


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT, stderr=subprocess.PIPE)


def read_json(rel: str):
    return json.loads((TASK / rel).read_text(encoding="utf-8"))


class Audit:
    def __init__(self):
        self.checks = []
        self.errors = []
        self.warnings = []
        self.tables = {}
        self.details = {}

    def check(self, name, condition, detail=None):
        row = {"check": name, "passed": bool(condition)}
        if detail is not None:
            row["detail"] = detail
        self.checks.append(row)
        if not condition:
            self.errors.append(row)
        return condition

    def section(self, name, action):
        try:
            action()
        except Exception as exc:
            self.check(name + " completed", False, f"{type(exc).__name__}: {exc}")

    def csv(self, name):
        path = TASK / name
        self.check(name + " exists", path.is_file())
        if not path.is_file():
            return []
        raw = path.read_bytes()
        self.check(name + " LF line endings", b"\r" not in raw)
        with path.open(newline="", encoding="utf-8") as f:
            cells = list(csv.reader(f))
        self.check(name + " exact header", bool(cells) and cells[0] == HEADERS[name].split(), cells[0] if cells else [])
        width = len(cells[0]) if cells else 0
        malformed = [(i + 2, len(row)) for i, row in enumerate(cells[1:]) if len(row) != width]
        self.check(name + " rectangular", not malformed, malformed)
        rows = [dict(zip(cells[0], row)) for row in cells[1:] if len(row) == width]
        self.tables[name] = rows
        return rows


def unpack_tiff(data: bytes):
    """Read only the uncompressed single-band uint8 TIFFs in this receipt.

    This does not implement resampling or GDAL's checksum algorithm.
    """
    order = "<" if data[:2] == b"II" else ">" if data[:2] == b"MM" else None
    if order is None or struct.unpack_from(order + "H", data, 2)[0] != 42:
        raise ValueError("Expected classic TIFF")
    off = struct.unpack_from(order + "I", data, 4)[0]
    number = struct.unpack_from(order + "H", data, off)[0]
    sizes = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 12: 8}
    tags = {}
    for i in range(number):
        entry = off + 2 + 12 * i
        tag, kind, count = struct.unpack_from(order + "HHI", data, entry)
        if kind not in sizes:
            continue
        length = count * sizes[kind]
        loc = entry + 8 if length <= 4 else struct.unpack_from(order + "I", data, entry + 8)[0]
        payload = data[loc : loc + length]
        if len(payload) != length:
            raise ValueError("Truncated TIFF tag")
        if kind == 3:
            values = struct.unpack(order + "H" * count, payload)
        elif kind == 4:
            values = struct.unpack(order + "I" * count, payload)
        elif kind == 12:
            values = struct.unpack(order + "d" * count, payload)
        else:
            values = tuple(payload)
        tags[tag] = values
    width, height = tags[256][0], tags[257][0]
    if tags.get(258, (1,)) != (8,) or tags.get(259, (1,)) != (1,) or tags.get(277, (1,)) != (1,):
        raise ValueError("Unsupported TIFF encoding; no silent interpretation")
    strips = tags[273]
    lengths = tags[279]
    if len(strips) != len(lengths):
        raise ValueError("Strip count mismatch")
    pixels = b"".join(data[s : s + n] for s, n in zip(strips, lengths))
    if len(pixels) != width * height:
        raise ValueError("Unexpected raster byte length")
    transform = None
    if 33550 in tags and 33922 in tags:
        sx, sy, _ = tags[33550]
        i, j, _, x, y, _ = tags[33922][:6]
        transform = [x - i * sx, sx, 0.0, y + j * sy, 0.0, -sy]
    return {"size": [width, height], "pixels": pixels, "geotransform": transform}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-expanded", action="store_true", help="Require each frozen search frame's second12: total48")
    parser.add_argument("--actor", default="unspecified external caller", help="Actual actor performing this validation")
    args = parser.parse_args()
    started = dt.datetime.now(dt.timezone.utc)
    a = Audit()
    def stop_prerequisite(reason):
        """Replace an old receipt with FAIL if an input cannot even be loaded."""
        a.check("prerequisite loading", False, reason)
        report = {"validator_actor": "AF-RES-074 model structural auditor", "command": shlex.join(["python", "-B", OWNED + "tools/validate.py", *sys.argv[1:]]),
        "argv": ["python", "-B", OWNED + "tools/validate.py", *sys.argv[1:]], "cwd": str(ROOT), "started_utc": started.isoformat(), "ended_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "exit_code": 1, "structural_status": "FAIL", "research_status": "PARTIAL", "check_count": len(a.checks), "error_count": len(a.errors), "errors": a.errors, "warnings": a.warnings, "checks": a.checks}
        output = TASK / "evidence/validation.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({k: report[k] for k in ("structural_status", "research_status", "exit_code", "errors")}, ensure_ascii=False, indent=2))
        return 1

    required = [*HEADERS, "packets.jsonl", "sources.jsonl", "manifest.json", "evidence/seals.json", "evidence/ledger-counts.json", "evidence/gdal3103-artifacts.json", "streams/gdal/researcher-run3103.json", "evidence/pandoc-fixed-run.json", "evidence/pandoc-fixed-fixtures.json", "evidence/pandoc-release-fetch.json"]
    for rel in required:
        a.check("required file " + rel, (TASK / rel).is_file())
    if a.errors:
        return stop_prerequisite("Required ledger or evidence file is missing; no prior PASS receipt is reused.")
    for name in HEADERS:
        a.section(name, lambda n=name: a.csv(n))
    if a.errors:
        return stop_prerequisite("CSV input has an invalid schema or encoding; dependent checks were not run.")
    try:
        packets = [json.loads(x) for x in (TASK / "packets.jsonl").read_text().splitlines() if x.strip()]
        sources = [json.loads(x) for x in (TASK / "sources.jsonl").read_text().splitlines() if x.strip()]
        counted = read_json("evidence/ledger-counts.json")
        manifest = read_json("manifest.json")
    except (ValueError, OSError, UnicodeError) as exc:
        return stop_prerequisite(f"{type(exc).__name__}: {exc}")
    frames, policies, criteria, events, scores, summaries, costs = (a.tables[n] for n in ("frame.csv", "policies.csv", "criteria.csv", "events.csv", "scores.csv", "policy-summary.csv", "costs.csv"))
    initial_reviews = a.tables["initial-version-review.csv"]
    packet_map = {r["case_id"]: r for r in packets}
    source_map = {r["source_id"]: r for r in sources}
    score_map = {r["row_id"]: r for r in scores}
    policy_map = {r["row_id"]: r for r in policies}
    criterion_map = {r["criterion_id"]: r for r in criteria}

    def keys_and_shapes():
        for name, rows, keys in [("frames", frames, ("frame_id",)), ("packets", packets, ("case_id",)), ("policies", policies, ("row_id",)), ("criteria", criteria, ("criterion_id",)), ("events", events, ("event_id",)), ("sources", sources, ("source_id",)), ("scores", scores, ("row_id",)), ("summaries", summaries, ("stratum", "policy", "response_branch")), ("costs", costs, ("case_id",)), ("initial reviews", initial_reviews, ("case_id",))]:
            values = [tuple(row[k] for k in keys) for row in rows]
            a.check(name + " keys unique/nonempty", len(values) == len(set(values)) and all(all(v not in (None, "") for v in key) for key in values))
        expected_cases = {f"{repo}-N{i}" for repo in ("PAN", "GDAL") for i in range(1, 5)} | {f"{repo}-C{i}" for repo in ("PAN", "GDAL") for i in (1, 2)}
        a.check("12 exact packet slots", set(packet_map) == expected_cases and len(packets) == 12)
        a.check("policy/score108 each", len(policies) == len(scores) == 108)
        a.check("criterion12,summary18,cost12", len(criteria) == 12 and len(summaries) == 18 and len(costs) == 12)
        a.check("policy/score row IDs join", set(policy_map) == set(score_map))
        for cid in expected_cases:
            expected = {(cid, pol, branch) for pol in POLICIES for branch in BRANCHES}
            for label, rows in [("policy", policies), ("score", scores)]:
                actual = {(r["case_id"], r["policy"], r["response_branch"]) for r in rows if r["case_id"] == cid}
                a.check(f"{cid} {label} all3x3 branches", actual == expected)
        for label, rows in [("policy", policies), ("criterion", criteria), ("event", events), ("score", scores), ("cost", costs)]:
            a.check(label + " packet joins", all(r["case_id"] in packet_map for r in rows))
        a.check("event source joins", all(r["source_id"] in source_map for r in events))
        a.check("score criterion joins", all(r["criterion_id"] in criterion_map and criterion_map[r["criterion_id"]]["case_id"] == r["case_id"] for r in scores))
        a.check("selected frames are natural slots", {r["case_id"] for r in frames if tri(r["selected"]) is True} == {r["case_id"] for r in packets if r["stratum"] == "natural"})
        frame_counts = collections.Counter(r["repository"] for r in frames)
        a.check("two repositories with complete12-row blocks", set(frame_counts) == {"jgm/pandoc", "OSGeo/gdal"} and all(v in (12, 24) for v in frame_counts.values()), dict(frame_counts))
        for repo, count in frame_counts.items():
            rows = sorted((r for r in frames if r["repository"] == repo), key=lambda r: int(r["rank"]))
            a.check(repo + " ranks and number order", [int(r["rank"]) for r in rows] == list(range(1, count + 1)) and [int(r["issue_number"]) for r in rows] == sorted(int(r["issue_number"]) for r in rows))
        if args.require_expanded:
            a.check("required expanded frame48", len(frames) == 48 and set(frame_counts.values()) == {24})
        elif len(frames) < 48:
            a.warnings.append("Second12 screening incomplete; final validation must use --require-expanded.")
        for label, rows in [("packets", packets), ("policies", policies), ("criteria", criteria), ("scores", scores), ("events", events)]:
            a.check(label + " source-ledger paths exist", all((TASK / r["source_ledger"]).is_file() for r in rows))

    a.section("keys, shapes, joins", keys_and_shapes)

    def initial_provenance_checks():
        natural_ids = {p["case_id"] for p in packets if p["stratum"] == "natural"}
        selected_frames = {r["case_id"]: r for r in frames if tri(r["selected"]) is True}
        a.check("eight initial reviews join natural cases", len(initial_reviews) == 8 and {r["case_id"] for r in initial_reviews} == natural_ids and len({r["event_id"] for r in initial_reviews}) == 8)
        for r in initial_reviews:
            cid = r["case_id"]; frame = selected_frames[cid]
            ledger = read_json(r["source_ledger"])
            original = next(item for item in ledger if item["case_id"] == cid)
            opening_hash = original.get("opening_body_sha256", original.get("initial_body_sha256"))
            current_hash = original["current_body_sha256"]
            canonical_url = f'https://github.com/{r["repository"]}/issues/{r["issue_number"]}'
            equivalent_api_url = f'https://api.github.com/repos/{r["repository"]}/issues/{r["issue_number"]}'
            a.check(cid + " opening event identity/source joins", r["repository"] == frame["repository"] and r["issue_number"] == frame["issue_number"] and r["original_url"] == canonical_url and frame["original_url"] in {canonical_url, equivalent_api_url} and r["event_id"] == str(original["event_id"]) and r["archive_url"] == original["archive_url"] and r["event_created_utc"] == original.get("event_created_utc", original.get("event_created_at")))
            a.check(cid + " opening/current hashes and equality", r["opening_body_sha256"] == opening_hash and r["current_body_sha256"] == current_hash == frame["body_sha256"] and all(re.fullmatch(r"[0-9a-f]{64}", h) is not None for h in (opening_hash, current_hash)) and tri(r["exact_body_equal"]) == (opening_hash == current_hash))
            changed = original.get("semantic_request_difference_observed", original.get("prespecified_field_goal_constraints_changed"))
            a.check(cid + " reviewed goal/constraint comparison", tri(r["goal_constraints_changed"]) is False and changed is False and bool(r["difference_summary"]))
            a.check(cid + " recovery does not rewrite pre-seal exposure", tri(r["opening_verified"]) is True and tri(r["verified_before_policy_seal"]) is False and original.get("policy_seal_unchanged", original.get("freeze_bytes_unchanged")) is True)
            failed = read_json(r["prior_failure_ledger"])
            failure_rows = failed if isinstance(failed, list) else [failed]
            a.check(cid + " original403 failure remains recorded", any(item.get("archive_url", item.get("url")) == r["archive_url"] and "403" in str(item.get("error", "")) for item in failure_rows))
            recovery_time = dt.datetime.fromisoformat(r["recovered_utc"].replace("Z", "+00:00"))
            sealed_time = dt.datetime.fromisoformat(git("show", "-s", "--format=%cI", packet_map[cid]["seal_commit"]).decode().strip())
            a.check(cid + " recovery timestamp follows actual seal commit", recovery_time > sealed_time)
        verified = sum(tri(r["opening_verified"]) is True for r in initial_reviews)
        exact = sum(tri(r["exact_body_equal"]) is True for r in initial_reviews)
        changed_count = sum(tri(r["goal_constraints_changed"]) is True for r in initial_reviews)
        a.check("initial provenance counts recomputed", counted["natural_initial_verified"] == verified == 8 and counted["natural_initial_exact_body_equal"] == exact == 6 and counted["natural_initial_goal_constraints_changed"] == changed_count == 0)
        a.details["initial_version_review"] = {"rows": len(initial_reviews), "opening_verified": verified, "exact_body_equal": exact, "meaning_changed": 0, "verified_before_policy_seal": 0, "scope": "Retrospective original-body provenance; not an intervention or strict question-effect denominator."}

    a.section("recovered initial-version provenance", initial_provenance_checks)

    def source_accounting():
        minimum = [r for r in sources if r["minimum_count"] is True]
        works = {r["work_id"] for r in minimum}
        bycat = collections.Counter(r["minimum_category"] for r in minimum)
        a.check("minimum work IDs counted once", len(works) == len(minimum))
        a.check("conservative minimum at least42", len(works) >= 42, len(works))
        a.check("original quota categories", all(bycat[k] >= n for k, n in {"request": 8, "test_example": 6, "spec_manual": 4, "crossfield_procedure": 4}.items()), dict(bycat))
        a.check("counted sources direct/independent and read", all(r.get("direct_read") is True and r.get("direct_independent_work") is True and r.get("confirmed_content") and not re.search(r"fail|403|404|error|blocked|not.read", r["access_status"], re.I) for r in minimum))
        a.check("contexts not counted", all(not r["minimum_count"] for r in sources if r["minimum_category"] == "context"))
        a.check("failed accesses not counted", all(not r["minimum_count"] for r in sources if re.search(r"fail|403|404|error|blocked", r["access_status"], re.I)))
        mandatory = {"source_id", "work_id", "original_url", "arrival_url", "author_publisher", "version_time", "checked_utc", "read_location", "confirmed_content", "supports_q", "claim_ids", "limitations", "counterevidence", "access_status", "direct_read", "minimum_count", "minimum_category", "minimum_count_reason", "phase"}
        a.check("source schema and real URL strings", all(mandatory <= set(r) and urlsplit(r["original_url"]).scheme in {"http", "https"} and urlsplit(r["arrival_url"]).scheme in {"http", "https"} for r in sources))
        a.check("source counts match ledger-counts", counted["source_rows"] == len(sources) and counted["minimum_independent_works"] == len(works) and counted["minimum_by_category"] == dict(bycat))
        independent = {r["work_id"] for r in sources if r.get("direct_independent_work") is True}
        a.check("direct independent works match declared", len(independent) == counted["direct_independent_works_conservative"])
        a.details["source_counts"] = {"rows": len(sources), "minimum_unique_works": len(works), "minimum_by_category": dict(bycat), "direct_independent_unique_works": len(independent)}

    a.section("source accounting", source_accounting)

    def policy_logic():
        for p in policies:
            rid = p["row_id"]; s = score_map[rid]; packet = packet_map[p["case_id"]]
            a.check(rid + " consistent labels", all(p[k] == s[k] for k in ("case_id", "stratum", "policy", "response_branch", "scenario_value")))
            expected_rounds = int(p["policy"] == "C")
            expected_reply = int(p["policy"] == "C" and p["response_branch"] != "no_answer")
            a.check(rid + " scenario rounds separate from actual", int(p["question_rounds_planned"]) == int(s["planned_question_rounds"]) == expected_rounds and int(p["completed_reply_rounds_in_scenario"]) == int(s["completed_reply_rounds_in_scenario"]) == expected_reply and int(s["actual_dialogue_rounds"]) == 0)
            expected_value = packet["values"][0 if p["response_branch"] == "value1" else 1] if p["response_branch"] != "no_answer" else None
            actual_value = jcell(p["scenario_value"])
            a.check(rid + " branch value preserved", actual_value == expected_value if p["response_branch"] != "no_answer" else actual_value == "unobserved")
            known = jcell(p["pre_known_field_value"])
            known_is_recorded = known is not None and str(known).casefold() not in {"", "unknown", "unobserved", "null", "none"}
            conflict = known_is_recorded and expected_value is not None and known != expected_value
            a.check(rid + " pre conflict Boolean", tri(p["conflicts_with_pre_known_value"]) == conflict)
            if p["case_id"] == "PAN-N2":
                a.check(rid + " intentional language-predicate override", tri(s["inconsistent_counterfactual"]) is False and tri(p["literal_lang_retention_ambiguity"]) is True)
            else:
                a.check(rid + " counterfactual follows pre flag", tri(s["inconsistent_counterfactual"]) == conflict)
            urls = jcell(p["answer_urls"])
            a.check(rid + " link counts", isinstance(urls, list) and int(p["displayed_link_references"]) == len(urls) and int(p["distinct_answer_urls"]) == len(set(urls)) and int(p["distinct_answer_documents"]) == len({u.split("#")[0] for u in urls}))
            a.check(rid + " score link counts", p["displayed_link_references"] == s["displayed_link_references"] and p["distinct_answer_documents"] == s["distinct_answer_documents"])
            a.check(rid + " no measured-person effect", p["actual_user_response_to_our_policy"] == "not_measured_no_contact" and p["human_time"] == s["human_time"] == "not_measured" and p["response_probability"] == s["response_probability"] == "not_measured")
        a.check("no event used for new selected value and independent success", not any(tri(r["new_selected_field_information"]) is True and tri(r["independent_success"]) is True for r in events))
        a.check("no actual responses to our policies", all(tri(r["actual_response_to_our_policy"]) is False for r in events))
        a.check("no actual user experiment count invented", counted["actual_user_experiments"] == 0)
        a.check("all statuses recognized", all(r["status"] in STATUSES for r in scores))
        a.check("natural technical denominator zero", not any(tri(r["technical_judgment_denominator"]) is True for r in scores if r["stratum"] == "natural"))
        a.check("all strict effect denominators zero", not any(tri(r["strict_initial_effect_denominator"]) is True for r in scores))
        known_control = [r for r in scores if r["stratum"] == "constructed" and r["response_branch"] != "no_answer"]
        a.check("24 known control scenario judgments", len(known_control) == 24 and all(tri(r["technical_judgment_denominator"]) is True for r in known_control))
        a.check("no ungrounded correct/wrong judgments", all(tri(r["technical_judgment_denominator"]) is True for r in scores if r["status"] in {"correct_single", "conditional_actionable", "wrong"}))
        for cid in ("PAN-N2", "PAN-N4", "GDAL-N1", "GDAL-N2", "GDAL-N3"):
            a.check(cid + " unknown avoidable C preserved", all(tri(r["avoidable_question"]) is None for r in scores if r["case_id"] == cid and r["policy"] == "C"))

    a.section("policy/scenario logic", policy_logic)

    def aggregate_checks():
        groups = collections.defaultdict(list)
        for r in scores:
            groups[(r["stratum"], r["policy"], r["response_branch"])].append(r)
        for summary in summaries:
            key = tuple(summary[k] for k in ("stratum", "policy", "response_branch")); rows = groups[key]
            expected = {"total_slots": len(rows), "technical_judgment_denominator": sum(tri(r["technical_judgment_denominator"]) is True for r in rows), "strict_initial_effect_denominator": sum(tri(r["strict_initial_effect_denominator"]) is True for r in rows), **{status: sum(r["status"] == status for r in rows) for status in STATUSES}, "avoidable_questions": sum(tri(r["avoidable_question"]) is True for r in rows), "avoidable_question_unknown": sum(tri(r["avoidable_question"]) is None for r in rows), "necessary_question_omitted": sum(tri(r["necessary_question_omitted"]) is True for r in rows)}
            a.check("summary " + str(key), all(int(summary[k]) == v for k, v in expected.items()) and set(jcell(summary["row_ids"])) == {r["row_id"] for r in rows}, expected)
        for row in costs:
            cid = row["case_id"]; controlled = row["stratum"] == "constructed"
            for pol in ("A", "C"):
                known = [score_map[f"{cid}-{pol}-{branch}"] for branch in ("value1", "value2")]
                expected = sum(r["status"] == "wrong" for r in known) if controlled else None
                a.check(cid + " " + pol + " known wrong cost", jcell(row[pol + "_known_wrong"]) == expected)
            a.check(cid + " cost scope", tri(row["independent_criterion_available"]) == controlled and int(row["known_scenarios_per_policy"]) == 2)
            a.check(cid + " question cost flag", tri(row["C_avoidable_question"]) == tri(score_map[f"{cid}-C-no_answer"]["avoidable_question"]))
            for pol in POLICIES:
                s = score_map[f"{cid}-{pol}-no_answer"]
                a.check(cid + " " + pol + " no-answer costs", row[pol + "_no_answer_status"] == s["status"] and row[pol + "_link_references_no_answer"] == s["displayed_link_references"] and row[pol + "_distinct_documents_no_answer"] == s["distinct_answer_documents"] and row[pol + "_planned_rounds"] == s["planned_question_rounds"])
        lengths = {"frame_rows": len(frames), "packet_rows": len(packets), "policy_rows": len(policies), "criterion_rows": len(criteria), "event_rows": len(events), "score_rows": len(scores), "summary_rows": len(summaries), "cost_rows": len(costs)}
        a.check("declared ledger row counts", all(counted[k] == v for k, v in lengths.items()), lengths)
        a.check("event outcome counts", counted["natural_new_selected_field_events"] == sum(tri(r["new_selected_field_information"]) is True for r in events) and counted["independent_success_events"] == sum(tri(r["independent_success"]) is True for r in events) and counted["author_success_report_events"] == sum(tri(r["author_success_report"]) is True for r in events))
        a.details["ledger_counts"] = lengths

    a.section("recomputed summaries and costs", aggregate_checks)

    def criteria_and_input_checks():
        controlled = [r for r in criteria if r["stratum"] == "constructed"]
        a.check("4 controls have one-field matched inputs", len(controlled) == 4 and all(tri(r["same_version"]) is True and tri(r["same_input"]) is True and tri(r["only_one_field_changed"]) is True and tri(r["technical_pair_denominator"]) is True for r in controlled))
        a.check("two positive/two negative expectations", sum(tri(r["expected_equal"]) is True for r in controlled) == 2 and sum(tri(r["expected_equal"]) is False for r in controlled) == 2)
        a.check("historical runs limited to two Pandoc controls", all(r["historical_execution_status"] == ("researcher_performed_fixed_release" if r["case_id"] in {"PAN-C1", "PAN-C2"} else "not_performed") for r in criteria))
        a.check("unperformed historical outputs remain null", all(jcell(r["historical_execution_output1"]) is None and jcell(r["historical_execution_output2"]) is None for r in criteria if r["case_id"] not in {"PAN-C1", "PAN-C2"}))
        for cr in controlled:
            cid = cr["case_id"]; packet = packet_map[cid]
            a.check(cid + " criterion values and field match frozen packet", cr["field"] == packet["field"] and [cr["value1"], cr["value2"]] == packet["values"])
            c1 = shlex.split(packet["candidate1"]["command"])
            c2 = shlex.split(packet["candidate2"]["command"])
            if cid.startswith("PAN-"):
                expected_c2 = [word.replace("latex+raw_tex", "latex") for word in c1]
                condition = c2 == expected_c2 and c1.count("latex+raw_tex") == 1 and c1 != c2
            elif cid == "GDAL-C1":
                condition = c2 == ["-rb" if word == "-rn" else word for word in c1] and c1.count("-rn") == 1 and cr["input1"] == cr["input2"]
            else:
                option = c1.index("-outsize")
                expected_c2 = c1[:option + 1] + ["200%", "200%"] + c1[option + 3:]
                condition = c1[option + 1:option + 3] == ["40", "40"] and c2 == expected_c2 and cr["input1"] == cr["input2"]
            a.check(cid + " one nominated option differs in exact commands", condition)
        for cid in ("PAN-C1", "PAN-C2"):
            cr = criterion_map[cid + "-CR"]; packet = packet_map[cid]
            inputs = [jcell(cr["input1"]), jcell(cr["input2"])]
            a.check(cid + " paired input hashes match", inputs[0]["input_sha256"] == inputs[1]["input_sha256"])
            for idx, variant in enumerate(packet["input_variants"]):
                a.check(cid + f" exact input{idx + 1} content hash", sha256(variant["input"].encode()) == variant["input_sha256"] == inputs[idx]["input_sha256"])
                if cid == "PAN-C1":
                    a.check(cid + f" exact output{idx + 1} content hash", sha256(inputs[idx]["expected_output"].encode()) == inputs[idx]["expected_output_sha256"])
            a.check(cid + " expectation equality hashes", (inputs[0]["expected_output_sha256"] == inputs[1]["expected_output_sha256"]) == tri(cr["expected_equal"]))

    a.section("paired criteria and input hashes", criteria_and_input_checks)

    def historical_pandoc_checks():
        fixtures = read_json("evidence/pandoc-fixed-fixtures.json")
        receipt = read_json("evidence/pandoc-fixed-run.json")
        release = read_json("evidence/pandoc-release-fetch.json")
        pin = "dcbd8d326cce4960e0d736e25e7d00f9057a1fc2"
        version = "2.11.3.2"
        a.check("Pandoc fixture/release/run version and pin", fixtures["pin"] == receipt["source_pin"] == pin and fixtures["version"] == version and receipt["version_stdout"] == release["version_stdout"] and receipt["version_stdout"].splitlines()[0].split()[-1] == version and release["version_exit_code"] == 0)
        a.check("Pandoc official download and binary hash", release["status"] == 200 and release["original_url"] == "https://github.com/jgm/pandoc/releases/download/2.11.3.2/pandoc-2.11.3.2-linux-amd64.tar.gz" and release["member"] == "pandoc-2.11.3.2/bin/pandoc" and re.fullmatch(r"[0-9a-f]{64}", release["binary_sha256"]) is not None and receipt["binary_sha256"] == release["binary_sha256"])
        expected_ids = {f"{name}-{i}" for name, count in [("parse-raw", 2), ("sloppypar", 2), ("empty_paragraphs", 4)] for i in range(1, count + 1)}
        fm = {r["test_id"]: r for r in fixtures["tests"]}
        rm = {r["test_id"]: r for r in receipt["tests"]}
        a.check("Pandoc exactly8 unique fixtures and matching runs", len(fixtures["tests"]) == len(receipt["tests"]) == 8 and set(fm) == set(rm) == expected_ids)
        calls = []
        for test_id, fixture in fm.items():
            run = rm[test_id]
            source_name, block = test_id.rsplit("-", 1)
            expected_source = f"https://github.com/jgm/pandoc/blob/{pin}/test/command/{source_name}.md"
            a.check(test_id + " original pinned source and command join", fixture["source_url"] == run["source_url"] == expected_source and fixture["test_block_number"] == int(block) and fixture["command"] == run["command"])
            a.check(test_id + " exact stdin and logical hashes", fixture["input"].endswith("\n") and sha256(fixture["input"].encode()) == fixture["stdin_sha256"] == run["stdin_sha256"] and sha256(fixture["input"][:-1].encode()) == fixture["input_logical_sha256"])
            actual = run["actual_stdout"]; expected = fixture["expected_stdout"]
            a.check(test_id + " actual/expected stdout bytes and hashes", actual == expected == run["expected_stdout"] and sha256(actual.encode()) == run["actual_stdout_sha256"] == run["expected_stdout_sha256"] and expected.endswith("\n") and sha256(expected[:-1].encode()) == fixture["expected_logical_sha256"] and run["exact_stdout_match"] is True)
            commands = [shlex.split(segment.strip()) for segment in fixture["command"].split("|")]
            a.check(test_id + " actual process calls match command pipeline", len(commands) == len(run["calls"]) and all(command[0] == "pandoc" and recorded["argv"][1:] == command[1:] and Path(recorded["argv"][0]).name == "pandoc-2.11.3.2" for command, recorded in zip(commands, run["calls"])))
            a.check(test_id + " pipeline exit and hash continuity", bool(run["calls"]) and all(c["exit_code"] == 0 and c["stderr"] == "" for c in run["calls"]) and run["calls"][0]["input_sha256"] == run["stdin_sha256"] and run["calls"][-1]["stdout_sha256"] == run["actual_stdout_sha256"] and all(left["stdout_sha256"] == right["input_sha256"] for left, right in zip(run["calls"], run["calls"][1:])))
            calls.extend(run["calls"])
        a.check("Pandoc12 process calls and8 fixture counts", len(calls) == receipt["process_invocations"] == counted["historical_project_binary_executions"] == 12 and len(fm) == receipt["test_count"] == counted["historical_fixture_runs"] == 8 and receipt["all_exit_zero"] is True and receipt["all_stdout_exact"] is True)
        a.check("Pandoc execution remains post-exposure researcher layer", "after exposure" in receipt["layer"] and "not preregistered" in receipt["layer"])
        for cid, name in [("PAN-C1", "parse-raw"), ("PAN-C2", "sloppypar")]:
            cr = criterion_map[cid + "-CR"]; packet = packet_map[cid]
            first, second = fm[name + "-1"], fm[name + "-2"]
            a.check(cid + " executed pair uses identical stdin", first["input"] == second["input"] and first["stdin_sha256"] == second["stdin_sha256"])
            for idx in (1, 2):
                f = fm[f"{name}-{idx}"]; run = rm[f"{name}-{idx}"]; frozen = packet["input_variants"][idx - 1]
                a.check(cid + f" run{idx} uses frozen logical input/expectation", f["input"] == frozen["input"] + "\n" and f["input_logical_sha256"] == frozen["input_sha256"] and f["expected_logical_sha256"] == frozen["expected_output_sha256"] and f["command"] == frozen["command"])
                a.check(cid + f" historical output{idx} equals receipt", jcell(cr[f"historical_execution_output{idx}"]) == run["actual_stdout"])
            a.check(cid + " executed equality matches criterion", (rm[name + "-1"]["actual_stdout"] == rm[name + "-2"]["actual_stdout"]) == tri(cr["expected_equal"]))
        empty = [rm[f"empty_paragraphs-{i}"]["actual_stdout"] for i in range(1, 5)]
        a.check("empty-paragraph counterexample needs both reader/writer flags", empty[0] == empty[1] == empty[2] and empty[3] != empty[0])
        binaries = {Path(call["argv"][0]) for call in calls}
        a.check("Pandoc calls share one named binary", len(binaries) == 1)
        available_binaries = [path for path in binaries if path.is_file()]
        for path in available_binaries:
            a.check("local historical Pandoc binary hash", sha256(path.read_bytes()) == receipt["binary_sha256"])
        a.details["historical_pandoc_execution"] = {"version": version, "source_pin": pin, "fixtures": len(fm), "process_calls": len(calls), "fixture_outputs_matched": sum(r["actual_stdout"] == r["expected_stdout"] for r in rm.values()), "runtime_binary_locally_rehashed": len(available_binaries), "scope": "Existing recorded researcher run verified; this validator does not execute Pandoc or assert public CI provenance."}

    a.section("historical Pandoc release fixture receipts", historical_pandoc_checks)

    def artifact_checks():
        transport = read_json("evidence/gdal3103-artifacts.json")
        receipt = read_json(transport["execution_receipt"])
        decoded = {}
        for entry in transport["files"]:
            content = base64.b64decode(entry["content"], validate=True)
            a.check("artifact " + entry["name"] + " bytes/hash", entry["encoding"] == "base64" and len(content) == entry["bytes"] and sha256(content) == entry["sha256"])
            decoded[entry["name"]] = content
        a.check("GDAL original input matches run receipt", sha256(decoded["byte-input.tif"]) == receipt["input_sha256"])
        images = {}
        for name, out in receipt["outputs"].items():
            data = decoded["recheck3103/" + name + ".tif"]; raster = unpack_tiff(data); images[name] = raster
            a.check("receipt " + name + " file and raster hashes", sha256(data) == out["sha256"] and sha256(raster["pixels"]) == out["pixel_array_sha256"] and raster["size"] == out["size"] and raster["geotransform"] == out["geotransform"])
        ref = unpack_tiff(decoded["warp-reference.tif"])
        near, bilin = images["nearest"]["pixels"], images["bilinear"]["pixels"]
        delta = [abs(x - y) for x, y in zip(near, bilin)]
        comps = receipt["comparisons"]
        a.check("receipt nearest/bilinear pixel differences", sum(x > 0 for x in delta) == comps["nearest_vs_bilinear_different_pixels"] and max(delta) == comps["nearest_vs_bilinear_max_absdiff"])
        a.check("receipt bilinear versus pinned reference", max(abs(x - y) for x, y in zip(bilin, ref["pixels"])) == comps["bilinear_vs_pinned_reference_max_absdiff"])
        a.check("receipt negative exact-array/file/geotransform comparisons", (images["pixels"]["pixels"] == images["percent"]["pixels"]) == comps["pixels_vs_percent_arrays_equal"] and (decoded["recheck3103/pixels.tif"] == decoded["recheck3103/percent.tif"]) == comps["pixels_vs_percent_files_equal"] and (images["pixels"]["geotransform"] == images["percent"]["geotransform"]) == comps["pixels_vs_percent_geotransforms_equal"])
        a.check("modern GDAL run explicitly separate", "3.10.3" in receipt["execution_version"] and "3.2.1" in receipt["pinned_expected_version"] and "NOT historical" in receipt["layer"])
        a.check("five receipt commands successful", len(receipt["commands"]) == counted["modern_gdal_execution_commands"] == 5 and all(r["exit_code"] == 0 and r["checked_utc"] for r in receipt["commands"]))
        a.details["artifact_validation"] = {"artifacts": len(decoded), "receipt_commands": len(receipt["commands"]), "raster_arrays_independently_decoded": len(images), "method": "stdlib uncompressed TIFF parser; no resampling or binary rerun", "limitation": "GDAL checksum algorithm not recomputed; full file/array hashes and recorded comparisons independently matched."}

    a.section("committed artifact transport and execution receipts", artifact_checks)

    def seal_and_scope_checks():
        seals = read_json("evidence/seals.json")["files"]
        a.check("exactly4 sealed pre files", len(seals) == 4)
        for seal in seals:
            path = OWNED + seal["file"]
            original = git("show", f'{seal["seal_commit"]}:{path}')
            current = (TASK / seal["file"]).read_bytes()
            blob = git("rev-parse", f'{seal["seal_commit"]}:{path}').decode().strip()
            a.check("seal " + seal["file"], original == current and blob == seal["seal_blob"] and seal["unchanged_since_seal"] is True)
        for p in packets:
            a.check(p["case_id"] + " packet source hash", sha256((TASK / p["source_ledger"]).read_bytes()) == p["source_ledger_sha256"])
        a.check("one allowed owned path", manifest["allowed_paths"] == [OWNED])
        a.check("fixed dependency", manifest["dependencies"] == [{"branch": "work/research-af-res-070", "commit": "1a92715786d444f57976082329470a24e2a291b6"}])
        changes = set()
        for cmd in [("diff", "--name-only", manifest["base_commit"], "HEAD"), ("diff", "--name-only"), ("diff", "--cached", "--name-only"), ("ls-files", "--others", "--exclude-standard")]:
            changes.update(git(*cmd).decode().splitlines())
        a.check("all changed paths owned", all(path.startswith(OWNED) for path in changes), sorted(path for path in changes if not path.startswith(OWNED)))
        a.details["git"] = {"head": git("rev-parse", "HEAD").decode().strip(), "base": manifest["base_commit"], "branch": git("branch", "--show-current").decode().strip(), "changed_paths": len(changes), "seal_files": 4, "remote_freshness": "not checked by this validator; workbench.session check --fetch is separate"}

    a.section("seal bytes and owned scope", seal_and_scope_checks)

    def all_json_and_optional_reports():
        paths = sorted(set(git("ls-files", "-c", "-o", "--exclude-standard", "--", OWNED).decode().splitlines()))
        json_count = 0
        markdown_tables = 0
        for rel in paths:
            path = ROOT / rel
            if not path.is_file():
                continue
            if path.suffix in {".json", ".jsonl"}:
                try:
                    if path.suffix == ".json":
                        json.loads(path.read_text(encoding="utf-8"))
                    else:
                        for line in path.read_text(encoding="utf-8").splitlines():
                            if line.strip():
                                json.loads(line)
                    json_count += 1
                except (ValueError, UnicodeError) as exc:
                    a.check("JSON parses " + rel, False, str(exc))
        for name in ("RESULT.md", "SELF_CHECK.md"):
            path = TASK / name
            if not path.exists():
                a.warnings.append(name + " not yet present; optional report check deferred, not research completion.")
                continue
            text = path.read_text()
            a.check(name + " preserves research PARTIAL", "PARTIAL" in text)
            active = False; width = None
            for line_no, line in enumerate(text.splitlines(), 1):
                if line.lstrip().startswith("```"):
                    active = not active; width = None; continue
                if active:
                    continue
                if line.strip().startswith("|") and line.strip().endswith("|"):
                    cells = re.split(r"(?<!\\)\|", line.strip())[1:-1]
                    if width is None:
                        width = len(cells); markdown_tables += 1
                    a.check(f"{name}:{line_no} table columns", len(cells) == width, {"expected": width, "actual": len(cells)})
                else:
                    width = None
            if name == "SELF_CHECK.md":
                a.check("SELF_CHECK Q1-Q8 present", all(f"Q{i}" in text for i in range(1, 9)))
        accept = TASK / "evidence/acceptance-evidence.json"
        if accept.exists():
            data = json.loads(accept.read_text())
            serialized = json.dumps(data, ensure_ascii=False)
            a.check("acceptance preserves PARTIAL", "PARTIAL" in serialized)
            for container_key in ("counts", "ledger_counts", "measured_counts"):
                section = data.get(container_key)
                if isinstance(section, dict):
                    for k, v in section.items():
                        if k in counted and isinstance(v, (int, dict)):
                            a.check("acceptance count " + k, v == counted[k])
        else:
            a.warnings.append("acceptance-evidence.json not yet present; its counts must be checked on final rerun.")
        a.details["parsed_artifacts"] = {"json_jsonl_files": json_count, "optional_markdown_tables": markdown_tables, "ignored_cache_files": "not read or counted"}

    a.section("all nonignored JSON and optional reports", all_json_and_optional_reports)
    ended = dt.datetime.now(dt.timezone.utc)
    exit_code = 0 if not a.errors else 1
    report = {
        "validator_author": "Pandoc model stream author; not independent human",
        "validator_actor": args.actor,
        "command": shlex.join(["python", "-B", OWNED + "tools/validate.py", *sys.argv[1:]]),
        "argv": ["python", "-B", OWNED + "tools/validate.py", *sys.argv[1:]],
        "cwd": str(ROOT), "started_utc": started.isoformat(), "ended_utc": ended.isoformat(),
        "exit_code": exit_code, "structural_status": "PASS" if exit_code == 0 else "FAIL", "research_status": "PARTIAL",
        "research_gaps": ["Natural cases still lack independent same-version outputs for both selected field values; strict question-effect denominator remains zero despite recovery of all8 original bodies", "Pandoc controls were expectation-informed; PAN-C1 purpose-to-configuration mapping and PAN-N2 nonexclusive alternatives limit causal interpretation", "Some judgments require reading beyond the shared section budget; extra reading is a separate layer", "GDAL3.2.1 was not executed; GDAL3.10.3 receipts remain separate from historical expectations and mixed-version natural reports"],
        "unmeasured_scope": ["No actual A/B/C policy experiment or measured user response probability/human time; these are recorded scope limits, not required new-human experiments.", "Model coauthor reviews are not independent human adjudication."],
        "check_count": len(a.checks), "error_count": len(a.errors), "errors": a.errors, "warnings": a.warnings,
        "details": a.details, "checks": a.checks,
    }
    output = TASK / "evidence/validation.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("structural_status", "research_status", "exit_code", "check_count", "error_count", "errors", "warnings")}, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
