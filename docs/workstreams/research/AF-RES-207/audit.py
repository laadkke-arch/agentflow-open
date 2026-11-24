"""Reopen pinned AF-RES-195 citations, observe their denominator, and score separately."""
import argparse
import base64
from collections import Counter
import csv
import ctypes
import datetime as dt
import errno
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile


BUNDLE = "bundle.json"
SEGMENTS = "segments.csv"
ASSIGNMENTS = "assignments.csv"
SOURCE_UNITS = "source-units.csv"
PAYLOAD = (SEGMENTS, ASSIGNMENTS, SOURCE_UNITS)
A_FIELDS = {"url", "sentence", "type", "revision", "relative_path", "excerpt_sha256", "locator", "excerpt_base64"}
B_FIELDS = ("row_selector", "group_by", "missing", "units", "formula")
DIMENSIONS = ["language", "doc_id", "condition", "subject_id"]
UNIT_KEY = ["segment_id", "flores_id", "source_sha256"]
DENOM_FIELDS = ("segments", "source_words", "participants", "assignments")
QA_MISSING = "independent_qa_link_and_reviewer_time_unavailable"
CLAIM_START = re.compile(r"^(ITA|TUR) (\d+)(?: (HT|PE1|PE2)(?: FLORES (\d+))?)?(?:의|\s)")
NUMERIC_CLAIM = re.compile(r"([\d,]+) (ms|초), 영어 원문 ([\d,]+)단어다\.$")
COUNT_CLAIM = re.compile(r"(\d+)분절 합")


def invariant(condition, message):
    if not condition:
        raise ValueError(message)


def encode(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def lines_digest(parts):
    return digest(b"".join(struct.pack(">Q", len(part)) + part for part in parts))


def file_json(path):
    return json.loads(path.read_bytes())


def write_jsonl(path, records):
    with path.open("wb") as stream:
        for record in records:
            stream.write(encode(record))


def read_jsonl(path):
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def csv_table(data):
    reader = csv.DictReader(io.StringIO(data.decode("utf-8"), newline=""))
    fields = reader.fieldnames
    rows = list(reader)
    invariant(fields and len(fields) == len(set(fields)), "CSV header absent or duplicated")
    invariant(reader.line_num == len(rows) + 1 and all(None not in row and None not in row.values() for row in rows),
              "expected one physical line and fixed field count per CSV record")
    return fields, rows


def csv_bytes(fields, rows, newline="\n", header=True):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fields, lineterminator=newline)
    if header:
        writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def quote(data, windows):
    rows = data.splitlines(keepends=True)
    offsets = [0]
    for row in rows:
        offsets.append(offsets[-1] + len(row))
    locator = []
    parts = []
    last = 0
    for first, end in windows:
        invariant(last < first <= end <= len(rows), "out-of-bounds or overlapping source locator")
        start_byte, end_byte = offsets[first - 1], offsets[end]
        locator.append(dict(first_line=first, last_line=end, start_byte=start_byte, end_byte=end_byte))
        parts.append(data[start_byte:end_byte])
        last = end
    return locator, parts


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def pinned(repo, artifact):
    ref = artifact["commit"] + ":" + artifact["path"]
    blob = git(repo, "rev-parse", ref).decode().strip()
    data = git(repo, "show", ref)
    invariant(blob == artifact["git_blob"] and digest(data) == artifact["sha256"] and len(data) == artifact["bytes"], ref)
    return data


def load_payload(repo, inputs):
    artifacts = inputs["artifacts"]
    payload = {name: pinned(repo, artifacts[source]) for name, source in inputs["local_payload"].items()}
    _, pairs = csv_table(payload[SOURCE_UNITS])
    columns = inputs["source_units_projection"]
    payload[SOURCE_UNITS] = csv_bytes(columns, [{field: row[field] for field in columns} for row in pairs])
    for data in payload.values():
        csv_table(data)
    return payload


