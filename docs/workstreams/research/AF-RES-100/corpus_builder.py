"""Build a fixed primary-source corpus without displaying its bodies to a reader.

Only official source archives are fetched. This preparation is charged separately
from the route-level four file attempts. No archive commands are executed.
"""
from pathlib import Path, PurePosixPath
import argparse, datetime, fnmatch, hashlib, io, json, tarfile, urllib.request, urllib.parse

ROOT = Path(__file__).resolve().parent

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def build():
    plan = json.loads((ROOT / 'corpus-plan.json').read_text())
    records, receipts = [], []
    for item in plan['repositories']:
        label = item['label']
        cache = ROOT / 'evidence/_cache/corpora' / label
        cache.mkdir(parents=True, exist_ok=True)
        url = item['archive_url']
        receipt = {'label': label, 'url': url, 'started_utc': now(),
                   'cost_class': 'preconstruction; no route contribution',
                   'bodies_shown_to_researcher': False}
        archive = cache / 'source.tar'
        try:
            if archive.exists():
                data = archive.read_bytes()
                receipt['cache_reuse'] = True
            else:
                request = urllib.request.Request(url, headers={'User-Agent': 'AF-RES-100-public-research'})
                with urllib.request.urlopen(request, timeout=60) as response:
                    data = response.read()
                    receipt['status'] = response.status
                    receipt['resolved_url'] = response.geturl()
                archive.write_bytes(data)
            receipt['archive_sha256'] = sha(data)
            receipt['download_bytes'] = len(data)
            skipped = {'out_of_scope': 0, 'binary_or_encoding': 0, 'too_large': 0,
                       'nonregular': 0}
            selected = []
            with tarfile.open(fileobj=io.BytesIO(data), mode='r:*') as tf:
                for entry in tf.getmembers():
                    if not entry.isfile():
                        skipped['nonregular'] += 1
                        continue
                    parts = PurePosixPath(entry.name).parts[1:]
                    if not parts or '..' in parts:
                        continue
                    rel = '/'.join(parts)
                    if not any(fnmatch.fnmatchcase(rel, g) for g in item['include']):
                        skipped['out_of_scope'] += 1
                        continue
                    if any(fnmatch.fnmatchcase(rel, g) for g in item.get('exclude', [])):
                        skipped['out_of_scope'] += 1
                        continue
                    if entry.size > plan['max_file_bytes']:
                        skipped['too_large'] += 1
                        continue
                    raw = tf.extractfile(entry).read()
                    try:
                        text = raw.decode('utf-8')
                        if '\x00' in text:
                            raise UnicodeError('NUL')
                    except UnicodeError:
                        skipped['binary_or_encoding'] += 1
                        continue
                    target = cache / 'files' / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(raw)
                    selected.append({'repo': item['repo'], 'label': label, 'path': rel,
                                     'version': item['version'], 'commit': item.get('commit'),
                                     'published_utc': item['published_utc'],
                                     'sha256': sha(raw), 'bytes': len(raw),
                                     'line_count': len(text.splitlines()),
                                     'url': item['file_url_template'].replace('{path}', urllib.parse.quote(rel, safe='/')),
                                     'archive_url': url,
                                     'cached_body': str(target.relative_to(ROOT))})
            for idx, row in enumerate(sorted(selected, key=lambda r: r['path']), 1):
                row['file_id'] = f'{label}-{idx:04}'
                records.append(row)
            receipt.update({'included_files': len(selected), 'excluded': skipped,
                            'status_summary': 'success'})
        except Exception as exc:
            receipt.update({'status_summary': 'failed', 'error': f'{type(exc).__name__}: {exc}'})
        receipt['finished_utc'] = now()
        receipts.append(receipt)
        print(json.dumps({k: receipt.get(k) for k in
                          ['label', 'status_summary', 'included_files', 'download_bytes', 'error']}), flush=True)
        dump(ROOT / 'evidence/corpus-build-receipts.json', receipts)
    records.sort(key=lambda r: (r['repo'], r['path']))
    out = ROOT / 'corpus-files.jsonl'
    out.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in records))
    dump(ROOT / 'evidence/corpus-manifest.json',
         {'built_utc': now(), 'files': len(records), 'corpus_file_sha256': sha(out.read_bytes()),
          'plan_sha256': sha((ROOT / 'corpus-plan.json').read_bytes()),
          'construction_only': True, 'researcher_body_exposure': False,
          'total_download_bytes': sum(r.get('download_bytes', 0) for r in receipts),
          'failed_repositories': [r['label'] for r in receipts if r['status_summary'] != 'success']})

if __name__ == '__main__':
    build()
