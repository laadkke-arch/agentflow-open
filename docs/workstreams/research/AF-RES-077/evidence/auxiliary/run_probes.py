#!/usr/bin/env python3
"""Unscored AF-RES-077 auxiliary predicates, never Shotcut/Sigil runtime tests.

Run --prepare-inputs once to materialize exact textual input fixtures. Then run
--record-run LABEL to capture a separate worker's stdout, stderr, and exit code.
Everything written stays below evidence/auxiliary/ or fixtures/research/.
"""

import argparse
import hashlib
import json
import platform
import posixpath
import shlex
import subprocess
import sys
import tempfile
import traceback
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[2]
AUX = ROOT / "evidence/auxiliary"
FIXTURES = ROOT / "fixtures/research"
DESCRIPTOR = FIXTURES / "probe-inputs.json"
MIB = 1024 * 1024
SAMPLE = 1_000_000
SOURCE_INPUTS = [
    "packets/SC-common.json",
    "packets/SG-common.json",
    "recruitment/shotcut/source__src__util.cpp",
    "recruitment/shotcut/source__src__dialogs__unlinkedfilesdialog.cpp",
    "postseal/shotcut/src__mainwindow.cpp",
]
WRAPPER_PREFIX = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                  '<html xmlns="http://www.w3.org/1999/xhtml">'
                  '<head><title>AF-RES-077 research fragment</title></head><body>')
WRAPPER_SUFFIX = '</body></html>\n'
LIMITS = [
    "Post-seal, research-authored auxiliary observations; excluded from all sealed A/B scores.",
    "Python standard-library execution only; neither pinned Qt application nor its unit tests was executed.",
    "SC-X is synthetic non-media bytes and a success-path Python transcription of the sampled-hash branch, not valid media, a GUI reproduction, or proxy preview evidence.",
    "SC-E replays one unresolved row and stipulated candidate order with symbolic hashes; it does not measure QDir enumeration, UI interaction, project repair, p2 preservation, proxy creation, or save/reopen.",
    "SG uses literal input fragments, XML parsing, and a strict unique-target URI resolver; it does not execute Sigil, build an EPUB, repair links, or save/reopen a book.",
    "A mechanical in-memory split without link rewriting and candidate href queries are diagnostic counterfactuals, not application output or a complete Sigil fix.",
    "An auxiliary assertion checks this probe's input or arithmetic; it is never a target GUI/runtime pass.",
]


def now():
    return datetime.now(timezone.utc).isoformat()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def fingerprint(path):
    data = Path(path).read_bytes()
    return {"path": relative(path), "size_bytes": len(data), "sha256": sha256(data)}


def case(packet, name):
    return next(item for item in packet["cases"] if item["id"] == name)


def write_exact_or_verify(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f"Refusing to overwrite a different existing input: {path}")
    else:
        path.write_bytes(data)


