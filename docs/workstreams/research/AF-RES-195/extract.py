#!/usr/bin/env python3
"""Inventory frozen DivEMT archives and reconcile de-identified segment records."""

import argparse
import ast
import csv
import hashlib
import io
import json
import logging
import os
import platform
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile
import zlib
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Optional


UPSTREAM = "934c4106001adeaa982a882d063f33ce0a398217"
PRIOR = "a5d9b2cc5f295fe5cb15764e3965c14326c872d9"
PRIOR_DIR = "docs/workstreams/research/AF-RES-181"
GITHUB = f"https://github.com/gsarti/divemt/blob/{UPSTREAM}"
HF_REV = "9abd1d1cea118ad7a9946e7f1f5a1a29c2a01762"
HF_URL = f"https://huggingface.co/datasets/GroNLP/divemt/resolve/{HF_REV}/main.tsv"
HF_HASH = "d54867ff860c36a24649266b54d7638a7d503d74ce98a71627af180d92b2f8d9"
LANGUAGES = ("ita", "tur")
CONDITIONS = ("ht", "pe1", "pe2")
JOB = re.compile(r"flores101-(main|warmup)-(ita|tur)-(\d+)-(ht|pe[12]?)")
PERSON = re.compile(r"(ita|tur)/(t\d+)_(main|warmup)/[^/]+")
BACKUP = re.compile(r"\.per\.(\d+)$")
INVENTORY_FIELDS = (
    "language archive_url entry_index entry kind revision bytes compressed_bytes crc32 sha256 "
    "zip_read xml_parse phase doc_id condition subject_id job_id job_status progress "
    "units unit_status_counts key_issue"
).split()
FRAME_FIELDS = (
    "row_kind slot_id language phase doc_rank doc_id condition subject_id status "
    "case_reason raw_entries planned_entries assignment_basis zip_url source_ids"
).split()
SOURCE_PATHS = (
    "README.md", "divemt/parse_utils.py", "scripts/preprocess.py", "notebooks/analysis.ipynb",
    "notebooks/modeling.Rmd", "divemt/qe_taggers.py", "divemt/wmt22qe_utils.py",
)


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def entry_kind(info):
    if info.is_dir():
        return "directory", None
    if info.filename.endswith(".per"):
        return "per", None
    if info.filename.endswith(".pej"):
        return "pej", None
    backup = BACKUP.search(info.filename)
    if backup:
        return "per_backup", int(backup[1])
    return "other", None


def census_entry(archive, info, index, language):
    kind, revision = entry_kind(info)
    data = dict(
        language=language, archive_url=f"{GITHUB}/data/raw/{language}.zip",
        entry_index=index, entry=info.filename, kind=kind, revision=revision,
        bytes=info.file_size, compressed_bytes=info.compress_size, crc32=f"{info.CRC:08x}",
        zip_read="directory" if info.is_dir() else "unread", xml_parse="not_applicable",
    )
    if info.is_dir():
        return data
    try:
        body = archive.read(info)
    except (zipfile.BadZipFile, OSError, RuntimeError) as error:
        return data | dict(zip_read=type(error).__name__, key_issue="entry_read_failed")
    data.update(sha256=sha_bytes(body), zip_read="crc_ok")
    if kind == "other":
        return data
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return data | dict(xml_parse="invalid_xml", key_issue="xml_parse_failed")
    units = root.findall("task" if kind == "pej" else "unit")
    data.update(
        xml_parse="parsed", job_status=root.get("status", "unset"), progress=root.get("progress"),
        units=len(units), unit_status_counts=";".join(
            f"{key}:{count}" for key, count in sorted(Counter(u.get("status", "unset") for u in units).items())
        ),
    )
    job = JOB.fullmatch(root.get("id", ""))
    person = PERSON.fullmatch(info.filename)
    if root.tag != "job" or not job or not person or (job[2], job[1]) != (person[1], person[3]):
        return data | dict(key_issue="unresolved_job_or_folder_key")
    condition = job[4]
    if condition == "pe":
        providers = {unit.find("MT").get("producer") for unit in units if unit.find("MT") is not None}
        condition = {"1": "pe1", "2": "pe2"}.get(next(iter(providers))) if len(providers) == 1 else None
    return data | dict(
        phase=job[1], doc_id=int(job[3]), condition=condition,
        subject_id=f"{language}_{person[2]}", job_id=job[0],
        key_issue="" if condition else "unresolved_pe_provider",
    )


