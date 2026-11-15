import unittest
from task import collect
from workbench.urls import RepositoryURL, repository_key


class RepositoryIdentityTests(unittest.TestCase):
    def test_clone_aliases(self):
        aliases = ['https://github.com/Python/CPython',
                   'http://github.com/python/cpython/',
                   'https://github.com/python/cpython.git/',
                   'git@github.com:python/cpython.git',
                   'ssh://git@github.com/python/cpython.git',
                   'https://github.com:443/python/cpython']
        for value in aliases:
            with self.subTest(value=value):
                self.assertEqual(repository_key(value), 'github.com/python/cpython')

    def test_reject_ambiguous_or_deceptive(self):
        cases = ['', None, 12, 'https://github.com/a/b/issues/1',
                 'https://github.com.evil.invalid/a/b', 'https://evil.invalid/a/b',
                 'https://github.com@evil.invalid/a/b', 'https://user@github.com/a/b',
                 'https://@github.com/a/b', 'ssh://git:@github.com/a/b',
                 'https://github.com/a/b?', 'https://github.com/a/b#',
                 'https://github.com/a/b?x=1', 'https://github.com/a/b#readme',
                 'https://github.com/a/%62', 'https://github.com/a/b//',
                 'https://github.com/a/..', 'https://github.com/a/.git',
                 'https://github.com:8443/a/b', 'https://github.com:xyz/a/b',
                 'file:///a/b', '//github.com/a/b', ' https://github.com/a/b',
                 'https://git\nhub.com/a/b', 'https://github.com/a/\\b',
                 'https://github.com/a/b\x00', 'https://github.com/a/b\x7f']
        for value in cases:
            with self.subTest(value=value):
                with self.assertRaises(RepositoryURL):
                    repository_key(value)

    def test_idempotent_canonical_identity(self):
        for owner in ('A', 'python', 'some-owner'):
            for repo in ('R', 'dot.name', 'under_score', 'a-b'):
                key = repository_key(f'https://github.com/{owner}/{repo}')
                self.assertEqual(repository_key('https://' + key), key)

    def test_distinct_owner_not_merged(self):
        self.assertNotEqual(repository_key('https://github.com/a/repo'), repository_key('https://github.com/b/repo'))

    def test_collect_preserves_indices(self):
        result = collect(['https://github.com/a/b', 'git@github.com:a/b.git', 'https://github.com/a/b/issues'])
        self.assertEqual(result['repositories'], [{'key':'github.com/a/b','input_indices':[0,1]}])
        self.assertEqual(result['rejected'][0]['index'], 2)
        self.assertFalse(result['existence_checked'])

    def test_rejected_credentials_not_echoed(self):
        self.assertNotIn('private-password', str(collect(['https://user:private-password@github.com/a/b'])))

    def test_bad_input_container(self):
        for value in (None, {}, 'https://github.com/a/b', [0]*10001):
            with self.assertRaises(ValueError):
                collect(value)


if __name__ == '__main__':
    unittest.main()
