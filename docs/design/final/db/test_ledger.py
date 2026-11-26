"""확인 장부 구조 v1 프로토타입 시험. 실행: python3 -I -m unittest -v test_ledger (이 디렉터리에서)."""
import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cases  # noqa: E402
from ledger import Ledger, PrivacyError  # noqa: E402

T = "2026-11-26T00:00:00Z"


def small():
    L = Ledger()
    o, _ = L.observe(url="https://example.org/doc", edition_key="v1", edition_kind="release", position="§1",
                     at=T, method="read_line", quote="Export is supported.", quote_lang="en",
                     statement="내보내기를 지원한다.")
    return L, o


class StorageContract(unittest.TestCase):
    def test_observation_is_append_only(self):
        L, o = small()
        with self.assertRaises(sqlite3.DatabaseError):
            L.db.execute("UPDATE observation SET statement='x' WHERE obs_id=?", (o,))
        with self.assertRaises(sqlite3.DatabaseError):
            L.db.execute("DELETE FROM observation WHERE obs_id=?", (o,))

    def test_same_content_is_a_sighting_other_edition_is_new(self):
        L, o = small()
        o2, created = L.observe(url="https://example.org/doc", edition_key="v1", edition_kind="release",
                                position="§1", at="2026-11-27T00:00:00Z", method="read_line",
                                quote="Export   is supported.", quote_lang="en", statement="내보내기를 지원한다.")
        self.assertEqual((o2, created), (o, False))
        self.assertEqual(L.counts()["sightings"], 1)
        o3, created = L.observe(url="https://example.org/doc", edition_key="v2", edition_kind="release",
                                position="§1", at="2026-11-28T00:00:00Z", method="read_line",
                                quote="Read-only.", quote_lang="en", statement="읽기 전용.")
        self.assertTrue(created)
        self.assertNotEqual(o3, o)

    def test_reverse_order_editions_use_publication_order(self):
        L = Ledger()
        for key, pub in (("rev:308427", "2025-10-09"), ("rev:308355", "2025-10-08")):
            L.observe(url=cases.KB, edition_key=key, edition_kind="revision", position="dates", at=T,
                      method="read_line", quote=key, quote_lang="en", statement=key, published_at=pub)
        self.assertEqual(L.latest_edition(cases.KB, T), "rev:308427")

    def test_intake_retry_and_conflict(self):
        L = Ledger()
        p = L.project("A")
        kw = dict(request_key="R", rev=1, at=T, text="t", selected_part="s",
                  requirements=[{"code": "H1", "kind": "must", "text": "x"}])
        self.assertEqual(L.intake(p, **kw), L.intake(p, **kw))
        with self.assertRaises(ValueError):
            L.intake(p, **dict(kw, text="다른 내용"))

    def test_privacy_lint_blocks_request_words_in_public_tags(self):
        L, o = small()
        p = L.project("A")
        L.intake(p, request_key="R", rev=1, at=T, text="auditor handover of confidential conversation transcripts",
                 selected_part="s", requirements=[])
        with self.assertRaises(PrivacyError):
            L.tag(o, "summary", "one_up", "en", "export confidential conversation transcripts for an auditor")
        L.tag(o, "summary", "one_up", "en", "export is supported")

    def test_compose_is_atomic_and_idempotent(self):
        L, o = small()
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[])
        slot = {"kind": "direct", "first": o, "ladder": "L2", "verb": "v", "where": "§1", "reason": "r", "hold": "h"}
        r1 = L.compose(p, req, T, slots=[slot])
        self.assertEqual(r1, L.compose(p, req, T, slots=[slot]))
        with self.assertRaises(ValueError):
            L.compose(p, req, T, slots=[slot, dict(slot, kind="nonsense")])
        self.assertEqual(L.db.execute(f"SELECT count(*) FROM {p}.answer_run").fetchone()[0], 1)

    def test_lease_prevents_double_work_and_expires(self):
        L, o = small()
        L.channel("ex", "https://example.org/changes", "changelog")
        L.watch(o, "https://example.org/changes")
        L.poll("https://example.org/changes", [{"id": "1", "title": "v2"}], T)
        job = L.jobs()[0]["job_id"]
        self.assertTrue(L.lease(job, "2026-11-26T01:00:00Z"))
        self.assertFalse(L.lease(job, "2026-11-26T01:00:00Z"))
        self.assertEqual(L.release_expired("2026-11-26T02:00:00Z"), 1)
        self.assertTrue(L.lease(job, "2026-11-26T03:00:00Z"))

    def test_channel_uses_id_diff_not_display_window(self):
        L, o = small()
        L.channel("ex", "https://example.org/changes", "changelog")
        L.watch(o, "https://example.org/changes")
        items = [{"id": "a", "title": "old"}, {"id": "b", "title": "new"}]
        self.assertEqual(len(L.poll("https://example.org/changes", items, T)), 2)
        self.assertEqual(len(L.poll("https://example.org/changes", list(reversed(items)), T)), 0)
        jobs = L.jobs()
        self.assertEqual(len(jobs), 1)       # 같은 관측의 열린 작업 하나에 두 항목이 합쳐진다
        self.assertIn("#b", jobs[0]["merged_causes"])

    def test_deadline_job_merges_with_channel_item_and_does_not_invalidate(self):
        L, o = small()
        L.channel("ex", "https://example.org/changes", "changelog")
        L.watch(o, "https://example.org/changes", deadline="2026-12-01T00:00:00Z")
        self.assertEqual(L.due("2026-11-29T00:00:00Z"), 0)
        self.assertEqual(L.due("2026-11-30T00:00:00Z"), 1)            # 기한 24시간 전
        self.assertEqual(L.due("2026-12-01T00:00:00Z"), 0)            # 열린 작업에 합쳐짐
        L.poll("https://example.org/changes", [{"id": "x", "title": "deadline moved"}], "2026-12-01T00:00:00Z")
        self.assertEqual(len(L.jobs()), 1)
        self.assertEqual(L.db.execute("SELECT count(*) FROM supersession").fetchone()[0], 0)  # 기한 경과만으로 무효 없음

    def test_reuse_gate_five_conditions(self):
        L, o = small()
        self.assertEqual(L.reuse_gate(o, T)["decision"], "reopen")      # 감시 없음
        L.channel("ex", "https://example.org/changes", "changelog", period_h=72)
        L.watch(o, "https://example.org/changes")
        L.poll("https://example.org/changes", [], "2026-11-26T06:00:00Z")
        g = L.reuse_gate(o, "2026-11-27T00:00:00Z")
        self.assertEqual(g["decision"], "reuse")
        self.assertIn("채널 확인 시각", g["basis"])
        self.assertEqual(L.reuse_gate(o, "2026-12-05T00:00:00Z")["decision"], "reopen")   # 커서·직접 확인 늙음
        L.poll("https://example.org/changes", [{"id": "n", "title": "v2"}], "2026-11-27T00:00:00Z")
        self.assertIn("처리 안 된 재확인 작업", L.reuse_gate(o, "2026-11-27T01:00:00Z")["why"])

    def test_exposure_needs_seal_first(self):
        L, o = small()
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[])
        run = L.compose(p, req, T, slots=[{"kind": "direct", "first": o, "ladder": "L2", "verb": "v", "where": "§1",
                                           "reason": "r", "hold": "h"}])
        with self.assertRaises(ValueError):
            L.show(p, run, 1, T)
        req2 = L.intake(p, request_key="R", rev=2, at=T, text="t", selected_part="s", requirements=[],
                        prior={"state": "declined"})
        run2 = L.compose(p, req2, T, slots=[{"kind": "direct", "first": o, "ladder": "L2", "verb": "v", "where": "§1",
                                             "reason": "r", "hold": "h"}])
        L.show(p, run2, 1, T)

    def test_check_slot_name_must_come_from_search_record(self):
        L, o = small()
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[])
        slot = {"kind": "check", "first": o, "ladder": "L0", "verb": "v", "reason": "r", "hold": "h"}
        with self.assertRaises(ValueError):
            L.compose(p, req, T, slots=[slot])
        L.search_fresh(p, req, T, {"direct": [{"url": "https://example.org/doc"}]})
        L.compose(p, req, T, slots=[slot])

    def test_cancelled_alias_is_not_followed(self):
        L = Ledger()
        a = L.alias("https://formulae.example/tree-sitter", "https://formulae.example/tree-sitter-cli", "moved", T)
        self.assertEqual(L.resolve("https://formulae.example/tree-sitter", T),
                         "https://formulae.example/tree-sitter-cli")
        L.cancel_alias(a, "2026-11-27T00:00:00Z", "이름은 남았지만 다른 대상을 가리킴(023)")
        self.assertEqual(L.resolve("https://formulae.example/tree-sitter", "2026-11-28T00:00:00Z"),
                         "https://formulae.example/tree-sitter")
        self.assertEqual(L.resolve("https://formulae.example/tree-sitter", "2026-11-26T12:00:00Z"),
                         "https://formulae.example/tree-sitter-cli")


