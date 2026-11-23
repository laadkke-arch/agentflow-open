#!/usr/bin/env python3
"""Assemble the nine-row evidence ledger without running any target or probe.

Reads existing sealed packets, reader outputs and captured evidence only. Writes
TESTS.csv and evidence/TEST_LEDGER_NOTES.md. JSON-valued cells retain structure
and exact reader prediction strings. This is a data-assembly utility, not a test.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
PREFIX = ROOT.relative_to(REPO).as_posix()
EXPECTED_IDS = [f"{brief}-{kind}" for brief in ("SC", "MS", "SG") for kind in ("N", "E", "X")]
AUXILIARY_IDS = {"SC-E", "SC-X", "SG-N", "SG-E", "SG-X"}


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def sealed_bytes(commit, path):
    return subprocess.check_output(
        ["git", "show", f"{commit}:{PREFIX}/{path}"], cwd=REPO
    )


def reference(path, *, url=None, source_id=None, registry=None, pointer=None, role=None):
    result = {"path": path, "sha256": digest(path)}
    if url is not None:
        result["url"] = url
    if source_id is not None:
        result["source_id"] = source_id
        result["source_id_registry"] = registry or "SOURCES.jsonl"
    if pointer is not None:
        result["pointer"] = pointer
    if role is not None:
        result["role"] = role
    return result


VIEWS = list(csv.DictReader((ROOT / "VIEWS.csv").open(encoding="utf-8", newline="")))
assert len(VIEWS) == 6
VIEW = {(v["brief_id"], v["view"]): v for v in VIEWS}
assert len(VIEW) == 6
COMMON = {b: read(f"packets/{b}-common.json") for b in ("SC", "MS", "SG")}
READERS = {(b, v): read(f"readers/{b}-{v}.json") for b in COMMON for v in ("A", "B")}
MS = read("postseal/musescore/report.json")
SG = read("postseal/sigil/report.json")
AUX = read("evidence/auxiliary/observed-run-20261123/stdout.json")
RECEIPT_PATH = "evidence/auxiliary/observed-run-20261123/receipt.json"
STDOUT_PATH = "evidence/auxiliary/observed-run-20261123/stdout.json"
RECEIPT = read(RECEIPT_PATH)
PROBE_INPUTS = read("fixtures/research/probe-inputs.json")
MS_MANIFEST = {x["path"]: x for x in read("postseal/musescore/source-manifest.json")}

# Verify joins and seals before emitting derived files. No input is modified.
packet_checks = set()
reader_checks = set()
seal_checks = set()
for (b, view), v in VIEW.items():
    common_path = f"packets/{b}-common.json"
    packet_path = f"packets/{b}-{view}.json"
    reader_path = f"readers/{b}-{view}.json"
    for p, expected in ((common_path, v["common_sha256"]),
                        (packet_path, v["packet_sha256"])):
        assert digest(p) == expected, (p, "working packet hash mismatch")
        assert hashlib.sha256(sealed_bytes(v["packet_seal_sha"], p)).hexdigest() == expected
        packet_checks.add(p)
        seal_checks.add((v["packet_seal_sha"], p))
    assert digest(reader_path) == v["reader_sha256"]
    assert hashlib.sha256(sealed_bytes(v["choice_seal_sha"], reader_path)).hexdigest() == v["reader_sha256"]
    reader_checks.add(reader_path)
    seal_checks.add((v["choice_seal_sha"], reader_path))
    reader = READERS[b, view]
    assert reader["chosen_candidate"]["id"] == v["selected_id"]
    assert [x["id"] for x in reader["candidates"]] == json.loads(v["candidate_ids"])
assert RECEIPT["worker_exit_code"] == 0
assert RECEIPT["target_gui_runtime_tests_executed"] == 0
assert AUX["target_gui_runtime_tests_executed"] == 0
assert RECEIPT["all_input_bytes_unchanged_during_run"] is True
assert RECEIPT["input_hashes_before"] == RECEIPT["input_hashes_after"]
for record in RECEIPT["input_hashes_after"] + RECEIPT["output_files"]:
    assert digest(record["path"]) == record["sha256"], record["path"]
assert set(AUX["SG"]) | {"SC-E", "SC-X"} == AUXILIARY_IDS
assert MS["evidence_categories"]["unexecuted_frozen_cases"]["executed"] == 0


def prediction(reader, case_id):
    """Return exact per-candidate strings and the untouched surrounding object."""
    raw = reader["predictions"]
    if isinstance(raw, dict):
        item = raw[case_id]
        outputs = item
    else:
        item = next(p for p in raw if p.get("case_id", p.get("case")) == case_id)
        if "candidates" in item:
            outputs = {p["id"]: p["results"] for p in item["candidates"]}
        elif "candidate_results" in item:
            outputs = item["candidate_results"]
        elif "candidate_outputs" in item:
            outputs = item["candidate_outputs"]
        else:
            outputs = {c["id"]: item[c["id"]] for c in reader["candidates"]}
    assert set(outputs) == {c["id"] for c in reader["candidates"]}
    assert all(isinstance(s, str) for s in outputs.values())
    return outputs, item


def choice_provenance(b, view):
    v = VIEW[b, view]
    r = READERS[b, view]
    return {
        "view": view,
        "source_work_id": v["source_work_id"],
        "source_version": v["source_version"],
        "source_urls": json.loads(v["source_urls"]),
        "packet": reference(f"packets/{b}-{view}.json"),
        "packet_seal_commit": v["packet_seal_sha"],
        "choice": reference(f"readers/{b}-{view}.json"),
        "choice_seal_commit": v["choice_seal_sha"],
        "choice_completed_utc": v["selected_utc"],
        "chosen_candidate": r["chosen_candidate"],
        "normalized_selected_mechanism": v["normalized_selected_mechanism"],
        "seal_bytes_verified_by_ledger_assembly": True,
    }


def failures(reader, case_item):
    keys = ("failure", "failure_rule", "minimum_contrary_evidence", "reversal",
            "necessary_assumption", "assumption", "assumptions")
    result = {k: case_item[k] for k in keys if k in case_item}
    if "candidates" in case_item:
        result["candidate_failure_rules"] = {
            c["id"]: c["failure_rule"] for c in case_item["candidates"] if "failure_rule" in c
        }
    for k in ("failure_criteria", "smallest_evidence_reversing_decision"):
        if k in reader:
            result[k] = reader[k]
    if "global_reversal" in reader["chosen_candidate"]:
        result["global_reversal"] = reader["chosen_candidate"]["global_reversal"]
    return result


def ms_file(path, *, role=None):
    record = MS_MANIFEST[path]
    ref = reference(f"postseal/musescore/source/{path}", url=record["url"], role=role)
    assert ref["sha256"] == record["sha256"]
    ref["pinned_commit"] = record["commit_sha"]
    ref["git_blob_sha"] = record["git_blob_sha"]
    return ref


SG_SOURCE = {}
for container in ("postseal/sigil/pinned-originals.json", "postseal/sigil/pinned-originals-part2.json"):
    for i, record in enumerate(read(container)["files"]):
        known = next((r for r in SG["source_records"] if r["url"] == record["url"]), {})
        ref = reference(container, url=record["url"], source_id=known.get("id"),
                        registry="postseal/sigil/report.json#/source_records", pointer=f"/files/{i}")
        ref.update({"embedded_source_path": record["path"],
                    "embedded_content_sha256": hashlib.sha256(record["content"].encode()).hexdigest(),
                    "git_blob_sha": record["blob_sha"], "pinned_commit": record["ref"]})
        SG_SOURCE[record["path"]] = ref


def sc_file(path, source_id=None):
    local = f"recruitment/shotcut/source__{path.replace('/', '__')}"
    if path == "src/mainwindow.cpp":
        local = "postseal/shotcut/src__mainwindow.cpp"
    return reference(local, url=f"https://github.com/mltframework/shotcut/blob/{COMMON['SC']['sha']}/{path}",
                     source_id=source_id)


def original_tests(b, case_id):
    if b == "SC":
        return {
            "status": "NO_MATCHING_ORIGINAL_TEST_SOURCE_FOUND_IN_BOUNDED_SCAN",
            "exact_frozen_case_harness_found": False,
            "finding": "Pinned recursive tree/README/build-path inspection found EDL JavaScript and GL-widget tests but no matching proxy/relink regression input/output. Current #910 comments contain no reproducible media/project attachment or executable original test.",
            "refs": [reference("postseal/shotcut/pinned-tree.json", url=f"https://api.github.com/repos/mltframework/shotcut/git/trees/{COMMON[b]['sha']}?recursive=1"),
                     reference("postseal/shotcut/REPORT.md", pointer="Original tests/environment/execution section")],
            "limit": "Bounded search absence is not proof that the repository has no relevant tests. All SC cases are researcher-authored extensions.",
            "counts_as_target_pass": False,
        }
    if b == "MS":
        inventory = MS["evidence_categories"]["original_test_source"]["inventory"]
        chosen_ids = {
            "MS-N": ["MS-ORIGINAL-PART-CREATE", "MS-ORIGINAL-VOICE-EXCERPT", "MS-ORIGINAL-PART-UNDO", "MS-ORIGINAL-LINK-UNDO", "MS-ORIGINAL-VOICE-UNDO"],
            "MS-E": ["MS-ORIGINAL-PART-CREATE", "MS-ORIGINAL-PART-UNDO", "MS-ORIGINAL-LINK-UNDO", "MS-ORIGINAL-ELEMENT-TYPE"],
            "MS-X": ["MS-ORIGINAL-PART-UNDO", "MS-ORIGINAL-LINK-UNDO", "MS-ORIGINAL-UNDO-RESET"],
        }[case_id]
        records = []
        for item in inventory:
            if item["id"] not in chosen_ids:
                continue
            records.append({
                "id": item["id"], "id_registry": "postseal/musescore/report.json#/evidence_categories/original_test_source/inventory",
                "functions": item["functions"], "assertion": item["assertion"],
                "source": ms_file(item["source"], role="original_test_source_unexecuted"),
                "inputs": [ms_file(p, role="original_input") for p in item["input_files"]],
                "references": [ms_file(p, role="expected_output_file_not_observed_application_output") for p in item["reference_files"]],
            })
        return {"status": "RELATED_ORIGINAL_TEST_SOURCE_UNEXECUTED", "exact_frozen_case_harness_found": False,
                "records": records, "counts_as_target_pass": False,
                "limit": "Related part/link/in-session undo sources do not instantiate this exact symbolic case. Snapshot reference equality is a whole-score test oracle, not proof of a whole-state undo implementation. Stored fixtures omit transient selected flags/selection lists and persistent undo records. MS-X is not an in-session undo test."}
    return {
        "status": "RELATED_ORIGINAL_MANUAL_TEST_SOURCE_UNEXECUTED",
        "exact_frozen_case_harness_found": False,
        "source_example": reference("postseal/sigil/issue450-comments.json", url="https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520240119", pointer="comment.id=520240119", role="manual_source_between_reference_and_target"),
        "public_fixture": reference("postseal/sigil/originals/test_split2.epub.zip", url=SG["fixture"]["attachment_url"], role="historical_manual_source_marker_before_both_nodes"),
        "inner_epub": reference("postseal/sigil/originals/test_split2.epub", url=SG["fixture"]["attachment_url"]),
        "fixture_comment_url": SG["fixture"]["comment_url"],
        "golden_output_epub_found": False,
        "bounded_automated_test_scan": SG["tests_and_ci"]["source_scan"],
        "limits": ["Public reduced fixture moves link and target together; frozen SG-N/E split between them.",
                   "Present original fixture href ../Section0001.xhtml#here resolves to absent OEBPS/Section0001.xhtml; fixture bytes were preserved.",
                   "No contemporary checksum establishes attachment byte identity with 2019; fixture 0.9.17 metadata does not establish reporter build.",
                   "Plugin-framework smoke tests and dependency suites are not anchor regression tests."],
        "counts_as_target_pass": False,
    }


def execution_receipt(b):
    if b == "SC":
        return {"status": "NOT_RETRIEVED", "retrieved_execution_receipts": 0,
                "search_scope": "Pinned tree/build files and current #910 discussion/timeline; no matching original execution log, attachment output or successful reproducer found.",
                "ref": reference("postseal/shotcut/REPORT.md"),
                "limit": "Issue closure is not a test receipt. Bounded absence does not prove no historical execution occurred."}
    if b == "MS":
        value = dict(MS["evidence_categories"]["actual_historical_recorded_execution"])
        value.update({"status": "NOT_RETRIEVED", "retrieved_execution_receipts": 0,
                      "ref": reference("postseal/musescore/report.json", pointer="/evidence_categories/actual_historical_recorded_execution"),
                      "receipt_refs": [reference(f"postseal/musescore/receipts/{name}.json", source_id=f"MS-POST-{name}", registry="postseal/musescore/report.json#/source_records")
                                       for name in ("head_status", "merge_status", "head_check_runs", "head_actions")]})
        return value
    return {"status": "NOT_RETRIEVED", "retrieved_execution_receipts": 0,
            "source": SG["tests_and_ci"],
            "ref": reference("postseal/sigil/report.json", pointer="/tests_and_ci"),
            "pasted_debug_artifact": "Comment 520259623 is a maintainer-posted debug artifact retained under maintainer_report; it is not an independent or CI execution receipt for a frozen case.",
            "limit": "Zero current status/check entries, current AppVeyor shell, 405 and 404 do not prove historical builds or tests never ran."}


def maintainer_report(b):
    if b == "SC":
        return {"status": "HISTORICAL_DIAGNOSTIC_DISCUSSION_NO_SUCCESS_RECEIPT",
                "finding": "ddennedy suggested seeking/start-point/stream-order causes, Timeline Replace, and XML stream-index removal. The author still reported black output in the last inspected reply. Cause and successful recovery remain unknown.",
                "comment_ref": reference("postseal/shotcut/issue910-comments.json", url="https://github.com/mltframework/shotcut/issues/910#issuecomment-699527361", pointer="comment.id=699527361"),
                "closure_utc": "2020-09-26T07:44:43Z",
                "relation_to_frozen_case": "#910 does not report the frozen moved-original/equal-basename cases or prove the sampled-hash mechanism caused its black timeline.",
                "counts_as_target_pass": False}
    if b == "MS":
        return {"status": "CONTRIBUTOR_DESIGN_OPINION_AND_MERGED_PATCH_NO_EXECUTION_CLAIM",
                "discussion": MS["discussion"],
                "adopted_change": MS["adopted_historical_change"],
                "ref": reference("postseal/musescore/report.json", pointer="/adopted_historical_change"),
                "limit": "The merged global copy reset corresponds to the readers' competing C2/global_copy_reset scope. Adoption does not establish preservation success or causally validate either reading.",
                "counts_as_target_pass": False}
    return {"status": "HISTORICAL_MAINTAINER_AND_AUTHOR_ASSERTIONS",
            "findings": SG["historical_outcome"],
            "ref": reference("postseal/sigil/issue450-comments.json", url=COMMON[b]["request_url"]),
            "important_comment_urls": [f"https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-{i}" for i in (520240119, 520254553, 520258201, 520259623, 520649931, 520947721)],
            "repair_commit": SG["repair"].get("sha", SG["repair"].get("commit_sha", "ae60e3e63a2f9343b40d316f179b9dfbcb6d838b")),
            "relation_to_frozen_case": "Historical failure moved reference and target into one split-off file; frozen N/E separate them. Reported success in a later test build is not a frozen-case execution.",
            "counts_as_target_pass": False}


CHECKPOINT_LIMITS = {
    "SC-N": "Symbolic RED/H1 input is not a supplied project/media archive. The exact target resource, saved XML and decoded identity need a concrete fixture and native round trip.",
    "SC-E": "The stipulated BLUE-then-RED order is not observed QDir order. 'No human identity confirmation' does not decide whether generic OK/QDialog::Accepted occurs. Observe suggestion, warning icon, dialog acceptance, repair gate, producer association, p2, then saved/reopened playback separately.",
    "SC-X": "Frozen 3 MiB bytes are non-media. A full current digest without a trusted historical digest cannot prove mutation; selected A1/F refuse missing provenance. No valid decoder, proxy, metadata-copy or preview checkpoint was exercised.",
    "MS-N": "Concrete score, symbolic-ID mapping, pitch/TPC command and checkpoint assertions remain unspecified. An initially false selected bit cannot distinguish copying from clearing. With no intervening unrelated edit/stale snapshot, whole-state and scoped undo can agree.",
    "MS-E": "Immediate in-memory selected flag/Selection-list/color observation after creating P1 is necessary; frozen observe list does not explicitly bind that time. A final-only check after reopening can erase the transient distinction. Neither local/global reset nor whole/scoped rollback is distinguished by the stated successful outputs.",
    "MS-X": "Concrete reopened score/UI harness remains unspecified; current pitch62 and links are known, former pitch is absent. Do not import pitch60 from N/E. Empty history supports no-op/refusal in either snapshot or command design.",
    "SG-N": "<!--SPLIT--> is not a recognized automatic Sigil marker. A manual cursor split at the comment is only a possible harness interpretation; complete archive/wrapper and observation timing remain unspecified. Native generated _0001 name requires ordinary basename rename to requested _1.",
    "SG-E": "Same marker/archive ambiguity as SG-N plus unsupported native nested-folder move. Literal toc hrefs in snippets may not match the normalized ../Text/ch1.xhtml external-update predicate. No flatter name, external ZIP edit or changed split placement is substituted.",
    "SG-X": "Same manual-cursor/marker and archive ambiguity; duplicate IDs violate the source's uniqueness assumption. No trusted original target exists. A later unique target after mechanical splitting is not evidence of original intent.",
}
APPLICABILITY = {
    "SC-N": "CONDITIONAL_NATIVE_CASE_REQUIRES_CONCRETE_PROJECT_AND_MEDIA",
    "SC-E": "CONDITIONAL_NATIVE_CASE_ORDER_AND_DIALOG_ACCEPTANCE_UNSPECIFIED",
    "SC-X": "NOT_A_VALID_MEDIA_GUI_FIXTURE_AS_FROZEN",
    "MS-N": "CONDITIONAL_NATIVE_CASE_REQUIRES_CONCRETE_SCORE_AND_ASSERTIONS",
    "MS-E": "CONDITIONAL_NATIVE_CASE_IMMEDIATE_CREATION_CHECKPOINT_NOT_BOUND",
    "MS-X": "CONDITIONAL_NATIVE_NEGATIVE_REQUIRES_CONCRETE_REOPENED_SCORE",
    "SG-N": "CONDITIONAL_NATIVE_CASE_MANUAL_CURSOR_SPLIT_AND_ARCHIVE_WRAPPER_UNSPECIFIED",
    "SG-E": "UNSUPPORTED_NATIVE_NESTED_FOLDER_MOVE_AS_FROZEN",
    "SG-X": "CONDITIONAL_NATIVE_NEGATIVE_DUPLICATE_ID_ASSUMPTION_VIOLATION",
}
SOURCE_PREDICTIONS = {
    "SC-N": "Pinned resource-restoration paths are consistent with restoring the retained original through disabling and ordinary XML save. Active resource, decoded RED identity and save/reopen preservation were not observed.",
    "SC-E": "For the frozen order, first filename-or-hash match fills the replacement row with BLUE plus a mismatch warning icon. Later RED is skipped after filling the row. MainWindow separately requires Accepted and a corrected checker result before repaired XML save; no committed wrong relink is established. fixUnlinkedFile uses the full missing path, so indiscriminate changes to every equal basename are not supported.",
    "SC-X": "Pinned hashing reads decimal 1,000,000-byte edges for length >2,000,000; length selects the branch and is not appended to the digest. Nonempty shotcut:hash is reused. These inspected paths do not detect the stipulated unsampled-middle change. Runtime stale preview/refusal remains unobserved.",
    "MS-N": MS["frozen_cases"]["cases"][0]["discrimination"],
    "MS-E": MS["frozen_cases"]["cases"][1]["discrimination"],
    "MS-X": MS["frozen_cases"]["cases"][2]["discrimination"] + " " + MS["frozen_cases"]["cases"][2]["source_support"],
    "SG-N": SG["frozen_case_assessments"][0]["original_source_prediction"],
    "SG-E": SG["frozen_case_assessments"][1]["original_source_prediction"],
    "SG-X": SG["frozen_case_assessments"][2]["original_source_prediction"] + " " + SG["frozen_case_assessments"][2]["expected_observation_limit"],
}
POSTSEAL_RELEVANCE = {
    "SC-N": "No native trace confirms or reverses either selected candidate. Both selected proposals predict the same original-resource round trip.",
    "SC-E": "Source and narrow replay refine A0's baseline suggestion branch but do not resolve generic dialog acceptance. Both selected A1/F refuse legacy unconfirmed relocation; no A-versus-B discrimination or producer-preservation result follows.",
    "SC-X": "Auxiliary equal sampled MD5/different full SHA256 supports the narrow unsampled-input distinction. Selected A1/F both reject unverified historical provenance. That refusal diagnoses absent evidence; it does not prove a historical change was detected.",
    "MS-N": "Original expected-state files provide related scope oracles, not a native result. Global copy reset was historically merged, while both readers preferred local scope; identical frozen predictions do not establish superiority.",
    "MS-E": "Historical merge chose global copy reset. This is concrete adoption of a competing scope, not a passing test. The undefined observation checkpoint prevents a final-only check from reliably testing inherited selection. Local/global implementations and whole/scoped rollback remain undiscriminated by the stated outputs.",
    "MS-X": "Source empty-stack guard supports refusing or doing nothing with absent history. No original lost-history run was retrieved. The two chosen policies and both history mechanisms agree on refusing fabrication.",
    "SG-N": "Historical between-node source/report and pinned existing branch reduce claims that a new mechanism is needed for this normal case. The later repaired branch concerns both nodes moving together. No frozen runtime result was measured.",
    "SG-E": "Pinned fixed-folder placement and slash rejection block the frozen native operation. The planned successful paths remain hypothetical candidate outputs. The original historical bug is not reproduced by the frozen split placement.",
    "SG-X": "Source predicts later-entry overwrite if this invalid duplicate-ID input reaches the updater. The auxiliary strict resolver leaves the original target unknown. No proposed preflight refusal, rollback, or GUI behavior was executed.",
}
FOLLOWUP = {
    "SC-N": "Create a concrete valid-media project mapped to p1/H1/RED at the pinned build; record active resource, original-resource XML and decoded identity through disable/save/reopen.",
    "SC-E": "Specify candidate enumeration and distinguish no dialog acceptance from acceptance without identity confirmation; capture row/icon, Accepted/checker gate, p1/p2, proxy and saved/reopened state without changing the frozen order.",
    "SC-X": "Preserve the frozen non-media predicate case. Add any valid-media middle-change fixture as a separate follow-up, and record trusted historical provenance before replacement; do not retroactively score it as this case.",
    "MS-N": "Map m1/u1 to an executable score and actual pitch commands; assert linked pitches, tracks, P2 layout and membership at defined stages. Add any intervening-unrelated-edit comparison only as a new case.",
    "MS-E": "Make an explicit follow-up harness with an immediate post-create selected()/Selection-list/curColor checkpoint before edit/undo/reopen; preserve the frozen packet's timing ambiguity and score no retrospective pass.",
    "MS-X": "Load a concrete score with current pitch62 and an empty stack; record unavailable/no-op/refusal and unchanged membership without supplying an earlier pitch from another case.",
    "SG-N": "Specify manual cursor placement at the frozen comment, wrap a complete EPUB, and retain requested filenames via supported basename rename; then record actual split/save/reopen targets.",
    "SG-E": "Keep this native applicability defect. If testing supported flat-folder behavior or a later-version folder move, register separate inputs/version and a separate row rather than silently replacing this frozen action.",
    "SG-X": "Use an explicit native split harness to observe duplicate warning/refusal or branch behavior; keep intended target unknown. Any trusted target-selection provenance belongs to a new case.",
}


def auxiliary(case_id):
    if case_id not in AUXILIARY_IDS:
        return {"status": "NO_CASE_PREDICATE_RUN", "predicate_case_contribution": 0,
                "complete_frozen_workflow_executed": False, "target_application_executed": False,
                "note": "MuseScore source/fixture parsing and other static inspections are recorded separately; they are not part of the five-case auxiliary predicate coverage."}
    node = AUX["SG"][case_id] if case_id.startswith("SG-") else AUX[case_id]
    pointer = f"/SG/{case_id}" if case_id.startswith("SG-") else f"/{case_id}"
    return {
        "status": "AUXILIARY_PREDICATE_OBSERVED_UNSCORED",
        "predicate_case_contribution": 1,
        "classification": node["classification"],
        "stdout": reference(STDOUT_PATH, pointer=pointer),
        "receipt": reference(RECEIPT_PATH),
        "command": RECEIPT["command"], "started_utc": RECEIPT["started_utc"],
        "finished_utc": RECEIPT["finished_utc"], "worker_exit_code": RECEIPT["worker_exit_code"],
        "input_hashes_unchanged": RECEIPT["all_input_bytes_unchanged_during_run"],
        "complete_frozen_workflow_executed": False,
        "target_application_executed": False,
        "proposed_candidate_implementation_executed": False,
        "discrimination_limit": node["discrimination_limit"],
    }


def observations(case_id):
    b = case_id[:2]
    result = [{"kind": "static_source_assessment_not_runtime", "fact": SOURCE_PREDICTIONS[case_id]}]
    if case_id == "SC-E":
        node = AUX[case_id]
        result.append({"kind": "executed_auxiliary_predicate", "frozen_order": node["frozen_stipulated_order"],
                       "supplemental_reverse_order": node["supplemental_reversed_order"],
                       "dialog_gate_not_executed": node["dialog_gate"],
                       "p2": node["unrelated_p2_preservation"]})
    elif case_id == "SC-X":
        node = AUX[case_id]
        result.append({"kind": "executed_auxiliary_nonmedia_hashes",
                       "original": node["observations"]["original"],
                       "replacement": node["observations"]["replacement"],
                       "sampled_md5_equal": node["sampled_md5_equal"],
                       "full_sha256_equal": node["full_sha256_equal"],
                       "changed_bytes_sampled": node["changed_bytes_sampled"],
                       "cached_branch": node["cached_getHash_branch"],
                       "limit": "Known before/after byte pairs distinguish full hashes in this auxiliary run. A reopened legacy project with only a current full digest lacks that historical comparison; refusal is not historical change detection."})
    elif b == "SG":
        node = AUX["SG"][case_id]
        result.append({"kind": "executed_auxiliary_uri_id_inspection",
                       "original_fixture_hashes": node["original_fixture_hashes"],
                       "wrapper_body_exactly_matches_frozen_fragment": node["wrapper_body_exactly_matches_frozen_fragment"],
                       "duplicate_ids_within_document": node["duplicate_ids_within_document"],
                       "repeated_fragment_names_across_documents": node["repeated_fragment_names_across_documents"],
                       "original_uri_resolutions": node["source_scoped_original_uri_resolutions"],
                       "limit": "Strict unique-target URI predicate, not Sigil or browser duplicate-ID behavior. Mechanical layouts and candidate href queries in stdout are supplemental diagnostics; no link repair was saved."})
        result.append({"kind": "executed_static_original_archive_inspection",
                       "ref": reference("postseal/sigil/fixture-inspection-receipt.json"),
                       "fact": "Historical attachment has marker before both nodes and a literal href resolving to a missing archive member. This is not the frozen input or a target application run."})
    elif b == "MS":
        result.append({"kind": "static_original_reference_file_comparison",
                       "fact": "Breath-add expected files add two Breath elements to master/Alto with Tenor subtree unchanged; undo reference is byte-identical to input. Voice-undo expected files restore pitch/voice sequences while serialization differs. None of ten inspected fixtures stores selected or undo tags.",
                       "ref": reference("postseal/musescore/scoped-fixture-comparisons.json"),
                       "limit": "Expected-file relationships do not report an executed native test, transient UI selection, pointer identity or a preference for whole/scoped rollback."})
    result.append({"kind": "target_runtime_observation", "value": None, "reason": "TARGET_NOT_RUN"})
    return result


def source_refs(b, case_id):
    sources = [reference(f"postseal/{ {'SC':'shotcut','MS':'musescore','SG':'sigil'}[b] }/REPORT.md")]
    if b == "SC":
        sources += [reference("postseal/shotcut/issue910-comments.json", url=COMMON[b]["request_url"]),
                    reference("postseal/shotcut/fetch-receipts.json"), reference("postseal/shotcut/source-receipts.json")]
        paths = {
            "SC-N": [("src/proxymanager.cpp", "SC-CODE-src-proxymanager.cpp"), ("src/mltxmlchecker.cpp", "SC-CODE-src-mltxmlchecker.cpp")],
            "SC-E": [("src/dialogs/unlinkedfilesdialog.cpp", "SC-CODE-src-dialogs-unlinkedfilesdialog.cpp"), ("src/mainwindow.cpp", None), ("src/mltxmlchecker.cpp", "SC-CODE-src-mltxmlchecker.cpp")],
            "SC-X": [("src/util.cpp", "SC-CODE-src-util.cpp"), ("src/mltxmlchecker.cpp", "SC-CODE-src-mltxmlchecker.cpp")],
        }[case_id]
        sources.extend(sc_file(p, s) for p, s in paths)
    elif b == "MS":
        sources += [reference("postseal/musescore/report.json"),
                    reference("postseal/musescore/frozen-case-assessment.json", pointer=f"/cases/{('MS-N','MS-E','MS-X').index(case_id)}"),
                    reference("postseal/musescore/baseline-code-excerpts.json"),
                    reference("postseal/musescore/source-manifest.json"),
                    reference("postseal/musescore/runtime-availability.json"),
                    reference("postseal/musescore/scoped-fixture-comparisons.json")]
        sources += [ms_file(p) for p in ("libmscore/undo.h", "libmscore/score.cpp", "mtest/testutils.cpp")]
        sources += [reference("recruitment/musescore/source_v3.0.1/libmscore/element.cpp", source_id="MS-CODE-element.cpp", url=f"https://raw.githubusercontent.com/musescore/MuseScore/{COMMON[b]['sha']}/libmscore/element.cpp")]
    else:
        sources += [reference("postseal/sigil/report.json", pointer=f"/frozen_case_assessments/{('SG-N','SG-E','SG-X').index(case_id)}"),
                    reference("postseal/sigil/issue450-comments.json", url=COMMON[b]["request_url"]),
                    reference("postseal/sigil/fixture-inspection-receipt.json"),
                    reference("postseal/sigil/originals/fixture-inspection.json"),
                    reference("postseal/sigil/postseal-receipts.json"),
                    reference("postseal/sigil/integrity.json")]
        paths = ["src/SourceUpdates/AnchorUpdates.cpp", "src/BookManipulation/Book.cpp", "src/BookManipulation/XhtmlDoc.cpp", "src/Exporters/ExportEPUB.cpp", "src/Importers/ImportEPUB.cpp"]
        if case_id == "SG-E":
            paths += ["src/BookManipulation/FolderKeeper.cpp", "src/MainUI/OPFModel.cpp", "src/Misc/GumboInterface.cpp"]
        sources += [SG_SOURCE[p] for p in paths]
    if case_id in AUXILIARY_IDS:
        sources += [reference("evidence/auxiliary/README.md"), reference(RECEIPT_PATH),
                    reference(STDOUT_PATH, pointer=f"/SG/{case_id}" if b == "SG" else f"/{case_id}"),
                    reference("fixtures/research/probe-inputs.json")]
    return sources


rows = []
prediction_count = 0
for b in ("SC", "MS", "SG"):
    common = COMMON[b]
    for ci, case in enumerate(common["cases"]):
        cid = case["id"]
        a = READERS[b, "A"]
        z = READERS[b, "B"]
        ao, ai = prediction(a, cid)
        bo, bi = prediction(z, cid)
        aid = a["chosen_candidate"]["id"]
        bid = z["chosen_candidate"]["id"]
        prediction_count += len(ao) + len(bo)
        assert VIEW[b, "A"]["normalized_selected_mechanism"] == VIEW[b, "B"]["normalized_selected_mechanism"]
        record = {
            "test_id": cid,
            "brief_id": b,
            "case_kind": case["kind"],
            "case_origin": "RESEARCH_AUTHORED_FROZEN_AUXILIARY_SPECIFICATION",
            "target_project": common["project"],
            "target_tag": common["tag"],
            "target_commit": common["sha"],
            "request_source_id": {"SC": "SC-REQ-910", "MS": "MS-PR-4590", "SG": "SIGIL-450"}[b],
            "request_url": common["request_url"],
            "request_status": common["request_status"],
            "input_packet": f"packets/{b}-common.json",
            "input_case_pointer": f"/cases/{ci}",
            "input_sha256": digest(f"packets/{b}-common.json"),
            "input_seal_commit": VIEW[b, "A"]["packet_seal_sha"],
            "initial_state_json": case["initial"],
            "actions_json": case["actions"],
            "observable_checkpoints_json": case["observe"],
            "frozen_condition": case["condition"],
            "checkpoint_limit": CHECKPOINT_LIMITS[cid],
            "native_applicability": APPLICABILITY[cid],
            "a_selected_candidate_id": aid,
            "a_selected_prediction": ao[aid],
            "a_candidate_ids_json": [c["id"] for c in a["candidates"]],
            "a_competing_candidate_outputs_json": ao,
            "a_prediction_context_json": ai,
            "b_selected_candidate_id": bid,
            "b_selected_prediction": bo[bid],
            "b_candidate_ids_json": [c["id"] for c in z["candidates"]],
            "b_competing_candidate_outputs_json": bo,
            "b_prediction_context_json": bi,
            "selected_mechanism_relation": "SAME_NORMALIZED_MECHANISM_UNIMPLEMENTED",
            "view_choice_provenance_json": [choice_provenance(b, view) for view in ("A", "B")],
            "failure_and_reversal_evidence_json": {
                "A_sealed_criteria": failures(a, ai), "B_sealed_criteria": failures(z, bi),
                "postseal_relevance": POSTSEAL_RELEVANCE[cid],
                "observed_candidate_implementation_failure": None,
                "limit": "No selected or competing candidate implementation was executed. Failure/reversal conditions remain criteria; source counterevidence and reports are not scored candidate failures."},
            "original_test_source_json": original_tests(b, cid),
            "original_execution_receipt_json": execution_receipt(b),
            "maintainer_report_json": maintainer_report(b),
            "researcher_auxiliary_run_json": auxiliary(cid),
            "specification_prediction_json": {"status": "UNEXECUTED_CONDITIONAL_PREDICTIONS", "reader_predictions_preserved_verbatim": True,
                                               "pinned_baseline_source_assessment": SOURCE_PREDICTIONS[cid],
                                               "postseal_discriminability": POSTSEAL_RELEVANCE[cid],
                                               "counts_as_target_pass": False},
            "target_not_run": True,
            "observed_facts_json": observations(cid),
            "source_paths_hashes_urls_json": source_refs(b, cid),
            "evidence_limits_json": [common["version_limit"], CHECKPOINT_LIMITS[cid],
                                     "No native target, original target suite or proposed candidate implementation was run for this frozen case; pass/fail unknown.",
                                     "Modern reading sources, shared model family, compiler pre-exposure, unequal excerpt lengths and unmeasurable pretraining preclude a causal source-effect estimate.",
                                     "No primary requester/version-confirmed sample; these nine slots do not repair the recruitment vacancies.",
                                     "Original test source, historical reports, captured auxiliary observations and specification predictions retain separate evidence classes."],
            "case_status": "TARGET_NOT_RUN_NATIVE_ACTION_UNSUPPORTED" if cid == "SG-E" else "TARGET_NOT_RUN_NONMEDIA_FIXTURE" if cid == "SC-X" else "TARGET_NOT_RUN_HARNESS_INCOMPLETE",
            "target_execution_status": "NOT_RUN",
            "target_pass_status": "UNKNOWN_NOT_RUN",
            "target_fail_status": "UNKNOWN_NOT_RUN",
            "frozen_case_denominator_contribution": 1,
            "primary_sample_contribution": 0,
            "target_executed_contribution": 0,
            "original_execution_receipt_contribution": 0,
            "auxiliary_predicate_case_contribution": int(cid in AUXILIARY_IDS),
            "auxiliary_complete_case_contribution": 0,
            "causal_effect_denominator_contribution": 0,
            "denominator_labels_json": {
                "frozen_specifications": "1 of 9 frozen case slots; not established executable-test coverage",
                "native_execution": "0 of 9 frozen slots executed; no pass rate",
                "original_execution_receipts": "0 retrieved for these frozen cases; historical nonexecution not inferred",
                "auxiliary_predicate_scope": "5 of 9 frozen slots have narrow captured predicates; not full-test coverage",
                "full_workflow_auxiliary_coverage": "0 of 9 complete frozen workflows",
                "primary_sample": "0; auxiliary case only",
                "independent_causal_effect": "0; ineligible"},
            "minimum_followup": FOLLOWUP[cid],
        }
        rows.append(record)

assert [r["test_id"] for r in rows] == EXPECTED_IDS
assert prediction_count == 39
assert sum(r["auxiliary_predicate_case_contribution"] for r in rows) == 5
assert all(r["target_not_run"] for r in rows)
assert all(r["target_pass_status"] == r["target_fail_status"] == "UNKNOWN_NOT_RUN" for r in rows)
fields = list(rows[0])
assert all(list(r) == fields for r in rows)
output = io.StringIO(newline="")
writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
writer.writeheader()
for row in rows:
    writer.writerow({k: compact(v) if isinstance(v, (dict, list)) else str(v).lower() if isinstance(v, bool) else v for k, v in row.items()})
csv_text = output.getvalue()
roundtrip = list(csv.DictReader(io.StringIO(csv_text)))
assert len(roundtrip) == 9
assert all(len(r) == len(fields) and None not in r for r in roundtrip)
for r, source in zip(roundtrip, rows):
    for column in fields:
        if column.endswith("_json"):
            assert json.loads(r[column]) == source[column]
    for view in ("a", "b"):
        predictions = json.loads(r[f"{view}_competing_candidate_outputs_json"])
        assert predictions[r[f"{view}_selected_candidate_id"]] == r[f"{view}_selected_prediction"]
(ROOT / "TESTS.csv").write_text(csv_text, encoding="utf-8", newline="")

notes = f"""# TESTS.csv — evidence classes, joins, and denominators

