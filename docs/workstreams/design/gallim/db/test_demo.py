import unittest
from pathlib import Path

from demo import evaluate, load_fixture, next_check


class EvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_fixture(Path(__file__).with_name("cases.json"))
        cls.candidates = {c["id"]: c for c in cls.data["candidates"]}

    def result(self, key, claims=None, criteria=None):
        return evaluate(self.candidates[key],
                        self.data["criteria"] if criteria is None else criteria,
                        self.data["claims"] if claims is None else claims)

    def test_documented_consume_refutes_original_location(self):
        row = self.result("consume")
        self.assertEqual(row["status"], "excluded")
        self.assertEqual(row["criteria"]["keep_source"]["used"], ["direct-removal"])
        self.assertEqual(row["criteria"]["retain_content"]["state"], "supported")

    def test_component_contract_proposal_and_analogy_do_not_prove_staged_copy(self):
        row = self.result("stage")
        self.assertEqual(row["status"], "pending")
        self.assertEqual(row["criteria"]["keep_source"]["state"], "unknown")
        self.assertEqual(set(row["criteria"]["keep_source"]["ignored"]),
                         {"other-system", "staged-copy-plan"})
        self.assertIn("불일치", row["criteria"]["retain_content"]["ignored"]["consumer-only"])

    def test_all_required_supported_despite_preference(self):
        row = self.result("control")
        self.assertEqual(row["status"], "verified")
        self.assertEqual(row["criteria"]["retry_once"]["state"], "refuted")

    def test_no_stitching_across_versions_or_scope_or_config(self):
        row = self.result("mismatch")
        self.assertEqual(row["status"], "pending")
        self.assertIn("version", row["criteria"]["keep_source"]["ignored"]["different-version"])
        claim = next(c for c in self.data["claims"] if c["id"] == "fixture-source")
        for key in ("scope", "configuration", "subject"):
            with self.subTest(key=key):
                candidate_claim = dict(claim, context={**claim["context"], key:"다른 범위"})
                mod = [candidate_claim if c is claim else c for c in self.data["claims"]]
                self.assertEqual(self.result("control", mod)["status"], "pending")

    def test_conflicting_and_unknown_are_distinct(self):
        row = self.result("conflict")
        self.assertEqual(row["status"], "pending")
        self.assertEqual(row["criteria"]["keep_source"]["state"], "conflicting")
        self.assertEqual(row["criteria"]["retry_once"]["state"], "unknown")
        self.assertEqual(self.result("conflict", list(reversed(self.data["claims"]))), row)

    def test_empty_requirements_unknown_context_or_empty_locator(self):
        self.assertEqual(self.result("control", criteria=[])["status"], "pending")
        claim = next(c for c in self.data["claims"] if c["id"] == "fixture-source")
        for key, value in (("context", {}), ("context", {**claim["context"], "version":"?"}),
                           ("locator", ""), ("locator", "https://example.org/")):
            with self.subTest(key=key, value=value):
                row = self.result("control", [{**claim, key:value}])
                self.assertEqual(row["criteria"]["keep_source"]["state"], "unknown")
                self.assertTrue(row["criteria"]["keep_source"]["ignored"])

    def test_prioritize_one_uncertain_required_condition(self):
        results = {key: self.result(key) for key in self.data["compare"]}
        self.assertEqual(next_check(self.data["criteria"], results),
                         {"criterion":"keep_source", "candidates":["stage"]})
        self.assertIsNone(next_check(self.data["criteria"], {"control":self.result("control")}))


if __name__ == "__main__":
    unittest.main()
