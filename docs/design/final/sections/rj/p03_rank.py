"""Re-rank AF-RES-012 fixtures with link_study BM25; inspect matched tokens per hit."""
import json, math, re, sys, unicodedata, hashlib
from collections import Counter
from statistics import mean
fx = sys.argv[1]
entries = [json.loads(l) for l in open(fx+'/entries.jsonl')]
queries = [json.loads(l) for l in open(fx+'/queries.jsonl')]
qrels = {}
for line in open(fx+'/qrels.tsv'):
    p = line.rstrip('\n').split('\t')
    if len(p) >= 3 and p[0] != 'query_id':
        qrels.setdefault(p[0], {})[p[1]] = p[2]
def tokens(t): return re.findall(r'[^\W_]+', unicodedata.normalize('NFKC', t).casefold())
# English function words (closed class) - fixed list, declared here
FW_EN = set("""a an the and or but nor so yet of in on at to for from by with without into onto over under
as is are was were be been being am do does did done have has had having it its this that these those
there their they them we our you your he she his her i me my not no can could may might must shall should
will would than then when while where which who whom whose what how if else also only just any all each
every both either neither some such own same other another more most less least very too up down out off
about above after again against before below between during through until upon per via""".split())
# Korean: particles/endings cannot be separated by this tokenizer; list whole-token function words
FW_KO = set("""및 또는 그 이 저 것 수 등 더 안 못 때 중 위 후 전 를 을 은 는 이 가 의 에 와 과 도 로 으로 에서""".split())
VARIANTS = ('URL', 'URL+한줄', 'URL+한줄+용도')
def docs_for(lang, n):
    out = {}
    for e in entries:
        prefix = e['name'] + ' — '
        title = e['D-a'][lang]; desc = e['D-b'][lang]
        assert desc.startswith(prefix)
        out[e['id']] = [e['url'], title, desc[len(prefix):]][:n]
    return out
def rank(docs, qtext, drop=frozenset()):
    words = {k: Counter(tokens(' '.join(f))) for k, f in docs.items()}
    lengths = {k: sum(c.values()) for k, c in words.items()}
    avg = mean(lengths.values())
    df = Counter(t for c in words.values() for t in c)
    idf = {t: math.log1p((len(words)-f+0.5)/(f+0.5)) for t, f in df.items()}
    tie = {k: hashlib.sha256(('12012:'+k).encode()).digest() for k in words}
    q = Counter(t for t in tokens(qtext) if t not in drop)
    scored = []
    for k, c in words.items():
        norm = 1.5*(0.25+0.75*lengths[k]/avg)
        m = [t for t in q if t in c]
        s = sum(q[t]*idf[t]*c[t]*2.5/(c[t]+norm) for t in m)
        if s > 0: scored.append((-s, tie[k], k, sorted(m)))
    scored.sort()
    return [(k, m, -s) for s, _, k, m in scored]
mode = sys.argv[2] if len(sys.argv) > 2 else 'p03'
if mode == 'p03':
    q = next(x for x in queries if x['id'] == 'P03.w')
    for lang, fw in (('en', FW_EN), ('ko', FW_KO)):
        for n, name in enumerate(VARIANTS, 1):
            d = docs_for(lang, n)
            for label, drop in (('all', frozenset()), ('noFW', fw)):
                r = rank(d, q[lang], drop)
                pos = {k: i for i, (k, _, _) in enumerate(r, 1)}
                tj = pos.get('toyota-jit'); tm = next((m for k, m, _ in r if k == 'toyota-jit'), None)
                print(f'{lang} {name} {label}: returned={len(r)} toyota={tj} matched={tm} | queue={pos.get("asyncio-queue")} sem={pos.get("asyncio-semaphore")} rs={pos.get("reactive-streams")} tb={pos.get("token-bucket")}')
                if label=='all' or n==1:
                    print('   top10:', [(k, qrels['P03.w'].get(k,'-'), m[:6]) for k, m, _ in r[:10]])
elif mode == 'all':
    # across all 36 queries: how many top-10 hits are function-word-only matches, and how many of those are judged relevant (1/2)
    for lang, fw in (('en', FW_EN), ('ko', FW_KO)):
        for n, name in enumerate(VARIANTS, 1):
            d = docs_for(lang, n)
            fwonly = fwonly_rel = top = rel_top = 0; rel_lost=[]
            rec_all=[]; rec_drop=[]
            for q in queries:
                r = rank(d, q[lang])[:10]
                r2 = rank(d, q[lang], fw)[:10]
                rel = {k for k, g in qrels.get(q['id'], {}).items() if g in ('1','2')}
                for k, m, _ in r:
                    top += 1
                    g = qrels.get(q['id'], {}).get(k)
                    if g in ('1','2'): rel_top += 1
                    if m and all(t in fw for t in m):
                        fwonly += 1
                        if g in ('1','2'): fwonly_rel += 1; rel_lost.append((q['id'],k,g,m))
                if rel:
                    rec_all.append(len(rel & {k for k,_,_ in r})/len(rel))
                    rec_drop.append(len(rel & {k for k,_,_ in r2})/len(rel))
            print(f'{lang} {name}: top10 slots={top} relevant={rel_top} fw-only={fwonly} fw-only&relevant={fwonly_rel} R@10 all={mean(rec_all):.3f} noFW-query={mean(rec_drop):.3f}')
            for x in rel_lost: print('   fw-only relevant:', x)