class Rules(unittest.TestCase):
    def test_clarify_rule(self):
        d = Ledger.decide
        self.assertEqual(d("§a", "§a"), "proceed")
        self.assertEqual(d("§a", "§b", fields_settle=True, irreversible=True), "reread")
        self.assertEqual(d("§a", "§b", common_action=True, irreversible=True), "common")
        self.assertEqual(d("§a", "§b", studio_can_fetch=True), "fetch")
        self.assertEqual(d("§a", "§b", execution_can_settle=True), "verify")
        self.assertEqual(d("§a", "§b", irreversible=True), "ask_once")
        self.assertEqual(d("§a", "§b"), "conditional")

    def test_gate_closes_when_target_doc_already_says_it(self):
        g = Ledger.gate(role_map=[("a", "b")], invariant_quote="q", break_input="x", baseline_prediction="p",
                        principle_prediction="q", target_doc_states_it=True)
        self.assertEqual(g["decision"], "fold_test")
        g = Ledger.gate(role_map=[("a", "b")], invariant_quote="q", break_input="x", baseline_prediction="p",
                        principle_prediction="q", target_doc_states_it=False)
        self.assertEqual(g["decision"], "open")


class Cases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = cases.run_all()

    # 사례 A
    def test_a_drawer_ranks_queue_first_and_drops_toyota_coincidence(self):
        a = self.r["A"]
        self.assertEqual(a["drawer"][0][0], "asyncio-queue")
        self.assertTrue(a["drawer"][0][3])
        rank_fw, matched_fw, _ = a["drawer_audit_toyota"][0]
        self.assertLessEqual(rank_fw, 4)                       # 기능어를 세면 상위에 오른다
        self.assertTrue({"the", "and", "of"} & set(matched_fw))
        self.assertEqual(a["drawer_content_toyota"][0][1], ["time"])  # 내용어로는 관용구 한 단어뿐
        self.assertNotIn("toyota-jit", [h[0] for h in a["drawer"]])
        self.assertEqual(a["gate_r1"]["decision"], "fold_test")
        # 자리는 해석 복창과 직접 도구 하나. 세마포어 선획득은 근접 대안, 범위 밖 실패 시험은 접힌 목록에만
        self.assertEqual([s["kind"] for s in a["run1"]["slots"]], ["check", "direct"])
        conds = [f["condition"] for f in a["run1"]["folded"]]
        self.assertIn("범위 안의 실패 시험인가", conds)
        self.assertIn("대기 8을 대기열 길이로 지키는가", conds)
        self.assertIn("[필수] 일꾼 작업을 정확히 4개", a["run1"]["slots"][1]["sentence"])

    def test_a_runtime_change_reopens_only_the_new_edition(self):
        a = self.r["A"]
        self.assertTrue(all(d["edition_mismatch"] for d in a["carry"]["dropped"]))
        self.assertTrue(a["same_sentence_across_editions"])
        self.assertIsNone(a["reuse_313_for_312"])
        self.assertIn("끝 표지", a["run2"]["slots"][1]["sentence"])
        self.assertIn("v3.12.3", a["run2"]["slots"][1]["sentence"])
        self.assertEqual(a["run1_after"]["slots"], a["run1"]["slots"])     # 지난 답은 그대로
        self.assertEqual(len(a["run1_after"]["notices"]), 1)

    def test_a_other_project_reuses_same_edition_without_rereading(self):
        a = self.r["A"]
        self.assertTrue(a["project_c_reused"])
        self.assertEqual(a["project_c_gate"]["decision"], "reopen")   # 16일 지남 → 뒤집을 위치만 대조
        self.assertEqual(a["project_c_full_opens"], 0)
        self.assertEqual(a["project_c_sees_A_slips"], 0)

    def test_a_no_answer_gives_next_action_not_a_bare_abstain(self):
        n = self.r["A"]["no_answer"]
        self.assertEqual(n["status"], "none_verified")
        self.assertEqual([s["kind"] for s in n["slots"]], ["check"])     # 해석 줄만 남는다
        self.assertIn("첫 확인 항목", n["next_action"])
        self.assertEqual(len(n["folded"]), 6)                              # 갈린 조건과 함께 남은 대안

    # 사례 B
    def test_b_t0(self):
        b = self.r["B"]
        self.assertEqual(b["clarify_T0c"], "reread")
        self.assertEqual(b["gate_x1"]["decision"], "open")
        kinds = [s["kind"] for s in b["run0"]["slots"]]
        self.assertEqual(kinds, ["check", "check", "principle"])    # 0번은 해석 복창
        self.assertIn("목록에 있다는 것만", b["run0"]["slots"][1]["sentence"])   # T0-a 오승인 없음

    def test_b_each_event_touches_only_the_pocket_slot(self):
        b = self.r["B"]
        for e in b["events"]:
            self.assertEqual(e["jobs"], 1)
            self.assertEqual([s for s, _ in e["notices"]], [1])
        self.assertEqual(b["principle_notices"], [])                 # T2-b
        self.assertTrue(b["run0"]["contrast"])                        # 원리 자리는 Pocket을 대조로만 인용
        self.assertTrue(any(e["merged"] for e in b["events"]))        # 기한 작업과 채널 항목이 하나로

    def test_b_what_we_knew_on_a_day(self):
        b = self.r["B"]
        self.assertIn("11월 6일", b["known_2025_10_09"])            # E-a
        self.assertIn("11월 12일", b["known_2025_10_10"])

    def test_b_replay_and_no_answer(self):
        b = self.r["B"]
        self.assertTrue(b["run0_slots_unchanged"])                    # T1-b
        self.assertEqual(b["run2"]["status"], "none_verified")        # T2-a
        self.assertIn("첫 확인 항목", b["run2"]["next_action"])

    def test_b_t3_rediscovers_principle_without_inheriting_judgment(self):
        b = self.r["B"]
        self.assertEqual(b["t3_drawer"][0][0], cases.OAI_URL)       # T3-a
        self.assertIn(cases.OAI_URL, b["t3_path_log"]["drawer_only"])
        self.assertEqual(b["t3_sees_X_slips"], 0)                     # T3-b
        self.assertEqual([s["kind"] for s in b["t3_run"]["slots"]], ["check", "principle"])
        self.assertIn("감시 없음", b["t3_reuse_gate"]["why"])
        for s in b["t3_run"]["slots"]:                               # X의 맥락이 W 답에 새지 않는다
            self.assertNotIn("Pocket", s["sentence"])
            self.assertNotIn("클리퍼", s["sentence"])
        self.assertEqual(b["t3_inherited"], 0)

    # 장면 2
    def test_r2_foreign_feature_rediscovered_by_slots(self):
        r2 = self.r["R2"]
        self.assertEqual(r2["clarify"], "common")                      # 공통 행동으로 질문 0
        urls = [u for u, _, _ in r2["drawer"]]
        self.assertIn(cases.II_SVN, urls)
        self.assertIn(cases.II_SVN, r2["path_log"]["drawer_only"])
        self.assertTrue(r2["ii_svn_in_answer"])
        self.assertEqual(r2["collection_opens"], 0)

    # 구성요소 삭제
    def test_ablation(self):
        rows = {r["variant"]: r for r in cases.ablation()}
        base, nodrawer = rows["기준(전부 켬)"], rows["서랍 끔"]
        self.assertTrue(nodrawer["A_first_link_same"] and nodrawer["B_T2_answer_same"])
        self.assertFalse(nodrawer["R2_foreign_precedent"])
        self.assertFalse(nodrawer["B_T3_principle_found"])
        self.assertGreater(nodrawer["A_projectC_full_opens"], base["A_projectC_full_opens"])
        self.assertGreater(rows["사용 쪽지 끔"]["B_principle_false_notices"], 0)
        self.assertGreater(rows["판단 분리 끔"]["B_T3_inherited_judgments"], 0)


if __name__ == "__main__":
    unittest.main()