`TESTS.csv` contains exactly **9 records**: SC-N/E/X, MS-N/E/X and SG-N/E/X.
It is a flat CSV evidence registry with JSON cells for structured source material.
The common packets and all six reader outputs remain unchanged.

## Counts and what they measure

| Measure | Count | Meaning |
| --- | ---: | --- |
| Frozen case slots | 9 | Three research-authored specifications per project, including applicability defects |
| Native target GUI/runtime executions | **0/9** | No native case execution; this is not a measured pass rate or a claim that all nine cases are executable as frozen |
| Native pass/fail outcomes | **Unknown for all 9** | Unknown is stored explicitly, never converted to zero failures or a passing status |
| Original execution receipts for these cases | **0** | Relevant original test source and maintainer reports are separate; bounded absence does not establish historical nonexecution |
| Cases with captured auxiliary predicates | **5/9** | SC-E, SC-X, SG-N, SG-E, SG-X only |
| Complete frozen workflows executed by the auxiliary | **0/9** | No native repair/preview/undo/split/save/reopen candidate workflow was executed |
| Sealed reader files | 6 | Three A and three B, joined by brief and view |
| Chosen candidate predictions | 18 | One A and one B prediction for each case; all unexecuted |
| All candidate-by-case predictions | **39** | SC 12, MS 12, SG 15; exact strings, not 39 observations |
| Normalized A/B mechanism agreements | 3/3 brief pairs | Both views select the same normalized mechanism in each pair; no implementation-choice change is attributed to B |
| Confirmed primary samples | 0 | Existing recruitment vacancies remain; this ledger does not fill them |
| Independent causal-effect denominator | 0 | No causal estimate, source-effect rate, author-adoption effect, or time-saving estimate |

