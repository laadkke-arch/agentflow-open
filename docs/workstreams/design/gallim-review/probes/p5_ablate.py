import sys, json, csv, io, math, hashlib
from statistics import mean
from collections import Counter
sys.path.insert(0, sys.argv[1])
import link_study as ls
from pathlib import Path
src=Path(sys.argv[2])
J=lambda p:[json.loads(l) for l in ls.read_file(src,p).splitlines()]
entries, queries = J('corpus/entries.jsonl'), J('queries/queries.jsonl')
Q={q['id']:q for q in queries}; roles={e['id']:e['role'] for e in entries}
grades={}
for p in ('qrels/qrels.tsv','results/pooled_judgments.tsv'):
    for r in csv.DictReader(io.StringIO(ls.read_file(src,p)),delimiter='\t'): grades[(r['query_id'],r['entry_id'])]=r['grade']
# Standard English function words (closed class) - fixed before looking at results
STOP=set("a an and the of to in on for with can is are be or by it that this as at from when which not but its into than so we our do does must should may without each only same one other no all any if then there these those their them they was were been has have had will would could about over under after before up out time".split())
STOP_NO_TIME = STOP - {"time"}
def rankings(docs, queries, lang, stop):
    tok=lambda s:[t for t in ls.tokens(s) if t not in stop]
    words={k:Counter(tok(' '.join(f))) for k,f in docs.items()}
    lengths={k:sum(c.values()) for k,c in words.items()}; avg=mean(lengths.values())
    df=Counter(t for c in words.values() for t in c)
    idf={t:math.log1p((len(words)-f+0.5)/(f+0.5)) for t,f in df.items()}
    tie={k:hashlib.sha256(('12012:'+k).encode()).digest() for k in words}
    res={}; contrib={}
    for q in queries:
        qc=Counter(tok(q[lang])); sc=[]
        for k,c in words.items():
            norm=1.5*(0.25+0.75*lengths[k]/avg) if avg else 1
            parts={t:n*idf[t]*c[t]*2.5/(c[t]+norm) for t,n in qc.items() if t in c}
            s=sum(parts.values())
            if s>0: sc.append((-s,tie[k],k)); contrib[(q['id'],k)]=parts
        res[q['id']]=[k for _,_,k in sorted(sc)]
    return res, contrib
def recall(ranks, group=None):
    gold={q:set() for q in Q}
    for (q,e),g in grades.items():
        if g in('1','2') and (group is None or (group=='principle' and roles[e]=='principle')): gold[q].add(e)
    return mean(len(set(ranks[q][:10])&ids)/len(ids) for q,ids in gold.items() if ids)
for stopname, stop in (("none",set()),("function-words",STOP_NO_TIME),("function-words+time",STOP)):
  for lang in ('en',):
    for name, docs in ls.projections(entries, lang).items():
        r,c=rankings(docs, queries, lang, stop)
        tr = r['P03.w'].index('toyota-jit')+1 if 'toyota-jit' in r['P03.w'] else None
        hub=sum('toyota-jit' in v[:10] for v in r.values())
        parts = {k:round(v,3) for k,v in sorted(c.get(('P03.w','toyota-jit'),{}).items(), key=lambda x:-x[1])}
        print(f"stop={stopname:20s} {lang} {name:12s} R@10={recall(r):.3f} principleR@10={recall(r,'principle'):.3f} toyota@P03.w={tr} toyota_top10_queries={hub} contrib={parts}")
