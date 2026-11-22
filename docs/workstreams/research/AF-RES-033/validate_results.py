"""Read-only validation of the sealed AF-RES-033 result bundle.

The transport adjudication was already remotely sealed at
889c5e792a3db3856bf5be8c90d9486490ce8677 before this separate validation task.
This validator reads queries/ranks to audit joins; it never revises judgments.
Python stdlib only; no network, file creation, or mutation. JSON receipt on stdout.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
import csv
import io
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

sys.dont_write_bytecode = True
FIELDS = ("library", "transport", "statistics")
LABELS = ("support", "conflict", "partial", "unverified")
TABLE_HEADERS = [
    ["수신 설계 ID·최초 목적", "필수 조건", "S·R 경로·원 순위", "후보·원문 절 URL", "입력·변화·출력 대응", "남은 접합·깨지는 조건", "부분·전체 판정", "신규성·미확인"],
    ["수신 ID", "상위 1·3에서 인용 완료 S·R", "둘 다·한쪽만·둘 다 놓침", "전체 목록의 지지·충돌·부분·미확인 수", "검색·열람 비용", "노출 또는 제외 민감도"],
    ["반례 ID·분야", "표면 유사점", "작동이 같거나 다른 지점", "원문 두 주소", "당시 이용 가능성", "결론을 바꿀 자료"],
]
FINAL_HEADER = ["가장 중요한 불일치 또는 약점", "근거 자료 주소", "영향을 받는 결론", "다음 조사 제안과 첫 자료"]


def hashbytes(data):
    return sha256(data).hexdigest()


def truth(value):
    return value is True or value == "True"


def clean_url(url):
    return str(url).split("#", 1)[0]


class Audit:
    def __init__(self, root, args):
        self.root, self.repo, self.args = root, root.parents[3], args
        self.checks, self.errors, self.warnings = Counter(), [], []
        self.files, self.metrics, self.cache_missing = {}, {}, []
        self.cached = {}

    def check(self, ok, code, detail=None):
        self.checks[code] += 1
        if not ok:
            self.errors.append({"check": code, "detail": detail})
        return ok

    def warn(self, code, detail):
        item = {"check": code, "detail": detail}
        if item not in self.warnings:
            self.warnings.append(item)

    def path(self, value):
        p = Path(value)
        if not p.is_absolute():
            p = (self.repo if str(value).startswith("docs/") else self.root) / p
        p = p.resolve()
        if not p.is_relative_to(self.root):
            raise ValueError("Referenced evidence path is outside owned path: " + str(value))
        return p

    def read(self, name):
        p = self.path(name)
        data = p.read_bytes()
        self.files[str(p.relative_to(self.root))] = hashbytes(data)
        return data

    def jl(self, name):
        return [json.loads(s) for s in self.read(name).decode().splitlines() if s.strip()]

    def js(self, name):
        return json.loads(self.read(name))

    def csv(self, name):
        return list(csv.DictReader(io.StringIO(self.read(name).decode())))

    def optional_cache(self, value, expected, label):
        p = self.path(value)
        if self.args.metadata_only or not p.exists():
            self.cache_missing.append({"evidence": label, "path": str(p.relative_to(self.root)), "reason": "metadata_only_requested" if self.args.metadata_only else "absent"})
            return None
        data = p.read_bytes()
        self.check(hashbytes(data) == expected, "cache_hash", label)
        return data

    def ranges(self, loc):
        for key in ("line_ranges", "line_ranges_1based"):
            if key in loc:
                return loc[key]
        if "line_range_1based" in loc:
            return [loc["line_range_1based"]]
        if "line_start" in loc and "line_end" in loc:
            return [[loc["line_start"], loc["line_end"]]]
        return []

    def mandatory_locations(self, item, side):
        if side + "_locations" in item:
            return item[side + "_locations"]
        if side + "_evidence" in item:
            v = item[side + "_evidence"]
            return v if isinstance(v, list) else [v]
        if side + "_url" in item:
            return [{"url": item[side + "_url"], "line_ranges": item.get(side + "_line_ranges", [])}]
        return []

    def check_locations(self, locations, expected_url, source, bound, context):
        self.check(bool(locations), "both_source_locations", context)
        ranges = []
        for loc in locations:
            self.check(clean_url(loc.get("url", "")) == clean_url(expected_url), "evidence_url_join", context)
            if loc.get("source_id"):
                self.check(self.aliases.get(loc["source_id"]) == source, "evidence_source_alias_join", context)
            rs = self.ranges(loc)
            self.check(bool(rs), "evidence_has_line_range", context)
            for span in rs:
                ok = isinstance(span, list) and len(span) == 2 and all(isinstance(v, int) for v in span) and 1 <= span[0] <= span[1] <= bound
                self.check(ok, "line_bounds", {"context": context, "range": span, "bound": bound})
                if ok:
                    ranges.append(span)
        return ranges

    def run(self):
        inputs = self.jl("inputs.jsonl")
        corpus = self.jl("corpus.jsonl")
        sources = self.jl("sources.jsonl")
        maps = self.csv("maps.csv")
        rankings = self.csv("rankings.csv")
        returns = self.jl("returns.jsonl")
        windows = self.jl("evidence/returned-window-audit.jsonl")
        recount = self.js("evidence/recount.json")
        input_seal = self.js("evidence/input-seal.json")
        corpus_seal = self.js("evidence/corpus-seal.json")
        observation_seal = self.js("evidence/observation-seal.json")
        retrieval_receipt = self.js("evidence/retrieval-receipt.json")
        targets = self.jl("recipient/recipient_targets.jsonl")
        self.inputs = {x["recipient_id"]: x for x in inputs}
        self.corpus = {x["candidate_id"]: x for x in corpus}
        target_index = {x["recipient_id"]: x for x in targets}
        self.check(len(inputs) == len(self.inputs) == 8, "input_count_unique", len(inputs))
        self.check(len(corpus) == len(self.corpus) == 18, "corpus_count_unique", len(corpus))
        self.check(Counter(x["field"] for x in corpus) == {f: 6 for f in FIELDS}, "provider_fields_six_each")
        self.check(Counter(x["repository"] for x in inputs) == {"rust-lang/rfcs": 4, "kubernetes/enhancements": 4}, "recipient_projects_four_each")
        self.check(self.files["inputs.jsonl"] == input_seal["inputs_file_sha256"] == observation_seal["original_inputs_sha256"] == retrieval_receipt["inputs_sha256"], "inputs_original_seal_hash")
        self.check(self.files["corpus.jsonl"] == corpus_seal["corpus_file_sha256"] == observation_seal["original_corpus_sha256"] == retrieval_receipt["corpus_sha256"], "corpus_original_seal_hash")
        self.check(self.files["rankings.csv"] == observation_seal["original_rankings_sha256"] == retrieval_receipt["rankings_sha256"], "rankings_original_seal_hash")
        self.check(len(sources) == 61, "source_rows_61", len(sources))
        canonical = {s["source_id"]: s for s in sources}
        self.check(len(canonical) == len(sources), "source_id_unique")
        self.aliases = {}
        for s in sources:
            for name in [s["source_id"]] + s.get("aliases", []):
                self.check(name not in self.aliases or self.aliases[name] == s["source_id"], "source_alias_unique", name)
                self.aliases[name] = s["source_id"]
        minimum = [s for s in sources if s.get("counted_minimum") is True]
        categories = Counter(s["minimum_category"] for s in minimum)
        self.check(len(minimum) == 30 and categories == {"recipient": 8, "candidate": 18, "field": 4}, "minimum_30_categories", dict(categories))
        self.check(len({s["duplicate_group"] for s in minimum}) == 30, "minimum_duplicate_groups_unique")
        self.check(len({clean_url(s.get("fixed_url") or s["original_url"]) for s in minimum}) == 30, "minimum_original_or_fixed_urls_unique")
        self.check(Counter(s["field"] for s in minimum if s["minimum_category"] == "candidate") == {f: 6 for f in FIELDS}, "minimum_provider_fields")
        field_domains = {s["field"] for s in minimum if s["minimum_category"] == "field"}
        self.check(len(field_domains) >= 2, "field_at_least_two_domains", sorted(field_domains))
        no_fixed_url = [s["source_id"] for s in minimum if not s.get("fixed_url")]
        if no_fixed_url:
            self.warn("no_immutable_web_url", {"source_ids": no_fixed_url, "scope": "Explicit null fixed_url is retained. Original URL plus captured byte hash identifies the read edition locally; it does not promise the live URL is immutable."})
        for s in minimum:
            self.check("fixed_url" in s, "fixed_url_field_present_even_if_null", s["source_id"])
            self.check(s.get("read_status") in ("content_verified", "full_original_read"), "minimum_direct_read_status", s["source_id"])
            self.check(all(s.get(k) for k in ("original_url", "publisher", "read_location", "observed", "limitations", "checked_utc")), "minimum_source_fields", s["source_id"])
            for fr in s.get("fetch_receipts", []):
                if fr.get("cache_path") and fr.get("body_sha256"):
                    self.optional_cache(fr["cache_path"], fr["body_sha256"], s["source_id"] + ":fetch")
        for r in inputs:
            rid = r["recipient_id"]
            self.check(self.aliases.get(rid) == r["initial_source_id"] and r["initial_source_id"] in canonical, "recipient_source_alias_join", rid)
            self.check(r["frozen_partial_target"] == target_index[rid]["frozen_partial_target"], "target_frozen_join", rid)
            t = r["frozen_partial_target"]
            self.check(len(t["mandatory_predicate_ids"]) == len(set(t["mandatory_predicate_ids"])) and set(t["mandatory_predicate_ids"]) == {p["id"] for p in t["mandatory_predicates"]}, "target_predicate_ids", rid)
            raw = self.optional_cache(r["snapshot_path"], r["original_source"]["raw_sha256"], rid + ":original")
            if raw is not None:
                self.check(len(raw.decode().splitlines()) == r["original_source"]["line_count"], "recipient_line_count", rid)
            for route in ("S", "R"):
                q = r["query_" + route.lower()]
                expected = next(x for x in input_seal["queries"] if x["recipient_id"] == rid)[route]
                self.check(hashbytes(q.encode()) == r["query_" + route.lower() + "_sha256"] == expected, "query_hash_sealed", rid + "-" + route)
        for c in corpus:
            cid = c["candidate_id"]
            self.check(self.aliases.get(c["source_id"]) == c["source_id"] and c["source_id"] in canonical, "provider_source_join", cid)
            seal = next(x for x in corpus_seal["documents_and_text_hashes"] if x["candidate_id"] == cid)
            self.check(c["source_id"] == seal["source_id"] and c["url"] == seal["url"] and c["features"]["source_text_sha256"] == seal["source_text_sha256"], "provider_seal_join", cid)
            raw = self.optional_cache(c["cache_text_path"], c["features"]["source_text_sha256"], cid + ":body")
            if raw is not None:
                self.cached[cid] = raw.decode()
                self.check(len(raw.decode().splitlines()) == c["body_lines"], "provider_line_count", cid)
            if c.get("cache_raw_path") and c.get("raw_sha256"):
                self.optional_cache(c["cache_raw_path"], c["raw_sha256"], cid + ":raw")
        primary = {}
        origin = {}
        for field in FIELDS:
            name = "judgments/" + field + ".jsonl"
            js = self.jl(name)
            self.check(len(js) == 48, "field_pair_count", field)
            self.check(self.files[name] == observation_seal["primary_sha256"][field], "judgment_observation_seal_hash", field)
            for index, j in enumerate(js, 1):
                pair = j["pair_id"]
                self.check(pair not in primary, "primary_pair_unique", pair)
                primary[pair] = j
                origin[pair] = name + ":" + str(index)
                self.check(self.corpus[j["candidate_id"]]["field"] == field, "judgment_provider_field", pair)
        expected_pairs = {r + "-" + c for r in self.inputs for c in self.corpus}
        self.check(len(primary) == 144 and set(primary) == expected_pairs, "primary_cartesian_144")
        self.check(len(maps) == 144 and len({m["pair_id"] for m in maps}) == 144 and {m["pair_id"] for m in maps} == expected_pairs, "maps_cartesian_144")
        mindex = {m["pair_id"]: m for m in maps}
        mcount = Counter()
        for pair, j in primary.items():
            rid, cid = j["recipient_id"], j["candidate_id"]
            r, c = self.inputs[rid], self.corpus[cid]
            t = r["frozen_partial_target"]
            mids = [m["predicate_id"] for m in j["mandatory_evidence"]]
            self.check(len(mids) == len(set(mids)) and set(mids) == set(t["mandatory_predicate_ids"]), "mandatory_fixed_ids", pair)
            self.check(j["judgment"] in LABELS and j["whole_design_judgment"] in LABELS, "four_way_labels", pair)
            mandatory_statuses = [m["status"] for m in j["mandatory_evidence"]]
            mcount.update(mandatory_statuses)
            self.check(all(s in ("match", "conflict", "missing") for s in mandatory_statuses), "mandatory_status_vocabulary", pair)
            if j["judgment"] == "support":
                self.check(all(s == "match" for s in mandatory_statuses) and not j["new_core_required"], "support_all_match_no_new_core", pair)
            if j["judgment"] == "conflict":
                self.check("conflict" in mandatory_statuses and bool(j["break_condition"]), "conflict_explicit_predicate", pair)
            if j["judgment"] == "unverified":
                self.check("conflict" not in mandatory_statuses and bool(j["unverified_and_next_evidence"]), "unverified_not_implicit_conflict", pair)
            rb, pb = r["original_source"]["line_count"], c["body_lines"]
            self.check_locations(j["recipient_locations"], r["immutable_source_url"], r["initial_source_id"], rb, pair + ":recipient")
            self.check_locations(j["provider_locations"], c["url"], c["source_id"], pb, pair + ":provider")
            for e in j["mandatory_evidence"]:
                rl = self.mandatory_locations(e, "recipient")
                pl = self.mandatory_locations(e, "provider")
                rr = self.check_locations(rl, r["immutable_source_url"], r["initial_source_id"], rb, pair + ":" + e["predicate_id"] + ":recipient")
                self.check_locations(pl, c["url"], c["source_id"], pb, pair + ":" + e["predicate_id"] + ":provider")
                frozen = next(p["source_line_spans"] for p in t["mandatory_predicates"] if p["id"] == e["predicate_id"])
                self.check(any(max(a, x) <= min(b, y) for a, b in rr for x, y in frozen), "mandatory_recipient_span_relevance", pair + ":" + e["predicate_id"])
                reason = e.get("assessment", e.get("evidence", e.get("reason")))
                self.check(bool(reason), "mandatory_reason_present", pair + ":" + e["predicate_id"])
            for a, b in j["provider_evidence_line_ranges"]:
                self.check(1 <= a <= b <= pb, "provider_required_ranges_bounds", pair)
            m = mindex[pair]
            self.check(m["judgment_origin"] == origin[pair], "map_primary_origin", pair)
            for key in ("recipient_id", "candidate_id", "judgment", "whole_design_judgment", "break_condition"):
                self.check(m[key] == j[key], "map_primary_scalar", pair + ":" + key)
            for key in ("mandatory_evidence", "recipient_locations", "provider_locations", "provider_evidence_line_ranges", "input_map", "state_change_map", "output_map", "role_map", "preconditions_exceptions", "remaining_glue", "new_core_required", "novelty", "unverified_and_next_evidence"):
                self.check(json.loads(m[key]) == j[key], "map_primary_json", pair + ":" + key)
            self.check(json.loads(m["mandatory_predicate_ids"]) == t["mandatory_predicate_ids"] and m["frozen_partial_objective"] == t["objective"], "map_target_join", pair)
            self.check(m["recipient_source_id"] == r["initial_source_id"] and m["provider_source_id"] == c["source_id"] and m["recipient_url"] == r["immutable_source_url"] and m["provider_url"] == c["url"] and m["provider_field"] == c["field"], "map_source_join", pair)
            date = c.get("publication_or_version_date")
            temporal = "unverified" if not date else ("available" if date < r["created_at"][:len(date)] else "later_fixed_edition")
            self.check(m["historical_fixed_edition_status"] == temporal, "map_temporal_recount", pair)
        self.check(sum(mcount.values()) == 504, "mandatory_504", dict(mcount))
        self.metrics.update({"sources": len(sources), "minimum_sources": len(minimum), "minimum_categories": dict(categories), "field_domains": sorted(field_domains), "pairs": len(maps), "mandatory": sum(mcount.values()), "mandatory_statuses": dict(mcount)})
        # Replay the sealed algorithm without invoking its writer/main entry point.
        self.read("retrieval.py")
        self.check(self.files["retrieval.py"] == retrieval_receipt["algorithm_sha256"], "retrieval_algorithm_seal")
        spec = importlib.util.spec_from_file_location("af033_sealed_retrieval_validator", self.root / "retrieval.py")
        engine = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(engine)
        replay, runs, config = engine.rank(corpus, inputs)
        self.check([{k: str(v) for k, v in x.items()} for x in replay] == rankings, "exact_rankings_replay_288")
        self.check(config == retrieval_receipt["config"], "retrieval_config_replay")
        run_index = {(x["recipient_id"], x["route"]): x for x in runs}
        for old in retrieval_receipt["runs"]:
            new = run_index[old["recipient_id"], old["route"]]
            self.check({k: v for k, v in old.items() if k != "elapsed_ns"} == {k: v for k, v in new.items() if k != "elapsed_ns"}, "retrieval_run_receipt_replay", [old["recipient_id"], old["route"]])
        for cid, text in self.cached.items():
            self.check(engine.features(text) == self.corpus[cid]["features"], "all_body_features_and_windows_recomputed", cid)
        rank_index = {(x["recipient_id"], x["route"], x["candidate_id"]): x for x in rankings}
        self.check(len(rankings) == len(rank_index) == 288, "rankings_cartesian_288")
        self.check(len(returns) == 16 and len({(x["recipient_id"], x["route"]) for x in returns}) == 16, "returns_routes_16")
        zero = sum(float(x["score"]) == 0 for x in rankings)
        returned = sum(truth(x["returned_top3"]) for x in rankings)
        self.check(zero == 8 and returned == 48, "zero_and_returned_rows", {"zero": zero, "returned": returned})
        self.check(sum(x["empty_result"] for x in returns) == 0, "empty_routes_zero")
        returned_index = {}
        for run in returns:
            rid, route = run["recipient_id"], run["route"]
            rr = run_index[rid, route]
            self.check(run["query_sha256"] == rr["query_sha256"] and run["empty_result"] == rr["empty_result"] and len(run["returned_documents"]) == rr["returned_documents"], "returned_route_join", rid + "-" + route)
            expected = sorted([x for x in rankings if x["recipient_id"] == rid and x["route"] == route and truth(x["returned_top3"])], key=lambda x: int(x["rank"]))
            self.check([x["candidate_id"] for x in run["returned_documents"]] == [x["candidate_id"] for x in expected], "returned_order", rid + "-" + route)
            for d in run["returned_documents"]:
                cid = d["candidate_id"]
                rank = rank_index[rid, route, cid]
                c = self.corpus[cid]
                w = next(x for x in c["features"]["windows"] if x["window_id"] == rank["best_window_id"])
                self.check(d["window"] == w and d["url"] == c["url"] and d["source_id"] == c["source_id"] and d["rank"] == int(rank["rank"]) and d["score"] == rank["score"], "returned_window_metadata_exact", rid + "-" + route + "-" + cid)
                returned_index[rid, route, cid] = (d, w)
        self.check(len(windows) == 48 and len({w["return_id"] for w in windows}) == 48, "window_audit_48_unique")
        audited = {}
        content_checks = 0
        for row in windows:
            rid, route, cid = row["recipient_id"], row["route"], row["candidate_id"]
            pair = rid + "-" + cid
            d, w = returned_index[rid, route, cid]
            audited[rid, route, cid] = row
            expected_meta = {"return_id": rid + "-" + route + "-" + str(d["rank"]), "pair_id": pair, "provider_url": d["url"], "rank": d["rank"], "window_id": w["window_id"], "window_sha256": w["normalized_window_sha256"], "line_start": w["text_line_start_1based"], "line_end": w["text_line_end_1based"], "char_start": w["lowercase_normalized_char_start_0based"], "char_end_exclusive": w["lowercase_normalized_char_end_exclusive"], "document_judgment": primary[pair]["judgment"]}
            self.check(all(row[k] == v for k, v in expected_meta.items()), "window_audit_locator_join", row["return_id"])
            self.check(bool(row["read_observation"]), "window_direct_read_note", row["return_id"])
            if cid in self.cached:
                body = unicodedata.normalize("NFC", self.cached[cid]).lower()
                start, end = row["char_start"], row["char_end_exclusive"]
                self.check(hashbytes(body[start:end].encode()) == row["window_sha256"], "exact_returned_text_hash", row["return_id"])
                self.check(1 + body[:start].count("\n") == row["line_start"] and 1 + body[:end].count("\n") == row["line_end"], "exact_returned_line_locator", row["return_id"])
                offsets = [0]
                for line in body.splitlines(keepends=True):
                    offsets.append(offsets[-1] + len(line))
                contained, outside = [], []
                for a, b in primary[pair]["provider_evidence_line_ranges"]:
                    lo, hi = offsets[a-1], offsets[b]
                    while lo < hi and body[lo].isspace():
                        lo += 1
                    while hi > lo and body[hi-1].isspace():
                        hi -= 1
                    (contained if start <= lo and hi <= end else outside).append([a, b])
                self.check(row["fully_contained_provider_evidence_ranges"] == contained and row["not_fully_contained_provider_evidence_ranges"] == outside, "exact_evidence_window_containment", row["return_id"])
                strict = primary[pair]["judgment"] == "support" and not outside
                self.check(row["strict_citation_complete"] is strict, "strict_window_citation_rule", row["return_id"])
                content_checks += 1
            elif primary[pair]["judgment"] != "support":
                self.check(row["strict_citation_complete"] is False, "nonsupport_cannot_be_citation_complete", row["return_id"])
        for m in maps:
            rid, cid = m["recipient_id"], m["candidate_id"]
            for route in ("S", "R"):
                rr = rank_index[rid, route, cid]
                for k in ("rank", "score", "returned_top1", "returned_top3", "best_window_id", "window_line_start", "window_line_end", "window_sha256"):
                    self.check(m[route + "_" + k] == rr[k], "map_rank_join", m["pair_id"] + ":" + route + ":" + k)
                aw = audited.get((rid, route, cid))
                self.check(truth(m[route + "_strict_citation_complete"]) == bool(aw and aw["strict_citation_complete"]), "map_window_citation_join", m["pair_id"] + ":" + route)
        # Independent arithmetic reconstruction, not a call to aggregate_results.py.
        counts = {label: sum(m["judgment"] == label for m in maps) for label in LABELS}
        per = []
        for rid in sorted(self.inputs):
            ms = [m for m in maps if m["recipient_id"] == rid]
            stat = {"recipient_id": rid, "candidate_counts": {label: sum(m["judgment"] == label for m in ms) for label in LABELS}, "strict_eligible_candidates": [m["candidate_id"] for m in ms if m["judgment"] == "support"], "historical_strict_eligible_candidates": [m["candidate_id"] for m in ms if m["judgment"] == "support" and m["historical_fixed_edition_status"] == "available"], "broad_eligible_candidates": [m["candidate_id"] for m in ms if m["judgment"] in ("support", "partial")], "searches": 2, "scored_documents": 36, "returned_slots": 6, "full_list_comparisons": 18, "unique_returned_candidates": len({w["candidate_id"] for w in windows if w["recipient_id"] == rid})}
            for route in ("S", "R"):
                stat[route] = {}
                for k in (1, 3):
                    subset = [m for m in ms if int(m[route + "_rank"]) <= k]
                    stat[route]["top" + str(k)] = {"strict_citation_ids": [m["candidate_id"] for m in subset if truth(m[route + "_strict_citation_complete"])], "strict_document_ids": [m["candidate_id"] for m in subset if m["judgment"] == "support"], "broad_document_ids": [m["candidate_id"] for m in subset if m["judgment"] in ("support", "partial")]}
            per.append(stat)
        self.check(per == recount["per_recipient"], "per_recipient_recount_equal")
        summary = {"recipients": len(inputs), "candidate_documents": len(corpus), "original_searches": len(returns), "scored_document_rows": len(rankings), "returned_slots": len(windows), "empty_searches": sum(r["empty_result"] for r in returns), "unique_candidate_window_pairs": len({(w["candidate_id"], w["window_id"]) for w in windows}), "pair_count": len(maps), "mandatory_evidence_count": sum(mcount.values()), "counts": counts, "whole_design_support": sum(m["whole_design_judgment"] == "support" for m in maps), "historical_candidate_counts": dict(Counter(m["historical_fixed_edition_status"] for m in maps)), "historical_candidate_ids": sorted({m["candidate_id"] for m in maps if m["historical_fixed_edition_status"] == "available"}), "strict_all_list_support_pairs": [m["pair_id"] for m in maps if m["judgment"] == "support"], "strict_both_missed_pairs": [m["pair_id"] for m in maps if m["judgment"] == "support" and not truth(m["S_returned_top3"]) and not truth(m["R_returned_top3"])], "strict_citation_complete_slots": sum(w["strict_citation_complete"] for w in windows), "input_sha256": self.files["inputs.jsonl"], "corpus_sha256": self.files["corpus.jsonl"], "rankings_sha256": self.files["rankings.csv"], "judgment_sha256": {f: self.files["judgments/" + f + ".jsonl"] for f in FIELDS}}
        for key, value in summary.items():
            self.check(recount.get(key) == value, "summary_recount_equal", key)
        variants = []
        for name, exclude in [("all", None), ("exclude_R01", "R01"), ("exclude_R03", "R03"), ("exclude_R04", "R04"), ("exclude_R08", "R08"), ("exclude_query_author_exposure", None), ("opening_verified_only", None)]:
            selected = [s for s in per if s["recipient_id"] != exclude]
            v = {"variant": name, "recipient_denominator": len(selected), "strict_full_list_eligible_questions": sum(bool(s["strict_eligible_candidates"]) for s in selected)}
            for route in ("S", "R"):
                for k in (1, 3):
                    for label, key in (("strict", "strict_citation_ids"), ("broad", "broad_document_ids")):
                        v[f"{label}_top{k}_{route}"] = sum(bool(s[route][f"top{k}"][key]) for s in selected)
            variants.append(v)
        self.check(variants == recount["sensitivities"], "sensitivity_recount_equal")
        self.metrics.update({"counts": counts, "rankings": len(rankings), "routes": len(returns), "returned_slots": len(windows), "zero_score_rows": zero, "empty_routes": summary["empty_searches"], "exact_window_content_checks": content_checks, "body_feature_replays": len(self.cached), "unique_candidate_window_pairs": summary["unique_candidate_window_pairs"], "strict_all_list_support_pairs": summary["strict_all_list_support_pairs"], "strict_citation_complete_slots": summary["strict_citation_complete_slots"], "whole_design_support": summary["whole_design_support"], "historical_candidate_counts": summary["historical_candidate_counts"], "per_recipient": per, "sensitivities": variants})
        if self.cache_missing:
            self.warn("cache_reproduction_limit", {"missing_or_skipped": len(self.cache_missing), "items": self.cache_missing, "scope": "Committed frequencies permit exact rank replay. Without original bytes, content/window hash, full-line containment, and underlying source authenticity cannot be independently replayed; metadata bounds alone do not prove semantic evidence."})
            self.check(not self.args.require_cache, "required_cache_available", len(self.cache_missing))
        self.primary, self.rank_index, self.window_rows = primary, rank_index, windows
        self.run_records, self.retrieval_receipt = runs, retrieval_receipt
        self.report(per, summary)
        # Detect an in-progress concurrent aggregate/report rewrite during validation.
        for name, digest in list(self.files.items()):
            self.check(hashbytes((self.root/name).read_bytes()) == digest, "read_snapshot_stable", name)

    def report(self, per, summary):
        file = self.root / "RESULT.md"
        if not file.exists():
            self.check(not self.args.require_report, "required_report_exists")
            self.warn("report_not_yet_available", "Run again with --require-report after RESULT.md is complete; no report schema or numeric claims checked in this receipt.")
            self.metrics["report_checked"] = False
            return
        text = self.read("RESULT.md").decode()
        lines = text.splitlines()
        tables = []
        i = 0
        while i < len(lines):
            if lines[i].lstrip().startswith("|"):
                start = i
                block = []
                while i < len(lines) and lines[i].lstrip().startswith("|"):
                    block.append(lines[i]); i += 1
                if len(block) >= 2:
                    cells = lambda s: [c.strip() for c in re.split(r"(?<!\\)\|", s.strip().strip("|"))]
                    if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells(block[1])):
                        tables.append({"start": start, "end": i, "header": cells(block[0]), "rows": [cells(s) for s in block[2:]]})
                continue
            i += 1
        self.check(bool(lines) and lines[0].startswith("# "), "report_title_first")
        self.check(len(tables) >= 4, "report_at_least_four_tables", len(tables))
        if len(tables) < 4:
            self.metrics["report_checked"] = True
            return
        for idx, header in enumerate(TABLE_HEADERS):
            self.check(tables[idx]["header"] == header, "report_required_table_order_headers", idx+1)
            self.check(bool(tables[idx]["rows"]) and all(len(row) == len(header) for row in tables[idx]["rows"]), "report_required_table_shape", idx+1)
        allowed = set()
        for table in tables[:3]:
            allowed.update(range(table["start"], table["end"]))
        prelude = [line for n, line in enumerate(lines[1:tables[2]["end"]], 1) if n not in allowed and line.strip()]
        self.check(not prelude, "report_three_tables_immediately_after_title", prelude)
        last = tables[-1]
        self.check(last["header"] == FINAL_HEADER and len(last["rows"]) == 3 and all(len(x) == 4 for x in last["rows"]), "report_final_exact_three_rows")
        self.check(not any(l.strip() for l in lines[last["end"]:]), "report_final_table_is_last")
        ids = []
        per_index = {s["recipient_id"]: s for s in per}
        totals = [summary["counts"][key] for key in LABELS]
        total_rows = 0
        for row in tables[1]["rows"]:
            aggregate = row[0].strip(" *") in ("합계", "전체")
            if aggregate:
                total_rows += 1
                expected, denominator, rid = totals, len(self.inputs), "aggregate"
                selected = per
            else:
                matches = re.findall(r"R0[1-8]", row[0])
                self.check(len(matches) == 1, "report_table2_recipient_id", row[0])
                if len(matches) != 1:
                    continue
                rid = matches[0]
                ids.append(rid)
                expected = [per_index[rid]["candidate_counts"][x] for x in LABELS]
                denominator, selected = 1, [per_index[rid]]
            left, sep, right = row[3].partition("=")
            values = [int(n) for n in re.findall(r"(?<![A-Za-z0-9])\d+(?![A-Za-z0-9])", left)]
            self.check(values == expected, "report_table2_candidate_counts", {"recipient": rid, "found": values, "expected": expected})
            if sep:
                self.check(right.strip() == str(sum(expected)), "report_table2_candidate_denominator", rid)
            citation_cells = re.findall(r"상위\s*([13])\s*S\s*(\d+)\s*/\s*(\d+)\s*[·,;]\s*R\s*(\d+)\s*/\s*(\d+)", row[1])
            self.check(len(citation_cells) == 2 and {x[0] for x in citation_cells} == {"1", "3"}, "report_table2_citation_schema", {"recipient": rid, "cell": row[1]})
            for k, sn, sd, rn, rd in citation_cells:
                sexp = sum(bool(x["S"]["top" + k]["strict_citation_ids"]) for x in selected)
                rexp = sum(bool(x["R"]["top" + k]["strict_citation_ids"]) for x in selected)
                self.check([int(sn), int(sd), int(rn), int(rd)] == [sexp, denominator, rexp, denominator], "report_table2_citation_counts", rid + ":top" + k)
        self.check(len(ids) == 8 and set(ids) == set(self.inputs), "report_table2_all_eight")
        self.check(total_rows == 1, "report_table2_one_checked_aggregate", total_rows)
        table1_pairs = []
        for row in tables[0]["rows"]:
            self.check(bool(re.search(r"R0[1-8]", row[0])), "report_table1_recipient_link", row[0])
            self.check(bool(re.search(r"[LST]0[1-6]", " ".join(row))), "report_table1_candidate_id", row[0])
            self.check("https://" in " ".join(row), "report_table1_source_url", row[0])
            pair_ids = re.findall(r"R0[1-8]-[LST]0[1-6]", row[3])
            self.check(len(pair_ids) == 1, "report_table1_pair_id", row[3])
            if len(pair_ids) == 1:
                pair = pair_ids[0]
                table1_pairs.append(pair)
                rid, cid = pair.split("-")
                mentioned_ranks = re.findall(r"([SR])\s*(\d+)위\s*(미반환|반환)", row[2])
                self.check(len(mentioned_ranks) == 2, "report_table1_both_original_ranks", pair)
                for route, rank, returned in mentioned_ranks:
                    rr = self.rank_index[rid, route, cid]
                    self.check(int(rank) == int(rr["rank"]) and (returned == "반환") == truth(rr["returned_top3"]), "report_table1_original_rank_values", pair + ":" + route)
                for route, wid, first, last_line in re.findall(r"([SR])\s+(W\d+)\s+L(\d+)[–-](\d+)", row[3]):
                    rr = self.rank_index[rid, route, cid]
                    self.check(wid == rr["best_window_id"] and int(first) == int(rr["window_line_start"]) and int(last_line) == int(rr["window_line_end"]), "report_table1_original_window_locators", pair + ":" + route)
        returned_pairs = {w["pair_id"] for w in self.window_rows}
        expected_pairs = returned_pairs | set(summary["strict_all_list_support_pairs"])
        self.check(len(table1_pairs) == len(set(table1_pairs)) and set(table1_pairs) == expected_pairs, "report_table1_return_union_and_full_list_support", {"rows": len(table1_pairs), "expected": len(expected_pairs)})
        for row in tables[2]["rows"]:
            urls = re.findall(r"https?://[^\s)>|]+", row[3])
            self.check(len(set(urls)) >= 2, "report_counterexample_two_urls", row[0])
        for row in last["rows"]:
            self.check(all(cell.strip() for cell in row), "report_last_three_rows_populated", row[0])
        self.metrics["report_checked"] = True
        self.metrics["report_tables"] = len(tables)
        self.metrics["report_first_table_rows"] = len(table1_pairs)
        self.metrics["report_returned_pair_union"] = len(returned_pairs)
        self.metrics["report_table2_counts_recomputed"] = {x["recipient_id"]: x["candidate_counts"] for x in per}
        self.narrative_checks(text, lines, tables, per, summary)
        self.warn("report_semantic_limit", "Table schema/counts, original-rank/window links and specified narrative arithmetic are checked. Meaning, opposing interpretations and analogy validity remain semantic adjudication, not proved by this script.")

    def narrative_checks(self, text, lines, tables, per, summary):
        body = "\n".join(lines[tables[2]["end"]:]).replace("**", "")
        checks = {}
        def claim(name, pattern, expected):
            matches = re.findall(pattern, body)
            vals = []
            if len(matches) == 1:
                groups = matches[0] if isinstance(matches[0], tuple) else (matches[0],)
                vals = [float(str(x).replace(",", "")) for x in groups]
            self.check(vals == [float(x) for x in expected], "report_narrative_arithmetic", {"claim": name, "found": vals, "expected": expected})
            checks[name] = {"observed": vals, "expected": expected}
        changes = []
        for rid in sorted(self.inputs):
            ranks = {route: [x["candidate_id"] for x in sorted(self.rank_index.values(), key=lambda x: int(x["rank"])) if x["recipient_id"] == rid and x["route"] == route and truth(x["returned_top3"])] for route in ("S", "R")}
            changes.append({"recipient_id": rid, "S": ranks["S"], "R": ranks["R"], "top1_changed": ranks["S"][0] != ranks["R"][0], "top3_set_changed": set(ranks["S"]) != set(ranks["R"])})
        budgets = {route: {"raw_sum": sum(r["raw_query_tokens"] for r in self.run_records if r["route"] == route), "effective_unique_sum": sum(r["unique_query_tokens_after_stopwords"] for r in self.run_records if r["route"] == route)} for route in ("S", "R")}
        field_slots = Counter(self.corpus[w["candidate_id"]]["field"] for w in self.window_rows)
        elapsed = sum(r["elapsed_ns"] for r in self.retrieval_receipt["runs"])/1e6
        claim("top1_changed_questions", r"상위1\s*문서는\s*(\d+)/(\d+)", [sum(x["top1_changed"] for x in changes), len(self.inputs)])
        claim("top3_set_changed_questions", r"상위3\s*집합은\s*(\d+)/(\d+)", [sum(x["top3_set_changed"] for x in changes), len(self.inputs)])
        claim("raw_query_tokens", r"원토큰\s*합도\s*S(\d+)/R(\d+)", [budgets["S"]["raw_sum"], budgets["R"]["raw_sum"]])
        claim("effective_unique_tokens", r"S의\s*고유\s*토큰\s*합(\d+)·평균([\d.]+),\s*R(\d+)·평균([\d.]+)다", [budgets["S"]["effective_unique_sum"], budgets["S"]["effective_unique_sum"]/8, budgets["R"]["effective_unique_sum"], budgets["R"]["effective_unique_sum"]/8])
        claim("returned_field_slots", r"상위(\d+)슬롯은\s*교통(\d+)·도서관(\d+)·통계(\d+)", [len(self.window_rows), field_slots["transport"], field_slots["library"], field_slots["statistics"]])
        claim("body_raw_token_examples", r"T04는([\d,]+)원토큰이고\s*L04는([\d,]+)원토큰", [self.corpus["T04"]["features"]["raw_token_count"], self.corpus["L04"]["features"]["raw_token_count"]])
        claim("zero_score_rows", r"점수0인\s*문서(\d+)행", [self.metrics["zero_score_rows"]])
        claim("empty_searches", r"빈\s*검색은\s*(\d+)/(\d+)", [summary["empty_searches"], summary["original_searches"]])
        claim("scorer_milliseconds", r"계산시간([\d.]+)ms", [round(elapsed, 3)])
        frame = self.csv("frame.csv")
        recipient_frame = self.csv("recipient/recipient_frame.csv")
        fc = Counter(r["record_type"] for r in frame)
        prefix = [r for r in recipient_frame if str(r["primary_chronological_prefix"]).lower() == "true"]
        selected = sum(r["screening_state"] == "selected" for r in prefix)
        claim("frame_units", r"원 프레임(\d+)행은\s*수신(\d+)·제공 발행처(\d+)·제공 발견 후보(\d+)", [len(frame), fc["recipient_pr"], fc["provider_issuer"], fc["provider_discovery_candidate"]])
        claim("recipient_metadata_rows", r"최초 생성 목록([\d,]+)행", [len(recipient_frame)])
        claim("selected_prefix", r"선택 접두부(\d+)건은 선정(\d+)·제외(\d+)", [len(prefix), selected, len(prefix)-selected])
        claim("whole_scope_count", r"전체 기능/절차 설계(\d+)개", [sum(r["target_scope"] == "whole_design" for r in self.inputs.values())])
        manifests = ["libraries_1_candidate_manifest.jsonl", "libraries_2_stats_1_candidate_manifest.jsonl", "statistics_2_candidate_manifest.jsonl", "library_directory_manifest.jsonl", "transit_candidate_manifest.jsonl"]
        discovered_lists = sum(len(self.jl("donor/" + name)) for name in manifests)
        claim("discovery_lists_and_candidates", r"(\d+)개 발견 목록/(\d+)후보 기록", [discovered_lists, fc["provider_discovery_candidate"]])
        # Compare additional numerical tables with independently rebuilt ledgers.
        field_header = ["분야", "지지", "충돌", "부분", "미확인", "전체"]
        field_tables = [t for t in tables if t["header"] == field_header]
        self.check(len(field_tables) == 1, "report_field_count_table_present")
        if field_tables:
            names = {"도서관": "library", "교통": "transport", "통계": "statistics", "전체": None}
            for row in field_tables[0]["rows"]:
                field = names.get(row[0])
                selected_rows = [j for j in self.primary.values() if field is None or self.corpus[j["candidate_id"]]["field"] == field]
                expected = [sum(j["judgment"] == label for j in selected_rows) for label in LABELS] + [len(selected_rows)]
                self.check([int(x) for x in row[1:]] == expected, "report_field_count_table_values", row[0])
        comparison_tables = [t for t in tables if t["header"][:5] == ["판독 수준", "S 상위1", "R 상위1", "S 상위3", "R 상위3"]]
        self.check(len(comparison_tables) == 1, "report_comparison_table_present")
        if comparison_tables:
            keys = ("strict_citation_ids", "strict_document_ids", "broad_document_ids")
            self.check(len(comparison_tables[0]["rows"]) == 3, "report_comparison_three_levels")
            for row, key in zip(comparison_tables[0]["rows"], keys):
                for cell, (route, k) in zip(row[1:5], (("S", 1), ("R", 1), ("S", 3), ("R", 3))):
                    expected = [sum(bool(x[route][f"top{k}"][key]) for x in per), len(per)]
                    found = [int(x) for x in re.findall(r"\d+", cell)]
                    self.check(found == expected, "report_comparison_fraction_values", {"level": key, "route": route, "top": k})
        # The title sensitivity is a separate 16 searches, never added to original runs.
        alt = self.csv("sensitivities/T02-title-excluded-rankings.csv")
        ar = {(x["recipient_id"], x["route"], x["candidate_id"]): x for x in alt}
        sensitivity_receipt = self.js("sensitivities/T02-title-excluded-receipt.json")
        order_changes, top1_changes, top3_changes = 0, 0, 0
        for rid in self.inputs:
            for route in ("S", "R"):
                old = sorted([x for x in self.rank_index.values() if x["recipient_id"] == rid and x["route"] == route], key=lambda x: int(x["rank"]))
                new = sorted([x for x in alt if x["recipient_id"] == rid and x["route"] == route], key=lambda x: int(x["rank"]))
                a, b = [x["candidate_id"] for x in old], [x["candidate_id"] for x in new]
                order_changes += a != b
                top1_changes += a[:1] != b[:1]
                top3_changes += set(a[:3]) != set(b[:3])
        self.check([order_changes, top1_changes, top3_changes] == [sensitivity_receipt["rank_order_changed"], sensitivity_receipt["top1_changed"], sensitivity_receipt["top3_set_changed"]], "title_sensitivity_recount")
        changed_returned_windows = sum(w["window_sha256"] != ar[w["recipient_id"], w["route"], w["candidate_id"]]["window_sha256"] for w in self.window_rows)
        # The report may cite a result not returned by retrieval only through full ranks/corpus.
        missing_links = []
        for label, link in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text):
            if link.startswith(("https://", "http://", "#")):
                continue
            destination = link.split("#", 1)[0]
            if not destination:
                continue
            target = self.path(destination)
            if not target.exists():
                missing_links.append(destination)
            if destination == "returns.jsonl":
                pair = re.search(r"(R0[1-8])[–-]([LST]0[1-6])", label)
                if pair:
                    self.check(pair[1] + "-" + pair[2] in {w["pair_id"] for w in self.window_rows}, "report_returns_link_actually_returned_pair", label)
        if missing_links:
            self.warn("report_pending_local_links", sorted(set(missing_links)))
        self.metrics["narrative_arithmetic"] = checks
        self.metrics["rank_changes"] = changes
        self.metrics["query_token_budgets"] = budgets
        self.metrics["returned_fields"] = dict(field_slots)
        self.metrics["original_scorer_elapsed_ms"] = elapsed
        self.metrics["T02_sensitivity"] = {"rank_order_changed": order_changes, "top1_changed": top1_changes, "top3_set_changed": top3_changes, "original_returned_window_hashes_changed": changed_returned_windows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--require-report", action="store_true", help="fail if RESULT.md is not yet present")
    parser.add_argument("--require-cache", action="store_true", help="fail if source bytes needed for content replay are missing")
    parser.add_argument("--metadata-only", action="store_true", help="explicitly skip local source bytes; report limits, but replay committed frequency vectors")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    if args.metadata_only and args.require_cache:
        parser.error("--metadata-only and --require-cache are mutually exclusive")
    audit = Audit(args.root.resolve(), args)
    try:
        audit.run()
    except Exception as exc:
        audit.errors.append({"check": "validator_exception", "detail": type(exc).__name__ + ": " + str(exc)})
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=audit.root, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        head = None
    receipt = {"status": "passed" if not audit.errors else "failed", "exit_code": 0 if not audit.errors else 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(), "checked_out_commit": head, "read_only": True, "validator_sha256": hashbytes(Path(__file__).read_bytes()), "mode": {"require_report": args.require_report, "require_cache": args.require_cache, "metadata_only": args.metadata_only}, "checks_executed": sum(audit.checks.values()), "check_groups": dict(sorted(audit.checks.items())), "error_count": len(audit.errors), "errors": audit.errors[:100], "warnings": audit.warnings, "metrics": audit.metrics, "checked_file_sha256": audit.files, "limits": ["Mechanical consistency and exact replay are not an independent semantic or human evaluation.", "A passed no-cache run validates frequency-vector rankings and ledger joins, not cached-original text or semantic correspondence."]}
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2 if args.pretty else None))
    return receipt["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
