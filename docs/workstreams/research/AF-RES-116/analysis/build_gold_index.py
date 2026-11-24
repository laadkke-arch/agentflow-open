#!/usr/bin/env python3
"""Normalize already sealed reference decisions; never read recipient outcomes.

External evidence uses explicit presence sentinels, not fabricated source offsets.
The real line/page/file locators remain in external_evidence and the source ledgers.
"""
from pathlib import Path
import argparse, csv, hashlib, io, json

OWN = Path(__file__).resolve().parent.parent

def read(name):
    return json.loads((OWN / name).read_text())

def j(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)

def digest(name):
    return hashlib.sha256((OWN / name).read_bytes()).hexdigest()

def normalize():
    originals = {c['case_id']: c for c in read('cases.json')['cases']}
    files = ['gold-work/pandoc/gold.json', 'gold-work/imagemagick/gold.json',
             'gold-work/pandoc/target-spans.json', 'gold-work/imagemagick/target-spans.json']
    refs = {c['case_id']: c for f in files[:2] for c in read(f)['cases']}
    targets = {c['case_id']: c for f in files[2:] for c in read(f)['cases']}
    cases, rows = [], []
    for cid in ['P1', 'P2', 'P3', 'I1', 'I2', 'I3']:
        r, t, original = refs[cid], targets[cid], originals[cid]
        is_pandoc = cid.startswith('P')
        input_packet = next(json.loads(line) for line in (OWN/'packets.jsonl').read_text().splitlines()
                            if json.loads(line)['case_id'] == cid)
        operation = r['O']['definition'] if is_pandoc else r['O_definition']
        preservation = r['P']['definition'] if is_pandoc else r['P_definition']
        answer = r['expected_qualified_answer'] if is_pandoc else r['correct_answer']
        exceptions = r['necessary_exceptions_counterinputs'] if is_pandoc else r['required_exceptions']
        intervals = r['minimum_supporting_intervals'] if is_pandoc else r['minimal_supporting_intervals']
        external = r['outside_corpus_minimum_evidence'] if is_pandoc else r['outside_corpus_requirements']
        gaps = r['known_gaps'] if is_pandoc else r['unknowns']
        # P3 lacks the rendering environment. I3 lacks the original JP2 bytes.
        full_complete = cid not in ('P3', 'I3')
        missing = []
        if cid == 'P3':
            missing = [{'required_for':['full'], 'item':'original rendering command, engine/template/TeX package versions and matched float/table test'}]
        elif cid == 'I3':
            missing = [{'required_for':['full'], 'item':'original JP2 bytes, colr/cmap/cdef/codestream and exact tile band metadata'}]
        mode_target = {'semantic_complete':True,
                       'alternatives':[[x] for x in t['related_operation_targets']]}
        sentinel = {'doc_id':'OUTSIDE_'+cid, 'start':0, 'end':1, 'outside_corpus':True,
                    'interval_kind':'presence sentinel only; 0:1 is NOT an original source offset',
                    'outside_reason':t['decisive_answer_target']['reason'],
                    'source_ids':t['decisive_answer_target'].get('source_ids',[]),
                    'external_evidence':external}
        modes = {'target':mode_target,
                 'full':{'semantic_complete':full_complete,
                         'alternatives':[[*t['related_operation_targets'], sentinel]],
                         'endpoint':'complete fixed-version source-level answer and required exceptions; not historical binary execution'}}
        for x in t.get('other_related_targets',[]):
            modes[x['interval_id']]={'semantic_complete':True,'alternatives':[[x]],
                                   'endpoint':x.get('role')}
        # Each reference-defined documentary interval is also measured separately.
        # These are partial support endpoints, not a relaxed definition of success.
        for x in intervals:
            modes['span_'+x['interval_id']]={'semantic_complete':True,'alternatives':[[x]],
                                           'endpoint':'this one documentary interval only'}
        cases.append({'case_id':cid,'graph':cid,'start_doc_id':input_packet['start_doc_id'],
                      'semantic_gold_complete':full_complete,'missing_inputs':missing,'modes':modes})
        rows.append({'case_id':cid,'layer':'natural','original_url':original['original_url'],
                     'specified_version':original.get('specified_version'),
                     'fixed_document_version':input_packet['document_version'],
                     'upstream_commit':r.get('fixed_commit',r.get('upstream_commit')),
                     'start_url':original['start_url'],'start_doc_id':input_packet['start_doc_id'],
                     'operation':operation,'preservation':preservation,
                     'answer':j(answer),'exceptions':j(exceptions),
                     'inside_corpus_intervals':j(intervals),'external_evidence':j(external),
                     'related_operation_targets':j(t['related_operation_targets']),
                     'decisive_answer_target':j(t['decisive_answer_target']),
                     'reference_author':'gold_pandoc' if is_pandoc else 'gold_imagemagick',
                     'reference_seal':'8b57d241d88cb6c5ddf3454d2b28fa3fb46fd473',
                     'semantic_complete':full_complete,'missing_inputs':j(missing),'known_gaps':j(gaps),
                     'historical_binary_execution':False})
    req={'schema':1,'corpus_sha256':digest('corpus.json.gz'),'cases':cases,
         'source_inputs':{f:digest(f) for f in files},
         'derivation':'Only pre-recipient sealed reference files are used. No packets hint text or recipient outcomes used to choose intervals.',
         'outside_interval_convention':'OUTSIDE_* 0:1 is an explicit evidence-presence marker absent from the fixed corpus, never a claimed quote span. Original source locators are preserved in external_evidence.',
         'semantic_scope':'P1/P2/I1/I2 source-level request disposition; P3/I3 remain unknown. Existing method cannot certify historical runtime or all possible workarounds.'}
    out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
    return {'gold.csv':out.getvalue(),'gold-intervals.json':json.dumps(req,ensure_ascii=False,indent=2)+'\n'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');a=parser.parse_args()
    outputs=normalize()
    if a.check:
        bad=[]
        for name,value in outputs.items():
            if not (OWN/name).exists() or (OWN/name).read_bytes()!=value.encode():bad.append(name)
        print(json.dumps({'checked':list(outputs),'mismatches':bad}));raise SystemExit(bool(bad))
    for name,value in outputs.items():(OWN/name).write_bytes(value.encode())
    print(json.dumps({'written':list(outputs),'case_count':6}))
