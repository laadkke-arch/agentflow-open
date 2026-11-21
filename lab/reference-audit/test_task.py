import unittest
from task import audit


class ReferenceTests(unittest.TestCase):
    def test_valid_reference(self):
        result = audit('Used [source:one].', [{'id':'one','url':'https://github.com/a/b'}])
        self.assertTrue(result['ok'])
        self.assertFalse(result['claim_truth_checked'])
        self.assertFalse(result['network_accessed'])

    def test_missing_source(self):
        self.assertEqual(audit('[source:missing]', [])['errors'], ['missing-source:missing'])

    def test_duplicate_id(self):
        self.assertFalse(audit('', [{'id':'one'}, {'id':'one'}])['ok'])

    def test_invalid_id(self):
        self.assertFalse(audit('', [{'id':'../../escape'}])['ok'])

    def test_unused(self):
        self.assertEqual(audit('', [{'id':'one'}])['unused'], ['one'])

    def test_reuses_root_identity(self):
        result = audit('[source:one]', [{'id':'one','url':'https://github.com/A/B'},
                                      {'id':'two','url':'git@github.com:a/b.git'}])
        self.assertEqual(result['duplicate_repository_sources'], {'github.com/a/b':['one','two']})

    def test_does_not_collapse_subpages(self):
        result = audit('', [{'id':'one','url':'https://github.com/a/b/blob/main/README.md'},
                            {'id':'two','url':'https://github.com/a/b'}])
        self.assertEqual(result['duplicate_repository_sources'], {})

    def test_repeated_marker(self):
        self.assertEqual(audit('[source:one] [source:one]', [{'id':'one'}])['used'], ['one'])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            audit(None, [])


if __name__ == '__main__':
    unittest.main()
