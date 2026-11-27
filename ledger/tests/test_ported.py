"""설계 예제 시험 33개를 제품 코드로 옮긴 것. 단언은 바꾸지 않았다.

출처: docs/design/final/db/test_ledger.py (StorageContract 13, Rules 2, OperationalFixes 14, Decisions 중 d1·d6·d7·d9 4).
옮기며 바꾼 것(단언 밖): import 경로, `cases.KB` 대신 같은 값의 상수 KB. 08-implementation.md I1 참조.
실행: python3 -I ledger/tests/run.py  또는  python3 -I -m unittest discover -s ledger/tests
"""
import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from afledger import Ledger, PrivacyError  # noqa: E402

KB = "https://support.mozilla.org/en-US/kb/future-of-pocket"   # 설계 예제 cases.KB와 같은 값
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
            L.observe(url=KB, edition_key=key, edition_kind="revision", position="dates", at=T,
                      method="read_line", quote=key, quote_lang="en", statement=key, published_at=pub)
        self.assertEqual(L.latest_edition(KB, T), "rev:308427")

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
            L.compose(p, req, T, slots=[slot], status="partial")
        with self.assertRaises(ValueError):    # first 없이 url만 줘도 같은 검사를 받는다
            L.compose(p, req, T, slots=[{"kind": "check", "url": "https://example.org/memory-only", "ladder": "L0",
                                         "verb": "v", "reason": "r", "hold": "h"}], status="partial")
        L.search_fresh(p, req, T, {"direct": [{"url": "https://example.org/doc"}]})
        L.compose(p, req, T, slots=[slot], status="partial")
        with self.assertRaises(ValueError):    # 확인할 후보만으로는 complete가 될 수 없다
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