def prepare_inputs():
    sc = load(ROOT / "packets/SC-common.json")
    sg = load(ROOT / "packets/SG-common.json")
    descriptor = {
        "schema": "AF-RES-077-auxiliary-inputs-v1",
        "classification": "postseal_research_auxiliary_unscored",
        "sealed_packets_edited": False,
        "pinned_projects": {"SC": {k: sc[k] for k in ("project", "tag", "sha")},
                            "SG": {k: sg[k] for k in ("project", "tag", "sha")}},
        "source_inputs": [fingerprint(ROOT / path) for path in SOURCE_INPUTS],
        "SC-X": {
            "frozen_case": case(sc, "SC-X"),
            "exact_generator": {
                "block_bytes": MIB, "file_bytes": 3 * MIB,
                "encoding": "one ASCII byte repeated block_bytes times per block",
                "original_blocks": ["A", "B", "C"],
                "replacement_blocks": ["A", "D", "C"],
                "same_temporary_path_replaced_sequentially": True,
                "large_binary_files_retained": False,
            },
            "hash_recipe": {"algorithm": "MD5", "large_file_threshold_bytes": 2 * SAMPLE,
                            "edge_read_bytes": SAMPLE, "file_size_in_digest": False,
                            "full_content_comparator": "SHA-256"},
        },
        "SC-E": {"frozen_case": case(sc, "SC-E"),
                 "reverse_order": "supplemental_unscored_counterexample_only",
                 "candidate_hashes": "symbolic frozen input values, not hashes of media files"},
        "SG": {
            "wrapper_prefix": WRAPPER_PREFIX, "wrapper_suffix": WRAPPER_SUFFIX,
            "fragment_policy": "Exact decoded JSON string inserted unchanged between wrappers; no unescaping, reserialization, or body edits.",
            "cases": {},
        },
    }
    for item in sg["cases"]:
        documents = []
        for document_path, fragment in item["initial"].items():
            if not document_path.endswith(".xhtml"):
                continue
            path = FIXTURES / item["id"] / "original" / document_path
            data = (WRAPPER_PREFIX + fragment + WRAPPER_SUFFIX).encode("utf-8")
            write_exact_or_verify(path, data)
            documents.append({"document_path": document_path, "fixture": fingerprint(path),
                              "original_fragment": fragment,
                              "fragment_sha256": sha256(fragment.encode("utf-8"))})
        descriptor["SG"]["cases"][item["id"]] = {
            "frozen_case": item, "document_order": [d["document_path"] for d in documents],
            "documents": documents,
        }
    write_exact_or_verify(DESCRIPTOR, json_bytes(descriptor))
    return {"prepared_paths": [relative(DESCRIPTOR)] +
            [d["fixture"]["path"] for c in descriptor["SG"]["cases"].values()
             for d in c["documents"]]}


def verify_inputs():
    descriptor = load(DESCRIPTOR)
    for expected in descriptor["source_inputs"]:
        if fingerprint(ROOT / expected["path"]) != expected:
            raise ValueError(f"Pinned source/packet changed: {expected['path']}")
    for item in descriptor["SG"]["cases"].values():
        for doc in item["documents"]:
            path = ROOT / doc["fixture"]["path"]
            if fingerprint(path) != doc["fixture"]:
                raise ValueError(f"Text fixture changed: {path}")
            expected = WRAPPER_PREFIX + doc["original_fragment"] + WRAPPER_SUFFIX
            if path.read_bytes() != expected.encode("utf-8"):
                raise ValueError(f"Original body fragment not preserved: {path}")
    return descriptor


def sampled_md5(path):
    """Pinned getFileHash successful open/seek/read path; size is not hashed."""
    size = path.stat().st_size
    with path.open("rb") as stream:
        if size > SAMPLE * 2:
            first = stream.read(SAMPLE)
            stream.seek(size - SAMPLE)
            last = stream.read()
            data = first + last
            ranges = [[0, len(first)], [size - SAMPLE, size - SAMPLE + len(last)]]
        else:
            data = stream.read()
            ranges = [[0, len(data)]]
    return {"md5": hashlib.md5(data).hexdigest(), "file_size_bytes": size,
            "logical_content_bytes_read": len(data), "ranges_half_open": ranges,
            "file_size_bytes_in_digest": 0}


def full_sha256(path):
    digest = hashlib.sha256()
    read_bytes = 0
    with path.open("rb") as stream:
        while chunk := stream.read(MIB):
            read_bytes += len(chunk)
            digest.update(chunk)
    return {"sha256": digest.hexdigest(), "logical_content_bytes_read": read_bytes}


