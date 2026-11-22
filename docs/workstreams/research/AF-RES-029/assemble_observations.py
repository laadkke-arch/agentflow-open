"""Deterministic, offline provenance assembly for AF-RES-029.

Run with python -B.  This is a bookkeeper, not a selector or a semantic judge.
The default mode requires all 36 gated packets and verified input/common/route
seals.  --allow-incomplete is a read-only schema check and never writes ledgers.
No source ledger, receipt, packet, seal, or repository state is modified.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urldefrag, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
UNKNOWN = "미확인"
UNMEASURED = "미계측"
SCHEMA = "AF-RES-029-observation-assembly-v1"
QIDS = [f"Q{number:02d}" for number in range(1, 13)]
WEB_COMMANDS = (
    "system1_search_query", "system2_search_query", "open", "click", "find",
    "screenshot", "image_query",
)
SEARCH_COMMANDS = {"system1_search_query", "system2_search_query", "image_query"}
COUNT_KEYS = (
    "counted", "counted_minimum", "counted_eligibility", "counting_eligibility",
    "count_eligibility", "countability", "count_category", "counting_basis",
)
RECEIPT_KEYS = ("receipt", "receipt_path", "receipt_file", "receipt_files", "recovery_receipt")
SUPPORT_FILE_KEYS = ("body_file", "stored_path", "capture_file")
FAILURE_RE = re.compile(
    r"Failed to fetch|Internal Error \(\)|HTTP (?:403|404|429|500|502|503)|"
    r"Too Many Requests|content length is too large", re.I,
)
HEADER_RE = re.compile(r"^([^\n]*) \((https?://[^\n]+)\)\r?\n【([^】]+)】", re.M)
LINE_RE = re.compile(r"^L(\d+)(?:@P\d+)?:", re.M)
REFERENCE_RE = re.compile(r"^【([^】]+)】\s*\[wordlim", re.M)
TRACKING_KEYS = {"highlight", "fbclid", "gclid", "mc_cid", "mc_eid"}


def digest(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def first_present(record, names, default=UNKNOWN):
    for name in names:
        value = record.get(name)
        if value is not None and value != "" and value != [] and value != {}:
            return value
    return default


def as_list(value):
    if value is None or value == "":
        return []
    return value if isinstance(value, list) else [value]


def unique(values):
    answer = []
    seen = set()
    for value in values:
        key = canonical_json(value)
        if key not in seen:
            seen.add(key)
            answer.append(value)
    return answer


def is_url(value):
    return isinstance(value, str) and value.startswith(("https://", "http://"))


def normalized_document_url(value):
    """Citation membership identity: retain editions and meaningful parameters.

    This is deliberately narrower than conservative counting identity.  It only
    removes fragments/tracking and makes exact GitHub raw/blob mirrors equal.
    A numbered manual is not deemed cited because another edition was cited.
    """
    if not is_url(value):
        return None
    part = urlsplit(value)
    host = part.netloc.lower()
    path = part.path or "/"
    query = [(key, val) for key, val in parse_qsl(part.query, keep_blank_values=True)
             if key.lower() not in TRACKING_KEYS and not key.lower().startswith("utm_")]
    if host == "raw.githubusercontent.com":
        bits = path.lstrip("/").split("/", 3)
        if len(bits) == 4:
            owner, repo, revision, rest = bits
            host, path = "github.com", f"/{owner}/{repo}/blob/{revision}/{rest}"
    if host == "github.com" and "/blob/" in path:
        query = [(key, val) for key, val in query if key not in {"plain", "raw"}]
    return urlunsplit((part.scheme.lower(), host, path, urlencode(sorted(query)), ""))


def counting_identity(value):
    """Collapse document editions, never unrelated API/reference paths."""
    normalized = normalized_document_url(value)
    if normalized is None:
        return None, []
    part = urlsplit(normalized)
    host, path = part.netloc.lower(), unquote(part.path)
    notes = []
    if normalized != value:
        notes.append("Fragments/tracking removed; exact GitHub raw/blob mirrors normalized.")
    numpy_path = None
    if host in {"numpy.org", "www.numpy.org"}:
        match = re.match(r"/(?:doc/[^/]+|devdocs)/(.*)$", path)
        if match:
            numpy_path = match.group(1)
    elif host == "github.com":
        match = re.match(r"/numpy/numpy/blob/[^/]+/doc/source/(.+)$", path)
        if match:
            numpy_path = match.group(1)
    if numpy_path is not None:
        numpy_path = re.sub(r"\.(?:html|rst|md|txt)$", "", numpy_path)
        notes.append("NumPy editions/aliases and source/rendered copies of this exact document path count once; version evidence remains separate.")
        return "numpy-manual:" + numpy_path, notes
    python_path = None
    if host == "docs.python.org":
        match = re.match(r"/(?:release/)?(?:\d+(?:\.\d+)*(?:[a-z]+\d*)?|dev|latest)/(?:[a-z]{2}(?:-[A-Z]{2})?/)?(.+)$", path)
        if match:
            python_path = match.group(1)
    elif host == "github.com":
        match = re.match(r"/python/cpython/blob/[^/]+/Doc/(.+)$", path)
        if match:
            python_path = match.group(1)
    if python_path is not None:
        python_path = re.sub(r"\.(?:html|rst|md|txt)$", "", python_path)
        if python_path == "library/functions":
            python_path = "builtins/functions"
            notes.append("CPython library/functions source and builtins/functions rendered chapter are the built-in-functions manual chapter.")
        notes.append("Python manual editions and source/rendered copies of this exact chapter count once; distinct API chapters remain distinct.")
        return "python-manual:" + python_path, notes
    hacking = False
    if host in {"go.dev", "golang.org", "golang.google.cn"}:
        hacking = bool(re.fullmatch(r"/src/runtime/HACKING(?:\.md|\.html)?/?", path))
    elif host == "github.com":
        hacking = bool(re.fullmatch(r"/golang/go/blob/[^/]+/src/runtime/HACKING\.md", path))
    elif host == "go.googlesource.com":
        hacking = bool(re.fullmatch(r"/go/\+/[^/]+/src/runtime/HACKING\.md", path))
    if hacking:
        notes.append("Official Go runtime HACKING mirrors/revisions form one conservative document family; URLs and revisions remain intact.")
        return "go-source:src/runtime/HACKING.md", notes
    return "document:" + normalized, notes


def line_ranges(numbers):
    ranges = []
    for number in sorted(set(numbers)):
        if ranges and number == ranges[-1]["end"] + 1:
            ranges[-1]["end"] = number
        else:
            ranges.append({"start": number, "end": number})
    return ranges


def response_metadata(response):
    texts = []
    if isinstance(response, dict):
        texts = [block["text"] for block in response.get("content", [])
                 if isinstance(block, dict) and isinstance(block.get("text"), str)]
    elif isinstance(response, str):
        texts = [response]
    text = "\n".join(texts)
    headers = [{"title": m.group(1), "url": m.group(2), "ref_id": m.group(3)}
               for m in HEADER_RE.finditer(text)]
    documents = []
    matches = list(HEADER_RE.finditer(text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        fragment = text[match.start():end]
        documents.append({
            "original_url": match.group(2), "source_ref": match.group(3),
            "actually_returned_line_ranges": line_ranges(map(int, LINE_RE.findall(fragment))),
        })
    return {
        "headers": headers,
        "documents": documents,
        "source_refs": unique(REFERENCE_RE.findall(text)),
        "actually_returned_line_ranges": line_ranges(map(int, LINE_RE.findall(text))),
        "local_text_utf8_bytes": len(text.encode("utf-8")),
        "failure_marker": bool(FAILURE_RE.search(text)),
        "tool_is_error": bool(isinstance(response, dict) and response.get("isError")),
    }


class Assembly:
    def __init__(self, allow_incomplete=False):
        self.allow_incomplete = allow_incomplete
        self.consumed_files = {}
        self.json_cache = {}
        self.warnings = []
        self.seals = {}
        self.sealed_paths = {}
        self.sources = []
        self.attempts = []
        self.visits = []
        self.routes = []
        self.returns = []
        self.citations = []
        self.raw_sources = []
        self.starts = {}
        self.route_records = {}
        self.packets = {}

    def warn(self, code, **details):
        self.warnings.append({"code": code, **details})

    def relative(self, path):
        return str(path.resolve().relative_to(ROOT))

    def local_path(self, value):
        if not isinstance(value, str) or is_url(value) or value in {UNKNOWN, UNMEASURED}:
            return None
        clean = value.split("#", 1)[0]
        path = Path(clean)
        if not path.is_absolute():
            path = (REPO / path) if clean.startswith("docs/") else (ROOT / path)
        path = path.resolve()
        if not path.is_relative_to(ROOT):
            return None
        return path

    def read_bytes(self, path):
        data = path.read_bytes()
        relative = self.relative(path)
        old = self.consumed_files.get(relative)
        actual = digest(data)
        if old is not None and old != actual:
            raise ValueError(f"Input changed during assembly: {relative}")
        self.consumed_files[relative] = actual
        return data

    def read_json(self, path):
        relative = self.relative(path)
        if relative not in self.json_cache:
            self.json_cache[relative] = json.loads(self.read_bytes(path))
        return self.json_cache[relative]

    def read_jsonl(self, path):
        rows = []
        for ordinal, line in enumerate(self.read_bytes(path).decode("utf-8").splitlines(), 1):
            if not line.strip():
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"Expected JSON object: {self.relative(path)}:{ordinal}")
            rows.append((ordinal, line, record))
        return rows

    def file_reference(self, path):
        if not path.exists():
            return {"path": self.relative(path), "exists": False, "sha256": UNKNOWN}
        self.read_bytes(path)
        relative = self.relative(path)
        return {
            "path": relative, "exists": True, "sha256": self.consumed_files[relative],
            "sealed_by": sorted(self.sealed_paths.get(relative, [])),
        }

    def validate_seals(self):
        for name in ("input-seal.json", "common-seal.json", "route-seal.json"):
            path = ROOT / "evidence" / name
            if not path.exists():
                if not self.allow_incomplete:
                    raise ValueError(f"Required seal absent: evidence/{name}")
                self.warn("missing_seal_read_only_check", file=f"evidence/{name}")
                continue
            record = self.read_json(path)
            files = record.get("files")
            if not isinstance(files, dict) or not files:
                raise ValueError(f"Seal has no file-hash mapping: evidence/{name}")
            self.seals[name] = record
            for relative, expected in sorted(files.items()):
                target = self.local_path(relative)
                if target is None or not target.exists():
                    raise ValueError(f"Sealed input absent/invalid: {name}: {relative}")
                actual = digest(self.read_bytes(target))
                if actual != expected:
                    raise ValueError(f"Sealed hash mismatch: {name}: {relative}")
                self.sealed_paths.setdefault(self.relative(target), []).append(name)

    def require(self, path, label):
        if path.exists():
            return True
        if not self.allow_incomplete:
            raise ValueError(f"Required {label} absent: {self.relative(path)}")
        self.warn("incomplete_input", file=self.relative(path), role=label)
        return False

    def load_inputs(self):
        self.validate_seals()
        self.questions = [row for _, _, row in self.read_jsonl(ROOT / "questions.jsonl")]
        identifiers = [q.get("id", q.get("question_id")) for q in self.questions]
        if sorted(identifiers) != QIDS:
            raise ValueError("Expected the same twelve unique frozen question IDs Q01–Q12")
        self.questions_by_id = dict(zip(identifiers, self.questions))
        initial = ROOT / "sources-initial.jsonl"
        if not initial.exists():
            raise ValueError("sources-initial.jsonl absent; no inferred replacement aggregate is permitted")
        source_files = [(initial, "initial", None)]
        for qid in QIDS:
            common = ROOT / "common" / qid
            start_path = common / "start.json"
            if self.require(start_path, "common start"):
                self.starts[qid] = self.read_json(start_path)
            for route in ("C", "A", "B"):
                directory = common if route == "C" else ROOT / "routes" / route / qid
                source_path = directory / "sources.jsonl"
                if self.require(source_path, "source ledger"):
                    source_files.append((source_path, route, qid))
                return_path = directory / ("baseline-return.json" if route == "C" else "return.json")
                if self.require(return_path, "gated return"):
                    packet = self.read_json(return_path)
                    self.validate_return(packet, return_path, qid, route)
                    self.packets[qid, route] = packet
                    enriched = dict(packet)
                    if "source_file" in enriched or "source_sha256" in enriched:
                        raise ValueError("Original packet already uses the two reserved assembly keys")
                    enriched["source_file"] = self.relative(return_path)
                    enriched["source_sha256"] = self.consumed_files[self.relative(return_path)]
                    self.returns.append(enriched)
                    for candidate_index, candidate in enumerate(packet.get("candidates", []), 1):
                        for citation_index, citation in enumerate(candidate.get("citations", []), 1):
                            self.citations.append({
                                "question_id": qid, "route": route,
                                "candidate_rank": candidate.get("rank", candidate_index),
                                "citation_ordinal": citation_index,
                                "source_id": citation.get("source_id", UNKNOWN),
                                "original_url": citation["url"], "section": citation["section"],
                                "normalized_document_url": normalized_document_url(citation["url"]),
                                "return_file": self.relative(return_path),
                                "return_sha256": enriched["source_sha256"],
                            })
                if route != "C":
                    route_path = directory / "route.json"
                    if self.require(route_path, "route record"):
                        self.route_records[qid, route] = self.read_json(route_path)
                    self.require(ROOT / "route-inputs" / route / f"{qid}.json", "frozen route input")
        for path, origin, qid in source_files:
            for ordinal, raw_line, record in self.read_jsonl(path):
                self.raw_sources.append({
                    "path": path, "origin": origin, "question_id": qid,
                    "line": ordinal, "line_sha256": digest(raw_line), "record": record,
                })
        exact = [item for item in self.raw_sources
                 if item["origin"] == "initial" and item["record"].get("counted") is True]
        if len(exact) != 12:
            raise ValueError(f"Frozen initial aggregate has {len(exact)} true counted flags, expected exactly 12")

    def validate_return(self, packet, path, qid, route):
        if packet.get("question_id") != qid or packet.get("route") != route:
            raise ValueError(f"Return identity mismatch: {self.relative(path)}")
        candidates = packet.get("candidates")
        if not isinstance(candidates, list) or len(candidates) > 3:
            raise ValueError(f"Original candidate cap/type violation: {self.relative(path)}")
        documents = set()
        for ordinal, candidate in enumerate(candidates, 1):
            if candidate.get("rank") != ordinal or not candidate.get("citations"):
                raise ValueError(f"Original rank/citation gate mismatch: {self.relative(path)}")
            for citation in candidate["citations"]:
                if not is_url(citation.get("url")) or not citation.get("section"):
                    raise ValueError(f"Original citation gate mismatch: {self.relative(path)}")
                documents.add(urldefrag(citation["url"])[0])
        gate = packet.get("serialization_gate", {})
        if (len(documents) > 3 or gate.get("candidate_count") != len(candidates)
                or gate.get("url_count") != len(documents)
                or set(gate.get("distinct_document_urls", [])) != documents
                or gate.get("posthoc_truncation") is not False):
            raise ValueError(f"Original serialization gate does not match packet: {self.relative(path)}")
        required_seal = "common-seal.json" if route == "C" else "route-seal.json"
        if not self.allow_incomplete and required_seal not in self.sealed_paths.get(self.relative(path), []):
            raise ValueError(f"Return is not in {required_seal}: {self.relative(path)}")

    def scan_visits(self):
        for qid in QIDS:
            for route in ("C", "A", "B"):
                directory = ROOT / "common" / qid if route == "C" else ROOT / "routes" / route / qid
                for path in sorted(directory.rglob("*.json")) if directory.exists() else []:
                    record = self.read_json(path)
                    if not isinstance(record, dict) or "request" not in record:
                        continue
                    if "response" not in record and not ("ended_utc" in record and ("error" in record or "thrown_error" in record)):
                        continue  # Plans, source records, and cache reads are not web operations.
                    request = record["request"]
                    if not isinstance(request, dict):
                        raise ValueError(f"Non-object web request: {self.relative(path)}")
                    commands = [(command, argument) for command in WEB_COMMANDS
                                for argument in as_list(request.get(command))]
                    if not commands:
                        continue
                    if len(commands) != 1:
                        raise ValueError(f"A receipt has multiple web operations; explicit per-operation debits needed: {self.relative(path)}")
                    command, argument = commands[0]
                    if route == "C":
                        default_navigation = int(command in SEARCH_COMMANDS)
                        default_body = int(command not in SEARCH_COMMANDS)
                    else:
                        default_navigation = None
                        default_body = None
                    debit = record.get("budget_debit", {})
                    navigation = record.get("navigation_debit", debit.get("navigation", default_navigation))
                    body = record.get("body_open_debit", debit.get("body_opens", default_body))
                    if type(navigation) is not int or type(body) is not int or navigation < 0 or body < 0:
                        raise ValueError(f"Explicit A/B operation debit missing/invalid: {self.relative(path)}")
                    response = record.get("response")
                    parsed = response_metadata(response)
                    explicit_error = first_present(record, ("error", "thrown_error"), default=None)
                    status = first_present(record, ("status",), default=None)
                    failed = bool(parsed["failure_marker"] or parsed["tool_is_error"] or explicit_error
                                  or (isinstance(status, str) and re.search(r"fail|error", status, re.I)))
                    if status is None:
                        status = "fetch_failed" if failed else "search_response" if command in SEARCH_COMMANDS else "original_line_response" if parsed["actually_returned_line_ranges"] else "metadata_or_unverified_response"
                    requested_urls = []
                    if is_url(record.get("requested_url")):
                        requested_urls.append(record["requested_url"])
                    if isinstance(argument, dict):
                        for key in ("ref_id", "url"):
                            if is_url(argument.get(key)):
                                requested_urls.append(argument[key])
                    rank_list, rank_basis = [], UNKNOWN
                    for key in ("provided_result_order", "provided_rank_list", "provided_hits"):
                        if key in record:
                            rank_list, rank_basis = record[key], f"{self.relative(path)}#{key}"
                            break
                    if not rank_list and route == "C" and command in SEARCH_COMMANDS:
                        start = self.starts.get(qid, {})
                        for key in ("top_ten", "search_results"):
                            if key in start:
                                rank_list, rank_basis = start[key], f"common/{qid}/start.json#{key}"
                                break
                    elapsed = record.get("elapsed_ms", UNKNOWN)
                    if elapsed == UNKNOWN and record.get("started_utc") and record.get("ended_utc"):
                        try:
                            elapsed = round((datetime.fromisoformat(record["ended_utc"].replace("Z", "+00:00")) - datetime.fromisoformat(record["started_utc"].replace("Z", "+00:00"))).total_seconds() * 1000, 3)
                        except ValueError:
                            pass
                    relative = self.relative(path)
                    visit = {
                        "schema": SCHEMA, "visit_id": "V-" + digest(relative)[:16],
                        "question_id": qid, "route": route,
                        "stage": first_present(record, ("stage", "operation", "operation_type"), "common" if route == "C" else "route"),
                        "operation_type": command,
                        "recorded_operation_type": first_present(record, ("operation_type", "operation", "stage")),
                        "tool": record.get("tool", UNKNOWN), "request": request,
                        "raw_query": argument.get("q", UNKNOWN) if command in SEARCH_COMMANDS and isinstance(argument, dict) else None,
                        "requested_urls": unique(requested_urls),
                        "response_original_urls": unique([header["url"] for header in parsed["headers"]]),
                        "response_source_refs": parsed["source_refs"],
                        "provided_rank_list": rank_list, "provided_rank_list_basis": rank_basis,
                        "provided_order_is_certified_global_rank": False,
                        "started_utc": record.get("started_utc", UNKNOWN),
                        "ended_utc": record.get("ended_utc", UNKNOWN), "elapsed_ms": elapsed,
                        "elapsed_basis": record.get("elapsed_basis", "Recorded tool invocation elapsed; no human-labor inference."),
                        "navigation_debit": navigation, "body_open_debit": body,
                        "dual_debit": bool(navigation and body),
                        "within_page_find": command == "find",
                        "find_additional_navigation_sensitivity": int(command == "find" and navigation == 0),
                        "status": status, "fetch_failed": failed,
                        "error": explicit_error if explicit_error is not None else None,
                        "actual_returned_line_ranges": parsed["actually_returned_line_ranges"],
                        "returned_documents": parsed["documents"],
                        "line_range_basis": "Only numbered lines literally delivered in the saved response; Total lines is never treated as read.",
                        "recorded_returned_line_ranges": first_present(record, ("actual_returned_line_ranges", "returned_line_ranges"), []),
                        "original_text_lines_returned": bool(parsed["actually_returned_line_ranges"]),
                        "substantive_original_body_read": False,
                        "server_transfer_bytes": UNMEASURED, "server_token_cost": UNMEASURED,
                        "local_response_canonical_json_utf8_bytes": len(canonical_json(response).encode("utf-8")),
                        "local_response_text_utf8_bytes": parsed["local_text_utf8_bytes"],
                        "local_receipt_file_bytes": path.stat().st_size,
                        "recorded_local_bytes": {key: val for key, val in record.items() if "bytes" in key and ("local" in key or "excerpt" in key)},
                        "local_byte_measurement_limit": "Saved UTF-8 serialization size, not transferred bytes or token cost.",
                        "receipt": relative, "receipt_sha256": self.consumed_files[relative],
                        "response_sha256_canonical_json": digest(canonical_json(response)),
                        "recorded_response_sha256": record.get("response_sha256", UNKNOWN),
                        "selection_receipt": record.get("selection_receipt", UNKNOWN),
                        "original_parent_link_evidence": record.get("original_parent_link_evidence", UNKNOWN),
                        "original_receipt_metadata": {key: val for key, val in record.items() if key != "response"},
                        "cache_read_counted_as_request": False,
                    }
                    self.visits.append(visit)
        self.visits.sort(key=lambda row: (row["question_id"], {"C": 0, "A": 1, "B": 2}[row["route"]], row["started_utc"], row["receipt"]))
        self.visits_by_path = {row["receipt"]: row for row in self.visits}
        for (qid, route) in {(row["question_id"], row["route"]) for row in self.visits}:
            seen = collections.Counter()
            for visit in [v for v in self.visits if v["question_id"] == qid and v["route"] == route]:
                # Exact request repeat is observable; a changed-line expansion is not labeled a retry.
                key = canonical_json(visit["request"])
                seen[key] += 1
                visit["same_request_attempt_ordinal"] = seen[key]
                visit["repeated_exact_request"] = seen[key] > 1

    def source_receipts(self, original):
        refs = []
        for key in RECEIPT_KEYS + SUPPORT_FILE_KEYS:
            for value in as_list(original.get(key)):
                path = self.local_path(value)
                if path is None:
                    refs.append({"original_reference": value, "role": key, "path": UNKNOWN, "exists": False, "sha256": UNKNOWN})
                else:
                    refs.append({"original_reference": value, "role": key, **self.file_reference(path)})
        return unique(refs)

    @staticmethod
    def declared_eligibility(original):
        flags = []
        for key in COUNT_KEYS:
            value = original.get(key)
            if isinstance(value, bool):
                flags.append((key, value))
            elif isinstance(value, dict) and isinstance(value.get("eligible"), bool):
                flags.append((key + ".eligible", value["eligible"]))
        if not flags:
            return UNKNOWN, []
        return all(value for _, value in flags), flags

    def normalize_sources(self):
        for item in self.raw_sources:
            original = item["record"]
            origin, qid = item["origin"], item["question_id"]
            kind = first_present(original, ("type", "kind"))
            lowered = str(kind).lower()
            linked = original.get("linked", {}) if isinstance(original.get("linked"), dict) else {}
            questions = []
            for key in ("question_id", "linked_question", "linked_questions", "question_links"):
                questions.extend(as_list(original.get(key)))
            questions.extend(as_list(linked.get("question")))
            if qid:
                questions.append(qid)
            questions = unique([value for value in questions if isinstance(value, str) and re.fullmatch(r"Q\d{2}", value)])
            receipts = self.source_receipts(original)
            visits = unique([self.visits_by_path[ref["path"]] for ref in receipts if ref.get("path") in self.visits_by_path])
            body_visits = [visit for visit in visits if visit["operation_type"] not in SEARCH_COMMANDS]
            source_url = first_present(original, ("original_url", "url"), None)
            url_basis = "Original source row URL"
            if not is_url(source_url):
                urls = unique([url for visit in body_visits for url in visit["response_original_urls"]])
                if len(urls) == 1:
                    source_url, url_basis = urls[0], "Single original URL in the associated saved body-response header"
                else:
                    source_url, url_basis = UNKNOWN, UNKNOWN
            associated_urls = unique([url for url in [source_url] + [url for visit in body_visits for url in visit["response_original_urls"]] if is_url(url)])
            document_urls = unique([normalized_document_url(url) for url in associated_urls])
            sections = first_present(original, ("read_sections", "directly_read_sections", "actually_read_sections"))
            finding = first_present(original, ("finding", "verified", "verified_finding", "checked_fact"))
            limitations = first_present(original, ("limitations", "limitations_unverified", "limitation"))
            eligible, eligibility_fields = self.declared_eligibility(original)
            exact_initial = origin == "initial" and original.get("counted") is True
            frozen_reuse = origin != "initial" and ("frozen_initial" in lowered or linked.get("stage") == "frozen_input" or original.get("stage") == "frozen_input")
            explicit_false_read = original.get("direct_original_read") is False or original.get("original_body_read") is False
            explicit_true_read = original.get("direct_original_read") is True or original.get("original_body_read") is True
            flags_text = canonical_json({key: original.get(key) for key in COUNT_KEYS if key in original}).lower()
            failure_kind = any(token in lowered for token in ("failed", "fetch_failure", "fetch_error"))
            snippet_kind = any(token in lowered for token in ("snippet", "search_navigation", "search_receipt"))
            provenance_kind = any(token in lowered for token in ("metadata", "provenance", "recovery", "nonselected", "later_draft"))
            locator_kind = "locator" in lowered or "document_find" in lowered
            index_only = eligible is not True and ("reference_index" in lowered or "catalog" in lowered) and any(token in flags_text for token in ("index only", "catalog only", "not returned", "navigation"))
            successful_lines = any(visit["original_text_lines_returned"] and not visit["fetch_failed"] for visit in body_visits)
            explicit_substantive = sections != UNKNOWN and finding != UNKNOWN
            if exact_initial:
                direct_read, category, reason = True, "first_design", "Exact true counted flag in the frozen initial aggregate; first-text reading is recorded."
            elif origin == "initial":
                direct_read, category, reason = UNKNOWN, "initial_provenance_or_attempt", "Initial aggregate explicitly excludes this row from the twelve first originals; metadata/recovery/nonselected reading is not promoted."
            elif (failure_kind or explicit_false_read or original.get("summary_only") is True
                  or (body_visits and all(visit["fetch_failed"] for visit in body_visits))):
                direct_read, category, reason = False, "failed_or_nonoriginal_attempt", "Explicit failed/nonoriginal/summary-only reading flag."
            elif snippet_kind or provenance_kind or locator_kind or index_only:
                direct_read, category, reason = False, "navigation_metadata_or_provenance_attempt", "Snippet, metadata/provenance, locator, or navigation-only index; no substantive original promoted."
            elif frozen_reuse and explicit_substantive and any(ref.get("exists") for ref in receipts):
                direct_read, category, reason = True, "first_design_reuse", "Previously frozen first text referenced by a worker; no additional first-design or supplier count."
            elif explicit_substantive and (explicit_true_read or successful_lines):
                direct_read, category, reason = True, "supplier_original", "Recorded source sections/finding and an explicit original-read flag or literally delivered original-body lines."
            else:
                direct_read, category, reason = UNKNOWN, "ambiguous_attempt", "Substantive direct-original reading cannot be established from recorded flags/sections and associated receipts."
            identity, normalization_notes = counting_identity(source_url)
            relative = self.relative(item["path"])
            row_id = "S-" + digest(f"{relative}:{item['line']}:{item['line_sha256']}")[:20]
            if identity is None:
                identity = "unresolved:" + row_id
                normalization_notes.append("No verified document URL; no inferred grouping with another source.")
            if category in {"first_design", "first_design_reuse"}:
                # A first draft's commit/path is retained; it is not grouped with later drafts.
                normalization_notes.append("First-design exact flags remain separate from supplier counts and reused input records.")
            memberships = []
            source_id = original.get("source_id", UNKNOWN)
            for citation in self.citations:
                matches = []
                if source_id != UNKNOWN and citation["source_id"] == source_id:
                    matches.append("sealed_citation_source_id")
                if citation["normalized_document_url"] in document_urls:
                    matches.append("normalized_document_url")
                if matches:
                    memberships.append({**citation, "association_basis": matches})
            route = linked.get("route", original.get("route", "initial" if origin == "initial" else origin))
            stage = first_present(original, ("stage",), linked.get("stage", "first_design_or_sampling" if origin == "initial" else "common_start" if origin == "C" else "route"))
            checked = first_present(original, ("checked_utc", "read_utc", "accessed_utc"))
            checked_basis = "Original source row"
            if checked == UNKNOWN and visits:
                checked = max(visit["ended_utc"] for visit in visits)
                checked_basis = "Associated saved operation end time; source row omitted an independent read time"
            row = {
                "schema": SCHEMA, "ledger_row_id": row_id, "source_id": source_id,
                "type": kind, "publisher": first_present(original, ("publisher", "author")),
                "authors": first_present(original, ("authors", "author")),
                "original_url": source_url, "original_url_basis": url_basis,
                "observed_original_urls": associated_urls,
                "normalized_document_urls": document_urls,
                "version": first_present(original, ("version", "version_date")),
                "date": first_present(original, ("date", "publication_date")),
                "checked_utc": checked, "checked_utc_basis": checked_basis,
                "actually_read_sections": sections,
                "finding": finding, "limitations": limitations,
                "linked_questions": questions or [UNKNOWN], "route": route, "stage": stage,
                "origin_ledger": origin, "category": category,
                "direct_read": direct_read, "classification_reason": reason,
                "receipt": [ref["path"] for ref in receipts if ref.get("path") != UNKNOWN] or [UNKNOWN],
                "receipt_provenance": receipts,
                "actual_returned_passages": [{"receipt": visit["receipt"], "documents": visit["returned_documents"], "line_ranges": visit["actual_returned_line_ranges"]} for visit in body_visits],
                "original_duplicate_group": original.get("duplicate_group", UNKNOWN),
                "duplicate_group": "D-" + digest(identity)[:20],
                "normalized_document_identity": identity,
                "normalization_note": normalization_notes or ["Only exact normalized document URLs are grouped; distinct document paths remain distinct."],
                "original_count_flags": {key: original[key] for key in COUNT_KEYS if key in original},
                "declared_count_eligibility": eligible,
                "declared_count_eligibility_fields": [{"field": key, "value": val} for key, val in eligibility_fields],
                "initial_aggregate_exact_counted_flag": original.get("counted", UNKNOWN) if origin == "initial" else None,
                "initial_design_count_eligible": exact_initial,
                "supplier_original_count_eligible": bool(category == "supplier_original" and direct_read is True and eligible is True),
                "returned_membership": memberships,
                "actually_returned_AB": any(member["route"] in {"A", "B"} for member in memberships),
                "actually_returned_C": any(member["route"] == "C" for member in memberships),
                "counted_initial_minimum": False,
                "counted_supplier_AB_minimum": False,
                "counted_supplier_C_sensitivity": False,
                "source_file": relative, "source_file_line": item["line"],
                "source_file_sha256": self.consumed_files[relative],
                "original_row_sha256": item["line_sha256"], "original_record": original,
            }
            missing = [key for key in ("source_id", "type", "publisher", "version", "date", "checked_utc", "actually_read_sections", "finding", "limitations", "original_url") if row[key] == UNKNOWN]
            row["missing_metadata"] = missing
            if missing:
                self.warn("missing_source_metadata", row_id=row_id, file=relative, line=item["line"], fields=missing, value=UNKNOWN)
            if any(ref.get("exists") is False for ref in receipts):
                self.warn("missing_or_nonlocal_source_receipt", row_id=row_id, file=relative)
            if direct_read is True:
                self.sources.append(row)
            else:
                self.attempts.append(row)
            for visit in visits:
                visit.setdefault("associated_source_rows", []).append(row_id)
                if (direct_read is True and category == "supplier_original" and visit in body_visits
                        and not visit["fetch_failed"] and visit["original_text_lines_returned"]):
                    visit["substantive_original_body_read"] = True
        for visit in self.visits:
            visit.setdefault("associated_source_rows", [])
            visit["metadata_or_unusable_body_response"] = bool(visit["body_open_debit"] and not visit["fetch_failed"] and not visit["substantive_original_body_read"])

    def apply_counting(self):
        all_rows = self.sources + self.attempts
        groups = collections.defaultdict(list)
        for row in all_rows:
            groups[row["duplicate_group"]].append(row)
        self.duplicate_groups = []
        self.initial_groups, self.ab_groups, self.c_groups = set(), set(), set()
        for group_id, members in sorted(groups.items()):
            initial = [row for row in members if row["initial_design_count_eligible"]]
            ab = [row for row in members if row["supplier_original_count_eligible"] and row["actually_returned_AB"]]
            common = [row for row in members if row["supplier_original_count_eligible"] and row["actually_returned_C"]]
            for candidates, field, collection in (
                (initial, "counted_initial_minimum", self.initial_groups),
                (ab, "counted_supplier_AB_minimum", self.ab_groups),
                (common, "counted_supplier_C_sensitivity", self.c_groups),
            ):
                if candidates:
                    representative = sorted(candidates, key=lambda row: (row["source_file"], row["source_file_line"]))[0]
                    representative[field] = True
                    collection.add(group_id)
            self.duplicate_groups.append({
                "duplicate_group": group_id,
                "normalized_document_identity": members[0]["normalized_document_identity"],
                "original_urls": sorted({url for row in members for url in row["observed_original_urls"]}),
                "original_duplicate_groups": sorted({str(row["original_duplicate_group"]) for row in members}),
                "source_ids": sorted({str(row["source_id"]) for row in members}),
                "row_ids": [row["ledger_row_id"] for row in members],
                "directly_read_original_rows": sum(row["direct_read"] is True for row in members),
                "attempt_rows": sum(row["direct_read"] is not True for row in members),
                "initial_minimum_count": int(bool(initial)),
                "supplier_AB_minimum_count": int(bool(ab)),
                "supplier_C_sensitivity_count": int(bool(common)),
                "AB_citation_witness_rows": [row["ledger_row_id"] for row in ab],
                "C_citation_witness_rows": [row["ledger_row_id"] for row in common],
                "normalization_notes": unique([note for row in members for note in row["normalization_note"]]),
            })
        for row in all_rows:
            row["count_eligibility"] = {
                "first_design_exact": row["initial_design_count_eligible"],
                "supplier_original": row["supplier_original_count_eligible"],
                "supplier_AB_returned": bool(row["supplier_original_count_eligible"] and row["actually_returned_AB"]),
                "reason": "No false/missing original flag is promoted. Supplier minimum additionally requires direct-original reading and sealed A/B source-ID or edition-preserving document-URL citation association. Each conservative document group counts once.",
            }
        self.citation_associations = []
        for citation in self.citations:
            matches = []
            for row in all_rows:
                basis = []
                if citation["source_id"] != UNKNOWN and citation["source_id"] == row["source_id"]:
                    basis.append("sealed_citation_source_id")
                if citation["normalized_document_url"] in row["normalized_document_urls"]:
                    basis.append("normalized_document_url")
                if basis:
                    matches.append({"row_id": row["ledger_row_id"], "source_id": row["source_id"], "source_file": row["source_file"], "ledger": "sources.jsonl" if row["direct_read"] is True else "attempts.jsonl", "direct_read": row["direct_read"], "basis": basis})
            self.citation_associations.append({**citation, "source_associations": matches})
            if not matches:
                self.warn("citation_without_source_row_association", return_file=citation["return_file"], candidate_rank=citation["candidate_rank"], citation_ordinal=citation["citation_ordinal"])

    def assemble_routes(self):
        for qid in QIDS:
            question = self.questions_by_id[qid]
            for route in ("C", "A", "B"):
                packet = self.packets.get((qid, route))
                if packet is None:
                    continue
                common = ROOT / "common" / qid
                directory = common if route == "C" else ROOT / "routes" / route / qid
                record = self.starts.get(qid, {}) if route == "C" else self.route_records.get((qid, route), {})
                visits = [visit for visit in self.visits if visit["question_id"] == qid and visit["route"] == route]
                navigation = sum(visit["navigation_debit"] for visit in visits)
                body = sum(visit["body_open_debit"] for visit in visits)
                find_extra = sum(visit["find_additional_navigation_sensitivity"] for visit in visits)
                doc_urls = unique([urldefrag(citation["url"])[0] for candidate in packet["candidates"] for citation in candidate["citations"]])
                caps = {"navigation": 1 if route == "C" else 2, "body_opens": 2 if route == "C" else 4, "candidates": 3, "document_urls": 3}
                actual = {
                    "navigation": navigation, "body_opens": body,
                    "web_operations": len(visits),
                    "web_searches": sum(visit["operation_type"] in SEARCH_COMMANDS for visit in visits),
                    "dual_debit_operations": sum(visit["dual_debit"] for visit in visits),
                    "within_page_find_operations": sum(visit["within_page_find"] for visit in visits),
                    "fetch_failure_operations": sum(visit["fetch_failed"] for visit in visits),
                    "failed_body_open_attempts": sum(bool(visit["body_open_debit"] and visit["fetch_failed"]) for visit in visits),
                    "substantive_original_body_responses": sum(visit["substantive_original_body_read"] for visit in visits),
                    "metadata_or_unusable_body_responses": sum(visit["metadata_or_unusable_body_response"] for visit in visits),
                    "repeated_exact_requests": sum(visit["repeated_exact_request"] for visit in visits),
                    "candidate_count": len(packet["candidates"]), "document_url_count": len(doc_urls),
                    "tool_elapsed_ms_sum": sum(visit["elapsed_ms"] for visit in visits if isinstance(visit["elapsed_ms"], (int, float))),
                    "elapsed_operation_count_measured": sum(isinstance(visit["elapsed_ms"], (int, float)) for visit in visits),
                    "server_transfer_bytes": UNMEASURED, "server_token_cost": UNMEASURED,
                    "local_response_canonical_json_utf8_bytes_sum": sum(visit["local_response_canonical_json_utf8_bytes"] for visit in visits),
                }
                declared = packet.get("budget", {})
                matches = declared.get("navigation") == navigation and declared.get("body_opens") == body
                compliance = navigation <= caps["navigation"] and body <= caps["body_opens"] and len(packet["candidates"]) <= 3 and len(doc_urls) <= 3
                declared_navigation = declared.get("navigation")
                sensitivity_base = declared_navigation if type(declared_navigation) is int else navigation
                sensitivity = {
                    "nav_if_find_is_navigation": sensitivity_base + find_extra,
                    "declared_return_navigation": declared_navigation if declared_navigation is not None else UNKNOWN,
                    "receipt_navigation_debits": navigation,
                    "receipt_nav_if_find_is_navigation": navigation + find_extra,
                    "additional_zero_navigation_find_operations": find_extra,
                    "navigation_cap": caps["navigation"],
                    "exceeds_navigation_cap": sensitivity_base + find_extra > caps["navigation"],
                    "A_B_exceeds_two_navigation_operations": route in {"A", "B"} and sensitivity_base + find_extra > 2,
                    "original_debits_and_return_unchanged": True,
                    "basis": "Alternative cost interpretation: each within-page find with navigation_debit=0 adds one navigation operation; original body and navigation debits remain intact.",
                }
                inputs = {
                    "questions": {**self.file_reference(ROOT / "questions.jsonl"), "question_id": qid},
                    "common_start": self.file_reference(common / "start.json"),
                    "initial_text": self.file_reference(self.local_path(question["initial_text_file"])),
                    "route_order_frozen": question.get("route_order", UNKNOWN),
                }
                if route != "C":
                    input_path = ROOT / "route-inputs" / route / f"{qid}.json"
                    inputs["route_input"] = self.file_reference(input_path)
                    if input_path.exists():
                        frozen = self.read_json(input_path)
                        inputs["input_commit"] = frozen.get("input_commit", UNKNOWN)
                        inputs["isolation"] = frozen.get("isolation", UNKNOWN)
                        if "literal_queries" in frozen:
                            inputs["literal_queries"] = frozen["literal_queries"]
                selection_paths = sorted(directory.glob("selection-*.json"))
                if (directory / "decision.json").exists():
                    selection_paths.insert(0, directory / "decision.json")
                original_path = directory / ("start.json" if route == "C" else "route.json")
                return_path = directory / ("baseline-return.json" if route == "C" else "return.json")
                row = {
                    "schema": SCHEMA, "observation_id": f"{qid}-{route}",
                    "question_id": qid, "independent_event_id": qid, "route": route,
                    "ledger": question.get("ledger", UNKNOWN), "scope": question.get("scope", question.get("whole_or_partial", UNKNOWN)),
                    "period": question.get("period", UNKNOWN), "input_provenance": inputs,
                    "selection_provenance": [self.file_reference(path) for path in selection_paths],
                    "raw_receipts": [{"visit_id": visit["visit_id"], "path": visit["receipt"], "sha256": visit["receipt_sha256"]} for visit in visits],
                    "common_reuse_recorded": record.get("common_reuse", packet.get("budget", {}).get("common_body_reuse", [])),
                    "common_reuse_is_additional_web_operation": False,
                    "actual_counters": actual, "declared_return_budget": declared,
                    "declared_budget_matches_receipts": matches, "caps": caps,
                    "actual_caps_met": compliance, "cost_sensitivity": sensitivity,
                    "started_utc": record.get("started_utc", packet.get("started_utc", record.get("elapsed", {}).get("started_utc", min([v["started_utc"] for v in visits], default=UNKNOWN)))),
                    "ended_utc": record.get("ended_utc", packet.get("ended_utc", record.get("elapsed", {}).get("ended_utc", max([v["ended_utc"] for v in visits], default=UNKNOWN)))),
                    "recorded_elapsed_ms": record.get("elapsed_ms", UNKNOWN),
                    "original_route_record": record,
                    "route_file": self.file_reference(original_path),
                    "return_file": self.file_reference(return_path),
                    "returned_document_urls_in_original_order": doc_urls,
                    "unused_candidate_slots": 3 - len(packet["candidates"]),
                    "unused_document_url_slots": 3 - len(doc_urls),
                    "semantic_success_assigned": False,
                }
                self.routes.append(row)
                if not matches:
                    self.warn("declared_budget_differs_from_receipts", observation_id=row["observation_id"], declared={key: declared.get(key, UNKNOWN) for key in ("navigation", "body_opens")}, actual={"navigation": navigation, "body_opens": body})
                if not compliance:
                    self.warn("actual_route_cap_exceeded", observation_id=row["observation_id"])

    def report(self):
        all_rows = self.sources + self.attempts
        category_counts = dict(sorted(collections.Counter(row["category"] for row in all_rows).items()))
        missing_counts = collections.Counter(field for row in all_rows for field in row["missing_metadata"])
        actual_caps = [{
            "question_id": row["question_id"], "route": row["route"],
            "actual_counters": row["actual_counters"], "caps": row["caps"],
            "actual_caps_met": row["actual_caps_met"],
            "declared_budget_matches_receipts": row["declared_budget_matches_receipts"],
            "cost_sensitivity": row["cost_sensitivity"],
        } for row in self.routes]
        unsealed = [path for path in self.consumed_files if path not in self.sealed_paths and path not in {"evidence/input-seal.json", "evidence/common-seal.json", "evidence/route-seal.json", "assemble_observations.py"}]
        if unsealed:
            self.warn("consumed_files_outside_three_seal_maps", files=sorted(unsealed), note="All originals are hashed in this report; absence from a seal is not represented as sealed provenance.")
        route_seal = self.seals.get("route-seal.json", {})
        return {
            "schema": SCHEMA,
            "assembly_basis_utc": route_seal.get("created_utc", UNKNOWN),
            "timestamp_basis": "Frozen route seal creation time; this deterministic assembler does not invent a wall-clock execution time.",
            "mode": "read_only_incomplete_schema_check" if self.allow_incomplete else "sealed_observation_assembly",
            "semantic_success_assigned": False,
            "no_return_reranking_or_clipping": True,
            "row_counts": {"sources": len(self.sources), "attempts": len(self.attempts), "all_input_source_provenance_rows": len(all_rows), "routes": len(self.routes), "visits": len(self.visits), "returns": len(self.returns)},
            "denominators": {
                "independent_design_events": len(self.questions),
                "expected_independent_design_events": 12,
                "route_observations": len(self.returns), "expected_route_observations": 36,
                "common_C_observations": sum(row["route"] == "C" for row in self.returns),
                "A_B_observations": sum(row["route"] in {"A", "B"} for row in self.returns),
                "observations_are_independent_events": False,
            },
            "actual_route_caps_and_URL_caps": actual_caps,
            "cost_sensitivity": {
                "rule": "Add each zero-navigation within-page find to navigation, without changing original debits or returns.",
                "A_B_routes_exceeding_two": [row["observation_id"] for row in self.routes if row["cost_sensitivity"]["A_B_exceeds_two_navigation_operations"]],
                "A_B_routes_within_alternative_cap": [row["observation_id"] for row in self.routes if row["route"] in {"A", "B"} and not row["cost_sensitivity"]["A_B_exceeds_two_navigation_operations"]],
                "no_semantic_recalculation": True,
            },
            "source_totals": {
                "categories": category_counts,
                "input_exact_initial_true_flags": sum(row["initial_aggregate_exact_counted_flag"] is True for row in all_rows),
                "input_exact_initial_false_flags": sum(row["initial_aggregate_exact_counted_flag"] is False for row in all_rows),
                "all_conservative_document_groups": len(self.duplicate_groups),
                "first_design_groups": len(self.initial_groups),
                "returned_supplier_AB_groups": len(self.ab_groups),
                "returned_supplier_C_groups_sensitivity": len(self.c_groups),
                "C_only_supplier_groups_sensitivity": len(self.c_groups - self.ab_groups),
                "AB_or_C_supplier_groups_sensitivity": len(self.ab_groups | self.c_groups),
                "primary_first_plus_AB_supplier_groups": len(self.initial_groups | self.ab_groups),
                "post_seal_supplementary_or_cross_field_sources_included": False,
                "strict_primary_counting_rule": "Only an explicitly eligible directly read supplier row with actual sealed A/B source-ID or normalized document-URL citation membership qualifies; duplicate-document groups count once. False/missing flags, snippets, metadata, failures, locators, and recovery rows are never promoted. C is reported separately.",
            },
            "category_minima": {
                "first_designs": {"required": 12, "observed": len(self.initial_groups), "met": len(self.initial_groups) >= 12},
                "returned_supplier_originals_AB": {"required": 12, "observed": len(self.ab_groups), "met": len(self.ab_groups) >= 12},
                "cross_field_originals": {"required": 4, "observed_in_this_assembly": 0, "met_in_this_assembly": False, "scope": "Post-seal challenges are assembled/audited separately and cannot improve route returns."},
                "combined_required": 28,
                "combined_observed_in_this_assembly": len(self.initial_groups | self.ab_groups),
            },
            "duplicate_groups": self.duplicate_groups,
            "source_URL_associations": self.citation_associations,
            "missing_metadata_counts": dict(sorted(missing_counts.items())),
            "warnings": self.warnings,
            "input_files_sha256": dict(sorted(self.consumed_files.items())),
            "seal_files": {name: {"created_utc": record.get("created_utc", UNKNOWN), "files_verified": len(record["files"]), "sha256": self.consumed_files[f"evidence/{name}"]} for name, record in sorted(self.seals.items())},
            "limits": [
                "Provenance and counters only; no predicate, novelty, supplier-functionality, runtime, or semantic-success verdict.",
                "All original source records are preserved in exactly one of sources.jsonl or attempts.jsonl; originals in per-stream/common/route files remain unchanged.",
                "Missing metadata is 미확인. Transfer bytes and server token usage are 미계측; local UTF-8 byte sizes are separate.",
                "Reported source Total lines is never used as actually read evidence; only delivered numbered lines are recorded.",
                "Conservative document-family grouping does not authorize combining versions into a supported component.",
                "Membership is citation association, not evidence sufficiency. Edition collapsing is for counts only, not URL-membership or protocol URL caps.",
                "Cache/common-body reuse contributes no new web-operation row; retries and failures with actual receipts remain operations.",
            ],
        }

    def run(self):
        self.load_inputs()
        self.scan_visits()
        self.normalize_sources()
        self.apply_counting()
        self.assemble_routes()
        self.read_bytes(Path(__file__))
        if not self.allow_incomplete and (len(self.routes) != 36 or len(self.returns) != 36):
            raise ValueError("Full assembly requires exactly 12 C plus 24 A/B observations")
        return self.report()


def serialize_jsonl(records):
    # Original nested candidate/citation order and packet key insertion order stay intact.
    return "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records).encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-incomplete", action="store_true", help="Read-only available-schema check; never writes any global ledger.")
    parser.add_argument("--check-only", action="store_true", help="Require complete seals and validate in memory without writing.")
    parser.add_argument("--replace-generated", action="store_true", help="Explicitly replace differing assembler-generated outputs; original inputs are never changed.")
    args = parser.parse_args()
    if args.allow_incomplete and args.replace_generated:
        parser.error("--allow-incomplete cannot be used with --replace-generated")
    assembly = Assembly(allow_incomplete=args.allow_incomplete)
    try:
        report = assembly.run()
        outputs = {
            ROOT / "sources.jsonl": serialize_jsonl(assembly.sources),
            ROOT / "attempts.jsonl": serialize_jsonl(assembly.attempts),
            ROOT / "routes.jsonl": serialize_jsonl(assembly.routes),
            ROOT / "visits.jsonl": serialize_jsonl(assembly.visits),
            ROOT / "returns.jsonl": serialize_jsonl(assembly.returns),
        }
        report["output_artifacts"] = {str(path.relative_to(ROOT)): {"sha256": digest(data), "local_utf8_bytes": len(data)} for path, data in outputs.items()}
        outputs[ROOT / "evidence" / "observation-assembly.json"] = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        if not args.allow_incomplete and not args.check_only:
            # Check all destinations and consumed bytes before making the first write.
            for relative, expected in assembly.consumed_files.items():
                path = ROOT / relative
                if not path.exists() or digest(path.read_bytes()) != expected:
                    raise ValueError(f"Input changed before output write: {relative}")
            for path, data in outputs.items():
                if path.exists() and path.read_bytes() != data and not args.replace_generated:
                    raise ValueError(f"Differing generated output exists: {path.relative_to(ROOT)}; inspect before explicit --replace-generated")
            for path, data in outputs.items():
                if not path.exists() or path.read_bytes() != data:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(data)
        print(json.dumps({
            "schema": SCHEMA,
            "mode": report["mode"],
            "wrote_global_ledgers": not args.allow_incomplete and not args.check_only,
            "row_counts": report["row_counts"],
            "independent_events": report["denominators"]["independent_design_events"],
            "warnings": len(report["warnings"]),
            "semantic_success_assigned": False,
        }, ensure_ascii=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error), "wrote_global_ledgers": False}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
