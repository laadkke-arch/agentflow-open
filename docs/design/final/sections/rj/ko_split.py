"""Korean queries: effect of splitting tokens at Latin/Hangul script boundaries (asyncio의 -> asyncio, 의)."""
import json, math, re, sys, unicodedata, hashlib
from collections import Counter
from statistics import mean
fx = sys.argv[1]
entries = [json.loads(l) for l in open(fx+'/entries.jsonl')]
queries = [json.loads(l) for l in open(fx+'/queries.jsonl')]
qrels = {}
for line in open(fx+'/qrels.tsv'):
    p = line.rstrip('\n').split('\t')
    if len(p) >= 3 and p[0] != 'query_id': qrels.setdefault(p[0], {})[p[1]] = p[2]
roles = {e['id']: e['role'] for e in entries}
def base(t): return re.findall(r'[^\W_]+', unicodedata.normalize('NFKC', t).casefold())
def split(t):
    out = []
    for w in base(t):
        out += re.findall(r'[a-z0-9]+|[^a-z0-9]+', w)
    return out
def run(tokfn, lang, n, qtok=None):
    qtok = qtok or tokfn
    docs = {}
    for e in entries:
        pre = e['name'] + ' — '
        docs[e['id']] = [e['url'], e['D-a'][lang], e['D-b'][lang][len(pre):]][:n]
    words = {k: Counter(tokfn(' '.join(f))) for k, f in docs.items()}
    L = {k: sum(c.values()) for k, c in words.items()}; avg = mean(L.values())
    df = Counter(t for c in words.values() for t in c)
    idf = {t: math.log1p((len(words)-f+0.5)/(f+0.5)) for t, f in df.items()}
    tie = {k: hashlib.sha256(('12012:'+k).encode()).digest() for k in words}
    rec, prin, empty = [], [], 0
    for q in queries:
        Q = Counter(qtok(q[lang]))
        sc = []
        for k, c in words.items():
            norm = 1.5*(0.25+0.75*L[k]/avg)
            s = sum(Q[t]*idf[t]*c[t]*2.5/(c[t]+norm) for t in Q if t in c)
            if s > 0: sc.append((-s, tie[k], k))
        top = [k for _, _, k in sorted(sc)][:10]
        if not top: empty += 1
        rel = {k for k, g in qrels.get(q['id'], {}).items() if g in ('1', '2')}
        if rel: rec.append(len(rel & set(top))/len(rel))
        pr = {k for k in rel if roles.get(k) == 'principle'}
        if pr: prin.append(len(pr & set(top))/len(pr))
    return mean(rec), mean(prin), empty
for n, name in enumerate(('URL', 'URL+한줄', 'URL+한줄+용도'), 1):
    a = run(base, 'ko', n); b = run(split, 'ko', n); e = run(base, 'en', n)
    print(f'{name}: ko base R@10={a[0]:.3f} prinR@10={a[1]:.3f} empty={a[2]} | ko split R@10={b[0]:.3f} prin={b[1]:.3f} empty={b[2]} | en R@10={e[0]:.3f} prin={e[1]:.3f}')
