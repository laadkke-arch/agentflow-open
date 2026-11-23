import random
import unittest

from select_passages import (
    candidate_pairs, first_window, make_segment, normalized_with_origins,
    occurrences, split_window, unique_token_masks,
)


class SelectionBoundaries(unittest.TestCase):
    def test_legacy_raw_after_two_hundred_context(self):
        text = "." * 350 + "JOIN" + "." * 1500
        self.assertEqual(first_window(text, [{"join"}, {"null"}]), ((150, 1350), 350))

    def test_legacy_no_raw_match_and_late_anchor_shortens(self):
        text = "." * 1400 + "ＪＯＩＮ"
        self.assertEqual(first_window(text, [{"join"}, {"null"}]), ((0, 1200), None))
        self.assertEqual(occurrences(text, {"join"}), [(1400, 1404, "join")])
        self.assertEqual(first_window("." * 350 + "JOIN", [{"join"}, set()]), ((150, 354), 350))

    def test_multibyte_crlf_and_ligature_coordinates(self):
        text = "🧪\r\nＡ ﬃ ß 가 A\u0315\u0300"
        self.assertEqual(normalized_with_origins(text)[0], "🧪\r\na ffi ss 가 à\u0315")
        self.assertEqual(occurrences(text, {"a", "ffi", "ss"}), [(3, 4, "a"), (5, 6, "ffi"), (7, 8, "ss")])
        self.assertEqual(make_segment(text.encode(), text, 1, 6)["utf8"], [4, 13])

    def test_token_must_fit_inside_one_segment(self):
        hits = [(2, 6, "sort")]
        self.assertEqual(unique_token_masks([0, 2, 4], 4, hits, {"sort": 1}), {0: 0, 2: 1, 4: 0})

    def test_zero_one_equal_and_odd_width_orientation(self):
        q = [set(), set()]
        self.assertEqual(split_window("x", q, (0, 1))[0], [(0, 1)])
        self.assertEqual(split_window("", q, (0, 0))[0], [(0, 0)])
        self.assertEqual(split_window("12345678", q, (0, 8))[0], [(0, 4), (4, 8)])
        self.assertEqual(split_window("a xz ", [{"a"}, {"xz"}], (0, 5))[0], [(0, 2), (2, 5)])

    def test_candidate_adjacency_and_file_edge(self):
        left, right = candidate_pairs(300, 20, 21, [(151, 155, "edge")])
        self.assertEqual((left, right), ([0, 31, 51, 259, 280], [0, 20, 51, 71, 279]))
        self.assertEqual(split_window("a" + " " * 800 + "b", [{"a"}, {"b"}], (0, 200))[1]["objective"], [1, 2])

    def test_matches_reference_enumeration_and_ties(self):
        rng = random.Random(104)
        for _ in range(36):
            text = " ".join(rng.choices(["x", "a", "b", "bb", "abc"], k=90))
            queries = [{"a", "bb"}, {"b", "bb"}]
            all_hits = occurrences(text, set.union(*queries))
            expected = []
            budget = rng.randrange(2, 25)
            for a in {budget // 2, (budget + 1) // 2}:
                b = budget - a
                starts, ends = candidate_pairs(len(text), a, b, all_hits)
                for x in starts:
                    for y in ends:
                        if x + a <= y:
                            found = {term for lo, hi, term in all_hits
                                     if x <= lo < hi <= x + a or y <= lo < hi <= y + b}
                            m, n = [len(q & found) for q in queries]
                            expected.append((-min(m, n), -(m+n), x, y, a, b))
            _, _, x, y, a, b = min(expected)
            self.assertEqual(split_window(text, queries, (0, budget))[0], [(x, x+a), (y, y+b)])


if __name__ == "__main__":
    unittest.main()
