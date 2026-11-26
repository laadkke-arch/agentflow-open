import sys, json, csv, io, re
sys.path.insert(0, sys.argv[1])
import link_study as ls
from pathlib import Path
src = Path(sys.argv[2])
J=lambda p:[json.loads(l) for l in ls.read_file(src,p).splitlines()]
entries, queries = J('corpus/entries.jsonl'), J('queries/queries.jsonl')
E={e['id']:e for e in entries}; Q={q['id']:q for q in queries}
grades={}
for p in ('qrels/qrels.tsv','results/pooled_judgments.tsv'):
    for r in csv.DictReader(io.StringIO(ls.read_file(src,p)),delimiter='\t'): grades[(r['query_id'],r['entry_id'])]=r['grade']
t=E['toyota-jit']
print("toyota url:", t['url']); print("role:", t['role'], "| D-a en:", t['D-a']['en']); print("D-b en:", t['D-b']['en'][:300]); print("D-b ko:", t['D-b']['ko'][:300])
print("P03.w en:", Q['P03.w']['en']); print("P03.w ko:", Q['P03.w']['ko'])
STOP={"a","an","and","the","of","to","in","on","for","with","can","is","are","be","or","by","it","that","this","as","at","from","when","which","not","but","its","into","than","so","we","our","do","does","must","should","without","each","only","same","one","other","no"}
for lang in ('en','ko'):
  for name, docs in ls.projections(entries, lang).items():
    ranks = ls.rankings(docs, queries, lang)
    # Toyota hits across queries
    hits=[(q, r.index('toyota-jit')+1) for q,r in ranks.items() if 'toyota-jit' in r[:10]]
    # stopword-only hits in top10
    tot=sw=sw_rel=nsw=nsw_rel=sw_unj=nsw_unj=0
    for q,r in ranks.items():
        qt=set(ls.tokens(Q[q][lang]))
        for e in r[:10]:
            ov=qt & set(ls.tokens(' '.join(docs[e])))
            g=grades.get((q,e))
            tot+=1
            if ov and ov<=STOP:
                sw+=1; sw_rel+= g in ('1','2'); sw_unj += g is None
            else:
                nsw+=1; nsw_rel+= g in ('1','2'); nsw_unj += g is None
    print(f"{lang} {name}: toyota top10 in {len(hits)} queries {hits[:8]} | top10 pairs {tot}; function-word-only {sw} (rel {sw_rel}, unjudged {sw_unj}); content-overlap {nsw} (rel {nsw_rel}, unjudged {nsw_unj})")
    if lang=='en':
        r=ranks['P03.w']; qt=set(ls.tokens(Q['P03.w'][lang]))
        print("   P03.w top5:", [(e, grades.get(('P03.w',e)), sorted(qt & set(ls.tokens(' '.join(docs[e]))))) for e in r[:5]])