The auxiliary worker's exit code 0 describes completion of the Python probe.
It supplies no native pass and does not alter the sealed A/B predictions.
Original-source fixture parsing in MuseScore and historical-archive inspection
in Sigil are static evidence, separately labeled in `observed_facts_json`; they
do not increase the five-case auxiliary predicate count.

## Exact joins and integrity

- `test_id` is the original `packets/*-common.json` case ID; `input_case_pointer`
  locates its original object. Initial state, actions, observation list and
  condition are copied without revisions. There are 9 case-object joins and no
  omitted, added or duplicated case IDs.
- `brief_id` joins each row to two `VIEWS.csv` rows, yielding 18 case/view joins.
  The six selected IDs are SC A1/F, MS C1/local_excerpt_reset, and
  SG C1/scoped_relocation. Candidate sets match the respective reader files.
- Selected prediction text and every competing output are copied verbatim from
  the heterogeneous reader structures. `*_prediction_context_json` also retains
  the original surrounding case object. Failure/reversal criteria are preserved
  separately from post-seal observations and source interpretations.
- `view_choice_provenance_json` retains both packet and reader paths, SHA-256,
  source work/version/URLs, choice timestamps, and seal commits. The assembly
  verified all **{len(packet_checks)} distinct packet files** and
  **{len(reader_checks)} reader files** against their VIEWS hashes and exact
  Git-sealed bytes ({len(seal_checks)} distinct commit/file comparisons).