def collect_archive(upstream, language):
    path = upstream / "data" / "raw" / f"{language}.zip"
    relpath = str(path.relative_to(upstream))
    tree = git(upstream, "ls-tree", "--long", "HEAD", "--", relpath).decode().strip()
    mode, kind, git_blob, blob_size = tree.split("\t")[0].split()
    with path.open("rb") as stream:
        start = stream.read(80)
    if start.startswith(b"version https://git-lfs.github.com/spec/v1"):
        raise ValueError(f"{relpath} is a Git LFS pointer")
    if git(upstream, "hash-object", relpath).decode().strip() != git_blob:
        raise ValueError(f"{relpath} does not match the pinned Git blob")
    with zipfile.ZipFile(path) as archive:
        rows = [census_entry(archive, info, index, language) for index, info in enumerate(archive.infolist(), 1)]
    valid = [row for row in rows if row.get("phase") and row.get("condition")]
    docs = sorted({row["doc_id"] for row in valid if row["phase"] == "main" and row["kind"] in ("per", "pej")})
    names = Counter(row["entry"] for row in rows)
    per = [row for row in rows if row["kind"] == "per"]
    main_counts = Counter((row["doc_id"], row["condition"]) for row in valid if row["phase"] == "main" and row["kind"] == "per")
    return rows, dict(
        path=relpath, url=f"{GITHUB}/{relpath}", sha256=sha_file(path), bytes=path.stat().st_size,
        git_blob=git_blob, git_blob_bytes=int(blob_size), git_mode=mode, git_kind=kind,
        lfs_pointer=False, zip_entries=len(rows), kinds=dict(Counter(row["kind"] for row in rows)),
        zip_read=dict(Counter(row["zip_read"] for row in rows)),
        xml_parse=dict(Counter(row["xml_parse"] for row in rows)),
        canonical_per_status=dict(Counter(row.get("job_status", "unknown") for row in per)),
        canonical_per_phase=dict(Counter(row.get("phase", "unknown") for row in per)),
        main_doc_ids=docs, selected_doc_ids=docs[:4],
        duplicate_zip_names={name: count for name, count in names.items() if count > 1},
        key_issues=dict(Counter(row["key_issue"] for row in rows if row.get("key_issue"))),
        canonical_main_condition_gaps=sum(main_counts[(doc, condition)] == 0 for doc in docs for condition in CONDITIONS),
        canonical_main_condition_multiplicity=sum(count > 1 for count in main_counts.values()),
    )


def position(language, doc_id, condition):
    return f"{language}-{doc_id}-{condition}"


def locators(rows):
    return "\n".join(f"{row['entry_index']}:{row['entry']}" for row in rows)


def cohort(rows, language, docs):
    per_by_slot = defaultdict(list)
    input_by_slot = defaultdict(list)
    positions = {doc: rank for rank, doc in enumerate(docs, 1)}
    for row in rows:
        if row.get("phase") != "main":
            continue
        key = (row["doc_id"], row["condition"])
        if row["kind"] == "per":
            per_by_slot[key].append(row)
        elif row["kind"] == "pej":
            input_by_slot[key].append(row)
    url = f"{GITHUB}/data/raw/{language}.zip"
    frame = []
    for rank in range(1, 5):
        doc = docs[rank - 1] if rank <= len(docs) else None
        for condition in CONDITIONS:
            raw = per_by_slot[(doc, condition)]
            planned = input_by_slot[(doc, condition)]
            status = "included" if raw else "missing_canonical_per"
            if doc is None:
                status = "missing_main_doc_rank"
            elif len(raw) > 1:
                status = "included_ambiguous_multiple_canonical_per"
            frame.append(dict(
                row_kind="planned_slot", slot_id=position(language, doc or f"rank{rank}", condition),
                language=language, phase="main", doc_rank=rank, doc_id=doc, condition=condition,
                subject_id=";".join(sorted({row["subject_id"] for row in raw + planned})),
                status=status, case_reason="first four numeric main doc IDs; all canonical states retained",
                raw_entries=locators(raw), planned_entries=locators(planned), zip_url=url,
                assignment_basis="PEJ folder/job/provider" if planned else "design slot only",
                source_ids=";".join(f"RAW-{language.upper()}-{r['entry_index']:04d}" for r in raw),
            ))
    for row in rows:
        if row["kind"] not in ("per", "per_backup", "pej"):
            continue
        phase, doc = row.get("phase"), row.get("doc_id")
        if row.get("key_issue"):
            status = "unresolved_entry"
        elif phase == "warmup":
            status = "excluded_warmup"
        elif doc not in positions:
            status = "excluded_main_rank_gt4"
        elif row["kind"] == "per":
            continue
        elif row["kind"] == "pej":
            status = "assignment_corroboration"
        else:
            status = "revision_diagnostic"
        # Keep canonical cut reasons plus all in-scope and unresolved auxiliary records.
        if row["kind"] != "per" and status.startswith("excluded"):
            continue
        frame.append(dict(
            row_kind=row["kind"], language=language, phase=phase, doc_id=doc,
            doc_rank=positions.get(doc), condition=row.get("condition"), subject_id=row.get("subject_id"),
            slot_id=position(language, doc, row.get("condition")) if doc in positions and phase == "main" else "",
            status=status, case_reason=row.get("key_issue") or row.get("job_status"),
            raw_entries=locators([row]), zip_url=url,
        ))
    return frame


