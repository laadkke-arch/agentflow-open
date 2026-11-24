#!/usr/bin/env python3
"""Inventory frozen DivEMT archives and reconcile de-identified segment records."""

import argparse
import csv
import hashlib
import json
import platform
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile
import zlib
from collections import Counter, defaultdict
from pathlib import Path


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
    units = root.findall("unit")
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(required=True)
    inventory_parser = subparsers.add_parser("inventory", help="read and hash both frozen ZIP archives")
    inventory_parser.add_argument("--upstream", type=Path, required=True)
    inventory_parser.add_argument("--prior-repo", type=Path, required=True)
    inventory_parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    inventory_parser.set_defaults(run=inventory)
    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
