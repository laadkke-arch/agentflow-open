#!/usr/bin/env python3
"""Preserve research captures losslessly in bounded deterministic archives."""
from pathlib import Path
import gzip,hashlib,io,json,tarfile
OWN=Path(__file__).resolve().parent.parent
GROUPS={
 'pandoc-reference':['gold-work/pandoc/snapshots','gold-work/pandoc/excerpts'],
 'imagemagick-text':['gold-work/imagemagick/snapshots'],
 'imagemagick-inputs':['gold-work/imagemagick/attachments'],
 'archive-examples':['analogies/eisenhower'],
}

def pack(files):
    buf=io.BytesIO()
    with tarfile.open(fileobj=buf,mode='w') as tar:
        for f in files:
            data=f.read_bytes();info=tarfile.TarInfo(str(f.relative_to(OWN)))
            info.size=len(data);info.mtime=0;info.mode=0o644;tar.addfile(info,io.BytesIO(data))
    return gzip.compress(buf.getvalue(),mtime=0)

def main():
    out=OWN/'evidence/reference-cache';out.mkdir(exist_ok=True)
    entries=[];archives=[]
    for label,dirs in GROUPS.items():
        files=sorted(f for d in dirs for f in (OWN/d).rglob('*') if f.is_file())
        groups=[];current=[];size=0
        # Bound raw per group where possible; single original PDF may exceed it.
        for f in files:
            n=f.stat().st_size
            if current and size+n>4_000_000:groups.append(current);current=[];size=0
            current.append(f);size+=n
        if current:groups.append(current)
        for n,group in enumerate(groups,1):
            dest=out/f'{label}-{n:02}.tar.gz';raw=pack(group)
            if dest.exists() and dest.read_bytes()!=raw:raise ValueError('archive already differs: '+str(dest))
            dest.write_bytes(raw)
            archives.append({'path':str(dest.relative_to(OWN)),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'files':len(group)})
            for f in group:
                entries.append({'path':str(f.relative_to(OWN)),'archive':str(dest.relative_to(OWN)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
    index={'format':'tar.gz; each archive uses paths relative to owned root','rebuild':'python -B analysis/archive_references.py after extracting all parts under owned root','archives':archives,'files':entries,'capture_is_not_read':True,'actual_read_sections':'sources.jsonl and role-specific read logs','duplicate_original_and_extracted_files':'Retained for exact input reproducibility, counted once by source lineage.'}
    (out/'index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'archives':archives,'files':len(entries),'total_archive_bytes':sum(x['bytes'] for x in archives)},ensure_ascii=False))

if __name__=='__main__':main()