def inventory(args):
    upstream, prior_repo, out = args.upstream, args.prior_repo, args.out
    if git(upstream, "rev-parse", "HEAD").decode().strip() != UPSTREAM:
        raise ValueError("check out the exact DivEMT input commit")
    all_rows, frames, archives = [], [], {}
    for language in LANGUAGES:
        rows, meta = collect_archive(upstream, language)
        all_rows.extend(rows)
        archives[language] = meta
        frames.extend(cohort(rows, language, meta["selected_doc_ids"]))
    sources = {
        path: dict(
            git_blob=git(upstream, "rev-parse", f"HEAD:{path}").decode().strip(),
            sha256=sha_file(upstream / path),
        )
        for path in SOURCE_PATHS
    }
    prior = {}
    for path in ("HANDOFF.md", "assignments.csv", "effort-quality.csv", "bounds.csv", "sources.jsonl"):
        spec = f"{PRIOR}:{PRIOR_DIR}/{path}"
        prior[path] = dict(
            git_blob=git(prior_repo, "rev-parse", spec).decode().strip(),
            sha256=sha_bytes(git(prior_repo, "show", spec)),
            url=f"https://github.com/laadkke-arch/agentflow-open/blob/{PRIOR}/{PRIOR_DIR}/{path}",
        )
    inputs = dict(
        work_id="AF-RES-195", input_git_head=UPSTREAM,
        input_git_tree=git(upstream, "rev-parse", "HEAD^{tree}").decode().strip(),
        archives=archives, upstream_text_files=sources, prior_git_commit=PRIOR, prior_files=prior,
        processed_hf={
            "revision": HF_REV, "frozen_url": HF_URL, "publisher_sha256": HF_HASH,
            "metadata_url": "https://huggingface.co/datasets/GroNLP/divemt/blob/main/main.tsv",
        },
        environment=dict(python=platform.python_version(), platform=platform.system(),
                         machine=platform.machine(), zlib=zlib.ZLIB_RUNTIME_VERSION,
                         git=git(upstream, "--version").decode().strip()),
        cohort=dict(
            expected_slots=24, canonical_condition_slots_with_file=sum(
                row["row_kind"] == "planned_slot" and row["status"].startswith("included") for row in frames
            ),
            frame_rows=len(frames),
        ),
    )
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "inventory.csv", INVENTORY_FIELDS, all_rows)
    write_csv(out / "frame.csv", FRAME_FIELDS, frames)
    write_json(out / "inputs.json", inputs)
    print(json.dumps({
        "archive_rows": len(all_rows), "frame_rows": len(frames), "cohort": inputs["cohort"],
        "archives": {lang: {key: meta[key] for key in
                    ("selected_doc_ids", "canonical_per_status", "zip_read", "xml_parse", "key_issues")}
                    for lang, meta in archives.items()},
    }, sort_keys=True))