def augmentation(selector):
    if "condition" not in selector:
        return dict(row_selector=selector, group_by=DIMENSIONS, missing={
            "required_roles": ["translator", "independent_reviewer"],
            "match": "accepted_target_sha256", "on_unlinked_role": "withhold",
        }, units={"time": "ms"}, formula={"op": "sum_linked_role_time", "time": "event_time_ms",
                                        "reviewer_time": "reviewer_time_ms"})
    return dict(row_selector=selector, group_by=DIMENSIONS, missing={
        "coverage": "planned_units", "cohort": SOURCE_UNITS, "status": "FINISHED",
        "on_missing": "withhold", "on_duplicate_source_unit": "withhold",
    }, units={"time": "ms", "source_words": "English words"},
        formula={"op": "sum", "time": "event_time_ms", "source_words": "src_words"})


def bundle_for(case, payload, inputs):
    artifact = inputs["artifacts"][case["primary_source_id"]]
    filename = Path(artifact["path"]).name
    locator, parts = quote(payload[filename], case["locator_lines"])
    citation = "#L{first_line}-L{last_line}".format(**locator[-1])
    base = dict(url=artifact["url"] + citation, sentence=case["sentence"], type="new", revision=artifact["commit"],
                relative_path=artifact["path"], excerpt_sha256=lines_digest(parts), locator=locator,
                excerpt_base64=[base64.b64encode(part).decode("ascii") for part in parts])
    invariant(set(base) == set(inputs["adopted_format"]["adopted_fields"]), "A field drift")
    return base, base | augmentation(case["selector"])


def claim_from_sentence(sentence):
    prefix = CLAIM_START.match(sentence)
    invariant(prefix is not None, "unrecognized display scope")
    lang, doc, condition, flores = prefix.groups()
    selector = {"language": lang.lower(), "doc_id": doc}
    if condition:
        selector["condition"] = condition.lower()
    if flores:
        selector["flores_id"] = flores
    claim = NUMERIC_CLAIM.search(sentence)
    if not condition:
        invariant(sentence.endswith("독립 QA 포함 총노동 비교는 보류한다."), "unrecognized withheld comparison")
        return selector, None
    invariant(claim is not None, "unrecognized numeric display")
    value, unit, words = claim.groups()
    count = COUNT_CLAIM.search(sentence)
    return selector, dict(value=int(value.replace(",", "")), unit="s" if unit == "초" else unit,
                          source_words=int(words.replace(",", "")), segments=int(count.group(1)) if count else 1)


def matches(row, selector):
    return all(row.get(field) == value for field, value in selector.items())


def key_tuple(row, fields):
    return tuple(row[field] for field in fields)


def row_key(row):
    return "{slot_id}/{subject_id}/{unit_id}/FLORES-{flores_id}".format(**row)


def ready(row):
    return (row["unit_status"] == "FINISHED" and row["raw_job_status"] == "FINISHED" and
            all(row[field] == "True" for field in ("raw_file_present", "raw_xml_parsed", "raw_comparison_eligible")) and
            row["event_time_ms"] != "" and row["src_words"] != "")


def observe_amount(rows, claim, policy=None):
    reasons = []
    if not rows or not all(map(ready, rows)):
        reasons.append("missing_required_observation")
    time_field = policy["formula"]["time"] if policy else "event_time_ms"
    words_field = policy["formula"]["source_words"] if policy else "src_words"
    timed = [row for row in rows if row[time_field] and row[words_field]]
    time = sum(int(row[time_field]) for row in timed) if timed else None
    words = sum(int(row[words_field]) for row in timed) if timed else None
    unit = (policy["units"]["time"] if policy else "ms") if timed else None
    subjects = sorted({row["subject_id"] for row in rows})
    assignments = sorted({row["slot_id"] for row in rows})
    denom = dict(zip(DENOM_FIELDS, (len(rows), words, len(subjects), len(assignments))))
    if (time, words, len(rows)) != (claim["value"], claim["source_words"], claim["segments"]):
        reasons.append("claim_arithmetic_mismatch")
    if unit != claim["unit"]:
        reasons.append("claim_unit_mismatch")
    return dict(value=time, unit=unit, rows=sorted(map(row_key, rows)), denominator=denom,
                reasons=reasons, admissible_rows=sum(map(ready, rows)), support_assignment_keys=assignments)


