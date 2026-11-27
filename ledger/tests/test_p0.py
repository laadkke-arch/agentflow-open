"""P0 임시안 셋(07 R-1 주소 정규화·판 사이 위치 대응, 예산 단위 D1·D11)의 계약."""
import hashlib
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
from afledger import Ledger, config, locate, normalize  # noqa: E402
from afledger.adapters.reader_github import GitHubPinnedReader, raw_url  # noqa: E402
from afledger.budget import BudgetExhausted, RequestBudget  # noqa: E402
from fakes import FakeTransport  # noqa: E402

T = "2026-11-26T00:00:00Z"
OLD = '''class Queue:
    """A queue.

    If maxsize is less than or equal to zero, the queue size is infinite.
    If it is an integer greater than 0, then put() will block.
    """

    def put(self, item):
        """Put an item into the queue."""
        return item

    def shutdown(self):
        """Shut-down the queue."""
'''
NEW = '''import os


class Queue:
    """A queue.

    If maxsize is less than or equal to zero, the queue size is infinite. If it
    is an integer greater than 0, then put() will block.
    """

    def put(self, item):
        """Put an item into the queue, waiting if necessary."""
        return item
'''


class NormalizeN1(unittest.TestCase):
    def test_vendored_file_is_byte_identical(self):
        data = (HERE.parent / "afledger/vendor/rcore_normalize.py").read_bytes()
        blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        self.assertEqual(blob, normalize.SOURCE["blob"])
        self.assertEqual(normalize.RULES, "n1")

    def test_github_blob_splits_into_page_edition_position(self):
        k = normalize.keys("https://github.com/python/cpython/blob/v3.13.18/Lib/asyncio/queues.py#L36-L38")
        self.assertEqual((k["page"], k["edition"], k["position"], k["target"]),
                         ("gh:python/cpython/Lib/asyncio/queues.py", "v3.13.18", "Lib/asyncio/queues.py#L36-L38",
                          "gh:python/cpython"))

    def test_reuse_meets_across_url_forms_but_not_across_target(self):
        L = Ledger()
        o, _ = L.observe(url="https://github.com/python/cpython/blob/v3.13.18/Lib/asyncio/queues.py",
                         edition_key="v3.13.18", edition_kind="release", position="L36-L38", at=T,
                         method="read_line", quote="q", quote_lang="en", statement="s")
        self.assertEqual(L.obs(o)["url"], "https://github.com/python/cpython/blob/v3.13.18/Lib/asyncio/queues.py")
        for form in ("https://github.com/python/cpython/blob/main/Lib/asyncio/queues.py",
                     "https://raw.githubusercontent.com/python/cpython/v3.13.18/Lib/asyncio/queues.py",
                     "https://GitHub.com/Python/CPython/blob/v3.13.18/Lib/asyncio/queues.py#L1"):
            self.assertEqual(L.reusable(form, "v3.13.18", "L36-L38"), o, form)
        # 같은 target(gh:python/cpython)의 다른 파일은 재사용하지 않는다(전역 병합 금지)
        self.assertIsNone(L.reusable("https://github.com/python/cpython/blob/v3.13.18/Lib/asyncio/locks.py",
                                     "v3.13.18", "L36-L38"))
        self.assertIsNone(L.reusable("https://github.com/python/cpython/blob/v3.13.18/Lib/asyncio/queues.py",
                                     "v3.12.3", "L36-L38"))
        row = L.db.execute("SELECT page, target, norm_rules FROM locator").fetchone()
        self.assertEqual(tuple(row), ("gh:python/cpython/Lib/asyncio/queues.py", "gh:python/cpython", "n1"))

    def test_failed_normalization_falls_back_to_the_raw_string(self):
        self.assertEqual(normalize.keys("https://example.org/doc")["page"], "https://example.org/doc")
        self.assertEqual(normalize.keys("https://example.org/doc")["rules"], "n1:not_source")


class PositionMapM1(unittest.TestCase):
    def test_exact_quote_then_symbol_then_unmapped(self):
        a = locate.anchor(OLD, 4, 5, python=True)
        self.assertEqual((a["symbol"], a["in_doc"]), ("Queue", True))
        m = locate.map_position(a, NEW, python=True)
        self.assertEqual((m["method"], m["lines"]), ("exact_quote", (7, 8)))      # 줄 바꿈이 달라도 공백을 접으면 같다
        b = locate.anchor(OLD, 9, 9, python=True)                                  # put의 docstring, 새 판에서 문장이 바뀜
        m = locate.map_position(b, NEW, python=True)
        self.assertEqual((m["method"], m["lines"]), ("symbol", (12, 12)))
        c = locate.anchor(OLD, 13, 13, python=True)                                # shutdown은 새 판에 없다
        m = locate.map_position(c, NEW, python=True)
        self.assertEqual((m["method"], m["lines"], m["symbol_present"]), ("unmapped", None, False))
        self.assertEqual(m["rules"], config.MAP_RULES)

    def test_ambiguous_quote_is_not_guessed(self):
        self.assertIsNone(locate.find_quote("x = 1\nx = 1\n", "x = 1"))

    def test_byte_span_matches_lines(self):
        a, b = locate.byte_span(OLD, 4, 5)
        self.assertEqual(locate.fold_ws(OLD.encode()[a:b + 1].decode()), locate.fold_ws(locate.lines_text(OLD, 4, 5)))


