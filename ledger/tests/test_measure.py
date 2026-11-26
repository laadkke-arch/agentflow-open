"""측정 결과 파일과 설정이 서로 맞는지 지킨다(측정을 바꾸면 결과 파일을 다시 쓴다)."""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from afledger import config, privacy  # noqa: E402

OUT = HERE.parent / "out"


def load(name):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


class MeasuredChoices(unittest.TestCase):
    def test_privacy_default_is_the_measured_choice(self):
        r = load("measure_r4.json")
        chosen = r["variants"][r["chosen"]]
        self.assertEqual(config.PRIVACY_RULES, "p2")
        self.assertEqual((privacy.KO_TOKEN_RULE, privacy.VERBATIM_CHARS),
                         (chosen.get("KO_TOKEN_RULE", True), chosen["VERBATIM_CHARS"]))
        self.assertEqual(chosen["leak_passed"], 0)
        self.assertLess(chosen["legit_reject_rate"], 0.05)

    def test_r6_choice_matches_config(self):
        r = load("measure_r6.json")
        v = r["variants"][r["chosen"]]
        self.assertEqual((config.RANK_RULES, config.RANK_LENGTH_B, config.DRAWER_SYMBOL_SCOPE),
                         (v["rank_rules"], v["length_b"], v["symbol_scope"]))
        self.assertTrue(v["T1_flow"] and v["T2"] and v["T3"])

    def test_a4_and_maps_are_recorded(self):
        a = load("measure_a4.json")
        self.assertFalse(a["variants"]["i1_en@t2"]["catalog_only"]["big_deviation"])
        self.assertEqual(set(a["r1_flow_with_i1_ko"]), {"t1_catalog_only", "t1_with_F01", "t2_catalog_only", "t2_with_F01"})
        b = load("measure_b1.json")["modes"]
        self.assertGreaterEqual(b["t2"]["reached"], b["t1"]["reached"])
        m = load("measure_r1_map.json")
        self.assertEqual(m["total"]["agree"], m["total"]["positions"])
        n = load("measure_normalize.json")
        self.assertEqual(n["errors"], {})


if __name__ == "__main__":
    unittest.main()
