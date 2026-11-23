#!/usr/bin/env python3
"""Read-only, offline structural verification for the AF-RES-102 research bundle.

Run without arguments. This verifies recorded structure and arithmetic, not source
understanding, historical generation, network availability, or repository contracts.
It neither rewrites evidence nor replaces workbench.session/cloud_check.py.
"""

from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_EXCLUSIONS = {"GG-S3-126", "GG-S3-143", "GG-S3-145", "GG-S3-146", "GG-S3-147"}
PROJECTS = {"ggplot2": ("ggplot2", "GG", 68), "Matplotlib": ("matplotlib", "MP", 47)}
STRATA = ("general", "old_asset_absent", "asset_retained_source_changed")
CASE_IDS = {f"{prefix}-{letter}{slot}" for prefix in ("GG", "MP")
            for letter in ("G", "A", "C") for slot in (1, 2)}
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def stamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"Timestamp lacks timezone: {value}")
    return parsed


def truth(value):
    if value is True or str(value).lower() in ("true", "yes", "1"):
        return True
    if value is False or str(value).lower() in ("false", "no", "0"):
        return False
    raise ValueError(f"Unrecognized boolean: {value!r}")


class Verification:
    def __init__(self):
        self.started_utc = utc_now()
        self.checks = []
        self.inputs = {}

    def path(self, relative):
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
            raise ValueError(f"Expected nonempty task-relative path: {relative!r}")
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError(f"Path escapes task directory: {relative}")
        return path

    def read(self, relative):
        data = self.path(relative).read_bytes()
        self.inputs[relative] = hashlib.sha256(data).hexdigest()
        return data.decode("utf-8")

    def load(self, relative):
        return json.loads(self.read(relative))

    def rows(self, relative):
        return list(csv.DictReader(io.StringIO(self.read(relative))))

    def check(self, name, passed, **details):
        self.checks.append({"check": name, "passed": bool(passed), **details})

    def run_group(self, name, function):
        try:
            function()
        except Exception as error:
            self.check(name + ".read_or_schema_error", False,
                       error=f"{type(error).__name__}: {error}")

    def seals(self):
        for filename, expected in (("stage1-seal.json", 21), ("prediction-seal.json", 18)):
            seal = self.load("evidence/" + filename)
            files = seal["files"]
            mismatches = []
            for relative, expected_hash in files.items():
                path = self.path(relative)
                actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
                if actual != expected_hash:
                    mismatches.append({"path": relative, "expected": expected_hash, "actual": actual})
            self.check(filename, len(files) == expected and not mismatches,
                       expected_files=expected, observed_files=len(files), mismatches=mismatches)

    def frame_and_selection(self):
        frame = self.rows("frame.csv")
        predictions = self.rows("predictions.csv")
        self.check("frame.total", len(frame) == 115 and
                   sum(truth(row["eligible"]) for row in frame) == 80,
                   rows=len(frame), eligible=sum(truth(row["eligible"]) for row in frame))
        self.check("frame.projects", set(row["project"] for row in frame) == set(PROJECTS))
        for project, (directory, prefix, expected_rows) in PROJECTS.items():
            subset = [row for row in frame if row["project"] == project]
            eligible = [row for row in subset if truth(row["eligible"])]
            ordered = sorted(eligible, key=lambda row: row["hash_sha256"])
            child = self.rows(f"evidence/{directory}/frame.csv")
            failures = []
            for row in eligible:
                key = f"AF-RES-102|{project}|{row['old_section_path']}"
                if hashlib.sha256(key.encode("utf-8")).hexdigest() != row["hash_sha256"]:
                    failures.append(row["old_section_path"])
            self.check(f"frame.{project}", len(subset) == expected_rows and len(eligible) == 40
                       and [row["page_path"] for row in subset] == sorted(row["page_path"] for row in subset)
                       and len({row["page_path"] for row in subset}) == expected_rows
                       and [int(row["prefix_rank"]) for row in subset] == list(range(1, expected_rows + 1))
                       and [int(row["eligible_rank"]) for row in eligible] == list(range(1, 41))
                       and all(row["exclusion"] for row in subset if not truth(row["eligible"]))
                       and [row["page_path"] for row in subset] == [row["page_path"] for row in child]
                       and not failures,
                       rows=len(subset), eligible=len(eligible), invalid_hashes=failures)
            selected = self.load(f"evidence/{directory}/selected-general.json")
            if isinstance(selected, dict):
                selected = selected["selected"]
            selected_paths = [row.get("old_section_path", row.get("section_path")) for row in selected]
            expected_general = [row["old_section_path"] for row in ordered[:2]]
            actual_general = sorted((row for row in predictions if row["project"] == project
                                     and row["stratum"] == "general"), key=lambda row: int(row["slot"]))
            self.check(f"selection.{project}.general_first_two",
                       selected_paths == expected_general == [row["old_section_path"] for row in actual_general],
                       expected=expected_general, selected=selected_paths)

            if directory == "ggplot2":
                signals = self.load("evidence/ggplot2/signals-stage2.json")
                listing = self.load("evidence/ggplot2/new-paths.json")
                path_names = set(listing["paths"])
                complete = listing["truncated"] is False and all(
                    row["new_tree_complete"] and row["new_source_tree_complete"] for row in signals)
            else:
                container = self.load("evidence/matplotlib/all40-signals.json")
                signals = container["signals"]
                listing = self.load("evidence/matplotlib/new-publication-paths.json")
                path_names = {row["path"] for row in listing["tree"]}
                complete = listing["truncated"] is False and container["tree_complete"] is True
            signal_map = {row.get("old_section_path", row.get("section_path")): row for row in signals}
            signal_errors, absent, changed = [], [], []
            used = set(expected_general)
            for row in ordered:
                section = row["old_section_path"]
                signal = signal_map[section]
                asset = row["old_resource_path"]
                present = signal.get("legacy_path_present", signal.get("legacy_asset_path_present"))
                if asset and (asset in path_names) != present:
                    signal_errors.append(section + ": asset membership")
                if section not in used and asset and present is False and complete:
                    absent.append(section)
            used.update(absent[:2])
            for row in ordered:
                section = row["old_section_path"]
                signal = signal_map[section]
                present = signal.get("legacy_path_present", signal.get("legacy_asset_path_present"))
                source_present = signal["old_source_path_present"]
                new_blob = signal.get("new_source_blob", signal.get("new_blob_at_old_source_path"))
                source_changed = signal.get("source_blob_changed", signal.get("corresponding_source_blob_changed"))
                if row["source_path"] and source_present and source_changed != (new_blob != row["source_blob"]):
                    signal_errors.append(section + ": source blob comparison")
                if section not in used and row["old_resource_path"] and present is True and row["source_path"] \
                        and complete and (not source_present or source_changed):
                    changed.append(section)
            self.check(f"selection.{project}.complete_tree_signals", complete and len(signals) == 40
                       and len(signal_map) == 40 and set(signal_map) == {row["old_section_path"] for row in eligible}
                       and not signal_errors, signals=len(signals), tree_complete=complete, errors=signal_errors)
            for stratum, pool in (("old_asset_absent", absent), ("asset_retained_source_changed", changed)):
                slots = sorted((row for row in predictions if row["project"] == project
                                and row["stratum"] == stratum), key=lambda row: int(row["slot"]))
                actual = [row["old_section_path"] for row in slots if not truth(row["vacant"])]
                self.check(f"selection.{project}.{stratum}", actual == pool[:2]
                           and sum(truth(row["vacant"]) for row in slots) == max(0, 2 - len(pool)),
                           pool_size=len(pool), chosen=actual, expected=pool[:2])

    def predictions_and_lineage(self):
        predictions = self.rows("predictions.csv")
        lineage = self.rows("lineage.csv")
        actual_predictions = [row for row in predictions if not truth(row["vacant"])]
        vacant_predictions = [row for row in predictions if truth(row["vacant"])]
        self.check("predictions.slots_and_values", len(predictions) == 12
                   and {row["case_id"] for row in predictions} == CASE_IDS
                   and len(actual_predictions) == 8 and len(vacant_predictions) == 4
                   and all(row["prediction_U"] == "YES" and truth(row["legacy_path_present"])
                           and row["old_section_path"] and row["hash_sha256"] for row in actual_predictions)
                   and all(row["prediction_U"] == "미확인" and row["vacancy_reason"]
                           and not row["old_section_path"] for row in vacant_predictions)
                   and all(row["new_body_asset_ci_reads"] == "0" for row in predictions),
                   rows=len(predictions), actual=len(actual_predictions), vacant=len(vacant_predictions))
        positions = {(row["case_id"], row["edition"]) for row in lineage}
        expected_positions = {(case, edition) for case in CASE_IDS for edition in ("old", "new")}
        actual = [row for row in lineage if not truth(row["vacant"])]
        vacant = [row for row in lineage if truth(row["vacant"])]
        prediction_map = {row["case_id"]: row for row in predictions}
        mismatch = []
        for row in lineage:
            prediction = prediction_map[row["case_id"]]
            for key in ("project", "stratum"):
                if row[key] != prediction[key]:
                    mismatch.append(f"{row['case_id']}:{row['edition']}:{key}")
            if truth(row["vacant"]) != truth(prediction["vacant"]) or \
                    row["version"] != prediction[row["edition"] + "_version"]:
                mismatch.append(f"{row['case_id']}:{row['edition']}:vacancy/version")
        self.check("lineage.unique_case_edition_join", len(lineage) == 24 and positions == expected_positions
                   and len(positions) == len(lineage) and not mismatch,
                   rows=len(lineage), unique_positions=len(positions), mismatches=mismatch)
        self.check("lineage.actual_P_U_G", len(actual) == 16 and all(
            row["P"] == row["U"] == "YES" and row["G"] == "미확인"
            and row["section_url"] and row["section_locator"] and row["literal_reference"]
            and row["payload_url"] and SHA256.fullmatch(row["payload_sha256"])
            and int(row["payload_bytes"]) > 0 and row["receipt"] and row["evidence"] for row in actual),
            actual_positions=len(actual), P=dict(Counter(row["P"] for row in actual)),
            U=dict(Counter(row["U"] for row in actual)), G=dict(Counter(row["G"] for row in actual)))
        self.check("lineage.vacancies_not_negatives", len(vacant) == 8 and all(
            row["P"] == row["U"] == row["G"] == "미확인" and row["limitation"]
            and not row["payload_url"] for row in vacant), vacant_positions=len(vacant))

    def confusion(self):
        counts = self.load("counts.json")
        duplicate = self.load("evidence/counts.json")
        self.check("counts.mirror", counts == duplicate)
        predictions = self.rows("predictions.csv")
        lineage = self.rows("lineage.csv")
        outcomes = {row["case_id"]: row for row in lineage if row["edition"] == "new"}
        recorded = {(row["project"], row["stratum"]): row for row in counts["strata"]}
        expected_keys = {(project, stratum) for project in PROJECTS for stratum in STRATA}
        self.check("counts.six_separate_strata", len(counts["strata"]) == 6 and set(recorded) == expected_keys)
        for key in sorted(expected_keys):
            rows = [row for row in predictions if (row["project"], row["stratum"]) == key]
            calc = dict.fromkeys(("TP", "FP", "FN", "TN", "abstention", "vacancy", "actual_positive", "actual_negative"), 0)
            for row in rows:
                if truth(row["vacant"]):
                    calc["vacancy"] += 1
                    continue
                observed, predicted = outcomes[row["case_id"]]["U"], row["prediction_U"]
                if observed == "YES":
                    calc["actual_positive"] += 1
                elif observed == "NO":
                    calc["actual_negative"] += 1
                if observed not in ("YES", "NO") or predicted not in ("YES", "NO"):
                    calc["abstention"] += 1
                else:
                    calc[{("YES", "YES"): "TP", ("YES", "NO"): "FP",
                          ("NO", "YES"): "FN", ("NO", "NO"): "TN"}[(predicted, observed)]] += 1
            entry = recorded[key]
            rates = {"sensitivity": (calc["TP"], calc["actual_positive"]),
                     "false_negative_rate": (calc["FN"], calc["actual_positive"]),
                     "false_positive_rate": (calc["FP"], calc["actual_negative"]),
                     "specificity": (calc["TN"], calc["actual_negative"])}
            rate_errors = []
            for name, (numerator, denominator) in rates.items():
                rate = entry[name]
                value = numerator / denominator if denominator else None
                if rate["numerator"] != numerator or rate["denominator"] != denominator \
                        or rate["value"] != value or (not denominator and rate["display"] != "산출 불가"):
                    rate_errors.append(name)
            self.check("counts." + ".".join(key), len(rows) == entry["slots"] == 2
                       and all(entry[name] == value for name, value in calc.items()) and not rate_errors
                       and set(entry["case_ids"]) == {row["case_id"] for row in rows},
                       recomputed=calc, rate_errors=rate_errors)
        actual = [row for row in lineage if not truth(row["vacant"])]
        main_expected = {"pair_slots": len(predictions), "filled_pairs": sum(not truth(row["vacant"]) for row in predictions),
                         "vacant_pairs": sum(truth(row["vacant"]) for row in predictions),
                         "edition_positions": len(lineage), "actual_edition_positions": len(actual),
                         "vacant_edition_positions": len(lineage) - len(actual)}
        filled = [row for row in predictions if not truth(row["vacant"])]
        main_expected["filled_predictions"] = {
            "YES": sum(row["prediction_U"] == "YES" for row in filled),
            "NO": sum(row["prediction_U"] == "NO" for row in filled),
            "abstention": sum(row["prediction_U"] not in ("YES", "NO") for row in filled),
        }
        current = [row for row in actual if row["edition"] == "new"]
        main_expected["new_U"] = {
            "YES": sum(row["U"] == "YES" for row in current),
            "NO": sum(row["U"] == "NO" for row in current),
            "unknown_actual": sum(row["U"] not in ("YES", "NO") for row in current),
        }
        for dimension in ("P", "U", "G"):
            unknown_key = "미확인" if dimension == "G" else "unknown"
            main_expected["actual_position_" + dimension] = {
                "YES": sum(row[dimension] == "YES" for row in actual),
                "NO": sum(row[dimension] == "NO" for row in actual),
                unknown_key: sum(row[dimension] not in ("YES", "NO") for row in actual),
            }
        self.check("counts.main_totals", all(counts["main"][key] == value for key, value in main_expected.items()),
                   recomputed=main_expected)

    def sources(self):
        sources = [json.loads(line) for line in self.read("sources.jsonl").splitlines() if line.strip()]
        counted = [row for row in sources if row["countable"] is True]
        reconcile = self.load("evidence/source-reconciliation.json")
        counts = self.load("counts.json")
        review = self.load("evidence/cross-domain/review-stage3.json")
        self.check("sources.totals_and_unique_ids", len(sources) == reconcile["rows"] == 477
                   and len(counted) == reconcile["countable"] == 111
                   and len({row["source_id"] for row in sources}) == len(sources)
                   and all(type(row["countable"]) is bool for row in sources),
                   rows=len(sources), countable=len(counted))
        hashes = Counter(row["sha256"] for row in counted)
        self.check("sources.counted_sha256_unique", all(SHA256.fullmatch(value) for value in hashes)
                   and all(number == 1 for number in hashes.values()),
                   unique_counted_sha256=len(hashes), duplicates={key: value for key, value in hashes.items() if value > 1})
        categories = dict(Counter(row["category"] for row in counted))
        groups = {"example_bodies": (8, {"example_body"}),
                  "resources_or_example_sources": (8, {"image_payload", "example_source"}),
                  "publication_release_change_build": (8, {"release_record", "publication_record", "deployment_listing",
                                                            "distribution_record", "distribution_bundle", "change_record", "build_rule"}),
                  "epub_spec_and_new_package": (2, {"epub_spec", "epub_package"}),
                  "wheel_specs_and_new_package": (2, {"wheel_spec", "wheel_package"})}
        minima = {}
        minimum_errors = []
        for group, (required, members) in groups.items():
            observed = sum(categories.get(category, 0) for category in members)
            minima[group] = {"required": required, "observed": observed}
            if observed < required or reconcile["minima"][group] != minima[group]:
                minimum_errors.append(group)
        self.check("sources.categories_and_minima", categories == reconcile["categories"] and not minimum_errors
                   and sum(item["observed"] for item in minima.values()) == len(counted)
                   and counts["source_minimum"] == reconcile,
                   categories=categories, minima=minima, errors=minimum_errors)
        ids = {row["source_id"]: row for row in sources}
        reconciled = {row["source_id"] for row in reconcile["review_inherited_exclusions"]}
        reviewed = {row["current_source_id"] for row in review["inherited_source_exclusions"]}
        adjusted = {row["source_id"] for row in sources if row.get("countable_before_root_reconciliation") is True}
        self.check("sources.five_review_exclusions", reconciled == reviewed == adjusted == EXPECTED_EXCLUSIONS
                   and all(ids[key]["countable"] is False and ids[key]["duplicate_reason"]
                           and ids[key]["review_adjustment"] == "evidence/cross-domain/review-stage3.json"
                           for key in EXPECTED_EXCLUSIONS)
                   and reconcile["stage3_snapshot_countable"] - len(EXPECTED_EXCLUSIONS) == len(counted),
                   excluded_ids=sorted(reconciled), pre_review=reconcile["stage3_snapshot_countable"], final=len(counted))
        origin_counts = dict(Counter(row["ledger_origin"] for row in counted))
        self.check("sources.origins", origin_counts == reconcile["counts_by_origin_after_review"], observed=origin_counts)
        input_errors = []
        for original in reconcile["input_ledgers"]:
            text = self.read(original["path"])
            rows = [json.loads(line) for line in text.splitlines() if line.strip()]
            if self.inputs[original["path"]] != original["sha256"] or len(rows) != original["rows"] \
                    or sum(row["countable"] is True for row in rows) != original["countable"]:
                input_errors.append(original["path"])
        self.check("sources.authored_input_ledgers", not input_errors,
                   original_ledgers=len(reconcile["input_ledgers"]), mismatches=input_errors)
        required_fields = {"source_id", "questions", "cases", "original_url", "fixed_url", "accessed_utc", "publisher",
                           "lineage", "category", "version", "location", "sha256", "observation", "claims_supported",
                           "claims_refuted", "limitations", "countable", "duplicate_reason", "receipt"}
        self.check("sources.schema", all(required_fields <= set(row) for row in sources))
        receipt_references = [(row["source_id"], row["receipt"]) for row in sources]
        frame = self.rows("frame.csv")
        self.check("receipts.eligible_frame_has_receipt", all(
            row["body_receipt"] for row in frame if truth(row["eligible"])))
        receipt_references += [(row["page_path"], row["body_receipt"]) for row in frame if row["body_receipt"]]
        for row in self.rows("lineage.csv"):
            for field in ("receipt", "body_receipt", "source_receipt"):
                if row.get(field):
                    # Matplotlib stores body and payload receipts in one CSV cell.
                    for relative in row[field].split(";"):
                        receipt_references.append((row["case_id"] + ":" + field, relative.strip()))
        missing = [{"owner": owner, "receipt": relative} for owner, relative in receipt_references
                   if not self.path(relative).is_file()]
        self.check("receipts.all_declared_paths_exist", not missing,
                   references=len(receipt_references), unique_paths=len({path for _, path in receipt_references}), missing=missing)

    def markdown(self):
        def tables(text):
            lines, found, index = text.splitlines(), [], 0
            while index < len(lines):
                if not lines[index].strip().startswith("|"):
                    index += 1
                    continue
                start = index
                block = []
                while index < len(lines) and lines[index].strip().startswith("|"):
                    block.append([part.strip() for part in re.split(r"(?<!\\)\|", lines[index].strip())[1:-1]])
                    index += 1
                if len(block) >= 2 and all(re.fullmatch(r":?-{3,}:?", cell) for cell in block[1]):
                    found.append({"start": start, "end": index, "header": block[0], "rows": block[2:]})
            return lines, found

        lines, result = tables(self.read("RESULT.md"))
        expected_headers = [
            ["프로젝트·층·순번", "이전 예제·절·목적", "두 발행판 주소·SHA", "목록에서만 본 신호", "봉인 U 예측 및 시각", "제외·선행 노출·미확인"],
            ["예제·판", "해당 절 주소·실제 참조 표현", "요청·패키지 내 최종 위치·지문", "배포 P·사용 U·생성 G", "직접 확인한 내용·반대 근거 주소", "미확인 사유"],
            ["프로젝트·층·예제", "사전 예측과 관측 U", "참·오귀속·놓침·유보", "당시 인용·현재 이용·재현 목적별 반환 URL과 볼 절", "실제 음성·양성 분모", "판단을 뒤집을 근거·미확인"],
        ]
        for index, expected_rows in enumerate((12, 24, 12)):
            table = result[index]
            ids = [re.search(r"(?:GG|MP)-[GAC][12]", row[0]).group() for row in table["rows"]]
            expected_occurrences = 2 if index == 1 else 1
            self.check(f"RESULT.table_{index + 1}", table["header"] == expected_headers[index]
                       and len(table["rows"]) == expected_rows
                       and all(len(row) == len(table["header"]) and all(row) for row in table["rows"])
                       and Counter(ids) == Counter({case: expected_occurrences for case in CASE_IDS}),
                       rows=len(table["rows"]), case_occurrences=dict(Counter(ids)))
        table_lineage = {}
        for row in result[1]["rows"]:
            case = re.search(r"(?:GG|MP)-[GAC][12]", row[0]).group()
            edition = re.search(r"\b(old|new)\b", row[0]).group()
            table_lineage[(case, edition)] = row[3].split(" / ")
        ledger_lineage = {(row["case_id"], row["edition"]): [row["P"], row["U"], row["G"]]
                          for row in self.rows("lineage.csv")}
        self.check("RESULT.lineage_table_join", table_lineage == ledger_lineage)
        last = result[-1]
        weakness_headers = ["가장 중요한 불일치·약점", "다음에 열 자료 또는 실행할 입력", "어떤 관측이면 결론을 바꿀지"]
        self.check("RESULT.final_three_weaknesses", last["header"] == weakness_headers
                   and len(last["rows"]) == 3 and all(len(row) == 3 and all(row) for row in last["rows"])
                   and not any(line.strip() for line in lines[last["end"]:]), rows=len(last["rows"]))
        _, self_tables = tables(self.read("SELF_CHECK.md"))
        questions = [row[0] for row in self_tables[0]["rows"]]
        self.check("SELF_CHECK.Q1_to_Q7", questions == [f"Q{number}" for number in range(1, 8)]
                   and all(len(row) == 5 and all(row) for row in self_tables[0]["rows"]), questions=questions)

    def chronology(self):
        checkpoints = self.load("evidence/checkpoints.json")
        gate = next(row for row in checkpoints["stages"] if row["stage"] == 2)
        gate_time = stamp(gate["verified_utc"])
        review = self.load("evidence/cross-domain/review-stage3.json")
        seal = self.load("evidence/prediction-seal.json")
        predictions = self.rows("predictions.csv")
        self.check("chronology.predictions_before_remote_gate",
                   gate["remote_sha"] == "f1c5d6ff927fd5fbe108565598810ca7e94c5753"
                   and stamp(seal["seal_file_written_utc"]) < gate_time
                   and all(stamp(row["prediction_recorded_utc"]) < gate_time for row in predictions)
                   and seal["new_body_image_individual_ci_reads_before_seal"] == 0,
                   gate_utc=gate["verified_utc"], gate_sha=gate["remote_sha"])
        for project in ("ggplot2", "matplotlib"):
            observation = review["chronology"][project]
            earliest = observation["earliest"]
            receipt = self.load(earliest["receipt"])
            start = receipt.get("started_utc", receipt.get("utc"))
            self.check(f"chronology.{project}.first_new_request_after_gate",
                       observation["semantic_receipts_checked"] > 0 and observation["before_or_at_gate"] == []
                       and start == earliest["start"] and stamp(start) > gate_time
                       and (earliest["receipt_complete"] is None or
                            stamp(earliest["receipt_complete"]) >= stamp(start)),
                       reviewed_semantic_receipts=observation["semantic_receipts_checked"],
                       first_request_started_utc=start, gate_utc=gate["verified_utc"],
                       receipt=earliest["receipt"], timestamp_semantics=observation["timestamp_semantics"])

    def report(self):
        groups = (self.seals, self.frame_and_selection, self.predictions_and_lineage,
                  self.confusion, self.sources, self.markdown, self.chronology)
        for function in groups:
            self.run_group(function.__name__, function)
        failures = [check["check"] for check in self.checks if not check["passed"]]
        return {"task": "AF-RES-102", "verification": "offline_read_only_research_structure",
                "task_root": str(ROOT), "started_utc": self.started_utc, "finished_utc": utc_now(),
                "scope": ["Recompute frozen hashes, selection arithmetic, joins, source minima and document table structure.",
                          "Check stored receipt paths and the independent review's request chronology against the remote gate.",
                          "No network requests, downloaded example execution, file writes or repository mutations.",
                          "This is not proof of source understanding, semantic U correctness, or actual historical G.",
                          "This does not replace workbench.session check, cloud_check.py or scripts/check.py.",
                          "Stage3 seal is a historical snapshot; post-review final root sources changed intentionally. Current immutability covers stage1 and stage2 only."],
                "checks": self.checks, "check_count": len(self.checks), "failed_checks": failures,
                "inputs_sha256": self.inputs, "passed": not failures,
                "exit_code": 1 if failures else 0}


def main():
    if len(sys.argv) != 1:
        print(json.dumps({"passed": False, "exit_code": 1, "error": "Run without arguments."}))
        return 1
    report = Verification().report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
