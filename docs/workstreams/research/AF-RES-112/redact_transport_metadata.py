"""Remove expired public-download signing parameters without changing exposure.

The original recipient seal remains identifiable. This is a later metadata-only
derivative, never a claim that old whole-file hashes describe the derivative.
"""
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / 'evidence/transport-redaction.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sanitize(value, pointer='', records=None):
    if records is None:
        records = []
    if isinstance(value, dict):
        return {k: sanitize(v, pointer + '/' + k, records) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize(v, pointer + '/' + str(i), records) for i, v in enumerate(value)]
    if isinstance(value, str) and value.startswith(('https://', 'http://')):
        parts = urlsplit(value)
        names = [k for k, _ in parse_qsl(parts.query, keep_blank_values=True)]
        if any(k.lower().startswith('x-amz-') for k in names):
            assert not pointer.endswith('/exposed_text'), 'never alter seen source text'
            redacted = urlunsplit((parts.scheme, parts.netloc, parts.path, '', parts.fragment))
            records.append({'json_pointer': pointer, 'raw_url_sha256': digest(value.encode()),
                            'query_parameter_names': names, 'redacted_url': redacted})
            return redacted
    return value


def paths():
    repo = ROOT.parents[3]
    relative = ROOT.relative_to(repo)
    result = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard',
                             '--', str(relative)], cwd=repo, check=True, capture_output=True,
                            text=True)
    return [repo / name for name in sorted(set(result.stdout.splitlines()))
            if Path(name).suffix in ('.json', '.jsonl') and repo / name != RECEIPT]


def main(check):
    changes = []
    if not check and RECEIPT.exists():
        raise SystemExit('receipt exists: use --check; do not overwrite the original receipt')
    for path in paths():
        old = path.read_bytes()
        original = ([json.loads(s) for s in old.decode().splitlines() if s]
                    if path.suffix == '.jsonl' else json.loads(old))
        records = []
        clean = sanitize(original, records=records)
        if not records:
            continue
        if check:
            raise AssertionError('unredacted transport metadata: ' + str(path.relative_to(ROOT)))
        if path.suffix == '.jsonl':
            new = ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in clean).encode()
        else:
            new = (json.dumps(clean, ensure_ascii=False, indent=2) + '\n').encode()
        path.write_bytes(new)
        changes.append({'file': str(path.relative_to(ROOT)), 'before_sha256': digest(old),
                        'after_sha256': digest(new), 'redactions': records})
    if not check:
        data = {'created_at_utc': datetime.now(timezone.utc).isoformat(),
                'actor': 'root metadata cleanup after main receiver seal and control completion',
                'original_main_seal_commit': 'dd3c615dc8060a88259af6294848749d042d697f',
                'reason': 'expired signed redirects for public GitHub attachments are temporary transport metadata; remove their complete query from the working deliverable',
                'preserved': ['original stable URL', 'arrival host and path', 'fragment',
                              'HTTP redirect status', 'exposed_text', 'reader choices',
                              'judgments', 'archive hash', 'raw redirect URL SHA256'],
                'scope': 'metadata only; no history rewrite; original whole-file seal hashes describe the original commit, not this derivative',
                'files': changes}
        RECEIPT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': 'passed', 'mode': 'check' if check else 'redact',
                      'changed_files': len(changes)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    main(parser.parse_args().check)