def b_amount(selector, policy, reader, archived_rows):
    _, segments = csv_table(reader.read(SEGMENTS))
    _, assignments = csv_table(reader.read(ASSIGNMENTS))
    _, source_units = csv_table(reader.read(SOURCE_UNITS))
    document = {field: selector[field] for field in ("language", "doc_id")}
    assignment = [row for row in assignments if matches(row, document | {"condition": selector["condition"]})]
    source_document = [row for row in source_units if matches(row, document)]
    expected = [row for row in source_document if "flores_id" not in selector or matches(row, {"flores_id": selector["flores_id"]})]
    candidate = [row for row in segments if matches(row, selector)]
    reasons = []
    if (len(assignment) != 1 or not expected or (assignment[0]["raw_status"] != policy["missing"]["status"]) or
            int(assignment[0][policy["missing"]["coverage"]]) != len(source_document)):
        reasons.append("assignment_or_planned_coverage_unavailable")
    actual = Counter(key_tuple(row, UNIT_KEY) for row in candidate)
    if any(n != 1 for n in actual.values()):
        reasons.append("duplicate_source_observation")
    if set(actual) != {key_tuple(row, UNIT_KEY) for row in expected}:
        reasons.append("source_cohort_mismatch")
    for row in candidate:
        if not assignment or any(row[field] != assignment[0][assigned] for field, assigned in (
            ("slot_id", "slot_id"), ("subject_id", "observed_subject"), ("raw_file_sha256", "raw_file_sha256")
        )):
            reasons.append("assignment_lineage_conflict")
            break
    groups = sorted({key_tuple(row, policy["group_by"]) for row in candidate})
    if len(groups) != 1:
        reasons.append("group_mismatch")
    if Counter(map(row_key, archived_rows)) != Counter(map(row_key, candidate)):
        reasons.append("quoted_rows_disagree_with_selector")
    trace = dict(source_unit_key=UNIT_KEY, source_units_examined=len(source_units),
                 cohort_ids=[row["flores_id"] for row in expected], segment_rows_examined=len(segments),
                 assignment_rows_examined=len(assignments), selected_candidate_keys=list(map(row_key, candidate)),
                 dimensions=policy["group_by"], groups=groups)
    return candidate, reasons, trace


def observe_qa(assignments, segments):
    assignment_keys = sorted(row["slot_id"] for row in assignments)
    evidence = [row for row in segments if row["slot_id"] in assignment_keys]
    linked = [r for r in evidence if r["independent_qa_status"] != "no_public_independent_key" and r["reviewer_time_ms"]]
    found_missing = (assignments and evidence and not linked and
                     all(r["independent_qa_status"] == "no_public_independent_key" for r in assignments) and
                     all(r["independent_qa_status"] == "no_public_independent_key" and not r["reviewer_time_ms"] for r in evidence))
    return dict(value=None, unit=None, rows=None, denominator=None, admissible_rows=0,
                reasons=[QA_MISSING if found_missing else "qa_evidence_outside_audit_schema"],
                support_assignment_keys=assignment_keys,
                translator_support_rows=len(evidence), linked_qa_time_rows=len(linked),
                support_segment_keys=sorted(map(row_key, evidence)))


class StagedFiles:
    """Keep only preopened handles and account for all data read after installing seccomp."""
    def __init__(self):
        self.handles = {name: os.open(name, os.O_RDONLY | os.O_NOFOLLOW) for name in (BUNDLE, *PAYLOAD)}
        self.cache = {}
        self.reads = []

    def read(self, name):
        if name not in self.cache:
            handle = self.handles[name]
            parts = []
            while part := os.read(handle, 65536):
                parts.append(part)
            data = b"".join(parts)
            self.reads.append(dict(path=name, bytes=len(data), sha256=digest(data)))
            self.cache[name] = data
        return self.cache[name]

    def close(self):
        for fd in self.handles.values():
            os.close(fd)