- Input/common and view packets are sealed at
  `9518c3dccbd21cda72cec715afe47eebd4dba543`. A choices are sealed at
  `7c1df93b11e06ca8b7f44ac5b7ff996879aebd09`; B choices at
  `7bc2d1f84c04b47711d72e7c110b8f927d97f4ad`.
- Existing source IDs are retained with their registry path. Original MuseScore
  test IDs come from `postseal/musescore/report.json`; Sigil post-seal code IDs
  come from its `report.json`. Where no source ID exists, an explicit local file,
  URL and SHA-256 is supplied rather than inventing an ID. For embedded Sigil
  code, both container and embedded-content hashes are retained.
- The captured auxiliary receipt's before/after input lists agree; its input and
  output SHA-256 values match current stored bytes. The worker's stdout and
  receipt hashes are cited in each of the five affected rows. No auxiliary
  execution was repeated to construct this ledger.
- CSV readback verifies exactly 9 records and {len(fields)} columns, all JSON cells,
  and all 18 selected-prediction-to-candidate-output joins.

## Evidence columns must not be collapsed

| Column | Permitted interpretation |
| --- | --- |
| `original_test_source_json` | Existing test code, inputs and expected files, or an explicit bounded source gap. A source fixture is not an execution receipt. |
| `original_execution_receipt_json` | Retrieved historical execution evidence. None establishes a result for the frozen cases. Empty current status lists are not failed/pending historical jobs. |
| `maintainer_report_json` | Contributor/maintainer/request-author statements, posted debug material, or adopted changes. These remain reports and historical facts. |
| `researcher_auxiliary_run_json` | Captured narrow Python predicates with actual command, UTC interval, exit code and fingerprints. No target/candidate implementation ran. |
| `specification_prediction_json` | Sealed candidate predictions and later explicitly unexecuted source-derived assessments. |
| `target_not_run` | `true` in every row, together with explicit unknown native pass/fail. |
| `observed_facts_json` | Typed static-file or auxiliary observations; target runtime observations are null. |
| `source_paths_hashes_urls_json` | Evidence locators and fingerprints, not additional independent works or test counts. |