TIME = re.compile(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?(?:,(\d{1,3}))?")
PRODUCER = re.compile(r"(t\d+)(?:\..*)?")
ASSIGNMENT_FIELDS = (
    "slot_id language doc_rank doc_id condition assigned_subject observed_subject "
    "raw_file_present raw_xml_parsed raw_count raw_entries raw_file_sha256 raw_status "
    "planned_entries planned_file_sha256 allocation_check output_key source_doc_sha256 "
    "draft_doc_sha256 target_doc_sha256 planned_units raw_units completed_units "
    "participant_relation hf_joined_units raw_comparison_eligible independent_qa_status "
    "missing_reason evidence_ids zip_url"
).split()
SEGMENT_FIELDS = (
    "slot_id language doc_id condition assigned_subject subject_id xml_producer raw_entry "
    "raw_entry_index raw_file_sha256 raw_file_present raw_xml_parsed raw_job_status "
    "unit_id unit_status translation_type segment_id flores_id item_id source_sha256 "
    "draft_sha256 draft_producer target_sha256 target_state draft_equals_target "
    "pej_src_agrees pej_draft_agrees src_words tgt_chars visits events key_command_events "
    "key_total event_time_ms editing_ms visit_last_ms visit_editing_ms last_event_tags "
    "nonmonotone_visits pause_ge300_count pause_ge300_ms pause_ge1000_count pause_ge1000_ms "
    "pause_ge60000_ms pause_max_ms after_ge1000_union_ms after_ge60000_union_ms "
    "author_state author_event_ms author_editing_ms author_src_words author_pause_ge300_ms "
    "author_pause_ge1000_ms author_fingerprint_match author_all_metrics_match author_event_delta_ms prior_row_id "
    "prior_event_ms prior_words prior_values_match hf_state hf_tsv_record hf_event_ms "
    "hf_src_words hf_event_delta_ms hf_source_match hf_draft_match hf_target_match "
    "analysis_notebook_filtered raw_comparison_eligible comparison_reason independent_qa_status "
    "reviewer_time_ms"
).split()
REVISION_FIELDS = (
    "slot_id language subject_id raw_entry raw_entry_index sha256 revision xml_status "
    "segment_id flores_id unit_status target_state target_sha256 visits event_time_ms editing_ms "
    "is_canonical_byte_copy"
).split()
COMPARE_FIELDS = (
    "case_id language doc_id segment_id flores_id item_id source_sha256 src_words "
    "distinct_subjects ht_ms pe1_ms pe2_ms pe1_minus_ht_ms pe2_minus_ht_ms "
    "ht_after_ge1000_ms pe1_after_ge1000_ms pe2_after_ge1000_ms "
    "ht_after_ge60000_ms pe1_after_ge60000_ms pe2_after_ge60000_ms "
    "same_final_condition_pairs same_final_display_pairs notebook_filtered"
).split()
QUALITY_FIELDS = (
    "reviewer_id", "reviewer_time_ms", "independent_quality_key", "accepted_output_hash",
    "final_quality_score", "reviewer_time", "review_time_s", "human_judgment_id",
)
AUTHOR_KEYS = (
    "k_total", "n_pause_geq_300", "len_pause_geq_300", "n_pause_geq_1000",
    "len_pause_geq_1000", "event_time", "src_len_wrd", "num_annotations", "tgt_len_chr",
)
KEY_INDICATORS = (
    "letter", "digit", "white", "symbol", "navigation", "erase", "copy", "cut", "paste", "do",
)


def text_hash(value):
    return sha_bytes(value.encode("utf-8")) if value is not None else None


def node_text(node, tag):
    child = node.find(tag)
    return (child.text or "") if child is not None else None


def integer_duration(value):
    match = TIME.fullmatch(value or "")
    if not match or not any(match.groups()):
        return None
    h, m, s, ms = (int(x or 0) for x in match.groups())
    return ((h * 60 + m) * 60 + s) * 1000 + ms


def complete_sum(values):
    return sum(values) if values and all(value is not None for value in values) else None


def union_size(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return sum(end - start for start, end in merged)


def measure_visit(annotation):
    events_node = annotation.find("events")
    events = list(events_node) if events_node is not None else []
    stamps = [event.get("t", "") for event in events]
    valid = events_node is not None and all(stamp.isdecimal() for stamp in stamps)
    pairs = [(node.tag, int(stamp)) for node, stamp in zip(events, stamps)] if valid else []
    times = [stamp for _, stamp in pairs]
    keys = [stamp for tag, stamp in pairs if tag in ("keystroke", "command")]
    intervals = list(zip([0] + keys, keys))
    backwards = any(a > b for a, b in zip(times, times[1:]))
    keys_recorded = [annotation.findtext(f"indicator[@id='{name}-keys']", "") for name in KEY_INDICATORS]
    return dict(
        end=(times[-1] if times else 0) if valid else None,
        editing=integer_duration(annotation.findtext("indicator[@id='editing']")),
        events=len(events), key_events=len(keys) if valid else None,
        key_total=sum(map(int, keys_recorded)) if all(x.isdecimal() for x in keys_recorded) else None,
        last_tag=pairs[-1][0] if pairs else "", backwards=backwards, intervals=intervals,
    )


def pause_summary(visits, threshold):
    groups = [[(a, b) for a, b in visit["intervals"] if b - a >= threshold] for visit in visits]
    return (
        sum(len(gaps) for gaps in groups),
        sum(b - a for gaps in groups for a, b in gaps),
        sum(union_size(gaps) for gaps in groups),
    )


def unit_record(unit, language):
    mode = unit.get("type")
    source = node_text(unit, "S")
    draft = node_text(unit, "MT")
    draft_node = unit.find("MT")
    annotations = unit.findall("annotations/annotation")
    final = annotations[-1].find("PE" if mode == "pe" else "HT") if annotations else None
    target = (final.text or "") if final is not None else None
    producer = PRODUCER.fullmatch(final.get("producer", "")) if final is not None else None
    visits = [measure_visit(annotation) for annotation in annotations]
    event_ms = complete_sum([visit["end"] for visit in visits])
    editing_ms = complete_sum([visit["editing"] for visit in visits])
    n300, ms300, _ = pause_summary(visits, 300)
    n1000, ms1000, union1000 = pause_summary(visits, 1000)
    _, ms60000, union60000 = pause_summary(visits, 60000)
    pauses_usable = event_ms is not None and not any(visit["backwards"] for visit in visits)
    max_pause = max((b - a for visit in visits for a, b in visit["intervals"]), default=0)
    return dict(
        segment_id=unit.get("id"), flores_id=unit.get("orig_id"), unit_status=unit.get("status", "unset"),
        translation_type=mode, xml_producer=f"{language}_{producer[1]}" if producer else None,
        source_sha256=text_hash(source), draft_sha256=text_hash(draft), target_sha256=text_hash(target),
        draft_producer=draft_node.get("producer") if draft_node is not None else None,
        target_state="missing" if target is None else "empty" if target == "" else "present",
        draft_equals_target=(draft == target) if draft is not None and target is not None else None,
        display_target_sha256=text_hash(" ".join(target.split()).casefold()) if target is not None else None,
        src_words=len(source.split()) if source is not None else None,
        tgt_chars=len(target) if target is not None else None,
        visits=len(visits), events=sum(v["events"] for v in visits),
        key_command_events=complete_sum([visit["key_events"] for visit in visits]),
        key_total=complete_sum([visit["key_total"] for visit in visits]),
        visit_last_ms=json.dumps([visit["end"] for visit in visits], separators=(",", ":")),
        visit_editing_ms=json.dumps([visit["editing"] for visit in visits], separators=(",", ":")),
        last_event_tags=";".join(visit["last_tag"] for visit in visits),
        nonmonotone_visits=sum(visit["backwards"] for visit in visits),
        event_time_ms=event_ms, editing_ms=editing_ms,
        pause_ge300_count=n300 if pauses_usable else None, pause_ge300_ms=ms300 if pauses_usable else None,
        pause_ge1000_count=n1000 if pauses_usable else None, pause_ge1000_ms=ms1000 if pauses_usable else None,
        pause_ge60000_ms=ms60000 if pauses_usable else None, pause_max_ms=max_pause if pauses_usable else None,
        after_ge1000_union_ms=event_ms - union1000 if pauses_usable else None,
        after_ge60000_union_ms=event_ms - union60000 if pauses_usable else None,
    )


def load_author(upstream):
    import pandas as pd

    path = upstream / "divemt" / "parse_utils.py"
    tree = ast.parse(path.read_bytes(), filename=str(path))
    names = {"_KEYS_INDICATOR_MAP", "_METRICS_DF_FIELDS"}
    funcs = {"time2seconds", "per2metrics", "per2texts"}
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in funcs:
            nodes.append(node)
        elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in names:
            nodes.append(node)
    if len(nodes) != len(names) + len(funcs):
        raise ValueError("unexpected author parser layout")
    logger = logging.Logger("af195_author")
    logger.addHandler(logging.NullHandler())
    context = dict(pd=pd, ET=ET, os=os, Optional=Optional, defaultdict=defaultdict, logger=logger)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), context)
    return context, pd.__version__


