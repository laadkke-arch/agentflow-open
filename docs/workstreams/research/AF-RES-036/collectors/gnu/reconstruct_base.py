"""Rebuild sealed B text from a measured original archive. No package execution."""
import argparse,hashlib,io,json,sys,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));from parse_html import parse
sys.path.insert(0,str(ROOT.parents[1]/'scripts'));from fetchlib import fetch
def sha(b):return hashlib.sha256(b).hexdigest()
def extract(raw,archive,member):
    if archive.endswith('.deb'):
        offset=8
        while offset<len(raw):
            h=raw[offset:offset+60];name=h[:16].decode().strip().rstrip('/');size=int(h[48:58]);body=raw[offset+60:offset+60+size];offset+=60+size+(size%2)
            if name.startswith('data.tar'):raw=body;break
    with tarfile.open(fileobj=io.BytesIO(raw)) as tf:return tf.extractfile(member).read()
ap=argparse.ArgumentParser();ap.add_argument('--download-missing',action='store_true');args=ap.parse_args()
rows=[json.loads(l) for l in (ROOT/'references.jsonl').read_text().splitlines()];out=[];memo={}
for r in rows:
    name=r['archive_url'].rsplit('/',1)[-1]
    if name not in memo:
        path=ROOT/name
        if path.exists():raw=path.read_bytes()
        elif args.download_missing:
            raw,receipt=fetch(r['archive_url'],ROOT/'replay',r['reference_id']+'-REBUILD','reconstruct_original_B',[r['reference_id']],name)
        else:raise SystemExit('Missing '+name+'; use --download-missing for an actual measured reacquisition')
        assert sha(raw)==r['archive_sha256'],name;memo[name]=raw
    member=extract(memo[name],name,r['member']);assert sha(member)==r['member_sha256']
    path=ROOT/'replay'/('member-'+r['reference_id']+'.html');path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(member)
    d=parse(path);assert sha(d['text'].encode())==r['text_location']['normalized_text_sha256']
    loc=r['text_location'];excerpt=d['text'][loc['start_char']:loc['end_char']]
    assert sha(excerpt.encode())==r['context_sha256'];assert excerpt==(ROOT/'base'/(r['reference_id']+'.txt')).read_text()
    out.append({'reference_id':r['reference_id'],'archive_sha256':r['archive_sha256'],'member_sha256':r['member_sha256'],'B_context_sha256':r['context_sha256'],'context_bytes':len(excerpt.encode()),'matched':True})
print(json.dumps({'check':'original archive → member → normalized offsets → exact B text','physical_archive_reads':len(memo),'logical_references':len(rows),'rows':out},ensure_ascii=False,indent=2))
