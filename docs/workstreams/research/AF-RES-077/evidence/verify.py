#!/usr/bin/env python3
"""Read-only AF-RES-077 integrity verifier. No network, target runs, or writes.

Mechanical consistency is not research acceptance or native application success.
--phase draft checks available data and reports missing final deliverables as skips.
--phase final requires all requested deliverables except the last-only HANDOFF.md.
Historical mistakes inside sealed inputs remain sealed; ERRATA is interpretation.
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys

TASK = Path(__file__).resolve().parents[1]
REPO = TASK.parents[3]
PREFIX = TASK.relative_to(REPO).as_posix() + "/"
BASE = "d73c8ec85d375f37451795b575dd7d0e6b2f3594"
RECRUIT = "b3fee8986841c3dbda82a4a3093d2316c915e9c5"
PACKETS = "9518c3dccbd21cda72cec715afe47eebd4dba543"
SEALS = {"A": "7c1df93b11e06ca8b7f44ac5b7ff996879aebd09",
         "B": "7bc2d1f84c04b47711d72e7c110b8f927d97f4ad"}
REGISTRY = "924a030d593501c4736d8f84f20335be86d868f4"
CHECKPOINT = "2f7e07542b4a59839556e00c9e266179150b21a3"
PROJECTS = ("SC", "MS", "SG")
CASE_IDS = {f"{b}-{k}" for b in PROJECTS for k in ("N", "E", "X")}
AUX_IDS = {"SC-E", "SC-X", "SG-N", "SG-E", "SG-X"}
FAMILIES = {"SHOTCUT-PROXY-GUIDE": "SC-CODEBASE",
            "MUSESCORE3-HANDBOOK": "MS-CODEBASE",
            "SIGIL-USER-GUIDE": "SG-CODEBASE"}
CORE = ("SCOPE.md", "FRAME.csv", "BRIEFS.jsonl", "VIEWS.csv", "SOURCES.jsonl",
        "CASEBOOK.md", "TESTS.csv", "COSTS.csv", "manifest.json")
FINAL = ("RESULT.md", "SELF_CHECK.md", "evidence/acceptance-evidence.json")
SCHEMA_SOURCE = {"id", "author_lineage", "purpose", "url", "version_or_sha", "utc",
                 "section_or_symbol", "confirmed", "unverified", "access_failures",
                 "local_receipt", "independent_work_id", "conservative_lineage_id",
                 "core20_eligible", "counted_work_units", "named_work_units"}

class Audit:
    def __init__(self, phase):
        self.phase = phase
        self.errors = []
        self.warnings = []
        self.skips = []
        self.counts = {}
        self.checks = collections.Counter()
        self.section = "setup"
        self.cache = {}
        self.data = {}
        self.hash_checks = set()

    def check(self, label, condition, detail=None):
        self.checks[self.section] += 1
        if not condition:
            error = {"section": self.section, "check": label}
            if detail is not None:
                error["detail"] = detail
            self.errors.append(error)
        return bool(condition)

    def run(self, name, method):
        self.section = name
        try:
            method()
        except Exception as exc:
            self.check("section completed without an unhandled data error", False,
                       f"{type(exc).__name__}: {exc}")

    def local(self, name):
        p = (TASK / name).resolve()
        if not p.is_relative_to(TASK):
            raise ValueError(f"path outside owned directory: {name}")
        return p

    def raw(self, name):
        name = str(name)
        if name not in self.cache:
            self.cache[name] = self.local(name).read_bytes()
        return self.cache[name]

    def text(self, name):
        return self.raw(name).decode("utf-8")

    def json(self, name):
        return json.loads(self.text(name))

    def csv(self, name):
        reader = csv.DictReader(io.StringIO(self.text(name), newline=""))
        if not self.check(name + " unique CSV headers",
                          reader.fieldnames is not None and len(set(reader.fieldnames)) == len(reader.fieldnames)):
            return []
        rows = list(reader)
        self.check(name + " rectangular rows", all(None not in r and None not in r.values() for r in rows))
        return rows

    def jsonl(self, name):
        rows = []
        for i, line in enumerate(self.text(name).splitlines(), 1):
            if not line.strip():
                self.check(f"{name}:{i} nonblank JSONL record", False)
                continue
            obj = json.loads(line)
            self.check(f"{name}:{i} object", isinstance(obj, dict))
            rows.append(obj)
        return rows

    def sha(self, name):
        return hashlib.sha256(self.raw(name)).hexdigest()

    def hashref(self, name, expected, context):
        key = (name, expected)
        if key not in self.hash_checks:
            self.hash_checks.add(key)
            try:
                self.check(context + " retained hash", self.sha(name) == expected, name)
            except (OSError, ValueError) as exc:
                self.check(context + " retained path", False, f"{name}: {exc}")

    def git(self, *args, allow_error=False):
        env = os.environ.copy()
        env["GIT_OPTIONAL_LOCKS"] = "0"
        env["GIT_NO_LAZY_FETCH"] = "1"
        cp = subprocess.run(["git", "-c", "core.fsmonitor=false", *args],
                            cwd=REPO, env=env, capture_output=True, check=False)
        if cp.returncode and not allow_error:
            raise RuntimeError(f"git {' '.join(args)}: {cp.stderr.decode(errors='replace').strip()}")
        return cp

    def frozen(self, name, commit):
        content = self.git("show", f"{commit}:{PREFIX}{name}").stdout
        self.check(f"{name} unchanged from original recorded seal",
                   self.raw(name) == content, {"seal": commit})

    def prerequisites(self):
        for name in CORE:
            self.check("required core " + name, self.local(name).is_file())
        for name in FINAL:
            if self.phase == "final":
                self.check("required final " + name, self.local(name).is_file())
            elif not self.local(name).is_file():
                self.skips.append({"path": name, "reason": "draft phase; final deliverable not present"})
        self.counts["head"] = self.git("rev-parse", "HEAD").stdout.decode().strip()
        self.counts["branch"] = self.git("branch", "--show-current").stdout.decode().strip()
        self.check("correct named branch or detached verification checkout",
                   self.counts["branch"] in ("work/research-af-res-077", ""))
        if not self.counts["branch"]:
            self.warnings.append("Detached checkout: source identity is checked by seal ancestry and owned diff; this does not assert a remote branch-head match.")
        manifest = self.json("manifest.json")
        self.check("manifest task", manifest.get("task_id") == "af-res-077")
        self.check("manifest base", manifest.get("base_commit") == BASE)
        self.check("manifest sole owned path", manifest.get("allowed_paths") == [PREFIX])
        self.check("manifest exact sole dependency", manifest.get("dependencies") == [
            {"branch": "work/research-af-res-073", "commit": "28dfa4d14ce33f0f98c823f83c20347d60c0e64e"}])

    def seals(self):
        chain = [BASE, RECRUIT, PACKETS, SEALS["A"], SEALS["B"], REGISTRY, CHECKPOINT,
                 self.counts["head"]]
        for older, newer in zip(chain, chain[1:]):
            cp = self.git("merge-base", "--is-ancestor", older, newer, allow_error=True)
            self.check("seal ancestry", cp.returncode == 0, {"older": older, "newer": newer})
        self.frozen("BRIEFS.jsonl", RECRUIT)
        # FRAME is a later exact transcription; candidate snapshots were sealed before views.
        self.frozen("FRAME.csv", REGISTRY)
        for folder in ("shotcut", "musescore", "sigil"):
            self.frozen(f"recruitment/{folder}/candidates.json", RECRUIT)
        for b in PROJECTS:
            self.frozen(f"packets/{b}-common.json", PACKETS)
            for v in ("A", "B"):
                self.frozen(f"packets/{b}-{v}.json", PACKETS)
                self.frozen(f"readers/{b}-{v}.json", SEALS[v])

    def sources(self):
        rows = self.jsonl("SOURCES.jsonl")
        self.data["sources"] = {r["id"]: r for r in rows}
        self.check("unique source IDs", len(self.data["sources"]) == len(rows))
        named, families = set(), set()
        ncontrib, ccontrib = collections.Counter(), collections.Counter()
        unavailable_raw = 0
        for r in rows:
            sid = r["id"]
            self.check(sid + " source schema", SCHEMA_SOURCE <= r.keys(),
                       sorted(SCHEMA_SOURCE - r.keys()))
            work, family = r["independent_work_id"], r["conservative_lineage_id"]
            self.check(sid + " consistent conservative lineage", family == FAMILIES.get(work, work))
            self.check(sid + " boolean eligibility", type(r["core20_eligible"]) is bool)
            self.check(sid + " contribution domain",
                       r["named_work_units"] in (0, 1) and r["counted_work_units"] in (0, 1))
            for field in ("confirmed", "unverified", "access_failures", "local_receipt"):
                self.check(sid + " list " + field, isinstance(r[field], list))
            url = r["url"]
            url_ok = (isinstance(url, str) and bool(url)) or (
                isinstance(url, list) and bool(url) and all(isinstance(x, str) and x for x in url))
            local_only = r["source_kind"] in {
                "local_environment_report", "local_environment_observation", "environment_command_failure"}
            self.check(sid + " source URL or declared local-only record",
                       (url_ok or (url is None and local_only and not r["core20_eligible"]))
                       and bool(r["section_or_symbol"]))
            self.check(sid + " time record", bool(r["utc"]))
            for ref in r["local_receipt"]:
                path = ref.split("#", 1)[0]
                self.check(sid + " local receipt exists", self.local(path).is_file(), path)
            if r["core20_eligible"]:
                named.add(work)
                families.add(family)
            else:
                self.check(sid + " ineligible work contributes zero",
                           r["named_work_units"] == r["counted_work_units"] == 0)
            ncontrib[work] += r["named_work_units"]
            ccontrib[family] += r["counted_work_units"]
            if r.get("raw_hash_recomputable_from_retained_files") is False:
                unavailable_raw += 1
        self.check("eligible named works24", len(named) == 24, sorted(named))
        self.check("eligible conservative lineages21", len(families) == 21, sorted(families))
        self.check("one named unit per eligible work",
                   all(ncontrib[x] == 1 for x in named) and sum(ncontrib.values()) == 24)
        self.check("one conservative unit per eligible lineage",
                   all(ccontrib[x] == 1 for x in families) and sum(ccontrib.values()) == 21)
        self.counts.update(source_records=len(rows), named_original_works=len(named),
                           conservative_original_lineages=len(families),
                           unavailable_fulltext_raw_hashes_not_recomputed=unavailable_raw)

    def frame_briefs(self):
        rows = self.csv("FRAME.csv")
        self.check("FRAME thirty rows", len(rows) == 30)
        self.check("FRAME unique candidate IDs", len({r["candidate_id"] for r in rows}) == len(rows))
        self.check("FRAME exactly three groups", {r["project"] for r in rows} == set(PROJECTS))
        folders = dict(zip(PROJECTS, ("shotcut", "musescore", "sigil")))
        for b in PROJECTS:
            group = [r for r in rows if r["project"] == b]
            self.check(b + " first ten ranks", [int(r["union_rank"]) for r in group] == list(range(1, 11)))
            ordering = [(parse_date(r["created_at_utc"]), int(r["number"])) for r in group]
            self.check(b + " chronological created/number order", ordering == sorted(ordering))
            candidate_data = self.json(f"recruitment/{folders[b]}/candidates.json")
            candidates = candidate_data if isinstance(candidate_data, list) else candidate_data["candidates"]
            self.check(b + " matches pre-view recruitment candidate order",
                       [int(r["number"]) for r in group] == [int(r["number"]) for r in candidates[:10]])
            for r in group:
                self.check(r["candidate_id"] + " source join", r["candidate_id"] in self.data["sources"])
                self.check(r["candidate_id"] + " in date window",
                           2019 <= parse_date(r["created_at_utc"]).year <= 2025)
                self.check(r["candidate_id"] + " primary remains vacant",
                           r["primary_qualifies"].lower() == "false" and r["primary_slot_status"] == "VACANT")
                members = json.loads(r["query_rank_memberships"])
                self.check(r["candidate_id"] + " query membership exists", len(members) >= 1)
                for m in members:
                    q = self.data["sources"].get(m["query_source_id"], {})
                    order = q.get("original_order", [])
                    rank = int(m["original_rank"])
                    self.check(r["candidate_id"] + " canonical original rank",
                               1 <= rank <= len(order) and int(order[rank - 1]) == int(r["number"]))
                self.check(r["candidate_id"] + " direct receipt", self.local(r["direct_read_receipt"]).is_file())
                json.loads(r["version_evidence"])
                json.loads(r["canonical_query_receipts"])
        briefs = self.jsonl("BRIEFS.jsonl")
        self.data["briefs"] = {r["brief_id"]: r for r in briefs}
        self.check("three unique briefs", len(briefs) == len(self.data["briefs"]) == 3)
        all_cases = []
        for b in PROJECTS:
            br = self.data["briefs"][b]
            common = self.json(f"packets/{b}-common.json")
            self.check(b + " common equals sealed brief", br == common)
            self.check(b + " two conditions", len(br["conditions"]) == 2)
            self.check(b + " unique condition IDs", len({x["id"] for x in br["conditions"]}) == 2)
            self.check(b + " three cases", len(br["cases"]) == 3)
            self.check(b + " case kinds", {x["kind"] for x in br["cases"]} == {"normal", "boundary", "negative"})
            all_cases.extend(x["id"] for x in br["cases"])
        self.check("nine fixed case IDs", len(all_cases) == 9 and set(all_cases) == CASE_IDS)
        self.counts.update(frame_rows=len(rows), briefs=len(briefs), frozen_cases=len(all_cases))

    def views(self):
        rows = self.csv("VIEWS.csv")
        views = {(r["brief_id"], r["view"]): r for r in rows}
        self.data["views"] = views
        self.data["readers"] = {}
        self.data["predictions"] = {}
        self.check("six views", len(rows) == len(views) == 6)
        candidates_total, selected_total, predictions_total = 0, 0, 0
        exposed = collections.Counter()
        for b in PROJECTS:
            for v in ("A", "B"):
                row = views[b, v]
                p = self.json(f"packets/{b}-{v}.json")
                reader = self.json(f"readers/{b}-{v}.json")
                self.data["readers"][b, v] = reader
                self.check(b+v + " packet single work", isinstance(p["work_id"], str) and bool(p["work_id"]))
                self.check(b+v + " source registry work join",
                           any(r["independent_work_id"] == p["work_id"] for r in self.data["sources"].values()))
                self.check(b+v + " at most two sections", 1 <= len(p["sections"]) <= 2)
                self.check(b+v + " excerpt cap", len(p["excerpt"]) <= 2000)
                self.check(b+v + " excerpt accounting",
                           len(p["excerpt"]) == int(row["actual_excerpt_characters"]) == int(p["display_characters"]))
                self.check(b+v + " excerpt hash", hashlib.sha256(p["excerpt"].encode()).hexdigest() == p["excerpt_sha256"])
                self.check(b+v + " full packet exposure count",
                           len(self.text(f"packets/{b}-{v}.json")) == int(row["actual_packet_characters"]))
                self.check(b+v + " common exposure count",
                           len(self.text(f"packets/{b}-common.json")) == int(row["common_characters"]))
                self.check(b+v + " source identity and sections",
                           p["work_id"] == row["source_work_id"] and p["sections"] == json.loads(row["source_sections"]))
                self.check(b+v + " source URLs", p["urls"] == json.loads(row["source_urls"]))
                self.check(b+v + " correct seal references",
                           row["packet_seal_sha"] == PACKETS and row["choice_seal_sha"] == SEALS[v])
                self.hashref(f"packets/{b}-{v}.json", row["packet_sha256"], b+v)
                self.hashref(f"packets/{b}-common.json", row["common_sha256"], b+v)
                self.hashref(f"readers/{b}-{v}.json", row["reader_sha256"], b+v)
                self.check(b+v + " packet common hash", p["common_sha256"] == row["common_sha256"])
                self.check(b+v + " no additional source opens",
                           len(reader["extra_source_opens"]) == int(row["additional_reader_source_opens"]) == 0)
                cids = [x["id"] for x in reader["candidates"]]
                chosen = reader["chosen_candidate"]["id"]
                self.check(b+v + " at least two unique candidates", len(cids) >= 2 and len(cids) == len(set(cids)))
                self.check(b+v + " chosen candidate", chosen in cids and chosen == row["selected_id"])
                self.check(b+v + " view candidate join", cids == json.loads(row["candidate_ids"]))
                self.check(b+v + " choice timestamp", reader["completed_utc"] == row["selected_utc"])
                self.check(b+v + " causal denominator remains zero",
                           row["causal_effect_eligible"].lower() == "false"
                           and int(row["independent_effect_denominator_contribution"]) == 0)
                for case in self.data["briefs"][b]["cases"]:
                    outputs, original = prediction(reader, case["id"])
                    self.check(b+v+case["id"] + " predictions cover every candidate",
                               set(outputs) == set(cids) and all(isinstance(s, str) and s for s in outputs.values()))
                    self.data["predictions"][b, v, case["id"]] = (outputs, original)
                    selected_total += int(chosen in outputs)
                    predictions_total += len(outputs)
                candidates_total += len(cids)
                exposed[v] += len(p["excerpt"])
            self.check(b + " identical A/B common hash",
                       views[b, "A"]["common_sha256"] == views[b, "B"]["common_sha256"])
            self.check(b + " A choice before B", parse_date(views[b, "A"]["selected_utc"]) < parse_date(views[b, "B"]["selected_utc"]))
        self.check("thirteen candidate definitions", candidates_total == 13)
        self.check("eighteen chosen case predictions", selected_total == 18)
        self.check("thirtynine all-candidate case predictions", predictions_total == 39)
        self.counts.update(views=len(rows), candidate_definitions=candidates_total,
                           chosen_predictions=selected_total, candidate_case_predictions=predictions_total,
                           source_excerpt_characters=dict(exposed))

    def reference_tree(self, obj, context):
        if isinstance(obj, dict):
            if "path" in obj and "sha256" in obj:
                self.hashref(obj["path"], obj["sha256"], context)
            if obj.get("source_id"):
                registry = obj.get("source_id_registry", "SOURCES.jsonl")
                if registry == "SOURCES.jsonl":
                    ids = self.data["sources"]
                else:
                    name, _, pointer = registry.partition("#")
                    collection = json_pointer(self.json(name), pointer) if pointer else self.json(name)
                    ids = {r.get("id", r.get("source_id")): r for r in collection}
                self.check(context + " explicit source ID join", obj["source_id"] in ids,
                           {"source_id": obj["source_id"], "registry": registry})
            for val in obj.values():
                self.reference_tree(val, context)
        elif isinstance(obj, list):
            for val in obj:
                self.reference_tree(val, context)

    def tests(self):
        rows = self.csv("TESTS.csv")
        self.check("nine unique TESTS IDs", len(rows) == 9 and {r["test_id"] for r in rows} == CASE_IDS)
        totals = collections.Counter()
        expected_contrib = {"frozen_case_denominator_contribution": 9, "primary_sample_contribution": 0,
                            "target_executed_contribution": 0, "original_execution_receipt_contribution": 0,
                            "auxiliary_predicate_case_contribution": 5, "auxiliary_complete_case_contribution": 0,
                            "causal_effect_denominator_contribution": 0}
        for r in rows:
            tid, b = r["test_id"], r["brief_id"]
            br = self.data["briefs"][b]
            case = next(x for x in br["cases"] if x["id"] == tid)
            self.check(tid + " correct project/tag/commit",
                       (r["target_project"], r["target_tag"], r["target_commit"]) == (br["project"], br["tag"], br["sha"]))
            self.check(tid + " request source join", r["request_source_id"] in self.data["sources"])
            self.check(tid + " frozen input pointer",
                       json_pointer(self.json(r["input_packet"]), r["input_case_pointer"]) == case)
            self.hashref(r["input_packet"], r["input_sha256"], tid)
            self.check(tid + " input seal", r["input_seal_commit"] == PACKETS)
            self.check(tid + " kind", r["case_kind"] == case["kind"])
            decoded = {k: json.loads(val) for k, val in r.items() if k.endswith("_json")}
            self.check(tid + " original input fields",
                       decoded["initial_state_json"] == case["initial"]
                       and decoded["actions_json"] == case["actions"]
                       and decoded["observable_checkpoints_json"] == case["observe"]
                       and r["frozen_condition"] == case["condition"])
            for v in ("A", "B"):
                k = v.lower()
                reader = self.data["readers"][b, v]
                outputs, original = self.data["predictions"][b, v, tid]
                chosen = reader["chosen_candidate"]["id"]
                self.check(tid+v + " unchanged prediction text",
                           r[k+"_selected_candidate_id"] == chosen
                           and r[k+"_selected_prediction"] == outputs[chosen]
                           and decoded[k+"_competing_candidate_outputs_json"] == outputs
                           and decoded[k+"_prediction_context_json"] == original)
                self.check(tid+v + " candidate IDs",
                           decoded[k+"_candidate_ids_json"] == [x["id"] for x in reader["candidates"]])
            self.check(tid + " native not-run flags",
                       r["target_not_run"].lower() == "true" and r["target_execution_status"] == "NOT_RUN"
                       and r["target_pass_status"] == r["target_fail_status"] == "UNKNOWN_NOT_RUN")
            original_receipt = decoded["original_execution_receipt_json"]
            self.check(tid + " no retrieved native execution receipt",
                       original_receipt["status"] == "NOT_RETRIEVED"
                       and original_receipt["retrieved_execution_receipts"] == 0)
            aux = decoded["researcher_auxiliary_run_json"]
            self.check(tid + " auxiliary scope matches ID",
                       int(r["auxiliary_predicate_case_contribution"]) == int(tid in AUX_IDS)
                       == aux["predicate_case_contribution"])
            for field in expected_contrib:
                n = int(r[field])
                self.check(tid + " contribution domain " + field, n in (0, 1))
                totals[field] += n
            for field, obj in decoded.items():
                self.reference_tree(obj, tid + " " + field)
        for field, expected in expected_contrib.items():
            self.check("TESTS total " + field, totals[field] == expected, totals[field])
        self.counts.update(target_executed=totals["target_executed_contribution"],
                           original_execution_receipts=totals["original_execution_receipt_contribution"],
                           auxiliary_predicate_cases=totals["auxiliary_predicate_case_contribution"],
                           complete_auxiliary_workflows=totals["auxiliary_complete_case_contribution"],
                           causal_effect_denominator=totals["causal_effect_denominator_contribution"])

    def auxiliary(self):
        receipt = self.json("evidence/auxiliary/observed-run-20261123/receipt.json")
        out = self.json("evidence/auxiliary/observed-run-20261123/stdout.json")
        self.check("captured worker exit0", receipt["worker_exit_code"] == 0)
        self.check("captured worker before/after inputs",
                   receipt["input_hashes_before"] == receipt["input_hashes_after"]
                   and receipt["all_input_bytes_unchanged_during_run"] is True)
        self.check("captured chronology", parse_date(receipt["started_utc"]) <= parse_date(receipt["finished_utc"]))
        self.check("native run never implied",
                   receipt["target_gui_runtime_tests_executed"] == out["target_gui_runtime_tests_executed"] == 0
                   and receipt["sealed_scores_updated"] is False and out["sealed_A_B_pass_counts_changed"] is False)
        for r in receipt["input_hashes_after"] + receipt["output_files"]:
            self.hashref(r["path"], r["sha256"], "captured auxiliary")
            self.check("captured auxiliary size", len(self.raw(r["path"])) == r["size_bytes"], r["path"])
        self.check("five auxiliary case predicates", set(out["SG"]) | {"SC-E", "SC-X"} == AUX_IDS)
        self.check("auxiliary actual SHA descriptor", out["input_descriptor"]["sha256"] == self.sha(out["input_descriptor"]["path"]))
        self.counts["auxiliary_receipt_exit"] = receipt["worker_exit_code"]
        self.counts["auxiliary_reexecuted_by_this_verifier"] = False

    def costs(self):
        rows = self.csv("COSTS.csv")
        indexed = {r["id"]: r for r in rows}
        self.check("unique cost IDs", len(indexed) == len(rows))
        total = 0
        gaps = 0
        resume_fields = (
            "resume_read_operations", "resume_github_read_operations", "resume_web_open_operations",
            "resume_web_find_operations", "resume_access_failure_operations", "resume_no_match_find_operations",
            "resume_additional_sealed_reader_exposures", "resume_native_target_runs")
        resume_totals = collections.Counter()
        resume_by_actor = {}
        for r in rows:
            rid = r["id"]
            n = int(r["count"]) if r["count"] else None
            inc = int(r["incremental_request_attempts_to_existing_root"] or 0)
            self.check(rid + " nonnegative request increment", inc >= 0 and (n is None or n >= 0))
            matched = r["matched_root_cost_id"]
            if matched:
                self.check(rid + " aggregation parent exists", matched in indexed and matched != rid)
                self.check(rid + " matched/subset not double-counted", inc == 0)
            role = r["aggregation_role"].lower()
            if "nonadditive" in role or "nonexternal" in role or "local or unknown" in role:
                self.check(rid + " nonadditive/local increment zero", inc == 0)
            if inc:
                self.check(rid + " increments match reported count", n == inc)
            # A mixed-operation unit label is not a count of finds. Only the
            # explicit operation columns define this separate resume ledger.
            if r.get("resume_read_operations", "") != "":
                operations = {field: int(r[field]) for field in resume_fields}
                self.check(rid + " explicit resume counts nonnegative",
                           all(value >= 0 for value in operations.values()))
                self.check(rid + " resume total equals GitHub/open/find breakdown",
                           operations["resume_read_operations"] == n ==
                           operations["resume_github_read_operations"] +
                           operations["resume_web_open_operations"] +
                           operations["resume_web_find_operations"])
                self.check(rid + " failure/no-match subsets bounded",
                           operations["resume_access_failure_operations"] <= n
                           and operations["resume_no_match_find_operations"] <= operations["resume_web_find_operations"])
                self.check(rid + " resume operations separate from historical requests", inc == 0)
                self.check(rid + " no new sealed exposure or target run",
                           operations["resume_additional_sealed_reader_exposures"] ==
                           operations["resume_native_target_runs"] == 0)
                self.check(rid + " resume cost remains incomplete", r.get("resume_cost_complete", "").lower() == "false")
                self.check(rid + " unique resume actor/project", r["project"] not in resume_by_actor)
                resume_by_actor[r["project"]] = operations["resume_read_operations"]
                resume_totals.update(operations)
            total += inc
            if "gap" in role or "partially logged" in r["count_status"].lower():
                gaps += inc
            for ref in r["receipt"].split(";"):
                if ref.strip():
                    local = ref.strip().split("#", 1)[0]
                    path = self.local(local)
                    self.check(rid + " cost receipt exists",
                               path.is_file() or (path.is_dir() and any(path.iterdir())), local)
        self.check("Shotcut existing eight requests not duplicated",
                   indexed["POST-SC"]["count"] == indexed["POST-SC-MATCHED"]["count"] == "8"
                   and indexed["POST-SC-MATCHED"]["matched_root_cost_id"] == "POST-SC"
                   and int(indexed["POST-SC-MATCHED"]["incremental_request_attempts_to_existing_root"]) == 0)
        self.check("MuseScore recorded total equals its two breakdowns",
                   int(indexed["POST-MS-TOTAL"]["count"]) ==
                   int(indexed["POST-MS-CONNECTOR-COMPONENT"]["count"]) + int(indexed["POST-MS-PUBLIC-COMPONENT"]["count"]))
        for b in PROJECTS:
            for v in ("A", "B"):
                cr, vr = indexed[f"READ-{b}-{v}"], self.data["views"][b, v]
                self.check(b+v + " cost/exposure join",
                           cr["count"] == "2" and cr["excerpt_characters"] == vr["actual_excerpt_characters"]
                           and cr["packet_characters"] == vr["actual_packet_characters"]
                           and cr["common_characters"] == vr["common_characters"])
        self.counts.update(cost_rows=len(rows),
                           reported_external_request_components_including_partially_logged_web=total,
                           recorded_external_request_components_excluding_partially_logged_web=total-gaps)
        if resume_by_actor:
            resume_sources = [r for r in self.data["sources"].values() if r.get("phase") == "resume_postseal_review"]
            source_totals = collections.Counter()
            source_by_actor = collections.Counter()
            operation_fields = {"github_read": "resume_github_read_operations",
                                "web_open": "resume_web_open_operations",
                                "web_find": "resume_web_find_operations"}
            local_count = 0
            for r in resume_sources:
                sid = r["id"]
                contribution = r["resume_read_operation_contribution"]
                self.check(sid + " resume operation contribution domain", contribution in (0, 1))
                operation = r["operation"]
                self.check(sid + " explicit recognized resume operation",
                           operation in {*operation_fields, "retained_original_reread"})
                if operation == "retained_original_reread":
                    local_count += 1
                    self.check(sid + " retained reread is not external operation", contribution == 0)
                else:
                    self.check(sid + " recorded tool operation contributes once", contribution == 1)
                    source_totals[operation_fields[operation]] += contribution
                    source_by_actor[r["project"]] += contribution
                source_totals["resume_read_operations"] += contribution
                source_totals["resume_access_failure_operations"] += contribution * int(bool(r["access_failures"]))
                source_totals["resume_no_match_find_operations"] += contribution * int(r.get("operation_outcome") == "no_matching_text")
                if r.get("operation_outcome") == "no_matching_text":
                    self.check(sid + " no-match is a find result", operation == "web_find")
                source_totals["resume_additional_sealed_reader_exposures"] += r["additional_sealed_reader_exposure"]
                source_totals["resume_native_target_runs"] += int(r["target_runtime_observed"])
            for field in resume_fields:
                self.check("resume COSTS/SOURCES " + field, resume_totals[field] == source_totals[field],
                           {"costs": resume_totals[field], "sources": source_totals[field]})
                self.counts[field] = resume_totals[field]
            self.check("resume COSTS/SOURCES actor breakdown", resume_by_actor == dict(source_by_actor),
                       {"costs": resume_by_actor, "sources": dict(source_by_actor)})
            self.counts.update(resume_source_records=len(resume_sources),
                               pre_resume_source_records=len(self.data["sources"]) - len(resume_sources),
                               resume_local_original_reread_records=local_count,
                               resume_read_operations_by_actor=resume_by_actor,
                               resume_new_named_work_units=sum(r["named_work_units"] for r in resume_sources),
                               resume_new_conservative_lineage_units=sum(r["counted_work_units"] for r in resume_sources))
            self.check("resume no new independently counted works",
                       self.counts["resume_new_named_work_units"] == self.counts["resume_new_conservative_lineage_units"] == 0)
        if self.local("evidence/COUNTS.json").is_file():
            recorded = self.json("evidence/COUNTS.json")
            for field in ("source_records", "named_original_works", "conservative_original_lineages", "frame_rows",
                          "frozen_cases", "views", "chosen_predictions", "candidate_case_predictions", "target_executed",
                          "auxiliary_predicate_cases", "complete_auxiliary_workflows", "causal_effect_denominator",
                          "source_excerpt_characters", "reported_external_request_components_including_partially_logged_web",
                          "recorded_external_request_components_excluding_partially_logged_web"):
                if field in recorded:
                    self.check("COUNTS " + field, recorded[field] == self.counts[field],
                               {"recorded": recorded[field], "computed": self.counts[field]})
            self.check("counts retain partial/incomplete cost", recorded.get("status") == "PARTIAL" and recorded.get("global_cost_complete") is False)
            for field in (*resume_fields, "resume_source_records", "pre_resume_source_records",
                          "resume_local_original_reread_records", "resume_read_operations_by_actor",
                          "resume_new_named_work_units", "resume_new_conservative_lineage_units"):
                if field in recorded:
                    self.check("COUNTS " + field, recorded[field] == self.counts.get(field),
                               {"recorded": recorded[field], "computed": self.counts.get(field)})

    def final_text(self):
        if self.local("RESULT.md").is_file():
            text = self.text("RESULT.md")
            headings = list(re.finditer(r"(?m)^#{1,6}\s+(.+)$", text))
            tables = []
            for n in (1, 2, 3):
                hits = [h for h in headings if re.search(rf"표\s*{n}(?!\d)", h[1])]
                self.check(f"RESULT table{n} heading exactly once", len(hits) == 1)
                if hits:
                    tables.append(hits[0].start())
                    end = next((h.start() for h in headings if h.start() > hits[0].start()), len(text))
                    self.check(f"RESULT table{n} Markdown rows", bool(re.search(r"(?m)^\|.*\|\s*$", text[hits[0].end():end])))
            self.check("RESULT three tables ordered first", len(tables) == 3 and tables == sorted(tables))
            qhead = [h for h in headings if re.match(r"Q[1-8](?:\b|[·:：.])", h[1])]
            self.check("RESULT Q1 through Q8 headings", [re.match(r"Q([1-8])", h[1])[1] for h in qhead] == list("12345678"))
            if tables and qhead:
                self.check("RESULT tables precede question answers", max(tables) < qhead[0].start())
            weak = [h for h in headings if "약점" in h[1] and ("불일치" in h[1] or "3" in h[1])]
            self.check("RESULT final weakness block", len(weak) == 1)
            if weak:
                tail = text[weak[0].end():]
                numbered = re.findall(r"(?m)^\s*([123])\.\s+\S", tail)
                table_rows = [line for line in tail.splitlines() if re.match(r"^\|\s*[123]\s*\|", line)]
                subheads = re.findall(r"(?m)^#{3,6}\s*(?:[123][.)·]?\s*)?.*(?:약점|불일치)", tail)
                self.check("RESULT exactly three final weaknesses",
                           numbered == ["1", "2", "3"] or len(table_rows) == 3 or len(subheads) == 3,
                           {"numbered": numbered, "table_rows": len(table_rows), "subheads": len(subheads)})
                self.check("RESULT weakness is last top section",
                           not any(h.start() > weak[0].start() and len(h[0].split()[0]) <= len(weak[0][0].split()[0])
                                   for h in headings))
                self.check("RESULT next investigation in weakness block", "다음" in tail or "후속" in tail)
        if self.local("SELF_CHECK.md").is_file():
            text = self.text("SELF_CHECK.md")
            qrows = re.findall(r"(?m)^(?:#{1,6}\s*|\|\s*)Q([1-8])(?:\b|[·:：.\s|])", text)
            self.check("SELF_CHECK covers all eight Qs", set(qrows) == set("12345678"), qrows)
            for term in ("질문", "확인", "한계", "반례", "후속"):
                self.check("SELF_CHECK checklist column " + term, term in text)
            self.check("SELF_CHECK provenance wording", ("원문" in text or "URL" in text) and ("판" in text or "SHA" in text))
        if self.local("evidence/acceptance-evidence.json").is_file():
            obj = self.json("evidence/acceptance-evidence.json")
            self.check("acceptance evidence object", isinstance(obj, dict) and bool(obj))
            serialized = json.dumps(obj, ensure_ascii=False)
            self.check("acceptance preserves PARTIAL", "PARTIAL" in serialized)
            self.check("acceptance has actual check/exit evidence", bool(re.search(r"exit|종료", serialized, re.I)))
            self.check("acceptance has actor/time evidence",
                       bool(re.search(r"actor|subject|검사.*주체", serialized, re.I))
                       and bool(re.search(r"utc|checked_at|시점", serialized, re.I)))

    def owned_diff(self):
        changed = self.git("diff", "--name-only", "-z", BASE).stdout.decode().split("\0")
        untracked = self.git("ls-files", "--others", "--exclude-standard", "-z").stdout.decode().split("\0")
        paths = sorted(set(p for p in changed + untracked if p))
        outside = [p for p in paths if not p.startswith(PREFIX)]
        self.check("all changed/untracked paths owned", not outside, outside)
        self.check("no unmerged index entries", not self.git("ls-files", "-u").stdout)
        self.counts["owned_changed_or_untracked_paths"] = len(paths)
        self.counts["outside_paths"] = outside
        self.counts["source_tree_clean"] = not bool(self.git("status", "--porcelain").stdout)

def parse_date(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))

def json_pointer(value, pointer):
    if not pointer or pointer == "#":
        return value
    pointer = pointer.lstrip("#")
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {pointer}")
    for token in pointer[1:].split("/"):
        key = token.replace("~1", "/").replace("~0", "~")
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value

def prediction(reader, case_id):
    raw = reader["predictions"]
    if isinstance(raw, dict):
        return raw[case_id], raw[case_id]
    item = next(x for x in raw if x.get("case_id", x.get("case")) == case_id)
    if "candidates" in item:
        return {c["id"]: c["results"] for c in item["candidates"]}, item
    if "candidate_results" in item:
        return item["candidate_results"], item
    if "candidate_outputs" in item:
        return item["candidate_outputs"], item
    return {c["id"]: item[c["id"]] for c in reader["candidates"]}, item

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("draft", "final"), default="final")
    args = parser.parse_args()
    a = Audit(args.phase)
    for name in ("prerequisites", "seals", "sources", "frame_briefs", "views",
                 "tests", "auxiliary", "costs", "final_text", "owned_diff"):
        a.run(name, getattr(a, name))
    checked = sum(a.checks.values())
    result = {
        "schema": "AF-RES-077-readonly-verifier-v1",
        "phase": args.phase,
        "checked_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "actor": "read-only local mechanical verifier",
        "result": "PASS" if not a.errors else "FAIL",
        "exit_code": 0 if not a.errors else 1,
        "research_status": "PARTIAL",
        "checks": {"executed": checked, "passed": checked-len(a.errors),
                   "failed": len(a.errors), "by_section": dict(a.checks)},
        "counts": a.counts,
        "errors": a.errors,
        "warnings": a.warnings,
        "skips": a.skips,
        "limits": [
            "Mechanical integrity is not substantive source validation, research acceptance, or a native test pass.",
            "No network, target executable, original suite, proposed candidate, or auxiliary probe was run.",
            "The script reads local files and local Git objects only and writes nothing.",
            "Sealed historical input mistakes are preserved; ERRATA and review documents govern interpretation.",
            "Unavailable deleted full texts are not asserted to be independently hash-recomputed.",
            "Original source counts are work-lineage bookkeeping, not statistical independence.",
            "The scope check covers Git-visible changed/untracked paths; it is not a complete operating-system audit.",
            "Sources and costs may increase; their record totals are derived rather than fixed at302.",
            "Markdown checks verify required structure, not truth, exhaustiveness, or semantic quality.",
            "Captured auxiliary exit0 is historical evidence; this verifier never reruns that command."
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result["exit_code"]

if __name__ == "__main__":
    sys.exit(main())

