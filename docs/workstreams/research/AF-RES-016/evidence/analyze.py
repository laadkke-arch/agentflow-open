#!/usr/bin/env python3
"""Reproduce nominal agreement from frozen responses; no label inference/editing.

Run from any directory. Outputs stay in AF-RES-016/evidence. Bootstrap seed,
cluster units, and impact selection implement the frozen SCOPE.md plan.
"""
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import random

BASE = Path(__file__).resolve().parents[1]
SEED = 2026112016 + 600
B = 5000
SCHEMES = ('S1', 'S2', 'S3', 'S3_form')

def read(path):
    return json.loads((BASE / path).read_text())

def save(path, data):
    (BASE / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def label(row, scheme):
    if scheme == 'S3':
        return row['S3']['form'] + ' | ' + row['S3']['contribution']
    if scheme == 'S3_form':
        return row['S3']['form']
    return row[scheme]

def point(a, b):
    n = len(a)
    assert n == len(b)
    if not n:
        return {'n': 0, 'agree': 0, 'po': None, 'pe': None, 'kappa': None}
    ca, cb = Counter(a), Counter(b)
    agree = sum(x == y for x, y in zip(a, b))
    po = agree / n
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    kappa = (po - pe) / (1 - pe) if pe < 1 else None
    return {'n': n, 'agree': agree, 'po': po, 'pe': pe, 'kappa': kappa}

def quantile(xs, p):
    if not xs:
        return None
    xs = sorted(xs)
    h = (len(xs) - 1) * p
    i = int(h)
    j = min(i + 1, len(xs) - 1)
    return xs[i] + (h - i) * (xs[j] - xs[i])

def ci(xs):
    valid = [x for x in xs if x is not None]
    return [quantile(valid, .025), quantile(valid, .975)]

def resamples(clusters, seed=SEED):
    by_cluster = defaultdict(list)
    for i, c in enumerate(clusters):
        by_cluster[c].append(i)
    names = sorted(by_cluster)
    rng = random.Random(seed)
    return [[i for c in rng.choices(names, k=len(names)) for i in by_cluster[c]] for _ in range(B)]

def report(a, b, clusters, draws=None):
    result = point(a, b)
    result['cluster_count'] = len(set(clusters))
    result['marginal_a'] = dict(sorted(Counter(a).items()))
    result['marginal_b'] = dict(sorted(Counter(b).items()))
    result['confusion'] = [{'a': x, 'b': y, 'n': n}
        for (x, y), n in sorted(Counter(zip(a, b)).items())]
    draws = resamples(clusters) if draws is None else draws
    boots = [point([a[i] for i in ix], [b[i] for i in ix]) for ix in draws]
    result['po_ci95'] = ci([x['po'] for x in boots])
    result['kappa_ci95'] = ci([x['kappa'] for x in boots])
    result['bootstrap_replicates'] = len(boots)
    result['undefined_kappa_replicates'] = sum(x['kappa'] is None for x in boots)
    return result, boots

def has(value, term):
    return term in value.split(' | ')

def main():
    units = read('sample/units.json')['units']
    ca = read('coding/coder-a.json')
    cb = read('coding/coder-b.json')
    a = {r['unit_id']: r for r in ca['rows']}
    b = {r['unit_id']: r for r in cb['rows']}
    assert len(a) == len(b) == len(units) == 198
    assert set(a) == set(b) == {u['unit_id'] for u in units}
    for coder in (a, b):
        for r in coder.values():
            assert r['S3']['contribution'] == r['S2'], r['unit_id']
    baseline = read('sample/baseline.json')
    result = {
        'study': 'AF-RES-016', 'coefficient': 'nominal Cohen kappa',
        'point_weighting': 'each observed unit equally weighted',
        'ci': 'paired cluster percentile bootstrap, linear-interpolated .025/.975 quantiles',
        'cluster_units': {'011':'thread','012':'selected query','004':'base problem'},
        'seed': SEED, 'replicates': B,
        'undefined_rule': 'Exclude only undefined kappa replicates from kappa quantiles; keep all for Po.',
        'limits': ['Same-model internal codings, not human-rater sampling.',
            'Convenience corpora and 4/15/31 clusters do not establish nominal population coverage.',
            'S3 contribution reuses S2; schemes are not randomized independent interventions.'],
        'input_sha256': {p: sha256((BASE/p).read_bytes()).hexdigest() for p in
            ('CODEBOOK.md','sample/units.json','sample/baseline.json','coding/coder-a.json','coding/coder-b.json')},
        'main': [], 'sensitivities': [], 'strata_012': [], 'baseline': {},
        'exploratory_source_strata': [], 'parent_problem_012_sensitivity': [],
        'S3_decomposition': [], 'small_repeated_target_checks': [],
        'paired_011_differences': [], 'scheme_differences': [], 'cluster_details': [],
    }
    historic = {r['unit_id']: r for r in baseline['011_selected']}
    for s in ('011','012','004'):
        us = [u for u in units if u['sample'] == s]
        ids = [u['unit_id'] for u in us]
        clusters = [u['cluster'] for u in us]
        draws = resamples(clusters)
        boot_by_scheme = {}
        report_by_scheme = {}
        for scheme in SCHEMES:
            aa = [label(a[i],scheme) for i in ids]
            bb = [label(b[i],scheme) for i in ids]
            stats, boots = report(aa,bb,clusters,draws)
            result['main'].append({'sample':s,'scheme':scheme,**stats})
            boot_by_scheme[scheme] = boots
            report_by_scheme[scheme] = stats
            for name, keep in (
                ('drop_unknown_agreements',lambda x,y: not (x==y and has(x,'unknown'))),
                ('drop_any_unknown',lambda x,y: not (has(x,'unknown') or has(y,'unknown'))),
                ('drop_any_mixed',lambda x,y: not (has(x,'mixed') or has(y,'mixed'))),
                ('drop_any_unknown_or_mixed',lambda x,y: not any(has(z,t) for z in (x,y) for t in ('mixed','unknown'))),
            ):
                ix = [i for i in range(len(ids)) if keep(aa[i],bb[i])]
                result['sensitivities'].append({'sample':s,'scheme':scheme,'rule':name,
                    'excluded_n':len(ids)-len(ix),**point([aa[i] for i in ix],[bb[i] for i in ix])})
            for cl in sorted(set(clusters)):
                ix = [i for i,c in enumerate(clusters) if c==cl]
                result['cluster_details'].append({'sample':s,'cluster':cl,'scheme':scheme,
                    **point([aa[i] for i in ix],[bb[i] for i in ix])})
        for x,y in (('S2','S1'),('S3','S1'),('S3','S2')):
            delta = {}
            for metric in ('po','kappa'):
                xv,yv=report_by_scheme[x][metric],report_by_scheme[y][metric]
                vals=[p[metric]-q[metric] if p[metric] is not None and q[metric] is not None else None
                      for p,q in zip(boot_by_scheme[x],boot_by_scheme[y])]
                delta[metric+'_difference']=xv-yv if xv is not None and yv is not None else None
                delta[metric+'_difference_ci95']=ci(vals)
                delta[metric+'_undefined_replicates']=sum(v is None for v in vals)
            result['scheme_differences'].append({'sample':s,'contrast':x+' minus '+y,**delta})
        joint=report_by_scheme['S3']['agree']
        form=report_by_scheme['S3_form']['agree']
        contribution=report_by_scheme['S2']['agree']
        result['S3_decomposition'].append({'sample':s,'n':len(ids),'both_axes_agree':joint,
            'contribution_agrees_form_differs':contribution-joint,
            'form_agrees_contribution_differs':form-joint,
            'both_axes_differ':len(ids)-form-contribution+joint})
        if s=='011':
            old_a=[historic[i]['a'] for i in ids]
            old_b=[historic[i]['b'] for i in ids]
            old,old_boot=report(old_a,old_b,clusters,draws)
            result['baseline']['011_selected_120']=old
            for scheme in SCHEMES:
                delta={}
                for metric in ('po','kappa'):
                    delta[metric+'_difference']=report_by_scheme[scheme][metric]-old[metric]
                    vals=[p[metric]-q[metric] if p[metric] is not None and q[metric] is not None else None
                          for p,q in zip(boot_by_scheme[scheme],old_boot)]
                    delta[metric+'_difference_ci95']=ci(vals)
                    delta[metric+'_undefined_replicates']=sum(v is None for v in vals)
                result['paired_011_differences'].append({'scheme':scheme,**delta})
    old_all=baseline['011_all']
    result['baseline']['011_all_149']=report([r['a'] for r in old_all],[r['b'] for r in old_all],[r['cluster'] for r in old_all])[0]
    bm={r['unit_id']:r for r in baseline['012_selected']}
    for fallback in (False,True):
        us=[u for u in units if u['sample']=='012' and bm[u['unit_id']]['fallback_query']==fallback]
        for scheme in SCHEMES:
            stats,_=report([label(a[u['unit_id']],scheme) for u in us],
                           [label(b[u['unit_id']],scheme) for u in us],[u['cluster'] for u in us])
            result['strata_012'].append({'stratum':'random_query_fallback' if fallback else 'historical_qrel_query','scheme':scheme,**stats})
    # Defined from source URLs, not from observed agreement or coder labels.
    registry=[u for u in units if u['sample']=='012' and any(h in u['source']['url'] for h in ('registry.npmjs.org/','pypi.org/pypi/'))]
    for scheme in SCHEMES:
        stats,_=report([label(a[u['unit_id']],scheme) for u in registry],
                       [label(b[u['unit_id']],scheme) for u in registry],[u['cluster'] for u in registry])
        result['exploratory_source_strata'].append({'stratum':'012 registry-origin URL, npm/PyPI','scheme':scheme,**stats})
    parent_path=BASE/'evidence/query-parent-map.json'
    if parent_path.exists():
        parent=json.loads(parent_path.read_text())['query_to_problem']
        us=[u for u in units if u['sample']=='012']
        for scheme in SCHEMES:
            stats,_=report([label(a[u['unit_id']],scheme) for u in us],
                           [label(b[u['unit_id']],scheme) for u in us],[parent[u['cluster']] for u in us])
            result['parent_problem_012_sensitivity'].append({'scheme':scheme,**stats})
    result['pooled_descriptive_only']=[{'scheme':sc,**point([label(a[u['unit_id']],sc) for u in units],[label(b[u['unit_id']],sc) for u in units])} for sc in SCHEMES]
    for first,second,why in (
        ('011-T023-001','011-T023-002','same Form Tools name, same problem; not cross-problem invariance'),
        ('011-T041-001','012-alternativeto','same AlternativeTo name, different problem; second context was random fallback'),
        ('004-R08','004-R18','explicitly same SQS FIFO configuration with changed H3; not a pure context experiment'),
    ):
        item={'unit_pair':[first,second],'interpretation_limit':why,'coders':{}}
        for coder_name,coder in (('a',a),('b',b)):
            item['coders'][coder_name]={sc:{'first':label(coder[first],sc),'second':label(coder[second],sc),
                'same':label(coder[first],sc)==label(coder[second],sc)} for sc in SCHEMES}
        result['small_repeated_target_checks'].append(item)
    disagreements=[]
    for u in units:
        uid=u['unit_id']
        different=[sc for sc in SCHEMES if label(a[uid],sc)!=label(b[uid],sc)]
        if different:
            disagreements.append({'unit_id':uid,'sample':u['sample'],'cluster':u['cluster'],
                'different':different,'a':a[uid],'b':b[uid],
                'evidence_location':'sample/units.json#'+uid})
    disagreements.sort(key=lambda r:r['unit_id'])
    assert len(disagreements)>=30, 'Less than 30 unique disagreements: do not fabricate additional pairs.'
    # Thirty evenly spaced sorted unique IDs, including both endpoints.
    ix=[round(i*(len(disagreements)-1)/29) for i in range(30)]
    assert len(set(ix))==30
    selected=[disagreements[i]['unit_id'] for i in ix]
    result['disagreement_unique_n']=len(disagreements)
    result['impact_selected_ids']=selected
    save('evidence/agreement.json',result)
    save('evidence/disagreements.json',{'rows':disagreements})
    save('evidence/impact-selection.json',{'selection':'round(i*(N-1)/29) for i=0..29, sorted unique disagreement unit IDs','N':len(disagreements),'indices':ix,'unit_ids':selected})
    # A deliberately restrictive, hypothetical retrieval gate, NOT a valid H rule.
    # Compare with the fixed prior researcher's document-based expectations only.
    expected={r['row_id']:r for r in baseline['004_expected']}
    gate_rows=[]
    for coder_name,coder in (('a',a),('b',b)):
        for u in units:
            if u['sample']!='004':continue
            uid=u['unit_id'];old=expected[uid.split('-')[-1]]
            gate_rows.append({'coder':coder_name,'unit_id':uid,'S1':coder[uid]['S1'],'S2':coder[uid]['S2'],
                'hypothetical_product_only_gate':coder[uid]['S1']=='product',
                'hypothetical_whole_contribution_gate':coder[uid]['S2']=='whole',
                'prior_document_expectation':old['label'],
                'known_documented_case_lost_by_product_gate':old['label']=='DIRECT_DOCUMENTED' and coder[uid]['S1']!='product',
                'known_mismatch_admitted_by_product_gate':old['label']=='SURFACE_OR_CONSTRAINT_MISMATCH' and coder[uid]['S1']=='product'})
    save('evidence/role-filter-counterexample.json',{'level':'D3-run of an H counterfactual gate; not observed user behavior or software execution',
        'reference':'004 EXPECTED.json at 2b798c7d2b7355b649691c18de196104ceabb0f0; researcher-made document expectations, not ground truth',
        'rule':'Require S1=product to consider a whole selected-scope alternative; intentionally test why that inference is invalid.',
        'rows':gate_rows})
    print(json.dumps({'rows':len(units),'main':[{'sample':x['sample'],'scheme':x['scheme'],'agree':x['agree'],'n':x['n'],'po':x['po'],'kappa':x['kappa'],'po_ci95':x['po_ci95'],'kappa_ci95':x['kappa_ci95']} for x in result['main']],'unique_disagreements':len(disagreements),'impact_selected_ids':selected},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