def sc_x_probe(descriptor):
    spec = descriptor["SC-X"]["exact_generator"]
    records = {}
    with tempfile.TemporaryDirectory(prefix="SC-X-", dir=FIXTURES) as directory:
        path = Path(directory) / "same-path.bin"
        for revision in ("original", "replacement"):
            blocks = spec[revision + "_blocks"]
            with path.open("wb") as stream:
                for character in blocks:
                    stream.write(character.encode("ascii") * spec["block_bytes"])
            assert path.stat().st_size == spec["file_bytes"] == 3_145_728
            records[revision] = {"blocks": blocks, "temporary_path": relative(path),
                                 "sampled": sampled_md5(path), "full": full_sha256(path)}
        temporary_path = relative(path)
    original, replacement = records["original"], records["replacement"]
    cached = original["sampled"]["md5"]
    return {
        "case": "SC-X", "classification": "python_reimplementation_auxiliary",
        "source": "recruitment/shotcut/source__src__util.cpp:383-421",
        "observations": records,
        "same_path_replaced": original["temporary_path"] == replacement["temporary_path"],
        "sampled_md5_equal": cached == replacement["sampled"]["md5"],
        "full_sha256_equal": original["full"]["sha256"] == replacement["full"]["sha256"],
        "changed_range_half_open": [MIB, 2 * MIB],
        "unsampled_range_half_open": [SAMPLE, 3 * MIB - SAMPLE],
        "changed_bytes_sampled": 0,
        "cached_getHash_branch": {"stipulated_cached_value": cached,
                                  "returned_value": cached, "logical_content_bytes_read": 0,
                                  "reason": "Non-empty shotcut:hash bypasses recomputation in the pinned guard; no Mlt::Properties object was executed."},
        "cost_scope": "Returned content-byte counts per Python hash call, not physical I/O, page-cache traffic, elapsed time, Qt performance, metadata I/O, or hashing security claims.",
        "large_temporary_binary_removed": not (ROOT / temporary_path).exists(),
        "temporary_directory_removed": not Path(directory).exists(),
        "target_gui_runtime_executed": False,
        "discrimination_limit": "Distinguishes the stipulated sampled/cache check from a fresh full-content digest on these bytes. It cannot choose A versus B when both selected proposals invalidate/recompute full content, share the same sample shortcut, or differ only in unexecuted preview/commit behavior.",
    }


def replay_candidate_order(initial, candidates, label):
    missing_basename = posixpath.basename(initial["missing"])
    replacement_hash = None
    selected = None
    trace = []
    for index, candidate in enumerate(candidates):
        if replacement_hash is not None:
            trace.append({"index": index, "candidate": candidate, "evaluated": False,
                          "reason": "One-row replay already returned when outstanding became zero; a populated replacement hash also fails the unresolved-row guard on a later call."})
            continue
        hash_match = candidate["hash"] == initial["stored_hash"]
        filename_match = posixpath.basename(candidate["path"]) == missing_basename
        matches = hash_match or filename_match
        entry = {"index": index, "candidate": candidate, "evaluated": True,
                 "hash_match": hash_match, "filename_match": filename_match,
                 "hash_OR_filename": matches}
        if matches:
            selected = dict(candidate)
            replacement_hash = candidate["hash"]
            selected["warning_icon"] = not hash_match
            selected["decoration_role_icon"] = (
                ":/icons/oxygen/32x32/status/task-complete.png" if hash_match else
                ":/icons/oxygen/32x32/status/task-attempt.png")
            entry["effect"] = "Set replacement suggestion/hash in dialog model; outstanding becomes zero and lookInDir returns false."
        trace.append(entry)
    return {"order_classification": label, "input_order": [c["path"] for c in candidates],
            "suggested_replacement": selected, "trace": trace,
            "warning_kind": "Qt DecorationRole icon only; no human identity confirmation observed",
            "actual_directory_enumeration_tested": False, "project_commit_observed": False}


