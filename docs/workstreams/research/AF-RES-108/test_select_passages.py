import unittest

from select_passages import HTMLBody, choose, exception_spans, extract_web, occurrences


class SelectorTest(unittest.TestCase):
    def test_unicode_origin(self):
        self.assertEqual(occurrences("ＷＩＤＴＨ ß", {"width", "ss"}), [(0, 5, "width"), (6, 7, "ss")])

    def test_sentence_stops_and_whole_tokens(self):
        source = "Prior excepted word. Unless width fits? Otherwise height fits! Exceptable width."
        hits = occurrences(source, {"width"})
        actual = [source[a:b] for a, b, _ in exception_spans(source, [(0, len(source), "prose")], hits)]
        self.assertEqual(actual, ["Unless width fits?"])

    def test_markup_boundaries(self):
        source, blocks, _ = HTMLBody("<body><ul><li>Unless width set</li><li>width set</li></ul>"
                                    "<pre>Otherwise width</pre><p>Width otherwise set.</p>"
                                    "<table><tr><td>Except width</td></tr></table></body>").stream.finish()
        hits = occurrences(source, {"width"})
        actual = [source[a:b] for a, b, _ in exception_spans(source, blocks, hits)]
        self.assertEqual(actual, ["Unless width set", "Width otherwise set."])

    def test_web_list_code_and_links(self):
        source, blocks, origin = extract_web("  * Unless 【1†width】 fits\n    code: otherwise width\n"
                                             "```\nexcept width\n```\n", "generic")
        hits = occurrences(source, {"width"})
        actual = [source[a:b] for a, b, _ in exception_spans(source, blocks, hits)]
        self.assertEqual(actual, ["Unless width fits"])
        self.assertTrue(any(x[3] == "web-link-label" for x in origin))

    def test_one_character_and_empty(self):
        for source in ("", "a"):
            selection, data = choose(source, [(0,len(source),"prose")], [["a"],["a"]])
            self.assertTrue(data["fallback"])
            self.assertEqual(selection, {"K":[(0,0),(0,len(source))],"E":[(0,0),(0,len(source))]})

    def test_same_candidates_and_displacement(self):
        source = "width unit " + "a "*720 + ". width unless unit applies. " + "b "*340
        selection, data = choose(source, [(0,len(source),"prose")], [["width"],["unit"]])
        self.assertEqual(data["n"],1200)
        self.assertNotEqual(selection["K"],selection["E"])
        self.assertTrue(all(b - a == 600 for arm in selection.values() for a, b in arm))
        self.assertTrue(data["orientations"][0]["exception_qualified_pairs"])


if __name__ == "__main__":
    unittest.main()