class OperationalFixes(unittest.TestCase):
    """운영 시뮬레이션(../sim/ops_sim.py)이 찾은 깨짐을 고친 뒤 지키는 계약. 07-review.md 5절."""
    CH = "https://example.org/changes"

    def watched(self, deadline=None):
        L, o = small()
        L.channel("ex", self.CH, "changelog")
        L.watch(o, self.CH, deadline=deadline)
        return L, o

    def second(self, L, at="2026-11-27T00:00:00Z", key="v2", quote="Read-only.", **kw):
        return L.observe(url="https://example.org/doc", edition_key=key, edition_kind="release", position="§1",
                         at=at, method="read_line", quote=quote, quote_lang="en", statement=quote, **kw)[0]

    def test_late_worker_is_fenced_and_supersession_is_written_once(self):   # M5a
        L, o = self.watched()
        L.poll(self.CH, [{"id": "1", "title": "v2"}], T)
        job = L.jobs()[0]["job_id"]
        t1 = L.lease(job, "2026-11-26T01:00:00Z")
        self.assertEqual(L.release_expired("2026-11-26T02:00:00Z"), 1)
        t2 = L.lease(job, "2026-11-26T03:00:00Z")
        self.assertNotEqual(t1, t2)
        o2 = self.second(L, at="2026-11-26T02:30:00Z")
        self.assertTrue(L.finish(job, o2, token=t2, supersede=(o, "changes_value", "2026-11-26T02:30:00Z", None)))
        o3 = self.second(L, at="2026-11-26T03:30:00Z", quote="Read-only, export removed.")
        self.assertFalse(L.finish(job, o3, token=t1, supersede=(o, "changes_value", "2026-11-26T03:30:00Z", None)))
        self.assertEqual(L.db.execute("SELECT count(*) FROM supersession").fetchone()[0], 1)
        self.assertEqual(L.db.execute("SELECT result_obs FROM recheck_job WHERE job_id=?", (job,)).fetchone()[0], o2)

    def test_new_cause_does_not_merge_into_a_leased_job(self):   # M5b
        L, o = self.watched()
        L.poll(self.CH, [{"id": "1", "title": "v2"}], T)
        job = L.jobs()[0]["job_id"]
        L.lease(job, "2026-11-26T05:00:00Z")
        L.poll(self.CH, [{"id": "2", "title": "v3"}], "2026-11-26T01:00:00Z")
        self.assertEqual(len(L.jobs("queued")), 1)
        self.assertNotEqual(L.jobs("queued")[0]["job_id"], job)

    def test_watch_moves_to_the_new_observation(self):   # M1 공급자 층 감시 소멸
        L, o = self.watched()
        o2 = self.second(L)
        L.supersede(o, o2, "changes_value", "2026-11-27T00:00:00Z")
        L.poll(self.CH, [{"id": "x", "title": "v3"}], "2026-11-28T00:00:00Z")
        self.assertEqual([j["obs_id"] for j in L.jobs()], [o2])

    def test_cancelled_supersession_restores_and_warns(self):   # M4c
        L, o = self.watched()
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[])
        slot = {"kind": "direct", "first": o, "ladder": "L2", "verb": "v", "where": "§1", "reason": "r", "hold": "h"}
        run = L.compose(p, req, T, slots=[slot])
        o2 = self.second(L, key="v1", quote="Export is not supported.")      # 같은 판을 잘못 읽은 판독
        L.supersede(o, o2, "changes_value", "2026-11-27T00:00:00Z")
        self.assertEqual(L.current(o, "2026-11-27T01:00:00Z"), o2)
        self.assertEqual([n["effect"] for n in L.propagate(p, "2026-11-27T01:00:00Z")], ["changes_value"])
        req2 = L.intake(p, request_key="R", rev=2, at="2026-11-27T02:00:00Z", text="t2", selected_part="s",
                        requirements=[])
        run2 = L.compose(p, req2, "2026-11-27T02:00:00Z", slots=[dict(slot, first=o2)])
        L.cancel_supersession(o, o2, "2026-11-28T00:00:00Z", "판독 오류")
        at = "2026-11-28T01:00:00Z"
        self.assertEqual(L.current(o, at), o)
        self.assertTrue(L.stale(o2, at))
        self.assertFalse(L.stale(o, at))
        got = {(n["run"], n["effect"]) for n in L.propagate(p, at)}
        self.assertEqual(got, {(run, "restored"), (run2, "invalidates")})
        L.poll(self.CH, [{"id": "y", "title": "v3"}], "2026-11-28T02:00:00Z")   # 감시가 앞 관측으로 돌아온다
        self.assertIn(o, [j["obs_id"] for j in L.jobs()])
        with self.assertRaises(sqlite3.DatabaseError):
            L.db.execute("DELETE FROM supersession")

    def test_stale_observation_is_not_reused_or_cited(self):   # M7e
        L, o = small()
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[])
        o2 = self.second(L)
        L.supersede(o, o2, "invalidates", "2026-11-27T00:00:00Z")
        at = "2026-11-27T01:00:00Z"
        self.assertEqual(L.reusable("https://example.org/doc", "v1", "§1", at=T), o)
        self.assertIsNone(L.reusable("https://example.org/doc", "v1", "§1", at=at))
        slot = {"kind": "direct", "first": o, "ladder": "L2", "verb": "v", "where": "§1", "reason": "r", "hold": "h"}
        with self.assertRaises(ValueError):
            L.compose(p, req, at, slots=[slot])
        L.compose(p, req, at, slots=[dict(slot, first=o2)])
        self.assertIn("대체되었거나", " ".join(L.reuse_gate(o, at)["why"]))

    def test_transient_failure_is_not_reusable(self):
        L = Ledger()
        L.observe(url="https://example.org/x", edition_key="v1", edition_kind="release", position="§1", at=T,
                  method="intro_only", outcome="unreachable", statement="열리지 않음")
        self.assertIsNone(L.reusable("https://example.org/x", "v1", "§1"))

    def test_compose_rules_for_principle_and_complete(self):
        L, o = small()
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[])
        base = {"first": o, "verb": "v", "where": "§1", "reason": "r", "hold": "h", "borrow": "b", "recheck": "c",
                "break": "x"}
        with self.assertRaises(ValueError):
            L.compose(p, req, T, slots=[dict(base, kind="principle", ladder="L3")], status="partial")
        with self.assertRaises(ValueError):
            L.compose(p, req, T, slots=[dict(base, kind="principle", ladder="L2")])
        L.compose(p, req, T, slots=[dict(base, kind="principle", ladder="L2")], status="partial")

    def test_deadline_formats_are_normalized_or_rejected(self):   # M9
        L, o = small()
        L.channel("ex", self.CH, "changelog")
        L.watch(o, self.CH, deadline="2026-12-01")
        self.assertEqual(L.db.execute("SELECT deadline FROM watch").fetchone()[0], "2026-12-01T00:00:00Z")
        self.assertEqual(L.due("2026-11-30T00:00:00Z"), 1)
        with self.assertRaises(ValueError):
            L.watch(o, self.CH, "k2", deadline="12월 1일")
        L.db.execute("INSERT INTO watch(obs_id, channel_id, match_key, layer, deadline) VALUES (?,1,'bad',"
                     "'same_address','soon')", (o,))
        L2, o2 = self.watched(deadline="2026-12-01T09:00:00+09:00")    # 한국 시각 9시 = UTC 0시
        self.assertEqual(L2.db.execute("SELECT deadline FROM watch").fetchone()[0], "2026-12-01T00:00:00Z")
        L.due("2026-12-02T00:00:00Z")             # 형식이 틀린 행 하나가 전체를 막지 않는다
        self.assertEqual(len(L.clock_errors), 1)

    def test_channel_duplicates_and_id_scheme_reset(self):   # M12
        L, o = self.watched()
        L.poll(self.CH, [{"id": "a", "title": "x"}, {"id": "a", "title": "x"}], T)
        L.poll(self.CH, [{"id": str(i), "title": "x"} for i in range(5)], "2026-11-27T00:00:00Z")
        before = len(L.jobs())
        L.poll(self.CH, [{"id": f"new-{i}", "title": "x"} for i in range(60)], "2026-11-28T00:00:00Z")
        self.assertEqual(len(L.jobs()), before)
        self.assertEqual(L.alerts[-1]["kind"], "channel_id_reset_suspected")
        self.assertEqual(L.poll(self.CH, [{"id": "new-0", "title": "x"}], "2026-11-29T00:00:00Z"), [])

    def test_exposure_needs_seal_time_and_seal_is_immutable(self):
        L, o = small()
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at="2026-11-27T00:00:00Z", text="t", selected_part="s",
                       requirements=[], prior={"state": "none"})
        run = L.compose(p, req, T, slots=[{"kind": "direct", "first": o, "ladder": "L2", "verb": "v", "where": "§1",
                                           "reason": "r", "hold": "h"}])
        with self.assertRaises(ValueError):
            L.show(p, run, 1, T)
        L.show(p, run, 1, "2026-11-27T00:00:00Z")
        with self.assertRaises(sqlite3.DatabaseError):
            L.db.execute(f"UPDATE {p}.prior_seal SET items_json='{{}}'")

    def test_privacy_error_does_not_echo_the_private_words(self):   # M2b
        L, o = small()
        p = L.project("A")
        L.intake(p, request_key="R", rev=1, at=T, text="auditor handover of confidential conversation transcripts",
                 selected_part="s", requirements=[])
        with self.assertRaises(PrivacyError) as e:
            L.tag(o, "summary", "one_up", "en", "export confidential conversation transcripts")
        for w in ("confidential", "conversation", "transcripts", p):
            self.assertNotIn(w, str(e.exception))

    def test_reader_is_recorded_and_can_be_recalled(self):   # M7c
        L = Ledger()
        for i, r in enumerate(("reader-a", "reader-a", "reader-b")):
            L.observe(url=f"https://example.org/{i}", edition_key="v1", edition_kind="release", position="§1",
                      at=T, method="read_line", quote=f"q{i}", quote_lang="en", statement=f"s{i}", reader=r)
        self.assertEqual(L.recall_reader("reader-a", "2026-11-27T00:00:00Z"), 2)
        self.assertTrue(all(j["cause"] == "audit" and j["cause_ref"] == "reader:reader-a" for j in L.jobs()))

    def test_interpretation_is_not_overwritten(self):
        L, _o = small()
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[])
        L.interpret(p, req, "C1", "a", "b", "ask_once", T, question="a인가요 b인가요?")
        L.interpret(p, req, "C1", "a", "b", "ask_once", T, question="a인가요 b인가요?")
        L.interpret(p, req, "C1", "a", "b", "ask_once", T, question="a인가요 b인가요?", answer="a")
        with self.assertRaises(ValueError):
            L.interpret(p, req, "C1", "b", "a", "proceed", T)
        self.assertEqual(L.db.execute(f"SELECT answer FROM {p}.interpretation").fetchone()[0], "a")

    def test_carry_slips_drops_judgments_on_retired_observations(self):   # M7d
        L, o = small()
        p = L.project("A")
        r1 = L.intake(p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[])
        L.judge(p, r1, "H1", o, "Y", "direct", "L2", "r", T)
        r2 = L.intake(p, request_key="R", rev=2, at="2026-11-28T00:00:00Z", text="t2", selected_part="s",
                      requirements=[])
        L.supersede(o, self.second(L), "invalidates", "2026-11-27T00:00:00Z")
        out = L.carry_slips(p, r1, r2, "2026-11-28T00:00:00Z", lambda obs, ctx: True)
        self.assertEqual(out["kept"], [])
        self.assertTrue(out["dropped"][0]["superseded"])