def author_rows(context, body, name):
    try:
        with tempfile.TemporaryDirectory(prefix="af195-pet-") as directory:
            path = Path(directory) / Path(name).name
            path.write_bytes(body)
            metrics = context["per2metrics"](str(path))
            texts = context["per2texts"](str(path))
    except (AttributeError, IndexError, TypeError, ValueError, ZeroDivisionError) as error:
        return f"author_error_{type(error).__name__}", {}
    if metrics is None or texts is None:
        return "author_FINISHED_filter", {}
    results = defaultdict(list)
    for row in metrics.merge(texts, on="unit_id", validate="one_to_one").to_dict("records"):
        results[row["unit_id"]].append(row)
    return "author_executed", results


def read_jobs(args, meta, slots):
    inv = read_csv(args.out / "inventory.csv")
    positions = {row["slot_id"] for row in slots}
    raw, plans, backup = defaultdict(list), defaultdict(list), defaultdict(list)
    indexes = {"per": raw, "pej": plans, "per_backup": backup}
    for language in LANGUAGES:
        path = args.upstream / meta["archives"][language]["path"]
        if sha_file(path) != meta["archives"][language]["sha256"]:
            raise ValueError(f"rerun inventory with the pinned archive for {language}")
        with zipfile.ZipFile(path) as z:
            entries = z.infolist()
            for row in inv:
                slot = position(row["language"], row["doc_id"], row["condition"])
                if row["language"] != language or row["phase"] != "main" or slot not in positions:
                    continue
                index = int(row["entry_index"]) - 1
                body = z.read(entries[index])
                if entries[index].filename != row["entry"] or sha_bytes(body) != row["sha256"]:
                    raise ValueError("selected entry does not match inventory")
                try:
                    root = ET.fromstring(body)
                except ET.ParseError:
                    root = None
                indexes[row["kind"]][slot].append((row, root, body if row["kind"] == "per" else None))
    return raw, plans, backup


def parse_hf(path, slots):
    if path is None:
        return {}, dict(state="pinned_tsv_unavailable", hf_sha256=None)
    digest = sha_file(path)
    if digest != HF_HASH:
        raise ValueError("HF TSV SHA-256 does not match the pinned publisher object")
    rows, all_rows = defaultdict(list), 0
    csv.field_size_limit(10 * 1024 * 1024)
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        for count, row in enumerate(reader, 1):
            all_rows = count
            if position(row["lang_id"], row["doc_id"], row["task_type"]) in slots:
                key = row["unit_id"], row["subject_id"], row["flores_id"]
                rows[key].append((count, row))
        fields = reader.fieldnames
    return rows, dict(
        state="pinned_tsv_read", hf_sha256=digest, hf_rows=all_rows,
        hf_candidate_rows=sum(map(len, rows.values())), fields=fields,
        candidate_review_fields=sorted(set(QUALITY_FIELDS).intersection(fields)),
    )


def add_hf(row, lookup, state):
    row["hf_state"] = state
    if state != "pinned_tsv_read":
        return
    matches = lookup.get((row["unit_id"], row["subject_id"], row["flores_id"]), [])
    if len(matches) != 1:
        row["hf_state"] = "hf_missing_key" if not matches else "hf_ambiguous_key"
        return
    record_index, result = matches[0]
    if (row["item_id"], row["language"], row["doc_id"], row["condition"], row["translation_type"]) != tuple(
        result[field] for field in ("item_id", "lang_id", "doc_id", "task_type", "translation_type")
    ):
        row["hf_state"] = "hf_secondary_key_mismatch"
        return
    event_ms, words = int(result["event_time"]), int(result["src_len_wrd"])
    mt = None if row["condition"] == "ht" and not result["mt_text"] else result["mt_text"]
    row.update(
        hf_state="hf_exact_keys", hf_tsv_record=record_index, hf_event_ms=event_ms,
        hf_src_words=words, hf_event_delta_ms=difference(row.get("event_time_ms"), event_ms),
        hf_source_match=text_hash(result["src_text"]) == row["source_sha256"],
        hf_draft_match=text_hash(mt) == row["draft_sha256"],
        hf_target_match=text_hash(result["tgt_text"]) == row["target_sha256"],
    )


def difference(a, b):
    return a - b if a is not None and b is not None else None


def add_author(row, state, results):
    row["author_state"] = state
    matches = results.get(row["unit_id"], [])
    if state != "author_executed":
        return
    if len(matches) != 1:
        row["author_state"] = "author_unit_missing_or_duplicated"
        return
    ref = matches[0]
    checks = (
        ref["flores_id"] == row["flores_id"], ref["task_type"] == row["condition"],
        ref["item_id"].replace(f"-{row['language']}-", "-") == row["item_id"],
        ref["translation_type"] == row["translation_type"],
        f"{row['language']}_{ref['subject_id']}" == row["subject_id"],
    )
    row.update(
        author_state="author_exact_keys" if all(checks) else "author_key_mismatch",
        author_event_ms=ref["event_time"], author_editing_ms=round(ref["edit_time"] * 1000),
        author_src_words=ref["src_len_wrd"], author_event_delta_ms=difference(row["event_time_ms"], ref["event_time"]),
        author_pause_ge300_ms=ref["len_pause_geq_300"], author_pause_ge1000_ms=ref["len_pause_geq_1000"],
        author_fingerprint_match=all(
            row[f"{col}_sha256"] == text_hash(ref[name])
            for col, name in (("source", "src_text"), ("draft", "mt_text"), ("target", "tgt_text"))
        ),
        author_all_metrics_match=all(
            row[name] == ref[field]
            for name, field in zip((
                "key_total", "pause_ge300_count", "pause_ge300_ms", "pause_ge1000_count",
                "pause_ge1000_ms", "event_time_ms", "src_words", "visits", "tgt_chars",
            ), AUTHOR_KEYS)
        ) and row["editing_ms"] == round(ref["edit_time"] * 1000),
    )


