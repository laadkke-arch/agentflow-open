import csv
import json
import re
import sys
import unittest
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from collect import ROOT, rows
from report_tables import type_totals
from signals import SIGNALS, evaluate_link, select_matrix
from simulate import calendar_checks, first_detection


def load(name):
    return json.loads((ROOT / name).read_text())


def reason(label, positive, before="성립", category="기능 지원", candidate="tool", days=None):
    return {"reason_id": "sample", "reason_target": "feature", "candidate": candidate,
            "now_evidence_url": "https://example.com/", "now_verdict": label,
            "then_verdict": before, "reason_type": category,
            "signals": {"commit_age": {"positive": positive, "url": "https://example.org/",
                                       "raw": {"days": days}}}}


class SignalTests(unittest.TestCase):
    def test_429_is_missing_and_explicit_404_is_positive(self):
        raw = {"status": "blocked", "url": "https://example.org/", "explicit": 429}
        self.assertIsNone(evaluate_link(raw)["http_dead"]["positive"])
        raw.update(status="unavailable", explicit=404)
        self.assertIs(evaluate_link(raw)["http_dead"]["positive"], True)
        self.assertIsNone(evaluate_link(raw)["domain_redirect"]["positive"])

    def test_alias_does_not_count_as_external_move(self):
        raw = {"status": "redirected", "url": "http://example.co.uk/a",
               "final_url": "https://www.example.co.uk/a"}
        self.assertIs(evaluate_link(raw)["domain_redirect"]["positive"], False)
        raw["final_url"] = "https://example.org/a"
        self.assertIs(evaluate_link(raw)["domain_redirect"]["positive"], True)

    def test_ineligible_and_initially_false_are_excluded(self):
        data = [reason("무너짐", True), reason("무너짐", False, before="처음부터 틀림"),
                reason("판단 불가", True), reason("약화", True), reason("성립", None),
                reason("성립", True, category="관리 상태")]
        main = select_matrix(data, "commit_age")
        weak = select_matrix(data, "commit_age", include_weak=True)
        self.assertEqual((main["n"], main["TP"], main["FP"], main["FN"]), (2, 1, 1, 0))
        self.assertEqual((weak["n"], weak["TP"], weak["FP"]), (2, 2, 0))

    def test_threshold_sensitivity_and_candidate_deduplication(self):
        data = [reason("무너짐", True, days=800), reason("무너짐", True, days=800),
                reason("성립", True, candidate="other", days=700)]
        main = select_matrix(data, "commit_age", unique=True)
        sensitivity = select_matrix(data, "commit_age", age_threshold=730, unique=True)
        self.assertEqual((main["TP"], main["FP"], main["TN"]), (1, 1, 0))
        self.assertEqual((sensitivity["TP"], sensitivity["FP"], sensitivity["TN"]), (1, 0, 1))


class CalendarTests(unittest.TestCase):
    def test_monthly_clamps_without_permanent_anchor_drift(self):
        self.assertEqual(calendar_checks(date(2024, 1, 31), 1, None, date(2024, 4, 30)),
                         [date(2024, 2, 29), date(2024, 3, 31), date(2024, 4, 30)])

    def test_right_censoring_and_same_day_detection(self):
        end = date(2024, 3, 1)
        self.assertIsNone(first_detection([], end))
        self.assertIsNone(first_detection([date(2024, 2, 29)], end))
        self.assertEqual(first_detection([end], end), end)

    def test_published_cadence_uses_two_exact_date_events(self):
        records = load("results/cadence.json")["summary"]
        late = {x["mode"]: x for x in records if x["cohort"] == "exact_date" and x["scenario"] == "late"}
        self.assertEqual([late[k]["median_delay_days"] for k in ("월", "분기", "연")], [12.5, 58.0, 242.0])
        self.assertEqual(late["요청 없음"]["right_censored"], 2)


class DeliverableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = list(rows(ROOT / "REASONS.jsonl"))
        cls.reasons = [r for r in cls.ledger if r["reason_type"] != "이유 없음"]
        cls.now = [r for r in cls.reasons if r["now_verdict"] != "판단 불가"]
        cls.then = [r for r in cls.reasons if r["then_verdict"] != "판단 불가"]

    def test_ledgers_and_dated_evidence(self):
        raw_ids = {r["reason_id"] for r in self.ledger}
        self.assertEqual(len(raw_ids), len(self.ledger))
        for group, threshold in ((self.reasons, 200), (self.now, 150), (self.then, 100)):
            self.assertGreaterEqual(len({r["answer_ref"] for r in group}), threshold)
        self.assertGreaterEqual(sum(r["then_evidence"]["level"] == "D2" for r in self.then), 100)
        self.assertTrue(all(r["now_evidence_url"] and r["now_checked_at_utc"] for r in self.now))
        for item in self.then:
            proof = item["then_evidence"]
            self.assertTrue(proof["url"] and proof["checked_at_utc"])
            if item["answer_date"]:
                self.assertLessEqual(proof["historical_date"], item["answer_date"], item["reason_id"])
        with (ROOT / "SIGNALS.csv").open() as stream:
            signals = list(csv.DictReader(stream))
        self.assertEqual(len(signals), len(self.ledger) * len(SIGNALS))
        self.assertEqual({r["reason_id"] for r in signals}, raw_ids)

    def test_sources_register_supports_coded_results_and_count_caps(self):
        ledger = load("sources.json")
        keys = {r["id"] for cat in ("methods", "execution", "excluded") for r in ledger[cat]}
        self.assertTrue(all(r["now_detail"]["source_id"] in keys for r in self.now))
        self.assertTrue(all(r["then_evidence"]["source_id"] in keys for r in self.then))
        counted = [r for r in ledger["methods"] if r["counts_toward_minimum"]]
        self.assertGreaterEqual(len(counted), 25)
        self.assertLessEqual(max(Counter(r["site_group"] for r in counted).values()), 3)
        for key, n in (("empirical", 5), ("crossfield", 6), ("signal", 5), ("rights", 2)):
            self.assertGreaterEqual(sum(r["category"] == key for r in counted), n)

    def test_tables_start_report_and_match_ledger(self):
        report = (ROOT / "RESULT.md").read_text()
        self.assertTrue(report.startswith("## §1 필수 결과 표\n"))
        self.assertEqual(re.findall(r"^## §(\d)", report, re.MULTILINE), list("12345"))
        weakness = report.split("## §4", 1)[1].split("## §5", 1)[0]
        self.assertEqual(re.findall(r"^### (\d)\.", weakness, re.MULTILINE), list("123"))
        headers = [
            "이유 유형 | 답 수(분모) | 지금 성립 | 약화 | 무너짐 | 판단 불가 | 처음부터 틀림 | 중앙 경과 연수 | 대표 사례(스레드 ID·후보) | 미확인",
            "신호 | 확인 가능 수(분모) | 무너짐 적중 | 놓침 | 잘못 경보 | 정밀도 | 재현율 | 항목당 비용(요청·초) | 대표 놓침 사례 | 미확인",
            "대안 | 항목당 비용 | 무너짐 발견 지연(중앙값) | 놓치는 것 | 필요한 저장 필드 | 근거 위치 | 미확인",
            "주장 | 근거 자료 주소 | 확인한 내용 | 반증 시도 | 미확인",
        ]
        offsets = [report.index(f"| {heading} |") for heading in headers]
        self.assertEqual(offsets, sorted(offsets))
        confusion = load("results/confusion.json")
        self.assertGreaterEqual(sum(v["strict"]["n"] > 0 for v in confusion.values()), 6)
        for signal, purpose in confusion.items():
            self.assertEqual(purpose["strict"], select_matrix(self.ledger, signal))
            stats = purpose["strict"]
            prefix = " | ".join(str(v) for v in (purpose["name"], stats["n"], stats["TP"], stats["FN"], stats["FP"]))
            self.assertIn(f"| {prefix} |", report)
        self.assertEqual(load("results/reason-types.json"), type_totals(self.ledger))

    def test_same_bench_fixture_and_logged_cost(self):
        cost = load("results/cost.json")["summary"]
        self.assertEqual([cost[k]["n"] for k in "ABC"], [12, 12, 12])
        self.assertEqual([cost[k]["body_pages_read"] for k in "ABC"], [24, 0, 14])
        self.assertEqual([cost[k]["known_http_requests"] for k in "BC"], [22, 22])
        self.assertIn("T009.A001/directus-oss", cost["C"]["unflagged_now_broken"])
        self.assertIn("T020.A001/dcoder-platform", cost["C"]["unflagged_now_broken"])


if __name__ == "__main__":
    unittest.main()
