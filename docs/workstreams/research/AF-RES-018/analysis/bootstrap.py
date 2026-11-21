"""Paired question-cluster percentile intervals. Never treat claims as questions."""
import math,random,statistics
from functools import lru_cache
import numpy as np
from common import quantile

@lru_cache(maxsize=80)
def sample_indices(n,iterations,seed):
    rng=random.Random(seed)
    return np.array([[rng.randrange(n) for i in range(n)] for j in range(iterations)],dtype=np.int32)

def value(rows,kind,numerator=None,denominator=None,field=None):
    if kind=='ratio':
        n=sum(r.get(numerator,0) or 0 for r in rows)
        d=sum(r.get(denominator,0) or 0 for r in rows)
        return n/d if d else None
    xs=[r[field] for r in rows if r.get(field) is not None]
    if not xs:return None
    if kind=='mean':return statistics.mean(xs)
    if kind=='median':return statistics.median(xs)
    raise ValueError(kind)

def paired_interval(pairs,kind,numerator=None,denominator=None,field=None,iterations=10000,seed=18018):
    """Each pair contains A/P rows from one question; duplication keeps its claims together."""
    if not pairs:return {'A':None,'P':None,'difference':None,'ci95':[None,None],
                         'questions':0,'iterations':iterations,'valid_replicates':0,'seed':seed}
    def statistic(ps,condition):return value([p[condition] for p in ps],kind,numerator,denominator,field)
    a,p=statistic(pairs,'A'),statistic(pairs,'P');indices=sample_indices(len(pairs),iterations,seed)
    estimates={}
    for condition in ['A','P']:
        rows=[pair[condition] for pair in pairs]
        if kind=='ratio':
            ns=np.array([r.get(numerator,0) or 0 for r in rows],dtype=float)[indices].sum(axis=1)
            ds=np.array([r.get(denominator,0) or 0 for r in rows],dtype=float)[indices].sum(axis=1)
            estimates[condition]=np.divide(ns,ds,out=np.full(iterations,np.nan),where=ds>0)
        else:
            values=np.array([np.nan if r.get(field) is None else r[field] for r in rows],dtype=float)[indices]
            estimates[condition]=(np.nanmean if kind=='mean' else np.nanmedian)(values,axis=1)
    deltas=estimates['P']-estimates['A'];differences=deltas[np.isfinite(deltas)].tolist()
    return {'A':a,'P':p,'difference':p-a if a is not None and p is not None else None,
            'ci95':[quantile(differences,0.025),quantile(differences,0.975)],
            'questions':len(pairs),'iterations':iterations,'valid_replicates':len(differences),
            'seed':seed,'unit':'question; paired A/P; all sampled claims within question retained',
            'backend':'NumPy reductions over cached Python Random(seed) bootstrap indices',
            'small_stratum':len(pairs)<5,
            'limits':'Conditional on this purposive sample and one execution per condition/question; not population sampling or model-repetition uncertainty.'}
