"""Capture three post-seal official follow-up pages; never search or score them."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    dict(source_id='OUT-DOC-ASM', recipient_id='R03', publisher='Rust Project',
         url='https://doc.rust-lang.org/reference/inline-assembly.html',
         title='Inline assembly — Rust Reference',
         read_location='Supported operand types: in, out, lateout, inout and inlateout; current web-reader lines333–414',
         observed='Current reference documents input-register initialization, output-place copy, and lateout reuse only after all inputs are read. This is present documented behavior, not execution by this study.',
         limitations='Mutable current documentation; does not prove every clause of the2020 first proposal shipped unchanged or that a donor procedure caused the choice.'),
    dict(source_id='OUT-DOC-MIXED', recipient_id='R05', publisher='Kubernetes Project',
         url='https://kubernetes.io/docs/concepts/services-networking/service/',
         title='Service — Kubernetes',
         read_location='Load balancers with mixed protocol types; current web-reader lines1283–1291',
         observed='The section describes API permission for mixed protocols and warns that providers may impose additional restrictions. Current text labels the feature stable since1.26.',
         limitations='Mutable current documentation, not provider execution. Adjacent general-default wording and feature-specific permission must be read together; no causal library citation follows from matching behavior.'),
    dict(source_id='OUT-DOC-APP', recipient_id='R07', publisher='Kubernetes Project',
         url='https://kubernetes.io/docs/tutorials/security/apparmor/',
         title='Restrict a Container’s Access to Resources with AppArmor',
         read_location='Feature-state statement and Securing a Pod; current web-reader lines908–959',
         observed='Current docs describe dedicated appArmorProfile fields, note the prior-to1.30 annotation API and label the feature stable since1.31.',
         limitations='Current feature existence does not prove that this unmerged initial PR or all its original seven skew predicates were adopted. No cluster execution or private design history examined.'),
]

def capture(doc):
    x=dict(doc);now=datetime.now(timezone.utc).isoformat()
    attempt={'kind':'followup_official_doc','url':x['url'],'source_id':x['source_id'],'checked_utc':now,
             'after_retrieval_seal':'a2ce15d10415c556574d1a65af77718a81052d01'}
    try:
        with urlopen(Request(x['url'],headers={'User-Agent':'AF-RES-033 public research'}),timeout=35) as response:
            raw=response.read();attempt.update(status='opened',http_status=response.status,final_url=response.url,bytes=len(raw))
        path=ROOT/'recipient/cache/outcomes'/f"{x['source_id']}.html"
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
        x.update(raw_sha256=sha256(raw).hexdigest(),cache_path=str(path.relative_to(ROOT)))
    except Exception as e:
        attempt.update(status='failed',error=str(e))
        x['capture_limitation']='Raw capture failed; substantive official sections were already read through web open/find.'
    x.update(kind='post_seal_official_documentation',original_url=x.pop('url'),fixed_url=None,
             fixed_url_status='Mutable current URL identified by checked UTC and captured hash where available',
             publication_date=None,version='Current page at checked UTC',checked_utc=now,
             read_status='content_verified',counted_minimum=False,minimum_category=None,
             duplicate_group=x['source_id'],supports=['Q6',x['recipient_id']])
    return x,attempt

if __name__=='__main__':
    pairs=list(ThreadPoolExecutor(max_workers=3).map(capture,DOCS))
    (ROOT/'recipient/outcome-doc-sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x,a in pairs))
    with (ROOT/'recipient/outcome_attempts.jsonl').open('a') as f:
        for x,a in pairs:f.write(json.dumps(a,ensure_ascii=False)+'\n')
    print(json.dumps({'official_followup_documents':len(pairs),'raw_captures':sum(a['status']=='opened' for x,a in pairs),'counted_in_minimum':0}))
