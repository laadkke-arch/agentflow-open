"""어댑터 넷(판독·실행 영수증·새 검색·Studio 입력)과 07 D6c(요청 수치는 프로젝트 장부로)의 계약."""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
from afledger import Ledger, PrivacyError, studio  # noqa: E402
from afledger.adapters import search_github  # noqa: E402
from afledger.adapters.http import ReplayMiss, Transport  # noqa: E402
from afledger.adapters.runner import ReceiptRunner, record_receipt  # noqa: E402
from afledger.intake import intake, write_needs  # noqa: E402
from afledger.ledger import content_tokens  # noqa: E402

T = "2026-11-26T00:00:00Z"
FIX = HERE.parent / "fixtures"


class D6cRequestNumbersStayInTheProject(unittest.TestCase):
    def setUp(self):
        self.L = Ledger()
        self.pa, self.pb = self.L.project("A"), self.L.project("B")
        self.inp = {"items": 40, "maxsize": 8, "workers": 4}
        self.outp = {"max_waiting": 8, "max_in_flight": 4, "tasks_created": 4}

    def test_receipt_body_goes_to_the_project_and_commons_holds_keyed_fingerprints(self):
        with self.assertRaises(PrivacyError):
            self.L.receipt("CPython 3.13.18", "abc", self.inp, self.outp, T)
        ra = self.L.receipt("CPython 3.13.18", "abc", self.inp, self.outp, "2026-11-26T13:47:05Z", p=self.pa)
        rb = self.L.receipt("CPython 3.13.18", "abc", self.inp, self.outp, T, p=self.pb)
        row = dict(self.L.db.execute("SELECT * FROM receipt WHERE receipt_id=?", (ra,)).fetchone())
        self.assertNotIn("input_json", row)
        self.assertEqual(row["ran_on"], "2026-11-26")                       # 날짜까지만
        self.assertNotIn("maxsize", json.dumps(row))
        self.assertNotEqual(ra, rb)                                          # 열쇠가 프로젝트마다 달라 지문도 다르다
        self.assertEqual(self.L.receipt_body(self.pa, ra)["input"], self.inp)
        self.assertIsNone(self.L.receipt_body(self.pb, ra))                  # 다른 프로젝트는 본문을 못 본다

    def test_execution_statement_and_contrast_values_are_project_only(self):
        rid = self.L.receipt("CPython 3.13.18", "abc", self.inp, self.outp, T, p=self.pa)
        oa, _ = self.L.observe_run(self.pa, url="https://github.com/python/cpython/blob/v3.13.18/Lib/asyncio/queues.py",
                                   edition_key="v3.13.18", edition_kind="release", position="run:p A", at=T,
                                   receipt_id=rid, statement="대기 최대 8, 처리 중 최대 4")
        ob, _ = self.L.observe_run(self.pa, url="https://github.com/python/cpython/blob/v3.13.18/Lib/asyncio/locks.py",
                                   edition_key="v3.13.18", edition_kind="release", position="run:p B", at=T,
                                   receipt_id=rid, statement="작업 객체 40개")
        public = self.L.obs(oa)["statement"]
        self.assertNotIn("8", public.replace("3.13.18", ""))
        self.assertEqual(self.L.exec_note(self.pa, oa), "대기 최대 8, 처리 중 최대 4")
        self.assertIsNone(self.L.exec_note(self.pb, oa))
        with self.assertRaises(PrivacyError):
            self.L.contrast(oa, ob, "c", "예(maxsize 8)", "아니오", rid)
        self.L.contrast(oa, ob, "대기열 길이 상한을 직접 정하는가", "예(maxsize 8)", "아니오", rid, p=self.pa)
        self.assertEqual(sorted(dict(self.L.db.execute("SELECT * FROM contrast").fetchone()).keys()),
                         ["body_fp", "contrast_id", "left_obs", "receipt_id", "right_obs"])
        self.assertEqual(self.L.db.execute(f"SELECT left_value FROM {self.pa}.contrast").fetchone()[0], "예(maxsize 8)")


