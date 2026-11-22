"""Reopen the Q1–Q7 anchors for self-review; never execute historical programs."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import io
import json
import tarfile
import urllib.request
import fitz

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT/'streams/root/cache/recheck'
CACHE.mkdir(parents=True, exist_ok=True)
items = [
    ('B01-P001','https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf','thanh2000.pdf'),
    ('B01-P004','https://tug.org/TUGboat/tb17-3/tb52sojk.pdf','sojka1996.pdf'),
    ('B01-P006','https://www.numdam.org/item/CG_1997___27_34_0.pdf','karow1997.pdf'),
    ('B01-P003','https://tug.org/TUGboat/tb22-3/tb72thanh.pdf','thanh2001.pdf'),
    ('B03-L001','https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz','lily101.tar.gz'),
    ('B03-L011','https://lilypond.org/download/sources/v0.1/lilypond-0.1.22.tar.gz','lily0122.tar.gz'),
    ('B03-L012','https://lilypond.org/download/sources/v0.1/lilypond-0.1.23.tar.gz','lily0123.tar.gz'),
    ('B01-P013','https://ftp.math.utah.edu/pub/tex/historic/systems/pdftex/pdftex-0.xx-web2c/web2c-7.3.3-pdftex-0.14f.tar.gz','pdftex014f.tar.gz'),
]
receipts=[]
for source_id,url,name in items:
    stamp=datetime.now(timezone.utc).isoformat()
    receipt=dict(source_id=source_id,url=url,checked_utc=stamp)
    try:
        with urllib.request.urlopen(url,timeout=25) as response:
            data=response.read()
            receipt.update(http_status=response.status,final_url=response.url,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        (CACHE/name).write_bytes(data)
        receipt['access']='success; direct body cached for locator self-review'
    except Exception as exc:
        receipt['access']='failed; no body confirmation'
        receipt['error']=str(exc)
    receipts.append(receipt)
    print(json.dumps(receipt,ensure_ascii=False),flush=True)
(ROOT/'evidence/final-recheck-downloads.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')

for name,terms in [('thanh2000.pdf',['no information about','URW.','Level 1']),('sojka1996.pdf',['emergencyfontwidthstretch']),('karow1997.pdf',['épaisseur','1993']),('thanh2001.pdf',['pdfadjustspacing'])]:
    path=CACHE/name
    if not path.exists():continue
    document=fitz.open(path)
    print('PDF',name,'physical_pages',len(document))
    for term in terms:
        for page in document:
            content=page.get_text()
            index=content.lower().find(term.lower())
            if index>=0:
                print('LOCATOR',name,'physical_page',page.number+1,'term',term,'EXCERPT',content[max(0,index-200):index+800])
                break
    if name=='karow1997.pdf':
        for page in document:
            text=page.get_text()
            if 'FIGURE 21' in text and 'Ek' in text:
                page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(CACHE/'karow-figure21.png')

for name,suffix,ranges in [
    ('lily101.tar.gz','mf/feta-toevallig.mf',[(11,27)]),
    ('lily0122.tar.gz','mf/feta-toevallig.mf',[(1,5),(140,167)]),
    ('lily0123.tar.gz','mf/feta-toevallig.mf',[(1,5),(114,125),(188,205)]),
    ('pdftex014f.tar.gz','pdftexdir/pdftex.ch',[(5108,5129),(5460,5469)]),
]:
    path=CACHE/name
    if not path.exists():continue
    with tarfile.open(fileobj=io.BytesIO(path.read_bytes()),mode='r:gz') as archive:
        members=[member for member in archive.getmembers() if member.name.endswith(suffix)]
        assert len(members)==1,(name,suffix,len(members))
        lines=archive.extractfile(members[0]).read().decode('latin1').splitlines()
        print('MEMBER',name,members[0].name)
        for first,last in ranges:
            for n in range(first,last+1):print(n,lines[n-1])