def add_prior(row, records):
    ref = records.get((row["unit_id"], row["subject_id"], row["flores_id"]))
    if not ref:
        return
    pairs = (
        ("event_time_ms", "event_time_ms"), ("src_words", "src_words"), ("tgt_chars", "target_chars"),
        ("pause_ge300_count", "pause_ge300_count"), ("pause_ge300_ms", "pause_ge300_ms"),
        ("pause_ge1000_count", "pause_ge1000_count"), ("pause_ge1000_ms", "pause_ge1000_ms"),
        ("visits", "annotations"),
    )
    row.update(
        prior_row_id=ref["row_id"], prior_event_ms=int(ref["event_time_ms"]), prior_words=int(ref["src_words"]),
        prior_values_match=all(row[ours] == int(ref[theirs]) for ours, theirs in pairs)
        and row["item_id"] == ref["item_id"] and row["segment_id"] == ref["segment_id"]
        and row["editing_ms"] == round(float(ref["edit_time_s"]) * 1000),
    )


def outlier_keys(upstream):
    notebook = json.loads((upstream / "notebooks" / "analysis.ipynb").read_text())
    for data in notebook["cells"]:
        source = "".join(data["source"])
        if source.startswith("outliers = ["):
            tree = ast.parse(source)
            return set(ast.literal_eval(tree.body[0].value))
    raise ValueError("could not locate author analysis exclusions")


def record_for_unit(slot, meta, unit, planned_units, exclusions):
    language, condition = slot["language"], slot["condition"]
    record = unit_record(unit, language)
    segment, flores = record["segment_id"], record["flores_id"]
    plan = planned_units.get((segment, flores))
    if plan is not None:
        record["pej_src_agrees"] = record["source_sha256"] == text_hash(node_text(plan, "S"))
        record["pej_draft_agrees"] = record["draft_sha256"] == text_hash(node_text(plan, "MT"))
    item = f"flores101-main-{slot['doc_id']}{segment}"
    record.update(
        slot_id=slot["slot_id"], language=language, doc_id=slot["doc_id"], condition=condition,
        subject_id=meta["subject_id"], raw_entry=meta["entry"], raw_entry_index=meta["entry_index"],
        raw_file_sha256=meta["sha256"], raw_file_present=True, raw_xml_parsed=True,
        raw_job_status=meta["job_status"], unit_id=f"{meta['job_id']}-{segment}", item_id=item,
        analysis_notebook_filtered=item in exclusions, independent_qa_status="no_public_independent_key",
    )
    checks = {
        "not_finished": meta["job_status"] != "FINISHED" or record["unit_status"] != "FINISHED",
        "missing_or_empty_target": record["target_state"] != "present",
        "missing_source_or_timing": not record["src_words"] or record["event_time_ms"] is None,
        "producer_folder_mismatch": record["xml_producer"] != meta["subject_id"],
        "nonmonotone_event_clock": bool(record["nonmonotone_visits"]),
        "no_agreeing_assigned_input": plan is None or not record["pej_src_agrees"] or not record["pej_draft_agrees"],
        "draft_condition_mismatch": record["draft_producer"] != {"ht": None, "pe1": "1", "pe2": "2"}[condition],
    }
    record["comparison_reason"] = ";".join(k for k, bad in checks.items() if bad)
    record["raw_comparison_eligible"] = not record["comparison_reason"]
    return record


def planned_only_record(slot, planned, unit, hf_state):
    participant = planned["subject_id"] if planned else ""
    return dict(
        slot_id=slot["slot_id"], language=slot["language"], doc_id=slot["doc_id"], condition=slot["condition"],
        assigned_subject=participant, subject_id=participant, raw_file_present=False, raw_xml_parsed=False,
        segment_id=unit.get("id") if unit is not None else None, flores_id=unit.get("orig_id") if unit is not None else None,
        source_sha256=text_hash(node_text(unit, "S")) if unit is not None else None,
        draft_sha256=text_hash(node_text(unit, "MT")) if unit is not None else None,
        raw_comparison_eligible=False, comparison_reason="missing_canonical_unit", hf_state=hf_state,
        independent_qa_status="no_public_independent_key",
    )


def hash_sequence(rows, field):
    if not rows or any(record.get(field) is None for record in rows):
        return None
    parts = [(row["segment_id"], row["flores_id"], row[field]) for row in rows]
    return sha_bytes(json.dumps(parts, separators=(",", ":")).encode("utf-8"))