def sc_e_probe(descriptor):
    initial = descriptor["SC-E"]["frozen_case"]["initial"]
    candidates = initial["candidate_order"]
    return {
        "case": "SC-E", "classification": "bounded_predicate_replay_auxiliary",
        "source": "recruitment/shotcut/source__src__dialogs__unlinkedfilesdialog.cpp:85-132",
        "frozen_stipulated_order": replay_candidate_order(initial, candidates, "frozen_input_order"),
        "supplemental_reversed_order": replay_candidate_order(initial, list(reversed(candidates)),
                                                              "supplemental_unscored_counterexample"),
        "frozen_input_mutated": False,
        "dialog_gate": {
            "source": "postseal/shotcut/src__mainwindow.cpp:1082-1092",
            "required": "dialog.exec() == QDialog::Accepted, then checker.check(fileName) && checker.isCorrected() before saveRepairedXmlFile",
            "dialog_executed": False, "QDialog_Accepted_observed": False,
            "checker_executed": False, "repair_or_save_observed": False,
            "no_human_identity_confirmation": "A warning suggestion is observable in this replay; the frozen lack of confirmation does not establish that the real dialog was accepted or that p1 was changed.",
        },
        "unrelated_p2_preservation": "unmeasured; retained only as a frozen input annotation",
        "target_gui_runtime_executed": False,
        "discrimination_limit": "Can expose order-sensitive first filename-or-hash suggestion. It cannot distinguish selected A/B proposals that both reject filename-only candidates or require confirmation; no proposed remedy or downstream project mutation is executed.",
    }


def parse_document(text):
    root = ET.fromstring(text)
    ids = defaultdict(list)
    links = []
    for ordinal, element in enumerate(root.iter()):
        if "id" in element.attrib:
            ids[element.attrib["id"]].append({"text": "".join(element.itertext()),
                                               "element_ordinal": ordinal,
                                               "tag": element.tag.rsplit("}", 1)[-1]})
        if element.tag.rsplit("}", 1)[-1] == "a" and "href" in element.attrib:
            links.append({"href": element.attrib["href"], "link_text": "".join(element.itertext())})
    return {"ids": dict(ids), "links": links}


def resolve_href(documents, source_document, href):
    """Fixture-local URI parsing; strict uniqueness, no browser selection rules."""
    resolved_uri = urljoin("https://auxiliary.invalid/" + source_document, href)
    parts = urlsplit(resolved_uri)
    target_document = posixpath.normpath(unquote(parts.path).lstrip("/"))
    fragment = unquote(parts.fragment)
    assert parts.scheme == "https" and parts.netloc == "auxiliary.invalid"
    matches = documents.get(target_document, {}).get("ids", {}).get(fragment, [])
    if target_document not in documents:
        status = "target_document_missing"
    elif not matches:
        status = "target_fragment_missing"
    elif len(matches) == 1:
        status = "unique_target"
    else:
        status = "ambiguous_duplicate_ids_in_target_document"
    return {"source_document": source_document, "href": href,
            "parsed_target_document": target_document, "parsed_fragment": fragment,
            "status": status, "target_matches": matches,
            "chosen_text": matches[0]["text"] if len(matches) == 1 else None}


def all_resolutions(documents):
    return [dict(resolve_href(documents, path, link["href"]), link_text=link["link_text"])
            for path, parsed in documents.items() for link in parsed["links"]]