def restrict_new_io():
    lib = ctypes.CDLL("libseccomp.so.2", use_errno=True)
    lib.seccomp_init.argtypes = [ctypes.c_uint32]
    lib.seccomp_init.restype = ctypes.c_void_p
    lib.seccomp_rule_add.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint]
    lib.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
    lib.seccomp_load.argtypes = [ctypes.c_void_p]
    lib.seccomp_release.argtypes = [ctypes.c_void_p]
    allow = 0x7FFF0000
    deny = 0x00050000 | errno.EPERM
    context = lib.seccomp_init(allow)
    invariant(context, "seccomp_init failed")
    try:
        for name in ("open", "openat", "openat2", "creat", "open_by_handle_at", "name_to_handle_at",
                     "socket", "socketpair", "connect", "io_uring_setup", "io_uring_enter", "io_uring_register",
                     "getdents", "getdents64", "readlink", "readlinkat", "stat", "lstat", "statx", "newfstatat",
                     "access", "faccessat", "faccessat2", "execve", "execveat", "clone", "clone3", "fork", "vfork"):
            syscall = lib.seccomp_syscall_resolve_name(name.encode())
            if syscall >= 0:
                invariant(lib.seccomp_rule_add(context, deny, syscall, 0) == 0, "seccomp rule failed: " + name)
        invariant(lib.seccomp_load(context) == 0, "seccomp_load failed")
    finally:
        lib.seccomp_release(context)
    probes = {}
    for label, try_io in (("new_open", lambda: os.open(BUNDLE, os.O_RDONLY)), ("socket", socket.socket)):
        try:
            opened = try_io()
        except OSError as failure:
            invariant(failure.errno == errno.EPERM, label + " failed without EPERM")
            probes[label] = "EPERM"
        else:
            os.close(opened) if isinstance(opened, int) else opened.close()
            raise RuntimeError(label + " still allowed")
    return probes


def reopen_excerpt(bundle, reader):
    source = Path(bundle["relative_path"]).name
    invariant(source in (SEGMENTS, ASSIGNMENTS), "unsupported citation source")
    expected_path = "/blob/" + bundle["revision"] + "/" + bundle["relative_path"]
    invariant(expected_path in bundle["url"], "citation revision/path mismatch")
    parts = [base64.b64decode(encoded, validate=True) for encoded in bundle["excerpt_base64"]]
    invariant(lines_digest(parts) == bundle["excerpt_sha256"], "stored window hash mismatch")
    windows = [(loc["first_line"], loc["last_line"]) for loc in bundle["locator"]]
    locator, local = quote(reader.read(source), windows)
    invariant(locator == bundle["locator"] and local == parts, "local citation bytes disagree")
    return source, csv_table(b"".join(parts))[1]


def worker():
    reader = StagedFiles()
    try:
        probes = restrict_new_io()
        bundle = json.loads(reader.read(BUNDLE))
        keys = set(bundle)
        invariant(keys in (A_FIELDS, A_FIELDS | set(B_FIELDS)), "unrecognized bundle schema")
        expanded = keys != A_FIELDS
        selector, claim = claim_from_sentence(bundle["sentence"])
        source, quoted_rows = reopen_excerpt(bundle, reader)
        policy = {field: bundle[field] for field in B_FIELDS} if expanded else None
        if expanded:
            invariant(policy == augmentation(selector), "unsupported semantic policy or display scope disagreement")
        trace = {"archived_source": source, "archived_locator": bundle["locator"], "archive_hash_match": True,
                 "quoted_keys": [row_key(row) if claim else row["slot_id"] for row in quoted_rows]}
        reasons = []
        if claim:
            invariant(source == SEGMENTS, "numeric claims require segment rows")
            candidate = quoted_rows
            if expanded:
                candidate, reasons, extra_trace = b_amount(policy["row_selector"], policy, reader, quoted_rows)
                trace.update(extra_trace)
            observed = observe_amount(candidate, claim, policy)
            if not all(matches(row, selector) for row in candidate):
                reasons.append("display_scope_mismatch")
            observed["reasons"].extend(reasons)
        else:
            invariant(source == ASSIGNMENTS, "withheld claim requires assignments for support")
            assignments = quoted_rows
            if expanded:
                _, universe = csv_table(reader.read(ASSIGNMENTS))
                assignments = [row for row in universe if matches(row, policy["row_selector"])]
            invariant(all(matches(row, selector) for row in assignments), "QA support scope mismatch")
            _, segments = csv_table(reader.read(SEGMENTS))
            observed = observe_qa(assignments, segments)
            trace["segment_rows_examined"] = len(segments)
        observed["reasons"] = sorted(set(observed["reasons"]))
        observed["status"] = "withheld" if observed["reasons"] else "confirmed"
        sys.stdout.buffer.write(encode(dict(scheme="B" if expanded else "A", claim=claim, observation=observed,
                                            trace=trace, io_guard=probes, preopened=list(reader.handles), reads=reader.reads)))
    finally:
        reader.close()