def assignment_and_units(slot, raw, plans, oracle, prior, hf, hf_state, exclusions):
    planned_meta, plan_root, _ = plans[0] if len(plans) == 1 else (None, None, None)
    planned_units = {
        (unit.get("id"), unit.get("orig_id")): unit
        for unit in plan_root.findall("task")
    } if plan_root is not None else {}
    participant = planned_meta["subject_id"] if planned_meta else ""
    units = []
    observed = set()
    for meta, root, body in raw:
        if root is None:
            continue
        state, ref = author_rows(oracle, body, meta["entry"])
        for unit in root.findall("unit"):
            record = record_for_unit(slot, meta, unit, planned_units, exclusions)
            record["assigned_subject"] = participant
            if len(raw) != 1 or record["subject_id"] != participant:
                record["raw_comparison_eligible"] = False
                reason = record["comparison_reason"]
                record["comparison_reason"] = ";".join(filter(None, (reason, "ambiguous_or_conflicting_allocation")))
            add_author(record, state, ref)
            add_prior(record, prior)
            add_hf(record, hf, hf_state)
            units.append(record)
            observed.add((record["segment_id"], record["flores_id"]))
    for key, unit in planned_units.items():
        if key not in observed:
            units.append(planned_only_record(slot, planned_meta, unit, hf_state))
    if not units:
        units.append(planned_only_record(slot, planned_meta, None, hf_state))
    slot_id = slot["slot_id"]
    observed_subjects = sorted({meta["subject_id"] for meta, _, _ in raw})
    eligible = len(raw) == 1 and bool(units) and all(r["raw_comparison_eligible"] for r in units)
    allocation_ok = len(raw) == 1 and len(plans) == 1 and observed_subjects == [participant]
    reasons = []
    if not raw:
        reasons.append("canonical_per_missing_or_unresolved")
    if len(plans) != 1:
        reasons.append("assignment_input_missing_or_ambiguous")
    if raw and not allocation_ok:
        reasons.append("allocation_conflict_or_duplicate")
    if hf_state != "pinned_tsv_read":
        reasons.append(hf_state)
    if not eligible:
        reasons.append("one_or_more_units_ineligible")
    summary = {field: slot[field] for field in ("slot_id", "language", "doc_rank", "doc_id", "condition", "zip_url")}
    summary.update(
        assigned_subject=participant, observed_subject=";".join(observed_subjects),
        raw_file_present=bool(raw), raw_xml_parsed=bool(raw) and all(root is not None for _, root, _ in raw),
        raw_count=len(raw), raw_entries=locators([m for m, _, _ in raw]),
        raw_file_sha256=";".join(m["sha256"] for m, _, _ in raw),
        raw_status=";".join(m["job_status"] for m, _, _ in raw),
        planned_entries=locators([m for m, _, _ in plans]),
        planned_file_sha256=";".join(m["sha256"] for m, _, _ in plans),
        allocation_check="pej_matches_folder_job_provider" if allocation_ok else "unconfirmed",
        output_key=f"{slot_id}/{participant}" if eligible else None,
        source_doc_sha256=hash_sequence(units, "source_sha256"),
        draft_doc_sha256=hash_sequence(units, "draft_sha256"),
        target_doc_sha256=hash_sequence(units, "target_sha256"),
        planned_units=len(planned_units), raw_units=sum(bool(r["raw_file_present"]) for r in units),
        completed_units=sum(r.get("unit_status") == "FINISHED" for r in units),
        hf_joined_units=sum(r["hf_state"] == "hf_exact_keys" for r in units),
        raw_comparison_eligible=eligible, independent_qa_status="no_public_independent_key",
        missing_reason=";".join(reasons),
        evidence_ids=";".join([
            f"RAW-{m['language'].upper()}-{int(m['entry_index']):04d}" for m, _, _ in raw
        ] + [f"JOB-{m['language'].upper()}-{int(m['entry_index']):04d}" for m, _, _ in plans]),
    )
    return summary, units


def revision_records(backups, canonical):
    for slot, files in backups.items():
        original = {meta["sha256"] for meta, _, _ in canonical[slot]}
        for meta, root, _ in files:
            if root is None:
                continue
            for unit in root.findall("unit"):
                row = unit_record(unit, meta["language"])
                yield dict(
                    slot_id=slot, language=meta["language"], subject_id=meta["subject_id"], raw_entry=meta["entry"],
                    raw_entry_index=meta["entry_index"], sha256=meta["sha256"], revision=meta["revision"],
                    xml_status=meta["job_status"], is_canonical_byte_copy=meta["sha256"] in original,
                    **{k: row[k] for k in ("segment_id", "flores_id", "unit_status", "target_state",
                                           "target_sha256", "visits", "event_time_ms", "editing_ms")},
                )


