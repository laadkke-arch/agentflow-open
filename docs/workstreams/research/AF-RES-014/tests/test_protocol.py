import unittest

from queries.generate import sanitize
from src.constraints import conflicts, postprocess, query_concepts
from src.language import augment
from src.metrics import evaluate


class ProtocolTests(unittest.TestCase):
    def test_requires_or_disallows_only_exact_concept(self):
        needs, bans, mapped = query_concepts([
            {"target": "  Boost 비의존·그래프 조작·공개 소스 ", "polarity": "positive"},
            {"target": "나중에 공개 소스", "polarity": "positive"},
            {"target": "ZooKeeper", "polarity": "positive"},
        ])
        self.assertEqual(needs, {"graph_edit", "open_source"})
        self.assertEqual(bans, {"boost"})
        self.assertEqual(mapped, 1)
        data = [{"target": "boost", "polarity": "required"},
                {"target": "boost", "polarity": "required"},
                {"target": "open_source", "polarity": "required"},
                {"target": "client_open_source", "polarity": "unsupported"},
                {"target": "open_source", "polarity": "unsupported"}]
        self.assertEqual(conflicts(data, needs, bans), {"boost", "open_source"})

    def test_filter_retains_relevance_denominator(self):
        baseline = ["a", "b", "c", "d"]
        match = {"a": {"offline"}, "c": {"opensource"}}
        self.assertEqual(postprocess(baseline, match, "filter"), ["b", "d"])
        self.assertEqual(postprocess(baseline, match, "penalty"), ["b", "d", "a", "c"])
        after = evaluate(["b", "d"], {"a": "2", "c": "1", "b": "1"}, dict.fromkeys(baseline))
        self.assertEqual(after["recall_at10"], 1 / 3)
        self.assertEqual(after["relevant_in_corpus"], 3)

    def test_sanitizer_omits_code_profiles_and_signatures(self):
        markdown = "Problem to solve.\n\n```py\nprivate_example\n```\n\n--\nPerson"
        self.assertEqual(sanitize(markdown), "Problem to solve.")
        html = '<p>Request <a href="/users/1">Profile</a>.</p><pre><code>run()</code></pre>'
        self.assertEqual(sanitize(html, html=True), "Request .")

    def test_identical_technical_token_for_two_languages(self):
        self.assertIn("afconceptlibrarycatalog", augment("도서관에서 운영"))
        self.assertIn("afconceptlibrarycatalog", augment("Library catalog"))
        self.assertNotIn("afconceptlibrarycatalog", augment("library for domain events"))


if __name__ == "__main__":
    unittest.main()