def sg_case_probe(identifier, spec):
    documents = {doc["document_path"]: parse_document((ROOT / doc["fixture"]["path"]).read_text(encoding="utf-8"))
                 for doc in spec["documents"]}
    by_bare_id = defaultdict(list)
    within = []
    for path, parsed in documents.items():
        for fragment, entries in parsed["ids"].items():
            by_bare_id[fragment].extend(dict(entry, document=path) for entry in entries)
            if len(entries) > 1:
                within.append({"document": path, "id": fragment, "count": len(entries),
                               "texts": [e["text"] for e in entries]})
    across = [{"id": key, "documents": sorted({entry["document"] for entry in entries})}
              for key, entries in by_bare_id.items()
              if len({entry["document"] for entry in entries}) > 1]
    original_resolutions = all_resolutions(documents)
    # This deliberately lossy example is not a reproduction of Sigil/QHash order.
    last_wins = {key: entries[-1] for key, entries in by_bare_id.items()}
    lossy_queries = []
    for result in original_resolutions:
        bare_id = unquote(urlsplit(result["href"]).fragment)
        lossy_queries.append({"source_document": result["source_document"],
                              "href": result["href"], "discarded_document_scope": True,
                              "bare_id": bare_id, "illustrative_last_wins_target": last_wins.get(bare_id)})
    original_fragments = {d["document_path"]: d["original_fragment"] for d in spec["documents"]}
    head, tail = original_fragments["Text/ch1.xhtml"].split("<!--SPLIT-->")
    tail_path = "Text/parts/ch1_tail.xhtml" if identifier == "SG-E" else "Text/ch1_1.xhtml"
    layout_fragments = dict(original_fragments)
    layout_fragments["Text/ch1.xhtml"] = head
    layout_fragments[tail_path] = tail
    layout = {path: parse_document(WRAPPER_PREFIX + fragment + WRAPPER_SUFFIX)
              for path, fragment in layout_fragments.items()}
    candidate_queries = []
    for result in original_resolutions:
        if result["status"] != "unique_target":
            candidate_queries.append({"source_document": result["source_document"],
                                      "old_href": result["href"], "candidate_href": None,
                                      "reason": "No unique trusted pre-edit document+fragment target; no preservation choice is inferred."})
            continue
        old_target = result["parsed_target_document"]
        fragment = result["parsed_fragment"]
        target = old_target
        if old_target == "Text/ch1.xhtml" and fragment in layout[tail_path]["ids"]:
            target = tail_path
        href = posixpath.relpath(target, posixpath.dirname(result["source_document"])) + "#" + fragment
        candidate_queries.append({"source_document": result["source_document"],
                                  "old_href": result["href"], "candidate_href": href,
                                  "classification": "expected_location_query_only_not_applied_fix",
                                  "resolver_observation": resolve_href(layout, result["source_document"], href)})
    return {
        "case": identifier, "classification": "original_input_uri_and_id_predicates_auxiliary",
        "original_fixture_hashes": [doc["fixture"] for doc in spec["documents"]],
        "wrapper_body_exactly_matches_frozen_fragment": True,
        "duplicate_ids_within_document": within,
        "repeated_fragment_names_across_documents": across,
        "source_scoped_original_uri_resolutions": original_resolutions,
        "bare_global_id_demo": {
            "purpose": "Demonstrate information loss when path scope is discarded; not Sigil's exact QHash iteration or update execution.",
            "document_order": list(documents), "collision_preserving_index": dict(by_bare_id),
            "illustrative_single_value_policy": "last wins in this explicit input document/element order",
            "queries": lossy_queries,
        },
        "mechanical_layout_only": {
            "classification": "in_memory_counterfactual_without_href_rewriting",
            "split_target": tail_path,
            "split_target_provenance": "Frozen action specifies tail path" if identifier != "SG-X" else "Auxiliary diagnostic assumption only; SG-X does not freeze a post-split filename",
            "href_queries": all_resolutions(layout),
            "expected_location_queries": candidate_queries,
            "files_saved_or_application_executed": False,
            "SG_X_warning": "Even if the mechanical post-split #fn query now finds FIRST uniquely, the original document had FIRST and SECOND under one id; that later uniqueness does not establish preservation of the intended target." if identifier == "SG-X" else None,
        },
        "target_gui_runtime_executed": False,
        "discrimination_limit": (
            "Both selected A/B solutions may preserve unique source-scoped identity and produce the same candidate paths; this resolver does not execute either."
            if identifier != "SG-X" else
            "Neither document scope nor unchanged file bytes/digests recover a trusted choice between FIRST and SECOND. Refusal and explicit user disambiguation remain alternatives; no implementation or preference among A/B is tested."),
    }


