#!/usr/bin/env python3
"""Normalize source ledgers without turning captures/repeated anchors into works."""
from pathlib import Path
from collections import Counter
import argparse
import csv
import hashlib
import io
import json

OWN = Path(__file__).resolve().parent.parent

def read_jsonl(p):
    return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]

def canon(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
    inputs=[('recruitment/sealed-sources.jsonl','recruitment'),
            ('gold-work/pandoc/sources-pandoc.jsonl','pandoc_reference'),
            ('gold-work/imagemagick/sources-imagemagick.jsonl','imagemagick_reference'),
            ('analogies/sources-analogies.jsonl','cross_domain'),
            ('evidence/root-source-reads.jsonl','root_verification')]
    for optional,role in [('evidence/recipient-source-reads.jsonl','recipient_reopen'),
                          ('evidence/resume-primary-rereads.jsonl','resume_primary_reread')]:
        if (OWN/optional).exists():inputs.append((optional,role))
    rows=[];input_hashes={}
    aliases={'pandoc-manual':'pandoc-manual-all-versions',
             'imagemagick-user-manual-all-versions':'im-manual',
             'eisenhower_finding_aid':'eisenhower_finding',
             'natural-pandoc-8518':'https://github.com/jgm/pandoc/issues/8518',
             'natural-pandoc-8522':'https://github.com/jgm/pandoc/issues/8522',
             'natural-pandoc-8526':'https://github.com/jgm/pandoc/issues/8526',
             'im-issue-6159':'https://github.com/ImageMagick/ImageMagick/issues/6159',
             'im-issue-6187':'https://github.com/ImageMagick/ImageMagick/issues/6187',
             'im-issue-6237':'https://github.com/ImageMagick/ImageMagick/issues/6237'}
    for name,origin in inputs:
        p=OWN/name;input_hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
        for original in read_jsonl(p):
            r=dict(original);r['ledger_origin']=origin
            if r['source_id']=='TIFF6':
                r['original_unique_counted']=r['unique_counted']
                r['unique_counted']=False
                r['credit_normalization']='Same work subsequently read at original Adobe publisher host (ROOT-TIFF6-ADOBE). ITU copy is evidence but gets no separate unique-work credit.'
            r['work_id']=aliases.get(r.get('work_id'),r.get('work_id'))
            r.setdefault('version',r.get('version_date',r.get('version_or_published_date')))
            r.setdefault('published_at',r.get('publication_date'))
            r.setdefault('read_utc',None)
            r.setdefault('ledger_rows',r.get('linked_case_rows',r.get('case_rows',[])))
            r.setdefault('counter_observation',r.get('counter_observation_or_unknown'))
            r.setdefault('unknown',r.get('counter_observation_or_unknown','Not separately observed beyond stated limits'))
            r.setdefault('reader',origin)
            r.setdefault('status',r.get('observation_status','read_status_in_original_fields'))
            r.setdefault('primary',bool(r.get('unique_counted')))
            r['original_status_fields_preserved']=True
            rows.append(r)
    startup=json.loads((OWN/'evidence/startup/startup.json').read_text())
    for i,item in enumerate(startup['required_files']+[{'path':'docs/automation/dot-control.json','sha256':None}],1):
        url=f"https://github.com/laadkke-arch/agentflow-open/blob/{startup['start_sha']}/{item['path']}"
        rows.append(dict(source_id=f'WORKFLOW-{i:02}',original_url=url,arrived_url=url,
            work_id='agentflow-workspace-contract',lineage='operating contract, not experimental primary quota',
            author='laadkke-arch/agentflow-open maintainers',version=startup['start_sha'],published_at=None,
            checked_utc=startup['checked_utc'],read_utc=None,
            timestamp_kind='startup receipt bounds read; exact individual read second not sampled',
            read_sections='complete file' if not item['path'].endswith('.json') else 'AF-RES-116 and dependency rows; baseline diff',
            confirmed='Task ownership, fixed dependency, research protocol and shared validation rules',
            limits='Operating instructions, not evidence of a navigation treatment effect',counter_observation=None,
            unknown='No other parallel task outputs were required or read',questions=['Q1','Q2','Q4'],ledger_rows=['SCOPE','manifest'],
            allocation='workflow_context',unique_counted=False,primary=False,reader='root',status='direct_read',
            sha256=item['sha256'],ledger_origin='startup'))
    for i,name in enumerate(startup['dependency_read_files'],1):
        sha=startup['dependency_handoff'] if name=='HANDOFF.md' else startup['dependency_result']
        url=f'https://github.com/laadkke-arch/agentflow-open/blob/{sha}/docs/workstreams/research/AF-RES-112/{name}'
        rows.append(dict(source_id=f'DEP112-{i:02}',original_url=url,arrived_url=url,
            work_id='AF-RES-112-bundle',lineage='one prior operating research bundle',
            author='AF-RES-112 research worker',version=sha,published_at=None,checked_utc=startup['checked_utc'],
            read_utc=None,timestamp_kind='startup receipt bounds read; exact individual read second not sampled',
            read_sections='complete result/ledger content returned by fixed GitHub read',
            confirmed=startup['dependency_findings'],limits='Prior Godot/LilyPond observations excluded from AF-RES-116 denominators',
            counter_observation='Same A/B exposure and zero full support do not establish general one-line effect',
            unknown='Old gaps were not recruited again',questions=['Q1','Q2','Q4','Q7'],ledger_rows=['STARTUP'],
            allocation='dependency_context',unique_counted=False,primary=False,reader='root',status='direct_read',ledger_origin='startup'))
    ids=[r['source_id'] for r in rows]
    if len(set(ids))!=len(ids):raise ValueError('source IDs must be globally unique')
    works={}
    for r in rows:
        for field in ['source_id','original_url','arrived_url','work_id','lineage','author','checked_utc','read_sections','confirmed','limits','questions','allocation','unique_counted']:
            if field not in r:raise ValueError(f"{r['source_id']} missing {field}")
        if r['unique_counted']:
            if r['work_id'] in works:raise ValueError('duplicate counted work '+r['work_id'])
            if not r['primary']:raise ValueError('nonprimary counted')
            works[r['work_id']]=r
    allocation=Counter(r['allocation'] for r in works.values())
    quota={'natural_request':6,'definition':8,'regression':6,'cross_domain_supplement':4}
    quota_met={k:allocation[k]>=n for k,n in quota.items()}
    event_files={'pandoc_reference':'gold-work/pandoc/read-log.jsonl',
                 'imagemagick_reference':'gold-work/imagemagick/read-events.jsonl',
                 'cross_domain':'analogies/sources-analogies.jsonl',
                 'root_verification_source_rows':'evidence/root-source-reads.jsonl'}
    events={key:len(read_jsonl(OWN/name)) for key,name in event_files.items()}
    summaries={
       'source_rows':len(rows),'distinct_original_urls':len({r['original_url'] for r in rows if r['original_url']}),
       'distinct_arrived_urls_or_locators':len({r['arrived_url'] for r in rows if r['arrived_url']}),
       'conservatively_counted_primary_works':len(works),'counted_by_allocation':dict(allocation),
       'quota_minimum':quota,'quota_met':quota_met,'all_quota_met':all(quota_met.values()),
       'required_classification_counted_works':sum(allocation[k] for k in quota),
       'workflow_and_dependency_rows_excluded':13,
       'natural_cases':6,'natural_packets_planned':18,'natural_stages_planned':54,
       'logged_exposure_or_inspection_events_by_role':events,
       'event_unit_warning':'Do not add unlike operations as reader opens: reference logs include index/excerpt/metadata or file inspections; cross-domain logs include web navigation/HTTP/image views. Actual recipient opens are counted only in trial-summary.json.',
       'known_machine_captured_document_count':214,
       'capture_is_direct_read':False,
       'initial_complete_issue_body_screening_rows':9,
       'source_rows_are_not_opens':'Repeated reads may be listed in read_utc/read_sections or separate source rows. Mirrors/versions/anchors were conservatively merged into a work.',
       'input_sha256':input_hashes,
       'failures_and_truncated_reads':'Original status/limits/read events preserved, including 404/403/navigation-only and corrected truncated displays; those attempts add no unique-work credit.',
    }
    inventory=io.StringIO();w=csv.DictWriter(inventory,fieldnames=['work_id','allocation','representative_source_id','author','version','original_url','independence_basis'],lineterminator='\n')
    w.writeheader()
    for wid,r in sorted(works.items()):w.writerow(dict(work_id=wid,allocation=r['allocation'],representative_source_id=r['source_id'],author=r['author'],version=r['version'],original_url=r['original_url'],independence_basis=r.get('independence_basis',r.get('lineage'))))
    outputs={'sources.jsonl':''.join(canon(r)+'\n' for r in rows),
             'analysis/source-counts.json':json.dumps(summaries,ensure_ascii=False,indent=2)+'\n',
             'analysis/source-inventory.csv':inventory.getvalue()}
    for name,text in outputs.items():
        p=OWN/name
        if a.check:
            if not p.exists() or p.read_text()!=text:raise SystemExit('rebuild mismatch: '+name)
        else:p.write_text(text)
    print(json.dumps({k:summaries[k] for k in ['source_rows','distinct_original_urls','conservatively_counted_primary_works','counted_by_allocation','all_quota_met']},ensure_ascii=False))

if __name__=='__main__': main()
