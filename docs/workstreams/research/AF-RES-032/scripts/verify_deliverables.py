#!/usr/bin/env python3
"""Read-only AF-RES-032 ledger checks; no network requests or Git mutations.

Print one JSON receipt to stdout. Only --receipt writes a file, and that path
must resolve inside this workstream. --final additionally requires HANDOFF.md
and acceptance-evidence.json. False research acceptance conditions are reported
as gaps, not converted into failed mechanical checks.
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import html
import io
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
from urllib.parse import unquote, urljoin, urlsplit


OWNED = Path(__file__).resolve().parents[1]
OWNED_REL = "docs/workstreams/research/AF-RES-032/"
START_SHA = "172c6bc37bdf91b91c86b9b3be29cb5b44fa4971"
SEAL_SHA = "168d90b8519bcb4f673acc659bbaae895f79fca5"
SEAL_BYTES = 50326
SEAL_HASH = "b3c2f68b905102f0fa682ab45a34c0f3401a69b61ba0a59327045e04a626d562"
BRANCH = "work/research-af-res-032"
A_IDS = [f"A-{route}{n:02}" for route in "DR" for n in range(1, 7)]
B_IDS = [f"B{n:02}" for n in range(1, 7)]
ALL_IDS = A_IDS + B_IDS
CATEGORIES = {"A_original": 12, "upstream": 34, "consumer_followup": 8,
              "cross_field": 8, "other_primary": 1, "B_consumer": 5,
              "B_auxiliary": 7}
TABLE_HEADERS = [
    ["참조 ID·A/B", "원 배포판·멤버·href·URL", "주변 문장·클릭 목적",
     "상류 전후 근거 URL·시점", "소비자 배포 전후 URL·시점", "유지/교체/보류", "미확인"],
    ["사건·참조", "시작 관측·근거", "끝 관측·근거", "시각 역할·정밀도",
     "계산 적격·구간", "끊긴 고리·필요 자료"],
    ["사례·목적", "URL만의 판정", "용도·판 추가 판정", "배포 이력 추가 판정",
     "원문 대조·반례", "재열람 수·미확인"],
]
WEAKNESS_HEADER = ["가장 중요한 불일치 또는 약점", "근거 URL", "영향을 받는 판단",
                   "다음 조사 제안·첫 자료"]
SELF_HEADER = ["주장", "근거 주소·위치 또는 탐색 실패 영수증", "자기 결론을 뒤집을 조건",
               "실제 반증을 찾은 경로와 결과", "남은 미확인"]
EARLIER_ATTEMPTS = [{
    "kind": "first draft validator development run",
    "target_HEAD": "6ac3d4d9c11f5a750401535a05caed29ed5daf01",
    "command_arguments": ["scripts/verify_deliverables.py", "--receipt", "evidence/deliverable-check-draft.json"],
    "exit_code": 1, "checks_total": 37, "checks_passed": 35,
    "data_defect_found": False,
    "failed_conditions": ["dedup_inventory_covers_395_and_preserves_conservative_semantics",
                          "committed_and_working_tree_changes_stay_in_owned_path"],
    "diagnosis": [
        "Validator expected the multi-record grouping inventory to include singleton originals: 301 grouped records plus 94 singletons actually cover all 395 records.",
        "Validator compared subdirectory-relative git ls-files output with repository-relative allowed paths. Commands now run at the repository root and ls-files uses --full-name."
    ],
    "receipt_retention_limit": "The first draft JSON was overwritten by a later successful draft run; its exit code, counts and diagnoses are retained from directly observed tool stdout. That run's complete input hash manifest and exact UTC are not retained.",
}]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def truth(value):
    if isinstance(value, bool):
        return value
    if str(value).lower() in ("true", "1"):
        return True
    if str(value).lower() in ("false", "0", "", "none", "null"):
        return False
    raise ValueError(f"Not a boolean: {value!r}")


def nested(value):
    if isinstance(value, str) and value[:1] in ("[", "{"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
    return value


def cells(line):
    return [c.strip().replace(r"\|", "|")
            for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def markdown_tables(text):
    lines = text.splitlines()
    tables = []
    i = 0
    while i + 1 < len(lines):
        header, separator = cells(lines[i]), cells(lines[i + 1])
        if (lines[i].lstrip().startswith("|") and separator
                and all(re.fullmatch(r":?-{3,}:?", c) for c in separator)):
            j, rows = i + 2, []
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append(cells(lines[j]))
                j += 1
            tables.append({"header": header, "rows": rows, "line": i + 1, "end": j})
            i = j
        else:
            i += 1
    return tables


def markdown_targets(text):
    """Read inline link destinations, preserving balanced parentheses in URLs."""
    for match in re.finditer(r"(?<!\\)\]\(", text):
        start = match.end()
        depth, i = 1, start
        while i < len(text) and depth:
            if text[i] == "\\":
                i += 2
                continue
            depth += (text[i] == "(") - (text[i] == ")")
            i += 1
        if not depth:
            raw = text[start:i - 1].strip()
            yield raw[1:raw.find(">")] if raw.startswith("<") else raw.split()[0] if raw else ""
    for match in re.finditer(r"(?m)^\s*\[[^\]]+\]:\s*(\S+)", text):
        yield match.group(1).strip("<>")


class Verifier:
    def __init__(self, final):
        self.final = final
        self.checks, self.deferred, self.inputs = [], [], {}
        self.cache = {}
        self.repo = Path(self.git("rev-parse", "--show-toplevel").decode().strip())
        self.head = self.git("rev-parse", "HEAD").decode().strip()
        self.refs, self.sources, self.chains, self.intervals, self.comparisons = [], [], [], [], []
        self.editions, self.frame, self.counts, self.dedup = [], [], {}, []
        self.card_inputs, self.research_gaps = {}, []

    def git(self, *args):
        # Run inventory commands at the repository root, so untracked files
        # outside this workstream cannot be hidden by Git's subdirectory scope.
        result = subprocess.run(["git", "-C", str(getattr(self, "repo", OWNED)), *args],
                                capture_output=True, check=False)
        if result.returncode:
            raise RuntimeError(f"git {shlex.join(args)}: {result.stderr.decode().strip()}")
        return result.stdout

    def data(self, name):
        path = (OWNED / name).resolve()
        if path not in self.cache:
            data = path.read_bytes()
            self.cache[path] = data
            self.inputs[str(path.relative_to(self.repo))] = {"sha256": sha(data), "bytes": len(data)}
        return self.cache[path]

    def text(self, name):
        return self.data(name).decode("utf-8")

    def json(self, name):
        return json.loads(self.text(name))

    def check(self, name, met, evidence=None, note=""):
        self.checks.append({"condition": name, "met": bool(met), "evidence": evidence, "note": note})

    def step(self, name, fn):
        try:
            fn()
        except Exception as error:
            self.check(name, False, {"error_type": type(error).__name__, "error": str(error)})

    def load(self):
        for name, attr, kind in [
            ("references.jsonl", "refs", "jsonl"), ("sources.jsonl", "sources", "jsonl"),
            ("chains.csv", "chains", "csv"), ("intervals.csv", "intervals", "csv"),
            ("comparisons.csv", "comparisons", "csv"), ("editions.csv", "editions", "csv"),
            ("frame.csv", "frame", "csv"), ("evidence/counts.json", "counts", "json"),
            ("evidence/source-deduplication.json", "dedup", "json"),
        ]:
            try:
                text = self.text(name)
                value = ([json.loads(line) for line in text.splitlines() if line.strip()]
                         if kind == "jsonl" else list(csv.DictReader(io.StringIO(text)))
                         if kind == "csv" else json.loads(text))
                setattr(self, attr, value)
            except Exception as error:
                self.check("read_input:" + name, False, str(error))
        for sample, name in [("A", "L3-input.json"), ("B", "B-L3-input.json")]:
            self.card_inputs[sample] = self.json("evidence/masked/" + name)
        self.data("scripts/verify_deliverables.py")

    def seal_and_sample(self):
        raw = self.data("references.jsonl")
        prefix = b"".join(raw.splitlines(keepends=True)[:12])
        sealed = self.data("evidence/a-sealed.jsonl")
        commit_bytes = self.git("show", f"{SEAL_SHA}:{OWNED_REL}references.jsonl")
        self.check("A_seal_prefix_bytes_and_sha", prefix == sealed == commit_bytes
                   and len(prefix) == SEAL_BYTES and sha(prefix) == SEAL_HASH,
                   {"prefix_bytes": len(prefix), "sha256": sha(prefix), "sealed_commit": SEAL_SHA,
                    "commit_blob_sha256": sha(commit_bytes)})
        self.check("A_seal_receipts", self.json("evidence/a-seal-receipt.json")["sha256"] == SEAL_HASH
                   and self.json("evidence/a-seal-remote.json")["commit"] == SEAL_SHA)
        a = [r for r in self.refs if r.get("sample") == "A"]
        projects = collections.Counter(r.get("consumer_project") for r in a)
        docs = {(r.get("artifact_url"), r.get("member")) for r in a}
        routes = collections.Counter(r.get("route") for r in a)
        ids = [r.get("reference_id") for r in self.refs]
        self.check("references_A12_B6_and_unique_ids", len(ids) == 18 and set(ids) == set(ALL_IDS)
                   and ids[:12] == A_IDS and len(a) == 12, ids)
        self.check("A_12_documents_6_projects_max2_D6_R6", len(docs) == 12 and len(projects) == 6
                   and all(n <= 2 for n in projects.values()) and routes == {"D": 6, "R": 6},
                   {"documents": len(docs), "projects": dict(projects), "routes": dict(routes)})
        required = ["raw_href", "base_url", "resolved_url", "link_text", "purpose", "minimum_success",
                    "intent_unknown", "artifact_url", "member", "consumer_version"]
        problems = []
        for r in a:
            for field in required:
                if not r.get(field):
                    problems.append([r["reference_id"], field, "missing"])
            for field in ("artifact_sha256", "member_sha256"):
                if not re.fullmatch(r"[0-9a-f]{64}", r.get(field, "")):
                    problems.append([r["reference_id"], field, "invalid SHA256"])
            if "fragment" not in r or not r.get("member", "").endswith(".html"):
                problems.append([r["reference_id"], "member/fragment", "missing HTML or fragment field"])
            if urljoin(r.get("base_url", ""), html.unescape(r.get("raw_href", ""))) != r.get("resolved_url"):
                problems.append([r["reference_id"], "resolved_url", "resolution differs"])
        self.check("A_raw_href_hash_member_purpose_fields", not problems, problems)

    def source_ledger(self):
        ids = [s.get("source_id") for s in self.sources]
        self.check("sources_395_unique_ids", len(ids) == len(set(ids)) == 395,
                   {"rows": len(ids), "unique": len(set(ids))})
        fields = ["source_id", "kind", "publisher", "original_url", "version", "publication_date",
                  "observed_at_utc", "read_location", "findings", "limits", "questions", "reference_ids",
                  "duplicate_group", "count_minimum", "count_category", "minimum_counting_group",
                  "collector_record", "minimum_representative"]
        missing = [[s.get("source_id"), key] for s in self.sources for key in fields
                   if key not in s or s[key] is None or s[key] == "" or s[key] == []]
        # A group without a selected representative legitimately has null here.
        missing = [x for x in missing if x[1] != "minimum_representative"]
        malformed = [s.get("source_id") for s in self.sources
                     if not isinstance(s.get("count_minimum"), bool)]
        self.check("source_required_fields_and_boolean_count_flag", not missing and not malformed,
                   {"missing": missing, "malformed_count_flags": malformed})
        counted = [s for s in self.sources if s.get("count_minimum") is True]
        categories = collections.Counter(s["count_category"] for s in counted)
        self.check("75_minimum_originals_with_separate_categories", len(counted) == 75
                   and dict(categories) == CATEGORIES,
                   {"counted": len(counted), "categories": dict(categories)},
                   "B and cross-field sources do not replace A's 12 original documents.")
        exact_groups = collections.defaultdict(list)
        minimum_groups = collections.defaultdict(list)
        for s in counted:
            exact_groups[s["duplicate_group"]].append(s["source_id"])
            minimum_groups[s["minimum_counting_group"]].append(s["source_id"])
        repeats = {k: v for k, v in exact_groups.items() if len(v) > 1}
        overcounted = {k: v for k, v in minimum_groups.items() if len(v) > 1}
        self.check("minimum_count_has_no_duplicate_original_or_group", not repeats and not overcounted,
                   {"exact_duplicates": repeats, "multiple_minimum_representatives": overcounted})
        by_id = {s["source_id"]: s for s in self.sources}
        problems, covered = [], []
        for group in self.dedup:
            members = group.get("source_ids", [])
            covered += members
            representative = group.get("minimum_representative")
            selected = [sid for sid in members if by_id.get(sid, {}).get("count_minimum")]
            if (group.get("is_identical_body_assertion") is not False
                    or any(sid not in by_id for sid in members)
                    or any(by_id.get(sid, {}).get("minimum_counting_group") != group.get("minimum_counting_group") for sid in members)
                    or selected != ([representative] if representative else [])):
                problems.append(group.get("minimum_counting_group"))
        sizes = collections.Counter(s["minimum_counting_group"] for s in self.sources)
        expected_grouped = [s["source_id"] for s in self.sources if sizes[s["minimum_counting_group"]] > 1]
        singleton_count = sum(sizes[s["minimum_counting_group"]] == 1 for s in self.sources)
        self.check("dedup_inventory_and_singletons_cover_395_with_conservative_semantics",
                   not problems and collections.Counter(covered) == collections.Counter(expected_grouped)
                   and len(covered) + singleton_count == 395,
                   {"invalid_groups": problems, "grouped_records": len(covered), "singleton_records": singleton_count},
                   "The inventory lists groups with multiple records. Singletons remain in sources.jsonl. minimum_counting_group is not an identical-body assertion; archive URL alone does not merge members.")
        expected = {"source_ledger_rows": len(ids), "unique_minimum_originals": len(counted),
                    "unique_minimum_by_category": dict(categories)}
        self.check("source_counts_match_published_counts", all(self.counts.get(k) == v for k, v in expected.items()), expected)

    def joins(self):
        source_ids = {s["source_id"] for s in self.sources}
        dangling, uses = [], 0

        def walk(value, path):
            nonlocal uses
            value = nested(value)
            if isinstance(value, dict):
                for key, child in value.items():
                    child = nested(child)
                    if (key in ("source_id", "source_ids", "start_source", "end_source", "source_card_ids")
                            or key.endswith("_source_id") or key.endswith("_source_ids")):
                        values = child if isinstance(child, list) else [child]
                        for sid in values:
                            if sid is None or sid == "":
                                continue
                            uses += 1
                            if not isinstance(sid, str) or sid not in source_ids:
                                dangling.append({"path": path + "." + key, "value": sid})
                    walk(child, path + "." + key)
            elif isinstance(value, list):
                for i, child in enumerate(value):
                    walk(child, f"{path}[{i}]")

        inputs = {"references": self.refs, "chains": self.chains, "intervals": self.intervals,
                  "editions": self.editions, "frame": self.frame, "source_deduplication": self.dedup,
                  "A_L3_cards": self.card_inputs["A"], "B_L3_cards": self.card_inputs["B"]}
        for name, value in inputs.items():
            walk(value, name)
        self.check("all_used_source_ids_join_ledger", not dangling, {"joins_checked": uses, "dangling": dangling})
        for name, rows in [("chains", self.chains), ("comparisons", self.comparisons)]:
            ids = [r["reference_id"] for r in rows]
            self.check(name + "_has_each_of_18_references_once", len(ids) == 18 and set(ids) == set(ALL_IDS), ids)

    def dates(self):
        strict = [r for r in self.intervals if r["interval_id"].endswith("-strict")]
        aux = [r for r in self.intervals if not r["interval_id"].endswith("-strict")]
        self.check("strict_18_rows_zero_eligible_zero_conditional_zero_censor",
                   len(strict) == 18 and {r["reference_id"] for r in strict} == set(ALL_IDS)
                   and all(not truth(r["eligible"]) and not truth(r["strict_eligible"])
                           and int(r["conditional_denominator"]) == 0 and not truth(r["right_censored"])
                           and not r["seconds"] for r in strict),
                   {"strict_rows": len(strict), "eligible": sum(truth(r["eligible"]) for r in strict),
                    "conditional_denominator": sum(int(r["conditional_denominator"]) for r in strict),
                    "censored": sum(truth(r["right_censored"]) for r in strict)},
                   "Zero eligible conditional denominator means not applicable, not 0% propagation.")
        self.check("chains_and_all_intervals_have_no_strict_or_censor_claims",
                   all(not truth(r["strict_eligible"]) and not truth(r["right_censored"])
                       for r in self.chains + self.intervals))
        values, errors = {}, []
        for r in aux:
            start = dt.datetime.fromisoformat(r["start"].replace("Z", "+00:00"))
            end = dt.datetime.fromisoformat(r["end"].replace("Z", "+00:00"))
            delta = (end - start).total_seconds()
            values[r["reference_id"]] = delta
            if (start.tzinfo is None or end.tzinfo is None or delta != float(r["seconds"])
                    or not r["event_key"] or not nested(r["source_ids"])):
                errors.append(r["interval_id"])
        expected = {"A-R01": 52600, "A-R02": 52600, "A-R04": 55797, "A-R05": 510146,
                    "A-R06": 8352241, "A-D02": 13480547, "B02": 14044}
        self.check("auxiliary_7_date_pairs_arithmetic_and_joins", len(aux) == 7 and not errors and values == expected,
                   {"calculated_seconds": values, "invalid": errors},
                   "Purpose retirement intervals remain ineligible for correction lag.")
        p = next(r for r in aux if r["reference_id"] == "A-D02")
        detail = nested(p["details"])
        self.check("Python_status_report_nominal_delta_has_no_effective_event_bounds",
                   p["clock_pair"] == "official_upstream_status_report→consumer_source_committer"
                   and detail.get("lower_seconds", "missing") is None
                   and detail.get("upper_seconds", "missing") is None
                   and detail.get("eligible_for_effective_change_delay") is False
                   and detail.get("precision") == "displayed minute versus committer second; nominal delta, no actual-event bound",
                   {k: detail.get(k) for k in ("clock_pair", "precision", "lower_seconds", "upper_seconds", "note")})
        b = next(r for r in aux if r["reference_id"] == "B02")
        self.check("B02_committer_clock_not_author_clock", b["start"] == "2022-05-03T20:25:58Z"
                   and b["end"] == "2022-05-04T00:20:02Z"
                   and b["clock_pair"] == "consumer_source_committer→consumer_publication", b["interval_id"])
        self.check("strict_denominators_match_counts", all(self.counts.get(k) == 0 for k in
                   ("strict_pairs_found_A_of12", "strict_pairs_found_B_of6", "conditional_eligible_denominator",
                    "right_censored", "same_medium_reader_failure_chains"))
                   and self.counts.get("conditional_result") == "해당 없음")

    def comparison_checks(self):
        published = self.json("evidence/comparison-counts.json")
        rows_by_id = {r["reference_id"]: r for r in self.comparisons}
        chains = {r["reference_id"]: r for r in self.chains}
        counts, problems = [], []
        for sample in ("A", "B"):
            rows = [r for r in self.comparisons if r["sample"] == sample]
            cards = {r["rid"]: r["source_cards"] for r in self.card_inputs[sample]}
            for view in ("L1", "L2", "L3"):
                decision_file = ("collectors/cross/" if sample == "A" else "collectors/cran/B-") + view + "-decisions.json"
                decisions = {r["rid"]: r for r in self.json(decision_file)}
                tally = dict(sample=sample, view=view, attempt_denominator=len(rows), correct_actions=0,
                             wrong_replacement=0, wrong_keep=0, abstentions=0,
                             nonevaluable_HTML_baseline=sum(not truth(r["adjudication_eligible"]) for r in rows),
                             same_A_case_duplicates=sum(truth(r["A_duplicate"]) for r in rows),
                             extra_external_pages=0, source_cards=0)
                for row in rows:
                    rid, decision = row["reference_id"], row[f"{view}_decision"]
                    actual = decisions[rid]
                    expected_cards = len(cards[rid]) if view == "L3" else 0
                    declared_cards = actual.get("source_cards_in_input", actual.get("source_cards_read", 0))
                    if (decision != actual["decision"] or int(row[f"{view}_additional_external_pages"]) != actual["additional_pages"]
                            or int(row[f"{view}_source_cards"]) != expected_cards or declared_cards != expected_cards):
                        problems.append([rid, view, "sealed decision/cost mismatch"])
                    if row["source_adjudication"] != chains[rid]["purpose_verdict"]:
                        problems.append([rid, view, "adjudication differs from chain"])
                    comparison = ("보류" if decision == "보류" else "정답" if decision == row["source_adjudication"]
                                  else "오교체" if decision == "교체" else "잘못 유지")
                    # Published labels currently contain only 정답 and 보류.
                    if comparison != row[f"{view}_comparison"]:
                        problems.append([rid, view, "comparison label mismatch"])
                    field = "abstentions" if decision == "보류" else "correct_actions" if comparison == "정답" else "wrong_replacement" if decision == "교체" else "wrong_keep"
                    tally[field] += 1
                    tally["extra_external_pages"] += int(row[f"{view}_additional_external_pages"])
                    tally["source_cards"] += expected_cards
                counts.append(tally)
        comparable = [{k: row[k] for k in counts[0]} for row in published]
        self.check("comparison_6_sample_views_match_sealed_decisions_and_denominators",
                   not problems and comparable == counts, {"recomputed": counts, "mismatches": problems})
        self.check("comparison_cards_A50_B23_and_no_new_external_pages",
                   [(r["sample"], r["source_cards"]) for r in counts if r["view"] == "L3"] == [("A", 50), ("B", 23)]
                   and all(r["extra_external_pages"] == 0 for r in counts))
        self.check("comparison_ineligible_B04_duplicate_B05_prior_exposure_and_no_backdating",
                   not truth(rows_by_id["B04"]["adjudication_eligible"])
                   and truth(rows_by_id["B05"]["A_duplicate"])
                   and truth(rows_by_id["A-D04"]["possible_prior_exposure"])
                   and truth(rows_by_id["B03"]["possible_prior_exposure"])
                   and all(not truth(r["later_correction_backdated"]) for r in self.comparisons),
                   {"B04": "HTML baseline not evaluable", "B05": "same A event", "possible_prior_exposure": ["A-D04", "B03"]})

    def git_scope(self):
        manifest = self.json("manifest.json")
        branch = self.git("symbolic-ref", "--short", "HEAD").decode().strip()
        self.check("branch_and_start_manifest", branch == BRANCH and manifest["base_commit"] == START_SHA
                   and manifest["allowed_paths"] == [OWNED_REL], {"branch": branch, "base_commit": manifest["base_commit"]})
        ancestor = subprocess.run(["git", "-C", str(self.repo), "merge-base", "--is-ancestor", START_SHA, self.head],
                                  capture_output=True, check=False)
        self.check("start_commit_is_ancestor", ancestor.returncode == 0, {"start": START_SHA, "HEAD": self.head})
        paths = {}
        for label, args in [("committed_since_start", ["diff", "--no-renames", "--name-only", "-z", START_SHA, self.head]),
                            ("working_tree_including_index", ["diff", "--no-renames", "--name-only", "-z", "HEAD"]),
                            ("untracked_not_ignored", ["ls-files", "--full-name", "--others", "--exclude-standard", "-z"])]:
            paths[label] = [p for p in self.git(*args).decode().split("\0") if p]
        disallowed = {k: [p for p in v if not p.startswith(OWNED_REL)] for k, v in paths.items()}
        self.check("committed_and_working_tree_changes_stay_in_owned_path", not any(disallowed.values()),
                   {"path_counts": {k: len(v) for k, v in paths.items()}, "outside_owned_path": disallowed})
        control = "docs/automation/dot-control.json"
        baseline, committed = self.git("show", START_SHA + ":" + control), self.git("show", self.head + ":" + control)
        worktree = (self.repo / control).read_bytes()
        self.inputs[control] = {"sha256": sha(worktree), "bytes": len(worktree)}
        self.check("dot_control_unchanged_from_start", baseline == committed == worktree,
                   {"start_sha256": sha(baseline), "HEAD_sha256": sha(committed), "working_tree_sha256": sha(worktree)})

    def document_checks(self):
        result = self.text("RESULT.md")
        tables = markdown_tables(result)
        self.check("RESULT_first_three_tables_exact_headers", [t["header"] for t in tables[:3]] == TABLE_HEADERS,
                   [t["header"] for t in tables[:3]])
        prefix = result.splitlines()[1:tables[0]["line"] - 1]
        self.check("RESULT_first_table_immediately_after_title", result.startswith("# ") and not any(s.strip() for s in prefix))
        issues = []
        for index, table in enumerate(tables[:3], 1):
            ids = [re.findall(r"\b(?:A-[DR]0[1-6]|B0[1-6])\b", row[0]) for row in table["rows"]]
            unique = [found[0] if found else None for found in ids]
            if len(unique) != 18 or set(unique) != set(ALL_IDS) or any(len(row) != len(table["header"]) or not all(row) for row in table["rows"]):
                issues.append({"table": index, "rows": len(unique), "ids": unique})
        self.check("RESULT_first_three_tables_each_18_complete_rows", len(tables) >= 3 and not issues, issues)
        self.weakness_table("RESULT.md", result)
        own = self.text("SELF_CHECK.md")
        qtables = [t for t in markdown_tables(own) if t["header"] == SELF_HEADER]
        qrows = qtables[0]["rows"] if qtables else []
        qids = [re.search(r"\bQ([1-8])\b", row[0]) for row in qrows]
        self.check("SELF_CHECK_Q1_to_Q8_with_evidence_countersearch_unknowns",
                   len(qrows) >= 8 and {int(x.group(1)) for x in qids if x} == set(range(1, 9))
                   and all(len(row) == 5 and all(cell.strip() for cell in row) for row in qrows),
                   {"Q_rows": len(qrows), "Qs": [x.group(0) if x else None for x in qids]})
        notes = sorted((OWNED / "evidence/rows").glob("*.md"))
        self.check("18_row_notes_present", {p.stem for p in notes} == set(ALL_IDS), [p.name for p in notes])
        documents = ["RESULT.md", "SELF_CHECK.md"] + [str(p.relative_to(OWNED)) for p in notes]
        if (OWNED / "HANDOFF.md").exists():
            documents.append("HANDOFF.md")
            self.weakness_table("HANDOFF.md", self.text("HANDOFF.md"))
        elif self.final:
            self.check("final_HANDOFF_exists", False, "HANDOFF.md")
        else:
            self.deferred.append("HANDOFF.md required by --final")
        missing, checked, deferred = [], 0, []
        for name in documents:
            for target in markdown_targets(self.text(name)):
                if not target or target.startswith("#"):
                    continue
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc:
                    continue
                path = (OWNED / name).parent / unquote(parsed.path)
                checked += 1
                if not path.exists():
                    item = {"document": name, "target": target}
                    if not self.final and path.resolve() in {(OWNED / "HANDOFF.md").resolve(), (OWNED / "evidence/acceptance-evidence.json").resolve()}:
                        deferred.append(item)
                    else:
                        missing.append(item)
        self.check("local_markdown_link_targets_exist", not missing,
                   {"links_checked": checked, "missing": missing, "deferred_final_targets": deferred})

    def weakness_table(self, name, text):
        tables = markdown_tables(text)
        last = tables[-1] if tables else {"header": [], "rows": [], "end": 0}
        rows = last["rows"]
        self.check(name + "_ends_with_exactly_three_substantive_weakness_rows",
                   last["header"] == WEAKNESS_HEADER and len(rows) == 3
                   and all(len(row) == 4 and all(row) and "http" in row[1] for row in rows)
                   and not any(s.strip() for s in text.splitlines()[last["end"]:]),
                   {"header": last["header"], "rows": len(rows)})

    def acceptance(self):
        name = "evidence/acceptance-evidence.json"
        if not (OWNED / name).exists():
            if self.final:
                self.check("final_acceptance_file_exists", False, name)
            else:
                self.deferred.append(name + " required by --final")
            return
        data = self.json(name)
        conditions = data if isinstance(data, list) else next((data[k] for k in ("conditions", "checks", "criteria") if isinstance(data.get(k), list)), [])
        errors = []
        for i, item in enumerate(conditions):
            if (not isinstance(item, dict) or not all(k in item for k in ("condition", "met", "evidence", "note"))
                    or not isinstance(item.get("met"), bool) or not item.get("condition")
                    or not item.get("evidence") or not item.get("note")):
                errors.append(i)
            elif item["met"] is False:
                self.research_gaps.append(item)
        self.check("acceptance_schema_and_explicit_false_gap_records", bool(conditions) and not errors and bool(self.research_gaps),
                   {"conditions": len(conditions), "schema_errors": errors, "research_gaps": len(self.research_gaps)},
                   "False acceptance conditions preserve acknowledged research gaps; they are not mechanical check failures.")
        if self.research_gaps:
            texts = self.text("SELF_CHECK.md") + (self.text("HANDOFF.md") if (OWNED / "HANDOFF.md").exists() else "")
            self.check("false_acceptance_gaps_have_WITH_GAPS_status", "REVIEW_READY_WITH_GAPS" in texts)

    def run(self):
        for name, fn in [("load_inputs", self.load), ("seal_sample", self.seal_and_sample),
                         ("source_ledger", self.source_ledger), ("source_id_joins", self.joins),
                         ("date_pairs", self.dates), ("comparisons", self.comparison_checks),
                         ("git_scope", self.git_scope), ("documents", self.document_checks),
                         ("acceptance", self.acceptance)]:
            self.step(name, fn)
        changed = [str(path.relative_to(self.repo)) for path, data in self.cache.items()
                   if not path.exists() or sha(path.read_bytes()) != sha(data)]
        self.check("input_snapshot_unchanged_during_check", not changed, changed)
        final_head = self.git("rev-parse", "HEAD").decode().strip()
        self.check("HEAD_unchanged_during_check", self.head == final_head,
                   {"start_of_check": self.head, "end_of_check": final_head})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final", action="store_true", help="Require acceptance and HANDOFF final deliverables")
    parser.add_argument("--receipt", help="Optional JSON receipt path, absolute or relative to the owned workstream")
    args = parser.parse_args()
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    receipt_path = None
    if args.receipt:
        candidate = Path(args.receipt)
        receipt_path = (candidate if candidate.is_absolute() else OWNED / candidate).resolve()
        if not receipt_path.is_relative_to(OWNED) or receipt_path.suffix != ".json":
            print(json.dumps({"exit_code": 2, "error": "--receipt must be a .json path inside the owned workstream"}))
            return 2
    try:
        verifier = Verifier(args.final)
        verifier.run()
        failed = [c["condition"] for c in verifier.checks if not c["met"]]
        result = {"schema": 1, "task_id": "AF-RES-032", "mode": "final" if args.final else "draft",
                  "started_at_utc": started, "completed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                  "target_HEAD": verifier.head, "start_SHA": START_SHA, "sealed_A_commit": SEAL_SHA,
                  "command": shlex.join([sys.executable, *sys.argv]), "argv": [sys.executable, *sys.argv],
                  "cwd": os.getcwd(), "exit_code": int(bool(failed)), "checks_total": len(verifier.checks),
                  "checks_passed": len(verifier.checks) - len(failed), "failed_conditions": failed,
                  "deferred": verifier.deferred, "research_acceptance_false_conditions": verifier.research_gaps,
                  "earlier_attempts": EARLIER_ATTEMPTS,
                  "input_sha256": verifier.inputs, "checks": verifier.checks,
                  "external_requests": 0, "git_mutations": 0,
                  "scope_limit": "Local ledger, byte, join, arithmetic, table and link validation. No new external verification, no independent re-adjudication of source meanings.",
                  "receipt_path": str(receipt_path) if receipt_path else None}
        if receipt_path is not None and receipt_path in verifier.cache:
            result["exit_code"] = 2
            result["error"] = "Refusing to overwrite a checked input with --receipt"
            receipt_path = None
    except Exception as error:
        result = {"schema": 1, "started_at_utc": started, "exit_code": 2,
                  "command": shlex.join([sys.executable, *sys.argv]),
                  "error_type": type(error).__name__, "error": str(error),
                  "external_requests": 0, "git_mutations": 0}
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if receipt_path is not None:
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(encoded, encoding="utf-8")
    sys.stdout.write(encoded)
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
