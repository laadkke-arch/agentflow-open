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


class CpythonQueues:
    """기록된 CPython v3.12.3·v3.13.18 queues.py로 재생하는 판 사이 위치 시험의 공통 준비."""
    REPO, PATH, CHC = "python/cpython", "Lib/asyncio/queues.py", "https://example.org/cpython-tags"

    def setUp(self):
        from afledger import locate, normalize
        from afledger.adapters.http import Transport
        from afledger.adapters.reader_channel import PinnedCodeChannelReader
        from afledger.adapters.reader_github import raw_url
        self.locate, self.normalize = locate, normalize
        self.t = Transport("replay", HERE.parent / "fixtures" / "http")
        self.old_text = self.t.get(raw_url(self.REPO, "v3.12.3", self.PATH)).text()
        self.L = Ledger()
        self.reader = PinnedCodeChannelReader(self.L, self.t)
        self.L.channel("cpython-tags", self.CHC, "release_notes")

    def obs_at(self, a, b, *, quote=None, symbol=None, in_doc=None, poll=True):
        an = self.locate.anchor(self.old_text, a, b, python=True)
        bs = self.locate.byte_span(self.old_text, a, b)
        o, _ = self.L.observe(url=self.normalize.pinned_blob(self.REPO, self.PATH, "v3.12.3"), edition_key="v3.12.3",
                              edition_kind="release", position=self.locate.position(a, b), at=T, method="read_line",
                              quote=quote or an["quote"], quote_lang="en", statement="앞 판의 문장",
                              anchor_symbol=symbol or an["symbol"],
                              anchor_in_doc=an["in_doc"] if in_doc is None else in_doc, byte_span=f"{bs[0]}-{bs[1]}")
        self.L.watch(o, self.CHC)
        if poll:
            self.poll()
        return o

    def poll(self):
        self.L.poll(self.CHC, [{"id": "v3.13.18", "title": "v3.13.18", "edition": "v3.13.18"}], "2026-11-27T00:00:00Z")

    def work(self):
        judge = lambda old, r: "confirms" if old["quote"] == r["quote"] else "changes_value"   # noqa: E731
        return RecheckWorker(self.L, self.reader, judge).run_once("2026-11-27T01:00:00Z")



class CrossEditionMappingI36(CpythonQueues, unittest.TestCase):
    """08 I36: 채널 항목이 준 새 판에서 앞 관측의 위치를 m1으로 찾는다."""

    def test_a_exact_quote_maps_to_new_lines_and_confirms(self):
        o = self.obs_at(36, 38)                                        # Queue.__init__ 안의 Futures 줄
        rec = self.work()
        self.assertEqual(rec[0]["result"], "superseded")
        n = self.L.obs(self.L.current(o, "2026-11-27T02:00:00Z"))
        self.assertEqual((n["edition_key"], n["position"], n["map_method"], n["map_from"]),
                         ("v3.13.18", "L48-L50", "exact_quote", o))
        self.assertEqual(n["quote"], self.L.obs(o)["quote"])
        self.assertEqual(rec[0]["chain"][0][2], "confirms")
        self.assertEqual(n["anchor_symbol"], "Queue.__init__")
        self.assertTrue(n["byte_span"])

    def test_a_symbol_fallback_maps_changed_docstring(self):
        o = self.obs_at(111, 115)                                      # Queue.put docstring, 3.13에서 문장이 늘었다
        rec = self.work()
        n = self.L.obs(self.L.current(o, "2026-11-27T02:00:00Z"))
        self.assertEqual((n["position"], n["map_method"], n["anchor_in_doc"]), ("L126-L132", "symbol", 1))
        self.assertEqual(rec[0]["chain"][0][2], "changes_value")

    def test_b_unmapped_makes_no_observation_and_opens_an_audit(self):
        o = self.obs_at(36, 38, quote="self._never_written = True", symbol="Queue._gone")
        n_obs = self.L.db.execute("SELECT count(*) FROM observation").fetchone()[0]
        rec = self.work()
        self.assertEqual(rec[0]["result"], "unmapped")
        self.assertEqual(self.L.db.execute("SELECT count(*) FROM observation").fetchone()[0], n_obs)
        self.assertEqual(self.L.db.execute("SELECT count(*) FROM supersession").fetchone()[0], 0)
        jobs = self.L.db.execute("SELECT state, cause, cause_ref FROM recheck_job ORDER BY job_id").fetchall()
        self.assertEqual([tuple(j) for j in jobs], [("done", "channel", jobs[0]["cause_ref"]),
                                                    ("queued", "audit", "unmapped:v3.13.18")])
        self.assertEqual([a["kind"] for a in self.L.alerts], ["position_unmapped"])
        self.assertIsNone(self.L.obs(o)["retracted_at"] if "retracted_at" in self.L.obs(o).keys() else None)
        self.assertEqual(self.L.current(o, "2026-11-27T02:00:00Z"), o)
        self.assertEqual(self.work(), [])                              # 감사 작업은 작업자가 잡지 않는다

    def test_c_one_follow_fetch_per_edition_and_no_request_budget(self):
        self.obs_at(36, 38)
        self.work()
        self.assertEqual(self.L.fetch_count(clock="follow"), 1)
        clocks = [r[0] for r in self.L.db.execute("SELECT clock FROM fetch_log")]
        self.assertEqual(clocks, ["follow"])                          # 요청판 장부(프로젝트 fetch_log)는 건드리지 않는다


