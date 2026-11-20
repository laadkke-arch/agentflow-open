# Adapted from AF-RES-012 cb602858378db90adb1f085953016267f9afbd6d (tests/test_metrics.py).
import unittest
from math import log2

import numpy as np

from src.metrics import evaluate
from src.search import competition_ranks, reciprocal_rank_fusion, tokens


class MetricTests(unittest.TestCase):
    def setUp(self):
        self.ranking = ["near", "unknown", "good", "partial"]
        self.labels = {"good": "2", "partial": "1", "near": "N"}
        self.roles = {"near": "product", "unknown": "other",
                      "good": "product", "partial": "principle"}

    def test_graded_and_binary_scores_with_a_near_miss(self):
        result = evaluate(self.ranking, self.labels, self.roles, k=3)
        self.assertEqual(result["recall_at10"], 0.5)
        self.assertAlmostEqual(result["ndcg_at10"], (3 / 2) / (3 + 1 / log2(3)))
        self.assertEqual(result["mrr"], 1 / 3)
        self.assertEqual(result["near_misses_at10"], 1)
        self.assertEqual(result["product_recall_at10"], 1)
        self.assertEqual(result["principle_recall_at10"], 0)
        self.assertIsNone(result["component_recall_at10"])

    def test_different_corpus_has_different_denominator(self):
        result = evaluate(self.ranking[:2], self.labels, {"near": "product", "unknown": "other"})
        self.assertIsNone(result["recall_at10"])
        self.assertIsNone(result["ndcg_at10"])
        self.assertEqual(result["mrr"], 0)
        self.assertEqual(result["judged_at10"], 1)

    def test_reciprocal_rank_beyond_cutoff(self):
        result = evaluate(self.ranking, self.labels, self.roles, k=2)
        self.assertEqual(result["recall_at10"], 0)
        self.assertEqual(result["first_relevant_rank"], 3)
        self.assertEqual(result["mrr"], 1 / 3)

    def test_explicit_zero_adds_coverage_but_not_gain(self):
        original = evaluate(self.ranking, self.labels, self.roles)
        updated = evaluate(self.ranking, self.labels | {"unknown": "0"}, self.roles)
        self.assertEqual(original["ndcg_at10"], updated["ndcg_at10"])
        self.assertEqual(updated["judged_at10"] - original["judged_at10"], 1)

    def test_equal_scores_have_equal_fusion_contribution(self):
        np.testing.assert_equal(competition_ranks(np.array([0.6, 0.0, 0.6])), [1, 3, 1])
        result = reciprocal_rank_fusion(np.array([[0., 0., 0.]]), np.array([[2., 0., 1.]]))
        np.testing.assert_allclose(result[0], [2 / 61, 1 / 61 + 1 / 63, 1 / 61 + 1 / 62])

    def test_both_methods_can_share_normalized_tokens(self):
        self.assertEqual(tokens("ＰＤＦ·가져오기 Worker/12"), ["pdf", "가져오기", "worker", "12"])


if __name__ == "__main__":
    unittest.main()