class StudioAndIntake(unittest.TestCase):
    def test_studio_input_validation_and_environment(self):
        kw = studio.parse({"request_key": "R", "rev": 1, "received_at": T, "text": "t",
                           "selected_part": {"label": "p", "path": "a.py", "lines": [1, 9], "commit": "c0ffee"},
                           "environment": {"runtime": "CPython 3.13", "deps": {"aiofiles": "23.2.1"}},
                           "requirements": [{"code": "H1", "kind": "must", "text": "x"}]})
        self.assertEqual(kw["selected_part"], "p (a.py:L1-L9@c0ffee)")
        self.assertEqual(kw["context"]["runtime"]["provenance"], "studio")
        self.assertIn("dep:aiofiles", kw["context"])
        with self.assertRaises(ValueError):
            studio.parse({"request_key": "R", "rev": 1, "received_at": T, "text": "t",
                          "requirements": [{"code": "H1", "kind": "maybe", "text": "x"}]})

    def test_intake_writes_needs_when_studio_gives_none(self):
        L = Ledger()
        p = L.project("A")
        d = json.loads((FIX / "r1/studio_rev1.json").read_text(encoding="utf-8"))
        d.pop("needs")
        req, info = intake(L, p, d)
        self.assertEqual(info["needs_by"], "i1")
        slots = {n["slot"] for n in info["needs"]}
        self.assertTrue({"keeps", "breaks_when"} <= slots)
        self.assertEqual(L.db.execute(f"SELECT count(*) FROM {p}.need WHERE req_id=?", (req,)).fetchone()[0], len(slots))

    def test_i1_slot_rules(self):
        n = {x["slot"]: x["text"] for x in write_needs("Goal: keep it small.\nGiven: The producer is lazy. One loop.",
                                                       [{"code": "H1", "kind": "must", "text": "at most eight items"},
                                                        {"code": "H2", "kind": "must_not", "text": "no buffer"}])}
        self.assertEqual(n, {"input": "The producer is lazy.", "keeps": "at most eight items",
                             "breaks_when": "no buffer", "summary": "keep it small. One loop."})


class SearchAndRunnerReplay(unittest.TestCase):
    def test_search_terms_rule_s1(self):
        needs = json.loads((FIX / "r1/studio_rev1.json").read_text(encoding="utf-8"))["needs"]
        ts = search_github.terms(needs, content_tokens)
        self.assertEqual(len(ts), search_github.MAX_TERMS)
        self.assertEqual([t["term"] for t in ts][:3], ["producer", "wait", "items"])   # 세 칸에 나온 낱말이 먼저
        sc = search_github.scope({"runtime": "CPython 3.13"}, "Python 3.13 asyncio의 작업", "")
        self.assertEqual((sc["repo"], sc["path"]), ("python/cpython", "Lib/asyncio"))
        self.assertIsNone(search_github.scope({"runtime": "Node 20"}, "x", ""))       # Python 밖은 범위 없음

    def test_replay_never_touches_the_network(self):
        with self.assertRaises(ReplayMiss):
            Transport("replay", FIX / "http").get("https://example.invalid/never-recorded")
        with self.assertRaises(Exception):
            ReceiptRunner("replay", FIX / "exec").run(HERE.parent / "programs/r1_queue.py", {"items": 1}, "3.9")

    def test_recorded_runs_report_the_runtime_that_actually_ran(self):
        L = Ledger()
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[])
        plan = json.loads((FIX / "r1/plan.json").read_text(encoding="utf-8"))
        for want, ran in (("3.13", "CPython 3.13.18"), ("3.12", "CPython 3.12.3")):
            rec = ReceiptRunner("replay", FIX / "exec").run(HERE.parent / plan["program"]["path"],
                                                            plan["program"]["input"], want)
            self.assertEqual(rec["runtime_ran"], ran)
            record_receipt(L, p, req, rec, T)
        self.assertEqual(L.db.execute(f"SELECT count(*) FROM {p}.exec_log").fetchone()[0], 2)
        self.assertEqual(L.fetch_count(p=p, req=req), 0)                                # 실행은 가져오기가 아니다


if __name__ == "__main__":
    unittest.main()