def changed_line(raw, data, identity):
    lines = raw.splitlines(keepends=True)
    fields, rows = csv_table(raw)
    matches_in_source = [i for i, row in enumerate(rows, 1) if row_key(row) == identity]
    invariant(len(matches_in_source) == 1, "control must target one original row")
    index = matches_in_source[0]
    newline = "\r\n" if lines[index].endswith(b"\r\n") else "\n"
    lines[index] = csv_bytes(fields, [data], newline, header=False)
    return b"".join(lines)


def display_amount(case, changed, line_windows):
    evidence = csv_table(b"".join(quote(changed, line_windows)[1]))[1]
    prefix = case["sentence"].split("의 PET", 1)[0]
    count = len(evidence)
    time = sum(int(row["event_time_ms"]) for row in evidence)
    words = sum(int(row["src_words"]) for row in evidence)
    return f"{prefix}의 PET 원 이벤트 {count}분절 합은 {time:,} ms, 영어 원문 {words:,}단어다."


def make_control(spec, original, payload):
    case = original | {"case_id": spec["case_id"], "kind": spec["id"]}
    updated = payload.copy()
    raw = payload[SEGMENTS]
    fields, rows = csv_table(raw)
    instance = [row for row in rows if matches(row, original["selector"])]
    altered_key = None
    generated = None
    if spec["id"] == "milliseconds_as_seconds":
        case["sentence"] = case["sentence"].replace(" ms,", " 초,")
    elif spec["id"] == "equal_sum_wrong_rows":
        target = instance[-1]
        generated = target | {"unit_id": target["unit_id"] + "-control-replacement",
                              "flores_id": "900000" + target["flores_id"],
                              "source_sha256": digest(b"AF-RES-207 synthetic alternate source")}
        altered_key = row_key(target)
        updated[SEGMENTS] = changed_line(raw, generated, altered_key)
    elif spec["id"] == "missing_as_zero":
        target = instance[-1]
        planned = ("slot_id", "language", "doc_id", "condition", "assigned_subject", "subject_id", "unit_id",
                   "segment_id", "flores_id", "item_id", "source_sha256", "src_words")
        generated = dict.fromkeys(fields, "") | {field: target[field] for field in planned}
        generated.update(raw_file_present="False", raw_xml_parsed="False", raw_job_status="GOING_ON",
                         unit_status="STARTED", raw_comparison_eligible="False", comparison_reason="control_imputation",
                         event_time_ms="0")
        altered_key = row_key(target)
        updated[SEGMENTS] = changed_line(raw, generated, altered_key)
        case["sentence"] = display_amount(case, updated[SEGMENTS], case["locator_lines"])
    elif spec["id"] == "duplicate_participant_observation":
        target = instance[0]
        generated = target | {"unit_id": target["unit_id"] + "-control-duplicate"}
        altered_key = row_key(target)
        updated[SEGMENTS] = raw + csv_bytes(fields, [generated], header=False)
        appended = len(rows) + 2
        case["locator_lines"] = [*case["locator_lines"], [appended, appended]]
        case["sentence"] = display_amount(case, updated[SEGMENTS], case["locator_lines"])
    else:
        raise ValueError("unknown control mutation")
    control = spec | dict(original_key=altered_key, generated_key=row_key(generated) if generated else None,
                          generated_rows=int(generated is not None), real_authority_rows=len(instance),
                          original_sha256=digest(raw), variant_sha256=digest(updated[SEGMENTS]),
                          resealed=True)
    return case, updated, control


