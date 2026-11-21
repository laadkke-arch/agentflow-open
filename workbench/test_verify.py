import unittest
from verify import validate_sources


class SourceValidationTests(unittest.TestCase):
    def item(self, **changes):
        item = dict(id='sample', url='https://example.org/docs', checked_on='2026-11-15',
                    evidence='official_documentation', decision='reference', note='Test fixture.')
        item.update(changes)
        return item

    def test_valid(self):
        self.assertEqual(validate_sources([self.item()]), 1)

    def test_empty(self):
        with self.assertRaises(ValueError):
            validate_sources([])

    def test_duplicate(self):
        with self.assertRaises(ValueError):
            validate_sources([self.item(), self.item()])

    def test_invalid_urls(self):
        for url in ('file:///etc/passwd', 'http://example.org', 'https://user:pass@example.org'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_sources([self.item(url=url)])

    def test_invalid_evidence(self):
        with self.assertRaises(ValueError):
            validate_sources([self.item(evidence='executed_but_not_really')])

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            validate_sources([self.item(checked_on='yesterday')])


if __name__ == '__main__':
    unittest.main()
