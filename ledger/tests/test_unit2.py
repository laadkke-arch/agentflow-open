"""둘째 구현 단위 착수: 재확인 작업자, 폴링 시계, 조건부 요청 채널, EVAL-X1 재생(06 3.4)."""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
from afledger import Ledger, config  # noqa: E402
from afledger.adapters.channel_raw import ConditionalFileChannel  # noqa: E402
from afledger.worker import RecheckWorker  # noqa: E402
from fakes import FakeResponse  # noqa: E402
import run_unit2  # noqa: E402

T = "2026-11-26T00:00:00Z"
CH = "https://example.org/history"


def doc_ledger():
    L = Ledger()
    o, _ = L.observe(url="https://example.org/doc", edition_key="rev:1", edition_kind="revision", position="§", at=T,
                     method="read_line", quote="Export until June.", quote_lang="en", statement="6월까지 내보내기",
                     published_at="2026-11-01T00:00:00Z")
    L.channel("ex", CH, "revision_history")
    L.watch(o, CH)
    return L, o


def reader_for(revs):
    def reader(obs, ek, at):
        r = revs.get(ek) if ek else revs[max(revs)]
        return {"url": "https://example.org/doc", "edition_key": r[0], "position": "§", "quote": r[1], "statement": r[1],
                "published_at": r[2]}
    return reader


class Worker(unittest.TestCase):
    def test_merged_job_reads_every_edition_and_chains_in_publication_order(self):   # D3
        L, o = doc_ledger()
        revs = {"rev:2": ("rev:2", "Export until July.", "2026-11-27T00:00:00Z"),
                "rev:3": ("rev:3", "Export closed.", "2026-11-28T00:00:00Z")}
        L.poll(CH, [{"id": "3", "title": "r3", "edition": "rev:3"}, {"id": "2", "title": "r2", "edition": "rev:2"}],
               "2026-11-28T01:00:00Z")
        w = RecheckWorker(L, reader_for(revs), lambda old, r: "changes_value")
        w.run_once("2026-11-28T02:00:00Z")
        self.assertEqual([L.obs(L.current(o, "2026-11-28T03:00:00Z"))["edition_key"]], ["rev:3"])
        chain = L.db.execute("SELECT count(*) FROM supersession").fetchone()[0]
        self.assertEqual(chain, 2)                                   # 가운데 판을 잃지 않는다
        self.assertEqual(L.fetch_count(clock="follow"), 2)           # 판마다 가져오기 1회

    def test_same_content_finishes_without_supersession(self):
        L, o = doc_ledger()
        L.poll(CH, [{"id": "1", "title": "r1", "edition": "rev:1"}], "2026-11-27T00:00:00Z")
        w = RecheckWorker(L, reader_for({"rev:1": ("rev:1", "Export until June.", "2026-11-01T00:00:00Z")}),
                          lambda old, r: "changes_value")
        self.assertEqual(w.run_once("2026-11-27T01:00:00Z")[0]["result"], "same")
        self.assertEqual(L.db.execute("SELECT count(*) FROM supersession").fetchone()[0], 0)

    def test_follow_budget_leaves_jobs_queued(self):
        L, o = doc_ledger()
        for i in range(config.FOLLOW_FETCHES_PER_10_SOURCES):
            L.fetched("https://example.org/x", None, "2026-11-26T12:00:00Z", clock="follow")
        L.poll(CH, [{"id": "9", "title": "r9"}], "2026-11-27T00:00:00Z")
        w = RecheckWorker(L, reader_for({"rev:1": ("rev:1", "x", "2026-11-01T00:00:00Z")}), lambda o_, r: "confirms")
        self.assertEqual(w.run_once("2026-11-27T01:00:00Z"), [])
        self.assertEqual(len(L.jobs("queued")), 1)


class ConditionalChannel(unittest.TestCase):
    class T:
        def __init__(self):
            self.body, self.etag, self.status, self.calls = b"v1 text", '"e1"', 200, []

        def get(self, url, headers=None, note=""):
            headers = headers or {}
            self.calls.append(dict(headers))
            if headers.get("If-None-Match") == self.etag and self.status == 200:
                r = FakeResponse(url, 304, b"")
            else:
                r = FakeResponse(url, self.status, self.body)
            r.headers = {"etag": self.etag}
            return r

    def test_304_is_not_counted_and_error_page_keeps_baseline(self):
        L = Ledger()
        t = self.T()
        ch = ConditionalFileChannel(L, t, "https://raw.example/a.txt", expect="text")
        self.assertEqual(len(ch.listing(T)), 1)
        self.assertEqual(len(ch.listing("2026-11-26T03:00:00Z")), 1)          # 304
        self.assertEqual(t.calls[1], {"If-None-Match": '"e1"'})
        self.assertEqual(L.fetch_count(clock="background"), 1)
        self.assertEqual(L.fetch_count(clock="background", include_not_modified=True), 2)
        t.body, t.etag = b"<html>error</html>", '"e2"'                           # 200인데 기대 표지가 없다(오류 페이지)
        self.assertEqual([i["id"] for i in ch.listing("2026-11-26T06:00:00Z")], ['"e1"'])
        self.assertEqual(ch.etag, '"e1"')                                       # 기준선을 옮기지 않는다
        t.body = b"v2 text"
        self.assertEqual([i["id"] for i in ch.listing("2026-11-26T09:00:00Z")], ['"e1"', '"e2"'])


