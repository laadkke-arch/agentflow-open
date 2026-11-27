"""R-5 결정(다국어 토큰화 t2): 한국어 어절 줄기와 음절 2-gram을 함께 쓰고, 기능 어절은 내용어로 세지 않는다."""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from afledger import Ledger, config  # noqa: E402
from afledger import tokenize as kt  # noqa: E402

T = "2026-11-26T00:00:00Z"


class KoreanUnits(unittest.TestCase):
    def test_stems_grams_and_function_eojeols(self):
        us = {u["word"]: u for u in kt.ko_units("대기열을 비울 수 있다. '신호'에서 용량이 돌아온다")}
        self.assertIn("대기열", us)
        self.assertEqual(us["대기열"]["grams"], ["대기", "기열"])
        self.assertEqual(us["용량"]["grams"], ["용량"])            # 두 음절 줄기는 그 자체가 gram
        for w in ("수", "있다", "에서"):                             # 기능 어절·떨어진 조사는 내용어가 아니다
            self.assertNotIn(w, us)
        self.assertIn("있다", {u["word"] for u in kt.ko_units("수 있다", include_function=True)})

    def test_morpheme_level_match_counts_once_per_query_word(self):
        q = kt.ko_units("producer가 기다려야 하는 대기열")
        words, grams = kt.index_text("항목을 꺼낼 때까지 기다린다. 대기 상태")
        got = kt.match_units(q, set(words.split()), set(grams.split()))
        self.assertIn(("기다려야~기다", False), got)
        self.assertIn(("대기열~대기", False), got)
        self.assertEqual(len(got), len({m.split("~")[0] for m, _ in got}))


class DrawerT2(unittest.TestCase):
    def ledger(self, rules):
        L = Ledger()
        L.token_rules = rules
        o, _ = L.observe(url="https://example.org/sem", edition_key="v1", edition_kind="release", position="§", at=T,
                         method="intro_only", statement="세마포어")
        L.tag(o, "summary", "one_up", "ko", "동기화 부품이 0이면 release가 용량을 돌려줄 때까지 기다린다")
        f, _ = L.observe(url="https://example.org/fn", edition_key="v1", edition_kind="release", position="§", at=T,
                         method="intro_only", statement="기능어만")
        L.tag(f, "summary", "one_up", "ko", "그렇게 할 수 있다 또는 없다")
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[],
                       needs=[{"slot": "keeps", "lang": "ko", "text": "용량 회복을 근거로 삼는다"},
                              {"slot": "breaks_when", "lang": "ko", "text": "느려지면 기다려야 하며 수 있다"}])
        return L, p, req, o, f

    def test_t2_reaches_korean_tags_t1_does_not(self):
        self.assertEqual(config.TOKEN_RULES, "t2")
        L, p, req, o, f = self.ledger("t1")
        self.assertEqual(L.search_drawer(p, req, T, log=False), [])
        L, p, req, o, f = self.ledger("t2")
        hits = {h["obs_id"]: h for h in L.search_drawer(p, req, T, log=False)}
        self.assertTrue(hits[o]["eligible"])                      # 두 칸, 서로 다른 내용어 둘(용량, 기다려야~기다)
        self.assertNotIn(f, hits)                                 # 기능 어절만 겹친 꼬리표는 적중도 아니다
        audit = {h["obs_id"]: h for h in L.search_drawer(p, req, T, min_slots=1, include_function_words=True, log=False)}
        self.assertTrue(audit[f]["lexical_accident"])             # 기능어를 세는 감사 검색에서는 우연 적중으로 표시
        self.assertFalse(audit[o]["lexical_accident"])


if __name__ == "__main__":
    unittest.main()
