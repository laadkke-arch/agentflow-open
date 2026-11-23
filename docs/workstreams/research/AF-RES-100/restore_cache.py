"""Restore registered source bytes, without changing a sealed ledger or printing bodies.

This is acquisition, not evidence reading. Existing differing cache bytes are rejected.
Run hydrate_ledgers.py first. --all restores the full ranking corpus; default restores
the 31 registered packet files. Original question revision bodies are always restored.
"""
from pathlib import Path, PurePosixPath
import argparse, concurrent.futures, datetime, hashlib, io, json, tarfile, urllib.request

ROOT = Path(__file__).resolve().parent

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'AF-RES-100-public-research'})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read(), response.geturl(), response.status

def install(path, raw, expected):
    if sha(raw) != expected:
        raise ValueError('source digest differs: ' + str(path))
    if path.exists() and path.read_bytes() != raw:
        raise ValueError('refusing to replace differing cache: ' + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)

def restore_repo(item, records):
    receipt = {'label': item['label'], 'url': item['archive_url'], 'started_utc': now(),
               'purpose': 'restore already sealed bytes; no new ranking or reading',
               'bodies_displayed': False}
    try:
        if all((ROOT / r['cached_body']).exists() and sha((ROOT / r['cached_body']).read_bytes()) == r['sha256'] for r in records):
            receipt.update(ok=True, restored_files=len(records), verified_existing_cache=True, finished_utc=now())
            return receipt
        raw, resolved, status = fetch(item['archive_url'])
        receipt.update(status=status, resolved_url=resolved, archive_sha256=sha(raw), archive_bytes=len(raw))
        wanted = {r['path']: r for r in records}
        count = 0
        with tarfile.open(fileobj=io.BytesIO(raw), mode='r:*') as archive:
            for member in archive:
                if not member.isfile():
                    continue
                name = '/'.join(PurePosixPath(member.name).parts[1:])
                if name not in wanted:
                    continue
                r = wanted[name]
                body = archive.extractfile(member).read()
                install(ROOT / r['cached_body'], body, r['sha256'])
                count += 1
        if count != len(wanted):
            raise ValueError(f'archive files restored {count} != registered {len(wanted)}')
        receipt.update(ok=True, restored_files=count)
    except Exception as exc:
        receipt.update(ok=False, error=f'{type(exc).__name__}: {exc}')
    receipt['finished_utc'] = now()
    return receipt

def restore_question(case):
    url = case.get('r0_api_url') or ('https://api.stackexchange.com/2.3/revisions/' + case['r0_guid'] + '?site=stackoverflow&filter=%211emQP-6jyLbLgZ0cpDxNT%281d')
    assignment = next(c for c in json.loads((ROOT / 'evidence/assignments/reader-1.json').read_text())['packets'] if c['case_id'] == case['case_id'])
    expected = assignment['r0_body_sha256']
    receipt = {'case_id': case['case_id'], 'url': url, 'started_utc': now(),
               'purpose': 'restore exact original revision; answers not requested', 'bodies_displayed': False}
    try:
        raw, resolved, status = fetch(url)
        items = json.loads(raw)['items']
        revision = next(r for r in items if r.get('revision_guid', '').casefold() == case['r0_guid'].casefold() and 'body' in r)
        body = revision['body'].encode('utf-8')
        install(ROOT / 'evidence/_cache/requests' / f"{case['question_id']}.html", body, expected)
        if case.get('r0_cache_path'):
            install(ROOT / case['r0_cache_path'], body, expected)
        receipt.update(ok=True, status=status, payload='items[matching revision_guid].body',
                       body_sha256=sha(body), body_chars=len(revision['body']), body_bytes=len(body),
                       revision_guid=revision['revision_guid'], revision_number=revision.get('revision_number'))
    except Exception as exc:
        receipt.update(ok=False, error=f'{type(exc).__name__}: {exc}')
    receipt['finished_utc'] = now()
    return receipt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    records = [json.loads(s) for s in (ROOT / 'corpus-files.jsonl').read_text().splitlines()]
    packets = [json.loads(s) for s in (ROOT / 'packets.jsonl').read_text().splitlines()]
    needed = {s['file_id'] for p in packets for s in p['slots'] if not s['empty']}
    if not args.all:
        records = [r for r in records if r['file_id'] in needed]
    plan = json.loads((ROOT / 'corpus-plan.json').read_text())
    cases = json.loads((ROOT / 'protocol.json').read_text())['cases']
    receipts = []
    output = ROOT / 'evidence/resume-cache-receipts.json'
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(restore_repo, r, [f for f in records if f['label'] == r['label']]) for r in plan['repositories']]
        futures += [pool.submit(restore_question, case) for case in cases]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            receipts.append(result)
            output.write_text(json.dumps(receipts, ensure_ascii=False, indent=2) + '\n')
            print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0 if all(r['ok'] for r in receipts) else 1

if __name__ == '__main__':
    raise SystemExit(main())