class BudgetB1(unittest.TestCase):
    def setUp(self):
        self.L = Ledger()
        self.p = self.L.project("A")
        self.req = self.L.intake(self.p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[])
        self.files = {raw_url("o/r", "v1", f"f{i}.py"): OLD for i in range(6)}
        self.reader = GitHubPinnedReader(self.L, FakeTransport(self.files), self.p, self.req)

    def test_same_file_and_edition_is_one_fetch(self):
        self.reader.read("o/r", "v1", "f0.py", T, lines=(4, 5))
        self.reader.read("o/r", "v1", "f0.py", T, symbol="Queue.put")
        self.reader.read("o/r", "v1", "f0.py", T, phrase="Shut-down the queue.")
        self.assertEqual(self.L.fetch_count(p=self.p, req=self.req), 1)

    def test_failures_count_and_cap_stops_fetching(self):
        from afledger.adapters.reader_github import SourceUnavailable
        with self.assertRaises(SourceUnavailable):
            self.reader.read("o/r", "v1", "missing.py", T, lines=(1, 1))        # 404도 1회
        for i in range(3):
            self.reader.read("o/r", "v1", f"f{i}.py", T, lines=(1, 1))
        self.assertEqual(RequestBudget(self.L, self.p, self.req).fetches(), config.REQUEST_FETCHES)
        with self.assertRaises(BudgetExhausted):
            self.reader.read("o/r", "v1", "f5.py", T, lines=(1, 1))

    def test_not_modified_is_recorded_but_not_counted(self):
        self.L.fetched("https://x.example/a", "v1", T, "not_modified", p=self.p, req=self.req)
        self.assertEqual(self.L.fetch_count(p=self.p, req=self.req), 0)
        self.assertEqual(self.L.fetch_count(p=self.p, req=self.req, include_not_modified=True), 1)

    def test_recheck_reads_only_the_byte_span_and_counts_once(self):
        r = self.reader.read("o/r", "v1", "f0.py", T, lines=(4, 5))
        o, _ = self.L.observe(url=r["url"], edition_key="v1", edition_kind="release", position=r["position"], at=T,
                              method="read_line", quote=r["quote"], quote_lang="en", statement="s",
                              byte_span=r["byte_span"], anchor_symbol=r["symbol"], anchor_in_doc=r["in_doc"],
                              map_method="direct")
        req2 = self.L.intake(self.p, request_key="R2", rev=1, at=T, text="t", selected_part="s", requirements=[])
        t = FakeTransport(self.files)
        chk = GitHubPinnedReader(self.L, t, self.p, req2).recheck(o, T)
        self.assertTrue(chk["same"])
        self.assertLess(chk["bytes"], len(OLD.encode()))
        self.assertIn("Range", t.log[0][1])
        self.assertEqual(self.L.fetch_count(p=self.p, req=req2), 1)


if __name__ == "__main__":
    unittest.main()


class ReadingConflictR3(unittest.TestCase):
    def test_same_position_read_differently_is_flagged_not_chosen(self):
        L = Ledger()
        kw = dict(url="https://github.com/o/r/blob/v1/a.py", edition_key="v1", edition_kind="release",
                  position="L1-L2", method="read_line", quote_lang="en", statement="s")
        o1, _ = L.observe(at=T, quote="First reading.", **kw)
        o1b, created = L.observe(at="2026-11-27T00:00:00Z", quote="First   reading.", **kw)
        self.assertEqual((o1b, created), (o1, False))                 # 같은 인용(공백만 다름)은 다시 본 기록
        self.assertEqual(L.alerts, [])
        o2, created = L.observe(at="2026-11-28T00:00:00Z", quote="Second reading.", **kw)
        self.assertTrue(created)                                      # 두 관측을 모두 남긴다
        self.assertEqual(L.alerts[-1]["kind"], "reading_conflict")
        self.assertEqual([(j["obs_id"], j["cause_ref"]) for j in L.jobs()], [(o1, f"conflict:{o2}")])
