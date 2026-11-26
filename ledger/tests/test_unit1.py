"""첫 구현 단위의 완료 기준 2~5(06 3.2)를 기록 재생으로 확인한다. 실제 실행 결과는 ledger/out/r1_live.json."""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import run_r1  # noqa: E402


class CompletionCriteria(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = run_r1.run("replay")
        cls.L = cls.r.pop("_ledger")

    def test_replay_used_no_network(self):
        self.assertEqual(self.r["transport"]["requests"], self.r["transport"]["replayed"])

    # ---- 완료 기준 2
    def test_c2_first_slot_is_cpython_313_queue_at_l4_with_pinned_source_link(self):
        a = self.r["rev1"]
        ans = a["answer"]
        self.assertEqual(ans["status"], "complete")
        self.assertEqual([s["kind"] for s in ans["slots"]], ["check", "direct"])
        s1 = ans["slots"][1]["sentence"]
        self.assertIn("첫 원문: https://github.com/python/cpython/blob/v3.13.", s1)            # D10 고정판 소스 줄
        self.assertIn("/Lib/asyncio/queues.py#L", s1)
        self.assertIn("근거 수준: 이 판에서 실행해 값을 확인했다", s1)                          # L4
        self.assertTrue(a["runtime_tag"].startswith("v3.13."))
        self.assertTrue(a["execution"]["runtime_ran"].startswith("CPython 3.13"))
        self.assertIn("[필수] 일꾼 작업을 정확히 4개", s1)
        self.assertLessEqual(a["budget"]["fetches"], 4)

    def test_c2_folded_keeps_the_two_near_misses_with_their_conditions(self):
        folded = {f["condition"]: f for f in self.r["rev1"]["answer"]["folded"]}
        self.assertIn("H1 U", folded["대기 8을 대기열 길이로 지키는가"]["reason"])           # 세마포어 선획득
        self.assertIn("locks.py#L", folded["대기 8을 대기열 길이로 지키는가"]["url"])
        self.assertIn("H2 위반", folded["입력마다 작업 객체를 미리 만드는가"]["reason"])       # 전부 미리 생성

    def test_c2_search_record_has_both_paths_tokens_and_accident_flags(self):
        a = self.r["rev1"]
        self.assertEqual(a["drawer"][0]["id"], "asyncio-queue")
        self.assertTrue(all("matched" in h and "lexical_accident" in h for h in a["drawer"]))
        self.assertTrue(a["fresh_direct"]["calls"])
        self.assertEqual(a["fresh_direct"]["results"][0]["path"], "Lib/asyncio/queues.py")
        self.assertIn("matched:", a["fresh_direct"]["results"][0]["why"])
        runs = {r[0] for r in self.L.db.execute("SELECT path FROM p_A.search_run WHERE req_id=1")}
        self.assertEqual(runs, {"drawer", "fresh"})
        self.assertTrue(a["drawer_audit_accidents"])                       # 기능어를 세면 생기는 우연 적중은 자격이 없다

    # ---- 완료 기준 3
    def test_c3_runtime_312_reopens_only_the_same_positions_and_notes_the_old_answer(self):
        b = self.r["rev2"]
        self.assertTrue(b["runtime_tag"].startswith("v3.12."))
        self.assertIsNone(b["reuse_313_for_312"])
        self.assertEqual(set(b["position_map"]), {"q1", "q2", "s1"})       # 지난 답이 인용한 줄 위치만
        self.assertEqual(b["position_map"]["q2"]["method"], "unmapped")
        self.assertEqual(b["hand_map_mismatches"], 0)
        self.assertTrue(all(f["edition_key"] == b["runtime_tag"] for f in b["fetch_log"]))
        self.assertTrue(b["run1_slots_unchanged"])
        self.assertEqual(len(b["run1_after"]["notices"]), 1)
        self.assertIn("끝 표지", b["answer"]["slots"][1]["sentence"])

    # ---- 완료 기준 4
    def test_c4_other_project_reuses_without_new_reading(self):
        c = self.r["project_c"]
        self.assertTrue(c["same_as_A_q1"])
        self.assertEqual(c["new_observations"], 0)
        self.assertEqual(c["gate"]["decision"], "reopen")
        self.assertEqual(c["fetches"], 1)
        self.assertTrue(c["recheck"]["same"])
        self.assertLess(c["recheck_bytes"], c["full_file_bytes"] / 10)      # 파일 전체를 다시 읽지 않는다
        self.assertEqual(c["sees_A_slips"], 0)

    # ---- 완료 기준 5
    def test_c5_request_sentences_cannot_become_public_tags(self):
        pv = self.r["privacy"]
        self.assertTrue(all(a["rejected"] for a in pv["attempts"]))
        self.assertTrue(pv["source_side_tag_accepted"])

    def test_d6c_in_the_r1_run(self):
        d = self.r["d6c"]
        self.assertNotIn("input_json", d["commons_receipt_columns"])
        self.assertNotIn("condition", d["commons_contrast_columns"])
        self.assertNotIn("대기 최대", d["commons_exec_statement_example"])
        self.assertIn("대기 최대 8", d["project_exec_note_example"])

    def test_c2_holds_with_automatic_korean_intake_after_r5_r6(self):
        # R-5(다국어 토큰화)와 R-6(순위 r2 + 확인 범위) 뒤: 자동 한국어 접수로도 완료 기준 2가 성립한다(08 I17·I18)
        for noise in (False, True):
            r = run_r1.run("replay", needs="i1", noise=noise)
            r.pop("_ledger")
            a = r["rev1"]
            self.assertEqual(a["needs_by"], "i1")
            folded = {f["condition"]: f["reason"] for f in a["answer"]["folded"]}
            self.assertIn("H1 U", folded["대기 8을 대기열 길이로 지키는가"], noise)
            self.assertIn("H2 위반", folded["입력마다 작업 객체를 미리 만드는가"])
            s1 = a["answer"]["slots"][1]["sentence"]
            self.assertIn("/blob/v3.13.", s1)
            self.assertIn("[필수] 일꾼 작업을 정확히 4개", s1)
            self.assertLessEqual(a["budget"]["external_attempts"], 10)

    def test_live_output_is_committed_and_agrees(self):
        live = json.loads((HERE.parent / "out/r1_live.json").read_text(encoding="utf-8"))
        self.assertEqual(live["mode"], "live")
        self.assertEqual(live["rev1"]["answer"], self.r["rev1"]["answer"])
        self.assertEqual(live["rev2"]["answer"], self.r["rev2"]["answer"])


if __name__ == "__main__":
    unittest.main()
