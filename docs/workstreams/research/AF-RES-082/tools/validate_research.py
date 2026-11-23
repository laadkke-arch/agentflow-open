#!/usr/bin/env python3
"""Validate AF-RES-082's recorded evidence, entirely offline.

This is a structural/accounting audit, not a replay of a deployment or a claim
that unknown evidence is false.  Read-only git show binds the two prior seals.
Only evidence/validation.json is written.  --final also rejects unfinished
post-budget placeholders; an explicit unconfirmed result remains valid.
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys


OWNED = Path(__file__).resolve().parents[1]
REPO = OWNED.parents[3]
RELATIVE = OWNED.relative_to(REPO).as_posix()
PRELINKS_COMMIT = "8ba1d686d4c7e50067f9d52bc753a4e02708cd42"
BUDGET_COMMIT = "5f881c7094bf30be13069554b412a00c5b01f7c0"
EXPECTED_CASES = {"P1", "P2", "P3", "R1", "R2", "R3"}
EXPECTED_ORGS = {"pypa": 58, "r-lib": 164}
SOURCE_FIELDS = (
    "source_id", "lineage_id", "canonical_lineage", "kind", "url",
    "version", "section", "opened_at_utc", "questions", "case_ids",
    "observed", "limitations", "claim_support", "directly_opened",
    "count_toward_minimum",
)
EMPTY_ALLOWED = {"case_ids"}  # Recruitment exclusions need not become a case.
SOURCE_TOKEN = re.compile(
    r"(?<![A-Za-z0-9-])(?:ROOT-[A-Z0-9][A-Z0-9-]*|"
    r"PY-[A-Z0-9][A-Z0-9-]*|R-(?:P)?[0-9]+|PUB[0-9]+|INC[0-9]+)"
    r"(?![A-Za-z0-9-])"
)


def sha256(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def csv_rows(body: bytes) -> tuple[list[str], list[dict[str, str]]]:
    reader = csv.DictReader(io.StringIO(body.decode("utf-8-sig")))
    rows = list(reader)
    return list(reader.fieldnames or []), rows


def git_read(*args: str) -> bytes:
    completed = subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, check=False
    )
    if completed.returncode:
        raise RuntimeError(
            "Read-only git command failed: "
            + " ".join(args)
            + ": "
            + completed.stderr.decode("utf-8", errors="replace").strip()
        )
    return completed.stdout


def valid_utc(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        # A recorded read-time interval is valid when both ends specify UTC.
        times = [dt.datetime.fromisoformat(x.replace("Z", "+00:00"))
                 for x in value.split("/")]
        return bool(times) and all(
            x.tzinfo is not None and x.utcoffset() == dt.timedelta(0)
            for x in times
        )
    except ValueError:
        return False


def split_references(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if not isinstance(value, str) or not value.strip():
        return []
    if value.lstrip().startswith("["):
        return split_references(json.loads(value))
    return [token for token in re.split(r"[;,\s]+", value.strip()) if token]


def source_references(value: object, location: str = ""):
    """Yield explicit reference fields, including nested artifact records."""
    if isinstance(value, dict):
        for key, item in value.items():
            loc = f"{location}.{key}" if location else key
            if (key in {"source_id", "source_ids", "sources"}
                    or key.endswith("_source_id")
                    or key.endswith("_source_ids")):
                for reference in split_references(item):
                    yield loc, reference
            elif isinstance(item, (dict, list)):
                yield from source_references(item, loc)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from source_references(item, f"{location}[{index}]")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final", action="store_true",
                        help="also reject unfinished post-budget placeholders")
    args = parser.parse_args()
    report: dict = {
        "schema_version": 1,
        "validated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "mode": "final" if args.final else "working",
        "command": "python -B " + RELATIVE + "/tools/validate_research.py"
                   + (" --final" if args.final else ""),
        "network_requests": 0,
        "scope": "Offline structural, reference, frozen-column and denominator audit",
        "unknown_policy": (
            "unconfirmed/unknown/미확인 are valid research outcomes. A failed "
            "check means an integrity/accounting mismatch or, in final mode, "
            "unfinished work; it does not mean an unobserved deployment failed."
        ),
        "inputs": {}, "metrics": {}, "checks": [],
    }

    def check(name: str, condition: bool, observed: object,
              expected: object = None) -> None:
        entry = {"name": name, "status": "pass" if condition else "fail",
                 "observed": observed}
        if expected is not None:
            entry["expected"] = expected
        report["checks"].append(entry)

    def read(name: str) -> bytes:
        body = (OWNED / name).read_bytes()
        report["inputs"][name] = {"bytes": len(body), "sha256": sha256(body)}
        return body

    try:
        report["working_tree_head"] = git_read("rev-parse", "HEAD").decode().strip()
        csv_data = {}
        for name in ("FRAME.csv", "requirements.csv", "paths.csv", "prelinks.csv"):
            body = read(name)
            columns, rows = csv_rows(body)
            csv_data[name] = (body, columns, rows)
            malformed = [i + 2 for i, row in enumerate(rows)
                         if None in row or any(value is None for value in row.values())]
            check(f"{name}:parse", not malformed and len(columns) == len(set(columns)),
                  {"rows": len(rows), "malformed_lines": malformed})
        sources = [json.loads(line) for line in read("sources.jsonl").splitlines() if line]
        deployments = [json.loads(line) for line in read("deployments.jsonl").splitlines() if line]
        frozen = json.loads(read("evidence/cases-frozen.json"))
        budget = json.loads(read("evidence/budget-seal.json"))
        http_receipts = [json.loads(line) for line in read("evidence/http-receipts.jsonl").splitlines()
                         if line]
        lineage_index = json.loads(read("evidence/lineage-index.json"))
        frame = csv_data["FRAME.csv"][2]
        requirements = csv_data["requirements.csv"][2]
        paths = csv_data["paths.csv"][2]
        prelinks = csv_data["prelinks.csv"][2]
        metrics = report["metrics"]

        # Complete recruitment frames, with names/order preserved from intake.
        org_counts = dict(collections.Counter(row["org"] for row in frame))
        metrics["frame_rows"] = len(frame)
        metrics["frame_by_org"] = org_counts
        check("frame:222_and_58_164", len(frame) == 222 and org_counts == EXPECTED_ORGS,
              org_counts, EXPECTED_ORGS)
        check("frame:unique_repositories", len({r["full_name"] for r in frame}) == len(frame),
              len({r["full_name"] for r in frame}), len(frame))
        invalid_visibility = [r["full_name"] for r in frame
                              if r["fork"].lower() != "false" or r["private"].lower() != "false"]
        check("frame:public_nonfork", not invalid_visibility, invalid_visibility)
        for org, count in EXPECTED_ORGS.items():
            subset = [r for r in frame if r["org"] == org]
            fixed_frame = json.loads(read(f"evidence/{org}-frame.json"))["repositories"]
            observed_order = [(r["full_name"], int(r["original_rank"])) for r in subset]
            expected_order = [(r["full_name"], int(r["original_rank"])) for r in fixed_frame]
            sorted_names = sorted((r["name"] for r in subset), key=lambda x: (x.casefold(), x))
            check(f"frame:{org}:frozen_order", observed_order == expected_order
                  and [r["name"] for r in subset] == sorted_names
                  and [int(r["original_rank"]) for r in subset] == list(range(1, count + 1)),
                  {"rows": len(subset), "matches_intake": observed_order == expected_order})
        unexplained = [r["full_name"] for r in frame if not r["status"]
                       or (r["status"] != "included" and not r["exclusion_reason"])]
        check("frame:exclusion_and_unscreened_reasons", not unexplained, unexplained)

        # Both seals are inspected from local git objects; no fetch is attempted.
        pre_seal = git_read("show", f"{PRELINKS_COMMIT}:{RELATIVE}/prelinks.csv")
        budget_seal = git_read("show", f"{BUDGET_COMMIT}:{RELATIVE}/paths.csv")
        report["frozen_baselines"] = {
            "prelinks": {"commit": PRELINKS_COMMIT, "sha256": sha256(pre_seal)},
            "paths": {"commit": BUDGET_COMMIT, "sha256": sha256(budget_seal)},
        }
        check("seal:prelinks_exact_bytes", csv_data["prelinks.csv"][0] == pre_seal,
              sha256(csv_data["prelinks.csv"][0]), sha256(pre_seal))
        sealed_columns, sealed_paths = csv_rows(budget_seal)
        prior_columns = [c for c in sealed_columns
                         if not c.startswith("postbudget") and c != "same_historical_deployment"]
        current_prior_columns = [c for c in csv_data["paths.csv"][1]
                                 if not c.startswith("postbudget") and c != "same_historical_deployment"]
        changes = []
        if len(paths) != len(sealed_paths):
            changes.append({"row_count": [len(sealed_paths), len(paths)]})
        for index, (previous, current) in enumerate(zip(sealed_paths, paths), 1):
            for column in prior_columns:
                if previous.get(column) != current.get(column):
                    changes.append({"row": index, "column": column,
                                    "frozen": previous.get(column), "current": current.get(column)})
        check("seal:all_prebudget_columns", not changes and prior_columns == current_prior_columns,
              {"columns_checked": prior_columns, "differences": changes,
               "column_order_matches": prior_columns == current_prior_columns})

        # The immutable initial links bind case identity, rank, tag and SHA.
        _, initial_rows = csv_rows(pre_seal)
        initial = {r["case_id"]: r for r in initial_rows}
        selected = {r["case_id"]: r for r in frame if r["status"] == "included"}
        frozen_values = {row[0]: row for row in frozen["case_values"]}
        identity_errors = []
        for case, prior in initial.items():
            row = selected.get(case, {})
            expected = [case, prior["repo"], int(prior["original_rank"]), prior["tag"], prior["tag_sha"],
                        prior["reader_url"], prior["requirement_1"], prior["requirement_2"]]
            if frozen_values.get(case) != expected:
                identity_errors.append([case, "cases-frozen differs from sealed prelinks"])
            for field, before_field in (("full_name", "repo"), ("original_rank", "original_rank"),
                                        ("last_2024_2025_formal_tag", "tag"), ("tag_sha", "tag_sha")):
                if row.get(field) != prior[before_field]:
                    identity_errors.append([case, "FRAME", field, row.get(field), prior[before_field]])
            for name, rows in (("requirements", requirements), ("paths", paths), ("prelinks", prelinks)):
                for current in (x for x in rows if x["case_id"] == case):
                    for field in ("repo", "original_rank", "tag", "tag_sha"):
                        if current[field] != prior[field]:
                            identity_errors.append([case, name, field, current[field], prior[field]])
        case_sets = {"initial_seal": sorted(initial), "included_frame": sorted(selected),
                     "frozen_file": sorted(frozen_values),
                     "requirements": sorted({r["case_id"] for r in requirements}),
                     "paths": sorted({r["case_id"] for r in paths})}
        metrics["fixed_case_count"] = len(initial)
        check("cases:fixed_six", all(set(v) == EXPECTED_CASES for v in case_sets.values())
              and frozen["case_count"] == 6 and not identity_errors,
              {"sets": case_sets, "identity_errors": identity_errors}, sorted(EXPECTED_CASES))

        requirements_per_case = dict(collections.Counter(r["case_id"] for r in requirements))
        confirmed = [r for r in requirements if r["status"] == "confirmed"]
        confirmed_second = [r for r in confirmed if re.search(r"-(?:R|C)2$", r["requirement_id"])]
        metrics["requirements"] = {"rows": len(requirements), "confirmed": len(confirmed),
            "confirmed_second_conditions": len(confirmed_second),
            "second_condition_cases": [r["case_id"] for r in confirmed_second],
            "status_counts": dict(collections.Counter(r["status"] for r in requirements))}
        check("requirements:12_rows_two_per_case", len(requirements) == 12
              and requirements_per_case == {case: 2 for case in EXPECTED_CASES}
              and len({r["requirement_id"] for r in requirements}) == 12,
              requirements_per_case)
        check("requirements:seven_confirmed_one_second", len(confirmed) == 7
              and len(confirmed_second) == 1, metrics["requirements"],
              {"confirmed": 7, "confirmed_second_conditions": 1})

        # Twelve applications of two documents are not twenty-four HTTP requests.
        pair_counts = collections.Counter((r["case_id"], r["arm"]) for r in paths)
        expected_pairs = {(case, arm) for case in EXPECTED_CASES for arm in ("A", "B")}
        check("paths:twelve_unique_case_arms", len(paths) == 12
              and set(pair_counts) == expected_pairs and all(v == 1 for v in pair_counts.values()),
              [list(key) + [count] for key, count in sorted(pair_counts.items())])
        exposure_rows = []
        budget_errors = []
        for row in paths:
            label = f"{row['case_id']}-{row['arm']}"
            urls = []
            for ordinal in (1, 2):
                prefix = f"exposure_{ordinal}_"
                urls.append(row[prefix + "url"])
                reused = row[prefix + "reused"]
                if reused not in {"true", "false"}:
                    budget_errors.append([label, "reuse flag", reused])
                exposure_rows.append({"arm": label, "source_id": row[prefix + "source_id"],
                                      "url": row[prefix + "url"], "reused": reused == "true"})
                if not all(row[prefix + suffix] for suffix in ("source_id", "url", "section")):
                    budget_errors.append([label, "missing exposure", ordinal])
            if (int(row["reading_budget"]) != 2 or int(row["case_document_assessments"]) != 2
                    or int(row["budget_unique_documents"]) != len(set(urls)) or len(set(urls)) != 2):
                budget_errors.append([label, "not exactly two recorded documents"])
            first = sum(row[f"exposure_{i}_reused"] == "false" for i in (1, 2))
            if int(row["allocated_first_fetches"]) != first:
                budget_errors.append([label, "first-fetch allocation differs", first])
            if len(json.loads(row["initial_links"])) != int(row["link_count"]):
                budget_errors.append([label, "link count differs"])
        reads = len(exposure_rows)
        fresh = sum(not row["reused"] for row in exposure_rows)
        reused = sum(row["reused"] for row in exposure_rows)
        urls = {row["url"] for row in exposure_rows}
        by_url = collections.defaultdict(list)
        for row in exposure_rows:
            by_url[row["url"]].append(row)
        allocation_ok = all(sum(not row["reused"] for row in rows) == 1 for rows in by_url.values())
        metrics["reading_budget"] = {"paths": len(paths), "logical_exposures": reads,
            "unique_documents": len(urls), "new_budget_http_allocations": fresh,
            "reused_exposures": reused,
            "note": "First-fetch allocation is accounting, not claimed concurrent-request order."}
        check("paths:two_documents_each", not budget_errors, budget_errors)
        check("paths:24_exposures_6_new_18_reused", (reads, fresh, reused, len(urls)) == (24, 6, 18, 6)
              and allocation_ok and int(budget["external_http_requests"]) == fresh
              and int(budget["case_document_assessments"]) == reads
              and int(budget["cross_case_document_reuses"]) == reused,
              metrics["reading_budget"])
        budget_receipts = [row for row in http_receipts if row.get("phase") == "budget"]
        recorded_requests = sum(int(row["http_requests_including_redirects"]) for row in budget_receipts)
        recorded_top_level = sum(int(row["top_level_requests"]) for row in budget_receipts)
        recorded_redirects = sum(len(row["redirects"]) for row in budget_receipts)
        receipt_errors = []
        budget_sources = {row["url"]: row for row in sources if row.get("phase") == "budget"}
        for receipt in budget_receipts:
            source = budget_sources.get(receipt["url"], {})
            if (receipt.get("http_status") != 200 or receipt.get("cache_reuse") is not False
                    or source.get("sha256") != receipt.get("body_sha256")):
                receipt_errors.append(receipt["url"])
        metrics["reading_budget"].update({
            "recorded_budget_http_requests_including_redirects": recorded_requests,
            "recorded_budget_top_level_requests": recorded_top_level,
            "recorded_budget_redirects": recorded_redirects,
        })
        check("paths:budget_http_receipts_and_fingerprints", len(budget_receipts) == 6
              and recorded_requests == recorded_top_level == fresh == 6 and recorded_redirects == 0
              and {row["url"] for row in budget_receipts} == urls and not receipt_errors,
              {"receipt_count": len(budget_receipts), "requests": recorded_requests,
               "top_level": recorded_top_level, "redirects": recorded_redirects,
               "status_or_fingerprint_errors": receipt_errors})

        # Normalized ledger contract. Empty case_ids is legitimate for exclusions.
        source_ids = [row.get("source_id") for row in sources]
        sources_by_id = {row["source_id"]: row for row in sources}
        duplicate_ids = [key for key, count in collections.Counter(source_ids).items() if count > 1]
        schema_errors = []
        for row in sources:
            sid = row.get("source_id", "<missing>")
            for field in SOURCE_FIELDS:
                if field not in row or (field not in EMPTY_ALLOWED and row[field] in (None, "", [])):
                    schema_errors.append([sid, field, "missing/empty"])
            for field in ("questions", "case_ids"):
                if not isinstance(row.get(field), list):
                    schema_errors.append([sid, field, "expected list"])
            if not valid_utc(row.get("opened_at_utc")):
                schema_errors.append([sid, "opened_at_utc", "invalid UTC instant/interval"])
            if not str(row.get("url", "")).startswith(("https://", "http://")):
                schema_errors.append([sid, "url", "not public HTTP(S)"])
            for field in ("directly_opened", "count_toward_minimum"):
                if not isinstance(row.get(field), bool):
                    schema_errors.append([sid, field, "expected boolean"])
            if row.get("count_toward_minimum") and row.get("directly_opened") is not True:
                schema_errors.append([sid, "count_toward_minimum", "not directly opened"])
        check("sources:unique_ids", not duplicate_ids, duplicate_ids)
        check("sources:required_fields_and_types", not schema_errors, schema_errors)

        references = []
        for label, rows in (("requirements", requirements), ("paths", paths), ("deployments", deployments)):
            for index, row in enumerate(rows, 1):
                references.extend((label, index, location, sid)
                                  for location, sid in source_references(row))
        # Post-budget evidence may mention source IDs or deployment/event IDs in prose.
        event_ids = {str(row.get("event_id") or row.get("deployment_id")) for row in deployments}
        postbudget_event_references = []
        for index, row in enumerate(paths, 1):
            for token in SOURCE_TOKEN.findall(row.get("postbudget_evidence", "")):
                if token in event_ids and token not in sources_by_id:
                    postbudget_event_references.append([index, token])
                else:
                    references.append(("paths", index, "postbudget_evidence", token))
        unresolved = [list(ref) for ref in references if ref[-1] not in sources_by_id]
        metrics["source_references"] = {
            "occurrences": len(references), "unique_ids": len({r[-1] for r in references}),
            "by_file": dict(collections.Counter(r[0] for r in references)),
            "postbudget_event_references": postbudget_event_references,
            "unresolved": len(unresolved),
        }
        check("references:all_source_ids_join", not unresolved, unresolved)

        counted = [row for row in sources if row.get("count_toward_minimum") is True
                   and row.get("directly_opened") is True]
        lineages = sorted({row["canonical_lineage"] for row in counted})
        index_lineages = sorted(row["canonical_lineage"] for row in lineage_index if row["counted_source_ids"])
        metrics["sources"] = {"rows": len(sources), "unique_ids": len(set(source_ids)),
            "directly_opened_rows": sum(row.get("directly_opened") is True for row in sources),
            "counted_source_rows": len(counted), "independent_lineages": len(lineages),
            "lineages": lineages}
        check("sources:at_least_22_independent_lineages", len(lineages) >= 22, len(lineages), ">=22")
        check("sources:lineage_index_agrees", lineages == index_lineages,
              {"ledger_count": len(lineages), "index_count": len(index_lineages),
               "only_ledger": sorted(set(lineages) - set(index_lineages)),
               "only_index": sorted(set(index_lineages) - set(lineages))})

        # Conservative event counting: four explicit incident lineages plus
        # separately flagged preservation records and explicit failed run records.
        # An unknown deployment state is never classified as a failure.
        events = {}
        for row in counted:
            if row.get("actual_incident") is True:
                events.setdefault(row["canonical_lineage"], []).append(
                    {"source_id": row["source_id"], "basis": "actual_incident=true"})
        for row in deployments:
            qualifying = row.get("count_as_preservation_or_failure_event") is True or row.get("success") is False
            if qualifying:
                refs = [sid for _, sid in source_references(row)]
                canonical = next((sources_by_id[sid]["canonical_lineage"] for sid in refs
                                  if sid in sources_by_id), row.get("lineage_id"))
                events.setdefault(canonical, []).append({
                    "record_id": row.get("event_id") or row.get("deployment_id"),
                    "basis": "explicit preservation flag" if row.get("count_as_preservation_or_failure_event")
                             else "explicit unsuccessful run",
                })
        originals = [row for row in counted if row.get("is_original_publication_record") is True]
        original_lineages = sorted({row["canonical_lineage"] for row in originals})
        metrics["events"] = {"conservatively_counted_failure_or_preservation_lineages": len(events),
            "basis_by_lineage": events,
            "excluded_from_this_count": "Unknowns, generic contract capabilities, and unflagged inferred events."}
        metrics["other_domain_originals"] = {"record_count": len(originals),
            "source_ids": [row["source_id"] for row in originals],
            "independent_lineage_count": len(original_lineages), "lineages": original_lineages}
        check("events:at_least_four", len(events) >= 4, metrics["events"], ">=4 independent lineages")
        check("publication:at_least_four_original_records", len(originals) >= 4
              and len(original_lineages) >= 4, metrics["other_domain_originals"],
              ">=4 original records, conservatively also >=4 lineages")

        placeholders = {"", "pending", "not_opened", "todo", "tbd"}
        unfinished = []
        for row in paths:
            for field in ("postbudget_evidence", "postbudget_verdict", "same_historical_deployment"):
                if row.get(field, "").strip().lower() in placeholders:
                    unfinished.append({"case_id": row["case_id"], "arm": row["arm"],
                                       "field": field, "value": row.get(field)})
        metrics["unfinished_postbudget_fields"] = unfinished
        if args.final:
            check("final:no_unfinished_postbudget_fields", not unfinished, unfinished)
        else:
            report["checks"].append({"name": "final:no_unfinished_postbudget_fields",
                "status": "pending" if unfinished else "pass", "observed": unfinished,
                "note": "Working mode permits placeholders. Run --final after post-budget synthesis."})

    except Exception as error:
        report["checks"].append({"name": "validator:execution", "status": "fail",
                                 "observed": f"{type(error).__name__}: {error}"})

    status_counts = dict(collections.Counter(item["status"] for item in report["checks"]))
    report["check_status_counts"] = status_counts
    report["exit_code"] = 1 if status_counts.get("fail", 0) else 0
    report["result"] = ("fail" if report["exit_code"] else
                        "pass_with_pending" if status_counts.get("pending", 0) else "pass")
    output = OWNED / "evidence" / "validation.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": report["result"], "exit_code": report["exit_code"],
                      "check_status_counts": status_counts,
                      "metrics": report["metrics"], "output": str(output)}, ensure_ascii=False))
    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
