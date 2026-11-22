import json, urllib.request, hashlib, datetime, pathlib, concurrent.futures, re
ROOT = pathlib.Path(__file__).resolve().parent

def fetch(url, name):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(url, timeout=35) as response:
            body = response.read()
            receipt = {'url': url, 'checked_utc': now, 'status': response.status, 'response_headers': dict(response.headers)}
        path = ROOT / 'raw' / name
        path.write_bytes(body)
        receipt.update(sha256=hashlib.sha256(body).hexdigest(), path=str(path.relative_to(ROOT)))
    except Exception as error:
        body = b''
        receipt = {'url': url, 'checked_utc': now, 'error': type(error).__name__ + ': ' + str(error)}
    return receipt, body

if __name__ == '__main__':
    data = json.loads((ROOT/'raw/ledger-directory.json').read_text())
    rows = [x for x in data if re.match(r'nep-\d+.*\.rst$', x['name'])]
    metadata, receipts = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(fetch, x['download_url'], 'current-header-source-' + x['name']):x for x in rows}
        for future in concurrent.futures.as_completed(futures):
            row = futures[future]
            receipt, body = future.result()
            receipts.append(receipt)
            lines = body.decode().splitlines()
            title = next((line for line in lines if re.match(r'NEP \d+', line)), '')
            created = next((line for line in lines if line.startswith(':Created:')), '')
            typ = next((line for line in lines if line.startswith(':Type:')), '')
            metadata.append({'canonical_id': 'NEP-' + str(int(re.search(r'nep-(\d+)',row['name']).group(1))), 'name':row['name'], 'path':row['path'], 'blob_sha_current':row['sha'], 'title':title, 'created_header_current':created, 'type_header_current':typ, 'raw_path':receipt.get('path'), 'retrieval_error': receipt.get('error')})
    with (ROOT/'attempts.jsonl').open('a') as output:
        for receipt in sorted(receipts,key=lambda x:x['url']):
            output.write(json.dumps(receipt)+'\n')
    metadata.sort(key=lambda x:int(x['canonical_id'].split('-')[1]))
    (ROOT/'official-ledger-headers.json').write_text(json.dumps(metadata, indent=2)+'\n')
    for item in metadata:
        print(item['canonical_id'], item['title'], item['created_header_current'], item['type_header_current'], item['retrieval_error'] or '')