class CancelMeetsWorkerI37(unittest.TestCase):
    """08 I37: 대체 취소가 작업자·채널과 만날 때."""
    REVS = {"rev:2": ("rev:2", "Export closed.", "2026-11-27T00:00:00Z"),        # rev:2의 오독(실제는 6월 그대로)
            "rev:3": ("rev:3", "Export until July.", "2026-11-29T00:00:00Z")}

    def setUp(self):
        self.L, self.o = doc_ledger()
        self.judged = []

    def judge(self, old, r):
        self.judged.append((old["quote"], r["quote"]))
        return "invalidates" if "closed" in r["quote"] else "changes_value"

    def worker(self, reader=None):
        return RecheckWorker(self.L, reader or reader_for(self.REVS), self.judge)

    def wrong(self):
        self.L.poll(CH, [{"id": "2", "title": "r2", "edition": "rev:2"}], "2026-11-27T01:00:00Z")
        self.worker().run_once("2026-11-27T02:00:00Z")
        n = self.L.current(self.o, "2026-11-27T03:00:00Z")
        self.assertNotEqual(n, self.o)
        return n

    def n_sup(self):
        return self.L.db.execute("SELECT count(*) FROM supersession").fetchone()[0]

    def test_a_cancel_restores_watch_and_notices_once(self):
        L, o = self.L, self.o
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[])
        slot = {"kind": "direct", "first": o, "ladder": "L2", "verb": "v", "where": "§", "reason": "r", "hold": "h"}
        run = L.compose(p, req, T, slots=[slot])
        n = self.wrong()
        self.assertEqual([x["effect"] for x in L.propagate(p, "2026-11-27T04:00:00Z")], ["invalidates"])
        L.cancel_supersession(o, n, "2026-11-28T00:00:00Z", "판독 오류")
        self.assertEqual(L.current(o, "2026-11-28T01:00:00Z"), o)
        self.assertEqual({(x["run"], x["effect"]) for x in L.propagate(p, "2026-11-28T01:00:00Z")}, {(run, "restored")})
        self.assertEqual(L.propagate(p, "2026-11-28T02:00:00Z"), [])                 # 한 번만
        L.poll(CH, [{"id": "3", "title": "r3", "edition": "rev:3"}], "2026-11-29T01:00:00Z")
        self.assertEqual([j["obs_id"] for j in L.jobs("queued")], [o])               # 철회된 쪽에는 작업이 없다

    def test_b_late_finish_after_cancel_writes_nothing_from_the_retracted_reading(self):
        L, o = self.L, self.o
        n = self.wrong()
        L.poll(CH, [{"id": "3", "title": "r3", "edition": "rev:3"}], "2026-11-29T01:00:00Z")
        self.assertEqual([j["obs_id"] for j in L.jobs("queued")], [n])
        base = reader_for(self.REVS)

        def cancelling_reader(obs, ek, at):                                          # 임차 뒤, 완료 전에 운영자가 취소
            L.cancel_supersession(o, n, at, "판독 오류")
            return base(obs, ek, at)
        rec = self.worker(cancelling_reader).run_once("2026-11-29T02:00:00Z")
        self.assertEqual((rec[0]["result"], rec[0]["accepted"]), ("base_moved", False))
        self.assertEqual(L.db.execute("SELECT count(*) FROM supersession WHERE old_obs=?", (n,)).fetchone()[0], 0)
        q = [(j["obs_id"], j["cause_ref"]) for j in L.jobs("queued")]
        self.assertEqual(q, [(o, CH + "#3")])
        self.assertEqual(L.current(o, "2026-11-29T03:00:00Z"), o)

    def test_b_queued_job_on_the_retracted_reading_is_closed_at_cancel(self):
        L, o = self.L, self.o
        n = self.wrong()
        L.poll(CH, [{"id": "3", "title": "r3", "edition": "rev:3"}], "2026-11-29T01:00:00Z")
        L.cancel_supersession(o, n, "2026-11-29T01:30:00Z", "판독 오류")
        rows = {(r["obs_id"], r["state"]) for r in L.db.execute("SELECT obs_id, state FROM recheck_job WHERE cause_ref=?",
                                                                 (CH + "#3",))}
        self.assertEqual(rows, {(n, "done"), (o, "queued")})
        self.worker().run_once("2026-11-29T02:00:00Z")
        self.assertEqual(L.obs(L.current(o, "2026-11-29T03:00:00Z"))["edition_key"], "rev:3")
        self.assertEqual(self.judged[-1], ("Export until June.", "Export until July."))   # 되살아난 관측과 견줌

    def test_c_rereading_the_retracted_reading_opens_an_audit(self):
        L, o = self.L, self.o
        n = self.wrong()
        L.cancel_supersession(o, n, "2026-11-28T00:00:00Z", "판독 오류")
        k = self.n_sup()
        L.poll(CH, [{"id": "2b", "title": "r2 again", "edition": "rev:2"}], "2026-11-28T01:00:00Z")
        rec = self.worker().run_once("2026-11-28T02:00:00Z")
        self.assertEqual(rec[0]["result"], "retracted_reread")
        self.assertEqual(self.n_sup(), k)
        self.assertEqual([(j["obs_id"], j["cause_ref"]) for j in L.jobs("queued")], [(o, f"reread_retracted:{n}")])
        self.assertEqual([a["kind"] for a in L.alerts], ["retracted_reread"])
        self.assertEqual(L.current(o, "2026-11-28T03:00:00Z"), o)

    def test_e_downstream_is_relinked_against_the_restored_observation(self):
        L, o = self.L, self.o
        n = self.wrong()
        L.poll(CH, [{"id": "3", "title": "r3", "edition": "rev:3"}], "2026-11-29T01:00:00Z")
        self.worker().run_once("2026-11-29T02:00:00Z")
        x = L.current(o, "2026-11-29T03:00:00Z")
        self.assertEqual(L.obs(x)["edition_key"], "rev:3")
        self.assertEqual(self.judged[-1], ("Export closed.", "Export until July."))     # 오독과 견준 효과
        L.cancel_supersession(o, n, "2026-11-30T00:00:00Z", "판독 오류")
        self.assertEqual(L.current(o, "2026-11-30T00:30:00Z"), o)
        self.assertEqual([(j["obs_id"], j["cause_ref"]) for j in L.jobs("queued")], [(o, CH + "#3")])
        rec = self.worker().run_once("2026-11-30T01:00:00Z")
        self.assertEqual(rec[0]["chain"], [(o, x, "changes_value")])
        self.assertEqual(self.judged[-1], ("Export until June.", "Export until July."))  # 되살아난 관측과 견줌
        self.assertEqual(L.current(o, "2026-11-30T02:00:00Z"), x)


class SharedTargetI37(CpythonQueues, unittest.TestCase):
    def test_d_two_observations_mapped_to_the_same_new_lines_are_both_superseded(self):
        o1 = self.obs_at(113, 115, poll=False)                    # Queue.put docstring 일부 둘
        o2 = self.obs_at(114, 115, poll=False)
        self.poll()
        self.work()
        at = "2026-11-27T02:00:00Z"
        n1, n2 = self.L.current(o1, at), self.L.current(o2, at)
        self.assertEqual(n1, n2)
        self.assertNotIn(n1, (o1, o2))
        self.assertEqual(self.L.obs(n1)["position"], "L126-L132")