class Decisions(unittest.TestCase):
    """07-review.md 6절에서 확정한 설계 결정. 갈린 결정은 ../sim/decide_sim.py로 비교해 골랐다."""
    CH = "https://example.org/changes"

    def test_d1_budget_counts_fetches_not_observations(self):
        L, o = small()
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[])
        L.fetched("https://example.org/doc", "v1", T, p=p, req=req)            # 한 파일에서 위치 셋을 읽어도 한 번
        L.fetched("https://example.org/doc2", "v1", T, "unreachable", p=p, req=req)   # 실패도 센다
        L.fetched("https://example.org/feed", None, T, "not_modified", clock="background")
        self.assertEqual(L.fetch_count(p=p, req=req), 2)
        self.assertEqual(L.request_budget_left(p, req), 2)
        self.assertEqual(L.fetch_count(clock="background"), 0)                 # 304는 읽기 예산 밖
        self.assertEqual(L.fetch_count(clock="background", include_not_modified=True), 1)
        with self.assertRaises(ValueError):
            L.fetched("https://example.org/doc", "v1", T)                       # 요청 시계는 요청판을 적는다

    def test_d6_private_source_and_request_time(self):
        L = Ledger()
        with self.assertRaises(PrivacyError):
            L.observe(url="https://github.com/acme/internal/blob/main/README.md", edition_key="abc", edition_kind="commit",
                      position="L1", at=T, method="read_line", quote="Internal.", quote_lang="en", statement="내부",
                      visibility="private")
        self.assertEqual(L.db.execute("SELECT count(*) FROM locator").fetchone()[0], 0)
        L.observe(url="https://example.org/a", edition_key="v1", edition_kind="release", position="§1",
                  at="2026-11-26T13:47:05Z", method="read_line", quote="A.", quote_lang="en", statement="a")
        self.assertEqual(L.db.execute("SELECT first_seen_at FROM locator").fetchone()[0], "2026-11-26T00:00:00Z")

    def test_d7_quote_is_erased_with_a_tombstone(self):
        L, o = small()
        self.assertEqual(L.obs(o)["quote"], "Export is supported.")
        self.assertEqual(L.redact(obs_id=o, at="2026-11-27T00:00:00Z", reason="권리자 요청"), 1)
        row = L.obs(o)
        self.assertIsNone(row["quote"])
        self.assertIsNotNone(row["quote_fp"])                                   # 지문·진술은 남는다
        self.assertEqual(row["statement"], "내보내기를 지원한다.")
        L.observe(url="https://example.org/doc", edition_key="v1", edition_kind="release", position="§1",
                  at="2026-11-28T00:00:00Z", method="read_line", quote="Export is supported.", quote_lang="en",
                  statement="내보내기를 지원한다.")
        self.assertIsNone(L.obs(o)["quote"])                                    # 다시 읽어도 본문을 되살리지 않는다
        with self.assertRaises(sqlite3.DatabaseError):
            L.db.execute("UPDATE quote_text SET text='x'")
        with self.assertRaises(sqlite3.DatabaseError):
            L.db.execute("DELETE FROM quote_text")

    def test_d9_edition_match_rule(self):
        m = Ledger.edition_matches
        self.assertTrue(m("CPython 3.13", "v3.13.18"))
        self.assertFalse(m("CPython 3.1", "v3.13.18"))
        self.assertTrue(m("3.13.18", "v3.13.18"))
        self.assertFalse(m("3.13.17", "v3.13.18"))
        self.assertFalse(m("", "v3.13.18"))


if __name__ == "__main__":
    unittest.main()