def run_worker():
    descriptor = verify_inputs()
    result = {
        "schema": "AF-RES-077-auxiliary-observations-v1", "observed_utc": now(),
        "classification": "postseal_unscored_research_auxiliary",
        "input_descriptor": fingerprint(DESCRIPTOR),
        "limits": LIMITS, "target_gui_runtime_tests_executed": 0,
        "sealed_A_B_pass_counts_changed": False,
        "SC-X": sc_x_probe(descriptor), "SC-E": sc_e_probe(descriptor),
        "SG": {key: sg_case_probe(key, value) for key, value in descriptor["SG"]["cases"].items()},
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def input_fingerprints():
    files = [Path(__file__).resolve(), DESCRIPTOR] + [ROOT / path for path in SOURCE_INPUTS]
    files += sorted(FIXTURES.glob("SG-*/original/**/*.xhtml"))
    return [fingerprint(path) for path in files]


def git_value(*args):
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def record_run(label):
    if not label or Path(label).name != label or label in {".", ".."}:
        raise ValueError("Use a single directory name as the run label")
    output = AUX / label
    output.mkdir(exist_ok=False)
    before = input_fingerprints()
    command = [sys.executable, str(Path(__file__).resolve()), "--worker"]
    started = now()
    worker = subprocess.run(command, cwd=ROOT, capture_output=True, check=False)
    ended = now()
    stdout = output / "stdout.json"
    stderr = output / "stderr.txt"
    stdout.write_bytes(worker.stdout)
    stderr.write_bytes(worker.stderr)
    after = input_fingerprints()
    receipt_path = output / "receipt.json"
    receipt = {
        "schema": "AF-RES-077-auxiliary-receipt-v1", "classification": "postseal_unscored_research_auxiliary",
        "supervisor_command": shlex.join([sys.executable, str(Path(__file__).resolve()), "--record-run", label]),
        "command": shlex.join(command), "argv": command, "cwd": str(ROOT),
        "started_utc": started, "finished_utc": ended,
        "interpreter": {"executable": sys.executable, "version": sys.version,
                        "implementation": platform.python_implementation(), "platform": platform.platform()},
        "worker_exit_code": worker.returncode,
        "exit_code_provenance": "subprocess.CompletedProcess.returncode from the captured worker, not inferred from stdout",
        "workspace_git_head_at_receipt": git_value("rev-parse", "HEAD"),
        "workspace_git_branch_at_receipt": git_value("branch", "--show-current"),
        "input_hashes_before": before, "input_hashes_after": after,
        "all_input_bytes_unchanged_during_run": before == after,
        "output_files": [fingerprint(stdout), fingerprint(stderr)],
        "receipt_path": relative(receipt_path),
        "receipt_self_hash": "not embedded because it would be self-referential",
        "transient_binary_input_hashes": "Recorded separately for original/replacement under stdout.json / SC-X / observations / full / sha256; generator is in probe-inputs.json.",
        "target_gui_runtime_tests_executed": 0, "sealed_scores_updated": False,
        "limits": LIMITS,
    }
    receipt_path.write_bytes(json_bytes(receipt))
    print(json.dumps({"worker_exit_code": worker.returncode, "receipt": relative(receipt_path),
                      "stdout": relative(stdout), "stderr": relative(stderr),
                      "inputs_unchanged": before == after}, indent=2))
    return worker.returncode if before == after else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prepare-inputs", action="store_true")
    group.add_argument("--record-run", metavar="LABEL")
    group.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.prepare_inputs:
        print(json.dumps(prepare_inputs(), indent=2))
        return 0
    if args.record_run:
        return record_run(args.record_run)
    run_worker()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        traceback.print_exc(file=sys.stderr)
        print(json.dumps({"auxiliary_probe_error": str(error), "target_runtime_pass": False}))
        sys.exit(1)