def run_worker(case, scheme, bundle, staged_payload, output, raw_stdout, raw_stderr):
    bundle_data = encode(bundle)
    with tempfile.TemporaryDirectory(prefix=f"af207-{case['case_id']}-{scheme}-") as scratch_arg:
        scratch = Path(scratch_arg)
        code = Path(__file__).read_bytes()
        inventory = {BUNDLE: bundle_data} | staged_payload | {"audit.py": code}
        for name, data in inventory.items():
            (scratch / name).write_bytes(data)
        actual = sorted(p.name for p in scratch.iterdir())
        invariant(actual == sorted(inventory), "extra file in reader directory")
        trace_path = output / "trace.tmp"
        argv = ["strace", "-qq", "-e", "trace=open,openat,openat2,socket,connect",
                "-o", str(trace_path.resolve()), sys.executable, "-I", "-B", "audit.py", "_worker"]
        result = subprocess.run(argv, cwd=scratch, capture_output=True, stdin=subprocess.DEVNULL, timeout=30,
                                env={"LC_ALL": "C.UTF-8", "PATH": os.defpath, "TZ": "UTC"})
        os_trace = trace_path.read_text().splitlines() if trace_path.exists() else []
        trace_path.unlink(missing_ok=True)
        focus = [line for line in os_trace if any(f'"{name}"' in line for name in (BUNDLE, *PAYLOAD)) or
                 line.startswith(("socket(", "connect("))]
        opened = [name for name in (BUNDLE, *PAYLOAD) if any(f'"{name}"' in line and " = -" not in line for line in focus)]
        raw_stdout.write(result.stdout)
        raw_stderr.write(result.stderr)
        view = json.loads(result.stdout) if result.returncode == 0 else None
        if view is not None:
            invariant(set(opened) == set(view["preopened"]) == {BUNDLE, *PAYLOAD}, "unexpected opened input paths")
            invariant(any("EPERM" in line and "socket(" in line for line in focus) and
                      any("EPERM" in line and '"bundle.json"' in line for line in focus), "guard was not observed by strace")
            invariant(view["scheme"] == scheme, "unexpected observed scheme")
    return dict(case_id=case["case_id"], kind=case["kind"], scheme=scheme, stage_entries=actual,
                inventory={name: dict(bytes=len(data), sha256=digest(data)) for name, data in inventory.items()},
                bundle_sha256=digest(bundle_data), bundle_bytes=len(bundle_data), worker_exit=result.returncode,
                stdout_bytes=len(result.stdout), stdout_sha256=digest(result.stdout), stderr_bytes=len(result.stderr),
                stderr_sha256=digest(result.stderr), syscall_trace=focus, other_bootstrap_trace_lines=len(os_trace)-len(focus),
                result=view)


def cost_record(case, a, b, payload):
    running = a.copy()
    start = len(encode(running))
    size = start
    increments = {}
    for name in B_FIELDS:
        running[name] = b[name]
        new_size = len(encode(running))
        increments[name + "_delta"] = new_size - size
        size = new_size
    invariant(running == b and len(encode(b)) - start == sum(increments.values()), "cost delta mismatch")
    return dict(case_id=case["case_id"], phase="core", a_bytes=start, b_bytes=size, additional_bytes=size-start,
                common_payload_bytes=sum(map(len, payload.values())), **increments)


