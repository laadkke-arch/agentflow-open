"""Refetch public immutable forum artifacts; persist metadata only, never original bodies."""
import concurrent.futures, datetime, hashlib, json, re, urllib.request
from pathlib import Path
BASE = Path(__file__).parent

def fetch(case_id, artifact_id):
    url = 'https://sqlite.org/forum/raw/' + artifact_id
    raw = urllib.request.urlopen(url, timeout=45).read()
    wm = re.search(rb'(?m)^W (\d+)\n', raw)
    if not wm:
        raise ValueError('No W body: '+artifact_id)
    body = raw[wm.end():wm.end()+int(wm[1])]
    cards = dict(re.findall(r'^([A-Z]) (.*)$', raw[:wm.start()].decode(), re.M))
    return dict(case_id=case_id, artifact_id=artifact_id, url=url,
      artifact_url='https://sqlite.org/forum/artifact/'+artifact_id,
      cards=cards, checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      raw_sha3_256=hashlib.sha3_256(raw).hexdigest(),
      id_matches_raw_sha3=hashlib.sha3_256(raw).hexdigest()==artifact_id,
      raw_sha256=hashlib.sha256(raw).hexdigest(),
      body_sha256=hashlib.sha256(body).hexdigest(), body_bytes=len(body),
      body_lines=len(body.decode().splitlines()),
      deleted_body=body.decode().strip()=='Deleted')

if __name__=='__main__':
    threads=json.loads((BASE/'thread-metadata.json').read_text())
    jobs=[(r['case_id'],x) for r in threads for x in r['artifact_ids']]
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        fs={pool.submit(fetch,*j):j for j in jobs}
        for f in concurrent.futures.as_completed(fs):
            try:
                r=f.result(); results.append(r)
                print(r['case_id'],r['artifact_id'][:12],r['cards'].get('D'),r['cards'].get('U'),r['body_lines'],flush=True)
            except Exception as exc:
                results.append(dict(case_id=fs[f][0],artifact_id=fs[f][1],error=str(exc)))
                print('FAILED',fs[f],str(exc),flush=True)
    results.sort(key=lambda r:(r['case_id'],r.get('cards',{}).get('D','')))
    (BASE/'followup-metadata.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