## Material case limits and reversals

| Case | Consequence for interpretation |
| --- | --- |
| SC-N | Symbolic media and no native round trip. Both chosen candidates predict the same restoration. |
| SC-E | BLUE is a warning-bearing **suggestion** only under the stipulated order. Actual enumeration is unmeasured. Native commit requires dialog acceptance and checker correction; no identity confirmation does not fix generic OK behavior. p1/p2 and save/reopen remain unobserved. |
| SC-X | Synthetic 3 MiB non-media input. Sampled MD5 is equal while full SHA-256 differs for a known before/after pair. Actual edge reads are decimal 1,000,000 bytes; file size is not digest input. A legacy binding lacking an old full digest can be refused as unverified but cannot thereby be called a detected historical change. |
| MS-N | Initially false selection does not separate inherited versus cleared selection. Whole-state and scoped rollback can agree because no unrelated change or stale snapshot intervenes. |
| MS-E | Immediate flag/list/color observation after part creation is required to test inherited UI selection. The frozen checkpoint is ambiguous; reopening can erase the distinction. Both proposed local/global fixes predict the same stated successful outputs, and no whole/scoped rollback preference follows. |
| MS-X | No stored former pitch or accessible undo record; refusal/no-op is consistent with either design. Pitch60 from the other cases must not be imported into this input. |
| SG-N | The comment marker needs an explicit manual-cursor interpretation; it is not Sigil's automatic `hr` marker. This between-node split exercises an existing branch, not the historical same-file repair. |
| SG-E | Native nested-folder move to `Text/parts/ch1_tail.xhtml` is unsupported in 0.9.17. Fixed category folders/slash rejection/import normalization are direct source constraints. No flat-name or external-ZIP substitute was used. |
| SG-X | Same-document duplicate IDs violate uniqueness assumptions; the source can collapse to the later section. The auxiliary strict resolver cannot establish FIRST versus SECOND intent. Predicted refusal was not executed. |

