"""Fetch only an issue's title/body; never fetch comments or linked fixes."""
import csv
import datetime
import hashlib
import json
from pathlib import Path
import sys
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
row = next(r for r in csv.DictReader((ROOT / 'frame.csv').open()) if r['frame_id'] == sys.argv[1])
project = row['project']
number = row['issue_number']
repositories = {'jupyterlab': 'jupyterlab/jupyterlab', 'home_assistant': 'home-assistant/core', 'godot': 'godotengine/godot'}
if project in repositories:
    url = f'https://api.github.com/repos/{repositories[project]}/issues/{number}'
else:
    repository = {'inkscape': 'inkscape/inbox', 'kicad': 'kicad/code/kicad'}[project]
    url = f'https://gitlab.com/api/v4/projects/{urllib.parse.quote(repository, safe="")}/issues/{number}'
observed = datetime.datetime.now(datetime.timezone.utc).isoformat()
with urllib.request.urlopen(url, timeout=25) as response:
    data = json.load(response)
body = data.get('body', data.get('description', '')) or ''
author = data.get('user', data.get('author', {}))
receipt = {'frame_id': row['frame_id'], 'url': data.get('html_url', data.get('web_url')), 'request_url': url,
           'observed_utc': observed, 'created_at': data['created_at'], 'updated_at': data['updated_at'],
           'state': data['state'], 'author': author.get('login', author.get('username')), 'author_type': author.get('type'),
           'author_bot': author.get('bot'), 'body_sha256': hashlib.sha256(body.encode()).hexdigest(),
           'title': data['title'], 'body_line_count': len(body.splitlines()), 'original_version_verified': False,
           'revision_fields': {k: v for k, v in data.items() if any(s in k for s in ['edited', 'changed', 'revision'])},
           'revision_limitation': 'Observed body only; updated_at includes other issue events. Comments and links not fetched.'}
with (ROOT / 'evidence/body-observations.jsonl').open('a') as stream:
    stream.write(json.dumps(receipt, ensure_ascii=False) + '\n')
print(json.dumps(receipt, ensure_ascii=False, indent=2))
print('\n'.join(f'L{n}: {line}' for n, line in enumerate(body.splitlines(), 1)))
