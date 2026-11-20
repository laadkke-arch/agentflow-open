from datetime import date
import unittest

from analyze import alert, auc, boot_ci, first_alert, nullable_logic, quantile, schedule
from collect import normalize_repo, notice_state, parse_day, previous_months, registry_metadata


class StudyTest(unittest.TestCase):
    def test_month_end_and_leap_year(self):
        self.assertEqual(previous_months(date(2024, 3, 31), 1), date(2024, 2, 29))
        self.assertEqual(previous_months(date(2024, 2, 29), 12), date(2023, 2, 28))

    def test_auc_ties_and_perfect_separation(self):
        self.assertEqual(auc([(4, 2), (4, 3)]), 1)
        self.assertEqual(auc([(1, 1)]), .5)
        self.assertEqual(auc([(1, 2)]), 0)
        self.assertEqual(boot_ci([(1, 3), (1, 3)], n=40), [0, 0])
        self.assertIsNone(boot_ci([(1, 3)]))

    def test_missing_logic_and_first_observed_alert(self):
        self.assertIsNone(nullable_logic("or", [False, None]))
        self.assertIs(nullable_logic("or", [True, None]), True)
        self.assertIs(nullable_logic("and", [False, None]), False)
        h = {"git_commit_age": [[10, None], [12, 45], [20, 91]]}
        self.assertEqual(first_alert(h, "git_commit_age", 10, 19), (False, None))
        self.assertEqual(first_alert(h, "git_commit_age", 10, 20), (True, 20))
        self.assertEqual(first_alert(h, "git_commit_age", 21, 19), (None, None))
        self.assertTrue(alert("git_commits_90d", 3))
        self.assertFalse(alert("git_commits_90d", 4))

    def test_cadence_and_quantile(self):
        first, last = parse_day("2023-11-12"), parse_day("2024-03-02")
        self.assertEqual(schedule(first, last, "quarterly"), [parse_day("2024-01-01")])
        self.assertEqual(list(schedule(10, 18, 3, 2)), [12, 15, 18])
        self.assertEqual(quantile([0, 10, 30], .75), 20)

    def test_packument_inactive_is_live_only(self):
        d = {"versions": {"1.0": {"deprecated": "migrate"}, "2.0": {}},
             "time": {"modified": "2024-01-01T00:00:00Z",
                      "1.0": "2020-01-01T00:00:00Z", "2.0": "2021-01-01T00:00:00Z"},
             "dist-tags": {"latest": "2.0"}}
        r = registry_metadata("npm", d)
        self.assertEqual(r["current_inactive_count"], 1)
        self.assertEqual(len(r["dated_versions"]), 2)
        self.assertFalse(r["current_latest_inactive"])

    def test_repository_normalization_and_notice_context(self):
        self.assertEqual(normalize_repo({"url": "git+ssh://git@github.com/Acme/Tool.git"}),
                         "https://github.com/acme/tool")
        self.assertEqual(notice_state("# This project is deprecated\nAn unrelated API moved to x", "A"), ["deprecated"])
        self.assertEqual(notice_state("This project is not deprecated.", "A"), [])


if __name__ == "__main__":
    unittest.main()
