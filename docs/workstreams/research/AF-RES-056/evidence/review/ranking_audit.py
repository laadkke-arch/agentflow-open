"""Read frozen Git objects; independently audit membership/rank without providers.

This audit does not import the study matcher or mutate its inputs. The boundary
matcher uses substring offsets and character tests rather than its regular
expression. Only evidence/review/ranking-audit-receipt.json is written.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import csv
import hashlib
import io
import json
import subprocess

HERE = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[6]
PREFIX = "docs/workstreams/research/AF-RES-056/"
STAGE1 = "1f63f0129207904a91ae9e01bb3e48c86415a644"
STAGE2 = "b765a189aa2a1f5982a4994fc0476273abbf7127"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def blob(name, ref=STAGE2):
    return git("show", ref + ":" + PREFIX + name)


def obj(name, ref=STAGE2):
    return json.loads(blob(name, ref))


def table(name, ref=STAGE2):
    return list(csv.DictReader(io.StringIO(blob(name, ref).decode())))


def normalize(value):
    return " ".join(value.casefold().replace("-", " ").split())


def word_character(value):
    return value == "_" or value.isalnum()


def bounded_phrase(field, phrase):
    haystack = normalize(field)
    needle = normalize(phrase)
    offset = 0
    while needle:
        location = haystack.find(needle, offset)
        if location < 0:
            return False
        end = location + len(needle)
        before_ok = location == 0 or not word_character(haystack[location - 1])
        after_ok = end == len(haystack) or not word_character(haystack[end])
        if before_ok and after_ok:
            return True
        offset = location + 1
    return False


catalog = table("catalog.csv")
vocabulary = table("vocabulary.csv")
requirements = obj("requirements.json")
matches = table("matches.csv")
slots = table("slots.csv")
frame = table("frame.csv")
plan = obj("evidence/path-plan.json")


def reproduce(slot_limit=3, drop_mapping=None):
    result = []
    for requirement in requirements:
        pool = [r for r in catalog if r["family"] == requirement["domain"]]
        assert [int(r["posted_rank"]) for r in pool] == list(range(1, len(pool) + 1))
        for method in ["L", "V"]:
            terms = []
            seen_terms = set()
            for mapping in vocabulary:
                if mapping["case_id"] != requirement["case_id"]:
                    continue
                if mapping["mapping_id"] == drop_mapping:
                    continue
                allowed = mapping["method"] == "L,V" or (method == "V" and mapping["method"] == "V")
                if not allowed:
                    continue
                normalized = normalize(mapping["target_term"])
                if normalized in seen_terms:
                    continue
                seen_terms.add(normalized)
                terms.append({"mapping_id": mapping["mapping_id"], "term": mapping["target_term"], "normalized": normalized})
            hits = []
            seen_urls = set()
            for entry in pool:
                evidences = []
                for term in terms:
                    for number, field in enumerate(json.loads(entry["search_fields_json"])):
                        if bounded_phrase(field, term["term"]):
                            evidences.append({"mapping_id": term["mapping_id"], "term": term["term"], "field_index": number, "field_value": field})
                if evidences and entry["destination_url"] not in seen_urls:
                    seen_urls.add(entry["destination_url"])
                    hits.append({"catalog_id": entry["catalog_id"], "posted_rank": int(entry["posted_rank"]), "url": entry["destination_url"], "hits": evidences})
            result.append({"comparison_id": requirement["case_id"] + "-" + method, "case_id": requirement["case_id"], "method": method, "terms": terms, "hits": hits, "top": [h["catalog_id"] for h in hits[:slot_limit]], "unfilled_slots": max(0, slot_limit - len(hits)), "unfilled_reason": "observed_no_match" if not hits else "matched_pool_exhausted" if len(hits) < slot_limit else "none"})
    return result


recomputed = reproduce()
checks = []


def check(name, passed, details):
    checks.append({"check": name, "passed": bool(passed), "details": details})


check("stage1_is_ancestor_of_stage2", subprocess.run(["git", "merge-base", "--is-ancestor", STAGE1, STAGE2], cwd=REPO).returncode == 0, "Pinned Git history, not a proof of unrecorded researcher exposure.")
for filename in ["requirements.json", "vocabulary.csv", "frame.csv"]:
    check("unchanged_" + filename, blob(filename, STAGE1) == blob(filename, STAGE2), "Byte-identical committed blobs between frozen stages.")

for computed, stored in zip(recomputed, matches):
    equal = computed["comparison_id"] == stored["comparison_id"]
    equal &= computed["terms"] == json.loads(stored["terms_json"])
    equal &= computed["hits"] == json.loads(stored["all_matches_json"])
    equal &= computed["top"] == json.loads(stored["top3_ids_json"])
    equal &= [h["posted_rank"] for h in computed["hits"][:3]] == json.loads(stored["top3_original_ranks_json"])
    equal &= len(computed["hits"]) == int(stored["total_matches"])
    equal &= computed["unfilled_slots"] == int(stored["unfilled_slots"])
    equal &= computed["unfilled_reason"] == stored["unfilled_reason"]
    check("match_" + computed["comparison_id"], equal, {"total_matches": len(computed["hits"]), "top3": computed["top"]})

expected_slots = []
for run in recomputed:
    for number in range(1, 4):
        hit = run["hits"][number - 1] if number <= len(run["hits"]) else None
        expected_slots.append({"slot_id": run["comparison_id"] + "-S" + str(number), "case_id": run["case_id"], "method": run["method"], "slot": str(number), "catalog_id": hit["catalog_id"] if hit else "", "original_rank": str(hit["posted_rank"]) if hit else "", "url": hit["url"] if hit else "", "status": "filled" if hit else run["unfilled_reason"]})
check("all_48_slots", expected_slots == slots, "Includes exact URL, original rank, and distinct empty states.")
check("dimensions", [len(requirements), len(vocabulary), len(catalog), len(matches), len(slots), len(frame)] == [8, 37, 62, 16, 48, 80], "Cases, vocabulary rows, published rows, paired comparisons, slots, frame records.")

family_stats = {}
for family in ["JSON Schema", "JSON-LD"]:
    entries = [r for r in catalog if r["family"] == family]
    family_stats[family] = {"posted_rows": len(entries), "exact_destination_urls": len(set(r["destination_url"] for r in entries)), "group_headings": dict(Counter(r["group_heading"] for r in entries)), "explicit_alias_rows": sum(bool(json.loads(r["explicit_aliases"])) for r in entries)}
    check("exact_url_unique_" + family, len(entries) == family_stats[family]["exact_destination_urls"], "No query/fragment, case, protocol, or trailing-slash canonicalization.")
    expected_fields = [[r["title"], r["function_field"]] if family == "JSON Schema" else [r["title"]] for r in entries]
    check("display_fields_" + family, expected_fields == [json.loads(r["search_fields_json"]) for r in entries], "No hidden description, destination evidence, language, or specification metadata enters matching.")

four_slots = reproduce(slot_limit=4)
dropped = reproduce(drop_mapping="LD-3-V1")
changed_four = [r["comparison_id"] for r, s in zip(recomputed, four_slots) if r["top"] != s["top"]]
changed_dropped = [r["comparison_id"] for r, s in zip(recomputed, dropped) if r["hits"] != s["hits"]]
check("slot4_retrieval_unchanged", not changed_four, changed_four)
check("drop_LD_3_V1_retrieval_unchanged", not changed_dropped, changed_dropped)

input_receipts = {}
for filename in ["requirements.json", "vocabulary.csv", "frame.csv", "catalog.csv", "matches.csv", "slots.csv", "evidence/path-plan.json"]:
    content = blob(filename)
    input_receipts[filename] = {"git_blob_sha1": git("rev-parse", STAGE2 + ":" + PREFIX + filename).decode().strip(), "committed_sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content), "crlf_count": content.count(b"\r\n")}
vocab_lf = blob("vocabulary.csv")
vocab_crlf_hash = hashlib.sha256(vocab_lf.replace(b"\n", b"\r\n")).hexdigest()
check("path_plan_vocab_hash_is_CRLF_only", vocab_crlf_hash == plan["vocabulary_sha256"], "Git LF hash differs; converting LF to CRLF exactly reproduces frozen working-tree byte hash.")
check("path_plan_catalog_hash", input_receipts["catalog.csv"]["committed_sha256"] == plan["catalog_sha256"], "Catalog was already LF.")

remote_observations = [
    {"ref": STAGE1, "path": "SCOPE.md", "blob_sha1": "7d725dbbe4f4ce1f573ff972090c8f39d861abb4"},
    {"ref": STAGE1, "path": "vocabulary.csv", "blob_sha1": "31e4da18e5e60e245d7682faf077e64720cffae5"},
    {"ref": STAGE2, "path": "SCOPE.md", "blob_sha1": "b836679ed65251b3933f1ea10b03bba5a05d87e5"},
    {"ref": STAGE2, "path": "matches.csv", "blob_sha1": "59ee4b29384251e71e28ff308f2e68cd7e62b4cc"},
    {"ref": STAGE2, "path": "catalog.csv", "blob_sha1": "6b182ef3d81ccb66fbcb949c4ec59c5b69e931c5"},
]
for observed in remote_observations:
    actual = git("rev-parse", observed["ref"] + ":" + PREFIX + observed["path"]).decode().strip()
    check("remote_blob_" + observed["ref"][:7] + "_" + observed["path"], actual == observed["blob_sha1"], "GitHub connector directly read fixed-ref content during this review; SHA compared with local Git object.")

source_stats = {}
for sourcefile in ["sources.jsonl", "evidence/catalog-pre/sources.jsonl"]:
    rows = [json.loads(line) for line in blob(sourcefile).decode().splitlines()]
    source_stats[sourcefile] = {"rows": len(rows), "source_ids": len(set(r["source_id"] for r in rows)), "raw_work_ids_including_failures": len(set(r["work_id"] for r in rows)), "status_labels": dict(Counter(r["직접열람_상태"] for r in rows))}

frame_stats = {}
for family in ["JSON Schema", "JSON-LD"]:
    records = [r for r in frame if r["domain"] == family]
    selected = [r for r in records if r["status"] == "selected"]
    frame_stats[family] = {"frame_records": len(records), "selected_ids": [r["question_id"] for r in selected], "selected_ranks": [int(r["screen_rank"]) for r in selected], "revision1_records": sum(r["revision"] == "1" for r in records), "selected_original_tag_absent": [r["question_id"] for r in selected if r["tag_at_creation"] not in ["True", "yes"]], "observed_creation_range": [min(r["created_utc"] for r in records), max(r["created_utc"] for r in records)]}

receipt = {
    "reviewer": "/root/authority_records; same-model within-team reviewer; not blinded or external",
    "checked_utc": datetime.now(timezone.utc).isoformat(),
    "stage1": STAGE1,
    "stage2": STAGE2,
    "input_receipts": input_receipts,
    "remote_observations": remote_observations,
    "scope": "Frozen input/ranking audit only. No provider destination evidence or implementation correctness judgment.",
    "counts": {"cases": 8, "pairs": len(recomputed), "catalog_rows": len(catalog), "vocabulary_rows": len(vocabulary), "vocabulary_methods": dict(Counter(v["method"] for v in vocabulary)), "unique_normalized_terms_across_cases_by_method": {m: sum(len(r["terms"]) for r in recomputed if r["method"] == m) for m in ["L", "V"]}, "slots": len(slots), "filled_slots": sum(bool(s["catalog_id"]) for s in slots), "slot_states": dict(Counter(s["status"] for s in slots)), "empty_L_cases": sum(not r["hits"] for r in recomputed if r["method"] == "L"), "empty_V_cases": sum(not r["hits"] for r in recomputed if r["method"] == "V"), "L_existing_item_displacement_denominator": sum(len(r["top"]) for r in recomputed if r["method"] == "L"), "empty_empty_ties": sum(not recomputed[i]["hits"] and not recomputed[i + 1]["hits"] for i in range(0, 16, 2))},
    "family_stats": family_stats,
    "comparisons": [{"comparison_id": r["comparison_id"], "query_count": len(r["terms"]), "total_matches": len(r["hits"]), "top3": r["top"], "all_matches": r["hits"]} for r in recomputed],
    "sensitivity": {"four_slots": {"changed_retrieval_rows": changed_four, "slot_count": 64, "filled_slots": sum(len(r["top"]) for r in four_slots), "interpretation": "Maximum match pool is one; a fourth slot has no opportunity to reveal an additional candidate."}, "remove_LD_3_V1": {"changed_retrieval_rows": changed_dropped, "changed_query_rows": [r["comparison_id"] for r, s in zip(recomputed, dropped) if r["terms"] != s["terms"]], "interpretation": "Only framing query disappears; framing was absent from all fixed display fields."}},
    "normalization_diagnostic": {"validation_matches_Validator": bounded_phrase("Validator", "validation"), "validate_matches_validation": bounded_phrase("validation", "validate"), "validation_matches_DSJSONSchemaValidation": bounded_phrase("DSJSONSchemaValidation", "validation"), "validator_schema_heading_count": sum(r["function_field"] == "Validator" for r in catalog if r["family"] == "JSON Schema"), "restriction": "No validator morphology mapping added; the heading count is post-hoc field diagnosis only."},
    "hash_discrepancy": {"frozen_path_plan_vocabulary_sha256": plan["vocabulary_sha256"], "git_LF_vocabulary_sha256": input_receipts["vocabulary.csv"]["committed_sha256"], "git_content_converted_to_CRLF_sha256": vocab_crlf_hash, "content_changed": False, "repair": "Preserve frozen plan; append committed-byte receipt."},
    "frame_stats": frame_stats,
    "source_stats_at_stage2": source_stats,
    "source_count_limit": "Different editions, components of one catalog, failed accesses, and mirrored formats must not inflate unique primary-work totals. Stage2 ledgers are intermediate, not final quota acceptance.",
    "checks": checks,
    "passed": all(c["passed"] for c in checks),
}
HERE.mkdir(parents=True, exist_ok=True)
out = HERE / "ranking-audit-receipt.json"
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"passed": receipt["passed"], "checks": len(checks), "failed": [c["check"] for c in checks if not c["passed"]], "receipt": str(out), "counts": receipt["counts"]}, ensure_ascii=False))
raise SystemExit(0 if receipt["passed"] else 1)
