#!/usr/bin/env python3
"""Record every observed recipient reopening without adding unique-work credit."""
from pathlib import Path
import argparse,json
OWN=Path(__file__).resolve().parent.parent

def render():
    rows=[]
    for r in map(json.loads,(OWN/'trails.jsonl').read_text().splitlines()):
        v=r['view'];project='pandoc' if r['case_id'].startswith('P') else 'imagemagick'
        rows.append({'source_id':f"READER-{r['packet_id']}-S{r['step']}",
            'original_url':v['requested_document_url'],'arrived_url':r['arrival_url'],
            'arrival_observation_kind':r['arrival_url_kind'],'http_request_performed':False,
            'work_id':'pandoc-manual-all-versions' if project=='pandoc' else 'im-manual',
            'lineage':'Repeated bounded view of already counted official manual; no new work or natural case',
            'author':'John MacFarlane/Pandoc contributors' if project=='pandoc' else 'ImageMagick Studio/contributors',
            'version':r['document_version'],'published_at':None,'checked_utc':r['exposure_at_utc'],
            'read_utc':r['exposure_at_utc'],'read_sections':f"{r['doc_id']}[{r['offset_start']}:{r['offset_end']}] {r['fragment']}",
            'confirmed':'Exact displayed text, choices, answer and quote-presence checks are preserved in the trail; semantic support is separately evaluated.',
            'limits':'Offline fixed-document view, not a live browser or historical software execution. Prior model knowledge and procedural isolation remain limitations.',
            'counter_observation':'An arrived heading does not by itself establish a sufficient answer.',
            'unknown':'Human active reading time and adoption unobserved.',
            'questions':['Q4','Q5','Q7'],'ledger_rows':[r['packet_id']+':'+str(r['step']),r['source_log']],
            'allocation':'recipient_reopen','unique_counted':False,'primary':True,
            'reader':r['reader_id'],'status':'direct_offline_view','display_sha256':r['display_sha256'],
            'document_source_sha':v['source_sha'],'corpus_sha256':r['corpus_sha256'],
            'display_codepoints':r['cost']['display_codepoints'],'display_utf8_bytes':r['cost']['display_utf8_bytes']})
    return ''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
    text=render();p=OWN/'evidence/recipient-source-reads.jsonl'
    if a.check:assert p.read_text()==text,'recipient source rows differ'
    else:p.write_text(text)
    print(json.dumps({'rows':len(text.splitlines()),'new_unique_work_credit':0,'check':a.check}))
