#!/usr/bin/env python3
"""Audit frozen sample and control completeness without network or full bodies."""
import collections
import hashlib
import json
import pathlib
import subprocess

P=pathlib.Path(__file__).resolve().parent
read=lambda n:json.loads((P/n).read_text())
q=read('new-questions.json');g=read('gold-draft.json')['rows'];c=read('checks-draft.json')['rows'];s=read('sources-draft.json')
assert len(q)==20 and len({x['id'] for x in q})==20
platforms=collections.Counter(x['platform'] for x in q)
assert len(platforms)>=3 and max(platforms.values())<=10
assert all('2026-06-01'<=x['date']<='2026-11-21' and x['date_confirmed_in_direct_source'] for x in q)
assert sum(x['initial_revision_recovered'] for x in q)==9
assert len(g)==93 and sum(x['grade']=='2' for x in g)==8
assert len(c)==60 and all(x['candidate'] and x['candidate_url'].startswith('https://') for x in c)
for x in q:
    rows=[r for r in c if r['qid']==x['id']]
    assert len(rows)==3 and len({r['candidate'] for r in rows})==3
    assert sum(r['slot']=='positive' for r in rows)==1
    assert sum(r['slot']=='irrelevant' for r in rows)==1
for r in c:
    if r['slot']=='auxiliary_unjudged':
        assert r['grade'] is None and not r['strict_N_count_eligible'] and not r['positive_rejection_count_eligible']
required={'id','url','accessed_at_utc','source_type','title','version_or_date','sections_read','confirmed','limits','level','used_in'}
assert all(required<=set(x) for x in s['sources'])
assert len({x['id'] for x in s['sources']})==len(s['sources'])
assert all(not x['count_for_method_comparison_literature'] for x in s['sources'])
sourceids={x['id'] for x in s['sources']}
assert all(set(x.get('source_ids',[]))<=sourceids for x in c)

root=P.parents[5]
frozen='fe8ad7f20ff387801d0e6af97c9c98f90e3fc081'
for n in ['new-questions.json','dedup-and-selection.json']:
    rel=(P/n).relative_to(root).as_posix()
    committed=subprocess.check_output(['git','show',frozen+':'+rel],cwd=root)
    assert committed==(P/n).read_bytes(), 'Frozen question changed: '+n

print(json.dumps({'questions':len(q),'platforms':dict(platforms),'original_revisions':9,'gold_rows':len(g),
                  'grade_counts':dict(collections.Counter(x['grade'] for x in g)),
                  'probe_slots':len(c),'probe_roles':dict(collections.Counter(x['slot'] for x in c)),
                  'sources':len(s['sources']),'excluded_reads':len(s['excluded']),
                  'question_freeze_unchanged':frozen,'strict_N_all_questions_met':False},ensure_ascii=False,indent=2))
