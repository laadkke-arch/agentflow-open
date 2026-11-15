"""A bounded, dependency-free check of the shared workbench, not a product test."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import date
from urllib.parse import urlsplit

REQUIRED = ('AGENTS.md', 'STATE.md', 'docs/WORKBENCH.md', 'workbench/sources.json')


def validate_sources(records):
    if not isinstance(records, list) or not records:
        raise ValueError('sources must be a nonempty list')
    seen = set()
    for item in records:
        if not isinstance(item, dict):
            raise ValueError('each source must be an object')
        for key in ('id', 'url', 'checked_on', 'evidence', 'decision', 'note'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError('source requires nonempty ' + key)
        if item['id'] in seen:
            raise ValueError('duplicate source id')
        seen.add(item['id'])
        url = urlsplit(item['url'])
        if url.scheme != 'https' or not url.hostname or url.username or url.password:
            raise ValueError('source URL must be HTTPS without credentials')
        date.fromisoformat(item['checked_on'])
        if item['evidence'] not in ('official_documentation', 'partial_search_only'):
            raise ValueError('invalid evidence level')
        if item['decision'] not in ('adopt', 'reference', 'defer'):
            raise ValueError('invalid decision')
    return len(records)


def inspect(root):
    for name in REQUIRED:
        if not (root / name).read_text(encoding='utf-8').strip():
            raise ValueError('empty required file: ' + name)
    raw = (root / 'workbench/sources.json').read_bytes()
    count = validate_sources(json.loads(raw))
    probe = json.loads((root / 'workbench/probe.json').read_text(encoding='utf-8'))
    if probe != {'challenge': 'agentflow-workbench-roundtrip-001', 'scope': 'environment-only'}:
        raise ValueError('unexpected probe; no arbitrary task execution is allowed')
    commit = subprocess.run(
        ['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True,
        text=True, timeout=5, check=True,
    ).stdout.strip()
    return {
        'status': 'passed', 'scope': probe['scope'], 'challenge': probe['challenge'],
        'commit': commit, 'run_id': os.environ.get('GITHUB_RUN_ID'),
        'checked_files': list(REQUIRED), 'source_count': count,
        'sources_sha256': hashlib.sha256(raw).hexdigest(),
        'limitation': 'Structure checked; source truth, product and deployment NOT tested.',
    }


def main():
    try:
        receipt = inspect(Path(__file__).resolve().parents[1])
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print('WORKBENCH_FAILED: ' + str(exc), file=sys.stderr)
        return 1
    print('WORKBENCH_RECEIPT=' + json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
