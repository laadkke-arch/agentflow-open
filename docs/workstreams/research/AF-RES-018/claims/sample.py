#!/usr/bin/env python3
"""Validate literal provenance and sample atomic output claims before checking them."""
from pathlib import Path
import collections,hashlib,json,random
ROOT=Path(__file__).resolve().parents[1]
pool=json.loads((ROOT/'claims/pool.json').read_text())
raw={};seen=set()
for c in pool:
    key=(c['condition'],c['qid'])
    if key not in raw:raw[key]=json.loads((ROOT/'runs'/key[0]/(key[1]+'.json')).read_text())['raw_response']
    assert c['source_quote'] and c['source_quote'] in raw[key],('claim lacks literal response provenance',c)
    assert raw[key].count(c['source_quote'])==1,('ambiguous source quote must be disambiguated before sampling',c)
    assert c['claim_type'] in ['price','license','offline','self_hosting','platform','feature','other'],c
    fingerprint=(key,c['candidate'].casefold(),' '.join(c['claim'].casefold().split()))
    assert fingerprint not in seen,('duplicate atomic claim',fingerprint)
    seen.add(fingerprint)
    c['id']='CL-'+hashlib.sha256(json.dumps(fingerprint,ensure_ascii=False).encode()).hexdigest()[:14]
    c['source_start']=raw[key].find(c['source_quote']);c['source_end']=c['source_start']+len(c['source_quote'])
    c['selection_frame']='all extracted atomic factual claims in frozen discovery raw_response'
pool.sort(key=lambda c:(c['condition'],c['qid'],c['candidate'],c['id']))
(ROOT/'claims/pool.json').write_text(json.dumps(pool,ensure_ascii=False,indent=2)+'\n')
rng=random.Random(18018);sample=[];summary={}
for condition in ['A','P']:
    eligible=[c for c in pool if c['condition']==condition];byq=collections.defaultdict(list)
    for c in eligible:byq[c['qid']].append(c)
    chosen=[rng.choice(byq[q]) for q in sorted(byq)]
    ids={c['id'] for c in chosen};remaining=[c for c in eligible if c['id'] not in ids]
    if len(chosen)<80:chosen+=rng.sample(remaining,min(80-len(chosen),len(remaining)))
    assert len(chosen)<=80,('more than80 question clusters?',len(chosen))
    sample.extend(chosen)
    summary[condition]={'pool_claims':len(eligible),'questions_with_factual_claims':len(byq),
                        'sampled_claims':len(chosen),'sampled_questions':len({c['qid'] for c in chosen}),
                        'types':dict(collections.Counter(c['claim_type'] for c in chosen))}
out={'seed':18018,'target_per_condition':80,'rule':'one random claim per nonempty question, then random without replacement to80; process A then P using one seeded generator','summary':summary,'claims':sample}
(ROOT/'claims/SAMPLE.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
if any(x['sampled_claims']<75 for x in summary.values()):raise SystemExit('Insufficient actual facts: do not fabricate claims to reach minimum')
