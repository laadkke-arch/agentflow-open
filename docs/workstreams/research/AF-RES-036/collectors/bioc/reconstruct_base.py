"""Refetch exact archive/member and validate the committed B excerpt.

Run from repository root: python -B docs/workstreams/research/AF-RES-036/collectors/bioc/reconstruct_base.py R01
No current destination is fetched. Outputs remain beneath this collector.
"""
from pathlib import Path
import hashlib, io, json, sys, tarfile
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parents[1]/'scripts'))
from fetchlib import fetch,utc
from html_extract import extract

def sha(b):return hashlib.sha256(b).hexdigest()
refs=[json.loads(x) for x in (P/'references.jsonl').read_text().splitlines()]
ids=sys.argv[1:] or [x['ref_id'] for x in refs]
results=[]
for row in refs:
 if row['ref_id'] not in ids:continue
 rid=row['ref_id'];d=P/'reconstruction'/rid;d.mkdir(parents=True,exist_ok=True)
 body,receipt=fetch(row['original_distribution_url'],d,'REPLAY-B-'+rid,'original_distribution_reconstruction',case_ids=[rid],save_name='archive.tar.gz')
 assert receipt['status']==200,(rid,receipt)
 assert sha(body)==row['archive_sha256'],rid+' archive hash changed'
 with tarfile.open(fileobj=io.BytesIO(body),mode='r:gz') as t:member=t.extractfile(row['member']).read()
 assert sha(member)==row['member_sha256'],rid+' member hash changed'
 path=d/'member.html';path.write_bytes(member)
 text=extract(path)['text']
 assert sha(text.encode())==row['clean_text_sha256'],rid+' parser/text changed'
 excerpt=text[row['clean_text_start']:row['clean_text_end']]
 assert sha(excerpt.encode())==row['context_sha256'],rid+' excerpt changed'
 assert excerpt==row['context'],rid+' context mismatch'
 results.append({'ref_id':rid,'verified_utc':utc(),'archive_member_text_and_excerpt_match':True,'receipt':receipt})
(P/'reconstruction'/'receipt.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps({'rows':len(results),'all_matched':True}))
