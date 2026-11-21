#!/usr/bin/env python3
"""Prepare condition-hidden 30-word rows; require review of every overflow.

The key is only emitted with --reveal-key after raw blind judgments exist.
Source responses are never overwritten. Overrides contain editorial reductions,
not added evidence or replacement candidates.
"""
from pathlib import Path
import argparse,hashlib,json,random,re,collections,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
SEED=18018
LABELS=['DIRECT_DOCUMENTED','INSUFFICIENT','CONDITIONAL_TRANSFER','SURFACE_OR_CONSTRAINT_MISMATCH']
def load(p,default=None):
    f=ROOT/p
    return json.loads(f.read_text()) if f.exists() else default
def save(p,d):
    f=ROOT/p;f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def clean(s):
    if s is None:return ''
    if isinstance(s,list):s='; '.join(str(v) for v in s)
    if isinstance(s,dict):s='; '.join(f'{k}: {v}' for k,v in s.items())
    s=str(s)
    for label in LABELS:s=s.replace(label,'')
    s=re.sub(r'https?://\S+','',s)
    return ' '.join(s.split()).strip(' ;:—-')
def rows():
    expected=load('questions/dispatch.json')['order'];out=[];keys={}
    # Checks received identical names/URLs. Restore those input fields when an
    # executor omitted them, rather than exposing a condition-specific omission.
    check_inputs={c['check_id']:c for q in load('gold/checks.json')['questions'] for c in q['checks']}
    for d in expected:
        f=ROOT/d['output'];run=json.loads(f.read_text())
        assert len(run.get('checks',[]))==3,('not complete',str(f))
        for kind,items in [('discovery',run['candidates']),('check',run['checks'])]:
            for i,c in enumerate(items):
                rid='R'+hashlib.sha256(f'{SEED}|{d["qid"]}|{d["condition"]}|{kind}|{i}'.encode()).hexdigest()[:16]
                reason=clean(c.get('reason',''));caveat=clean(c.get('constraints_or_caveat','')) if kind=='discovery' else ''
                text=reason if not caveat or caveat in reason else reason+' '+caveat
                source={'reason':c.get('reason',''),'constraints_or_caveat':c.get('constraints_or_caveat') if kind=='discovery' else None}
                identity=check_inputs[c['check_id']] if kind=='check' else c
                out.append({'row_id':rid,'qid':d['qid'],'name':identity.get('name') or identity.get('candidate'),
                            'url':identity.get('url') or identity.get('candidate_url'),
                            'source_text':text,'proposed_reason':text if len(text.split())<=30 else ' '.join(text.split()[:30]),
                            'needs_review':len(text.split())>30,'source_word_count':len(text.split())})
                keys[rid]={'condition':d['condition'],'qid':d['qid'],'kind':kind,'index':i,
                           'rank':c.get('rank'),'check_id':c.get('check_id'),'source_file':d['output'],'source_fields':source,
                           'decision':c.get('decision',c.get('verdict',c.get('judgment'))) if kind=='check' else None}
    assert len(out)==len(keys)
    return out,keys

def main(prepare,finalize,reveal):
    data,keys=rows()
    if prepare:
        review=[r for r in data if r['needs_review']]
        rng=random.Random(SEED);rng.shuffle(review)
        save('judging/normalization-input.json',{'rule':'Reduce to <=30 English whitespace words without new facts. Preserve negation, edition, platform and material uncertainty. No condition is supplied. Record unavoidable scope loss.','rows':review})
        save('judging/normalization-overflow-summary.json',{'total_rows':len(data),'within_limit':len(data)-len(review),'need_editorial_reduction':len(review),'seed':SEED})
        print(json.dumps({'total_rows':len(data),'need_review':len(review)}))
    if finalize:
        overrides=load('judging/overrides.json',{})
        converted=[];groups=collections.defaultdict(list)
        for r in data:
            override=overrides.get(r['row_id'])
            if r['needs_review']:assert override,('unreviewed overflow',r['row_id'])
            reason=override['reason'] if override else r['proposed_reason']
            assert len(reason.split())<=30 and reason.strip(),r['row_id']
            assert not any(l in reason for l in LABELS),r['row_id']
            groups[r['qid']].append({k:r[k] for k in ['row_id','qid','name','url']}|{'reason':reason})
            converted.append({'row_id':r['row_id'],'source_word_count':r['source_word_count'],
                              'normalized_word_count':len(reason.split()),'source_text':r['source_text'],
                              'normalized_reason':reason,'operation':'editorial reduction' if override else 'format-label/URL stripping and whitespace only',
                              'editor_note':override.get('note') if override else None,
                              'scope_loss':override.get('scope_loss','none reported') if override else 'none',
                              'new_facts_allowed':False})
        rng=random.Random(SEED);qids=sorted(groups);rng.shuffle(qids)
        for q in qids:
            rng.shuffle(groups[q]);save(f'judging/normalized/{q}.json',{'qid':q,'rows':groups[q]})
            inp=load(f'questions/inputs/{q}.json');inp.pop('common_run_instructions',None)
            save(f'judging/question-inputs/{q}.json',inp)
        # The transformation log contains no condition or source path until reveal.
        save('judging/conversion-log.json',converted)
        save('judging/batch-order.json',{'seed':SEED,'qids':qids,'row_count':sum(len(v) for v in groups.values())})
        print(json.dumps({'normalized_rows':sum(len(v) for v in groups.values()),'questions':len(qids)}))
    if reveal:
        subprocess.run([sys.executable,str(ROOT/'judging/batches.py'),'--validate'],check=True)
        normalized=set();byqid={}
        for f in (ROOT/'judging/normalized').glob('*.json'):
            d=json.loads(f.read_text());byqid[d['qid']]={r['row_id'] for r in d['rows']};normalized.update(byqid[d['qid']])
        assert normalized==set(keys)
        coverage=collections.defaultdict(set)
        for f in (ROOT/'judging/blind-raw').glob('*.json'):
            judgment=json.loads(f.read_text())
            for row in judgment.get('rows',[]):
                assert row['row_id'] in normalized,('unknown judgment row',str(f),row['row_id'])
                coverage[judgment['judge_id']].add(row['row_id'])
        plan=load('judging/plan.json');assert plan,'Missing coverage plan'
        planned={j['judge_id']:set().union(*(byqid[q] for q in j['qids'])) for j in plan['judges']}
        assert planned.get('primary')==normalized
        assert set(coverage)==set(planned) and all(coverage[j]==expected for j,expected in planned.items()),'Incomplete planned blind judge coverage: refuse key release'
        save('judging/key.json',{'released_after_raw_judging':True,'seed':SEED,
                               'complete_judges':{j:len(ids) for j,ids in coverage.items()},'rows':keys})
        print('Key released after primary full coverage and secondary planned subset coverage.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--finalize',action='store_true');p.add_argument('--reveal-key',action='store_true');a=p.parse_args();main(a.prepare,a.finalize,a.reveal_key)
