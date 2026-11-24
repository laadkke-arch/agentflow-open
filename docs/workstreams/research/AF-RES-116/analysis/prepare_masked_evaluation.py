#!/usr/bin/env python3
"""Make condition-masked judgment inputs from remotely sealed recipient logs.

Neither this script nor the mechanical exporter judges semantic correctness.
Reader prose is preserved, including residual references that can reveal a hint.
"""
from pathlib import Path
import argparse, hashlib, json

OWN=Path(__file__).resolve().parent.parent
SEAL='47e8d24ad9c0313f6d1a361882198f42307a0d5d'
def h(b):return hashlib.sha256(b).hexdigest()
def load(name):return json.loads((OWN/name).read_text())

def build():
    cases={c['case_id']:c for c in load('cases.json')['cases']}
    refs={c['case_id']:c for name in ['gold-work/pandoc/gold.json','gold-work/imagemagick/gold.json'] for c in load(name)['cases']}
    trails=[json.loads(l) for l in (OWN/'trails.jsonl').read_text().splitlines()]
    sessions={};mapping=[]
    for row in trails:
        sid=row['packet_id'];mid='m'+h(('AF116-mask-'+sid).encode())[:10]
        if mid not in sessions:
            sessions[mid]={'masked_id':mid,'case_id':row['case_id'],
                           'common_request':cases[row['case_id']]['common_request'],
                           'version':row['document_version'],'stages':[]}
            mapping.append({'masked_id':mid,'packet_id':sid,'case_id':row['case_id'],'condition':row['condition']})
        checks=[{k:v for k,v in c.items() if k not in ['packet_id','session','reader_id','condition']} for c in row['citation_checks']]
        sessions[mid]['stages'].append({'step':row['step'],
            'visible':{'doc_id':row['doc_id'],'start':row['offset_start'],'end':row['offset_end'],
                       'display_text':row['view']['display_text'],'display_sha256':row['display_sha256'],
                       'arrival_url':row['arrival_url'],'fragment':row['fragment']},
            'answer_original':row['answer_original'],'citation_checks':checks})
    instructions={
        'role':'fresh AI semantic evaluator, condition identity and one-line hint masked',
        'source_seal':SEAL,
        'definition':'Judge each stage from cumulative views of that masked recipient, never from another recipient view or reference knowledge alone.',
        'allowed_grades':['full_supported','justified_hold','partial_reconstruction','label_only','dangerous_certainty','unsupported_or_wrong'],
        'flags':'full_supported, justified_hold and partial_reconstruction are separately reported booleans; partial evidence plus justified hold is possible.',
        'full_supported':'Both requested operation and preservation plus material exceptions have actually exposed supporting evidence; correct-looking answer from prior knowledge is not success.',
        'dangerous_certainty':'Unqualified adoption, preservation guarantee, definitive diagnosis or fix without exposed required evidence. Explicit hypothetical or unverified idea is not this flag.',
        'label_only':'Correct decision word without sufficient evidence; distinguish justified noncommitment.',
        'counterexample_found':'Actual exposed exception relevant to this request, not a merely imagined possibility or unrelated manual warning.',
        'claim_errors':'Record minor citation/scope errors separately, even if final safety judgment remains justified hold.',
        'masking_limit':'Unedited answer prose may reference a hint or previously supplied label. Such residual exposure must be reported. This is not OS isolation or a human study.',
        'required_row_keys':['masked_id','case_id','step','grade','full_supported','justified_hold','partial_reconstruction','label_only','dangerous_certainty','counterexample_found','counterexample_detail','evidence_used','missing_required_evidence','errors','rationale_ko'],
        'prohibited_reads':'Do not read packets, authoring, inputs, readers, trails, pairs, other evaluator output, hidden mapping or study result. Read only assigned masked input plus this interface; supplied reference is allowed.',
    }
    outputs={}
    for group,prefix in [('pandoc','P'),('imagemagick','I')]:
        data={'instructions':instructions,'group':group,
              'reference':{cid:r for cid,r in refs.items() if cid.startswith(prefix)},
              'sessions':[sessions[k] for k in sorted(sessions) if sessions[k]['case_id'].startswith(prefix)]}
        outputs['evaluation/masked-'+group+'.json']=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    outputs['evaluation/masking-map.json']=json.dumps(mapping,ensure_ascii=False,indent=2)+'\n'
    outputs['evaluation/input-receipt.json']=json.dumps({'source_seal':SEAL,'trails_sha256':h((OWN/'trails.jsonl').read_bytes()),
        'masked_inputs':{k:h(v.encode()) for k,v in outputs.items()},'source_stage_count':len(trails),
        'independent_evaluator_started_before_source_seal':False,'masking_is_partial':True,
        'removed_fields':['A/B/C identity','hint','packet/session ID','choice reasons','wall times'],
        'preserved_fields':['common request','actual display','exact answer','citation check','reference gold']},ensure_ascii=False,indent=2)+'\n'
    return outputs

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
    (OWN/'evaluation').mkdir(exist_ok=True)
    bad=[]
    for name,value in build().items():
        path=OWN/name
        if a.check:
            if not path.exists() or path.read_bytes()!=value.encode():bad.append(name)
        else:path.write_bytes(value.encode())
    print(json.dumps({'check':a.check,'mismatches':bad}));raise SystemExit(bool(bad))