Sigil's later historical diagnosis moved **both reference and target together**,
unlike frozen N/E. The retained public fixture additionally has a literal href
resolving to a missing archive member and no golden output EPUB. Its metadata and
later tester statements do not establish the original reporter's build or a
frozen-case result. MuseScore's historical patch adopted **global constructor
deselection**, the competing scope to both readers' local preference; that is
adoption evidence, not proof that either implementation passed the preservation
conditions. Shotcut's closed issue retained a final author report of black
output, with cause and successful recovery unknown.

These facts constrain applicability and the strength of a proposed preference.
They do not retroactively change sealed inputs, predictions or choices. No
source report or ported predicate earns a target pass. Failure criteria and
minimum contrary evidence remain prospective where no implementation ran.

## Reproduction and scope

Run `python evidence/assemble_tests.py` from the workstream directory (or pass the
script's full path). The helper reads local evidence and Git objects, validates
the joins/hashes, and rewrites only `TESTS.csv` and this note. It makes no network
requests, launches no target application, reruns no auxiliary probe, changes no
sealed input, and creates no commit. The ledger is a structured evidence export;
no workbook formula or native application outcome is implied by CSV generation.

The capture interval and runtime details remain those in the existing auxiliary
receipt; assembly time is not substituted for execution time. The output CSV
SHA-256 is `{hashlib.sha256(csv_text.encode()).hexdigest()}`.
"""
(ROOT / "evidence/TEST_LEDGER_NOTES.md").write_text(notes, encoding="utf-8")
print(compact({"rows": len(rows), "columns": len(fields), "ids": EXPECTED_IDS,
               "native_executions": 0, "native_pass_fail": "unknown for all 9",
               "auxiliary_predicate_cases": sorted(AUXILIARY_IDS), "auxiliary_complete_cases": 0,
               "chosen_predictions": 18, "candidate_predictions": prediction_count,
               "packet_files_verified": len(packet_checks), "reader_files_verified": len(reader_checks),
               "seal_comparisons": len(seal_checks), "csv_sha256": digest("TESTS.csv")}))