def registry_cost(extras):
    registry = {}
    references = {}
    for case_id, rules in extras.items():
        references[case_id] = {}
        for field, value in rules.items():
            items = registry.setdefault(field, [])
            if value not in items:
                items.append(value)
            references[case_id][field] = items.index(value)
    inline = {case: rules for case, rules in extras.items()}
    pooled = {"rules": registry, "cases": references}
    return dict(inline_rule_map_bytes=len(encode(inline)), shared_rule_map_bytes=len(encode(pooled)),
                unique_rules=sum(map(len, registry.values())), inline_rule_count=sum(map(len, inline.values())),
                references_count=sum(map(len, references.values())), registry=pooled)


def run_observations(args):
    inputs = file_json(args.inputs)
    phase = args.phase
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    started = dt.datetime.now(dt.UTC).isoformat()
    payload = load_payload(args.repo, inputs)
    slots = {case["case_id"]: case for case in inputs["slots"]}
    if phase == "core":
        jobs = [(case, payload, None) for case in slots.values()]
    else:
        jobs = [make_control(spec, slots[spec["parent"]], payload) for spec in inputs["control_plan"]]
    receipts, costs, extras = [], [], {}
    with (output / "worker.stdout.jsonl").open("wb") as raw_stdout, (output / "worker.stderr").open("wb") as raw_stderr:
        for case, same_payload, control in jobs:
            a, b = bundle_for(case, same_payload, inputs)
            for scheme, bundle in (("A", a), ("B", b)):
                record = run_worker(case, scheme, bundle, same_payload, output, raw_stdout, raw_stderr)
                receipts.append(record | {"control": control, "phase": phase})
            if phase == "core":
                costs.append(cost_record(case, a, b, same_payload))
                extras[case["case_id"]] = {name: b[name] for name in B_FIELDS}
    write_jsonl(output / "observations.jsonl", receipts)
    write_jsonl(output / "bytes.jsonl", costs)
    if extras:
        (output / "rule-registry.json").write_bytes(encode(registry_cost(extras)))
    errors = sum(row["worker_exit"] != 0 for row in receipts)
    completed = dt.datetime.now(dt.UTC).isoformat()
    (output / "run.json").write_bytes(encode(dict(phase=phase, start_utc=started, end_utc=completed,
        argv=sys.argv, worker_argv="strace -qq -e trace=open,openat,openat2,socket,connect -o TRACE python3 -I -B audit.py _worker",
        python=platform.python_version(), platform=platform.platform(),
        seccomp=subprocess.check_output(["dpkg-query", "-W", "-f=${Version}", "libseccomp2"], text=True),
        strace=subprocess.check_output(["strace", "--version"], text=True).splitlines()[0], git=git(args.repo, "--version").decode().strip(),
        source_sha256=digest(Path(__file__).read_bytes()), inputs_sha256=digest(args.inputs.read_bytes()),
        repository_head=git(args.repo,"rev-parse","HEAD").decode().strip(),
        staged_input_sha256={name:digest(data) for name,data in payload.items()},
        output_sha256={p.name:digest(p.read_bytes()) for p in sorted(output.iterdir())},
        expected_workers=2*len(jobs), actual_workers=len(receipts), worker_failures=errors, exit_code=int(errors > 0))))
    print(f"{phase}: {len(receipts)} observation workers, {errors} execution failures")
    return int(errors > 0)


def score_one(record, expected, control=None):
    observation = record["result"]["observation"] if record["result"] else {}
    if record["worker_exit"]:
        return "실행 실패", {}, observation
    axes = {name: observation[name] == expected[name] for name in ("value", "unit", "rows", "denominator")}
    if control:
        axes["reason"] = control["expected_reason"] in observation["reasons"]
        if observation["status"] == "confirmed":
            return "오승인", axes, observation
        return ("합리적 보류" if axes["reason"] else "근거 다른 보류"), axes, observation
    axes["reason"] = observation["reasons"] == expected["reasons"]
    axes["support"] = observation["support_assignment_keys"] == expected["support_assignment_keys"]
    if observation["status"] == "withheld":
        outcome = "합리적 보류" if expected["status"] == "withheld" and all(axes.values()) else "과잉 보류"
    else:
        outcome = "정답" if expected["status"] == "confirmed" and all(axes.values()) else "오승인"
    return outcome, axes, observation


