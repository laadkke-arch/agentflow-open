"""07 R-6: 서랍 순위 r2(단위별 IDF + 꼬리표 길이 정규화)와 사용자 판 확인 범위(마지막 수단, 08 I18)."""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from afledger import Ledger, config  # noqa: E402

T = "2026-11-26T00:00:00Z"


class RankR2(unittest.TestCase):
    def scores(self, rank):
        """같은 낱말을 꼬리표 셋에 나눠 가진 관측(F01 행처럼 여러 행이 한 관측으로 합쳐진 경우)과 꼬리표 하나인 관측."""
        L = Ledger()
        L.rank_rules = rank
        text = "작업 허가를 얻고 용량이 돌아올 때까지 기다린다"
        one, _ = L.observe(url="https://example.org/one", edition_key="v1", edition_kind="fetch", position="§", at=T,
                           method="intro_only", statement="하나")
        L.tag(one, "summary", "one_up", "ko", text)
        many, _ = L.observe(url="https://example.org/many", edition_key="v1", edition_kind="fetch", position="§", at=T,
                            method="intro_only", statement="여럿")
        for i, h in enumerate(("one_up", "concrete")):
            L.tag(many, "summary", h, "ko", text)
        L.tag(many, "summary", "one_up", "mixed", text + " ")
        for i in range(6):   # IDF가 0이 되지 않게 다른 글도 둔다
            o, _ = L.observe(url=f"https://example.org/x{i}", edition_key="v1", edition_kind="fetch", position="§",
                             at=T, method="intro_only", statement="x")
            L.tag(o, "summary", "one_up", "ko", f"관련 없는 운영 기록 {i}")
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at=T, text="t", selected_part="s", requirements=[],
                       needs=[{"slot": "keeps", "lang": "ko", "text": "용량 회복"},
                              {"slot": "breaks_when", "lang": "ko", "text": "기다려야 한다"}])
        return {h["obs_id"]: h["score"] for h in L.search_drawer(p, req, T, k=50, log=False)}, one, many

    def test_repeated_tags_do_not_multiply_the_score(self):
        self.assertEqual(config.RANK_RULES, "r2")
        s0, one, many = self.scores("r0")
        self.assertLess(s0[many], s0[one])                     # 설계 순위(bm25 합)는 꼬리표 행마다 더해 앞선다
        s2, one, many = self.scores("r2")
        self.assertAlmostEqual(s2[many], s2[one])              # r2는 맞은 단위마다 한 번만 센다

    def test_symbol_scope_is_the_recorded_last_resort(self):
        self.assertEqual(config.DRAWER_SYMBOL_SCOPE, "eligible")


if __name__ == "__main__":
    unittest.main()
