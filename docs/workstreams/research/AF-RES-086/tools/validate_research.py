#!/usr/bin/env python3
"""Offline structural audit of AF-RES-086; no network and no Git mutations.

Run from any directory with Python 3.10+:
  python -B docs/workstreams/research/AF-RES-086/tools/validate_research.py \
    --output docs/workstreams/research/AF-RES-086/evidence/local-validation.json

Exit 0 means the checks that could run passed. Missing final documents are
explicitly PENDING unless --require-final-docs is used. Exit 1 means a structural
failure. The historical research verdict remains a separate PARTIAL field.
Full responses deliberately not retained cannot be rehashed by this program;
their receipts and retained extracts are checked without claiming otherwise.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from collections import Counter, defaultdict


OWNED = "docs/workstreams/research/AF-RES-086/"
BASE = "9dcae48a47b05d7ba2a1320444be28f5d0fcd739"
PLAN = "184137d2f257f5d1a7ef584e0f3a6b35f3d280cd"
DEPENDENCY = "1f8bf039ad4f9a38b99764a11f72b515facef39c"
PRIOR = "586b33488f6338ee8309a671d270656d837df636"
STREAMS = ("python", "r", "incidents", "preservation")
POLICY_LINEAGES = {
    "service-rtd-platform", "github-pages-official-contract",
    "PR-L-SWH-POLICY", "PR-L-ZENODO-POLICY",
}
WINDOWS = {
    "P3": ["2025-11-11T00:00:00Z", "2025-11-14T00:00:00Z"],
    "R1": ["2025-03-24T00:00:00Z", "2025-03-27T00:00:00Z"],
    "P1": ["2025-12-16T17:51:34.578405Z", "2025-12-19T17:51:34.578405Z"],
    "R2": ["2024-01-21T20:53:46Z", "2024-01-24T20:53:46Z"],
}
SOURCES = {
    "P3": "63fd63b352a9a8bdcc24791c9dbee952ee9a8abc",
    "R1": "a4c6ec37fc8737a189ca7ec7095ec0161888f9e8",
    "P1": "7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74",
    "R2": "f992b26f3cb30c799fbb95f6148852d8ae8a7f18",
}
SLOTS = {
    "P3-STABLE": ("P3", "https://cibuildwheel.pypa.io/en/stable/options/#enable", "PY-P3-STABLE-NOW"),
    "P3-LEGACY": ("P3", "https://cibuildwheel.pypa.io/en/1.x/", "PY-P3-LEGACY-NOW"),
    "P3-TAG": ("P3", "https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable", "PY-P3-TAG-NOW"),
    "P1-LATEST": ("P1", "https://bandersnatch.readthedocs.io/en/latest/", "PY-P1-LATEST-NOW"),
    "P1-NAMED": ("P1", "https://bandersnatch.readthedocs.io/en/7.0.1/", "PY-P1-NAMED-NOW"),
    "R1-ROOT": ("R1", "https://archive.r-lib.org/", "R1-CURRENT-ROOT"),
    "R1-LEAF": ("R1", "https://archive.r-lib.org/reference/archive_read.html", "R1-CURRENT-LEAF"),
    "R2-ROOT": ("R2", "https://asciicast.r-lib.org/", "R2-CURRENT-ROOT"),
    "R2-LEAF": ("R2", "https://asciicast.r-lib.org/articles/asciicast-demo.html", "R2-CURRENT-LEAF"),
}
TABLE_HEADERS = [
    ["사례·원 독자", "원 약속과 주소", "필요한 판·관측창", "당시 소스·생성물", "주장 근거 URL", "빠진 약속"],
    ["사례·경로", "source SHA", "build·artifact", "deployment·최종 상태", "응답 UTC·최종 URL·파일/절 지문", "같은 시점의 두 조건", "미확인"],
    ["독자 목적", "현재 정보로 선택한 링크", "역사 근거를 더한 선택", "바뀐 근거·반례", "추가 확인 비용", "보류 조건"],
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def read_json(path: Path):
    return json.loads(path.read_text())


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def utc(value: str) -> dt.datetime:
    result = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None or result.utcoffset() != dt.timedelta():
        raise ValueError(f"Not an explicit UTC timestamp: {value}")
    return result


def truth(value) -> bool:
    return value is True or (isinstance(value, str) and value.lower() == "true")


def refs(value) -> list[str]:
    if not value:
        return []
    return value if isinstance(value, list) else value.split(";")


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text.replace("`", "").replace("**", "")).strip()


class Audit:
    def __init__(self, root: Path):
        self.root = root
        self.repo = root.parents[3]
        self.checks = []
        self.issues = []
        self.snapshots = {}

    def require(self, condition, message: str):
        if not condition:
            self.issues.append(message)

    def run(self, name: str, function):
        self.issues = []
        try:
            details = function() or {}
        except Exception as error:
            self.issues.append(f"{type(error).__name__}: {error}")
            details = {}
        self.checks.append({
            "check": name, "status": "FAIL" if self.issues else "PASS",
            "issues": list(self.issues), "details": details,
        })

    def pending(self, name: str, explanation: str, fail: bool):
        self.checks.append({
            "check": name, "status": "FAIL" if fail else "PENDING",
            "issues": [explanation] if fail else [], "details": {"reason": explanation},
        })

    def git(self, *args: str) -> bytes:
        environment = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
        result = subprocess.run(
            ["git", *args], cwd=self.repo, env=environment,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        if result.returncode:
            raise ValueError(f"read-only git {' '.join(args)} exited {result.returncode}: {result.stderr.decode().strip()}")
        return result.stdout

    def owned_path(self, path: str, relative: Path | None = None) -> Path:
        resolved = ((relative or self.root) / path).resolve()
        if not resolved.is_relative_to(self.root):
            raise ValueError(f"Evidence path escapes owned_path: {path}")
        return resolved

    def remember(self, path: Path):
        self.snapshots[str(path.relative_to(self.root))] = digest(path.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON file inside this task's owned_path; JSON is also printed.")
    parser.add_argument("--require-final-docs", action="store_true", help="Treat missing RESULT/cards/SELF_CHECK as structural failures.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    audit = Audit(root)
    sources = jsonl(root / "sources.jsonl")
    claims = read_csv(root / "claims.csv")
    routes = jsonl(root / "routes.jsonl")
    incidents = read_csv(root / "incidents.csv")
    manifest = read_json(root / "manifest.json")
    by_id = {row["id"]: row for row in sources}
    claim_ids = {row["claim_id"] for row in claims}
    receipt_data = {row["id"]: read_json(audit.owned_path(row["receipt_path"])) for row in sources}
    source_audit = read_json(root / "evidence/source-audit.json")
    denominators = read_json(root / "evidence/route-denominators.json")
    costs = read_json(root / "costs.json")
    pairs = read_json(root / "streams/preservation/pairs.json")
    core_paths = ["manifest.json", "sources.jsonl", "claims.csv", "routes.jsonl", "incidents.csv", "costs.json", "evidence/source-audit.json", "evidence/route-denominators.json", "streams/preservation/pairs.json"]
    for path in core_paths:
        audit.remember(root / path)

    def references():
        for label, rows, field in [("sources", sources, "id"), ("claims", claims, "claim_id"), ("routes", routes, "route_id"), ("incidents", incidents, "incident_id")]:
            values = [r[field] for r in rows]
            audit.require(all(values) and len(values) == len(set(values)), f"{label}: empty or duplicate IDs")
        path_count = 0
        for row in sources:
            sid = row["id"]
            for key in ("lineage_id", "kind", "url", "read_utc", "observed", "observer", "limitations", "support_refute", "version", "section"):
                audit.require(bool(row.get(key)), f"{sid}: missing {key}")
            utc(row["read_utc"])
            audit.require(bool(row.get("Q")), f"{sid}: missing question linkage")
            audit.require(set(row.get("Q", [])).issubset({f"Q{i}" for i in range(1, 8)}), f"{sid}: unexpected Q labels")
            for claim in row.get("claim_ids", []):
                audit.require(claim in claim_ids, f"{sid}: unresolved claim {claim}")
            for key in ("receipt_path", "extract_path", "excerpt_path"):
                if row.get(key):
                    path_count += 1
                    audit.require(audit.owned_path(row[key]).is_file(), f"{sid}: missing {key} {row[key]}")
        external = []
        for row in claims:
            for sid in refs(row["source_ids"]):
                if sid == "brief":
                    external.append({"claim": row["claim_id"], "reference": sid, "role": "user instruction; not counted source"})
                else:
                    audit.require(sid in by_id, f"Claim {row['claim_id']}: unresolved source {sid}")
        for row in routes + incidents:
            for sid in refs(row.get("source_ids", row.get("source_id"))):
                audit.require(sid in by_id, f"Route/incident: unresolved source {sid}")
        for stream in STREAMS:
            local = jsonl(root / "streams" / stream / "sources.jsonl")
            local_ids = {r.get("id", r.get("source_id")) for r in local}
            central_ids = {r["id"] for r in sources if r["stream"] == stream}
            audit.require(local_ids == central_ids, f"{stream}: central IDs differ from stream ledger")
            for old in local:
                sid = old.get("id", old.get("source_id"))
                current = by_id[sid]
                for key in ("lineage_id", "url", "read_utc", "receipt_path", "observed", "limitations"):
                    audit.require(old.get(key) == current.get(key), f"{stream}/{sid}: changed central {key}")
        audit.require((root / "incidents.csv").read_bytes() == (root / "streams/incidents/incidents.csv").read_bytes(), "Central incident ledger differs from stream")
        return {"sources": len(sources), "claims": len(claims), "routes": len(routes), "incidents": len(incidents), "source_local_path_references": path_count, "external_instruction_references": external}

    audit.run("unique_ids_references_and_owned_paths", references)

    def quantities():
        eligible = [r for r in sources if r["countable_original"]]
        lineages = {r["lineage_id"] for r in eligible}
        groups = defaultdict(list)
        for row in eligible:
            audit.require(row.get("direct_read") is True, f"{row['id']}: countable but not direct_read")
            groups[row.get("direct_sha256") or row.get("snapshot_sha256") or ("unknown:" + row["id"])].append(row["id"])
        duplicates = sorted(sorted(ids) for ids in groups.values() if len(ids) > 1)
        calculated = {
            "source_rows": len(sources), "eligible_original_rows": len(eligible),
            "minimum_originals_after_equal_payload_dedup": len(groups),
            "conservative_lineage_count": len(lineages),
            "non_policy_lineages": len(lineages - POLICY_LINEAGES),
            "unique_eligible_url_version_pairs": len({(r["url"], r["version"]) for r in eligible}),
        }
        expected = {"source_rows": 201, "eligible_original_rows": 126, "minimum_originals_after_equal_payload_dedup": 123, "conservative_lineage_count": 25, "non_policy_lineages": 21, "unique_eligible_url_version_pairs": 126}
        for key, value in expected.items():
            audit.require(calculated[key] == value, f"{key}: calculated {calculated[key]} != frozen expected {value}")
            if key in source_audit:
                audit.require(source_audit[key] == calculated[key], f"source-audit.json disagrees on {key}")
        audit.require(set(source_audit["lineages"]) == lineages, "Declared lineage set differs from eligible records")
        audit.require(duplicates == sorted(sorted(g) for g in source_audit["equal_payload_groups_excluded_from_extra_minimum_count"]), "Equal-payload groups differ")
        audit.require(POLICY_LINEAGES.issubset(lineages), "Expected policy lineages absent")
        calculated["equal_payload_groups"] = duplicates
        calculated["policy_lineages_excluded_from_21"] = sorted(POLICY_LINEAGES)
        calculated["quantity_gate_pass"] = len(groups) >= 24 and len(lineages) >= 20
        return calculated

    audit.run("independent_source_and_lineage_counts", quantities)

    def fixed_scope():
        research = manifest["research"]
        audit.require(manifest["base_commit"] == BASE, "Actual start SHA differs")
        audit.require(research["plan_commit"] == PLAN, "Planning SHA differs")
        audit.require(manifest["allowed_paths"] == [OWNED], "Manifest write scope differs")
        audit.require(manifest["dependencies"] == [{"branch": "work/research-af-res-082", "commit": DEPENDENCY}], "Dependency pin differs")
        audit.require(set(research["cases"]) == set(WINDOWS), "Fixed four cases differ")
        audit.require(research["main_windows"] == WINDOWS, "Frozen UTC windows differ")
        for case, (start, end) in WINDOWS.items():
            audit.require(utc(end) - utc(start) == dt.timedelta(days=3), f"{case}: window is not exactly 72 hours")
        audit.require(research["route_denominator"] == 9, "Manifest route denominator != 9")
        audit.require(research["original_two_condition_denominator"] == 6 and research["original_two_condition_confirmed"] == 1, "Original promise denominator altered")
        for relative, expected_hash in manifest["contract"]["files"].items():
            path = audit.repo / relative
            audit.require(digest(path.read_bytes()) == expected_hash, f"Pinned contract file changed: {relative}")
        slot_rows = denominators["slots"]
        audit.require(len(slot_rows) == 9 and {r["slot_id"] for r in slot_rows} == set(SLOTS), "Nine slot identities differ")
        for row in slot_rows:
            expected = SLOTS[row["slot_id"]]
            audit.require((row["case_id"], row["url"], row["current_source_id"]) == expected, f"{row['slot_id']}: fixed URL or source changed")
            receipt = receipt_data[row["current_source_id"]]
            status = receipt.get("status", receipt.get("http_status"))
            audit.require(row["current_http_status"] == status, f"{row['slot_id']}: status disagrees with receipt")
        for case, expected_source in SOURCES.items():
            audit.require(any(r.get("case_id") == case and r.get("source_sha") == expected_source for r in routes), f"{case}: fixed source SHA not linked in routes")
        for run, case in [(30298914, "P3"), (30298916, "P3"), (30720077, "P1")]:
            found = [r for r in routes if r.get("run_id") == run]
            audit.require(len(found) == 1 and found[0]["source_sha"] == SOURCES[case], f"Selected build {run} missing or source mismatch")
        for deployment, case, generated in [(2328795124, "R1", "45e0d9ebc168cf3632bc2d737c9db2318668a826"), (1283145596, "R2", "92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1")]:
            found = [r for r in routes if str(r.get("deployment_id")) == str(deployment) and r.get("stage") == "deployment_current_retained_status"]
            audit.require(len(found) == 1 and found[0].get("deployment_input_sha") == generated, f"Selected {case} deployment input mismatch")
        for row in routes:
            case = row.get("case_id")
            if case not in WINDOWS:
                continue
            start, end = map(utc, WINDOWS[case])
            if row.get("window_start_utc"):
                audit.require(utc(row["window_start_utc"]) == start and utc(row["window_end_utc_exclusive"]) == end, f"{row['route_id']}: route window differs")
            label = row.get("window", "")
            # P1's preregistered control window starts at build *completion*,
            # so a build created before that instant is not out of scope.
            # Reader responses still use their capture time, never a build time.
            instant = row.get("captured_at_utc") or row.get("capture_utc")
            if instant is None:
                instant = row.get("summary_finished_utc") if row.get("stage") == "build" else row.get("created_utc")
            if instant and label == "main":
                audit.require(start <= utc(instant) < end, f"{row['route_id']}: main observation outside main window")
            if instant and "supplement" in label:
                observed = utc(instant)
                audit.require(start - dt.timedelta(days=30) <= observed < end + dt.timedelta(days=30), f"{row['route_id']}: supplement exceeds 30 days")
                audit.require(not start <= observed < end, f"{row['route_id']}: main observation labelled supplemental")
        return {"cases": sorted(WINDOWS), "windows": WINDOWS, "slots": 9, "current_200": sum(r["current_http_status"] == 200 for r in slot_rows), "contract_files_rehashed": len(manifest["contract"]["files"]), "build_window_time_basis": "summary_finished_utc, matching preregistered P1 completion boundary; captured reader responses use capture UTC"}

    audit.run("manifest_fixed_cases_routes_and_utc_windows", fixed_scope)

    def receipts_and_hashes():
        metrics = Counter()
        not_retained = []
        for row in sources:
            sid, stream = row["id"], row["stream"]
            receipt_path = audit.owned_path(row["receipt_path"])
            receipt = receipt_data[sid]
            metrics["receipt_records_read"] += 1
            request_url = receipt.get("url", receipt.get("request_url"))
            audit.require(request_url == row["url"], f"{sid}: receipt request URL mismatch")
            if stream == "incidents" and row.get("transport") == "github_connector":
                data = receipt_path.read_bytes()
                audit.require(digest(data) == row["snapshot_sha256"] and len(data) == row["snapshot_bytes"], f"{sid}: committed connector snapshot bytes/hash mismatch")
                metrics["connector_snapshot_files_rehashed"] += 1
                continue
            received_hash = receipt.get("response_sha256", receipt.get("direct_sha256", receipt.get("sha256")))
            received_bytes = receipt.get("bytes", receipt.get("response_bytes", receipt.get("bytes_downloaded")))
            source_hash = row.get("transport_sha256") or row.get("direct_sha256") or row.get("snapshot_sha256")
            source_bytes = row.get("transport_body_bytes")
            if source_bytes is None and stream == "incidents":
                source_bytes = row.get("snapshot_bytes")
            audit.require(source_hash == received_hash, f"{sid}: source/receipt transport hash mismatch")
            audit.require(source_bytes == received_bytes, f"{sid}: source/receipt byte count mismatch")
            audit.require(isinstance(received_bytes, int) and received_bytes >= 0, f"{sid}: invalid byte count")
            audit.require(isinstance(received_hash, str) and bool(re.fullmatch(r"[0-9a-f]{64}", received_hash)), f"{sid}: invalid SHA-256")
            metrics["transport_receipt_metadata_checked"] += 1
            body = None
            if stream == "python" and receipt.get("body_file"):
                body = audit.owned_path(receipt["body_file"], receipt_path.parent)
            elif stream == "r":
                body = root / "streams/r/.workbench" / (sid + ".body")
            elif stream == "preservation" and receipt.get("body_path"):
                body = audit.owned_path(receipt["body_path"], root / "streams/preservation")
            if body is not None and body.is_file():
                data = body.read_bytes()
                audit.require(digest(data) == received_hash and len(data) == received_bytes, f"{sid}: retained raw body hash/length mismatch")
                metrics["retained_raw_bodies_rehashed"] += 1
                metrics["retained_raw_body_bytes_rehashed"] += len(data)
                if receipt.get("decoded_sha256"):
                    decoded = gzip.decompress(data)
                    audit.require(digest(decoded) == receipt["decoded_sha256"] and len(decoded) == receipt["decoded_bytes"], f"{sid}: decoded gzip hash/length mismatch")
                    if row.get("transport_sha256"):
                        audit.require(row["direct_sha256"] == receipt["decoded_sha256"], f"{sid}: decoded source fingerprint mismatch")
                    metrics["gzip_payloads_decoded_and_rehashed"] += 1
            else:
                not_retained.append(sid)
            if receipt.get("extract_path") and receipt.get("extract_sha256"):
                excerpt = audit.owned_path(receipt["extract_path"], root / "streams" / stream)
                audit.require(digest(excerpt.read_bytes()) == receipt["extract_sha256"], f"{sid}: retained extract hash mismatch")
                metrics["retained_extracts_rehashed"] += 1
        metrics = dict(metrics)
        metrics["full_body_not_retained_or_absent"] = not_retained
        metrics["body_absence_meaning"] = "Receipt consistency and retained extract verification only; not a new full-response checksum verification. Local .workbench caches are optional and are never fetched by this validator."
        return metrics

    audit.run("four_stream_receipts_bytes_and_available_hashes", receipts_and_hashes)

    def selected_identity_bindings():
        checked_builds = []
        unavailable_builds = []
        for row in routes:
            if row.get("stage") != "build" or row.get("run_id") not in {30298914, 30298916, 30298915, 30720077}:
                continue
            sid = row["source_ids"][0]
            receipt = receipt_data[sid]
            receipt_path = audit.owned_path(by_id[sid]["receipt_path"])
            body = audit.owned_path(receipt["body_file"], receipt_path.parent)
            if not body.is_file():
                unavailable_builds.append(row["run_id"])
                continue
            record = read_json(body)
            if isinstance(record, dict) and "results" in record:
                exact = [item for item in record["results"] if item.get("id") == row["run_id"]]
                audit.require(len(exact) == 1, f"Build{row['run_id']}: exact run absent/duplicated in source query")
                if not exact:
                    continue
                record = exact[0]
            audit.require((record["id"], record["commit"], record["version"], record["success"]) == (row["run_id"], row["source_sha"], row["version"], row["provider_build_success"]), f"Build{row['run_id']}: actual JSON ID/source/version/success differs from route")
            audit.require(record["created"] == row["created_utc"] and record["finished"] == row["summary_finished_utc"], f"Build{row['run_id']}: metadata UTC differs")
            checked_builds.append(row["run_id"])
        file_matches = []
        unavailable_files = []
        for row in routes:
            if row.get("stage") != "generated_file_vs_current_reader_response":
                continue
            generated_sid = next(sid for sid in row["source_ids"] if "-GENERATED-" in sid and not sid.endswith("-COMMIT"))
            current_sid = next(sid for sid in row["source_ids"] if "-CURRENT-" in sid)
            generated_file = root / "streams/r/.workbench" / (generated_sid + ".body")
            current_file = root / "streams/r/.workbench" / (current_sid + ".body")
            if not generated_file.is_file() or not current_file.is_file():
                unavailable_files.append(row["route_id"])
                continue
            generated, current = generated_file.read_bytes(), current_file.read_bytes()
            blob = hashlib.sha1(b"blob " + str(len(generated)).encode() + b"\0" + generated).hexdigest()
            audit.require(blob == row["publisher_hash"] == row["direct_git_blob_sha1"] == row["artifact_id"], f"{row['route_id']}: Git blob binding differs")
            audit.require(digest(generated) == row["direct_generated_sha256"] and digest(current) == row["current_sha256"], f"{row['route_id']}: generated/current SHA-256 differs")
            audit.require((generated == current) is row["current_matches_generated_bytes"], f"{row['route_id']}: byte-equality claim differs")
            file_matches.append({"route_id": row["route_id"], "git_blob": blob, "current_bytes_equal_generated": generated == current})
        retained_statuses = []
        for case, deployment, status_id, stamp in [("R1", 2328795124, 6150834411, "2025-03-24T12:38:03Z"), ("R2", 1283145596, 3093912083, "2024-01-21T20:58:36Z")]:
            original = read_json(root / "streams/r/evidence" / (case + "-DEPLOYMENT-STATUSES.original.json"))
            audit.require(len(original) == 1, f"{case}: retained original status sequence changed")
            if original:
                status = original[0]
                audit.require((status["id"], status["state"], status["created_at"], status["environment_url"]) == (status_id, "inactive", stamp, ""), f"{case}: actual retained status fields differ")
                audit.require(f"/deployments/{deployment}/statuses/" in status["url"], f"{case}: status/deployment ID mismatch")
                retained_statuses.append({"case": case, "deployment_id": deployment, "status_id": status_id, "state": status["state"], "utc": stamp, "environment_url": status["environment_url"]})
        return {"raw_build_json_bindings_checked": checked_builds, "raw_build_json_absent_not_rechecked": unavailable_builds, "generated_current_files_rechecked": file_matches, "raw_file_pairs_absent_not_rechecked": unavailable_files, "retained_original_statuses": retained_statuses, "identity_boundary": "Same source is not a unique run-to-file manifest. Git blob identity and present byte equality are not historical serving proof."}

    audit.run("selected_build_artifact_and_original_status_bindings", selected_identity_bindings)

    def byte_costs():
        calculated = {}
        for stream in ("python", "r"):
            receipts = [receipt_data[r["id"]] for r in sources if r["stream"] == stream]
            calculated[stream] = {"logical_gets": len(receipts), "body_bytes": sum(r["bytes"] for r in receipts)}
        inc_attempts = jsonl(root / "streams/incidents/attempts.jsonl")
        direct = [r for r in inc_attempts if r.get("transport") == "direct_public_http"]
        calculated["incidents"] = {"logical_gets": len(direct), "body_bytes": sum(r["bytes_downloaded"] for r in direct)}
        connector_calls = sum(r.get("connector_calls", 0) for r in inc_attempts)
        pr_attempts = jsonl(root / "streams/preservation/attempts.jsonl")
        audit.require(len({r["id"] for r in pr_attempts}) == len(pr_attempts), "Repeated preservation attempt IDs")
        calculated["preservation"] = {"logical_gets": len(pr_attempts), "body_bytes": sum(r["response_bytes"] for r in pr_attempts)}
        count = sum(r["logical_gets"] for r in calculated.values())
        size = sum(r["body_bytes"] for r in calculated.values())
        audit.require(count == 172 == costs["instrumented_logical_http_gets"], "Instrumented GET count mismatch")
        audit.require(size == 7377636 == costs["instrumented_response_body_bytes"], "Instrumented response bytes mismatch")
        audit.require(connector_calls == 46 == costs["incident_github_connector_calls_separate"], "Connector calls mismatch")
        archives = [r for r in pr_attempts if r.get("category") == "archive_download"]
        archive_bytes = sum(r["response_bytes"] for r in archives)
        audit.require(len(archives) == 2 and archive_bytes == 3542168, "Preservation archive cost mismatch")
        audit.require(archive_bytes == costs["preservation_archive_download_bytes_subset"], "Archive bytes incorrectly totalled")
        return {"by_stream": calculated, "logical_gets": count, "body_bytes": size, "connector_calls_separate": connector_calls, "archive_bytes_subset": archive_bytes, "unknown_not_zero": costs["not_measured"]}

    audit.run("recorded_request_and_byte_cost_arithmetic", byte_costs)

    def incident_sample():
        first = [r for r in incidents if r["sampling_group"] == "first12"]
        extra = [r for r in incidents if r["sampling_group"] != "first12"]
        audit.require(len(first) == 12 and len(extra) == 4 and len(incidents) == 16, "Incident strata not 12+4")
        repositories = Counter(r["repository"] for r in first)
        audit.require(repositories == Counter({"jimporter/mike": 3, "mkdocs/mkdocs": 3, "readthedocs/readthedocs.org": 3, "actions/deploy-pages": 3}), "First12 quota is not 3 per four repositories")
        ordered = sorted(first, key=lambda r: (utc(r["created_utc"]), int(r["issue_number"])))
        audit.require([int(r["chronological_rank_first12"]) for r in ordered] == list(range(1, 13)), "First12 coding ranks not createdUTC then issue number")
        for row in incidents:
            instant = utc(row["created_utc"])
            audit.require(utc("2024-01-01T00:00:00Z") <= instant < utc("2026-01-01T00:00:00Z"), f"{row['incident_id']}: incident outside 2024–2025")
            audit.require(bool(row["admission_or_rejection"]), f"{row['incident_id']}: missing admission/rejection")
        strong_first = sum(truth(r["strong_complete_counterexample"]) for r in first)
        strong_extra = sum(truth(r["strong_complete_counterexample"]) for r in extra)
        audit.require(strong_first == 0 and strong_extra == 0, "Frozen strong-counterexample result changed")
        relevant = [r for r in incidents if truth(r["relevant_for_minimum"])]
        audit.require(len(relevant) == 12 and len({r["lineage_id"] for r in relevant}) == 12, "Relevant independent incident count mismatch")
        return {"first12": len(first), "quota_by_repository": dict(repositories), "supplement": len(extra), "first12_strong": strong_first, "supplement_strong": strong_extra, "relevant_independent_events": len(relevant), "order_boundary": "CreatedUTC→issue-number coding order after quota3×4; concurrent transport is not falsely called sequential retrieval; not all-web first12."}

    audit.run("incident_stratification_chronology_and_zero_strong", incident_sample)

    def preservation_pairs():
        institutions = {r["institution"] for r in pairs}
        works = defaultdict(list)
        for row in pairs:
            works[(row["institution"], row["work"])].append(row)
            audit.require(row["source_id"] in by_id and by_id[row["source_id"]]["countable_original"], f"Version record {row['source_id']} is not a countable source")
            if row.get("manifest_source"):
                audit.require(row["manifest_source"] in by_id, f"Missing manifest source {row['manifest_source']}")
        audit.require(len(pairs) == 6 and len(works) == 3 and len(institutions) == 2, "Cross-domain design is not 2 institutions / 3 pairs / 6 actual records")
        for (institution, work), records in works.items():
            audit.require(len(records) == 2 and len({r["version"] for r in records}) == 2, f"{work}: not two actual distinct versions")
            if institution == "Zenodo":
                audit.require(len({r["concept_doi"] for r in records}) == 1 and len({r["version_doi"] for r in records}) == 2, f"{work}: DOI relationship mismatch")
                for record in records:
                    audit.require(bool(record.get("file_name")) and bool(record.get("publisher_checksum")) and record.get("publisher_size", 0) > 0, f"{work}: missing publisher file manifest")
                    if record.get("download_verified"):
                        manifests = [r for r in receipt_data.values() if r.get("record_id") == record["record_id"] and r.get("members")]
                        audit.require(len(manifests) == 1, f"{work}/{record['version']}: missing direct archive manifest")
                        if manifests:
                            item = manifests[0]
                            audit.require(item["sha256"] == record["direct_sha256"] and item["publisher_checksum_equal"] is True, f"{work}/{record['version']}: archive checksum fields disagree")
            else:
                for record in records:
                    audit.require(record["direct_sha256"] == record["publisher_sha256"] and record["checksum_equal"] is True, f"{work}/{record['version']}: recorded representative file checksum mismatch")
                    audit.require(record["root_entries"] > 0 and record["synthetic"] is True, f"{work}: directory/synthetic classification missing")
        return {"institutions": sorted(institutions), "pairs": len(works), "actual_records": len(pairs), "works": [work for _, work in works], "limitation": "Manifest/receipt consistency; absent full ZIPs are not newly downloaded or independently rehashed by this run."}

    audit.run("cross_domain_actual_version_pairs_and_manifests", preservation_pairs)

    def prior_and_git_scope():
        names = audit.git("ls-tree", "-r", "--name-only", PRIOR, "--", OWNED).decode().splitlines()
        priors = sorted(path for path in names if path.endswith("/prerecommendations.json"))
        audit.require(len(priors) == 3, "Prior commit does not contain the expected three recommendation files")
        matches = []
        for relative in priors:
            earlier = audit.git("show", f"{PRIOR}:{relative}")
            current = (audit.repo / relative).read_bytes()
            audit.require(earlier == current, f"Prerecommendation changed after frozen commit: {relative}")
            matches.append({"path": relative, "sha256": digest(current), "byte_identical": earlier == current})
        changed = audit.git("diff", "--name-only", "-z", BASE, "--").decode().split("\0")
        outside = [p for p in changed if p and not p.startswith(OWNED)]
        audit.require(not outside, f"Tracked changes outside owned_path: {outside}")
        committed = audit.git("diff", "--name-only", "-z", BASE, "HEAD", "--").decode().split("\0")
        committed_outside = [p for p in committed if p and not p.startswith(OWNED)]
        audit.require(not committed_outside, f"Committed changes outside owned_path: {committed_outside}")
        return {"prior_commit": PRIOR, "prior_files": matches, "local_head": audit.git("rev-parse", "HEAD").decode().strip(), "base_commit": BASE, "tracked_changed_paths": len([p for p in changed if p]), "outside_owned_path": outside, "committed_outside_owned_path": committed_outside, "scope_boundary": "Local Git objects/index/worktree only; no remote reread, fetch, commit, index update or branch mutation performed."}

    audit.run("prerecommendation_immutability_and_tracked_change_scope", prior_and_git_scope)

    def historical_unknowns():
        slot_rows = denominators["slots"]
        main_count = sum(truth(r["main_historical_target_identified"]) for r in slot_rows)
        unknown_count = sum(r["main_historical_status"] == "unconfirmed" for r in slot_rows)
        audit.require(main_count == 0 == denominators["main_historical_target_identified"], "Historical path numerator changed")
        audit.require(unknown_count == 9 == denominators["main_historical_unknown"], "Historical path unknown count changed")
        audit.require(denominators["joint_historical_confirmation"] == {"numerator": 0, "denominator": 1, "unknown": 1, "refuted": 0}, "Joint confirmation denominator/result changed")
        pages = [r for r in routes if r.get("stage") == "deployment_current_retained_status"]
        audit.require(len(pages) == 2 and all(r.get("provider_reported_success_directly_observed") is False for r in pages), "Inactive converted to direct provider success")
        audit.require(all(r.get("final_retained_status") == "inactive" for r in pages), "Retained selected Pages status differs")
        audit.require(denominators["other_cases_joint_confirmation"]["numerator"] == 0 and denominators["other_cases_joint_confirmation"]["denominator"] == 0, "No-applicable-owner-condition 0/0 changed")
        return {"research_verdict": "PARTIAL", "reason": "P3 main-window dual-route identification and R1 historical final-publication chain remain unconfirmed.", "historical_paths": f"{main_count}/9", "joint_confirmation": "0/1; unknown1; refuted0", "other_cases_joint": "0/0 not computable", "pages_direct_success": "0/2", "structural_pass_is_not_research_completion": True}

    audit.run("partial_research_verdict_and_nonconflated_denominators", historical_unknowns)

    result_path = root / "RESULT.md"
    if result_path.exists():
        def result_structure():
            audit.remember(result_path)
            lines = result_path.read_text().splitlines()
            headers = []
            header_lines = []
            for number in range(len(lines) - 1):
                line = lines[number].strip()
                separator = lines[number + 1].strip()
                if line.startswith("|") and re.fullmatch(r"\|[\s:\-|]+\|", separator) and "-" in separator:
                    headers.append([normalized(c) for c in line.strip("|").split("|")])
                    header_lines.append(number + 1)
            audit.require(headers[:3] == [[normalized(c) for c in table] for table in TABLE_HEADERS], "First three RESULT table headers/order differ from requested columns")
            weakness_headers = [i for i, line in enumerate(lines) if re.match(r"^#{1,6}\s", line) and ("약점" in line or "불일치" in line)]
            audit.require(bool(weakness_headers), "Missing final weakness/discrepancy section")
            numbered = []
            if weakness_headers:
                start = weakness_headers[-1]
                tail = lines[start + 1:]
                numbered = [int(m.group(1)) for line in tail if (m := re.match(r"^(\d+)[.)]\s", line))]
                audit.require(numbered == [1, 2, 3], "Final weakness section must have exactly numbered1,2,3")
                audit.require(not any(re.match(r"^#{1,6}\s", line) for line in tail), "A new section follows the final weakness section")
            audit.require("PARTIAL" in result_path.read_text(), "RESULT does not state the remaining PARTIAL verdict")
            return {"first_table_header_line_numbers": header_lines[:3], "required_table_headers": TABLE_HEADERS, "final_weakness_numbers": numbered}
        audit.run("result_required_tables_and_exactly_three_final_weaknesses", result_structure)
    else:
        audit.pending("result_required_tables_and_exactly_three_final_weaknesses", "RESULT.md not present at this invocation; rerun after authoring.", args.require_final_docs)

    for filename, terms in [("cards.md", list(WINDOWS)), ("SELF_CHECK.md", [f"Q{i}" for i in range(1, 8)])]:
        path = root / filename
        if path.exists():
            def document_coverage(path=path, terms=terms):
                audit.remember(path)
                content = path.read_text()
                for term in terms:
                    audit.require(bool(re.search(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])", content)), f"{path.name}: missing {term}")
                return {"terms_checked": terms, "scope": "Label/coverage presence only; claim correctness remains tied to sources and human review."}
            audit.run(f"{filename}_coverage", document_coverage)
        else:
            audit.pending(f"{filename}_coverage", f"{filename} not present at this invocation; rerun after authoring.", args.require_final_docs)

    def stable_inputs():
        for path, before in audit.snapshots.items():
            audit.require(digest((root / path).read_bytes()) == before, f"Input changed while validator was running: {path}")
        return {"input_snapshots": dict(sorted(audit.snapshots.items())), "validator_sha256": digest(Path(__file__).read_bytes())}

    audit.run("input_snapshot_stability", stable_inputs)
    failures = sum(check["status"] == "FAIL" for check in audit.checks)
    pending = sum(check["status"] == "PENDING" for check in audit.checks)
    report = {
        "schema": 1, "task_id": "AF-RES-086",
        "checked_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "structural_status": "FAIL" if failures else "PASS",
        "research_verdict": "PARTIAL",
        "completion_status": "PENDING_FINAL_DOCUMENT_CHECKS" if pending else "CHECKS_EXECUTED",
        "exit_code": 1 if failures else 0,
        "check_counts": dict(Counter(c["status"] for c in audit.checks)),
        "network_requests_made": 0, "git_mutations_made": 0,
        "limitations": [
            "The validator checks consistency, frozen scope and available bytes; it cannot create missing historical response or publication evidence.",
            "Full bodies intentionally absent are explicitly listed; matching stored receipt fields is not a new measurement of absent bytes.",
            "Local Git verification is separate from required remote reread and workbench.session check --fetch.",
            "Missing final documents are PENDING by default and fatal only with --require-final-docs.",
        ],
        "checks": audit.checks,
    }
    if args.output is not None:
        output = args.output.resolve()
        if not output.is_relative_to(root):
            parser.error("--output must be inside AF-RES-086 owned_path")
        if output.exists():
            previous = read_json(output)
            history = list(previous.get("previous_runs", []))
            if previous.get("checked_utc"):
                snapshot_check = next((c for c in previous.get("checks", []) if c["check"] == "input_snapshot_stability"), {})
                history.append({
                    "checked_utc": previous["checked_utc"],
                    "structural_status": previous.get("structural_status"),
                    "research_verdict": previous.get("research_verdict"),
                    "exit_code": previous.get("exit_code"),
                    "check_counts": previous.get("check_counts"),
                    "nonpassing_checks": [{"check": c["check"], "status": c["status"], "issues": c.get("issues", [])} for c in previous.get("checks", []) if c["status"] != "PASS"],
                    "input_snapshots": snapshot_check.get("details", {}).get("input_snapshots", {}),
                    "validator_sha256": snapshot_check.get("details", {}).get("validator_sha256"),
                })
            report["previous_runs"] = history
        report["validation_method_note"] = "The initial validator used build creation for the P1 main-window test; corrected to the preregistered completion boundary. Initial missing R excerpt-path failures were data-reference errors, corrected by the integrator. Earlier run results remain in previous_runs."
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload)
    sys.stdout.write(payload)
    return report["exit_code"]


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError, csv.Error) as error:
        # Malformed required input cannot be represented as a successful audit.
        sys.stdout.write(json.dumps({"structural_status": "FAIL", "research_verdict": "PARTIAL", "exit_code": 1, "fatal_input_error": f"{type(error).__name__}: {error}", "network_requests_made": 0, "git_mutations_made": 0}, ensure_ascii=False) + "\n")
        sys.exit(1)