class EvalX1Replay(unittest.TestCase):
    def test_criteria_2_and_3_hold_and_1_depends_on_the_deadline_budget(self):
        saved = config.DEADLINE_BUDGET
        try:
            config.DEADLINE_BUDGET = "follow"
            r = run_unit2.run_phase({"supplier": 10, "kb": 40})
            self.assertTrue(all(r["supplier_watch_alive"]))
            self.assertEqual(r["notices_principle_slot"], 0)
            self.assertEqual({s for s, _ in r["notices"]}, {1})
            self.assertGreater(r["max_delay_h"], 96)                            # D4+D11 충돌(08 I22)
            config.DEADLINE_BUDGET = "separate"
            r = run_unit2.run_phase({"supplier": 10, "kb": 40})
            self.assertLessEqual(r["max_delay_h"], 96)
            self.assertEqual(r["follow_budget_skips"], 0)
        finally:
            config.DEADLINE_BUDGET = saved


class ChangeCursorI35(unittest.TestCase):
    def test_error_polls_do_not_freshen_the_cursor_and_the_gate_reopens(self):            # (b)
        L, o = doc_ledger()
        L.poll(CH, [], "2026-11-26T00:00:00Z")                                     # 항목 없음: 재확인 작업도 없다
        self.assertEqual(L.reuse_gate(o, "2026-11-27T00:00:00Z")["decision"], "reuse")
        for h in ("2026-11-29T00:00:00Z", "2026-12-02T00:00:00Z", "2026-12-05T00:00:00Z"):
            L.poll(CH, [], h, outcome="error")
        g = L.reuse_gate(o, "2026-12-05T01:00:00Z")
        self.assertEqual(g["decision"], "reopen")
        self.assertTrue(any("채널 커서가 늙음" in w for w in g["why"]))
        row = L.db.execute("SELECT last_polled_at, confirmed_at FROM channel WHERE url=?", (CH,)).fetchone()
        self.assertEqual((row[0], row[1]), ("2026-12-05T00:00:00Z", "2026-11-26T00:00:00Z"))

    def test_windowed_listing_missing_the_newest_known_id_is_a_gap_until_a_full_listing(self):   # (c)
        L = Ledger()
        feed = "https://example.org/feed"
        L.channel("ex", feed, "feed", windowed=True)
        L.poll(feed, [{"id": "a", "title": "a"}, {"id": "b", "title": "b"}], "2026-11-26T00:00:00Z")
        c0 = L.db.execute("SELECT confirmed_at, cursor FROM channel WHERE url=?", (feed,)).fetchone()
        new = L.poll(feed, [{"id": "d", "title": "d"}, {"id": "e", "title": "e"}], "2026-11-29T00:00:00Z")
        self.assertEqual([i["id"] for i in new], ["d", "e"])                         # 새 ID는 넣는다
        self.assertEqual(L.last_poll_outcome, "gap")
        self.assertTrue(any(a["kind"] == "channel_gap_suspected" for a in L.alerts))
        c1 = L.db.execute("SELECT confirmed_at, cursor, needs_full_listing FROM channel WHERE url=?", (feed,)).fetchone()
        self.assertEqual((c1[0], c1[1], c1[2]), (c0[0], c0[1], 1))                   # 확인 커서는 멈춘다
        new = L.poll(feed, [{"id": x, "title": x} for x in "abcde"], "2026-11-29T01:00:00Z", full_listing=True)
        self.assertEqual([i["id"] for i in new], ["c"])                              # 빠졌던 c를 전체 목록에서 찾는다
        c2 = L.db.execute("SELECT confirmed_at, needs_full_listing FROM channel WHERE url=?", (feed,)).fetchone()
        self.assertEqual((c2[0], c2[1]), ("2026-11-29T01:00:00Z", 0))

    def test_ok_poll_without_new_ids_advances_the_cursor(self):                          # (d) BOOKMARK
        L, o = doc_ledger()
        L.poll(CH, [], "2026-11-26T00:00:00Z")
        L.poll(CH, [], "2026-12-02T00:00:00Z")
        self.assertEqual(L.db.execute("SELECT confirmed_at FROM channel WHERE url=?", (CH,)).fetchone()[0],
                         "2026-12-02T00:00:00Z")
        self.assertEqual(L.reuse_gate(o, "2026-12-03T00:00:00Z")["why"].count("채널 커서가 늙음(%s)" % CH), 0)

    def test_conditional_channel_error_reaches_poll_as_error(self):                       # (f)
        L = Ledger()
        t = ConditionalChannel.T()
        ch = ConditionalFileChannel(L, t, "https://example.org/f", expect="hello")
        L.channel("ex", "https://example.org/f", "revision_history")
        t.body, t.status = b"hello v1", 200
        L.poll("https://example.org/f", ch.listing("2026-11-26T00:00:00Z"), "2026-11-26T00:00:00Z",
               outcome=ch.last_outcome)
        t.body, t.etag = b"<html>error</html>", '"e2"'                              # 200인데 기대 표지가 없다
        listing = ch.listing("2026-11-29T00:00:00Z")
        self.assertEqual(ch.last_outcome, "error")
        L.poll("https://example.org/f", listing, "2026-11-29T00:00:00Z", outcome=ch.last_outcome)
        self.assertEqual(L.db.execute("SELECT confirmed_at FROM channel WHERE url=?", ("https://example.org/f",)).fetchone()[0],
                         "2026-11-26T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