def score_results(args):
    gold = file_json(args.gold)
    main = {row["case_id"]: row for row in gold["main"]}
    controls = {row["case_id"]: row for row in gold["controls"]}
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    scored = {}
    byte_records = []
    sequences = {}
    fingerprints = {}
    for directory in args.runs:
        run_data = file_json(directory / "run.json")
        phase = run_data["phase"]
        invariant(phase not in sequences, "duplicate run phase")
        sequences[phase] = []
        for name, wanted in run_data["output_sha256"].items():
            invariant(digest((directory / name).read_bytes()) == wanted, "observation file differs from run receipt")
        fingerprints[phase] = digest((directory / "run.json").read_bytes())
        for index, record in enumerate(read_jsonl(directory / "observations.jsonl"), 1):
            case = record["case_id"]
            scheme = record["scheme"]
            control = controls[case] if phase == "controls" else None
            expected = main[control["authority_case"] if control else case]
            key = (phase, case, scheme)
            invariant(key not in scored, "duplicate measurement")
            label, axes, observation = score_one(record, expected, control)
            scored[key] = dict(outcome=label, value=observation.get("value"), unit=observation.get("unit"),
                               row_keys=observation.get("rows"), denominator=observation.get("denominator"),
                               reasons=observation.get("reasons"), axes=axes,
                               receipt=f"receipts/{phase}.jsonl#L{index}")
            if case not in sequences[phase]:
                sequences[phase].append(case)
        byte_records.extend(read_jsonl(directory / "bytes.jsonl"))
    fields = ("outcome", "value", "unit", "row_keys", "denominator", "reasons", "axes", "receipt")
    matrix = []
    tallies = Counter()
    for phase, cases in sequences.items():
        invariant(set(cases) == (set(main) if phase == "core" else set(controls)), "incomplete measurement phase")
        for case in cases:
            expressions = [("A",), ("B",)] if phase == "core" else [("A", "B")]
            for versions in expressions:
                kind = main[case]["kind"] if phase == "core" else "control"
                row = dict(phase=phase, case_id=case, kind=kind, expression="/".join(versions))
                for scheme in versions:
                    entry = scored[phase, case, scheme]
                    row.update({scheme.lower() + "_" + key: encode(value).decode().strip() if isinstance(value, (dict, list)) else value
                                for key, value in entry.items()})
                    tallies[phase, kind, scheme, entry["outcome"]] += 1
                matrix.append(row)
    columns = ["phase", "case_id", "kind", "expression"] + [f"{scheme}_{field}" for scheme in ("a","b") for field in fields]
    (out / "matrix.csv").write_bytes(csv_bytes(columns, matrix))
    if byte_records:
        (out / "costs.csv").write_bytes(csv_bytes(list(byte_records[0]), byte_records))
    counters = [dict(phase=p, kind=k, scheme=s, outcome=o, count=n) for (p,k,s,o),n in sorted(tallies.items())]
    (out / "score.json").write_bytes(encode(dict(gold_sha256=digest(args.gold.read_bytes()), run_sha256=fingerprints,
        logical_matrix_rows=len(matrix), scored_worker_results=len(scored), tallies=counters, exit_code=0)))
    print(f"scored {len(scored)} worker results as {len(matrix)} logical matrix rows")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="mode", required=True)
    observe = commands.add_parser("observe")
    for name in ("inputs", "repo", "out"):
        observe.add_argument("--" + name, required=True, type=Path)
    observe.add_argument("--phase", choices=("core", "controls"), required=True)
    score = commands.add_parser("score")
    score.add_argument("--gold", type=Path, required=True)
    score.add_argument("--runs", type=Path, nargs="+", required=True)
    score.add_argument("--out", type=Path, required=True)
    commands.add_parser("_worker")
    args = parser.parse_args()
    if args.mode == "_worker":
        worker()
        return 0
    if args.mode == "observe":
        return run_observations(args)
    return score_results(args)


if __name__ == "__main__":
    raise SystemExit(main())