def compare_records(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[(row["language"], row["doc_id"], row["segment_id"], row["flores_id"])].append(row)
    complete = []
    for key, hits in groups.items():
        by_condition = {row["condition"]: row for row in hits if row["raw_comparison_eligible"]}
        sources = {row["source_sha256"] for row in hits}
        people = {row["subject_id"] for row in hits}
        if len(hits) != 3 or len(by_condition) != 3 or len(sources) != 1 or len(people) != 3:
            continue
        lang, doc, segment, flores = key
        ht, p1, p2 = (by_condition[condition] for condition in CONDITIONS)
        combined = dict(
            case_id=f"{lang}-{doc}-{segment}-{flores}", language=lang, doc_id=doc, segment_id=segment,
            flores_id=flores, item_id=ht["item_id"], source_sha256=ht["source_sha256"], src_words=ht["src_words"],
            distinct_subjects=len(people), notebook_filtered=ht["analysis_notebook_filtered"],
            pe1_minus_ht_ms=p1["event_time_ms"] - ht["event_time_ms"],
            pe2_minus_ht_ms=p2["event_time_ms"] - ht["event_time_ms"],
        )
        pairs = combinations(CONDITIONS, 2)
        combined["same_final_condition_pairs"] = ";".join(
            a + "=" + b for a, b in pairs if by_condition[a]["target_sha256"] == by_condition[b]["target_sha256"]
        )
        combined["same_final_display_pairs"] = ";".join(
            a + "=" + b for a, b in combinations(CONDITIONS, 2)
            if by_condition[a]["display_target_sha256"] == by_condition[b]["display_target_sha256"]
        )
        for mode, r in by_condition.items():
            combined[f"{mode}_ms"] = r["event_time_ms"]
            combined[f"{mode}_after_ge1000_ms"] = r["after_ge1000_union_ms"]
            combined[f"{mode}_after_ge60000_ms"] = r["after_ge60000_union_ms"]
        complete.append(combined)
    return complete, len(groups)


def measure(args):
    if git(args.upstream, "rev-parse", "HEAD").decode().strip() != UPSTREAM:
        raise ValueError("check out the exact DivEMT input commit")
    meta = json.loads((args.out / "inputs.json").read_text())
    slots = [row for row in read_csv(args.out / "frame.csv") if row["row_kind"] == "planned_slot"]
    oracle, pandas_version = load_author(args.upstream)
    raw, plans, backups = read_jobs(args, meta, slots)
    exclusions = outlier_keys(args.upstream)
    raw_prior = git(args.prior_repo, "show", f"{PRIOR}:{PRIOR_DIR}/effort-quality.csv")
    prior = {(r["unit_id"], r["participant_key"], r["flores_id"]): r
             for r in csv.DictReader(io.StringIO(raw_prior.decode("utf-8")))}
    hf, hf_meta = parse_hf(args.hf_main, {row["slot_id"] for row in slots})
    assignments, segments = [], []
    for slot in slots:
        key = slot["slot_id"]
        result, units = assignment_and_units(slot, raw[key], plans[key], oracle, prior, hf,
                                             hf_meta["state"], exclusions)
        assignments.append(result)
        segments.extend(units)
    people = defaultdict(set)
    for a in assignments:
        people[(a["language"], a["doc_id"])].update(filter(None, a["observed_subject"].split(";")))
    for a in assignments:
        count = len(people[(a["language"], a["doc_id"])])
        a["participant_relation"] = "three_different_subjects" if count == 3 else f"{count}_observed_subjects"
    cases, source_cases = compare_records(segments)
    revisions = list(revision_records(backups, raw))
    prior_hits = [row for row in segments if row.get("prior_row_id")]
    summary = dict(
        parser_git_pin=UPSTREAM, pandas=pandas_version, python=platform.python_version(),
        assignments=len(assignments), allocation_matches=sum(a["allocation_check"].startswith("pej_matches") for a in assignments),
        segments=len(segments), comparable_raw_segments=sum(row["raw_comparison_eligible"] for row in segments),
        source_cases=source_cases, complete_triplets=len(cases),
        oracle_all_fields_equal=sum(row.get("author_all_metrics_match", False) and
                                    row.get("author_state") == "author_exact_keys" and
                                    row.get("author_fingerprint_match", False) for row in segments),
        hf=hf_meta | dict(joined_rows=sum(row["hf_state"] == "hf_exact_keys" for row in segments)),
        prior_rows=len(prior_hits), prior_rows_all_fields_equal=sum(row["prior_values_match"] for row in prior_hits),
        prior_reproduced_event_ms=sum(row["event_time_ms"] for row in prior_hits),
        prior_reproduced_words=sum(row["src_words"] for row in prior_hits),
        editing_event_delta_count=sum(row.get("editing_ms") != row.get("event_time_ms") for row in segments),
        visit_count=dict(Counter(row.get("visits", "missing") for row in segments)),
        canonical_raw_zero_count=sum(row.get("event_time_ms") == 0 for row in segments),
        revision_entries=len({r["raw_entry"] for r in revisions}),
        revision_units=len(revisions),
        revision_byte_copies=len({r["raw_entry"] for r in revisions if r["is_canonical_byte_copy"]}),
        revision_file_status=dict(Counter(dict((r["raw_entry"], r["xml_status"]) for r in revisions).values())),
        revision_missing_time=sum(r["event_time_ms"] is None for r in revisions),
        revision_zero_time=sum(r["event_time_ms"] == 0 for r in revisions),
        same_final_exact_cases=sum(bool(c["same_final_condition_pairs"]) for c in cases),
        same_final_display_cases=sum(bool(c["same_final_display_pairs"]) for c in cases),
        analysis_outlier_ids=sorted(exclusions),
        filtered_items_in_sample=sorted({row["item_id"] for row in segments if row.get("analysis_notebook_filtered")}),
    )
    write_csv(args.out / "assignments.csv", ASSIGNMENT_FIELDS, assignments)
    write_csv(args.out / "segments.csv", SEGMENT_FIELDS, [{k: r.get(k) for k in SEGMENT_FIELDS} for r in segments])
    receipts = args.out / "receipts"
    receipts.mkdir(exist_ok=True)
    write_csv(receipts / "03-pairs.csv", COMPARE_FIELDS, cases)
    write_csv(receipts / "03-revisions.csv", REVISION_FIELDS, revisions)
    write_json(receipts / "03-summary.json", summary)
    print(json.dumps(summary, sort_keys=True))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(required=True)
    inventory_parser = subparsers.add_parser("inventory", help="read and hash both frozen ZIP archives")
    inventory_parser.add_argument("--upstream", type=Path, required=True)
    inventory_parser.add_argument("--prior-repo", type=Path, required=True)
    inventory_parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    inventory_parser.set_defaults(run=inventory)
    measure_parser = subparsers.add_parser("measure", help="join raw, author and optional pinned HF rows")
    measure_parser.add_argument("--upstream", type=Path, required=True)
    measure_parser.add_argument("--prior-repo", type=Path, required=True)
    measure_parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    measure_parser.add_argument("--hf-main", type=Path, help="exact HF main.tsv, verified by SHA-256")
    measure_parser.set_defaults(run=measure)
    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
